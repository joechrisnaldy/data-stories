"""Post 29: the house chase. Writes results.json from the frozen data files.

Every rule is the pre-registration's (docs/2026-11-09-genz-house-chase-design.md, R1 to R16, amendment A1); the rule
each step implements is named beside it. Readers, hashes and row choices live in profile_data.py and the chase
arithmetic in chase.py (checked by test_chase.py), so no rule is written twice. Run from the post folder:
python3 build_analysis.py
"""
import hashlib
import json
import statistics

import chase as ch
import profile_data as pdata

LAST = 2025                                 # the last year with income, price and rate data
AGE_START = 25                              # R1: the saver turns 25 in the start year
CE_FIRST, CE_LAST = 1984, 2024              # R9, R12: years in the CE file
SHARES = (0.05, 0.10, 0.15, 0.20)           # R3
HEADLINE = 0.10                             # R3 (owner, design checkpoint)
DOWN, DOWN_CHECK = 0.20, 0.10               # R5
LIKE_YEARS = 3                              # R7
PROGRESS_YEARS = (1, 2, 3, 4)               # R7's table
BRACKETS = ((25, 34, "25 to 34 Years"), (35, 44, "35 to 44 Years"), (45, 54, "45 to 54 Years"))   # R2
CX_CODE = {"25 to 34 Years": "03", "35 to 44 Years": "04", "45 to 54 Years": "05"}               # R9: same ages in CE
TREATS = ("FOODAWAY", "ENTRTAIN", "PERSCARE")   # R9, R10, R12
NARROW, NARROW_YEARS = "SNKNABEV", range(2010, 2022)   # R10
EXISTING_FROM, ANCHOR_YEAR = 1975, 2000     # R8(b)
ACS_YEAR = 2025                             # R8(b): the vintage of data/census_acs_b25077_2025.dat
SALARY_FIRST, WEEKS = 1979, 52              # R11
REAL_FROM = 1979                            # R13
IDN_FIRST, IDN_LAST = 2018, 2024            # R15; the method break inside the window is read from the ILO file
KEY = {"all": "all", "25 to 34": "age25_34", "urban": "urban"}    # R15: result names for the ILO series
GRADS_MID = (2018, 2020)                    # R14: the years between the long quiet stretch and the streak
HVS_FIRST, HVS_LAST = "1982", "2025*"       # R16
HVS_SKIP = {"1993", "2002"}                 # R16: the unrevised columns; 1993r1 and 2002r2 are used


def sample_id(items) -> str:
    """A short hash of the entities a statistic was computed on, so prose can pair figures from one sample."""
    return hashlib.sha256(json.dumps(sorted(map(str, items))).encode()).hexdigest()[:12]


def src(key: str) -> dict:
    """The values of one stored, quoted source (docs/sources.json), checked by the gate's sources check."""
    with open("docs/sources.json", encoding="utf-8") as fh:
        return json.load(fh)[key]["values"]


def generations() -> tuple:
    """R1: start years are Pew Research Center's birth years plus 25; Gen Z, with no end year, runs to the last year."""
    out, prev = [], None
    for g in ("boomers", "genx", "millennials", "genz"):
        v = src(f"pew_{g}")
        first, last = v["first"] + AGE_START, (v["last"] + AGE_START if "last" in v else LAST)
        if prev is not None and first != prev + 1:
            raise SystemExit(f"Pew birth years leave a gap or overlap before {g}")
        out.append((g, first, last))
        prev = last
    return tuple(out)


GENERATIONS = generations()
FIRST_START = GENERATIONS[0][1]


def med(xs: list) -> float | None:
    return statistics.median(xs) if xs else None


def pct_change(a: float, b: float) -> float:
    return 100 * (b / a - 1)


# --- inputs -------------------------------------------------------------------------------------------

def inputs() -> dict:
    h10, h10_alt = pdata.read_h10()
    income = {b: {y: float(v) for y, v in d.items()} for b, d in h10.items()}
    income_alt = {b: {**income[b], **{y: float(v) for y, v in h10_alt.get(b, {}).items()}} for b in income}
    tbill, _ = pdata.read_tbill()
    cx = pdata.read_cx()
    treats = {b: {y: sum(cx[(i, code)][y] for i in TREATS) for y in range(CE_FIRST, CE_LAST + 1)}
              for b, code in CX_CODE.items()}
    for d in treats.values():
        d[LAST] = d[CE_LAST]                # R9: no CE data for 2025 yet; 2024 carried forward, flagged
    return {"income": income, "income_alt": income_alt, "price": {y: float(v[0]) for y, v in pdata.read_soc_price().items()},
            "rate": {y: v / 100 for y, v in tbill.items()}, "tbill_pct": tbill, "cq": pdata.read_cq_index(),
            "fhfa": pdata.read_fhfa_at(), "anchor": pdata.read_census2000_value(), "acs": pdata.read_acs2025(),
            "cx": cx, "treats": treats, "pay": pdata.read_le()["LEU0252888500"], "rs": pdata.read_rcpiurs(),
            "cpiu": pdata.read_cpiu(), "sqft": pdata.read_sqft()}


# --- the chase (R2 to R9) ----------------------------------------------------------------------------

def one_chase(d: dict, start: int, share: float = HEADLINE, down: float = DOWN, price: dict | None = None,
              rate: dict | None = None, income: dict | None = None, extra: dict | None = None) -> ch.ChaseResult:
    """R2 to R6. The path runs to 2025 or to age 54 (the last income bracket), whichever comes first; a chase still
    running at 54 before 2025 would need a bracket the design does not have, so it stops the build."""
    end = min(LAST, start + BRACKETS[-1][1] - 25)
    p = price if price is not None else d["price"]
    c = ch.contributions(start, end, share, income if income is not None else d["income"], BRACKETS, extra)
    target = {t: down * p[t] for t in range(start, end + 1)}
    res = ch.run_chase(start, end, c, target, rate if rate is not None else d["rate"])
    if not res.finished and end < LAST:
        raise SystemExit(f"chase from {start} still running at age {BRACKETS[-1][1]}")
    return res


def as_dict(r: ch.ChaseResult) -> dict:
    return {"years": r.years, "finished": r.finished, "catch_year": r.catch_year,
            "share_reached_pct": 100 * r.share_reached,
            "progress_pct": {str(n): 100 * r.progress[n - 1] for n in PROGRESS_YEARS if n <= len(r.progress)}}


def summarize(runs: dict[int, ch.ChaseResult], first: int, last: int) -> dict:
    """One generation (or any span of start years): finished chases' years, unfinished ones, R7's progress."""
    starts = [s for s in range(first, last + 1) if s in runs]
    done = [s for s in starts if runs[s].finished]
    open_ = [s for s in starts if not runs[s].finished]
    out = {"n": len(starts), "sample": sample_id(starts), "first_start": starts[0], "last_start": starts[-1],
           "finished": {"n": len(done), "sample": sample_id(done), "median_years": med([runs[s].years for s in done]),
                        "min_years": min((runs[s].years for s in done), default=None),
                        "max_years": max((runs[s].years for s in done), default=None)},
           "unfinished": {"n": len(open_), "sample": sample_id(open_), "starts": open_,
                          "median_share_pct": med([100 * runs[s].share_reached for s in open_])}}
    for n in PROGRESS_YEARS:
        have = [s for s in starts if len(runs[s].progress) >= n]
        out[f"after{n}"] = {"n": len(have), "sample": sample_id(have),
                            "median_pct": med([100 * runs[s].progress[n - 1] for s in have])}
    return out


def by_generation(runs: dict[int, ch.ChaseResult]) -> dict:
    return {g: summarize(runs, a, b) for g, a, b in GENERATIONS if any(s in runs for s in range(a, b + 1))}


def chase_section(d: dict) -> dict:
    starts = range(FIRST_START, LAST + 1)
    head = {s: one_chase(d, s) for s in starts}
    out = {"rules": {"share_pct": 100 * HEADLINE, "down_pct": 100 * DOWN, "first_start": FIRST_START, "last": LAST,
                     "like_years": LIKE_YEARS},
           "by_start": {str(s): as_dict(r) for s, r in head.items()}, "generations": by_generation(head)}
    out["shares"] = {f"{100 * s:g}": by_generation({t: one_chase(d, t, share=s) for t in starts}) for s in SHARES}
    zero = {y: 0.0 for y in d["rate"]}
    checks = {"no_interest": {s: one_chase(d, s, rate=zero) for s in starts},
              "down_10": {s: one_chase(d, s, down=DOWN_CHECK) for s in starts},
              "h10_alternate_rows": {s: one_chase(d, s, income=d["income_alt"]) for s in starts},
              "same_house": {s: one_chase(d, s, price={t: d["price"][s] * d["cq"][t] / d["cq"][s] for t in range(s, LAST + 1)})
                             for s in starts}}
    existing = {t: d["anchor"] * d["fhfa"][t] / d["fhfa"][ANCHOR_YEAR] for t in range(EXISTING_FROM, LAST + 1)}
    checks["existing_homes"] = {s: one_chase(d, s, price=existing) for s in range(EXISTING_FROM, LAST + 1)}
    out["checks"] = {k: {"generations": by_generation(v), "by_start": {str(s): as_dict(r) for s, r in v.items()}}
                     for k, v in checks.items()}
    out["checks"]["existing_homes"]["level_check"] = {
        "anchor_year": ANCHOR_YEAR, "acs_year": ACS_YEAR, "anchor_value": d["anchor"], "implied_last": existing[LAST], "acs_last": d["acs"],
        "gap_pct": pct_change(d["acs"], existing[LAST])}
    return out, head


def treat_section(d: dict, head: dict) -> dict:
    """R9: the broad treat budget saved too, start years 1984 to 2024; R10: the narrow snacks line."""
    starts = range(CE_FIRST, CE_LAST + 1)
    treat = {s: one_chase(d, s, extra=d["treats"]) for s in starts}
    base_done = [s for s in starts if head[s].finished]
    ratios = [treat[s].years / head[s].years for s in base_done]
    rescued = [s for s in starts if not head[s].finished and treat[s].finished]
    gens = {}
    for g, a, b in GENERATIONS:
        ss = [s for s in base_done if a <= s <= b]
        if ss:
            gens[g] = {"n": len(ss), "sample": sample_id(ss), "median_base_years": med([head[s].years for s in ss]),
                       "median_treat_years": med([treat[s].years for s in ss])}
    snacks = d["cx"][(NARROW, "03")]
    narrow = {str(t): {"dollars": snacks[t], "target": DOWN * d["price"][t], "target_pct": 100 * snacks[t] / (DOWN * d["price"][t]),
                       "years_to_equal": DOWN * d["price"][t] / snacks[t]} for t in NARROW_YEARS}
    pcts = [v["target_pct"] for v in narrow.values()]
    cheap, dear = min(narrow, key=lambda y: narrow[y]["dollars"]), max(narrow, key=lambda y: narrow[y]["dollars"])
    broad_last = d["treats"]["25 to 34 Years"][CE_LAST]
    return {"broad": {"first_start": CE_FIRST, "last_start": CE_LAST,
                      "by_start": {str(s): {"base": as_dict(head[s]), "treat": as_dict(treat[s])} for s in starts},
                      "base_finished": {"n": len(base_done), "sample": sample_id(base_done),
                                        "median_base_years": med([head[s].years for s in base_done]),
                                        "median_treat_years": med([treat[s].years for s in base_done]),
                                        "median_ratio": med(ratios)},
                      "rescued": {"n": len(rescued), "sample": sample_id(rescued), "starts": rescued},
                      "generations": gens, "carried_forward_year": LAST, "ce_last": CE_LAST},
            "narrow": {"group": "25 to 34", "years": narrow, "n": len(narrow), "sample": sample_id(narrow),
                       "max_target_pct": max(pcts), "min_target_pct": min(pcts), "first_year": NARROW_YEARS[0],
                       "min_dollars": narrow[cheap]["dollars"], "min_dollars_year": int(cheap),
                       "max_dollars": narrow[dear]["dollars"], "max_dollars_year": int(dear),
                       "min_years_to_equal": min(v["years_to_equal"] for v in narrow.values()),
                       "min_years_floor": int(min(v["years_to_equal"] for v in narrow.values())),
                       "last_year": NARROW_YEARS[-1], "last_dollars": snacks[NARROW_YEARS[-1]]},
            "broad_last": {"year": CE_LAST, "dollars": broad_last, "target": DOWN * d["price"][CE_LAST],
                           "years_to_equal": DOWN * d["price"][CE_LAST] / broad_last,
                           "income_pct": 100 * broad_last / d["income"]["25 to 34 Years"][CE_LAST]}}


# --- the other measures (R11 to R16) -----------------------------------------------------------------

def with_pct(stats: dict) -> dict:
    """The same statistics under names ending in _pct, for a series already in percent (the gate reads the suffix)."""
    return {**stats, **{f"{k}_pct": stats[k] for k in ("first", "last", "max", "min")}}


def series_stats(s: dict) -> dict:
    """First, last, highest and lowest of a yearly series; every year that ties for the top or the bottom is listed."""
    ys = sorted(s)
    hi, lo = max(s.values()), min(s.values())
    return {"by_year": {str(y): s[y] for y in ys}, "first_year": ys[0], "first": s[ys[0]], "last_year": ys[-1],
            "last": s[ys[-1]], "max": hi, "max_years": [y for y in ys if s[y] == hi], "max_year": next(y for y in ys if s[y] == hi),
            "min": lo, "min_years": [y for y in ys if s[y] == lo], "min_year": next(y for y in ys if s[y] == lo),
            "n": len(ys), "sample": sample_id(ys)}



def ratio_section(d: dict) -> dict:
    """R11: the new-home median price in years of pay, nominal over nominal."""
    inc = d["income"]["25 to 34 Years"]
    hh = {y: d["price"][y] / inc[y] for y in range(FIRST_START, LAST + 1)}
    sal = {y: d["price"][y] / (WEEKS * d["pay"][y]) for y in range(SALARY_FIRST, LAST + 1)}
    out = {"household": series_stats(hh), "salary": series_stats(sal), "weeks": WEEKS}
    out["household"]["at_salary_first"] = hh[SALARY_FIRST]
    out["household_change_from_salary_first_pct"] = pct_change(hh[SALARY_FIRST], hh[LAST])
    out["salary_change_pct"] = pct_change(sal[SALARY_FIRST], sal[LAST])
    out["price"] = {"first_year": FIRST_START, "first": d["price"][FIRST_START], "last": d["price"][LAST], "last_year": LAST}
    out["income"] = {"first": inc[FIRST_START], "last": inc[LAST]}
    out["pay_annual"] = {"first_year": SALARY_FIRST, "first": WEEKS * d["pay"][SALARY_FIRST], "last": WEEKS * d["pay"][LAST]}
    return out


def share_section(d: dict) -> dict:
    """R12: eating out, entertainment and personal care over average annual expenditures, by age."""
    cx, out = d["cx"], {}
    for code, name in (("01", "all"), ("02", "under25"), ("03", "age25_34")):
        s = {y: 100 * sum(cx[(i, code)][y] for i in TREATS) / cx[("TOTALEXP", code)][y] for y in range(CE_FIRST, CE_LAST + 1)}
        out[name] = with_pct(series_stats(s))
    raw = {int(y): v for y, v in out["under25"]["by_year"].items()}
    smooth = {y: statistics.fmean([raw[y - 1], raw[y], raw[y + 1]]) for y in range(CE_FIRST + 1, CE_LAST)}
    out["under25_smoothed"] = with_pct(series_stats(smooth))
    out["age25_34_dollars_last"] = sum(cx[(i, "03")][CE_LAST] for i in TREATS)
    return out


def real_section(d: dict) -> dict:
    """R13 (amendment A1): real change, 1979 to 2025, in the stored R-CPI-U-RS; the CPI-U as a check."""
    out = {}
    for name, idx in (("rs", d["rs"]), ("cpiu", d["cpiu"])):
        f = idx[LAST] / idx[REAL_FROM]
        pay = {y: d["pay"][y] * idx[LAST] / idx[y] for y in range(REAL_FROM, LAST + 1)}
        out[name] = {"pay_change_pct": pct_change(d["pay"][REAL_FROM] * f, d["pay"][LAST]),
                     "price_change_pct": pct_change(d["price"][REAL_FROM] * f, d["price"][LAST]),
                     "pay_first_in_last_dollars": d["pay"][REAL_FROM] * f, "pay_last": d["pay"][LAST],
                     "pay_min_year": min(pay, key=pay.get), "pay_min": min(pay.values()),
                     "years_above_first": [y for y in pay if y > REAL_FROM and pay[y] > pay[REAL_FROM]]}
    out["first_year"], out["last_year"] = REAL_FROM, LAST
    sq = d["sqft"]
    out["sqft"] = {"first_year": min(sq), "first": sq[min(sq)], "max_year": max(sq, key=sq.get), "max": max(sq.values()),
                   "last_year": LAST, "last": sq[LAST]}
    return out


def grads_section() -> dict:
    """R14: NY Fed monthly rates as published; the streak of months with recent graduates above all workers."""
    rows = pdata.read_nyfed()
    k = len(rows)
    while k > 0 and rows[k - 1][2] > rows[k - 1][3]:
        k -= 1
    streak = rows[k:]
    year_mean = lambda y, i: statistics.fmean(r[i] for r in rows if r[0] == y)
    a2, b2 = GRADS_MID
    above = lambda a, b: sum(1 for r in rows if a <= r[0] <= b and r[2] > r[3])
    months = lambda a, b: sum(1 for r in rows if a <= r[0] <= b)
    return {"first": list(rows[0][:2]), "last": list(rows[-1][:2]), "n_months": len(rows), "sample": sample_id(r[:2] for r in rows),
            "streak": {"start": list(streak[0][:2]) if streak else None, "n_months": len(streak),
                       "start_year": streak[0][0], "start_month": streak[0][1], "end_year": rows[-1][0], "end_month": rows[-1][1]},
            "early": {"first": rows[0][0], "last": a2 - 1, "above": above(rows[0][0], a2 - 1), "months": months(rows[0][0], a2 - 1)},
            "mid": {"first": a2, "last": b2, "above": above(a2, b2), "months": months(a2, b2)},
            "means": {str(y): {"recent_pct": year_mean(y, 2), "all_pct": year_mean(y, 3)} for y in (2019, 2025)},
            "chatgpt_release_year": src("yale_chatgpt_release")["release_year"],
            "series": [[r[0], r[1], r[2], r[3]] for r in rows]}


def indonesia_section() -> dict:
    """R15: Bank Indonesia's index (annual mean of four quarters) against ILOSTAT median earnings, 2018 to 2024."""
    bi = {y: statistics.fmean(q) for y, q in pdata.read_bi("bi_2025q3").items() if len(q) == 4}
    newer = {y: statistics.fmean(q) for y, q in pdata.read_bi("bi_2026q3").items() if len(q) == 4}
    pay = {name: pdata.read_ilo("ilo_median_area" if name == "urban" else "ilo_median_age", lab)
           for name, lab in pdata.ILO_LABELS.items()}
    g = lambda s, a, b: pct_change(s[a], s[b])
    breaks = sorted({y for name, lab in pdata.ILO_LABELS.items()
                     for y in pdata.read_ilo_breaks("ilo_median_area" if name == "urban" else "ilo_median_age", lab)
                     if IDN_FIRST < y <= IDN_LAST})
    if len(breaks) != 1:
        raise SystemExit(f"ILO: expected one flagged break inside {IDN_FIRST} to {IDN_LAST}, found {breaks}")
    IDN_BREAK = breaks[0]
    out = {"window": [IDN_FIRST, IDN_LAST], "first_year": IDN_FIRST, "last_year": IDN_LAST,
           "index_growth_pct": g(bi, IDN_FIRST, IDN_LAST),
           "pay_growth": {f"{KEY[k]}_pct": g(v, IDN_FIRST, IDN_LAST) for k, v in pay.items()},
           "break_year": IDN_BREAK,
           "split": {"before": [IDN_FIRST, IDN_BREAK - 1], "after": [IDN_BREAK, IDN_LAST],
                     "index_pct": [g(bi, IDN_FIRST, IDN_BREAK - 1), g(bi, IDN_BREAK, IDN_LAST)],
                     "pay_pct": {k: [g(v, IDN_FIRST, IDN_BREAK - 1), g(v, IDN_BREAK, IDN_LAST)] for k, v in pay.items()}},
           "vintage_max_gap": max(abs(bi[y] - newer[y]) for y in bi if y in newer and y <= IDN_LAST),
           "n": IDN_LAST - IDN_FIRST + 1, "sample": sample_id(range(IDN_FIRST, IDN_LAST + 1))}
    out["pay_outpaced_index"] = {k: v > out["index_growth_pct"] for k, v in out["pay_growth"].items()}
    return out


def year_of_col(label: str) -> int:
    """'2025*' or '1993r1' as a year."""
    return int(label[:4])


def ownership_section() -> dict:
    """R16: HVS Table 17, under 25 and under 35 always together; 1993r1 and 2002r2 stand for those years."""
    out = {}
    for lab in pdata.HVS_ROWS:
        v = {k: x for k, x in pdata.read_hvs17()[lab].items() if k not in HVS_SKIP}
        hi, lo = max(v.values()), min(v.values())
        out["under25" if "25" in lab else "under35"] = {
            "first_pct": v[HVS_FIRST], "last_pct": v[HVS_LAST], "max_pct": hi, "min_pct": lo, "max": hi, "max_years": [k for k in v if v[k] == hi],
            "min": lo, "min_years": [k for k in v if v[k] == lo], "n": len(v), "sample": sample_id(v)}
    out["first_year"], out["last_year"] = year_of_col(HVS_FIRST), year_of_col(HVS_LAST)
    out["columns"] = [HVS_FIRST, HVS_LAST]
    return out


# --- predictions (design section 6) -------------------------------------------------------------------

def gap_years(gens: dict) -> float | None:
    """P3, P7: median years of finished Millennial chases less those of Boomer chases; None if either has none."""
    m, b = gens["millennials"]["finished"]["median_years"], gens["boomers"]["finished"]["median_years"]
    return None if m is None or b is None else m - b


def predictions(chase: dict, treat: dict, ratio: dict) -> dict:
    """Design section 6. A prediction whose premise is empty is None (not testable), never False."""
    gen = chase["generations"]
    boom, genz = gen["boomers"], gen["genz"]
    b = treat["broad"]["base_finished"]
    g0 = gap_years(gen)
    gs, ge = gap_years(chase["checks"]["same_house"]["generations"]), gap_years(chase["checks"]["existing_homes"]["generations"])
    out = {
        "P1_ratio_higher_last": ratio["household"]["last"] > ratio["household"]["first"],
        "P2_salary_rose_more": ratio["salary_change_pct"] > ratio["household_change_from_salary_first_pct"],
        "P3_boomers_faster": None if g0 is None else g0 > 0,
        "P4_genz_behind_after3": genz["after3"]["median_pct"] < boom["after3"]["median_pct"],
        "P5_treats_cut_a_third": b["median_treat_years"] <= (2 / 3) * b["median_base_years"],
        "P6_snacks_under_1pct": treat["narrow"]["max_target_pct"] < 1,
        "P7_same_house_narrows": None if g0 is None or gs is None else 0 < gs < g0,
        "P7_existing_same_direction": None if ge is None else ge > 0,
        "gap_years": {"headline": g0, "same_house": gs, "existing_homes": ge},
    }
    flags = [v for k, v in out.items() if k.startswith("P")]
    return {**out, "n_true": sum(1 for v in flags if v is True), "n_untestable": sum(1 for v in flags if v is None),
            "n": len(flags)}


def robustness(chase: dict) -> dict:
    """Every version of the chase that was run (shares, checks): do finished Millennial chases take longer than
    Boomer chases, by median years? Licenses the post's sentence on the versions run."""
    versions = {f"share_{k}": v for k, v in chase["shares"].items()}
    versions.update({k: v["generations"] for k, v in chase["checks"].items()})
    gaps = {k: gap_years(v) for k, v in versions.items()}
    return {"versions": sorted(versions), "gaps": gaps, "n": len(gaps),
            "n_millennials_longer": sum(1 for g in gaps.values() if g is not None and g > 0),
            "all_millennials_longer": all(g is not None and g > 0 for g in gaps.values())}


def main() -> None:
    pdata.check_hashes()
    d = inputs()
    chase, head = chase_section(d)
    treat = treat_section(d, head)
    ratio = ratio_section(d)
    results = {"chase": chase, "treats": treat, "ratio": ratio, "shares": share_section(d), "real": real_section(d),
               "grads": grads_section(), "indonesia": indonesia_section(), "ownership": ownership_section(),
               "tbill_pct": {str(y): d["tbill_pct"][y] for y in range(FIRST_START, LAST + 1)}}
    results["predictions"] = predictions(chase, treat, ratio)
    results["robustness"] = robustness(chase)
    with open("results.json", "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote results.json")


if __name__ == "__main__":
    main()
