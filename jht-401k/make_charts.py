"""Charts for Post 28, JHT and the 401(k).

Reads results.json (written by build_analysis.py), so every number drawn or written here comes from the build.
Typed literals are limited to axis limits, layout coordinates and fixed source labels.
Output: charts/jh-N-name.png, each at most 2000 px on its long edge.

Colour has one meaning across the post: orange is JHT, blue the S&P 500 fund, aqua the 90/10 mix (the dataviz
reference palette's slots 2, 1 and 3, validated for colour-blind separation; aqua's low contrast is why every line
carries a direct label). Bars that split worker and employer use two steps of one neutral blue.

House rule: no em or en dashes anywhere, including inside rendered images; axes.unicode_minus is off.
After editing any caption, re-open the PNG and look at it.
"""

import json
import os
import textwrap

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BASE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(BASE, "results.json")))
G, YBY, CONTRIB, PUB = R["growth"], R["year_by_year"], R["contributions"], R["published"]

ORANGE, BLUE, AQUA = "#eb6834", "#2a78d6", "#1baf7a"
EMPLOYER, WORKER = "#2a78d6", "#9ec5f4"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
NEUTRAL = "#a9a79f"
WRAP = 150

NONCOMMERCIAL = "Non-commercial use."
SRC_JHT = ("JHT rates: PT Jamsostek and BPJS Ketenagakerjaan (each rate's page is in "
           "docs/jht-manifest.csv).")
SRC_IDN_CPI = ("Indonesian prices: International Monetary Fund, Consumer Price Index (headline index, compiled by "
               "BPS-Statistics Indonesia); BPS's published December inflation from Bank Indonesia's Data Inflasi.")
SRC_US = ("US returns: Aswath Damodaran, Historical Returns on Stocks, Bonds and Bills (S&P 500 with dividends; "
          "10-year US Treasury bond); US prices: International Monetary Fund, Consumer Price Index.")

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


def save(fig, name):
    fig.savefig(os.path.join(BASE, "charts", name), dpi=200, bbox_inches="tight", pad_inches=0.15,
                facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def footnote(fig, text, y=-0.02):
    fig.text(0.0, y, textwrap.fill(" ".join(text.split()), WRAP, break_on_hyphens=False), ha="left", va="top",
             fontsize=8.4, color=MUTED)


def signed1(x: float) -> str:
    return f"{x:+.1f}".replace("-", "minus ") if x < 0 else f"{x:+.1f}"


def chart_growth():
    """Chart 1 (R2 to R5): each line's real balance over the real money put in, at the end of each year."""
    rules = G["rules"]
    years = list(range(rules["first_year"], rules["last_year"] + 1))
    series = [("sp500", "S&P 500 fund", BLUE, "-"), ("mix_90_10", "90/10 mix", AQUA, "-"),
              ("jht", "JHT", ORANGE, "-"), ("jht_base_only", "JHT, base rate alone", ORANGE, (0, (3, 2)))]
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    ax.axhline(1, color=BASELINE, lw=1.0, zorder=1)
    ends = []
    for key, label, colour, style in series:
        ys = [G[key]["path"][str(y)] for y in years]
        ax.plot(years, ys, color=colour, lw=2.2 if style == "-" else 1.6, ls=style, zorder=3)
        ends.append((ys[-1], f"{label} {G[key]['multiple']:.1f}x", colour))
    # direct labels at the right edge, nudged apart where two ends nearly touch
    ends.sort()
    placed = []
    for y, text, colour in ends:
        y_text = max(y, placed[-1] + 0.09) if placed else y
        placed.append(y_text)
        ax.annotate(text, (years[-1], y), (years[-1] + 0.35, y_text), color=INK2, fontsize=9.6, va="center",
                    arrowprops=dict(arrowstyle="-", color=colour, lw=1.0))
        ax.plot([years[-1]], [y], "o", color=colour, ms=5, zorder=4)
    ax.set_xlim(years[0] - 0.3, years[-1] + 4.6)
    ax.set_xticks(years[::3])
    ax.set_ylabel("Real balance per unit of real money put in")
    ax.set_title(f"The same yearly saving, {years[0]} to {years[-1]}, each in its own currency after its own "
                 "inflation", loc="left")
    ax.text(years[-1], 1.0, "1 = got back exactly what was put in ", color=MUTED, fontsize=8.6, va="bottom", ha="right")
    footnote(fig, (
        "Each year the saver puts in the same real amount, raised by that country's annual-average consumer price "
        "index, in the middle of the year; each line credits the year's rate on the opening balance and half of it "
        "on the year's money. Balances are valued in December prices of the same year. JHT: the "
        "rate set for member balances (2015: the year-end rate BPJS reported; reading "
        f"{PUB['last_credited_year']}'s figure as the rate for balances is an inference), with the incentives of 2008 and 2009 "
        "and the payouts of 2013; the dashed line leaves those out. S&P 500 fund and the 90/10 mix "
        f"({rules['stock_pct']:.0f}% S&P 500, {rules['bond_pct']:.0f}% 10-year Treasury bond, rebalanced yearly): returns less a "
        f"{rules['fee_pct']:.2f}% yearly fee. Not financial advice; "
        "a stock fund can fall sharply in a year, and the savers face different currencies and risks. "
        f"{SRC_JHT} {SRC_IDN_CPI} {SRC_US} Calculations by the author. {NONCOMMERCIAL}"), y=0.0)
    save(fig, "jh-1-growth.png")


def chart_year_by_year():
    """Chart 2 (R6, A1): JHT's rate after Indonesian inflation each year, against both inflation measures."""
    rows = YBY["rows"]
    years = sorted(rows, key=int)
    xs = [int(y) for y in years]
    imf = [rows[y]["real_imf_pct"] for y in years]
    bps = [rows[y]["real_bps_pct"] for y in years]
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ax.axhline(0, color=INK2, lw=0.9, zorder=2)
    ax.bar(xs, imf, width=0.62, color=ORANGE, zorder=3, edgecolor=SURFACE, linewidth=1.0)
    differs = [i for i, y in enumerate(years) if abs(rows[y]["imf_bps_gap_pp"]) >= 0.05]
    ax.plot([xs[i] for i in differs], [bps[i] for i in differs], "o", ms=6.5, color=INK, mfc=SURFACE, mew=1.5,
            zorder=4)
    for i, v in enumerate(imf):
        if v < 0:
            ax.text(xs[i] + 0.38, v / 2, signed1(v), ha="left", va="center", fontsize=9.2, color=INK2)
    ax.set_xticks(xs[::3])
    ax.set_ylim(min(min(imf), min(bps)) - 1.0, max(max(imf), max(bps)) + 4.2)
    ax.set_ylabel("Real rate, percent")
    neg = YBY["negative_real_imf"]
    ax.set_title(f"JHT's rate after Indonesian inflation: below zero in {neg['n']} of {YBY['n']} years",
                 loc="left")
    handles = [Line2D([], [], color=ORANGE, lw=8, label="the year's JHT rate after December-to-December inflation "
                                                         "(IMF index)"),
               Line2D([], [], marker="o", ls="", color=INK, mfc=SURFACE, mew=1.5, ms=6.5,
                      label="the same, against BPS's published December inflation")]
    ax.legend(handles=handles, loc="upper right", frameon=False, fontsize=8.6)
    footnote(fig, (
        "Real rate: (1 + the year's JHT rate) divided by (1 + that year's December-to-December inflation), less 1. "
        "The JHT rate is the base rate set for member balances, without the 2009 incentive; 2015 is the year-end "
        f"rate BPJS reported, and reading {PUB['last_credited_year']}'s figure as the rate for balances is an inference. "
        "The IMF's linked index and BPS's published December inflation differ in a few years. "
        f"{SRC_JHT} {SRC_IDN_CPI} Calculations by the author. {NONCOMMERCIAL}"), y=0.0)
    save(fig, "jh-2-jht-real.png")


def chart_contributions():
    """Chart 3 (R7): what goes in, worker and employer."""
    k401 = CONTRIB["k401"]
    rows = [(f"CPF, Singapore (aged {CONTRIB['cpf']['max_age']} and under)", CONTRIB["cpf"]),
            (f"401(k), Vanguard plans ({k401['year']})", k401),
            ("JHT, Indonesia", CONTRIB["jht"]),
            ("JP, Indonesia (a pension)", CONTRIB["jp"])]
    fig, ax = plt.subplots(figsize=(8.0, 3.9))
    for i, (label, r) in enumerate(rows):
        ax.barh(i, r["worker_pct"], color=WORKER, height=0.56, edgecolor=SURFACE, linewidth=1.5, zorder=3)
        ax.barh(i, r["employer_pct"], left=r["worker_pct"], color=EMPLOYER, height=0.56, edgecolor=SURFACE,
                linewidth=1.5, zorder=3)
        ax.text(r["total_pct"] + 0.5, i, f"{r['total_pct']:g}%", va="center", fontsize=9.6, color=INK2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, max(r["total_pct"] for _, r in rows) + 7)
    ax.set_xlabel("Contribution rate, percent")
    ax.set_title("Contribution rates each year, worker and employer", loc="left")
    ax.legend(handles=[Line2D([], [], color=WORKER, lw=8, label="worker"),
                       Line2D([], [], color=EMPLOYER, lw=8, label="employer")],
              loc="lower right", frameon=False, fontsize=9)
    footnote(fig, (
        "JHT and JP: the rates the regulations set (PP 46/2015 Pasal 16; PP 45/2015 Pasal 28). 401(k): Vanguard, "
        f"How America Saves 2026, plans Vanguard keeps records for, {k401['year']}, among participants: the average deferral rate as the "
        "worker share, and the average total contribution rate less that as the employer share (a difference of two "
        "averages). 401(k) deferrals are optional. CPF: CPF Board contribution rates "
        f"in force on 1 January 2026 for wages in the top band, the same for each age group up to {CONTRIB['cpf']['max_age']} (data.gov.sg, "
        "Singapore Open Data Licence, data.gov.sg/open-data-licence). JP is a separate pension scheme. Calculations by the "
        "author. Non-commercial use."), y=-0.06)
    save(fig, "jh-3-contributions.png")


def chart_shown():
    """Chart 4 (R8): what BPJS publishes each year: the fund's investment yield, and the rate for balances."""
    rows = PUB["rows"]
    years = sorted(rows, key=int)
    xs = [int(y) for y in years]
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ys = [rows[y]["yield_pct"] for y in years]
    ax.bar([x for x, v in zip(xs, ys) if v is not None], [v for v in ys if v is not None], width=0.62,
           color=NEUTRAL, zorder=2, edgecolor=SURFACE, linewidth=1.0)
    credited = {y: R["year_by_year"]["rows"].get(y, {}).get("rate_pct") for y in years if rows[y]["credited_published"]}
    ax.plot([int(y) for y in credited], list(credited.values()), "o", ms=8, color=ORANGE, mec=SURFACE, mew=1.5,
            zorder=4)
    gap = PUB["years_without_credited"]
    if gap:
        ax.axvspan(gap[0] - 0.45, gap[-1] + 0.45, color=GRID, alpha=0.55, zorder=1, lw=0)
        ax.text((gap[0] + gap[-1]) / 2, 1.0, "rate for balances\nnot published", ha="center", va="bottom",
                fontsize=9.4, color=INK2, zorder=5)
    ax.set_xticks(xs)
    ax.tick_params(axis="x", labelsize=9)
    ax.set_ylim(0, max(v for v in ys if v is not None) + 2.5)
    ax.set_ylabel("Percent")
    ax.set_title(f"BPJS publishes what the JHT fund earns; the rate for balances is not published after "
                 f"{PUB['last_credited_year']}", loc="left")
    ax.legend(handles=[Line2D([], [], color=NEUTRAL, lw=8, label="the JHT fund's investment yield, as published"),
                       Line2D([], [], marker="o", ls="", color=ORANGE, ms=8, label="the rate set for member balances")],
              loc="upper right", frameon=False, fontsize=8.8)
    missing = [y for y in years if rows[y]["yield_pct"] is None]
    footnote(fig, (
        "Yields: the JHT program's investment yield in BPJS's annual and integrated reports, as each report states "
        "it; the basis is labelled gross in the first of these reports, net in the last three, and not labelled in between. "
        + (f"No searchable report gives a yield for {', '.join(missing)}. " if missing else "")
        + "Rate for balances: the rate set each year for member balances (2015: the year-end rate BPJS reported; "
        f"reading {PUB['last_credited_year']}'s figure as the rate for balances is an inference). "
        f"{SRC_JHT} {NONCOMMERCIAL}"), y=0.0)
    save(fig, "jh-4-shown.png")


if __name__ == "__main__":
    os.makedirs(os.path.join(BASE, "charts"), exist_ok=True)
    chart_growth()
    chart_year_by_year()
    chart_contributions()
    chart_shown()
