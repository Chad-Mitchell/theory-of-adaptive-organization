# A Theory of Adaptive Organization

Private working repository for a general theory of **any adaptive organization** — cells, immune systems, ant colonies, people, firms, and cities. It is **not** a theory of everything. The bet is narrower: once acting late is costly, the same tradeoff between what a system remembers, what it predicts, and what that costs shapes efficient design at every scale. The physics is meant literally; only the cost currency changes (heat in a cell, time and money in a firm).

This repository holds the theory drafts, the theorem notes with their code checks, the tests (locked predictions, code, and results), a literature map, and reviews. It is **private** until the author says otherwise. Nothing here is a published paper.

**Author:** Chad Mitchell. Working name: GTAO (A Theory of Adaptive Organization).

## In plain words

An adaptive organization has to stay solvent in a changing world. It can hold a fact, check it, correct it, or let it fade. Doing any of those costs something, and waiting too long also costs something. From that budget, a handful of design rules follow: check on a clock matched to how fast things drift; fade what no longer pays; update beliefs by how reliable the signal is; keep cheap frozen history; recopy and recheck as copies go stale; log what was used or ignored; and spend watching effort where the shock is large relative to the buffer, but not so large that watching no longer helps.

The same tradeoff, applied at several speeds, is why memory often comes in layers. Layers that are spaced geometrically ("fractal") are predicted only when the world's drift has no single characteristic pace. That is a condition, not a slogan.

## Honest status

- **There is no new theorem yet.** Most of the individual rules are known results, restated and placed side by side. The math notes label what is already known, what is a calculation, and what fails.
- **This is a working hypothesis under test**, not a finished theory and not a finding.
- A literature sweep (`litmap/`, 14 November 2026, America/New_York; not independently reviewed) is the current basis for "what looks new" versus prior art. A sweep of this breadth cannot rule out an obscure precursor. Targeted searches are still needed before any public novelty claim.

### What looks already published

- The seven rules, taken one by one (decision theory, Kalman/Muth, append-only logs, stigmergy, inattention).
- The square-root memory-scaling law: Lee, Flack & Krakauer 2024 derived optimal memory ∝ τ_E^{1/2} with an energy cost. That is the core of the theory's "√ rule". The same √ form also appears in EOQ, menu-cost / inattention models (Reis 2006; Alvarez, Lippi & Paciello 2011), and Kalman filtering.
- The "temperature" ratio shock × √(time to fix) ÷ buffer is the inventory safety-stock factor turned upside down, and it has the same shape as Merton's distance to default.
- "Fast learns, slow remembers" and geometric spacing of levels: Brand, Holling's panarchy, Simon, and several neural-memory cascade papers, including Shankar & Howard 2013.

See `litmap/PRIOR_ART.md` and `litmap/THREATS.md` for the full accounting, including the recommended wording changes (those need the author's approval before any public text is edited).

### What still looks like this project's own contribution

Pending targeted searches, and not yet demonstrated empirically:

- the √N rule for how shared memory (for example a trail) should fade as the number of independent depositors grows;
- an explicit threshold for when a new shared level pays (T3a);
- the temperature *identity*, the fix-mechanism universality classes, and the fixed-spread sign that distinguish this from static risk indices;
- the "if and only if" for geometric (fractal) levels, and a count of levels, when drift is scale-free;
- a cost condition for acting ahead (pay for a model only if lateness loss exceeds model upkeep);
- a cross-scale, preregistered falsification program.

## Test scoreboard

Dates below are America/New_York, 14 November 2026, unless noted. "Hit / miss / inconclusive / killed" follow each test's own locked rules. Several tests have no independent review yet. Formal labels and plain-language readings sometimes come apart; both are recorded.

| Test | What it asked | Formal status | Plain reading |
|---|---|---|---|
| **BIO1** | Does memory/adaptation track environmental change at biological scales? | Global kill **not triggered**. One locked contradiction (P3a, naive immune-lifetime vs drift). Several **supports**, several **insufficient**, T4 √N **untested**. | The drift-matching *idea* holds in cells, useful immune memory, ants, and neurons, but those results are almost entirely prior art. Host antibody *lifetime* does not track pathogen drift (it tracks antigen type). The one clean neural slope is about 1, which fits a jump-world or a scale-free mechanism better than the single-timescale √ law. Literature check, not a blind experiment. |
| **COLLAPSE1** | Do memory times track world times, and do exponents collapse across substrates? | **A1 killed** (cue model for immune durability). **C2 killed** (inventory vs demand volatility). B1 passes but is non-diagnostic. The class-C square-root slope was **not** seen (firm inventory slope ≈ 0.86, not 0.5). E5a partial pass. | Timescale-collapse plots are a weak test. A change of variable to *exponents* looks more promising: code "need" decays as a power law with exponent ~0.6, close to known human-need exponents. That chain is a hypothesis, not a confirmed finding. |
| **C3** | Does bankruptcy-like project death track shock × √(time to fix) ÷ buffer, in 896 PyPI/GitHub projects? | **Inconclusive** under the prereg letter; **miss** under the analysis code as run. **Not a hit.** τ (time-to-fix) added no detectable risk once size and buffers were accounted for. | Buffers mattered (already expected). Slow fixing did not, on this operationalization, with real caveats: shock is user demand, not an exogenous hit, and τ partly measures tracker habits. |
| **C3b** | Exogenous-shock follow-up (adaptation lag to upstream breaking releases). | **Not finished.** Preregistration is locked; no results file. | In progress. |
| **F1** | Same index, second scale: ~4,100 US public firm-cohorts, 183 bankruptcies. | **Inconclusive.** No kill fired; hit criteria failed (τ-weight point estimate outside the locked band; the novel interaction p = 0.055). | All four predicted *directions* held: slow cost-adjusters failed more, and bigger buffers protected them. The "slow fixing hurts most when the shock is large relative to the buffer" interaction leaned the right way but missed significance. The main "slow costs → bankruptcy" link is already published, and exploratory checks suggest it mostly measures fixed costs and thin margins. Data fit a τ weight near 1 better than the predicted ½, the same ½-versus-1 split flagged in the literature map. No independent review yet. |
| **DRIFT1** | Is drift scale-free (the condition for geometric levels)? | Kill reading **not triggered**. No domain passed *both* the rate rule and the time rule. | City 311 request rates look mostly scale-free across categories (after a post-hoc dequantization). Wikipedia articles and firm filings have characteristic cadences. This supports T7 as a *conditional* claim, and cuts against "fractal at every scale." A person-scale arm used a private journal and is **withheld** from this repository (see `tests/DRIFT1/REDACTION.md`). |
| **ANTS1** | Code-ant test of the √N trail-fade law (T4) and drift-matched evaporation. | **Not finished.** Preregistration is locked; the run was only partly complete; there is no RESULTS.md. | Simulation only, even when finished. It cannot speak for real ants (see BIO1 P4c: no field data on decay vs colony size). |
| **DECISIVE** | Joint test of the temperature / τ term at bank, glucose, and population scales, with locked preregistrations. | **Not written up.** Preregs are locked. Each arm now has a machine-written `results.json` produced after its prereg commit. There is no RESULTS.md and no review for any arm. | **Not entered on this scoreboard.** The JSON files are in the tree for the record only (they contain the code's own labels). Do not treat those labels as hits or misses until the tests are written up and reviewed. Glucose raw recordings are clinical and are not in this repository. |

**Across the finished real-data tests of the √τ / temperature claim (C3, F1): no clean hit and no clean kill.** Directions often look right; the part that would be new has not yet cleared a locked test. BIO1 and COLLAPSE1 change how the "√ rule" and the immune "miss" should be read (exponents and scale-free memory vs a single √ timescale).

## Repository layout

```
theory/           Theorem notes, the math attack, and their code checks
tests/            Preregistered tests: predictions, code, results (raw data excluded)
litmap/           Literature map, prior-art table, threats, and DOI verification
reviews/          Hostile and independent reviews of the math and of the AI-memory toy
applications/     How this theory is applied (AI memory; Looper; ants) — no personal data
LICENSE.md        Placeholder: no license chosen yet (TODO for the author)
```

## Applications (separate from the theory)

- **AI memory**, worked out as math and a toy simulation in the public repository [`Chad-Mitchell/adaptive-memory-levels`](https://github.com/Chad-Mitchell/adaptive-memory-levels). That repo is one application. It is not this theory, and its toy results are not evidence that the theory is true.
- **Looper** is a personal-assistant application of the same hypothesis. It is developed separately. This repository does not contain Looper code, store contents, or any personal data.
- **Ants:** the field-literature check is in BIO1; a code-ant simulation of the √N claim is ANTS1 (unfinished).

## How this should be read

Do not treat locked predictions as findings, and do not treat a support that is already in the literature as a new confirmation. Formal misses and inconclusives stay on the board. Wording in public-facing documents needs the author's go, and this repository stays private until that go is given.

## License

See `LICENSE.md`. No license has been chosen.
