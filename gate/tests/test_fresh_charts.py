"""fresh and charts, on a miniature post built in a temp directory."""

import hashlib
import os
import shutil
import tempfile
import unittest

from gate.checks import charts, fresh, numbers
from gate.config import load

BUILD = '''import json, os
here = os.path.dirname(os.path.abspath(__file__))
json.dump({"demo": {"r": 0.5, "n": 3, "sample": "abc"}}, open(os.path.join(here, "results.json"), "w"))
'''
CHARTS = '''import json, os
import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(here, "results.json")))
d = R["demo"]
fig, ax = plt.subplots()
ax.scatter([1, 2, 3], [1, 2, 3])
ax.text(0.1, 0.9, f"r = {d['r']:+.2f}   n = {d['n']}", transform=ax.transAxes)
ax.set_title("A small chart")
os.makedirs(os.path.join(here, "charts"), exist_ok=True)
fig.savefig(os.path.join(here, "charts", "demo-1.png"), dpi=50, metadata={"Software": None})
'''
TOML = '''[post]
slug = "demo"
source = "draft/demo.src.md"
rendered = "draft/demo.md"
results = "results.json"
build = ["build_analysis.py"]
charts = "make_charts.py"
'''


def make_post(build=BUILD, charts_src=CHARTS):
    d = tempfile.mkdtemp(prefix="minipost-")
    for name, body in (("build_analysis.py", build), ("make_charts.py", charts_src), ("gate.toml", TOML)):
        with open(os.path.join(d, name), "w") as f:
            f.write(body)
    os.makedirs(os.path.join(d, "draft"))
    os.makedirs(os.path.join(d, "charts"))
    import subprocess, sys
    for s in ("build_analysis.py", "make_charts.py"):
        subprocess.run([sys.executable, s], cwd=d, check=True, env={**os.environ, "MPLBACKEND": "Agg"})
    return d


def tree_hash(d):
    h = hashlib.sha256()
    if os.path.isfile(d):
        with open(d, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    for root, _, files in sorted(os.walk(d)):
        for f in sorted(files):
            p = os.path.join(root, f)
            with open(p, "rb") as fh:
                h.update(p.encode()); h.update(fh.read())
    return h.hexdigest()


class FreshTest(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree(getattr(self, "d", ""), ignore_errors=True)

    def test_clean_post_passes_and_captures_text(self):
        self.d = make_post()
        fails, cap = fresh.check(load(self.d))
        self.assertEqual(fails, [])
        self.assertEqual(cap[0]["axes"][0]["points"], 3)
        self.assertTrue(any("n = 3" in t for t in cap[0]["texts"]))

    def test_chart_script_that_expects_its_committed_folder_still_runs(self):
        # Post 25's make_charts.py writes into charts/ without creating it, as a fresh clone allows;
        # the clean copy removed the folder itself and the build crashed instead of being checked
        self.d = make_post(charts_src=CHARTS.replace('os.makedirs(os.path.join(here, "charts"), exist_ok=True)\n', ""))
        fails, cap = fresh.check(load(self.d))
        self.assertEqual(fails, [])
        self.assertEqual(len(cap), 1)

    def test_a_chart_folder_linked_outside_the_post_is_never_emptied(self):
        # review of v2: emptying the clean copy's chart folder followed the link and deleted the real files
        self.d = make_post()
        outside = tempfile.mkdtemp(prefix="outside-images-")
        self.addCleanup(shutil.rmtree, outside, True)
        shutil.copy(os.path.join(self.d, "charts", "demo-1.png"), outside)
        with open(os.path.join(outside, "other-post-chart.png"), "wb") as f:
            f.write(b"keep me")
        shutil.rmtree(os.path.join(self.d, "charts"))
        os.symlink(outside, os.path.join(self.d, "charts"))
        fresh.check(load(self.d))
        self.assertEqual(sorted(os.listdir(outside)), ["demo-1.png", "other-post-chart.png"])

    def test_a_difference_that_changes_a_printed_figure_is_not_noise(self):
        # review of v2: 1234567891 vs 1234567890 and 0.12500000001 vs 0.125 were inside the tolerance
        self.assertTrue(fresh._json_diff({"pop": 1234567891.0}, {"pop": 1234567890.0}))
        self.assertTrue(fresh._json_diff({"x": 0.12500000001}, {"x": 0.125}))
        self.assertEqual(fresh._json_diff({"x": 0.35137588465200854}, {"x": 0.35137588465200854 * (1 + 1e-13)}), [])

    def test_a_figure_that_prints_differently_from_a_rebuild_fails_whatever_the_tolerance(self):
        # a value on a rounding boundary can flip its printed digit by less than any tolerance
        self.d = make_post(build=BUILD.replace('"r": 0.5', '"r": 0.25'))
        committed = os.path.join(self.d, "results.json")
        with open(committed) as f:
            text = f.read()
        with open(committed, "w") as f:
            f.write(text.replace("0.25", "0.25000000000000006"))
        fails, _ = fresh.check(load(self.d), templates=[("draft", "r is {{demo.r:dec1}}")])
        self.assertTrue(any("prints differently" in x for x in fails), fails)

    def test_a_chart_folder_reached_through_a_linked_parent_is_never_touched(self):
        # review of v3: only a chart folder that was itself a link was protected
        self.d = make_post()
        outside = tempfile.mkdtemp(prefix="outside-parent-")
        self.addCleanup(shutil.rmtree, outside, True)
        os.makedirs(os.path.join(outside, "charts"))
        shutil.copy(os.path.join(self.d, "charts", "demo-1.png"), os.path.join(outside, "charts"))
        with open(os.path.join(outside, "charts", "precious.txt"), "w") as f:
            f.write("keep me")
        os.symlink(outside, os.path.join(self.d, "out"))
        with open(os.path.join(self.d, "gate.toml"), "a") as f:
            f.write('chart_dir = "out/charts"\n')
        fails, _ = fresh.check(load(self.d))
        self.assertEqual(sorted(os.listdir(os.path.join(outside, "charts"))), ["demo-1.png", "precious.txt"])
        self.assertTrue(any("outside the post" in x for x in fails), fails)

    def test_gate_never_writes_into_the_post(self):
        self.d = make_post()
        before = tree_hash(self.d)
        fresh.check(load(self.d))
        self.assertEqual(tree_hash(self.d), before)

    def test_self_referencing_symlink_does_not_crash_or_leak(self):
        # Post 25's data/ held 'data -> <its own path>', created during its build; the first real
        # run of this gate crashed on it with 'too many levels of symbolic links'
        self.d = make_post()
        os.makedirs(os.path.join(self.d, "data"))
        os.symlink(os.path.join(self.d, "data"), os.path.join(self.d, "data", "data"))
        before = tree_hash(os.path.join(self.d, "charts")) + tree_hash(os.path.join(self.d, "results.json"))
        fails, _ = fresh.check(load(self.d))
        self.assertEqual(fails, [])
        self.assertEqual(tree_hash(os.path.join(self.d, "charts")) + tree_hash(os.path.join(self.d, "results.json")), before)

    def test_committed_chart_no_script_produces_fails(self):
        # attack: the clean copy was seeded with the committed charts, so an orphan chart passed
        self.d = make_post()
        shutil.copy(os.path.join(self.d, "charts", "demo-1.png"), os.path.join(self.d, "charts", "demo-2.png"))
        fails, _ = fresh.check(load(self.d))
        self.assertTrue(any("demo-2.png" in x and "no script" in x for x in fails), fails)

    def test_build_cannot_write_into_the_post_through_an_absolute_link(self):
        # review: an absolute link copied as-is still pointed into the committed post
        leak = ('if os.path.isdir(os.path.join(here, "data", "data")):\n'
                '    open(os.path.join(here, "data", "data", "leak.txt"), "w").write("x")\n')
        self.d = make_post(build=BUILD + leak)
        os.makedirs(os.path.join(self.d, "data"))
        os.symlink(os.path.join(self.d, "data"), os.path.join(self.d, "data", "data"))
        fresh.check(load(self.d))
        self.assertFalse(os.path.exists(os.path.join(self.d, "data", "leak.txt")))

    def test_stale_committed_results_fail(self):
        self.d = make_post()
        with open(os.path.join(self.d, "results.json"), "w") as f:
            f.write('{"demo": {"r": 0.9, "n": 3, "sample": "abc"}}')
        fails, _ = fresh.check(load(self.d))
        self.assertTrue(any("results.json" in x and "differs" in x for x in fails))

    def test_last_bit_float_noise_is_tolerated(self):
        # an OS upgrade moved Post 25's regression outputs by 1 part in 1e13; that is not staleness
        self.d = make_post(build=BUILD.replace('"r": 0.5', '"r": 0.5 + 3e-14'))
        with open(os.path.join(self.d, "results.json"), "w") as f:
            f.write('{"demo": {"r": 0.5, "n": 3, "sample": "abc"}}')
        fails, _ = fresh.check(load(self.d))
        self.assertFalse(any("results.json" in x for x in fails), fails)

    def test_changed_annotation_in_committed_chart_fails(self):
        self.d = make_post()
        alt = make_post(charts_src=CHARTS.replace("n = {d['n']}", "n = 250"))
        shutil.copy(os.path.join(alt, "charts", "demo-1.png"), os.path.join(self.d, "charts", "demo-1.png"))
        shutil.rmtree(alt, ignore_errors=True)
        fails, _ = fresh.check(load(self.d))
        self.assertTrue(any("demo-1.png" in x and "pixels changed" in x for x in fails), fails)

    def test_nondeterministic_build_fails(self):
        self.d = make_post(build=BUILD.replace('"r": 0.5', '"r": int.from_bytes(os.urandom(4), "big")'))
        fails, _ = fresh.check(load(self.d))
        self.assertTrue(any("not deterministic" in x for x in fails))

    def test_failing_build_is_reported(self):
        self.d = make_post()
        with open(os.path.join(self.d, "build_analysis.py"), "a") as f:
            f.write("\nraise SystemExit('boom')\n")
        fails, _ = fresh.check(load(self.d))
        self.assertTrue(any("failed in a clean copy" in x for x in fails))


class CaptureTest(unittest.TestCase):
    """What the instrumented savefig records, on real matplotlib figures."""

    def capture(self, draw):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from gate import chart_capture
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, True)
        fig, ax = plt.subplots()
        draw(fig, ax)
        chart_capture.RECORDS.clear()
        chart_capture._spy(fig, os.path.join(d, "c.png"))
        plt.close(fig)
        return chart_capture.RECORDS[-1]

    def test_ticks_are_separated_from_prose(self):
        rec = self.capture(lambda f, a: (a.plot([0, 1], [0, 1]), a.set_title("A title")))
        self.assertIn("A title", rec["prose"])
        self.assertTrue(rec["ticks"])
        self.assertFalse(set(rec["ticks"]) & set(rec["prose"]))

    def test_table_cells_and_legends_are_captured(self):
        def draw(f, a):
            a.plot([0, 1], [0, 1], label="Every place")
            a.legend()
            a.table(cellText=[["n = 250"]], loc="bottom")
        rec = self.capture(draw)
        self.assertIn("n = 250", rec["texts"])
        self.assertIn("Every place", rec["prose"])

    def test_axis_labels_are_read_for_n(self):
        rec = self.capture(lambda f, a: (a.scatter([1, 2], [1, 2]), a.set_xlabel("Temperature, n = 196")))
        self.assertIn("Temperature, n = 196", rec["axes"][0]["texts"])

    def test_points_count_finite_scatter_and_line_markers(self):
        def draw(f, a):
            a.scatter([1, 2, float("nan")], [1, 2, 3])
            a.plot([1, 2, 3], [1, 2, 3], "o", linestyle="None")
        self.assertEqual(self.capture(draw)["axes"][0]["points"], 5)


class ChartsTest(unittest.TestCase):
    def test_a_single_panel_figure_footnote_n_must_match_its_points(self):
        # review of v2: a footnote 'n = 98' on a 97-point panel reached GATE PASSED
        cap = [{"file": "c.png", "fig_texts": ["Former colonies only, n = 98."], "axes": [{"points": 97, "texts": []}]}]
        self.assertTrue(charts.panel_counts(cap))
        cap[0]["fig_texts"] = ["Every entity with both, 97 of them."]
        self.assertEqual(charts.panel_counts(cap), [])

    def test_rates_and_names_are_not_counts(self):
        # review of v3: 'per 100,000 people', 'COVID-19 cases', 'G20 countries' were read as n
        for label in ("Deaths per 100,000 people", "COVID-19 cases per million", "G20 countries", "per 1,000 people"):
            cap = [{"file": "a.png", "axes": [{"points": 148, "texts": [label]}]}]
            with self.subTest(label=label):
                self.assertEqual(charts.panel_counts(cap), [])

    def test_a_footnote_n_is_checked_against_the_one_panel_with_points(self):
        # a colorbar is a second axes; a bar chart has no countable points
        cap = [{"file": "c.png", "fig_texts": ["n = 150"], "axes": [{"points": 148, "texts": []}, {"points": 0, "texts": []}]}]
        self.assertTrue(charts.panel_counts(cap))
        bars = [{"file": "b.png", "fig_texts": ["Means over 150 countries."], "axes": [{"points": 0, "texts": []}]}]
        self.assertEqual(charts.panel_counts(bars), [])

    def test_more_wordings_of_n(self):
        cap = [{"file": "c.png", "axes": [{"points": 160, "texts": ["across 196 former colonies"]}]}]
        self.assertTrue(charts.panel_counts(cap))

    def test_chart_figures_read_sign_words_and_bare_numbers_as_written(self):
        # review of v2: an unsigned printed number matched a result of either sign
        r = {"col": {"r": 0.294, "n": 97}, "tidy": {"r": -0.4352, "r2_share": 0.19}}
        rec = lambda t: [{"file": "c.png", "prose": [t]}]
        self.assertTrue(numbers.chart_figures(rec("r = minus 0.29"), r, {}, {}))
        self.assertTrue(numbers.chart_figures(rec("r = 0.44"), r, {}, {}))
        self.assertEqual(numbers.chart_figures(rec("-0.44 and +0.29, n = 97"), r, {}, {}), [])
        self.assertEqual(numbers.chart_figures(rec("r = minus 0.44"), r, {}, {}), [])

    def test_a_statistic_printed_with_its_n_must_be_one_result(self):
        # replay of v3: 'minus 0.29' on a +0.29 panel matched an unrelated r of -0.286 elsewhere in results
        r = {"col": {"r": 0.294, "n": 97}, "other": {"r": -0.286, "n": 50}}
        rec = lambda t: [{"file": "c.png", "prose": [t]}]
        self.assertTrue(numbers.chart_figures(rec("r = minus 0.29   n = 97"), r, {}, {}))
        self.assertEqual(numbers.chart_figures(rec("r = +0.29   n = 97"), r, {}, {}), [])
        self.assertTrue(numbers.chart_figures(rec("r = +0.29   n = 50"), r, {}, {}))

    def test_chart_figures_read_percent_as_written(self):
        r = {"tidy": {"r2_share": 0.19, "density_pct": 78.7}}
        rec = lambda t: [{"file": "c.png", "prose": [t]}]
        self.assertTrue(numbers.chart_figures(rec("0.19% of the variation"), r, {}, {}))
        self.assertEqual(numbers.chart_figures(rec("19% of the variation, the 78.7 percent mark"), r, {}, {}), [])

    def test_hardcoded_wrong_n_on_a_panel_fails(self):
        cap = [{"file": "c.png", "texts": [], "axes": [{"points": 3, "texts": ["r = +0.50   n = 4"]}]}]
        self.assertTrue(charts.panel_counts(cap))

    def test_n_printed_on_a_panel_with_nothing_countable_fails(self):
        cap = [{"file": "c.png", "texts": [], "axes": [{"points": 0, "texts": ["N = 250"]}]}]
        self.assertTrue(charts.panel_counts(cap))

    def test_other_wordings_of_n_are_read(self):
        cap = [{"file": "c.png", "texts": [], "axes": [{"points": 97, "texts": ["across 98 countries"]}]}]
        self.assertTrue(charts.panel_counts(cap))

    def test_matching_n_passes(self):
        cap = [{"file": "c.png", "texts": [], "axes": [{"points": 97, "texts": ["r = +0.29   n = 97", ""]}]}]
        self.assertEqual(charts.panel_counts(cap), [])

    def test_hand_typed_chart_figures_are_found(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, True)
        p = os.path.join(d, "make_charts.py")
        with open(p, "w") as f:
            f.write('"""Charts, 4 of them."""\nR = {}\nax.text(0, 0, "on raw dollars r is -0.39")\n'
                    'ax.text(0, 0, f"r = {R[\'tidy_story\']:+.2f}")\nfig.savefig("charts/rf-1-a.png")\n'
                    'x = R["density_1500|income_2023|all"]\ncolor = "#2a78d6"\n')
        with open(p, "a") as f:
            f.write('assert ok, "chart 4 has no display name"\nraise SystemExit("needs 3 inputs")\n')
        lits = charts.literal_strings(p)
        self.assertFalse(any("chart 4" in v or "3 inputs" in v for v in lits.values()))
        self.assertTrue(any("-0.39" in v for v in lits.values()))
        self.assertFalse(any("2023" in v or "rf-1" in v or "2a78d6" in v or "4 of them" in v for v in lits.values()))
        self.assertTrue(numbers.check("", [], {}, extra=lits))


if __name__ == "__main__":
    unittest.main()
