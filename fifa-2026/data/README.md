# Data

Not committed to this repository (download it from Kaggle).

## Source

[FIFA match, player and team dataset 2026](https://www.kaggle.com/datasets/wasiqaliyasir/fifa-match-player-and-team-dataset-2026)
by wasiqaliyasir. Three files: `matches.csv` (20 matches), `teams.csv` (40 teams, 136
columns), `players.csv` (1,035 players, 72 columns).

## Download

With the [Kaggle CLI](https://github.com/Kaggle/kaggle-api):

```bash
kaggle datasets download -d wasiqaliyasir/fifa-match-player-and-team-dataset-2026 -p .
unzip fifa-match-player-and-team-dataset-2026.zip
```

Or download from the dataset page and place `matches.csv`, `teams.csv` and `players.csv`
here.

## Note

This is an early snapshot (created 2026-06-19): about 20 matches into the tournament, and
40 of the 48 qualified teams. Squad composition is fully observed, so the "built abroad"
analysis is robust; the 20-match performance statistics are far too thin to judge anyone on
and are not used in the argument.
