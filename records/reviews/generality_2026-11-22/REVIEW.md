# Review of draft PR #209

**Verdict: NEEDS-FIXES.**

Hostile reading and blind recomputation of `generality-audit-2026-11-22` at `9a5c8c1`, before the merge of `main`. This file edits the audit only by the fixes listed below. It does not edit `THEORY.md` and it does not merge the pull request. No lake build. Recomputation at nice 19. NumPy 2.5.5, SciPy 1.18.1, SymPy 1.14.0.

The hypothesis sentence is unchanged, byte for byte:

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

## What holds

**Representation.** Theorem R1, under A1–A7, on at least three essential intervals, with closed contour sets, concatenation, and finite-law Shannon information in the scope of A6, gives \(C=a(\sum_i p_i z_i)+b\) with one \(a>0\). Nonnegative prices are A8. The term \(hK\) needs the extra separability assumption, and ruin stays a constraint. Debreu's Crossref year is empty at doi 10.1017/ccol052123736x.010. The von Neumann–Morgenstern record is the 2007 edition, doi 10.1515/9781400829460. A differential mutual information is the extension A6 already names. The draft's §3 omitted that scope.

**Stake monotonicity.** For \(J=S+wE\) on a menu that does not depend on \(w\), with ruin slack or absent, the two optimality inequalities give \(E(w_2)\le E(w_1)\) and \(S(w_1)\le S(w_2)\) whenever \(w_1<w_2\), for every minimizer at each stake. The draft's §3 did not name \(S+wE\).

**Undominated minimizers.** A minimizer of a linear cost at strictly positive prices is undominated in the coordinates those prices charge: a distinct point that is smaller in the product order would have a strictly smaller inner product. Free disposal and convexity are not used. No Gaussian step is used. Part (ii) of Theorem F1, the converse, does use convexity. The draft's sentence did not say the cost is linear or which coordinates are charged.

**Boundary screening.** If the joint is \(f(x_R,x_B)\,g(x_E,x_B)\) with respect to a product measure, then \(X_R\perp X_E\mid X_B\). Positivity is not required for this direction. Besag (1974), doi 10.1111/j.2517-6161.1974.tb00999.x, is the other direction, and the note does not use it. The exterior expected loss is a function of the blanket posterior only when the loss depends on the world through the exterior and the decision is a function of the screened side. The draft's §3 skipped that clause. The path-of-three pair \(3/5\) and \(1/2\) was attached to the identity. The identity is \(1/2=1/2\). The value \(3/5\) is the variance given the region alone.

**Bipartite bath.** In steady state, with the boundary terms gone, EQ-heat gives \(\mathrm{Sr}_M\ge\dot I_M\). With mobility 1 and \(kT=D_M\), the energy flow into the memory bath is \(D_M\,\mathrm{Sr}_M\ge kT\,\dot I_M\). JP-heat, at \(kT=1\), is \(\dot Q=\sigma_M+I_{\mathrm{alt}}\ge I_{\mathrm{alt}}\) from local detailed balance and the pair term \((a-b)\ln(a/b)\). Restoring \(kT\) multiplies the right-hand side. Neither identity is \(a(v-\varepsilon)/\varepsilon\). Horowitz and Esposito (2014), doi 10.1103/PhysRevX.4.031015, are the jump split. Lemma D, now on `main`, is the diffusion split. The rerun gives \(\dot Q=1.13180408\), \(\sigma_M=0.43682545\), \(I_{\mathrm{alt}}=0.69497863\).

**One-dimensional learning rate.** For an exogenous equilibrium diffusion, \(L=D(\mathbb{E}[F]-\mathcal I(p_X))\ge D(1/\varepsilon-\mathcal I(p_X))\), with \(F(m)\ge 1/\mathrm{Var}(X\mid m)\) by Cauchy–Schwarz and \(s\mapsto 1/s\) convex. Equality with \(a(v-\varepsilon)/\varepsilon\) needs a Gaussian conditional of constant variance, a Gaussian marginal, and \(D=av\). The draft's §3 wrote the lower bound as the replacement for the rate. On the quartic, the rerun matches the printed digits: \(\mathcal I=2.027935\), \(1/v=1.479338\), \(L=1.395822\), bound \(1.010946\), and \(D(1/\varepsilon-1/v)=1.559543\).

**Jensen.** A finite convex \(\varphi\) with finite mean satisfies \(\mathbb{E}[\varphi(X)]\ge\varphi(\mathbb{E}[X])\) by a supporting line. A cap can reverse it: mass \(1/2\) on \(0\) and \(4\), \(\mathbb{E}[\min(X^2,1)]=1/2<1=\min((\mathbb{E} X)^2,1)\). The heavy-tail run matches the note: \(5.063876\) against \(2.579402\), second moment \(29.5050\), mean \(0.8808\), squared mean \(0.776\).

**Additive drift at \(b=0\).** If the control enters only as \(b\,u\,\partial_x\) and the martingale problem for \(G_0\) is unique, the law at \(b=0\) is the law of \(G_0\). The draft's §3 omitted uniqueness. The identity does not produce the five-term sum. The birth-death mean \(0.622433\) at \(b=1\), \(u=1\) is the Gibbs mean of \(x^4/4-x\) on the same grid.

**Citations.** All thirteen DOIs returned a Crossref work record on 23 November 2026. Titles match the note. Debreu's year field is empty. Shannon's reprint is year 2009 with an empty author list, doi 10.1109/9780470544242.ch1. von Neumann–Morgenstern is the 2007 edition.

**The one A row that was class-specific in part.** Theorem R2's Kelly half does not use a Gaussian step. The claim that the Lundberg argmin differs from the expected-cost argmin is the pair \(0.2362\) and \(0.3162\) on the scalar diffusion path. The draft said that separation does not use the numbers.

## T47

The draft says PR #203 was open and that T47 is not on `main`. `origin/main` is `ddba436` ("Point STATUS at the #201 pointer and record the #203 merge"). The merge of PR #203 is `3a364d8`. T47 is the acting-derivation row. The proposal diff is not applied.

Corrected rows, in place of the single "not on main" row:

| Result | Class | Assumptions | Class-specific step |
|---|---|---|---|
| R1′ | A | A1–A6 and A7′; at least three essential intervals; closed contour sets; concatenation; finite-law Shannon information in the scope of A6. Nonnegative prices need A8. The term \(hK\) needs the extra separability assumption. At \(b=0\) the effort coordinate is absent and the law is exogenous, so the cost is Theorem R1's five-term equation, each term kept, before minimization | None for the additive form. The drift does not produce the sum. GN-zero is the generator half of the reduction |
| Lemma D | A | Bipartite additive noise, smooth drift, vanishing boundary terms; steady state for \(\Sigma=\mathrm{Sr}-\dot I\) | None. EQ-heat is the memory coordinate of this identity, with the marginal-entropy term kept |
| Corollary LG, LG-0, LG-K | C | Linear bipartite diffusion, Lyapunov equation | The closed bath rates and the gain comparison |
| T47, cubic ordering | conjecture | The preregistered grid on the cubic plant. Not a theorem | GN-zero and Lemma LG do not decide it. The continuous gains are \(K_E=0.2327\) and \(K_H=0\). The locked grid difference \(0.25\) is one step of that grid |

## Paste-ready fixes

Applied on this branch after the merge.

1. Header date and status. Replace the Sunday sentence and the "not merged" sentence with:

*Monday 23 November 2026. An audit of the proofs on `main`, including the acting-derivation note merged with PR #203. This note does not edit `THEORY.md`. The master equation is unchanged. The hypothesis sentence is unchanged:*

and

*PR #203 is merged on `main` at `ddba436` (merge `3a364d8`). T47 is the acting-derivation row. The proposal diff is not applied. The generator question is answered below and is not an adoption into `THEORY.md`.*

23 November 2026 is a Monday. The hypothesis sentence is not part of either replacement.

2. Section 0, the EQ-learn sentences. State that the Fisher information replaces the lower bound, that \(D=av\) and \(\mathcal I(p_X)=1/v\) are the special case of that bound, and that equality of the learning rate with \(a(v-\varepsilon)/\varepsilon\) also needs a Gaussian conditional of constant variance.

3. Section 1.4. Replace the path-of-three sentence with: on the path of three the screening identity evaluates to \(\mathrm{Var}(X_E\mid X_B)=\mathrm{Var}(X_E\mid X_R,X_B)=1/2\). The variance given the region alone is \(3/5\). Those two numbers are the Gaussian calculation. They are not the identity.

4. Section 1.7. Corollary LG and Corollary LG-K are on `main`, the cubic ordering stays a conjecture, and recording the class is not an adoption into `THEORY.md`.

5. Section 3. Add the finite-law scope of A6. Name \(S+wE\). Say a minimizer of a linear cost at strictly positive prices is undominated in the coordinates those prices charge. Split the blanket sentence so the expected loss is a function of the blanket posterior only when the loss depends on the exterior and the decision is a function of the screened side. Split the learning sentence: the rate equals \(D(\mathbb{E}[F]-\mathcal I(p_X))\) and is at least \(D(1/\varepsilon-\mathcal I(p_X))\), with equality to \(a(v-\varepsilon)/\varepsilon\) only under the EQ-learn row's further assumptions. Add uniqueness of the martingale problem to the \(b=0\) sentence. Leave the closed-heat sentence and the hypothesis sentence as they stand.

6. Table. On the EQ-heat row, say Lemma D is the same split. Replace the Theorem R2 row with the Kelly / Lundberg split above. Replace the R1′ and T47 row with the four rows above.

## Checks

`theory/generality_checks/generality_checks.py` at nice 19: FAILS 0. The printed quartic, chain, heavy-tail, cap, and birth-death digits match this run, including the mean \(0.622433\).

`reviews/generality_2026-11-22/spotcheck.py` does not import that file. The quartic moments from \(\Gamma\) and from an infinite quadrature agree: \(v=0.6759782401\), \(\mathcal I=2.0279347202\). A Laplace channel on the same prior, centers \((-1.2,0,1.2)\) and scale \(0.9\), has score moments \(-1\), learning rate \(0.909110\) against current \(0.909109\), bound \(0.145078\), and Ornstein–Uhlenbeck-style value \(0.693675\). The conditional Fisher numbers sit strictly above \(1/\mathrm{Var}\). On masses \(0.7,0.2,0.1\) at \(0,1,8\), \(\mathbb{E}[e^{X/4}]=1.695711\) and \(e^{(\mathbb{E} X)/4}=1.284025\). The Gibbs measure of \(x^4/4-bux\) is the same at \(b=0\) for \(u=0\) and \(u=5\), and its mean at \(b=1\), \(u=1\) is \(0.622433\).

On the tree after the merge and these edits, at nice 19: `check_consistency.py` reports FAIL: 0 and exits 0; `check_open_work.py` reports union missing from `OPEN_WORK.md` is 0 and exits 0; `pytest -q tools` reports 263 tests and 1 skipped, and exits 0. The extra test, relative to the draft's 262, is the acting-derivation check that arrived with `ddba436`. No lake build.
