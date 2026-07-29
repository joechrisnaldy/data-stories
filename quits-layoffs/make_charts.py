"""Charts for Post 15 'Nobody Quit. Nobody Was Unemployed Either.'
Reads results.json. Output: charts/quits-N-name.png."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())
C, V = R["computed"], R["verified"]

BLUE, GREEN, AMBER, RED = "#2a78d6", "#1baf7a", "#eda100", "#e34948"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE, SHADE = "#e1e0d9", "#c3c2b7", "#fcfcfb", "#ecebe4"

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": BASELINE, "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": INK2,
    "text.color": INK, "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "font.size": 10.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "text.parse_math": False,
})

prime = pd.read_stata(BASE / "data" / "qlmonthly_prime.dta").set_index("time").sort_index()
allw = pd.read_stata(BASE / "data" / "qlmonthly_all.dta").set_index("time").sort_index()
RECS = [(v["start"], v["end"]) for v in C["recessions"].values()]


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def shade(ax):
    for a, b in RECS:
        ax.axvspan(pd.Timestamp(a), pd.Timestamp(b), color=SHADE, zorder=0)


def chart1_resignation():
    """Same period, two measures, one shared axis.

    Both pairs are drawn against the same y-axis on purpose. The height gap between the JOLTS pair
    and the household pair is not a nuisance to be scaled away: it IS the job-to-job switching this
    essay is about, because JOLTS counts every quit while the household series counts only the ones
    that end in non-employment.
    """
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    j = [V["jolts_quits_rate_2019_avg"], V["jolts_quits_rate_record"]]
    c = [C["eras"]["2019"]["quits"], C["eras"]["great_resignation_2021_22"]["quits"]]
    xs = [0, 1, 2.5, 3.5]
    vals = j + c
    ax.bar(xs, vals, color=[MUTED, RED, MUTED, BLUE], width=0.62)
    # Not "record": the Nov 2021 RATE matched the September 2021 high rather than setting one.
    ax.set_xticks(xs, ["2019\naverage", "November 2021\nseries high", "2019\naverage",
                       "2021 to 2022\naverage"], fontsize=10)
    # JOLTS is published to one decimal; the household series is quoted to three in the body, so
    # the labels match the prose exactly rather than rounding to a number that appears nowhere else.
    for x, v, dp in zip(xs, vals, [1, 1, 3, 3]):
        ax.annotate(f"{v:.{dp}f}%", (x, v), xytext=(0, 5), textcoords="offset points",
                    ha="center", fontsize=13, fontweight="bold", color=INK)
    ax.set_ylim(0, 4.3)
    ax.set_ylabel("quits, % of employment per month")
    ax.set_title("The Great Resignation, measured two ways")
    ax.grid(axis="x", visible=False)

    def bracket(x0, x1, y, label, sub, colour):
        ax.plot([x0, x0, x1, x1], [y - 0.09, y, y, y - 0.09], color=colour, lw=1.2)
        ax.annotate(label, ((x0 + x1) / 2, y + 0.55), ha="center", fontsize=15,
                    fontweight="bold", color=colour)
        ax.annotate(sub, ((x0 + x1) / 2, y + 0.12), ha="center", va="bottom",
                    fontsize=9, color=MUTED)

    bracket(0, 1, 3.20, f"{V['jolts_quits_pct_change_2019_to_peak']:+.0f}%",
            "JOLTS: every quit, even straight\ninto another job", RED)
    bracket(2.5, 3.5, 1.22, "no change",
            "Household survey: only quits that\nended in non-employment", BLUE)
    ax.annotate("the gap between the two pairs is\nthe quitting that never left work",
                (1.42, 2.30), ha="left", va="top", fontsize=9, color=INK2, style="italic")
    fig.text(0.09, -0.09, "Both pairs share one axis. Left pair: BLS JOLTS quits rate, "
             "establishment-based, all nonfarm payrolls at any age; 2019 average\nagainst November "
             "2021, which matched the series high set that September. Right pair: quits into "
             "non-employment, household-based, prime "
             "age (Ellieroth and Michaud,\nMinneapolis Fed); 2019 average against the 2021 to 2022 "
             "average. The right-hand pair differs by 1.5%, which a Welch test on\nthose windows "
             "cannot distinguish from zero (p = 0.81), so it is labelled as no change. On all ages "
             "the same comparison gives\n+2.8%, and on a matched single month, November 2021, +5.9% "
             "prime age and +7.3% all ages. Single digits, either way.",
             fontsize=8.5, color=MUTED)
    save(fig, "quits-1-resignation-that-wasnt.png")


def chart2_vanishing():
    """Share of laid-off workers who leave the labour force entirely."""
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    shade(ax)
    # raw monthly faint, 12-month rolling mean bold, so the level is readable
    for df, col, lab in [(allw, AMBER, "All workers 16+"), (prime, BLUE, "Prime age 25-55")]:
        s = df.share_layoff_n_seats * 100
        ax.plot(df.index, s, color=col, lw=0.6, alpha=0.25)
        ax.plot(df.index, s.rolling(12, center=True).mean(), color=col, lw=2.2, label=lab)
    ax.axhline(C["prime"]["mean_share_layoff_to_nilf"] * 100, color=INK2, ls="--", lw=1.0)
    ax.annotate(f"prime-age average, {C['prime']['mean_share_layoff_to_nilf']*100:.0f}%",
                (pd.Timestamp("2026-04-01"), C["prime"]["mean_share_layoff_to_nilf"] * 100 - 3.2),
                ha="right", fontsize=9, color=INK2, fontweight="bold")
    ax.set_ylim(10, 70)
    ax.set_ylabel("share of newly laid-off workers who leave the labour force")
    ax.set_title("A third of laid-off workers never become 'unemployed'")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left", frameon=False, fontsize=9.5, ncols=2)
    fig.text(0.09, -0.14, "Ellieroth and Michaud (Minneapolis Fed), from Current Population Survey "
             "microdata. Bold lines are 12-month averages, faint lines the raw\nmonthly series. "
             "Shaded bands are recessions. To count as unemployed you must have looked for work in "
             "the previous four weeks, unless you\nare awaiting recall from a temporary layoff; "
             "these workers did neither, so they leave the labour force and the unemployment rate "
             "never\nsees them. The share dips in most recessions, 2001 excepted, which the authors "
             "report as a finding of their own. The series falls through\nthe 1980s and 1990s and "
             "rises after, ending a little above the middle of the sample; a straight line through "
             "it explains 5% of the variation,\nso nothing here is built on a trend.",
             fontsize=8.5, color=MUTED)
    save(fig, "quits-2-vanishing.png")


def chart3_layoffs_vs_quits():
    """48 years: layoffs sit above quits almost always."""
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    shade(ax)
    ax.plot(prime.index, prime.elall_seats, color=RED, lw=1.3, label="Laid off")
    ax.plot(prime.index, prime.eqall_seats, color=GREEN, lw=1.3, label="Quit")
    ax.set_ylim(0, 3.0)
    ax.set_ylabel("% of prime-age employment, per month")
    ax.set_title("For prime-age workers, layoffs sit above quits in 88% of the last 48 years")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left", frameon=False, fontsize=10, ncols=2)
    ax.annotate(f"April 2020: layoffs hit {C['covid_apr2020_layoff']:.1f}%,\n"
                f"{C['covid_multiple']:.2f} times the average,\nwhile quits fell to "
                f"{C['covid_apr2020_quit']:.2f}%",
                (pd.Timestamp("2020-04-01"), 2.92), xytext=(pd.Timestamp("2006-01-01"), 2.55),
                fontsize=9, color=INK2, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2))
    fig.text(0.09, -0.06, "Ellieroth and Michaud (Minneapolis Fed), prime-age transitions from "
             "employment into non-employment. Shaded bands are recessions.\nThe axis is clipped at "
             "3%: the April 2020 layoff spike runs to 10.7%. Quits and layoffs move against each "
             f"other, correlation {C['corr_quits_layoffs']['prime_monthly']:.2f} on the monthly "
             "series plotted here.\nThe ordering reverses for all workers 16 and over, where teenage "
             "and older-worker quitting is much heavier: there, quits sit\nabove layoffs in "
             f"{(C['n_months'] - C['months_layoffs_exceed_quits_all']) / C['n_months'] * 100:.0f}% "
             "of months.", fontsize=8.5, color=MUTED)
    save(fig, "quits-3-layoffs-vs-quits.png")


def chart4_where_they_go():
    """Every layoff splits two ways, and the split moves across recessions."""
    recs = C["recessions"]
    labels = list(recs.keys())
    # Weighted by how many people were laid off each month, because the claim is about people.
    # It matters only for COVID, whose 3-month window mixes a normal February with a 10.7% April.
    to_nilf = np.array([recs[k]["wtd_share_to_nilf"] for k in labels]) * 100
    to_unemp = 100 - to_nilf
    fig, ax = plt.subplots(figsize=(9.4, 5.2))
    x = np.arange(len(labels))
    ax.bar(x, to_unemp, color=BLUE, width=0.62, label="Counted: still searching, so 'unemployed'")
    ax.bar(x, to_nilf, bottom=to_unemp, color=AMBER, width=0.62,
           label="Uncounted: left the labour force")
    ax.set_xticks(x, labels, fontsize=10.5)
    for xi, (u, n) in enumerate(zip(to_unemp, to_nilf)):
        ax.annotate(f"{u:.0f}%", (xi, u / 2), ha="center", va="center", color="#ffffff",
                    fontsize=11, fontweight="bold")
        ax.annotate(f"{n:.0f}%", (xi, u + n / 2), ha="center", va="center", color=INK,
                    fontsize=11, fontweight="bold")
    ax.axhline(100 - C["prime"]["mean_share_layoff_to_nilf"] * 100, color=INK2, ls="--", lw=1.1)
    ax.annotate("48-year average split", (-0.42,
                100 - C["prime"]["mean_share_layoff_to_nilf"] * 100 + 1.5),
                ha="left", fontsize=9, color=INK2, fontweight="bold")
    ax.set_ylim(0, 100)
    ax.set_ylabel("where newly laid-off prime-age workers went")
    ax.set_title("Every layoff splits two ways, and only one of them is counted")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.28), frameon=False, fontsize=9.5, ncols=2)
    fig.text(0.09, -0.22, "Ellieroth and Michaud (Minneapolis Fed), averaged across each NBER "
             "peak-to-trough window and weighted by the number laid off each\nmonth. Windows differ "
             "in length, from 3 months in 2020 to 19 in 1981 to 1982, and the 2020 window includes "
             "February, before the collapse.\nThe uncounted share tends to be smallest in the "
             "sharpest downturns, which is a tendency rather than a rule: 2001 is the mildest "
             "recession\nhere and has the largest uncounted share. In April 2020, 18.1 million of "
             "the 23.1 million unemployed were on temporary layoff, and people\nawaiting recall are "
             "counted as unemployed without an active search, which is why 2020 has the smallest "
             "uncounted share.",
             fontsize=8.5, color=MUTED)
    save(fig, "quits-4-where-they-go.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_resignation()
    chart2_vanishing()
    chart3_layoffs_vs_quits()
    chart4_where_they_go()
    print("built all 4 charts")
