"""Post 26: re-testing a 2020 claim that Bitcoin was steadier and safer than stocks.

Implements docs/2026-10-09-safe-haven-retest-design.md as amended in its section 8:
  daily layer    Bitcoin against the S&P 500 (measures 1 to 4, FC1, FC2a, FC3)
  monthly layer  Bitcoin and gold against the S&P 500, all three as calendar-month averages
                 (measures 6 and 7, FC2b, FC3)
  Covid aside    weekly world cases (measure 5, amended)
Output: results.json. Every figure the post prints is emitted here; the prose does no arithmetic.
"""

import hashlib
import json
import math
import os

import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

SAMPLE_START = pd.Timestamp("2020-01-02")
WINDOW = (pd.Timestamp("2020-03-05"), pd.Timestamp("2020-05-05"))
WORST_DAYS, WORST_DAYS_ROBUST = 0.05, 0.01
WORST_MONTHS, WORST_MONTHS_ROBUST = 0.10, 0.20
EPISODE_FALL, EPISODE_FALL_ROBUST = 0.15, 0.10
ROLL_DAYS, ROLL_MONTHS = 90, 24
GOLD_CHECK_MONTHS = ("2025-05", "2025-06")
CONFIDENCE = 0.95

# Raw files are frozen by hash (design 8.1); a re-download needs a new vet.
FILES = {
    "sp500": ("sp500_fred.csv", "1e46a3007dc7cdd666c38175c3d1e3cbaf9fa0d5c0124a1a7f60abdee360a4a8"),
    "bitcoin": ("btc_coinmetrics_github.csv", "06495ff8e643432e6948b7b4686ce44fc106217287dabdc1b38351d9ddec46c3"),
    "gold": ("gold_worldbank_CMO-Historical-Data-Monthly.xlsx",
             "ea1c350827878ea3bbe30e3cda16a13fd3bd5b409b8458940dc94a36b5a33154"),
    "covid": ("covid_who.csv", "47afc78d45fa38929d9c66b401a222292ba4b9d4159cfe30b97d2baee7c63b2e"),
}


def path(key):
    name, digest = FILES[key]
    p = os.path.join(DATA, name)
    with open(p, "rb") as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    if got != digest:
        raise SystemExit(f"{name}: sha256 {got} is not the vetted file {digest}")
    return p


# --- readers (make_charts.py imports these, so the two scripts cannot drift) -------------------------

def read_sp500():
    """FRED SP500 daily close. Blank rows are US market holidays and are dropped."""
    d = pd.read_csv(path("sp500"), parse_dates=["observation_date"])
    s = pd.Series(pd.to_numeric(d["SP500"], errors="coerce").values, index=d["observation_date"]).dropna()
    assert s.index.is_unique and s.index.is_monotonic_increasing and (s > 0).all()
    return s.rename("sp500")


def read_bitcoin():
    """Coin Metrics PriceUSD. The value stamped D is the rate fixed at 00:00 UTC at the end of day D,
    so it is mapped to date D with no shift (design 8.1)."""
    d = pd.read_csv(path("bitcoin"), usecols=["time", "PriceUSD"], parse_dates=["time"])
    s = d.set_index("time")["PriceUSD"].dropna()
    assert s.index.is_unique and s.index.is_monotonic_increasing and (s > 0).all()
    every_day = pd.date_range(SAMPLE_START, s.index.max(), freq="D")
    assert s.reindex(every_day).notna().all(), "a calendar day is missing from the Bitcoin series"
    return s.rename("bitcoin")


def read_gold():
    """World Bank Pink Sheet, monthly average gold price in US dollars per troy ounce."""
    raw = pd.read_excel(path("gold"), sheet_name="Monthly Prices", header=None)
    cols = [c for c in raw.columns if raw.iloc[4, c] == "Gold"]
    assert len(cols) == 1 and raw.iloc[5, cols[0]] == "($/troy oz)"
    body = raw.iloc[6:, [0, cols[0]]].dropna()
    months = pd.PeriodIndex([f"{p[:4]}-{p[5:]}" for p in body[0]], freq="M")
    s = pd.Series(pd.to_numeric(body[cols[0]]).values, index=months)
    assert s.index.is_unique and s.index.is_monotonic_increasing and (s > 0).all()
    return s.rename("gold")


def read_covid_world():
    """WHO daily new cases summed over every country by date reported. Blank cells count as zero."""
    d = pd.read_csv(path("covid"), keep_default_na=False,
                    usecols=["Date_reported", "Country_code", "New_cases"])
    d["New_cases"] = pd.to_numeric(d["New_cases"].replace("", "0"))
    d["Date_reported"] = pd.to_datetime(d["Date_reported"])
    assert not d.duplicated(["Date_reported", "Country_code"]).any()
    return d, d.groupby("Date_reported")["New_cases"].sum()


# --- helpers ----------------------------------------------------------------------------------------

def sample_id(index) -> str:
    """Short hash of the dates a statistic was computed on, so the prose can tell two samples apart."""
    text = "|".join(str(x) for x in sorted(index))
    return hashlib.sha256(text.encode()).hexdigest()[:10]


def max_fall(x: pd.Series) -> float:
    """Largest peak-to-trough fall along the path, as a positive share."""
    return float((1 - x / x.cummax()).max())


def mean_test(x: pd.Series, stock_mean: float, monthly: bool) -> dict:
    """Mean return with t statistic and confidence interval, and the FC2 verdict (design 4 and 8.2)."""
    n = len(x)
    m, se = float(x.mean()), float(x.std(ddof=1) / math.sqrt(n))
    t = m / se
    half = float(stats.t.ppf(0.5 + CONFIDENCE / 2, n - 1)) * se
    lo, hi = m - half, m + half
    if monthly and lo <= 0 <= hi and lo <= stock_mean <= hi:
        verdict = "cannot tell"
    elif lo > 0:
        verdict = "strong safe haven"
    elif hi < 0:
        verdict = "not a safe haven"
    else:
        verdict = "weak safe haven"
    return dict(n=n, mean_pct=100 * m, t=t, p=float(2 * stats.t.sf(abs(t), n - 1)),
                ci_low_pct=100 * lo, ci_high_pct=100 * hi, n_up=int((x > 0).sum()),
                share_up=float((x > 0).mean()), verdict=verdict, sample=sample_id(x.index))


def worst_periods(returns: pd.DataFrame, share: float) -> pd.Series:
    """The stock index's worst periods: its lowest k returns, k = share of the periods rounded up."""
    return returns["sp500"].nsmallest(math.ceil(share * len(returns)))


def worst_test(returns: pd.DataFrame, share: float, assets, monthly=False) -> dict:
    """The asset's mean return on the stock index's worst periods, with the FC2 verdict."""
    worst = worst_periods(returns, share)
    k = len(worst)
    out = dict(share=share, k=k, n_total=len(returns), n=k, sample=sample_id(worst.index),
               sp500_mean_pct=100 * float(worst.mean()), sp500_threshold_pct=100 * float(worst.max()))
    for a in assets:
        out[a] = mean_test(returns.loc[worst.index, a], float(worst.mean()), monthly)
    return out


def correlation(a: pd.Series, b: pd.Series) -> dict:
    r, p = stats.pearsonr(a, b)
    return dict(r=float(r), p=float(p), n=len(a), sample=sample_id(a.index))


# --- daily layer ------------------------------------------------------------------------------------

def daily_prices(sp, btc):
    """S&P 500 trading days from SAMPLE_START to the last one with a Bitcoin value."""
    end = sp.index[sp.index <= btc.index.max()].max()
    days = sp.index[(sp.index >= SAMPLE_START) & (sp.index <= end)]
    f = pd.DataFrame({"sp500": sp.reindex(days), "bitcoin": btc.reindex(days)})
    assert f.notna().all().all()
    return f


PAIRINGS = (0, 1)   # two-day returns pair days from the first or the second trading day; both are reported


def log_returns(prices: pd.DataFrame, crash=None) -> pd.DataFrame:
    """Log returns between consecutive rows. With crash=(peak, trough), drop every return whose interval
    (previous date, date] overlaps the crash (peak, trough]."""
    r = np.log(prices).diff().iloc[1:]
    if crash is None:
        return r
    starts = pd.Series(prices.index[:-1], index=r.index)
    return r[~((r.index > crash[0]) & (starts < crash[1]))]


def two_day(prices: pd.DataFrame, pairing: int, crash=None) -> pd.DataFrame:
    """Non-overlapping two-day log returns: every second trading day, starting from day 'pairing'."""
    return log_returns(prices.iloc[pairing::2], crash)


def worst_days(prices, crash) -> dict:
    """FC2a and its robustness checks; the FC3 sample drops the 2020 crash, peak to trough (design 4)."""
    rets = log_returns(prices)
    out = dict(primary=worst_test(rets, WORST_DAYS, ["bitcoin"]),
               worst1=worst_test(rets, WORST_DAYS_ROBUST, ["bitcoin"]),
               without_crash=worst_test(log_returns(prices, crash), WORST_DAYS, ["bitcoin"]))
    for p in PAIRINGS:
        tag = f"pairing{p + 1}"
        out[f"two_day_{tag}"] = worst_test(two_day(prices, p), WORST_DAYS, ["bitcoin"])
        out[f"two_day_worst1_{tag}"] = worst_test(two_day(prices, p), WORST_DAYS_ROBUST, ["bitcoin"])
        out[f"two_day_without_crash_{tag}"] = worst_test(two_day(prices, p, crash), WORST_DAYS, ["bitcoin"])
    verdicts = {k: v["bitcoin"]["verdict"] for k, v in out.items()}
    differ = sorted(k for k, v in verdicts.items() if v != verdicts["primary"])
    out["robustness"] = dict(n_checks=len(verdicts) - 1, n_same=len(verdicts) - 1 - len(differ), differ=differ)
    return out


def hedge_daily(prices, rets) -> dict:
    roll = rets["bitcoin"].rolling(ROLL_DAYS).corr(rets["sp500"]).dropna()
    two = {f"two_day_pairing{p + 1}": correlation(two_day(prices, p)["bitcoin"], two_day(prices, p)["sp500"])
           for p in PAIRINGS}
    return dict(primary=correlation(rets["bitcoin"], rets["sp500"]), **two,
                rolling=dict(window=ROLL_DAYS, min=float(roll.min()), max=float(roll.max()),
                             min_date=str(roll.idxmin().date()), max_date=str(roll.idxmax().date()),
                             n=len(roll)))


def window_2020(prices, btc) -> dict:
    w = prices.loc[WINDOW[0]:WINDOW[1]]
    out = dict(n_days=len(w), n_returns=len(w) - 1, first=str(w.index[0].date()), last=str(w.index[-1].date()),
               sample=sample_id(w.index))
    for a in ["sp500", "bitcoin"]:
        x = w[a]
        low = x.idxmin()
        out[a] = dict(return_pct=100 * float(x.iloc[-1] / x.iloc[0] - 1), fall=max_fall(x),
                      daily_vol_pct=100 * float(np.log(x).diff().std(ddof=1)),
                      low_vs_start_pct=100 * float(x.min() / x.iloc[0] - 1),
                      low_day=int(low.day), low_month=int(low.month), n=len(x), sample=sample_id(w.index))
    cal = btc.loc[WINDOW[0]:WINDOW[1]]
    out["bitcoin_every_day"] = dict(n=len(cal), fall=max_fall(cal),
                                    daily_vol_pct=100 * float(np.log(cal).diff().std(ddof=1)))
    b, s = out["bitcoin"], out["sp500"]
    out["fc1"] = dict(smaller_fall=b["fall"] < s["fall"], lower_vol=b["daily_vol_pct"] < s["daily_vol_pct"])
    out["fc1"]["survives"] = out["fc1"]["smaller_fall"] and out["fc1"]["lower_vol"]
    return out


# --- episodes ---------------------------------------------------------------------------------------

def find_episodes(sp, end):
    """From a running all-time-high close to the lowest close before that high is regained (design 2).
    The running high uses the whole FRED history, so a 2020 peak is an all-time high, not a sample high."""
    s = sp[sp.index <= end]
    high = s.cummax()
    eps, cur = [], None
    for day in s.index[s.index >= SAMPLE_START]:
        if s[day] >= high[day]:
            if cur:
                cur["end"] = day
                eps.append(cur)
                cur = None
            continue
        if cur is None:
            peak_day = s.loc[:day][s.loc[:day] == high[day]].index[-1]
            cur = dict(peak=peak_day, trough=day, end=None)
        if s[day] < s[cur["trough"]]:
            cur["trough"] = day
    if cur:
        eps.append(cur)
    for e in eps:
        e["fall"] = float(1 - s[e["trough"]] / s[e["peak"]])
    return eps


def regain_days(x: pd.Series, start, stop) -> int | None:
    """Trading days from start until x is back at its start level after its lowest point between start and
    stop; 0 if it never fell below that level in the window; None if not back by the sample end."""
    window = x.loc[start:stop]
    level, low_day = window.iloc[0], window.idxmin()
    if window.min() >= level:
        return 0
    after = x.loc[low_day:]
    back = after[after >= level]
    return None if back.empty else int(x.index.get_loc(back.index[0]) - x.index.get_loc(start))


def episode_table(sp, prices) -> list:
    rows = []
    for e in find_episodes(sp, prices.index[-1]):
        if e["fall"] < EPISODE_FALL_ROBUST:
            continue
        row = dict(peak=str(e["peak"].date()), trough=str(e["trough"].date()),
                   end=None if e["end"] is None else str(e["end"].date()),
                   peak_year=int(e["peak"].year), trough_year=int(e["trough"].year),
                   primary=e["fall"] >= EPISODE_FALL, sp500_fall=e["fall"])
        for a in ["sp500", "bitcoin"]:
            seg = prices.loc[e["peak"]:e["trough"], a]     # the episode window: peak to trough (design 2)
            row[a] = dict(fall=max_fall(seg), regain_days=regain_days(prices[a], e["peak"], e["trough"]),
                          at_stock_trough_pct=100 * float(prices.loc[e["trough"], a] / prices.loc[e["peak"], a] - 1),
                          n=len(seg), sample=sample_id(seg.index))
        rows.append(row)
    return rows


# --- monthly layer ----------------------------------------------------------------------------------

def monthly_prices(sp, btc, gold) -> pd.DataFrame:
    """Calendar-month averages over the month's S&P 500 trading days; a month counts only if Bitcoin has a
    value on every one of those days and gold has a value (design 8.2)."""
    days = sp.index[sp.index >= SAMPLE_START]
    f = pd.DataFrame({"sp500": sp.reindex(days), "bitcoin": btc.reindex(days)})
    month = f.index.to_period("M")
    complete = f["bitcoin"].notna().groupby(month).all()
    avg = f.groupby(month).mean()[complete]
    avg["gold"] = gold.reindex(avg.index)
    avg = avg.dropna()
    assert (avg.index == pd.period_range(avg.index[0], avg.index[-1], freq="M")).all(), "a month is missing"
    return avg


def monthly_tests(mp) -> dict:
    rets = np.log(mp).diff().dropna()
    roll = {a: rets[a].rolling(ROLL_MONTHS).corr(rets["sp500"]).dropna() for a in ["bitcoin", "gold"]}
    keep = ~rets.index.strftime("%Y-%m").isin(GOLD_CHECK_MONTHS)
    gold_roll = rets.loc[keep, "gold"].rolling(ROLL_MONTHS).corr(rets.loc[keep, "sp500"]).dropna()

    def tests(r):
        return dict(worst10=worst_test(r, WORST_MONTHS, ["bitcoin", "gold"], monthly=True),
                    worst20=worst_test(r, WORST_MONTHS_ROBUST, ["bitcoin", "gold"], monthly=True),
                    ex2020=worst_test(r[r.index.year != 2020], WORST_MONTHS, ["bitcoin", "gold"], monthly=True),
                    hedge={a: correlation(r[a], r["sp500"]) for a in ["bitcoin", "gold"]})

    return dict(
        **tests(rets),
        gold_check=dict(**tests(rets[keep]), rolling=rolling_summary(gold_roll)),
        first_change=str(rets.index[0]), first_change_year=int(rets.index[0].year),
        rolling={a: rolling_summary(r) for a, r in roll.items()},
    ), rets, roll


def rolling_summary(r: pd.Series) -> dict:
    return dict(window=ROLL_MONTHS, n=len(r), sample=sample_id(r.index), min=float(r.min()), max=float(r.max()),
                last=float(r.iloc[-1]),
                n_negative=int((r < 0).sum()), first_month=str(r.index[0]), last_month=str(r.index[-1]),
                first_year=int(r.index[0].year))


def fc3(worst, monthly) -> dict:
    """FC3 scored: does each FC2 verdict hold without the 2020 crash (design 4 and 8.2)?"""
    def row(full, without):
        return dict(full=full, without=without, holds=full == without)
    daily = worst["primary"]["bitcoin"]["verdict"]
    out = dict(daily_bitcoin=row(daily, worst["without_crash"]["bitcoin"]["verdict"]))
    for p in PAIRINGS:
        out[f"daily_bitcoin_two_day_pairing{p + 1}"] = row(
            daily, worst[f"two_day_without_crash_pairing{p + 1}"]["bitcoin"]["verdict"])
    for a in ["bitcoin", "gold"]:
        out[f"monthly_{a}"] = row(monthly["worst10"][a]["verdict"], monthly["ex2020"][a]["verdict"])
    return out


# --- Covid aside ------------------------------------------------------------------------------------

def covid_weekly(prices, by_country, world) -> dict:
    """Weekly world cases over WHO's Monday-to-Sunday weeks, against weekly log returns measured from the
    last S&P 500 trading day of one week to the last of the next (design 8.3)."""
    weeks = world.resample("W-SUN").sum()
    last_day = prices.groupby(prices.index.to_period("W-SUN")).tail(1)
    wk = pd.DataFrame({"cases": weeks})
    wk.index = wk.index.to_period("W-SUN")
    last_day.index = last_day.index.to_period("W-SUN")
    wk = wk.join(np.log(last_day))
    wk["growth"] = np.log(wk["cases"]).diff()
    for a in ["sp500", "bitcoin"]:
        wk[a + "_ret"] = wk[a].diff()
    first, last = WINDOW[0].to_period("W-SUN"), WINDOW[1].to_period("W-SUN")
    w = wk.loc[first:last]
    assert w[["growth", "sp500_ret", "bitcoin_ret"]].notna().all().all()
    fr = by_country[(by_country.Country_code == "FR")
                    & by_country.Date_reported.between(w.index[0].start_time, w.index[-1].end_time)]
    return dict(n_weeks=len(w), first_week_end=str(w.index[0].end_time.date()),
                last_week_end=str(w.index[-1].end_time.date()),
                cases_bitcoin=correlation(w["growth"], w["bitcoin_ret"]),
                cases_sp500=correlation(w["growth"], w["sp500_ret"]),
                bitcoin_sp500=correlation(w["bitcoin_ret"], w["sp500_ret"]),
                france_cases_in_window=int(fr["New_cases"].sum()))


# --- main -------------------------------------------------------------------------------------------

def main():
    sp, btc, gold = read_sp500(), read_bitcoin(), read_gold()
    by_country, world = read_covid_world()
    prices = daily_prices(sp, btc)
    rets = log_returns(prices)
    mp = monthly_prices(sp, btc, gold)
    monthly, _, _ = monthly_tests(mp)
    eps = episode_table(sp, prices)
    crash = next((pd.Timestamp(e["peak"]), pd.Timestamp(e["trough"])) for e in eps
                 if e["primary"] and e["peak_year"] == 2020)
    worst = worst_days(prices, crash)
    in_sample = sp[(sp.index >= SAMPLE_START) & (sp.index <= prices.index[-1])]
    meta = dict(
        start=str(prices.index[0].date()), start_year=int(prices.index[0].year),
        start_month=int(prices.index[0].month), start_day=int(prices.index[0].day),
        daily_end=str(prices.index[-1].date()), daily_end_year=int(prices.index[-1].year),
        daily_end_month=int(prices.index[-1].month), daily_end_day=int(prices.index[-1].day),
        bitcoin_last=str(btc.index.max().date()), n_trading_days=len(prices), n_daily_returns=len(rets),
        n_sp500_rows_in_range=len(in_sample),
        first_month=str(mp.index[0]), last_month=str(mp.index[-1]),
        last_month_year=int(mp.index[-1].year), last_month_number=int(mp.index[-1].month),
        n_months=len(mp), n_monthly_changes=len(mp) - 1,
        gold_last_month=str(gold.index.max()), sp500_last=str(sp.index.max().date()),
        n_episodes=sum(e["primary"] for e in eps), n_episodes_robust=len(eps),
    )
    rules = dict(worst_days=WORST_DAYS, worst_days_robust=WORST_DAYS_ROBUST, worst_months=WORST_MONTHS,
                 worst_months_robust=WORST_MONTHS_ROBUST, episode_fall=EPISODE_FALL,
                 episode_fall_robust=EPISODE_FALL_ROBUST, roll_days=ROLL_DAYS, roll_months=ROLL_MONTHS,
                 confidence=CONFIDENCE)
    out = dict(meta=meta, rules=rules, window_2020=window_2020(prices, btc), worst_days=worst,
               hedge_daily=hedge_daily(prices, rets), episodes=eps, monthly=monthly, fc3=fc3(worst, monthly),
               covid=covid_weekly(prices, by_country, world))
    with open(os.path.join(BASE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=lambda v: v.item() if hasattr(v, "item") else str(v))
    report(out)


def report(out):
    """Print the full tables before any claim is written."""
    print(json.dumps(out["meta"], indent=1))
    w = out["window_2020"]
    print(f"\n2020 WINDOW {w['first']} to {w['last']}: {w['n_days']} trading days")
    for a in ["sp500", "bitcoin"]:
        x = w[a]
        print(f"  {a:8s} return {x['return_pct']:+7.2f}%  max fall {100*x['fall']:6.2f}%  "
              f"daily vol {x['daily_vol_pct']:5.2f}%  low {x['low_vs_start_pct']:+7.2f}% on {x['low_month']}-{x['low_day']}")
    print(f"  bitcoin every calendar day: fall {100*w['bitcoin_every_day']['fall']:.2f}%  "
          f"vol {w['bitcoin_every_day']['daily_vol_pct']:.2f}%   FC1 {w['fc1']}")
    print("\nWORST DAYS (daily layer)")
    for k, v in out["worst_days"].items():
        if k == "robustness":
            print(f"  robustness: {v}")
            continue
        b = v["bitcoin"]
        print(f"  {k:15s} k={v['k']:3d}/{v['n_total']:4d} sp500 {v['sp500_mean_pct']:+6.2f}%  bitcoin "
              f"{b['mean_pct']:+6.2f}% [{b['ci_low_pct']:+6.2f}, {b['ci_high_pct']:+6.2f}] t={b['t']:+5.2f} "
              f"up {b['n_up']}/{b['n']}  -> {b['verdict']}")
    h = out["hedge_daily"]
    print(f"\nHEDGE daily r={h['primary']['r']:+.3f} n={h['primary']['n']}  two-day r="
          f"{h['two_day_pairing1']['r']:+.3f} / {h['two_day_pairing2']['r']:+.3f}  rolling {h['rolling']}")
    print(f"\nEPISODES ({out['meta']['n_episodes']} at 15%, {out['meta']['n_episodes_robust']} at 10%)")
    for e in out["episodes"]:
        print(f"  {e['peak']} -> trough {e['trough']} -> end {e['end']}  S&P fall {100*e['sp500_fall']:5.1f}% "
              f"primary={e['primary']}  BTC fall {100*e['bitcoin']['fall']:5.1f}% regain {e['bitcoin']['regain_days']}  "
              f"S&P regain {e['sp500']['regain_days']}  BTC at S&P trough {e['bitcoin']['at_stock_trough_pct']:+.1f}%")
    print("\nMONTHLY LAYER")
    rows = [(k, out["monthly"][k]) for k in ["worst10", "worst20", "ex2020"]]
    rows += [("gc_" + k, out["monthly"]["gold_check"][k]) for k in ["worst10", "worst20", "ex2020"]]
    for k, v in rows:
        line = f"  {k:10s} k={v['k']}/{v['n_total']} sp500 {v['sp500_mean_pct']:+6.2f}%"
        for a in ["bitcoin", "gold"]:
            x = v[a]
            line += (f" | {a} {x['mean_pct']:+6.2f}% [{x['ci_low_pct']:+6.2f}, {x['ci_high_pct']:+6.2f}] "
                     f"up {x['n_up']}/{x['n']} {x['verdict']}")
        print(line)
    for a, c in out["monthly"]["hedge"].items():
        print(f"  hedge {a}: r={c['r']:+.3f} p={c['p']:.3f} n={c['n']}  rolling {out['monthly']['rolling'][a]}")
    print(f"  gold check rolling {out['monthly']['gold_check']['rolling']}")
    print(f"\nFC3 {json.dumps(out['fc3'], indent=1)}")
    c = out["covid"]
    print(f"\nCOVID weekly {c['first_week_end']} to {c['last_week_end']} ({c['n_weeks']} weeks): "
          f"cases~btc r={c['cases_bitcoin']['r']:+.3f}  cases~sp r={c['cases_sp500']['r']:+.3f}  "
          f"btc~sp r={c['bitcoin_sp500']['r']:+.3f}  France cases in window {c['france_cases_in_window']}")


if __name__ == "__main__":
    main()
