# Round 4 scope: round 3's unverified findings, plus round 3's own fixes

Round 3 ran seven refuter lenses and then attacked each finding with three skeptics. The run hit a
usage limit partway through the verification phase, so **37 of 67 findings never reached a skeptic.**
They are OPEN, not refuted. A finding whose skeptics all died is unverified; treating it as refuted
would turn an infrastructure failure into a verdict, which is the one thing this process must never
do.

Round 4 has two jobs:

**Job one: verify the 37 below.** Each needs the same treatment the other 30 got: attack the finding
itself, default to rejecting it if you cannot substantiate it. Round 3's skeptics killed 14 of 30
findings including four HIGHs, so the prior on any single unverified finding being real is well under
a half.

**Job two: verify round 3's own fixes**, listed in `docs/2026-09-07-reversal-design.md` section 6.3.
Every round of this fact-check has had its worst defects inside the previous round's corrections, and
round 3 proved it again by withdrawing round 2's amendment 8. Section 6.3 is eight numbered claims
and none has been checked.

Body is FROZEN at 1,999 words against a 2,000 ceiling.

## The 37 unverified findings

### [HIGH] consistency / D1

**Text:** 8. **`lpd1500s` is not density per ARABLE acre.** Its denominator `lland15` is total land area with desert netted out; checked against known land areas (USA 1.001, India 1.000, Brazil 1.012, Egypt 0.040). The post said arable and now does not

**Claimed evidence:** I downloaded the cited paper (https://economics.mit.edu/sites/default/files/publications/reversal-of-fortune.pdf, pdftotext -layout) and read it. AJR say the opposite of amendment 8, three times: (a) p.1243, immediately after the page header 'REVERSAL OF FORTUNE 1243': "We calculate population density by dividing total population by arable land (also estimated by McEvedy and Jones). This excludes primarily desert, inland water, and tundra."; (b) the note to Table V, p.1251: "Population density in 1500 is total population divided by arable land area", and Table V Panel B's own row label is "Log arable land in 1500" - i.e. `lland15` IS arable land in the paper's vocabulary; (c) Appendix 2 (Var

**Proposed fix:** Withdraw amendment 8 in place (do not delete it) and record that AJR Appendix 2, p.1243 and the Table V note all define the denominator as arable land from McEvedy and Jones, with the caveat that the shipped `lland15` equals total land area for the USA, India and Brazil. In the draft, restore the source: replace line 45-46 "per unit of land, with uninhabitable desert netted out, reconstructed from

### [HIGH] logic / A16

**Text:** it cannot produce a ranking that inverted in one group and did not in the other

**Claimed evidence:** "Cannot" is false, and the draft's own data show why. I fitted a probit of AJR's ex2col on standardised temperature and standardised 1500 density using build_analysis.load(): P(colonised) = Phi(0.122 + 0.757*zT - 0.445*zD). Opposite-signed weights (Europeans went where it was HOT and where it was SPARSE), independently corroborated by the raw pooled marginals corr(tas, ex2col) = +0.4152 (n=203, t=+6.47) and corr(lpd1500s, ex2col) = -0.3497 (n=177, t=-4.94). Opposite-signed selection weights on a collider are exactly the Berkson configuration that manufactures a POSITIVE within-stratum association. I then simulated a world with ONE homogeneous, arrival-independent heat-density relation (rho =

**Proposed fix:** Replace "it cannot produce a ranking that inverted in one group and did not in the other" (16 words) with "it can produce a ranking that inverted in one group and not the other only through the split itself" (19 words, +3). This keeps the filter's force, names the one escape the draft's own data supply, and is honest about the modal verb. Offsetting cuts named at the bottom of the A28 fix.

### [HIGH] logic / A28

**Text:** because among former colonies that same thermometer used to point the other way: the hot places were the crowded ones

**Claimed evidence:** This is a RANK claim, in a post titled "The Map Used to Run the Other Way" whose filter and close are both about "a ranking". On rank statistics the single cell it rests on is not clear of chance. Recomputed on the 97 former colonies with both variables: Spearman rho = +0.1612, p = 0.1146; Kendall tau = +0.1058, p = 0.1293. Only the Pearson coefficient (+0.2946, r-squared 0.087) is significant, and it is carried by an 11-country tied block: BEN, BFA, CIV, GHA, GIN, GMB, GNB, NGA, SEN, SLE, TGO all sit at lpd1500s = 1.442202 with a mean temperature of 27.26 C against a sample mean of 23.12 C. Dropping that block gives r = +0.2468 (n=86); leave-one-out on Canada alone gives r = +0.1694. The po

**Proposed fix:** Replace "the hot places were the crowded ones" (7 words) with "hotter went with more crowded, weakly" (6 words, -1). This matches chart two's own panel title verbatim ("In 1500, hotter went with more crowded"), drops the categorical rank assertion the rank statistics do not support, and frees a word.

### [HIGH] logic / A28

**Text:** The thermometer cannot be the whole of it, and it cannot be what inverted the ranking underneath it.

**Claimed evidence:** Unconditional, and the filter it is drawn from is conditional. A16 disqualifies only explanations whose effect was BOTH constant over the period AND arrival-independent. The draft explicitly leaves the door open for a heat story whose effect changed: "The test is on the effect, not the cause: the equator has not moved, but what it does to prosperity may have" (lines 103-104), and A19 states that such stories survive: "What survives is anything whose effect changed over those five centuries" (line 119). So a temperature explanation with a time-varying effect passes the filter and could be exactly what inverted the ranking. The close asserts the categorical, dropping both qualifiers the casual

**Proposed fix:** Replace (18 words) with: "The thermometer cannot be the whole of it, and cannot have inverted the ranking unchanged." (15 words, -3). "Unchanged" restores the conditional the filter actually licenses. Budget note for the whole set: my nine fixes net +5 against a 1,999/2,000 body; offset by deleting "just" at line 186 ("It is just the thing that is easiest to measure", -1) and tightening line 116 t

### [HIGH] rhetoric / A4

**Text:** a plain Africa dummy does better still at minus 0.68. I left those out of an earlier draft, which was the wrong instinct: they tell you how much the thermometer is really carrying.

**Claimed evidence:** HOSTILE-READER, determinist/essentialising direction. `grep -n -i "africa" draft/the-map-used-to-run-the-other-way.md` returns exactly ONE hit, line 26. The word appears once in the whole post, as a variable that outperforms temperature, and there is no gloss anywhere saying a continent dummy is a label rather than a cause. The next sentence (round-2 text) actively endorses reading it as substantive: it tells the reader these three numbers 'tell you how much the thermometer is really carrying'. This is the single most quotable determinist line in the current draft and NO counterweight is within sight of it, or anywhere else on the page. Compare the two determinist lines round 1 handled corre

**Proposed fix:** Replace the clause after the colon. Line 26-27: 'I left those out of an earlier draft, which was the wrong instinct: they tell you how much the thermometer is really carrying.' -> 'I left those out of an earlier draft, which was the wrong instinct: a continent label beats the thermometer, and explains nothing.' Cuts one word (10 -> 9 after the colon), so it fits inside the 1,999/2,000 body. This s

### [HIGH] rhetoric / A4

**Text:** they tell you how much the thermometer is really carrying

**Claimed evidence:** OVER-CORRECTION check 7. Three bivariate correlations cannot tell you what share of temperature's association is temperature; that is a partial/variance question. `build_analysis.py` computes `rivals` as three SEPARATE `corr()` calls on one common sample (lines 148-151); there is no partial correlation and no multiple regression anywhere in the script. I ran the question the sentence claims to answer, on the same 159 countries from `B.load()`: bivariate r(tas, lgdp2023) = -0.4642; partial r controlling for lat_abst = +0.1499; controlling for africa = -0.2611; controlling for BOTH = +0.2168. The sign REVERSES. Also r(tas, lat_abst) = -0.8719, so the three variables are near-collinear and no o

**Proposed fix:** Same edit as above: '...which was the wrong instinct: a continent label beats the thermometer, and explains nothing.' This is what the three correlations DO support (ordering of crude summaries on one sample), and drops the decomposition claim they do not. Net -1 word.

### [MODERATE] consistency / B3

**Text:** Urbanisation was unaffected.

**Claimed evidence:** Recomputed. I reproduced the pre-fix pipeline (drop_duplicates('shortnam') keeping the first row) against the shipped build_analysis.py load() and diffed sample membership. The urbanisation-1500 vs 1995-income correlation gains Germany: never-colonised n 42 -> 43, r +0.4337 -> +0.4256; pooled n 83 -> 84, r +0.0532 -> +0.0548. The mechanism is visible in the data: maketable3.dta row 179 (DEU) carries sjb1500 = 8.0 while maketable5.dta row 179 (DEU) carries logpgp95 = NaN, so the merged first row has urbanisation but no 1995 income and the old dedup dropped Germany from that pair. Only the 2023 urbanisation pairings (43/43) are genuinely untouched. The same false claim appears three times: dra

**Proposed fix:** Replace "Urbanisation was unaffected." with "Urbanisation moved only in its 1995 pairing." (5 words for 3, +2). Cut the redundant ", and, more usefully," at line 222 (4 words) to stay under the ceiling. Make the same correction in build_analysis.py line 59 and design doc 6.2 item 7.

### [MODERATE] consistency / B3

**Text:** Fixing it moved six published correlations at the second decimal and changed every sample size in the post by one or two

**Claimed evidence:** Recomputed, pre-fix against shipped. (1) "every sample size in the post" is false at least twice. The post's n=196 (line 17 "196 countries and territories" and line 267 "all 196 entities with both") comes from the World Bank/ERA5 frame in main(), which never touches the AJR duplicates; it is 196 before and after. The post's urbanisation sample sizes (line 91 "43 countries on each side") are 43 and 43 before and after. Indonesia's rank ("47th") is also unchanged. This directly contradicts the sentence two lines earlier in the same paragraph, "Urbanisation was unaffected." (2) "six published correlations" is one too many. Exactly five correlations anywhere in the repository change their two-de

**Proposed fix:** Replace with "Fixing it moved five published correlations at the second decimal and changed most of the historical sample sizes by one or two" (21 words for 21, word-neutral). Correct design doc line 107-108 the same way.

### [MODERATE] consistency / D1

**Text:** chart 4's bottom row was selected by an arbitrary tiebreak between Guyana and Uruguay, which the de-duplication fix had silently swapped. All fixed.

**Claimed evidence:** Recomputed on the shipped frame. Guyana and Uruguay do NOT tie: GUY slide = -81.38297872340426 (float hex -0x1.45882b9310573p+6), URY slide = -81.38297872340425 (-0x1.45882b9310572p+6), differing by 1.42e-14. Sorting col2 by ["slide"] alone and by ["slide","inc_pct"] produces the identical last six, ['GUY','USA','HKG','AUS','CAN','SGP'], so the added inc_pct key never fires for this pair; the bottom row is still chosen by floating-point residue, which is precisely the "arbitrary tiebreak" the amendment claims to have removed. Worse, had they actually tied, inc_pct descending would rank GUY (93.617) above URY (88.298) and put URY last - the opposite of what renders. I opened charts/rf-4-who-a

**Proposed fix:** Either make the ordering genuinely deterministic - sort on the rounded slide plus a final iso3 key, e.g. col2.assign(_s=col2.slide.round(9)).sort_values(["_s","inc_pct","shortnam"], ascending=[False,False,True], kind="stable") - or, if the ordering is left as is, correct both the code comment and design doc 6.2 item 11 to say the two are separated by 1.4e-14 of floating-point residue rather than t

### [MODERATE] consistency / D1

**Text:** 8. **Source corrections.** Density is per ARABLE land, from McEvedy and Jones.

**Claimed evidence:** docs/2026-09-07-reversal-design.md line 195 (section 6.1 item 8) still asserts this in the document's current voice with no AMENDED/WITHDRAWN marker, while section 6.2 item 8 (lines 231-234) asserts the opposite. The document's own preamble, lines 4-5, states "Amendments are marked in place (AMENDED / WITHDRAWN / SUPERSEDED), never edited silently", and round 2 did apply in-place markers to 6.1 items 1 (line 156) and 5 (lines 181-183). Two further 6.1 items are refuted by 6.2 and carry no marker either: 6.1 item 4 line 178 "the flip disappears" against 6.2 item 4 line 219 "so 'the flip disappears' was wrong"; and 6.1 item 6 lines 185-187 "none of the three conditions would have fired" agains

**Proposed fix:** Add in-place markers to 6.1 items 4, 6 and 8 pointing to the 6.2 items that supersede them, on the document's own stated convention. For item 8 specifically, the marker must record that 6.2's refutation is itself refuted by AJR Appendix 2 and p.1243, so the 6.1 wording stands. Design document only; no draft words change.

### [MODERATE] consistency / D1

**Text:** This document pre-registered the disqualified class as a CONJUNCTION, "BOTH constant over the period AND independent of colonisation". ... The draft now states the conjunction

**Claimed evidence:** design doc lines 164-171 (6.1 item 2) endorse section 3.4's wording as the correct standard the draft had departed from. Lines 206-210 (6.2 item 1) then declare that exact wording invalid: "'An explanation cannot be both constant over the period and indifferent to who arrived' equivocates between a constant CAUSE and a constant EFFECT", and say the shipped claim is now "about the constancy of the EFFECT, and is restricted to explanations of the ranking BETWEEN countries". The draft's current filter (line 102-103) is therefore NOT section 3.4's pre-registered conjunction: it is an effect-level claim with a domain restriction that 3.4 does not contain. Section 3.4 lines 83-87 still reads "What

**Proposed fix:** Add a SUPERSEDED marker under section 3.4's filter paragraph recording that 6.2 item 1 replaced the pre-registered cause-level, unrestricted conjunction with an effect-level claim restricted to the ranking between countries, and mark 6.1 item 2's closing sentence as superseded by it. Design document only; no draft words change.

### [MODERATE] consistency / D2

**Text:** | urbanisation 1500 | +0.06 (n=84) | **-0.44 (n=41)** | **+0.43 (n=43)** |

**Claimed evidence:** results.json flip["urbanisation_1500|income_1995|all"] = {r: 0.05480, n: 84}, which renders +0.05, not +0.06; I re-ran build_analysis.py and reproduced 0.0548 on n=84. The pre-de-duplication value was +0.0532, which also renders +0.05, so no vintage of the pipeline produces +0.06. The other five cells in the table reconcile exactly (density +0.0517/-0.5842/+0.5035 on 156/91/65; urbanisation -0.4398 on 41 and +0.4256 on 43). This matters because the section immediately below, "STALE FIGURES IN AN EARLIER VERSION OF THIS FILE, CORRECTED" (lines 75-82), asserts that the table has been reconciled with the pipeline.

**Proposed fix:** Change "+0.06 (n=84)" to "+0.05 (n=84)" in docs/provenance-audit.md line 32. Audit file only; no draft words change.

### [MODERATE] consistency / D2

**Text:** - `logpgp95` "log PPP GDP pc in 1995, World Bank"

**Claimed evidence:** pandas read_stata(...).variable_labels() gives logpgp95 = 'log PPP GDP pc in 1995, World Bank' in data/ajr_t5/maketable5.dta but 'log GDP per capita 1995' in data/ajr_t3/maketable3.dta. The audit quotes only the t5 label, in a list introduced as "Documented variables I can use" whose figures are drawn from both files. Six lines below, the ex2col entry (lines 20-22) says "CORRECTED round 2: this audit originally quoted one label as if it were the only one, which is the same error it catches for `temp1` below." So the very failure mode round 2 identified survives in the same bullet list, which is the check D2 asks for ("check no equivalent survives anywhere in that file"). Design doc section 3

**Proposed fix:** Record both labels for logpgp95 in docs/provenance-audit.md line 18, as the ex2col entry now does: `logpgp95` "log PPP GDP pc in 1995, World Bank" in maketable5.dta, "log GDP per capita 1995" in maketable3.dta. Audit and design doc only; no draft words change.

### [MODERATE] consistency / E

**Text:** Places they did not

**Claimed evidence:** I opened charts/rf-3-the-flip.png: the right panel, over the n=69 ex2col==0 group, is titled "Places they did not" (make_charts.py line 179), meaning places Europeans did not colonise. Design doc 6.2 item 9 (lines 235-237) says "`ex2col == 0` means 'not on AJR's list', not 'never colonised'. It contains Bermuda, the Cayman Islands, Puerto Rico, Aruba and Cambodia ... the wording did not [hold] and is fixed." The draft body was fixed (line 76 "the 69 not on that list"; line 78 "That group is AJR's residual rather than a list of untouched places; Bermuda and Puerto Rico are in it") but the chart the reader sees was not, and its footnote carries no equivalent caveat. Both PRI (lpd1500s 1.7299, 

**Proposed fix:** Retitle the right panel "Places not on AJR's colony list" and add one clause to chart 3's footnote, e.g. "the right-hand group is AJR's residual, so it includes Bermuda, Puerto Rico and Aruba". Chart script only; regenerate rf-3-the-flip.png. No draft words change.

### [MODERATE] consistency / B5

**Text:** `rf-3-the-flip.png` Log population density 1500 against income today, two panels, former colonies and never colonised. The sign flip. Unchanged, and fixed before the data was seen.

**Claimed evidence:** docs/provenance-audit.md, whose own title line reads "Provenance audit, Post 25, run before any design", already contains exactly this relationship on 1995 income before the design document was written: the table at lines 29-32 reports "log population density 1500 | +0.05 (n=156) | **-0.58 (n=91)** | **+0.50 (n=65)**" under the heading "**The reversal replicates, and the split is the finding.**" The draft concedes this at lines 246-248: "Chart three was specified in the design document before the 2023 version was run, though the same relationship on 1995 income was already sitting in my provenance notes, so it is not a clean case." The design document's "fixed before the data was seen" there

**Proposed fix:** Amend design doc line 115 in place: "Unchanged, and fixed before the 2023 data was seen; the same relationship on AJR's 1995 income was already in the provenance audit, so it is not a clean pre-registration." Design document only; no draft words change.

### [MODERATE] logic / A16

**Text:** Outside that world heat ran the same way in both eras, minus 0.21 then and minus 0.29 now, which is the other half of the contrast.

**Claimed evidence:** Recomputed from build_analysis.load(): non-colonised heat vs 1500 density r = -0.2112, n = 76, t = -1.86, p = 0.0670. By the post's own evidentiary standard that is not clear of chance: the draft calls +0.28 with t = +2.39 (p = 0.0197) "weaker and only just clear of chance" (line 77) and calls t = -1.4 "not distinguishable from zero" (line 206-207). Asserting -0.21 flatly, with no hedge, is an inconsistent standard applied to the cell that carries the whole "and did not in the other" clause. Second problem: the "no inversion" in that group is a null, not a finding. Fisher-z comparing -0.2112 (n=76) with -0.2861 (n=85) gives z = +0.496, p = 0.6197 - failure to detect an inversion, not evidenc

**Proposed fix:** Replace with: "Outside that world heat did not visibly flip, minus 0.21 then, short of the usual threshold, and minus 0.29 now, the other half of the contrast." 26 words in, 26 words out, exactly word-neutral. It states the null as a null and flags that the -0.21 misses the bar the post applies elsewhere.

### [MODERATE] logic / A24

**Text:** Europeans chose where to go partly on the basis of what was already there, and partly on things like latitude that shape income today, so the thing I am conditioning on sits downstream of one side of the comparison and upstream of the other.

**Claimed evidence:** The "so" does not follow, and the structure named is not a collider. Clause 1 gives density1500 -> colonisation. Clause 2 gives latitude -> colonisation AND latitude -> income today; it makes C a DESCENDANT of a cause of the modern side, not a cause of it. The graph the two clauses actually establish is density1500 -> C <- latitude -> income2023: C has two arrowheads into it, so it is a collider on that path and conditioning on it opens the path. "Downstream of one side and upstream of the other" describes a mediator chain density1500 -> C -> income2023, a different structure with a different problem (over-control / post-treatment bias). Nothing in the sentence supplies the C -> income2023 a

**Proposed fix:** Replace "so the thing I am conditioning on sits downstream of one side of the comparison and upstream of the other" (20 words) with "so the thing I am conditioning on sits downstream of one side and of a cause of the other" (19 words, -1). That is the collider structure the two clauses actually establish, and it saves a word.

### [MODERATE] logic / A24

**Text:** That minus 0.74 is the measurement of it.

**Claimed evidence:** Minus 0.74 is corr(lat_abst, ex2col) = -0.7416 (n=167), which measures the latitude-to-colonisation link only, i.e. clause 2. It measures neither clause 1 (density1500 -> colonisation) nor any colonisation-to-income link. The unmeasured half is the load-bearing one: I computed corr(lpd1500s, ex2col) = -0.3497, n = 177, t = -4.94, p < 0.0001. Its SIGN is what matters - Europeans went to SPARSER places - because that, paired with corr(tas, ex2col) = +0.4152, is the opposite-signed selection configuration that manufactures a positive heat-density association inside the colonised stratum (see the A16 Berkson finding). The post cites the harmless half of the problem as "the measurement of it" and

**Proposed fix:** Replace "That minus 0.74 is the measurement of it." (8 words) with "That minus 0.74 measures the second link; the first is minus 0.35." (12 words, +4). Covered by the offsetting cuts named in the A28 fix.

### [MODERATE] logic / A16

**Text:** That is a within-country question rather than a question about the ranking between them, so the filter above does not touch it

**Claimed evidence:** The exemption is granted on the study's IDENTIFICATION STRATEGY, but the filter is about the properties of a MECHANISM. Whether Dell, Jones and Olken identified their effect from within-country year-to-year variation says nothing about whether the mechanism they identified could explain a between-country ranking - and the post is invoking them precisely as evidence that heat really does affect output ("it is evidence of a real effect of heat on output"), which is the mechanism the casualty sentence disqualifies eleven lines earlier. DJO themselves position the work on the between-country question: their published abstract (AEJ: Macroeconomics 4(3), fetched from https://www.aeaweb.org/article

**Proposed fix:** Replace "That is a within-country question rather than a question about the ranking between them, so the filter above does not touch it" (22 words) with "An effect that size in poor countries and not in rich ones is not the same everywhere, so the filter above does not touch it" (25 words, +3). Covered by the offsetting cuts named in the A28 fix. This exempts DJO on the correct conjunct and stops 

### [MODERATE] rhetoric / A26

**Text:** and their other measure runs through urbanisation

**Claimed evidence:** A26 (line 172) is correct and I verified it against the source: AJR (2002), p.1 of the NYU copy (pdftotext -layout), 'Our main measure of economic prosperity in 1500 is urbanization... As an additional proxy for prosperity we use population density, for which there are relatively more extensive data.' Confirms both halves of 'the wider-coverage second of AJR's two proxies rather than their first' (wider coverage also holds in this analysis: density n=163, urbanisation n=86, results.json). But the correction was applied in ONE place only. Line 49 still frames density as primary and urbanisation as the afterthought: 'Acemoglu, Johnson and Robinson, whose measure this is... and their other meas

**Proposed fix:** Line 49: 'and their other measure runs through urbanisation' -> 'and their main measure runs through urbanisation'. Net 0 words.

### [MODERATE] rhetoric / A15

**Text:** I am not going to tell you what caused the reversal.

**Claimed evidence:** OVER-CORRECTION check 1: the section no longer establishes a live scholarly dispute. Round 2 deleted the only sentence that did ('That argument has been running between serious people for decades...'), leaving this as a one-line paragraph at line 97. I grepped the entire body (lines 2-188) for every dispute signal: `grep -i "debate|dispute|contest|disagree|argu|economists|scholar|decades|literature"` returns only line 18 ('Nothing in this post disputes'), line 57 ('it is mine rather than the literature's', about a caveat), line 80, line 120 ('the most famous explanation in this literature' - names one explanation, does not say it is contested) and line 126. Nothing in the body tells the read

**Proposed fix:** Line 97 -> 'What caused the reversal has been argued over for decades, and I am not going to settle it here.' (+8 words). Pay for it at line 125 by cutting 'and I am leaving it as a set. Less satisfying, and the honest shape of what the data supports:' (-19 words), so line 125 reads 'That is a set, not an answer. The difference between "the tropics are hot" and...'. Net -11 words, and it also fixe

### [MODERATE] rhetoric / B6

**Text:** the replication file I read carries AJR's settler mortality series and their expropriation risk index, so the material for that argument was open on my desk and I left it alone. That is a choice about scope, not an absence of data, and a reader is entitled to know which one it was.

**Claimed evidence:** The disclosure's FACT is true: `data/ajr_t5/maketable5.dta` carries `logem4` (Stata label 'log settler mortality') and `avexpr` ('average protection against expropriation risk'). But it performs candour while dodging the question it raises. At lines 120-123 the body singles out ONE explanation by name as the thing its filter leaves standing: 'it contains the most famous explanation in this literature, in which a fixed tropical disease environment mattered enormously because of how it shaped European settlement.' That is the settler-mortality mechanism, i.e. `logem4`. So the single hypothesis the post elevates as surviving is the one whose data it had open and chose not to run, and B6 never c

**Proposed fix:** Method notes are outside the word ceiling, so this is free. Append to the B6 paragraph: 'That disease environment is also the one explanation this post names as surviving its filter, so leaving the settler-mortality series unrun is the most obvious gap here rather than a neutral scope choice. Running it would have made this an argument about institutions, which is a different post.'

### [MODERATE] rhetoric / B2

**Text:** That assumes the ranking of countries by warmth is roughly stable over five centuries.

**Claimed evidence:** The disclosure names a weaker assumption than the one the analysis actually makes. Every correlation in the post is Pearson, not rank: `build_analysis.py:81` is `r = float(np.corrcoef(s[x], s[y])[0, 1])`, and `corr()` is the only correlation function in the file (the +0.29, -0.18 and -0.25 figures all route through it, lines 130-131 and 180-181). Pearson r is not rank-invariant, so rank stability is insufficient: the cross-country temperature SPACINGS in degrees, not just the ordering, have to be roughly stable for these coefficients to mean what the post says. B2 is otherwise the most honest paragraph in the notes ('I am relying on the assumption rather than testing it'), which makes unders

**Proposed fix:** Method notes, outside the word count. Replace the sentence with: 'These are Pearson correlations, so the assumption is stronger than rank stability: the spacing between countries in degrees, not just their order, has to be roughly stable over five centuries.'

### [MODERATE] rhetoric / B7

**Text:** Places they did not

**Claimed evidence:** HOSTILE-READER, charts travel without the prose. I opened charts/rf-3-the-flip.png. Its right panel is titled 'Places they did not' (i.e. places Europeans did not colonise). The post's own body refutes that title at lines 76-78: 'Among the 69 not on that list... That group is AJR's residual rather than a list of untouched places; Bermuda and Puerto Rico are in it.' results.json `robustness.awkward_never_colonised` lists nine such codes including ABW, ATG, BMU. Round 2 fixed this wording in the body (A12) and in the method notes (B7, 'places absent from AJR's ex-colony list... a residual, not a curated set') and left the chart title alone. Chart 3's footnote does not correct it either. Shared

**Proposed fix:** make_charts.py, chart 3 right-panel title: 'Places they did not' -> 'Places not on AJR's list'. Charts are outside the body word count.

### [MODERATE] rhetoric / A11

**Text:** In 1500, hotter went with more crowded

**Claimed evidence:** HOSTILE-READER on the images. I opened charts/rf-2-the-same-heat-in-1500.png. Neither panel title carries a scope marker (round 2 dropped the '(former colonies)' suffix per C7), and the suptitle 'The same thermometer, pointing opposite ways five centuries apart' carries none either. So every large-type element of the image states, unrestricted, the exact global claim the post declares FALSE at lines 58-60 ('I pre-registered this chart as a global claim and the global version is false. Across all countries, temperature against 1500 density is minus 0.18'). The only correction is in the smallest text on the image, the footnote ('Former European colonies only... Hot places were not the dense pl

**Proposed fix:** make_charts.py chart 2 panel titles: 'In 1500, hotter went with more crowded' -> 'In the colonies in 1500, hotter went with more crowded'; 'Today, hotter goes with poorer' -> 'In the same places today, hotter goes with poorer'. Outside the body word count.

### [MODERATE] rhetoric / A13

**Text:** This is the test the argument actually rests on.

**Claimed evidence:** OVER-CORRECTION check 4: the deletion is inconsistent with the post's own practice. I counted the process admissions round 2 KEPT: five in the body (line 26 'I left those out of an earlier draft, which was the wrong instinct'; lines 58-59 'I pre-registered this chart as a global claim and the global version is false'; lines 112-113 'an earlier draft said something stronger and false'; lines 145-148 'I could have written the Indonesian section anyway'; lines 177-178 'I nearly wrote it as one') and six in the method notes (two bugs, a withdrawn variable, a false pre-registration, chart four chosen after the data, a gap in the falsification set, evidence loaded and unused). Round 2 deleted exac

**Proposed fix:** Restore a short form at line 81, paid for out of the 11 words freed by the A15 fix: 'This is the test the argument actually rests on, and an earlier draft asserted the pattern without running it.' (+11 words, exactly covered).

### [MODERATE] rhetoric / A21

**Text:** Former European colonies only, 94 with both measures. Circles are the percentile by population density in 1500, diamonds the percentile by GDP per capita today. Red slid down, blue climbed. Indonesia in amber, at the 79th percentile then and the 65th now, a 14 point slide that ranks it 47th of 94: t

**Claimed evidence:** HOSTILE-READER, colonisation-excuses-everything direction, on the images. I opened all four PNGs. Chart 4 shows eight named countries collapsing (Burundi, Sudan, Afghanistan, Rwanda, Uganda, Ethiopia, Pakistan, Burkina Faso) and six named places climbing (Singapore, Canada, Australia, Hong Kong SAR, United States, Guyana) under the title 'Who actually reversed', on an axis reading 'Percentile among former European colonies'. It is by some distance the most colonisation-loaded of the four images, and it is the only one of the four whose footnote carries no statement of what the chart does not show. Chart 1's footnote has one ('this chart cannot be read as heat acting on prosperity'); chart 3'

**Proposed fix:** make_charts.py, chart 4 footnote: append 'This is a description of who moved, not a claim about what moved them; the post does not say what caused the flip.' Outside the body word count. (The A21 text itself is arithmetically clean: results.json ranks give BDI 98.40/1.06, SDN 91.49/9.57, AFG 87.23/8.51, SGP 3.72/100.0, AUS 2.13/96.81, USA 5.32/98.94, IDN 78.72/64.89, slide 13.83, rank 47 of 94.)

### [LOW] consistency / D2

**Text:** The two files agree on the values (all 42 apparent disagreements are missing-versus-missing), so nothing downstream moves.

**Claimed evidence:** Recomputed three ways and 42 appears in none of them. Outer-merging both files on non-blank `shortnam` (256 rows each, 262 merged) gives 41 both-missing pairs plus 2 rows for ZWE where one file has NaN and the other 1.0, i.e. 43 non-equal pairs of which 2 are missing-versus-VALUE, so under that framing "all" is false. De-duplicating on shortnam first gives 41 (keep=first) or 40 (keep=last), all missing-versus-missing. The downstream conclusion holds - there is no value-versus-value contradiction - but the count is unreproducible, and it is a hand computation that no script in this repository emits, which is the rule design doc 6.2 item 6 invoked to move seven other figures into build_analysi

**Proposed fix:** Change to "all 41 apparent disagreements are missing-versus-missing once each file is de-duplicated on `shortnam`", or emit the count from build_analysis.py. Audit file only; no draft words change.

### [LOW] consistency / B5

**Text:** **Chart four was chosen after the correlations were run.** A chart picked after seeing the data is a weaker object than one picked before. Chart two was specified in advance as a global claim, that claim turned out false, and the chart was narrowed to former colonies after the data came back, which 

**Claimed evidence:** The four statements each reconcile with the design document individually: chart 1 against section 4 item 1 and the absence of any temperature-income correlation from the provenance audit; chart 3 against section 4 item 3 (with the caveat filed separately above); chart 4 against section 4 item 4 "**AMENDED 2026-09-07, chosen AFTER seeing the data**"; chart 2 against the struck-through section 4 item 2 plus its AMENDED note. But the ranking claim is not supported by anything: the design document ranks no chart against another, and the paragraph names two different worst charts in consecutive sentences - chart 4 is "a weaker object than one picked before" (it had no pre-registration at all) and

**Proposed fix:** Make the ordering explicit or drop the ranking: replace "which is the least clean of the four" (7 words) with "a rescued pre-registration rather than a kept one" (8 words, +1), or delete the clause entirely (-7 words).

### [LOW] consistency / E

**Text:** | 40 | Temperature is ERA5 near-surface air temperature, annual mean 1991 to 2020, from the World Bank Climate Knowledge Portal |

**Claimed evidence:** grep for "Climate Knowledge Portal" excluding "Climate Change Knowledge Portal" returns docs/claim-inventory-r1.md lines 79 and 89 and nothing else in the repository. Design doc 6.1 item 8 line 199 records the correction ("The portal is the Climate CHANGE Knowledge Portal"), and the draft, both scripts, results.json and the audit all use the corrected name, but the round-1 claim inventory that carries the claim text was never marked. It is a historical record rather than a shipping surface, which is why this is low.

**Proposed fix:** Add one line at the top of docs/claim-inventory-r1.md noting it is a frozen round-1 snapshot whose claim wording predates the corrections in design doc 6.1 and 6.2. No draft words change.

### [LOW] consistency / E

**Text:** ax.set_title("The tidy story, and it is true")

**Claimed evidence:** I opened all four PNGs. Chart 1's title is centred over the axes, roughly the middle of the image, while its own footnote begins at the left edge; charts 2, 3 and 4 all start their titles flush at the figure's left edge. The cause is in make_charts.py: chart 1 uses ax.set_title (line 106) while chart2 (line 154), chart3 (line 193) and chart4 (lines 236-237) use fig.suptitle(..., x=0.0, ha="left"). Design doc 6.2 item 11 fixed chart 4's alignment against charts 2 and 3 and closed with "All fixed", leaving chart 1 as the only chart of the four whose title does not align with its footnote.

**Proposed fix:** Replace chart1's ax.set_title("The tidy story, and it is true") with fig.suptitle("The tidy story, and it is true", fontsize=14.5, fontweight="bold", x=0.0, ha="left", y=1.02) to match the other three, and regenerate rf-1-the-tidy-story.png. No draft words change.

### [LOW] logic / A18

**Text:** A geographic story is not disqualified for being unable to see the colonial split. It is disqualified only if its effect also held steady across the five centuries.

**Claimed evidence:** Drift against A16 and A19. A16 requires a CONJUNCTION (constant over the period AND the same whether or not Europeans arrived); A19 is its exact negation and is consistent ("What survives is anything whose effect changed over those five centuries, and anything constant that acted differently depending on whether Europeans arrived"). A18 states only the first conjunct, and states it as a necessary condition. Two problems. First, the "also" has no antecedent: the preceding sentence is a negative ("not disqualified for being unable to see the colonial split"), so there is no earlier condition for "also" to be added to, and the condition it should point at - arrival-independence - is exactly the

**Proposed fix:** Tighten the first sentence and restore the missing conjunct in the second: "A geographic story is not disqualified for seeing the colonial split. It is disqualified only if its effect held steady across the five centuries and did not turn on whether Europeans arrived." First sentence 14 -> 11 words (-3), second 17 -> 22 (+5); net +2, and the -3 is one of the offsets already named in the A28 fix, s

### [LOW] logic / A16

**Text:** No explanation of the ranking between countries can have an effect that was both constant over the period and the same whether or not Europeans arrived. ... If something pressed equally on prosperity in 1500 and today

**Claimed evidence:** The bolded headline and the gloss that argues for it are not the same condition. "Constant over the period" is constancy throughout 1500 to today. "Pressed equally on prosperity in 1500 and today" is equality at the two ENDPOINTS only. Endpoint-equality is strictly weaker than constancy (constant implies endpoint-equal; the converse fails - an effect that was strong in 1500, reversed in 1700 and returned to its 1500 strength today is endpoint-equal but not constant). A conditional with a weaker antecedent and the same consequent is a STRONGER claim, so the gloss disqualifies a strictly larger class of explanations than the bolded sentence asserts. The paragraph therefore argues for something

**Proposed fix:** Make the headline endpoint-based, matching the gloss and the evidence: replace "an effect that was both constant over the period and the same whether or not Europeans arrived" (17 words) with "an effect that was the same in 1500 as today and the same whether or not Europeans arrived" (18 words, +1). Then A28's "whose effect never changed" should become "whose effect was the same in both eras" for 

### [LOW] rhetoric / A1

**Text:** What follows disputes what the correlation means.

**Claimed evidence:** Checked against what actually follows. Two of the five subsequent sections do not dispute what the correlation means. (a) 'The country I went looking for' (lines 129-148) is about the author's own country ranking 47th of 94 and about resisting a cherry-pick; it makes no claim about the temperature-income correlation at all. (b) The Dell et al. paragraph (lines 152-157) explicitly SUPPORTS the plain reading of heat: 'it is evidence of a real effect of heat on output', and the section it opens is titled 'What this does and does not show'. Round 2 weakened 'Everything in it disputes' to 'What follows disputes', which is quieter but still reads as covering everything after it, so the over-claim 

**Proposed fix:** Line 19: 'What follows disputes what the correlation means.' -> 'Most of what follows disputes what it means.' Net 0 words.

### [LOW] rhetoric / A20

**Text:** Less satisfying, and the honest shape of what the data supports: the difference between "the tropics are hot" and "the tropics are hot and something happened to them" is most of the argument.

**Claimed evidence:** OVER-CORRECTION check 5: the shortened sentence no longer says what it promises. The colon announces 'the honest shape of what the data supports' and then delivers a statement about rhetoric, not about data: 'the difference between X and Y is most of the argument' is a claim about where the argument's weight sits, not a shape any correlation in results.json supports. 'Less satisfying' also has no comparand left in the sentence after the shortening; the reader has to reach back to the previous clause to supply 'than an answer'. This is the tail of the post's central section, one sentence after the filter, so it is load-bearing prose.

**Proposed fix:** Cut the fragment, which is also how the A15 fix is paid for: line 125 -> 'That is a set, not an answer. The difference between "the tropics are hot" and "the tropics are hot and something happened to them" is most of the argument.' (-19 words).

### [LOW] rhetoric / A15

**Text:** I am not going to tell you what caused the reversal. / That is a set, not an answer, and I am leaving it as a set. / It does not show that institutions caused the reversal, or extraction, or disease. I have deliberately not gone there. / nobody should read "the split determines the sign" as a causal

**Claimed evidence:** OVER-CORRECTION check 10, the disclaimer count. Round 2 cut one of three, but the family is larger than round 2 measured. Grepping the body for refusals returns FIVE: line 60 ('I am not going to inflate it into something bigger than that', a scope refusal), and four causal refusals at lines 97, 125, 159-160 and 166-167 - plus a sixth restatement in the method notes at line 261 ('The post says it has deliberately not gone near institutions, extraction or disease'). Against that, the post states its actual thesis exactly once, in the bolded sentence at lines 102-103. Four in-body causal refusals to one thesis statement reads as a post that has decided in advance not to have one, which is a dif

**Proposed fix:** The A15 edit already removes one (line 125 loses 'and I am leaving it as a set'). Take a second at lines 159-160: cut 'I have deliberately not gone there.' (-6 words), which is fully restated in the method notes at line 261 and in the body at 166-167. Leaves three, with the line-97 refusal converted into the scholarly-dispute signal the section is missing.

### [LOW] rhetoric / A23

**Text:** Two problems with the comparison itself, on the record rather than buried.

**Claimed evidence:** OVER-CORRECTION check 5. The sentence promises a closed set of two and the section delivers three. 'The first is that splitting on colonisation is not innocent' (line 162), 'The second is that population density in 1500 and income per head today are not the same quantity' (line 169), and then, unnumbered and outside the promise, line 177: 'And the reversal is a fact about former colonies. It is not a fact about the tropics in general, and I nearly wrote it as one.' That third item is a limitation of exactly the same comparison, and it is the one a hostile reader would most want counted, because it is the guard against the colonisation-explains-everything reading. Announcing 'Two problems' an

**Proposed fix:** Line 162: 'Two problems with the comparison itself, on the record rather than buried.' -> 'Three problems with the comparison itself, on the record rather than buried.' Net 0 words. (Or move the line-177 paragraph above line 180 and label it 'The third is'.)
