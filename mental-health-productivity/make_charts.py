"""Charts for 'What Actually Moves Your Mental Health'. Reads results.json.
Output: charts/*.png on a light surface (series dataviz palette).
Chart 3 carries verified external figures (WHO), not numbers from the dataset."""
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

NICE = {"work_life_balance": "work-life balance", "social_support": "social support",
        "sleep_quality": "sleep quality", "sleep_hours": "sleep hours",
        "physical_activity_days": "physical activity", "academic_work_pressure": "work pressure",
        "social_media_hours": "social media hours"}


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_levers():
    rows = R["distress"]["levers"]  # sorted by |std_beta| desc
    rows = rows[::-1]               # barh plots bottom-up; reverse so strongest on top
    names = [NICE[r["lever"]] for r in rows]
    raw = [abs(r["raw_corr"]) for r in rows]
    adj = [abs(r["std_beta"]) for r in rows]
    y = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(8.8, 6.8))
    h = 0.38
    ax.barh(y + h / 2, raw, height=h, color="#b9b7ae", label="on its own (raw correlation)")
    hi = {"work-life balance", "social support"}
    deflate = {"sleep quality", "physical activity"}
    adjc = [AQUA if n in hi else (RED if n in deflate else BLUE) for n in names]
    ax.barh(y - h / 2, adj, height=h, color=adjc, label="adjusted for the other levers")
    ax.set_yticks(y, names, fontsize=10.5)
    ax.set_xlabel("strength of link to distress  (|correlation|, |standardized beta|)")
    ax.set_title("What actually moves mental health, once you stop double-counting")
    ax.grid(axis="y", visible=False)
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    fig.text(0.10, -0.03, "Distress = stress + anxiety + depression (standardized). Balance and "
             "support (green) stay strong after adjusting; sleep quality and exercise (red)\n"
             "shrink a lot, because the levers travel together. Simulated data, 500 rows; "
             "associations, not effects.", fontsize=8.5, color=MUTED)
    save(fig, "01_levers.png")


def chart2_bridge():
    pts = R["scatter"]
    order = ["Normal", "Anxiety", "Depression", "Burnout"]
    cond_color = {"Normal": AQUA, "Anxiety": YELLOW, "Depression": BLUE, "Burnout": RED}
    fig, ax = plt.subplots(figsize=(8.6, 6.4))
    for cond in order:
        xs = [p["d"] for p in pts if p["cond"] == cond]
        ys = [p["c"] for p in pts if p["cond"] == cond]
        ax.scatter(xs, ys, s=27, color=cond_color[cond], alpha=0.75, edgecolor="white",
                   linewidth=0.4, label=cond, zorder=3)
    xd = np.array([p["d"] for p in pts])
    yd = np.array([p["c"] for p in pts])
    m, c = np.polyfit(xd, yd, 1)
    xs = np.array([xd.min(), xd.max()])
    ax.plot(xs, m * xs + c, color=INK2, lw=1.6, ls=(0, (4, 3)), zorder=4)
    ax.set_xlabel("distress score  (worse mental health ->)")
    ax.set_ylabel("concentration level, 1-10  (better focus ->)")
    ax.set_title("Worse mental health tracks worse focus")
    ax.legend(loc="upper right", frameon=False, fontsize=9, title="condition")
    ax.annotate(f"r = {R['bridge_corr']:.2f}", (0.04, 0.07), xycoords="axes fraction",
                fontsize=12, color=INK, fontweight="bold")
    fig.text(0.10, -0.02, "Each point is one person (n=%d). Concentration is the in-data proxy "
             "for 'can you actually work'. The same two levers, balance and support, sit\nbehind "
             "both sides. Association only; simulated data." % R["bridge_n"],
             fontsize=8.5, color=MUTED)
    save(fig, "02_bridge.png")


def chart3_payoff():
    """External macro evidence, kept separate from the toy data. Figures verified against WHO;
    NOT computed from the dataset."""
    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    ax.axis("off")
    ax.set_title("What poor mental health costs, and what treating it returns",
                 loc="left", pad=18)
    ax.text(0.01, 0.62, "US$1 trillion", fontsize=33, color=RED, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.01, 0.44, "lost every year to depression and anxiety\n"
            "in reduced productivity (about 12 billion\nworking days)",
            fontsize=11, color=INK2, transform=ax.transAxes, va="top")
    ax.text(0.55, 0.62, "US$4 back", fontsize=33, color=AQUA, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.55, 0.44, "in better health and ability to work,\nfor every US$1 invested in "
            "scaled-up\ntreatment (WHO's estimate)",
            fontsize=11, color=INK2, transform=ax.transAxes, va="top")
    ax.axvline(0.51, ymin=0.10, ymax=0.80, color=BASELINE, lw=0.8)
    fig.text(0.01, 0.00, "Sources: WHO, Mental health at work (2024); WHO (2016), restating "
             "Chisholm et al. (2016), The Lancet Psychiatry. Global figures, not from this "
             "dataset.", fontsize=8.5, color=MUTED)
    save(fig, "03_payoff.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_levers()
    chart2_bridge()
    chart3_payoff()
