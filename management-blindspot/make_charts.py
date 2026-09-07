"""Charts for Post 24, 'the job nobody takes away'.

Reads results.json. Output: charts/mg-N-name.png.

Every number drawn or written here is interpolated from results.json. Typed literals are limited
to axis limits, layout coordinates, and fixed source labels that describe the data rather than the
result ("1 to 5", "O*NET 31.0").

House rule: no em or en dashes anywhere, including inside rendered images. matplotlib writes a
Unicode minus on negative ticks unless axes.unicode_minus is False.

After editing any caption, RE-OPEN THE PNG and look at it. Eight prose-versus-image desyncs shipped
across six rounds on Post 23 and every one was invisible in this file and visible in the picture.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

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
    "text.parse_math": False, "axes.unicode_minus": False,
})

# Colour carries one argument only: blue is the managing, amber is the doing.
C_PEOPLE, C_HANDS = BLUE, AMBER


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def footnote(fig, text, y=-0.02):
    fig.text(0.0, y, text, ha="left", va="top", fontsize=8.6, color=MUTED, wrap=True)


def short(t):
    return t.replace("First-Line Supervisors of ", "").replace(
        ", Except Gambling Services", "").replace(" Workers", "").replace(
        " and Vehicle Operators", "").replace(", Hand", "")


# ------------------------------------------------------------------ 1. the second job

def chart1():
    """The promotion shift. Two bars per comparison, sorted by the managing."""
    rows = sorted(R["by_major_group"], key=lambda r: r["d_people"])
    p = R["promotion"]
    y = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(11.6, 8.4))
    ax.set_axisbelow(True)
    h = 0.38
    ax.barh(y + h / 2, [r["d_people"] for r in rows], height=h, color=C_PEOPLE,
            label="Managing people")
    ax.barh(y - h / 2, [r["d_hands"] for r in rows], height=h, color=C_HANDS,
            label="Doing the work")
    ax.axvline(0, color=BASELINE, lw=1.0)
    ax.set_yticks(y, [short(r["supervisor"]) for r in rows], fontsize=9.6)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Change in rated importance on becoming the supervisor, 1 to 5 scale")
    ax.set_title("The promotion adds the managing. It does not remove the doing.")
    ax.set_xlim(min(r["d_hands"] for r in rows) - 0.25, max(r["d_people"] for r in rows) + 0.55)
    # No legend: it collided with these two lines, and these two lines already carry the colour
    # mapping. The blue sentence names the blue bar and the amber sentence names the amber one.
    ax.text(0.985, 0.115,
            f"Managing people rises in {p['n_people_rises']} of {p['n_comparisons']}",
            transform=ax.transAxes, ha="right", fontsize=11.8, color=C_PEOPLE, fontweight="bold")
    ax.text(0.985, 0.055,
            f"Doing the work falls in only {p['n_hands_falls']} of {p['n_comparisons']}",
            transform=ax.transAxes, ha="right", fontsize=11.8, color="#b57f00", fontweight="bold")
    footnote(fig,
             f"O*NET 31.0, Importance scale. Each row is one of the {p['n_comparisons']} "
             f"occupations titled 'First-Line Supervisors of ...', compared against every "
             f"non-supervisory occupation sharing its SOC major group. The pairing is done by that "
             f"rule, not by choosing which jobs go together. Managing people is the mean of four "
             f"activities: coordinating others, building teams, directing subordinates, coaching. "
             f"Doing the work is the mean of six: physical activities, handling objects, "
             f"controlling machines, working with computers, drafting, repairing. Mean shift "
             f"across all {p['n_comparisons']}: managing {p['mean_shift_people']:+.2f}, "
             f"doing {p['mean_shift_hands']:+.2f}.", y=-0.035)
    save(fig, "mg-1-the-second-job.png")


# ------------------------------------------------------------------ 2. what the net hides

def chart2():
    """The +0.18 is the average of two opposite movements."""
    d = R["hands_decomposition"]
    p = R["promotion"]
    items = sorted(d.items(), key=lambda kv: kv[1]["mean_shift"])
    y = np.arange(len(items))
    fig, ax = plt.subplots(figsize=(11.2, 4.6))
    ax.set_axisbelow(True)
    vals = [v["mean_shift"] for _, v in items]
    ax.barh(y, vals, height=0.62, color=[AMBER if v > 0 else MUTED for v in vals])
    ax.axvline(0, color=BASELINE, lw=1.0)
    ax.set_yticks(y, [n.split(",")[0][:46] for n, _ in items], fontsize=9.8)
    ax.grid(axis="y", visible=False)
    for yy, (_, v) in zip(y, items):
        off = 0.02 if v["mean_shift"] > 0 else -0.02
        ax.text(v["mean_shift"] + off, yy,
                f"{v['mean_shift']:+.2f}   rises in {v['n_rising']} of {v['n']}",
                va="center", ha="left" if v["mean_shift"] > 0 else "right",
                fontsize=9.3, color=INK2)
    ax.set_xlim(min(vals) - 0.42, max(vals) + 0.52)
    ax.set_xlabel("Change in rated importance on becoming the supervisor, 1 to 5 scale")
    ax.set_title("What the flat number hides: you stop lifting and start typing")
    footnote(fig,
             f"The same {p['n_comparisons']} comparisons as the previous chart, with the six "
             f"doing-the-work activities separated. The net shift of "
             f"{p['mean_shift_hands']:+.2f} is the average of two opposite movements. Remove "
             f"Working with Computers and the remaining five come to "
             f"{p['mean_shift_hands_excluding_computers']:+.2f}, falling in "
             f"{p['n_hands_excluding_computers_falls']} of {p['n_comparisons']}. Physical work "
             f"does go away. It is replaced by other doing, not by managing.", y=-0.06)
    save(fig, "mg-2-what-the-net-hides.png")


# ------------------------------------------------------------------ 3. what actually rises

def chart3():
    """Across all occupations, seniority is not mainly about managing people."""
    z = R["zone_corr"]
    items = sorted(z.items(), key=lambda kv: kv[1]["r"])
    y = np.arange(len(items))
    fig, ax = plt.subplots(figsize=(11.0, 10.4))
    ax.set_axisbelow(True)
    cols = [C_PEOPLE if v["is_people_management"] else
            (C_HANDS if v["is_hands_on"] else SHADE) for _, v in items]
    ax.barh(y, [v["r"] for _, v in items], height=0.66, color=cols,
            edgecolor=[BASELINE if c == SHADE else "none" for c in cols], linewidth=0.7)
    ax.axvline(0, color=BASELINE, lw=1.0)
    ax.set_yticks(y, [n[:52] for n, _ in items], fontsize=8.9)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Correlation between the activity's importance and the job's preparation level")
    ax.set_title("Seniority is not mainly about managing people")
    ax.scatter([], [], marker="s", s=90, color=C_PEOPLE, label="Managing people")
    ax.scatter([], [], marker="s", s=90, color=C_HANDS, label="Doing the work")
    ax.legend(loc="lower right", frameon=False, fontsize=9.8)
    n = list(z.values())[0]["n"]
    footnote(fig,
             f"O*NET 31.0, all {n} occupations with a job zone, {len(z)} generalised work "
             f"activities. Job zone is the preparation a job requires, education plus training "
             f"plus experience, and it is NOT position in a hierarchy: a surgeon is the top zone "
             f"and manages nobody. So this chart cannot carry the promotion argument and is not "
             f"asked to. It is here because it complicates it: what rises fastest with preparation "
             f"is interpreting and analysing information, not managing people, and the four "
             f"people-management activities sit in the middle of the pack.", y=-0.028)
    save(fig, "mg-3-what-actually-rises.png")


# ------------------------------------------------------------------ 4. what lands on other people

def chart4():
    """The third act: the promotion moves the cost of your decisions onto other people."""
    c = R["context_shift"]
    p = R["promotion"]
    items = sorted(c.items(), key=lambda kv: kv[1]["mean_shift"])
    y = np.arange(len(items))
    fig, ax = plt.subplots(figsize=(11.4, 4.4))
    ax.set_axisbelow(True)
    ax.barh(y, [v["mean_shift"] for _, v in items], height=0.6, color=RED, alpha=0.88)
    ax.set_yticks(y, [n.replace(" in Accomplishing Work Activities", "")
                       .replace(" or Company Results", "")[:48] for n, _ in items], fontsize=10)
    ax.grid(axis="y", visible=False)
    for yy, (_, v) in zip(y, items):
        ax.text(v["mean_shift"] + 0.015, yy,
                f"{v['mean_shift']:+.2f}   in {v['n_rising']} of {v['n']}",
                va="center", fontsize=9.4, color=INK2)
    ax.set_xlim(0, max(v["mean_shift"] for _, v in items) * 1.42)
    ax.set_xlabel("Change on becoming the supervisor, O*NET work context scale, 1 to 5")
    ax.set_title("What the promotion makes you responsible for")
    footnote(fig,
             f"O*NET 31.0 Work Context, same {p['n_comparisons']} supervisor comparisons as the "
             f"first chart. These five were chosen AFTER the first result was computed, unlike the "
             f"activity groupings, and the design document records that. The row that matters is "
             f"the impact of your decisions on co-workers: it rises in "
             f"{c['Impact of Decisions on Co-workers or Company Results']['n_rising']} of "
             f"{c['Impact of Decisions on Co-workers or Company Results']['n']} comparisons. "
             f"O*NET describes what a job requires. It contains nothing about whether the person "
             f"holding it is meeting the requirement, which is the subject of the last section.",
             y=-0.065)
    save(fig, "mg-4-what-lands-on-other-people.png")


if __name__ == "__main__":
    chart1(), chart2(), chart3(), chart4()
