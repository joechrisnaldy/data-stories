"""Post 30: buy, or rent and invest the difference. Writes results.json from the pinned data files.

Every rule is the pre-registration's (docs/2026-11-13-rent-vs-buy-design.md, R1 to R16, amendments A1 and A2); the rule
each step implements is named beside it. Pins and readers live in profile_data.py and the model in rentbuy.py (checked
by test_rentbuy.py), so no rule is written twice. Run from the post folder: python3 -I build_analysis.py
"""
import hashlib
import json
import math
import os
import statistics
import sys
from dataclasses import dataclass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)   # python3 -I leaves the script's folder off sys.path; appended, the standard library still wins
import profile_data as pdata  # noqa: E402
import rentbuy as rb  # noqa: E402

FIRST_START, LAST_YEAR = 1972, 2025      # R1: start years 1972 to 2025; nothing is measured after December 2025
MAX_H = 30                               # R1: h = 1 to 30 whole years
STAYS = (5, 10, 30)                      # R1, R10: the reported stays
LABELED = (1972, 1976)                   # R1: start years labeled for their substitute inputs
FROM = 1977                              # R1: headline counts again for start years from 1977
TIE_H = (10, 30)                         # R12
HOUSEHOLD_START = 1996                   # R14
LEVELS = ("a", "b")                      # R3: rental equivalence (A) and national accounts (B)
FIRST_FHFA = (1975, 1)                   # R2: the all-transactions index from 1975Q1
BRIDGE = tuple((y, q) for y in range(1972, 1975) for q in (1, 2, 3, 4))   # R2: 1972Q1 to 1974Q4
DLM_LAST = (2018, 2)                     # R3: the workbook's last quarter
RAPPAPORT_OWNER_DECADES = (1970, 1990)   # R16: decades whose ten-year stays Rappaport (2010) found owners ahead in
P_FIX_YEARS = range(2018, 2023)          # R4, R5, R9: the 2018 to 2022 window
TAX_MEANS = (1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1983)   # R7a, A2: no national survey in 1982
TAX_MEDIANS = range(1985, 2004, 2)       # R7a: AHS medians, odd years 1985 to 2003
TAX_ACS = tuple(range(2010, 2020)) + tuple(range(2021, 2026))   # R7a: ACS aggregates (no 2020 1-year release)
TAX_ACS_MEDIANS = range(2005, 2010)      # R7a, A2: ACS ratio of medians, B25103_001 over B25077_001
NAIC_YEARS = (2021, 2022, 2023)          # R7b
INSURANCE_BASE_YEAR = 2005               # R7b: the AHS 2005 median over the ACS 2005 median value
FA_LAST = 2023                           # R7c, A2: 2024 and 2025 hold the 2023 share
FEE_FIRST = 1996                         # R8: 1972 to 1995 take the 1996 value
OWNER_EXAMPLE = (200, 700)               # section 1 and R13: rent against mortgage and fees
PO_LINK = (1991, 1)                      # R15.3: purchase-only from 1991Q1, chained
CPI_LINK = (1982, 12)                    # R15.1: rent of primary residence through December 1982, OER from January
VANGUARD_FEE = 0.0043                    # R15.4: the Vanguard 500 Index Fund's first expense ratio, 1972 to 1995
COST_YEAR, TAX_RATIO_YEAR = 2023, 2025   # R15.5, R15.6: NAIC, ACS and AHS 2023; the ACS 2025 tax ratios
LOW_BUY, LOW_SELL = 0.01, 0.05           # R15.5: buying costs 1% of the price; selling 5%
HIGH_BUY_ADD, HIGH_SELL = 0.01, 0.07     # R15.6: buying costs plus 1% of the price; selling 7%
START_YEARS = range(FIRST_START, LAST_YEAR + 1)
YEARS = range(FIRST_START, LAST_YEAR + 1)


@dataclass(frozen=True)
class Variant:
    """The main run or one R15 sensitivity."""
    name: str
    rule: str
    refinance: bool = True       # R9 in the main run; R15.2 drops it
    cpi_rent: bool = False       # R15.1
    purchase_only: bool = False  # R15.3
    fee: str = "ici"             # R8; R15.4: "vanguard" for 1972 to 1995, or "none"
    costs: str = "main"          # R5 to R7; R15.5 "low", R15.6 "high"


MAIN = Variant("main", "R1 to R13")
SENSITIVITIES = (Variant("cpi_rent", "R15.1", cpi_rent=True), Variant("no_refinancing", "R15.2", refinance=False),
                 Variant("purchase_only", "R15.3", purchase_only=True), Variant("fee_vanguard", "R15.4", fee="vanguard"),
                 Variant("no_fee", "R15.4", fee="none"), Variant("costs_low", "R15.5", costs="low"),
                 Variant("costs_high", "R15.6", costs="high"))


def sample_id(items) -> str:
    """A short hash of the entities a statistic was computed on, so prose can pair figures from one sample."""
    return hashlib.sha256(json.dumps(sorted(map(str, items))).encode()).hexdigest()[:12]


def qkey(q: tuple[int, int]) -> str:
    return f"{q[0]}Q{q[1]}"


def by_year(d: dict) -> dict:
    return {str(y): d[y] for y in sorted(d)}


# --- inputs ---------------------------------------------------------------------------------------------------------

def inputs() -> dict:
    french, rights = pdata.read_french()
    return {"pmms": pdata.read_pmms(), "dlm": pdata.read_dlm(), "at": pdata.read_fhfa_at(), "po": pdata.read_fhfa_po(),
            "new_house": pdata.read_new_house_index(), "z1": pdata.read_z1(), "nipa": pdata.read_nipa(),
            "fa": pdata.read_fa(), "french": french, "french_rights": rights, "ici": pdata.read_ici(),
            "cpi": pdata.read_cpi(), "rs": pdata.read_rcpiurs(), "census": pdata.read_census_value(),
            "acs": pdata.read_acs(), "ahs": pdata.read_ahs_values(), "costs": pdata.read_cost_values()}


def mortgage_inputs(d: dict) -> dict:
    """R4, R5, R9: the year's and the month's mean rate, points per start year and per month, p_fix and c_np."""
    weeks = d["pmms"]
    rate_year = rb.weekly_means([(w, r) for w, r, _ in weeks])
    rate_month = rb.weekly_means([(w, r) for w, r, _ in weeks], by_month=True)
    points_year = rb.weekly_means([(w, p) for w, _, p in weeks])
    points_month = rb.weekly_means([(w, p) for w, _, p in weeks], by_month=True)
    fix_weeks = [p for w, _, p in weeks if p is not None and w[0] in P_FIX_YEARS]
    fix_dates = [w for w, _, p in weeks if p is not None and w[0] in P_FIX_YEARS]
    p_fix = rb.mean(fix_weeks)
    no_points = [y for y in YEARS if y not in points_year]
    if no_points != list(range(min(no_points), LAST_YEAR + 1)):
        raise SystemExit(f"R4: years without points {no_points} are not the years from 2023")
    c = d["costs"]
    costs = {y: c[("cfpb_median_total_loan_costs_conv_conforming_purchase", y)] for y in P_FIX_YEARS}
    amounts = {y: c[("cfpb_median_loan_amount_conv_conforming_purchase", y)] for y in P_FIX_YEARS}
    months = rb.months_from(FIRST_START, LAST_YEAR - FIRST_START + 1)
    return {"rate_year": {y: rate_year[y] for y in YEARS}, "rate_month": {m: rate_month[m] for m in months},
            "points_year": {y: points_year.get(y) for y in YEARS}, "p0": {y: points_year.get(y, p_fix) for y in YEARS},
            "points_month": {m: points_month.get(m, p_fix) for m in months}, "p_fix": p_fix, "p_fix_weeks": len(fix_weeks),
            "p_fix_sample": sample_id("-".join(map(str, w)) for w in fix_dates),
            "c_np": rb.other_loan_costs(costs, amounts, p_fix), "cfpb_costs": costs, "cfpb_amounts": amounts,
            "cfpb_mean_share": rb.mean([costs[y] / (amounts[y] * 1000) for y in P_FIX_YEARS]),
            "first_year_without_points": no_points[0]}


def value_inputs(d: dict, quarters: list) -> dict:
    """R2: the bridged value index and depreciation; R15.3: purchase-only from 1991Q1, chained."""
    index = rb.value_index(d["new_house"], d["at"], FIRST_FHFA, BRIDGE)
    po_nsa = {q: v[0] for q, v in d["po"].items()}
    lm = d["z1"]["LM155035015"]
    return {"index": {q: index[q] for q in quarters}, "index_po": rb.chain(index, po_nsa, quarters, PO_LINK),
            "d": rb.share_of_stock(d["nipa"]["B2607C"], lm, range(FIRST_START, rb.LAST_BRIDGE_YEAR + 1))}


def rent_inputs(d: dict, quarters: list, months: list) -> dict:
    """R3: k_A by quarter (the workbook, then the OER over purchase-only extension), k_B by year, the scope check;
    R15.1: the chained CPI rent index."""
    po_sa = {q: v[1] for q, v in d["po"].items()}
    k_a = rb.extend_ratio(d["dlm"], DLM_LAST, d["cpi"]["CUSR0000SEHC01"], po_sa, quarters)
    nipa, z1 = d["nipa"], d["z1"]
    return {"k_a": k_a, "k_b": rb.share_of_stock(nipa["DOSTRC"], z1["FL155035013"], YEARS),
            "scope": rb.share_of_stock(nipa["DOWNRC"], z1["LM155035015"], YEARS),
            "cpi": rb.chain(d["cpi"]["CUUR0000SEHA"], d["cpi"]["CUUR0000SEHC01"], months, CPI_LINK)}


def tax_inputs(d: dict) -> dict:
    """R7a: the survey values, then straight lines for the years without one. A2: 2005 to 2009 take the ACS ratio of
    medians, B25103_001 over B25077_001; a year without both cells stops the build, since A2 chose that ratio over a
    straight line for those years."""
    ahs, acs = d["ahs"], d["acs"]
    known = {y: ahs[("ahs_re_tax_mean_per_1000", y)] / 1000 for y in TAX_MEANS}
    known.update({y: ahs[("ahs_re_tax_median_per_1000", y)] / 1000 for y in TAX_MEDIANS})
    known.update({y: acs[(y, "B25090_001")] / acs[(y, "B25082_001")] for y in TAX_ACS})
    medians = rb.acs_ratio(acs, TAX_ACS_MEDIANS, "B25103_001", "B25077_001")
    known.update(medians)
    tau = rb.fill_straight(known, YEARS)
    source = {}
    for y in YEARS:
        source[y] = ("AHS mean" if y in TAX_MEANS else "AHS median" if y in TAX_MEDIANS else
                     "ACS aggregate" if y in TAX_ACS else "ACS ratio of medians" if y in medians else
                     "the first survey value" if y < min(known) else "straight line")
    return {"tau": tau, "source": source, "medians_read": sorted(medians)}


def insurance_inputs(d: dict) -> dict:
    """R7b: iota_2005, iota_late and the path between them."""
    acs, ahs, c = d["acs"], d["ahs"], d["costs"]
    early = 12 * ahs[("ahs_property_insurance_median_monthly", INSURANCE_BASE_YEAR)] / acs[(INSURANCE_BASE_YEAR, "B25077_001")]
    naic = {y: c[("naic_ho3_average_premium", y)] / acs[(y, "B25077_001")] for y in NAIC_YEARS}
    late = rb.mean([naic[y] for y in NAIC_YEARS])
    return {"iota": rb.insurance_path(early, late, YEARS), "iota_2005": early, "iota_late": late, "naic_ratio": naic}


def upkeep_inputs(d: dict) -> dict:
    """R7c: routine upkeep and improvements, each over the mean of the year's four quarter-end Z.1 values; R15.6 sets
    the owner-occupied share to 1."""
    nipa, fa, lm = d["nipa"], d["fa"], d["z1"]["LM155035015"]
    routine = {y: nipa["DOWNRC"][y] - nipa["B1300C"][y] + nipa["W307RC"][y] - nipa["W316RC"][y] for y in YEARS}
    share = {y: fa["k1r53101esoo"][min(y, FA_LAST)] / fa["k1r53101es00"][min(y, FA_LAST)] for y in YEARS}
    improve = {y: nipa["A946RC"][y] * share[y] for y in YEARS}
    routine_s = rb.share_of_stock(routine, lm, YEARS)
    improve_s = rb.share_of_stock(improve, lm, YEARS)
    all_tenures = rb.share_of_stock(nipa["A946RC"], lm, YEARS)
    return {"u": rb.upkeep(routine_s, improve_s, YEARS), "routine": routine_s, "improvements": improve_s,
            "owner_share": share, "u_high": rb.upkeep(routine_s, all_tenures, YEARS)}


def sensitivity_inputs(d: dict) -> dict:
    """R15.5 and R15.6: the ACS 2025 tax ratios, the NAIC 2023 insurance rates and the AHS 2023 routine upkeep."""
    acs, c = d["acs"], d["costs"]
    forms = sum(c[(f"naic_premium_{f}", COST_YEAR)] for f in ("ho1", "ho2", "ho3", "ho5", "ho8"))
    if abs(forms - (c[("naic_premium_total_dw_and_owner_forms", COST_YEAR)] - c[("naic_premium_dw", COST_YEAR)])) > 0.5:
        raise SystemExit("R15.5: the five NAIC forms do not sum to Table 4's total less dwelling fire")
    tax = acs[(TAX_RATIO_YEAR, "B25103_001")]
    return {"tax_low": acs[(TAX_RATIO_YEAR, "B25103_003")] / tax, "tax_high": acs[(TAX_RATIO_YEAR, "B25103_002")] / tax,
            "iota_low": forms / acs[(COST_YEAR, "B25082_001")], "naic_forms_premium": forms,
            "routine_low": c[("ahs_mean_routine_maintenance", COST_YEAR)] / c[("ahs_mean_value", COST_YEAR)],
            "iota_high": c[("naic_ho3_average_premium", COST_YEAR)] / acs[(COST_YEAR, "B25077_001")]}


def prepare(d: dict) -> dict:
    """Every series the runs use, keyed by month, quarter or year."""
    months = rb.months_from(FIRST_START, LAST_YEAR - FIRST_START + 1)
    quarters = sorted({rb.quarter_of(m) for m in months})
    fee = {y: d["ici"][max(y, FEE_FIRST)] / 100 for y in YEARS}                    # R8
    m = {"months": months, "quarters": quarters, "market_pct": {k: sum(d["french"][k]) for k in months},
         "fee": {"ici": fee, "vanguard": {y: VANGUARD_FEE if y < FEE_FIRST else fee[y] for y in YEARS},
                 "none": {y: 0.0 for y in YEARS}}}
    for part in (mortgage_inputs(d), value_inputs(d, quarters), rent_inputs(d, quarters, months), tax_inputs(d),
                 insurance_inputs(d), upkeep_inputs(d), sensitivity_inputs(d)):
        m.update(part)
    m["carry"] = {"main": {y: m["tau"][y] + m["iota"][y] + m["u"][y] for y in YEARS},
                  "low": {y: m["tau"][y] * m["tax_low"] + m["iota_low"] + m["routine_low"] for y in YEARS},
                  "high": {y: m["tau"][y] * m["tax_high"] + m["iota_high"] + m["u_high"][y] for y in YEARS}}
    return m


# --- runs -----------------------------------------------------------------------------------------------------------

def buy_cost(m: dict, v: Variant, s: int) -> float:
    """R5; R15.5: 1% of the price; R15.6: R5's cost plus 1% of the price."""
    if v.costs == "low":
        return LOW_BUY * rb.PRICE
    base = rb.buying_cost(m["p0"][s], m["c_np"])
    return base + HIGH_BUY_ADD * rb.PRICE if v.costs == "high" else base


def run_start(m: dict, v: Variant, s: int) -> dict[str, rb.Run]:
    """One start year under both rent levels."""
    months = rb.months_from(s, min(MAX_H, LAST_YEAR - s + 1))
    value = rb.value_path(months, m["index_po"] if v.purchase_only else m["index"], rb.depreciation(months, m["d"]))
    carry = [m["carry"][v.costs][y] for y, _ in months]
    returns = rb.fund_returns(months, m["market_pct"], m["fee"][v.fee])
    refi = (rb.Refinancing(tuple(m["rate_month"][mo] for mo in months), tuple(m["points_month"][mo] for mo in months),
                           m["c_np"]) if v.refinance else None)
    sell = {"low": LOW_SELL, "high": HIGH_SELL}.get(v.costs, rb.SELL)
    out = {}
    for level in LEVELS:
        ratio = ([m["k_a"][rb.quarter_of(mo)] for mo in months] if level == "a" else
                 [m["k_b"][y] for y, _ in months])
        rent = rb.ratio_rent(ratio, value)
        if v.cpi_rent:                                   # R15.1: the month-1 rent, grown with the chained CPI index
            rent = [rent[0] * m["cpi"][mo] / m["cpi"][months[0]] for mo in months]
        out[level] = rb.simulate(value, rent, carry, returns, m["rate_year"][s], buy_cost(m, v, s), refi, sell)
    return out


def run_all(m: dict, v: Variant) -> dict[int, dict[str, rb.Run]]:
    return {s: run_start(m, v, s) for s in START_YEARS}


def cells(runs: dict) -> dict[int, dict[int, dict]]:
    """R10 for every (start year, h): each level's net worths, who is ahead and the renter's multiple; the verdict."""
    out = {}
    for s, pair in runs.items():
        out[s] = {}
        for ya, yb in zip(pair["a"].year_ends, pair["b"].year_ends, strict=True):
            lv = {}
            for name, ye in (("a", ya), ("b", yb)):
                lv[name] = {"buyer_nw": ye.buyer_nw, "renter_nw": ye.renter_nw, "buyer_fund": ye.buyer_fund,
                            "ahead": rb.ahead(ye.buyer_nw, ye.renter_nw),
                            "multiple": ye.renter_nw / ye.buyer_nw if ye.buyer_nw != 0 else None}
            out[s][ya.h] = {"year": s + ya.h - 1, "value": ya.value, "balance": ya.balance,
                            "verdict": rb.verdict(lv["a"]["ahead"], lv["b"]["ahead"]), "a": lv["a"], "b": lv["b"]}
    return out


# --- measures -------------------------------------------------------------------------------------------------------

def counts(table: dict, h: int, first: int = FIRST_START, last: int = LAST_YEAR) -> dict:
    """R10: the number of start years (first to last, with an h-year history) with each verdict."""
    ss = [s for s in sorted(table) if first <= s <= last and h in table[s]]
    v = {s: table[s][h]["verdict"] for s in ss}
    return {"h": h, "n": len(ss), "sample": sample_id(f"{s}:{h}" for s in ss), "first_start": ss[0], "last_start": ss[-1],
            "buy": sum(1 for s in ss if v[s] == rb.BUY), "rent": sum(1 for s in ss if v[s] == rb.RENT),
            "depends": sum(1 for s in ss if v[s] == rb.DEPENDS),
            "buy_starts": [s for s in ss if v[s] == rb.BUY], "rent_starts": [s for s in ss if v[s] == rb.RENT],
            "depends_starts": [s for s in ss if v[s] == rb.DEPENDS]}


def headline(table: dict) -> dict:
    """R10's headline: every stay, all start years and start years from 1977."""
    return {str(h): {"all": counts(table, h), "from_1977": counts(table, h, FROM)} for h in range(1, MAX_H + 1)}


def break_evens(table: dict) -> dict:
    """R11: per start year and level, the first h at which buying is ahead and whether it stays ahead; the agreed
    break-even is the first h with the verdict 'buy'."""
    per = {}
    for s in sorted(table):
        hs = sorted(table[s])
        entry = {"h_max": hs[-1]}
        flags = {lv: [table[s][h][lv]["ahead"] == rb.BUY for h in hs] for lv in LEVELS}
        flags["agreed"] = [table[s][h]["verdict"] == rb.BUY for h in hs]
        for name, f in flags.items():
            first, stays = rb.break_even(f)
            entry[name] = {"first_h": first, "stays": stays, "within_data": first is not None}
        per[str(s)] = entry
    summary = {}
    for name, need in (("all", 1), ("ten_years", 10), ("thirty_years", MAX_H)):
        ss = [s for s in sorted(table) if len(table[s]) >= need]
        summary[name] = {"n": len(ss), "sample": sample_id(ss), "first_start": ss[0], "last_start": ss[-1]}
        for lv in LEVELS + ("agreed",):
            firsts = [per[str(s)][lv]["first_h"] for s in ss]
            within = sorted(f for f in firsts if f is not None)
            longer = sorted(within + [math.inf] * (len(firsts) - len(within)))
            med = statistics.median(longer)
            summary[name][lv] = {"within_data": len(within), "not_within_data": len(firsts) - len(within),
                                 "median_counting_not_within_as_longer": None if math.isinf(med) else med,
                                 "median_is_not_within_data": math.isinf(med),
                                 "median_within_data": statistics.median(within) if within else None,
                                 "stays": sum(1 for s in ss if per[str(s)][lv]["stays"])}
    return {"by_start": per, "summary": summary}


def shares_to_tie(runs: dict) -> dict:
    """R12: per start year with an h-year history, level and h = 10 and 30, the share of each monthly gap the renter
    must invest to tie."""
    out = {}
    for h in TIE_H:
        per, ss = {}, [s for s in sorted(runs) if len(runs[s]["a"].year_ends) >= h]
        for s in ss:
            per[str(s)] = {}
            for lv in LEVELS:
                ye = runs[s][lv].year_ends[h - 1]
                label, share, raw = rb.share_to_tie(ye.buyer_nw, ye.renter_day_one, ye.renter_fund, ye.any_gap)
                per[str(s)][lv] = {"label": label, "share": share, "raw": raw}
        summary = {"n": len(ss), "sample": sample_id(f"{s}:{h}" for s in ss), "first_start": ss[0], "last_start": ss[-1]}
        for lv in LEVELS:
            got = [per[str(s)][lv] for s in ss]
            numeric = [g["share"] for g in got if g["share"] is not None]
            summary[lv] = {**{lab: sum(1 for g in got if g["label"] == lab)
                              for lab in (rb.SHARE, rb.ZERO, rb.CANNOT_TIE, rb.NO_GAP)},
                           "median_share": statistics.median(numeric) if numeric else None,
                           "below_half": sum(1 for x in numeric if x < 0.5)}
        out[str(h)] = {"by_start": per, "summary": summary}
    return out


def split(m: dict) -> dict:
    """R13: the month-1 rent as a percent of the buyer's month-1 outlay, per start year and level."""
    example_pct = 100 * OWNER_EXAMPLE[0] / OWNER_EXAMPLE[1]
    per = {}
    for s in START_YEARS:
        k1 = {"a": m["k_a"][(s, 1)], "b": m["k_b"][s]}
        pay = rb.payment(rb.LOAN, m["rate_year"][s] / 100, rb.TERM)
        carry = m["carry"]["main"][s] / 12
        per[str(s)] = {"payment": pay, "carrying": carry, "outlay": pay + carry, "rate_pct": m["rate_year"][s],
                       **{lv: {"split_pct": rb.month_one_split(k1[lv], m["rate_year"][s], m["carry"]["main"][s])}
                          for lv in LEVELS}}
    ss = list(START_YEARS)
    summary = {"n": len(ss), "sample": sample_id(ss), "first_start": ss[0], "last_start": ss[-1]}
    for lv in LEVELS:
        pct = {s: per[str(s)][lv]["split_pct"] for s in ss}
        lo, hi = min(ss, key=pct.get), max(ss, key=pct.get)
        summary[lv] = {"min_pct": pct[lo], "min_start": lo, "max_pct": pct[hi], "max_start": hi,
                       "above_example": sum(1 for s in ss if pct[s] > example_pct),
                       "starts_not_above_example": [s for s in ss if not pct[s] > example_pct]}
    first_ext = min(s for s in ss if (s, 1) > DLM_LAST)
    return {"by_start": per, "summary": summary, "extension_first_start": first_ext,
            "owner_example": {"rent": OWNER_EXAMPLE[0], "outlay": OWNER_EXAMPLE[1], "share_pct": example_pct}}


def household(d: dict, runs: dict) -> dict:
    """R14: the 1996 buyer and renter at each December, in 2025 dollars of the R-CPI-U-RS annual averages."""
    at, rs = d["at"], d["rs"]
    base_year, base_value = d["census"]
    price = rb.household_price(base_value, at[(HOUSEHOLD_START, 1)], [at[(base_year, q)] for q in (1, 2, 3, 4)])
    base = rs[LAST_YEAR]["avg"]
    years = {}
    for lv in LEVELS:
        for ye in runs[HOUSEHOLD_START][lv].year_ends:
            y = HOUSEHOLD_START + ye.h - 1
            years.setdefault(str(y), {})[lv] = {
                "buyer": rb.in_dollars_of(ye.buyer_nw, price, rs[y]["avg"], base),
                "renter": rb.in_dollars_of(ye.renter_nw, price, rs[y]["avg"], base)}
    last = years[str(LAST_YEAR)]
    return {"start": HOUSEHOLD_START, "price": price, "price_in_dollars_of_last": price * base / rs[HOUSEHOLD_START]["avg"],
            "census_year": base_year, "census_value": base_value, "dollars_year": LAST_YEAR,
            "cpi": {str(y): rs[y]["avg"] for y in range(HOUSEHOLD_START, LAST_YEAR + 1)}, "by_year": years,
            "first_year": HOUSEHOLD_START, "last_year": LAST_YEAR, "n": len(years), "sample": sample_id(years),
            "last": {lv: {**last[lv], "renter_minus_buyer": last[lv]["renter"] - last[lv]["buyer"]} for lv in LEVELS}}


def refinancings(runs: dict) -> dict:
    """R9 in the main run: the months each buyer refinanced, the new rate and the cost."""
    per = {}
    for s, pair in runs.items():
        months = rb.months_from(s, len(pair["a"].year_ends))
        per[str(s)] = [[months[t][0], months[t][1], lm.rate_pct, lm.refi_cost]
                       for t, lm in enumerate(pair["a"].loan) if lm.refi_cost > 0]
    did = [s for s in runs if per[str(s)]]
    return {"by_start": per, "n": len(runs), "sample": sample_id(runs), "starts_with_one": len(did),
            "most_in_one_start": max(len(v) for v in per.values())}


def sensitivity(name: str, rule: str, table: dict, main: dict) -> dict:
    """R15: verdict counts at 5, 10 and 30 years and the cells whose verdict changes from the main run."""
    keys = [(s, h) for s in sorted(main) for h in sorted(main[s])]
    changed = [[s, h, main[s][h]["verdict"], table[s][h]["verdict"]] for s, h in keys
               if main[s][h]["verdict"] != table[s][h]["verdict"]]
    out = {"rule": rule, "counts": {str(h): {"all": counts(table, h), "from_1977": counts(table, h, FROM)} for h in STAYS},
           "changed": {"n": len(keys), "sample": sample_id(f"{s}:{h}" for s, h in keys), "cells": len(changed),
                       "list": changed}}
    for h in STAYS:
        at_h = [s for s in sorted(main) if h in main[s]]
        out["changed"][f"at_{h}"] = {"n": len(at_h), "sample": sample_id(f"{s}:{h}" for s in at_h),
                                    "cells": sum(1 for c in changed if c[1] == h)}
    return out


def monotonicity(m: dict, all_runs: dict) -> dict:
    """R3's check: if k_A < k_B in every month from 1972 to 2025, renter minus buyer must be higher under A in every
    cell. Checked in the main run and, since R15 changes neither ratio, in every sensitivity run too."""
    below = [k for k in m["months"] if m["k_a"][rb.quarter_of(k)] < m["k_b"][k[0]]]
    holds = len(below) == len(m["months"])
    checked = 0
    if holds:
        for name, runs in all_runs.items():
            for s, pair in runs.items():
                if not rb.lead_higher(pair["a"], pair["b"]):
                    raise SystemExit(f"R3 check failed: {name}, start {s}: renter minus buyer is not higher under A")
                checked += len(pair["a"].year_ends)
    return {"k_a_below_k_b_every_month": holds, "months": len(m["months"]), "months_below": len(below),
            "asserted": holds, "cells_checked": checked, "runs_checked": sorted(all_runs) if holds else []}


# --- predictions (design section 6) ---------------------------------------------------------------------------------

def predictions(sp: dict, table: dict, be: dict, ties: dict) -> dict:
    """Design section 6, scored on the main run. A prediction whose premise is empty is None (not testable)."""
    ex, ss = sp["owner_example"]["share_pct"], list(START_YEARS)
    above = {lv: sum(1 for s in ss if sp["by_start"][str(s)][lv]["split_pct"] > ex) for lv in LEVELS}
    low = {lv: sp["summary"][lv]["min_start"] for lv in LEVELS}
    c5, c30 = counts(table, 5), counts(table, MAX_H)
    early, eighties = counts(table, 10, 1972, 1976), counts(table, 10, 1980, 1989)
    c10 = counts(table, 10)
    p5 = be["summary"]["ten_years"]["agreed"]
    rent30 = c30["rent_starts"]
    cheap = [s for s in rent30 if (ties["30"]["by_start"][str(s)]["a"]["share"] is not None
                                   and ties["30"]["by_start"][str(s)]["a"]["share"] < 0.5)]
    out = {
        "P1": {"n": len(ss), "sample": sample_id(ss), "b_above_example": above["b"], "a_above_example": above["a"],
               "lowest_start": low, "true": above["b"] == len(ss) and above["a"] >= 45
               and all(1979 <= low[lv] <= 1985 for lv in LEVELS)},
        "P2": {"n": c5["n"], "sample": c5["sample"], "rent": c5["rent"], "true": c5["rent"] > c5["n"] / 2},
        "P3": {"early": {"n": early["n"], "sample": early["sample"], "buy": early["buy"]},
               "eighties": {"n": eighties["n"], "sample": eighties["sample"], "rent": eighties["rent"]},
               "true": early["buy"] > early["n"] / 2 and eighties["rent"] > eighties["n"] / 2},
        "P4": {"n": c30["n"], "sample": c30["sample"], "rent": c30["rent"], "true": c30["rent"] > c30["n"] / 2},
        "P5": {"n": be["summary"]["ten_years"]["n"], "sample": be["summary"]["ten_years"]["sample"],
               "median": p5["median_counting_not_within_as_longer"], "median_not_within_data": p5["median_is_not_within_data"],
               "true": p5["median_is_not_within_data"] or p5["median_counting_not_within_as_longer"] > 5},
        "P6": {"n": len(rent30), "sample": sample_id(rent30), "below_half": len(cheap),
               "true": None if not rent30 else len(cheap) >= len(rent30) / 2},
        "P7": {"n": c10["n"], "sample": c10["sample"], "depends": c10["depends"], "true": c10["depends"] >= c10["n"] / 5},
    }
    flags = [v["true"] for v in out.values()]
    return {**out, "n": len(flags), "n_true": sum(1 for f in flags if f is True),
            "n_untestable": sum(1 for f in flags if f is None)}


# --- inputs the post may quote ------------------------------------------------------------------------------------------

def annual_returns(m: dict, fee: dict) -> dict:
    """The market's and the fund's compounded return by calendar year, in percent, and annualized over 1972 to 2025."""
    def year_pct(y: int, f: float) -> float:
        return 100 * (math.prod(1 + m["market_pct"][(y, k)] / 100 - f / 12 for k in range(1, 13)) - 1)
    market = {y: year_pct(y, 0.0) for y in YEARS}
    fund = {y: year_pct(y, fee[y]) for y in YEARS}
    span = len(YEARS)
    return {"market_pct": by_year(market), "fund_pct": by_year(fund), "first_year": FIRST_START, "last_year": LAST_YEAR,
            "n": span, "sample": sample_id(YEARS),
            "market_annualized_pct": 100 * (math.prod(1 + v / 100 for v in market.values()) ** (1 / span) - 1),
            "fund_annualized_pct": 100 * (math.prod(1 + v / 100 for v in fund.values()) ** (1 / span) - 1)}


def input_section(d: dict, m: dict) -> dict:
    rights = d["french_rights"]
    return {
        "pmms": {"rate_pct": by_year(m["rate_year"]), "points": by_year(m["points_year"]), "p0": by_year(m["p0"]),
                 "p_fix": {"value": m["p_fix"], "n": m["p_fix_weeks"], "sample": m["p_fix_sample"],
                           "first_year": P_FIX_YEARS[0], "last_year": P_FIX_YEARS[-1]},
                 "first_year_without_points": m["first_year_without_points"]},
        "loan_costs": {"cfpb_share": by_year({y: m["cfpb_costs"][y] / (m["cfpb_amounts"][y] * 1000) for y in P_FIX_YEARS}),
                       "cfpb_total_costs": by_year(m["cfpb_costs"]), "cfpb_loan_amount_thousands": by_year(m["cfpb_amounts"]),
                       "c_np": {"value": m["c_np"], "n": len(P_FIX_YEARS), "sample": sample_id(P_FIX_YEARS),
                                "cfpb_mean_share": m["cfpb_mean_share"]},
                       "buy_cost": by_year({y: rb.buying_cost(m["p0"][y], m["c_np"]) for y in YEARS})},
        "value": {"new_house_index": by_year({y: d["new_house"][y] for y in range(1971, 1976)}),
                  "index": {qkey(q): m["index"][q] for q in m["quarters"]},
                  "index_purchase_only_chained": {qkey(q): m["index_po"][q] for q in m["quarters"]},
                  "depreciation": by_year(m["d"]), "first_fhfa_year": FIRST_FHFA[0], "last_bridge_year": rb.LAST_BRIDGE_YEAR},
        "rent_ratio": {"a_last_workbook_quarter": qkey(DLM_LAST), "b_by_year": by_year(m["k_b"]),
                       "b_scope_check": by_year(m["scope"])},
        "property_tax": {"by_year": by_year(m["tau"]), "source": by_year(m["source"]),
                         "acs_medians_read": m["medians_read"]},
        "insurance": {"by_year": by_year(m["iota"]), "iota_2005": m["iota_2005"],
                      "iota_late": {"value": m["iota_late"], "n": len(NAIC_YEARS), "sample": sample_id(NAIC_YEARS)},
                      "naic_ratio": by_year(m["naic_ratio"])},
        "upkeep": {"by_year": by_year(m["u"]), "routine": by_year(m["routine"]), "improvements": by_year(m["improvements"]),
                   "owner_share": by_year(m["owner_share"]), "high_by_year": by_year(m["u_high"])},
        "carrying": {k: by_year(v) for k, v in m["carry"].items()},
        "stocks": annual_returns(m, m["fee"]["ici"]),
        "sensitivity": {k: m[k] for k in ("tax_low", "tax_high", "iota_low", "iota_high", "routine_low",
                                          "naic_forms_premium")},
        "french_copyright": {"line": rights, "year": int(rights.split()[1])},
    }


def rules() -> dict:
    return {"price": rb.PRICE, "loan_share": rb.LOAN, "down_share": rb.PRICE - rb.LOAN, "term_months": rb.TERM,
            "term_years": rb.TERM // 12, "sell_share": rb.SELL, "refi_spacing_months": rb.REFI_SPACING,
            "refi_min_left_months": rb.REFI_MIN_LEFT, "refi_drop_pp": rb.REFI_DROP_PCT, "first_start": FIRST_START,
            "last_start": LAST_YEAR, "last_year": LAST_YEAR, "max_h": MAX_H, "stays": list(STAYS),
            "labeled_first": LABELED[0], "labeled_last": LABELED[1], "from_start": FROM, "tie_h": list(TIE_H),
            "household_start": HOUSEHOLD_START, "first_improvement_year": rb.FIRST_IMPROVEMENT_YEAR,
            "insurance_ramp": list(rb.INSURANCE_RAMP), "fee_carried_back_from": FEE_FIRST, "vanguard_fee": VANGUARD_FEE,
            "low": {"buy_share": LOW_BUY, "sell_share": LOW_SELL}, "high": {"buy_add_share": HIGH_BUY_ADD, "sell_share": HIGH_SELL},
            "purchase_only_from": qkey(PO_LINK), "levels": list(LEVELS), "tie_floor_share": rb.TIE_FLOOR}


def cell_output(table: dict) -> dict:
    return {str(s): {str(h): c for h, c in sorted(table[s].items())} for s in sorted(table)}


# --- quantities the draft states (step 6), derived from the results above ----------------------------------------------

def year_runs(years) -> dict:
    """Consecutive runs of years, in order: {"n_runs": k, "r1": {"first": a, "last": b}, ...}."""
    runs: list[list[int]] = []
    for y in sorted(int(x) for x in years):
        if runs and y == runs[-1][1] + 1:
            runs[-1][1] = y
        else:
            runs.append([y, y])
    return {"n_runs": len(runs), **{f"r{i}": {"first": a, "last": b} for i, (a, b) in enumerate(runs, 1)}}


def household_verdicts(hh: dict) -> dict:
    """R14's household at each December, read with R10's rule: runs of the years in which each verdict holds."""
    by = hh["by_year"]
    ahead = {y: tuple(rb.ahead(by[y][lv]["buyer"], by[y][lv]["renter"]) for lv in LEVELS) for y in by}
    verdict = {y: rb.verdict(*ahead[y]) for y in by}
    out = {}
    for name, v in (("buy", rb.BUY), ("rent", rb.RENT), ("depends", rb.DEPENDS)):
        years = [y for y in by if verdict[y] == v]
        out[name] = {"years": len(years), **year_runs(years)}
    return out


def tax_check(acs: dict) -> dict:
    """A2's cross-check of R7a, as profile_data.py prints it: in the years with both ACS measures, how far the ratio of
    medians (B25103_001 over B25077_001, R7a's 2005 to 2009 measure) sits above the aggregate ratio (B25090_001 over
    B25082_001, R7a's measure from 2010), in percent."""
    def gap_pct(y: int) -> float:
        medians = acs[(y, "B25103_001")] / acs[(y, "B25077_001")]
        aggregate = acs[(y, "B25090_001")] / acs[(y, "B25082_001")]
        return 100 * (medians / aggregate - 1)
    years = range(2010, 2020)
    gaps = {y: gap_pct(y) for y in years}
    lo, hi = min(years, key=gaps.get), max(years, key=gaps.get)
    return {"first_year": years[0], "last_year": years[-1], "years": len(gaps),
            "years_above": sum(1 for g in gaps.values() if g > 0), "by_year_pct": by_year(gaps),
            "min_gap_pct": gaps[lo], "min_year": lo, "max_gap_pct": gaps[hi], "max_year": hi,
            "last_year_with_both": LAST_YEAR, "last_year_gap_pct": gap_pct(LAST_YEAR)}


def multiples_30(cells_out: dict, ties_30: dict) -> dict:
    """R10's renter-to-buyer multiple after 30 years, per level, over the start years with a 30-year history."""
    ss = sorted(ties_30["by_start"], key=int)
    out = {"n": len(ss), "sample": ties_30["summary"]["sample"]}
    for lv in LEVELS:
        m = {s: cells_out[s][str(MAX_H)][lv]["multiple"] for s in ss}
        lo, hi = min(ss, key=m.get), max(ss, key=m.get)
        out[lv] = {"min": m[lo], "min_start": int(lo), "max": m[hi], "max_start": int(hi),
                   "median": statistics.median(m.values())}
    return out


def rappaport_decades_10(results: dict) -> dict:
    """R16's comparison with Rappaport (2010): the 10-year verdicts of the start years in the decades whose ten-year
    stays Rappaport found owners ahead in. Added with the critics' round before fact-check round 1."""
    h10 = results["headline"]["10"]["all"]
    starts = [s for s in range(h10["first_start"], h10["last_start"] + 1) if s // 10 * 10 in RAPPAPORT_OWNER_DECADES]
    counts = {name: sum(1 for s in starts if s in h10[f"{name}_starts"]) for name in ("buy", "rent", "depends")}
    return {**counts, "n": len(starts), "first_start": min(starts), "last_start": max(starts),
            "sample": sample_id(starts)}


def derived(results: dict, acs: dict) -> dict:
    """Every quantity the draft states that no key above holds, computed from the keys above (and, for A2's
    cross-check, from the ACS cells the build reads). Added for step 6; no key above changes."""
    ex, be, sens = results["split"]["owner_example"], results["break_even"]["by_start"], results["sensitivities"]
    medians = results["inputs"]["property_tax"]["acs_medians_read"]   # R7a's years on the ACS ratio of medians
    stays = [int(s) for s, v in be.items() if v["agreed"]["stays"]]
    led = [int(s) for s, v in be.items() if v["agreed"]["within_data"]]
    last_stays = max(stays)
    return {
        "owner_example": {"gap": ex["outlay"] - ex["rent"]},
        "verdict_runs": {f"h{h}": {name: year_runs(results["headline"][str(h)]["all"][f"{name}_starts"])
                                   for name in ("buy", "rent", "depends")} for h in STAYS},
        "household": household_verdicts(results["household"]),
        "break_even": {"stays_start": last_stays, "stays_years": be[str(last_stays)]["h_max"],
                       "stays_is_last_led": last_stays == max(led), "led_runs": year_runs(led)},
        "multiple_30": multiples_30(results["cells"], results["share_to_tie"][str(MAX_H)]),
        "rappaport_decades_10": rappaport_decades_10(results),
        "sensitivity_summary": {"runs": len(sens),
                                "runs_buy_30_zero": sum(1 for v in sens.values() if v["counts"][str(MAX_H)]["all"]["buy"] == 0),
                                "runs_rent_30_every": sum(1 for v in sens.values() if v["counts"][str(MAX_H)]["all"]["rent"]
                                                          == v["counts"][str(MAX_H)]["all"]["n"])},
        "tax_check": {**tax_check(acs), "medians_first_year": min(medians), "medians_last_year": max(medians)},
    }


def cell_summary(table: dict) -> dict:
    """How many cells there are, and in how many a buyer's net worth is not above zero (where a multiple misleads)."""
    keys = [(s, h) for s in sorted(table) for h in sorted(table[s])]
    return {"n": len(keys), "sample": sample_id(f"{s}:{h}" for s, h in keys),
            "buyer_nw_not_positive": {lv: sum(1 for s, h in keys if table[s][h][lv]["buyer_nw"] <= 0) for lv in LEVELS}}


def no_verbatim(results: dict, banned: set) -> None:
    """Stop if any float in results.json is in banned."""
    hits = []

    def walk(o, path: str) -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, f"{path}.{k}" if path else str(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")
        elif isinstance(o, float) and o in banned:
            hits.append(path)

    walk(results, "")
    if hits:
        raise SystemExit(f"results.json would carry {len(hits)} AEI or ICI values unchanged, e.g. {hits[:3]}")


def main() -> None:
    pdata.check_hashes()
    d = inputs()
    m = prepare(d)
    all_runs = {v.name: run_all(m, v) for v in (MAIN,) + SENSITIVITIES}
    runs = all_runs[MAIN.name]
    table = cells(runs)
    sp, be, ties = split(m), break_evens(table), shares_to_tie(runs)
    results = {"rules": rules(), "inputs": input_section(d, m), "split": sp, "cells": cell_output(table),
               "cell_summary": cell_summary(table), "headline": headline(table), "break_even": be, "share_to_tie": ties, "household": household(d, runs),
               "refinancing": refinancings(runs), "checks": {"r3_monotonicity": monotonicity(m, all_runs)},
               "sensitivities": {v.name: sensitivity(v.name, v.rule, cells(all_runs[v.name]), table) for v in SENSITIVITIES}}
    results["predictions"] = predictions(sp, table, be, ties)
    results["derived"] = derived(results, d["acs"])
    no_verbatim(results, {m["k_a"][q] for q in m["quarters"] if q <= DLM_LAST} | {v / 100 for v in d["ici"].values()})
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
        fh.write("\n")
    h = results["headline"]
    print("; ".join(f"{s} years: buy {h[str(s)]['all']['buy']}, rent {h[str(s)]['all']['rent']}, depends "
                    f"{h[str(s)]['all']['depends']} of {h[str(s)]['all']['n']}" for s in STAYS))
    print(f"R3 check: k_A below k_B in every month {results['checks']['r3_monotonicity']['k_a_below_k_b_every_month']}, "
          f"cells asserted {results['checks']['r3_monotonicity']['cells_checked']}")
    print("wrote results.json")


if __name__ == "__main__":
    main()
