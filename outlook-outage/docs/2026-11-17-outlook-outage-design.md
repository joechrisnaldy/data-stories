# Post 31 design: the November 2026 Outlook outage, a break or a blocker

Post folder `outlook-outage`, slug `outlook-break-or-blocker`. Working title: "Outlook Went Down. Was It a Break or a Blocker?" The owner's request and answers are in `docs/research/brainstorm.md` (verbatim request, the answer to question 1 verbatim, then each choice); the research sweep is in `docs/research/sweep-*.json`. This is revision 1, after one doc-check (93 findings) and four owner answers recorded at the end.

## Intent

A short first-person reflection, about an 8-minute read (roughly 1,600 to 1,800 words), on the Microsoft 365 outage that began on 12 November 2026. The owner's words: "This is more on reflecttion", "not technical things but open disucssion", and outages should not be a "blocker anymore in the future". Durations are stated only against named endpoints from Microsoft's record and bound to results.

Why the owner wants it (verbatim): "In my opinion, for a company outage means that some core system that depends on them are not able to use since the login depend on them. But some people said that it's time to take a break." The post lives between those two reactions. These are the only two personal facts it may use.

Reader: people who were stuck at work that day, employees and team leads. Takeaway: what to agree with your team before the next outage.

## Thesis

The outage was not only a lost inbox. What failed was the system that connects people to their Exchange Online mailboxes, and Microsoft listed other services as impacted because their features depend on it, some sign-ins included: one dependency, many doors. For a company, that dependency is where work stops; meanwhile some people said it was time to take a break. Two lessons, in the owner's order: agree on a backup channel before the next outage (such as WhatsApp, which most internet users in Indonesia use), and know which work stops when that one dependency fails, because a backup chat does not reopen those doors. With both in place, the next outage can be a pause rather than a stop. The owner's wider worry, that a company's logins often run through Microsoft, is stated as the owner's view, never as what happened on 12 November.

## Structure (word budget about 1,700)

1. **Opening (about 150).** The two reactions, the blocker and the break, in the owner's view.
2. **What happened (about 350).** The story in Microsoft's own record (incidents EX1550543 and MO1550821): the first post, the spread to other services, the fixes that did not take, the 48-hour mail timeout extension, "approaching normal levels", the stated end of impact, the apology in the record's own wording, Microsoft's statement that there was no indication of malicious activity, and the preliminary cause from the final status in one or two plain sentences. UTC with Jakarta time beside it. Chart 1.
3. **How big, and how people reacted (about 350).** Downdetector's counts, attributed to Downdetector as named outlets quoted them: they count reports, not users, and Microsoft gave no figure for affected users. What organisations said they could not do (Singapore Courts, Guy's and St Thomas' NHS trust telling patients to phone rather than email, the Supreme Court of Victoria, Western Australia's planning department, Workhorse moving its results call). Scammers sending fake outage notices (Field Effect, Mimecast, Microsoft Threat Intelligence), with no counts and no confirmed credential theft stated. Cost in one sentence: estimates exist from several firms, they measure different things (lost productivity, refunds, insured losses), they range widely, and none publishes its method; no single figure is given as the answer.
4. **Should we depend less on email? (about 350).** Open discussion. What share of internet users used email and WhatsApp in the past month, in GWI's surveyed markets and in Indonesia (chart 2): email is used more widely across the surveyed markets, while in Indonesia WhatsApp reaches most internet users. Organisations that fell back to the phone. WhatsApp as one candidate for a second official channel and what makes a channel official (agreed in advance, who is in it, what may be decided there). Counterpoints the discussion must answer: HSBC told staff not to use personal email or WhatsApp (Reuters), and Microsoft said Teams' core chat and meetings kept working, so the lesson covers the case where the company's own chat also fails.
5. **The turn: one dependency, many doors (about 300).** Microsoft listed services besides mail as impacted (chart 3), some sign-ins among them (Dynamics 365 Field Service mobile, which named Exchange as its upstream dependency). A backup chat keeps people talking but does not reopen those doors, so the second lesson is to know, before the next outage, which work stops when that one dependency fails. The owner's login worry, as the owner's view.
6. **Close (about 200).** A pause, not a stop: with a backup channel and that list, the next outage can be the break some people said they wanted. Open questions for the reader.

## The three charts (an override of the series' four-chart rule, at the owner's request)

1. **`oo-1-timeline.png`, the outage in Microsoft's own record.** A horizontal timeline in hours, from the first post in EX1550543 (16:20:07 UTC, 12 November; also the start the final status gives) to the final status (04:15:46 UTC, 14 November). About seven labelled updates for a non-technical reader. Microsoft's stated impact window (16:20 UTC 12 November to 16:10 UTC 13 November, declared in the final status) shaded and captioned as Microsoft's global window. A second axis in Jakarta time (WIB, UTC+7). No working-hours band (it would need a sourced definition). One track only: every time read from the stored capture of the record by the parser script.
2. **`oo-2-email-vs-whatsapp.png`, who uses what.** The share of internet users aged 16 and over who used each in the past month, from DataReportal's Digital 2027 Global Overview (21 October 2026) and Digital 2027 Indonesia (4 November 2026), GWI survey data: email and WhatsApp in GWI's surveyed markets, WhatsApp in Indonesia. Labelled "GWI's surveyed markets", not "worldwide". Footnote: about 54 markets, China included (WhatsApp is blocked there), Russia excluded, the WhatsApp wave not named, self-reported. Indonesia email: the email-by-country chart in the Global Overview is read in step 2; if Indonesia is absent, the footnote says the reports give no Indonesia email figure on this basis. No figure from another survey (BPS, APJII, Kominfo) sits beside these, and no user counts in billions.
3. **`oo-3-many-doors.png`, one dependency, many doors.** The services besides Exchange Online that Microsoft listed as impacted in MO1550821's updates, as the list changed during the incident (the sweep reads four at the first post and nineteen in the final status; both provisional until the parser counts the stored capture). Labelled "listed by Microsoft as impacted", never "down". Inclusion rules: only services named in MO1550821's own updates; OneDrive (named only in the post-incident review as reproduced by others), Azure, Xbox and Entra (news or Downdetector only) and TM1550488 (an earlier Teams incident Microsoft never linked) are left out; PP1550869 and CR1551339 (separate advisories naming an Exchange dependency) go in a footnote. Exchange Online itself is shown at most as a labelled reference.

## Sources and rights (captured first, as soon as the design is approved)

- **Microsoft's service health record** for EX1550543 and MO1550821, Microsoft's text as republished by the University of Pennsylvania ISC mirror (https://mailservices.isc.upenn.edu/computing/email/penno365/alerts/ms-incidents.html), cross-checked against the Cloud Admin Hub mirror. Cited with Microsoft as the author and the mirror as where it was retrieved. A raw capture of both incidents is stored in `sources/`; a later capture may differ from the one cited. Quotes are planned long enough to occur once in the capture (carrying the incident's distinguishing words), and the reference title is chosen to open the stored capture.
- **No posts on X** (owner's answer). The all-clear on X and the executive's root-cause summary of 16 November are not used; the cause comes from the final status alone. If Microsoft's final post-incident review becomes public before publication, the cause sentence is checked against it; otherwise it is called preliminary, with its date.
- **DataReportal** reports above. Terms: attribution to DataReportal and its partners with a link, within fair dealing; whether a chart may be redrawn from their data points, and GWI's own terms, go in `docs/rights-notes.md`, with a question to DataReportal if needed, and a decision on `restricted_inputs`. No WhatsApp logo on the chart.
- **Downdetector** figures only as quoted by named outlets, attributed to Downdetector.
- **Reactions and cost**: each organisation's own page (Singapore Courts, Guy's and St Thomas', the Supreme Court of Victoria, Western Australia's planning department, Workhorse's release from GlobeNewswire or its investor page), the security reports (Field Effect, Mimecast, Microsoft Security blog), Reuters for HSBC, and each cost estimate from the outlet that first reported it. The break side rests on the owner's own fact unless a stored source for the jokes is found.

## Goals, non-goals, anti-goals

- Goals: the story in Microsoft's own record; the two reactions side by side; two lessons a team can act on; Indonesia as a thread where WhatsApp comes up.
- Non-goals: a technical root-cause analysis; a tool comparison; security advice beyond reporting the scams.
- Anti-goals: saying that Microsoft's sign-in service failed on 12 November; using the 31 August to 3 September outage as evidence about November; presenting WhatsApp as already official anywhere; mixing Downdetector snapshots as one series; any personal fact about the owner beyond the two above; blaming Microsoft beyond what its record says; criticising GWI's data beyond its stated caveats.

## Constraints and how the pipeline maps

- No Kaggle dataset: the data are stored records and published figures (the owner's choice of topic). Step 2's go/no-go covers the captures; a parser script reads the stored captures into `data/*.csv` (timeline events, service lists, the three shares) and prints its own summary in place of `profile_data.py`; the build script emits every figure to `results.json`.
- Times in prose: elapsed hours and dates are bound to results; a clock time appears in prose only through an `[allow]` entry naming the stored record, decided in step 6, or not at all.
- The gate's rules as usual (no typed numbers, the claims register, APA 7, no em or en dash, the `[published]` templates with the draft, the MDX before round 1); two fact-check rounds at most, then cuts only.

## Approaches considered

- **Draft now from Microsoft's own record (chosen by the owner).** Disagreements are stated, not hidden: the post says which start and end it uses.
- Wait for Microsoft's final post-incident review: it sits behind an admin login and its public timing is unknown.
- Keep the story minimal: a thinner background story than the owner asked for.

## Owner answers recorded in this revision (2026-11-17)

- The turn: "One dependency, many doors (Recommended)".
- Cost: "One honest sentence (Recommended)".
- Chart 2: "Survey shares (Recommended)" (in place of the published user counts first proposed).
- Sources: "Mirror only" (no posts on X; the timeline ends at the final status; the cause from that status alone).

## Left to the builder

The exact updates labelled on chart 1; the order of chart 3's services; the wording of the open questions in the close; the title's final form within the "break or blocker" direction.
