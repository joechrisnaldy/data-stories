"""Render {{path:fmt}} placeholders from results.json (and sources.json for {{src:...}}).

Strict by design: an unknown key, an unknown formatter, an unclosed placeholder or a selector that does
not match exactly one element is an error, never a blank or a guess. Each resolved placeholder is
returned as a Binding so later checks know which result object every printed figure came from.
"""

import re
from dataclasses import dataclass
from typing import Any

from gate.formats import FormatError, apply


class RenderError(ValueError):
    pass


@dataclass(frozen=True)
class Binding:
    start: int            # span of the placeholder in the SOURCE text
    end: int
    origin: str           # "results" or "src"
    path: str             # dotted path as written, without the "src:" prefix
    leaf: str             # last path segment, e.g. "r"
    parent_path: str      # path of the object holding the leaf
    parent: Any           # that object (dict), for n / sample lookups
    value: Any
    fmt: str
    out: str


_PLACEHOLDER = re.compile(r"\{\{(.*?)\}\}", re.S)
_INNER = re.compile(r"^\s*(?:(src):)?\s*([^:{}]+?)\s*:\s*([a-z0-9_]+)\s*$")
_SEGMENT = re.compile(r"^([^\[\]]+)(?:\[([^=\]]+)=([^\]]+)\])?$")


def _split_path(path: str) -> list:
    parts, buf, depth = [], "", 0
    for ch in path:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "." and depth == 0:
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    parts.append(buf)
    if depth != 0 or any(not p.strip() for p in parts):
        raise RenderError(f"malformed path {path!r}")
    return [p.strip() for p in parts]


def _step(node, segment: str, so_far: str):
    m = _SEGMENT.match(segment)
    if not m:
        raise RenderError(f"malformed path segment {segment!r} after {so_far or 'the root'}")
    key, field, want = m.groups()
    if not isinstance(node, dict) or key not in node:
        avail = ", ".join(sorted(node)[:12]) if isinstance(node, dict) else type(node).__name__
        raise RenderError(f"no key {key!r} under {so_far or 'the root'} (available: {avail})")
    node = node[key]
    if field is None:
        return node
    if not isinstance(node, list):
        raise RenderError(f"selector [{field}={want}] used on {so_far + '.' + key if so_far else key}, which is not a list")
    hits = [e for e in node if isinstance(e, dict) and str(e.get(field)) == want]
    if len(hits) != 1:
        raise RenderError(f"selector [{field}={want}] under {key!r} matched {len(hits)} elements, not exactly 1")
    return hits[0]


def resolve(path: str, root: dict):
    """Return (parent_object, parent_path, leaf_name, value) for a dotted path."""
    segments = _split_path(path)
    node, walked = root, ""
    for seg in segments[:-1]:
        node = _step(node, seg, walked)
        walked = f"{walked}.{seg}" if walked else seg
    parent = node
    value = _step(node, segments[-1], walked)
    if isinstance(value, (dict, list)):
        raise RenderError(f"path {path!r} ends on a {type(value).__name__}, not a number")
    return parent, walked, segments[-1], value


_PERCENT_WORDS = {"pct", "percent", "percentage", "pc"}


def percent_unit(path: str):
    """'pct' when the key's last segment names a percentage anywhere ('growth_pct', 'pct_growth',
    'growth_percent'), 'pp' when it names percentage points, else None: the unit lives in the key's name."""
    words = set(re.split(r"[_|\[=]", re.split(r"[.\]]", path.rstrip("]"))[-1].lower()))
    return "pct" if words & _PERCENT_WORDS else "pp" if "pp" in words else None


def render(text: str, results: dict, sources: dict = None):
    """Return (rendered_text, [Binding]) or raise RenderError."""
    opens, closes = text.count("{{"), text.count("}}")
    if opens != closes:
        raise RenderError(f"unbalanced placeholders: {opens} '{{{{' against {closes} '}}}}'")
    out, bindings, last = [], [], 0
    for m in _PLACEHOLDER.finditer(text):
        inner = _INNER.match(m.group(1))
        if not inner:
            raise RenderError(f"malformed placeholder {m.group(0)!r}: expected {{{{path:formatter}}}}")
        is_src, paths, fmt = inner.groups()
        root = sources if is_src else results
        if root is None:
            raise RenderError(f"{m.group(0)!r} needs sources.json, which this post does not configure")
        # 'a.n&b.n' states one number that is the value of several keys: all must be exactly equal
        resolved = [(p.strip(), *resolve(p.strip(), root)) for p in paths.split("&")]
        values = {r[4] for r in resolved}
        if len(values) != 1:
            raise RenderError(f"{m.group(0)!r} joins keys with different values {sorted(map(str, values))}")
        value = resolved[0][4]
        for path, *_ in resolved:
            # a source figure outside 'values' is never compared with the quote, so it is never allowed
            if is_src and not re.fullmatch(r"[^.\[\]]+\.values\.[^.\[\]]+", path):
                raise RenderError(f"{m.group(0)!r}: a source placeholder is src:<id>.values.<name>, the only "
                                  "figures checked against the stored quote")
            if fmt.startswith("pct") and percent_unit(path):
                raise RenderError(f"{m.group(0)!r}: {path} is already in percent; {fmt} would multiply it by 100 "
                                  "again. Use dec0 or dec1")
        try:
            shown = apply(fmt, value)
        except FormatError as e:
            raise RenderError(f"{m.group(0)!r} ({paths.strip()} = {value!r}): {e}") from e
        out.append(text[last:m.start()])
        out.append(shown)
        last = m.end()
        for path, parent, parent_path, leaf, v in resolved:
            bindings.append(Binding(m.start(), m.end(), "src" if is_src else "results", path, leaf,
                                    parent_path, parent, v, fmt, shown))
    out.append(text[last:])
    rendered = "".join(out)
    if "{{" in rendered or "}}" in rendered:
        raise RenderError("braces left in the rendered text: a placeholder is misordered or unclosed")
    return rendered, bindings
