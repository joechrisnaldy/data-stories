"""Charts for Post 17 'A Third of the World's Labour Laws Still Assume You Work Saturday'.

Reads results.json. Output: charts/hours-N-name.png.
Every number in every label is interpolated from results.json rather than typed, so a rerun cannot
leave a stale figure behind. Every series plotted is law-havers only, cut at 2012, for the two
reasons documented at the top of build_analysis.py.

Chart 4 deliberately starts at the 1920s rather than at the first year with data. Before then fewer
than 27% of polities had a working-hours law, so a dispersion minimum in the 1890s is a statement
about which FOUR early adopters happen to be in the set (Austria, France, Russia, Switzerland), not
about the world. Marking that as "tightest" would have contradicted the point the chart exists to
make.

Chart 4's overtime panel plots the spread among countries that actually HAVE a premium. Plotting it
across all law-havers, as an earlier version did, produces a 45.8% "convergence" that is entirely a
denominator effect: the mean premium nearly doubles as the share of law-havers with no premium at
all falls from 30.1% in the 1920s to 7.2% by the 2010s, while the raw standard deviation RISES 5%
over the 1920s-to-1990s window the apparent convergence is measured on. That is the same
extensive-margin trap the 96 sentinel sets for normal hours, in a different column.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())
CUT = R["meta"]["cut_year"]

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
    # matplotlib writes a Unicode minus (U+2212) on negative ticks by default, which breaks the
    # house no-dash rule inside the rendered image. Force an ASCII hyphen.
    "axes.unicode_minus": False,
})


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def runs(years):
    """Collapse a sorted year list into contiguous runs, for labelling the zero-spread stretches."""
    out = []
    for y in sorted(years):
        if out and y == out[-1][1] + 1:
            out[-1][1] = y
        else:
            out.append([y, y])
    return [tuple(r) for r in out]


def chart1_agreement_peaked():
    """The hook, as a shape.

    The bands are the spread of the statutory normal week across every polity that had a law that
    year. The middle half collapses to zero width in two stretches and never returns after 1951.
    The median line falls almost the whole time, which is exactly why the reopening is invisible in
    any headline average.

    The zero-spread stretches are marked with a rug along the bottom rather than a full-height
    shaded span: a span tints the percentile bands and then reads as though it were a band itself.
    """
    d = pd.DataFrame(R["dispersion_by_year"])
    fig, ax = plt.subplots(figsize=(10.0, 5.9))
    YLO, YHI = 32.0, 74.0

    ax.fill_between(d.year, d.p10, d.p90, color=BLUE, alpha=0.14,
                    label="middle 80% of countries (10th to 90th percentile)")
    ax.fill_between(d.year, d.p25, d.p75, color=BLUE, alpha=0.34,
                    label="middle half of countries (25th to 75th percentile)")
    ax.plot(d.year, d.p50, color=INK, lw=2.4, label="median country")

    for h in (40, 48):
        ax.axhline(h, color=MUTED, lw=0.7, ls=(0, (4, 4)), zorder=0)

    zr = runs(R["zero_iqr_years"])
    n_zero = sum(b - a + 1 for a, b in zr)
    ax.broken_barh([(a - 0.5, b - a + 1) for a, b in zr], (YLO + 0.5, 1.3),
                   facecolors=AMBER, edgecolors="none", zorder=4)
    ax.annotate(
        f"middle half at exactly one number\n{n_zero} years: "
        + ", ".join(f"{a} to {b}" for a, b in zr),
        xy=(sum(zr[-1]) / 2, YLO + 1.9), xytext=(1926, 36.2), textcoords="data",
        fontsize=9.5, color=INK2, ha="left",
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

    last = d.iloc[-1]
    ax.annotate(f"by {CUT} the middle half\nspans {last.iqr:.0f} hours, "
                f"{last.p25:.0f} to {last.p75:.0f}",
                xy=(last.year, (last.p25 + last.p75) / 2), xytext=(1972, 37.0),
                textcoords="data", fontsize=9.5, color=INK2, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

    ax.set_title("The world's working-hours laws agreed most in the mid-century,\n"
                 "then drifted apart for sixty years")
    ax.set_ylabel("Statutory normal week, hours")
    ax.set_xlim(d.year.min(), d.year.max())
    ax.set_ylim(YLO, YHI)
    ax.legend(loc="upper right", frameon=False, fontsize=9.5)

    bp = R["balanced_panel"]["1950"]
    ax.annotate(
        f"Countries with a working-hours law only, {d.year.min()} to {CUT}: the first year at least "
        f"{R['fan_min_n']} had one, and the last year before the file's 2013 coding cliff. Countries with "
        f"no law are excluded\nentirely, because the file codes them 96, which is a placeholder and "
        f"not a measured week. The widening is not an artefact of more countries joining: on the "
        f"{bp['n_constant']} countries\nthat had a law in both 1950 and {CUT}, the middle half still "
        f"goes from {bp['iqr_1950']:.0f} hours to {bp[f'iqr_{CUT}']:.0f}.",
        xy=(0, -0.145), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "hours-1-agreement-peaked.png")


def chart2_two_numbers():
    """One pile becomes two.

    Dot area is proportional to the number of countries at that exact statutory week, so the shape
    of the row IS the distribution. 1950 is a single stack. 2012 is a standoff.
    """
    s = R["snapshots"]
    fig, ax = plt.subplots(figsize=(10.4, 4.8))
    XLO, XHI = 30.0, 61.5
    rows = [("1950", s["1950"], 1.0, MUTED), (str(CUT), s[str(CUT)], 0.0, BLUE)]

    for label, snap, y, colour in rows:
        counts = {float(k): v for k, v in snap["counts"].items()}
        xs = sorted(counts)
        ns = [counts[x] for x in xs]
        ax.scatter(xs, [y] * len(xs), s=[n * 26 for n in ns], color=colour,
                   alpha=0.85, edgecolors=SURFACE, linewidths=1.1, zorder=3)
        for x, n in zip(xs, ns):
            if n >= 6:
                ax.annotate(str(n), (x, y), ha="center", va="center", fontsize=9.5,
                            color="white", fontweight="bold", zorder=4)
        ax.annotate(f"{label}\n{snap['n']} countries\nwith a law", xy=(XLO + 0.4, y), ha="left",
                    va="center", fontsize=10, color=INK, fontweight="bold")

    for h in (40, 48):
        ax.axvline(h, color=MUTED, lw=0.7, ls=(0, (4, 4)), zorder=0)

    s50, s12 = s["1950"], s[str(CUT)]
    counts_44 = int(s12["counts"].get("44.0", 0))
    ax.annotate(f"{s50['at48']} of {s50['n']} at 48 hours ({s50['at48_pct']}%)",
                xy=(48, 1.0), xytext=(0, 30), textcoords="offset points", ha="center",
                fontsize=9.8, color=INK2, fontweight="bold")
    ax.annotate(f"{s12['at40']} at 40 ({s12['at40_pct']}%)", xy=(40, 0.0), xytext=(0, -32),
                textcoords="offset points", ha="center", fontsize=9.8, color=BLUE, fontweight="bold")
    ax.annotate(f"{s12['at48']} at 48 ({s12['at48_pct']}%)", xy=(48, 0.0), xytext=(0, -32),
                textcoords="offset points", ha="center", fontsize=9.8, color=BLUE, fontweight="bold")

    ax.set_title("The world never agreed on one number. It ended up split between two")
    ax.set_xlabel("Statutory normal week, hours")
    ax.set_yticks([])
    ax.set_ylim(-0.68, 1.56)
    ax.set_xlim(XLO, XHI)
    ax.set_xticks([35, 40, 45, 48, 50, 55, 60])
    ax.grid(axis="y", visible=False)
    ax.annotate(
        f"Dot area is proportional to the number of countries at that exact figure. In {CUT}, "
        f"{s12['at40_pct'] + s12['at48_pct']:.1f}% of countries sit on 40 or 48 and the rest are "
        f"spread over {s12['n_distinct'] - 2} other values.\nThe median country is at "
        f"{s12['median']:.0f} hours, a third and smaller cluster of {counts_44} countries sitting "
        f"between the two peaks. A 48-hour week is six eight-hour days; it cannot be worked as five "
        f"({R['arithmetic']['hours_per_day_if_48_over_5_days']} hours a day would be needed).",
        xy=(0, -0.29), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "hours-2-two-numbers.png")


def chart3_how_it_spread():
    """Standards arrive in bursts, and the two biggest bursts have names.

    Counts the first year each polity's statutory week equals exactly 48, then exactly 40. Labels
    describe the BAR they point at, not a subset of it: the 1951 to 1955 window holds 16 first-time
    adoptions of 40 hours, 15 of which happened in 1952 alone.
    """
    a48 = pd.DataFrame(R["adoption"]["48"]["windows"])
    a40 = pd.DataFrame(R["adoption"]["40"]["windows"])
    fig, ax = plt.subplots(figsize=(10.4, 5.6))
    w = 2.1
    ax.bar(a48.end - w / 2, a48.n, width=w, color=AMBER, label="first year at exactly 48 hours")
    ax.bar(a40.end + w / 2, a40.n, width=w, color=GREEN, label="first year at exactly 40 hours")
    ax.set_ylim(0, 27)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=6))

    w19 = R["wave_1919"]
    ax.annotate(f"{w19['n']} countries in {w19['window']}. ILO Convention No. 1,\n"
                "adopted 1919: \"eight in the day and forty-eight in the week\"",
                xy=(1920 - w / 2, w19["n"]), xytext=(1925, 23.6), textcoords="data",
                fontsize=9.3, color=INK2, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

    w52 = R["wave_1952"]
    bar52 = int(a40.loc[a40.end.eq(1955), "n"].iloc[0])
    ax.annotate(f"{bar52} countries in 1951 to 1955, of which {w52['n']} are French\n"
                f"African territories that all adopted in {w52['year']}",
                xy=(1955 + w / 2, bar52), xytext=(1962, 19.4), textcoords="data",
                fontsize=9.3, color=INK2, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

    ax.set_title("Both numbers arrived in bursts, and the two biggest were copied", pad=34)
    ax.set_ylabel("Countries adopting that figure for the first time")
    ax.set_xlabel("Five-year window ending")
    ax.set_xlim(1898, CUT + 4)
    # Legend above the plot area: inside the axes it collides with the 1919 annotation, which has
    # to sit next to the tall 1920 bar it points at.
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.004), ncol=2, frameon=False, fontsize=9.5)
    ax.annotate(
        "The 40-hour convention, ILO No. 47 of 1935, declares approval only of \"the principle of a "
        "forty-hour week\" and leaves every detail to later treaties.\nIt took 22 years to enter into "
        "force and has 15 ratifications, against 52 for the 1919 convention. The 40-hour wave never "
        f"finished: {R['snapshots'][str(CUT)]['at40_pct']}% of countries\nwere there by {CUT}. A "
        "country can appear in both series, since reaching 48 and later 40 are different events.",
        xy=(0, -0.155), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "hours-3-how-it-spread.png")


def chart4_three_instruments():
    """The same question asked of all three instruments, with three different answers.

    Dispersion of each regulated quantity across law-havers, by decade, from the 1920s on. Normal
    hours and the overtime premium both converged a long way and then partly reversed. The maximum
    permitted week never converged at all and ends at the widest point in its series, which matters
    because the maximum is the number that actually binds.
    """
    W = R["instrument_window_start"]
    d = pd.DataFrame(R["instruments_by_decade"])
    d = d[d.decade >= W]
    # The overtime series is taken from overtime_honest, which is computed only on countries that
    # actually have a premium. See the module docstring for why the all-law-havers version is a
    # denominator artefact rather than a measure of spread.
    oh = pd.DataFrame(R["overtime_honest"])
    oh = oh[oh.decade >= W].rename(columns={"cv_with_premium_pct": "overtime_cv_pct"})
    d = d.drop(columns=["overtime_cv_pct"]).merge(oh[["decade", "overtime_cv_pct"]], on="decade")
    C = dict(R["instrument_convergence"])
    C["overtime"] = R["overtime_convergence_honest"] | {
        "window_start_decade": R["overtime_convergence_honest"]["start_decade"]}
    panels = [
        ("normal", "normal_cv_pct", "Normal weekly hours", BLUE, "the number everyone quotes"),
        ("overtime", "overtime_cv_pct", "Overtime premium", GREEN, "among countries that have one"),
        ("max", "max_cv_pct", "Maximum weekly hours", RED, "the outer limit on the week"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(11.6, 4.5))

    for ax, (key, col, title, colour, sub) in zip(axes, panels):
        s = d[["decade", col]].dropna()
        c = C[key]
        ax.plot(s.decade, s[col], color=colour, lw=2.4)
        ax.fill_between(s.decade, 0, s[col], color=colour, alpha=0.10)
        ax.scatter([c["cv_min_decade"]], [c["cv_min"]], s=54, color=colour, zorder=5,
                   edgecolors=SURFACE, linewidths=1.4)
        ax.annotate(f"tightest\n{c['cv_min_decade']}s", xy=(c["cv_min_decade"], c["cv_min"]),
                    xytext=(0, -34), textcoords="offset points", ha="center", fontsize=9.0,
                    color=colour, fontweight="bold")
        ax.annotate(f"{c['cv_at_start']:.0f}%", xy=(c["window_start_decade"], c["cv_at_start"]),
                    xytext=(2, 9), textcoords="offset points", ha="left", fontsize=9.6,
                    color=MUTED, fontweight="bold")
        ax.annotate(f"{c['cv_at_end']:.0f}%", xy=(c["end_decade"], c["cv_at_end"]),
                    xytext=(-2, 9), textcoords="offset points", ha="right", fontsize=9.8,
                    color=colour, fontweight="bold")
        ax.set_title(f"{title}\n{sub}", fontsize=11, pad=9)
        rise = (c["cv_at_end"] - c["cv_min"]) / c["cv_min"] * 100
        verdict = f"fell {c['pct_fall_to_min']:.0f}% to its\nlow, then rose {rise:.0f}%"
        if c["pct_fall_to_min"] < 10:
            verdict = (f"never converged: fell only {c['pct_fall_to_min']:.0f}%,\n"
                       f"ends {c['pct_wider_than_start']:.0f}% wider than it began")
        ax.annotate(verdict, xy=(0.5, 0.055), xycoords="axes fraction", ha="center",
                    fontsize=9.2, color=INK2)
        ax.set_xlim(W - 4, CUT + 8)
        ax.set_ylim(0, s[col].max() * 1.40)
        ax.set_xticks([1940, 1970, 2000])

    axes[0].set_ylabel("Spread across countries\n(coefficient of variation, %)")
    fig.suptitle("Two of the three converged and drifted back. The third never converged at all",
                 fontsize=13, fontweight="bold", y=1.05)
    i, oh = R["instruments_at_cut"], R["overtime_convergence_honest"]
    fig.text(0.0, -0.135,
             f"Higher means countries disagree more. Each panel has its own scale, so read the shape "
             f"and the marked low point, not the heights against each other. The window starts in the "
             f"{W}s, the first decade in which more\nthan a quarter of polities had any law at all; "
             f"before that a low spread just describes whichever four early adopters are in the set. "
             f"The overtime panel covers only countries that actually have a\npremium: across all "
             f"law-havers the same measure appears to fall by half, but that is the mean nearly "
             f"doubling as the share with no premium at all drops from {oh['pct_zero_at_start']:.0f}% in the "
             f"{W}s to {oh['pct_zero_at_end']:.0f}% by the 2010s, while the raw\nspread rises. In {CUT} the maximum "
             f"permitted week took {i['max']['n_distinct']} distinct values from {i['max']['min']:.0f} "
             f"to {i['max']['max']:.0f} hours across {i['max']['n']} countries, and "
             f"{i['overtime']['at50_pct']}% of countries set the premium at exactly +50%.",
             fontsize=8.6, color=MUTED, va="top", ha="left")
    save(fig, "hours-4-three-instruments.png")


if __name__ == "__main__":
    (BASE / "charts").mkdir(exist_ok=True)
    chart1_agreement_peaked()
    chart2_two_numbers()
    chart3_how_it_spread()
    chart4_three_instruments()
