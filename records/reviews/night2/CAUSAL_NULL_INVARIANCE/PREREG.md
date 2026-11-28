# CAUSAL-NULL-INVARIANCE — locked in-model test (pick 35, ledger 165 claim)

Locked before any outcome-arm learner was run. Author: executor queue-pick35 (for Ace, Chad t1914/t1916). In-model only; says
nothing about real organizations. Vigilance (H8) stays OPEN. Nothing posted or sent.

## Question (causal first principles)
Does a tracker that is *selected by payoff* (never told the world model) change its adaptation time t_A, under a change in the
world that leaves the best linear (Kalman) tracker's memory time fixed, by the amount the Bayes-locked optimum predicts?
The change is q-fixed: λ ×2, μ² ×½, N fixed (κ = λN/μ² ×4). Pre-lock derivation (`derive.py`, `derive.json`, own Monte Carlo,
grid Δ = 0.01, 'switch' law): the Bayes (discrete Wonham) optimum's t_A goes 0.6698 ± 0.0040 → 0.9509 ± 0.0047
(Δln = **+0.3504**, se 0.0078); the Kalman (MSE-best linear) tracker's zero-crossing time goes 1.6468 → 1.5339 (Δln = −0.0711).
Kalman memory time 1/β moves −0.4%.

## Design
- World: telegraph ±μ, flip rate λ each way, white noise N = 1, sampled Δ = 0.01. Arm A: λ = 0.01, μ = 2 (κ = 0.0025).
  Arm B: λ = 0.02, μ = √2 (κ = 0.01). q = 4λμ² = 0.16 in both.
- Learner (`learner.py`, `learner_mse`): candidate grid of the family F(pp, g) (13 × 13 nonlinear members, pp = p·{1/8..8},
  g = g_Bayes·{1/16..4}) plus 25 linear members (poles around the Kalman pole, ×{1/8..8} on 1 − pole). Payoff: mean squared
  error of the best-scaled estimate (tanh(L/2) or L, scale fitted by least squares on the experience). Each learner sees its
  own experience record of E = 20 expected switches and keeps the candidate with the lowest experience MSE. Its t_A (mean
  samples × Δ from the last pre-switch sample to the first sample whose sign matches the new state) is measured on a fresh
  test record of 200 expected switches.
- R = 24 independent learners per arm; seeds A 1000–1023, B 2000–2023 (test records seed + 10,000,000).
- Code: `core.py`, `learner.py`, `run_test.py` as committed in the lock commit.

## Locked rule (THEORY v1.4.13 §1 N6 causal form, κ_F = ½; Bayes-locked optimum)
D = mean ln t_A(B) − mean ln t_A(A); σ = √(s_A²/24 + s_B²/24) (sample sds of ln t_A); z = 1.96; predicted move +0.3504
(adjustment share 1 and reliability 1: inputs known exactly in-model).
- **FAILED** iff D + zσ < ½ · 0.3504 = 0.1752.
- **PASSED** iff D − zσ > 0 and not FAILED.
- Else **INCONCLUSIVE**.
Label: "passed/failed on proxy 'MSE-payoff-selected learners (F(pp,g) + linear family; E = 20 switches), zero-crossing t_A
on Δ = 0.01 grid'".
Descriptive (no verdict): share of learners choosing a linear member; D against the Kalman rival's −0.0711.

## MV10 (`tools/power_gate.py contrast`, `mv10_mse.json`)
Noise from a pilot at a point that is **not** an outcome arm (P: λ = 0.01√2, μ² = 4/√2, κ = 0.005, q fixed; 8 learners;
`pilot2.py`, `pilot2.json`): sd of ln t_A = 0.0968 → σ = 0.0968·√(2/24) = 0.0279. Effect 0.3504, κ_F = 0.5, noise df 7:
SNR 12.5; P(PASS | Bayes true) ≈ 1.0, P(FAIL | b = 0) ≈ 1.0; both best cases fire. **Gate met.** The gate's null is b = 0; the
Kalman rival (−0.0711) is further from the kill line.

## Pre-lock finding recorded before the outcome (not a verdict of this test): the 0–1 (decision) payoff version cannot meet MV10
`pilot.py`, `pilot.json`: the best *linear* tracker for the same 0–1 payoff (accuracy; pole optimized, 17-point grid,
2·10⁷ samples) has t_A 0.7008 (A) → 0.9308 (B), Δln = +0.2838, i.e. 81% of the Bayes move, and error rate 0.0101 vs Bayes
0.0087 (A), 0.0301 vs 0.0270 (B). With κ_F ≤ ½ the causal kill fires only below half the predicted move, so a Bayes-locked
causal test cannot FAIL a world whose tracker is the 0–1-best linear one at any sample size: MV10's FAIL leg is structurally
unreachable for that rival. The −29.5% / 0% Bayes-vs-linear contrast of the CAUSAL-KILL-INPUTS review is a contrast between
Bayes and the **MSE**-best linear tracker; the loss is part of the locked optimum.
