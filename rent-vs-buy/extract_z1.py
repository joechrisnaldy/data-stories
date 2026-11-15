"""Extract the two Federal Reserve Z.1 series Post 30 uses from the full Z.1 CSV package.

The package (data/frb_z1_csv_2026-09-11.zip, release of 2026-09-11) holds one CSV of about 3.3 GB, too slow to read on
every build. This script streams it once and writes data/z1_owner_occupied_extract.csv with the quarter-end levels of:
  - LM155035015.Q  households' owner-occupied real estate at market value, including vacant land and mobile homes
  - FL155035013.Q  households' owner-occupied real estate excluding vacant land and mobile homes
profile_data.py pins both the package and the extract by sha256, so the extract can always be rebuilt and compared.

usage: python3 extract_z1.py   (run from the post folder)
"""
import csv
import hashlib
import io
import pathlib
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
PACKAGE = HERE / "data" / "frb_z1_csv_2026-09-11.zip"
PACKAGE_SHA256 = "83b8eded0bc7f9b74c0269ef503a863cee88312460fd7eef076284b98fc28c06"
OUT = HERE / "data" / "z1_owner_occupied_extract.csv"
SERIES = ("LM155035015.Q", "FL155035013.Q")
COLUMNS = ("series_name", "date", "value", "unit_mult", "long_description")


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_rows() -> list[list[str]]:
    """Stream Z1.csv inside the package and keep the rows of SERIES, columns as in COLUMNS (code instead of path)."""
    with zipfile.ZipFile(PACKAGE) as zf:
        members = zf.namelist()
        if members != ["Z1.csv"]:
            sys.exit(f"expected one member Z1.csv, found {members}")
        with zf.open("Z1.csv") as raw:
            reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8", newline=""))
            header = next(reader)
            missing = [c for c in COLUMNS if c not in header]
            if missing:
                sys.exit(f"columns {missing} not in the header {header}")
            idx = [header.index(c) for c in COLUMNS]
            rows = []
            for rec in reader:
                code = rec[idx[0]].rsplit("/", 1)[-1]
                if code in SERIES:
                    rows.append([code] + [rec[i] for i in idx[1:]])
    return rows


def main() -> None:
    got = sha256(PACKAGE)
    if got != PACKAGE_SHA256:
        sys.exit(f"{PACKAGE.name}: sha256 {got} is not the pinned {PACKAGE_SHA256}")
    rows = read_rows()
    found = sorted({r[0] for r in rows})
    if found != sorted(SERIES):
        sys.exit(f"series found {found}, expected {sorted(SERIES)}")
    rows.sort(key=lambda r: (r[0], r[1]))
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["series", "date", "value", "unit_mult", "long_description"])
        w.writerows(rows)
    for code in SERIES:
        dates = [r[1] for r in rows if r[0] == code]
        print(f"{code}: {len(dates)} rows, {dates[0]} to {dates[-1]}")
    print(f"wrote {OUT.name} sha256 {sha256(OUT)}")


if __name__ == "__main__":
    main()
