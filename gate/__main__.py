"""The gate's command line. Run from Projects/analytics-blog; see gate/README.md.

    python3 -m gate check <post>                 (also: python3 -m gate <post>)
    python3 -m gate render <post>
    python3 -m gate snapshot <post> <N>
    python3 -m gate scope <post> --since <N>
    python3 -m gate close-round <post> <N>
    python3 -m gate publish-check <post>
"""

import argparse
import json
import os
import re
import subprocess
import sys

from gate import rounds
from gate.checks import charts, cite, claims, fresh, links, numbers, pairs, published, sources, style
from gate.config import ConfigError, load
from gate.render import RenderError, render

GATE_DIR = os.path.dirname(os.path.abspath(__file__))
COMMANDS = ("check", "render", "snapshot", "scope", "close-round", "publish-check")
SELFTEST_TIMEOUT = 600
# The self-test can itself start the gate (tests of the command line). Without this guard that recursed
# without bound and leaked thousands of temp directories on 2026-10-09.
_IN_SELFTEST = "GATE_IN_SELFTEST"


def selftest() -> int:
    """Number of tests passed, or -1. Refuses to recurse, and refuses skipped tests."""
    if os.environ.get(_IN_SELFTEST) or os.environ.get("GATE_SKIP_SELFTEST"):
        return 0
    try:
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", os.path.join(GATE_DIR, "tests"),
                            "-t", os.path.dirname(GATE_DIR)], capture_output=True, text=True,
                           timeout=SELFTEST_TIMEOUT, env={**os.environ, _IN_SELFTEST: "1"})
    except subprocess.TimeoutExpired:
        print(f"self-test exceeded {SELFTEST_TIMEOUT}s")
        return -1
    m = re.search(r"Ran (\d+) tests?", r.stderr)
    last = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""
    if r.returncode or not m or last != "OK":          # 'OK (skipped=3)' is not OK
        print(r.stderr[-1500:])
        return -1
    return int(m.group(1))


def _report(name: str, fails: list, note: str = "") -> int:
    if fails:
        print(f"{name:9s} {len(fails)} problem(s)")
        for f in fails:
            print(f"            - {f}")
    else:
        print(f"{name:9s} ok{('      ' + note) if note else ''}")
    return len(fails)


def _run(name: str, fn, note=""):
    """Run one check; an exception is a reported problem, never a crash of the whole gate. A note may be a
    callable, evaluated after the check, so nothing it computes can escape this guard."""
    try:
        fails = fn()
        return _report(name, fails, note() if callable(note) else note)
    except Exception as e:  # noqa: BLE001 - every failure must be reported, whatever its type
        return _report(name, [f"CRASHED: {type(e).__name__}: {e}"])


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def _inputs(cfg):
    results = json.loads(_read(cfg.results))
    src = json.loads(_read(cfg.sources)) if cfg.sources else None
    source = _read(cfg.source)
    rendered, binds = render(source, results, src)
    extra = [(a, b, *render(_read(a), results, src)) for a, b in cfg.extra]
    pub = {k: (t, *render(t, results, src)) for k, t in cfg.published.items()}
    return results, src, source, rendered, binds, extra, pub


def _stale(cfg, rendered, extra) -> list:
    out = []
    for path, want in [(cfg.rendered, rendered)] + [(b, o) for _, b, o, _ in extra]:
        if not os.path.exists(path):
            out.append(f"{os.path.relpath(path, cfg.root)} does not exist: run 'python3 -m gate render'")
        elif _read(path) != want:
            out.append(f"{os.path.relpath(path, cfg.root)} differs from a fresh render: hand-edited or not re-rendered")
    return out


def _checks(cfg, results, src, source, rendered, binds, extra, pub) -> int:
    # every template besides the draft, as (label, template text, bindings, rendered text): the README
    # templates and the published fields get the same checks as the draft wherever they apply
    others = [(os.path.relpath(a, cfg.root), _read(a), xb, out) for a, _, out, xb in extra]
    others += [(f"[published] {k}", t, b, out) for k, (t, out, b) in pub.items()]
    bad = _run("rendered", lambda: _stale(cfg, rendered, extra))
    box = {}
    printed = [("draft", source)] + [(label, t) for label, t, _, _ in others]
    bad += _run("fresh", lambda: box.setdefault("f", fresh.check(cfg, templates=printed))[0],
                "results and charts match a clean rebuild, and every template prints the same from both; "
                "two rebuilds match byte for byte")
    capture = box.get("f", ([], []))[1]
    seen = {}

    def _numbers():
        seen["literals"] = charts.literal_strings(cfg.charts) if cfg.charts else {}
        hand = [(os.path.relpath(p, cfg.root), _read(p)) for p in numbers.unconfigured_readmes(cfg)]
        seen["hand"] = hand
        templates = [(label, t, b) for label, t, b, _ in others] + [(label, t, []) for label, t in hand]
        seen["templates"] = len(templates)
        return (numbers.check(source, binds, cfg.allow, extra=seen["literals"], templates=templates)
                + numbers.chart_figures(capture, results, src, cfg.allow))
    bad += _run("numbers", _numbers, lambda: f"{len(cfg.allow)} [allow] phrases, {len(seen['literals'])} chart "
                                             f"literals, {seen['templates']} further templates")
    bad += _run("pairs", lambda: pairs.check(source, binds, cfg.pairs)
                + [f"{label}: {f}" for label, t, b, _ in others for f in pairs.check(t, b, {})],
                f"{len(cfg.pairs)} [pairs] exemptions")
    chart_text = [t for r in capture for t in charts.prose_texts(r)]
    fields = [out for label, _, _, out in others if label.startswith("[published]")]
    readmes = [out for label, _, _, out in others if not label.startswith("[published]")]
    bad += _run("claims", lambda: claims.check(rendered, cfg.claims, extra=chart_text + fields,
                                               readmes=readmes + [t for _, t in seen.get("hand", [])]),
                f"{len(cfg.claims)} [claims] entries")
    bad += _run("cite", lambda: cite.check(rendered))
    all_src = {b.path.split(".")[0] for b in binds if b.origin == "src"}
    all_src |= {b.path.split(".")[0] for _, _, bs, _ in others for b in bs if b.origin == "src"}
    bad += _run("sources", lambda: sources.check(source, rendered, binds, src, cfg.root)
                + [f"{label}: {f}" for label, t, b, _ in others if any(x.origin == "src" for x in b)
                   for f in sources.check(t, rendered, b, src, cfg.root)],
                f"{len(all_src)} stored documents verified")
    if cfg.charts:
        bad += _run("panels", lambda: charts.panel_counts(capture), f"{sum(len(r['axes']) for r in capture)} panels")
    else:
        print("panels    SKIPPED   no charts script configured")
    strings = {f"{r['file']} text {i + 1}": t for r in capture for i, t in enumerate(r["texts"])}
    bad += _run("style", lambda: style.check_files(seen.setdefault("files", style.text_files(cfg)))
                + style.check_strings(strings),
                lambda: f"{len(seen.get('files', []))} files, {len(strings)} rendered chart strings")
    bad += _run("links", lambda: links.check(rendered, os.path.dirname(cfg.rendered)))
    if cfg.mdx:
        fields = {k: out for k, (_, out, _) in pub.items()}
        bad += _run("published", lambda: published.check(_read(cfg.mdx), rendered, capture, fields, cfg),
                    f"whole page, {len(fields)} templated fields, captions and images against the charts")
    else:
        print("published SKIPPED   no MDX configured")
    return bad


def run_check(post: str) -> bool:
    n = selftest()
    if n < 0:
        print("self-test FAILED: the gate's own tests are red, so its verdicts mean nothing. Not checking.")
        return False
    print(f"gate      {os.path.basename(os.path.abspath(post))}")
    print(f"self-test {n} tests passed" if n else "self-test SKIPPED")
    try:
        cfg = load(post)
        inputs = _inputs(cfg)
    except (ConfigError, RenderError, OSError, ValueError) as e:
        print(f"setup     FAILED: {type(e).__name__}: {e}")
        return False
    binds, pub = inputs[4], inputs[6]
    n_src = sum(1 for b in binds if b.origin == "src")
    n_pub, n_extra = sum(len(b) for _, _, b in pub.values()), sum(len(x[3]) for x in inputs[5])
    print(f"render    {len(binds) + n_pub + n_extra} placeholders bound ({len(binds) - n_src} results and "
          f"{n_src} sources in the draft, {n_pub} in published fields, {n_extra} in other templates)")
    bad = _checks(cfg, *inputs)
    if not bad and not n and not os.environ.get(_IN_SELFTEST):
        print("GATE INCOMPLETE: every check passed but the self-test was skipped (GATE_SKIP_SELFTEST), so "
              "this is not a pass")
        return False
    print("GATE PASSED" if not bad else f"GATE FAILED: {bad} problem(s)")
    return not bad


def _parser():
    p = argparse.ArgumentParser(prog="python3 -m gate", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("check", "render", "publish-check"):
        sub.add_parser(name).add_argument("post")
    for name in ("snapshot", "close-round"):
        s = sub.add_parser(name)
        s.add_argument("post")
        s.add_argument("round", type=int)
    s = sub.add_parser("scope")
    s.add_argument("post")
    s.add_argument("--since", type=int, required=True)
    return p


def main(argv) -> int:
    if argv and argv[0] not in COMMANDS and not argv[0].startswith("-") and len(argv) == 1:
        argv = ["check", argv[0]]                       # python3 -m gate <post>
    args = _parser().parse_args(argv)
    try:
        if args.cmd == "check":
            return 0 if run_check(args.post) else 1
        cfg = load(args.post)
        if args.cmd == "render":
            _, _, _, rendered, _, extra, _ = _inputs(cfg)
            for path, text in [(cfg.rendered, rendered)] + [(b, o) for _, b, o, _ in extra]:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"rendered {os.path.relpath(path, cfg.root)}")
            return 0
        if args.cmd == "snapshot":
            print(f"snapshot {rounds.snapshot(cfg, args.round)}")
            return 0
        if args.cmd == "scope":
            changed = rounds.scope(cfg, args.since)
            print(f"{len(changed)} sentence(s) added or changed since round {args.since}; these are the next round's scope:")
            for s in changed:
                print(f"  - {s}")
            return 0
        if args.cmd == "close-round":
            print(json.dumps(rounds.close_round(cfg, args.round, run_check(args.post))))
            return 0
        errs = rounds.publish_check(cfg, run_check(args.post))
        print("PUBLISH OK" if not errs else "PUBLISH BLOCKED:\n  - " + "\n  - ".join(errs))
        return 0 if not errs else 1
    except (ConfigError, RenderError, rounds.RoundError, OSError, ValueError) as e:
        print(f"{args.cmd}: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
