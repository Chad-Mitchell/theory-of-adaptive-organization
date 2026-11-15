# TELEGRAPH-REFEREE — hostile referee of TELEGRAPH-LINEAR-PREMISE (PR #25, CLAIM_MAP N16)

Executor telegraph-referee (for Ace; Chad t1914), Sunday 15 Nov 2026, 11:30–11:48 AM ET (merged as PR #26 at 11:48). Queue pick 7 (unaided slot;
ledger 41–44). **I did not author TELEGRAPH-LINEAR-PREMISE.** All code in `checks/` is mine, written without running or copying the
PR #25 code (I read its REPORT, PREREG and output JSON to know the claims). In-model mathematics only; no field data. THEORY.md not
edited. Compute at `nice -n 19`.

Setting (as in PR #25): y(t) ∈ {+μ, −μ}, switching at rate λ each way (correlation time 1/2λ), observed as ds = y dt + √N dW.
κ = λN/μ². Conti & Mora (C&M) units: μ = 1, λ = 1/(2τ), N = θ, so κ = θ/(2τ) and their α = θ/τ = 2κ.

## 1. Verdicts
| # | Claim (PR #25 / N16) | Verdict | Evidence |
|---|---|---|---|
| V1 | Wonham filter; log-odds form dL = (2μ/N) ds − 2λ sinh L dt | **confirmed** | `symbolic_ref.py` R1–R2 (from the Wonham equation for p, not from C&M) |
| V2 | C&M eq. (20) as printed, read as Itô, omits the drift −x(1−x²)/θ; read as Stratonovich it is the exact filter | **confirmed** | R3: second-order Itô expansion of C&M eq. (11) = Wonham; R4: printed − Wonham = +x(1−x²)/θ, which is exactly the Stratonovich→Itô correction. C&M state "with Itô convention", their FP eq. (31) uses the Itô form, and they integrate with Euler–Maruyama. **Published PRE text (author copy, header "PHYSICAL REVIEW E 106, 054404 (2022)", read) prints the same eq. (20), (36), (41)**; no erratum found (Crossref relation search; web search) |
| V3 | C&M's ln² (eq. 36) is an artifact of V2 | **confirmed, with mechanism** | R5: in L, the printed equation after a switch has drift → 0 at large L (2/θ·(tanh(L/2) − 1)), so the belief escapes by diffusion: time ≈ L*²/σ² = (θ/4)ln²(τ/θ). Deterministic quadrature of the printed equation's mean first passage: 21.3 at τ = 10⁴ (C&M eq. 36: 21.2), 83.2 at τ = 10⁸ (84.8); ln²-coefficient 0.236 over τ = 10…10⁴ |
| V4 | Exact-filter adaptation is single-log, slope θ/2 per e-fold | **confirmed** | Deterministic quadrature (no Monte Carlo) of the mean first passage: slope 0.499θ (τ = 300…10⁴), ln²-coefficient 0.003θ; my own MC (independent discrete HMM filter) agrees with the quadrature (τ = 100: 2.218 ± 0.020 vs 2.217; τ = 10⁴: 4.54 ± 0.03 vs 4.51) |
| V5 | t_A ≈ (θ/2)[ln(4τ/θ) − 0.7] (REPORT §Verdicts P1) | **corrected** | The O(1) constant is **γ + 1 ≈ 1.577**, derived in §2 and matched by quadrature to 4 digits (1.5769 at τ = 10⁴, 1.5773 at τ = 10⁸). PR #25's own MC implies 1.39–1.46 over τ = 10³…10⁴ (its values sit ~2% above the quadrature and my MC, ≈ 3 SE at τ = 10⁴; not a dt effect, its dt/2 rerun is unchanged); "−0.7" matches neither. General units: **t_A = (N/2μ²)[ln(2μ²/λN) − γ − 1] + o(1)** |
| V6 | C&M's own definition (argmax of ⟨y(t₀)x(t₀+t)⟩, eq. 27–28) not simulated (REPORT "Unresolved") | **closed: same single log** | `xcorr_ref.py`: exact filter 1.20, 1.71, 2.29, 2.78, 3.43 at τ = 10, 30, 100, 300, 1000 (within ~0.1 of the first-passage quadrature), ln²-coefficient 0.008; the printed equation gives 2.1…10.1 with ln²-coefficient 0.15 |
| V7 | MSE_B ≈ 2λN ln(2μ²/λN), error elasticity η → 1 in λ and N, 2 − 2η in μ | **confirmed and sharpened; leading order PRIOR ART** | **Exact closed form: MSE/μ² = 2K₀(κ)/(K₀(κ) + K₁(κ))** (§2), = 2κ[ln(2/κ) − γ] + o(κ). Matches quadrature of the density to 6 digits and PR #25's Fokker–Planck values (η = 0.854, 0.879, 0.892 at κ = 9·10⁻⁴, 2.5·10⁻⁴, 1.1·10⁻⁴; mine 0.8543, 0.8792, 0.8908). The −γ explains P2c's ratio 0.92–0.96. Leading order: Khasminskii & Zeitouni 1996 (error probability), Golubev 2000 (MSE), continuous-time form per Chigansky 2005 (§4) |
| V8 | Linear-tracker comparators (MSE_L ≈ 2μ√(λN), memory time √(N/q), q = 4λμ²) | **confirmed** | Riccati steady state, `quad_ref.py` (η_K 0.485–0.495) |
| V9 | Precision-effort elasticities 1/(θp+η), η/(θp+η), 2(1−η)/(θp+η) | **corrected (label)** | These are the elasticities of **precision P**. Effort c·P^θp has θp/(θp+η), θpη/(θp+η), 2θp(1−η)/(θp+η). Identical at θp = 1, so P3's numbers (0.54, 0.46, 0.16) stand |
| V10 | Exact reset reads unaffected (Bayes predictor = linear; MSE = OU's at equal covariance; hold-last-value depends only on the variogram) | **confirmed** | Analytic: E[y(t+s) \| y(t)] = y(t)e^{−2λs}, Markov ⇒ last exact read sufficient; MSE μ²(1 − e^{−4λs}) for both worlds |
| V11 | "Any projection (regression) kernel equals the Kalman kernel, so kernels cannot tell Bayes from linear" (P5, E5, audit of KERNEL-MEASURE / VIX-KERNEL) | **corrected (narrowed)** | True only for a regression **on the tracker's own observations s** (iterated projections). Regressing the output on the **true driver y** (sensing noise unseen by the experimenter, the usual stimulus–response design) has no such identity: `kernel_input_ref.py` (τ = 30, θ = 1, κ = 1/60): Kalman kernel on y matches its analytic form (rel. L2 0.05), the Bayes kernel on y differs from it by rel. L2 **0.61** (peaked at lag ≈ 1, not exponential). Such kernels **can** discriminate Bayes from linear |
| V12 | Elasticities "≈ 0, 1, −2" for t_A | **corrected (quantified)** | With ℓ = ln(2μ²/λN) − γ − 1: elasticities 1/ℓ (switching time), 1 − 1/ℓ (N), −2 + 2/ℓ (μ). At κ = 10⁻³: 0.17, 0.83, −1.67 (linear 0.5, 0.5, −1). The limits are approached only logarithmically |
| V13 | C&M eqs. (41) P_wrong ≈ α/4 and (42) P_wrong,av ≈ (α/8)ln²α (flagged "need re-derivation") | **refuted for the exact filter (new here)** | Both inherit V2. Exact: P_wrong (after the transient) ≈ (α/4)[ln(4/α) − γ] (quasi-stationary law e^{L − κ cosh L}); P_wrong,av = (1 − ⟨x²⟩)/2 = **K₀(α/2)/(K₀(α/2) + K₁(α/2))** ≈ (α/2)[ln(4/α) − γ]. The printed equation reproduces α/4 to 4 digits (`pwrong_ref.py`), so C&M's "agrees very well with the simulation" is a check of the printed equation against itself |

Overall: the premise finding (Bayes ≠ linear exponents in a jump world at the same spectrum; q alone does not set them) and the
C&M diagnosis **stand**; one constant is wrong; one scope claim (projection kernels) is too broad; the error asymptotics and the
single-log form are prior art.

## 2. Derivations (mine)
**Stationary law and exact MSE.** In the observation filtration (innovations dν), dL = [(2μ²/N)tanh(L/2) − 2λ sinh L]dt +
(2μ/√N)dν. The 1-D stationary density is p(L) ∝ cosh²(L/2)·exp(−κ cosh L) (R6). MSE = μ²E[1 − x²] = μ²E[sech²(L/2)], and with
∫e^{−κ cosh L}dL = 2K₀(κ), ∫cosh L e^{−κ cosh L}dL = 2K₁(κ): **MSE = μ²·2K₀(κ)/(K₀(κ) + K₁(κ))**. Small κ: K₀ ≈ ln(2/κ) − γ,
K₁ ≈ 1/κ ⇒ MSE ≈ 2λN[ln(2μ²/λN) − γ].
**Adaptation constant.** Before the switch L has the quasi-stationary law ∝ e^{L − κ cosh L}, so B = (κ/2)e^{L₀} ≈ Exp(1)
(E ln B = −γ). After the switch (y = −μ, θ = 1 units, σ² = 4), the mean first passage to 0 is T(L₀) = ½∫₀^{L₀}dy∫_y^∞
exp[(y − z) − κ(cosh z − cosh y)]dz. With b = (κ/2)e^y the inner integral is e^b E₂(b), and dy = db/b, so
E T = ½[ln(2/κ) − γ − ∫₀^∞(e^{−b} − E₂(b))/b db] = ½[ln(2/κ) − γ − ∫₀^∞E₁(b)db] = ½[ln(4τ/θ) − γ − 1] (using E₂ = e^{−b} − bE₁,
∫E₁ = 1). The noiseless descent alone gives γ + eE₁(1) ≈ 1.17; diffusion adds the rest. Leading-order argument (large-L
approximations), confirmed by quadrature of the exact 1-D problem; not a rigorous proof.

## 3. Prior art (read = text I read this session; restated = read only in a secondary source)
- **Error asymptotics (V7): PRIOR ART.** Khasminskii & Zeitouni 1996 (*Stoch. Proc. Appl.* 63:1–10, doi 10.1016/0304-4149(96)00060-9):
  optimal filtering error probability ≈ (Σᵢμᵢ Σ_{j≠i} λᵢⱼ/D(g_j‖gᵢ)) ε log ε⁻¹ for rare transitions; Golubev 2000 (*Probl. Inform.
  Transmission* 36(3):213–219): the same with weights (aᵢ − aⱼ)² for the MSE. **Restated, not read in full** (paywalled): read in
  Chigansky 2005 (arXiv math/0508446, §1 eq. 1.4–1.5 and §2.2, **read**), which says they hold in continuous time with D replaced
  by (hᵢ − hⱼ)²/2σ² and that weak noise is the same limit with ε = σ². For our case this gives MSE ≈ 2λN ln(1/·) and error
  probability ≈ (κ/2)ln(1/κ): PR #25's leading order exactly. Chigansky also states that for d = 2 the exact stationary density
  of the Wonham filter, hence exact P and E, are known from Wonham 1964 (*SIAM J. Control* 2:347–369, doi 10.1137/0302028) and
  Liptser & Shiryaev, *Statistics of Random Processes* (neither read here). The Bessel closed form 2K₀/(K₀+K₁) and the −γ term
  were **not found stated** in what I read; they are an elementary consequence of the classical density and are probably known.
  Label: DERIVED HERE (likely classical).
- **Single-log adaptation (V4): PRIOR ART in form.** The delay to drive a log-likelihood statistic from a threshold set by the
  change rate down at the KL rate I is the classical quickest-detection asymptotic: Shiryaev's Bayesian problem for a Brownian
  drift change, expected delay ≈ log(1/α)/(I + ρ) with I = r²/2 (Shiryaev 1963; Baron & Tartakovsky 2006, *Sequential Analysis*
  25:257–296, doi 10.1080/07474940600609597, continuous time; Tartakovsky & Veeravalli 2005, *Theory Probab. Appl.* 49:458–497;
  review Tartakovsky & Moustakides 2010, *Sequential Analysis* 29:125–145). **Read only as search-result excerpts** of Baron &
  Tartakovsky and Tartakovsky & Moustakides; Shiryaev 1963 not read. Here I = (2μ)²/2N = 2μ²/N and the "threshold" is the
  posterior's own resting level ln(2μ²/λN), so t_A ≈ ℓ/I. Logarithmic adaptation in this sensory setting: Conti & Mora 2022
  (who print ln²). The two-way-switching version with the quasi-stationary start and the constant γ + 1: not found stated.
- **C&M ln² / α/4 / α ln²α artifact (V2, V3, V13):** not found anywhere (no erratum; no comment found). New, in-model.
- **Iterated projections (V11, narrowed part):** textbook (Wiener/Kalman as the best linear estimator; any L² Bayes estimator
  projects onto it). No novelty.

## 4. Proposed THEORY edits E2′, E4, E5, E6 (referee verdicts; THEORY not edited here)
- **E2′ — accept with changes.** (a) Use the sharpened forms: adaptation ≈ (N/2μ²)[ln(2μ²/λN) − γ − 1], error
  = μ²·2K₀(κ)/(K₀+K₁) ≈ 2λN[ln(2μ²/λN) − γ]. (b) Replace "exponents ≈ 0, 1, −2" with "elasticities 1/ℓ, 1 − 1/ℓ, −2 + 2/ℓ, ℓ =
  ln(2μ²/λN) − γ − 1 (about 0.17, 0.83, −1.67 at λN/μ² = 10⁻³), instead of ½, ½, −1". (c) Credit: "the leading-order error is
  Khasminskii & Zeitouni 1996 / Golubev 2000 (continuous time per Chigansky 2005); the log-threshold-over-KL form of the
  adaptation time is the quickest-detection asymptotic (Shiryaev; Tartakovsky & Veeravalli 2005)". (d) Keep "q alone does not set
  them" (confirmed).
- **E4 — accept**, with the kernel row premise worded as in E5 below (not "any regression kernel").
- **E5 — accept with correction.** Replace "a regression (projection) kernel equals the linear optimum for any stationary world, so
  only transient responses to jumps can tell a Bayes tracker from a linear one" by "a regression kernel **on the tracker's own
  observations** equals the linear optimum for any stationary world; a kernel on the true driver (sensing noise unobserved) and
  transient responses to jumps can tell a Bayes tracker from a linear one". N12 homogeneity caveat: accept.
- **E6 — accept with correction.** "Conti & Mora 2022 (PRE 106:054404) for logarithmic Bayes adaptation to switching; their
  printed eq. (20) read as Itô omits a drift term, so their ln² adaptation (eq. 36), P_wrong ≈ α/4 (eq. 41) and α ln²α average
  error (eq. 42) do not hold for the exact filter, which gives a single log, (α/4)ln(4/α) and K₀/(K₀+K₁)." Add the §3 credits.
- These are wording/credit edits to §2.2, §2.5 and §10, not a rewrite of the headline or core; still for TLP-EDITS-REVIEW (an
  independent reviewer applies them), per Chad t1916.

## 5. Consequences for pending items
- KERNEL-MEASURE, VIX-KERNEL: the PR #25 audit's "OK (cannot discriminate)" holds only if the regressors are the system's own
  inputs. For VIX (implied variance regressed on realized variance) the regressor is neither the market's information set nor the
  latent variance; state which. A kernel on the true driver is a discriminating design (new item KERNEL-INPUT-DISCRIMINATE).
- SAME-SYSTEM-AQN / AQN-ESTIMATORS: NEEDS-PREMISE confirmed; for a jump driver the inputs are λ, μ, N separately.
- GITHUB-UPSTREAM, WIKIDATA-BAND: reset-read verdict (OK) confirmed.
- CM-PUBLISHED-CHECK: done here (published text unchanged; no erratum found).

## 6. Unresolved
- Khasminskii & Zeitouni 1996, Golubev 2000, Wonham 1964, Liptser–Shiryaev and Shiryaev 1963 not read in full (paywalled or not
  located openly); their statements are cited through Chigansky 2005 (read) and search excerpts, labelled so
  (WONHAM-PRIORART-FULLTEXT).
- The γ + 1 constant uses large-L approximations (quadrature-confirmed, not proved). Only the symmetric two-state case.
- Poisson (event) observations of a switching world are not covered (POISSON-SENSING-JUMP); multi-state and 1/f jump worlds
  remain JUMP-STORES.
- V11 is one numerical example (κ = 1/60); the size of the Bayes–linear gap for kernels on y as κ → 0 is not derived.

## Files
`checks/symbolic_ref.py` → `out_symbolic_ref.json` (R1–R6); `checks/quad_ref.py` → `out_quad_ref.json` (closed-form MSE,
elasticities, first-passage quadrature for the exact and printed filters); `checks/mc_ref.py` → `out_mc_ref.json` (seeds 7100+);
`checks/xcorr_ref.py` → `out_xcorr_ref.json` (seeds 7400+); `checks/pwrong_ref.py` → `out_pwrong_ref.json`;
`checks/kernel_input_ref.py` → `out_kernel_input_ref.json` (seed 7300). C&M texts read: arXiv 2011.09958v2 and the author-hosted
published PDF (phys.ens.psl.eu/~tmora/Physique/ContiMora2022.pdf); not stored in the repo.
