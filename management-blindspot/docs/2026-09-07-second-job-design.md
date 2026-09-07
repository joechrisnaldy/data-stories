# Post 24 design: the job nobody takes away

Binding design document. Written 2026-09-07, BEFORE the first-line-supervisor comparison is run.
Amendments are marked in place (AMENDED / WITHDRAWN / SUPERSEDED), never edited silently.

Repo folder: `Projects/analytics-blog/management-blindspot/`

---

## 1. The question and the answer

His question: what separates a good manager from a bad one, and how would you know which you are?

His stated belief, in his words: the higher the position, the more time you spend managing people
and the less on execution; a bad manager executes more and their team absorbs it as overtime.

The answer this post reaches: **half of that is wrong, and the wrong half is the important one.**
The promotion adds the managing. It does not remove the doing. The manager who is still executing
is not failing a rule; they were handed a second job and nobody took the first one away. What makes
that bad management is not the executing, it is that the added half is the half nobody measures, so
it is the half that slides, and it slides onto other people's evenings.

## 2. Structure

Three acts, ~1,800 to 2,000 words, four charts, engineering reader.

1. **The promotion.** What actually changes when you become a supervisor, from the activity data.
2. **The complication.** What rises with seniority is not mainly people management, which
   complicates both his thesis and the tidy version of mine.
3. **The blind spot.** Why you cannot check yourself from the inside, and the two external
   signals that are left.

## 3. Pre-registered method

### 3.1 Data

O*NET 31.0, `onetcenter.org/dl_files/database/db_31_0_csv/`, CC BY 4.0, no registration.
Files: `work_activities.csv`, `job_zones.csv`, `occupation_data.csv`, `content_model_reference.csv`.
911 occupations, 41 generalised work activities, Importance scale (IM), 1 to 5.

**What this data is and is not.** O*NET rates how IMPORTANT an activity is to an occupation. It is
not a measure of hours. Every claim in the post is phrased as importance, never as time spent.
This is a real limitation on his original framing and the post states it in the body, not only in
the method notes.

### 3.2 The two activity groups, fixed now

**PEOPLE MANAGEMENT** (four generalised work activities):
- 4.A.4.b.1 Coordinating the Work and Activities of Others
- 4.A.4.b.2 Developing and Building Teams
- 4.A.4.b.4 Guiding, Directing, and Motivating Subordinates
- 4.A.4.b.5 Coaching and Developing Others

Deliberately EXCLUDED and why: 4.A.4.b.3 Training and Teaching Others, because teachers and
instructors score high on it without managing anyone; and 4.A.4.b.6 Providing Consultation and
Advice to Others, because it is advisory work done by consultants, doctors and lawyers who have no
subordinates. Including either would let non-managers score as managers.

**HANDS-ON EXECUTION** (six generalised work activities):
- 4.A.3.a.1 Performing General Physical Activities
- 4.A.3.a.2 Handling and Moving Objects
- 4.A.3.a.3 Controlling Machines and Processes
- 4.A.3.b.1 Working with Computers
- 4.A.3.b.2 Drafting, Laying Out, and Specifying Technical Devices, Parts, and Equipment
- 4.A.3.b.4 Repairing and Maintaining Mechanical Equipment

Each group is scored as the unweighted mean Importance of its members.

**AGAINST MYSELF, recorded here rather than discovered later.** These groupings were written down
before any comparison was run, but I had already seen a related result: the same groupings applied
to job zone, which is a different question. So the grouping is theory-driven and mechanically
checkable, but it is NOT blind, and the post says so. Same disclosure as Post 23 section 3.6.

### 3.3 The comparison, fixed now

**The pairing rule, chosen so that no judgement of mine selects the pairs.** O*NET contains 20
occupations titled "First-Line Supervisors of ...", each named for the workers it supervises and
sharing a SOC major group with them. For each, the comparison group is every non-supervisory
occupation in the same SOC major group. The supervisor is the first rung of the promotion this
post is about.

Reported: the mean shift in each activity group, across all 20, with the per-major-group values
shown rather than only the average.

### 3.4 Falsification conditions

The post is wrong, and becomes a different post, if any of these hold:

1. People-management importance does not rise from worker to first-line supervisor.
2. Hands-on execution falls by as much as people management rises, that is, the promotion really
   does swap one for the other. This is his original thesis and it is a live possibility.
3. The pattern reverses in the major groups covering skilled or technical work, meaning it is an
   artefact of low-skill service occupations.

### 3.5 Guardrails

- **No pair hand-picking.** The 20 supervisor occupations are whatever O*NET contains. Illustrative
  manager-versus-specialist pairs may appear in prose but never as a headline figure, because I
  looked at eight of them before this document existed.
- **Scope limit stated, not buried.** The 20 supervisor occupations cover service, sales, admin,
  construction, production and transport. There is no "First-Line Supervisors of Software
  Developers" in the SOC. The post is written for an engineering reader from data that does not
  contain engineers, and it must earn that generalisation in a sentence rather than assume it.
- **Importance, never hours.** Any sentence that would need time-use data is cut or rewritten.
- **The self-assessment finding is cited, not reproduced.** Bloom et al. (2014) NBER 20102 is
  quoted with a reference because the underlying variable sits behind a login this repository
  cannot pass. It supports the third act; it is never a headline number.

## 4. Chart spine

Exactly four, prefix `mg-`.

1. `mg-1-the-second-job.png` The promotion shift: people management against hands-on execution,
   worker versus first-line supervisor, all 20 major-group comparisons.
2. `mg-2-what-actually-rises.png` Across all 911 occupations, which activities rise with job zone.
   The complication: analysis and interpretation rise faster than managing people.
3. `mg-3-what-the-net-hides.png` AMENDED 2026-09-07, decided after act 1 was computed. The +0.18
   net shift in hands-on work is the average of two opposite movements and publishing only the net
   would be the aggregation this series exists to complain about. Per-element: Working with
   Computers +0.66 rising in 18 of 20, drafting +0.40, repairing +0.26, controlling machines +0.09,
   against handling and moving objects -0.12 and general physical activities -0.23.
4. `mg-4-what-lands-on-other-people.png` AMENDED 2026-09-07. O*NET Work Context, CX scale, same
   20 comparisons: Coordinate or Lead Others +0.81 in 20 of 20, Conflict Situations +0.74 in 20 of
   20, Impact of Decisions on Co-workers or Company Results +0.47 in 19 of 20, Freedom to Make
   Decisions +0.22 in 16 of 20, Consequence of Error +0.15 in 12 of 20. This is the third act: the
   promotion moves the cost of your decisions onto other people.

~~Charts 3 and 4 are deliberately unfixed.~~ RESOLVED 2026-09-07 as above. The original text is
kept because a chart chosen after seeing the data is a different object from one chosen before,
and the reader is entitled to know which this is. Charts 1 and 2 were specified in advance;
charts 3 and 4 were not.

### 4.1 The limit of this dataset, which is also the third act's argument

O*NET describes what an occupation REQUIRES. It contains nothing about whether any individual is
meeting the requirement. The most detailed occupational database in the world can tell a new
supervisor exactly what their job demands and not one thing about whether they are doing it. That
is not a flaw in the data for this post's purposes; it is the post's point, and it must be stated
as a property of the source rather than smuggled in as a rhetorical flourish.

The self-assessment evidence that fills that gap is cited, not reproduced: Bloom, Lemos, Sadun,
Scur and Van Reenen (2014), NBER Working Paper 20102, Figure 17, self-scored management
uncorrelated with labour productivity at 0.03. See `docs/provenance-audit.md` for the verbatim
quotes and why the underlying variable could not be downloaded.

## 5. Out of scope

- Any claim about a named employer, including his. Experience enters as composite and flagged.
- Any claim that managers should not execute. The finding is that the job is additive, not that
  the doing is wrong.
- Time-use claims of any kind unless an open hours dataset is found and added here first.
