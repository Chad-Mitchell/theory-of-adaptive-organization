# CAUSAL-KILL-MAGNITUDE — should a locked elasticity band be a causal kill? (pick 24, uniform slot)

**Queue:** CAUSAL-KILL-MAGNITUDE (from `CAUSAL_KILL_INPUTS_REVIEW.md` §5 Q4). Pick 24, UNIFORM slot (ledger 112 unaided order,
113 rule_rank, 114 claim; outcome entry at the end of this pick). 15 Nov 2026, ~5:15–5:40 PM ET.
**By:** executor queue-pick24 (for Ace, Chad t1914). Exposure: authored none of N6, §9, R2, the pick-17 author note or review,
or `tools/power_gate.py`.
**Scope:** proposal and analysis only. No THEORY.md text changes in this file's PR. The kill-condition edit it recommends is in a
separate author-only PR marked **DO NOT MERGE without separate reviewer PASS** (Chad t1916). No row or status change. Vigilance OPEN.
No prior art is credited here (none read for this pick).

## 1. Question
THEORY v1.4.6 §1 N6 (causal form) and §9 kill a locked test when the design quantity "does not move in the direction the locked
optimum predicts from the measured inputs before and after the change, after its adjustment lag". The kill is sign-only. Q4 asked
whether a right-sign move that is far too small should also be a kill, via a locked elasticity band.

## 2. First principles
Let a contrast read the log design quantity's move Δy against the measured log input change Δx, with locked elasticity b\* (e.g.
1/α for the reset-read read rate in stakes). Three things that are not theory failures shrink the measured slope b̂ toward 0 but
never flip its sign:
1. **Partial adjustment.** If the design adjusts with time constant τ, the share realised at lag L is s = 1 − e^{−L/τ} < 1.
2. **Errors in the measured input** (errors-in-variables). The OLS slope is attenuated by the reliability λ = var(Δx)/(var(Δx)+σ_x²).
3. **The other optimum.** In the one non-Gaussian world derived (two-state switching, CLAIM_MAP N16), the Bayes adaptation-time
   elasticity in switching time is 1/ℓ (≈ 0.17 at κ_N16 = 10⁻³), against ½ for the best linear tracker; the precision-effort
   elasticity in stakes is ≈ 0.55 against 2/3. Same sign, smaller size.

So E[b̂] ≈ b·s·λ. A sign-only kill is robust to all three by construction; any magnitude kill inherits all three. That is the
case for sign-only. The case against it is §3.

## 3. Finding: the sign-only kill cannot catch the main named rival, so every MV10 prereg already carries a magnitude
A design that does not move at all (fixed budget share, b = 0, N6's own named rival) "does not move in the predicted direction",
but a statistical sign rule (kill iff b̂ + z·se < 0) fires on it only at its size: **5–6%** in the Monte Carlo below, whatever
the data. To reach MV10's π = 0.8 against b = 0, a FAIL rule must exclude a positive share κ of the predicted move:
FAIL iff b̂ + z·se < κ·b\*, with P(FAIL | b = 0) = Φ(κ·SNR − z) (`tools/power_gate.py`, whose `required` default is κ = 1;
STAKES-SHIFT-CAISO used an absolute margin of a 5% rise). So in practice the causal kill is already a one-sided magnitude rule, but
κ is chosen per prereg and N6 says nothing about it. With κ = 1 and a lag at half the adjustment time, a test kills an exactly
optimal design 99.9% of the time (table, row "true s = 0.39").

## 4. Numerical checks (own code, `CAUSAL_KILL_MAGNITUDE_checks/`; seeds fixed; 4,000 reps; K = 30 contrasts, sd(Δx) = 0.5,
σ_y = 0.15, b\* = 0.5)
`band_mc.py` compares the sign rule, a symmetric 95% band |b̂ − b\*| > 1.96·se (with α̂'s se), and the one-sided κ = 0.5 rule.
`kappa_grid.py` scans κ ∈ {0, ¼, ½, 1}, naive and with the predicted move scaled by a known s·λ (best case; estimation error in
s and λ not modelled). An analytic check Φ((κb\* − b)·SNR − 1.645) matches the clean rows (e.g. b = 0.125, κ = ½: 0.738 vs MC 0.725).

Kill rate (share of reps that kill):

| scenario | sign (κ=0) | symmetric band | κ=¼ | κ=½ | κ=1 | κ=½, s·λ-adjusted | κ=1, s·λ-adjusted |
|---|---|---|---|---|---|---|---|
| theory true, clean | 0.00 | 0.06 | 0.00 | 0.00 | 0.05 | 0.00 | 0.05 |
| true, s = 0.63 (L = τ) | 0.00 | 0.85 | — | 0.00 | — | — | — |
| true, s = 0.39 (L = τ/2) | 0.00 | 1.00 | 0.00 | 0.25 | 1.00 | 0.00 | 0.05 |
| true, λ = 0.5 | 0.00 | 0.96 | 0.00 | 0.05–0.07 | 0.98 | 0.00 | 0.05 |
| true, s = 0.63 and λ = 0.5 | 0.00 | 1.00 | 0.01 | 0.59–0.60 | 1.00 | 0.00 | 0.05 |
| Bayes-optimal switching design (b = 1/ℓ = 0.166) scored against the default linear lock | 0.00 | 1.00 | 0.01 | 0.45 | 1.00 | 0.45 | 1.00 |
| false: fixed share b = 0 | 0.06 | 1.00 | 0.74 | 0.99 | 1.00 | 0.99 | 1.00 |
| false: under-responder b = ¼b\* | 0.00 | 1.00 | 0.06 | 0.71–0.73 | 1.00 | 0.73 | 1.00 |
| false: wrong sign b = −½b\* | 0.99 | 1.00 | — | 1.00 | — | — | — |
| false: b = 0 with s = 0.63, λ = 0.5 | 0.05 | 1.00 | 0.92 | 1.00 | 1.00 | 0.64 | 0.99 |

(Ranges are the two scripts' independent draws; "—" not run. Sources: `band_mc.out`, `kappa_grid.out`.)

Reading:
- **The symmetric band is unusable as a kill:** 85–100% false kills under ordinary partial adjustment or input noise.
- **The sign rule never false-kills, but has 5–6% power against b = 0**, N6's named rival.
- **A one-sided share rule with κ fixed in the prereg and the predicted move scaled by measured s and λ** keeps the false-kill rate
  at its nominal size (≤ 5% at κ = 1, ≈ 0 at κ ≤ ½) and still catches b = 0 (0.64–1.0) and a ¼-size responder (0.73 at κ = ½).
  Without the s·λ scaling, κ = ½ false-kills a true optimum 25–60% under realistic nuisances.
- **The lock matters only once there is a magnitude.** A Bayes-optimal switching design scored against N6's default linear lock is
  never killed by the sign rule, but is killed 45% at κ = ½ and 100% at κ = 1 (only 1% at κ = ¼). N6 already says the locked
  optimum is the one scored and the premise cannot excuse a miss afterwards, so this kill would be "by design". But the premise
  test that would warn a prereg to lock Bayes is jump-blind (AQN-REFEREE: 0/24 jump worlds rejected; E-A2 failed), so today a
  prereg cannot reliably know which lock is safe.

## 5. Recommendation (for a separate reviewer; draft PR, DO NOT MERGE)
1. **No symmetric elasticity band as a kill** (false kills from s and λ alone). Over-response is left to the optimality form.
2. **Make the magnitude explicit instead of hidden in each prereg's FAIL rule.** In N6's causal form and §9, the kill fires when the
   measured move **excludes a share κ of the move the locked optimum predicts** (κ a number fixed in the prereg, 0 < κ ≤ ½), where
   the predicted move is scaled by the adjustment share at the locked lag and by the input measurement's reliability, both
   measured before the data. This (i) widens the kill to catch the named rival b = 0, which the sign reading cannot; (ii) caps κ
   at ½ so that unmodelled error in s, λ and α̂ does not turn a small shortfall into a kill (κ = 1 is a test of size, which is the
   optimality form's job); (iii) keeps the wrong-sign case as a kill (any κ ≥ 0 contains it).
3. **Reviewer question on the cap:** should κ be capped lower (≤ ¼) for linear-locked tests until PREMISE-TEST-WIDEN gives a
   jump-sensitive premise test? At κ = ¼ the Bayes-switching design is killed 1% under a linear lock; at κ = ½, 45%.
4. Existing locked tests are unaffected in result: STAKES-SHIFT-CAISO ended INCONCLUSIVE (its FAIL rule used an absolute 5% margin,
   not a share κ, and had no s·λ scaling; how it would be read under the new wording is moot).
5. MV10 itself needs no change; `power_gate.py --fail-kappa` already computes the gate. A one-line FRAMEWORK note pointing MV10's κ
   at N6 belongs with the THEORY edit, after its review.

## 6. Limits
- Gaussian contrasts, OLS through the origin, K = 30, one SNR; s and λ treated as known in the adjusted rows (their estimation
  error would raise false kills somewhat; not modelled).
- Partial adjustment modelled as first-order; a design with a dead time then a jump would need s measured differently.
- The Bayes-switching row uses N16's refereed closed form for 1/ℓ (κ_N16 = 10⁻³); it is not re-derived here.

## 7. Surprise (for the queue's surprise rule)
Moderate: the sign-only causal kill, read statistically, has only its size (5–6%) as power against the theory's own named rival
(no move), so the theory's causal kill has in practice been a per-prereg magnitude rule with an unconstrained κ.
