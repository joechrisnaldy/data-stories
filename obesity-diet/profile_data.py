"""Vet the four OWID extracts BEFORE building anything.

Questions this answers, in order of how badly a wrong answer would hurt:
  1. Are the entities countries, or do OWID's aggregates (World, continents, income
     groups) sit in the same column? A scatter that silently includes "World" is a
     scatter with a fake point in it.
  2. Crude vs age-standardised obesity: how much does the choice move a country?
     Age structure varies enormously and obesity rises with age, so the crude series
     partly measures demography.
  3. What is the latest year where all four series actually overlap, and how many
     countries survive the join?
  4. Do the macronutrient components reconcile to the total calorie series?
  5. Physical sanity: shares in [0, 100], calories in a survivable range.
"""
import pandas as pd
from pathlib import Path

from build_analysis import YEAR, only_countries

DATA = Path(__file__).resolve().parent / "data"

FILES = {
    "obesity_crude": ("share-of-adults-defined-as-obese.csv", "obesity_crude_pct"),
    "obesity_std": ("obesity-age-standardized.csv", "obesity_std_pct"),
    "calories": ("daily-per-capita-caloric-supply.csv", "kcal"),
    "gdp": ("gdp-per-capita-worldbank.csv", "gdp_pc"),
}


def load_single(fname, newname):
    d = pd.read_csv(DATA / fname)
    value_cols = [c for c in d.columns
                  if c not in ("entity", "code", "year", "owid_region")]
    assert len(value_cols) == 1, f"{fname}: expected 1 value column, got {value_cols}"
    return d.rename(columns={value_cols[0]: newname})[["entity", "code", "year", newname]]


def load_macros():
    d = pd.read_csv(DATA / "daily-caloric-supply-derived-from-carbohydrates-protein-and-fat.csv")
    return d.rename(columns={
        "energy_from_animal_protein": "kcal_animal_protein",
        "energy_from_vegetal_protein": "kcal_vegetal_protein",
        "total_energy_from_fat": "kcal_fat",
        "total_energy_from_carbohydrates": "kcal_carbs"})


def main():
    frames = {k: load_single(f, n) for k, (f, n) in FILES.items()}
    macros = load_macros()

    print("=" * 78)
    print("1. SHAPE AND COVERAGE")
    for name, d in list(frames.items()) + [("macros", macros)]:
        yrs = d.year
        print(f"  {name:16s} rows {len(d):>7,}  entities {d.entity.nunique():>4}  "
              f"years {yrs.min()}-{yrs.max()}")

    print()
    print("=" * 78)
    print("2. AGGREGATES HIDING IN THE ENTITY COLUMN")
    # ROUND 3 CORRECTION. This tested only for a missing or OWID_ code, which is WEAKER than
    # build_analysis.only_countries(). The WHO obesity files carry six regional aggregates coded
    # WHO_AFR, WHO_AMR, WHO_EMR, WHO_EUR, WHO_SEAR and WHO_WPAC: not blank, not OWID_, and not
    # three characters. This section reported 1 non-country entity where there are 7, and section
    # 3 below computed its comparison with six fabricated points in it. Share the real filter.
    for name, d in list(frames.items()) + [("macros", macros)]:
        noniso = sorted(set(d.entity) - set(only_countries(d).entity))
        print(f"  {name:16s} {len(noniso):>3} non-country entities: {noniso[:8]}"
              f"{' ...' if len(noniso) > 8 else ''}")

    print()
    print("=" * 78)
    print("3. CRUDE VS AGE-STANDARDISED OBESITY")
    ob = frames["obesity_crude"].merge(
        frames["obesity_std"], on=["entity", "code", "year"], how="inner")
    ob = only_countries(ob)
    # ROUND 2 CORRECTION. This pinned to ob.year.max(), which is 2024, while the post analyses
    # 2023, so the vet printed a comparison the post never quotes. ROUND 3: the year is now
    # imported from build_analysis rather than retyped, because a second hardcoded constant is a
    # second thing to forget on a data refresh.
    latest_ob = ob[ob.year == YEAR].copy()
    latest_ob["gap"] = latest_ob.obesity_crude_pct - latest_ob.obesity_std_pct
    print(f"  analysis year {YEAR}, {len(latest_ob)} countries")
    print(f"  mean gap {latest_ob.gap.mean():+.2f} pts, "
          f"sd {latest_ob.gap.std():.2f}, "
          f"range {latest_ob.gap.min():+.2f} to {latest_ob.gap.max():+.2f}")
    print(f"  correlation of the two series: {latest_ob.obesity_crude_pct.corr(latest_ob.obesity_std_pct):.4f}")
    print("  most understated by the crude series (older populations read heavier):")
    for _, r in latest_ob.nlargest(5, "gap").iterrows():
        print(f"    {r.entity:28s} crude {r.obesity_crude_pct:5.1f}  "
              f"std {r.obesity_std_pct:5.1f}  gap {r.gap:+.1f}")
    print("  most overstated:")
    for _, r in latest_ob.nsmallest(5, "gap").iterrows():
        print(f"    {r.entity:28s} crude {r.obesity_crude_pct:5.1f}  "
              f"std {r.obesity_std_pct:5.1f}  gap {r.gap:+.1f}")

    print()
    print("=" * 78)
    print("4. MACRONUTRIENTS VS THE TOTAL CALORIE SERIES")
    m = macros.copy()
    m["macro_sum"] = (m.kcal_animal_protein + m.kcal_vegetal_protein
                      + m.kcal_fat + m.kcal_carbs)
    chk = m.merge(frames["calories"], on=["entity", "code", "year"], how="inner")
    chk = chk[chk.code.notna() & ~chk.code.astype(str).str.startswith("OWID")]
    chk["resid_pct"] = (chk.macro_sum - chk.kcal) / chk.kcal * 100
    print(f"  {len(chk):,} country-years compared")
    print(f"  components minus total, as % of total: mean {chk.resid_pct.mean():+.2f}, "
          f"median {chk.resid_pct.median():+.2f}, "
          f"p5 {chk.resid_pct.quantile(.05):+.2f}, p95 {chk.resid_pct.quantile(.95):+.2f}")
    print("  NOTE: alcohol and a few minor items are calories but not carb/fat/protein,")
    print("        so a small negative residual is expected, not a bug.")

    print()
    print("=" * 78)
    print("5. LATEST COMMON YEAR AND JOIN SURVIVAL")
    for y in range(2023, 2009, -1):
        counts, sets_ = {}, []
        for name, d in list(frames.items()) + [("macros", macros)]:
            sub = only_countries(d[d.year == y]).dropna()
            counts[name] = len(sub)
            sets_.append(set(sub.code))
        joined = set.intersection(*sets_)
        core = set.intersection(*[s for n, s in zip(
            [*frames, "macros"], sets_) if n != "obesity_crude"])
        print(f"  {y}: " + "  ".join(f"{k} {v:>3}" for k, v in counts.items())
              + f"   -> JOIN {len(joined):>3}")
        if len(joined) >= 100:
            break

    print()
    print("=" * 78)
    print("6. PHYSICAL SANITY")
    for name in ("obesity_crude", "obesity_std"):
        d = frames[name].dropna()
        bad = d[(d[FILES[name][1]] < 0) | (d[FILES[name][1]] > 100)]
        print(f"  {name}: min {d[FILES[name][1]].min():.2f} max "
              f"{d[FILES[name][1]].max():.2f}  out-of-range rows {len(bad)}")
    cal = frames["calories"].dropna()
    print(f"  calories: min {cal.kcal.min():.0f} max {cal.kcal.max():.0f}")
    print(f"    below 1500 kcal: {(cal.kcal < 1500).sum()} rows; "
          f"above 4200: {(cal.kcal > 4200).sum()} rows")
    g = frames["gdp"].dropna()
    print(f"  gdp pc: min {g.gdp_pc.min():,.0f} max {g.gdp_pc.max():,.0f}")


if __name__ == "__main__":
    main()
