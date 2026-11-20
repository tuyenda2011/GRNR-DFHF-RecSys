"""Regenerate separate validation figures and tables under reports/val/.

Ranking figures use checkpoint inference. Full EASE uses its recorded predictions
unless --refit-full-ease is specified. The test split is not used.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
import pyarrow  # noqa: F401 -- load Arrow DLLs before Torch on Windows

from scripts.compare_val_runs import holm_adjust, paired_bootstrap
from scripts.summarize_results import collect
from scripts.train_model import DENSITIES, normalize_history

# Fixed identity per model (reference categorical palette, slots 1-5 in validated order); shapes and
# solid/dashed (hatched) styles are the secondary encoding. Proposed models solid, baselines dashed.
STYLE = {
    "grnr": {"label": "GRNR (đề xuất)", "short": "GRNR", "color": "#2a78d6", "marker": "o", "line": "-"},
    "dfhf": {"label": "DFHF (đề xuất)", "short": "DFHF", "color": "#eb6834", "marker": "s", "line": "-"},
    "lightgcn": {"label": "LightGCN", "short": "LightGCN", "color": "#1baf7a", "marker": "^", "line": "--"},
    "xsimgcl": {"label": "XSimGCL", "short": "XSimGCL", "color": "#eda100", "marker": "D", "line": "--"},
    "directau": {"label": "DirectAU", "short": "DirectAU", "color": "#e87ba4", "marker": "v", "line": "--"},
}
ORDER = ("dfhf", "lightgcn", "xsimgcl", "directau")
PROPOSED, BASELINES = ("grnr", "dfhf"), ("lightgcn", "xsimgcl", "directau")
FIGURE_METRICS = ("NDCG@20", "NDCG@10", "Recall@20", "Recall@10")
TABLE_METRICS = ("NDCG@10", "NDCG@20", "Recall@10", "Recall@20")
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
SPLIT = "validation"
SIZE = (6.4, 4.0)  # every figure uses the same canvas (16:10)


def slug(metric):
    return metric.lower().replace("@", "")


def vn(text):
    """Vietnamese number format: decimal comma and thousands dot ("7,671.0" -> "7.671,0")."""
    return text.translate(str.maketrans({",": ".", ".": ","}))


def vn_density(density):
    return vn(f"{density:.2f}")


class VNFormatter(matplotlib.ticker.ScalarFormatter):
    """Linear tick labels with a decimal comma; log axes keep their own formatter."""

    def __call__(self, x, pos=None):
        return vn(super().__call__(x, pos))


def style_axes(ax):
    ax.xaxis.set_major_formatter(VNFormatter())
    ax.yaxis.set_major_formatter(VNFormatter())
    ax.set_facecolor("white")
    ax.grid(axis="y", color=GRID, linewidth=.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelcolor=INK)


def setup():
    plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman"], "mathtext.fontset": "stix",
                         "font.size": 9, "axes.titlesize": 9.5, "axes.labelsize": 9,
                         "legend.fontsize": 8, "pdf.fonttype": 42, "ps.fonttype": 42, "figure.dpi": 100,
                         "axes.labelcolor": INK, "text.color": INK})


def save(fig, folder, name, notes):
    fig.savefig(folder / f"{name}.png", dpi=300, facecolor="white")
    plt.close(fig)
    notes.append(f"{name}: written")


def model_average(scores, model, density, metric):
    """Per-user metric averaged over the available seeds of one model, on the common user set."""
    runs = [value for (name, dens, _), value in scores.items() if name == model and dens == density]
    if not runs:
        return None, None
    common = runs[0][0]
    for users, *_ in runs[1:]:
        common = np.intersect1d(common, users)
    stacked = [pd.Series(values[metric], index=users).loc[common].to_numpy() for users, _, values, _ in runs]
    return common, np.mean(stacked, axis=0)


def read_history(path):
    file = Path(path) / "history.csv"
    return normalize_history(pd.read_csv(file)) if file.exists() else None


def table_dataset(full_train, validation, stats, folder):
    degree = full_train.groupby("u_idx").size()
    rows = [("Số user", stats["num_users"]), ("Số item", stats["num_items"]),
            ("Tương tác train", len(full_train)), ("Tương tác validation", len(validation)),
            ("Độ thưa train (%)", round(100 * (1 - len(full_train) / (stats["num_users"] * stats["num_items"])), 4)),
            ("Độ dài lịch sử user trung bình", round(degree.mean(), 2)),
            ("Độ dài lịch sử user trung vị", int(degree.median()))]
    pd.DataFrame(rows, columns=["Thống kê", "Giá trị"]).to_csv(folder / "B1_dataset.csv", index=False,
                                                                encoding="utf-8-sig")


def table_metrics(summary, folder, density):
    """All ranking metrics at one density: mean (and std when several seeds) per model."""
    rows = []
    for model in ORDER:
        values = summary[(summary.model == model) & (summary.density == density)]
        if values.empty:
            continue
        row = {"Mô hình": STYLE[model]["label"], "Số seed": len(values)}
        for metric in TABLE_METRICS:
            row[metric] = round(values[metric].mean(), 5)
            if len(values) > 1:
                row[f"{metric} std"] = round(values[metric].std(), 5)
        rows.append(row)
    pd.DataFrame(rows).to_csv(folder / f"B2a_metrics_d{round(density * 100)}.csv", index=False, encoding="utf-8-sig")


def table_density(summary, folder):
    """One row per model, one column per density and metric (mean over seeds)."""
    rows = []
    for model in ORDER:
        row = {"Mô hình": STYLE[model]["label"]}
        for density in sorted(DENSITIES, reverse=True):
            for metric in ("NDCG@20", "Recall@20"):
                values = summary[(summary.model == model) & (summary.density == density)][metric]
                row[f"{metric} d={density:.2f}"] = round(values.mean(), 5) if len(values) else None
        rows.append(row)
    pd.DataFrame(rows).to_csv(folder / "B2b_by_density.csv", index=False, encoding="utf-8-sig")


def table_training(summary, folder, density):
    """Best versus last epoch (no early stopping), epochs run and seconds per epoch, from history.csv."""
    rows = []
    for model in ORDER:
        for run in summary[(summary.model == model) & (summary.density == density)].itertuples():
            history = read_history(run.path)
            row = {"Mô hình": STYLE[model]["label"], "Seed": run.seed, "NDCG@20 tốt nhất": round(summary.at[run.Index, "NDCG@20"], 5)}
            if history is not None and "NDCG@20" in history:
                best = history["NDCG@20"].idxmax()
                row.update({"Epoch tốt nhất": int(history["epoch"][best]), "Số epoch đã chạy": int(history["epoch"].iloc[-1]),
                            "NDCG@20 epoch cuối": round(history["NDCG@20"].iloc[-1], 5),
                            "Giây/epoch": round(history["seconds"].mean(), 1) if "seconds" in history else None})
            rows.append(row)
    if rows:
        table = pd.DataFrame(rows)
        for column in ("Epoch tốt nhất", "Số epoch đã chạy"):
            if column in table:
                table[column] = table[column].astype("Int64")  # GRNR (closed form) leaves these empty
        table.to_csv(folder / f"B4_training_d{round(density * 100)}.csv", index=False, encoding="utf-8-sig")


def table_tests(scores, folder, metric, name, density=1.0, repeats=10_000):
    """Paired user bootstrap, one-sided (proposed > baseline), Holm over the trained-group comparisons."""
    rows = []
    for proposed in ("dfhf",):
        for baseline in BASELINES:
            users_b, values_b = model_average(scores, proposed, density, metric)
            users_a, values_a = model_average(scores, baseline, density, metric)
            if values_a is None or values_b is None:
                continue
            common = np.intersect1d(users_a, users_b)
            a = pd.Series(values_a, index=users_a).loc[common].to_numpy()
            b = pd.Series(values_b, index=users_b).loc[common].to_numpy()
            rows.append({"proposed": proposed, "baseline": baseline, **paired_bootstrap(a, b, repeats=repeats)})
    if not rows:
        return
    adjusted = holm_adjust([row["p_one_sided"] for row in rows])
    pd.DataFrame([{"So sánh": f"{STYLE[r['proposed']]['short']} - {STYLE[r['baseline']]['short']}",
                   "Mật độ": density, f"Delta {metric}": round(r["delta"], 5),
                   "KTC 95% dưới": round(r["ci95"][0], 5), "KTC 95% trên": round(r["ci95"][1], 5),
                   "p một phía": round(r["p_one_sided"], 5), "p Holm": round(p, 5), "Số user": r["n_users"]}
                  for r, p in zip(rows, adjusted)]).to_csv(folder / f"{name}.csv", index=False, encoding="utf-8-sig")


# Retire only the mixed-group figures produced by earlier versions of this script.
OBSOLETE_FIGURES = (
    *(f"{prefix}_{slug(metric)}.png" for prefix in ("H1_density", "H2", "H4_retention", "H5_user_groups")
      for metric in FIGURE_METRICS),
    *(f"H3_learning_curves_{slug(metric)}.png" for metric in ("NDCG@10", "NDCG@20")),
    "H6a_popularity_trajectory.png", "H6b_coverage.png", "H7a_train_time.png",
    "H7b_inference_latency.png", "H8_ndcg_at_k.png",
)


def publish_report(staging, output, summary, *, trained, closed, refit_full_ease):
    manifest = {
        "created": datetime.now().isoformat(timespec="seconds"), "split": SPLIT,
        "groups": {"trained": trained, "closed_form": closed},
        "full_ease": ("refitted" if refit_full_ease else "recorded_predictions") if closed else None,
        "runs": summary[["model", "density", "seed", "path", "source"]].to_dict("records"),
    }
    (staging / "report_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    for source in sorted(staging.rglob("*")):
        if source.is_file():
            target = output / source.relative_to(staging)
            target.parent.mkdir(parents=True, exist_ok=True)
            source.replace(target)
    for name in OBSOLETE_FIGURES:
        (output / "figures" / name).unlink(missing_ok=True)


def main(argv=None):
    from scripts import make_closed_form_report, make_trained_group_report

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--results", type=Path, default=ROOT / "results/val")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/val")
    parser.add_argument("--bootstrap", type=int, default=10_000)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto",
                        help="Device for replaying the trained checkpoints")
    parser.add_argument("--refit-full-ease", action="store_true", help="Rebuild the dense EASE matrix before scoring")
    args = parser.parse_args(argv)
    if args.bootstrap < 1:
        parser.error("--bootstrap must be positive")
    summary = collect(args.results)
    if summary.empty:
        parser.error(f"No model results under {args.results}")
    trained = bool(summary.model.isin(ORDER).any())
    closed_runs = summary[summary.seed == make_closed_form_report.SEED]
    available = set(zip(closed_runs.model, closed_runs.density))
    required = {(model, density) for model in ("grnr", "ease", "gfcf") for density in DENSITIES}
    closed = required <= available
    if not closed:
        print("Closed-form report requires GRNR, EASE and GF-CF at all four densities (seed 42).", flush=True)
    if not trained and not closed:
        parser.error("No model group has sufficient results to draw figures")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".report-", dir=args.output.parent) as temporary:
        staging = Path(temporary)
        if trained:
            make_trained_group_report.generate(args.results, staging / "figures", args.device,
                                               tables=staging / "tables", bootstrap=args.bootstrap)
        if closed:
            make_closed_form_report.generate(args.results, staging, refit_full_ease=args.refit_full_ease,
                                             bootstrap=args.bootstrap)
        publish_report(staging, args.output, summary, trained=trained, closed=closed, refit_full_ease=args.refit_full_ease)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
