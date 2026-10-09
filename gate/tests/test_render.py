"""The renderer turns {{path:fmt}} placeholders into text and refuses anything it cannot resolve."""

import unittest

from gate.render import RenderError, render

RESULTS = {
    "tidy_story": {"r": -0.43518, "n": 196, "share_pct": 18.9, "growth_pp": 1.3},
    "flip": {"density_1500|income_2023|all": {"r": 0.0351, "n": 163}},
    "ranks": [{"iso3": "BDI", "density_pct": 98.40}, {"iso3": "IDN", "density_pct": 78.72}],
    "indonesia": {"rank_by_slide": 47},
}
SOURCES = {"dell2012": {"values": {"growth_pp": 1.3}, "extra": {"growth_pp": 1.1}}}


class RenderTest(unittest.TestCase):
    def test_simple_placeholder(self):
        out, b = render("r is {{tidy_story.r:signed2}}.", RESULTS)
        self.assertEqual(out, "r is minus 0.44.")
        self.assertEqual(len(b), 1)
        self.assertEqual(b[0].path, "tidy_story.r")
        self.assertEqual(b[0].leaf, "r")
        self.assertEqual(b[0].parent_path, "tidy_story")
        self.assertEqual(b[0].parent["n"], 196)

    def test_whitespace_inside_braces(self):
        out, _ = render("{{ tidy_story.n : int }}", RESULTS)
        self.assertEqual(out, "196")

    def test_key_containing_pipes(self):
        out, _ = render("{{flip.density_1500|income_2023|all.r:signed2}}", RESULTS)
        self.assertEqual(out, "plus 0.04")

    def test_list_selector(self):
        out, b = render("{{ranks[iso3=IDN].density_pct:ordinal0}}", RESULTS)
        self.assertEqual(out, "79th")
        self.assertEqual(b[0].parent_path, "ranks[iso3=IDN]")

    def test_source_placeholder(self):
        out, b = render("{{src:dell2012.values.growth_pp:dec1}}", RESULTS, SOURCES)
        self.assertEqual(out, "1.3")
        self.assertEqual(b[0].origin, "src")

    def test_positions_refer_to_source_text(self):
        src = "a {{tidy_story.n:int}} b"
        _, b = render(src, RESULTS)
        self.assertEqual(src[b[0].start:b[0].end], "{{tidy_story.n:int}}")

    def test_text_without_placeholders_is_unchanged(self):
        self.assertEqual(render("plain text, 1500.", RESULTS)[0], "plain text, 1500.")


class SharedValueTest(unittest.TestCase):
    R2 = {"a": {"n": 43, "r": -0.42}, "b": {"n": 43, "r": 0.28}, "c": {"n": 41}}

    def test_equal_values_render_once_and_bind_both(self):
        out, b = render("{{a.n&b.n:int}} countries on each side", self.R2)
        self.assertEqual(out, "43 countries on each side")
        self.assertEqual(sorted(x.parent_path for x in b), ["a", "b"])

    def test_unequal_values_are_refused(self):
        with self.assertRaises(RenderError):
            render("{{a.n&c.n:int}}", self.R2)


class RefusalTest(unittest.TestCase):
    def assertRefuses(self, src, sources=None):
        with self.assertRaises(RenderError, msg=src):
            render(src, RESULTS, sources)

    def test_unknown_key(self):
        self.assertRefuses("{{tidy_story.rho:signed2}}")

    def test_unknown_top_level_key(self):
        self.assertRefuses("{{nothing.r:signed2}}")

    def test_unknown_formatter(self):
        self.assertRefuses("{{tidy_story.r:pretty}}")

    def test_missing_formatter(self):
        self.assertRefuses("{{tidy_story.r}}")

    def test_unclosed_placeholder(self):
        self.assertRefuses("r is {{tidy_story.r:signed2 and more text")

    def test_stray_closing_braces(self):
        self.assertRefuses("r is tidy_story.r:signed2}} here")

    def test_selector_with_no_match(self):
        self.assertRefuses("{{ranks[iso3=XXX].density_pct:ordinal0}}")

    def test_selector_on_a_non_list(self):
        self.assertRefuses("{{tidy_story[iso3=IDN].r:signed2}}")

    def test_path_ending_on_an_object(self):
        self.assertRefuses("{{tidy_story:signed2}}")

    def test_formatter_error_carries_the_path(self):
        with self.assertRaises(RenderError) as cm:
            render("{{tidy_story.r:dec2}}", RESULTS)
        self.assertIn("tidy_story.r", str(cm.exception))

    def test_misordered_braces_never_leak_into_output(self):
        self.assertRefuses("{{tidy_story.n:int}} then }} and {{ again")

    def test_source_placeholder_without_sources(self):
        self.assertRefuses("{{src:dell2012.values.growth_pp:dec1}}")


if __name__ == "__main__":
    unittest.main()


class UnitTest(unittest.TestCase):
    """Review of v2: a source figure outside 'values' was rendered but never compared with the quote, and
    a key already in percent could be multiplied by 100 again."""

    def test_source_placeholder_must_point_inside_values(self):
        with self.assertRaises(RenderError):
            render("{{src:dell2012.extra.growth_pp:dec1}}", RESULTS, SOURCES)

    def test_a_key_named_as_a_percentage_anywhere_cannot_take_a_percent_formatter(self):
        # review of v3: only the suffixes _pct and _pp were recognised
        res = {"g": {"growth_percent": 0.8, "pct_growth": 0.8, "growth_pc": 0.8, "r2_share": 0.19}}
        for key in ("g.growth_percent", "g.pct_growth", "g.growth_pc"):
            with self.subTest(key=key), self.assertRaises(RenderError):
                render("{{" + key + ":pct1}}", res)
        self.assertEqual(render("{{g.r2_share:pct0}}", res)[0], "19")

    def test_a_percent_key_cannot_take_a_percent_formatter(self):
        for key in ("tidy_story.share_pct", "tidy_story.growth_pp"):
            with self.subTest(key=key), self.assertRaises(RenderError):
                render("{{" + key + ":pct1}}", RESULTS)
        self.assertEqual(render("{{tidy_story.share_pct:dec1}}", RESULTS)[0], "18.9")
