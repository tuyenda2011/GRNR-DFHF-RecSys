"""Benchmark tab back end, split into the report's two groups; the proposed models are never compared directly.

Test split, as in the report. Quality comes from results/test/summary_test.csv (scripts/evaluate_test.py);
training time and inference latency are those measured during training (results/val/summary.csv).
Paired tests are read from the report's test tables (reports/test/tables): B3 for DFHF against LightGCN,
XSimGCL and DirectAU, B5/B6 for GRNR against full EASE, EASE top-128 and GF-CF, so the page always shows
the report's own numbers.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from app.recommender import KINDS, LABELS, ROOT
from src.utils.model_names import canonical_model_name

MAIN = ("dfhf", "lightgcn", "xsimgcl", "directau")  # the trained group
PROPOSED, GRAPH = ("dfhf",), ("lightgcn", "xsimgcl", "directau")
METRICS = ("NDCG@20", "NDCG@10", "Recall@20", "Recall@10", "MRR@20")
TABLES = ROOT / "reports/test/tables"
SUMMARY = ROOT / "results/test/summary_test.csv"
COSTS = ROOT / "results/val/summary.csv"  # training time and latency, recorded when the models were trained


def read_summary(summary_path=None):
    """Test metrics per run, with the training cost of the same run; model IDs normalized for display."""
    summary = pd.read_csv(summary_path or SUMMARY)
    summary["model"] = summary.model.map(canonical_model_name)
    if COSTS.exists() and "train_seconds" not in summary:
        costs = pd.read_csv(COSTS)
        costs["model"] = costs.model.map(canonical_model_name)
        costs = costs.groupby(["model", "density"], as_index=False)[["train_seconds", "inference_ms_per_user"]].mean()
        summary = summary.merge(costs, on=["model", "density"], how="left")
    return summary


def current_report_labels(frame):
    """Translate legacy display labels while preserving all numerical columns."""
    frame = frame.copy()
    for column in ("Mô hình", "So sánh"):
        if column in frame:
            frame[column] = frame[column].str.replace(
                r"\bSGKR\b", "GRNR", regex=True
            ).str.replace(r"\bSPHR\b", "DFHF", regex=True)
    return frame


def leaderboard(density, summary_path=None):
    """The trained group at this density, ranked by NDCG@20, with the gap to DFHF in percent."""
    summary = read_summary(summary_path)
    rows = summary[(summary.density == density) & summary.model.isin(MAIN)]
    rows = rows.groupby("model", sort=False)[[*METRICS, "train_seconds", "inference_ms_per_user"]].mean()
    table = rows.reindex([m for m in MAIN if m in rows.index]).reset_index()
    reference = table.loc[table.model == "dfhf", "NDCG@20"]
    table["vs DFHF"] = (table["NDCG@20"] / reference.iloc[0] - 1) * 100 if len(reference) else np.nan
    table = table.sort_values("NDCG@20", ascending=False).reset_index(drop=True)
    table.insert(0, "Hạng", range(1, len(table) + 1))
    table.insert(2, "Nhóm", table.model.map(KINDS))
    table["Mô hình"] = table.model.map(LABELS)
    return table


def by_density(summary_path=None):
    summary = read_summary(summary_path)
    summary = summary[summary.model.isin(MAIN)]
    return summary.groupby(["model", "density"], as_index=False)[[*METRICS, "train_seconds"]].mean()


def significance(density, targets=None):
    """Report table B3 at this density: DFHF minus each baseline of its group (bootstrap CI, one-sided p, Holm)."""
    path = TABLES / "B3_trained_significance.csv"
    if not path.exists():
        return pd.DataFrame()
    table = current_report_labels(pd.read_csv(path, encoding="utf-8-sig"))
    table = table[np.isclose(table["Mật độ"], density)]
    keys = {label.lower(): model for model, label in LABELS.items()}
    rows = []
    for _, row in table.iterrows():
        baseline = keys[row["So sánh"].split(" - ")[-1].strip().lower()]
        p, low, high = row["p Holm"], row["KTC 95% dưới"], row["KTC 95% trên"]
        rows.append({"proposed": "dfhf", "baseline": baseline, "delta": row["Delta NDCG@20"], "ci95": (low, high),
                     "p_one_sided": row["p một phía"], "p_holm": p, "n_users": int(row["Số user"]),
                     "verdict": "DFHF tốt hơn" if p < .05 and low > 0 else "Baseline tốt hơn" if high < 0
                     else "Chưa khác biệt có ý nghĩa"})
    return pd.DataFrame(rows)


def closed_form_all():
    """Report table B5 for every density (for the closed-form charts), or None before the report has run."""
    path = TABLES / "B5_closed_form.csv"
    return current_report_labels(pd.read_csv(path, encoding="utf-8-sig")) if path.exists() else None


def closed_form(density):
    """Report tables B5 (metrics, size, time) and B6 (GRNR minus each closed-form model) at one density."""
    metrics, tests = TABLES / "B5_closed_form.csv", TABLES / "B6_closed_form_significance.csv"
    if not metrics.exists() or not tests.exists():
        return None, None
    b5 = current_report_labels(pd.read_csv(metrics, encoding="utf-8-sig"))
    b6 = current_report_labels(pd.read_csv(tests, encoding="utf-8-sig"))
    b5, b6 = b5[np.isclose(b5["Mật độ"], density)], b6[np.isclose(b6["Mật độ"], density)]
    b6 = b6.assign(**{"Kết luận": [
        "GRNR tốt hơn" if p < .05 and low > 0 else "Mô hình này tốt hơn" if high < 0 else "Chưa khác biệt có ý nghĩa"
        for p, low, high in zip(b6["p Holm"], b6["KTC 95% dưới"], b6["KTC 95% trên"])]})
    return b5.reset_index(drop=True), b6.reset_index(drop=True)
