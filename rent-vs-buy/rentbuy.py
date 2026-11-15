"""The buy-or-rent-and-invest model of design rules R1 to R13 and R15 (docs/2026-11-13-rent-vs-buy-design.md, as
amended by A1 and A2), as pure functions.

No file access here: build_analysis.py reads the pinned data through profile_data.py and passes plain sequences and
mappings in, so every input series is an argument and test_rentbuy.py runs the model on small made-up series.
Conventions: the home costs 1 at purchase (R2), so every amount is a share of the price; month 1 is January of the
start year; a rate in percent is named *_pct, and every other rate is a decimal share (R1).
"""
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

Month = tuple[int, int]          # (year, month 1 to 12)
Quarter = tuple[int, int]        # (year, quarter 1 to 4)

PRICE = 1.0                      # R2: P0 = 1
LOAN = 0.80                      # R4: L0, 80% of the price
TERM = 360                       # R4: 30 years of monthly payments
SELL = 0.06                      # R6: selling costs, a share of the value
REFI_SPACING = 12                # R9: months since the purchase or the last refinancing
REFI_MIN_LEFT = 60               # R9: months of the loan that must remain
REFI_DROP_PCT = 1.00             # R9: percentage points below the loan's current rate
FLOAT_GUARD_PCT = 1e-9           # R9's comparison, made in percent, allows this much rounding in the weekly means
LAST_BRIDGE_YEAR = 1974          # R2: depreciation is charged on bridge months up to December 1974
FIRST_IMPROVEMENT_YEAR = 1975    # R7c: improvements are charged from January 1975 only
INSURANCE_RAMP = (2005, 2022)    # R7b: iota_2005 up to 2005, a straight line to iota_late in 2022, iota_late after
TIE_FLOOR = 0.0                  # R12: the share reported when s <= 0, where the day-one sum alone ties or wins
BUY, RENT, DEPENDS = "buy", "rent", "depends on the rent"                    # R10
SHARE, ZERO, CANNOT_TIE, NO_GAP = "share", "zero", "cannot tie", "no gap"   # R12


def mean(xs: Sequence[float]) -> float:
    """Arithmetic mean; an empty sequence is an error, never a silent zero."""
    if not xs:
        raise ValueError("mean of an empty sequence")
    return math.fsum(xs) / len(xs)


# --- time (R1) ------------------------------------------------------------------------------------------------------

def months_from(start: int, years: int) -> list[Month]:
    """R1: the months of a run, January of the start year first, for a whole number of years."""
    return [(y, m) for y in range(start, start + years) for m in range(1, 13)]


def quarter_of(month: Month) -> Quarter:
    """R1: a quarterly series gives each month its quarter's value."""
    return month[0], (month[1] - 1) // 3 + 1


def weekly_means(weeks: Sequence[tuple[tuple[int, int, int], float | None]], by_month: bool = False) -> dict:
    """R1: a weekly PMMS value averaged over the weeks dated in each year (or each month). Weeks without a value (None)
    are left out, so a period with no value at all is absent from the result."""
    groups: dict = {}
    for (y, m, _), v in weeks:
        if v is not None:
            groups.setdefault((y, m) if by_month else y, []).append(v)
    return {k: mean(v) for k, v in groups.items()}


def year_mean(quarterly: Mapping[Quarter, float], year: int) -> float:
    """The mean of a year's four quarter-end values (R2, R3, R7c); a year without all four stops the build."""
    try:
        return mean([quarterly[(year, q)] for q in (1, 2, 3, 4)])
    except KeyError as e:
        raise SystemExit(f"no quarter-end value {e} in {year}") from e


def share_of_stock(flow: Mapping[int, float], stock: Mapping[Quarter, float], years: Sequence[int]) -> dict[int, float]:
    """An annual flow over the mean of the year's four quarter-end stock values: d(y) in R2, k_B(y) in R3, and
    routine(y) and improvements(y) in R7c."""
    return {y: flow[y] / year_mean(stock, y) for y in years}


# --- the home's value (R2) ------------------------------------------------------------------------------------------

def interpolate_quarter(annual: Mapping[int, float], q: Quarter) -> float:
    """R2: annual index values placed at mid-year and interpolated log-linearly to the quarter's midpoint."""
    y, k = q
    mid = y + (2 * k - 1) / 8                       # 0.125, 0.375, 0.625, 0.875 into the year
    lo = math.floor(mid - 0.5)                      # the year whose mid-year point is the last one at or before mid
    w = mid - (lo + 0.5)
    try:
        return math.exp((1 - w) * math.log(annual[lo]) + w * math.log(annual[lo + 1]))
    except KeyError as e:
        raise SystemExit(f"no annual value {e} for quarter {y}Q{k}") from e


def value_index(annual_new: Mapping[int, float], fhfa: Mapping[Quarter, float], first_fhfa: Quarter,
                bridge: Sequence[Quarter]) -> dict[Quarter, float]:
    """R2: J is the FHFA index from first_fhfa on; for a bridge quarter q before it,
    J(q) = FHFA(first_fhfa) x C(q) / C(first_fhfa), with C the interpolated new-house index."""
    if any(q >= first_fhfa for q in bridge):
        raise SystemExit("a bridge quarter is not before the first FHFA quarter")
    c0 = interpolate_quarter(annual_new, first_fhfa)
    out = {q: fhfa[first_fhfa] * interpolate_quarter(annual_new, q) / c0 for q in bridge}
    return {**out, **fhfa}


def depreciation(months: Sequence[Month], rate: Mapping[int, float],
                 last_bridge_year: int = LAST_BRIDGE_YEAR) -> list[float]:
    """R2: D(t), the product of (1 - d(y)/12) over the bridge months before month t, y the month's year. D(1) = 1, and
    D stays fixed once the bridge months are over (from January 1975)."""
    out, factor = [], 1.0
    for y, _ in months:
        out.append(factor)
        if y <= last_bridge_year:
            factor *= 1 - rate[y] / 12
    return out


def value_path(months: Sequence[Month], index: Mapping[Quarter, float], factors: Sequence[float]) -> list[float]:
    """R2: V(t) = [J(q(t)) / J(q0)] x D(t), q0 the first quarter of the start year."""
    j0 = index[quarter_of(months[0])]
    return [index[quarter_of(m)] / j0 * f for m, f in zip(months, factors, strict=True)]


def chain(early: Mapping, late: Mapping, keys: Sequence, link) -> dict:
    """R15.1 and R15.3: the early index through the link period, then the early level at the link times the late
    index's growth since the link. A period the late (or early) index does not publish (None) holds the previous level,
    and the next published period chains through its own value: October 2025 is skipped and November chains to
    September."""
    out: dict = {}
    prev = None
    for k in keys:
        source = early if k <= link else late
        v = source.get(k)
        if v is None:
            if prev is None:
                raise SystemExit(f"chain: no value for {k}")
            out[k] = prev
        else:
            out[k] = v if k <= link else early[link] * v / late[link]
        prev = out[k]
    return out


# --- the rent of the same home (R3) ---------------------------------------------------------------------------------

def published_mean(monthly: Mapping[Month, float | None], q: Quarter) -> float:
    """R3: the mean of a quarter's monthly values; a month BLS did not publish (None or absent) is skipped."""
    y, k = q
    values = [monthly.get((y, m)) for m in range(3 * k - 2, 3 * k + 1)]
    published = [v for v in values if v is not None]
    if not published:
        raise SystemExit(f"no published month in {y}Q{k}")
    return mean(published)


def extend_ratio(ratio: Mapping[Quarter, float], last: Quarter, rent_index: Mapping[Month, float | None],
                 price_index: Mapping[Quarter, float], quarters: Sequence[Quarter]) -> dict[Quarter, float]:
    """R3 level A: the workbook's ratio up to its last quarter, then
    k_A(q) = k_A(last) x [OER(q) / OER(last)] / [PO(q) / PO(last)]."""
    oer0, po0 = published_mean(rent_index, last), price_index[last]
    out = {}
    for q in quarters:
        if q <= last:
            out[q] = ratio[q]
        else:
            out[q] = ratio[last] * (published_mean(rent_index, q) / oer0) / (price_index[q] / po0)
    return out


def ratio_rent(ratio: Sequence[float], value: Sequence[float]) -> list[float]:
    """R3: r(t) = k(t) x V(t) / 12."""
    return [k * v / 12 for k, v in zip(ratio, value, strict=True)]


# --- the buyer's costs (R4 to R7) -----------------------------------------------------------------------------------

def payment(balance: float, annual_rate: float, months_left: int) -> float:
    """R4: m = B x (i/12) / (1 - (1 + i/12)^(-n)), B the balance and n the months left; zero once none are left."""
    if months_left <= 0:
        return 0.0
    j = annual_rate / 12
    if j == 0:
        return balance / months_left
    return balance * j / (1 - (1 + j) ** (-months_left))


def other_loan_costs(total_costs: Mapping[int, float], amounts_thousands: Mapping[int, float], points: float) -> float:
    """R5: c_np = the mean over the years given of the median total loan costs over the median loan amount (published
    in thousands, so times 1,000), less the mean points over the same years as a share of the loan."""
    years = sorted(total_costs)
    if years != sorted(amounts_thousands):
        raise SystemExit("loan costs and loan amounts cover different years")
    return mean([total_costs[y] / (amounts_thousands[y] * 1000) for y in years]) - points / 100


def buying_cost(points: float, c_np: float, loan: float = LOAN) -> float:
    """R5: K_buy = (p0 / 100 + c_np) x L0."""
    return (points / 100 + c_np) * loan


def fill_straight(known: Mapping[int, float], years: Sequence[int]) -> dict[int, float]:
    """R7a: a year with no survey value lies on the straight line between the nearest years with values; a year
    before the first value takes that value (1972 takes 1973's). A year after the last value stops the build."""
    have = sorted(known)
    out = {}
    for y in years:
        if y in known:
            out[y] = known[y]
        elif y < have[0]:
            out[y] = known[have[0]]
        elif y > have[-1]:
            raise SystemExit(f"no survey value at or after {y}")
        else:
            lo, hi = max(k for k in have if k < y), min(k for k in have if k > y)
            out[y] = known[lo] + (y - lo) / (hi - lo) * (known[hi] - known[lo])
    return out


def acs_ratio(cells: Mapping[tuple[int, str], float], years: Sequence[int], numerator: str,
              denominator: str) -> dict[int, float]:
    """R7a: an ACS ratio by year, cells[(y, numerator)] / cells[(y, denominator)]. A year without both cells stops the
    build and is named, so a year the rule takes from the ACS never falls back to the straight line (A2)."""
    missing = [f"{y} {c}" for y in years for c in (numerator, denominator) if (y, c) not in cells]
    if missing:
        raise SystemExit(f"R7a: no pinned ACS value for {', '.join(missing)}")
    return {y: cells[(y, numerator)] / cells[(y, denominator)] for y in years}


def insurance_path(early: float, late: float, years: Sequence[int],
                   ramp: tuple[int, int] = INSURANCE_RAMP) -> dict[int, float]:
    """R7b: iota_2005 up to 2005, a straight line from iota_2005 in 2005 to iota_late in 2022, and iota_late after."""
    a, b = ramp
    return {y: early if y <= a else late if y >= b else early + (y - a) / (b - a) * (late - early) for y in years}


def upkeep(routine: Mapping[int, float], improvements: Mapping[int, float], years: Sequence[int],
           first_improvement: int = FIRST_IMPROVEMENT_YEAR) -> dict[int, float]:
    """R7c: u(y) = routine(y) + improvements(y), each already a share of value; improvements from 1975 only."""
    return {y: routine[y] + (improvements[y] if y >= first_improvement else 0.0) for y in years}


# --- the fund (R8) --------------------------------------------------------------------------------------------------

def fund_returns(months: Sequence[Month], market_pct: Mapping[Month, float], fee: Mapping[int, float]) -> list[float]:
    """R8: R(t) = (Mkt-RF + RF) / 100 - f(y) / 12, with market_pct[m] = Mkt-RF + RF as published (percent) and f(y) a
    decimal share."""
    return [market_pct[m] / 100 - fee[m[0]] / 12 for m in months]


def grow(start: float, flows: Sequence[float], returns: Sequence[float]) -> list[float]:
    """R8: each month the balance earns R(t), then the month's investment is added. The balance after each month."""
    out, w = [], start
    for f, r in zip(flows, returns, strict=True):
        w = w * (1 + r) + f
        out.append(w)
    return out


# --- the loan, month by month (R4, R9) ------------------------------------------------------------------------------

@dataclass(frozen=True)
class Refinancing:
    """R9's inputs for one run, one entry per month of the run (month 1 first)."""
    month_rate_pct: Sequence[float]   # the month's mean PMMS 30-year rate, percent
    month_points: Sequence[float]     # the month's mean PMMS fees and points, p_fix for a month with none
    c_np: float                       # R5: the loan's other costs, a share of the balance


@dataclass(frozen=True)
class LoanMonth:
    payment: float      # this month's payment (zero after month 360)
    balance: float      # after this month's payment and any refinancing
    refi_cost: float    # R9: paid this month as part of the outlay; zero in a month without one
    rate_pct: float     # the loan's rate after this month


def loan_schedule(n_months: int, rate_pct: float, refi: Refinancing | None, loan: float = LOAN,
                  term: int = TERM) -> list[LoanMonth]:
    """R4: each month the balance grows by i/12 and falls by the payment, which follows R4's formula for the months
    left. R9: at the end of month t, after its payment, the buyer refinances when at least 12 months have passed since
    the purchase or the last refinancing, at least 60 months remain, and the month's mean rate is at least one
    percentage point below the loan's current rate; the new rate is that mean, the payoff date stays the same, and the
    cost (p / 100 + c_np) x the balance is paid that month."""
    balance, rate, left, last = loan, rate_pct, term, 0
    out = []
    for t in range(1, n_months + 1):
        pay = payment(balance, rate / 100, left)
        if left > 0:
            balance = balance * (1 + rate / 100 / 12) - pay
            left -= 1
        cost = 0.0
        if (refi is not None and t - last >= REFI_SPACING and left >= REFI_MIN_LEFT
                and rate - refi.month_rate_pct[t - 1] >= REFI_DROP_PCT - FLOAT_GUARD_PCT):
            cost = (refi.month_points[t - 1] / 100 + refi.c_np) * balance
            rate, last = refi.month_rate_pct[t - 1], t
        out.append(LoanMonth(pay, balance, cost, rate))
    return out


# --- one household pair, one rent path (R8 to R10) -----------------------------------------------------------------

@dataclass(frozen=True)
class Flows:
    """R8, one month: both households spend max(outlay, rent) on housing plus investing."""
    outlay: float           # O(t) = the mortgage payment + carrying costs + any refinancing cost
    rent: float             # r(t)
    renter_invests: float   # O(t) - r(t) when positive
    buyer_invests: float    # r(t) - O(t) when positive


@dataclass(frozen=True)
class YearEnd:
    """R10 at the end of the December after h whole years."""
    h: int
    value: float            # V at the December
    balance: float          # the loan balance after the December payment
    buyer_fund: float
    renter_fund: float      # every dollar of each gap invested (R8); R12's W_R(1)
    renter_day_one: float   # the day-one sum alone, no gap invested; R12's W_R(0)
    any_gap: bool           # the renter had a positive gap in some month so far (R12)
    sell: float             # R6: selling costs, a share of the value

    @property
    def buyer_nw(self) -> float:
        return self.value * (1 - self.sell) - self.balance + self.buyer_fund

    @property
    def renter_nw(self) -> float:
        return self.renter_fund


@dataclass(frozen=True)
class Run:
    day_one: float
    loan: tuple[LoanMonth, ...]
    flows: tuple[Flows, ...]
    year_ends: tuple[YearEnd, ...]


def simulate(value: Sequence[float], rent: Sequence[float], carry_rate: Sequence[float], returns: Sequence[float],
             rate_pct: float, buy_cost: float, refi: Refinancing | None, sell: float = SELL,
             loan: float = LOAN) -> Run:
    """R4 to R10 for one start year and one rent path. value (V), rent (r), carry_rate (tau + iota + u of the month's
    year) and returns (R) have one entry per month, month 1 first, over a whole number of years. The buyer pays the
    down payment and buy_cost at purchase; the renter invests the same sum at the start of month 1 (R5, R8)."""
    n = len(value)
    if n == 0 or n % 12 or not len(rent) == len(carry_rate) == len(returns) == n:
        raise SystemExit(f"simulate: series of lengths {n}, {len(rent)}, {len(carry_rate)}, {len(returns)}")
    if refi is not None and not len(refi.month_rate_pct) == len(refi.month_points) == n:
        raise SystemExit("simulate: refinancing terms do not cover the run")
    schedule = loan_schedule(n, rate_pct, refi, loan)
    outlay = [lm.payment + c * v / 12 + lm.refi_cost for lm, c, v in zip(schedule, carry_rate, value)]
    gaps = [o - r for o, r in zip(outlay, rent)]
    flows = tuple(Flows(o, r, max(g, 0.0), max(-g, 0.0)) for o, r, g in zip(outlay, rent, gaps))
    day_one = (PRICE - loan) + buy_cost
    renter = grow(day_one, [f.renter_invests for f in flows], returns)
    alone = grow(day_one, [0.0] * n, returns)
    buyer = grow(0.0, [f.buyer_invests for f in flows], returns)
    year_ends = []
    for h in range(1, n // 12 + 1):
        t = 12 * h
        year_ends.append(YearEnd(h, value[t - 1], schedule[t - 1].balance, buyer[t - 1], renter[t - 1], alone[t - 1],
                                 any(g > 0 for g in gaps[:t]), sell))
    return Run(day_one, tuple(schedule), flows, tuple(year_ends))


def lead_higher(lower_rent: Run, higher_rent: Run) -> bool:
    """R3's check: the renter's net worth minus the buyer's is higher under the lower rent at every year-end."""
    return all(a.renter_nw - a.buyer_nw > b.renter_nw - b.buyer_nw
               for a, b in zip(lower_rent.year_ends, higher_rent.year_ends, strict=True))


# --- verdicts and measures (R10 to R14) ------------------------------------------------------------------------------

def ahead(buyer_nw: float, renter_nw: float) -> str | None:
    """R10, one rent level: 'buy' if the buyer's net worth is higher, 'rent' if the renter's is, None if equal."""
    if buyer_nw > renter_nw:
        return BUY
    if renter_nw > buyer_nw:
        return RENT
    return None


def verdict(level_a: str | None, level_b: str | None) -> str:
    """R10: 'buy' if buying is ahead under both levels, 'rent' if renting is ahead under both, else 'depends on the
    rent'."""
    if level_a == level_b and level_a in (BUY, RENT):
        return level_a
    return DEPENDS


def break_even(ahead_by_h: Sequence[bool]) -> tuple[int | None, bool | None]:
    """R11: the first h (1-based) at which the flag holds and whether it holds at every later h; (None, None) if it
    never holds within the data."""
    for h, flag in enumerate(ahead_by_h, 1):
        if flag:
            return h, all(ahead_by_h[h:])
    return None, None


def share_to_tie(buyer_nw: float, renter_none: float, renter_all: float,
                 any_gap: bool) -> tuple[str, float | None, float | None]:
    """R12: s = (NW_B - W_R(0)) / (W_R(1) - W_R(0)). Returns (label, share, raw s): 'no gap' if the renter never had a
    positive gap; 'cannot tie' if s > 1; 'zero' with the share TIE_FLOOR (0) if s <= 0 (the day-one sum alone ties or
    wins); otherwise 'share'."""
    if not any_gap:
        return NO_GAP, None, None
    s = (buyer_nw - renter_none) / (renter_all - renter_none)
    if s > 1:
        return CANNOT_TIE, None, s
    if s <= 0:
        return ZERO, TIE_FLOOR, s
    return SHARE, s, s


def month_one_split(k_month_one: float, rate_pct: float, carry: float, loan: float = LOAN) -> float:
    """R13: the month-1 rent as a percent of the buyer's month-1 outlay (mortgage payment plus carrying costs), with
    V(1) = 1."""
    return 100 * (k_month_one / 12) / (payment(loan, rate_pct / 100, TERM) + carry / 12)


def household_price(value_base: float, fhfa_start: float, fhfa_base_quarters: Sequence[float]) -> float:
    """R14: the Census 2000 median value x FHFA(start quarter) / the mean of FHFA's four quarters of 2000."""
    if len(fhfa_base_quarters) != 4:
        raise SystemExit("R14 needs the four quarters of the base year")
    return value_base * fhfa_start / mean(fhfa_base_quarters)


def in_dollars_of(amount: float, price: float, cpi_year: float, cpi_base: float) -> float:
    """R14: a share of the price, in dollars of the base year: amount x price x CPI(base) / CPI(year)."""
    return amount * price * cpi_base / cpi_year
