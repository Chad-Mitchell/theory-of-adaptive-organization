# End-of-day synthesis — 15 November 2026

**As of:** Sunday 15 November 2026, about 8:25 PM ET (America/New_York). **Stamped against:** `THEORY.md` v1.4.17 and `measurement/CLAIM_MAP_v2.md` v2.37 on main (`000a9a8`, PR #74, merged about 8:19 PM ET). If `git log -1 -- THEORY.md` is newer than this stamp, reread THEORY.md and STATUS.md before trusting anything here.

This is a plain-language account of where A Theory of Adaptive Organization (GTAO) stood at the end of the day's work. Every claim points to a file in this repository. Call it a **theory**, not a law. Field and proxy results are labelled "passed / failed on proxy X". Nothing here is a field confirmation or a field kill. Vigilance (H8) stays **OPEN**. The repository is private; nothing was posted or sent.

Canonical pointers: `THEORY.md`, `STATUS.md`, `QUEUE.md`, `measurement/CLAIM_MAP_v2.md`, `measurement/FRAMEWORK.md`.

---

## 1. What is proved (in-model math)

These are theorems or derived relations inside the model. They are not claims about nature.

- **The tracking layer is classical.** The map from a world's spectral slope α (with drift level q, sensing noise N and stakes) to read rate, precision effort, memory time, forgetting kernel and number of stores is optimal filtering and approximation theory plus a price on effort, credited and refereed (`reviews/night2/SPECTRUM_MAP_REFEREE.md`; THEORY §0, §2.2, §10). It is no longer the headline. The open bet is empirical (CLAIM_MAP N13, J6).
- **Those noisy-sensing exponents hold for a Gaussian world, or for the best linear tracker.** For the Bayes tracker of a two-state switching world, jump rate and jump size enter separately, and adaptation time is a single logarithm (`reviews/night2/TELEGRAPH_LINEAR_PREMISE/REPORT.md`, refereed in `reviews/night2/TELEGRAPH_REFEREE/REPORT.md`; CLAIM_MAP N16, MATH-CORRECTED; THEORY v1.4.3). On a sampled grid, t_A picks up a term that approaches −ζ(½)/√(2π) ≈ 0.58 only as κ → 0 (`reviews/night2/DISCRETE_TA/REPORT.md`, `reviews/night2/DISCRETE_TA_N16_REVIEW.md`; THEORY v1.4.9).
- **Pooling-onset exponents do not depend on α** for the sensing technologies in §2.2, under stated premises (same α for shared and private drift; exact reads at the level): −1 for exact reset reads, −(1+θ) for precision priced ∝ precision^θ (CLAIM_MAP N12, MATH-CORRECTED; `reviews/night2/N12_REFEREE.md`). Vigilance growth, the mixed-technology private-drift exponent and the constants do depend on α. With noisy member reads the onset collapses to N\*ρ = X_α(σ²/ρ); a noise-limited level is the θ = 1 class (exponent −2 at every α); the crossover is ρ_c = σ² C_α α^{−α/(α−1)}, about 27√2/8 σ² at α = 2, with the assumed asymptote now derived from the Kolmogorov–Szegő formula (`reviews/night2/ONSET_NOISY_READS/REPORT.md`, `reviews/night2/ONSET_NOISY_READS_REVIEW.md`; THEORY v1.4.11).
- **Store count.** Finitely many exponential stores are exact iff the spectrum is rational; otherwise the number grows with span and with stakes over upkeep. One store suffices, to leading order near α = 2, iff ψ·c(α−2)² ≲ 1, where c is set by span and store model, not a universal constant (largest found ≈ 0.18 with no free short-lag memory; smaller with free taps or a short span) (`reviews/night2/STORE_COEF_REVIEW.md`; THEORY v1.4.8; CLAIM_MAP K12, MATH-CORRECTED).
- **Formal layer** (sensing classes, pooling onset, vigilance, ordering, freeze/hold/lookup band): proved in-model, with corrections. At zero upkeep the onset vigilance value is 1 + (1+ρ)^{−1/2}, between 1 and 2; the earlier "≥ 2" is wrong as stated (THEORY status block; `reviews/night1/formal/`).
- **The loss is an input of the optimum**, like α, q, N and w. Every §2.2 row is computed for squared error. Under |e|^p and Gaussian errors, reset-read elasticities are a_p = 2/(2+p(α−1)) in stakes and b_p = p/(2+p(α−1)) in q, so **a = b = 1/α only at p = 2**. The §2.5 bridge is that p = 2 case. Precision-effort elasticities likewise change with p. Independently re-derived (sympy; precision by quadrature at α = 1.5, 2, 2.5, within 10⁻⁵). In a Gaussian world the linear filter at a given noise level is loss-free (Sherman 1958, abstract read); the chosen noise level still moves with p. In the two-state world the best linear tracker depends on the loss (next section). Under bundled decisions, formal Theorem 4 keeps the level's squared-error onset exponent; at α = 2 the separable reset-read onset is already −2/p. (`reviews/night2/PREREG_LOSS_LOCK.md`, `reviews/night2/PREREG_LOSS_LOCK_REVIEW.md`; THEORY v1.4.16.)
- **Bayes and linear optima in the telegraph world separate only through κ = λN/μ²** (and λΔ on a sampled grid). A change at fixed κ moves both alike (`reviews/night2/CAUSAL_NULL_INVARIANCE.md`, `reviews/night2/CAUSAL_NULL_INVARIANCE_REVIEW.md`; THEORY v1.4.15).

---

## 2. What passed on which proxy, and how strongly

No field test measured GTAO's quantities validly, so nothing is confirmed in the field (`measurement/FRAMEWORK.md`; THEORY status block). These are the locked or refereed passes, with their strength.

- **KERNEL-MEASURE** — **passed on proxy "VIX vs range (Parkinson) variance", exploratory.** Survival at 21 business days Ŵ21 = 0.260 ± 0.041 vs the linear-optimum like-with-like prediction 0.277; three named rival kernels excluded. Realized resolution 0.049 > the locked 0.040 decisive bar, so it is not certified. Independent review reproduced the numbers and corrected the author's free-noise "inconclusive" sensitivity: a consistent joint refit keeps the prediction at 0.276–0.278, so neither the noise treatment nor the band choice decides the verdict (`tests/KERNEL_MEASURE/RESULTS.md`; `reviews/night2/KERNEL_MEASURE_REVIEW.md`; THEORY v1.4.10; CLAIM_MAP v2.28). The VIX-free kernel of the realized 21-day mean log range variance has the same survival (0.259 ± 0.058 vs 0.258 like-with-like): **passed on proxy, exploratory**; proxy distortions of the shape statistic were **consistent, not certified** (MV10 not met for a certification). The gain deficit is post hoc and target-dependent (`reviews/night2/KERNEL_PROXY_REVIEW.md`, `reviews/night2/KERNEL_PROXY_REVIEW2.md`; THEORY v1.4.13; CLAIM_MAP v2.31). K13 stays MATH-CORRECTED; N13 stays OPEN. This is the first measured tracking kernel in any GTAO test, on one system, for the linear optimum, and not a Bayes-vs-linear test.

- **ONSET-ACROSS-ALPHA-SIM** — **passed in-model, on proxy "learned reset-read pooling onset in simulated fBm worlds".** Reset-read exponents −0.950 (α = 1.5) vs −0.937 (α = 2.5), Δ = +0.013 [−0.072, +0.118] inside the locked ±0.267 margin; the informative 95% bound is |Δ| ≲ 0.13 (a 1/α-sized movement is excluded, not every α-dependence). Independent code (Cholesky fBm; ES and grid learners) replicates (ES PASS; grid INCONCLUSIVE at the locked 16 seeds, PASS at 48 seeds, post hoc) (`tests/ONSET_ACROSS_ALPHA/RESULTS.md`; `reviews/night2/ONSET_ACROSS_ALPHA_REVIEW.md`; THEORY v1.4.14; CLAIM_MAP v2.33). N12 stays MATH-CORRECTED. In-model only; reset reads only.

- **CAUSAL-NULL-INVARIANCE** — **passed in-model, on proxy "MSE-payoff-selected learners, zero-crossing t_A on a Δ = 0.01 grid".** Locked D = +0.290 ± 0.029, above the κ_F = ½ kill line 0.175 (MV10 met). Independent re-implementation, seven replicates: D = 0.347 ± 0.012, all passed. This survives the mirrored pass rule of v1.4.17 (D − 1.96σ still clears the kill line). It shows that, under a squared-error payoff, selection can reach the Bayes adaptation-time response; the family contained the Bayes filter, so the informative part of the pick is the loss-dependence result, not the pass itself (`reviews/night2/CAUSAL_NULL_INVARIANCE.md`, `reviews/night2/CAUSAL_NULL_INVARIANCE_REVIEW.md`; THEORY v1.4.15; CLAIM_MAP v2.34). N16 stays MATH-CORRECTED.

- **LAB-AKLMT-TAU (CLAIM_MAP N23)** — **passed on proxy "implied persistence of h = 1 lab forecasts, AKLMT Exp 1 (MTurk)", weak, at the boundary; not refereed.** D = 0.518 ± 0.048 against a predicted move 0.984 and kill line 0.492. Participants move 53% of the feasible OLS learner's move (CI [0.43, 0.62]), about 10 SE below 1, and their level at ρ = 0 is 0.45 against an optimum of 0.02. The locked rule required only a direction established and a kill not fired. MTurk participants in a short novel task are not a strongly selected system, so N23 cannot move N6. N11's τ_E slope was inapplicable (innovation sd fixed, exact reads). Under the mirrored pass rule the same numbers would read **inconclusive** (report-only; the locked PROXY-PASS stands) (`tests/LAB_AKLMT_TAU/RESULTS.md`; `reviews/night2/CAUSAL_KAPPA_LENIENCY.md`; CLAIM_MAP v2.35, v2.37).

- **STAKES-REFEREE R-EIV** — **passed on proxy "CAISO night-hour k_lin, ACTUAL vs RTD reference error".** About 79% of N21's all-hours log gap closes at night, when there is no behind-the-meter solar. N21's "stakes moved about 4×" reading is withdrawn. N21 and N22 themselves stay **INCONCLUSIVE** (`reviews/night2/STAKES_REFEREE.md`; CLAIM_MAP v2.32).

- **Earlier, still standing, and weaker or non-discriminating.** WIKIDATA-BAND P4 passed on proxy (4/4 wikis; known-groups check failed; P1–P3 inconclusive; N20 PROXY-PASS, weak). Locked D3S and D3-OOS's original statistics passed on proxy "binary daily edit series" but are non-discriminating. VIGIL_ONA's direction passed on nomination-network proxies and was downgraded by a blind referee; vigilance stays OPEN. LEARNSIM's RA mixed arm and class-R vigilance at onset were locked-rule in-model passes; the overall T1.8 test was **not passed** (AR inconclusive on MV8). Under a CI-inside-band (TOST) re-read, those LEARNSIM passes would read inconclusive; that re-read is report-only and does not move CLAIM_MAP G26/G27 (`reviews/night2/PASS_RULE_SYMMETRY_AUDIT.md` §5; `reviews/night2/LEARNSIM_REFEREE.md`).

---

## 3. What failed on proxy

- **P1** failed on proxy "headline-word recurrence as need" (0.32, CI 0.29–0.35, vs a predicted 0.5–1.2) (THEORY status block; CLAIM_MAP H1).
- **Enron rank vs external mail** failed on proxy "external share of received mail" (THEORY status block).
- **GITHUB-UPSTREAM** failed on proxy "weekly CI-state change rate vs nominal cron reads/week" (b̂ −0.06 [−0.24, 0.17], â −0.10 [−0.17, −0.04]); Tier 3 because the drift instrument failed MV5, MV7(i) and MV8(ii) (`night2/GITHUB/RESULTS.md`; CLAIM_MAP N14–N15).
- **D3-OOS:** pure renewal **failed on proxy** (27/27 new GitHub repos and 5/5 Wikipedia groups); Cox vs Hawkes vs trend unresolved (`tests/D3_OOS/RESULTS.md`; CLAIM_MAP N17).
- **SPF-NOISE-PROXY:** LFK's dispersion-as-N **failed on proxy "horizon overidentification"** for 6 of 7 variables; the post hoc S-a closeness was an artifact of that proxy (`tests/SPF_NOISE_PROXY/RESULTS.md`; `reviews/night2/NOISE_PROXY_REFEREE.md`).
- **MEASURE-SELF:** √ allocation failed on a statement-time proxy with its premise unmet (STATUS).
- **In-model simulation failures** (not field): six earlier locked predictions failed (SENSING class R, SENSING2's risky world, three in ANTS1, LAYERS1 P2); LEARNSIM T1.8 was not passed (THEORY status block; CLAIM_MAP G23–G29).

Several other locked tests were **inconclusive** or never locked because a gate was not met: STAKES-EXOGENOUS (N21) and STAKES-SHIFT-CAISO (N22) on CAISO proxies; LFK-ALPHA-SPF primary; SPF-RIGIDITY-OOS (MV10 not met); ONA-MORE (no qualifying public dataset); C3b (MV10 not met at any reachable n).

---

## 4. What is open (vigilance stays OPEN)

- **The open bet is untested:** once α, q, N and stakes are measured on the same system, real systems sit near the §2.2 optima, with the same relations at every scale (CLAIM_MAP N13, J6; THEORY §1 N6). No system has had all four inputs measured validly. N6's causal form is also untested on a strongly selected system (N22 inconclusive; N23 cannot move N6).
- **Vigilance (H8) is OPEN.** No valid field measurement; VIGIL_ONA was downgraded; ONA-MORE did not find data.
- **Nothing is confirmed or validly refuted in the field.** Kernel and lab results are on named proxies, and the kernel pass is exploratory.
- Queued sibling rule work, not yet theory text: HIT-ZERO-MISS-FLOOR, RELATIVE-BAND-TOST, CAUSAL-OVER-RESPONSE, LOSS-SENSITIVITY-REPORT (`QUEUE.md`; `reviews/night2/PASS_RULE_SYMMETRY_AUDIT.md`; `reviews/night2/CAUSAL_KAPPA_LENIENCY_REVIEW.md`; `reviews/night2/PREREG_LOSS_LOCK_REVIEW.md`).

---

## 5. What the reviewers corrected

Every core, premise, kill, headline or math edit to THEORY today went through a separate reviewer (Chad t1916) and landed as PASS-WITH-FIXES. The substantive corrections:

- **PREREG-LOSS-LOCK (PR #73 → v1.4.16).** The author's "about zero" squared-error move was wrong: with the output scale free, the squared-error-best one-pole tracker *is* the Kalman filter and moves **Δln t_A = −0.068**, slightly the wrong way. The absolute-error-best one-pole tracker moves **−0.225** (author Monte Carlo −0.19), opposite Bayes (+0.354). The sign-payoff one-pole value +0.318 (90% of Bayes) was confirmed on an independent exact grid. Scope fixes: "in any world" became "Gaussian errors"; unnamed loss defaults to squared error; the new requirements bind preregs locked after v1.4.16 and do not relabel earlier verdicts; at α = 2 the separable reset-read onset is already −2/p, not "not derived"; Theorem 4's H3 for reset reads in fBm needs p > 2(α−2)/(α−1). (`reviews/night2/PREREG_LOSS_LOCK_REVIEW.md`.)
- **CAUSAL-KAPPA-LENIENCY (PR #74 → v1.4.17).** Mirror PASS confirmed. Wrong-pass rates 48–83% under the old rule fall to ≤ 1% at true share 0.40, and to the one-sided 2.5% size as the share approaches κ_F. The old PASS and FAIL regions overlap (FAIL's precedence decided the label in those draws). The "no power cost" claim holds for a known scaled prediction; with s·λ plug-in error the PASS leg can bind, so MV10's simulation route must check both legs. A passed result whose share interval lies wholly below 1 now carries "below the locked optimum's move" in its label. Non-retroactivity is stated in the N6 cell; N23's re-reading stays report-only. (`reviews/night2/CAUSAL_KAPPA_LENIENCY_REVIEW.md`.)
- **CAUSAL-NULL-INVARIANCE (PR #70 → v1.4.15).** The authored 70–81% share was a noise-limited Monte Carlo; the exact one-pole value is 90% (+0.318 vs +0.354). Two-pole linear kernels of equal accuracy span 90–105%, so a Bayes-locked causal test cannot fail that rival at any sample size when the payoff is 0–1.
- **KERNEL-MEASURE (PR #58 → v1.4.10) and the VIX referee (PR #66 → v1.4.13).** The free-noise "inconclusive" claim moved α alone. "Supported, not certified" was overstated and became "consistent, not certified". The in-model reference for VIX minus the realized-target share is about +0.02, not 0. The gain finding is target-dependent.
- **ONSET-ACROSS-ALPHA (PR #64 → v1.4.14).** Resolution stated as |Δ| ≲ 0.13, not the generous ±0.267 margin; times corrected to commit times; one n = 16 grid replicate was INCONCLUSIVE and is reported.
- **STAKES-REFEREE.** S3 tests predictability at issue time, not exogeneity of the slope; ŵ is a reduced-form cost of a load surprise, not yet §2.2's w. System resource cost is about half the load-serving payment under a locally linear supply response (cancels in Δlog w, not in levels). 2024's size is driven by one July heat week. S2's "pass" is uninformative (CI spans a factor of ~20). A linear bias×premium term sits outside k_lin.

Earlier in the day, reviewers also corrected the telegraph adaptation constant (−0.7 → −(γ+1)), narrowed kernel invariance to regressions on the tracker's own observations, replaced a universal store-count constant with a model- and span-dependent c, derived the noisy-read onset asymptote, and tightened Regime C's premises. No locked verdict was relabelled by any of these merges.

---

## 6. The biggest finding of the day

**The optimum depends on the loss; the §2.5 bridge holds only under squared error; and the pass rules were lenient.**

An optimum is the argmin of THEORY §2.1's J, and J contains w·E[ℓ(e)]. Every number in §2.2, including the bridge a = b = 1/α on which the lone-tracker reset-read onset exponent −1 rests, is a squared-error fact (v1.4.16).

In the two-state world, under a q-fixed κ ×4 change, the direction of the best linear tracker's adaptation-time move itself depends on the payoff (exact grid, independently reproduced):

| Tracker | Δln t_A | share of Bayes |
|---|---|---|
| Bayes | +0.354 | 1 |
| sign (0–1)-best one-pole | +0.318 | 0.90 |
| squared-error-best one-pole (= Kalman) | −0.068 | −0.19 |
| absolute-error-best one-pole | −0.225 | −0.64 |

So a Bayes-locked causal test **cannot fail** the 0–1-best linear rival at any sample size, and it *can* discriminate under squared or absolute error, where the linear rival moves the other way. That is why every new prereg must name its loss and its rival family up front; a prereg that names no loss is scored under squared error. The requirement binds going forward; no earlier locked verdict is relabelled (v1.4.16).

Separately, the causal pass rule only asked for an effect above zero, while the fail rule asked for a miss of the κ_F kill line. A design whose true share lay *below* the kill line still read as a pass most of the time (about 48–83% at share 0.40). The fix, now in N6, is the mirror: pass only when the move is established above the same κ_F share the kill uses (v1.4.17). Wrong passes drop to about 1% at share 0.40; false kills are unchanged. This also binds going forward; N23's locked PROXY-PASS stands, with a report-only re-reading of inconclusive. CAUSAL-NULL-INVARIANCE still passes.

The same kind of split lives in other locked families (`reviews/night2/PASS_RULE_SYMMETRY_AUDIT.md`, report-only, PR #76): HIT against zero / MISS against a floor (C3b, F1, DECISIVE banks), and relative 15% bands that pass on the point estimate even when the interval cannot support closeness (LEARNSIM RA, AA, V RR, V RRh would read inconclusive under TOST). KERNEL, the VIX-proxy shape test and the EIV midpoint rule were already symmetric; the onset primary already uses TOST. Those sibling fixes are queued (HIT-ZERO-MISS-FLOOR, RELATIVE-BAND-TOST), not edited into THEORY today.

---

## 7. The top five next tests

Ranked by how much a decisive result would change belief about the open empirical bet (N13/N6) or about today's loss-and-discrimination finding — not by the queue's current I-score. Item notes are in `queue/items.json` and `QUEUE.md`.

1. **SAME-SYSTEM-AQN.** The first real test of N13: measure α, q, N, stakes and one design quantity on one real system, lock the §2.2 prediction, and name fixed-budget-share and universal-½ rivals, with the loss fixed. Until this (or an equivalent) is done, the open bet remains untested. Candidates named in the item: SPF, VIX, E. coli, each with premise work still owed (AQN referee corrections; linear vs Bayes lock).
2. **BAYES-LINEAR-LAB.** The decisive real-data version of today's discriminator: a graded (quadratic) payoff, κ ×4 at fixed q, λ, μ and N measured, change-of-mind latency, enough switches for σ on Δln t_A, and the rival computed for the same payoff. Under a 0–1 payoff the test cannot fail the linear rival. **Blocked on Chad** (recruiting participants, or requesting Piet 2018 data, which is "available from the authors upon request") (`reviews/night2/CAUSAL_NULL_INVARIANCE.md` §5).
3. **A powered N6 causal test on cleaned stakes (STAKES-SHIFT-MULTIYEAR, after or with STAKES-CAUSAL-CONTROLS and STAKES-SETTLEMENT-PRICE).** The first locked causal-form test (N22) was inconclusive and underpowered; the apparent 4× stakes fall was mostly a behind-the-meter definition effect. A many-contrast, like-for-like test, with supply surprises partialled out and the settlement price declared, would be the first causal reading of N6 on a real system.
4. **KERNEL-DECISIVE-RV.** The only real-data §2.2-row result is exploratory because tracker noise left σ_D above 0.040. A design that reaches the locked resolution (intraday realized variance, a second independent noise proxy, or a second implied-vol system), locked with MV10, would be the first decisive pass or fail of the kernel map on proxy.
5. **SENSE-CELL.** A different substrate (E. coli adaptation; Keegstra et al. 2017, Lan et al. 2012). N6's theory-level claim needs two strongly selected systems at different scales. Receptor reads are noisy, so the physics enters through the precision-price exponent θ (N12 referee C1).

Queued rule work that would change how existing evidence is read, but is not a world test: **RELATIVE-BAND-TOST**, **HIT-ZERO-MISS-FLOOR**, **CAUSAL-OVER-RESPONSE**, **LOSS-SENSITIVITY-REPORT**.

---

## 8. What is blocked on Chad

None of these was done, and none will be done without an explicit go:

- Contacting data authors, or lab participants, including a request for Piet 2018 data or a new recruitment for **BAYES-LINEAR-LAB**.
- The X correction post.
- Making this repository public (it stays private).
- Changing the Looper README wording.

Standing constraints unchanged: no emails, posts or messages unasked; no public acts; calendar writes only to the private calendar; never invent facts or citations; field results labelled by proxy; no field kills; heavy compute at nice 19.

---

## 9. Sources (all in this repository)

- Theory and status: `THEORY.md` (v1.4.17, especially the status block, §1 N6, §2.2 loss premise, §2.5, §8c, §13 changelog), `STATUS.md`, `QUEUE.md`, `measurement/CLAIM_MAP_v2.md` (v2.37), `measurement/FRAMEWORK.md`.
- Loss lock: `reviews/night2/PREREG_LOSS_LOCK.md`, `reviews/night2/PREREG_LOSS_LOCK_REVIEW.md`.
- Pass-rule leniency: `reviews/night2/CAUSAL_KAPPA_LENIENCY.md`, `reviews/night2/CAUSAL_KAPPA_LENIENCY_REVIEW.md`, `reviews/night2/PASS_RULE_SYMMETRY_AUDIT.md`.
- Causal-null and lab: `reviews/night2/CAUSAL_NULL_INVARIANCE.md`, `reviews/night2/CAUSAL_NULL_INVARIANCE_REVIEW.md`, `tests/LAB_AKLMT_TAU/RESULTS.md`.
- Kernel and onset: `tests/KERNEL_MEASURE/RESULTS.md`, `reviews/night2/KERNEL_MEASURE_REVIEW.md`, `reviews/night2/KERNEL_PROXY_REVIEW.md`, `reviews/night2/KERNEL_PROXY_REVIEW2.md`, `tests/ONSET_ACROSS_ALPHA/RESULTS.md`, `reviews/night2/ONSET_ACROSS_ALPHA_REVIEW.md`.
- Stakes: `reviews/night2/STAKES_REFEREE.md`, `tests/STAKES_EXOGENOUS/RESULTS.md`, `tests/STAKES_SHIFT_CAISO/RESULTS.md`.
- Ledger of today's picks and reviews: `queue/LEDGER.jsonl` entries through 186.
