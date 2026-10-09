"""The command line accepts the README's own usage, the config refuses what it cannot honour, and a
crash inside any check is reported as a problem instead of killing the run."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

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
