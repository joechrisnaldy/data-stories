"""The four charts of Post 32, drawn from results.json only (written by build_analysis.py).

oh-1-sleep-by-hours.png   sleep, and sports, exercise and recreation, by usual weekly hours (time-use survey)
oh-2-output-curve.png     weekly output against weekly hours, Pencavel's historical estimate, as productive hours
                          (the line is computed by model.py from the knot and peak in results.json)
oh-3-cost-test.png        two people at 60 hours against three at 40: productive hours and cost per productive hour
oh-4-two-rules.png        the same 60-hour week under the US rule and Indonesia's law
Every printed figure is formatted from a results key; nothing is typed.
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from model import Curve, productive_hours  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "charts")
INK, MUTED, ACCENT, LIGHT = "#222222", "#777777", "#c0392b", "#cccccc"
plt.rcParams.update({"axes.unicode_minus": False, "font.family": "DejaVu Sans", "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False})


def load() -> dict:
    with open(os.path.join(HERE, "results.json"), encoding="utf-8") as f:
        return json.load(f)


def save(fig, name: str, note: str) -> None:
    fig.text(0.01, 0.01, note, fontsize=8.5, color=MUTED, ha="left", va="bottom", wrap=True)
    fig.savefig(os.path.join(OUT, name), dpi=150)
    plt.close(fig)


def label_bars(ax, xs, values, places: int) -> None:
    for x, v in zip(xs, values):
        ax.text(x, v, f"{v:.{places}f}", ha="center", va="bottom", fontsize=10, color=INK)


def sleep_by_hours(r: dict) -> None:
    s = r["survey"]
    bands = list(s["bands"].values())
    xs = range(len(bands))
    g = s["gap"]
    colors = [ACCENT if b["label"] == g["long_label"] else INK if b["label"] == g["short_label"] else MUTED
              for b in bands]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.6))
    panels = ((axes[0], [b["sleep_hours"] for b in bands], 1, "Sleep, hours a day"),
              (axes[1], [b["sports_min"] for b in bands], 0, "Taking part in sports, exercise and recreation, minutes a day"))
    for ax, values, places, title in panels:
        ax.bar(xs, values, color=colors, width=0.62)
        label_bars(ax, xs, values, places)
        ax.set_xticks(list(xs), [b["label"] for b in bands])
        ax.set_xlabel("Usual hours worked a week")
        ax.set_title(title, loc="left", fontsize=12, color=INK)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
    fig.suptitle(f"Usual weeks of {g['long_label']} hours: about {g['sleep_min']:.0f} minutes less sleep a day "
                 f"than weeks of {g['short_label']} hours", x=0.01, ha="left", fontsize=14, color=INK)
    fig.subplots_adjust(left=0.03, right=0.98, top=0.82, bottom=0.2, wspace=0.12)
    save(fig, "oh-1-sleep-by-hours.png",
         "U.S. Bureau of Labor Statistics, American Time Use Survey, analysed by the author: employed people at "
         f"work aged {s['age_min']} to {s['age_max']}, diaries from {s['first_year']} to {s['last_year']}, "
         f"{s['n']:,} respondents; weighted averages per day, weekends included. Sleep includes time recorded as sleeplessness.")


def output_curve(r: dict) -> None:
    c, sc = r["curve"], r["scenario"]
    curve = Curve(c["knot"], c["peak"])
    steps = int((c["data_max"] - c["data_min"]) * 4)
    hours = [c["data_min"] + i / 4 for i in range(steps + 1)]
    fig, ax = plt.subplots(figsize=(12, 5.6))
    ax.plot(hours, hours, color=LIGHT, lw=2, ls="--", label="If each hour counted in full")
    ax.plot(hours, [productive_hours(h, curve) for h in hours], color=INK, lw=2.4,
            label="Pencavel's estimate, column (ii)")
    for h, color in ((sc["short_week"], INK), (sc["long_week"], ACCENT)):
        p = productive_hours(h, curve)
        ax.plot(h, p, "o", color=color, ms=9, zorder=3)
        ax.annotate(f"{h:.0f} hours worked: {p:.1f} productive hours", (h, p), textcoords="offset points",
                    xytext=(10, -22), fontsize=10, color=color)
    ax.axvline(c["knot"], color=MUTED, lw=0.8, ls=":")
    ax.axvline(c["peak"], color=MUTED, lw=0.8, ls=":")
    ax.text(c["knot"], ax.get_ylim()[1], f" output stops keeping pace at {c['knot']:.0f} hours", va="top",
            fontsize=9.5, color=MUTED)
    ax.text(c["peak"], ax.get_ylim()[0], f" peak at about {c['peak']:.0f} hours", va="bottom", fontsize=9.5,
            color=MUTED)
    ax.set_xlabel("Hours worked a week")
    ax.set_ylabel("Weekly output, in productive hours")
    ax.legend(frameon=False, loc="upper left")
    ax.set_title("Past a point, longer weeks add little output", loc="left", fontsize=14, color=INK)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.2)
    save(fig, "oh-2-output-curve.png",
         "Pencavel's estimates for British munition workers in the First World War, weekly hours "
         f"from {c['data_min']:g} to {c['data_max']:g}. Productive hours count output at the pace of a week under "
         f"{c['knot']:.0f} hours. A historical estimate, used in this post as an assumption, not a measurement of "
         "today's work.")


def cost_test(r: dict) -> None:
    sc, c, ne, ex = r["scenario"], r["curve"], r["nonexempt"], r["exempt"]
    long_tick = f"Team A: {sc['long_people']} people,\n{sc['long_week']:.0f} hours each"
    short_tick = f"Team B: {sc['short_people']} people,\n{sc['short_week']:.0f} hours each"
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5.6))
    left.bar([0, 1], [c["long_team"], c["short_team"]], color=[ACCENT, INK], width=0.55)
    label_bars(left, [0, 1], [c["long_team"], c["short_team"]], 0)
    left.set_xticks([0, 1], [long_tick, short_tick])
    left.set_title("Productive hours a week", loc="left", fontsize=12, color=INK)
    width = 0.36
    groups = (("Overtime owed\n(non-exempt)", ne), ("Same salary at any hours\n(exempt)", ex))
    for i, (name, case) in enumerate(groups):
        right.bar(i - width / 2, case["long_per_hour"], width, color=ACCENT, label="Team A" if i == 0 else None)
        right.bar(i + width / 2, case["short_per_hour"], width, color=INK, label="Team B" if i == 0 else None)
        label_bars(right, [i - width / 2, i + width / 2], [case["long_per_hour"], case["short_per_hour"]], 2)
    right.set_xticks([0, 1], [g[0] for g in groups])
    right.set_title("Cost per productive hour, US dollars", loc="left", fontsize=12, color=INK)
    right.set_ylim(0, max(case[k] for _, case in groups for k in ("long_per_hour", "short_per_hour")) * 1.3)
    right.legend(frameon=False, loc="upper center", ncol=2)
    for ax in (left, right):
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
    fig.suptitle(f"Both teams work {sc['team_hours']:.0f} hours; on Pencavel's curve, the shorter weeks deliver more "
                 "output",
                 x=0.01, ha="left", fontsize=14, color=INK)
    fig.subplots_adjust(left=0.03, right=0.98, top=0.82, bottom=0.2, wspace=0.12)
    save(fig, "oh-3-cost-test.png",
         "Output: Pencavel's estimates, as in the previous chart. Costs: U.S. Bureau of Labor Statistics, employer "
         "costs for full-time private industry workers; overtime pay: U.S. Department of Labor. Benefits counted in "
         "full as a cost per person. The author's model.")


def two_rules(r: dict) -> None:
    us, idn, sc = r["rules"]["us"], r["rules"]["indonesia"], r["scenario"]
    if idn["first_hour_rate"] != sc["overtime_rate"]:
        raise SystemExit("chart 4 labels both countries' first overtime rate with the US rate; they now differ")
    rows = (("United States", us["regular_hours"], us["overtime_hours"], 0, us["pay_in_hourly_wages"]),
            ("Indonesia", idn["regular_hours"], idn["first_overtime_hours"], idn["later_overtime_hours"],
             idn["pay_in_hourly_wages"]))
    fig, ax = plt.subplots(figsize=(12, 5.6))
    for y, (name, regular, at_one_half, at_two, pay) in enumerate(rows):
        ax.barh(y, regular, color=MUTED, height=0.5, label="Regular hours" if y == 0 else None)
        for left, width in ((0, regular), (regular, at_one_half), (regular + at_one_half, at_two)):
            if width:
                ax.text(left + width / 2, y, f"{width:g}", ha="center", va="center", color="white", fontsize=10.5)
        ax.barh(y, at_one_half, left=regular, color=INK, height=0.5,
                label=f"Overtime paid at {sc['overtime_rate']:.1f} times the hourly wage" if y == 0 else None)
        ax.barh(y, at_two, left=regular + at_one_half, color=ACCENT, height=0.5,
                label=f"Overtime paid at {idn['later_rate']:g} times the hourly wage" if y == 1 else None)
        ax.text(regular + at_one_half + at_two, y, f"  pay: {pay:g} hours of wages", va="center", fontsize=10.5)
    cap = idn["regular_hours"] + idn["cap_week"]
    ax.plot([cap, cap], [0.65, 1.35], color=ACCENT, lw=2)
    ax.text(cap, 1.42, f"Indonesia's weekly limit: {cap:.0f} hours", ha="center", fontsize=10, color=ACCENT)
    ax.set_yticks([0, 1], [row[0] for row in rows])
    ax.set_xlabel("Hours in the week")
    ax.set_ylim(-0.6, 2.2)
    ax.set_xlim(0, sc["long_week"] * 1.3)
    ax.legend(frameon=False, loc="upper left", ncol=3, fontsize=9.5)
    ax.set_title(f"The same {sc['long_week']:.0f}-hour week under each country's rule", loc="left", fontsize=14,
                 color=INK)
    fig.subplots_adjust(left=0.12, right=0.98, top=0.9, bottom=0.2)
    save(fig, "oh-4-two-rules.png",
         "U.S. Department of Labor, overtime fact sheet (Fair Labor Standards Act; no limit on weekly hours for "
         f"employees aged {us['no_limit_age']} and older). Indonesia: the labour protection law, articles on working "
         "time and overtime. Pay in hours of the regular hourly wage.")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    r = load()
    sleep_by_hours(r)
    output_curve(r)
    cost_test(r)
    two_rules(r)


if __name__ == "__main__":
    main()
