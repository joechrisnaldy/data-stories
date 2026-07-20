# Post 11 design: everyone knows social media is wrecking teens, the evidence doesn't

**Date:** 2026-07-18
**Series:** data-stories (Post 11)
**Folder:** `Projects/analytics-blog/social-media-teens/`
**Title (CHOSEN):** "Everyone Knows Social Media Is Wrecking Teens. The Evidence Doesn't."
**Slug / filename base:** `everyone-knows-social-media-is-wrecking-teens`

## The idea

The claim that social media is destroying adolescent mental health is now common sense: a bestseller,
a Surgeon General advisory, school phone bans, laws. But the careful evidence underneath that
certainty is thin. When researchers measure the link rigorously the effect is tiny and unstable, and
the field cannot even measure the supposed cause (screen time) accurately. This post is about the gap
between how sure we are and how little we can actually show. Not a claim that social media is harmless,
a claim that we ruled before we could measure.

## Thesis (chosen)

> Everyone has reached a verdict on social media and teenagers, but the evidence is too small, too
> contested, and too poorly measured to earn that certainty. The honest answer is that we cannot know
> yet, and acting certain is its own risk.

Landing (locked): **"we can't know yet"** (epistemic humility), NOT "social media is harmless" and NOT
a counter-panic. Hold the real crisis and the weak evidence at once.

## Brainstorm decisions (locked)

- **Core thesis:** panic vs evidence (our certainty vs the small, contested measured effect).
- **Landing:** we can't know yet, the evidence cannot bear the weight of the verdict.
- **Hook:** open on the wall of certainty (the bestseller, school phone bans, the Surgeon General),
  then pull the rug.
- **Framing:** universal, NO Indonesia and NO personal thread. The argument carries it.
- **Scope pillars (his picks):** the certainty itself; the crisis is real; the broken ruler; plus the
  contested link (the 4th chart, done fairly, not the "potatoes" gimmick).

## The four charts (all REAL data, verified-or-omit)

1. **The wall of certainty** (`smteens-1-certainty`). How sure everyone is: Pew shares of US
   adults/teens who say social media has a negative effect on teens, anchored by the US Surgeon
   General's 2023 advisory. Establishes the verdict everyone has already reached.
2. **The crisis is real** (`smteens-2-crisis`). CDC Youth Risk Behavior Survey: share of US
   high-schoolers reporting persistent feelings of sadness or hopelessness, rising since ~2011. We are
   NOT dismissing teen pain; the question is the cause.
3. **The contested link** (`smteens-3-contested`). Orben & Przybylski (2019, Nature Human Behaviour):
   analyzing the same data thousands of defensible ways yields a tiny effect that flips sign. Careful
   measurement shrinks the effect. Represent the specification-curve / effect-size honestly from the
   paper's published figures; if not faithfully reproducible, fall back to their headline numbers and
   flag it.
4. **The broken ruler** (`smteens-4-ruler`). Self-reported screen time barely matches objectively
   logged usage (Parry et al., 2021, Nature Human Behaviour meta-analysis). The debate rests on a
   number teens cannot accurately give.

## Section spine (~1,300-1,800 words, no long dashes)

1. **Open, the wall of certainty.** The bestseller, the phone bans, the Surgeon General. Everyone has
   already ruled. [chart 1]
2. **The crisis is real.** Teen distress genuinely rose. We take that seriously; this is not a
   dismissal. [chart 2]
3. **But the measured link is tiny and unstable.** When you measure carefully, the effect is minuscule
   and flips with analytic choices. [chart 3]
4. **And we can't even measure the cause.** Self-reported screen time is a broken ruler. [chart 4]
5. **We can't know yet.** The certainty is unearned. This is not "social media is fine"; it is "the
   evidence cannot bear this verdict." Acting certain (bans, laws) on thin evidence is its own risk.
6. **Close.** What it would take to actually know, and why we reach for one clean villain for a
   complicated generational change. Not medical advice.
7. **Method notes + References.**

## Citations to verify (verified-or-omit; pin exact numbers at sourcing)

- **CDC YRBS**: persistent sadness/hopelessness among US high schoolers, trend and by-sex (girls vs
  boys). Source: CDC Youth Risk Behavior Survey / YRBS Data Summary & Trends Report. VERIFY exact
  percentages and years.
- **Orben, A., & Przybylski, A. K. (2019).** The association between adolescent well-being and digital
  technology use. *Nature Human Behaviour*. VERIFY the variance-explained figure (~0.4%), the
  comparison anchors, and the specification-curve description/numbers.
- **Parry, D. A., et al. (2021).** A systematic review and meta-analysis of discrepancies between
  logged and self-reported digital media use. *Nature Human Behaviour*. VERIFY the self-report vs
  logged correlation (~r) and the over/under-estimation findings.
- **Pew Research Center**: adults'/teens' views that social media harms teens; teen usage. VERIFY exact
  shares and report year.
- **US Surgeon General (2023).** *Social Media and Youth Mental Health: The U.S. Surgeon General's
  Advisory.* VERIFY title, year, and the key wording (an advisory calling for more evidence, not a
  proven-harm verdict).

## Guardrails

- No em or en dashes; APA 7 references for every external fact; verified or omit.
- Objective: hold the real rise in teen distress AND the weak causal evidence together. Do NOT tip into
  "social media is harmless." The target is the certainty, not a new counter-certainty.
- Correlation is not cause; name it. Distinguish the real trend (crisis) from the contested attribution.
- Not medical advice.
- All four charts from real, cited public data; the rejected synthetic Kaggle dataset is not used.

## Verification plan

Source and verify all four datasets BEFORE building (dataset go/no-go on the real sources). Then: full
rank/summary tables before any claim; 4 charts; long-dash scan; adversarial fact-check (4-agent) before
the Word review; slug match; local astro build; publish to .com.
