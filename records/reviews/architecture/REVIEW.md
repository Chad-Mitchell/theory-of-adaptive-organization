# REVIEW of FRACTAL_ARCHITECTURE.md and sim/ (skeptical-physicist pass)

Date: Friday 2026-11-13, about 2:50 PM ET.

**Independence: NOT independent.** This pass was done by the same executor that wrote the documents and the simulation, as a separate adversarial reread. No tool for launching a separate reviewer was available in this run.

That breaks Chad's standing rule that graders be independent and blind, with no self-grading. **An independent reviewer should redo this review before any public use.** The preregistration, deviations and raw per-seed results are all on disk, so a blind rerun is possible.

## Framing used
"I suspect this simulation was built so the favored design wins. Find the thumb on the scale, the predictions quietly moved after the fact, and every architecture claim that the math or the simulation does not support."

## Findings and fixes

| # | Finding | Severity | Fix applied |
|---|---|---|---|
| A1 | Prediction N2 said upkeep "scales with the number of drivers, not facts". T3a's own cost has a per-fact residual term that is linear in N, so only the shared-drift part scales as √N per driver | Overclaim | N2 rewritten, with the correction marked |
| A2 | The simulation gives nested the true joint model and flat an independence approximation. At high sharing the win is partly textbook | Thumb on the scale (disclosed) | Added a "what a statistician would say first" paragraph in §6; the caveat is in sim/RESULTS.md |
| A3 | Inference compute was not charged. Nested's updates took about 5x longer, and charging it could erase the half-shared advantage | Fairness | Stated in §6 and RESULTS caveats, with real wall-clock numbers (0.17 s vs 0.88 s per run) |
| A4 | The rescue rule for the middle layer (co-movement, mom_raw) was chosen after the preregistered rule failed | Post hoc | Labeled post hoc in RESULTS, DEVIATIONS (D1) and §3.4; the failed preregistered result is reported first |
| A5 | The "self-confirming" control (mom_post) did **not** fail as intended, so the simulation does not demonstrate the Test C self-confirmation mechanism. It demonstrates an identifiability failure | Interpretation | RESULTS says so explicitly; §3.4's design rule is grounded in identifiability, not in self-confirmation |
| A6 | P4's "crossover ≤ 5.83" compared a run with upkeep against a zero-upkeep bound. The added zero-upkeep run (E2b) is the fair comparison | Prereg flaw | Scored as failed as preregistered; E2b reported as a deviation (D2) |
| A7 | E5 (jump collateral) had too few jumps (about 9 per seed); E5b raised the rate, and collateral was still undetectable in aggregate MSE. The 9-15% sibling-shift figure comes from an exploratory probe, not a preregistered test | Evidence strength | Labeled exploratory everywhere it appears |
| A8 | A bug (observation noise sharing the world's random stream) was found after looking at a first run, then fixed, and everything was rerun | Process | Recorded as D0 with the size of the change (≤ about 2%) |
| A9 | Architecture §3.2 compression threshold: the bound needs the driver to be readable from its own source (THEOREMS R1) | Math assumption | Added |
| A10 | The escalation thresholds (3-4 sd), gate corroboration and level time scales are design defaults, not derived | Overclaim risk | Labeled "design defaults to calibrate" |
| A11 | Temperature: the posted prediction uses σ√τ/B, and the README's operational definition reads σ/B. This document uses σ√τ/B throughout | Consistency | Done here. **The README mismatch remains**, and changing README wording needs Chad's approval |
| A12 | Mermaid diagram | — | Parsed successfully with mermaid 11 (flowchart-v2) |
| A13 | Every figure in §6 and RESULTS re-checked against RESULTS_raw.md: 14/18/19%, 36-39%, 57%, 1.67x, 45x, 15%, 50%, 0.5% | — | All match |

## Scorecard honesty check
Of 8 preregistered predictions (counting sub-parts):
- **Clear passes:** P1, P3, P5, P6e, P7c, P8.
- **Failures:** P2 (the 20% threshold at half sharing), P4's bound clause, P6a and P6b.
- **Trivial pass:** P6c.
- **Not detected or inconclusive:** P7a and P7b.

The documents report all of these. No prediction was edited after the runs.

## What remains unresolved
1. **One synthetic world family, built to match nested's structure.** The next fair test is a world where nested's assumed structure is wrong: overlapping drivers, drivers that switch, non-Gaussian jumps.
2. **No Looper or real-data test of N1-N6.**
3. **The architecture is a design consequence, not evidence for the theory** (rule (f) in the earlier reviews).

## Verdict
The architecture follows coherently from the cost tradeoff, and its strongest concrete rules are the compression threshold, the watcher-with-escalation condition, and the identifiable middle layer. The simulation supports nested only where drift is genuinely shared, and it exposed a real fragility in learned middle layers. **Shareable as a hypothesis plus a preregistered toy result, with its failures stated, after an independent review.**
