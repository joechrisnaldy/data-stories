# Nobody Builds a World Cup Team at Home Anymore: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Post 04, "Nobody Builds a World Cup Team at Home Anymore," an Indonesia-framed data essay showing that nearly every 2026 World Cup qualifier fields a squad employed at foreign clubs, and holding the tension that "built abroad" is employment, not development.

**Architecture:** Content build, not TDD software. Reuse the series pipeline (profile -> analyze -> chart -> draft -> verify -> MDX -> publish). The one novel technical piece is a club-to-country lookup for the 234 clubs in `players.csv`, which powers a per-nation foreign-based share. Verification is data sanity checks, citation checks against sources, a long-dash scan, a slug/filename match, and a clean Astro build.

**Tech Stack:** Python (pandas, numpy, matplotlib, scipy) in the reused venv at `sberbank-housing/.venv`; Astro MDX site; the series dataviz palette.

**Design doc:** `Projects/analytics-blog/fifa-2026/docs/2026-07-11-built-abroad-design.md`

**Rules (repo CONVENTIONS.md):** no long dashes (em or en); APA 7 references for every external fact. **Live blog domain is `joechrisnaldy.com` (NOT .app).**

---

## File map

- Create: `fifa-2026/profile_data.py` (shape, club coverage, distinct clubs, first look)
- Create: `fifa-2026/club_country.csv` (the club-to-country lookup; the crux; committed)
- Create: `fifa-2026/build_analysis.py` (foreign-based share per nation, league concentration, writes `results.json`)
- Create: `fifa-2026/make_charts.py` (3 to 4 charts)
- Create: `fifa-2026/results.json`
- Create: `fifa-2026/data/README.md` (Kaggle download note; data gitignored)
- Create: `fifa-2026/README.md` (storytelling README for the repo)
- Create: `fifa-2026/docs/2026-07-11-built-abroad-references-verified.md` (pinned citations)
- Create: `fifa-2026/draft/nobody-builds-a-world-cup-team-at-home-anymore.md` and `.docx` (gitignored)
- Create: `site/public/images/blog/worldcup2026-1..N-*.png` (chart copies)
- Create: `site/src/content/blog/nobody-builds-a-world-cup-team-at-home-anymore.mdx`
- Modify: `Projects/analytics-blog/README.md` (series index row for Post 04)

Data already downloaded to `fifa-2026/data/` (matches.csv, teams.csv, players.csv).

---

### Task 1: Profile script (lock the shape)

**Files:** Create `fifa-2026/profile_data.py`

- [ ] **Step 1: Write the profiler**

```python
"""Profile the FIFA 2026 dataset: shapes, club coverage, distinct clubs, squad sizes."""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
players = pd.read_csv(BASE / "data" / "players.csv")
teams = pd.read_csv(BASE / "data" / "teams.csv")
matches = pd.read_csv(BASE / "data" / "matches.csv")

print("players:", players.shape, "| teams:", teams.shape, "| matches:", matches.shape)
played = players[players.games.fillna(0) > 0]
print("played:", len(played), "| club known:", played.club.notna().sum())
print("distinct clubs (played):", played.club.dropna().nunique())
clubs = sorted(played.club.dropna().unique())
(BASE / "clubs_list.txt").write_text("\n".join(clubs))
print("wrote clubs_list.txt with", len(clubs), "clubs")
print("nations:", players.team.nunique())
```

- [ ] **Step 2: Run it**

Run: `cd fifa-2026 && ../sberbank-housing/.venv/bin/python profile_data.py`
Expected: players (1035, 72); ~627 played; ~556 club known; ~234 distinct clubs; writes `clubs_list.txt`.

---

### Task 2: Club-to-country lookup (the crux)

**Files:** Create `fifa-2026/club_country.csv` (columns: `club,country`)

The foreign-based metric depends entirely on mapping each club to the country whose league it plays in. Do this deliberately and spot-check it; do not guess silently.

- [ ] **Step 1: Generate the club list with player counts**

```bash
cd fifa-2026 && ../sberbank-housing/.venv/bin/python - <<'EOF'
import pandas as pd
p = pd.read_csv("data/players.csv")
pl = p[p.games.fillna(0) > 0]
vc = pl.club.dropna().value_counts()
vc.to_csv("clubs_with_counts.csv", header=["n_players"])
print("wrote clubs_with_counts.csv:", len(vc), "clubs")
EOF
```

- [ ] **Step 2: Build `club_country.csv`**

Create `club_country.csv` mapping every club in `clubs_with_counts.csv` to the country of the league it plays in (for example `Bayern Munich,Germany`; `Al-Hilal,Saudi Arabia`; `PSV,Netherlands`; `Toluca,Mexico`; `Celtic,Scotland`). Map the clubs by recognition; for any club you are unsure of, verify against a quick web search rather than guessing. Coverage target: every club with a player. Unmapped clubs are handled in Task 3 (flagged, not dropped silently).

- [ ] **Step 3: Verify coverage**

```bash
cd fifa-2026 && ../sberbank-housing/.venv/bin/python - <<'EOF'
import pandas as pd
clubs = set(pd.read_csv("clubs_with_counts.csv").iloc[:,0])
mapped = set(pd.read_csv("club_country.csv").club)
missing = sorted(clubs - mapped)
print("clubs:", len(clubs), "| mapped:", len(clubs & mapped), "| MISSING:", len(missing))
if missing: print("MISSING:", missing)
EOF
```
Expected: MISSING is empty. If not, add the missing clubs and rerun.

---

### Task 3: Analysis (foreign-based share + league concentration)

**Files:** Create `fifa-2026/build_analysis.py`; writes `fifa-2026/results.json`

- [ ] **Step 1: Write the analysis**

```python
"""Foreign-based share per nation and league concentration for WC 2026 squads.
Foreign-based = club country not equal to the national-team country.
Computed over players with a known, mapped club. Unmapped clubs are reported."""
import json
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
p = pd.read_csv(BASE / "data" / "players.csv")
cc = pd.read_csv(BASE / "club_country.csv").set_index("club").country.to_dict()

played = p[p.games.fillna(0) > 0].copy()
known = played[played.club.notna()].copy()
known["club_country"] = known.club.map(cc)

unmapped = known[known.club_country.isna()]
mapped = known[known.club_country.notna()].copy()
# team_country is the national team's country; foreign if club country differs
mapped["abroad"] = mapped.club_country != mapped.team_country

by_nation = (mapped.groupby("team")
             .agg(n=("player", "size"), abroad=("abroad", "sum")))
by_nation["foreign_share"] = (by_nation.abroad / by_nation.n).round(3)
by_nation = by_nation.sort_values("foreign_share", ascending=False)

league_conc = mapped.club_country.value_counts()

results = {
    "n_players_total": int(len(p)),
    "n_played": int(len(played)),
    "n_club_known": int(len(known)),
    "n_unmapped": int(len(unmapped)),
    "unmapped_clubs": sorted(unmapped.club.dropna().unique().tolist()),
    "n_nations": int(mapped.team.nunique()),
    "overall_foreign_share": round(float(mapped.abroad.mean()), 3),
    "by_nation": by_nation.reset_index().to_dict(orient="records"),
    "league_concentration": league_conc.head(20).to_dict(),
    "home_based_examples": by_nation.sort_values("foreign_share").head(6).reset_index()[["team", "foreign_share", "n"]].to_dict(orient="records"),
}
(BASE / "results.json").write_text(json.dumps(results, indent=2))
print("overall foreign share:", results["overall_foreign_share"])
print("unmapped players:", results["n_unmapped"])
print("top league dests:", list(league_conc.head(6).items()))
```

- [ ] **Step 2: Run it and sanity-check**

Run: `cd fifa-2026 && ../sberbank-housing/.venv/bin/python build_analysis.py`
Expected: `n_unmapped` is 0 (or a small, named set). Overall foreign share is high (roughly 0.6 to 0.8 expected). Home-based examples include Mexico and other big-league hosts. If a "home-based" nation is actually a big-league nation (England, Spain), note that nuance for the essay (home-based can mean elite domestic league, not weak talent).

- [ ] **Step 3: Manual gut-check against the raw data**

Confirm Morocco, Japan, Senegal show near-1.0 foreign share and Mexico shows a low one, matching the profiling seen during brainstorming. If not, debug the mapping before proceeding.

---

### Task 4: Charts

**Files:** Create `fifa-2026/make_charts.py`; writes `fifa-2026/charts/*.png`

- [ ] **Step 1: Write the chart script** using the series palette (BLUE #2a78d6, AQUA #1baf7a, YELLOW #eda100, RED #e34948, INK #0b0b0b, INK2 #52514e, MUTED #898781, GRID #e1e0d9, BASELINE #c3c2b7, SURFACE #fcfcfb), reading `results.json`. Produce:
  1. `01_foreign_share.png`: ranked foreign-based share across the 40 nations (horizontal bars), with a labeled annotation for Indonesia's would-be position as an EXTERNAL note (not a data bar).
  2. `02_league_concentration.png`: where the world's WC players are employed (top league countries by player count).
  3. `03_home_based.png`: the home-based counterexamples (lowest foreign-share nations), with a note distinguishing elite-domestic-league from small-league.
  4. (Optional) `04_*.png` only if a clean visual for the employment-not-development tension emerges; otherwise stop at 3.

Write real titles, axis labels, and footnotes. No long dashes in any chart text.

- [ ] **Step 2: Run and eyeball**

Run: `cd fifa-2026 && ../sberbank-housing/.venv/bin/python make_charts.py`
Expected: 3 (or 4) PNGs in `charts/`, each non-empty, no label collisions.

---

### Task 5: Pin the citations

**Files:** Create `fifa-2026/docs/2026-07-11-built-abroad-references-verified.md`

Verify each external fact against its source before it goes in the essay.

- [ ] **Step 1: Verify Indonesia's 2026 qualifying run and naturalization program.** WebSearch / WebFetch to confirm: how far Indonesia reached in AFC qualifying (the 4th round claim), the naturalization of Dutch-Indonesian / Eredivisie-based players, and the 2026 coaching situation (Patrick Kluivert). Record exact, dated, sourced statements. If a specific claim cannot be verified, soften or drop it.
- [ ] **Step 2: Verify a football labor-migration source** for the "built abroad" context (for example a CIES Football Observatory expatriate-players report). Record the citation actually used.
- [ ] **Step 3: Write each confirmed source as an APA 7 entry** into the references file, each annotated with the exact claim it supports. This file is the single source of truth for the essay's References block.

---

### Task 6: Data-download note and storytelling README

**Files:** Create `fifa-2026/data/README.md` and `fifa-2026/README.md`

- [ ] **Step 1: Write `data/README.md`** with the Kaggle source (`wasiqaliyasir/fifa-match-player-and-team-dataset-2026`), the CLI download command, and a note that it is an early snapshot (created 2026-06-19, 20 matches).
- [ ] **Step 2: Write `fifa-2026/README.md`** as the storytelling README (the argument in the charts, a "how the analysis works" table, reproduce steps, method and caveats), matching the style of `gaming-mental-health/README.md`. Link the live essay URL on `joechrisnaldy.com` once known.

---

### Task 7: Draft the essay for author review

**Files:** Create `fifa-2026/draft/nobody-builds-a-world-cup-team-at-home-anymore.md` and its `.docx`

Draft ~1,600 to 1,900 words following the five-section spine in the design doc, using numbers from `results.json` and citations from Task 5. Match the author's voice from `a-model-can-be-86-percent-right-and-useless.mdx` (lead with a stance; short declarative sentences; one honest caveat per risky claim).

Required content anchors (each MUST appear):
- Open on Indonesia's near-miss and naturalization, and the home debate.
- The finding: overall foreign-based share and the ranked spread; Morocco / Japan / Senegal near the top, Mexico and big-league hosts near the bottom.
- Where "abroad" means Europe: the league concentration figure.
- The held tension: `club` is employment, not development; the data cannot separate grow-and-export from import-and-naturalize; home-based can mean an elite domestic league, not weak talent.
- Close on Indonesia: naturalization bought presence, not a pipeline; both sides held.
- The snapshot caveat framed as a strength: squad composition is fully observed even though the 20-match performance stats are thin, so the argument does not lean on them.

Guardrails: no long dashes; Indonesia is framing, not in the dataset (no data claim about Indonesia); no causal claim that building abroad causes qualifying.

- [ ] **Step 1: Write the draft markdown** with figures noted inline as image references to `../charts/*.png` (so the Word export embeds them).
- [ ] **Step 2: Convert to Word** via `../sberbank-housing/md_to_docx.py` (input md, output docx).
- [ ] **Step 3: Long-dash scan.** `grep -nP "[\x{2014}\x{2013}]" draft/nobody-builds-a-world-cup-team-at-home-anymore.md || echo clean`. Expected: clean.
- [ ] **Step 4: AUTHOR REVIEW GATE.** Hand the `.docx` to Jonathan. Do not proceed until he approves or gives edits.

---

### Task 8: Adversarial verification (before handoff)

Run a four-agent Workflow over the draft, scoped to: (a) numbers match `results.json` (foreign shares, league counts, coverage); (b) logic and intellectual honesty (employment-not-development held; no overclaim; Indonesia framing kept out of the data claims; the elite-league nuance present); (c) facts (Indonesia qualifying and naturalization and the labor-migration source match the pinned citations exactly); (d) voice and no-long-dash. Fix confirmed issues, re-run the dash scan, and if prose changed re-confirm with the author.

(Per the Post 03 lesson, do this BEFORE the author reads it, so he reviews a clean draft. Reorder Task 7 Step 4 to follow this if executing that way.)

---

### Task 9: Build the MDX page

**Files:** Create `site/src/content/blog/nobody-builds-a-world-cup-team-at-home-anymore.mdx`

- [ ] **Step 1: Copy charts into the site** as `worldcup2026-1-foreign-share.png`, `worldcup2026-2-leagues.png`, `worldcup2026-3-home-based.png` (and `-4-*` if a fourth exists), from `fifa-2026/charts/` to `site/public/images/blog/`. Verify each is non-empty.
- [ ] **Step 2: Write the frontmatter** (match the Post 02/03 shape exactly):

```yaml
---
title: "Nobody Builds a World Cup Team at Home Anymore"
slug: "nobody-builds-a-world-cup-team-at-home-anymore"
excerpt: "<one to two sentences from the approved draft; single quotes only, no long dashes>"
publishedAt: 2026-07-11
tags: ["Data", "Indonesia", "Football"]
status: published
seoTitle: "Nobody Builds a World Cup Team at Home Anymore - Jonathan Chrisnaldy"
metaDescription: "<about 150 chars, no long dashes, no internal double quotes>"
---
```
Slug MUST equal the filename base.

- [ ] **Step 3: Paste the approved prose; convert each chart to site figure markup** using the exact filenames from Step 1:

```html
<figure>
  <img src="/images/blog/worldcup2026-1-foreign-share.png" alt="<real alt text>" />
  <figcaption><real caption></figcaption>
</figure>
```

- [ ] **Step 4: Add the `## References` block** mirroring the APA 7 markdown-link format at the end of `a-model-can-be-86-percent-right-and-useless.mdx`, populated from the verified references file.
- [ ] **Step 5: Long-dash scan on the MDX.** Expected: clean.
- [ ] **Step 6: Confirm slug equals filename.** `grep '^slug:' ...mdx` returns `nobody-builds-a-world-cup-team-at-home-anymore`.

---

### Task 10: Build the site and verify it renders

- [ ] **Step 1: Build.** `cd site && npm run build`. Expected EXIT 0 and the route `/blog/nobody-builds-a-world-cup-team-at-home-anymore/index.html` generated.
- [ ] **Step 2: Guard the image optimizer side effect.** After the build, `git status --short` will show the optimizer re-encoded pre-existing blog images. `git restore public/images/blog/` to revert those; re-copy the raw Post 04 charts so only the new `worldcup2026-*.png` are added. (Same issue handled in Post 03.)
- [ ] **Step 3: Preview-verify** via `preview_start` (astro-dev) that the route is 200, all charts load, captions and References render, and the console is clean. Screenshot as proof.

---

### Task 11: Update the series index

**Files:** Modify `Projects/analytics-blog/README.md`

- [ ] **Step 1: Add the Post 04 row** to the series table, linking `https://joechrisnaldy.com/blog/nobody-builds-a-world-cup-team-at-home-anymore` as the live essay and `fifa-2026/` as the analysis. Use `.com`, not `.app`.
- [ ] **Step 2: Dash-scan the README.**

---

### Task 12: PUBLISH GATE (author-triggered)

Do these only when Jonathan says go. Publishing pushes to two repos.

- [ ] **Step 1: Commit and push the portfolio site** (`site/` repo, remote `joechrisnaldy-portfolio`, branch `main`) with only the new MDX, the new `worldcup2026-*.png`, and the auto-maintained `.published-slugs.json`. This triggers the Vercel deploy. **Verify live on `https://joechrisnaldy.com/...` (NOT .app; .app is detached).**
- [ ] **Step 2: Commit and push the analytics-blog repo** (Post 04 folder: code, `club_country.csv`, `results.json`, README, docs, data/README.md; NOT `draft/` or `data/*` which are gitignored; NOT `clubs_list.txt`/`clubs_with_counts.csv` scratch unless wanted) plus the series-index README update.
- [ ] **Step 3: Update memory** (`analytics-blog-workflow.md`): Post 04 shipped, live `.com` URL, thesis, any gotchas.

---

## Self-review

- **Spec coverage:** thesis and stance (Tasks 3, 7), Indonesia bookend (Task 7 anchors), foreign-based share (Tasks 2, 3, chart 1), league concentration (chart 2), home-based counterexamples (chart 3), held tension employment-not-development (Tasks 3 note, 7 anchor, 8 check), snapshot-as-strength (Task 7 anchor), no fabricated Indonesia chart (Task 4), APA 7 (Tasks 5, 9), honesty guardrails (Tasks 3, 7, 8). All present.
- **Placeholder scan:** the excerpt/metaDescription/alt/captions are filled from the approved draft at Task 9 (they depend on final prose); the club mapping and citations are explicit verification tasks, not deferred hand-waves. No orphan TODOs.
- **Consistency:** chart filenames identical across Task 9 Step 1 and Step 3; slug identical across Task 9 and the filename; foreign_share / by_nation / club_country field names consistent across Tasks 2, 3, 4; domain is `.com` throughout.
- **Review gates:** author Word review (Task 7 / reordered with Task 8), adversarial verify (Task 8), publish gate (Task 12) explicit and ordered.
