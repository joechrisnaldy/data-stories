# The Job Nobody Takes Away

Post 24 in the data-stories series.
Live: https://joechrisnaldy.com/blog/the-job-nobody-takes-away

## The question

What separates a good manager from a bad one, and how would you know which you are?

The belief this post started from: the higher you go, the more you manage people and the less you
execute, so a manager who is still executing has failed to make the switch.

Half of that is wrong, and the wrong half is the important one.

## What the analysis found

**The promotion adds a job. It does not replace one.** Across the 20 O*NET occupations titled
"First-Line Supervisors of ...", each compared against every non-supervisory occupation in its own
SOC major group, managing people rises in **20 of 20** by 1.02 points on a five-point importance
scale. Doing the work rises 0.18 and falls in only 3 of 20.

**The flat number hides two opposite movements.** Working with computers +0.66 rising in 18 of 20,
drafting +0.40, repairing +0.26, against handling and moving objects -0.12 and general physical
activities -0.23. Remove computers and the remaining five come to +0.08. You stop lifting and start
typing; you do not stop doing.

**Seniority is not mainly about managing people.** Across all 911 occupations, what rises fastest
with required preparation is interpreting information for others (0.70) and analysing data (0.66).
The four people-management activities sit mid-pack, 0.19 to 0.33.

**What the promotion reliably hands you is exposure.** Coordinating or leading others +0.81 in 20
of 20, conflict situations +0.74 in 20 of 20, and the impact of your decisions on co-workers +0.47
in 19 of 20.

## What the data cannot do, which is the post's point

O*NET rates how IMPORTANT an activity is to an occupation. It is not a measure of hours, and no
claim here is about time. It also describes what a job requires and contains nothing about whether
the person holding it is meeting the requirement. The most detailed occupational database in the
world can tell a new supervisor exactly what the job demands and nothing about how they are doing.

The self-assessment evidence that fills that gap is cited rather than reproduced. The World
Management Survey asks managers to score their own firm "excluding yourself" and those scores
correlate with labour productivity at 0.03 (Bloom et al., 2014). The underlying variable sits
behind a registration wall this analysis did not pass, and `docs/provenance-audit.md` records that.

## Discipline

- `docs/2026-09-07-second-job-design.md` is binding and amendments are marked in place.
- `conditions.py` fixes the two activity groups and the pairing rule before any comparison was run,
  and records that the groupings are theory-driven but NOT blind.
- Three falsification conditions were written in advance. **None fired.** All are scored in
  `results.json`.
- Charts 1 and 2 were specified before the data was touched. **Charts 3 and 4 were not**, and both
  the design document and the fourth chart's own caption say so.
- The pairing is rule-based: no pair was chosen by hand.

## Scope limit

The 20 comparisons are supervisors of cooks, cleaners, cashiers, mechanics, police officers and
construction crews. There is no "First-Line Supervisors of Software Developers" in the SOC, so the
engineering reader the post addresses is not in the data. The post argues the transfer rather than
assuming it: what rises is coordinating, directing, team-building and coaching, none of which is
trade-specific.

## Files

| File | What it does |
|---|---|
| `conditions.py` | Activity groups, exclusions with reasons, the pairing rule |
| `build_analysis.py` | Every number in the post, into `results.json` |
| `make_charts.py` | The four charts in `charts/` |
| `results.json` | Committed output; the post quotes nothing that is not in here |
| `docs/2026-09-07-second-job-design.md` | Binding design document |
| `docs/provenance-audit.md` | What was opened, what was blocked, and why |
| `data/README.md` | Sources and download instructions |

## Reproducing

```bash
pip install -r ../requirements.txt
python3 build_analysis.py
python3 make_charts.py
```

O*NET is CC BY 4.0 and downloads without registration. Data files are gitignored.
