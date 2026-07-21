"""Charts for 'The Benefit That Costs Less Than It Delivers' (WIC food rebates).
Reads results.json. Output: charts/*.png on a light surface (series dataviz palette)."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())

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
    "text.parse_math": False,   # render literal $ (dollar signs), not mathtext
})


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_wedge():
    f = R["fy2016"]
    net, reb, gross = f["net"] / 1e9, f["rebates"] / 1e9, f["gross"] / 1e9
    fig, ax = plt.subplots(figsize=(9.0, 3.6))
    ax.barh(0, net, color=BLUE, height=0.5, edgecolor=SURFACE, linewidth=1.5)
    ax.barh(0, reb, left=net, color=AQUA, height=0.5, edgecolor=SURFACE, linewidth=1.5)
    ax.text(net / 2, 0, f"Taxpayers pay\n${net:.2f}B", ha="center", va="center",
            color="#ffffff", fontsize=11, fontweight="bold")
    ax.text(net + reb / 2, 0, f"Formula rebates\n${reb:.2f}B", ha="center", va="center",
            color=INK, fontsize=10.5, fontweight="bold")
    ax.annotate(f"${gross:.2f}B of food delivered to families", (gross, 0.32), ha="right", va="bottom",
                fontsize=10.5, color=INK, fontweight="bold")
    ax.set_xlim(0, gross * 1.02)
    ax.set_ylim(-0.5, 0.75)
    ax.set_yticks([])
    ax.set_title("WIC delivers $5.7B of food for a net public cost of $3.9B")
    ax.grid(False)
    for sp in ["left", "right", "top"]:
        ax.spines[sp].set_visible(False)
    fig.text(0.12, -0.12, "USDA WIC data, fiscal year 2016 (billions of dollars). The food families "
             "receive is worth more than taxpayers pay, because infant-formula\nmakers cover the "
             "difference through rebates (about 30% of the food's value in 2016).",
             fontsize=8.5, color=MUTED)
    save(fig, "01_rebate_wedge.png")


def chart2_share():
    by = R["by_year"]
    yrs = [str(r["fy"]) for r in by]
    share = [r["rebate_share_of_gross"] * 100 for r in by]
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    x = np.arange(len(yrs))
    ax.bar(x, share, color=AQUA, width=0.62)
    ax.set_xticks(x, yrs, fontsize=11)
    for xi, s in zip(x, share):
        ax.annotate(f"{s:.0f}%", (xi, s), xytext=(0, 3), textcoords="offset points",
                    ha="center", fontsize=11, fontweight="bold", color=INK2)
    ax.set_ylim(0, 45)
    ax.set_ylabel("rebates as a share of gross WIC food cost")
    ax.set_xlabel("fiscal year")
    ax.set_title("Every year, formula rebates cover about 30% of the food")
    ax.grid(axis="x", visible=False)
    fig.text(0.12, -0.04, "USDA WIC data (gross food cost = net food cost + rebates). The claw-back is "
             "durable, not a one-off. A US government audit found\nit ranged from 39% (2020) to 27% "
             "(2023) nationally as rebate levels shifted (GAO, 2025).", fontsize=8.5, color=MUTED)
    save(fig, "02_rebate_share.png")


def chart3_per_person():
    f = R["fy2016"]
    g, n = f["per_person_gross_month"], f["per_person_net_month"]
    fig, ax = plt.subplots(figsize=(8.0, 5.4))
    bars = ["Food value\nfamilies receive", "What taxpayers\npay"]
    vals = [g, n]
    ax.bar([0, 1], vals, color=[AQUA, BLUE], width=0.58)
    ax.set_xticks([0, 1], bars, fontsize=11)
    for xi, v in zip([0, 1], vals):
        ax.annotate(f"${v:.0f}", (xi, v), xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=14, fontweight="bold", color=INK)
    ax.annotate("", xy=(0, g), xytext=(0, n), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6))
    ax.text(0.06, (g + n) / 2, f"${round(g)-round(n):.0f} covered\nby rebates", color=RED, fontsize=9.5,
            fontweight="bold", va="center")
    ax.set_ylim(0, g * 1.2)
    ax.set_ylabel("per participant, per month (FY2016 dollars)")
    ax.set_title("Per person: about $61 of food a month, for $43 of public money")
    ax.grid(axis="x", visible=False)
    fig.text(0.12, -0.04, "USDA WIC data, FY2016. Each participant received roughly $61 a month of food; "
             "the net cost to taxpayers was $42.77 (USDA), the\ndifference paid by formula rebates.",
             fontsize=8.5, color=MUTED)
    save(fig, "03_per_person.png")


def chart4_formula():
    b = R["breastfeeding"]
    cats = ["Fully\nbreastfed", "Partially\nbreastfed", "Formula\nonly"]
    vals = [b["fully_bf_pct"], b["partial_bf_pct"], b["formula_only_pct"]]
    cols = [AQUA, YELLOW, BLUE]
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    x = np.arange(3)
    ax.bar(x, vals, color=cols, width=0.6)
    ax.set_xticks(x, cats, fontsize=10.5)
    for xi, v in zip(x, vals):
        ax.annotate(f"{v:.1f}%", (xi, v), xytext=(0, 3), textcoords="offset points",
                    ha="center", fontsize=12, fontweight="bold", color=INK2)
    ax.set_ylim(0, 80)
    ax.set_ylabel("share of WIC infants (FY2016)")
    ax.set_title("The engine is formula: about 68% of WIC infants are formula-fed")
    ax.grid(axis="x", visible=False)
    fig.text(0.12, -0.05, "USDA FNS FY2016 Breastfeeding Report. WIC buys over half of all US infant "
             "formula, and that scale is exactly what lets states\nwin rebates worth up to 90% of the "
             "wholesale price (GAO, 2025).", fontsize=8.5, color=MUTED)
    save(fig, "04_formula_engine.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_wedge()
    chart2_share()
    chart3_per_person()
    chart4_formula()
