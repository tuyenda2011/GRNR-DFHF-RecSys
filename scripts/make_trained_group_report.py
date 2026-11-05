"""Figures for the trained group only (DFHF, LightGCN, XSimGCL, DirectAU), without GRNR.

  python scripts/make_trained_group_report.py      # -> report/image/*.png

The report compares each proposed model only within its own group; the main report's H1/H3/H4/H5/H7 figures
also show GRNR, so this script redraws them for the trained group with the same drawing code. It writes outside
reports/ (which make_report.py clears) and reads validation data only.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import scripts.make_combined_figures as mcf  # noqa: E402
from scripts.make_report import FIGURE_METRICS, MUTED, STYLE, per_user, setup, slug  # noqa: E402
from scripts.summarize_results import collect  # noqa: E402
from scripts.validation_io import load_validation_inputs  # noqa: E402

TRAINED = ("dfhf", "lightgcn", "xsimgcl", "directau")
METRICS = ("NDCG@20",)  # only the figures the report uses


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--results", type=Path, default=ROOT / "results")
    parser.add_argument("--output", type=Path, default=ROOT / "report" / "image")
    args = parser.parse_args(argv)
    args.output.mkdir(parents=True, exist_ok=True)
    setup()
    summary = collect(args.results)
    summary = summary[summary.model.isin(TRAINED)].copy()
    _, full_train, validation, _ = load_validation_inputs(None, ROOT)
    targets = dict(zip(validation.u_idx.to_numpy().tolist(), validation.i_idx.to_numpy().tolist()))
    scores = per_user(summary, targets)
    means = summary.groupby(["model", "density"])
    kwargs = {"order": TRAINED, "style": STYLE, "ncol": 4}
    notes = []

    def column(name):
        values = means[name].mean()
        return lambda model, density: values.get((model, density))

    for metric in METRICS:
        values = means[metric].mean()
        # The density figure is drawn as a line chart with MostPop by make_mostpop_reference_figures.py.
        mcf.bar_figure(lambda m, d, v=values: 100 * v[(m, d)] / v[(m, 1.0)], f"{metric} so với mật độ 1.00 (%)",
                       f"H4_trained_retention_{slug(metric)}", args.output, notes, fmt="{:.1f}",
                       extra=lambda ax: ax.axhline(100, color=MUTED, linestyle="--", linewidth=.8, zorder=0), **kwargs)
        mcf.figure_groups(scores, full_train, metric, args.output, notes, name="H5_trained_user_groups", **kwargs)

    # figure_curves iterates the module-level ORDER; restrict it to the trained group for this call only.
    saved = mcf.ORDER
    mcf.ORDER = TRAINED
    try:
        for metric in METRICS:
            mcf.figure_curves(summary, metric, args.output, notes)
    finally:
        mcf.ORDER = saved
    for old in args.output.glob("H3_learning_curves_*.png"):
        old.replace(args.output / old.name.replace("H3_learning_curves_", "H3_trained_learning_curves_"))

    mcf.bar_figure(column("train_seconds"), "Thời gian huấn luyện 200 epoch (giây, thang log)\nTesla T4",
                   "H7a_trained_train_time", args.output, notes, fmt="{:,.0f}", log=True, **kwargs)
    mcf.bar_figure(column("inference_ms_per_user"), "Thời gian suy luận (ms/user, thang log)\nTesla T4, theo batch",
                   "H7b_trained_inference_latency", args.output, notes, fmt="{:.4f}", log=True, **kwargs)
    print("\n".join(notes))


if __name__ == "__main__":
    main()
