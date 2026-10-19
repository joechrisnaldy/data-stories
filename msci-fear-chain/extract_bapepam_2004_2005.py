"""Write data/bapepam_ihsg_monthend_2004_2005.csv from Bapepam's weekly Statistik Pasar Modal.

Source: Bapepam (Riset, Biro PIR), Statistik Pasar Modal, 28 November to 2 December 2005, Table 8
"Indeks Harga Saham Gabungan (IHSG)", Bursa Efek Jakarta, column Akhir (period-end close); an Internet
Archive copy of the OJK archive file Documents/408.pdf, stored in sources/. Bank Indonesia's table
III.3 has only December of 2004 and 2005; this fills January 2004 to November 2005. Run from the post
folder; needs poppler's pdftotext. The analysis reads the CSV, never the PDF.
"""
import csv
import hashlib
import re
import subprocess
from pathlib import Path

PDF = Path("sources/bapepam_statistik_pasar_modal_2005-11_week4.pdf")
PDF_SHA256 = "95921cd7bb5d8f53398d4053ffcd17329b90f136e79afd259415716a9231480d"
PAGE = 16
OUT = Path("data/bapepam_ihsg_monthend_2004_2005.csv")
MONTHS = ["Januari", "Pebruari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
          "Oktober", "November", "Desember"]


def number(token: str) -> float:
    return float(token.replace(".", "").replace(",", "."))


def main() -> None:
    if hashlib.sha256(PDF.read_bytes()).hexdigest() != PDF_SHA256:
        raise SystemExit(f"{PDF} does not match its frozen SHA-256")
    text = subprocess.run(["pdftotext", "-layout", "-f", str(PAGE), "-l", str(PAGE), str(PDF), "-"],
                          check=True, capture_output=True, text=True).stdout
    rows, year = [], None
    for line in text.splitlines():
        head = line.strip()
        if re.fullmatch(r"200[45]", head) or re.match(r"200[45]\s+[\d.,]+\s+[\d.,]+\s+[\d.,]+", head):
            year = int(head[:4])
            continue
        parts = head.split()
        if year and parts and parts[0] in MONTHS and len(parts) == 7:
            month = MONTHS.index(parts[0]) + 1
            rows.append((f"{year}-{month:02d}", number(parts[3])))  # Bursa Efek Jakarta, Akhir
    want = [f"2004-{m:02d}" for m in range(1, 13)] + [f"2005-{m:02d}" for m in range(1, 12)]
    if [r[0] for r in rows] != want:
        raise SystemExit(f"unexpected months: {[r[0] for r in rows]}")
    with OUT.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["month", "ihsg_close", "source"])
        for month, value in rows:
            w.writerow([month, f"{value:.2f}", "Bapepam Statistik Pasar Modal 2005-11 week 4, Table 8, Akhir"])
    print(f"wrote {OUT}: {len(rows)} months, {rows[0]} .. {rows[-1]}")


if __name__ == "__main__":
    main()
