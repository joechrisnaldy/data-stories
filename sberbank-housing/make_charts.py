"""Charts for the money-illusion post. Style follows the dataviz palette:
entity colors fixed across charts, single axis per chart, direct labels,
recessive grid. Output: charts/*.png (light surface).
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

from build_series import build, counterfactual

# palette roles
BLUE, AQUA, YELLOW = "#2a78d6", "#1baf7a", "#eda100"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"

CRASH = pd.Timestamp("2014-12-01")  # ruble crash month
WINDOW = slice("2013-01", "2015-06")

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": BASELINE, "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.labelcolor": INK2, "text.color": INK,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlecolor": INK,
    "font.size": 10.5, "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "ytick.left": False,
})


def style_time_axis(ax):
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
    ax.grid(axis="x", visible=False)
    ax.margins(x=0.01)


def end_label(ax, x, y, text, color, dy=0):
    ax.annotate(text, (x, y), xytext=(8, dy), textcoords="offset points",
                color=color, fontweight="bold", fontsize=10, va="center")


def save(fig, name):
    fig.savefig(f"charts/{name}", dpi=200, bbox_inches="tight",
                facecolor=SURFACE)
    plt.close(fig)
    print(f"charts/{name}")


def chart1(m):
    """Two stacked panels, shared x: flat RUB prices above a collapsing ruble."""
    w = m.loc[WINDOW]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6.4), sharex=True,
                                   gridspec_kw={"hspace": 0.35})
    ax1.plot(w.index, w.psqm_adj / 1000, color=BLUE, lw=2)
    ax1.set_title("Moscow apartment prices held — even rose…")
    ax1.set_ylabel("price, thousand ₽ per m²")
    ax1.set_ylim(0, 180)
    end_label(ax1, w.index[-1], w.psqm_adj.iloc[-1] / 1000,
              f"{w.psqm_adj.iloc[-1]/1000:,.0f}k ₽", BLUE)

    ax2.plot(w.index, w.usdrub, color=AQUA, lw=2)
    ax2.set_title("…while the ruble collapsed")
    ax2.set_ylabel("rubles per US dollar")
    ax2.set_ylim(0, 75)
    end_label(ax2, w.index[-1], w.usdrub.iloc[-1], f"{w.usdrub.iloc[-1]:.0f} ₽/$", AQUA)

    for ax in (ax1, ax2):
        ax.axvline(CRASH, color=MUTED, lw=0.8, ls=(0, (4, 3)))
        style_time_axis(ax)
    ax2.annotate("Dec 2014\nruble crash", (CRASH, 12), xytext=(-72, 4),
                 textcoords="offset points", color=INK2, fontsize=9)
    fig.text(0.125, 0.015, "Source: Sberbank Russian Housing Market (Kaggle) — "
             "28,357 cleaned transactions. Mix-adjusted (district fixed effects), "
             "anchored to the Jan 2014 median.", fontsize=8, color=MUTED)
    save(fig, "01_stable_prices.png")


def chart2(m):
    """Same asset, three measuring sticks, one axis (indexed Jan 2014 = 100)."""
    w = m.loc[WINDOW]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    series = [("idx_psqm_adj", BLUE, "in rubles", 4),
              ("idx_psqm_real", YELLOW, "inflation-adjusted", 0),
              ("idx_psqm_usd", AQUA, "in US dollars", 0)]
    for col, color, label, dy in series:
        ax.plot(w.index, w[col], color=color, lw=2, label=label)
        end_label(ax, w.index[-1], w[col].iloc[-1],
                  f"{w[col].iloc[-1]:.0f}  {label}", color, dy)
    ax.axhline(100, color=BASELINE, lw=0.8)
    ax.axvline(CRASH, color=MUTED, lw=0.8, ls=(0, (4, 3)))
    ax.set_title("One asset, three stories: Moscow housing, index (Jan 2014 = 100)")
    ax.set_ylim(40, 130)
    style_time_axis(ax)
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    fig.text(0.125, -0.02, "Mix-adjusted price/m² re-denominated. Inflation-adjusted "
             "uses Russian CPI; dollar series uses monthly average USD/RUB.",
             fontsize=8, color=MUTED)
    save(fig, "02_redenominated.png")


def chart3(m):
    """The local-earner view: m² one month of average salary buys."""
    w = m.loc[WINDOW]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.plot(w.index, w.sqm_per_salary, color=BLUE, lw=2)
    ax.set_title("For ruble earners, nothing looked wrong")
    ax.set_ylabel("m² per average monthly Moscow salary")
    ax.set_ylim(0, 0.6)
    ax.axvline(CRASH, color=MUTED, lw=0.8, ls=(0, (4, 3)))
    end_label(ax, w.index[-1], w.sqm_per_salary.iloc[-1],
              f"{w.sqm_per_salary.iloc[-1]:.2f} m²", BLUE)
    style_time_axis(ax)
    fig.text(0.125, -0.03, "Average monthly wage (macro dataset, annual series) ÷ "
             "mix-adjusted price/m². Salaries are nominal — inflation ate them too.",
             fontsize=8, color=MUTED)
    save(fig, "03_affordability.png")


def chart4(m):
    """Counterfactual: 1M RUB from Jan 2014 into three assets, vs CPI."""
    cf = counterfactual(m)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    series = [("usd_cash", AQUA, "US dollar cash", 0),
              ("deposit", YELLOW, "ruble deposit", 5),
              ("housing", BLUE, "Moscow apartment", -5)]
    for col, color, label, dy in series:
        ax.plot(cf.index, cf[col] / 1e6, color=color, lw=2, label=label)
        end_label(ax, cf.index[-1], cf[col].iloc[-1] / 1e6,
                  f"{cf[col].iloc[-1]/1e6:.2f}M  {label}", color, dy)
    ax.plot(cf.index, cf.cpi_needed / 1e6, color=MUTED, lw=1.4, ls=(0, (4, 3)),
            label="needed to match inflation")
    end_label(ax, cf.index[-1], cf.cpi_needed.iloc[-1] / 1e6 + 0.03,
              "inflation", MUTED, 5)
    ax.set_title("1M rubles, January 2014: where each choice ended up")
    ax.set_ylabel("value, million ₽")
    ax.set_ylim(0.8, 2.0)
    style_time_axis(ax)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    fig.text(0.125, -0.02, "Housing tracks the mix-adjusted price/m² index (excludes "
             "rent income and transaction costs). Deposit compounds at the average "
             "reported deposit rate.", fontsize=8, color=MUTED)
    save(fig, "04_counterfactual.png")


def chart5(m):
    """Volume: panic spike, then a frozen market."""
    w = m.loc[WINDOW]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.bar(w.index, w.n_sales, width=22, color=BLUE, linewidth=0)
    ax.set_title("Prices held — because the market froze instead")
    ax.set_ylabel("recorded transactions per month")
    peak = w.n_sales.idxmax()
    ax.annotate(f"Dec 2014: {w.n_sales.max():,.0f} sales —\npanic buying as the "
                "ruble fell", (peak, w.n_sales.max()), xytext=(-150, -14),
                textcoords="offset points", color=INK2, fontsize=9,
                arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.8})
    h1_2015 = w.n_sales.loc["2015"].mean()
    ax.annotate(f"2015: ~{h1_2015:,.0f}/month,\nhalf the 2014 pace",
                (pd.Timestamp("2015-04-15"), h1_2015), xytext=(-10, 60),
                textcoords="offset points", color=INK2, fontsize=9)
    style_time_axis(ax)
    fig.text(0.125, -0.03, "Transactions in the dataset by month. Stable prices on "
             "collapsing volume are a frozen market, not a stable one.",
             fontsize=8, color=MUTED)
    save(fig, "05_volume.png")


if __name__ == "__main__":
    import os
    os.makedirs("charts", exist_ok=True)
    m = build()
    for f in (chart1, chart2, chart3, chart4, chart5):
        f(m)
