"""T6h: each model minus MostPop (NDCG@20), paired user bootstrap, per density. Descriptive reference, post hoc,
no multiplicity correction; MostPop ranks retained-train candidates by retained count and masks full-train history."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT))
from scripts.compare_val_runs import paired_bootstrap, per_user_metrics
from scripts.validation_io import load_validation_inputs
from src.data.sparsity import create_sparse_train_set
RUNS = {"GRNR": "sgkr", "EASE (đầy đủ)": "ease", "GF-CF": "gfcf", "DFHF": "sphr", "LightGCN": "lightgcn", "XSimGCL": "xsimgcl", "DirectAU": "directau"}
_, full_train, validation, stats = load_validation_inputs(None, ROOT)
targets = dict(zip(validation.u_idx.astype(int), validation.i_idx.astype(int)))
hist = full_train.groupby("u_idx").i_idx.agg(set).to_dict()
rows = []
for d in (0.25, 0.5, 0.75, 1.0):
    train = create_sparse_train_set(full_train, d, 42)
    counts = np.bincount(train.i_idx, minlength=stats["num_items"])
    order = np.argsort(-counts, kind="stable"); order = order[counts[order] > 0][:2000]
    users = np.load(ROOT / "results/sphr" / f"d{round(d*100)}" / "seed42/val_users.npy").astype(np.int64)
    pop = np.array([[i for i in order if i not in hist.get(int(u), set())][:20] for u in users], dtype=np.int64)
    truth = np.array([targets[int(u)] for u in users])
    base = pd.Series(dict(per_user_metrics(pop, truth))["NDCG@20"], index=users)
    rows.append({"Mô hình": "MostPop", "Mật độ": d, "NDCG@20": round(base.mean(), 5)})
    for name, folder in RUNS.items():
        run = ROOT / "results" / folder / f"d{round(d*100)}" / "seed42"
        u = np.load(run / "val_users.npy").astype(np.int64); p = np.load(run / "val_predictions.npy").astype(np.int64)
        s = pd.Series(dict(per_user_metrics(p, np.array([targets[int(x)] for x in u])))["NDCG@20"], index=u)
        c = s.index.intersection(base.index)
        t = paired_bootstrap(base.loc[c].to_numpy(float), s.loc[c].to_numpy(float), repeats=10_000)
        rows.append({"Mô hình": name, "Mật độ": d, "NDCG@20": round(s.mean(), 5), "Delta so với MostPop": round(t["delta"], 5),
                     "KTC 95% dưới": round(t["ci95"][0], 5), "KTC 95% trên": round(t["ci95"][1], 5)})
df = pd.DataFrame(rows); df.to_csv(Path(__file__).parent / "T6h_vs_mostpop.csv", index=False, encoding="utf-8-sig"); print(df.to_string())
