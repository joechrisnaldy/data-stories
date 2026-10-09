"""Fact-check round bookkeeping: snapshot, diff-scoped next round, close, and the publish precondition.

The record shows rounds failed in two mechanical ways: fixes re-entered unseen (130 of 404 incidents were
introduced by a previous fix), and a dead verifier's finding was filed as refuted. The first version of
this module was then beaten by closing an old round again and by changing analysis code after the last
round. So: rounds are consecutive and closed once; each reviews its own snapshot; round 2 onward accounts
for exactly the sentences changed since the previous snapshot; a clean round means nothing moved after
its snapshot; and the publish lock covers every input, not just the draft.

A review of that version showed snapshots compared only the template, so a code or results change during
a 'clean' round passed and a figure fixed in code never entered the next scope. Snapshots now hold the
RENDERED text of every surface (draft, extra outputs, published fields) and the manifest of every input.
Snapshots live beside the draft (draft/.rounds/, local like the draft); docs/rounds.jsonl is the record.
"""

import datetime
import hashlib
import json
import os

from gate.render import RenderError, render
from gate.text import paragraph_sentences

FINAL = {"CONFIRMED", "REFUTED", "UNVERIFIABLE"}
BLOCKING = {"UNVERIFIED", "OPEN"}
_MIN_EVIDENCE = 12
_HOLLOW = {"tbd", "todo", "n/a", "na", "see above", "none", "-", "ok", "checked", "verified"}


class RoundError(ValueError):
    pass


def _rounds_dir(cfg) -> str:
    return os.path.join(os.path.dirname(cfg.source), ".rounds")


def _snap(cfg, n: int) -> str:
    return os.path.join(_rounds_dir(cfg), f"{n}.json")


def _log(cfg) -> str:
    return os.path.join(cfg.root, "docs", "rounds.jsonl")


def _sha(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def manifest(cfg) -> str:
    """One hash over everything that determines what gets published."""
    paths = [cfg.source, cfg.rendered, cfg.results, os.path.join(cfg.root, "gate.toml"), *cfg.build]
    paths += [p for p in (cfg.sources, cfg.charts, cfg.mdx) if p]
    paths += [a for a, _ in cfg.extra]
    if os.path.isdir(cfg.chart_dir):
        paths += [os.path.join(cfg.chart_dir, f) for f in sorted(os.listdir(cfg.chart_dir))]
    entries = sorted((os.path.relpath(p, cfg.root), _sha(p) if os.path.isfile(p) else "missing") for p in set(paths))
    return hashlib.sha256(json.dumps(entries).encode()).hexdigest()


def _records(cfg) -> list:
    if not os.path.exists(_log(cfg)):
        return []
    with open(_log(cfg)) as f:
        try:
            return [json.loads(line) for line in f if line.strip()]
        except json.JSONDecodeError as e:
            raise RoundError(f"docs/rounds.jsonl is not valid JSON lines: {e}") from e


def _load(path: str):
    with open(path) as f:
        return json.load(f)


def texts(cfg) -> dict:
    """What readers see, by surface: the rendered draft, each extra output, each published field."""
    results = _load(cfg.results)
    src = _load(cfg.sources) if cfg.sources else None
    try:
        with open(cfg.source) as f:
            out = {"draft": render(f.read(), results, src)[0]}
        for tmpl, dest in cfg.extra:
            with open(tmpl) as f:
                out[os.path.relpath(dest, cfg.root)] = render(f.read(), results, src)[0]
        for key, tmpl in cfg.published.items():
            out[f"[published] {key}"] = render(tmpl, results, src)[0]
    except RenderError as e:
        raise RoundError(f"the post does not render, so no round can start or close: {e}") from e
    return out


def _sentences(surfaces: dict) -> list:
    """Every sentence of every surface; outside the draft each is labelled with where it lives."""
    return [s if label == "draft" else f"[{label}] {s}"
            for label, text in surfaces.items() for s in paragraph_sentences(text)]


def _snapshot_texts(cfg, n: int) -> dict:
    if not os.path.exists(_snap(cfg, n)):
        raise RoundError(f"no snapshot for round {n}; run 'snapshot {n}' when the round starts")
    return _load(_snap(cfg, n))["texts"]


def snapshot(cfg, n: int) -> str:
    os.makedirs(_rounds_dir(cfg), exist_ok=True)
    dest = _snap(cfg, n)
    if os.path.exists(dest):
        raise RoundError(f"round {n} already has a snapshot at {dest}; snapshots are never overwritten")
    record = {"round": n, "texts": texts(cfg), "manifest": manifest(cfg)}
    with open(dest, "w") as f:
        json.dump(record, f, indent=1, ensure_ascii=False)
    return dest


def scope(cfg, since: int) -> list:
    """Sentences added or changed since the round-start snapshot, as readers see them. These ARE the next
    round's scope: a figure changed by code alone appears here too."""
    old = set(_sentences(_snapshot_texts(cfg, since)))
    return [s for s in _sentences(texts(cfg)) if s not in old]


def _scope_between(cfg, a: int, b: int) -> list:
    old = set(_sentences(_snapshot_texts(cfg, a)))
    return [s for s in _sentences(_snapshot_texts(cfg, b)) if s not in old]


def _validate(v: dict, n: int) -> list:
    errs = []
    d, r, e = (v.get(k) for k in ("lenses_dispatched", "lenses_returned", "lenses_errored"))
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in (d, r, e)):
        return ["lenses_dispatched, lenses_returned and lenses_errored must all be integers"]
    if d != r + e:
        errs.append(f"{d} lenses dispatched but {r} returned and {e} errored: {d - r - e} unaccounted for")
    if e:
        errs.append(f"{e} lens(es) errored; an errored lens means the round did not run. Re-run it.")
    if d == 0:
        errs.append("no lenses dispatched: a round with no lenses is not a round")
    findings = v.get("findings")
    if not isinstance(findings, list) or not findings or not all(isinstance(f, dict) for f in findings):
        return errs + ["findings must be a non-empty list: every claim in scope gets a verdict, CONFIRMED included"]
    for f in findings:
        fid, verdict = f.get("id", "?"), f.get("verdict")
        if verdict in BLOCKING:
            errs.append(f"finding {fid} is {verdict}; unverified is not refuted, adjudicate it with evidence")
        elif verdict not in FINAL:
            errs.append(f"finding {fid} has verdict {verdict!r}; must be one of {sorted(FINAL)}")
        ev = str(f.get("evidence", "")).strip()
        if len(ev) < _MIN_EVIDENCE or ev.lower() in _HOLLOW:
            errs.append(f"finding {fid} has no evidence locator (file:line, computation, or fetched source)")
        if verdict in ("REFUTED", "UNVERIFIABLE") and f.get("fixed") is not True:
            errs.append(f"finding {fid} is {verdict} but not marked fixed: fix it, or cut the claim")
    if v.get("round") != n:
        errs.append(f"verdicts file says round {v.get('round')!r}, expected {n}")
    return errs


def _sequence_errors(cfg, n: int, records: list) -> list:
    done = [r.get("round") for r in records]
    errs = []
    if n in done:
        errs.append(f"round {n} is already closed; a closed round is never closed again")
    expected = (max(done) + 1) if done else 1
    if n != expected:
        errs.append(f"the next round to close is {expected}, not {n}")
    if not os.path.exists(_snap(cfg, n)):
        errs.append(f"round {n} has no snapshot; run 'snapshot {n}' when the round starts")
    if n > 1 and not os.path.exists(_snap(cfg, n - 1)):
        errs.append(f"round {n - 1}'s snapshot is missing, so round {n}'s scope cannot be computed")
    return errs


def close_round(cfg, n: int, gate_passed: bool) -> dict:
    if not gate_passed:
        raise RoundError("the gate is not green; a round cannot close on a failing gate")
    records = _records(cfg)
    errs = _sequence_errors(cfg, n, records)
    path = os.path.join(cfg.root, "docs", f"round{n}-verdicts.json")
    if not os.path.exists(path):
        raise RoundError("\n  - ".join(["round cannot close:"] + errs + [f"no docs/round{n}-verdicts.json"]))
    with open(path) as f:
        try:
            v = json.load(f)
        except json.JSONDecodeError as e:
            raise RoundError(f"docs/round{n}-verdicts.json is not valid JSON: {e}") from e
    errs += _validate(v, n)
    if n > 1 and not errs:
        want = set(_scope_between(cfg, n - 1, n))
        if set(v.get("scope", [])) != want:
            errs.append(f"round {n} must list in 'scope' exactly the {len(want)} sentence(s) changed since round "
                        f"{n - 1}'s snapshot; it lists {len(v.get('scope', []))}")
    findings = v.get("findings") or []
    clean = not any(isinstance(f, dict) and f.get("fixed") for f in findings)
    if clean and not errs and _load(_snap(cfg, n)).get("manifest") != manifest(cfg):
        errs.append(f"round {n} is clean but something that determines the post (draft, results, sources, "
                    "config, scripts, charts or MDX) changed after its snapshot; that change was never reviewed")
    if errs:
        raise RoundError("round cannot close:\n  - " + "\n  - ".join(errs))
    counts = {k: sum(1 for f in findings if f["verdict"] == k) for k in sorted(FINAL)}
    record = {"round": n, "closed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
              "lenses": v["lenses_dispatched"], "findings": len(findings), **counts,
              "fixed": sum(1 for f in findings if f.get("fixed")), "clean": clean,
              "snapshot_sha256": _sha(_snap(cfg, n)), "manifest": manifest(cfg)}
    with open(_log(cfg), "a") as fh:
        fh.write(json.dumps(record) + "\n")
    return record


def publish_check(cfg, gate_passed: bool) -> list:
    errs = [] if gate_passed else ["the gate is not green"]
    # checks that are SKIPPED while drafting cannot be skipped at publish time
    if not cfg.charts:
        errs.append("no charts script is configured, so the chart checks never ran")
    if not (cfg.mdx and os.path.exists(cfg.mdx)):
        errs.append("no published MDX is configured or found, so the published-page checks never ran")
    records = _records(cfg)
    if not records:
        return errs + ["no fact-check round has been closed; publishing requires at least one"]
    last = records[-1]
    if not last.get("clean"):
        errs.append(f"round {last.get('round')} fixed {last.get('fixed')} finding(s); those fixes need a "
                    f"diff-scoped round {last.get('round', 0) + 1} before publishing")
    if last.get("manifest") != manifest(cfg):
        errs.append(f"something that determines the published post changed after round {last.get('round')} "
                    "closed (draft, results, sources, config, scripts, charts or MDX); it has never been checked")
    return errs
