# The Map Used to Run the Other Way

Post 25 of the data-stories series. Live at
<https://joechrisnaldy.com/blog/the-map-used-to-run-the-other-way/>.

Average temperature against national income looks like one of the tidiest charts in economics: {{tidy_story.r:signed2}} on
log income across {{tidy_story.n:int}} countries and territories. This post argues it cannot mean what it looks like.

| Finding | Figure |
|---|---|
| Temperature against log income today | {{tidy_story.r:signed2}} (n = {{tidy_story.n:int}}) |
| Temperature against log population density in 1500, former colonies | {{heat_reversal.former_colonies.vs_density_1500.r:signed2}} (n = {{heat_reversal.former_colonies.vs_density_1500.n:int}}) |
| Temperature against log income today, former colonies | {{heat_reversal.former_colonies.vs_income_2023.r:signed2}} (n = {{heat_reversal.former_colonies.vs_income_2023.n:int}}) |
| Log density in 1500 against log income today, pooled | {{flip.density_1500|income_2023|all.r:signed2}} (n = {{flip.density_1500|income_2023|all.n:int}}) |
| ... among {{flip.density_1500|income_2023|former_colonies.n:int}} former colonies | {{flip.density_1500|income_2023|former_colonies.r:signed2}} |
| ... among the {{flip.density_1500|income_2023|never_colonised.n:int}} not on AJR's list | {{flip.density_1500|income_2023|never_colonised.r:signed2}} |
| The interaction on log density, which is the test the argument rests on | t = {{interaction.t:signed1}} (n = {{interaction.n:int}}) |

What the reversal rules out: selection aside, no explanation of the ranking between countries can rest only on an effect
that was both constant over the period and the same whether or not Europeans arrived. The post does not
claim to know what caused the flip.

## Files

| Path | What |
|---|---|
| `build_analysis.py` | Every result the post computes, into `results.json` |
| `make_charts.py` | The four charts; every computed figure on a chart reads from `results.json` |
| `gate.toml` | This post's configuration for the shared gate in `../gate/`: exemptions with reasons, the claims register, and templates for the published MDX fields |
| `docs/README.src.md`, `docs/data-README.src.md` | Templates for this file and `data/README.md`, rendered by the gate like the draft |
| `draft/*.src.md` (not committed) | The draft as written: every figure from `results.json` a `key:fmt` placeholder |
| `docs/sources.json` | Each external figure the draft binds as a `src:` key, with its stored document, hash, page and verbatim quote |
| `docs/2026-09-07-reversal-design.md` | Binding pre-registration, with amendments recorded in sections 6.1 to 6.4 |
| `docs/provenance-audit.md` | What each source actually says, opened rather than assumed |
| `docs/round2-scope.md`, `round3-scope.md`, `round4-scope.md` | What each fact-check round was scoped at |

## On the fact-checking

This post took four adversarial rounds before publication, and the honest lesson is that most of the
recurring defect classes they caught should never have needed them. Six of the seven recurring defect classes were deterministic checks being
performed by re-reading. The response is the shared gate in `../gate/`, which runs before a draft is shown
rather than after; this post's own first gate, `check.py`, was withdrawn on 2026-10-09 after an audit
showed it could be defeated, and this post was the first one ported to its replacement.
Another round, the first under that gate and run a month after publication, found a country-code
join bug and a central comparison that rests on a few cold colonies.
The one class no script can catch, trusting a variable's label over the document that defines it,
occurred twice here, the second time inside the correction for the first. See `data/README.md`.
