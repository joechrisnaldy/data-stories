"""Read Microsoft's service health record, as stored from the University of Pennsylvania ISC mirror, into CSV files.

Input:  sources/penn-ms-incidents/ms-incidents.html (stored once; see docs/data-README.src.md)
Output: data/incidents.csv  one row per incident: id, title, status and the header start and end times
        data/updates.csv    one row per update: incident, UTC time, and Microsoft's text as plain text
Only the incidents the post names are kept. Nothing is computed here; build_analysis.py reads these files.
"""
import csv
import datetime
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "sources", "penn-ms-incidents", "ms-incidents.html")
KEEP = ("EX1550543", "MO1550821", "TM1550488", "CR1551339", "PP1550869")
HEADING = re.compile(r"<h4>\s*([A-Z]{2}\d{7})\s*-\s*(.*?)</h4>", re.S)
ROW = re.compile(r'<tr><th class="[^"]*">\s*([^<:]+):\s*</th><td>(.*?)</td></tr>', re.S)
STAMP = re.compile(r"\w{3} (\w{3}) +(\d{1,2}) (\d{2}):(\d{2}):(\d{2}) (\d{4}) UTC")


def plain(fragment: str) -> str:
    """Microsoft's text without markup: line breaks become spaces, entities are decoded."""
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", fragment.replace("<br>", " "))).split())


def utc(stamp: str) -> str:
    """'Thu Nov 12 16:20:07 2026 UTC (...)' as ISO 8601 UTC."""
    m = STAMP.search(stamp)
    if not m:
        raise ValueError(f"no UTC time in {stamp[:80]!r}")
    month, day, hh, mm, ss, year = m.groups()
    t = datetime.datetime.strptime(f"{year} {month} {day} {hh}:{mm}:{ss}", "%Y %b %d %H:%M:%S")
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    with open(SOURCE, encoding="utf-8") as f:
        page = f.read()
    heads = list(HEADING.finditer(page))
    incidents, updates = [], []
    for i, h in enumerate(heads):
        ident, title = h.group(1), plain(h.group(2))
        if ident not in KEEP:
            continue
        block = page[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(page)]
        rows = [(label.strip(), body) for label, body in ROW.findall(block)]
        header = {label: plain(body) for label, body in rows[:6] if label in ("Status", "Start Time", "End Time")}
        incidents.append({"id": ident, "title": title, "status": header.get("Status", ""),
                          "start_header_utc": utc(header["Start Time"]) if "Start Time" in header else "",
                          "end_header_utc": utc(header["End Time"]) if "End Time" in header else ""})
        when = None
        for label, body in rows:
            if label == "Time":
                when = utc(body)
            elif label == "Description" and when:
                updates.append({"incident": ident, "time_utc": when, "text": plain(body)})
                when = None
    found = {r["id"] for r in incidents}
    missing = [k for k in KEEP if k not in found]
    if missing:
        raise SystemExit(f"incidents not found in the stored record: {missing}")
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    for name, rows, fields in (("incidents.csv", incidents, ["id", "title", "status", "start_header_utc", "end_header_utc"]),
                               ("updates.csv", sorted(updates, key=lambda r: (r["incident"], r["time_utc"])),
                                ["incident", "time_utc", "text"])):
        with open(os.path.join(HERE, "data", name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
    for r in incidents:
        n = sum(1 for u in updates if u["incident"] == r["id"])
        print(f"{r['id']}: {n} updates, status {r['status']}, header {r['start_header_utc']} to {r['end_header_utc']}")


if __name__ == "__main__":
    main()
