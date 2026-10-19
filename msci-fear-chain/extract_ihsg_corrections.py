"""Write data/ihsg_monthend_corrections.csv: the six months where Bank Indonesia's table III.3 disagrees
with the exchange's own publications or Bapepam's statistics (design amendment 8.6).

Precedence, fixed before the checks reported: the exchange's figure, then Bapepam's or OJK's. Each value
is read from a stored PDF in sources/ whose SHA-256 is checked first. Run from the post folder; needs
poppler's pdftotext. The analysis reads the CSV, never the PDFs.
"""
import csv
import hashlib
import re
import subprocess
from pathlib import Path

OUT = Path("data/ihsg_monthend_corrections.csv")
BAPEPAM_2007 = ("sources/bapepam_lk_statistik_pasar_modal_2007-03_week1.pdf",
                "09588c28aaa9db80c123068347a20a05f1126fbbd7b515431a89e24b7d49a10a", 16)
IDX_2007 = ("sources/idx_statistics_2007.pdf",
            "ca21468573409d7b5d5d331b19a9013ff6d5d0fa45ca2f725c460fffb83d3348", 110)
IDX_2009 = ("sources/idx_statistics_2009_revised.pdf",
            "c43d75181a0d061a1946ad5f2e329dbf2a773c0bccdd1e18d657ba3914f4b434", 8)
IDX_2021_04 = ("sources/idx_monthly_statistics_2021-04.pdf",
               "a7e19d0fca8dfea1b8b9626a3231402aafb439cce699d6eb7a66f8f7e1e2d46d", None)
MONTHS = ["Januari", "Pebruari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
          "Oktober", "November", "Desember"]


def page_text(spec) -> list[str]:
    path, sha, page = spec
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if not digest.startswith(sha):
        raise SystemExit(f"{path} does not match its frozen SHA-256")
    args = ["pdftotext", "-layout"] + (["-f", str(page), "-l", str(page)] if page else []) + [path, "-"]
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.splitlines()


def bapepam_2006(month: str) -> float:
    year = None
    for line in page_text(BAPEPAM_2007):
        parts = line.split()
        if parts and re.fullmatch(r"20\d\d", parts[0]):
            year = int(parts[0])
        elif year == 2006 and parts and parts[0] == month and len(parts) == 7:
            return float(parts[3].replace(".", "").replace(",", "."))  # Bursa Efek Jakarta, Akhir
    raise SystemExit(f"Bapepam 2006 {month} not found")


def idx_2007_q3_2006() -> float:
    lines = page_text(IDX_2007)
    start = next(i for i, l in enumerate(lines) if l.split()[:1] == ["2006"])
    q3 = next(l for l in lines[start + 1:start + 6] if l.split()[:1] == ["03"])  # OCR of 'Q3'
    return float(re.search(r"\b\d,\d{3}\.\d{3}\b", q3).group(0).replace(",", ""))


def idx_2009_march() -> float:
    close = next(l for l in page_text(IDX_2009) if l.split()[:1] == ["Close"] and len(l.split()) == 13)
    return float(close.split()[3].replace(",", ""))  # Close row: Jan, Feb, Mar, ...


def idx_2021_april() -> float:
    row = next(l for l in page_text(IDX_2021_04) if l.split()[:1] == ["30-Apr-21"])
    return float(row.split()[1].replace(",", ""))  # first index column is the JCI


ROWS = [
    ("2006-01", lambda: bapepam_2006("Januari"), "Bapepam-LK Statistik Pasar Modal 2007-03 week 1, Table 8, 2006, Akhir"),
    ("2006-02", lambda: bapepam_2006("Pebruari"), "Bapepam-LK Statistik Pasar Modal 2007-03 week 1, Table 8, 2006, Akhir"),
    ("2006-08", lambda: bapepam_2006("Agustus"), "Bapepam-LK Statistik Pasar Modal 2007-03 week 1, Table 8, 2006, Akhir"),
    ("2006-09", idx_2007_q3_2006, "IDX Statistics 2007, IDX development table, Q3 2006 composite close (Bapepam: 1534.61)"),
    ("2009-03", idx_2009_march, "IDX Statistics 2009 (revised), daily Jakarta Composite Index table, Close row, March"),
    ("2021-04", idx_2021_april, "IDX Monthly Statistics April 2021, Daily IDX Indices, 30 April 2021, JCI"),
]


def main() -> None:
    out = [(month, f(), source) for month, f, source in ROWS]
    with OUT.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["month", "ihsg_close", "source"])
        for month, value, source in out:
            w.writerow([month, f"{value:.3f}", source])
    for row in out:
        print(row)


if __name__ == "__main__":
    main()
