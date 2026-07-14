"""Charts for 'The Score You Didn't Build'. Reads results.json.
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


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_recipe():
    rows = R["recipe"]["weights_all"]          # 33 nutrients, sorted by weight desc
    rows = rows[::-1]                           # barh bottom-up
    names = [r["nutrient"] for r in rows]
    wts = [r["weight"] for r in rows]
    ingredients = set(R["recipe"]["ingredients"])
    colors = [AQUA if n in ingredients else "#d7d6cf" for n in names]
    fig, ax = plt.subplots(figsize=(8.6, 9.2))
    y = np.arange(len(names))
    ax.barh(y, wts, color=colors, height=0.78)
    ax.set_yticks(y, names, fontsize=8.5)
    ax.set_xlabel("weight recovered by regressing the score on every nutrient")
    ax.set_title("We fed the 'Nutrition Density' score to a regression.\nIt handed back the recipe.")
    ax.grid(axis="y", visible=False)
    ax.axvline(1.0, color=BASELINE, lw=0.8, ls=(0, (4, 3)))
    fig.text(0.12, 0.02, "Eight nutrients (green) each enter with weight 1; the other 25 (grey) "
             "are ignored. R-squared = 1.00: the score is exactly their sum.",
             fontsize=8.5, color=MUTED)
    save(fig, "01_recipe.png")


def chart2_madeof():
    c = R["contribution"]                       # sorted by share desc
    names = [f"{r['term']} ({r['unit']})" for r in c][::-1]
    shares = [r["share_pct"] for r in c][::-1]
    top = c[0]["term"]
    colors = [RED if r["term"] == top else (BLUE if r["unit"] == "g" else "#9bbcea")
              for r in c][::-1]
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    y = np.arange(len(names))
    ax.barh(y, shares, color=colors, height=0.72)
    ax.set_yticks(y, names, fontsize=10)
    for yi, s in zip(y, shares):
        ax.annotate(f"{s:.0f}%", (s, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=9, color=INK2)
    ax.set_xlim(0, max(shares) * 1.15)
    ax.set_xlabel("share of the total 'Nutrition Density' score")
    ax.set_title("Half the 'nutrition' score is calcium,\nonly because calcium is counted in milligrams")
    ax.grid(axis="y", visible=False)
    fig.text(0.12, -0.03, "The score adds grams (macros), milligrams (calcium, vitamin C, iron) "
             "and micrograms (vitamin A) as if equal. Big-number units win; the vitamins it is\n"
             "named for barely count. The score correlates %.2f with plain calories."
             % R["density_calorie_corr"], fontsize=8.5, color=MUTED)
    save(fig, "02_madeof.png")


def chart3_calories():
    s = R["atwater_scatter"]
    xp = np.array([p["pred"] for p in s])
    ya = np.array([p["actual"] for p in s])
    fig, ax = plt.subplots(figsize=(7.8, 7.4))
    ax.scatter(xp, ya, s=10, color=BLUE, alpha=0.25, edgecolor="none", zorder=3)
    lim = 900
    ax.plot([0, lim], [0, lim], color=INK2, lw=1.4, ls=(0, (4, 3)), zorder=4)
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_xlabel("calories predicted from macros  (4*carb + 4*protein + 9*fat)")
    ax.set_ylabel("calories listed in the dataset")
    ax.set_title("Calories are also a formula, but an honest one")
    at = R["atwater"]
    ax.annotate(f"median miss = {at['median_abs_err_clean']:.1f} kcal\n"
                f"{at['within20_clean_pct']:.0f}% within 20 kcal",
                (0.05, 0.90), xycoords="axes fraction", fontsize=11, color=INK, fontweight="bold")
    fig.text(0.12, 0.01, "Each dot is one of %d physically plausible foods. The dashed line is a "
             "perfect match. Atwater's 1900s 4/4/9 factors reproduce the calorie column to\n"
             "within a couple of kcal. The honest misses are alcohol (7 kcal/g, not a macro "
             "column here); a few impossible rows are excluded." % at["n_clean"],
             fontsize=8.5, color=MUTED)
    save(fig, "03_calories.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_recipe()
    chart2_madeof()
    chart3_calories()
