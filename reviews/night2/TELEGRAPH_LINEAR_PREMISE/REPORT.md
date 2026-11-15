# TELEGRAPH-LINEAR-PREMISE — report (queue pick 6, rule slot; ledger 36–39)

Executor queue-pick6 (for Ace; Chad t1914), Sunday 15 Nov 2026, 11:14 AM–about 11:30 AM ET. Prereg, code, seeds and decision
rules locked in commit 4d55366 (11:20 AM ET) before any run; amendment 1 (P5) committed before P5 was written or run. **In-model only.
No field data. THEORY.md not edited.** Verdicts are computed from the outputs by `code/verdicts.py` → `VERDICTS.json`.
Not independently reviewed (TELEGRAPH-REFEREE queued).

## Source and regime (THEORY.md v1.4.2)
§2.2 Regime A lists "switching at one rate" as an α = 2 example with "Memory time τ ∝ (N/q)^{1/2}; one exponential store (the Kalman
EWMA)"; the Regime B rows for error, precision effort, memory time and kernel assume white observation noise and (kernel row) a
"linear optimal filter"; §2.5 N12 rests on "the error of an optimal linear tracker scales by λ when the drift level and the sensing
noise are both scaled by λ". Regime here: **A** (Lorentzian spectrum, α = 2 above the corner), two-state Markov jump world,
white Gaussian sensing noise, high signal-to-noise κ = λN/μ² ≪ 1. Flag from `reviews/night2/PRIORART_LFK_ALPHA/REPORT.md` §4.

## Verdicts (all locked rules met)
| Rule | Result | Verdict |
|---|---|---|
| S1, S2, S5 (sympy) | Itô map of the exact LLR filter and the 2nd-order limit of C&M eq. (11) both give drift −x/τ − x(1−x²)/θ; telegraph E[y(t+s)\|y(t)] = y(t)e^{−s/τ} | pass |
| P1a slope of mean adaptation time on ln τ (τ ≥ 300), exact filter F1 | 0.508 θ (dt/2 rerun 0.508); band [0.40, 0.60]; C&M's ln² would give 2.9–4.6 | pass |
| P1b ln²τ coefficient, F1 | 0.0045 θ (rerun 0.0026); need \|c\| < 0.05 | pass |
| P1c two exact discretisations (F1 discrete Bayes, F2 Wonham SDE) | max difference 0.24% | pass |
| P1e log-log slope on τ (τ ≥ 1000), F1 | 0.129 (linear tracker 0.5) | pass |
| **P1 verdict** | **single-log adaptation CONFIRMED in-model**: t_A ≈ (θ/2)[ln(4τ/θ) − 0.7] over τ = 10…10⁴ | |
| P1d C&M eq. (20) as printed, read as Itô (F4 exact map; F3 Euler) | ln² coefficient 0.192 θ (rerun 0.237; F3 0.202/0.250); slope 3.36 θ; at τ = 10⁴ F4 gives 20.5 vs C&M eq. (36) (θ/4)ln²(τ/θ) = 21.2 | pass: **C&M's ln² is reproduced by their printed equation and not by the exact filter** |
| P2a error elasticity η_B (= in λ and in N, exactly, by dimensional analysis) | 0.854, 0.879, 0.891 at κ ≈ 9·10⁻⁴, 2.5·10⁻⁴, 1.1·10⁻⁴ (rising to 0.924 at κ = 1.7·10⁻⁶); linear 0.485–0.495 | pass (kill not triggered) |
| P2b Monte Carlo vs Fokker–Planck MSE (τ = 100, 300, 1000); grid doubling | −2.4%, −3.0%, −0.8% (\|z\| ≤ 1.3); grid 5·10⁻⁶ | pass |
| P2c MSE_B vs 2κ ln(2/κ), κ ≤ 10⁻³ | ratio 0.92–0.96 | pass |
| P3 precision-effort elasticities at κ ≈ 10⁻³, price ∝ precision (θp = 1) | stakes 0.54, switching rate 0.46, amplitude 0.16 (linear 2/3, 1/3, 2/3) | pass |
| P4 exact reset reads, telegraph vs OU (same covariance), T/τ = 0.01, 0.1, 1 | all \|z\| ≤ 1.1 (hold-last-value and conditional mean) | pass: **reset-read rows unchanged** |
| P5 (amendment 1) projection kernel of the Bayes tracker vs true-y projection vs analytic Kalman kernel | relative L2 0.3% and 0.4% | pass: **a regression kernel cannot tell a Bayes tracker from a linear one** |

## What this establishes (in-model, regime A, two-state jump world, white Gaussian noise; self-checked, not refereed)
1. **The premise is real and sharper than flagged.** At the same spectrum the Bayes-optimal tracker and the best linear tracker have
   different exponents for every *noisy-continuous-sensing* design quantity:
   - adaptation (memory) time after a switch: Bayes ≈ (N/2μ²)·[ln(2μ²/λN) + O(1)] — elasticity ≈ 0 in the switching time, ≈ 1 in N,
     ≈ −2 in μ; linear ∝ (N/q)^{1/2} = √(N/4λμ²) — ½, ½, −1;
   - error: Bayes MSE ≈ 2λN ln(2μ²/(λN))·(1 + O(1/ln)) [= μ²·2κ ln(2/κ)], elasticity η → 1 in λ and N, 2 − 2η → 0 in μ;
     linear ≈ 2μ√(λN), elasticities ½, ½, 1;
   - precision effort (price ∝ precision^θp): stakes 1/(θp+η), rate η/(θp+η), amplitude 2(1−η)/(θp+η) (S4) — at θp = 1 about ½, ½, 0
     for Bayes vs ⅔, ⅓, ⅔ linear.
   The spectrum level q = 4λμ² is a sufficient input for the linear tracker but **not** for the Bayes tracker, which needs the jump rate
   λ and amplitude μ separately. So "the spectrum sets the exponents" holds for Gaussian worlds (where Bayes = linear) or for the
   best linear tracker in any world (only second moments enter), not for the Bayes optimum in a jump world.
2. **What does not change.** (a) Exact reset reads: for a telegraph world the last exact read is sufficient and the conditional mean is
   linear in it, so the Bayes predictor equals the linear one and the MSE equals OU's at the same covariance (S5, P4); hold-last-value
   depends only on the variogram in any world. The §2.2 read-rate row, N7's a = b = 1/α at α = 2 and N12's −1 reset class survive here.
   (b) Any *projection* (regression) kernel: by iterated projections it equals the Wiener/Kalman kernel whether the system is Bayes or
   linear (P5). A kernel test therefore compares with the linear optimum and is valid as such, but cannot discriminate the two;
   only transient, switch-triggered responses (adaptation time after a jump, its N- and μ-elasticity) can.
3. **Conti & Mora 2022's ln² (their eq. 36, t_A ∼ (θ/4) ln²(τ/θ)) does not hold for the exact filter.** Their eq. (20) is stated
   "with Itô convention" but omits the drift −x(1−x²)/θ that the Itô limit of their own exact eq. (11) contains (S2); read as
   Stratonovich it would be correct. Their eq. (31) Fokker–Planck and App. A use the incomplete drift. The printed equation
   reproduces their ln² numerically (F3/F4); the exact filter (two independent discretisations) gives a single log. Their qualitative
   statement ("logarithmic", sublinear in τ, faster than OU in the efficient regime) stands; the ln² form and the α ln²α error term
   (their eq. 42) need re-derivation with the full drift. **Caveats:** arXiv v2 text read via pdftotext; the published PRE version
   (106:054404) not read and may differ; my t_A is the mean first passage of the posterior mean to 0 (the quantity their App. A
   computes), not their argmax-cross-correlation definition (eq. 28), which was not simulated. Not refereed.
4. **Earlier statements this corrects (inside the repo).** `PRIORART_LFK_ALPHA/REPORT.md` §4 and CLAIM_MAP N11 say "∝ ln τ (Conti &
   Mora 2022)": the single log is right, but C&M's own formula is ln²; credit should read "logarithmic (Conti & Mora 2022; single
   logarithm for the exact filter, this repo)". The earlier `telegraph_check.py` slope 0.44/e-fold (θ = 1, rate 1/τ, prediction 0.5)
   is consistent.
5. **Pooling onset (N12) in jump worlds — sketch only, not derived.** If a level's cost stayed in the power class with local η, the
   onset exponent would be −(θp + η − ηθp)/η when the shared/private ratio ρ is a ratio of switching rates (−1 at η = 1 for any θp),
   and −(1+θp) when ρ is a ratio of squared amplitudes (S4). Additive shared + private jump drifts are not a two-state world, so this
   is a hypothesis for a new item (JUMP-WORLD-ONSET), not a result.

## Audit of pending tests (locked rule, PREREG §6)
| Item | World / design quantity | Optimum compared | Class | Note |
|---|---|---|---|---|
| GITHUB-UPSTREAM (active; locked) | binary weekly CI state (jump world); cron read rate; reset reads (class R) | read-rate row, a = b = 1/(1+2Ĥ) | **OK** on linear-vs-Bayes (exact reset reads) | **Separate measurement flag:** the addendum's Ĥ is an Allan-factor exponent of the *change-count* process; the read-rate row needs the *variogram* exponent of the target, P(state differs at lag s), near the read interval. These coincide for fBm-type continuous targets, not in general for a binary target (a finite switching rate makes P(differ) ∝ s at short lags whatever the clustering). Locked files not touched; noted in items.json; GITHUB-VARIOGRAM-CHECK queued as a post-lock descriptive check |
| WIKIDATA-BAND (active; locked) | value replacements (jump world); freeze/hold/lookup modes; reset reads | signs/orderings in T8's power class | **OK** | Its error-growth object for non-quantity types, −ln(1 − P(any change within τ)), is a variogram-type quantity; signs hold for every H (its §2b) |
| D3-DISCRIMINATE, D3-TWO-EXPONENT-OOS | event series; hazards vs spectra | none (renewal vs Cox discrimination) | **OK** (no optimum) | — |
| AQN-ESTIMATORS | estimators of α, q, N, incl. event worlds | feeds §2.2 rows | **NEEDS-PREMISE** | For event/jump worlds also estimate jump rate λ and amplitude μ separately (q = 4λμ² is not sufficient for the Bayes optimum), and state which optimum the estimate feeds |
| SAME-SYSTEM-AQN | one real system; read rate / memory time / store count | §2.2 optimum | **NEEDS-PREMISE** | Lock linear vs Bayes optimum before data; if the driver jumps, the discriminating design quantity is switch-triggered adaptation time (Bayes ≈ (N/2μ²) ln(2μ²/λN), linear √(N/q)); a regression kernel equals the linear optimum either way (P5) |
| KERNEL-MEASURE | response kernel on one system | kernel row (linear filter) | **OK if** the kernel is a projection/regression kernel; **NEEDS-PREMISE** if it is a step or impulse response to discrete events | — |
| VIX-KERNEL | regression kernel of implied on past realized log-variance | kernel row | **OK** (projection kernel = Wiener kernel even for a Bayes market, P5) | Cannot discriminate Bayes vs linear |
| LAB-AKLMT-TAU | Gaussian AR(1), known DGP | Kalman | **OK** | — |
| SPF-RIGIDITY-OOS | macro forecasts; noisy-information CG coefficient | Gaussian noisy-information filter | **OK** (premise implicit: Gaussian) | State the Gaussian premise in its prereg |

## CLAIM_MAP (my item's row only)
New row **N14** (v2.7), status **PROVED (in-model)** with qualifier "leading order + numerics; self-checked; not refereed": items 1–3
above. No existing row's status changes. N11's evidence text gets a pointer (premise wording unchanged).

## Proposed THEORY.md edits (NOT applied; independent review first, Chad t1916; queue TLP-EDITS-REVIEW)
- **E2′ (replaces E2 of PRIORART_LFK_ALPHA):** §2.2 Regime A, memory-time bullet → "Memory time τ ∝ (N/q)^{1/2}, one exponential store
  — for a Gaussian world, or for the best linear tracker in any world (only second moments enter). For a world that switches between
  two levels ±μ at rate λ, sensed in white noise of density N with λN/μ² ≪ 1, the Bayes-optimal tracker adapts after a switch in
  ≈ (N/2μ²) ln(2μ²/λN) and its error is ≈ 2λN ln(2μ²/λN): exponents ≈ 0, 1, −2 in switching time, noise and amplitude instead of
  ½, ½, −1, and q alone does not set them (`reviews/night2/TELEGRAPH_LINEAR_PREMISE/`, in-model, CLAIM_MAP N14). Logarithmic
  adaptation: Conti & Mora 2022 (who give ln²; the exact filter gives one log, this repo)."
- **E4:** Regime B table, "Premises" column of the error, precision-effort, memory-time and kernel rows: add "Gaussian world, or the
  best linear tracker". Read-rate row: add "exact reads: hold-last-value depends only on the variogram, so the row holds in any world
  with that variogram; for the optimal predictor, also in Markov worlds whose conditional mean is linear in the last read (e.g.
  two-state switching)".
- **E5:** §2.5 binding premise list ("exact vs noisy reads; predictor class; …"): add "linear vs Bayes optimum, for non-Gaussian
  worlds; a regression (projection) kernel equals the linear optimum for any stationary world, so only transient responses to jumps
  can tell a Bayes tracker from a linear one". §2.5 N12 bullet: add "The degree-1 homogeneity holds for linear trackers; for the Bayes
  tracker of a jump world the error depends on rate and amplitude separately and the onset exponent is not derived (JUMP-WORLD-ONSET)."
- **E6:** §10 credit: Conti & Mora 2022 (PRE 106:054404) for logarithmic Bayes adaptation to switching, with the ln² caveat above.

## New queue items (rationale in items.json)
TELEGRAPH-REFEREE (w 3), TLP-EDITS-REVIEW (w 2), JUMP-WORLD-ONSET (w 2), JUMP-STORES (w 2), GITHUB-VARIOGRAM-CHECK (w 2),
CM-PUBLISHED-CHECK (w 1). Notes added to AQN-ESTIMATORS, SAME-SYSTEM-AQN, KERNEL-MEASURE, GITHUB-UPSTREAM, SPF-RIGIDITY-OOS.

## Unresolved
- Not refereed. Leading-order formulas are asymptotic arguments checked numerically, not proofs; the O(1) constant (−0.7 in t_A) is
  measured, not derived.
- Only the two-state, symmetric, white-Gaussian-noise case. Multi-state, asymmetric, Poisson-observation (event-sensing) and
  power-law jump worlds (e.g. superpositions of switches giving 1/f spectra) are not done; store counts under Bayes tracking are set by
  the sufficient-statistic dimension, which is not derived beyond one dimension here (JUMP-STORES).
- C&M's published text not read; their cross-correlation adaptation time not simulated.
- No literature search for prior statements of the single-log Wonham adaptation time or the 2κ ln(2/κ) error asymptotics; asymptotic
  Wonham-filter error results are believed to exist in the filtering literature but were **not read here and are not cited**
  (TELEGRAPH-REFEREE should search). Novelty of items 1–2: not claimed.
