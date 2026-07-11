# The Gaming-Addiction Number Nobody Checked: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the Indonesia-spine blog version of Post 03 ("The Gaming-Addiction Number Nobody Checked") as MDX on the Astro portfolio, reusing the four existing charts, with every external fact cited in APA 7.

**Architecture:** This is a content build, not software. The analysis and its numbers are already computed and verified in `results.json`; the four charts already exist. The new work is (1) pinning real Indonesian citations, (2) drafting the re-spined essay for the author's review, (3) wiring it into the site as MDX with the site's frontmatter and figure conventions. Verification is citation-checking against source pages, a long-dash scan, a slug/filename match, and a clean site build, not unit tests.

**Tech Stack:** Astro content collection (MDX), existing matplotlib PNGs, Python `md_to_docx` helper for the review draft.

**Design doc:** `Projects/analytics-blog/gaming-mental-health/docs/2026-07-10-indonesia-blog-design.md`

**Convention rules (repo CONVENTIONS.md):** no long dashes (em or en) anywhere; APA 7 references for every external fact at the end of the page.

---

## File map

- Create: `Projects/analytics-blog/gaming-mental-health/draft/the-gaming-addiction-number-nobody-checked.md` (review draft, gitignored)
- Create: `Projects/analytics-blog/gaming-mental-health/draft/the-gaming-addiction-number-nobody-checked.docx` (Word review, gitignored)
- Create: `Projects/analytics-blog/gaming-mental-health/docs/2026-07-10-references-verified.md` (pinned citations, committed)
- Create: `Projects/joechrisnaldy-portfolio/site/public/images/blog/gamingaddiction-1-formula.png` (copy)
- Create: `.../gamingaddiction-2-madeof.png`, `.../gamingaddiction-3-harm.png`, `.../gamingaddiction-4-tells.png` (copies)
- Create: `Projects/joechrisnaldy-portfolio/site/src/content/blog/the-gaming-addiction-number-nobody-checked.mdx`

Numbers come from `Projects/analytics-blog/gaming-mental-health/results.json` (already verified). Do not recompute; reuse.

---

### Task 1: Pin the Indonesian citations

**Files:**
- Create: `Projects/analytics-blog/gaming-mental-health/docs/2026-07-10-references-verified.md`

The opening rests on real numbers. Verify each against its source page before it goes in the essay. If a figure cannot be confirmed on the page, drop or replace it; no number ships unsourced.

- [ ] **Step 1: Fetch and confirm the low-end prevalence figure**

WebFetch `https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0269528`
Confirm: the IGD prevalence estimate (about 1.90%) among the ~1,233 Indonesian youth sample, and record authors, year, journal, title, DOI.

- [ ] **Step 2: Fetch and confirm the high-end prevalence figure**

WebFetch `https://www.mattioli1885journals.com/index.php/actabiomedica/article/view/15826`
Confirm: the ~30.8% gaming-disorder figure among Indonesian adolescents (Banda Aceh / multi-settings), and record full citation. If the article page is thin, fall back to the PDF at `https://www.mattioli1885journals.com/index.php/actabiomedica/article/download/15826/12123/126785`.

- [ ] **Step 3: Confirm the WHO gaming-disorder definition**

WebFetch a WHO ICD-11 page for "gaming disorder" (search `https://www.who.int` if the direct URL is unknown). Confirm gaming disorder is classified in ICD-11 and record the WHO citation (year of the ICD-11 release used).

- [ ] **Step 4: Confirm the market-scale context figure**

Confirm the "150M+ Indonesian gamers, mobile-first (~83% on smartphones), largest market in Southeast Asia" context from a citable source (Newzoo, or the Xsolla/Allcorrect summaries that attribute Newzoo). Record the citation actually used. If only a secondary source is available, cite the secondary source honestly.

- [ ] **Step 5: Write the verified reference list**

Write each confirmed source as an APA 7 entry into `docs/2026-07-10-references-verified.md`, each with the exact figure it supports noted in a comment. This file is the single source of truth for the essay's References block.

- [ ] **Step 6: Commit**

```bash
cd /Users/jonathanchrisnaldy/Claude-Workspace/Projects/analytics-blog
git add gaming-mental-health/docs/2026-07-10-references-verified.md
git commit -m "docs: pin verified APA 7 citations for post 03 Indonesia blog"
```

---

### Task 2: Copy the four charts into the site

**Files:**
- Create the four `gamingaddiction-*.png` files under `site/public/images/blog/`

- [ ] **Step 1: Copy with the site naming convention**

```bash
SRC=/Users/jonathanchrisnaldy/Claude-Workspace/Projects/analytics-blog/gaming-mental-health/charts
DST=/Users/jonathanchrisnaldy/Claude-Workspace/Projects/joechrisnaldy-portfolio/site/public/images/blog
cp "$SRC/01_formula.png"   "$DST/gamingaddiction-1-formula.png"
cp "$SRC/02_made_of.png"   "$DST/gamingaddiction-2-madeof.png"
cp "$SRC/03_harm_small.png" "$DST/gamingaddiction-3-harm.png"
cp "$SRC/04_tells.png"     "$DST/gamingaddiction-4-tells.png"
```

- [ ] **Step 2: Verify all four copied and non-empty**

```bash
ls -l /Users/jonathanchrisnaldy/Claude-Workspace/Projects/joechrisnaldy-portfolio/site/public/images/blog/gamingaddiction-*.png
```
Expected: four files listed, each with a non-zero byte size.

---

### Task 3: Draft the essay for author review

**Files:**
- Create: `gaming-mental-health/draft/the-gaming-addiction-number-nobody-checked.md`
- Create: `.docx` sibling via the repo's md-to-docx helper

Draft the full essay (about 1,600 to 1,900 words) following the seven-section spine in the design doc. Use the verified numbers from Task 1 and `results.json`. Match the author's voice from `a-model-can-be-86-percent-right-and-useless.mdx` (lead with a stance; short declarative sentences; one honest caveat paragraph per risky claim).

Required content anchors (each MUST appear):
- Open on the prevalence spread: about 1.9% versus about 30.8% among Indonesian adolescents, a roughly sixteen-fold gap, same country, same "disorder."
- Pivot: what is an "addiction score," really? Introduce the Kaggle dataset (250 gamers, 49 columns, synthetic).
- Chart 1 point: cross-validated R square of 0.91 rebuilding the score from its own inputs; daily playtime alone 0.74.
- Chart 2 point: a plausible composite (hours 0.74 to 0.86; missed deadlines 0.47; impulsiveness and self-control drive it yet barely correlate with hours); the mental-health scales load least.
- Chart 3 point: harm is at most small on this synthetic data (sleep -0.40, stress 0.33 robust; anxiety 0.14 small but real; depression and loneliness not distinguishable from zero on n=250). Hard caveat: this is about a constructed dataset, not real Indonesian gamers; gaming disorder is real and WHO-recognized; real research also finds small and mixed effects.
- Chart 4 point: the tells (burnout 1.0 for ~99%, GPA 4.0 for ~71%).
- Land it: circular scores guarantee alarming answers; that is how you get a paper epidemic; before Indonesia medicalizes or legislates, ask how "addiction" was defined; name the transferable trap (engagement as time-in-app, health score as usage); close on 150M young players deserving a real number.

Guardrails: no long dashes; keep the "gaming disorder is real" caveat explicit; never imply the synthetic data describes real Indonesians; the critique is of circular measurement, not of the dataset's author.

- [ ] **Step 1: Write the draft markdown**

Write the essay to `gaming-mental-health/draft/the-gaming-addiction-number-nobody-checked.md` with a plain title line and the prose (no MDX frontmatter yet; figures noted inline as `[CHART 1: formula]` placeholders for the review read).

- [ ] **Step 2: Convert to Word for review**

Use the same md-to-docx approach as Post 01 (`sberbank-housing/md_to_docx.py` pattern) to produce the `.docx` sibling in `draft/`. If a reusable script exists, call it; otherwise write a tiny one-off using python-docx in the reused venv.

- [ ] **Step 3: Long-dash scan on the draft**

```bash
grep -nP "[\x{2014}\x{2013}]" /Users/jonathanchrisnaldy/Claude-Workspace/Projects/analytics-blog/gaming-mental-health/draft/the-gaming-addiction-number-nobody-checked.md || echo "clean: no long dashes"
```
Expected: `clean: no long dashes`.

- [ ] **Step 4: AUTHOR REVIEW GATE**

Hand the `.docx` to Jonathan for review (his established Word-review step). Do not proceed to Task 4 until he approves the prose or gives edits. Apply edits, then re-run Step 3.

---

### Task 4: Adversarial verification of the new material

The last time this dataset was written up, a four-agent adversarial pass caught two real intellectual-honesty errors (an overstated "just hours" and an absence-of-evidence "no harm" claim). Re-run that check, scoped to the new Indonesian framing plus a full read.

- [ ] **Step 1: Run the verification workflow**

Dispatch four parallel reviewers over the approved draft: (a) numbers (every figure matches `results.json` and Task 1 citations), (b) logic (no absence-of-evidence claims; the circularity claim stays "composite," not "just hours"), (c) facts (the Indonesian statistics and WHO claim match the pinned sources exactly), (d) voice (matches the Post 02 register; no long dashes). Collect only confirmed issues.

- [ ] **Step 2: Fix confirmed issues in the draft, re-run the dash scan, and if any prose changed, re-confirm with the author.**

---

### Task 5: Build the MDX page

**Files:**
- Create: `site/src/content/blog/the-gaming-addiction-number-nobody-checked.mdx`

- [ ] **Step 1: Write the frontmatter**

```yaml
---
title: "The Gaming-Addiction Number Nobody Checked"
slug: "the-gaming-addiction-number-nobody-checked"
excerpt: "<one to two sentences, drawn from the 1.9% versus 30.8% spread and the circular-score finding>"
publishedAt: 2026-07-10
tags: ["Data", "Indonesia", "Mental Health"]
status: published
seoTitle: "The Gaming-Addiction Number Nobody Checked - Jonathan Chrisnaldy"
metaDescription: "<about 150 characters: Indonesia's gaming-addiction stats swing sixteenfold; a look at how an addiction score can be built from its own inputs.>"
---
```
Slug MUST equal the filename base. Fill the excerpt and metaDescription from the approved draft; keep metaDescription near 150 characters and free of long dashes.

- [ ] **Step 2: Paste the approved prose and insert the four figures**

Replace each `[CHART N]` placeholder with the site figure markup, using the exact filenames from Task 2:

```html
<figure>
  <img src="/images/blog/gamingaddiction-1-formula.png" alt="Scatter of predicted versus actual addiction_score; points hug the diagonal, cross-validated R squared 0.91." />
  <figcaption>A plain linear model rebuilds the addiction score from the other columns at R squared 0.91. Daily playtime alone reaches 0.74.</figcaption>
</figure>
```
Repeat for `gamingaddiction-2-madeof.png`, `gamingaddiction-3-harm.png`, `gamingaddiction-4-tells.png` with alt text and captions matching each chart's point from Task 3. Write real alt text and captions, not placeholders.

- [ ] **Step 3: Add the References block**

Append a `## References` section that mirrors the APA 7 formatting used at the end of `a-model-can-be-86-percent-right-and-useless.mdx`, populated from `docs/2026-07-10-references-verified.md`.

- [ ] **Step 4: Long-dash scan on the MDX**

```bash
grep -nP "[\x{2014}\x{2013}]" /Users/jonathanchrisnaldy/Claude-Workspace/Projects/joechrisnaldy-portfolio/site/src/content/blog/the-gaming-addiction-number-nobody-checked.mdx || echo "clean: no long dashes"
```
Expected: `clean: no long dashes`.

- [ ] **Step 5: Confirm slug equals filename**

```bash
cd /Users/jonathanchrisnaldy/Claude-Workspace/Projects/joechrisnaldy-portfolio/site/src/content/blog
grep '^slug:' the-gaming-addiction-number-nobody-checked.mdx
```
Expected: `slug: "the-gaming-addiction-number-nobody-checked"` (matches the filename base).

---

### Task 6: Build the site and confirm the page renders

- [ ] **Step 1: Build**

Run the site's build (from the design of Posts 01 and 02, the site is the Astro app under `site/`). Use `preview_start` / the project's dev or build command and confirm the new blog route compiles with the four images resolving. Check the console and build logs for errors referencing the new slug or missing images.

- [ ] **Step 2: Verify the four images resolve and the References render.** Fix any broken path or MDX parse error, then rebuild.

---

### Task 7: Update the series index and repo README (analytics-blog)

**Files:**
- Modify: `Projects/analytics-blog/README.md` (Post 03 row: change "Essay forthcoming" to the live essay link)
- Modify: `Projects/analytics-blog/gaming-mental-health/README.md` (remove the "blog essay is in progress" line; link the live post)

- [ ] **Step 1: Update both READMEs to point at the live essay URL** `https://joechrisnaldy.app/blog/the-gaming-addiction-number-nobody-checked`.

- [ ] **Step 2: Dash scan both, then commit (analytics-blog repo only).**

```bash
cd /Users/jonathanchrisnaldy/Claude-Workspace/Projects/analytics-blog
grep -rnP "[\x{2014}\x{2013}]" README.md gaming-mental-health/README.md || echo "clean"
git add README.md gaming-mental-health/README.md gaming-mental-health/docs/2026-07-10-indonesia-blog-design.md gaming-mental-health/docs/2026-07-10-indonesia-blog-plan.md
git commit -m "docs: link post 03 live blog essay; add Indonesia blog design + plan"
```

---

### Task 8: PUBLISH GATE (author-triggered)

Publishing pushes to two remotes and goes live. Do these only when Jonathan says go.

- [ ] **Step 1: Push the portfolio site** (`joechrisnaldy-portfolio`), which triggers the Vercel deploy.
- [ ] **Step 2: Push the analytics-blog repo** to GitHub.
- [ ] **Step 3: Confirm the live URL renders and update memory** (`analytics-blog-workflow.md`): Post 03 blog PUBLISHED, Indonesia spine, with the live URL.

---

## Self-review

- **Spec coverage:** thesis (Task 3 landing), spine sections 1 to 7 (Task 3 anchors), scary-statistic open (Task 1 + Task 3), one-anchor-stat-plus-light-context (Task 1 four sources), reuse four charts and no fabricated chart (Task 2, Task 5), frontmatter and slug convention (Task 5), APA 7 references (Task 1, Task 5 Step 3), honesty guardrails (Task 3, Task 4). All present.
- **Placeholders:** the excerpt and metaDescription are intentionally filled from the approved draft at Task 5 Step 1 (they depend on the final prose); chart alt/captions are specified as "write real text" with one worked example. No orphan TODOs.
- **Consistency:** image filenames (`gamingaddiction-1-formula`, `-2-madeof`, `-3-harm`, `-4-tells`) are identical across Task 2 and Task 5. Slug is identical across Task 5 and the filename. Numbers sourced only from `results.json` and Task 1.
- **Review gates:** author Word review (Task 3), adversarial verify (Task 4), publish gate (Task 8) are explicit and ordered.
