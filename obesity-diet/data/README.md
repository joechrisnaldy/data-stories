# Data

Four extracts, all from Our World in Data's grapher API, all tracing to primary statistical
producers. Nothing is joined from anywhere else. Files are not redistributed here; everything below
reproduces from scratch in under a minute.

## The files

| File | What it is | Producer | Coverage |
|---|---|---|---|
| `obesity-age-standardized.csv` | Adults with BMI of 30 or more, **age standardised**, both sexes, 18+ | WHO Global Health Observatory (2026) | 206 entities, 1980 to 2024 |
| `share-of-adults-defined-as-obese.csv` | The same measure, **crude**. Kept only to quantify what the choice does | WHO Global Health Observatory (2026) | 206 entities, 1980 to 2024 |
| `daily-per-capita-caloric-supply.csv` | Daily calorie supply per person | FAO Food Balance Sheets (2025) and, for the pre-1961 rows, historical reconstructions | 244 entities, 1274 to 2023 |
| `daily-caloric-supply-derived-from-carbohydrates-protein-and-fat.csv` | kcal from animal protein, vegetal protein, fat, carbohydrate | FAO (2025) | 244 entities, 1961 to 2023 |
| `gdp-per-capita-worldbank.csv` | GDP per capita, PPP, international dollars in 2021 prices | Eurostat, OECD, IMF, World Bank (2026), jointly | 212 entities, 1990 to 2025 |

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
Q="v=1&csvType=full&useColumnShortNames=true"
curl -sL -A "$UA" -o obesity-age-standardized.csv \
  "https://ourworldindata.org/grapher/obesity-prevalence-adults-who-gho.csv?$Q"
for s in share-of-adults-defined-as-obese daily-per-capita-caloric-supply \
         daily-caloric-supply-derived-from-carbohydrates-protein-and-fat \
         gdp-per-capita-worldbank; do
  curl -sL -A "$UA" -o "$s.csv" "https://ourworldindata.org/grapher/$s.csv?$Q"
done
```

Append `.metadata.json` to any of those grapher URLs to get the producer citation and the variable
definition. Do that before using a column; the slug is not the definition.

**A guessable slug is not a guarantee.** `share-of-calories-from-animal-protein` and
`caloric-supply-from-animal-and-vegetal-products` both 404. The age-standardised obesity series is
not at any slug containing "age-standardized"; it is at `obesity-prevalence-adults-who-gho`.

## TRAP 1: the default obesity chart is the crude estimate

OWID's headline obesity chart, `share-of-adults-defined-as-obese`, serves the **crude** prevalence.
Crude means not adjusted for age structure. Obesity rises with age across most of the adult range,
and countries differ enormously in how old their populations are, so a crude cross-country
comparison puts demography on the axis alongside obesity.

The two series correlate 0.9909 in 2023 across 199 countries, which is exactly why this is easy to
miss. The mean gap is only 0.41 points. Individual countries move much further:

| Country | Crude | Age standardised | Gap |
|---|---|---|---|
| Greece | 33.3% | 27.2% | +6.1 |
| Croatia | 35.7% | 30.1% | +5.6 |
| Latvia | 27.7% | 22.3% | +5.5 |
| Palestine | 33.0% | 37.2% | -4.3 |
| Syria | 29.8% | 32.8% | -2.9 |
| Iraq | 36.4% | 39.3% | -2.9 |

The sign is not random. Old populations (Greece, Croatia, Latvia) read heavier crude; young ones
(Palestine, Syria, Iraq) read lighter. That is age structure leaking into the measure.

**Handling: the age-standardised series everywhere.** The crude file is kept only to compute the
comparison above.

## TRAP 2: OWID aggregates sit in the same column as countries

The FAO files carry **52 non-country entities** mixed in with the countries: `World`, `Africa`,
`Asia`, `Africa (FAO)`, `Americas (FAO)`, `Belgium-Luxembourg (FAO)`, and so on. The GDP file adds
income groups (`High-income countries`, `Low-income countries`). A scatter that does not filter
these has fabricated points in it, and `World` sits right in the middle of the cloud where nobody
would notice it.

**Handling: keep only rows carrying a real three-letter ISO code.** `build_analysis.py` filters on
`code` being present, three characters long, and not starting with `OWID`.

**The three-character test is load-bearing, and the vet script missed it for three rounds.**
`profile_data.py` originally tested only for a missing or `OWID`-prefixed code. That is weaker,
because the WHO obesity files carry six regional aggregates coded `WHO_AFR`, `WHO_AMR`, `WHO_EMR`,
`WHO_EUR`, `WHO_SEAR` and `WHO_WPAC`: not blank, not `OWID`, and not three characters. The vet
therefore reported one non-country entity per obesity file where there are seven, and computed its
crude-versus-standardised comparison across 205 rows rather than 199. The script whose whole job is
catching aggregates was leaking six of them. Both files now share one `only_countries()`.

**No real country is lost to that rule.** An earlier version of this file said Kosovo was, which
was false and flattering: Kosovo has zero rows in the obesity file and zero in both FAO files, so
the ISO3 filter never touched it. It carries GDP rows under the code `OWID_KOS` and nothing else.

**The countries actually lost are lost to the income requirement**, one step later. See TRAP 7.

## TRAP 3: the macronutrient components are not a second measurement

It is tempting to treat "total calories" and "calories by macronutrient" as two independent things
to test. They are not. The four components sum to the calorie series itself:

```
max | (animal protein + vegetal protein + fat + carbohydrate) - total calories |
  = 0.077 kcal, across 10,187 country-years
```

That is a rounding residual, not a difference. Diet composition is the same FAO number cut a
different way.

This does **not** make the composition result meaningless: shares can carry information the total
does not, and here they carry roughly four times as much. It does mean the post cannot claim
composition as corroboration from a second source, and it does not.

## TRAP 4: FAO measures supply, not intake

Food balance sheets track what reaches the retail level. Household and retail waste is still inside
the number, and nobody eats a food balance sheet.

This matters more than the usual "the data is imperfect" caveat, because the gap between supply and
intake is unlikely to be constant across countries: it plausibly varies with income, which is itself
related to obesity. So it is not guaranteed to behave like well-mannered random error.

**But the direction of that bias is NOT known, and an earlier version of this file claimed it was.**
Waste that varies across countries adds spread to the calorie axis carrying no information about
intake, which attenuates a correlation; waste that rises with income, and therefore with obesity,
inflates it. Which dominates depends on quantities these files do not contain. Do not describe the
5.7% as conservative, generous, or biased in any stated direction.

## TRAP 5: eleven countries decide what income explains

The Pacific island states are the highest-obesity countries on earth: Tonga 73.0%, Nauru 71.1%,
Tuvalu 64.6%, Samoa 63.6%. They sit at middle incomes with extreme obesity, which is exactly the
position that flattens an income gradient.

| Sample | n | Obesity explained by log GDP per capita |
|---|---|---|
| All countries | 168 | **7.2%** |
| Excluding Pacific island states | 157 | **23.3%** |

Neither figure is wrong. Which one gets quoted is a choice about eleven countries out of 168, and a
statistic that moves by a factor of three on 7% of the sample is a finding rather than a nuisance.
**Handling: both are reported, in `results.json`, in the post, and on the chart itself, where the
eleven are drawn in a distinct colour rather than dropped.**

## TRAP 6: this is an ecological comparison

Every figure here is a country-level association. None of it says anything about whether an
individual's intake affects their own weight, and the post says so explicitly. A weak correlation
across countries and a strong relationship within a person are entirely compatible, and confusing
the two is the ecological fallacy.

Related: BMI of 30 or more is a threshold on a continuous measure, and BMI does not measure body
fat. A prevalence figure can move because the whole distribution shifted or because a cluster of
people sat just under the line.

## TRAP 7: income, not food data, is what sets the sample size

It is natural to assume a post about obesity and diet is limited by obesity and diet coverage. It
is not. For 2023:

| Filter | Countries |
|---|---|
| Age-standardised obesity | 199 |
| FAO daily calorie supply | 176 |
| Obesity AND calories | **172** |
| Obesity AND calories AND income | **168** |

The macronutrient file adds no constraint at all: its 2023 coverage is identical to the calorie
file's. So the binding constraint is the World Bank income series, and the four countries it
removes are **French Polynesia, Syria, Venezuela and Yemen**. Three of the four sit above the
sample's median obesity. French Polynesia is the sharpest case: at 48.6% it is heavier than any
country that did make the panel except the four Pacific states, and it is itself a Pacific
territory, so its absence thins out the very cluster the income chart turns on. What including it
would do to the 23.3% cannot be computed, because the missing income figure is the reason it drops
out: there is no income to place it at.

The panel is still the right choice, because using one set of countries for all four charts is what
makes the R2 values comparable across them. But the reason for 168 is income, and saying otherwise
describes a filter that was never run.

## Other things worth knowing

- **Analysis year is 2023**, the latest year all four series overlap. Obesity runs to 2024 and GDP
  to 2025, but FAO stops at 2023.
- **168 countries** survive the join across all four series.
- The joint least squares fit of obesity on calorie supply, log income and animal-protein share
  reaches R2 = 0.235 and has a root mean squared error of **11.0 percentage points**, on an outcome
  whose values run from 2.2% to 73.0%.
- Single-variable R2 values do **not** sum to the joint R2. The predictors are correlated with each
  other, so no share of the total is being attributed to any one of them, and none is claimed.

## What the vet found

Nothing wrong with any source. All four are official statistical output with documented methods and
free downloads. Every trap above is packaging, definition or scope: which estimate OWID serves by
default, which entities are countries, which numbers are independent of each other, and which
countries decide a headline. The post argues that the folk explanation for obesity does badly at
country level, and the reason it can argue that is that these producers publish enough detail to
check.
