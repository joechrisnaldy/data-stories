# Data Stories

Opinionated data essays. Each one starts with a question, pulls a public dataset, analyzes it in Python, and argues a point. The writing leads with a stance; the analysis is the evidence.

Every post lives in its own folder with the full pipeline: the cleaning code, the chart code, the robustness checks, and a narrated notebook so anyone can see exactly how the numbers were produced. Raw datasets are not committed (they come from Kaggle and similar sources under their own licenses); each folder tells you how to download them.

## Posts

| # | Post | Question | Data | Read |
|---|------|----------|------|------|
| 01 | [Property Isn't the Hedge You Think](sberbank-housing/) | When a currency collapses, does property protect your wealth, or just hide the loss? | [Sberbank Russian Housing Market](https://www.kaggle.com/c/sberbank-russian-housing-market) (Kaggle) | [Live essay](https://joechrisnaldy.app/blog/property-isnt-the-hedge-you-think) · [Notebook](sberbank-housing/analysis.ipynb) |
| 02 | [A Model Can Be 86% Right and Useless](student-health-risk/) | If 86% of people share one label, what does a "good" model even mean? | [Playground Series S6E7](https://www.kaggle.com/competitions/playground-series-s6e7) (Kaggle) | [Live essay](https://joechrisnaldy.app/blog/a-model-can-be-86-percent-right-and-useless) · [Model](student-health-risk/model/) |
| 03 | [The Dataset That Already Knew the Answer](gaming-mental-health/) | What happens when a dataset's outcome is built from its own inputs? | [Gaming Addiction & Mental Health](https://www.kaggle.com/datasets/dreamtensor/gaming-addiction-and-mental-health-analysis) (Kaggle) | Essay forthcoming · [Analysis](gaming-mental-health/) |

## How these are built

- **Python**: pandas, numpy, matplotlib. No heavy frameworks; the analysis should be readable end to end.
- **Reproducible**: each folder has a `requirements.txt`, a data-download note, and scripts you can run in order. The notebook reproduces every figure in the essay.
- **Honest**: cleaning decisions, robustness checks, and caveats are part of the story, not hidden. Where a claim comes from outside the dataset, it is cited.

Writing and sourcing conventions for the series are in [`CONVENTIONS.md`](CONVENTIONS.md).

## About

Written by Jonathan Chrisnaldy. More writing at [joechrisnaldy.app/blog](https://joechrisnaldy.app/blog).

The analysis code in this repository is released under the MIT License (see [`LICENSE`](LICENSE)). Datasets are **not** included and remain under their original providers' terms.
