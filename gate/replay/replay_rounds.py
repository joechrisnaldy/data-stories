"""Replay the publish rule on real posts: what each round changed, and what the rule of 2026-10-09 (publish only
after a round that fixed nothing, with no input changed since) and the rule of 2026-11-16 (two rounds, then cuts
only) each say about publishing the post as it stands.

Run from Projects/analytics-blog, with a copy of gate/rounds.py from before the change:
    git show fc616c3:gate/rounds.py > /tmp/old_rounds.py
    python3 gate/replay/replay_rounds.py reversal-of-fortune rent-vs-buy --old /tmp/old_rounds.py

Reads only. Needs each post's local snapshots (draft/.rounds/) and its results. The run fails (exit 1) if the new
rule blocks a post the old rule let publish. Not part of the self-test.
"""

import argparse
import collections
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from gate import rounds  # noqa: E402
from gate.config import load  # noqa: E402

SHOWN = 100          # characters of an item printed; the count is what matters


def _old_rule(path: str):
    spec = importlib.util.spec_from_file_location("rounds_before_2026_11_16", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _clip(text: str) -> str:
    return text if len(text) <= SHOWN else text[:SHOWN] + " [...]"


def _pair(cfg, a: int, b: int) -> str:
    """What changed between the snapshots two consecutive rounds started from."""
    was, now = (rounds._closed_snapshot(cfg, n) for n in (a, b))
    changes = rounds._text_changes(was["texts"], now["texts"])
    kinds = collections.Counter(r["kind"] for r in changes["sentences"])
    if "outputs" in was and "outputs" in now:
        charts = f"{len(rounds._chart_changes(was['outputs'], now['outputs']))} chart file(s) differ"
    else:
        charts = "charts not comparable (a snapshot predates per-file hashes)"
    return (f"  snapshot {a} -> {b}: {len(changes['sentences'])} sentence(s) changed ({kinds['cut']} cut, "
            f"{kinds['new']} new words, {kinds['moved']} moved), {len(changes['deleted'])} gone, "
            f"{len(changes['new_surfaces'])} new surface(s); {charts}")


def replay(post: str, old) -> tuple:
    cfg = load(post)
    closed = [r.get("round") for r in rounds._records(cfg)]
    print(f"== {os.path.basename(os.path.abspath(post))}: {len(closed)} closed round(s)")
    for a, b in zip(closed, closed[1:]):
        print(_pair(cfg, a, b))
    verdicts = []
    for name, rule in (("old rule", old.publish_check), ("new rule", rounds.publish_check)):
        errs = rule(cfg, True)
        verdicts.append(not errs)
        print(f"  {name}: " + ("PUBLISH OK" if not errs else f"BLOCKED, {len(errs)} reason(s)"))
        for e in errs:
            print(f"      - {_clip(e)}")
    return tuple(verdicts)


def main(argv) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("posts", nargs="+")
    ap.add_argument("--old", required=True, help="gate/rounds.py as it was before the change")
    args = ap.parse_args(argv)
    old = _old_rule(args.old)
    results = {os.path.basename(os.path.abspath(p)): replay(p, old) for p in args.posts}
    newly_blocked = sorted(p for p, (was, now) in results.items() if was and not now)
    differ = sorted(p for p, (was, now) in results.items() if was != now)
    print(f"SUMMARY: {len(results)} post(s); the old rule lets {sum(was for was, _ in results.values())} publish, "
          f"the new rule {sum(now for _, now in results.values())}; verdicts differ on {differ or 'none'}; "
          f"blocked by the new rule only: {newly_blocked or 'none'}")
    return 1 if newly_blocked else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
