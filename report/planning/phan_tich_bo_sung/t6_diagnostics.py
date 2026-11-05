"""T6 diagnostics for the report plan (validation only; never reads test labels).

(a) share of warm validation users whose retained train degree is 1, per density (R10)
(b) share of negative raw GRNR scores among each user's top-20, sampled users, d100 (R11)
(c) GF-CF and all-run environment/timing table (R13, R16)
(d) user/item degree distribution of the retained train per density (R21)
(e) whether locked baseline configs enable hard negatives (R22)

Run from the repository root:
  D:/Miniconda/envs/AML/python.exe report/planning/w1/t6_diagnostics.py
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.validation_io import load_validation_inputs  # noqa: E402
from src.data.quality_report import warm_cohort  # noqa: E402
from src.data.sparsity import create_sparse_train_set  # noqa: E402
from src.models.grnr import GRNR  # noqa: E402

OUT = Path(__file__).resolve().parent
DENSITIES = (1.0, 0.75, 0.5, 0.25)
RUNS = {"grnr": "sgkr", "dfhf": "sphr", "lightgcn": "lightgcn", "xsimgcl": "xsimgcl",
        "directau": "directau", "ease": "ease", "gfcf": "gfcf"}


def main():
    _, full_train, validation, stats = load_validation_inputs(None, ROOT)
    report = {"validation_only": True, "a_degree_one": {}, "d_degrees": {}, "c_runs": [], "e_hard_negatives": {}}

    for d in DENSITIES:
        train = create_sparse_train_set(full_train, d, 42)
        warm, _ = warm_cohort(train, validation)
        user_deg = train.groupby("u_idx").size()
        item_deg = train.groupby("i_idx").size()
        warm_deg = user_deg.reindex(warm.u_idx.unique()).fillna(0)
        report["a_degree_one"][str(d)] = {
            "warm_users": int(len(warm_deg)),
            "degree_one": int((warm_deg == 1).sum()),
            "degree_one_share": float((warm_deg == 1).mean()),
        }
        q = [0.25, 0.5, 0.75, 0.9, 0.99]
        report["d_degrees"][str(d)] = {
            "edges": int(len(train)),
            "users": int(user_deg.size), "items": int(item_deg.size),
            "user_degree_mean": float(user_deg.mean()),
            "user_degree_quantiles": dict(zip(map(str, q), map(float, user_deg.quantile(q)))),
            "user_degree_max": int(user_deg.max()),
            "item_degree_mean": float(item_deg.mean()),
            "item_degree_quantiles": dict(zip(map(str, q), map(float, item_deg.quantile(q)))),
            "item_degree_one_share": float((item_deg == 1).mean()),
        }

    # (b) GRNR at d100: raw score sign within top-20 (tilt applied for ranking, as in the evaluator).
    model = GRNR.load(ROOT / "results/sgkr/d100/seed42/checkpoint.npz")
    train = create_sparse_train_set(full_train, 1.0, 42)
    warm, _ = warm_cohort(train, validation)
    rng = np.random.default_rng(42)
    users = np.sort(rng.choice(warm.u_idx.unique(), size=3000, replace=False)).astype(np.int64)
    history = full_train.groupby("u_idx").i_idx.agg(list).to_dict()
    counts = np.asarray(model.interactions.sum(0)).ravel()
    tilt = (1.0 + counts) ** model.config.popularity_tilt
    candidates = counts > 0
    negative, total, users_with_negative = 0, 0, 0
    for start in range(0, len(users), 500):
        batch = users[start:start + 500]
        raw = model.score(batch, exclude_seen=False)
        ranked = raw * tilt
        ranked[:, ~candidates] = -np.inf
        for row, user in enumerate(batch):
            ranked[row, history.get(int(user), [])] = -np.inf
        top = np.argpartition(-ranked, 20, axis=1)[:, :20]
        signs = np.take_along_axis(raw, top, axis=1) < 0
        negative += int(signs.sum()); total += signs.size
        users_with_negative += int(signs.any(axis=1).sum())
    report["b_grnr_negative_top20"] = {"sampled_users": int(len(users)), "negative_share": negative / total,
                                       "users_with_any_negative_share": users_with_negative / len(users)}

    # (c) environment and timing for every run
    for name, folder in RUNS.items():
        for d in DENSITIES:
            path = ROOT / "results" / folder / f"d{round(d * 100)}" / "seed42" / "metrics.json"
            if not path.is_file():
                continue
            m = json.loads(path.read_text(encoding="utf-8"))
            env = m.get("env", {})
            report["c_runs"].append({"model": name, "density": d, "gpu": env.get("gpu"), "torch": env.get("torch"),
                                     "git_commit": env.get("git_commit"), "train_seconds": m.get("train_seconds"),
                                     "inference_ms_per_user": m.get("inference_ms_per_user"),
                                     "best_epoch": m.get("best_epoch"), "epochs_run": m.get("epochs_run"),
                                     "config": {k: v for k, v in m.get("config", {}).items()
                                                if k not in ("dataset", "evaluation", "sparsity", "history_dir")}})

    # (e) hard negatives: keys mentioning 'hard' or 'disliked' in locked baseline configs
    for name in ("lightgcn", "xsimgcl", "directau"):
        m = json.loads((ROOT / "results" / name / "d100/seed42/metrics.json").read_text(encoding="utf-8"))
        text = json.dumps(m.get("config", {})).lower()
        report["e_hard_negatives"][name] = {"mentions_hard": "hard" in text, "mentions_disliked": "disliked" in text}

    (OUT / "t6_diagnostics.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("a_degree_one", "b_grnr_negative_top20", "e_hard_negatives")}, indent=2))


if __name__ == "__main__":
    main()
