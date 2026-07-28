"""Charts for Post 14 'The Easiest Promise to Keep Is the One You Can Count'.
Reads results.json (verified constants only). Output: charts/edubudget-N-name.png."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())

BLUE, GREEN, AMBER, RED = "#2a78d6", "#1baf7a", "#eda100", "#e34948"
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
    "text.parse_math": False,
})


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_mandate():
    """The promise, and the court that enforced it."""
    m = R["mandate"]
    labels = [str(r["year"]) for r in m]
    vals = [r["share"] for r in m]
    cols = [RED if r["status"] == "struck down" else GREEN for r in m]
    fig, ax = plt.subplots(figsize=(8.8, 5.4))
    x = np.arange(len(m))
    ax.bar(x, vals, color=cols, width=0.6)
    ax.set_xticks(x, labels, fontsize=11)
    for xi, r in zip(x, m):
        ax.annotate(r["label"], (xi, r["share"]), xytext=(0, 4),
                    textcoords="offset points", ha="center", fontsize=12,
                    fontweight="bold", color=INK)
        if r["status"] == "struck down":
            ax.annotate("struck down", (xi, r["share"] / 2), ha="center", va="center",
                        fontsize=9, color="#ffffff", fontweight="bold", rotation=90)
    ax.axhline(20, color=INK2, ls="--", lw=1.2)
    ax.annotate("the constitution says at least 20%", (len(m) - 0.45, 20.4), ha="right",
                va="bottom", fontsize=9.5, color=INK2, fontweight="bold")
    ax.set_ylim(0, 24)
    ax.set_ylabel("education share of the state budget")
    ax.set_title("A promise the courts had to enforce")
    ax.grid(axis="x", visible=False)
    fig.text(0.09, -0.05, "Indonesia's Constitutional Court voided the 2007 budget's 11.8% education "
             "ceiling, then the entire revised 2008 budget law at 15.6%, finding a\ndeliberate breach. "
             "The floor has been met nationally every year since 2009 (Mahkamah Konstitusi; "
             "Kementerian Keuangan). Part of what made 20%\nreachable was definitional: educator "
             "salaries, originally outside the mandate, were later held to count inside it.",
             fontsize=8.5, color=MUTED)
    save(fig, "edubudget-1-mandate.png")


def chart2_small_pie():
    """Twenty percent of a budget that is itself small."""
    peers = sorted(R["peers"], key=lambda r: r["pct"])
    names = [p["country"] for p in peers]
    vals = [p["pct"] for p in peers]
    cols = [RED if p["country"] == "Indonesia" else BLUE for p in peers]
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    y = np.arange(len(peers))
    ax.barh(y, vals, color=cols, height=0.66)
    ax.set_yticks(y, names, fontsize=11)
    for yi, p in zip(y, peers):
        ax.annotate(f"{p['pct']:.2f}%", (p["pct"], yi), xytext=(5, 0), textcoords="offset points",
                    va="center", fontsize=10.5, fontweight="bold", color=INK2)
    idx = [i for i, p in enumerate(peers) if p["country"] == "Indonesia"][0]
    ax.get_yticklabels()[idx].set_color(RED)
    ax.get_yticklabels()[idx].set_fontweight("bold")
    ax.set_xlim(0, max(vals) * 1.2)
    ax.set_xlabel("government education spending, % of GDP")
    ax.set_title("A fifth of the budget is still only three percent of the economy")
    ax.grid(axis="y", visible=False)
    fig.text(0.09, -0.09, "Indonesia's 20% of the state budget lands at 3.00% of GDP, because total "
             "state spending is only about 15% of GDP. Indonesia is\nbudget-based (Kementerian "
             "Keuangan, 2024); the others are World Bank and UNESCO figures for 2022 to 2024. Not "
             "strictly like for like:\nIndonesia's allocation includes a financing component the peer "
             "definition would exclude. On an expenditure-only basis it is about 2.7%.",
             fontsize=8.5, color=MUTED)
    save(fig, "edubudget-2-small-pie.png")


def chart3_more_kids():
    """The learning gap, shown with the reason the mean moved as it did."""
    pisa = {k: {int(y): v for y, v in s.items()} for k, s in R["pisa"].items()}
    cov = {int(y): v for y, v in R["coverage"].items()}
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    style = {"reading": (BLUE, "Reading"), "maths": (AMBER, "Mathematics"),
             "science": (GREEN, "Science")}
    for subj, (c, lab) in style.items():
        yrs = sorted(pisa[subj])
        ax.plot(yrs, [pisa[subj][y] for y in yrs], color=c, lw=2.4, marker="o",
                ms=5, label=lab)
    ax.set_ylim(330, 420)
    ax.set_ylabel("PISA mean score")
    ax.set_xlabel("PISA cycle")
    ax.set_title("More children in the exam room, and a mean that never took off")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="lower left", frameon=False, fontsize=9.5, ncols=3)

    ax2 = ax.twinx()
    cy = sorted(cov)
    ax2.plot(cy, [cov[y] for y in cy], color=MUTED, ls="--", lw=1.6, marker="s", ms=6)
    for y in cy:
        ax2.annotate(f"{cov[y]}%", (y, cov[y]), xytext=(0, 7), textcoords="offset points",
                     ha="center", fontsize=9.5, color=INK2, fontweight="bold")
    ax2.set_ylim(0, 130)
    ax2.set_ylabel("share of 15-year-olds covered by PISA", color=MUTED)
    ax2.grid(False)
    ax2.spines["right"].set_visible(True)
    ax2.annotate("PISA coverage of 15-year-olds\n(two published points)", (2022.3, 14),
                 ha="right", va="bottom", fontsize=9, color=MUTED)
    fig.text(0.09, -0.09, "OECD PISA. Each subject starts at its first trend-comparable cycle: "
             "reading 2000, mathematics 2003, science 2006. Coverage rose from\n46% of Indonesia's "
             "15-year-olds to 85% by 2018, over 1.1 million more teenagers inside the school system, "
             "which mechanically lowers a mean.\nOnly those two coverage points are published, so "
             "only those two are plotted. Measured at the 75th percentile of all 15-year-olds,\n"
             "OECD's enrolment-adjusted reading of Indonesia from 2012 to 2022 is science up, reading "
             "down, mathematics stable. Scores fell\nacross the OECD after 2018 as well.",
             fontsize=8.5, color=MUTED)
    save(fig, "edubudget-3-more-kids.png")


def chart4_what_it_buys():
    """What the guaranteed share is actually allowed to buy."""
    b = R["budget26"]
    parts = [("Educators' pay", b["educators_pay_t"], b["educators_pay_pct"], BLUE),
             ("Free school meals", b["mbg_inside_educ_t"], b["mbg_pct"], AMBER),
             ("Everything else", b["other_t"], b["other_pct"], GREEN)]
    fig, ax = plt.subplots(figsize=(9.4, 3.4))
    left = 0.0
    for name, val, pct, col in parts:
        ax.barh(0, val, left=left, color=col, height=0.5, edgecolor=SURFACE, linewidth=1.6)
        ax.text(left + val / 2, 0, f"{name}\nRp{val:.0f}T  ({pct:.1f}%)", ha="center", va="center",
                color="#ffffff" if col != AMBER else INK, fontsize=10, fontweight="bold")
        left += val
    ax.set_xlim(0, b["total_draft_t"])
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.set_xlabel("trillions of rupiah")
    ax.set_title("What a fifth of the state budget is allowed to buy")
    ax.grid(False)
    for sp in ["left", "right", "top"]:
        ax.spines[sp].set_visible(False)
    fig.text(0.09, -0.20, "Indonesia's 2026 DRAFT education budget, Rp757.8 trillion (Sekretariat "
             "Negara, August 2025); the enacted figure is Rp769.1 trillion. As\nproposed, nearly "
             "three in ten rupiah of the constitutionally protected education budget was allocated to "
             "the free nutritious meals\nprogramme, for 82.9 million beneficiaries. 'Everything else' is a "
             "residual: the source's own itemisation does not exhaust the total.",
             fontsize=8.5, color=MUTED)
    save(fig, "edubudget-4-what-it-buys.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_mandate()
    chart2_small_pie()
    chart3_more_kids()
    chart4_what_it_buys()
    print("built all 4 charts")
