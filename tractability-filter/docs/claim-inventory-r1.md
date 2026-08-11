# Post 23 claim inventory, round 1

Every checkable claim in `draft/greed-you-can-regulate-difficulty-you-have-to-pay-for.md`.
Each refuter lens must return a verdict on every numbered item. Claims are quoted or closely
paraphrased.

## Transport

1. In 2000 the world lost 19.0 people per 100,000 to road traffic.
2. In 2019 it lost 16.7.
3. 2019 is "the most recent year the World Health Organization has published for that indicator".
4. That is a fall of 12 percent.
5. The span is "nineteen years".
6. Electric vehicles went from 0.012 percent of new car sales worldwide in 2010 to 25.0 percent
   in 2025.
7. That is "one of the fastest technology substitutions in industrial history". (Superlative:
   supportable, or must it be cut or softened?)
8. Road deaths "barely moved" inside the same window. (Note the windows differ: 2000 to 2019 for
   deaths, 2010 to 2025 for EVs. Is "the same window" accurate?)
9. The two chart panels are different units over different spans and are not on a common scale.

## Burden against effort

10. The analysis covers 34 conditions.
11. Burden alone explains "about 9 percent" of the variation in trial counts.
12. Back and neck pain is the THIRD largest cause of lost healthy life in rich countries.
13. It is behind only COVID-19 and ischaemic heart disease.
14. Back and neck pain costs 25.2 million healthy years a year in high-income countries.
15. Multiple sclerosis costs 692,879.
16. Back and neck pain carries 36 times the burden of multiple sclerosis.
17. It draws 1.6 times the trials.
18. Against rheumatoid arthritis: 27 times the burden.
19. Against rheumatoid arthritis: 1.7 times the trials.
20. Back pain is "one of the most thoroughly monetised conditions in medicine" via physiotherapy,
    imaging, injections, fusion surgery, and "a good deal of the opioid crisis". (Is this
    sourced anywhere? Verified or omit.)
21. Malaria destroyed 52.1 million healthy years worldwide in 2021.
22. Malaria destroyed 2,541 healthy years in high-income countries.
23. "There is no rich-world market for a malaria drug at all." (Overclaim risk: travel
    prophylaxis and military markets exist.)
24. Malaria has 1,472 registered trials.
25. Malaria drew 239.8 million dollars from the NIH in a single year.
26. The market measure is the share of a condition's global burden falling in high-income
    countries, and it has "no judgement in it".
27. Its coefficient runs a t of 0.71.
28. Adding it to the model makes the model slightly worse.
29. The tractability coding was done "before running any of this". (Cross-check against the
    design doc section 3.6, which records the coding was written AFTER a vetting table was read.
    Is the draft sentence accurate?)
30. 24 conditions have a validated target; their median is 1,448 trials per million healthy
    years lost.
31. 10 conditions have none; their median is 300.
32. Adding the binary lifts explained variation from 9 percent to 28.
33. The bottom of chart 2 shows road injury, falls, self-harm, hearing loss, migraine, back and
    neck pain as the no-target group. (Check: migraine is coded t1=True in conditions.py. Does
    the sentence misrepresent the chart's colouring?)
34. "Malaria is up in the top left" of chart 2. (Check against the rendered PNG.)

## The money

35. NIH fiscal year 2024 was used.
36. Money is compared against US burden.
37. 31 conditions are in the money analysis.
38. The slope runs a t of 0.77.
39. The adjusted R squared is negative.
40. Excluding HIV, tuberculosis and malaria improves it to a t of 2.23.
41. And to 12.5 percent of the variation.
42. The NIH funds HIV, TB and malaria "against world burden rather than American burden".
    (Assertion about NIH intent: supportable or must it be softened?)
43. Among the twelve largest burdens, dementias draw 895 dollars per healthy year lost.
44. Back and neck pain draws 12.
45. Multiple sclerosis draws 479.
46. That is 42 times what back pain gets per unit of damage.
47. Multiple sclerosis is NOT among the twelve largest burdens shown in the chart's bar panel.
    (Does the paragraph imply it is? Check for a false implication.)
48. Using Chronic Pain instead of Back Pain moves back pain's total from 68.8 million dollars to
    792.6 million.
49. "and it still loses". (Against what comparator? Check the arithmetic: 792.6M over back pain's
    US DALYs versus MS at 479 per DALY.)
50. Blue and amber in chart 3 are the same target coding as chart 2.
51. "the pattern is the same but softer".

## The part that did not work

52. The pre-registered prediction was a three-step gradient, tractable > partly > intractable.
53. Conditions coded least tractable sit ABOVE the middle group.
54. Depression has no validated causal target and no objective endpoint.
55. Depression has 12,693 registered trials.
56. Anxiety has 10,400.
57. Both beat back and neck pain.
58. Back and neck pain has more burden than either. (Check on which basis.)

## Artificial intelligence

59. Private investment in AI went from 6.01 billion dollars in 2013 to 290.1 billion in 2025.
60. That is a rise of 4,725 percent.
61. Total corporate investment reached 489.6 billion dollars in 2025.
62. Epoch AI tracks the training compute of 527 notable models.
63. "There is no measure of what any of this has done for human welfare. Not a weak one, not a
    contested one." (Strong universal negative. Refute if any published measure exists.)
64. The best available numbers are adoption figures.
65. Registered trials rose 87 percent between 2010 and 2019.
66. Healthy years lost per person in high-income countries fell 2.0 percent over the same window.
67. The bottom row of chart 4 has no bar.

## Conclusions and framing

68. "Research effort does not follow the biggest human problems."
69. "It does not follow the richest markets either."
70. "It follows the problems that have a handle on them." (Is this stronger than the evidence,
    given the money models are null and the global-basis result is weak?)
71. The two headline comparisons "do not depend on" the author's coding.
72. "I had already seen the broad shape of the data before I wrote the rule down." (Cross-check
    against design doc 3.6 for accuracy and completeness of the admission.)

## Method notes

73. Burden is DALYs from WHO Global Health Estimates 2021, July 2024 release.
74. Trial counts are the whole registry to date.
75. "Three burden bases, never mixed" and "Every figure above states which basis it uses."
    (Audit EVERY figure in the body against this promise. This is the most likely place for a
    real defect.)
76. On the global basis the effect explains 10 percent rather than 28.
77. With the no-target coefficient at t of minus 2.26.
78. Back and neck pain scores 6,334 under "back pain OR neck pain".
79. It would score 1,826 under "chronic low back pain".
80. Road injury scores 338 under the most generous wording and 18 under the least.
81. NIH categories are not a partition and do not sum to the total.
82. Leukaemia is excluded because no general category exists.
83. Road injury and falls are merged with burden summed.
84. "No claim about AI's benefits or harms is made or implied." (Check the whole draft against
    this, including the AI section's rhetoric.)

## Cross-surface

85. Every number in the four chart footnotes matches results.json and the prose.
86. No em dash, en dash or Unicode minus anywhere in the draft or in any rendered chart.
87. `README.md` and `data/README.md` agree with the draft on every figure they repeat.
88. No chart caption, tick label, annotation or alt text contains a hardcoded numeral that has
    gone stale.
89. Every reference resolves, attributes the right claim to the right producer, and the year is
    right.
90. The four image paths in the draft match the four files actually in `charts/`.
