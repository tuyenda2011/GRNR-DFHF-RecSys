"""T6g: MostPop reference (rank candidates by retained-train count, mask full train history). Validation only."""
import json, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT))
from scripts.validation_io import load_validation_inputs
from src.data.quality_report import warm_cohort
from src.data.sparsity import create_sparse_train_set
_, full_train, validation, stats = load_validation_inputs(None, ROOT)
hist = full_train.groupby("u_idx").i_idx.agg(set).to_dict()
out = {}
for d in (1.0, 0.75, 0.5, 0.25):
    train = create_sparse_train_set(full_train, d, 42)
    warm, _ = warm_cohort(train, validation)
    deg = train.groupby("u_idx").size()
    counts = np.bincount(train.i_idx, minlength=stats["num_items"])
    order = np.argsort(-counts, kind="stable"); order = order[counts[order] > 0][:2000]
    nd, rc, d1 = [], [], []
    for u, t in zip(warm.u_idx, warm.i_idx):
        seen = hist.get(int(u), set()); top = [i for i in order if i not in seen][:20]
        r = top.index(t) if t in top else -1
        nd.append(1/np.log2(r+2) if r >= 0 else 0.); rc.append(1. if r >= 0 else 0.); d1.append(deg.get(u, 0) == 1)
    nd, rc, d1 = map(np.array, (nd, rc, d1))
    out[str(d)] = {"NDCG@20": float(nd.mean()), "Recall@20": float(rc.mean()),
                   "NDCG@20_deg1": float(nd[d1].mean()) if d1.any() else None, "NDCG@20_deg2plus": float(nd[~d1].mean()), "n": int(len(nd))}
    print(d, out[str(d)])
(Path(__file__).parent / "t6g_mostpop.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
