"""Write data/idx_ihsg_daily_2026-10.csv from the Indonesia Stock Exchange's IDX Daily Statistics.

Source: IDX Daily Statistics for 15 and 16 October 2026 (DS261015, DS261016), page 1, block "IDX Composite
Index (IHSG)": the close, the change and the previous close. Downloaded by the owner from idx.co.id
(Market Data, Statistical Reports, Daily) on 17 October 2026 and stored in sources/. October 2026 has no
monthly or quarterly IDX file yet (design amendment 8.1). Run from the post folder; needs poppler's
pdftotext. The analysis reads the CSV, never the PDFs.
"""
import csv
import hashlib
import re
import subprocess
from datetime import date
from pathlib import Path

REPORTS = [
    (date(2026, 10, 15), Path("sources/ds_261015.pdf"),
     "5a424eea2f52688cb71119f426d5a82dc60b9c444d7d26fa17f04b2383d9dbe3"),
    (date(2026, 10, 16), Path("sources/ds_261016.pdf"),
     "08e80f11ec5fb466e6a34e430f9cc7bc60f756efe458c0dae1bf6d9b9d4c3608"),
]
OUT = Path("data/idx_ihsg_daily_2026-10.csv")
NUM = r"-?[\d,]+\.\d{3}"


def number(token: str) -> float:
    return float(token.replace(",", ""))


def read_report(day: date, pdf: Path, sha: str) -> dict:
    if hashlib.sha256(pdf.read_bytes()).hexdigest() != sha:
        raise SystemExit(f"{pdf} does not match its frozen SHA-256")
    lines = subprocess.run(["pdftotext", "-layout", "-f", "1", "-l", "1", str(pdf), "-"],
                           check=True, capture_output=True, text=True).stdout.splitlines()
    heading = f"{day.day} {day.strftime('%B %Y')}"
    if not any(line.strip().endswith(heading) for line in lines[:3]):
        raise SystemExit(f"{pdf}: report date is not {heading}")
    start = next(i for i, line in enumerate(lines) if "IDX Composite Index (IHSG)" in line)
    close = prev = None
    for i, line in enumerate(lines[start:], start):
        m = re.match(rf"\s*({NUM})\s+({NUM})\s+\((-?[\d.]+)%\)", line)
        if m and close is None:
            close, change, change_pct = number(m[1]), number(m[2]), float(m[3])
        if close is not None and re.match(r"\s*Previous\s+Highest\s+Lowest", line):
            prev = number(next(l for l in lines[i + 1:] if l.strip()).split()[0])
            break
    if close is None or prev is None:
        raise SystemExit(f"{pdf}: IHSG block not found")
    if abs(close - prev - change) > 0.0005:
        raise SystemExit(f"{pdf}: close {close} minus previous {prev} is not the printed change {change}")
    return dict(date=day.isoformat(), ihsg_close=close, previous_close=prev, change=change,
                change_pct_printed=change_pct, source=f"IDX Daily Statistics {pdf.stem.upper().replace('_', '')}, page 1")


def main() -> None:
    rows = [read_report(*spec) for spec in REPORTS]
    if rows[1]["previous_close"] != rows[0]["ihsg_close"]:
        raise SystemExit("16 October's previous close is not 15 October's close")
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({**r, **{k: f"{r[k]:.3f}" for k in ("ihsg_close", "previous_close", "change")}})
    print(f"wrote {OUT}: " + "; ".join(f"{r['date']} close {r['ihsg_close']:.3f} ({r['change_pct_printed']}%)"
                                       for r in rows))


if __name__ == "__main__":
    main()
