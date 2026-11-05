"""T6f: per-user NDCG@20 at each density, split by retained-train degree (1 vs >=2). Validation only."""
import json, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT))
from scripts.validation_io import load_validation_inputs
from src.data.quality_report import warm_cohort
from src.data.sparsity import create_sparse_train_set
RUNS = {"dfhf": "sphr", "lightgcn": "lightgcn", "xsimgcl": "xsimgcl", "directau": "directau",
        "grnr": "sgkr", "ease": "ease", "gfcf": "gfcf"}
_, full_train, validation, _ = load_validation_inputs(None, ROOT)
out = {}
for d in (0.75, 0.5, 0.25):
    train = create_sparse_train_set(full_train, d, 42)
    warm, _ = warm_cohort(train, validation)
    warm = warm.sort_values("u_idx")
    target = dict(zip(warm.u_idx, warm.i_idx))
    deg = train.groupby("u_idx").size()
    out[str(d)] = {}
    for name, folder in RUNS.items():
        run = ROOT / "results" / folder / f"d{round(d*100)}" / "seed42"
        if not (run / "val_predictions.npy").is_file():
            continue
        users = np.load(run / "val_users.npy"); pred = np.load(run / "val_predictions.npy")
        t = np.array([target[int(u)] for u in users])
        hit = pred == t[:, None]
        ndcg = (hit / np.log2(np.arange(2, 22))).sum(1)
        g = deg.reindex(users).to_numpy() == 1
        out[str(d)][name] = {"n_deg1": int(g.sum()), "ndcg20_deg1": float(ndcg[g].mean()),
                             "n_deg2plus": int((~g).sum()), "ndcg20_deg2plus": float(ndcg[~g].mean()),
                             "ndcg20_all": float(ndcg.mean())}
(Path(__file__).parent / "t6f_degree_split.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
for d, r in out.items():
    print(d); [print(f"  {k:9s} deg1 {v['ndcg20_deg1']:.5f} (n={v['n_deg1']})  deg2+ {v['ndcg20_deg2plus']:.5f}  all {v['ndcg20_all']:.5f}") for k, v in r.items()]
