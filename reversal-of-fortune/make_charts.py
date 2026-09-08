"""Charts for Post 25, 'the map used to run the other way'.

Reads results.json and the source files. Output: charts/rf-N-name.png.

Every number drawn or written here comes from results.json. Typed literals are limited to axis
limits, layout coordinates, and fixed source labels that describe the data rather than the result.

House rule: no em or en dashes anywhere, including inside rendered images. matplotlib writes a
Unicode minus on negative ticks unless axes.unicode_minus is False.

After editing any caption, RE-OPEN THE PNG and look at it.
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from build_analysis import WB_AGGREGATES

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
R = json.load(open(os.path.join(BASE, "results.json")))

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
    "text.parse_math": False, "axes.unicode_minus": False,
})

C_COL, C_NEV = RED, BLUE          # former colonies, never colonised


def frame():
    gdp = json.load(open(os.path.join(DATA, f"wb_gdp_{R['meta']['gdp_year']}.json")))[1]
    # Round 1 replaced the dead region filter in build_analysis.py and left this copy untouched,
    # so 43 World Bank aggregates (WLD, EUU, OED) sat in this frame and reached no chart only
    # because none of them has an ERA5 temperature. Round 2 caught it. Same list, same assert.
    g = {r["countryiso3code"]: r["value"] for r in gdp
         if r["value"] and r["countryiso3code"] and r["countryiso3code"] not in WB_AGGREGATES}
    assert not (set(g) & WB_AGGREGATES), sorted(set(g) & WB_AGGREGATES)
    tas = {k: list(v.values())[0] for k, v in
           json.load(open(os.path.join(DATA, "cckp_tas.json")))["data"].items() if v}
    t5 = pd.read_stata(os.path.join(DATA, "ajr_t5/maketable5.dta"))
    t5 = t5[t5.shortnam.notna() & t5.shortnam.str.fullmatch(r"[A-Z]{3}")]
    a = t5[["shortnam", "lpd1500s", "ex2col"]].copy()
    # Same de-duplication as build_analysis, filter and sort included: keep the informative row,
    # not the first, or Germany and Zimbabwe are silently deleted. Round 3 found the two loaders
    # had drifted apart, so the method note's claim about both scripts was not true of this step.
    a["_filled"] = a.notna().sum(axis=1)
    a = (a.sort_values("_filled", ascending=False, kind="stable")
          .drop_duplicates("shortnam").drop(columns="_filled"))
    # Universe is the UNION of countries with income and countries in AJR. Round 1 found chart 2's
    # left panel drawing 93 points under an n=96 annotation, because that panel needs only
    # temperature and 1500 density while the frame demanded GDP.
    iso = sorted(set(g) | set(a.shortnam.dropna()))
    d = pd.DataFrame({"iso3": iso}).assign(gdp=lambda x: x.iso3.map(g),
                                           tas=lambda x: x.iso3.map(tas))
    d["lgdp"] = np.log(d.gdp)
    return d.merge(a, left_on="iso3", right_on="shortnam", how="left")


def save(fig, name):
    fig.savefig(os.path.join(BASE, "charts", name), dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def footnote(fig, text, y=-0.02):
    fig.text(0.0, y, text, ha="left", va="top", fontsize=8.6, color=MUTED, wrap=True)


def fitline(ax, x, y, color, exp=False):
    """Fit on the log values, then draw in the axis's own space.

    exp=True when the y-axis is log-scaled but holds RAW values (dollars). Without it the fitted
    line is drawn at log-space heights against a dollar axis and lands flat near the bottom of the
    chart, which is what the first render of charts 1 and 3 did. Caught by opening the PNG.
    """
    b = np.polyfit(x, y, 1)
    gx = np.linspace(min(x), max(x), 50)
    gy = b[0] * gx + b[1]
    ax.plot(gx, np.exp(gy) if exp else gy, color=color, lw=1.6, ls="--", zorder=2)


def chart1(d):
    """The claim, drawn at full strength."""
    s = d.dropna(subset=["tas", "lgdp"])
    t = R["tidy_story"]
    fig, ax = plt.subplots(figsize=(11.0, 6.6))
    ax.set_axisbelow(True)
    ax.scatter(s.tas, s.gdp, s=52, color=MUTED, alpha=0.75, edgecolor=SURFACE, linewidth=0.8, zorder=3)
    fitline(ax, s.tas.values, s.lgdp.values, INK2, exp=True)
    ax.set_yscale("log")
    ax.set_xlabel("Average annual temperature, degrees Celsius, 1991 to 2020")
    ax.set_ylabel("GDP per capita, PPP, log scale")
    ax.set_title("The tidy story, and it is true")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    for iso, lab in (("IDN", "Indonesia"), ("SGP", "Singapore"), ("NOR", "Norway"),
                     ("COD", "DR Congo"), ("QAT", "Qatar"), ("MNG", "Mongolia")):
        r = s[s.iso3 == iso]
        if len(r):
            ax.annotate(lab, (r.tas.iloc[0], r.gdp.iloc[0]), textcoords="offset points",
                        xytext=(7, 5), fontsize=9.4, color=INK2, zorder=4)
    # Bottom LEFT, not top right: at 0.985/0.94 this box overlapped the Singapore and Qatar labels
    # by 90 x 31 px and rendered as broken text. Round 1 caught it by measuring the PNG.
    ax.text(0.015, 0.055, f"r = {t['r']:.2f} on log income   n = {t['n']} countries and territories",
            transform=ax.transAxes, ha="left", fontsize=11.6, color=INK, fontweight="bold")
    footnote(fig,
             f"Temperature: ERA5 reanalysis, near-surface air temperature, 1991 to 2020 annual "
             f"mean, via the World Bank Climate Change Knowledge Portal. Income: World "
             f"Bank, GDP per capita at purchasing power parity, constant international dollars, "
             f"{R['meta']['gdp_year']}. Every entity with both, {t['n']} of them, which includes "
             f"territories such as Aruba, Greenland and Hong Kong SAR alongside sovereign states. "
             f"Both r and the fitted line are computed on LOG income; on raw dollars r is "
             f"{R['tidy_story_raw_dollars']['r']:.2f}. This chart is the claim the post starts "
             f"from. Nothing after it disputes that the relationship is real, but among former "
             f"European colonies the same thermometer ran the OTHER way against the best measure "
             f"of 1500 prosperity we have, population density, so this chart cannot be read as "
             f"heat acting on prosperity in a way that never changed.", y=-0.055)
    save(fig, "rf-1-the-tidy-story.png")


def chart2(d):
    """Temperature's own reversal, and only inside the colonised world."""
    h = R["heat_reversal"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(12.6, 5.4), gridspec_kw={"wspace": 0.26})
    col = d[(d.ex2col == 1)]
    for ax, yv, ylab, ttl, key in (
            (a, "lpd1500s", "Log population density in 1500",
             "In 1500, hotter went with more crowded", "vs_density_1500"),
            (b, "lgdp", "Log GDP per capita today",
             "Today, hotter goes with poorer", "vs_income_2023")):
        s = col.dropna(subset=["tas", yv])
        ax.set_axisbelow(True)
        ax.scatter(s.tas, s[yv], s=48, color=C_COL, alpha=0.7, edgecolor=SURFACE, linewidth=0.8, zorder=3)
        fitline(ax, s.tas.values, s[yv].values, INK2)
        ax.set_xlabel("Average annual temperature, degrees Celsius")
        ax.set_ylabel(ylab)
        ax.set_title(ttl, fontsize=12)
        r = h["former_colonies"][key]
        # Upper left, not lower left: the lower-left corner of the density panel holds Canada, and
        # at (0.03, 0.06) this box sat 5 px from that marker, which is sub-pixel at blog width.
        ax.text(0.03, 0.93, f"r = {r['r']:+.2f}   n = {r['n']}", transform=ax.transAxes,
                va="top", fontsize=11.4, color=INK, fontweight="bold")
    fig.suptitle("The same thermometer, pointing opposite ways five centuries apart",
                 fontsize=14.5, fontweight="bold", x=0.0, ha="left", y=1.04)
    g = h["all"]["vs_density_1500"]
    footnote(fig,
             f"Former European colonies only, using Acemoglu, Johnson and Robinson's own ex-colony "
             f"classification. This is a narrower claim than it looks and the narrowing is "
             f"deliberate: across ALL countries, temperature against 1500 population density is "
             f"{g['r']:+.2f} (n={g['n']}), which is slightly negative. Hot places were not the dense "
             f"places worldwide. The sign flip shown here exists inside the colonised world and "
             f"the post says so rather than generalising it. Population density in 1500 is a proxy "
             f"for prosperity in a period with no income statistics, which is an assumption of the "
             f"method, not a measurement. It is also coarse: {R['density_ties']['largest_tied_block']} "
             f"West African countries share one identical density value here, so some of the dots "
             f"at the hot end are one regional estimate repeated rather than "
             f"{R['density_ties']['largest_tied_block']} independent observations.", y=-0.055)
    save(fig, "rf-2-the-same-heat-in-1500.png")


def chart3(d):
    """The flip: 1500 prosperity against income today, split by colonisation."""
    f = R["flip"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(12.6, 5.4), gridspec_kw={"wspace": 0.26},
                               sharey=True, sharex=True)
    for ax, flag, colr, ttl, key in (
            (a, 1, C_COL, "Places Europeans colonised", "former_colonies"),
            (b, 0, C_NEV, "Places not on AJR's list", "never_colonised")):
        s = d[(d.ex2col == flag)].dropna(subset=["lpd1500s", "lgdp"])
        ax.set_axisbelow(True)
        ax.scatter(s.lpd1500s, s.gdp, s=48, color=colr, alpha=0.72,
                   edgecolor=SURFACE, linewidth=0.8, zorder=3)
        fitline(ax, s.lpd1500s.values, s.lgdp.values, INK2, exp=True)
        ax.set_yscale("log")
        ax.set_xlabel("Log population density in 1500")
        ax.set_title(ttl, fontsize=12)
        r = f[f"density_1500|income_2023|{key}"]
        ax.text(0.03, 0.055, f"r = {r['r']:+.2f}   n = {r['n']}", transform=ax.transAxes,
                fontsize=11.8, color=INK, fontweight="bold")
    a.set_ylabel("GDP per capita, PPP, log scale")
    a.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    fig.suptitle("Being prosperous in 1500 predicts poverty now, but only on one side of the split",
                 fontsize=14.5, fontweight="bold", x=0.0, ha="left", y=1.04)
    al = f["density_1500|income_2023|all"]
    n95 = f["density_1500|income_1995|former_colonies"]
    footnote(fig,
             f"Population density in 1500 from Acemoglu, Johnson and Robinson's replication data, "
             f"against World Bank GDP per capita for {R['meta']['gdp_year']}. Pooled across both "
             f"panels the correlation is {al['r']:+.2f} (n={al['n']}), which is nothing: the "
             f"relationship is invisible until the sample is split, and then it points in opposite "
             f"directions. Their paper used 1995 income and found {n95['r']:+.2f} among former "
             f"colonies; it survives 28 more years of data at {f['density_1500|income_2023|former_colonies']['r']:+.2f}. "
             f"The right-hand group is AJR's residual rather than a list of untouched places, so "
             f"Bermuda, Puerto Rico and Aruba are in it. This post does not claim to know what "
             f"caused the flip.", y=-0.055)
    save(fig, "rf-3-the-flip.png")


def chart4():
    """Who actually reversed. Chosen after seeing the data, unlike charts 1 and 3."""
    ranks = R["ranks"]
    top = ranks[:8]
    bot = list(reversed(ranks[-6:]))
    idn = [r for r in ranks if r["iso3"] == "IDN"]
    NAME = {"BDI": "Burundi", "SDN": "Sudan", "AFG": "Afghanistan", "RWA": "Rwanda",
            "UGA": "Uganda", "ETH": "Ethiopia", "PAK": "Pakistan", "BFA": "Burkina Faso",
            "SGP": "Singapore", "AUS": "Australia", "CAN": "Canada", "HKG": "Hong Kong SAR",
            "USA": "United States", "URY": "Uruguay", "IDN": "Indonesia",
            "GUY": "Guyana", "NZL": "New Zealand", "ARE": "United Arab Emirates",
            "QAT": "Qatar", "BRN": "Brunei", "MYS": "Malaysia",
            "MLI": "Mali", "NER": "Niger", "TCD": "Chad", "SOM": "Somalia"}
    rows = top + idn + bot
    y = np.arange(len(rows))[::-1]
    missing = [r["iso3"] for r in rows if r["iso3"] not in NAME]
    assert not missing, f"chart 4 has no display name for {missing}; add them to NAME"
    fig, ax = plt.subplots(figsize=(11.4, 7.6))
    ax.set_axisbelow(True)
    for yy, r in zip(y, rows):
        c = AMBER if r["iso3"] == "IDN" else (C_COL if r["slide"] > 0 else C_NEV)
        ax.plot([r["density_pct"], r["income_pct"]], [yy, yy], color=c, lw=2.4, alpha=0.55, zorder=2)
        ax.scatter([r["density_pct"]], [yy], s=64, color=c, zorder=3)
        ax.scatter([r["income_pct"]], [yy], s=64, color=c, zorder=3, marker="D")
    ax.set_yticks(y, [NAME[r["iso3"]] for r in rows], fontsize=10)
    ax.grid(axis="y", visible=False)
    ax.set_xlim(-4, 104)
    ax.set_xlabel("Percentile among former European colonies")
    fig.suptitle("Who actually reversed", fontsize=14.5, fontweight="bold",
                 x=0.0, ha="left", y=1.02)
    ax.scatter([], [], s=64, color=MUTED, label="Population density in 1500")
    ax.scatter([], [], s=64, color=MUTED, marker="D", label="Income today")
    # Above the plot, not inside it: at "lower center" the legend lay across the bottom data row
    # and its swatches were the same shape and size as real markers, so that country appeared to
    # have four data points. Round 1 measured 731 px of overlap. Visible only in the rendered PNG.
    # (Round 1's note named Uruguay. Round 2 thought Guyana and Uruguay tied exactly and broke the
    # tie on income; round 3 found they differ by one unit in the last place, so that tie-break
    # never fired and the row order rested on float residue. build_analysis.py now rounds the slide
    # and breaks ties on income then alphabetically. Five such pairs existed, not one.)
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 1.005), frameon=False, fontsize=10, ncol=2)
    i = idn[0] if idn else None
    footnote(fig,
             f"Former European colonies only, {len(ranks)} with both measures. Circles are the "
             f"percentile by population density in 1500, diamonds the percentile by GDP per capita "
             f"today. Red slid down, blue climbed. Indonesia in amber, at the "
             f"{i['density_pct']:.0f}th percentile then and the {i['income_pct']:.0f}th now, a "
             f"{i['slide']:.0f} point slide that ranks it "
             f"{[r['iso3'] for r in ranks].index('IDN') + 1}th of {len(ranks)}: the middle of the "
             f"distribution rather than a case study. This chart was chosen after the "
             f"correlations were computed, unlike the first and third, and the method notes say so.",
             y=-0.038)
    save(fig, "rf-4-who-actually-reversed.png")


if __name__ == "__main__":
    d = frame()
    chart1(d), chart2(d), chart3(d), chart4()
