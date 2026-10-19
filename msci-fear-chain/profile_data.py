"""Dataset vet profile for Post 27: the structural checks behind the go/no-go, rerunnable.

Reads the raw files through build_analysis's readers, which assert each file's SHA-256 against the vetted
copy, then prints coverage, gaps and duplicates. The vet, the month-by-month IHSG checks and every source's
terms are recorded in docs/provenance-audit.md and docs/ihsg-checks/.
"""

import pandas as pd

from build_analysis import (month_end, read_bop, read_cpi, read_idx_daily, read_ihsg, read_ojk_daily,
                            read_ojk_weekly, read_rupiah)

ihsg, prelim = read_ihsg()
rupiah, last_bis = read_rupiah()
bop, cpi = read_bop(), read_cpi()
ojk, weekly, idx = read_ojk_daily(), read_ojk_weekly(), read_idx_daily()

print(f"IHSG month-end  {ihsg.index[0]} to {ihsg.index[-1]}  months {len(ihsg)}  missing 0 by construction  "
      f"preliminary {prelim}")
gaps = rupiah.index.to_series().diff().dt.days
print(f"Rupiah daily    {rupiah.index[0].date()} to {rupiah.index[-1].date()}  rows {len(rupiah)}  "
      f"last BIS {last_bis.date()}  longest gap {gaps.max():.0f} days  complete months {len(month_end(rupiah))}")
print(f"BoP equity      {bop.index[0]} to {bop.index[-1]}  quarters {len(bop)}  "
      f"missing {len(pd.period_range(bop.index[0], bop.index[-1], freq='Q').difference(bop.index))}")
print(f"CPI headline    {cpi.index[0]} to {cpi.index[-1]}  months {len(cpi)}  missing 0 by construction")
print(f"OJK daily IHSG  {ojk.index[0].date()} to {ojk.index[-1].date()}  rows {len(ojk)}")
print(f"OJK weekly      {weekly.index[0]} to {weekly.index[-1]}  weeks {len(weekly)}")
print(f"IDX daily       {idx.index[0].date()} to {idx.index[-1].date()}  rows {len(idx)}")
