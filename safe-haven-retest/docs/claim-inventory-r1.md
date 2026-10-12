# Claim inventory, round 1 (Post 26)

Every sentence of the rendered draft body, numbered. Every item gets a verdict. Charts, alt text,
READMEs and the reference list are covered by the lenses directly.


**The Dip I Waved Away**

1. In late 2020 I started a research proposal, in Indonesian, on whether Covid-19 and Indonesia's LQ45 stock index moved the price of Bitcoin.
2. I never finished it.
3. Chapter one exists; the rest are headings.
4. But chapter one had already reached its answer.
5. Bitcoin, I wrote, was "much more stable" than the stocks and "tended to rise".
6. There was a fall on 11 March, then a significant rise again.
7. So during a pandemic, Bitcoin was "more promising and safer" than buying stocks.
8. (The quotes are my translation.)
9. This post audits that claim in public, with current data.
10. Two things change.
11. It goes global: instead of LQ45 it tests the claim against the S&P 500, the index readers are more likely to know, so the verdict is on the general claim that Bitcoin was steadier and safer than stocks, not on Indonesian stocks in particular.
12. And it adds the asset people mean when they call Bitcoin "digital gold": gold.
13. The tests, and what would count as passing them, were written down before I downloaded any data.

**Two dates, and the path between them**

14. My draft compared 5 March and 5 May 2020.
15. On those two dates the claim holds up.
16. Bitcoin finished the window at minus 0.8 percent and the S&P 500 at minus 5.1 percent.
17. Judged by its endpoints, Bitcoin did better.
18. Now look between them.
19. Bitcoin's largest fall inside the window was 46 percent, bottoming on 12 March.
20. The S&P 500's largest fall was 26 percent, bottoming on 23 March.
21. Bitcoin's daily volatility, the standard deviation of its daily log returns, was 9.2 percent against 4.5 percent for the index, across 43 trading days.
22. That is the dip I waved away.
23. My draft saw it, called the recovery significant, and kept going.
24. The recovery was real.
25. It was a recovery from a fall of 46 percent, in the asset I had just called more stable than stocks that fell 26 percent.
26. Before downloading anything, I wrote down what the 2020 claim had to show to survive: Bitcoin's largest fall in that window had to be smaller than the S&P 500's, and its daily volatility lower.
27. It failed on both counts.
28. In the words I committed to in advance: the 2020 claim was wrong.

**What "safe" means, and a test you can run**

29. The finance literature has a precise version of what I was reaching for.
30. Dirk Baur and Brian Lucey split it in two.
31. An asset is a hedge if it is uncorrelated or negatively correlated with stocks on average, and a safe haven if it is uncorrelated or negatively correlated with stocks in extreme market conditions (Baur & Lucey, 2006).
32. Baur and McDermott then split the safe haven into weak, an asset uncorrelated with stocks in those conditions, and strong, an asset negatively correlated with them, and note that the weak kind keeps its value when the market falls while the strong kind gains (Baur & McDermott, 2009).
33. Their tests are regressions on the market's worst days.
34. Mine is not their test.
35. It asks the value question directly, and anyone with a spreadsheet can run it:
36. 1.
37. Take the stock market's worst days, here the S&P 500's worst 5 percent of days. 2.
38. Average what your asset did on those days, and put a 95 percent confidence interval around that average. 3.
39. If the whole interval sits below zero, it is not a safe haven.
40. If it includes zero, call it a weak safe haven.
41. If the whole interval sits above zero, a strong safe haven.
42. The weak bar is generous.
43. A volatile asset gets a wide interval, and a wide interval is more likely to include zero.
44. The strong bar has the opposite weakness: an asset that usually rises can clear it without being negatively correlated with anything.

**The worst days**

45. From 2 January 2020 to 22 May 2026 there were 1,605 daily returns, so the S&P 500's worst 5 percent of days is 81 days.
46. On those days the S&P 500 averaged minus 3.1 percent.
47. Bitcoin averaged minus 4.4 percent, with an interval from minus 5.9 to minus 2.8, and it rose on 16 of the 81 days.
48. By my own test, Bitcoin is not a safe haven.
49. It does not rest on the Covid crash.
50. Drop the days from the S&P 500's February 2020 high to its March low and the S&P 500's worst 5 percent of the remaining days is 80 days, on which Bitcoin averaged minus 3.7 percent: the same verdict.
51. Counting that check, I ran eight variations of the test, adding the worst 1 percent of days and two-day returns, which allow for Bitcoin's price being taken a few hours after the stock market closes.
52. The verdict held in six of them.
53. It did not hold for the worst 1 percent of two-day periods, where nine periods remain and the interval is wide enough to include zero.
54. Gold is harder.
55. I could not find a free daily gold price whose terms let a blog publish charts made from it, so gold comes from the World Bank's monthly average price (World Bank, 2026), and the comparison has to be monthly as well: Bitcoin, gold and the S&P 500 as calendar-month averages, which dampen how deep a crash month looks.
56. In the S&P 500's worst 10 percent of months, eight of 75, the S&P 500 averaged minus 7.4 percent.
57. Gold averaged minus 0.5 percent, with an interval from minus 4.0 to plus 3.0: a weak safe haven by my test.
58. Bitcoin averaged minus 13.1 percent, with an interval from minus 24.8 to minus 1.4: not a safe haven.
59. Eight months is a small sample, and the monthly verdict on Bitcoin does rest on the Covid crash.
60. Leave out 2020 and the S&P 500's worst 10 percent of months is seven of 64, in which Bitcoin averaged minus 10.3 percent with an interval from minus 21.8 to plus 1.2.
61. That includes both zero and the S&P 500's own average of minus 5.5 percent, so the monthly test cannot tell.
62. Gold's verdict held without 2020 and in the S&P 500's worst 20 percent of months.

**Each big fall since 2020**

63. My rule for a stress episode: a fall of 15 percent or more from an S&P 500 all-time high, running from that high to the lowest close before the high was regained.
64. Since January 2020 there were three: February to March 2020, January to October 2022, and February to April 2025.
65. A 10 percent threshold finds the same three.
66. Bitcoin fell further in each: 49 percent against the S&P 500's 34, then 61 against 25, then 22 against 19.
67. It also got back to its starting level sooner in each: 55 trading days against 126, 505 against 513, and 51 against 89.
68. In the 2022 episode they were close.
69. Deeper falls, faster rebounds.
70. For someone who can sit through a fall, that may be worth something.
71. It is not what safe means.
72. A safe haven is supposed to hold its value while stocks are falling, not to recover sooner afterwards.

**Digital gold, or something else**

73. The hedge test asks about the average relationship.
74. On daily returns, Bitcoin moved with the S&P 500 at a correlation of 0.40 across 1,605 days.
75. On monthly averages, like for like with gold, Bitcoin's correlation was 0.51 and gold's 0.16, across 75 monthly changes.
76. Gold's is small enough to be chance (p = 0.16).
77. Bitcoin's is not.
78. Over rolling 24-month windows, Bitcoin's correlation with the S&P 500 stayed between 0.29 and 0.60.
79. Gold's swung from 0.49 to minus 0.29.
80. Over this period gold behaved like the hedge in the definition and Bitcoin did not: it moved with stocks.

**The Covid question I started with**

81. My draft's first question was whether Covid-19 cases moved the price of Bitcoin, and its planned method was a neural network.
82. Here is what the data allows.
83. WHO's counts are by date of reporting, and some countries group several days into one report (World Health Organization, n.d.), so I summed world cases by week.
84. The window touches ten weeks.
85. Week-on-week growth in world cases correlated with Bitcoin's weekly return at minus 0.50 and with the S&P 500's at minus 0.54.
86. With ten points, and with case growth slowing over the same weeks that markets recovered, those correlations do not separate Covid from the rest of what happened that spring.
87. The counts have gaps too: WHO's daily file records 0 new cases for France in those weeks.
88. My planned neural network would have been trained on daily data from 5 March to 5 May 2020: a single stretch of a single spring, a daily case series that weekly batching distorts, and no way to tell what else was happening.
89. The question was a fair question to ask.
90. The method could not have answered it.

**What I would tell my 2020 self**

91. Look at the path, not the two dates.
92. The endpoints said Bitcoin held up; the path said it fell 46 percent on the way.
93. Run the test before using the word.
94. Take the stock market's worst days, average what the asset did on them, and check whether the interval clears zero.
95. Then check it again with the big crash left out.
96. On that test, over these years, Bitcoin fell with stocks, and gold's average stayed close to zero.
97. This is an audit of my own old claim, not investment advice.
98. No sentence here recommends buying or selling anything.

**Method notes**

99. **Data.** The S&P 500 is FRED's daily close of the price index, which excludes dividends (S&P Dow Jones Indices LLC, 2026).
100. Bitcoin is the Coin Metrics reference rate, PriceUSD, from the free data archive of Coin Metrics, Inc.
101. (Coin Metrics, 2026).
102. Gold is the World Bank's monthly average price in US dollars per troy ounce (World Bank, 2026): the average of daily London afternoon fixings to May 2025 and of daily spot rates from June 2025.
103. Gold's verdicts are the same without the May and June 2025 values, where the series changed definition.
104. Covid-19 cases are WHO's daily reports, summed by week (World Health Organization, 2023).
105. I transformed each series: rebased, converted to returns, averaged or summed as described above.
106. **Credits and notices.** This is a non-commercial post, and no publisher of these data endorses it.
107. - S&P 500: Copyright © 2016, S&P Dow Jones Indices LLC.
108. All rights reserved.
109. The full notice, which FRED asks users to keep with the data, is on the [FRED series page](https://fred.stlouisfed.org/series/SP500). - Bitcoin: Coin Metrics, Inc., from [github.com/coinmetrics/data](https://github.com/coinmetrics/data), licensed [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), and published by Coin Metrics "without any warranty". - Gold: The World Bank: World Bank Commodity Price Data (The Pink Sheet): Bloomberg Finance L.P.; Kitco.com; International Monetary Fund, International Financial Statistics; London Bullion Market; Metals Week; Platts Metals Week; Shearson Lehman Brothers, Metal Market Weekly Review; Thomson Reuters Datastream; World Bank.
110. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). - Covid-19 cases, cited as WHO asks: World Health Organization 2023 data.who.int, WHO Coronavirus (COVID-19) dashboard > More resources [Dashboard].
111. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
112. **Samples.** The daily layer runs from 2 January 2020 to 22 May 2026, 1,606 S&P 500 trading days; it ends where the free Coin Metrics archive ends.
113. The monthly layer runs from January 2020 to April 2026, the last complete month for Bitcoin, gold and the S&P 500, which gives 75 monthly changes.
114. **Timing.** Bitcoin's price for a date is fixed at midnight UTC at the end of that day, a few hours after the S&P 500 closes, which is why the worst-days test was also run on two-day returns.
115. Two-day returns can pair days starting from the first trading day or the second; both are reported in the repository, and the verdicts above hold for both except where the post says otherwise.
116. **Returns.** The worst-days and worst-months averages, their intervals, the volatility and the correlations use log returns, shown in percent.
117. The falls and the window's start-to-end changes are ordinary percentage changes.
118. For moves of a few percent the difference is small; on Bitcoin's extreme days it is not.
119. **What was fixed in advance, and what was not.** The questions, the tests and the conditions that would count as failing them were written before any data was downloaded.
120. Three things changed after the data came in, each recorded with its date in the design document: FRED's Bitcoin series was rejected, since it carries the next day's price under a stretch of dates in 2024 and 2025; gold became monthly, for the licensing reason above; and the Covid aside became weekly.
121. A code review then found a bug, a stress episode measured to the day the high was regained rather than to the low, which moved Bitcoin's 2022 fall to the figure above.
122. A few smaller choices were settled after the first results, and are marked as such.
123. **Scored conditions.** The 2020 claim needed a smaller fall and lower volatility than the S&P 500; it had neither.
124. Bitcoin is not a safe haven on daily data, with or without the Covid crash.
125. Gold is a weak safe haven on monthly data, with or without 2020.
126. Bitcoin is not a safe haven on monthly data with 2020 included, and the monthly test cannot tell without it.
127. **What this does not show.** Why any of these assets moved.
128. Whether the pattern holds outside these years, which contain three large falls.
129. Anything about other cryptocurrencies, bonds or other stock markets, including the LQ45 my draft started from.
