"""Mutation checks for extract_jht.py: each corruption of docs/jht-manifest.csv must make the extractor fail.

The unchanged manifest must pass; then a changed value, a changed quote, a changed hash, a duplicated year, a
missing year and two credited rows with their quotes and values swapped (and a few neighbours of those, plus a
manifest line broken by an unquoted comma) must each raise SystemExit with the matching reason. Run from
the post folder with python3 -m unittest test_extract_jht, or from anywhere with python3 -m unittest discover -s
<post folder> -p test_extract_jht.py; the tests move to the post folder, where the extractor's relative paths
point. Needs the stored documents in sources/jht/ and poppler's pdftotext.
"""
import os
import tempfile
import unittest
from pathlib import Path

import extract_jht as ex

POST = Path(__file__).resolve().parent


def setUpModule() -> None:
    os.chdir(POST)


class ManifestMutations(unittest.TestCase):
    rows: list[dict]
    docs: ex.Documents

    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = ex.read_manifest(ex.MANIFEST)
        cls.docs = ex.Documents()  # shared page and hash cache; it stores what the files hold, never the manifest

    def copy_rows(self) -> list[dict]:
        return [dict(r) for r in self.rows]

    @staticmethod
    def find(rows: list[dict], year: int, kind: str) -> dict:
        return next(r for r in rows if int(r["year"]) == year and r["kind"] == kind)

    def assert_fails(self, rows: list[dict], reason: str) -> None:
        with self.assertRaisesRegex(SystemExit, reason):
            ex.build(rows, self.docs)

    def test_unchanged_manifest_passes(self) -> None:
        out = ex.build(self.copy_rows(), self.docs)
        credited = sorted(int(r["year"]) for r in out if r["kind"] in ex.CREDITED_KINDS)
        self.assertEqual(credited, list(ex.CREDITED_YEARS))
        self.assertEqual(len(out), len(self.rows))

    def test_changed_value_fails(self) -> None:
        rows = self.copy_rows()
        row = self.find(rows, 2010, "base")
        row["value_pct"] = "10.70"
        self.assert_fails(rows, "the quote prints")

    def test_changed_value_on_the_html_release_fails(self) -> None:
        rows = self.copy_rows()
        self.find(rows, 2015, "yearend_reported")["value_pct"] = "6.98"
        self.assert_fails(rows, "the quote prints")

    def test_changed_quote_wording_fails(self) -> None:
        rows = self.copy_rows()
        row = self.find(rows, 2006, "base")
        row["quote"] = row["quote"].replace("saldo awal", "saldo akhir")
        self.assert_fails(rows, "found 0 times")

    def test_changed_quote_and_value_together_fail(self) -> None:
        rows = self.copy_rows()
        row = self.find(rows, 2014, "base")
        row["quote"] = row["quote"].replace("10,55%", "10,65%")
        row["value_pct"] = "10.65"
        self.assert_fails(rows, "found 0 times")

    def test_swapped_2005_and_2006_quotes_and_values_fail(self) -> None:
        # Both quotes sit on the same page of the same report, so only the year check can catch the swap.
        rows = self.copy_rows()
        a, b = self.find(rows, 2005, "base"), self.find(rows, 2006, "base")
        a["quote"], b["quote"] = b["quote"], a["quote"]
        a["value_pct"], b["value_pct"] = b["value_pct"], a["value_pct"]
        self.assert_fails(rows, "prints the year 2006, not the row's year 2005")

    def test_quote_cut_inside_a_word_fails(self) -> None:
        rows = self.copy_rows()
        row = self.find(rows, 2006, "base")
        row["quote"] = row["quote"][1:]
        self.assert_fails(rows, "whole words")

    def test_quote_found_twice_on_its_page_fails(self) -> None:
        rows = self.copy_rows()
        march = next(r for r in rows if r["kind"] == "oneoff" and "6,50%" in r["quote"])
        march["quote"] = "kepada seluruh peserta yang belum mengambil JHT"
        self.assert_fails(rows, "found 2 times")

    def test_changed_hash_fails(self) -> None:
        rows = self.copy_rows()
        row = self.find(rows, 2013, "base")
        row["sha256"] = row["sha256"][:-1] + ("0" if row["sha256"][-1] != "0" else "1")
        self.assert_fails(rows, "does not match")

    def test_duplicated_base_year_fails(self) -> None:
        rows = self.copy_rows()
        rows.append(dict(self.find(rows, 2012, "base")))
        self.assert_fails(rows, "2012 has 2 base or yearend_reported rows")

    def test_base_beside_yearend_reported_fails(self) -> None:
        rows = self.copy_rows()
        extra = dict(self.find(rows, 2020, "base"))  # its quote prints no year, so only the coverage check applies
        extra["year"] = "2015"
        rows.append(extra)
        self.assert_fails(rows, "2015 has 2 base or yearend_reported rows")

    def test_duplicated_yield_year_fails(self) -> None:
        rows = self.copy_rows()
        rows.append(dict(self.find(rows, 2019, "yield")))
        self.assert_fails(rows, "2019 has 2 yield rows")

    def test_missing_base_year_fails(self) -> None:
        rows = [r for r in self.copy_rows() if not (r["year"] == "2012" and r["kind"] == "base")]
        self.assert_fails(rows, r"no base or yearend_reported row for \[2012\]")

    def test_missing_yearend_reported_year_fails(self) -> None:
        rows = [r for r in self.copy_rows() if r["kind"] != "yearend_reported"]
        self.assert_fails(rows, r"no base or yearend_reported row for \[2015\]")

    def test_base_row_after_2020_fails(self) -> None:
        rows = self.copy_rows()
        extra = dict(self.find(rows, 2020, "base"))
        extra["year"] = "2021"
        rows.append(extra)
        self.assert_fails(rows, "outside 2005 to 2020")

    def test_missing_bonus_fails(self) -> None:
        rows = [r for r in self.copy_rows() if not (r["year"] == "2009" and r["kind"] == "incentive")]
        self.assert_fails(rows, "R3")

    def test_unquoted_comma_in_the_manifest_file_fails(self) -> None:
        text = ex.MANIFEST.read_text(encoding="utf-8")
        quoted = '"penerimaan iuran JHT tahun 2011 adalah 10,10%"'
        self.assertEqual(text.count(quoted), 1)
        with tempfile.TemporaryDirectory() as tmp:
            broken = Path(tmp) / "jht-manifest.csv"
            broken.write_text(text.replace(quoted, quoted.strip('"')), encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "expected 9 fields"):
                ex.read_manifest(broken)


if __name__ == "__main__":
    unittest.main()
