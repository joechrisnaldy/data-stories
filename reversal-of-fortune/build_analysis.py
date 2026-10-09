"""Compute every number quoted in Post 25 and write results.json.

Nothing in the draft may be a figure recalled from memory. Run:  python3 build_analysis.py

Sources, all open and downloadable without registration:
  World Bank API            GDP per capita, PPP, constant 2021 international dollars
  World Bank Climate Portal ERA5 near-surface air temperature, 1991-2020 annual mean
  Acemoglu, Johnson and Robinson replication files, "Reversal of Fortune", tables 3 and 5

WITHDRAWN and never to be used: AJR's temp1..temp5. Round 1 withdrew them as "undocumented" and
round 2 refuted that reason: the QJE's Appendix 2 (Appendix Table A1 in NBER w8460) defines them,
citing Parker (1997). They stay withdrawn on the sanity check computed in temp1_sanity() below:
33 distinct integers, the United States at 27 C and Greenland at 26, r=0.58 against ERA5.
All temperature here is ERA5.
"""

import hashlib
import json
import math
import os
import re

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
GDP_YEAR = 2023

# World Bank aggregate codes returned by the /indicator endpoint alongside real countries.
WB_AGGREGATES = {
    "AFE", "AFW", "ARB", "CEB", "CSS", "EAP", "EAR", "EAS", "ECA", "ECS", "EMU", "EUU", "FCS",
    "HIC", "HPC", "IBD", "IBT", "IDA", "IDB", "IDX", "LAC", "LCN", "LDC", "LIC", "LMC", "LMY",
    "LTE", "MEA", "MIC", "MNA", "NAC", "OED", "OSS", "PRE", "PSS", "PST", "SAS", "SSA", "SSF",
    "SST", "TEA", "TEC", "TLA", "TMN", "TSA", "TSS", "UMC", "WLD",
}

# Country codes mapped so the joins find these places (fact-check of 2026-10-09).
AJR_CODE_FIXES = {"ROM": "ROU", "ZAR": "COD", "WBG": "PSE"}
TAS_CODE_FIXES = {"KSV": "XKX"}
AJR_DEFUNCT = {"ANT", "YUG"}   # Netherlands Antilles and Yugoslavia


def read_gdp():
    d = json.load(open(os.path.join(DATA, f"wb_gdp_{GDP_YEAR}.json")))[1]
    gdp = {r["countryiso3code"]: r["value"] for r in d
           if r["value"] and r["countryiso3code"] and r["countryiso3code"] not in WB_AGGREGATES}
    assert not (set(gdp) & WB_AGGREGATES), sorted(set(gdp) & WB_AGGREGATES)
    return gdp


def read_tas():
    raw = json.load(open(os.path.join(DATA, "cckp_tas.json")))["data"]
    return {TAS_CODE_FIXES.get(k, k): list(v.values())[0] for k, v in raw.items() if v}


def read_ajr(table: int):
    """One AJR table: ISO3-shaped codes only, legacy codes mapped to the ones the other sources use."""
    t = pd.read_stata(os.path.join(DATA, f"ajr_t{table}/maketable{table}.dta"))
    t = t[t.shortnam.notna() & t.shortnam.str.fullmatch(r"[A-Z]{3}")].copy()
    t["shortnam"] = t.shortnam.replace(AJR_CODE_FIXES)
    return t


# The exact request that produced data/cckp_tas.json. Recorded because round 1 found the series
# could not be regenerated from this repository: the URL lived only in a shell command.
CCKP_REQUEST = ("https://cckpapi.worldbank.org/cckp/v1/era5-x0.25_climatology_tas_climatology_"
                "annual_1991-2020_mean_historical_era5_x0.25_mean/all_countries?_format=json")


def load():
    # The /indicator endpoint carries NO region field, so the old filter on region id "NA" was dead
    # code that passed all 265 rows including World, Euro area and OECD members. Round 1 caught it.
    # Aggregates are now excluded by explicit code list, and asserted gone rather than assumed.
    gdp, tas = read_gdp(), read_tas()
    t3, t5 = read_ajr(3), read_ajr(5)
    # Keep only ISO3-shaped country codes. Both files carry 120 empty-string rows plus 33 rows whose
    # shortnam is a US state abbreviation, a bare ".", or the literal "notIndonesia" (leftovers from
    # AJR's own do-files). None carries an analysis value except ex2col=0 on the "." row, which was
    # sitting in the never-colonised group as a phantom member. Round 3 found these; the previous
    # assert here could not fail, so it never looked.
    ajr = t5[["shortnam", "lpd1500s", "lat_abst", "ex2col", "logpgp95", "africa"]].merge(
        t3[["shortnam", "sjb1500"]], on="shortnam", how="outer")
    # Keep the row with the MOST non-null fields per country, not the first. DEU, ZWE and YUG are
    # each duplicated; for DEU and ZWE the first row carries latitude but neither density nor
    # income, so drop_duplicates() silently deleted them from every correlation needing 1500 density or
    # 1995 income. Urbanisation barely moved. Caught in round 1, comment corrected in round 2.
    # The corrected 1995 former-colony figure, -0.5842 on n=91, matches to the precision AJR publish
    # in Table V Panel A, column 1 (coefficient -0.38, R-squared 0.34, n=91): sqrt(0.34) = 0.583.
    # Both .dta files carry 120 rows whose shortnam is the empty STRING, which dropna() does not
    # remove; left in, the outer merge fans them out to 14,400 blank rows. Dropped explicitly.
    ajr = ajr.dropna(subset=["shortnam"]).copy()
    ajr = ajr[ajr.shortnam.str.len() > 0].copy()
    ajr["_filled"] = ajr.notna().sum(axis=1)
    ajr = (ajr.sort_values("_filled", ascending=False, kind="stable")
              .drop_duplicates("shortnam").drop(columns="_filled"))
    assert ajr.shortnam.str.fullmatch(r"[A-Z]{3}").all(), \
        sorted(ajr.shortnam[~ajr.shortnam.str.fullmatch(r"[A-Z]{3}")])
    # Places with a density, urbanisation or 1995 income value must be in gdp or tas, bar AJR_DEFUNCT;
    # every place in gdp must be in tas.
    with_data = set(ajr[ajr[["lpd1500s", "sjb1500", "logpgp95"]].notna().any(axis=1)].shortnam)
    unmatched = sorted(with_data - set(gdp) - set(tas) - AJR_DEFUNCT)
    assert not unmatched, unmatched
    assert not (set(gdp) - set(tas)), sorted(set(gdp) - set(tas))
    ajr["gdp2023"] = ajr.shortnam.map(gdp)
    ajr["tas"] = ajr.shortnam.map(tas)
    ajr["lgdp2023"] = np.log(ajr.gdp2023)
    assert len(gdp) > 150 and len(tas) > 150, (len(gdp), len(tas))
    return gdp, tas, ajr


def _sample_id(frame) -> str:
    """Short hash of the entities a statistic was computed on, so the prose can tell two samples apart."""
    col = "shortnam" if "shortnam" in frame.columns else "iso3"
    return hashlib.sha1(",".join(sorted(frame[col].astype(str))).encode()).hexdigest()[:12]


def corr(d, x, y):
    s = d.dropna(subset=[x, y])
    if len(s) < 5:
        return None
    r = float(np.corrcoef(s[x], s[y])[0, 1])
    # two-sided t test on the correlation
    n = len(s)
    t = r * np.sqrt((n - 2) / max(1e-12, 1 - r ** 2))
    return dict(r=r, n=n, t=float(t), slope=float(np.polyfit(s[x], s[y], 1)[0]), sample=_sample_id(s))


def temp1_sanity(tas):
    """Reproduce the reason AJR's temp1 is withdrawn. Round 2 found the post quoted 0.58 from a
    hand computation that no script produced, which is the rule this repository exists to enforce."""
    t3 = pd.read_stata(os.path.join(DATA, "ajr_t3/maketable3.dta"))     # raw, for the raw counts
    t = read_ajr(3)[["shortnam", "temp1"]].dropna()
    t = t.drop_duplicates("shortnam")
    t["era5"] = t.shortnam.map(tas)
    m = t.dropna(subset=["era5"])
    return dict(n_matched=len(m), r=float(np.corrcoef(m.temp1, m.era5)[0, 1]),
                mae=float(np.abs(m.temp1 - m.era5).mean()),
                distinct_values=int(t.temp1.nunique()), rows=int(len(t)),
                rows_at_7=int((t.temp1 == 7).sum()),
                raw_distinct=int(t3.temp1.dropna().nunique()), raw_rows=int(t3.temp1.notna().sum()),
                usa=float(t[t.shortnam == "USA"].temp1.iloc[0]),
                grl=float(t[t.shortnam == "GRL"].temp1.iloc[0]),
                khm=float(t[t.shortnam == "KHM"].temp1.iloc[0]),
                n_temperature_variables=sum(1 for c in t3.columns if re.fullmatch(r"temp\d", c)))


def interact(d, x, y, g):
    """OLS of y on x, g and x*g. The gap between the two slopes is the coefficient on the product;
    its t is what the post means by 'the two differ'."""
    f = d.dropna(subset=[x, y, g])
    X = np.column_stack([np.ones(len(f)), f[x], f[g], f[x] * f[g]])
    yv = f[y].values
    beta = np.linalg.lstsq(X, yv, rcond=None)[0]
    resid = yv - X @ beta
    dof = X.shape[0] - X.shape[1]
    se = np.sqrt(np.diag(np.linalg.pinv(X.T @ X)) * (resid @ resid) / dof)
    return dict(coef=float(beta[3]), se=float(se[3]), t=float(beta[3] / se[3]),
                n=int(X.shape[0]), dof=int(dof), slope_never_colonised=float(beta[1]),
                slope_former_colonies=float(beta[1] + beta[3]), sample=_sample_id(f))


def main():
    gdp, tas, ajr = load()

    # --- the modern claim, on every country with both, not just AJR's sample
    modern = pd.DataFrame({"iso3": list(gdp)}).assign(
        gdp=lambda d: d.iso3.map(gdp), tas=lambda d: d.iso3.map(tas))
    modern["lgdp"] = np.log(modern.gdp)
    tidy = corr(modern, "tas", "lgdp")

    # --- the same heat, five centuries earlier
    heat_1500 = corr(ajr, "tas", "lpd1500s")
    heat_1500_col = corr(ajr[ajr.ex2col == 1], "tas", "lpd1500s")

    # --- the flip, on AJR's own 1995 income and on 2023 income (falsification condition 2)
    flip = {}
    for basis, xv in (("density_1500", "lpd1500s"), ("urbanisation_1500", "sjb1500")):
        for era, yv in (("income_1995", "logpgp95"), ("income_2023", "lgdp2023")):
            for grp, sub in (("all", ajr), ("former_colonies", ajr[ajr.ex2col == 1]),
                             ("never_colonised", ajr[ajr.ex2col == 0])):
                c = corr(sub, xv, yv)
                if c:
                    flip[f"{basis}|{era}|{grp}"] = c

    lat = {k: corr(ajr if k == "all" else ajr[ajr.ex2col == (1 if k == "former_colonies" else 0)],
                   "lat_abst", "lgdp2023") for k in ("all", "former_colonies", "never_colonised")}

    # Rival crude variables, all three on ONE common sample. The draft claimed latitude beat
    # temperature "on the same countries" when temperature was n=196 and latitude n=159; a
    # comparison across different samples is not a comparison. Round 2 refutation.
    common = ajr.dropna(subset=["tas", "lgdp2023", "lat_abst", "africa"])
    rivals = dict(n=len(common), sample=_sample_id(common), **{v: corr(common, v, "lgdp2023")
                                    for v in ("tas", "lat_abst", "africa")})

    # The collider measurement the post asserts at minus 0.74: latitude against colonisation.
    colonisation_vs_latitude = corr(ajr, "lat_abst", "ex2col")

    # The tidy story on RAW dollars, quoted in chart 1's footnote as a hardcoded literal.
    tidy_raw = corr(modern, "tas", "gdp")

    # Hot and rich. The draft called all seventeen "countries"; seven are territories.
    NON_SOVEREIGN = {"MAC", "BMU", "CYM", "HKG", "SXM", "PRI", "ABW"}
    hot_rich = sorted(k for k, v in gdp.items()
                      if v > 40000 and tas.get(k) is not None and tas[k] > 20)
    hot_and_rich = dict(threshold_c=20, threshold_gdp=40000, n=len(hot_rich), iso3=hot_rich,
                        n_sovereign=len([k for k in hot_rich if k not in NON_SOVEREIGN]),
                        territories=sorted(set(hot_rich) & NON_SOVEREIGN))

    # The spread inside a narrow temperature band, quoted in the opening section.
    band = modern.dropna(subset=["tas", "gdp"]).query("24 <= tas <= 28")
    spread = dict(low_c=24, high_c=28, n=len(band), min=float(band.gdp.min()),
                  max=float(band.gdp.max()), min_iso3=band.loc[band.gdp.idxmin(), "iso3"],
                  max_iso3=band.loc[band.gdp.idxmax(), "iso3"])

    # The temperature variable's own reversal. The design document pre-registered this as a GLOBAL
    # claim ("hot places were the dense ones in 1500") and computing it showed the premise was
    # wrong: globally it is negative. It is positive only inside the colonised world. Both are
    # reported so the correction is visible rather than quietly narrowed.
    heat = {}
    for grp, sub in (("all", ajr), ("former_colonies", ajr[ajr.ex2col == 1]),
                     ("never_colonised", ajr[ajr.ex2col == 0])):
        heat[grp] = dict(vs_density_1500=corr(sub, "tas", "lpd1500s"),
                         vs_income_2023=corr(sub, "tas", "lgdp2023"))

    # The heat flip among former colonies leans on its coldest members (round 1 of 2026-10-09 found
    # it): reported without Canada and without the coldest four, so the post can say how much.
    col_t = ajr[ajr.ex2col == 1].dropna(subset=["tas"])
    coldest = list(col_t.dropna(subset=["lpd1500s"]).nsmallest(4, "tas").shortnam)
    assert coldest == ["CAN", "CHL", "USA", "NZL"], coldest     # the post names these four

    def heat_without(drop):
        sub = col_t[~col_t.shortnam.isin(drop)]
        return dict(vs_density_1500=corr(sub, "tas", "lpd1500s"), vs_income_2023=corr(sub, "tas", "lgdp2023"))
    heat_robust = dict(coldest=coldest, n_coldest=len(coldest),
                       without_canada=heat_without(["CAN"]), without_coldest=heat_without(coldest))

    # The never-colonised comparison the draft quotes, on ONE sample. Round 3 found the published
    # pair (-0.21 then, -0.29 now) was two different samples, n=76 and n=85; on the 69 places with
    # both, the "now" figure collapses from -0.29 to -0.04 and neither is clear of chance. This is
    # the same defect round 2 fixed two paragraphs earlier and reintroduced here.
    nev = ajr[ajr.ex2col == 0].dropna(subset=["tas", "lpd1500s", "lgdp2023"])
    never_colonised_common = dict(n=len(nev), sample=_sample_id(nev),
                                  vs_density_1500=corr(nev, "tas", "lpd1500s"),
                                  vs_income_2023=corr(nev, "tas", "lgdp2023"))

    # Who actually reversed. Percentile within former colonies, 1500 density against income today.
    # Chosen AFTER seeing the correlations, unlike charts 1 and 3.
    col2 = ajr[ajr.ex2col == 1].dropna(subset=["lpd1500s", "gdp2023"]).copy()
    col2["dens_pct"] = col2.lpd1500s.rank(pct=True) * 100
    col2["inc_pct"] = col2.gdp2023.rank(pct=True) * 100
    col2["slide"] = (col2.dens_pct - col2.inc_pct).round(9)
    ranks = [dict(iso3=r.shortnam, density_pct=float(r.dens_pct), income_pct=float(r.inc_pct),
                  slide=float(r.slide), tas=float(r.tas) if r.tas == r.tas else None)
             for _, r in col2.sort_values(["slide", "inc_pct", "shortnam"],
                                          ascending=[False, False, True],
                                          kind="stable").iterrows()]

    # Indonesia's percentiles are computed ONCE, on the same frame the rank chart uses, so the
    # post cannot end up quoting two different numbers for one quantity. An earlier version had
    # 78.4/63.4 here from a 97-country base and 78/64 in the ranks from a 93-country base.
    indonesia = None

    if (col2.shortnam == "IDN").any():
        i = col2[col2.shortnam == "IDN"].iloc[0]
        order = [r["iso3"] for r in ranks]
        indonesia = dict(
            tas=float(i.tas), gdp2023=float(i.gdp2023), lpd1500s=float(i.lpd1500s),
            density_pct=float(i.dens_pct), income_pct=float(i.inc_pct), slide=float(i.slide),
            rank_by_slide=order.index("IDN") + 1, n_colonies=len(ranks))

    # The interaction test. The post's central claim is a Simpson's paradox: a pooled near-zero
    # hiding two opposite subgroup slopes. Two subgroup correlations do not establish that; the
    # interaction term does. Added in fact-check round 1, which pointed out the post asserted the
    # paradox without ever testing it.
    interaction = interact(ajr, "lpd1500s", "lgdp2023", "ex2col")

    # The same test on urbanisation. The draft asserts "the gap between them is [significant]" for
    # the urbanisation pair; round 2 found no computation behind it. This is that computation.
    interaction_urbanisation = interact(ajr, "sjb1500", "lgdp2023", "ex2col")

    # And on UNTRANSFORMED density. This is the honest cost of the log: the two subgroup signs stay
    # opposite, but the interaction the argument rests on stops being distinguishable from zero.
    raw = ajr.assign(pd1500=np.exp(ajr.lpd1500s))
    interaction_raw_density = interact(raw, "pd1500", "lgdp2023", "ex2col")
    flip_raw_density = {g: corr(raw[raw.ex2col == v], "pd1500", "lgdp2023")
                        for g, v in (("former_colonies", 1), ("never_colonised", 0))}

    # Robustness the post asserts. ex2col == 0 is a residual, not a curated set of untouched
    # countries; these nine are the awkward ones. If the interaction only survives their placement,
    # the post has no result. Round 2 asked the question, so the answer ships as code.
    AWKWARD = ["ABW", "ATG", "BMU", "CYM", "GNQ", "KHM", "LBR", "MLT", "PRI"]
    recoded = ajr.copy()
    recoded.loc[recoded.shortnam.isin(AWKWARD), "ex2col"] = 1.0
    robustness = dict(
        awkward_never_colonised=AWKWARD,
        recoded_as_colonies=interact(recoded, "lpd1500s", "lgdp2023", "ex2col"),
        dropped=interact(ajr[~ajr.shortnam.isin(AWKWARD)], "lpd1500s", "lgdp2023", "ex2col"))

    # The density proxy is coarse, and chart 2's footnote says so. This is the number behind it.
    tied = (ajr[(ajr.ex2col == 1)].dropna(subset=["tas", "lpd1500s"])
            .groupby("lpd1500s").shortnam.apply(list))
    biggest = max(tied, key=len)
    density_ties = dict(largest_tied_block=len(biggest), iso3=sorted(biggest),
                        n_plotted=int(heat_1500_col["n"]))

    sc = dict(
        fc1_premise_fails=bool(tidy is None or abs(tidy["r"]) < 0.2),
        fc2_reversal_is_a_vintage_artefact=bool(
            flip["density_1500|income_1995|former_colonies"]["r"] < -0.2
            and flip["density_1500|income_2023|former_colonies"]["r"] >= -0.2),
        fc3_sign_does_not_flip=bool(
            flip["density_1500|income_2023|former_colonies"]["r"]
            * flip["density_1500|income_2023|never_colonised"]["r"] > 0),
        fc2_note=("AJR published on 1995 income. Nobody in this repository had checked whether the "
                  "reversal survives 28 more years, so it is tested on 2023 income too."))

    tidy["r2_share"] = tidy["r"] ** 2                 # "about a fifth of the variation in log income"
    tidy["rest_share"] = 1 - tidy["r"] ** 2           # "which leaves four fifths somewhere else"

    # The two panels of chart 2 are different country lists; the prose says how far they overlap.
    col_dens = set(ajr[(ajr.ex2col == 1)].dropna(subset=["tas", "lpd1500s"]).shortnam)
    col_inc = set(ajr[(ajr.ex2col == 1)].dropna(subset=["tas", "lgdp2023"]).shortnam)
    heat_reversal_overlap = dict(n=len(col_dens & col_inc), only_density=sorted(col_dens - col_inc),
                                 only_income=sorted(col_inc - col_dens))

    dens = np.exp(ajr.lpd1500s.dropna())
    density_range = dict(min=float(dens.min()), max=float(dens.max()),
                         orders=int(math.floor(math.log10(dens.max() / dens.min()))))

    # "for the United States, India and Brazil it equals total land area to within two percent": round 4
    # checked this against World Bank figures fetched by hand. Now a script reproduces it.
    land = {r["countryiso3code"]: r["value"] for r in json.load(open(os.path.join(DATA, "wb_land_2020.json")))[1]}
    t5_land = pd.read_stata(os.path.join(DATA, "ajr_t5/maketable5.dta")).dropna(subset=["lland15"])
    ratios = {k: float(np.exp(t5_land[t5_land.shortnam == k].lland15.iloc[0]) / land[k]) for k in sorted(land)}
    worst = max(abs(v - 1) * 100 for v in ratios.values())
    land_area_check = dict(ratios=ratios, max_pct_off=worst, bound_pct=int(math.ceil(worst)), year=2020)

    sc["n_conditions"] = sum(1 for v in sc.values() if isinstance(v, bool))
    robustness["n_awkward"] = len(robustness["awkward_never_colonised"])

    ppp = json.load(open(os.path.join(DATA, f"wb_gdp_{GDP_YEAR}.json")))[1][0]["indicator"]["value"]
    era5 = re.search(r"climatology_annual_(\d{4})-(\d{4})", CCKP_REQUEST)

    out = dict(
        meta=dict(gdp_year=GDP_YEAR, gdp_indicator="NY.GDP.PCAP.PP.KD",
                  ppp_base_year=int(re.search(r"constant (\d{4})", ppp).group(1)),
                  era5_first_year=int(era5.group(1)), era5_last_year=int(era5.group(2)),
                  ajr_income_year=1995, years_since_ajr=GDP_YEAR - 1995,
                  n_code_fixes=len(AJR_CODE_FIXES) + len(TAS_CODE_FIXES),
                  temperature="ERA5 near-surface air temperature, 1991-2020 annual mean, "
                              "World Bank Climate Change Knowledge Portal",
                  historical="Acemoglu, Johnson and Robinson, Reversal of Fortune, tables 3 and 5",
                  withdrawn="AJR temp1..temp5, failed a sanity check as country averages; see docs/provenance-audit.md",
                  n_countries_modern=len(modern.dropna(subset=["tas", "lgdp"]))),
        tidy_story=tidy, heat_vs_1500_density=heat_1500,
        heat_vs_1500_density_colonies=heat_1500_col,
        tidy_story_raw_dollars=tidy_raw, rivals_common_sample=rivals,
        colonisation_vs_latitude=colonisation_vs_latitude,
        hot_and_rich=hot_and_rich, spread_24_28c=spread,
        flip=flip, latitude_2023=lat, heat_reversal=heat, heat_reversal_robustness=heat_robust, ranks=ranks,
        interaction=interaction, interaction_urbanisation=interaction_urbanisation,
        interaction_raw_density=interaction_raw_density, flip_raw_density=flip_raw_density,
        withdrawn_temp1_sanity_check=temp1_sanity(tas),
        robustness=robustness, density_ties=density_ties,
        never_colonised_common_sample=never_colonised_common,
        heat_reversal_overlap=heat_reversal_overlap, density_range=density_range,
        land_area_check=land_area_check,
        indonesia=indonesia, scorecard=sc)
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    print(f"modern sample: {out['meta']['n_countries_modern']} countries with temperature and GDP\n")
    print(f"1. THE TIDY STORY  temperature vs log GDP {GDP_YEAR}: "
          f"r={tidy['r']:+.3f}  n={tidy['n']}  t={tidy['t']:+.1f}")
    print(f"2. THE SAME HEAT IN 1500  temperature vs log density 1500: "
          f"r={heat_1500['r']:+.3f}  n={heat_1500['n']}  t={heat_1500['t']:+.1f}")
    print(f"   among former colonies only: r={heat_1500_col['r']:+.3f}  n={heat_1500_col['n']}")
    print("\n3. THE FLIP")
    for basis in ("density_1500", "urbanisation_1500"):
        for era in ("income_1995", "income_2023"):
            row = [f"{grp.replace('_',' '):16s} r={flip[f'{basis}|{era}|{grp}']['r']:+.3f} "
                   f"(n={flip[f'{basis}|{era}|{grp}']['n']:3d})"
                   for grp in ("all", "former_colonies", "never_colonised")
                   if f"{basis}|{era}|{grp}" in flip]
            print(f"   {basis:18s} {era:12s}  " + " | ".join(row))
    print("\n   TEMPERATURE'S OWN REVERSAL (design doc's global version was wrong):")
    for g, v in heat.items():
        a_, b_ = v["vs_density_1500"], v["vs_income_2023"]
        print(f"     {g:16s} heat vs 1500 density r={a_['r']:+.3f} (n={a_['n']:3d})   "
              f"heat vs income 2023 r={b_['r']:+.3f} (n={b_['n']:3d})")

    if indonesia:
        print(f"\n4. INDONESIA  {indonesia['density_pct']:.0f}th percentile by 1500 density, "
              f"{indonesia['income_pct']:.0f}th by income today, a {indonesia['slide']:.0f} point "
              f"slide, ranking {indonesia['rank_by_slide']} of {indonesia['n_colonies']} "
              f"({indonesia['tas']:.1f} C, ${indonesia['gdp2023']:,.0f})")
    print(f"\nINTERACTION  coef {interaction['coef']:+.4f}  t {interaction['t']:+.2f}  "
          f"n={interaction['n']}  slopes: never {interaction['slope_never_colonised']:+.3f}, "
          f"colonies {interaction['slope_former_colonies']:+.3f}")

    rv = out["rivals_common_sample"]
    print(f"\nRIVAL VARIABLES on ONE common sample of {rv['n']}:  "
          f"temperature {rv['tas']['r']:+.3f}   absolute latitude {rv['lat_abst']['r']:+.3f}   "
          f"Africa dummy {rv['africa']['r']:+.3f}")
    cl = out["colonisation_vs_latitude"]
    print(f"latitude vs colonised: r={cl['r']:+.4f} (n={cl['n']})   "
          f"hot and rich: {hot_and_rich['n']} places, {hot_and_rich['n_sovereign']} sovereign   "
          f"24-28C spread: ${spread['min']:,.0f} to ${spread['max']:,.0f}")
    iu, ir = interaction_urbanisation, interaction_raw_density
    print(f"INTERACTION urbanisation  coef {iu['coef']:+.4f}  t {iu['t']:+.2f}  n={iu['n']}")
    print(f"INTERACTION raw density   coef {ir['coef']:+.4f}  t {ir['t']:+.2f}  n={ir['n']}   "
          f"(subgroup r: colonies {flip_raw_density['former_colonies']['r']:+.3f}, "
          f"never {flip_raw_density['never_colonised']['r']:+.3f})")
    rb = robustness
    print(f"ROBUSTNESS  9 awkward never-colonised recoded as colonies: t {rb['recoded_as_colonies']['t']:+.2f}"
          f"   dropped entirely: t {rb['dropped']['t']:+.2f}")
    print(f"DENSITY TIES  largest tied block among the {density_ties['n_plotted']} plotted: "
          f"{density_ties['largest_tied_block']} countries ({', '.join(density_ties['iso3'])})")
    ts = out["withdrawn_temp1_sanity_check"]
    print(f"WITHDRAWN temp1: r={ts['r']:.4f} vs ERA5, MAE {ts['mae']:.2f} C, n={ts['n_matched']}, "
          f"{ts['distinct_values']} distinct values over {ts['rows']} matched rows "
          f"({ts['rows_at_7']} at 7), USA {ts['usa']:.0f}, GRL {ts['grl']:.0f}")
    nc = never_colonised_common
    print(f"NEVER-COLONISED on ONE sample of {nc['n']}: heat vs 1500 density "
          f"{nc['vs_density_1500']['r']:+.3f} (t {nc['vs_density_1500']['t']:+.2f}), heat vs income "
          f"{nc['vs_income_2023']['r']:+.3f} (t {nc['vs_income_2023']['t']:+.2f})")

    print("\nPRE-REGISTERED FALSIFICATION CONDITIONS")
    for k, v in sc.items():
        if isinstance(v, bool):
            print(f"  {'FIRED' if v else 'did not fire':>13s}  {k}")


if __name__ == "__main__":
    main()
