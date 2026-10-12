"""Dataset vet profile for Post 26: the structural checks behind the go/no-go, rerunnable.

Reads the raw files through build_analysis's readers, which assert each file's SHA-256 against the
vetted copy, then prints coverage, gaps and duplicates. The full vet (two rounds, each verdict attacked
by an independent verifier) is recorded in data/README.md and docs/provenance-audit.md.
"""

import pandas as pd

from build_analysis import SAMPLE_START, read_bitcoin, read_covid_world, read_gold, read_sp500

sp, btc, gold = read_sp500(), read_bitcoin(), read_gold()
by_country, world = read_covid_world()

print(f"S&P 500   {sp.index.min().date()} to {sp.index.max().date()}  rows {len(sp)}  "
      f"weekend rows {(sp.index.dayofweek >= 5).sum()}  longest gap {sp.index.to_series().diff().max().days} days")
every = pd.date_range(SAMPLE_START, btc.index.max(), freq="D")
print(f"Bitcoin   {btc.index.min().date()} to {btc.index.max().date()}  rows {len(btc)}  "
      f"missing calendar days since sample start {btc.reindex(every).isna().sum()}")
months = pd.period_range(gold.index.min(), gold.index.max(), freq="M")
print(f"Gold      {gold.index.min()} to {gold.index.max()}  months {len(gold)}  missing months "
      f"{len(months.difference(gold.index))}  range in sample {gold[gold.index >= '2020-01'].min():.0f} "
      f"to {gold[gold.index >= '2020-01'].max():.0f} dollars per troy ounce")
print(f"WHO       {world.index.min().date()} to {world.index.max().date()}  country-days {len(by_country)}  "
      f"countries {by_country.Country_code.nunique()}  negative new-case rows {(by_country.New_cases < 0).sum()}")
