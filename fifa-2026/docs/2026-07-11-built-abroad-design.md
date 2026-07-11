# Post 04: "Built abroad" (Indonesia's mirror)

Design doc for the fourth data story. Dataset: Kaggle
`wasiqaliyasir/fifa-match-player-and-team-dataset-2026` (real 2026 FIFA World Cup data
in FBref schema; an early snapshot). Folder: `analytics-blog/fifa-2026/`.

Date: 2026-07-11
Status: approved POV, design pending user review

## The data (profiled)

Three CSVs, created 2026-06-19 (first week of group stage):
- `matches.csv`: 20 matches, 42 cols (only a slice of the 104-match tournament).
- `teams.csv`: 40 teams, 136 cols (FBref team stats, "for" and "against" mirrors).
- `players.csv`: 1,035 players, 72 cols (full squads; 627 have featured, 556 of those
  have a `club` listed = 89% coverage; 234 distinct clubs).

Key profiling result that carries the thesis: among players who have featured, the `club`
field is well populated and recognizable, and the foreign-based pattern is already stark.
Morocco (14 clubs, all European), Japan (Feyenoord, Celtic, Bayern, Mainz, Wolfsburg),
Senegal (PSG, Monaco, Everton, West Ham) field squads employed almost entirely abroad.
Mexico, the host, is the counterexample: Toluca, Guadalajara, Cruz Azul, Tijuana, America,
mostly Liga MX.

## POV (locked with the user)

- **Angle:** Indonesia's mirror (Indonesia frames the essay; analysis is on the 40
  qualifiers, since Indonesia is not in the dataset).
- **Thesis:** "Built abroad." Nearly every 2026 qualifier fields a squad that plays its
  club football abroad, mostly in a few European leagues. Indonesia's naturalized
  Eredivisie strategy was not gaming the system; it was buying into the reality every
  modern national team already runs on. But "built abroad" says where players work, not
  how they were made, which is the difference between a pipeline and a purchase.
- **Stance:** Nuanced, hold the tension. Show empirically that building abroad is the norm
  (so Indonesia is not aberrant), and hold the honest counter-question: does it mask a weak
  domestic pipeline? The data shows the where, not the how. Soft lean, both sides respected.

## Why this thesis dodges the snapshot problem

Unlike the match statistics (a noisy 20-game slice, where per90 rates and hot starts are
mostly noise), squad *composition* is fully observed: the rosters are set regardless of how
many games have been played. So a squad-composition essay is robust on this data in a way a
performance essay would not be. The essay will say this explicitly, and will NOT lean on the
thin match stats for its argument.

## Title

Chosen: "Nobody Builds a World Cup Team at Home Anymore" (declarative, contrarian, states
the finding; the essay then complicates it).

Alternates kept on the table:
- "The World Cup Is Built Abroad. That's the Easy Part."
- "What Indonesia Saw in the World Cup It Missed"

## Section flow (the spine)

1. **Open (Indonesia).** The historic near-miss: the run to the 4th round of Asian
   qualifying on the back of naturalized Dutch-Indonesian players, and the home debate
   ("are they really ours?"). Pivot: before judging that strategy, look at who actually
   qualified.
2. **The finding.** Foreign-based share per nation across the 40. Morocco, Japan, Senegal
   near-entirely abroad; hosts and big-league nations (Mexico) the home-based exceptions.
   Indonesia's model is the norm, not the exception.
3. **Where "abroad" means Europe.** League and club-country concentration: the world's
   World Cup talent funnels through a handful of leagues.
4. **The tension (held).** The club column shows employment, not development. One label,
   two realities: grow-and-export (Morocco academies, Japan's pipeline) versus
   import-and-naturalize (Indonesia). The data cannot separate them; that is the honest
   limit of the analysis.
5. **Close (Indonesia).** Naturalization bought presence, a seat at the reality everyone
   lives in; it did not buy a pipeline. "Built abroad" is a destination, not a foundation.
   Both sides held.

## Charts (3, maybe 4)

Reuse the series dataviz palette. No fabricated "Indonesia" data chart (Indonesia is not in
the dataset), same honesty rule as Post 03.
1. Foreign-based share ranked across the 40 qualifiers, with Indonesia's would-be position
   annotated as an external note (not a data point).
2. League or club-country concentration: where the world's World Cup players are employed.
3. The home-based counterexamples: hosts and big-league nations that keep players home.
4. (Optional) A clean visual for the tension if one emerges (for example home-league share
   distribution); dropped if it does not earn its place.

## Method

- Build a club-to-country lookup for the 234 distinct clubs (recognizable names; mapped
  manually or with a helper, spot-checked).
- Foreign-based = club country not equal to the national-team country.
- Per-nation foreign-based share computed over players with a known club (556 of the 627
  who have featured); coverage noted.
- League concentration = counts of players by club country / league.

## Honesty guardrails

- `club` is where a player is employed now, not where he was developed; the analysis cannot
  distinguish an export pipeline from an import/naturalization. State this plainly.
- Early snapshot; do not lean on the 20-match performance stats for the argument.
- Indonesia is framing, not in the dataset; make no data claim about Indonesia.
- No causal claim that building abroad causes qualifying.
- No long dashes; APA 7 references for every external fact.

## References (APA 7, to pin at write time)

External facts to verify against sources before publishing:
- Indonesia's 2026 World Cup qualifying run (reached the AFC 4th round, a national first)
  and the naturalization program (Dutch-Indonesian, Eredivisie-based players; coaching
  change to Patrick Kluivert in early 2026). Verify specifics.
- A football labor-migration source for the "built abroad" context (for example the CIES
  Football Observatory expatriate-players reports).
- FIFA eligibility / nationality rules context if cited.

If a figure cannot be verified cleanly against its source at write time, it gets dropped or
softened; no number ships unsourced.
