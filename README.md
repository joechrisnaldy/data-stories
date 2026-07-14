# Data Stories

Opinionated data essays. Each one starts with a question, pulls a public dataset, analyzes it in Python, and argues a point. The writing leads with a stance; the analysis is the evidence.

Every post lives in its own folder with the full pipeline: the cleaning code, the chart code, the robustness checks, and a narrated notebook so anyone can see exactly how the numbers were produced. Raw datasets are not committed (they come from Kaggle and similar sources under their own licenses); each folder tells you how to download them.

## Posts

| # | Post | Question | Data | Read |
|---|------|----------|------|------|
| 01 | [Property Isn't the Hedge You Think](sberbank-housing/) | When a currency collapses, does property protect your wealth, or just hide the loss? | [Sberbank Russian Housing Market](https://www.kaggle.com/c/sberbank-russian-housing-market) (Kaggle) | [Live essay](https://joechrisnaldy.com/blog/property-isnt-the-hedge-you-think) · [Notebook](sberbank-housing/analysis.ipynb) |
| 02 | [A Model Can Be 86% Right and Useless](student-health-risk/) | If 86% of people share one label, what does a "good" model even mean? | [Playground Series S6E7](https://www.kaggle.com/competitions/playground-series-s6e7) (Kaggle) | [Live essay](https://joechrisnaldy.com/blog/a-model-can-be-86-percent-right-and-useless) · [Model](student-health-risk/model/) |
| 03 | [The Dataset That Already Knew the Answer](gaming-mental-health/) | What happens when a dataset's outcome is built from its own inputs? | [Gaming Addiction & Mental Health](https://www.kaggle.com/datasets/dreamtensor/gaming-addiction-and-mental-health-analysis) (Kaggle) | [Live essay](https://joechrisnaldy.com/blog/the-gaming-addiction-number-nobody-checked) · [Analysis](gaming-mental-health/) |
| 04 | [Nobody Builds a World Cup Team at Home Anymore](fifa-2026/) | Does any country still build its national team at home? | [FIFA Match, Player & Team 2026](https://www.kaggle.com/datasets/wasiqaliyasir/fifa-match-player-and-team-dataset-2026) (Kaggle) | [Live essay](https://joechrisnaldy.com/blog/nobody-builds-a-world-cup-team-at-home-anymore) · [Analysis](fifa-2026/) |
| 05 | [Everyone Says Substance. Everyone Picks Chemistry.](speed-dating/) | What do we say we want in a partner, and who do we actually pick? | [Speed Dating Experiment](https://www.kaggle.com/datasets/annavictoria/speed-dating-experiment) (Kaggle) | [Live essay](https://joechrisnaldy.com/blog/everyone-says-substance-everyone-picks-chemistry) · [Analysis](speed-dating/) |
| 06 | [The Cheapest Degree Abroad Isn't the Best Deal](international-education/) | Is the cheapest place to study abroad actually the best deal? | [Cost of International Education](https://www.kaggle.com/datasets/adilshamim8/cost-of-international-education) (Kaggle) + OECD wages and employment | [Live essay](https://joechrisnaldy.com/blog/the-cheapest-degree-abroad-isnt-the-best-deal) · [Analysis](international-education/) |
| 07 | [What Actually Moves Your Mental Health](mental-health-productivity/) | What most moves mental health, and what is that worth for productivity? | [Mental Health Prediction Dataset](https://www.kaggle.com/datasets/harpartapsingh13/mental-health-prediction-dataset) (Kaggle) + WHO figures | [Live essay](https://joechrisnaldy.com/blog/what-actually-moves-your-mental-health) · [Analysis](mental-health-productivity/) |
| 08 | [The Score You Didn't Build (and Shouldn't Trust)](nutrition/) | When a dataset hands you a "health score", is it a measurement or just a formula? | [Food Nutrition Dataset](https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset) (Kaggle) | [Live essay](https://joechrisnaldy.com/blog/the-score-you-didnt-build) · [Analysis](nutrition/) |

## How these are built

- **Python**: pandas, numpy, matplotlib. No heavy frameworks; the analysis should be readable end to end.
- **Reproducible**: each folder has a `requirements.txt`, a data-download note, and scripts you can run in order. The notebook reproduces every figure in the essay.
- **Honest**: cleaning decisions, robustness checks, and caveats are part of the story, not hidden. Where a claim comes from outside the dataset, it is cited.

Writing and sourcing conventions for the series are in [`CONVENTIONS.md`](CONVENTIONS.md).

## About

Written by Jonathan Chrisnaldy. More writing at [joechrisnaldy.com/blog](https://joechrisnaldy.com/blog).

The analysis code in this repository is released under the MIT License (see [`LICENSE`](LICENSE)). Datasets are **not** included and remain under their original providers' terms.
