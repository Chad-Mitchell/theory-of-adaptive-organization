# The master equation: derivations, checks and a worked example

Companion to `THEORY.md` v2.1 (§3–§5, Appendix B.9). `THEORY.md` governs where they disagree. Written 19 Nov 2026 (ET) from the review `reviews/master-equation_2026-11-19/REVIEW.md` (a separate executor from the author of the layer proofs, same bot family; **not independent of the theory's authorship as a whole, and not refereed**). The sections below are copied from that review with paths updated; the review's verdict words ("modest synthesis", "weak for firms and teams", "does not apply to any adaptive system") are superseded in THEORY v2.1 §4, §7, §9–§10: the parts are known and the claim is new; applicability is general and the bottleneck is measurement; worlds that respond to the design are inside the theory as an open theorem (CX2), not outside its scope.

Checks: `theory/meq_checks/` (run at nice 19; a few seconds each). **`meq_derive.py` asserts that each special case listed in THEORY §5 derives from the master equation** and is run by the test suite (`tools/test_meq_derive.py`). The layer proofs L1–L4 are in `theory/LAYERS.md` with checks in `theory/layers_checks/`.

## 1. Theorem or definition, and the theorem it carries (THEORY CT20–CT22)

**Steelman.** Least action is also "just" an objective, yet it is the most compressed statement of mechanics, because the equations of motion fall out of it. In the same way, J's value is that its solutions are checkable.

**Hostile view.** "Minimize some cost" fits any behavior: every admissible design is optimal for some cost (the complete-class and revealed-preference problem; GENERAL_THEOREM §0 item 7). Least action is exact for its domain and has no free cost function. J has as many free prices as it has terms. So J gets content only from (i) structure that holds for **every** admissible price, and (ii) predictions with independently measured prices.

**Both are right.** That is why the theorem below leads with world-free monotone structure.

### Master Theorem (proposed; parts (i)–(iv) proved here or in the repo, unreviewed as a whole)

**Setting 𝓜_LG.**
- **World.** The world is exogenous (g = 0). It is a zero-mean Gaussian process, either stationary with spectral density S(ω) or with stationary increments, observed through white noise of density N > 0, or read exactly at price c per read.
- **Design.** D = (K, an LTI estimator realizable with K first-order stores whose rates lie in a compact set [b_min, b_max], read rates f_k ∈ [0, F], and a sharing graph).
- **Costs.** h > 0, c_k ≥ 0, κ ≥ 0, w > 0, all in one currency. Loss is squared error at lead k ≥ 0.
- **Ruin.** Ruin follows the diffusion reserve of GENERAL_THEOREM §5, with the constraint imposed through the Lundberg bound, θ(D) ≥ ln(1/ε)/B. This is a sufficient condition, not an equivalent one.

**(i) Existence.** If any design is feasible, a minimizer exists, and K\* ≤ J(D₁)/h, where D₁ is any feasible one-layer design.
*Proof.* J ≥ hK, so only finitely many K matter. For each K, J is continuous on a compact parameter set (Weierstrass). Without the compact rate set, the infimum may only be approached, because poles can run off to 0 or ∞.

**(ii) Monotone comparative statics, for every world and every loss, with sensing fixed (restated v2.4).** Let E_K be the least expected loss over nested design classes, so E_K is nonincreasing in K, with the read rates held fixed.
- K\* is nondecreasing in w/h.
- For one layer whose error grows with the age of its reading, the read rate f\* is nondecreasing in w/c.
- *Proof.* −J = −hK − wE_K has increasing differences in (K, w/h), so Topkis (1978) and Milgrom & Shannon (1994) apply. Likewise −J(f) = −cf − wĒ(1/f), with Ē(1/f) decreasing in f.
- With sensing fixed and the ruin constraint slack or absent this holds **independently of the world's statistics**. With read rates chosen it can fail (reads substitute for layers; the referee's counterexample is in THEORY B.9): what survives, with ruin slack, is that total judgment spend never falls and error never rises with stakes (CT33; a binding ruin constraint breaks it, `scope_checks.py` §1b; THEORY B.10; `scope_checks.py` §1). Checked: K\* = 1, 1, 1, 2, 2, 2 at R = 1 … 1000 (`theory/meq_checks/meq_checks.out` S3).

**(iii) Layer cap set by the world.**
- K\* is at most the McMillan degree of the world's optimal predictor, counting one state per layer: J for a sum of J OU modes (PROOF_A L2(i)); a rhythm (complex pole) is a two-state mode, two layers by degree, and unbounded if only real first-order stores are allowed (`scope_checks.py` §4).
- K\* ∈ {0, 1} for a single pole, including the random walk (L1; K\* = 0, acting blind, can win when stakes are small).
- At k = 0 with J modes, K\* = J once R = wE_∞/h > R\* (L2(ii)–(iii)).
- No finite K is exact for an irrational spectrum (L3).

**(iv) Survival as a constraint.**
- With B_min = ln(1/ε)/max_D θ and B_slack = ln(1/ε)/θ(D_E), where D_E is the expected-cost optimum:
  - for B < B_min, no design is feasible;
  - for B ≥ B_slack, the constraint is slack and the expected-cost rules are exactly optimal;
  - in between, the constraint binds with multiplier μ > 0, and the design moves from D_E toward the survival-optimal design.
- Checked in the GENERAL_THEOREM §5 setting with ε = 10⁻³: B_min = 0.486 and B_slack = 0.508, and τ\* moves 0.267 → 0.299 → 0.310 → EOQ 0.316 as B goes 0.49 → 0.508 (`theory/meq_checks/meq_checks2.out`).

**(v) Reductions.** CT12, L1–L3, LAT-1, Result 4 and the Lagrangian of P3 are solutions of J under the restrictions listed in §1a. CT7 is a **bound** on J, not a solution of it.

**What cannot be proved:** that real systems sit near argmin J. That is an empirical hypothesis (THEORY §2.1, "Selection"; Alchian 1950).

### 1a. Special-case checks: does each result really come out of J?

| Claim | Restrictions on J | Result | Notes |
|---|---|---|---|
| CT12: J(T) = c/T + wqT^{α−1}/α, read rate ∝ (wq/c)^{1/α} | K = 1, κ = h = g = 0, exact reset reads, hold-last-value, W-b world | **PASS.** Mean error qT^{α−1}/α (sympy). The numerical T\* matches the formula to 6 digits at α = 1.3, 1.6, 2, 2.5, 2.9. Elasticities in w, q, c are +1/α, +1/α, −1/α. CT13 penalty matches. J\* at α = 2 is √(2cwq) = σ√(2cw) | Exact in-model |
| L1–L3: J_K = hK + wE_K | κ = g = 0, **reads not chosen**: sensing is a fixed noise density N | **PASS with a caveat.** Two OU modes: ε₁ = 1.16%, R\* = 86, K\* switches 1 → 2 between R = 30 and 100 | The Σc_k f_k term is frozen, not optimized. So J must allow sensing priced by **precision** (A_θ, Lemma B2), not only per read |
| "Layers at the world's time scales" | Same | **COUNT PASSES, TIMING DOES NOT.** For modes at 3 and 90 days, the optimal stores' time constants are 1/b_j = 0.16–2.6 days and 6.2–11.9 days, depending on sensing noise (`theory/meq_checks/meq_roots.out`) | One layer per world time scale, with each layer's memory set by scale **and** noise, and much faster than its mode (GAPS G10) |
| CT7 floor: J\* = σ√(2kT·w) | Read term re-expressed as **price per nat acquired**, λ·ι, with λ ≥ kT (Barato, Hartich & Seifert 2014) | **PARTIAL.** Minimizing λσ²/(2D) + wD gives σ√(2λw) (sympy) | Not c_k f_k, and not κI_mem (that prices nats *held*). It is a lower bound over physically allowed trackers, not a design optimum. "Same form as EOQ" is forced by dimensions up to the √2 (CT7's own text) |
| Theorem L: "expected-cost rules are the large-buffer limit" | Ruin enters as a constraint | **MISSTATED.** Theorem L (B9, GENERAL_THEOREM §5) maximizes the Lundberg exponent θ. Its argmax **does not depend on B** (L3). EOQ is its limit when the reserve's own noise dominates (checked: s₀ = 3 gives 0.314 vs EOQ 0.316), not when the buffer is large | Under the chance-constrained J, "large buffer ⇒ expected-cost rules" is **true**, but it is the new Lemma (iv) above, not Theorem L |
| LAT-1 | E[ℓ] evaluated at latency ℓ | **PASS.** Error ≥ qℓ^{α−1}, which is a floor on the E term | Federation needs a coupling-cost term J does not yet have (§e) |
| Result 4, pooling | Needs the link cost κ_b, telling price d and lookup u | **Not in Ace's J as written.** It is in Axiom 5 | Add these terms |
| "The world enters only as q and α" | | **FALSE as stated.** L2/L3 need the full spectrum (rates, weights, lines), the noise N and the lead k. Jump worlds bring in rate and size separately (N16). Theorem G needs Φ of a general Markov law | (q, α) is the scale-free special case. The input is the world's measured law |
| The g term (making the world drift less) | | **Breaks exogeneity.** With g > 0, q depends on the design, which violates A1 and Still et al.'s no-feedback condition. Every proved result has g = 0 (CL11 open) | Keep g in the problem statement, flagged open, and say every theorem sets g = 0 |
| κI_mem + hK | | Both count as "holding". Only P3 uses κ (alone). No layer theorem uses κ and h jointly | Say which holding term each result uses |

## 2. Worked engineering example (hypothetical numbers)

**System.** A team keeps a demand forecast (units/day) that feeds replenishment. *All numbers below are hypothetical and chosen for illustration.*
1. **Measure the world.** Fit the structure function and spectrum of the demand logs with the repo's gated estimator. Suppose it finds two modes: a 3-day fluctuation (sd 40) and a 90-day trend (sd 120), seen through daily sampling noise (density 3600 units²·day).
2. **Solve for the layers.** From `theory/meq_checks/meq_checks2.out`, E_∞ = 1762.7, E_1 = 1796.3 (flat penalty 1.9%) and E_2 = E_∞. So a second forecasting layer pays iff w(E_1 − E_2) > h, i.e. w > h/33.6.
   - At an upkeep of h = $40/day, that needs a stake w > $1.19 per unit² per day of error.
   - The optimal stores have time constants of about 1.5 and 6.9 days. They are **not** 3 and 90 days.
3. **Solve for read cadence.** For a hold-last-value dashboard of a metric with α = 1.5, q = 50, c = $25 per pull and w = 0.02, CT12 gives T\* = 17.8 days (7.1 days at α = 2). Doubling the stakes shortens T\* by a factor of 0.63, versus 0.71 at α = 2.
4. **Robustness.** Misjudging c/(wq) by 2× costs about 6% at α = 2 (CT13). An engineer can therefore act on rough prices.

**Inputs ranked by how hard they are to measure.**
- **Easy:** q, α and the spectrum, which are measurable with care.
- **Usually priced:** c, from API prices, meeting hours or sample costs.
- **Accounting-level:** h, which is fuzzy for people.
- **Hard:** w, which needs exogenous variation in error cost (G3).
- **Hardest:** κ, the price per nat held, which is almost never measured outside cells.

**Verdict.** It is buildable today for machine systems: monitors, caches, sensor networks and inventory. For organizations, use it for **signs and thresholds** (§b) until w and h are measured.

## 3. Revealed costs and the price of survival (THEORY §7, CT22)

**(c) The inverse problem: revealed costs. PARTLY HOLDS. Circular when exactly identified, real when over-identified.**
- Only price **ratios** are identified (w/c, h/w), by homogeneity (S1).
- With a free c_k per layer, any observed K layers and K rates can be fitted. That is circular.
- It becomes a test when there are more observed design features than free ratios. Three ways to get there:
  - one system observed at several exogenous q (the implied w/c must be constant, and the rates must move as q^{1/α});
  - several items under one clock (Result 5: equality iff c_i/(w_iσ_i²) is equal);
  - the same read technology across layers.
- This is Afriat/Varian revealed preference and Kalman's 1964 inverse-optimality question applied to design. It is a real way around the w bottleneck.
- **Over-identification count (v2.2).** One system observed at m exogenous drift levels gives m − 1 equalities of the implied w/c. n items under one clock give n − 1 equalities of c_i/(w_iσ_i²). A K-way allocation under one binding budget gives K − 1 equalities of marginal value per currency unit (the shadow price of THEORY CT24). A test needs at least one such equality beyond the free ratios.

**(d) The ruin multiplier as a price of survival. HOLDS (diffusion approximation, Lundberg sufficient bound).**
- μ = −m′/θ′ at the binding constraint. It is the marginal expected cost of extra survival exponent.
  - It is 0 for B ≥ B_slack, where the expected-cost rules hold exactly.
  - It rises toward the feasibility edge B_min, below which no design survives. This is the constructive face of Theorem P's "not viable".
  - At B = 0.5 it is μ = 0.0052 per unit θ, and the buffer is worth dJ\*/dB = −0.145.
- **It unifies Theorem L.** EOQ is the μ = 0 end and Theorem L's survival-optimal interval is the μ → ∞ end. The constrained optimum moves between them (0.236 ↔ 0.316 in the check). This is the same direction as risk-sensitive control (Jacobson 1973).
- μ carries the system's own units, so it is not comparable across systems.

## 4. Dimensionless groups, phase diagram, dynamics, robustness (THEORY CT23, N54, N55)

### (h) Dimensionless numbers. PARTLY HOLDS: equal numbers give the same design only when the world's shape is also equal

**Quantities that look dimensionless but are not.** E[ℓ] has units x², so w has units of cost per (x²·time). Then:
- w·σ²/h has units 1/time;
- w·q/c has units time^{−α};
- buffer/σ mixes cost with x/√time.

The correct groups come from scaling time by the natural read interval T₀ = (c/(wq))^{1/α} and cost by the one-tracker cost J₁ = c^{(α−1)/α}(wq)^{1/α}.

**The fewest groups, for a scale-free world with one tracker or several:**

| Group | Meaning | Decides |
|---|---|---|
| α (or the spectrum's **shape**) | how the world changes | everything; it is a function, not a number, for a general world |
| Π_h = h/J₁ (J₁ from the read-priced CT12; R = wE_∞/h comes from the noise-priced L2: the two are different normalizations, not equal) | upkeep relative to what tracking costs | how many layers (L2) |
| Π_ℓ = ℓ/T₀ | latency relative to the natural read interval | reach and federation (LAT-1) |
| Π_u = μu/J₁ | lookup relative to holding | hold or look up (T5b cliff) |
| Π_y = y/J₁ | income relative to the cheapest tracking | viability (Theorem P0) |
| Π_B = θB = 2mB/s² (with ε) | buffer in ruin lengths | whether survival binds (Lemma iv) |
| N, ρ | members, shared share | shared layers (Result 4) |

The noise share Nτ/Var counts as part of the world's shape when sensing is noise-priced.

**Check** (`theory/meq_checks/part2.out`). Rescaling time by s ∈ {1, 7, 0.01} and amplitude by A ∈ {1, 13, 10³}, with the groups held fixed, gives identical designs: ε₁ = 2.2302%, K\* = 2, and layer memories 0.215 and 5.600 in units of s. This is Buckingham π, i.e. Theorem S (S1–S2).

**Counter-check.** With the same R and the same mode ratio but a different noise share (N = 0.005, 0.05, 0.5), R\* is 135, 45 and 21. So the shape carries extra groups.

**Verdict.**
- For a **parametric** world (a power law, or a few modes) the design is fixed by about 5–7 numbers, and systems with equal numbers get the same design up to units. That is the precise meaning of "the same design at every scale".
- For a general world the shape is a whole function, so "few numbers" holds only after the world has been summarized.

### (i) Phase diagram. HOLDS in a model world; cells, firms and cities can be placed only illustratively

`theory/meq_checks/phase.png` (illustrative) is computed exactly in one model world (`theory/meq_checks/phase.py`).
- **World:** two OU modes at τ = 1 and 100, equal variance, sensing noise 0.05.
- **Costs:** upkeep h per layer, federation overhead 20h, income 200h.
- **Axes:** x = R = w·Var/h; y = latency ℓ/τ_fast.
- **Designs compared:**
  - no model (loss w·Var);
  - one or two central layers, with readings late by ℓ;
  - federate (local trackers with zero latency, paying the overhead);
  - not viable (the cheapest design costs more than the fixed income y = 200h: an artifact of holding income fixed while stakes rise; if income scales with stakes the region moves or vanishes).

**Boundaries found** (`theory/meq_checks/phase.out`):

| Latency | Region boundaries along R |
|---|---|
| ℓ = 0.01 | no model to R ≈ 1.25, one layer to 142, two layers to about 1045, then "not viable" at the fixed income y = 200h |
| ℓ = 0.14 | one layer from 1.39, two layers from 72, federate from 247 |
| ℓ = 2.2 | one layer from 2.5, federate from 50 |
| ℓ = 30 | one layer from 4.5, federate from 35 |

The two-layer region is closed at large latency: the fast mode can't be predicted that far ahead, so only the slow layer is worth keeping. Latency also shifts the no-model boundary right, because a late model is worth less.

**What is and is not general.**
- The region **order** along R (none → one → many) follows from Master Theorem (ii) **with sensing fixed**; "not viable" is an artifact of the fixed income, and this two-scale world caps the layers at two by construction. A many-scale map is being rebuilt; the earlier draft, `figures/face.png`, is withdrawn from README and THEORY (many-scale world, read effort optimized, federation charged n× upkeep and sensing and the lost pooling, the ruin constraint imposed with assumed income and reserve; regions computed from J, placements hypotheses). In this two-scale diagram federation is a free fixed overhead with no lost pooling, so its region is too large: superseded.
- Region **positions** depend on the shape, h_f/h and y/h. The figure is a 2-D slice of a 5–7-dimensional space.

**Placing real systems.**
- **Atoms (w = 0) honestly:** R = 0 is the far-left edge by E1 (no decision, no model). This placement is definitional.
- **Cells, firms and cities only illustratively.** No system in the repo has a valid measured R (stakes have never been measured, G3), latency ratio or shape. Putting them on the plot now would be invented placement.
- **The first honest placement** would be a system where the same-system test of G2 measures all three. A cell's chemotaxis pathway, where sensing costs are physically measured (Lan et al. 2012), is the best candidate.

### (j) Dynamics: selection or learning as descent on J. PARTLY HOLDS; two testable predictions, both elementary

**Status of the setting.** Gradient descent on design traits is a standard limit of selection (adaptive dynamics: Dieckmann & Law 1996, 10.1007/bf02409751) and of learning. Discrete choices such as K follow replicator- or threshold-type dynamics instead.

**What follows:**
1. **The design layer is the slowest layer.**
   - To redesign, a system must estimate the world's statistics, and estimating the slowest rate a to relative precision δ needs a record of about 2/(aδ²) of that time scale.
   - Monte Carlo (`theory/meq_checks/part2.out`): records of 10, 30 and 100 slowest time constants give relative errors of 0.55, 0.30 and 0.15, against the asymptotic √(2/(aT)) of 0.45, 0.26 and 0.14.
   - So the record a redesign learns from must be **tens of the slowest tracked time scale** long (the record length, not the update cadence: a system can redesign daily on a sliding window). Redesign is itself a layer, inside J, which is the recursion of (e).
   - Two-timescale learning is known in substance (Borkar 1997, 10.1016/s0167-6911(97)90015-3). The GTAO-specific prediction is the ratio: redesign record length ≳ 10–100× the slowest tracked scale.
2. **Designs scatter more in rough worlds.**
   - The relative curvature of J in ln T at the optimum is exactly **α − 1** (from CT13).
   - Under any noisy selection or learning that balances against this restoring force, the spread of ln(read interval) across a population scales as 1/√(α − 1). Rough worlds (α near 1) should show widely scattered cadences; smooth worlds should show tight ones.
   - This is testable across populations at known α. Its premise (spread set by curvature) is standard for stabilizing selection and was not derived here for a specific selection model. I found no prior statement, but the search was not targeted.
3. **Rates move before structure, with hysteresis.** Continuous parameters re-tune smoothly after a shift in q, with elasticity 1/α. K changes only at thresholds, and with a switching cost it shows hysteresis (entry and exit under uncertainty: Dixit 1989, 10.1086/261619). This is known in substance.

**Verdict.** Treating dynamics as descent adds two testable predictions: the redesign/slowest-scale ratio and the 1/√(α−1) scatter. Both are elementary. "Redesign is the slowest layer" holds as a necessity (you cannot redesign faster than you can learn the world's statistics). It is not a theorem that real systems do it.

### (k) Robustness: regret and flatness. HOLDS as the formal form of "re-measure, not a dead theory", with three named exceptions

**Theorem (local regret; elementary).** Suppose J is C² in log design variables with a nondegenerate minimum, and the design is computed from a picture of the world that is off by δ in log parameters. Then:
- the design error is O(δ) (implicit function theorem);
- the regret is ½δᵀHδ + o(δ²) (envelope theorem): **second order in the picture error.**

For one layer, mis-scaling drift by a factor m costs exactly [(α−1)m^{−1/α} + m^{(α−1)/α}]/α − 1 ≈ (α−1)(ln m)²/(2α²).

**Checks** (`theory/meq_checks/part2.out`):
- **Drift misjudged by 2×:** costs 3.8% at α = 1.3, 6.1% at α = 2 and 6.0% at α = 2.7. By 10×, it costs 35–85%.
- **Wrong slow time scale:** a two-layer design built for a slow mode at τ = 10 or 100 (true τ = 30) loses only **0.49% and 0.45%** of the error.
- **α misjudged by ±0.3:**
  - 0.05–7.7% when the structure function is matched near the read interval;
  - **up to 29%** when it is matched 10× away (α = 1.5 → 1.2 at τ_ref = 0.1T\*).
- **One mode believed instead of two:** costs the flat penalty, 2.2% here and at most about 20% in the earlier scans.

**Exceptions:**
1. **A wrong layered design can be worse than no layering.** Believing variance shares of 0.2/0.8 instead of 0.5/0.5 costs 7.0%, more than the 2.2% of a correct one-layer design.
2. **Fitting α far from the scales that matter** (the 29% case). Measure the statistics at the scales of the decision.
3. **Phase boundaries with cliffs.** Near the viability edge B_min (Lemma iv) or the lookup cliff (T5b), a small picture error can flip feasibility. Regret is not flat there, so a system near an edge can die of a picture error even though the theory does not.

**Verdict.** The "two kinds of wrong" (t1970) now has a formal form:
- **Picture errors cost second-order regret.** The fix is to re-measure. Exceptions 1–3 mark where that fails for the *system*.
- **Cost errors are a different object.** A missing cost term (J16) is not a perturbation of the inputs. No regret bound covers it, and it is what kills the theory.


## 5. Cost shares, the floor multiplier and the temperature (THEORY CT24, CT25; added v2.2)

Derivations are in THEORY B.9 (CT24) and B.6 (CT25); checks in `theory/meq_checks/scale_free_checks.py` (run by `tools/test_scale_free_checks.py`, output in `scale_free_checks.out`). Origin: `reviews/audit_2026-11-19/AUDIT.md` §2 and §5.

- **Scale-free accounting.** In CT12's single tracker J is degree-1 homogeneous in prices, so the optimum depends only on α and the cost shares equal price elasticities: sensing (α−1)/α, error 1/α, so reads : error = α − 1 in any currency (N57, open). Checked to 10⁻⁷ over 18 decades of currency.
- **Floor with an inefficiency multiplier.** Pricing a nat at β·kT multiplies J\* by β^{(α−1)/α} and leaves the shares unchanged; J\* is nondecreasing in every price, so any actual price at or above kT is above the CT7 floor. β is one measured number per system, which the theory does not predict.
- **Shadow prices.** For a system with a binding read budget B, the stake w is the reciprocal of the budget's multiplier; equal marginal values across trackers under one budget are testable equalities. That real internal prices equal multipliers is a conjecture (CX5).
- **Not claimed.** One conserved energy across scales; firms or cities paying in joules; physics fixing prices above the cell; equal numbers across systems of different world shape.
- **Temperature.** In the diffusive-reset class ruin ≤ ε is B ≥ z_ε·σ√τ (z_ε = 3.29 at ε = 10⁻³); the survivable shock is ∝ τ^{−1/2}. Monte Carlo of the closed form agrees within 5%.

## 6. Rules, closure and the compete / collaborate / organize toy (THEORY CT18-H, CT26–CT29; added v2.3)

Derivations are in THEORY B.6 (CT18-H), B.9 (CT24, general form) and B.10 (CT26–CT29); checks in `theory/meq_checks/rules_scaling_checks.py` (run by `tools/test_rules_scaling_checks.py`, output in `rules_scaling_checks.out`).

- **Temperature, general form.** For error self-similar with exponent H (fBm; stable Lévy with H = 1/α_s) the group is z = B/(σ·τ^H); the √ is H = ½.
- **Rule 4 (CT26).** Keep the superseded version until proof iff its upkeep rate k < p·ν·(L_f − L_r); the optimum is bang-bang.
- **Rules 6 and 1 (CT27).** Outcome records are information about the model's own error; regret falls in the number of records, and the number worth buying falls in their price. The Hebbian form is a hypothesis.
- **Homogeneity (CT28).** J\*(nW) = n^{1/α}J\*(W); level-by-level solving equals the joint optimum if levels interact through passed-up stakes, else regret O(κ²).
- **Free-riding toy (CT29).** Price of anarchy ½(√(a/W) + √(W/a)); free-riders capture (√N+1)/(2√N) of the pooling gain; stake-proportional cost shares restore the joint optimum; adaptation settles iff step < 2/N. CX2 (general convergence) stays open.

## 7. The ant trail, the CX2 classification, judgment spend and exact nesting (THEORY CT30–CT34; added v2.4)

Derivations are in THEORY B.10; checks in `theory/meq_checks/ants_cx2_checks.py` (run by `tools/test_ants_cx2_checks.py`, output in `ants_cx2_checks.out`).

- **Trail update (CT30).** The steady-state optimal tracker of a random walk seen through noise is x ← (1−λ)x + λ·signal, which is reinforce-on-use plus evaporation at λ\* = (−ρ+√(ρ²+4ρ))/2, ρ = q/r (√(q/r) in continuous time). Independent trails updated locally equal the central filter. That real systems implement it by selection is a hypothesis.
- **CX2 classes (CT31, CT32).** Shared-driver coupling is a weighted potential game: Nash = argmin of the potential, PoA ≤ (N+1)/(2√N), stake-proportional cost shares give Nash = joint optimum. Opposed coupling cycles, so no general convergence theorem is true; time-scale separation moves gradient play to a point that is not a Nash equilibrium when the slow cost is concave, and with convex own costs never changes stability (CT32 (iii); `scope_checks.py` §9): whether it restores equilibrium inside J's class is open.
- **Judgment spend (CT33).** With J = S + wE, adding the optimality inequalities at two stakes shows error never rises and spend S never falls as stakes rise, for any design set with reads chosen and the ruin constraint slack or absent (a binding ruin constraint makes the feasible set depend on the stake, and spend can fall); the layer count can fall. Check: `scope_checks.py` §1.
- **Exact nesting (CT34).** A team's optimized cost enters its parent's problem exactly as upkeep if (generically only if) the parent sees the team only through quantities fixed before the team optimizes; weak coupling ε costs at most (εL)²/(2μ). Check: `scope_checks.py` §2.
