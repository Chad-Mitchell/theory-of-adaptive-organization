# CAUSAL-NULL-INVARIANCE-REVIEW: independent review of PR #70 (THEORY v1.4.15, CLAIM_MAP v2.34 note)

Out-of-cycle and unscored (independent review of the pick-35 author PR per Chad t1916). Reviewer: an independent executor (for Ace,
Chad t1914/t1916). I wrote none of pick 35, `CAUSAL_NULL_INVARIANCE*`, PR #69/#70, N16, CAUSAL-KILL-INPUTS or DISCRETE-TA.
Sunday 15 November 2026, written about 7:47 PM ET (America/New_York). In-model only. Vigilance (H8) stays OPEN. No CLAIM_MAP
status changes. Nothing posted or sent.
Own code: `CAUSAL_NULL_INVARIANCE_REVIEW_checks/` (nice 19; imports nothing from `CAUSAL_NULL_INVARIANCE/`).

## Verdict: PASS-WITH-FIXES (merged)
The qualitative finding holds, and is stronger than the author stated. The headline number is wrong. Under the q-fixed κ ×4
change, the accuracy-best (0–1 payoff) linear tracker's adaptation time moves **Δln t_A = +0.318, exactly** (deterministic grid
computation, converged). That is **90% of the Bayes move** (+0.354 on the same exact grid; 91% of the author's locked +0.350).
The author's 70–81% (+0.244 / +0.284) came from Monte Carlo scans that could not locate a flat optimum. The conclusion "a
Bayes-locked causal test with κ_F ≤ ½ cannot fail that rival" holds with more margin. The locked in-model test is correctly
scored PASS on its proxy. My own re-implementation with new seeds also passes: seven replicates average D = +0.347 ± 0.012.
So the author's 0.290 is a low draw, not a learner bias. Fixes are applied in THEORY v1.4.15 (number still free on main),
in the CLAIM_MAP v2.34 note, and as an erratum appended to `CAUSAL_NULL_INVARIANCE.md`.

## Method (own code)
`gridengine.py` computes the sampled world exactly, with no Monte Carlo noise. The author's world and estimator are used as
written: flip with probability p = (1 − e^{−2λΔ})/2, then y = xμ + √(N/Δ)ε, then z ← f(z) + g·y. The engine builds the joint
(z, x) Markov chain on a state grid (cell-integrated Gaussian kernel, 0 on a cell edge) and solves for the stationary law
directly with a sparse solve. It then reads two things. The error rate is P(z·x ≤ 0). The switch-law adaptation time is
D·E[n], where n is the first sample n ≥ 1 after the switch with sign(z) equal to the new state. It starts from the stationary
law of z given the pre-switch state. A passage overtaken by a later switch is dropped, with weight (1 − p)^{n−1}, which is
exactly the author's stationary-record estimator. Grid convergence (h halved): t_A changes by ≤ 2×10⁻⁶ relative, err by
≤ 0.1% (smooth in the pole, so the argmin is unaffected). Cross-checks against my own numba Monte Carlo (`mc.py`, `t1.py`,
`t2.py`) agree within MC error at every point tried (e.g. A, pole ×2: err 0.009922 grid vs 0.009956 ± 0.00005 MC; t_A 0.8218
vs 0.8241 ± 0.002). Kalman pole from my own closed-form discrete Riccati.

Reproduced author numbers (exact grid; author MC in brackets):
| Point (N = 1, Δ = 0.01) | κ | Bayes t_A | Kalman zero-crossing t_A | 0–1-best one-pole t_A (pole ×) | errors: Bayes / 0–1 linear |
|---|---|---|---|---|---|
| A: λ 0.01, μ² 4 | 0.0025 | 0.6630 [0.670 ± 0.004] | 1.6384 [1.647] | 0.7246 (×2.265) | 0.00869 / 0.00967 (+11.3%) |
| B: λ 0.02, μ² 2 | 0.010 | 0.9447 [0.951 ± 0.005] | 1.5310 [1.534] | 0.9960 (×1.548) | 0.02709 / 0.02928 (+8.1%) |
| Bnull: λ ×2.6546, μ² ×0.7534 | 0.0088 | 0.6559 [0.658] | 1.0975 [1.105] | 0.6934 (×1.597) | 0.02447 / 0.02653 (+8.4%) |

A→B: Bayes +0.354 (+42%), Kalman zero-crossing −0.068 (−7%), 0–1-best linear **+0.318 (+37%)**. A→Bnull: Bayes −0.011,
Kalman −0.401 (−33%), 0–1-best linear −0.044 (author −11%). My Bayes values include the overtaken-passage censoring that the
author's MC estimator also applies. Without it, they match the author's lattice (0.664 / 0.951); the censoring lowers B by
about 0.7%.

## Q1. Scope of the κ-only separation: correct, with two scope words added
- The dimensional analysis is right. λ [1/T], μ² [X²] and N [X²T] admit one dimensionless group, so in continuous time every
  design quantity of either optimum is λ^{−a}μ^{2b}f(κ). This needs **a loss with no scale of its own** (squared error and
  0–1 qualify; a fixed cost per switch, a threshold or a deadline adds a group). It also needs **the symmetric two-level world
  with one white-noise channel** (asymmetric rates or levels, more states, or a second noise source add groups). Both scope
  phrases are added to the passage.
- Grid check (`q1_scaling.py`). λ ×2, μ² ×2 at fixed N and Δ keeps κ but doubles λΔ. The t_A ratios are Bayes 0.511,
  Kalman 0.504 and 0–1 linear 0.510 (author: 0.507 / 0.504). Halving Δ as well, which keeps λΔ, gives **exactly 0.5000**
  for all three. So on sampled data the two groups are κ and λΔ, as stated.
- "Separation per unit Δln κ is about ½ − 1/ℓ" holds for Bayes t_A against the **linear memory time** in continuous time:
  0.274 over κ 0.0025 → 0.01 (½ − 1/ℓ = 0.304, 0.273 and 0.231 at κ = 0.0025, 0.005 and 0.01). Against the linear
  **zero-crossing** time, which is what a test measures, the separation is larger here (0.304 per unit Δln κ on the grid).
  This is now said.

## Q2. The 0–1-best linear move: +0.318, i.e. 90% of Bayes (author's 70–81% is a noise artefact)
`q2_lin01.py` minimizes the exact error rate over the one-pole family z ← a z + y, with a = 1 − (1 − a_Kalman)·t. It uses a
bounded Brent search with x-tolerance 10⁻⁵ in ln t.
- Optimum t: A **2.2647**, B **1.5479**, Bnull **1.5968** (author: A 2.065 / 2.378, B 1.525 / 1.682).
- Curvature of the error rate in ln t at the optimum: A d²err/d(ln t)² = 0.0353 (3.65 × err_min), B 0.0705 (2.41 × err_min),
  Bnull 0.0670. The error rate rises by 1% of its minimum only at ±0.074 (A) and ±0.091 (B) in ln t. Meanwhile
  d ln t_A / d ln t = −1.01 (A) and −1.00 (B), so locating t_A to ±0.01 needs the error rate to about 2×10⁻⁶. The author's MC
  error SEs were about 10⁻⁴ per point, and their scans moved the argmin by ±0.1 in ln t, which is the 0.04 disagreement.
- Exact move: **Δln t_A(A→B) = +0.3181** (h halved: +0.3181). Ratio to Bayes on the same grid: **0.898**; to the locked
  +0.3504: 0.908; to the author's lattice +0.359: 0.886. Bnull: −0.044.
- A common-random-number MC (`q2_twopole.py`) independently confirms the one-pole optimum. No one-pole neighbour (±30% in t)
  beats t = 2.265 or 1.548, and MC t_A there is 0.7227 / 0.9971.
- **Scope: one-pole is a family choice, not "the best linear tracker".** I searched 432 two-pole kernels z = r₁m₁ + w·r₂m₂
  on common random numbers. None beats the one-pole optimum by more than 0.04% (A, 2.6σ) or 0.08% (B, 1.6σ) in error rate.
  But kernels within that tolerance have t_A from 0.708 to 0.723 (A) and 0.997 to 1.025 (B), i.e. Δln t_A from about +0.32
  to +0.37. Over all linear kernels, the 0–1-best response is therefore pinned only to about 0.32–0.37, which is 90–105% of
  Bayes. Either way it is far above the κ_F·predicted = 0.175 kill line.
- Consequence for the report's §3 optimality-form gap. Bayes minus the one-pole 0–1 optimum is 0.036, not "0.07–0.11". It
  could be about 0 for richer linear kernels. A 2.8σ gap test would need σ ≲ 0.013 and is not robust to the rival family.
  Under a 0–1 payoff, the adaptation-time response barely discriminates Bayes from linear at all, in either form.

## Q3. Should "the prereg fixes the loss" become N6/§2.5 text?
Yes, in substance. It belongs to PREREG-LOSS-LOCK (active as pick 37) with a separate applier and reviewer, not this PR.
Nothing of the kind was added here. Three points for that item:
- (a) The prereg must fix the loss **and the rival family**. Under 0–1 payoff the one-pole and two-pole optima differ by up
  to about 0.05 in the response.
- (b) Use the corrected number: 0.318 (≈ 90%), not 70–81%.
- (c) A test meant to separate Bayes from linear should use a graded (quadratic) payoff, where the Kalman rival's −0.068 sits
  0.42 below the Bayes +0.354. Or it should use an observable other than the mean adaptation time, e.g. the dependence of t_A
  on pre-switch confidence (the hazard-set bound).

## Q4. In-model PASS label: correct
The locked rule is applied correctly from `test_result.json`. D = 0.2895 and σ = 0.0295, so D − 1.96σ = 0.232 > 0 and
D + 1.96σ = 0.347 > 0.1752, which is PASSED. The lock is intact: `PREREG.md`, `core.py`, `learner.py`, `run_test.py`,
`derive.*`, `pilot*.*` and `mv10_mse.json` are unchanged between `93a6ca4` and the PR head. The outcome commit only added
outputs and `check_lin01.*`. Realized arm sds of ln t_A (0.095, 0.109) are close to the 8-learner pilot's 0.097, so using a
non-arm pilot for MV10 was harmless here.
I re-implemented the locked design from the prereg text (`q4_learner.py`, own numba, new seeds 51000+/52000+):
**D = +0.400 ± 0.028, PASSED**, 0/48 linear. Seven independent replicates (`q4_replicates.py`) gave D = 0.400, 0.358,
0.315, 0.353, 0.361, 0.327 and 0.315. That is a mean of **0.347 ± 0.012** with an across-replicate sd of 0.031, against a
mean within-run σ of 0.027. All seven PASSED, and 0 of 336 learners chose a linear member. So the author's post hoc
"finite-experience bias" reading of the 0.06 shortfall is not supported. At E = 20 switches the learners' expected response
equals the Bayes prediction (0.350 / 0.354) within 0.012, and 0.290 is a 1.9σ low draw. The label "passed on proxy
'MSE-payoff-selected learners …'" stands. Added: the replication, and that a PASS here cannot separate Bayes from the 0–1
linear rival (not its purpose).

## Prior art (read this review)
- Piet, El Hady & Brody 2018, *Nat Commun* 9:4265 (read via nature.com). Verified verbatim: "the linear agent to have 99.8% of
  the accuracy of the nonlinear model … 77.15 and 77.34% accuracy … agree on 97% of trials". They "did not examine whether our
  subjects demonstrated nonlinear evidence discounting". "Lower sensory noise would … potentially distinguish the nonlinear and
  linear discounting models". Data "available from the authors upon request". Also relevant and now noted: their Fig. 2g shows
  that the accuracy-best linear discounting rate changes with sensory noise. Their task is Poisson clicks, an event-sensed
  observation model, not Gaussian white noise.
- Glaze, Kable & Gold 2015, *eLife* 4:e08825 (full text via Europe PMC PMC4584511). Their Eq. 4, dL = −2λ sinh L dt + A dx,
  is the same continuous-time filter. **Attribution fix:** "report small model-comparison differences" was imprecise. The
  leaky-accumulator (linear) model fit **worse** than the normative model for 34 of 48 subjects (triangles task; median ΔBIC
  −5.2) and 10 of 13 (dots-reversal). The "similarly small BIC differences" on simulated data refer to the normative versus
  **stabilizing-boundary** model. Passage reworded.

## Wording, goalposts, scope
In-model and on-proxy throughout. "Theory", not "law". Vigilance OPEN. No CLAIM_MAP status change (N16 MATH-CORRECTED, N13
OPEN). No kill condition, headline, locked prediction or result moved. No N6/§2.5 text added (left to PREREG-LOSS-LOCK). The
THEORY diff touches only the §2.2 Regime A premise bullet (one appended passage), the header and the changelog, plus the
CLAIM_MAP pointer and note.

## Fixes applied
- F1: 0–1 linear move corrected to +0.318 (+37%, 90% of Bayes, exact for the one-pole family). The MC origin of 70–81% is
  stated, along with the two-pole range 0.32–0.37.
- F2: excess errors 8–11% (was 8–16%).
- F3: scope phrases added: loss with no scale of its own; symmetric two-level world with one noise channel. The ½ − 1/ℓ
  statement is tied to the memory time, with the zero-crossing separation given.
- F4: Glaze attribution corrected; Piet Fig. 2g noted.
- F5: replication of the locked test stated (0.400; seven replicates 0.347 ± 0.012).
- F6: CLAIM_MAP v2.34 note numbers corrected. THEORY's CLAIM_MAP pointer set to v2.35, the latest note on main.
- F7: erratum appended to `CAUSAL_NULL_INVARIANCE.md` (the author's text is left as written). Notes added to
  PREREG-LOSS-LOCK and LIN01-RESPONSE-EXACT.
