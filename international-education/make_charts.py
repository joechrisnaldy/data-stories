"""Charts for 'The Cheapest Degree Abroad Isn't the Best Deal'. Reads results.json.
Output: charts/*.png on a light surface (series dataviz palette)."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())
rows = R["by_country"]

BLUE, AQUA, YELLOW, RED = "#2a78d6", "#1baf7a", "#eda100", "#e34948"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": BASELINE, "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": INK2,
    "text.color": INK, "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "font.size": 10.5,
    "axes.spines.top": False, "axes.spines.right": False,
})


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_cost():
    d = sorted(rows, key=lambda r: r["total_cost"])
    names = [r["Country"] for r in d]
    vals = [r["total_cost"] / 1000 for r in d]
    fig, ax = plt.subplots(figsize=(8.4, 8.4))
    y = np.arange(len(names))
    colors = [RED if n == "USA" else (AQUA if n == "Greece" else BLUE) for n in names]
    ax.barh(y, vals, color=colors, height=0.74)
    ax.set_yticks(y, names, fontsize=9.5)
    for yi, v in zip(y, vals):
        ax.annotate(f"${v:.0f}k", (v, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=INK2)
    ax.set_xlabel("total cost of a master's degree (USD, thousands)")
    ax.set_title("What a master's degree abroad costs")
    ax.grid(axis="y", visible=False)
    fig.text(0.12, 0.02, "Median across the master's programs in each country: tuition over "
             "the degree, plus rent, visa and insurance. USA is 13 times Greece. Sample of "
             "programs; 27 OECD destinations.", fontsize=8.5, color=MUTED)
    save(fig, "01_cost.png")


def chart2_payback():
    d = sorted(rows, key=lambda r: r["payback_years"])
    names = [r["Country"] for r in d]
    vals = [r["payback_years"] for r in d]
    fig, ax = plt.subplots(figsize=(8.4, 8.4))
    y = np.arange(len(names))
    color = {"Mexico": RED, "Germany": AQUA, "Luxembourg": AQUA, "USA": RED}
    colors = [color.get(n, BLUE) for n in names]
    ax.barh(y, vals, color=colors, height=0.74)
    ax.set_yticks(y, names, fontsize=9.5)
    for yi, v in zip(y, vals):
        ax.annotate(f"{v:.2f}", (v, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=INK2)
    ax.set_xlabel("years of the local average salary to earn the degree back")
    ax.set_title("The bargain ranking is not the price ranking")
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, 2.05)
    # annotate the two headline movers
    mex = names.index("Mexico")
    ax.annotate("cheap tuition, but low wages make it\none of the slowest to earn back",
                (vals[mex], mex), xytext=(44, 0), textcoords="offset points", ha="left",
                va="center", fontsize=8.5, color=RED, fontweight="bold")
    lux = names.index("Luxembourg")
    ax.annotate("mid-priced, but the world's\nhighest wage pays it off fast",
                (vals[lux], lux), xytext=(30, 0), textcoords="offset points", ha="left",
                va="center", fontsize=8.5, color="#0e7a54", fontweight="bold")
    fig.text(0.12, 0.02, "Total cost divided by the local average annual wage (OECD, 2024, "
             "PPP-USD). Assumes you stay and work there; the average wage is not a "
             "new-graduate wage, so real payback is longer.", fontsize=8.5, color=MUTED)
    save(fig, "02_payback.png")


def chart3_employment():
    fig, ax = plt.subplots(figsize=(9.0, 6.6))
    xs = [r["payback_years"] for r in rows]
    ys = [r["employment"] for r in rows]
    ax.scatter(xs, ys, s=46, color=BLUE, alpha=0.75, edgecolor="white", linewidth=0.5, zorder=3)
    # label a curated set: sweet spot, traps, expensive, cheap-but-weak-jobs
    LABEL = {"Germany": (8, -1), "Netherlands": (8, 2), "Iceland": (10, -5),
             "Mexico": (-8, -12), "USA": (-8, 8), "Australia": (8, 2),
             "Greece": (8, -8), "Italy": (8, -3), "Luxembourg": (-8, -10), "Japan": (8, 2),
             "UK": (8, 2), "Switzerland": (8, 3)}
    for r in rows:
        n = r["Country"]
        if n in LABEL:
            dx, dy = LABEL[n]
            col = RED if n == "Mexico" else ("#0e7a54" if n in ("Germany", "Norway", "Netherlands", "Sweden") else INK2)
            ax.annotate(n, (r["payback_years"], r["employment"]), xytext=(dx, dy),
                        textcoords="offset points", fontsize=9, color=col,
                        fontweight="bold" if n in ("Germany", "Mexico") else "normal")
    ax.set_xlabel("payback (years of local salary to earn the degree back)  ->  worse")
    ax.set_ylabel("employment rate, 15-64 (%)  ->  better")
    ax.set_title("The best deals are cheap to earn back and easy to find work in")
    med_x, med_y = np.median(xs), np.median(ys)
    ax.axvline(med_x, color=BASELINE, lw=0.8, ls=(0, (4, 3)))
    ax.axhline(med_y, color=BASELINE, lw=0.8, ls=(0, (4, 3)))
    ax.annotate("better deals", (0.06, 0.90), xycoords="axes fraction", va="top",
                fontsize=9.5, color="#0e7a54", fontweight="bold")
    fig.text(0.12, -0.02, "Payback from OECD average wages (2024); employment rate is the "
             "OECD 15-64 rate (2024-2025), economy-wide, not new-graduate. Mexico is the "
             "double trap: slow payback and a weaker job market.", fontsize=8.5, color=MUTED)
    save(fig, "03_employment.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_cost()
    chart2_payback()
    chart3_employment()
