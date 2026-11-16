# PREREG-LOSS-LOCK-REVIEW — independent review of PR #73 (THEORY v1.4.16 / CLAIM_MAP v2.36, pick 37)

Out-of-cycle, unscored (independent review of pick 37 author PR per t1916); ledger 185. Reviewer: independent reviewer
executor (for Ace, Chad t1914/t1916). I authored none of pick 37, `PREREG_LOSS_LOCK*`, PRs #72/#73, N6's kill text, the
CAUSAL-NULL-INVARIANCE work or formal Theorem 4. Sunday 15 November 2026, about 7:54–8:15 PM ET. Own code, imported from
nothing of the author's: `PREREG_LOSS_LOCK_REVIEW_checks/` (all runs at nice 19). In-model checks only; no data outcome
computed; no test locked. Nothing posted or sent; repository private. Vigilance (H8) stays OPEN.

## Verdict: PASS-WITH-FIXES (merged)
The core is right from first principles. An optimum is the argmin of §2.1's J, and J contains w·E[ℓ(e)], so the loss is
an input of every §2.2 number in the same way α, q, N and w are. A prereg that does not fix it leaves a free choice
that could be made after the data, and a rival computed under a different loss is a confounded comparison. Fixing the loss
and the rival family at lock, and labelling a test that cannot reach its rival as non-discriminating, closes a real gap
that pick 35 exposed. The exponents re-derive exactly. The fixes below tighten scope, correct two numbers, and add the
default and prospective clauses N6 needs so that no locked verdict changes silently.

## 1. Re-derivation (own code)
- **Reset reads, |e|^p (`r1_symbolic.py`).** With Gaussian errors, the time-averaged loss over a read interval is
  k_p q^{p/2} T^{pH}/(1+pH). Minimising c/T + w·(that) in sympy gives a_p = 2/(2+p(α−1)) in stakes and
  b_p = p/(2+p(α−1)) in q, so a_p = b_p iff p = 2 (sympy solve). At α = 2 these are formal Lemma 1(iv)'s 2/(p+2) and
  p/(p+2), so the α = 2 case is already in the repo (also Corollary 4.1: a lone R1 member under absolute loss shows (⅔, ⅓)).
- **Precision effort (`r1_symbolic.py`, `r3_precision.py`).** With V = K q^{1/α}N^{1−1/α} and effort r = 1/N priced
  linearly: a = 2α/(2α+p(α−1)), b = p/(2α+p(α−1)) (FOC residual ~10⁻¹⁵). Independent of that scaling assumption, I
  computed V by quadrature of the causal-filtering error integral (N/π)∫₀^∞ ln(1 + qω^{−α}/N) dω (it matches the §2.2
  closed form q^{1/α}N^{1−1/α}/sin(π/α) to 10 digits) and optimised J numerically. At α ∈ {1.5, 2, 2.5} and
  p ∈ {½, 1, 2, 4} every elasticity matches the formula within 10⁻⁵. The author checked α = 2 only.
- **fBm moments (`r2_resetread_discrete.py`).** Own Cholesky fGn (n = 1024, 400 paths): the slope of ln E|X_t − X_0|^p
  on ln t equals pH within 0.012 over all 12 (α, p) pairs.

## 2. Answers to the report's §7 questions
**Q1. Default loss.** "ℓ measured per FRAMEWORK §3.3, or e² stated as an assumption" is the right default. Treating an
unmeasured loss as making a prereg exploratory would be inconsistent with how every other premise is handled: §2.5's
binding rule asks that premises be stated and checked, not that each be measured. It would also retire most effort tests
for a premise that does not move loss-invariant predictions. Those include the linear filter at a given noise level in a
Gaussian world (Sherman) and the Bayes act in the symmetric two-state world. What *was* missing is what happens when a prereg
names no loss. The existing N6 has a default for the optimum ("a prereg that names none is scored against the best
linear optimum"), and the loss needs the parallel default; without it, every earlier prereg would be in limbo. Fix applied: "a prereg that
names no loss is scored under squared error, the loss every §2.2 row is computed for". Recommended, not applied (it would
be new kill text): a prereg whose locked prediction is loss-sensitive (effort elasticities; a linear rival in a
non-Gaussian world) reports its prediction at one alternative p. Queued as LOSS-SENSITIVITY-REPORT.

**Q2. Label, not kill or gate.** Correct. MV10 already requires P(FAIL | the null its FAIL rule targets) ≥ π. The
discrimination line concerns a different null, the rival optimum. A test that cannot reach the rival can still be a
valid test of the shared prediction against its own null. Turning that into a gate failure would block legitimate tests,
and turning it into a kill would be a category error. The label prevents the one real abuse, which is reporting a pass
as evidence for Bayes over linear (or any optimum over its rival) when no outcome could have favoured the rival. The
FRAMEWORK sentence "at or above the kill line … no sample size reaches it" is right for the one-sided causal rule: at
equality P(FAIL | rival) tends to the one-sided test size, not to π.

**Q3. Exponents; the α = 1.5, p = ½ gap.** Confirmed exactly (§1). The 0.03 gap is a sampled-time effect, not grid noise
in the formula. In a sampled-time model, with reads every T steps (T made continuous through the Hurwitz zeta, so the lag
sum is exact), the stakes elasticity at α = 1.5, p = ½ is 0.991 at T\* ≈ 49, 0.900 at T\* ≈ 418 and 0.8890 at
T\* ≈ 2.5×10⁴, against 0.8889. Convergence is slowest exactly where pH is small (here pH = 0.125), because the loss then
grows so slowly with T that the discrete lag-0 term matters out to long intervals. The bias has the author's sign. At
p = 2, α = 2 the sampled model is exact at every T. (`r2_resetread_discrete.out`.)

**Q4. §2.5 wording vs Theorem 4.** The bridge edit is accurate: Lemma 1(i) is a squared-error statement, and the |e|^p
generalisation is the p = 2 case's extension (credit Lemma 1(iv) for α = 2; added). The §2.2 Theorem 4 sentence needed
three fixes. (a) Theorem 4's hypotheses are Gaussian drift, linear trackers, bundled loss, H3, small ρ and h = 0, not just
"Gaussian errors, linear trackers"; these are now listed. (b) H3 depends on α. For R1 in fBm, κ_ℓ = E_t[L′(V_u(t))] with
V_u ∝ t^{α−1} and L′ ∝ v^{p/2−1} is finite iff p > 2(α−2)/(α−1) (`r1_symbolic.py`). That is every p > 0 at α ≤ 2, but
only p > ⅔ at α = 2.5. Theorem 4 states H3 at the Brownian case ("iff p > 0"), and its numerical checks are at α = 2
only. (c) "Outside bundling the onset exponent under a non-quadratic loss is not derived" was wrong at α = 2. Theorem
4's own exact checks and Corollary 4.2 give the separable reset-read values −1.996 (p = 1) and −0.499 (p = 4), which are
the lone-member −(1−b_p)/(1−a_p) = −2/p. Text now: −2/p at α = 2 for reset reads; not derived at other α or for priced
precision (QUEUE SEPARABLE-LOSS-ONSET). The report's "weak-moderate" surprise is therefore weaker than stated. At α = 2,
the fact that a = b only at p = 2 and that the lone-member exponent then misleads was already Corollary 4.1. What is new
is the general-α form.

**Q5. Absolute-loss sign (`r4_telegraph_grid.py`, `r6_convergence.py`, `r6_summary.out`).** This is my own exact grid
engine: the joint (x, z) chain, a cell-integrated Gaussian kernel, the stationary law by sparse solve, and t_A from
generating functions with overtaken passages dropped, as defined in the PR #70 review's Method. The one-pole family is
z ← f z + (1−f) y with a free output scale c. The Bayes tracker uses the same engine on the log-odds. Results at 6 and 12
cells per kernel sd agree within 0.002 in Δln t_A. My Kalman t_A at A is 1.6384, the PR #70 review's value.

| Tracker (A → B, q fixed, κ ×4) | t_A at A | t_A at B | Δln t_A | share of Bayes |
|---|---|---|---|---|
| Bayes | 0.6629 | 0.9446 | +0.354 | 1 |
| sign (0–1)-best one-pole (pole ×2.27 / ×1.55 Kalman) | 0.724 | 0.996 | +0.318 to +0.319 | 0.90 |
| squared-error-best one-pole, scale free (= Kalman, pole ×1.000) | 1.639 | 1.532 | −0.068 | −0.19 |
| absolute-error-best one-pole, scale free (pole ×0.565 / ×0.660) | 2.837 | 2.265 | −0.225 | −0.64 |

The absolute-loss sign is **confirmed**: −0.23 exact, where the author's Monte Carlo gave −0.19. The absolute-best
tracker smooths more than Kalman (t_A 2.84 against 1.64 at A).

The squared-error row was **wrong in the PR**. The author's "about 0 (−0.07 to +0.12)" fixed the output scale at 1. With
the scale free, the squared-error-best one-pole tracker is the Kalman filter (my argmin is ×0.9997 of the Kalman pole),
which moves −0.068. Because the telegraph world's autocorrelation is exponential, Kalman is also the best of *all*
linear kernels under squared error, so for this loss the "one-pole only" caveat is unnecessary. The direction claim
stands, and is sharper: the best linear rival's direction depends on the loss.

The minima are flat. Across poles within 0.5% of each minimum loss, Δln t_A spans about ±0.2–0.3 (`r5_flatness.out`), so
a learner selected on a finite record can sit well away from the exact argmin. The text now says so.

## 3. Sentence-by-sentence (causal correctness and overreach), with the fixes applied
- **N6, number column.** The loss and rival family are fixed at lock, and the rival is computed for the same loss. This is
  right: comparing optima computed for different losses confounds the loss with the mechanism. *Added* the squared-error
  default.
- **N6, kill column.** "Switching … to another loss, after the data are seen is not allowed" is right and closes a rescue
  route. The discrimination label is right (Q2). *Added*: these requirements bind preregs locked after v1.4.16, and no
  earlier verdict is relabelled (§4).
- **§2.2 premise, (i).** "In any world" was overreach. The derivation needs E ℓ = c_p V^{p/2}, that is, an error law whose
  shape is fixed as its scale moves (Gaussian here). A non-Gaussian self-similar world gives different exponents (Lemma 1(v),
  α-stable), and a non-self-similar one gives none. → "Gaussian errors". Credit for the α = 2 case was added, and the
  checks are stated as performed.
- **(ii) Sherman.** I read the Sherman 1958 abstract (*IRE Trans. Inf. Theory* 4(3):125–126, doi
  10.1109/TIT.1958.1057451, via the DOI landing page's indexed text; Crossref metadata confirmed). It states that for
  Gaussian processes the non-mean-square criteria "given in three recent textbooks" yield Wiener's linear MMSE predictor,
  which is narrower in wording than "every symmetric, nondecreasing loss". The general class (losses symmetric about 0 and
  nondecreasing in |e|, Gaussian conditional law) is the standard statement. The author read it in a secondary source,
  and the paper's own reference list includes Sherman 1955 (*Ann. Math. Stat.* 26:763–767), which I could not open. I also
  read the abstract of Brown 1962, "Asymmetric non-mean-square error criteria", *IRE Trans. Automatic Control* 7:64–66
  (doi 10.1109/TAC.1962.1105406), which calls the symmetric result "well known" for Gaussian inputs. The text now states
  exactly what was read. "So the memory-time row at a given noise level is loss-free, while the chosen noise level moves
  with p" is correct.
- **(ii) two-state numbers.** "This file's own Monte Carlo" (THEORY is not the source) → the report's. The squared-error
  and absolute numbers were corrected per Q5, and the flatness was stated.
- **(iii) Bayes act.** Correct. In the symmetric two-state world the posterior mean μ(2π−1), the posterior median
  μ·sign(π − ½) and the sign act all change sign at π = ½, so zero-crossing t_A is loss-invariant across these three
  losses. An asymmetric loss moves the threshold. My Bayes t_A (0.6629 → 0.9446) reproduces the PR #70 review's
  0.6630 → 0.9447.
- **Consequences.** The Theorem 4 sentence was fixed per Q4. "A test meant to tell Bayes from linear uses a graded
  (squared-error) payoff" is consistent with Q5 (absolute error also discriminates, with the opposite sign).
- **§2.5 bridge and the binding rule's premise list.** Accurate. The Lemma 1(iv) pointer was added.
- **FRAMEWORK MV10 discrimination line.** Accurate. `tools/power_gate.py` tests pass (21/21 in `test_power_gate.py`),
  and `--rival-effect` is report-only and does not change `gate_met`.
- **CLAIM_MAP v2.36 note.** "N13 gains a scope pointer" suggested a row edit that does not exist; reworded. A review
  summary was added. No status changed.

## 4. Locked preregs: does any verdict silently change? No.
I checked every locked file in `tests/*/PREREG*.md`, `PREDICTIONS.md`, `tests/DECISIVE/*/PREREG.md`, `prereg/*/PREREG.md`
and `reviews/night2/KERNEL_PROXY_PREREG.md` and `reviews/night2/CAUSAL_NULL_INVARIANCE/PREREG.md` for a stated loss and
for a reported locked-optimum-vs-rival-optimum discrimination.
- **States its loss already:** STAKES_EXOGENOUS (quadratic; it even tests the shape, S2), WIKIDATA-BAND (quadratic),
  ONSET_ACROSS_ALPHA (bundled quadratic), CAUSAL_NULL_INVARIANCE in-model (MSE payoff; rival Kalman = the MSE-best
  linear for the same loss; MV10 shown at lock), LEARNSIM (bundled loss).
- **Names no loss:** KERNEL_MEASURE, KERNEL_PROXY, LAB_AKLMT_TAU (N23), LFK_SPF, SPF_NOISE_PROXY, SPF_RIGIDITY_OOS, D3_OOS,
  C3, C3b, F1, DRIFT1, ANTS1, BIO1, COLLAPSE1, MATCH1, DECISIVE (3), STAKES_SHIFT_CAISO, vigil-ona. Under the added
  default these are scored under squared error, which is what they implicitly used: kernel and forecast regressions are
  least-squares objects, and LAB_AKLMT's AR(1)-Gaussian world makes the linear forecast loss-invariant anyway. So no
  verdict moves.
- **Reports a discrimination from a rival optimum:** KERNEL_MEASURE ("three rival kernels excluded"; already labelled
  exploratory because MV10 failed at lock); KERNEL_PROXY (P1 rival discrimination shown at lock, P 0.998: compliant);
  LFK_SPF (rival R-M = α forced to 2; primary INCONCLUSIVE, MV8 failed: nothing claimed); CAUSAL_NULL_INVARIANCE
  (compliant). None would be relabelled.
- **Ruling:** the rule applies going forward. Locked files cannot have satisfied a rule written after their lock, and
  relabelling them now would itself be a post-lock change. The inventory shows that applying the rule retroactively would
  change nothing in any case. N6 now says this explicitly.

## 5. Prior art (counted only where read)
Read by me: the Sherman 1958 abstract; the Brown 1962 abstract; formal Lemma 1, Theorem 4 and Corollaries 4.1–4.2 in
`reviews/night1/formal/THEOREMS.md` (in-repo prior statement of the α = 2 power-loss elasticities and of the separable
exponents). Not read: Sherman 1958's full text, Sherman 1955, and the Dytso slides (the author's secondary source). The
general-α power-loss elasticities remain ELEMENTARY, and I made no novelty claim. No outside search for them was made.

## 6. New queue items
- **LOSS-SENSITIVITY-REPORT** (w 1, c 0.5): a prereg whose locked prediction is loss-sensitive reports it at one
  alternative p (or across the measured p's CI). Kill-text edit, so it needs an author-only PR and a separate reviewer.
- **THM4-H3-ALPHA** (w 1, c 0.5): Theorem 4's H3 and its exact checks at α ≠ 2. H3 for R1 in fBm needs
  p > 2(α−2)/(α−1), and the bundled exponent for p at or below that bound at α > 2 is not derived.

## 7. No locked goalpost moved
No file under `tests/`, `prereg/` or any `reviews/night2/*PREREG*` is touched by this review or by PR #73. No verdict,
headline, locked prediction or CLAIM_MAP status changed. N13 and N6 stay OPEN, N16 is unchanged, and vigilance stays
OPEN. "Theory", not "law".
