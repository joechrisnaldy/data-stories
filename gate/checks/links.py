"""Every image the draft links to exists."""

import os
import re

_IMG = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


def check(rendered: str, draft_dir: str) -> list:
    return [f"image link does not resolve: {m.group(1)}" for m in _IMG.finditer(rendered)
            if not m.group(1).startswith(("http://", "https://"))
            and not os.path.exists(os.path.normpath(os.path.join(draft_dir, m.group(1))))]
