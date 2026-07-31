"""Charts for Post 18 'A Quarter of the Median County's Income Is a Transfer.'

Reads results.json. Output: charts/income-N-name.png.
Every figure that comes out of the data is interpolated from results.json rather than typed. The only
typed numbers are chosen thresholds (the 40% line in chart 3) and layout coordinates. That guarantee
used to be stated more broadly than it was true: chart 3's footnote carried a hardcoded sentence that
survived a round of corrections everywhere else, so the claim of full interpolation was itself what
hid the stale text. Every series stops at 2022, because CAINC35 does.

Everything plotted is a SHARE of personal income, so nominal dollars cancel and no deflator is
needed. That is the reason this post can run 1969 to 2022 without a price index.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())
CUT = R["traps"]["cut_year"]

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


def chart1_long_arc():
    """The scale of the thing, and that it happened to the whole distribution.

    The band is the middle half of counties, so the reader can see this is not a story about a tail.
    """
    d = pd.DataFrame(R["by_year"])
    fig, ax = plt.subplots(figsize=(10.0, 5.7))

    ax.fill_between(d.year, d.county_p25, d.county_p75, color=BLUE, alpha=0.18,
                    label="middle half of counties")
    ax.plot(d.year, d.county_median, color=BLUE, lw=2.6, label="median county")
    ax.plot(d.year, d.us_pct, color=INK, lw=2.2, ls=(0, (5, 2)), label="United States as a whole")

    a, b = d.iloc[0], d.iloc[-1]
    for s, col, off in ((a.county_median, BLUE, 10), (a.us_pct, INK, -16)):
        ax.annotate(f"{s:.1f}%", (a.year, s), xytext=(4, off), textcoords="offset points",
                    fontsize=10, color=col, fontweight="bold")
    ax.annotate(f"{b.county_median:.1f}%", (b.year, b.county_median), xytext=(6, 0),
                textcoords="offset points", fontsize=11, color=BLUE, fontweight="bold", va="center")
    ax.annotate(f"{b.us_pct:.1f}%", (b.year, b.us_pct), xytext=(6, 0),
                textcoords="offset points", fontsize=11, color=INK, fontweight="bold", va="center")

    peak = d.loc[d.county_median.idxmax()]
    ax.annotate(f"{peak.county_median:.1f}% in {int(peak.year)},\nthe pandemic years",
                xy=(peak.year, peak.county_median), xytext=(2002, 33.2), textcoords="data",
                fontsize=9.4, color=INK2, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

    ax.set_title("In the median American county, transfers went from a tenth of\n"
                 "personal income in 1969 to more than a quarter")
    ax.set_ylabel("Transfers, share of personal income")
    ax.set_xlim(d.year.min(), d.year.max() + 1)
    ax.set_ylim(0, 42)
    ax.yaxis.set_major_formatter(lambda v, p: f"{v:.0f}%")
    ax.legend(loc="upper left", frameon=False, fontsize=9.6)
    ax.annotate(
        f"BEA CAINC1 and CAINC35, {int(a.year)} to {CUT}. Transfers are personal current transfer "
        f"receipts. Every figure is a share of personal income, so nominal dollars cancel and no "
        f"price index is\nneeded. The series stops at {CUT} because the transfer table does; the "
        f"income table runs to {R['traps']['cainc1_last_year']}. Counties per year: "
        f"{d.n_counties.iloc[-1]:,}.",
        xy=(0, -0.135), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "income-1-the-long-arc.png")


def chart2_cash_or_on_behalf():
    """The hook. The same total, split by who actually receives the money.

    Medical benefits are paid to providers on a person's behalf and counted as that person's income.
    Most of the rest arrives as cash the person can spend, but not all of it: about 13% of the
    residual is SNAP, education and training assistance, and receipts of nonprofit institutions, so
    the green band is labelled "paid to the person" rather than "cash".
    """
    d = pd.DataFrame(R["by_year"])
    fig, ax = plt.subplots(figsize=(10.0, 5.7))

    ax.fill_between(d.year, 0, d.us_cash_pct, color=GREEN, alpha=0.55,
                    label="paid to the person, mostly as cash")
    ax.fill_between(d.year, d.us_cash_pct, d.us_cash_pct + d.us_medical_pct, color=RED, alpha=0.55,
                    label="paid to providers on the person's behalf (medical)")
    ax.plot(d.year, d.us_cash_pct + d.us_medical_pct, color=INK, lw=1.6)

    a, b = d.iloc[0], d.iloc[-1]
    ax.annotate(f"medical\n{a.us_medical_pct:.1f}%", (a.year + 1, a.us_cash_pct + a.us_medical_pct / 2),
                fontsize=9.4, color=RED, fontweight="bold", va="center")
    ax.annotate(f"{b.us_medical_pct:.1f}%", (b.year, b.us_cash_pct + b.us_medical_pct / 2),
                xytext=(7, 0), textcoords="offset points", fontsize=11, color=RED,
                fontweight="bold", va="center")
    ax.annotate(f"{b.us_cash_pct:.1f}%", (b.year, b.us_cash_pct / 2), xytext=(7, 0),
                textcoords="offset points", fontsize=11, color=GREEN, fontweight="bold", va="center")

    g = R["growth_split"]
    ax.annotate(
        f"Of the {g['total_change_pts']:.1f} point rise in transfers since {int(a.year)},\n"
        f"{g['medical_change_pts']:.1f} points is medical: {g['medical_share_of_growth_pct']:.0f}% of the whole increase",
        xy=(2006, 11.0), xytext=(1972, 16.4), textcoords="data", fontsize=9.5, color=INK2, ha="left",
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

    ax.set_title("Nearly half of American transfers are now paid to a provider, not to a person")
    ax.set_ylabel("Share of US personal income")
    ax.set_xlim(a.year, b.year)
    ax.set_ylim(0, 24)
    ax.yaxis.set_major_formatter(lambda v, p: f"{v:.0f}%")
    ax.legend(loc="upper left", frameon=False, fontsize=9.6)
    ax.annotate(
        f"Medical benefits are Medicare, Medicaid and military medical insurance. BEA's methodology "
        f"describes all three as payments to vendors for care\nprovided. They sum to the medical "
        f"total exactly (maximum absolute "
        f"error {R['medical_partition_max_abs_error']:.1f}), so this is a partition of transfers "
        f"rather than an overlap. Medical was {a.us_medical_share_of_transfers:.1f}% of all transfers "
        f"in {int(a.year)}\nand {b.us_medical_share_of_transfers:.1f}% in {CUT}. The bulge in 2020 "
        f"and 2021 is pandemic cash: unemployment insurance and refundable tax credits.",
        xy=(0, -0.135), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "income-2-cash-or-on-behalf.png")


def chart3_everywhere():
    """Not a story about a tail. The whole distribution moved."""
    dist = R["distribution"]
    a, b = dist["1969"], dist[str(CUT)]
    fig, ax = plt.subplots(figsize=(10.0, 5.4))
    bins = np.arange(0, 66, 1.5)
    ax.hist(a["values"], bins=bins, color=MUTED, alpha=0.75, label=f"1969  ({a['n']:,} counties)")
    ax.hist(b["values"], bins=bins, color=BLUE, alpha=0.70, label=f"{CUT}  ({b['n']:,} counties)")

    for snap, col, lab in ((a, MUTED, "1969"), (b, BLUE, str(CUT))):
        ax.axvline(snap["median"], color=col, lw=1.8, ls=(0, (4, 3)))
        ax.annotate(f"median {snap['median']:.1f}%", xy=(snap["median"], ax.get_ylim()[1] * 0.93),
                    xytext=(5, 0), textcoords="offset points", fontsize=9.6, color=col,
                    fontweight="bold")

    ax.axvline(40, color=RED, lw=1.2, ls=(0, (2, 3)))
    ax.annotate(f"above 40%:\n{a['n_above_40']} counties in 1969\n{b['n_above_40']} in {CUT}",
                xy=(40, ax.get_ylim()[1] * 0.46), xytext=(46, ax.get_ylim()[1] * 0.52),
                textcoords="data", fontsize=9.4, color=RED, ha="left",
                arrowprops=dict(arrowstyle="->", color=RED, lw=0.9))

    ov = R["overlap"]
    ax.axvline(ov["max_1969"], color=INK, lw=1.1, ls=(0, (5, 3)))
    ax.annotate(f"the highest county in 1969 was {ov['max_1969']:.1f}%.\n"
                f"{ov['share_of_cut_counties_above_1969_max']:.0f}% of counties are above that line in {CUT}",
                xy=(ov["max_1969"], ax.get_ylim()[1] * 0.30), xytext=(43.0, ax.get_ylim()[1] * 0.28),
                textcoords="data", fontsize=9.3, color=INK2, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
    ax.set_title("The whole distribution moved right and pulled apart.\n"
                 "This is not a story about a handful of poor counties")
    ax.set_xlabel("Transfers as a share of the county's personal income")
    ax.set_ylabel("Counties")
    ax.set_xlim(0, 66)
    ax.xaxis.set_major_formatter(lambda v, p: f"{v:.0f}%")
    ax.legend(loc="upper right", frameon=False, fontsize=9.8)
    ax.annotate(
        f"Every county with both figures in the year shown. The 1969 distribution runs from "
        f"{a['p10']:.1f}% at the 10th percentile to {a['p90']:.1f}% at the 90th, with a maximum of "
        f"{a['max']:.1f}%.\nBy {CUT} those are {b['p10']:.1f}%, {b['p90']:.1f}% and {b['max']:.1f}%. "
        f"The distribution moved right and pulled apart rather than a tail growing: the middle half "
        f"widened from {R['dispersion']['iqr_1969']:.1f} to {R['dispersion']['iqr_cut']:.1f} points.",
        xy=(0, -0.155), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "income-3-everywhere.png")


def chart4_same_number():
    """The close, as a picture. Two counties can match on the total and differ on everything else.

    The amber line is the contour on which the total is constant, so Queens and Saluda sitting on
    opposite sides of the diagonal while both lying on the amber line IS the argument. Labels are
    placed in data coordinates because the point cloud leaves only a few genuinely empty regions.
    """
    t = pd.DataFrame(R["scatter"])
    fig, ax = plt.subplots(figsize=(10.2, 6.6))
    above = t.medical_pct > t.cash_pct
    ax.scatter(t.loc[~above, "cash_pct"], t.loc[~above, "medical_pct"], s=9, color=BLUE,
               alpha=0.28, linewidths=0, label="cash exceeds medical")
    ax.scatter(t.loc[above, "cash_pct"], t.loc[above, "medical_pct"], s=9, color=RED,
               alpha=0.40, linewidths=0,
               label=f"medical exceeds cash  ({int(above.sum())} counties)")

    lim = 46
    tot = R["close_pair"]["queens"]["transfer_pct"]
    ax.plot([0, tot], [tot, 0], color=AMBER, lw=1.8, zorder=4)
    ax.plot([0, lim], [0, lim], color=INK, lw=1.1, ls=(0, (4, 3)), zorder=3)
    ax.annotate("equal split", xy=(lim * 0.82, lim * 0.82), xytext=(-4, 8),
                textcoords="offset points", fontsize=9.2, color=INK2, ha="right", rotation=45)
    ax.annotate(f"every county on this line draws\n{tot:.1f}% of its income from transfers",
                xy=(6.0, tot - 6.0), xytext=(1.2, 34.0), textcoords="data",
                fontsize=9.3, color="#a06e00", ha="left",
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.1))

    pair = R["close_pair"]
    top = R["county_cut"]["top_medical"][0]
    marks = [
        (pair["queens"], (1.0, 25.2), "left"),
        (pair["saluda"], (27.5, 13.0), "left"),
        ({"name": top["name"], "cash_pct": top["cash_pct"], "medical_pct": top["medical_pct"],
          "transfer_pct": top["transfer_pct"]}, (24.5, 43.0), "left"),
    ]
    for c, xy_text, ha in marks:
        ax.scatter([c["cash_pct"]], [c["medical_pct"]], s=70, facecolor="none",
                   edgecolor=INK, linewidths=1.7, zorder=6)
        ax.annotate(f"{c['name']}\n{c['transfer_pct']:.1f}% total, {c['medical_pct']:.1f}% medical",
                    xy=(c["cash_pct"], c["medical_pct"]), xytext=xy_text, textcoords="data",
                    fontsize=9.4, color=INK, fontweight="bold", ha=ha, zorder=7,
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=1.0))

    ax.set_title("Two counties can report the same share of income from transfers\n"
                 "and mean entirely different things by it")
    ax.set_xlabel("Cash transfers, share of personal income")
    ax.set_ylabel("Medical transfers paid on residents' behalf,\nshare of personal income")
    ax.set_xlim(0, lim); ax.set_ylim(0, lim)
    ax.xaxis.set_major_formatter(lambda v, p: f"{v:.0f}%")
    ax.yaxis.set_major_formatter(lambda v, p: f"{v:.0f}%")
    ax.set_aspect("equal")
    ax.legend(loc="lower right", frameon=False, fontsize=9.5, borderaxespad=1.4, markerscale=3.2)
    q, s = pair["queens"], pair["saluda"]
    ax.annotate(
        f"Every county in {CUT} ({len(t):,} of them). {q['name']} and {s['name']} both draw about "
        f"{q['transfer_pct']:.1f}% of personal income from transfers, but medical is "
        f"{q['medical_of_transfers']:.1f}% of that in {q['name'].split(',')[0]}\nand "
        f"{s['medical_of_transfers']:.1f}% in {s['name'].split(',')[0]}. Anything that ranks places "
        f"on income alone treats those two as the same result.",
        xy=(0, -0.125), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "income-4-same-number.png")


if __name__ == "__main__":
    (BASE / "charts").mkdir(exist_ok=True)
    chart1_long_arc()
    chart2_cash_or_on_behalf()
    chart3_everywhere()
    chart4_same_number()
