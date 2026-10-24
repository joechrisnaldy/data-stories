"""Post 28: JHT and the 401(k). Writes results.json from the frozen data files and docs/sources.json.

Every rule here is the pre-registration's (docs/2026-10-21-jht-401k-design.md, R1 to R8, amendment A1); the rule
it implements is named beside each step. The readers, file hashes and row filters live in profile_data.py, which this
script imports, so the two cannot disagree. Run from the post folder: python3 build_analysis.py
"""
import csv
import hashlib
import json

import pandas as pd

import profile_data as pdata

WINDOW = range(2005, 2021)          # R1: calendar years 2005 to 2020
PUBLISHED = range(2014, 2026)       # R8: years whose publication status is shown
PRICE_YEAR = 2020                   # R5: balances valued in prices of December of this year
SOURCES = "docs/sources.json"
HAS_YEAR = 2024                     # R7: How America Saves' latest year that is not an estimate (A2)


def sample_id(items) -> str:
    """A short hash of the entities a statistic was computed on, so prose can pair figures from one sample."""
    return hashlib.sha256(json.dumps(sorted(map(str, items))).encode()).hexdigest()[:12]


def src(key: str) -> dict:
    with open(SOURCES, encoding="utf-8") as fh:
        return json.load(fh)[key]["values"]


# --- inputs -------------------------------------------------------------------------------------------

def jht_rates() -> dict:
    """data/jht_rates.csv by kind: {kind: {year: [value_pct, ...]}}."""
    out = {}
    with open(pdata.path("jht_rates"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out.setdefault(r["kind"], {}).setdefault(int(r["year"]), []).append(float(r["value_pct"]))
    return out


def credited_rates(kinds: dict) -> dict:
    """R1, R3: one rate per year 2005 to 2020: the base rate, or 2015's year-end reported rate."""
    rates = {}
    for kind in ("base", "yearend_reported"):
        for y, vals in kinds.get(kind, {}).items():
            if y in WINDOW:
                if y in rates or len(vals) != 1:
                    raise SystemExit(f"jht_rates.csv: more than one credited rate for {y}")
                rates[y] = vals[0] / 100
    missing = sorted(set(WINDOW) - set(rates))
    if missing:
        raise SystemExit(f"jht_rates.csv: no credited rate for {missing}")
    return rates


def cpi_points(key: str) -> tuple[dict, dict]:
    """December index and annual-average index per year, from the shared IMF reader."""
    s, _ = pdata.read_cpi(key)
    dec, avg = {}, {}
    for y in range(WINDOW.start - 1, WINDOW.stop):
        months = s[[p for p in s.index if p.year == y]]
        if len(months) != 12:
            raise SystemExit(f"{key}: {y} has {len(months)} monthly values")
        dec[y] = float(s[pd.Period(f"{y}-12", "M")])
        avg[y] = float(months.mean())
    return dec, avg


def us_returns() -> tuple[dict, dict]:
    """Damodaran's annual S&P 500 (with dividends) and 10-year Treasury bond returns, from the shared reader."""
    df, _ = pdata.read_damodaran()
    stocks, bonds = pdata.DAMODARAN_COLUMNS
    return ({y: float(df.at[y, stocks]) for y in WINDOW}, {y: float(df.at[y, bonds]) for y in WINDOW})


# --- the saver (R2, R3, R4, R5) -----------------------------------------------------------------------

def grow(rate: dict, cpi_dec: dict, cpi_avg: dict, opening_bonus: dict | None = None) -> dict:
    """R2: one real unit a year, raised by the annual-average CPI, paid mid-year; the year's rate on the opening
    balance plus half of it on the year's contribution. opening_bonus[y] is extra credited on the opening balance
    only (R3). R5: the result is the real balance over the real total put in, both in December prices of the
    same year."""
    bonus = opening_bonus or {}
    base = cpi_avg[WINDOW.start]
    bal, path = 0.0, {}
    for i, y in enumerate(WINDOW, 1):
        c = cpi_avg[y] / base
        bal = bal * (1 + rate[y] + bonus.get(y, 0.0)) + c * (1 + rate[y] / 2)
        put_in_real = i * cpi_dec[y] / base     # the contributions so far, valued in December-y prices
        path[y] = bal / put_in_real
    return path


def jht_bonuses(kinds: dict) -> tuple[dict, dict]:
    """R3: the 2008 incentive (2.1% of the end-2007 balance, so of the 2008 opening balance) and the 2013 payouts
    are paid on the opening balance; the 2009 incentive is added to that year's rate."""
    opening = {}
    for kind in ("incentive", "oneoff"):
        for y, vals in kinds.get(kind, {}).items():
            if y == 2009 and kind == "incentive":
                continue
            opening[y] = opening.get(y, 0.0) + sum(vals) / 100
    added = {2009: sum(kinds["incentive"][2009]) / 100}
    if sorted(opening) != [2008, 2013]:
        raise SystemExit(f"unexpected opening-balance bonus years {sorted(opening)}")
    return opening, added


def lines() -> dict:
    kinds = jht_rates()
    jht = credited_rates(kinds)
    opening, added = jht_bonuses(kinds)
    jht_with = {y: r + added.get(y, 0.0) for y, r in jht.items()}
    idn_dec, idn_avg = cpi_points("cpi_idn")
    usa_dec, usa_avg = cpi_points("cpi_usa")
    stocks, bonds = us_returns()
    fee = src("vanguard_tr2045_expenses")["total_expenses_pct"] / 100
    stock_share = src("vanguard_glide_age20")["stock_pct"] / 100          # R4: 90% from age 20 to 40
    net = lambda r: (1 + r) * (1 - fee) - 1
    sp500 = {y: net(stocks[y]) for y in WINDOW}
    mix = {y: net(stock_share * stocks[y] + (1 - stock_share) * bonds[y]) for y in WINDOW}
    paths = {
        "jht": grow(jht_with, idn_dec, idn_avg, opening),
        "jht_base_only": grow(jht, idn_dec, idn_avg),
        "sp500": grow(sp500, usa_dec, usa_avg),
        "mix_90_10": grow(mix, usa_dec, usa_avg),
    }
    # A3: the fee is charged on the year's closing value; the other reading of R4, the fee subtracted from the
    # return, is kept as a check (it moves the US multiples in the third decimal; the post prints one decimal)
    gross_mix = {y: stock_share * stocks[y] + (1 - stock_share) * bonds[y] for y in WINDOW}
    check = {"sp500": grow({y: stocks[y] - fee for y in WINDOW}, usa_dec, usa_avg),
             "mix_90_10": grow({y: gross_mix[y] - fee for y in WINDOW}, usa_dec, usa_avg)}
    years = list(WINDOW)
    out = {k: {"path": {str(y): v for y, v in p.items()}, "multiple": p[WINDOW.stop - 1],
               "low_year": min(p, key=p.get), "low": min(p.values()),
               "n": len(years), "sample": sample_id(years)} for k, p in paths.items()}
    out["fee_subtracted_check"] = {k: p[WINDOW.stop - 1] for k, p in check.items()}
    out["rules"] = {"stock_share": stock_share, "fee": fee, "first_year": WINDOW.start,
                    "last_year": WINDOW.stop - 1, "years": len(years), "fee_pct": fee * 100,
                    "stock_pct": stock_share * 100, "bond_pct": (1 - stock_share) * 100}
    return out, jht, idn_dec


# --- year by year (R6, A1) ----------------------------------------------------------------------------

def year_by_year(jht: dict, idn_dec: dict) -> dict:
    """R6: JHT's real rate each year against the IMF December-to-December inflation; A1: and against BPS's published
    December year-on-year rate (Bank Indonesia's Data Inflasi)."""
    bps, _ = pdata.read_published_inflation()
    rows = {}
    for y in WINDOW:
        imf_pi = idn_dec[y] / idn_dec[y - 1] - 1
        bps_pi = bps[pd.Period(f"{y}-12", "M")] / 100
        rows[str(y)] = {"rate_pct": jht[y] * 100, "imf_inflation_pct": imf_pi * 100,
                        "bps_inflation_pct": bps_pi * 100,
                        "real_imf_pct": ((1 + jht[y]) / (1 + imf_pi) - 1) * 100,
                        "real_bps_pct": ((1 + jht[y]) / (1 + bps_pi) - 1) * 100,
                        "imf_bps_gap_pp": (imf_pi - bps_pi) * 100}
    neg = lambda k: [y for y, r in rows.items() if r[k] < 0]
    years = list(rows)
    first_last = lambda ys: {"first": int(ys[0]), "last": int(ys[-1])} if ys else {}
    return {"rows": rows, "n_positive_imf": len(years) - len(neg("real_imf_pct")),
            "negative_real_imf": {"years": neg("real_imf_pct"), "n": len(neg("real_imf_pct")), **first_last(neg("real_imf_pct"))},
            "negative_real_bps": {"years": neg("real_bps_pct"), "n": len(neg("real_bps_pct"))},
            "n": len(years), "sample": sample_id(years)}


# --- what goes in (R7) --------------------------------------------------------------------------------

def contributions() -> dict:
    jht = src("pp46_jht_contribution")
    jp = src("pp45_jp_split")
    deferral = src("has_average_deferral")[f"y{HAS_YEAR}_pct"]
    total = src("has_total_contribution")[f"y{HAS_YEAR}_pct"]
    cpf = pdata.cpf_young_rates()
    return {
        "jht": {"worker_pct": jht["worker_pct"], "employer_pct": jht["employer_pct"], "total_pct": jht["total_pct"]},
        "jp": {"worker_pct": jp["worker_pct"], "employer_pct": jp["employer_pct"],
               "total_pct": jp["worker_pct"] + jp["employer_pct"]},
        "k401": {"year": HAS_YEAR, "worker_pct": deferral, "employer_pct": round(total - deferral, 10),
                 "total_pct": total},
        "cpf": cpf,
    }


# --- what the saver is shown (R8) ---------------------------------------------------------------------

def published() -> dict:
    kinds = jht_rates()
    credited = set(kinds.get("base", {})) | set(kinds.get("yearend_reported", {}))
    yields = {y: v[0] for y, v in kinds.get("yield", {}).items()}
    rows = {str(y): {"credited_published": y in credited, "yield_pct": yields.get(y)} for y in PUBLISHED}
    last = max(y for y in credited)
    years = [y for y in PUBLISHED]
    return {"rows": rows, "last_credited_year": last,
            "years_without_credited": [y for y in years if y not in credited],
            "years_without_credited_n": len([y for y in years if y not in credited]),
            "years_with_yield": sorted(y for y in yields if y in PUBLISHED),
            "years_with_yield_n": len([y for y in yields if y in PUBLISHED]),
            "years_without_yield": [y for y in PUBLISHED if y not in yields],
            "n": len(years), "sample": sample_id(years)}


# --- predictions (design section 6) -------------------------------------------------------------------

def predictions(g: dict, yby: dict, contrib: dict) -> dict:
    m = {k: g[k]["multiple"] for k in ("sp500", "mix_90_10", "jht", "jht_base_only")}
    bonus_effect = abs(m["jht"] - m["jht_base_only"])
    out = {
        "P1_order": m["sp500"] > m["mix_90_10"] > m["jht"],
        "P2_jht_above_one": m["jht"] > 1,
        "P3_negative_real_year": yby["negative_real_imf"]["n"] >= 1,
        "P4_bonus_effect_below_gap": bonus_effect < abs(m["mix_90_10"] - m["jht"]),
        "P5_jht_below_401k": contrib["jht"]["total_pct"] < contrib["k401"]["total_pct"],
        "bonus_effect": bonus_effect,
    }
    flags = [v for k, v in out.items() if k.startswith("P")]
    return {**out, "n_true": sum(flags), "n": len(flags)}


def main() -> None:
    pdata.check_hashes()
    g, jht, idn_dec = lines()
    yby = year_by_year(jht, idn_dec)
    contrib = contributions()
    pub = published()
    results = {"growth": g, "year_by_year": yby, "contributions": contrib, "published": pub,
               "predictions": predictions(g, yby, contrib)}
    with open("results.json", "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote results.json")


if __name__ == "__main__":
    main()
