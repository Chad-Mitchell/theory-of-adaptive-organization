# DISCRETE-TA-N16-REVIEW: independent review of PR #53 (N16 sampled-grid scope)

Sunday 15 November 2026, about 5:42–6:02 PM ET (America/New_York). Grok Bot independent reviewer executor for Chad Mitchell, via Ace (Chad t1914/t1916). Private; nothing posted or sent. This reviewer authored none of DISCRETE-TA, `tools/discrete_ta.py`, PR #53, N16, the TELEGRAPH reports or AQN_REFEREE. Queue: out-of-cycle and unscored (continuation of the pick-23 author PR under the t1916 independent-review rule); no rank or pick logged; ledger 133. All results are in-model (mathematics and numerics); no field claim. Vigilance stays OPEN (untouched). Own code in `DISCRETE_TA_N16_REVIEW_checks/`, run at nice 19. It imports nothing from `tools/discrete_ta.py` or the author's `checks/`. The author's tool was run once only to compare the continuous T (E2).

## Verdict: **PASS-WITH-FIXES**

The core is right. The linear closed form, the threshold tables, the quiet/switch definitions and the referee-Q1 answer all reproduce with independent code. One mathematical claim in the derivation is wrong: the grid coefficient is **not** independent of κ. The fixes below make the THEORY text say only what holds. With them applied, PR #53 is merged as THEORY v1.4.9 (CLAIM_MAP v2.26 note, kept and ordered before v2.27).

## Checks

**1. Linear tracker closed form (`lin.py`, `lin.out`).** The steady-state Riccati iteration matches cosh(βΔ) = cosh(aΔ) + ρ sinh(aΔ), with a = 2λ and ρ = μ²Δ/N, to 12–14 digits in four cases. Sympy series: β² = a² + b − b²Δ²/12 + O(Δ⁴) with b = 2aμ²/N. So β_c/β − 1 = b²Δ²/(24β_c²) = (1 − a²τ_c²)²/(24r²) exactly at this order. **Confirmed.** Report erratum: the report's first form, with /(24β_c⁴), is dimensionally wrong (typo); the r-form is right. In the slow world (a → 0), the exact ratio is 1.0102 at r = 2.0, and the 1/5/10% thresholds are r = 2.02/0.876/0.595. So "within 1% at ≥ 2 samples" is very slightly false. Fixed to "within about 1% … (1.0% at 2.0)".

**2. Grid overshoot term (`bayes.py`, `gscan*.py`, `extrap.py`).** This is an independent Nyström solver: Gauss–Legendre panels, the exact discrete HMM filter, the stationary start law as a null vector, and expected hitting steps from the integral equation. It converges to 10 digits under h- and p-refinement. It matches the author's lattice at 4 cells to ≤ 0.01% (`cells.out`), which in turn matches the author's independent MC. Continuous T(κ) comes from the reviewer's own quadrature and agrees with the author's to 1e-6.
- **BGK constant read in the source**: Broadie, Glasserman & Kou 1997, *Math. Finance* 7(4):325–348 (Columbia Business School author PDF, `bgk_mf.pdf`). Theorem 1.1 states β = −ζ(½)/√(2π) ≈ 0.5826. Lemma 4.2 states that β is the mean of the limiting overshoot distribution B_R (via Siegmund 1985 Thm 10.55 and Chernoff 1965, which were not read). Numerically −ζ(½)/√(2π) = 0.5825972. **Credit confirmed** as stated: Siegmund's constant, as stated by BGK.
- **The κ → 0 limit is confirmed**: at κ = 10⁻⁴, g(ρ) = (t_grid − T)/√(ρθ) extrapolates to 0.5822 (C₁ = 0.5826), with slope about 0.25√ρ, as the report says.
- **Error: the coefficient depends on κ.** Extrapolated limits are c(10⁻²) = 0.5673 and c(3·10⁻²) = 0.5466, which are 2.6% and 6.2% below C₁. Fits on 4, 5 and 6 points agree to 1e-4, and ρ goes down to 6.25·10⁻⁴. The report's step "E∫_{τ_c}^{τ_d} 2λ sinh L ds = O(λΔ^{3/2}) because L stays near 0" is the failure. Between the two crossings the path makes O(1) upward excursions, so the term is O(λ√Δ), times a log. A barrier-shift heuristic (sampled crossing ≈ continuous crossing of −C₁σ_L√Δ) gives C₁·2g(0) = C₁∫₀^∞e^{−z−κ(cosh z−1)}dz = 0.5702 at κ = 10⁻² and 0.5543 at 3·10⁻². That accounts for about 80% of the deficit; the rest is unexplained (DISCRETE-TA-SECOND-ORDER). Consequences: the "0.58" applies only as κ → 0. The grid term's λ elasticity is small but not zero, and its N and μ elasticities are "about" ½ and −1.

**3. Validity thresholds (`thr.py`, `thr.out`).** Smallest r = plug-in/Δ at which the quiet-law grid value is within the band, found by root-finding on the exact solver:

| | κ = 10⁻⁶ | 10⁻³ | 10⁻² |
|---|---|---|---|
| quiet 10% (report) | 9.6 (10) | 16.2 (17) | 26.8 (27) |
| quiet 5% (report) | 30.4 (30) | 56.2 (57) | 119.8 (122) |
| switch 10% (report) | 9.6 (10) | 14.8 (15) | 15.1 (16) |
| switch 5% (report) | 30.4 (30) | 46.8 (47) | 38.7 (39) |

**Reproduced** within the report's log-interpolation. The thresholds are exact-lattice values, so E2's κ-dependence does not affect them. One causal gap: they assume time is counted from the last pre-switch sample. Timed from a switch placed uniformly within the interval (−Δ/2), the quiet-law 10% thresholds become 5.2 (κ = 10⁻³) and 15.6 (10⁻²), the 5% thresholds become 35.7 and 94.9, and the switch-law 10% thresholds become 4.1 and 6.8. The clock origin must therefore be stated. Fixed.

**4. The 4.5% residual at κ = 10⁻², ρ = 0.0025.** The finest-grid value is g = 0.5803 (10-digit converged), not 0.568. The 4.5% figure was a lattice-extrapolation artifact. However, the underlying suspicion was right: the ρ → 0 limit at κ = 10⁻² is 0.567, 2.6% below C₁. **Ruling: the "0.58" wording must be hedged.** It now reads: c → −ζ(½)/√(2π) ≈ 0.58 as κ → 0, lower by O(κ ln 1/κ), about 0.57 at κ = 10⁻² (numerical). Because N16 itself is a κ ≪ 1 asymptote, this narrows the statement without contradicting it.

**5. Definition: quiet law vs switch law (`cont.out`).** Own quadrature gives quiet/plug-in = 1.17821, 1.03573, 1.00981, 1.00079, 1.00007 and switch/plug-in = 1.02309, 0.96537, 0.97774, 0.99578, 0.99940 at κ = 0.1, 0.03, 10⁻², 10⁻³, 10⁻⁴, matching the report. The quiet−switch gap is 0.501% of the plug-in at κ = 10⁻³ (O(κ ln 1/κ): 0.69%). So "under 0.5%" is marginally false and is fixed to "0.5% or less". **Ruling: name both laws; do not lock the quiet one.** Causal reason: the formula's derivation used the quiet law, but the commonest field estimator, averaging over all switches of a record, measures the switch law. Locking the quiet law in THEORY would make the text silently wrong by 3% at κ = 10⁻² and 7% at 3·10⁻² for that estimator. The narrowest true text says which law the formula was derived for, states the size of the gap, and leaves the choice to the prereg, as the PR does.

**6. Goalposts.** No locked prereg's goalposts move. The only locked files that touch N16's t_A are `measurement/estimators/PREREG.md` (lock 3595c48; a method lock whose acceptance rule is estimator bias against synthetic truth, unchanged) and `reviews/night2/TELEGRAPH_LINEAR_PREMISE/PREREG.md` (in-model, done). No locked test (`tests/*/PREREG.md`, `PREDICTIONS.md`, `prereg/*`) reads a sampled t_A against the plug-in. STAKES-SHIFT-CAISO, F1, COLLAPSE1 and BIO1 mention switching but not t_A. CAUSAL-NULL-INVARIANCE is queued, not locked; its note about the grid term (+1.2% of t_A at 20 samples) should use c(κ), a < 3% change in that correction at κ ≤ 10⁻².

## Fixes applied (narrow)
- F1: grid coefficient c with c → −ζ(½)/√(2π) ≈ 0.58 as κ → 0; about 0.57 at κ = 10⁻² (THEORY, CLAIM_MAP N16 row and v2.26 note).
- F2: clock origin "time counted from the last sample before the switch", plus a sentence that timing from a switch inside the interval subtracts about Δ/2 and changes the thresholds.
- F3: thresholds labelled quiet law; switch-law thresholds (10–16, 30–47) added.
- F4: "under 0.5%" → "0.5% or less" at κ ≤ 10⁻³; "3% at κ = 10⁻²" added.
- F5: linear "within 1% at ≥ 2 samples" → "within about 1% … at ≥ 2 samples per memory time (1.0% at 2.0)".
- F6: BGK credit in the passage itself; grid elasticities "about" (½, −1).
- F7: dated, bracketed reviewer errata E1–E4 in `reviews/night2/DISCRETE_TA/REPORT.md` (original text kept).
- Version: THEORY v1.4.9 (v1.4.8 taken by PR #51); CLAIM_MAP v2.26 note kept, ordered before v2.27.

## New and updated items
- DISCRETE-TA-SECOND-ORDER (updated): derive c(κ) (barrier-shift heuristic explains about 80% of the deficit) and c₂; the 4.5% residual is resolved as a lattice artifact.
- No new items.

## Limits
In-model only. The symmetric two-state, per-sample HMM with switches only between samples (integrate-and-dump stays DISCRETE-TA-INTEGRATED). c(κ) is extrapolated numerically, not derived. Siegmund 1985 and Chernoff 1965 were not read; only BGK was.
