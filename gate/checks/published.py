"""The published MDX agrees with the draft, the charts, and the templates for its hand-written fields.

Post 25 shipped a metaDescription that still carried wording round 3 had corrected on the chart, and alt
texts with figures typed by hand at publish time; neither surface had ever been checked. The attack on
the first version of this check then showed a single-quoted field was skipped, anything after the
references was unseen, and any rendered string passed as a caption. Each of those now fails.
"""

import os
import re

from gate.text import paragraphs

_FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)
_LINE = re.compile(r"^(\w+):\s*(.*?)\s*$")
_FIGURE = re.compile(r'<figure>\s*<img src="([^"]*)" alt="([^"]*)"\s*/>\s*<figcaption>(.*?)</figcaption>\s*</figure>', re.S)
_IMG_MD = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)[ \t]*$", re.M)   # not \s*: that swallows the blank line after it
# Fields that carry no prose. Every other text field needs a [published] template; title is compared
# with the draft's heading instead.
STRUCTURAL = {"slug", "publishedAt", "updatedAt", "tags", "status", "cover", "draft", "title"}


def _norm(s: str) -> str:
    return " ".join(s.split())


def _paras(text: str) -> list:
    return [_norm(text[a:b]) for a, b in paragraphs(text)]


def _front(block: str):
    """(fields, failures). One 'key: value' per line; anything else is a failure, never a skip."""
    fields, fails = {}, []
    for line in block.split("\n"):
        if not line.strip():
            continue
        m = _LINE.match(line)
        if not m:
            fails.append(f"front matter line cannot be parsed (write each field on one line): {line[:70]!r}")
            continue
        key, raw = m.groups()
        if raw in (">", "|", ">-", "|-") or not raw:
            fails.append(f"front matter field {key!r} is folded or empty; write it on one line")
            continue
        if key in fields:
            fails.append(f"front matter field {key!r} appears twice")
        q = raw[0]
        if q in "\"'" and raw.endswith(q) and len(raw) > 1:
            raw = raw[1:-1].replace('\\"', '"') if q == '"' else raw[1:-1].replace("''", "'")
        fields[key] = raw
    return fields, fails


def parse(mdx: str):
    m = _FRONT.match(mdx)
    fields, fails = _front(m.group(1)) if m else ({}, ["the MDX has no front matter block"])
    rest = mdx[m.end():] if m else mdx
    figures = [{"src": s, "file": s.rsplit("/", 1)[-1], "alt": a, "caption": c} for s, a, c in _FIGURE.findall(rest)]
    body = _FIGURE.sub(lambda f: f"\n\n[[figure {f.group(1).rsplit('/', 1)[-1]}]]\n\n", rest)
    return fields, figures, body, fails


def _draft_sequence(rendered_md: str):
    title = re.match(r"\A#\s+([^\n]*)\n", rendered_md)
    md = rendered_md[title.end():] if title else rendered_md
    md = _IMG_MD.sub(lambda m: f"[[figure {m.group(1).rsplit('/', 1)[-1]}]]", md)
    return (title.group(1).strip() if title else None), _paras(md)


def _bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def _images(figures, cfg) -> list:
    if cfg is None:
        return []
    from gate.checks.fresh import _png_diff
    fails = []
    public = cfg.site_public
    if not public and cfg.mdx:
        d = os.path.dirname(cfg.mdx)
        while d != os.path.dirname(d) and not os.path.isdir(os.path.join(d, "public")):
            d = os.path.dirname(d)
        public = os.path.join(d, "public") if os.path.isdir(os.path.join(d, "public")) else None
    if not public:
        return ["cannot find the site's public folder to compare published images; set [post] site_public"]
    for f in figures:
        live = os.path.join(public, f["src"].lstrip("/"))     # the path the page links, never just its name
        chart = os.path.join(cfg.chart_dir, f["file"])
        if not os.path.exists(live):
            fails.append(f"published image {f['src']} does not exist at {live}")
        elif not os.path.exists(chart):
            fails.append(f"published image {f['file']} has no chart of that name in {cfg.chart_dir}")
        else:
            d = _png_diff(live, chart) if live.endswith(".png") else (None if _bytes(live) == _bytes(chart) else "bytes differ")
            if d:
                fails.append(f"published image {f['file']} differs from the chart the scripts produce: {d}")
    return fails


def check(mdx: str, rendered_md: str, capture: list, fields: dict, cfg=None) -> list:
    front, figures, body, fails = parse(mdx)
    title, draft = _draft_sequence(rendered_md)
    page = _paras(body)
    if front.get("title") != title:
        fails.append(f"published title {front.get('title')!r} is not the draft's heading {title!r}")
    if page != draft:
        i = next((k for k, (x, y) in enumerate(zip(page, draft)) if x != y), min(len(page), len(draft)))
        fails.append(f"published page differs from the rendered draft at paragraph {i + 1}: "
                     f"published {page[i][:90] if i < len(page) else '(none)'!r} vs draft {draft[i][:90] if i < len(draft) else '(none)'!r}")
    footnotes = {r["file"]: {_norm(t) for t in r.get("fig_texts", [])} for r in capture}
    for f in figures:
        if _norm(f["caption"]) not in footnotes.get(f["file"], set()):
            fails.append(f"{f['file']}: the published caption is not the chart's own footnote")
    live = {k: v for k, v in front.items() if k not in STRUCTURAL}
    live.update({f"alt:{f['file']}": f["alt"] for f in figures})
    for key, value in live.items():
        if key not in fields:
            fails.append(f"published {key} has no template in gate.toml [published]; hand-written fields must be bound")
        elif _norm(fields[key]) != _norm(value):
            fails.append(f"published {key} differs from its rendered template: {value[:80]!r} vs {fields[key][:80]!r}")
    for key in sorted(set(fields) - set(live)):
        fails.append(f"[published] {key} has a template but no such field on the published page")
    return fails + _images(figures, cfg)
