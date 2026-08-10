# Post 22 design: Reading Part of One Sentence Counts as Literate

Written 2026-08-09. Binding. Anything this document approves can still be refuted by the data or by
a fact-check round, and when that happens the superseded wording gets marked WITHDRAWN in place
rather than quietly deleted. Post 21 lost three findings to a design doc that presented refuted text
as approved.

## Thesis

The measure is honest about what it does. The word is not.

"Literate" in one of the world's most-used household surveys certifies one of three things: that you have
more than a secondary education and were therefore never asked, that you read a whole sentence off a
card, or that you read **part** of one. There is no state of the instrument that means "this person
cannot read" for anyone with enough schooling. And globally, the instrument that could produce that
result is used almost exclusively on the poor.

Explanatory, not accusatory. Nobody is hiding anything: DHS publishes the coding rule, the Stata
that implements it, and a "Changes over Time" note warning that its own older estimates may
overstate literacy. The gap is between what the indicator can certify and what the word promises.

## Approved by the user during brainstorming

| Question | Decision |
|---|---|
| Core angle | The instrument decides the verdict, not the literacy of the population |
| Contrast | The same survey that asks also tests, so no cross-source comparability problem |
| Posture | The word promises more than the measure delivers. No villain |
| Scope | DHS spine plus a rich-world second movement |
| Indonesia | **None this time.** The finding is universal and an Indonesia frame would narrow it |
| Close | A measure that cannot record failure cannot report success |
| Title | Reading Part of One Sentence Counts as Literate |

Dropped from the five source URLs the user supplied: financing-education, research-and-development,
internet, books. The argument does not need them and forcing them in would spend the word budget
without adding evidence.

**The second movement changed during vetting, with the user's approval implied by the posture rather
than stated.** The plan was OECD adult-skills proficiency against declared literacy. PIAAC turned
out not to be in the OECD SDMX API (1,544 dataflows, no match), and a better second movement was
already in hand: UNESCO's own record of *how* each country's rate was produced. **WITHDRAWN IN
ROUND 1:** this said "every European country in that file self-declares and none tests". That is
false. Bosnia and Herzegovina and Ukraine both appear in the post's own ever-tested list. The true
picture is 25 European countries in the file, 22 self-declaring only, Andorra on an indirect
estimate, and those two tested. The 40 ever-tested countries are still overwhelmingly poor. That is a stronger claim, needs no new source, and has no
comparability caveat. **If the essay ever reverts to a PIAAC comparison, this paragraph is void and
the sourcing has to be redone.**

## The instrument, stated exactly

From the DHS Guide to DHS Statistics, numerator 2, verbatim:

> Number of women (or men) age 15-49 literate (women: v106 = 3 or v155 in 1,2)

and from the same page:

> The question on the ability of the respondent to read a sentence are not asked to women and men
> with higher than secondary education.

`v106 = 3` is higher than secondary. `v155 = 2` is a whole sentence, `v155 = 1` is part of one. The
published Stata implements exactly this (`DHS-Indicators-Stata`, `Chap03_RC/RC_CHAR.do`):

```stata
gen rc_litr=0
replace rc_litr=1 if v106==3 | v155==1 | v155==2
label var rc_litr "Literate - higher than secondary or can read part or whole sentence"
```

Two things follow that the post must state and neither overstate:

1. Nobody above secondary is tested, so for them the indicator has no failure state.
2. Reading part of one sentence is counted as literate.

And one that cuts the OTHER way and must be given equal prominence, because the post's posture is
explanatory: `v155 = 3`, "no card with required language", is counted as NOT literate. A respondent
who reads fluently in a language the interviewer had no card for is recorded as illiterate. The
instrument errs in both directions. It is small in practice (0.05 points at the median and 1.5 at the maximum, in Mali (CORRECTED IN ROUND 2; the earlier
"0.0 to 0.8" came from a four-country probe)) but it is real and it is the honest counterweight.

## The break, and why it is a finding rather than a trap

DHS changed the rule. Its own "Changes over Time" note:

> In DHS-VI and earlier surveys the question on the ability of the respondent to read a sentence was
> not asked to women and men with secondary education or higher than secondary. Thus estimates from
> earlier surveys may overestimate literacy relative to DHS-7 and DHS-8 surveys. Care should be
> taken in interpreting trends.

The API exposes no phase field, and the two regimes **overlap in time** (old-rule surveys run 2000
to 2016, new-rule 2015 to 2025), so a fieldwork-year cutoff misclassifies surveys. Do not use one.

Classify empirically instead, and validate against the documented rule. Under the old rule the
never-tested column equals the share with secondary **or higher**; under the new rule it equals the
share with **more than** secondary. Both are separately published (`ED_EDUC_W_SEH`,
`ED_EDUC_W_HGH`). Assign each survey to whichever it matches:

- old-rule surveys match `SEH` to a mean of **0.03 points**, against 30.4 for the alternative
- new-rule surveys match `HGH` to a mean of **0.05 points**, against 36.7 for the alternative
- 221 of 226 surveys classify; 142 old, 79 new (CORRECTED IN ROUND 1: the earlier 225/145/80 came
  from a probe that predated the missing-column fix)

That is a clean separation, not a judgement call, and `build_analysis.py` must implement it as a
function and emit the counts so the classification is auditable.

**Ghana is the worked example and it is the strongest fact in the post.** Between 2014 and 2022 the
share of Ghanaian women with secondary or higher education rose from 63.1% to 70.2%, while measured
literacy FELL from 67.1% to 60.8%. Ghanaian women did not forget how to read. DHS started handing
them the card. In 2014, 63.1 of the 67.1 literacy points were people never asked to read anything.

## Chart spine, four charts

1. **What "literate" is made of.** Stacked bars, one per country, latest new-rule survey only:
   never tested (above secondary) / read a whole sentence / read part of a sentence / cannot read.
   The "part of a sentence" band is the payload. Nigeria 2024 and 2021 are the sharpest instances.
2. **The year the instrument changed.** Ghana, India, Indonesia, Nigeria, before and after, showing
   the never-tested column collapsing and Ghana's headline rate falling while its education rises.
   Must be drawn so the reader sees the composition change, not just the total.
3. **How the world's literacy statistics are actually made.** UNESCO's reporting mode across 686
   country-years: 333 self-reported by the head of household, 283 self-reported by the individual,
   52 an actual literacy test, 18 indirect estimate.
4. **Who is asked to prove it.** The 40 ever-tested countries against the 129 never-tested.
   **AMENDED TWICE.** The spec said "by income"; the shipped chart plots the literacy level each
   method produced, because no income series is in this post's data. And the European claim here
   was refuted in round 1, see the WITHDRAWN note above. The tested list is Chad, Niger, Sierra
   Leone, Malawi, Haiti and their peers, plus South Korea, Ukraine and Bosnia and Herzegovina.

Not a chart, but in the prose: where DHS and UNESCO both cover a country (33 country-years, 28
countries) they disagree by up to +15.9 points (Pakistan 2005) and 11.7 lower (East Timor 2015), around a
mean gap of only +1.8. The average conceals the disagreement entirely.

## Traps recorded during the vet

1. **`ED_LITR_W_SCH` is mislabelled in the API** as "Women with secondary or higher education". Its
   actual numerator under the current rule is `v106 = 3`, higher than secondary. Trusting the label
   would misdescribe the column in every chart. Use the Guide's definition, not the label.
2. **Survey type is not the break.** Ghana 2014 DHS and Ghana 2022 DHS sit on opposite sides of it,
   and MIS rounds appear in both regimes. Do not classify by `SurveyType`.
3. **Fieldwork year is not the break either.** The regimes overlap 2015 to 2019.
4. **`dhsprogram.com` returns HTTP 403 to automated fetches.** The Guide is reachable through the
   Wayback Machine via `curl` (WebFetch cannot reach web.archive.org from here); the indicator code
   is on GitHub.
5. **The OECD SDMX API does not carry PIAAC.** Checked all 1,544 dataflows.
6. **This machine's Python has an empty CA bundle**, so `urllib` fails every HTTPS request with
   CERTIFICATE_VERIFY_FAILED. `fetch_data.py` resolves a working bundle rather than disabling
   verification.
7. **The eight literacy indicators sum to 100 and `SCH = LIT - RDW - RDP` exactly**, on all 21
   surveys spot-checked. Assert both in `build_analysis.py`; a break in either means the definitions
   moved again.

## What this post cannot say

- It cannot say the world is less literate than reported. It can say the reported figure is not
  built to answer that question, and that almost nobody has measured it. Only 52 of 686 country-years
  were ever tested.
- It cannot compare DHS literacy trends across the rule change. Any trend line must stay inside one
  regime, and the post should say so on the chart.
- It cannot claim intent. The rule is published, the change is disclosed, and the warning about
  trends is DHS's own.
- The reporting-mode file ends in 2016, so "this era" has to be worded against that vintage.

## Method notes the essay owes the reader

Two time bases: DHS surveys at their own fieldwork years, and UNESCO reporting mode 1975 to 2016.
Women aged 15 to 49 throughout, which is the DHS universe and is NOT the same population as
UNESCO's adult 15+ rate; the post must not present them as the same measure. Percentages are DHS's
own published weighted estimates, not recomputed from microdata.
