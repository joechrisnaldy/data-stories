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

from gate.checks import sources
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
