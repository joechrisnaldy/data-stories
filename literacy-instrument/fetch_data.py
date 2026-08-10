"""Download every source file for Post 22 from its primary producer.

Nothing here is redistributed in the repository. Run this once and the four files in data/
reproduce exactly. All of it is small; there is no large download in this post.

    python3 fetch_data.py

Two producers:

  The DHS Program's public API, which needs no registration and no key. It serves the full
  percent distribution behind every published literacy rate: the never-tested column, the two
  card-test outcomes, and the residuals. This is the spine of the post.

  Our World in Data, for UNESCO's record of HOW each country's literacy rate was produced. That
  is the second movement: which countries are tested and which are taken at their word.
"""

import os
import ssl
import sys
import urllib.request
from pathlib import Path

DATA = Path(__file__).parent / "data"


def ssl_context() -> ssl.SSLContext:
    """A verifying context that works on a stock machine.

    Python.org builds on macOS ship an empty certificate bundle until the user runs
    "Install Certificates.command", so urllib fails every HTTPS request with
    CERTIFICATE_VERIFY_FAILED even though the system trust store is fine. Fall back to
    certifi, then to the system bundle, rather than the usual advice of disabling
    verification. Nothing here is worth downloading over an unverified connection.
    """
    ctx = ssl.create_default_context()
    if ctx.cert_store_stats()["x509"]:
        return ctx
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    for bundle in ("/etc/ssl/cert.pem", "/usr/local/etc/openssl/cert.pem"):
        if os.path.exists(bundle):
            return ssl.create_default_context(cafile=bundle)
    raise RuntimeError(
        "No usable CA bundle. On macOS run Install Certificates.command from your Python "
        "install, or pip install certifi."
    )

DHS = "https://api.dhsprogram.com/rest/dhs"
OWID = "https://ourworldindata.org/grapher"

# The eight indicators are the eight columns of the DHS literacy table, and they are mutually
# exclusive and exhaustive: they sum to 100 for every survey. SCH is the one that matters most
# and is the easiest to miss, because it is the group that was never handed the card at all.
LIT_INDICATORS = ",".join([
    "ED_LITR_W_SCH",   # higher than secondary schooling: literate by assumption, NOT tested
    "ED_LITR_W_RDW",   # can read a whole sentence
    "ED_LITR_W_RDP",   # can read PART of a sentence, and still counted literate
    "ED_LITR_W_NRD",   # cannot read at all
    "ED_LITR_W_NCD",   # no card available in the respondent's language
    "ED_LITR_W_BLD",   # blind or visually impaired
    "ED_LITR_W_MIS",   # missing
    "ED_LITR_W_LIT",   # the published headline: SCH + RDW + RDP
])

SOURCES = [
    (
        "dhs_literacy.json",
        f"{DHS}/data?indicatorIds={LIT_INDICATORS}&breakdown=national&perpage=20000&f=json",
        "DHS literacy distribution, every survey in the API, women 15-49. The eight indicators "
        "are the eight columns of the published literacy table",
    ),
    (
        "dhs_surveys.json",
        f"{DHS}/surveys?perpage=20000&f=json",
        "DHS survey metadata: survey type, phase and fieldwork years. The PHASE is load-bearing. "
        "DHS-VI and earlier did not administer the card test to anyone with secondary education "
        "or above; DHS-7 and DHS-8 exempt only those above secondary. Mixing phases in one trend "
        "compares two different instruments",
    ),
    (
        "dhs_education.json",
        f"{DHS}/data?indicatorIds=ED_EDUC_W_SEH,ED_EDUC_W_HGH&breakdown=national"
        "&perpage=20000&f=json",
        "Share of women with secondary-or-higher and with more-than-secondary education. Required "
        "by build_analysis.py to tell the two coding rules apart: the never-tested column equals "
        "the first under the old rule and the second under the new one. Without this the "
        "classification would have to guess from the fieldwork year, which is wrong because the "
        "two regimes overlap",
    ),
    (
        "mode_of_reporting.csv",
        f"{OWID}/mode-of-reporting-literacy-rates.csv?v=1&csvType=full&useColumnShortNames=true",
        "UNESCO's record of how each country's literacy rate was obtained: self-reported by the "
        "individual, self-reported by the head of household, an actual literacy test, or an "
        "indirect estimate. 169 countries, 1975 to 2016",
    ),
    (
        "dhs_vs_unesco.csv",
        f"{OWID}/literacy-rate-adult-total-dhs-surveys-vs-unesco.csv"
        "?v=1&csvType=full&useColumnShortNames=true",
        "DHS and UNESCO adult literacy rates side by side, plus population and region. Used only "
        "for the country-years where BOTH are present, which is 33 of them",
    ),
]


def fetch(name: str, url: str, what: str) -> None:
    target = DATA / name
    if target.exists():
        print(f"  skip {name} ({target.stat().st_size / 1e3:.0f} KB, already present)")
        return
    print(f"  get  {name}: {what}")
    req = urllib.request.Request(url, headers={"User-Agent": "data-stories/1.0"})
    # Download to a .part file and rename only on success, so an interrupted transfer cannot
    # leave a stub that the exists() guard above then reports as complete on every later run.
    tmp = target.with_suffix(target.suffix + ".part")
    try:
        with urllib.request.urlopen(req, timeout=180, context=ssl_context()) as r, open(tmp, "wb") as f:
            f.write(r.read())
        os.replace(tmp, target)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    print(f"       done, {target.stat().st_size / 1e3:.0f} KB")


def main() -> int:
    DATA.mkdir(exist_ok=True)
    print(f"Writing to {DATA}")
    for name, url, what in SOURCES:
        fetch(name, url, what)
    print("\nAll sources present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
