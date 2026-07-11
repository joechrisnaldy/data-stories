# Post 03 blog version: Indonesia spine

Design doc for the website (Astro blog) version of Post 03. The GitHub repo already
carries the methods-focused essay ("The Dataset That Already Knew the Answer"); this
is the differentiated blog version, rebuilt around an Indonesian reader.

Date: 2026-07-10
Status: approved design, pending build

## The reframe

The GitHub essay is about a measurement trap in the abstract. The blog version lands
that trap where it actually bites: Indonesia, a country with 150M+ young, mobile-first
gamers and a live moral panic about "kecanduan game."

The opening is not a single scary statistic. It is the spread of them. Published
prevalence estimates for internet gaming disorder among Indonesian adolescents run from
about 1.9% to about 30.8%, a roughly sixteen-fold gap, depending on the instrument and
the sample. That spread is the whole argument in miniature: a "measurement" that swings
that hard is not measuring one fixed thing. The definition is doing the work. The
synthetic dataset then explains, mechanically, how a definition can manufacture its own
answer.

## Thesis

Measure before you panic. Indonesia has real reasons to care about kids and screens, but
the "addiction" numbers driving the alarm swing sixteen-fold depending on how you measure,
and the dataset that promises to define addiction turns out to have built its answer from
its own inputs. A country this young and this online deserves real measurement, not a
mirror.

## Title

Chosen: "The Gaming-Addiction Number Nobody Checked" (declarative, contrarian, matches
the Post 01 and Post 02 voice).

Alternates kept on the table:
- "One in Fifty, or One in Three? Indonesia's Gaming-Addiction Problem"
- "Before Indonesia Panics About Gaming, Check the Number"

## Section flow (the spine)

1. **The spread.** Open on 1.9% versus 30.8% among Indonesian adolescents. Same country,
   same "disorder," a sixteen-fold gap. Every panic quotes whichever number suits it. What
   could make a measurement swing that hard? The definition.
2. **What is an "addiction score," really?** Pivot to the Kaggle dataset as a stand-in for
   how these scores get built (250 gamers, 49 columns, synthetic).
3. **Chart 1 (formula).** The score is arithmetic: cross-validated R square of 0.91,
   rebuilt from its own inputs. Not a measurement; the inputs rearranged.
4. **Chart 2 (made of).** A plausible composite (hours plus impulse-control plus
   impairment), which is exactly what makes it seductive. The mental-health scales it is
   named for load least of all.
5. **Chart 3 (harm small).** The harm the label promises is, at most, small on this
   synthetic data. Hard caveat: this is a fact about a constructed dataset, not about real
   Indonesian gamers; gaming disorder is a real, WHO-recognized condition; real research
   also finds small and mixed effects.
6. **Chart 4 (tells).** The giveaways of a manufactured dataset (burnout pinned at 1.0 for
   99%, GPA pinned at the 4.0 ceiling for 71%).
7. **Land it (Indonesia).** Circular scores guarantee alarming answers; that is how you
   manufacture an epidemic on paper. Before Indonesia medicalizes or legislates, demand to
   know how "addiction" was defined. Name the transferable trap (engagement defined as
   time-in-app, a health score built from usage). Close on the stakes: 150M young players
   deserve a real number.

## Charts

Reuse the existing four charts as-is; they are already leakage-clean and honest. No
fabricated "Indonesia chart": there is no Indonesian micro-data here, and inventing a
visual would betray the essay's own argument. Not charting what we cannot measure is the
on-brand, honest choice.

Files copied to the site as `gamingaddiction-01..04.png` under
`site/public/images/blog/`.

## Scope and mechanics

- Length: weekend-sized, about 1,600 to 1,900 words.
- Output: MDX to the Astro blog at `site/src/content/blog/`, slug equal to filename,
  `status: published`, date 2026-07-10.
- Tags: Data, Indonesia, Mental Health (final set decided at build).
- Frontmatter: title, slug, excerpt, publishedAt (date), tags, status, seoTitle,
  metaDescription (per the site convention used by Posts 01 and 02).

## References (APA 7, to pin exact author and year at build)

Real, citable sources identified in research; exact citations to be verified against the
source pages before publishing:

- Indonesian adolescent IGD prevalence, low end (about 1.9%): the 1,233-youth study using
  the Indonesian ten-item IGD test (PLOS One).
- Indonesian adolescent IGD prevalence, high end (about 30.8%): the Banda Aceh
  cross-sectional study (Acta Biomedica / multi-settings study). Makassar (~30%) available
  as a secondary corroborating figure.
- WHO ICD-11 recognition of "gaming disorder" (World Health Organization).
- Indonesia gaming scale and mobile-first split (150M+ gamers, ~83% on smartphones,
  largest market in Southeast Asia): Newzoo or an equivalent market source.

If a specific figure cannot be verified cleanly against its source at build time, it gets
dropped or replaced; no number goes in unsourced.

## Honesty guardrails (carried from the analysis)

- Never imply the synthetic data describes real Indonesians.
- Keep the "gaming disorder is real" caveat explicit.
- The critique is of circular measurement, not of the dataset's author or of legitimate
  concern for young people.
- No long dashes; APA 7 references for every external fact (repo CONVENTIONS.md).
