# CAUSAL-NULL-INVARIANCE — null manifolds, the Bayes-vs-linear discriminator, and a locked in-model test (pick 35)

Pick 35, unaided slot (ledger 163 unaided order, 164 rule rank, 165 claim, 167 outcome; 166 is the PR #64 review). Author: executor queue-pick35 (for Ace,
Chad t1914/t1916); I authored none of CAUSAL-KILL-INPUTS, its review, or DISCRETE-TA. 15 Nov 2026, about 7:30 PM ET.
In-model only. Vigilance (H8) stays OPEN. No CLAIM_MAP status change. Nothing posted or sent; no one contacted; no money spent.
Files: `CAUSAL_NULL_INVARIANCE/` (own code, nice 19). Prereg and code locked in 93a6ca4 (pushed) before any outcome-arm run.

## 1. Answer to the item
**Ruling proposed (for a separate reviewer): keep null predictions unscored; no invariance clause.** Reason, from first principles:
the discriminating information between the Bayes-locked and the linear optimum lives entirely in the change of one dimensionless
group (§2), so any change on which one optimum predicts no move is a change on which the other predicts a move, and the same
test can be locked on the optimum that predicts the move and scored by the existing direction + magnitude rule (§1 N6, κ_F ≤ ½).
An invariance clause would widen the claims without adding discriminating power. **But the discriminator only exists if the
prereg also locks the loss** (§3): against the best linear tracker for a 0–1 (decision) payoff, the Bayes-locked causal test
cannot fail at any sample size.

## 2. Null manifolds (derivation; checked numerically)
Telegraph world ±μ, flip rate λ each way, white noise density N. The inputs carry units λ [1/T], μ² [X²], N [X²·T]; the only
dimensionless group is κ = λN/μ². Hence every design quantity Q of dimension T^a X^{2b} of **either** optimum is
Q = λ^{−a} μ^{2b} f_Q(κ): Bayes t_A = (1/λ) F_B(κ) (N16: F_B ≈ (κ/2)[ln(2/κ) − γ − 1]); Kalman memory time =
(1/λ)·1/(2√(1 + 1/κ)); Bayes MSE = μ²·2K₀(κ)/(K₀ + K₁); Kalman MSE = μ²·2(√(κ² + κ) − κ). Consequences:
- **Null manifold of Q** (per optimum): −a dlnλ + b dlnμ² + (dln f_Q/dlnκ)(dlnλ + dlnN − dlnμ²) = 0, one surface per
  quantity and per optimum (the review's point that a null belongs to a quantity, not to a world change, is this statement).
- **Bayes vs linear separate only through κ:** Δln(Q_B/Q_L) = Δln(f_B/f_L)(κ). For t_A at small κ the separation per unit
  Δlnκ is ½ − 1/ℓ (ℓ = ln(2/κ) − γ − 1; 0.304 at κ = 0.0025). A change at fixed κ (e.g. λ ×2 with μ²/N ×2) is a pure time
  rescaling and moves both optima identically. Check (`derive.py`, own MC, Δ = 0.01): λ ×2, μ² ×2 halves Bayes t_A
  (ratio 0.507) and the Kalman zero-crossing time (0.504) alike (the grid term breaks exact equality slightly).
- **Precision** (1/MSE) is the same statement with b = −1.
- On sampled data λΔ is a second dimensionless group: changes of the sampling interval also separate the optima (via the
  grid term c√(ΔN)/μ of THEORY v1.4.9).
- Most discriminating direction at fixed N for t_A: along lnκ, i.e. the q-fixed direction (λ ×s, μ² ×1/s); the review's
  split (λ ×2.6546, μ² ×0.7534; κ ×3.52) discriminates by the same Δlnκ rule.

Numbers (`derive.json`; Bayes also by the lattice solver `tools/discrete_ta.py`, 'switch' law):

| Point (N = 1, Δ = 0.01) | κ | Bayes t_A MC (lattice) | Kalman zero-crossing t_A | Kalman memory time |
|---|---|---|---|---|
| A: λ 0.01, μ² 4 | 0.0025 | 0.670 ± 0.004 (0.664) | 1.647 | 2.497 |
| B: λ 0.02, μ² 2 (q fixed) | 0.010 | 0.951 ± 0.005 (0.951) | 1.534 | 2.488 |
| Bnull: λ ×2.6546, μ² ×0.7534 | 0.0088 | 0.658 ± 0.003 (0.660) | 1.105 | 1.760 |

A→B: Bayes +42% (lattice +43%), Kalman zero-crossing −7%. A→Bnull: Bayes −1.8% (lattice −0.6%), Kalman −33% (the review's
−29.5% is the memory time; the zero-crossing time, the quantity a test would measure, moves −33%).

## 3. The loss is part of the locked optimum (pre-lock finding; strong surprise relative to the queue note)
The "linear tracker" of THEORY is the MSE-best (Kalman) one. For a **0–1 decision payoff** (fraction of time the sign is right;
the Bayes sign rule is optimal for it too), the best linear tracker has a different pole. Its error rate is only 8–16% above
Bayes (A: 0.0097–0.0101 vs 0.0087; B: 0.0292–0.0301 vs 0.0270), and the accuracy is flat in the pole, so its t_A is poorly
identified: A→B Δln t_A = +0.284 (17-point grid, `pilot.json`) or +0.244 (finer quadratic fit, new seeds, `check_lin01.json`),
i.e. **70–81% of the Bayes move (+0.350)**; A→Bnull −11% (vs Kalman −33%). Consequences:
- A Bayes-locked causal test kills only below κ_F × predicted ≤ ½ × 0.350 = 0.175. A world whose tracker is the 0–1-best linear
  one moves +0.24 to +0.28: above the kill line. **MV10's FAIL leg is structurally unreachable for that rival at any n.**
- So the −29.5% / 0% contrast of the CAUSAL-KILL-INPUTS review compares Bayes with the MSE-best linear tracker; it mixes
  "nonlinear vs linear" with "which loss". A discriminating prereg must fix the payoff and name the rival optimum for that payoff;
  under a decision payoff only an optimality-form gap test (Δ ≈ 0.07–0.11 in Δln t_A, needing σ ≲ 0.025–0.04) could separate them.
- Prior art (read in full): Piet, El Hady & Brody 2018, *Nat Commun* 9:4265, doi 10.1038/s41467-018-06561-y: in a dynamic
  Poisson-clicks task the accuracy-best linear discounting agent reaches 99.8% of the nonlinear normative accuracy (77.15% vs
  77.34%; 97% of choices agree), so they did not test nonlinearity and say lower sensory noise might separate the two. Glaze,
  Kable & Gold 2015, *eLife* 4:e08825 (read in part: abstract, model section, Fig. 2 legend, model comparison): the normative
  update is a leaky accumulator near L = 0 and a hazard-set bound far from it; fits of simulated data from the normative or the
  bounded model gave "similarly small BIC differences"; subjects' subjective hazard regressed toward the middle. Neither paper
  states the loss dependence of the adaptation-time response or the κ-only separation; I found no source that does (not a
  claim of novelty: search was limited to these two and their references as listed).

## 4. Locked in-model test (MSE payoff; PREREG.md; MV10 met)
Learners never told the world model pick, by realized squared error over 20 switches of experience, one member of a grid family
that contains the Bayes filter, mis-specified nonlinear filters and 25 linear filters. 24 learners per arm; arms A and B (q fixed,
κ ×4). MV10 (`mv10_mse.json`): noise from a pilot at a non-arm point (κ = 0.005), σ = 0.028, effect 0.350, κ_F = ½: SNR 12.5,
both legs reachable, both best cases fire.

**Result (`test_result.json`): D = +0.290 ± 0.029 (σ), D − 1.96σ = 0.232 > 0, D + 1.96σ = 0.347 > kill line 0.175 → PASSED on
proxy 'MSE-payoff-selected learners (F(pp,g) + linear family; E = 20 switches), zero-crossing t_A on a Δ = 0.01 grid'.**
Descriptive: no learner chose a linear member (0/24, 0/24); mean t_A 0.681 (A) and 0.909 (B) vs Bayes 0.664–0.670 and 0.951;
the Kalman rival predicted −0.071. Post hoc: D sits 0.06 (about 2σ) below the Bayes prediction (lattice 0.359): the learners' t_A
is slightly long in A and short in B (they trade hazard against gain along a ridge); with 20 switches of experience this is
selection noise or a finite-experience bias, not tested here.
What this does and does not show: payoff selection under a quadratic loss reaches the Bayes response with modest experience,
so the discriminator is usable in a system optimized for squared error. It is evidence within the model only and is close to
guaranteed by the family containing the Bayes filter with a 3× MSE gap to Kalman (A: 0.120 vs 0.382); the informative part of
this pick is §3.

## 5. What a decisive real-data version needs (not doable now: needs a lab or a partner → blocked on Chad)
- A system whose payoff is known to be quadratic in the tracking error (continuous report or graded reward), not a binary choice.
- A manipulation of κ by ×4 or more at fixed q (λ ×2, μ² ×½ or noise ×4), with λ, μ, N measured, and the adjustment lag and
  share fixed in the prereg (N6).
- Adaptation time read as zero-crossing (change-of-mind) latency after switches: ideal-observer per-switch CV 0.54–0.62, so
  ≥ ~180 switches per arm for σ ≤ 0.0625 on Δln t_A before behavioral noise; the rival named and its prediction computed for the
  same payoff. Human or rat change-point tasks (Glaze 2015; Piet 2018) are the natural instrument; their published designs use a
  binary payoff and do not manipulate κ at fixed q. Running one needs recruiting participants or contacting labs for data
  (Piet 2018 data "available from the authors upon request") — blocked on Chad.

## 6. Questions for the separate reviewer (THEORY v1.4.15 PR, author-only, DO NOT MERGE without separate reviewer PASS)
1. Is the κ-only separation (dimensional analysis) stated with the right scope (continuous time; λΔ on grids; one noise channel)?
2. Is 70–81% for the 0–1-best linear move robust (flat accuracy in the pole; my two grids disagree by 0.04)? Re-derive with own code.
3. Should "the prereg fixes the loss of the locked optimum" become N6/§2.5 text (a kill/premise edit: separate applier)?
4. Is the in-model PASS correctly labelled (D 2σ below the prediction; pilot noise from a non-arm point with 8 learners)?
