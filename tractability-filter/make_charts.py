"""Charts for Post 23, 'Greed You Can Regulate. Difficulty You Have to Pay For.'

Reads results.json. Output: charts/tf-N-name.png.

Numbers drawn or written here are interpolated from results.json, with three classes of exception
that round 4 forced into the open rather than leaving behind a docstring that claimed otherwise:
axis limits and layout coordinates; the names of conditions the post calls out; and a small number
of fixed vintage labels that would be wrong to interpolate because they describe the source rather
than the result ("2021", "per 100,000", "constant 2021 dollars"). Row and condition counts used to
be typed here too, which is how chart 3 came to print "31 conditions" for 31 rows covering 32; they
are interpolated now.

House rule: no em or en dashes anywhere, including inside rendered images. matplotlib writes a
Unicode minus on negative ticks unless axes.unicode_minus is False.

After editing any caption, RE-OPEN THE PNG and look at it. Posts 20, 21 and 22 each shipped a
caption that had gone stale while the code looked correct, and on Post 21 an annotation box
covered a data point entirely. Reading the code is not the same as looking at the picture.
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

# Colour carries one argument and only one: blue means the disease has something to aim at,
# amber means it does not. That binary is the finding that survived; the three-class gradient
# in the design doc did not, and is deliberately NOT encoded anywhere in these charts.
C_TARGET, C_NONE = BLUE, AMBER
COND = {c["cause"]: c for c in R["conditions"]}


def human(v, _=None):
    """Plain-text axis labels.

    The house style sets text.parse_math False, which stops matplotlib rendering the dollar
    signs that would otherwise appear in captions. The side effect is that its default log
    formatter emits a literal '$\\mathdefault{10^{4}}$' on every log tick. Caught by opening
    the PNG; invisible in the code. Every log axis in this file sets this formatter.
    """
    if v <= 0:
        return "0"
    for div, suffix in ((1e9, " bn"), (1e6, " m"), (1e3, "k")):
        if v >= div:
            q = v / div
            return f"{q:,.0f}{suffix}" if q >= 10 or q == int(q) else f"{q:,.1f}{suffix}"
    return f"{v:,.0f}"


def logticks(ax, which="both"):
    from matplotlib.ticker import FuncFormatter, NullFormatter
    for axis in ((ax.xaxis, ax.yaxis) if which == "both" else
                 ((ax.xaxis,) if which == "x" else (ax.yaxis,))):
        axis.set_major_formatter(FuncFormatter(human))
        axis.set_minor_formatter(NullFormatter())


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def footnote(fig, text, y=-0.02):
    fig.text(0.0, y, text, ha="left", va="top", fontsize=8.6, color=MUTED, wrap=True)


def colour(c):
    return C_TARGET if c["t1"] else C_NONE


# ------------------------------------------------------------------ 1. transport

def chart1():
    """What we fixed and what we did not.

    Two panels, two different units, two different spans. They are deliberately NOT plotted on a
    shared axis: the comparison is between the SHAPES, and forcing them onto one scale would be
    the exact sleight of hand this post is about.
    """
    t = R["transport"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(12.0, 4.7),
                               gridspec_kw={"width_ratios": [1.08, 1.0], "wspace": 0.34})

    # WHO's OWN published global split, from the REPORT, pages 10, 15 and 17. This panel has been
    # wrong twice. Rounds 1 to 3 plotted a recomputation from country-level RS_246 at 22.8 percent
    # labelled "car occupants". Round 4 replaced it with 30 percent from WHO's launch NEWS RELEASE,
    # which assigns to car occupants the share the report gives to MOTORCYCLISTS. Round 5 opened
    # the report. Four-wheeled vehicle occupants are 25 percent, and the residual is WHO's own 19.
    order = sorted(t["user_shares_pct"].items(), key=lambda kv: kv[1])
    ypos = np.arange(len(order))
    resid = t["user_shares_residual_label"]
    four = "Occupants of four-wheeled vehicles"
    # Blue is the vehicle that got the engineering. Amber is everyone outside it. The residual is
    # grey because it is a mixed bag WHO does not break out, not because it is derived here.
    cols = [BLUE if k == four else (SHADE if k == resid else AMBER) for k, _ in order]
    a.set_axisbelow(True)          # gridlines were rendering OVER the bars, segmenting them
    a.barh(ypos, [v for _, v in order], color=cols, height=0.68,
           edgecolor=[BASELINE if k == resid else "none" for k, _ in order], linewidth=0.9)
    a.set_yticks(ypos, [k.replace("Riders of powered two and three wheelers",
                                  "Riders of powered two\nand three wheelers")
                         .replace("Occupants of four-wheeled vehicles",
                                  "Occupants of\nfour-wheeled vehicles")
                         .replace("Buses, heavy goods, other and unknown",
                                  "Buses, heavy goods,\nother and unknown")
                        for k, _ in order], fontsize=9.2)
    for y, (k, v) in zip(ypos, order):
        a.text(v + 0.5, y, f"{v:.0f}%", va="center", fontsize=9.6, color=INK2)
    a.set_xlim(0, max(v for _, v in order) * 1.26)
    a.grid(axis="y", visible=False)
    a.set_xlabel("Share of the world's road deaths, WHO's published global split")
    a.set_title("Who actually dies on the roads")
    # Two stacked annotations. At 0.10 and 0.03 the bold line struck straight through the WHO line
    # below it, which the code could not show and the PNG did in one look. Round 5.
    a.text(0.985, 0.185, f"{t['not_in_four_wheeler_pct']:.0f}% were not in a car",
           transform=a.transAxes, ha="right", va="bottom", fontsize=11.4, color=AMBER,
           fontweight="bold")
    # WHO states a word here, not a number. The 53 percent an earlier version printed came from the
    # news release and was built on its transposed shares.
    a.text(0.985, 0.035,
           f"WHO: pedestrians, cyclists and other vulnerable\nroad users are {t['vulnerable_wording']}",
           transform=a.transAxes, ha="right", va="bottom", fontsize=9.4, color=INK2, linespacing=1.5)

    eyrs = sorted(int(y) for y in t["ev_share_by_year"])
    evals = [t["ev_share_by_year"][str(y)] for y in eyrs]
    b.plot(eyrs, evals, color=BLUE, lw=2.6, marker="o", ms=5)
    b.set_ylim(0, max(evals) * 1.25)
    b.set_xticks([y for y in eyrs if y % 3 == 1] + [eyrs[-1]])
    b.set_title("What the car became instead")
    b.set_ylabel("Electric share of new car sales, world (%)")
    b.annotate(f"{evals[0]:.3f}% in {eyrs[0]}", (eyrs[0], evals[0]), textcoords="offset points",
               xytext=(6, 10), fontsize=9.6, color=INK2)
    # ".0f", not ".1f": the IEA series is published to two significant figures (15, 18, 21, 25),
    # so "25.0" asserts a decimal place neither the IEA nor Our World in Data publishes. Offset
    # widened from -10 to -16 because at -10 the label sat on the series line at blog width.
    b.annotate(f"{evals[-1]:.0f}% in {eyrs[-1]}", (eyrs[-1], evals[-1]),
               textcoords="offset points", xytext=(-16, -20), fontsize=9.6, color=INK2, ha="right")

    fig.suptitle("The engineering went into the box that a minority of the victims sit in",
                 fontsize=14.5, fontweight="bold", x=0.0, ha="left", y=1.05)
    d = t["user_split_disagreement"]
    v = d["variants"]
    four = "Occupants of four-wheeled vehicles"
    footnote(fig,
             f"Left: WHO's own published global distribution, Global status report on road safety "
             f"2023, from country-reported data for 2021. The {t['user_shares_residual_pct']:.0f}% "
             f"in grey is WHO's own residual, not a figure derived here: WHO describes it as "
             f"occupants of vehicles carrying more than ten people, heavy goods vehicles, and "
             f"users it records as other or unknown. Recomputing the split from WHO's own "
             f"country-level indicator RS_246, whose returns are from 2013 and 2016, does not "
             f"quite reproduce it: "
             f"{v['complete_filter'][four]:.1f}% across the "
             f"{v['complete_filter']['countries']} countries reporting a complete five-way split "
             f"that sums near 100, {v['all_five_no_tolerance'][four]:.1f}% across all "
             f"{v['all_five_no_tolerance']['countries']} reporting five categories. Both sit "
             f"within about two points of WHO's 25%, and the post reports the lower one. "
             f"Right: International "
             f"Energy Agency, world, {eyrs[0]} to {eyrs[-1]}. The panels share no unit and are "
             f"not drawn to a common scale.", y=-0.05)
    save(fig, "tf-1-who-dies-and-what-we-rebuilt.png")


# ------------------------------------------------------------------ 2. burden vs effort

SHORT = {"Alzheimer disease and other dementias": "Dementias",
         "Ischaemic heart disease": "Heart disease",
         "Chronic obstructive pulmonary disease": "COPD",
         "Other hearing loss": "Hearing loss",
         "Depressive disorders": "Depression",
         "Trachea, bronchus, lung cancers": "Lung cancer",
         "Colon and rectum cancers": "Colorectal cancer",
         "Uncorrected refractive errors": "Refractive errors",
         # The merged money row is named "Road injury and falls" in results.json. An entry keyed
         # "Falls and road injury" sat here unused until round 4: every lookup is .get(), so a dead
         # key never raises, it just silently stops shortening. That is what forced the wspace
         # widening below, when the full-length tick label overflowed into the left panel.
         "Road injury and falls": "Road injury, falls"}

# Labels placed by offset in points. Safe only where a point has clear space around it.
# Round 4 moved two of these after measuring the rendered pixels: the "Depression" label sat ON the
# blue lung-cancer marker, so a screenshot of this chart appeared to code depression as having a
# validated target, which is the exact opposite of what the post argues at its most contested
# point; and "Stroke" sat on the ischaemic-heart-disease marker. Depression now takes a leader line
# into the clear top-right, which is the mechanism this file already uses for crowded points.
NUDGE = {"Back and neck pain": (-12, -22), "Multiple sclerosis": (-92, 4),
         "Malaria": (13, -4), "Ischaemic heart disease": (-20, -24),
         "Breast cancer": (8, 8),
         "Diabetes mellitus": (-20, 12), "HIV/AIDS": (10, 6)}

# Leader lines out to clear space, for points with no room around them. Three separate
# collisions were only visible in the rendered PNG and invisible in the code: the five
# lowest-effort conditions pile up around eight to eleven million healthy years lost, the
# rheumatoid arthritis label landed on top of the epilepsy marker, and the dementias label
# ran across the back and neck pain point. Y positions are data coordinates, hand-spaced.
LEADERS = {"Depressive disorders": 17500, "Stroke": 12300,
           "Alzheimer disease and other dementias": 9200,
           "Falls": 2450, "Migraine": 1500,
           "Other hearing loss": 920, "Self-harm": 560, "Road injury": 345}
# Round 5 moved this from 2350 to 3050 to clear the Multiple sclerosis marker and made it worse:
# at 3050 the line runs INTO the MS disc and stops, so it reads as labelling MS, which is the named
# half of the post's most-defended comparison. Round 6 measured both and put it back below the
# marker instead of above it. Round 6 swept every candidate position and measured the minimum
# clearance to all 34 markers: 3050 gives 4.9 pt, 2350 gives 6.7, 800 gives 12.3. Re-run that
# sweep before moving this again; three rounds moved it by eye and two made it worse.
LEADERS_LEFT = {"Rheumatoid arthritis": 800}


def chart2():
    """Burden against effort, coloured by whether there is anything to aim at."""
    rows = R["conditions"]
    x = np.array([c["hi_dalys"] for c in rows])
    y = np.array([c["trials"] for c in rows])

    fig, ax = plt.subplots(figsize=(11.4, 7.2))
    for c in rows:
        ax.scatter(c["hi_dalys"], c["trials"], s=86, color=colour(c),
                   edgecolor=SURFACE, linewidth=1.1, zorder=3)

    b = R["models"]["m1_burden_only"]["beta"]
    gx = np.logspace(np.log10(x.min()) - 0.2, np.log10(x.max()) + 0.2, 60)
    ax.plot(gx, 10 ** (b[0] + b[1] * np.log10(gx)), color=MUTED, lw=1.4, ls="--", zorder=2)

    for name, off in NUDGE.items():
        c = COND[name]
        ax.annotate(SHORT.get(name, name), (c["hi_dalys"], c["trials"]),
                    textcoords="offset points", xytext=off, fontsize=9.4, color=INK2, zorder=4)

    ax.set_xscale("log"), ax.set_yscale("log")
    ax.set_xlim(1.2e3, 7.0e8)
    ax.set_ylim(250, 4.2e4)
    logticks(ax)
    ax.set_xlabel("Healthy years of life lost in high-income countries, 2021 (log scale)")
    ax.set_ylabel("Clinical trials ever registered (log scale)")
    ax.set_title("The size of a problem barely predicts how much it gets studied")

    for stack, lx, ha in ((LEADERS, 1.15e8, "left"), (LEADERS_LEFT, 1.5e4, "right")):
        for name, ly in stack.items():
            c = COND[name]
            ax.annotate(SHORT.get(name, name), xy=(c["hi_dalys"], c["trials"]),
                        xytext=(lx, ly), fontsize=9.4, color=INK2, va="center", ha=ha,
                        zorder=4, arrowprops=dict(arrowstyle="-", color=BASELINE, lw=0.9,
                                                  shrinkA=2, shrinkB=5))

    bp, ms = COND["Back and neck pain"], COND["Multiple sclerosis"]
    h = R["headline"]["back_pain_vs_ms"]
    ax.annotate("", xy=(bp["hi_dalys"], bp["trials"]), xytext=(ms["hi_dalys"], ms["trials"]),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5, alpha=0.7), zorder=1)
    ax.text(0.015, 0.045,
            f"Back and neck pain carries {h['burden_multiple']:.0f} times the burden of\n"
            f"multiple sclerosis and draws {h['trials_multiple']:.1f} times the trials.",
            transform=ax.transAxes, ha="left", va="bottom", fontsize=10.6, color=RED,
            fontweight="bold", zorder=5)

    ax.scatter([], [], s=86, color=C_TARGET, label="Has a validated biological target")
    ax.scatter([], [], s=86, color=C_NONE, label="No validated biological target")
    ax.plot([], [], color=MUTED, lw=1.4, ls="--", label="Fitted line, burden only")
    ax.legend(loc="upper left", frameon=False, fontsize=9.8)

    tgt = R["by_target"]
    footnote(fig,
             f"Burden: WHO Global Health Estimates 2021, high-income economies, all ages, both "
             f"sexes. Effort: studies registered on ClinicalTrials.gov, whole registry to date. "
             f"Trial counts are global while burden here is high-income, and the most generous "
             f"of several search terms was used for every condition, both of which work against "
             f"the pattern shown. One exception, and it runs the other way: the term rule provably "
             f"failed for road injury, labelled here, whose candidate terms were all crash "
             f"vocabulary while the registry files trauma by pathology. That undercounts a "
             f"low-effort condition and so flatters the pattern. Median trials per million "
             f"healthy years lost: "
             f"{tgt['validated_target']['median_trials_per_m_hi']:,.0f} for the "
             f"{tgt['validated_target']['n']} conditions with a target, "
             f"{tgt['no_validated_target']['median_trials_per_m_hi']:,.0f} for the "
             f"{tgt['no_validated_target']['n']} without one.", y=-0.02)
    save(fig, "tf-2-burden-against-effort.png")


# ------------------------------------------------------------------ 3. the money

def chart3():
    """Money, and the two explanations for where it goes."""
    rows = R["money_rows"]      # shared RCDC categories merged, not deduplicated
    # wspace 0.40: at the default the right panel's longest tick label, "Road injury and falls",
    # overflowed left into panel A and the fitted line was drawn straight through it. Visible
    # only in the rendered PNG.
    fig, (a, b) = plt.subplots(1, 2, figsize=(13.0, 5.6),
                               gridspec_kw={"width_ratios": [1.02, 1.0], "wspace": 0.40})

    for c in rows:
        a.scatter(c["us_dalys"], c["nih_usd"] / 1e6, s=74, color=colour(c),
                  edgecolor=SURFACE, linewidth=1.1, zorder=3)
    m = R["models"]["money_m1_burden_only"]
    xs = np.array([c["us_dalys"] for c in rows], float)
    gx = np.logspace(np.log10(xs.min()) - 0.15, np.log10(xs.max()) + 0.15, 60)
    a.plot(gx, 10 ** (m["beta"][0] + m["beta"][1] * np.log10(gx)) / 1e6,
           color=MUTED, lw=1.4, ls="--", zorder=2)
    a.set_xscale("log"), a.set_yscale("log")
    logticks(a)
    a.set_xlabel("Healthy years lost in the United States, 2021 (log scale)")
    a.set_ylabel("NIH research funding, millions of dollars (log scale)")
    a.set_title("American money against American disease")
    # "rows", not "conditions": road injury and falls share one NIH category and are merged, so
    # 31 rows cover 32 conditions. The prose was corrected in round 1 and this image was not.
    a.text(0.03, 0.86,
           f"Burden explains almost none of\nwhat these categories capture.\nSlope t = {m['t'][1]:.2f}, "
           f"adjusted R squared = {m['adj_r2']:.3f}, {m['n']} rows.",
           transform=a.transAxes, va="top", fontsize=10, color=INK2)

    top = sorted(rows, key=lambda c: -c["hi_dalys"])[:12]
    top = sorted(top, key=lambda c: c["nih_usd_per_us_daly"])
    ypos = np.arange(len(top))
    b.barh(ypos, [c["nih_usd_per_us_daly"] for c in top],
           color=[colour(c) for c in top], height=0.72)
    b.set_yticks(ypos, [SHORT.get(c["cause"], c["cause"]) for c in top], fontsize=9.6)
    b.set_xlabel("NIH dollars per healthy year lost in the United States")
    # NOT "the twelve largest high-income burdens": COVID-19 is larger than all of them and the
    # post says so two sections earlier, but it is not one of the 34 conditions and is not drawn
    # here. These are the twelve largest of the rows this chart has. Caught in round 4.
    b.set_title(f"The twelve largest of these {len(rows)} by high-income burden,\n"
                f"plotted by US money per US year of life lost", fontsize=11.6)
    for yv, c in zip(ypos, top):
        # One decimal below 100. At ".0f" back and neck pain printed "$12" while the post printed
        # 11.5 and derived "about 42 times" from 11.5; a reader comparing the two saw two different
        # numbers for one quantity, and 479/12 is 40, not 42. Caught in round 4.
        v = c["nih_usd_per_us_daly"]
        b.text(v * 1.03, yv, f"${v:,.0f}" if v >= 100 else f"${v:,.1f}",
               va="center", fontsize=9.2, color=INK2)
    b.set_xlim(0, max(c["nih_usd_per_us_daly"] for c in top) * 1.22)
    b.grid(axis="y", visible=False)

    fig.suptitle("NIH money does not follow the damage either",
                 fontsize=14.5, fontweight="bold", x=0.0, ha="left", y=1.03)
    md = R["models"]["money_domestic_m1_burden_only"]
    footnote(fig,
             f"NIH RePORTER, fiscal year {R['meta']['money_source'].split('FY')[1][:4]} awards "
             f"summed over projects tagged with each disease category. Categories overlap by "
             f"construction and do not partition the NIH budget. The chart excludes leukaemia, "
             f"which has no general category, and malaria, whose American burden rounds to zero; "
             f"road injury and falls share a category and are merged, so {m['n']} rows cover "
             f"{m['n'] + 1} conditions. Three categories are wider than the condition they stand "
             f"for and are ceilings, not measurements: refractive errors under all eye disease, "
             f"cirrhosis under all liver disease, drug use disorders under substance misuse. "
             f"Removing HIV and tuberculosis, whose American burden is a fraction of their world "
             f"burden, leaves {md['n']} rows and raises the slope only to t = {md['t'][1]:.2f} "
             f"with adjusted R squared {md['adj_r2']:.3f}. Blue and amber as in the previous "
             f"chart.",
             y=-0.03)
    save(fig, "tf-3-money-against-damage.png")


# ------------------------------------------------------------------ 4. the synthesis

def chart4():
    """Three domains, three windows, one absence.

    The empty slot in the AI row is an absence of data and must never read as a zero. It is
    drawn as a hatched outline with its reason printed inside it, and it carries no bar.
    """
    rows = R["synthesis"]
    fig, ax = plt.subplots(figsize=(11.8, 5.4))
    h = 0.34
    ticks, labels = [], []

    for i, row in enumerate(rows):
        base = -i * 1.25
        ticks.append(base - h / 2)
        labels.append(f"{row['domain']}\n{row['window']}")

        ax.barh(base, row["input_pct_change"], height=h, color=BLUE, zorder=3)
        ax.text(row["input_pct_change"] * 1.12, base,
                f"{row['input_label']}   {row['input_pct_change']:+,.0f}%",
                va="center", fontsize=9.8, color=INK2)

        y2 = base - h - 0.06
        if row["outcome_pct_change"] is None:
            # NOT a bar. A bar of any length asserts a magnitude, and there is no magnitude to
            # assert. The band spans the entire row, edge to edge, so it reads as "this row is
            # unavailable" rather than as a value that happens to be small.
            ax.axhspan(y2 - h / 2, y2 + h / 2, xmin=0, xmax=1, facecolor=SHADE, alpha=0.55,
                       hatch="///", edgecolor=MUTED, linewidth=0.0, zorder=1)
            # get_yaxis_transform: x in axes fraction, y in data units, so the label sits just
            # inside the left edge whatever the symlog limits end up being.
            ax.text(0.012, y2, f"{row['outcome_label']}, so no bar is drawn on this row",
                    transform=ax.get_yaxis_transform(), ha="left", va="center", fontsize=9.8,
                    color=RED, fontweight="bold", zorder=4,
                    bbox=dict(facecolor=SURFACE, edgecolor="none", pad=2.0))
        else:
            ax.barh(y2, row["outcome_pct_change"], height=h, color=RED, zorder=3)
            ax.text(1.35, y2, f"{row['outcome_label']}   {row['outcome_pct_change']:+,.1f}%",
                    va="center", fontsize=9.8, color=INK2)

    ax.axvline(0, color=BASELINE, lw=1.0, zorder=2)
    ax.set_xscale("symlog", linthresh=1)
    # Lower limit must clear the largest negative bar. At -3 the transport bar was clipped flush
    # against the spine, so a 5.6 percent fall and a 2.0 percent fall rendered nearly the same
    # length. The design doc forbids exactly that on this chart.
    worst = min(r["outcome_pct_change"] for r in rows if r["outcome_pct_change"] is not None)
    ax.set_xlim(worst * 2.6, 300_000)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(
        lambda v, _: "0" if v == 0 else f"{v:,.0f}%"))
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_yticks(ticks, labels, fontsize=10.6)
    ax.set_xlabel("Percent change over the window shown, log scale, blue is what we put in "
                  "and red is what happened to people")
    ax.grid(axis="y", visible=False)
    ax.set_title("Every domain measures its input far better than its result",
                 fontsize=14.5, pad=14)

    footnote(fig,
             "Each row covers a different window and each window is printed with the row; the "
             "three are not comparable to one another and the chart is not drawn as though they "
             "were. Transport: IEA electric car sales share against the number of people killed "
             "on the roads, Our World in Data's annual aggregation of the WHO Global Health "
             "Estimates, which runs slightly below WHO's own published totals. Medicine: "
             "studies first registered on "
             "ClinicalTrials.gov that year, whole registry, against healthy years lost per "
             "100,000 in high-income countries. Artificial intelligence: private investment via "
             "the Stanford AI Index, in constant 2021 dollars. The hatched slot is not a value "
             "of zero, and it does not mean nothing has been measured. Randomised task-level "
             "studies exist, and the AI Index itself carries a population-level estimate of US "
             "consumer surplus with two dated observations, both cited in the post. What does "
             "not exist is an agreed series running year by year alongside the money.", y=-0.05)
    save(fig, "tf-4-the-input-we-count-the-outcome-we-do-not.png")


if __name__ == "__main__":
    chart1()
    chart2()
    chart3()
    chart4()
