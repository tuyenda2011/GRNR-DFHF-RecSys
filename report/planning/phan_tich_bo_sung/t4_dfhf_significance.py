"""T4: DFHF minus each trained-group baseline, NDCG@20, per density; family of 3 per density, Holm.
Same paired_bootstrap/holm_adjust calls as make_closed_form_report.table_tests (B6). Validation only. Post hoc."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT))
from scripts.compare_val_runs import holm_adjust, paired_bootstrap, per_user_metrics
from scripts.validation_io import load_validation_inputs
RUNS = {"DFHF": "sphr", "LightGCN": "lightgcn", "XSimGCL": "xsimgcl", "DirectAU": "directau"}
_, _, validation, _ = load_validation_inputs(None, ROOT)
targets = dict(zip(validation.u_idx.astype(int), validation.i_idx.astype(int)))
def scores(folder, d):
    run = ROOT / "results" / folder / f"d{round(d*100)}" / "seed42"
    users = np.load(run / "val_users.npy").astype(np.int64); pred = np.load(run / "val_predictions.npy").astype(np.int64)
    truth = np.array([targets[int(u)] for u in users]); return pd.Series(dict(per_user_metrics(pred, truth))["NDCG@20"], index=users)
rows = []
for d in (0.25, 0.5, 0.75, 1.0):
    ref = scores(RUNS["DFHF"], d); block = []
    for name in ("LightGCN", "XSimGCL", "DirectAU"):
        other = scores(RUNS[name], d); common = ref.index.intersection(other.index)
        t = paired_bootstrap(other.loc[common].to_numpy(float), ref.loc[common].to_numpy(float), repeats=10_000)
        block.append({"So sánh": f"DFHF - {name}", "Mật độ": d, **t})
    for r, p in zip(block, holm_adjust([r["p_one_sided"] for r in block])): r["p_holm"] = p
    rows += block
df = pd.DataFrame([{"So sánh": r["So sánh"], "Mật độ": r["Mật độ"], "Delta NDCG@20": round(r["delta"], 5),
                    "KTC 95% dưới": round(r["ci95"][0], 5), "KTC 95% trên": round(r["ci95"][1], 5),
                    "p một phía": round(r["p_one_sided"], 5), "p Holm": round(r["p_holm"], 5), "Số user": r["n_users"]} for r in rows])
df.to_csv(Path(__file__).parent / "T4_dfhf_significance.csv", index=False, encoding="utf-8-sig"); print(df.to_string())
