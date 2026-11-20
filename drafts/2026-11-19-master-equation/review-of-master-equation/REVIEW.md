# REVIEW: the "master equation" of A Theory of Adaptive Organization

Independent, read-only review. Written Thu 19 Nov 2026, about 10:30 PM ET, by a Grok Bot executor for Chad (via Ace), in answer to t1973u and the widened scope in t1974u. **Nothing in the GTAO repo was edited, committed or pushed, and /workspace/looper was not touched.** Repo: a fresh clone of origin/main at `5b65c1e` in `/workspace/gtao-meq/repo`. Also read: `/workspace/gtao-spine/` (VERDICT, PROOF_A, GAPS, IMPLICATIONS) and `/workspace/gtao-v21/NOTES_SO_FAR.md`. Checks are in `/workspace/gtao-meq/checks/` (`meq_checks.py`, `meq_checks2.py`, `meq_roots.py` with `.out` files), all run at nice 19. Citations were checked against Crossref this session (`checks/crossref.out`). DOIs that failed or resolved to the wrong paper were dropped.

**The object under review** (Ace, t1972s9011):

  min over D of J(D) = κ·I_mem + h·K  +  w·E[ℓ]  +  Σ_k c_k f_k + g,  subject to P(ruin) ≤ ε.

## Bottom line

1. **Theorem or definition?** It is a **definition**: an objective that poses a design problem, not something that can be true or false. A constrained minimization cannot be proved. What can be proved is a set of statements about it: that a minimizer exists, structural properties that hold for every world, and that each repo result is its solution under stated restrictions. Section 1 gives one precise theorem that carries all three.
2. **Is it new?** **Modest synthesis, not a new result.** Every term and the Lagrangian form are textbook: an information or sensing cost plus expected loss (Sims; Tishby & Polani; Ortega & Braun; Meier, Peschon & Dressler 1967), a chance constraint (Roy 1952; Charnes & Cooper 1959), and hierarchy arising from information costs (Genewein et al. 2015). The repo already wrote it in one line: `reviews/night1/formal/AXIOMS.md` l.64, Axiom 5. What is distinctive is the package: a layer count priced inside the objective, the world's measured law as the only world input, one booking rule with a kill condition (J16), and a set of cross-scale predictions. I found no prior statement of exactly that package, but the search was not exhaustive.
3. **Is it useful?** **Yes, as a design calculator** where the read price, upkeep and stakes can be priced: monitoring, caching, sensor fleets, inventory and forecasting. It is **weak for firms and teams** until stakes w and upkeep h are measured (gap G3). Its most robust outputs do not need those costs at all: signs, exponents and thresholds.
4. **Does it apply to literally any adaptive system?** **No.** It covers systems that track a world they do not steer, with costs that add up in one currency per system and a world law that can be measured. "Every scale" means **the same problem with system-specific inputs and prices**. It does not mean one exchange rate, and it does not mean a proof outside the linear-Gaussian class.

**Is this equation the theory?** Mostly yes. It is the theory's **problem statement**. The theory is (problem) + (its solutions in stated classes) + (the bet that strongly selected systems sit near those solutions). Section 8 gives the statement I recommend for the top of the core.

---

## 1. Theorem or definition, and the precise theorem it can carry

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

**(ii) Monotone comparative statics, for every world and every loss.** Let E_K be the least expected loss over nested design classes, so E_K is nonincreasing in K.
- K\* is nondecreasing in w/h.
- For one layer whose error grows with the age of its reading, the read rate f\* is nondecreasing in w/c.
- *Proof.* −J = −hK − wE_K has increasing differences in (K, w/h), so Topkis (1978) and Milgrom & Shannon (1994) apply. Likewise −J(f) = −cf − wĒ(1/f), with Ē(1/f) decreasing in f.
- This is the one part that holds **independently of the world's law**. Checked: K\* = 1, 1, 1, 2, 2, 2 at R = 1 … 1000 (`meq_checks.out` S3).

**(iii) Layer cap set by the world.**
- K\* is at most the McMillan degree of the world's optimal predictor: J for a sum of J OU modes (PROOF_A L2(i)).
- K\* = 1 for a single pole, including the random walk (L1).
- At k = 0 with J modes, K\* = J once R = wE_∞/h > R\* (L2(ii)–(iii)).
- No finite K is exact for an irrational spectrum (L3).

**(iv) Survival as a constraint.**
- With B_min = ln(1/ε)/max_D θ and B_slack = ln(1/ε)/θ(D_E), where D_E is the expected-cost optimum:
  - for B < B_min, no design is feasible;
  - for B ≥ B_slack, the constraint is slack and the expected-cost rules are exactly optimal;
  - in between, the constraint binds with multiplier μ > 0, and the design moves from D_E toward the survival-optimal design.
- Checked in the GENERAL_THEOREM §5 setting with ε = 10⁻³: B_min = 0.486 and B_slack = 0.508, and τ\* moves 0.267 → 0.299 → 0.310 → EOQ 0.316 as B goes 0.49 → 0.508 (`meq_checks2.out`).

**(v) Reductions.** CT12, L1–L3, LAT-1, Result 4 and the Lagrangian of P3 are solutions of J under the restrictions listed in §1a. CT7 is a **bound** on J, not a solution of it.

**What cannot be proved:** that real systems sit near argmin J. That is an empirical hypothesis (THEORY §2.1, "Selection"; Alchian 1950).

### 1a. Special-case checks: does each result really come out of J?

| Claim | Restrictions on J | Result | Notes |
|---|---|---|---|
| CT12: J(T) = c/T + wqT^{α−1}/α, read rate ∝ (wq/c)^{1/α} | K = 1, κ = h = g = 0, exact reset reads, hold-last-value, W-b world | **PASS.** Mean error qT^{α−1}/α (sympy). The numerical T\* matches the formula to 6 digits at α = 1.3, 1.6, 2, 2.5, 2.9. Elasticities in w, q, c are +1/α, +1/α, −1/α. CT13 penalty matches. J\* at α = 2 is √(2cwq) = σ√(2cw) | Exact in-model |
| L1–L3: J_K = hK + wE_K | κ = g = 0, **reads not chosen**: sensing is a fixed noise density N | **PASS with a caveat.** Two OU modes: ε₁ = 1.16%, R\* = 86, K\* switches 1 → 2 between R = 30 and 100 | The Σc_k f_k term is frozen, not optimized. So J must allow sensing priced by **precision** (A_θ, Lemma B2), not only per read |
| "Layers at the world's time scales" | Same | **COUNT PASSES, TIMING DOES NOT.** For modes at 3 and 90 days, the optimal stores' time constants are 1/b_j = 0.16–2.6 days and 6.2–11.9 days, depending on sensing noise (`meq_roots.out`) | One layer per world time scale, with each layer's memory set by scale **and** noise, and much faster than its mode (GAPS G10) |
| CT7 floor: J\* = σ√(2kT·w) | Read term re-expressed as **price per nat acquired**, λ·ι, with λ ≥ kT (Barato, Hartich & Seifert 2014) | **PARTIAL.** Minimizing λσ²/(2D) + wD gives σ√(2λw) (sympy) | Not c_k f_k, and not κI_mem (that prices nats *held*). It is a lower bound over physically allowed trackers, not a design optimum. "Same form as EOQ" is forced by dimensions up to the √2 (CT7's own text) |
| Theorem L: "expected-cost rules are the large-buffer limit" | Ruin enters as a constraint | **MISSTATED.** Theorem L (B9, GENERAL_THEOREM §5) maximizes the Lundberg exponent θ. Its argmax **does not depend on B** (L3). EOQ is its limit when the reserve's own noise dominates (checked: s₀ = 3 gives 0.314 vs EOQ 0.316), not when the buffer is large | Under the chance-constrained J, "large buffer ⇒ expected-cost rules" is **true**, but it is the new Lemma (iv) above, not Theorem L |
| LAT-1 | E[ℓ] evaluated at latency ℓ | **PASS.** Error ≥ qℓ^{α−1}, which is a floor on the E term | Federation needs a coupling-cost term J does not yet have (§e) |
| Result 4, pooling | Needs the link cost κ_b, telling price d and lookup u | **Not in Ace's J as written.** It is in Axiom 5 | Add these terms |
| "The world enters only as q and α" | | **FALSE as stated.** L2/L3 need the full spectrum (rates, weights, lines), the noise N and the lead k. Jump worlds bring in rate and size separately (N16). Theorem G needs Φ of a general Markov law | (q, α) is the scale-free special case. The input is the world's measured law |
| The g term (making the world drift less) | | **Breaks exogeneity.** With g > 0, q depends on the design, which violates A1 and Still et al.'s no-feedback condition. Every proved result has g = 0 (CL11 open) | Keep g in the problem statement, flagged open, and say every theorem sets g = 0 |
| κI_mem + hK | | Both count as "holding". Only P3 uses κ (alone). No layer theorem uses κ and h jointly | Say which holding term each result uses |

## 2. Is it new? (prior art, every citation checked against Crossref this session)

| Piece | Known as | Citation (verified) |
|---|---|---|
| Information or sensing spend + expected loss | Rational inattention; information-theoretic decisions; free-energy decision-making | Sims 2003, J Monetary Econ, 10.1016/S0304-3932(03)00029-1; Maćkowiak, Matějka & Wiederholt 2023, JEL, 10.1257/jel.20211524; Tishby & Polani 2011, 10.1007/978-1-4419-1452-1_19; Ortega & Braun 2013, Proc R Soc A, 10.1098/rspa.2012.0683 (abstract read); information bottleneck, Tishby, Pereira & Bialek, arXiv physics/0004057 (page opened) |
| Sensing cost inside LQG/Kalman | Control of measurement subsystems | Meier, Peschon & Dressler 1967, IEEE TAC 12:528, 10.1109/tac.1967.1098668; Kalman 1960, 10.1115/1.3662552 |
| How often to look | EOQ, cash inventory, inattention, crawlers, age of information, value of information | Harris (1990 reprint), 10.1287/opre.38.6.947; Baumol 1952, 10.2307/1882104; Tobin 1956, 10.2307/1925776; Reis 2006, 10.1016/j.jmoneco.2006.03.001; Cho & Garcia-Molina 2003, 10.1145/958942.958945; Kaul, Yates & Gruteser 2012, 10.1109/INFCOM.2012.6195689; Howard 1966, 10.1109/TSSC.1966.300074 |
| Echelons and geometric clocks | Multi-echelon inventory; power-of-two lot sizing | Clark & Scarf 1960, 10.1287/mnsc.6.4.475; Roundy 1985, 10.1287/mnsc.31.11.1416 |
| Hierarchy and multiple time scales | Near-decomposability; multiscale estimation; brain time-scale hierarchy; **hierarchies from information cost** | Simon & Ando 1961, 10.2307/1909285; Simon 1962, JSTOR 985254 (URL resolves); Chou, Willsky & Benveniste 1994, 10.1109/9.280746; Willsky 2002, 10.1109/JPROC.2002.800717; Kiebel, Daunizeau & Friston 2008, 10.1371/journal.pcbi.1000209; **Genewein, Leibfried, Grau-Moya & Braun 2015, Front Robot AI, 10.3389/frobt.2015.00027** (abstract read: "the formation of abstractions and decision-making hierarchies depends on information-processing costs") |
| Organization design as information processing | | Galbraith 1974, 10.1287/inte.4.3.28; Radner 1993, 10.2307/2951495; Marschak & Radner 1972, *Economic Theory of Teams* (book, no DOI) |
| Predictive information; thermodynamics of prediction; Landauer | | Bialek, Nemenman & Tishby 2001, 10.1162/089976601753195969; Still et al. 2012, 10.1103/PhysRevLett.109.120604; Still 2020, 10.1103/PhysRevLett.124.050601; Landauer 1961, 10.1147/rd.53.0183; Barato, Hartich & Seifert 2014, 10.1088/1367-2630/16/10/103024; Lan et al. 2012, 10.1038/nphys2276; Mehta & Schwab 2012, 10.1073/pnas.1207814109; Tkačik & Bialek 2016, 10.1146/annurev-conmatphys-031214-014803 |
| Free-energy principle | | Friston 2010, 10.1038/nrn2787 |
| Ruin, Kelly, risk sensitivity, chance constraints | | Kelly 1956, 10.1002/j.1538-7305.1956.tb03809.x; Roy 1952, 10.2307/1907413; Charnes & Cooper 1959, 10.1287/mnsc.6.1.73; Jacobson 1973, 10.1109/TAC.1973.1100265; Cramér–Lundberg via Asmussen & Albrecher 2010 (credited in the repo, not re-checked) |
| Monotone comparative statics; inverse optimality; revealed preference | | Topkis 1978, 10.1287/opre.26.2.305; Milgrom & Shannon 1994, 10.2307/2951479; Kalman 1964, 10.1115/1.3653115; Afriat 1967, 10.2307/2525382; Varian 1982, 10.2307/1912771; Ng & Russell 2000, ICML (no DOI) |
| Causal states | | Crutchfield & Young 1989, 10.1103/PhysRevLett.63.105 |

**Verdict.**
- **The equation is a modest synthesis.** The closest neighbours are Ortega & Braun 2013 (the same Lagrangian, framed thermodynamically), Genewein et al. 2015 (hierarchy from information cost, static, with no drifting world), Meier et al. 1967 (sensing cost in LQG), and Kiebel et al. 2008 (time-scale hierarchy, with no priced layer count).
- **What I did not find stated together** is the full package: a priced layer count, a world-law-as-input with its spectrum's degree capping the layers, a ruin chance constraint whose slackness recovers the EOQ-type rules, and one booking rule across substrates with a kill rule. That is a genuine but **elementary** contribution.
- **The L2 math is classical** (Kalman degree, spectral factorization). The new part is posing it as a priced layer choice with the iff threshold R\*.
- Do not call the equation itself a discovery. Call it the theory's problem statement, and credit the neighbours above.

## 3. Is it useful? A worked engineering example

**System.** A team keeps a demand forecast (units/day) that feeds replenishment. *All numbers below are hypothetical and chosen for illustration.*
1. **Measure the world.** Fit the structure function and spectrum of the demand logs with the repo's gated estimator. Suppose it finds two modes: a 3-day fluctuation (sd 40) and a 90-day trend (sd 120), seen through daily sampling noise (density 3600 units²·day).
2. **Solve for the layers.** From `meq_checks2.out`, E_∞ = 1762.7, E_1 = 1796.3 (flat penalty 1.9%) and E_2 = E_∞. So a second forecasting layer pays iff w(E_1 − E_2) > h, i.e. w > h/33.6.
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

## 4. Scope: does it apply to any adaptive system?

**Where the assumptions fail:**
1. **The world reacts to you.** Adversaries, markets, games, or g > 0. Exogeneity is broken, so the opponent's strategy has to be in the model; this becomes a game, not a tracking problem.
2. **Costs that do not separate or add.** Coordination, legitimacy and politics (J16 is the kill rule for this), and fixed plus proportional costs (S4 crossovers).
3. **Non-stationary laws.** Regime shifts mean the input is not a stable spectrum, so it must be re-measured or modelled as a switching law (N16).
4. **Non-Gaussian, jump or heavy-tailed worlds, other losses, nonlinear Bayes trackers.** The layer theorems are linear-Gaussian only (G4).
5. **Goals beyond tracking.** Exploration, construction and play. J prices staying matched, not what is worth wanting (THEORY §0).
6. **Weak selection.** "Should be built" holds; "are built" is untested (G2, G7).
7. **Indivisible reads.** No clock gain (Prop 9).
8. **Separate stores versus separate agents.** These are not distinguished without the member axis (G5).

**What "every scale" can mean.** The same problem, solved with each system's own measured law and prices, in that system's single currency (Theorem S, S1). It cannot mean one exchange rate across scales (S4), and it is not a proof beyond the stated classes.

## 5. Ace's ideas (t1974u), each on its merits

**(a) A variational principle ("sit near argmin J", like least action). PARTLY HOLDS.**
- As a **normative** principle ("should be built") it holds by construction.
- As a **descriptive** one, it is a selection hypothesis, not a law. Unlike least action, it has free prices, so it says nothing until either (i) its world-free structure (Master Theorem ii: K\* nondecreasing in w/h, f\* nondecreasing in w/c, K\* ≤ the world's predictive degree) or (ii) independently measured prices pin it down.
- Comparative statics are the right content, but **signs are robust and magnitudes are not**.
- Drop "like least action" from the public text. It invites a comparison it loses.

**(b) Exponent predictions that do not need unmeasured costs. PARTLY HOLDS.**
- **Holds:** the read-rate elasticity in drift is 1/α within one system, if c and w do not move with q. It is proved for hold-last-value and for any predictor class closed under time rescaling (CT12). This is the N51 lab test and needs no w.
- **Also cost-free:** the onset exponent is set by the level's technology (Result 4), and the flatness of CT13.
- **Fails:** "layer spacing set by α alone."
  - In the clock model, spacing is e^{L/K}, and K depends on C/h (L4).
  - In the store model, spacing depends on span and noise (PROOF_A Exp3).
  - At α = 2 there are no layers at all (L1).
  - Layer count always needs R = wE/h.
- So (b) shrinks gap G3 for the rate predictions but does not close it for the layer predictions.

**(c) The inverse problem: revealed costs. PARTLY HOLDS. Circular when exactly identified, real when over-identified.**
- Only price **ratios** are identified (w/c, h/w), by homogeneity (S1).
- With a free c_k per layer, any observed K layers and K rates can be fitted. That is circular.
- It becomes a test when there are more observed design features than free ratios. Three ways to get there:
  - one system observed at several exogenous q (the implied w/c must be constant, and the rates must move as q^{1/α});
  - several items under one clock (Result 5: equality iff c_i/(w_iσ_i²) is equal);
  - the same read technology across layers.
- This is Afriat/Varian revealed preference and Kalman's 1964 inverse-optimality question applied to design. It is a real way around the w bottleneck, and the repo should state the over-identification count for each test.

**(d) The ruin multiplier as a price of survival. HOLDS (diffusion approximation, Lundberg sufficient bound).**
- μ = −m′/θ′ at the binding constraint. It is the marginal expected cost of extra survival exponent.
  - It is 0 for B ≥ B_slack, where the expected-cost rules hold exactly.
  - It rises toward the feasibility edge B_min, below which no design survives. This is the constructive face of Theorem P's "not viable".
  - At B = 0.5 it is μ = 0.0052 per unit θ, and the buffer is worth dJ\*/dB = −0.145.
- **It unifies Theorem L.** EOQ is the μ = 0 end and Theorem L's survival-optimal interval is the μ → ∞ end. The constrained optimum moves between them (0.236 ↔ 0.316 in the check). This is the same direction as risk-sensitive control (Jacobson 1973).
- μ carries the system's own units, so it is not comparable across systems.

**(e) Recursion: J of J's. PARTLY HOLDS.**
- **The real part:** closure under coarse-graining.
  - A pooled level is a tracker with stake W = Σw_iB_i² and the same power-class cost φ ∝ p^{1−a}W^a q^b.
  - Pooling n identical members costs n^{a−1} of n separate trackers (checked).
  - Sums of Gaussian random walks are random walks (T7c).
  - So a level faces the same problem as a member, and "same form at every scale" is a **closure property**, not an assertion.
- **The conditions:** a Gaussian world, quadratic loss and power-class costs. It breaks with fixed plus proportional costs (S4) and with heavy tails (the loss must change).
- **Fixed point:** this is not a fixed-point *theorem*. Nothing forces real systems into the closed class.
- **Federation:** LAT-1's reach cap does fall out of the E term. Federation itself needs a coupling-cost term that J lacks: federate iff Σ_i J_i\* + J_coupling < J\*_single.

**(f) One common currency (free-energy units). PARTLY HOLDS AS INEQUALITIES; FAILS AS ONE CURRENCY.**
- The right form is one equation per system in that system's currency, with physics adding **price floors**:
  - price per nat acquired or erased ≥ kT (Landauer; Barato et al.);
  - the holding floor can approach 0 for slow drift (SCALE_ENDS E3).
- Converting attention or money to joules has no fixed rate. Above the cell, firm prices sit 10⁵ or more above the floor (THEORY l.52), so the kT form and the money form share a *shape*, not a currency.
- The only currency-free exchange rate is Kelly growth: a bit buys ln 2 of log-growth, for multiplicative systems (S5).

**(g) The stronger form I would put forward.**
- **Layers are the components of the world's predictive state that are worth their upkeep.** K\* is the number of predictive-state dimensions whose marginal value w·(E_{k−1} − E_k) exceeds h.
- K\* is nondecreasing in w/h and capped by the world's predictive dimension: the McMillan degree in linear-Gaussian worlds, and statistical complexity (Crutchfield & Young 1989) or predictive information (Bialek et al. 2001) in general.
- This ties "layered, at the world's time scales" directly to the world's measured law.
- It is **proved in 𝓜_LG** (Master Theorem ii–iii) and a **conjecture** beyond it. A two-state switching world (G4) would be the first test.

## 6. What this equation makes possible

1. **One checkable claim map.** Each result becomes "J with these restrictions". This review found three mismatches that way: the Theorem L wording, (q, α)-only inputs, and the CT7 currency.
2. **A design calculator.** Measure the law, price c, h and w, then get K, the read rates and the sharing.
3. **World-free sign predictions** (Master Theorem ii), which hold for any world.
4. **Cost-free exponent tests** (N51) and **over-identified revealed-cost tests** (§c), which are the two ways around G3.
5. **The price of survival:** one dial connecting EOQ, Theorem L and Theorem P.
6. **A sharp kill rule:** a level whose design needs a cost J cannot book (J16), or a design that misses argmin with measured inputs.

## 7. Top fixes before it goes at the top of the core

1. **Call it the problem statement.** Credit Axiom 5 (AXIOMS l.64), Sims, Tishby & Polani, Ortega & Braun, Genewein et al. and Meier et al. Never call it a theorem or a discovery.
2. **Fix the Theorem L sentence.** Theorem L says EOQ is the limit of policy-insensitive variance, and its optimal interval ignores B. Add Lemma (iv): under the chance constraint, a large buffer makes the constraint slack, giving the expected-cost rules, with multiplier μ.
3. **The world enters through its measured law** (spectrum or Markov law), with (q, α) as the scale-free special case.
4. **Generalize the read term** to information-acquisition spend (per read, per nat, per precision). Add κ_b, d and u, or Results 4 and 8 and CT7 do not come out of J.
5. **Set g = 0 in every theorem.** Keep g as an open lever (CL11), because it breaks exogeneity.
6. **Mark CT7 as a floor (inequality)** on the acquisition price, not a solution.
7. **Reword "layers at the world's time scales"** to "one layer per separated time scale of the world, each layer's memory set by that scale and the sensing noise". In the example, a 90-day mode gets a 6–12-day store.
8. **Add the Master Theorem**, with its world-free monotone part, and get L1–L3 plus Lemma (iv) independently reviewed (G8).
9. Keep "should be built" until a same-system test exists.

## 8. Recommended statement for the top of the core

> **The problem.** A system that must act ahead of a world it does not control chooses its design D (how many layers, what each tracks, how and how often it senses, and what it shares) to minimize, in its own currency,
>
>  J(D) = [κ·I_mem + h·K] + w·E[ℓ_D] + [information-acquisition spend + link, telling and lookup costs],  subject to P(ruin) ≤ ε,
>
> with the world entering only through its measured law. This is the theory's definition of the problem, not a theorem. The theorems are its solutions in stated classes (Appendix B): how often to look, when to share, how far one tracker reaches, and when layers pay. In every world, more layers pay as stakes rise relative to upkeep. No more layers pay than the world has predictive time scales. Survival is free when the buffer is large and decides the design when it is not. The bet, untested, is that strongly selected systems sit near these solutions once their inputs are measured.
