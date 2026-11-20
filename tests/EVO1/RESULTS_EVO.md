# EVO1 results: designed-world, in-silico evolution test (interim; S031/S07 PENDING)

Hypothesis tested (from `PREREG_EVO.md` §1): *The law of adaptive organization (hypothesis): strongly selected systems
minimize the cost of judgment.* Here that means: agents whose banks of leaky-integrator stores evolve under selection on
**realized** outcome costs (upkeep, speed charge, stake × realized error, death on ruin) should end at the design that
minimizes J, where J comes from the repository's closed forms (`predict_evo.py`, SHA-256 `803922a1…`). Fitness never sees J.

- Preregistration lock: commit `70fcbad`, Fri 20 Nov 2026, 1:39:31 PM ET. The hashes in `PREREG_EVO.sha256` still verify.
- Declared diagnostics: D1 (`cf77048`), D2 (`610e87a`), D3 (reporting only). All are in `DEVIATIONS_EVO.md`.
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
| S031 | store noise s = 0.31 → 4 copies, slower than mode | **PENDING** | — | runs in progress (D3) |
| S07 | store noise s = 0.7 → 4 copies, faster than mode | **PENDING** | — | runs in progress (D3) |

**Secondary verdicts:**
- PC→W1 design move: Δ ln b observed −0.177 vs predicted −0.176 (tolerance 0.100). **PASSED.**
- W2 interlacing (λ₁ < b₁ < λ₂ < b₂): 7/7 scored seeds. **PASSED.**
- Store-noise threshold and the S031→S07 move: **PENDING.**

## Controls

- **Positive control:** PASSED, so no world is INVALID on that ground.
- **Null controls (selection off):** 0 of 4 null seeds met both criteria in every finished world (PC, W1, W2, W3, W4, W4b).
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

  Every gate passes, so there is no INVALID on this ground.

## Rivals

- **"More layers always better":** excluded everywhere it was tested (PC, W1, W2, W3, W4, W4b). Evolution consistently
  pruned extra stores, and four-store starts collapsed to the predicted count.
- **"One layer always":** excluded in W2 (7 of 8 seeds evolved two layers with interlacing) and in W4 (5 of 8 seeds evolved
  1 local + 1 shared). It is **not** excluded in W4b: there it is exactly what evolution produced (8/8).
- **Set-at (τ = 1/λ):** excluded in PC, W1 (gaps of 35% and 27%) and W2 (4.25%). The S arms, where it matters most, are
  pending.

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

The two FAILs are real and stay on record. Strongly selected agents did **not** sit at argmin J in W4 (3/8 seeds) or W4b
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
- The S arms are the largest remaining risk. S031's set-at rival gap is only 0.45% (sNe 40).

## Files

- `ANALYSIS_EVO.json`: the locked analysis (S arms will show "NO RUNS" until they finish).
- `ANALYSIS_EVO_interim.json`: the earlier interim run.
- `diag/DIAG_SCORES.json` and `diag/<ID>/runs/*.json`: the diagnostics.
- `runs/*.json`: per-seed runs. The `*_snaps.npz` files are not committed.
- `logs/`: run logs.
