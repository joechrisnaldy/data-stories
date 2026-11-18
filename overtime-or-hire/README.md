# Two 12-hour days or three 8-hour days?

A test of whether two people on 60-hour weeks give a company what three people on 40-hour weeks give: the same 120 hours, but not the same output or cost. Sleep and sports, exercise and recreation by usual weekly hours come from the American Time Use Survey; output against hours from Pencavel's estimates for British munition workers, used as an assumption; costs from the Bureau of Labor Statistics and the US overtime rule; and the same week under Indonesia's labour law.

On Pencavel's curve, the long-hours team delivers about 111 productive hours a week against 120. Where overtime is owed, it costs $58.71 per productive hour against $54.00. Where pay is the same at any hours, it costs less on paper; the teams cost the same per productive hour when each long-hours worker carries about $847 a week of costs the model leaves out.

## Files

| File | What it is |
|---|---|
| `profile_data.py` | reads the survey file (frozen by its recorded hash), sets the weights and holds the sample rule; run alone, it prints the file's checks |
| `model.py` | the output curve, the cost of each team and a week under each overtime rule |
| `test_model.py` | the model's tests: `python3 -m unittest test_model` |
| `build_analysis.py` | computes the figures the post states into `results.json`, reading each external input from `docs/sources.json` |
| `make_charts.py` | draws the charts in `charts/` from `results.json` |
| `store_text.py` | writes the text copies of the stored documents that `docs/sources.json` pins |
| `docs/` | the design, the provenance audit, the rights notes and the sources file |

## Reproduce

From this folder, with the survey file in `data/` and the stored documents in `sources/` (see `data/README.md`): `python3 store_text.py`, then `python3 build_analysis.py`, then `python3 make_charts.py`.
