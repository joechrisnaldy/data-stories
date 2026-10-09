"""claims: universals and causal words need a register entry. cite: both directions. style, links."""

import os
import tempfile
import unittest
import zipfile

from gate.checks import cite, claims, links, style


class ClaimsTest(unittest.TestCase):
    def test_universal_without_entry_fails(self):
        self.assertTrue(claims.check("Every hot country is poor.", {}))

    def test_causal_without_entry_fails(self):
        self.assertTrue(claims.check("Heat causes poverty.", {}))
        self.assertTrue(claims.check("The split explains the sign.", {}))

    def test_registered_sentence_passes(self):
        reg = {"cannot have inverted the ranking": "licensed by interaction.t on the full 163"}
        self.assertEqual(claims.check("It cannot have inverted the ranking unless its effect changed. Everything else is fine.",
                                      {**reg, "Everything else is fine": "rhetorical, no data claim"}), [])

    def test_unflagged_text_passes(self):
        self.assertEqual(claims.check("Hot countries tend to be poorer.", {}), [])

    def test_word_boundaries(self):
        # 'allocation' contains 'all', 'because' must not match 'becausee'
        self.assertEqual(claims.check("The allocation was fair.", {}), [])

    def test_sentences_never_span_a_heading(self):
        f = claims.check("A plain sentence.\n\n## Nothing here is a heading claim\n\nAnother plain one.", {})
        self.assertTrue(all("A plain sentence" not in x for x in f))

    def test_the_idiom_at_all_is_exempt_and_a_group_label_is_registered_once(self):
        # review of v2: hyphenated compounds were exempt wholesale, which also let 'worst-hit' and
        # 'best-known' through. A group label is now one register entry naming it.
        s = "The never-colonised group differs, which is why it is here at all."
        self.assertTrue(claims.check(s, {}))
        self.assertEqual(claims.check(s, {"never-colonised": "group name: the countries absent from AJR's list"}), [])

    def test_at_all_before_a_noun_is_a_universal(self):
        self.assertTrue(claims.check("The relationship holds at all latitudes and at all income levels.", {}))

    def test_any_superlative_is_a_claim(self):
        for sentence in ("The hottest countries are the poorest.", "This is the clearest casualty.",
                         "It is the easiest thing to measure.", "The worst-hit countries are the best-known cases."):
            with self.subTest(sentence=sentence):
                self.assertTrue(claims.check(sentence, {}))
        self.assertEqual(claims.check("An honest interest in modest forest tests.", {}), [])

    def test_still_more_universal_and_causal_words(self):
        for sentence in ("Heat can lead to poverty.", "The data prove it.", "Temperature accounts for the gap.",
                         "Colonisation is the main driver.", "It is driving the result.", "Heat can't be it.",
                         "No country escaped the reversal."):
            with self.subTest(sentence=sentence):
                self.assertTrue(claims.check(sentence, {}))

    def test_a_short_phrase_licenses_only_a_whole_sentence(self):
        # review of v2: a one-word entry "because" licensed every 'because' in the post, later fixes included
        self.assertTrue(claims.check("Heat is poor because it is hot.", {"because": "too short"}))
        self.assertEqual(claims.check("Nothing. A flat cloud.", {"Nothing.": "the pooled r of 0.04"}), [])

    def test_only_the_idiom_at_all_is_exempt(self):
        # the first version exempted every token after 'at', silencing 'at only' and 'at every'
        self.assertTrue(claims.check("They correlate at only 0.58 with ERA5.", {}))
        self.assertTrue(claims.check("It holds at every level.", {}))

    def test_a_licence_covers_only_the_words_inside_its_phrase(self):
        # attack: a causal clause added to an already-registered sentence inherited the sentence's licence
        reg = {"the thermometer cannot be the whole of it": "tidy_story.r2_share"}
        ok = "We know the thermometer cannot be the whole of it."
        bad = "We know the thermometer cannot be the whole of it, because colonisation caused the gap."
        self.assertEqual(claims.check(ok, reg), [])
        f = claims.check(bad, reg)
        self.assertTrue(any("because" in x or "caused" in x for x in f), f)

    def test_more_universal_and_causal_words(self):
        for sentence in ("This proves the point.", "Therefore heat matters.", "It is the most famous case.",
                         "Colonisation produced the gap.", "Not a single country escaped."):
            self.assertTrue(claims.check(sentence, {}), sentence)

    def test_register_phrases_need_word_boundaries(self):
        f = claims.check("Everything changed.", {"thing changed": "too short to be a licence"})
        self.assertTrue(f)

    def test_chart_strings_are_checked_too(self):
        self.assertTrue(claims.check("Clean prose.", {}, extra=["Nothing after it disputes the claim"]))

    def test_stale_register_entry_fails(self):
        f = claims.check("Clean prose.", {"never happens": "old"})
        self.assertTrue(any("licenses nothing" in x for x in f))

    def test_readmes_are_read_without_their_code(self):
        # 'all' inside '`api.worldbank.org/v2/country/all/...`' is a URL, not a universal
        self.assertEqual(claims.check("Fine.", {}, readmes=["Fetch `api/country/all/x` and\n```\nall\n```\n"]), [])
        self.assertTrue(claims.check("Fine.", {}, readmes=["Fine here.\n\nAll of it is ERA5."]))

    def test_a_flagged_word_beside_an_apostrophe_or_inside_italics_is_still_flagged(self):
        # review of v3: the new lookarounds treated apostrophes and quotes as part of the word, and '_'
        # (italics) always had been
        for sentence in ("Everyone's income fell after independence.", "Acemoglu called it 'the cause'.",
                         "The authors call it \u2018the worst\u2019 outcome.", "It was everyone\u2019s problem.",
                         "It was \u2018the poorest\u2019 place.", "Income fell in _every_ former colony.",
                         "It was the _cause_.", "It was the _only_ case."):
            with self.subTest(sentence=sentence):
                self.assertTrue(claims.check(sentence, {}))
        self.assertTrue(claims.check("Heat can't be it.", {}))

    def test_reference_list_is_checked_too(self):
        # review of v2: a sentence appended to a reference entry was read by no check at all
        self.assertTrue(claims.check("Fine.\n\n## References\n\nDell, M. (2012). Growth. *AEJ*. Heat explains all of it.", {}))


DOC = """Text citing (Acemoglu et al., 2002) and Dell et al. (2012), and the atlas by Colin McEvedy and Richard Jones (1978).

## References

Acemoglu, D., Johnson, S., & Robinson, J. A. (2002). Reversal of fortune. *QJE, 117*(4), 1231-1294.

Dell, M., Jones, B. F., & Olken, B. A. (2012). Temperature shocks. *AEJ: Macro, 4*(3), 66-95.

McEvedy, C., & Jones, R. (1978). *Atlas of world population history*. Facts on File.
"""


class CiteTest(unittest.TestCase):
    def test_matched_both_ways(self):
        self.assertEqual(cite.check(DOC), [])

    def test_narrative_citation_without_entry_fails(self):
        f = cite.check(DOC.replace("and the atlas", "and Nunn (2020) argues, and the atlas"))
        self.assertTrue(any("Nunn" in x for x in f))

    def test_parenthetical_without_entry_fails(self):
        self.assertTrue(cite.check(DOC.replace("(Acemoglu et al., 2002)", "(Acemoglu et al., 2003)")))

    def test_uncited_entry_fails(self):
        f = cite.check(DOC.replace(" and Dell et al. (2012),", ","))
        self.assertTrue(any("Dell" in x and "never cited" in x for x in f))

    def test_every_citation_in_a_multi_citation_is_checked(self):
        f = cite.check(DOC.replace("(Acemoglu et al., 2002)", "(Nunn, 2008; Acemoglu et al., 2002)"))
        self.assertTrue(any("Nunn" in x for x in f), f)

    def test_page_locators_are_understood(self):
        self.assertEqual(cite.check(DOC.replace("(Acemoglu et al., 2002)", "(Acemoglu et al., 2002, p. 1243)")), [])

    def test_narrative_lookback_cannot_borrow_the_previous_surname(self):
        doc = DOC.replace("Dell et al. (2012)", "Acemoglu et al. (2002). Dell et al. (2002)")
        self.assertTrue(any("Dell" in x for x in cite.check(doc)))

    def test_section_after_references_fails(self):
        # attack: an '## Update' appended after the reference list was invisible to every prose check
        self.assertTrue(any("after the reference list" in x for x in cite.check(DOC + "\n## Update\n\nIt explains 112 cases.\n")))

    def test_block_in_references_that_is_not_an_entry_fails(self):
        self.assertTrue(any("not a reference entry" in x for x in cite.check(DOC + "\nAlso, heat explains 112 cases.\n")))

    def test_a_sentence_shaped_like_an_entry_is_not_an_entry(self):
        # review of v2: 'Dell et al. (2012) later showed ...' after the references passed as an entry
        f = cite.check(DOC + "\nDell, M., Jones, B. F., & Olken, B. A. (2012) later showed heat explains all 112 cases.\n")
        self.assertTrue(any("not a reference entry" in x for x in f), f)

    def test_apa_date_forms_parse(self):
        doc = DOC.replace("and the atlas", "and the agency (World Bank, 2024a) and the atlas") + \
              "\nWorld Bank. (2024a, March 3). *A dataset*.\n"
        self.assertEqual(cite.check(doc), [])

    def test_year_ranges_in_parentheses_are_not_citations(self):
        self.assertEqual(cite.check("Mean over (1991 to 2020) here."), [])


class StyleTest(unittest.TestCase):
    def test_strings(self):
        self.assertTrue(style.check_strings({"chart1 legend": "a – b"}))
        self.assertTrue(style.check_strings({"x": "minus −0.4"}))
        self.assertEqual(style.check_strings({"x": "plain - hyphen"}), [])

    def test_files_including_docx(self):
        d = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, d, True)
        with open(os.path.join(d, "a.md"), "w") as f:
            f.write("ok\nbad — here\n")
        with zipfile.ZipFile(os.path.join(d, "a.docx"), "w") as z:
            z.writestr("word/document.xml", "<w:t>title — sub</w:t>")
        f = style.check_files([os.path.join(d, "a.md"), os.path.join(d, "a.docx")])
        self.assertEqual(len(f), 2)
        self.assertTrue(any("a.md:2" in x for x in f))


class StyleFilesTest(unittest.TestCase):
    def test_a_readme_inside_the_data_folder_is_scanned(self):
        # review of v2: data/ is skipped for its raw files, and an em dash in data/README.md passed
        from types import SimpleNamespace
        d = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, d, True)
        os.makedirs(os.path.join(d, "data"))
        for name in ("README.md", "raw.csv"):
            with open(os.path.join(d, "data", name), "w") as f:
                f.write("An aside \u2014 here.\n")
        files = style.text_files(SimpleNamespace(root=d, docx=None, mdx=None))
        self.assertIn(os.path.join(d, "data", "README.md"), files)
        self.assertNotIn(os.path.join(d, "data", "raw.csv"), files)


class StyleMarkdownTest(unittest.TestCase):
    def test_double_hyphen_and_entities_become_dashes_on_the_live_page(self):
        d = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, d, True)
        for name, text in (("a.md", "heat -- and more"), ("b.mdx", "a &mdash; b"), ("c.md", "a table |---|---|\n---\n")):
            with open(os.path.join(d, name), "w") as f:
                f.write(text)
        f = style.check_files([os.path.join(d, n) for n in ("a.md", "b.mdx", "c.md")])
        self.assertEqual(sorted(x.split(":")[0].rsplit("/", 1)[-1] for x in f), ["a.md", "b.mdx"])


class LinksTest(unittest.TestCase):
    def test_resolves_relative_to_the_draft(self):
        d = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, d, True)
        os.makedirs(os.path.join(d, "charts"))
        open(os.path.join(d, "charts", "rf-1.png"), "w").close()
        draft_dir = os.path.join(d, "draft")
        self.assertEqual(links.check("![a](../charts/rf-1.png)", draft_dir), [])
        self.assertTrue(links.check("![a](../charts/missing.png)", draft_dir))


if __name__ == "__main__":
    unittest.main()
