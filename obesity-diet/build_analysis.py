"""Post 20 analysis: does diet explain obesity across countries?

Reads the four OWID extracts in data/, writes results.json. Every number the post
quotes has to come out of this file; nothing gets typed into prose from memory.

Three decisions made here that a reader could reasonably have made differently, so
each one is recorded in results.json rather than argued in the essay:

  1. AGE-STANDARDISED obesity, not crude. OWID's default chart is the crude estimate,
     which partly measures age structure. In 2023 Greece reads 33.3% crude against 27.2%
     standardised because its population is old; Palestine reads 33.0% against 37.2%
     because its population is young. Using crude would put demography on the y-axis.

  2. YEAR 2023, the latest year all four series overlap. The obesity series runs to
     2024 and GDP to 2025, but FAO stops at 2023, so 2023 it is.

  3. The PACIFIC CLUSTER is reported in and out, never silently. Eleven small island
     states move the income R2 from 0.072 to 0.233 by themselves. Whichever number you
     quote is a choice, so both are emitted.

TRAP, and it is the one that would have quietly broken everything: the FAO files carry
52 non-country entities in the same column as countries (World, continents, "Africa
(FAO)", "Belgium-Luxembourg (FAO)"). A scatter that includes "World" has a fabricated
point in it. Filter on a real ISO3 code.

ROUND 1 CORRECTION. An earlier version of this docstring, and of the post, said Kosovo was
"a real country lost to a mechanical rule". That was false and it flattered the method: Kosovo
has ZERO rows in the obesity file and ZERO in both FAO files, so the ISO3 filter never touched
it and it could never have entered the sample. The countries genuinely lost at the join are
French Polynesia, Syria, Venezuela and Yemen, which have both an obesity and a calorie figure
for 2023 but no 2023 income figure. They are emitted below rather than described from memory.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
YEAR = 2023

# Pacific island states and territories. Eleven of these reach the 2023 panel; the rest lack
# food or income data. Reported separately because they are a genuine cluster with the highest
# obesity on earth, not because they are inconvenient: including them is what makes income look
# like it explains nothing.
#
# ROUND 3 CORRECTION. This list omitted French Polynesia (PYF) while including American Samoa,
# the Cook Islands and Niue, its immediate Polynesian neighbours. That was an accident of typing,
# not a criterion, and the draft then leaned on the gap to argue French Polynesia was "not one of
# the eleven". Adding PYF changes no statistic, because it has no income figure and never enters
# the panel, but it makes the classification answer to geography rather than to an oversight.
PACIFIC = {"NRU", "WSM", "TUV", "FSM", "TON", "KIR", "MHL", "PLW", "COK",
           "NIU", "FJI", "VUT", "SLB", "PNG", "ASM", "PYF"}

R = {}


def only_countries(d):
    """OWID mixes aggregates into the entity column. Real countries carry an ISO3 code."""
    code = d.code.astype(str)
    return d[d.code.notna() & ~code.str.startswith("OWID") & (code.str.len() == 3)]


def load():
    ob_raw = pd.read_csv(DATA / "obesity-age-standardized.csv")
    ob_col = [c for c in ob_raw.columns
              if c not in ("entity", "code", "year", "owid_region")][0]
    ob = only_countries(ob_raw).rename(columns={ob_col: "obesity"})

    ob_crude_raw = pd.read_csv(DATA / "share-of-adults-defined-as-obese.csv")
    oc_col = [c for c in ob_crude_raw.columns
              if c not in ("entity", "code", "year", "owid_region")][0]
    ob_crude = only_countries(ob_crude_raw).rename(columns={oc_col: "obesity_crude"})

    cal = only_countries(pd.read_csv(DATA / "daily-per-capita-caloric-supply.csv")
                         ).rename(columns={"daily_calories": "kcal"})
    mac = only_countries(pd.read_csv(
        DATA / "daily-caloric-supply-derived-from-carbohydrates-protein-and-fat.csv"))
    gdp = only_countries(pd.read_csv(DATA / "gdp-per-capita-worldbank.csv")
                         ).rename(columns={"ny_gdp_pcap_pp_kd": "gdp"})
    return ob, ob_crude, cal, mac, gdp


def build_panel(ob, cal, mac, gdp):
    y = lambda d: d[d.year == YEAR]
    m = (y(ob)[["entity", "code", "obesity"]]
         .merge(y(cal)[["code", "kcal"]], on="code")
         .merge(y(gdp)[["code", "gdp"]], on="code")
         .merge(y(mac).drop(columns=["entity"]), on="code")
         .dropna(subset=["obesity", "kcal", "gdp"]))

    # Shares of the SAME total. These are a decomposition of the calorie series, not an
    # independent measurement: the four components reconcile to it within 0.08 kcal.
    m["fat_share"] = m.total_energy_from_fat / m.kcal * 100
    m["animal_protein_share"] = m.energy_from_animal_protein / m.kcal * 100
    m["carb_share"] = m.total_energy_from_carbohydrates / m.kcal * 100
    m["log_gdp"] = np.log(m.gdp)
    m["is_pacific"] = m.code.isin(PACIFIC)
    return m.reset_index(drop=True)


def r2(x, y):
    r = float(np.corrcoef(x, y)[0, 1])
    return {"r": round(r, 4), "r2": round(r * r, 4), "n": int(len(x))}


def ols_r2(X, y):
    """Multiple R2 by least squares, with an intercept."""
    A = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    beta, *_ = np.linalg.lstsq(A, np.asarray(y, float), rcond=None)
    pred = A @ beta
    ss_res = float(((y - pred) ** 2).sum())
    ss_tot = float(((y - np.mean(y)) ** 2).sum())
    return round(1 - ss_res / ss_tot, 4), pred


def main():
    ob, ob_crude, cal, mac, gdp = load()

    # ---------------------------------------------------------------- measurement choice
    both = (ob[ob.year == YEAR][["entity", "code", "obesity"]]
            .merge(ob_crude[ob_crude.year == YEAR][["code", "obesity_crude"]], on="code")
            .dropna())
    both["gap"] = both.obesity_crude - both.obesity
    R["measurement"] = {
        "series_used": "age-standardised",
        "why": ("the crude estimate partly measures age structure, because obesity rises "
                "with age and populations differ in how old they are"),
        "n": int(len(both)),
        "correlation_crude_vs_standardised": round(float(both.obesity.corr(both.obesity_crude)), 4),
        "mean_gap_pts": round(float(both.gap.mean()), 2),
        "gap_range_pts": [round(float(both.gap.min()), 2), round(float(both.gap.max()), 2)],
        "crude_most_overstates": [
            {"entity": r.entity, "crude": round(r.obesity_crude, 1), "standardised": round(r.obesity, 1),
             "gap": round(r.gap, 1)} for _, r in both.nlargest(3, "gap").iterrows()],
        "crude_most_understates": [
            {"entity": r.entity, "crude": round(r.obesity_crude, 1), "standardised": round(r.obesity, 1),
             "gap": round(r.gap, 1)} for _, r in both.nsmallest(3, "gap").iterrows()],
    }

    m = build_panel(ob, cal, mac, gdp)
    nonpac = m[~m.is_pacific]

    R["meta"] = {
        "year": YEAR,
        "n_countries": int(len(m)),
        "n_pacific": int(m.is_pacific.sum()),
        "n_excluding_pacific": int(len(nonpac)),
        "obesity_source": "WHO Global Health Observatory (2026), via Our World in Data",
        "diet_source": "FAO Food Balance Sheets (2025), via Our World in Data",
        "gdp_source": "Eurostat, OECD, IMF and World Bank (2026), via Our World in Data",
    }

    # The panel rule, stated exactly, because round 1 caught the draft describing a filter it
    # did not use. Obesity AND calories alone gives 172; the income requirement is what makes
    # it 168. The macronutrient file adds no constraint at all: its 2023 coverage is identical
    # to the calorie file's.
    y = lambda d: d[d.year == YEAR]
    n_ob_cal = len(y(ob)[["code", "obesity"]].merge(y(cal)[["code", "kcal"]], on="code").dropna())
    dropped = sorted(set(y(ob).merge(y(cal)[["code"]], on="code").dropna(subset=["obesity"]).entity)
                     - set(m.entity))
    R["meta"]["sample_rule"] = {
        "requires": ["WHO age-standardised obesity", "FAO daily calorie supply",
                     "World Bank income per person"],
        "n_obesity_and_calories_only": n_ob_cal,
        "n_final": int(len(m)),
        "macronutrients_add_no_constraint": True,
        "dropped_for_missing_income": dropped,
        "note": ("the macronutrient file has the same 2023 country coverage as the calorie "
                 "file, so requiring it changes nothing; income is the binding constraint"),
    }

    # ------------------------------------------------------------------ the headline test
    R["explains"] = {}
    for label, col in (("calories", "kcal"), ("log_gdp", "log_gdp"),
                       ("fat_share", "fat_share"),
                       ("animal_protein_share", "animal_protein_share"),
                       ("carb_share", "carb_share")):
        R["explains"][label] = {
            "all": r2(m[col], m.obesity),
            "excluding_pacific": r2(nonpac[col], nonpac.obesity),
        }

    # Joint model. Reported ONLY as a joint figure: single-variable R2 values do not sum to
    # it, because calorie supply, income and diet composition are correlated with each other.
    for name, d in (("all", m), ("excluding_pacific", nonpac)):
        joint, pred = ols_r2([d.kcal, d.log_gdp, d.animal_protein_share], d.obesity)
        R["explains"].setdefault("joint_three_factor", {})[name] = {
            "r2": joint, "n": int(len(d)),
            "unexplained": round(1 - joint, 4)}
        if name == "all":
            resid = d.obesity - pred
            far = d.assign(resid=resid).reindex(resid.abs().sort_values(ascending=False).index)
            R["residuals"] = {
                "model": "obesity ~ kcal + log(gdp) + animal protein share",
                # RMSE is NOT the average miss. Round 1 caught the draft calling it that: RMSE
                # exceeds mean absolute error whenever residuals are uneven, and here a handful
                # of Pacific residuals near 40 points dominate the squares. Emit both so the
                # prose can use the one it actually means.
                "rmse_pts": round(float(np.sqrt((resid ** 2).mean())), 2),
                "mae_pts": round(float(resid.abs().mean()), 2),
                "median_abs_error_pts": round(float(resid.abs().median()), 2),
                "most_above_prediction": [
                    {"entity": r.entity, "actual": round(r.obesity, 1),
                     "predicted": round(r.obesity - r.resid, 1), "resid": round(r.resid, 1)}
                    for _, r in far[far.resid > 0].head(6).iterrows()],
                "most_below_prediction": [
                    {"entity": r.entity, "actual": round(r.obesity, 1),
                     "predicted": round(r.obesity - r.resid, 1), "resid": round(r.resid, 1)}
                    for _, r in far[far.resid < 0].head(6).iterrows()],
            }

    # ------------------------------------------------------------------------- the hook
    # A THRESHOLD, not a rank. "The five highest-calorie countries" is a hand-picked set
    # whose span moves when the fifth country changes; 3,700 kcal is a stated cut and the
    # group it selects is stable, all rich, and contains no Pacific state, so the spread
    # inside it cannot be blamed on poverty or on small-island outliers.
    HOOK_KCAL = 3700
    top = m[m.kcal >= HOOK_KCAL].sort_values("kcal", ascending=False)
    assert not top.is_pacific.any(), "hook group must contain no Pacific state"
    R["hook_high_calorie_group"] = {
        "threshold_kcal": HOOK_KCAL,
        "n": int(len(top)),
        "obesity_min_pct": round(float(top.obesity.min()), 1),
        "obesity_max_pct": round(float(top.obesity.max()), 1),
        "obesity_ratio": round(float(top.obesity.max() / top.obesity.min()), 1),
        "kcal_min": round(float(top.kcal.min()), 0),
        "kcal_max": round(float(top.kcal.max()), 0),
        "kcal_spread_pct": round(float((top.kcal.max() / top.kcal.min() - 1) * 100), 1),
        "countries": [{"entity": r.entity, "kcal": round(r.kcal, 0),
                       "obesity": round(r.obesity, 1)} for _, r in top.iterrows()],
    }

    # Near-identical calorie supply, far apart on obesity. Computed, not hand-picked.
    a = m.sort_values("kcal").reset_index(drop=True)
    pairs = []
    for i in range(len(a)):
        for k in range(i + 1, len(a)):
            if a.kcal[k] - a.kcal[i] > 30:
                break
            gap = abs(a.obesity[i] - a.obesity[k])
            if gap > 25:
                pairs.append({"a": a.entity[i], "a_kcal": round(a.kcal[i], 0),
                              "a_obesity": round(a.obesity[i], 1),
                              "b": a.entity[k], "b_kcal": round(a.kcal[k], 0),
                              "b_obesity": round(a.obesity[k], 1),
                              "kcal_apart": round(abs(a.kcal[k] - a.kcal[i]), 0),
                              "obesity_apart": round(gap, 1),
                              "either_pacific": bool(a.is_pacific[i] or a.is_pacific[k])})
    pairs.sort(key=lambda p: -p["obesity_apart"])
    R["near_identical_pairs"] = {
        "rule": "within 30 kcal of each other, more than 25 points apart on obesity",
        "n_pairs": len(pairs),
        "n_pairs_no_pacific": sum(1 for p in pairs if not p["either_pacific"]),
        "top": pairs[:6],
        "top_no_pacific": [p for p in pairs if not p["either_pacific"]][:6],
    }

    # ------------------------------------------------------------------------- context
    R["extremes"] = {
        "highest_obesity": [{"entity": r.entity, "obesity": round(r.obesity, 1),
                             "kcal": round(r.kcal, 0)}
                            for _, r in m.nlargest(6, "obesity").iterrows()],
        "lowest_obesity": [{"entity": r.entity, "obesity": round(r.obesity, 1),
                            "kcal": round(r.kcal, 0)}
                           for _, r in m.nsmallest(6, "obesity").iterrows()],
        "obesity_median_pct": round(float(m.obesity.median()), 1),
        "kcal_median": round(float(m.kcal.median()), 0),
        "kcal_range": [round(float(m.kcal.min()), 0), round(float(m.kcal.max()), 0)],
    }

    # The decomposition check: the four macronutrient components ARE the calorie total.
    chk = mac.merge(cal, on=["code", "year"])
    s = (chk.energy_from_animal_protein + chk.energy_from_vegetal_protein
         + chk.total_energy_from_fat + chk.total_energy_from_carbohydrates)
    R["composition_is_not_independent"] = {
        "max_abs_difference_kcal": round(float((s - chk.kcal).abs().max()), 3),
        "n_country_years": int(len(chk)),
        "meaning": ("the macronutrient components sum to the calorie series itself, so diet "
                    "composition is the same FAO number cut differently, not a second source"),
    }

    R["scatter"] = [{"entity": r.entity, "code": r.code, "obesity": round(r.obesity, 2),
                     "kcal": round(r.kcal, 1), "gdp": round(r.gdp, 1),
                     "animal_protein_share": round(r.animal_protein_share, 2),
                     "fat_share": round(r.fat_share, 2),
                     "carb_share": round(r.carb_share, 2),
                     "is_pacific": bool(r.is_pacific)} for _, r in m.iterrows()]

    (BASE / "results.json").write_text(json.dumps(R, indent=1))

    # ------------------------------------------------------------------------- console
    print(f"PANEL   {YEAR}: {len(m)} countries ({int(m.is_pacific.sum())} Pacific)")
    print(f"        obesity median {R['extremes']['obesity_median_pct']}%, "
          f"calories median {R['extremes']['kcal_median']:.0f}, "
          f"range {R['extremes']['kcal_range'][0]:.0f}-{R['extremes']['kcal_range'][1]:.0f}")
    print()
    print("EXPLAINS obesity variance across countries (R2)")
    print(f"        {'factor':24s} {'all':>8s} {'excl. Pacific':>14s}")
    for k, v in R["explains"].items():
        if k == "joint_three_factor":
            continue
        print(f"        {k:24s} {v['all']['r2']:>8.3f} {v['excluding_pacific']['r2']:>14.3f}")
    j = R["explains"]["joint_three_factor"]
    print(f"        {'JOINT (3 factors)':24s} {j['all']['r2']:>8.3f} "
          f"{j['excluding_pacific']['r2']:>14.3f}")
    print(f"        unexplained by all three: {j['all']['unexplained']:.1%} (all), "
          f"{j['excluding_pacific']['unexplained']:.1%} (excl. Pacific)")
    print("        single-variable R2 do NOT sum to the joint figure; the predictors overlap")
    print()
    h = R["hook_high_calorie_group"]
    print(f"HOOK    {h['n']} countries at or above {h['threshold_kcal']} kcal "
          f"(a {h['kcal_spread_pct']}% spread in supply) span "
          f"{h['obesity_min_pct']}% to {h['obesity_max_pct']}% obesity, {h['obesity_ratio']}x")
    for c in h["countries"]:
        print(f"          {c['entity']:16s} {c['kcal']:.0f} kcal  {c['obesity']:5.1f}%")
    print()
    print(f"PAIRS   {R['near_identical_pairs']['n_pairs']} pairs within 30 kcal and >25 pts apart "
          f"({R['near_identical_pairs']['n_pairs_no_pacific']} without any Pacific state)")
    for p in R["near_identical_pairs"]["top_no_pacific"][:3]:
        print(f"          {p['a']:14s} {p['a_kcal']:.0f}/{p['a_obesity']:.1f}%  vs  "
              f"{p['b']:14s} {p['b_kcal']:.0f}/{p['b_obesity']:.1f}%")
    print()
    print("CHECK   macronutrients vs calorie total: max abs difference "
          f"{R['composition_is_not_independent']['max_abs_difference_kcal']} kcal "
          f"over {R['composition_is_not_independent']['n_country_years']:,} country-years")
    print(f"        -> composition is a DECOMPOSITION, not an independent measurement")
    print()
    print(f"MEASURE crude vs age-standardised: r="
          f"{R['measurement']['correlation_crude_vs_standardised']}, "
          f"gap {R['measurement']['gap_range_pts'][0]:+.1f} to "
          f"{R['measurement']['gap_range_pts'][1]:+.1f} pts")
    print(f"wrote results.json")


if __name__ == "__main__":
    main()
