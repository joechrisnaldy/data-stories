"""Profile the FIFA 2026 dataset: shapes, club coverage, distinct clubs, squad sizes.
The first look that motivated the 'built abroad' analysis."""
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
players = pd.read_csv(BASE / "data" / "players.csv")
teams = pd.read_csv(BASE / "data" / "teams.csv")
matches = pd.read_csv(BASE / "data" / "matches.csv")

print("players:", players.shape, "| teams:", teams.shape, "| matches:", matches.shape)

played = players[players.games.fillna(0) > 0]
print("players who have featured:", len(played))
print("of those, club recorded:", int(played.club.notna().sum()))
print("distinct clubs among them:", int(played.club.dropna().nunique()))
print("national teams:", int(players.team.nunique()))

# A few nations' club spread, the pattern the essay is built on
for nat in ["Morocco", "Japan", "Mexico", "Senegal"]:
    sub = played[played.team == nat]
    if len(sub):
        clubs = list(sub.club.dropna().unique())
        print(f"  {nat}: {len(sub)} featured across {len(set(clubs))} clubs -> {clubs[:8]}")
