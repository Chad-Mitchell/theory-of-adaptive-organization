# STORE-COEF-REVIEW — independent review of PR #51 (THEORY N4 and §2.2 store-row constant)

**Verdict: PASS-WITH-FIXES.** Merged as THEORY v1.4.8 after the fixes below.

- Queue: STORE-COEF-REVIEW, pick 27 (unaided slot, protocol v2); ledger 125 (unaided order), 126 (rule_rank), 128 (claim), outcome entry after this report. Sunday 15 November 2026, about 5:40–6:15 PM ET.
- Reviewer: executor queue-pick27 (for Ace, Chad t1914/t1916). I wrote none of pick 26, PR #51, `SPECTRUM_MAP/checks/c3_layers.py`, `SPECTRUM_MAP_FIXES_checks/` or the referee's R4.
- Own code: `STORE_COEF_REVIEW_checks/` (`coef.py`, `cont2.py`, `c_limit.py` and their `.out`/`.json`). It imports nothing from the repo. I re-implemented the model class from its written definition (SPECTRUM_MAP §1, Prop. 4) and did not run or read the author's checks.
- Everything here is **in-model**. No data and no outcomes are involved.

## 1. What PR #51 changes

N4 (§1) and the §2.2 store row change from "one store iff ψ·0.14(α−2)² ≲ 1" to "ψ·c(α−2)², c ≈ 0.03–0.2 depending on span and store model (in-model)". The changelog says the knife-edge bullet ("α within ±0.05 of 2 already needs two stores at ψ ≈ 10⁴") is unchanged.

## 2. First principles: why (α−2)², and why c is not a world constant

- **Why the excess is quadratic.** At α = 2 the discrete world S = q(4 sin²(θ/2) + w²)^(−1) is exactly AR(1). With white noise added, the Wiener filter is ARMA(1,1): one exponential store plus an instantaneous tap. So the one-store family contains the optimum, and the best one-store excess ε₁(α) ≥ 0 is zero at α = 2. If ε₁ is smooth in α, its first derivative there is zero and the leading term is c(α−2)². That is generic and does not depend on the model.
- **What c measures.** c is the curvature of the misfit between the power-law optimal kernel and the best "one pole plus whatever is free" kernel. That misfit sits in two places:
  - **Short lags (≲ a few τ_c).** Free short-lag taps absorb this part.
  - **The long tail.** The optimal weight falls as τ^(−(1+α/2)) rather than exponentially. A short span cuts this part off.
- **So c depends on how a store is defined and on the span, not on the world alone.** The numbers in §3 show exactly this.

## 3. Own re-derivation

**Method.**
- Composite Gauss–Legendre quadrature: a linear panel on [0, 10⁻²·w_min] plus 60 log panels up to π.
- Store weights by QR least squares on the residual integrand, which avoids the c − w·b cancellation that broke the author's first pass.
- K = 1 rate: a dense 161-point grid in log λ, then bounded Brent to 10⁻⁷.
- K = 2: grid plus Nelder–Mead multistart.
- Wiener floor by Kolmogorov–Szegő.

**Validation.**
- At α = 2 the Wiener floor matches an exact Kalman Riccati to 10⁻¹² relative (span 10, 10², 10⁴). The one-store excess there is |ε₁| < 2×10⁻¹⁵: one store is exact.
- Quadrature converges: ε₁ = 2.00473×10⁻⁴ at 30, 60 and 120 panels (α 1.95, span 10⁴).

**Model:** c3 class (four free taps, τ_c = 4, N = τ_c^α). c = ε₁/(α−2)²:

| span R | α 1.8 | 1.9 | 1.95 | 1.98 | 2.02 | 2.05 | 2.1 | 2.2 | two-store ψ at α 1.95 / 2.05 |
|---|---|---|---|---|---|---|---|---|---|
| 10 | 0.0053 | 0.0063 | 0.0069 | 0.0073 | 0.0078 | 0.0081 | 0.0088 | 0.0102 | 5.8×10⁴ / 5.0×10⁴ |
| 10² | 0.0334 | 0.0393 | 0.0425 | 0.0444 | 0.0470 | 0.0490 | 0.0524 | 0.0595 | 9.8×10³ / 8.5×10³ |
| 10³ | 0.0574 | 0.0662 | 0.0709 | 0.0737 | 0.0776 | 0.0806 | 0.0858 | 0.0967 | 6.1×10³ / 5.3×10³ |
| 10⁴ | 0.0659 | 0.0752 | 0.0802 | 0.0833 | 0.0875 | 0.0908 | 0.0965 | 0.1088 | 5.5×10³ / 4.9×10³ |
| 10⁵ | 0.0680 | 0.0772 | 0.0822 | 0.0853 | 0.0896 | 0.0929 | 0.0988 | 0.1117 | 5.5×10³ / 4.8×10³ |

The two-store threshold is 1/(ε₁ − ε₂), with ε₂ the polished two-store excess.

**Store-model dependence** (span 10³, α 1.9 / 2.1; `coef_model.out`):

| free taps | τ_c = 2 | τ_c = 4 | τ_c = 16 |
|---|---|---|---|
| 0 | 0.145 / 0.158 | 0.158 / 0.174 | 0.158 / 0.179 |
| 1 | 0.086 / 0.102 | 0.114 / 0.134 | 0.143 / 0.166 |
| 4 | 0.038 / 0.054 | 0.066 / 0.086 | 0.116 / 0.140 |
| 8 | 0.017 / 0.026 | 0.041 / 0.061 | 0.094 / 0.118 |

**Scale-free continuous world, one unit-gain EWMA.** Unit gain is forced: otherwise the error diverges at ω → 0 for α ≥ 1.
- **Closed form:** E(λ) = qλ^(1−α)/(−2cos(πα/2)) + Nλ/2, against e* = q^(1/α)N^(1−1/α)/sin(π/α).
- **Exact limit (sympy, `c_limit.out`):** c → **π²/32 − 1/8 = 0.18343**, and the linear term is exactly 0.
- **Over α 1.8–2.2:** c runs 0.160–0.212. Quadrature matches the closed form to 10⁻¹¹.
- **Two EWMAs with a free split** (`cont2.out`): the two-store threshold at |α−2| = 0.05 is ψ ≈ 2.6×10³ (α 1.95) and 2.4×10³ (2.05).

## 4. Findings

1. **Every author number reproduces** to the digits given:
   - span 10²: 0.033, 0.039, 0.043, 0.049, 0.052, 0.060
   - span 10⁴: 0.066–0.109
   - continuous model: 0.16–0.21
   - two-store thresholds: 9.8/8.5×10³, 6.1/5.4×10³ (mine 5.35×10³), 5.5/4.9×10³

   The author's diagnosis of the referee's 0.14 (an unpolished 5-point rate grid) is consistent with the polished numbers. I did not re-run c3.
2. **The (α−2)² scaling is confirmed:**
   - local exponents at span 10⁴: 1.96 (from α 1.98 and 1.95) and 2.04 (from 2.02 and 2.05);
   - exact zero linear term in the continuous model.

   c drifts upward with α, about 1.3–1.9× from α 1.8 to 2.2, so c(α−2)² is a leading-order statement only.
3. **"c ≈ 0.03–0.2" is not a bound** (fix i):
   - At span 10 in the same model, c = 0.005–0.010.
   - With more free taps per crossover time, c falls to 0.017 (and lower as more short-lag memory is free).
   - c saturates with span (10⁴ → 10⁵: +2–3%).
   - The largest value found is the no-free-memory, scale-free limit, π²/32 − 1/8 ≈ 0.18. I found no case above it, but I have not proved it is an upper bound.
4. **The knife-edge bullet is span- and model-dependent** (fix ii). "Two stores at ψ ≈ 10⁴ for |α−2| = 0.05" holds:
   - with four free taps at span 10²–10⁵ (threshold 4.8×10³–9.8×10³);
   - with no free memory (2.4–2.6×10³).

   It fails at span 10 (5–6×10⁴) and with eight free taps at τ_c = 2 (threshold ≳ 1.5×10⁴, from ε₁ alone). PR #51's changelog claimed this bullet was unchanged and true. It is true only with that qualification.

## 5. Rulings

- **Should THEORY quote a constant? No universal constant.** The narrowest true statement is:
  - the scaling ("one store iff ψ·c(α−2)² ≲ 1, leading order near α = 2");
  - c named as set by span and store model, with the one exact reference value (π²/32 − 1/8 for one EWMA with no free short-lag memory, scale-free);
  - the computed in-model cases labelled as such;
  - an obligation: **a prereg computes c for its own store model**.

  A bare range would be read as a bound, and §3 shows it is not one.
- **Threshold:** state it with its model and span ranges (fix ii), not as one number.
- **Locked preregs: no goalposts move.**
  - No locked prereg cites 0.14, a value of c or the ψ threshold (searched `tests/`, `prereg/`, `reviews/`).
  - MATCH1 C1 (layer count; locked, scored INCONCLUSIVE) uses its own K* rule (weighted RMS ≤ 0.02 in log₁₀ f) and is unaffected.
  - SPECTRUM-BRIDGE-SIM is not locked. Its QUEUE note now points to computing c for its own store model.
  - STAKES-SHIFT-CAISO, STAKES-EXOGENOUS, SELF, WIKIDATA-BAND and vigil-ona do not involve stores. H8 vigilance stays OPEN.
- **Not re-checked:** K* ≈ (ln 8R/2π²)·ln(stakes/upkeep), its rate, and the committed K* tables (the author's `c3_kstar_diag`).

## 6. Fixes applied (narrowing only)

- (i) N4 and the §2.2 store row: c is named as span- and model-dependent, with the exact no-free-memory value and the c3-model cases by span, and a prereg computes its own c.
- (ii) The §2.2 knife-edge bullet: thresholds are given with model and span (2.4–2.6×10³; 4.8×10³–9.8×10³; about 5–6×10⁴ at span 10).
- (iii) The changelog entry is v1.4.8 with this review record, and the header CLAIM_MAP pointer is v2.26.

No CLAIM_MAP status changes: K12 stays MATH-CORRECTED.
