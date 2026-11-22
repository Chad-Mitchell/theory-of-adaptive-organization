# Mathematical completeness audit

Hostile independent reading of `main` at `2eeab306ce1e50a3d8a8e658906b7e2401310998` (22 November 2026). The commit named in the request, `d1a6de4`, is not in this clone. The tree that was read is current `main`, which already contains `theory/SELECTION_AXIOMS.md` and `theory/MASTER_EQUATION.md`.

`python3 tools/check_consistency.py` returned PASS (0 FAIL; two advisory length warnings). `python3 -m pytest -q tools` returned 175 passed and 1 skipped (Lean is not installed, so the suite did not build it). `lake build` was not run. Those checks run the repository's own scripts. They are not a proof of the representation gap in §3.1.

This note does not re-derive the stationary excess in `theory/SELECTION_AXIOMS.md` and does not re-check the special-case algebra in `theory/meq_checks/meq_derive.py`. Both already take \(J\) as given. The question is whether anything upstream forces that \(J\).

Status words are the repository's: **PROVED (in-model)** is a theorem inside a stated model; **KNOWN** is a cited published result; **NUMERICAL** is a computation; **OPEN** is not derived. "In-model" is not a claim about cells, firms, or cities. There is no file `theory/LAYER_CONVEXITY.md` and no file `theory/COADAPTATION.md`. The convexity claim lives in `core/KEYSTONE_NOTE.md` and `theory/HT_INDEX.md`. Coadaptation lives in CT31–CT32 and CX2.

Citations below were resolved on the Crossref API on 22 November 2026. A DOI is printed only when the returned title and authors match the work. Books and the 1948 Shannon paper are marked when Crossref returned a reprint or a review rather than the original issue.

---

## 1. Load-bearing claims in the core

"Load-bearing" means: if the claim fails, either the hypothesis sentence or the assertion that this \(J\) is the cost of judgment fails with it. The long list of in-model corollaries (CT11–CT19, CT26–CT32, CT35–CT43) is not repeated. They are consequences of a restricted \(J\), and `meq_derive.py` checks that several of them are restrictions. A restriction check is not a derivation of the objective.

| Claim | Where it is stated | CLAIM_MAP | What it actually assumes | Scope | Lean |
|---|---|---|---|---|---|
| \(J=\kappa I_{\mathrm{mem}}+hK+w\mathbb E[\ell]+A+L\) subject to \(P(\mathrm{ruin})\le\varepsilon\) | THEORY.md:25–39; CORE.md:15–24 | No row. Appendix C does not index it. It is the problem statement | One currency (A4). \(A\) and \(L\) are unspecified functionals of the design. Three pricings of \(A\) are used (per read, per nat, per precision). Ruin is a hard constraint, not a term | Posited for any exogenous system. Not derived | `FiniteDesignMenu.J` defines \(J=S+wE\) on a finite menu with ruin slack or absent. It does not derive the split |
| Strongly selected systems sit near the minimum | THEORY.md:41–44; the principle at THEORY.md:71; the assumption at THEORY.md:209 | The hypothesis is not a row. R1–R3 are the side-note remainder | R1 needs A2-L, haploid Moran or a named Wright–Fisher exponent, \(N\mu\ll 1\), a connected undirected graph, equal clocks, and a quadratic well. A2-M is not enough. The note is not folded into THEORY.md | Static excess is PRIOR ART under those hypotheses. The drifting sum R2 is one model. No real class is qualified | Not formalized. README.md:76 says the hypothesis is a claim about the world |
| Information floor (S1): \(J\ge\min(\kappa I+c\,r+w\max(D_{\mathrm{IB}},D_{\mathrm{seq}}))\) | `theory/SHANNON_2026-11-21.md`:31–35; CORE.md:28 | No row. S1–S3 are absent from CLAIM_MAP and from Appendix C | Exogenous, stationary, ergodic. Assumption S-A: acquisition cost \(A\ge c\cdot r\) for directed information rate \(r\). \(L\ge 0\). \(hK\) is dropped. Ruin is not in the floor | A relaxation bound. Joint \((I,r)\) feasibility is OPEN. Drifting worlds are CX1, OPEN. One scalar Gauss–Markov curve has a closed form | Not formalized. CT1–CT3 are listed as absent (README.md:89) |
| Frontier dual S2 and Farrell split S3 | SHANNON.md:62–79; CORE.md:30 | No row | S2 is the support function of a set of resource vectors. It equals operational least cost only if some minimizer has \(A=c\cdot r\) and \(L=0\). S3's product identity is for \(C=\kappa I+c\,r\), not for \(J_{\mathrm{floor}}/J\). Ruin need not preserve convexity | Standard convex analysis once the set is defined. The set is not computed outside one Gaussian example | CT33's concavity in the single price \(w\), finite menu only |
| Theorem P / CT1–CT4: mean loss \(\ge D(I_{\mathrm{pred}})\); a model is necessary when blind play is not viable; lead is capped; the first bit pays when the right slope at 0 is negative | THEORY.md:262–280; GENERAL_THEOREM.md §2 | CT1, CT2, CT3, CT4, all PROVED (in-model). CX1 OPEN | CT1: exogenous stationary ergodic, single-letter distortion-rate function of the marginal, integrable loss. Equality-case recurrence is asserted, not proved. CT4's closed form is scalar Gaussian AR(1), squared error, \(\kappa\) per bit, unit stake | Stationary exogenous. The Gaussian constant is one plant. The slope test is wider and still not a bound on operational \(J\) inside Lean | CT4: convexity of \(L(I)=D(IB(I))+\kappa I\) and the slope sign. README.md:80: "That \(L\) is a lower bound on cost is not formalized." No Gaussian closed form |
| Hold, fade, effort: CT8–CT10 | THEORY.md:304–318 | CT8, CT9, CT10 PROVED (in-model) | Stationary Markov, any loss, renewal checks. CT8 fails for non-Markov coordinates (MA(2), seasonality), and the text says so | The broadest positive class in the file | CT10 only, and only as discrete decreasing differences on a frequency coordinate |
| Master Theorem (i)–(iv) in \(\mathcal M_{LG}\) | THEORY.md:77–97; MASTER_EQUATION.md:15–45 | CT20, CT21, CT22, CT33 PROVED (in-model) | Exogenous Gaussian, white noise or exact reads, first-order LTI stores on a compact rate set, squared error, ruin via a Lundberg certificate. (ii) needs sensing fixed and ruin slack. With reads chosen, \(K\) can fall. With ruin binding, spend can fall | Linear-Gaussian, and narrower once the monotone claims are stated honestly. Existence on a continuum is Weierstrass plus an unproved continuity claim | Finite menu: existence, \(K\le J(d_1)/h\), and monotone \(K\) when spend is exactly \(hK\). Not the continuous parameter set. Not CT21. Not the binding multiplier |
| Layer cap CT21 / L1–L3, and N60's count | THEORY.md:81, 431–435; LAYERS.md §2; HT_INDEX.md:48–54 | CT21 PROVED (in-model). N60 PROVED (in-model) given convexity, and the convexity is numerical | Squared error, linear-Gaussian, noisy sensing. N60 needs discrete convexity of \(\varepsilon_K\), which is unchecked as a proof (120/120 and related scans). The written cardinality starts at \(K=1\) | Real poles for the increment formula. False for rhythms inside \(\mathcal M_{LG}\) (`core/KEYSTONE_NOTE.md`:46, formula 2 against argmin 3). A fractal spectrum does not force a stack (`theory/LAYER_LIFETIME_2026-11-21.md`:17–65) | Hull: every minimizer lies on the lower convex hull. Adjacent walk only under an assumed discrete convexity. The written cardinality, and the \(K^*=0\) hole, are not certified (README.md:79–80) |
| Physics floor CT7, \(J^*=\sigma\sqrt{2kT\cdot w}\) | THEORY.md:294–298 | CT7 PROVED (in-model) | A random walk the tracker does not affect; a learning rate at least \(\sigma^2/(2D)\); that rate charged at \(kT\) per nat via Barato, Hartich & Seifert | One plant, no feedback. MASTER_EQUATION.md:56 calls the match PARTIAL: it prices nats acquired, not \(\kappa I_{\mathrm{mem}}\), and the shape is forced by dimensions | Not formalized |
| Cost shares CT24 | THEORY.md:101, 449 | CT24 PROVED (in-model) | \(J=\sum p_i\varphi_i\) with a feasible set that does not depend on prices. Binding ruin is a counterexample, and the text gives one | Any objective of that homogeneous form. The ratio \((\alpha-1):1\) is the single exact-read power-law tracker | Not formalized |
| Ruin price CT22 | THEORY.md:439 | CT22 PROVED (in-model) | Unique unconstrained minimizer, quasiconvex \(J\) and quasiconcave Lundberg exponent along a scalar path. "Infeasible" means "not certified", not "ruins" | One diffusion reserve. The binding-path claim is a citation of KKT, not a written argument | Slack certificate and \(B_{\min}\le B_{\mathrm{slack}}\) only. README.md:88: the multiplier and the binding region are not formalized |
| Selection remainder \(d/(2\beta)\) | SELECTION_AXIOMS.md §3–§4 | R1 PRIOR ART. R2 PROVED (in-model) as a sum. R3 OPEN | J given (A1, line 23). A2-L, not A2-M. R2 adds SA2-A–C: additive split, timescale separation, zero discount, Brownian lumpy coordinate, the optimum moves only in that coordinate. Coefficient 6 was not matched to the cited papers' displayed equations (line 109) | Named population processes. Not "selection". No finite-time rate (SA4) | Not formalized |
| Scale covariance, Theorem S | GENERAL_THEOREM.md §6; THEORY.md Lemma B12 | CL3 PROVED (in-model) | Homogeneity in one currency; self-similar drift; loss \(\lvert e\rvert^p\). S4: two differently scaling cost components, and covariance fails | A classification of exponents, plus an explicit failure | Not formalized |

The hypothesis sentence is unchanged and is still a hypothesis. R1 does not promote it. THEORY.md:209 still says selection within \(\varepsilon\) of the cheapest design is an assumption.

---

## 2. Shannon's four demands

Shannon's standard, used here as the floor: (a) the central quantity is the unique object satisfying stated axioms; (b) a coding theorem with a construction that meets the bound and a converse that no scheme beats it; (c) the hypotheses are explicit and the theorem is for a class, not one plant; (d) every term is an operational quantity. Entropy's uniqueness is the 1948 theory together with the Faddeev axioms as stated by Aczél, Forte and Ng (doi 10.2307/1426210) and surveyed by Csiszár (doi 10.3390/e10030261). The coding theorem is Shannon's source and channel theorems; the fidelity version is the 1959 convention paper, which Crossref returns as the IEEE reprint doi 10.1109/9780470544242.ch21 and not as a 1959 record.

### (a) Uniqueness of the central quantity — missing

\(J\) is posited. THEORY.md:39: "The equation is assembled from known parts… It is the theory's statement of the problem, not a theorem." CORE.md:24: "The equation is a definition, assembled from known parts." SELECTION_AXIOMS.md:23 uses that definition and "does not reopen the term list."

What is unique, off the shelf, is Shannon information, once an information measure is already the object and Faddeev's axioms are granted. That fixes \(-\sum p\log p\). It does not choose gross mutual information against predictive information, directed information, or \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\), and the repository uses all four. It does not put a linear price on the chosen measure, and it does not add \(hK\), a stake, a read functional, a link functional, and a ruin constraint.

The deepened verdict — axioms that would have to be added, which representation theorems they are, and where the uniqueness fails — is §3.1. Short form: a theorem that starts from "store, predict, act, stay solvent" and concludes this additive \(J\) is not plausible. The chain the author wants is open at that first arrow.

### (b) Achievability and converse — partly met, and only for a relaxation of the information terms

**Converse, as far as it goes.** S1 is a real lower bound under S-A, for an exogenous stationary design: expected loss is at least the information-bottleneck distortion and at least the sequential distortion, so it is at least the max, and the linear combination of those resources can be minimized. CT1 is the same idea with the single-letter distortion-rate function of the marginal and a ruin reading of a negative mean margin. Both are relaxations. A design that meets \(D_{\mathrm{IB}}(I)\) need not meet \(D_{\mathrm{seq}}(r)\) at the same point, and S1's minimum is allowed to range over pairs \((I,r)\) no design attains. A relaxation is a lower bound. It becomes a Shannon converse when every design is at least the bound and some design meets it.

The bound does not charge \(h\). SHANNON.md:41 gives a memoryless design with \(K=0\) and \(I_{\mathrm{mem}}>0\) that undercuts any floor which adds \(h\). There is no proved floor on the number of layers. LAYER_LIFETIME.md:17 scores the hope that \(T^*\) would supply one as not met. The ruin cap can only raise the minimum, and no formula for the rise is derived (SHANNON.md:49).

**Achievability.** On one scalar Gauss–Markov plant, the Kalman filter meets the directed-information term when memory is free, and a noisy copy of the state meets the memory term when reads are free. Both are known (Tanaka, Kim, Parrilo and Mitter, doi 10.1109/TAC.2016.2601148, for the sequential Gaussian tradeoff). With both prices positive, the best one-layer Kalman design on a 36-point grid sits 4.26% above the relaxation floor on one world (\(a=0.9\), \(Q=1\), lead 2), layer price left out of both sides. SHANNON.md:55 leaves open whether the true minimum equals the floor or lies strictly above that design. Several time scales are OPEN. So the matching pair "construction meets the bound, and nothing beats it" is absent for the objective the theory actually minimizes, which has both prices, a layer price, and a ruin cap.

### (c) A stated class, not one plant — partly met

The hypotheses are unusually explicit, and several theorems say where they stop. That part meets the standard.

The theorems do not share a class.

- Any design menu, any loss, ruin slack: CT33 (revealed preference). This is comparative statics of \(J=S+wE\). It is not a description of the minimizer's structure.
- Any stationary Markov world, any loss, renewal checks: CT8–CT10. False for non-Markov observations, with a counterexample in the proof.
- Stationary ergodic exogenous worlds: CT1, as a single-letter bound.
- \(\mathcal M_{LG}\): the Master Theorem. Gaussian, squared error, linear filters.
- One scalar AR(1): the CT4 constant. One random walk: CT7. Power-law increments and exact reads: CT12. Haploid Moran, weak mutation, log-linear fitness: R1.

CORE.md:7 says the proved limits "hold by proof, like Shannon's limits." Shannon's limits are one pair of theorems for every discrete memoryless channel and every stationary source in the class. The sentence attaches that scope to a list of plant-level theorems. The attachment is the overstatement.

### (d) Operational meaning — partly met

The five slots are named, and the qualification rule in THEORY.md §3 says how a class would be measured. Several terms still do not have one operation.

- \(\kappa\) is "per nat" in the master equation (THEORY.md:31) and "per bit" in CT4 (THEORY.md:278). The closed form is the bit derivative. See §4.
- \(I_{\mathrm{mem}}\) is nats held, \(I(M_t;X^t)\), and, in CT4, bits. \(I_{\mathrm{pred}}\) in the notation table (THEORY.md:223) is a single-time mutual information. Bialek, Nemenman and Tishby's predictive information is a different functional. The proofs use the single-time quantity. The English in §1 does not keep them apart.
- \(A\) has three definitions. \(L\) has three summands. MASTER_EQUATION.md:62: no layer theorem uses \(\kappa\) and \(h\) jointly.
- Ruin is two constraints. THEORY.md:185 says so: lifetime Lundberg ruin, and a per-window chance constraint (CT25). CT22's "infeasible" means "not certified by a sufficient bound".
- "Layer" is a first-order store, a McMillan degree, an org-chart level, and a lumpy reset. CT21's "a rhythm counts two" is a degree count. The objects one would build, real first-order stores, do not come in twos on the worked rhythm (`core/KEYSTONE_NOTE.md`:46).

S-A, the inequality \(A\ge c\cdot r\), is labeled an assumption and not a sensor law (SHANNON.md:29). Sagawa and Ueda (doi 10.1103/PhysRevLett.102.250602; erratum doi 10.1103/PhysRevLett.106.189901) bound measurement work and erasure work together. They do not provide a second thermodynamic price to stack on a Landauer floor under \(\kappa\). The text says this. It is the right reading, and it leaves \(c\) without an operational floor.

---

## 3. Ranked gaps

The order is the order in which a proof would change what can be claimed. Difficulty is the mathematical size: a short argument from a cited theorem, a paper, or a program. Calendar time is not estimated.

### 3.1. A representation theorem for this \(J\). Likely false. The negative statement is short. This is the upstream gap.

**What is already done, and is not this gap.** `theory/SELECTION_AXIOMS.md` derives the stationary excess \(d/(2\beta)\) with \(J\) given (A1, line 23). R1 is Sella and Hirsh's weight (doi 10.1073/pnas.0501865102) plus equipartition on a quadratic well. R2 adds the lumpy lag under SA2-A–C by linearity of expectation. `theory/MASTER_EQUATION.md`:15–45 states the Master Theorem in \(\mathcal M_{LG}\): existence, monotone comparative statics with sensing fixed, the degree cap, and the Lundberg certificate. `meq_derive.py` checks that listed special cases are restrictions of \(J\). MASTER_EQUATION.md:11 already records the complete-class objection: every admissible design is optimal for some cost, so a free \(J\) has no content beyond price-free structure and independently measured prices. None of that produces the objective.

**The theorem that would close the chain.** Call it U.

> Let a design specify a memory, a finite collection of stores, an action kernel, a read channel, and a link structure. Suppose the only axioms are that the system stores, predicts, acts, and remains solvent in the sense \(P(\mathrm{ruin})\le\varepsilon\). Then any cost consistent with those axioms equals \(\kappa I_{\mathrm{mem}}+hK+w\mathbb E[\ell]+A+L\), uniquely, or uniquely up to a stated equivalence, and the selection map of A2-L applied to that cost has stationary excess \(d/(2\beta)\).

U is the missing first arrow. The second arrow is R1, and it is already proved under A2-L. U is likely false. The second arrow cannot repair it.

**Why "store, predict, act, stay solvent" does not determine the sum.**

Those four demands constrain the feasible set and the viability criterion. They do not choose a functional on that set.

- Storing is satisfied by any memory. The axiom does not say the cost is linear in a Shannon information of that memory.
- Predicting and acting are satisfied by any kernel from memory to actions. An expected loss is one scoring of the kernel. A shortfall, a quantile, and a probability of a miss are others. vNM expected utility (von Neumann and Morgenstern, *Theory of Games and Economic Behavior*, commemorative edition doi 10.1515/9781400829460) can force an expectation, and only after completeness, transitivity, continuity, and independence are assumed for preferences over lotteries. Those are axioms about preference, not about persistence.
- Solvency is satisfied by any rule that keeps the ruin probability down. Expected cost with a chance constraint, the Lundberg exponent (Theorem L), Kelly growth, and the lineage mixture in CT42 all do that. They are not the same function. THEORY.md:403 and MASTER_EQUATION.md:57: the survival-optimal interval agrees with the expected-cost interval when the reserve's own noise dominates, not because the buffer is large. GENERAL_THEOREM.md:292 still says "large-buffer, policy-insensitive-variance" in one breath. The canonical correction is the one in THEORY and in MASTER_EQUATION. The disagreement is the point: "stay solvent" is a family of objectives.

**What would have to be assumed, and which cited theorem it actually is.** Each of these is an extra axiom. None of them is a restatement of persistence.

1. **Separability of named coordinates.** Fix coordinates \((I, K, \bar\ell, r, \lambda)\) for information, store count, mean loss, read resource, and link resource. Assume preferential independence: the ranking of two values of one coordinate does not depend on the others. Debreu's additive representation (the essay "Topological methods in cardinal utility theory", Crossref reprint doi 10.1017/ccol052123736x.010) then gives \(C=\sum_i f_i\) with each \(f_i\) continuous and increasing, unique up to one common positive scale and additive constants, once at least two coordinates are essential. This is the closest real theorem, and its hypothesis is separability. Separability is the claim under examination, not a consequence of storing and acting.

2. **Linearity of each \(f_i\).** Debreu does not give \(f(I)=\kappa I\). An arbitrary increasing \(f\) has the same argmin only if it is strictly increasing in a one-dimensional problem; with several coordinates the composition \(\kappa I\) and \(f(I)\) have different minimizers. Linearity needs a concatenation axiom: the cost of independent copies adds, there is no fixed charge, and there is no capacity ceiling. Monotone solutions of Cauchy's equation \(f(x+y)=f(x)+f(y)\) are linear. That axiom excludes a hard information capacity (Sims, doi 10.1016/S0304-3932(03)00029-1, uses both a capacity and a linear penalty; they are duals, not the same primal) and excludes a submodular cost of layers, which is the natural reading of "the next store is worth less".

3. **Which information.** Given Faddeev's axioms, the measure is Shannon's (Aczél, Forte and Ng, doi 10.2307/1426210; Csiszár, doi 10.3390/e10030261; Khinchin, *Mathematical Foundations of Information Theory*, Dover 1957, of which Crossref resolves reviews, for example doi 10.1126/science.128.3329.894-c, and not a DOI for the book; Shannon 1948 is returned as the reprint doi 10.1109/9780470544242.ch1). The axiom set has to say that an information measure of the memory is the coordinate. It still has to choose \(I(M;\mathrm{past})\), \(I(M;X_{t+k})\), directed information (the currency of S1; Tatikonda and Mitter, doi 10.1109/tac.2004.831187), or \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\). The repository's own theorems make different choices. Uniqueness of entropy does not choose.

4. **One currency.** The sum is defined only if the pieces are commensurate (A4). Theorem S4 is the counter-model: a fixed cost plus a size-proportional cost, and the optimum crosses over instead of obeying one homogeneous law. A representation in one currency is a per-system accounting convention. It is not a universal derivation.

5. **The ruin axiom has to pick expected cost.** Chance-constrained expected cost (the master equation), maximize the Lundberg exponent (Theorem L), maximize expected log growth (Kelly; the multiplicative bound the repository credits to Donaldson-Matasci, Bergstrom and Lachmann, doi 10.1111/j.1600-0706.2009.17781.x), and maximize lineage growth under shared shocks (CT42, a mixture) are four expressions of "remain solvent". Affine equivalence covers only the first, and only after separability. The selection note attaches A2-L to the numerical value of \(J\). If solvency points at \(\theta\) or at a growth rate, A2-L is applied to the wrong function, and \(d/(2\beta)\) is the excess of a stand-in.

**What Landauer and rate-distortion contribute.** They contribute bounds.

- Landauer (doi 10.1147/rd.53.0183) is an inequality on the erasure piece of a physical cost. Still, Sivak, Bell and Crooks (doi 10.1103/PhysRevLett.109.120604) give, under their hypotheses (driven, no feedback, Markov, a heat bath), a dissipation equal to \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\) per step, in units \(kT=1\). That functional depends on how predictive the memory is. It is not \(\kappa I_{\mathrm{mem}}+w\mathbb E[\ell]\). Barato, Hartich and Seifert (doi 10.1088/1367-2630/16/10/103024) bound a sensor's learning rate by its entropy production in a bipartite model. CT7 identifies that bound with \(kT\cdot\sigma^2/(2D)\) for a random-walk tracker. The identification is an extra model, and MASTER_EQUATION.md:56 already says it does not price \(\kappa I_{\mathrm{mem}}\).
- Sagawa and Ueda's bound, with the erratum, is one inequality for measurement plus erasure. Stacking \(\kappa I_{\mathrm{mem}}\) and \(c\cdot r\) as two thermodynamic costs double-counts that inequality. SHANNON.md:29 already refuses the stacking. A representation that treats both prices as physical floors contradicts that refusal.
- The causal rate-distortion function (Tatikonda, Sahai and Mitter, doi 10.1109/TAC.2004.834430; Tanaka, Kim, Parrilo and Mitter, doi 10.1109/TAC.2016.2601148; the scalar Wiener case is Berger, doi 10.1109/tit.1970.1054423) describes the feasible set of \((r,D)\). The linear combination \(\kappa I+c\,r+w D\) is a support function of that set, which is S2. A support function is the dual value of an already linear pricing. It is not a derivation of the pricing.

**Where U fails inside material the repository already has.**

- **Still's cross term.** If the cost of memory is the thermodynamic dissipation, it depends on \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\). Separability in \((I_{\mathrm{mem}},\mathbb E[\ell])\) fails on that functional.
- **Non-separable design costs.** CT34(ii): the team's optimized cost is a constant upkeep only when what the parent passes down does not depend on the parent's design, and the "only if" direction is not proved (§4). CT34(iv): a shared driver is not weak coupling, and the sum of standalone costs misses the pooling gain. CT36: joint value can exceed the sum of the separate values when a shared store is a common-mode reference. A theorem that forces \(hK\) as a sum of per-layer upkeeps is false for those designs. Partial minimization can still write the parent's problem as \(F(x)+J_T^*(\theta(x))\). That is exact and it is not the five-term form with a constant \(h\).
- **CX2, responsive worlds.** MASTER_EQUATION.md:61: a positive effort spent reducing drift makes the world's law depend on the design and drops every proved theorem (CL11, OPEN). Touchette and Lloyd (doi 10.1103/PhysRevLett.84.1156) bound how much feedback can reduce entropy by the information gathered, which also says the agent can buy the same persistence by changing the world. The cost of that intervention is a coordinate \(J\) does not have. Any representation proved for an exogenous product space stops at the boundary the repository marks CX2. The term list is incomplete on the other side of the boundary, so it is not the unique cost of persistence.
- **A2-M.** Even if U were true, monotone copying does not give \(d/(2\beta)\). SELECTION_AXIOMS.md:28 says so. The chain needs A2-L as a further axiom about fitness, not as a consequence of U.

**Equivalence is not free, because the excess is cardinal.** Any strictly increasing transform of \(J\) has the same argmin on a fixed menu and a different excess. An affine transform \(aJ+b\) is absorbed into the fitness slope \(\alpha\) for the absolute excess \(d/(2\beta)\), because that excess is computed on the quadratic well above \(J^*\). The same constant \(b\) changes \(J^*\) and therefore changes the fractional excess \((\mathbb E[J]-J^*)/J^*\) used in Corollary SA1c and in the qualification band. Ordinal uniqueness would support "they minimize". It would not support the number \(d/(2\beta)\) unless the zero and the scale of \(J\) are fixed. The chain U then R1 needs a cardinal representation, not an argmin representation.

**What is plausible instead.** A lemma that assumes separability, concatenation, one currency, an exogenous world, and expected cost with ruin as a constraint, and concludes linear \(J\) up to one scale, is plausible and short. It is Debreu plus Cauchy. It should be labeled as a list of assumptions. It is not a theorem about persisting systems, and it is not U. Writing it would make the hypothesis's hypothesis list honest. It would not make \(J\) derived.

**Route, if the negative statement is the one that gets written.** Exhibit four functionals consistent with store / predict / act / stay solvent, with different argmin: chance-constrained \(J\), the Lundberg objective (Theorem L, already computed to disagree with the EOQ interval), Kelly growth, and CT42's mixture. Exhibit Still's \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\) as a cost of memory that is not linear in gross \(I_{\mathrm{mem}}\). Exhibit CX2 as a sixth coordinate. None of these citations has to be new; the counter-models are in the tree. Difficulty: a short note. Likely false that a stronger U exists. I would not treat a search for U as open in the sense of "probably true, hard to prove". It is open in the sense of "not proved", and the obstruction is already on the page.

### 3.2. A matching information converse on one plant with both prices. Unknown; a strict gap is the likely outcome. A paper.

**Statement.** On the scalar Gauss–Markov world, with \(\kappa>0\), \(c>0\), \(h=0\), and ruin slack, either exhibit a causal design whose \((\kappa I_{\mathrm{mem}}+c\,r+w D)\) equals S1's minimum, or prove a strictly higher lower bound that a named design attains.

**Why it is load-bearing.** This is Shannon's (b) for the only piece of \(J\) that has an information bound at all. The 4.26% figure is one design against a relaxation. It is not a theorem that the floor is unattainable, and it is not a theorem that it is attainable.

**Route.** The sequential Gaussian problem is solved by a Kalman filter when the memory price is zero (Tanaka, Kim, Parrilo and Mitter, doi 10.1109/TAC.2016.2601148; the rate-cost form is Kostina and Hassibi, doi 10.1109/TAC.2019.2912256). The obstruction the repository points at is real: the filter state is a function of the observation history, so \(I(\hat x; X^t)\) can exceed \(I(\hat x; x_t)=\tfrac12\ln(V/P)\). A two-stage scheme that keeps only a sufficient statistic of the predictive state is the construction to try. For a first-order Markov plant the predictive state is one-dimensional, and a fresh noisy observation of \(x_t\) meets the memory bound while spending a different read rate. The minimum of the sum need not be the sum of the minima. I expect a strict gap. That is a judgment, not a proof. Difficulty: a paper, including the zero-delay constraint. Block coding with free delay is the wrong problem, because lateness is charged as loss (Neuhoff and Gilbert, doi 10.1109/tit.1982.1056552, causal source codes).

### 3.3. Extend the information lower bound to drifting linear plants. Likely true by citation. A short derivation.

**Statement.** For a linear plant with additive white driving noise, any causal policy whose long-run mean squared error is \(D\) has directed information rate at least the causal rate-distortion value of that plant, and the mean margin against income is nonpositive when that distortion exceeds the margin. This is CX1 for linear plants, not for arbitrary processes with stationary increments.

**Why it is load-bearing.** Most of the design theorems (CT12, CT18, CT19, the random-walk half of L1) live on drifting worlds, where CT1's stationary hypothesis is false. The core is split across that line.

**Route.** Nair and Evans (doi 10.1137/S0363012902402116) and Tatikonda and Mitter (doi 10.1109/tac.2004.831187) are the data-rate theorems. Berger (doi 10.1109/tit.1970.1054423) is the Wiener rate. The work is to match their hypotheses to the repository's lead time and its ruin reading, and to say in one paragraph what they do not give (a layer price, a matching achievability at both \(\kappa\) and \(c\), non-linear plants). A general-process CX1 is a different and larger problem. Difficulty of the linear case: a short derivation. Likely true.

### 3.4. Convexity of \(\varepsilon_K\) in Model S, and an honest count. Convexity unknown. The written formula is already false outside real poles.

**Statement.** For a finite sum of OU spectra in white noise, the minimal squared error \(E_K\) of a degree-\(K\) causal filter is a convex function of \(K\). Separately: the cardinality in HT_INDEX.md:50, including the blind option \(K=0\), equals \(\arg\min_K(hK+w E_K)\).

**Why it is load-bearing.** N60 is the only explicit layer-count formula. CT21's degree cap is an upper bound, not a count of what is worth buying. Without convexity the adjacent-increment rule can return the wrong integer, and KEYSTONE_NOTE.md:46 already exhibits that failure for two oscillators (formula returns 2, argmin is 3) inside the Gaussian class of the Master Theorem.

**Route.** The upper bound \(K\le J\) for \(J\) real modes at high stake is L2, and it is spectral factorization plus uniqueness of the \(L^2\) projection. Convexity is a statement about the MSE of best degree-\(K\) approximants of a rational spectrum. The nearest citation the repository found, Das and Kempe (doi 10.1145/1374376.1374384), is subset selection for linear regression, which is a different constraint. I do not know a proof, and 120 convex samples are not one. The \(K^*=0\) hole is not a missing idea: KEYSTONE_NOTE.md:31 records that the formula starts at 1, and the Lean development proves the ingredients of the hole without identifying the written cardinality with 0 (README.md:70, 79–80). Fixing the index is a definition. Proving convexity is open and may be a paper. A closed-form count for arbitrary spectra is likely false; L3 already says a non-rational spectrum has no exact finite design, and the rate at which \(K^*\) grows is conjectural.

### 3.5. A finite-time, assumption-light selection rate. Likely false in the form "any selection does this". The stationary special case is done.

**Statement that would match the hypothesis sentence.** Under a stated definition of strong selection that does not include A2-L, the occupied design's excess over \(J^*\) is at most a stated function of selection strength, with a proved approach time.

**Why this is ranked below the representation.** R1 already gives \(d/(2\beta)\) when A2-L, weak mutation, and the quadratic well are assumed. Re-proving Sella and Hirsh would not raise the Shannon status of the theory. SA4 says plainly that there is no finite-time bound: a Poincaré or log-Sobolev step is not claimed. A2-P, persistence without copying, is OPEN. A2-M does not give the constant.

**Route, if a rate is wanted inside the Moran model.** The stationary weight is done. A convergence time needs a spectral gap for the origination–fixation chain on the design graph. That is a standard Markov-chain estimate and it depends on the graph. It will not be uniform over graphs: SA4's valley obstruction (EVO1 W4/W4b) is already a counterexample to a uniform time. Likely false that the hypothesis sentence, as English, becomes this theorem. Difficulty of a graph-dependent gap: a paper. Difficulty of a universal rate: the claim is the wrong one.

### 3.6. Replace "KKT" in CT22's binding region with an argument. Likely true on the scalar diffusion path. A short proof.

**Statement.** Under the quasiconvexity hypotheses THEORY.md:439 actually lists, the constrained minimizer on the scalar path is the unique point where the Lundberg constraint is tight, the multiplier equals \(-m'/\theta'\), and the design parameter moves monotonically between the expected-cost optimum and the survival optimum as \(B\) goes from \(B_{\mathrm{slack}}\) down to \(B_{\min}\).

**Why it is load-bearing.** The "price of survival" is one of the four parts of the Master Theorem. The written proof is the word KKT and a numerical path. Lean checks the slack end only.

**Route.** Parameterize the path, write the Lagrangian in one variable, and use quasiconvexity to exclude other stationary points. This is textbook and local to Lemma B9's diffusion. It does not extend to a general design set; the text already says the path hypotheses are necessary. Difficulty: short. Likely true on that path.

---

## 4. Errors, gaps, and overstatements

Line numbers are the file as it stands at `2eeab30`.

1. **THEORY.md:31 against THEORY.md:87 and THEORY.md:278. Unit of \(\kappa\).** The master equation prices \(\kappa\) per nat. CT4 prices \(\kappa\) per bit and differentiates \(\mathrm{Var}\cdot a^2\cdot 2^{-2I}\). The derivative at zero is \(-2\ln 2\cdot a^2\cdot\mathrm{Var}\), so the bit threshold is \(\kappa<2\ln 2\cdot a^2\cdot\mathrm{Var}\). In nats, \(2^{-2I_{\mathrm{bit}}}=e^{-2I_{\mathrm{nat}}}\) and the derivative at zero is \(-2 a^2\cdot\mathrm{Var}\), so the threshold is \(\kappa<2 a^2\cdot\mathrm{Var}\). The summary table in §5 prints the bit threshold under a per-nat price. The factor between them is \(\ln 2\). The displayed \(I^*=\tfrac12\log_2(2\ln 2\cdot a^2\cdot\mathrm{Var}/\kappa)\) also contains no stake. If the loss is \(w\) times squared error, both the threshold and the log pick up a factor \(w\). The sentence "size grows with log stakes" is the dependence of that corrected expression. It is not the expression printed. GENERAL_THEOREM.md:137–138 is internally consistent (it says per bit) and prints the same unit-stake formula. The contradiction is between the canonical equation and its summary table.

2. **THEORY.md:266. Recurrence at a zero mean margin is not a proof.** The strict case, negative mean and ergodic integrable increments, is the ergodic theorem, and A5's bounded increments make the integrability cheap. The next sentence says ruin is still certain at mean zero "by recurrence", with a coboundary exception. No theorem is cited and no hypothesis (one dimension, finite variance, mixing) is used in an argument. The claim may be true for i.i.d. finite-variance increments. It is not proved on the page.

3. **THEORY.md:439. "Proof: the constraint set grows with \(B\); KKT."** Growth of the feasible set in \(B\) gives the ordering of \(B_{\min}\) and \(B_{\mathrm{slack}}\) once the certificate is the constraint. It does not produce \(\mu_s=-m'/\theta'\), uniqueness along the path, or monotone movement of the design. Those are the content of "the price of survival". The numerical path (one setting, \(\varepsilon_r=10^{-3}\)) is a check. Lean does not contain it (README.md:88).

4. **THEORY.md:472, "generically, only if".** Exact nesting when \(\theta\) is independent of the parent's design is proved, and Lean has that direction (README.md:59). The converse, that a flat team value forces \(\theta\) independent of \(x\), is an assertion. A flat restriction of a non-constant value function is the obvious obstruction, and the text says "can be flat in the direction \(\theta\) moves" without a topology or a measure that would make the word "generically" a theorem.

5. **THEORY.md:468 against the status PROVED (in-model) for CT32.** Part (i), the opposed linear system, is a conserved orbit and is a proof. Part (iii), the Jacobian, is a proof for those two linear games, and it shows time-scale separation moving gradient play to a point that is not Nash. Part (ii) is a simulation of a payoff table "taken from a secondary source and not checked against Shapley's chapter", and the text says "a simulation and not a proof". The claim-map row and Appendix C mark the whole of CT32 PROVED (in-model). The simulation should not inherit that label.

6. **THEORY.md:82 against THEORY.md:395. The fractional-Brownian check.** The main-text statement of the temperature identity says the self-similar form was "checked on simulated fBm". The proof note says one seed and rescaled Cholesky factors are reused, "so equality holds by construction, self-similarity being exact". The construction does not test the claim. The proof that does the work is the scaling argument, which is fine, and it does not need the check. The main text overstates what was checked.

7. **HT_INDEX.md:50 against KEYSTONE_NOTE.md:31 and :46. N60's cardinality.** Under discrete convexity the adjacent rule is right for the leftmost minimizer on \(\{1,\ldots,J\}\) when the paying set is a prefix. The printed formula \(1+\#\{k\ge 2: R(\varepsilon_{k-1}-\varepsilon_k)>1\}\) returns at least 1. CT21 allows \(K^*=0\). KEYSTONE records 379 comparisons where this is the whole disagreement. On two oscillators the same formula returns 2 and the argmin is 3, because the decrements are not monotone. The status "PROVED given convexity" is fair only inside Model S, on the set where the argmin is at least 1, and only while convexity is an assumption. CLAIM_MAP's N60 row does not carry the \(K^*=0\) exception in the displayed formula. Lean refuses to identify the written cardinality with the minimizer (README.md:79–80). That refusal is correct.

8. **LAYERS.md:35 against THEORY.md:81.** LAYERS.md's Theorem L1 concludes "\(K^*=1\) for every \(w\) and \(h\)". A single OU mode has finite blind error, so a positive \(h\) and a small stake make the blind design cheaper. THEORY's restatement, \(K^*\in\{0,1\}\), is the one that matches the proof that \(E_1=E_\infty\). LAYERS.md's header says the v2.4 reading changed and "this copy is otherwise not edited". The stale theorem statement is still the statement a reader of that file proves. KEYSTONE_NOTE.md:31 already flags it. It remains in the file.

9. **GENERAL_THEOREM.md:292.** "The expected-cost results are the large-buffer, policy-insensitive-variance limit." MASTER_EQUATION.md:57 and THEORY.md:403 separate those: agreement of the two intervals is the noise condition, and slackness of the chance constraint at large \(B\) is CT22. The file's own banner says it is a frozen derivation. Frozen does not make the sentence true. The canonical text corrected it. The derivation people are sent to for Theorem L still conflates it.

10. **SELECTION_AXIOMS.md:109. The coefficient 6 is re-derived, not matched.** The renewal arithmetic inside the note is consistent: occupation density \((b-\lvert x\rvert)/b^2\) on \([-b,b]\) gives \(\mathbb E[x^2]=b^2/6\), and \(b^*=(6k\sigma^2/w)^{1/4}\) gives \(T^*=\sqrt{6k/(w\sigma^2)}\). Dixit 1991 (doi 10.2307/2298051) and Chalkley 1997 (doi 10.1016/s0165-1765(97)00222-x) are real papers. The note says the coefficient was not checked against their displayed equations. "KNOWN, exact at zero discounting" claims a match that was not made. The internal derivation can stand on its own without that sentence.

11. **THEORY.md:292. CT6 is empty on the class the rest of the theory uses.** The strong data-processing bound is a theorem under its Markov hypothesis. For unconstrained Gaussian kernels the contraction coefficient is 1 and the bound says nothing. The linear-Gaussian theory then switches to a different contraction, cited and not proved in the file. CT6 does not support \(\mathcal M_{LG}\).

12. **CORE.md:7. "Like Shannon's limits."** The limits that are proved are catalogued in §1. They are not a coding theorem for a class. The comparison is the claim this audit refuses.

13. **Index gap.** S1, S2, and S3 are the Shannon-shaped core of CORE.md and of `theory/SHANNON_2026-11-21.md`. They have no CLAIM_MAP row and no Appendix C line. `tools/check_consistency.py` checks Appendix C against section O. It cannot see a claim that was never indexed. R1–R3 are indexed. The absence is not a failed check; it is a missing row for the claims §2 of this audit is about.

`python3 tools/check_consistency.py` on this tree: PASS, 0 FAIL, 26 INFO hits in frozen records, advisory word-count warnings on THEORY.md and README.md. That checker does not test mathematics.

`python3 -m pytest -q tools`, after `numpy`, `scipy`, and `sympy` were installed in the environment: 175 passed, 1 skipped, in 250 seconds. The skip is `tools/test_lean.py::test_lean_build_if_available`, because `lake` is not installed. `lake build` was not run. The pass is the repository's own scripts, including the numerical checks those scripts contain. It is not an independent proof, and it does not cover the representation gap in §3.1.

---

## 5. Bottom line

Proved today, and honestly claimable as mathematics:

- A posited additive cost, minimized under explicit restrictions, gives a list of standard or elementary consequences: a single-letter or information-bottleneck lower bound on loss (CT1, CT4's slope), Blackwell monotonicity of staleness (CT8), a Topkis comparison for check effort and, with sensing fixed and ruin slack, for layer count (CT10, CT20(ii)), revealed-preference monotonicity of spend (CT33), the McMillan degree of a linear-Gaussian filter as a cap on store dimension (CT21, known spectral factorization), homogeneity and cost shares when the feasible set does not depend on prices (CT24), and a Lundberg certificate at the slack end (the part of CT22 Lean actually checks).
- Given that same posited \(J\), a log-linear Wrightian map, and weak mutation on a named graph, the stationary excess on a quadratic well is \(d/(2\beta)\). That is R1. It is prior art applied to \(J\). The drifting sum R2 is bookkeeping under a long extra list.
- Finite-menu fragments of CT33, CT20, CT10, CT34(i)–(iii), the CT4 slope abstractly, and the slack half of CT22 are machine-checked, with no `sorry`. The information bound, the Gaussian constant, the layer theory, the selection theorem, and the hypothesis are not.

Not claimable at Shannon's standard:

- \(J\) is not derived. The upstream chain "persistence axioms \(\Rightarrow\) this \(J\) \(\Rightarrow\) excess \(d/(2\beta)\)" stops at the first arrow. The second arrow is conditional on A2-L and does not apply the axiom "stay solvent" until someone shows that solvency selects expected-cost \(J\) rather than Theorem L, Kelly growth, or a lineage mixture. §3.1 is the argument that the first arrow is likely false, and that a Debreu-plus-Cauchy lemma would only rename the assumptions.
- There is no matching achievability and converse for the cost that includes a holding price and a read price, and none for layers or for ruin.
- The structural theorems that make the theory recognizable (layers matched to the world's time scales, a rhythm counts two, geometric stacks, the temperature as a law of organizations) are true inside plants, false in nearby plants the same files already compute, or forced by dimensional analysis.

A Shannon-grade claim would need, at minimum, a representation that is actually unique, or an honest retreat from uniqueness together with one matching converse-and-construction for a stated class. The representation is the piece that makes the selection note and the Master Theorem into one chain. On the evidence in the tree, that piece is not available, and the obstructions are the theory's own alternative objectives.

---

## 6. Beyond Shannon: universality

Shannon's standard is the floor. Universality would be a theorem whose hypotheses are a process class, with the same conclusion for every process in the class, plus a representation that forces the objective, plus converses that do not pick the plant because the filter is known. The tree is mostly the other kind of result: a sharp calculation in a plant where the filter is a textbook.

### (i) Which theorems are class statements

Already a class statement, and the class is written down:

- CT33. Any nonempty design set on which \(J=S+wE\) and the set does not depend on \(w\). Any loss, any world. Error does not rise and spend does not fall as \(w\) rises. This is revealed preference. It survives a change of plant. It says nothing about layers. Binding ruin is a counterexample in the same file, so the class is not "any persisting system".
- CT8–CT10. Stationary Markov, arbitrary loss, renewal checks. CT8's garbling step is Blackwell's theorem (doi 10.1214/aoms/1177729032). The MA(2) counterexample shows the Markov hypothesis is doing the work.
- CT1. Stationary ergodic and exogenous, single-letter \(D\). Every process with a marginal in that class. Not every process the design theorems use.
- CT20(ii), sensing fixed, nested classes, ruin slack. Topkis (doi 10.1287/opre.26.2.305) and Milgrom and Shannon (doi 10.2307/2951479). The "any world" phrase in the main text is true for this comparison and only for this comparison.
- CT24. Any price-weighted sum with a price-independent feasible set. Euler's theorem. The content about organizations is the hypothesis that their feasible set is price-independent.
- CT18. One diffusive scale. Buckingham's theorem: the hazard is \(F(z)/\tau\) because \(z\) is the only dimensionless group. Universal inside that dimensional hypothesis, and empty outside it. The file lists the exits (bias, jumps, long memory, partial resets).

Plant statements, where a change of plant changes the conclusion, and a counter-plant is already computed:

- CT21, N60, interlacing. Linear-Gaussian, squared error. Real first-order stores on a rhythm are not counted by the increment formula (KEYSTONE_NOTE.md:46). One random walk, the scale-free Gaussian process, needs at most one layer (L1). A joint reset of a sum can beat a specialized stack (LAYER_LIFETIME.md:71).
- CT4's constant. One AR(1), one loss, one unit system.
- CT7. One random walk, no feedback.
- CT12. Exact reads, hold-last-value, power-law increments.
- R1–R2. Named Markov chains on designs, not a definition of selection.

A universal layer theorem that is plausible is an upper bound, not a formula. If a layer is one state of a causal realization, a sufficient statistic of the predictive state is always enough, and the causal-state construction of Crutchfield and Young (doi 10.1103/PhysRevLett.63.105) is the general object. The bound "you never need more states than a sufficient statistic" is close to a definition. The bound "the number worth buying is the number of spectral modes whose marginal mean-square contribution exceeds \(h/w\)" is Model S plus convexity, and it is already false for complex poles. CX4 is the conjecture that layers are the predictive-state components worth their upkeep. The upper bound is a short argument once "layer" is defined as a state. The count is likely false as a formula outside squared-error linear-Gaussian models. Difficulty of the upper bound: short. Difficulty of a universal count: the claim is the wrong shape.

### (ii) A model-independent derivation of \(J\)

The full argument is §3.1. The universality reading is the same fact, stated for a class: there is no representation in the sense of von Neumann–Morgenstern, Cox (doi 10.1119/1.1990764), or Shannon/Faddeev that takes "persisting adaptive system" as the structure and returns this \(J\) on that class.

Cox forces a probability. vNM forces an expected utility of lotteries, after preference axioms. Shannon forces the information measure, after the grouping axiom. Debreu forces an additive utility after separability. Cauchy forces linearity after concatenation. Landauer, Still, Sagawa–Ueda, and the causal rate-distortion theorem force inequalities or feasible sets. The sum \(\kappa I_{\mathrm{mem}}+hK+w\mathbb E[\ell]+A+L\) is what you get by assuming, in addition, that the coordinates are those five, that they are separable, that the first three are linear, that one currency exists, that the world is exogenous, and that solvency is imposed as a constraint on expected cost rather than as the objective. That package is a model. It is not forced by the four verbs.

Likely false: uniqueness from the four verbs. Likely true and not sufficient: the Debreu–Cauchy lemma under the extra axioms. The lemma should be written only as a fence around the hypothesis, so that later text cannot call \(J\) derived.

### (iii) Scale invariance and renormalization

Theorem S is homogeneity and a two-parameter family of exponents \((p,H)\). S4 is a proved failure of that homogeneity when two cost components scale differently. MATH_ATTACK.md's coarse-graining discussion concludes that a population obeying the objective is not, in general, an agent obeying the same objective. L4's geometric clocks are Jensen's inequality for a convex penalty in a shared-clock model (LAYERS.md:55–57), not a fixed point of a renormalization map. LAYERS1 P2, span invariance of spacing, is a SIM-FAIL (CLAIM_MAP G20). The store-model spacings in LAYERS.md §3 are roughly logarithmic and not equal.

An RG argument would be a coarse-graining on spectra and designs, a beta function for the price ratios, and an attractive fixed point whose design is layered. Wilson's renormalization-group paper (doi 10.1103/PhysRevB.4.3174) is the standard of that shape of theorem. Nothing in the tree is that argument. L1 is a counterexample to the slogan that would motivate it: the scale-free random walk is tracked by one store. A universal layered fixed point is likely false. Dimensionless groups determining the design once the world's shape is fixed are already proved, and the shape is a function (THEORY.md B.9, the paragraph on dimensionless groups). They do not produce layers.

### (iv) Which pieces are corollaries, and what is added

| Established law | What it already gives | What this \(J\) adds | Verdict |
|---|---|---|---|
| Rate-distortion and the data-rate theorem | CT1, S1's read term, the Gaussian sequential tradeoff | Several prices, a layer slot, a ruin cap, none of them in the classical bound | The information inequality is a corollary. The objective is not |
| Thermodynamics of computation | Floors under erasure and under nonpredictive dissipation; a learning-rate bound for a bipartite sensor | Nothing thermodynamic equals \(hK+w\mathbb E[\ell]+A+L\). Above the cell the repository says the floors are slack | A derivation of \(J\) from the second law is likely false. GENERAL_THEOREM.md §9 objection 1 already says the derivations do not use the second law except as a reason a maintenance cost exists |
| Large deviations | The Lundberg exponent | Theorem L, which disagrees with \(\arg\min J\) outside the noise-dominated limit | \(J\) is not the large-deviation objective. Claiming it is reintroduces the conflation in GENERAL_THEOREM.md:292 |
| Free energy and variational principles | A bound on surprise, in Friston's program, under hypotheses Biehl, Pollock and Kanai (doi 10.3390/e23030293) find do not hold in general | The repository explicitly does not identify \(J\) with free energy (SHANNON.md §6; GENERAL_THEOREM.md §8) | This is the wrong route. Importing that principle would narrow the hypotheses and would not prove the master equation |
| Internal model principle | Exact asymptotic regulation of a deterministic exosystem requires a copy of the generator (Francis and Wonham, doi 10.1016/0005-1098(76)90006-6) | A stochastic, approximate, persistence reading that does not give structure | P is weaker than the IMP on structure and is not a corollary of it. A stochastic IMP is marked as a conjecture in GENERAL_THEOREM.md §2 and is not attempted |

Genuinely added, once the corollaries are stripped: one ledger with free prices, a ruin constraint written next to it, a catalogue of where each classical inequality stops, and a set of short calculations (the \(\Phi\) threshold, the telling inequality, the temperature elasticities, the \(R^*\) comparison). The catalogue is valuable. It is not a new general law. THEORY.md §10 says the parts are known and the package is the claim. That sentence is the accurate one. CORE.md:7 is not.

### (v) Fully general converses

State them, then say what is likely.

**C-stat.** For every causal design in a stationary ergodic exogenous world, \(J\) is at least the causal rate-cost function at the lead, plus a holding price on predictive information, and a sequence of designs approaches the bound. The inequality half, relaxed and under S-A, is S1. Matching achievability with both prices is §3.2. I think the relaxation is not tight. A general stationary source with no Gaussian structure has a causal rate-distortion function that is usually not computable in closed form; existence of codes is not the same as a formula "from the statistics alone" that an experimenter can evaluate. Likely true as an existence bound for some classes. Likely false as a closed form.

**C-drift.** The same for stationary increments. Likely true for linear plants by §3.3. Open, and not a citation, for general processes.

**C-feedback.** With the world responding to the action, the exogenous converse is false: intervention can replace prediction. A true converse is a directed-information bound that treats "change the world" as a feasible purchase. Likely true in that form, following Touchette and Lloyd and the data-rate literature. Likely false as a bound that forces every solvent system to carry a model. CT2 and the bet-hedging counterexample already refuse the forced model inside exogenous worlds. CX2 is the responsive version of the same refusal.

**C-layer.** No design achieves distortion \(D\) with fewer than \(K_{\min}\) states. For a rational spectrum, \(K_{\min}\) at zero excess is the McMillan degree, which is CT21, and it is not the number worth buying at a finite price. For a general process there is no formula. The lifetime \(T^*\) does not provide one. A closed-form layer converse for arbitrary processes is likely false.

**C-ruin.** The cap raises the floor. A formula in the world's statistics alone is unlikely: the Lundberg root depends on the increment law of the reserve, which depends on the design. An existence statement for a sufficient certificate is CT22's \(B_{\min}\), and it is not tight.

**C-select.** Every process in which cheaper designs are favored ends within a stated distance of \(\arg\min J\), at a stated rate. Likely false. A2-M is the counter-hypothesis written in SELECTION_AXIOMS.md:28. Any true theorem has to assume a fitness map at least as strong as A2-L and a population process. The rate it then gives is a stationary gap, not a time.

The universal claim that survives this list is conditional and already half written: price-free comparative statics (CT33, CT20(ii) with sensing fixed), a single-letter information lower bound on a stationary exogenous world (CT1), and a degree cap for linear-Gaussian squared error (CT21). Everything that sounds like a law of adaptive organization at every scale is a further assumption, a plant calculation, or a hypothesis.
