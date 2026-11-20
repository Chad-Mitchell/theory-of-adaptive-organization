# DYNAMICS: redesign cost, the lineage objective, and time averages (v2.9 draft)

20 November 2026, about 2:45 PM ET (America/New_York). Branch `v2.9-dynamics` off `main` at `1597218` (PR #113 merged).
Written by one executor for Chad Mitchell after a separate wide-net scan of antifragility and optimal design (Chad's
t2015 request); the scan's top three findings and its two OVERREACH verdicts were re-derived here from scratch before
anything was written. **A self-check, not independently reviewed.** Checks: `theory/dynamics_checks/` (d1–d4, run by
`tools/test_dynamics_checks.py`); DOIs: `theory/dynamics_checks/crossref.out`.

Status words as in THEORY.md: **PRIOR ART** (a published result, credited), **PROVED (in-model)** (a derivation inside
the stated model, which says nothing by itself about nature), **OPEN** (untested, not refuted). Row IDs CT41–CT43,
CL19–CL21, CX9–CX10 skip the IDs that open PR #115 uses (CT37–CT40, CL18, CX7, CX8).

## 1. What changes and what does not

**The master equation is unchanged.** J, its terms and the ruin constraint stay as THEORY §2 states them. Everything
here is an **extension** a substrate class may put on its closed term list before a test (THEORY §3 item (1)), plus one
amendment to a kill rule that was too strict. In a stationary world (A2) with fixed inputs nothing is ever redesigned,
the extension's extra term is zero, and J is recovered exactly.

Three things J, as a per-unit, per-moment average, does not see:
1. **Changing the design costs something** (§2). With a lump-sum cost, a correct design often does not move when its
   inputs change. The current kill rule would score that as a miss.
2. **Selection may act on a lineage, not a unit** (§3). When shocks hit many units at once, the lineage's long-run
   (geometric) growth is maximized by a *mixture* of designs: bet-hedging. No per-unit argmin produces a mixture.
3. **A time average is not an ensemble average when stakes compound** (§4). For additive stakes, and for stakes that act
   on the log of the reserve, J is already the time average. For lumpy losses that act on returns it is not.

## 2. Redesign cost and the inaction band

**Extension (stated minimally).** Write 𝒟_t for the design in force and 𝒟\*_t for argmin J at the inputs in force. The
dynamic cost is the long-run rate

  J_R = lim (1/T) E[ ∫₀ᵀ J(𝒟_t) dt + Σ_{redesigns i ≤ T} k_i + ∫₀ᵀ κ |d𝒟_t/dt|² dt ],

with k ≥ 0 a lump-sum cost per redesign and κ ≥ 0 a smooth (convex) adjustment cost. With fixed inputs, J_R = J\*. Near
its minimum J is flat, J(𝒟) − J(𝒟\*) ≈ w·x² along the direction of a move, with x = 𝒟 − 𝒟\* the gap and w = H/2
(THEORY §3, "From a cost band to a design band").

**CL19 (PRIOR ART; re-derived in `d1_redesign_band.py`).**
- (a) *Lump-sum cost, drifting optimum* (𝒟\* a Brownian motion with variance rate σ²): the best policy leaves the gap
  alone until |x| reaches b\* = (6kσ²/w)^{1/4}, then resets it to zero. The excess cost rate is kσ²/b² + wb²/6, minimal at
  b\* with value 2√(kwσ²/6). The fourth-root scaling is Dixit's (1991, doi 10.1016/0165-1889(91)90037-2). The coefficient 6
  is re-derived here by a renewal argument in the undiscounted limit (exit time b²/σ²; accumulated loss b⁴/6σ² from the
  ODE (σ²/2)f″ = −x²). It is checked against a BVP solve and Monte Carlo (0.0813 ± 0.0006 against 0.0816). It was not
  re-checked against the paper's own text. A cost 100× smaller narrows the band only 3.2×.
- (b) *Lump-sum cost, one step change* of size Δ in 𝒟\* that lasts a regime of length T (or forever, discounted at
  rate r): move iff wΔ²T > k, so Δ_k = √(k/(wT)) (or √(kr/w)). This threshold scales as k^{1/2}, not k^{1/4}. **Which band
  applies depends on how the inputs move.** THEORY §3's kill rule is written for step changes.
- (c) *Smooth (convex) cost only* (k = 0, κ > 0): there is no band. After a step the gap decays as e^{−t/T_red} with
  T_red = √(κ/w), which is THEORY §3's redesign time (a closed form, from the Euler–Lagrange equation; checked
  numerically: 2.01 against 2.00).
- (d) *Aggregation:* units with lump-sum costs and dispersed gaps respond to a common step smoothly *on average*. No
  unit moves for a small step, but the class mean closes the gap (Caballero & Engel 1999, doi 10.1111/1468-0262.00053;
  checked in d1 D1d). Inaction band and switching hysteresis: Dixit (1989, doi 10.1086/261619).

**CT41 (PROVED (in-model): when a non-move is a miss).** Take a class whose closed term list includes a lump-sum
redesign cost with a preregistered upper bound k̄, measured independently of the design. Suppose a design minimizes J_R.
After a measured change in its inputs that moves argmin J by Δ, it is optimal **not to move** whenever |Δ| < Δ_R(k̄).
Here Δ_R is the class's band from CL19, √(k̄/(wT)) for a step lasting T and (6k̄σ_d²/w)^{1/4} for an optimum drifting at
variance rate σ_d². A design anywhere inside its band is consistent with the hypothesis. A non-move is therefore evidence
against it only when |Δ| exceeds max(Δ_band, Δ_R). Here Δ_band ≈ √(2εJ\*/H) is THEORY §3's static band. *Proof:* CL19
(a)–(b) give the optimal policy, and the static band is THEORY §3's. A lump-sum mover that does move goes to the target,
not to the band edge, which is a second testable signature. With purely proportional costs a move stops at the band edge
(singular control; stated, not checked here). ∎

**Kill-rule amendment (THEORY §3 and §8, FRAMEWORK §9 item 5).** "A design that fails to move with a measured change in
its inputs, by the preregistered share, counts as a miss" now reads "…counts as a miss, **unless the move argmin J calls
for is inside the class's preregistered redesign band** (CT41). A band exists only where adjustment is lumpy, and only
with a redesign cost or upper bound on the closed term list, measured independently of the design. Without that, the
band is zero and the rule is as before." **Anti-rescue.** A redesign cost added after a non-move is seen is the "needed
cost not on the preregistered list" that THEORY §3 already scores as a miss. Without the measured-k condition, the band
would excuse any non-move. Where units adjust in lumps, the rule and qualification item (e)'s T_red are judged on the
class average over units (CL19 (d)), as the class preregisters.

**CX9 (OPEN): layer-count hysteresis.** K is an integer, so adding or dropping a layer is lumpy by nature. With switching
cost k_K and a stake w that moves, the best policy adds a layer at w_up above the static crossing w_c and drops it at
w_down below it. In d1 D1c (value iteration, J\*(K, w) = Kh + wG₀/(K+1), K: 1 → 2, w_c = 1, k_K = 3, discount 2% per
period), w_up = 1.107 and w_down = 0.895. Without the cost, both equal w_c within the grid. THEORY B.9 (its Dynamics paragraph) already
says this qualitatively, crediting Dixit 1989. New here is only the field form: in a qualifying class with measured add
and drop costs, the stake at which a layer appears exceeds the stake at which it goes. No hysteresis under a measured
positive switching cost would count against the extension, not against J.

**Price on the redesign option (pointer to PR #115).** PR #115's CT40 says that redesigning per regime gains from
fluctuating volatility (E J\*(a) ≤ J\*(E a)). With CL19, that gain is net of switching. Redesign per regime pays only if
the Jensen gain per unit time exceeds the regime-switch rate times k. This is elementary, has no row, and is PR #115's
"Gap 3".

## 3. The lineage objective and bet-hedging

**Extension.** A lineage is a population of units sharing a heritable strategy π, a distribution over designs (a single
design is a point mass). Each generation, unit j's growth factor is f(𝒟_j, s, e_j). Here s is a shock shared by every
unit in the generation and e_j is idiosyncratic. For a large population, the lineage's long-run growth is

  G(π) = E_s ln E_{𝒟∼π, e}[ f(𝒟, s, e) ]   (geometric across generations, arithmetic within one).

Which objective a class's selection acts on, per-unit J (through the cost-to-fitness map, THEORY §3 (a)) or G, is a
preregistered modelling choice.

**CL20 (PRIOR ART).** Under shared environmental variation, selection on long-run growth favours spreading designs within
a genotype (bet-hedging). Sources: Cohen (1966, doi 10.1016/0022-5193(66)90188-3); within-generation variance, Gillespie
(1974, doi 10.1093/genetics/76.3.601); Philippi & Seger (1989, doi 10.1016/0169-5347(89)90138-9); the means, variances
and correlations trade-off, Starrfelt & Kokko (2012, doi 10.1111/j.1469-185X.2012.00225.x); information and phenotypic
switching, Kussell & Leibler (2005, doi 10.1126/science.1114383). E. coli persistence is a spontaneous phenotypic switch
(Balaban et al. 2004, doi 10.1126/science.1099390). A model with measured switching rates reads it as insurance tuned to
how often antibiotic stress occurs (Kussell, Kishony, Balaban & Leibler 2005, doi 10.1534/genetics.104.035352). That is a
model-based reading, not a selection experiment. A simulation study proposes that cell-to-cell diversity in E. coli
chemotaxis protein levels is a selectable trait (Frankel et al. 2014, doi 10.7554/eLife.03526). That is a proposal,
untested.

**CT42 (PROVED (in-model): when the lineage objective differs from per-unit J).**
- (i) Any per-unit objective that is an expectation over units is linear in π. That covers expected J, expected factor,
  and a per-unit ruin probability read as an average. Its optimum is a pure design, or a mixture of at most (number of
  constraints + 1) designs when constraints are averaged (LP; see §5).
- (ii) With no shared component (s constant) and a large population, G(π) = ln E[f]. G is maximized by the design with the
  highest per-unit expected factor, so the two objectives agree. d2 D2b checks this analytically and by simulation
  (5,000 units, 400 generations).
- (iii) With a shared component, G is concave in π and generally has an interior optimum. For two designs where the lean
  one (factor a₁ calm, 0 under the shock) is wiped out by a shared shock of probability β and the robust one has b₁ calm
  and b₀ > 0 under the shock, the robust share is q\* = min(1, βa₁/(a₁ − b₁)) (first-order condition; Kelly-type). With
  β = 0.05, a₁ = 1.30, b₁ = 1.05, b₀ = 0.90: q\* = 0.26 and G = 0.128 per generation. The best pure design (robust,
  forced by a per-unit ruin constraint) gives G = 0.041, and pure lean gives −∞. The per-unit expectation picks pure lean
  (1.235 against 1.043).
- (iv) If the shock is shared with probability ρ and independent otherwise (same marginal β), q\* rises from 0 with ρ:
  0, 0.016, 0.061, 0.144 and 0.26 at ρ = 0, 0.05, 0.2, 0.5 and 1 (d2 D2c, numerical).

*Proof:* (i) linearity. (ii) the law of large numbers within a generation. (iii) ln is concave, and the first-order
condition is β/q = (1 − β)(a₁ − b₁)/(a₁ − (a₁ − b₁)q). ∎ The bet-hedging theorem itself is Cohen's. New here is only its
placement against J: the lineage optimum differs from per-unit argmin J exactly through the shared component of variance.
A per-unit ruin constraint rules out designs a lineage profitably carries at a minority share.

**What this does to existing work.**
- *PR #115 CX7* ("the optimal form of diversity against common mode"): in the class of multiplicative lineage growth
  with shared shocks, the known answer is a mixture of different designs, not identical copies (consistent with #115's
  R1-c). This settles that part of CX7 for this class only. It says nothing about the robust layer count, which stays
  open.
- *E. coli (the best next candidate to qualify).* P1 and P10 compare one adaptation time with a per-cell argmin. If
  E. coli's chemotaxis shocks are shared within a generation and selection acts on lineage growth, the optimum is a
  distribution of designs, and its mean need not equal the per-cell argmin. A bet-hedging spread would then read as
  scatter or as a miss. **Any E. coli qualification or preregistration must name the objective before data are opened**:
  per-cell J, or lineage growth G with its shared-shock structure. It must also name the compared statistic: per-cell
  values, the population mean, or the distribution. This is recorded as a dated deviation in
  `theory/measured/ecoli/DEVIATIONS.md` (DV2). Locked files and verdicts are unchanged.
- *EVO1 (PR #114).* Genomes there are single designs with no phenotypic randomization, so EVO1 cannot express
  bet-hedging and does not test §3. Its exponential fitness is the log-reserve form in which J is the time average
  (§4 (i)).

**CX10 (OPEN): the lineage objective in the field.** In a qualifying class whose shocks are shared within a generation,
the distribution of designs, not one design, sits near argmax G. Candidates are the E. coli persister fraction against
the measured frequency of stress (Kussell et al. 2005's model with independently measured inputs) and chemotaxis protein
spread (Frankel et al. 2014, untested). Neither has been checked against a G computed from measured inputs.

## 4. Time average and ensemble average

**CL21 (PRIOR ART).** When wealth compounds, the quantity a single trajectory realizes is the time-average growth rate,
not the ensemble mean (Peters & Gell-Mann 2016, doi 10.1063/1.4940236; Peters 2019, doi 10.1038/s41567-019-0732-0; Kelly
1956, already credited in THEORY). Peters' coin (×1.5 or ×0.6) has an ensemble mean of +5% per step and a time average of
½ ln 0.9 = −5.3% per step (d3 D3d).

**CT43 (PROVED (in-model): where J is already the time average and where it is not).**
- (i) *Additive reserve* (THEORY §2): the reserve's time average equals its ensemble mean under A2 (ergodic theorem).
  *Log-reserve form* W′ = W·exp(−(c + wℓ)): time-average log growth = −(c̄ + wE ℓ) = −J almost surely. J needs no change
  in either case. d3 D3a checks this on a correlated AR(1) loss: −0.02998 against −0.03.
- (ii) *Arithmetic multiplicative form* W′ = W(1 + g − wℓ) with an unbounded loss (Gaussian squared error, THEORY's
  𝓜_LG): P(1 + g − wℓ ≤ 0) > 0 for every design, so E ln = −∞ for all of them. The form is defined only for bounded loss
  and gives no alternative ranking in the linear-Gaussian class.
- (iii) *Threshold ruin* (ruin = W falls below θW₀ within horizon T): a design with negative time-average growth has
  log W as a random walk with negative drift, so its ruin probability → 1 as T → ∞. Any ε < 1 excludes it over a long
  horizon, so **the ruin constraint fixes the sign**. **It does not fix the ranking**: d3 D3d has two designs that both
  pass (θ = 0.3, T = 300, ε = 0.01; P = 0 and 0.0013) yet are ranked oppositely by the ensemble mean (1.031 > 1.030) and by
  the time average (0.026 < 0.030).
- (iv) *Numerical, not proved.* In the copies toy (each of n copies down with probability p per window; all down costs a
  fraction X of the reserve; stakes act on returns), the copy count under time-average growth is never smaller than
  under J. On a 600-point grid (g, h, X, p) it is one larger in 90 cases (15%), never more than one larger, and only
  for lumpy X; for X = 0.05 the counts coincide. The scan's 3-against-4 example is real but sits near a tie under J (J(3)
  and J(4) differ by 0.6%).

*Proof:* (i) Birkhoff and THEORY A2. (ii) Gaussian tails. (iii) recurrence of a random walk with negative drift; D3d is
an explicit pair. ∎

**Per-class fix.** Preregister whether a class's stakes are additive (a reserve) or compounding (returns). For
compounding stakes with lumpy losses, use −E ln(1 + g − wℓ) in place of w·E ℓ, or state the loss on the log of the
reserve. For additive stakes, nothing changes.

**A confound for PR #115's ROBUST-SLACK (CX8).** RS-1 predicts reserves and copies above the plug-in ε-minimum.
Compounding stakes with lumpy losses predict extra copies with no uncertainty at all (CT43 (iv)), so RS-1 alone cannot
separate the two. RS-2 (the excess rises with the record's uncertainty) can. Proposed deviation for that prereg, to be
filed on PR #115's branch before any data (this branch cannot edit a file main does not have): *"D10 (20 Nov 2026):
before data, record for each system whether its stakes are additive or compounding. For compounding stakes with lumpy
losses, compute the plug-in minimum under time-average growth (DYNAMICS CT43) as well as under J. RS-1 counts only
excess above the larger of the two."*

## 5. The two OVERREACH verdicts, re-checked

- **Bode sensitivity ("conservation of fragility") stays OVERREACH for the present class.** The steady-state Kalman–Bucy
  filter's sensitivity S = 1 − H never exceeds 1. This is the filter dual of Kalman's return-difference inequality
  (Kalman 1964, doi 10.1115/1.3653115). Checked on 40 random worlds with 1–3 OU modes: max |S| = 1 − 9×10⁻¹¹. With no band
  where |S| > 1 there is no waterbed. ∫₀^∞ ln|S| dω = −(π/2)·CL is reproduced to 10⁻¹² in six worlds; that is the
  relative-degree-1 identity, which every such filter satisfies. A waterbed needs a loop that acts on the world, with
  unstable poles or delay (Freudenberg & Looze 1985, doi 10.1109/tac.1985.1104004; Seron et al. 1997, doi
  10.1007/978-1-4471-0965-5). That belongs to CX2.
- **Barbell stays OVERREACH.** In CT22's model (Lemma B9 setting; B_min = 0.486 reproduced), the cost against
  ruin-probability frontier equals its own lower convex hull at B = 0.49, 0.50 and 0.505, so mixing two designs at an
  averaged ε gains exactly nothing. With discrete copies a mix does gain (6.555 mean copies against 7 at ε = 5×10⁻⁴), but
  only if ε binds *before* the randomization. A system that drew 6 copies has ruin probability 10⁻³ > ε itself. That is
  LP / constrained-MDP randomization (Altman, CRC reprint 2021 of the 1999 book, doi 10.1201/9781315140223), not a
  safe-plus-speculative barbell.

## 6. Corrections to the wide-net scan (for the record)

1. *Finding 1:* hysteresis in K is not missing from THEORY. THEORY B.9 (Dynamics paragraph) and §10's credits already name it
   (Dixit 1989). What is missing is the term in J and the kill-rule consequence. The fourth-root band applies to a
   drifting optimum; for the step changes THEORY §3's rule is written for, the threshold is √(k/(wT)), which shrinks
   faster as k falls. The band also needs a measured k, or it becomes an escape hatch.
2. *Finding 2:* "answers CX7" is too broad. It answers the diversity question in one class only. Per-unit and lineage
   objectives agree when shocks are independent (CT42 (ii)). For E. coli the more direct case is chemotaxis diversity
   (the measured layer), not only persisters, and the adaptive reading of persistence is model-based.
3. *Finding 3:* the scan's check that "arithmetic multiplicative growth ranks LG designs the same way" clipped a log
   that is −∞ for Gaussian loss (CT43 (ii)). The conclusion "no flaw in the core" holds through the log-reserve form
   instead. The 3-against-4 example is a near tie; over a grid the effect is at most one copy, in 15% of cases.
4. *Barbell:* the condition is ex-ante against ex-post binding, not "frequency against probability", and the discrete
   mix is randomization, not a barbell.
5. *DOIs:* all 24 distinct DOIs the scan cites resolve on Crossref to the papers named. Altman's DOI is the 2021 CRC reprint.

## 7. Not claimed

None of this is a new theorem about nature, and CT41–CT43 are elementary placements of known results against J. Nothing
here is evidence for or against the hypothesis. No locked prediction or verdict changes. What changes is how future
tests are scored: (1) a correct non-move inside a measured redesign band is no longer a miss; (2) a class names its
objective (per-unit or lineage) and its stake type (additive or compounding) before data. All three extensions add
quantities to preregister, and each must be measured independently of the design, or it becomes a free parameter.
