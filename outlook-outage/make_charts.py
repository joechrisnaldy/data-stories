"""The three charts of Post 31, drawn from results.json only (written by build_analysis.py).

oo-1-timeline.png        the outage in Microsoft's own record, hours from its first post, UTC and Jakarta time
oo-2-email-vs-whatsapp.png  share of internet users aged 16+ who used each in the past month (GWI via DataReportal)
oo-3-many-doors.png      services besides Exchange Online that Microsoft listed as impacted, as the list changed
Every printed figure is formatted from a results key; nothing is typed.
"""
import datetime
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "charts")
INK, MUTED, ACCENT, SHADE = "#222222", "#777777", "#c0392b", "#f3d9d6"
plt.rcParams.update({"axes.unicode_minus": False, "font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False})


def load():
    with open(os.path.join(HERE, "results.json"), encoding="utf-8") as f:
        return json.load(f)


def utc(iso):
    return datetime.datetime.strptime(iso.replace("Z", ""), "%Y-%m-%dT%H:%M:%S" if iso.count(":") == 2 else "%Y-%m-%dT%H:%M")


def clock(t):
    return t.strftime("%a %d %b %H:%M")


def save(fig, name, note):
    fig.text(0.01, 0.01, note, fontsize=8.5, color=MUTED, ha="left", va="bottom", wrap=True)
    fig.savefig(os.path.join(OUT, name), dpi=150)
    plt.close(fig)


def timeline(r):
    tl = r["timeline"]
    t0 = utc(tl["t0_utc"])
    end_h = (utc(tl["impact_end_utc"]) - t0).total_seconds() / 3600
    start_h = (utc(tl["impact_start_utc"]) - t0).total_seconds() / 3600
    last = tl["events"][-1]["hours"]
    fig, ax = plt.subplots(figsize=(12, 5.6))
    ax.axvspan(start_h, end_h, color=SHADE, zorder=0)
    ax.text((start_h + end_h) / 2, -1.25, f"Microsoft's stated impact window: {tl['impact_hours']:.1f} hours",
            ha="center", va="center", color=ACCENT, fontsize=10)
    ax.axhline(0, color=INK, lw=1)
    for i, e in enumerate(tl["events"]):
        y = 0.9 if i % 2 == 0 else -0.9
        ax.plot([e["hours"], e["hours"]], [0, y * 0.82], color=MUTED, lw=0.8)
        ax.plot(e["hours"], 0, "o", color=ACCENT if e["key"] in ("first_post", "final_status") else INK, ms=6, zorder=3)
        t = utc(e["utc"])
        label = e["label"] + (f" to {tl['timeout_hours']} hours" if e["key"] == "timeout_48h" else "")
        ax.text(e["hours"], y, f"{label}\n{clock(t)} UTC\n{clock(t + datetime.timedelta(hours=7))} Jakarta",
                ha="center", va="center", fontsize=8.8)
    ax.set_ylim(-1.35, 1.35)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlim(-2, last + 2)
    ax.set_xticks(range(0, int(last) + 5, 5))
    ax.set_xlabel("Hours after Microsoft's first post on the mailbox incident")
    ax.set_title("The outage in Microsoft's own record", loc="left", fontsize=14, color=INK)
    fig.subplots_adjust(left=0.03, right=0.98, top=0.88, bottom=0.2)
    save(fig, "oo-1-timeline.png",
         "Microsoft service health record, incident EX1550543, "
         "as republished by the University of Pennsylvania ISC. " f"Jakarta is UTC+{tl['jakarta_offset_hours']}.")


def shares(r):
    s = r["shares"]
    bars = [("Email,\nGWI's surveyed markets", s["email_global_pct"]), ("WhatsApp,\nGWI's surveyed markets", s["whatsapp_global_pct"])]
    fig, ax = plt.subplots(figsize=(9, 5.6))
    xs = range(len(bars))
    ax.bar(xs, [v for _, v in bars], color=[MUTED, INK], width=0.6)
    for x, (_, v) in zip(xs, bars):
        ax.text(x, v + 1.5, f"{v:.1f}%", ha="center", fontsize=12)
    ax.set_xticks(list(xs), [k for k, _ in bars])
    ax.set_ylim(0, 100)
    ax.set_ylabel(f"Share of internet users aged {s['base_age']}+ (%)")
    ax.set_title("Who used it in the past month", loc="left", fontsize=14, color=INK)
    fig.subplots_adjust(left=0.1, right=0.97, top=0.9, bottom=0.24)
    save(fig, "oo-2-email-vs-whatsapp.png",
         "GWI survey data via DataReportal, Digital 2027 Global Overview. Self-reported; "
         "China included, Russia excluded.")


def doors(r):
    sv = r["services"]
    t0 = utc(sv["series"][0]["utc"])
    xs = [(utc(p["utc"]) - t0).total_seconds() / 3600 for p in sv["series"]]
    ys = [p["n"] for p in sv["series"]]
    fig, ax = plt.subplots(figsize=(12, 5.6))
    ax.step(xs, ys, where="post", color=ACCENT, lw=2)
    ax.plot(xs, ys, "o", color=ACCENT, ms=4)
    ax.annotate(f"{sv['first_n']} services at Microsoft's first post", (xs[0], ys[0]), xytext=(8, -18), textcoords="offset points", fontsize=9.5)
    ax.annotate(f"{sv['final_n']} in the final status", (xs[-1], ys[-1]), xytext=(-140, -22), textcoords="offset points", fontsize=9.5)
    ax.set_ylim(0, sv["peak_n"] + 3)
    ax.set_xticks(range(0, int(max(xs)) + 5, 5))
    ax.set_xlabel("Hours after Microsoft's first post on the multi-service incident (MO1550821)")
    ax.set_ylabel("Services listed as impacted")
    ax.set_title("One dependency, many doors: services besides mail that Microsoft listed as impacted", loc="left", fontsize=13, color=INK)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.18)
    save(fig, "oo-3-many-doors.png",
         "Microsoft service health record, incident MO1550821, as republished by the University of Pennsylvania ISC. Listed as impacted means "
         "features that interact with Exchange Online were affected, not that the service was down.")


def main():
    os.makedirs(OUT, exist_ok=True)
    r = load()
    timeline(r)
    shares(r)
    doors(r)
    print("wrote", ", ".join(sorted(f for f in os.listdir(OUT) if f.endswith(".png"))))


if __name__ == "__main__":
    main()
