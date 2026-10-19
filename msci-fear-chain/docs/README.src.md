# What Should My Family Worry About If MSCI Drops Indonesia?

MSCI has proposed moving Indonesia from its emerging markets into the Standalone category. People fear a chain: the stock market crashes and stays down, the rupiah falls, foreign investors leave, and the cost of living rises faster; for a family it reaches savings and borrowing too. This folder tests each link against Indonesia's own history since {{meta.ihsg_first_year:year}}. The first four tests were fixed before any outcome was computed; the savings and borrowing tests were added after those results; their rules were fixed before the rate data was read, but not before the broad outline of Indonesia's economic history was known, and predictions were written down first, as the pre-registration records.

By those rules, the foreign-money link holds: foreign investors pulled money out of Indonesian shares around {{links.L3.n_meeting:words}} of {{links.L3.n:words}} past shocks. The other links do not hold. A year after a shock, the IHSG was back above its pre-shock level in {{links.L1.n_not_meeting:words}} of {{links.L1.n:words}} episodes; the rupiah was {{rules.rupiah_weaker:pct0}} percent or more weaker {{rules.rupiah_horizon_months:words}} months on after {{links.L2.n_meeting:words}} of {{links.L2.n:words}}; inflation sped up by {{rules.inflation_gap_pp:int}} percentage points or more after {{links.L4.n_meeting:words}} of {{links.L4.n:words}} rupiah slides; a one-month bank deposit lost buying power after tax after {{household.L5.verdict.n_meeting:words}} of {{household.L5.verdict.n:words}}; and the consumer-loan rate rose a point or more after {{household.L6.verdict.n_meeting:words}} of {{household.L6.verdict.n:words}}. Unemployment could not be tested. The samples are small, and the essay sets out the limits.

The essay: https://joechrisnaldy.com/blog/if-msci-drops-indonesia/

## Files

| File | What it is |
|---|---|
| `docs/2026-10-16-msci-fear-chain-design.md` | The pre-registration and its dated amendments |
| `build_analysis.py` | Reads the frozen data, finds the shock months and rupiah slides, tests each link, writes `results.json` |
| `make_charts.py` | Draws the charts from `results.json` |
| `profile_data.py` | Prints coverage and gaps |
| `extract_bapepam_2004_2005.py` | Writes the Bapepam month-end closes from the stored PDF |
| `extract_ihsg_corrections.py` | Writes the corrected month-ends from the stored IDX and Bapepam-LK PDFs |
| `seki.py` | Reads Bank Indonesia's SEKI rate tables (deposit, loan and policy rates) |
| `household.py` | The savings and borrowing tests, the policy-rate note, BPS's published rates and the fuel list |
| `extract_fuel.py` | Writes the fuel price changes from the stored regulations and notices, checking each quote |
| `docs/fuel-manifest.csv` | Each fuel price change with its document, hash and quote |
| `docs/2026-10-17-predictions-8.7.csv` | The predictions written before the rate data was read |
| `docs/sources.json` | The stored quote behind the deposit tax rate |
| `extract_idx_daily.py` | Writes the October closes from the stored IDX daily reports |
| `check_ihsg_2023on.py` | Writes the check of Bank Indonesia's recent month-ends against OJK's daily closes |
| `gate.toml` | The blog gate's configuration for this post |
| `results.json` | Figures the essay prints |
| `charts/` | The charts in the essay |
| `docs/provenance-audit.md` | The defining document and licence terms behind each source |
| `docs/ihsg-checks/` | The month-by-month checks of the index series |
| `data/README.md` | Where each data file the build reads comes from |
| `draft/*.src.md` (not committed) | The essay source |

## Run it

The data files are not in the repository; `data/README.md` says where each file the build reads comes from. Then, from this folder:

```bash
pip install -r requirements.txt
python3 build_analysis.py
python3 make_charts.py
```

The build refuses to run on any file that does not match the copy that was vetted.
