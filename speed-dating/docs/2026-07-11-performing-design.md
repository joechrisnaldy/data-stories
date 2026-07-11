# Post 05: "both are performing" (the gender gap in what we say we want)

Design doc for the fifth data story. Dataset: Kaggle
`annavictoria/speed-dating-experiment` (Columbia speed dating experiment, Fisman &
Iyengar, ~2002-2004). Folder: `analytics-blog/speed-dating/`.

Date: 2026-07-11
Status: approved POV, design pending user review

## The data (profiled)

`Speed Dating Data.csv` (latin-1 encoded), 8,378 rows (one row per date, per person),
551 subjects, 21 waves, 195 columns. Gender is binary (0 = Female, 1 = Male), roughly even
(4,184 F / 4,194 M rows). Key variables: stated "what I look for" allocations
`attr1_1, sinc1_1, intel1_1, fun1_1, amb1_1, shar1_1` (100 points across six attributes in
waves 1-5 and 10-21; a 1-10 importance scale in waves 6-9, which is a measurement wrinkle);
partner ratings `attr, sinc, intel, fun, amb, shar` (1 to 10); the yes/no `dec`; the mutual
`match`.

Confirmed findings (100-point waves for stated; all waves for revealed):

Stated allocation, mean by gender:

| | attractive | sincere | intelligent | fun | ambitious | shared |
|---|---|---|---|---|---|---|
| Women | 18.8 | 18.4 | 21.6 | 17.0 | 12.0 | 12.3 |
| Men | 29.1 | 16.2 | 19.6 | 17.7 | 7.5 | 10.3 |

Revealed: correlation of each partner-rating with the yes decision, by gender:

| | attractive | sincere | intelligent | fun | ambitious | shared |
|---|---|---|---|---|---|---|
| Women | 0.45 | 0.22 | 0.23 | 0.42 | 0.18 | 0.41 |
| Men | 0.52 | 0.19 | 0.22 | 0.41 | 0.22 | 0.39 |

Selectivity: women say yes 36.5% of the time, men 47.4%.

The read: the stated gender gap is real and stereotyped (men lead with looks at 29 points;
women lead with intelligence). But the actual choices are driven by the same three things
for both, attractiveness, fun, chemistry (shared interests). The asymmetry: the "substance"
traits women are expected to prize collapse hardest, intelligence falls from women's #1
stated to #4 revealed; ambition, which women rated above men, is women's single weakest
predictor (0.18). Men lead with looks and then choose on looks, candid.

## POV (locked with the user)

- **Angle:** the gender gap in what we say we want versus what we choose.
- **Thesis:** "both are performing." Men and women state sharply different priorities, but
  their yes/no choices are driven by the same things. The stated gap is louder than the
  real one, and it is asymmetric: the substance traits women are expected to prize evaporate
  most at decision time. Everyone's wishlist overweights substance and underweights
  chemistry; the gendered part is that women are pushed to lead with substance while men are
  allowed to admit looks. The wishlist is partly a costume; the choosing is the tell.
- **Stance held:** the data shows the say-do gap, not its cause. "Performing social norms"
  is the reading; "we are simply bad at introspection" is the rival; both can be true, and
  the essay says so. Explicitly resist the "women are hypocrites" gotcha; the point is that
  the pressure is gendered, not that one sex is dishonest.
- **Indonesia weight:** light touch. Mostly the data; one paragraph near the end on the
  gendered criteria list (ta'aruf biodata, the pressure on women to want a provider) and the
  universal lesson. Framing is universal, not Indonesia-spine.

## Title

Chosen: "Everyone Says Substance. Everyone Picks Chemistry." (states the finding, fair to
both genders, declarative in the series voice).

Alternates kept on the table:
- "The Gender Gap in Dating Is Mostly Talk"
- "The Wishlist Nobody Follows"

## Section flow (the spine)

1. **Open (stance-first).** We all make a list of what we want in a partner. The list is
   mostly aspiration; the tell is what people actually pick.
2. **The stated gap (chart 1).** The cliche, confirmed, in what people say: men's 29-point
   looks spike, women's spread toward intelligence and ambition.
3. **The revealed choices (chart 2).** What actually earns a yes, by gender: attractiveness
   first for both, the substance traits barely moving the needle.
4. **The performance (chart 3).** The say-do gap per trait: women's intelligence and
   ambition fall furthest; men lead with looks and mean it. Hold the caveat (performance
   versus self-ignorance).
5. **Close (light Indonesia + universal).** One paragraph on the gendered criteria list and
   the universal lesson: stated preferences mislead, from dating to customer surveys. The
   choosing is the truth.

## Charts (3)

Series dataviz palette. Colors by gender kept consistent across all three (for example BLUE
for women, YELLOW or AQUA for men, chosen for contrast and accessibility, decided at build).
1. Stated allocation by gender (grouped bars, six attributes).
2. Revealed: correlation of each rating with the yes decision, by gender (grouped bars).
3. The say-do gap: for each gender, each trait's stated importance versus its revealed
   weight, as a dumbbell or rank-shift, so the collapse of women's intelligence and ambition
   is the visual punchline. Stated (100-point share) and revealed (correlation) are on
   different scales, so this chart compares RANKS or normalized shares, disclosed in the
   caption.

## Method

- Stated preferences from the 100-point-allocation waves only (1-5, 10-21); waves 6-9 used a
  1-10 importance scale and are excluded from the stated-allocation figures (or normalized),
  disclosed.
- Revealed weight via the correlation of each 1-10 partner-rating with the yes decision,
  computed per gender. A simple logistic regression per gender is an optional robustness
  check; correlation is the headline for readability.
- One row per date, per rater; ratings are of the partner. Missing values dropped pairwise.

## Honesty guardrails

- Hard population and era fence: Columbia graduate and professional students, roughly
  2002-2004, a binary and heteronormative design. No projection to 2026, and no claim that
  Indonesia's numbers would match; Indonesia is framing, not measurement.
- "Performing" is an interpretation, not a measured cause; state the introspection-failure
  rival explicitly.
- Correlation, not causation; revealed "weight" is descriptive.
- The stated scale changed across waves; disclose the restriction.
- Do not reduce this to "women lie." The wishlist is aspirational for everyone; the gendered
  part is the direction of the social script.
- No long dashes; APA 7 references for every external fact.

## References (APA 7, to pin at write time)

- The source study: Fisman, R., Iyengar, S. S., Kamenica, E., & Simonson, I. (2006). Gender
  differences in mate selection: Evidence from a speed dating experiment. The Quarterly
  Journal of Economics, 121(2), 673-697. Verify exact pages and DOI at write time.
- The dataset: Kaggle (annavictoria), which redistributes the experiment's data and key.
- An Indonesian source only if a specific local claim is made in the close; otherwise the
  Indonesia paragraph stays a cultural observation, not a cited statistic.

## Scope and mechanics

- Length: weekend-sized, about 1,300 to 1,700 words.
- Folder `analytics-blog/speed-dating/` (data pulled to `data/`, gitignored except a data
  README); scripts profile_data.py, build_analysis.py, make_charts.py; results.json.
- Output: MDX to the Astro blog, slug equal to filename, status published, 3 charts copied to
  `site/public/images/blog/speeddating-*.png`, live on joechrisnaldy.com.
