# Data for Post 26

Of this folder, git tracks this README alone. Each file below is frozen by its SHA-256,
which `build_analysis.py` checks before it reads anything; a re-download needs a new vet.

| File | Source | Licence |
|---|---|---|
| `sp500_fred.csv` | FRED series `SP500`, S&P Dow Jones Indices LLC | Copyright © 2016, S&P Dow Jones Indices LLC. All rights reserved. Full notice below |
| `btc_coinmetrics_github.csv` | Coin Metrics, Inc., free data archive on GitHub, column `PriceUSD` | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) |
| `gold_worldbank_CMO-Historical-Data-Monthly.xlsx` | The World Bank: World Bank Commodity Price Data (The Pink Sheet): Bloomberg Finance L.P.; Kitco.com; International Monetary Fund, International Financial Statistics; London Bullion Market; Metals Week; Platts Metals Week; Shearson Lehman Brothers, Metal Market Weekly Review; Thomson Reuters Datastream; World Bank. Monthly prices, column `Gold` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| `covid_who.csv` | World Health Organization 2023 data.who.int, WHO Coronavirus (COVID-19) dashboard > More resources [Dashboard]. https://data.who.int/dashboards/covid19/more-resources | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

```bash
curl -o sp500_fred.csv "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500"
curl -o btc_coinmetrics_github.csv https://raw.githubusercontent.com/coinmetrics/data/master/csv/btc.csv
curl -o covid_who.csv https://srhdpeuwpubsa.blob.core.windows.net/whdh/COVID/WHO-COVID-19-global-daily-data.csv
```

The World Bank workbook is linked from `https://www.worldbank.org/en/research/commodity-markets`
as the monthly historical data file. FRED serves a rolling window of the S&P 500, so a later download
starts later and will not match the frozen hash.

## S&P 500 notice

As it reads on the [FRED series page](https://fred.stlouisfed.org/series/SP500):

> Copyright © 2016, S&P Dow Jones Indices LLC. All rights reserved. Reproduction of S&P 500 in any form is prohibited except with the prior written permission of S&P Dow Jones Indices LLC ("S&P"). S&P does not guarantee the accuracy, adequacy, completeness or availability of any information and is not responsible for any errors or omissions, regardless of the cause or for the results obtained from the use of such information. S&P DISCLAIMS ANY AND ALL EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, ANY WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE OR USE. In no event shall S&P be liable for any direct, indirect, special or consequential damages, costs, expenses, legal fees, or losses (including lost income or lost profit and opportunity costs) in connection with subscriber's or others' use of S&P 500.

## Traps hit while vetting

1. **FRED's Bitcoin series was rejected.** `CBBTCUSD` carries the next day's price under each date
   from September 2024 to November 2025, confirmed against Bitstamp, Coinbase and Coin Metrics.
2. **No free daily gold price whose terms allowed published charts was found in the vet.** So gold
   is the World Bank's monthly average, whose definition changed in June 2025.
3. **The Coin Metrics archive stops in May 2026.** The free API runs later, but Coin Metrics' former
   terms of use limited API data to internal use, so the post uses the archive and ends where it ends.
4. **The daily counts batch whole weeks onto Sundays for some countries, and have no new-case figures
   for France in the weeks covering 5 March to 5 May 2020.** So the Covid aside uses weekly sums.
5. **Read `covid_who.csv` with `keep_default_na=False`,** or pandas turns Namibia's code `NA` into a
   missing value.
