"""Charts for Post 30: buy, or rent and invest the difference (design section 5).

Reads results.json (written by build_analysis.py), so every number drawn or written here comes from the build. Typed
literals are limited to axis limits, layout coordinates and fixed source labels; no string literal holds a digit.
Output: charts/rb-N-name.png, each at most 2000 px on its long edge.

Colour: the dataviz reference palette's categorical slots in their fixed order (blue, orange, aqua), run through its
validator on the light surface: blue and orange pass every check as a pair; blue, orange and aqua pass all-pairs for
the verdict grid, with aqua below 3:1 contrast, so the grid carries a legend, a label naming the years held beside
each framed row, and each framed row's counts in the footnote.
Rent level A is blue and level B orange in charts 1 and 4; in chart 2 the buyer is blue and the renter orange, with
level B dashed; in chart 3 buy is blue, rent orange and "depends on the rent" aqua.

House rule: no em or en dashes anywhere, including inside rendered images; axes.unicode_minus is off.
After editing any caption, re-open the PNG and look at it.
"""
import json
import os
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "results.json"), encoding="utf-8") as _fh:
    R = json.load(_fh)
RU, SP, HH, TIE = R["rules"], R["split"], R["household"], R["share_to_tie"]

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE, BAND = "#e1e0d9", "#c3c2b7", "#fcfcfb", "#f0efec"
WRAP = 148
LEVEL = {"a": ("level A, lower rent", BLUE), "b": ("level B, higher rent", ORANGE)}
VERDICTS = (("buy", "buy", BLUE), ("rent", "rent", ORANGE), ("depends on the rent", "depends on the rent", AQUA))

TERM, LOAN = RU["term_years"], RU["loan_share"]
LAB_FIRST, LAB_LAST = RU["labeled_first"], RU["labeled_last"]
FIRST, LAST = RU["first_start"], RU["last_year"]
BRIDGE_LAST = R["inputs"]["value"]["last_bridge_year"]      # R2: the new-house bridge ends in this year
TIE_FLOOR = RU["tie_floor_share"]                            # R12: s <= 0 is drawn at this share
COPYRIGHT = R["inputs"]["french_copyright"]["line"]

FHFA_NOTICE = "This product uses FHFA data but is neither endorsed nor certified by FHFA."
SRC_FHFA = ("Source: FHFA HPI®, all-transactions, not seasonally adjusted, nominal (home values); FHFA HPI®, "
            "purchase-only, seasonally adjusted, nominal (rent level A after the Davis, Lehnert and Martin workbook ends). "
            + FHFA_NOTICE)
SRC_PMMS = "Mortgage rates, and fees and points: Freddie Mac, Primary Mortgage Market Survey, used with attribution."
SRC_PMMS_RATES = "Mortgage rates: Freddie Mac, Primary Mortgage Market Survey, used with attribution."   # chart 1
SRC_BRIDGE = (f"Home values in {FIRST} to {BRIDGE_LAST}: U.S. Census Bureau and U.S. Department of Housing and Urban "
              "Development, Survey of Construction, Price Indexes of New Single-Family Houses Sold Including Lot Value "
              "(constant quality).")
SRC_LEVELS = ("Rent level A: the rent-price ratio of Davis, Lehnert and Martin for owner-occupied housing, data from the "
              "AEI Housing Center (no relationship with AEI is implied), continued with BLS owners' equivalent rent of "
              "primary residence over the FHFA purchase-only index. Rent level B: BEA imputed rental of owner-occupied "
              "stationary homes over the Federal Reserve's Financial Accounts of the United States value of households' "
              "owner-occupied real estate.")
SRC_TAX = ("Property tax: U.S. Census Bureau, Annual Housing Survey, American Housing Survey and American Community "
           "Survey.")
SRC_TAX_HOUSEHOLD = "Property tax: U.S. Census Bureau, American Housing Survey and American Community Survey."
SRC_INSURANCE = "Insurance: NAIC homeowners reports and the American Housing Survey, over ACS median values."
SRC_UPKEEP = "BEA national accounts and fixed assets over Financial Accounts values."
SRC_LOAN_COSTS = "Loan costs: CFPB, HMDA data."
# chart 1: no loan costs; R13 sets V(1) = 1, so no value index or bridge depreciation
SRC_COSTS_SPLIT = f"{SRC_TAX} {SRC_INSURANCE} Upkeep: {SRC_UPKEEP}"
SRC_COSTS_HOUSEHOLD = (f"{SRC_TAX_HOUSEHOLD} {SRC_INSURANCE} Upkeep: {SRC_UPKEEP} "   # chart 2: no Annual Housing
                       f"{SRC_LOAN_COSTS}")                                            # Survey year, no bridge year
SRC_COSTS = f"{SRC_TAX} {SRC_INSURANCE} Upkeep and early depreciation: {SRC_UPKEEP} {SRC_LOAN_COSTS}"   # charts 3, 4
SRC_STOCKS = ("Stocks: Kenneth R. French Data Library, Fama/French factors, market return (Mkt-RF plus RF), "
              f"{COPYRIGHT}. Fund fee: Investment Company Institute, index equity mutual funds, asset-weighted average "
              "expense ratio (www.ici.org).")
ARCHIVE_ALL = "The BEA, BLS, ICI and NAIC files are Internet Archive copies."
ARCHIVE_SPLIT = "The BEA, BLS and NAIC files are Internet Archive copies."
NONCOMMERCIAL = "Calculations by the author. Non-commercial; no publisher of these data endorses this chart."

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


def footnote(fig, text: str, y: float = 0.0) -> None:
    fig.text(0.0, y, textwrap.fill(" ".join(text.split()), WRAP, break_on_hyphens=False), ha="left", va="top",
             fontsize=8.2, color=MUTED)


def year_ticks(ax, first: int, last: int) -> None:
    """Ticks at the first year, each decade between, and the last year: none past the data."""
    ax.set_xticks([first] + [y for y in range(first - first % 10 + 10, last - 2, 10)] + [last])


def mark_labeled(ax, y_text: float) -> None:
    """R1: shade the start years that rest on substitute inputs and say so."""
    ax.axvspan(LAB_FIRST - 0.5, LAB_LAST + 0.5, color=BAND, lw=0, zorder=0)
    ax.text(LAB_FIRST - 0.3, y_text, f"start years {LAB_FIRST} to {LAB_LAST}:\nsubstitute inputs", fontsize=8.4,
            color=INK2, va="top")


def end_labels(ax, items: list, gap: float, x_pad: float) -> None:
    """Direct labels at the right end of each line, nudged apart by at least `gap`. items: [(x, y, text, colour)]."""
    x_text = max(x for x, _, _, _ in items) + x_pad
    placed = []
    for x, y, text, colour in sorted(items, key=lambda i: i[1]):
        y_text = max(y, placed[-1] + gap) if placed else y
        placed.append(y_text)
        ax.annotate(text, (x, y), (x_text, y_text), color=INK2, fontsize=9.0, va="center",
                    arrowprops=dict(arrowstyle="-", color=colour, lw=0.8, shrinkA=0, shrinkB=2))


def chart_monthly_split() -> None:
    """Chart 1 (R13): the first-month rent as a percent of the buyer's first-month outlay, by start year."""
    by = SP["by_start"]
    starts = sorted(by, key=int)
    ext = SP["extension_first_start"]
    ex = SP["owner_example"]
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    top = max(by[s][lv]["split_pct"] for s in starts for lv in LEVEL)
    mark_labeled(ax, top + 9)
    for lv, (name, colour) in LEVEL.items():
        xs, ys = [int(s) for s in starts], [by[s][lv]["split_pct"] for s in starts]
        if lv == "a":
            cut = xs.index(ext)
            ax.plot(xs[:cut], ys[:cut], color=colour, lw=2.0, zorder=3, label=name)
            ax.plot(xs[cut - 1:], ys[cut - 1:], color=colour, lw=2.0, ls=(0, (1.6, 1.4)), zorder=3)
        else:
            ax.plot(xs, ys, color=colour, lw=2.0, zorder=3, label=name)
        ax.plot(xs, ys, "o", color=colour, ms=3.0, zorder=4)
    ax.axhline(ex["share_pct"], color=INK2, lw=0.9, zorder=2)
    ax.text(FIRST + 1.5, ex["share_pct"] - 1.2, f"my example: ${ex['rent']} rent against ${ex['outlay']} of "
            f"mortgage and fees ({ex['share_pct']:.1f}%)", fontsize=8.8, color=INK2, va="top")
    target = int(starts[-1]) - 3
    ax.annotate(f"level A from {ext}: the extension\nwith owners' equivalent rent\nand the purchase-only index",
                (target, by[str(target)]["a"]["split_pct"]), (ext - 11, 15), fontsize=8.4, color=INK2, va="center",
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8, shrinkA=2, shrinkB=3))
    end_labels(ax, [(int(starts[-1]), by[starts[-1]][lv]["split_pct"], LEVEL[lv][0], LEVEL[lv][1]) for lv in LEVEL],
               4.5, 1.0)
    ax.set_xlim(FIRST - 1.5, LAST + 16)
    year_ticks(ax, FIRST, LAST)
    ax.set_ylim(0, top + 12)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.set_ylabel("Percent of the buyer's first-month outlay")
    ax.set_xlabel("Start year (January purchase)")
    ax.set_title(f"First-month rent as a percent of the buyer's first-month outlay, start years {FIRST} to {LAST}",
                 loc="left")
    ax.legend(loc="lower left", frameon=False, fontsize=8.8)
    footnote(fig, (
        "The first month of each start year, the home priced at its value: the rent of the same home under each rent "
        "level (the annual rent-to-price ratio applied to the value, paid monthly) as a percent of the buyer's outlay, "
        f"the payment on a {TERM}-year fixed-rate loan for {100 * LOAN:.0f}% of the price at the year's average rate "
        "plus property tax, insurance and upkeep. Level A: lower rent; level B: higher rent. Start years "
        f"{LAB_FIRST} to {LAB_LAST} rest on substitute inputs; level A from {ext} rests on the extension (dashed). "
        f"{SRC_PMMS_RATES} {SRC_LEVELS} {SRC_COSTS_SPLIT} Source: FHFA HPI®, purchase-only, seasonally adjusted, "
        f"nominal (level A from {ext}). {FHFA_NOTICE} {ARCHIVE_SPLIT} {NONCOMMERCIAL}"))
    save(fig, "rb-1-monthly-split.png")


def chart_one_household() -> None:
    """Chart 2 (R14): the 1996 buyer and renter, December 1996 to December 2025, in 2025 dollars, both rent levels."""
    years = sorted(HH["by_year"], key=int)
    xs = [int(y) for y in years]
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    items = []
    for who, colour in (("buyer", BLUE), ("renter", ORANGE)):
        for lv, style in (("a", "-"), ("b", (0, (4, 2)))):
            ys = [HH["by_year"][y][lv][who] for y in years]
            ax.plot(xs, ys, color=colour, lw=2.0, ls=style, zorder=3,
                    label=f"{who}, {LEVEL[lv][0]}")
            ax.plot([xs[-1]], [ys[-1]], "o", color=colour, ms=4.5, zorder=4)
            items.append((xs[-1], ys[-1], f"{who}, level {lv.upper()}: ${HH['last'][lv][who]:,.0f}", colour))
    top = max(i[1] for i in items)
    end_labels(ax, items, top * 0.055, 0.8)
    ax.set_xlim(xs[0] - 0.8, xs[-1] + 11)
    year_ticks(ax, xs[0], xs[-1])
    ax.set_ylim(0, top * 1.08)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v / 1000:,.0f}k"))
    ax.set_ylabel(f"Net worth, {HH['dollars_year']} dollars")
    ax.set_title(f"Net worth of the {HH['start']} buyer and renter, December {xs[0]} to December {xs[-1]}, in "
                 f"{HH['dollars_year']} dollars", loc="left")
    ax.legend(loc="upper left", frameon=False, fontsize=8.6)
    footnote(fig, (
        f"The {HH['start']} buyer and renter: a home at the Census Bureau's {HH['census_year']} median value of "
        f"specified owner-occupied homes, moved to {HH['start']} with the FHFA index (${HH['price']:,.0f}); "
        f"{100 * RU['down_share']:.0f}% down and a {TERM}-year fixed-rate loan at the year's average rate, refinanced "
        f"when the month's average rate falls {RU['refi_drop_pp']:.0f} percentage point or more below the loan's rate. "
        "The renter invests the down payment and buying costs at closing and the monthly gap after that; the buyer "
        "invests the gap when the rent exceeds the buyer's outlay. Net worth at each December: the home's value less "
        f"{100 * RU['sell_share']:.0f}% selling costs, less the loan balance, plus the buyer's fund; the renter's fund. "
        f"Solid lines: rent level A (the lower rent); dashed: level B (the higher rent). In {HH['dollars_year']} "
        "dollars of the BLS R-CPI-U-RS annual averages. The aggregate rent ratios are applied to a median-priced home. "
        f"{SRC_FHFA} {SRC_PMMS} {SRC_LEVELS} {SRC_COSTS_HOUSEHOLD} {SRC_STOCKS} {ARCHIVE_ALL} {NONCOMMERCIAL}"))
    save(fig, "rb-2-one-household.png")


def chart_who_is_ahead() -> None:
    """Chart 3 (R10): the verdict for every start year and number of years held."""
    cells = R["cells"]
    starts = sorted(cells, key=int)
    code = {v: i for i, (v, _, _) in enumerate(VERDICTS)}
    grid = [[float("nan")] * len(starts) for _ in range(RU["max_h"])]
    for j, s in enumerate(starts):
        for h, c in cells[s].items():
            grid[int(h) - 1][j] = code[c["verdict"]]
    fig, ax = plt.subplots(figsize=(8.8, 6.0))
    x0 = int(starts[0])
    edges_x = [x0 - 0.5 + j for j in range(len(starts) + 1)]
    edges_y = [0.5 + i for i in range(RU["max_h"] + 1)]
    ax.pcolormesh(edges_x, edges_y, grid, cmap=ListedColormap([c for _, _, c in VERDICTS]), vmin=-0.5, vmax=2.5,
                  edgecolors=SURFACE, linewidth=0.6, zorder=2)
    ax.grid(False)
    last_x = int(starts[-1])
    counted = []
    for h in RU["stays"]:
        have = [int(s) for s in starts if str(h) in cells[s]]
        ax.add_patch(Rectangle((have[0] - 0.5, h - 0.5), have[-1] - have[0] + 1, 1, fill=False, ec=INK, lw=1.1,
                               zorder=3))
        ax.text(last_x + 1.0, h, f"{h} years", fontsize=8.8, color=INK2, va="center")
        c = R["headline"][str(h)]["all"]
        counted.append(f"after {h} years, buy {c['buy']}, rent {c['rent']} and depends on the rent {c['depends']} "
                       f"(start years {c['first_start']} to {c['last_start']})")
    ax.plot([LAB_FIRST - 0.4, LAB_LAST + 0.4], [RU["max_h"] + 1.0] * 2, color=INK2, lw=1.0, clip_on=False)
    ax.text(LAB_FIRST - 0.4, RU["max_h"] + 1.4, f"start years {LAB_FIRST} to {LAB_LAST}: substitute inputs",
            fontsize=8.4, color=INK2, va="bottom")
    ax.set_xlim(x0 - 0.5, last_x + 0.5)
    ax.set_ylim(0.5, RU["max_h"] + 0.5)
    year_ticks(ax, x0, last_x)
    ax.set_yticks([1] + list(range(5, RU["max_h"] + 1, 5)))
    ax.set_xlabel("Start year (January purchase)")
    ax.set_ylabel("Years held, to the end of a December")
    ax.set_title(f"Who is ahead, by start year and years held, start years {x0} to {last_x}", loc="left", pad=26)
    handles = [Patch(facecolor=c, edgecolor=SURFACE, label=label) for _, label, c in VERDICTS]
    ax.legend(handles=handles, loc="upper right", frameon=False, fontsize=9.0, title="verdict", title_fontsize=9.0)
    footnote(fig, (
        "Each cell compares the buyer and the renter at the end of a December after the years held: buy if the "
        "buyer's net worth is higher under both rent levels, rent if the renter's is higher under both, depends on the "
        "rent if the levels disagree. The buyer puts "
        f"{100 * RU['down_share']:.0f}% down and takes a {TERM}-year fixed-rate loan at the year's average rate, "
        "refinanced when rates fall; pays property tax, insurance and upkeep; and invests the monthly gap when the rent "
        "exceeds that outlay. The renter invests the buyer's cash at closing and the monthly gap in a stock market fund. "
        f"Net worth: the home's value less {100 * RU['sell_share']:.0f}% selling costs, less the loan balance, plus "
        f"the buyer's fund; the renter's fund. Framed rows, start years by verdict: {'; '.join(counted)}. "
        f"{SRC_FHFA} {SRC_BRIDGE} {SRC_PMMS} {SRC_LEVELS} {SRC_COSTS} {SRC_STOCKS} {ARCHIVE_ALL} {NONCOMMERCIAL}"))
    save(fig, "rb-3-who-is-ahead.png")


def chart_share_to_tie() -> None:
    """Chart 4 (R12): the share of each monthly gap the renter must invest to tie after 30 years."""
    h = RU["max_h"]
    data = TIE[str(h)]
    by, summ = data["by_start"], data["summary"]
    starts = sorted(by, key=int)
    xs = [int(s) for s in starts]
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    mark_labeled(ax, 96)
    above, below = 112, -12
    for lv, (name, colour) in LEVEL.items():
        ys = [100 * by[s][lv]["share"] if by[s][lv]["share"] is not None else float("nan") for s in starts]
        ax.plot(xs, ys, color=colour, lw=2.0, zorder=3, label=name)
        filled = lv == "a"
        ax.plot(xs, ys, "o", ms=6.5 if filled else 9.0, mfc=colour if filled else "none", mec=colour, mew=1.6,
                ls="none", zorder=4 if filled else 5)
        for s in starts:
            label = by[s][lv]["label"]
            if label in ("cannot tie", "no gap"):
                ax.plot([int(s)], [above if label == "cannot tie" else below], "^" if label == "cannot tie" else "v",
                        ms=8, mfc=colour if filled else "none", mec=colour, mew=1.6, ls="none", zorder=5)
    ax.axhline(100 * TIE_FLOOR, color=INK2, lw=0.9, zorder=2)
    ax.axhline(100, color=GRID, lw=0.9, zorder=1)
    ax.text(xs[-1] + 0.8, 100 * TIE_FLOOR, f"{100 * TIE_FLOOR:.0f}%: the sum invested at\nclosing alone ties or wins",
            fontsize=8.6, color=INK2, va="center")
    shown = {by[s][lv]["label"] for s in starts for lv in LEVEL}
    notes = []
    if "cannot tie" in shown:
        ax.text(xs[-1] + 0.8, above, "cannot tie: more than the\nwhole gap would be needed", fontsize=8.6, color=INK2,
                va="center")
        notes.append("triangles at the top: investing the whole gap is not enough to tie")
    if "no gap" in shown:
        ax.text(xs[-1] + 0.8, below, "no gap: the rent did not fall\nbelow the buyer's outlay", fontsize=8.6,
                color=INK2, va="center")
        notes.append("triangles at the bottom: the rent did not fall below the buyer's outlay in any month")
    ax.set_xlim(xs[0] - 1, xs[-1] + 9)
    year_ticks(ax, xs[0], xs[-1])
    ax.set_ylim(below - 6 if "no gap" in shown else below / 2, above + 6 if "cannot tie" in shown else 106)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.set_ylabel("Share of each monthly gap invested")
    ax.set_xlabel("Start year (January purchase)")
    ax.set_title(f"Share of the monthly gap the renter must invest to tie after {h} years, start years "
                 f"{summ['first_start']} to {summ['last_start']}", loc="left")
    handles = [Line2D([], [], color=BLUE, lw=2.0, marker="o", ms=6.5, label=LEVEL["a"][0]),
               Line2D([], [], color=ORANGE, lw=2.0, marker="o", mfc="none", ms=9.0, mew=1.6, label=LEVEL["b"][0])]
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(0.0, 0.62), frameon=False, fontsize=8.8)
    footnote(fig, (
        f"For each start year with {h} years of data: the share of each monthly gap (the buyer's outlay less the rent, "
        f"when positive) the renter would have to invest for the renter's fund to equal the buyer's net worth after {h} "
        "years. The sum invested at closing (the buyer's down payment and buying costs) is invested in full and the "
        "buyer's side does not change; the renter's fund grows in step with the share. "
        f"{100 * TIE_FLOOR:.0f}%: the sum invested at closing alone ties or wins. "
        + "".join(f"{n[0].upper()}{n[1:]}. " for n in notes)
        + f"{SRC_FHFA} {SRC_BRIDGE} {SRC_PMMS} {SRC_LEVELS} {SRC_COSTS} {SRC_STOCKS} {ARCHIVE_ALL} {NONCOMMERCIAL}"))
    save(fig, "rb-4-share-to-tie.png")


if __name__ == "__main__":
    os.makedirs(os.path.join(BASE, "charts"), exist_ok=True)
    chart_monthly_split()
    chart_one_household()
    chart_who_is_ahead()
    chart_share_to_tie()
