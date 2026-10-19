"""Post 27: testing the fear chain after MSCI's Standalone proposal against Indonesia's own history.

Implements docs/2026-10-16-msci-fear-chain-design.md as amended in its section 8 (8.1 to 8.6):
  shock months  the IHSG month-end close is 10% or more below the previous month's (7% if fewer
                than 4 episodes); a shock month within 3 months of an earlier one joins its episode
  L1            stocks stay down: the close 12 months after month 0 is still below "before"
  L2            the rupiah weakens: 5% or more weaker at the end of month 3 than at the end of "before"
  L3            foreign investors leave: net portfolio equity outflow over month 0's quarter and the next
  L4            the cost of living rises: after a three-month rupiah slide of 10% or more (7% if fewer
                than 4 episodes), inflation over the next 12 months beats the previous 12 by 2 points
Verdicts: two thirds or more of complete episodes, holds; one third or fewer, does not hold; else mixed.
Output: results.json. Every figure the post prints is emitted here; the prose does no arithmetic.
"""

import csv
import hashlib
import json
import os
import xml.etree.ElementTree as ET

import pandas as pd
import xlrd

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

SHOCK, SHOCK_FALLBACK, SHOCK_CLUSTER = 0.10, 0.07, 3
HORIZONS = (1, 3, 12)
MIN_EPISODES = 4
RUPIAH_WEAKER = 0.05
SLIDE, SLIDE_FALLBACK, SLIDE_CLUSTER, SLIDE_SPAN = 0.10, 0.07, 12, 3
INFLATION_GAP_PP, INFLATION_WINDOW = 2.0, 12
HOLDS, FAILS = 2 / 3, 1 / 3
FLOAT_MONTH = pd.Period("1997-08", "M")     # the rupiah floated in August 1997 (design section 4)
OUTER_BOUND_YEARS = (1997, 1998)            # shown, never counted (design section 2)
SHOCK_DAY = pd.Timestamp("2026-10-16")      # October 2026: day 0, never counted (design section 3)
IDX_ACCESS = "2026-10-17"                   # the day the IDX statistics files were fetched (IDX terms: cite it)

# Raw files are frozen by hash (design section 7); a re-download needs a new vet.
FILES = {
    "bi_ihsg": ("bi_seki_table_iii3_ihsg_monthend.xls",
                "da0c63edff686f6292b41326006c3fcd4b37d35880de86dfb43a443e77436364"),
    "bapepam_ihsg": ("bapepam_ihsg_monthend_2004_2005.csv",
                     "52612d5fe72934a80961960d4373386f066b1a2f458c16aaf7b0ac3cdda925f8"),
    "ihsg_fixes": ("ihsg_monthend_corrections.csv",
                   "e882c66436808121e1a95f409624fbfa684e3d9ab13a574da5a602fa79437b3b"),
    "bis": ("bis_idr_usd_daily.csv", "7002a7c243f9c09bb7597e2abc1b279b835eea99447760d9dd26e4c03bd9183b"),
    "ecb": ("ecb_idr_usd_per_eur_daily.csv", "52b483819f87103deff3c84a8ee08b29bac31befc6fffa94f3b23d885a629612"),
    "bop": ("imf_bop_portfolio_equity_liab_q.xml",
            "39dc6a2eda9ff82bcfe766593e0fabe2b0ee7611e9e7902e76613038cd0fe9bf"),
    "cpi": ("imf_cpi_idn_m.csv", "b3ba15f60d304316b78adedd37229ff945c8669b67321f9284196e564071c20b"),
    "ojk_daily": ("ojk_ihsg_daily_2023on.xml", "33e4eb3e941634c471069adf3b6eed24f6b8fce2e64cf0531f426ecf904ed4f3"),
    "ojk_weekly": ("ojk_foreign_trading_weekly.xml",
                   "b6b7df7eb2bb18bf3a334cc223d868f80be690d3c944d5eed9d07d89ea46e32f"),
    "idx_daily": ("idx_ihsg_daily_2026-10.csv", "48f360ad8f6d8908eda7a9f9c635488b4887f66f82212652d17e749d1ecb54ec"),
    # amendment 8.7
    "bi_inflasi": ("Data Inflasi.xlsx", "5c79086509b6c19f90c5e3e835c5dcc40a02d322087d94e1c2a30a17e0280217"),
    "seki_deposit": ("bi_seki_table_i28_deposit_rates.xls",
                     "4b19af0c8cbc3ed0ed3093a53062d5db66062491be3a8f30982e8f2f1909e69c"),
    "seki_loan": ("bi_seki_table_i26_loan_rates.xls", "d437c35c64b72be1d76d16a152fd8eab8ee44e44e0e9662517b671c883c7b83c"),
    "seki_policy": ("bi_seki_table_i25a_policy_rate.xls",
                    "aae221bd92d1365237c850a13e4e58a8f98dcb8b83a5045533e744079e658058"),
    "fuel": ("fuel_price_changes.csv", "803a859dcef4bcbd0a5faec54b1a22d9d2857ef215c52a204d687242c38d7e45"),
}


def path(key: str) -> str:
    name, digest = FILES[key]
    p = os.path.join(DATA, name)
    with open(p, "rb") as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    if got != digest:
        raise SystemExit(f"{name}: sha256 {got} is not the vetted file {digest}")
    return p


# --- readers (make_charts.py imports these, so the two scripts cannot drift) -------------------------

MONTHS = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}


def _month_of(label) -> int | None:
    return MONTHS.get(str(label).strip().rstrip("*")[:3])


def _year_of(cell) -> int | None:
    if isinstance(cell, float) and 1980 < cell < 2100:
        return int(cell)
    s = str(cell).strip()
    return int(s[:4]) if s[:4].isdigit() else None


def _bi_sheet(sh) -> list:
    """(month, close, preliminary) from one sheet. A year is a block of month columns ended by a blank
    column or by the month number starting again; its label may sit on any cell of the block (January
    in older years, the last month from 2024). A block with no label that continues the previous one's
    months belongs to the same year (2004 is split by a blank column)."""
    mo_r = next(r for r in range(min(sh.nrows, 12)) if sum(1 for v in sh.row_values(r) if _month_of(v)) >= 12)
    years, months = sh.row_values(mo_r - 1), sh.row_values(mo_r)
    vals = sh.row_values(next(r for r in range(sh.nrows)
                              if "IHSG" in " ".join(str(v) for v in sh.row_values(r)[:4]).upper()))
    blocks, cur = [], []
    for c in range(sh.ncols):
        m = _month_of(months[c])
        if m and cur and m <= _month_of(months[cur[-1]]):
            blocks.append(cur)
            cur = []
        if m:
            cur.append(c)
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    out, prev = [], None
    for cols in blocks:
        ys = {_year_of(years[c]) for c in cols} - {None}
        if not ys and prev and _month_of(months[cols[0]]) > _month_of(months[prev[1][-1]]):
            ys = {prev[0]}
        if len(ys) != 1:
            raise SystemExit(f"{sh.name}: cannot place the block at column {cols[0]} in a year: {ys}")
        year = ys.pop()
        prev = (year, cols)
        for c in cols:
            if isinstance(vals[c], float) and vals[c] > 0:
                out.append((pd.Period(f"{year}-{_month_of(months[c]):02d}", "M"), vals[c],
                            str(months[c]).strip().endswith("*")))
    return out


def read_ihsg() -> tuple[pd.Series, list[str]]:
    """IHSG month-end close from January 2004 (design 8.6): Bapepam for January 2004 to November 2005,
    Bank Indonesia's table III.3 from December 2005, then the six corrections. Also returns the months
    Bank Indonesia marks preliminary."""
    bi, prelim = {}, []
    for sh in xlrd.open_workbook(path("bi_ihsg")).sheets():
        for month, value, p in _bi_sheet(sh):
            if month in bi and abs(bi[month] - value) > 0.005:
                raise SystemExit(f"BI sheets disagree on {month}: {bi[month]} vs {value}")
            bi[month] = value
            if p:
                prelim.append(str(month))
    s = pd.Series({m: v for m, v in bi.items() if m >= pd.Period("2005-12", "M")}, dtype=float)
    for row in csv.DictReader(open(path("bapepam_ihsg"))):
        s[pd.Period(row["month"], "M")] = float(row["ihsg_close"])
    for row in csv.DictReader(open(path("ihsg_fixes"))):
        s[pd.Period(row["month"], "M")] = float(row["ihsg_close"])
    s = s.sort_index()
    full = pd.period_range(s.index[0], s.index[-1], freq="M")
    assert s.index[0] == pd.Period("2004-01", "M") and s.index.equals(full), "IHSG months are not continuous"
    return s.rename("ihsg"), sorted(prelim)


def read_rupiah() -> tuple[pd.Series, pd.Timestamp]:
    """Rupiah per US dollar, daily: BIS WS_XRU, then the ECB cross rate (rupiah per euro divided by
    dollars per euro) for days after BIS's last observation (design 8.4). Returns the series and the
    last BIS date."""
    bis = pd.read_csv(path("bis"), usecols=["TIME_PERIOD", "OBS_VALUE"], parse_dates=["TIME_PERIOD"])
    bis = pd.Series(pd.to_numeric(bis["OBS_VALUE"], errors="coerce").values, index=bis["TIME_PERIOD"]).dropna()
    ecb = pd.read_csv(path("ecb"), usecols=["KEY", "TIME_PERIOD", "OBS_VALUE"], parse_dates=["TIME_PERIOD"])
    ecb["OBS_VALUE"] = pd.to_numeric(ecb["OBS_VALUE"], errors="coerce")
    wide = ecb.pivot(index="TIME_PERIOD", columns="KEY", values="OBS_VALUE").dropna()
    cross = wide["EXR.D.IDR.EUR.SP00.A"] / wide["EXR.D.USD.EUR.SP00.A"]
    last_bis = bis.index.max()
    s = pd.concat([bis, cross[cross.index > last_bis]]).sort_index()
    assert s.index.is_unique and (s > 0).all()
    return s.rename("idr_per_usd"), last_bis


def read_bop() -> pd.Series:
    """IMF BOP, Indonesia: portfolio investment liabilities, equity and investment fund shares, net
    incurrence, quarterly, in US dollars. OBS_VALUE is already in dollars despite SCALE=6 (checked against
    Bank Indonesia's report); the zeros for 1981 to 1992 are missing data (design 8.2)."""
    root = ET.parse(path("bop")).getroot()
    obs = {e.get("TIME_PERIOD"): float(e.get("OBS_VALUE")) for e in root.iter() if e.tag.endswith("Obs")}
    s = pd.Series({pd.Period(k.replace("-", ""), "Q"): v for k, v in obs.items()}).sort_index()
    return s[s.index >= pd.Period("1993Q1", "Q")].rename("equity_liab_usd")


def read_cpi() -> pd.Series:
    """IMF CPI, Indonesia, headline index (all items), monthly (design 8.3)."""
    rows = [r for r in csv.DictReader(open(path("cpi"), encoding="utf-8"))
            if r["COICOP_1999"] == "_T" and r["TYPE_OF_TRANSFORMATION"] == "IX"]
    s = pd.Series({pd.Period(r["TIME_PERIOD"].replace("-M", "-"), "M"): float(r["OBS_VALUE"]) for r in rows})
    s = s.sort_index()
    assert s.index.equals(pd.period_range(s.index[0], s.index[-1], freq="M"))
    return s.rename("cpi")


def _xmla_rows(key: str) -> tuple[list[str], list[list[str]]]:
    ns = {"md": "urn:schemas-microsoft-com:xml-analysis:mddataset"}
    root = ET.parse(path(key)).getroot().find(".//md:root", ns)
    axes = {a.get("name"): a for a in root.findall("md:Axes/md:Axis", ns)}
    cap = lambda ax: [[m.find("md:Caption", ns).text for m in t.findall("md:Member", ns)]
                      for t in ax.findall("md:Tuples/md:Tuple", ns)]
    cols = [c[0] for c in cap(axes["Axis0"])]
    cells = {int(c.get("CellOrdinal")): c.find("md:Value", ns).text for c in root.findall("md:CellData/md:Cell", ns)
             if c.find("md:Value", ns) is not None}
    rows = [labels + [cells.get(r * len(cols) + i) for i in range(len(cols))] for r, labels in enumerate(cap(axes["Axis1"]))]
    return cols, rows


def read_ojk_daily() -> pd.Series:
    """OJK Portal Data, IHSG (COMPOSITE, Nilai Indeks), daily from January 2023."""
    cols, rows = _xmla_rows("ojk_daily")
    i = cols.index("Nilai Indeks") + 2
    s = pd.Series({pd.Timestamp(r[0]): float(r[i]) for r in rows if r[i]}).sort_index()
    return s.rename("ihsg_daily")


def read_ojk_weekly() -> pd.Series:
    """OJK Portal Data, foreign (Asing) net buying on the exchange, rupiah, by OJK week label."""
    cols, rows = _xmla_rows("ojk_weekly")
    i = cols.index("Net Buy Sell") + 2
    return pd.Series({r[0]: float(r[i]) for r in rows if r[1] == "Asing" and r[i]}).rename("foreign_net_idr")


def read_idx_daily() -> pd.DataFrame:
    """IDX Daily Statistics, IHSG close and previous close, 15 and 16 October 2026 (extract_idx_daily.py)."""
    return pd.read_csv(path("idx_daily"), parse_dates=["date"]).set_index("date")


# --- helpers ----------------------------------------------------------------------------------------

def sample_id(items) -> str:
    """Short hash of the episodes a statistic was computed on, so the prose can tell two samples apart."""
    return hashlib.sha256("|".join(str(x) for x in sorted(items)).encode()).hexdigest()[:10]


def month_end(daily: pd.Series) -> pd.Series:
    """Last observation in each month; the month of the latest observation is dropped (incomplete)."""
    me = daily.groupby(daily.index.to_period("M")).last()
    return me[me.index < daily.index.max().to_period("M")]


def cluster(months: list, gap: int) -> list[list]:
    """Group sorted months: a month within `gap` months after the episode's latest month joins it."""
    eps = []
    for m in months:
        if eps and (m - eps[-1][-1]).n <= gap:
            eps[-1].append(m)
        else:
            eps.append([m])
    return eps


def verdict(flags: dict) -> dict:
    """flags maps an episode's month 0 (str) to True/False for the complete episodes only."""
    n, k = len(flags), sum(flags.values())
    share = k / n if n else None
    word = None if not n else "holds" if share >= HOLDS else "does not hold" if share <= FAILS else "mixed"
    return dict(n=n, n_meeting=k, n_not_meeting=n - k, share=share, verdict=word, sample=sample_id(flags))


def slide_variants(cpi: pd.Series, rme: pd.Series) -> dict:
    """Readings of the slide rule that the independent recomputations flagged (reported, not used for the
    verdict): the outer-bound episode cut at the end of 1998, and inflation windows pivoting on the month
    before the slide."""
    change = rme / rme.shift(SLIDE_SPAN) - 1
    change = change[change.index > FLOAT_MONTH]
    out = {}
    for threshold in (SLIDE, SLIDE_FALLBACK):
        months = list(change[change >= threshold].index)
        eps = cluster([m for m in months if m.year <= OUTER_BOUND_YEARS[-1]], SLIDE_CLUSTER) + \
            cluster([m for m in months if m.year > OUTER_BOUND_YEARS[-1]], SLIDE_CLUSTER)
        counted = [e for e in eps if e[0].year not in OUTER_BOUND_YEARS]
        if len(counted) >= MIN_EPISODES or threshold == SLIDE_FALLBACK:
            flags = {}
            for e in counted:
                p = prices_link(cpi, rme, e[0])
                if p["complete"]:
                    flags[str(e[0])] = p["rises"]
            out["cut_at_1998"] = dict(threshold=threshold, starts=[str(e[0]) for e in counted], **verdict(flags))
            break
    return out


# --- the shock months and links L1 to L3 --------------------------------------------------------------

def shock_episodes(ihsg: pd.Series) -> tuple[list[list], float, dict]:
    change = ihsg / ihsg.shift(1) - 1
    counts = {}
    for threshold in (SHOCK, SHOCK_FALLBACK):
        eps = cluster(list(change[change <= -threshold].index), SHOCK_CLUSTER)
        counts[threshold] = len(eps)
        if len(eps) >= MIN_EPISODES:
            return eps, threshold, counts
    return eps, SHOCK_FALLBACK, counts


def stock_link(ihsg: pd.Series, m0) -> dict:
    before = ihsg[m0 - 1]
    path_ = {k: ihsg[m0 - 1 + k] / before * 100 for k in range(0, 14) if m0 - 1 + k in ihsg.index}
    window = [ihsg[m0 + k] for k in range(0, 13) if m0 + k in ihsg.index]
    regain = next((k for k in range(0, len(ihsg)) if m0 + k in ihsg.index and ihsg[m0 + k] >= before), None)
    out = dict(before_month=str(m0 - 1), before=before, fall_month0_pct=(ihsg[m0] / before - 1) * 100,
               low_pct=(min(window) / before - 1) * 100, months_to_regain=regain, path=path_)
    for h in HORIZONS:
        if m0 + h in ihsg.index:
            out[f"change_{h}m_pct"] = (ihsg[m0 + h] / before - 1) * 100
    out["complete"] = m0 + 12 in ihsg.index
    out["stays_down"] = bool(ihsg[m0 + 12] < before) if out["complete"] else None
    out["fall0_pct"] = -out["fall_month0_pct"]
    if out["complete"]:
        ch = out["change_12m_pct"]
        out.update(above_12m_pct=ch if ch > 0 else None, below_12m_pct=-ch if ch < 0 else None)
    else:
        last = max(path_)
        out.update(latest_month=str(m0 - 1 + last), latest_below_pct=100 - path_[last] if path_[last] < 100 else None)
    return out


def rupiah_link(rme: pd.Series, m0) -> dict:
    before = rme[m0 - 1]
    out = dict(before=before, path={k: rme[m0 - 1 + k] / before * 100 for k in range(0, 14) if m0 - 1 + k in rme.index})
    for h in HORIZONS:
        if m0 + h in rme.index:
            out[f"weaker_{h}m_pct"] = (rme[m0 + h] / before - 1) * 100
    out["complete"] = m0 + 3 in rme.index
    out["weakens"] = bool(out["weaker_3m_pct"] >= RUPIAH_WEAKER * 100) if out["complete"] else None
    return out


def flows_link(bop: pd.Series, m0) -> dict:
    q0 = m0.asfreq("Q")
    qs = [q0, q0 + 1]
    out = dict(quarters=[str(q) for q in qs], complete=all(q in bop.index for q in qs))
    if out["complete"]:
        total = sum(bop[q] for q in qs)
        out.update(net_usd_bn=total / 1e9, per_quarter_usd_bn=[bop[q] / 1e9 for q in qs], leave=bool(total < 0),
                   outflow_usd_bn=-total / 1e9 if total < 0 else None)
    else:
        out["leave"] = None
    return out


# --- L4: rupiah slides and prices ---------------------------------------------------------------------

def slide_episodes(rme: pd.Series) -> tuple[list[list], float, dict]:
    change = rme / rme.shift(SLIDE_SPAN) - 1
    change = change[change.index > FLOAT_MONTH]
    counts = {}
    for threshold in (SLIDE, SLIDE_FALLBACK):
        eps = cluster(list(change[change >= threshold].index), SLIDE_CLUSTER)
        counted = [e for e in eps if e[0].year not in OUTER_BOUND_YEARS]
        counts[threshold] = len(counted)
        if len(counted) >= MIN_EPISODES:
            return eps, threshold, counts
    return eps, SLIDE_FALLBACK, counts


def prices_link(cpi: pd.Series, rme: pd.Series, s) -> dict:
    out = dict(slide_pct=(rme[s] / rme[s - SLIDE_SPAN] - 1) * 100,
               outer_bound=s.year in OUTER_BOUND_YEARS,
               complete=s + INFLATION_WINDOW in cpi.index and s - INFLATION_WINDOW in cpi.index)
    if out["complete"]:
        before = (cpi[s] / cpi[s - INFLATION_WINDOW] - 1) * 100
        after = (cpi[s + INFLATION_WINDOW] / cpi[s] - 1) * 100
        out.update(inflation_before_pct=before, inflation_after_pct=after, gap_pp=after - before,
                   rises=bool(after - before >= INFLATION_GAP_PP))
    else:
        out["rises"] = None
    return out


# --- October 2026 and context -------------------------------------------------------------------------

def october_2026(rupiah: pd.Series, rme: pd.Series, ojk: pd.Series, weekly: pd.Series, slide_used: float) -> dict:
    """What the data shows so far around 16 October 2026; never counted in a verdict. A slide since then is the
    L4 rule as applied (slide_used): a month-end from October on, against three month-ends earlier; until
    October's month-end exists, the latest daily rate against the month-end three months before stands in."""
    latest = rupiah.index.max()
    july = pd.Period("2026-07", "M")
    out = dict(shock_day=str(SHOCK_DAY.date()), shock_quarter=str(SHOCK_DAY.to_period("Q")),
               rupiah_latest_date=str(latest.date()), rupiah_latest=rupiah[latest],
               rupiah_end_july=rme[july], rupiah_vs_end_july_pct=(rupiah[latest] / rme[july] - 1) * 100,
               rupiah_on_shock_day=rupiah.get(SHOCK_DAY), ojk_daily_last=str(ojk.index.max().date()))
    month_ends = [m for m in rme.index if m >= SHOCK_DAY.to_period("M")]
    by_month_end = any(rme[m] / rme[m - SLIDE_SPAN] - 1 >= slide_used for m in month_ends)
    by_latest_day = rupiah[latest] / rme[latest.to_period("M") - SLIDE_SPAN] - 1 >= slide_used
    out.update(slide_so_far=bool(by_month_end or by_latest_day), slide_month_ends_tested=len(month_ends))
    out["rupiah_stronger_than_july_pct"] = -out["rupiah_vs_end_july_pct"] if out["rupiah_vs_end_july_pct"] < 0 else None
    jan = ojk[(ojk.index >= "2026-01-01") & (ojk.index <= "2026-01-31")]
    falls = (jan / jan.shift(1) - 1).dropna()
    worst = falls.idxmin()
    out.update(freeze_day=str(worst.date()), freeze_day_d=int(worst.day), freeze_day_y=int(worst.year),
               freeze_fall_pct=-falls[worst] * 100, freeze_close=jan[worst], freeze_prev_close=jan[jan.index < worst].iloc[-1])
    y2026 = weekly[[k.startswith("2026-") for k in weekly.index]]
    out.update(foreign_net_2026_idr_tn=y2026.sum() / 1e12, foreign_weeks_2026=len(y2026),
               foreign_last_week=y2026.index[-1], foreign_sold_2026_idr_tn=-y2026.sum() / 1e12,
               shock_day_d=int(SHOCK_DAY.day), shock_day_y=int(SHOCK_DAY.year))
    return out


def october_idx(idx: pd.DataFrame, ojk: pd.Series, ihsg: pd.Series, ep: dict) -> dict:
    """The 16 October close (IDX) and the latest episode's path past Bank Indonesia's last month, for the chart only:
    OJK's last September close, then the 16 October close at its place in the month (x = months from month 0)."""
    close, prev = idx.loc[SHOCK_DAY, "ihsg_close"], idx.loc[SHOCK_DAY, "previous_close"]
    if prev != idx["ihsg_close"][idx.index < SHOCK_DAY].iloc[-1]:
        raise SystemExit("IDX: the 16 October previous close is not the 15 October close")
    fall = (1 - close / prev) * 100
    if round(fall, 2) != -idx.loc[SHOCK_DAY, "change_pct_printed"]:
        raise SystemExit(f"IDX: computed fall {fall:.4f}% does not round to the printed change")
    ojk_me = ojk.groupby(ojk.index.to_period("M")).tail(1)
    last_bi = ihsg.index[-1]
    if abs(ojk_me[ojk_me.index.to_period("M") == last_bi].iloc[0] - ihsg[last_bi]) > 0.01:
        raise SystemExit(f"OJK and Bank Indonesia disagree on the {last_bi} month-end close")
    sep = ojk_me[ojk_me.index.to_period("M") == last_bi + 1]
    m0, before = pd.Period(ep["month0"], "M"), ep["stocks"]["before"]
    day_x = (SHOCK_DAY.to_period("M") - m0).n - 1 + SHOCK_DAY.day / SHOCK_DAY.days_in_month
    extension = [dict(date=str(sep.index[0].date()), day=int(sep.index[0].day), source="OJK", x=(last_bi + 1 - m0).n, index=sep.iloc[0] / before * 100),
                 dict(date=str(SHOCK_DAY.date()), day=int(SHOCK_DAY.day), source="IDX", x=day_x, index=close / before * 100)]
    return dict(idx_close=close, idx_prev_close=prev, idx_fall_pct=fall,
                idx_below_latest_before_pct=(1 - close / before) * 100, latest_extension=extension)


def october_rupiah(rupiah: pd.Series, ep: dict) -> dict:
    """The rupiah on 16 October against the latest episode's "before" month-end, for chart 1's dotted end only."""
    m0, before = pd.Period(ep["month0"], "M"), ep["rupiah"]["before"]
    x = (SHOCK_DAY.to_period("M") - m0).n - 1 + SHOCK_DAY.day / SHOCK_DAY.days_in_month
    return dict(rupiah_extension=[dict(date=str(SHOCK_DAY.date()), day=int(SHOCK_DAY.day), x=x,
                                       index=rupiah[SHOCK_DAY] / before * 100)])


def main():
    ihsg, prelim = read_ihsg()
    rupiah, last_bis = read_rupiah()
    rme = month_end(rupiah)
    bop, cpi = read_bop(), read_cpi()
    ojk, weekly, idx = read_ojk_daily(), read_ojk_weekly(), read_idx_daily()

    eps, threshold, counts = shock_episodes(ihsg)
    episodes = []
    for e in eps:
        m0 = e[0]
        episodes.append(dict(month0=str(m0), shock_months=[str(m) for m in e], year=m0.year,
                             stocks=stock_link(ihsg, m0), rupiah=rupiah_link(rme, m0), flows=flows_link(bop, m0)))
    links = {
        "L1": verdict({ep["month0"]: ep["stocks"]["stays_down"] for ep in episodes if ep["stocks"]["complete"]}),
        "L2": verdict({ep["month0"]: ep["rupiah"]["weakens"] for ep in episodes if ep["rupiah"]["complete"]}),
        "L3": verdict({ep["month0"]: ep["flows"]["leave"] for ep in episodes if ep["flows"]["complete"]}),
    }
    s_eps, s_threshold, s_counts = slide_episodes(rme)
    slides = [dict(start=str(e[0]), slide_months=[str(m) for m in e], year=e[0].year,
                   **prices_link(cpi, rme, e[0])) for e in s_eps]
    links["L4"] = verdict({s["start"]: s["rises"] for s in slides if s["complete"] and not s["outer_bound"]})
    latest = episodes[-1]["month0"]
    pivot = {}
    for s in slides:
        if s["complete"] and not s["outer_bound"]:
            m = pd.Period(s["start"], "M") - 1
            before, after = cpi[m] / cpi[m - INFLATION_WINDOW] - 1, cpi[m + INFLATION_WINDOW] / cpi[m] - 1
            pivot[s["start"]] = bool((after - before) * 100 >= INFLATION_GAP_PP)
    sensitivity = dict(
        latest_episode=latest,
        L2_without_latest=verdict({ep["month0"]: ep["rupiah"]["weakens"] for ep in episodes
                                   if ep["rupiah"]["complete"] and ep["month0"] != latest}),
        L3_without_latest=verdict({ep["month0"]: ep["flows"]["leave"] for ep in episodes
                                   if ep["flows"]["complete"] and ep["month0"] != latest}),
        L4_with_outer_bound=verdict({s["start"]: s["rises"] for s in slides if s["complete"]}),
        L4_pivot_month_before=verdict(pivot),
        **slide_variants(cpi, rme),
        closest_shock=min(({"month": ep["month0"], "fall_pct": ep["stocks"]["fall_month0_pct"]} for ep in episodes),
                          key=lambda d: abs(d["fall_pct"] + threshold * 100)),
    )

    bapepam = [r["month"] for r in csv.DictReader(open(path("bapepam_ihsg")))]
    fix_rows = list(csv.DictReader(open(path("ihsg_fixes"))))
    fixes = [r["month"] for r in fix_rows]
    meta = dict(ihsg_first=str(ihsg.index[0]), ihsg_first_year=ihsg.index[0].year, ihsg_last=str(ihsg.index[-1]),
                ihsg_last_year=ihsg.index[-1].year, n_ihsg_months=len(ihsg),
                bapepam_first=bapepam[0], bapepam_last=bapepam[-1], bi_first_used="2005-12", bi_first_used_year=2005,
                ihsg_corrections=fixes, n_ihsg_corrections=len(fixes), float_month=str(FLOAT_MONTH),
                n_corrections_idx=sum(r["source"].startswith("IDX") for r in fix_rows),
                n_corrections_bapepam=sum(r["source"].startswith("Bapepam") for r in fix_rows), idx_access=IDX_ACCESS,
                bi_old_first="1995-07", bi_old_last="2003-12", bi_old_first_year=1995, bi_old_last_year=2003,
                ihsg_preliminary=prelim, rupiah_first=str(rupiah.index[0].date()),
                rupiah_last=str(rupiah.index.max().date()), rupiah_last_bis=str(last_bis.date()),
                rupiah_last_complete_month=str(rme.index[-1]), bop_first=str(bop.index[0]), bop_last=str(bop.index[-1]),
                cpi_first=str(cpi.index[0]), cpi_last=str(cpi.index[-1]), n_episodes=len(episodes),
                n_slides=len(slides), n_slides_counted=sum(not s["outer_bound"] for s in slides))
    rules = dict(shock=SHOCK, shock_fallback=SHOCK_FALLBACK, shock_used=threshold, shock_counts=counts,
                 shock_cluster_months=SHOCK_CLUSTER, horizons=list(HORIZONS), min_episodes=MIN_EPISODES,
                 rupiah_weaker=RUPIAH_WEAKER, slide=SLIDE, slide_fallback=SLIDE_FALLBACK, slide_used=s_threshold,
                 slide_counts=s_counts, slide_cluster_months=SLIDE_CLUSTER, slide_span_months=SLIDE_SPAN,
                 inflation_gap_pp=INFLATION_GAP_PP, inflation_window_months=INFLATION_WINDOW, holds=HOLDS, fails=FAILS,
                 outer_bound_years=list(OUTER_BOUND_YEARS), rupiah_horizon_months=HORIZONS[1],
                 stock_horizon_months=HORIZONS[-1])
    from household import household_links      # household imports this module, so import it here
    household = household_links(slides, cpi, links)
    out = dict(meta=meta, rules=rules, episodes=episodes, slides=slides, links=links, sensitivity=sensitivity,
               household=household,
               october_2026={**october_2026(rupiah, rme, ojk, weekly, s_threshold), **october_idx(idx, ojk, ihsg, episodes[-1]),
                             **october_rupiah(rupiah, episodes[-1])})
    with open(os.path.join(BASE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=lambda v: v.item() if hasattr(v, "item") else str(v))
    report(out)


def report(out: dict) -> None:
    print(json.dumps(out["meta"], indent=1))
    print("rules used: shock", out["rules"]["shock_used"], out["rules"]["shock_counts"],
          "| slide", out["rules"]["slide_used"], out["rules"]["slide_counts"])
    print("\nSHOCK EPISODES (month 0, shock months | L1 stays down | L2 rupiah 3m | L3 flows)")
    for ep in out["episodes"]:
        st, rp, fl = ep["stocks"], ep["rupiah"], ep["flows"]
        print(f"  {ep['month0']} {ep['shock_months']} fall {st['fall_month0_pct']:.1f}% | "
              f"12m {st.get('change_12m_pct', float('nan')):.1f}% down={st['stays_down']} | "
              f"rupiah 3m {rp.get('weaker_3m_pct', float('nan')):.1f}% weakens={rp['weakens']} | "
              f"flows {fl.get('net_usd_bn', float('nan')):.2f}bn leave={fl['leave']}")
    print("\nRUPIAH SLIDES (start | slide | inflation before -> after | rises)")
    for s in out["slides"]:
        print(f"  {s['start']} outer={s['outer_bound']} slide {s['slide_pct']:.1f}% | "
              f"{s.get('inflation_before_pct', float('nan')):.1f} -> {s.get('inflation_after_pct', float('nan')):.1f} "
              f"gap {s.get('gap_pp', float('nan')):.1f}pp rises={s['rises']}")
    print("\nVERDICTS")
    for k, v in out["links"].items():
        print(f"  {k}: {v}")
    print("\nSENSITIVITY", json.dumps(out["sensitivity"], indent=1, default=str))
    print("\nOCTOBER 2026", json.dumps(out["october_2026"], indent=1, default=str))


if __name__ == "__main__":
    main()
