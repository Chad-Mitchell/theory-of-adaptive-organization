# PREREG — KERNEL-MEASURE (QUEUE pick 28, uniform slot; ledger 130–132)

Executor `queue-pick28` (for Ace; Chad t1914), Sunday 15 Nov 2026, America/New_York. Locked by the git commit that adds this file, pushed to `origin/q-pick28` **before** the VIX kernel regression was run (no external timestamp: MV9 needs Chad's go, so Tier 2 at best). Code and data hashes: `SHA256SUMS`.

## 1. What is tested (THEORY v1.4.8 §2.2, Regime B table, row "Forgetting kernel"; §2.5 rule "regime first")
The best linear tracker of a drifting target with spectrum S(ω) = q|ω|^−α observed in white noise N weights past readings by a kernel whose survival (weight on everything older than τ) falls as τ^−α/2, positive for α < 2, exponential only at α = 2. No GTAO test has measured a kernel (§2.2, "no kernel has been measured in any GTAO test"). This test measures one, on one system, with α, q and N measured on that system's driver.

- **System.** Driver: S&P 500 daily variance. Tracker: VIX (the market's 30-calendar-day forecast of S&P 500 variance; `VIXCLS`, FRED).
- **Proxies (declared).** Driver reading y_t = ln[(ln H_t/L_t)²/(4 ln 2)] (Parkinson daily range variance, Yahoo `^GSPC` OHLC; overnight variance excluded); tracker z_t = 2 ln VIX_t; business days as equal steps; 1990‑01‑02 … 2026‑10‑30 (n = 9 276).
- **Which projection (TELEGRAPH-REFEREE; THEORY §2.5).** The kernel measured is the regression of z on the past proxy readings y. The proxy is in the market's information set, so by iterated projections this equals the best linear predictor of the target from the proxy alone **if VIX is an optimal forecast**. It is an own-observation-type kernel: it **cannot** tell a Bayes tracker from a linear one, and does not test N16. It tests the spectrum → kernel map for the linear optimum (Gaussian world or best linear tracker premise), on proxy.
- **Optimum locked (one, before data):** the best linear tracker (THEORY §2.2 premise bullet; HEADLINE-PREMISE lock guard).

## 2. Regime first (driver only; no VIX data used; `driver_spectrum.py/.json`, `driver_band.py/.json`)
- Full-band Whittle (AQN-ESTIMATORS `aqn.py`): α̂ = 1.303 ± 0.048, ln q̂ = −1.92, ln ŝ2 = −0.900 ± 0.118 (crossover ω_c = 0.46 rad/day). Under AQN's R1 as written (band split at 20 days) the label is **not established**: high band (periods ≤ 20 d) α̂ = 2.83 ± 0.51 (noise-dominated) vs low band 1.18 ± 0.10, z = −3.2.
- **Declared band:** periods ≥ 21 business days (one VIX horizon; the signal dominates the noise there). In-band consistency: periods 21–126 d α̂ = 1.24 ± 0.45 vs > 126 d 1.15 ± 0.30, z = −0.16; in-band corner LR 2.26 < 6.63 (no corner). **Regime B (scale-free over periods 21 d – 37 y), α̂ ≈ 1.2–1.3.**
- **Locked inputs (primary):** in-band Whittle with the noise fixed at the full-band ŝ2 (noise is identified only where it dominates, AQN R2): **α̂ = 1.2587 ± 0.0429, ln q̂ = −1.8116 ± 0.1009, ln ŝ2 = −0.9005 ± 0.1185.** Sensitivity (reported, not decisive): in-band free-noise fit α̂ = 1.190 ± 0.098 (noise term unidentified).
- **MV5 check of N:** own simulation of the Parkinson log-variance floor for a Brownian day (`range_floor.py`): Var = 0.34–0.39 (4000 to 78 intraday steps) vs Whittle ŝ2 = 0.41; |Δ ln| ≤ 0.18.
- **Raw prediction:** survival exponent α̂/2 = 0.63, positive weights.
- **Already seen before lock (declared):** the log-VIX spectrum (AQN demo, repo); in this pick the marginal variance of 2 ln VIX (0.49) vs the variance of the theory forecast on the real driver (0.64), computed to plan the tracker-noise ratio; uninformative (it implies r ≈ 0 only if the forecast slope b = 1). No regression of VIX on the driver was run.

## 3. Numerical checks of the theory kernel (`klib.ok_kernel`, `check_kernel.py/.json`)
The kernel is computed exactly as intrinsic (ordinary) kriging with generalized covariance −½qD1|τ|^{α−1} + nugget ŝ2, target = mean of the next 21 days, weights summing to 1. Checks: (i) against an unconstrained regression on 2.4 M simulated steps (window 40): max |Δw| = 4×10⁻⁴; (ii) survival slope over ages 100–400 in a 2000-day window: −0.64, −0.66, −0.76, −0.89 at α = 1.2, 1.26, 1.5, 1.8 (theory −α/2 = −0.60, −0.63, −0.75, −0.90). Finite windows pile weight at the oldest age, so the per-age weight slope (−1.46 at α = 1.2 vs −1.6) is not a usable statistic; the test compares like with like (§4).

## 4. Design 1 (dropped at MV10, before lock; recorded)
Grid MLE of a kernel family (τ + c)^−(1+s) over ages 0–503 with block bootstrap (`power_sim.py`, `power/`). Failed MV10 in simulation: (a) a flat 1/5/22-day average kernel (R2) gives ŝ ≈ 0.52 vs the theory's pseudo-true 0.58, so the nearest rival gap is ≈ 0.04 (needs 2.8σ); (b) ŝ moves 1.5 per unit α (0.42/0.58/0.72 at α 1.16/1.26/1.36), so α̂'s SE alone gives σ ≈ 0.064; (c) bootstrap sd 0.13 at tracker-noise ratio r = 0.25, 0.29 at r = 0.5.

## 5. Design 2 (locked): survival at one horizon of the binned projection kernel
- **Estimator (`klib.fit_bins`).** OLS of z_t on a constant and bin sums of y over ages [0], [1], [2–4], [5–9], [10–20], [21–41], [42–83], [84–167], [168–335], [336–503] (rows with VIX missing dropped). Per-age weight in bin j = coefficient j; **W21 = (weight on ages ≥ 21) / (total weight)** = the kernel's survival at age 21. Inference: non-overlapping block bootstrap, blocks of 126 rows, 999 reps, seed 20261128.
- **Prediction (like with like):** W21_pred = **0.2770** = mean W21 from the same estimator on 100 simulated planned data sets (n = 9 276) with the driver fBm(α̂, q̂) + noise ŝ2 and a tracker equal to the theory's best linear predictor (2000-day window) with no tracker noise (`power2/H0_0.json`). Direct kernel survival S(21) of `ok_kernel` (504-day window) is 0.301; the binned projection differs by 0.024, hence the simulated value. dW21/dα = −0.601 (sims at α ± 0.1); σ_pred = 0.0264 from the SEs of α̂, ln q̂, ln ŝ2 (0.0258, 0.0035, 0.0045).
- **Named rivals (population W21 from the same estimator):** R1 Kalman/EWMA kernel at α = 2 (exponential forgetting; THEORY: exponential only at α = 2), q matched at lag 21: **0.000**; R2 flat 1/5/22-day averages (a universal short-memory kernel): **0.012**; R3 "matching" power-law kernel with survival exponent α − 1 (c = 21): **0.725**.
- **Decision (`decide.rule`; D = Ŵ21 − W21_pred; σ_D = √(boot sd² + σ_pred²); δ = 0.13):**
  - **PASS** iff |D| + 1.96σ_D ≤ 0.13 **and** the 95% CI of Ŵ21 (±1.96 boot sd) excludes all three rival values.
  - **FAIL** iff |D| − 1.96σ_D > 0.13 (the CI of D lies wholly outside ±0.13).
  - Else **INCONCLUSIVE**; labelled *low resolution* if σ_D > δ/3.24 = 0.040.
  - Label: "passed / failed on proxy 'Parkinson range variance as driver, 2 ln VIX as tracker, survival at 21 business days of the 504-day binned projection kernel'". In-model inputs; field result on proxy; no field kill claimed.
- **Reported, not decisive:** verdict under the free-noise α (W21_pred 0.318, σ_pred 0.059); block length 252; design-1 family ŝ; the tail survival slope from the bins (too noisy to decide: boot sd 0.26 at r = 0.25).

## 6. MV10 gate (`gate.py` → `gate.out`; locked decision code on 100 simulated planned data sets per cell, prediction error N(0, σ_pred) added per rep)
| tracker-noise ratio r (AR(1) φ = 0.95) | P(PASS \| theory kernel) | P(FAIL \| R1) | P(FAIL \| R2) | P(FAIL \| R3) | false FAIL under theory |
|---|---|---|---|---|---|
| 0 | 1.00 | — | — | 1.00 | 0.00 |
| 0.25 | **0.91** | **0.96** | **0.88** | **1.00** | 0.00 |
| 0.35 | 0.76 | — | — | — | 0.00 |
| 0.5 | 0.33 | 0.64 | 0.53 | 1.00 | 0.00 |
| 1.0 | 0.00 | — | — | — | 0.01 |

Each rule fires at its own best-case data (r = 0). Bootstrap CI coverage of W21 under the theory kernel: 0.94, 0.93, 0.95, 0.93 at r = 0.25, 0.35, 0.5, 1.0; bias ≤ 0.007 (`coverage.out`). **Gate met at π = 0.8 for r ≤ 0.25, not at r ≥ 0.35.** r cannot be measured without the outcome, so the lock is **decisive only if the realized σ_D ≤ 0.040** (the MV8(i)/MV10 resolution the gate requires, evaluated on the data; it depends on the noise, not on the mean of D); otherwise the result is exploratory. A FAIL with a larger σ_D is still reported as FAIL (its CI excludes the whole band).

## 7. Limits declared in advance
VIX is a risk-neutral forecast (variance risk premium, time-varying); log of an expectation vs expectation of a log; the proxy omits overnight variance; Gaussian-world premise for the driver not tested (no jump screen); one system; the test is of the linear optimum only and cannot discriminate Bayes vs linear; overlaps QUEUE VIX-KERNEL (which asks for the tail exponent itself; this design shows the exponent is not resolvable here).
