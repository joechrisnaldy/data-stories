"""Rounds cannot close with an errored lens, an unresolved finding, a skipped or repeated number, or an
unaccounted scope; nothing publishes after a dirty round or any unchecked change to any input. These
encode the hard rule the owner adopted on 2026-10-09 and the attacks made on its first version."""

import json
import os
import shutil
import tempfile
import unittest

from gate import rounds
from gate.config import load

TOML = ('[post]\nslug="d"\nsource="draft/d.src.md"\nrendered="draft/d.md"\nresults="results.json"\nbuild=["b.py"]\n'
        'charts="c.py"\nmdx="p.mdx"\n')


def finding(fid="A1", verdict="CONFIRMED", fixed=False, evidence="results.json tidy_story.r = -0.4352"):
    return {"id": fid, "verdict": verdict, "evidence": evidence, "fixed": fixed}


class RoundsTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)
        os.makedirs(os.path.join(self.d, "draft"))
        os.makedirs(os.path.join(self.d, "docs"))
        for name, body in (("gate.toml", TOML), ("draft/d.src.md", "First sentence. Second sentence."),
                           ("draft/d.md", "x"), ("results.json", "{}"), ("b.py", "pass\n"), ("c.py", "pass\n"),
                           ("p.mdx", "---\ntitle: x\n---\n")):
            with open(os.path.join(self.d, name), "w") as f:
                f.write(body)
        self.src = os.path.join(self.d, "draft", "d.src.md")
        self.cfg = load(self.d)

    def write(self, rel, body):
        with open(os.path.join(self.d, rel), "w") as f:
            f.write(body)

    def verdicts(self, n, findings, d=4, r=4, e=0, scope=None):
        v = {"round": n, "lenses_dispatched": d, "lenses_returned": r, "lenses_errored": e, "findings": findings}
        if scope is not None:
            v["scope"] = scope
        self.write(f"docs/round{n}-verdicts.json", json.dumps(v))

    def close(self, n, findings, **kw):
        self.verdicts(n, findings, **kw)
        return rounds.close_round(self.cfg, n, gate_passed=True)

    def test_scope_lists_only_changed_sentences(self):
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "First sentence. Second sentence, now changed. A new one.")
        self.assertEqual(rounds.scope(self.cfg, 1), ["Second sentence, now changed.", "A new one."])

    def test_scope_respects_paragraphs(self):
        self.write("draft/d.src.md", "Intro.\n\n## Heading\n\nBody.")
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "Intro.\n\n## Heading\n\nBody changed.")
        self.assertEqual(rounds.scope(self.cfg, 1), ["Body changed."])

    def test_snapshot_is_never_overwritten(self):
        rounds.snapshot(self.cfg, 1)
        with self.assertRaises(rounds.RoundError):
            rounds.snapshot(self.cfg, 1)

    def test_clean_round_closes_and_permits_publishing(self):
        rounds.snapshot(self.cfg, 1)
        self.assertTrue(self.close(1, [finding()])["clean"])
        self.assertEqual(rounds.publish_check(self.cfg, gate_passed=True), [])

    def test_cannot_close_on_a_red_gate(self):
        rounds.snapshot(self.cfg, 1)
        self.verdicts(1, [finding()])
        with self.assertRaises(rounds.RoundError):
            rounds.close_round(self.cfg, 1, gate_passed=False)

    def test_round_needs_its_snapshot(self):
        with self.assertRaises(rounds.RoundError):
            self.close(1, [finding()])

    def test_errored_or_unaccounted_lens_blocks(self):
        rounds.snapshot(self.cfg, 1)
        for d, r, e in ((4, 3, 1), (4, 3, 0)):
            with self.assertRaises(rounds.RoundError):
                self.close(1, [finding()], d=d, r=r, e=e)

    def test_unverified_hollow_or_unfixed_findings_block(self):
        rounds.snapshot(self.cfg, 1)
        for bad in (finding(verdict="UNVERIFIED"), finding(evidence="checked"), finding(verdict="REFUTED")):
            with self.assertRaises(rounds.RoundError, msg=bad):
                self.close(1, [bad])

    def test_a_round_with_no_findings_is_not_a_round(self):
        rounds.snapshot(self.cfg, 1)
        with self.assertRaises(rounds.RoundError):
            self.close(1, [])

    def test_round_with_fixes_does_not_permit_publishing(self):
        rounds.snapshot(self.cfg, 1)
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        self.assertTrue(any("round 2" in x for x in rounds.publish_check(self.cfg, True)))

    def test_closing_an_old_round_again_cannot_launder_an_edit(self):
        # attack: round 1 clean, round 2 dirty, then 'close-round 1' again unlocked publishing
        rounds.snapshot(self.cfg, 1)
        self.close(1, [finding()])
        with self.assertRaises(rounds.RoundError):
            self.close(1, [finding()])

    def test_round_numbers_cannot_skip(self):
        rounds.snapshot(self.cfg, 1)
        rounds.snapshot(self.cfg, 3)
        with self.assertRaises(rounds.RoundError):
            self.close(3, [finding()])

    def test_later_round_must_account_for_its_scope(self):
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "First sentence. Second sentence, fixed.")
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        rounds.snapshot(self.cfg, 2)
        with self.assertRaises(rounds.RoundError):
            self.close(2, [finding()], scope=[])
        self.assertTrue(self.close(2, [finding()], scope=["Second sentence, fixed."])["clean"])

    def test_a_clean_round_cannot_hide_an_edit_made_during_it(self):
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "First sentence. A quiet edit.")
        with self.assertRaises(rounds.RoundError):
            self.close(1, [finding()])

    def test_any_input_changing_after_the_last_round_blocks_publishing(self):
        # attack: the lock hashed only the draft, so an analysis-code change after the round published
        for rel in ("draft/d.src.md", "results.json", "b.py", "gate.toml"):
            with self.subTest(rel=rel):
                self.setUp()
                rounds.snapshot(self.cfg, 1)
                self.close(1, [finding()])
                with open(os.path.join(self.d, rel), "a") as f:
                    f.write("\n# changed\n")
                self.assertTrue(rounds.publish_check(self.cfg, True), rel)

    def test_a_clean_round_cannot_hide_a_code_or_results_change_made_during_it(self):
        # review of v2: only the template was compared, so a round in which the build changed closed clean
        for rel in ("b.py", "results.json"):
            with self.subTest(rel=rel):
                self.setUp()
                rounds.snapshot(self.cfg, 1)
                with open(os.path.join(self.d, rel), "a") as f:
                    f.write("\n")
                with self.assertRaises(rounds.RoundError):
                    self.close(1, [finding()])

    def test_a_figure_changed_by_code_enters_the_next_scope(self):
        # review of v2: a code-only fix left the template unchanged, so round 2's scope was empty
        self.write("draft/d.src.md", "First sentence. It is {{x.r:dec2}} now.")
        self.write("results.json", json.dumps({"x": {"r": 0.44}}))
        rounds.snapshot(self.cfg, 1)
        self.write("results.json", json.dumps({"x": {"r": 0.61}}))
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        self.assertEqual(rounds.scope(self.cfg, 1), ["It is 0.61 now."])
        rounds.snapshot(self.cfg, 2)
        with self.assertRaises(rounds.RoundError):
            self.close(2, [finding()], scope=[])
        self.assertTrue(self.close(2, [finding()], scope=["It is 0.61 now."])["clean"])

    def test_a_missing_earlier_snapshot_is_an_error_not_a_skip(self):
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "First sentence. Second sentence, fixed.")
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        os.remove(os.path.join(self.d, "draft", ".rounds", "1.json"))
        rounds.snapshot(self.cfg, 2)
        with self.assertRaises(rounds.RoundError):
            self.close(2, [finding()])

    def test_publishing_needs_charts_and_the_mdx_configured(self):
        # a check that is SKIPPED at draft stage cannot be skipped at publish time
        for key in ('charts="c.py"\n', 'mdx="p.mdx"\n'):
            with self.subTest(key=key):
                self.setUp()
                self.write("gate.toml", TOML.replace(key, ""))
                self.cfg = load(self.d)
                rounds.snapshot(self.cfg, 1)
                self.close(1, [finding()])
                self.assertTrue(rounds.publish_check(self.cfg, True))

    def test_no_round_at_all_blocks_publishing(self):
        self.assertTrue(rounds.publish_check(self.cfg, True))


if __name__ == "__main__":
    unittest.main()
