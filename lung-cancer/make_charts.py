"""Charts for Post 13 'The Internet's Favorite Lung-Cancer Dataset Says Smoking Is Harmless. It Isn't.'
Charts 1-2 are the FOIL (from the Kaggle survey, illustrating the selection-bias trap).
Charts 3-4 are the TRUTH (verified real epidemiology; filled from results.json['real']).
Sober palette; serious health topic. Reads results.json. Output: charts/*.png."""
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


def chart1_ranks_last():
    """Foil: the 15 features ranked by correlation with cancer, smoking dead last (red)."""
    rk = R["ranking"]
    labels = [r["feature"] for r in rk][::-1]        # smallest at bottom -> reverse for barh
    corrs = [r["corr"] for r in rk][::-1]
    cols = [RED if r["is_smoking"] else BLUE for r in rk][::-1]
    fig, ax = plt.subplots(figsize=(8.6, 6.4))
    y = np.arange(len(labels))
    ax.barh(y, corrs, color=cols, height=0.72)
    ax.set_yticks(y, labels, fontsize=10.5)
    for yi, c in zip(y, corrs):
        ax.annotate(f"{c:.2f}", (c, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=9, color=INK2)
    ax.set_xlim(0, max(corrs) * 1.18)
    ax.set_xlabel("correlation with a lung-cancer diagnosis (in the file)")
    ax.set_title("In the file, smoking is the weakest of 15 signals for lung cancer")
    ax.grid(axis="y", visible=False)
    # highlight smoking
    s_idx = [i for i, r in enumerate(rk[::-1]) if r["is_smoking"]][0]
    ax.get_yticklabels()[s_idx].set_color(RED)
    ax.get_yticklabels()[s_idx].set_fontweight("bold")
    fig.text(0.09, -0.03, "Kaggle 'survey lung cancer' file (309 rows). Allergy and alcohol appear to "
             "matter most; smoking appears to matter least.\nThis is an artifact of a broken sample, "
             "not a fact about smoking (see text).", fontsize=8.5, color=MUTED)
    save(fig, "lung-1-ranks-last.png")


def chart2_no_control():
    """Foil: 87% of the sample already has cancer; smokers vs non-smokers barely differ."""
    f = R["foil"]
    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    cats = ["Non-smokers", "Smokers"]
    rates = [f["p_cancer_nonsmoker"] * 100, f["p_cancer_smoker"] * 100]
    ns = [f["n_nonsmoker"], f["n_smoker"]]
    x = np.arange(2)
    ax.bar(x, rates, color=[BLUE, RED], width=0.55)
    ax.set_xticks(x, [f"{c}\n(n={n})" for c, n in zip(cats, ns)], fontsize=11)
    for xi, r in zip(x, rates):
        ax.annotate(f"{r:.0f}%", (xi, r), xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=15, fontweight="bold", color=INK)
    ax.axhline(f["cancer_rate"] * 100, color=INK2, ls="--", lw=1.1)
    ax.annotate(f"{f['cancer_rate']*100:.0f}% of everyone in the file already has cancer",
                (1.46, f["cancer_rate"] * 100), ha="right", va="bottom", fontsize=9.5,
                color=INK2, fontweight="bold")
    ax.set_ylim(0, 100)
    ax.set_ylabel("share diagnosed with lung cancer (in the file)")
    ax.set_title("There is no healthy comparison group, so nothing separates")
    ax.grid(axis="x", visible=False)
    fig.text(0.09, -0.04, f"Kaggle 'survey lung cancer' file. Smokers {rates[1]:.0f}% vs non-smokers "
             f"{rates[0]:.0f}% is not a real difference (Fisher exact odds ratio {f['fisher_or']}, "
             f"p = {f['fisher_p']}).\nWhen almost everyone sampled is already sick, no cause can stand "
             "out.", fontsize=8.5, color=MUTED)
    save(fig, "lung-2-no-control.png")


def chart3_real_risk():
    """Truth: real relative risk of dying of lung cancer, rising with intensity, vs the file's 1.4x."""
    r = R["real"]
    cats = ["Never\nsmoker", "Under 1\ncigarette/day", "1 to 10\ncigarettes/day", "Regular\nsmoker"]
    vals = [r["rr_never"], r["rr_lt1_cig"], r["rr_1to10_cig"], r["rr_regular"]]
    cols = [GREEN, AMBER, AMBER, RED]
    fig, ax = plt.subplots(figsize=(8.8, 5.6))
    x = np.arange(4)
    ax.bar(x, vals, color=cols, width=0.62)
    ax.set_xticks(x, cats, fontsize=10.5)
    for xi, v in zip(x, vals):
        ax.annotate(f"{v:.0f}x", (xi, v), xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=14, fontweight="bold", color=INK)
    ax.axhline(r["file_or"], color=INK2, ls="--", lw=1.2)
    ax.annotate(f"what the Kaggle file 'saw': {r['file_or']}x, and not even significant",
                (3.46, r["file_or"] + 0.5), ha="right", va="bottom", fontsize=9,
                color=INK2, fontweight="bold")
    ax.set_ylim(0, r["rr_regular"] * 1.16)
    ax.set_ylabel("times a never-smoker's risk of dying of lung cancer")
    ax.set_title("The risk the file could not see: even a little smoking multiplies it")
    ax.grid(axis="x", visible=False)
    fig.text(0.09, -0.05, "Risk of dying of lung cancer versus never-smokers. Under 1 and 1 to 10 per "
             "day: Inoue-Choi et al. (2017), NIH-AARP cohort of 290,215 adults;\nregular smokers about "
             "25 times: Thun et al. (2013), contemporary US cohort. There is no safe level.",
             fontsize=8.5, color=MUTED)
    save(fig, "lung-3-real-risk.png")


def chart4_indonesia():
    """Light Indonesia touch: roughly two-thirds of men use tobacco (GATS 2021)."""
    r = R["real"]
    cats = ["Men", "All adults", "Women"]
    vals = [r["id_men_pct"], r["id_overall_pct"], r["id_women_pct"]]
    cols = [RED, BLUE, GREEN]
    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    x = np.arange(3)
    ax.bar(x, vals, color=cols, width=0.58)
    ax.set_xticks(x, cats, fontsize=11)
    for xi, v in zip(x, vals):
        ax.annotate(f"{v:.1f}%", (xi, v), xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=14, fontweight="bold", color=INK)
    ax.set_ylim(0, 80)
    ax.set_ylabel("current tobacco use, adults 15+ (2021)")
    ax.set_title("In Indonesia, roughly two-thirds of men use tobacco")
    ax.grid(axis="x", visible=False)
    fig.text(0.09, -0.04, f"Global Adult Tobacco Survey, Indonesia 2021 (Ministry of Health, WHO, CDC). "
             f"About {r['id_users_m']:.0f} million tobacco users, among the world's\nhighest male rates. "
             f"The average smoker started at about {r['id_init_age']:.0f}.", fontsize=8.5, color=MUTED)
    save(fig, "lung-4-indonesia.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_ranks_last()
    chart2_no_control()
    chart3_real_risk()
    chart4_indonesia()
    print("built all 4 charts (foil 1-2 + truth 3-4)")
