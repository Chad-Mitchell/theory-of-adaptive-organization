# DISCRETE-TA: adaptation time on a sampled grid (pick 23, unaided slot; ledger 108–110, outcome 127)

Sunday 15 November 2026, about 5:35 PM ET (America/New_York). Grok Bot executor (queue-pick23) for Chad Mitchell, via Ace. Private; nothing posted or sent. This executor authored none of N16, the TELEGRAPH reports or `AQN_REFEREE`. All numbers are in-model (mathematics and simulation); no field data. **THEORY.md and CLAIM_MAP are not edited in this PR.** A proposed N16 scope sentence is in §6 and is authored in PR #53, marked "DO NOT MERGE without separate reviewer PASS" (queue item DISCRETE-TA-N16-REVIEW).

## 0. Verdict

| Question | Answer |
|---|---|
| Referee open question 1: is the referee's discrete t_A the same quantity as N16's? | **Yes, to within the referee's MC error, but it is one of two definitions.** The referee's values match the exact discrete filter started from the *quiet* law, meaning the filter's resting law after a long period with no switch, within 0.3–1.1 SE in all six block-C cells and both calibration cells (§5). That is the law N16's derivation used (∝ e^{L−κ cosh L}; TELEGRAPH_REFEREE §2). For a switch at a *typical* time, the right law is the stationary law at a switch. The two laws give t_A values 7–15% apart at κ = 0.03–0.1 (quiet 1.036–1.178× the plug-in, switch 0.965–1.023×). Both agree with the N16 plug-in to < 0.5% at κ ≤ 10⁻³ (§1). |
| Best linear tracker on the grid | **Closed form, exact:** cosh(βΔ) = cosh(aΔ) + ρ sinh(aΔ), t_A = 1/β (a = 2λ, ρ = μ²Δ/N). Ratio to the continuous memory time is 1 + (1 − a²τ²)²/(24 r²) + O(r⁻⁴). It is within 1% at r ≥ 2.0, within 5% at r ≥ 0.88 and within 10% at r ≥ 0.60 (r = t_A/Δ, slow world). |
| Bayes (Wonham) filter on the grid | **Leading correction derived:** t_A,grid = T(κ) + C₁√(ΔN)/μ + c₂Δ + o(Δ), with C₁ = −ζ(½)/√(2π) = 0.5826 (expected overshoot of the sampled log-odds below 0, by optional stopping) and c₂ ≈ 0.25 (numerical, 0.21–0.26; not derived). T(κ) is the exact continuous mean first passage (quadrature). With the Δ/4 term the formula is within 1.0% of the exact grid value for the quiet law, and within 1.5% for the switch law, whenever ρ ≤ 2 (fewer than about 2 samples per adaptation breaks it). Exact values on any grid come from a lattice Markov-chain solve, validated against an independent Monte Carlo: 20 cases, χ² = 12.9 on 20 df, max |z| = 2.25. |
| Correction factor vs r = t_A/Δ | **Not a function of r alone.** Relative to its own continuous value, the factor is 1 + 0.824/√(ℓ r) + 0.25/r, with ℓ = 2T/θ = ln(2/κ) − γ − 1, θ = N/μ². It decays like r^{−1/2}, much more slowly than the linear tracker's r^{−2}. |
| When is the continuous formula good? (quiet law, grid value vs the N16 plug-in) | **Within 10%:** r ≥ 10 (κ = 10⁻⁶), 13 (10⁻⁴), 17 (10⁻³), 27 (10⁻²), 65 (3·10⁻²). **Within 5%:** r ≥ 30, 43, 57, 122, and > 500. The switch law needs r ≥ 10–16 for 10% and 30–47 for 5% (§3.4). The referee's rule of thumb, "continuous only when t̂_A ≳ 20 steps", holds for 10% at κ ≤ 10⁻³ but not at κ ≥ 10⁻². No 5% rule at 20 steps holds for any κ. |
| Referee's V8 numbers | **Ratios stand to within their MC error; slightly revised:** 1.16–1.89× at plug-in 0.6–14 steps, and 1.06–1.08× at 56–151 steps (referee: 1.07–1.11×) (§5). |

Labels: in-model results (the per-sample HMM of §1.2). No field claim. No CLAIM_MAP status change is proposed (N16 stays MATH-CORRECTED; this narrows how its formula may be used on sampled data). Vigilance stays OPEN; untouched.

## 1. Definitions

### 1.1 Continuous time (N16)
World x(t) ∈ {+μ, −μ}, flips at rate λ each way; observation dy = x dt + √N dW. With θ = N/μ² and κ = λθ, the Wonham filter in log-odds L = ln P(+|y)/P(−|y) obeys dL = −2λ sinh L dt + (2μ/N) dy. After a switch to −μ, with the world held there, dL = (−2/θ − 2λ sinh L)dt + (2/√θ)dW.

**t_A = E inf{t ≥ 0 : L(t) ≤ 0}**, with L(0) drawn from a pre-switch law. Two laws are natural:
- **quiet:** p_q(L) = e^{L − κ cosh L}/(2K₁(κ)). This is the exact stationary density of the filter when the world has stayed at + forever, and the law TELEGRAPH_REFEREE §2 used to derive γ + 1.
- **switch:** p_s(L) = (1 + e^L) e^{−κ cosh L}/(2(K₀(κ) + K₁(κ))), the stationary law of L given x = + (from the stationary density ∝ cosh²(L/2) e^{−κ cosh L}, TELEGRAPH_REFEREE §2, times P(+|L)). Because the switch hazard is constant, this is the law at a switch chosen at a typical time. It is what averaging over all switches in a stationary record measures.

The mean first passage from y is T(y) = ∫₀^y g, with g(y) = ½∫_y^∞ e^{Φ(y) − Φ(z)} dz and Φ = L + κ cosh L (generator 2T″ − (2 + 2κ sinh L)T′ = −1, T(0) = 0, T′ bounded). This matches TELEGRAPH_REFEREE §2. Then t_A = θ∫₀^∞ g(y) P(L₀ > y) dy, computed by quadrature in `tools/discrete_ta.py::bayes_ta_cont`. The two laws differ in mass of relative order K₀/K₁ ≈ κ ln(2/κ):

| κ | plug-in (θ units) | quiet / plug-in | switch / plug-in |
|---|---|---|---|
| 0.1 | 0.709 | 1.178 | 1.023 |
| 0.03 | 1.311 | 1.036 | 0.965 |
| 0.01 | 1.861 | 1.010 | 0.978 |
| 10⁻³ | 3.012 | 1.0008 | 0.996 |
| 10⁻⁴ | 4.163 | 1.0001 | 0.9994 |

Both tend to the N16 plug-in (N/2μ²)[ln(2μ²/λN) − γ − 1], which is the κ → 0 asymptote of either. N16's "+o(1)" covers both. **Recommendation:** a prereg that reads t_A off a record averaged over switches should lock the switch law. One that measures adaptation after long quiet spells should lock the quiet law. Each is computable exactly with the tool.

### 1.2 Sampled grid (the HMM the `aqn` estimators fit)
Samples every Δ: x_k ∈ {±μ}, flip probability p = (1 − e^{−2λΔ})/2 between samples, and y_k = x_k + e_k with Var e = s² = N/Δ (so N = s²Δ, as in `aqn`). Per-sample SNR ρ = μ²Δ/N = Δ/θ. The exact filter is the forward recursion L_k = f(L_{k−1}) + 2μy_k/s², with f(L) = ln[((1−p)e^L + p)/(p e^L + 1 − p)]. Given x_k = −μ, the increment is N(−2ρ, 4ρ). The KL rate per unit time is 2μ²/N, the same as in continuous time.

**t_A,grid = Δ · E min{n ≥ 0 : L_n ≤ 0}.** Here L_0 is the posterior after the last pre-switch sample, drawn from the discrete analogue of the quiet or switch law. The first post-switch sample is n = 1, and the world is held at −μ. This is the exact discrete analogue of §1.1. Holding the world matters: without it, MC gives 24.0 ± 0.2 instead of 15.6 at σ = 3, λ = 0.002, because the filter can be chasing a world that has already switched back. Model scope: the world switches only between samples. An integrate-and-dump record of a continuous world, with switches inside intervals, is not covered (new item DISCRETE-TA-INTEGRATED).

### 1.3 Linear tracker
Same second moments: an OU world with rate a = 2λ, variance μ², q = 2aμ² = 4λμ², sampled exactly. So x_k = φx_{k−1} + w_k with φ = e^{−aΔ}, Var w = μ²(1 − φ²), and Var e = N/Δ. The best linear tracker is the steady-state Kalman filter x̂_k = z x̂_{k−1} + K y_k, with pole z = (1 − K)φ. **t_A = memory (e-folding) time = Δ/(−ln z).** Its continuous limit is 1/√(a² + q/N), the memory time of THEORY §2.2. The "mean lag" definition z/(1 − z)·Δ = t_A − Δ/2 + O(Δ²) differs at O(Δ), so preregs must say which they use.

## 2. Linear tracker: closed form

The discrete algebraic Riccati equation for the prior variance M is M² + [R(1 − φ²) − Q]M − QR = 0, with R = N/Δ and Q = μ²(1 − φ²). It gives K = M/(M + R) and z = φR/(M + R). Eliminating M gives z + 1/z = φ + 1/φ + Q/(φR). Write z = e^{−βΔ} and φ = e^{−aΔ}, and use Q/(2φR) = ρ sinh(aΔ). Then

  **cosh(βΔ) = cosh(aΔ) + ρ sinh(aΔ)**  (exact).

Expanding both sides to fourth order in Δ, with β_c² = a² + 2aμ²/N:

  β_c/β = 1 + (β_c² − a²)²Δ²/(24β_c⁴) + O(Δ⁴) = 1 + (1 − a²τ_c²)²/(24 r²) + O(r⁻⁴),  r = τ_c/Δ.

Checks (`checks/compare.out`, `tools/test_discrete_ta.py`): the closed form equals the Riccati iteration to 10 digits in four cases, the empirical filter MSE matches P_post (0.17301 vs 0.17297), and the series matches the exact ratio at r ≥ 1.5. The ratio is at most 1 + 1/(24r²): 4.2% at r = 1, 1.0% at r = 2, 0.04% at r = 10. **The linear memory time needs no grid correction once r ≥ 2.** At r ≈ 0.6–0.9 it is still within 10% and 5%. Credit: derived here. The scalar steady-state Kalman filter is textbook, and the cosh form is probably classical, but no source was read this session, so none is cited.

## 3. Bayes filter on the grid

### 3.1 Exact values (lattice)
`bayes_ta_grid` puts L on a lattice of cells of width h ≤ min(0.05, sd/12), with an edge at 0. The transition is the exact prediction f followed by the Gaussian increment, integrated over each cell. The stationary law uses the symmetry p₋(L) = p₊(−L) and is solved as a null vector, p₊ = T₊[(1 − p)p₊ + pJp₊]. The quiet law is the null vector of T₊ alone. The post-switch mean is E n = 1′(I − Q)⁻¹v₀, where Q is the transition restricted to L > 0. Lattice convergence: 6.1308 at h = 0.05 and 0.025; 58.200 → 58.211 → 58.214 at h = 0.028, 0.025, 0.0125; padding 8 → 14 changes 58.210 → 58.210.

### 3.2 The leading correction (derivation)
Let τ_c be the continuous crossing time and τ_d the first grid time with L ≤ 0, so τ_d ≥ τ_c. M_t = L_t + 2t/θ + ∫₀^t 2λ sinh L_s ds is a martingale. Optional stopping at τ_c and at τ_d, then subtracting, gives

  (2/θ)(E τ_d − E τ_c) = −E L_{τ_d} − E ∫_{τ_c}^{τ_d} 2λ sinh L ds.

The last term is O(λ Δ^{3/2}), because L stays near 0 between the two times. −E L_{τ_d} is the expected overshoot of a diffusion with volatility σ_L = 2/√θ, monitored every Δ. That overshoot is β σ_L √Δ + o(√Δ), with β = −ζ(½)/√(2π) ≈ 0.5826. This is the constant of Siegmund's corrected diffusion approximation, as stated and used by Broadie, Glasserman & Kou (1997, *Math. Finance* 7:325–348, **read**: their eq. under Theorem 1.1, "β = −ζ(½)/√(2π) ≈ 0.5826", and §1.2 identifying the shift βσ√Δt with the overshoot at the first monitoring instant; Siegmund's papers were not read). Hence

  **E τ_d − E τ_c = β √(θΔ) + o(√Δ) = 0.5826 √(ΔN)/μ.**

This is in time units. It does not depend on λ or κ, because the drift at L = 0 is −2/θ whatever λ is. The −κ sinh term vanishes there. BGK prove the probability version; the mean-time version is derived here by the stopping argument, at physicist's rigour. The elasticities of this term are ½ in N, −1 in μ and 0 in λ, the linear tracker's N and μ elasticities. So on a grid, a measured Bayes t_A mixes N16's exponents with linear-looking ones (§6).

### 3.3 Numerical check of the expansion
g = (t_A,grid − T)/√(Δθ) as a function of ρ, from `checks/compare.out`:
- κ = 10⁻⁴: g = 0.603, 0.618, 0.634, 0.656, 0.700, 0.747, 0.810, 0.871 at ρ = 0.008, 0.021, 0.042, 0.083, 0.21, 0.42, 0.83, 1.39. So g − C₁ ≈ 0.25√ρ (0.22–0.26) throughout, which means t_A,grid ≈ T + C₁√(Δθ) + 0.25Δ.
- κ = 10⁻² and 3·10⁻²: g − C₁ ≈ (0.21–0.24)√ρ at ρ ≥ 0.04. At the finest grid (ρ = 0.0025), lattice extrapolation gives g = 0.595 at κ = 10⁻⁴, exactly C₁ + 0.25√ρ = 0.595, but 0.568 at κ = 10⁻², 4.5% below it. A κ-dependent residual at small ρ is not resolved. It is at most 0.0013θ in time there, but it means the leading constant is confirmed numerically only to about 5% at κ = 10⁻². **c₂ is a fit, not derived** (new item DISCRETE-TA-SECOND-ORDER).
- Coarse grids, ρ > 2 (fewer than about 2 samples per adaptation): g rises steeply (1.1–1.9), and E n is at least about 1 step. Use the lattice there.

**[Reviewer errata, DISCRETE-TA-N16-REVIEW, 15 Nov 2026 about 6:05 PM ET; original text kept; `reviews/night2/DISCRETE_TA_N16_REVIEW.md`.]** (E1) §3.2: "The last term is O(λΔ^{3/2})" and "It does not depend on λ or κ" do not hold. Between the continuous and the sampled crossing the path makes upward excursions of O(1) in L, so E∫_{τ_c}^{τ_d} 2λ sinh L ds is O(λ√Δ), with a log. The √Δ coefficient is c(κ) = C₁(1 − O(κ ln 1/κ)). Converged Nyström values extrapolated to ρ → 0 (reviewer's own code) give c = 0.5822 (κ = 10⁻⁴), 0.5673 (10⁻²) and 0.5466 (3·10⁻²), that is 0.06%, 2.6% and 6.2% below C₁. A barrier-shift heuristic, C₁∫₀^∞e^{−z−κ(cosh z−1)}dz, accounts for about 80% of that deficit. (E2) §3.3: the finest-grid value at κ = 10⁻², ρ = 0.0025 is g = 0.5803 (converged to 10 digits), not 0.568; the 4.5% residual was a lattice-extrapolation artifact, but the real κ-dependence is E1. (E3) §2: the first form of the ratio should read (β_c² − a²)²Δ²/(24β_c²), not /(24β_c⁴); the r-form is right. The slow-world ratio is 1.0102 at r = 2.0, so 1% is reached at r ≥ 2.02. (E4) §3.4: the thresholds assume time is counted from the last pre-switch sample. Timed from a switch placed uniformly inside the interval (−Δ/2), the quiet-law 10% thresholds are 5.2 (κ = 10⁻³) and 15.6 (10⁻²), and the 5% thresholds are 35.7 and 94.9. The threshold values in the table reproduce within interpolation (reviewer: 9.6/30.4, 16.2/56.2, 26.8/119.8 quiet; 15.1/38.7, 14.8/46.8 switch).

`bayes_asymptotic` (T + C₁√(Δθ) + Δ/4) vs lattice over the full table: worst error is 1.0% (quiet) and 1.5% (switch) at ρ ≤ 2, against 11% at ρ > 2.

### 3.4 Correction-factor map (θ = 1; cells: quiet/T_quiet · quiet/plug-in · switch/plug-in)

| r = plug-in/Δ | κ=0.03 | κ=0.01 | κ=0.001 | κ=0.0001 | κ=1e-06 |
|---|---|---|---|---|---|
| 1 | 1.718 / 1.780 / 1.713 | 1.654 / 1.670 / 1.643 | 1.556 / 1.557 / 1.553 | 1.501 / 1.501 / 1.500 | 1.448 / 1.448 / 1.448 |
| 2 | 1.455 / 1.507 / 1.430 | 1.416 / 1.430 / 1.397 | 1.358 / 1.359 / 1.354 | 1.324 / 1.324 / 1.323 | 1.288 / 1.288 / 1.288 |
| 5 | 1.259 / 1.304 / 1.226 | 1.236 / 1.248 / 1.213 | 1.200 / 1.201 / 1.196 | 1.177 / 1.178 / 1.177 | 1.151 / 1.151 / 1.151 |
| 10 | 1.172 / 1.214 / 1.137 | 1.156 / 1.168 / 1.133 | 1.131 / 1.132 / 1.127 | 1.116 / 1.116 / 1.115 | 1.098 / 1.098 / 1.098 |
| 20 | 1.116 / 1.156 / 1.081 | 1.105 / 1.116 / 1.082 | 1.088 / 1.089 / 1.083 | 1.077 / 1.077 / 1.076 | 1.064 / 1.064 / 1.064 |
| 50 | 1.070 / 1.109 / 1.035 | 1.063 / 1.074 / 1.041 | 1.052 / 1.053 / 1.048 | 1.045 / 1.046 / 1.045 | 1.038 / 1.038 / 1.038 |
| 100 | 1.049 / 1.086 / 1.013 | 1.044 / 1.054 / 1.021 | 1.036 / 1.037 / 1.032 | 1.031 / 1.031 / 1.030 | 1.025 / 1.025 / 1.025 |
| 200 | 1.034 / 1.071 / 0.999 | 1.030 / 1.040 / 1.008 | 1.025 / 1.026 / 1.021 | 1.021 / 1.021 / 1.021 | 1.017 / 1.017 / 1.017 |
| 500 | 1.021 / 1.057 / 0.986 | 1.019 / 1.029 / 0.996 | 1.015 / 1.016 / 1.011 | 1.013 / 1.013 / 1.013 | 1.011 / 1.011 / 1.011 |

Thresholds are the smallest r beyond which the factor stays inside the band, log-interpolated (`checks/compare.out`):

| factor | κ = 3·10⁻² | 10⁻² | 10⁻³ | 10⁻⁴ | 10⁻⁶ |
|---|---|---|---|---|---|
| quiet grid / plug-in, 10% | 65 | 27 | 17 | 13 | 10 |
| quiet grid / plug-in, 5% | > 500 | 122 | 57 | 43 | 30 |
| switch grid / plug-in, 10% | 16 | 16 | 15 | 13 | 10 |
| switch grid / plug-in, 5% | 36 | 39 | 47 | 42 | 30 |
| grid / own continuous T, 10% | 26 | 22 | 16 | 13 | 10 |
| grid / own continuous T, 5% | 96 | 80 | 55 | 43 | 30 |

At κ = 3·10⁻², the quiet law's own continuous value is 3.6% above the plug-in, so the 5% band against the plug-in is never reached. At κ ≥ 10⁻², the switch law's continuous value sits below the plug-in, which partly cancels the grid excess. The closed-form guide is grid/T − 1 ≈ 0.824/√(ℓr) + 0.25/r: 5% needs ℓr ≈ 300–400 and 10% needs ℓr ≈ 80–130, because the 0.25/r term matters at small r.

## 4. Independent validation
`checks/mc_discrete.py` simulates the actual per-sample worlds and filters with its own code. It does not import the tool or any `AQN_REFEREE` code, and its probability-form and log-odds-form filter steps agree to 10⁻¹⁵. The switch law is taken at real flips of long stationary chains; the quiet law comes from long no-flip burn-ins. Each case has 200,000 switch events (seed 2312; `checks/mc_discrete.json`). The first run (seed 2311) is superseded and not kept. Its one 2.6 SE cell (λ = 0.0005, N = 36) came out at 0.8 SE on rerun.

| law | λ | N | Δ | MC | lattice | z |
|---|---|---|---|---|---|---|
| switch | 0.002 | 0.25 | 1 | 1.3566 ± 0.0012 | 1.3568 | −0.16 |
| switch | 0.01 | 0.25 | 1 | 1.2048 ± 0.0010 | 1.2060 | −1.12 |
| switch | 0.002 | 2.25 | 1 | 6.1144 ± 0.0073 | 6.1308 | −2.25 |
| switch | 0.01 | 2.25 | 1 | 4.2465 ± 0.0060 | 4.2458 | +0.10 |
| switch | 0.002 | 9 | 1 | 15.575 ± 0.023 | 15.569 | +0.24 |
| switch | 0.01 | 9 | 1 | 8.608 ± 0.016 | 8.592 | +1.00 |
| switch | 0.0005 | 36 | 1 | 58.28 ± 0.09 | 58.21 | +0.76 |
| switch | 0.01 | 1 | 0.05 / 0.2 / 0.5 | 1.9583 / 2.1214 / 2.3464 (± 0.003) | 1.9564 / 2.1211 / 2.3456 | +0.70 / +0.10 / +0.28 |
| quiet | 0.002 / 0.01 | 2.25 | 1 | 6.2268 / 4.4634 | 6.2253 / 4.4553 | +0.22 / +1.40 |
| quiet | 0.002 / 0.01 | 9 | 1 | 16.297 / 9.697 | 16.315 / 9.702 | −0.83 / −0.32 |
| quiet | 0.0005 | 36 | 1 | 61.05 ± 0.09 | 61.10 | −0.64 |
| quiet | 0.001 | 1 | 0.01 / 0.05 / 0.2 | 3.0745 / 3.1589 / 3.3265 (± 0.004) | 3.0746 / 3.1567 / 3.3255 | −0.04 / +0.61 / +0.27 |
| quiet | 10⁻⁴ | 1 | 0.02 / 0.5 | 4.2528 / 4.6990 (± 0.004) | 4.2507 / 4.7021 | +0.51 / −0.69 |

Over all 20 cases, χ² = 12.9 on 20 df. The small-Δ quiet cases also check the continuous limit. At κ = 10⁻³ and Δ = 0.01, MC gives 3.0745 against T_quiet + C₁√Δ + Δ/4 = 3.0142 + 0.0583 + 0.0025 = 3.0750.

## 5. The referee's V8 numbers, re-read
Lattice values in steps (μ = 1, Δ = 1, N = σ²):

| σ | λ | plug-in | referee (MC) | quiet (lattice) | switch (lattice) | noiseless resting start | quiet/plug-in |
|---|---|---|---|---|---|---|---|
| 0.5 | 0.002 | 0.84 | 1.35 ± 0.01 | 1.358 | 1.357 | 1.364 | 1.62 |
| 0.5 | 0.01 | 0.64 | 1.21 ± 0.01 | 1.209 | 1.206 | 1.214 | 1.89 |
| 1.5 | 0.002 | 5.08 | 6.31 ± 0.08 | 6.225 | 6.131 | 6.659 | 1.22 |
| 1.5 | 0.01 | 3.27 | 4.43 ± 0.06 | 4.455 | 4.246 | 4.888 | 1.36 |
| 3 | 0.002 | 14.10 | 16.14 ± 0.25 | 16.315 | 15.569 | 18.098 | 1.16 |
| 3 | 0.01 | 6.86 | 9.90 ± 0.19 | 9.702 | 8.592 | 11.345 | 1.41 |
| 6 | 0.0005 | 56.40 | 62.56 ± 1.58 | 61.101 | 58.210 | 68.196 | 1.083 |
| 10 | 0.0002 | 151.40 | 161.56 ± 3.82 | 160.525 | 152.278 | 180.053 | 1.060 |

The referee's numbers are the quiet-law quantity (|z| ≤ 1.1), not the switch law (up to 6.9 SE off) and not a deterministic resting point. So the referee's "no-switch resting state" means the quiet law, which is N16's derivation law. **Q1 answered: same quantity.** The caveat is that, at the referee's κ (0.018–0.09), a record averaged over switches would show the switch-law values, which are 1.5–11% shorter at σ ≥ 1.5.

## 6. Consequences and proposed text (not applied here)
1. **Field use of N16 on sampled data.** Do not compare a sampled t̂_A with the plug-in unless r = t̂_A/Δ clears the §3.4 threshold for the measured κ and the chosen law. Otherwise, compare with `tools/discrete_ta.py bayes`, or with the two-term formula when ρ ≤ 2. This replaces AQN_REFEREE's rule "continuous only when t̂_A ≳ 20 steps". That rule is right for 10% at κ ≤ 10⁻³ and wrong at κ ≥ 10⁻²; the 5% thresholds are 30–120+ steps. It also replaces the "1.1–1.9× at < 20 steps" summary in items.json.
2. **Exponents on a grid.** The grid term C₁√(ΔN)/μ has elasticities (0, ½, −1) in (switching time, N, μ). A measured Bayes elasticity is therefore the T-weighted mix (T·ε_N16 + δ·ε_grid)/(T + δ), with δ the grid excess. At r = 20 and κ = 10⁻³, δ/T ≈ 8.8%, so the switching-time elasticity drops from 1/ℓ ≈ 0.166 to 0.153, and the N elasticity moves from 0.834 to 0.80. A Bayes-vs-linear discrimination on sampled data must use the grid-corrected exponents. Example: CAUSAL-NULL-INVARIANCE's discriminator, λ ×2.65 with μ² ×0.75, holds the continuous Bayes t_A fixed but raises the √ part of δ by 15.5% (μ⁻¹), about +1.2% of t_A at r = 20. That is small but not zero.
3. **Proposed N16 scope sentence (THEORY §2.2 Regime A premise bullet and CLAIM_MAP N16; a math scope correction to core text, so a separate PR "DO NOT MERGE without separate reviewer PASS"):** "Definition and grid: t_A is the mean time to cross zero after a switch, with the filter's pre-switch law fixed in the prereg. The formula is derived for the resting law after a long quiet period; for a switch at a typical time the value differs by O(κ ln 1/κ), < 0.5% at κ ≤ 10⁻³ (`reviews/night2/DISCRETE_TA/REPORT.md` §1). On data sampled every Δ, the adaptation time read at the samples is longer, t_A + 0.58√(ΔN)/μ + O(Δ), so the formula is within 10% only when t_A ≳ 10–27 samples (κ = 10⁻⁶ to 10⁻²) and within 5% only when t_A ≳ 30–120 samples; the best linear tracker's memory time needs no correction beyond 2 samples. Use `tools/discrete_ta.py` otherwise."

## 7. Scope limits and what is not done
- Only the symmetric two-state world with a held post-switch world. Sampling is per-sample point noise with switches only between samples. Integrate-and-dump of a continuous world (switch inside an interval) is not covered; it changes the effective first post-switch sample (DISCRETE-TA-INTEGRATED).
- C₁ is derived at physicist's rigour, using BGK's constant for the mean-time version. c₂ ≈ 0.25 is a numerical fit (DISCRETE-TA-SECOND-ORDER).
- The quiet/switch distinction is about the filter's state at the switch, not the world model. Both are N16's "t_A" to o(1).
- Prior art read this session: Broadie, Glasserman & Kou 1997 (full text, Columbia-hosted author PDF). Not read: Siegmund (1979, 1985), the discrete Riccati literature, Wonham 1964. None is cited for a result beyond what BGK state.

## 8. Files
- `tools/discrete_ta.py` (CLI + library) and `tools/test_discrete_ta.py` (12 tests, about 3 s).
- `checks/mc_discrete.py` → `mc_discrete.json`, `mc_discrete.log` (independent MC, seed 2312).
- `checks/table.py` → `table.json`, `table.out` (correction-factor map).
- `checks/compare.py` → `compare.out` (lattice vs MC, linear closed form vs iteration, asymptote, universality, thresholds).
