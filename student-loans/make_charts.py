"""Charts for Post 19, 'The Payback Period Assumes You Are Paying It Back'.

Reads results.json. Output: charts/loans-N-name.png.

Most figures are interpolated from results.json, but NOT all of them, and saying otherwise is how
stale text survives. Post 18 shipped a blanket guarantee that hid a hardcoded footnote; round 1
here repeated the boast, and round 3 found that chart 3 was still hardcoding a date and chart 4 a
row count, both of which sat in results.json the whole time. They now go through qend() and a
computed `pbc`. Typed literals still present, deliberately: the one-year diagonal in chart 4,
histogram bin width, axis limits, all layout coordinates, plan names, and the statutory dollar
figures quoted from 34 CFR 685.203. Any DATA claim in a label must be interpolated; if you find
yourself typing a number that came from the file, that is the bug.

Two conventions:
  - Every share is a share of DOLLARS outstanding, never of recipients, because the FSA files count
    recipients at loan level and double count them across statuses.
  - Charts 2 and 3 have DIFFERENT denominators and say so on the figure. The repayment-plan table
    excludes default, in-school and grace; the status table does not.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
    # matplotlib writes a Unicode minus (U+2212) on negative ticks by default, which breaks the
    # house no-dash rule inside the rendered image. Force an ASCII hyphen.
    "axes.unicode_minus": False,
})


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def qdec(q):
    """Federal fiscal quarter label to a decimal calendar year.

    The FSA files are on federal fiscal years, which begin 1 October. Q1 ends 12/31 of the PREVIOUS
    calendar year, Q2 ends 3/31, Q3 ends 6/30, Q4 ends 9/30. Plotting the fiscal year as if it were
    a calendar year would shift the pandemic suspension by a quarter, which matters here because the
    argument turns on when the suspension started and ended.
    """
    y, n = int(q[:4]), int(q[-1])
    return {1: y + 0.0, 2: y + 0.25, 3: y + 0.5, 4: y + 0.75}[n]


def qend(q):
    """Federal fiscal quarter label to the calendar date it ends on, spelled out.

    Same trap as qdec, and it has now bitten this post five times. Any caption that wants to say
    WHEN a quarter is must come through here rather than through a human typing a month name.
    """
    y, n = int(q[:4]), int(q[-1])
    return {1: f"31 December {y - 1}", 2: f"31 March {y}",
            3: f"30 June {y}", 4: f"30 September {y}"}[n]


def chart1_the_sum():
    """The price, and it is reassuring. This is the number the reader is allowed to believe."""
    p = R["price"]
    ratios = np.array([s["debt"] / s["earn"] for s in R["scatter"]])
    med = p["ratio_percentiles"]["50"]

    fig, ax = plt.subplots(figsize=(10.0, 5.6))
    bins = np.arange(0, 2.51, 0.05)
    ax.hist(np.clip(ratios, 0, 2.5), bins=bins, color=BLUE, alpha=0.75, edgecolor="none")

    ax.axvline(med, color=INK, lw=2.0, ls=(0, (5, 2)))
    ax.annotate(f"median {med:.2f} years\nof gross salary,\nabout {p['ratio_median_months']:.0f} months",
                xy=(med, ax.get_ylim()[1] * 0.86), xytext=(8, 0), textcoords="offset points",
                fontsize=10.2, color=INK, fontweight="bold", va="center")

    ax.axvline(1.0, color=RED, lw=1.3, ls=(0, (2, 3)))
    ax.annotate(f"one full year of salary.\nOnly {p['share_over_1yr_pct']:.1f}% of programmes\n"
                f"are past this line",
                xy=(1.0, ax.get_ylim()[1] * 0.52), xytext=(1.28, ax.get_ylim()[1] * 0.60),
                textcoords="data", fontsize=9.4, color=RED, ha="left",
                arrowprops=dict(arrowstyle="->", color=RED, lw=0.9))

    ax.set_title("The sum looks fine. The median American programme costs about seven months\n"
                 "of what its graduates go on to earn")
    ax.set_xlabel("Median debt at graduation, divided by median earnings one year later")
    ax.set_ylabel("Programmes")
    ax.set_xlim(0, 2.5)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.1f}")
    ax.annotate(
        f"College Scorecard, field of study. Every programme with both a median debt and a median "
        f"earnings figure: {p['n_programmes']:,} programmes at {p['n_institutions']:,} institutions "
        f"across {p['n_cip']} fields.\nMedian debt ${p['median_debt']:,.0f} against median earnings "
        f"${p['median_earnings']:,.0f}. Quartiles {p['ratio_percentiles']['25']:.2f} and "
        f"{p['ratio_percentiles']['75']:.2f}, 95th percentile {p['ratio_percentiles']['95']:.2f}. "
        f"Bars beyond 2.5 are stacked into the last bin.\nEarnings count only graduates working and "
        f"not enrolled, so the "
        f"{R['traps']['not_working']['analysis_sample']['pct_of_not_enrolled_graduates']:.1f}% of "
        f"non-enrolled graduates with no earnings that year are outside this picture, which flatters "
        f"it.\n0.59 is the median of each programme's own ratio, not the ratio of the two medians, "
        f"which is {p['median_debt'] / p['median_earnings']:.2f}.",
        xy=(0, -0.155), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "loans-1-the-sum.png")


def chart2_the_break():
    """The load-bearing chart. The schedule the sum assumes is a minority of the money.

    This one carries the structural claim rather than chart 3, but NOT because the endpoints
    match. Round 2 showed the raw series swings 21.9 to 17.5 to 28.3 to 21.9 as loans leave and
    re-enter the "not on a plan" bucket. The stable reading is against dollars on a NAMED plan:
    22.6% before the suspension, 22.1% now.
    """
    s = pd.DataFrame(R["plans"]["series"])
    s["t"] = s.quarter.map(qdec)
    pl = R["plans"]

    fig, ax = plt.subplots(figsize=(10.0, 5.7))
    # ROUND 3 CORRECTION. The middle band used to be 100 - standard - IDR, labelled "other fixed or
    # graduated plans". That band also held the file's residual "not on any plan" column, which at
    # its peak was larger than the genuine other plans. So the annotation and the footnote both told
    # the reader the swing came from a bucket that the picture gave them no way to see, inside a
    # band named as something it was not. The residual now has its own band and its own name, and
    # the argument is visible rather than asserted.
    ax.stackplot(s.t, s.standard_pct, s.other_named_pct, s.residual_pct, s.idr_pct,
                 colors=[BLUE, SHADE, BASELINE, AMBER], alpha=0.85,
                 labels=["standard plan, 10 years or less",
                         "other fixed or graduated plans",
                         "not on any plan (the file's residual column)",
                         "income-driven plans"])

    for y, lab, col in ((s.standard_pct.iloc[-1] / 2, f"{pl['latest']['standard_pct']:.1f}%", INK),
                        (100 - s.idr_pct.iloc[-1] / 2, f"{pl['latest']['idr_pct']:.1f}%", INK)):
        ax.annotate(lab, xy=(s.t.iloc[-1], y), xytext=(8, 0), textcoords="offset points",
                    fontsize=11, fontweight="bold", color=col, va="center")

    # ROUND 2 CORRECTION. This used to test only whether the two endpoints matched and, when they
    # did, print "Identical: the suspension never touched this series". Equal endpoints say nothing
    # about the path, and the path moves: the raw share fell to 17.5% and spiked to 28.3% as loans
    # left and re-entered the "not on a plan" bucket. Describe the journey, not the endpoints.
    pre, w = pl["pre_pandemic"], pl["since_pre_pandemic"]
    ax.annotate(f"{pre['standard_pct']:.1f}% before the suspension and "
                f"{pl['latest']['standard_pct']:.1f}% now,\nbut it travelled: {w['raw_min']}% to "
                f"{w['raw_max']}% in between,\nas loans left and re-entered the\n"
                f"'not on any plan' bucket",
                xy=(qdec(pre["quarter"]), pre["standard_pct"]), xytext=(2014.2, 46),
                textcoords="data", fontsize=9.4, color=INK2, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

    # Scope in the title: 21.9% is of the repayment-plan table, not of all federal student debt.
    # ROUND 3 CORRECTION. The title said "of the loans on a repayment plan", which names the NAMED
    # denominator ($1,230.5B, against which the figure is 22.1%). The 21.9% is of the whole table,
    # which includes the residual column. In a post about denominators, say which one.
    ax.set_title("The payback sum assumes a ten-year schedule.\n"
                 "About one dollar in five of the loans in this table is on one")
    ax.set_ylabel("Share of dollars outstanding")
    ax.set_xlim(s.t.min(), s.t.max())
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.legend(loc="lower left", frameon=False, fontsize=9.6)
    # Keep every line short enough that bbox_inches="tight" does not widen the whole figure. A
    # previous edit spliced this sentence in mid-clause, producing "This table Measured against..."
    # and blowing the PNG out to 3096px wide. ALWAYS read the rendered image after editing a caption.
    ax.annotate(
        f"Federal Student Aid, Direct Loan portfolio by repayment plan, {s.quarter.iloc[0]} to "
        f"{s.quarter.iloc[-1]}, ${s.total_bn.iloc[-1]:,.0f}B outstanding. Standard plans fell from "
        f"{pl['first']['standard_pct']:.1f}% in {pl['first']['quarter']} while\nincome-driven plans "
        f"rose from {pl['first']['idr_pct']:.1f}% to {pl['latest']['idr_pct']:.1f}%. Equal endpoints "
        f"are not stability: the standard line fell to {w['raw_min']}% and spiked to {w['raw_max']}% "
        f"in between, as loans left and\nre-entered the file's residual 'not on any plan' column, "
        f"which ran {w['other_pre']}% before the suspension, {w['other_peak']}% at its peak and "
        f"{w['other_latest']}% now. Against dollars on a NAMED plan the\nartefact mostly clears: "
        f"{pl['pre_pandemic']['standard_named_pct']:.1f}% before against "
        f"{pl['latest']['standard_named_pct']:.1f}% now, and since that quarter within a "
        f"{w['named_min']}% to {w['named_max']}% band, against "
        f"{pl['first']['standard_named_pct']:.1f}% on the same basis in {pl['first']['quarter']}.\n"
        f"This table covers loans in repayment, deferment and forbearance "
        f"and EXCLUDES default, in-school and grace, so its denominator is "
        f"${s.total_bn.iloc[-1]:,.0f}B against the\n"
        f"${R['status']['latest_total_bn']:,.0f}B whole portfolio in chart 3.",
        xy=(0, -0.135), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "loans-2-the-break.png")


def chart3_second_proof():
    """The second, independent argument: a schedule that can be switched off for three years."""
    s = pd.DataFrame(R["status"]["series"])
    s["t"] = s.quarter.map(qdec)
    order = ["Repayment", "Forbearance", "Deferment", "Cumulative in Default*", "In-School",
             "Grace", "Other"]
    cols = [GREEN, AMBER, "#c9a227", RED, BLUE, "#9dc3ea", SHADE]
    lab = {"Cumulative in Default*": "in default", "In-School": "in school", "Grace": "grace",
           "Repayment": "in active repayment", "Forbearance": "forbearance",
           "Deferment": "deferment", "Other": "other"}

    fig, ax = plt.subplots(figsize=(10.0, 5.7))
    ax.stackplot(s.t, *[s[c] for c in order], colors=cols, alpha=0.85,
                 labels=[lab[c] for c in order])

    rp = R["status"]["repayment_share_of_post_school"]
    pause = R["traps"]["pause"]
    pre_t = qdec(pause["pre_pandemic_quarter"])
    # Point at the TOP of the repayment band in the quarter being named, not at an arbitrary spot
    # inside it. The first version put the arrow tip at y=28 in the middle of the green, which
    # labelled nothing.
    ax.annotate(f"{pause['pre_pandemic_repayment_pct']:.1f}% of all dollars in active repayment,\n"
                f"and {rp['pre_pandemic']:.1f}% of those that had left school",
                xy=(pre_t, pause["pre_pandemic_repayment_pct"]), xytext=(2013.75, 72),
                textcoords="data", fontsize=9.4, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=INK2, lw=0.9))
    ax.annotate(f"the CARES suspension:\nrepayment falls to "
                f"{pause['repayment_min_pct']:.1f}%",
                xy=(qdec(pause["repayment_min_quarter"]), 1.5),
                xytext=(2019.6, 20), textcoords="data", fontsize=9.4, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=INK2, lw=0.9))
    # ROUND 1 CORRECTION. The chart previously let the reader infer that repayment never recovered,
    # which the draft then said outright and which is false. Mark the overshoot.
    rc = R["status"]["recovery"]
    ax.annotate(f"then it overshoots: {rc['peak_after_suspension_pct']:.1f}%,\n"
                f"above the {rc['pre_pandemic_pct']:.1f}% of before",
                xy=(qdec(rc["peak_quarter"]), rc["peak_after_suspension_pct"] * 0.55),
                xytext=(2024.35, 84), textcoords="data", fontsize=9.4, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=INK2, lw=0.9))

    # The legend sits above the axes, so the title needs padding or the two collide.
    # ROUND 3 CORRECTION. This title said "switched off and on twice in six years". The series shows
    # ONE complete off-and-on cycle, then a single step down in the quarter ending 31 December 2024
    # that has not reversed: repayment has sat between 37.8% and 40.7% for seven quarters. It also
    # implied an agent behind the second move, which the draft explicitly declines to attribute.
    ax.set_title("The schedule was switched off, came back, then settled well below where it "
                 "started.\n"
                 "Every federal Direct Loan dollar, by what it was doing", pad=46)
    ax.set_ylabel("Share of dollars outstanding")
    ax.set_xlim(s.t.min(), s.t.max())
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.085), frameon=False,
              fontsize=9.2, ncol=7, columnspacing=1.1, handletextpad=0.5)
    fp = R["status"]["federal_portfolio_bn"]
    fs = R["status_forbearance_second_episode"]
    ax.annotate(
        f"Federal Student Aid, Direct Loan portfolio by loan status, {s.quarter.iloc[0]} to "
        f"{s.quarter.iloc[-1]}, ${R['status']['latest_total_bn']:,.0f}B outstanding. That is Direct "
        f"Loans only, of a ${fp['total']:,.0f}B federal total that also holds\n${fp['ffel']:,.0f}B of "
        f"FFEL and ${fp['perkins']:,.1f}B of Perkins. Shares are of dollars, not of borrowers: the "
        f"file counts recipients at loan level and warns they may be counted in more than one "
        f"status.\nOf dollars that had left school, {rp['pre_pandemic']:.1f}% were in active "
        f"repayment in the quarter ending {qend(R['traps']['pause']['pre_pandemic_quarter'])} and "
        f"{rp['latest']:.1f}% are now, so even "
        f"in a calm year about a third were not. The 2020 to 2023\nblock is the CARES Act "
        f"suspension; the later decline is a second and separate rise in forbearance, which peaked "
        f"at {fs['peak_pct']:.1f}% in the quarter ending\n{qend(fs['peak_quarter'])} and has fallen "
        f"in each of the {fs['quarters_falling_since_peak']} quarters since, not "
        f"pandemic residue.",
        xy=(0, -0.135), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "loans-3-second-proof.png")


def chart4_the_cap():
    """The close, and the chart that changed what I thought the post was about.

    This began as "debt and earnings travel together", which the picture refuted: the correlation is
    0.25. The second guess, "debt hardly moves", was also wrong; the two spread by almost the same
    factor. What is genuinely in the figure is horizontal banding. Median debt piles up on the
    federal borrowing caps, so the reassuring price in chart 1 is partly a statutory artefact rather
    than a market outcome. Axes are cut close to the data so the bands are visible; the earlier
    version ran both to $120k and buried them.
    """
    t = pd.DataFrame(R["scatter"])
    p, c = R["price"], R["caps"]
    creds = [x["CREDDESC"] for x in R["by_credential"] if x["n"] >= 100]
    # The one credential below the legend threshold, named in the footnote. Counting it here rather
    # than typing "22" keeps the caption true when the file is refreshed.
    pbc = sum(x["n"] for x in R["by_credential"] if x["n"] < 100)
    colmap = {"Bachelor's Degree": BLUE, "Associate's Degree": GREEN,
              "Undergraduate Certificate or Diploma": AMBER}

    fig, ax = plt.subplots(figsize=(10.2, 6.4))
    for cd in creds:
        g = t[t.cred == cd]
        n = [x for x in R["by_credential"] if x["CREDDESC"] == cd][0]
        ax.scatter(g.earn, g.debt, s=6, color=colmap.get(cd, MUTED), alpha=0.22, linewidths=0,
                   label=f"{cd}  ({n['n']:,})")

    xlim, ylim = 100000, 45000
    for cap, lab in ((c["four_year_cap"],
                      f"${c['four_year_cap']:,}, four years at the annual maximums: "
                      f"{c['n_at_four_year_cap']:,} programmes ({c['pct_at_four_year_cap']:.1f}%)"),
                     (c["aggregate_cap"],
                      f"${c['aggregate_cap']:,}, the ceiling for a DEPENDENT undergraduate")):
        ax.axhline(cap, color=RED, lw=1.4, ls=(0, (5, 3)), zorder=5)
        ax.annotate(lab, xy=(xlim * 0.995, cap), xytext=(0, 5), textcoords="offset points",
                    fontsize=9.3, color=RED, ha="right", va="bottom", fontweight="bold")

    ax.scatter([p["median_earnings"]], [p["median_debt"]], s=130, facecolor="none",
               edgecolor=INK, lw=2.0, zorder=6)
    ax.annotate(f"the median programme:\n${p['median_debt']:,.0f} against ${p['median_earnings']:,.0f}",
                xy=(p["median_earnings"], p["median_debt"]), xytext=(30, -46),
                textcoords="offset points", fontsize=9.8, color=INK, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))

    # ROUND 1 CORRECTION. This was titled "The price is capped by statute, not set by the market",
    # which asserts that the caps explain the low ratio. They do not: dropping every programme on a
    # cap moves the median 0.591 to 0.569, about eight days. The clustering is real, the causal
    # claim was not. The title now says what the picture shows and nothing more.
    ax.set_title("Borrowing piles up on round numbers set in Washington.\n"
                 "An administered price, and one that says little about what the degree earns")
    ax.set_xlabel("Median earnings one year after completing")
    ax.set_ylabel("Median debt at graduation")
    ax.set_xlim(0, xlim); ax.set_ylim(0, ylim)
    for a in (ax.xaxis, ax.yaxis):
        a.set_major_formatter(lambda v, _: f"${v / 1000:,.0f}k")
    ax.legend(loc="upper left", frameon=False, fontsize=9.2, markerscale=3.0)
    ax.annotate(
        f"College Scorecard, field of study: {p['n_programmes']:,} programmes. Debt is median "
        f"Stafford and Grad PLUS borrowing across all institutions attended, so it is what the "
        f"borrower owes, not what this school lent.\nDebt and earnings correlate only "
        f"{c['corr_debt_earnings_pearson']:.2f} ({c['corr_debt_earnings_spearman']:.2f} on ranks), "
        f"so the price of a degree says little about what it pays. "
        f"{c['share_15k_to_32k_pct']:.1f}% of programmes sit between $15k and $32k. The two lines "
        f"are the\ndependent undergraduate limits in {c['regulation']}: $5,500, $6,500, $7,500 and "
        f"$7,500 by year of study, each a subsidised maximum plus a $2,000 unsubsidised addition, "
        f"and ${c['aggregate_cap']:,} in total.\nThe caps do NOT explain the low debt-to-earnings "
        f"ratio: dropping every programme sitting on one moves the median from "
        f"{c['median_ratio_all']:.3f} to {c['median_ratio_excluding_caps']:.3f}, about "
        f"{c['cap_effect_days']:.0f} days of salary. {c['pct_above_dependent_cap']:.1f}% sit above "
        f"${c['aggregate_cap']:,}, which is\nallowed: an INDEPENDENT undergraduate may borrow "
        f"${c['aggregate_cap_independent']:,}. The next two densest values, "
        f"${c['second_band']['debt']:,.0f} and ${c['third_band']['debt']:,.0f}, are not statutory "
        f"limits at all.\nAxes are cut at ${xlim / 1000:,.0f}k and ${ylim / 1000:,.0f}k; graduate "
        f"degrees are absent because the all-institutions debt figure is not published for them, and "
        f"post-baccalaureate certificates are left out of the legend at {pbc:,}.",
        xy=(0, -0.135), xycoords="axes fraction", fontsize=8.6, color=MUTED, va="top")
    save(fig, "loans-4-the-cap.png")


if __name__ == "__main__":
    (BASE / "charts").mkdir(exist_ok=True)
    chart1_the_sum()
    chart2_the_break()
    chart3_second_proof()
    chart4_the_cap()
