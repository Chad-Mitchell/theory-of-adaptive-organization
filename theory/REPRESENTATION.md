# When the additive cost is forced

*Sunday 22 November 2026, America/New_York. Branch `representation-2026-11-21`, draft PR, off `main` at `d1a6de4`. Written by one executor for Chad Mitchell. Revised the same day after `reviews/representation_2026-11-21/REVIEW.md` (NOT-READY). The repairs are a self-check, not a re-review. Addresses the representation gap in `theory/MATH_COMPLETENESS_AUDIT.md` §3.1 (draft PR #151; that note is not on this branch). It does not change the Part 2 hypothesis sentence, and it does not edit `reviews/`, any preregistration, or any hash or locked file.*

*Theorems R1 and R2 below are this note's names. CLAIM_MAP section R is already the selection note (`theory/SELECTION_AXIOMS.md`, rows R1–R3). These two theorems are indexed as V1 and V2.*

## 0. Bottom line

The master equation

\[
J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L,
\]

subject to \(P(\mathrm{ruin})\le\varepsilon_r\), is not forced by "store, predict, act, stay solvent." Those four demands constrain a feasible set. They do not choose a functional on it. THEORY §3 already says the equation is the statement of the problem, not a theorem. This note does not withdraw that sentence. A weaker price-free candidate, Hypothesis F in §7, is stated as a hypothesis to test and is not a conclusion.

What is true is narrower, and it is a theorem.

**Theorem R1 (sufficiency).** Under A1–A7, on a product of at least three essential intervals, every continuous cost that represents the preorder equals

\[
C=a\bigl(\sum_i p_i z_i\bigr)+b
\]

with one \(a>0\) and one real \(b\). The prices \(p_i\) are not signed by those seven axioms. A coordinate that is not essential has price zero. Nonnegative prices need A8, the further assumption that each concatenating coordinate is a bad. Layer count is discrete. Debreu's theorem, as cited, does not cover it. The term \(hK\) is a separate integer argument, and it enters the sum only under an extra separability assumption that the citation does not prove (§3).

**The affine freedom, stated carefully.** \(C=aJ+b\) with \(a>0\):

- preserves the argmin on any menu that does not depend on the numerical value of the cost;
- preserves the absolute excess \(d/(2\beta)\) only if the scale \(a\) is fixed, when \(\beta\) is held fixed as the selection slope on a named numerical cost;
- does not preserve the constrained argmin when the reserve pays the numerical cost, and does not preserve the fractional excess \((\mathbb{E}[J]-J^\star)/J^\star\), unless the zero is fixed as well.

A strictly increasing transform that is not affine still preserves the argmin on a fixed menu. It does not preserve \(d/(2\beta)\). Ordinal uniqueness would support "they minimize." It does not support the number.

**Theorem R2.** Kelly and the Lundberg objective are ways to store, predict, act, and stay solvent, and their argmins differ from the argmin of expected currency cost. The four verbs do not force \(J\). This note does not claim that each axiom has a witness which violates that axiom alone and leaves the additive form. Several candidates stay inside the form. They are reclassified in §5.

The pieces of R1 are known theorems applied to this coordinate list (Debreu, a monotone Cauchy equation, von Neumann–Morgenstern, Faddeev's axioms as stated by Aczél, Forte and Ng). The packaging is the claim. It is not a derivation of \(J\) from persistence, and it is not the missing arrow the audit called U.

## 1. The axioms

Each axiom is an assumption. None of them is a restatement of persistence.

**A1. Continuous complete preorder.** On the product of resource coordinates to which Debreu is applied, the decision maker has a complete, transitive preorder \(\succeq\) whose upper and lower contour sets are closed in the product topology. Continuity is part of the axiom. Completeness alone does not give a real-valued cost: a lexicographic preorder is complete and has none. This repository does not compute a lexicographic design. F1, in §5, is a two-party game without a potential. It is not a failure of completeness for one agent.

**A2. Expected cost under risk.** Preferences over lotteries of currency outcomes satisfy the von Neumann–Morgenstern axioms: completeness, transitivity, continuity, and independence (von Neumann and Morgenstern, *Theory of Games and Economic Behavior*, 60th Anniversary Commemorative Edition, doi 10.1515/9781400829460; Crossref returns this edition, 2007, not a 1944 record). The von Neumann–Morgenstern index is affine in the currency loss. That is risk neutrality in the one currency of A4. The ranking of risky designs is then the ranking by expected currency cost. Solvency is a constraint on the feasible set, \(P(\mathrm{ruin})\le\varepsilon_r\), not a term in the objective and not a replacement of the objective by a tail exponent or a growth rate.

Von Neumann–Morgenstern alone gives an expected utility, unique up to a positive affine transformation. It does not give expected cost. Logarithmic utility is a von Neumann–Morgenstern index, and it is Kelly's criterion, which R2 separates from expected cost.

**A3. Separability across independent sub-activities.** For the coordinates to which Debreu is applied, the resource vector lies in a product of \(n\ge 3\) intervals, each a connected separable space, at least three of them essential. The preorder is preferentially independent: for every subset of those coordinates, the ranking of two values does not depend on the fixed values of the others. This is Debreu's hypothesis, not a consequence of storing and acting. Layer count is an integer. It is not one of these factors.

**A4. One currency.** The consequences Debreu adds are one real index, not a vector of incomparable objectives. Debreu's scalar sum is already that index. R1 does not use homogeneity of degree 1. That strong form is the hypothesis of Theorem S (Lemma B12). S4 breaks a constant elasticity in size. It does not break A4 as R1 uses it (§5).

**A5. Concatenation.** Two concatenations, both Cauchy equations.

- *Over time.* The cost of running the same design on successive durations \(t\) and \(s\) is the sum of the costs. There is no fixed charge per interval.
- *Over independent copies.* The cost of two independent parallel copies is the sum of the costs, in each extensive coordinate that is priced (information, layer count, expected loss, and whichever acquisition or link coordinate is the one that adds). There is no capacity ceiling on that coordinate.

**A6. Shannon information, in nats, with the scope the citation actually has.** Aczél, Forte and Ng (doi 10.2307/1426210) show that expansibility, symmetry, subadditivity, and additivity characterize the linear combinations of the Shannon and Hartley entropies, and then characterize each entropy on its own. Faddeev's grouping axiom is the further hypothesis that isolates Shannon entropy of a finite probability law, up to a positive constant (Csiszár, doi 10.3390/e10030261, surveys the characterizations). The constant is the base of the logarithm. This note takes natural logarithms, so a finite-law entropy is in nats, and the constant is absorbed into \(\kappa\). Shannon's 1948 paper is cited as the IEEE reprint doi 10.1109/9780470544242.ch1, which is the reprint Crossref returns, not a record of the 1948 issue.

Mutual information of finite variables is a difference of those entropies, so the finite-law theorem covers it. The Gaussian plants in this repository use a differential mutual information. Faddeev's finite-law theorem does not state that formula. For those plants A6 is an extension, named as such, not a corollary of the finite-law uniqueness. Grouping does not choose which mutual information is the coordinate. A6 includes that choice for the finite case: the coordinate is the gross stock \(I_{\mathrm{mem}}=I(M_t;X^t)\). Predictive information, directed information, and \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\) are different functionals. The repository uses all four (THEORY notation table; `theory/SHANNON_2026-11-21.md`; `theory/THEOREMS.md` T6). No witness in the tree drops only that choice and leaves the additive form (§5).

**A7. Exogenous world.** The law of the world does not depend on the design. The resource vector and the loss lottery are functions of the design alone, against that fixed law. Effort spent changing the world's drift is not one of the coordinates. Every proved theorem in THEORY already sets that effort to zero (the open lever, CX2, CL11). F3 does not, by itself, leave the additive form (§5).

**A8. Monotonicity.** Each concatenating coordinate is a bad: at fixed values of the others, a larger value is weakly worse. A1–A7 do not say this. Without A8 a price may be negative. The cost \(I_{\mathrm{mem}}+K-\mathbb{E}[\ell]\) is continuous, additive, concatenating, Shannon in the memory coordinate, risk-neutral expected currency, and exogenous, and its error price is negative.

## 2. Two lemmas used in the proof

**Lemma C (monotone Cauchy).** Let \(f:(0,\infty)\to\mathbb{R}\) satisfy \(f(x+y)=f(x)+f(y)\) and be monotone. Then \(f(x)=x\,f(1)\).

*Proof.* Induction gives \(f(nx)=nf(x)\) and \(f(x)=nf(x/n)\), so \(f(q)=q\,f(1)\) for every positive rational \(q\). Let \(x>0\) and let rationals \(q_k\uparrow x\) and \(r_k\downarrow x\). If \(f\) is nondecreasing, \(f(q_k)\le f(x)\le f(r_k)\). Both ends converge to \(x\,f(1)\), so \(f(x)=x\,f(1)\). If \(f\) is nonincreasing, \(-f\) is nondecreasing and additive, and the same conclusion holds. □

No continuity axiom beyond monotonicity is used. A discontinuous additive function that is not of this form requires the axiom of choice and is not monotone. It is excluded here. Debreu continuity of a real factor also excludes it: a continuous additive \(f\) is linear, monotone or not. The proof above uses monotonicity because that is the hypothesis Lemma C states.

**Lemma P (Pexider).** Suppose \(f(x+y)=f(x)+f(y)+c\) for a constant \(c\), and \(f\) is monotone, or continuous. Set \(g=f+c\). Then \(g(x+y)=g(x)+g(y)\). Lemma C, or continuity, gives \(g(z)=pz\), so \(f(z)=pz-c\). The constant \(-c\) joins the additive constant \(b\) of the total cost. Concatenation "up to a constant" is this one line. It is not an application of Lemma C to an equation Lemma C does not state.

**Lemma C\(_\mathbb{Z}\) (integer Cauchy).** Let \(f\) map nonnegative integers to the reals and satisfy \(f(m+n)=f(m)+f(n)\). Then \(f(0)=0\) and \(f(n)=nf(1)\). *Proof.* \(f(0)=f(0+0)=2f(0)\). Induction gives the rest. No monotonicity and no topology are used. □

**Lemma M (signs).** If \(f(z)=pz\) and \(f\) is nondecreasing, then \(p\ge 0\). If the coordinate is not essential, the preorder does not depend on it, so \(p=0\). Lemma M uses A8. It is not a conclusion of A1–A7.

## 3. Theorem R1 (sufficiency)

**Theorem R1.** Assume A1–A7. Restrict Debreu's step to a product of intervals, at least three of them essential, with contour sets closed in that product topology. Then any continuous cost representing the preorder on that product has the form

\[
C=a\Bigl(\sum_i p_i z_i\Bigr)+b,
\]

with one \(a>0\) and one real \(b\). A coordinate that is not essential has price zero. The prices \(p_i\) may have either sign. The cost \(I_{\mathrm{mem}}+K-\mathbb{E}[\ell]\) is an example with a negative error price, and it satisfies A1–A7.

Assume A8 in addition. Then each price on a concatenating coordinate is nonnegative, and the master equation's \(\kappa,h,w\ge 0\) is that case.

Layer count is not a factor in the Debreu step. Under concatenation of nonnegative integer counts, Lemma C\(_\mathbb{Z}\) gives a term \(hK\). Putting that term in the same sum assumes the discrete factor is preferentially independent of the interval factors. A3's wording states that independence for the interval factors. Debreu's cited theorem does not prove an additive representation on a mixed product of intervals and a discrete set. R1 claims \(hK\) inside the sum only under that extra separability assumption, which is named here and is not the citation.

The ruin constraint is not produced by the representation. It is the feasibility restriction in A2.

*Proof.*

1. *The criterion is an expectation.* By A7 the world law is fixed, so each design determines a lottery over currency outcomes and a resource vector. By A2 the von Neumann–Morgenstern theorem supplies an expected utility of that lottery, and risk neutrality makes the utility the currency loss. The ranking is expected currency cost. The only freedom at this step is a positive affine regraduation of the currency unit.

2. *The expectation adds across interval coordinates.* Apply A1 and A3 on a product of intervals. Debreu's theorem (the essay "Topological methods in cardinal utility theory," cited here as the Crossref reprint doi 10.1017/ccol052123736x.010; the year field came back empty, and the title and author match the essay) gives continuous functions \(f_i\) on those factors such that one vector is preferred to another if and only if \(\sum_i f_i\) is smaller as a cost, and

   \[
   f_i\;\mapsto\;a f_i+b_i,\qquad a>0,
   \]

   is the only freedom. Continuity in the citation is closed upper and lower contour sets in the product topology. The hypothesis \(n\ge 3\) is Debreu's. Preferential independence of two coordinates is not enough for an additive representation. The missing ingredient in the two-coordinate case is the Thomsen condition on tradeoffs. This note does not assume it, and R1 is not claimed when fewer than three interval coordinates are essential. A two-term problem such as CT12 is inside the written master equation by specification of those two terms. It is not an application of Debreu's \(n\ge 3\) theorem. The integer layer count is not a factor in this step.

3. *Each concatenating real coordinate is linear.* Fix an essential interval coordinate \(z\) that satisfies A5, and hold the others fixed. Additivity over independent copies may carry a constant: \(f(z_1+z_2)=f(z_1)+f(z_2)+c\). Lemma P, using monotonicity or Debreu continuity, gives \(f(z)=pz-c\), and \(-c\) joins \(b\). Additivity over time, at a fixed rate, is the same equation in the duration. The prices are not signed unless A8 is assumed. Under A8, Lemma M gives \(p\ge 0\).

   *The discrete count, separately.* If layer counts concatenate, Lemma C\(_\mathbb{Z}\) gives \(f(K)=hK\) with no topological hypothesis. The sign of \(h\) is nonnegative only under A8. Adding \(hK\) to the Debreu sum of the interval factors assumes preferential independence of \(K\) from those factors. That assumption is extra. It is not Debreu's theorem on a mixed product.

4. *The memory coordinate, in the scope A6 states.* For finite variables, A6 makes the memory coordinate Shannon mutual information in nats, and the positive constant is absorbed into \(\kappa\). A change of base rescales \(\kappa\) and does not change the argmin on a fixed menu. For a Gaussian plant the coordinate in the proofs is a differential mutual information. That step is the extension A6 names. It is not the finite-law theorem.

5. *Acquisition and links.* The same two steps apply to any acquisition or link coordinate that is an interval and concatenates: its Debreu component is linear in that coordinate. The price is nonnegative only under A8. The sum of those terms is what the master equation writes as \(A+L\). A pricing that does not concatenate in its displayed coordinate is not forced to be linear. The per-precision price \(c'\,r^{-\theta}\) (Lemma B2) is a function of precision, not a linear function of the precision coordinate. It can still be a rate, linear in duration at fixed precision, and that rate can still sit in an additive sum. R1 does not choose the coordinate. Which of the three pricings of \(A\) a system pays is V4, and it is open.

6. *One scale, one constant.* The currency regraduation of step 1 and Debreu's common scale are the same \(a\), because the cost is already the von Neumann–Morgenstern index of the currency loss. The constants \(b_i\) sum to one \(b\). They are not a second, independent rescaling. □

**Nonnegative prices are A8, not A1–A7.** Nothing in A1–A7 stops a coordinate from being a good. The positive-affine class, one \(a>0\) and one real \(b\), with price ratios fixed by the Cauchy equation, is the uniqueness class those seven axioms give. The orthant constraint is A8. The master equation writes nonnegative prices by taking A8. That is not a theorem about physics. Landauer (doi 10.1147/rd.53.0183) and Barato, Hartich and Seifert (doi 10.1088/1367-2630/16/10/103024) are floors under a physical price. They are inequalities. They do not produce the sum. Sagawa and Ueda (doi 10.1103/PhysRevLett.102.250602; erratum doi 10.1103/PhysRevLett.106.189901) bound measurement work and erasure work together. Stacking \(\kappa I_{\mathrm{mem}}\) and a second thermodynamic price on directed information double-counts that bound. `theory/SHANNON_2026-11-21.md` already refuses the stacking. R1 does not restore it. The prices here are accounting prices in one currency. A physical floor is a separate, optional, lower bound on a price.

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

**Theorem R2.** Kelly growth and the Lundberg objective are both ways to store, predict, act, and stay solvent. Neither is expected currency cost, and neither has the argmin of expected currency cost. The four verbs do not force \(J\).

*Kelly isolates risk neutrality, and it leaves the expected-currency form.* Logarithmic utility satisfies the von Neumann–Morgenstern axioms and violates the risk-neutrality clause of A2. Kelly 1956 (doi 10.1002/j.1538-7305.1956.tb03809.x) maximizes expected log growth. CT42 in `theory/DYNAMICS.md`: a shared shock of probability \(0.05\), calm factors \(a_1=1.30\) and \(b_1=1.05\), shock factor \(b_0=0.90\). The lineage weight on the robust design is \(q^\star=\beta a_1/(a_1-b_1)=0.26\). The per-unit expectation picks the pure lean design. Its mean factor is \(0.95\times 1.30=1.235\). The robust design's mean factor is \(0.95\times 1.05+0.05\times 0.90=1.0425\). A mixture is not the argmin of a linear expected cost on a simplex. Donaldson-Matasci, Bergstrom and Lachmann (doi 10.1111/j.1600-0706.2009.17781.x) are the fitness-value form of the same growth criterion, already used as S5 in `theory/GENERAL_THEOREM.md`.

*Lundberg is a different objective, not a one-clause drop of risk neutrality.* Maximizing \(\theta=2m/s^2\) drops expected utility, not only the shape of the utility index. On the published point (\(y=1\), \(c=0.05\), \(w=\sigma=1\), \(s_0=0.3\)) the survival-optimal interval is \(\tau_S=0.2362\) and the expected-cost interval is \(\tau_E=0.3162\). They are not the same design. The agreement when the reserve's own noise dominates is a limit inside this model, not an identity of the two objectives (THEORY, the correction to Theorem L). `theory/representation_checks/binding_multiplier.py` recomputes both endpoints. Chance-constrained expected cost remains one way to stay solvent. It is not the only way. CT33 applies to \(S+wE\) on a stake-independent menu. It is not a theorem about \(\arg\max\theta\).

**Reclassified. These do not leave the additive form, and they are not ablations of one axiom.**

- *F1 is not a failure of A1 for one agent.* Matching pennies (`theory/COADAPTATION.md`) has no potential. The chain is uniform at every selection strength, and each party's regret stays \(1/2\). A single decision maker's preorder can still be complete. F1 is a two-party game.
- *CT34(iv) and CT36 do not leave an additive joint cost.* Four units with a shared driver, scored as if their upkeeps added, miss the pooling gain: per-unit error \(0.0905\) locally against \(0.0410\) pooled at correlation \(1\) (`scope_checks.py` §2). The joint design can still carry one additive cost in joint coordinates. CT36's fixed-rate excess at \(r_L=r_S=0.5\), \(r_{LS}=0.8\) is \(-2/9\): the joint value depends on \(r_{LS}\), and that interaction sits inside one error term. Upkeeps can add while the values do not. CT34(ii)'s proved direction is different and still additive: when what the parent passes down depends on the parent's design, the parent's objective is \(F(x)+J_T^\star(\theta(x))\), a value function, not \(F(x)\) plus a constant upkeep. The converse is not proved.
- *S4 stays inside R1's family.* A fixed per-check cost plus a size-proportional cost, with stakes and drift variance proportional to size, has local interval elasticities from about \(-1\) to \(-1/2\) as size runs from \(1\) to \(10^6\) (`theory/GENERAL_THEOREM.md` S4, `c5c`). Both components are one currency. The objective stays a sum and is homogeneous of degree 1 in that currency. The interval optimum is the EOQ optimum of the linear check-rate cost \((a_1+a_2 n)/T\). What S4 breaks is a constant elasticity in size. That is Theorem S. It is not an exit from the additive form, and it is not two axioms at once.
- *A flow price is a price vector inside the same family.* The cost \(c\cdot r+wD\) is the master-equation form with \(\kappa=0\), \(h=0\), and \(A=c\cdot r\). Comparing its argmin with the argmin of \(\kappa I_{\mathrm{mem}}+w\,\mathbb{E}[\ell]\) compares two price vectors. The grid figure \(0.9574\) (`theory/SHANNON_2026-11-21.md`) is an achievability gap for a design that prices the stock and the flow together. It is not an exit from the form. Tatikonda and Mitter (doi 10.1109/tac.2004.831187) and Tatikonda, Sahai and Mitter (doi 10.1109/TAC.2004.834430) remain the sources for the flow. There is no witness in the tree that drops only A6.
- *Still drops two axioms.* Still, Sivak, Bell and Crooks (doi 10.1103/PhysRevLett.109.120604): under their hypotheses, dissipation per step equals \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\) (`theory/THEOREMS.md` T6, \(I[s_t;x_t]-I[s_t;x_{t+1}]\), checked to 6 decimals on a two-state system). That functional is not \(\kappa I_{\mathrm{mem}}\), and \(I_{\mathrm{pred}}\) is not a function of \(I_{\mathrm{mem}}\) and \(\mathbb{E}[\ell]\) separately, so separability fails with the information choice. It is not a pure A6 ablation.
- *F3 does not leave the additive form.* For \(g>1\) the weighted potential is a saddle unbounded below, and the linearization runs away (`theory/COADAPTATION.md`). Each party cost is nonnegative, and both are zero at the origin, so each cost has a minimizer. Those costs are additive quadratics. The missing minimum is a fact about the saddle. It is not a fact about the form of either cost. Touchette and Lloyd (doi 10.1103/PhysRevLett.84.1156) bound feedback. They do not, by themselves, exhibit a cost that has left the additive form. CX2 stays open.

**What R2 does not say.** It does not say the four verbs are inconsistent with expected-cost \(J\). That objective is one way to stay solvent. It does not say each of A1–A8 is necessary in the sense of a one-axiom witness. The isolating witness that is actually in the tree is Kelly's, for risk neutrality. Lundberg shows a second solvency criterion with a different argmin, and it drops more than one clause of A2.

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
- **F-0.** The scores actually attained, \(Z_0(W)\), are the image of a nonempty compact set of designs. \(Z_0(W)\) is compact. The sum of the five coordinates attains its minimum on \(Z_0(W)\), and that minimizer is Pareto in \(Z_0(W)\).
- **F-D.** Free disposal is a hull, not a property of the compact image. Set \(Z(W)=Z_0(W)+\mathbb{R}_+^5\). If \(z\in Z(W)\) and \(z'\ge z\), then \(z'\in Z(W)\). This hull is closed and unbounded. It is not compact. In \(\mathbb{R}^5\) no nonempty set is both compact and closed under adding an arbitrary positive increment. A Pareto point of the hull is a Pareto point of \(Z_0(W)\): waste is dominated by the point it wastes from, or tied with it and not a new efficient score. Existence comes from F-0, not from compactness of the hull.

F3 is not a missing Pareto point. At \((x,\theta)=(0,0)\) both party costs are zero, and every other score is coordinatewise at least that, so the origin is Pareto for the cost vector. The potential's saddle, unbounded below, is a different fact (§5).

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

**Theorem F1 (scalarization; S3 on this vector).** Let \(Z\subset\mathbb{R}^5\) be a free-disposal set: \(Z=Z_0+\mathbb{R}_+^5\) for some nonempty \(Z_0\). The hull need not be convex. Part (ii) assumes convexity, for instance by passing to \(\mathrm{conv}(Z_0)+\mathbb{R}_+^5\).

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

A coordinate cap preserves convexity. If \(Z\) is convex and \(\rho\) is one of its coordinates, then \(Z\cap\{\rho\le\varepsilon_r\}\) is convex, and every Pareto point of the capped set minimizes a nonnegative weighted sum over that set. On the scalar path of CT22, unimodality makes \(\{\theta\ge\theta_{\mathrm{req}}\}\) a closed interval, so that cap preserves convexity too. What can fail is a chance constraint that is not a half-space in the scored coordinates. S3's caveat is that statement: \(P(\mathrm{ruin})\le\varepsilon\) cut into the design set, rather than into \((I,r,K,D)\), need not leave a convex image. A nonconvex set of surviving designs can have a nonconvex score image even when the uncapped image was convex. That is the case in which ruin breaks the convexity (ii) uses. A cap on a coordinate of a convex score set does not.

### 7.5 What is GTAO-specific, and what is not

Not specific, and not new: Pareto order, weighted sums, supporting hyperplanes, Farrell efficiency, Debreu's 1951 coefficient, Geoffrion's proper efficiency, Shoval et al. on evolutionary fronts, and S2–S3 as already written for \((I, r, K, D)\).

Specific to this repository, and already stated before this section: the feasible set is computed from the world's statistics and from the information floors, rather than fitted to a cloud of traits (SHANNON §6, the sentence on Shoval). The layer cap is the dominance fact in §7.3, in the linear-Gaussian plants where it is proved.

Specific to Chad's note, and still a hypothesis: the bads are these five, attention is a coordinate rather than the currency, and ruin risk is a coordinate rather than only a cap. Nothing in the tree shows that a selected system lies on that front. Hypothesis F stays **OPEN**.

Two routes produce an additive cost, and they are not the same route. On a convex score set, F1(ii) says the prices in a weighted sum are supporting weights, some \(p\ge 0\), \(p\neq 0\). Strictly positive weights are Geoffrion's proper efficiency, which this note does not re-prove. Farrell 1957 and Debreu 1951 are the radial efficiency facts, technical efficiency and the coefficient of resource utilization. They are not the separating-hyperplane argument. R1's route is Debreu plus concatenation on interval factors. It does not need convexity of the image, and a coordinate that does not concatenate can keep a nonlinear Debreu component. The closing identification "the prices are the supporting weights" is the convex route only.

## 8. The scalar path is a different theorem

CT22's binding multiplier is not part of R1. R1 produces the objective. CT22 is a fact about minimizing that objective on one path. The proof is in THEORY Appendix B.9. It replaces the one-word appeal to KKT. The conditions stated there are \(J''>0\) and \((s^2)''>0\) together, which make \(\theta\) strictly unimodal on \(\{m>0\}\) and the feasible set an interval, and constraint qualification \(\theta'\ne 0\) at the binding point. Convexity of the variance rate is one of the two signs. \(\theta\) itself is not concave on the whole domain. A reading that needs a concave certificate is stronger than what the path satisfies, and the scalar proof does not use it.

## 9. Status of the claims

| ID | What | Status |
|---|---|---|
| V1 | Theorem R1 on interval factors: additive form up to one \(a>0\) and one \(b\), signs free until A8; discrete \(K\) is an integer Cauchy term under an extra separability assumption, not Debreu's mixed product | **PROVED (in-model)** |
| V2 | Kelly and Lundberg have different argmins from expected currency cost, so the four verbs do not force \(J\). No one-axiom ablation is claimed for the axioms whose witnesses stay additive | **PROVED (in-model)** |
| V3 | Universal core: CT33 on Class B, CT24 on Class L, CT20(ii) with sensing fixed, CT1 as a bound | **PROVED (in-model)** |
| V4 | Which concatenating coordinate the acquisition price is linear in. Three pricings of \(A\) are in use. A1–A7 do not choose among them | **OPEN** |
| V5 | Hypothesis F: a selected design lies on the Pareto front of (memory held, information bought, error, attention, ruin risk), given the world and the floors. Additive \(J\) would be the priced convex special case. Not a replacement of the Part 2 sentence | **OPEN** |
| V6 | Theorem F1 and the survival list in §7: information floors and the antitone shape of the front need no prices; CT33 and CT20(ii) need a stake with single crossing; layer caps survive as dominance only under an extra monotonicity; weighted-sum equivalence needs convexity, and the three-point dent is the miss | **PROVED (in-model)** |

V1 is a theorem under axioms that are not themselves derived, on the domain §3 states. Calling \(J\) derived from persistence would be a misreading of V1. V2 is the four-verbs claim: Kelly and Lundberg have different argmins from expected currency cost. It is not an ablation of each axiom. V3 adds no inequality. V4 is the slot R1 deliberately leaves unspecified. V5 is a hypothesis, not a conclusion. V6 is S3 on a longer vector, plus a scope list. It is not a new existence theorem about systems. A coordinate cap on a convex score set preserves convexity.

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
