"""Charts for Post 29, the house chase.

Reads results.json (written by build_analysis.py), so every number drawn or written here comes from the build.
Typed literals are limited to axis limits, layout coordinates, the month of ChatGPT's release (the stored Yale quote
names it in words) and fixed source labels.
Output: charts/gz-N-name.png, each at most 2000 px on its long edge.

Colour: the dataviz reference palette's categorical slots in their fixed order (blue, orange, aqua, yellow), run
through its validator for adjacent pairs on the light surface: all checks pass; aqua and yellow sit below 3:1
contrast, so every generation and every line carries a direct text label. Generations take the four slots in birth
order, so neighbouring bars are neighbouring slots. The comparison series ("all consumer units", "all workers") are
muted grey and dashed in every chart.

House rule: no em or en dashes anywhere, including inside rendered images; axes.unicode_minus is off.
After editing any caption, re-open the PNG and look at it.
"""

import json
import os
import textwrap

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

BASE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(BASE, "results.json")))
CH, TR, RA, SH, GR = R["chase"], R["treats"], R["ratio"], R["shares"], R["grads"]

BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
WRAP = 150
CHATGPT_MONTH = 11          # November, as the stored quote words it

GENS = (("boomers", "Boomers", BLUE), ("genx", "Gen X", ORANGE), ("millennials", "Millennials", AQUA),
        ("genz", "Gen Z", YELLOW))
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")
NONCOMMERCIAL = "Calculations by the author. Non-commercial use."
SRC_PRICE = ("Home prices: U.S. Census Bureau and U.S. Department of Housing and Urban Development, Survey of "
             "Construction (median sales price of new houses sold, lot included).")
SRC_INCOME = ("Incomes: U.S. Census Bureau, Current Population Survey, Annual Social and Economic Supplement, "
              "Table H-10 (median household income by age of householder, before taxes).")
SRC_BLS = "U.S. Bureau of Labor Statistics, Current Population Survey (copies from the Internet Archive)"

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": BASELINE, "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": INK2,
    "text.color": INK, "axes.titlesize": 11.5, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "font.size": 10.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "text.parse_math": False, "axes.unicode_minus": False,
})


def save(fig, name: str) -> None:
    fig.savefig(os.path.join(BASE, "charts", name), dpi=200, bbox_inches="tight", pad_inches=0.15, facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def footnote(fig, text: str, y: float = -0.02) -> None:
    fig.text(0.0, y, textwrap.fill(" ".join(text.split()), WRAP, break_on_hyphens=False), ha="left", va="top",
             fontsize=8.4, color=MUTED)


def series(stats: dict) -> tuple[list, list]:
    ys = sorted(stats["by_year"], key=int)
    return [int(y) for y in ys], [stats["by_year"][y] for y in ys]


def year_ticks(ax, first: int, last: int) -> None:
    """Ticks at the first year, each decade between, and the last year: none past the data."""
    ax.set_xticks([first] + [y for y in range(first - first % 10 + 10, last - 2, 10)] + [last])


def end_labels(ax, items: list, gap: float) -> None:
    """Direct labels at the right end of each line, nudged apart by at least `gap`, each tied by a thin leader.
    items: [(x, y, text, colour)]."""
    x_text = max(x for x, _, _, _ in items) + 0.9
    placed = []
    for x, y, text, colour in sorted(items, key=lambda i: i[1]):
        y_text = max(y, placed[-1] + gap) if placed else y
        placed.append(y_text)
        ax.plot([x], [y], "o", color=colour, ms=5, zorder=4)
        ax.annotate(text, (x, y), (x_text, y_text), color=INK2, fontsize=9.4, va="center",
                    arrowprops=dict(arrowstyle="-", color=colour, lw=0.8, shrinkA=0, shrinkB=2))


def chart_years_of_pay() -> None:
    """Chart 1 (R11): the median new-home price in years of pay, current dollars over current dollars."""
    hh, sal = RA["household"], RA["salary"]
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    for stats, colour in ((hh, BLUE), (sal, ORANGE)):
        xs, ys = series(stats)
        ax.plot(xs, ys, color=colour, lw=2.2, zorder=3)
        ax.plot([xs[0]], [ys[0]], "o", color=colour, ms=5, zorder=4)
        ax.annotate(f"{stats['first']:.1f}", (xs[0], ys[0]), (xs[0], ys[0] - 0.55), ha="center", fontsize=9.2,
                    color=INK2)
    end_labels(ax, [(sal["last_year"], sal["last"], f"one full-time salary: {sal['last']:.1f} years", ORANGE),
                    (hh["last_year"], hh["last"], f"a young household's income: {hh['last']:.1f} years", BLUE)], 0.5)
    for stats in (hh, sal):
        ax.annotate(f"{stats['max']:.1f} in {stats['max_year']}", (stats["max_year"], stats["max"]),
                    (stats["max_year"] - 3.2, stats["max"] + 0.45), fontsize=8.8, color=INK2)
    ax.set_xlim(hh["first_year"] - 1.5, hh["last_year"] + 17)
    year_ticks(ax, hh["first_year"], hh["last_year"])
    ax.set_ylim(0, sal["max"] + 1.6)
    ax.set_ylabel("Years of pay")
    ax.set_title(f"What the typical new home cost in years of pay, {hh['first_year']} to {hh['last_year']}", loc="left")
    footnote(fig, (
        "Years of pay: the year's median sales price of new houses sold divided by the year's pay, both in current "
        "dollars. A young household: the median income of households whose householder is aged 25 to 34. One "
        f"full-time salary: {RA['weeks']} times the median usual weekly earnings of full-time wage and salary workers "
        f"aged 25 to 34, from {sal['first_year']}. {SRC_PRICE} {SRC_INCOME} Salaries: {SRC_BLS}. {NONCOMMERCIAL}"), y=0.0)
    save(fig, "gz-1-years-of-pay.png")


def chart_chase() -> None:
    """Chart 2 (R2 to R6, R9): years of saving to reach the down payment, by the year the saver turned 25."""
    rules, by = CH["rules"], CH["by_start"]
    starts = sorted(by, key=int)
    colour = {}
    for key, _, c in GENS:
        g = CH["generations"][key]
        colour.update({s: c for s in range(g["first_start"], g["last_start"] + 1)})
    fig, ax = plt.subplots(figsize=(9.6, 5.4))
    for s in starts:
        r, c = by[s], colour[int(s)]
        if r["finished"]:
            ax.bar(int(s), r["years"], width=0.78, color=c, edgecolor=SURFACE, linewidth=1.0, zorder=3)
        else:
            ax.bar(int(s), r["years"], width=0.78, facecolor=SURFACE, edgecolor=c, hatch="////", linewidth=1.0, zorder=3)
    tb = TR["broad"]["by_start"]
    for s in sorted(tb, key=int):
        t = tb[s]["treat"]
        ax.plot(int(s), t["years"], "o", ms=4.6, color=INK, mfc=INK if t["finished"] else SURFACE, mew=1.1, zorder=5)
    for key, name, c in GENS:
        g = CH["generations"][key]
        f = g["finished"]
        if f["n"] == g["n"]:
            text = f"{name}\nmedian {f['median_years']:g} years"
        elif f["n"]:
            text = f"{name}\nmedian {f['median_years']:g} years\nfor the {f['n']} of {g['n']} done"
        else:
            text = f"{name}\nstill saving"
        reach = range(g["first_start"] - (5 if f["n"] == 0 else 0), g["last_start"] + 1)   # the label is wider than Gen Z's bars
        top = max(by[str(s)]["years"] for s in reach)
        ax.text((g["first_start"] + g["last_start"]) / 2, top + 0.6, text, ha="center", va="bottom", fontsize=9.2,
                color=INK2)
    ax.set_ylim(0, max(by[s]["years"] for s in starts) + 4.2)
    ax.set_xlim(int(starts[0]) - 1, int(starts[-1]) + 1)
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("Years of saving")
    ax.set_xlabel("The year the saver turned 25")
    ax.set_title(f"Years to save a {rules['down_pct']:g}% down payment on the typical new home, putting aside "
                 f"{rules['share_pct']:g}% of income", loc="left")
    handles = [Patch(facecolor=MUTED, edgecolor=SURFACE, label="years it took"),
               Patch(facecolor=SURFACE, edgecolor=MUTED, hatch="////", label=f"still saving in {rules['last']}: years so far"),
               Line2D([], [], marker="o", ls="", color=INK, ms=4.6,
                      label="if eating out, entertainment and personal care were saved too")]
    ax.legend(handles=handles, loc="upper left", frameon=False, fontsize=8.8)
    b = TR["broad"]
    footnote(fig, (
        f"Each year from age 25, the saver puts aside {rules['share_pct']:g}% of the median income of households in "
        "their age bracket (25 to 34, then 35 to 44), mid-year, and the balance earns that year's 3-month Treasury bill "
        f"rate, untaxed. The chase ends in the first year the balance reaches {rules['down_pct']:g}% of that year's "
        "median new-home price; chases still running are not projected. Generations by Pew Research Center's birth "
        f"years. Dots, from {b['first_start']}: the same saver also saves the mean spending of consumer units of the "
        "same age on food away from home, entertainment, and personal care products and services (BLS Consumer "
        f"Expenditure Survey; {b['carried_forward_year']} uses the {b['ce_last']} figure); an open dot is still saving. "
        f"{SRC_PRICE} {SRC_INCOME} Interest: Board of Governors of the Federal Reserve System, H.15 (discount basis). "
        f"Spending: U.S. Bureau of Labor Statistics (copies from the Internet Archive). {NONCOMMERCIAL}"), y=0.0)
    save(fig, "gz-2-chase.png")


def chart_treat_share() -> None:
    """Chart 3 (R12): eating out, entertainment and personal care as a share of spending, by age."""
    a, y, raw, sm = SH["all"], SH["age25_34"], SH["under25"], SH["under25_smoothed"]
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    xs, ys = series(raw)
    ax.plot(xs, ys, "o", ms=3.2, color=ORANGE, alpha=0.45, zorder=2)
    for stats, colour, style in ((sm, ORANGE, "-"), (y, BLUE, "-"), (a, MUTED, (0, (4, 2)))):
        xs, ys = series(stats)
        ax.plot(xs, ys, color=colour, lw=2.2 if style == "-" else 1.6, ls=style, zorder=3)
    end_labels(ax, [(sm["last_year"], sm["last"], "under 25 (three-year average; dots: single years)", ORANGE),
                    (y["last_year"], y["last"], f"aged 25 to 34: {y['last']:.1f}%", BLUE),
                    (a["last_year"], a["last"], "all consumer units", MUTED)], 0.42)
    ax.annotate(f"{y['first']:.1f}%", (y["first_year"], y["first"]), (y["first_year"] + 1.2, y["first"] - 0.9),
                fontsize=9.0, color=INK2, arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8, shrinkA=0, shrinkB=2))
    ax.set_xlim(a["first_year"] - 1, a["last_year"] + 16)
    year_ticks(ax, a["first_year"], a["last_year"])
    ax.set_ylim(min(raw["min"], a["min"]) - 0.6, max(raw["max"], sm["max"]) + 0.6)
    ax.set_ylabel("Percent of average annual spending")
    ax.set_title(f"Eating out, entertainment and personal care: a smaller share of spending in {a['last_year']} than "
                 f"in {a['first_year']}", loc="left")
    footnote(fig, (
        "Mean spending of consumer units by the age of the reference person on food away from home, entertainment, "
        "and personal care products and services, as a share of their average annual expenditures. The categories hold "
        f"some necessities too (school meals, toiletries, pet food). The low point in {y['min_year']} is the "
        f"pandemic year; from {a['last_year']}, food away from home includes delivery fees. Source: U.S. Bureau of Labor "
        f"Statistics, Consumer Expenditure Surveys, LABSTAT database (copy from the Internet Archive). {NONCOMMERCIAL}"),
        y=0.0)
    save(fig, "gz-3-treat-share.png")


def chart_recent_grads() -> None:
    """Chart 4 (R14): the NY Fed's monthly rates as published, with the streak and ChatGPT's release as dates."""
    rows = GR["series"]
    xs = [r[0] + (r[1] - 1) / 12 for r in rows]
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    st = GR["streak"]["start"]
    x0 = st[0] + (st[1] - 1) / 12
    ax.axvspan(x0, xs[-1], color=BLUE, alpha=0.07, lw=0, zorder=1)
    ax.plot(xs, [r[3] for r in rows], color=MUTED, lw=1.6, ls=(0, (4, 2)), zorder=3)
    ax.plot(xs, [r[2] for r in rows], color=BLUE, lw=2.0, zorder=4)
    top = max(max(r[2] for r in rows), max(r[3] for r in rows))
    cg = GR["chatgpt_release_year"] + (CHATGPT_MONTH - 1) / 12
    ax.axvline(cg, color=INK2, lw=0.9, ls=":", zorder=2)
    ax.text(cg + 0.2, top + 0.15, f"ChatGPT released,\nNovember {GR['chatgpt_release_year']}", fontsize=8.8,
            color=INK2, va="top")
    ax.annotate(f"recent graduates above\nall workers every month\nsince {MONTHS[st[1] - 1]} {st[0]}",
                (x0 + 0.3, top * 0.62), (x0 - 2.2, top * 0.80), fontsize=8.8, color=INK2, va="center", ha="right",
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    end_labels(ax, [(xs[-1], rows[-1][2], "recent college graduates", BLUE),
                    (xs[-1], rows[-1][3], "all workers", MUTED)], 0.5)
    ax.set_xlim(xs[0] - 0.5, xs[-1] + 8)
    year_ticks(ax, GR["first"][0], GR["last"][0])
    ax.set_ylim(0, top + 0.8)
    ax.set_ylabel("Unemployment rate, percent")
    ax.set_title(f"Unemployment, recent college graduates and all workers, {GR['first'][0]} to {GR['last'][0]}",
                 loc="left")
    e, m = GR["early"], GR["mid"]
    footnote(fig, (
        "Recent college graduates: aged 22 to 27 with a bachelor's degree or higher; all workers: aged 16 to 65; both "
        "leave out people in school. Seasonally adjusted three-month moving averages, as published; the New York Fed "
        f"estimated October 2025, a month the survey skipped. Recent graduates' rate was above the rate for all workers in {e['above']} "
        f"of {e['months']} months from {e['first']} to {e['last']} and in {m['above']} of {m['months']} months from "
        f"{m['first']} to {m['last']}. The ChatGPT line is a date, not a cause. Source: Federal Reserve Bank of New "
        "York, The Labor Market for Recent College Graduates, https://nyfed.org/collegelabor (release of November 2, "
        "2026), plotted as published, with the bank's source line: U.S. Census Bureau and U.S. Bureau of Labor Statistics, "
        "Current Population Survey (IPUMS); not endorsed by the Federal Reserve Bank of New York. ChatGPT's release date: "
        f"Gimbel and others, The Budget Lab at Yale. {NONCOMMERCIAL}"), y=0.0)
    save(fig, "gz-4-recent-grads.png")


if __name__ == "__main__":
    os.makedirs(os.path.join(BASE, "charts"), exist_ok=True)
    chart_years_of_pay()
    chart_chase()
    chart_treat_share()
    chart_recent_grads()
