"""Write docs/ihsg-checks/comparison_2023_2026.csv: Bank Indonesia's IHSG month-end close (SEKI Table III.3, as the
build reads it) against the last daily close of the same month in OJK's Portal Data, January 2023 to Bank
Indonesia's last month. Bank Indonesia prints two decimals and OJK three, so a month matches when they differ by
less than 0.01. Run from the post folder; it fails if any month does not match.
"""
import csv
from pathlib import Path

from build_analysis import read_ihsg, read_ojk_daily

OUT = Path("docs/ihsg-checks/comparison_2023_2026.csv")
TOL = 0.01


def main() -> None:
    ihsg, _ = read_ihsg()
    ojk = read_ojk_daily()
    last = ojk.groupby(ojk.index.to_period("M")).tail(1)
    by_month = {d.to_period("M"): (d, v) for d, v in last.items()}
    rows = []
    for m in ihsg.index[ihsg.index >= "2023-01"]:
        day, close = by_month[m]
        diff = close - ihsg[m]
        rows.append(dict(month=str(m), bi=f"{ihsg[m]:.2f}", ojk_last_close=f"{close:.3f}", ojk_date=str(day.date()),
                         difference=f"{diff:+.3f}", match="MATCH" if abs(diff) < TOL else "DIFFER"))
    bad = [r["month"] for r in rows if r["match"] != "MATCH"]
    if bad:
        raise SystemExit(f"months that do not match: {bad}")
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT}: {len(rows)} months, {rows[0]['month']} to {rows[-1]['month']}, all match")


if __name__ == "__main__":
    main()
