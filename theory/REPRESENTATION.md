# When the additive cost is forced

*Sunday 22 November 2026, America/New_York. Branch `representation-2026-11-21`, draft PR, off `main` at `d1a6de4`. Written by one executor for Chad Mitchell. A self-check, not an independent review. Addresses the representation gap in `theory/MATH_COMPLETENESS_AUDIT.md` §3.1 (draft PR #151; that note is not on this branch). It does not change the Part 2 hypothesis sentence, and it does not edit `reviews/`, any preregistration, or any hash or locked file.*

*Theorems R1 and R2 below are this note's names. CLAIM_MAP section R is already the selection note (`theory/SELECTION_AXIOMS.md`, rows R1–R3). These two theorems are indexed as V1 and V2.*

## 0. Bottom line

The master equation

\[
J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L,
\]

subject to \(P(\mathrm{ruin})\le\varepsilon_r\), is not forced by "store, predict, act, stay solvent." Those four demands constrain a feasible set. They do not choose a functional on it. THEORY §3 already says the equation is the statement of the problem, not a theorem. This note does not withdraw that sentence. A weaker price-free candidate, Hypothesis F in §7, is stated as a hypothesis to test and is not a conclusion.

What is true is narrower, and it is a theorem.

**Theorem R1 (sufficiency).** Under the seven axioms in §1, every continuous cost that represents the preorder equals

\[
C=a\bigl(\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L\bigr)+b
\]

with one \(a>0\), one real \(b\), and prices \(\kappa,h,w\ge 0\) (and likewise the prices inside \(A\) and \(L\), on any coordinate that concatenates). A coordinate that is not essential has price zero and drops out.

**The affine freedom, stated carefully.** \(C=aJ+b\) with \(a>0\):

- preserves the argmin on any menu that does not depend on the numerical value of the cost;
- preserves the absolute excess \(d/(2\beta)\) only if the scale \(a\) is fixed, when \(\beta\) is held fixed as the selection slope on a named numerical cost;
- does not preserve the constrained argmin when the reserve pays the numerical cost, and does not preserve the fractional excess \((\mathbb{E}[J]-J^\star)/J^\star\), unless the zero is fixed as well.

A strictly increasing transform that is not affine still preserves the argmin on a fixed menu. It does not preserve \(d/(2\beta)\). Ordinal uniqueness would support "they minimize." It does not support the number.

**Theorem R2 (obstructions).** Drop any one of the seven axioms and the form, or its argmin, fails on a functional already in this repository. The four verbs are not a substitute for the list.

The pieces of R1 are known theorems applied to this coordinate list (Debreu, a monotone Cauchy equation, von Neumann–Morgenstern, Faddeev's axioms as stated by Aczél, Forte and Ng). The packaging is the claim. It is not a derivation of \(J\) from persistence, and it is not the missing arrow the audit called U.

## 1. The axioms

Each axiom is an assumption. None of them is a restatement of persistence.

**A1. Continuous complete preorder.** On the set of designs, or on the resource vectors defined below, the decision maker has a complete, transitive, continuous preorder \(\succeq\). Continuity is part of the axiom. Completeness alone does not give a real-valued cost: a lexicographic preorder is complete and has none. This repository does not compute a lexicographic design. The interacting-parties witness that no single cost ranks the joint designs is F1, in R2.

**A2. Expected cost under risk.** Preferences over lotteries of currency outcomes satisfy the von Neumann–Morgenstern axioms: completeness, transitivity, continuity, and independence (von Neumann and Morgenstern, *Theory of Games and Economic Behavior*, 60th Anniversary Commemorative Edition, doi 10.1515/9781400829460; Crossref returns this edition, 2007, not a 1944 record). The von Neumann–Morgenstern index is affine in the currency loss. That is risk neutrality in the one currency of A4. The ranking of risky designs is then the ranking by expected currency cost. Solvency is a constraint on the feasible set, \(P(\mathrm{ruin})\le\varepsilon_r\), not a term in the objective and not a replacement of the objective by a tail exponent or a growth rate.

Von Neumann–Morgenstern alone gives an expected utility, unique up to a positive affine transformation. It does not give expected cost. Logarithmic utility is a von Neumann–Morgenstern index, and it is Kelly's criterion, which R2 separates from expected cost.

**A3. Separability across independent sub-activities.** A design's resource vector lies in a product \(X=\prod_{i=1}^{n}X_i\) with \(n\ge 3\), each \(X_i\) a connected separable space (an interval of reals), and at least three coordinates essential. The preorder is preferentially independent: for every subset of coordinates, the ranking of two values of that subset does not depend on the fixed values of the others. This is Debreu's hypothesis, not a consequence of storing and acting.

**A4. One currency.** The coordinates are commensurate: they are paid in one unit, so the sum Debreu returns is the book's cost and not a vector of incomparable objectives. Theorem S (Lemma B12) uses the strong form of this, homogeneity of degree 1 in that one unit. S4 is the failure of the strong form.

**A5. Concatenation.** Two concatenations, both Cauchy equations.

- *Over time.* The cost of running the same design on successive durations \(t\) and \(s\) is the sum of the costs. There is no fixed charge per interval.
- *Over independent copies.* The cost of two independent parallel copies is the sum of the costs, in each extensive coordinate that is priced (information, layer count, expected loss, and whichever acquisition or link coordinate is the one that adds). There is no capacity ceiling on that coordinate.

**A6. Shannon information, in nats.** The memory coordinate is an information measure of a finite probability law, continuous and symmetric, and it satisfies Faddeev's grouping axiom as stated by Aczél, Forte and Ng (doi 10.2307/1426210). The measure is then Shannon entropy, unique up to a positive constant (Csiszár, doi 10.3390/e10030261, surveys the axiomatic characterizations). The constant is the base of the logarithm. This note fixes natural logarithms, so the unit is nats, and the constant is absorbed into \(\kappa\). Shannon's 1948 paper is cited as the IEEE reprint doi 10.1109/9780470544242.ch1, which is the reprint Crossref returns, not a record of the 1948 issue.

Faddeev's axioms fix the entropy once the object is an information measure of a probability law. They do not choose which mutual information is the coordinate. A6 includes the choice: the coordinate is the gross stock \(I_{\mathrm{mem}}=I(M_t;X^t)\), in nats. Predictive information, directed information, and \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\) are different functionals. The repository uses all four (THEORY notation table; `theory/SHANNON_2026-11-21.md`; `theory/THEOREMS.md` T6).

**A7. Exogenous world.** The law of the world does not depend on the design. The resource vector and the loss lottery are functions of the design alone, against that fixed law. Effort spent changing the world's drift is not one of the coordinates. Every proved theorem in THEORY already sets that effort to zero (the open lever, CX2, CL11).

## 2. Two lemmas used in the proof

**Lemma C (monotone Cauchy).** Let \(f:(0,\infty)\to\mathbb{R}\) satisfy \(f(x+y)=f(x)+f(y)\) and be monotone. Then \(f(x)=x\,f(1)\).

*Proof.* Induction gives \(f(nx)=nf(x)\) and \(f(x)=nf(x/n)\), so \(f(q)=q\,f(1)\) for every positive rational \(q\). Let \(x>0\) and let rationals \(q_k\uparrow x\) and \(r_k\downarrow x\). If \(f\) is nondecreasing, \(f(q_k)\le f(x)\le f(r_k)\). Both ends converge to \(x\,f(1)\), so \(f(x)=x\,f(1)\). If \(f\) is nonincreasing, \(-f\) is nondecreasing and additive, and the same conclusion holds. □

No continuity axiom beyond monotonicity is used. A discontinuous additive function that is not of this form requires the axiom of choice and is not monotone. It is excluded here.

**Lemma M (signs).** If \(f(z)=pz\) on \([0,\infty)\) and \(f\) is nondecreasing, then \(p\ge 0\). If the coordinate is not essential, the preorder does not depend on it, so \(p=0\).

## 3. Theorem R1 (sufficiency)

**Theorem R1.** Assume A1–A7, and assume at least three resource coordinates are essential. Then any continuous cost representing \(\succeq\) has the form

\[
C=a\bigl(\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L\bigr)+b,
\]

where \(a>0\), \(b\in\mathbb{R}\), the prices \(\kappa,h,w\) are nonnegative, and \(A\) and \(L\) are the Debreu components of the acquisition and link coordinates. On any such coordinate that satisfies A5, that component is linear in the coordinate with a nonnegative price. A coordinate that is not essential has price zero.

The ruin constraint is not produced by the representation. It is the feasibility restriction in A2.

*Proof.*

1. *The criterion is an expectation.* By A7 the world law is fixed, so each design determines a lottery over currency outcomes and a resource vector. By A2 the von Neumann–Morgenstern theorem supplies an expected utility of that lottery, and risk neutrality makes the utility the currency loss. The ranking is expected currency cost. The only freedom at this step is a positive affine regraduation of the currency unit.

2. *The expectation adds across coordinates.* Apply A1 and A3. Debreu's theorem (the essay "Topological methods in cardinal utility theory," cited here as the Crossref reprint doi 10.1017/ccol052123736x.010; the year field came back empty, and the title and author match the essay) gives continuous functions \(f_i\) on the factors such that one vector is preferred to another if and only if \(\sum_i f_i\) is smaller as a cost, and

   \[
   f_i\;\mapsto\;a f_i+b_i,\qquad a>0,
   \]

   is the only freedom. The hypothesis \(n\ge 3\) is Debreu's. Preferential independence of two coordinates is not enough for an additive representation. The missing ingredient in the two-coordinate case is the Thomsen condition on tradeoffs. This note does not assume it, and R1 is not claimed when fewer than three coordinates are essential. A two-term problem such as CT12 is inside the written master equation by specification of those two terms. It is not an application of Debreu's \(n\ge 3\) theorem.

3. *Each concatenating coordinate is linear.* Fix an essential coordinate \(z\) that satisfies A5, and hold the others fixed. Additivity over independent copies is \(f(z_1+z_2)=f(z_1)+f(z_2)\) up to a constant that does not depend on \(z\) (the \(b_i\) of step 2). Additivity over time, at a fixed rate, forces the objective to be a rate: the cost of a duration is proportional to the duration, so there is no fixed charge in the rate. Lemma C gives \(f(z)=pz\). Lemma M gives \(p\ge 0\). Applied to the memory stock, the layer count, and the expected loss, the prices are \(\kappa\), \(h\), and \(w\).

4. *The memory coordinate is Shannon's, in nats.* By A6 the memory coordinate is Shannon mutual information of the memory and the world's past. The positive constant in the entropy uniqueness is absorbed into \(\kappa\). A change of base rescales \(\kappa\) and does not change the argmin on a fixed menu.

5. *Acquisition and links.* The same two steps apply to any acquisition or link coordinate that concatenates: its Debreu component is linear in that coordinate with a nonnegative price, and the sum of those terms is what the master equation writes as \(A+L\). A pricing that does not concatenate in its displayed coordinate is not forced. The per-precision price \(c'\,r^{-\theta}\) (Lemma B2) is a function of precision, not a linear function of the precision coordinate. It can still be a rate, linear in duration at fixed precision. R1 does not choose it. Which of the three pricings of \(A\) a system pays is V4, and it is open.

6. *One scale, one constant.* The currency regraduation of step 1 and Debreu's common scale are the same \(a\), because the cost is already the von Neumann–Morgenstern index of the currency loss. The constants \(b_i\) sum to one \(b\). They are not a second, independent rescaling. □

**Nonnegative prices are the monotone case.** Nothing in A1–A7 stops a coordinate from being a good. If more of it is worse, Lemma M gives a nonnegative price. The master equation's prices are nonnegative by that monotonicity, which is part of how the preorder is pointed, not a theorem about physics. Landauer (doi 10.1147/rd.53.0183) and Barato, Hartich and Seifert (doi 10.1088/1367-2630/16/10/103024) are floors under a physical price. They are inequalities. They do not produce the sum. Sagawa and Ueda (doi 10.1103/PhysRevLett.102.250602; erratum doi 10.1103/PhysRevLett.106.189901) bound measurement work and erasure work together. Stacking \(\kappa I_{\mathrm{mem}}\) and a second thermodynamic price on directed information double-counts that bound. `theory/SHANNON_2026-11-21.md` already refuses the stacking. R1 does not restore it. The prices here are accounting prices in one currency. A physical floor is a separate, optional, lower bound on a price.

## 4. What \(aJ+b\) preserves

Let \(C=aJ+b\) with \(a>0\), and let the menu be fixed, independent of the numerical cost.

**Argmin.** \(C(\mathcal{D}_1)\le C(\mathcal{D}_2)\) if and only if \(J(\mathcal{D}_1)\le J(\mathcal{D}_2)\). The argmin is the same set. The additive constant \(b\) does not move it. The scale \(a\) does not move it. Any strictly increasing function of \(J\), affine or not, has the same argmin on that menu.

**Absolute excess.** Under A2-L of `theory/SELECTION_AXIOMS.md`, Malthusian fitness is \(m=m_0-\alpha C\) and the stationary weight on the haploid Moran chain is \(\pi\propto e^{-\beta C}\) with \(\beta=\alpha(N-1)\) (Theorem SA1; the weight is Sella and Hirsh 2005, doi 10.1073/pnas.0501865102). On a nondegenerate quadratic well in \(d\) whitened coordinates, Theorem SA1b gives

\[
\mathbb{E}[C]-C^\star=\frac{d}{2\beta}.
\]

Write \(C=aJ+b\). Then \(C-C^\star=a(J-J^\star)\), so

\[
\mathbb{E}[J]-J^\star=\frac{d}{2a\beta}=\frac{d}{2\beta_J},\qquad \beta_J=a\beta.
\]

The formula "excess \(=d/(2\beta)\)" is the excess of whichever numerical cost A2-L is applied to, with \(\beta\) the slope on that cost. If \(\beta\) is held fixed and the cost is replaced by \(aJ+b\), the excess of the new cost is \(a\) times the excess of \(J\). That equals \(d/(2\beta)\) if and only if \(a=1\). The constant \(b\) does not appear in \(\mathbb{E}[C]-C^\star\). Fixing the zero is not required for the absolute excess. Fixing the scale is.

If instead \(\beta\) is refit to the new unit, so that the exponent \(-\beta_{\mathrm{old}}J\) is rewritten as \(-\beta_{\mathrm{new}}C\), then \(\beta_{\mathrm{new}}=\beta_{\mathrm{old}}/a\) and the excess of \(C\) is again \(d/(2\beta_{\mathrm{new}})\). The number previously quoted for \(J\) is recovered only at \(a=1\). Refitting \(\beta\) changes the number. It does not cancel the need to name the unit.

**Fractional excess.** Corollary SA1c uses \((\mathbb{E}[J]-J^\star)/J^\star\), and the qualification band is a fractional gap. With \(C^\star=aJ^\star+b\),

\[
\frac{\mathbb{E}[C]-C^\star}{C^\star}=\frac{a\,(\mathbb{E}[J]-J^\star)}{aJ^\star+b}.
\]

Pure rescaling (\(b=0\)) leaves the fraction unchanged. A nonzero \(b\) changes it. The absolute excess and the fractional excess do not fix the same part of the affine freedom. The chain from this representation to the number \(d/(2\beta)\), and to the fractional band, needs the scale fixed. The fractional band needs the zero fixed as well. A2-M, monotone copying without the log-linear map, does not give \(d/(2\beta)\) even when the scale is fixed. `theory/SELECTION_AXIOMS.md` already says so.

**When the menu depends on the numerical cost.** The Lundberg certificate in CT22 constrains \(m=y-C\). Replacing \(J\) by \(aJ+b\) changes the margin, the exponent, and the feasible set. The constrained argmin is preserved only for the scale and the zero that match the reserve's currency. Section 4's first bullet is for a menu that does not move with the cost. CT22's menu is not that menu.

The check of the absolute and fractional arithmetic is `theory/representation_checks/binding_multiplier.py` (the affine block).

## 5. Theorem R2 (obstructions)

**Theorem R2.** For each axiom in §1, the repository already contains an explicit functional, consistent with storing, predicting, acting, and staying solvent, on which the conclusion of R1 fails. The functional violates that axiom. One witness (Still's dissipation) also violates separability, and the note says so. Therefore no axiom on the list is idle, and the four verbs do not force \(J\).

"Fails" means: the argmin differs from the argmin of \(J\), or the functional is not a nonnegative linear combination of \((I_{\mathrm{mem}},K,\mathbb{E}[\ell])\) plus additive acquisition and link terms, or there is no minimizer. Each witness is identified below. This is not a claim that no other axiom package, incomparable with A1–A7, could force the same sum. That is open (V4). A counterexample isolates an axiom only to the extent the note says it does.

**A1 dropped.** F1 in `theory/COADAPTATION.md`: matching pennies, costs in \(\{0,1\}\), equal clocks. The joint chain is uniform at every selection strength, and each party's regret stays \(1/2\). There is no potential, so there is no complete ranking of joint designs by one additive \(J\) that the chain minimizes. A single decision maker's preorder can still be complete. The obstruction is to reading "selected parties stay in some arrangement" as the argmin of one \(J\).

**A2 dropped.** Two witnesses, already computed.

- *Lundberg, Lemma B9.* Maximizing the diffusion exponent \(\theta=2m/s^2\) is a solvency criterion. On the published point (\(y=1\), \(c=0.05\), \(w=\sigma=1\), \(s_0=0.3\)) the survival-optimal interval is \(\tau_S=0.2362\) and the expected-cost interval is \(\tau_E=0.3162\). They are not the same design. The agreement when the reserve's own noise dominates is a limit inside this model, not an identity of the two objectives (THEORY, the correction to Theorem L). `theory/representation_checks/binding_multiplier.py` recomputes both endpoints.
- *Kelly growth, and the lineage mixture.* Kelly 1956 (doi 10.1002/j.1538-7305.1956.tb03809.x) maximizes expected log growth. That is a von Neumann–Morgenstern criterion with logarithmic utility, so dropping risk neutrality while keeping A2's other clauses is enough. CT42 in `theory/DYNAMICS.md`: with a shared shock of probability \(0.05\), the lineage optimum puts weight \(q^\star=0.26\) on the robust design, and the per-unit expectation picks the pure lean design (mean factor \(1.235\) against \(1.043\)). Donaldson-Matasci, Bergstrom and Lachmann (doi 10.1111/j.1600-0706.2009.17781.x) are the fitness-value form of the same growth criterion, already used as S5 in `theory/GENERAL_THEOREM.md`. A mixture is not the argmin of a linear expected cost on a simplex.

What still holds if one keeps expected cost and only changes the ruin rule: CT33, on any menu that does not depend on the stake. The survival objective itself is not of the form \(S+wE\), and CT33 is not a theorem about \(\arg\max\theta\).

**A3 dropped.** Non-separable layer costs, both already proved.

- CT34(iv): four units with a shared driver, scored as if their upkeeps added, miss the pooling gain. Per-unit error \(0.0905\) locally against \(0.0410\) pooled at correlation \(1\) (`scope_checks.py` §2). The sum of the standalone costs is not the joint cost. The proved direction of CT34(ii) is the companion: when what the parent passes down depends on the parent's design, the parent's objective is \(F(x)+J_T^\star(\theta(x))\), a value function, not \(F(x)\) plus a constant upkeep \(h\). The converse, "only if," is not proved (THEORY states the flat-direction obstruction and does not give it a topology). R2 uses only the proved direction.
- CT36: the joint value of two estimates depends on their mutual correlation \(r_{LS}\). It is not the sum of the separate values. The fixed-rate excess is negative at \(r_L=r_S=0.5\), \(r_{LS}=0.8\) (excess \(-0.22\)), and the sign condition for a positive excess is stated in THEORY B.11. Priced reading makes net worth superadditive in \(119\) of \(1500\) worlds in that check. A representation that forces \(hK\) as a sum of per-layer upkeeps is false for those designs.

Partial minimization still writes the parent's problem as \(F+J_T^\star\). That identity does not need separability of the layers. CT33 still applies to any problem that, after the partial minimization, has the form \(S+wE\) on a stake-independent menu. The five-term form with a constant \(h\) does not.

**A4 dropped.** Lemma B12, S4, in `theory/GENERAL_THEOREM.md`: a fixed per-check cost plus a size-proportional cost. The local exponent of the optimal interval slides from \(-1\) to \(-1/2\) as size runs from \(1\) to \(10^6\) (`c5c`). One homogeneous law in one currency does not describe the path. A real sum of the two components still exists. What fails is A4's strong form, the form Theorem S uses. CT24's share identity also needs one price vector and a feasible set that does not depend on it. S4 is outside that hypothesis.

**A5 dropped.** The same S4 example is a failure of concatenation: a fixed charge means the cost of size \(n\) is not \(n\) times the cost of size \(1\), so Lemma C does not apply, and the optimum is not the optimum of a linear rate. Separately, a hard information capacity is not a linear penalty. Sims (doi 10.1016/S0304-3932(03)00029-1) uses a capacity; the linear penalty is the dual problem, not the same primal. THEORY §10 cites Sims. This repository does not recompute his model. The computed witness for dropping concatenation is S4.

**A6 dropped.** The clean witness is a different information coordinate, not a different entropy formula. Directed information is the read currency of S1. Tatikonda and Mitter (doi 10.1109/tac.2004.831187) and Tatikonda, Sahai and Mitter (doi 10.1109/TAC.2004.834430) are the control and rate-distortion sources. A cost \(c\cdot r+wD\) ranks designs by the flow. A cost \(\kappa I_{\mathrm{mem}}+w\,\mathbb{E}[\ell]\) ranks them by the stock. They are separable expected-cost criteria in one currency, on an exogenous world, and each coordinate concatenates on its own terms. They are not the same functional. With both prices positive, the best one-layer design on the reported grid sits above the relaxation floor that uses both coordinates (`theory/SHANNON_2026-11-21.md`: efficiency \(0.9574\), gap \(4.26\%\)). Faddeev uniqueness fixes the entropy once the object is an information measure. It does not choose the stock over the flow.

Still, Sivak, Bell and Crooks (doi 10.1103/PhysRevLett.109.120604) are the repository's other information cost, and they are not a pure ablation of A6. Under their hypotheses (driven, no feedback, Markov, a heat bath), dissipation per step equals \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\) in units \(kT=1\). `theory/THEOREMS.md` T6 records the equality and a two-state enumeration to 6 decimals. That functional depends on how predictive the memory is. It is not \(\kappa I_{\mathrm{mem}}\). Separability in \((I_{\mathrm{mem}},\mathbb{E}[\ell])\) fails on it, because \(I_{\mathrm{pred}}\) couples the memory to the prediction. The witness drops A6 and A3 together. It is still a cost of memory, already in the tree, that R1 does not produce.

**A7 dropped.** F3 in `theory/COADAPTATION.md`: the world copies the design with gain \(g>1\). Every party cost is nonnegative, and the potential is unbounded below, so there is no minimizer. The coupled system runs away. Touchette and Lloyd (doi 10.1103/PhysRevLett.84.1156) bound how much feedback can reduce entropy by the information gathered, which is the same structural point: the agent can buy persistence by changing the world, and the cost of that intervention is a coordinate \(J\) does not have. CX2 and CL11 stay open. A representation proved on an exogenous product stops at that boundary. The term list is incomplete on the other side, so it is not the unique cost of persistence.

**What R2 does not say.** It does not say the four verbs are inconsistent with \(J\). Chance-constrained expected cost is one way to store, predict, act, and stay solvent. R2 says it is not the only way, and that the alternatives already written down in this repository do not share \(J\)'s argmin. The search for a derivation of this \(J\) from the four verbs alone is not open in the sense of a missing lemma. The obstructions are the theorems just cited.

## 6. The universal core

R1 fixes a price vector up to one common scale. Most of the theory's structural statements do not need the whole vector, and several do not need the five-term split. This section lists what holds for every cost in a named class, and what does not. No new inequality is proved here. Each line is the scope of a theorem already proved. The list is V3.

**Class B.** Any nonempty design set and any cost \(J(\mathcal{D};w)=S(\mathcal{D})+w\,E(\mathcal{D})\), with the set independent of the stake \(w\). \(S\) need not be linear, need not split into \(I_{\mathrm{mem}}\), \(K\), \(A\), and \(L\), and need not price Shannon information.

- **CT33.** Expected loss is nonincreasing in \(w\), judgment spend \(S\) is nondecreasing in \(w\), and \(J^\star\) is concave in \(w\) with slope \(E^\star\). Any loss, any world. Ties may be broken either way.
- The class excludes a binding ruin constraint. THEORY's counterexample (spend falls and error rises once the reserve pays \(J\)) is `scope_checks.py` §1b. Class B is not "any persisting system."

**Class L.** \(J(x;p)=\sum_i p_i\,\varphi_i(x)\) with price-free \(\varphi_i\ge 0\) and a feasible set that does not depend on the price vector \(p\). Every admissible price vector means every \(p\) in the nonnegative orthant, in this class.

- **CT24.** At a differentiable optimum, the share of term \(i\) equals the elasticity of \(J^\star\) in \(p_i\), and the shares sum to 1. \(J^\star\) is concave and homogeneous of degree 1. The envelope gives \(\partial J^\star/\partial p_i=\varphi_i(x^\star)\).
- **CT33** is the one-price case, with \(S\) the sum of the terms that do not carry \(w\).
- The numerical split \((\alpha-1):1\) is not in this class for free. It needs the single exact-read power-law tracker (CT12). With more terms, or with read noise, Euler still gives shares summing to 1 and does not give that ratio.
- A binding ruin constraint is a counterexample inside the same file: shares \(0.528\) and \(0.472\), elasticities \(0.584\) and \(0.563\), sum \(1.147\) (THEORY CT24).

**Class M, sensing fixed.** \(J=hK+w E_K\) with \(E_K\) nonincreasing, read rates not chosen, ruin slack or absent.

- **CT20(ii).** For every world and every loss, \(K^\star\) is nondecreasing in \(w/h\). For one layer whose error grows with the age of its reading, the read rate is nondecreasing in \(w/c\). The tools are Topkis (doi 10.1287/opre.26.2.305) and Milgrom and Shannon (doi 10.2307/2951479).
- This is every positive price ratio \(w/h\), not every functional. With read rates chosen, \(K^\star\) can fall (THEORY B.9). With ruin binding, spend can fall.

**Price-free structure, no price vector at all.**

- **CT8.** In a stationary Markov world, any loss, renewal checks: staleness is a garbling, so more frequent checking is better as information. The step is Blackwell's theorem (doi 10.1214/aoms/1177729032). It is false for non-Markov observations. The prices do not enter the monotonicity.
- **CT1 and S1.** A lower bound on loss given an information resource, for an exogenous stationary design. The bound is not a priced minimizer. It holds before any particular positive price is chosen. The priced minimum of \(\kappa I+c\,r+w D\) does depend on the prices, and S1's relaxation is not known to be tight when both prices are positive.

**What does not survive every admissible price vector, even inside Class L.**

- The argmin itself: layer count, read interval, and the numerical shares beyond the Euler identity all depend on the price ratios.
- **CT22.** The binding multiplier is a fact about one scalar diffusion path (THEORY Appendix B.9). It is not a fact about every price vector, and it is not a fact about a general design set.
- **The number \(d/(2\beta)\).** It needs A2-L and a fixed scale (§4). It is not a theorem about every price vector. Rescaling the currency rescales the excess unless \(\beta\) is rescaled with it.
- **CT7's floor** \(J^\star=\sigma\sqrt{2kT\cdot w}\) prices nats acquired in one random-walk model. It is not the master equation evaluated at an arbitrary price vector (`theory/MASTER_EQUATION.md` already marks the match partial).

The core that is actually universal, inside the hypotheses just named, is CT33 for every cost in Class B, CT24 for every price vector in Class L, CT20(ii) for every price ratio with sensing fixed and ruin slack, and the information lower bound CT1 on a stationary exogenous world. Everything beyond that list is a further restriction, a plant calculation, or the hypothesis.

## 7. A price-free frontier, as a hypothesis

*Added 22 November 2026 from a note of Chad's dated 21 November, 11:20 PM ET. This section treats that note as a hypothesis to test. It is not a conclusion, and it does not replace the Part 2 hypothesis sentence.*

The scalar cost is a special case of something weaker. The candidate general form is price-free: a selected design lies on the efficient frontier of five bads, given the world's pattern of change and the floors already proved. Additive \(J\) is what you get back when one currency exists and the costs separate and are linear. The geometry is prior art. The five names are a proposal.

### 7.1 What is already in the repository

Grep before any of this was called new. It is not new.

- `theory/SHANNON_2026-11-21.md` Theorem S2 defines \(\mathcal{F}_W=\{(I,r,K,D)\}\) with no prices, and identifies \(J^\star(p)=\inf\langle p,z\rangle\) with the support function of that set. S2 says this recovers the free-disposal hull of the Pareto face of the convex hull, not the hull itself and not dominated points.
- Theorem S3, same note: a minimizer at strictly positive prices is undominated; if the feasible set is convex, every undominated point minimizes a linear cost for some nonzero \(p\ge 0\). The proof named there is the supporting hyperplane.
- The same note already says the price-free content of the hypothesis is "selected systems sit on their world's frontier," and it already credits Farrell (doi 10.2307/2343100), Debreu's coefficient of resource utilization (doi 10.2307/1906814, Econometrica 19:273, 1951; resolved on Crossref on 22 November 2026), and Shoval et al. (doi 10.1126/science.1217405).
- `theory/PRICE_FREE_2026-11-21.md` already sorts the scalar theorems into price-free, price-ratio, and absolute-price. That sort assumes a scalar \(J\) whose unit is unknown. It does not drop the scalar.

Shoval, Sheftel, Shinar, Hart, Ramote, Mayo, Dekel, Kavanagh and Alon (2012; Crossref title "Evolutionary Trade-Offs, Pareto Optimality, and the Geometry of Phenotype Space") show that multi-objective optimality in trait space produces a low-dimensional front, and they read data as lying near one. Pareto optimality as evidence of tradeoffs in evolution is their result. It is not a GTAO theorem. Farrell's technical efficiency and Debreu's 1951 coefficient are the price-free efficiency facts S3 uses. Geoffrion (doi 10.1016/0022-247X(68)90201-1) names proper efficiency and ties it to strictly positive weights. Weighted-sum scalarization is that literature. None of it is claimed here as new.

What S2 does not do is put attention and ruin risk on the frontier as coordinates. Its vector is memory, reads, layer count, and distortion. Ruin is a cap that cuts the set (S3's own caveat: the cap need not keep the set convex). Attention, in THEORY §3, is one name for the currency, not a fifth bad. Chad's list is a different vector. The theorems below say what that change does to results the repository already has. They do not propose a new front in nature.

### 7.2 The frontier, under a partial order

Fix an exogenous world \(W\): its pattern of change, the read channel, and the lead. A design \(\mathcal{D}\) is scored by five bads, each to be made smaller:

\[
z(\mathcal{D};W)=\bigl(I_{\mathrm{mem}},\;\iota,\;e,\;a,\;\rho\bigr)\in\mathbb{R}^5.
\]

- \(I_{\mathrm{mem}}\): memory held. A6's Shannon stock is one choice. The partial order does not need it.
- \(\iota\): information bought. A read count or a directed-information rate. Not a price.
- \(e\): error. The single-letter floors are proved for an expected distortion. The order itself allows any loss index that is a bad.
- \(a\): attention spent, a nonnegative quantity. If attention is the unit in which the other four are already paid, it is not an independent coordinate, and the vector has collapsed toward a scalar. That collapse is the special case, not this form.
- \(\rho\): ruin risk. \(P(\mathrm{ruin})\), or the Lundberg bound \(e^{-\theta B}\). The master equation's constraint is the slice \(\rho\le\varepsilon_r\). Here \(\rho\) is traded off, not only capped.

Let \(Z(W)\) be the set of vectors of feasible designs. The physical floors (Landauer; Still, under that paper's hypotheses) and the information floors (CT1, S1, and the drifting flow floor PD1) are constraints that define \(Z(W)\). They are not summands.

**Assumptions used below, and nothing stronger.**

- **F-O.** The order is the product order: \(z\le z'\) coordinatewise. It is a partial order. Two feasible designs may be incomparable. There is no complete preorder, and no currency.
- **F-D.** Free disposal: if \(z\in Z(W)\) and \(z'\ge z\), then \(z'\in Z(W)\). Dominated waste is feasible. It is never efficient.
- **F-C.** \(Z(W)\) is nonempty and compact. Then a Pareto point exists: the minimizer of the sum of the five coordinates exists and is undominated. Compactness is the regularity. F3 in `theory/COADAPTATION.md` (the world copies the design with gain above 1, and the potential is unbounded below) is a case where no Pareto point exists. The hypothesis is silent there.

A point \(z^\star\in Z(W)\) is **Pareto efficient** when no \(z\in Z(W)\) has \(z\le z^\star\) and \(z\neq z^\star\). Write \(P(Z(W))\) for that set.

**Hypothesis F.** A strongly selected system in world \(W\) occupies a design whose score lies on \(P(Z(W))\), or in a band of it that a preregistration would have to set. This is weaker than minimizing additive \(J\). Theorem F1(i) below is the reason: every positive-price minimizer of \(J\) is on the frontier, and the converse is not free. Hypothesis F is not the Part 2 sentence, it does not rewrite it, and it is not tested. Status: **OPEN**.

### 7.3 What survives without prices

**Lemma F-A (the front is antitone).** Take any two coordinates and hold the other three fixed. If \(z\) and \(z'\) are both Pareto in that slice, the two free coordinates move in opposite directions: their differences multiply to a nonpositive number. *Proof.* If both differences were positive, one point would dominate the other. □

No price, no additivity, and no lattice. This is the definition of a two-objective front.

**Information floors survive, as constraints on \(Z(W)\).** CT1 and S1 say that \((\iota, e)\) and \((I_{\mathrm{mem}}, e)\) cannot fall below the single-letter or information-bottleneck curve of an exogenous stationary world. PD1a is the same statement for a drifting world with a density, in the flow coordinate. They do not use a price and they do not use additivity. They do not choose a point on the front. CT8 survives the same way: in a stationary Markov world with renewal checks, a staler reading is a garbling, so it cannot lower the best \(e\) at given other coordinates (Blackwell, doi 10.1214/aoms/1177729032). The Markov hypothesis is still required. The prices are not.

**Layers, split into what is dominance and what is a price.**

Survives, as dominance, and only under an extra monotonicity the five names do not give by themselves. An extra layer that does not cut \(e\) and that raises memory or attention, and that raises no other bad's opposite, is dominated. Under that monotonicity:

- One real pole, \(E_1=E_\infty\) (CT21 L1): every \(K\ge 2\) is dominated by \(K=1\) at the same error. Both \(K=0\) and \(K=1\) can sit on the front. The scalar statement "\(K^\star\in\{0,1\}\) for every \(w,h\)" is the priced version. The dominance of \(K\ge 2\) is the part that needs no price.
- At most the McMillan degree (L2's cap): stores beyond the degree do not cut \(e\) below \(E_\infty\). If they raise memory or attention, they are dominated. The cap is a property of the minimum-error end of the front.
- L3: a non-rational spectrum has \(E_K>E_\infty\) for every finite \(K\). No finite design is undominated at zero excess error. That needs no price. "\(K^\star(R)\to\infty\) as \(R\to\infty\)" needs the ratio \(R\).
- Interlacing describes the error-minimizing filter at full degree. It is a fact about that end of the front. It does not say the system sits there.

Needs a price ratio, and does not survive on the bare front:

- \(K^\star\) as a function of \(R=w E_\infty/h\), the threshold \(R^\star\), and the from-0 count \(K^\star_0(R)\) (N60, N64). The curve \(\varepsilon_K\) is a slice of the front. The count is a point picked by \(R\).
- "\(K=J\) once \(R\) is large enough."
- CT24's shares, the ratio \((\alpha-1):1\), and \(d/(2\beta)\). Shares need linear prices and Euler. The excess needs a scalar cardinal cost and A2-L.

If a layer raises none of the five bads, it is not dominated. The repository's \(h>0\) makes the layer a bad only inside the scalar cost. On this front that monotonicity is an assumption, not a consequence of the five names.

**CT33 and Master Theorem (ii), in the ordinal setting.**

Two different statements are easy to mix up.

The antitone property is Lemma F-A. On a slice in \((S, e)\), efficient points satisfy \((S-S')(e-e')\le 0\). Spend and error move against each other along the front. The same holds for \((K, e)\) when \(K\) is a bad. No stake is involved. This is what survives with no prices and no additivity.

The comparative static needs a parameter. Milgrom and Shannon (doi 10.2307/2951479) give monotone selection when the objective is quasisupermodular in the choice and has single crossing in the choice and the parameter. On a chain, quasisupermodularity is free, and single crossing is the whole condition. Topkis (doi 10.1287/opre.26.2.305) is the lattice form used for \(K\) in CT20(ii). For \(J=S+wE\), the difference between a higher-spend, lower-error design and its alternative is single-crossing in \(w\): once the costlier design wins, it keeps winning as \(w\) rises. That is why \(E^\star\) falls and \(S^\star\) rises, and why, with sensing fixed, \(K^\star\) rises in \(w/h\).

Single crossing uses the scalar form \(S+wE\). It does not need the five-term split inside \(S\). It does need a stake, or some other parameter that crosses. A pure Pareto front has no such parameter. A selection rule that picks an arbitrary efficient point as the world changes can move either way. So:

- Lemma F-A survives.
- CT33's sentence "as stakes rise, error falls and spend rises" survives for every objective with single crossing in \((design, w)\), including every cost in Class B. It does not survive a selection from \(P(Z)\) with no stake.
- Master Theorem (ii) survives as "efficient \(K\) is antitone in error" under the monotonicity above, and as a monotone selection in \(w/h\) only when the scalar \(hK+wE_K\) is back. With read rates chosen, layers can still fall as stakes rise. That counterexample is about the scalar problem (THEORY B.9). It remains a counterexample there. It is not a statement about the bare front.
- CT10, effort rising in \(w/c\), is the same split. The front in \((f, e)\) is antitone. The derivative in \(w\) needs \(w\).

**CT22 does not survive as a multiplier.** If \(\rho\) is a coordinate, the tradeoff is a slope of the front between ruin risk and the other bads. The identity \(\mu_s=-m'/\theta'\) is the Lagrange multiplier of a scalar \(J\) on a scalar path. It needs additivity of the margin \(m=y-J\) and the whole of the proof in THEORY B.9. What survives with no prices is Lemma F-A on the slice \((J, \rho)\), and only after a scalar \(J\) has already been chosen. Without that scalar there is no EOQ end and no survival end, only an antitone set of \((cost, risk)\) pairs.

### 7.4 When the front plus a scalarization is additive \(J\)

**Theorem F1 (scalarization; S3 on this vector).** Let \(Z\subset\mathbb{R}^5\) satisfy F-D.

(i) If \(p\gg 0\) and \(z^\star\) minimizes \(\langle p, z\rangle\) over \(Z\), then \(z^\star\) is Pareto. *Proof.* A point with \(z\le z^\star\) and \(z\neq z^\star\) would have a strictly smaller inner product. Convexity is not used. □

(ii) If \(Z\) is convex and \(z^\star\) is Pareto, then some \(p\ge 0\), \(p\neq 0\), has \(z^\star\) minimizing \(\langle p, z\rangle\). *Proof.* \(Z-z^\star\) is convex and does not meet the open negative orthant. A separating hyperplane has nonnegative normal \(p\neq 0\), and \(z^\star\) minimizes the inner product. This is the argument S3(ii) names, on a longer vector. □

The inner product is an additive linear cost in the five coordinates, with nonnegative prices, up to a constant that does not move the argmin. Prices on inessential coordinates may be zero. Strictly positive prices, in (i), are the case where every coordinate is charged, which is R1's essential-coordinate case. Geoffrion's theorem says proper efficiency, not mere Pareto, is the notion that matches strictly positive weights on a convex set. This note does not re-prove that characterization. (i) and (ii) are the directions it uses, and both are S3.

**What convexity is doing.** (ii) is the converse the hypothesis needs: front plus a linear scalarization, under convexity, is additive linear \(J\) for some nonnegative prices. One currency is the inner product. Separation of the costs is linearity in the five coordinates. R1's route was different and does not use convexity of \(Z\). R1 starts from a complete preorder, Debreu additivity, and concatenation, and it can produce nonlinear Debreu components if a coordinate does not concatenate. A supporting hyperplane produces linear prices and needs convexity of the image. Neither route is the other.

**What fails without convexity.** Pareto does not imply a weighted-sum minimum. Three points in \(\mathbb{R}^2\), the other coordinates fixed:

\[
A=(0,1),\qquad B=(1,0),\qquad C=(0.6,0.6).
\]

None dominates another, so each is Pareto in \(\{A,B,C\}\). For any \(p\ge 0\) not both zero, \(C\) is not a minimizer of \(\langle p,\cdot\rangle\). If \(p_1=0\), then \(B\) scores \(0\) and \(C\) scores \(0.6 p_2>0\). If \(p_2=0\), \(A\) wins the same way. If both are positive, \(\langle p, C\rangle\le\langle p, A\rangle\) and \(\langle p, C\rangle\le\langle p, B\rangle\) rearrange to \(p_1/p_2\le 2/3\) and \(p_2/p_1\le 2/3\), which cannot hold together. The check is `frontier_scalarization` in `theory/representation_checks/binding_multiplier.py`.

The mixture \(\tfrac12 A+\tfrac12 B=(0.5,0.5)\) dominates \(C\). If mixtures are feasible, \(C\) is not on the front at all, and (ii) has nothing to explain. The miss is the case where the image is nonconvex and \(C\) stays feasible. Linear scalarization then sees only the exposed face of the convex hull. S2 already says that \(J^\star\) recovers that face and does not recover the dent. A monotone nonlinear scalarization can still prefer \(C\). So "some scalarization of the front" is weaker than additive linear \(J\). Convexity of \(Z\), or of its free-disposal hull, is the condition that closes the gap.

The ruin cap can destroy the convexity (ii) needs. S3 says so, and gives no repair. A front cut by \(\rho\le\varepsilon_r\) need not satisfy (ii) even when the uncapped front does.

### 7.5 What is GTAO-specific, and what is not

Not specific, and not new: Pareto order, weighted sums, supporting hyperplanes, Farrell efficiency, Debreu's 1951 coefficient, Geoffrion's proper efficiency, Shoval et al. on evolutionary fronts, and S2–S3 as already written for \((I, r, K, D)\).

Specific to this repository, and already stated before this section: the feasible set is computed from the world's statistics and from the information floors, rather than fitted to a cloud of traits (SHANNON §6, the sentence on Shoval). The layer cap is the dominance fact in §7.3, in the linear-Gaussian plants where it is proved.

Specific to Chad's note, and still a hypothesis: the bads are these five, attention is a coordinate rather than the currency, and ruin risk is a coordinate rather than only a cap. Nothing in the tree shows that a selected system lies on that front. Hypothesis F stays **OPEN**. Additive \(J\) remains the special case in which a currency exists, the image is convex or the preorder separates and concatenates, and the prices are the supporting weights.

## 8. The scalar path is a different theorem

CT22's binding multiplier is not part of R1. R1 produces the objective. CT22 is a fact about minimizing that objective on one path. The proof is in THEORY Appendix B.9. It replaces the one-word appeal to KKT. The conditions stated there are strict convexity of \(J\), convexity of the variance rate \(s^2\) (which gives strict unimodality of \(\theta\), and therefore a convex feasible set), and constraint qualification \(\theta'\ne 0\) at the binding point. \(\theta\) itself is not concave on the whole domain. A reading that needs a concave certificate is stronger than what the path satisfies, and the scalar proof does not use it.

## 9. Status of the claims

| ID | What | Status |
|---|---|---|
| V1 | Theorem R1, sufficiency, under A1–A7, at least three essential coordinates | **PROVED (in-model)** |
| V2 | Theorem R2, each axiom dropped, a repository counterexample | **PROVED (in-model)** |
| V3 | Universal core: CT33 on Class B, CT24 on Class L, CT20(ii) with sensing fixed, CT1 as a bound | **PROVED (in-model)** |
| V4 | Which concatenating coordinate the acquisition price is linear in. Three pricings of \(A\) are in use. A1–A7 do not choose among them | **OPEN** |
| V5 | Hypothesis F: a selected design lies on the Pareto front of (memory held, information bought, error, attention, ruin risk), given the world and the floors. Additive \(J\) would be the priced convex special case. Not a replacement of the Part 2 sentence | **OPEN** |
| V6 | Theorem F1 and the survival list in §7: information floors and the antitone shape of the front need no prices; CT33 and CT20(ii) need a stake with single crossing; layer caps survive as dominance only under an extra monotonicity; weighted-sum equivalence needs convexity, and the three-point dent is the miss | **PROVED (in-model)** |

V1 is a theorem under axioms that are not themselves derived. Calling \(J\) derived from persistence would be a misreading of V1. V2 is the reason that misreading is false. V3 adds no inequality. V4 is the slot R1 deliberately leaves unspecified. V5 is a hypothesis, not a conclusion. V6 is S3 on a longer vector, plus a scope list. It is not a new existence theorem about systems.

## 10. Citations

Every DOI below was resolved on the Crossref API on 22 November 2026. A DOI is printed only when the returned title matches the work. The record is `theory/representation_checks/crossref.out`. Books and reprints are marked when Crossref did not return the original issue.

- Debreu, "Topological methods in cardinal utility theory," reprint doi 10.1017/ccol052123736x.010. Title and author match. The year field came back empty.
- von Neumann and Morgenstern, *Theory of Games and Economic Behavior*, 60th Anniversary Commemorative Edition, doi 10.1515/9781400829460 (2007).
- Aczél, Forte and Ng, "Why the Shannon and Hartley entropies are 'natural'," doi 10.2307/1426210 (1974).
- Csiszár, "Axiomatic Characterizations of Information Measures," doi 10.3390/e10030261 (2008).
- Shannon, "A Mathematical Theory of Communication," IEEE reprint doi 10.1109/9780470544242.ch1 (2009). Crossref returned no author list on this record.
- Still, Sivak, Bell and Crooks, doi 10.1103/PhysRevLett.109.120604 (2012).
- Landauer, doi 10.1147/rd.53.0183 (1961).
- Barato, Hartich and Seifert, doi 10.1088/1367-2630/16/10/103024 (2014).
- Sagawa and Ueda, doi 10.1103/PhysRevLett.102.250602 (2009); erratum doi 10.1103/PhysRevLett.106.189901 (2011).
- Touchette and Lloyd, doi 10.1103/PhysRevLett.84.1156 (2000).
- Kelly, doi 10.1002/j.1538-7305.1956.tb03809.x (1956).
- Donaldson-Matasci, Bergstrom and Lachmann, doi 10.1111/j.1600-0706.2009.17781.x (2010).
- Sims, doi 10.1016/S0304-3932(03)00029-1 (2003).
- Tatikonda and Mitter, doi 10.1109/tac.2004.831187 (2004).
- Tatikonda, Sahai and Mitter, doi 10.1109/TAC.2004.834430 (2004).
- Sella and Hirsh, doi 10.1073/pnas.0501865102 (2005).
- Topkis, doi 10.1287/opre.26.2.305 (1978).
- Milgrom and Shannon, doi 10.2307/2951479 (1994).
- Blackwell, doi 10.1214/aoms/1177729032 (1953).
- Farrell, "The Measurement of Productive Efficiency," doi 10.2307/2343100 (1957).
- Debreu, "The Coefficient of Resource Utilization," doi 10.2307/1906814 (1951).
- Shoval, Sheftel, Shinar, Hart, Ramote, Mayo, Dekel, Kavanagh and Alon, doi 10.1126/science.1217405 (2012). Crossref title: "Evolutionary Trade-Offs, Pareto Optimality, and the Geometry of Phenotype Space."
- Geoffrion, "Proper efficiency and the theory of vector maximization," doi 10.1016/0022-247X(68)90201-1 (1968).

Khinchin's *Mathematical Foundations of Information Theory* was not given a DOI. It is not cited. Faddeev's 1956 note was not given a DOI by the search that returned these records. His axiom is used only as stated by Aczél, Forte and Ng.

## 11. Checks

`theory/representation_checks/binding_multiplier.py`, run by `tools/test_representation_checks.py`. It checks the algebra in the CT22 proof (the sign of the numerator of \(\theta'\), the Sturm count on the published point, the multiplier identity, monotonicity, constraint qualification off \(\tau_S\)), the two obstructions used to show convexity and unimodality are doing work, the affine arithmetic of §4, and the three-point dent of §7.4 (Pareto, supported by no nonnegative weight, and dominated once mixtures are allowed). It does not re-derive CT34, CT36, CT42, F1, or F3. Those proofs stay where they are.

The Part 2 hypothesis sentence is unchanged and is not restated here.
