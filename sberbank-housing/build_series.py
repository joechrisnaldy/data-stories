"""Build the cleaned monthly series for the money-illusion analysis.

Cleaning rules (see docs/2026-07-09-money-illusion-design.md):
  1. drop declared-price fakes: price_doc exactly 1M or 2M RUB
  2. drop absurd areas: full_sq <= 10 or >= 1000
  3. psqm = price_doc / full_sq, trimmed to 1st-99th percentile
"""
import pandas as pd

CPI_BASE_MONTH = "2014-01"
INDEX_BASE = "2014-01"


def load_clean_train(path="data/train.csv"):
    df = pd.read_csv(path, parse_dates=["timestamp"],
                     usecols=["timestamp", "price_doc", "full_sq", "product_type"])
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
    return m


def monthly_macro(path="data/macro.csv"):
    macro = pd.read_csv(path, parse_dates=["timestamp"])
    cols = ["usdrub", "cpi", "salary", "deposits_rate", "oil_urals", "mortgage_rate"]
    return macro.set_index("timestamp")[cols].resample("MS").mean()


def build(train_path="data/train.csv", macro_path="data/macro.csv"):
    df = load_clean_train(train_path)
    m = monthly_housing(df).join(monthly_macro(macro_path), how="left")

    m["psqm_usd"] = m.psqm / m.usdrub
    m["psqm_real"] = m.psqm / (m.cpi / m.loc[CPI_BASE_MONTH, "cpi"].iloc[0])
    m["sqm_per_salary"] = m.salary / m.psqm

    base = m.loc[INDEX_BASE].iloc[0]
    for col in ["psqm", "psqm_usd", "psqm_real"]:
        m[f"idx_{col}"] = m[col] / base[col] * 100
    return m


def counterfactual(m, start="2014-01", capital=1_000_000):
    """Value of 1M RUB placed in housing / USD cash / ruble deposit at `start`."""
    cf = m.loc[start:].copy()
    s = cf.iloc[0]
    cf["housing"] = capital * cf.psqm / s.psqm
    cf["usd_cash"] = capital * cf.usdrub / s.usdrub
    monthly_rate = cf.deposits_rate.shift(1).fillna(s.deposits_rate) / 100 / 12
    cf["deposit"] = capital * (1 + monthly_rate).cumprod()
    cf["cpi_needed"] = capital * cf.cpi / s.cpi  # value needed just to keep pace with CPI
    return cf[["housing", "usd_cash", "deposit", "cpi_needed"]]


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    m = build()

    print("\n--- quarterly view of the story ---")
    q = m[["psqm", "psqm_usd", "psqm_real", "sqm_per_salary", "n_sales", "usdrub", "deposits_rate"]]
    print(q.resample("QS").mean().round(1).to_string())

    print("\n--- indexed (Jan 2014 = 100): where each series ends (Jun 2015) ---")
    print(m[["idx_psqm", "idx_psqm_usd", "idx_psqm_real"]].iloc[-1].round(1).to_string())

    print("\n--- peak-to-end for USD series ---")
    peak = m.idx_psqm_usd.idxmax()
    print(f"USD-terms peak: {peak:%Y-%m} at {m.idx_psqm_usd.max():.1f}; "
          f"Jun 2015: {m.idx_psqm_usd.iloc[-1]:.1f} "
          f"({(m.idx_psqm_usd.iloc[-1] / m.idx_psqm_usd.max() - 1) * 100:+.1f}%)")

    print("\n--- counterfactual: 1M RUB from Jan 2014 (values in RUB) ---")
    cf = counterfactual(m)
    print(cf.resample("QS").last().round(0).to_string())

    print("\n--- volume check: monthly sales 2014 vs 2015 ---")
    print(m.n_sales.loc["2014":].to_string())

    print("\n--- salary series variation check ---")
    print(m.salary.resample("QS").first().round(0).to_string())
