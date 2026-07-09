"""Build the cleaned monthly series for the money-illusion analysis.

Cleaning rules (see docs/2026-07-09-money-illusion-design.md):
  1. drop declared-price fakes: price_doc exactly 1M or 2M RUB
  2. drop absurd areas: full_sq <= 10 or >= 1000
  3. psqm = price_doc / full_sq, trimmed to 1st-99th percentile

Headline price series (user decision 2026-07-09): district fixed-effects
index (within-district demeaned log psqm averaged by month) which controls
for the New Moscow composition artifact. Anchored to the Jan 2014 citywide
median so charts read in rubles. Raw median kept for robustness/affordability.
"""
import numpy as np
import pandas as pd

CPI_BASE_MONTH = "2014-01"
INDEX_BASE = "2014-01"


def load_clean_train(path="data/train.csv"):
    df = pd.read_csv(path, parse_dates=["timestamp"],
                     usecols=["timestamp", "price_doc", "full_sq", "product_type",
                              "sub_area"])
    n0 = len(df)
    df = df[~df.price_doc.isin([1_000_000, 2_000_000])]
    n1 = len(df)
    df = df[(df.full_sq > 10) & (df.full_sq < 1000)]
    n2 = len(df)
    df["psqm"] = df.price_doc / df.full_sq
    lo, hi = df.psqm.quantile([0.01, 0.99])
    df = df[df.psqm.between(lo, hi)]
    n3 = len(df)
    print(f"rows: {n0:,} -> drop 1M/2M fakes -> {n1:,} -> area filter -> {n2:,} "
          f"-> psqm trim [{lo:,.0f}, {hi:,.0f}] -> {n3:,}")
    return df


def monthly_housing(df):
    m = df.set_index("timestamp").resample("MS").agg(
        psqm=("psqm", "median"), n_sales=("psqm", "size"))
    # district fixed-effects index: within-district demeaned log psqm by month
    lp_dm = np.log(df.psqm) - df.groupby("sub_area").psqm.transform(
        lambda s: np.log(s).mean())
    fe = np.exp(lp_dm.groupby(df.timestamp.dt.to_period("M").dt.to_timestamp()).mean())
    m["fe_raw"] = fe
    return m


def monthly_macro(path="data/macro.csv"):
    macro = pd.read_csv(path, parse_dates=["timestamp"])
    cols = ["usdrub", "cpi", "salary", "deposits_rate", "oil_urals", "mortgage_rate"]
    return macro.set_index("timestamp")[cols].resample("MS").mean()


def build(train_path="data/train.csv", macro_path="data/macro.csv"):
    df = load_clean_train(train_path)
    m = monthly_housing(df).join(monthly_macro(macro_path), how="left")

    base = m.loc[INDEX_BASE].iloc[0]
    # headline: mix-adjusted price level, FE index anchored to Jan 2014 median
    m["psqm_adj"] = m.fe_raw / base.fe_raw * base.psqm
    m["psqm_usd"] = m.psqm_adj / m.usdrub
    m["psqm_real"] = m.psqm_adj / (m.cpi / m.loc[CPI_BASE_MONTH, "cpi"].iloc[0])
    # affordability on the same mix-adjusted level for cross-chart consistency
    m["sqm_per_salary"] = m.salary / m.psqm_adj

    base = m.loc[INDEX_BASE].iloc[0]
    for col in ["psqm", "psqm_adj", "psqm_usd", "psqm_real"]:
        m[f"idx_{col}"] = m[col] / base[col] * 100
    return m


def counterfactual(m, start="2014-01", capital=1_000_000):
    """Value of 1M RUB placed in housing / USD cash / ruble deposit at `start`."""
    cf = m.loc[start:].copy()
    s = cf.iloc[0]
    cf["housing"] = capital * cf.psqm_adj / s.psqm_adj
    cf["usd_cash"] = capital * cf.usdrub / s.usdrub
    monthly_rate = cf.deposits_rate.shift(1).fillna(s.deposits_rate) / 100 / 12
    cf["deposit"] = capital * (1 + monthly_rate).cumprod()
    cf["cpi_needed"] = capital * cf.cpi / s.cpi  # value needed just to keep pace with CPI
    return cf[["housing", "usd_cash", "deposit", "cpi_needed"]]


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    m = build()

    print("\n--- quarterly view of the story (psqm_adj = mix-adjusted level) ---")
    q = m[["psqm", "psqm_adj", "psqm_usd", "psqm_real", "sqm_per_salary", "n_sales",
           "usdrub", "deposits_rate"]]
    print(q.resample("QS").mean().round(1).to_string())

    print("\n--- indexed (Jan 2014 = 100): where each series ends (Jun 2015) ---")
    print(m[["idx_psqm", "idx_psqm_adj", "idx_psqm_usd", "idx_psqm_real"]]
          .iloc[-1].round(1).to_string())

    print("\n--- counterfactual: 1M RUB from Jan 2014 (values in RUB) ---")
    cf = counterfactual(m)
    print(cf.resample("QS").last().round(0).to_string())

    print("\n--- volume check: monthly sales 2014 vs 2015 ---")
    print(m.n_sales.loc["2014":].to_string())

    print("\n--- salary series variation check ---")
    print(m.salary.resample("QS").first().round(0).to_string())
