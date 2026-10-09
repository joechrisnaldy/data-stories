"""Paragraph and sentence splitting, masking, and the per-post config."""

import os
import tempfile
import unittest

from gate.config import ConfigError, load
from gate.text import body_and_refs, mask_spans, paragraphs, sentences


class TextTest(unittest.TestCase):
    def test_references_split_off(self):
        body, refs = body_and_refs("Text.\n\n## References\n\nAuthor (2002).")
        self.assertEqual(body.strip(), "Text.")
        self.assertIn("Author (2002)", refs)

    def test_no_references_section(self):
        self.assertEqual(body_and_refs("Just text.")[1], "")

    def test_paragraph_offsets_point_into_the_text(self):
        t = "First para\nstill first.\n\nSecond para."
        ps = paragraphs(t)
        self.assertEqual(len(ps), 2)
        self.assertEqual(t[ps[1][0]:ps[1][1]], "Second para.")

    def test_sentences_survive_abbreviations_and_decimals(self):
        s = sentences("Dell et al. (2012) find 1.3 points. The gap is real. See e.g. this.")
        self.assertEqual(s, ["Dell et al. (2012) find 1.3 points.", "The gap is real.", "See e.g. this."])

    def test_masking_preserves_length_and_offsets(self):
        t = "keep {{x.r:signed2}} keep"
        m = mask_spans(t, [(5, 20)])
        self.assertEqual(len(m), len(t))
        self.assertTrue(m.startswith("keep ") and m.endswith(" keep"))
        self.assertNotIn("x.r", m)


class ConfigTest(unittest.TestCase):
    def write(self, body):
        d = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, d, True)
        with open(os.path.join(d, "gate.toml"), "w") as f:
            f.write(body)
        return d

    GOOD = '''
[post]
slug = "demo"
source = "draft/demo.src.md"
rendered = "draft/demo.md"
results = "results.json"
build = ["build_analysis.py"]

[allow]
"1500" = "the year the comparison is about"
'''

    def test_loads_and_resolves_paths(self):
        d = self.write(self.GOOD)
        c = load(d)
        self.assertEqual(c.slug, "demo")
        self.assertEqual(c.source, os.path.join(d, "draft/demo.src.md"))
        self.assertEqual(c.allow["1500"], "the year the comparison is about")
        self.assertEqual(c.claims, {})
        self.assertIsNone(c.sources)

    def test_missing_required_field(self):
        with self.assertRaises(ConfigError):
            load(self.write(self.GOOD.replace('results = "results.json"\n', "")))

    def test_allow_entry_without_a_reason_is_refused(self):
        # the audit: an allowlist without per-entry justification launders figures
        with self.assertRaises(ConfigError):
            load(self.write(self.GOOD.replace('"the year the comparison is about"', '""')))

    def test_unknown_section_is_refused(self):
        with self.assertRaises(ConfigError):
            load(self.write(self.GOOD + '\n[external]\n"-0.38" = "AJR"\n'))

    def test_missing_file(self):
        d = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, d, True)
        with self.assertRaises(ConfigError):
            load(d)


if __name__ == "__main__":
    unittest.main()
