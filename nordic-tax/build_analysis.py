"""Post 21 analysis: how Scandinavia actually pays for itself.

Every number quoted in the post is produced here and written to results.json. Nothing in the
draft may be recalled from memory.

Reads the six files in data/ (see data/README.md for their traps) and answers four questions:

  1. Where does the top income tax bracket begin, as a factor of the average wage?
  2. How is the money actually raised, by type of tax?
  3. What does the revenue buy: poverty, longevity, schooling?
  4. Where does the equalising happen, in the tax system or in the transfer system?

    python3 build_analysis.py
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
DATA = HERE / "data"

# Vintages. These are deliberately separate constants: the three sources do not share a year and
# the post must never imply they do. See data/README.md TRAP 6.
YEAR_THRESHOLD = 2025
# 2021, not 2022, and the reason matters. In 2022 the revenue file is missing a total for Japan
# and Australia and any personal income tax split for Greece, so a 2022 analysis silently drops
# three countries, including the OECD's longest-lived one. Every code is complete for all 38
# members in 2021. One year for everybody beats a newer year for most.
YEAR_REVENUE = 2021
YEAR_LIFE = 2023

# How much a country taxes is a level, not an event. Five complete years, averaged, so that
# one volatile year cannot decide where a country sits on the chart-3 axis.
TAX_WINDOW = [2017, 2018, 2019, 2020, 2021]

# Indonesia uses the SAME window as everything else. An earlier pass introduced a separate
# 2018-2021 "matched window" on the belief that Indonesia's series began in 2018. It does not: the
# 2018 start was an artefact of a startPeriod parameter in fetch_data.py. Round 2 caught it.
MATCHED_WINDOW = TAX_WINDOW

# Denmark's arbejdsmarkedsbidrag. Danish statutory thresholds are stated on personlig indkomst,
# which is already net of it, while the average wage is gross, so a threshold must be grossed up
# before the two can meet. This is the whole of TRAP 1 and it is why OECD's published factor
# cannot be reproduced by dividing a threshold by a wage.
AM_BIDRAG = 0.08

# The countries the post names. Everything else is still plotted, just unlabelled.
NORDIC = ["DNK", "SWE", "NOR", "FIN", "ISL"]
LABELLED = NORDIC + ["USA", "DEU", "FRA", "BEL", "IRL", "NLD", "GBR", "JPN", "ESP", "ITA", "CHE"]

# Personal income tax. T_1100 is "Taxes on income, profits and capital gains of individuals";
# T_1110 is "Taxes on income and profits of individuals". The difference between them is CAPITAL
# GAINS, not the individual-versus-corporate split (that is T_1300, "unallocable"). T_1110 is
# missing for five countries in 2021 and seven in 2022, so the wider T_1100 is used throughout.
# Both are computed below and the gap recorded, so the choice is visible rather than buried.
PIT_CODE = "T_1100"
PIT_CODE_NARROW = "T_1110"

REV_CODES = {
    "_T": "total",
    "T_1100": "personal_income",
    "T_1110": "personal_income_narrow",
    "T_1200": "corporate_income",
    "T_1300": "income_unallocable",
    "T_2000": "social_contributions",
    "T_3000": "payroll",
    "T_4000": "property",
    "T_5111": "vat",
    "T_5000": "goods_and_services_all",
    "T_6000": "other_taxes",
}

# The bands of the stacked revenue chart. They must sum to the published total, or the chart
# is hiding a residual. Reconciliation is checked below and recorded in results.json.
STACK_BANDS = [
    ("personal_income", "Personal income tax"),
    ("social_contributions", "Social security contributions"),
    ("vat", "Value added tax"),
    ("other_goods_services", "Other taxes on goods and services (excises, vehicle and the rest)"),
    ("payroll", "Payroll taxes"),
    ("corporate_income", "Corporate income tax"),
    ("property", "Property taxes"),
    ("residual", "Unallocable income tax and other taxes"),
]

# IDD dimension choices. Fixed once here and used by every IDD read in this file.
IDD_AGE = "_T"           # total population, not working age
IDD_METH = "METH2012"    # income definition since 2012
IDD_DEFN = "D_CUR"       # current definition; 41 countries carry all three Gini series
IDD_PLINE = "PL_50"      # 50 percent of median disposable income


# ---------------------------------------------------------------------------
# loaders
# ---------------------------------------------------------------------------

def load_prior_year(measure, year):
    """One threshold measure for the year before the analysis year.

    Used only to show what a country reported before a zero appeared, which is how a
    missing-value placeholder is told apart from a genuine flat tax.
    """
    d = pd.read_csv(DATA / "pit_thresh.csv", low_memory=False)
    d = d[(d.TIME_PERIOD == year) & (d.MEASURE == measure)]
    return d.set_index("REF_AREA").OBS_VALUE


def load_thresholds():
    """OECD Tax Database Table I.7.

    TS_PIT_TH is OECD's own published multiple of the average wage. It is never recomputed here;
    see data/README.md TRAP 1 for why dividing a threshold by a wage gives a different number.
    """
    d = pd.read_csv(DATA / "pit_thresh.csv", low_memory=False)
    d = d[d.TIME_PERIOD == YEAR_THRESHOLD]

    def one(measure, unit=None):
        s = d[d.MEASURE == measure]
        if unit is not None:
            s = s[s.UNIT_MEASURE == unit]
        return s.set_index("REF_AREA").OBS_VALUE

    out = pd.DataFrame({
        "country": d.drop_duplicates("REF_AREA").set_index("REF_AREA")["Reference area"],
        "threshold_x_avg_wage": one("TS_PIT_TH"),
        "top_rate_pct": one("TS_PIT"),
        "rate_at_threshold_pct": one("PIT_R_TH"),
        "rate_plus_employee_ssc_pct": one("PIT_SSC_R_TH"),
        "avg_wage_lcu": one("WGE", "XDC"),
        "avg_wage_usd_ppp": one("WGE", "USD_PPP"),
    })
    return out.dropna(subset=["threshold_x_avg_wage"])


def load_revenue(path, year):
    """Tax revenue as percent of GDP, general government, for one year."""
    keep = []
    for chunk in pd.read_csv(path, low_memory=False, chunksize=300_000):
        s = chunk[
            (chunk.UNIT_MEASURE == "PT_B1GQ")
            & (chunk.SECTOR == "S13")
            & (chunk.TIME_PERIOD == year)
            & (chunk.STANDARD_REVENUE.isin(REV_CODES))
        ]
        keep.append(s[["REF_AREA", "Reference area", "STANDARD_REVENUE", "OBS_VALUE"]])
    d = pd.concat(keep)
    names = d.drop_duplicates("REF_AREA").set_index("REF_AREA")["Reference area"]
    p = d.pivot_table(index="REF_AREA", columns="STANDARD_REVENUE", values="OBS_VALUE")
    p = p.rename(columns=REV_CODES)
    p.insert(0, "country", names)
    return p


def load_code_mean(path, code, years):
    """Mean revenue for one classification code, as percent of GDP, over a window of years.

    A single year is a bad measure of how much a country taxes. Denmark's total swings from
    47.4 percent of GDP in 2021 to 41.9 in 2022 because its pension yield tax rides on
    investment returns, which moves Denmark from near the top of the OECD to seventh on the
    choice of year alone. Averaging a window is more honest for a cross-sectional axis, and
    the per-year values are kept so the volatility can be shown rather than smoothed away.
    """
    keep = []
    for chunk in pd.read_csv(path, low_memory=False, chunksize=300_000):
        s = chunk[
            (chunk.UNIT_MEASURE == "PT_B1GQ")
            & (chunk.SECTOR == "S13")
            & (chunk.STANDARD_REVENUE == code)
            & (chunk.TIME_PERIOD.isin(years))
        ]
        keep.append(s[["REF_AREA", "TIME_PERIOD", "OBS_VALUE"]])
    d = pd.concat(keep)
    wide = d.pivot_table(index="REF_AREA", columns="TIME_PERIOD", values="OBS_VALUE")
    return pd.DataFrame({
        "mean": wide.mean(axis=1),
        "min": wide.min(axis=1),
        "max": wide.max(axis=1),
        "years_n": wide.notna().sum(axis=1),
    })


def load_total_tax_mean(path, years):
    """Averaged total tax revenue, with the column names the rest of this file expects."""
    return load_code_mean(path, "_T", years).rename(columns={
        "mean": "total_tax_mean", "min": "total_tax_min",
        "max": "total_tax_max", "years_n": "total_tax_years_n",
    })


def load_idd(measure, poverty_line=None):
    """One OECD Income Distribution Database series, latest year per country.

    The three dimension choices are module constants so that no two reads of this file can
    silently disagree with each other.
    """
    d = pd.read_csv(DATA / "idd.csv", low_memory=False)
    s = d[
        (d.MEASURE == measure)
        & (d.AGE == IDD_AGE)
        & (d.METHODOLOGY == IDD_METH)
        & (d.DEFINITION == IDD_DEFN)
    ]
    if poverty_line is not None:
        s = s[s.POVERTY_LINE == poverty_line]
    s = s.sort_values("TIME_PERIOD").groupby("REF_AREA").tail(1)
    return s.set_index("REF_AREA")[["OBS_VALUE", "TIME_PERIOD"]].rename(
        columns={"OBS_VALUE": measure, "TIME_PERIOD": f"{measure}_year"}
    )


def load_gdp():
    """GDP per capita, PPP, constant 2021 international dollars, for the revenue year."""
    d = pd.read_csv(DATA / "gdp.csv")
    col = [c for c in d.columns if c not in ("entity", "code", "year")][0]
    d = d[(d.year == YEAR_REVENUE) & d.code.notna()]
    return d.set_index("code")[col].rename("gdp_pc")


def load_life():
    d = pd.read_csv(DATA / "le.csv")
    d = d[(d.year == YEAR_LIFE) & d.code.notna()]
    return d.set_index("code").life_expectancy_0.rename("life_expectancy")


# ---------------------------------------------------------------------------
# analysis
# ---------------------------------------------------------------------------

def fit(x, y):
    """Slope, r and R-squared for a simple linear fit, on the rows where both exist."""
    m = x.notna() & y.notna()
    if m.sum() < 3:
        return None
    xs, ys = x[m].astype(float), y[m].astype(float)
    r = float(np.corrcoef(xs, ys)[0, 1])
    slope, intercept = np.polyfit(xs, ys, 1)
    return {
        "n": int(m.sum()),
        "slope": round(float(slope), 4),
        "intercept": round(float(intercept), 4),
        "r": round(r, 4),
        "r2": round(r ** 2, 4),
    }


def multi_fit(y, *xs):
    """R-squared of an ordinary least squares fit of y on the given predictors plus a constant."""
    cols = [np.asarray(x, dtype=float) for x in xs]
    yv = np.asarray(y, dtype=float)
    m = np.isfinite(yv)
    for c in cols:
        m &= np.isfinite(c)
    if m.sum() < len(cols) + 3:
        return None
    X = np.column_stack([np.ones(m.sum())] + [c[m] for c in cols])
    yy = yv[m]
    beta, *_ = np.linalg.lstsq(X, yy, rcond=None)
    resid = yy - X @ beta
    ss_res = float(resid @ resid)
    ss_tot = float(((yy - yy.mean()) ** 2).sum())
    return {"n": int(m.sum()), "r2": round(1 - ss_res / ss_tot, 4)}


def main():
    res = {
        "vintages": {
            "thresholds": YEAR_THRESHOLD,
            "revenue": YEAR_REVENUE,
            "life_expectancy": YEAR_LIFE,
            "note": ("Five time bases: thresholds 2025, revenue 2021, life expectancy 2023, a "
                     "2017-2021 mean tax level, and income-distribution data at the latest year "
                     "per country (2019 to 2025). Every figure in the post states its own."),
        },
        "idd_choices": {
            "age": IDD_AGE, "methodology": IDD_METH,
            "definition": IDD_DEFN, "poverty_line": IDD_PLINE,
        },
    }

    # -- 1. where the top bracket begins ------------------------------------
    th = load_thresholds()
    prior_th = load_prior_year("TS_PIT_TH", YEAR_THRESHOLD - 1)
    prior_rate = load_prior_year("TS_PIT", YEAR_THRESHOLD - 1)
    oecd_members = sorted(th.index)
    res["oecd_members_n"] = len(oecd_members)

    # A zero threshold means two completely different things and round 3 caught this repo
    # conflating them. Hungary reports threshold 0 alongside a real 15 percent rate every year:
    # a genuine flat tax. Latvia reports threshold 0 AND rate 0, and only in 2025, after
    # thresholds of 3.9 to 4.9 times the average wage every year from 2018 to 2024. That is a
    # missing-value placeholder, not a tax system. Classifying it as a flat tax put a false
    # statement about Latvian law into the essay and into a shipped chart.
    zero_th = th[th.threshold_x_avg_wage == 0]
    flat = zero_th[zero_th.top_rate_pct > 0]
    unusable = zero_th[~(zero_th.top_rate_pct > 0)]
    res["flat_tax_excluded"] = {
        "reason": ("Top rate applies from the first unit of income, so a multiple of the average "
                   "wage is not defined. Excluded from the threshold chart and named there."),
        "countries": [{"code": c, "country": r.country,
                       "top_rate_pct": None if pd.isna(r.top_rate_pct) else float(r.top_rate_pct)}
                      for c, r in flat.iterrows()],
    }
    res["unusable_excluded"] = {
        "reason": ("Both the threshold and the top rate are reported as zero in the analysis year, "
                   "which is a missing-value placeholder rather than a flat tax. Excluded from the "
                   "threshold chart for a different reason and must be described differently."),
        "countries": [{"code": c, "country": r.country,
                       "prior_year_threshold": (
                           None if c not in prior_th.index else round(float(prior_th[c]), 2)),
                       "prior_year_top_rate_pct": (
                           None if c not in prior_rate.index else round(float(prior_rate[c]), 1))}
                      for c, r in unusable.iterrows()],
    }
    # A tripwire for future vintages, not a classification. Anything already explained by the two
    # blocks above is excluded, so a country never appears in two of these at once: in round 3
    # Latvia sat in unusable_excluded AND here, which is the contradiction that let a false
    # statement about Latvian law survive three fact-check rounds.
    res["implausible_top_rate"] = [
        {"code": c, "country": r.country, "top_rate_pct": float(r.top_rate_pct)}
        for c, r in th.iterrows()
        if pd.notna(r.top_rate_pct) and r.top_rate_pct == 0
        and c not in unusable.index and c not in flat.index
    ]

    th_ranked = th[th.threshold_x_avg_wage > 0].sort_values("threshold_x_avg_wage")
    res["thresholds"] = [
        {
            "rank": i,
            "code": c,
            "country": r.country,
            "threshold_x_avg_wage": round(float(r.threshold_x_avg_wage), 2),
            "top_rate_pct": None if pd.isna(r.top_rate_pct) else round(float(r.top_rate_pct), 1),
            "rate_plus_employee_ssc_pct": (
                None if pd.isna(r.rate_plus_employee_ssc_pct)
                else round(float(r.rate_plus_employee_ssc_pct), 1)
            ),
        }
        for i, (c, r) in enumerate(th_ranked.iterrows(), 1)
    ]
    res["threshold_headline"] = {
        code: round(float(th.loc[code, "threshold_x_avg_wage"]), 2)
        for code in ["DNK", "SWE", "NOR", "FIN", "ISL", "USA", "DEU", "BEL", "IRL", "NLD", "FRA"]
        if code in th.index
    }
    # The two disciplines the design doc requires the post to carry.
    nordic_th = th.loc[[c for c in NORDIC if c in th.index], "threshold_x_avg_wage"]
    res["nordics_are_not_a_bloc"] = {
        "spread": {c: round(float(v), 2) for c, v in nordic_th.sort_values().items()},
        "min": round(float(nordic_th.min()), 2),
        "max": round(float(nordic_th.max()), 2),
        "ratio_max_over_min": round(float(nordic_th.max() / nordic_th.min()), 2),
    }
    below_dk = th_ranked[th_ranked.threshold_x_avg_wage < th.loc["DNK", "threshold_x_avg_wage"]]
    res["at_or_below_denmark"] = [
        {"code": c, "country": r.country, "threshold_x_avg_wage": round(float(r.threshold_x_avg_wage), 2)}
        for c, r in below_dk.iterrows()
    ]

    # What OECD's indicator would print for Denmark in 2026 if it tracks the new top-top tier.
    # "top-top", not "top": the draft names three tiers, and the middle one is the DKK 777,900 top
    # tax, whose factor is 1.57, not five. OECD has published no 2026 figure, so this is the post's
    # own projection and is labelled as such wherever it appears. Every Danish statutory figure the
    # draft prints is encoded here rather than recalled, because the post's standing rule is that
    # every number in the essay is produced by this script.
    #
    # Statutory thresholds are on personlig indkomst, already net of the 8 percent AM-bidrag, so
    # they gross up by dividing by 0.92 before meeting a gross average wage (see TRAP 1).
    toptop_2026 = 2_592_700.0            # Skatteministeriet, toptopskattegraense 2026
    mellem_2026 = 641_200.0              # Skatteministeriet, mellemskattegraense 2026
    top_2026 = 777_900.0                 # Skatteministeriet, topskattegraense 2026
    kapital_bundfradrag_2026 = 55_000.0  # Skatteministeriet, bundfradrag for positiv
                                         # nettokapitalindkomst 2026, single taxpayer
    topskat_2025 = 611_800.0             # Skatteministeriet, topskattegraense 2025
    dnk_wage_2025 = float(th.loc["DNK", "avg_wage_lcu"])
    factors = {
        f"wage_growth_{int(g * 100)}pct": round(
            (toptop_2026 / (1 - AM_BIDRAG)) / (dnk_wage_2025 * (1 + g)), 2)
        for g in (0.02, 0.04, 0.06)
    }
    res["denmark_2026_projection"] = {
        "note": ("Projection, not an OECD publication. OECD has published no 2026 threshold for "
                 "Denmark. If it tracks the new top-top tier rather than the middle tax, the "
                 "factor of the average wage moves from the 2025 value to roughly five."),
        "toptop_threshold_dkk": toptop_2026,
        "am_bidrag": AM_BIDRAG,
        "gross_equivalent_dkk": round(toptop_2026 / (1 - AM_BIDRAG), 2),
        "mellem_threshold_2026_dkk": mellem_2026,
        "top_threshold_2026_dkk": top_2026,
        "capital_allowance_2026_single_dkk": kapital_bundfradrag_2026,
        "capital_allowance_2026_couple_dkk": 2 * kapital_bundfradrag_2026,
        "topskat_threshold_2025_dkk": topskat_2025,
        "topskat_gross_equivalent_2025_dkk": round(topskat_2025 / (1 - AM_BIDRAG), 2),
        "avg_wage_2025_dkk": round(dnk_wage_2025, 2),
        "factor_2025_published": round(float(th.loc["DNK", "threshold_x_avg_wage"]), 2),
        "projected_factor_by_wage_growth": factors,
        "range": [min(factors.values()), max(factors.values())],
    }

    # -- 2. how the money is raised -----------------------------------------
    rev = load_revenue(DATA / "rev_oecd.csv", YEAR_REVENUE)
    rev_members = rev[rev.index.isin(oecd_members)].copy()

    # Coverage of the two personal income tax codes, so the choice of T_1100 is auditable.
    res["pit_code_choice"] = {
        "used": PIT_CODE,
        "reason": ("T_1100 includes individuals' capital gains; T_1110 excludes them. The gap "
                   "between the two codes is capital gains, not the individual-versus-corporate "
                   "split, which is T_1300. T_1110 is not reported by every country, so the "
                   "wider T_1100 is used. Counts are on OECD members in the revenue year."),
        "n_reporting_T_1100": int(rev_members["personal_income"].notna().sum()),
        "n_reporting_T_1110": int(rev_members["personal_income_narrow"].notna().sum()),
        "missing_T_1110": sorted(
            rev_members.index[rev_members["personal_income_narrow"].isna()].tolist()
        ),
    }

    # VAT is split out of the goods and services total so the stacked chart can name it. The
    # remainder is excises, vehicle taxes and the rest, and its label must say so.
    rev_members["other_goods_services"] = (
        rev_members.goods_and_services_all.fillna(0) - rev_members.vat.fillna(0)
    )
    # Payroll is its own band, not part of the residual. Sweden raises 5.0 percent of GDP that
    # way and it is a labour tax, so burying it would misstate exactly the thing this post is
    # about. Austria and France are the other two where it is material.
    named = ["personal_income", "social_contributions", "vat", "other_goods_services",
             "payroll", "corporate_income", "property"]
    rev_members["residual"] = (
        rev_members.total - rev_members[named].fillna(0).sum(axis=1)
    )
    res["stack_reconciliation"] = {
        "bands": [b for b, _ in STACK_BANDS],
        "note": ("The six named bands plus a residual sum to the published total by construction. "
                 "The residual is payroll taxes, income tax unallocable between individuals and "
                 "corporations, and other taxes. Its size is reported so it cannot hide anything."),
        "residual_max_pct_gdp": round(float(rev_members.residual.max()), 2),
        "residual_max_country": str(rev_members.residual.idxmax()),
        "residual_median_pct_gdp": round(float(rev_members.residual.median()), 2),
        "residual_negative_countries": sorted(
            rev_members.index[rev_members.residual < -0.05].tolist()
        ),
    }

    mix_cols = ["total", "personal_income", "social_contributions", "vat",
                "other_goods_services", "goods_and_services_all", "corporate_income",
                "property", "payroll", "other_taxes", "residual"]
    res["tax_mix"] = [
        {"code": c, "country": r.country,
         **{k: (None if pd.isna(r.get(k)) else round(float(r[k]), 2)) for k in mix_cols}}
        for c, r in rev_members.sort_values("total", ascending=False).iterrows()
    ]
    res["tax_mix_oecd_mean"] = {
        "note": "Unweighted mean across OECD members reporting each component. Computed here; "
                "the OECD row in the source file carries a total but no component breakdown.",
        **{k: round(float(rev_members[k].mean()), 2) for k in mix_cols},
        "n_by_component": {k: int(rev_members[k].notna().sum()) for k in mix_cols},
    }

    # The correction at the centre of the post: income tax versus income tax plus contributions.
    lab = rev_members.assign(
        labour_taxes=(rev_members.personal_income.fillna(0)
                      + rev_members.social_contributions.fillna(0)
                      + rev_members.payroll.fillna(0))
    )
    res["labour_tax_correction"] = {
        "note": ("Denmark's social contributions are essentially zero, not missing. Comparing "
                 "personal income tax lines alone compares plumbing, not burden. Payroll taxes "
                 "are included in the combined figure because Sweden raises 5 percent of GDP "
                 "that way and it is a tax on labour by any reading."),
        "columns": "personal income tax, social contributions, payroll taxes, their sum, and total tax",
        "by_country": [
            {"code": c, "country": lab.loc[c, "country"],
             "personal_income": round(float(lab.loc[c, "personal_income"]), 2),
             "social_contributions": round(float(lab.loc[c, "social_contributions"]), 2),
             "payroll": round(float(lab.loc[c, "payroll"]), 2),
             "labour_taxes_combined": round(float(lab.loc[c, "labour_taxes"]), 2),
             "total": round(float(lab.loc[c, "total"]), 2)}
            for c in ["DNK", "SWE", "NOR", "FIN", "ISL", "DEU", "FRA", "NLD", "GBR", "USA"]
            if c in lab.index and pd.notna(lab.loc[c, "personal_income"])
        ],
    }
    res["labour_tax_spread"] = {
        "note": ("How close the combined labour tax burden is across the countries the post "
                 "names, against how far apart their personal income tax lines look."),
        "personal_income_min_max": [
            round(float(lab.loc[["DNK", "SWE", "NOR", "FIN", "DEU", "FRA", "NLD", "GBR", "USA"],
                                "personal_income"].min()), 2),
            round(float(lab.loc[["DNK", "SWE", "NOR", "FIN", "DEU", "FRA", "NLD", "GBR", "USA"],
                                "personal_income"].max()), 2),
        ],
        "combined_min_max": [
            round(float(lab.loc[["DNK", "SWE", "NOR", "FIN", "DEU", "FRA", "NLD", "GBR", "USA"],
                                "labour_taxes"].min()), 2),
            round(float(lab.loc[["DNK", "SWE", "NOR", "FIN", "DEU", "FRA", "NLD", "GBR", "USA"],
                                "labour_taxes"].max()), 2),
        ],
    }
    res["missing_personal_income_tax"] = sorted(
        rev_members.index[rev_members.personal_income.isna()].tolist()
    )

    # Five countries whose personal income tax lines differ by a factor of two and a half collect
    # within a couple of points of GDP of each other once every tax on labour is counted. Round 1
    # refuted the unqualified gloss "routing, not burden": the convergence belongs to these five
    # (see selection_sensitivity below), and Denmark still ranks 4/38 on labour taxes and 1/38 on
    # total tax. It supports the Denmark-versus-Germany-and-France comparison, nothing wider.
    CONVERGE = ["DNK", "SWE", "FIN", "DEU", "FRA"]
    cv = lab.loc[CONVERGE]
    res["labour_tax_convergence"] = {
        "countries": [str(rev_members.loc[c, "country"]) for c in CONVERGE],
        "personal_income_range": [round(float(cv.personal_income.min()), 2),
                                  round(float(cv.personal_income.max()), 2)],
        "personal_income_ratio": round(float(cv.personal_income.max() / cv.personal_income.min()), 2),
        "combined_range": [round(float(cv.labour_taxes.min()), 2),
                           round(float(cv.labour_taxes.max()), 2)],
        "combined_spread_pts": round(float(cv.labour_taxes.max() - cv.labour_taxes.min()), 2),
        "detail": [
            {"code": c, "country": str(rev_members.loc[c, "country"]),
             "personal_income": round(float(cv.loc[c, "personal_income"]), 2),
             "social_contributions": round(float(cv.loc[c, "social_contributions"]), 2),
             "payroll": round(float(cv.loc[c, "payroll"]), 2),
             "combined": round(float(cv.loc[c, "labour_taxes"]), 2)}
            for c in CONVERGE
        ],
    }
    res["norway_petroleum_flag"] = {
        "corporate_income_pct_gdp": round(float(rev_members.loc["NOR", "corporate_income"]), 2),
        "oecd_mean_corporate": round(float(rev_members["corporate_income"].mean()), 2),
        "note": "Norway's corporate tax is petroleum revenue. Flagged wherever Norway appears.",
    }

    # -- 3. what it buys -----------------------------------------------------
    pov_mkt = load_idd("PR_INC_MRKT", IDD_PLINE)
    pov_dsp = load_idd("PR_INC_DISP", IDD_PLINE)
    life = load_life()

    tax_mean = load_total_tax_mean(DATA / "rev_oecd.csv", TAX_WINDOW)
    res["tax_level_volatility"] = {
        "window": [min(TAX_WINDOW), max(TAX_WINDOW)],
        "note": ("How much a country taxes is measured as the mean total tax revenue over the "
                 "window, not a single year. Within this window Denmark's own swing is 3.25 "
                 "points, sixth largest. The five-point-plus fall that motivates the averaging "
                 "happens between 2021 and 2022, which is OUTSIDE the window; see "
                 "denmark_2022_fall, which decomposes it rather than attributing it to one tax."),
        "biggest_swings": [
            {"code": c, "country": rev_members.loc[c, "country"] if c in rev_members.index else c,
             "mean": round(float(r.total_tax_mean), 2),
             "min": round(float(r.total_tax_min), 2),
             "max": round(float(r.total_tax_max), 2),
             "swing_pts": round(float(r.total_tax_max - r.total_tax_min), 2)}
            for c, r in tax_mean.assign(sw=tax_mean.total_tax_max - tax_mean.total_tax_min)
                                .sort_values("sw", ascending=False).head(8).iterrows()
        ],
    }

    out = rev_members[["country", "total"]].join(tax_mean).join(pov_mkt).join(pov_dsp).join(life)
    out["poverty_reduction_pts"] = out.PR_INC_MRKT - out.PR_INC_DISP
    out["poverty_reduction_pct"] = 100 * out.poverty_reduction_pts / out.PR_INC_MRKT

    res["outcomes"] = [
        {"code": c, "country": r.country,
         "total_tax_pct_gdp_year": None if pd.isna(r.total) else round(float(r.total), 2),
         "total_tax_mean": None if pd.isna(r.total_tax_mean) else round(float(r.total_tax_mean), 2),
         "total_tax_swing_pts": None if pd.isna(r.total_tax_max) else round(float(r.total_tax_max - r.total_tax_min), 2),
         "poverty_market_pct": None if pd.isna(r.PR_INC_MRKT) else round(float(r.PR_INC_MRKT), 2),
         "poverty_disposable_pct": None if pd.isna(r.PR_INC_DISP) else round(float(r.PR_INC_DISP), 2),
         "poverty_year": None if pd.isna(r.get("PR_INC_DISP_year")) else int(r["PR_INC_DISP_year"]),
         "poverty_reduction_pts": None if pd.isna(r.poverty_reduction_pts) else round(float(r.poverty_reduction_pts), 2),
         "life_expectancy": None if pd.isna(r.life_expectancy) else round(float(r.life_expectancy), 2)}
        for c, r in out.sort_values("total_tax_mean", ascending=False).iterrows()
    ]
    res["outcome_fits"] = {
        "tax_vs_poverty_disposable": fit(out.total_tax_mean, out.PR_INC_DISP),
        "tax_vs_poverty_reduction_pts": fit(out.total_tax_mean, out.poverty_reduction_pts),
        "tax_vs_life_expectancy": fit(out.total_tax_mean, out.life_expectancy),
        "note": ("Cross-country association on the OECD field. Not causal, and not evidence that "
                 "health spending does or does not work."),
    }
    # Robustness. A positive tax-versus-longevity association across the whole OECD field is
    # suspect: the low-tax end of that field is also the poor end. If the association is really
    # about income rather than tax, it should weaken sharply once the poorer members are removed
    # and once the United States, a large visible outlier, is removed. Test both rather than
    # asserting either.
    # Which countries leave is not a judgement call. It is the five OECD members with the lowest
    # GDP per capita, taken from the data rather than chosen. Greece is sixth and stays in.
    gdp = load_gdp()
    gdp_oecd = gdp[gdp.index.isin(oecd_members)].sort_values()
    POORER = list(gdp_oecd.head(5).index)
    res["poorer_rule"] = {
        "rule": ("The five OECD members with the lowest GDP per capita, PPP, constant 2021 "
                 f"international dollars, in {YEAR_REVENUE}. Selected from the data, not by hand."),
        "excluded": [{"code": c, "gdp_pc": round(float(gdp_oecd[c]))} for c in POORER],
        "next_in_line": {"code": str(gdp_oecd.index[5]), "gdp_pc": round(float(gdp_oecd.iloc[5]))},
        "oecd_median_gdp_pc": round(float(gdp_oecd.median())),
    }

    # The cutoff-free version of the same test. If the tax level only looks like it buys longer
    # life because richer countries tax more, then adding income to the model should absorb
    # nearly all of what tax appeared to explain. Reported as incremental R-squared so no
    # threshold has to be defended.
    out = out.join(gdp)
    log_gdp = np.log(out.gdp_pc)
    res["income_control"] = {
        "note": ("Ordinary least squares on the full OECD field. 'Income only' regresses the "
                 "outcome on log GDP per capita. 'Income plus tax' adds the averaged tax level. "
                 "The increment is what the tax level explains that income does not."),
        "outcomes": {},
    }
    for name, series in [("life_expectancy", out.life_expectancy),
                         ("poverty_disposable", out.PR_INC_DISP),
                         ("poverty_reduction_pts", out.poverty_reduction_pts)]:
        only_tax = multi_fit(series, out.total_tax_mean)
        only_inc = multi_fit(series, log_gdp)
        both = multi_fit(series, log_gdp, out.total_tax_mean)
        res["income_control"]["outcomes"][name] = {
            "tax_only_r2": only_tax["r2"], "income_only_r2": only_inc["r2"],
            "income_plus_tax_r2": both["r2"],
            "increment_from_tax": round(both["r2"] - only_inc["r2"], 4),
            "n": both["n"],
        }

    subsets = {
        "all_oecd": out,
        "excl_united_states": out.drop(index=["USA"], errors="ignore"),
        "excl_poorer_members": out.drop(index=POORER, errors="ignore"),
        "excl_poorer_and_usa": out.drop(index=POORER + ["USA"], errors="ignore"),
    }
    res["outcome_robustness"] = {
        "poorer_members_removed": POORER,
        "note": ("The OECD's low-tax end is also its low-income end, so any tax-versus-outcome "
                 "association across the full field may be an income association wearing a tax "
                 "label. These subsets test that. Read the R-squared column, not the sign."),
        "fits": {
            name: {
                "tax_vs_life_expectancy": fit(s.total_tax_mean, s.life_expectancy),
                "tax_vs_poverty_disposable": fit(s.total_tax_mean, s.PR_INC_DISP),
                "tax_vs_poverty_reduction_pts": fit(s.total_tax_mean, s.poverty_reduction_pts),
            }
            for name, s in subsets.items()
        },
    }

    res["life_expectancy_ranked"] = [
        {"code": c, "country": rev_members.loc[c, "country"] if c in rev_members.index else c,
         "life_expectancy": round(float(v), 2)}
        for c, v in life[life.index.isin(oecd_members)].sort_values(ascending=False).items()
    ]

    # -- 4. where the equalising happens -------------------------------------
    g_mkt = load_idd("INC_MRKT_GINI")
    g_grs = load_idd("INC_GROSS_GINI")
    g_dsp = load_idd("INC_DISP_GINI")
    gini = g_mkt.join(g_grs, how="inner").join(g_dsp, how="inner")
    gini = gini[gini.index.isin(oecd_members)]

    # market -> gross adds cash transfers; gross -> disposable removes direct taxes and employee SSC
    gini["transfer_effect"] = gini.INC_MRKT_GINI - gini.INC_GROSS_GINI
    gini["tax_effect"] = gini.INC_GROSS_GINI - gini.INC_DISP_GINI
    gini["total_effect"] = gini.INC_MRKT_GINI - gini.INC_DISP_GINI
    gini["transfer_share_pct"] = 100 * gini.transfer_effect / gini.total_effect

    res["redistribution"] = {
        "note": ("Market to gross adds cash transfers. Gross to disposable removes direct taxes "
                 "and employee social contributions. Latest year per country, stated per row."),
        "n_countries": int(len(gini)),
        "by_country": [
            {"code": c, "country": rev_members.loc[c, "country"] if c in rev_members.index else c,
             "year": int(r.INC_MRKT_GINI_year),
             "gini_market": round(float(r.INC_MRKT_GINI), 4),
             "gini_gross": round(float(r.INC_GROSS_GINI), 4),
             "gini_disposable": round(float(r.INC_DISP_GINI), 4),
             "transfer_effect": round(float(r.transfer_effect), 4),
             "tax_effect": round(float(r.tax_effect), 4),
             "total_effect": round(float(r.total_effect), 4),
             "transfer_share_pct": round(float(r.transfer_share_pct), 1)}
            for c, r in gini.sort_values("total_effect", ascending=False).iterrows()
        ],
        "transfer_share_median_pct": round(float(gini.transfer_share_pct.median()), 1),
        "transfer_share_gt_50_n": int((gini.transfer_share_pct > 50).sum()),
    }

    # -- 5. Indonesia, for the close ----------------------------------------
    idn_all = load_revenue(DATA / "rev_asap.csv", YEAR_REVENUE)
    idn = idn_all.loc["IDN"]
    # Indonesia gets the same averaged treatment as the OECD field, so the comparison is like
    # for like. 2021 alone is a pandemic trough and 2022 a commodity peak; quoting either one
    # on its own would pick a side.
    idn_mean = load_total_tax_mean(DATA / "rev_asap.csv", MATCHED_WINDOW).loc["IDN"]
    idn_pit_mean = load_code_mean(DATA / "rev_asap.csv", "T_1100", MATCHED_WINDOW).loc["IDN"]
    dnk_pit_mean = load_code_mean(DATA / "rev_oecd.csv", "T_1100", MATCHED_WINDOW).loc["DNK"]
    res["indonesia"] = {
        "year": YEAR_REVENUE,
        "source": "OECD Revenue Statistics in Asia and the Pacific",
        **{k: (None if pd.isna(idn.get(k)) else round(float(idn[k]), 2)) for k in mix_cols},
        "total_tax_mean": round(float(idn_mean.total_tax_mean), 2),
        "total_tax_min": round(float(idn_mean.total_tax_min), 2),
        "total_tax_max": round(float(idn_mean.total_tax_max), 2),
        "total_tax_window": [min(MATCHED_WINDOW), max(MATCHED_WINDOW)],
        "window_note": ("Indonesia and Denmark are both averaged over the same window as every "
                        "other tax level in this file. An earlier pass used 2018 to 2021 on the "
                        "false belief that Indonesia's series started in 2018; that was a "
                        "startPeriod artefact in fetch_data.py, not a property of the source."),
        "years_available": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
        "denmark_personal_income_pct_gdp": round(float(rev_members.loc["DNK", "personal_income"]), 2),
        "denmark_total_tax_mean": round(float(tax_mean.loc["DNK", "total_tax_mean"]), 2),
        "personal_income_mean": round(float(idn_pit_mean["mean"]), 2),
        "denmark_personal_income_mean": round(float(dnk_pit_mean["mean"]), 2),
        "ratio_denmark_pit_to_indonesia_total_mean": round(
            float(dnk_pit_mean["mean"] / idn_mean.total_tax_mean), 2),
        "ratio_denmark_pit_to_indonesia_pit_mean": round(
            float(dnk_pit_mean["mean"] / idn_pit_mean["mean"]), 1),
        "ratio_note": ("Two different ratios and they must never be run together. Denmark's "
                       "personal income tax against Indonesia's ENTIRE tax take is one number; "
                       "against Indonesia's own personal income tax is another."),
    }

    # ---- diagnostics forced by round 1 of the fact-check -------------------
    # The poverty-reduction result is close to definitional and the post has to say so. These
    # four numbers are what make the concession credible instead of merely modest.
    red_all = out.poverty_reduction_pts
    res["poverty_reduction_is_near_definitional"] = {
        "definition": "market-income poverty rate minus disposable-income poverty rate",
        "why": ("Disposable income is market income plus transfers minus direct taxes, so the "
                "outcome IS the arithmetic output of the tax and transfer system, and the "
                "regressor is the size of that same system."),
        "tax_only_r2": multi_fit(red_all, out.total_tax_mean)["r2"],
        "market_poverty_alone_r2": multi_fit(red_all, out.PR_INC_MRKT)["r2"],
        "income_adds_once_tax_known": round(
            multi_fit(red_all, np.log(out.gdp_pc), out.total_tax_mean)["r2"]
            - multi_fit(red_all, out.total_tax_mean)["r2"], 5),
        "corr_tax_vs_market_poverty": round(float(
            out[["total_tax_mean", "PR_INC_MRKT"]].dropna().corr().iloc[0, 1]), 4),
        "counterexample": ("France collects slightly less of GDP than Denmark and removes far "
                           "more poverty, so size is correlated with redistributive output but "
                           "does not determine it."),
        "france": {"tax": round(float(out.loc["FRA", "total_tax_mean"]), 2),
                   "poverty_removed": round(float(out.loc["FRA", "poverty_reduction_pts"]), 2)},
        "denmark": {"tax": round(float(out.loc["DNK", "total_tax_mean"]), 2),
                    "poverty_removed": round(float(out.loc["DNK", "poverty_reduction_pts"]), 2)},
        "tax_vs_transfer_effect_r2": None,
        "tax_vs_tax_effect_r2": None,
    }
    gj = gini.join(out[["total_tax_mean"]], how="inner")
    res["poverty_reduction_is_near_definitional"]["tax_vs_transfer_effect_r2"] = \
        multi_fit(gj.transfer_effect, gj.total_tax_mean)["r2"]
    res["poverty_reduction_is_near_definitional"]["tax_vs_tax_effect_r2"] = \
        multi_fit(gj.tax_effect, gj.total_tax_mean)["r2"]

    # The post uses the drop-the-five-poorest test to kill the tax-longevity story. Applying the
    # SAME test to the income-longevity story is only fair, and it roughly halves that too.
    rich = out.drop(index=POORER, errors="ignore")
    res["income_longevity_under_the_same_test"] = {
        "note": ("The post's own exclusion rule applied to the income story rather than only to "
                 "the tax story. Reporting one and not the other would be a double standard."),
        "all_oecd_r2": multi_fit(out.life_expectancy, np.log(out.gdp_pc))["r2"],
        "excl_five_lowest_r2": multi_fit(rich.life_expectancy, np.log(rich.gdp_pc))["r2"],
    }

    # The five-country convergence is a property of the five chosen. Say by how much.
    alts = {}
    for swap, repl in [("FRA", "NOR"), ("FRA", "ISL"), ("DEU", "USA")]:
        codes = [c if c != swap else repl for c in CONVERGE]
        sub = lab.loc[codes]
        alts[f"{swap}->{repl}"] = round(float(sub.labour_taxes.max() - sub.labour_taxes.min()), 2)
    nordics = lab.loc[[c for c in NORDIC if c in lab.index]]
    res["labour_tax_convergence"]["selection_sensitivity"] = {
        "note": ("The 1.56-point spread is a property of these five countries. Swapping any of "
                 "them widens it sharply, and the post must present the five as a chosen "
                 "comparison rather than as a general result."),
        "alternatives": alts,
        "five_nordics_spread": round(float(nordics.labour_taxes.max() - nordics.labour_taxes.min()), 2),
        "all_oecd_pit_ratio": round(float(
            rev_members.personal_income.max() / rev_members.personal_income.min()), 2),
    }

    # Denmark's 2021 to 2022 fall, decomposed rather than blamed on one tax.
    def _series(code, area="DNK"):
        keep = []
        for chunk in pd.read_csv(DATA / "rev_oecd.csv", low_memory=False, chunksize=300_000):
            sl = chunk[(chunk.UNIT_MEASURE == "PT_B1GQ") & (chunk.SECTOR == "S13")
                       & (chunk.REF_AREA == area) & (chunk.STANDARD_REVENUE == code)
                       & (chunk.TIME_PERIOD.isin([2021, 2022]))]
            keep.append(sl[["TIME_PERIOD", "OBS_VALUE"]])
        return pd.concat(keep).set_index("TIME_PERIOD").OBS_VALUE
    dnk_tot, dnk_t13 = _series("_T"), _series("T_1300")
    fall = float(dnk_tot[2021] - dnk_tot[2022])
    t13_fall = float(dnk_t13[2021] - dnk_t13[2022])
    res["denmark_2022_fall"] = {
        "total_2021": round(float(dnk_tot[2021]), 3), "total_2022": round(float(dnk_tot[2022]), 3),
        "fall_pts": round(fall, 3),
        "pension_yield_tax_fall_pts": round(t13_fall, 3),
        "pension_yield_share_of_fall_pct": round(100 * t13_fall / fall, 1),
        "note": ("The pension yield tax, which sits in the unallocable income tax category and "
                 "follows investment returns, accounts for the share above. The rest is mostly "
                 "the denominator: nominal GDP grew while revenue in kroner did not. The two "
                 "channels are not additive shares of one decomposition, so the post says the "
                 "pension tax accounts for about a third and the denominator does most of the "
                 "rest, rather than quoting two percentages that sum past 100."),
    }

    # The draft asserts there is essentially no relationship between how much a country collects
    # and where its top bracket starts. Round 2 required that be reproducible, with n and both
    # samples, because it flips sign on the full field. Note "where", not "how low": the regressor
    # is threshold_x_avg_wage, on which a HIGH value means the bracket starts HIGH, so pairing a
    # negative r with "how low" inverts the sign. Round 4 caught that wording shipped in README.md.
    th_join = th[["threshold_x_avg_wage"]].join(tax_mean[["total_tax_mean"]], how="inner")
    th_join = th_join[th_join.threshold_x_avg_wage > 0]
    th_rich = th_join.drop(index=POORER, errors="ignore")
    res["threshold_vs_tax_level"] = {
        "note": ("Does collecting more require starting the top bracket lower? Across the rich "
                 "members, no. Across the full field the relationship is negative, but it is "
                 "carried by the same five low-income members the post excludes elsewhere, so "
                 "quoting only the full-field figure would be the double standard this post "
                 "criticises."),
        "all_members": fit(th_join.total_tax_mean, th_join.threshold_x_avg_wage),
        "rich_members": fit(th_rich.total_tax_mean, th_rich.threshold_x_avg_wage),
    }

    # "Almost entirely" needed a decomposition, not a ratio of two R-squareds.
    gj2 = gini.join(out[["total_tax_mean"]], how="inner")
    cov_tr = float(np.cov(gj2.total_tax_mean, gj2.transfer_effect)[0, 1])
    cov_tx = float(np.cov(gj2.total_tax_mean, gj2.tax_effect)[0, 1])
    res["redistribution"]["covariance_split"] = {
        "note": ("How the association between the tax level and total Gini reduction divides "
                 "between the transfer step and the tax step. A ratio of two R-squareds does "
                 "not decompose an association; this does."),
        "transfer_share_of_covariance_pct": round(100 * cov_tr / (cov_tr + cov_tx), 1),
        "n": int(len(gj2)),
    }

    # Denmark's lead over France depends on the window. Disclose it.
    alt_mean = load_total_tax_mean(DATA / "rev_oecd.csv", [2018, 2019, 2020, 2021, 2022])
    res["window_sensitivity"] = {
        "note": "Denmark ranks first on either window, but its margin over France is not robust.",
        "window_2017_2021": {"DNK": round(float(tax_mean.loc["DNK", "total_tax_mean"]), 2),
                             "FRA": round(float(tax_mean.loc["FRA", "total_tax_mean"]), 2)},
        "window_2018_2022": {"DNK": round(float(alt_mean.loc["DNK", "total_tax_mean"]), 2),
                             "FRA": round(float(alt_mean.loc["FRA", "total_tax_mean"]), 2)},
        # Emit the margins from the unrounded values. Differencing the 2-dp fields above gives
        # 0.06 where the true margin is 0.054, which is the same double-rounding defect round 1
        # found in the chart-2 labels.
        "margin_2017_2021_pts": round(float(
            tax_mean.loc["DNK", "total_tax_mean"] - tax_mean.loc["FRA", "total_tax_mean"]), 2),
        "margin_2018_2022_pts": round(float(
            alt_mean.loc["DNK", "total_tax_mean"] - alt_mean.loc["FRA", "total_tax_mean"]), 2),
    }

    # Three-decimal fields so chart labels never round twice.
    res["tax_mix_raw3"] = {
        c: {k: (None if pd.isna(rev_members.loc[c, k]) else round(float(rev_members.loc[c, k]), 3))
            for k in ["total", "personal_income", "social_contributions", "payroll", "vat",
                      "other_goods_services", "corporate_income", "property", "residual"]}
        for c in rev_members.index
    }

    (HERE / "results.json").write_text(json.dumps(res, indent=2))

    # -- console summary -----------------------------------------------------
    print(f"OECD members in threshold file: {len(oecd_members)}")
    print(f"\nThreshold as factor of average wage, {YEAR_THRESHOLD}, lowest 12:")
    for row in res["thresholds"][:12]:
        print(f"  {row['rank']:2d}. {row['country'][:20]:20s} {row['threshold_x_avg_wage']:6.2f}"
              f"   top rate {row['top_rate_pct']}")
    print(f"\nNordic spread: {res['nordics_are_not_a_bloc']['spread']}")
    print(f"At or below Denmark: {[r['country'] for r in res['at_or_below_denmark']]}")

    print(f"\nLabour tax correction, {YEAR_REVENUE} (percent of GDP):")
    print(f"  {'country':16s} {'PIT':>6s} {'SSC':>6s} {'payroll':>8s} {'LABOUR':>7s} {'TOTAL':>7s}")
    for r in res["labour_tax_correction"]["by_country"]:
        print(f"  {r['country'][:16]:16s} {r['personal_income']:6.1f} {r['social_contributions']:6.1f}"
              f" {r['payroll']:8.1f} {r['labour_taxes_combined']:7.1f} {r['total']:7.1f}")

    print("\nWhat the revenue buys (fits across the OECD field):")
    for k, v in res["outcome_fits"].items():
        if isinstance(v, dict):
            print(f"  {k:32s} n={v['n']:3d}  r={v['r']:+.3f}  R2={v['r2']:.3f}")

    ic = res["income_control"]["outcomes"]
    print("\nIncome control (no cutoff needed). R-squared on the full OECD field:")
    print(f"  {'outcome':24s} {'tax only':>9s} {'income':>8s} {'inc+tax':>9s} {'tax adds':>9s}")
    for k, v in ic.items():
        print(f"  {k:24s} {v['tax_only_r2']:9.3f} {v['income_only_r2']:8.3f} "
              f"{v['income_plus_tax_r2']:9.3f} {v['increment_from_tax']:+9.3f}")
    pr = res["poorer_rule"]
    print(f"\nExcluded by rule ({pr['rule'][:60]}...):")
    print("  " + ", ".join(f"{e['code']} {e['gdp_pc']:,}" for e in pr["excluded"]))
    print(f"  next in line: {pr['next_in_line']['code']} {pr['next_in_line']['gdp_pc']:,}"
          f" | OECD median {pr['oecd_median_gdp_pc']:,}")

    print("\nRobustness of those fits (R-squared):")
    print(f"  {'subset':24s} {'life exp':>10s} {'poverty':>10s} {'pov reduc':>10s}   n")
    for name, f in res["outcome_robustness"]["fits"].items():
        le, pv, pr = f["tax_vs_life_expectancy"], f["tax_vs_poverty_disposable"], f["tax_vs_poverty_reduction_pts"]
        print(f"  {name:24s} {le['r2']:10.3f} {pv['r2']:10.3f} {pr['r2']:10.3f}   {le['n']}")

    rd = res["redistribution"]
    print(f"\nRedistribution, {rd['n_countries']} countries."
          f" Median transfer share of total equalising: {rd['transfer_share_median_pct']}%"
          f"  ({rd['transfer_share_gt_50_n']} of {rd['n_countries']} above 50%)")
    for r in rd["by_country"][:8]:
        print(f"  {r['country'][:16]:16s} {r['year']}  market {r['gini_market']:.3f}"
              f" -> gross {r['gini_gross']:.3f} -> disp {r['gini_disposable']:.3f}"
              f"   transfers {r['transfer_share_pct']:.0f}% of the work")

    cv = res["labour_tax_convergence"]
    print(f"\nLabour tax convergence, {YEAR_REVENUE}. {', '.join(cv['countries'])}:")
    print(f"  personal income tax ranges {cv['personal_income_range'][0]} to "
          f"{cv['personal_income_range'][1]} pct of GDP, a factor of {cv['personal_income_ratio']}")
    print(f"  ALL labour taxes together range {cv['combined_range'][0]} to "
          f"{cv['combined_range'][1]}, a spread of {cv['combined_spread_pts']} points")

    i = res["indonesia"]
    print(f"\nIndonesia: total tax {i['total_tax_mean']}% of GDP averaged over "
          f"{i['total_tax_window'][0]} to {i['total_tax_window'][1]} "
          f"(range {i['total_tax_min']} to {i['total_tax_max']}), "
          f"personal income tax {i['personal_income_mean']}% on the same window")
    print(f"  Denmark: personal income tax alone {i['denmark_personal_income_mean']}% of GDP, "
          f"= {i['ratio_denmark_pit_to_indonesia_total_mean']}x Indonesia's entire tax take "
          f"and {i['ratio_denmark_pit_to_indonesia_pit_mean']}x Indonesia's own personal income tax")
    print("  (all four figures on the same averaged window, so the ratios cannot move with the year)")

    print("\nwrote results.json")


if __name__ == "__main__":
    main()
