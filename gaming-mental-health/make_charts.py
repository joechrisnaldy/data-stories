"""Charts for 'the conclusion was in the definition'. Reads results.json and
oof_pred.csv. Output: charts/*.png on a light surface (dataviz palette)."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

PRETTY = {
    "daily_playtime_hours": "daily playtime", "screen_time_total_hours": "screen time",
    "consecutive_hours_max": "longest session", "late_night_sessions_hours": "late-night hours",
    "weekly_play_sessions": "weekly sessions", "weekend_playtime_hours": "weekend playtime",
    "anxiety_level": "anxiety", "depression_indicator": "depression",
    "loneliness_score": "loneliness", "emotional_stability": "emotional (in)stability",
    "stress_score": "stress", "self_control_score": "self-control",
    "impulsiveness_score": "impulsiveness", "missed_deadlines": "missed deadlines",
    "gpa_or_performance_score": "GPA / performance",
    "sleep_hours": "sleep", "social_interaction_hours": "social hours",
}


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_formula():
    d = pd.read_csv(BASE / "oof_pred.csv")
    fig, ax = plt.subplots(figsize=(7.2, 6))
    lo, hi = 5, 72
    ax.plot([lo, hi], [lo, hi], color=MUTED, lw=1, ls=(0, (4, 3)), zorder=1)
    ax.scatter(d.actual, d.predicted, s=26, color=BLUE, alpha=0.55,
               edgecolor="white", linewidth=0.4, zorder=2)
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_aspect("equal")
    ax.set_xlabel("actual addiction_score")
    ax.set_ylabel("predicted from the OTHER columns")
    ax.set_title("The 'addiction score' is not a measurement. It is arithmetic.")
    ax.annotate(f"cross-validated R² = {R['r2_clean_cv']:.2f}\n"
                f"(1.0 = perfectly rebuilt)\n"
                f"daily playtime alone: R² = {R['r2_daily_playtime_cv']:.2f}",
                (0.04, 0.96), xycoords="axes fraction", va="top", fontsize=11,
                fontweight="bold", color=INK)
    fig.text(0.12, -0.03, "Each point is one of 250 gamers. A plain linear model rebuilds "
             "the score from the raw inputs (excluding the other engineered indices), "
             "out-of-fold.", fontsize=8.5, color=MUTED)
    save(fig, "01_formula.png")


def _hbar(ax, labels, vals, colors):
    y = np.arange(len(labels))
    ax.barh(y, vals, color=colors)
    ax.set_yticks(y, labels, fontsize=9.5)
    ax.invert_yaxis()
    ax.axvline(0, color=BASELINE, lw=0.8)
    ax.grid(axis="y", visible=False)
    for yi, v in zip(y, vals):
        ax.annotate(f"{v:+.2f}", (v, yi), xytext=(6 if v >= 0 else -6, 0),
                    textcoords="offset points", va="center",
                    ha="left" if v >= 0 else "right", fontsize=9,
                    fontweight="bold", color=INK2)


def chart2_madeof():
    tiers = [(R["corr_playtime"], BLUE), (R["corr_impairment"], AQUA),
             (R["corr_mentalhealth"], RED)]
    items = [(PRETTY[k], v, c) for grp, c in tiers for k, v in grp.items()]
    items.sort(key=lambda t: t[1], reverse=True)
    labels, vals, colors = zip(*items)
    fig, ax = plt.subplots(figsize=(9.0, 6.2))
    _hbar(ax, labels, vals, colors)
    ax.set_xlim(-0.52, 1.0)
    ax.set_xlabel("correlation with addiction_score")
    ax.set_title("What the score is built from, and what it barely touches")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (BLUE, AQUA, RED)]
    ax.legend(handles, ["gaming hours", "impulse-control & impairment",
                        "the mental-health scales"], loc="lower right", frameon=False,
              fontsize=9.5)
    fig.text(0.12, -0.02, "The score is a composite of hours plus impulse-control and "
             "impairment columns (impulsiveness and self-control barely correlate with "
             "hours). The mental-health scales it is named for load least of all. Synthetic, "
             "n=250.", fontsize=8.5, color=MUTED)
    save(fig, "02_made_of.png")


def chart3_harm():
    w = R["playtime_vs_wellbeing"]
    items = sorted(((PRETTY[k], d["r"], d["p"]) for k, d in w.items()),
                   key=lambda t: t[1])
    labels, vals, ps = zip(*items)
    # blue = statistically distinguishable from zero (p<0.05); grey = not
    colors = [BLUE if p < 0.05 else MUTED for p in ps]
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    _hbar(ax, labels, vals, colors)
    ax.set_xlim(-0.58, 0.58)
    ax.set_xlabel("correlation of daily playtime with each marker")
    ax.set_title("The harm the label promises is, at most, small")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (BLUE, MUTED)]
    ax.legend(handles, ["real (p < 0.05)", "not distinguishable from zero"],
              loc="upper right", frameon=False, fontsize=9)
    fig.text(0.12, -0.03, "Sleep and stress are the robust effects; anxiety is small but "
             "real; depression and loneliness cannot be told from zero on 250 people. All "
             "of it is far smaller than the word 'addiction' implies. Synthetic.",
             fontsize=8.5, color=MUTED)
    save(fig, "03_harm_small.png")


def chart4_tells():
    df = pd.read_csv(BASE / "data" / "gaming_addiction.csv")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 4))
    a1.hist(df.burnout_probability, bins=30, color=RED)
    a1.set_title("burnout_probability", fontsize=11)
    a1.set_xlabel("value")
    a1.annotate(f"{R['tells']['burnout_prob_eq_1_share']:.0%} of people\nsit at exactly 1.0",
                (0.04, 0.9), xycoords="axes fraction", va="top", fontsize=10,
                fontweight="bold", color=INK)
    a2.hist(df.gpa_or_performance_score.dropna(), bins=30, color=YELLOW)
    a2.set_title("gpa_or_performance_score", fontsize=11)
    a2.set_xlabel("value")
    a2.annotate(f"{R['tells']['gpa_eq_4_share']:.0%} pinned\nat the 4.0 ceiling",
                (0.04, 0.9), xycoords="axes fraction", va="top", fontsize=10,
                fontweight="bold", color=INK)
    for ax in (a1, a2):
        ax.grid(axis="x", visible=False)
        ax.set_ylabel("count")
    fig.suptitle("The tells: columns that never learned to vary",
                 fontsize=13, fontweight="bold", y=1.02)
    fig.text(0.12, -0.06, "Two 'outcome' columns are degenerate, a giveaway that this is a "
             "constructed dataset, not a survey of real lives.", fontsize=8.5, color=MUTED)
    save(fig, "04_tells.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_formula()
    chart2_madeof()
    chart3_harm()
    chart4_tells()
