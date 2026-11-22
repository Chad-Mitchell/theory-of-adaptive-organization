# Independent hostile review: PR #154 (representation)

**Reviewer:** independent. Wrote none of `theory/REPRESENTATION.md`, the binding-multiplier check, the claim-map rows, or the pointer edits. The only file added by this review is this one.
**Date:** Sunday 22 November 2026 (UTC).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/154
**Head reviewed:** `e648ef23a560b996d99cc09e8d60a216c2869936` on `representation-2026-11-21`, base `d1a6de448bbaca2e2e0f18d4dc2ce9c3972308a5`. Draft. Not merged.

**Verdict: NOT-READY**

The scalar-path proof of CT22 is valid, the positive-affine arithmetic for the argmin and for \(d/(2\beta)\) is valid, and the three-point dent is a correct failure of weighted-sum scalarization. Theorem R1 as stated is stronger than its proof: nonnegative prices are an extra assumption, and Debreu's theorem is cited for a product that contains a discrete layer count. Theorem R2 does not isolate the seven axioms. In §7 the free-disposal and compactness package cannot hold together, F3 is not a missing Pareto point, and a coordinate cap \(\rho\le\varepsilon_r\) preserves convexity.

## Blockers

1. Theorem R1 states nonnegative prices as a conclusion of A1–A7, and it invokes Debreu on a product Debreu's hypotheses do not cover.

   `theory/REPRESENTATION.md:21–25`, `:49`, `:82`, `:90–98`, `:106`. `measurement/CLAIM_MAP_v2.md:674`. `CORE.md:24`. `THEORY.md:39`.

   The displayed formula has \(\kappa,h,w\ge 0\). The paragraph after the proof says a coordinate may be a good, and Lemma M then gives a negative price. That paragraph is the correct reading of A1–A7. The cost \(C=I_{\mathrm{mem}}+K-\mathbb{E}[\ell]\) is continuous, additive, concatenating, Shannon in the memory coordinate, risk-neutral expected currency, and exogenous, and its error price is negative. Nonnegativity is the further assumption that each concatenating coordinate is a bad. The positive-affine class, one \(a>0\) and one real \(b\), with price ratios fixed by the Cauchy equation, is the right uniqueness class. The orthant constraint is not part of it.

   Debreu's theorem, as cited, needs a continuous complete preorder on a full product of connected separable spaces, at least three of them essential. Continuity means closed upper and lower contour sets in the product topology. A1 places the preorder "on the set of designs, or on the resource vectors," and A3 requires every factor to be an interval. Layer count is an integer. The integer Cauchy equation gives \(f(n)=nf(1)\) once additivity in that coordinate is already in hand. It does not put an additive representation on a product that contains a discrete essential factor. Lemma C itself is valid: a monotone solution of \(f(x+y)=f(x)+f(y)\) on \((0,\infty)\) is linear, and a non-monotone additive pathological solution is excluded by monotonicity.

2. The axiom-by-axiom ablation does not do what V2 says. Several witnesses keep an additive expected cost, and several violate more than the axiom they are paired with.

   `theory/REPRESENTATION.md:142–174`. `measurement/CLAIM_MAP_v2.md:675`.

   R2 says that dropping any one axiom, the form or its argmin fails on a functional already in the repository, and that the functional violates that axiom. "The form" is \(a(\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L)+b\) with \(a>0\). A zero price on an inessential coordinate is inside that form.

   - **A1, F1** (`:148`; `theory/COADAPTATION.md:249`). Matching pennies has no potential, the chain is uniform at every selection strength, and each party's regret stays \(1/2\). The same paragraph says a single decision maker's preorder can still be complete. F1 is a two-party game without a potential. It is not a failure of completeness or continuity for one agent.
   - **A2** (`:150–155`). The diffusion gap is real on the published point: recomputed \(\tau_S=0.236208\), \(\tau_E=0.316228\). Maximizing \(\theta=2m/s^2\) is a different objective, on a one-coordinate menu, and it drops expected utility, not only risk neutrality. The Kelly half does the isolation that is actually available: logarithmic utility is von Neumann–Morgenstern, and CT42's mixture \(q^\star=\beta a_1/(a_1-b_1)=0.26\) at \(\beta=0.05\), \(a_1=1.30\), \(b_1=1.05\) is not the pure per-unit optimum (mean factors \(1.235\) and \(1.0425\)).
   - **A3, CT34(iv) and CT36** (`:157–161`). Shared-driver pooling is a real failure of writing the joint cost as a sum of standalone upkeeps (per-unit error \(0.0905\) against \(0.0410\) at correlation 1, as THEORY states it). The joint design can still carry one additive cost in joint coordinates. CT36's fixed-rate excess at \(r_L=r_S=0.5\), \(r_{LS}=0.8\) is \(-2/9\), so the joint value depends on \(r_{LS}\). That interaction sits inside one error term. The sentence that a representation which forces \(hK\) as a sum of per-layer upkeeps is false for those designs overreaches: the upkeeps can add while the values do not.
   - **A4 and A5, S4** (`:51`, `:164–166`; `theory/GENERAL_THEOREM.md:324–325`). One witness is asked to drop two axioms. Check cost \(a_1+a_2 n\) with stakes and drift variance proportional to size has local interval elasticities from \(-0.999\) to \(-0.501\) across \(n=1\) to \(10^6\). A real sum of the two components exists, which the note says. Both components can be one currency, and the objective stays homogeneous of degree 1 in that currency. The interval optimum is the EOQ optimum of the linear check-rate cost \((a_1+a_2 n)/T\). The clause "the optimum is not the optimum of a linear rate" is false. What S4 breaks is a constant elasticity in size. That is Theorem S. It is inside R1's family.
   - **A6** (`:168–171`). A cost \(c\cdot r+wD\) is the master-equation form with \(\kappa=0\), \(h=0\), and \(A=c\cdot r\). Comparing its argmin with the argmin of \(\kappa I_{\mathrm{mem}}+w\,\mathbb{E}[\ell]\) compares two price vectors inside one family. The grid gap \(0.9574\) is an achievability figure for a design that prices the stock and the flow together. Still's \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\) (T6: \(I[s_t;x_t]-I[s_t;x_{t+1}]\)) lies outside \(\kappa I_{\mathrm{mem}}\), and the note already says it drops A3 as well. There is no witness that drops only A6.
   - **A7, F3** (`:172`; `theory/COADAPTATION.md:251`). For \(g>1\) the weighted potential is a saddle unbounded below, and the linearization runs away. Each party cost is nonnegative and both are zero at the origin, so each cost has a minimizer. The additive form of those costs still holds.

   The sentence that the four verbs do not force \(J\) stands on its own: Kelly and the Lundberg objective are ways to store, predict, act, and stay solvent, and their argmins differ from expected currency cost. That is a smaller claim than an ablation of each axiom.

3. Free disposal and compactness are stated as joint assumptions, and F3 is offered as a case with no Pareto point.

   `theory/REPRESENTATION.md:247–251`.

   F-D says that if \(z\in Z(W)\) and \(z'\ge z\), then \(z'\in Z(W)\). F-C says \(Z(W)\) is nonempty and compact. In \(\mathbb{R}^5\), any nonempty set closed under adding a positive increment is unbounded, so the two assumptions describe no set. Compactness alone does give a Pareto point: the sum of the five coordinates attains its minimum, and that minimizer is undominated. F3 does not remove that conclusion. At \((x,\theta)=(0,0)\) both party costs are zero, and every other score is coordinatewise at least that, so \((0,0)\) is Pareto for the cost vector. The potential having no minimum is a fact about the saddle. It is a different fact.

4. A ruin cap \(\rho\le\varepsilon_r\) on a convex set of score vectors preserves the convexity Theorem F1(ii) uses.

   `theory/REPRESENTATION.md:320`. `theory/MASTER_EQUATION.md:96` is the related overstatement that convexity of the variance rate is what makes \(\theta\) unimodal.

   If \(Z\subset\mathbb{R}^5\) is convex and \(\rho\) is a coordinate, \(Z\cap\{\rho\le\varepsilon_r\}\) is convex, and every Pareto point of the capped set minimizes a nonnegative weighted sum over that set. On the scalar path just proved, unimodality makes \(\{\theta\ge\theta_{\mathrm{req}}\}\) a closed interval, so the cap preserves convexity there too. S3's caveat is a different statement: a constraint \(P(\mathrm{ruin})\le\varepsilon\) that is not a half-space in the scored coordinates of \((I,r,K,D)\) does not hand you a convex image. The sentence that the cap can destroy convexity, and that S3 says so, states a stronger claim than S3 and a false claim about a coordinate cap.

## Should-fixes

1. `THEORY.md:82`. Section 5 (iv) still says the binding multiplier moves the design from the expected-cost optimum toward the survival optimum, with no scalar-path restriction. The proof at `:439` and `:461`, the claim-map row for CT22, and `theory/REPRESENTATION.md:332` all limit the claim to Lemma B9's diffusion path. The same sentence should carry that limit. `theory/MASTER_EQUATION.md:98` still says that below \(B_{\min}\) no design survives; the proof says the design is not certified by a sufficient bound.

2. `theory/REPRESENTATION.md:98`. Concatenation is said to give \(f(z_1+z_2)=f(z_1)+f(z_2)\) up to a constant, and Lemma C, which has no constant, is applied directly. The Pexider step is one line: if \(f(x+y)=f(x)+f(y)+c\), then \(g=f+c\) is Cauchy, \(g(z)=pz\), and \(c\) joins the additive constant \(b\). Monotonicity, or Debreu continuity, has to be named as the hypothesis that licenses Lemma C.

3. `theory/REPRESENTATION.md:51` and `:59`. A4, as written, is commensurability. Debreu's scalar sum is already a commensurate index, and R1 does not use homogeneity of degree 1. The strong form is Theorem S's hypothesis. A6 cites Aczél, Forte and Ng for Faddeev's grouping axiom and Shannon uniqueness. Their abstract's natural list (expansibility, symmetry, subadditivity, and additivity) characterizes linear combinations of the Shannon and Hartley entropies, and the paper then characterizes each entropy on its own. The grouping axiom is the further hypothesis. Faddeev also fixes the entropy of a finite law. The coordinate in use is a mutual information, and in the Gaussian plants it is a differential mutual information.

4. `theory/REPRESENTATION.md:226` and `:328`. Farrell 1957 and Debreu 1951 are the radial efficiency facts (technical efficiency; the coefficient of resource utilization). S3(ii) and F1(ii) are supporting-hyperplane arguments for some nonzero \(p\ge 0\). Geoffrion 1968 is cited accurately at `:306`: proper efficiency, strictly positive weights, convex data. The closing sentence that the prices are the supporting weights covers only the convex route. R1's route is Debreu plus concatenation and allows a nonlinear component on a coordinate that does not concatenate.

## Nits

1. `theory/representation_checks/binding_multiplier.py:341–346`. The dent is checked on 21 weights of the simplex. The rearrangement in the note already covers every \(p\ge 0\). A 10,001-point rerun also found no supporting weight. The constraint-qualification check at the end of `published_path` tests \(\theta'(\tau_S)\approx 0\) and one binding point.

2. `theory/MASTER_EQUATION.md:96`. Unimodality on this path uses \(J''>0\) and \((s^2)''>0\) together, on \(\{m>0\}\). Convexity of the variance rate is one of those two signs.

## Per-claim table

| Claim | Verdict |
|---|---|
| V1, additive form and positive-affine uniqueness under a repaired domain and an explicit "each coordinate is a bad" | WEAKER |
| V1, nonnegative prices as a conclusion of A1–A7 | WRONG |
| V1, argmin on a menu that does not depend on the numerical cost | FAITHFUL |
| V1, absolute excess \(d/(2\beta)\) at fixed \(\beta\), scale \(a\), constant \(b\) | FAITHFUL |
| V1, fractional excess moves with \(b\) and is invariant to pure rescaling | FAITHFUL |
| V1, reserve constraint: the constrained argmin moves with \(a\) and \(b\) | FAITHFUL |
| V2, each axiom dropped, a witness violates only that axiom and leaves the additive form | WRONG |
| V2, the four verbs do not force \(J\) | FAITHFUL |
| V3, scope list for CT33, CT24, CT20(ii), CT1 | FAITHFUL |
| V4, which acquisition coordinate concatenates, left open | FAITHFUL |
| V5, Hypothesis F labeled open and untested | FAITHFUL |
| F-O, product order, incomparable designs | FAITHFUL |
| F-D together with F-C | WRONG |
| F3 as a case with no Pareto point | WRONG |
| Antitone slice, information floors as constraints, layer caps as dominance under an extra monotonicity, one real pole | FAITHFUL |
| CT33 and Master Theorem (ii) as monotone selection need a stake with single crossing | FAITHFUL |
| F1(i), F1(ii), and the dent \(A=(0,1)\), \(B=(1,0)\), \(C=(0.6,0.6)\) | FAITHFUL |
| A coordinate cap \(\rho\le\varepsilon_r\) breaks convexity | WRONG |
| CT22 on Lemma B9's diffusion path: strict convexity, strict unimodality, \(\mu_s=-m'/\theta'>0\) on \((B_{\min},B_{\mathrm{slack}})\) | FAITHFUL |
| V6 as the scalarization, the dent, and the survival list in the claim-map row | FAITHFUL |

V6's claim-map sentence does not contain the free-disposal package or the ruin-cap sentence. Those two sentences sit in the section the note marks proved, and they are the blockers above. The status word on the claim-map sentence can stand once they are corrected or removed.

## What was checked and holds

**Lemma C and the affine class.** Induction gives linearity on the positive rationals. A monotone function is squeezed by rational sequences, so \(f(x)=xf(1)\) on \((0,\infty)\). Debreu's \(n\ge 3\) theorem, under its own hypotheses, gives continuous additive components unique up to one common scale and coordinatewise constants. After a Cauchy equation on each concatenating coordinate, the constants sum to one \(b\). The note is right that two essential coordinates need the Thomsen condition, and that CT12 is inside the written equation by specification of two terms. The currency regraduation and Debreu's scale are one \(a\) when the represented cost is already the von Neumann–Morgenstern index of currency loss. Risk neutrality is an extra clause beyond the von Neumann–Morgenstern axioms, and logarithmic utility is the Kelly case. Both of those distinctions are drawn correctly.

**Argmin and \(d/(2\beta)\).** On a menu that does not depend on the numerical cost, \(C(\mathcal{D}_1)\le C(\mathcal{D}_2)\) if and only if \(J(\mathcal{D}_1)\le J(\mathcal{D}_2)\) whenever \(C=aJ+b\) with \(a>0\). Any strictly increasing transform of \(J\) has the same argmin. It does not preserve \(d/(2\beta)\).

Theorem SA1b applies to whichever numerical cost the log-linear map is applied to. If \(C=aJ+b\) and the weight is the weight of \(J\), with \(\beta\) held fixed as the slope on \(J\), then \(C-C^\star=a(J-J^\star)\) pathwise, so \(\mathbb{E}[C]-C^\star=a\,d/(2\beta)\). That equals \(d/(2\beta)\) if and only if \(a=1\). The constant \(b\) cancels. Refitting the exponent \(-\beta_{\mathrm{old}}J\) as \(-\beta_{\mathrm{new}}C\) gives \(\beta_{\mathrm{new}}=\beta_{\mathrm{old}}/a\), and the excess of \(C\) is \(d/(2\beta_{\mathrm{new}})=a\,d/(2\beta_{\mathrm{old}})\). The form survives the refit. The number quoted for \(J\) survives only at \(a=1\). Whitening does not disturb the pathwise identity. The fractional excess is \(a(\mathbb{E}[J]-J^\star)/(aJ^\star+b)\). Pure rescaling leaves it unchanged. A nonzero \(b\) changes it. A2-M, monotone copying without the log-linear map, does not give \(d/(2\beta)\). The haploid Moran slope \(\beta=\alpha(N-1)\) is the case the note names.

The Lundberg margin is \(m=y-C\). Replacing \(J\) by \(aJ+b\) changes the margin, the exponent, and the feasible set. The constrained argmin is the argmin in the reserve's unit.

**CT22, every step on the diffusion path.** \(J(\tau)=c/\tau+\alpha\tau\) with \(\alpha=w\sigma^2/2>0\) has \(J''=2c/\tau^3>0\) and unique minimizer \(\tau_E=\sqrt{c/\alpha}\). The margin is \(m=y-J\), so \(m'=-J'\). The variance rate \(s^2=s_0^2+\beta\tau^3\) with \(\beta=w^2\sigma^4/3>0\) has \((s^2)''=6\beta\tau>0\). On \(\{m>0\}\), \(\theta=2m/s^2\). With \(\varphi=m's^2-m(s^2)'\), the quotient rule gives \(\theta'=2\varphi/(s^2)^2\), and differentiating gives \(\varphi'=m''s^2-m(s^2)''\). The cross terms cancel. Both remaining terms are negative on \(\{m>0\}\), so \(\varphi\) is strictly decreasing there. The assumption \(m(\tau_E)>0\) puts \(\tau_E\) in an open interval \((r_1,r_2)\) on which \(m>0\), with \(r_1<\tau_E<r_2\). Near \(r_1\), \(m\downarrow 0\) and \(m'>0\), so \(\varphi>0\). At \(\tau_E\), \(m'=0\) and \((s^2)'>0\), so \(\varphi<0\). Hence exactly one zero \(\tau_S\in(r_1,\tau_E)\). An independent grid on \((r_1,r_2)\) found one sign change of \(\varphi\) and a negative \(\varphi'\) throughout.

Superlevel sets of a positive requirement are closed intervals. \(B_{\min}=\ln(1/\varepsilon_r)/\theta(\tau_S)\) and \(B_{\mathrm{slack}}=\ln(1/\varepsilon_r)/\theta(\tau_E)\) satisfy \(0<B_{\min}<B_{\mathrm{slack}}\) because \(\theta(\tau_S)>\theta(\tau_E)>0\). Below \(B_{\min}\) the bound certifies nothing. Above \(B_{\mathrm{slack}}\), \(\tau_E\) is feasible and is the unique minimizer. At \(B_{\mathrm{slack}}\) the multiplier \(\mu_s=0\) is the only one, because \(\theta'(\tau_E)\ne 0\). Between them the feasible set is \([\tau_L,\tau_R]\) with \(\tau_L<\tau_S<\tau_R<\tau_E\), and a strictly convex \(J\) whose unconstrained minimizer lies to the right of that interval is minimized at the right endpoint. There \(\theta'<0\) and \(J'<0\), so the stationarity condition \(J'-\mu\theta'=0\) gives \(\mu_s=J'/\theta'=-m'/\theta'>0\). Strict convexity of \(J\) and convexity of the feasible interval give uniqueness. Concavity of \(\theta\) is not used. A second-difference grid found both signs of \(\theta''\) (about \(+42\) and \(-1.1\times 10^4\)).

Recomputed published point, \(\varepsilon_r=10^{-3}\), \(s_0=0.3\): \(\tau_S=0.236208\), \(\tau_E=0.316228\), \(B_{\min}=0.486441\), \(B_{\mathrm{slack}}=0.507853\). Along \(B=0.49,0.50,0.505\) the optimum is \(0.267416\), \(0.299050\), \(0.310392\), and \(\mu_s\) is \(0.031483\), \(0.005231\), \(0.001482\). At \(B=0.5\), \(dJ^\star/dB=-0.1445\), which rounds to the \(-0.145\) in `theory/MASTER_EQUATION.md`. As \(B\downarrow B_{\min}\), \(\theta'\to 0\) from below while \(J'(\tau_S)<0\), so \(\mu_s\to+\infty\). As \(B\uparrow B_{\mathrm{slack}}\), \(\mu_s\to 0\). The obstructions in the check do the work claimed for them: a non-quasiconvex \(J\) can have a feasible local minimum with multiplier zero while the global unconstrained minimum is uncertified, and a two-peak \(\theta\) can put the constrained minimizer off the segment between the survival peak and the expected-cost minimum. The exact Lundberg root in `theory/theorem-v2-checks/c3_lundberg_persistence.py` is a different object, at \(s_0=0.5\) (exact \(0.258\), diffusion \(0.269\)). The proof is about \(\theta=2m/s^2\).

**Frontier geometry that holds.** The product order is a partial order. In a slice with the other coordinates fixed, two Pareto points have coordinate differences whose product is nonpositive: if both differences were positive, one point would dominate the other. Information floors constrain \(Z(W)\) and do not pick a point. An extra layer that raises memory or attention, and does not cut error, is dominated. For one real pole, \(E_1=E_\infty\), so under that monotonicity every \(K\ge 2\) is dominated by \(K=1\) at the same error, and \(K=0\) and \(K=1\) can both sit on the front when the blind error is finite. The priced statement \(K^\star\in\{0,1\}\) for every stake ratio is a further selection. Milgrom and Shannon's condition, on a chain, reduces to single crossing. For \(J=S+wE\) the difference between a higher-spend, lower-error design and its alternative crosses zero at most once in \(w\). A parameter-free selection from the Pareto set has no such parameter. Topkis 1978 is the right citation for isotone minimizers of a submodular function on a lattice: the Crossref abstract of doi 10.1287/opre.26.2.305 states that comparative-statics theorem.

F1(i): a strictly positive weight makes a dominated point strictly more expensive, with no convexity. F1(ii): \(Z-z^\star\) is convex and misses the open negative orthant, so a separating normal may be taken nonnegative and nonzero, and \(z^\star\) minimizes the inner product. Strictly positive weights are Geoffrion's proper-efficiency theorem. The dent is Pareto in \(\{A,B,C\}\) because each pair is incomparable. For \(p\gg 0\), \(\langle p,C\rangle\le\langle p,A\rangle\) and \(\langle p,C\rangle\le\langle p,B\rangle\) rearrange to \(p_1/p_2\le 2/3\) and \(p_2/p_1\le 2/3\). The product of those bounds is \(4/9\). If either price is zero, \(A\) or \(B\) scores zero and \(C\) scores a positive multiple of the other price. The mixture \((1/2)A+(1/2)B=(0.5,0.5)\) dominates \(C\). Once mixtures are feasible, \(C\) is off the front, and linear scalarization sees the exposed face of the convex hull. S2 already says that.

**Prior art, checked on Crossref in this session.** Farrell 1957, doi 10.2307/2343100, is "The Measurement of Productive Efficiency," Journal of the Royal Statistical Society Series A, 120:253. It defines technical efficiency and price efficiency for a firm's inputs. Debreu 1951, doi 10.2307/1906814, is "The Coefficient of Resource Utilization," Econometrica 19:273. The coefficient is the smallest resource shrinkage that still meets the same wants. Geoffrion 1968, doi 10.1016/0022-247X(68)90201-1, is "Proper efficiency and the theory of vector maximization," Journal of Mathematical Analysis and Applications 22:618–630. Proper efficiency is the notion tied to strictly positive weights on a convex problem. Shoval, Sheftel, Shinar, Hart, Ramote, Mayo, Dekel, Kavanagh and Alon 2012, doi 10.1126/science.1217405, Science 336:1157, has the title the note prints. The abstract presents multi-objective optimality as a low-dimensional front in trait space and reads data as lying near one. That is their result. The note does not claim it as a theorem of this repository.

The Debreu cardinal-utility reprint doi 10.1017/ccol052123736x.010 returns the essay title, author Debreu, and an empty year field, as the note says. The original essay is from 1960. The claim-map Why cell says so. Aczél, Forte and Ng 1974 is the paper discussed under should-fix 3. The packaging sentence, that the pieces of R1 are known theorems applied to this coordinate list, matches those sources. Pareto order, weighted sums, supporting hyperplanes, and proper efficiency are standard vector optimization. The note says so in §7.5. The five names, with attention as a coordinate and ruin risk as a coordinate, are marked open. That division is the right one.

**Duplication.** `theory/SHANNON_2026-11-21.md` S2–S3 already has the support function, the free-disposal hull of the Pareto face, and the weighted-sum equivalence for \((I,r,K,D)\), including the caveat that a ruin constraint need not leave a convex set. `CORE.md:30` already records that frontier and that caveat. `theory/PRICE_FREE_2026-11-21.md` sorts scalar theorems and keeps a scalar cost. `measurement/FRAMEWORK.md` has no Debreu, Farrell, Geoffrion, or Pareto-front representation. THEORY §3 already says the master equation is the statement of the problem. The new sentences at `THEORY.md:39` and `CORE.md:24` point at this note. V6 is S3 on a longer vector, which the note says.

**Hypothesis sentence and the diff.** The sentence `The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.` occurs once each in `THEORY.md`, `CORE.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`, the same bytes as at `d1a6de4`. `git diff --stat d1a6de4...e648ef2` is the 14 files in the PR. No path under `reviews/` is in that diff, and no preregistration or locked hash is in it. This review adds one file under `reviews/`.

## Commands

All of these were run from the repo root on head `e648ef2`, after `git fetch origin main` (`origin/main` = `d1a6de4`). The local `origin/main` before that fetch was `2eeab30`, and `check_fresh.py` failed against that stale ref. Numerics and the test suite used `nice -n 19`. `lake build` was not run. NumPy 2.5.5, SciPy 1.18.1, SymPy 1.14.0, pytest 9.2.0. An independent recomputation of the path, the dent, CT36's \(-2/9\), CT42's \(0.26\), and the S4 elasticities was run outside the repository and was not committed.

- `python3 tools/check_fresh.py`. `STATUS.md main is d1a6de4; window: d1a6de4 b16193d e88b692 8e829e5 fda5557`. `RESULT: PASS`. Exit 0.
- `python3 tools/check_consistency.py`. THEORY v2.9; CLAIM_MAP latest note v2.77; version pins OK; wording FAILs 0 on 31 maintained docs; section N mismatches 0; tally 363; process-rule FAILs 0; core-rule FAILs 0. Two advisory length warnings. `RESULT: PASS`. Exit 0.
- `python3 tools/check_open_work.py`. `union missing from OPEN_WORK.md: 0`. `RESULT: PASS`. Exit 0.
- `python3 theory/representation_checks/binding_multiplier.py`. 39 checks, 0 FAIL, `RESULT: PASS`. Exit 0. The lines include \(\tau_S=0.236208\), \(\mu=0.005231\) at \(B=0.5\), and \(\theta''\) of both signs.
- `python3 -m pytest -q tools`. `248 passed, 1 skipped in 299.13s`. Exit 0. The skip is the Lean test: `lake` is not installed.
