# Independent review: THEOREMS.md, FRACTAL_ARCHITECTURE.md + sim/, X_THREAD_DRAFT.txt

Reviewer: independent pass (did not write the reviewed work; authors' REVIEW.md files read only after forming this judgment).
Date: Fri 2026-11-13, ~3:15 PM ET. Nothing was posted or sent.

Artifacts in this folder:
- `indep_checks.py` / `.out` — my own sympy/numeric re-derivations (not copied from checks/check_all.py).
- `simrerun/` — clean rerun of the authors' sim (`rerun.log`, `RESULTS_raw.md` byte-identical to the original), plus `fresh_seeds.py/.out` (seeds 7-12).
- `xcount.py` — X weighted-length counter (twitter-text v3 weights; URL = 23).
- `.venv/` — local venv (sympy, scipy) — the system python has no sympy.

## Verdict in one paragraph
The math is correct within its stated assumptions; I found no wrong result, one wrong justification (T7b), and several overclaims of novelty or relevance. All prior-art attributions check out against real sources. The simulation is honest: the prereg hash matches and its file birth time predates the code, numbers reproduce exactly, fresh seeds agree, and post-hoc arms are labeled. But the sim is a best case by construction and several "confirmations" cannot fail. The draft thread is mostly accurate but has one false sentence (post 3, "Below that, keep raw facts"), omits three failed predictions and the uncharged-compute caveat, and points at a [LINK] that does not exist publicly yet. The corrected thread (`../architecture/X_THREAD_REVIEWED.txt`) is safe to post **once a public link to the materials exists**.

## Prior-art verification (sources fetched this pass)
| Claim | Verdict | Source |
|---|---|---|
| Harris 1913 EOQ | Correct. "How Many Parts to Make at Once", Factory, The Magazine of Management 10(2):135-136,152; reprinted Oper. Res. 38(6) 1990 (Erlenkotter). | pubsonline.informs.org/doi/10.1287/opre.38.6.947 |
| Muth 1960 | Correct. JASA 55(290):299-306; EWMA optimal for random walk + white noise. | doi.org/10.2307/2281742 |
| Kalman 1960 | Correct. J. Basic Eng. 82(1):35-45. | doi.org/10.1115/1.3662552 |
| Cho & Garcia-Molina 2003 | Correct in substance (ACM TODS 28(4):390-426): to maximize freshness, penalize/ignore pages that change too often; for age, refresh rises monotonically. Minor: THEOREMS T1 attributes the explicit small-λ formula √(μWλ/2c) to them; that is the authors' own expansion, not a formula I found in the paper. Fig. 11(a)/(b) citation not verified. | dl.acm.org/doi/10.1145/958942.958945 |
| Roundy 1985 2.01% / 6.07% | Correct. Mgmt Sci 31(11):1416-1430: optimal power-of-two policy within 2% (1/(√2 ln2)=1.0201) with optimized base period; ~6% (3/(2√2)=1.0607) with fixed base. Note: Roundy's 1.02 is a worst-case bound after optimizing the base period; T7b's 2.01% is a population mean under a log-uniform spread. Same integral, different statement; say "same number, same math", not "exactly Roundy's bound". | doi.org/10.1287/mnsc.31.11.1416 |
| Still, Sivak, Bell & Crooks 2012 | Correct and conditions stated faithfully (PRL 109,120604; arXiv:1203.3271): stochastic drive, **no feedback**, Markov discrete-time system, heat bath, starts in equilibrium; Eq. 14 per-step equality, Eq. 18 bound, Eq. 21 refined Landauer. My independent toy reproduces Eq. 14 to 6 decimals; it is an identity once F_neq is defined (authors say so). | arxiv.org/abs/1203.3271 |
| Benjamin 1976 vortex rings | Correct: steady rings **maximize** kinetic energy at fixed impulse over isovortical rearrangements (Lecture Notes in Math 503:8-29; Fukumoto & Moffatt 2008 restate). | doi.org/10.1007/bfb0088744 |
| Equitz & Cover 1991 | Correct: Gaussian/MSE successively refinable (IEEE T-IT 37(2):269-275). | doi.org/10.1109/18.75242 |
| Lastras & Berger 2001 | Correct: any i.i.d. source, squared error, an achievable scheme with rate loss ≤ ½ bit/sample per stage (IEEE T-IT 47(3):918-926). | doi.org/10.1109/18.915645 |
| Francis & Wonham 1976 | Correct: Automatica 12(5):457-465. | doi.org/10.1016/0005-1098(76)90006-6 |
| Arnold structure theorem | Correct (needs bounded analytic domain; regions fibered by invariant tori or cylinders). | math.toronto.edu/khesin/papers/steady.pdf |
| Poincaré–Hopf / torus | Correct as stated for closed **orientable** surfaces (χ=0 ⇒ torus; the Klein bottle also has χ=0 but cannot embed in R³). Tokamak flux-surface argument is standard. | Flux surface refs; Parabola "hairy doughnut" |

## Independent math checks (all in `indep_checks.out`)
T1a T\*, J\* ✓ · T1b K²/(1−K)=q/r and series ✓ · T1c 6.1% / 73.9% ✓ (my EWMA version gives +6.1% / +74.3% vs their 6.2% / 75.8%: definition-dependent, immaterial) · T2b ε < 1 − c_w/c_main ✓ · T3a N\* = ρ/(√(1+ρ)−1)² = (√(1+ρ)+1)²/ρ ✓ (5.83, 9.90, 41.98) · T3b 5.1/14.3/22.6/29.3% ✓ · T4 local exponents 0.489…0.33 ✓ · T5 ∂²F/∂f² and dF/df→1/λ ✓, f\* hump peaking ≈2.98 near λ=5 and zero for λ>10 ✓ · T6 ✓ · T7b φ(Δ), 1.0201, 1.0607 ✓, K\* = (CL²/(12h))^{1/3} ✓ · T7c exponent ✓ · E3 crossover r_w\* ≈ 0.454 ✓. T3c table not independently re-run (not used publicly).

## Simulation audit
- **Prereg timing: OK, self-attested.** sha256 of PREREG_2026-11-13.md = cea65473…8f1f = PREREG.sha256. Birth times: prereg 14:39:00, nested_sim.py 14:40:12, run_all.py 14:40:27, first results 14:40:45 ET. The header's "2:45 PM" is wrong (D5 discloses it). Caveat: all local timestamps, no third-party timestamp, so publicly say "written down before the code", not "verifiably preregistered".
- **Reproduction: exact.** Full rerun in 82 s; RESULTS_raw.md byte-identical. Fresh seeds 7-12 (B=4): nested/flat 1.048 (φ=0), 0.828 (φ=0.5), 0.626 (φ=0.75); NIS-learned/flat at φ=0 1.497. All match the reported ranges.
- **Post-hoc labels: honest.** D0-D5 are disclosed, the failed prereg rule is reported first, and the P4 clause is scored as failed.

## Issues by severity

### High (must fix before posting)
1. **Thread post 3 states something false: "Below that, keep raw facts."** T3a is a *sufficient* condition (an upper bound on nested cost). The sim shows compression paying from n=2 at zero upkeep and about 6-8 with upkeep. *Fix:* say it is a sufficient condition, not a cutoff, and give the sim numbers (reviewed posts 3-4).
2. **The thread's [LINK] does not exist publicly.** Post 9 promises math, code, prereg and failures, but they live only on the box. *Fix:* publish a public repo or gist (THEOREMS.md, sim/, prereg + sha256, DEVIATIONS.md, RESULTS.md, this review) before posting, or drop the link sentence. Do not point it at the main post, which has none of this.
3. **The thread omits failed or null predictions** (P6a: 15% vs ≥20%; P4 bound clause; P7a/b not detected) and the **uncharged compute** (nested updates about 5x slower, which could erase the half-shared gain). The draft names only the P2 miss and the P6b failure. *Fix:* reviewed posts 6-8.

### Medium
4. **E2b and the high-sharing E1 wins cannot fail.** With h=0 and the true joint model, a Kalman filter cannot lose to an independence approximation, up to greedy scheduling. So E2b "agreeing that T3a is conservative" is not a test of T3a. The sim also optimizes a different objective (budgeted MSE, greedy) from the bound (periodic EOQ cost). *Fix (THEOREMS T3a "Sim check", FRACTAL §3.2):* call it consistent but non-diagnostic. A real test needs a misspecified world (overlapping or switching drivers).
5. **The FRACTAL §3.4 design rule is contradicted by its own sim.** It says level parameters "must never be estimated from the level's own outputs", but mom_post (the filter's own posterior means) repaired 97% of the planted error, against 98% for mom_raw. What the sim shows is identifiability (co-movement statistics separate the levels; total-error size does not). *Fix:* delete "never from its own outputs", keep "from statistics that separate the levels", and note the post-hoc rule was tested only on the worlds that motivated it.
6. **T2b is labeled NEW? but is cost accounting, and its model is internally odd.** It assumes a watcher check is as informative as a main check, so escalating adds nothing. Real escalations are triggered by surprise, not random. "Worthless above 90%" is a tautology (each check then costs ≥ c_main). *Fix:* relabel as an accounting identity and add the assumption. I dropped it from the thread.
7. **T8 overreaches with successive refinement.** Equitz–Cover and Lastras–Berger concern coarse-to-fine descriptions of one i.i.d. source. They say nothing about driver-plus-residual memory of drifting, correlated facts with upkeep. *Fix:* call it an analogy and cut "this is a real, citable result in favor of nested storage".
8. **The FRACTAL §3.3 gate was not tested against real shared shocks.** "The gate cost nothing" was measured only in worlds without group-level jumps. A gate that forces a big single-item surprise to stay local is exactly what delays detecting a real driver change first seen on one item. *Fix:* state this as untested and add a world with group jumps.
9. **"I derived" (draft post 3).** The account voice implies Chad derived it personally; it came from AI-assisted work. *Fix:* "we" or neutral wording (as in the reviewed thread).

### Low
10. **T7b's convexity reason uses the wrong function.** The objective is Σ Δ_k·φ(Δ_k)/L, so the needed convexity is ψ(Δ) = Δφ(Δ) = 2 sinh(Δ/2) − Δ (ψ'' = ½ sinh(Δ/2) > 0), not φ. The conclusion (equal log-widths) still holds. *Fix:* replace the argument.
11. T7b is also near-tautological: scale-free input gives scale-free output. The text already says the design "inherits the world's structure"; keep that and don't call it a finding.
12. T1a "hard tolerance T\* ≈ (ε/σ)²" drops the confidence factor. *Fix:* (ε/(zσ))².
13. T9's "the sharpest true reason donuts are everywhere" is rhetorical overreach. *Fix:* "one rigorous reason recirculating surfaces without rest points are tori".
14. RESULTS.md cites "THEOREMS T1d", which doesn't exist. *Fix:* T1c.
15. FRACTAL §3.4 says "checked √N times as often". That holds only if the driver's drift equals the fact's. *Fix:* "√N times more often than a fact with the same drift".
16. The E3 "watchers" are cheaper, noisier sensors with no escalation logic. Don't cite E3 as evidence for the escalation rule.

## Must not be claimed publicly
- That nested/fractal memory is shown to beat flat memory in general, or on real data (it was a toy built to favor nested; no real-data test exists).
- That the compression threshold is a cutoff below which raw facts are better.
- That the architecture is fractal (it is only under scale-free drift and power-law costs), or that this is a new theorem.
- That T2b, T3a or T4 are new results (unconfirmed; elementary; likely known in inventory or hierarchical forecasting).
- Anything that ties Still et al. to Looper, people or firms (the no-feedback condition is violated; kT is irrelevant there); any "information = energy" or energy-minimization claim; any claim that toroidal flow is minimum-energy (vortex rings are energy *maxima*).
- That the preregistration is externally verifiable (local timestamps only), or that the post-hoc co-movement rule is validated.
- Phase-locking as a finding (untested; earlier toy runs did not support a torus reading).

## Changes made to the thread (X_THREAD_REVIEWED.txt, 10 posts, all ≤ 280 weighted)
- Post 2: EOQ analogy stated precisely ("drift variance in place of demand").
- Old post 3 split into new posts 3-4: credited cousins (square-root pooling, joint replenishment); the claim is now framed as a sufficient condition, and the false "keep raw facts" line is removed; the sim numbers are added.
- Old post 4 (watcher/escalation) dropped as a trivial identity with an odd model (issue 6).
- Post 5 adds "6 seeds" and "an independent rerun matched, fresh seeds agreed".
- New post 6 covers the best-case construction and the uncharged ~5x compute.
- Post 7 lists every failed prediction: P2 threshold, P6a, P4 clause, P6b.
- Post 8 adds that the post-hoc fix was tested only on the same worlds, and that P7 collateral was not detected.
- Post 9: "fractal" kept conditional; Roundy wording changed to "same math".
- Post 10: torus line kept, with "untested" added; the closer and the [LINK] are merged in.
- "I" changed to "we" or neutral wording.
