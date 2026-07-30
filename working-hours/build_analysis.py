"""Analysis for Post 17 'A Third of the World's Labour Laws Still Assume You Work Saturday'.

Input:  data/public_workingtimedata.dta  (Rasmussen Working Time Regulation Dataset)
Output: results.json

TWO CODING TRAPS GOVERN THIS ENTIRE SCRIPT. Both were found in the pre-build vet and both produce a
publishable-looking false headline if ignored.

  TRAP 1  `normalhours == 96` is a CODE FOR "NO LAW", not a measurement. It equals `workinglaw == 0`
          across all 14,824 such rows with zero exceptions. A naive mean over the raw column returns
          73.4 hours and a naive time series says the world's normal week fell from 96 to 46.
          => Every hours statistic here is computed on `workinglaw == 1` only. See LAW below.

  TRAP 2  A COVERAGE CLIFF AT 2013. Holding the same 179 countries and stepping 2012 to 2013, 70
          lose `hours_max` to missing and 62 drop from a positive overtime premium to exactly zero
          (61 of them coded as having a law), while ZERO change normal hours. The author's datasets
          page states coverage to 2014; the paper's appendix says the public dataset ends in 2010.
          => The whole analysis is cut at CUT = 2012. See `df` below.

A third quieter trap: the float32 storage turns 41.3 into 41.299999 and 67.3 into 67.300003, so raw
value_counts fragments. Hours columns are rounded to 1 decimal before any equality test. 40.0 and
48.0 are exactly representable in binary floating point, so the "exactly 40" and "exactly 48" counts
are unaffected either way.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat

BASE = Path(__file__).resolve().parent
CUT = 2012          # last year inside the author's documented coverage, see TRAP 2
NOLAW = 96.0        # the sentinel, see TRAP 1
R: dict = {}


def load():
    df, meta = pyreadstat.read_dta(BASE / "data" / "public_workingtimedata.dta")
    for c in ("normalhours", "hours_max"):
        df[c] = df[c].round(1)
    return df, meta


def verify_traps(df):
    """Prove both traps from the data rather than asserting them from the vet notes."""
    both = df[df.workinglaw.notna() & df.normalhours.notna()]
    sentinel_rows = int(both.normalhours.eq(NOLAW).sum())
    nolaw_rows = int(both.workinglaw.eq(0).sum())
    mismatch = int((both.normalhours.eq(NOLAW) != both.workinglaw.eq(0)).sum())
    assert mismatch == 0, f"sentinel is not a perfect proxy for no-law: {mismatch} mismatches"

    a = df[df.year.eq(2012)].set_index("country_name")
    b = df[df.year.eq(2013)].set_index("country_name")
    common = a.index.intersection(b.index)
    a, b = a.loc[common], b.loc[common]

    # BUG FIXED AFTER ADVERSARIAL REVIEW. Differencing the STOCK of law-havers with a zero premium
    # counts countries entering and leaving the panel as if they had changed their law. Count
    # WITHIN-COUNTRY transitions from a positive premium to exactly zero in consecutive years
    # instead. The corrected comparison is far starker: 61 countries in 2013 against at most 1 in
    # any earlier year, not the 8 the stock difference reported for 1945.
    law = df[df.workinglaw.eq(1)].sort_values(["country_name", "year"])
    law = law.assign(prev_ot=law.groupby("country_name").overtime_remun.shift(),
                     prev_yr=law.groupby("country_name").year.shift())
    drops = law[law.prev_yr.eq(law.year - 1) & law.prev_ot.gt(0) & law.overtime_remun.eq(0)]
    by_year = drops.groupby("year").size()
    jump_2013 = int(by_year.get(2013.0, 0))
    pre = by_year[by_year.index <= 2012]
    biggest_real = int(pre.max())
    biggest_real_year = int(pre.idxmax())

    R["traps"] = {
        "sentinel_value": NOLAW,
        "sentinel_rows": sentinel_rows,
        "nolaw_rows": nolaw_rows,
        "sentinel_mismatches": mismatch,
        "sentinel_share_of_file_pct": round(sentinel_rows / len(both) * 100, 1),
        "naive_mean_all_rows": round(float(both.normalhours.mean()), 1),
        "cliff_countries_compared": len(common),
        "cliff_lost_hours_max": int((a.hours_max.notna() & b.hours_max.isna()).sum()),
        "cliff_overtime_to_zero": int((a.overtime_remun.gt(0) & b.overtime_remun.eq(0)).sum()),
        # BUG FIXED AFTER ADVERSARIAL REVIEW. A bare `!=` counts NaN != NaN as a change, which
        # reported 2 countries changing their normal week across the cliff when the true number is
        # zero: both flagged rows (Sierra Leone, Somalia) are missing in BOTH years. Require both
        # values present before calling it a change.
        "cliff_normalhours_changed": int((a.normalhours.notna() & b.normalhours.notna()
                                          & (a.normalhours != b.normalhours)).sum()),
        "cliff_workinglaw_changed": int((a.workinglaw.notna() & b.workinglaw.notna()
                                         & (a.workinglaw != b.workinglaw)).sum()),
        "cliff_jump_2013": jump_2013,
        "biggest_real_jump": biggest_real,
        "biggest_real_jump_year": biggest_real_year,
        "cut_year": CUT,
    }


def naive_vs_honest(df, LAW):
    """The decomposition that shows WHY the naive series is not a finding.

    naive_mean = s * h + (1 - s) * 96, where s is the share of polities with any law and h is the
    mean statutory week among those that have one. The identity is exact, so the fall in the naive
    mean splits cleanly into a composition effect (s) and a real effect (h).

    A two-factor split is ORDERING DEPENDENT. Reporting one ordering is how you accidentally flip a
    majority. Both orderings and the symmetric (Shapley) average are reported, and the essay quotes
    the symmetric split with its range.

    BASELINE CHOICE MATTERS AND THE OBVIOUS ONE IS UNUSABLE. Anchoring at 1850 looks natural because
    that is near the start of the series, but in 1850 exactly ONE polity of 86 had a law, so
    `hours_among_law` is one country and the split ranges from 45.6% to 99.3% depending on ordering.
    That is not a finding, it is a coin flip. The baseline here is 1920, the first year with a
    broad enough set for the mean to mean anything. The 1850 levels are still reported, as levels.
    """
    y0, y1 = 1920, CUT
    out = {}
    for y in (y0, y1, 1850):
        f = df[df.year.eq(y)]
        fl = LAW[LAW.year.eq(y)]
        out[y] = {
            "share_with_law": float(f.workinglaw.mean()),
            "hours_among_law": float(fl.normalhours.mean()),
            "naive_mean": float(f.normalhours.mean()),
            "n_polities": len(f),
            "n_law": len(fl),
        }
    a, b = out[y0], out[y1]
    ds = b["share_with_law"] - a["share_with_law"]
    dh = b["hours_among_law"] - a["hours_among_law"]
    total = b["naive_mean"] - a["naive_mean"]

    # ordering A: move share first, then hours.  ordering B: the reverse.
    oa = {"composition": ds * (a["hours_among_law"] - NOLAW), "real": dh * b["share_with_law"]}
    ob = {"composition": ds * (b["hours_among_law"] - NOLAW), "real": dh * a["share_with_law"]}
    sym = {k: (oa[k] + ob[k]) / 2 for k in oa}

    R["naive_vs_honest"] = {
        "year_from": y0, "year_to": y1,
        "from": {k: round(v, 4) if isinstance(v, float) else v for k, v in a.items()},
        "to": {k: round(v, 4) if isinstance(v, float) else v for k, v in b.items()},
        "levels_1850": {k: round(v, 4) if isinstance(v, float) else v for k, v in out[1850].items()},
        "baseline_note": ("anchored at 1920, not 1850: in 1850 only one polity of 86 had a law, "
                          "which makes the split range from 45.6% to 99.3% by ordering"),
        "naive_total_change": round(total, 2),
        "honest_change_among_law": round(dh, 2),
        "ordering_a": {k: round(v, 2) for k, v in oa.items()},
        "ordering_b": {k: round(v, 2) for k, v in ob.items()},
        "symmetric": {k: round(v, 2) for k, v in sym.items()},
        "symmetric_pct": {k: round(v / total * 100, 1) for k, v in sym.items()},
        "composition_pct_range": sorted([round(oa["composition"] / total * 100, 1),
                                        round(ob["composition"] / total * 100, 1)]),
        "identity_residual": round(total - sum(sym.values()), 10),
    }


def dispersion(LAW):
    """Chart 1 and the hook: agreement peaked and reversed."""
    def stats(s):
        return dict(n=len(s), mean=float(s.mean()), sd=float(s.std()),
                    p10=float(s.quantile(.10)), p25=float(s.quantile(.25)),
                    p50=float(s.median()), p75=float(s.quantile(.75)),
                    p90=float(s.quantile(.90)),
                    iqr=float(s.quantile(.75) - s.quantile(.25)),
                    cv_pct=float(s.std() / s.mean() * 100),
                    at40_pct=float(s.eq(40).mean() * 100),
                    at48_pct=float(s.eq(48).mean() * 100))

    dec = (LAW.year // 10 * 10).astype(int)
    by_dec = {int(d): {k: round(v, 4) for k, v in stats(g).items()}
              for d, g in LAW.groupby(dec).normalhours}
    R["dispersion_by_decade"] = by_dec

    # Per-year for the fan chart. Percentiles are meaningless on a handful of polities, so the
    # plotted window starts at the first year with at least MIN_N law-havers.
    MIN_N = 20
    rows = []
    for y, g in LAW.groupby("year").normalhours:
        if len(g) >= MIN_N:
            rows.append({"year": int(y), **{k: round(v, 4) for k, v in stats(g).items()}})
    R["dispersion_by_year"] = rows
    R["fan_min_n"] = MIN_N
    R["fan_first_year"] = rows[0]["year"] if rows else None

    # "Tightest" is meaningless without conditioning on how much of the world is in the set. The
    # 1890s have the lowest CV of any decade, but only 33 polities had a law and they are all early
    # European adopters. So report BOTH: the unconditional minimum, and the minimum restricted to
    # decades where most of the world actually legislated. The essay must not quote the second
    # without stating the condition.
    # "Lowest spread of any decade" is FALSE without the size condition: the 1840s, 1850s and 1860s
    # all have a spread of exactly zero, because France is the only polity with a law and it sits at
    # 72 hours every year. The 1890s are only the lowest among decades big enough to mean anything.
    all_cvs = {int(d): v["cv_pct"] for d, v in by_dec.items()}
    R["decades_below_1890s"] = sorted(d for d, c in all_cvs.items()
                                      if c < all_cvs.get(1890, 1e9))
    cvs = {int(d): v["cv_pct"] for d, v in by_dec.items() if v["n"] >= MIN_N}
    tight = min(cvs, key=cvs.get)
    R["tightest_decade_unconditional"] = {
        "decade": tight, "cv_pct": round(cvs[tight], 2), "n": by_dec[tight]["n"],
        "share_with_law_pct": R["coverage_by_decade"][tight],
        "condition": f"decades with at least {MIN_N} polity-years of law",
        "decades_with_lower_spread_but_fewer_observations": [
            {"decade": d, "cv_pct": round(all_cvs[d], 2), "polity_years": by_dec[d]["n"]}
            for d in sorted(all_cvs) if all_cvs[d] < cvs[tight]],
    }
    broad = {d: c for d, c in cvs.items() if R["coverage_by_decade"].get(d, 0) >= 50.0}
    tb = min(broad, key=broad.get)
    R["tightest_decade_broad"] = {
        "decade": tb, "cv_pct": round(broad[tb], 2), "n": by_dec[tb]["n"],
        "share_with_law_pct": R["coverage_by_decade"][tb],
        "condition": "decades in which at least 50% of polities had a working-hours law",
    }
    R["zero_iqr_decades"] = sorted(int(d) for d, v in by_dec.items()
                                   if v["n"] >= MIN_N and v["iqr"] == 0.0)
    R["zero_iqr_years"] = [r["year"] for r in rows if r["iqr"] == 0.0]

    # THE YEARLY MINIMUM IS THE ONE THE ESSAY SHOULD QUOTE, not the decade minimum. Chart 1 is a
    # yearly series, and decade aggregation pools within-decade change: the 1950s decade CV (7.92)
    # is higher than any single year from 1949 to 1951 (about 6.2) because the 1952 adoption wave
    # happens inside that decade. Quoting the 1960s as "tightest" beside a chart whose visible
    # minimum is 1949 reads as a contradiction, and the yearly figure is what the chart shows.
    yr = {r["year"]: r for r in rows}
    lo = min(rows, key=lambda r: r["cv_pct"])
    after = [r for r in rows if r["year"] > 1951]
    # 1949 and 1950 are the SAME distribution to the row, so min() was silently tie-breaking on the
    # earlier year and presenting an arbitrary choice as a finding. Report every tied year.
    tied = sorted(r["year"] for r in rows if abs(r["cv_pct"] - lo["cv_pct"]) < 1e-9)
    R["tightest_year"] = {
        "years": tied, "year": lo["year"], "cv_pct": round(lo["cv_pct"], 2), "n": lo["n"],
        "sd": round(lo["sd"], 3), "iqr": lo["iqr"],
        "coverage_pct": R["coverage_by_year"][lo["year"]],
        "condition": f"years in which at least {MIN_N} polities had a law",
    }
    # The median does not "step" from 48 to 44. It holds 48 for 59 years, then takes 17 more and
    # nine separate moves, two of them upward, to settle at 44 in 1994.
    med = {r["year"]: r["p50"] for r in rows}
    flat = [y for y in sorted(med) if med[y] == 48.0]
    moves = [(y, med[y] - med[y - 1]) for y in sorted(med)
             if y - 1 in med and med[y] != med[y - 1] and y > flat[-1]]
    R["median_path"] = {
        "held_48_from": flat[0], "held_48_to": flat[-1], "years_at_48": len(flat),
        "first_year_at_44": min((y for y in sorted(med) if med[y] == 44.0), default=None),
        "n_moves_after": len(moves),
        "n_upward_moves": sum(1 for _, d in moves if d > 0),
        "upward_move_years": [y for y, d in moves if d > 0],
        "levels_after": sorted({med[y] for y in sorted(med) if y > flat[-1]}, reverse=True),
    }
    R["never_regained"] = {
        "years_after_1951_below_that_cv": [r["year"] for r in after if r["cv_pct"] < lo["cv_pct"]],
        "best_since_1951": {"year": min(after, key=lambda r: r["cv_pct"])["year"],
                            "cv_pct": round(min(r["cv_pct"] for r in after), 2)},
        "cv_at_cut": round(yr[CUT]["cv_pct"], 2),
    }


def balanced_panel(LAW):
    """ROBUSTNESS. Does the spread widen because the world genuinely disagrees more, or only because
    the set of law-havers grew from 97 polities in 1950 to 168 in 2012?

    Adding countries can widen a spread mechanically. So repeat the comparison on the constant set
    of polities that had a law in BOTH years. If dispersion still widens there, composition is not
    the explanation. If it does not, the hook is an artefact and the essay must be rewritten.
    """
    out = {}
    for base in (1930, 1950, 1960):
        a = LAW[LAW.year.eq(base)].set_index("country_name").normalhours
        b = LAW[LAW.year.eq(CUT)].set_index("country_name").normalhours
        both = a.index.intersection(b.index)
        aa, bb = a.loc[both], b.loc[both]
        out[base] = {
            "n_constant": len(both),
            "n_in_base_all": len(a), "n_in_cut_all": len(b),
            f"sd_{base}": round(float(aa.std()), 3), f"sd_{CUT}": round(float(bb.std()), 3),
            f"iqr_{base}": round(float(aa.quantile(.75) - aa.quantile(.25)), 2),
            f"iqr_{CUT}": round(float(bb.quantile(.75) - bb.quantile(.25)), 2),
            f"cv_{base}_pct": round(float(aa.std()) / float(aa.mean()) * 100, 2),
            f"cv_{CUT}_pct": round(float(bb.std()) / float(bb.mean()) * 100, 2),
            f"mean_{base}": round(float(aa.mean()), 2), f"mean_{CUT}": round(float(bb.mean()), 2),
            f"distinct_{base}": int(aa.nunique()), f"distinct_{CUT}": int(bb.nunique()),
            "widened_sd": bool(bb.std() > aa.std()),
            "widened_iqr": bool((bb.quantile(.75) - bb.quantile(.25)) > (aa.quantile(.75) - aa.quantile(.25))),
        }
    R["balanced_panel"] = out


def two_numbers(LAW):
    """Chart 2: the standoff. 1950 stacked on one number, 2012 split between two."""
    snaps = {}
    for y in (1950, CUT):
        s = LAW[LAW.year.eq(y)].normalhours
        counts = {float(k): int(v) for k, v in s.value_counts().sort_index().items()}
        snaps[y] = {
            "n": len(s),
            "counts": counts,
            "at40": int(s.eq(40).sum()), "at40_pct": round(s.eq(40).mean() * 100, 1),
            "at48": int(s.eq(48).sum()), "at48_pct": round(s.eq(48).mean() * 100, 1),
            "other": int((~s.isin([40, 48])).sum()),
            "other_pct": round((~s.isin([40, 48])).mean() * 100, 1),
            "n_distinct": int(s.nunique()),
            "min": float(s.min()), "max": float(s.max()),
            "median": float(s.median()), "mean": round(float(s.mean()), 2),
        }
    R["snapshots"] = snaps

    s = LAW[LAW.year.eq(CUT)]
    R["bloc48_countries"] = sorted(s[s.normalhours.eq(48)].country_name.tolist())
    R["bloc40_countries"] = sorted(s[s.normalhours.eq(40)].country_name.tolist())
    R["below40"] = (s[s.normalhours.lt(40)][["country_name", "normalhours"]]
                    .sort_values("normalhours")
                    .to_dict("records"))
    # 48 hours does not fit into five eight-hour days. This is the only form of the title's claim
    # the data can support: the dataset has no days-per-week column.
    R["arithmetic"] = {
        "five_eight_hour_days": 40, "six_eight_hour_days": 48,
        "hours_per_day_if_48_over_5_days": round(48 / 5, 1),
    }


def how_it_spread(LAW):
    """Chart 3: adoption waves. First year each polity's statutory week equals exactly 48, then 40."""
    out = {}
    for val in (48, 40):
        first = LAW[LAW.normalhours.eq(val)].groupby("country_name").year.min()
        bins = range(1900, CUT + 6, 5)
        hist = pd.cut(first, bins=bins, right=True).value_counts().sort_index()
        out[val] = {
            "n_polities": len(first),
            "windows": [{"end": int(iv.right), "n": int(n)} for iv, n in hist.items() if n > 0],
            "by_year": {int(y): int(c) for y, c in first.value_counts().sort_index().items()},
        }
        peak_year = int(first.value_counts().idxmax())
        out[val]["peak_year"] = peak_year
        out[val]["peak_year_n"] = int(first.value_counts().max())
        out[val]["peak_year_countries"] = sorted(first[first.eq(peak_year)].index.tolist())
    R["adoption"] = out

    f48 = LAW[LAW.normalhours.eq(48)].groupby("country_name").year.min()
    R["wave_1919"] = {
        "window": "1916 to 1920",
        "n": int(f48.between(1916, 1920).sum()),
        "countries": sorted(f48[f48.between(1916, 1920)].index.tolist()),
    }
    f40 = LAW[LAW.normalhours.eq(40)].groupby("country_name").year.min()
    R["wave_1952"] = {
        "year": 1952,
        "n": int(f40.eq(1952).sum()),
        "countries": sorted(f40[f40.eq(1952)].index.tolist()),
    }
    R["early_40"] = (f40[f40 < 1952].sort_values()
                     .reset_index().rename(columns={"country_name": "country", "year": "year"})
                     .assign(year=lambda d: d.year.astype(int)).to_dict("records"))

    # WHICH WAVE IS ACTUALLY THE BIGGEST. An earlier draft called the 1919 wave the fastest thing in
    # the file. It is not. The fixed five-year BIN 1916 to 1920 does hold the most first-adoptions of
    # 48 (20), but a ROLLING five-year window starting 1944 holds 24, and the largest single year for
    # 48 is 1945 with 14, not 1919 with 12. Only the 1952 figure survives as an outright maximum:
    # 15 in one year is the largest single-year adoption across both series.
    waves = {}
    for val, first in ((48, f48), (40, f40)):
        vc = first.value_counts()
        roll = max(((int(first.between(s, s + 4).sum()), s) for s in range(1789, CUT - 3)))
        waves[val] = {
            "largest_single_year": int(vc.max()), "largest_single_year_year": int(vc.idxmax()),
            "top_single_years": [[int(y), int(c)] for y, c in vc.sort_values(ascending=False).head(5).items()],
            "largest_rolling_5yr": roll[0], "largest_rolling_5yr_start": roll[1],
            "largest_rolling_5yr_countries": sorted(first[first.between(roll[1], roll[1] + 4)].index.tolist()),
            "countries_in_peak_year": sorted(first[first.eq(int(vc.idxmax()))].index.tolist()),
        }
    # "Most of them French African territories" needs a count, not an impression.
    FR_AFRICA = {"Benin", "Burkina Faso", "Central African Republic", "Chad", "Comoros", "Djibouti",
                 "Gabon", "Guinea", "Ivory Coast", "Madagascar", "Mali", "Mauritania", "Niger",
                 "Republic of the Congo", "Senegal", "Togo"}
    w48 = waves[48]
    inwin = w48["largest_rolling_5yr_countries"]
    fr = sorted(set(inwin) & FR_AFRICA)
    w48["french_african_in_window"] = fr
    w48["n_french_african_in_window"] = len(fr)
    w48["n_french_african_in_first_year"] = int(
        f48[f48.eq(w48["largest_rolling_5yr_start"])].index.isin(FR_AFRICA).sum())
    R["waves"] = waves
    R["largest_single_year_overall"] = max(
        ({"value": v, "n": w["largest_single_year"], "year": w["largest_single_year_year"]}
         for v, w in waves.items()), key=lambda d: d["n"])

    # The essay makes a claim about 1948 specifically. Compute it rather than asserting it.
    s48y = LAW[LAW.year.eq(1948)].normalhours
    R["snapshot_1948"] = {
        "n": len(s48y), "at48": int(s48y.eq(48).sum()),
        "at48_pct": round(s48y.eq(48).mean() * 100, 1),
        "counts": {float(k): int(v) for k, v in s48y.value_counts().sort_index().items()},
        "iqr": float(s48y.quantile(.75) - s48y.quantile(.25)),
        "n_distinct": int(s48y.nunique()),
    }


def three_instruments(LAW):
    """Chart 4: only one of the three instruments standardized."""
    dec = (LAW.year // 10 * 10).astype(int)
    rows, raw_cv = [], []
    for d, g in LAW.groupby(dec):
        raw_cv.append({"decade": int(d), **{
            k: (float(g[c].dropna().std()) / float(g[c].dropna().mean()) * 100
                if len(g[c].dropna()) > 1 and g[c].dropna().mean() > 0 else None)
            for k, c in (("normal", "normalhours"), ("max", "hours_max"),
                         ("overtime", "overtime_remun"))}})
        row = {"decade": int(d), "n": len(g)}
        for key, col in (("normal", "normalhours"), ("max", "hours_max"), ("overtime", "overtime_remun")):
            s = g[col].dropna()
            m = float(s.mean()) if len(s) else np.nan
            # Early decades have a mean overtime premium of exactly 0, so CV is undefined there.
            row[f"{key}_n"] = len(s)
            row[f"{key}_mean"] = round(m, 3) if len(s) else None
            row[f"{key}_sd"] = round(float(s.std()), 3) if len(s) > 1 else None
            row[f"{key}_cv_pct"] = (round(float(s.std()) / m * 100, 2)
                                    if len(s) > 1 and m and m > 0 else None)
        rows.append(row)
    R["instruments_by_decade"] = rows

    snap = {}
    for key, col in (("normal", "normalhours"), ("max", "hours_max"), ("overtime", "overtime_remun")):
        s = LAW[LAW.year.eq(CUT)][col].dropna()
        snap[key] = {"n": len(s), "n_distinct": int(s.nunique()),
                     "min": float(s.min()), "max": float(s.max()),
                     "mean": round(float(s.mean()), 2), "sd": round(float(s.std()), 2),
                     "cv_pct": round(float(s.std()) / float(s.mean()) * 100, 2)}
    ot = LAW[LAW.year.eq(CUT)].overtime_remun.dropna()
    snap["overtime"]["at50_pct"] = round(ot.eq(50).mean() * 100, 1)
    snap["overtime"]["at50_n"] = int(ot.eq(50).sum())
    # The overtime panel is scoped to countries that HAVE a premium, so the "% at exactly +50" quoted
    # beside it must be on the same denominator or it silently switches population mid-sentence.
    pos = ot[ot > 0]
    snap["overtime"]["n_with_premium"] = int(len(pos))
    snap["overtime"]["at50_pct_of_premium_havers"] = round(pos.eq(50).mean() * 100, 1)
    # The 1940 law-haver range, used to bound the Table 3 impossibility argument.
    y40 = LAW[LAW.year.eq(1940)].normalhours.dropna()
    R["range_1940"] = {"min": float(y40.min()), "max": float(y40.max()), "n": int(len(y40)),
                       "max_possible_sd": round((float(y40.max()) - float(y40.min())) / 2, 1)}
    R["instruments_at_cut"] = snap

    # Convergence summary over a window where the country set is broad enough for dispersion to
    # mean something. Before 1920 fewer than 27% of polities had a law and the CV series is driven
    # by which handful of early adopters happens to be in the set, so the minimum there is noise.
    W = 1920
    R["instrument_window_start"] = W
    summary = {}
    # Percentage changes are computed from the UNROUNDED series. Deriving them from the 2-decimal
    # rounded column manufactured a 24.1% where the true figure is 24.0%, which is exactly the kind
    # of false precision this post is about.
    for key in ("normal", "overtime", "max"):
        s = pd.DataFrame(raw_cv)
        s = s[(s.decade >= W) & s[key].notna()][["decade", key]]
        s.columns = ["decade", "cv"]
        lo = s.loc[s.cv.idxmin()]
        summary[key] = {
            "window_start_decade": int(s.iloc[0].decade),
            "cv_at_start": round(float(s.iloc[0].cv), 2),
            "cv_min": round(float(lo.cv), 2), "cv_min_decade": int(lo.decade),
            "cv_at_end": round(float(s.iloc[-1].cv), 2),
            "end_decade": int(s.iloc[-1].decade),
            "pct_fall_to_min": round((s.iloc[0].cv - lo.cv) / s.iloc[0].cv * 100, 1),
            "pct_rise_since_min": round((s.iloc[-1].cv - lo.cv) / lo.cv * 100, 1),
            "ends_wider_than_start": bool(s.iloc[-1].cv > s.iloc[0].cv),
            "pct_wider_than_start": round((s.iloc[-1].cv - s.iloc[0].cv) / s.iloc[0].cv * 100, 1),
        }
    R["instrument_convergence"] = summary

    # THE OVERTIME CV IS NOT A MEASURE OF SPREAD. Adversarial review caught this. Its 45.8% "fall"
    # is entirely the denominator: the mean premium nearly doubles as the share of law-havers with
    # NO premium at all collapses, while the raw standard deviation actually RISES. That is the same
    # extensive-margin effect the 96 sentinel creates for normal hours, reappearing in another
    # column. Report the honest version: convergence among countries that actually have a premium.
    rows2 = []
    for d, g in LAW.groupby(dec):
        pos = g[g.overtime_remun.gt(0)].overtime_remun
        allv = g.overtime_remun.dropna()
        rows2.append({
            "decade": int(d), "n_all": len(allv), "n_with_premium": len(pos),
            "pct_zero": round(float(allv.eq(0).mean()) * 100, 2) if len(allv) else None,
            "sd_all": round(float(allv.std()), 3) if len(allv) > 1 else None,
            "cv_with_premium_pct": (round(float(pos.std()) / float(pos.mean()) * 100, 2)
                                    if len(pos) > 1 and pos.mean() > 0 else None),
        })
    R["overtime_honest"] = rows2
    w = [r for r in rows2 if r["decade"] >= W and r["cv_with_premium_pct"] is not None]
    lo = min(w, key=lambda r: r["cv_with_premium_pct"])
    sd_start = next(r for r in rows2 if r["decade"] == W)["sd_all"]
    sd_at_lo = next(r for r in rows2 if r["decade"] == lo["decade"])["sd_all"]
    R["overtime_convergence_honest"] = {
        "cv_at_start": w[0]["cv_with_premium_pct"], "start_decade": w[0]["decade"],
        "cv_min": lo["cv_with_premium_pct"], "cv_min_decade": lo["decade"],
        "cv_at_end": w[-1]["cv_with_premium_pct"], "end_decade": w[-1]["decade"],
        "pct_fall_to_min": round((w[0]["cv_with_premium_pct"] - lo["cv_with_premium_pct"])
                                 / w[0]["cv_with_premium_pct"] * 100, 1),
        "pct_zero_at_start": w[0]["pct_zero"], "pct_zero_at_end": w[-1]["pct_zero"],
        "sd_all_at_start": sd_start, "sd_all_at_min": sd_at_lo,
        "sd_all_pct_change_to_min": round((sd_at_lo - sd_start) / sd_start * 100, 1),
    }

    # Is the maximum week really "at its widest"? Only on decade-pooled CV, and only by 0.03 points.
    # At year level 2012 is nowhere near the top. Drop the superlative.
    yv = LAW.groupby("year").hours_max.agg(sd="std", mean="mean")
    yv = yv[yv.sd.notna() & yv["mean"].gt(0)]
    yv["cv"] = yv.sd / yv["mean"] * 100
    R["hours_max_rank"] = {
        "cv_at_cut": round(float(yv.loc[CUT, "cv"]), 2),
        "rank_of_cut_year": int((yv.cv > yv.loc[CUT, "cv"]).sum()) + 1,
        "n_years": int(len(yv)),
        "max_cv_year": int(yv.cv.idxmax()), "max_cv": round(float(yv.cv.max()), 2),
        "decade_cv_2010s": summary["max"]["cv_at_end"],
        "decade_cv_1990s": next(r["max_cv_pct"] for r in rows if r["decade"] == 1990),
    }


def paper_table3(df):
    """Reproduce Table 3 of Rasmussen (2024) and show what it is computed on.

    The table is captioned "standard Deviations for countries regulating working time" and its
    values rise to 23.68 in 1940 before falling to 9.64 in 2010, which the paper reads as
    convergence. An SD of 23.68 is arithmetically impossible among countries whose statutory week
    lay between 40 and 60, as every law-haver's did in 1940: the widest a variable bounded there can be
    is 10. So the statistic cannot be computed on regulators only.

    It reproduces to a maximum absolute error of 0.03 over all polities carrying a COW code, WITH
    the 96 no-law code included. Computed on law-havers only it does not reproduce at all, and it
    falls to a minimum in 1950 and then RISES.

    This is not presented as an error. Treating an unregulated week as 96 hours is a defensible
    modelling choice, and on that choice the falling SD measures exactly what the paper argues:
    the world converging as regulation spreads. It answers a different question from "do the
    countries that regulate agree with each other", which is the question this post asks.
    """
    published = {2010: 9.64, 2000: 12.82, 1990: 15.11, 1980: 16.70, 1970: 19.59, 1960: 21.79,
                 1950: 23.35, 1940: 23.68, 1930: 21.96, 1920: 18.76, 1910: 7.87, 1900: 5.17,
                 1890: 5.90}
    rows, pub, rep, own = [], [], [], []
    for y in sorted(published, reverse=True):
        f = df[df.year.eq(y)]
        with_cow = float(f[f.COWcode.notna()].normalhours.std())
        law_only = float(f[f.workinglaw.eq(1)].normalhours.std())
        rows.append({"year": y, "published": published[y],
                     "reproduced_all_polities_with_cowcode": round(with_cow, 2),
                     "law_havers_only": round(law_only, 2),
                     "n_law": int(f.workinglaw.eq(1).sum())})
        pub.append(published[y]); rep.append(with_cow); own.append(law_only)
    R["paper_table3"] = {
        "rows": rows,
        "max_abs_error_vs_published": round(float(np.abs(np.array(pub) - np.array(rep)).max()), 3),
        "corr_vs_published": round(float(np.corrcoef(pub, rep)[0, 1]), 6),
        "corr_law_havers_vs_published": round(float(np.corrcoef(pub, own)[0, 1]), 4),
        "law_havers_1940": round(own[pub.index(23.68)], 2),
        "law_havers_1950": round(own[pub.index(23.35)], 2),
        "law_havers_2010": round(own[pub.index(9.64)], 2),
        "published_1940": 23.68, "published_2010": 9.64,
    }


def reforms(LAW):
    """Context: reform is rare and almost always one directional."""
    S = LAW.sort_values(["country_name", "year"])
    d = S.groupby("country_name").normalhours.diff()
    gap = S.year - S.groupby("country_name").year.shift()
    ev = S.assign(delta=d, gap=gap)[d.notna() & d.ne(0)]
    # A diff taken across a break in a country's own coverage is not a reform. Six of the 206 are
    # re-entries, three of them Baltic states returning after half a century of annexation. Report
    # the contiguous count as the headline and keep the gap cases visible.
    cont = ev[ev.gap.eq(1)]
    R["reforms"] = {
        "n_events": len(ev),
        "n_cuts": int((ev.delta < 0).sum()),
        "n_increases": int((ev.delta > 0).sum()),
        "n_events_contiguous": len(cont),
        "n_cuts_contiguous": int((cont.delta < 0).sum()),
        "n_increases_contiguous": int((cont.delta > 0).sum()),
        "gap_spanning": [{"country": r.country_name, "year": int(r.year),
                          "gap_years": int(r.gap), "delta": float(r.delta)}
                         for r in ev[ev.gap.ne(1)].itertuples()],
        "median_cut": round(float(cont[cont.delta < 0].delta.median()), 2),
        "mean_cut": round(float(cont[cont.delta < 0].delta.mean()), 2),
        "first_year": int(ev.year.min()), "last_year": int(ev.year.max()),
        "by_decade": {int(k): int(v) for k, v in
                      cont.assign(dec=(cont.year // 10 * 10).astype(int)).groupby("dec").size().items()},
    }
    bd = R["reforms"]["by_decade"]
    peak = max(bd, key=bd.get)
    R["reforms"]["peak_decade"] = {"decade": peak, "n": bd[peak]}


def frame(df, LAW, raw):
    R["meta"] = {
        "source_rows_raw": len(raw),
        "polities_raw": int(raw.country_name.nunique()),
        "year_min_raw": int(raw.year.min()), "year_max_raw": int(raw.year.max()),
        "duplicate_country_years": int(raw.duplicated(["country_name", "year"]).sum()),
        "cut_year": CUT,
        "rows_after_cut": len(df),
        "polities_after_cut": int(df.country_name.nunique()),
        "law_rows_after_cut": len(LAW),
        "polities_ever_with_law": int(LAW.country_name.nunique()),
        "polities_never_with_law": int(df.country_name.nunique() - LAW.country_name.nunique()),
        "share_with_law_at_cut_pct": round(float(df[df.year.eq(CUT)].workinglaw.mean()) * 100, 1),
        "n_law_at_cut": int(df[df.year.eq(CUT)].workinglaw.sum()),
        "n_polities_at_cut": int(df.year.eq(CUT).sum()),
    }
    # Share of polities holding any working-hours law, by decade. Used to condition every
    # "tightest agreement" claim, because a low spread across 33 early adopters is not the same
    # statement as a low spread across most of the world.
    dec = (df.year // 10 * 10).astype(int)
    R["coverage_by_decade"] = {int(d): round(float(g.mean()) * 100, 1)
                               for d, g in df.assign(dec=dec).groupby("dec").workinglaw}
    R["coverage_by_year"] = {int(y): round(float(g.mean()) * 100, 1)
                             for y, g in df.groupby("year").workinglaw}
    # The 1890s "tightest decade" caveat counts POLITY-YEARS, not polities. Conflating the two put
    # "all 33 are European early adopters" in an earlier draft when the real number is four.
    d90 = LAW[LAW.year.between(1890, 1899)]
    R["decade_1890s"] = {
        "polity_years": len(d90),
        "polities": sorted(d90.country_name.unique().tolist()),
        "n_polities": int(d90.country_name.nunique()),
    }


def main():
    raw, meta = load()
    df = raw[raw.year <= CUT].copy()
    LAW = df[df.workinglaw.eq(1)].copy()

    verify_traps(raw)
    frame(df, LAW, raw)
    naive_vs_honest(df, LAW)
    dispersion(LAW)
    balanced_panel(LAW)
    two_numbers(LAW)
    how_it_spread(LAW)
    three_instruments(LAW)
    paper_table3(raw)
    reforms(LAW)

    (BASE / "results.json").write_text(json.dumps(R, indent=2, sort_keys=True))
    print("wrote results.json")

    t, m, n = R["traps"], R["meta"], R["naive_vs_honest"]
    print(f"\nTRAP 1  sentinel {t['sentinel_value']:.0f} == no-law in {t['sentinel_rows']} rows, "
          f"{t['sentinel_mismatches']} mismatches, {t['sentinel_share_of_file_pct']}% of file")
    print(f"        naive mean over raw column = {t['naive_mean_all_rows']} hours")
    print(f"TRAP 2  2012->2013 on {t['cliff_countries_compared']} countries: "
          f"{t['cliff_lost_hours_max']} lose max hours, {t['cliff_overtime_to_zero']} lose overtime, "
          f"only {t['cliff_normalhours_changed']} change normal hours")
    print(f"        overtime-zero jump 2013 = +{t['cliff_jump_2013']:.0f} vs biggest real "
          f"+{t['biggest_real_jump']:.0f} ({t['biggest_real_jump_year']})")
    print(f"\nFRAME   {m['rows_after_cut']} rows to {CUT}, {m['polities_after_cut']} polities, "
          f"{m['polities_ever_with_law']} ever legislate, {m['polities_never_with_law']} never")
    print(f"DECOMP  naive fall {n['naive_total_change']} hrs = composition "
          f"{n['symmetric']['composition']} ({n['symmetric_pct']['composition']}%) + real "
          f"{n['symmetric']['real']} ({n['symmetric_pct']['real']}%), "
          f"composition range {n['composition_pct_range']}%")
    tu, tb = R["tightest_decade_unconditional"], R["tightest_decade_broad"]
    print(f"HOOK    tightest overall: {tu['decade']}s CV {tu['cv_pct']}% on n={tu['n']} "
          f"({tu['share_with_law_pct']}% of polities had a law)")
    print(f"        tightest once most of the world legislates: {tb['decade']}s CV {tb['cv_pct']}% "
          f"on n={tb['n']} ({tb['share_with_law_pct']}% coverage)")
    print(f"        zero-IQR decades {R['zero_iqr_decades']}, zero-IQR years "
          f"{R['zero_iqr_years'][:3]}...{R['zero_iqr_years'][-3:] if len(R['zero_iqr_years'])>3 else ''} "
          f"({len(R['zero_iqr_years'])} yrs), fan starts {R['fan_first_year']}")
    print("\nBALANCED PANEL (does the widening survive holding the country set constant?)")
    for base, v in R["balanced_panel"].items():
        print(f"        {base} vs {CUT} on the {v['n_constant']} polities with a law in both: "
              f"SD {v[f'sd_{base}']} -> {v[f'sd_{CUT}']}, IQR {v[f'iqr_{base}']} -> {v[f'iqr_{CUT}']}, "
              f"distinct {v[f'distinct_{base}']} -> {v[f'distinct_{CUT}']}  "
              f"[widened SD={v['widened_sd']}, IQR={v['widened_iqr']}]")
    s = R["snapshots"]
    print(f"STANDOFF {CUT}: {s[CUT]['at40']} at 40 ({s[CUT]['at40_pct']}%), "
          f"{s[CUT]['at48']} at 48 ({s[CUT]['at48_pct']}%), "
          f"{s[CUT]['other']} other ({s[CUT]['other_pct']}%), n={s[CUT]['n']}")
    print(f"         1950: {s[1950]['at48']} at 48 ({s[1950]['at48_pct']}%), n={s[1950]['n']}")
    print(f"WAVES   1919 window {R['wave_1919']['n']} to 48; 1952 {R['wave_1952']['n']} to 40")
    i = R["instruments_at_cut"]
    print(f"INSTR   at {CUT}: normal CV {i['normal']['cv_pct']}%, max CV {i['max']['cv_pct']}% "
          f"({i['max']['n_distinct']} values, {i['max']['min']:.0f} to {i['max']['max']:.0f}), "
          f"overtime CV {i['overtime']['cv_pct']}% ({i['overtime']['at50_pct']}% at +50)")
    print(f"CONVERGENCE (window from {R['instrument_window_start']}s, where coverage is broad)")
    for k, v in R["instrument_convergence"].items():
        print(f"        {k:9s} CV {v['cv_at_start']:6.2f} ({v['window_start_decade']}s) -> min "
              f"{v['cv_min']:6.2f} ({v['cv_min_decade']}s) -> {v['cv_at_end']:6.2f} "
              f"({v['end_decade']}s) | fell {v['pct_fall_to_min']:5.1f}%, then rose "
              f"{v['pct_rise_since_min']:5.1f}% | vs start: {v['pct_wider_than_start']:+5.1f}%")


if __name__ == "__main__":
    main()
