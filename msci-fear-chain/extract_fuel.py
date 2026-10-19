"""Write data/fuel_price_changes.csv from the fuel documents stored in sources/fuel/.

Design amendment 8.7, "Fuel, described, never a verdict": each change in the government-set retail price
of Premium or Solar comes from its regulation or an official notice stored in sources/ with a quote.
docs/fuel-manifest.csv lists one row per change and product: the stored file, its SHA-256 and exact
passages from it (quote, quote2). Where that document does not print the price in force before,
old_source_file and old_quote give it from the earlier regulation or notice. For each row this script
checks every file's SHA-256, extracts its text (pdftotext -layout for PDF; for HTML, tags stripped with
the standard library's parser, which also unescapes entities), normalises whitespace, asserts each
passage occurs exactly once, checks that the only date quote and quote2 print is the effective date,
reads the prices in rupiah per litre from the passages and checks the direction. Run from the post
folder; needs poppler's pdftotext. The analysis reads the CSV, never the documents.

Reading prices. A passage containing "Rp" gives the amounts written after it ("Rp 4.500,00", "Rp. 7600",
"Rp6,400"); a passage without "Rp" gives the amounts with a thousands separator, as in a "Harga Lama,
Harga Baru" table row ("6.400 6.900"). quote and quote2 together give two amounts, the old and the new
price in that order, or one, the new price, and then old_quote gives the old price: its only amount, or,
for a table row, the figure at position old_column among its numbers of four or more digits. Prices must
lie in PRICE_RANGE and match the direction.

A row whose status is "size not verified" gets no prices in the CSV. Its direction must come either from
an old and a new price read from stored passages as above (when it gives old_source_file and old_quote),
or otherwise from a naik or turun word (or their forms) in its passages. Its region_note must say that
the prices it shows are the government-set price outside Java-Madura-Bali or carry no region, and that
the Java price is not verified. Each verified change's old price must equal the new price of the same
product's previous change when that one is verified too: a mismatch means a missing change or a wrong
price. Percentages are rounded with Python's round(), as the gate's formatters round.
"""
import csv
import hashlib
import re
import subprocess
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

MANIFEST = Path("docs/fuel-manifest.csv")
SOURCES = Path("sources/fuel")
OUT = Path("data/fuel_price_changes.csv")
OUT_COLUMNS = ["date", "product", "direction", "old_price", "new_price", "pct_change", "instrument", "source_file",
               "status", "region_note"]
PRODUCTS, DIRECTIONS = ("Premium", "Solar"), ("rise", "cut")
VERIFIED, NOT_VERIFIED = "verified", "size not verified"
MAX_WORDS = 40
PRICE_RANGE = (1_000, 15_000)  # rupiah per litre; every price here lies in 1,650 to 8,500
MAX_ABS_PCT = 150
MONTHS = [["Januari"], ["Februari", "Pebruari"], ["Maret"], ["April"], ["Mei"], ["Juni"], ["Juli"], ["Agustus"],
          ["September"], ["Oktober"], ["November", "Nopember"], ["Desember"]]
MONTH_NUMBER = {name.lower(): i for i, names in enumerate(MONTHS, 1) for name in names}
DATE_PRINTED = re.compile(rf"(?<!\d)(\d{{1,2}}) ({'|'.join(MONTH_NUMBER)}) (\d{{4}})(?!\d)", re.IGNORECASE)
DIRECTION_WORDS = {"rise": re.compile(r"\b(?:naik|kenaikan|dinaikkan|menaikkan)\b", re.IGNORECASE),
                   "cut": re.compile(r"\b(?:turun|penurunan|menurunkan|diturunkan)\b", re.IGNORECASE)}
JAVA_NOT_VERIFIED = "the java price is not verified"
REGION_STATED = ("outside java-madura-bali", "no region")
RP_AMOUNT = re.compile(r"Rp\.?\s*(\d{1,3}(?:[.,]\d{3})+|\d+)(?:,00|,-)?(?![.,]?\d)")
TABLE_AMOUNT = re.compile(r"(?<![\d.,])\d{1,3}(?:[.,]\d{3})+(?!\d)")
COLUMN_FIGURE = re.compile(r"\d{1,3}(?:[.,]\d{3})+|\d{4,}")


class _Text(HTMLParser):
    """Collects the text of an HTML page, dropping script and style, with a space at every tag."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        self.parts.append(" ")

    def handle_endtag(self, tag) -> None:
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        self.parts.append(" ")

    def handle_data(self, data) -> None:
        if not self.skip:
            self.parts.append(data)


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def document_text(rel: str, sha: str, cache: dict[str, tuple[str, str]]) -> str:
    """Text of a stored document; every call checks the manifest's SHA-256 against the file's."""
    path = Path(rel)
    if path.parent != SOURCES:
        raise SystemExit(f"{rel}: not a file directly under {SOURCES}/")
    if rel not in cache:
        raw = path.read_bytes()
        if raw[:5] == b"%PDF-":
            text = subprocess.run(["pdftotext", "-layout", str(path), "-"], check=True, capture_output=True,
                                  text=True).stdout
        else:
            parser = _Text()
            parser.feed(raw.decode("utf-8"))
            parser.close()
            text = "".join(parser.parts)
        cache[rel] = (hashlib.sha256(raw).hexdigest(), normalise(text))
    actual, text = cache[rel]
    if actual != sha:
        raise SystemExit(f"{rel} does not match its SHA-256 in {MANIFEST}")
    return text


def assert_once(text: str, passage: str, rel: str) -> None:
    words = len(passage.split())
    if words >= MAX_WORDS:
        raise SystemExit(f"{rel}: passage has {words} words, limit is under {MAX_WORDS}: {passage!r}")
    count = text.count(normalise(passage))
    if count != 1:
        raise SystemExit(f"{rel}: passage found {count} times, expected exactly once: {passage!r}")


def amounts(passage: str) -> list[int]:
    found = RP_AMOUNT.findall(passage) if "Rp" in passage else TABLE_AMOUNT.findall(passage)
    return [int(re.sub(r"[.,]", "", a)) for a in found]


def column_figure(passage: str, column: int) -> int:
    figures = [t for t in passage.split() if COLUMN_FIGURE.fullmatch(t)]
    if not 1 <= column <= len(figures):
        raise SystemExit(f"old_column {column} is outside the {len(figures)} figures in {passage!r}")
    return int(re.sub(r"[.,]", "", figures[column - 1]))


def assert_date_printed(day: date, passages: list[str], label: str) -> None:
    printed = {date(int(y), MONTH_NUMBER[m.lower()], int(d)) for p in passages for d, m, y in DATE_PRINTED.findall(p)}
    if printed != {day}:
        raise SystemExit(f"{label}: the passages print {sorted(map(str, printed))}; expected only {day}")


def assert_direction_named(direction: str, passages: list[str], label: str) -> None:
    other = "cut" if direction == "rise" else "rise"
    joined = " ".join(passages)
    if not DIRECTION_WORDS[direction].search(joined) or DIRECTION_WORDS[other].search(joined):
        raise SystemExit(f"{label}: the passages must name a {direction} and only a {direction}")


def prices(row: dict, cache: dict[str, tuple[str, str]], label: str) -> tuple[int, int]:
    found = amounts(row["quote"]) + amounts(row["quote2"])
    if not row["old_quote"]:
        if len(found) != 2:
            raise SystemExit(f"{label}: expected old and new price in quote and quote2, found {found}")
        return found[0], found[1]
    if len(found) != 1:
        raise SystemExit(f"{label}: expected only the new price in quote and quote2, found {found}")
    old_text = document_text(row["old_source_file"], row["old_source_sha256"], cache)
    assert_once(old_text, row["old_quote"], row["old_source_file"])
    if row["old_column"]:
        return column_figure(row["old_quote"], int(row["old_column"])), found[0]
    old = amounts(row["old_quote"])
    if len(old) != 1:
        raise SystemExit(f"{label}: expected one amount in old_quote, found {old}")
    return old[0], found[0]


def sized(row: dict, cache: dict[str, tuple[str, str]], label: str) -> tuple[int, int]:
    """Old and new price from the stored passages, checked against PRICE_RANGE and the direction."""
    old, new = prices(row, cache, label)
    if not all(PRICE_RANGE[0] <= p <= PRICE_RANGE[1] for p in (old, new)):
        raise SystemExit(f"{label}: prices {old} and {new} are outside {PRICE_RANGE} rupiah per litre")
    if (new > old) != (row["direction"] == "rise") or new == old:
        raise SystemExit(f"{label}: prices {old} to {new} do not match direction {row['direction']!r}")
    return old, new


def assert_unverified_note(note: str, label: str) -> None:
    lowered = note.lower()
    if JAVA_NOT_VERIFIED not in lowered or not any(m in lowered for m in REGION_STATED):
        raise SystemExit(f"{label}: region_note must say {JAVA_NOT_VERIFIED!r} and one of {REGION_STATED}")


def check_row(row: dict, cache: dict[str, tuple[str, str]]) -> dict:
    label = f"{row['date']} {row['product']}"
    day = date.fromisoformat(row["date"])
    if row["product"] not in PRODUCTS or row["direction"] not in DIRECTIONS:
        raise SystemExit(f"{label}: unknown product or direction {row['product']!r} {row['direction']!r}")
    if row["status"] not in (VERIFIED, NOT_VERIFIED) or not row["quote"]:
        raise SystemExit(f"{label}: unknown status {row['status']!r} or empty quote")
    old_fields = [bool(row[k]) for k in ("old_source_file", "old_source_sha256", "old_quote")]
    if any(old_fields) != all(old_fields) or (row["old_column"] and not row["old_quote"]):
        raise SystemExit(f"{label}: old_source_file, old_source_sha256 and old_quote go together; "
                         "old_column needs them")
    text = document_text(row["source_file"], row["source_sha256"], cache)
    passages = [q for q in (row["quote"], row["quote2"]) if q]
    for passage in passages:
        assert_once(text, passage, row["source_file"])
    assert_date_printed(day, passages, label)
    out = {k: row[k] for k in ("date", "product", "direction", "instrument", "source_file", "status", "region_note")}
    if row["status"] == NOT_VERIFIED:
        assert_unverified_note(row["region_note"], label)
        if any(old_fields):
            sized(row, cache, label)  # direction from the stored old and new prices; no size is printed
        else:
            assert_direction_named(row["direction"], passages, label)
        return {**out, "old_price": "", "new_price": "", "pct_change": ""}
    old, new = sized(row, cache, label)
    pct = (new - old) / old * 100
    if abs(pct) > MAX_ABS_PCT:
        raise SystemExit(f"{label}: a change of {pct:.1f}% is beyond {MAX_ABS_PCT}%")
    return {**out, "old_price": old, "new_price": new, "pct_change": f"{round(pct, 1):.1f}"}


def assert_chain(results: list[dict]) -> None:
    for product in PRODUCTS:
        rows = [r for r in results if r["product"] == product]
        for prev, cur in zip(rows, rows[1:]):
            if prev["status"] == cur["status"] == VERIFIED and prev["new_price"] != cur["old_price"]:
                raise SystemExit(f"{cur['date']} {product}: old price {cur['old_price']} is not the new price "
                                 f"{prev['new_price']} set on {prev['date']} (a missing change or a wrong price)")


def main() -> None:
    with MANIFEST.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    keys = [(r["date"], r["product"]) for r in rows]
    if len(set(keys)) != len(keys):
        raise SystemExit(f"{MANIFEST}: duplicate date and product rows")
    cache: dict[str, tuple[str, str]] = {}
    results = sorted((check_row(r, cache) for r in rows), key=lambda r: (r["date"], r["product"]))
    assert_chain(results)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_COLUMNS)
        w.writeheader()
        w.writerows(results)
    for r in results:
        size = f"{r['old_price']} -> {r['new_price']} ({r['pct_change']}%)" if r["old_price"] else "size not verified"
        print(f"{r['date']} {r['product']:<7} {r['direction']:<4} {size}")
    verified = sum(r["status"] == VERIFIED for r in results)
    print(f"wrote {OUT}: {len(results)} rows ({verified} verified, {len(results) - verified} size not verified) "
          f"from {len(cache)} documents")


if __name__ == "__main__":
    main()
