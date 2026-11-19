"""Supplementary report: GRNR against the closed-form baselines only (EASE, EASE top-128, GF-CF).

  python scripts/make_closed_form_report.py

Writes next to the main report without touching it. The figures are the main report's own types (same
drawing code, make_combined_figures.bar_figure), restricted to these four models:
  reports/val/tables/B5_closed_form.csv                   metrics, train time and checkpoint size, all four densities
  reports/val/tables/B6_closed_form_significance.csv      GRNR minus each model: paired bootstrap, Holm over 3 per density
  reports/val/figures/H1_closed_form_density_<metric>.png as H1
  reports/val/figures/H4_closed_form_retention_<metric>.png as H4
  reports/val/figures/H5_closed_form_user_groups_<metric>.png as H5
  reports/val/figures/H7a_closed_form_train_time.png      as H7a
  reports/val/figures/H7c_closed_form_checkpoint_size.png as H7a, checkpoint size instead of train time
  reports/val/figures/H8_closed_form_ndcg_at_k.png        as H8

GRNR, GF-CF and EASE top-128 are evaluated from checkpoints. Full EASE uses its
recorded predictions unless --refit-full-ease is supplied, since its dense matrix was not saved.
Exploratory: this comparison family was defined after the results were seen. Validation split only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import numpy as np
import pandas as pd
import pyarrow  # noqa: F401 -- load Arrow DLLs before Torch on Windows

from scripts.compare_val_runs import holm_adjust, paired_bootstrap
from scripts.make_combined_figures import bar_figure, figure_groups, figure_ndcg_at_k
from scripts.make_report import FIGURE_METRICS, MUTED, setup, slug
from scripts.report_inference import report_device, rescore, saved_predictions, score_rows, validation_sample
from scripts.validation_io import load_validation_inputs
from src.utils.model_names import resolve_model_run

SEED = 42
DENSITIES = (0.25, 0.5, 0.75, 1.0)
METRICS = ("NDCG@10", "NDCG@20", "Recall@10", "Recall@20")
RIVALS = ("ease", "ease128", "gfcf")
ARMS = ("grnr", *RIVALS)
# Same keys as make_report.STYLE; baselines are hatched/dashed by the drawing code (only GRNR is proposed here).
STYLE = {"grnr": {"label": "GRNR (đề xuất)", "color": "#2a78d6", "marker": "o", "line": "-"},
         "ease": {"label": "EASE (đầy đủ)", "color": "#7a5cc7", "marker": "D", "line": "--"},
         "ease128": {"label": "EASE top-128", "color": "#b39ae6", "marker": "d", "line": ":"},
         "gfcf": {"label": "GF-CF", "color": "#8c6d46", "marker": "s", "line": "--"}}


def run_dir(model, density, results):
    folder = "ease" if model == "ease128" else model
    return resolve_model_run(results, folder, density, SEED)


def checkpoint_mb(model, density, results, num_items):
    if model == "ease":
        return num_items * num_items * 4 / 2**20  # dense float32 item-item matrix, not stored
    return (run_dir(model, density, results) / "checkpoint.npz").stat().st_size / 2**20


def table_tests(scores, repeats=10_000):
    rows = []
    for density in DENSITIES:
        users, _, values, _ = scores[("grnr", density, SEED)]
        reference = pd.Series(values["NDCG@20"], index=users)
        block = []
        for model in RIVALS:
            users, _, values, _ = scores[(model, density, SEED)]
            other = pd.Series(values["NDCG@20"], index=users)
            common = reference.index.intersection(other.index)
            test = paired_bootstrap(other.loc[common].to_numpy(float), reference.loc[common].to_numpy(float),
                                    repeats=repeats)
            block.append({"model": model, "Mật độ": density, **test})
        for row, p in zip(block, holm_adjust([row["p_one_sided"] for row in block])):
            row["p_holm"] = p
        rows += block
    return pd.DataFrame(rows)


def figures(table, scores, full_train, folder, notes):
    """H1, H4, H5, H7 and H8 for the four closed-form models (same code and layout as the main report)."""
    values = table.set_index(["model", "Mật độ"])

    def lookup(column):
        return lambda model, density: float(values.at[(model, density), column])
    kwargs = {"order": ARMS, "style": STYLE, "ncol": 4}
    for metric in FIGURE_METRICS:
        bar_figure(lookup(metric), metric, f"H1_closed_form_density_{slug(metric)}", folder, notes, **kwargs)
        bar_figure(lambda m, d, metric=metric: 100 * values.at[(m, d), metric] / values.at[(m, 1.0), metric],
                   f"{metric} so với mật độ 1.00 (%)", f"H4_closed_form_retention_{slug(metric)}", folder, notes,
                   fmt="{:.1f}", extra=lambda ax: ax.axhline(100, color=MUTED, linestyle="--", linewidth=.8, zorder=0),
                   **kwargs)
        figure_groups(scores, full_train, metric, folder, notes, name="H5_closed_form_user_groups", **kwargs)
    figure_ndcg_at_k(scores, folder, notes, name="H8_closed_form_ndcg_at_k", **kwargs)
    bar_figure(lookup("train_seconds"), "Thời gian huấn luyện (giây, thang log)\nTất cả chạy trên CPU; "
               "EASE top-128 = EASE + cắt", "H7a_closed_form_train_time", folder, notes, fmt="{:,.0f}", log=True,
               **kwargs)
    bar_figure(lookup("Checkpoint (MB)"), "Dung lượng checkpoint (MB, thang log)\nEASE đầy đủ: ma trận float32, "
               "không lưu", "H7c_closed_form_checkpoint_size", folder, notes, fmt="{:,.1f}", log=True, **kwargs)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=ROOT / "results/val")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/val")
    parser.add_argument("--refit-full-ease", action="store_true", help="Rebuild the dense EASE matrix before scoring")
    args = parser.parse_args(argv)
    generate(args.results, args.output, refit_full_ease=args.refit_full_ease)


def generate(results, reports, *, refit_full_ease=False, bootstrap=10_000):
    device = report_device("cpu")
    if refit_full_ease:
        import psutil

        from scripts.run_ease import ease_memory_required

    _, full_train, validation, stats = load_validation_inputs(None, ROOT)
    if refit_full_ease and psutil.virtual_memory().available < ease_memory_required(stats["num_items"]):
        raise MemoryError("Refitting full EASE requires about 9 GiB of available RAM")
    if not refit_full_ease:
        for density in DENSITIES:
            folder = run_dir("ease", density, results)
            if any(not (folder / file).is_file() for file in ("val_users.npy", "val_predictions.npy")):
                raise FileNotFoundError(f"Full EASE predictions missing in {folder}. Provide them or use --refit-full-ease.")
    (reports / "figures").mkdir(parents=True, exist_ok=True)
    (reports / "tables").mkdir(parents=True, exist_ok=True)
    setup()
    targets = dict(zip(validation.u_idx.astype(int), validation.i_idx.astype(int)))
    scores, rows = {}, []
    for density in DENSITIES:
        train, warm = validation_sample(full_train, validation, density)
        for model in ARMS:
            folder = run_dir(model, density, results)
            run = json.loads((folder / "metrics.json").read_text(encoding="utf-8"))
            if model == "ease" and not refit_full_ease:
                print(f"Recorded full EASE predictions: density={density:.0%}", flush=True)
                users, predictions = saved_predictions(folder)
                metrics = run["val_metrics"]
            else:
                print(f"Validation inference: {model}, density={density:.0%}", flush=True)
                l2 = run["config"]["l2"] if model == "ease" else None
                users, predictions, metrics = rescore(model, folder, train, full_train, warm, stats, device,
                                                      full_ease_l2=l2)
            scores[(model, density, SEED)] = score_rows(users, predictions, targets)
            rows.append({"Mô hình": STYLE[model]["label"], "model": model, "Mật độ": density,
                         **{m: metrics[m] for m in METRICS}, "train_seconds": run["train_seconds"],
                         "Checkpoint (MB)": checkpoint_mb(model, density, results, stats["num_items"])})
    table = pd.DataFrame(rows)
    table.drop(columns="model").assign(**{"Train (phút)": (table.train_seconds / 60).round(1)}).drop(
        columns="train_seconds").round({**{m: 5 for m in METRICS}, "Checkpoint (MB)": 1}).to_csv(
        reports / "tables/B5_closed_form.csv", index=False, encoding="utf-8-sig", lineterminator="\n")
    tests = table_tests(scores, repeats=bootstrap)
    pd.DataFrame({"So sánh": "GRNR - " + tests.model.map(lambda m: STYLE[m]["label"]), "Mật độ": tests["Mật độ"],
                  "Delta NDCG@20": tests.delta.round(5), "KTC 95% dưới": [round(c[0], 5) for c in tests.ci95],
                  "KTC 95% trên": [round(c[1], 5) for c in tests.ci95], "p một phía": tests.p_one_sided.round(5),
                  "p Holm": tests.p_holm.round(5), "Số user": tests.n_users}
                 ).to_csv(reports / "tables/B6_closed_form_significance.csv", index=False, encoding="utf-8-sig",
                          lineterminator="\n")
    notes = []
    figures(table, scores, full_train, reports / "figures", notes)
    print("\n".join(notes))


if __name__ == "__main__":
    main()
