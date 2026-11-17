# Data for this post

No dataset is downloaded from a data portal. The figures come from stored copies of public pages, kept in `sources/`, which stays out of the repository. To rebuild, store each page again as `index.html` (`ms-incidents.html` for `penn-ms-incidents`) in the folder that `store_text.py` names for it, then run `python3 store_text.py`.

| Folder under `sources/` | Page |
|---|---|
| `penn-ms-incidents` | Microsoft's service health text, as republished by the University of Pennsylvania ISC: `https://mailservices.isc.upenn.edu/computing/email/penno365/alerts/ms-incidents.html` (the mirror keeps a rolling window, so a later copy may no longer hold these incidents) |
| `datareportal-2027-global-overview` | `https://datareportal.com/reports/digital-2027-global-overview-report` |
| `datareportal-2027-indonesia` | `https://datareportal.com/reports/digital-2027-indonesia` |
| `datareportal-2027-internet-use` | `https://datareportal.com/reports/digital-2027-internet-use-around-the-world` |
| news and notices | the addresses in `docs/sources.json` and the post's references |

`parse_records.py` writes `data/incidents.csv` (a row per incident: identifier, title, status, header start and end) and `data/updates.csv` (a row per update: incident, UTC time, Microsoft's text). The survey shares are read from the stored DataReportal pages by `build_analysis.py`; they are self-reported shares of internet users aged 16 and over who used each service in the past month, from GWI's survey.
