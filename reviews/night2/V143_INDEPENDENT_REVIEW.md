# V143-INDEPENDENT-REVIEW — after-the-fact independent hostile review of THEORY v1.4.3 (PR #31)

Executor v143-independent-review (for Ace; Chad t1914, t1916), Sunday 15 Nov 2026, about 12:41–12:55 PM ET (America/New_York). Out-of-cycle maintenance, unscored (ledger entry below). Private repo; nothing posted or sent. **I authored none of PR #31, TELEGRAPH-LINEAR-PREMISE, TELEGRAPH-REFEREE or TLP-EDITS-REVIEW.** PR #31 (merged 12:40 PM ET, main `e8bae15`) was second-checked only by its own applier, so Chad's rule (independent review before theory-core edits merge) was not fully met; this is that review, after the fact. §0, §1 and §2.1 were not edited (HEADLINE-PREMISE-SCOPE / HEADLINE-PREMISE-APPLY). Compute at `nice -n 19`.

Read in full: `git diff 426d062 e8bae15` (all files); `TELEGRAPH_LINEAR_PREMISE/REPORT.md`; `TELEGRAPH_REFEREE/REPORT.md`; `TLP_EDITS_REVIEW.md` (+ checks); CLAIM_MAP N16, N17; `tests/D3_OOS/RESULTS.md`; `PRIORART_LFK_ALPHA/REPORT.md` §4. Primary texts opened this session: Chigansky, arXiv math/0508446 (pdf); Conti & Mora, arXiv 2011.09958v2 (pdf; the published PRE text was **not** read by me).

## 1. Verdict per edit

| Edit (v1.4.3) | Verdict | Notes |
|---|---|---|
| Header, CLAIM_MAP pointer v2.11 | PASS | — |
| §2.2 Regime A parenthetical ("need not give the same Bayes optimum") | PASS | — |
| §2.2 memory-time bullet premise | PASS | Kalman/Wiener bandwidth uses only second moments |
| **E2′** §2.2 Regime A premise bullet | **PASS with one wording fix (F1)** | All numbers re-derived (§2). "They do not describe the Bayes-optimal tracker of a non-Gaussian world" was a universal drawn from one case; now "need not describe ..., and in the one case derived they do not". Credits, read/not-read labels, "derived here, likely classical", "γ + 1 not rigorously proved", reset-read invariance and the two-state-only scope all match the referee |
| **E4** Regime B premises column (read rate, error, precision effort, memory time, kernel) | PASS | Read-rate premise (hold-last-value and optimal *linear* predictor depend only on second moments) is correct and is a fair narrowing of the proposed E4 (TLP_EDITS_REVIEW C1). Kernel-row "own observations" wording matches referee V11 |
| **E5** §2.5 rule premise list + kernel sentence | PASS | Iterated-projection identity correctly restricted to regressions on the tracker's own observations; driver-kernel discrimination stated as one in-model case (κ = 1/60) |
| **E5** §2.5 N12 homogeneity caveat | PASS | Error = μ² f(λN/μ²): ×3.000 under (N, μ²)×3, ×5.97 under (N, λ)×3; the linear tracker's 2μ√(λN) is ×3 under both (my check). "Onset exponent not derived" is honest |
| **E6** §10 credits | **PASS with one notation fix (F3)** | Every citation resolved (§3). The quickest-detection formula wrote the false-alarm level as α, which in this file is the spectral slope; now p_FA |
| §2.4 D3 → N17 pointer | PASS | Matches `tests/D3_OOS/RESULTS.md` (proxy name verbatim, 27/27, 5/5, locked, not refereed, three alternatives not separated) |
| §13 changelog | PASS | Describes the second pass accurately (same executor) |
| Untouched §2.2 Lee, Flack & Krakauer sentence | **inconsistency created by E2′ (F2)** | It said LFK reach τ_E^{1/2} "on a telegraph environment", directly above the new bullet saying the Bayes optimum on that world is a single log. Fixed: the √ form belongs to their learner class (`PRIORART_LFK_ALPHA/REPORT.md` §4) |
| CLAIM_MAP v2.11 note (not THEORY) | **overstatement (F4)** | Said "independently reviewed and second-checked", the wording THEORY's own changelog had already withdrawn (TLP H7). Fixed to say what happened; STATUS line likewise |

Nothing is seriously wrong, so nothing was reverted. All four fixes are wording; no number, status, locked file, result or proof changed.

## 2. Independent numerics (`V143_INDEPENDENT_REVIEW_checks/`; my code, not the referee's or the applier's)
Different routes from the referee where possible: the stationary law is derived in x = E[y|F]/μ from the Wonham SDE dx = −2λx dt + (1−x²)(μ/N)dν, giving ρ(x) ∝ (1−x²)⁻² e^{−2κ/(1−x²)}; the first-passage start law is the **exact** pre-switch law (stationary density × P(y = +|L)), not the large-L approximation e^{L−κ cosh L}; and a full Monte Carlo of the telegraph world with the log-odds filter tests the t_A definition end to end.
- **MSE closed form.** Quadrature of ρ(x) equals μ²·2K₀/(K₀+K₁) to all printed digits at κ = 10⁻¹…10⁻⁴; ratio to 2κ[ln(2/κ) − γ] is 0.993 (10⁻³), 0.999 (10⁻⁴). Elasticity in κ (hence in λ and N): 0.852, 0.879, 0.892 at κ = 10⁻³, 2.5·10⁻⁴, 10⁻⁴ ✔ ("0.85–0.89").
- **t_A constant γ + 1.** Exact-start quadrature, implied constant ln(2/κ) − 2t_A: 1.642, 1.660, 1.603, 1.582, 1.5780, 1.5773 at κ = 5·10⁻², 10⁻², 10⁻³, 10⁻⁴, 10⁻⁵, 10⁻⁶ → γ + 1 = 1.5772 ✔ (the o(1) is visible at κ ≥ 10⁻³, as "+ o(1)" says). Monte Carlo (full world, 38,801 switches, κ = 10⁻², dt = 0.002): t_A = 1.817 ± 0.006 vs quadrature 1.819 ✔. At κ = 0.05, MC 1.007–1.011 ± 0.006 vs 1.024 (the MC drops passages interrupted by a second switch, which biases it low by O(λ·Var T); dt/4 rerun unchanged).
- **Elasticities.** ℓ = 6.0237 at κ = 10⁻³; finite differences of the leading form give 0.1660, 0.8340, −1.6680 = 1/ℓ, 1 − 1/ℓ, −2 + 2/ℓ ✔. The exact-quadrature switching-time elasticity at κ = 10⁻³ is 0.170, so "about 0.17" holds for the exact t_A too.
- **q = 4λμ²**: telegraph spectrum μ²·4λ/(4λ² + ω²) → 4λμ²/ω² ✔. Linear comparators ½, ½, −1 (memory time √(N/4λμ²)) and error ½ (2μ√(λN)) ✔.
- Khasminskii–Zeitouni/Golubev leading term specialised to two states (weights ½, rate λ, (2μ)², KL rate 2μ²/N) gives 2λN·log ✔, matching the credited leading order.

## 3. Citations (resolved this session)
Crossref: Conti & Mora 2022, *PRE* 106(5):054404, "Nonequilibrium dynamics of adaptation in sensory systems" ✔; Khasminskii & Zeitouni 1996, *SPA* 63(1):1–10 ✔; Wonham 1964, *J SIAM Ser A Control* 2(3):347–369 ✔; Shiryaev 1963, *Theory Probab Appl* 8(1):22–46 ✔; Baron & Tartakovsky 2006, *Seq Anal* 25(3):257–296 ✔; Tartakovsky & Veeravalli 2005, *Theory Probab Appl* 49(3):458–497, doi 10.1137/S0040585X97981202 ✔; Tartakovsky & Moustakides 2010, *Seq Anal* 29(2):125–145, doi 10.1080/07474941003740997 ✔. arXiv API: math/0508446 = Chigansky, journal ref *IEEE Trans Inf Theory* 52(9):4267–4272 (2006) ✔; 2011.09958 = Conti & Mora ✔. **Golubev 2000**: not in Crossref; it is reference [6] of Chigansky (read): "G. Golubev, On filtering for a Hidden Markov Chain under square performance criterion, Problems of Information Transmission Vol. 36, No. 3, 2000, pp. 213–219" — matches THEORY's citation; THEORY's label "citation as given by the referee, not resolved" is accurate.
Content checks in texts I opened: Chigansky §2 says (i) for d = 2 the exact P and E follow from the explicitly solvable KFP density (refs Wonham, Liptser–Shiryaev) ✔; (ii) the continuous-time forms hold with D replaced by (hᵢ − hⱼ)²/2σ² and the weak-noise limit is obtained with ε = σ² ✔ (THEORY's "treats the weak-noise case as the same limit" is fair). Conti & Mora arXiv v2 eq. (20) reads dx/dt = −x/τ + ((1−x²)/θ)(y + √θ ξ), stated "with Itô convention"; the exact Itô filter has (1−x²)/θ·(ds − x dt), so the printed form omits −x(1−x²)/θ, which equals the Stratonovich→Itô correction of (1−x²)/θ ∘ ds ✔. I did not read the published PRE text; THEORY attributes that reading to the TELEGRAPH authors and referee, correctly.
Reading labels in §10 are honest (read / restated / search excerpts / not read). No invented citation found. Quickest-detection formula itself (log(1/p_FA)/(I + ρ)) not verified by me beyond the referee's excerpts; labelled so.

## 4. Other checks
- **Novelty:** none overclaimed. The Bessel form and γ + 1 are "derived in this repository ... likely classical"; the C&M artifact is labelled in-model, no erratum found. ✔
- **No "law"**; proxy labels intact ("failed on proxy ..." in the D3 pointer); vigilance not touched (still OPEN). ✔
- **Consistency with untouched §0, status block, §2.1, §1 N6:** they still state the noisy-sensing exponents and the inputs (α, q, N, stakes) without the premise. Conflict noted, not edited; already queued (HEADLINE-PREMISE-SCOPE proposal on main; HEADLINE-PREMISE-APPLY open). One addition for that applier: the status-block "What changed" item 2 ("The square-root memory scaling is Kalman/Muth filtering ... predates Lee, Flack & Krakauer 2024") and the §10 LFK entry ("an application of the α = 2 filtering result") should carry the same learner-class qualifier as F2.
- Store-count row and Regime C: not touched by v1.4.3; open items JUMP-STORES, REGIME-C-GAUSSIAN-PREMISE.

## 5. Fixes applied (THEORY v1.4.3a; this PR)
- F1 §2.2 Regime A premise bullet: "They do not describe" → "They need not describe ..., and in the one case derived they do not."
- F2 §2.2 Regime A, LFK sentence: + "On a telegraph world that √ form belongs to their learner class, not to the Bayes optimum, which adapts on a single log (premise bullet below; `reviews/night2/PRIORART_LFK_ALPHA/REPORT.md` §4)."
- F3 §10 quickest detection: log(1/α) → log(1/p_FA), with a note that it is not the spectral α.
- F4 CLAIM_MAP v2.11 note and STATUS: "independently reviewed and second-checked" → what was done, plus a pointer here.
- Header/changelog v1.4.3a; README and STATUS pointers.

## 6. Unresolved
- Originals of Khasminskii & Zeitouni, Golubev, Wonham, Liptser–Shiryaev, Shiryaev, Tartakovsky et al. not read by me either (WONHAM-PRIORART-FULLTEXT).
- γ + 1 remains a leading-order argument confirmed numerically (now also by an exact-start quadrature and a full-world MC), not a proof.
- §0/§1/§2.1 premise scope: HEADLINE-PREMISE-APPLY (add the LFK qualifier noted in §4).
