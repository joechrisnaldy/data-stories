# Post 15 design: nobody quit, nobody was unemployed either

**Date:** 2026-07-29
**Series:** data-stories (Post 15)
**Folder:** `Projects/analytics-blog/quits-layoffs/`
**Title (CHOSEN):** "Nobody Quit. Nobody Was Unemployed Either."
**Slug (proposed):** `nobody-quit-nobody-was-unemployed-either`
**Data:** QLmonthly (Ellieroth & Michaud, Minneapolis Fed), CPS-based quit and layoff transition
rates, 582 months, Jan 1978 to Jun 2026, from github.com/qlmonthly/Data, also on FRED (release 738).
Plus verified BLS primary sources. NO Kaggle dataset.

## Thesis (chosen)

> Once a month the world reads two numbers to decide how the labour market feels. The quits rate
> counts people leaving a job even when they walk straight into a better one, so it measured a
> reshuffle and we called it a resignation. The unemployment rate counts only people still actively
> looking, so it loses anyone who gives up. Both numbers are real. Neither measures what we think.

## Brainstorm decisions (locked)

- **Thesis:** two famous numbers, both measuring the wrong thing.
- **Hook:** jobs report day, the monthly ritual of reading two numbers.
- **Framing:** personal, but **a single line of disclosure only** (he is job hunting and building a
  job-search tool), then the piece stays analytical.
- **Close:** turn on the reader, ask what a number counts and who it leaves out.
- **4th chart:** where the laid-off actually go, across recessions.

## The verified spine

### Number one: the quits rate measures job-switching

- BLS defines a quit as an employee who "left voluntarily at any point during the reference month",
  with **no condition on where they went**. JOLTS is establishment-based: it counts separations from
  "an establishment's payroll".
- FRED Blog (2025): **"The JOLTS data include employer-to-employer transitions, when workers move
  from one job to another without being unemployed in between."**
- BLS's own worked example (Monthly Labor Review, 2008): **"The worker who switched from
  establishment A to establishment B never became unemployed, so that worker's status would not
  change in the CPS data."** And: "assume that the number of quits rises in the JOLTS data. To infer
  the implications of such a rise, it would be useful to know where these workers went."
- **THE CONTRAST (the heart of the post):**
  - JOLTS quits rate: **2.3% average in 2019 -> 3.0% in November 2021**, a series record, 4.5 million
    quits in a single month.
  - CPS quits *into non-employment* (prime age): **0.938% in 2019 -> 0.924% in 2021-22.** Slightly
    LOWER.
  - So the Great Resignation was a record in a measure that counts job-to-job moves, while quitting
    out of work did not rise at all. A reshuffle, not an exodus.
- JOLTS begins December 2000; the CPS-based series begins 1978.

### Number two: the unemployment rate loses people who stop looking

- BLS: to be counted unemployed you must be jobless, **available**, and have **actively searched in
  the prior four weeks**. Stop searching and you are "not in the labor force", not unemployed.
- June 2026: **U-3 4.2%**, U-4 4.5%, U-5 5.2%, **U-6 7.9%**.
- **6.0 million people** not in the labour force who currently want a job, explicitly excluded.
  Marginally attached 1,761,000; discouraged workers 477,000.
- **THE KILLER STAT (BLS Monthly Labor Review, Dec 2024 flows): of people leaving unemployment,
  23.7% found work and 22.4% stopped looking and left the labour force.** Almost as many exit by
  giving up as by succeeding.
- **A live worked example, June 2026:** labour force **-720,000**, not-in-labour-force **+832,000**,
  and the unemployment rate **fell from 4.3% to 4.2%**. The number improved because people left.
- Labour force participation 61.5%, down 0.3 points in the month.

### What the QLmonthly data itself shows (computed, reproducible)

- 582 months, Jan 1978 to Jun 2026, zero missing.
- **Realism:** every recession present. 1981-82 peak layoffs 2.26% (1.79x average), Great Recession
  2.40% (1.90x), **COVID April 2020 10.71% (8.49x)** while quits collapsed 1.03% -> 0.32%.
- **Share of laid-off workers who leave the labour force rather than become unemployed:
  prime age mean 34.9%** (range 14% to 62%), **all workers 44.5%**. The Minneapolis Fed's own
  plain-language summary: about 40% exit the labour force, about 60% enter unemployment.
- **Quitters who go to non-participation: prime age 84.7%, all workers 90.9%.**
- **Layoffs exceeded quits in 514 of 582 months (88%).**
- Paper's own figures: layoffs are 20% more common than EU flows; quits 45% less common than EN
  flows, "because nearly 40% of EN transitions are actually layoffs"; layoffs contribute 15% more to
  unemployment fluctuations than EU; corr(quits, layoffs) = -0.46.

### Where we are now (context, factual only)

- JOLTS quits **1.9%** (May 2026), 3.1 million, **down 31.9% from the April 2022 peak**; lowest since
  May 2020 outside the pandemic months.
- Payrolls +57,000 in June 2026; prior 12-month average +36,000. Long-term unemployed 27.3% of all
  unemployed.
- Powell's "low-firing, low-hiring" framing (2025), restated April 2026 as "an unusual and
  uncomfortable kind of a balance". NOTE: the Fed chair changed; Kevin Warsh chaired the June 2026
  FOMC. Attribute each quote to the right person and date.
- Richmond Fed: a January 2026 hiring rate of 3.3% would historically have implied **6 to 10 percent**
  unemployment, against an actual 4.3%.
- Long-run US unemployment average 5.66%; 4.2% sits in the lowest 20% of months since 1948.

## The four charts (`quits-N-name.png`)

1. `quits-1-resignation-that-wasnt`: JOLTS quits rate (2019 -> Nov 2021 record) against CPS
   quits-into-non-employment over the same period. The thesis in one image.
2. `quits-2-vanishing`: share of laid-off workers leaving the labour force, 1978 to 2026, prime age
   and all workers.
3. `quits-3-layoffs-vs-quits`: the 48-year series, layoffs above quits in 88% of months, recessions
   marked, COVID annotated.
4. `quits-4-where-they-go`: every layoff split into still-searching versus gone from the labour
   force, compared across six recessions.

## Section spine (~1,400 to 1,900 words, no long dashes)

1. **Open, jobs report day.** The ritual: two numbers, markets move, headlines write themselves.
   One line of personal disclosure here (job hunting, building a job-search tool), then move on.
2. **The first number counts the wrong thing (chart 1).** JOLTS definition; the record; the CPS
   series that did not move; BLS's own worked example of the job-switcher.
3. **So what actually happened in 2021 (chart 3 context).** A reshuffle. Quits and layoffs move
   against each other (corr -0.46).
4. **The second number loses people (chart 2).** The active-search test; 34.9% of laid-off workers
   exit the labour force; 6.0 million want a job and are not counted; U-3 4.2% vs U-6 7.9%.
5. **The month it happened in public.** June 2026: labour force -720,000, not-in-labour-force
   +832,000, rate falls 4.3% to 4.2%. And the Dec 2024 flow: 23.7% found work, 22.4% gave up.
6. **Where the laid-off actually go (chart 4).** Six recessions, two destinations.
7. **Close, turn on the reader.** What is it counting, and who does it leave out.
8. **Method notes + References.**

## Guardrails

- **No AI causal story.** Challenger attributes 101,743 announced cuts to AI year to date, but the
  Budget Lab at Yale finds "no clear labour-market effect of AI detectable as of May 2026". If AI is
  mentioned at all, report the attribution and the absence of measured effect, and go no further.
- **Announced cuts are not measured separations.** Challenger numbers are announcements; never mix
  them with BLS measurements.
- Do **not** claim the unemployment rate is "wrong" or manipulated. It measures exactly what it
  defines. The point is the gap between the definition and the public reading of it.
- Attribute Fed quotes to the correct chair and date (Powell 2025 and April 2026; Warsh June 2026).
- Note that no household survey estimates exist for October 2025.
- No em or en dashes; APA 7 references; verified or omit.
- The personal disclosure is ONE line. This is not an essay about his job search.

## Two findings strong enough to reconsider the spine

Flag to the author before building:
- **23.7% found work vs 22.4% stopped looking** (BLS MLR, Dec 2024) is arguably the single most
  striking number in the whole post and currently has no chart.
- **U-3 4.2% vs U-6 7.9%, plus 6.0 million who want a job and are uncounted**, is the cleanest
  possible picture of number two and also has no chart.
Either could replace chart 2 or chart 4 if he wants.

## Verification plan

Sourcing complete (4 clusters, all high verifiability, verbatim primary quotes on file). Next: build
analysis + 4 charts from the QLmonthly data plus verified constants; full tables before any claim;
dash scan; Word review CHECKPOINT; adversarial fact-check with a MANDATORY round-2 recheck on changed
sections; local astro build; publish to joechrisnaldy.com.
