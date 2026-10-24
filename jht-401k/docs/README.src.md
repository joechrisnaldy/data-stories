# Forced to Save, and I Never Knew It

Post 28 of the data-stories series. The US 401(k) is voluntary, yet savers watch it grow. Indonesia already requires workers to save through BPJS Ketenagakerjaan's Jaminan Hari Tua (JHT), with the worker and the employer paying in, but a worker can pay in for years without knowing. This folder compares what the same yearly saving became from {{growth.rules.first_year:year}} to {{growth.rules.last_year:year}} at JHT's rate for member balances, in an S&P 500 fund and in a 90/10 stock and bond mix, each in its own currency after its own inflation, and what each system shows the saver.

The rules were written down before any result, with dated amendments; the fee formula was settled after the first results, and the record says so; {{predictions.n_true:words}} of the {{predictions.n:words}} predictions written first came true. After inflation, the same saving became {{growth.sp500.multiple:dec1}} times what was put in for the S&P 500 saver, {{growth.mix_90_10.multiple:dec1}} times for the 90/10 saver and {{growth.jht.multiple:dec1}} times for the JHT saver ({{growth.jht_base_only.multiple:dec1}} at the base rate alone). JHT's rate was below Indonesian inflation in {{year_by_year.negative_real_imf.n:words}} of {{year_by_year.n:words}} years. BPJS has not published the rate it credited to JHT balances for the {{published.years_without_credited_n:words}} years after {{published.last_credited_year:year}}, while it still publishes the fund's investment yield. Not financial advice.

## Files

| File | What it is |
|---|---|
| `docs/2026-10-21-jht-401k-design.md` | The pre-registration and its dated amendments |
| `build_analysis.py` | Applies the pre-registered rules to the frozen data and writes `results.json` |
| `profile_data.py` | The shared readers and file hashes, and a profile of each input |
| `extract_jht.py` | Writes the JHT rates from the stored documents, checking each quoted passage |
| `test_extract_jht.py` | Tests that the extractor stops on a changed figure, quote, hash or year |
| `make_charts.py` | Draws the charts from `results.json` |
| `docs/jht-manifest.csv` | Each JHT rate with its document, page, hash and quote |
| `docs/sources.json` | The stored quotes behind the external figures the essay cites |
| `docs/provenance-audit.md` | The document that defines each variable, and the rights basis for each source |
| `gate.toml` | The blog gate's configuration for this post |
| `results.json` | Figures the essay prints |
| `charts/` | The charts in the essay |
| `data/README.md` | Where each data file the build reads comes from |
| `draft/*.src.md` (not committed) | The essay source |

## Run it

The data files and stored documents are not in the repository; `data/README.md` says where each comes from. Then, from this folder:

```bash
pip install -r requirements.txt
python3 extract_jht.py
python3 build_analysis.py
python3 make_charts.py
```

The build refuses to run on any data file that does not match the copy that was vetted.
