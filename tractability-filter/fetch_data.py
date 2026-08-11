"""Download every input for Post 23 into data/.

Five sources, all public and free, none needing a key or registration:

  1. WHO Global Health Estimates 2021 (2024 release), DALYs by cause, by World Bank income
     group and by country. Direct xlsx download from cdn.who.int.
  2. WHO Global Health Observatory API, indicators RS_196, RS_198 and RS_246 for road deaths,
     death rate and road user type. Taken directly because Our World in Data's copy of the
     road death rate stops at 2019 while WHO has published 2021.
  3. Our World in Data grapher CSVs for electric car sales and the AI series.
  4. ClinicalTrials.gov API v2, study counts per condition query.
  5. NIH RePORTER API v2, award amounts per RCDC spending category.

Everything goes through curl rather than urllib, for two reasons recorded in the design doc:
this machine's Python ships an EMPTY CA bundle (ssl.create_default_context().cert_store_stats()
returns zero x509 certificates), and ClinicalTrials.gov answers curl but returns HTTP 403 to
urllib regardless of the User-Agent sent. Verification is never disabled.

Run:  python3 fetch_data.py
"""

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from conditions import CONDITIONS

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

WHO_BASE = ("https://cdn.who.int/media/docs/default-source/gho-documents/"
            "global-health-estimates")
WHO_FILES = [
    "ghe2021_daly_wbincome_new.xlsx",    # DALYs by cause and World Bank income group
    "ghe2021_daly_bycountry_2021.xlsx",  # DALYs by cause and country; needed for the US, because
                                         # NIH money is US money and must meet US burden
    "ghe2021_daly_bycountry_2010.xlsx",  # 2010 comparison year for the chart 4 medicine row
    # DEATHS, not DALYs. Added in fact-check round 6, which found the post's opening two numbers
    # taken from Our World in Data's aggregation and attributed to WHO. WHO's own table says
    # 1,184,514 for 2000 and 1,182,759 for 2021; OWID's copy says 1,177,422 and 1,174,078, and its
    # country values differ from WHO's published country file in 177 of 183 countries. A mirror is
    # not the publisher. This file is the publisher.
    "ghe2021_deaths_global_new2.xlsx",
]

GHO = "https://ghoapi.azureedge.net/api"
GHO_INDICATORS = {
    "RS_196": "who_road_deaths_count.json",     # estimated number of road traffic deaths, 2021
    "RS_198": "who_road_death_rate.json",       # estimated rate per 100,000, 2021
    "RS_246": "who_road_user_type.json",        # distribution of deaths by road user type, 2016
}

# Terms probed to DISCLOSE that road injury cannot be mapped onto the registry, not to feed the
# analysis. Round 1 of the fact-check established that every pre-registered road-injury term was
# crash vocabulary, while ClinicalTrials.gov indexes trauma by injury pathology. Swapping these
# in after the fact would be exactly the post-hoc move this repository refuses, so the analysis
# keeps the pre-registered terms and the post reports the problem and the sensitivity.
ROAD_INJURY_PROBE = ["road traffic accident OR motor vehicle accident", "traumatic brain injury",
                     "spinal cord injury", "fractures", "multiple trauma", "wounds and injuries"]

OWID_SLUGS = [
    "death-rate-road-traffic-injuries",              # OWID's copy, stops at 2019, kept for context
    "deaths-from-road-injuries",                     # WHO GHE, absolute deaths
    "electric-car-sales-share",                      # IEA, EV share of new car sales
    "private-investment-in-artificial-intelligence",  # Stanford AI Index / Quid
    "corporate-investment-in-artificial-intelligence-by-type",
    "computation-used-to-train-notable-artificial-intelligence-systems",  # Epoch AI
]

CT_API = "https://clinicaltrials.gov/api/v2/studies"
NIH_API = "https://api.reporter.nih.gov/v2/projects/search"
NIH_FY = 2024              # latest fiscal year certain to be complete
NIH_PAGE = 500             # RePORTER maximum page size
NIH_OFFSET_CAP = 14000     # RePORTER refuses offsets beyond ~15000


# --------------------------------------------------------------------------- transport


def _run(args, timeout=300):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)


def curl_download(url, target):
    """Download to a temporary file and rename, so a failure never leaves a half file."""
    tmp = target + ".part"
    r = _run(["curl", "-sSL", "--fail", "--max-time", "600", "-o", tmp, url])
    if r.returncode != 0 or not os.path.exists(tmp) or os.path.getsize(tmp) == 0:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise RuntimeError(f"download failed: {url}\n{r.stderr.strip()[:300]}")
    os.replace(tmp, target)
    return os.path.getsize(target)


def curl_json(url, params=None, post=None, tries=4):
    for attempt in range(tries):
        if post is None:
            args = ["curl", "-sG", "--max-time", "90", url]
            for k, v in (params or {}).items():
                args += ["--data-urlencode", f"{k}={v}"]
        else:
            args = ["curl", "-s", "--max-time", "120", "-X", "POST", url,
                    "-H", "Content-Type: application/json", "-d", json.dumps(post)]
        r = _run(args)
        try:
            return json.loads(r.stdout)
        except Exception:
            if attempt == tries - 1:
                raise RuntimeError(f"bad JSON from {url}: {r.stdout[:200]!r}")
    raise AssertionError("unreachable")


# --------------------------------------------------------------------------- steps


def fetch_files():
    print("== WHO Global Health Estimates")
    for f in WHO_FILES:
        n = curl_download(f"{WHO_BASE}/{f}", os.path.join(DATA, f))
        print(f"   {f:38s} {n:>10,} bytes")

    print("== Our World in Data grapher CSVs")
    for slug in OWID_SLUGS:
        url = (f"https://ourworldindata.org/grapher/{slug}.csv"
               "?v=1&csvType=full&useColumnShortNames=true")
        target = os.path.join(DATA, f"{slug}.csv")
        n = curl_download(url, target)
        with open(target, encoding="utf-8") as fh:
            head = fh.readline()
        if head.lstrip().startswith("{"):
            raise RuntimeError(f"{slug}: OWID returned an error body, not a CSV: {head[:160]}")
        print(f"   {slug:56s} {n:>9,} bytes")


def fetch_trials():
    """Count studies for every alternate term. The build uses the largest count per condition."""
    print("== ClinicalTrials.gov study counts")
    jobs = [(c["ghe_name"], t) for c in CONDITIONS for t in c["ct_terms"]]

    def one(job):
        _, term = job
        d = curl_json(CT_API, {"query.cond": term, "countTotal": "true", "pageSize": 1})
        return d["totalCount"]

    with ThreadPoolExecutor(max_workers=6) as ex:
        counts = list(ex.map(one, jobs))

    out = {}
    for (name, term), n in zip(jobs, counts):
        out.setdefault(name, {})[term] = n
    with open(os.path.join(DATA, "ct_counts.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    for name in sorted(out):
        best = max(out[name], key=out[name].get)
        print(f"   {name[:44]:46s} {out[name][best]:>7,}  via {best!r}")
    return out


def fetch_who_roads():
    """WHO Global Health Observatory, direct.

    Our World in Data's copy of the road death rate stops at 2019 and the draft originally
    attributed that stopping point to WHO. WHO has published 2021. These three indicators come
    from WHO's own API so the post is never quoting a mirror for a claim about what WHO has
    published.
    """
    print("== WHO Global Health Observatory, road safety")
    for code, name in GHO_INDICATORS.items():
        d = curl_json(f"{GHO}/{code}")
        rows = d["value"]
        with open(os.path.join(DATA, name), "w") as fh:
            json.dump(rows, fh)
        years = sorted({r["TimeDim"] for r in rows})
        print(f"   {code} -> {name:30s} {len(rows):>5} rows, years {years}")


def probe_road_injury_terms():
    print("== ClinicalTrials.gov road-injury mapping probe (disclosure only, not analysis input)")
    with ThreadPoolExecutor(max_workers=4) as ex:
        counts = list(ex.map(
            lambda t: curl_json(CT_API, {"query.cond": t, "countTotal": "true",
                                         "pageSize": 1})["totalCount"], ROAD_INJURY_PROBE))
    out = dict(zip(ROAD_INJURY_PROBE, counts))
    with open(os.path.join(DATA, "ct_road_injury_probe.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    for t, n in out.items():
        print(f"   {t:52s} {n:>7,}")
    return out


def fetch_trials_by_year(years=range(2008, 2025)):
    """Registry-wide count of studies first posted in each calendar year.

    Used only for the chart 4 medicine row, which pairs the growth of registered research
    against the change in burden. This is the whole registry, not just this post's conditions,
    and the chart labels it as such.
    """
    print("== ClinicalTrials.gov studies first posted per year")

    def one(y):
        d = curl_json(CT_API, {
            "filter.advanced": f"AREA[StudyFirstPostDate]RANGE[{y}-01-01,{y}-12-31]",
            "countTotal": "true", "pageSize": 1})
        return d["totalCount"]

    with ThreadPoolExecutor(max_workers=6) as ex:
        counts = list(ex.map(one, years))
    out = {str(y): n for y, n in zip(years, counts)}
    with open(os.path.join(DATA, "ct_by_year.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    for y, n in out.items():
        print(f"   {y}  {n:>8,}")
    return out


def harvest_nih_categories(sample_pages=10):
    """Build the RCDC category id to name map.

    RePORTER returns spending_categories (ids) and spending_categories_desc (names joined by
    '; ') in the SAME order, so they can be paired positionally. Verified on sampled records:
    any project whose two lists differ in length is skipped rather than guessed at.
    """
    print("== NIH RCDC category harvest")
    id2name, skipped = {}, 0
    for page in range(sample_pages):
        d = curl_json(NIH_API, post={
            "criteria": {"fiscal_years": [NIH_FY]},
            "include_fields": ["SpendingCategories", "SpendingCategoriesDesc"],
            "limit": NIH_PAGE, "offset": page * NIH_PAGE,
        })
        results = d.get("results") or []
        if not results:
            break
        for r in results:
            ids = r.get("spending_categories") or []
            desc = (r.get("spending_categories_desc") or "").split("; ")
            desc = [x for x in desc if x]
            if len(ids) != len(desc):
                skipped += 1
                continue
            for i, nm in zip(ids, desc):
                id2name[str(i)] = nm
    print(f"   {len(id2name)} categories from {sample_pages * NIH_PAGE} sampled projects "
          f"({skipped} projects skipped on length mismatch)")
    with open(os.path.join(DATA, "nih_categories.json"), "w") as fh:
        json.dump(id2name, fh, indent=1, sort_keys=True)
    return id2name


def fetch_nih_spend(id2name):
    """Sum award_amount over every FY project tagged with each needed category.

    RCDC categories overlap by construction and do not partition NIH's budget. That is NIH's
    own documented behaviour and the post says so rather than presenting a partition.
    """
    print(f"== NIH RePORTER award totals, FY{NIH_FY}")
    name2id = {v: k for k, v in id2name.items()}
    wanted = sorted({cat for c in CONDITIONS
                     for cat in ([c["nih"]] + list(c.get("nih_alt", []))) if cat})
    missing = [w for w in wanted if w not in name2id]
    if missing:
        print(f"   NOT MATCHED ({len(missing)}): {missing}")

    def one(cat):
        cid = int(name2id[cat])
        total, n, offset, truncated = 0.0, 0, 0, False
        while True:
            d = curl_json(NIH_API, post={
                "criteria": {"fiscal_years": [NIH_FY],
                             "spending_categories": {"Values": [cid], "match_all": False}},
                "include_fields": ["AwardAmount"],
                "limit": NIH_PAGE, "offset": offset,
            })
            res = d.get("results") or []
            total += sum((r.get("award_amount") or 0) for r in res)
            n += len(res)
            reported = d.get("meta", {}).get("total", 0)
            offset += NIH_PAGE
            if len(res) < NIH_PAGE or offset > min(reported, NIH_OFFSET_CAP):
                truncated = reported > NIH_OFFSET_CAP
                return dict(category=cat, category_id=cid, projects_summed=n,
                            projects_reported=reported, award_total_usd=total,
                            truncated=truncated)

    todo = [w for w in wanted if w in name2id]
    with ThreadPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(one, todo))

    out = {r["category"]: r for r in rows}
    for r in sorted(rows, key=lambda x: -x["award_total_usd"]):
        flag = "  TRUNCATED" if r["truncated"] else ""
        print(f"   {r['category'][:52]:54s} ${r['award_total_usd']/1e6:>9,.1f}M  "
              f"{r['projects_summed']:>6,} projects{flag}")
    with open(os.path.join(DATA, "nih_spend.json"), "w") as fh:
        json.dump({"fiscal_year": NIH_FY, "unmatched_categories": missing, "totals": out},
                  fh, indent=1, sort_keys=True)
    return out


def main():
    """`python3 fetch_data.py` runs everything; `python3 fetch_data.py nih` runs only the NIH
    steps, so a category-mapping correction does not force a re-download of the rest."""
    only = sys.argv[1] if len(sys.argv) > 1 else None
    os.makedirs(DATA, exist_ok=True)
    if only == "roads":
        fetch_who_roads()
        probe_road_injury_terms()
        return
    if only == "extra":
        fetch_files()
        fetch_trials_by_year()
        return
    if only is None:
        fetch_files()
        fetch_who_roads()
        fetch_trials()
        probe_road_injury_terms()
        fetch_trials_by_year()
    id2name = harvest_nih_categories()
    fetch_nih_spend(id2name)
    print("\nDone. All inputs are in data/ and are gitignored; see data/README.md.")


if __name__ == "__main__":
    sys.exit(main())
