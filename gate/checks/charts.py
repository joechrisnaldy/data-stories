"""What a chart prints must agree with what it plots, and its hand-typed text is held to the prose rules.

panel_counts reads the 'n = X' a panel actually renders and compares it with the points actually drawn
on that panel. The previous check recomputed n from its own copy of the data and never looked at the
chart, so a hardcoded 'n = 250' annotation passed.
"""

import ast
import re

# 'per 100,000 people', 'COVID-19 cases' and 'G20 countries' are rates and names, not counts
_N_SHOWN = re.compile(r"\bn\s*=\s*([\d,]+)|(?<![\w,.\-])(?<!per )(?<!per\u00a0)([\d,]+)\s+(?:of\s+them|(?:former\s+)?"
                      r"(?:countries|colonies)|observations|entities|places|points|territories|nations|economies|cases|"
                      r"rows|people|respondents)\b", re.I)
_NON_TEXT = re.compile(r"^(?:[A-Za-z_][\w|.\-]*|#[0-9a-fA-F]{3,8}|.*\.(?:png|json|dta|csv|txt|md|py)|[^\s]*[\\/][^\s]*)$")


def prose_texts(record: dict) -> list:
    """Everything a figure renders except tick labels: what claims and figure checks read."""
    return record.get("prose", record.get("texts", []))


def _shown(texts) -> set:
    return {int((m.group(1) or m.group(2)).replace(",", "")) for t in texts for m in _N_SHOWN.finditer(t)}


def panel_counts(records: list) -> list:
    """Each panel's own text (annotations, title, axis labels, legend) against its points; on a
    single-panel figure the footnote and other figure-level text too. A multi-panel footnote may report a
    statistic that is not drawn (Post 25's chart 2 gives the all-country n beside its colonies-only
    panels), so it is not compared; its figures are still checked as results by chart_figures."""
    fails = []
    for rec in records:
        plotted = [ax for ax in rec["axes"] if ax["points"]]   # a colorbar or an empty axes is not a panel
        if len(plotted) == 1:
            for n in sorted(_shown(rec.get("fig_texts", []))):
                if n != plotted[0]["points"]:
                    fails.append(f"{rec['file']}: the figure text prints n = {n} but its one panel plots "
                                 f"{plotted[0]['points']} points")
        for i, ax in enumerate(rec["axes"]):
            shown = _shown(ax["texts"])
            for n in sorted(shown):
                if not ax["points"]:
                    fails.append(f"{rec['file']} panel {i + 1}: prints n = {n} but plots no countable points")
                elif n != ax["points"]:
                    fails.append(f"{rec['file']} panel {i + 1}: prints n = {n} but plots {ax['points']} points")
    return fails


def _docstring_ids(tree) -> set:
    ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                ids.add(id(first.value))
    return ids


def literal_strings(script_path: str) -> dict:
    """Hand-typed strings in a charts script that could reach a rendered figure, keyed by line."""
    with open(script_path) as f:
        tree = ast.parse(f.read())
    skip = _docstring_ids(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript):
            skip.update(id(n) for n in ast.walk(node.slice))
        if isinstance(node, (ast.Assert, ast.Raise)):       # error messages never reach a figure
            skip.update(id(n) for n in ast.walk(node))
        if isinstance(node, ast.FormattedValue) and node.format_spec is not None:
            skip.update(id(n) for n in ast.walk(node.format_spec))
    out = {}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in skip
                and node.value.strip() and not _NON_TEXT.match(node.value.strip())):
            key = f"{script_path.rsplit('/', 1)[-1]}:{node.lineno}"
            out[key] = (out.get(key, "") + " " + node.value).strip()
    return out
