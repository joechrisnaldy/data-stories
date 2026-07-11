"""Foreign-based share per nation and league concentration for WC 2026 squads.

Foreign-based = the country of the club's LEAGUE differs from the player's national
team country. Computed over players who have featured and have a known, mapped club.
National-team country names are reconciled to the club-country naming (USA, South
Korea, Czechia) before comparing."""
import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent

# Reconcile national-team country strings to the club_country naming
ALIASES = {
    "United States": "USA",
    "Korea Republic": "South Korea",
    "Czech Republic": "Czechia",
}

p = pd.read_csv(BASE / "data" / "players.csv")
cc = pd.read_csv(BASE / "club_country.csv").set_index("club").country.to_dict()

played = p[p.games.fillna(0) > 0].copy()
known = played[played.club.notna()].copy()
known["club_country"] = known.club.map(cc)

unmapped = known[known.club_country.isna()]
mapped = known[known.club_country.notna()].copy()
mapped["nation_country"] = mapped.team_country.replace(ALIASES)
mapped["abroad"] = mapped.club_country != mapped.nation_country

by_nation = (mapped.groupby("team")
             .agg(n=("player", "size"),
                  abroad=("abroad", "sum"),
                  nation_country=("nation_country", "first"))
             .reset_index())
by_nation["home"] = by_nation.n - by_nation.abroad
by_nation["foreign_share"] = (by_nation.abroad / by_nation.n).round(3)
by_nation = by_nation.sort_values("foreign_share", ascending=False).reset_index(drop=True)

league_conc = mapped.club_country.value_counts()

# For each nation, its single most common league destination (context for the essay)
top_league = (mapped.groupby("team").club_country
              .agg(lambda s: s.value_counts().idxmax()))

results = {
    "n_players_total": int(len(p)),
    "n_played": int(len(played)),
    "n_club_known": int(len(known)),
    "n_unmapped": int(len(unmapped)),
    "unmapped_clubs": sorted(unmapped.club.dropna().unique().tolist()),
    "n_nations": int(mapped.team.nunique()),
    "overall_foreign_share": round(float(mapped.abroad.mean()), 3),
    "n_fully_foreign": int((by_nation.foreign_share == 1.0).sum()),
    "by_nation": by_nation[["team", "nation_country", "n", "abroad", "home", "foreign_share"]].to_dict(orient="records"),
    "league_concentration": {k: int(v) for k, v in league_conc.items()},
    "home_based_examples": by_nation.sort_values("foreign_share").head(8)[["team", "foreign_share", "home", "n"]].to_dict(orient="records"),
    "top_league_by_nation": top_league.to_dict(),
}
(BASE / "results.json").write_text(json.dumps(results, indent=2))

print("nations:", results["n_nations"], "| players (club known):", results["n_club_known"])
print("overall foreign share:", results["overall_foreign_share"])
print("nations 100% foreign:", results["n_fully_foreign"])
print("\n--- top 10 most foreign-based ---")
print(by_nation.head(10)[["team", "n", "foreign_share"]].to_string(index=False))
print("\n--- most home-based ---")
print(by_nation.tail(8)[["team", "n", "home", "foreign_share"]].to_string(index=False))
print("\n--- top league destinations ---")
print(league_conc.head(10).to_string())
