"""Vet + explore QLmonthly (Ellieroth & Michaud, Minneapolis Fed), quits and layoffs from CPS microdata.
Files from github.com/qlmonthly/Data. Variables (per the project's data page):
  eqall_seats          Employment-to-NonEmployment QUITS, % of employed, seasonally adjusted
  elall_seats          Employment-to-NonEmployment LAYOFFS, % of employed, seasonally adjusted
  share_layoff_n_seats share of newly LAID-OFF workers flowing to Non-participation (vs Unemployment)
  share_quit_n_seats   share of newly QUIT workers flowing to Non-participation (vs Unemployment)
Realism checks: does it show the actual recessions, and does COVID look like COVID."""
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")
BASE = Path(__file__).resolve().parent
prime = pd.read_stata(BASE / "data" / "qlmonthly_prime.dta").assign(grp="prime 25-55")
allw = pd.read_stata(BASE / "data" / "qlmonthly_all.dta").assign(grp="all 16+")

for name, df in [("PRIME AGE", prime), ("ALL WORKERS", allw)]:
    print(f"=== {name}: {df.shape[0]} months, {df.time.min():%Y-%m} to {df.time.max():%Y-%m} | "
          f"missing {int(df.isna().sum().sum())} ===")

d = prime.set_index("time")
print("\n=== REALISM CHECK: do the recessions show up? ===")
# NBER recessions since 1978
REC = {"1980 recession": ("1980-01", "1980-07"), "1981-82 recession": ("1981-07", "1982-11"),
       "1990-91 recession": ("1990-07", "1991-03"), "2001 recession": ("2001-03", "2001-11"),
       "Great Recession": ("2007-12", "2009-06"), "COVID": ("2020-02", "2020-04")}
base = d.elall_seats.mean()
print(f"  mean prime-age layoff rate over the whole sample: {base:.3f}% of employed per month")
for label, (a, b) in REC.items():
    w = d.loc[a:b]
    print(f"  {label:20s} peak layoffs {w.elall_seats.max():5.3f}%  "
          f"(vs {base:.3f} average)  = {w.elall_seats.max()/base:4.2f}x")

print("\n=== COVID, month by month (should be violent and unmistakable) ===")
print(d.loc["2020-01":"2020-08"][["eqall_seats", "elall_seats"]].round(3).to_string())

print("\n=== THE HEADLINE STRUCTURAL FACT ===")
print("  share of newly separated workers who leave the LABOR FORCE entirely")
print("  (rather than becoming officially 'unemployed'):")
for lbl, df2 in [("prime age 25-55", prime), ("all workers 16+", allw)]:
    x = df2.set_index("time")
    print(f"\n  {lbl}:")
    print(f"    laid-off workers going to non-participation: mean {x.share_layoff_n_seats.mean()*100:.1f}%"
          f"  (min {x.share_layoff_n_seats.min()*100:.0f}%, max {x.share_layoff_n_seats.max()*100:.0f}%)")
    print(f"    quitters going to non-participation:         mean {x.share_quit_n_seats.mean()*100:.1f}%"
          f"  (min {x.share_quit_n_seats.min()*100:.0f}%, max {x.share_quit_n_seats.max()*100:.0f}%)")

print("\n=== quits vs layoffs: which is bigger, and when does that flip? ===")
d2 = prime.set_index("time")
d2["quit_minus_layoff"] = d2.eqall_seats - d2.elall_seats
by_dec = d2.groupby(d2.index.year // 10 * 10)[["eqall_seats", "elall_seats"]].mean().round(3)
by_dec["quits_exceed_layoffs"] = (by_dec.eqall_seats > by_dec.elall_seats)
print(by_dec.to_string())
flips = d2[d2.quit_minus_layoff < 0]
print(f"\n  months where layoffs EXCEEDED quits: {len(flips)} of {len(d2)} ({len(flips)/len(d2)*100:.0f}%)")
print(f"  most recent 6 months:")
print(d2.tail(6)[["eqall_seats", "elall_seats", "share_layoff_n_seats"]].round(3).to_string())

print("\n=== the Great Resignation, and now ===")
for lbl, a, b in [("2019 (pre-COVID)", "2019-01", "2019-12"),
                  ("2021-22 Great Resignation", "2021-01", "2022-12"),
                  ("last 12 months", "2025-07", "2026-06")]:
    w = d2.loc[a:b]
    print(f"  {lbl:26s} quits {w.eqall_seats.mean():.3f}%  layoffs {w.elall_seats.mean():.3f}%  "
          f"laid-off leaving labor force {w.share_layoff_n_seats.mean()*100:.0f}%")
