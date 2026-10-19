"""Post 27, amendment 8.7: the household links. L5 (a one-month deposit after tax against inflation), L6 (the
consumer-loan rate) with the policy-rate note, BPS's published rates beside L4, the fuel list, and the
one-episode flags for every link. Reads only frozen files (hashes in build_analysis.FILES); called from
build_analysis.main(), which passes in the series it has already read.
"""

import csv
import math
import re

import openpyxl
import pandas as pd

from build_analysis import BASE, FAILS, HOLDS, INFLATION_GAP_PP, path, verdict
from seki import read_policy, read_seki

INDONESIAN_MONTHS = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
                     "Oktober", "November", "Desember"]
SEKI_SHEETS = [("Th 1990-2008", "1990-01", "2008-12"), ("Th 2009-2018", "2009-01", "2019-03"),
               ("Th 2010-2024", "2010-01", "2025-03")]
SEKI_LAST = "2026-08"


def read_published_inflation() -> pd.Series:
    """Bank Indonesia's Data Inflasi page: BPS's published headline inflation, year on year, percent, by month.
    The file's last row, 'Desember 2002, 0,00 %', is a placeholder and is excluded."""
    ws = openpyxl.load_workbook(path("bi_inflasi"), read_only=True, data_only=True).active
    out = {}
    for row in ws.iter_rows(values_only=True):
        label, value = (row[1], row[2]) if len(row) > 2 else (None, None)
        m = re.fullmatch(r"(\w+) (\d{4})", str(label or "").strip())
        if not m or m.group(1) not in INDONESIAN_MONTHS:
            continue
        p = pd.Period(year=int(m.group(2)), month=INDONESIAN_MONTHS.index(m.group(1)) + 1, freq="M")
        if p == pd.Period("2002-12", "M"):
            if str(value).strip() != "0,00 %":
                raise SystemExit("Data Inflasi: the December 2002 row is no longer the known placeholder")
            continue
        if p in out:
            raise SystemExit(f"Data Inflasi: {p} appears twice")
        out[p] = float(str(value).replace("%", "").strip().replace(",", "."))
    s = pd.Series(out).sort_index()
    if len(pd.period_range(s.index[0], s.index[-1], freq="M")) != len(s):
        raise SystemExit("Data Inflasi: months are not one unbroken run")
    return s.rename("published_yoy_pct")


def read_rates() -> dict:
    """SEKI I.28 one-month time deposits and I.26 consumer loans (all commercial banks), and I.25.A's policy rate
    pieces. From January 2025 the newest sheet supersedes."""
    dep = read_seki(path("seki_deposit"), "Bank Umum", "1 Bulan", SEKI_SHEETS + [("1.28", "2025-01", SEKI_LAST)], "2025-01")
    loan = read_seki(path("seki_loan"), "Bank Umum", "Pinjaman Konsumsi Yang Diberikan",
                     SEKI_SHEETS + [("1.26", "2025-01", SEKI_LAST)], "2025-01")
    return dict(deposit=dep, loan=loan, policy=read_policy(path("seki_policy")))


# --- rules fixed in amendment 8.7 ---------------------------------------------------------------------

DEPOSIT_MONTHS = 12
LOAN_RISE_PP, POLICY_RISE_PP, POLICY_MONTHS = 1.0, 0.25, 3
COMPARATIVE_MARGIN = 1 / 3          # a comparative word needs the slides' share above the base share by a third
MIN_FOR_WORD = 4                    # fewer complete episodes than this: no verdict word
BASE_FROM = pd.Period("2004-01", "M")
# Final tax on rupiah time-deposit interest, residents, from the regulations stored in sources/tax/: 15% under
# PP 51/1994 (in force 1 January 1995), 20% under PP 131/2000 (in force 1 January 2001; PP 123/2015 keeps 20% for
# deposits not funded by export proceeds).
DEPOSIT_TAX = [(pd.Period("1995-01", "M"), 0.15), (pd.Period("2001-01", "M"), 0.20)]
INSTRUMENTS = [(pd.Period("1990-01", "M"), "one-month SBI rate"), (pd.Period("2005-07", "M"), "BI Rate"),
               (pd.Period("2016-08", "M"), "BI 7-day reverse repo rate")]


def tax_rate(m: pd.Period) -> float | None:
    rates = [r for start, r in DEPOSIT_TAX if m >= start]
    return rates[-1] if rates else None


def word_of(n: int, k: int, holds: float, fails: float, min_n: int = 1) -> str | None:
    if n < min_n or not n:
        return None
    return "holds" if k / n >= holds else "does not hold" if k / n <= fails else "mixed"


def one_episode_flips(v: dict, holds: float, fails: float, min_n: int = 1) -> bool:
    """Would a different outcome in one episode change the verdict word?"""
    n, k = v["n"], v["n_meeting"]
    return any(word_of(n, kk, holds, fails, min_n) != v["verdict"] for kk in (k - 1, k + 1) if 0 <= kk <= n)


def gated_verdict(flags: dict, holds: float, fails: float) -> dict:
    """build_analysis.verdict with amendment 8.7's floor: fewer than MIN_FOR_WORD episodes get no word."""
    v = verdict(flags)
    v["verdict"] = word_of(v["n"], v["n_meeting"], holds, fails, MIN_FOR_WORD)
    return v


def compounded(rates: pd.Series, tax: float) -> float:
    out = 1.0
    for r in rates:
        out *= 1 + (1 - tax) * r / 1200
    return out - 1


def deposit_window(dep: pd.Series, cpi: pd.Series, s: pd.Period, tax: float) -> dict | None:
    """L5 for a window starting at month s: the deposit's return over s+1..s+12 against CPI from s to s+12."""
    months = [s + k for k in range(DEPOSIT_MONTHS)]
    if any(m not in dep.index or math.isnan(dep[m]) for m in months) or s + 12 not in cpi.index or s not in cpi.index:
        return None
    rates = dep[months]
    net, gross = compounded(rates, tax), compounded(rates, 0.0)
    infl = cpi[s + 12] / cpi[s] - 1
    return dict(return_net_pct=net * 100, return_gross_pct=gross * 100, inflation_pct=infl * 100,
                real_net_pct=((1 + net) / (1 + infl) - 1) * 100, loses=bool(net < infl),
                loss_pct=(1 - (1 + net) / (1 + infl)) * 100 if net < infl else None)


def base_share(cond, months) -> dict:
    """Share of all windows (one starting in each month given) that meet a condition; cond returns None when a
    window is incomplete."""
    flags = [x for x in (cond(m) for m in months) if x is not None]
    return dict(n=len(flags), n_meeting=sum(flags), share=sum(flags) / len(flags) if flags else None,
                first=str(months[0]), last=str(months[-1]))


def comparative_allowed(slides_share: float, base: float) -> bool:
    return base is not None and slides_share is not None and slides_share > base * (1 + COMPARATIVE_MARGIN)


def savings_link(slides: list, dep: pd.Series, cpi: pd.Series, holds: float, fails: float) -> dict:
    """L5: per slide (1997 included where complete), then the verdict over counted slides and the base share."""
    rows = []
    for s in slides:
        m = pd.Period(s["start"], "M")
        tax = tax_rate(m)
        w = deposit_window(dep, cpi, m, tax) if tax is not None else None
        rows.append(dict(start=s["start"], outer_bound=s["outer_bound"], tax=tax, complete=w is not None, **(w or {})))
    counted = {r["start"]: r["loses"] for r in rows if r["complete"] and not r["outer_bound"]}
    with_outer = {r["start"]: r["loses"] for r in rows if r["complete"]}
    v = gated_verdict(counted, holds, fails)
    last = min(dep.dropna().index[-1] - (DEPOSIT_MONTHS - 1), cpi.index[-1] - 12)
    base = base_share(lambda m: (lambda w: None if w is None else w["loses"])(deposit_window(dep, cpi, m, tax_rate(m))),
                      list(pd.period_range(BASE_FROM, last, freq="M")))
    return dict(episodes=rows, verdict=v, with_outer=gated_verdict(with_outer, holds, fails), base=base,
                comparative_allowed=comparative_allowed(v["share"], base["share"]))


def policy_rate(pol: dict, m: pd.Period) -> tuple[float | None, str]:
    """The policy rate at the end of month m and its instrument (amendment 8.7); July to September 2005 have no
    stored value (the BI Rate decision record for July 2005 was not found)."""
    inst = [name for start, name in INSTRUMENTS if m >= start][-1]
    if m < pd.Period("2005-07", "M"):
        s = pol["sbi_1m"]
    elif m < pd.Period("2005-10", "M"):
        return None, inst
    elif m < pd.Period("2010-01", "M"):
        s = pol["bi_rate"]
    else:
        s = pol["policy"]
    v = s.get(m)
    return (None if v is None or math.isnan(v) else float(v)), inst


def policy_note(pol: dict, s: pd.Period) -> dict:
    base, inst0 = policy_rate(pol, s - 1)
    later = [policy_rate(pol, s + k) for k in range(POLICY_MONTHS + 1)]
    if any(inst != inst0 for _, inst in later):
        return dict(status="not comparable", instrument=inst0)
    if base is None or any(v is None for v, _ in later):
        return dict(status="not available", instrument=inst0)
    top = max(v for v, _ in later)
    return dict(status="raised" if top >= base + POLICY_RISE_PP else "not raised", instrument=inst0,
                before=base, highest=top, rise_pp=top - base)


def loans_link(slides: list, loan: pd.Series, pol: dict, holds: float, fails: float) -> dict:
    """L6 per slide, the policy-rate note beside it, the verdict over counted slides and the base share (second tier)."""
    def change(m):
        a, b = loan.get(m), loan.get(m + 12)
        return None if a is None or b is None or math.isnan(a) or math.isnan(b) else b - a
    rows = []
    for s in slides:
        m = pd.Period(s["start"], "M")
        ch = change(m)
        note = policy_note(pol, m) if not s["outer_bound"] else dict(status="not available")
        rows.append(dict(start=s["start"], outer_bound=s["outer_bound"], complete=ch is not None,
                         loan_at_slide=loan.get(m), loan_12m=loan.get(m + 12), change_pp=ch,
                         dearer=None if ch is None else bool(ch >= LOAN_RISE_PP), policy=note))
    counted = {r["start"]: r["dearer"] for r in rows if r["complete"] and not r["outer_bound"]}
    with_outer = {r["start"]: r["dearer"] for r in rows if r["complete"]}
    last = loan.dropna().index[-1] - 12
    base = base_share(lambda m: None if change(m) is None else change(m) >= LOAN_RISE_PP,
                      list(pd.period_range(BASE_FROM, last, freq="M")))
    raised = [r["start"] for r in rows if r["policy"]["status"] == "raised" and not r["outer_bound"]]
    return dict(episodes=rows, verdict=gated_verdict(counted, holds, fails),
                with_outer=gated_verdict(with_outer, holds, fails), base=base, policy_raised=raised,
                n_policy_raised=len(raised),
                policy_checked=sum(r["policy"]["status"] in ("raised", "not raised") for r in rows if not r["outer_bound"]))


def published_comparison(slides: list, pub: pd.Series, gap_pp: float) -> dict:
    """BPS's published rates beside L4's IMF-based before and after rates (counted slides only)."""
    rows, flags = [], {}
    for s in slides:
        if s["outer_bound"] or not s["complete"]:
            continue
        m = pd.Period(s["start"], "M")
        b, a = pub.get(m), pub.get(m + 12)
        rows.append(dict(start=s["start"], published_before=b, published_after=a,
                         gap_before_pp=b - s["inflation_before_pct"], gap_after_pp=a - s["inflation_after_pct"]))
        flags[s["start"]] = bool(a - b >= gap_pp)
    gaps = [abs(g) for r in rows for g in (r["gap_before_pp"], r["gap_after_pp"])]
    v = verdict(flags)
    return dict(episodes=rows, largest_gap_pp=max(gaps), n_rises_published=v["n_meeting"], n=v["n"])


def predictions_tally(path_csv: str, cells: dict, verdicts: dict) -> dict:
    """Compare the committed predictions (docs/2026-10-17-predictions-8.7.csv) with the results.
    cells: {(item, episode): outcome string}; verdicts: {item: 'k of n: word'}."""
    rows = list(csv.DictReader(open(path_csv)))
    out, matched, n = [], 0, 0
    for r in rows:
        key = (r["item"], r["episode"])
        got = cells.get(key) if key in cells else verdicts.get(r["item"])
        if got is None:
            continue
        hit = r["predicted"] == got
        out.append(dict(item=r["item"], episode=r["episode"], predicted=r["predicted"], result=got, matched=hit))
        n, matched = n + 1, matched + hit
    return dict(rows=out, n=n, n_matched=matched)


def outcome(flag) -> str | None:
    return None if flag is None else "met" if flag else "not met"


def household_links(slides: list, cpi: pd.Series, links: dict) -> dict:
    """Everything amendment 8.7 adds (unemployment, L7, is added separately once its source passes the rights
    test). links holds L1 to L4; the one-episode flags are recorded for every link."""
    rates, pub = read_rates(), read_published_inflation()
    l5 = savings_link(slides, rates["deposit"]["series"], cpi, HOLDS, FAILS)
    l6 = loans_link(slides, rates["loan"]["series"], rates["policy"], HOLDS, FAILS)
    comp = published_comparison(slides, pub, INFLATION_GAP_PP)
    prices_rose = verdict({s["start"]: bool(s["inflation_after_pct"] > 0) for s in slides
                           if s["complete"] and not s["outer_bound"]})
    flips = {k: one_episode_flips(v, HOLDS, FAILS) for k, v in links.items()}
    flips.update(L5=one_episode_flips(l5["verdict"], HOLDS, FAILS, MIN_FOR_WORD),
                 L6=one_episode_flips(l6["verdict"], HOLDS, FAILS, MIN_FOR_WORD))
    cells = {("L5", r["start"]): outcome(r.get("loses")) for r in l5["episodes"] if r["complete"]}
    cells |= {("L6", r["start"]): outcome(r["dearer"]) for r in l6["episodes"] if r["complete"]}
    cells |= {("policy note", r["start"]): r["policy"]["status"] for r in l6["episodes"]
              if r["policy"]["status"] in ("raised", "not raised")}
    in_range = lambda x: x is not None and 0.2 <= x <= 0.4
    verdicts = {
        "L5 verdict": f"{l5['verdict']['n_meeting']} of {l5['verdict']['n']}: {l5['verdict']['verdict']}",
        "L6 verdict": f"{l6['verdict']['n_meeting']} of {l6['verdict']['n']}: {l6['verdict']['verdict']}",
        "L5 share of all windows": "between a fifth and two fifths of windows" if in_range(l5["base"]["share"])
        else f"{l5['base']['share']:.2f} of windows",
        "BPS comparison": f"largest gap {'under' if comp['largest_gap_pp'] < 1 else 'at least'} 1 point; L4 count "
                          f"{'unchanged' if comp['n_rises_published'] == links['L4']['n_meeting'] else 'changed'}",
    }
    tally = predictions_tally(f"{BASE}/docs/2026-10-17-predictions-8.7.csv", cells, verdicts)
    checks = dict(deposit={k: v for k, v in rates["deposit"].items() if k != "series"},
                  loan={k: v for k, v in rates["loan"].items() if k != "series"},
                  published_first=str(pub.index[0]), published_last=str(pub.index[-1]))
    return dict(L5=l5, L6=l6, published=comp, prices_rose=prices_rose, fuel=fuel_list(slides), flips=flips,
                predictions=tally, checks=checks,
                rules=dict(deposit_months=DEPOSIT_MONTHS, loan_rise_pp=LOAN_RISE_PP, policy_rise_pp=POLICY_RISE_PP,
                           policy_months=POLICY_MONTHS, min_for_word=MIN_FOR_WORD, base_from=str(BASE_FROM),
                           base_from_year=BASE_FROM.year,
                           comparative_margin=COMPARATIVE_MARGIN, deposit_tax=DEPOSIT_TAX[-1][1]))


# --- fuel, described, never a verdict ----------------------------------------------------------------

FUEL_WINDOW = 12


def read_fuel() -> list[dict]:
    """data/fuel_price_changes.csv, written by extract_fuel.py from the stored regulations and notices."""
    rows = list(csv.DictReader(open(path("fuel"))))
    for r in rows:
        r["month"] = pd.Period(r["date"][:7], "M")
        r["pct_change"] = float(r["pct_change"]) if r["pct_change"] else None
    return rows


def fuel_window(rows: list, months: list, edges: set) -> dict:
    """Changes whose effective month is in the window, grouped by date (both fuels on one date are one change)."""
    by_date = {}
    for r in rows:
        if r["month"] in months:
            by_date.setdefault(r["date"], []).append(r)
    changes = []
    for date, rs in sorted(by_date.items()):
        dirs = {r["direction"] for r in rs}
        if len(dirs) != 1:
            raise SystemExit(f"fuel: {date} mixes a rise and a cut")
        changes.append(dict(date=date, year=int(date[:4]), direction=dirs.pop(), edge=pd.Period(date[:7], "M") in edges,
                            products=[dict(product=r["product"], pct_change=r["pct_change"], status=r["status"])
                                      for r in rs]))
    return dict(changes=changes, n_rises=sum(c["direction"] == "rise" for c in changes),
                n_cuts=sum(c["direction"] == "cut" for c in changes))


def fuel_list(slides: list) -> dict:
    """For each counted slide: Premium and Solar price changes in the twelve months up to and including the slide
    month (before) and the twelve months after it (after); the 1997 slide is not checked."""
    rows = read_fuel()
    out = []
    for s in slides:
        if s["outer_bound"]:
            out.append(dict(start=s["start"], checked=False))
            continue
        m = pd.Period(s["start"], "M")
        before = [m - k for k in range(FUEL_WINDOW - 1, -1, -1)]
        after = [m + k for k in range(1, FUEL_WINDOW + 1)]
        edges = {before[0], m, after[0], after[-1]}
        out.append(dict(start=s["start"], checked=True, before=fuel_window(rows, before, edges),
                        after=fuel_window(rows, after, edges)))
    covered = (min(r["month"] for r in rows), max(r["month"] for r in rows))
    return dict(episodes=out, n_changes_in_file=len({r["date"] for r in rows}),
                file_first=str(covered[0]), file_last=str(covered[1]), slowed=slowed_with_rise(slides, out),
                premium_regional_from_year=min(r["month"].year for r in rows if r["product"] == "Premium"
                                               and "outside java-madura-bali" in r["region_note"].lower()))


def slowed_with_rise(slides: list, fuel: list) -> dict:
    """Slides whose inflation slowed (L4 gap below zero) with a fuel rise in the twelve months up to the slide: the
    main rise in each (the one with the biggest verified change) and the smallest product change among them."""
    rows = []
    for s, e in zip(slides, fuel):
        if not e["checked"] or not s["complete"] or s["gap_pp"] >= 0:
            continue
        rises = [c for c in e["before"]["changes"] if c["direction"] == "rise"
                 and all(p["pct_change"] is not None for p in c["products"])]
        if rises:
            main = max(rises, key=lambda c: max(p["pct_change"] for p in c["products"]))
            rows.append(dict(start=s["start"], date=main["date"], year=main["year"],
                             min_pct=min(p["pct_change"] for p in main["products"])))
    return dict(episodes=rows, n=len(rows), min_pct=min(r["min_pct"] for r in rows) if rows else None)
