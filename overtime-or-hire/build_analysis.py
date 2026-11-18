"""Post 32: two 12-hour days or three 8-hour days? Writes results.json, every quantity the post states.

Survey figures use profile_data.py's one sample rule. Every external input is read from docs/sources.json, the
stored and quoted documents the gate checks (docs/provenance-audit.md says where each is defined); the one input
written in words, the US overtime rate, is held beside its quote and checked against it. The model's functions are
in model.py (tests: test_model.py). Run from the post folder: python3 build_analysis.py
"""
import json
import os

import pandas as pd

import profile_data as pdata
from model import (Costs, Curve, Team, exempt_break_even, exempt_week_cost, indonesia_week, nonexempt_week_cost,
                   payback_weeks, productive_hours, team_productive_hours, us_week)

BASE = os.path.dirname(os.path.abspath(__file__))
SOURCES = os.path.join(BASE, "docs", "sources.json")
RESULTS = os.path.join(BASE, "results.json")
OVERTIME_RATE = 1.5     # Fact Sheet #23, in words: OVERTIME_WORDS
OVERTIME_WORDS = "at a rate not less than time and one-half their regular rates of pay"
WEEKS_PER_YEAR = 52
LONG, SHORT, DAYS = (2, 12), (3, 8), 5      # the question: two people on 12-hour days, three on 8-hour days
CONTRAST = ("35 to 40", "60 or more")       # a standard full-time week against the longest band
EARLY, LATE = (2015, 2019), (2021, 2024)    # the sample's years before and after the pandemic year
REPRODUCE_YEAR = 2024                       # the published sleep figure (sources.json atus2024_sleep)


def src(key: str) -> dict:
    with open(SOURCES, encoding="utf-8") as f:
        return json.load(f)[key]["values"]


def overtime_rate() -> float:
    with open(SOURCES, encoding="utf-8") as f:
        quote = json.load(f)["fs23_overtime"]["quote"]
    if OVERTIME_WORDS not in quote:
        raise SystemExit("the US overtime rate's words are no longer in the fs23_overtime quote")
    return OVERTIME_RATE


def wmean(d: pd.DataFrame, col: str) -> float:
    return float((d[col] * d["weight"]).sum() / d["weight"].sum())


def stat(d: pd.DataFrame) -> dict:
    return {"n": len(d), "sample": pdata.sample_id(d["TUCASEID"])}


def reproduction(d: pd.DataFrame) -> dict:
    year = d[d["TUYEAR"] == REPRODUCE_YEAR]
    hours = round(wmean(year, "sleep_min") / 60, 2)
    published = src("atus2024_sleep")["hours_per_day"]
    if hours != published:
        raise SystemExit(f"sleep in {REPRODUCE_YEAR} is {hours} hours a day here, {published} in the release")
    return {**stat(year), "year": REPRODUCE_YEAR, "sleep_hours": hours}


def bands(kept: pd.DataFrame) -> dict:
    out, total = {}, kept["weight"].sum()
    for low, high, label in pdata.BANDS:
        b = kept[kept["band"] == label]
        key = f"b{low}_{high}" if high < 999 else f"b{low}_plus"
        out[key] = {**stat(b), "label": label, "low": low, "high": high if high < 999 else None,
                    "sleep_hours": round(wmean(b, "sleep_min") / 60, 4),
                    "sports_min": round(wmean(b, "sports_min"), 4), "share": round(b["weight"].sum() / total, 4)}
    return out


def gap(d: pd.DataFrame) -> dict:
    """Sleep and sports, exercise and recreation: the standard full-time band minus the longest band."""
    short, long = (d[d["band"] == label] for label in CONTRAST)
    both = pd.concat([short, long])
    sleep_min = wmean(short, "sleep_min") - wmean(long, "sleep_min")
    bounds = {label: (low, high) for low, high, label in pdata.BANDS}
    return {**stat(both), "short_label": CONTRAST[0], "long_label": CONTRAST[1], "short_low": bounds[CONTRAST[0]][0],
            "short_high": bounds[CONTRAST[0]][1], "long_low": bounds[CONTRAST[1]][0], "n_short_band": len(short),
            "n_long_band": len(long), "sleep_min": round(sleep_min, 4),
            "sleep_hours_week": round(sleep_min * 7 / 60, 4),
            "sports_min": round(wmean(short, "sports_min") - wmean(long, "sports_min"), 4)}


def survey() -> dict:
    d = pdata.read()
    kept, dropped = pdata.sample(d)
    weekday = kept[kept["TUDIARYDAY"].isin(pdata.WEEKDAYS) & (kept["TRHOLIDAY"] == 0)]
    b = bands(kept)
    sports = [v["sports_min"] for v in b.values()]
    return {**stat(kept), "first_year": pdata.YEARS[0], "last_year": pdata.YEARS[1], "age_min": pdata.AGES[0],
            "age_max": pdata.AGES[1], "dropped": {key: n for key, _, n in dropped}, "reproduction": reproduction(d), "bands": b,
            "sports_spread_min": round(max(sports) - min(sports), 4), "sports_low_min": min(sports),
            "sports_high_min": max(sports), "band_count": len(b), "gap": gap(kept), "weekday_gap": gap(weekday),
            "early_gap": {**gap(kept[kept["TUYEAR"].between(*EARLY)]), "first_year": EARLY[0], "last_year": EARLY[1]},
            "late_gap": {**gap(kept[kept["TUYEAR"].between(*LATE)]), "first_year": LATE[0], "last_year": LATE[1]}}


def curve_results(curve: Curve, alt: Curve, long: Team, short: Team) -> dict:
    at_long = productive_hours(long.hours, curve)
    observed = src("pencavel_range")
    return {"knot": curve.knot, "peak": curve.peak, "alt_peak": alt.peak,
            "at_short": round(productive_hours(short.hours, curve), 4),
            "data_min": observed["min_hours"], "data_max": observed["max_hours"],
            "at_long": round(at_long, 4), "lost_per_person": round(long.hours - at_long, 4),
            "added_past_short": round(at_long - productive_hours(short.hours, curve), 4),
            "hours_past_short": long.hours - short.hours, "at_peak": round(productive_hours(curve.peak, curve), 4),
            "long_team": round(team_productive_hours(long, curve), 4), "short_team": team_productive_hours(short, curve),
            "long_team_share_pct": round(100 * team_productive_hours(long, curve) / team_productive_hours(short, curve), 4),
            "gap": round(team_productive_hours(short, curve) - team_productive_hours(long, curve), 4),
            "two_max": round(long.people * productive_hours(curve.peak, curve), 4),
            "two_max_alt": round(long.people * productive_hours(alt.peak, alt), 4),
            "long_team_alt": round(team_productive_hours(long, alt), 4)}


def nonexempt_results(costs: Costs, curve: Curve, long: Team, short: Team, hiring_cost: float) -> dict:
    lc, sc = nonexempt_week_cost(long, costs), nonexempt_week_cost(short, costs)
    lp, sp = team_productive_hours(long, curve), team_productive_hours(short, curve)
    output_saving = lc - (sc / sp) * lp
    return {"long_cost": round(lc, 2), "short_cost": round(sc, 2), "cash_saving": round(lc - sc, 2),
            "premium": round(long.people * (long.hours - costs.overtime_after) * (costs.overtime_rate - 1)
                             * costs.wage, 2),
            "extra_benefits": round((short.people - long.people) * costs.benefits * costs.benefit_hours, 2),
            "long_per_hour": round(lc / lp, 4), "short_per_hour": round(sc / sp, 4),
            "per_hour_gap_pct": round(100 * ((lc / lp) / (sc / sp) - 1), 4), "output_saving": round(output_saving, 2),
            "payback_cash_weeks": round(payback_weeks(hiring_cost, lc - sc), 4),
            "payback_output_weeks": round(payback_weeks(hiring_cost, output_saving), 4)}


def exempt_results(costs: Costs, curve: Curve, long: Team, short: Team) -> dict:
    lc, sc = exempt_week_cost(long, costs), exempt_week_cost(short, costs)
    lp, sp = team_productive_hours(long, curve), team_productive_hours(short, curve)
    extra = exempt_break_even(long, short, costs, curve)
    weekly_compensation = (costs.wage + costs.benefits) * costs.benefit_hours
    return {"long_cost": round(lc, 2), "short_cost": round(sc, 2), "long_per_hour": round(lc / lp, 4),
            "short_per_hour": round(sc / sp, 4), "weekly_compensation": round(weekly_compensation, 2),
            "break_even": round(extra, 2), "break_even_pct": round(100 * extra / weekly_compensation, 4)}


def rules_results(rate: float) -> dict:
    hours, cap, pay = src("uu27_hours"), src("uu27_overtime_cap"), src("uu27_overtime_pay")
    if hours["hours_per_day"] * hours["workdays"] != hours["hours_per_week"]:
        raise SystemExit("the law's five-day week does not add up to its weekly hours")
    us = us_week(LONG[1], DAYS, src("fs23_overtime")["hours"], rate)
    idn = indonesia_week(LONG[1], DAYS, hours["hours_per_day"], pay["first_hour_multiple"],
                         pay["later_hours_multiple"], cap["max_hours_day"], cap["max_hours_week"])
    return {"us": {**vars(us), "no_limit_age": src("fs23_no_limit")["age"]}, "indonesia": {**vars(idn), "overtime_hours": idn.first_overtime_hours
                                          + idn.later_overtime_hours, "cap_day": cap["max_hours_day"],
                                          "cap_week": cap["max_hours_week"],
                                          "week_limit": idn.regular_hours + cap["max_hours_week"],
                                          "first_hour_rate": pay["first_hour_multiple"],
                                          "later_rate": pay["later_hours_multiple"]},
            "pay_gap": idn.pay_in_hourly_wages - us.pay_in_hourly_wages}


def main() -> None:
    long, short = Team(LONG[0], LONG[1] * DAYS), Team(SHORT[0], SHORT[1] * DAYS)
    curve = Curve(src("pencavel_knot")["hours"], src("pencavel_peak")["hours"])
    alt = Curve(curve.knot, src("pencavel_t4_peaks")["col_iii"])
    wage, benefits = src("ecec_ft_wages")["usd_per_hour"], src("ecec_ft_benefits")["usd_per_hour"]
    if round(wage + benefits, 2) != src("ecec_ft_total")["usd_per_hour"]:
        raise SystemExit("wages and benefits do not add up to total compensation in the release")
    rate = overtime_rate()
    costs = Costs(wage, benefits, short.hours, src("fs23_overtime")["hours"], rate)
    annual_pay = wage * short.hours * WEEKS_PER_YEAR
    hiring_cost = annual_pay * src("cap_turnover")["median_pct"] / 100
    results = {
        "scenario": {"long_people": long.people, "short_people": short.people, "long_day": LONG[1],
                     "short_day": SHORT[1], "days": DAYS, "long_week": long.hours, "short_week": short.hours,
                     "team_hours": long.people * long.hours, "overtime_rate": rate},
        "survey": survey(),
        "curve": curve_results(curve, alt, long, short),
        "costs": {"wage": wage, "benefits": benefits, "total": round(wage + benefits, 2),
                  "annual_pay": round(annual_pay, 2), "hiring_cost": round(hiring_cost, 2)},
        "nonexempt": nonexempt_results(costs, curve, long, short, hiring_cost),
        "exempt": exempt_results(costs, curve, long, short),
        "rules": rules_results(rate),
    }
    if results["scenario"]["team_hours"] != short.people * short.hours:
        raise SystemExit("the two teams do not work the same nominal hours")
    with open(RESULTS, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main()
