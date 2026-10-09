"""The published MDX is the surface readers see; it must agree with the draft, the charts and the
templates that own its hand-written fields (alt text, excerpt, metaDescription)."""

import os
import shutil
import tempfile
import unittest
from types import SimpleNamespace

from gate.checks import published

MD = """# Title

First paragraph with minus 0.44.

![Chart one](../charts/c-1.png)

Second paragraph.
"""
MDX = """---
title: "Title"
excerpt: "An excerpt."
metaDescription: "Correlates at minus 0.44."
---

First paragraph with minus 0.44.

<figure>
  <img src="/images/blog/c-1.png" alt="A scatter plot, r = minus 0.44." />
  <figcaption>Footnote text of chart one.</figcaption>
</figure>

Second paragraph.
"""
CAPTURE = [{"file": "c-1.png", "texts": ["Chart one", "Footnote text of chart one.", "r = -0.44"],
            "fig_texts": ["Footnote text of chart one."], "axes": []}]
FIELDS = {"excerpt": "An excerpt.", "metaDescription": "Correlates at minus 0.44.",
          "alt:c-1.png": "A scatter plot, r = minus 0.44."}


class PublishedTest(unittest.TestCase):
    def test_consistent(self):
        self.assertEqual(published.check(MDX, MD, CAPTURE, FIELDS), [])

    def test_body_drift_fails(self):
        self.assertTrue(published.check(MDX.replace("Second paragraph.", "Second paragraph, edited."), MD, CAPTURE, FIELDS))

    def test_caption_must_be_the_charts_own_footnote(self):
        self.assertTrue(published.check(MDX.replace("Footnote text of chart one.", "A different caption."), MD, CAPTURE, FIELDS))

    def test_field_must_match_its_template(self):
        self.assertTrue(published.check(MDX.replace("Correlates at minus 0.44.", "Correlates at minus 0.48."), MD, CAPTURE, FIELDS))

    def test_hand_written_field_without_a_template_fails(self):
        fields = {k: v for k, v in FIELDS.items() if k != "alt:c-1.png"}
        self.assertTrue(any("no template" in x for x in published.check(MDX, MD, CAPTURE, fields)))

    def test_single_quoted_field_is_parsed_and_checked(self):
        # attack: a single-quoted metaDescription was skipped by a parser that only read double quotes
        mdx = MDX.replace('metaDescription: "Correlates at minus 0.44."', "metaDescription: 'Correlates at minus 0.64.'")
        self.assertTrue(published.check(mdx, MD, CAPTURE, FIELDS))

    def test_unparseable_front_matter_fails(self):
        mdx = MDX.replace('excerpt: "An excerpt."', "excerpt: >\n  An excerpt\n  folded.")
        self.assertTrue(any("front matter" in x for x in published.check(mdx, MD, CAPTURE, FIELDS)))

    def test_title_must_be_the_drafts_heading(self):
        self.assertTrue(published.check(MDX.replace('title: "Title"', 'title: "Another Title"'), MD, CAPTURE, FIELDS))

    def test_untemplated_text_field_fails(self):
        mdx = MDX.replace('excerpt:', 'seoTitle: "Heat Explains Half of 196 Countries"\nexcerpt:')
        self.assertTrue(any("seoTitle" in x for x in published.check(mdx, MD, CAPTURE, FIELDS)))

    def test_template_whose_field_is_absent_fails(self):
        mdx = MDX.replace('metaDescription: "Correlates at minus 0.44."\n', "")
        self.assertTrue(any("metaDescription" in x for x in published.check(mdx, MD, CAPTURE, FIELDS)))

    def test_text_after_the_references_is_compared(self):
        md = MD + "\n## References\n\nAuthor, A. (2002). Title.\n"
        mdx = MDX + "\n## References\n\nAuthor, A. (2002). Title.\n\n## Update\n\nIt explains 112 cases.\n"
        self.assertTrue(published.check(mdx, md, CAPTURE, FIELDS))

    def test_moved_figure_fails(self):
        fig = MDX[MDX.index("<figure>"):MDX.index("</figure>") + len("</figure>")]
        mdx = MDX.replace(fig + "\n\n", "").replace("Second paragraph.", "Second paragraph.\n\n" + fig)
        self.assertTrue(published.check(mdx, MD, CAPTURE, FIELDS))

    def test_caption_must_be_the_figure_level_footnote(self):
        mdx = MDX.replace("Footnote text of chart one.", "r = -0.44")
        self.assertTrue(published.check(mdx, MD, CAPTURE, FIELDS))

    def test_published_body_shorter_than_the_draft_is_reported_not_a_crash(self):
        self.assertTrue(published.check(MDX.replace("\nSecond paragraph.\n", "\n"), MD, CAPTURE, FIELDS))

    def test_figure_missing_from_mdx_fails(self):
        mdx = MDX.split("<figure>")[0] + "Second paragraph.\n"
        self.assertTrue(published.check(mdx, MD, CAPTURE, FIELDS))


if __name__ == "__main__":
    unittest.main()


class ImagesTest(unittest.TestCase):
    """Each live image is the chart the scripts produce, found by its full path on the site."""

    def setUp(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        self.d = tempfile.mkdtemp(prefix="pub-images-")
        self.addCleanup(shutil.rmtree, self.d, True)
        for rel, text in (("charts/c-1.png", "current"), ("public/images/blog/c-1.png", "current"),
                          ("public/images/blog/old/c-1.png", "stale")):
            os.makedirs(os.path.dirname(os.path.join(self.d, rel)), exist_ok=True)
            fig, ax = plt.subplots(figsize=(2, 1))
            ax.text(0.1, 0.5, text, fontsize=20)
            fig.savefig(os.path.join(self.d, rel), dpi=40, metadata={"Software": None})
            plt.close(fig)
        self.cfg = SimpleNamespace(site_public=os.path.join(self.d, "public"), mdx=None,
                                   chart_dir=os.path.join(self.d, "charts"))

    def fig(self, src):
        return [{"src": src, "file": src.rsplit("/", 1)[-1], "alt": "", "caption": ""}]

    def test_the_image_the_page_actually_links_is_compared(self):
        # review of v2: with the folder configured only the basename was used, so a page linking a stale
        # copy under another path passed
        self.assertEqual(published._images(self.fig("/images/blog/c-1.png"), self.cfg), [])
        self.assertTrue(published._images(self.fig("/images/blog/old/c-1.png"), self.cfg))
