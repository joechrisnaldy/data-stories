"""Charts for 'Everyone Says Substance. Everyone Picks Chemistry.' Reads results.json.
Output: charts/*.png on a light surface (series dataviz palette).
Women = BLUE, Men = YELLOW throughout (legended; no gender-color stereotype intended)."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())

BLUE, AQUA, YELLOW, RED = "#2a78d6", "#1baf7a", "#eda100", "#e34948"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
W_COLOR, M_COLOR = BLUE, YELLOW

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

PRETTY = {"attr": "attractive", "sinc": "sincere", "intel": "intelligent",
          "fun": "fun", "amb": "ambitious", "shar": "shared interests"}
# fixed display order (roughly by revealed importance), consistent across charts
ORDER = ["attr", "fun", "shar", "intel", "sinc", "amb"]


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def _grouped(metric_key, title, xlabel, fmt, fname, foot):
    W = R[metric_key]["Female"]
    M = R[metric_key]["Male"]
    labels = [PRETTY[a] for a in ORDER]
    wv = [W[a] for a in ORDER]
    mv = [M[a] for a in ORDER]
    y = np.arange(len(ORDER))
    h = 0.38
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    ax.barh(y + h / 2, wv, height=h, color=W_COLOR, label="women")
    ax.barh(y - h / 2, mv, height=h, color=M_COLOR, label="men")
    ax.set_yticks(y, labels, fontsize=10.5)
    ax.invert_yaxis()
    for yi, v in zip(y + h / 2, wv):
        ax.annotate(fmt(v), (v, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=INK2)
    for yi, v in zip(y - h / 2, mv):
        ax.annotate(fmt(v), (v, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=INK2)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.grid(axis="y", visible=False)
    ax.legend(loc="lower right", frameon=False, fontsize=10)
    fig.text(0.12, -0.02, foot, fontsize=8.5, color=MUTED)
    save(fig, fname)


def chart1_stated():
    _grouped("stated_by_gender",
             "What people SAY they want in a date",
             "points allocated (out of 100)", lambda v: f"{v:.0f}",
             "01_stated.png",
             "Mean of the 100-point 'what I look for' allocation, by gender. Men lead with "
             "looks; women lead with intelligence. 100-point-allocation waves only.")


def chart2_revealed():
    _grouped("revealed_corr_by_gender",
             "What actually earns a 'yes'",
             "correlation of the rating with the yes decision", lambda v: f"{v:.2f}",
             "02_revealed.png",
             "Correlation of each 1-to-10 partner rating with the decision to say yes, by "
             "gender. Attractiveness leads for both; the substance traits barely move it.")


def _decollide(items, ys, mingap):
    """Push labels apart vertically (ascending) so they do not overlap."""
    order = sorted(range(len(items)), key=lambda i: ys[i])
    adj = list(ys)
    for k in range(1, len(order)):
        i, j = order[k], order[k - 1]
        if adj[i] - adj[j] < mingap:
            adj[i] = adj[j] + mingap
    return adj


def chart3_gap():
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 5.8))
    for ax, g in [(axes[0], "Female"), (axes[1], "Male")]:
        ss = R["stated_share_by_gender"][g]
        rs = R["revealed_share_by_gender"][g]
        span = max(list(ss.values()) + list(rs.values()))
        for a in ORDER:
            hot = a in ("intel", "attr")
            col = RED if a == "intel" else (BLUE if a == "attr" else MUTED)
            ax.plot([0, 1], [ss[a], rs[a]], color=col, lw=2.6 if hot else 1.1,
                    marker="o", markersize=6, alpha=1.0 if hot else 0.4,
                    zorder=3 if hot else 2)
        # right-side value labels ONLY for the two highlighted story lines
        for a, col in [("intel", RED), ("attr", BLUE)]:
            ax.annotate(f"{rs[a]:.0%}", (1, rs[a]), xytext=(7, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=9, fontweight="bold", color=col)
        # left-side trait names, de-collided
        left_y = _decollide(ORDER, [ss[a] for a in ORDER], span * 0.058)
        for a, y in zip(ORDER, left_y):
            hot = a in ("intel", "attr")
            col = RED if a == "intel" else (BLUE if a == "attr" else MUTED)
            ax.annotate(PRETTY[a], (0, y), xytext=(-8, 0), textcoords="offset points",
                        ha="right", va="center", fontsize=8.7,
                        color=col if hot else MUTED, fontweight="bold" if hot else "normal")
        ax.set_xlim(-0.62, 1.22)
        ax.set_xticks([0, 1], ["what they\nSAY", "what earns\na YES"], fontsize=9.5)
        ax.set_ylim(0, span * 1.14)
        ax.yaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
        ax.set_title("Women" if g == "Female" else "Men", fontsize=12)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("share of stated / revealed importance")
    fig.suptitle("Intelligence is what we say; looks and chemistry are what we pick",
                 fontsize=13, fontweight="bold", y=1.02)
    fig.text(0.5, -0.02, "Each trait's share of stated importance (left) versus its share of "
             "what actually predicted a yes (right), normalized within each gender. "
             "Intelligence (red) collapses for both; attractiveness (blue) rises or stays on top.",
             ha="center", fontsize=8.5, color=MUTED)
    save(fig, "03_say_do_gap.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_stated()
    chart2_revealed()
    chart3_gap()
