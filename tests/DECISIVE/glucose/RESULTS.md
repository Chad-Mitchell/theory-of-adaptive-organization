# DECISIVE / glucose — results (organism scale)

Prereg: `PREREG.md` (sha256 38a03d01…, git commit 2b12786, 2026-11-14 22:53 ET, before any second-block episode count). Raw: `results.json`, `analysis_output.txt`. **Not independently reviewed.**

## Data

| Cohort | n | Hypo episodes (second block) | Notes |
|---|---|---|---|
| REPLACE-BG | 224 adults with T1D | 27,366 | ~114 days per block, 5-min Dexcom; decisive cohort |
| ShanghaiT1DM/T2DM | 125 recordings | 223 | ~6 days per block, 15-min Libre |
| Colas | 191 | — | used only for the collapse test |

## Preregistered results (negative binomial; 95% CI)

| Prediction | REPLACE-BG (decisive) | Shanghai (replication) |
|---|---|---|
| **P1 fixed-spread slope of hypo rate on ln τ** (theory −1; sampling/duration-corrected β\* = −0.82 REPLACE-BG, −0.65 Shanghai; static indices predict 0) | **−0.46 [−0.70, −0.23]** | −0.31 [−1.09, 0.48] |
| P2 at fixed σ, B: β_τ / β_σ / β_B | +1.49 / +4.16 / −3.81. The identity predicts β_τ = 1.08; Wald p = 0.002. ε_B = −ε_σ, p = 0.02 | +0.61 / +2.47 / −2.01 (identity not rejected; p = 0.43) |
| P3 ln τ × z > 0 | −0.16 [−0.45, 0.13] (not met; only 2 subjects have z ≥ 1.5) | +0.14 [−1.07, 1.36] |
| P5 τ adds to LBGI | −0.26 [−0.49, −0.02], LR p = 0.04, ΔAIC = 2.4 (weak yes) | no (p = 0.67) |
| Cold regime (z ≥ 1.5) β_τ\|σ,B | n = 2, not evaluable | n = 34: +16.5 [3.2, 29.8] (implausibly large; tiny n) |
| Hyper (secondary) fixed-spread slope | −0.21 [−0.43, 0.01] | −0.57 [−1.38, 0.25] |

- **P2 is not independent of P1.** σ is defined as s√(2/τ), so P2 is a reparametrization of P1.
- **P4 collapse across cohorts fails.** Offsets relative to REPLACE-BG: SH-T1DM −0.22, SH-T2DM −1.40, Colas −1.20. The prereg threshold was |offset| < 0.3.

**Verdicts under the prereg:**
- REPLACE-BG: **SIGN-RIGHT, SIZE-OFF.** At fixed spread, slower-correcting people have fewer hypo episodes, which no static index predicts. The effect is about half the theory-implied size, and the CI excludes β\*.
- Shanghai: INCONCLUSIVE (underpowered, as the prereg said).
- **Literal MATH_ATTACK rule (closer to 0 than to −1):** this **fires (KILL) for REPLACE-BG**.

## Circularity guards

| Guard | Slope [95% CI] |
|---|---|
| G1: τ from upper-half dynamics only (no hypo-tail information) | −0.40 [−0.60, −0.20]. Survives |
| G2: circular in-block estimate | −0.49 [−0.63, −0.35] |
| G3: conditional on first-block episode rate | −0.14 [−0.55, 0.27]. τ's information largely overlaps with the past episode rate |

- G2 is close to the out-of-block −0.46, so sharing the trace does not inflate the effect.
- Sensitivity, lag-1 AR(1) τ: −0.09 [−0.19, 0.01]. The effect depends on using the ACF 1/e time; glucose is not a single-time-scale process.

## Deviations
- **D1 (numerical, after outcomes):** some negative-binomial fits returned NaN SEs (singular Hessian). Added a BFGS refit, then a fallback to GLM-NB with ML α and HC0 SEs. The primary REPLACE-BG P1 estimate was unchanged by this fix.
- Collapse-model call rewritten to use the same fit function (same specification).
- REPLACE-BG and Colas were added beyond the brief and labelled as such. Figshare was blocked, so the Shanghai data came from a Zenodo re-archive of the authors' zip.

## Caveats
- Glucose excursions are driven by meals and insulin (forcing), not white-noise shocks.
- The lever arm is narrow: the SD of ln τ is 0.23 in REPLACE-BG.
- Most subjects are in the hot regime (z < 1.5), so the cold-regime predictions are essentially untested.
- Even a full hit here would be generic to single-time-scale stationary processes (stated in the prereg).
