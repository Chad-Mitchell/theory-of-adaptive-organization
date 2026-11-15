# TELEGRAPH-LINEAR-PREMISE — prereg (queue pick 6, rule slot; ledger 36–38)

Executor queue-pick6 (for Ace; Chad t1914), Sunday 15 Nov 2026, locked 11:20 AM ET (commit 4d55366; header first said "about 11:40", a typo fixed in the next commit, still before any run), **before any code below was run**.
In-model derivation + numerical checks + a reading audit. No field data. THEORY.md is not edited (Chad t1916); edits are proposed only.

## 1. What is being tested, from the current theory
- **Source (THEORY.md v1.4.2 §2.2, Regime A):** "Examples: a random walk with white increments; a mean-reverting process above its
  corner frequency; switching at one rate. … Memory time τ ∝ (N/q)^{1/2}; one exponential store (the Kalman EWMA)". Regime B table
  rows "Error under noisy continuous sensing", "Precision effort", "Memory time" assume "white observation noise" and (forgetting
  kernel) "linear optimal filter". §2.5 N12: "the error of an optimal linear tracker scales by λ when the drift level and the sensing
  noise are both scaled by λ".
- **Flag (reviews/night2/PRIORART_LFK_ALPHA/REPORT.md §4):** Conti & Mora 2022 (PRE 106:054404; arXiv 2011.09958v2, read) report a
  Bayes-optimal adaptation time that grows logarithmically with τ for a switching (telegraph) world vs √ for OU, at the same
  Lorentzian spectrum. So the §2.2 rows may need the premise "Gaussian world or linear tracker".
- **Regime:** A (α = 2 above the corner; Lorentzian spectrum), Markov, two-state jump world, white Gaussian observation noise.
  Every number below is a regime-A, two-state, in-model statement.

## 2. Exposure declared
Before locking I read C&M's text (eqs. 9–11, 16–23, 27–36, 41–42, App. A) and the earlier in-model check
`reviews/night2/PRIORART_LFK_ALPHA/checks/telegraph_check.json` (correct Wonham filter, θ = 1, rate 1/τ: median crossing time
grew ≈ 0.44 per e-fold of τ over τ = 10…3000). **Reading finding (before any new run):** C&M eq. (20), stated "with Itô
convention", is dx = −x/τ dt + (1−x²)/θ · s dt. Expanding their exact discrete update eq. (11) to second order (Itô) gives an extra
drift −x(1−x²)/θ (the innovation is s − x, not s). Their eq. (31) Fokker–Planck and App. A first-passage (which yields
t_A ≈ (θ/4) ln²(τ/θ), eq. 36) use the drift without that term. Read as Stratonovich, eq. (20) is the correct filter. Hypothesis
H_CM-artifact: the ln² is a property of the printed equation read as Itô, and the exact filter gives a single log.

## 3. Derivation to be checked (mine; leading order, high signal-to-noise κ = λN/μ² ≪ 1)
C&M units: y = ±1 (μ = 1), switching rate λ = 1/(2τ), ds = y dt + √θ dW (N = θ), κ = θ/(2τ).
- Exact filter in full log-likelihood ratio L (x = tanh(L/2)): dL = (2/θ) ds − (1/τ) sinh L dt. At y = +1 the level sits where
  2/θ ≈ e^L/(2τ), L* ≈ ln(4τ/θ). After a switch L falls at speed ≈ 2/θ, so the **mean first-passage time to x = 0 is
  t_A ≈ (θ/2)[ln(4τ/θ) + O(1)]**: slope θ/2 per e-fold of τ; log-log slope on τ → 1/ln(τ/θ) → 0.
  General units: t_A ≈ (N/2μ²) ln(μ²/(λN)) — elasticity ≈ 1 in N (linear tracker ½), ≈ −2 in μ (linear −1), ≈ 0 in τ (linear ½).
- **Error.** Each switch costs ∫(1 + tanh(L/2))² dt ≈ (θ/2)·4·L* = 2θ L*; at rate 1/(2τ): **MSE_B ≈ 2κ ln(2/κ)** (leading order).
  Dimensional analysis (exact): MSE_B = μ² F(κ), so its elasticities in λ and N are equal, η(κ) = dlnF/dlnκ, and in μ it is 2 − 2η.
  Prediction η → 1 (minus 1/ln(1/κ) corrections). Linear Kalman, same spectrum: MSE_L = θ(−1/τ + √(1/τ² + 2/(τθ))) ≈ 2√κ, η = ½.
- **Precision effort** (price c·P^θp, P = 1/N; θp the price exponent): with local η, effort ∝ w^{1/(θp+η)} λ^{η/(θp+η)} μ^{2(1−η)/(θp+η)}.
  Linear (η = ½, θp = 1): w^{2/3} λ^{1/3} μ^{2/3} (= THEORY's w^{2/3} q^{1/3}). Bayes (η → 1, θp = 1): w^{1/2} λ^{1/2} μ^{0}.
- **Pooling-onset sketch (N12), conditional:** if a level's cost is in the power class, onset = −(1−b)/(1−a). With η: shared/private
  ratio ρ in switching **rate** → −(θp+η−ηθp)/η (−(1+θp) at η = ½; **−1 at η = 1**); ρ in **amplitude²** → −(1+θp) at η = 1.
  NOT a derivation for additive shared + private jump drifts (their sum is not two-state); reported as a sketch only.
- **Exact reset reads** (§2.2 read-rate row, §2.5 N7): for a telegraph world E[y(t+s)|y(t)] = y(t)e^{−s/τ}, linear in the read; with
  exact reads the Markov property makes the last read sufficient, so the Bayes predictor equals the linear one and its MSE
  1 − e^{−2s/τ} equals OU's. Hold-last-value MSE depends only on the variogram. ⇒ the reset-read rows and N12's −1 class are unchanged
  by non-Gaussianity here.

## 4. Code (locked with this file; `code/`), seeds, runs
- `symbolic.py` (sympy): S1 Itô map of the LLR SDE to x; S2 second-order continuum limit of eq. (11); S3 Kalman steady state;
  S4 effort and onset elasticities; S5 telegraph conditional mean and MSE.
- `adapt_mc.py` (seed 20261115+i; dt 0.005; 2000 reps; τ ∈ {10, 30, 100, 300, 1000, 3000, 10000}; θ = 1): four filters on common noise —
  F1 exact discrete Bayes (eq. 11, stable tanh addition), F2 exact Wonham Itô SDE in L, F3 C&M eq. (20) as printed (Itô, x-form),
  F4 the printed equation mapped exactly to L. Burn-in 100θ at y = +1, switch, first passage of x below 0, censor 200θ.
  Declared robustness rerun: dt 0.0025, 1000 reps (does not change verdicts unless a primary criterion flips; then reported as fragile).
- `fp_mse.py` (deterministic): stationary Fokker–Planck of the exact filter (Scharfetter–Gummel finite volume, 6000 and 12000 cells),
  MSE_B(κ) for τ ∈ geomspace(30, 3·10⁵, 23); η by centred differences on the 12000-cell solution.
- `mse_mc.py` (seed 20261116+i): Monte Carlo MSE of F1 at τ ∈ {100, 300, 1000}, cross-check of `fp_mse.py`.
- `reset_reads.py` (seed 20261117+j): exact reads every T, T/τ ∈ {0.01, 0.1, 1}, telegraph vs OU, hold-last-value and conditional mean.
- Heavy runs at `nice -n 19`.

## 5. Locked decision rules
**P1 (adaptation time, exact filter F1; primary).**
- P1a: OLS slope of mean first-passage time on ln τ over τ ≥ 300 ∈ [0.40, 0.60]·θ (single log predicts 0.5; C&M eq. 36 predicts
  (θ/2) ln(τ/θ) ≈ 2.9–4.6 over that range).
- P1b: quadratic fit in ln τ over all τ: |coefficient of ln²τ| < 0.05·θ (C&M eq. 36: 0.25).
- P1c: F2 mean within 5% of F1 at every τ (two exact-filter discretisations agree).
- P1e (premise): F1 log-log slope on τ over τ ≥ 1000 < 0.25 (linear tracker: 0.5).
- **Verdict rule:** P1a ∧ P1b ∧ P1c ∧ P1e → "single-log adaptation CONFIRMED in-model; the spectrum does not set the memory-time
  exponent for the Bayes tracker of a two-state jump world". If P1e holds but P1a or P1b fails, report the measured form (e.g. ln²)
  and keep the premise finding. If P1e fails → premise finding NOT confirmed; no E2 premise edit proposed.
- P1d (diagnosis of C&M): F4 ln²-coefficient ∈ [0.15, 0.35]·θ **and** F4 slope over τ ≥ 300 > 1.5·θ → "C&M's ln² reproduced by
  their printed eq. (20) read as Itô, not by the exact filter". F3 reported alongside (x-form Euler near ±1 is less accurate).
**P2 (error, exact filter; fp_mse.py primary, mse_mc.py check).**
- P2a: η_B ∈ [0.75, 1.00) at κ ≈ 10⁻³, 3·10⁻⁴, 10⁻⁴ (nearest grid points), non-decreasing as κ falls; η_K ∈ [0.45, 0.55] there.
- P2b: MC MSE within 10% (or 3 SE) of FP at τ ∈ {100, 300, 1000}; 6000- vs 12000-cell FP within 2%.
- P2c (secondary): MSE_B within 30% of 2κ ln(2/κ) for κ ≤ 10⁻³.
- Kill for the error claim: η_B ≤ 0.6 or ≥ 1.05 at any of the three κ.
**P3 (effort; consistency):** with η_B at κ ≈ 10⁻³ and θp = 1: elasticities w ∈ [0.50, 0.60], λ ∈ [0.40, 0.50], μ ∈ [0, 0.30], and
  w and λ each differ from linear (2/3, 1/3) by ≥ 0.07.
**P4 (reset reads):** telegraph and OU time-averaged MSE equal within 3 SE (hold and conditional mean) at all three T, and each within
  3 SE of the theory value; S5 symbolic identity true.
**S (symbolic):** S1, S2 (second-order term −x(1−x²)), S5 must hold; a failure means my derivation is wrong and is reported first.

## 6. Audit (reading task; rule locked here, files read after this lock)
For each pending item using an event/jump world or a §2.2 noisy-sensing row — GITHUB-UPSTREAM, WIKIDATA-BAND, D3-DISCRIMINATE,
D3-TWO-EXPONENT-OOS, AQN-ESTIMATORS, SAME-SYSTEM-AQN (plus KERNEL-MEASURE, VIX-KERNEL, LAB-AKLMT-TAU, SPF-RIGIDITY-OOS if they apply a
§2.2 row) — record: world type (Gaussian/continuous vs event/jump vs unknown), design quantity, which §2.2 row and optimum it compares
against (linear/second-order vs Bayes), whether the premise is stated. Classes: **OK** (reset reads, second-order-only quantity,
Gaussian world, or no optimum compared), **NEEDS-PREMISE** (a noisy-continuous-sensing row — memory time, error, precision effort,
kernel — applied to an event/jump world without saying linear vs Bayes optimum), **UNCLEAR** (file does not say). Locked tests
are not edited; findings go into items.json notes and the report.

## 7. Outputs
`REPORT.md`, `out_*.json`, CLAIM_MAP: a new row for this item's result (status "PROVED (in-model, self-checked; not refereed)" or as the
verdicts dictate); N11 premise text already states the premise. Proposed THEORY edits in the report only + a queue item for
independent review. Field results: none.

## Amendment 1 (dated 15 Nov 2026, ~11:35 AM ET; after P1–P4 outputs were seen, before this check was written or run)
Added because the audit (§6) raised a measurement question: does a *linear-regression* (projection) kernel of a Bayes-optimal
tracker look like the linear optimum? Identity (law of iterated projections): for a stationary world, the best linear projection of
the Bayes estimate E[y_t | s_{≤t}] onto the past observations equals the projection of y_t itself, i.e. the Kalman/Wiener estimate.
**P5 (`code/linproj.py`, seed 20261118):** τ = 100, θ = 1, dt = 0.01, 64 paths × 400τ. Regress (i) F1's output x̂ and (ii) the true y on
80 lagged bins of observation increments (width 0.5); compare with the analytic Kalman kernel g·e^{−βu} (β = √(1/τ² + 2/(τθ)),
g = P/θ). Pass: relative L2 difference ≤ 0.10 between (i) and (ii), and between (i) and the Kalman kernel. Consequence if it passes:
a projection kernel cannot tell a Bayes from a linear tracker; only transient (switch-triggered) responses can. This amendment does
not change P1–P4 rules or verdicts.
