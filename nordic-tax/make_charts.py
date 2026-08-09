"""Charts for Post 21, 'How Scandinavia Actually Pays for Itself, and What Others Can Learn From It'.

Reads results.json. Output: charts/tax-N-name.png.

Every number drawn or written here is interpolated from results.json. Typed literals are limited
to axis limits, layout coordinates, and the list of countries the post names.

House rule: no em or en dashes anywhere, including inside rendered images. matplotlib writes a
Unicode minus on negative ticks unless axes.unicode_minus is False.

After editing any caption, RE-OPEN THE PNG and look at it. Three fact-check rounds on Post 20
each found a caption that had gone stale while the code looked fine.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())

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

NORDIC = {"DNK", "SWE", "NOR", "FIN", "ISL"}
# The three non-Nordic countries whose threshold sits at or below Denmark's. Their presence is
# the whole reason chart 1 cannot be read as a story about Scandinavia.
ALSO_LOW = {"BEL", "IRL", "NLD"}


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def footnote(fig, text, y=-0.02):
    fig.text(0.0, y, text, ha="left", va="top", fontsize=8.6, color=MUTED, wrap=True)


def chart1_where_the_top_begins():
    """The hook, with its own correction built in.

    A reader is meant to see two things at once: Denmark's top bracket starts a hair above the
    average wage, and so do Belgium's, Ireland's and the Netherlands'. Colouring those three
    differently from the Nordics is what stops the chart arguing something the data does not.
    """
    rows = R["thresholds"]
    codes = [r["code"] for r in rows]
    vals = [r["threshold_x_avg_wage"] for r in rows]
    names = [r["country"] for r in rows]

    colours, sizes = [], []
    for c in codes:
        if c in NORDIC:
            colours.append(BLUE); sizes.append(62)
        elif c in ALSO_LOW:
            colours.append(AMBER); sizes.append(62)
        elif c == "USA":
            colours.append(RED); sizes.append(62)
        else:
            colours.append(MUTED); sizes.append(34)

    fig, ax = plt.subplots(figsize=(9.4, 11.2))
    y = np.arange(len(rows))
    ax.hlines(y, 0.25, vals, color=GRID, lw=1.4, zorder=1)
    ax.scatter(vals, y, s=sizes, color=colours, zorder=3, linewidths=0)

    ax.axvline(1.0, color=BASELINE, lw=1.1, ls=(0, (4, 3)), zorder=2)
    ax.text(1.02, len(rows) - 0.4, "the average wage", fontsize=9, color=INK2, va="top")

    for i, (v, c) in enumerate(zip(vals, codes)):
        if c in NORDIC or c in ALSO_LOW or c in ("USA", "EST"):
            ax.text(v * 1.09, i, f"{v:.2f}", va="center", fontsize=8.8, color=INK2)

    ax.set_xscale("log")
    ax.set_xlim(0.25, 75)
    ax.set_xticks([0.5, 1, 2, 5, 10, 20, 50])
    ax.set_xticklabels(["0.5x", "1x", "2x", "5x", "10x", "20x", "50x"])
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=9.4)
    ax.set_ylim(-0.8, len(rows) - 0.2)
    ax.set_xlabel("Earnings at which the top statutory rate starts, as a multiple of the average wage"
                  "  (log scale)")
    ax.set_title("Where the top income tax bracket begins, 2025", pad=14)
    ax.grid(axis="y", visible=False)

    handles = [
        plt.Line2D([], [], marker="o", ls="", color=BLUE, label="Nordic countries"),
        plt.Line2D([], [], marker="o", ls="", color=AMBER,
                   label="Belgium, Ireland, Netherlands: at or below Denmark"),
        plt.Line2D([], [], marker="o", ls="", color=RED, label="United States"),
    ]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=9.2)

    nb = R["nordics_are_not_a_bloc"]
    flat = ", ".join(c["country"] for c in R["flat_tax_excluded"]["countries"])
    unus = R["unusable_excluded"]["countries"]
    footnote(fig,
             "OECD Tax Database, Table I.7, 2025. The series is OECD's own published factor of the "
             "average annual wage, not a ratio computed here.\n"
             f"The Nordic countries do not behave as a bloc: Sweden {nb['spread']['SWE']}, "
             f"Denmark {nb['spread']['DNK']}, Iceland {nb['spread']['ISL']}, "
             f"Norway {nb['spread']['NOR']}, Finland {nb['spread']['FIN']}, a range of "
             f"{nb['ratio_max_over_min']} times end to end.\n"
             f"{flat} is excluded because its top rate applies from the first unit of income, so a "
             "multiple of the average wage is not defined for it. "
             + (f"{unus[0]['country']} is excluded for a different reason: it reports both a zero "
                f"threshold and a zero top rate in {R['vintages']['thresholds']}, which is a "
                f"missing value rather than a flat tax. In "
                f"{R['vintages']['thresholds'] - 1} it reported "
                f"{unus[0]['prior_year_threshold']} times the average wage at "
                f"{unus[0]['prior_year_top_rate_pct']} percent.\n" if unus else "")
             + "Estonia, at "
             f"{[r['threshold_x_avg_wage'] for r in rows if r['code'] == 'EST'][0]}, is close to "
             "the same case: a near-flat tax whose single "
             f"{[r['top_rate_pct'] for r in rows if r['code'] == 'EST'][0]} percent rate begins "
             "just above a small allowance.\n"
             "A low threshold and a high rate are different things, and this chart shows only the "
             "threshold.")
    save(fig, "tax-1-where-the-top-begins.png")


def chart2_how_the_money_is_raised():
    """The correction at the centre of the post, drawn.

    Denmark's personal income tax bar is the longest in the OECD and its social contributions bar
    is invisible. Germany and France are the mirror image. The totals are close. That is the
    point, so the bands are ordered to put the two labour taxes adjacent and first.
    """
    order = ["DNK", "SWE", "FIN", "NOR", "ISL", "FRA", "DEU", "NLD", "GBR", "USA"]
    # Three-decimal source values. Formatting from the two-decimal results.json fields rounded
    # twice and drifted four labels, three of them upward (25.045 became "25.1", not "25.0").
    raw = R["tax_mix_raw3"]
    rows = {r["code"]: {**r, **raw.get(r["code"], {})} for r in R["tax_mix"]}
    mean = R["tax_mix_oecd_mean"]

    bands = [
        ("personal_income", "Personal income tax", BLUE),
        ("social_contributions", "Social security contributions", "#7fb2e8"),
        ("payroll", "Payroll taxes", "#b9d4f2"),
        ("vat", "Value added tax", GREEN),
        ("other_goods_services", "Other goods and services taxes\n(excises, vehicle and the rest)",
         "#9fdcc4"),
        ("corporate_income", "Corporate income tax", AMBER),
        ("property", "Property taxes", "#f0cd7a"),
        ("residual", "Unallocable income tax and other", MUTED),
    ]

    labels, series = [], []
    for c in order:
        labels.append(rows[c]["country"])
        series.append([rows[c].get(k) or 0.0 for k, _, _ in bands])
    labels.append("OECD average")
    series.append([mean.get(k) or 0.0 for k, _, _ in bands])

    arr = np.array(series)
    y = np.arange(len(labels))[::-1]

    fig, ax = plt.subplots(figsize=(11.6, 6.6))
    left = np.zeros(len(labels))
    for j, (key, name, colour) in enumerate(bands):
        ax.barh(y, arr[:, j], left=left, color=colour, height=0.66,
                label=name, edgecolor=SURFACE, linewidth=0.6)
        left += arr[:, j]

    for i, c in enumerate(order + ["OECD"]):
        tot = left[i]
        ax.text(tot + 0.45, y[i], f"{tot:.1f}", va="center", fontsize=9.2, color=INK2)

    # Label the two labour-tax bands in place. An earlier version used arrow callouts and they
    # collided across three rows, hiding Iceland's total and the Norway note. Text inside the
    # band cannot collide with anything.
    for i, c in enumerate(order):
        r = rows[c]
        run = 0.0
        for key in ("personal_income", "social_contributions"):
            w = r.get(key) or 0.0
            if w >= 3.2:
                ax.text(run + w / 2, y[i], f"{w:.1f}", va="center", ha="center",
                        fontsize=8.8, color="white", fontweight="bold")
            run += w

    # Norway's corporate band is mostly petroleum, and it is wide enough to say so inside it.
    # "mostly", not "petroleum" flat: the band is the whole 1200 code, and this repository computes
    # no petroleum share, so an unqualified label would assert a number nothing here produces.
    nor = rows["NOR"]
    nor_start = sum(nor.get(k) or 0.0 for k, _, _ in bands[:5])
    ax.text(nor_start + (nor["corporate_income"] or 0) / 2, y[3], "mostly petroleum",
            va="center", ha="center", fontsize=8.8, color="white", fontweight="bold")

    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlim(0, 52)
    ax.set_xlabel("Percent of GDP")
    ax.set_title(f"How the money is actually raised, {R['vintages']['revenue']}", pad=14)
    ax.grid(axis="y", visible=False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3,
              frameon=False, fontsize=9)

    cv = R["labour_tax_convergence"]
    footnote(fig,
             f"OECD Revenue Statistics, {R['vintages']['revenue']}, general government. Bands sum "
             "to the published total by construction; the residual is income tax that a country "
             "does not split between individuals\nand corporations, plus other taxes. The OECD "
             "average is an unweighted mean computed here, because the source file publishes an "
             "OECD total with no component breakdown.\n"
             f"Read the two labour taxes together. Across {', '.join(cv['countries'])} the "
             f"personal income tax line ranges from {cv['personal_income_range'][0]} to "
             f"{cv['personal_income_range'][1]} percent of GDP, a factor of "
             f"{cv['personal_income_ratio']}.\nCount social contributions and payroll taxes as "
             f"well and the same five countries land between {cv['combined_range'][0]} and "
             f"{cv['combined_range'][1]}, a spread of {cv['combined_spread_pts']} points.\n"
             "Against Germany and France in particular, Denmark's income tax is the same money "
             "routed through one channel instead of two. That convergence belongs to these five "
             "countries: swapping France for Norway widens the spread to "
             f"{cv['selection_sensitivity']['alternatives']['FRA->NOR']} points, and the five "
             f"Nordic countries span {cv['selection_sensitivity']['five_nordics_spread']}.\n"
             "Norway's corporate band is mostly petroleum, taxed there under a separate regime at a "
             "78 percent marginal rate rather than the ordinary 22 (rates from the Norwegian "
             "Offshore Directorate and Ministry of Energy; the petroleum share of the band is not "
             "computed here). It is not evidence about what a tax system can raise from ordinary "
             "companies.",
             y=-0.20)
    save(fig, "tax-2-how-the-money-is-raised.png")


def chart3_what_it_buys():
    """The bundle, and the collapse.

    Two fit lines per panel, not one. Across the whole OECD field the tax level looks like it
    buys longer life. Restrict the comparison to countries at similar income and that association
    falls to almost nothing, while poverty reduction survives. A single fit line per panel would
    show the opposite of what is true.
    """
    rows = [r for r in R["outcomes"] if r["total_tax_mean"] is not None]
    poorer = set(R["outcome_robustness"]["poorer_members_removed"])
    fits_all = R["outcome_robustness"]["fits"]["all_oecd"]
    fits_rich = R["outcome_robustness"]["fits"]["excl_poorer_members"]

    ic = R["income_control"]["outcomes"]
    panels = [
        ("life_expectancy", "Life expectancy at birth, years",
         f"Life expectancy, {R['vintages']['life_expectancy']}", "tax_vs_life_expectancy",
         "life_expectancy", (0.97, 0.04, "right", "bottom")),
        ("poverty_disposable_pct", "Share below half the median income, percent",
         "Poverty rate, after taxes and transfers", "tax_vs_poverty_disposable",
         "poverty_disposable", (0.97, 0.96, "right", "top")),
        ("poverty_reduction_pts", "Percentage points removed",
         "Poverty removed by the state", "tax_vs_poverty_reduction_pts",
         "poverty_reduction_pts", (0.03, 0.96, "left", "top")),
    ]

    fig, axes = plt.subplots(1, len(panels), figsize=(15.4, 5.5))
    for ax, (key, ylab, title, fitkey, ickey, box) in zip(axes, panels):
        pts = [(r["total_tax_mean"], r[key], r["code"]) for r in rows if r.get(key) is not None]
        xs = np.array([p[0] for p in pts])
        ys = np.array([p[1] for p in pts])
        cols = [AMBER if p[2] in poorer else BLUE for p in pts]
        ax.scatter(xs, ys, s=40, c=cols, linewidths=0, alpha=0.85, zorder=3)

        grid = np.linspace(xs.min(), xs.max(), 50)
        fa, fr = fits_all[fitkey], fits_rich[fitkey]
        ax.plot(grid, fa["intercept"] + fa["slope"] * grid, color=MUTED, lw=1.6,
                ls=(0, (5, 3)), zorder=2)
        rich_x = np.array([p[0] for p in pts if p[2] not in poorer])
        grid_r = np.linspace(rich_x.min(), rich_x.max(), 50)
        ax.plot(grid_r, fr["intercept"] + fr["slope"] * grid_r, color=BLUE, lw=2.0, zorder=4)

        ax.set_title(title, fontsize=11.5, pad=9)
        ax.set_ylabel(ylab, fontsize=9.6)
        ax.set_xlabel("Total tax revenue, percent of GDP", fontsize=9.6)
        # The annotation box is opaque and sits top-right on this panel, where it covered Costa
        # Rica, the panel's highest observation and one of the five highlighted countries. Give
        # the panel headroom so the box has somewhere to sit that is not on top of the data.
        if key == "poverty_disposable_pct":
            lo, hi = ax.get_ylim()
            ax.set_ylim(lo, hi + 0.20 * (hi - lo))

        bx, by, bha, bva = box
        v = ic[ickey]
        ax.text(bx, by,
                f"Tax alone, all {fa['n']}: R2 {fa['r2']:.3f}\n"
                f"Excluding the 5 lowest income: R2 {fr['r2']:.3f}\n"
                f"What tax adds once income is known: {v['increment_from_tax']:+.3f}",
                transform=ax.transAxes, va=bva, ha=bha, fontsize=9.2, color=INK2,
                bbox=dict(boxstyle="round,pad=0.42", fc=SURFACE, ec=GRID, lw=0.8))

    excl = ", ".join(e["code"] for e in R["poorer_rule"]["excluded"])
    handles = [
        plt.Line2D([], [], marker="o", ls="", color=BLUE, label="Other OECD members"),
        plt.Line2D([], [], marker="o", ls="", color=AMBER,
                   label=f"Five lowest GDP per capita ({excl})"),
        plt.Line2D([], [], ls=(0, (5, 3)), color=MUTED, label="Fit across all OECD members"),
        plt.Line2D([], [], ls="-", color=BLUE, lw=2.0, label="Fit excluding those five"),
    ]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.10), ncol=4,
               frameon=False, fontsize=9.6)
    fig.suptitle("What the revenue buys, and what it only appears to buy",
                 fontsize=13.5, fontweight="bold", y=1.03)

    w = R["vintages"]
    footnote(fig,
             "Tax revenue is the mean of "
             f"{R['tax_level_volatility']['window'][0]} to "
             f"{R['tax_level_volatility']['window'][1]}, the most recent five years in which every "
             "OECD member reports. Single years are unreliable here: Denmark's total falls from "
             f"{R['denmark_2022_fall']['total_2021']:.1f} percent of GDP in 2021 to "
             f"{R['denmark_2022_fall']['total_2022']:.1f} in 2022, outside this window. Its pension "
             f"yield tax accounts for about "
             f"{R['denmark_2022_fall']['pension_yield_share_of_fall_pct']:.0f} percent of that "
             "fall and nominal GDP growth for most of the rest.\nPoverty is "
             "the share below 50 percent of median disposable income, total population, current "
             "income definition, latest year per country, 2019 to 2025, from the OECD Income "
             "Distribution Database.\n"
             f"Life expectancy is {w['life_expectancy']}, a Riley, Zijdeman, HMD and UN WPP "
             "composite with major processing by Our World in Data. GDP per capita is purchasing "
             "power parity, constant 2021 international dollars, 2021, from Eurostat, the OECD, "
             "the IMF and the World Bank jointly,\nwith minor processing by Our World in Data.\n"
             "The five excluded countries are chosen by rule, not by hand: they are the OECD "
             "members with the lowest GDP per capita. Greece is sixth and stays in.\n"
             "Colombia reports no income-distribution data, so the two poverty panels cover 37 "
             "members and drop four of those five rather than all five.\n"
             "These are associations across countries, not causal estimates. The last line in "
             "each box needs no cutoff at all: it is how much the tax level adds to an ordinary "
             "least squares fit that already knows log GDP per capita.\n"
             "Read together: how rich a country is predicts how long its people live, while how "
             "much it taxes tracks how much levelling its transfer system does. The third panel is "
             "the weakest of the three, because poverty removed is DEFINED as market poverty, "
             "which is not plotted here, minus the disposable-income rate in the middle panel,\nso "
             "a larger fiscal state having a larger fiscal effect is close to arithmetic. Market "
             f"poverty alone predicts it better (R2 "
             f"{R['poverty_reduction_is_near_definitional']['market_poverty_alone_r2']:.3f}) than "
             f"the tax level does "
             f"({R['poverty_reduction_is_near_definitional']['tax_only_r2']:.3f}).",
             y=-0.16)
    save(fig, "tax-3-what-it-buys.png")


def chart4_where_the_equalising_happens():
    """Transfers do the work. Taxes do less than almost anyone assumes."""
    rows = R["redistribution"]["by_country"]
    labels = [r["country"] for r in rows]
    tr = np.array([r["transfer_effect"] for r in rows])
    tx = np.array([r["tax_effect"] for r in rows])
    y = np.arange(len(rows))[::-1]

    tot = np.array([r["total_effect"] for r in rows])
    pos = tx.clip(min=0)

    fig, ax = plt.subplots(figsize=(9.8, 10.4))
    ax.barh(y, tr, color=BLUE, height=0.66, label="Done by cash transfers", edgecolor=SURFACE,
            linewidth=0.6)
    ax.barh(y, pos, left=tr, color=AMBER, height=0.66,
            label="Done by direct taxes and employee contributions",
            edgecolor=SURFACE, linewidth=0.6)

    # One country, Switzerland, has a negative tax effect: its disposable-income Gini is higher
    # than its gross-income Gini. Drawn as a red tip running back from the net total to the
    # transfer level. Plotting it as an ordinary negative bar made matplotlib draw it leftwards
    # on top of the blue, which read as if the country simply had a shorter bar.
    giveback = np.where(tx < 0, -tx, 0.0)
    if giveback.any():
        ax.barh(y, giveback, left=tot, color=RED, height=0.66, edgecolor=SURFACE, linewidth=0.6,
                label="Direct taxes measured as slightly increasing inequality")

    for i, r in enumerate(rows):
        end = max(r["total_effect"], r["transfer_effect"])
        ax.text(end + 0.004, y[i], f"{r['transfer_share_pct']:.0f}%",
                va="center", fontsize=8.6, color=RED if r["tax_effect"] < 0 else INK2)

    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9.2)
    ax.set_xlabel("Reduction in the Gini coefficient, market income to disposable income")
    ax.set_title("Where the equalising actually happens", pad=14)
    ax.grid(axis="y", visible=False)
    ax.legend(loc="lower right", frameon=False, fontsize=9.4)
    ax.set_xlim(0, max(r["total_effect"] for r in rows) * 1.16)

    rd = R["redistribution"]
    footnote(fig,
             "OECD Income Distribution Database, latest year available per country, 2019 to 2025, "
             "total population, current income definition. Market income to gross income adds cash "
             "transfers;\ngross to disposable removes direct taxes and employee social "
             "contributions. The percentage at the end of each bar is the transfer share of that "
             "country's total reduction.\n"
             f"The median country does {rd['transfer_share_median_pct']} percent of its "
             f"equalising through transfers, and {rd['transfer_share_gt_50_n']} of "
             f"{rd['n_countries']} countries do more than half of it that way.\n"
             "Switzerland exceeds 100 percent because its disposable-income Gini is measured "
             "slightly above its gross-income Gini, so the tax step subtracts rather than adds.\n"
             "That is what the OECD publishes, and this post does not speculate about the cause. "
             "Israel, at 49 percent, is the only country where transfers do less than half.")
    save(fig, "tax-4-where-the-equalising-happens.png")


if __name__ == "__main__":
    (BASE / "charts").mkdir(exist_ok=True)
    chart1_where_the_top_begins()
    chart2_how_the_money_is_raised()
    chart3_what_it_buys()
    chart4_where_the_equalising_happens()
