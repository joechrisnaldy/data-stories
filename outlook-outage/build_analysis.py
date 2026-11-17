"""The figures Post 31 states from Microsoft's record and the DataReportal pages: writes results.json.

Reads data/updates.csv and data/incidents.csv (written by parse_records.py from Microsoft's service health record)
and the stored DataReportal pages under sources/. Prints what it found, so prose cannot invent it.
"""
import csv
import datetime
import hashlib
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
WIB = datetime.timedelta(hours=7)                       # Jakarta, Western Indonesia Time, UTC+7
# timeline events: (key, label for the chart, a phrase Microsoft's EX1550543 update must contain)
EVENTS = [
    ("first_post", "First post", None),
    ("deployments_paused", "Deployments paused", "paused all deployments"),
    ("servers_returned", "Some servers returned to service", "returning a portion of the affected servers"),
    ("fixes_not_taking", "Fixes not taking as expected", "not taking as expected"),
    ("timeout_48h", "Mail timeout extended", "email timeout window to"),
    ("approaching_normal", "Approaching normal levels", "approaching normal levels"),
    ("final_status", "Final status", "Final status"),
]


def read(name):
    with open(os.path.join(HERE, "data", name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def when(iso):
    return datetime.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")


def sample(*parts):
    return hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:12]


def services_in(text):
    """The services an MO1550821 update names, in either of Microsoft's two formats: a list after 'services include:'
    ('- A - B - C: details'), or '- Name: impact' lines. Quick updates without a list name none."""
    info = text.split("More info :", 1)[-1].split("Scope of impact :", 1)[0].split("Current status :", 1)[0]
    named = re.findall(r"(?:^|\s)-\s?([A-Z][^:\-]{1,60}?):", info)        # Microsoft once wrote '-Name:'
    named += re.findall(r"(?:^|\s)- ([A-Z][^:\-]{1,60}?)\s+(?=- [A-Z])", info)     # a bare '- Name' item before the next
    if "include:" in info:
        for item in info.split("include:", 1)[1].split(" - "):
            name = item.split(":", 1)[0].strip(" .")
            if name and len(name) <= 60 and name[0].isupper():
                named.append(name)
    return sorted({re.sub(r"^Microsoft (?!365)", "", n.strip()) for n in named})   # 'Microsoft Teams' is Teams; 'Microsoft 365 apps' stays


def page_text(folder):
    with open(os.path.join(HERE, "sources", folder, "index.html"), encoding="utf-8") as f:
        return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", f.read())).split())


def share(text, pattern):
    hits = re.findall(pattern, text)
    if len(hits) != 1:
        raise SystemExit(f"expected one match for {pattern!r}, found {len(hits)}")
    return float(hits[0])


def main():
    updates = read("updates.csv")
    incidents = {r["id"]: r for r in read("incidents.csv")}
    ex = [u for u in updates if u["incident"] == "EX1550543"]
    t0 = when(ex[0]["time_utc"])
    events = []
    for key, label, phrase in EVENTS:
        u = ex[0] if phrase is None else next((x for x in ex if phrase in x["text"]), None)
        if u is None:
            raise SystemExit(f"no EX1550543 update contains {phrase!r}")
        t = when(u["time_utc"])
        w = t + WIB
        events.append({"key": key, "label": label, "utc": u["time_utc"], "utc_day": t.day, "utc_hour": t.hour, "utc_minute": t.minute,
                       "wib_day": w.day, "wib_hour": w.hour, "wib_minute": w.minute,
                       "wib": (t + WIB).strftime("%Y-%m-%dT%H:%M:%S+07:00"),
                       "hours": round((t - t0).total_seconds() / 3600, 1)})
    final = next(x for x in ex if "Final status" in x["text"])
    start_txt = re.search(r"Start time : \w+, (\w+ \d+, \d{4}), at (\d+:\d+ [AP]M) UTC", final["text"])
    end_txt = re.search(r"End time : \w+, (\w+ \d+, \d{4}), at (\d+:\d+ [AP]M) UTC", final["text"])
    start = datetime.datetime.strptime(" ".join(start_txt.groups()), "%B %d, %Y %I:%M %p")
    end = datetime.datetime.strptime(" ".join(end_txt.groups()), "%B %d, %Y %I:%M %p")
    mo = [u for u in updates if u["incident"] == "MO1550821"]
    lists = [(u["time_utc"], [s for s in services_in(u["text"]) if s != "Exchange Online"]) for u in mo]
    lists = [(t, s) for t, s in lists if s]
    final_mo = next(u for u in mo if "Final status" in u["text"])
    final_list = [s for s in services_in(final_mo["text"]) if s != "Exchange Online"]
    shares_g, shares_i = page_text("datareportal-2027-global-overview"), page_text("datareportal-2027-indonesia")
    results = {
        "timeline": {"t0_utc": ex[0]["time_utc"], "events": events, "jakarta_offset_hours": int(WIB.total_seconds() // 3600),
                     "impact_start_utc": start.strftime("%Y-%m-%dT%H:%MZ"), "impact_end_utc": end.strftime("%Y-%m-%dT%H:%MZ"),
                     "impact_hours": round((end - start).total_seconds() / 3600, 1),
                     "timeout_hours": int(re.search(r"email timeout window to (\d+) hours", next(x for x in ex if "email timeout window to" in x["text"])["text"]).group(1)),
                     "header_start_utc": incidents["EX1550543"]["start_header_utc"], "updates_ex": len(ex), "updates_mo": len(mo)},
        "services": {"first_utc": lists[0][0], "first_n": len(lists[0][1]), "peak_n": max(len(s) for _, s in lists),
                     "final_utc": final_mo["time_utc"], "final_n": len(final_list), "final_list": final_list,
                     "series": [{"utc": t, "n": len(s)} for t, s in lists],
                     "sample": sample("MO1550821", final_mo["time_utc"], *final_list)},
        "shares": {"email_global_pct": share(shares_g, r"with (\d+\.\d) percent of respondents to GWI.s survey answering in the affirmative"),
                   "whatsapp_global_pct": share(shares_g, r"WhatsApp claims fourth place, with (\d+\.\d) percent"),
                   "whatsapp_indonesia_pct": share(shares_i, r"(\d+\.\d)% WHATSAPP"),
                   "base_age": int(share(shares_g, r"internet users aged (\d+) and above saying they used the platform")),
                   "sample_global": "gwi-global-internet-users-16plus", "sample_indonesia": "gwi-indonesia-internet-users-16plus"},
    }
    for k in ("email_global", "whatsapp_global", "whatsapp_indonesia"):       # the same shares as fractions, for prose
        results["shares"][k] = round(results["shares"][k + "_pct"] / 100, 4)
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
        f.write("\n")
    print(json.dumps({k: v for k, v in results["timeline"].items() if k != "events"}))
    for e in events:
        print(f"  +{e['hours']:>5} h  {e['utc']}  {e['wib']}  {e['label']}")
    s = results["services"]
    print(f"services besides Exchange Online: first {s['first_n']} at {s['first_utc']}, peak {s['peak_n']}, final {s['final_n']} at {s['final_utc']}")
    print("  final list:", "; ".join(final_list))
    print("  every name any update lists:", "; ".join(sorted({n for u in mo for n in services_in(u["text"])})))
    print("shares:", results["shares"])


if __name__ == "__main__":
    main()
