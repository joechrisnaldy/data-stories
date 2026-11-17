"""Fact-check round bookkeeping: snapshot, diff-scoped next round, close, and the publish precondition.

The record shows rounds failed in two mechanical ways: fixes re-entered unseen (130 of 404 incidents were
introduced by a previous fix), and a dead verifier's finding was filed as refuted. The first version of
this module was then beaten by closing an old round again and by changing analysis code after the last
round. So: rounds are consecutive and closed once; each reviews its own snapshot; round 2 onward accounts
for exactly the sentences changed since the previous snapshot; and a clean round means nothing moved after
its snapshot.

A review of that version showed snapshots compared only the template, so a code or results change during
a 'clean' round passed and a figure fixed in code never entered the next scope. Snapshots now hold the
RENDERED text of every surface (draft, extra outputs, published fields), the manifest of every input and
the hash of every chart file. Snapshots live beside the draft (draft/.rounds/, local like the draft);
docs/rounds.jsonl is the record.

Publishing (owner's rule of 2026-11-16, two rounds and then cuts only; evidence in
Outputs/2026-11-16-round-evaluation) is decided from the sentences and chart files a reader would find
different from the snapshot the last closed round started from, not from the round's 'fixed' count. A
snapshot is taken before its round's verdicts exist. publish_check returns [] only if that snapshot is the
file the round closed on, and against it:
  (1) every surface existed then;
  (2) every current sentence stands unchanged in its order, or is a cut made where a sentence stood (the
      fuller sentence is gone from the same changed stretch) with a CONFIRMED read of that cut, or carries
      the owner's acceptance of it as the change it is (new words, a move, or that cut);
  (3) every sentence that is gone, and is not the source of a standing cut, has a CONFIRMED read of its
      deletion or the owner's acceptance of it;
  (4) every chart file's hash equals the snapshot's, or the hash the owner accepted.
A read or an acceptance counts only for the row it was made for. A REFUTED read is kept when reads are
recorded again, and among the reads of a row a REFUTED one decides: a row a read refuted stays open until
the change is undone or the owner accepts the row after that read. A later read does not clear it.
After round 1 there is no exception to (2) to (4): any such difference needs round 2. Reads and acceptances
live in docs/after-round<N>.json. A paragraph after a References heading (a reference entry) is compared
whole, like a sentence; elsewhere paragraph breaks and spacing are not compared.
"""

import datetime
import difflib
import hashlib
import json
import os
import re
import subprocess

from gate.render import RenderError, render
from gate.text import body_and_refs, paragraph_sentences, paragraphs

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


def _verdicts(cfg, n: int) -> str:
    return os.path.join(cfg.root, "docs", f"round{n}-verdicts.json")


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


def _units(text: str) -> list:
    """What a round compares on one surface: its sentences, and each paragraph after a References heading whole (an
    entry of the reference list, where blank lines set the entries apart; entries joined or split are a change).
    Split into sentences an entry is fragments such as '(2026).' and 'U.S.' that repeat from entry to entry, so
    that a corrected year reads as a fragment that moved and nobody can read or accept the entry by name."""
    body, refs = body_and_refs(text)
    if not refs:
        return paragraph_sentences(text)
    heading = text[len(body):len(text) - len(refs)]
    return paragraph_sentences(body + heading) + [" ".join(refs[a:b].split()) for a, b in paragraphs(refs)]


def _sentences(surfaces: dict) -> list:
    """Every sentence of every surface; outside the draft each is labelled with where it lives."""
    return [s if label == "draft" else f"[{label}] {s}" for label, text in surfaces.items() for s in _units(text)]


_WORD = re.compile(r"\d+(?:[.,]\d+)*|[^\W\d_]+(?:['’-][^\W\d_]+)*")
LEGACY_CHANGE = "(an input changed; this snapshot predates per-file hashes)"


def is_cut(old: str, new: str) -> bool:
    """True when `new` is `old` with words removed: its words all occur in `old`, in order, case and punctuation
    aside. A number in digits is one word, so '10.1' to '10' is not a cut; a number in words is several, so
    'twenty-three thousand' to 'twenty-three' is one, and the read is what judges it."""
    rest = iter(_WORD.findall(old.lower()))
    words = _WORD.findall(new.lower())
    return bool(words) and all(w in rest for w in words)


def outputs(cfg) -> dict:
    """sha256 of every file in the chart folder, by path relative to the post: what a reader sees besides the text.
    results.json has no entry: a results change reaches a reader only through a rendered sentence or a chart."""
    if not os.path.isdir(cfg.chart_dir):
        return {}
    files = [os.path.join(cfg.chart_dir, f) for f in sorted(os.listdir(cfg.chart_dir))]
    return {os.path.relpath(f, cfg.root): _sha(f) for f in files if os.path.isfile(f)}


def _closed_snapshot(cfg, n: int) -> dict:
    """Snapshot n. Once round n is closed, only the file it closed on will do: a missing one cannot be retaken."""
    record = next((r for r in _records(cfg) if r.get("round") == n), None)
    path = _snap(cfg, n)
    if not os.path.exists(path):
        raise RoundError(f"round {n}'s snapshot is missing and cannot be retaken: the round closed on it" if record
                         else f"no snapshot for round {n}; run 'snapshot {n}' when the round starts")
    if record and record.get("snapshot_sha256") != _sha(path):
        raise RoundError(f"draft/.rounds/{n}.json is not the snapshot round {n} closed on")
    return _load(path)


def _label(surface: str, sentence: str) -> str:
    return sentence if surface == "draft" else f"[{surface}] {sentence}"


def _surface_changes(a: list, b: list) -> tuple:
    """(rows, deleted, lost) between one surface's old and current sentence lists, by position. A sentence that
    stands where it stood is unchanged. An inserted one is 'moved' when its text is an old sentence of the surface,
    else a 'cut' of the first unclaimed old sentence that is gone from the SAME changed stretch (a cut is made
    where the sentence stood; words that turn up elsewhere are new words), else 'new'. An old sentence that is gone
    and is neither a cut's source nor a moved sentence is deleted: a rewrite lists both its new and its old text.
    `lost` is the part of `deleted` in stretches that lost more sentences than they gained new ones."""
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    blocks = [(range(i1, i2), b[j1:j2]) for tag, i1, i2, j1, j2 in ops if tag != "equal"]
    gone = [i for old, _ in blocks for i in old]
    used, rows = set(), []
    for old, added in blocks:
        for s in added:
            moved = s in a
            src = next((i for i in (gone if moved else old)
                        if i not in used and (a[i] == s if moved else is_cut(a[i], s))), None)
            used.add(src)
            kind = "moved" if moved else "cut" if src is not None else "new"
            rows.append({"sentence": s, "cut_of": a[src] if kind == "cut" else None, "kind": kind})
    new, lost = iter(rows), []
    for old, added in blocks:
        left = [a[i] for i in old if i not in used]
        if len(left) > sum(next(new)["kind"] == "new" for _ in added):
            lost += left
    return rows, [a[i] for i in gone if i not in used], lost


def _text_changes(old: dict, new: dict) -> dict:
    """Sentence changes between two {surface: text} maps, each sentence labelled with its surface."""
    out = {"sentences": [], "deleted": [], "lost": [], "new_surfaces": sorted(set(new) - set(old))}
    for surface, text in old.items():
        rows, deleted, lost = _surface_changes(_units(text), _units(new.get(surface, "")))
        out["sentences"] += [{"sentence": _label(surface, r["sentence"]),
                              "cut_of": r["cut_of"] and _label(surface, r["cut_of"]), "kind": r["kind"]} for r in rows]
        out["deleted"] += [_label(surface, s) for s in deleted]
        out["lost"] += [_label(surface, s) for s in lost]
    return out


_CHECK = 10_000


def _bound_id(position: int, *text) -> int:
    """A list position followed by a four-digit check of what stands there (an inventory passes its round and the
    item's text; a changed row passes the row). A verdict that names an id can then be joined only to that text at
    that place: the same list written again after an edit, a list built by hand and another round's inventory all
    carry other ids."""
    digest = hashlib.sha256(json.dumps(text, ensure_ascii=False).encode()).hexdigest()
    return position * _CHECK + int(digest, 16) % _CHECK


def _chart_changes(was: dict, now: dict) -> list:
    return sorted(path for path in set(was) | set(now) if was.get(path) != now.get(path))


def changed_since(cfg, n: int) -> dict:
    """What a reader would find different from round n's snapshot: changed sentences (cut, new or moved), sentences
    that are gone, chart files that differ, and surfaces that did not exist."""
    snap = _closed_snapshot(cfg, n)
    changes = _text_changes(snap["texts"], texts(cfg))
    if "outputs" in snap:
        charts = _chart_changes(snap["outputs"], outputs(cfg))
    else:
        charts = [LEGACY_CHANGE] if snap.get("manifest") != manifest(cfg) else []
    return {**{k: changes[k] for k in ("sentences", "deleted", "new_surfaces")}, "charts": charts}


def _marks(old: dict, new: dict) -> list:
    """What a sentence-by-sentence scope cannot list, marked for a round's inventory: a sentence that only moved,
    and the old sentences of each stretch that lost more than it gained (a rewrite in place is not marked: its new
    text is in the scope already)."""
    changes = _text_changes(old, new)
    return ([f"[moved] {r['sentence']}" for r in changes["sentences"] if r["kind"] == "moved"]
            + [f"[deleted] {s}" for s in changes["lost"]])


def moved_or_deleted(cfg, since: int) -> list:
    """The moved and deleted sentences since a round-start snapshot, as the post stands now."""
    return _marks(_snapshot_texts(cfg, since), texts(cfg))


def round_inventory(cfg, n: int) -> list:
    """What round n (2 or later) checks, from its own snapshot and the one before: every sentence added or changed,
    then the moved ones and those of a stretch that lost more than it gained, then every chart file that differs.
    An earlier snapshot from before per-file hashes cannot say which chart differs: every chart is then listed
    when any input moved (two such snapshots list none; no round can still start between two). Nothing else is on
    the list."""
    if n < 2:
        raise RoundError("round 1 checks the whole post; only later rounds have a computed inventory")
    was, now = (_closed_snapshot(cfg, k) for k in (n - 1, n))
    items = _scope_between(cfg, n - 1, n) + _marks(was["texts"], now["texts"])
    if "outputs" in was and "outputs" in now:
        items += [f"[chart] {path}" for path in _chart_changes(was["outputs"], now["outputs"])]
    elif was.get("manifest") != now.get("manifest"):
        items += [f"[chart] {path}" for path in sorted(now.get("outputs", {}))]
    return [{"id": _bound_id(i, n, s), "text": s} for i, s in enumerate(items, 1)]


def _snapshot_texts(cfg, n: int) -> dict:
    return _closed_snapshot(cfg, n)["texts"]


def snapshot(cfg, n: int) -> str:
    os.makedirs(_rounds_dir(cfg), exist_ok=True)
    dest = _snap(cfg, n)
    if any(r.get("round") == n for r in _records(cfg)):
        raise RoundError(f"round {n} is already closed; its snapshot cannot be retaken")
    if os.path.exists(dest):
        raise RoundError(f"round {n} already has a snapshot at {dest}; snapshots are never overwritten")
    if os.path.exists(_verdicts(cfg, n)):
        raise RoundError(f"round {n}'s verdicts are already written (docs/round{n}-verdicts.json): a snapshot is "
                         "taken before the panel reads the post, never after, or it would hold the round's own "
                         "fixes. Run the round again: remove that file, take the snapshot, then run the panel")
    record = {"round": n, "texts": texts(cfg), "manifest": manifest(cfg), "outputs": outputs(cfg)}
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
        errs.append(f"round {n} has no snapshot. It is taken before the panel reads the post ('snapshot {n}'), "
                    "so run the round again from its snapshot")
    if n > 1 and not os.path.exists(_snap(cfg, n - 1)):
        errs.append(f"round {n - 1}'s snapshot is missing, so round {n}'s scope cannot be computed")
    return errs


def close_round(cfg, n: int, gate_passed: bool) -> dict:
    if not gate_passed:
        raise RoundError("the gate is not green; a round cannot close on a failing gate")
    records = _records(cfg)
    errs = _sequence_errors(cfg, n, records)
    path = _verdicts(cfg, n)
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


SETTLED = ("accepted", "cut, read", "deleted, read")
_ROW_KINDS = ("sentence", "deletion", "chart")
_READ_KINDS = _ROW_KINDS[:2]                               # a chart is the owner's to accept, never read
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
# every character gate/checks/style.py forbids: the record is one of the files that check reads. A test holds the
# two sets equal.
_LONG_DASHES = dict.fromkeys("\u2010\u2011\u2012\u2013\u2014\u2015\u2212", "-")


def _after_path(cfg, n: int) -> str:
    return os.path.join(cfg.root, "docs", f"after-round{n}.json")


def _after_faults(rec, n: int) -> list:
    """Why a docs/after-round<n>.json record cannot be relied on; [] when it can."""
    if not isinstance(rec, dict) or rec.get("round") != n:
        return [f"it is not the record of round {n}"]
    read, accepted = rec.get("read"), rec.get("accepted")
    if not (isinstance(read, list) and isinstance(accepted, list) and all(isinstance(e, dict) for e in read + accepted)):
        return ["'read' and 'accepted' must each be a list of entries"]
    text = lambda v: isinstance(v, str) and bool(v.strip())
    faults = []
    for key, entries in (("sentence", read), ("item", accepted)):
        for e in entries:
            name = e.get(key)
            if not text(name):
                faults.append(f"an entry has no '{key}'")
            if not (isinstance(e.get("date"), str) and _DATE.fullmatch(e["date"])):
                faults.append(f"the date of {name!r} is not YYYY-MM-DD")
            if type(e.get("seq", 0)) is not int:
                faults.append(f"the seq of {name!r} is not a whole number")
            if not (e.get("cut_of") is None or text(e["cut_of"])):
                faults.append(f"the cut_of of {name!r} is not a sentence")
    for e in read:
        evidence = str(e.get("evidence", "")).strip()
        if e.get("kind") not in _READ_KINDS:
            faults.append(f"the read of {e.get('sentence')!r} has kind {e.get('kind')!r}, not one of {list(_READ_KINDS)}")
        if e.get("verdict") not in ("CONFIRMED", "REFUTED"):
            faults.append(f"the read of {e.get('sentence')!r} has verdict {e.get('verdict')!r}, not CONFIRMED or REFUTED")
        if len(evidence) < _MIN_EVIDENCE or evidence.lower() in _HOLLOW:
            faults.append(f"the read of {e.get('sentence')!r} has no evidence")
    for e in accepted:
        if e.get("kind") not in _ROW_KINDS:
            faults.append(f"the acceptance of {e.get('item')!r} has kind {e.get('kind')!r}, not one of {list(_ROW_KINDS)}")
        if not (e.get("sha") is None or isinstance(e["sha"], str)):
            faults.append(f"the acceptance of {e.get('item')!r} has a sha that is not text")
        if not text(e.get("owner")) or len("".join(e["owner"].split())) < 3:
            faults.append(f"the acceptance of {e.get('item')!r} does not carry the owner's words")
    return faults


def _after(cfg, n: int) -> dict:
    """docs/after-round<n>.json: what was read and what the owner accepted after round n closed. No file: nothing."""
    path, name = _after_path(cfg, n), f"docs/after-round{n}.json"
    if not os.path.exists(path):
        return {"round": n, "read": [], "accepted": []}
    try:
        rec = _load(path)
    except ValueError as e:                               # not JSON, or not text
        raise RoundError(f"{name} is not valid JSON: {e}") from e
    faults = _after_faults(rec, n)
    if faults:
        raise RoundError(f"{name} cannot be relied on: " + "; ".join(faults))
    return rec


def _order(entry: dict) -> tuple:
    """When an entry without a seq was recorded (a record written by hand): by day."""
    return entry["date"], entry.get("seq", 0)


def _before(a: dict, b: dict) -> bool:
    """Whether entry a was recorded before entry b: by the order the commands wrote them (seq), whatever day each
    was given; by day only when one of them carries no seq."""
    return a["seq"] < b["seq"] if "seq" in a and "seq" in b else _order(a) < _order(b)


def _version(cfg, path: str) -> str:
    """What an acceptance of a chart row is of: the file as it is now, 'gone', or (a legacy snapshot) every input."""
    if path == LEGACY_CHANGE:
        return manifest(cfg)
    full = os.path.join(cfg.root, path)
    return _sha(full) if os.path.isfile(full) else "gone"


def _state(cfg, kind: str, change: str, item: str, cut_of, rec: dict) -> str:
    """A row is settled by the owner's acceptance of that row (that item, as that kind of change, cut from that
    sentence, and for a chart at that version), unless a read recorded later refuted it; a cut or a deletion is
    also settled by a CONFIRMED read of that row. A read or an acceptance made for another row with the same text
    (the sentence where it stood before it was deleted, new words before they became a cut) does not count, and
    among the reads of one row a REFUTED one decides."""
    reads = [e for e in rec["read"] if (e["sentence"], e["kind"], e.get("cut_of")) == (item, kind, cut_of)]
    refuting = [e for e in reads if e["verdict"] == "REFUTED"]
    version = _version(cfg, item) if kind == "chart" else None
    accepted = [e for e in rec["accepted"]
                if (e["kind"], e["item"], e.get("sha"), e.get("cut_of")) == (kind, item, version, cut_of)]
    if accepted:
        late = any(all(_before(e, r) for e in accepted) for r in refuting)
        return "accepted, then refuted by the read" if late else "accepted"
    if change in ("cut", "deleted"):
        return f"{change}, " + ("not read" if not reads else "refuted by the read" if refuting else "read")
    return {"new": "new words", "moved": "moved", "chart": "changed"}[change] + ", not accepted"


def settlement(cfg) -> dict:
    """Every difference a reader would find from the snapshot the last closed round started from, as rows with a
    state each: changed sentences first, then deleted ones, then charts. The states in SETTLED need nothing more.
    `index` is what the owner's accept command names; `id` is what a read returns its verdict under."""
    records = _records(cfg)
    if not records:
        raise RoundError("no fact-check round has been closed; publishing requires at least one")
    n = records[-1].get("round")
    diff, rec = changed_since(cfg, n), _after(cfg, n)
    rows = [("sentence", r["kind"], r["sentence"], r["cut_of"]) for r in diff["sentences"]]
    rows += [("deletion", "deleted", s, None) for s in diff["deleted"]]
    rows += [("chart", "chart", path, None) for path in diff["charts"]]
    return {"round": n, "new_surfaces": diff["new_surfaces"],
            "rows": [{"index": i, "id": _bound_id(i + 1, kind, item, cut_of), "kind": kind, "item": item,
                      "cut_of": cut_of, "state": _state(cfg, kind, change, item, cut_of, rec)}
                     for i, (kind, change, item, cut_of) in enumerate(rows)]}


def _open_record(cfg, n: int) -> tuple:
    """(rows, record) for round n, which must be the last closed round and later than round 1."""
    s = settlement(cfg)
    if s["round"] != n:
        raise RoundError(f"round {n} is not the last closed round; round {s['round']} is")
    if n < 2:
        raise RoundError("after round 1 every change needs round 2; reads and acceptances start after round 2")
    return s["rows"], _after(cfg, n)


def _save_record(cfg, n: int, rec: dict) -> None:
    faults = _after_faults(rec, n)
    if faults:
        raise RoundError(f"docs/after-round{n}.json was not written: " + "; ".join(faults))
    with open(_after_path(cfg, n), "w") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
        f.write("\n")


def _next_seq(rec: dict) -> int:
    return 1 + max((e.get("seq", 0) for e in rec["read"] + rec["accepted"]), default=0)


def record_read(cfg, n: int, entries: list) -> None:
    """Record a read in docs/after-round<n>.json: its entries replace the CONFIRMED reads on file, and every REFUTED
    read on file is kept (a refutation is answered by undoing the change or by the owner's acceptance, never by a
    later read). Each entry is {sentence, kind, cut_of, verdict, evidence, date} for one row of settlement(cfg): a
    sentence changed since round n's snapshot (kind 'sentence', with the sentence it was cut from, or None) or a
    deleted one (kind 'deletion'). An entry that is not a current row is refused."""
    rows, rec = _open_record(cfg, n)
    known = {(r["item"], r["kind"], r["cut_of"]) for r in rows if r["kind"] in _READ_KINDS}
    row_of = lambda e: (e.get("sentence"), e.get("kind"), e.get("cut_of")) if isinstance(e, dict) else None
    stray = [e for e in entries if row_of(e) not in known]
    if stray:
        raise RoundError(f"not a sentence changed or deleted since round {n}'s snapshot, or not as that kind of "
                         f"change: {stray}")
    seq = _next_seq(rec)
    undash = lambda s: "".join(_LONG_DASHES.get(c, c) for c in str(s))
    read = [{"sentence": e["sentence"], "kind": e["kind"], "cut_of": e.get("cut_of"), "verdict": e.get("verdict"),
             "evidence": undash(e.get("evidence", "")), "date": e.get("date"), "seq": seq} for e in entries]
    kept = [e for e in rec["read"] if e["verdict"] == "REFUTED"]
    _save_record(cfg, n, {**rec, "read": kept + read})


def record_acceptance(cfg, n: int, index: int, starts: str, owner: str, date: str) -> dict:
    """Record the owner's acceptance of ONE row of settlement(cfg), in the owner's words: the row at `index`,
    which must open with `starts` (the whole item, or its first characters). Returns the row."""
    rows, rec = _open_record(cfg, n)
    row = next((r for r in rows if r["index"] == index), None)
    if row is None:
        raise RoundError(f"there is no row {index}; 'python3 -m gate changed' lists the rows")
    if not (row["item"].startswith(starts) and (len(starts) >= _MIN_EVIDENCE or starts == row["item"])):
        raise RoundError(f"row {index} does not open with {starts!r} (give the whole item or at least its first "
                         f"{_MIN_EVIDENCE} characters); it reads: {row['item']}")
    if any(dash in owner for dash in _LONG_DASHES):
        raise RoundError("the owner's words hold a dash or minus character the style check forbids (anything but "
                         "the plain hyphen); record them without it")
    entry = {"item": row["item"], "kind": row["kind"], "cut_of": row["cut_of"],
             "sha": _version(cfg, row["item"]) if row["kind"] == "chart" else None,
             "owner": owner.strip(), "date": date, "seq": _next_seq(rec)}
    _save_record(cfg, n, {**rec, "accepted": rec["accepted"] + [entry]})
    return row


def _restricted_errors(cfg) -> list:
    """A post that names an input whose terms bar redistribution keeps its results file out of the repository."""
    if not cfg.restricted_inputs:
        return []
    name = os.path.relpath(cfg.results, cfg.root)
    try:
        r = subprocess.run(["git", "-C", cfg.root, "check-ignore", "-q", cfg.results], capture_output=True, text=True)
    except OSError as e:
        return [f"cannot tell whether {name} is git-ignored ({e})"]
    if r.returncode == 1:
        return [f"{name} is not git-ignored although [post] restricted_inputs names {list(cfg.restricted_inputs)}: "
                "keep it out of the repository"]
    why = r.stderr.strip() or f"git exited with {r.returncode}"
    return [f"cannot tell whether {name} is git-ignored ({why})"] * bool(r.returncode)


def publish_check(cfg, gate_passed: bool) -> list:
    """Why the post cannot publish; [] when it can. The rule is the invariant in this module's docstring."""
    errs = [] if gate_passed else ["the gate is not green"]
    # checks that are SKIPPED while drafting cannot be skipped at publish time
    if not cfg.charts:
        errs.append("no charts script is configured, so the chart checks never ran")
    if not (cfg.mdx and os.path.exists(cfg.mdx)):
        errs.append("no published MDX is configured or found, so the published-page checks never ran")
    errs += _restricted_errors(cfg)
    try:
        s = settlement(cfg)
    except RoundError as e:
        return errs + [str(e)]
    if s["round"] < 2:
        changes = len(s["rows"]) + len(s["new_surfaces"])
        return errs + [f"{changes} thing(s) a reader sees changed since the snapshot round 1 started from "
                       "('python3 -m gate changed' lists them): run round 2 over them before publishing"] * bool(changes)
    errs += [f"new surface, covered by no round: {label}" for label in s["new_surfaces"]]
    return errs + [f"{r['state']}: {r['item']}" for r in s["rows"] if r["state"] not in SETTLED]
