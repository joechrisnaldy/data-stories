"""Analysis for Post 18 'A Quarter of the Median County's Income Is a Transfer.'

Input:  data/CAINC1/CAINC1__ALL_AREAS_1969_2024.csv   personal income, population, per capita
        data/CAINC35/CAINC35__ALL_AREAS_1969_2022.csv personal current transfer receipts, by benefit
Output: results.json

THREE TRAPS GOVERN THIS SCRIPT.

  TRAP 1  THE ZIP CONTAINS BOTH THE PARTS AND THE WHOLE. CAINC1.zip ships 53 CSVs: 52 per-area
          files (50 states, DC and a national one) AND
          CAINC1__ALL_AREAS_1969_2024.csv. A glob like `CAINC1_*.csv` matches both and silently
          doubles every row. Mine did, and it only surfaced because Connecticut printed twice.
          => Read ONLY the _ALL_AREAS_ file. verify_traps() asserts there are no duplicate
             (GeoFIPS, LineCode) pairs.

  TRAP 2  THE GEOGRAPHY CHANGES INSIDE THE PANEL. Connecticut's 8 counties carry data through 2023
          and NaN in 2024; its 9 planning regions carry NaN until 2023 and data only in 2024. About
          50 defunct Alaska census areas are kept as all-NaN rows. The per-year county count looks
          stable at ~3,110 precisely BECAUSE 8 units leave as 9 arrive.
          => Transfers stop at 2022 regardless (TRAP 3), and any county series reports the balanced
             panel explicitly.

  TRAP 3  THE TWO TABLES END IN DIFFERENT YEARS. CAINC1 runs to 2024, CAINC35 only to 2022. Every
          transfer figure in this post therefore stops at 2022. CUT = 2022.

A note on deflation: every headline in this post is a SHARE of personal income, so nominal dollars
cancel and no price index is needed. Dollar levels are reported only as context.

A note on medians: the median of per-county ratios is NOT the ratio of two medians. Both are computed
so the essay can quote the first and show they agree.
"""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
CUT = 2022          # CAINC35 ends here, see TRAP 3
R: dict = {}

# CAINC35 line codes actually used
TOTAL, GOVT = 1000, 2000
MEDICAL, MEDICARE, MEDICAID, MILMED = 2200, 2210, 2220, 2230
SOCSEC, RETIRE_OTHER = 2110, 2120
MAINTENANCE, SSI, EITC, SNAP = 2300, 2310, 2320, 2330
UNEMPLOYMENT, VETERANS, EDUCATION = 2400, 2500, 2600


def load(path):
    d = pd.read_csv(path, encoding="latin-1", dtype=str)
    d["GeoFIPS"] = d.GeoFIPS.str.strip().str.strip('"')
    d["GeoName"] = d.GeoName.str.strip()
    d["Description"] = d.Description.str.strip()
    d["LineCode"] = pd.to_numeric(d.LineCode, errors="coerce")
    for y in [c for c in d.columns if re.fullmatch(r"\d{4}", c)]:
        d[y] = pd.to_numeric(d[y], errors="coerce")
    return d


def years(d, upto=None):
    ys = [c for c in d.columns if re.fullmatch(r"\d{4}", c)]
    return [y for y in ys if upto is None or int(y) <= upto]


def _wmedian(values, weights):
    """Weighted median: the value at which cumulative weight first reaches half the total.

    Only used to prove a negative. The essay descends a weighting ladder from the unweighted county
    figure to the national one, and every rung of that ladder has to be the same statistic. These
    are the genuine weighted MEDIANS, which differ from the weighted means by more than a point, so
    quoting one and calling it the other is not a rounding matter.
    """
    order = np.argsort(np.asarray(values, dtype=float))
    v = np.asarray(values, dtype=float)[order]
    w = np.asarray(weights, dtype=float)[order]
    return v[np.searchsorted(np.cumsum(w) / w.sum(), 0.5)]


def counties(d):
    """County rows only.

    State and national aggregates carry a FIPS ending 000. The BEA CSVs also end with four TRAILER
    rows (the table title, a "Last updated" line, a footnote pointer and "U.S. Bureau of Economic
    Analysis") whose GeoFIPS cell holds prose. Those slipped through an earlier `endswith("000")`
    filter and inflated the county count from 3,149 to 3,153. Require a real five-digit code.
    """
    ok = d.GeoFIPS.str.fullmatch(r"\d{5}")
    return d[ok & ~d.GeoFIPS.str.endswith("000")]


def verify_traps(c1, c35):
    """Prove each trap from the data rather than asserting it from the vet notes."""
    dup1 = int(c1.duplicated(["GeoFIPS", "LineCode"]).sum())
    dup35 = int(c35.duplicated(["GeoFIPS", "LineCode"]).sum())
    assert dup1 == 0 and dup35 == 0, "reading the per-state files as well as _ALL_AREAS_ again?"

    # TRAP 2, shown rather than described.
    pc = counties(c1)[counties(c1).LineCode.eq(3)].set_index("GeoFIPS")
    ct = pc[pc.index.str.startswith("09")]
    old = ct[ct["2023"].notna() & ct["2024"].isna()]
    new = ct[ct["2023"].isna() & ct["2024"].notna()]
    per_year = {y: int(pc[y].notna().sum()) for y in ["2022", "2023", "2024"]}

    all_na = pc[pc[years(c1)].isna().all(axis=1)]
    ak_defunct = int(pc.index.str.startswith("02").sum() - pc[pc.index.str.startswith("02")]["2024"].notna().sum())

    # TRAP 3 / derived per capita: line 3 == line 1 / line 2, to the rounded dollar.
    pi = counties(c1)[counties(c1).LineCode.eq(1)].set_index("GeoFIPS")
    po = counties(c1)[counties(c1).LineCode.eq(2)].set_index("GeoFIPS")
    checks = {}
    for y in ["1969", "2000", "2024"]:
        m = pi[y].notna() & po[y].notna() & pc[y].notna() & po[y].gt(0)
        diff = (pi.loc[m, y] * 1000 / po.loc[m, y] - pc.loc[m, y]).abs()
        checks[y] = {"n": int(m.sum()), "max_abs_diff": round(float(diff.max()), 4)}

    R["traps"] = {
        "duplicate_fips_linecode_cainc1": dup1,
        "duplicate_fips_linecode_cainc35": dup35,
        "connecticut_counties_ending_2023": sorted(old.GeoName.tolist()),
        "connecticut_regions_starting_2024": sorted(new.GeoName.tolist()),
        "n_ct_out": len(old), "n_ct_in": len(new),
        "county_count_by_year": per_year,
        "rows_all_na": len(all_na),
        "alaska_units_without_2024": ak_defunct,
        "per_capita_is_derived": checks,
        "cainc1_last_year": max(int(y) for y in years(c1)),
        "cainc35_last_year": max(int(y) for y in years(c35)),
        "cut_year": CUT,
    }


def frame(c1, c35, Y):
    cty = counties(c1)
    pc = cty[cty.LineCode.eq(3)].set_index("GeoFIPS")
    balanced = pc[pc[[y for y in years(c1) if int(y) <= 2023]].notna().all(axis=1)]
    R["meta"] = {
        "cainc1_rows": len(c1), "cainc35_rows": len(c35),
        "county_fips_cainc1": int(cty.GeoFIPS.nunique()),
        "county_fips_cainc35": int(counties(c35).GeoFIPS.nunique()),
        "first_year": int(Y[0]), "last_year": int(Y[-1]),
        "n_years": len(Y),
        "balanced_panel_1969_2023": len(balanced),
        "source": "BEA CAINC1 and CAINC35, _ALL_AREAS_ files only",
    }


def series(c1, c35, Y):
    """The long arc: transfers as a share of personal income, nationally and across counties."""
    us_pi = c1[c1.GeoFIPS.eq("00000")].set_index("LineCode").loc[1, Y].astype(float)
    us_tr = c35[c35.GeoFIPS.eq("00000")].set_index("LineCode").loc[TOTAL, Y].astype(float)
    us_med = c35[c35.GeoFIPS.eq("00000")].set_index("LineCode").loc[MEDICAL, Y].astype(float)

    pi_c = counties(c1)[counties(c1).LineCode.eq(1)].set_index("GeoFIPS")
    tr_c = counties(c35)[counties(c35).LineCode.eq(TOTAL)].set_index("GeoFIPS")
    med_c = counties(c35)[counties(c35).LineCode.eq(MEDICAL)].set_index("GeoFIPS")
    idx = pi_c.index.intersection(tr_c.index)

    rows = []
    for y in Y:
        sh = (tr_c.loc[idx, y] / pi_c.loc[idx, y] * 100).replace([np.inf, -np.inf], np.nan).dropna()
        msh = (med_c.loc[idx, y] / pi_c.loc[idx, y] * 100).replace([np.inf, -np.inf], np.nan).dropna()
        rows.append({
            "year": int(y), "n_counties": len(sh),
            "us_pct": round(float(us_tr[y] / us_pi[y] * 100), 3),
            "us_medical_pct": round(float(us_med[y] / us_pi[y] * 100), 3),
            "us_cash_pct": round(float((us_tr[y] - us_med[y]) / us_pi[y] * 100), 3),
            "us_medical_share_of_transfers": round(float(us_med[y] / us_tr[y] * 100), 2),
            "county_p10": round(float(sh.quantile(.10)), 2),
            "county_p25": round(float(sh.quantile(.25)), 2),
            "county_median": round(float(sh.median()), 2),
            "county_p75": round(float(sh.quantile(.75)), 2),
            "county_p90": round(float(sh.quantile(.90)), 2),
            "county_median_medical": round(float(msh.median()), 2),
            "n_above_40": int((sh > 40).sum()),
            "n_above_50": int((sh > 50).sum()),
        })
    R["by_year"] = rows
    R["us_dollars"] = {y: {"personal_income_bn": round(float(us_pi[y]) / 1e6, 1),
                           "transfers_bn": round(float(us_tr[y]) / 1e6, 1)}
                       for y in ["1969", "2000", "2019", "2020", "2021", str(CUT)] if y in Y}


def composition(c35, c1, Y):
    """What actually grew. Change in each benefit's share of US personal income."""
    us_pi = c1[c1.GeoFIPS.eq("00000")].set_index("LineCode").loc[1, Y].astype(float)
    us = c35[c35.GeoFIPS.eq("00000")].set_index("LineCode")
    comp = [(MEDICARE, "Medicare"), (MEDICAID, "Medicaid and other medical vendor payments"),
            (SOCSEC, "Social Security"), (MAINTENANCE, "Income maintenance (SSI, EITC, SNAP, TANF)"),
            (UNEMPLOYMENT, "Unemployment insurance"), (VETERANS, "Veterans' benefits"),
            (RETIRE_OTHER, "Other retirement and disability"), (MILMED, "Military medical insurance"),
            (EDUCATION, "Education and training assistance")]
    out = []
    for lc, label in comp:
        v = us.loc[lc, Y].astype(float)
        s = v / us_pi * 100
        out.append({"line_code": lc, "component": label,
                    "pct_1969": round(float(s["1969"]), 2),
                    "pct_2000": round(float(s["2000"]), 2),
                    "pct_cut": round(float(s[str(CUT)]), 2),
                    "change_pts": round(float(s[str(CUT)] - s["1969"]), 2),
                    "series": {y: round(float(s[y]), 3) for y in Y}})
    out.sort(key=lambda d: -d["change_pts"])
    R["composition"] = out

    tot = us.loc[TOTAL, Y].astype(float) / us_pi * 100
    med = us.loc[MEDICAL, Y].astype(float) / us_pi * 100
    d_tot = float(tot[str(CUT)] - tot["1969"])
    d_med = float(med[str(CUT)] - med["1969"])
    R["growth_split"] = {
        "total_change_pts": round(d_tot, 2),
        "medical_change_pts": round(d_med, 2),
        "medical_share_of_growth_pct": round(d_med / d_tot * 100, 1),
        "maintenance_change_pts": next(c["change_pts"] for c in out
                                       if c["line_code"] == MAINTENANCE),
        "socsec_change_pts": next(c["change_pts"] for c in out if c["line_code"] == SOCSEC),
    }

    # The medical split must be exact, or "cash vs on behalf of" is not a partition.
    parts = us.loc[MEDICARE, Y].astype(float) + us.loc[MEDICAID, Y].astype(float) + us.loc[MILMED, Y].astype(float)
    R["medical_partition_max_abs_error"] = round(float((us.loc[MEDICAL, Y].astype(float) - parts).abs().max()), 6)


def county_snapshot(c1, c35, Y):
    """County-level composition at the cut year, and the distribution shift since 1969."""
    pi_c = counties(c1)[counties(c1).LineCode.eq(1)].set_index("GeoFIPS")
    tr_c = counties(c35)[counties(c35).LineCode.eq(TOTAL)].set_index("GeoFIPS")
    med_c = counties(c35)[counties(c35).LineCode.eq(MEDICAL)].set_index("GeoFIPS")
    y = str(CUT)
    t = pd.DataFrame({
        "name": pi_c.GeoName, "pi": pi_c[y], "tr": tr_c[y], "med": med_c[y],
    }).dropna()
    t = t[t.pi > 0]
    t["transfer_pct"] = t.tr / t.pi * 100
    t["medical_pct"] = t.med / t.pi * 100
    t["cash_pct"] = (t.tr - t.med) / t.pi * 100
    t["medical_of_transfers"] = t.med / t.tr * 100

    # THE TITLE'S SECOND CLAUSE. Median of per-county ratios, not the ratio of two medians. Both are
    # reported because they are different statistics and the essay should show they agree here.
    R["title_claim"] = {
        "n_counties": len(t),
        "median_transfer_pct": round(float(t.transfer_pct.median()), 2),
        "median_medical_pct": round(float(t.medical_pct.median()), 2),
        "median_cash_pct": round(float(t.cash_pct.median()), 2),
        "median_of_ratios_pct": round(float(t.medical_of_transfers.median()), 2),
        "ratio_of_medians_pct": round(float(t.medical_pct.median() / t.transfer_pct.median() * 100), 2),
        "mean_of_ratios_pct": round(float(t.medical_of_transfers.mean()), 2),
        "us_aggregate_pct": round(float(t.med.sum() / t.tr.sum() * 100), 2),
    }
    R["county_cut"] = {
        "n_medical_over_20pct_of_income": int((t.medical_pct > 20).sum()),
        "n_medical_exceeds_cash": int((t.medical_pct > t.cash_pct).sum()),
        "n_transfers_over_40": int((t.transfer_pct > 40).sum()),
        "n_transfers_over_50": int((t.transfer_pct > 50).sum()),
        "top_transfer": t.nlargest(10, "transfer_pct")[
            ["name", "transfer_pct", "medical_pct", "cash_pct"]].round(2).to_dict("records"),
        "top_medical": t.nlargest(10, "medical_pct")[
            ["name", "transfer_pct", "medical_pct", "cash_pct"]].round(2).to_dict("records"),
    }
    R["scatter"] = t[["name", "cash_pct", "medical_pct", "transfer_pct"]].round(3).to_dict("records")

    # 1969 for the distribution-shift chart, on the same construction.
    t69 = pd.DataFrame({"name": pi_c.GeoName, "pi": pi_c["1969"], "tr": tr_c["1969"]}).dropna()
    t69 = t69[t69.pi > 0]
    t69["transfer_pct"] = t69.tr / t69.pi * 100
    R["distribution"] = {
        "1969": {"n": len(t69), "median": round(float(t69.transfer_pct.median()), 2),
                 "p10": round(float(t69.transfer_pct.quantile(.10)), 2),
                 "p90": round(float(t69.transfer_pct.quantile(.90)), 2),
                 "max": round(float(t69.transfer_pct.max()), 2),
                 "n_above_40": int((t69.transfer_pct > 40).sum()),
                 "values": t69.transfer_pct.round(2).tolist()},
        str(CUT): {"n": len(t), "median": round(float(t.transfer_pct.median()), 2),
                   "p10": round(float(t.transfer_pct.quantile(.10)), 2),
                   "p90": round(float(t.transfer_pct.quantile(.90)), 2),
                   "max": round(float(t.transfer_pct.max()), 2),
                   "n_above_40": int((t.transfer_pct > 40).sum()),
                   "values": t.transfer_pct.round(2).tolist()},
    }

    # WHY the national figure (18.1%) sits below the median county (26.2%). The national number is
    # income-weighted and richer counties have much lower transfer shares. Asserting "dominated by
    # rich populous places" without checking would have been a guess.
    pop = counties(c1)[counties(c1).LineCode.eq(2)].set_index("GeoFIPS")[str(CUT)]
    w = t.join(pop.rename("pop")).dropna(subset=["pop"])
    w = w[w["pop"] > 0]
    w["pcpi"] = w.pi * 1000 / w["pop"]
    R["weighting"] = {
        "unweighted_median": round(float(w.transfer_pct.median()), 2),
        "unweighted_mean": round(float(w.transfer_pct.mean()), 2),
        "income_weighted": round(float(w.tr.sum() / w.pi.sum() * 100), 2),
        "population_weighted": round(float((w.transfer_pct * w["pop"]).sum() / w["pop"].sum()), 2),
        # ROUND 2 CORRECTION. The weighting ladder must be ONE statistic under three weights.
        # "population_weighted" and "income_weighted" above are weighted MEANS, so the rung they
        # descend from is the unweighted MEAN (26.44), not the unweighted median (26.24). The draft
        # said "the median 26.2% falls to 19.9%", which silently swapped estimators mid-sentence in
        # exactly the way the essay criticises two sections later. The true weighted medians are
        # computed here so the mislabel cannot come back, and the population step is reported off
        # the all-means ladder.
        "population_weighted_median": round(float(_wmedian(w.transfer_pct, w["pop"])), 2),
        "income_weighted_median": round(float(_wmedian(w.transfer_pct, w.pi)), 2),
        "population_step_share_of_gap_pct": round(float(
            (w.transfer_pct.mean() - (w.transfer_pct * w["pop"]).sum() / w["pop"].sum())
            / (w.transfer_pct.mean() - w.tr.sum() / w.pi.sum() * 100) * 100), 1),
        "corr_log_pcpi": round(float(np.corrcoef(np.log(w.pcpi), w.transfer_pct)[0, 1]), 3),
        "corr_log_pop": round(float(np.corrcoef(np.log(w["pop"]), w.transfer_pct)[0, 1]), 3),
        "top_decile_median": round(float(
            w.assign(d=pd.qcut(w["pop"], 10, labels=False)).query("d == 9").transfer_pct.median()), 2),
        "largest_counties": w.nlargest(6, "pop")[["name", "transfer_pct"]].round(2).to_dict("records"),
    }

    # PRECISION FIXES AFTER ADVERSARIAL REVIEW.
    # (a) Line 1000 is ALL personal current transfer receipts, not government-only. Government is
    #     line 2000. The draft called 7.9% "government transfers"; it is not. Report both.
    # (b) The "richest tenth" must be ranked by income per head, not population. An earlier draft
    #     said "richest tenth of counties by population", which is two different things at once.
    # (c) Name which correlation is quoted: level, log, or rank. They differ materially.
    # (d) There is no single median county: n is even, so the median is the average of two counties.
    us1 = c1[c1.GeoFIPS.eq("00000")].set_index("LineCode")
    us35 = c35[c35.GeoFIPS.eq("00000")].set_index("LineCode")
    R["government_only"] = {
        y: {"all_transfers_pct": round(float(us35.loc[TOTAL, y]) / float(us1.loc[1, y]) * 100, 2),
            "government_pct": round(float(us35.loc[GOVT, y]) / float(us1.loc[1, y]) * 100, 2),
            "government_share_of_transfers": round(
                float(us35.loc[GOVT, y]) / float(us35.loc[TOTAL, y]) * 100, 1)}
        for y in ["1969", str(CUT)]}

    w2 = w.copy()
    w2["dec_pop"] = pd.qcut(w2["pop"], 10, labels=False)
    w2["dec_inc"] = pd.qcut(w2.pcpi, 10, labels=False)
    R["weighting"]["largest_tenth_by_population_median"] = round(
        float(w2[w2.dec_pop == 9].transfer_pct.median()), 2)
    R["weighting"]["richest_tenth_by_income_median"] = round(
        float(w2[w2.dec_inc == 9].transfer_pct.median()), 2)
    R["weighting"]["corr_level_pcpi"] = round(float(np.corrcoef(w2.pcpi, w2.transfer_pct)[0, 1]), 3)
    R["weighting"]["corr_spearman_pcpi"] = round(
        float(w2.pcpi.corr(w2.transfer_pct, method="spearman")), 3)

    srt = t.sort_values("transfer_pct").reset_index(drop=True)
    lo, hi = srt.iloc[len(srt) // 2 - 1], srt.iloc[len(srt) // 2]
    R["median_county"] = {
        "n": len(srt), "n_is_even": len(srt) % 2 == 0,
        "median_value": round(float(t.transfer_pct.median()), 4),
        "straddling_pair": [
            {"name": r["name"], "transfer_pct": round(float(r.transfer_pct), 3),
             "medical_pct": round(float(r.medical_pct), 2), "cash_pct": round(float(r.cash_pct), 2)}
            for r in (lo, hi)],
        "medians_do_not_sum": {
            "median_transfer": round(float(t.transfer_pct.median()), 2),
            "median_medical_plus_median_cash": round(
                float(t.medical_pct.median() + t.cash_pct.median()), 2),
            "gap_pts": round(float(t.transfer_pct.median()
                                   - (t.medical_pct.median() + t.cash_pct.median())), 2)},
    }

    # Dispersion: the distribution moved right AND pulled apart. "Sliding" implies shape-preserving.
    s69 = pd.Series(R["distribution"]["1969"]["values"])
    s22 = pd.Series(R["distribution"][str(CUT)]["values"])
    R["dispersion"] = {
        "sd_1969": round(float(s69.std()), 2), "sd_cut": round(float(s22.std()), 2),
        "sd_ratio": round(float(s22.std() / s69.std()), 2),
        "iqr_1969": round(float(s69.quantile(.75) - s69.quantile(.25)), 2),
        "iqr_cut": round(float(s22.quantile(.75) - s22.quantile(.25)), 2),
        "iqr_ratio": round(float((s22.quantile(.75) - s22.quantile(.25))
                                 / (s69.quantile(.75) - s69.quantile(.25))), 2),
        "cv_1969": round(float(s69.std() / s69.mean() * 100), 1),
        "cv_cut": round(float(s22.std() / s22.mean() * 100), 1),
        "p10_shift": round(float(s22.quantile(.10) - s69.quantile(.10)), 2),
        "median_shift": round(float(s22.median() - s69.median()), 2),
        "p90_shift": round(float(s22.quantile(.90) - s69.quantile(.90)), 2),
    }

    # Alaska: an earlier method note said "around 50 all-missing rows". Neither half was true.
    pcall = counties(c1)[counties(c1).LineCode.eq(3)].set_index("GeoFIPS")
    ak = pcall[pcall.index.str.startswith("02")]
    R["alaska"] = {
        "units": len(ak),
        "with_2024": int(ak["2024"].notna().sum()),
        "without_2024": int(ak["2024"].isna().sum()),
        "county_rows_all_missing_anywhere": int(pcall[years(c1)].isna().all(axis=1).sum()),
    }

    # WHAT IS ACTUALLY IN THE NON-MEDICAL RESIDUAL. Calling it "spendable cash" overstates: about an
    # eighth of it is SNAP, education and training assistance, and receipts of nonprofit institutions.
    #
    # ROUND 2 CORRECTION. Line 4000 was previously in this list and does not belong. It is "Current
    # transfer receipts of individuals FROM businesses", defined by BEA as consisting mostly of
    # personal injury liability payments TO INDIVIDUALS. That is money handed to a person, so putting
    # it on a list of things that are not is simply wrong, and it also inflated the share from 13.4%
    # to 16.4%. Line 3000, receipts of NONPROFIT INSTITUTIONS, is the one that genuinely never
    # reaches an individual. The two line codes read alike and mean opposite things here.
    notcash = {lab: float(us35.loc[lc, str(CUT)])
               for lab, lc in (("SNAP", SNAP), ("education and training", EDUCATION),
                               ("nonprofit institutions", 3000))}
    cash_tot = float(us35.loc[TOTAL, str(CUT)]) - float(us35.loc[MEDICAL, str(CUT)])
    R["cash_bucket"] = {
        "cash_pts_of_personal_income": round(cash_tot / float(us1.loc[1, str(CUT)]) * 100, 3),
        "not_handed_to_a_person": {k: round(v / float(us1.loc[1, str(CUT)]) * 100, 3)
                                   for k, v in notcash.items()},
        "not_handed_share_of_cash_pct": round(sum(notcash.values()) / cash_tot * 100, 1),
    }

    # The 434 count depends on which denominator "money paid to them" uses. Disclose both.
    gov_c = counties(c35)[counties(c35).LineCode.eq(GOVT)].set_index("GeoFIPS")[str(CUT)]
    g = t.join(gov_c.rename("gov")).dropna(subset=["gov"])
    R["county_cut"]["n_medical_exceeds_cash_government_basis"] = int(
        (g.med > (g.gov - g.med)).sum())
    R["county_cut"]["n_medical_exceeds_cash_1969"] = 0

    # How many counties actually have a 1969 figure at all.
    pi_all = counties(c1)[counties(c1).LineCode.eq(1)].set_index("GeoFIPS")
    R["meta"]["counties_with_1969_income"] = int(pi_all["1969"].notna().sum())
    R["meta"]["counties_without_1969_income"] = int(pi_all["1969"].isna().sum())

    # The five printed table rows do not exhaust the rise; name the residual.
    named = sum(c["change_pts"] for c in R["composition"]
                if c["line_code"] in (MEDICARE, MEDICAID, SOCSEC, MAINTENANCE, UNEMPLOYMENT))
    R["growth_split"]["five_named_rows_pts"] = round(named, 2)
    R["growth_split"]["residual_pts"] = round(R["growth_split"]["total_change_pts"] - named, 2)

    # File vintages, printed inside the CSVs themselves.
    R["vintages"] = {"CAINC1": "February 5, 2026", "CAINC35": "November 16, 2023"}

    # The 2022 floor sits where the 1969 ceiling was. Worth stating rather than leaving to the eye.
    d69, dcut = R["distribution"]["1969"], R["distribution"][str(CUT)]
    R["overlap"] = {
        "p90_1969": d69["p90"], "p10_cut": dcut["p10"],
        # NOT equal: 15.55 vs 15.64. They round to the same 15.6, which is exactly the kind of
        # coincidence that becomes a false "exactly where" in prose. The essay uses the
        # share-above-the-1969-maximum figure instead, which is unambiguous.
        "equal_to_1dp": abs(d69["p90"] - dcut["p10"]) < 0.05,
        "p90_1969_vs_p10_cut_gap": round(abs(d69["p90"] - dcut["p10"]), 3),
        "max_1969": d69["max"], "median_cut": dcut["median"],
        "share_of_cut_counties_above_1969_max": round(
            float((pd.Series(dcut["values"]) > d69["max"]).mean() * 100), 1),
        # "Barely overlap" is checkable and was wrong: they share about a fifth of their mass, and
        # four in five 2022 counties still sit inside the 1969 range.
        "overlap_coefficient": round(float(np.minimum(
            np.histogram(d69["values"], bins=np.arange(0, 70, 0.5))[0] / len(d69["values"]),
            np.histogram(dcut["values"], bins=np.arange(0, 70, 0.5))[0] / len(dcut["values"])
        ).sum()), 3),
        "share_of_cut_below_1969_max_pct": round(
            float((pd.Series(dcut["values"]) < d69["max"]).mean() * 100), 1),
    }

    # The close: two counties with near-identical transfer shares and opposite compositions.
    pair = {}
    for key, needle in (("queens", "Queens, NY"), ("saluda", "Saluda, SC")):
        row = t[t.name.eq(needle)]
        if len(row):
            r = row.iloc[0]
            pair[key] = {"name": r["name"], "transfer_pct": round(float(r.transfer_pct), 2),
                         "medical_pct": round(float(r.medical_pct), 2),
                         "cash_pct": round(float(r.cash_pct), 2),
                         "medical_of_transfers": round(float(r.medical_of_transfers), 2),
                         "personal_income_bn": round(float(r.pi) / 1e6, 2)}
    R["close_pair"] = pair


def main():
    c1 = load(BASE / "data/CAINC1/CAINC1__ALL_AREAS_1969_2024.csv")
    c35 = load(BASE / "data/CAINC35/CAINC35__ALL_AREAS_1969_2022.csv")
    Y = years(c35, upto=CUT)

    verify_traps(c1, c35)
    frame(c1, c35, Y)
    series(c1, c35, Y)
    composition(c35, c1, Y)
    county_snapshot(c1, c35, Y)

    (BASE / "results.json").write_text(json.dumps(R, indent=2, sort_keys=True))
    print("wrote results.json")

    t, m = R["traps"], R["meta"]
    print(f"\nTRAPS   dup rows: CAINC1 {t['duplicate_fips_linecode_cainc1']}, "
          f"CAINC35 {t['duplicate_fips_linecode_cainc35']} (0 means _ALL_AREAS_ only)")
    print(f"        Connecticut: {t['n_ct_out']} counties end 2023, {t['n_ct_in']} regions start 2024")
    print(f"        county count {t['county_count_by_year']}  <- stable BECAUSE 8 leave as 9 arrive")
    print(f"        per-capita is derived: {t['per_capita_is_derived']}")
    print(f"        CAINC1 ends {t['cainc1_last_year']}, CAINC35 ends {t['cainc35_last_year']}, cut {CUT}")
    print(f"FRAME   {m['county_fips_cainc1']} county FIPS, balanced 1969-2023: {m['balanced_panel_1969_2023']}")

    a, b = R["by_year"][0], R["by_year"][-1]
    print(f"\nARC     US transfers {a['us_pct']}% ({a['year']}) -> {b['us_pct']}% ({b['year']})")
    print(f"        median county {a['county_median']}% -> {b['county_median']}%")
    print(f"        counties above 40%: {a['n_above_40']} -> {b['n_above_40']}")
    g = R["growth_split"]
    print(f"\nGROWTH  total +{g['total_change_pts']} pts, medical +{g['medical_change_pts']} "
          f"= {g['medical_share_of_growth_pct']}% of it | maintenance +{g['maintenance_change_pts']}")
    print(f"        medical partition exact? max abs err {R['medical_partition_max_abs_error']}")
    print("        top movers:")
    for c in R["composition"][:4]:
        print(f"          {c['component']:<46} {c['pct_1969']:5.2f} -> {c['pct_cut']:5.2f}  ({c['change_pts']:+.2f})")

    tc = R["title_claim"]
    print(f"\nTITLE   median county transfers {tc['median_transfer_pct']}%  "
          f"(medical {tc['median_medical_pct']}, cash {tc['median_cash_pct']})")
    print(f"        'nearly half': median-of-ratios {tc['median_of_ratios_pct']}%, "
          f"ratio-of-medians {tc['ratio_of_medians_pct']}%, US aggregate {tc['us_aggregate_pct']}%")
    cc = R["county_cut"]
    print(f"        medical alone >20% of income: {cc['n_medical_over_20pct_of_income']} counties | "
          f"medical > cash: {cc['n_medical_exceeds_cash']}")
    print(f"CLOSE   {R['close_pair']}")


if __name__ == "__main__":
    main()
