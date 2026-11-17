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


def heads(fails):
    """Each failure without its location and context: "unbound number word 'three'"."""
    return [f.split(" at ")[0] for f in fails]


ROWS = {"gdp": [{"country": "Korea (Rep.)", "gap": 1.1}]}
PAGES = {"pg": {"half": 12.5, "whole": 12, "big": 1234, "year": 2007}}
JOINED = {"a": {"y": 2007, "x": 1}, "b": {"y": 2007, "x": 1}}


def fails_in(results, src, readme=False):
    """numbers on a source rendered from other results; readme=True checks it as a README template."""
    _, b = render(src, results)
    if readme:
        return numbers.check("", [], {}, templates=[("README.md", src, b)])
    return numbers.check(src, b, {})


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

    def test_a_span_of_years_in_a_citation_is_not_a_quantity(self):
        # Post 30 round 1: '(Census Bureau, 1976-2004)' cites volumes issued over a span of years
        self.assertEqual(num_fails("property tax (Census Bureau, 1976-2004) and more."), [])
        self.assertTrue(num_fails("prices rose (1976-2004) then fell."))
        # round 2 attack: a span was masked wherever it followed '(' or ';', but cite reads only the post's '(...)'
        self.assertTrue(num_fails("Renting won; US data, 1972-2025; buying lost."))
        self.assertTrue(tmpl_fails("Each start year (US data, 1972-2025) is raced."))

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
        self.assertEqual(num_fails("as found (Dell et al., 2007, 2009, 2021; Smith & Jones, 2019)."), [])
        self.assertTrue(num_fails("growth fell (Dell et al., 2012, 1.1 points) in poor countries"))
        self.assertIn("unbound number '3'", heads(num_fails("rents rose (up 3 percent per Dell et al., 2012) then.")))

    def test_a_number_word_before_a_citation_author_is_still_a_quantity(self):
        # Post 30 rounds 3 and 4: the whole 'Name..., YEAR' segment was masked, so a number word in front of the
        # author passed unchecked. Only the date may be masked; 'three' must be reported.
        three = ["unbound number word 'three'"]
        self.assertEqual(heads(num_fails("rents rose (up three percent per the U.S. Census Bureau, 2026) then.")),
                         three)
        self.assertEqual(heads(num_fails("rents rose (up three percent per the U.S. Census Bureau, 1976-2004) then.")),
                         three)
        self.assertEqual(heads(num_fails("as shown (in three studies, Rappaport, 2007, 2010) then.")), three)
        self.assertEqual(heads(num_fails("as found (up three percent per Dell et al., 2012, p. 67).")), three)
        self.assertEqual(heads(num_fails("rents rose (by one point, Dell et al., 2012) then.")),
                         ["unbound number word 'one'"])

    def test_a_number_word_anywhere_in_a_citation_names_part_is_a_quantity(self):
        # the names part is read up to the comma before the date, not only up to the first capital letter
        self.assertEqual(heads(num_fails("rents rose (U.S. Census Bureau, three-year estimates, 2026) then.")),
                         ["unbound number word 'three'"])
        self.assertEqual(heads(num_fails("as shown (Dell and three coauthors, 2007, 2010) then.")),
                         ["unbound number word 'three'"])
        self.assertEqual(heads(num_fails("tax (U.S. Census Bureau and three agencies, 1976-2004) then.")),
                         ["unbound number word 'three'"])
        g20 = "leaders met (Group of Twenty, 2019) then."
        self.assertEqual(heads(num_fails(g20)), ["unbound number word 'Twenty'"])
        self.assertEqual(heads(tmpl_fails(g20)), ["unbound number word 'Twenty'"])
        # gate/README.md's way out: the [allow] phrase is the name without its date
        self.assertEqual(num_fails(g20, {"Group of Twenty": "an organisation"}), [])

    def test_a_number_word_before_a_citation_author_is_a_quantity_in_a_readme(self):
        self.assertEqual(heads(tmpl_fails("rents rose (up three percent per the U.S. Census Bureau, 2026) then.")),
                         ["unbound number word 'three'"])

    def test_citation_names_and_dates_without_quantities_stay_clean(self):
        # controls: the date (year, years or span, and any page locator) is still masked after the names part
        self.assertEqual(num_fails("Tax (U.S. Census Bureau & U.S. Department of Housing and Urban Development, "
                                   "1976-2004) and ACS (U.S. Census Bureau, 2026)."), [])
        self.assertEqual(num_fails("as argued (e.g., Dell et al., 2012, p. 14; see also Kiyosaki, 2016)."), [])
        self.assertEqual(num_fails("as argued (e.g., Rappaport, 2007, 2010, p. 3)."), [])
        self.assertEqual(num_fails("as argued (e.g., Census Bureau, 1976-2004, p. 3)."), [])
        self.assertEqual(tmpl_fails("as argued (e.g., Dell et al., 2012)."), [])

    def test_several_years_are_masked_only_in_a_post_citation(self):
        # several years are masked only inside a full '(...)' of the post; anywhere else they stay figures
        self.assertTrue(num_fails("prices rose; Jakarta, 1850, 1900) then fell."))
        self.assertTrue(num_fails("prices rose; Jakarta, 2005, 2008; then fell."))
        self.assertTrue(tmpl_fails("as found (Dell et al., 2007, 1850)."))

    def test_a_year_in_a_semicolon_run_outside_parentheses_is_a_quantity(self):
        # attack on 8de312e: the single-year mask matched any 'Name, YEAR' run after ';', so outside parentheses,
        # where cite never reads, 'prices rose; Jakarta, 2005; then fell.' hid its year
        self.assertEqual(heads(num_fails("prices rose; Jakarta, 2005; then fell.")), ["unbound number '2005'"])
        self.assertEqual(heads(num_fails("prices rose; Jakarta, 1850) then fell.")), ["unbound number '1850'"])
        self.assertEqual(heads(num_fails("Counts were high; Jakarta, 1850; Bali, 1700; Lombok, 1650.")),
                         ["unbound number '1850'", "unbound number '1700'", "unbound number '1650'"])
        self.assertEqual(heads(tmpl_fails("prices rose; Jakarta, 2005; then fell.")), ["unbound number '2005'"])

    def test_a_year_after_a_semicolon_inside_parentheses_is_still_a_citation_date(self):
        # controls: inside an innermost '(...)', where cite reads, the date after ';' or across a line stays masked
        self.assertEqual(num_fails("Tax (see the volumes; U.S. Census Bureau, 2026) and more."), [])
        self.assertEqual(num_fails("Tax (U.S. Census\nBureau, 2026) and more."), [])
        self.assertEqual(tmpl_fails("Tax (see the volumes; U.S. Census Bureau, 2026) and more."), [])

    def test_a_semicolon_run_is_masked_only_inside_its_own_innermost_pair(self):
        # mutants that searched past a pair's end, from before its start, or in pairs that are not innermost survived
        # the tests above, which had no other parenthesis in the text
        y2005 = ["unbound number '2005'"]
        self.assertEqual(heads(num_fails("A (note). Prices rose; Jakarta, 2005; then fell (a lot).")), y2005)
        self.assertEqual(heads(num_fails("Prices (rose; Jakarta, 2005; then (fell)) later.")), y2005)
        self.assertEqual(heads(num_fails("A (note) and prices rose; Jakarta, 2005) then fell.")), y2005)
        self.assertEqual(heads(tmpl_fails("A (note). Prices rose; Jakarta, 2005; then fell (a lot).")), y2005)

    def test_a_placeholder_path_with_parentheses_does_not_break_a_citation(self):
        # found in the source, a selector such as '[country=Korea (Rep.)]' would hold a '(' that its printed value does
        # not, so an innermost-only rule would find the citation not innermost and report its year
        cited = "Growth lagged (by {{gdp[country=Korea (Rep.)].gap:dec1}} points; World Bank, 2024) there."
        first = "Growth lagged (World Bank, 2024; by {{gdp[country=Korea (Rep.)].gap:dec1}} points) there."
        self.assertEqual(fails_in(ROWS, cited), [])
        self.assertEqual(fails_in(ROWS, first), [])
        self.assertEqual(fails_in(ROWS, cited, readme=True), [])

    def test_a_printed_figure_in_a_names_part_ends_the_citation_as_cite_reads_it(self):
        # numbers read '{{tidy.n:int}}' as letters and hid ', 2002', while cite reads the printed '196', cannot parse
        # that citation and never checks its year
        digits = "The sample (the {{tidy.n:int}} colonies of Acemoglu et al., 2002) is small."
        words = "The sample (the {{hot_rich.count:words}} colonies of Acemoglu et al., 2002) is small."
        self.assertEqual(heads(num_fails(digits)), ["unbound number '2002'"])
        self.assertEqual(num_fails(words), [])

    def test_a_readme_citation_holding_a_link_or_code_keeps_its_date_masked(self):
        # in a README, where cite never runs, a link target or code with parentheses inside a citation's parentheses
        # would make them not innermost, and an innermost-only rule would report the year
        self.assertEqual(tmpl_fails("Household spending comes from the survey microdata (`SUSENAS`, 2024)."), [])
        lancet = ("Data come from the Lancet series (see [the paper](https://doi.org/10.1016/S0140-6736(20)30183-5); "
                  "Huang et al., 2020).")
        self.assertEqual(tmpl_fails(lancet), [])
        self.assertEqual(tmpl_fails("Rates rose (BPS, 2024; [table](https://bps.go.id/x))."), [])
        self.assertEqual(tmpl_fails("Rates rose (BPS, 2024; built by `load()` in the script)."), [])
        # a bare URL is not blanked for pairing: its mask runs to the next space, past the closing ')'
        self.assertEqual(tmpl_fails("Rates rose (BPS, 2024; https://bps.go.id/x)."), [])
        # in the post, cite reads the same text and skips those parentheses, so the year is reported there
        self.assertEqual(heads(num_fails("Rates rose (BPS, 2024; [table](https://bps.go.id/x)).")),
                         ["unbound number '2024'"])
        # a URL whose own parentheses pair (a DOI), and code with no letter, also pair nothing for the citation
        doi = "Cases rose (Huang et al., 2020; https://doi.org/10.1016/S0140-6736(20)30183-5) fast."
        self.assertEqual(tmpl_fails(doi), [])
        self.assertEqual(tmpl_fails("Rates rose (BPS, 2024; built by `()` here)."), [])
        self.assertEqual(tmpl_fails("Rates rose (see https://bps.go.id/x; BPS, 2024)."), [])
        # code blanked for pairing must not let a date run stretch over a bare figure in backticks, still a figure
        self.assertEqual(heads(tmpl_fails("Rates rose (BPS, `1850` 2024) there.")),
                         ["unbound number '1850'", "unbound number '2024'"])

    def test_a_citation_is_read_in_the_printed_text_not_the_placeholder_source(self):
        # a page number that does not print as plain digits is no page locator to cite, which then never checks the
        # year, so the year must be reported; a page that prints as digits leaves the citation to cite
        self.assertEqual(heads(fails_in(PAGES, "It lagged (Smith, 2011, p. {{pg.half:dec1}}) then.")),
                         ["unbound number '2011'"])
        self.assertEqual(heads(fails_in(PAGES, "It lagged (Smith, 2011, p. {{pg.big:int}}) then.")),
                         ["unbound number '2011'"])
        self.assertEqual(heads(fails_in(PAGES, "It lagged (Smith, 2011, p. {{pg.half:dec1}}) then.", readme=True)),
                         ["unbound number '2011'"])
        self.assertEqual(fails_in(PAGES, "It lagged (Smith, 2011, p. {{pg.whole:int}}) then."), [])
        # a placeholder that prints a year is a year: cite reads '(Smith, 2007, 2012)' and checks both
        self.assertEqual(fails_in(PAGES, "Growth was slow (Smith, {{pg.year:year}}, 2012) then."), [])
        self.assertEqual(fails_in(PAGES, "Growth was slow (Smith, 2012, {{pg.year:year}}) then."), [])

    def test_a_joined_placeholder_is_printed_once(self):
        # render gives each key of '{{a.y&b.y:year}}' a binding over the same span; printed once per key, the year read
        # '20072007', so a year cite accepts was reported and a citation cite cannot read hid its typed figures
        self.assertEqual(fails_in(JOINED, "Growth was slow (Smith, {{a.y&b.y:year}}, 2012) then."), [])
        self.assertEqual(heads(fails_in(JOINED, "Growth was slow (Smith, 20{{a.x&b.x:int}}, 2007) then.")),
                         ["unbound number '20'", "unbound number '2007'"])

    def test_a_number_word_in_underscore_italics_is_a_quantity(self):
        # attack on 8de312e: '\b' treats '_' as a letter, so '_three_' (Markdown italics) passed everywhere
        three = ["unbound number word 'three'"]
        self.assertEqual(heads(num_fails("rents rose _three_ percent then.")), three)
        self.assertEqual(heads(num_fails("rents rose __three__ percent then.")), three)
        self.assertEqual(heads(num_fails("it _doubled_ and then _quadrupled_.")),
                         ["unbound number word 'doubled'", "unbound number word 'quadrupled'"])
        self.assertEqual(heads(num_fails("a _threefold_ rise.")), ["unbound number word 'threefold'"])
        self.assertEqual(heads(num_fails("rents rose (up _three_ percent per Dell et al., 2012) then.")), three)
        self.assertEqual(heads(tmpl_fails("rents rose _three_ percent then.")), three)

    def test_an_underscore_sign_or_percent_beside_a_placeholder_is_still_typed_by_hand(self):
        # _SIGN_BEFORE kept '\b', so '_minus_ {{x}}' passed, and one '_' was the only underscore emphasis read beside
        # a placeholder
        sign = ["a sign is typed by hand before {{col.r:dec2}}"]
        self.assertEqual(heads(num_fails("correlate at _minus_ {{col.r:dec2}} here")), sign)
        self.assertEqual(heads(num_fails("correlate at __minus__ {{col.r:dec2}} here")), sign)
        self.assertEqual(heads(tmpl_fails("correlate at _negative_ {{col.r:dec2}} here")), sign)
        self.assertEqual(heads(num_fails("about {{tidy.r2_share:dec2}} __percent__ of it")),
                         ["{{tidy.r2_share:dec2}} is printed as a percent"])

    def test_underscore_emphasis_around_a_points_unit_or_inside_an_identifier_is_not_a_typed_sign(self):
        # 'percentage points' in '_' or '__' emphasis is still points, and a snake_case name ending in a sign word is a
        # name: Markdown reads an underscore as emphasis only at a word's edge
        self.assertEqual(num_fails("cut growth by {{tidy.growth_pp:dec1}} __percentage points__ there"), [])
        self.assertEqual(num_fails("cut growth by {{tidy.growth_pp:dec1}} _percentage points_ there"), [])
        self.assertEqual(tmpl_fails("the column false_positive {{tidy.n:int}} rows"), [])
        self.assertEqual(num_fails("the field net_negative {{tidy.n:int}} rows"), [])
        self.assertEqual(num_fails("the field net\\_negative {{tidy.n:int}} rows"), [])

    def test_a_number_word_inside_an_identifier_is_not_a_quantity(self):
        # 'top_ten' and 'share_one' join words with '_' (no emphasis), as '\b' always read them
        self.assertEqual(tmpl_fails("see top_ten.csv and the share_one column"), [])
        self.assertEqual(num_fails("see top_ten.csv and the share_one column"), [])
        self.assertEqual(num_fails("see ten_rows.csv and the one_hot column"), [])
        # an escaped '\_' joins two words the same way
        self.assertEqual(num_fails("See the top\\_ten column and the share\\_one column."), [])

    def test_an_allow_phrase_switches_off_chart_pairing_only_where_it_covers_r_or_n(self):
        # an [allow] phrase anywhere in a chart text switched off the r and n pairing ('(base 1500)' with '1500'); now
        # only one that covers a printed r or n does, so an italic '_three_' does not either
        for prose, allow in (("r = 0.81, n = 97 (base 1500)", {"1500": "the year the comparison is about"}),
                             ("r = 0.81, n = 97, _three_ panels", {"three": "the panel count"})):
            fails = numbers.chart_figures([{"file": "c.png", "prose": [prose]}], R, None, allow)
            self.assertTrue(any("no single result has both" in f for f in fails), (prose, fails))

    def test_an_allow_phrase_also_covers_its_italic_form(self):
        # [allow] phrases matched with (?<!\w)...(?!\w), so an italic '_three_' could not be exempted
        self.assertEqual(num_fails("rents rose _three_ percent then.", {"three": "a count stated in the source"}), [])
        self.assertEqual(num_fails("the _Three-Body Problem_ sold well.", {"Three-Body Problem": "a book title"}), [])

    def test_a_number_word_inside_a_longer_word_is_not_a_quantity(self):
        # control: a letter on either side keeps 'one' in 'someone' and 'ten' in 'often' or 'tenant' out
        self.assertEqual(num_fails("Someone, anyone and the tenant often phone; _tenant_ too."), [])
        # a digit or a non-ASCII letter touching it counts as a letter, and 'fold' alone is not '-fold'
        self.assertEqual(num_fails("the A4one form, the one4all fund, Ñone and oneñ"), [])
        self.assertEqual(num_fails("each fold of a k-fold split"), [])

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


SHARES = {"shares": {"email": 0.764, "whatsapp": 0.549, "indonesia": 0.927},
          "ci": {"mean_pct": -0.4, "lo_pct": -1.3, "hi_pct": 0.5},
          "ranks": {"density_pct": 80, "income_pct": 20},
          "gap": {"change_pp": 1.3, "first_pct": 12.1, "last_pct": 14.0},
          "days": {"count": 17}}


def unit_fails(src, readme=False):
    """The failures that say a percent was printed with no unit in its sentence."""
    return [f for f in fails_in(SHARES, src, readme) if "names no unit" in f]


class PercentUnitTest(unittest.TestCase):
    """pct0 and pct1 print a bare number: Post 31 printed '76.4 of internet users' and passed the gate."""

    def test_post_31s_sentences_without_the_unit_fail(self):
        # draft/outlook-break-or-blocker.src.md before the fix of 2026-11-17, figures and citations as written
        src = ("In GWI's survey, {{shares.email:pct1}} of internet users in its surveyed markets said they used email "
               "in the past month, against {{shares.whatsapp:pct1}} for WhatsApp (DataReportal, 2026a). In Indonesia "
               "the picture flips: {{shares.indonesia:pct1}} of internet users said they used WhatsApp in the past "
               "month (DataReportal, 2026b).")
        self.assertEqual(len(unit_fails(src)), 3)

    def test_post_31s_alt_text_without_the_unit_fails(self):
        # the chart 2 alt template of the same day, checked as the published fields are: as a template
        src = ("A bar chart of the share of internet users who used email and WhatsApp in the past month: email "
               "{{shares.email:pct1}} and WhatsApp {{shares.whatsapp:pct1}} in GWI's surveyed markets, WhatsApp "
               "{{shares.indonesia:pct1}} in Indonesia.")
        self.assertEqual(len(unit_fails(src, readme=True)), 3)

    def test_a_unit_named_once_covers_its_sentence(self):
        # the conventions of the live posts: a range, a run sharing one unit, an interval after a stated mean
        for src in ("Among householders under 25 it rose, from {{gap.first_pct:dec1}} to {{gap.last_pct:dec1}} percent.",
                    "Bitcoin fell further in each: {{shares.email:pct0}} percent against the S&P 500's "
                    "{{shares.whatsapp:pct0}}, then {{shares.indonesia:pct0}} against {{shares.whatsapp:pct0}}.",
                    "Bitcoin averaged {{ci.mean_pct:signed1}} percent, with an interval from {{ci.lo_pct:signed1}} to "
                    "{{ci.hi_pct:signed1}}, and it rose on {{days.count:int}} of the days.",
                    "In GWI's survey, {{shares.email:pct1}} percent of internet users said they used email, against "
                    "{{shares.whatsapp:pct1}} for WhatsApp."):
            with self.subTest(src=src):
                self.assertEqual(unit_fails(src), [])

    def test_every_spelling_of_the_unit_counts(self):
        for src in ("the worst {{shares.email:pct0}}% of days", "about {{shares.email:pct0}} per cent of it",
                    "about {{shares.email:pct0}}&nbsp;percent of it", "a **{{shares.email:pct0}} percent** share"):
            with self.subTest(src=src):
                self.assertEqual(unit_fails(src), [])

    def test_percentage_points_are_named_by_points(self):
        self.assertEqual(unit_fails("after August, by {{gap.change_pp:dec1}} points."), [])
        self.assertEqual(unit_fails("| Inflation speeds up | {{gap.change_pp:dec1}} points or more faster |"), [])
        self.assertEqual(len(unit_fails("rates rose by {{gap.change_pp:dec1}} in the year after the slide.")), 1)

    def test_a_percentile_rank_printed_as_an_ordinal_is_not_a_percent(self):
        # Post 25: 'Sudan, 80th to 20th.' is a rank in percentiles, stated in the sentence before
        self.assertEqual(unit_fails("Sudan, {{ranks.density_pct:ordinal0}} to {{ranks.income_pct:ordinal0}}."), [])

    def test_a_unit_in_another_sentence_does_not_count(self):
        src = "Email reached {{shares.email:pct1}} of users. WhatsApp reached {{shares.whatsapp:pct1}} percent."
        self.assertEqual(len(unit_fails(src)), 1)

    def test_percentage_points_do_not_name_a_percent(self):
        src = "Email reached {{shares.email:pct1}} of users, up {{gap.change_pp:dec1}} percentage points."
        self.assertEqual(len(unit_fails(src)), 1)

    def test_a_unit_inside_a_link_or_url_does_not_count(self):
        for src in ("Email reached {{shares.email:pct1}} of users ([the report](https://example.org/percent-of-users)).",
                    "Email reached {{shares.email:pct1}} of users (https://example.org/percent-of-users)."):
            with self.subTest(src=src):
                self.assertEqual(len(unit_fails(src)), 1)

    # The attack round of 2026-11-17 printed Post 31's own sentences through each layout below and passed the gate.
    POST31_ITEMS = ("In its surveyed markets, {{shares.email:pct1}} of internet users said they used email (Kemp, 2026a).",
                    "WhatsApp reached {{shares.whatsapp:pct1}} percent.",
                    "In Indonesia, {{shares.indonesia:pct1}} of internet users said they used WhatsApp (Kemp, 2026b).")

    def test_each_list_item_is_its_own_sentence(self):
        for marker in ("- ", "* ", "+ "):
            for intro in ("The shares:\n", "The shares:\n\n"):
                src = intro + "\n".join(marker + item for item in self.POST31_ITEMS)
                with self.subTest(src=src):
                    self.assertEqual(len(unit_fails(src)), 2)
                    self.assertEqual(len(unit_fails(src, readme=True)), 2)
        numbered = "\n".join(f"{i}. {item}" for i, item in enumerate(self.POST31_ITEMS, 1))
        self.assertEqual(len(unit_fails(numbered)), 2)

    def test_a_stop_before_a_closing_mark_ends_the_sentence(self):
        # rent-vs-buy and reversal-of-fortune open paragraphs with '**Lead.** Next', 84 times in the live templates
        bare = "In Indonesia, {{shares.indonesia:pct1}} of internet users said they used WhatsApp"
        for left, right in (("**", ".**"), ("_", "._"), ('"', '."'), ("“", ".”"), ("(", ".)"), ("*", ".*")):
            src = f"{left}{bare}{right} In GWI's survey, {{{{shares.email:pct1}}}} percent used email."
            with self.subTest(src=src):
                self.assertEqual(len(unit_fails(src)), 1)

    def test_each_table_row_is_its_own_sentence(self):
        src = "| Service | Share |\n|---|---|\n| Email | {{shares.email:pct1}} percent |\n| WhatsApp | {{shares.whatsapp:pct1}} |"
        self.assertEqual(len(unit_fails(src)), 1)
        self.assertEqual(len(unit_fails(src, readme=True)), 1)

    def test_a_column_header_names_the_unit_for_its_column(self):
        self.assertEqual(unit_fails("| Service | Share (%) |\n|---|---|\n| Email | {{shares.email:pct1}} |\n"
                                    "| WhatsApp | {{shares.whatsapp:pct1}} |"), [])
        self.assertEqual(len(unit_fails("| Share (%) | Later |\n|---|---|\n| {{shares.email:pct1}} | "
                                        "{{shares.whatsapp:pct1}} |")), 1)

    def test_a_heading_image_or_quote_line_is_its_own_sentence(self):
        for src in ("Email reached {{shares.email:pct1}} percent of users.\n![WhatsApp at {{shares.whatsapp:pct1}}](c.png)",
                    "## Email at {{shares.email:pct1}} percent\nWhatsApp reached {{shares.whatsapp:pct1}} of users.",
                    "Email reached {{shares.email:pct1}} percent of users.\n> WhatsApp reached {{shares.whatsapp:pct1}} of users."):
            with self.subTest(src=src):
                self.assertEqual(len(unit_fails(src)), 1)

    def test_a_sentence_may_open_with_any_capital_quote_or_mark(self):
        for opener in ("“WhatsApp”", "_WhatsApp_", "`WhatsApp`", "Émile's app", "**WhatsApp**"):
            src = (f"Email reached {{{{shares.email:pct1}}}} percent of users. {opener} reached "
                   "{{shares.whatsapp:pct1}} of users.")
            with self.subTest(src=src):
                self.assertEqual(len(unit_fails(src)), 1)

    def test_a_word_that_ends_like_an_abbreviation_still_ends_its_sentence(self):
        # 'devs.' holds 'vs.', which the splitter protects only as a word of its own
        src = "Email reached {{shares.email:pct1}} percent of devs. WhatsApp reached {{shares.whatsapp:pct1}} of devs."
        self.assertEqual(len(unit_fails(src)), 1)

    def test_an_ellipsis_ends_a_sentence(self):
        src = "Email reached {{shares.email:pct1}} percent of users… WhatsApp reached {{shares.whatsapp:pct1}} of users."
        self.assertEqual(len(unit_fails(src)), 1)

    def test_a_hard_line_break_ends_a_sentence(self):
        # the verification round of 2026-11-17: key-figure lines joined by a hard break passed as one sentence
        for brk in ("<br>", "<br />", "  ", "\\"):
            src = (f"**Email:** {{{{shares.email:pct1}}}} of internet users{brk}\n"
                   "**WhatsApp:** {{shares.whatsapp:pct1}} percent of internet users")
            with self.subTest(brk=repr(brk)):
                self.assertEqual(len(unit_fails(src)), 1)

    def test_a_sentence_may_open_with_anything_but_a_lowercase_letter(self):
        for opener in ("£5 plans", "«WhatsApp»", "&amp; WhatsApp", "#WhatsApp"):
            src = (f"Email reached {{{{shares.email:pct1}}}} percent of users. {opener} reached "
                   "{{shares.whatsapp:pct1}} of users.")
            with self.subTest(opener=opener):
                self.assertEqual(len(unit_fails(src)), 1)

    def test_an_escaped_pipe_does_not_move_a_figure_to_another_column(self):
        src = ("| App | Share of users | Change, percent |\n|---|---|---|\n"
               "| Email \\| Gmail | {{shares.email:pct1}} | none |")
        self.assertEqual(len(unit_fails(src)), 1)

    def test_a_unit_in_code_or_a_comment_does_not_count(self):
        self.assertEqual(len(unit_fails("Email reached {{shares.email:pct1}} of users; `make_charts.py` prints it "
                                        "with `'%.1f'`.", readme=True)), 1)
        self.assertEqual(len(unit_fails("Email reached {{shares.email:pct1}} of users. <!-- percent -->")), 1)


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
