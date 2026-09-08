# The Map Used to Run the Other Way

Post 25 of the data-stories series. Live at
<https://joechrisnaldy.com/blog/the-map-used-to-run-the-other-way/>.

Average temperature against national income is one of the tidiest charts in economics: minus 0.44 on
log income across 196 countries and territories. This post argues it cannot mean what it looks like,
because among former European colonies the same thermometer used to point the other way.

| Finding | Figure |
|---|---|
| Temperature against log income today | -0.44 (n=196) |
| Temperature against population density in 1500, former colonies | +0.29 (n=97) |
| Temperature against income today, former colonies | -0.25 (n=98) |
| Density in 1500 against income today, pooled | +0.04 (n=163) |
| ... among 94 former colonies | -0.49 |
| ... among the 69 not on AJR's list | +0.28 |
| The interaction, which is the test the argument rests on | t = -5.3 (n=163) |

What the reversal rules out: no explanation of the ranking between countries can have an effect that
was both constant over the period and the same whether or not Europeans arrived. The post does not
claim to know what caused the flip.

## Files

| Path | What |
|---|---|
| `build_analysis.py` | Every number the post quotes, into `results.json` |
| `make_charts.py` | The four charts; every drawn figure reads from `results.json` |
| `check.py`, `checks/` | The gate: ten deterministic checks that must pass before a draft is shown |
| `checks/test_gate.py` | Asserts the gate still catches real defects from this repo's history |
| `docs/2026-09-07-reversal-design.md` | Binding pre-registration, with every amendment marked in place |
| `docs/provenance-audit.md` | What each source actually says, opened rather than assumed |
| `docs/round2-scope.md`, `round3-scope.md`, `round4-scope.md` | What each fact-check round was scoped at |

## On the fact-checking

This post took four adversarial rounds, and the honest lesson is that most of what they caught should
never have needed them. Six of the seven recurring defect classes were deterministic checks being
performed by re-reading. `check.py` is the response: it runs before a draft is shown, not after.
The one class no script can catch, trusting a variable's label over the document that defines it,
shipped twice here, the second time inside the correction for the first. See `data/README.md`.
