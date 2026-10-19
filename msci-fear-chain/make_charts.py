"""Charts for Post 27, the fear chain after MSCI's Standalone proposal tested against Indonesia's own history.

Reads results.json (written by build_analysis.py), so every number drawn or written here comes from the
build. Typed literals are limited to axis limits, layout coordinates and fixed source labels.
Output: charts/mf-N-name.png, each at most 2000 px on its long edge.

Colour has one meaning across the post: blue is the latest episode, amber is "the link's condition is met",
grey is everything else.

House rule: no em or en dashes anywhere, including inside rendered images; axes.unicode_minus is off.
After editing any caption, re-open the PNG and look at it.
"""

import calendar
import json
import os
import textwrap

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

BASE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(BASE, "results.json")))
META, RULES, LINKS, SENS = R["meta"], R["rules"], R["links"], R["sensitivity"]
EPISODES, SLIDES, OCT = R["episodes"], R["slides"], R["october_2026"]

BLUE, AMBER = "#2a78d6", "#e8890c"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
PAST = "#a9a79f"
WRAP = 150

NONCOMMERCIAL = "Non-commercial use."
SRC_RUPIAH = ("Rupiah per US dollar: Bank for International Settlements, US dollar exchange rates (national sources: "
              "US Federal Reserve, then European Central Bank); month-end values and the index calculated by the author.")
SRC_RUPIAH_SLIDES = SRC_RUPIAH.replace(" and the index", "")
SRC_BOP = "Flows: International Monetary Fund, Balance of Payments statistics; sums calculated by the author."
SRC_CPI = ("Prices: International Monetary Fund, Consumer Price Index (headline index, compiled by BPS-Statistics "
           "Indonesia); inflation calculated by the author.")

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
    fig.text(0.0, y, textwrap.fill(" ".join(text.split()), WRAP, break_on_hyphens=False), ha="left", va="top", fontsize=8.4, color=MUTED)


def month_label(iso: str) -> str:
    return f"{calendar.month_abbr[int(iso[5:7])]} {iso[:4]}"


def month_long(iso: str) -> str:
    return f"{calendar.month_name[int(iso[5:7])]} {iso[:4]}"


def day_long(iso: str) -> str:
    return f"{int(iso[8:10])} {calendar.month_name[int(iso[5:7])]} {iso[:4]}"


def pct0(share: float) -> str:
    return f"{share * 100:.0f}%"


def shock_definition() -> str:
    return (f"An IHSG shock month: a month-end close at least {pct0(RULES['shock_used'])} below the previous "
            f"month-end; a shock within {RULES['shock_cluster_months']} months of an earlier one joins its episode.")


def slide_definition() -> str:
    return (f"A rupiah slide: a month-end rate at least {pct0(RULES['slide_used'])} weaker against the US dollar than "
            f"{RULES['slide_span_months']} months earlier, after the rupiah's float in {month_long(META['float_month'])}; "
            f"slides within {RULES['slide_cluster_months']} months of an earlier one join its episode.")


def latest_note(key: str, why: str) -> str:
    ep = EPISODES[-1]
    return f"{month_label(ep['month0'])} is counted here: {why}." if ep[key]["complete"] else ""


def ihsg_source() -> str:
    prelim = META["ihsg_preliminary"]
    span = f"{calendar.month_name[int(prelim[0][5:7])]} to {month_long(prelim[-1])}"
    return (f"IHSG month-end closes: "
            f"Bank Indonesia, SEKI Table III.3, from {month_long(META['bi_first_used'])}; Bapepam, Statistik Pasar "
            f"Modal, {month_long(META['bapepam_first'])} to {month_long(META['bapepam_last'])}; "
            f"{META['n_corrections_idx']} months corrected to IDX Statistics 2007, IDX Statistics 2009 and IDX Monthly "
            f"Statistics April 2021 (Indonesia Stock Exchange, accessed {day_long(META['idx_access'])}) and "
            f"{META['n_corrections_bapepam']} to Bapepam-LK, Statistik Pasar Modal. Bank Indonesia marks {span} as "
            f"preliminary (the last three solid points of the {month_label(EPISODES[-1]['month0'])} line). Its closes for "
            f"{META['bi_old_first_year']} to {META['bi_old_last_year']} are not used: they failed a check against the "
            f"exchange's own figures.")


def spread(labels: list, gap: float) -> list:
    """Nudge end-of-line labels apart vertically: tuples starting with y, sorted by y, min distance gap."""
    out = sorted(labels)
    for i in range(1, len(out)):
        if out[i][0] - out[i - 1][0] < gap:
            out[i] = (out[i - 1][0] + gap, *out[i][1:])
    return out


def lined_up(ax, key: str, link: str, extension: list | None = None, mark_x: int | None = None):
    """Draw each episode's path (key 'stocks' or 'rupiah'), x = months from the shock month. extension: points
    (dicts with x and index) continuing the latest episode past its last month-end, drawn dotted. mark_x: the
    test month, where an amber dot marks each episode that meets the link."""
    ends = []
    latest = EPISODES[-1]["month0"]
    for ep in EPISODES:
        path = {int(k) - 1: v for k, v in ep[key]["path"].items()}
        xs = sorted(path)
        counted = ep["stocks"]["complete"] if link == "L1" else ep[key]["complete"]
        colour, width, z = (BLUE, 2.2, 3) if ep["month0"] == latest else (PAST, 1.4, 2)
        label = month_label(ep["month0"]) + ("" if counted else " (open)")
        ax.plot(xs, [path[x] for x in xs], color=colour, lw=width, zorder=z, solid_capstyle="round")
        end_x, end_y = xs[-1], path[xs[-1]]
        if extension and ep["month0"] == latest:
            ex, ey = [end_x] + [p["x"] for p in extension], [end_y] + [p["index"] for p in extension]
            ax.plot(ex, ey, color=BLUE, lw=1.6, ls=(0, (1.5, 2)), zorder=z, dash_capstyle="round")
            ax.plot(ex[-1], ey[-1], "o", ms=6, mfc=SURFACE, mec=BLUE, mew=1.8, zorder=4)
            end_x, end_y = ex[-1], ey[-1]
            label += f", to {day_long(extension[-1]['date'])[:-5]}"
        met = ep["stocks"]["stays_down"] if link == "L1" else ep[key]["weakens"]
        if mark_x is not None and met and mark_x in path:
            ax.scatter([mark_x], [path[mark_x]], s=42, color=AMBER, edgecolor=SURFACE, linewidth=1.4, zorder=5)
        ends.append((end_y, label, INK if ep["month0"] == latest else INK2, end_x, end_y))
    ax.axhline(100, color=BASELINE, lw=1.0, zorder=1)
    span = ax.get_ylim()[1] - ax.get_ylim()[0]
    for y, text, colour, x, y_end in spread(ends, span * 0.045):
        if abs(y - y_end) > span * 0.005:
            ax.plot([x + 0.05, x + 0.2], [y_end, y], color=PAST, lw=0.6, zorder=1)
        ax.text(x + 0.25, y, text, color=colour, fontsize=8.6, va="center")
    horizon = RULES["horizons"][-1]
    ax.set_xlim(-1.3, horizon + 2.6)
    ax.set_xticks(range(-1, horizon + 1))
    ax.set_xlabel("Months from the shock month (0); minus 1 is the month before, set to 100")


# --- mf-1: markets ------------------------------------------------------------------------------------

def chart_markets():
    l1, l2 = LINKS["L1"], LINKS["L2"]
    horizon, test_m = RULES["horizons"][-1], RULES["horizons"][1]
    test_y = 100 * (1 + RULES["rupiah_weaker"])
    fig, (top, bot) = plt.subplots(2, 1, figsize=(8.0, 8.2), sharex=True, gridspec_kw=dict(hspace=0.24))
    fig.subplots_adjust(top=0.9, bottom=0.07)
    lined_up(top, "stocks", "L1", OCT["latest_extension"], mark_x=horizon)
    lined_up(bot, "rupiah", "L2", OCT["rupiah_extension"], mark_x=test_m)
    top.set_xlabel("")
    top.axvline(horizon, color=MUTED, lw=0.9, ls=(0, (3, 3)), zorder=1)
    bot.hlines(test_y, -1.3, horizon, color=MUTED, lw=0.9, ls=(0, (3, 3)), zorder=1)
    bot.axvline(test_m, color=MUTED, lw=0.9, ls=(0, (3, 3)), zorder=1)
    bot.text(-1.2, test_y, f" {pct0(RULES['rupiah_weaker'])} weaker", color=INK2, fontsize=8.4, va="bottom",
             bbox=dict(fc=SURFACE, ec="none", pad=1), zorder=4)
    top.set_ylabel("IHSG month-end close,\n100 = month before the shock")
    bot.set_ylabel("Rupiah per US dollar, 100 = month before\n(higher means a weaker rupiah)")
    top.set_title(f"Stocks: still below the pre-shock level a year later after {l1['n_meeting']} of {l1['n']}",
                  loc="left")
    bot.set_title(f"The rupiah: {pct0(RULES['rupiah_weaker'])} or more weaker {test_m} months on after "
                  f"{l2['n_meeting']} of {l2['n']}", loc="left")
    fig.legend(handles=[Line2D([], [], color=BLUE, lw=2.2, label=f"{month_label(EPISODES[-1]['month0'])}, this year's episode"),
                        Line2D([], [], color=BLUE, lw=1.6, ls=(0, (1.5, 2)), label="dotted: daily close or rate, not counted"),
                        Line2D([], [], marker="o", ls="", color=AMBER, markersize=7, label="the test is met")],
               loc="lower left", bbox_to_anchor=(0.1, 0.935), ncol=3, frameon=False, fontsize=8.4)
    ext, rext = OCT["latest_extension"], OCT["rupiah_extension"]
    footnote(fig, (f"{shock_definition()} Each line runs from the month before the shock to {horizon} months after "
                   f"it; an open episode is not counted for a test it has not reached. {ihsg_source()} Dotted ends, not "
                   f"from Bank Indonesia: the IHSG close on {day_long(ext[0]['date'])} (OJK, Portal Data "
                   f"SJK Terintegrasi) and on {day_long(ext[-1]['date'])}, placed at its day in the month (IDX Daily "
                   f"Statistics, Indonesia Stock Exchange, idx.co.id, accessed {day_long(META['idx_access'])}); the "
                   f"rupiah on {day_long(rext[-1]['date'])} from the European Central Bank's reference rates. "
                   f"{SRC_RUPIAH} Calculations by the author. {NONCOMMERCIAL}"), y=0.0)
    save(fig, "mf-1-markets.png")


# --- mf-2: foreign flows -------------------------------------------------------------------------------

def chart_flows():
    l3 = LINKS["L3"]
    eps = [ep for ep in EPISODES if ep["flows"]["complete"]]
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    vals = [ep["flows"]["net_usd_bn"] for ep in eps]
    xs = list(range(len(eps)))
    ax.bar(xs, vals, width=0.56, color=[AMBER if v < 0 else PAST for v in vals], zorder=2)
    ax.axhline(0, color=BASELINE, lw=1.0, zorder=1)
    for x, v in zip(xs, vals):
        ax.text(x, v + (0.18 if v >= 0 else -0.18), f"{v:+.1f}", ha="center", va="bottom" if v >= 0 else "top",
                fontsize=9, color=INK)
    lo, hi = min(vals + [0]), max(vals + [0])
    pad = (hi - lo) * 0.14
    ax.set_ylim(lo - pad, hi + pad)
    slot = len(eps)
    ax.text(slot, lo * 0.275, f"{OCT['shock_quarter'][4:]} {OCT['shock_quarter'][:4]}\nnot yet\npublished",
            ha="center", va="center", fontsize=8.4, color=MUTED)
    ax.set_xticks(xs + [slot], [month_label(ep["month0"]) for ep in eps] + [month_label(OCT["shock_day"][:7])])
    ax.set_xlim(-0.6, slot + 0.6)
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("US$ billion, quarter of the shock and the next")
    ax.set_title(f"Foreign investors pulled money out of Indonesian shares around {l3['n_meeting']} of "
                 f"{l3['n']} IHSG shocks", loc="left")
    ax.legend(handles=[Line2D([], [], color=AMBER, lw=7, label="Net outflow"),
                       Line2D([], [], color=PAST, lw=7, label="Net inflow")],
              loc="upper right", frameon=False, fontsize=9)
    footnote(fig, (f"{shock_definition()} Net foreign purchases of Indonesian equities: balance of payments, portfolio "
                   f"investment liabilities, equity and investment fund shares, net incurrence, summed over the quarter "
                   f"that contains the shock month and the next quarter, so each window starts before the shock. A "
                   f"negative value means non-residents cut their holdings through sales, buybacks or fund redemptions. "
                   f"{latest_note('flows', 'both of its quarters are published')} The fall of "
                   f"{day_long(OCT['shock_day'])} is not shown: its quarter is not yet published. {SRC_BOP} "
                   f"{NONCOMMERCIAL}"))
    save(fig, "mf-2-flows.png")


# --- mf-3: prices after rupiah slides -------------------------------------------------------------------

def fuel_cell(w: dict) -> str:
    parts = [f"{n} {word}{'s' if n > 1 else ''}" for n, word in ((w["n_rises"], "rise"), (w["n_cuts"], "cut")) if n]
    return ",\n".join(parts) if parts else "no change\nfound"


def chart_prices():
    l4, pr = LINKS["L4"], R["household"]["prices_rose"]
    fuel = {e["start"]: e for e in R["household"]["fuel"]["episodes"]}
    gap, win = RULES["inflation_gap_pp"], RULES["inflation_window_months"]
    y0, y1 = RULES["outer_bound_years"][0], RULES["outer_bound_years"][-1]
    counted = [s for s in SLIDES if s["complete"] and not s["outer_bound"]]
    outer = [s for s in SLIDES if s["complete"] and s["outer_bound"]]
    fig = plt.figure(figsize=(8.6, 6.0))
    gs = GridSpec(1, 2, width_ratios=[5, 1.25], wspace=0.28, figure=fig)
    ax, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    fig.subplots_adjust(bottom=0.27)

    def dumbbell(axis, slides):
        for i, s in enumerate(slides):
            b, a = s["inflation_before_pct"], s["inflation_after_pct"]
            axis.plot([i, i], [b, a], color=BASELINE, lw=2, zorder=1)
            axis.scatter([i], [b], s=46, facecolor=SURFACE, edgecolor=PAST, linewidth=1.6, zorder=3)
            axis.scatter([i], [a], s=58, color=AMBER if s["rises"] else INK2, zorder=4,
                         edgecolor=SURFACE, linewidth=1.5)
            axis.text(i + 0.14, a, f"{s['gap_pp']:+.1f} pts", fontsize=8.6, va="center", color=INK)
        axis.set_xticks(range(len(slides)), [month_label(s["start"]) for s in slides])
        axis.set_xlim(-0.5, len(slides) - 0.2)
        axis.grid(axis="x", visible=False)

    dumbbell(ax, counted)
    dumbbell(ax2, outer)
    rows = ((-0.17, "before", f"Fuel price changes,\n{win} months to the slide"), (-0.31, "after", f"{win} months after"))
    for y, key, label in rows:
        ax.text(-0.75, y, label, transform=ax.get_xaxis_transform(), ha="right", va="top", fontsize=8.4, color=INK2)
        for i, s in enumerate(counted):
            ax.text(i, y, fuel_cell(fuel[s["start"]][key]), transform=ax.get_xaxis_transform(), ha="center",
                    va="top", fontsize=8.4, color=INK)
    ax2.text(0, rows[0][0], "fuel not\nchecked", transform=ax2.get_xaxis_transform(), ha="center", va="top",
             fontsize=8.4, color=MUTED)
    top = max(max(s["inflation_before_pct"], s["inflation_after_pct"]) for s in counted)
    ax.set_ylim(top=top * 1.32)
    ax.set_ylabel(f"Consumer price inflation over {win} months, %")
    ax.set_title(f"Inflation sped up by {gap:.0f} percentage points or more after {l4['n_meeting']} of {l4['n']}\n"
                 f"rupiah slides; prices rose after {pr['n_meeting']} of {pr['n']}", loc="left")
    if outer:
        ax2.set_title(f"{y0} slide, shown apart\n(not counted)", fontsize=9.5, color=INK2, loc="left",
                      fontweight="normal")
    ax.legend(handles=[Line2D([], [], marker="o", ls="", markerfacecolor=SURFACE, markeredgecolor=PAST,
                              markersize=7, label=f"{win} months to the slide's first month"),
                       Line2D([], [], marker="o", ls="", color=INK2, markersize=7, label=f"{win} months after it"),
                       Line2D([], [], marker="o", ls="", color=AMBER, markersize=7,
                              label=f"{win} months after, {gap:.0f} percentage points or more higher")],
              loc="upper right", frameon=False, fontsize=8.6)
    met = RULES["slide_counts"][str(RULES["slide"])]
    with_outer = SENS["L4_with_outer_bound"]
    footnote(fig, (f"{slide_definition()} The pre-registered threshold was {pct0(RULES['slide'])}; {met} episodes "
                   f"starting after {y1} met it, fewer than {RULES['min_episodes']}, so the rule's fallback of "
                   f"{pct0(RULES['slide_fallback'])} applies. The {y0} slide is shown apart and not counted: it combined a "
                   f"banking crisis with the end of the managed rupiah; with it included, {with_outer['n_meeting']} of "
                   f"{with_outer['n']}. Inflation: change in the headline consumer price index over the {win} months up "
                   f"to the slide's first month and over the {win} months after it; pts: percentage points. Fuel price "
                   f"changes: changes in the government-set retail price of Premium gasoline or Solar diesel, among those "
                   f"verified in the regulations and official notices; from {R['household']['fuel']['premium_regional_from_year']} "
                   f"the Premium price the government set applied outside Java, Madura and Bali. Kerosene, LPG, electricity and other fuels are not covered. "
                   f"{SRC_CPI} {SRC_RUPIAH_SLIDES} {NONCOMMERCIAL}"), y=0.0)
    save(fig, "mf-3-prices.png")


# --- mf-4: savings and loans after rupiah slides ----------------------------------------------------------

def bars(ax, xs, vals, met, fmt):
    ax.bar(xs, vals, width=0.56, color=[AMBER if m else PAST for m in met], zorder=2)
    ax.axhline(0, color=BASELINE, lw=1.0, zorder=1)
    span = max(vals + [0]) - min(vals + [0])
    for x, v in zip(xs, vals):
        ax.text(x, v + span * (0.03 if v >= 0 else -0.03), fmt(v), ha="center", va="bottom" if v >= 0 else "top",
                fontsize=9, color=INK)
    ax.set_ylim(min(vals + [0]) - span * 0.18, max(vals + [0]) + span * 0.18)
    ax.grid(axis="x", visible=False)


def chart_savings_loans():
    h = R["household"]
    l5, l6, hr = h["L5"], h["L6"], h["rules"]
    r5 = [r for r in l5["episodes"] if r["complete"] and not r["outer_bound"]]
    r6 = [r for r in l6["episodes"] if r["complete"] and not r["outer_bound"]]
    if [r["start"] for r in r5] != [r["start"] for r in r6]:
        raise SystemExit("chart 4: the savings and loans panels must show the same slides")
    xs = list(range(len(r5)))
    fig, (top, bot) = plt.subplots(2, 1, figsize=(8.0, 7.4), sharex=True, gridspec_kw=dict(hspace=0.34))
    bars(top, xs, [r["real_net_pct"] for r in r5], [r["loses"] for r in r5], lambda v: f"{v:+.1f}%")
    bars(bot, xs, [r["change_pp"] for r in r6], [r["dearer"] for r in r6], lambda v: f"{v:+.1f}")
    bot.axhline(hr["loan_rise_pp"], color=MUTED, lw=0.9, ls=(0, (3, 3)), zorder=1)
    bot.text(len(xs) - 0.55, hr["loan_rise_pp"], f"{hr['loan_rise_pp']:.0f} point higher", ha="right", va="bottom",
             fontsize=8.4, color=INK2)
    bot.set_xticks(xs, [month_label(r["start"]) for r in r5])
    bot.set_xlabel("Rupiah slide (first month)")
    top.set_ylabel(f"Buying power after {hr['deposit_months']} months, %\n(negative: prices rose faster)")
    bot.set_ylabel(f"Change in the rate over\n{hr['deposit_months']} months, percentage points")
    top.set_title(f"Savers: a one-month deposit, after tax, lost buying power after {l5['verdict']['n_meeting']} of "
                  f"{l5['verdict']['n']} slides", loc="left")
    bot.set_title(f"Borrowers: the consumer-loan rate was {hr['loan_rise_pp']:.0f} point or more higher a year later "
                  f"after {l6['verdict']['n_meeting']} of {l6['verdict']['n']}", loc="left")
    footnote(fig, (f"{slide_definition()} Savers: a one-month rupiah time deposit at commercial banks as a whole (Bank "
                   f"Indonesia, SEKI Table I.28), rolled over each month for the {hr['deposit_months']} months after the "
                   f"slide month, after the {pct0(hr['deposit_tax'])} final tax on its interest, against consumer prices "
                   f"over the same months; buying power is the deposit's end value in the slide month's prices against its "
                   f"start value. Borrowers: the average rate on rupiah consumer loans at commercial banks as a whole (SEKI Table "
                   f"I.26), {hr['deposit_months']} months after the slide month against the slide month. Bank Indonesia's "
                   f"tables do not say whether the rates are weighted averages or cover new or existing balances. Savings "
                   f"accounts, longer deposits, other assets and loans outside banks are not covered. Rates credited to "
                   f"Bank Indonesia. {SRC_CPI} {SRC_RUPIAH_SLIDES} {NONCOMMERCIAL}"), y=0.0)
    save(fig, "mf-4-savings-loans.png")

if __name__ == "__main__":
    os.makedirs(os.path.join(BASE, "charts"), exist_ok=True)
    chart_markets()
    chart_flows()
    chart_prices()
    chart_savings_loans()
