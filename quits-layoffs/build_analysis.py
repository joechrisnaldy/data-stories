"""Post 15 analysis: two famous labour-market numbers, and what each one actually counts.

Two kinds of input, kept strictly separate:
  1. COMPUTED, from the QLmonthly panel (Ellieroth & Michaud, Minneapolis Fed), CPS-based quit and
     layoff transition rates, 582 months, Jan 1978 to Jun 2026. Downloaded from
     github.com/qlmonthly/Data. Everything here is recomputed from the .dta files.
  2. VERIFIED CONSTANTS, external figures each pinned to a primary source with a verbatim quote on
     file (see docs/ and the essay References). Nothing here is recalled from memory.

Writes results.json. Prints full tables.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- 1. COMPUTED from QLmonthly
prime = pd.read_stata(BASE / "data" / "qlmonthly_prime.dta").set_index("time").sort_index()
allw = pd.read_stata(BASE / "data" / "qlmonthly_all.dta").set_index("time").sort_index()

NBER = {  # NBER peak-to-trough, used only to mark and to take within-window maxima
    "1980": ("1980-01", "1980-07"), "1981-82": ("1981-07", "1982-11"),
    "1990-91": ("1990-07", "1991-03"), "2001": ("2001-03", "2001-11"),
    "2008-09": ("2007-12", "2009-06"), "COVID": ("2020-02", "2020-04"),
}

def era(df, a, b):
    w = df.loc[a:b]
    return {"quits": round(float(w.eqall_seats.mean()), 3),
            "layoffs": round(float(w.elall_seats.mean()), 3),
            "share_layoff_to_nilf": round(float(w.share_layoff_n_seats.mean()), 4)}

ERAS = {"2019": era(prime, "2019-01", "2019-12"),
        "great_resignation_2021_22": era(prime, "2021-01", "2022-12"),
        "last_12m": era(prime, "2025-07", "2026-06")}

recessions = {}
for k, (a, b) in NBER.items():
    w = prime.loc[a:b]
    recessions[k] = {
        "start": a, "end": b,
        "n_months": int(len(w)),
        "peak_layoff": round(float(w.elall_seats.max()), 3),
        "min_quits": round(float(w.eqall_seats.min()), 3),
        # composition at the layoff peak: where did the laid-off go
        "share_to_nilf_at_peak": round(float(w.loc[w.elall_seats.idxmax(), "share_layoff_n_seats"]), 4),
        "mean_share_to_nilf": round(float(w.share_layoff_n_seats.mean()), 4),
        # The claim "X% of laid-off workers" is about PEOPLE, so it has to be weighted by how many
        # were laid off each month. Unweighted and weighted agree to within 0.5pp everywhere except
        # COVID, whose 3-month NBER window mixes a normal February with a 10.7% April.
        "wtd_share_to_nilf": round(float(np.average(w.share_layoff_n_seats, weights=w.elall_seats)), 4),
    }

COMPUTED = {
    "n_months": int(len(prime)),
    "start": str(prime.index.min().date()), "end": str(prime.index.max().date()),
    "prime": {
        "mean_layoff": round(float(prime.elall_seats.mean()), 3),
        "mean_quit": round(float(prime.eqall_seats.mean()), 3),
        "mean_share_layoff_to_nilf": round(float(prime.share_layoff_n_seats.mean()), 4),
        "min_share_layoff_to_nilf": round(float(prime.share_layoff_n_seats.min()), 4),
        "max_share_layoff_to_nilf": round(float(prime.share_layoff_n_seats.max()), 4),
        "mean_share_quit_to_nilf": round(float(prime.share_quit_n_seats.mean()), 4),
    },
    "all": {
        "mean_layoff": round(float(allw.elall_seats.mean()), 3),
        "mean_quit": round(float(allw.eqall_seats.mean()), 3),
        "mean_share_layoff_to_nilf": round(float(allw.share_layoff_n_seats.mean()), 4),
        "mean_share_quit_to_nilf": round(float(allw.share_quit_n_seats.mean()), 4),
    },
    "months_layoffs_exceed_quits": int((prime.elall_seats > prime.eqall_seats).sum()),
    # The ordering is a prime-age fact and reverses for all workers, where teenage and older-worker
    # quitting is far heavier. Any sentence quoting 514/582 has to name the age group.
    "months_layoffs_exceed_quits_all": int((allw.elall_seats > allw.eqall_seats).sum()),
    "covid_apr2020_layoff": round(float(prime.loc["2020-04-01", "elall_seats"]), 3),
    "covid_apr2020_quit": round(float(prime.loc["2020-04-01", "eqall_seats"]), 3),
    "covid_feb2020_layoff": round(float(prime.loc["2020-02-01", "elall_seats"]), 3),
    "covid_feb2020_quit": round(float(prime.loc["2020-02-01", "eqall_seats"]), 3),
    "eras": ERAS, "recessions": recessions,
}
COMPUTED["covid_multiple"] = round(COMPUTED["covid_apr2020_layoff"] / COMPUTED["prime"]["mean_layoff"], 2)
COMPUTED["share_months_layoffs_exceed_quits"] = round(
    COMPUTED["months_layoffs_exceed_quits"] / COMPUTED["n_months"], 4)

# --- correlation, computed here rather than quoted --------------------------------------------
# The paper reports -0.46. That is a real figure from IWP 94 (Table 6), but it does not reproduce
# on the raw monthly series this post plots: raw monthly is -0.30, and -0.46 only appears once the
# series are smoothed to six-month centred averages. Charts may only claim what they plot, so both
# are computed and the chart footnote uses the raw one.
def _corr(df, smooth=None):
    q, l = df.eqall_seats, df.elall_seats
    if smooth:
        q, l = q.rolling(smooth, center=True).mean(), l.rolling(smooth, center=True).mean()
    return round(float(q.corr(l)), 4)

COMPUTED["corr_quits_layoffs"] = {
    "prime_monthly": _corr(prime),
    "prime_6m_avg": _corr(prime, 6),
    "prime_6m_avg_1978_2024": _corr(prime.loc["1978-01":"2024-12"], 6),
    "all_monthly": _corr(allw),
}

# --- is the headline contrast robust to how you cut it? ---------------------------------------
# JOLTS covers nonfarm payroll establishments at any age; this panel is households, and the
# headline figures are prime age. So the contrast is checked on both age cuts and on both a
# single-month and a two-year basis. All four say the same thing: single digits, against +30%.
ROBUSTNESS = {}
for _nm, _df in (("prime", prime), ("all", allw)):
    _q19 = float(_df.loc["2019-01":"2019-12"].eqall_seats.mean())
    ROBUSTNESS[_nm] = {
        "q_2019": round(_q19, 4),
        "q_nov2021": round(float(_df.loc["2021-11-01", "eqall_seats"]), 4),
        "q_2021_22": round(float(_df.loc["2021-01":"2022-12"].eqall_seats.mean()), 4),
        "pct_2019_to_nov2021": round((float(_df.loc["2021-11-01", "eqall_seats"]) / _q19 - 1) * 100, 1),
        "pct_2019_to_2021_22": round(
            (float(_df.loc["2021-01":"2022-12"].eqall_seats.mean()) / _q19 - 1) * 100, 1),
    }
COMPUTED["headline_robustness"] = ROBUSTNESS

# --- October 2025 has no household survey; what does that do to the 12-month figure? ------------
# BLS did not collect the CPS for the October 2025 reference period (lapse in appropriations, not
# collected retroactively). The panel nonetheless carries values for October and November 2025 and
# the project does not document how. Both rows are dropped here to size the exposure.
_w12 = prime.loc["2025-07":"2026-06"]
_w12_ex = _w12.drop(index=[pd.Timestamp("2025-10-01"), pd.Timestamp("2025-11-01")])
COMPUTED["last12_oct2025_sensitivity"] = {
    "quits_with_oct_nov_2025": round(float(_w12.eqall_seats.mean()), 4),
    "quits_without": round(float(_w12_ex.eqall_seats.mean()), 4),
    "n_without": int(len(_w12_ex)),
}

# --- share versus level: where do people actually vanish? --------------------------------------
# The SHARE of the laid-off who stop looking is higher outside recessions, but the LEVEL (how much
# of employment vanishes from the count each month) is higher inside them, because there are far
# more layoffs. The essay may only claim the share.
_rec = pd.Series(False, index=prime.index)
for _a, _b in NBER.values():
    _rec.loc[_a:_b] = True
_vanish = prime.elall_seats * prime.share_layoff_n_seats
COMPUTED["vanishing"] = {
    "share_in_recession": round(float(prime.share_layoff_n_seats[_rec].mean()), 4),
    "share_in_expansion": round(float(prime.share_layoff_n_seats[~_rec].mean()), 4),
    "level_in_recession": round(float(_vanish[_rec].mean()), 3),
    "level_in_expansion": round(float(_vanish[~_rec].mean()), 3),
}

# ---------------------------------------------------------------- 2. VERIFIED external constants
# Each value below has a primary-source verbatim quote recorded in docs/ and the References list.
VERIFIED = {
    # --- JOLTS, the first number (BLS) ---
    "jolts_quits_rate_2019_avg": 2.3,          # BLS series JTS000000000000000QUR, 2019 mean
    "jolts_quits_rate_record": 3.0,
    # NOT "a record set in November 2021". The Nov 2021 release (jolts_01042022) says the RATE was
    # "matching the series high in September"; what was a series high that month was the LEVEL,
    # "a series high 4.5 million". No 2022 month exceeds a 3.0 rate.
    "jolts_quits_record_month": "November 2021",
    "jolts_quits_rate_record_note": "matched the September 2021 high; never exceeded since",
    "jolts_quits_level_nov2021_k": 4453,       # "a series high 4.5 million" in that release
    "jolts_quits_level_record_k": 4499,        # April 2022, thousands, the later level record
    "jolts_quits_rate_may2026": 1.9,
    "jolts_quits_level_may2026_m": 3.1,
    # Two different comparisons, previously conflated. Rate to rate is 36.7% below; the 31.9% is a
    # LEVEL decline (3,065k vs the 4,499k April 2022 record). Prose must not mix them.
    "jolts_quits_rate_pct_below_peak": 36.7,
    "jolts_quits_level_pct_below_peak": 31.9,
    "jolts_layoffs_rate_may2026": 1.1,
    "jolts_hires_rate_may2026": 3.3,
    "jolts_openings_rate_may2026": 4.6,
    "jolts_start": "December 2000",
    # The two numbers never arrive together, which the essay's own two sources prove:
    # JOLTS May 2026 "For release 10:00 a.m. (ET) Tuesday, June 30, 2026" (USDL-26-1123);
    # Employment Situation June 2026 "embargoed until 8:30 a.m. (ET) Thursday, July 2, 2026".
    "empsit_release_time": "8:30 a.m. ET",
    "jolts_release_time": "10:00 a.m. ET",
    # --- the unemployment rate, the second number (BLS Employment Situation, June 2026) ---
    "u1_jun2026": 1.8, "u2_jun2026": 1.9, "u3_jun2026": 4.2,
    "u4_jun2026": 4.5, "u5_jun2026": 5.2, "u6_jun2026": 7.9,
    "want_a_job_not_in_lf_m": 6.0,             # 6,045,000, Table A-1
    "marginally_attached_k": 1761,
    "discouraged_k": 477,
    "lfpr_jun2026": 61.5,
    "unemployed_jun2026_m": 7.1,
    "long_term_share_jun2026": 27.3,           # unemployed 27+ weeks as share of all unemployed
    # the month the mechanism happened in public (June 2026 vs May 2026)
    # All from Summary table A of USDL-26-1125. The stock levels matter: without them the essay
    # cannot say WHY the rate fell, and the intuitive answer is arithmetically backwards.
    "jun2026_labor_force_change_k": -720,
    "jun2026_nilf_change_k": 832,
    "jun2026_employed_change_k": -507,
    "jun2026_unemployed_change_k": -213,
    "may2026_labor_force_k": 170078, "jun2026_labor_force_k": 169358,
    "may2026_unemployed_k": 7307, "jun2026_unemployed_k": 7094,
    "u3_may2026": 4.3,
    # --- the flow that makes the point (BLS Monthly Labor Review, Dec 2024) ---
    # The base is EVERYONE unemployed a month earlier, not the subset who left unemployment.
    # Verbatim: "In December 2024, 23.7 percent of people who were unemployed a month earlier found
    # work, while 22.4 percent stopped looking for work and left the labor force." The three shares
    # sum to 100 with the 53.9 percent who stayed unemployed, which is the proof of the base.
    "flow_out_found_work_pct": 23.7,
    "flow_out_left_lf_pct": 22.4,
    "flow_stayed_unemployed_pct": 53.9,
    # --- Ellieroth & Michaud IWP 94, Revised January 2026 (their own headline findings) ---
    "em_layoffs_vs_eu_pct": 20,                # "layoffs are 1.2 times more common than EU flows"
    "em_quits_vs_en_pct": 45,                  # "quits are 45% less common than EN flows indicate"
    # Was stored as 15. IWP 94 says 45: "layoffs to non-employment contribute 45% more to
    # unemployment fluctuations than EU flows."
    "em_layoff_contribution_pct": 45,
    # Their Table 6 figure. It does NOT reproduce on the raw monthly panel (-0.30); it reproduces
    # on six-month centred averages. Kept for attribution only; charts use COMPUTED.
    "em_corr_quits_layoffs": -0.46,
    "em_corr_specification": "IWP 94 Table 6; reproduces on 6-month centred averages, not raw monthly",
    "em_share_layoff_exit_lf_pct": 40,         # superseded Oct 2024 vintage; not used in the essay
    "em_prime_age_range": "25 to 55",          # IWP 94 p.11 "prime-age population (25-55 years old)"
    "em_lf_attachment_amplification_pct": 25,
    # --- context ---
    "payrolls_jun2026_k": 57, "payrolls_12m_avg_k": 36,
    "unrate_longrun_mean": 5.66,
    "richmond_implied_unrate": "6 to 10 percent",
    "richmond_hiring_rate": 3.3,
    # --- AI: attribution only, and the measured finding of no clear effect ---
    # One named private tracker, not "trackers". Verbatim: "Through June, employers have announced
    # 443,604 job cuts" and "AI has been cited in 101,743 job cut announcements".
    "challenger_ai_attributed_ytd": 101743,
    "challenger_total_cuts_ytd": 443604,
    "challenger_report_date": "July 1, 2026",
    "yale_ai_finding": "no clear labour-market effect of AI detectable as of May 2026",
}
# Counterfactuals for June 2026, so the essay states the mechanism the arithmetic supports.
# A shrinking labour force RAISES the unemployment rate; the rate fell because the numerator fell.
_lfM, _lfJ = VERIFIED["may2026_labor_force_k"], VERIFIED["jun2026_labor_force_k"]
_uM, _uJ = VERIFIED["may2026_unemployed_k"], VERIFIED["jun2026_unemployed_k"]
VERIFIED["u3_jun2026_exact"] = round(_uJ / _lfJ * 100, 2)
VERIFIED["u3_may2026_exact"] = round(_uM / _lfM * 100, 2)
VERIFIED["u3_if_labor_force_held"] = round(_uJ / _lfM * 100, 2)     # 4.17: still falls
VERIFIED["u3_if_unemployed_held"] = round(_uM / _lfJ * 100, 2)      # 4.31: rises
# If the 507k drop in employment had shown up as job seekers instead of as exits:
VERIFIED["u3_if_job_losers_had_searched"] = round(
    (_uJ - VERIFIED["jun2026_employed_change_k"]) / (_lfJ - VERIFIED["jun2026_employed_change_k"]) * 100, 2)
VERIFIED["jolts_quits_pct_change_2019_to_peak"] = round(
    (VERIFIED["jolts_quits_rate_record"] / VERIFIED["jolts_quits_rate_2019_avg"] - 1) * 100, 1)
cps_2019 = ERAS["2019"]["quits"]
cps_gr = ERAS["great_resignation_2021_22"]["quits"]
# Arithmetically -1.5%, but a Welch test on the two windows gives p = 0.81 and the gap is about a
# twelfth of an ordinary month-to-month move. Reported as "did not move", never as a fall.
VERIFIED["cps_quits_pct_change_2019_to_gr"] = round((cps_gr / cps_2019 - 1) * 100, 1)

# ---------------------------------------------------------------- print
print(f"=== QLmonthly: {COMPUTED['n_months']} months, {COMPUTED['start']} to {COMPUTED['end']} ===")
print(f"  prime-age mean layoff {COMPUTED['prime']['mean_layoff']}%  mean quit "
      f"{COMPUTED['prime']['mean_quit']}%")
print(f"  layoffs exceeded quits in {COMPUTED['months_layoffs_exceed_quits']} of "
      f"{COMPUTED['n_months']} months ({COMPUTED['share_months_layoffs_exceed_quits']*100:.0f}%)")

print("\n=== THE CONTRAST: the same period, two measures ===")
print(f"  JOLTS quits rate      2019 {VERIFIED['jolts_quits_rate_2019_avg']}%  ->  "
      f"record {VERIFIED['jolts_quits_rate_record']}% ({VERIFIED['jolts_quits_record_month']})"
      f"   = {VERIFIED['jolts_quits_pct_change_2019_to_peak']:+.1f}%")
print(f"  CPS quits to non-employment (prime) 2019 {cps_2019}%  ->  2021-22 {cps_gr}%"
      f"   = {VERIFIED['cps_quits_pct_change_2019_to_gr']:+.1f}%")

print("  robustness of that contrast, both age cuts and both bases:")
for _nm, _r in ROBUSTNESS.items():
    print(f"    {_nm:5s} 2019 {_r['q_2019']}  -> Nov 2021 {_r['q_nov2021']} ({_r['pct_2019_to_nov2021']:+.1f}%)"
          f"  -> 2021-22 avg {_r['q_2021_22']} ({_r['pct_2019_to_2021_22']:+.1f}%)")

print("\n=== correlation of quits and layoffs ===")
for k, v in COMPUTED["corr_quits_layoffs"].items():
    print(f"  {k:24s} {v}")
print(f"  paper reports {VERIFIED['em_corr_quits_layoffs']} ({VERIFIED['em_corr_specification']})")

print("\n=== era table (prime age) ===")
print(pd.DataFrame(ERAS).T.to_string())

print("\n=== where the laid-off go ===")
p = COMPUTED["prime"]
print(f"  prime age: {p['mean_share_layoff_to_nilf']*100:.1f}% of laid-off workers leave the labour "
      f"force (range {p['min_share_layoff_to_nilf']*100:.0f}% to {p['max_share_layoff_to_nilf']*100:.0f}%)")
print(f"  all workers: {COMPUTED['all']['mean_share_layoff_to_nilf']*100:.1f}%")
print(f"  quitters going to non-participation: prime {p['mean_share_quit_to_nilf']*100:.1f}%, "
      f"all {COMPUTED['all']['mean_share_quit_to_nilf']*100:.1f}%")

print("\n=== recessions (prime age), unweighted vs weighted by layoff volume ===")
print(pd.DataFrame(recessions).T.to_string())
print("  -> counted as unemployed, weighted: " + ", ".join(
    f"{k} {100 - v['wtd_share_to_nilf']*100:.0f}%" for k, v in recessions.items()))

print("\n=== share versus level: where the vanishing happens ===")
_v = COMPUTED["vanishing"]
print(f"  share of laid-off leaving the labour force: recession {_v['share_in_recession']*100:.1f}%, "
      f"expansion {_v['share_in_expansion']*100:.1f}%  (share is higher OUTSIDE recessions)")
print(f"  level vanishing per month, % of employment: recession {_v['level_in_recession']}, "
      f"expansion {_v['level_in_expansion']}  (level is higher INSIDE recessions)")

_s = COMPUTED["last12_oct2025_sensitivity"]
print(f"\n=== October 2025 exposure: last-12m quits {_s['quits_with_oct_nov_2025']} with Oct+Nov 2025, "
      f"{_s['quits_without']} without (n={_s['n_without']}) ===")
print(f"\n  COVID April 2020: layoffs {COMPUTED['covid_apr2020_layoff']}% "
      f"({COMPUTED['covid_multiple']}x the 48-year average) while quits fell to "
      f"{COMPUTED['covid_apr2020_quit']}% from {COMPUTED['covid_feb2020_quit']}% in February")

print("\n=== the unemployment rate and what sits outside it (June 2026, verified) ===")
v = VERIFIED
print(f"  U-3 {v['u3_jun2026']}%   U-4 {v['u4_jun2026']}%   U-5 {v['u5_jun2026']}%   U-6 {v['u6_jun2026']}%")
print(f"  want a job but not in the labour force: {v['want_a_job_not_in_lf_m']} million")
print(f"  leaving unemployment: {v['flow_out_found_work_pct']}% found work, "
      f"{v['flow_out_left_lf_pct']}% stopped looking")
print(f"  June 2026: labour force {v['jun2026_labor_force_change_k']:+,}k, "
      f"employed {v['jun2026_employed_change_k']:+,}k, unemployed {v['jun2026_unemployed_change_k']:+,}k, "
      f"not-in-labour-force {v['jun2026_nilf_change_k']:+,}k, "
      f"rate {v['u3_may2026']}% -> {v['u3_jun2026']}%")
print(f"    why it fell: {v['u3_may2026_exact']}% -> {v['u3_jun2026_exact']}%; "
      f"hold the labour force at May and it is {v['u3_if_labor_force_held']}% (still falls); "
      f"hold the unemployed at May and it is {v['u3_if_unemployed_held']}% (rises). "
      f"A shrinking labour force pushes the rate UP.")
print(f"    had the {abs(v['jun2026_employed_change_k'])}k drop in employment shown up as job "
      f"seekers: {v['u3_if_job_losers_had_searched']}%")

out = {"computed": COMPUTED, "verified": VERIFIED}
(BASE / "results.json").write_text(json.dumps(out, indent=2))
print("\nwrote results.json")
