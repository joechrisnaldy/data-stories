# Post 32 design (revision 1): two 12-hour days or three 8-hour days?

Working title: "Two 12-Hour Days or Three 8-Hour Days?" (the example the owner saw with the chosen title option, "The 24-hour question"). Post folder: `overtime-or-hire/`. Slug: built from the final title at drafting.

## Intent and the why

The owner asked for an objective research piece on what long working hours and short sleep cost a company and the wider economy, and on whether a company does better hiring more people, still on merit, than having a smaller team work long hours. The framing: two people on 12-hour days give the same 24 hours as three people on 8-hour days. Those nominal hours are equal by arithmetic; what the post tests is whether they give the same productive hours, and at what cost per productive hour. The post ends with recommendations for companies.

Rule: the post, its READMEs, this document and every committed file are impersonal: no autobiographical material, and the first person only for judgments and the recommendation. The private brainstorm record (kept outside the repository) holds the details.

## Decisions the owner made

The chosen option labels, verbatim; the option descriptions the owner saw are in the private brainstorm record.
1. "Test it, then recommend (Recommended)"
2. "Cost and output together (Recommended)"
3. "Managers who set staffing (Recommended)"
4. "First-person stance, no story (Recommended)"
5. "US core, Indonesia thread (Recommended)"
6. "Cover paid and unpaid (Recommended)"
7. "The 24-hour question (Recommended)"
8. "A: analysis + cost model (Recommended)"
9. After the design check: "Add it as one section (Recommended)" (what insufficient sleep costs employers and the economy)
10. After the design check: "Exercise in chart 1, burnout named (Recommended)"

## Goals, non-goals, anti-goals

Goals:
- Test one week of five 12-hour days for two people against five 8-hour days for three people, by productive hours and by cost per productive hour, in two cases: non-exempt staff, owed the federal overtime premium for hours over 40 in a workweek, and exempt salaried staff, whose pay is the same at 40 and 60 hours (definitions quoted from the statute and 29 CFR part 541 at provenance).
- Show what long weekly hours go with in sleep and exercise, from US time-use microdata analysed for this post.
- Show how output behaves as weekly hours grow, from a primary study.
- One section on what insufficient sleep costs US employers and the US economy, from a stored primary estimate.
- Give managers a decision rule, stated in an input they can estimate, and a short list of what to track.
- Compare the US rule with Indonesia's statutory overtime pay and caps for the same week.

Non-goals:
- Medical or health advice; the post says it is not medical advice.
- Sleep quality (the survey measures time, not quality); the four-day week, remote work and shift scheduling as topics of their own; a full Indonesian cost analysis.
- Burnout as a measured quantity: it is named as a cost the test cannot price unless a primary source quantifies it.

Anti-goals:
- Stating the claim as proven before the test, or a model output as a measured fact.
- A causal claim from the time-use survey: it shows what long hours go with.
- Any figure typed by hand, or any model input without a stored, quoted source. An input no primary source gives is not ranged by hand: the build script solves for its break-even value and the post reports that value.
- Any autobiographical material, or anything about the author's employer.
- Country comparisons presented as evidence about companies.

## Constraints

- The blog pipeline (`/data-story`) and the shared gate: placeholders for every figure, stored and quoted sources, the claims register, four charts, roughly 1,500 to 2,000 words, MDX before round 1, two fact-check rounds at most.
- Writing rules: no em or en dashes; APA 7 references for internet-sourced facts; citations verified or omitted.
- Downloaded files are untrusted: each in its own folder, read with `python3 -I`.

## Approaches

- A, chosen: own analysis plus a sourced cost model with break-evens. Trade-off: the model rests on assumptions, so its value is in showing where the answer flips, not one number.
- B, evidence review only: faster, but no data of the post's own and no decision rule.
- C, cross-country hours against output per hour: easy data, but country differences have many causes and do not answer the company question.

## Analysis plan

Every source fact below is expected, to be confirmed when the document is stored and quoted in `docs/provenance-audit.md` (step 3), before any analysis.

1. Sleep and exercise (own analysis): the latest American Time Use Survey multi-year activity summary file. Minutes of sleep and of exercise on the diary day, by usual weekly hours band, for employed people, with the survey's weights and respondent counts per band. The activity codes counted as sleep and as exercise, the usual-hours variable and the weights are named and quoted from the stored lexicon and data dictionary; one published estimate is reproduced before any band is built; the sample rule lives in one shared filter function.
2. Output and hours: Pencavel's study of output against weekly hours, from his reported estimates, stored and quoted, read by the build script. Its data are British munitions workers of the First World War, so the curve enters the model as an assumption, said wherever it is used; step 2 also looks for a modern primary estimate for salaried work.
3. The cost test, for one week (two people at 60 hours, three at 40):
   - Costs from the latest BLS Employer Costs for Employee Compensation release: its unit, the group used, which components scale with hours and which come per person, and the hours that turn one into the other, each named and sourced.
   - Non-exempt case: the federal premium on hours 41 to 60. Exempt case: pay and per-person costs the same at 40 and 60 hours, so nothing scales with hours past 40. On cash alone the exempt case favours two people by construction; the post says so and reports instead the extra weekly cost per long-hours worker (output lost, tired-staff and turnover costs) at which hiring breaks even, and the productive hours of each team side by side.
   - The third hire: same wage and the same output once trained (the merit assumption); hiring cost from a primary source or solved as a break-even. Turnover is treated the same for both teams.
   - Left out on the long-hours side: mistakes, sick days, quits, burnout. Left out on the hiring side: vacancy time, ramp-up, management overhead. Each named; no direction claimed for their net effect.
4. Sleep cost: a primary national estimate of lost output and workdays from insufficient sleep, quoted, used in the cost test only if it gives a per-worker figure.
5. Indonesia: Government Regulation 35 of 2021 on overtime pay and overtime caps, read from the stored regulation text, applied to the same 60-hour week.

What the test cannot answer: day length within the week (the output curve is weekly); whether a qualified hire is available; firm-specific output measures; anything outside the five-day, 60-hour week.

## Charts (four)

1. Sleep and exercise minutes by usual weekly hours (own analysis).
2. Output against weekly hours (Pencavel's estimates), labelled as a historical estimate.
3. The test: productive hours and cost per productive hour for the two teams, non-exempt and exempt, with each break-even.
4. The 60-hour week under the US rule and under Indonesia's rule: hours at each pay rate and whether each cap is exceeded.

## Structure (about 1,500 to 2,000 words)

An opening on why equal hours deserve a test; what long weeks go with in sleep and exercise; what short sleep costs employers and the economy; what long weeks do to output; the cost test, non-exempt then exempt; the Indonesian rule in brief; recommendations for managers (the decision rule and what to track); a short close. References in APA 7.

## Left to the builder

Hours bands, chart styling, and any value a primary source gives; every other model input is solved as a break-even, not chosen.
