"""Charts for 'Nobody Builds a World Cup Team at Home Anymore'. Reads results.json.
Output: charts/*.png on a light surface (series dataviz palette)."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())

BLUE, AQUA, YELLOW, RED = "#2a78d6", "#1baf7a", "#eda100", "#e34948"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": BASELINE, "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": INK2,
    "text.color": INK, "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "font.size": 10.5,
    "axes.spines.top": False, "axes.spines.right": False,
})

PRETTY = {"IR Iran": "Iran", "United States": "USA", "Korea Republic": "South Korea",
          "Bosnia & Herz.": "Bosnia", "Côte d'Ivoire": "Ivory Coast"}


def label(t):
    return PRETTY.get(t, t)


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_foreign_share():
    rows = [r for r in R["by_nation"] if r["n"] >= 5]
    rows.sort(key=lambda r: r["foreign_share"])
    names = [label(r["team"]) for r in rows]
    vals = [r["foreign_share"] for r in rows]
    colors = [BLUE if v >= 0.999 else (AQUA if v >= 0.6 else YELLOW) for v in vals]
    fig, ax = plt.subplots(figsize=(8.4, 10))
    y = np.arange(len(names))
    ax.barh(y, vals, color=colors, height=0.72)
    ax.set_yticks(y, names, fontsize=9)
    ax.set_xlim(0, 1.06)
    ax.axvline(R["overall_foreign_share"], color=INK2, lw=1, ls=(0, (4, 3)))
    for yi, v in zip(y, vals):
        ax.annotate(f"{v:.0%}", (v, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8, color=INK2)
    ax.text(0.50, 0.12, "dashed line: the tournament average,\n"
            f"{R['overall_foreign_share']:.0%} of players are employed abroad",
            transform=ax.transAxes, fontsize=9, color=INK2, va="top")
    ax.set_xlabel("share of the squad playing club football abroad")
    ax.set_title("At the 2026 World Cup, most teams are built abroad")
    ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    ax.grid(axis="y", visible=False)
    fig.text(0.5, 0.007, "Featured players with a known club; nations with fewer than 5 such "
             "players (Egypt, Jordan, Qatar) omitted. Club = league employer, 2026 snapshot.",
             ha="center", fontsize=8, color=MUTED)
    save(fig, "01_foreign_share.png")


def chart2_leagues():
    lc = R["league_concentration"]
    items = list(lc.items())[:10]
    names = [k for k, _ in items]
    vals = [v for _, v in items]
    big5 = {"England", "Spain", "Italy", "Germany", "France"}
    colors = [BLUE if n in big5 else (YELLOW if n == "Saudi Arabia" else MUTED) for n in names]
    fig, ax = plt.subplots(figsize=(8.6, 5))
    x = np.arange(len(names))
    ax.bar(x, vals, color=colors, width=0.7)
    ax.set_xticks(x, names, rotation=30, ha="right", fontsize=9.5)
    for xi, v in zip(x, vals):
        ax.annotate(str(v), (xi, v), xytext=(0, 3), textcoords="offset points",
                    ha="center", fontsize=9, fontweight="bold", color=INK2)
    ax.set_ylabel("World Cup players employed there")
    ax.set_title("Where the world's World Cup players actually work")
    ax.grid(axis="x", visible=False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (BLUE, YELLOW, MUTED)]
    ax.legend(handles, ["the big-five European leagues", "the Saudi Pro League",
                        "everywhere else"], loc="upper right", frameon=False, fontsize=9)
    n5 = sum(v for n, v in lc.items() if n in big5)
    tot = sum(lc.values())
    fig.text(0.12, -0.06, f"The five big European leagues employ {n5} of the {tot} "
             f"featured players ({n5/tot:.0%}). The talent of the whole world funnels "
             "through a handful of leagues.", fontsize=8.5, color=MUTED)
    save(fig, "02_league_concentration.png")


def chart3_home_based():
    rows = [r for r in R["by_nation"] if r["n"] >= 5]
    rows.sort(key=lambda r: r["foreign_share"])
    rows = rows[:8]
    names = [label(r["team"]) for r in rows]
    home_share = [1 - r["foreign_share"] for r in rows]
    # type by hand-read of what "home-based" means for each
    KIND = {"Saudi Arabia": "money", "IR Iran": "domestic", "Germany": "elite",
            "South Africa": "domestic", "Spain": "elite", "Mexico": "domestic",
            "Türkiye": "domestic", "Czechia": "domestic"}
    CK = {"elite": BLUE, "money": YELLOW, "domestic": AQUA}
    colors = [CK.get(KIND.get(r["team"], "domestic"), AQUA) for r in rows]
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    y = np.arange(len(names))
    ax.barh(y, home_share, color=colors, height=0.68)
    ax.set_yticks(y, names, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.0)
    for yi, v in zip(y, home_share):
        ax.annotate(f"{v:.0%} home", (v, yi), xytext=(5, 0), textcoords="offset points",
                    va="center", fontsize=9, color=INK2)
    ax.set_xlabel("share of the squad playing in the home league")
    ax.set_title("'Home-based' means three different things")
    ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    ax.grid(axis="y", visible=False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (BLUE, YELLOW, AQUA)]
    ax.legend(handles, ["an elite league (Germany, Spain)",
                        "money keeps them home (Saudi Arabia)",
                        "a genuine domestic base (Mexico, Iran)"],
              loc="lower right", frameon=False, fontsize=9)
    fig.text(0.12, -0.04, "Keeping players home can mean three opposite things: a league "
             "good enough to hold them, oil money outbidding Europe, or simply nowhere "
             "else to go. The share alone cannot tell them apart.", fontsize=8.5, color=MUTED)
    save(fig, "03_home_based.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_foreign_share()
    chart2_leagues()
    chart3_home_based()
