# Provenance audit, Post 24, run before any design

Rule carried from Post 23: open the primary document or report that you could not.

## VERIFIED, and it is the hook

**Source opened:** Bloom, N., Lemos, R., Sadun, R., Scur, D., & Van Reenen, J. (2014).
*The New Empirical Economics of Management*. NBER Working Paper 20102, May 2014.
Downloaded from nber.org, 65 pages, read directly.

The World Management Survey asks, at the end of the interview, verbatim:

> "Excluding yourself, how well managed would you say your firm is on a scale of 1 to 10,
> where 1 is worst practice, 5 is average and 10 is best practice"

**Figure 17 is titled "SELF-SCORED MANAGEMENT UNCORRELATED WITH PRODUCTIVITY"** and its note
reads "Insignificant 0.03 correlation with labor productivity". Source given as Bloom, Sadun &
Van Reenen (2013b).

The body text, quoted exactly:

> "Unlike the management score, this is a purely subjective question capturing how the managers'
> perceive the management quality in their firms. Figure 17 plots these scores against labor
> productivity. Unlike the management scores in Figure 13 there is no relationship at all. Many
> good managers underestimate their firm's quality whereas many poor managers over-estimate it."

The contrast is the point. Figure 13, "TFP IS INCREASING IN MANAGEMENT", N=8,314, uses the
measured 18-question management score against TFP residuals with capital, labour, skills,
industry, country and year controls. Figure 11 shows the same score against log sales, N=10,197.

**So the precise claim the post can make:** the measured practices predict productivity; the
manager's own opinion of how well managed the place is predicts nothing. Note it is self-score
against PRODUCTIVITY, not self-score against the survey's own management score. Do not restate
it as "managers cannot score themselves" without that distinction.

## BLOCKED

**WMS microdata requires an account.** `worldmanagementsurvey.org/data/wms-data/download-public-data/`
returns a login form (verified: fetched, 74,713 bytes, body is a WordPress login page). Claude
cannot create accounts, so the self-score variable cannot be pulled here. The finding is citable;
it is not currently reproducible in this repository.

**US Census MOPS tables are JS-rendered.** The tables and data pages return 200 with zero linked
xlsx/csv/zip files in the HTML. Reachable, but needs a different route than a plain fetch.

**LSE CEP mirror is down.** `cep.lse.ac.uk` timed out after 75s. The AEA PDF returns 403.
The NBER copies work and were used instead.

## NOT YET CHECKED

Executive time-use by seniority; working-hours data that can be linked to management quality;
whether WMS publishes country aggregates outside the login; whether MOPS has an API.

## OPEN AND REPRODUCIBLE: O*NET 31.0

`onetcenter.org/dl_files/database/db_31_0_csv/*.csv`, direct download, no login, **CC BY 4.0**.
Pulled work_activities (11.8 MB), job_zones, occupation_data, content_model_reference.
911 occupations, 41 generalised work activities, each rated for Importance (1 to 5).

### First result, and it partly refutes the brief

Job zone (preparation required) against activity importance:
- Hands-on execution falls steeply: handling and moving objects -0.62, physical activities -0.58,
  controlling machines -0.53, operating vehicles -0.52.
- People management rises only weakly: coordinating others +0.20, directing subordinates +0.29,
  building teams +0.32, coaching +0.33.
- What actually rises fastest is not management at all: interpreting information for others +0.70,
  analysing data +0.66, using knowledge +0.64, working with computers +0.61.

**Caveat that disqualifies this as the headline:** job zone is education and training required, not
position in a hierarchy. A surgeon is job zone 5 and manages nobody.

### Second result, and this is the spine

Compare SOC major group 11 (management occupations, n=55) against all others (n=856), mean
Importance across four people-management activities and six hands-on ones:

| | people management | hands-on |
|---|---|---|
| management occupations | 3.88 | 2.51 |
| everyone else | 3.00 | 2.76 |

Matched promotion pairs (manager version against the individual-contributor version of the same
work) give a mean shift of **+0.82 on people management and -0.09 on hands-on**. The sharpest is
Computer and Information Systems Managers against Software Developers: people 2.24 to 3.94, and
hands-on 2.08 to 2.33, which goes UP.

**The finding: the promotion adds the managing and does not remove the doing.**

### The limitation that must be in the post, not buried

O*NET rates IMPORTANCE, not hours. It cannot support the sentence "managers spend more time on
people". It supports "the job is rated as requiring more of it". If the post needs hours, that is
a different dataset and I have not found an open one yet.
