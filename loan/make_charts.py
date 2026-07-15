"""Charts for 'What the Bank Sees When It Looks at You'. Reads results.json.
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


def chart1_what_weighs():
    rows = R["corr_approval"][::-1]               # barh bottom-up: strongest on top
    names = [r["nice"] for r in rows]
    mags = [abs(r["corr"]) for r in rows]
    signs = [r["corr"] for r in rows]
    colors = [RED if r["feature"] == "CreditScore"
              else (AQUA if r["feature"] == "AnnualIncome" else BLUE) for r in rows]
    fig, ax = plt.subplots(figsize=(8.8, 6.2))
    y = np.arange(len(names))
    ax.barh(y, mags, color=colors, height=0.72)
    ax.set_yticks(y, names, fontsize=10.5)
    for yi, m, s in zip(y, mags, signs):
        tag = "more likely" if s > 0 else "less likely"
        ax.annotate(f"{m:.2f}  ({tag})", (m, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=INK2)
    ax.set_xlim(0, max(mags) * 1.28)
    ax.set_xlabel("strength of link to getting approved (|correlation|)")
    ax.set_title("What the decision actually weighs: income and debt, not your credit score")
    ax.grid(axis="y", visible=False)
    fig.text(0.12, -0.02, "Curated features, correlation with approval on 20,000 synthetic "
             "applicants. Annual income (green) dominates; the credit score people guard (red) "
             "is near the\nbottom. A gradient-boosting model agrees.", fontsize=8.5, color=MUTED)
    save(fig, "01_what_weighs.png")


def chart2_credit_prices():
    s = R["credit_rate_scatter"]
    x = np.array([p["credit"] for p in s])
    yv = np.array([p["rate"] * 100 for p in s])   # percent
    fig, ax = plt.subplots(figsize=(8.4, 6.2))
    ax.scatter(x, yv, s=10, color=BLUE, alpha=0.25, edgecolor="none", zorder=3)
    ax.set_xlabel("credit score")
    ax.set_ylabel("loan interest rate offered (%)")
    ax.set_title("Your credit score prices you, it does not judge you")
    ax.annotate(f"correlation = {R['credit_rate_corr']:.2f}", (0.05, 0.90),
                xycoords="axes fraction", fontsize=11, color=INK, fontweight="bold")
    fig.text(0.12, -0.04, "Each dot is an applicant. A better credit score buys a lower interest "
             "rate, almost mechanically. And it is the interest rate, not the score itself, that\n"
             "the approval decision leans on. Synthetic data.", fontsize=8.5, color=MUTED)
    save(fig, "02_credit_prices.png")


def chart3_not_risk():
    labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rate_by_month = {r["month"]: r["rate"] * 100 for r in R["approval_by_month"]}
    rates = [rate_by_month[i] for i in range(1, 13)]
    colors = [YELLOW if 3 <= i <= 8 else "#c2c1b8" for i in range(1, 13)]   # spring/summer bonus
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    x = np.arange(12)
    ax.bar(x, rates, color=colors, width=0.7)
    ax.set_xticks(x, labels, fontsize=9.5)
    for xi, r in zip(x, rates):
        ax.annotate(f"{r:.0f}", (xi, r), xytext=(0, 3), textcoords="offset points",
                    ha="center", fontsize=8, color=INK2)
    ax.set_ylim(0, max(rates) * 1.18)
    ax.set_ylabel("share of applicants approved (%)")
    ax.set_xlabel("month of application")
    ax.set_title("A factor with no risk story: the month you apply")
    ax.grid(axis="x", visible=False)
    ss = R["season"]["spring_summer_rate"] * 100
    rest = R["season"]["rest_rate"] * 100
    fig.text(0.12, -0.05, "Approval rate by application month (synthetic data). Application dates "
             "are assigned independently of the applicant, so this gap is purely the rulebook's\n"
             "seasonal bonus: spring and summer (yellow, months 3 to 8) approve %.1f%% against "
             "%.1f%% the rest of the year. A choice with no risk story." % (ss, rest),
             fontsize=8.5, color=MUTED)
    save(fig, "03_not_risk.png")


def chart4_no_score():
    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    ax.axis("off")
    ax.set_title("The rulebook can only judge people it can already see", loc="left", pad=16)
    ax.text(0.01, 0.60, "20,000 of 20,000", fontsize=30, color=BLUE, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.01, 0.44, "applicants in this dataset already have\nincome, accounts and a credit "
            "history:\nfully legible to any scorecard", fontsize=11, color=INK2,
            transform=ax.transAxes, va="top")
    ax.text(0.55, 0.60, "~1.3 billion", fontsize=30, color=RED, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.55, 0.44, "adults worldwide have no bank account,\ncast no financial shadow, and are"
            "\ninvisible to any credit rulebook", fontsize=11, color=INK2,
            transform=ax.transAxes, va="top")
    ax.axvline(0.51, ymin=0.12, ymax=0.80, color=BASELINE, lw=0.8)
    fig.text(0.01, 0.0, "Left: this dataset (synthetic). Right: World Bank Global Findex 2025. A "
             "credit score is a stack of choices, and also a fence.", fontsize=8.5, color=MUTED)
    save(fig, "04_no_score.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_what_weighs()
    chart2_credit_prices()
    chart3_not_risk()
    chart4_no_score()
