# Outlook went down. Was it a break or a blocker?

A short reflection on the Microsoft 365 outage of November, built from Microsoft's own service health record and published survey figures. The post asks what a team should agree on before the next outage: a backup channel such as WhatsApp, and a list of the work that stops.

Microsoft's stated impact window ran for 23.8 hours. Besides mail, it listed 19 services as impacted in its final status, up from 4 at its first post on the multi-service incident.

## Files

| File | What it is |
|---|---|
| `parse_records.py` | reads Microsoft's stored service health record into `data/incidents.csv` and `data/updates.csv` |
| `build_analysis.py` | computes the figures the post states from Microsoft's record and the DataReportal pages into `results.json` |
| `make_charts.py` | draws the charts in `charts/` from `results.json` |
| `store_text.py` | writes the text copies of the stored pages that `docs/sources.json` pins |
| `docs/` | the design, the provenance audit, the rights notes and the sources file |

## Reproduce

From this folder, with the stored pages in `sources/` (see `data/README.md`): `python3 parse_records.py`, then `python3 build_analysis.py`, then `python3 make_charts.py`.
