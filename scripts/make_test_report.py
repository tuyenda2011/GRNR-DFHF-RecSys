"""Test-split counterparts of the validation figures and tables, drawn from the saved test predictions.

  python scripts/make_test_report.py        # reads results/test, writes reports/test/{figures,tables}

Inputs come from scripts/evaluate_test.py (results/test/<model>/d<pct>/seed42/: metrics.json,
test_predictions.npy, test_users.npy); nothing is re-scored here. Same drawing code, names and layout as
reports/val, so each test file sits beside its validation file:
  tables/B5_closed_form.csv, tables/B6_closed_form_significance.csv
  tables/B3_trained_significance.csv   DFHF minus each trained baseline, NDCG@20, Holm over 3 per density
  tables/B7_mostpop_significance.csv   DFHF and GRNR minus MostPop, NDCG@20, Holm over 2 per density
    (both: paired user bootstrap, same procedure as B6)
  figures/H1_*_density_<metric>, H4_*_retention_<metric>, H5_*_user_groups_<metric>, H8_*_ndcg_at_k
    for the closed-form group (GRNR, EASE, EASE top-128, GF-CF) and the trained group (DFHF and baselines).
  figures/H3_trained_learning_curves_<metric>, H3c_loss, H7a_*_train_time, H7b_trained_inference_latency,
    H7c_closed_form_checkpoint_size: drawn from the training runs, so they match reports/val (learning curves
    are per-epoch validation traces; train time, latency and checkpoint size do not depend on the split).
    They are included so reports/test holds the full figure set.
  figures/H9_mostpop_{closed,trained}_ndcg20: as report/image/H9_*, with test NDCG@20 and test MostPop.
--report-image copies every figure to report/image/ (the validation figures live in report/image/val/).
B5 repeats train time and checkpoint size from the validation runs so its columns match reports/val.
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

import scripts.make_closed_form_report as cf
import scripts.make_combined_figures as mcf
from scripts.evaluate_test import load_inputs
from scripts.make_report import FIGURE_METRICS, MUTED, STYLE, setup, slug
from scripts.make_trained_group_report import CURVE_METRICS, TRAINED
from scripts.report_inference import score_rows
from scripts.summarize_results import collect

SEED = 42
DENSITIES = (0.25, 0.5, 0.75, 1.0)


def test_run(results, model, density):
    return results / model / f"d{round(density * 100)}" / f"seed{SEED}"


def load_scores(results, models, targets):
    """Per-user test scores and stored test metrics for every (model, density); fails on a missing run."""
    scores, metrics = {}, {}
    for model in models:
        for density in DENSITIES:
            run = test_run(results, model, density)
            if not (run / "metrics.json").is_file():
                raise FileNotFoundError(f"Missing test run {run}; run scripts/evaluate_test.py --models {model}")
            users = np.load(run / "test_users.npy").astype(np.int64, copy=False)
            predictions = np.load(run / "test_predictions.npy").astype(np.int64, copy=False)
            scores[(model, density, SEED)] = score_rows(users, predictions, targets)
            metrics[(model, density)] = json.loads((run / "metrics.json").read_text(encoding="utf-8"))["test_metrics"]
    return scores, metrics


def bar_figures(metrics, scores, full_train, folder, notes, group, order, style):
    kwargs = {"order": order, "style": style, "ncol": 4}
    for metric in FIGURE_METRICS:
        mcf.bar_figure(lambda m, d, metric=metric: metrics[(m, d)][metric], metric,
                       f"H1_{group}_density_{slug(metric)}", folder, notes, **kwargs)
        mcf.bar_figure(lambda m, d, metric=metric: 100 * metrics[(m, d)][metric] / metrics[(m, 1.0)][metric],
                       f"{metric} so với $d$ = 1 (%)", f"H4_{group}_retention_{slug(metric)}", folder, notes,
                       fmt="{:.1f}", extra=lambda ax: ax.axhline(100, color=MUTED, linestyle="--", linewidth=.8,
                                                                 zorder=0), **kwargs)
        mcf.figure_groups(scores, full_train, metric, folder, notes, name=f"H5_{group}_user_groups", **kwargs)
    mcf.figure_ndcg_at_k(scores, folder, notes, name=f"H8_{group}_ndcg_at_k", **kwargs)


def closed_form_tables(metrics, scores, val_results, tables, num_items, bootstrap):
    rows = []
    for density in DENSITIES:
        for model in cf.ARMS:
            source = cf.run_dir(model, density, val_results)
            run = json.loads((source / "metrics.json").read_text(encoding="utf-8"))
            rows.append({"Mô hình": cf.STYLE[model]["label"], "Mật độ": density,
                         **{m: metrics[(model, density)][m] for m in cf.METRICS},
                         "Checkpoint (MB)": cf.checkpoint_mb(model, density, val_results, num_items),
                         "Train (phút)": round(run["train_seconds"] / 60, 1)})
    pd.DataFrame(rows).round({**{m: 5 for m in cf.METRICS}, "Checkpoint (MB)": 1}).to_csv(
        tables / "B5_closed_form.csv", index=False, encoding="utf-8-sig", lineterminator="\n")
    tests = cf.table_tests(scores, repeats=bootstrap)
    pd.DataFrame({"So sánh": "GRNR - " + tests.model.map(lambda m: cf.STYLE[m]["label"]), "Mật độ": tests["Mật độ"],
                  "Delta NDCG@20": tests.delta.round(5), "KTC 95% dưới": [round(c[0], 5) for c in tests.ci95],
                  "KTC 95% trên": [round(c[1], 5) for c in tests.ci95], "p một phía": tests.p_one_sided.round(5),
                  "p Holm": tests.p_holm.round(5), "Số user": tests.n_users}
                 ).to_csv(tables / "B6_closed_form_significance.csv", index=False, encoding="utf-8-sig",
                          lineterminator="\n")


def training_figures(val_results, folder, notes, num_items):
    """H3, H3c and H7a/b/c: the same drawing and the same data as reports/val (they come from training)."""
    kwargs = {"ncol": 4}
    summary = collect(val_results)
    summary = summary[summary.model.isin(TRAINED)].copy()
    means = summary.groupby(["model", "density"])

    def column(name):
        values = means[name].mean()
        return lambda model, density: values.get((model, density))
    for metric in CURVE_METRICS:
        mcf.figure_curves(summary, metric, folder, notes, name="H3_trained_learning_curves")
    mcf.figure_loss(summary, folder, notes)
    trained = {"order": TRAINED, "style": STYLE, **kwargs}
    mcf.bar_figure(column("train_seconds"), "Thời gian huấn luyện 200 epoch (giây, thang log)\nTesla T4",
                   "H7a_trained_train_time", folder, notes, fmt="{:,.0f}", log=True, **trained)
    mcf.bar_figure(column("inference_ms_per_user"), "Thời gian suy luận (ms/người dùng, thang log)\nTesla T4, theo batch",
                   "H7b_trained_inference_latency", folder, notes, fmt="{:.4f}", log=True, **trained)

    def closed(model, density):
        return json.loads((cf.run_dir(model, density, val_results) / "metrics.json").read_text(encoding="utf-8"))
    closed_form = {"order": cf.ARMS, "style": cf.STYLE, **kwargs}
    mcf.bar_figure(lambda m, d: closed(m, d)["train_seconds"], "Thời gian huấn luyện (giây, thang log)\nTất cả chạy "
                   "trên CPU; EASE top-128 = EASE + cắt", "H7a_closed_form_train_time", folder, notes, fmt="{:,.0f}",
                   log=True, **closed_form)
    mcf.bar_figure(lambda m, d: cf.checkpoint_mb(m, d, val_results, num_items), "Dung lượng checkpoint (MiB, thang "
                   "log)\nEASE đầy đủ: ma trận float32, không lưu", "H7c_closed_form_checkpoint_size", folder, notes,
                   fmt="{:,.1f}", log=True, **closed_form)


def mostpop_figures(results, folder):
    """H9: NDCG@20 by density per group with the MostPop reference (test counterpart of the report's H9)."""
    from scripts.make_mostpop_reference_figures import DENSITIES as H9_DENSITIES, draw

    def series(model):
        return [json.loads((test_run(results, model, d) / "metrics.json").read_text(encoding="utf-8"))
                ["test_metrics"]["NDCG@20"] for d in H9_DENSITIES]
    mostpop = series("mostpop")
    draw({m: series(m) for m in cf.ARMS}, cf.STYLE, mostpop, "H9_mostpop_closed_ndcg20", folder)
    draw({m: series(m) for m in TRAINED}, STYLE, mostpop, "H9_mostpop_trained_ndcg20", folder)


def significance_table(scores, pairs, path, repeats, metric="NDCG@20"):
    """Paired user bootstrap of proposed minus rival, Holm over the comparisons of each density (as B6)."""
    from scripts.compare_val_runs import holm_adjust, paired_bootstrap
    rows = []
    for density in DENSITIES:
        block = []
        for proposed, rival in pairs:
            users, _, values, _ = scores[(proposed, density, SEED)]
            reference = pd.Series(values[metric], index=users)
            users, _, values, _ = scores[(rival, density, SEED)]
            other = pd.Series(values[metric], index=users)
            common = reference.index.intersection(other.index)
            test = paired_bootstrap(other.loc[common].to_numpy(float), reference.loc[common].to_numpy(float),
                                    repeats=repeats)
            block.append({"proposed": proposed, "rival": rival, **test})
        for row, p in zip(block, holm_adjust([row["p_one_sided"] for row in block])):
            rows.append({"So sánh": f"{LABELS[row['proposed']]} - {LABELS[row['rival']]}", "Mật độ": density,
                         f"Delta {metric}": round(row["delta"], 6), "KTC 95% dưới": round(row["ci95"][0], 5),
                         "KTC 95% trên": round(row["ci95"][1], 5), "p một phía": round(row["p_one_sided"], 5),
                         "p Holm": round(p, 5), "Số user": row["n_users"]})
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig", lineterminator="\n")


LABELS = {**{m: STYLE[m]["label"] for m in TRAINED}, **{m: cf.STYLE[m]["label"] for m in cf.ARMS},
          "mostpop": "MostPop"}


def generate(results, val_results, reports, *, bootstrap=10_000):
    _, full_train, _, test, stats = load_inputs(None)
    targets = dict(zip(test.u_idx.astype(int), test.i_idx.astype(int)))
    figures, tables = reports / "figures", reports / "tables"
    figures.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)
    setup()
    notes = []
    scores, metrics = load_scores(results, cf.ARMS, targets)
    bar_figures(metrics, scores, full_train, figures, notes, "closed_form", cf.ARMS, cf.STYLE)
    closed_form_tables(metrics, scores, val_results, tables, stats["num_items"], bootstrap)
    grnr_scores = {key: value for key, value in scores.items() if key[0] == "grnr"}
    scores, metrics = load_scores(results, TRAINED, targets)
    bar_figures(metrics, scores, full_train, figures, notes, "trained", TRAINED, STYLE)
    significance_table(scores, [("dfhf", rival) for rival in TRAINED[1:]],
                       tables / "B3_trained_significance.csv", bootstrap)
    mostpop_scores, _ = load_scores(results, ("mostpop",), targets)
    significance_table({**scores, **grnr_scores, **mostpop_scores}, [("dfhf", "mostpop"), ("grnr", "mostpop")],
                       tables / "B7_mostpop_significance.csv", bootstrap)
    training_figures(val_results, figures, notes, stats["num_items"])
    mostpop_figures(results, figures)
    print("\n".join(notes))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--results", type=Path, default=ROOT / "results/test")
    parser.add_argument("--val-results", type=Path, default=ROOT / "results/val",
                        help="validation runs, for B5's train time and checkpoint size")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/test")
    parser.add_argument("--bootstrap", type=int, default=10_000)
    parser.add_argument("--report-image", type=Path, nargs="?", const=ROOT / "report/image", default=None,
                        help="also copy the figures here for the LaTeX report (default report/image)")
    args = parser.parse_args(argv)
    generate(args.results, args.val_results, args.output, bootstrap=args.bootstrap)
    if args.report_image:
        import shutil
        args.report_image.mkdir(parents=True, exist_ok=True)
        for figure in sorted((args.output / "figures").glob("*.png")):
            shutil.copy2(figure, args.report_image / figure.name)
        print(f"copied figures -> {args.report_image}")


if __name__ == "__main__":
    main()
