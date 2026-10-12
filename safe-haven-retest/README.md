# The Dip I Waved Away

Post 26 of the data-stories series. In late 2020 I drafted a research proposal claiming Bitcoin was
"more stable" and "safer" than Indonesia's LQ45 stocks during the pandemic. This post audits that claim with current
data, against the S&P 500 and against gold.

| Finding | Figure |
|---|---|
| Bitcoin's largest fall from 5 March to 5 May 2020, the window my draft used | 46 percent, against 26 percent for the S&P 500 |
| Bitcoin's average log return on the S&P 500's worst 5 percent of days | minus 4.4 percent (81 days) |
| Gold's average log change in the S&P 500's worst 10 percent of months, monthly averages | minus 0.5 percent (8 months) |
| Bitcoin's in the same months | minus 13.1 percent (8 months) |

Verdicts: the 2020 claim, tested against the S&P 500 instead of LQ45, was wrong; by my test, Bitcoin was not a safe haven on daily data, with or
without the Covid crash; gold was a weak safe haven by this test on monthly data.

## Files

| Path | What |
|---|---|
| `build_analysis.py` | The results the post states, into `results.json` |
| `make_charts.py` | The four charts; the figures on each chart read from `results.json` |
| `data/README.md` | Sources, credits, licences and download instructions |
| `profile_data.py` | The structural checks behind the dataset go/no-go, rerunnable |
| `gate.toml` | This post's configuration for the shared gate in `../gate/` |
| `docs/README.src.md`, `docs/data-README.src.md` | Templates for this file and `data/README.md`, rendered by the gate |
| `docs/2026-10-09-safe-haven-retest-design.md` | The pre-registration, with amendments in section 8 |
| `docs/provenance-audit.md` | What each source and data series is, quoted from the document that defines it |
| `draft/*.src.md` (not committed) | The draft as written: each figure a `key:fmt` placeholder |

Not financial advice.
