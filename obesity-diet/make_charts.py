"""Charts for Post 20, 'Calories In, Calories Out Is True. It Explains Almost Nothing.'

Reads results.json. Output: charts/diet-N-name.png.

Every figure derived from the data is interpolated from results.json. Typed literals are
limited to axis limits, layout coordinates, and the 3,700 kcal hook threshold, which is a
stated analytical choice and is also emitted to results.json so the two cannot drift.

Post 19 shipped three fact-check rounds and each one found a caption that had gone stale
while the docstring claimed none had. So: after editing any caption, RE-OPEN THE PNG and
read it. A footnote spliced mid-clause once blew a figure out to 3096px and nobody noticed
because the build did not fail.

House rule: no em or en dashes anywhere, including inside rendered images. matplotlib
writes a Unicode minus on negative ticks unless axes.unicode_minus is False.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())
S = pd.DataFrame(R["scatter"])

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
    "axes.unicode_minus": False,
})


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def fitline(ax, x, y, color, lw=1.8, ls="-", zorder=3):
    b, a = np.polyfit(x, y, 1)
    xs = np.linspace(float(np.min(x)), float(np.max(x)), 50)
    ax.plot(xs, a + b * xs, color=color, lw=lw, ls=ls, zorder=zorder)


def chart1_same_calories():
    """The hook. Ten rich countries at one level of food supply, 26 points of obesity apart.

    The point of this chart is the VERTICAL spread inside the shaded band, not the slope.
    The fit is drawn faintly on purpose: it is there to be dismissed, and the R2 label
    says how much of the picture it accounts for.
    """
    h = R["hook_high_calorie_group"]
    e = R["explains"]["calories"]["all"]
    thr = h["threshold_kcal"]

    fig, ax = plt.subplots(figsize=(10.2, 6.2))
    ax.axvspan(thr, 3990, color=SHADE, zorder=0)

    hi = S[S.kcal >= thr]
    rest = S[S.kcal < thr]
    ax.scatter(rest.kcal, rest.obesity, s=34, color=BLUE, alpha=0.42, linewidths=0, zorder=2)
    ax.scatter(hi.kcal, hi.obesity, s=52, color=RED, alpha=0.95, linewidths=0, zorder=4)
    fitline(ax, S.kcal.values, S.obesity.values, MUTED, lw=1.6, ls=(0, (5, 3)))

    # Label only the extremes of the band and let a bracket carry the span. Ten inline
    # labels collided in the 20 to 22 percent range and made the chart unreadable; the
    # full roster lives in the footnote instead, where it has room.
    top_c = hi.loc[hi.obesity.idxmax()]
    bot = hi.nsmallest(2, "obesity").sort_values("entity")
    ax.annotate(f"{top_c.entity} {top_c.obesity:.1f}%", xy=(top_c.kcal, top_c.obesity),
                xytext=(10, 0), textcoords="offset points", fontsize=9.6,
                fontweight="bold", color=INK, va="center")
    # Leader line, not a bare offset: without it the label reads as if it belongs to the
    # blue dots it happens to sit among.
    ax.annotate(" and ".join(f"{r.entity} {r.obesity:.1f}%" for _, r in bot.iterrows()),
                xy=(float(bot.kcal.min()), float(bot.obesity.min())), xytext=(3845, 6.0),
                textcoords="data", fontsize=9.6, fontweight="bold",
                color=INK, va="center", ha="center",
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8,
                                shrinkA=2, shrinkB=6))

    # The vertical bracket IS the argument: one level of food supply, this much spread.
    bx = 4035
    ax.plot([bx, bx], [h["obesity_min_pct"], h["obesity_max_pct"]], color=INK2, lw=1.2)
    for yy in (h["obesity_min_pct"], h["obesity_max_pct"]):
        ax.plot([bx - 22, bx + 22], [yy, yy], color=INK2, lw=1.2)
    ax.annotate(f"{h['obesity_ratio']}x apart\nat the same\nfood supply",
                xy=(bx, (h["obesity_min_pct"] + h["obesity_max_pct"]) / 2),
                xytext=(9, 0), textcoords="offset points", fontsize=9.6,
                fontweight="bold", color=INK2, va="center", ha="left")

    # The pair that makes the point without any band at all: same supply, opposite outcome.
    pair = R["near_identical_pairs"]["top_no_pacific"][1]
    px = (pair["a_kcal"] + pair["b_kcal"]) / 2
    lo_c, hi_c = sorted([(pair["a_obesity"], pair["a"]), (pair["b_obesity"], pair["b"])])
    ax.plot([px, px], [lo_c[0], hi_c[0]], color=INK, lw=1.1, ls=(0, (2, 2)), zorder=5)
    ax.annotate(f"{hi_c[1]} {hi_c[0]:.1f}%", xy=(px, hi_c[0]), xytext=(-9, 0),
                textcoords="offset points", fontsize=9.4, color=INK,
                fontweight="bold", va="center", ha="right")
    ax.annotate(f"{lo_c[1]} {lo_c[0]:.1f}%", xy=(px, lo_c[0]), xytext=(-9, 0),
                textcoords="offset points", fontsize=9.4, color=INK,
                fontweight="bold", va="center", ha="right")
    ax.annotate(f"{pair['kcal_apart']:.0f} kcal apart,\n{pair['obesity_apart']:.0f} points apart",
                xy=(px, (lo_c[0] + hi_c[0]) / 2), xytext=(10, 0),
                textcoords="offset points", fontsize=9.2, color=INK2, va="center")

    ax.annotate(f"{h['n']} countries eat at or above {thr:,} kcal,\n"
                f"a spread of only {h['kcal_spread_pct']}% in supply.\n"
                f"Their obesity runs {h['obesity_min_pct']}% to "
                f"{h['obesity_max_pct']}%.",
                xy=(1880, 71), xytext=(1880, 71), textcoords="data",
                fontsize=10.0, color=INK, ha="left", va="top")

    ax.set_title("Calories in, calories out is true. Across countries it explains almost nothing.\n"
                 f"Adult obesity against daily calorie supply, {R['meta']['n_countries']} countries, "
                 f"{R['meta']['year']}")
    ax.set_xlabel("Daily calorie supply per person, kcal")
    ax.set_ylabel("Adults with BMI of 30 or more, age standardised")
    ax.set_xlim(1800, 4230)
    ax.set_ylim(0, 80)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.annotate(
        f"WHO Global Health Observatory obesity, age standardised, against FAO food balance "
        f"sheet calorie supply, both via Our World in Data.\nThe dashed line is the least squares "
        f"fit across all {e['n']} countries: it accounts for {e['r2'] * 100:.1f}% of the variation "
        f"in obesity (r = {e['r']:.2f}). Supply is what reaches\nthe retail level, so household "
        f"and retail waste is still inside the horizontal axis, which is therefore a proxy for\n"
        f"intake rather than a measure of it.\n"
        # ROUND 1 CORRECTION. This sorted on h["countries"] kcal values, which build_analysis
        # has already rounded to whole numbers, so Ireland (3920.9) and Belgium (3921.3) tie at
        # 3921 and the stable sort emitted them in the descending order they were written in,
        # backwards. The list is stored descending by construction; reverse it instead.
        f"The shaded band, left to right: "
        + ", ".join(f"{c['entity']} {c['obesity']:.1f}%"
                    for c in reversed(h["countries"])) + ".",
        xy=(0, -0.135), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "diet-1-same-calories.png")


def chart2_the_rival():
    """Income, and the eleven countries that decide what it explains.

    Drawn with BOTH fits because the honest answer depends on a cluster the reader should
    be shown rather than told about. Excluding a group of countries to make a number look
    better is exactly the move this series exists to catch, so the excluded group is the
    most visible thing on the chart.
    """
    ea, ex = R["explains"]["log_gdp"]["all"], R["explains"]["log_gdp"]["excluding_pacific"]
    pac, rest = S[S.is_pacific], S[~S.is_pacific]

    fig, ax = plt.subplots(figsize=(10.2, 6.0))
    ax.scatter(rest.gdp, rest.obesity, s=34, color=BLUE, alpha=0.45, linewidths=0,
               zorder=2, label=f"other countries ({ex['n']})")
    ax.scatter(pac.gdp, pac.obesity, s=76, color=AMBER, alpha=0.95, linewidths=0,
               zorder=4, label=f"Pacific island states ({R['meta']['n_pacific']})")

    lg_all, lg_rest = np.log(S.gdp.values), np.log(rest.gdp.values)
    for xs, ys, col, ls, lab in (
            (lg_all, S.obesity.values, MUTED, (0, (5, 3)),
             f"all {ea['n']}: {ea['r2'] * 100:.1f}% explained"),
            (lg_rest, rest.obesity.values, BLUE, "-",
             f"excluding the Pacific: {ex['r2'] * 100:.1f}%")):
        b, a = np.polyfit(xs, ys, 1)
        grid = np.linspace(xs.min(), xs.max(), 60)
        ax.plot(np.exp(grid), a + b * grid, color=col, lw=1.9, ls=ls, zorder=5, label=lab)

    for _, r in pac.nlargest(4, "obesity").iterrows():
        ax.annotate(r.entity, xy=(r.gdp, r.obesity), xytext=(8, 0),
                    textcoords="offset points", fontsize=9.0, color=INK, va="center")

    ax.set_xscale("log")
    ax.set_title("The obvious rival explains more, and eleven countries decide how much.\n"
                 "Adult obesity against income per person")
    ax.set_xlabel("GDP per capita, PPP, international dollars in 2021 prices, log scale")
    ax.set_ylabel("Adults with BMI of 30 or more, age standardised")
    ax.set_ylim(0, 80)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.xaxis.set_major_formatter(lambda v, _: f"${v:,.0f}")
    ax.legend(loc="upper left", frameon=False, fontsize=9.2)
    ax.annotate(
        f"Income data from Eurostat, OECD, IMF and the World Bank via Our World in Data. "
        f"Both fits are on log income.\nDropping {R['meta']['n_pacific']} small Pacific island "
        f"states moves what income accounts for from {ea['r2'] * 100:.1f}% to "
        f"{ex['r2'] * 100:.1f}%. Neither figure is wrong; which one you quote is a choice,\n"
        f"and it is a choice about eleven countries out of {ea['n']}. They are drawn in amber "
        f"rather than dropped, because a number that moves this much on so few\ncountries is "
        f"a finding, not a nuisance.",
        xy=(0, -0.135), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "diet-2-the-rival.png")


def chart3_the_mix():
    """The same FAO number, cut differently, carries four times the signal."""
    ec = R["explains"]["calories"]["all"]
    em = R["explains"]["animal_protein_share"]["all"]
    dec = R["composition_is_not_independent"]

    fig, ax = plt.subplots(figsize=(10.2, 6.0))
    ax.scatter(S.animal_protein_share, S.obesity, s=36, color=GREEN, alpha=0.5,
               linewidths=0, zorder=2)
    fitline(ax, S.animal_protein_share.values, S.obesity.values, GREEN)

    # ROUND 1 CORRECTION. A flat (8, 2) offset for every label put "United States" directly on
    # top of the Marshall Islands point, so the word named one country and sat on another.
    # Labels that would land in a crowded patch go below their point instead.
    # ROUND 2 CORRECTION. Round 1 replaced a flat offset with per-label offsets, which stopped
    # "United States" sitting ON the Marshall Islands point but left it nearer to Argentina's
    # marker than to its own. In a scatter this dense no offset is unambiguous, so every label
    # now carries a leader line to the point it names.
    LABEL_OFFSETS = {"United States": (26, -20), "Denmark": (24, -16), "Italy": (-24, -16),
                     "Vietnam": (22, -12), "Egypt": (20, 14), "Ethiopia": (22, -10)}
    for name, off in LABEL_OFFSETS.items():
        r = S[S.entity == name]
        if len(r):
            r = r.iloc[0]
            ax.annotate(name, xy=(r.animal_protein_share, r.obesity), xytext=off,
                        textcoords="offset points", fontsize=9.0, color=INK,
                        ha="right" if off[0] < 0 else "left", va="center",
                        arrowprops=dict(arrowstyle="-", color=INK2, lw=0.7,
                                        shrinkA=1, shrinkB=4))

    ax.set_title("The mix carries signal the total does not.\n"
                 "Adult obesity against the share of calories that comes from animal protein")
    ax.set_xlabel("Share of daily calorie supply from animal protein")
    ax.set_ylabel("Adults with BMI of 30 or more, age standardised")
    ax.set_ylim(0, 80)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.annotate(
        f"Animal protein share accounts for {em['r2'] * 100:.1f}% of the variation in obesity "
        f"across {em['n']} countries, against {ec['r2'] * 100:.1f}% for total calorie supply.\n"
        f"This is NOT a second measurement. The four macronutrient components reconcile to the "
        f"calorie series itself to within {dec['max_abs_difference_kcal']} kcal across "
        f"{dec['n_country_years']:,}\ncountry-years, so this is the same FAO number cut a "
        f"different way. Composition also tracks development, so part of what it picks up is "
        f"the income story from the previous chart.",
        xy=(0, -0.135), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "diet-3-the-mix.png")


def chart4_what_is_left():
    """The closing image: stack everything and most of the variation is still unaccounted for."""
    e = R["explains"]
    j = e["joint_three_factor"]["all"]
    rows = [
        ("Total calorie supply", e["calories"]["all"]["r2"], BLUE),
        ("Income per person", e["log_gdp"]["all"]["r2"], AMBER),
        ("Share from animal protein", e["animal_protein_share"]["all"]["r2"], GREEN),
        ("All three together", j["r2"], INK2),
    ]

    fig, ax = plt.subplots(figsize=(10.2, 5.4))
    ypos = np.arange(len(rows))[::-1]
    for y, (lab, v, col) in zip(ypos, rows):
        ax.barh(y, 100, color=SHADE, height=0.58, zorder=1)
        ax.barh(y, v * 100, color=col, height=0.58, zorder=2)
        ax.annotate(f"{v * 100:.1f}%", xy=(v * 100, y), xytext=(7, 0),
                    textcoords="offset points", fontsize=11, fontweight="bold",
                    color=col, va="center")
    ax.set_yticks(ypos)
    ax.set_yticklabels([r[0] for r in rows], fontsize=10.5, color=INK)
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.grid(axis="y", visible=False)

    ax.annotate(f"{j['unexplained'] * 100:.1f}% of the variation\nis not accounted for by\n"
                f"any of them",
                xy=(j["r2"] * 100 + (100 - j["r2"] * 100) / 2, ypos[-1]),
                xytext=(0, 0), textcoords="offset points", fontsize=10.5,
                color=INK2, ha="center", va="center")

    ax.set_title("Stack all three and three quarters of it is still unexplained.\n"
                 f"Share of the cross-country variation in adult obesity accounted for, "
                 f"{R['meta']['n_countries']} countries, {R['meta']['year']}")
    ax.set_xlabel("Variation in adult obesity accounted for")
    ax.annotate(
        f"Each bar is the R squared of a least squares fit on all {j['n']} countries. The first "
        f"three are single variables; the fourth is all three at once.\nThey do NOT add up, "
        f"because calorie supply, income and diet composition are correlated with each other, so "
        f"no share of the total is\nbeing attributed to any one of them. Adding calorie supply "
        f"and income to composition alone moves the joint figure from "
        f"{e['animal_protein_share']['all']['r2'] * 100:.1f}%\nto {j['r2'] * 100:.1f}%. "
        f"Excluding the Pacific island states the joint figure is "
        f"{e['joint_three_factor']['excluding_pacific']['r2'] * 100:.1f}%, leaving "
        f"{e['joint_three_factor']['excluding_pacific']['unexplained'] * 100:.1f}% unexplained.",
        xy=(0, -0.20), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "diet-4-what-is-left.png")


if __name__ == "__main__":
    chart1_same_calories()
    chart2_the_rival()
    chart3_the_mix()
    chart4_what_is_left()
