# Skip the Matcha, Still No House

Post 29 of the data-stories series. A Forbes column calls it the permanent lipstick effect: young people priced out of a home spend on small treats instead. My view going in: Boomers and Millennials could save their way into a home and Gen Z can't, so small spending is rational. This folder tests the part that data can test, with a chase: a saver who turns 25 puts aside {{chase.rules.share_pct:dec0}} percent of the median income of US households their age each year, earns the Treasury bill rate, and chases a {{chase.rules.down_pct:dec0}} percent down payment on the year's median new home.

The rules were written down before the chase was run, with dated amendments; {{predictions.n_true:words}} of the {{predictions.n:words}} predicted outcomes written first came true. A young household's income bought the typical new home in {{ratio.household.first:dec1}} years in {{ratio.household.first_year:year}} and {{ratio.household.last:dec1}} years in {{ratio.household.last_year:year}}. The median Boomer chase took {{chase.generations.boomers.finished.median_years:words}} years across {{chase.generations.boomers.n:words}} start years; the {{chase.generations.millennials.finished.n:words}} Millennial chases that finished took a median of {{chase.generations.millennials.finished.median_years:words}}, and no Gen Z chase has finished yet. Snacks and nonalcoholic drinks bought away from home cost young households at most {{treats.narrow.max_target_pct:dec2}} percent of a year's down payment, while also saving eating out, entertainment and personal care as a whole cuts the median chase from {{treats.broad.base_finished.median_base_years:words}} years to {{treats.broad.base_finished.median_treat_years:words}} across {{treats.broad.base_finished.n:words}} start years. Not financial advice.

## Files

| File | What it is |
|---|---|
| `docs/2026-11-09-genz-house-chase-design.md` | The pre-registration and its dated amendments |
| `docs/provenance-audit.md` | The document that defines each variable, with the quote and where it sits |
| `docs/sources.json` | The stored quotes behind the external figures the essay cites |
| `profile_data.py` | The shared readers and file hashes, and a profile of each series the analysis reads |
| `chase.py` | The chase arithmetic, with no file access |
| `test_chase.py` | Tests of the chase on small made-up inputs |
| `build_analysis.py` | Applies the pre-registered rules to the frozen data and writes `results.json` |
| `make_charts.py` | Draws the charts from `results.json` |
| `gate.toml` | The blog gate's configuration for this post |
| `results.json` | Figures the essay prints |
| `charts/` | The charts in the essay |
| `data/README.md` | Where each data file the build reads comes from |
| `draft/*.src.md` (not committed) | The essay source |

## Run it

The data files and stored documents are not in the repository; `data/README.md` says where each data file comes from. Then, from this folder:

```bash
pip install -r requirements.txt
python3 -m unittest test_chase
python3 build_analysis.py
python3 make_charts.py
```

The build refuses to run on any data file that does not match the copy that was vetted.
