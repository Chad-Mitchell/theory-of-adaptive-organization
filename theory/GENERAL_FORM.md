# The general form of the cost of judgment

*Sunday 22 November 2026, America/New_York. Branch `general-form-2026-11-22`. Written by one executor for Chad Mitchell. A self-check, not an independent review. It does not edit a locked preregistration, a hash, or a LOCK file. It does not change the Part 2 hypothesis sentence. THEORY.md remains the canonical statement where the two disagree: the additive equation there is still the statement of the problem. This note derives the weaker object of which that equation is a special case.*

*`theory/REPRESENTATION.md` is on `main` (PR #154, merged; confirm PR #157, including the nits at `40e10c1`). This note builds on that text. It does not reopen V1–V6. V5 stays OPEN. The frontier re-read was read as a draft, not as authority; it is now `theory/FRONTIER_REREAD_2026-11-22.md` and remains a planning note. Algebra shared with the representation note is re-derived here.*

*Status (23 November 2026). The independent review is `reviews/general_form_2026-11-22/REVIEW.md` (PR #163, NOT-READY). The repair is on main (PR #161). Independent confirm PR #164 is CONFIRMED-WITH-NITS (`reviews/CONFIRM_PR161.md`).*

## 0. The derived form, in one statement

Under an exogenous ergodic environment, a pure design's long-run growth is the Lyapunov exponent \(\lambda=\mathbb{E}[\log W]\), when that expectation is finite. That exponent is a complete preorder on designs. If offspring is strictly decreasing in each coordinate of a chosen bad vector, every maximizer of \(\lambda\) is Pareto in that vector (**PROVED** under H1–H3, §3). If the exponent is known, the selected set is its argmax, which may be a single point. If an observer knows only the monotonicity, the Pareto front is the identified set of points some such exponent could select. It is not proved that one copying process occupies the whole front. Persistence only, with no growth ranking, yields the viability kernel.

A map \(\log W=-\langle c(\omega),z\rangle\) with \(c\ge 0\) makes growth-rate selection minimize the nonnegative linear cost \(\langle\mathbb{E}[c],z\rangle\). That cost is in growth units. It is not the master equation. The master equation is risk-neutral expected currency plus a ruin cap, and those two criteria have different argmins (V2). The coordinates of \(z\) are an input to the map. The information floors constrain which scores are feasible. A floor does not, by itself, make retention decrease in the slot it mentions.

The additive master equation

\[
J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L
\qquad\text{subject to}\qquad P(\mathrm{ruin})\le\varepsilon
\]

with nonnegative prices is the special case in which that front is ranked by risk-neutral expected currency, the prices are linear, and ruin is a half-space cap rather than a traded coordinate.

That special-case relation is the comparison with the ideal-gas law: a named list of extra assumptions collapses a more general relation to a linear formula. It is not a claim that judgment is a gas.

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The sentence is unchanged. "Strongly selected" in THEORY §3 is the operational definition and is not rewritten here. Retention-maximizing, below, is an in-model object.

## 1. Status words

**PROVED** means proved inside the stated model, which says nothing by itself about nature. **NUMERICAL** means computed, not proved. **OPEN** means not derived or not tested, not refuted. **FALSE** means the claim does not follow, and a counterexample is given. **SKETCH** means a protocol that is not a lock. Nothing here is a field result.

Labels used below for the questions in the task: Q1 is §3, Q2 is §4, Q3 is §5, Q4 is §6, Q5 is §7.

## 2. Premises, and the premise that is not used

The selection note's A1 and A2-L take a scalar cost \(J\) as already defined (`theory/SELECTION_AXIOMS.md` §2). This note does not. The representation draft's A1–A8 produce an additive cost only after a complete preorder, expected currency, separability, concatenation, and a sign restriction are assumed. Those are special-case assumptions, catalogued in §5. They are not the starting point.

Four premises are used.

**S-W (exogenous world).** The law of the world does not depend on the design. This is representation A7 and the standing assumption of THEORY. The coupled case is CX2 and is open.

**S-Z (scores).** A design is scored by a finite vector \(z(\mathcal{D};W)\) of real bads, orientation smaller-is-better. \(Z_0(W)\) is the set of scores actually attained. Free disposal is the hull \(Z_0(W)+\mathbb{R}_+^n\), not a second compactness assumption. The hull is closed and unbounded. It is not compact: in \(\mathbb{R}^n\) no nonempty set is both compact and closed under adding an arbitrary positive vector.

**S-M (coordinatewise monotone retention).** If \(z\le z'\) and the two are not equal, the retention of the first is at least that of the second. The strict form S-M+ makes the inequality strict. S-M+ does not rank incomparable points. It is what remains of a growth exponent after every feature except the product order has been forgotten.

**S-P (persistence only).** A design is eliminated when a named scarce account hits a ruin set, and designs that do not hit it are not ranked against each other. This is the selection note's A2-P, restated without a scalar \(J\).

**H1–H3, the copying hypotheses used in the lemma.** H1: the environment is exogenous and ergodic, and a pure design's offspring \(W\) depends only on the design and the environment. H2: retention is the Lyapunov exponent \(\lambda=\mathbb{E}[\log W]\), and the expectation is finite. H3: for almost every environment, offspring is strictly decreasing in each coordinate of a chosen bad vector, and \(W>0\). H3 is a monotonicity hypothesis on offspring. It is the vector form of the selection note's A2-M, which that note already labels an axiom. The replicator equation does not supply H3.

## 3. Q1. What copying produces, and what an observer can identify

**Lemma LY (PROVED in-model, under H1–H3).** Let \(z\le z'\) with \(z\neq z'\). Then \(\lambda(z)>\lambda(z')\). Every maximizer of \(\lambda\) is Pareto in \(z\).

*Proof.* H3 gives \(W(z,\omega)\ge W(z',\omega)\) for almost every \(\omega\), and the inequality is strict on a set of positive probability: at least one coordinate is strictly smaller, and raising that coordinate strictly lowers offspring. The difference of the logarithms is therefore nonnegative and not almost surely zero. H2 makes the difference integrable. Its expectation is positive, so \(\lambda(z)>\lambda(z')\). A design that is strictly dominated then has a strictly smaller exponent than the design that dominates it, and cannot maximize \(\lambda\). □

On a nonempty compact design set, if \(\lambda\) is continuous, a maximizer exists and is Pareto. Finiteness of the design set is not required for the comparison. Continuity of the score, for compactness of the image, is F-0 below and is a separate hypothesis.

**Corollary LY-c (PROVED in-model, under H1–H2 and the stated map).** Suppose \(\log W=-\langle c(\omega),z\rangle\) with \(c(\omega)\ge 0\) almost surely and \(\mathbb{E}[c_i]>0\) for each charged coordinate. Then

\[
\lambda(z)=-\langle\mathbb{E}[c],z\rangle.
\]

Growth-rate selection minimizes a nonnegative linear cost in the chosen score. The selected object is one priced point, \(\arg\min\langle\mathbb{E}[c],z\rangle\). A nonnegative price selects a supported point. In the convex case every Pareto point is supported, so an observer who knows the signs and not the prices sees the front. Without convexity the price-selected set is only the supported subset: \(C=(0.6,0.6)\) is Pareto on \(\{A,B,C\}\) and no nonnegative inner product selects it (§5). The lineage, under this map, minimizes the linear cost. It does not sit on an unranked front.

*What this is, against V1, V2, and GF3.* The corollary is a route to a nonnegative linear cost. It is not V1. V1 starts from a complete preorder, risk-neutral expected currency, Debreu separability on at least three essential intervals, and concatenation; nonnegative prices are the further axiom A8. The corollary never uses those. The linearity is the linearity of the logarithm in a score that was already chosen. It does not choose the coordinates, and it does not produce a ruin cap. It is also not the master equation's objective. \(\lambda\) is an expected logarithm. V2 records that Kelly growth and expected currency have different argmins, and that the Lundberg exponent is a third argmin. A state-dependent \(c\) makes \(\lambda\) linear in \(z\) even when \(\lambda\) is not monotone in the vector of expected bads. The table below is that gap. So the corollary may look like a derivation of \(J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L\). It is a derivation of \(\langle\mathbb{E}[c],z\rangle\) in growth units, for a \(z\) supplied from outside. GF3's extra conditions, risk-neutral currency and the half-space cap, are still required before that linear cost is the master equation.

**Counterexample LY-1 (PROVED in-model; H1 and H2 hold, H3 fails for expected bads).** Two states, probability \(1/2\), i.i.d. Both designs use a constant resource and make a constant error.

| Design | Resource | Error | Offspring | \(\lambda=\mathbb{E}[\log W]\) |
|---|---|---|---|---|
| L | 1 | 0 | \(4\) and \(0.05\) | \(0.5\ln 0.2=-0.804718956\) |
| H | 2 | \(0.4\) | \(1.1\) and \(1.1\) | \(\ln 1.1=0.095310180\) |

The expected-bad vector of L is strictly smaller in both coordinates. The long-run growth of L is strictly smaller. S-M+ applied to \((\mathbb{E}[\text{resource}],\mathbb{E}[\text{error}])\) is false. Both offspring numbers are positive, so neither lineage is eliminated by persistence only. The state-contingent log-offspring vectors \((\ln 4,\ln 0.05)\) and \((\ln 1.1,\ln 1.1)\) are incomparable, and \(\lambda\) is monotone in each of those coordinates. S-M+ returns if the coordinates are the arguments of \(\lambda\). It does not return for the expected bads. This is the Jensen gap already in CT42, on a vector that looks like a bad vector and with both offspring numbers positive, so a ruin coordinate does not separate the designs. Recomputed in `tools/general_form_checks.py`.

**Counterexample LY-2 (PROVED in-model; H1 fails).** Bad vectors \(z_A=(1,1)\) and \(z_B=(2,2)\), so B is strictly dominated. Random matching, row payoff \(1\) for A against A, \(0\) for A against B, \(3\) for B against A, and \(0.5\) for B against B. At frequency \(x\) of B, \(f_A=1-x\) and \(f_B=3-2.5x\), so \(f_B-f_A=2-1.5x\ge 0.5\) on \([0,1]\). The replicator derivative of \(x\) is positive on \((0,1)\). The strictly dominated type goes to fixation. At \(x=0\) the invasion gap is \(2\).

**No frequency-independent scalar (PROVED in-model).** If A beats B, B beats C, and C beats A, each by a strict margin when the loser is common, no triple of numbers \(\lambda_A,\lambda_B,\lambda_C\) represents those invasions: a cycle of strict inequalities cannot hold among three reals. In that regime copying does not emit a complete preorder. The exogenous case H1–H2 does emit one, namely \(\lambda\). The two regimes are not the same theorem.

**Trichotomy (PROVED in-model, as a classification of what is known).**

1. *Known exponent.* Under H1–H2, copying emits the complete preorder \(\lambda\). The selected set is \(\arg\max\lambda\). It may be a single point.
2. *Monotonicity only.* Under H1–H3, \(\lambda\) satisfies S-M+. An observer who knows the values selects \(\arg\max\lambda\). An observer who knows only S-M+ cannot rule out a Pareto point: for each Pareto point \(z^\star\) the retention \(\lambda(z^\star)=0\) and \(\lambda(z)=-1-\sum_i\exp(z_i)\) for every other feasible \(z\) satisfies S-M+ and selects \(z^\star\). If \(a\le b\) and \(a\neq b\), the case \(b=z^\star\) does not arise, because \(z^\star\) is undominated; the case \(a=z^\star\) gives \(0>\lambda(b)\); if neither is \(z^\star\), the constant cancels and the exponential sum is strictly larger at \(b\). The front is the union of those argmax sets. It is an identified set. It is not proved to be the set one copying process occupies.
3. *Persistence only.* S-P produces the viable set, which is the viability kernel for a static design. It does not rank designs inside that set, and it does not produce the front.

**What is not proved.** That selection occupies the Pareto front. That claim is the second item read as an occupation statement rather than as an identification statement. Occupation of the front is not a theorem under H1–H3. H3 itself is not derived from copying.

The comparisons that follow are about S-M+ and S-P. They are not, by themselves, facts about a copying process.

**Theorem GF-1 (PROVED in-model, as geometry of those two relations).**

(i) *Existence, with a continuous score.* Let the design set be nonempty and compact, and let the score be continuous. Then \(Z_0\) is compact, as a continuous image, the sum of the coordinates attains its minimum, and that minimizer is Pareto. *Proof.* A continuous image of a compact set is compact, so the continuous sum attains its minimum. A point \(z\le z^\star\) with \(z\neq z^\star\) would have a strictly smaller sum. □ Without continuity the image need not be compact. On \([0,1]\), \(f(0)=0\) and \(f(x)=1/x\) for \(x>0\) has image \(\{0\}\cup[1,\infty)\). Lower semicontinuity of the sum, on a nonempty compact design set, is enough for that sum to attain its minimum. Compactness of the image, which free disposal uses, needs continuity of the score. This is F-0 in the merged representation note. It is not a second compactness assumption on the hull.

(ii) *Free disposal does not add efficient points.* If \(z=z_0+u\) with \(u\ge 0\) and \(u\neq 0\), then \(z_0\le z\) and \(z_0\neq z\), so \(z\) is not Pareto in the hull. A Pareto point of the hull is a Pareto point of \(Z_0\), and the waste vector is zero. Existence comes from (i), not from compactness of the hull. □

(iii) *Retention.* Under S-M+, on a finite design set, every design that maximizes retention is Pareto in the attainable scores. *Proof.* A strictly dominated design has a feasible alternative with a strictly higher retention rate, so it is not a maximizer. □ S-M without the strict inequality allows a dominated design to tie its dominator. The strict form is what puts the support of a unique maximizer on the front. Several incomparable Pareto points may tie. The theorem does not pick one of them.

(iv) *Persistence only is weaker.* Under S-P, the forced object is the viable set. It need not be the Pareto front. *Counterexample.* Scores \((e,\rho)=(1,0.2)\) and \((0.5,0.2)\). Both have ruin probability below 1, so neither is eliminated by S-P. The first is strictly dominated. □

(v) *A lexicographic order is stronger, and is not forced.* On \(\{(0,1),(1,0)\}\) both points are Pareto. The order "smaller second coordinate first, then smaller first coordinate" ranks \((1,0)\) strictly above \((0,1)\). A complete refinement is an extra assumption. The master equation's hard cap is a threshold form of that refinement: any violation of \(\rho\le\varepsilon\) is worse than any finite cost inside the cap. S-M does not produce the threshold.

(vi) *A viability kernel is the object under S-P, not under S-M.* Aubin's viability kernel is the set of states from which some design keeps the trajectory inside a constraint set (Aubin, *Viability Theory*, the edition Crossref returns under doi 10.1007/978-0-8176-4910-4, issued 2009). For a static design and a ruin constraint, that set is the viable set of (iv). It does not rank designs inside the set. It is not the Pareto front.

(vii) *A large-deviation rate is a complete scalar ranking, and is not forced.* Maximizing the Lundberg exponent \(\theta=2m/s^2\) orders designs completely. On a front with two incomparable points there is nothing in S-M that selects the design with the larger exponent. Section 5 shows that this argmax is not the argmin of expected currency cost.

**What Q1 concludes.** Under H1–H2 the output of copying is \(\arg\max\lambda\), a complete preorder. Under H1–H3 the same exponent is Pareto, and the front is what an observer can identify without the values. Under S-P the output is the viability kernel. S-M+ does not rank incomparable points, does not produce a ruin cap, and does not produce a lexicographic order or a Lundberg objective. Those last three are stronger complete rankings than the product order. They are not what H1–H2 withhold: H1–H2 already supply a complete ranking, and it is \(\lambda\), which need not be any of those three.

**FALSE, scoped.** "S-P forces the Pareto front" is false (the viable pair in (iv)). "S-M+ forces a ruin cap, a lexicographic order, or a Lundberg objective" is false ((v) and (vii)). "The viability kernel ranks designs inside the viable set" is false. "Exogenous growth selection emits a complete preorder" is the lemma's setting, not a falsehood: under H1–H2 it emits \(\lambda\). The same sentence is false once offspring depends on the frequencies of other designs (LY-2, and the cycle with no scalar). The unscoped sentence "selection alone forces a complete preorder" is not stamped false. It is true in one regime and false in the other.

## 4. Q2. Which coordinates a floor mentions

Two relations are easy to collapse, and they are not the same. A floor or the task can mention a slot. That constrains which scores are feasible. Retention decreases in a slot only under H3, a statement about \(\log W\). A floor is not that statement. Whether retention decreases in the slots named below is not proved. V5, the five-name front as a hypothesis about selected designs, stays **OPEN**.

**Mentioned by a floor or by the task. Not thereby a bad.**

1. *A task loss \(e\).* Judgment, in THEORY §1, is acting ahead of a world the system does not control. The loss at the moment of use is the task's distortion. Which loss (squared, 0–1, or another) is a modelling choice. Folding lateness into the loss is the identification THEORY §3 states ("a prediction that arrives after the moment to act buys nothing"). It is not a theorem that every late action is worthless.

2. *A memory resource, with the functional restricted by the domain.* In a stationary exogenous world, \(D\ge D_{\mathrm{IB}}(I_{\mathrm{mem}})\) (CT1, Theorem S1). The floor mentions a memory slot: feasible scores cannot fall below the curve. It does not say that retention decreases in memory. If memory is free, extra memory at the same loss is not dominated. The gross stock \(I(M_t;X^t)\), predictive information, and Still's \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\) are different functionals. Still, Sivak, Bell and Crooks (doi 10.1103/PhysRevLett.109.120604) bound dissipation by the nonpredictive part under their hypotheses. They do not force the gross stock to be the bad. On a Gaussian world whose variance diverges, every uniformly accurate design has \(I(M_t;X_t)\to\infty\) (PD6, already **PROVED**). The raw stock cannot be the viability coordinate there. A rate can. So "memory held," as a stock, is the slot the stationary floor mentions. Outside that domain the slot the divergence leaves open is an information rate. Neither sentence is H3. Calling one stock the coordinate on every world is **FALSE**. The sign of a Shannon coordinate is not free inside the characterization the representation note uses. Aczél, Forte and Ng characterize the nonnegative cone generated by the Shannon and Hartley entropies: nonnegative multiples, added. A negative multiple is not in that cone. \(-\!H\) fails subadditivity whenever \(H(X,Y)<H(X)+H(Y)\). A negative price has to sit on a different coordinate.

3. *An acquisition resource, as a floor.* Reads must pay at least the sequential rate–distortion rate of the accuracy reached (S1; Tatikonda, Sahai and Mitter, doi 10.1109/TAC.2004.834430). The drifting form is PD1a. The floor mentions an acquisition slot in the feasible set. It does not make that slot a bad: S-A (\(A\ge c\cdot r\)) is an assumption, not a sensor law (SHANNON). Which concatenating coordinate the price is linear in — per read, per nat, or per precision — is open (the representation draft's V4). The per-precision price \(c'r^{-\theta}\) is not linear in precision. That slot stays **OPEN**. This note does not close it.

4. *A ruin statistic.* S-P eliminates a design when a scarce account is exhausted, so that elimination rule has to read a hitting event. Growth-rate selection with \(W=0\) on ruin already has the event inside \(\lambda\), and a second ruin coordinate double-counts it. Whether the statistic is traded as a bad, imposed as a cap \(\rho\le\varepsilon\), or promoted to the objective (maximize \(\theta\)) is a modelling choice. The master equation makes the second choice. That choice is not H3.

**Not forced.**

5. *Attention, as a peer of the other four.* THEORY §3 lists attention as one name for the currency ("heat, attention, money, compute"). If memory, acquisition, error, and linking are already paid in attention, a fifth coordinate repeats the currency and the vector collapses toward a scalar. No selection premise and no information floor produces a simultaneous-processing capacity as a separate bad. A capacity limit, if one is measured, is a constraint on the feasible set, not a fifth summand. Putting attention on the five-name list as a peer is a modelling choice. As a derived coordinate it is **FALSE**.

6. *Layer count.* S1 charges no \(h\cdot 1[I>0]\). A memoryless read has \(K=0\) and can still carry information (the numerical example in SHANNON §2: \(J=2.197<3.187\) for a floor that illegally adds \(h\)). An extra layer that leaves \((I,r,e,\rho)\) unchanged is not dominated in those coordinates. Dominance of \(K\ge 2\) by \(K=1\) at the same error needs an extra monotonicity: the extra layer raises some bad (memory, acquisition, or a separate upkeep). That monotonicity is an assumption, not a consequence of the floors. **PROVED** as a conditional. The unconditional claim "the floors make \(K\) a bad" is **FALSE**.

7. *Linking.* A communication slot is mentioned only when more than one agent shares a resource and the communication consumes something the acquisition coordinate does not already count. Mention is not H3.

**The five-name list.** Memory held, information bought, error, attention, and ruin risk are not a derived list of bads. Error, a memory resource, an acquisition resource, and a ruin statistic are slots a floor or an elimination rule mentions, with the domain restriction on memory in (2). Mention is not monotonicity of retention. Attention is not a derived bad. Layer count is a bad only under the extra monotonicity in (6). Linking is a further slot when communication consumes a resource the acquisition coordinate does not count. V5 stays **OPEN**. This note does not change that row.

## 5. Q3. When the front collapses to additive linear \(J\)

**Theorem GF-3 (PROVED in-model).** The general form of §3–§4 reduces to a minimization of \(\langle p, z\rangle\) over \(\{z:\rho\le\varepsilon\}\), with \(p\ge 0\), exactly when all of the following hold.

**(R-a) Risk-neutral expected currency.** Preferences over lotteries satisfy the von Neumann–Morgenstern axioms and the index is affine in currency loss. Von Neumann–Morgenstern alone gives an expected utility, not expected cost. Logarithmic utility is a von Neumann–Morgenstern index. It is Kelly's criterion.

*Kelly is a different argmin.* CT42's shared shock: probability \(0.05\), calm factors \(a_1=1.30\) and \(b_1=1.05\), shock factor \(b_0=0.90\). The lineage weight on the robust design is \(q^\star=0.05\times 1.30/(1.30-1.05)=0.26\). The per-unit mean of the lean design is \(0.95\times 1.30=1.235\). The robust design's mean is \(0.95\times 1.05+0.05\times 0.90=1.0425\). Expected currency cost on that pair picks the pure lean design. The growth-rate criterion picks a mixture. Recomputed in `tools/general_form_checks.py`. This is the same arithmetic as `theory/DYNAMICS.md` CT42. It is not a new mechanism.

**(R-b) Ruin is a half-space cap, not a coordinate and not the objective.** The cap is the slice \(\rho\le\varepsilon\). A finite price on \(\rho\) is a different scalar: it trades ruin against the other bads at a finite rate. An infinite penalty on \((\rho-\varepsilon)_+\) is the cap, and it is the threshold lexicography of §3(v). Maximizing the Lundberg exponent drops expected currency.

*Lundberg is a different argmin.* On the published path of Lemma B9 (\(y=1\), \(c=0.05\), \(w=\sigma=1\), \(s_0=0.3\)), the cost is \(J(\tau)=c/\tau+\alpha\tau\) with \(\alpha=w\sigma^2/2=1/2\), so the expected-cost interval is \(\tau_E=\sqrt{c/\alpha}=\sqrt{0.1}=0.3162\). The variance rate is \(s^2=s_0^2+\beta\tau^3\) with \(\beta=w^2\sigma^4/3=1/3\), and \(\theta=2(y-J)/s^2\). The unique zero of \(\theta'\) on the positive-margin interval is \(\tau_S=0.2362\). The two designs differ. Recomputed here by bisection; the same published point is in `theory/meq_checks/meq_checks.py`. Agreement when the reserve's own noise dominates is a limit inside that model, not an identity of the two objectives (THEORY, the correction to Theorem L).

**(R-c) Linear nonnegative prices.** Two routes. They are not the same route.

*Convex route.* Let \(Z\) be convex and free-disposal, and let \(z^\star\) be Pareto. Then some \(p\ge 0\), \(p\neq 0\), has \(z^\star\) minimizing \(\langle p,z\rangle\) over \(Z\). *Proof.* \(Z-z^\star\) is convex and does not meet the open negative orthant. A separating hyperplane has nonnegative normal \(p\neq 0\). □ This is the argument SHANNON Theorem S3(ii) names. Debreu 1954 (doi 10.1073/pnas.40.7.588, "Valuation Equilibrium and Pareto Optimum") is the classical supporting-price theorem this argument is an instance of. Strictly positive prices on every coordinate are Geoffrion's proper efficiency (doi 10.1016/0022-247X(68)90201-1), not mere Pareto. This note does not re-prove Geoffrion's characterization. Part (i) of S3, that a minimizer at strictly positive prices is undominated, does not need convexity.

*Debreu route, without convexity of the image.* A continuous complete preorder on a product of at least three essential intervals, preferentially independent, has an additive representation \(\sum_i f_i\) up to one positive scale and one additive constant per coordinate (Debreu, "Topological methods in cardinal utility theory," reprint doi 10.1017/ccol052123736x.010; the year field came back empty). The \(f_i\) need not be linear. Constant marginal rates are a further assumption: concatenation, \(f(x+y)=f(x)+f(y)\) up to one constant, and monotonicity or continuity, give \(f(z)=pz+b\) (the monotone Cauchy equation). Nonnegative \(p\) needs each concatenating coordinate to be a bad. A negative error price satisfies additivity, concatenation, and expected currency. Layer count is discrete. The cited Debreu theorem is about interval factors. An integer count is linear by the integer Cauchy equation \(f(n)=nf(1)\), and it enters the same sum only under an extra separability assumption the citation does not prove. A two-coordinate problem is not an application of the \(n\ge 3\) theorem; the missing ingredient is the Thomsen condition, which this note does not assume.

The convex route needs convexity and produces linear prices directly. The Debreu route needs a complete preorder and separability, does not need convexity of the image, and produces linear prices only after concatenation. Neither route is a consequence of S-M.

Nonnegative prices are A8, not A1–A7. That is V1, as merged. On three interval coordinates the witness \(I+A-\mathbb{E}[\ell]\) satisfies A1–A7 and has a negative error price. Layer count is not one of those three intervals. The negative sign is on the loss. It is not a negative multiple of the memory entropy, which A6's nonnegative cone excludes.

**(R-d) What replaces the linear sum when a hypothesis fails.**

- *Separable but not concatenating:* \(C=\sum_i f_i(z_i)\). The marginal rate \(f_i'(z_i)\) depends on the level. The square \(f(z)=z^2\) is the one-line witness that additivity of the representation is not linearity: \((1+1)^2\neq 1^2+1^2\), and the derivative \(2z\) is not constant.
- *Nonconvex image:* a nonnegative weighted sum sees only the exposed face of the convex hull. The three-point set \(A=(0,1)\), \(B=(1,0)\), \(C=(0.6,0.6)\) has every point Pareto. For \(p\ge 0\) not both zero, \(C\) minimizes no such inner product. If \(p_1=0\), \(B\) scores 0 and \(C\) scores \(0.6p_2\). If \(p_2=0\), \(A\) wins the same way. If both are positive, \(C\) beating both \(A\) and \(B\) requires \(p_1/p_2\le 2/3\) and \(p_2/p_1\le 2/3\), which cannot hold together. The mixture \(\tfrac12 A+\tfrac12 B=(0.5,0.5)\) dominates \(C\). If mixtures are feasible, \(C\) is not on the front at all. The miss is the case where the dent stays feasible.
- *A strictly monotone ranking can select the dent. Unweighted Chebyshev cannot be that ranking.* \(\max(z_1,z_2)\) scores \(A\mapsto 1\), \(B\mapsto 1\), \(C\mapsto 0.6\), so \(C\) is its unique minimizer on the three points. The same function is only weakly monotone: \(\max(0.6,0.6)=\max(0.6,0.5)\). Moving the second coordinate down does not change the value, so unweighted Chebyshev is not an S-M+ retention. On \(\{A,B,C\}\) no pair is ordered by the product order, so every ranking satisfies S-M+ on that set. The retention \(r(C)=0\), \(r(A)=r(B)=-1\) satisfies S-M+ and selects \(C\). On a larger set the augmented score \(\max_i(z_i-z_i^\star)+\varepsilon\sum_i(z_i-z_i^\star)\) for small \(\varepsilon>0\) is strictly monotone and still selects a Pareto point the weighted sum misses. Zadeh (doi 10.1109/TAC.1963.1105511), Wierzbicki (doi 10.1007/978-3-642-48782-8_32), and Bowman (doi 10.1007/978-3-642-87563-2_5) are the scalarizations that reach unsupported points. The three-point arithmetic is re-derived here. Miettinen (*Nonlinear Multiobjective Optimization*, doi 10.1007/978-1-4615-5563-6; Crossref issued-year 1998) is the textbook account. None of this is claimed as new.
- *Kelly and Lundberg,* as in (R-a) and (R-b). A growth factor that multiplies across periods is optimized by a sum of logarithms, not by a sum of expected losses. That is why the mixture appears.

**(R-e) A coordinate cap preserves convexity. A constraint that is not a half-space in the scored coordinates need not.** If \(Z\) is convex and \(H=\{z:z_i\le\varepsilon\}\) is a closed half-space, then \(Z\cap H\) is convex, because a convex combination of points in both sets stays in both. The script checks 200 random combinations on a triangle cut by \(y\le 1\). What can fail is a chance constraint imposed on the design set before scoring. The dent \(\{A,B,C\}\) is not convex, its convex hull contains the mixture that dominates \(C\), and \(C\) stays Pareto only because that mixture is not a feasible score. S3's caveat is this case. The earlier claim that a plain cap \(\rho\le\varepsilon\) breaks convexity of a convex score set is **FALSE**.

**One currency.** Without it, (R-c) does not start: Debreu's scalar sum is already one index, and a supporting price is one index. Two incomparable objectives stay a front. That is the general form, not a failure of it.

**FALSE.** "Convexity is enough for the master equation." Convexity gives some nonnegative linear price at a Pareto point. It does not give risk neutrality, it does not give the cap rather than a finite price on ruin, and it does not choose the memory functional. "Separability is enough for linear prices" is also **FALSE**: separability gives \(\sum f_i\), and linearity is concatenation.

## 6. Q4. What survives, and the extra assumption each survivor needs

No new inequality is proved in this section. Each line is either the scope of a theorem already proved or the one-line dominance argument named with it. **PROVED (in-model)** as a scope list.

**Survives with no price, under S-M and the floors.**

| Result | What survives | Minimal extra assumption |
|---|---|---|
| Antitone front | In any pair of coordinates, with the others fixed, two Pareto points move against each other | The definition of Pareto. No additivity |
| Existence | A Pareto point exists | Continuous score on a nonempty compact design set (F-0) |
| CT1, S1, PD1a | The pair \((I,e)\) or \((r,e)\) cannot fall below the proved curve. They do not pick a point on it | Exogenous world; the loss the floor was proved for. Stationary for S1; a density for PD1a |
| CT8 | A staler reading is a garbling, so it cannot lower the best error at given other coordinates | Stationary Markov world, renewal checks, Blackwell (doi 10.1214/aoms/1177729032). False for non-Markov observations, as THEORY already says |
| CT25's buffer scaling | \(B\ge z_\varepsilon\sigma\tau^H\) is the shape of a per-window chance constraint | Self-similarity of the error. No price on the error. This is a constraint, not a traded bad |
| L3's inequality | \(E_K>E_\infty\) for every finite \(K\), on a non-rational spectrum | The spectrum. No price. "\(K^\star\to\infty\) as \(R\to\infty\)" needs the ratio \(R\) |
| Layer cap as dominance | \(K\) beyond the McMillan degree, or a second layer on one real pole, is dominated at the minimum-error end | The extra monotonicity of §4(6): the extra layer raises a bad. Without it, the cap does not survive |

Interlacing describes the error-minimizing filter at full degree. It is a fact about that end of the front. It does not say the system sits there.

**Needs a stake, a price ratio, or a scalar cost.** The minimal extra assumption is the whole of what is named. Dropping it is a counterexample, not a remark.

| Result | Minimal extra assumption | What fails without it |
|---|---|---|
| CT33 | A scalar \(J=S+wE\) on a menu that does not depend on \(w\) (ruin slack or absent). Single crossing in \((design, w)\). The five-term split inside \(S\) is not needed | An arbitrary pick from the front can raise error as \(w\) rises. On \(e=1/m\), the scalar minimizer \(m^\star=\sqrt{w}\) has falling error; the pick \(m=1/w\) has rising error. Checked in the script. Milgrom and Shannon (doi 10.2307/2951479) and Topkis (doi 10.1287/opre.26.2.305, title as Crossref gives it, "Minimizing a Submodular Function on a Lattice") are the monotone-selection tools. They need the parameter |
| CT20(ii), sensing fixed | The scalar \(hK+wE_K\), ruin slack | \(K^\star\) as a function of \(w/h\). With read rates chosen, \(K^\star\) can fall even in the scalar problem (THEORY B.9). That counterexample stays a fact about the scalar problem |
| \(K^\star(R)\), \(R^\star\), \(K^\star_0(R)\) | The ratio \(R=w E_\infty/h\). The from-0 count also needs the decrement hypotheses of N64 | The curve \(\varepsilon_K\) is a slice of the front. The count is the point the ratio picks |
| CT24 shares | Linear prices, a price-independent feasible set, differentiability | Euler. A binding ruin constraint is the existing counterexample (shares 0.528 and 0.472, elasticities summing to 1.147) |
| The ratio \((\alpha-1):1\) | CT12's single exact-read power-law tracker, on top of CT24 | Euler gives shares summing to 1 and does not give that ratio once read noise or further terms are present |
| \(d/(2\beta)\) | A scalar cardinal cost, A2-L, a quadratic well, whitened coordinates, and the scale fixed if \(\beta\) is held fixed. The fractional form also needs the zero fixed and \(J^\star>0\) | There is no quadratic well on a bare front. A homogeneous cost of degree \(p\) has Gibbs mean \(d/(p\beta)\); the Lean equipartition already records the general \(p\), and the quadratic case is \(p=2\). For \(J=x^4\) the one-dimensional mean is \(1/(4\beta)\), because \(\Gamma(5/4)/\Gamma(1/4)=1/4\), not \(1/(2\beta)\). Checked |
| CT22's multiplier \(\mu_s=-m'/\theta'\) | The scalar path, \(J''>0\) and \((s^2)''>0\) together, and \(\theta'\neq 0\) off the survival endpoint | Without a scalar cost there is no margin \(m=y-J\) and no multiplier. What survives with no prices is antitonicity of a pair \((cost,\rho)\) only after a scalar cost has been chosen |
| CT7, \(\sigma\sqrt{2kT\cdot w}\) | A price per nat in one random-walk model | It is not the master equation at an arbitrary price vector |
| CT12's elasticity \(1/\alpha\) | The ratio \(wq/c\) and the power-law plant | No ratio, no elasticity |
| \(T^\star=\sqrt{6k/(w\sigma^2)}\) | The ratio \(k/w\), zero discount, a Brownian gap, a lumpy reset | The lifetime is a priced band. The existence of a lump is prior art (Dixit, Chalkley) and is not a price-free lifetime |
| Sharing threshold \(N^\star(\rho)\) | A scalar cost in the class \(P(a,b)\), and the drift ratio \(\rho=q_g/q_u\) (THEORY, the setting of CT14: shared drift intensity over private drift intensity). At zero upkeep and equal prices the common price cancels, and for the square-root technology \(N^\star=(\sqrt{1+\rho}+1)^2/\rho\). The telling threshold \(d/c\) of CT16 is a different ratio | Without the scalar comparison there is no \(N^\star\). A sign about shared versus private drift still needs the drift ratio as a parameter. That parameter is not a price |

**CT42** is not a survivor of additive expected-cost \(J\). It is the Kelly scalarization, which the general form allows and the master equation's risk-neutral clause does not.

## 7. Q5. A prediction the additive cost does not make

A fitted antitone cloud is not a prediction of this form. Any strictly monotone tradeoff is antitone in the two traded coordinates. Shoval, Sheftel, Shinar, Hart, Ramote, Mayo, Dekel, Kavanagh and Alon (doi 10.1126/science.1217405) already read phenotype clouds as lying near a low-dimensional front. Farrell (doi 10.2307/2343100) and Debreu's coefficient of resource utilization (doi 10.2307/1906814) are the price-free efficiency facts. An antitone relation among observed traits, with no front computed from the world, does not discriminate this hypothesis from any tradeoff. The draft re-read on `frontier-reread-2026-11-22` reaches the same conclusion. It is used here as a draft, not as authority. Its package-registry candidate is an antitone test with a weak world split. It is not the prediction below, and this note does not adopt it.

**GF-P1 (OPEN; not a locked prediction).** A fitted antitone cloud is not evidence that a design sits on the achievable front. The arithmetic below shows that antitonicity does not see interiority to the information relaxation. It does not certify a miss of the achievable set. A miss of "on the achievable front" needs a dominating score that is achievable, or excess over a bound proved tight for the preregistered class. Excess over the relaxation is neither.

*Scalar Gauss–Markov relaxation, stationary, exogenous, squared error, lead \(k\).* World \(x_{t+1}=a x_t+n_t\), \(\mathrm{Var}\,n=Q\), \(\mathrm{Var}\,x=V=Q/(1-a^2)\). For a posterior variance \(P\),

\[
I\ge\tfrac12\ln(V/P),\qquad
r\ge\tfrac12\ln(a^2+Q/P),\qquad
D\ge a^{2k}P+V(1-a^{2k}).
\]

These are the curves S1 writes. They are a relaxation. SHANNON §3, on this same world, records efficiency \(J_{\mathrm{floor}}/J=0.9574\) when memory and reads are both priced, and leaves joint achievability **OPEN**. A point can lie strictly inside the relaxation and still be Pareto in a smaller achievable set.

*Rigid shift.* Let \(A=\{(I(P)+0.4,\, r(P)+0.4,\, D(P)):0<P\le V\}\). Every point of \(A\) lies \(0.4\) nats above both curves, so \(A\) sits inside the relaxation. \(A\) is a translate of the efficient curve, so no point of \(A\) dominates another. Strict excess over the relaxation is compatible with sitting on the achievable front, whenever that front is such a shift. The shift is what the open achievability gap leaves room for.

*Worked point, recomputed, as arithmetic only.* \(a=0.9\), \(Q=1\), \(k=2\), \(P=0.5\): \(V=5.263158\), \(I=1.176939\), \(r=0.516592\), \(D=2.138050\). The point \((I+0.4,\, r+0.4,\, D)\) is dominated by \((I,r,D)\) inside the relaxation. Along \(P\in\{0.3,0.5,0.8,1.2\}\), the cloud \((I(P)+0.4,\, D(P))\) is antitone, and every point lies \(0.4\) nats inside the memory curve. Antitonicity does not see that interiority. Neither fact is a rejection rule for an achievable design.

**What a later preregistration would have to fix. SKETCH, not a lock.** The loss, the memory functional, the lead, and the world class, fixed before the design's resources are computed. World parameters from a series the design does not choose, with an error budget. An estimator of the memory mutual information and of directed information, with a bias bound the margin has to clear: underestimating information manufactures interior points, and overestimating information manufactures points on the floor. Channel noise and store noise measured or excluded. A second task and a nonstationary world move the front. Qualification under THEORY §3 and the binomial allowance in THEORY §8 are not set here. GF5 stays a sketch until they are set, and the sketch does not treat excess over the relaxation as a miss.

Comparisons that additive expected-currency \(J\) does not share, each still a sketch: an unsupported feasible point, with mixtures infeasible, in a designed world (§5); a stake change that moves the operating point along one computed front, which CT33 predicts and an unranked front does not; two designs tied on every priced coordinate, both inside a slack cap, ranked by ruin, which additive \(J\) ties. None of these is locked.

**Two further separations, in-model only, not field predictions.**

- *Unsupported Pareto point.* On the dent of §5, every nonnegative additive \(J\) selects \(A\) or \(B\). The S-M+ retention \(r(C)=0\), \(r(A)=r(B)=-1\) selects \(C\). Observing \(C\), in a designed world whose only feasible scores are those three and whose mixtures are infeasible, would refute nonnegative additive \(J\). It would not refute S-M+. This is **PROVED** as arithmetic. It is not a field protocol.
- *Slack cap.* At equal scores on the priced coordinates, with both ruin probabilities under a slack cap, additive \(J\) ties the two designs. S-M with ruin as a bad ranks the lower ruin risk strictly higher. **PROVED** as a one-line comparison. It does not use a world-computed front, so it does not answer the distinctiveness demand by itself. Any theory that treats ruin as a bad makes the same ranking.

**FALSE.** "An antitone cloud of selected designs tests the general form." The worked cloud is the counterexample.

## 8. Prior art, and what is not claimed

Every DOI below was resolved on the Crossref API on 22 November 2026. A DOI is printed only when the returned title contains the work. The record is `theory/general_form_checks/crossref.out`. Reprints are marked when the year field came back empty.

Known, and not claimed as new:

- Pareto order; supporting prices for a Pareto point of a convex set (Debreu 1954, doi 10.1073/pnas.40.7.588); proper efficiency and strictly positive weights (Geoffrion 1968, doi 10.1016/0022-247X(68)90201-1); weighted sums missing nonconvex parts, and Tchebycheff or reference-point scalarizations reaching them (Zadeh 1963, doi 10.1109/TAC.1963.1105511; Bowman 1976, doi 10.1007/978-3-642-87563-2_5; Wierzbicki 1980, doi 10.1007/978-3-642-48782-8_32; Miettinen, doi 10.1007/978-1-4615-5563-6).
- A continuous numerical representation of a complete continuous preorder (Debreu, "Representation of a preference ordering by a numerical function," reprint doi 10.1017/ccol052123736x.007; year field empty) and the additive representation on a product (Debreu, "Topological methods in cardinal utility theory," reprint doi 10.1017/ccol052123736x.010; year field empty).
- Technical efficiency and the coefficient of resource utilization (Farrell 1957, doi 10.2307/2343100; Debreu 1951, doi 10.2307/1906814). Phenotype fronts as evidence of tradeoffs (Shoval et al. 2012, doi 10.1126/science.1217405).
- Kelly 1956 (doi 10.1002/j.1538-7305.1956.tb03809.x); Still et al. 2012 (doi 10.1103/PhysRevLett.109.120604); Landauer 1961 (doi 10.1147/rd.53.0183); Sagawa and Ueda 2009 (doi 10.1103/PhysRevLett.102.250602), who bound measurement and erasure together and do not license a second price stacked on that bound (SHANNON already refuses the stacking).
- The viability kernel (Aubin, doi 10.1007/978-0-8176-4910-4, issued 2009). The Lundberg exponent, as THEORY already uses it. Sella and Hirsh 2005 (doi 10.1073/pnas.0501865102) for the stationary weight. The excess \(d/(2\beta)\) is prior art in the quadratic case (CLAIM_MAP R1).
- Rate-distortion floors and the causal rate (Tatikonda, Sahai and Mitter 2004, doi 10.1109/TAC.2004.834430), already S1 and PD1.
- Monotone comparative statics (Milgrom and Shannon 1994, doi 10.2307/2951479; Topkis 1978, doi 10.1287/opre.26.2.305). Blackwell 1953 (doi 10.1214/aoms/1177729032).

Already in this repository, and not presented as new: SHANNON S2–S3 for the vector \((I,r,K,D)\); CORE's technical/allocative split; CT33, CT24, CT20, CT22, CT42; PD6's failure of the raw stock; the selection note's refusal to derive the term list from A1–A3.

**What this note adds, as packaging, not as a new theorem of multiobjective optimization.** The Lyapunov comparison under H1–H3, the log-linear corollary and its limit against V1 and V2, and the two counterexamples that separate expected bads from growth. The trichotomy: a known exponent, an identified front, and the viability kernel. The split between a floor that mentions a slot and H3, which is a map into \(\log W\). The exact extra assumption for each named theorem, with \(N^\star\) charged to the drift ratio \(\rho=q_g/q_u\). The warning that an antitone cloud, and excess over an unattainable relaxation, are not a miss of the achievable front. V5 stays the open field claim. Lemma LY does not promote it.

A hostile reading that calls the geometry textbook material is right about the geometry. The packaging is the claim. It is not a derivation of additive \(J\) from persistence, and it is not a field result.

## 9. What this does not show

- It does not make the hypothesis a physical law.
- It does not replace THEORY §3's equation or the operational definition of strongly selected.
- It does not show that any real offspring map satisfies H3. The lemma is conditional on that hypothesis. Occupation of the front is not a theorem.
- It does not show that a system on the information relaxation is on the achievable front. Joint achievability with both prices positive stays **OPEN**, as SHANNON §3 left it.
- It does not test layers. The floors do not charge \(K\).
- It does not close V4, CX1, or CX2.
- It does not re-score a locked preregistration. The frontier re-read's inventory is not adopted as a result.

## 10. Checks

`tools/general_form_checks.py`, run by `tools/test_general_form_checks.py`. **NUMERICAL** as a check of algebra that is proved in the text: the dent, the weak monotonicity of unweighted Chebyshev, the S-M+ ranking that selects \(C\), the mixture, the coordinate-cap combinations, Kelly's \(0.26\), \(1.235\) and \(1.0425\), Lundberg's \(0.2362\) and \(0.3162\), the quartic factor \(1/4\), the L/H growth gap, the frequency-dependent invasion gap, the Gauss–Markov point, and the antitone cloud inside the relaxation. Crossref output, when refreshed with `--crossref`, is `theory/general_form_checks/crossref.out`. The committed copy is the resolution of 22 November 2026.

The Part 2 hypothesis sentence is the sentence in §0. It is byte-identical to the sentence in THEORY §3 and in CORE.
