"""Charts for Post 22, 'Reading Part of One Sentence Counts as Literate'.

Reads results.json. Output: charts/lit-N-name.png.

Every number drawn or written here is interpolated from results.json. Typed literals are limited
to axis limits, layout coordinates, and the names of countries the post calls out.

House rule: no em or en dashes anywhere, including inside rendered images. matplotlib writes a
Unicode minus on negative ticks unless axes.unicode_minus is False.

After editing any caption, RE-OPEN THE PNG and look at it. On Posts 20 and 21 a fact-check round
found a caption that had gone stale while the code looked fine, three times.
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

# The four bands of a published literacy rate, in the order they are stacked. The first three
# sum to the headline; the fourth is what is left. Colour carries the argument: amber is an
# exemption rather than a result, red is the threshold nobody expects.
BANDS = [
    ("above_secondary_not_tested", AMBER, "Never tested: above secondary education"),
    ("read_whole_sentence", BLUE, "Read a whole sentence"),
    ("read_part_of_sentence", RED, "Read only PART of a sentence"),
    ("cannot_read_at_all", SHADE, "Cannot read at all"),
]


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def footnote(fig, text, y=-0.02):
    fig.text(0.0, y, text, ha="left", va="top", fontsize=8.6, color=MUTED, wrap=True)


def chart1_what_literate_is_made_of():
    """The rule, drawn.

    A reader should be able to find, for any country, the point on the bar where the survey
    stopped asking and started assuming. The amber segment is not a measurement.
    """
    rows = R["composition"]["countries"]
    labels = [r["country"] for r in rows]
    y = np.arange(len(rows))[::-1]

    fig, ax = plt.subplots(figsize=(11.2, 12.4))
    left = np.zeros(len(rows))
    for key, colour, label in BANDS:
        w = np.array([r[key] for r in rows])
        ax.barh(y, w, left=left, color=colour, height=0.7, label=label,
                edgecolor=SURFACE, linewidth=0.6)
        left += w

    # The headline rate at the end of each bar, which is the sum of the first three bands.
    for i, r in enumerate(rows):
        ax.text(101.5, y[i], f"{r['literate_published']:.1f}", va="center",
                fontsize=8.6, color=INK2)
    ax.text(101.5, len(rows) + 0.2, "literate", va="center", fontsize=8.6, color=INK2,
            fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9.2)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percent of women age 15 to 49")
    ax.set_title("What a literacy rate is actually made of", pad=14)
    ax.grid(axis="y", visible=False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.045), ncol=2, frameon=False,
              fontsize=9.4)

    c = R["composition"]
    med = c["medians"]
    nc = c["no_card_in_language"]
    most = c["most_part_of_sentence"][0]
    # The largest band in POINTS and the largest as a SHARE of the literate population are two
    # different countries. Round 1 caught the footnote quoting both metrics in one sentence.
    _bs = max(c["countries"], key=lambda x: x["read_part_of_sentence"] / x["literate_published"])
    by_share = {"country": _bs["country"],
                "share": round(100 * _bs["read_part_of_sentence"] / _bs["literate_published"], 1)}
    footnote(fig,
             f"The DHS Program, latest survey per country among the {c['n_countries']} using the "
             "current coding rule, women age 15 to 49. Published weighted percentages, not "
             "recomputed from microdata.\n"
             "The first three bands sum to the published literacy rate. The amber band is not a "
             "test result: respondents with more than secondary education are never handed the "
             "card, so for them the indicator has no way to record that someone cannot read.\n"
             f"Column medians across these countries, each computed separately and NOT the profile "
             f"of any one country: {med['above_secondary_not_tested']} percent never tested, "
             f"{med['read_whole_sentence']} read a whole sentence, {med['read_part_of_sentence']} "
             f"read only part of one, {med['cannot_read_at_all']} cannot read at all. They do not "
             "sum to 100, and the first three do not sum to the median published rate.\n"
             f"{most['country']} has the largest partial-reading band in absolute terms, "
             f"{most['read_part_of_sentence']} of its {most['literate_published']} points. Measured "
             f"as a share of the literate population the extreme is {by_share['country']}, at "
             f"{by_share['share']} percent.\n"
             "The instrument errs downward too, and this chart shows it only as a sliver. Where "
             "the interviewer had no card in the respondent's language the respondent is counted "
             f"as NOT literate; that is {nc['median']} percent at the median and above one "
             f"percent in {nc['n_countries_above_1pct']} of these countries. Blind respondents "
             "and missing values are also inside the residual.",
             y=-0.052)
    save(fig, "lit-1-what-literate-is-made-of.png")


def chart2_the_year_the_instrument_changed():
    """What happened when DHS started handing the card to more people.

    Drawn as composition, not as a trend line, because a trend line across the rule change would
    compare two different instruments. That is the exact thing DHS warns against.
    """
    countries = R["rule_change"]["countries"]
    names = [c for c in ["Ghana", "India", "Indonesia", "Nigeria"] if c in countries]

    fig, axes = plt.subplots(1, len(names), figsize=(14.6, 5.6), sharey=True)
    for ax, name in zip(axes, names):
        v = countries[name]
        pair = [v["last_old_rule"], v["latest_new_rule"]]
        x = np.arange(2)
        bottom = np.zeros(2)
        for key, colour, label in BANDS:
            h = np.array([p[key] for p in pair])
            ax.bar(x, h, bottom=bottom, color=colour, width=0.62, edgecolor=SURFACE,
                   linewidth=0.8, label=label if name == names[0] else None)
            bottom += h

        for i, p in enumerate(pair):
            ax.text(i, p["literate_published"] + 2.0, f"{p['literate_published']:.1f}",
                    ha="center", fontsize=10, fontweight="bold",
                    color=RED if name == "Ghana" else INK)
        ax.set_xticks(x)
        ax.set_xticklabels([f"{p['year']}\n{'old rule' if i == 0 else 'current rule'}"
                            for i, p in enumerate(pair)], fontsize=9.4)
        ax.set_title(name, fontsize=11.5, pad=8)
        ax.set_ylim(0, 100)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("Percent of women age 15 to 49")
    fig.legend(loc="lower center", bbox_to_anchor=(0.5, -0.10), ncol=4, frameon=False,
               fontsize=9.4)
    fig.suptitle("The year the instrument changed, not the year the reading changed",
                 fontsize=13.5, fontweight="bold", y=1.02)

    gh = countries["Ghana"]
    rc = R["rule_change"]
    footnote(fig,
             "The DHS Program. Left bar in each panel is that country's last survey under the "
             "rule that exempted everyone with secondary education or above; right bar is its "
             "latest survey under the current rule, which exempts only those above secondary. "
             f"{rc['n_old_rule']} surveys use the old rule and {rc['n_new_rule']} the current one, "
             "and the two overlap in time, so they are separated by comparing the never-tested "
             "column against both published education shares rather than by year.\n"
             "The number above each bar is the published literacy rate. In all four countries the "
             "amber never-tested band collapses, because people who were previously assumed "
             "literate are now asked to read.\n"
             f"Ghana is the clean case: between {gh['last_old_rule']['year']} and "
             f"{gh['latest_new_rule']['year']} the share of Ghanaian women with secondary or "
             f"higher education ROSE from {gh['last_old_rule']['secondary_or_higher']} to "
             f"{gh['latest_new_rule']['secondary_or_higher']} percent, while measured literacy "
             f"FELL from {gh['last_old_rule']['literate_published']} to "
             f"{gh['latest_new_rule']['literate_published']}. The other three rose. Real schooling "
             "grew over their gaps as well, and in each of the three the schooling gain is larger "
             "than the literacy gain it would have to explain, so the rule change and the "
             "schooling cannot be separated in those three panels. The rule "
             "change moves the composition everywhere; it decides the headline only in Ghana.\n"
             "DHS states the problem itself: estimates from earlier surveys may overestimate "
             "literacy relative to DHS-7 and DHS-8, and care should be taken in interpreting "
             "trends.",
             y=-0.13)
    save(fig, "lit-2-the-year-the-instrument-changed.png")


def chart3_how_the_numbers_are_made():
    """Where literacy statistics come from at all."""
    h = R["how_measured"]
    order = ["Self-reported (head of household)", "Self-reported (individual)",
             "Literacy test", "Indirect estimate", "No data"]
    order = [k for k in order if k in h["counts"]]
    vals = [h["counts"][k] for k in order]
    colours = [RED, AMBER, BLUE, MUTED, SHADE][:len(order)]
    y = np.arange(len(order))[::-1]

    fig, ax = plt.subplots(figsize=(11.0, 4.4))
    ax.barh(y, vals, color=colours, height=0.66, edgecolor=SURFACE, linewidth=0.6)
    for i, v in enumerate(vals):
        ax.text(v + 5, y[i], f"{v}", va="center", fontsize=10, fontweight="bold", color=INK2)
    ax.set_yticks(y)
    ax.set_yticklabels(order, fontsize=10)
    ax.set_xlim(0, max(vals) * 1.16)
    ax.set_xlabel("Country-years")
    ax.set_title("How the world's literacy statistics are actually produced", pad=14)
    ax.grid(axis="y", visible=False)

    footnote(fig,
             f"UNESCO Institute for Statistics, via Our World in Data. {h['n_country_years']} "
             f"country-years across {h['n_countries']} countries, {h['years'][0]} to "
             f"{h['years'][1]}.\n"
             f"Of the {h['n_country_years_with_a_method']} country-years with a recorded method, "
             f"{h['tested_share_pct']} percent come from an actual literacy test. "
             f"{h['self_reported_share_pct']} percent are self-reported, and "
             f"{h['proxy_share_pct']} percent of the total are reported by the head of the "
             "household on behalf of everyone in it, including adults who were never asked "
             "themselves.\n"
             "This chart counts country-years, not people, so a country reporting often weighs "
             "more here than one reporting once.",
             y=-0.16)
    save(fig, "lit-3-how-the-numbers-are-made.png")


def chart4_who_is_asked_to_prove_it():
    """Who gets tested, plotted against the literacy level their method produced."""
    mv = R["method_vs_level"]
    order = [m for m in ["Literacy test", "Self-reported (head of household)",
                         "Self-reported (individual)", "Indirect estimate"]
             if m in mv["by_method"]]
    colours = {"Literacy test": BLUE, "Self-reported (head of household)": RED,
               "Self-reported (individual)": AMBER, "Indirect estimate": MUTED}

    fig, ax = plt.subplots(figsize=(11.4, 5.2))
    rng = np.random.default_rng(11)
    for i, m in enumerate(order):
        v = mv["by_method"][m]
        xs = [c["literacy"] for c in v["countries"]]
        ys = np.full(len(xs), i, dtype=float) + rng.uniform(-0.17, 0.17, len(xs))
        ax.scatter(xs, ys, s=34, c=colours[m], alpha=0.75, linewidths=0, zorder=3)
        ax.plot([v["median_literacy"]] * 2, [i - 0.32, i + 0.32], color=INK, lw=2.2, zorder=4)
        ax.text(v["median_literacy"], i + 0.40, f"median {v['median_literacy']:.1f}",
                ha="center", fontsize=8.8, color=INK)

    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([f"{m}\n(n = {mv['by_method'][m]['n']})" for m in order], fontsize=9.6)
    ax.set_ylim(-0.7, len(order) - 0.3)
    ax.set_xlim(15, 102)
    ax.set_xlabel("Adult literacy rate the method produced, percent")
    ax.set_title("Who is asked to prove it", pad=14)
    ax.grid(axis="y", visible=False)
    ax.invert_yaxis()

    test = mv["by_method"]["Literacy test"]
    ind = mv["by_method"]["Self-reported (individual)"]
    eur = R["who_is_tested"]["europe"]
    # The footnote hardcodes "two" and "Andorra" beside data-driven joins. Assert rather than hope:
    # a hardcoded European fact is exactly what round 1 refuted here.
    assert len(eur["ever_tested"]) == 2 and list(eur["other"]) == ["Andorra"], eur
    footnote(fig,
             f"Each of {mv['n_countries']} countries plotted once, at its most recently recorded "
             "reporting method against the UNESCO adult literacy rate nearest that year. "
             "Reporting method from UNESCO Institute for Statistics, Methodologies used for "
             "measuring literacy (2017); literacy rates from UNESCO Institute for Statistics via "
             "the World Bank. Both compiled by Our World in Data.\n"
             f"Countries whose rate came from a literacy test sit at a median of "
             f"{test['median_literacy']} percent; those where individuals were asked to describe "
             f"their own literacy sit at {ind['median_literacy']}.\n"
             "That gap has two readings and this chart cannot separate them: testing may be "
             "applied where literacy is already doubted, and testing may also return lower "
             "numbers than asking. Neither is established here.\n"
             f"Of the {eur['n_in_file']} European countries in the file, "
             f"{eur['n_self_declared_only']} have only ever self-declared and Andorra reports an "
             f"indirect estimate. {' and '.join(eur['ever_tested'])} are the only two ever recorded "
             "testing; Italy, Spain, Portugal, Greece, Poland and Russia are all self-declared. "
             "Those that do appear on the tested list include Chad, Niger, Sierra Leone, Malawi "
             "and Haiti.\n"
             f"{mv['n_dropped_for_no_literacy_value']} of the "
             f"{mv['n_countries_with_a_method']} countries with a recorded method are absent from "
             "this chart because no literacy rate could be matched to them.",
             y=-0.085)
    save(fig, "lit-4-who-is-asked-to-prove-it.png")


if __name__ == "__main__":
    (BASE / "charts").mkdir(exist_ok=True)
    chart1_what_literate_is_made_of()
    chart2_the_year_the_instrument_changed()
    chart3_how_the_numbers_are_made()
    chart4_who_is_asked_to_prove_it()
