"""numbers: every quantity is bound or explicitly exempted. pairs: mixed samples must each show their n.

Fixtures are real defective sentences from this repository's history and the audit's attacks on the
previous gate, which passed all of them.
"""

import os
import unittest

from gate.checks import numbers, pairs
from gate.render import render

R = {
    "tidy": {"r": -0.43518, "n": 196, "sample": "s196", "r2_share": 0.189, "rest_share": 0.811, "growth_pp": 1.3},
    "spread": {"min": 1132.68, "max": 130296.8, "n": 77},
    "col": {"r": 0.29462, "n": 97, "sample": "sA"},
    "inc": {"r": -0.25016, "n": 98, "sample": "sB"},
    "nev_dens": {"r": -0.21122, "n": 76, "sample": "s76"},
    "nev_inc": {"r": -0.28610, "n": 85, "sample": "s85"},
    "common1": {"r": -0.153, "n": 69, "sample": "s69"},
    "common2": {"r": -0.041, "n": 69, "sample": "s69"},
    "nosample1": {"r": 0.5, "n": 10},
    "nosample2": {"r": 0.4, "n": 12},
    "hot_rich": {"count": 17},
}
ALLOW = {"1500": "the year the comparison is about"}


def num_fails(src, allow=None):
    allow = {} if allow is None else allow
    _, b = render(src, R)
    return numbers.check(src, b, allow)


def tmpl_fails(src, allow=None):
    _, b = render(src, R)
    return numbers.check("", [], allow or {}, templates=[("README.md", src, b)])


def pair_fails(src, exempt=None):
    _, b = render(src, R)
    return pairs.check(src, b, exempt or {})


class NumbersTest(unittest.TestCase):
    def test_bound_figures_pass(self):
        self.assertEqual(num_fails("The correlation is {{tidy.r:signed2}} across {{tidy.n:int}} places."), [])

    def test_hand_typed_digit_fails(self):
        self.assertTrue(num_fails("The correlation is minus 0.44 across 196 places."))

    def test_number_followed_by_comma_is_still_seen(self):
        # the old gate's lookahead skipped any number immediately followed by a comma
        self.assertTrue(num_fails("on 2023 income it is {{tidy.r:signed2}} across 941, as before."))

    def test_word_quantities_are_seen(self):
        # the audit rewrote 'a fifth' to 'nine tenths' and the old gate never noticed
        self.assertTrue(num_fails("accounts for about nine tenths of the variation, leaving one tenth."))
        self.assertTrue(num_fails("there are seventeen places above twenty degrees"))

    def test_bound_word_quantity_passes(self):
        self.assertEqual(num_fails("about {{tidy.r2_share:fraction}} of it; {{hot_rich.count:words}} places"), [])

    def test_allowed_phrase_passes_and_reason_is_required_elsewhere(self):
        self.assertEqual(num_fails("in 1500, density was high", ALLOW), [])

    def test_allow_phrase_matches_across_a_line_break(self):
        self.assertEqual(num_fails("over those five\ncenturies, and more", {"five centuries": "1500 to 2023"}), [])

    def test_stale_allow_entry_fails(self):
        f = num_fails("nothing to see", {"1500": "year", "1995": "AJR's income vintage"})
        self.assertTrue(any("1995" in x and "matches nothing" in x for x in f))

    def test_reference_list_and_urls_are_not_prose(self):
        src = "Text in 1500.\n\n## References\n\nAuthor, A. (2002). Title. *J, 117*(4), 1231-1294. https://doi.org/10.1162/0033"
        self.assertEqual(num_fails(src, ALLOW), [])

    def test_image_alt_text_is_prose_but_the_path_is_not(self):
        self.assertTrue(num_fails("![r = -0.44 across 196](../charts/rf-1-tidy.png)"))
        self.assertEqual(num_fails("![The tidy story](../charts/rf-1-tidy.png)"), [])

    def test_citation_years_are_not_quantities(self):
        self.assertEqual(num_fails("as argued (Acemoglu et al., 2002), and Dell et al. (2012) agree; see (World Bank, 2026a)."), [])

    def test_a_number_in_parentheses_is_still_a_quantity(self):
        self.assertTrue(num_fails("the sample (97 countries) was small"))

    def test_sign_typed_beside_a_placeholder_fails(self):
        # attack: 'minus {{x:dec2}}' on a positive value reversed the post's central finding and passed
        self.assertTrue(num_fails("correlate at **minus {{col.r:dec2}}** across {{col.n:int}}"))
        self.assertTrue(num_fails("correlate at -{{col.r:dec2}}"))

    def test_quantity_words_beyond_the_first_lexicon(self):
        for phrase in ("It has halved since.", "about a tenth of it", "ranking seventeenth of them",
                       "a threefold rise", "hundreds of places", "it doubled"):
            self.assertTrue(num_fails(phrase), phrase)

    def test_percentage_points_need_a_key_that_says_so(self):
        # Post 25's Dell et al. figure is already in points; the unit lives in the key name, as _pct does
        self.assertEqual(num_fails("cut growth by {{tidy.growth_pp:dec1}} percentage points"), [])
        self.assertTrue(num_fails("cut growth by {{tidy.r2_share:dec1}} percentage points"))
        self.assertTrue(num_fails("cut growth by {{tidy.growth_pp:dec1}} percent"))

    def test_code_and_list_markers_in_a_readme_are_not_quantities(self):
        # Post 25's data README: '`ex2col == 0`', a fenced build command and '1.' list markers are
        # identifiers or structure, not figures anyone could get wrong in prose
        src = ("1. **Junk.** `ex2col == 0` sits in `ajr_t5/x.dta`.\n   More of the same item.\n2. Next item.\n\n"
               "```bash\npython3 make_charts.py   # writes charts/rf-1..4.png\n```\n")
        self.assertEqual(tmpl_fails(src), [])

    def test_a_bare_figure_in_backticks_is_still_a_figure(self):
        self.assertTrue(tmpl_fails("the correlation is `0.44` today"))
        self.assertTrue(tmpl_fails("1. **Junk.** 120 rows were dropped"))

    def test_the_post_itself_masks_no_code(self):
        # review of v2: '`r = -0.44`' and a fenced 'OLS coef = -0.61, n = 250' passed in the post
        self.assertTrue(num_fails("the correlation is `r = -0.44` across `196 countries`"))
        self.assertTrue(num_fails("Output:\n\n```\nOLS coef = -0.61, n = 250\n```\n"))

    def test_a_hard_wrapped_line_starting_with_a_number_is_not_a_list(self):
        self.assertTrue(num_fails("The sample covers every place with both series, which comes to\n197. The rest"))
        self.assertTrue(tmpl_fails("The sample covers every place, which comes to\n197. The rest"))

    def test_inside_a_list_only_sequential_markers_are_structure(self):
        # review of v3: in a paragraph that opens as a list, a hard-wrapped '197.' was masked too
        self.assertTrue(tmpl_fails("1. Of the colonies, the count fell to\n   197. The rest were dropped."))
        self.assertEqual(tmpl_fails("  1. First point here.\n  2. Second point here."), [])

    def test_other_spellings_of_a_figure(self):
        # review of v2, each passed: APA's leading dot, underscore italics, digits glued after a placeholder,
        # Unicode fractions and 'trillion'
        for src in ("The correlation is r = .44 (p < .01).", "The correlation is _0.44_ across _196_ places.",
                    "across {{tidy.n:int}}.5 places", "about ¾ of the variation, and ½ of the rest",
                    "a trillion dollars of output"):
            with self.subTest(src=src):
                self.assertTrue(num_fails(src))

    def test_other_spellings_of_a_sign_or_percent_beside_a_placeholder(self):
        for src in ("about {{tidy.r2_share:dec2}} per cent of it", "a {{tidy.r2_share:dec2}}-percent share",
                    "about {{tidy.r2_share:dec2}}&nbsp;% of it", "correlate at minus&nbsp;{{tidy.r2_share:dec2}}"):
            with self.subTest(src=src):
                self.assertTrue(num_fails(src))

    def test_a_readme_section_after_references_is_still_scanned(self):
        self.assertTrue(tmpl_fails("Intro.\n\n## References\n\nNotes: heat drops 34 countries.\n"))

    def test_share_printed_as_percent_must_use_a_percent_formatter(self):
        self.assertTrue(num_fails("about {{tidy.r2_share:dec2}} percent of it"))
        self.assertEqual(num_fails("about {{tidy.r2_share:pct0}} percent of it"), [])

    def test_a_citation_parenthetical_cannot_hide_a_figure(self):
        self.assertTrue(num_fails("the gap (r = 0.81 for Europe, 2023) was large"))
        self.assertTrue(num_fails("growth fell (by 1.1 points; Dell et al., 2012) in poor countries"))
        self.assertEqual(num_fails("as found (Smith & Jones, 2019; Dell et al., 2012, p. 67)."), [])

    def test_allow_phrase_needs_word_boundaries(self):
        # attack: an allow entry 'round one' also exempted 'around one'
        self.assertTrue(num_fails("it fell around one tenth", {"round one": "fact-check round name"}))

    def test_digits_inside_a_name_are_not_quantities(self):
        # 'ERA5' is a dataset; '5' glued to letters is part of a name, not a figure
        self.assertEqual(num_fails("from the ERA5 reanalysis, the G20 and PM2.5 levels"), [])

    def test_digits_after_punctuation_are_still_quantities(self):
        self.assertTrue(num_fails("the sample is n=97 here"))
        self.assertTrue(num_fails("(97 countries)"))

    def test_headings_are_prose(self):
        self.assertTrue(num_fails("## Three things we learned\n\nText."))


class PairsTest(unittest.TestCase):
    def test_mixed_samples_with_both_n_pass(self):
        src = ("They correlate at {{col.r:signed2}} across {{col.n:int}} countries. The same thermometer "
               "correlates at {{inc.r:signed2}} across {{inc.n:int}}.")
        self.assertEqual(pair_fails(src), [])

    def test_round_3_defect_fails(self):
        # Post 25 round 3: two figures from samples of 76 and 85, neither n given
        src = "Outside that world heat ran the same way in both eras, {{nev_dens.r:signed2}} then and {{nev_inc.r:signed2}} now."
        self.assertTrue(pair_fails(src))

    def test_magic_phrase_no_longer_silences_it(self):
        src = "Outside that world heat ran the same way, {{nev_dens.r:signed2}} then and {{nev_inc.r:signed2}} now on each side."
        self.assertTrue(pair_fails(src))

    def test_splitting_into_two_sentences_does_not_evade_it(self):
        src = "Then it was {{nev_dens.r:signed2}}. Now it is {{nev_inc.r:signed2}}."
        self.assertTrue(pair_fails(src))

    def test_one_shared_sample_needs_no_n(self):
        src = "On the common set it runs {{common1.r:signed2}} then and {{common2.r:signed2}} now."
        self.assertEqual(pair_fails(src), [])

    def test_separate_paragraphs_are_independent(self):
        self.assertEqual(pair_fails("It was {{nev_dens.r:signed2}}.\n\nIt is {{nev_inc.r:signed2}}."), [])

    def test_different_kinds_of_statistic_are_not_a_comparison(self):
        src = "It is {{tidy.r:signed2}}, about {{tidy.r2_share:fraction}}. Incomes run from {{spread.min:sig2}} to {{spread.max:sig2}}."
        self.assertEqual(pair_fails(src), [])

    def test_reasoned_exemption_silences_a_paragraph(self):
        src = "Then it was {{nev_dens.r:signed2}}. Now it is {{nev_inc.r:signed2}}."
        self.assertEqual(pair_fails(src, {"Then it was": {"reason": "both n stated above", "paths": ["nev_dens", "nev_inc"]}}), [])

    def test_exemption_covers_only_the_paths_it_names(self):
        # attack: a comparison added later to an exempted paragraph inherited the exemption
        src = "Then it was {{nev_dens.r:signed2}}. Now it is {{nev_inc.r:signed2}}, and {{col.r:signed2}} elsewhere."
        f = pair_fails(src, {"Then it was": {"reason": "both n stated above", "paths": ["nev_dens", "nev_inc"]}})
        self.assertTrue(any("col.r" in x for x in f))

    def test_exemption_must_open_exactly_one_paragraph(self):
        # review of v2: the phrase matched anywhere, so a key name ('nev_dens') or a phrase reused in a
        # new paragraph excused that paragraph too
        ex = {"Then it was": {"reason": "both n stated above", "paths": ["nev_dens", "nev_inc"]}}
        src = ("Then it was {{nev_dens.r:signed2}}. Now it is {{nev_inc.r:signed2}}.\n\n"
               "And later: Then it was {{nev_dens.r:signed2}}, now {{nev_inc.r:signed2}}.")
        self.assertTrue(pair_fails(src, ex))
        twice = "Then it was {{nev_dens.r:signed2}}. Now {{nev_inc.r:signed2}}.\n\nThen it was {{nev_dens.r:signed2}} again."
        self.assertTrue(any("opens 2 paragraphs" in x for x in pair_fails(twice, ex)))
        by_key = {"nev_dens": {"reason": "a key name", "paths": ["nev_dens", "nev_inc"]}}
        self.assertTrue(pair_fails("Then it was {{nev_dens.r:signed2}}. Now it is {{nev_inc.r:signed2}}.", by_key))

    def test_stale_exemption_fails(self):
        f = pair_fails("Clean.", {"Then it was": {"reason": "old", "paths": ["nev_dens"]}})
        self.assertTrue(any("excuses nothing" in x for x in f))

    def test_mixing_objects_without_sample_ids_fails_loudly(self):
        f = pair_fails("One is {{nosample1.r:signed2}} and two is {{nosample2.r:signed2}}.")
        self.assertTrue(any("sample id" in x for x in f))


if __name__ == "__main__":
    unittest.main()


class ReadmeTest(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.d = tempfile.mkdtemp(prefix="readmes-")
        for rel in ("README.md", "data/README.md", "docs/README.src.md", "docs/notes.md"):
            os.makedirs(os.path.dirname(os.path.join(self.d, rel)) or self.d, exist_ok=True)
            open(os.path.join(self.d, rel), "w").close()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.d, ignore_errors=True)

    def cfg(self, extra):
        from types import SimpleNamespace
        return SimpleNamespace(root=self.d, extra=[(os.path.join(self.d, a), os.path.join(self.d, b)) for a, b in extra])

    def test_hand_written_readmes_are_scanned(self):
        found = {os.path.relpath(p, self.d) for p in numbers.unconfigured_readmes(self.cfg([]))}
        self.assertEqual(found, {"README.md", "data/README.md", "docs/README.src.md"})

    def test_a_rendered_readme_and_its_template_are_not_scanned_twice(self):
        # the template is checked as a template, with its placeholders masked; scanning it again as
        # hand-written text reported every '{{' line as unbound
        cfg = self.cfg([("docs/README.src.md", "README.md")])
        found = {os.path.relpath(p, self.d) for p in numbers.unconfigured_readmes(cfg)}
        self.assertEqual(found, {"data/README.md"})
