# Everyone Says Substance. Everyone Picks Chemistry.: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Post 05, a data essay showing that men and women state sharply different partner priorities but choose on the same things (attractiveness, fun, chemistry), with the "substance" traits women are expected to prize collapsing hardest at decision time.

**Architecture:** Content build, not TDD software. Reuse the series pipeline (profile -> analyze -> chart -> draft -> verify -> MDX -> publish). The analysis compares STATED preference allocations by gender (100-point waves only) against REVEALED weight (correlation of each partner-rating with the yes decision) by gender. Verification is data sanity checks against numbers already profiled, citation checks, a long-dash scan, a slug match, and a clean Astro build.

**Tech Stack:** Python (pandas, numpy) in the reused venv at `sberbank-housing/.venv`; Astro MDX site; series dataviz palette.

**Design doc:** `Projects/analytics-blog/speed-dating/docs/2026-07-11-performing-design.md`

**Rules (repo CONVENTIONS.md):** no long dashes; APA 7 references for every external fact. **Live blog domain is `joechrisnaldy.com` (NOT .app).** CSV is latin-1 encoded.

**Numbers already profiled (sanity targets):** stated allocation women intel 21.6 / attr 18.8 / amb 12.0; men attr 29.1 / amb 7.5. Revealed corr with `dec`: women attr 0.45 / amb 0.18; men attr 0.52. Yes-rate women 0.365, men 0.474. 8,378 rows, 551 subjects, 21 waves.

---

## File map

- Create: `speed-dating/profile_data.py`
- Create: `speed-dating/build_analysis.py` (stated by gender, revealed corr by gender, normalized shares, ranks, yes-rate; writes `results.json`)
- Create: `speed-dating/make_charts.py` (3 charts)
- Create: `speed-dating/results.json`
- Create: `speed-dating/data/README.md` (Kaggle download note; data gitignored)
- Create: `speed-dating/README.md` (storytelling README)
- Create: `speed-dating/docs/2026-07-11-performing-references-verified.md`
- Create: `speed-dating/draft/everyone-says-substance-everyone-picks-chemistry.md` and `.docx` (gitignored)
- Create: `site/public/images/blog/speeddating-1-stated.png`, `-2-revealed.png`, `-3-say-do-gap.png`
- Create: `site/src/content/blog/everyone-says-substance-everyone-picks-chemistry.mdx`
- Modify: `Projects/analytics-blog/README.md` (Post 05 row)

Data already downloaded to `speed-dating/data/Speed Dating Data.csv` (+ the `.doc` key).

---

### Task 1: Profile script

**Files:** Create `speed-dating/profile_data.py`

- [ ] **Step 1: Write the profiler**

```python
"""Profile the Columbia speed dating dataset: shape, gender split, the stated
preference and revealed rating columns that the essay is built on."""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "Speed Dating Data.csv", encoding="latin-1")
print("rows:", len(df), "| subjects:", df.iid.nunique(), "| waves:", df.wave.nunique())
print("gender rows (0=F,1=M):", df.gender.value_counts().to_dict())
STATED = ["attr1_1", "sinc1_1", "intel1_1", "fun1_1", "amb1_1", "shar1_1"]
RATE = ["attr", "sinc", "intel", "fun", "amb", "shar"]
print("stated cols present:", [c for c in STATED if c in df.columns])
print("rating cols present:", [c for c in RATE if c in df.columns])
print("dec present:", "dec" in df.columns, "| match present:", "match" in df.columns)
print("100-pt-allocation waves rows (exclude 6-9):", (~df.wave.isin([6,7,8,9])).sum())
```

- [ ] **Step 2: Run it**

Run: `cd speed-dating && ../sberbank-housing/.venv/bin/python profile_data.py`
Expected: 8,378 rows, 551 subjects, 21 waves; all stated and rating cols present; dec and match present.

---

### Task 2: Analysis

**Files:** Create `speed-dating/build_analysis.py`; writes `speed-dating/results.json`

- [ ] **Step 1: Write the analysis**

```python
"""Stated vs revealed partner preferences by gender.
STATED: mean of the 100-point 'what I look for' allocation (attr1_1..shar1_1),
computed on the 100-point-allocation waves only (exclude waves 6-9, which used a
1-10 importance scale). REVEALED: correlation of each 1-10 partner-rating with the
yes decision (dec), by gender. Both are also normalized to a share of importance so
they can be compared on one axis, and ranked 1..6."""
import json
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "Speed Dating Data.csv", encoding="latin-1")

ATTRS = ["attr", "sinc", "intel", "fun", "amb", "shar"]
STATED = [a + "1_1" for a in ATTRS]
GENDER = {0: "Female", 1: "Male"}

pt = df[~df.wave.isin([6, 7, 8, 9])]  # 100-point allocation waves only

stated, revealed, stated_share, revealed_share, ranks = {}, {}, {}, {}, {}
for gv, gl in GENDER.items():
    s = pt[pt.gender == gv][STATED].mean()
    s.index = ATTRS
    stated[gl] = {a: round(float(s[a]), 1) for a in ATTRS}
    ssum = float(s.sum())
    stated_share[gl] = {a: round(float(s[a]) / ssum, 3) for a in ATTRS}

    sub = df[df.gender == gv]
    corr = {a: round(float(sub[[a, "dec"]].dropna().corr().iloc[0, 1]), 3) for a in ATTRS}
    revealed[gl] = corr
    csum = sum(corr.values())
    revealed_share[gl] = {a: round(corr[a] / csum, 3) for a in ATTRS}

    stated_rank = {a: r for r, a in enumerate(sorted(ATTRS, key=lambda x: -s[x]), 1)}
    revealed_rank = {a: r for r, a in enumerate(sorted(ATTRS, key=lambda x: -corr[x]), 1)}
    ranks[gl] = {a: {"stated": stated_rank[a], "revealed": revealed_rank[a]} for a in ATTRS}

results = {
    "n_rows": int(len(df)),
    "n_subjects": int(df.iid.nunique()),
    "n_waves": int(df.wave.nunique()),
    "n_stated_rows": int(pt[STATED].dropna(how="all").shape[0]),
    "attrs": ATTRS,
    "stated_by_gender": stated,
    "revealed_corr_by_gender": revealed,
    "stated_share_by_gender": stated_share,
    "revealed_share_by_gender": revealed_share,
    "ranks_by_gender": ranks,
    "yes_rate_by_gender": {GENDER[gv]: round(float(df[df.gender == gv].dec.mean()), 3)
                            for gv in GENDER},
}
(BASE / "results.json").write_text(json.dumps(results, indent=2))
print("stated women:", stated["Female"])
print("stated men:", stated["Male"])
print("revealed women:", revealed["Female"])
print("revealed men:", revealed["Male"])
print("yes-rate:", results["yes_rate_by_gender"])
print("women intelligence rank stated->revealed:",
      ranks["Female"]["intel"]["stated"], "->", ranks["Female"]["intel"]["revealed"])
```

- [ ] **Step 2: Run and sanity-check**

Run: `cd speed-dating && ../sberbank-housing/.venv/bin/python build_analysis.py`
Expected (must match the profiled numbers): stated women intel 21.6 / attr 18.8 / amb 12.0; men attr 29.1 / amb 7.5. Revealed women attr 0.45 / amb 0.18; men attr 0.52. Yes-rate women 0.365, men 0.474. Women intelligence rank should move from near the top stated (1) to mid revealed (about 4). If any headline number is off, stop and debug before charts.

---

### Task 3: Charts

**Files:** Create `speed-dating/make_charts.py`; writes `speed-dating/charts/*.png`

- [ ] **Step 1: Write the chart script** using the series palette (BLUE #2a78d6, AQUA #1baf7a, YELLOW #eda100, RED #e34948, INK #0b0b0b, INK2 #52514e, MUTED #898781, GRID #e1e0d9, BASELINE #c3c2b7, SURFACE #fcfcfb), reading `results.json`, with women and men in two consistent colors across all charts (for example BLUE = women, YELLOW = men; state the legend on each). Pretty attribute labels (attr -> attractive, sinc -> sincere, intel -> intelligent, fun -> fun, amb -> ambitious, shar -> shared interests). Produce:
  1. `01_stated.png`: grouped horizontal bars, stated allocation (points) per attribute by gender. Title conveys "what people say they want." Annotate men's attractiveness spike and women's intelligence/ambition.
  2. `02_revealed.png`: grouped horizontal bars, correlation of each rating with the yes decision by gender. Title conveys "what actually earns a yes." Show attractiveness leading for both.
  3. `03_say_do_gap.png`: the money chart. For each gender, a dumbbell per attribute connecting stated_share to revealed_share (both 0 to 1 shares of importance, disclosed in the footnote), so the drop of women's intelligence and ambition is visible. Alternatively use ranks (1..6 stated vs revealed) if clearer; decide at build and disclose the scale in a footnote. No long dashes in any chart text.

- [ ] **Step 2: Run and eyeball**

Run: `cd speed-dating && ../sberbank-housing/.venv/bin/python make_charts.py`
Expected: 3 PNGs in `charts/`, each non-empty, no label collisions. Read each PNG back and fix any overlap before proceeding.

---

### Task 4: Pin the citations

**Files:** Create `speed-dating/docs/2026-07-11-performing-references-verified.md`

- [ ] **Step 1: Verify the source study.** WebSearch / WebFetch to confirm the citation for Fisman, Iyengar, Kamenica & Simonson (2006), "Gender Differences in Mate Selection: Evidence from a Speed Dating Experiment," The Quarterly Journal of Economics, and pin the volume (121), issue (2), page range, and DOI. Also confirm one headline finding to corroborate (women more selective; men respond more to physical attractiveness) so the essay can cite the origin study for external validity.
- [ ] **Step 2: Record the dataset citation** (Kaggle, annavictoria, speed-dating-experiment; the data and key redistribute the Columbia experiment).
- [ ] **Step 3: Write each confirmed source as an APA 7 entry** into the references file, annotated with the claim it supports. If the Indonesia close makes a specific local claim (for example a statistic about arranged marriage or biodata), add and verify a source for it; otherwise keep the Indonesia paragraph a cultural observation with no statistic.

---

### Task 5: Data-download note and storytelling README

**Files:** Create `speed-dating/data/README.md` and `speed-dating/README.md`

- [ ] **Step 1: Write `data/README.md`** with the Kaggle source (`annavictoria/speed-dating-experiment`), the CLI download command, the latin-1 encoding note, and the wave-scale wrinkle (waves 6-9 used a 1-10 stated scale; the analysis restricts stated preferences to the 100-point waves).
- [ ] **Step 2: Write `speed-dating/README.md`** as the storytelling README (the argument in the three charts, a how-the-analysis-works table, reproduce steps, method and caveats), matching the style of `fifa-2026/README.md`. Link the live essay URL on joechrisnaldy.com once known.

---

### Task 6: Draft the essay for author review

**Files:** Create `speed-dating/draft/everyone-says-substance-everyone-picks-chemistry.md` and its `.docx`

Draft ~1,300 to 1,700 words following the five-section spine in the design doc, using numbers from `results.json`. Match the author's voice from `a-model-can-be-86-percent-right-and-useless.mdx` (lead with a stance; short declarative sentences; one honest caveat per risky claim).

Required content anchors (each MUST appear):
- Open stance-first: the wishlist of what we want in a partner is mostly aspiration; the tell is what people actually pick.
- The stated gap: men allocate 29 points to attractiveness, women lead with intelligence (21.6) and rate ambition above men (12.0 vs 7.5).
- The revealed choices: attractiveness is the top predictor of a yes for both (women 0.45, men 0.52); fun and shared interests close behind; the substance traits barely move the decision.
- The performance and its asymmetry: women's intelligence falls from #1 stated to about #4 revealed, and ambition is their weakest predictor (0.18); men lead with looks and choose on looks. Everyone overweights substance in words; the gendered part is the direction of the script.
- The held caveat: the data shows the say-do gap, not its cause; performing norms vs poor introspection; both can be true. Population and era fence (Columbia grad students, roughly 2002-2004, binary and heteronormative). Do not say "women lie."
- Light Indonesia close and the universal lesson (stated preferences mislead, from dating to customer surveys). The selectivity gap (women 37%, men 47% say yes) may appear as supporting color.

Guardrails: no long dashes; correlation not causation; Indonesia is framing, not measurement.

- [ ] **Step 1: Write the draft markdown** with figures as image references to `../charts/*.png` (so the Word export embeds them).
- [ ] **Step 2: Convert to Word** via `../sberbank-housing/md_to_docx.py`.
- [ ] **Step 3: Long-dash scan.** `grep -nP "[\x{2014}\x{2013}]" draft/*.md || echo clean`. Expected: clean.
- [ ] **Step 4: AUTHOR REVIEW GATE.** Hand the `.docx` to Jonathan. Do not proceed until he approves or gives edits.

---

### Task 7: Adversarial verification (before handoff)

Run a four-agent Workflow over the draft, scoped to: (a) numbers match `results.json` (stated allocations, revealed correlations, ranks, yes-rate); (b) logic and intellectual honesty (the say-do gap held as descriptive; "performing" flagged as interpretation with the introspection rival; NO "women lie" gotcha; population/era fence present; correlation-not-causation); (c) facts (the Fisman et al. citation and any Indonesia claim match the pinned sources); (d) voice and no-long-dash. Fix confirmed issues, re-run the dash scan, and if prose changed re-confirm with the author.

(Per the Post 03/04 lesson, do this BEFORE the author reads it, so he reviews a clean draft. Reorder Task 6 Step 4 to follow this if executing that way.)

---

### Task 8: Build the MDX page

**Files:** Create `site/src/content/blog/everyone-says-substance-everyone-picks-chemistry.mdx`

- [ ] **Step 1: Copy charts into the site** as `speeddating-1-stated.png`, `speeddating-2-revealed.png`, `speeddating-3-say-do-gap.png`, from `speed-dating/charts/` to `site/public/images/blog/`. Verify each is non-empty.
- [ ] **Step 2: Write the frontmatter** (match the Post 02/03/04 shape exactly):

```yaml
---
title: "Everyone Says Substance. Everyone Picks Chemistry."
slug: "everyone-says-substance-everyone-picks-chemistry"
excerpt: "<one to two sentences from the approved draft; single quotes only, no long dashes>"
publishedAt: 2026-07-11
tags: ["Data", "Psychology", "Gender"]
status: published
seoTitle: "Everyone Says Substance. Everyone Picks Chemistry. - Jonathan Chrisnaldy"
metaDescription: "<about 150 chars, no long dashes, no internal double quotes>"
---
```
Slug MUST equal the filename base.

- [ ] **Step 3: Paste the approved prose; convert each chart to site figure markup** using the exact filenames from Step 1 (`<figure><img src="/images/blog/speeddating-..." alt="..." /><figcaption>...</figcaption></figure>`). Write real alt text and captions.
- [ ] **Step 4: Add the `## References` block** mirroring the APA 7 markdown-link format at the end of `a-model-can-be-86-percent-right-and-useless.mdx`, populated from the verified references file.
- [ ] **Step 5: Long-dash scan on the MDX.** Expected: clean.
- [ ] **Step 6: Confirm slug equals filename.**

---

### Task 9: Build the site and verify it renders

- [ ] **Step 1: Build.** `cd site && npm run build`. Expected EXIT 0 and the route `/blog/everyone-says-substance-everyone-picks-chemistry/index.html` generated.
- [ ] **Step 2: Guard the image-optimizer side effect.** After the build, `git status --short` will show the optimizer re-encoded pre-existing blog images. `git restore public/images/blog/` to revert those; re-copy the raw Post 05 charts so only the new `speeddating-*.png` are added. (Same issue handled in Posts 03/04.)
- [ ] **Step 3: Verify the built HTML** at `dist/client/blog/everyone-says-substance-everyone-picks-chemistry/index.html`: correct title, three `speeddating-*.png` refs, all section headings, References block. (Dev-server port 4321 may be taken by another session; verifying the built HTML is sufficient.)

---

### Task 10: Update the series index

**Files:** Modify `Projects/analytics-blog/README.md`

- [ ] **Step 1: Add the Post 05 row** to the series table, linking `https://joechrisnaldy.com/blog/everyone-says-substance-everyone-picks-chemistry` as the live essay and `speed-dating/` as the analysis. Use `.com`.
- [ ] **Step 2: Dash-scan the README.**

---

### Task 11: PUBLISH GATE (author-triggered)

Do these only when Jonathan says go. Publishing pushes to two repos.

- [ ] **Step 1: Commit and push the portfolio site** (`site/` repo, remote `joechrisnaldy-portfolio`, branch `main`) with only the new MDX, the new `speeddating-*.png`, and the auto-maintained `.published-slugs.json`. Triggers the Vercel deploy. **Verify live on `https://joechrisnaldy.com/...` (NOT .app).**
- [ ] **Step 2: Commit and push the analytics-blog repo** (Post 05 folder: code, `results.json`, README, docs, data/README.md; NOT `draft/` or `data/*.csv` which are gitignored) plus the series-index README update.
- [ ] **Step 3: Update memory** (`analytics-blog-workflow.md`): Post 05 shipped, live `.com` URL, thesis, gotchas (latin-1, wave-scale wrinkle).

---

## Self-review

- **Spec coverage:** thesis and stance (Tasks 2, 6), stated gap (chart 1), revealed choices (chart 2), say-do gap with asymmetry (chart 3, Task 2 ranks), the held caveat + population fence + no-gotcha (Task 6 anchors, Task 7 checks), light Indonesia close (Task 6), wave-scale restriction (Tasks 2, 5), APA 7 (Tasks 4, 8). All present.
- **Placeholder scan:** excerpt/metaDescription/alt/captions filled from the approved draft at Task 8; the Fisman citation and any Indonesia claim are explicit verification tasks. No orphan TODOs.
- **Consistency:** chart filenames identical across Task 8 Step 1 and Step 3; slug identical across Task 8 and the filename; ATTRS / stated_by_gender / revealed_corr_by_gender field names consistent across Tasks 2 and 3; domain `.com` throughout; latin-1 encoding used in every read.
- **Review gates:** author Word review (Task 6 / reordered with Task 7), adversarial verify (Task 7), publish gate (Task 11) explicit and ordered.
