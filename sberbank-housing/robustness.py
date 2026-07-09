"""Mix-shift robustness: is 'flat ruble prices' an artifact of district composition?

Checks, on the Jan 2013 - Jun 2015 window (Jan 2014 = 100):
  1. New-Moscow ('Poselenie ...') share of transactions over time
  2. Old-Moscow-only median psqm index
  3. District fixed-effects index (within-district demeaned log psqm by month)
"""
import numpy as np
import pandas as pd

BASE = "2014-01"
WINDOW = slice("2013-01", "2015-06")


def load():
    df = pd.read_csv("data/train.csv", parse_dates=["timestamp"],
                     usecols=["timestamp", "price_doc", "full_sq", "sub_area"])
    df = df[~df.price_doc.isin([1_000_000, 2_000_000])]
    df = df[(df.full_sq > 10) & (df.full_sq < 1000)]
    df["psqm"] = df.price_doc / df.full_sq
    lo, hi = df.psqm.quantile([0.01, 0.99])
    df = df[df.psqm.between(lo, hi)].copy()
    df["month"] = df.timestamp.dt.to_period("M").dt.to_timestamp()
    df["new_moscow"] = df.sub_area.str.startswith("Poselenie")
    return df


def index_of(series):
    return series / series.loc[BASE].iloc[0] * 100


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    df = load()

    g = df.groupby("month")
    share = g.new_moscow.mean()
    print("--- New Moscow share of monthly transactions ---")
    print((share.loc[WINDOW] * 100).round(1).resample("QS").mean().round(1).to_string())

    print("\n--- median psqm: old Moscow vs New Moscow (whole window) ---")
    print(df.loc[df.month.between("2013-01", "2015-06")]
            .groupby("new_moscow").psqm.median().round(0).to_string())

    raw = index_of(g.psqm.median()).loc[WINDOW]
    old = index_of(df[~df.new_moscow].groupby("month").psqm.median()).loc[WINDOW]

    # district fixed-effects index: demean log psqm within district, average by month
    df["lp"] = np.log(df.psqm)
    df["lp_dm"] = df.lp - df.groupby("sub_area").lp.transform("mean")
    fe = np.exp(df.groupby("month").lp_dm.mean())
    fe = index_of(fe).loc[WINDOW]

    cmp = pd.DataFrame({"raw_median": raw, "old_moscow_only": old, "fixed_effects": fe})
    print("\n--- indices, Jan 2014 = 100 (quarterly means) ---")
    print(cmp.resample("QS").mean().round(1).to_string())
    print("\n--- end values, Jun 2015 ---")
    print(cmp.iloc[-1].round(1).to_string())
    print("\n--- 2013 volatility (std of monthly index values in 2013) ---")
    print(cmp.loc["2013"].std().round(1).to_string())
