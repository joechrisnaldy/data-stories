# Reading Part of One Sentence Counts as Literate

Post 22 in the data-stories series. [Read the essay](https://joechrisnaldy.com/blog/reading-part-of-one-sentence-counts-as-literate).

## The question

Most of the world's adults are recorded as literate. What was actually measured to produce those
numbers?

This is an explanatory post, not an expose. The DHS Program publishes its coding rule, the Stata
that implements it, and a note warning that its own older estimates may overstate literacy. Nothing
here was hidden. The gap is between what the indicator can certify and what the word promises.

## What the data says

**The rule, stated exactly.** The published literacy indicator is `v106 = 3 or v155 in 1,2`. That
is: more than secondary education, or read a whole sentence off a card, or read **part** of one.
Respondents above secondary are never handed the card at all. So for anyone with enough schooling,
the indicator has no state that means "this person cannot read".

**What a literacy rate is made of.** Across the 46 countries using the current rule, most of the
people counted literate did read a whole sentence: 45.5 points at the median, about 68 percent of
the median country's literate population. The post is about the other third. The median
never-tested share is 7.2 points and the median partial-reader share is 9.6. Those are separate medians, not one country's profile. Cambodia has the largest partial-reading band in points, 28.0 of its 80.5. Measured as a share of
the literate population the extreme is Sierra Leone, at 43.0 percent. The Philippines reports 98.8 percent literate, of
which 37.3 points were never tested.

**The instrument errs downward too.** Where the interviewer had no card in the respondent's
language, a fluent reader is recorded as illiterate. Small, under a tenth of a percent at the median, but real.

**The year the instrument changed.** DHS used to exempt everyone with secondary education or above;
it now exempts only those above secondary. Between 2014 and 2022 the share of Ghanaian women with
secondary or higher education rose from 63.1 to 70.2 percent while measured literacy fell from 67.1
to 60.8. In 2014, 94.0 percent of Ghana's literacy rate was people never asked to read anything.
India, Indonesia and Nigeria rose across the same change. Real schooling grew over their gaps as
well, fastest in the two five-year windows: India added 5.7 points of secondary-or-higher education
and Indonesia 7.5 against Nigeria's 8.8 across nine years, each larger than the literacy rise it
would have to explain, so the rule change
and the schooling cannot be separated in those three panels. The rule moves the composition everywhere. Of these four it decides the headline only in Ghana, but
the four are worked examples: 39 countries have surveys under both rules and five headlines fell,
three of them with education rising more than five points as literacy dropped.

**How the world's literacy statistics are produced.** Of 686 country-years where UNESCO records the
method, 52 came from an actual literacy test. 333 are self-reported by the head of the household on
behalf of everyone in it. 283 are self-reported by the individual.

**Who is asked to prove it.** 40 countries have ever been recorded using a test; 129 have not. Of the 25
European countries in the file, 22 have only ever self-declared, Andorra reports an indirect
estimate, and only Bosnia and Herzegovina and Ukraine have ever been recorded testing. The tested list
includes Chad, Niger, Sierra Leone, Malawi and Haiti. Countries whose rate came from a test sit at a
median literacy of 73.2 percent against 94.1 for individual self-report, and that gap has two
readings the data cannot separate.

## The lesson

A measure that cannot record failure cannot report success.

## Charts

| | |
|---|---|
| `charts/lit-1-what-literate-is-made-of.png` | The four bands inside a published literacy rate, 46 countries on the current coding rule |
| `charts/lit-2-the-year-the-instrument-changed.png` | Ghana, India, Indonesia and Nigeria, before and after the rule change, drawn as composition rather than as a trend |
| `charts/lit-3-how-the-numbers-are-made.png` | 686 country-years by reporting method |
| `charts/lit-4-who-is-asked-to-prove-it.png` | Reporting method against the literacy level it produced, 159 countries |

## Running it

```bash
python3 fetch_data.py       # four files, under 1.5 MB, from the DHS API and Our World in Data
python3 build_analysis.py   # writes results.json
python3 make_charts.py      # writes charts/
```

Every number in the essay is produced by `build_analysis.py` and read from `results.json`.

## Notes on doing this honestly

The traps are documented in [`data/README.md`](data/README.md), and several would have produced a
confidently wrong post:

- The API mislabels the never-tested column as "secondary or higher education" when its current
  numerator is *higher than* secondary. The label and the definition disagree.
- Neither survey type nor fieldwork year identifies the rule change: Ghana 2014 and Ghana 2022 are
  both full DHS rounds on opposite sides of it, and the two regimes overlap from 2015 to 2016.
  Surveys are classified by comparing the never-tested column against both published education
  shares, which separates them to 0.005 points against 32.9 for the wrong assignment.
- DHS omits a column when it rounds to zero. Requiring all eight silently dropped 65 percent of the
  surveys, including every country this post names.
- Three different constructions are in play and none is averaged with another: DHS's published
  table for women 15 to 49, UNESCO's adult 15-and-over rate, and Our World in Data's compilation of
  DHS survey estimates across all respondents. The last two disagree by up to 15.9 points on the
  same country, around a mean of 1.8.
- Chart 4 concedes its own ambiguity on its face rather than in a footnote nobody reads.
- **There is no rich-world proficiency panel, on purpose.** The obvious one, comparing declared
  literacy against tested adult proficiency in high-income countries, needs PIAAC, which is not in
  the OECD SDMX API. Rather than reach for a weaker substitute, the second movement was rebuilt on
  UNESCO's record of who tests and who declares, which answers the same question from data already
  in hand.

Written by Jonathan Chrisnaldy. Sources are The DHS Program and the UNESCO Institute for Statistics
via Our World in Data. Datasets are not committed; `fetch_data.py` reproduces them.
