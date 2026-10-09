"""Run a charts script with savefig instrumented, recording what each saved figure actually shows.

Invoked as a subprocess by checks/fresh.py:  python3 -m gate.chart_capture <script> <out.json>
For each saved figure: every visible string ('texts', for style), the same minus tick labels ('prose',
for claims and figures), the tick labels ('ticks'), figure-level text such as the footnote ('fig_texts',
for captions), and per axes the finite points actually plotted and the axes' own text, title, axis labels and legend.
"""

import json
import os
import runpy
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.collections as mcoll  # noqa: E402
import matplotlib.figure as mfig  # noqa: E402
import matplotlib.lines as mlines  # noqa: E402
import matplotlib.text as mtext  # noqa: E402
import numpy as np  # noqa: E402

RECORDS = []
_ORIGINAL = mfig.Figure.savefig


def _points(ax) -> int:
    n = 0
    for c in ax.collections:
        if isinstance(c, mcoll.PathCollection):
            off = np.ma.filled(np.ma.asarray(c.get_offsets(), dtype=float), np.nan)
            n += int(np.isfinite(off).all(axis=1).sum()) if off.size else 0
    for line in ax.get_lines():
        if line.get_marker() not in (None, "", "None", " ") and line.get_linestyle() in ("None", "", " "):
            xy = np.column_stack([np.asarray(line.get_xdata(), float), np.asarray(line.get_ydata(), float)])
            n += int(np.isfinite(xy).all(axis=1).sum())
    return n


def _texts(fig) -> list:
    artists = list(fig.findobj(mtext.Text))
    for ax in fig.axes:
        for tbl in ax.tables:
            artists += [cell.get_text() for cell in tbl.get_celld().values()]
    seen, out = set(), []
    for t in artists:
        if id(t) not in seen and t.get_visible() and t.get_text().strip():
            seen.add(id(t))
            out.append(t)
    return out


def _spy(self, fname, *args, **kwargs):
    self.canvas.draw()
    ticks = {id(t) for ax in self.axes for t in ax.get_xticklabels() + ax.get_yticklabels()
             + ax.get_xticklabels(minor=True) + ax.get_yticklabels(minor=True)}
    texts = _texts(self)
    axes = []
    for ax in self.axes:
        legend = ax.get_legend()
        own = [t.get_text() for t in ax.texts] + [ax.get_title(loc) for loc in ("left", "center", "right")]
        own += [ax.get_xlabel(), ax.get_ylabel()]
        own += [t.get_text() for t in legend.get_texts()] if legend else []
        axes.append({"points": _points(ax), "texts": [t for t in own if t.strip()]})
    supt = [self._suptitle.get_text()] if getattr(self, "_suptitle", None) else []
    RECORDS.append({"file": os.path.basename(str(fname)),
                    "texts": [t.get_text() for t in texts],
                    "prose": [t.get_text() for t in texts if id(t) not in ticks],
                    "ticks": [t.get_text() for t in texts if id(t) in ticks],
                    "fig_texts": [t.get_text() for t in self.texts if t.get_text().strip()] + supt,
                    "axes": axes})
    return _ORIGINAL(self, fname, *args, **kwargs)


def main(script: str, out: str) -> None:
    mfig.Figure.savefig = _spy
    sys.argv = [script]
    runpy.run_path(script, run_name="__main__")
    with open(out, "w") as f:
        json.dump(RECORDS, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
