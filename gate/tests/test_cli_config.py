"""The command line accepts the README's own usage, the config refuses what it cannot honour, and a
crash inside any check is reported as a problem instead of killing the run."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from gate import rounds
from gate.config import ConfigError, load

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = '[post]\nslug="d"\nsource="draft/d.src.md"\nrendered="draft/d.md"\nresults="results.json"\nbuild=["b.py"]\n'


def gate(*args):
    # a manual run with the self-test skipped (which also prevents recursion), even when these tests are
    # themselves running inside the self-test
    env = {k: v for k, v in os.environ.items() if k != "GATE_IN_SELFTEST"}
    return subprocess.run([sys.executable, "-m", "gate", *args], cwd=HERE, capture_output=True, text=True,
                          env={**env, "GATE_SKIP_SELFTEST": "1"})


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)

    def write(self, body):
        with open(os.path.join(self.d, "gate.toml"), "w") as f:
            f.write(body)
        return self.d

    def test_misspelt_key_is_refused_not_ignored(self):
        # 'chart' instead of 'charts' used to switch the chart checks off silently
        with self.assertRaises(ConfigError):
            load(self.write(BASE + 'chart = "make_charts.py"\n'))

    def test_restricted_inputs_is_a_list_of_source_names(self):
        for bad in ('"AEI"', '[""]', "[1]", '["AEI", " "]'):
            with self.subTest(bad=bad), self.assertRaises(ConfigError):
                load(self.write(BASE + f"restricted_inputs = {bad}\n"))
        self.assertEqual(load(self.write(BASE + 'restricted_inputs = ["AEI"]\n')).restricted_inputs, ("AEI",))
        self.assertEqual(load(self.write(BASE)).restricted_inputs, ())

    def test_build_must_be_a_list(self):
        with self.assertRaises(ConfigError):
            load(self.write(BASE.replace('build=["b.py"]', 'build="b.py"')))

    def test_malformed_toml_is_a_config_error_not_a_traceback(self):
        with self.assertRaises(ConfigError):
            load(self.write("[post\nslug="))

    def test_extra_entries_must_be_pairs_of_paths(self):
        # review of v2: extra = [[1, 2]] crashed with a TypeError traceback
        with self.assertRaises(ConfigError):
            load(self.write(BASE + "extra = [[1, 2]]\n"))

    def test_every_path_is_absolute(self):
        rel = os.path.relpath(self.write(BASE), os.getcwd())
        self.assertTrue(os.path.isabs(load(rel).source))


class CliTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)
        os.makedirs(os.path.join(self.d, "draft"))
        with open(os.path.join(self.d, "gate.toml"), "w") as f:
            f.write(BASE)
        for rel, body in (("draft/d.src.md", "Text."), ("draft/d.md", "Text."), ("results.json", "{}"),
                          ("b.py", "import json, os\njson.dump({}, open(os.path.join(os.path.dirname("
                                   "os.path.abspath(__file__)), 'results.json'), 'w'))\n")):
            with open(os.path.join(self.d, rel), "w") as f:
                f.write(body)

    def test_snapshot_takes_post_then_round_as_documented(self):
        r = gate("snapshot", self.d, "1")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(os.path.join(self.d, "draft", ".rounds", "1.json")))

    def test_scope_takes_post_then_since(self):
        gate("snapshot", self.d, "1")
        r = gate("scope", self.d, "--since", "1")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def put(self, rel, body):
        os.makedirs(os.path.dirname(os.path.join(self.d, rel)), exist_ok=True)
        with open(os.path.join(self.d, rel), "w") as f:
            f.write(body)

    def close(self, n, scope=None):
        """Close round n in this process: the close-round command would run the whole gate on this stub post."""
        v = {"round": n, "lenses_dispatched": 4, "lenses_returned": 4, "lenses_errored": 0, "findings": [
            {"id": "A1", "verdict": "REFUTED", "evidence": "results.json tidy_story.r = -0.4352", "fixed": True}]}
        self.put(f"docs/round{n}-verdicts.json", json.dumps({**v, **({} if scope is None else {"scope": scope})}))
        rounds.close_round(load(self.d), n, gate_passed=True)

    def round_1_fixed_a_sentence_and_a_chart(self):
        self.put("draft/d.src.md", "First sentence. Second sentence. Third sentence.")
        self.put("charts/c1.png", "one")
        rounds.snapshot(load(self.d), 1)
        self.put("draft/d.src.md", "First sentence. Second sentence, fixed and long.")
        self.put("charts/c1.png", "one, redrawn")
        self.close(1)

    def two_rounds_then_a_cut_and_a_redrawn_chart(self):
        self.round_1_fixed_a_sentence_and_a_chart()
        rounds.snapshot(load(self.d), 2)
        self.close(2, scope=["Second sentence, fixed and long."])
        self.put("draft/d.src.md", "First sentence. Second sentence, fixed.")
        self.put("charts/c1.png", "one, redrawn twice")

    def test_scope_names_changed_charts_and_writes_the_round_inventory(self):
        self.round_1_fixed_a_sentence_and_a_chart()
        out = os.path.join(self.d, "inventory.json")
        r = gate("scope", self.d, "--since", "1", "--json", out)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)           # round 2 has no snapshot to list from yet
        self.assertIn("no snapshot for round 2", r.stdout)
        self.assertFalse(os.path.exists(out))
        gate("snapshot", self.d, "2")
        r = gate("scope", self.d, "--since", "1", "--json", out)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("  - Second sentence, fixed and long.", r.stdout)
        self.assertIn("2 sentence(s) moved or deleted since round 1:\n  - [deleted] Second sentence.\n"
                      "  - [deleted] Third sentence.", r.stdout)
        self.assertIn("1 chart file(s) changed since round 1:\n  - charts/c1.png", r.stdout)
        with open(out) as f:
            self.assertEqual([x["text"] for x in json.load(f)], [
                "Second sentence, fixed and long.", "[deleted] Second sentence.", "[deleted] Third sentence.",
                "[chart] charts/c1.png"])

    def test_scope_does_not_call_an_input_change_it_cannot_place_a_chart(self):
        # attack of 2026-11-16: on a post whose snapshot predates per-file hashes, any input change was printed as
        # "1 chart file(s) changed" although no chart had moved
        self.put("charts/c1.png", "one")
        path = rounds.snapshot(load(self.d), 1)
        with open(path) as f:
            snap = json.load(f)
        del snap["outputs"]
        self.put("draft/.rounds/1.json", json.dumps(snap))
        self.assertIn("0 chart file(s) changed since round 1", gate("scope", self.d, "--since", "1").stdout)
        self.put("results.json", "{ }")
        r = gate("scope", self.d, "--since", "1")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("chart file(s) changed", r.stdout)
        self.assertIn("an input changed since round 1; that snapshot predates per-file hashes, so which input, and "
                      "whether a chart, is not known", r.stdout)

    def test_changed_lists_each_row_and_writes_json(self):
        self.two_rounds_then_a_cut_and_a_redrawn_chart()
        out = os.path.join(self.d, "changed.json")
        r = gate("changed", self.d, "--json", out)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("2 change(s) since the snapshot round 2 started from, 2 not settled", r.stdout)
        self.assertIn("  [0] cut, not read: Second sentence, fixed.\n        cut of: Second sentence, fixed and long.",
                      r.stdout)
        self.assertIn("  [1] changed, not accepted: charts/c1.png", r.stdout)
        with open(out) as f:
            got = json.load(f)
        self.assertEqual((got["round"], [(x["index"], x["kind"], x["state"]) for x in got["rows"]]),
                         (2, [(0, "sentence", "cut, not read"), (1, "chart", "changed, not accepted")]))

    def test_accept_records_the_owners_words_for_one_row(self):
        self.two_rounds_then_a_cut_and_a_redrawn_chart()
        r = gate("accept", self.d, "--index", "1", "--starts", "charts/c9.png", "--owner", "yes, the redrawn chart stands")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)           # not what row 1 opens with
        self.assertIn("accept: RoundError: row 1 does not open with", r.stdout)
        r = gate("accept", self.d, "--index", "1", "--starts", "charts/c1.png", "--owner",
                 "yes, the redrawn chart stands", "--date", "2026-11-16")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("accepted [1] charts/c1.png", r.stdout)
        r = gate("accept", self.d, "--index", "0", "--starts", "Second sentence, fixed.", "--owner", "fine, keep the cut")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)           # the day defaults to today
        after = gate("changed", self.d).stdout
        self.assertIn("  [0] accepted: Second sentence, fixed.", after)
        self.assertIn("2 change(s) since the snapshot round 2 started from, 0 not settled", after)
        self.assertIn("  [1] accepted: charts/c1.png", gate("changed", self.d).stdout)
        with open(os.path.join(self.d, "docs", "after-round2.json")) as f:
            entry = json.load(f)["accepted"][0]
        self.assertEqual((entry["owner"], entry["date"], entry["kind"]),
                         ("yes, the redrawn chart stands", "2026-11-16", "chart"))

    def test_changed_says_round_2_is_needed_after_round_1_and_lists_a_new_surface(self):
        self.round_1_fixed_a_sentence_and_a_chart()
        self.assertIn("after round 1 every change needs round 2", gate("changed", self.d).stdout)
        self.put("p.mdx", "---\ntitle: x\n---\n")
        self.put("gate.toml", BASE + 'mdx="p.mdx"\n[published]\nexcerpt="Hello there."\n')
        r = gate("changed", self.d)
        self.assertIn("  new surface, covered by no round: [published] excerpt", r.stdout, r.stdout + r.stderr)

    def test_changed_and_accept_without_a_closed_round_are_errors_not_tracebacks(self):
        gate("snapshot", self.d, "1")
        for args in (("changed", self.d), ("accept", self.d, "--index", "0", "--starts", "Text.", "--owner", "ok then")):
            with self.subTest(cmd=args[0]):
                r = gate(*args)
                self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
                self.assertIn("no fact-check round has been closed", r.stdout)
                self.assertNotIn("Traceback", r.stdout + r.stderr)

    def test_unknown_command_is_an_error_not_a_silent_check(self):
        r = gate("publish_check", self.d)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("GATE PASSED", r.stdout)

    def test_a_run_without_the_self_test_never_passes(self):
        # review of v2: GATE_SKIP_SELFTEST printed 'self-test SKIPPED' and then GATE PASSED
        r = gate("check", self.d)
        self.assertIn("links", r.stdout, r.stdout + r.stderr)
        self.assertNotIn("GATE PASSED", r.stdout)
        self.assertNotEqual(r.returncode, 0)

    def test_a_broken_charts_script_is_a_reported_problem_not_a_traceback(self):
        # review of v2: a syntax error in the charts script killed the run with no verdict
        with open(os.path.join(self.d, "gate.toml"), "a") as f:
            f.write('charts = "c.py"\n')
        with open(os.path.join(self.d, "c.py"), "w") as f:
            f.write("def broken(:\n")
        r = gate("check", self.d)
        self.assertNotIn("Traceback", r.stdout + r.stderr)
        self.assertIn("GATE FAILED", r.stdout)
        self.assertIn("links", r.stdout)

    def test_missing_results_is_reported_not_a_traceback(self):
        os.remove(os.path.join(self.d, "results.json"))
        r = gate("check", self.d)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("Traceback", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
