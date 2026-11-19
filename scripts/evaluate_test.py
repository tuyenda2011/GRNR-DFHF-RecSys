"""Test evaluation of the 28 saved runs (7 models x 4 densities, seed 42) without any retraining.

Protocol: each model scores users exactly as in validation (its density's training graph, saved checkpoint).
Only the target and the mask change: the target is the test item, and the mask is the user's full-train
history plus the validation item. Test cohort = test targets whose user and item are in the density's
training graph (same warm rule as validation); candidates = items of that training graph.

Before scoring test, every run re-scores validation with the same code and compares NDCG@20 with its
metrics.json, so a different machine/library version that changes rankings is caught (--skip-val-check
turns this off). EASE: by default the exact dense matrix is recomputed from the same retained train
sample (deterministic closed form, ~11 min and ~9 GB RAM per density) because the reported validation
numbers come from that matrix; --ease checkpoint uses the saved top-128 matrix instead.

Outputs (resumable: finished runs are skipped):
  <output>/<model>/d<density>/seed42/metrics.json, test_predictions.npy, test_users.npy
  <output>/summary_test.csv

  python scripts/evaluate_test.py                       # all 28 runs
  python scripts/evaluate_test.py --models grnr ease --densities 1.0 0.5 --device cuda
"""
from __future__ import annotations

import argparse
import csv
import json
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import pyarrow  # noqa: F401 -- load Arrow DLLs before Torch on Windows
import torch

from src.data.bundle import BundleError, _inventory_path, sha256_file
from src.data.graph import get_norm_adj_tensor
from src.data.quality_report import warm_cohort
from src.data.sparsity import create_sparse_train_set
from src.evaluation.evaluator import EVALUATION_PROTOCOL, Evaluator
from src.evaluation.metrics import compute_topk_metrics
from src.utils.model_names import resolve_model_run

MODELS = ("grnr", "ease", "gfcf", "dfhf", "lightgcn", "xsimgcl", "directau")
DENSITIES = (1.0, 0.75, 0.5, 0.25)
METRICS = ("Recall@10", "NDCG@10", "MRR@10", "Recall@20", "NDCG@20", "MRR@20")
SEED = 42


def load_inputs(bundle_arg):
    """Train, validation, test and stats of the active bundle, each checksum-verified against its manifest."""
    from scripts.validation_io import load_validation_inputs
    bundle, full_train, validation, stats = load_validation_inputs(bundle_arg, ROOT)
    path = bundle.split_path("test")
    matches = [e for e in bundle.manifest.get("artifacts", []) if _inventory_path(bundle, e["path"]) == path.resolve()]
    if len(matches) != 1 or sha256_file(path) != matches[0].get("sha256"):
        raise BundleError(f"Missing or mismatched test checksum: {path}")
    return bundle, full_train, validation, pd.read_parquet(path), stats


def scorer(model, run, train, stats, device, ease_mode):
    """(user_table, item_table, score_fn, device) for the Evaluator, built from the run's saved artifact."""
    cpu = torch.device("cpu")
    empty = torch.empty(0)
    if model == "grnr":
        from src.models.grnr import GRNR
        grnr = GRNR.load(run / "checkpoint.npz")
        return empty, empty, grnr.get_user_rating_scores, cpu
    if model == "gfcf":
        from src.models.gfcf import GFCF
        gfcf = GFCF.load(run / "checkpoint.npz")
        return empty, empty, gfcf.get_user_rating_scores, cpu
    if model == "ease":
        from scipy import sparse
        from scripts.extra.run_item_baselines import ItemScores
        from src.models.grnr import GRNR
        x = GRNR.interaction_matrix(train.u_idx.to_numpy(), train.i_idx.to_numpy(),
                                    stats["num_users"], stats["num_items"])
        if ease_mode == "full":
            from scripts.config_io import read_model_config
            from scripts.run_ease import ease
            l2 = json.loads((run / "metrics.json").read_text(encoding="utf-8"))["config"]["l2"]
            if l2 != read_model_config(ROOT / "configs/ease.yaml", "ease")["l2"]:
                print(f"  note: using l2={l2} from metrics.json (differs from configs/ease.yaml)", flush=True)
            weights = ease(x, l2)
        else:
            weights = sparse.load_npz(run / "checkpoint.npz").astype(np.float32).tocsr()
        return empty, empty, ItemScores(x.astype(np.float32), weights).get_user_rating_scores, cpu
    if model == "dfhf":
        from src.models.dfhf import DFHF, DFHFConfig
        state = torch.load(run / "checkpoint.pt", map_location="cpu", weights_only=True)
        net = DFHF(stats["num_users"], stats["num_items"], DFHFConfig.from_dict(state["config"]))
        net.set_history(train.u_idx.to_numpy(), train.i_idx.to_numpy())
        net.load_state_dict(state["model_state_dict"])
        net.to(device).eval()
        with torch.no_grad():
            users, items = net()
        return users, items, net.get_user_rating_scores, device
    from scripts.rescore_neural_checkpoints import build_model
    state = torch.load(run / "checkpoint.pt", map_location="cpu", weights_only=False)
    net = build_model(model, state["config"], stats["num_users"], stats["num_items"])
    net.load_state_dict(state["model_state_dict"])
    net.to(device).eval()
    with torch.no_grad():
        users, items = net(get_norm_adj_tensor(train, stats["num_users"], stats["num_items"], device))
    return users, items, net.get_user_rating_scores, device


def rank(history, targets, train, stats, users, items, score_fn, device, batch):
    evaluator = Evaluator(history, targets, stats["num_users"], stats["num_items"], [10, 20], batch,
                          candidate_items=set(train.i_idx.unique()), popularity_df=history, score_fn=score_fn)
    with torch.no_grad():
        predictions, latency = evaluator.get_predictions(users, items, device)
    predictions = predictions.cpu()
    return evaluator, predictions, compute_topk_metrics(evaluator.ground_truth, predictions, [10, 20]), latency


def evaluate(model, density, data, args, device):
    full_train, validation, test, stats = data
    run = resolve_model_run(ROOT / "results", model, density, SEED)
    stored = json.loads((run / "metrics.json").read_text(encoding="utf-8"))
    train = create_sparse_train_set(full_train, density, SEED)
    started = time.perf_counter()
    users, items, score_fn, run_device = scorer(model, run, train, stats, device, args.ease)
    setup_seconds = time.perf_counter() - started

    val_check = None
    if not args.skip_val_check:
        warm_val, _ = warm_cohort(train, validation)
        _, _, val_metrics, _ = rank(full_train, warm_val, train, stats, users, items, score_fn, run_device,
                                    args.eval_batch_size)
        reference = stored["checkpoint_val_metrics"] if model == "ease" and args.ease == "checkpoint" \
            else stored["val_metrics"]
        diff = abs(val_metrics["NDCG@20"] - reference["NDCG@20"])
        val_check = {"NDCG@20": val_metrics["NDCG@20"], "stored_NDCG@20": reference["NDCG@20"],
                     "abs_diff": diff, "ok": diff <= args.tolerance}
        print(f"  val check NDCG@20 {val_metrics['NDCG@20']:.6f} vs stored {reference['NDCG@20']:.6f} "
              f"-> {'ok' if val_check['ok'] else 'MISMATCH'}", flush=True)
        if not val_check["ok"] and not args.allow_mismatch:
            raise AssertionError(f"{model} d{density}: validation NDCG@20 differs from metrics.json by {diff:.2e}; "
                                 "rankings on this machine differ from the original run (--allow-mismatch to continue)")

    # Test: same scores, mask = full train + validation item, target = test item.
    history = pd.concat([full_train[["u_idx", "i_idx"]], validation[["u_idx", "i_idx"]]], ignore_index=True)
    warm_test, cohort = warm_cohort(train, test)
    evaluator, predictions, metrics, latency = rank(history, warm_test, train, stats, users, items, score_fn,
                                                    run_device, args.eval_batch_size)
    return run, {"model": model, "density": density, "seed": SEED, "split": "test", "test_metrics": metrics,
                 "validation_metrics_stored": stored["val_metrics"], "validation_check": val_check,
                 "ease_matrix": args.ease if model == "ease" else None, "source_run": run.relative_to(ROOT).as_posix(),
                 "test_cohort": cohort, "evaluation_protocol": EVALUATION_PROTOCOL,
                 "mask": "full_train + validation item", "retrained": False,
                 "setup_seconds": setup_seconds, "seconds": time.perf_counter() - started,
                 "inference_ms_per_user": latency, "device": str(run_device),
                 "env": {"python": platform.python_version(), "torch": torch.__version__,
                         "os": platform.platform(), "cuda": torch.version.cuda}}, evaluator, predictions


def write_summary(output):
    rows = []
    for path in sorted(output.glob("*/d*/seed*/metrics.json")):
        result = json.loads(path.read_text(encoding="utf-8"))
        check = result.get("validation_check") or {}
        rows.append({"model": result["model"], "density": result["density"], "seed": result["seed"], "split": "test",
                     **result["test_metrics"], "val_NDCG@20_stored": result["validation_metrics_stored"]["NDCG@20"],
                     "val_check_ok": check.get("ok"), "evaluable_users": result["test_cohort"]["evaluable_users"],
                     "seconds": round(result["seconds"], 1), "path": path.parent.relative_to(output).as_posix()})
    rows.sort(key=lambda r: (MODELS.index(r["model"]), -r["density"]))
    if rows:
        with (output / "summary_test.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--models", nargs="+", choices=MODELS, default=list(MODELS))
    parser.add_argument("--densities", nargs="+", type=float, choices=DENSITIES, default=list(DENSITIES))
    parser.add_argument("--output", type=Path, default=ROOT / "results/test")
    parser.add_argument("--bundle", default=None)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto",
                        help="for DFHF/LightGCN/XSimGCL/DirectAU; closed-form models always run on CPU")
    parser.add_argument("--eval-batch-size", type=int, default=256)
    parser.add_argument("--ease", choices=("full", "checkpoint"), default="full")
    parser.add_argument("--skip-val-check", action="store_true")
    parser.add_argument("--tolerance", type=float, default=1e-4, help="allowed |val NDCG@20 - metrics.json|")
    parser.add_argument("--allow-mismatch", action="store_true", help="record a failed val check and continue")
    args = parser.parse_args(argv)
    device = torch.device("cuda" if args.device == "auto" and torch.cuda.is_available()
                          else "cpu" if args.device == "auto" else args.device)
    _, full_train, validation, test, stats = load_inputs(args.bundle)
    data = (full_train, validation, test, stats)
    jobs = [(m, d) for m in args.models for d in args.densities]
    print(f"{len(jobs)} runs, device {device}, test targets {len(test)}", flush=True)
    for index, (model, density) in enumerate(jobs, 1):
        target = args.output / model / f"d{round(density * 100)}" / f"seed{SEED}"
        if (target / "metrics.json").exists():
            print(f"[{index}/{len(jobs)}] {model} d{density}: already done, skipped", flush=True)
            continue
        print(f"[{index}/{len(jobs)}] {model} d{density}: start", flush=True)
        _, result, evaluator, predictions = evaluate(model, density, data, args, device)
        target.mkdir(parents=True, exist_ok=True)
        np.save(target / "test_predictions.npy", predictions.numpy().astype(np.int64, copy=False))
        np.save(target / "test_users.npy", np.asarray(evaluator.eval_users, dtype=np.int64))
        (target / "metrics.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        m = result["test_metrics"]
        print(f"[{index}/{len(jobs)}] {model} d{density}: test NDCG@20={m['NDCG@20']:.5f} "
              f"Recall@20={m['Recall@20']:.5f} in {result['seconds'] / 60:.1f} min", flush=True)
        if device.type == "cuda":
            torch.cuda.empty_cache()
    rows = write_summary(args.output)
    print(f"summary: {args.output / 'summary_test.csv'} ({len(rows)} runs)", flush=True)


if __name__ == "__main__":
    main()
