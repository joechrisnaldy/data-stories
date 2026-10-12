"""Charts for Post 26, the re-test of a 2020 claim that Bitcoin was steadier and safer than stocks.

Reads results.json and the data through build_analysis's own readers and helpers, so the two scripts
cannot drift. Output: charts/sh-N-name.png.

Every number drawn or written here comes from results.json. Typed literals are limited to axis limits,
layout coordinates and fixed source labels.

House rule: no em or en dashes anywhere, including inside rendered images; axes.unicode_minus is off.
After editing any caption, re-open the PNG and look at it.
"""

import calendar
import json
import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from build_analysis import (WINDOW, daily_prices, monthly_prices, read_bitcoin, read_gold, read_sp500,
                            worst_periods)

BASE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(BASE, "results.json")))
META, RULES = R["meta"], R["rules"]

BLUE, AMBER, GOLD = "#2a78d6", "#e8890c", "#b8901f"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
COLOR = {"sp500": BLUE, "bitcoin": AMBER, "gold": GOLD}
NAME = {"sp500": "S&P 500", "bitcoin": "Bitcoin", "gold": "Gold"}

SRC_SP = "S&P 500: S&P Dow Jones Indices LLC via FRED. Copyright \u00a9 2016, S&P Dow Jones Indices LLC. All rights reserved."
SRC_BTC = "Bitcoin: Coin Metrics Community data (PriceUSD), licensed CC BY-NC 4.0."
SRC_GOLD = ("Gold: The World Bank: World Bank Commodity Price Data (The Pink Sheet): Bloomberg Finance L.P.; "
            "Kitco.com; International Monetary Fund, International Financial Statistics; London Bullion Market; "
            "Metals Week; Platts Metals Week; Shearson Lehman Brothers, Metal Market Weekly Review; Thomson Reuters "
            "Datastream; World Bank. Monthly averages, licensed CC BY 4.0.")
CHANGED = "Each series transformed by the author."

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": BASELINE, "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": INK2,
    "text.color": INK, "axes.titlesize": 11.5, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "font.size": 10.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "text.parse_math": False, "axes.unicode_minus": False,
})


def save(fig, name):
    fig.savefig(os.path.join(BASE, "charts", name), dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def footnote(fig, text, y=-0.02):
    fig.text(0.0, y, text, ha="left", va="top", fontsize=8.4, color=MUTED, wrap=True)


def pct(v, places=1):
    return f"{v:+.{places}f}%"


def month_name(iso: str) -> str:
    return calendar.month_name[int(iso[5:7])]


def sample_dates() -> str:
    return (f"{META['start_day']} {calendar.month_name[META['start_month']]} {META['start_year']} to "
            f"{META['daily_end_day']} {calendar.month_name[META['daily_end_month']]} {META['daily_end_year']}")


# --- sh-1 -------------------------------------------------------------------------------------------

def chart_window(prices):
    w = prices.loc[WINDOW[0]:WINDOW[1]]
    idx = 100 * w / w.iloc[0]
    res = R["window_2020"]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    for a in ["sp500", "bitcoin"]:
        ax.plot(idx.index, idx[a], color=COLOR[a], lw=2.2, label=NAME[a])
        low = idx[a].idxmin()
        ax.scatter([low], [idx[a].min()], color=COLOR[a], s=36, zorder=3)
        if a == "bitcoin":
            ax.annotate(f"{NAME[a]}'s largest fall: {100 * res[a]['fall']:.0f}%", (low, idx[a].min()),
                        xytext=(8, -14), textcoords="offset points", color=COLOR[a], fontsize=10,
                        fontweight="bold", va="top")
        else:
            ax.annotate(f"{NAME[a]}'s largest fall: {100 * res[a]['fall']:.0f}%", (low, idx[a].min()),
                        xytext=(low + pd.Timedelta(days=10), 63), color=COLOR[a], fontsize=10, fontweight="bold",
                        arrowprops=dict(arrowstyle="-", color=COLOR[a], lw=0.9))
        ax.scatter([idx.index[-1]], [idx[a].iloc[-1]], color=COLOR[a], s=36, zorder=3)
        ax.annotate(f"{pct(res[a]['return_pct'])} at the end", (idx.index[-1], idx[a].iloc[-1]),
                    xytext=(8, 4 if a == "bitcoin" else -4), textcoords="offset points",
                    color=COLOR[a], fontsize=10, va="bottom" if a == "bitcoin" else "top")
    for day in (idx.index[0], idx.index[-1]):
        ax.axvline(day, color=INK2, lw=1, ls=":")
    ax.text(idx.index[0], ax.get_ylim()[1], "  my 2020 draft's window", color=INK2,
            fontsize=9.5, va="top")
    ax.axhline(100, color=BASELINE, lw=1)
    ax.set_xlim(idx.index[0] - pd.Timedelta(days=2), idx.index[-1] + pd.Timedelta(days=13))
    ax.set_ylim(48, None)
    ax.set_ylabel("Value, indexed to 100 on the first day")
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%-d %b"))
    ax.legend(loc="lower right", frameon=False)
    ax.set_title("Both dates said Bitcoin held up; the path between them said otherwise", loc="left")
    footnote(fig, f"Daily values on the {res['n_days']} S&P 500 trading days from 5 March to 5 May 2020. "
                  f"Bitcoin is the Coin Metrics reference rate at the end of each UTC day.\n"
                  f"{SRC_SP}\n{SRC_BTC} {CHANGED}")
    save(fig, "sh-1-window.png")


# --- sh-2 -------------------------------------------------------------------------------------------

def strip(ax, values, color, mean, lo, hi, stock_mean, n, unit):
    order = np.argsort(values)
    x = ((np.arange(len(values)) % 7) - 3) * 0.045
    ax.scatter(x, np.asarray(values)[order], color=color, s=16, alpha=0.75, zorder=3)
    ax.hlines(mean, -0.32, 0.32, color=color, lw=3, zorder=4)
    ax.vlines(0.38, lo, hi, color=color, lw=2)
    ax.axhline(stock_mean, color=BLUE, lw=1.4, ls="--")
    ax.axhline(0, color=INK2, lw=0.9)
    ax.text(0.5, mean, f"average {pct(mean)}", color=color, fontsize=9.5, va="center", fontweight="bold")
    ax.text(0.5, stock_mean, f"S&P 500\naverage {pct(stock_mean)}", color=BLUE, fontsize=9,
            va="bottom" if stock_mean > mean else "top")
    ax.text(0.97, 0.98, f"n = {n} {unit}", fontsize=9, color=INK2, ha="right", va="top", transform=ax.transAxes)
    ax.set_xlim(-0.4, 1.45)
    ax.set_xticks([])


def chart_worst(prices, mp):
    rets = np.log(prices).diff().dropna()
    mrets = np.log(mp).diff().dropna()
    wd, wm = worst_periods(rets, RULES["worst_days"]), worst_periods(mrets, RULES["worst_months"])
    day, mon = R["worst_days"]["primary"], R["monthly"]["worst10"]
    fig = plt.figure(figsize=(11, 5.4))
    ax0 = fig.add_subplot(1, 3, 1)
    ax1 = fig.add_subplot(1, 3, 2)
    ax2 = fig.add_subplot(1, 3, 3, sharey=ax1)
    b = day["bitcoin"]
    strip(ax0, 100 * rets.loc[wd.index, "bitcoin"].values, AMBER, b["mean_pct"], b["ci_low_pct"],
          b["ci_high_pct"], day["sp500_mean_pct"], day["k"], "days")
    ax0.set_title(f"Bitcoin on the S&P 500's\nworst {100 * RULES['worst_days']:.0f}% of days", loc="left")
    ax0.set_ylabel("Log return in the period (%)")
    for ax, a in ((ax1, "bitcoin"), (ax2, "gold")):
        x = mon[a]
        strip(ax, 100 * mrets.loc[wm.index, a].values, COLOR[a], x["mean_pct"], x["ci_low_pct"],
              x["ci_high_pct"], mon["sp500_mean_pct"], mon["k"], "months")
        ax.set_title(f"{NAME[a]} in the S&P 500's worst\n{100 * RULES['worst_months']:.0f}% of months (monthly averages)",
                     loc="left")
    fig.suptitle("On the S&P 500's worst days and months, Bitcoin fell too",
                 x=0.0, ha="left", fontsize=12.5, fontweight="bold", y=1.04)
    footnote(fig, f"Dots: each period's return; thick bar: the average; thin bar: its "
                  f"{100 * RULES['confidence']:.0f}% confidence interval; dashed line: the S&P 500's own average "
                  f"in the same periods. Daily: log returns on S&P 500 trading days, {sample_dates()}. Monthly: "
                  f"log changes in calendar-month averages; the bottom {mon['k']} of the S&P 500's "
                  f"{META['n_monthly_changes']} monthly changes. The daily panel has its own scale.\n"
                  f"{SRC_SP}\n{SRC_BTC}\n{SRC_GOLD} {CHANGED}")
    save(fig, "sh-2-safe-haven-test.png")


# --- sh-3 -------------------------------------------------------------------------------------------

def chart_episodes():
    eps = [e for e in R["episodes"] if e["primary"]]
    fig, ax = plt.subplots(figsize=(9.5, 1.6 + 1.25 * len(eps)))
    labels = []
    for i, e in enumerate(eps):
        for j, a in enumerate(["sp500", "bitcoin"]):
            y = i * 3 + j
            fall = 100 * e[a]["fall"]
            ax.barh(y, fall, color=COLOR[a], height=0.8, label=NAME[a] if i == 0 else None)
            days = e[a]["regain_days"]
            back = "not back by the sample end" if days is None else f"back in {days} trading days"
            ax.text(fall + 1, y, f"fell {fall:.0f}%, {back}", va="center", fontsize=9.5, color=COLOR[a])
        labels.append((i * 3 + 0.5, f"{month_name(e['peak'])} {e['peak_year']}\nto {month_name(e['trough'])} "
                                    f"{e['trough_year']}"))
    ax.set_yticks([p for p, _ in labels], [t for _, t in labels])
    ax.invert_yaxis()
    ax.set_xlabel("Largest fall between the S&P 500's high and its low (%)")
    ax.set_xlim(0, 100)
    ax.grid(axis="y", visible=False)
    ax.legend(loc="lower right", frameon=False)
    ax.set_title(f"In each S&P 500 fall of {100 * RULES['episode_fall']:.0f}% or more, Bitcoin fell further",
                 loc="left")
    footnote(fig, f"Episodes: each fall of {100 * RULES['episode_fall']:.0f}% or more from an S&P 500 all-time high "
                  f"since {META['start_year']}, from the high to the S&P 500's lowest close before the high was "
                  f"regained. 'Back' counts S&P 500 trading days from the high until the asset closed at or above "
                  f"its level on that day, after its lowest point in the episode. Gold is not drawn: its series "
                  f"here is the World Bank's monthly average.\n{SRC_SP}\n{SRC_BTC} {CHANGED}")
    save(fig, "sh-3-episodes.png")


# --- sh-4 -------------------------------------------------------------------------------------------

def chart_rolling(mp):
    mrets = np.log(mp).diff().dropna()
    n = RULES["roll_months"]
    fig, ax = plt.subplots(figsize=(9, 5))
    for a in ["bitcoin", "gold"]:
        r = mrets[a].rolling(n).corr(mrets["sp500"]).dropna()
        t = r.index.to_timestamp()
        ax.plot(t, r.values, color=COLOR[a], lw=2.2)
        ax.text(t[-1], r.iloc[-1], f"  {NAME[a]}", color=COLOR[a], va="center", fontweight="bold")
    ax.axhline(0, color=INK2, lw=0.9)
    ax.set_ylim(-1, 1)
    ax.set_ylabel(f"Correlation with the S&P 500\nover the previous {n} months")
    h = R["monthly"]["hedge"]
    m = R["monthly"]
    ax.text(0.01, 0.04, f"Whole period, {month_name(m['first_change'] + '-')} {m['first_change_year']} to "
                        f"{month_name(META['last_month'] + '-')} {META['last_month_year']} ({h['bitcoin']['n']} "
                        f"monthly changes): Bitcoin r = {h['bitcoin']['r']:.2f}, gold r = {h['gold']['r']:.2f}",
            transform=ax.transAxes, fontsize=9.5, color=INK2)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_title(f"Over {n}-month windows, Bitcoin's link with stocks stayed positive; gold's came and went",
                 loc="left")
    footnote(fig, f"Correlation of log changes in calendar-month averages over a rolling {n}-month window; "
                  f"windows ending "
                  f"{month_name(R['monthly']['rolling']['bitcoin']['first_month'] + '-')} "
                  f"{R['monthly']['rolling']['bitcoin']['first_year']} "
                  f"to {month_name(META['last_month'] + '-')} {META['last_month_year']}.\n"
                  f"{SRC_SP}\n{SRC_BTC}\n{SRC_GOLD} {CHANGED}", y=-0.04)
    save(fig, "sh-4-rolling.png")


def main():
    os.makedirs(os.path.join(BASE, "charts"), exist_ok=True)
    sp, btc, gold = read_sp500(), read_bitcoin(), read_gold()
    prices = daily_prices(sp, btc)
    mp = monthly_prices(sp, btc, gold)
    chart_window(prices)
    chart_worst(prices, mp)
    chart_episodes()
    chart_rolling(mp)


if __name__ == "__main__":
    main()
