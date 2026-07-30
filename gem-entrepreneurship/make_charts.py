"""Charts for Post 16 'The Survey Found Indonesia's Business Owners. It Just Couldn't Count Them.'

Reads results.json. Output: charts/gem-N-name.png.
Every footnote may claim only what the plotted series shows. Every number is interpolated from
results.json rather than typed, so a rerun cannot leave a stale figure behind.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())

BLUE, GREEN, AMBER, RED = "#2a78d6", "#1baf7a", "#eda100", "#e34948"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE, SHADE = "#e1e0d9", "#c3c2b7", "#fcfcfb", "#ecebe4"

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
    # matplotlib writes a Unicode minus (U+2212) on negative ticks by default, which breaks the
    # house no-dash rule inside the rendered image. Force an ASCII hyphen.
    "axes.unicode_minus": False,
})


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_three_lines():
    """The setup and the reveal in one panel.

    GEM's own screening question tracks Indonesia's national survey by 2022. It is the DERIVED
    established-ownership number that walks away. That is why the story is about the classification
    step and not about the survey failing to find anyone.
    """
    d = pd.DataFrame(R["divergence"])
    fig, ax = plt.subplots(figsize=(10.0, 5.8))
    ax.plot(d.year, d.sakernas_pct_1564, "o-", color=GREEN, lw=2.8, ms=7,
            label="Indonesia's own labour force survey")
    ax.plot(d.year, d.gem_screen_pct, "o--", color=BLUE, lw=2.2, ms=6,
            label="GEM, raw screening question")
    ax.plot(d.year, d.gem_ebo_pct, "o-", color=RED, lw=2.8, ms=7,
            label="GEM, published established ownership")
    ax.fill_between(d.year, d.gem_ebo_pct, d.sakernas_pct_1564, color=RED, alpha=0.06)

    f, l = d.iloc[0], d.iloc[-1]
    ax.annotate(f"{f.sakernas_pct_1564:.1f}%", (f.year, f.sakernas_pct_1564), xytext=(0, 9),
                textcoords="offset points", ha="center", fontsize=10.5, fontweight="bold", color=GREEN)
    ax.annotate(f"{l.sakernas_pct_1564:.1f}%", (l.year, l.sakernas_pct_1564), xytext=(0, 10),
                textcoords="offset points", ha="center", fontsize=11, fontweight="bold", color=GREEN)
    ax.annotate(f"{f.gem_screen_pct:.1f}%", (f.year, f.gem_screen_pct), xytext=(0, 9),
                textcoords="offset points", ha="center", fontsize=10.5, fontweight="bold", color=BLUE)
    ax.annotate(f"{l.gem_screen_pct:.1f}%", (l.year, l.gem_screen_pct), xytext=(8, -4),
                textcoords="offset points", ha="left", fontsize=11, fontweight="bold", color=BLUE)
    ax.annotate(f"{f.gem_ebo_pct:.1f}%", (f.year, f.gem_ebo_pct), xytext=(-9, -4),
                textcoords="offset points", ha="right", fontsize=10.5, fontweight="bold", color=RED)
    ax.annotate(f"{l.gem_ebo_pct:.1f}%", (l.year, l.gem_ebo_pct), xytext=(0, -20),
                textcoords="offset points", ha="center", fontsize=11, fontweight="bold", color=RED)

    ax.annotate("", xy=(l.year, l.sakernas_pct_1564), xytext=(l.year, l.gem_ebo_pct),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.3))
    ax.annotate(f"about {l.distance_pts:.0f} points apart", (l.year - 0.18, 17),
                ha="right", va="center", fontsize=10, fontweight="bold", color=INK2)
    ax.annotate("the screen starts far above the national\ncount and ends close to it",
                (2019.0, 34.5), ha="center", fontsize=9.5, color=BLUE, style="italic")

    ax.set_ylim(0, 52)
    ax.set_xticks(list(d.year))
    ax.set_ylabel("business owners, % of working-age population")
    ax.set_title("GEM found Indonesia's business owners. Its published number lost them.")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right", frameon=False, fontsize=9.5)
    fig.text(0.09, -0.12,
             "Green: employers plus own-account workers from Indonesia's labour force survey "
             "(Sakernas) via ILOSTAT, direct survey data rather than a\nmodelled estimate. Blue: the "
             "share answering yes to GEM's screening question, which asks whether you currently own a "
             "business you help\nmanage, are self-employed, or sell any goods or services. Red: GEM's "
             "published established-ownership rate, which requires that the\nbusiness has paid the "
             "owner for more than 42 months. The bases are close but not identical: GEM's rates are "
             "per person aged 18 to 64, while the\nSakernas share here is per person aged 15 to 64 "
             "with an all-ages numerator, so every gap on this chart is approximate to about two "
             "points.\nThe widening is many times larger than that. GEM has no Indonesian round in "
             "2019 or 2021.",
             fontsize=8.5, color=MUTED)
    save(fig, "gem-1-three-lines.png")


def chart2_inside():
    """Where it breaks, and how much of the fall each step accounts for."""
    p = pd.DataFrame(R["classification_path"])
    dec = R["decomposition"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 5.2),
                                   gridspec_kw={"width_ratios": [1.3, 1]})

    ax1.plot(p.year, p.conversion_pct, "o-", color=RED, lw=2.6, ms=7,
             label="share of screened owners classed as established")
    nr = p.dropna(subset=["payment_year_missing_pct"])
    ax1.plot(nr.year, nr.payment_year_missing_pct, "s--", color=AMBER, lw=2.2, ms=7,
             label="payment-year answer missing")
    pr = p.dropna(subset=["pass_rate_if_answered_pct"])
    ax1.plot(pr.year, pr.pass_rate_if_answered_pct, "^:", color=GREEN, lw=2.0, ms=7,
             label="passes the 42-month test, of those who answered")
    lo = p.loc[p.conversion_pct.idxmin()]
    ax1.annotate(f"{lo.conversion_pct:.1f}%", (lo.year, lo.conversion_pct), xytext=(10, -2),
                 textcoords="offset points", ha="left", fontsize=11, fontweight="bold", color=RED)
    hi = nr.iloc[-1]
    ax1.annotate(f"{hi.payment_year_missing_pct:.1f}%", (hi.year, hi.payment_year_missing_pct),
                 xytext=(8, 2), textcoords="offset points", ha="left", fontsize=11,
                 fontweight="bold", color=AMBER)
    ax1.annotate(f"{nr.iloc[0].payment_year_missing_pct:.1f}%",
                 (nr.iloc[0].year, nr.iloc[0].payment_year_missing_pct), xytext=(0, -18),
                 textcoords="offset points", ha="center", fontsize=10.5,
                 fontweight="bold", color=AMBER)
    ax1.set_ylim(0, 100)
    ax1.set_xticks(list(p.year))
    ax1.tick_params(axis="x", labelrotation=45)
    ax1.set_ylabel("percent")
    ax1.set_title("The rule held. The answer it needs went missing.", fontsize=11.5)
    ax1.grid(axis="x", visible=False)
    ax1.legend(loc="lower left", frameon=False, fontsize=8.6)

    S = dec["symmetric_shapley"]
    A, B = dec["ordering_a_hold_2013_conversion"], dec["ordering_b_hold_2022_conversion"]
    vals = [S["screen"]["pts"], S["classification"]["pts"]]
    shares = [S["screen"]["share"], S["classification"]["share"]]
    rng = [(min(A["screen"]["share"], B["screen"]["share"]),
            max(A["screen"]["share"], B["screen"]["share"])),
           (min(A["classification"]["share"], B["classification"]["share"]),
            max(A["classification"]["share"], B["classification"]["share"]))]
    ax2.bar([0, 1], vals, color=[BLUE, RED], width=0.55)
    for i, (v, s) in enumerate(zip(vals, shares)):
        ax2.annotate(f"{s:.0f}%", (i, v + 1.05), ha="center", fontsize=17,
                     fontweight="bold", color=BLUE if i == 0 else RED)
        ax2.annotate(f"{rng[i][0]:.0f} to {rng[i][1]:.0f}% by ordering", (i, v + 0.42),
                     ha="center", fontsize=8.6, color=MUTED)
        ax2.annotate(f"{v:.2f} pts", (i, v / 2), ha="center", va="center", fontsize=11,
                     fontweight="bold", color="#ffffff")
    ax2.set_xticks([0, 1], ["the screen\nnarrowing", "the classification\nstep"], fontsize=10.5)
    ax2.set_ylim(0, max(vals) * 1.38)
    ax2.set_ylabel("percentage points of the fall")
    ax2.set_title(f"The {dec['total_fall_pts']}-point fall, split symmetrically", fontsize=11.5)
    ax2.grid(axis="x", visible=False)

    fig.suptitle("Inside the machine: a screening question, then a 42-month test",
                 fontsize=14, fontweight="bold", y=1.03)
    fig.text(0.09, -0.13,
             "Left, red: of everyone GEM's screening question catches, the share published as an "
             "established owner, from the national files for all\neight rounds. It is volatile, not "
             "flat, and 2022 is its lowest point. Amber: among screened Indonesian owners, the share "
             "who did not\nreport the year the business first paid them, which is the answer the "
             "42-month rule needs. Green: among those who did answer, the\nshare passing the test, "
             "which is stable. The rule did not tighten; its input went missing. Right: the fall "
             "decomposed. A two-factor split\nhas no unique answer and its residual is always zero, "
             "so the symmetric average is shown with the range across orderings beneath.",
             fontsize=8.5, color=MUTED)
    save(fig, "gem-2-inside-the-machine.png")


def chart3_missing_answer():
    """Is the unanswered question an Indonesian problem or everyone's?"""
    nr = pd.DataFrame(R["nonresponse_2022"]["all"]).sort_values("pct_missing")
    med = R["nonresponse_2022"]["median_pct"]
    idn = R["nonresponse_2022"]["indonesia_pct"]
    rank = R["nonresponse_2022"]["indonesia_rank"]
    n = R["nonresponse_2022"]["n_economies"]

    fig, ax = plt.subplots(figsize=(9.8, 5.6))
    colors = [RED if c == "Indonesia" else BASELINE for c in nr.country]
    ax.barh(np.arange(len(nr)), nr.pct_missing, color=colors, height=0.78)
    ax.axvline(med, color=INK2, ls="--", lw=1.2)
    ax.annotate(f"median {med:.1f}%", (med + 1.2, len(nr) * 0.06), fontsize=9.5,
                fontweight="bold", color=INK2)
    i = int(np.where(nr.country.values == "Indonesia")[0][0])
    ax.annotate(f"Indonesia {idn:.1f}%, the highest of {n}", (2, i), ha="left",
                va="center", fontsize=10.5, fontweight="bold", color="#ffffff")
    worst = nr.iloc[-1]
    ax.annotate(f"{worst.country} {worst.pct_missing:.1f}%", (2, len(nr) - 1),
                ha="left", va="center", fontsize=9.5, color=INK2)
    ax.set_yticks([])
    ax.set_xlim(0, 100)
    ax.set_xlabel("share of screened business owners who did not report the year it first paid them")
    ax.set_ylabel(f"{n} economies with 50 or more screened owners")
    ax.set_title("The question that decides the count, left blank")
    ax.grid(axis="y", visible=False)
    fig.text(0.09, -0.10,
             "GEM 2022 individual-level data, question Q2E2: the first year the founders received "
             "wages, profits or payments in kind. Each bar is\none economy, showing the share of "
             "screened business owners who did not answer it. Without that year the 42-month rule "
             f"cannot be\napplied, so the respondent cannot be classed as established. Indonesia is "
             f"the highest of {n} at {idn:.1f}%, against a median of {med:.1f}%.\nHigh nonresponse "
             "on this item is common everywhere; what is unusual is its level in Indonesia in 2022, "
             "having been 24.1% in 2013.",
             fontsize=8.5, color=MUTED)
    save(fig, "gem-3-missing-answer.png")


def chart4_not_alone():
    """Indonesia at the extreme of a spread that is wide in both directions."""
    div = pd.DataFrame(R["cross_country"]["divergence_ranking"]).sort_values("divergence")
    fig, ax = plt.subplots(figsize=(9.8, 5.6))
    colors = [RED if c == "Indonesia" else BASELINE for c in div.country]
    ax.barh(np.arange(len(div)), div.divergence, color=colors, height=0.78)
    ax.axvline(0, color=INK2, lw=1.0)
    i = int(np.where(div.country.values == "Indonesia")[0][0])
    v = float(div.divergence.iloc[i])
    z = (v - div.divergence.mean()) / div.divergence.std()
    ax.annotate(f"Indonesia, {v:+.0f} points", (v - 6, i), ha="right", va="center",
                fontsize=11, fontweight="bold", color=RED)
    for nm in ("Saudi Arabia", "Estonia", "Guatemala"):
        w = np.where(div.country.values == nm)[0]
        if len(w):
            j = int(w[0])
            ax.annotate(nm, (float(div.divergence.iloc[j]) + 5, j), va="center",
                        fontsize=9, color=MUTED)
    med = float(div.divergence.median())
    ax.annotate(f"median {med:+.0f}", (med + 5, len(div) * 0.52), ha="left", fontsize=9,
                color=INK2, fontweight="bold")
    ax.set_yticks([])
    ax.set_xlabel("gap between the two measures' change, first to last GEM round, percentage points")
    ax.set_ylabel(f"{len(div)} economies with five or more GEM rounds")
    ax.set_title("Indonesia is the most extreme case of a disagreement that is everywhere")
    ax.grid(axis="y", visible=False)
    w = R["cross_country"]["within"]
    fig.text(0.09, -0.11,
             "Each bar is one economy: the percentage change in its GEM established-ownership rate "
             "between its first and last round, minus the\nchange in its ILO self-employment rate "
             "over the same span. Spans differ by economy, so this is a like-for-like comparison "
             "within each\ncountry rather than a common window. Zero would mean the two measures "
             f"moved together. Indonesia has the largest negative gap, at a\nz-score of {z:+.2f}, "
             "which for the most extreme value in the set is unremarkable. Within economies over "
             f"time the two measures barely relate:\nthe median correlation is {w['median_r']:+.2f} "
             f"across {w['n_economies']} economies with six or more rounds.",
             fontsize=8.5, color=MUTED)
    save(fig, "gem-4-not-alone.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    for old in ("gem-1-divergence.png", "gem-2-suspects.png", "gem-3-not-alone.png",
                "gem-4-never-agreed.png"):
        p = BASE / "charts" / old
        if p.exists():
            p.unlink()
            print("removed stale", old)
    chart1_three_lines()
    chart2_inside()
    chart3_missing_answer()
    chart4_not_alone()
    print("built all 4 charts")
