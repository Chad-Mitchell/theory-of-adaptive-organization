# EVO1 results: designed-world, in-silico evolution test (final; all 96 locked runs scored)

Hypothesis tested (from `PREREG_EVO.md` §1): *The law of adaptive organization (hypothesis): strongly selected systems
minimize the cost of judgment.* Here that means: agents whose banks of leaky-integrator stores evolve under selection on
**realized** outcome costs (upkeep, speed charge, stake × realized error, death on ruin) should end at the design that
minimizes J, where J comes from the repository's closed forms (`predict_evo.py`, SHA-256 `803922a1…`). Fitness never sees J.

- Preregistration lock: commit `70fcbad`, Fri 20 Nov 2026, 1:39:31 PM ET. The hashes in `PREREG_EVO.sha256` verify, with one disclosed exception: the dependency `theory/layers_checks/stores.py` was changed on `main` by the v2.67 numerical-guard fix (PR #116) and merged here after scoring; the locked analysis gives the same result with either version (D4).
- Declared diagnostics and record entries: D1 (`cf77048`), D2 (`610e87a`), D3 (reporting only, now closed) and D4 (S arms finished; scoring unchanged). All are in `DEVIATIONS_EVO.md`.
- Scoring: the locked `analyze_evo.py` was run unchanged → `ANALYSIS_EVO.json`. Diagnostic seeds were scored with the same
  `score_seed` function → `diag/DIAG_SCORES.json`.
- Selection: Wright–Fisher, P = 300, β = 30, so EPS_BAND = 1/(βP) = 0.00111. Each world has 8 seeds (even seeds start at
  one store, odd seeds at four) and 4 null seeds (β = 0, no death).

## Verdicts (locked rules, §6–§7)

| World | What it tests | Verdict | Misses | Notes |
|---|---|---|---|---|
| PC (positive control) | Kalman–Bucy store, b* = 0.04 | **PASSED** | 0/8 | evolved b 0.0394–0.0405; J gap ≤ 5e-5 |
| W1 | one mode with a speed price | **PASSED** | 0/8 | b 0.0327–0.0343 vs 0.03356 predicted |
| W2 | two separated modes → two layers | **PASSED** | 1/7 scored | seed 4 stuck at one store (gap 3.4%); seed 2 unscored (still improving) |
| W3 | random walk → one store | **INVALID** (ruin gate) | 0/8 (raw PASSED) | final-window deaths 10.6–15.2% > 10% |
| W4 | two modes, group, common mode → 1 local + 1 shared | **FAILED** | 3/8 | seeds 0, 4, 6 (one-store starts) stayed at 1 local store, gap 8.1% |
| W4b (CT36 case) | superadditive, below the edge → 1L1S | **FAILED** | 8/8 | all seeds at 1 local store, gap 1.04% (the "no sharing" rival) |
| S031 | store noise s = 0.31 → 4 copies, slower than mode | **INCONCLUSIVE** | 2/8 (both miss A) | seeds 1 and 2 (J gap 1.24e-3 and 1.29e-3 vs band 1.11e-3); structure matched 8/8 |
| S07 | store noise s = 0.7 → 4 copies, faster than mode | **INCONCLUSIVE** | 2/8 (both miss A) | seeds 1 and 2 (J gap 1.13e-3 and 1.21e-3 vs band 1.11e-3); structure matched 8/8 |

**Secondary verdicts:**
- PC→W1 design move: Δ ln b observed −0.177 vs predicted −0.176 (tolerance 0.100). **PASSED.**
- W2 interlacing (λ₁ < b₁ < λ₂ < b₂): 7/7 scored seeds. **PASSED.**
- Store-noise threshold (S031 slower than its mode, S07 faster, ≥ 7 of 8 each): S031 8/8, S07 8/8. **PASSED.**
- S031→S07 design move: Δ ln b observed +1.470 vs predicted +1.376 (tolerance 0.311). **PASSED.**

## Controls

- **Positive control:** PASSED, so no world is INVALID on that ground.
- **Null controls (selection off):** 0 of 4 null seeds met both criteria in every world (all 8).
  For example, PC's null seeds ended at J gaps of 30–122%. The criteria discriminate.
- **Selection strength against drift (βP × gap of the nearest named rival; the gate is ≥ 10):**

  | World | Nearest rival | sNe |
  |---|---|---|
  | PC | more layers | 3000 |
  | W1 | set-at | 2448 |
  | W2 | more layers | 287 |
  | W3 | more layers (K = 4) | 3686 |
  | W4 | no sharing | 612 |
  | W4b | no sharing / one layer | 94 |
  | S031 | set-at | 40 |
  | S07 | set-at | 175 |

  Every gate (≥ 10) passes, so there is no INVALID on this ground. The tightest are S031 (40) and W4b (94).

## Rivals

- **"More layers always better":** excluded everywhere it was tested (PC, W1, W2, W3, W4, W4b). Evolution consistently
  pruned extra stores, and four-store starts collapsed to the predicted count.
- **"One layer always":** excluded in W2 (7 of 8 seeds evolved two layers with interlacing) and in W4 (5 of 8 seeds evolved
  1 local + 1 shared). It is **not** excluded in W4b: there it is exactly what evolution produced (8/8).
- **Set-at (τ = 1/λ):** excluded by the band in every world where it is defined: PC, W1 (gaps of 35% and 27%), W2 (4.25%),
  W4, W4b, and the S arms (S031 gap 0.45%, 4.0× the band, sNe 40; S07 gap 1.95%, 17.5× the band, sNe 175).
  The S031 margin is the thinnest of all.

## The S arms: what the data show (diagnostic, not scoring)

Per-seed J gap (as a multiple of the band 1.11e-3), the evolved rate against the predicted rate, and the sampled structure:

| Seed | start | S031 gap / band | S031 Δ ln b | S07 gap / band | S07 Δ ln b |
|---|---|---|---|---|---|
| 0 | low | 0.66 | −0.111 | 0.92 | +0.001 |
| 1 | high | **1.11 (miss)** | −0.132 | **1.02 (miss)** | +0.073 |
| 2 | low | **1.16 (miss)** | −0.153 | **1.09 (miss)** | 0.000 |
| 3 | high | 0.66 | −0.049 | 0.96 | −0.028 |
| 4 | low | 0.85 | −0.127 | 0.87 | +0.002 |
| 5 | high | 0.75 | −0.106 | 0.83 | −0.038 |
| 6 | low | 0.74 | +0.013 | 0.77 | −0.034 |
| 7 | high | 0.64 | −0.086 | 0.90 | −0.086 |

(Gap in absolute terms, ×10⁻³: S031 seeds 1 and 2 are 1.235 and 1.289; S07 seeds 1 and 2 are 1.128 and 1.211; the band is 1.111.)

- Misses are criterion A only. Criterion B (counted structure 1L0S, genome four copies) held in 16/16 seeds, all rates
  were inside the preregistered rate band, no seed was still improving, and the final-window death rate was 0.
- All 16 seeds are within 1.16 band widths of J's minimum. The null seeds (selection off) sit at gaps of 1.4–9.3%.
- Misses fall on seeds 1 (high start) and 2 (low start) in both arms. Both starts are represented, so the start does not explain them.
- S031: the gap tracks the rate offset. The evolved rate is a median 10.8% below the predicted rate, and gap against
  (Δ ln b)² has correlation 0.79 over the 8 seeds. The two misses are the two largest offsets (−0.13, −0.15).
  This is consistent with a small, consistent slowness of the counted store in this arm (which could come from the
  discretization offset, δ_sim +0.4% in calibration, or from how four correlated copies are counted as one).
  I did not test which. n = 8, so this is descriptive.
- S07: no such relation (median offset −1.4%; correlation 0.06). The gaps sit at 0.77–1.09 of the band whatever the offset,
  which looks like a floor near the band, not a rate error.
- Diagnosis in the order of §8 for the S arms (declared as a diagnostic): (1) optimizer/discretization: a possible
  contributor in S031 (above); (2) selection strength: the misses are 4–16% over the band edge with sNe ≥ 40 on the
  rival, so this is drift-scale scatter at the band rather than a different design; (3) cost mismatch: no sign (structure,
  threshold and move all agree with J). No rerun was made to separate these, so the diagnosis is a reading, not a result.
  A larger population (smaller band) or more seeds would settle it; neither was preregistered.

## Diagnostics (declared before running; they never replace a locked verdict)

| ID | World | Change | Pre-set bar | Outcome |
|---|---|---|---|---|
| D1a | W4b | start every agent at J's design | ≥ 3/4 stay in band → J's minimum is selection-stable | **4/4 stayed at 1L1S**, gap ≤ 1e-4 → stable |
| D1b | W4b | a new store's weight drawn from N(0, 0.3²), not 0 | ≥ 3/4 reach band → the valley is the barrier | **2/4** (seeds 0, 1 reached 1L1S; 2, 3 stayed 1L0S) → **not shown** |
| D1c | W3 | buffer ×10 | (reported beside INVALID) | 8/8 in band, deaths 5.6–8.2% (< 10%) |
| D1c-ruin | W3 | the evolved consensus as a fixed design, locked gate, 40 worlds | — | consensus death rate **0/40** in all 8 seeds; mutants whose read-weight sum misses 1 by ≥ 0.02 die 22–36% |
| D2b | W4 | a new store's weight drawn from N(0, 0.3²) (one-store starts 0, 2, 4, 6) | ≥ 3/4 reach band → the valley is the barrier | **4/4 reached 1L1S**, gap ≤ 5e-5 → shown |

**§8 diagnosis, in order:**
- **(1) Optimizer / discretization.** Calibration (§4.2, before the lock) puts δ_sim at −0.8% to −2.0% in the OU and
  random-walk worlds and +0.4% in the S arms. In W4b, the predicted 1L1S is realized-cheaper than 1L0S by 2.5% ± 0.8% per
  generation. In W4, calibration has 1L1S realized-cheaper than 1L0S by 8.2%, and the final median costs agree: 1.666–1.713 for the 1L1S seeds vs 1.772–1.816 for the 1L0S seeds. Neither miss comes from
  a mis-specified prediction.
- **(2) Selection strength.** The scatter is not null-like: every miss converged to the same rival design, and sNe ≥ 94.
- **(3) Cost mismatch.** No. D1a shows that the realized world rewards J's design and holds it once it is present.

**Causal reading.**
- **W4:** the miss is about reachability. A shared store created from nothing has read weight 0, so it costs its upkeep
  (hc, 2.4% of J*) before it can pay. D2b removes that valley and all four failing starts then reach J's design.
- **W4b:** the CT36 superadditive case, below the edge. The shared layer alone does not pay (X_S = 0.9 < 1), so 1L1S sits
  behind a fitness valley even with nonzero initial weights. D1b crossed it in only 2 of 4 seeds, below its bar.

What evolution found in W4b is what the quadrant/edge rule predicts: below the edge, no shared layer. The exact rule
predicts the global, selection-stable optimum, which evolution did not reach from the locked starts.

## What this does and does not show (honest caveat, fixed in the prereg)

An in-silico PASS shows that the theory's minimum is what selection finds when it acts on outcomes priced with these costs,
in these worlds. It does **not** show that nature obeys the hypothesis. PC, W1 and W2 are evidence that J books the costs a
lineage actually experiences and that the repository's optimizer finds the designs selection finds, including layer count,
interlacing, and how the design moves with its inputs.

The S arms (INCONCLUSIVE, 2/8 each) neither support nor contradict the hypothesis by the locked rule; their threshold
and design-move tests passed.

The two FAILs are real and stay on record. On the proxy, strongly selected agents did **not** sit at argmin J in W4 (3/8 seeds) or W4b
(8/8). The diagnostics locate the cause in **reachability** (fitness valleys created by building a layer from nothing), not
in J's books: D1a shows the minimum is stable, and D2b shows W4's valley is the barrier. As tested here, the hypothesis
needs a reachability qualifier: selection minimizes J among designs reachable by small steps. Where the cheaper design
needs two coordinated changes and neither alone pays (W4b), evolution can stall at the edge-rule design. W3's INVALID is a
gate misfire on mutants, not on the evolved design (its consensus never dies), but the locked verdict stands.

## Worries

- The ruin gate counts mutant deaths. In a random-walk world, a read-weight error grows without bound, so the gate cannot
  tell a fragile design from a fragile mutation load. This should be fixed in any successor preregistration, not here.
- A discretization offset (δ_sim −1% to −2%) is about 10× EPS_BAND. It is the same for competing designs (paired
  differences are exact), so ranking is unaffected, but absolute J is not checked at band precision.
- W4b's structure is scored on the genome, because the counting rule cannot resolve it (declared before the lock, §4.3).
- The S arms are inconclusive by the locked rule, and the evolved designs sit at the edge of the band, not far from it.
  S031's set-at rival gap is only 0.45% (sNe 40), so it separates from J's design by about four band widths.
- The preregistered band (1/(βP)) is the scale of selection-drift itself. A result whose median sits at 0.75–0.91 of
  the band (S arms) is close to the resolving limit of this design (P = 300), whichever way the verdict falls.
- The merged `stores.py` differs from the locked bytes (see D4); the effect on scoring was checked and is nil.

## Files

- `ANALYSIS_EVO.json`: the locked analysis, final (all 96 runs).
- `ANALYSIS_EVO_interim.json`: the earlier interim run.
- `logs_recovered/`: copies of the S-arm logs recovered after the interruption (see the run-record note).
- `diag/DIAG_SCORES.json` and `diag/<ID>/runs/*.json`: the diagnostics.
- `runs/*.json`: per-seed runs. The `*_snaps.npz` files are not committed.
- `logs/`: run logs.
