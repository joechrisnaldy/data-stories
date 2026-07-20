"""Charts for 'Everyone Knows Social Media Is Wrecking Teens. The Evidence Doesn't.'
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
})


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_certainty():
    c = R["certainty"]
    labels = ["For people\ntheir age", "For\nthemselves"]
    vals = [c["peers_2025"], c["self_2025"]]
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    x = np.arange(2)
    ax.bar(x, vals, color=[RED, BLUE], width=0.6)
    ax.set_xticks(x, labels, fontsize=11)
    for xi, v in zip(x, vals):
        ax.annotate(f"{v}%", (xi, v), xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=13, fontweight="bold", color=INK)
    ax.annotate("up from 32% in 2022", (0, c["peers_2025"]), xytext=(0, -22),
                textcoords="offset points", ha="center", fontsize=8.5, color="#ffffff")
    ax.set_ylim(0, 58)
    ax.set_ylabel("share of US teens who say social media\nhas a mostly negative effect (2025)")
    ax.set_title("Teens are sure social media harms other teens, not themselves")
    ax.grid(axis="x", visible=False)
    fig.text(0.12, -0.03, "Pew Research Center, 2025. And the emblem of the alarm hedges: the 2023 US "
             "Surgeon General's advisory says\n\"we do not yet have enough evidence to determine if "
             "social media is sufficiently safe for children and adolescents.\"",
             fontsize=8.5, color=MUTED)
    save(fig, "01_certainty.png")


def chart2_crisis():
    fig, ax = plt.subplots(figsize=(8.8, 5.6))
    styles = {"Female": (RED, "o", 2.4), "Total": (INK2, "s", 1.8), "Male": (BLUE, "^", 2.4)}
    for g in ["Female", "Total", "Male"]:
        s = R["crisis"][g]
        yrs = [p["year"] for p in s]
        pct = [p["pct"] for p in s]
        col, mk, lw = styles[g]
        ax.plot(yrs, pct, color=col, marker=mk, markersize=5, linewidth=lw, label=g, zorder=3)
    ax.annotate("girls, 56.6% in 2021", (2021, 56.6), xytext=(-6, 10), textcoords="offset points",
                fontsize=9, color=RED, ha="right")
    ax.annotate("boys, 27.7% in 2023", (2023, 27.7), xytext=(4, -4), textcoords="offset points",
                fontsize=9, color=BLUE, ha="left")
    ax.set_ylim(15, 62)
    ax.set_xticks([2011, 2013, 2015, 2017, 2019, 2021, 2023])
    ax.set_ylabel("share reporting persistent sadness or hopelessness (%)")
    ax.set_title("The distress is real, and it did not rise evenly")
    ax.grid(axis="x", visible=False)
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    fig.text(0.12, -0.03, "US high school students, CDC Youth Risk Behavior Survey. Felt so sad or "
             "hopeless almost every day for two weeks that they\nstopped usual activities. The rise is "
             "steepest for girls, and it eased slightly from 2021 to 2023.", fontsize=8.5, color=MUTED)
    save(fig, "02_crisis.png")


def chart3_contested():
    bars = R["contested"]["bars"]
    names = [b["behavior"] for b in bars]
    betas = [b["beta"] for b in bars]
    def colr(b):
        if b["is_tech"]:
            return RED
        return AQUA if b["beta"] > 0 else MUTED
    colors = [colr(b) for b in bars]
    fig, ax = plt.subplots(figsize=(8.8, 6.0))
    y = np.arange(len(names))
    ax.barh(y, betas, color=colors, height=0.72)
    ax.set_yticks(y, names, fontsize=10.5)
    tech_i = next(i for i, b in enumerate(bars) if b["is_tech"])
    ax.annotate("the whole worry", (0.012, tech_i), ha="left", va="center",
                fontsize=10, color=RED, fontweight="bold")
    ax.axvline(0, color=BASELINE, lw=0.9)
    ax.set_xlim(-0.25, 0.20)
    ax.set_xlabel("association with teen well-being (standardized beta); left = worse, right = better")
    ax.set_title("Measured carefully, the digital-tech effect is potato-sized")
    ax.grid(axis="y", visible=False)
    fig.text(0.12, -0.02, "Orben & Przybylski, Nature Human Behaviour 2019, US YRBS data. Across "
             "hundreds of millions of defensible specifications, digital technology\nuse explains at most "
             "0.4% of the variation in well-being, dwarfed by being bullied, and by sleep and "
             "breakfast.", fontsize=8.5, color=MUTED)
    save(fig, "03_contested.png")


def chart4_ruler():
    acc = {a["category"]: a["pct"] for a in R["ruler"]["accuracy"]}
    order = ["Over-reported", "Under-reported", "Accurate (within 5%)"]
    cols = {"Over-reported": BLUE, "Under-reported": YELLOW, "Accurate (within 5%)": AQUA}
    txt = {"Over-reported": "#ffffff", "Under-reported": INK, "Accurate (within 5%)": INK}
    fig, ax = plt.subplots(figsize=(9.0, 3.6))
    left = 0
    for k in order:
        w = acc[k]
        ax.barh(0, w, left=left, color=cols[k], height=0.55, edgecolor=SURFACE, linewidth=1.5)
        if k != "Accurate (within 5%)":
            ax.text(left + w / 2, 0, f"{k}\n{w:.0f}%", ha="center", va="center",
                    fontsize=11, color=txt[k], fontweight="bold")
        left += w
    # accurate is a tiny sliver at the far right; label it above with a pointer
    ax.annotate("accurate\n(within 5%): 6%", xy=(97, 0.28), xytext=(88, 0.62),
                ha="center", va="bottom", fontsize=9.5, color=INK, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.45, 0.9)
    ax.set_yticks([])
    ax.set_xlabel("share of 49 study comparisons of self-reported vs objectively logged screen time")
    ax.set_title("And we can't even measure the cause: self-reports miss both ways")
    ax.grid(False)
    for sp in ["left", "right", "top"]:
        ax.spines[sp].set_visible(False)
    fig.text(0.12, -0.10, "Parry et al., Nature Human Behaviour 2021. Only 3 of 49 comparisons landed "
             "within 5% of actual logged use; self-reported and logged\nscreen time correlate just r "
             "= 0.38. The number the whole debate rests on is one teens cannot accurately give.",
             fontsize=8.5, color=MUTED)
    save(fig, "04_ruler.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_certainty()
    chart2_crisis()
    chart3_contested()
    chart4_ruler()
