"""Data profile for Post 32: the American Time Use Survey 2003-24 activity summary file.

data/atussum-0324.zip is frozen by its SHA-256 (docs/data-README.src.md says where it comes from); a file that
does not match stops the script. Every variable used here is defined in docs/provenance-audit.md. The one sample
rule lives here (sample()), and build_analysis.py imports it, so no second filter can disagree with it. Run on its
own, this prints the file's checks and the coverage of the sample: python3 profile_data.py
"""
import hashlib
import os
import zipfile

import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_ZIP = ("atussum-0324.zip", "bf39ac14710ab4850c88e3cfc41c6b527bdfb7828549e0f7ccbe889e1d2922a8")
MEMBER = "atussum_0324.dat"
PERSON = ["TUCASEID", "TUYEAR", "TELFS", "TEHRUSLT", "TEAGE", "TUFNWGTP", "TU20FWGT", "TUDIARYDAY", "TRHOLIDAY"]
SLEEP = "t0101"         # lexicon 0101 Sleeping: 010101 Sleeping, 010102 Sleeplessness, 010199 n.e.c.
SPORTS = "t1301"        # lexicon 1301 Participating in Sports, Exercise, and Recreation
PANDEMIC_YEAR = 2020    # TUFNWGTP is missing for this year; the data dictionary says to use TU20FWGT
YEARS = (2015, 2024)    # the latest ten years in the file
AGES = (18, 64)
AT_WORK = 1             # TELFS 1: Employed - at work
HOURS_VARY = -4         # TEHRUSLT -4: Hours vary
WEEKDAYS = (2, 3, 4, 5, 6)   # TUDIARYDAY 2 Monday to 6 Friday
BANDS = ((1, 34, "1 to 34"), (35, 40, "35 to 40"), (41, 49, "41 to 49"), (50, 59, "50 to 59"),
         (60, 999, "60 or more"))


def data_path() -> str:
    name, digest = DATA_ZIP
    path = os.path.join(BASE, "data", name)
    with open(path, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != digest:
            raise SystemExit(f"{path} does not match its frozen SHA-256; see docs/data-README.src.md")
    return path


def weights(d: pd.DataFrame) -> pd.Series:
    """TUFNWGTP, except for the pandemic year, whose cases use TU20FWGT (the data dictionary's rule)."""
    return d["TUFNWGTP"].where(d["TUYEAR"] != PANDEMIC_YEAR, d["TU20FWGT"])


def read(all_columns: bool = False) -> pd.DataFrame:
    """The respondents, with the person variables and the minutes of each sleep and sports activity code."""
    def wanted(col: str) -> bool:
        return all_columns or col in PERSON or col.startswith((SLEEP, SPORTS))
    with zipfile.ZipFile(data_path()) as z, z.open(MEMBER) as f:
        d = pd.read_csv(f, usecols=wanted)
    weight = weights(d)
    sleep = d[[c for c in d.columns if c.startswith(SLEEP)]].sum(axis=1)
    sports = d[[c for c in d.columns if c.startswith(SPORTS)]].sum(axis=1)
    return pd.concat([d, pd.DataFrame({"weight": weight, "sleep_min": sleep, "sports_min": sports})], axis=1)


def band(hours: pd.Series) -> pd.Series:
    labels = pd.Series(pd.NA, index=hours.index, dtype="object")
    for low, high, label in BANDS:
        labels = labels.mask(hours.between(low, high), label)
    return labels


def sample(d: pd.DataFrame) -> tuple:
    """The post's sample: employed and at work, aged 18 to 64, diaries from 2015 to 2024, usual weekly hours of at
    least one, and a positive weight. Returns the kept rows with their band and the rows dropped at each step."""
    steps = (
        ("not_at_work", "not employed and at work", d["TELFS"] == AT_WORK),
        ("outside_ages", "aged outside the age range", d["TEAGE"].between(*AGES)),
        ("outside_years", "diary year outside the year range", d["TUYEAR"].between(*YEARS)),
        ("hours_vary", "usual hours vary", d["TEHRUSLT"] != HOURS_VARY),
        ("no_hours", "usual hours of zero or not reported", d["TEHRUSLT"] >= 1),
        ("no_weight", "no positive weight", d["weight"] > 0),
    )
    dropped, keep = [], pd.Series(True, index=d.index)
    for key, reason, rule in steps:
        dropped.append((key, reason, int((keep & ~rule).sum())))
        keep &= rule
    kept = pd.concat([d[keep], band(d.loc[keep, "TEHRUSLT"]).rename("band")], axis=1)
    if kept["band"].isna().any():
        raise SystemExit("a kept respondent falls in no hours band")
    return kept, dropped


def sample_id(ids) -> str:
    """A short hash of the respondents a statistic was computed on, so prose can pair figures from one sample."""
    return hashlib.sha256(",".join(map(str, sorted(ids))).encode()).hexdigest()[:12]


def main() -> None:
    d = read(all_columns=True)
    activity = [c for c in d.columns if len(c) == 7 and c[0] == "t" and c[1:].isdigit()]
    minutes = d[activity].sum(axis=1)
    print(f"respondents {len(d):,}; TUCASEID unique: {d['TUCASEID'].is_unique}; years {d['TUYEAR'].min()} to "
          f"{d['TUYEAR'].max()}; activity columns {len(activity)}")
    print(f"diaries not summing to 1,440 minutes: {int((minutes != 1440).sum())}; negative minutes: "
          f"{int((d[activity] < 0).sum().sum())}")
    print(f"{PANDEMIC_YEAR}: TUFNWGTP positive {int((d.loc[d.TUYEAR == PANDEMIC_YEAR, 'TUFNWGTP'] > 0).sum())}, "
          f"TU20FWGT positive {int((d.loc[d.TUYEAR == PANDEMIC_YEAR, 'TU20FWGT'] > 0).sum())}")
    kept, dropped = sample(d)
    for _, reason, n in dropped:
        print(f"dropped {n:>7,}  {reason}")
    print(f"kept {len(kept):,}")
    print(kept.groupby("band", sort=False).size().reindex([b[2] for b in BANDS]).to_string())


if __name__ == "__main__":
    main()
