"""Download every source file for Post 21 from its primary producer.

Nothing here is redistributed in the repository. Run this once and the six files in data/
reproduce exactly. Two of them are large (the OECD revenue files together are about 270 MB)
because the OECD SDMX endpoint has no server-side filter for the revenue classification.

    python3 fetch_data.py
"""

import os
import sys
import urllib.request
from pathlib import Path

DATA = Path(__file__).parent / "data"

SDMX = "https://sdmx.oecd.org/public/rest/data"
OWID = "https://ourworldindata.org/grapher"

# (filename, url, what it is)
SOURCES = [
    (
        "pit_thresh.csv",
        f"{SDMX}/OECD.CTP.TPS,DSD_TAX_PIT@DF_PIT_TOP_EARN_THRESH,1.0/all"
        "?format=csvfilewithlabels",
        "OECD Tax Database Table I.7: top statutory PIT rate and the earnings threshold "
        "at which it starts, expressed as a factor of the average annual wage",
    ),
    (
        "rev_oecd.csv",
        f"{SDMX}/OECD.CTP.TPS,DSD_REV_COMP_OECD@DF_RSOECD,1.0/all"
        "?startPeriod=2015&format=csvfilewithlabels",
        "OECD Revenue Statistics: tax revenue by the full OECD revenue classification",
    ),
    (
        "rev_asap.csv",
        f"{SDMX}/OECD.CTP.TPS,DSD_REV_COMP_ASAP@DF_RSASAP,1.0/all"
        # 2015, not 2018. An earlier version of this file requested startPeriod=2018, which
        # truncated Indonesia's series and was then mistaken for a property of the source. The
        # dataflow actually carries Indonesia from 2015.
        "?startPeriod=2015&format=csvfilewithlabels",
        "OECD Revenue Statistics in Asia and the Pacific, used only for Indonesia",
    ),
    (
        "idd.csv",
        f"{SDMX}/OECD.WISE.INE,DSD_WISE_IDD@DF_IDD,1.0/all"
        "?startPeriod=2015&format=csvfilewithlabels",
        "OECD Income Distribution Database: poverty rates and Gini on market, gross "
        "and disposable income",
    ),
    (
        "gdp.csv",
        f"{OWID}/gdp-per-capita-worldbank.csv?v=1&csvType=full&useColumnShortNames=true",
        "GDP per capita, PPP, constant 2021 international dollars, from Eurostat, the OECD, the "
        "IMF and the World Bank jointly, with minor processing by Our World in Data. Required by "
        "build_analysis.py; an earlier version of this file omitted it, so a clean checkout could "
        "not reproduce the analysis",
    ),
    (
        "le.csv",
        f"{OWID}/life-expectancy.csv?v=1&csvType=full&useColumnShortNames=true",
        "Life expectancy at birth: a Riley (2005), Zijdeman et al. (2015), HMD (2025) and "
        "UN WPP (2024) composite, with major processing by Our World in Data",
    ),
]


def fetch(name: str, url: str, what: str) -> None:
    target = DATA / name
    if target.exists():
        print(f"  skip {name} ({target.stat().st_size / 1e6:.1f} MB, already present)")
        return
    print(f"  get  {name}: {what}")
    req = urllib.request.Request(url, headers={"User-Agent": "data-stories/1.0"})
    # Download to a .part file and rename only on success. Writing straight to `target` would
    # truncate it before the first byte arrived, so an interrupted 151 MB transfer left a stub
    # that the exists() guard above then reported as "already present" on every later run.
    tmp = target.with_suffix(target.suffix + ".part")
    try:
        with urllib.request.urlopen(req, timeout=300) as r, open(tmp, "wb") as f:
            f.write(r.read())
        os.replace(tmp, target)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    print(f"       done, {target.stat().st_size / 1e6:.1f} MB")


def main() -> int:
    DATA.mkdir(exist_ok=True)
    print(f"Writing to {DATA}")
    for name, url, what in SOURCES:
        fetch(name, url, what)
    print("\nAll sources present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
