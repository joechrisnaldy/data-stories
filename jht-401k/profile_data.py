"""Data profile for Post 28: each file's coverage, gaps and key columns, then the exact input rows the
analysis will read.

Every file is frozen by its SHA-256 (docs/data-README.src.md says where each comes from and how to fetch
it again); a file that does not match stops the script. This prints inputs only: none of the design's
rules (R1 to R8 in docs/2026-10-21-jht-401k-design.md) is applied here.
"""

import csv
import hashlib
import os
import re

import openpyxl
import pandas as pd
import xlrd

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

FILES = {
    "damodaran": ("damodaran_histretSP.xls", "28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69"),
    "cpi_idn": ("imf_cpi_idn_m.csv", "b3ba15f60d304316b78adedd37229ff945c8669b67321f9284196e564071c20b"),
    "cpi_usa": ("imf_cpi_usa_m.csv", "9789f725405061e7d38fcc1d78fe7cbf7daf9254e13c1f185733f7850f900c17"),
    "cpf_contrib": ("cpf_contribution_rates.csv", "c4529a8e3cb1fb364dcb7d1279dbaf8ee1f73212b7e335d8b711ef735925d2f2"),
    "cpf_alloc": ("cpf_allocation_rates.csv", "4cb1fc28020c2b41ed12c8bcc64983a185db54c227352328f070ffe3e1c03b04"),
    "ilo": ("ilo_idn_employment_by_status.csv", "73572b2829c2fae8e24396d0580fb9f838d707e66cfc3e03d08b9c221396cdb6"),
    # design amendment A1: Post 27's file (msci-fear-chain/data/Data Inflasi.xlsx), the same hash it pins
    "bi_inflasi": ("bi_data_inflasi.xlsx", "5c79086509b6c19f90c5e3e835c5dcc40a02d322087d94e1c2a30a17e0280217"),
    # written by extract_jht.py from docs/jht-manifest.csv; the build refuses a copy that changed since
    "jht_rates": ("jht_rates.csv", "4a6ab8b769536e5c66aa0bbbc657563bfde91f58b12fcbfd38b8014f7f37351f"),
}

GROWTH_YEARS = range(2005, 2021)        # design R1: the growth window
CPI_YEARS = range(2004, 2021)           # R2 to R6 need the year before the window too
CPF_IN_FORCE = "2026-01"                # design R7: rates in force on 1 January 2026
CPF_MAX_AGE = 55                        # design R7: workers aged 55 and under
ILO_YEARS = range(2015, 2026)

DAMODARAN_SHEET = "Returns by year"
DAMODARAN_COLUMNS = ("S&P 500 (includes dividends)", "US T. Bond (10-year)")
CPI_DATAFLOW = "IMF.STA:CPI(5.0.0)"
CPI_INDEX_TYPE = "CPI"
INDONESIAN_MONTHS = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
                     "Oktober", "November", "Desember"]
INFLASI_PLACEHOLDER = (pd.Period("2002-12", "M"), "0,00 %")    # the file's last row; not a published rate
ILO_EMPLOYEES = "STE_AGGREGATE_EES: Employees"
ILO_COLS = {"area": "REF_AREA: Reference area", "measure": "MEASURE: Measure", "sex": "SEX: Sex",
            "ste": "STE: Status in employment", "year": "TIME_PERIOD: Time period",
            "status": "OBS_STATUS: Observation status", "source": "SOURCE: Source",
            "unit": "UNIT_MEASURE: Unit of measure", "mult": "UNIT_MULT: Unit multiplier"}


def path(key: str) -> str:
    name, digest = FILES[key]
    p = os.path.join(DATA, name)
    with open(p, "rb") as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    if got != digest:
        raise SystemExit(f"{name}: sha256 {got} is not the vetted file {digest}")
    return p


def section(title: str) -> None:
    print(f"\n=== {title} ===")


# --- Damodaran: annual returns ------------------------------------------------------------------------

def read_damodaran() -> tuple[pd.DataFrame, dict]:
    """Year rows of 'Returns by year', columns found by their header text. Returns the frame and, per
    column, its header as written and its Excel column letter."""
    sh = xlrd.open_workbook(path("damodaran")).sheet_by_name(DAMODARAN_SHEET)
    hdr = next((r for r in range(sh.nrows) if sh.cell_value(r, 0) == "Year"), None)
    if hdr is None:
        raise SystemExit(f"{FILES['damodaran'][0]}: no 'Year' header row on {DAMODARAN_SHEET!r}")
    heads = [str(v) for v in sh.row_values(hdr)]
    absent = [h for h in DAMODARAN_COLUMNS if h not in heads]
    if absent:
        raise SystemExit(f"{FILES['damodaran'][0]}: headers {absent} not found on {DAMODARAN_SHEET!r}")
    cols = {h: heads.index(h) for h in DAMODARAN_COLUMNS}      # first exact match: the annual return
    rows = []
    for r in range(hdr + 1, sh.nrows):
        year = sh.cell_value(r, 0)
        if not isinstance(year, float):
            break
        rows.append({"year": int(year), **{h: sh.cell_value(r, c) for h, c in cols.items()}})
    meta = {"header_row": hdr + 1, "letters": {h: xlrd.colname(c) for h, c in cols.items()}}
    return pd.DataFrame(rows).set_index("year"), meta


def profile_damodaran() -> None:
    section("damodaran_histretSP.xls")
    df, meta = read_damodaran()
    years = df.index.tolist()
    missing = sorted(set(range(years[0], years[-1] + 1)) - set(years))
    print(f"sheet {DAMODARAN_SHEET!r}, header row {meta['header_row']}")
    for h, letter in meta["letters"].items():
        blanks = int(df[h].apply(lambda v: not isinstance(v, float)).sum())
        print(f"  column {letter}: {h!r}  non-numeric cells {blanks}")
    print(f"years {years[0]} to {years[-1]}  rows {len(years)}  missing years {missing}")
    print(f"rows used (window {GROWTH_YEARS.start} to {GROWTH_YEARS.stop - 1}), as stored (fraction of 1):")
    print(f"  {'Year':<6}" + "".join(f"{h:>32}" for h in DAMODARAN_COLUMNS))
    for y in GROWTH_YEARS:
        print(f"  {y:<6}" + "".join(f"{float(df.at[y, h])!r:>32}" for h in DAMODARAN_COLUMNS))
    print(f"note: the {years[-1]} row is outside the window; its quirks are in docs/data-README.src.md")


# --- IMF CPI: headline index, monthly -----------------------------------------------------------------

def read_cpi(key: str) -> tuple[pd.Series, dict]:
    """Headline (all items, COICOP _T) index (IX), monthly, from an IMF SDMX-CSV file."""
    with open(path(key), encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    flows = {r["DATAFLOW"] for r in rows}
    if flows != {CPI_DATAFLOW}:
        raise SystemExit(f"{FILES[key][0]}: dataflow {flows}, expected {CPI_DATAFLOW}")
    ix = [r for r in rows if r["INDEX_TYPE"] == CPI_INDEX_TYPE and r["COICOP_1999"] == "_T"
          and r["TYPE_OF_TRANSFORMATION"] == "IX" and r["FREQUENCY"] == "M" and r["OBS_VALUE"].strip()]
    countries = {r["COUNTRY"] for r in ix}
    if len(countries) != 1:
        raise SystemExit(f"{FILES[key][0]}: headline index rows carry COUNTRY {sorted(countries)}, expected one")
    s = pd.Series({pd.Period(r["TIME_PERIOD"].replace("-M", "-"), "M"): float(r["OBS_VALUE"]) for r in ix})
    if len(s) != len(ix):
        raise SystemExit(f"{FILES[key][0]}: duplicate months in the headline index")
    meta = {
        "rows": len(rows),
        "series": sorted({(r["COICOP_1999"], r["TYPE_OF_TRANSFORMATION"], r["FREQUENCY"]) for r in rows}),
        "country": sorted({r["COUNTRY"] for r in ix}),
        "reference": sorted({r["REFERENCE_PERIOD"] for r in ix}),
        "derivation": sorted({r["DERIVATION_TYPE"] for r in ix}),
        "published": sorted({r["PUBLICATION_DATE"] for r in ix}),
        "raw": {pd.Period(r["TIME_PERIOD"].replace("-M", "-"), "M"): r["OBS_VALUE"] for r in ix},
    }
    return s.sort_index(), meta


def profile_cpi(key: str) -> None:
    section(FILES[key][0])
    s, meta = read_cpi(key)
    gaps = pd.period_range(s.index[0], s.index[-1], freq="M").difference(s.index)
    print(f"rows {meta['rows']}  series in file (COICOP, transformation, frequency): {meta['series']}")
    print(f"headline IX: country {meta['country']}  reference period {meta['reference']}  "
          f"derivation {meta['derivation']}  publication date {meta['published']}")
    print(f"headline IX months {s.index[0]} to {s.index[-1]}  values {len(s)}  "
          f"missing months {[str(p) for p in gaps]}")
    print(f"rows used ({CPI_YEARS.start} to {CPI_YEARS.stop - 1}): December value as stored, and the annual "
          "average of the twelve monthly values")
    for y in CPI_YEARS:
        months = s[[p for p in s.index if p.year == y]]
        if len(months) != 12:
            raise SystemExit(f"{FILES[key][0]}: {y} has {len(months)} monthly values")
        dec = pd.Period(f"{y}-12", "M")
        print(f"  {y}  December {meta['raw'][dec]:<22} annual average {float(months.mean())!r}")


# --- Bank Indonesia, Data Inflasi: BPS's published inflation, year on year (design amendment A1) -------------

def read_published_inflation() -> tuple[pd.Series, dict]:
    """BPS's published headline inflation, year on year, percent, by month, from Bank Indonesia's Data Inflasi
    file. The parsing and its three stops (the known placeholder row, a repeated month, a gap) are Post 27's
    household.read_published_inflation (msci-fear-chain/household.py), reused as written; this copy also keeps
    each cell as stored, the sheet name and the header row, for the profile to print."""
    ws = openpyxl.load_workbook(path("bi_inflasi"), read_only=True, data_only=True).active
    out, raw, header = {}, {}, None
    for row in ws.iter_rows(values_only=True):
        label, value = (row[1], row[2]) if len(row) > 2 else (None, None)
        if row and row[0] == "No":
            header = row
        m = re.fullmatch(r"(\w+) (\d{4})", str(label or "").strip())
        if not m or m.group(1) not in INDONESIAN_MONTHS:
            continue
        p = pd.Period(year=int(m.group(2)), month=INDONESIAN_MONTHS.index(m.group(1)) + 1, freq="M")
        if p == INFLASI_PLACEHOLDER[0]:
            if str(value).strip() != INFLASI_PLACEHOLDER[1]:
                raise SystemExit("Data Inflasi: the December 2002 row is no longer the known placeholder")
            continue
        if p in out:
            raise SystemExit(f"Data Inflasi: {p} appears twice")
        out[p] = float(str(value).replace("%", "").strip().replace(",", "."))
        raw[p] = value
    s = pd.Series(out).sort_index()
    if len(pd.period_range(s.index[0], s.index[-1], freq="M")) != len(s):
        raise SystemExit("Data Inflasi: months are not one unbroken run")
    return s.rename("published_yoy_pct"), {"sheet": ws.title, "header": header, "raw": raw}


def profile_inflasi() -> None:
    section(FILES["bi_inflasi"][0])
    s, meta = read_published_inflation()
    print(f"sheet {meta['sheet']!r}  header row {list(meta['header'] or [])}")
    print(f"months {s.index[0]} to {s.index[-1]}  values {len(s)}, one unbroken run (checked)  "
          f"excluded: the {INFLASI_PLACEHOLDER[0]} placeholder row {INFLASI_PLACEHOLDER[1]!r}")
    print(f"rows used ({CPI_YEARS.start} to {CPI_YEARS.stop - 1}): December, year on year, percent, as stored "
          "and as read")
    for y in CPI_YEARS:
        dec = pd.Period(f"{y}-12", "M")
        if dec not in s.index:
            raise SystemExit(f"{FILES['bi_inflasi'][0]}: no December {y}")
        print(f"  {y}  December {meta['raw'][dec]!r:<10} read as {float(s[dec])!r}")


# --- CPF Board: contribution and allocation rates -----------------------------------------------------

def upper_age(group: str) -> int | None:
    """The top age of a CPF age-group label ('35 years & below' is 35, 'Above 50 - 55 years' is 55); None
    for an open-ended group ('Above 70 years')."""
    m = re.fullmatch(r"(\d+) years & below|Above \d+ - (\d+) years|Above \d+ years", group)
    if m is None:
        raise SystemExit(f"unrecognised CPF age group {group!r}")
    top = m.group(1) or m.group(2)
    return int(top) if top else None


def in_force(df: pd.DataFrame) -> pd.DataFrame:
    """The rows in force on CPF_IN_FORCE: for each age group, every row of its latest effective date on or
    before that month (a table replaces the previous one whole, so a dropped account does not linger)."""
    live = df[df["effective_from"] <= CPF_IN_FORCE]
    latest = live.groupby("age_grp")["effective_from"].transform("max")
    return live[live["effective_from"] == latest]


def profile_cpf_table(key: str, party_col: str, rate_col: str, unit: str) -> None:
    section(FILES[key][0])
    df = pd.read_csv(path(key), dtype={"effective_from": str})
    dates = sorted(df["effective_from"].unique())
    print(f"columns {df.columns.tolist()}  rows {len(df)}  unit of {rate_col!r}: {unit}")
    print(f"effective dates {dates[0]} to {dates[-1]}  distinct {len(dates)}  "
          f"blank cells {int(df.isna().sum().sum())}")
    print(f"age groups {sorted(df['age_grp'].unique(), key=lambda g: (upper_age(g) or 999))}")
    print(f"{party_col} values {sorted(df[party_col].unique())}")
    per_value = df.groupby(party_col)["effective_from"].agg(["min", "max", "count"])
    print("rows per value (first date, last date, count):")
    for v, r in per_value.iterrows():
        print(f"  {v:<12} {r['min']} {r['max']} {r['count']}")
    young = df[df["age_grp"].map(lambda g: (upper_age(g) or 999) <= CPF_MAX_AGE)]
    used = in_force(young).sort_values(["age_grp", party_col])
    print(f"rows used (in force on {CPF_IN_FORCE}, age groups up to {CPF_MAX_AGE}):")
    for _, r in used.iterrows():
        print(f"  {r['effective_from']}  {r['age_grp']:<22} {r[party_col]:<12} {r[rate_col]}")


# --- ILO: employment by status, modelled estimates ----------------------------------------------------

def cpf_young_rates() -> dict:
    """Design R7: the worker and employer rates in force on CPF_IN_FORCE for every age group up to CPF_MAX_AGE
    (highest wage band). Stops if those groups do not share one rate per party, since R7 shows one bar."""
    df = pd.read_csv(path("cpf_contrib"), dtype={"effective_from": str})
    used = in_force(df[df["age_grp"].map(lambda g: (upper_age(g) or 999) <= CPF_MAX_AGE)])
    rates = {party: sorted(set(part["contribution_rate"])) for party, part in used.groupby("contributing_party")}
    if set(rates) != {"Employer", "Employee"} or any(len(v) != 1 for v in rates.values()):
        raise SystemExit(f"{FILES['cpf_contrib'][0]}: age groups up to {CPF_MAX_AGE} do not share one rate: {rates}")
    worker, employer = float(rates["Employee"][0]), float(rates["Employer"][0])
    return {"worker_pct": worker, "employer_pct": employer, "total_pct": worker + employer,
            "in_force": CPF_IN_FORCE, "max_age": CPF_MAX_AGE, "age_groups": sorted(used["age_grp"].unique())}


def check_hashes() -> None:
    """Every frozen data file matches its pinned SHA-256 (path() stops the script otherwise)."""
    for key in FILES:
        path(key)


def profile_ilo() -> None:
    """ILO SDMX-CSV with labels: each coded column reads 'CODE: Label'."""
    section(FILES["ilo"][0])
    df = pd.read_csv(path("ilo"), dtype=str)
    print(f"rows {len(df)}  columns {df.columns.tolist()}")
    for col in ("DATAFLOW", ILO_COLS["area"], ILO_COLS["measure"], ILO_COLS["sex"], ILO_COLS["source"],
                ILO_COLS["unit"], ILO_COLS["mult"]):
        print(f"  {col}: {sorted(df[col].dropna().unique())}")
    print(f"  blank OBS_VALUE cells {int(df['OBS_VALUE'].isna().sum())}  status flags "
          f"{df[ILO_COLS['status']].fillna('(none)').value_counts().to_dict()}")
    print("years per status group (first, last, count, missing years):")
    for g, part in df.groupby(ILO_COLS["ste"]):
        ys = sorted(part[ILO_COLS["year"]].astype(int))
        missing = sorted(set(range(ys[0], ys[-1] + 1)) - set(ys))
        print(f"  {g:<44} {ys[0]} {ys[-1]} {len(ys)} {missing}")
    years = df[ILO_COLS["year"]].astype(int)
    used = df[(df[ILO_COLS["ste"]] == ILO_EMPLOYEES) & years.isin(ILO_YEARS)].sort_values(ILO_COLS["year"])
    repeated = sorted(used.loc[used[ILO_COLS["year"]].duplicated(), ILO_COLS["year"]].unique())
    if repeated:
        raise SystemExit(f"{FILES['ilo'][0]}: more than one {ILO_EMPLOYEES!r} row for {repeated}")
    used = used.fillna({ILO_COLS["status"]: ""})
    print(f"rows used ({ILO_EMPLOYEES!r}, {ILO_YEARS.start} to {ILO_YEARS.stop - 1}, "
          f"unit {used[ILO_COLS['mult']].unique().tolist()} persons):")
    for _, r in used.iterrows():
        print(f"  {r[ILO_COLS['year']]}  {r['OBS_VALUE']:<12} {r[ILO_COLS['status']]}")
    absent = sorted(set(ILO_YEARS) - set(used[ILO_COLS["year"]].astype(int)))
    print(f"years asked for but absent: {absent}")


def main() -> None:
    profile_damodaran()
    profile_cpi("cpi_idn")
    profile_cpi("cpi_usa")
    profile_inflasi()
    profile_cpf_table("cpf_contrib", "contributing_party", "contribution_rate", "whole percent of wages")
    profile_cpf_table("cpf_alloc", "account_type", "allocation_rate", "fraction of the contribution")
    profile_ilo()


if __name__ == "__main__":
    main()
