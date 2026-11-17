"""Rounds cannot close with an errored lens, an unresolved finding, a skipped or repeated number, or an
unaccounted scope (the owner's rule of 2026-10-09 and the attacks made on its first version). Publishing
follows the owner's rule of 2026-11-16, two rounds and then cuts only: whatever a reader would find changed
since the snapshot the last closed round started from needs round 2 after round 1, and after round 2 a
recorded read (a cut, a deletion) or the owner's acceptance of that one item."""

import itertools
import json
import os
import random
import shutil
import subprocess
import tempfile
import unittest
import unittest.mock

from gate import rounds
from gate.checks import style
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

    def test_a_snapshot_is_not_taken_once_the_rounds_verdicts_exist(self):
        # attack of 2026-11-16: the panel ran with no snapshot, its fixes were applied, and a snapshot taken at
        # close time held the fixed text, so nothing differed from it and the post could publish after one round
        self.verdicts(1, [finding(verdict="REFUTED", fixed=True)])
        self.write("draft/d.src.md", "First sentence. Second sentence, fixed.")
        with self.assertRaisesRegex(rounds.RoundError, "before the panel reads the post"):
            rounds.snapshot(self.cfg, 1)
        self.assertFalse(os.path.exists(os.path.join(self.d, "draft", ".rounds", "1.json")))
        with self.assertRaisesRegex(rounds.RoundError, "run the round again"):
            rounds.close_round(self.cfg, 1, gate_passed=True)
        self.assertTrue(rounds.publish_check(self.cfg, True))

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

    def test_a_reader_facing_change_after_the_last_round_blocks_publishing(self):
        # was "any input changing": a build or config change that moves nothing a reader sees is the fresh
        # check's job now (gate_passed), not this lock's
        def edit(): self.write("draft/d.src.md", "First sentence. Second sentence. A late one.")
        def cut(): self.write("draft/d.src.md", "First sentence. Second.")
        def delete(): self.write("draft/d.src.md", "First sentence.")
        def redraw(): self.chart("c1.png", "one, redrawn")
        def add_chart(): self.chart("c2.png", "two")
        def drop_chart(): os.remove(os.path.join(self.d, "charts", "c1.png"))
        for change in (edit, cut, delete, redraw, add_chart, drop_chart):
            with self.subTest(change=change.__name__):
                self.setUp()
                self.chart("c1.png", "one")
                rounds.snapshot(self.cfg, 1)
                self.close(1, [finding()])
                self.assertEqual(rounds.publish_check(self.cfg, True), [])
                change()
                self.blocked("run round 2")

    def test_a_results_change_blocks_through_the_sentence_it_moves(self):
        self.write("draft/d.src.md", "First sentence. It is {{x.r:dec2}} now.")
        self.write("results.json", json.dumps({"x": {"r": 0.44}}))
        rounds.snapshot(self.cfg, 1)
        self.close(1, [finding()])
        self.write("results.json", json.dumps({"x": {"r": 0.44}, "unused": 1}))   # moves nothing a reader sees
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.write("results.json", json.dumps({"x": {"r": 0.61}}))
        self.blocked("run round 2")

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

    # --- what changed since a snapshot (two rounds, then cuts only) ---

    def chart(self, name, body):
        os.makedirs(os.path.join(self.d, "charts"), exist_ok=True)
        with open(os.path.join(self.d, "charts", name), "w") as f:
            f.write(body)

    def test_a_snapshot_stores_the_hash_of_each_chart(self):
        self.chart("c1.png", "one")
        snap = json.load(open(rounds.snapshot(self.cfg, 1)))
        self.assertEqual(list(snap["outputs"]), ["charts/c1.png"])
        self.assertEqual(len(snap["outputs"]["charts/c1.png"]), 64)

    def test_changed_since_lists_cuts_new_words_and_charts(self):
        self.chart("c1.png", "one")
        self.chart("c2.png", "two")
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "First. Second sentence, with a new clause.")
        self.chart("c1.png", "one, redrawn")
        os.remove(os.path.join(self.d, "charts", "c2.png"))
        self.chart("c3.png", "three")
        self.assertEqual(rounds.changed_since(self.cfg, 1), {
            "sentences": [{"sentence": "First.", "cut_of": "First sentence.", "kind": "cut"},
                          {"sentence": "Second sentence, with a new clause.", "cut_of": None, "kind": "new"}],
            "deleted": ["Second sentence."],                   # rewritten: the old sentence is gone, and is listed
            "charts": ["charts/c1.png", "charts/c2.png", "charts/c3.png"], "new_surfaces": []})

    def test_no_change_lists_nothing_and_a_whole_deletion_is_listed(self):
        rounds.snapshot(self.cfg, 1)
        empty = {"sentences": [], "deleted": [], "charts": [], "new_surfaces": []}
        self.assertEqual(rounds.changed_since(self.cfg, 1), empty)
        self.write("draft/d.src.md", "First sentence.")
        self.assertEqual(rounds.changed_since(self.cfg, 1), {**empty, "deleted": ["Second sentence."]})

    def test_a_moved_or_repeated_sentence_is_a_change(self):
        self.write("draft/d.src.md", "Renters came out ahead. That was true in most years.\n\nBuyers who sold early lost money.")
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "Renters came out ahead.\n\nBuyers who sold early lost money. That was true in most years.")
        got = rounds.changed_since(self.cfg, 1)                # a swap: either sentence may be reported as the mover
        self.assertEqual(([r["kind"] for r in got["sentences"]], got["deleted"]), (["moved"], []))
        self.write("draft/d.src.md", "Renters came out ahead. That was true in most years.\n\n"
                                     "Buyers who sold early lost money. Renters came out ahead.")
        self.assertEqual(rounds.changed_since(self.cfg, 1)["sentences"],
                         [{"sentence": "Renters came out ahead.", "cut_of": None, "kind": "moved"}])

    def test_a_sentence_added_beside_its_standing_source_is_new_not_a_cut(self):
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "First sentence. Second sentence. Second.")
        self.assertEqual(rounds.changed_since(self.cfg, 1)["sentences"],
                         [{"sentence": "Second.", "cut_of": None, "kind": "new"}])

    def test_a_cut_is_looked_for_where_the_sentence_stood(self):
        # attack of 2026-11-16: new words elsewhere on the surface that happen to occur, in order, in a deleted
        # sentence were called a cut of it, so the deleted sentence had no row and nobody read its paragraph
        self.write("draft/d.src.md", "Alpha one two three four. Bravo stays here.\n\nCharlie stays too. Delta five six.")
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "Bravo stays here.\n\nCharlie stays too. Delta five six. One four.")
        got = rounds.changed_since(self.cfg, 1)
        self.assertEqual((got["sentences"], got["deleted"]),
                         ([{"sentence": "One four.", "cut_of": None, "kind": "new"}], ["Alpha one two three four."]))
        self.write("draft/d.src.md", "Bravo stays here. Alpha one four.\n\nCharlie stays too. Delta five six.")
        got = rounds.changed_since(self.cfg, 1)                # cut AND moved: new words there, a deletion here
        self.assertEqual((got["sentences"], got["deleted"]),
                         ([{"sentence": "Alpha one four.", "cut_of": None, "kind": "new"}], ["Alpha one two three four."]))
        self.write("draft/d.src.md", "Alpha one four. Bravo stays here.\n\nCharlie stays too. Delta five six.")
        self.assertEqual(rounds.changed_since(self.cfg, 1)["sentences"],
                         [{"sentence": "Alpha one four.", "cut_of": "Alpha one two three four.", "kind": "cut"}])

    def test_a_reference_entry_is_one_unit(self):
        # attack of 2026-11-16: split into sentences, a reference entry became fragments such as '(2026).' that repeat
        # across entries, so a corrected year showed as a fragment that 'moved' and the owner could accept nothing by name
        body = "First sentence (Gimbel & Lee, 2025).\n\n"
        refs = ("## References\n\nGimbel, M., & Lee, M. (2025). *Evaluating the impact.* Brookings.\n\n"
                "U.S. Bureau of Labor Statistics. (2026). *Consumer expenditures.* U.S. Department of Labor.")
        self.write("draft/d.src.md", body + refs)
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", (body + refs).replace("2025", "2026"))
        cite = "First sentence (Gimbel & Lee, 2026)."
        entry = "Gimbel, M., & Lee, M. (2026). *Evaluating the impact.* Brookings."
        got = rounds.changed_since(self.cfg, 1)
        self.assertEqual(got["sentences"], [{"sentence": cite, "cut_of": None, "kind": "new"},
                                            {"sentence": entry, "cut_of": None, "kind": "new"}])
        self.assertEqual(got["deleted"], [cite.replace("2026", "2025"), entry.replace("2026", "2025")])
        self.assertEqual(rounds.scope(self.cfg, 1), [cite, entry])
        self.write("draft/d.src.md", body)                                          # the list is gone, heading and all
        self.assertEqual(rounds.changed_since(self.cfg, 1)["deleted"], ["## References", entry.replace("2026", "2025"),
                         "U.S. Bureau of Labor Statistics. (2026). *Consumer expenditures.* U.S. Department of Labor."])
        self.write("draft/d.src.md", body + refs.replace(" Brookings.", ""))        # an entry that lost its last part
        self.assertEqual(rounds.changed_since(self.cfg, 1)["sentences"], [{
            "sentence": "Gimbel, M., & Lee, M. (2025). *Evaluating the impact.*", "kind": "cut",
            "cut_of": "Gimbel, M., & Lee, M. (2025). *Evaluating the impact.* Brookings."}])

    def test_one_gone_sentence_is_the_source_of_one_cut(self):
        self.write("draft/d.src.md", "Alpha beta gamma delta.")
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "Alpha beta. Gamma delta.")
        self.assertEqual([r["kind"] for r in rounds.changed_since(self.cfg, 1)["sentences"]], ["cut", "new"])

    def test_a_cut_that_fits_two_gone_sentences_is_of_the_first(self):
        self.write("draft/d.src.md", "Alpha beta gamma. Alpha beta gamma delta.")
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "Alpha beta.")
        got = rounds.changed_since(self.cfg, 1)
        self.assertEqual((got["sentences"], got["deleted"]), (
            [{"sentence": "Alpha beta.", "cut_of": "Alpha beta gamma.", "kind": "cut"}], ["Alpha beta gamma delta."]))

    def test_a_cut_is_judged_within_its_own_surface(self):
        self.write("gate.toml", TOML + '[published]\nexcerpt="Second sentence."\n')
        self.cfg = load(self.d)
        rounds.snapshot(self.cfg, 1)
        self.write("gate.toml", TOML + '[published]\nexcerpt="First."\n')      # a cut of the DRAFT's sentence only
        self.cfg = load(self.d)
        self.assertEqual(rounds.changed_since(self.cfg, 1)["sentences"],
                         [{"sentence": "[[published] excerpt] First.", "cut_of": None, "kind": "new"}])

    def test_a_new_surface_is_listed(self):
        rounds.snapshot(self.cfg, 1)
        self.write("gate.toml", TOML + '[published]\nexcerpt="Hello there."\n')
        self.cfg = load(self.d)
        self.assertEqual(rounds.changed_since(self.cfg, 1)["new_surfaces"], ["[published] excerpt"])

    def test_a_snapshot_from_before_per_file_hashes_falls_back_to_the_manifest(self):
        path = rounds.snapshot(self.cfg, 1)
        snap = json.load(open(path))
        del snap["outputs"]                                   # the shape of every snapshot written before this change
        json.dump(snap, open(path, "w"))
        self.assertEqual(rounds.changed_since(self.cfg, 1)["charts"], [])
        self.write("b.py", "pass\n# moved\n")
        self.assertEqual(rounds.changed_since(self.cfg, 1)["charts"],
                         ["(an input changed; this snapshot predates per-file hashes)"])

    def test_a_closed_rounds_snapshot_cannot_be_retaken_or_edited(self):
        path = rounds.snapshot(self.cfg, 1)
        self.close(1, [finding()])
        with self.assertRaises(rounds.RoundError):
            rounds.snapshot(self.cfg, 1)
        snap = json.load(open(path))
        os.remove(path)
        os.remove(os.path.join(self.d, "docs", "round1-verdicts.json"))   # even with the round's verdicts gone too
        with self.assertRaisesRegex(rounds.RoundError, "already closed"):
            rounds.snapshot(self.cfg, 1)                      # the attack: delete it and take it again
        with self.assertRaises(rounds.RoundError):
            rounds.changed_since(self.cfg, 1)
        snap["texts"]["draft"] = "First sentence. Second sentence. An unseen one."
        json.dump(snap, open(path, "w"))
        with self.assertRaises(rounds.RoundError):
            rounds.changed_since(self.cfg, 1)                 # not the snapshot the round closed on

    def test_round_inventory_is_the_changed_sentences_and_charts(self):
        self.chart("c1.png", "one")
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "First sentence. Second sentence, fixed.")
        self.chart("c1.png", "one, redrawn")
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        rounds.snapshot(self.cfg, 2)
        inventory = rounds.round_inventory(self.cfg, 2)           # a rewrite in place is one item, its new text
        self.assertEqual([i["text"] for i in inventory], ["Second sentence, fixed.", "[chart] charts/c1.png"])
        self.assertEqual([i["id"] // 10_000 for i in inventory], [1, 2])
        with self.assertRaisesRegex(rounds.RoundError, "round 1 checks the whole post"):
            rounds.round_inventory(self.cfg, 1)

    def strip_hashes(self, path):
        """Make a snapshot the shape every snapshot had before 2026-11-16: no per-file chart hashes."""
        with open(path) as f:
            snap = json.load(f)
        del snap["outputs"]
        with open(path, "w") as f:
            json.dump(snap, f)

    def test_the_first_round_after_a_snapshot_without_chart_hashes_lists_every_chart(self):
        # attack of 2026-11-16: on each of the six posts closed before per-file hashes, a chart redrawn before the
        # next round was on no list (the older snapshot cannot say which chart moved) and the tool refused to add it
        self.chart("c1.png", "one")
        self.chart("c2.png", "two")
        self.strip_hashes(rounds.snapshot(self.cfg, 1))
        self.close(1, [finding()])
        rounds.snapshot(self.cfg, 2)                                     # nothing moved: nothing to check
        self.assertEqual(rounds.round_inventory(self.cfg, 2), [])
        os.remove(os.path.join(self.d, "draft", ".rounds", "2.json"))
        self.chart("c1.png", "one, redrawn")
        rounds.snapshot(self.cfg, 2)
        self.assertEqual([i["text"] for i in rounds.round_inventory(self.cfg, 2)],
                         ["[chart] charts/c1.png", "[chart] charts/c2.png"])
        self.strip_hashes(os.path.join(self.d, "draft", ".rounds", "2.json"))   # two old snapshots: as before, none
        self.assertEqual(rounds.round_inventory(self.cfg, 2), [])

    def test_an_id_is_a_position_and_a_check_of_the_text_at_it(self):
        # attack of 2026-11-16: verdicts were joined to a list by position alone, so a panel's verdicts for a list
        # built by hand, or a read's verdicts for rows listed before a further edit, were laid over other text
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "First sentence. Second sentence, fixed.")
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        rounds.snapshot(self.cfg, 2)
        first = rounds.round_inventory(self.cfg, 2)[0]["id"]
        self.assertEqual(first, rounds.round_inventory(self.cfg, 2)[0]["id"])       # the same text: the same id
        os.remove(os.path.join(self.d, "draft", ".rounds", "2.json"))
        self.write("draft/d.src.md", "First sentence. Second sentence, fixed again.")
        rounds.snapshot(self.cfg, 2)
        other = rounds.round_inventory(self.cfg, 2)[0]["id"]
        self.assertEqual((first // 10_000, other // 10_000), (1, 1))               # both are item 1 of their list
        self.assertNotEqual(first, other)
        self.close(2, [finding()], scope=["Second sentence, fixed again."])
        rows = []
        for text in ("Second sentence, fixed.", "Second sentence.", "Second sentence, fixed."):
            self.write("draft/d.src.md", "First sentence. " + text)
            rows.append(rounds.settlement(self.cfg)["rows"][0])
        self.assertEqual([(r["index"], r["id"] // 10_000) for r in rows], [(0, 1)] * 3)
        self.assertEqual(rows[0]["id"], rows[2]["id"])
        self.assertNotEqual(rows[0]["id"], rows[1]["id"])
        self.write("draft/d.src.md", "First sentence. Second sentence, fixed again. Second sentence.")
        beside = rounds.settlement(self.cfg)["rows"][0]                             # new words beside their source
        self.assertEqual((beside["item"], beside["cut_of"], rows[1]["cut_of"]),
                         ("Second sentence.", None, "Second sentence, fixed again."))
        self.assertNotEqual(beside["id"], rows[1]["id"])                            # not the row that was a cut
        self.write("draft/d.src.md", "First sentence. Second sentence, again.")
        as_long = rounds.settlement(self.cfg)["rows"][0]                            # another cut of it, as long
        self.assertEqual((len(as_long["item"]), as_long["cut_of"]), (len(rows[0]["item"]), rows[0]["cut_of"]))
        self.assertNotEqual(as_long["id"], rows[0]["id"])

    def test_an_inventory_id_is_of_its_round_too(self):
        # verification round of 2026-11-16: an item that recurred unchanged at the same place in the next round's list
        # kept its id, so the earlier round's verdicts joined it
        self.chart("c1.png", "one")
        rounds.snapshot(self.cfg, 1)
        self.chart("c1.png", "two")
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        rounds.snapshot(self.cfg, 2)
        self.chart("c1.png", "three")
        self.close(2, [finding(verdict="REFUTED", fixed=True)], scope=[])
        rounds.snapshot(self.cfg, 3)
        two, three = rounds.round_inventory(self.cfg, 2), rounds.round_inventory(self.cfg, 3)
        self.assertEqual([i["text"] for i in two], [i["text"] for i in three])
        self.assertEqual(["[chart] charts/c1.png"], [i["text"] for i in two])
        self.assertEqual((two[0]["id"] // 10_000, three[0]["id"] // 10_000), (1, 1))
        self.assertNotEqual(two[0]["id"], three[0]["id"])

    def test_round_inventory_marks_a_moved_sentence_and_a_stretch_that_lost_sentences(self):
        # the sentence scope lists new text only, so a sentence round 1's fixes removed had no item: round 2 is the
        # last panel, and it has to be pointed at what a paragraph lost
        self.write("draft/d.src.md", "First sentence. Second sentence. Third sentence. Fourth sentence.")
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "Second sentence. First sentence. Third sentence, fixed.")
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        marks = ["[moved] Second sentence.", "[deleted] Third sentence.", "[deleted] Fourth sentence."]
        self.assertEqual(rounds.moved_or_deleted(self.cfg, 1), marks)
        rounds.snapshot(self.cfg, 2)
        self.assertEqual([i["text"] for i in rounds.round_inventory(self.cfg, 2)], ["Third sentence, fixed."] + marks)


    # --- the publish rule (two rounds, then cuts only) ---

    def after(self, n, read=(), accepted=(), read_date="2026-11-16"):
        """docs/after-round<n>.json written by hand: read holds (sentence, verdict[, kind[, cut_of]]) and accepted
        (kind, item, sha[, cut_of]). Unless it says otherwise an entry is of a 'sentence' row that is no cut."""
        row = lambda sentence, verdict, kind="sentence", cut_of=None: {
            "sentence": sentence, "kind": kind, "cut_of": cut_of, "verdict": verdict,
            "evidence": "read the paragraph before and after", "date": read_date}
        took = lambda kind, item, sha, cut_of=None: {"item": item, "kind": kind, "sha": sha, "cut_of": cut_of,
                                                      "owner": "ok, keep that wording", "date": "2026-11-16"}
        self.write(f"docs/after-round{n}.json", json.dumps({"round": n, "read": [row(*r) for r in read],
                                                             "accepted": [took(*a) for a in accepted]}))

    LONG = "Second sentence, fixed and long."

    def two_rounds(self):
        """Round 1 fixed a sentence, round 2 reviewed the fix and closed with a fix of its own."""
        self.chart("c1.png", "one")
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "First sentence. Second sentence, fixed and long.")
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        rounds.snapshot(self.cfg, 2)
        self.close(2, [finding(verdict="REFUTED", fixed=True)], scope=["Second sentence, fixed and long."])

    def blocked(self, text):
        errs = rounds.publish_check(self.cfg, True)
        self.assertTrue(any(text in e for e in errs), errs)

    def test_a_fix_off_the_rendered_surfaces_never_forces_a_round(self):
        rounds.snapshot(self.cfg, 1)
        self.close(1, [finding(verdict="REFUTED", fixed=True)])        # say, a code comment
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.write("b.py", "pass\n# a comment\n")                      # the gate's fresh check guards the build
        self.assertEqual(rounds.publish_check(self.cfg, True), [])

    def test_round_1_fixes_on_a_rendered_surface_need_round_2(self):
        rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "First sentence. Second sentence, fixed.")
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        self.blocked("run round 2")
        self.after(1, read=[("Second sentence, fixed.", "CONFIRMED")],  # after round 1 nothing stands in for round 2
                   accepted=[("sentence", "Second sentence, fixed.", None), ("deletion", "Second sentence.", None)])
        self.blocked("run round 2")

    def test_after_round_2_nothing_changed_publishes(self):
        self.two_rounds()
        self.assertEqual(rounds.publish_check(self.cfg, True), [])

    def test_after_round_2_a_cut_needs_one_read(self):
        self.two_rounds()
        cut = "Second sentence, fixed."
        self.write("draft/d.src.md", "First sentence. " + cut)
        self.assertEqual(rounds.publish_check(self.cfg, True), ["cut, not read: " + cut])
        self.after(2, read=[(cut, "REFUTED", "sentence", self.LONG)])
        self.blocked("cut, refuted by the read: " + cut)
        self.after(2, read=[(cut, "CONFIRMED")])                         # a read of new words: not of this cut
        self.blocked("cut, not read: " + cut)
        self.after(2, read=[(cut, "CONFIRMED", "sentence", self.LONG)])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.write("draft/d.src.md", "First sentence. Second.")          # edited again: the read is stale
        self.blocked("cut, not read: Second.")

    def test_after_round_2_new_words_need_the_owner(self):
        self.two_rounds()
        old, new = "Second sentence, fixed and long.", "Second sentence, rewritten."
        self.write("draft/d.src.md", "First sentence. " + new)
        self.assertEqual(rounds.publish_check(self.cfg, True),
                         ["new words, not accepted: " + new, "deleted, not read: " + old])
        self.after(2, read=[(new, "CONFIRMED"), (old, "CONFIRMED", "deletion")])
        self.assertEqual(rounds.publish_check(self.cfg, True),            # a read alone never passes new words
                         ["new words, not accepted: " + new])
        self.after(2, read=[(old, "CONFIRMED", "deletion")], accepted=[("sentence", new, None)])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])

    def test_after_round_2_a_deletion_needs_one_read(self):
        self.two_rounds()
        gone = "Second sentence, fixed and long."
        self.write("draft/d.src.md", "First sentence.")
        self.assertEqual(rounds.publish_check(self.cfg, True), ["deleted, not read: " + gone])
        self.after(2, read=[(gone, "REFUTED", "deletion")])
        self.blocked("deleted, refuted by the read: " + gone)
        self.after(2, read=[(gone, "CONFIRMED")])                        # read as a sentence that stands: not of this
        self.blocked("deleted, not read: " + gone)
        self.after(2, read=[(gone, "CONFIRMED", "deletion")])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.after(2, accepted=[("deletion", gone, None)])               # or the owner accepts the deletion
        self.assertEqual(rounds.publish_check(self.cfg, True), [])

    def test_after_round_2_a_moved_sentence_needs_the_owner(self):
        self.two_rounds()
        self.write("draft/d.src.md", "Second sentence, fixed and long. First sentence.")
        errs = rounds.publish_check(self.cfg, True)
        self.assertEqual([e.split(": ")[0] for e in errs], ["moved, not accepted"])
        moved = errs[0].split(": ", 1)[1]
        self.after(2, read=[(moved, "CONFIRMED")])
        self.blocked("moved, not accepted: " + moved)                    # a move follows the new-words rule
        self.after(2, accepted=[("sentence", moved, None)])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])

    def test_an_acceptance_is_of_one_kind_of_change(self):
        self.two_rounds()
        first = "First sentence."
        self.after(2, accepted=[("sentence", first, None)])              # accepted as it stood, say after a move
        self.write("draft/d.src.md", "Second sentence, fixed and long.")
        self.blocked("deleted, not read: " + first)                      # its deletion is another change

    def test_after_round_2_a_changed_chart_needs_the_owner_and_the_acceptance_is_of_one_version(self):
        self.two_rounds()
        self.chart("c1.png", "one, redrawn")
        self.assertEqual(rounds.publish_check(self.cfg, True), ["changed, not accepted: charts/c1.png"])
        self.after(2, accepted=[("chart", "charts/c1.png", rounds.outputs(self.cfg)["charts/c1.png"])])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.chart("c1.png", "one, redrawn again")                       # changed after the acceptance
        self.blocked("changed, not accepted: charts/c1.png")
        os.remove(os.path.join(self.d, "charts", "c1.png"))
        self.blocked("changed, not accepted: charts/c1.png")
        self.after(2, accepted=[("chart", "charts/c1.png", "gone")])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.chart("c2.png", "two")
        self.blocked("changed, not accepted: charts/c2.png")

    def test_a_new_surface_after_the_last_round_blocks(self):
        self.two_rounds()
        self.write("gate.toml", TOML + '[published]\nexcerpt="Hello there."\n')
        self.cfg = load(self.d)
        self.blocked("new surface")
        self.setUp()                                                     # and after round 1 it needs round 2
        rounds.snapshot(self.cfg, 1)
        self.close(1, [finding()])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.write("gate.toml", TOML + '[published]\nexcerpt="Hello there."\n')
        self.cfg = load(self.d)
        self.blocked("run round 2")

    def test_a_bad_after_round_record_blocks_with_a_message(self):
        self.two_rounds()
        cut = "Second sentence, fixed."
        self.write("draft/d.src.md", "First sentence. " + cut)
        good_read = {"sentence": cut, "kind": "sentence", "cut_of": self.LONG, "verdict": "CONFIRMED",
                     "evidence": "read the paragraph before and after", "date": "2026-11-16"}
        good_acc = {"item": cut, "kind": "sentence", "cut_of": self.LONG, "sha": None, "owner": "ok, keep that",
                    "date": "2026-11-16"}
        bad = ["{not json", json.dumps([]), json.dumps({"round": 3, "read": [], "accepted": []}),
               json.dumps({"round": 2, "read": "none", "accepted": []})]
        bad += [json.dumps({"round": 2, "read": [{**good_read, **fault}], "accepted": []}) for fault in (
            {"verdict": "PROBABLY"}, {"evidence": "ok"}, {"date": "yesterday"}, {"sentence": ""}, {"seq": "1"},
            {"kind": "chart"}, {"kind": None}, {"cut_of": 7}, {"cut_of": " "}, {"date": "2026-11-16 at noon"})]
        bad += [json.dumps({"round": 2, "read": [], "accepted": [{**good_acc, **fault}]}) for fault in (
            {"owner": " "}, {"owner": "ok"}, {"date": "16 Nov"}, {"kind": "cut"}, {"item": 7}, {"sha": 5},
            {"cut_of": 7}, {"date": "2026-11-16T09:00"})]
        for body in bad:
            with self.subTest(body=body):
                self.write("docs/after-round2.json", body)
                self.blocked("docs/after-round2.json")
        self.write("docs/after-round2.json", json.dumps({"round": 2, "read": [good_read], "accepted": [good_acc]}))
        self.assertEqual(rounds.publish_check(self.cfg, True), [])

    def test_a_post_closed_before_this_change_still_publishes_until_an_input_moves(self):
        path = rounds.snapshot(self.cfg, 1)
        snap = json.load(open(path))
        del snap["outputs"]
        json.dump(snap, open(path, "w"))
        self.close(1, [finding()])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.write("b.py", "pass\n# moved\n")
        self.blocked("run round 2")

    def test_after_round_2_a_post_without_chart_hashes_shows_any_input_change_as_one_row(self):
        # the state of every post closed before per-file hashes: the snapshot cannot say which input moved
        marker = "changed, not accepted: " + rounds.LEGACY_CHANGE
        self.chart("c1.png", "one")
        self.strip_hashes(rounds.snapshot(self.cfg, 1))
        self.write("draft/d.src.md", "First sentence. " + self.LONG)
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        self.strip_hashes(rounds.snapshot(self.cfg, 2))
        self.close(2, [finding(verdict="REFUTED", fixed=True)], scope=[self.LONG])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.write("b.py", "pass\n# moved\n")
        self.assertEqual(rounds.publish_check(self.cfg, True), [marker])
        self.write("draft/d.src.md", f"First sentence. {self.LONG} Entirely fresh words.")
        self.assertEqual(rounds.publish_check(self.cfg, True),            # the row stands beside a sentence row
                         ["new words, not accepted: Entirely fresh words.", marker])
        self.write("draft/d.src.md", "First sentence. " + self.LONG)
        rounds.record_acceptance(self.cfg, 2, 0, "(an input changed", "yes, that input may move", "2026-11-16")
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.write("b.py", "pass\n# moved again\n")                      # the acceptance was of the inputs as they stood
        self.assertEqual(rounds.publish_check(self.cfg, True), [marker])

    def test_only_the_last_closed_rounds_record_counts(self):
        self.chart("c1.png", "one")
        for n in (1, 2, 3):
            rounds.snapshot(self.cfg, n)
            self.close(n, [finding()], **({"scope": []} if n > 1 else {}))
        new = "Entirely fresh words."
        self.write("draft/d.src.md", "First sentence. Second sentence. " + new)
        self.after(2, accepted=[("sentence", new, None)])                # round 2's record, after round 3 closed
        self.blocked("new words, not accepted: " + new)
        self.write("draft/d.src.md", "First sentence. Second.")
        with self.assertRaises(rounds.RoundError):
            rounds.record_read(self.cfg, 2, [self.read_entry("Second.", cut_of="Second sentence.")])
        rounds.record_read(self.cfg, 3, [self.read_entry("Second.", cut_of="Second sentence.")])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])

    def test_each_acceptance_is_kept_beside_the_earlier_ones(self):
        self.two_rounds()
        self.write("draft/d.src.md", "First sentence, reworded. Second sentence, rewritten.")
        for index, starts in ((0, "First sentence, reworded."), (1, "Second sentence, rewritten.")):
            rounds.record_acceptance(self.cfg, 2, index, starts, "ok, keep that wording", "2026-11-16")
        self.assertEqual([r["state"] for r in rounds.settlement(self.cfg)["rows"]],
                         ["accepted", "accepted", "deleted, not read", "deleted, not read"])

    def test_a_removed_surface_is_a_deletion_of_each_of_its_sentences(self):
        self.write("gate.toml", TOML + '[published]\nexcerpt="Hello there. And more."\n')
        self.cfg = load(self.d)
        self.two_rounds()
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.write("gate.toml", TOML)
        self.cfg = load(self.d)
        self.assertEqual(rounds.publish_check(self.cfg, True), [
            "deleted, not read: [[published] excerpt] Hello there.", "deleted, not read: [[published] excerpt] And more."])

    def test_a_chart_folder_file_that_is_not_an_image_is_a_row_too(self):
        self.chart("c2.svg", "one")
        self.two_rounds()
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.chart("c2.svg", "two")
        self.assertEqual(rounds.publish_check(self.cfg, True), ["changed, not accepted: charts/c2.svg"])

    def read_entry(self, sentence, verdict="CONFIRMED", date="2026-11-16", kind="sentence", cut_of=None):
        return {"sentence": sentence, "kind": kind, "cut_of": cut_of, "verdict": verdict,
                "evidence": "read the paragraph before and after", "date": date}

    def test_record_read_and_record_acceptance_write_the_record(self):
        self.two_rounds()
        cut = "Second sentence, fixed."
        self.write("draft/d.src.md", "First sentence. " + cut)
        the_cut = lambda *a: self.read_entry(cut, *a, cut_of=self.LONG)
        for n, entry in ((2, self.read_entry("Not a changed sentence.")), (1, the_cut()), (2, the_cut("PROBABLY")),
                         (2, self.read_entry(cut)), (2, self.read_entry(cut, kind="deletion")),
                         (2, self.read_entry(cut, kind="deletion", cut_of=self.LONG))):                # not as this row
            with self.assertRaises(rounds.RoundError):
                rounds.record_read(self.cfg, n, [entry])
        self.assertFalse(os.path.exists(os.path.join(self.d, "docs", "after-round2.json")))   # nothing half-written
        rounds.record_read(self.cfg, 2, [the_cut()])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.chart("c1.png", "one, redrawn")
        with self.assertRaises(rounds.RoundError):
            rounds.record_acceptance(self.cfg, 2, 1, "charts/c1.png", "  ", "2026-11-16")
        with self.assertRaises(rounds.RoundError):
            rounds.record_read(self.cfg, 2, [self.read_entry("charts/c1.png")])               # a chart is not read
        rounds.record_acceptance(self.cfg, 2, 1, "charts/c1.png", "yes, the redrawn chart stands", "2026-11-16")
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.assertEqual([(r["index"], r["kind"], r["item"], r["cut_of"], r["state"])
                          for r in rounds.settlement(self.cfg)["rows"]],
                         [(0, "sentence", cut, "Second sentence, fixed and long.", "cut, read"),
                          (1, "chart", "charts/c1.png", None, "accepted")])
        rec = json.load(open(os.path.join(self.d, "docs", "after-round2.json")))
        self.assertEqual((rec["round"], [(e["sentence"], e["kind"], e["cut_of"]) for e in rec["read"]],
                          rec["accepted"][0]["kind"], rec["accepted"][0]["sha"]),
                         (2, [(cut, "sentence", self.LONG)], "chart", rounds.outputs(self.cfg)["charts/c1.png"]))

    def test_accept_names_the_row_by_its_opening_words(self):
        self.two_rounds()
        new = "Second sentence, rewritten for the owner."
        self.write("draft/d.src.md", "First sentence. " + new)
        for index, starts in ((5, "Second sentence"), (0, "First sentence"), (0, ""), (0, "S"), (-1, new)):
            with self.subTest(index=index, starts=starts), self.assertRaises(rounds.RoundError):
                rounds.record_acceptance(self.cfg, 2, index, starts, "ok, keep that wording", "2026-11-16")
        rounds.record_acceptance(self.cfg, 2, 0, "Second sentence, rewritten", "ok, keep that wording", "2026-11-16")
        self.assertEqual(rounds.settlement(self.cfg)["rows"][0]["state"], "accepted")
        with self.assertRaises(rounds.RoundError):                       # after round 1 nothing can be accepted
            self.setUp()
            rounds.snapshot(self.cfg, 1)
            self.write("draft/d.src.md", "First sentence. A new one.")
            self.close(1, [finding(verdict="REFUTED", fixed=True)])
            rounds.record_acceptance(self.cfg, 1, 0, "A new one.", "ok, keep that wording", "2026-11-16")

    def test_an_acceptance_before_a_refuting_read_does_not_settle(self):
        self.two_rounds()
        old, new = "Second sentence, fixed and long.", "Second sentence, rewritten."
        self.write("draft/d.src.md", "First sentence. " + new)
        rounds.record_acceptance(self.cfg, 2, 0, new, "ok, keep that wording", "2026-11-16")
        gone = self.read_entry(old, kind="deletion")
        rounds.record_read(self.cfg, 2, [self.read_entry(new, "REFUTED"), gone])                   # later, same day
        self.assertEqual(rounds.publish_check(self.cfg, True), ["accepted, then refuted by the read: " + new])
        rounds.record_acceptance(self.cfg, 2, 0, new, "I read the objection; keep it", "2026-11-16")
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.after(2, read=[(new, "REFUTED"), (old, "CONFIRMED", "deletion")], accepted=[("sentence", new, None)],
                   read_date="2026-11-17")                               # by date, in a record written by hand
        self.blocked("accepted, then refuted by the read: " + new)
        self.after(2, read=[(new, "REFUTED"), (old, "CONFIRMED", "deletion")], accepted=[("sentence", new, None)],
                   read_date="2026-11-15")
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.after(2, read=[(new, "REFUTED"), (old, "CONFIRMED", "deletion")], accepted=[("sentence", new, None)])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])       # by hand and the same day: the acceptance stands
        self.after(2, accepted=[("sentence", new, None)])                # an acceptance by hand, then the command's read
        rounds.record_read(self.cfg, 2, [self.read_entry(new, "REFUTED"), gone])
        self.blocked("accepted, then refuted by the read: " + new)       # the same day: the entry with a seq is the later

    def test_a_read_recorded_after_an_acceptance_refutes_it_whatever_day_each_carries(self):
        # attack of 2026-11-16: entries were ordered by the day each command was given, so an acceptance dated a day
        # ahead (the UTC day against the local one) outranked the refuting read recorded after it
        self.two_rounds()
        old, new = self.LONG, "Second sentence, rewritten."
        self.write("draft/d.src.md", "First sentence. " + new)
        rounds.record_acceptance(self.cfg, 2, 0, new, "ok, keep that wording", "2026-11-17")
        rounds.record_read(self.cfg, 2, [self.read_entry(new, "REFUTED"), self.read_entry(old, kind="deletion")])
        self.assertEqual(rounds.publish_check(self.cfg, True), ["accepted, then refuted by the read: " + new])
        rounds.record_acceptance(self.cfg, 2, 0, new, "I read the objection; keep it", "2026-11-15")
        self.assertEqual(rounds.publish_check(self.cfg, True), [])       # recorded after the read, whatever its day

    def test_a_read_or_an_acceptance_counts_only_for_the_row_it_was_made_for(self):
        # attack of 2026-11-16: entries were matched by text alone, so the read of a sentence where it stood settled
        # its later deletion, and a read or an acceptance of new words settled the cut they became once their fuller
        # source was deleted. In each case nobody had read the paragraph that lost a sentence.
        first, short = "First sentence.", "Second sentence."
        self.two_rounds()
        self.write("draft/d.src.md", f"{self.LONG} {first}")
        moved = rounds.settlement(self.cfg)["rows"][0]["item"]           # a swap: either may be called the mover
        rounds.record_read(self.cfg, 2, [self.read_entry(moved)])
        self.write("draft/d.src.md", next(s for s in (first, self.LONG) if s != moved))
        self.assertEqual(rounds.publish_check(self.cfg, True), ["deleted, not read: " + moved])
        for settle in ("read", "accept"):
            with self.subTest(settle=settle):
                self.setUp()
                self.two_rounds()
                self.write("draft/d.src.md", f"{first} {self.LONG} {short}")
                self.assertEqual(rounds.publish_check(self.cfg, True), ["new words, not accepted: " + short])
                if settle == "read":
                    rounds.record_read(self.cfg, 2, [self.read_entry(short)])
                else:
                    rounds.record_acceptance(self.cfg, 2, 0, short, "fine, add the short line", "2026-11-16")
                    self.assertEqual(rounds.publish_check(self.cfg, True), [])
                self.write("draft/d.src.md", f"{first} {short}")         # the fuller sentence is deleted afterwards
                self.assertEqual(rounds.publish_check(self.cfg, True), ["cut, not read: " + short])

    def test_a_refuted_read_is_not_cancelled_by_a_confirmed_read_of_the_same_text(self):
        # attack of 2026-11-16: two rows with one text shared the last verdict recorded for that text
        same = "Same words here."
        self.write("draft/d.src.md", f"First sentence. {same}\n\nSecond sentence. {same}")
        for n in (1, 2):
            rounds.snapshot(self.cfg, n)
            self.close(n, [finding()], **({"scope": []} if n == 2 else {}))
        self.write("draft/d.src.md", "First sentence.\n\nSecond sentence.")
        self.assertEqual(rounds.publish_check(self.cfg, True), ["deleted, not read: " + same] * 2)
        for verdicts in (("REFUTED", "CONFIRMED"), ("CONFIRMED", "REFUTED")):
            with self.subTest(verdicts=verdicts):
                rounds.record_read(self.cfg, 2, [self.read_entry(same, v, kind="deletion") for v in verdicts])
                self.assertEqual(rounds.publish_check(self.cfg, True), ["deleted, refuted by the read: " + same] * 2)
        rounds.record_read(self.cfg, 2, [self.read_entry(same, kind="deletion")] * 2)
        self.assertEqual(rounds.publish_check(self.cfg, True),            # a later read does not clear a refutation
                         ["deleted, refuted by the read: " + same] * 2)
        rounds.record_acceptance(self.cfg, 2, 0, same, "both may go, I have read the objection", "2026-11-16")
        self.assertEqual(rounds.publish_check(self.cfg, True), [])       # one acceptance is of the text: both rows

    def test_a_refuted_row_stays_open_until_the_change_is_undone_or_accepted(self):
        # verification round of 2026-11-16: each recording of a read replaced the one before, so a second read that
        # CONFIRMED a row the first had REFUTED settled it, with nobody undoing the change or accepting it
        self.two_rounds()
        first, cut = "First.", "Second sentence, fixed."
        self.write("draft/d.src.md", f"{first} {cut}")
        a = lambda v: self.read_entry(first, v, cut_of="First sentence.")
        b = lambda v: self.read_entry(cut, v, cut_of=self.LONG)
        rounds.record_read(self.cfg, 2, [a("CONFIRMED"), b("REFUTED")])
        self.assertEqual(rounds.publish_check(self.cfg, True), ["cut, refuted by the read: " + cut])
        rounds.record_read(self.cfg, 2, [b("CONFIRMED")])               # a read of one row: the other's read is gone,
        self.assertEqual(rounds.publish_check(self.cfg, True),            # the refutation stays on file
                         ["cut, not read: " + first, "cut, refuted by the read: " + cut])
        rounds.record_acceptance(self.cfg, 2, 1, cut, "I read the objection; keep the cut", "2026-11-16")
        rounds.record_read(self.cfg, 2, [a("CONFIRMED"), b("CONFIRMED")])
        self.assertEqual(rounds.publish_check(self.cfg, True), [])       # accepted after the refutation, and read
        rounds.record_read(self.cfg, 2, [a("CONFIRMED"), b("REFUTED")])
        self.blocked("accepted, then refuted by the read: " + cut)       # refuted again after the acceptance
        self.write("draft/d.src.md", f"{first} {self.LONG}")             # the change undone: no row, nothing open
        self.assertEqual(rounds.publish_check(self.cfg, True), [])
        self.write("draft/d.src.md", f"{first} {cut}")                   # and made again: refuted as before
        self.blocked("accepted, then refuted by the read: " + cut)
        further = "Second sentence, fixed and."
        self.write("draft/d.src.md", f"{first} {further}")               # cut another way and read, then back again
        rounds.record_read(self.cfg, 2, [a("CONFIRMED"), self.read_entry(further, cut_of=self.LONG)])
        self.write("draft/d.src.md", f"{first} {cut}")
        rounds.record_read(self.cfg, 2, [a("CONFIRMED"), b("CONFIRMED")])
        self.blocked("accepted, then refuted by the read: " + cut)       # a refutation is never dropped

    def test_owner_words_and_evidence_carry_no_long_dashes(self):
        # attack of 2026-11-16: only the em and en dash were handled, so a minus sign in a read's evidence or in the
        # owner's words went into the record and the gate's own style check then failed on that record
        forbidden = [chr(c) for c in range(0x2000, 0x2300) if style.FORBIDDEN.fullmatch(chr(c))]
        self.assertEqual(len(forbidden), 7, forbidden)
        self.two_rounds()
        cut = "Second sentence, fixed."
        self.write("draft/d.src.md", "First sentence. " + cut)
        for dash in forbidden:
            with self.subTest(dash=hex(ord(dash))), self.assertRaises(rounds.RoundError):
                rounds.record_acceptance(self.cfg, 2, 0, cut, f"ok {dash} keep that wording", "2026-11-16")
        rounds.record_read(self.cfg, 2, [{**self.read_entry(cut, cut_of=self.LONG),
                                          "evidence": "draft lines 3\u20135 \u2014 still true " + "".join(forbidden)}])
        with open(os.path.join(self.d, "docs", "after-round2.json")) as f:
            body = f.read()
        self.assertEqual(json.loads(body)["read"][0]["evidence"], "draft lines 3-5 - still true -------")
        self.assertIsNone(style.FORBIDDEN.search(body))

    def test_an_edited_earlier_snapshot_cannot_shrink_the_next_scope(self):
        path = rounds.snapshot(self.cfg, 1)
        self.write("draft/d.src.md", "First sentence. Second sentence, fixed.")
        self.close(1, [finding(verdict="REFUTED", fixed=True)])
        snap = json.load(open(path))
        snap["texts"]["draft"] = "First sentence. Second sentence, fixed."   # as if round 1 had seen the fix
        json.dump(snap, open(path, "w"))
        with self.assertRaises(rounds.RoundError):
            rounds.scope(self.cfg, 1)
        rounds.snapshot(self.cfg, 2)
        with self.assertRaises(rounds.RoundError):
            self.close(2, [finding()], scope=[])

    def restricted(self):
        self.write("gate.toml", TOML + 'restricted_inputs=["AEI Housing Center", "ICI"]\n')
        self.cfg = load(self.d)
        rounds.snapshot(self.cfg, 1)
        self.close(1, [finding()])

    def test_restricted_inputs_need_results_git_ignored(self):
        subprocess.run(["git", "init", "-q", self.d], check=True)
        self.restricted()
        self.assertEqual(rounds.publish_check(self.cfg, True), [
            "results.json is not git-ignored although [post] restricted_inputs names "
            "['AEI Housing Center', 'ICI']: keep it out of the repository"])
        self.write(".gitignore", "results.json\n")
        self.assertEqual(rounds.publish_check(self.cfg, True), [])

    def test_restricted_inputs_outside_a_repository_block_with_a_message(self):
        self.restricted()
        with unittest.mock.patch.dict(os.environ, {"GIT_CEILING_DIRECTORIES": os.path.dirname(self.d)}):
            self.blocked("cannot tell whether results.json is git-ignored")
        with unittest.mock.patch.object(rounds.subprocess, "run", side_effect=OSError("no git here")):
            self.blocked("cannot tell whether results.json is git-ignored (no git here)")

    WORDS = ["rent", "buy", "years", "home", "stocks", "price", "rose", "fell", "more", "less", "often", "slowly"]
    NAMES = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet"]

    def test_publish_check_agrees_with_a_model(self):
        """300 random sets of edits after round 2, over 30 random posts. The expected verdict comes from the edit
        log by the invariant, not from the diff under test: every sentence opens with a name no other sentence has,
        so the model knows which old sentence each current one descends from, and whether it still stands between
        the same unchanged sentences, without running a diff. (The chart's hash is read through rounds.outputs.)"""
        rng, said = random.Random(20261116), lambda s: " ".join(s) + "."
        body = lambda lo, hi: [rng.choice(self.WORDS) for _ in range(rng.randint(lo, hi))]
        within = lambda s, o: any(list(c) == s for c in itertools.combinations(o, len(s)))
        outcomes = {True: 0, False: 0}
        for case in range(300):
            if case % 10 == 0:                                           # a new post every ten cases
                self.setUp()
                orig = [[self.NAMES[i]] + body(2, 5) for i in range(rng.randint(3, 6))]
                self.write("draft/d.src.md", " ".join(map(said, orig)))
                self.chart("c1.png", "one")
                for n in (1, 2):
                    rounds.snapshot(self.cfg, n)
                    self.close(n, [finding()], **({"scope": []} if n == 2 else {}))
            cur, chart, fresh = [list(s) for s in orig], "one", iter(self.NAMES[len(orig):])
            for _ in range(rng.randint(0, 3)):
                op = rng.choice(["cut", "replace", "delete", "move", "add", "chart", "cut and move"])
                i = rng.randrange(len(cur))
                if op == "chart":
                    chart = rng.choice(["two", None])
                elif op == "add":
                    cur.insert(rng.randint(0, len(cur)), [next(fresh)] + body(1, 3))
                elif op == "delete" and len(cur) > 1:
                    del cur[i]
                elif op == "move" and len(cur) > 1:
                    s = cur.pop(i)
                    cur.insert(rng.choice([j for j in range(len(cur) + 1) if j != i]), s)
                elif op == "cut" and len(cur[i]) > 1:
                    del cur[i][rng.randrange(1, len(cur[i]))]
                elif op == "cut and move" and len(cur) > 1 and len(cur[i]) > 1:
                    s = cur.pop(i)
                    del s[rng.randrange(1, len(s))]
                    cur.insert(rng.choice([j for j in range(len(cur) + 1) if j != i]), s)
                elif op == "replace" and len(cur[i]) > 1:
                    cur[i][rng.randrange(1, len(cur[i]))] = "zeta"
            self.write("draft/d.src.md", " ".join(map(said, cur)))
            self.chart("c1.png", chart or "")
            if chart is None:
                os.remove(os.path.join(self.d, "charts", "c1.png"))
            # the invariant, from the log: what each difference needs (a read can settle a cut or a deletion only).
            # A cut is a sentence that lost words where it stood, between the same unchanged sentences as before; one
            # that also moved is new words there and a deletion here.
            was = {o[0]: o for o in orig}
            stands = [s[0] for s in cur if was.get(s[0]) == s]
            reordered = stands != [o[0] for o in orig if o[0] in stands]
            gap = lambda seq, name: sum(s[0] in stands for s in seq[:[x[0] for x in seq].index(name)])
            lives, needs, either = set(stands), [], []
            for s in cur:
                shorter = s[0] in was and s[0] not in stands and within(s, was[s[0]])
                if shorter and reordered:                                # where a stretch ends is then the diff's choice
                    either.append((said(s), said(was[s[0]])))
                elif shorter and gap(cur, s[0]) == gap(orig, s[0]):
                    needs.append(("sentence", said(s), said(was[s[0]]), True))
                elif s[0] not in stands:
                    needs.append(("sentence", said(s), None, False))
                    continue
                lives.add(s[0])
            needs += [("deletion", said(o), None, True) for o in orig if o[0] not in lives]
            expected, full, read, accepted = True, rng.random() < 0.5, [], []
            a_read = lambda kind, item, cut_of, verdict, date="2026-11-17": {
                "sentence": item, "kind": kind, "cut_of": cut_of, "verdict": verdict,
                "evidence": "read the paragraph before and after", "date": date}
            for kind, item, cut_of, readable in needs:
                how = rng.choice(["accept"] + ["read"] * readable if full else
                                 ["accept", "read", "nothing", "refuted", "other kind", "accept, then refuted",
                                  "refuted, then accept", "read as the other kind", "accept, another source"])
                other = "deletion" if kind == "sentence" else "sentence"
                if how in ("accept", "accept, then refuted", "refuted, then accept"):
                    accepted.append((kind, item, None, cut_of))
                if how == "other kind":
                    accepted.append((other, item, None, cut_of))
                if how == "accept, another source":
                    accepted.append((kind, item, None, "Zulu was the fuller sentence."))
                if how == "read as the other kind":
                    read.append(a_read(other, item, cut_of, "CONFIRMED"))
                if how in ("read", "refuted", "accept, then refuted", "refuted, then accept"):
                    read.append(a_read(kind, item, cut_of, "CONFIRMED" if how == "read" else "REFUTED",
                                       "2026-11-15" if how == "refuted, then accept" else "2026-11-17"))
                expected &= how in ("accept", "refuted, then accept") or (how == "read" and readable)
            for item, source in either:                                  # a cut where it stood, or new words and a
                if full or rng.random() < 0.5:                           # deletion: settle both readings, or neither
                    accepted += [("sentence", item, None, None), ("sentence", item, None, source)]
                    read.append(a_read("deletion", source, None, "CONFIRMED"))
                else:
                    expected = False
            if reordered:                                                # which sentence the diff calls the mover is
                if full or rng.random() < 0.5:                           # its choice: accept all that stand, or none
                    accepted += [("sentence", said(was[name]), None, None) for name in stands]
                else:
                    expected = False
            if chart != "one":
                sha = rounds.outputs(self.cfg).get("charts/c1.png", "gone")
                how = "this version" if full else rng.choice(["this version", "another version", "nothing"])
                version = sha if how == "this version" else "0" * 64
                accepted += [("chart", "charts/c1.png", version, None)] * (how != "nothing")
                expected &= how == "this version"
            self.write("docs/after-round2.json", json.dumps({"round": 2, "read": read, "accepted": [
                {"item": i, "kind": k, "sha": sha, "cut_of": source, "owner": "ok, keep that wording",
                 "date": "2026-11-16"} for k, i, sha, source in accepted]}))
            errs = rounds.publish_check(self.cfg, True)
            self.assertEqual(errs == [], expected, (case, orig, cur, chart, read, accepted, errs))
            outcomes[expected] += 1
        self.assertGreater(min(outcomes.values()), 75, outcomes)         # both verdicts are well represented


class CutTest(unittest.TestCase):
    OLD = "So a buyer who had to move soon usually sold behind the renter, in 49 of 50 start years."

    def test_a_cut_only_removes_words(self):
        self.assertTrue(rounds.is_cut(self.OLD, "A buyer who had to move soon usually sold behind the renter."))
        self.assertTrue(rounds.is_cut(self.OLD, self.OLD.upper()))            # case and punctuation alone
        self.assertFalse(rounds.is_cut(self.OLD, "A buyer who had to move soon often sold behind the renter."))
        self.assertFalse(rounds.is_cut(self.OLD, "A renter who had to move soon usually sold behind the buyer."))
        self.assertFalse(rounds.is_cut(self.OLD, ""))

    def test_a_word_with_a_hyphen_or_an_apostrophe_is_one_word(self):
        self.assertFalse(rounds.is_cut("Renting won in twenty-three start years.", "Renting won in three start years."))
        self.assertFalse(rounds.is_cut("The never-colonised states did well.", "The colonised states did well."))
        self.assertFalse(rounds.is_cut("It wasn't the renter's gain.", "It was the renter gain."))

    def test_a_number_is_one_word(self):
        self.assertFalse(rounds.is_cut("The index fell 10.1 percent.", "The index fell 10 percent."))
        self.assertFalse(rounds.is_cut("Renting won in 1,185 cells.", "Renting won in 185 cells."))
        self.assertTrue(rounds.is_cut("The index fell 10.1 percent in 1998.", "The index fell 10.1 percent."))

    def test_is_cut_agrees_with_a_slow_subsequence_check(self):
        rng = random.Random(20261116)
        words = ["rent", "buy", "23", "25", "10.1", "of", "start", "years", "won", "none"]
        for _ in range(2000):
            old = [rng.choice(words) for _ in range(rng.randint(1, 7))]
            new = [rng.choice(words) for _ in range(rng.randint(1, 7))]
            want = len(new) <= len(old) and any(list(c) == new for c in itertools.combinations(old, len(new)))
            self.assertEqual(rounds.is_cut(" ".join(old) + ".", " ".join(new) + "."), want, (old, new))


if __name__ == "__main__":
    unittest.main()
