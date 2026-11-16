# PREREG-LOSS-LOCK — the loss is an input of the locked optimum (pick 37)

Pick 37, rule slot (ledger 172 unaided order, 173 rule rank, 174 claim; outcome logged after). Author: executor queue-pick37
(for Ace, Chad t1914/t1916). I authored none of CAUSAL-NULL-INVARIANCE (pick 35), its PR #70, the N6 kill text or formal
Theorem 4. 15 Nov 2026, written about 7:50 PM ET. **Proposal only.** The THEORY / FRAMEWORK text below is in an author-only
PR, **DO NOT MERGE without separate reviewer PASS** (Chad t1916). In-model checks only; no data outcome computed, so no
prereg was needed (no test was locked). Vigilance (H8) stays OPEN. No CLAIM_MAP status change. Nothing posted or sent; no one
contacted; no money spent. Own code: `PREREG_LOSS_LOCK_checks/` (nice 19).

## 1. The question and the answer
The item (from pick 35 §3): should N6 / §2.5 say that a prereg fixes the loss (payoff) of its locked optimum and names the
rival optimum for the same loss? **Yes, and the reason is wider than the Bayes-vs-linear case that raised it.** From first
principles: an optimum is the argmin of THEORY §2.1's J, and J contains w·E[ℓ(e)]. Every number in §2.2 is computed at
ℓ(e) = e². So ℓ is an input of the optimum exactly as α, q, N and w are, and N6's list ("α, q, N and stakes") omits it.
`measurement/FRAMEWORK.md` §3.3 already defines how to measure it (error-cost curve, fit ℓ ∝ |e|^p); nothing in THEORY
requires a prereg to use it. The loss enters in three separable places:

1. **The price trade-off (any world).** Read rate and effort balance a price against w·E[ℓ(e)]. With Gaussian errors and
   ℓ = |e|^p, E[ℓ] = c_p V^{p/2}, so the elasticities change with p (§2).
2. **The tracker family (non-Gaussian worlds only).** Within linear trackers, the best one depends on the loss when errors are
   not Gaussian, and it depends on the **rival family** too (pick 35's finding, corrected by its reviewer, ledger 175:
   one-pole sign-payoff optimum +0.318 = 90% of the Bayes +0.354, exact; two-pole kernels of equal accuracy 0.32–0.37 =
   90–105%; re-checked independently in §3). In a Gaussian world it does not: any symmetric,
   nondecreasing loss is minimised by the same linear filter (Sherman 1958), so memory time at a given noise level is
   loss-free; but the chosen noise level, hence the memory time at the effort optimum, still moves with p (place 1).
3. **The Bayes act.** The posterior does not depend on the loss; the act does. In the symmetric two-state world the MSE act
   (posterior mean), the absolute-loss act (posterior median, μ·sign) and the sign act all change sign when the posterior
   crosses ½, so Bayes t_A is the same under these three losses; an asymmetric loss moves the threshold and t_A.

## 2. Price trade-off under power loss (derivation; checked by own Monte Carlo)
**Reset reads (hold-last-value or any rescaling-closed predictor), Regime B fBm, 1 < α < 3.** E|X(t) − X(0)|^p ∝
q^{p/2} t^{p(α−1)/2}, so the cost rate c/T + w·k_p q^{p/2} T^{p(α−1)/2} gives read rate 1/T\* ∝ (w q^{p/2}/c)^{a_p} with

  a_p = 2/(2 + p(α−1)) (stakes),  b_p = p/(2 + p(α−1)) (drift level q).

p = 2 gives a = b = 1/α (THEORY §2.2 row 1 and the §2.5 bridge). **a = b only at p = 2.** α = 2, p = 1 (absolute loss):
a = ⅔, b = ⅓. Check C1 (`c1_resetread_powerloss.py/.json`: Davies–Harte fBm, 60 paths of 2¹⁶ per α, empirical moments at
120 lags, numerical optimum of the cost rate over T, slopes over w and q ×e^{±1.2}): every a, b within 0.019 of the formula
for α ∈ {1.5, 2, 2.5}, p ∈ {½, 1, 2, 4}, except α = 1.5, p = ½ (a 0.921 vs 0.889, 0.03; that case's optimum sits nearest
the lag-1 end of the grid). Moment exponents match pH to ≤ 0.01.

**Linear-priced precision effort, α = 2 (random walk + white noise, steady Kalman).** V ∝ (qN)^{1/2}, effort r = 1/N, so
r\* ∝ w^{a} q^{b} with a = 2α/(2α + p(α−1)), b = p/(2α + p(α−1)) in general (Gaussian errors, V ∝ q^{1/α}N^{1−1/α});
α = 2: 4/(4+p), p/(4+p); p = 2 gives ⅔, ⅓ (§2.2 precision row). Check C2 (`c2_precision_powerloss.py/.json`: exact discrete
Riccati, memory 135–765 steps, numerical optimum): a, b within 0.0015 for p ∈ {½, 1, 2, 4}; Monte Carlo confirms the
Gaussian moment E|e|^p = c_p V^{p/2} to < 1% at one point.

What this does to existing text: §2.2's read-rate and precision-effort rows, and the §2.5 bridge a = b = 1/α, are
quadratic-loss statements; they hold for the lone tracker only at p = 2. For the pooling-onset exponent (§2.5, N12) formal
Theorem 4 (`reviews/night1/formal/THEOREMS.md`) already shows that under **bundled** decisions (Gaussian errors, linear
trackers, loss satisfying its H3) the level's exponent keeps its quadratic value; outside bundling the onset exponent under
a non-quadratic loss is not derived here (FRAMEWORK §6.2 already lists the lone-member absolute-loss value, −2 for R1, as a
rival, which is −(1−b_p)/(1−a_p) at α = 2, p = 1).

## 3. Tracker family under three losses, telegraph world (independent check of pick 35 §3)
Check C3 (`c3_telegraph_ewma_loss.py/.json`, `c3_flatness.json`; own numba code, not pick 35's): one-pole EWMA trackers
(33 gains around the continuous Kalman gain, 9 output scales), pick 35's two points on its grid (Δ = 0.01, N = 1;
A: λ 0.01, μ² 4, κ 0.0025; B: λ 0.02, μ² 2, κ 0.01: q fixed, κ ×4), 4 × 4·10⁷ samples per point (15,895 switches at A),
common random numbers, optimum by local quadratic fit in ln g. t_A = mean zero-crossing time after a switch.

| Loss (best EWMA for it) | A→B Δln t_A at fit | range over gains within 0.5% of the minimum loss | share of Bayes move |
|---|---|---|---|
| sign (0–1) | +0.32 | +0.24 to +0.34 | 0.67–0.95 (exact one-pole, ledger 175: +0.318, 0.90) |
| squared error (scale 1) | −0.01 | −0.07 to +0.12 | below the kill line |
| absolute error (best scale) | −0.19 | −0.36 to +0.01 | opposite sign |
| continuous Kalman gain (fixed) | −0.07 | — | — |
| Bayes (lattice, `tools/discrete_ta.py`, switch law) | +0.36 (0.664 → 0.951) | — | 1 |

Sign-error minima 0.0097 (A) and 0.0294 (B) reproduce pick 35's 0.0097–0.0101 and 0.0292–0.0301. **Pick 35's finding
reproduces**: under a sign payoff the best one-pole linear tracker moves most of the Bayes move, above the κ_F = ½ kill line
(0.18), so a Bayes-locked causal test cannot fail it at any n. My central value (+0.32, 89%) agrees with the reviewer's exact
one-pole value (+0.318, 90%; `CAUSAL_NULL_INVARIANCE_REVIEW.md` Q2, written in parallel, read after my run) and not with the
authored 70–81%; across richer (two-pole) linear kernels the reviewer finds 90–105%. All C3 results are for the **one-pole
(EWMA) family**; the MSE and absolute-loss rows are not claimed for richer linear kernels. New: under **absolute** loss the best one-pole tracker moves the
other way (−0.19), and under squared error about zero, so for those losses the same test does discriminate. The direction
of the linear rival's move is loss-dependent, not just its size. (MSE and absolute minima are flat too: the ranges are wide.)

## 4. Proposed text (author-only PR; DO NOT MERGE without separate reviewer PASS)
- **§1 N6, "The number" column:** after "exactly one optimum … is locked in the prereg before the data, and it is the one
  scored", add: the prereg also fixes the **loss** the optimum is computed for (the error-cost shape ℓ, measured on the system
  per FRAMEWORK §3.3, or ℓ = e² stated as an assumption) and computes any named rival optimum **for the same loss and a
  named rival family** (e.g. one-pole linear, or all linear kernels up to a stated order).
- **§1 N6, "How it dies" column:** a test reported as telling the locked optimum from a named rival optimum shows, at lock,
  that its FAIL rule reaches that rival with probability ≥ π on the planned data (MV10 discrimination line); if not, its
  result is labelled non-discriminating between them.
- **§2.2, new premise bullet (after "One rule, credited"):** quadratic loss; the power-loss elasticities of §2; Sherman's
  invariance for the filter in a Gaussian world; loss dependence of the best linear tracker in a non-Gaussian world (§3).
- **§2.5:** the bridge's a = b = 1/α is the p = 2 case; the premise list of the binding rule gains "the loss".
- **FRAMEWORK MV10:** one sentence for the discrimination line; `tools/power_gate.py --rival-effect` (report-only; added on
  `q-pick37`, does not change `gate_met`; 2 new tests, 33 pass) prints P(FAIL | rival true) and flags
  `rival_unreachable_any_n` when the rival's predicted move is at or above the kill line. Pick 35's numbers: Bayes move 0.350,
  σ 0.028, κ_F ½ → rival +0.318 (exact one-pole) or 0.32–0.37 (two-pole): unreachable at any n; Kalman −0.068:
  P(FAIL | rival) > 0.999. (The tool's unit tests use pick 35's authored +0.244/+0.284; the corrected values give the same
  verdict.) As the reviewer notes, a Bayes-vs-linear test should use a graded (quadratic) payoff, or an observable other than
  mean t_A.

Not proposed: an invariance clause for nulls (pick 35's ruling stands for its reviewer), or any κ_F change (that is
CAUSAL-KAPPA-LENIENCY).

## 5. Prior art (read only where stated)
- Sherman, S. 1958, "Non-mean-square error criteria", *IRE Trans. Inf. Theory* 4(3):125–126, doi 10.1109/TIT.1958.1057451:
  **abstract read**; the statement (Gaussian X, linear estimators, symmetric nondecreasing g ⇒ same argmin as MSE) and its
  proof read in A. Dytso's 2016 Princeton lecture slides ("Overview and New Advances on the Interplay Between Estimation and
  Information Measures", slides "LMMSE Optimality for General Cost Function"). The full 1958 paper was not read.
- Piet, El Hady & Brody 2018 and Glaze, Kable & Gold 2015: as read and reported in pick 35 (not re-read here).
- The power-loss elasticities are ELEMENTARY (one-line calculus on a self-similar moment); I did not search for a prior
  statement, so no novelty is claimed. Reis 2006 and Alvarez, Lippi & Paciello 2011 (cited in §2.2) use quadratic loss (not
  re-read here).

## 6. Surprises (rule 4)
- **Weak-moderate:** the §2.5 bridge a = b = 1/α, on which the reset-read onset exponent −1 rests for a lone tracker, is a
  quadratic-loss fact; T4 protects only the bundled case. A system with a measured non-quadratic, separable loss has no
  derived onset exponent.
- **Weak:** under absolute loss the best one-pole tracker's t_A response to the q-fixed κ ×4 change has the opposite sign to
  Bayes; the loss sets the rival's direction, not only its size.

## 7. Questions for the separate reviewer
1. Is "ℓ measured per FRAMEWORK §3.3, or e² stated as an assumption" the right default, or should an unmeasured loss make a
   prereg exploratory?
2. Is the discrimination line correctly a label rule ("non-discriminating") rather than a kill or gate change?
3. Re-derive a_p, b_p and the precision exponents with own code; is the α = 1.5, p = ½ discrepancy (0.03) grid-limited?
4. Is the §2.5 wording (bridge is the p = 2 case; Theorem 4 covers bundled decisions) accurate to Theorem 4's hypotheses?
5. Re-check C3's absolute-loss sign (−0.19; flat minimum, range −0.36 to +0.01).
