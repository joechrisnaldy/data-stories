"""Charts for 'The Most Generous Country on Earth Isn't the Happiest'. Reads results.json.
Output: charts/*.png on a light surface (series dataviz palette)."""
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
})

FEEL_REGIONS = {"Latin America and Caribbean", "Southeast Asia"}
RATE_REGIONS = {"Central and Eastern Europe", "Commonwealth of Independent States"}


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_two_happinesses():
    pts = R["scatter"]
    fig, ax = plt.subplots(figsize=(8.8, 6.8))
    for p in pts:
        if p["country"] == "Indonesia":
            continue
        reg = p["region"]
        col = AQUA if reg in FEEL_REGIONS else (BLUE if reg in RATE_REGIONS else "#c9c8c0")
        ax.scatter(p["ladder"], p["posaff"], s=34, color=col, alpha=0.8,
                   edgecolor="white", linewidth=0.4, zorder=3)
    ind = next(p for p in pts if p["country"] == "Indonesia")
    ax.scatter(ind["ladder"], ind["posaff"], s=180, color=RED, edgecolor="white",
               linewidth=1.0, zorder=5, marker="*")
    ax.annotate("Indonesia", (ind["ladder"], ind["posaff"]), xytext=(9, 5),
                textcoords="offset points", fontsize=10.5, color=RED, fontweight="bold")
    ax.set_xlabel("how they RATE their life  (ladder score, 0-10)  ->")
    ax.set_ylabel("how they FEEL day to day  (positive affect)  ->")
    ax.set_title("Two kinds of happiness, and they only loosely agree")
    ax.annotate("Latin America and SE Asia (green):\nlots of daily joy, any ladder score",
                (0.02, 0.14), xycoords="axes fraction", fontsize=9, color="#0e7a54",
                fontweight="bold")
    ax.annotate("Eastern Europe (blue):\nrates high, feels low", (0.66, 0.10),
                xycoords="axes fraction", fontsize=9, color="#1c5fb0", fontweight="bold")
    fig.text(0.12, -0.02, "Each dot is a country (latest survey year). The ladder tracks daily "
             "feeling only loosely (r = %.2f). Indonesia (star) feels a lot and rates itself\n"
             "middling." % R["corr"]["posaff_ladder"], fontsize=8.5, color=MUTED)
    save(fig, "01_two_happinesses.png")


def chart2_generosity():
    g = R["generosity_top"][::-1]                 # barh bottom-up, so #1 ends on top
    names = [x["country"] for x in g]
    vals = [x["generosity"] for x in g]
    colors = [RED if n == "Indonesia" else BLUE for n in names]
    fig, ax = plt.subplots(figsize=(8.6, 5.8))
    y = np.arange(len(names))
    ax.barh(y, vals, color=colors, height=0.72)
    ax.set_yticks(y, names, fontsize=10)
    for yi, v in zip(y, vals):
        ax.annotate(f"{v:.2f}", (v, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=INK2)
    ax.set_xlim(0, max(vals) * 1.12)
    ax.set_xlabel("generosity (giving, after accounting for income)")
    ax.set_title("Indonesia gives more than any country on earth")
    ax.grid(axis="y", visible=False)
    fig.text(0.12, -0.03, "World Happiness Report generosity measure, latest year. And it buys "
             "nothing on the ranking: generosity's correlation with the happiness ladder is "
             "%.2f,\nso these givers sit all across it." % R["corr"]["generosity_ladder"],
             fontsize=8.5, color=MUTED)
    save(fig, "02_generosity.png")


def chart3_feeling_vs_judging():
    cur = R["curated"]
    n = len(cur)
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    y = np.arange(n)[::-1]
    for yi, c in zip(y, cur):
        ax.plot([c["posaff_rank"], c["ladder_rank"]], [yi, yi], color=BASELINE, lw=2.4, zorder=1)
        ax.scatter(c["posaff_rank"], yi, s=95, color=AQUA, zorder=3, edgecolor="white")
        ax.scatter(c["ladder_rank"], yi, s=95, color=BLUE, zorder=3, edgecolor="white")
    ax.set_yticks(y, [c["country"] for c in cur], fontsize=11)
    ax.set_xlabel("world rank (1 = best)  <-- better")
    ax.set_title("Where a country ranks on feeling vs on judging its life")
    ax.scatter([], [], color=AQUA, label="rank on daily feeling (positive affect)")
    ax.scatter([], [], color=BLUE, label="rank on rating life (the ladder)")
    ax.legend(loc="center right", frameon=True, facecolor=SURFACE, edgecolor=BASELINE,
              framealpha=0.95, fontsize=9)
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, max(max(c["ladder_rank"], c["posaff_rank"]) for c in cur) + 12)
    fig.text(0.12, -0.05, "Indonesia is near the top of the world for daily feeling but "
             "middling on the ladder; Poland is the opposite. Latest survey year, ~%d countries."
             % R["n_panel"], fontsize=8.5, color=MUTED)
    save(fig, "03_feeling_judging.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_two_happinesses()
    chart2_generosity()
    chart3_feeling_vs_judging()
