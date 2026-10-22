"""External figures must come from a stored, hash-pinned copy of the cited document, quoted verbatim.

Each failure mode is one that shipped or was caught late: a figure from a working paper cited as the
published article (Post 25), a press release standing in for the report it summarises (Post 23), and
a figure added to an allowlist with an invented citation (the audit's attack on the previous gate).
"""

import copy
import hashlib
import os
import tempfile
import unittest

from gate.checks import cite, sources
from gate.render import render

ARTICLE = ("Temperature Shocks and Economic Growth: Evidence from the Last Half Century\n"
           "By Melissa Dell, Benjamin F. Jones, and Benjamin A. Olken\n... we find that a 1C rise in "
           "temperature in a given year reduced economic growth in that year by about 1.3 percentage\n"
           "points. In rich countries, changes in temperature do not have a robust, discern-\nable effect.")
DRAFT = ("Dell et al. (2012) find growth fell by {{src:dell2012.values.growth_pp:dec1}} points.\n\n"
         "## References\n\nDell, M., Jones, B. F., & Olken, B. A. (2012). Temperature shocks and economic "
         "growth: Evidence from the last half century. *AEJ: Macro, 4*(3), 66-95.\n")


class SourcesTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, self.root, True)
        os.makedirs(os.path.join(self.root, "sources"))
        self.write_doc(ARTICLE)
        self.src = {"dell2012": {
            "ref": "Dell 2012", "title": "Temperature shocks and economic growth",
            "doc": "sources/dell2012.txt", "sha256": hashlib.sha256(ARTICLE.encode()).hexdigest(),
            "page": "67", "quote": "reduced economic growth in that year by about 1.3 percentage points",
            "values": {"growth_pp": 1.3}}}

    def write_doc(self, text):
        with open(os.path.join(self.root, "sources", "dell2012.txt"), "w") as f:
            f.write(text)

    def fails(self, src=None, draft=DRAFT):
        src = self.src if src is None else src
        rendered, b = render(draft, {}, src)
        return sources.check(draft, rendered, b, src, self.root)

    def mutate(self, **kw):
        s = copy.deepcopy(self.src)
        s["dell2012"].update(kw)
        return s

    def test_clean(self):
        self.assertEqual(self.fails(), [])

    def test_quote_spanning_a_hyphenated_line_break_still_matches(self):
        self.assertEqual(self.fails(self.mutate(
            quote="by about 1.3 percentage points. In rich countries, changes in temperature do not have a robust, discernable effect")), [])

    def test_missing_document_fails(self):
        os.remove(os.path.join(self.root, "sources", "dell2012.txt"))
        self.assertTrue(any("fetch" in x for x in self.fails()))

    def test_changed_document_fails_the_hash(self):
        self.write_doc(ARTICLE + " edited")
        self.assertTrue(any("sha256" in x for x in self.fails()))

    def test_quote_not_in_document_fails(self):
        self.assertTrue(self.fails(self.mutate(quote="reduced growth by about 1.1 percentage points")))

    def test_value_not_in_quote_fails(self):
        # the round-3 defect: 1.1 is from the 2008 working paper, not this article
        s = self.mutate()
        s["dell2012"]["values"] = {"growth_pp": 1.1}
        self.assertTrue(any("1.1" in x for x in self.fails(s)))

    def test_wrong_document_fails_the_title_check(self):
        # a press release or working paper with a different title, stored in place of the article
        wp = "Climate Change and Economic Growth\nNBER Working Paper 14132\n" + ARTICLE.split("\n", 2)[2]
        self.write_doc(wp)
        s = self.mutate(sha256=hashlib.sha256(wp.encode()).hexdigest())
        self.assertTrue(any("title" in x for x in self.fails(s)))

    def test_title_only_in_a_running_header_deep_in_the_text_fails(self):
        # the first version searched 4,000 characters, and a swapped-in working paper passed because the
        # article's running page header repeats the title on page two
        wp = "Climate Change and Economic Growth\nNBER Working Paper 14132\n" + "filler text " * 80 + ARTICLE
        self.write_doc(wp)
        s = self.mutate(sha256=hashlib.sha256(wp.encode()).hexdigest())
        self.assertTrue(any("title" in x for x in self.fails(s)))

    def test_dropped_sign_fails(self):
        # attack: coef 0.38 against a quote reading -0.38 passed because the check compared abs()
        doc = ARTICLE + " The coefficient was -0.38 in the base sample."
        self.write_doc(doc)
        s = self.mutate(sha256=hashlib.sha256(doc.encode()).hexdigest(), quote="The coefficient was -0.38")
        s["dell2012"]["values"] = {"coef": 0.38}
        self.assertTrue(any("0.38" in x for x in self.fails(s, draft=DRAFT.replace("growth_pp", "coef"))))

    def test_hand_rounded_value_fails(self):
        # attack: 0.3 passed against '0.34' because the check used substring containment
        s = self.mutate(quote="by about 1.3 percentage points")
        s["dell2012"]["values"] = {"growth_pp": 1.0}
        self.assertTrue(self.fails(s))

    def test_one_number_per_value(self):
        # attack: a whole table row as the quote let a figure from the wrong column pass
        doc = ARTICLE + " R2 0.34 0.55 0.27"
        self.write_doc(doc)
        s = self.mutate(sha256=hashlib.sha256(doc.encode()).hexdigest(), quote="R2 0.34 0.55 0.27")
        s["dell2012"]["values"] = {"growth_pp": 0.55}
        self.assertTrue(any("number" in x for x in self.fails(s)))

    def test_malformed_entry_is_reported_not_a_crash(self):
        s = self.mutate(ref="Dell")                    # no year
        self.assertTrue(any("ref" in x for x in self.fails(s)))

    def test_reference_entry_missing_fails(self):
        draft = DRAFT.split("## References")[0] + "## References\n\nOther, A. (2001). Something.\n"
        self.assertTrue(any("reference" in x for x in self.fails(draft=draft)))

    def test_declared_alias_counts_as_a_citation(self):
        s = self.mutate(aliases=["DJO"])
        draft = DRAFT.replace("Dell et al. (2012) find", "DJO find")
        self.assertEqual(self.fails(s, draft=draft), [])

    def test_paragraph_using_the_figure_must_cite_it(self):
        draft = DRAFT.replace("Dell et al. (2012) find", "Economists find")
        self.assertTrue(any("cite" in x for x in self.fails(draft=draft)))


if __name__ == "__main__":
    unittest.main()


class ReviewV2Test(unittest.TestCase):
    """Review of v2: each of these passed."""
    setUp, write_doc, fails, mutate = SourcesTest.setUp, SourcesTest.write_doc, SourcesTest.fails, SourcesTest.mutate

    def test_quote_cut_inside_a_number_fails(self):
        doc = ARTICLE.replace("by about 1.3 percentage", "by about 11.38 percentage")
        self.write_doc(doc)
        s = self.mutate(sha256=hashlib.sha256(doc.encode()).hexdigest(),
                        quote="reduced economic growth in that year by about 11.3")
        s["dell2012"]["values"] = {"growth_pp": 11.3}
        self.assertTrue(any("inside a number" in x for x in self.fails(s)), self.fails(s))

    def test_quote_that_drops_a_sign_fails(self):
        doc = ARTICLE + "\nTable 2: coefficient -0.38 in the base sample."
        self.write_doc(doc)
        s = self.mutate(sha256=hashlib.sha256(doc.encode()).hexdigest(), quote="0.38 in the base sample")
        s["dell2012"]["values"] = {"growth_pp": 0.38}
        self.assertTrue(any("inside a number" in x for x in self.fails(s)), self.fails(s))

    def test_paragraph_citing_another_year_fails(self):
        # the year sat inside the placeholder key 'dell2012', so any paragraph naming Dell passed
        draft = DRAFT.replace("Dell et al. (2012) find", "Dell et al. (2008) find")
        self.assertTrue(any("does not cite" in x for x in self.fails(draft=draft)))

    def test_title_must_be_the_reference_title_not_a_phrase_from_it(self):
        self.assertTrue(any("title" in x for x in self.fails(self.mutate(title="economic growth"))))
        full = "Temperature shocks and economic growth: Evidence from the last half century"
        self.assertEqual([x for x in self.fails(self.mutate(title=full)) if "reference entry" in x], [])

    def test_titles_are_read_from_every_apa_entry_shape(self):
        # review of v3: the title was always read up to the first '*'
        from gate.checks.sources import _entry_titles
        chapter = ("Acemoglu, D., Johnson, S., & Robinson, J. A. (2005). Institutions as a fundamental cause of "
                   "long-run growth. In P. Aghion & S. N. Durlauf (Eds.), *Handbook of economic growth* (pp. 385-472).")
        self.assertIn("institutions as a fundamental cause of long-run growth", _entry_titles(chapter))
        book = "McEvedy, C., & Jones, R. (1978). *Atlas of world population history*. Facts on File."
        self.assertIn("atlas of world population history", _entry_titles(book))
        under = "McEvedy, C., & Jones, R. (1978). _Atlas of world population history_. Facts on File."
        self.assertIn("atlas of world population history", _entry_titles(under))
        italic_term = "Smith, A. (2020). Biting rates of *Aedes aegypti* in cities: A review. *J. Ent., 4*(1), 1-9."
        self.assertIn("biting rates of aedes aegypti in cities", _entry_titles(italic_term))

    def test_a_quote_must_locate_one_place(self):
        # a sign-dropped '0.38' borrowed a clean occurrence from another cell of the same paper
        doc = ARTICLE + "\nTable 2: coefficient -0.38 in the base sample; elsewhere 0.38 in another column."
        self.write_doc(doc)
        s = self.mutate(sha256=hashlib.sha256(doc.encode()).hexdigest(), quote="0.38")
        s["dell2012"]["values"] = {"growth_pp": 0.38}
        self.assertTrue(any("occurs 2 times" in x for x in self.fails(s)), self.fails(s))


PP46 = ("Iuran Jaminan Hari Tua\nIuran JHT bagi Peserta penerima Upah sebesar 5,7% (lima koma tujuh persen) dari "
        "Upah, dengan ketentuan: a. 2% (dua persen) ditanggung oleh Pekerja; dan b. 3,7% (tiga koma tujuh persen) "
        "ditanggung oleh Pemberi Kerja. Peserta program JHT sebanyak 19.100.050 orang.")
PP46_QUOTE = ("sebesar 5,7% (lima koma tujuh persen) dari Upah, dengan ketentuan: a. 2% (dua persen) ditanggung oleh "
              "Pekerja; dan b. 3,7% (tiga koma tujuh persen)")
IRS = ("Retirement topics\nThe limit on employee elective deferrals is: $24,500 in 2026. Generally, early "
       "distributions are those you receive before reaching age 59½ and are taxed.")
SIM = "Pengembangan Saldo JHT\nBesarnya pengembangan 5% per tahun dari saldo."


class NumberFormatAndUndatedTest(unittest.TestCase):
    """Post 28 (jht-401k): Indonesian sources print '5,7%' and '19.100.050', the IRS prints '$24,500' and
    'age 59½', and a BPJS web page carries no date. Each value of those quotes failed (or the wrong one passed:
    19.1 from '19.100.050', 59 from '59½'), and a 'Surname n.d.' ref was refused outright."""

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, self.root, True)
        os.makedirs(os.path.join(self.root, "sources"))

    def fails(self, doc, quote, values, fmt=None, ref="Agency 2015", title="Iuran jaminan hari tua", citing=None):
        """(sources failures, rendered draft) for one entry used once, in a sentence that ends with `citing`
        (default '(Surname, Year)'), over a reference list holding only that entry."""
        with open(os.path.join(self.root, "sources", "doc.txt"), "w", encoding="utf-8") as f:
            f.write(doc)
        entry = {"ref": ref, "title": title, "doc": "sources/doc.txt", "quote": quote, "values": values,
                 "sha256": hashlib.sha256(doc.encode("utf-8")).hexdigest()}
        if fmt is not None:
            entry["number_format"] = fmt
        surname, year = ref.rsplit(" ", 1)
        leaf = next(iter(values))
        draft = (f"The figure is {{{{src:k.values.{leaf}:dec1}}}}, {citing or '(' + surname + ', ' + year + ')'}.\n\n"
                 f"## References\n\n{surname}. ({year}). {title[0].upper() + title[1:]}. Publisher.\n")
        rendered, b = render(draft, {}, {"k": entry})
        return sources.check(draft, rendered, b, {"k": entry}, self.root), rendered

    def test_indonesian_quote_reads_comma_decimals(self):
        f, _ = self.fails(PP46, PP46_QUOTE, {"total": 5.7, "worker": 2, "employer": 3.7}, fmt="id")
        self.assertEqual(f, [])

    def test_indonesian_quote_reads_dot_thousands(self):
        f, _ = self.fails(PP46, "Peserta program JHT sebanyak 19.100.050 orang", {"members": 19100050}, fmt="id")
        self.assertEqual(f, [])

    def test_a_piece_of_an_indonesian_number_is_not_its_value(self):
        # before: the English reader took 19.1 from '19.100.050', so a value of 19.1 passed
        f, _ = self.fails(PP46, "Peserta program JHT sebanyak 19.100.050 orang", {"members": 19.1}, fmt="id")
        self.assertTrue(any("19.1" in x for x in f), f)
        f, _ = self.fails(PP46, "sebesar 5,7% (lima", {"total": 5}, fmt="id")
        self.assertTrue(any("is not a number in its quote" in x for x in f), f)

    def test_an_indonesian_quote_read_as_english_fails(self):
        f, _ = self.fails(PP46, PP46_QUOTE, {"total": 5.7, "worker": 2, "employer": 3.7})
        self.assertTrue(f)

    def test_a_number_joined_to_letters_is_not_read(self):
        # 'Rp19.100.050' read from its second group gave 100050 and 19.1-style fragments in "id"
        self.assertEqual(sources._quote_numbers("sebesar Rp19.100.050 orang", "id"), [])
        self.assertEqual(sources._quote_numbers("ERA5 grid", "en"), [])

    def test_indonesian_thousands_and_decimal_together(self):
        self.assertEqual(sources._quote_numbers("naik 1.234,5 persen", "id"), [1234.5])

    def test_an_unknown_number_format_is_reported(self):
        f, _ = self.fails(PP46, "sebesar 5,7% (lima", {"total": 5.7}, fmt="de")
        self.assertTrue(any("number_format" in x for x in f), f)

    def test_english_quote_reads_comma_thousands(self):
        quote = "is: $24,500 in 2026"
        for fmt in (None, "en"):
            with self.subTest(fmt=fmt):
                f, _ = self.fails(IRS, quote, {"limit": 24500, "year": 2026}, fmt=fmt, title="Retirement topics")
                self.assertEqual(f, [])

    def test_the_groups_of_an_english_number_are_not_numbers(self):
        # before: '$24,500' was read as 24 and 500, so three values 24, 500 and 2026 passed
        f, _ = self.fails(IRS, "is: $24,500 in 2026", {"a": 24, "b": 500, "year": 2026}, title="Retirement topics")
        self.assertTrue(any("values.a = 24 is not a number" in x for x in f), f)
        self.assertTrue(any("values.b = 500 is not a number" in x for x in f), f)

    def test_a_half_attached_to_a_number_is_read(self):
        f, _ = self.fails(IRS, "before reaching age 59½", {"age": 59.5}, title="Retirement topics")
        self.assertEqual(f, [])

    def test_the_whole_part_of_a_half_is_not_the_value(self):
        # before: '59½' was read as 59, so a value of 59 passed
        f, _ = self.fails(IRS, "before reaching age 59½", {"age": 59}, title="Retirement topics")
        self.assertTrue(any("values.age = 59 is not a number" in x for x in f), f)

    def test_an_undated_reference_splits_matches_and_is_cited(self):
        kw = dict(fmt="id", ref="BPJS Ketenagakerjaan n.d.", title="Pengembangan saldo JHT")
        for citing in (None, "as BPJS Ketenagakerjaan (n.d.) assumes"):
            with self.subTest(citing=citing):
                f, rendered = self.fails(SIM, "Besarnya pengembangan 5% per tahun", {"r": 5}, citing=citing, **kw)
                self.assertIn("(BPJS Ketenagakerjaan, n.d.)." if citing is None else "Ketenagakerjaan (n.d.) assumes",
                              rendered)
                self.assertIn("BPJS Ketenagakerjaan. (n.d.). Pengembangan saldo JHT.", rendered)
                self.assertEqual(f, [])
                self.assertEqual(cite.check(rendered), [])

    def test_an_undated_reference_still_needs_its_citation(self):
        f, _ = self.fails(SIM, "Besarnya pengembangan 5% per tahun", {"r": 5}, fmt="id",
                          ref="BPJS Ketenagakerjaan n.d.", title="Pengembangan saldo JHT",
                          citing="(BPJS Ketenagakerjaan, 2025)")
        self.assertTrue(any("does not cite BPJS Ketenagakerjaan (n.d.)" in x for x in f), f)
