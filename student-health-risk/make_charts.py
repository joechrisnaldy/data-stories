"""Charts for the "metric encodes your values" post.

Reads model/results.json (validation metrics + confusion matrices) and data/train.csv
(for the domain distributions). Output: charts/*.png on a light surface.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

BASE = Path(__file__).resolve().parent
RESULTS = json.loads((BASE / "model" / "results.json").read_text())

# palette (dataviz): semantic class colors + chart chrome
FIT, ATRISK, UNHEALTHY = "#1baf7a", "#eda100", "#e34948"   # green / amber / red
BLUE = "#2a78d6"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
CLASS_COLOR = {"fit": FIT, "at-risk": ATRISK, "unhealthy": UNHEALTHY}
LABELS = RESULTS["labels"]  # ["fit", "at-risk", "unhealthy"]

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


def chart1_imbalance():
    counts = RESULTS["class_counts"]
    n = RESULTS["n_train"]
    order = ["fit", "at-risk", "unhealthy"]
    pct = [counts[c] / n * 100 for c in order]
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    bars = ax.barh(order, pct, color=[CLASS_COLOR[c] for c in order])
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.grid(axis="y", visible=False)
    for c, p, b in zip(order, pct, bars):
        ax.annotate(f"{p:.1f}%", (p, b.get_y() + b.get_height() / 2),
                    xytext=(6, 0), textcoords="offset points", va="center",
                    fontweight="bold", color=CLASS_COLOR[c])
    ax.set_title("85.9% of students are labeled 'at-risk'")
    base = RESULTS["baseline"]
    ax.set_xlabel("share of training set")
    fig.text(0.125, -0.04, "Predict 'at-risk' for everyone and you score "
             f"{base['accuracy']*100:.1f}% accuracy, but balanced accuracy "
             f"{base['balanced_accuracy']:.3f}, the floor. Source: Kaggle Playground S6E7.",
             fontsize=8.5, color=MUTED)
    save(fig, "01_imbalance.png")


def _confusion_ax(ax, cm, title):
    cm = np.array(cm, float)
    recall = cm / cm.sum(axis=1, keepdims=True)  # row-normalized
    cmap = LinearSegmentedColormap.from_list("blues", ["#f4f8fd", BLUE])
    ax.imshow(recall, cmap=cmap, vmin=0, vmax=1, aspect="equal")
    ax.set_xticks(range(3), LABELS, fontsize=9)
    ax.set_yticks(range(3), LABELS, fontsize=9)
    ax.set_xlabel("predicted", color=INK2)
    ax.set_title(title, fontsize=11)
    ax.grid(False)
    for i in range(3):
        for j in range(3):
            v = recall[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=10,
                    color="white" if v > 0.55 else INK,
                    fontweight="bold" if i == j else "normal")


def chart2_confusion():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.9))
    _confusion_ax(a1, RESULTS["A"]["confusion"],
                  f"Model A (accuracy)\nbalanced acc {RESULTS['A']['balanced_accuracy']:.3f}")
    _confusion_ax(a2, RESULTS["B"]["confusion"],
                  f"Model B (balanced weights)\nbalanced acc {RESULTS['B']['balanced_accuracy']:.3f}")
    a1.set_ylabel("actual", color=INK2)
    fig.suptitle("Same model, same data. The metric decides where the errors go.",
                 fontsize=13, fontweight="bold", y=1.02)
    fig.text(0.125, -0.02, "Row-normalized (recall): each row sums to 1. Model A protects "
             "the majority (at-risk 0.99) and lets the rare classes leak; Model B spreads "
             "its attention across all three.", fontsize=8.5, color=MUTED)
    save(fig, "02_confusion.png")


def chart3_tradeoff():
    a, b = RESULTS["A"], RESULTS["B"]
    groups = ["Model A\n(accuracy)", "Model B\n(balanced)"]
    acc = [a["accuracy"], b["accuracy"]]
    bal = [a["balanced_accuracy"], b["balanced_accuracy"]]
    x = np.arange(2)
    w = 0.36
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    b1 = ax.bar(x - w/2, acc, w, color=MUTED, label="accuracy")
    b2 = ax.bar(x + w/2, bal, w, color=BLUE, label="balanced accuracy (the metric)")
    ax.set_xticks(x, groups)
    ax.set_ylim(0, 1.05)
    ax.grid(axis="x", visible=False)
    ax.axhline(RESULTS["baseline"]["balanced_accuracy"], color=UNHEALTHY, lw=1,
               ls=(0, (4, 3)))
    ax.annotate("0.333 floor (all at-risk)", (1.4, RESULTS["baseline"]["balanced_accuracy"]),
                xytext=(0, 4), textcoords="offset points", color=UNHEALTHY, fontsize=8.5)
    for bars in (b1, b2):
        for bar in bars:
            ax.annotate(f"{bar.get_height():.3f}", (bar.get_x()+bar.get_width()/2, bar.get_height()),
                        xytext=(0, 3), textcoords="offset points", ha="center",
                        fontsize=9, fontweight="bold", color=INK2)
    ax.legend(loc="lower center", frameon=False, fontsize=9, ncol=2)
    ax.set_title("More accurate and better point in opposite directions")
    fig.text(0.125, -0.03, "Model B is 3 points less accurate but wins the balanced-accuracy "
             f"metric. Live leaderboard confirmed it: A {a.get('lb', 0.87241):.3f} vs "
             f"B {b.get('lb', 0.94991):.3f}.", fontsize=8.5, color=MUTED)
    save(fig, "03_tradeoff.png")


def chart4_separators(train):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.4))
    order = ["fit", "at-risk", "unhealthy"]
    for ax, col, title, unit in (
            (ax1, "sleep_duration", "Sleep", "hours / night"),
            (ax2, "step_count", "Movement", "steps / day")):
        data = [train.loc[train.health_condition == c, col].dropna().values for c in order]
        bp = ax.boxplot(data, tick_labels=order, patch_artist=True, showfliers=False,
                        medianprops={"color": INK, "linewidth": 1.5},
                        widths=0.6)
        for patch, c in zip(bp["boxes"], order):
            patch.set_facecolor(CLASS_COLOR[c]); patch.set_alpha(0.85)
            patch.set_edgecolor(CLASS_COLOR[c])
        for whisk in bp["whiskers"] + bp["caps"]:
            whisk.set_color(MUTED)
        ax.set_title(title)
        ax.set_ylabel(unit, color=INK2)
        ax.grid(axis="x", visible=False)
    fig.suptitle("What separates them: the fit move a lot; the unhealthy barely sleep",
                 fontsize=13, fontweight="bold", y=1.01)
    fig.text(0.125, -0.03, "Distributions by class (outliers hidden). Data is synthetic "
             "(Kaggle-generated), so read these as modeled patterns, not epidemiology.",
             fontsize=8.5, color=MUTED)
    save(fig, "04_separators.png")


def chart5_profile(train):
    order = ["fit", "at-risk", "unhealthy"]
    feats = [("sleep_duration", "Sleep (h)"), ("step_count", "Steps"),
             ("exercise_duration", "Exercise (min)"), ("bmi", "BMI")]
    fig, axes = plt.subplots(1, 4, figsize=(11, 3.4))
    for ax, (col, label) in zip(axes, feats):
        means = [train.loc[train.health_condition == c, col].mean() for c in order]
        bars = ax.bar(order, means, color=[CLASS_COLOR[c] for c in order])
        ax.set_title(label, fontsize=11)
        ax.grid(axis="x", visible=False)
        ax.tick_params(axis="x", labelrotation=30, labelsize=8.5)
        top = max(means)
        for m, bar in zip(means, bars):
            ax.annotate(f"{m:,.0f}" if top > 100 else f"{m:.1f}",
                        (bar.get_x()+bar.get_width()/2, m), xytext=(0, 2),
                        textcoords="offset points", ha="center", fontsize=8.5, color=INK2)
        ax.set_ylim(0, top * 1.18)
    fig.suptitle("The behavior profile of each class", fontsize=13, fontweight="bold", y=1.04)
    fig.text(0.09, -0.05, "Class means. 'Fit' sleeps more, moves far more, and is leaner; "
             "'unhealthy' is defined most by short sleep. Synthetic data.",
             fontsize=8.5, color=MUTED)
    save(fig, "05_profile.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    # inject leaderboard scores for the caption
    RESULTS["A"]["lb"], RESULTS["B"]["lb"] = 0.87241, 0.94991
    train = pd.read_csv(BASE / "data" / "train.csv",
                        usecols=["health_condition", "sleep_duration", "step_count",
                                 "exercise_duration", "bmi"])
    chart1_imbalance()
    chart2_confusion()
    chart3_tradeoff()
    chart4_separators(train)
    chart5_profile(train)
