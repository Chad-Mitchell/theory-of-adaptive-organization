# LAB-AKLMT-TAU — results (pick 36, uniform slot; ledger 168–170 + outcome)

15 Nov 2026, about 7:35 PM ET. Executor queue-pick36 (for Ace, Chad t1914/t1916). Lock: commit `1b47884`
(pushed 7:33 PM ET, before any participant-forecast statistic; the only later prereg change is a time-stamp fix).
Not refereed.

## Verdict
**Passed on proxy "implied persistence of h = 1 lab forecasts, AKLMT Exp 1 (MTurk)", at the boundary.**
D = 0.518 (σ_boot 0.048; 95% [0.424, 0.612]) against the locked optimum's move b_opt = 0.984 per unit ρ and the
κ_F = ½ kill threshold 0.492. D − zσ > 0 (direction established) and D + zσ = 0.612 > 0.492 (no kill), so the locked
rule reads PASS. Participants move **53% of the optimum's move** (D/b_opt 0.527, percentile CI [0.436, 0.626]): the
point estimate sits 0.03 above the kill line, and the prediction itself (0.98) is missed by ~10 SE. Read it as
"the response to ρ is not excluded from half of the optimum's", not as "near-optimal".

Scope: MTurk participants in a ~18-minute novel task are not a strongly selected system, so this cannot move N6
(needs ≥ 2 strongly selected systems). Vigilance (H8) stays OPEN. N11's fixed-variance τ_E slope was **not tested**:
inapplicable to this design (innovation sd fixed, so variance moves with ρ; exact reads, N = 0; τ_E 0.6–4.5 rounds,
no asymptotic band). PREREG §2.

## Numbers (`results.json`)
| ρ | 0 | 0.2 | 0.4 | 0.6 | 0.8 | 1 |
|---|---|---|---|---|---|---|
| participants' implied persistence | 0.453 | 0.625 | 0.770 | 0.846 | 0.913 | 0.991 |
| feasible OLS learner (locked optimum) | 0.023 | 0.214 | 0.383 | 0.613 | 0.806 | 0.999 |

The participant row reproduces AKLMT's published Figure II panel B labels (0.45, 0.62, 0.77, 0.85, 0.91, 0.99),
read after the analysis ran.

Report-only rows: R1 FIRE b = 1: PASS (threshold 0.50). R2 trimming |F − x_{t−1}| > 200: drops 0 rows, same.
R3 Exp 3 (MIT EECS, ρ 0.2 / 0.6, n = 204): D = 0.629 ± 0.094 vs b_opt 1.027: PASS. R5 lag weights (regression on
x_{t−1}, x_{t−2}): participants put **negative** weight on x_{t−2} at ρ ≥ 0.2 (−0.04 to −0.17) and weight > 1 on
x_{t−1} at ρ ≥ 0.8 (1.03, 1.16), i.e. they extrapolate; the learner's x_{t−2} weight is +0.04 throughout.

## Independent numerical checks (`independent_check.py`, own code, no shared imports)
C1 stacked interaction regression with participant-clustered covariance: D 0.5182, se 0.0469, PASS. C2 recursive
least squares learner: b_opt 0.9835 (same). C3 participant jackknife: se 0.0485, PASS. Pilot σ_gate (0.102) was
conservative against the realized 0.048. Synthetic validation of the rule (`validate.json`) passed before lock.

## Surprises (rule 4)
1. **Strong (kill-rule leniency):** a system whose level at ρ = 0 is 0.45 against an optimum of 0.02, and whose
   response is ~10 SE below the predicted move, passes the N6 causal form at κ_F = ½. The causal clause alone
   tests direction and a half-size floor, not optimality. New item CAUSAL-KAPPA-LENIENCY.
2. **Weak (post hoc):** trend extrapolation (negative lag-2 weights). The optimum never uses a negative weight on
   older reads; the participants' memory is shorter than the optimum's and signed differently. New item
   LAB-AKLMT-EXTRAPOLATION.
3. **Weak (post hoc):** the response is concave in ρ (slope ≈ 0.65 over 0–0.6, ≈ 0.36 over 0.6–1), so the span
   chosen for a causal contrast changes the verdict. New item LAB-AKLMT-CURVATURE.
4. The item's original target (τ_E slope / τ ∝ (N/q)^{1/α}) needs read noise: new item LAB-NOISY-READ-TAU.

## Prior art (read)
AKLMT (2023) itself: they document overreaction falling with ρ and fit a costly-processing model; this test adds
only the N6 magnitude reading against a feasible-information optimum. da Silveira, Sung and Woodford (2020) known
only via AKLMT footnote 26 (not read; no claim made about it).
