# LAB-AKLMT-TAU — preregistration (pick 36, uniform slot; ledger 168–170)

Written 15 Nov 2026, about 7:35 PM ET, by executor queue-pick36 (for Ace, Chad t1914/t1916). Locked by the pushed
commit that adds this file together with `common.py`, `analysis.py`, `analysis_rule.py`, `prediction.py/json`,
`pilot.py/json`, `validate.py/json` and `power_gate.json`. `analysis.py` had not been run when this was pushed.

## 1. What was read before lock (declared)
- AKLMT working paper (afrouzi.com/aklmt_overreaction.pdf, 7 Feb 2023 version): abstract, §1 opening, §3 (design,
  payments), §4.2 model list and estimation text (pp. 21–25), §5.1–5.3 (costly-processing model). The abstract states
  qualitatively that overreaction is stronger for less persistent processes, so **D < b_opt is expected**. §4.2's text
  says the implied persistence rises with ρ and is close to one for random walks. The executor did **not** open any
  table or figure file of the package, did **not** read the Figure II values, and did **not** compute any statistic
  of participant forecasts before lock. Whether D falls below κ_F·b_opt is unknown to the executor.
- AKLMT `code/FigureII.do` (row convention and the implied-persistence regression; no trimming).
- da Silveira, Sung and Woodford (2020) is known here **only as described in AKLMT footnote 26**; not read.
- Noise pilot: Experiment 2 (different participants), only bootstrap sds printed (`pilot.json`).

## 2. Theory to proxy (causal first principles)
THEORY v1.4.14 §2.2: the best linear tracker's memory is set by the drift spectrum and the read noise,
τ ∝ (N/q)^{1/α}. In this lab the reads are exact (N = 0) and the world is a known-form stationary AR(1), α = 2 above
the corner τ_E = −1/ln ρ, with **fixed innovation sd 20**, not fixed variance. Consequences, derived before lock:
1. **N11's fixed-variance τ_E slope does not apply** (variance 400/(1−ρ²) moves with ρ; τ_E ∈ {0.62, 1.09, 1.96,
   4.48, ∞} rounds has no asymptotic band; with N = 0 the τ formula degenerates to "the latest read"). The item's
   "fixed-variance τ_E slope" test is therefore **not run**; recorded as inapplicable to this design.
2. What the theory does fix here is the optimum's **memory split**: weight ρ on the latest read, the rest on a
   long-window mean. The design quantity is the forecast's loading on the latest read (AKLMT's implied persistence);
   the input is ρ (equivalently τ_E). §1 N6 causal form (v1.4.5/v1.4.7): when the input moves, the design quantity
   moves in the direction the locked optimum predicts from the measured inputs, by at least κ_F of the predicted move.
3. **Locked optimum (exactly one):** the best linear forecaster with the participant's information: a rolling OLS
   AR(1) learner on all values shown before each forecast (history included), run on the **same realized paths**
   (`prediction.py`). Implied persistence by condition 0.023, 0.214, 0.383, 0.613, 0.806, 0.999 → predicted move
   **b_opt = 0.9835** per unit ρ (FIRE with known ρ: 1.000, report-only R1). Adjustment share × reliability = 1
   (ρ set by design and constant within participant; the learner already embodies what is learnable from the data).

## 3. Primary statistic and rules (proxy "implied persistence of h = 1 lab forecasts, AKLMT Exp 1, MTurk")
D = OLS slope on ρ (six conditions, equal weight) of the per-condition pooled OLS slope of `predictiona_value` on
x_{t−1}, rounds 1–40, no trimming (AKLMT's own regression). σ = participant-bootstrap sd of D (resample participants
within condition, B = 2000, seed 20261284). z = 1.96, κ_F = ½.
- **FAIL (failed on proxy)** iff D + zσ < κ_F·b_opt = 0.4918 (takes precedence).
- **PASS (passed on proxy)** iff D − zσ > 0 and not FAIL.
- Otherwise **INCONCLUSIVE**.
Report-only (no verdict): R1 FIRE b = 1; R2 trimmed |F − x_{t−1}| > 200; R3 Exp 3 (MIT, ρ 0.2/0.6) same rule;
R4 D/b_opt with percentile CI; R5 lag-2 weight given x_{t−1}, participants vs learner; R6 per-condition values.

## 4. MV10 (tools/power_gate.py, causal form)
σ_gate = 0.1017 (pilot projection 0.0678 × 1.5, `pilot.json`); effect 0.9835; κ = ½: SNR 9.67, P(PASS | true) ≈ 1,
P(FAIL | b = 0) = 0.998, both best cases fire; **gate met** (`power_gate.json`). Synthetic validation of the rule with
the forecast column replaced (`validate.json`): optimal forecaster → PASS; slope 0.25 → FAIL; flat → FAIL.

## 5. Scope
MTurk participants in an ~18-minute novel task are **not a strongly selected system**; §1 N6's kill needs ≥ 2
strongly selected systems. Any verdict here is evidence on this proxy only and cannot change N6's status alone.
Vigilance (H8) stays OPEN. Not a test of AKLMT's model; their costly-processing model and others are rivals only in
discussion. Data: Harvard Dataverse doi:10.7910/DVN/3Q6BHC (CC0 1.0), Replication.zip sha256 efa8fd12…c9, CSVs in
`data/` with SHA256SUMS.
