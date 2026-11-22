# Proposal: the cost when the action enters the world

*Sunday 22 November 2026. A proposal, not an adoption. `THEORY.md` is not edited. The master equation in THEORY §3 is not edited. The hypothesis sentence is not edited. The acting-loop preregistration is not edited. The scalar identities this file uses are the ones checked in `theory/acting_loop_checks/acting_loop_checks.py`.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

Labels on each step: **PROVED** (the argument is on this page, in the class named with it), **STANDARD** (a cited theorem, or a theorem already proved in this repository, used only for what it states), **CONJECTURE** (named, not proved).

## 0. What the repository already uses

The master equation is a definition of the problem, not a theorem. THEORY §3 says so. `theory/REPRESENTATION.md` states the assumptions under which an additive cost represents the preorder, and it states what those assumptions do not force.

**A1–A7, Theorem R1. STANDARD.** Under a continuous complete preorder, expected cost under risk, separability across at least three essential interval coordinates, one currency, concatenation, Shannon information in the scope of the citation, and an exogenous world, every continuous cost representing the preorder is a positive affine image of a sum of coordinate prices. This is Theorem R1 of `theory/REPRESENTATION.md`. It is not re-proved here. Debreu's theorem is the cited step in that proof.

**A8. STANDARD.** Nonnegative prices are the further assumption that each concatenating coordinate is a bad. Theorem R1 without A8 allows a negative price. The master equation's nonnegative \(\kappa\), \(h\), and \(w\) use A8.

**Ruin. STANDARD.** The constraint \(P(\mathrm{ruin})\le\varepsilon_r\) is the feasibility restriction in A2 of that note. It is not a summand. Von Neumann–Morgenstern risk neutrality makes the objective an expected cost. It does not produce the cap.

**A7, the exogenous world. STANDARD, and the clause this proposal relaxes.** A7 says the law of the world does not depend on the design. THEORY §3 records the same restriction: effort spent making the world drift less is the open lever, and every theorem below that sentence holds the world fixed. The night-1 formal file's Axiom 5 is the earlier one-budget statement of the same additive cost. It is not a second derivation.

**Heat. STANDARD as a bound, not as the cost.** Horowitz and Esposito, doi 10.1103/PhysRevX.4.031015, give the shape \(\dot Q\ge kT\) times the learning rate for a bipartite stationary system. The repository already uses that shape. Attainment of the floor by a finite-rate linear spring, for an exogenous equilibrium Ornstein–Uhlenbeck signal and a mean-squared decision loss, is proved in `theory/INFO_PHYSICS_ATTAINABILITY.md`. That attainment is not re-proved here, and it is not proved there for a signal whose drift depends on the estimate.

**Limited fragile parts. Assumption, already used as a feasible-set restriction.** A part that holds at most a finite precision, and that fails, is the restriction scored in the holographic-memory note and in the turnover draft. It cuts the set of designs. It does not, by itself, add a term to the sum. This proposal keeps that use.

Storing, predicting, acting, and staying solvent do not force the additive form. That negative statement is Theorem R1's companion in `theory/REPRESENTATION.md`, and it stays.

## 1. The one new assumption

**A7-act.** The state that the loss scores obeys
\[
dX=-aX\,dt+b u_a\,dt+\sqrt{2a\theta}\,dW,
\]
with \(b\) allowed to be positive, and with \(u_a\) a function of the design. Observation, when it is bought, is the fixed-noise channel \(dY=X\,dt+u_o^{-1/2}\,dV\).

A7-act is the replacement of A7 inside this proposal. At \(b=0\) it is A7. Nothing else in A1–A6 or A8 is changed. Preferential independence, concatenation, one currency, and nonnegative prices are statements about the cost of the resource vector. They are not statements about whether the map from the design to that vector depends on a controlled drift.

## 2. The extended cost

**Proposal AL-J. CONJECTURE as an adoption, PROVED as an accounting identity inside class AL.** Write the resource coordinates as the heat charged for the conditional, the expected loss, the probe price, and the actuation price. In the scalar class of the acting-loop note, with layer upkeep and the link term set to zero,
\[
J=Q+\alpha u_o+\rho\,\mathbb{E}[u_a^2]+q\,\mathbb{E}[X^2],
\]
subject to \(P(q X^2>B)\le\varepsilon_r\), where the heat is
\[
Q=kT\,L+\gamma_1\theta
\]
and, when the finite-rate factor is charged, \(kT\,L\) is replaced by the shrunk-spring expression at a frozen memory rate. \(L=a(\theta/p-1)\) is the learning rate of the Kalman conditional. The law of \(X\) depends on \(u_a\) through A7-act, so \(v=\mathbb{E}[X^2]\) depends on the gain.

The additive shape is R1's shape, with the memory coordinate priced at the heat rather than at \(\kappa I_{\mathrm{mem}}\). **STANDARD** that the floor sits under the heat. **CONJECTURE** that the price to charge is the floor plus the frozen gap, for a plant whose drift depends on the estimate: the attainment proof does not cover that plant. **PROVED** that, once those coordinates are the ones being summed, the scalar expression above is the sum. The gap \(\gamma_1\theta\) and the finite-rate factor are frozen in the preregistration. They are not derived from A1–A8.

A fragile part enters as a restriction of the same set. If its failure time is independent of \(X\) given its quality, the conditional law of \(X\) does not change. That is already proved in the acting-memory note. If the failure intensity is \(\lambda(x)=\lambda_0+\beta x^2\), the failure is an observation. At the frozen Cox point the posterior variance is \(1/2\) against a prior variance \(1\). That comparison is **PROVED (in-model)** in the acting-loop note. The price of the observation is the loss of the part. This proposal books that price inside the acquisition coordinate. It does not add a new summand.

## 3. Reduction at \(b=0\)

**Proposition AL-reduce (PROVED, in class AL, for the quadratic regulation cost).** Set \(b=0\). Then for every gain \(K\) and every error variance \(p\in(0,\theta]\),
\[
\mathbb{E}[X^2]=\theta.
\]
The actuation price \(\rho K^2 s\) with \(s=\theta-p\) is zero at \(K=0\) and positive at \(K>0\). The minimizer over \(K\) is \(K=0\), and the actuation price at the minimum is \(0\). The error variance is the exogenous Riccati, because the action has already cancelled out of the error equation for every \(b\), including zero. The cost at that minimum is
\[
J=kT\,L+\gamma_1\theta+\alpha u_o+q\theta
\]
when the floor is charged, and \(u_o=0\) minimizes it over intensities whenever \(kT\,L+\alpha u_o>0\) for every \(u_o>0\), which is the case at the frozen positive prices. Then
\[
J=q\theta+\gamma_1\theta.
\]
At \(\gamma_1=0\) this is \(q\,\mathbb{E}[X^2]\).

*Proof.* Substitute \(b=0\) into \(v=p+a(\theta-p)/(a+bK)\). The second term is \(\theta-p\), so \(v=\theta\). The derivative of \(\rho K^2(\theta-p)\) in \(K\) is \(2\rho K(\theta-p)\), which is zero at \(K=0\) and positive for \(K>0\). The checks evaluate \(v=1\) at \(b=0\), \(p=1/2\), \(\theta=1\), and an arbitrary gain. The Riccati has no \(b\) in it. The channel cost \(kT\,L+\alpha u_o\) is nonnegative and zero only at \(u_o=0\). ∎

**Corollary.** At \(b=0\), \(\gamma_1=0\), and the minimizing design, \(J\) is the stake term of the master equation. Restoring a priced observation that the loss can use, as the acting-memory note does for the sign loss, puts the probe price where the read term stands and the heat where the memory term stands, with layer upkeep and the link term zero. That is the master equation in this scalar class, on an exogenous world. The world law no longer depends on the design, which is A7 again.

The corollary is **PROVED** as a specialization of the sum. It is not a proof that every coordinate of the master equation is forced. Theorem R1 already says the additive form needs A1–A8, and that storing, predicting, acting, and staying solvent do not force it.

## 4. What stays a conjecture

- Charging the controlled plant at the exogenous heat floor plus a gap that increases in \(\theta\). The floor is a bound. Equality under feedback is not proved.
- Adopting AL-J in place of the equation in THEORY. This file does not do that.
- The synthesis in the acting-loop note, §8: layers, shared stores, boundary screening, and turnover, as the minimum of this one cost under limited fragile parts. The acting identities and the reduction in §3 are proved. The unification is not.
- The hypothesis sentence. It is unchanged, and it is still a bet.

## 5. What this file does not do

It does not edit `THEORY.md`, `CORE.md`, `README.md`, or the hypothesis sentence. It does not replace the master equation. It does not re-prove Theorem R1, the heat floor, or the acting-memory sign cost.
