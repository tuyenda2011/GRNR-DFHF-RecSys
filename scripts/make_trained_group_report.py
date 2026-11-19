"""Replay trained checkpoints and draw the DFHF, LightGCN, XSimGCL and DirectAU figures.

  python scripts/make_trained_group_report.py      # -> reports/val/figures/*.png

Ranking figures use fresh validation predictions. Learning curves and measured
training/inference times come from the original training runs.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import scripts.make_combined_figures as mcf  # noqa: E402
from scripts.make_report import (FIGURE_METRICS, MUTED, STYLE, setup, slug, table_dataset, table_density,
                                 table_metrics, table_tests, table_training)  # noqa: E402
from scripts.report_inference import report_device, rescore, score_rows, validation_sample  # noqa: E402
from scripts.summarize_results import collect  # noqa: E402
from scripts.validation_io import load_validation_inputs  # noqa: E402

TRAINED = ("dfhf", "lightgcn", "xsimgcl", "directau")
METRICS = FIGURE_METRICS  # the report shows NDCG and Recall at 10 and 20
CURVE_METRICS = ("NDCG@20", "NDCG@10")  # the metrics recorded in the training history


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--results", type=Path, default=ROOT / "results/val")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/val/figures")
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    args = parser.parse_args(argv)
    generate(args.results, args.output, args.device)


def generate(results, output, device, *, tables=None, bootstrap=10_000):
    output.mkdir(parents=True, exist_ok=True)
    setup()
    summary = collect(results)
    summary = summary[summary.model.isin(TRAINED)].copy()
    if summary.empty:
        raise ValueError(f"No trained model results under {results}")
    device = report_device(device)
    _, full_train, validation, stats = load_validation_inputs(None, ROOT)
    targets = dict(zip(validation.u_idx.to_numpy().tolist(), validation.i_idx.to_numpy().tolist()))
    scores = {}
    for density, runs in summary.groupby("density", sort=False):
        train, warm = validation_sample(full_train, validation, density)
        for run in runs.itertuples():
            print(f"Validation inference: {run.model}, density={density:.0%}, seed={run.seed}", flush=True)
            users, predictions, metrics = rescore(run.model, Path(run.path), train, full_train, warm, stats, device)
            for name, value in metrics.items():
                if name in summary.columns:
                    summary.at[run.Index, name] = value
            scores[(run.model, density, run.seed)] = score_rows(users, predictions, targets)
    means = summary.groupby(["model", "density"])
    kwargs = {"order": TRAINED, "style": STYLE, "ncol": 4}
    notes = []

    def column(name):
        values = means[name].mean()
        return lambda model, density: values.get((model, density))

    for metric in METRICS:
        values = means[metric].mean()
        mcf.bar_figure(lambda m, d, v=values: v.get((m, d)), metric, f"H1_trained_density_{slug(metric)}",
                       output, notes, **kwargs)
        if 1.0 in values.index.get_level_values("density"):
            reference = values.xs(1.0, level="density")
            relative = (100 * values.div(reference.where(reference != 0), level="model")).dropna()
            mcf.bar_figure(lambda m, d, v=relative: v.get((m, d)), f"{metric} so với mật độ 1.00 (%)",
                           f"H4_trained_retention_{slug(metric)}", output, notes, fmt="{:.1f}",
                           extra=lambda ax: ax.axhline(100, color=MUTED, linestyle="--", linewidth=.8, zorder=0), **kwargs)
        mcf.figure_groups(scores, full_train, metric, output, notes, name="H5_trained_user_groups", **kwargs)

    for metric in CURVE_METRICS:
        mcf.figure_curves(summary, metric, output, notes, name="H3_trained_learning_curves")
    mcf.figure_loss(summary, output, notes)
    mcf.figure_ndcg_at_k(scores, output, notes, name="H8_trained_ndcg_at_k", **kwargs)

    mcf.bar_figure(column("train_seconds"), "Thời gian huấn luyện 200 epoch (giây, thang log)\nTesla T4",
                   "H7a_trained_train_time", output, notes, fmt="{:,.0f}", log=True, **kwargs)
    mcf.bar_figure(column("inference_ms_per_user"), "Thời gian suy luận (ms/user, thang log)\nTesla T4, theo batch",
                   "H7b_trained_inference_latency", output, notes, fmt="{:.4f}", log=True, **kwargs)
    if tables is not None:
        tables.mkdir(parents=True, exist_ok=True)
        table_dataset(full_train, validation, stats, tables)
        for density in sorted(summary.density.unique(), reverse=True):
            table_metrics(summary, tables, density)
            table_training(summary, tables, density)
        table_density(summary, tables)
        table_tests(scores, tables, "NDCG@20", "B3_significance_ndcg20", repeats=bootstrap)
        table_tests(scores, tables, "NDCG@10", "B3b_significance_ndcg10", repeats=bootstrap)
    print("\n".join(notes))


if __name__ == "__main__":
    main()
