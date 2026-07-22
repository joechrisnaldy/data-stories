# Post 13 design: the dataset that can't see smoking (lung cancer & selection bias)

**Date:** 2026-07-21
**Series:** data-stories (Post 13)
**Folder:** `Projects/analytics-blog/lung-cancer/`
**Title (CHOSEN):** "The Internet's Favorite Lung-Cancer Dataset Says Smoking Is Harmless. It Isn't."
**Slug / filename base:** `the-lung-cancer-dataset-that-cant-see-smoking` (confirm at publish)
**Dataset:** Kaggle `mysarahmadbhat/lung-cancer` ("survey lung cancer.csv"), a real but small,
self-selected online survey (309 rows, CC0, 2021). Used as a FOIL/specimen, not as evidence for
causation. Vetted: real (not synthetic), but structurally unable to answer its own title question.

## The idea

The most-downloaded lung-cancer dataset on Kaggle is titled "Does Smoking cause Lung Cancer." Run the
obvious analysis and smoking looks irrelevant, it ranks dead last as a predictor of cancer, behind
allergy and alcohol. That is a selection-bias trap: the sample is 87% cancer patients with no control
group, so nothing predicts cancer and the real cause flattens into noise. The essay uses that failure
to teach the trap, while relentlessly anchoring the real, settled truth: smoking causes the large
majority of lung cancer, and there is no safe level.

## Thesis (chosen)

> Smoking's harm is so certain that a broken dataset cannot dent it. A famous, convenient file can make
> the strongest finding in medicine disappear, and if you trust the file over the evidence, you learn
> the exact opposite of the truth.

Spine: **truth-forward** (public-health truth is the anchor; the selection-bias lesson rides
underneath, never over it).

## Brainstorm decisions (locked)

- **Thesis:** smoking's harm is so certain that bad data can't dent it (truth-forward).
- **Hook:** a human stake, specifically **a data-science learner** (one of the 174 people who built a
  model on this file and "learned" smoking is irrelevant), a confident wrong conclusion.
- **Framing:** universal + ONE **light Indonesia touch** (one section: Indonesia among the world's
  highest male smoking rates, why getting this right matters locally).
- **Behavior thread:** keep it **strict, smoking vs cancer**; do NOT wander into the peer-pressure /
  alcohol columns except as a symptom of the trap.
- **GUARDRAIL (non-negotiable):** never imply smoking is safe or harmless. Repeatedly affirm the real
  truth, tobacco harms your health at any level, **there is no safe amount**. "The data can't detect
  smoking's effect" must never read as "smoking is fine."
- **Close:** **turn on the learner**, the data wasn't lying, it just couldn't see, and neither could
  you; next time a tidy file hands you a comfortable answer, remember the one that "proved" smoking is
  harmless.
- **Title (chosen):** "The Internet's Favorite Lung-Cancer Dataset Says Smoking Is Harmless. It Isn't."

## What the data shows (from the vet; foil only)

- 309 rows, 16 cols, 0 missing, but **33 exact duplicate rows** (real-survey messiness).
- Target **87.4% cancer** (270 YES / 39 NO), self-selected "online prediction system" sample, no
  control group.
- **Smoking does not significantly predict cancer here:** P(cancer|smoker) 0.891 vs 0.852; Fisher
  exact **OR 1.42, p = 0.39**.
- **Smoking ranks LAST of 15** as a correlate of cancer (r = 0.058), below allergy (0.33), alcohol
  (0.29), swallowing difficulty (0.26), wheezing/coughing (0.25).
- Smoking is not even correlated with yellow fingers (-0.01) or coughing (-0.13) here, its real-world
  tells, further evidence the sample is too selected to carry the real relationships.

## The four charts (foil = Kaggle data; truth = verified real sources)

1. `lung-1-ranks-last` (Kaggle): the 15 features ranked by correlation with cancer; SMOKING at the
   bottom, allergy/alcohol on top. The seduction.
2. `lung-2-no-control` (Kaggle): 87% of the sample already has cancer; smoker vs non-smoker cancer
   rates nearly identical (89% vs 85%). When everyone is sick, nothing predicts sickness.
3. `lung-3-real-risk` (VERIFIED real epidemiology): smokers' relative risk of lung cancer ~15-30x, and
   ~80-90% of lung cancer caused by smoking. The truth the file can't hold. Include the no-safe-level
   point.
4. `lung-4-indonesia` (VERIFIED real data): Indonesia in global context, among the world's highest
   male smoking rates. Local stakes.

## Section spine (~1,200-2,000 words, no long dashes)

1. **Open, the learner.** Downloads the top lung-cancer file, runs the obvious model, concludes smoking
   is the least important thing about lung cancer. Confident and wrong.
2. **The seduction (chart 1).** In the file, smoking ranks last; allergy and alcohol look like the
   "causes."
3. **Why the file lies (chart 2).** 87% cancer, no control; smoker vs non-smoker rates nearly equal
   (OR 1.42, p 0.39). Selection bias, when everyone is sick nothing predicts sickness.
4. **The truth the file can't hold (chart 3).** Real epidemiology: ~15-30x relative risk, ~80-90% of
   cases; Doll & Hill, Surgeon General. No safe level. (Reaffirm the guardrail here, hard.)
5. **Why it matters, Indonesia (chart 4).** Among the world's highest male smoking rates; the cost of
   believing a comfortable wrong number is measured in lives.
6. **Close, turn on the learner.** The data wasn't lying, it couldn't see, and neither could you.
7. **Method notes + References.**

## Citations to verify (verified-or-omit; pin at sourcing, Post 11 model)

- **Smoking causes ~80-90% of lung cancer** (US Surgeon General 2014 / CDC). VERIFY exact figure + year.
- **Relative risk of lung cancer for smokers ~15-30x** non-smokers. VERIFY (Surgeon General / major
  cohort; note it varies by sex, intensity, duration).
- **No safe level of tobacco use** / even light smoking raises risk substantially. VERIFY (Surgeon
  General; a light-smoking cohort study).
- **Doll & Hill British Doctors Study** (1950 case-control; 1954+ cohort) as the historical anchor.
  VERIFY.
- **Indonesia male smoking prevalence** (~65-70% of men) and any total-smoker figure. VERIFY (WHO
  GATS Indonesia / Tobacco Atlas / Riskesdas); keep apolitical, existence/scale only.

## Guardrails

- Objective, sober tone (serious health topic; real deaths). No jokey loading messages or framing.
- The no-safe-level truth is stated plainly and more than once; the dataset is never presented as
  evidence that smoking is safe.
- No em or en dashes; APA 7 references for every external fact; verified or omit.
- The dataset is a FOIL: its correlations are used to illustrate the trap, never as findings about real
  causation.
- 4 charts; charts 3-4 rest on verified real sources, not the Kaggle file.
- The learner is an illustrative composite, not a real individual.

## Verification plan

Source + verify all real-epidemiology and Indonesia figures against primaries (WHO, US Surgeon General,
CDC, Doll & Hill). Full rank/summary tables before any claim; 4 charts; long-dash scan;
adversarial-fact-check skill; slug match; local astro build; publish to joechrisnaldy.com.
