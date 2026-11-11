"""Data profile for Post 29.

Each data file in data/ is frozen by its SHA-256 (docs/data-README.src.md says where each comes from); a file that
does not match stops the script. Run on its own, this prints the coverage of each series the analysis reads and the
cross-checks it runs.
"""
import csv
import hashlib
import io
import os
import re
import statistics
import subprocess
import zipfile
from xml.etree import ElementTree

import openpyxl
import xlrd

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

FILES = {
    "h10": ("census_h10ar.xlsx", "fe3041e6445323518e6919b02d82461c15777037391108d23420b094f17d1d53"),
    "hvs17": ("census_hvs_ann25t_17.xlsx", "c9f6e22b5bce78b657cae7cd2fa69e592916e1a3acfe9055c3425ac9851da194"),
    "soc_price": ("census_nrs_price_cust.xlsx", "d543bbad67384a30292f64a4965b33c62a03b7340425e0d37b3c2cde3f119237"),
    "cq_index": ("census_nrs_price_sold_cust.xlsx", "9b48bfe97fa5e6c9b654eea90017b7d29502dc660f15db0d15d41cd3aa6bcfd3"),
    "sqft": ("census_chars_soldsquarefeet_cust.xls", "b3e24b4beef8026c423ecad7b438d2eb0985f0b13751c06c5087aa09304cd34e"),
    "fhfa_at": ("fhfa_hpi_at_us_and_census.csv", "580d761c3488f3e9a6f25074bdace5de96f476f579c06eeb7144835e8f52deba"),
    "coh_values": ("census_coh_values_unadj.txt", "5fbabee6743983f4f39b61c6e42cc9a5727c2266173344ec3fc0381b06a221b6"),
    "acs_2025": ("census_acs_b25077_2025.dat", "7ab895b182348af2e79cb31e45717be5fdcc38ab1e1ad959cb4e0e7e9393b772"),
    "h15": ("frb_h15_package.zip", "295b4e17daf1d2ae6fdd215d5aa2c9d4e9cce98eaddad40e18749cd345e3dc3a"),
    "le": ("bls_le_data_alldata_ia20260512.txt", "a4585d4f14097762deb6f4988196f353474029d889a5292992d09a3541d81598"),
    "le_2025_08": ("bls_le_data_alldata_ia20250802.txt", "daad9793a5dbbf03947deed1d9f85d710db0840e15968c5c68852f255df067ec"),
    "le_series": ("bls_le_series.txt", "137e0d9a6ba1e2bc1b39cc77409483bc4a198e6b7ab0dbdb27454db276810a0f"),
    "rcpiurs": ("bls_rcpiurs_allitems_ia20260819.xlsx", "355ea8a14a6d07d777a17a1ddad526b8a199390a7c1bb8c7b58e2dec1a2544d8"),
    "cpiu": ("bls_cu_data_allitems.txt", "f3c22c8592d9134fa5ab305fa2df6e37dfd2388f10168985fdbc84082deb4ff0"),
    "cx": ("bls_cx_data_alldata.txt", "eb080c52b0d213d2f891c1658cd3c5d0860bd3826558e8c07a41108fa4d2cfdd"),
    "cx_series": ("bls_cx_series.txt", "9755a92a6605d05bae92ca34080b4214500603dd487c37090e0e1ed95b8432f2"),
    "cx_item": ("bls_cx_item.txt", "6c2bcd8c37c8de2f2092376c6a3501e707c0b251c064ffc51485edd298a32e98"),
    "cx_characteristics": ("bls_cx_characteristics.txt", "a264f45122a82fc3a56f8304c17bab015b5fad3c45c01eae4b137f9d7fd4d666"),
    "cx_demographics": ("bls_cx_demographics.txt", "ea97efd13956cbc61a63455af584e05cff7f67621e753192ee9ff84424c6809a"),
    "cx_footnote": ("bls_cx_footnote.txt", "3f32756911577e6df3c007b6400c495c08cdeaa1089988401789f8128b2e0cb5"),
    "ce_1984": ("bls_ce_age_1984.pdf", "dd2abcd23013052e846c4f1e232f4225e40b565d6cbdad74cf9d8977d2bd511f"),
    "ce_2024": ("bls_ce_age_2024.xlsx", "0abaa86afa5d2b226c21952ff958a2c5300287b2b1fefc115a452f361a55ba86"),
    "nyfed": ("nyfed_college_labor_unemployment.csv", "f7a508bb5d8091b2d67a3ab1266526cf0b39fc424ad9bd6c2278c3785b55dae7"),
    "bi_2025q3": ("bi_shpr_2018eq100_tw3_2025.xlsx", "1f1b7d967c4fa6fd0750b6e67e9eaa333bb3eee045e42fc74c45596ffcc8a4dc"),
    "bi_2026q3": ("bi_shpr_tw3_2026.xlsx", "153980dd12efc1992de8b2cbb77f23f81c93e8caf92ddc867526e4414d4c62c9"),
    "ilo_median_age": ("ilo_ear_emtm_sex_age_idn.csv", "6aa994d63fba35a328909056ab03975ead57f4e4e8c10a6076bbaf0d2af46b2c"),
    "ilo_median_area": ("ilo_ear_emtm_sex_geo_idn.csv", "1d316f3a6d6eaedc84081783c908d7e540d5b2c6e6651f96a539984435772f61"),
}

H10_BRACKETS = ("25 to 34 Years", "35 to 44 Years", "45 to 54 Years")
H10_COMPARABLE = {2013: "(39)", 2017: "(40)"}      # design R2: the rows Census marks for comparison with later years
H15_SERIES = "RIFSGFSM03_N.A"                      # 3-month Treasury bill, secondary market, discount basis, annual
LE_SERIES = {"LEU0252888500": "25 to 34", "LEU0252881500": "16 and over", "LEU0252886300": "16 to 24"}
CPIU_SERIES = "CUUR0000SA0"
CX_GROUPS = {"01": "All consumer units", "02": "Under 25", "03": "25 to 34", "04": "35 to 44", "05": "45 to 54"}
CX_ITEMS = ("TOTALEXP", "FOODAWAY", "ENTRTAIN", "PERSCARE", "SNKNABEV")
ILO_LABELS = {"all": "Age (Youth, adults): 15+", "25 to 34": "Age (10-year bands): 25-34", "urban": "Area type: Urban"}
HVS_ROWS = ("Less than 25 years", "Less than 35 years")


def path(key: str) -> str:
    name, digest = FILES[key]
    p = os.path.join(DATA, name)
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    if h.hexdigest() != digest:
        raise SystemExit(f"{name}: sha256 {h.hexdigest()} is not the vetted file {digest}")
    return p


def check_hashes() -> None:
    for key in FILES:
        path(key)


def year_of(label) -> int | None:
    """A year from a cell such as 2025, '2025', '2024 (42)' or 1978.0; None for anything else."""
    m = re.match(r"\s*(\d{4})(\.0)?\b", str(label)) if label is not None else None
    return int(m.group(1)) if m else None


def _num(v) -> float:
    return float(str(v).replace(",", "").replace("$", "").strip())


# --- income (Census H-10) ----------------------------------------------------------------------------

def read_h10() -> tuple[dict, dict]:
    """Current-dollar median household income by age bracket: ({bracket: {year: median}}, {bracket: {year: alternate}}).
    One row per year; for 2013 and 2017 the row marked in H10_COMPARABLE, the other row kept as the alternate."""
    rows = list(openpyxl.load_workbook(path("h10"), data_only=True).active.iter_rows(values_only=True))
    picked, alt, block = {}, {}, None
    for r in rows:
        a = r[0]
        if isinstance(a, str) and year_of(a) is None and a.strip().endswith(("Years", "Older", "Over")):
            block = a.strip()
            continue
        y = year_of(a)
        if block not in H10_BRACKETS or y is None:
            continue
        label, median = str(a).strip(), int(r[2])
        if y in H10_COMPARABLE and H10_COMPARABLE[y] not in label:
            alt.setdefault(block, {})[y] = median
            continue
        if y in picked.setdefault(block, {}):
            raise SystemExit(f"H-10 {block}: two rows for {y}")
        picked[block][y] = median
    for b in H10_BRACKETS:
        gaps = sorted(set(range(1967, 2026)) - set(picked.get(b, {})))
        if gaps:
            raise SystemExit(f"H-10 {b}: missing years {gaps}")
    return picked, alt


# --- home prices -------------------------------------------------------------------------------------

def read_soc_price() -> dict[int, tuple[int, int]]:
    """Census NRS: US median and average sales price of new houses sold, annual: {year: (median, average)}."""
    ws = openpyxl.load_workbook(path("soc_price"), data_only=True)["Annual"]
    rows = list(ws.iter_rows(values_only=True))
    if rows[5][1] != "Median sales price" or rows[5][2] != "Average sales price":
        raise SystemExit(f"price_cust.xlsx: unexpected header {rows[5][:3]}")
    return {year_of(r[0]): (int(r[1]), int(r[2])) for r in rows[6:] if year_of(r[0]) and r[1] is not None}


def read_cq_index() -> dict[int, float]:
    """Census constant-quality (Laspeyres) price index of new single-family houses sold, US, annual (2005 = 100)."""
    rows = list(openpyxl.load_workbook(path("cq_index"), data_only=True)["Price Index"].iter_rows(values_only=True))
    hdr = next(i for i, r in enumerate(rows) if r[0] == "Year")
    if rows[hdr][1] != "Annual index":
        raise SystemExit(f"price_sold_cust.xlsx: column B is {rows[hdr][1]!r}")
    out = {}
    for r in rows[hdr + 1:]:
        y = year_of(r[0])
        if y is None:
            break
        if str(r[1]).strip() not in ("", "None"):     # a year with quarters only (2026) has no annual index yet
            out[y] = float(r[1])
    gaps = sorted(set(range(1963, 2026)) - set(out))
    if gaps:
        raise SystemExit(f"price_sold_cust.xlsx: no annual index for {gaps}")
    return out


def read_sqft() -> dict[int, float]:
    """Census: median square feet of floor area in new single-family houses sold, US, annual."""
    sh = xlrd.open_workbook(path("sqft")).sheet_by_name("SoldMedAvgSF")
    if "Median" not in str(sh.cell_value(3, 1)):
        raise SystemExit("soldsquarefeet_cust.xls: column B is not the median")
    return {year_of(sh.cell_value(i, 0)): float(sh.cell_value(i, 1)) for i in range(sh.nrows)
            if isinstance(sh.cell_value(i, 0), float) and sh.cell_value(i, 1) not in ("", None)}


def read_fhfa_at() -> dict[int, float]:
    """FHFA all-transactions index, USA, not seasonally adjusted: annual mean of the four quarters (complete years)."""
    q = {}
    with open(path("fhfa_at"), encoding="utf-8") as fh:
        for area, y, qtr, v in csv.reader(fh):
            if area == "USA":
                q.setdefault(int(y), {})[int(qtr)] = float(v)
    return {y: statistics.fmean(v.values()) for y, v in q.items() if sorted(v) == [1, 2, 3, 4]}


def read_census2000_value() -> int:
    """Census of Housing, median value of specified owner-occupied units, United States, 2000 (unadjusted)."""
    with open(path("coh_values"), encoding="latin-1") as fh:
        lines = fh.read().splitlines()
    head = next(l for l in lines if l.strip().startswith("2000"))
    us = next(l for l in lines if l.startswith("United States"))
    years, vals = head.split(), re.findall(r"\$[\d,]+", us)
    return int(_num(vals[years.index("2000")]))


def read_acs2025() -> int:
    """ACS 2025 1-year, B25077 median value of owner-occupied units, United States."""
    with open(path("acs_2025"), encoding="utf-8") as fh:
        for line in fh:
            geo, est, moe = line.strip().split("|")
            if geo == "0100000US":
                return int(est)
    raise SystemExit("acsdt1y2025-b25077.dat: no United States row")


# --- interest (Federal Reserve H.15) -----------------------------------------------------------------

def read_tbill() -> tuple[dict[int, float], dict]:
    """H.15 annual 3-month Treasury bill rate, percent: ({year: rate}, the series' annotations)."""
    with zipfile.ZipFile(path("h15")) as z, z.open("H15_data.xml") as fh:
        out, ann, cur = {}, {}, False
        for ev, el in ElementTree.iterparse(io.BufferedReader(fh), events=("start", "end")):
            tag = el.tag.split("}")[-1]
            if ev == "start" and tag == "Series":
                cur = el.attrib.get("SERIES_NAME") == H15_SERIES
            elif ev == "end" and tag == "Obs" and cur:
                if el.attrib.get("OBS_STATUS") == "A":
                    out[int(el.attrib["TIME_PERIOD"][:4])] = float(el.attrib["OBS_VALUE"])
            elif ev == "end" and tag == "Annotation" and cur:
                parts = [(c.text or "").strip() for c in el.iter() if (c.text or "").strip()]
                if len(parts) >= 2:
                    ann[parts[0]] = parts[1]
            if ev == "end" and tag in ("Obs", "Series"):
                el.clear()
    if not out:
        raise SystemExit(f"H15_data.xml: no observations for {H15_SERIES}")
    return out, ann


# --- pay and prices (BLS) ----------------------------------------------------------------------------

def read_le(key: str = "le", period: str = "Q05", series: tuple = tuple(LE_SERIES)) -> dict[str, dict[int, float]]:
    """BLS LE flat file: {series: {year: value}} for one period code (Q05 = annual average, A01 = annual)."""
    out = {s: {} for s in series}
    with open(path(key), encoding="latin-1") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 4 and p[0].strip() in out and p[2].strip() == period:
                out[p[0].strip()][int(p[1])] = float(p[3])
    return out


def read_rcpiurs() -> dict[int, float]:
    """BLS R-CPI-U-RS, all items, annual average (column AVG)."""
    rows = list(openpyxl.load_workbook(path("rcpiurs"), data_only=True).worksheets[0].iter_rows(values_only=True))
    hdr = next(r for r in rows if r[0] == "YEAR")
    col = list(hdr).index("AVG")
    return {year_of(r[0]): float(r[col]) for r in rows if year_of(r[0]) and isinstance(r[col], (int, float))}


def read_cpiu() -> dict[int, float]:
    """BLS CPI-U, all items, US city average, not seasonally adjusted, annual average (period M13)."""
    out = {}
    with open(path("cpiu"), encoding="latin-1") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if p[0].strip() == CPIU_SERIES and p[2].strip() == "M13":
                out[int(p[1])] = float(p[3])
    return out


def read_cx() -> dict[tuple[str, str], dict[int, float]]:
    """BLS CE LABSTAT means by age of reference person (LB04): {(item, group code): {year: dollars}}."""
    want = {f"CXU{i}LB04{g}M": (i, g) for i in CX_ITEMS for g in CX_GROUPS}
    out = {v: {} for v in want.values()}
    with open(path("cx"), encoding="latin-1") as fh:
        next(fh)
        for line in fh:
            key = want.get(line[:30].strip())
            if key:
                p = line.rstrip("\n").split("\t")
                if p[2].strip() == "A01":
                    out[key][int(p[1])] = float(p[3])
    return out


def read_ce_2024_printed() -> dict[str, dict[str, float]]:
    """BLS CE Table 1300 for 2024, the printed means: {item label: {column: mean}}, to check the LABSTAT file."""
    rows = list(openpyxl.load_workbook(path("ce_2024"), data_only=True).worksheets[0].iter_rows(values_only=True))
    cols = [str(c).replace("\n", " ") if c else "" for c in rows[2]]
    out, label = {}, None
    for r in rows:
        if isinstance(r[0], str) and r[0].strip() not in ("Mean", "SE", "RSE", "Share"):
            label = r[0].strip()
        elif r[0] == "Mean" and label and label not in out:
            out[label] = {cols[j]: float(v) for j, v in enumerate(r) if j and isinstance(v, (int, float))}
    return out


def read_ce_1984_printed() -> dict[str, list[int]]:
    """BLS CE Table 3 for 1984 (PDF, read with poppler's pdftotext -layout): {row label: the row's numbers}, columns All,
    Under 25, 25-34, ... in the table's order. Used only to check the LABSTAT file."""
    text = subprocess.run(["pdftotext", "-layout", path("ce_1984"), "-"], capture_output=True, text=True, check=True).stdout
    out = {}
    for line in text.splitlines():
        m = re.match(r"\s*([A-Za-z][A-Za-z ,]+?):?\s{2,}\$?([\d,]+(?:\s+\$?[\d,]+)+)\s*$", line)
        if m and m.group(1).strip() not in out:
            out[m.group(1).strip()] = [int(x.replace(",", "").replace("$", "")) for x in m.group(2).split()]
    return out


# --- context: NY Fed, HVS, Indonesia -------------------------------------------------------------------

def read_nyfed() -> list[tuple[int, int, float, float]]:
    """NY Fed monthly unemployment rates as published: [(year, month, recent graduates, all workers)]."""
    out = []
    with open(path("nyfed"), encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            m, _, y = r["Date"].split("/")
            out.append((int(y), int(m), float(r["Recent graduates"]), float(r["All workers"])))
    return sorted(out)


def read_hvs17() -> dict[str, dict[str, float]]:
    """Census HVS Table 17 (first block, United States by age): {row label: {column label: rate}}."""
    rows = list(openpyxl.load_workbook(path("hvs17"), data_only=True).worksheets[0].iter_rows(values_only=True))
    out, hdr = {}, None
    for r in rows:
        cells = [c for c in r[1:] if c is not None]
        if r[0] is None and cells and year_of(cells[0]):
            hdr = [str(c).strip() if c is not None else None for c in r]
            continue
        lab = str(r[0]).strip(" .…") if r[0] is not None else ""
        if hdr and lab in HVS_ROWS:
            for j, c in enumerate(r[1:], start=1):
                if hdr[j] and isinstance(c, (int, float)):
                    out.setdefault(lab, {}).setdefault(hdr[j], float(c))
        if lab.startswith("Married-couple"):
            break
    return out


def read_bi(key: str) -> dict[int, list[float]]:
    """Bank Indonesia SHPR, TABEL 1, national TOTAL row (2018 = 100): {year: [quarterly index values]}."""
    rows = list(openpyxl.load_workbook(path(key), data_only=True)["TABEL 1"].iter_rows(values_only=True))
    years = rows[5]
    total = next(r for r in rows if r[2] == "TOTAL")
    out, cur = {}, None
    for j in range(3, len(total)):
        if year_of(years[j]):
            cur = year_of(years[j])
        if cur and isinstance(total[j], (int, float)):
            out.setdefault(cur, []).append(float(total[j]))
    return out


def read_ilo(key: str, label: str) -> dict[int, float]:
    """ILOSTAT monthly earnings of employees, Indonesia, both sexes, one classification: {year: rupiah}."""
    out = {}
    with open(path(key), encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if r["sex.label"] == "Total" and r["classif1.label"] == label:
                out[int(r["time"])] = float(r["obs_value"])
    return out


def read_ilo_breaks(key: str, label: str) -> list[int]:
    """The years ILOSTAT flags 'Break in series' for one classification (both sexes)."""
    with open(path(key), encoding="utf-8-sig") as fh:
        return sorted(int(r["time"]) for r in csv.DictReader(fh)
                      if r["sex.label"] == "Total" and r["classif1.label"] == label and r["obs_status.label"] == "Break in series")


# --- profile ------------------------------------------------------------------------------------------

def span(d: dict) -> str:
    ys = sorted(d)
    gaps = sorted(set(range(ys[0], ys[-1] + 1)) - set(ys))
    return f"{ys[0]} to {ys[-1]}, {len(ys)} years, gaps {gaps}"


def main() -> None:
    check_hashes()
    print(f"all {len(FILES)} files match their pinned sha256")
    picked, alt = read_h10()
    for b in H10_BRACKETS:
        print(f"H-10 {b}: {span(picked[b])}; alternates {alt.get(b)}; 1971 {picked[b][1971]}, 2025 {picked[b][2025]}")
    soc = read_soc_price()
    print(f"SOC new-home price: {span(soc)}; 1971 {soc[1971]}, 2025 {soc[2025]}")
    cq, sq, fh = read_cq_index(), read_sqft(), read_fhfa_at()
    print(f"constant-quality index: {span(cq)}; 2005 {cq[2005]}, 2025 {cq[2025]}")
    print(f"median sq ft sold: {span(sq)}; 1978 {sq[1978]}, 2025 {sq[2025]}")
    print(f"FHFA AT annual means: {span(fh)}; 2000 {fh[2000]:.3f}, 2025 {fh[2025]:.3f}")
    print(f"Census 2000 median value {read_census2000_value()}; ACS 2025 median value {read_acs2025()}")
    tb, ann = read_tbill()
    print(f"T-bill {H15_SERIES}: {span(tb)}; annotations {ann}")
    le = read_le()
    for s, d in le.items():
        print(f"LE {s} ({LE_SERIES[s]}) Q05: {span(d)}; 1979 {d[1979]}, 2025 {d[2025]}")
    old = read_le("le_2025_08")
    for s in le:
        common = sorted(set(le[s]) & set(old[s]))
        print(f"  vs 2025-08 vintage: {len(common)} common years, differing {[y for y in common if le[s][y] != old[s][y]]}")
    rs, cu = read_rcpiurs(), read_cpiu()
    print(f"R-CPI-U-RS AVG: {span(rs)}; 1979 {rs[1979]}, 2025 {rs[2025]}")
    print(f"CPI-U M13: {span({y: v for y, v in cu.items() if y >= 1970})} (from 1970); 1979 {cu[1979]}, 2025 {cu[2025]}")
    cx = read_cx()
    for k, d in sorted(cx.items()):
        print(f"CE {k[0]} {CX_GROUPS[k[1]]}: {span(d)}")
    first = read_ce_1984_printed()
    for item, lab in (("TOTALEXP", "Average annual expenditures"), ("FOODAWAY", "Food away from home"),
                      ("ENTRTAIN", "Entertainment"), ("PERSCARE", "Personal care products and services")):
        print(f"  1984 printed vs LABSTAT {item}: 25-34 {first[lab][2]} vs {cx[(item, '03')][1984]:.0f}")
    printed = read_ce_2024_printed()
    for item, lab in (("TOTALEXP", "Average annual expenditures"), ("FOODAWAY", "Food away from home"),
                      ("ENTRTAIN", "Entertainment"), ("PERSCARE", "Personal care products and services")):
        p = printed[lab]
        print(f"  2024 printed vs LABSTAT {item}: 25-34 {p['25-34 years']} vs {cx[(item, '03')][2024]}")
    ny = read_nyfed()
    print(f"NY Fed: {ny[0][:2]} to {ny[-1][:2]}, {len(ny)} months")
    hvs = read_hvs17()
    for lab in HVS_ROWS:
        print(f"HVS {lab}: {len(hvs[lab])} columns; 1982 {hvs[lab]['1982']}, 2025* {hvs[lab].get('2025*')}")
    for key in ("bi_2025q3", "bi_2026q3"):
        b = read_bi(key)
        print(f"BI {key}: quarters per year {{{', '.join(f'{y}: {len(v)}' for y, v in sorted(b.items()))}}}")
    for name, label in ILO_LABELS.items():
        key = "ilo_median_area" if name == "urban" else "ilo_median_age"
        d = read_ilo(key, label)
        print(f"ILO median {name}: {span(d)}; 2018 {d[2018]:.0f}, 2024 {d[2024]:.0f}")


if __name__ == "__main__":
    main()
