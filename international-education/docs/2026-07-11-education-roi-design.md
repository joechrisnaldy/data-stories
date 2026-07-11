# Post 06: "The Cheapest Degree Abroad Isn't the Best Deal" (education ROI)

Design doc for the sixth data story. Primary dataset: Kaggle
`adilshamim8/cost-of-international-education` (International_Education_Costs.csv). Joined
with external OECD wage and employment data. Folder: `analytics-blog/international-education/`.

Date: 2026-07-11
Status: approved POV and title, design pending user review

## The data (profiled)

`International_Education_Costs.csv`: 907 rows (one per program at a university), 12 columns,
71 destination countries. Columns: Country, City, University, Program, Level (Bachelor /
Master / PhD), Duration_Years, Tuition_USD, Living_Cost_Index, Rent_USD, Visa_Fee_USD,
Insurance_USD, Exchange_Rate. Created May 2025. The only external join key is Country.

The dataset has cost only. It does NOT include average salary or employment rate, so those
come from external, authoritative, up-to-date sources.

## Scope (locked with the user)

Restrict the salary side to the roughly 30 OECD destinations where a clean, comparable
average wage exists. Clean and defensible; these are also most of where people actually
study abroad. Accepted cost: this drops non-OECD destinations (Singapore, Malaysia, UAE,
China, India, Indonesia and others) from the wage analysis. Exact overlap of the 71 cost
countries with OECD wage coverage to be confirmed at build (expected about 30).

Primary lens: Master's-level programs (the most common international degree and the most
comparable across countries). Bachelor and PhD noted where relevant.

## POV (locked with the user)

- **Angle:** the return on investment of an international degree (cost versus salary versus
  employment).
- **Thesis:** "Sticker price is the wrong ruler." People shop for a degree abroad by tuition
  sticker price, and the cost ranking (USA, UK, Australia expensive; Germany, the Nordics
  cheap) is misleading. Measure value as payback (years of the local average salary to earn
  the degree cost back), with employment rate as the reality check. The value ranking
  reshuffles: some expensive places pay back fast on high wages, and some cheap, high-wage
  places (likely Germany) are the real bargains. Price is not value; the right ruler is what
  you get back. This is the fourth measuring-stick cousin (currency, metric, circular target,
  now sticker price).
- **Indonesia weight:** light touch. One paragraph near the end on the sticker-price instinct
  (the gengsi, prestige, of an expensive Western degree) versus the payback truth. Universal
  framing otherwise.

## The core metric

For each OECD destination country, aggregate the Master's programs to a country total cost:

total_cost = Tuition_USD * Duration_Years + Rent_USD * 12 * Duration_Years + Visa_Fee_USD +
Insurance_USD

Then payback = total_cost / average_annual_wage (OECD, 2024, PPP-USD) = years of the local
average salary to earn the degree back. Employment rate (OECD or World Bank, 2024) is the
"will you actually get the job" overlay: value is payback discounted by the odds of working.

Aggregation: median (robust to a few elite, expensive universities) across the Master's
programs per country; report the number of programs behind each country's figure and drop
countries with too few programs to be stable.

## Section flow (the spine)

1. **Open (stance-first).** Everyone shops for a degree abroad by the tuition sticker price,
   and it is the wrong ruler.
2. **The cost ranking (chart 1).** Total Master's cost by country. The familiar, expensive-
   West ranking.
3. **The payback reshuffle (chart 2).** Years of local salary to earn it back. The ranking
   changes; the real bargains appear.
4. **The employment reality check (chart 3).** Payback assumes you land the job; overlay
   employment rate so value is payback and the odds of working together.
5. **Close (light Indonesia + universal).** The sticker-price instinct versus the payback
   truth; price is not value.

## Charts (3)

Series dataviz palette. (1) total cost ranking by country; (2) the payback ranking (years of
local wage), showing the reshuffle versus chart 1; (3) an employment overlay or a
cost-versus-payback view that folds in employment rate.

## Honesty guardrails (these are large and must be foregrounded)

- The destination-country wage ASSUMES the student stays and works there. Many international
  students return home or cannot get a work visa. This is the load-bearing assumption and the
  essay must say so plainly and early.
- Average wage is not a NEW-GRADUATE wage, so payback reads optimistically (a fresh graduate
  earns below the economy-wide average at first).
- OECD wage and employment are economy-wide, not by field of study; a data-science graduate's
  payoff differs from the average.
- The cost data is a sample of programs and universities, not an exhaustive census; the
  country figure depends on which programs are in the sample.
- Payback ignores forgone earnings, scholarships, debt interest, and the non-monetary value
  of a degree. This is a rough ROI lens for comparison, not financial advice, and the essay
  says so.
- No long dashes; APA 7 references for every external fact.

## External data and references (APA 7, to pin at build)

- OECD average annual wages, 2024, PPP-adjusted USD (dataset AV_AN_WAGE). Source and exact
  figures pinned at build (OECD Data Explorer, or a reliable mirror cross-checked to OECD).
- Employment rate by country, 2024 (OECD employment rate, or World Bank / ILO
  employment-to-population ratio). Source pinned at build.
- The cost dataset: Kaggle (adilshamim8, 2025).

## Scope and mechanics

- Length: weekend-sized, about 1,300 to 1,700 words.
- Folder `analytics-blog/international-education/` (cost data pulled to `data/`, gitignored
  except a data README; the small external wage/employment table committed as a CSV with its
  source documented).
- Scripts profile_data.py, build_analysis.py, make_charts.py; results.json.
- Output: MDX to the Astro blog, slug equal to filename, 3 charts copied to
  `site/public/images/blog/educationroi-*.png`, live on joechrisnaldy.com.
