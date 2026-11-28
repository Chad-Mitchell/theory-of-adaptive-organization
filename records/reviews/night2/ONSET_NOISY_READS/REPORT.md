# ONSET-NOISY-READS: the noisy-read crossover of the pooling onset, in closed form

Sunday 15 November 2026, about 6:07–6:20 PM ET (America/New_York). QUEUE ONSET-NOISY-READS, pick 29, rule slot (ledger 134 unaided order, 135 rule_rank, 136 claim, outcome entry in the same branch). Grok Bot executor for Chad Mitchell, via Ace. Private; nothing posted or sent. In-model only (formal layer, THEORY §2.5, CLAIM_MAP N12); no field claim, no "law".

**Source of the item:** `reviews/night2/N12_REFEREE.md` C1 and limit "a closed form for the crossover ρ_c(α, σ²) is not derived". **Code:** `reviews/night2/ONSET_NOISY_READS_checks/` (own code; imports nothing from `N12_REFEREE_checks/`; run at nice 19).

## 1. Model (same as N12 referee c3, restated)

Member units q_u = w = c = 1. fBm drift with Var[x(t)−x(s)] = q|t−s|^{α−1}, 1 < α < 3. A tracker reads x + ε every T (Var ε = σ², price c per read), predicts with the optimal linear (Gaussian-conditioning) predictor on its past reads, and pays c/T + w·(time-averaged MSE). The MSE is q T^{α−1} f_α(z), z = σ²/(q T^{α−1}). Cost φ(w, q; σ²) = min_T [1/T + w q T^{α−1} f_α(σ²/(q T^{α−1}))].
Flat: each of N members tracks q = 1 + ρ. Pooled (𝒜₁, no broadcast cost, h = 0): each member tracks q = 1, a level tracks the shared drift ρ at weight N. Onset N\*: N[φ(1, 1+ρ) − φ(1, 1)] = φ(N, ρ). Read noise σ² is the same at the level and the members (members' noise enters only through their marginal cost D, §2).

## 2. Results

**R1. Exact collapse (identity).** φ(N, ρ; σ²) = Ψ(Nρ, σ²/ρ) with Ψ(x, s) = min_T [1/T + x T^{α−1} f_α(s/T^{α−1})]. With the flat gain N·ρ·D + O(Nρ²), D = ∂_q φ(1, q; σ_m²)|_{q=1}, the onset obeys, to leading order in ρ,

  **N\* ρ = X_α(s),  s = σ²/ρ,**  where X solves x D = Ψ(x, s).

So at small ρ the crossover depends on (ρ, σ²) only through s = σ²/ρ, the level's read noise over the shared drift in member units (in physical units s = σ_L²/(q_g τ₀^{α−1}), τ₀ = (c/(w q_u))^{1/α}). Numerically (`onset.out`): at fixed s, N\*ρ for σ² = 10⁻⁴, 10⁻³, 10⁻² agree to ≤ 0.02% once ρ ≤ 10⁻³ (e.g. α = 2, s = 10: 191.026, 191.039, 191.140, the last at ρ = 10⁻³).

**R2. Two closed asymptotes.**
- s → 0 (exact reads): X₀ = α^{α/(α−1)} (3.375, 4, 4.605 at α = 1.5, 2, 2.5), independent of the predictor constant f_α(0) (it cancels). Recovers N\* ≈ 4/ρ at α = 2. Exponent −1.
- s → ∞ (noise-limited level): the level's optimal T → 0 and z → ∞, where f_α(z) → g_α z^{1−1/α} with
  **g_α = (Γ(α) sin(π(α−1)/2))^{1/α} / sin(π/α)**
  (dense-sampling limit = continuous observation with noise intensity σ²T; Yovits–Jackson error (n/2π)∫ln(1+S/n)dω for S(ω) = qΓ(α)sin(π(α−1)/2)|ω|^{−α}, using ∫₀^∞ ln(1+u^{−α})du = π/sin(π/α)). Then the level's cost is c/T + N g ρ^{1/α}(σ²T)^{1−1/α}: per-read price linear in precision 1/(σ²T), i.e. the **θ = 1 class**, a_L = α/(2α−1), b_L = 1/(2α−1), onset exponent −(1−b_L)/(1−a_L) = **−2 for every α** (sympy, `sym.out`). The onset is
  **X ≈ C_α s, i.e. N\* ≈ C_α σ²/ρ²,  C_α = [(2α−1)/((α−1)D)]^{(2α−1)/(α−1)} · (g_α(α−1)/α)^{α/(α−1)},**
  with D = D₀ = (α−1)^{1/α−1} f_α(0)^{1/α} for exact-reading members. C_α = 9.247, 19.09, 38.87 at α = 1.5, 2, 2.5 (f_α(0) = 0.5910, 0.5, 0.3231 by conditioning, M = 2000).

**R3. Crossover in closed form.** Defining the crossover where the two asymptotes meet,
  **ρ_c = σ² · C_α / X₀ = σ² · C_α α^{−α/(α−1)}**, i.e. s_c = X₀/C_α.
ρ_c/σ² = 2.10, 2.74, 4.77, 8.44, 12.2 at α = 1.25, 1.5, 2, 2.5, 2.75: **linear in σ², with an α-dependent prefactor rising with α**. This is the closed form the referee asked for (exact up to the one numerical constant f_α(0); at α = 2, f₂(0) = ½ and g₂ = 1, so everything is closed: C₂ = 27√2/2 ≈ 19.09, X₀ = 4, **ρ_c = (27√2/8) σ² ≈ 4.773 σ²**, i.e. N\* ≈ (27√2/2) σ²/ρ² beyond it; `xs.out`).
At the crossover the level's own noise ratio at its optimal read interval is z_L ≈ 0.17–0.47 (α = 2.75 … 1.25): the referee's criterion "σ² ≪ q_g T\*^{α−1}" is the right one, with the boundary at z_L of order ½.

**R4. Shape of the transition (`xs.out`).** The local exponent e(s) = −1 − d ln X/d ln s is a universal function of s for each α. It passes −1.25, −1.5, −1.75 at s = (0.158, 0.409, 0.950) for α = 1.5, (0.100, 0.244, 0.517) for α = 2, (0.058, 0.139, 0.288) for α = 2.5: the middle half of the transition spans about 0.6–0.8 decades of s, so about the same in ρ at fixed σ². The sum X₀ + C_α s is within 13–18% of X everywhere (largest near s_c).

**R5. Reproduction of the referee (independent code).** σ² = 10⁻³, local slope between ρ = 10⁻² and 10^{−2.5}: −1.277, −1.401, −1.583 at α = 1.5, 2, 2.5 (referee c3: −1.28, −1.40, −1.58).

## 3. The limit (proof sketch, with what is assumed)

Claim: for fixed σ² > 0, N\*ρ²/σ² → C_α and d ln N\*/d ln ρ → −2 as ρ → 0, at every 1 < α < 3, for the model of §1.
1. R1's collapse is an identity (substitute z; `sym.out` checks the integrand).
2. Flat gain: φ(1, ·) is smooth in q at q = 1, so N[φ(1,1+ρ) − φ(1,1)] = NρD(1 + O(ρ)).
3. With x = Ψ-root of order s (the limiting equation x D = K(x g s^β)^{α/(2α−1)}, β = 1 − 1/α, has the unique positive root x = C_α s because its right side is sublinear in x), the optimising T scales as s^{−1} and z = s/T^{α−1} ∝ s^α → ∞; given f_α(z) = g_α z^β(1 + o(1)) as z → ∞ and f increasing, Ψ(x, s) = Ψ_∞(x, s)(1 + o(1)) uniformly on x ∈ [s/K, Ks], so the root obeys X(s)/s → C_α.
4. N\* = X(σ²/ρ)/ρ · (1 + O(ρ)) → C_α σ²/ρ².

**Assumed, not proved here:** the dense-sampling asymptote f_α(z) ~ g_α z^{1−1/α} for periodically sampled fBm with the optimal predictor on the full past (the Yovits–Jackson formula is applied, not read here; its integral identity is checked in sympy). Numerically: exact at α = 2 (conditioning = discrete Kalman to 10⁻¹⁰; f/(g z^{1/2}) = 1.00001 at z = 10⁴); f/(g z^β) = 1.000–1.004 at α = 1.5 (z = 10²–10³), 1.001–1.003 at α = 2.5 and 2.75 (z = 10²–10⁴). Finite-M truncation spoils the check at α = 1.25 for z ≥ 10³ and at α = 1.5 for z ≥ 10⁴ (values move toward 1 as M grows; `fz.out`, `g125.out`). The step "e(s) → −2" additionally needs X'(s) → C_α, shown numerically (e = −2.000 ± 0.003 for s ≥ 10 at α ≥ 1.5), not proved. Periodic reading is assumed, as in the referee (not shown optimal for α ≠ 2 with noisy reads).
**Status: derived at physicist's rigour, numerically checked, not refereed.**

## 4. How an N2 test classifies the level's technology

1. A measured onset slope between −1 and −2 does **not** identify θ. Priced precision with θ = ½ gives −1.5 at every ρ; noisy reset reads give −1.5 at one s only (s ≈ 0.24 at α = 2). The signature that separates them is **curvature**: with fixed read noise, noisy reset reads steepen from −1 toward −2 as ρ falls (e(s) in R4); priced precision is straight.
2. **Measure z_L** = σ_L²/(q_g T_L^{α−1}) at the level's actual read interval: z_L ≲ 0.05 → reset class (−1); z_L ≳ 10 → θ = 1 (−2); in between, the prereg must use e(s) at the measured s, not either asymptote.
3. Where read noise can be varied (or differs across groups), the collapse N\*ρ = X_α(σ²/ρ) is a parameter-free check once α and D are measured: plotting N\*ρ against σ²/ρ should put all groups on one curve with asymptotes X₀ and C_α s.
4. The members' noise moves only D (their marginal cost per unit drift); with measured D, use X₀ = (κ f_α(0)^{1/α}/D)^{α/(α−1)}, κ = α(α−1)^{1/α−1}, and C_α with that D.

## 5. Consequences for THEORY and CLAIM_MAP

- THEORY §2.5 N12 premise (ii) currently says the −2 limit is "shown numerically, not proved; the crossover's closed form is not derived". Proposed text in the separate author-only PR #60 (THEORY v1.4.11, DO NOT MERGE without separate reviewer PASS; v1.4.10 is taken by unmerged PR #58): the collapse, ρ_c = σ² C_α/X₀ (2.7, 4.8, 8.4 σ² at α = 1.5, 2, 2.5), the θ = 1 classification, the z_L criterion, and the curvature test. CLAIM_MAP v2.29 note (v2.28 taken by PR #58): N12 stays MATH-CORRECTED; premise (ii) moves from "numerical" to "derived (sketch; one assumed asymptote)".
- No locked prereg moves (none cites ρ_c; LEARNSIM used exact reads).

## 6. Limits

In-model only. One technology (periodic noisy reads, linear predictor); same α for shared and private drift; small ρ; 𝒜₁, no broadcast cost, h = 0. The α = 1.25 large-s numbers are M-limited (X/(C s) = 1.13 at s = 10³ is a truncation artifact, not a counterexample; the closed C_α is unaffected). Prior art: none read; nothing credited. The Yovits–Jackson formula is used as standard, not read here. Novelty: elementary; not searched.

## 7. Files

`fz.py/.out/.json` (f_α(z), Kalman check, asymptote g_α), `onset.py/.out/.json` (onset over ρ, σ², α; collapse; referee reproduction), `xs.py/.out/.json` (X_α(s), e(s), s_c, z_L, two-asymptote error), `sym.py/.out` (branch algebra, θ = 1 class, integral identity), `g125.py/.out` (asymptote at α = 1.25, 2.75).
