# Kiyosaki Was Half Right About Your House

Post 30 of the data-stories series. Robert Kiyosaki (2016) calls a house a liability, not an asset; the essay's reference list has the full entry. My view going in: a home gives comfort and security, but a big mortgage and fees would feel like a jail, and on money alone, renting and investing the difference can beat buying. This folder tests that with a race on US data. For each start year from {{rules.first_start:year}} to {{rules.last_start:year}}, a buyer and a renter live in the same typical home, start with the same cash and spend the same each month. The renter invests the down payment and buying costs on day one and the monthly difference after that in the US stock market; the buyer invests the difference whenever the rent is the larger cost.

The rules and {{predictions.n:words}} predictions were written down before the race was run, with dated amendments; {{predictions.n_true:words}} predictions came true. The rent of the same home is estimated with rent levels A and B, and a verdict counts as buy or rent only when both levels agree. After {{headline.30.all.h:int}} years, the renter was ahead under both levels in {{headline.30.all.rent:int}} of {{headline.30.all.n:int}} start years and it depends on the rent in {{headline.30.all.depends:words}}; the buyer was never ahead under both. Buying won some shorter stays: after {{headline.5.all.h:int}} years, {{headline.5.all.buy:int}} of {{headline.5.all.n:int}} start years. Under level A, the down payment and buying costs alone, invested on day one, tied or beat the buyer after {{rules.max_h:int}} years in {{share_to_tie.30.summary.a.zero:int}} of {{share_to_tie.30.summary.n:int}} start years. Not financial advice.

## Files

| File | What it is |
|---|---|
| `docs/2026-11-13-rent-vs-buy-design.md` | The pre-registration: rules, predictions, limits and the dated amendments |
| `docs/provenance-audit.md` | The document that defines each variable, with the definition and where it sits, and each data file's address and hash |
| `docs/sources.json` | The stored quote behind the external figure the essay cites |
| `profile_data.py` | The pinned file hashes and readers, and a profile of each series the analysis reads |
| `extract_z1.py` | Extracts the Federal Reserve Z.1 series the race uses from the full Z.1 package |
| `rentbuy.py` | The buy-or-rent model, with no file access |
| `test_rentbuy.py` | Tests of the model on small made-up inputs |
| `build_analysis.py` | Applies the pre-registered rules to the pinned data and writes `results.json` |
| `make_charts.py` | Draws the charts from `results.json` |
| `gate.toml` | The blog gate's configuration for this post |
| `charts/` | The charts in the essay |
| `data/README.md` | Where each data file comes from, its terms and credits, and how to rebuild |
| `draft/*.src.md` (not committed) | The essay source |

## Run it

The data files and stored documents are not in the repository; `data/README.md` says where each data file comes from. Then, from this folder:

```bash
pip install -r requirements.txt
python3 -m unittest test_rentbuy
python3 -I extract_z1.py
python3 -I build_analysis.py
python3 -I make_charts.py
```

The build refuses to run on a data file that does not match the copy that was vetted.
