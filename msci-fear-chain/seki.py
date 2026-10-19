"""Readers for Bank Indonesia's SEKI rate tables (amendment 8.7): I.28 time-deposit rates, I.26 loan rates.

Each table spreads one series over several sheets. A sheet's month columns are read in order; a column's year
comes from the year row where it has a label and is carried forward otherwise (some sheets label only one month
a year), and every label that is present must agree with the carried year. A column that repeats the previous
month is skipped if its value is the same and refused if not; columns after a sheet's last month are ignored.
Overlapping sheets must agree to the printed precision, except where the newest sheet supersedes (from 2025).
"""

import math

import pandas as pd
import xlrd

MONTH_NAMES = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
TOL = 1e-9


def _label(v) -> str:
    return " ".join(str(v).split()) if isinstance(v, str) else ""


def _month_header(sh) -> tuple[int, int]:
    """(year row, month row): the month row has the most month names; the year row is the one above it."""
    counts = [(sum(_label(v).rstrip("*").strip() in MONTH_NAMES for v in sh.row_values(r)), r) for r in range(min(10, sh.nrows))]
    n, r = max(counts)
    if n < 6:
        raise ValueError(f"{sh.name}: no month header row")
    return r - 1, r


def _find_row(sh, block: str | None, row: str) -> int:
    """The first row labelled `row` after the row labelled `block` (labels sit in the first four columns);
    with no block, the first row labelled `row`."""
    labels = [" ".join(_label(sh.cell_value(r, c)) for c in range(min(4, sh.ncols))).strip() for r in range(sh.nrows)]
    start = -1 if block is None else next(i for i, s in enumerate(labels) if s == block or s.startswith(block + " ")
                                          or s.endswith(" " + block))
    return next(i for i in range(start + 1, sh.nrows) if labels[i] == row or labels[i].startswith(row + " ")
                or labels[i].endswith(" " + row))


def sheet_series(sh, block: str, row: str, first: str, last: str) -> tuple[pd.Series, set, int]:
    """Values of one row for months first..last (YYYY-MM) as printed (a repeated month keeps its filled copy);
    returns the series, the provisional months (header marked '*') and the number of duplicate columns."""
    yr, mr = _month_header(sh)
    r = _find_row(sh, block, row)
    want = pd.period_range(first, last, freq="M")
    out, prov, dupes, i, year, prev = {}, set(), 0, 0, None, None
    for c in range(sh.ncols):
        name = _label(sh.cell_value(mr, c))
        bare = name.rstrip("*").strip()
        if bare not in MONTH_NAMES:
            continue
        if i >= len(want):
            break
        v = sh.cell_value(r, c)
        val = float(v) if isinstance(v, float) and v != 0 else math.nan
        if prev is not None and bare == prev[0]:
            if math.isnan(prev[1]) and not math.isnan(val):
                out[want[i - 1]] = val          # the first copy was empty: keep the filled one
                prev = (bare, val)
            elif not (math.isnan(val) or abs(val - prev[1]) < TOL):
                raise ValueError(f"{sh.name} col {c}: repeated {bare} with a different value")
            dupes += 1
            continue
        y = sh.cell_value(yr, c)
        if isinstance(y, float) and y == int(y) and 1980 < y < 2100:
            if year is not None and bare != "Jan" and int(y) != year:
                raise ValueError(f"{sh.name} col {c}: year label {int(y)} disagrees with carried year {year}")
            year = int(y)
        elif bare == "Jan" and year is not None:
            year += 1
        if year is None:
            raise ValueError(f"{sh.name} col {c}: month before any year label")
        p = want[i]
        if MONTH_NAMES[p.month - 1] != bare or p.year != year:
            raise ValueError(f"{sh.name} col {c}: expected {p}, found {bare} {year}")
        out[p] = val
        if name.endswith("*"):
            prov.add(p)
        prev, i = (bare, val), i + 1
    if i != len(want):
        raise ValueError(f"{sh.name}: found {i} of {len(want)} months {first}..{last}")
    return pd.Series(out), prov, dupes


def _sheet(book, prefix: str):
    return next(s for s in book.sheets() if s.name.strip() == prefix)


def read_seki(path: str, block: str, row: str, sheets: list[tuple[str, str, str]], supersede_from: str) -> dict:
    """Join a row across sheets [(sheet name, first, last), ...], oldest first. Months in two sheets must agree,
    except months from `supersede_from` on, where the later sheet wins and the disagreements are counted."""
    book = xlrd.open_workbook(path)
    series, prov, dupes, overlap, superseded = pd.Series(dtype=float), set(), 0, 0, 0
    for name, first, last in sheets:
        s, p, d = sheet_series(_sheet(book, name), block, row, first, last)
        common = series.index.intersection(s.index)
        for m in common:
            a, b = series[m], s[m]
            same = (math.isnan(a) and math.isnan(b)) or abs(a - b) < TOL
            if m >= pd.Period(supersede_from, "M"):
                superseded += not same
            elif not same:
                raise ValueError(f"{name}: {m} disagrees with an earlier sheet")
        overlap += len(common)
        series = pd.concat([series.drop(common), s]).sort_index()
        prov |= p
        dupes += d
    return dict(series=series, provisional=sorted(str(m) for m in prov), duplicates_skipped=dupes,
                overlap_months_checked=overlap, superseded_disagreements=superseded)


def dated_sheet_series(sh, block: str | None, row: str) -> pd.Series:
    """A sheet whose month row holds Excel dates in one unbroken run (I.25.A "Th 2002-2009"); '-' and 0 are
    missing."""
    mr = next(r for r in range(min(10, sh.nrows))
              if sum(isinstance(v, float) and 30000 < v < 60000 for v in sh.row_values(r)) >= 12)
    r = _find_row(sh, block, row)
    out = {}
    for c, v in enumerate(sh.row_values(mr)):
        if isinstance(v, float) and 30000 < v < 60000:
            y, m, *_ = xlrd.xldate_as_tuple(v, sh.book.datemode)
            p = pd.Period(year=y, month=m, freq="M")
            if p in out:
                raise ValueError(f"{sh.name}: month {p} appears twice")
            x = sh.cell_value(r, c)
            out[p] = float(x) if isinstance(x, float) and x != 0 else math.nan
    s = pd.Series(out).sort_index()
    if len(pd.period_range(s.index[0], s.index[-1], freq="M")) != len(s):
        raise ValueError(f"{sh.name}: months are not one unbroken run")
    return s


def read_policy(path: str) -> dict:
    """Bank Indonesia's policy-rate pieces from Table I.25.A, end of period: the one-month SBI rate and the BI Rate
    to 2009 (sheet "Th 2002-2009"), and the "Policy Rate" row from 2010 (sheets "Th 2010-2016" and "1.25A_1")."""
    book = xlrd.open_workbook(path)
    old = book.sheet_by_name("Th 2002-2009")
    policy, _, _ = sheet_series(_sheet(book, "Th 2010-2016"), None, "Policy Rate", "2010-01", "2016-12")
    recent, prov, _ = sheet_series(_sheet(book, "1.25A_1"), None, "Policy Rate", "2017-01", "2026-09")
    return dict(sbi_1m=dated_sheet_series(old, "Sertifikat Bank Indonesia", "1 Bulan"),
                bi_rate=dated_sheet_series(old, None, "BI Rate"),
                policy=pd.concat([policy, recent]).sort_index(), provisional=sorted(str(m) for m in prov))
