# Data

**There is no dataset file in this folder, and that is deliberate.**

This post is built entirely from primary sources. Every figure used in the essay and the charts is a
verified constant held in [`build_analysis.py`](../build_analysis.py) with its source recorded, and
mirrored into `results.json`. Nothing is scraped, interpolated, or modelled.

## Where each figure comes from

| Thread | Source |
|---|---|
| The 20% mandate, verbatim | UUD 1945 Art. 31(4), Fourth Amendment (10 August 2002) |
| The budgets struck down | Mahkamah Konstitusi, Putusan 026/PUU-IV/2006 and 13/PUU-VI/2008 |
| Compliance since 2009, APBN totals | Kementerian Keuangan, Informasi APBN 2024, 2025, 2026 |
| Tax-to-GDP comparisons | OECD, Revenue Statistics in Asia and the Pacific 2025 |
| Education spending, % of GDP, peers | World Bank / UNESCO Institute for Statistics |
| PISA scores, coverage, proficiency | OECD PISA country notes (2018 and 2022 cycles) |
| Learning poverty | World Bank, Indonesia Learning Poverty Brief (April 2024) |
| Enrolment, literacy, years of schooling | UNESCO Institute for Statistics; World Bank WDI |
| Spending and learning, global pattern | World Bank World Development Report 2018; OECD PISA 2022 |
| Teacher pay experiment | de Ree, Muralidharan, Pradhan & Rogers (2018) |
| 2026 budget composition | Sekretariat Negara (August 2025); Media Keuangan, Kemenkeu |

## One important measurement note

Indonesia's education spending as a share of GDP is computed **from the budget** (Rp665.0T of
Rp22,139.0T GDP = 3.00%, Kemenkeu, 2024), not taken from the World Bank/UNESCO series. That series
reports implausibly low recent values for Indonesia (1.28% of GDP), which are not consistent with the
country's own published budget documents. The peer countries in chart 2 do use the World Bank/UNESCO
series, so that chart mixes a budget-based Indonesian figure with survey-based peers, and the essay
and the chart footnote both say so.

## Three Kaggle datasets were rejected before this post existed

1. `laveshjadon/ai-impact-on-students`: synthetic. Sequential IDs, zero missing values, mutually
   independent inputs, and a burnout column that is an injected formula.
2. `harshadapatil31/student-performance-and-study-habits-dataset`: self-labelled "Simulated". A
   part-time job has no relationship to study hours, and 78 of 1,000 students score exactly 100.0.
3. `ashyou09/global-budget-allocation-dataset-19362026`: modelled. Every file is named
   `*_Real_Budget_*`, yet the United States carries one frozen set of percentages from 1936 to 2000,
   so the file contains no World War II.

See [`../docs/`](../docs/) for the full vetting notes.
