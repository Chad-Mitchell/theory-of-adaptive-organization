# ANTS1: the write-up nobody had written (by the physics/statistics referee)

Written Sun 15 Nov 2026, about 02:45 ET. The ANTS1 final analysis finished at 01:54:39 ET (`tests/ANTS1/watch.log`), and no RESULTS.md existed. This file is in the review folder. Nothing in `tests/ANTS1/` was edited. Sources: `tests/ANTS1/analysis_output.txt` (the official run of the committed and disclosed-fixed `analyze.py`), plus my own independent re-analysis from `results.pkl` (`rerun/ants_rerun.py`, `rerun/ants_determinism.py`, outputs `*.out`).

## Integrity
- **Lock.** PREREG.md was git-committed at d38ff12 (22:21:16 ET, 14 Nov), together with PREREG.sha256, meanfield.py and meanfield_pred.json. The ant code was committed at 6ed0500 (22:24:06), one second after the run log says the Pool started (22:24:05). The current PREREG.md matches the committed hash (38224fd1…). Caveats: the commit is local and author-dated. The PREREG body says it was written "~10:45 PM", which is 24 minutes *after* the commit time, so the self-reported times in these files are not reliable. File mtimes were all reset at about 23:20 by the VM fork and restore, so mtimes carry no information here.
- **Analysis code.** It was committed at 22:33, after the run started (disclosed, DEVIATIONS 3). The only later change is using all 1,000 bootstrap draws instead of the first 200 (DEVIATIONS 5). I diffed it and confirmed that is the only change, and it does not touch point estimates.
- **Resume after the VM fork.** All 1,201 pre-interrupt jobs in `_recovery/results_at_interrupt_1201.pkl` are bit-identical in the final `results.pkl`. Three jobs I re-ran from the committed `job()` (IND/RW, FOL/POIS, PRIV/RW) came out **bit-identical** to the stored results. The run is deterministic, so the interruption could not have biased anything.
- **Reproduction.** My own estimator code reproduces every P1/P3 exponent and the P6 count exactly.

## Scored against the locked predictions
| Pred. | Locked bar | Result | Verdict | Is it informative? |
|---|---|---|---|---|
| C0 (code check) | e* within ×1.3 of Kalman K* | 53/53 | pass | Code check by construction |
| C1 | PRIV exponent in [−0.1, 0.1] | +0.000 to +0.002 | pass | By construction |
| P1 MEAN | exponent in [0.3, 0.7] | 0.458–0.498 (5/5) | pass | **Circular.** The MEAN trail readout is an EWMA, so e* is the steady-state Kalman gain. My recomputation: e*-exponents 0.493/0.498/0.464/0.482/0.458 against the Kalman K* exponents 0.491/0.498/0.467/0.484/0.459 over the same N sets. This is C0 restated. |
| P1 MODE | same band | 0.352–0.472 (5/5) | pass | The only non-trivial part. But every MODE exponent sits **below** the Kalman value (by 0.02–0.12), and the band is wide |
| P1 count | "≥ 10/12" | 10/10 (only 5 cells × 2 readouts had ≥ 3 small-gain N; drift 1.0/obs 4 has 2) | pass on its own terms | The prereg's "12 tests" was wrong about its own design |
| P2 | large-gain exponent < 0.3; Spearman < 0 | 0.205 / 0.154; ρ = −0.593 (n = 93) | pass | Expected from Kalman saturation (K → 1) |
| P3 MEAN | MSE slope in [−0.6, −0.4] | −0.460 to −0.495 (5/5) | pass | Circular (Kalman error ∝ √(qr/N) at small gain) |
| **P3 MODE** | same | **−0.259 to −0.398 (0/5)** | **FAIL** | Real: the nonlinear, ant-like readout does **not** pool error as N^{−½} |
| P4(a) | FOL/IND e* ratio in [0.7, 1.5] in ≥ 80% | 39/41 | pass | In-model mean-field check |
| P4(b) | FOL MSE ≥ 2× IND in ≥ 90% | 54/54 (≈ 4×, as the mean field predicts) | pass | In-model; supports "fade scaling does not diagnose pooling; error scaling does" |
| P5(a) | LOCK exponent > 0.55 in ≥ 4/6 | 5/6 | pass | In-model |
| P5(b) | LOCK MSE rises at N = 256, > 2× IND, in ≥ 5/6 | 6/6 | pass | In-model |
| **P5(c)** | jump worlds, N ≥ 32: LOCK MSE > 2× IND in ≥ 80% | **36/96 (38%)** | **FAIL** | The lock-in mimic is not distinguishable from IND by error in jump worlds |
| **P6** (H77 inverted U) | interior optimum in ≥ 90% of IND curves with N ≤ 16 | **154/180 (85.6%)** | **FAIL** | All 26 failures are the **MEAN readout in POIS/HEAVY jump worlds at obs sd 4**: the optimum is e = 1 (keep no memory), and MSE at the next grid point is about 4% worse. So it is not noise. When the world relocates faster than the trail can average, no interior forgetting rate exists. |
| P7 | e* rises with drift in ≥ 90% | 75/75 | pass | Trivial for any filter (the optimal gain rises with q/r). The "21 of 21" quoted to Chad earlier is this kind of result |
| P8 | jump worlds: e* non-decreasing in N, ≥ 80% | 24/24 | pass | Weak: several series are pinned at the grid edge e = 1 |

**Tally:** 3 locked predictions fail (P3-MODE, P5(c), P6). The passes are either by construction (P1-MEAN, P3-MEAN, C0, C1, P7) or checks of the authors' own mean-field approximation of their own simulator (P4, P5(a,b)).

## Honest bottom line
ANTS1 shows that a stochastic implementation of pheromone deposits behaves like a Kalman/EWMA filter when the readout is linear. That is known mathematics, so the T4 √N fade there is guaranteed. With an ant-like nonlinear readout (MODE), the fade exponent stays inside the wide band but drifts low, and the error pooling the theory relies on **fails** (slopes −0.26 to −0.40 against −0.5). The forgetting-rate inverted U (H77) **fails** in fast jump worlds, where forgetting everything is optimal. The most useful positive result is a methodological one, and it holds inside the model: the *fade rate* does not reveal whether depositors pool independently (followers fade the same but make 4× the error). Nothing here is evidence about real ants.
