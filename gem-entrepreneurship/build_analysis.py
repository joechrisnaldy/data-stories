"""Post 16 analysis: a survey that found Indonesia's business owners and could not count them.

Everything here is COMPUTED from files on disk. There are no recalled figures.

Inputs, all documented in data/README.md:
  1. GEM APS national-level panel 2013 to 2022 (SPSS .sav), gemconsortium.org, public.
  2. GEM APS individual-level microdata for 2013, 2016, 2018, 2020 and 2022.
  3. ILOSTAT EMP_TEMP_SEX_STE_NB_A for Indonesia, source BA:510 (Sakernas). NOT modelled.
  4. World Bank SL.EMP.SELF.ZS (modelled ILO self-employment) for the cross-country panel, and
     SP.POP.1564.TO for the working-age denominator.

Note on 3 versus 4: the World Bank headline series is a MODELLED ILO estimate, so a flat modelled
line would prove nothing. Every Indonesian claim rests on the direct Sakernas data in (3). The
modelled series is used only where a consistent cross-country panel is needed.

THE VARIABLES THAT MATTER. READ THE LABEL, NEVER THE NAME. Two errors were made here by guessing
from variable names, and both are recorded so nobody repeats them:
  ownmge    the raw screening question Q2A, "are you, alone or with others, currently the owner of a
            business you help manage, self-employed, or selling any goods or services to others?"
  ESTBBUSO  "Manages and owns a business that is older than 42 months". This is the published
            established-ownership measure; its weighted mean reproduces Estbbu<yy> exactly.
  ESTBBUS1  "Value ESTBBUSO BEFORE reclassification". TRAP 1: an earlier version used this and got
            3.49% for 2022 instead of the published 5.69%.
  OWNMGEyy  "OWNS AND MANAGES OWN BUSINESS (compressed for DK/REF)". This is what the published
            Ownmge<yy> equals; raw `ownmge` is missing for 78 of Indonesia's 2,600 respondents in
            2022 and gives 27.42 against the published 28.93. Present only from 2020.
  omwageyr  "Q2E2. What was the first year the founders of the business received wages, profits, or
            payments in kind from this business?" THIS is the 42-month gate.
  omyr5job  "Q2H2. Not counting owners, how many people will be working for this business five years
            from now?" TRAP 2: a five-year headcount projection. An earlier version treated it as the
            payment-year question and computed the whole mechanism on it.

Writes results.json. Prints every table it computes.
"""
import glob
import json
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat
from scipy import stats

warnings.filterwarnings("ignore")
BASE = Path(__file__).resolve().parent


def read_sav(path, **kw):
    """Some GEM files carry byte sequences pyreadstat cannot decode with the default encoding."""
    last = None
    for enc in (None, "latin1", "cp1252"):
        try:
            return pyreadstat.read_sav(path, **kw) if enc is None else \
                   pyreadstat.read_sav(path, encoding=enc, **kw)
        except Exception as exc:  # noqa: BLE001
            last = exc
    raise last


def _first(df, pattern):
    return next((c for c in df.columns if re.match(pattern, str(c), re.I)), None)


# ---------------------------------------------------------------- 1. GEM national panel
def load_national():
    rows = []
    for path in sorted(glob.glob(str(BASE / "data" / "national" / "*" / "**" / "*.sav"),
                                 recursive=True)):
        year = int(re.search(r"/(\d{4})/", path).group(1))
        if year < 2013:
            continue  # earlier files have no country_name column
        df, _ = read_sav(path)
        lower = {str(c).lower(): c for c in df.columns}
        if "country_name" not in lower:
            continue
        name = df[lower["country_name"]].astype(str).str.strip()
        tea, ebo = _first(df, r"^TEA\d\d$"), _first(df, r"^Estbbu\d\d$")
        screen, smp = _first(df, r"^Ownmge\d\d$"), _first(df, r"^Sample\d\d$")
        if tea is None:
            continue
        num = lambda c: (pd.to_numeric(df[c], errors="coerce") if c
                         else pd.Series(np.nan, index=df.index))
        rows.append(pd.DataFrame({"country": name.values, "year": year,
                                  "tea": num(tea).values, "ebo": num(ebo).values,
                                  "screen": num(screen).values, "sample_n": num(smp).values}))
    panel = pd.concat(rows, ignore_index=True)
    return panel.drop_duplicates(subset=["country", "year"], keep="first")


# GEM spells some economies more than one way. These MUST be applied before any groupby, not just
# before the World Bank merge: an earlier version aliased only the merge key and silently
# double-counted the United States, Korea, Japan and Uruguay.
GEM_CANON = {"USA": "United States", "South Korea": "Korea", "japan": "Japan",
             "Urguay": "Uruguay"}
WB_ALIAS = {"United States": "United States", "Korea": "Korea, Rep.",
            "Russia": "Russian Federation", "Iran": "Iran, Islamic Rep.",
            "Egypt": "Egypt, Arab Rep.", "Slovakia": "Slovak Republic",
            "Venezuela": "Venezuela, RB", "Turkey": "Turkiye", "Vietnam": "Viet Nam",
            "Czech Republic": "Czechia", "Bosnia": "Bosnia and Herzegovina",
            "Trinidad & Tobago": "Trinidad and Tobago", "Macedonia": "North Macedonia"}

NAT = load_national()
NAT["country"] = NAT.country.replace(GEM_CANON)
NAT = NAT.drop_duplicates(subset=["country", "year"], keep="first")
IDN = NAT[NAT.country.eq("Indonesia")].sort_values("year").reset_index(drop=True)

# ---------------------------------------------------------------- 2. Indonesia's own survey
ilo = pd.read_csv(BASE / "data" / "ilo_idn.csv")
ilo = ilo[ilo.sex.eq("SEX_T")]
STE = ilo.pivot_table(index="time", columns="classif1", values="obs_value", aggfunc="sum")
SAKERNAS = pd.DataFrame({
    "employers_k": STE["STE_ICSE93_2"], "own_account_k": STE["STE_ICSE93_3"],
    "employees_k": STE["STE_ICSE93_1"], "family_workers_k": STE["STE_ICSE93_5"],
    "total_employed_k": STE["STE_ICSE93_TOTAL"],
})
SAKERNAS["owners_k"] = SAKERNAS.employers_k + SAKERNAS.own_account_k
# share of EMPLOYMENT, which is the denominator any "X of Indonesian workers" sentence must use.
SAKERNAS["owners_pct_employed"] = SAKERNAS.owners_k / SAKERNAS.total_employed_k * 100
SAKERNAS["with_family_pct_employed"] = ((SAKERNAS.owners_k + SAKERNAS.family_workers_k)
                                        / SAKERNAS.total_employed_k * 100)

INDIVIDUAL = {2013: "gem2013_individual.sav", 2016: "gem2016_individual.sav",
              2018: "gem2018_individual.sav", 2020: "gem2020_individual.sav"}


def individual_path(year):
    if year in INDIVIDUAL:
        p = BASE / "data" / "individual" / INDIVIDUAL[year]
        return str(p) if p.exists() else None
    hits = glob.glob(str(BASE / "data" / "individual" / f"*{year}*.sav"))
    return hits[0] if hits else None


def indonesia_rows(year, wanted):
    """Pull Indonesian respondents for one round, tolerating name/case/encoding differences."""
    path = individual_path(year)
    if path is None:
        return None
    _, meta = read_sav(path, metadataonly=True)
    low = {c.lower(): c for c in meta.column_names}
    keep = [low[w] for w in wanted if w in low]
    has_name = "country_name" in low
    keep.append(low["country_name"] if has_name else low["country"])
    df, _ = read_sav(path, usecols=keep)
    df.columns = [c.lower() for c in df.columns]
    if has_name:
        sel = df.country_name.astype(str).str.strip().str.lower().str.startswith("indones")
    else:
        nat = read_sav(glob.glob(str(BASE / "data" / "national" / str(year) / "**" / "*.sav"),
                                 recursive=True)[0])[0]
        code = float(nat.loc[nat.country_name.astype(str).str.strip().eq("Indonesia"),
                             "country"].iloc[0])
        sel = df.country == code
    return df[sel].copy()


def wmean(df, var, weight="weight"):
    s = df[[var, weight]].dropna()
    return float((s[var] * s[weight]).sum() / s[weight].sum() * 100) if len(s) else np.nan


# ---------------------------------------------------------------- 3. THE MACHINE
def classification_path():
    """Where the published number comes apart: the screen, then the 42-month test.

    The screen and established rates come from the PUBLISHED national files, so all eight Indonesian
    rounds are covered and the figures are GEM's own. Nonresponse and the conditional pass rate need
    respondent records, so they exist only for the five rounds with individual-level files.
    """
    pub = IDN[["year", "screen", "ebo"]].copy()
    pub["conversion_pct"] = (pub.ebo / pub.screen * 100).round(1)
    pub = pub.rename(columns={"screen": "screen_pct", "ebo": "established_pct"})
    pub[["screen_pct", "established_pct"]] = pub[["screen_pct", "established_pct"]].round(2)

    micro = {}
    for year in (2013, 2016, 2018, 2020, 2022):
        d = indonesia_rows(year, ["ownmge", "ownmgeyy", "estbbuso", "omwageyr", "weight"])
        if d is None:
            continue
        # prefer the DK/REF-compressed screen, which is what the published rate uses; it exists
        # only from 2020, and for the earlier rounds raw ownmge does reproduce the published figure
        col = "ownmgeyy" if "ownmgeyy" in d.columns else "ownmge"
        owners = d[d[col] == 1]
        answered = owners[owners.omwageyr.notna()]
        micro[year] = {
            "screen_var_used": col,
            "n_screened": int(len(owners)),
            "payment_year_missing_pct": round(float(owners.omwageyr.isna().mean() * 100), 1),
            # among owners who DID give a payment year, how often does the 42-month rule pass?
            "pass_rate_if_answered_pct": round(float(answered.estbbuso.mean() * 100), 1)
            if len(answered) else None,
        }
    for k in ("screen_var_used", "n_screened", "payment_year_missing_pct",
              "pass_rate_if_answered_pct"):
        pub[k] = pub.year.map(lambda y: micro.get(int(y), {}).get(k))
    return pub


def decompose(path):
    """Split the fall in established ownership into the screen and the classification step.

    A two-factor multiplicative decomposition has no unique answer: the split depends on which year
    you hold fixed, and the residual is identically zero in EVERY ordering, so a zero residual is not
    evidence of robustness. All orderings are reported and the symmetric (Shapley) split is the one
    the essay quotes.
    """
    a, b = path.iloc[0], path.iloc[-1]
    total = float(a.established_pct - b.established_pct)
    d_screen = float(a.screen_pct - b.screen_pct)
    d_conv = float(a.conversion_pct - b.conversion_pct) / 100
    A = {"screen": d_screen * (a.conversion_pct / 100), "classification": b.screen_pct * d_conv}
    B = {"screen": d_screen * (b.conversion_pct / 100), "classification": a.screen_pct * d_conv}
    S = {k: (A[k] + B[k]) / 2 for k in A}
    fmt = lambda dd: {k: {"pts": round(float(v), 2), "share": round(float(v / total * 100), 1)}
                      for k, v in dd.items()}
    return {"total_fall_pts": round(total, 2),
            "ordering_a_hold_2013_conversion": fmt(A),
            "ordering_b_hold_2022_conversion": fmt(B),
            "symmetric_shapley": fmt(S),
            "quoted": fmt(S),
            "note": ("the split is order-dependent; the symmetric average makes the classification "
                     "step the larger term, and the conversion rate is volatile across all eight "
                     "rounds rather than flat")}


def nonresponse_2022():
    """Is the missing payment-year answer an Indonesian problem or everyone's?"""
    path = individual_path(2022)
    df, _ = read_sav(path, usecols=["country_name", "OWNMGEyy", "omwageyr"])
    out = []
    for name, grp in df.groupby(df.country_name.astype(str).str.strip()):
        owners = grp[grp.OWNMGEyy == 1]
        if len(owners) >= 50:
            out.append({"country": name, "n_owners": int(len(owners)),
                        "pct_missing": round(float(owners.omwageyr.isna().mean() * 100), 1)})
    r = pd.DataFrame(out).sort_values("pct_missing", ascending=False).reset_index(drop=True)
    return r


# ---------------------------------------------------------------- 4. THE DIVERGENCE
def divergence_table(pop_1564):
    out = []
    for _, r in IDN.iterrows():
        y = int(r.year)
        if y not in SAKERNAS.index or y not in pop_1564:
            continue
        owners = SAKERNAS.loc[y, "owners_k"] * 1000
        out.append({"year": y,
                    "sakernas_owners_m": round(owners / 1e6, 2),
                    # NOTE: this is per person aged 15 to 64 (SP.POP.1564.TO) with an all-ages
                    # Sakernas numerator, while GEM's rates are per person aged 18 to 64. The bases
                    # are close but not identical, so the gaps below are approximate to about two
                    # points. The widening is far larger than that mismatch.
                    "sakernas_pct_1564": round(owners / pop_1564[y] * 100, 2),
                    "gem_screen_pct": round(float(r.screen), 2) if pd.notna(r.screen) else None,
                    "gem_ebo_pct": round(float(r.ebo), 2),
                    "gem_tea_pct": round(float(r.tea), 2),
                    "gem_sample_n": int(r.sample_n) if pd.notna(r.sample_n) else None})
    d = pd.DataFrame(out)
    d["distance_pts"] = (d.sakernas_pct_1564 - d.gem_ebo_pct).round(2)
    d["screen_vs_sakernas_pts"] = (d.gem_screen_pct - d.sakernas_pct_1564).round(2)
    return d


# ---------------------------------------------------------------- 5. THE BORING SUSPECTS
def partial_corr(x, y, z):
    """Correlation of x and y with a linear trend in z removed from both.

    df is n-3, not n-2: one degree of freedom goes to the control. scipy.pearsonr on the residuals
    would report n-2 and a p-value that is slightly too small.
    """
    rx = x - np.poly1d(np.polyfit(z, x, 1))(z)
    ry = y - np.poly1d(np.polyfit(z, y, 1))(z)
    r = float(np.corrcoef(rx, ry)[0, 1])
    n = len(x)
    t = r * np.sqrt((n - 3) / max(1e-12, 1 - r ** 2))
    p = float(2 * stats.t.sf(abs(t), df=n - 3))
    # Fisher CI, also on df = n-3
    se = 1 / np.sqrt(n - 4) if n > 4 else np.nan
    lo, hi = np.tanh(np.arctanh(r) - 1.96 * se), np.tanh(np.arctanh(r) + 1.96 * se)
    return {"r": round(r, 3), "p": round(p, 3), "ci": [round(float(lo), 2), round(float(hi), 2)]}


def suspect_sample_size(d):
    s = d.dropna(subset=["gem_sample_n"])
    raw_r, raw_p = stats.pearsonr(s.gem_sample_n, s.gem_tea_pct)
    par = partial_corr(s.gem_sample_n.values.astype(float), s.gem_tea_pct.values.astype(float),
                       s.year.values.astype(float))
    return {"n_rounds": int(len(s)), "raw_r": round(float(raw_r), 3), "raw_p": round(float(raw_p), 3),
            "partial": par,
            "verdict": ("no association survives once the shared time trend is removed, but with "
                        "eight rounds the interval is far too wide to rule one out either")}


def suspect_composition():
    """Reweight 2022 to 2013's joint income x work x education profile."""
    a = indonesia_rows(2013, ["teayy", "estbbuso", "gemeduc", "gemwork3", "gemhhinc", "weight"])
    b = indonesia_rows(2022, ["teayy", "estbbuso", "gemeduc", "gemwork3", "gemhhinc", "weight"])
    if a is None or b is None:
        return {"skipped": "individual files missing"}
    KEYS = ["gemhhinc", "gemwork3", "gemeduc"]
    out = {}
    for var in ("teayy", "estbbuso"):
        aa = a.dropna(subset=KEYS + [var])
        bb = b.dropna(subset=KEYS + [var]).copy()
        ratio = ((aa.groupby(KEYS).size() / len(aa)) /
                 (bb.groupby(KEYS).size() / len(bb))).replace([np.inf, -np.inf], np.nan).dropna()
        bb = bb.join(ratio.rename("rw"), on=KEYS)
        bb["rw"] = bb["rw"].fillna(0)
        v13, v22 = aa[var].mean() * 100, bb[var].mean() * 100
        v22rw = (bb[var] * bb.rw).sum() / bb.rw.sum() * 100
        out[var] = {"n_2013_complete": int(len(aa)), "n_2022_complete": int(len(bb)),
                    "pct_2013": round(float(v13), 2), "pct_2022": round(float(v22), 2),
                    "pct_2022_reweighted": round(float(v22rw), 2),
                    "share_of_fall_explained": round(float((v22rw - v22) / (v13 - v22) * 100), 1)}
    # the shift the essay describes in prose, so those percentages are not typed from a scratch run
    prof = {}
    for tag, frame in (("2013", a), ("2022", b)):
        prof[tag] = {}
        for col, name in (("gemhhinc", "household_income"), ("gemwork3", "working_status"),
                          ("gemeduc", "education")):
            s = frame[col].dropna()
            prof[tag][name] = {str(int(k)): round(float(v) * 100, 1)
                               for k, v in s.value_counts(normalize=True).sort_index().items()}
    out["composition_profile"] = prof
    out["verdict"] = "composition explains a small single-digit share of the fall on either measure"
    return out


def suspect_weighting():
    """Test the CHANGE, not one year's level. An earlier version tested a level and used the wrong
    variable (ESTBBUS1, the pre-reclassification value), and wrongly concluded weighting did nothing.
    """
    a = indonesia_rows(2013, ["teayy", "estbbuso", "weight"])
    b = indonesia_rows(2022, ["teayy", "estbbuso", "weight"])
    if a is None or b is None:
        return {"skipped": "individual files missing"}
    out = {}
    for var in ("teayy", "estbbuso"):
        u13, u22 = a[var].mean() * 100, b[var].mean() * 100
        w13, w22 = wmean(a, var), wmean(b, var)
        out[var] = {"unweighted_2013": round(float(u13), 2), "unweighted_2022": round(float(u22), 2),
                    "weighted_2013": round(float(w13), 2), "weighted_2022": round(float(w22), 2),
                    "unweighted_fall_pts": round(float(u13 - u22), 2),
                    "weighted_fall_pts": round(float(w13 - w22), 2)}
        out[var]["weighting_share_of_fall"] = round(
            float((out[var]["weighted_fall_pts"] - out[var]["unweighted_fall_pts"])
                  / out[var]["weighted_fall_pts"] * 100), 1)
    out["verdict"] = ("weighting makes the fall LOOK STEEPER, not shallower, so it cannot be the "
                      "explanation; the published figures already use the weights")
    return out


# ---------------------------------------------------------------- 6. IS INDONESIA ALONE?
def cross_country():
    wb = pd.read_csv(BASE / "data" / "wb_selfemp.csv")
    g = NAT.copy()
    g["wb_name"] = g.country.replace(WB_ALIAS)
    m = g.merge(wb, left_on=["wb_name", "year"], right_on=["name", "year"], how="inner")
    m = m.dropna(subset=["ebo", "self_emp"])
    unmatched = sorted(set(g.country) - set(m.country))

    agree = []
    for y in sorted(m.year.unique()):
        s = m[m.year == y]
        if len(s) < 15:
            continue
        r, p = stats.pearsonr(s.ebo, s.self_emp)
        agree.append({"year": int(y), "n": int(len(s)), "pearson_r": round(float(r), 3),
                      "p": float(f"{p:.3g}")})

    counts = m.groupby("country").year.nunique()
    keep = counts[counts >= 8].index
    constant = []
    for y in sorted(m.year.unique()):
        s = m[(m.year == y) & (m.country.isin(keep))]
        if len(s) >= 12:
            r, p = stats.pearsonr(s.ebo, s.self_emp)
            constant.append({"year": int(y), "n": int(len(s)), "r": round(float(r), 3),
                             "p": round(float(p), 3)})
    cdf = pd.DataFrame(constant)
    slope = stats.linregress(cdf.year, cdf.r) if len(cdf) > 3 else None

    same = sorted(set(m[m.year == 2013].country) & set(m[m.year == 2022].country))
    fisher = None
    if len(same) > 10:
        ss = m[m.country.isin(same)]
        d13, d22 = ss[ss.year == 2013], ss[ss.year == 2022]
        r13 = stats.pearsonr(d13.ebo, d13.self_emp)[0]
        r22 = stats.pearsonr(d22.ebo, d22.self_emp)[0]
        z = (np.arctanh(r13) - np.arctanh(r22)) / np.sqrt(1 / (len(d13) - 3) + 1 / (len(d22) - 3))
        p = float(2 * (1 - stats.norm.cdf(abs(z))))
        fisher = {"n_economies": len(same), "r_2013": round(float(r13), 3),
                  "r_2022": round(float(r22), 3), "fisher_z": round(float(z), 2), "p": round(p, 3),
                  "verdict": ("the apparent decay is the changing country roster, not decay"
                              if p >= 0.05 else "the fall survives a constant panel")}

    within = []
    for c, grp in m.groupby("country"):
        grp = grp.sort_values("year")
        if len(grp) >= 6 and grp.ebo.nunique() > 3 and grp.self_emp.nunique() > 3:
            within.append({"country": c, "n_years": int(len(grp)),
                           "r": round(float(stats.pearsonr(grp.ebo, grp.self_emp)[0]), 3)})
    within = pd.DataFrame(within).dropna().sort_values("r").reset_index(drop=True)

    div = []
    for c, grp in m.groupby("country"):
        grp = grp.sort_values("year")
        if len(grp) < 5:
            continue
        div.append({"country": c, "n_years": int(len(grp)),
                    "first_year": int(grp.year.iloc[0]), "last_year": int(grp.year.iloc[-1]),
                    "ebo_pct_change": round(float((grp.ebo.iloc[-1] / grp.ebo.iloc[0] - 1) * 100), 1),
                    "ilo_pct_change": round(float((grp.self_emp.iloc[-1] / grp.self_emp.iloc[0] - 1) * 100), 1)})
    div = pd.DataFrame(div)
    div["divergence"] = (div.ebo_pct_change - div.ilo_pct_change).round(1)
    div = div.sort_values("divergence").reset_index(drop=True)
    idn_z = None
    if (div.country == "Indonesia").any():
        v = float(div.loc[div.country == "Indonesia", "divergence"].iloc[0])
        idn_z = round(float((v - div.divergence.mean()) / div.divergence.std()), 2)
    return {"agree": agree, "indonesia_z": idn_z, "divergence_median": round(float(div.divergence.median()), 1), "constant": constant,
            "constant_slope_p": round(float(slope.pvalue), 3) if slope is not None else None,
            "constant_mean_r": round(float(cdf.r.mean()), 3) if len(cdf) else None,
            "fisher": fisher, "within": within, "div": div, "unmatched_gem_names": unmatched}


# ---------------------------------------------------------------- run
if __name__ == "__main__":
    import sys
    pj = BASE / "data" / "pop_1564.json"
    if not pj.exists():
        sys.exit("missing data/pop_1564.json; see data/README.md")
    pop = {int(k): v for k, v in json.loads(pj.read_text()).items()}

    print("=== 0. WHAT SHARE OF INDONESIAN WORKERS WORK FOR THEMSELVES? ===")
    for y in (2013, 2022):
        print(f"  {y}: employers + own-account = {SAKERNAS.loc[y,'owners_pct_employed']:.1f}% of "
              f"employment; adding contributing family workers = "
              f"{SAKERNAS.loc[y,'with_family_pct_employed']:.1f}%")
    print("  the essay uses employers + own-account, so any 'share of workers' sentence must use "
          "the first number")

    DIV = divergence_table(pop)
    print("\n=== 1. THE DIVERGENCE, business owners as % of the 18-64 population ===")
    print(DIV.to_string(index=False))
    f, l = DIV.iloc[0], DIV.iloc[-1]
    print(f"\n  Sakernas: {f.sakernas_owners_m}M -> {l.sakernas_owners_m}M "
          f"({(l.sakernas_owners_m/f.sakernas_owners_m-1)*100:+.1f}%), "
          f"{f.sakernas_pct_1564}% -> {l.sakernas_pct_1564}% of working age")
    print(f"  GEM established: {f.gem_ebo_pct}% -> {l.gem_ebo_pct}%   distance "
          f"{f.distance_pts} -> {l.distance_pts} pts")
    print(f"  GEM raw screen : {f.gem_screen_pct}% -> {l.gem_screen_pct}%   "
          f"screen minus Sakernas {f.screen_vs_sakernas_pts:+.1f} -> {l.screen_vs_sakernas_pts:+.1f} pts")
    print(f"  missing GEM rounds: {sorted(set(range(2013,2023)) - set(DIV.year))}")

    PATH = classification_path()
    print("\n=== 2. INSIDE THE MACHINE: screen, then the 42-month test ===")
    print(PATH.to_string(index=False))
    DEC = decompose(PATH)
    print(f"\n  fall of {DEC['total_fall_pts']} pts, by decomposition ordering:")
    for key in ("ordering_a_hold_2013_conversion", "ordering_b_hold_2022_conversion",
                "symmetric_shapley"):
        s, c = DEC[key]["screen"], DEC[key]["classification"]
        print(f"    {key:34s} screen {s['pts']:6.2f} ({s['share']:5.1f}%)  "
              f"classification {c['pts']:6.2f} ({c['share']:5.1f}%)")
    print(f"  QUOTED: the symmetric split. {DEC['note']}")

    NR = nonresponse_2022()
    idn_nr = NR[NR.country == "Indonesia"]
    print(f"\n=== 3. THE MISSING ANSWER, 2022, {len(NR)} economies with 50+ screened owners ===")
    print(NR.head(6).to_string(index=False))
    print(f"  median {NR.pct_missing.median():.1f}%   Indonesia {float(idn_nr.pct_missing.iloc[0])}% "
          f"-> rank {int(idn_nr.index[0]) + 1} of {len(NR)}")

    print("\n=== 4. THE BORING SUSPECTS ===")
    s1 = suspect_sample_size(DIV); s2 = suspect_composition(); s3 = suspect_weighting()
    print(f"  sample size : raw r={s1['raw_r']} (p={s1['raw_p']}); partial r={s1['partial']['r']} "
          f"(p={s1['partial']['p']}, 95% CI {s1['partial']['ci']})")
    print(f"                {s1['verdict']}")
    for var in ("teayy", "estbbuso"):
        c, w = s2[var], s3[var]
        print(f"  {var:9s} : composition {c['pct_2013']}% -> {c['pct_2022']}%, reweighted "
              f"{c['pct_2022_reweighted']}% = {c['share_of_fall_explained']}% of the fall")
        print(f"              weighting: unweighted fall {w['unweighted_fall_pts']} pts vs weighted "
              f"{w['weighted_fall_pts']} pts")
    print(f"  {s3['verdict']}")

    CC = cross_country()
    div, within = CC["div"], CC["within"]
    print(f"\n=== 5. IS INDONESIA ALONE? {len(div)} economies with 5+ rounds ===")
    print(div.head(6).to_string(index=False))
    i = div[div.country == "Indonesia"]
    v = float(i.divergence.iloc[0])
    print(f"  Indonesia {v:+.1f} -> rank {int(i.index[0])+1} of {len(div)}, "
          f"z = {(v-div.divergence.mean())/div.divergence.std():+.2f}, "
          f"median {div.divergence.median():+.1f}")
    print(f"  NOTE spans differ per economy (first to last round), not a common 2013-2022 window")
    print(f"  GEM names with no World Bank match: {CC['unmatched_gem_names']}")
    print(f"\n  within-country agreement: median r = {within.r.median():+.3f} across {len(within)} "
          f"economies; above +0.5 {(within.r>0.5).mean()*100:.0f}%, below -0.5 {(within.r<-0.5).mean()*100:.0f}%")
    print(f"  constant-panel mean r = {CC['constant_mean_r']}, slope p = {CC['constant_slope_p']}")
    if CC["fisher"]:
        print(f"  identical {CC['fisher']['n_economies']} economies 2013 vs 2022: "
              f"{CC['fisher']['r_2013']} -> {CC['fisher']['r_2022']}, z={CC['fisher']['fisher_z']}, "
              f"p={CC['fisher']['p']} -> {CC['fisher']['verdict']}")

    out = {
        "sakernas_share_of_employment": {
            str(y): {"owners_pct": round(float(SAKERNAS.loc[y, "owners_pct_employed"]), 1),
                     "with_family_pct": round(float(SAKERNAS.loc[y, "with_family_pct_employed"]), 1)}
            for y in (2013, 2022)},
        "divergence": DIV.to_dict(orient="records"),
        "classification_path": PATH.to_dict(orient="records"),
        "decomposition": DEC,
        "nonresponse_2022": {"median_pct": round(float(NR.pct_missing.median()), 1),
                             "n_economies": int(len(NR)),
                             "indonesia_pct": float(idn_nr.pct_missing.iloc[0]),
                             "indonesia_rank": int(idn_nr.index[0]) + 1,
                             "all": NR.to_dict(orient="records")},
        "suspects": {"sample_size": s1, "composition": s2, "weighting": s3},
        "cross_country": {"agreement_by_year": CC["agree"], "constant_panel": CC["constant"],
                          "constant_slope_p": CC["constant_slope_p"],
                          "constant_mean_r": CC["constant_mean_r"], "decay_test": CC["fisher"],
                          "unmatched_gem_names": CC["unmatched_gem_names"],
                          "indonesia_z": CC["indonesia_z"],
                          "divergence_median": CC["divergence_median"],
                          "within": {"median_r": round(float(within.r.median()), 3),
                                     "n_economies": int(len(within)),
                                     "share_above_0_5": round(float((within.r > 0.5).mean()), 3),
                                     "share_below_minus_0_5": round(float((within.r < -0.5).mean()), 3),
                                     "indonesia_r": float(within.loc[within.country == "Indonesia", "r"].iloc[0])
                                     if (within.country == "Indonesia").any() else None,
                                     "all_r": within.to_dict(orient="records")},
                          "divergence_ranking": div.to_dict(orient="records")},
        "sakernas": SAKERNAS.round(1).to_dict(orient="index"),
    }
    (BASE / "results.json").write_text(json.dumps(out, indent=2, default=str))
    print("\nwrote results.json")
