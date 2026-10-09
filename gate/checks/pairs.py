"""Like-for-like figures from different samples in one paragraph must each show their sample size.

Structural, not lexical: a value counts as a statistic of a sample when the result object holding it
has an 'n'. The previous gate matched phrases like 'on each side', which could be appended to silence
it, and worked per sentence, which a full stop evaded. Neither is possible here.

A comparison is between statistics of the same kind (an r beside an r, a t beside a t), so figures are
grouped by their leaf name; a correlation next to an income range is not a comparison. A paragraph that
legitimately relies on an n stated elsewhere needs a [pairs] entry in gate.toml with a reason.
"""

from gate.text import body_and_refs, paragraphs


def _group_fails(kind: str, stats: dict, shown_n: set, snippet: str) -> list:
    """[(message, object path)] for one kind of statistic in one paragraph."""
    missing_ids = [p for p, obj in stats.items() if "sample" not in obj]
    if missing_ids:
        return [(f"'{kind}' figures from {len(stats)} result objects share a paragraph but {p} has no sample id; "
                 f"the build script must emit one: {snippet}", p) for p in missing_ids]
    if len({obj["sample"] for obj in stats.values()}) == 1:
        return []
    return [(f"{path}.{kind} (n={obj['n']}) is set beside '{kind}' figures from other samples but its n is not "
             f"shown in the paragraph: {snippet}", path) for path, obj in stats.items() if obj["sample"] not in shown_n]


def check(source: str, bindings, exempt: dict = None) -> list:
    """exempt: {phrase: {"reason": ..., "paths": [result object paths]}}. An exemption excuses only the
    paths it names, in a paragraph containing its phrase; anything added to that paragraph later is still
    reported, and an entry or path that excuses nothing is stale."""
    exempt = exempt or {}
    body, _ = body_and_refs(source)
    fails, used = [], set()
    paras = paragraphs(body)
    # an exemption names the opening words of exactly one paragraph: matched anywhere, a reused phrase or a
    # placeholder key excused paragraphs written later
    opening = lambda a, b: " ".join(body[a:b].split()).lstrip("*_#> ")
    opens = {ph: [i for i, (a, b) in enumerate(paras) if opening(a, b).startswith(" ".join(ph.split()).lstrip("*_#> "))]
             for ph in exempt}
    for ph, hits in opens.items():
        if len(hits) > 1:
            fails.append(f"[pairs] entry {ph!r} opens {len(hits)} paragraphs; it must open exactly one")
    for i, (a, b) in enumerate(paras):
        inside = [x for x in bindings if x.origin == "results" and a <= x.start and x.end <= b]
        groups = {}
        for x in inside:
            if isinstance(x.parent, dict) and "n" in x.parent and x.leaf != "n":
                groups.setdefault(x.leaf, {})[x.parent_path] = x.parent
        shown_n = {x.parent.get("sample") for x in inside if x.leaf == "n" and isinstance(x.parent, dict)}
        snippet = " ".join(body[a:b].split())[:140]
        excused = {(phrase, path) for phrase, e in exempt.items() if opens[phrase] == [i] for path in e["paths"]}
        for kind, stats in groups.items():
            if len(stats) < 2:
                continue
            for f, path in _group_fails(kind, stats, shown_n, snippet):
                hit = [(ph, p) for ph, p in excused if p == path]
                if hit:
                    used.update(hit)
                else:
                    fails.append(f)
    for phrase, e in exempt.items():
        for path in e["paths"]:
            if (phrase, path) not in used:
                fails.append(f"[pairs] entry {phrase!r} path {path!r} excuses nothing: remove it")
    return fails
