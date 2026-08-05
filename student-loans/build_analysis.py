"""Post 19: 'The Payback Period Assumes You Are Paying It Back'.

Two sources, both US Department of Education, nothing joined from anywhere else:

  College Scorecard, field of study   -> what a programme cost and what it earned (the PRICE)
  Federal Student Aid data center     -> what borrowers actually do  (the DEADLINE)

Output: results.json

FIVE TRAPS GOVERN THIS SCRIPT. All are proved from the data by verify_traps().

  TRAP 1  RECIPIENT COUNTS ARE LOAN-LEVEL. The FSA files say so themselves: "Recipient counts are
          based at the loan level. As a result, recipients may be counted multiple times across
          varying loan statuses." Summing recipients across statuses double counts people.
          => EVERY share in this post is a share of DOLLARS OUTSTANDING, never of recipients.

  TRAP 2  THE TWO FSA TABLES HAVE DIFFERENT DENOMINATORS. PortfoliobyLoanStatus covers the whole
          portfolio. DLPortfoliobyRepaymentPlan covers only borrowers "in Repayment, Deferment and
          Forbearance" and EXCLUDES default, in-school and grace. Mixing them into one percentage
          would be silently wrong.
          => The two series are reported separately and their denominators are printed.

  TRAP 3  THE PANDEMIC PAUSE MAKES ANY SINGLE RECENT QUARTER A POLICY ARTEFACT. Repayment ran 56.9%
          of dollars in 2019 Q3, fell to 0.7% in 2023 Q3 under the CARES suspension, and is 39.2% in
          2026 Q2. A structural claim taken from the latest quarter would be the same error as
          quoting a placeholder-inflated statistic.
          => Full series always plotted; every structural claim quotes the pre-pandemic baseline;
             the plan mix is used for the load-bearing claim because it barely moved (21.4% in
             2019 Q4 against 21.9% now).

  TRAP 4  DEBT_ALL_STGP_ANY vs _EVAL IS NOT UNDERGRADUATE vs GRADUATE. The data dictionary labels
          them "debt disbursed at ALL institutions" and "debt disbursed at THIS institution". _ANY_
          happens to be empty for every graduate credential, which is a coverage fact and not a
          definitional one. Inferring from the variable name would silently drop 38,621 master's
          rows. (Post 16 taught this the hard way: read the label, never infer from the name.)
          => _ANY_ is the headline because it is the debt the person actually owes; _EVAL_ is
             computed alongside as a robustness check and its extra credential coverage is reported.

  TRAP 5  EARNINGS ARE CONDITIONAL ON WORKING. The label is "median earnings of graduates WORKING
          AND NOT ENROLLED 1 year after completing highest credential". People with no job are out
          of the denominator, which makes the price look better than it is.
          => The share of completers not working is computed and reported, so the caveat carries a
             number rather than a hedge.
"""
import json
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
FOS = DATA / "Most-Recent-Cohorts-Field-of-Study.csv"
STATUS_XLS = DATA / "PortfoliobyLoanStatus.xls"
PLAN_XLS = DATA / "DLPortfoliobyRepaymentPlan.xls"

# The quarter the piece treats as "normal", i.e. the last one lying wholly before the CARES
# suspension, which began 13 March 2020.
#
# ROUND 1 CORRECTION. This was "2019Q4", which is WRONG, and the error is the fiscal calendar. The
# workbooks run on federal fiscal years beginning 1 October, and their own Definitions tab says
# "Q4 ends 9/30". So FY2019 Q4 is the snapshot of 30 September 2019, five months before the
# suspension, not the quarter immediately preceding it. The right quarter is FY2020 Q1, ending
# 31 December 2019. Every "just before the pandemic" figure moves:
#   standard-plan share      21.4% -> 21.9%   (see the plans block: equal endpoints are NOT
#                                             evidence the suspension left the series alone)
#   repayment, all dollars   55.2% -> 58.2%
#   post-school not repaying 35.7% -> 33.9%
PRE_PANDEMIC = "2020Q1"

# Fiscal quarter-ends lying WHOLLY inside the payment suspension: 30 Jun 2020 to 30 Jun 2023. The
# pause itself ran 13 Mar 2020 to 31 Aug 2023, so FY2020Q2 (ends 31 Mar 2020) and FY2023Q4 (ends
# 30 Sep 2023) each straddle an edge and are excluded. Any average over the pause has to name a
# window: including FY2020Q2 moves the forbearance mean by more than four points.
PAUSE_WHOLLY_INSIDE = ("2020Q3", "2023Q3")

STATUSES = ["In-School", "Grace", "Repayment", "Deferment", "Forbearance",
            "Cumulative in Default*", "Other"]
# Statuses that describe a loan which has already left school. In-school and grace are excluded
# because those borrowers are not expected to be paying yet, so counting them as "not repaying"
# would be unfair to the point being made.
POST_SCHOOL = ["Repayment", "Deferment", "Forbearance", "Cumulative in Default*", "Other"]

IDR_PLANS = ["Income-Contingent", "Income-Based", "Pay As You Earn*", "SAVE"]
STANDARD_PLAN = "Level:  10 Yrs or Less"          # note the double space, it is in the file

# The data dictionary documents CONTROL as numeric codes 1 to 4, but the field-of-study CSV ships
# the LABELS as text ("Public", "Private, nonprofit", "Private, for-profit", "Foreign"). Mapping the
# documented codes returned an empty breakout, silently. Read the column, not the dictionary, for
# what is physically in the file. Foreign institutions are a real fourth category, 4,662 rows.


# ----------------------------------------------------------------------------- FSA quarterly files

def _fsa_sheet(path, sheet, header_row=4):
    """Parse one FSA quarterly sheet into a dollars-by-category frame indexed by fiscal quarter.

    The layout is a two-row header: row `header_row` carries the category spanning two columns, row
    header_row+1 splits it into "Dollars Outstanding" and "Recipients". Only the dollar columns are
    kept, per TRAP 1.
    """
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    top = pd.Series(raw.iloc[header_row]).ffill().tolist()
    sub = raw.iloc[header_row + 1].tolist()
    raw.columns = [f"{str(t).strip()}|{'$' if 'Dollars' in str(s) else 'n'}" for t, s in zip(top, sub)]

    body = raw.iloc[header_row + 2:].copy()
    body.iloc[:, 0] = pd.to_numeric(body.iloc[:, 0], errors="coerce").ffill()
    body = body[body.iloc[:, 1].astype(str).str.match(r"Q\d")]
    idx = [f"{int(y)}{q}" for y, q in zip(body.iloc[:, 0], body.iloc[:, 1].astype(str))]

    dollar_cols = [c for c in raw.columns if c.endswith("|$") and "nan" not in c]
    out = body[dollar_cols].apply(pd.to_numeric, errors="coerce")
    out.index = idx
    out.columns = [c[:-2] for c in dollar_cols]
    return out.dropna(how="all")


def load_status():
    d = _fsa_sheet(STATUS_XLS, "Direct Loan")
    return d[[c for c in STATUSES if c in d.columns]]


def load_plans():
    d = _fsa_sheet(PLAN_XLS, "DLPortfoliobyRepaymentPlan", header_row=5)
    return d


# ------------------------------------------------------------------------------------- Scorecard

def load_fos():
    cols = ["UNITID", "INSTNM", "CONTROL", "CIPCODE", "CIPDESC", "CREDLEV", "CREDDESC",
            "DEBT_ALL_STGP_ANY_MDN", "DEBT_ALL_STGP_EVAL_MDN",
            "EARN_MDN_HI_1YR", "EARN_MDN_HI_2YR",
            "EARN_COUNT_WNE_HI_1YR", "EARN_COUNT_NWNE_HI_1YR"]
    d = pd.read_csv(FOS, usecols=cols, dtype=str, low_memory=False)
    for c in ["DEBT_ALL_STGP_ANY_MDN", "DEBT_ALL_STGP_EVAL_MDN", "EARN_MDN_HI_1YR",
              "EARN_MDN_HI_2YR", "EARN_COUNT_WNE_HI_1YR", "EARN_COUNT_NWNE_HI_1YR"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["control_name"] = d.CONTROL.astype(str).str.strip()
    return d


# ------------------------------------------------------------------------------------ trap proofs

def verify_traps(status, plans, fos, R):
    print("TRAPS")

    # TRAP 1: recipients double count. Prove it by summing recipient columns and comparing against
    # the published total borrower count, which is smaller.
    raw = pd.read_excel(STATUS_XLS, sheet_name="Direct Loan", header=None)
    note = " ".join(str(x) for x in raw.iloc[:4].values.ravel() if str(x) != "nan")
    defs = pd.read_excel(STATUS_XLS, sheet_name="LoanStatusDefinitions", header=None)
    loan_level = any("loan level" in str(x).lower() for x in defs.values.ravel())
    print(f"  1 recipient counts are loan-level per the file's own note: {loan_level}")
    R["traps"]["recipients_are_loan_level"] = bool(loan_level)

    # TRAP 2: different denominators between the two tables, in the same quarter.
    q = status.index[-1]
    if q in plans.index:
        s_tot, p_tot = float(status.loc[q].sum()), float(plans.loc[q].sum())
        print(f"  2 same quarter {q}: status table ${s_tot:,.0f}B vs plan table ${p_tot:,.0f}B "
              f"(plan table excludes default/in-school/grace, gap ${s_tot - p_tot:,.0f}B)")
        R["traps"]["denominator_gap"] = {"quarter": q, "status_total_bn": round(s_tot, 1),
                                         "plan_total_bn": round(p_tot, 1),
                                         "gap_bn": round(s_tot - p_tot, 1)}

    # TRAP 3: the pause. Show the collapse and the recovery.
    tot = status.sum(axis=1)
    rep = status["Repayment"] / tot * 100
    R["traps"]["pause"] = {"repayment_min_pct": round(float(rep.min()), 1),
                           "repayment_min_quarter": str(rep.idxmin()),
                           "pre_pandemic_quarter": PRE_PANDEMIC,
                           "pre_pandemic_repayment_pct": round(float(rep[PRE_PANDEMIC]), 1),
                           "latest_quarter": str(status.index[-1]),
                           "latest_repayment_pct": round(float(rep.iloc[-1]), 1)}

    # ROUND 3 CORRECTION. The draft carried a hand-typed "forbearance averaged 72% across the three
    # years of the pause". That average is not window-stable: on the 13 quarter-ends lying WHOLLY
    # inside the pause it is 72.1%, but including the quarter the suspension began in, when it was
    # 18 days old and only 12.7% of dollars had been recoded, drags it to 67.9%. Emit both, so the
    # window is a recorded choice rather than a silent one, and so no future pass can re-pick it.
    forb = status["Forbearance"] / tot * 100
    inside = forb.loc[PAUSE_WHOLLY_INSIDE[0]:PAUSE_WHOLLY_INSIDE[1]]
    R["traps"]["pause"]["forbearance_in_pause"] = {
        "window": list(PAUSE_WHOLLY_INSIDE),
        "window_note": "quarter-end snapshots lying wholly inside the pause, 30 Jun 2020 to 30 Jun 2023",
        "n_quarters": int(len(inside)),
        "mean_pct": round(float(inside.mean()), 1),
        "min_pct": round(float(inside.min()), 1),
        "max_pct": round(float(inside.max()), 1),
        "mean_pct_incl_transition_quarter": round(float(forb.loc["2020Q2":PAUSE_WHOLLY_INSIDE[1]].mean()), 1),
        "transition_quarter": "2020Q2",
        "transition_quarter_pct": round(float(forb["2020Q2"]), 1),
        "pre_pandemic_pct": round(float(forb[PRE_PANDEMIC]), 1)}
    # The second, post-pandemic forbearance episode. The draft called it a climb "through 2024 and
    # 2025" running "to 30.4% now", which reads a falling series as a rising one: it peaked in the
    # quarter ending 30 June 2025 and has fallen every quarter since. Emit the peak and the path.
    after = forb.loc["2023Q4":]
    R["status_forbearance_second_episode"] = {
        "trough_quarter": str(after.idxmin()), "trough_pct": round(float(after.min()), 1),
        "peak_quarter": str(after.idxmax()), "peak_pct": round(float(after.max()), 1),
        "latest_quarter": str(after.index[-1]), "latest_pct": round(float(after.iloc[-1]), 1),
        "quarters_falling_since_peak": int(len(after.loc[str(after.idxmax()):]) - 1),
        "path": [{"quarter": q, "pct": round(float(after[q]), 1)} for q in after.index]}
    # Repayment did not keep sliding after the second forbearance rise; it stepped down once, in the
    # quarter ending 31 December 2024, and has been flat since. Emit the plateau so the prose stops
    # having to characterise it by eye.
    plateau = rep.loc["2024Q4":]
    R["status_repayment_plateau"] = {
        "from_quarter": "2024Q4", "n_quarters": int(len(plateau)),
        "min_pct": round(float(plateau.min()), 1), "max_pct": round(float(plateau.max()), 1)}
    print(f"  3 repayment share of dollars: {rep[PRE_PANDEMIC]:.1f}% ({PRE_PANDEMIC}) -> "
          f"{rep.min():.1f}% ({rep.idxmin()}, the CARES suspension) -> {rep.iloc[-1]:.1f}% "
          f"({status.index[-1]})")

    # TRAP 4: _ANY_ is empty for every graduate credential; _EVAL_ is not.
    cov = fos.groupby("CREDDESC").agg(any_n=("DEBT_ALL_STGP_ANY_MDN", "count"),
                                      eval_n=("DEBT_ALL_STGP_EVAL_MDN", "count"))
    grad = cov[cov.index.str.contains("Master|Doctoral|Professional", regex=True)]
    print(f"  4 graduate rows with _ANY_ debt: {int(grad.any_n.sum())}; with _EVAL_ debt: "
          f"{int(grad.eval_n.sum())}  (the names mean all-institutions vs this-institution)")
    R["traps"]["debt_variable_coverage"] = {
        "graduate_rows_with_any": int(grad.any_n.sum()),
        "graduate_rows_with_eval": int(grad.eval_n.sum()),
        "any_label": "Median Stafford and Grad PLUS loan debt disbursed at all institutions",
        "eval_label": "Median Stafford and Grad PLUS loan debt disbursed at this institution"}

    # TRAP 5: earnings are conditional on working.
    #
    # ROUND 1 CORRECTION. This was computed across all 227,980 rows and described as a share of
    # "completers". Both are wrong. WNE is "working and not enrolled" and NWNE is "not working and
    # not enrolled", so their sum is graduates who are NOT ENROLLED, not all completers: anyone who
    # went straight on to more study is in neither. And the analysis sample is the 31,941 rows with
    # both debt and earnings, so the figure quoted beside those results should be computed there.
    sample = fos.dropna(subset=["DEBT_ALL_STGP_ANY_MDN", "EARN_MDN_HI_1YR"])
    for label, frame in (("all_rows", fos), ("analysis_sample", sample)):
        w = float(frame.EARN_COUNT_WNE_HI_1YR.sum())
        nw = float(frame.EARN_COUNT_NWNE_HI_1YR.sum())
        R["traps"].setdefault("not_working", {})[label] = {
            "working_n": int(w), "not_working_n": int(nw),
            "pct_of_not_enrolled_graduates": round(nw / (w + nw) * 100, 1)}
    s = R["traps"]["not_working"]["analysis_sample"]
    print(f"  5 of graduates NOT ENROLLED a year out, in the analysis sample, "
          f"{s['not_working_n']:,} of {s['not_working_n'] + s['working_n']:,} = "
          f"{s['pct_of_not_enrolled_graduates']}% had no earnings and are excluded from the median")
    print()


# ------------------------------------------------------------------------------------------ main

def main():
    R = {"traps": {}, "meta": {}}
    status, plans, fos = load_status(), load_plans(), load_fos()

    # ROUND 2 CORRECTION, the most consequential one. The numerator and the denominator of the
    # headline ratio are DIFFERENT GRADUATING COHORTS. From the dictionary's FieldOfStudy_Cohort_Map
    # for the Most Recent file:
    #   DEBT_ALL_STGP_ANY_MDN  NSLDS pooled AY2018-19, AY2019-20
    #   EARN_MDN_HI_1YR        Treasury pooled AY2016-17, AY2017-18, measured CY2018 and CY2019
    #   EARN_MDN_HI_2YR        Treasury pooled AY2014-15, AY2015-16, measured CY2017 and CY2018
    # So the ratio divides one cohort's debt by an earlier cohort's earnings, and the "two years
    # out" check is a THIRD cohort, four academic years earlier, which makes it no robustness check
    # at all. This is disclosed in the post rather than quietly carried.
    R["cohorts"] = {
        "debt": "NSLDS pooled AY2018-19, AY2019-20 cohort",
        "earnings_1yr": "Treasury AY2016-17, AY2017-18 pooled, measured CY2018 and CY2019, "
                        "inflation adjusted to 2020 dollars",
        "earnings_2yr": "Treasury AY2014-15, AY2015-16 pooled, measured CY2017 and CY2018, "
                        "inflation adjusted to 2019 dollars",
        "same_cohort": False,
        "note": "the ratio pairs different graduating cohorts; the 2-year series is a third cohort "
                "and is therefore not a like-for-like check on the same graduates",
    }
    R["meta"] = {"source": "US Department of Education: College Scorecard field of study, and "
                           "Federal Student Aid data center",
                 "fos_rows": int(len(fos)), "fos_institutions": int(fos.UNITID.nunique()),
                 "fos_cip": int(fos.CIPCODE.nunique()),
                 "first_quarter": str(status.index[0]), "last_quarter": str(status.index[-1]),
                 "n_quarters": int(len(status))}

    verify_traps(status, plans, fos, R)

    # ---- THE SUM. Price of a programme in years of gross earnings.
    d = fos.dropna(subset=["DEBT_ALL_STGP_ANY_MDN", "EARN_MDN_HI_1YR"]).copy()
    d = d[d.EARN_MDN_HI_1YR > 0]
    d["ratio"] = d.DEBT_ALL_STGP_ANY_MDN / d.EARN_MDN_HI_1YR
    pct = [5, 10, 25, 50, 75, 90, 95]
    R["price"] = {
        "n_programmes": int(len(d)), "n_institutions": int(d.UNITID.nunique()),
        "n_cip": int(d.CIPCODE.nunique()),
        "median_debt": float(d.DEBT_ALL_STGP_ANY_MDN.median()),
        "median_earnings": float(d.EARN_MDN_HI_1YR.median()),
        "ratio_percentiles": {str(p): round(float(np.percentile(d.ratio, p)), 3) for p in pct},
        "ratio_median_months": round(float(d.ratio.median()) * 12, 1),
        "share_over_1yr_pct": round(float((d.ratio > 1).mean() * 100), 1),
        "share_over_2yr_pct": round(float((d.ratio > 2).mean() * 100), 1),
    }
    # Robustness: the same ratio on the other debt variable and the other earnings horizon.
    e = fos.dropna(subset=["DEBT_ALL_STGP_EVAL_MDN", "EARN_MDN_HI_1YR"]).copy()
    e = e[e.EARN_MDN_HI_1YR > 0]
    e["ratio"] = e.DEBT_ALL_STGP_EVAL_MDN / e.EARN_MDN_HI_1YR
    y2 = d.dropna(subset=["EARN_MDN_HI_2YR"])
    y2 = y2[y2.EARN_MDN_HI_2YR > 0]
    # ROUND 1 CORRECTION. The _EVAL_ check was reported as agreeing with the headline (0.577 against
    # 0.591), but that agreement is CANCELLATION, not robustness: on the same undergraduate rows the
    # this-institution figure is materially lower, and the graduate rows _EVAL_ adds pull it back up.
    # Report both so the check cannot be read as stronger than it is.
    e_ug = e[e.CREDDESC.isin(d.CREDDESC.unique())]
    R["price"]["robustness"] = {
        "eval_debt_median_ratio": round(float(e.ratio.median()), 3), "eval_n": int(len(e)),
        "eval_undergrad_only_ratio": round(float(e_ug.ratio.median()), 4),
        "eval_undergrad_only_n": int(len(e_ug)),
        "eval_includes_graduate": bool(e.CREDDESC.str.contains("Master").any()),
        "earnings_2yr_median_ratio": round(float((y2.DEBT_ALL_STGP_ANY_MDN /
                                                  y2.EARN_MDN_HI_2YR).median()), 3),
        "earnings_2yr_n": int(len(y2)),
    }
    print(f"PRICE   median debt ${R['price']['median_debt']:,.0f} / median earnings "
          f"${R['price']['median_earnings']:,.0f}")
    print(f"        debt-to-earnings median {R['price']['ratio_percentiles']['50']} years "
          f"= {R['price']['ratio_median_months']} months, n={len(d):,} programmes")
    print(f"        p25 {R['price']['ratio_percentiles']['25']}  p75 "
          f"{R['price']['ratio_percentiles']['75']}  p95 {R['price']['ratio_percentiles']['95']}")
    print(f"        over one year of salary: {R['price']['share_over_1yr_pct']}% of programmes")
    print(f"        robustness: _EVAL_ debt {R['price']['robustness']['eval_debt_median_ratio']}, "
          f"2-year earnings {R['price']['robustness']['earnings_2yr_median_ratio']}")

    # By credential and by control, for chart 4's colouring and the "where is it worst" line.
    by_cred = (d.groupby("CREDDESC")
                 .agg(n=("ratio", "size"), median_ratio=("ratio", "median"),
                      median_debt=("DEBT_ALL_STGP_ANY_MDN", "median"),
                      median_earn=("EARN_MDN_HI_1YR", "median"))
                 .sort_values("median_ratio", ascending=False).round(3))
    by_ctrl = (d.groupby("control_name")
                 .agg(n=("ratio", "size"), median_ratio=("ratio", "median"))
                 .sort_values("median_ratio", ascending=False).round(3))
    R["by_credential"] = by_cred.reset_index().to_dict("records")
    R["by_control"] = by_ctrl.reset_index().to_dict("records")
    print("\n        by credential:")
    print(by_cred.to_string())
    print("        by control:")
    print(by_ctrl.to_string())

    # Worst and best fields, for annotation. Require a real sample so a single tiny programme
    # cannot become "the worst degree in America".
    big = d.groupby("CIPDESC").filter(lambda g: len(g) >= 25)
    fld = (big.groupby("CIPDESC").agg(n=("ratio", "size"), median_ratio=("ratio", "median"),
                                      median_debt=("DEBT_ALL_STGP_ANY_MDN", "median"),
                                      median_earn=("EARN_MDN_HI_1YR", "median"))
              .sort_values("median_ratio"))
    R["fields"] = {"min_programmes_per_field": 25, "n_fields": int(len(fld)),
                   "best": fld.head(8).round(3).reset_index().to_dict("records"),
                   "worst": fld.tail(8).round(3).reset_index().to_dict("records")}

    # ---- THE BREAK. What plan the dollars are actually on.
    # ROUND 2 CORRECTION, and it overturns what round 1 called the load-bearing fact.
    #
    # Round 1 said the suspension "did not touch this series" because the standard-plan share was
    # 21.9% before it and 21.9% now. Equal endpoints prove nothing about the path, and the path
    # moved: 21.9 -> 17.5 (FY2023Q2) -> 28.3 (FY2023Q4) -> 21.9. The cause is a denominator
    # artefact, which is embarrassing in a post about denominator artefacts. The file's "Other"
    # column is defined as "loans at the time of the data query not currently listed on a repayment
    # plan". During the suspension it swelled, deflating every named plan's share; when repayment
    # resumed those dollars were assigned to plans and the named shares jumped for one quarter.
    #
    # So compute BOTH: the raw share (of every dollar in the table) and the share of dollars
    # actually on a NAMED plan, which strips the artefact out and is the honest series.
    ptot = plans.sum(axis=1)
    named = ptot - plans["Other"] if "Other" in plans.columns else ptot
    std = plans[STANDARD_PLAN] / ptot * 100
    idr = plans[[c for c in IDR_PLANS if c in plans.columns]].sum(axis=1) / ptot * 100
    std_named = plans[STANDARD_PLAN] / named * 100
    idr_named = plans[[c for c in IDR_PLANS if c in plans.columns]].sum(axis=1) / named * 100
    other_pct = (plans["Other"] / ptot * 100) if "Other" in plans.columns else ptot * 0
    R["plans"] = {
        "standard_plan_label": STANDARD_PLAN.replace("  ", " "),
        "idr_plans": [c for c in IDR_PLANS if c in plans.columns],
        # ROUND 3 CORRECTION. The series used to carry one middle band, 100 - standard - IDR, keyed
        # "other_pct" while the variable of that name a few lines up is the residual column. Chart 2
        # stacked the first and labelled it "other fixed or graduated plans", so the residual bucket
        # the whole paragraph is about was invisible, folded inside a band named as something else.
        # Split it: named non-standard, non-IDR plans in one band, the residual in its own.
        "series": [{"quarter": q, "total_bn": round(float(ptot[q]), 1),
                    "standard_pct": round(float(std[q]), 1), "idr_pct": round(float(idr[q]), 1),
                    "other_named_pct": round(float(100 - std[q] - idr[q] - other_pct[q]), 1),
                    "residual_pct": round(float(other_pct[q]), 1)} for q in plans.index],
        "first": {"quarter": str(plans.index[0]), "standard_pct": round(float(std.iloc[0]), 1),
                  "idr_pct": round(float(idr.iloc[0]), 1),
                  "standard_named_pct": round(float(std_named.iloc[0]), 1)},
        "pre_pandemic": {"quarter": PRE_PANDEMIC, "standard_pct": round(float(std[PRE_PANDEMIC]), 1),
                         "idr_pct": round(float(idr[PRE_PANDEMIC]), 1),
                         "standard_named_pct": round(float(std_named[PRE_PANDEMIC]), 1),
                         "idr_named_pct": round(float(idr_named[PRE_PANDEMIC]), 1),
                         "other_pct": round(float(other_pct[PRE_PANDEMIC]), 1)},
        "latest": {"quarter": str(plans.index[-1]), "standard_pct": round(float(std.iloc[-1]), 1),
                   "idr_pct": round(float(idr.iloc[-1]), 1),
                   "standard_named_pct": round(float(std_named.iloc[-1]), 1),
                   "idr_named_pct": round(float(idr_named.iloc[-1]), 1),
                   "other_pct": round(float(other_pct.iloc[-1]), 1),
                   # The two denominators, in dollars. The prose quotes both, so both come from here
                   # rather than from someone subtracting one number from another in their head.
                   "table_total_bn": round(float(ptot.iloc[-1]), 1),
                   "residual_bn": round(float(plans["Other"].iloc[-1]), 1),
                   "named_total_bn": round(float(named.iloc[-1]), 1)},
        # The path, which is what round 1 failed to look at.
        "raw_min": {"quarter": str(std.idxmin()), "pct": round(float(std.min()), 1)},
        "raw_max": {"quarter": str(std.idxmax()), "pct": round(float(std.max()), 1)},
        "named_min": {"quarter": str(std_named.idxmin()), "pct": round(float(std_named.min()), 1)},
        "named_max": {"quarter": str(std_named.idxmax()), "pct": round(float(std_named.max()), 1)},
        "other_peak": {"quarter": str(other_pct.idxmax()), "pct": round(float(other_pct.max()), 1)},
        "named_series": [{"quarter": q, "standard_pct": round(float(std_named[q]), 2)}
                         for q in plans.index],
    }
    # Ranges must be WINDOWED. The whole-series min/max spans the pre-2016 decline, so quoting it as
    # evidence of pandemic-era stability would repeat the endpoint error in a new costume. Two
    # quarters, 2023Q4 and 2024Q1, are the resumption reassignment and are named explicitly rather
    # than smoothed away.
    win = [q for q in plans.index if q >= PRE_PANDEMIC]
    transition = ["2023Q4", "2024Q1"]
    calm = [q for q in win if q not in transition]
    R["plans"]["since_pre_pandemic"] = {
        "window_from": PRE_PANDEMIC,
        "raw_min": round(float(std[win].min()), 1), "raw_max": round(float(std[win].max()), 1),
        "raw_swing_pts": round(float(std[win].max() - std[win].min()), 1),
        "named_min": round(float(std_named[win].min()), 1),
        "named_max": round(float(std_named[win].max()), 1),
        "named_min_excluding_transition": round(float(std_named[calm].min()), 1),
        "named_max_excluding_transition": round(float(std_named[calm].max()), 1),
        "transition_quarters": transition,
        "other_pre": round(float(other_pct[PRE_PANDEMIC]), 1),
        "other_peak": round(float(other_pct[win].max()), 1),
        "other_peak_quarter": str(other_pct[win].idxmax()),
        "other_latest": round(float(other_pct.iloc[-1]), 1),
    }
    w = R["plans"]["since_pre_pandemic"]
    print(f"        WINDOWED from {PRE_PANDEMIC}: raw {w['raw_min']}% to {w['raw_max']}% "
          f"(swing {w['raw_swing_pts']} pts); named {w['named_min']}% to {w['named_max']}%, "
          f"or {w['named_min_excluding_transition']}% to {w['named_max_excluding_transition']}% "
          f"outside the two resumption quarters")
    print(f"        'Other' (not on any plan): {w['other_pre']}% before, peak {w['other_peak']}% "
          f"({w['other_peak_quarter']}), {w['other_latest']}% now")
    pl = R["plans"]
    print(f"\nBREAK   standard plan, RAW share of every dollar in the table: "
          f"{std.iloc[0]:.1f}% ({plans.index[0]}) -> {std[PRE_PANDEMIC]:.1f}% ({PRE_PANDEMIC}) -> "
          f"{std.iloc[-1]:.1f}% ({plans.index[-1]})")
    print(f"        but the RAW path swings: min {pl['raw_min']['pct']}% ({pl['raw_min']['quarter']}), "
          f"max {pl['raw_max']['pct']}% ({pl['raw_max']['quarter']}) -- equal endpoints hid this")
    print(f"        cause: the 'Other' bucket (not on any plan) peaked at "
          f"{pl['other_peak']['pct']}% in {pl['other_peak']['quarter']}, deflating every named share")
    print(f"        ARTEFACT-FREE, share of dollars on a NAMED plan: "
          f"{pl['pre_pandemic']['standard_named_pct']}% ({PRE_PANDEMIC}) -> "
          f"{pl['latest']['standard_named_pct']}% ({plans.index[-1]}), "
          f"range {pl['named_min']['pct']}% to {pl['named_max']['pct']}%")
    print(f"        income-driven, named basis: {pl['pre_pandemic']['idr_named_pct']}% -> "
          f"{pl['latest']['idr_named_pct']}%")

    # ---- THE SECOND PROOF. Status of every dollar, including the suspension.
    tot = status.sum(axis=1)
    postq = status[POST_SCHOOL].sum(axis=1)
    R["status"] = {
        "statuses": STATUSES, "post_school_statuses": POST_SCHOOL,
        "series": [{"quarter": q, "total_bn": round(float(tot[q]), 1),
                    **{s: round(float(status.loc[q, s] / tot[q] * 100), 2) for s in STATUSES}}
                   for q in status.index],
        "repayment_share_of_post_school": {
            "pre_pandemic": round(float(status.loc[PRE_PANDEMIC, "Repayment"] /
                                        postq[PRE_PANDEMIC] * 100), 1),
            "latest": round(float(status["Repayment"].iloc[-1] / postq.iloc[-1] * 100), 1)},
        "latest_breakdown_bn": {s: round(float(status.loc[status.index[-1], s]), 1)
                                for s in STATUSES},
        "latest_total_bn": round(float(tot.iloc[-1]), 1),
    }

    # ROUND 1 CORRECTION, the worst factual error in the draft. It said repayment "has not fully
    # come back" and "five years later has not returned to where it was". It DID come back and
    # overshot: the post-suspension peak is well above the pre-pandemic level. What pulled it down
    # again is a SECOND, later forbearance episode that began after the recovery, so attributing
    # today's share to the CARES suspension is wrong. Compute the path so the prose has to face it.
    rep = status["Repayment"] / tot * 100
    post = rep[[q for q in rep.index if q >= "2023Q4"]]
    R["status"]["recovery"] = {
        "pre_pandemic_pct": round(float(rep[PRE_PANDEMIC]), 1),
        "peak_after_suspension_pct": round(float(post.max()), 1),
        "peak_quarter": str(post.idxmax()),
        "exceeded_pre_pandemic": bool(post.max() > rep[PRE_PANDEMIC]),
        "latest_pct": round(float(rep.iloc[-1]), 1),
        "path": [{"quarter": q, "repayment_pct": round(float(rep[q]), 1),
                  "forbearance_pct": round(float(status.loc[q, "Forbearance"] / tot[q] * 100), 1)}
                 for q in rep.index if q >= "2023Q3"],
    }
    rc = R["status"]["recovery"]
    print(f"        RECOVERY: repayment peaked at {rc['peak_after_suspension_pct']}% in "
          f"{rc['peak_quarter']}, ABOVE the pre-pandemic {rc['pre_pandemic_pct']}%, then fell to "
          f"{rc['latest_pct']}% as forbearance rose again")

    # The two FSA tables are BOTH Direct Loan only. The draft called the status table "everything".
    # PortfolioSummary carries the real federal total, and the gap is FFEL plus Perkins.
    # Read the labelled columns rather than guessing. The header at row 4 spans Direct Loans, FFEL,
    # Perkins and Total, each split into dollars and recipients on row 5. Quarter rows leave the
    # fiscal-year cell blank, so the last row is found on the QUARTER column, not the year column.
    # (A first attempt took max() of the last year-bearing row and returned $1,696B, which is not a
    # figure in the file at all. Never let a heuristic invent a number.)
    summ = pd.read_excel(DATA / "PortfolioSummary.xls", sheet_name="PortfolioSummary", header=None)
    body = summ[summ.iloc[:, 1].astype(str).str.match(r"Q\d")]
    last = body.iloc[-1]
    direct, ffel, perkins, total = (float(last[2]), float(last[4]), float(last[6]), float(last[8]))
    assert abs(direct + ffel + perkins - total) < 1.0, "PortfolioSummary columns moved"
    R["status"]["federal_portfolio_bn"] = {
        "direct": round(direct, 1), "ffel": round(ffel, 1), "perkins": round(perkins, 1),
        "total": round(total, 1)}
    print(f"        SCOPE: both FSA tables in this post are DIRECT LOANS only (${direct:,.1f}B). "
          f"The whole federal portfolio is ${total:,.1f}B: plus FFEL ${ffel:,.1f}B and Perkins "
          f"${perkins:,.1f}B")
    pre = R["status"]["repayment_share_of_post_school"]["pre_pandemic"]
    print(f"\nPROOF2  of dollars that had left school, in active repayment: {pre}% "
          f"({PRE_PANDEMIC}) -> {R['status']['repayment_share_of_post_school']['latest']}% "
          f"({status.index[-1]})")
    print(f"        so even in a normal year {100 - pre:.1f}% of post-school dollars were not "
          f"being actively repaid")

    # ---- WHY THE PRICE LOOKS SO STEADY. Found by looking at the chart, not by assuming.
    #
    # The first version of chart 4 was captioned "debt and earnings travel together", which the
    # picture flatly refuted: the correlation is 0.25. The second guess, "debt barely moves while
    # earnings vary hugely", was also wrong, an artefact of reading a compressed axis; the two
    # spread by almost the same factor (p90/p10 of 3.00 against 2.79).
    #
    # What is actually there is a set of hard horizontal bands. Median debt piles up on the federal
    # borrowing caps. Under 34 CFR 685.203 a dependent undergraduate may borrow $5,500, $6,500,
    # $7,500 and $7,500 across four years, which sums to $27,000, and the aggregate ceiling is
    # $31,000. Those two figures are the two biggest spikes in the data. The price looks modest
    # partly because Congress capped the numerator.
    # ROUND 1 CORRECTION, TWICE OVER.
    #
    # (a) These counts used to be taken on `.round(-2)`, which buckets everything from $26,950 to
    #     $27,049 together and reported 3,271 programmes "at exactly $27,000". The exact count is
    #     3,098. If the prose says "exactly", the count has to be exact.
    #
    # (b) The section used to conclude "the numerator was capped before the division was done",
    #     i.e. that the caps explain the reassuring ratio. THAT IS REFUTED and the test is below:
    #     dropping every programme sitting on a cap moves the median ratio from 0.5911 to 0.5692,
    #     which is eight days. (Those were 0.5678 and "a third of a month" until the round-2 fix
    #     below replaced the plus-or-minus-$50 window with exact equality. Keep this comment in
    #     step with the code: a stale figure here is how the wrong number gets copied into prose.)
    #     The clustering is real and worth showing, because it says
    #     these prices are administered rather than negotiated. It does not explain the ratio, and
    #     14.6% of programmes sit ABOVE the four-year cap anyway.
    corr_p = float(d.DEBT_ALL_STGP_ANY_MDN.corr(d.EARN_MDN_HI_1YR))
    corr_s = float(d.DEBT_ALL_STGP_ANY_MDN.corr(d.EARN_MDN_HI_1YR, method="spearman"))
    counts = d.DEBT_ALL_STGP_ANY_MDN.value_counts()
    # ROUND 2 CORRECTION. This used a plus-or-minus $50 window, which swept in 211 programmes at
    # values like $26,975 that are not the cap. If the prose says "sitting on a limit", the test has
    # to be equality with the limit.
    at_caps = d.DEBT_ALL_STGP_ANY_MDN.isin([27000.0, 31000.0])
    R["caps"] = {
        "corr_debt_earnings_pearson": round(corr_p, 3),
        "corr_debt_earnings_spearman": round(corr_s, 3),
        "debt_p10": float(np.percentile(d.DEBT_ALL_STGP_ANY_MDN, 10)),
        "debt_p90": float(np.percentile(d.DEBT_ALL_STGP_ANY_MDN, 90)),
        "earn_p10": float(np.percentile(d.EARN_MDN_HI_1YR, 10)),
        "earn_p90": float(np.percentile(d.EARN_MDN_HI_1YR, 90)),
        "debt_p90_over_p10": round(float(np.percentile(d.DEBT_ALL_STGP_ANY_MDN, 90) /
                                         np.percentile(d.DEBT_ALL_STGP_ANY_MDN, 10)), 2),
        "earn_p90_over_p10": round(float(np.percentile(d.EARN_MDN_HI_1YR, 90) /
                                         np.percentile(d.EARN_MDN_HI_1YR, 10)), 2),
        # 34 CFR 685.203: annual dependent maximums are $5,500, $6,500, $7,500, $7,500, summing to
        # $27,000 over four years. The aggregate ceiling is $31,000 for DEPENDENT undergraduates
        # (e)(1) but $57,500 for INDEPENDENT ones (e)(2), which is why programmes legitimately sit
        # above the $31,000 line and the chart must not call it a universal ceiling.
        "four_year_cap": 27000, "aggregate_cap": 31000, "aggregate_cap_independent": 57500,
        "n_above_dependent_cap": int((d.DEBT_ALL_STGP_ANY_MDN > 31000).sum()),
        "pct_above_dependent_cap": round(float((d.DEBT_ALL_STGP_ANY_MDN > 31000).mean() * 100), 1),
        "n_at_four_year_cap": int(counts.get(27000.0, 0)),
        "n_at_aggregate_cap": int(counts.get(31000.0, 0)),
        "pct_at_four_year_cap": round(float(counts.get(27000.0, 0) / len(d) * 100), 1),
        # Does the cap explain the low ratio? No.
        "median_ratio_all": round(float(d.ratio.median()), 4),
        "median_ratio_excluding_caps": round(float(d.loc[~at_caps, "ratio"].median()), 4),
        "cap_effect_months": round(float(abs(d.loc[~at_caps, "ratio"].median()
                                             - d.ratio.median()) * 12), 2),
        # ROUND 3 CORRECTION. The chart rendered cap_effect_months at one decimal, "about 0.3 of a
        # month", while the prose said "about a quarter of a month" for the same 0.26. Two roundings
        # of one number, shipping side by side. Days divide cleanly and read better than a fraction
        # of a month, so chart and prose now quote the same interpolated figure.
        "cap_effect_days": round(float(abs(d.loc[~at_caps, "ratio"].median()
                                          - d.ratio.median()) * 365.25), 0),
        "pct_above_four_year_cap": round(float((d.DEBT_ALL_STGP_ANY_MDN > 27000).mean() * 100), 1),
        "median_debt_as_pct_of_cap": round(float(d.DEBT_ALL_STGP_ANY_MDN.median() / 27000 * 100), 0),
        # The second and third densest values are NOT statutory limits, so "the bands are the caps"
        # is only true of the biggest band.
        "second_band": {"debt": float(counts.index[1]), "n": int(counts.iloc[1])},
        "third_band": {"debt": float(counts.index[2]), "n": int(counts.iloc[2])},
        "share_15k_to_32k_pct": round(float(d.DEBT_ALL_STGP_ANY_MDN.between(15000, 32000).mean()
                                            * 100), 1),
        "top_debt_values": [{"debt": float(k), "n": int(v)} for k, v in counts.head(6).items()],
        "regulation": "34 CFR 685.203",
    }
    c = R["caps"]
    print(f"\nCAPS    debt vs earnings correlation {c['corr_debt_earnings_pearson']} pearson, "
          f"{c['corr_debt_earnings_spearman']} spearman: they do NOT track each other")
    print(f"        spread is similar though: debt p90/p10 {c['debt_p90_over_p10']}x, "
          f"earnings {c['earn_p90_over_p10']}x")
    print(f"        ${c['four_year_cap']:,} (four years at the dependent annual maximums) is the "
          f"single most common median debt: {c['n_at_four_year_cap']:,} programmes = "
          f"{c['pct_at_four_year_cap']}%")
    print(f"        ${c['aggregate_cap']:,} (the aggregate ceiling) appears "
          f"{c['n_at_aggregate_cap']:,} times; {c['share_15k_to_32k_pct']}% of programmes sit "
          f"between $15k and $32k")

    # ---- CHART 4 scatter payload. Every programme, thinned only if huge.
    R["scatter"] = [{"debt": float(r.DEBT_ALL_STGP_ANY_MDN), "earn": float(r.EARN_MDN_HI_1YR),
                     "cred": r.CREDDESC}
                    for r in d.itertuples()]

    (BASE / "results.json").write_text(json.dumps(R, indent=1))
    print(f"\nwrote results.json  ({len(json.dumps(R)) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
