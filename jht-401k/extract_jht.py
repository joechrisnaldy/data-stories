"""Write data/jht_rates.csv from the PT Jamsostek and BPJS Ketenagakerjaan documents stored in sources/jht/.

Design section 3 and rules R1, R3 and R8. docs/jht-manifest.csv lists one row per figure: year, kind, value_pct,
applies_to, the stored document, its SHA-256, the page, a verbatim quote from that page and a note. Kinds:
  base              the rate set for member balances in a year (2005 to 2014, 2016 to 2020)
  yearend_reported  2015 only: no annual decree exists; the year-end rate BPJS itself reported
  incentive         2008 (2.1% of the end-2007 balance) and 2009 (1.60%, added to that year's rate)
  oneoff            the two 2013 payouts from the JHT development fund
  yield             the JHT program's published investment yield (2014 to 2025), not what members are credited

For each row this script checks the document's SHA-256, extracts the cited page's text (pdftotext -layout -f P -l P
for a PDF; for the one HTML page, the whole page with tags stripped by the standard library's parser, which also
unescapes entities), normalises whitespace, and asserts that the quote occurs exactly once on that page and starts
and ends on whole words. It then reads the percentage the quote prints, in Indonesian notation ("10,50%",
"10,6 %", "6,08 persen", or a bare "6,81" table cell when the quote has no percent sign), and asserts it equals
value_pct. A quote prints only its own figure, except a table-row quote, which runs from the row label to the
cited column, so the value is always the last figure in the quote (the note names the column). For base and
yearend_reported rows, every four-digit year (19xx or 20xx) the quote prints must equal the row's year; a quote
may print none (the 2009, 2015 and 2020 quotes do not).

Not checked here, so manual-review items: that each row's kind is right (a credited rate, not an investment yield
or a monthly claim rate); for a table-row quote, that it stops at the column the note names; and the year of a
yield, incentive or oneoff row, which the year rule does not cover (yield quotes print no year; the 2008 incentive
quote prints the balance year 2007). No string match
can tell these apart when the quote is unique on its page and its last figure equals value_pct.

Coverage checks: exactly one base or yearend_reported row for every year 2005 to 2020 and none outside it (BPJS
has published no credited rate for 2021 to 2025); at most one yield row a year, within 2014 to 2025; and the
bonus rows are exactly the ones R3 lists. Run from the post folder; needs poppler's pdftotext. The analysis reads
the CSV, never the documents. Any failure raises SystemExit with the reason.
"""
import csv
import hashlib
import re
import subprocess
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from pathlib import Path

MANIFEST = Path("docs/jht-manifest.csv")
SOURCES = Path("sources/jht")
OUT = Path("data/jht_rates.csv")
MANIFEST_COLUMNS = ["year", "kind", "value_pct", "applies_to", "document", "sha256", "page", "quote", "note"]
OUT_COLUMNS = ["year", "kind", "value_pct", "applies_to", "document"]
KINDS = ("base", "yearend_reported", "incentive", "oneoff", "yield")
CREDITED_KINDS = ("base", "yearend_reported")
CREDITED_YEARS = range(2005, 2021)  # R1 window
YIELD_YEARS = range(2014, 2026)  # R8
R3_BONUSES = sorted([(2008, "incentive"), (2009, "incentive"), (2013, "oneoff"), (2013, "oneoff")])
MAX_WORDS = 40
VALUE_RANGE = (Decimal("0"), Decimal("20"))  # percent a year; exclusive below, inclusive above
VALUE_FORMAT = re.compile(r"\d{1,2}\.\d{2}")
SHA_FORMAT = re.compile(r"[0-9a-f]{64}")
PERCENT = re.compile(r"(?<![\d.,])(\d{1,2}(?:,\d{1,2})?)\s?(?:%|persen\b)")
TABLE_CELL = re.compile(r"(?<![\d.,])(\d{1,2},\d{1,2})(?!\d|[.,]\d)")
YEAR = re.compile(r"(?<!\d)(?:19|20)\d{2}(?!\d)")
WORD_CHAR = re.compile(r"\w")


class _Text(HTMLParser):
    """Collects the text of an HTML page, dropping script and style, with a space at every tag."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        self.parts.append(" ")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class Documents:
    """Reads each stored file once: its SHA-256 and the normalised text of each cited page."""

    def __init__(self) -> None:
        self._sha: dict[Path, str] = {}
        self._pages: dict[tuple[Path, int], str] = {}

    def sha256(self, path: Path) -> str:
        if path not in self._sha:
            self._sha[path] = hashlib.sha256(path.read_bytes()).hexdigest()
        return self._sha[path]

    def page_text(self, path: Path, page: int) -> str:
        key = (path, page)
        if key not in self._pages:
            self._pages[key] = normalise(_pdf_page(path, page) if path.suffix == ".pdf" else _html_text(path, page))
        return self._pages[key]


def _pdf_page(path: Path, page: int) -> str:
    with path.open("rb") as fh:
        if fh.read(5) != b"%PDF-":
            raise SystemExit(f"{path}: not a PDF")
    cmd = ["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(path), "-"]
    done = subprocess.run(cmd, capture_output=True, text=True)
    if done.returncode != 0:
        raise SystemExit(f"{path} p.{page}: pdftotext failed: {done.stderr.strip()}")
    return done.stdout


def _html_text(path: Path, page: int) -> str:
    if path.suffix != ".html" or page != 1:
        raise SystemExit(f"{path}: an HTML document is one page (page 1); other formats are not read")
    parser = _Text()
    parser.feed(path.read_bytes().decode("utf-8"))
    parser.close()
    return "".join(parser.parts)


def read_manifest(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != MANIFEST_COLUMNS:
            raise SystemExit(f"{path}: columns {reader.fieldnames}, expected {MANIFEST_COLUMNS}")
        rows = list(reader)
    for line, row in enumerate(rows, 2):
        if None in row or None in row.values():  # an unquoted comma adds fields; a short row leaves some empty
            raise SystemExit(f"{path} line {line}: expected {len(MANIFEST_COLUMNS)} fields (quote any with a comma)")
    return rows


def quoted_value(quote: str) -> Decimal | None:
    """The last percentage the quote prints (see the module docstring), or None when it prints none."""
    figures = PERCENT.findall(quote) or TABLE_CELL.findall(quote)
    return Decimal(figures[-1].replace(",", ".")) if figures else None


def on_whole_words(text: str, start: int, end: int) -> bool:
    before, after = text[start - 1:start], text[end:end + 1]
    if WORD_CHAR.match(before or " ") or WORD_CHAR.match(after or " "):
        return False
    number_cut_before = text[start].isdigit() and re.search(r"\d[.,]$", text[max(0, start - 2):start])
    number_cut_after = text[end - 1].isdigit() and re.match(r"[.,]\d", text[end:end + 2])
    return not (number_cut_before or number_cut_after)


def check_fields(row: dict, label: str) -> tuple[Path, int, Decimal]:
    """Field formats; returns the document path, the page and value_pct."""
    if row["kind"] not in KINDS:
        raise SystemExit(f"{label}: unknown kind {row['kind']!r}")
    if not VALUE_FORMAT.fullmatch(row["value_pct"]) or not SHA_FORMAT.fullmatch(row["sha256"]):
        raise SystemExit(f"{label}: value_pct must look like 10.50 and sha256 like 64 lowercase hex digits")
    if not row["applies_to"].strip() or not row["note"].strip():
        raise SystemExit(f"{label}: applies_to and note must not be empty")
    path = Path(row["document"])
    if path.parent != SOURCES or not path.is_file():
        raise SystemExit(f"{label}: {path} is not a stored file directly under {SOURCES}/")
    try:
        page, value = int(row["page"]), Decimal(row["value_pct"])
    except (ValueError, InvalidOperation):
        raise SystemExit(f"{label}: page must be an integer and value_pct a number") from None
    if not VALUE_RANGE[0] < value <= VALUE_RANGE[1]:
        raise SystemExit(f"{label}: value_pct {value} is outside {VALUE_RANGE[0]} to {VALUE_RANGE[1]}")
    return path, page, value


def check_quote(text: str, quote: str, label: str) -> None:
    if quote != normalise(quote) or not quote:
        raise SystemExit(f"{label}: the quote must be non-empty with single spaces and no outer spaces")
    words = len(quote.split())
    if words >= MAX_WORDS:
        raise SystemExit(f"{label}: quote has {words} words, limit is under {MAX_WORDS}")
    count = len(re.findall(f"(?={re.escape(quote)})", text))  # overlapping occurrences count too
    if count != 1:
        raise SystemExit(f"{label}: quote found {count} times on its page, expected exactly once: {quote!r}")
    start = text.index(quote)
    if not on_whole_words(text, start, start + len(quote)):
        raise SystemExit(f"{label}: quote does not start and end on whole words: {quote!r}")


def check_row(row: dict, docs: Documents) -> dict:
    label = f"{row['year']} {row['kind']} ({row['document']} p.{row['page']})"
    if not row["year"].isdigit():
        raise SystemExit(f"{label}: year must be a number")
    path, page, value = check_fields(row, label)
    actual = docs.sha256(path)
    if actual != row["sha256"]:
        raise SystemExit(f"{label}: the file's SHA-256 {actual[:12]}... does not match the manifest's "
                         f"{row['sha256'][:12]}...")
    check_quote(docs.page_text(path, page), row["quote"], label)
    printed = quoted_value(row["quote"])
    if printed is None:
        raise SystemExit(f"{label}: the quote prints no percentage")
    if printed != value:
        raise SystemExit(f"{label}: the quote prints {printed}%, but value_pct is {value}")
    check_year(row, label)
    return {k: row[k] for k in OUT_COLUMNS}


def check_year(row: dict, label: str) -> None:
    """A base or yearend_reported quote may print no year, but every year it prints must be the row's year."""
    if row["kind"] not in CREDITED_KINDS:
        return
    others = sorted(set(YEAR.findall(row["quote"])) - {row["year"]})
    if others:
        raise SystemExit(f"{label}: the quote prints the year {', '.join(others)}, not the row's year {row['year']}")


def check_coverage(rows: list[dict]) -> None:
    credited = [int(r["year"]) for r in rows if r["kind"] in CREDITED_KINDS]
    outside = sorted(y for y in set(credited) if y not in CREDITED_YEARS)
    if outside:
        raise SystemExit(f"base or yearend_reported rows for {outside}: none allowed outside 2005 to 2020 "
                         "(BPJS has published no credited rate for 2021 to 2025)")
    missing = [y for y in CREDITED_YEARS if y not in credited]
    if missing:
        raise SystemExit(f"no base or yearend_reported row for {missing}")
    for year in CREDITED_YEARS:
        if credited.count(year) != 1:
            raise SystemExit(f"{year} has {credited.count(year)} base or yearend_reported rows, expected one")
    yields = [int(r["year"]) for r in rows if r["kind"] == "yield"]
    for year in sorted(set(yields)):
        if year not in YIELD_YEARS or yields.count(year) != 1:
            raise SystemExit(f"{year} has {yields.count(year)} yield rows; at most one a year, within 2014 to 2025")
    bonuses = sorted((int(r["year"]), r["kind"]) for r in rows if r["kind"] in ("incentive", "oneoff"))
    if bonuses != R3_BONUSES:
        raise SystemExit(f"bonus rows {bonuses} differ from the ones R3 lists {R3_BONUSES}")
    keys = [(r["year"], r["kind"], r["applies_to"]) for r in rows]
    if len(set(keys)) != len(keys):
        raise SystemExit("two rows share year, kind and applies_to")


def build(rows: list[dict], docs: Documents) -> list[dict]:
    """Checked output rows, sorted by year and kind (manifest order within them); SystemExit on a failed check."""
    checked = [check_row(r, docs) for r in rows]
    check_coverage(checked)
    return sorted(checked, key=lambda r: (int(r["year"]), KINDS.index(r["kind"])))


def main() -> None:
    docs = Documents()
    rows = read_manifest(MANIFEST)
    out = build(rows, docs)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=OUT_COLUMNS)
        writer.writeheader()
        writer.writerows(out)
    pages = {(r["document"], r["page"]) for r in rows}
    for r in out:
        print(f"{r['year']} {r['kind']:<16} {r['value_pct']:>6}  {r['applies_to']}")
    counts = {k: sum(r["kind"] == k for r in out) for k in KINDS}
    no_yield = [y for y in YIELD_YEARS if not any(r["kind"] == "yield" and int(r["year"]) == y for r in out)]
    print(f"wrote {OUT}: {len(out)} rows ({', '.join(f'{v} {k}' for k, v in counts.items())}) "
          f"from {len({d for d, _ in pages})} documents, {len(pages)} pages; every quote found once and its "
          f"figure equal to value_pct")
    print(f"no yield row for {no_yield}; no credited row for 2021 to 2025")


if __name__ == "__main__":
    main()
