"""Post 14 analysis: Indonesia's constitutional 20% education budget mandate vs learning outcomes.

There is NO Kaggle dataset here. Every figure below is a VERIFIED constant taken from a primary
source with a verbatim quote on file (see docs/ and the essay's References): Mahkamah Konstitusi
rulings, Kementerian Keuangan APBN documents, OECD PISA, UNESCO UIS and the World Bank.

This script's job is to hold those constants in one auditable place, derive only the few quantities
that are honest arithmetic (the 20%-of-a-small-budget reconciliation, budget composition shares),
print full tables, and write results.json for the charts.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- 1. the mandate and the court fight
# Education share of the state budget at the documented decision points. We chart ONLY years the
# sources pin exactly; the court also found FY2004-FY2007 never reached 20% (Putusan 026/PUU-IV/2006).
# `label` carries only the precision the source supports: 2009 is "met the floor" per Kemenkeu,
# not a figure verified to two decimals, so it is not labelled as one.
MANDATE = [
    {"year": 2007, "share": 11.8, "status": "struck down", "label": "11.8%",
     "note": "Putusan 026/PUU-IV/2006: the 11.8% ceiling (Rp54.07T) held unconstitutional"},
    {"year": 2008, "share": 15.6, "status": "struck down", "label": "15.6%",
     "note": "Putusan 13/PUU-VI/2008: the entire revised budget law held unconstitutional"},
    {"year": 2009, "share": 20.0, "status": "met", "label": "20%",
     "note": "Kemenkeu: the 20% mandate has been met since 2009"},
    {"year": 2024, "share": 20.00, "status": "met", "label": "20.00%",
     "note": "Rp665.0T of Rp3,325.1T"},
    {"year": 2025, "share": 20.00, "status": "met", "label": "20.00%",
     "note": "Rp724.3T of Rp3,621.3T"},
]

# ---------------------------------------------------------------- 2. twenty percent of a small pie
FISCAL = {
    "educ_2024_t": 665.0, "belanja_2024_t": 3325.1, "gdp_2024_t": 22138.99,
    "educ_2025_t": 724.3, "belanja_2025_t": 3621.3,
    "educ_2026_t": 769.1, "belanja_2026_t": 3842.7,
    "tax_gdp_id_2023": 12.0, "tax_gdp_asiapac_2023": 19.5, "tax_gdp_oecd_2023": 33.9,
    "tax_gdp_id_2007": 12.2,
}
# honest arithmetic, not new facts
FISCAL["belanja_share_gdp_2024"] = round(FISCAL["belanja_2024_t"] / FISCAL["gdp_2024_t"] * 100, 2)
FISCAL["educ_share_belanja_2024"] = round(FISCAL["educ_2024_t"] / FISCAL["belanja_2024_t"] * 100, 2)
FISCAL["educ_share_gdp_2024"] = round(FISCAL["educ_2024_t"] / FISCAL["gdp_2024_t"] * 100, 2)

# NOT LIKE-FOR-LIKE: the education budget's numerator includes a financing component (the LPDP
# endowment) that is not part of belanja negara. Kemenkeu APBN 2024: BPP 241.5 + TKD 346.6 +
# financing 77.0. APBN 2025: BPP 297.2 + TKD 347.1 + financing 80.0. On an expenditure-only basis
# the ratio is lower, and the essay and charts must disclose this.
FISCAL["financing_2024_t"], FISCAL["financing_2025_t"] = 77.0, 80.0
FISCAL["educ_ex_fin_share_belanja_2024"] = round(
    (FISCAL["educ_2024_t"] - FISCAL["financing_2024_t"]) / FISCAL["belanja_2024_t"] * 100, 2)
FISCAL["educ_ex_fin_share_belanja_2025"] = round(
    (FISCAL["educ_2025_t"] - FISCAL["financing_2025_t"]) / FISCAL["belanja_2025_t"] * 100, 2)
FISCAL["educ_ex_fin_share_gdp_2024"] = round(
    (FISCAL["educ_2024_t"] - FISCAL["financing_2024_t"]) / FISCAL["gdp_2024_t"] * 100, 2)

# Subnational compliance is materially worse (World Bank Subnational Education PER, 2020).
SUBNATIONAL = {"districts_noncompliant_pct": 22, "districts_n": 112, "districts_total": 508,
               "provinces_noncompliant_pct": 35, "provinces_n": 12, "provinces_total": 34}

# DEFINITION DRIFT: what counts inside the 20% has changed. Law 20/2003 Art. 49(1) originally
# EXCLUDED educator salaries ("Dana pendidikan selain gaji pendidik ..."); Putusan 24/PUU-V/2007
# allowed teacher salaries to be counted inside the education budget, a large part of why 20%
# became reachable in 2009. The endowment transfer counts, and from 2025-2026 so does the free
# meals programme. NOTE: the pronouncement date of 24/PUU-V/2007 is UNVERIFIED, do not state it.
DEFINITION_DRIFT = {
    "sisdiknas_excluded_salaries": "Law No. 20/2003 Art. 49(1) set the 20% on education funds "
                                   "OTHER THAN educator salaries and official-service education",
    "ruling_that_let_salaries_in": "Putusan 24/PUU-V/2007",
}

# education spending as % of GDP; Indonesia is budget-based (Kemenkeu 2024), peers are World Bank/UIS.
# NOTE: the World Bank/UIS Indonesia series is NOT usable at face value for recent years (it reports
# 1.28% of GDP), so the Kemenkeu-derived figure is used and the discrepancy is disclosed in the essay.
PEERS = [
    {"country": "OECD members", "pct": 5.06, "year": 2022, "src": "World Bank/UIS"},
    {"country": "Philippines", "pct": 3.93, "year": 2024, "src": "World Bank/UIS"},
    {"country": "Malaysia", "pct": 3.51, "year": 2023, "src": "World Bank/UIS"},
    {"country": "Indonesia", "pct": 3.00, "year": 2024, "src": "Kemenkeu APBN (budget-based)"},
    {"country": "Viet Nam", "pct": 2.89, "year": 2022, "src": "World Bank/UIS"},
    {"country": "Thailand", "pct": 2.52, "year": 2023, "src": "World Bank/UIS"},
]

# ---------------------------------------------------------------- 3. outcomes, with the honest caveats
# OECD comparability rule: trends valid only from reading 2000, maths 2003, science 2006.
PISA = {
    "reading": {2000: 371, 2003: 382, 2006: 393, 2009: 402, 2012: 396, 2015: 397, 2018: 371, 2022: 359},
    "maths":   {2003: 360, 2006: 391, 2009: 371, 2012: 375, 2015: 386, 2018: 379, 2022: 366},
    "science": {2006: 393, 2009: 383, 2012: 382, 2015: 403, 2018: 396, 2022: 383},
}
OECD_AVG_2022 = {"reading": 476, "maths": 472, "science": 485}
# PISA coverage of the 15-year-old population: only two published points, so only two are plotted.
COVERAGE = {2000: 46, 2018: 85}
BASELINE_2022 = {"maths": 18, "reading": 25, "science": 34}          # % at Level 2 or above
BASELINE_OECD_2022 = {"maths": 69, "reading": 74, "science": 76}
ACCESS = {
    "upper_sec_ner_2001": 40.1, "upper_sec_ner_2009": 56.6, "upper_sec_ner_2018": 81.5,
    "lower_sec_ner_2001": 73.7, "lower_sec_ner_2023": 94.9,
    "sec_ger_2000": 55.6, "sec_ger_2023": 96.0,
    "literacy_2004": 90.4, "literacy_2020": 96.0,
    "mys_2006": 7.57, "mys_2020": 8.56,
    "extra_15yos_in_school_m": 1.1,       # millions brought into PISA-eligible schooling 2012-2022
}
LEARNING_POVERTY = {"indonesia": 53, "gap_vs_eap_pp": 18, "gap_vs_umic_pp": 20}

# ---------------------------------------------------------------- 4. where the money goes
# 2026 DRAFT budget composition (announced 21 Aug 2025, on a then-proposed Rp757.8T education budget).
BUDGET26 = {"total_draft_t": 757.8, "educators_pay_t": 274.7, "mbg_inside_educ_t": 223.0,
            "total_enacted_t": 769.1, "mbg_total_2026_t": 335.0, "mbg_after_cut_t": 268.0,
            "mbg_beneficiaries_m": 82.9}
BUDGET26["other_t"] = round(BUDGET26["total_draft_t"] - BUDGET26["educators_pay_t"]
                            - BUDGET26["mbg_inside_educ_t"], 1)
for k, v in [("educators_pay", "educators_pay_t"), ("mbg", "mbg_inside_educ_t"), ("other", "other_t")]:
    BUDGET26[f"{k}_pct"] = round(BUDGET26[v] / BUDGET26["total_draft_t"] * 100, 1)

SPEND_THRESHOLD = {"oecd_threshold_usd": 75000, "indonesia_cumulative_usd": 19700}

# ---------------------------------------------------------------- print full tables
print("=== 1. THE MANDATE AND THE COURT FIGHT (education share of the state budget) ===")
for m in MANDATE:
    print(f"  {m['year']}  {m['share']:5.2f}%  {m['status']:12s}  {m['note']}")

print("\n=== 2. TWENTY PERCENT OF A SMALL PIE (2024, from Kemenkeu APBN) ===")
print(f"  education        Rp{FISCAL['educ_2024_t']:,.1f}T")
print(f"  state spending   Rp{FISCAL['belanja_2024_t']:,.1f}T   = {FISCAL['belanja_share_gdp_2024']}% of GDP")
print(f"  GDP              Rp{FISCAL['gdp_2024_t']:,.1f}T")
print(f"  => education is {FISCAL['educ_share_belanja_2024']}% of the budget "
      f"but only {FISCAL['educ_share_gdp_2024']}% of GDP")
print(f"  tax-to-GDP: Indonesia {FISCAL['tax_gdp_id_2023']}% vs Asia-Pacific "
      f"{FISCAL['tax_gdp_asiapac_2023']}% vs OECD {FISCAL['tax_gdp_oecd_2023']}% "
      f"(and {FISCAL['tax_gdp_id_2007']}% back in 2007)")
print(f"  NOT LIKE-FOR-LIKE: excluding the financing component (Rp{FISCAL['financing_2024_t']}T in "
      f"2024, Rp{FISCAL['financing_2025_t']}T in 2025), education is "
      f"{FISCAL['educ_ex_fin_share_belanja_2024']}% of state spending in 2024 "
      f"({FISCAL['educ_ex_fin_share_belanja_2025']}% in 2025) and "
      f"{FISCAL['educ_ex_fin_share_gdp_2024']}% of GDP")
print(f"  subnational: {SUBNATIONAL['districts_noncompliant_pct']}% of districts/cities "
      f"({SUBNATIONAL['districts_n']} of {SUBNATIONAL['districts_total']}) and "
      f"{SUBNATIONAL['provinces_noncompliant_pct']}% of provinces "
      f"({SUBNATIONAL['provinces_n']} of {SUBNATIONAL['provinces_total']}) did not meet the mandate")
print("\n  education spending as % of GDP:")
for p in sorted(PEERS, key=lambda r: -r["pct"]):
    print(f"    {p['country']:15s} {p['pct']:4.2f}%  ({p['year']}, {p['src']})")

print("\n=== 3. OUTCOMES ===")
years = sorted({y for s in PISA.values() for y in s})
print("  PISA mean scores by cycle (blank = before that subject's comparable baseline)")
print("    year   " + "".join(f"{y:>7d}" for y in years))
for subj, series in PISA.items():
    print(f"    {subj:8s}" + "".join(f"{series.get(y, ''):>7}" for y in years))
print(f"  OECD 2022 averages: {OECD_AVG_2022}")
print(f"  2022 gap vs OECD: " + ", ".join(
    f"{s} {PISA[s][2022] - OECD_AVG_2022[s]:+d}" for s in PISA))
print(f"  baseline proficiency 2022 (Level 2+): {BASELINE_2022}  vs OECD {BASELINE_OECD_2022}")
print(f"  PISA coverage of 15-year-olds: {COVERAGE[2000]}% (2000) -> {COVERAGE[2018]}% (2018); "
      f"+{ACCESS['extra_15yos_in_school_m']}M more 15-year-olds in school 2012-2022")
print(f"  learning poverty: {LEARNING_POVERTY['indonesia']}% "
      f"({LEARNING_POVERTY['gap_vs_eap_pp']}pp worse than East Asia and Pacific)")
print("  ACCESS GAINS (what the money bought):")
print(f"    upper-secondary net enrolment {ACCESS['upper_sec_ner_2001']}% (2001) -> "
      f"{ACCESS['upper_sec_ner_2018']}% (2018)")
print(f"    lower-secondary net enrolment {ACCESS['lower_sec_ner_2001']}% -> {ACCESS['lower_sec_ner_2023']}%")
print(f"    secondary gross enrolment {ACCESS['sec_ger_2000']}% -> {ACCESS['sec_ger_2023']}%")
print(f"    adult literacy {ACCESS['literacy_2004']}% -> {ACCESS['literacy_2020']}%")

print("\n=== 4. WHERE THE MONEY GOES (2026 draft education budget, Rp757.8T) ===")
print(f"  educators' pay   Rp{BUDGET26['educators_pay_t']:6.1f}T  {BUDGET26['educators_pay_pct']:5.1f}%")
print(f"  free meals (MBG) Rp{BUDGET26['mbg_inside_educ_t']:6.1f}T  {BUDGET26['mbg_pct']:5.1f}%")
print(f"  everything else  Rp{BUDGET26['other_t']:6.1f}T  {BUDGET26['other_pct']:5.1f}%")
print(f"  spending threshold: Indonesia ~USD {SPEND_THRESHOLD['indonesia_cumulative_usd']:,} cumulative "
      f"per student vs the USD {SPEND_THRESHOLD['oecd_threshold_usd']:,} level past which more "
      f"spending stops predicting higher scores")

out = {"mandate": MANDATE, "fiscal": FISCAL, "peers": PEERS,
       "pisa": {k: {str(y): v for y, v in s.items()} for k, s in PISA.items()},
       "oecd_avg_2022": OECD_AVG_2022, "coverage": {str(k): v for k, v in COVERAGE.items()},
       "baseline_2022": BASELINE_2022, "baseline_oecd_2022": BASELINE_OECD_2022,
       "access": ACCESS, "learning_poverty": LEARNING_POVERTY,
       "budget26": BUDGET26, "spend_threshold": SPEND_THRESHOLD,
       "subnational": SUBNATIONAL, "definition_drift": DEFINITION_DRIFT}
(BASE / "results.json").write_text(json.dumps(out, indent=2))
print("\nwrote results.json")
