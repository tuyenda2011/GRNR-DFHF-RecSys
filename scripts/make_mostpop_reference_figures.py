"""NDCG@20 versus training density for each comparison group, with the MostPop reference as a dashed line.

  python scripts/make_mostpop_reference_figures.py   # -> report/image/H9_mostpop_{closed,trained}_ndcg20.png

Inputs (validation only): reports/tables/B5_closed_form.csv, reports/tables/B2b_by_density.csv and
report/planning/phan_tich_bo_sung/t6g_mostpop.json (MostPop ranks retained-train candidates by retained count).
Each figure holds one group only; GRNR and DFHF never share a figure.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import pandas as pd  # noqa: E402

from scripts.make_closed_form_report import STYLE as CLOSED_STYLE  # noqa: E402
from scripts.make_report import MUTED, STYLE, setup, style_axes  # noqa: E402

DENSITIES = (0.25, 0.5, 0.75, 1.0)
OUT = ROOT / "report" / "image"


def draw(series, styles, mostpop, name):
    fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
    style_axes(ax)
    for key, values in series.items():
        spec = styles[key]
        ax.plot(DENSITIES, values, color=spec["color"], marker=spec["marker"], linestyle=spec["line"],
                linewidth=1.6, markersize=5, label=spec["label"])
    ax.plot(DENSITIES, mostpop, color=MUTED, linestyle=(0, (4, 3)), linewidth=1.6, marker="x", markersize=5,
            label="MostPop (tham chiếu)")
    ax.set_xticks(DENSITIES, [f"{d:.2f}".replace(".", ",") for d in DENSITIES])
    ax.set_xlabel("Tỉ lệ tương tác huấn luyện được giữ lại $d$")
    ax.set_ylabel("NDCG@20")
    ax.set_ylim(0, None)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.3f}".replace(".", ",")))
    fig.legend(loc="outside lower center", ncol=3, frameon=False)
    fig.savefig(OUT / f"{name}.png", dpi=300, facecolor="white")
    plt.close(fig)
    print(f"{name}: written")


def main():
    setup()
    OUT.mkdir(parents=True, exist_ok=True)
    pop = json.loads((ROOT / "report/planning/phan_tich_bo_sung/t6g_mostpop.json").read_text(encoding="utf-8"))
    mostpop = [pop[str(d)]["NDCG@20"] for d in DENSITIES]

    b5 = pd.read_csv(ROOT / "reports/tables/B5_closed_form.csv", encoding="utf-8-sig")
    labels = {"grnr": "GRNR (đề xuất)", "ease": "EASE (đầy đủ)", "ease128": "EASE top-128", "gfcf": "GF-CF"}
    closed = {key: [float(b5[(b5["Mô hình"] == label) & (b5["Mật độ"] == d)]["NDCG@20"].iloc[0]) for d in DENSITIES]
              for key, label in labels.items()}
    draw(closed, CLOSED_STYLE, mostpop, "H9_mostpop_closed_ndcg20")

    b2 = pd.read_csv(ROOT / "reports/tables/B2b_by_density.csv", encoding="utf-8-sig").set_index("Mô hình")
    trained = {key: [float(b2.at[STYLE[key]["label"], f"NDCG@20 d={d:.2f}"]) for d in DENSITIES]
               for key in ("dfhf", "lightgcn", "xsimgcl", "directau")}
    draw(trained, STYLE, mostpop, "H9_mostpop_trained_ndcg20")


if __name__ == "__main__":
    main()
