# Robustness, redundancy and antifragility in the cost of judgment (v2.7 draft, 20 November 2026)

Written by one executor for Chad (his t2007 question, relayed by the parent agent), on branch `v2.7-robust` off `main`
at `45a70cf`. **A self-check, not independently reviewed.** Labels: **PROVED (in-model)** = a theorem inside the stated
model, checked numerically; **PRIOR ART** = published by others; **OPEN** = not shown; **UNTESTED** = a preregistered
prediction about real systems with no data yet. Checks: `theory/robust_checks/` (run by `tools/test_robust_checks.py`);
DOIs verified on Crossref in `theory/robust_checks/crossref.out`.

## 0. The question and the short answer

*Chad's question:* are the designs that minimize J = κI_mem + hK + w·E[ℓ] + A + L subject to P(ruin) ≤ ε already
fail-proof, because the ruin constraint is in the master equation, or must extra parts be added?

**Short answer.** The *form* is right and does real work: survival enters as a hard chance constraint, not averaged
into the cost, so a system cannot trade a small chance of ruin for a lower mean cost. Once a risk is *in the model*,
the same J produces its own defences, with nothing added: buffers (CT25), faster checking (Theorem L, CL2), and, once
component failure is put into the design space, **redundant copies** (CT37, new here). But the minimizer is exactly as
safe as ε **under the model, and no safer**: whenever the ruin constraint binds, the cost-minimizing design has
**zero margin** against anything outside the model (CT39). Two things therefore have to be put *into* J's problem
rather than bolted on: (1) the failure modes (component failure, common-mode failure), and (2) the uncertainty about
the world's parameters and tail. With (2) in, the theory itself prescribes reserve **above** the fitted-model minimum,
growing with that uncertainty (CT38). Antifragility proper (gaining from disorder in absolute terms) is **not** implied
by the fixed-world theory; two weaker, precise forms are (CT40).

So: not "extra parts beyond the theory", but also not "already baked in" as the repository stood. The constraint
is the right place; what it protects against is only what the model contains.

## 1. What the current theory already implies (read from `THEORY.md` at `45a70cf`)

| Item | What it says about robustness | Where |
|---|---|---|
| Ruin as a chance constraint | P(ruin) ≤ ε_r is a constraint, not a fourth cost term; the expected-cost rules are exact only above B_slack | §3; (iv); CT22 |
| Price of survival | Below B_min nothing is certified; between B_min and B_slack the constraint binds with multiplier μ_s > 0 and moves the design toward Theorem L's survival-optimal end | CT22 |
| Buffers | per-window ruin ≤ ε ⇔ B ≥ z_ε·σ·τ^H; faster correction raises the survivable shock | CT25, CT18 |
| Checking under survival | the survival-optimal interval is shorter than the cost-optimal one; extra effort is worth most at θB ≈ 1 | CL2 (Lemma B9) |
| Copies for accuracy | with independent *store* noise, two copies of one layer nearly double its value, best at **one** time constant; shared sensing noise gives copies nothing | `theory/STORE_NOISE.md` E1-c |
| Fragility at the edge | near feasibility edges (B_min, the lookup cliff) regret is not smooth: a picture error can flip survival | CT23 exceptions |
| Where (ii) fails | with ruin binding, judgment spend can *fall* as stakes rise (a costlier, safer design becomes uncertified); cost shares stop equalling elasticities | (ii), CT33, CT24 |
| Stress strengthening | "stress strengthens up to a ceiling": only the ceiling half is in-model | K7 (OPEN) |
| Making the world calmer | effort g that reduces drift is a lever the theory names and holds at zero | CL11, CX2 (OPEN) |

**Corrections to the parent's preliminary read.** (a) "No parallel copies in the design space" is not quite right:
`STORE_NOISE.md` E1-c already makes copy number a priced design variable, but for **noise**, not **failure**.
(b) "Nearly all theorems assume ruin slack" is right for (ii), CT24 and CT33; existence (i) and the layer cap (iii)
do not involve ruin, and CT22, CT25 and CL2 are the binding-ruin results.

**What it does not contain.** No component in 𝓜_LG can fail (ruin is only the reserve hitting zero); ε is computed
under the assumed world, with its parameters known; and the world is fixed (g = 0), so nothing can gain from disorder.

## 2. Setting for the extensions
Everything below is in-model. R1 uses one needed layer realized by n copies over windows of unit length. R2-e and R3
use CT22's own model (THEORY B.9; `theory/meq_checks/meq_derive.py`): a diffusion reserve with check interval τ,
mean margin m = y − c/τ − wσ²τ/2, variance s² = s₀² + w²σ⁴τ³/3, Lundberg exponent θ ≈ 2m/s², certified iff
θ ≥ ln(1/ε)/B. R4 uses one OU mode read through white noise (𝓜_LG with K ∈ {0, 1}).

## 3. R1 — Redundancy under component failure (CT37, PROVED (in-model); CL18 for the known parts)

*Model.* n independent copies of one layer, upkeep h each per window; each copy is down in a window with probability
p (independently; repaired by the next window). The layer's loss is w·E₁ if at least one copy is up and w·E₀ if all
are down; Δ = E₀ − E₁ > 0. Expected cost J(n) = n·h + w·E₁ + w·Δ·p^n.

**R1-a (expected cost).** J(n+1) − J(n) = h − wΔ·p^n(1 − p) rises with n, so J is discretely convex and
**n_E = 1 if wΔ·p(1−p) ≤ h, else n_E = ⌈ln(h / (wΔ(1−p))) / ln p⌉.** Redundancy pays (n_E > 1) iff
wΔ·p(1−p) > h. n_E never falls as w or Δ rises and never rises as h rises; it grows only **logarithmically** in the
stake, about ln(wΔ/h)/ln(1/p) (slope 1/ln(1/p) checked over eight decades of w). It is **not monotone in p**: copies
are worthless when parts never fail and when they always fail, and pay most at intermediate reliability (they can pay
for some p iff wΔ/4 > h).

**R1-b (catastrophic failure: the ruin constraint sets a floor of copies that is free of stakes and prices).** If an
all-down window is ruin, then over N windows P(ruin) = 1 − (1 − p^n)^N ≤ ε iff p^n ≤ ε₁ := 1 − (1−ε)^{1/N} (≈ ε/N),
i.e. **n ≥ n_R = ⌈ln ε₁ / ln p⌉**, which does not depend on w, h or B. With J convex, **n\* = max(n_E, n_R)**.
Example: p = 0.1, ε = 10⁻³, N = 1000 gives n_R = 6. *Consequence:* with a catastrophic failure mode and an
unbounded horizon (N → ∞), n_R → ∞: a lifetime ruin target with a fixed number of independently failing copies is
infeasible; the master equation's ε then needs a horizon (CL9's finite horizon) or a repair/renewal of the whole.

**R1-c (common mode; PRIOR ART in substance, CL18).** If one common cause takes every copy down with chance β per
window, P(all down) = β + (1−β)p^n ≥ β. If β > ε₁, **no number of copies is feasible**: identical copies buy nothing
against common-mode failure, and only a different design (diversity) or a calmer world helps. This is the
reliability-engineering common-cause limit (Barlow & Proschan, *Mathematical Theory of Reliability*, SIAM reprint
1996, doi 10.1137/1.9781611971194; redundancy allocation reviewed by Kuo & Prasad 2000, doi 10.1109/24.877336), and
it is the failure-side twin of STORE_NOISE E1-c (shared sensing noise gives copies nothing).

**R1-d (non-catastrophic failure paid from a reserve; new in this form).** Let an all-down window cost the reserve a
lump X = wΔ, arriving at rate p^n, on top of the diffusion of CT22: the Lundberg function is
κ_n(t) = −t(y − nh − wE₁) + t²s²/2 + p^n(e^{tX} − 1), θ_n its positive root (Dufresne & Gerber 1991, doi
10.1016/0167-6687(91)90023-Q, for ruin with jumps and diffusion). *Claim:* θ_n ≤ θ_{n_E} for every n < n_E, hence
**the constrained optimum is n\* = min{n ≥ n_E : θ_n ≥ ln(1/ε)/B}**: a binding ruin constraint **adds copies and
never removes them**, and n\* falls to n_E as B rises past B_slack = ln(1/ε)/θ_{n_E}.
*Proof.* For n < n_E, κ_n(t) − κ_{n_E}(t) = t(n − n_E)h + (p^n − p^{n_E})(e^{tX} − 1) ≥ t(n − n_E)h +
(p^n − p^{n_E})tX = t[J(n) − J(n_E)] ≥ 0 for t > 0 (using e^{tX} − 1 ≥ tX and p^n > p^{n_E}). Each κ_n is convex
with κ_n(0) = 0 and κ_n′(0) = −(mean margin) < 0, so a pointwise larger κ has a smaller positive root. ∎
This is the opposite of CT33's binding-ruin case, where spend can fall: copies lower both the mean and the variance
of the jump term, so here survival and cost pull the same way. Checks: 300 random parameter sets, no violation of the
θ ordering, the n\* formula or monotonicity in B; worked case (y = 1, h = 0.05, p = 0.2, X = 2, s = 0.5,
ε = 10⁻³): n_E = 3, and n\* = 7, 5, 3 at B = 1.5, 2, ≥ 3; Monte Carlo ruin by T = 200 stays under e^{−θB}.

**What R1 does not give.** Every copy above sits at **one time constant**. Nothing in R1 makes extra *distinct*
time-scale layers; diversity against common mode (R1-c) would, but its optimal form is not derived (OPEN, CX7).

## 4. R2 — Uncertainty about the world (CT38, PROVED (in-model); CL18 for the known parts)

The ruin constraint is a statement about a probability, and a probability needs a model. If the system (or the
selecting process) does not know σ, p or the tail, "P(ruin) ≤ ε" must be read either under its **predictive**
distribution (Bayes) or for **every** world in an ambiguity set (robust). Both give more reserve than the fitted
(plug-in) model.

**R2-a (reserve and checking under an ambiguity set; PROVED (in-model)).** Choose τ and a buffer B carried at price r:
min c/τ + wσ̂²τ/2 + rB subject to B ≥ z_ε·σ·√τ for every σ ∈ [σ̂, σ̂(1+u)]. With x = √τ and a = r·z_ε·σ̂(1+u),
J(x) = c/x² + (wσ̂²/2)x² + a·x is strictly convex, and at its optimum (sympy, `r2_ambiguity.py`)
**d ln x / d ln a = −a / (8Ax + 3a) ∈ (−1/3, 0)**, A = wσ̂²/2. Hence, as the uncertainty u grows: the robust
interval τ\* falls (check faster), the robust buffer B\* = z_ε σ̂(1+u)x rises with elasticity in (2/3, 1), so
**(1+u)^{2/3} ≤ B\*_robust / B\*_fitted ≤ 1 + u**, and the optimal cost rises (envelope). Under the fitted model the
robust design shows slack: its per-window ruin chance is Φ̄(z_ε(1+u)), e.g. 1.0·10⁻⁴ and 1.8·10⁻⁶ at u = 0.2, 0.5
for ε = 10⁻³. If the cost term is also taken at the worst σ, τ\* still falls and B\* still rises (checked), with a
smaller ratio (1.46 at u = 1 instead of 1.83).

**R2-b (finite record; PRIOR ART: the Gaussian prediction interval).** With σ (and the mean) estimated from n
windows, the buffer with exact coverage 1 − ε for the next shock is t_{n−1,1−ε}·√(1+1/n)·s, not z_ε·s. The factor
over plug-in at ε = 10⁻³ is 2.54, 1.46, 1.19, 1.07, 1.02 for n = 5, 10, 20, 50, 200; the plug-in buffer's true
exceedance at n = 20 is 3.6·10⁻³, 3.6 times ε (exact t distribution; Monte Carlo agrees). Plug-in under-reserves; the gap
shrinks as the record grows.

**R2-c (uncertain failure rate ⇒ more copies; PROVED (in-model), Jensen).** With p uncertain (posterior
Beta(a, b)), P(all n down) = E[p^n] ≥ (E p)^n because p^n is convex, so the predictive copy count is never below
the plug-in count at the posterior mean. E[p^n] = Π_{i<n}(a+i)/(a+b+i). Example (ε₁ = 10⁻⁶, uniform prior):
1 failure in 10 windows gives 6 copies at the MLE, 8 at the posterior mean, **17** predictive; 500 in 5000 gives
6 / 7 / 7. Redundancy rises with how little the system knows about its parts' reliability.

**R2-d (tail uncertainty; PRIOR ART).** At fixed variance and ε = 10⁻³, the one-sided quantile is 3.09 (Gaussian),
3.27 (Student t, ν = 30), 4.57 (ν = 5), 5.90 (ν = 3). If only the mean and variance are trusted, the worst case over
all distributions (Cantelli's bound, tight) needs B ≥ σ√((1−ε)/ε) = 31.6σ, about ten times the Gaussian buffer
(the moment-based distributionally robust chance constraint: El Ghaoui, Oks & Oustry 2003, doi
10.1287/opre.51.4.543.16101; Calafiore & El Ghaoui 2006, doi 10.1007/s10957-006-9084-x). The size of the ambiguity
set, not the fitted variance, decides the slack.

**R2-e (in CT22's own model; PROVED (in-model), numeric).** θ falls as σ rises (m falls, s² rises), so the worst
world in [σ̂, σ̂(1+u)] is its top. B_min rises (0.4864 → 0.4917 as u goes 0 → 2%); at B = 0.51, slack under the
fitted model, the robust interval falls 0.3162 → 0.3028 and its cost under the fitted model rises: the robust design
moves toward Theorem L's survival-optimal end, as a smaller effective buffer would.

**Layer count under uncertainty: OPEN (CX7).** Ambiguity tightens the constraint, so by CT22 the design moves toward
the survival-optimal design; the layer count rises only where that design has more layers, which is not general
(CT33 shows binding ruin can lower spend). Not claimed.

**Who holds the uncertainty (a blind spot, OPEN, CX7).** For a firm, the record is its own few years. For an evolved
lineage, selection has integrated over a much longer record, so the relevant n in R2-b is the lineage's, not the
individual's; an evolved design may then sit near the true-parameter optimum while a young firm should not. The
prediction below therefore uses the system's own record and must preregister, per class, whose record counts.

**Testability guard.** An ambiguity set chosen after seeing a design could excuse any excess reserve. So the
ambiguity is never a free parameter: it is fixed from the system's measured record (R2-b, R2-c) by a rule locked
before data (`prereg/ROBUST-SLACK/PREREG.md`).

## 5. R3 — Lean versus robust (CT39, PROVED (in-model); PRIOR ART in substance)

**Claim.** In CT22's class, when the ruin constraint binds (B_min < B < B_slack), the cost-minimizing design is
certified with **zero margin**: θ(𝒟\*) = ln(1/ε)/B exactly (complementary slackness), so any adverse change in a
parameter that θ strictly decreases in (σ here) voids the certificate at first order. When the constraint is slack
the margin is positive and grows with B. *Numbers:* the largest σ rise the optimal design survives is 0 at
B = 0.49, 0.50, 0.505 (binding), and 2.6%, 16%, 49%, 104% at B = 0.52, 0.6, 1.0, 5.0; at B = 0.5 a 1% rise in σ
puts the Lundberg bound at 1.057·ε. And a risk that is not in the model at all (a jump of size above B at rate λ)
gives P(ruin by T) ≥ 1 − e^{−λT} for every design in the class, whatever ε says.

**Reading.** The theory's optimum is "fail-proof" only in the sense P(ruin) ≤ ε, only against risks in the model,
and, where survival binds, with nothing to spare. Cost minimization pushes designs onto the edge of what the model
certifies; that is the theory's own version of "robust yet fragile". Prior art: highly optimized tolerance (Carlson &
Doyle 1999, doi 10.1103/PhysRevE.60.1412; 2002, doi 10.1073/pnas.012582499) showed that designs optimized against
anticipated disturbances are fragile to unanticipated ones; robust optimization (Ben-Tal & Nemirovski 1998, doi
10.1287/moor.23.4.769; Ben-Tal, El Ghaoui & Nemirovski 2009, doi 10.1515/9781400831050) and chance-constrained
programming (Charnes & Cooper 1959, doi 10.1287/mnsc.6.1.73; Nemirovski & Shapiro 2006, doi 10.1137/050622328)
are the standard repairs. What is the theory's own is only the placement inside J and the link to CT22's μ_s.

## 6. R4 — Antifragility (CT40, PROVED (in-model) for (a)–(c); (d) OPEN)

Setting: 𝓜_LG, ruin slack, world signal scaled by a ("volatility"), sensing noise fixed.

- **(a) No absolute gain from volatility.** At a fixed design the error is affine in a, E = a·V_S(𝒟) + V_N(𝒟) with
  V_S ≥ 0, so J\*(a) = min over designs is **concave and nondecreasing**: more volatility never lowers the best
  attainable cost. The fixed-world theory cannot produce Taleb-style antifragility in absolute terms.
- **(b) Judgment gains relative to a blind rival.** The blind system's cost is linear in a, so the tracker's advantage
  Δ(a) = J_blind(a) − J\*(a) is **convex**; with Δ(0) = 0 and Δ ≥ 0 it is also nondecreasing (if Δ fell between
  a₁ < a₂, convexity would give Δ(a₁) ≤ (a₁/a₂)Δ(a₂) ≤ Δ(a₂)). Volatility widens the edge of judgment over no
  judgment, convexly: the selective advantage of a model grows with disorder even though every system pays more.
- **(c) Gain from volatility of volatility needs the option to redesign.** If a switches between regimes and the
  system re-optimizes in each, E[J\*(a)] ≤ J\*(E a) (Jensen, concavity): fluctuating volatility costs *less* on
  average than steady volatility of the same mean. With one fixed design, E J(𝒟, a) = J(𝒟, E a): no gain. Worked case
  (a ∈ {0.5, 4.5}): fixed design 1.631, redesign per regime 1.336 (18% lower). The convexity that makes gain from
  disorder possible is the **option to redesign**, worth having only when redesign is faster than regime change and
  cheaper than this gain; redesign cost is not in J (OPEN). This is Taleb's point that optionality is the source of
  antifragility (Taleb, *Antifragile*, Random House 2012; a book, no DOI), and the value of flexibility in real
  options, read inside J; known in substance.
- **(d) Stress that makes the system stronger** (overcompensation; K7) needs an adaptation rule and the drift-reduction
  lever g (CL11). Not implied; OPEN. A binding ruin constraint also breaks (a)–(c), since the feasible set then
  depends on a.

Related, not used: maxmin and robust-control decision rules (Gilboa & Schmeidler 1989, doi
10.1016/0304-4068(89)90018-9; Hansen & Sargent 2001, doi 10.1257/aer.91.2.60); growth versus security in fractional
Kelly betting (MacLean, Ziemba & Blazenko 1992, doi 10.1287/mnsc.38.11.1562); bet hedging (Philippi & Seger 1989,
doi 10.1016/0169-5347(89)90138-9); biological robustness and degeneracy (Kitano 2004, doi 10.1038/nrg1471; Edelman &
Gally 2001, doi 10.1073/pnas.231499798); distributionally robust optimization under moment uncertainty (Delage & Ye
2010, doi 10.1287/opre.1090.0741).

## 7. Known parts, new claim
| Result | Label | Known | New here |
|---|---|---|---|
| R1-a copies under expected cost | PROVED (in-model), CT37 | parallel-redundancy allocation (reliability engineering) | the closed form inside J; logarithmic growth in stakes |
| R1-b stake-free copy floor from the chance constraint | PROVED (in-model), CT37 | chance-constrained reliability | that J's ruin constraint, not the stakes, sets it; infinite-horizon infeasibility |
| R1-c common-mode floor | PRIOR ART, CL18 | common-cause failure | the link to STORE_NOISE E1-c |
| R1-d binding ruin adds copies, never removes them | PROVED (in-model), CT37 | Lundberg with jumps (Dufresne & Gerber) | the ordering θ_n ≤ θ_{n_E} and the n\* formula, as far as found (not searched exhaustively) |
| R2-a robust reserve: B ratio in [(1+u)^{2/3}, 1+u], faster checks | PROVED (in-model), CT38 | robust optimization | the closed elasticity in this design problem |
| R2-b prediction-interval buffer | PRIOR ART, CL18 | classical statistics | — |
| R2-c Jensen: predictive copies ≥ plug-in | PROVED (in-model), CT38 | Bayesian reliability (in substance) | the copy-count reading |
| R2-d tail and moment ambiguity | PRIOR ART, CL18 | Cantelli; El Ghaoui et al.; Calafiore & El Ghaoui | — |
| R2-e robust design in CT22's model | PROVED (in-model), CT38 | — | the numbers in the theory's own model |
| R3 zero margin when ruin binds | PROVED (in-model), CT39 | HOT; robust optimization | the link to μ_s |
| R4 (a)–(c) | PROVED (in-model), CT40 | concavity of a minimum of affine functions; optionality | the reading inside J |
| Who holds the uncertainty; robust layer count | OPEN, CX7 | — | — |
| ROBUST-SLACK prediction | UNTESTED (OPEN), CX8 | precautionary cash rises with risk; duplicate genes buffer nulls | dependence on the system's own record length at fixed estimated risk |

## 8. Implication for the GRID diagnosis (PR #113)
GRID-DX B1 computes K\* = 1 for GB **with ruin slack**. The results here do not rescue the three extra layers:
CT37 and CT38 produce more copies at one time constant and larger buffers, not extra distinct time scales. They do
say that GB's reserve *volumes* cannot be called waste from a plug-in calculation alone, because a selected system
should hold more than the plug-in minimum. If anything explains extra speed layers it is a cost not on J's list
(fast units that cannot run long: a speed–endurance trade-off), which would have to be added publicly before any
future test. Stated in `prereg/ROBUST-SLACK/PREREG.md` §5 before any data. GB stays NOT APPLICABLE (not qualified).

## 9. Open gaps
1. Robust layer count, and the optimal form of diversity against common mode (CX7).
2. Whose record sets the uncertainty: individual or lineage (CX7).
3. Redesign cost, so R4(c)'s option has a price (OPEN).
4. Stress strengthening and the drift lever (K7, CL11).
5. Correlated failures beyond one common cause; failures that are not window-renewed (ageing).
6. The ROBUST-SLACK prediction is UNTESTED; no dataset has been opened.
7. Independent review of everything here.

## Files
`theory/robust_checks/r1_redundancy.py`, `r2_ambiguity.py`, `r3_lean.py`, `r4_antifragile.py`, `results.out`,
`crossref_check.py`, `crossref.out`; `tools/test_robust_checks.py`; `prereg/ROBUST-SLACK/PREREG.md`.
