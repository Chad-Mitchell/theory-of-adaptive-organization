# The cost when the action enters the drift

*Sunday 22 November 2026. A derivation, not an adoption. `THEORY.md` is not edited. The hypothesis sentence is not edited. This note does not touch the acting-loop draft or its review.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

Labels: **PROVED HERE** (the argument is on this page), **STANDARD** (a cited theorem, or a lemma already proved in this repository, used only for what it states), **CONJECTURE** (named, not proved).

`theory/SELECTION_AXIOMS.md` uses a different A1–A3 (persistence, copying, drift of the optimum). Night-1 Axiom 7 is near-minimization. Neither is the A7 below. The A1–A8 of this note are the axioms of `theory/REPRESENTATION.md`.

## 0. What is proved

**A7 is replaced by A7′.** A1–A6 and A8 are unchanged as statements. A3 is applied to the product A7′ names.

**Theorem R1′** is the additive cost under A1–A6 and A7′. At feedback strength \(b=0\) it is Theorem R1's cost. With A8 and the same extra separability assumption on the integer layer count, that cost is the five-term master equation of THEORY §3, each term kept, before any minimization.

**In the linear bipartite diffusion LG-b,** the bath heats and the information flows are computed from the Fokker–Planck current. At \(b=0\) the world's bath heat is 0 and the memory's information flow equals the exogenous Gaussian learning rate. For \(b\neq 0\) both heats depend on the gain. The uncontrolled spring heat is not the heat of the controlled loop.

The ordering of two gains on a cubic plant is a **CONJECTURE**. It is the preregistered test. It is not a corollary that has been proved.

## 1. Axiom A7′

**A7′ (the action may enter the drift).** A design \(\mathcal{D}\) includes a feedback rule \(u\). The world \(X\) and the memory \(M\) are one bipartite process. There is a strength \(b\) such that the drift of \(X\) is \(F_0(X)+b\,u\), and the diffusion coefficient of \(X\) does not depend on \(u\). The design induces one law \(P^{b,u}\). The resource coordinates and the loss lottery are computed under that law. When \(b\neq 0\), the effort of the feedback is a coordinate \(z_u\) of the product to which A3 and A5 apply.

**The case \(b=0\) is A7.** The drift of \(X\) does not depend on the design, so \(P^{0,u}\) does not depend on \(u\). The effort of changing the drift is not a coordinate. Both clauses of A7 in `theory/REPRESENTATION.md` are this case, and neither is weakened inside it.

A1–A6 and A8 keep the wording in that note. What changes is the product A3 sees: it includes \(z_u\) if and only if \(b\neq 0\). Preferential independence of \(z_u\) is that axiom applied to the new factor. It is not derived from the dynamics. If effort is disliked only because it changes the loss, it is not a separate coordinate, and Theorem R1′ does not add a price for it.

## 2. Theorem R1′

**Theorem R1′ (PROVED HERE, from A1–A6 and A7′, by the steps marked).** Restrict Debreu's step to a product of at least three essential intervals, with closed contour sets. A continuous cost representing the preorder has the form

\[
C=a\Bigl(\sum_i p_i z_i\Bigr)+c,\qquad a>0,
\]

with each \(z_i\) evaluated under \(P^{b,u}\). The prices are not signed by A1–A6 and A7′. When \(b\neq 0\) the sum includes the effort coordinate. When \(b=0\) the coordinate list and the law are those of A7, and \(C\) is the cost in Theorem R1.

Assume A8 as well, unchanged. Then each price on a concatenating coordinate is nonnegative.

The integer layer count is still not a Debreu factor. Under concatenation of nonnegative integer counts, Lemma C\(_\mathbb{Z}\) of the representation note gives \(hK\). Putting \(hK\) in the same sum still assumes preferential independence of \(K\) from the interval factors. That assumption is extra. It is not Debreu's theorem. The ruin constraint remains the feasibility restriction in A2. It is not a summand.

**Reduction (PROVED HERE).** At \(b=0\),

\[
J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L,
\]

subject to \(P(\mathrm{ruin})\le\varepsilon_r\). This is the master equation in THEORY §3. The equality is of the cost as a function of the design. It is not the value at a minimizer. None of the five terms is removed by minimization, and the effort coordinate is absent because A7′ says it is absent, not because an optimum set it to zero.

*Proof.*

1. **PROVED HERE.** By A7′ the design induces one law \(P^{b,u}\), hence one loss lottery and one resource vector. At \(b=0\) the law does not depend on \(u\).

2. **STANDARD.** Von Neumann and Morgenstern, *Theory of Games and Economic Behavior*, 60th Anniversary edition, doi 10.1515/9781400829460 (Crossref: 2007, that edition). Risk neutrality, as in A2 and in step 1 of Theorem R1, makes the ranking the expected currency cost. The freedom at this step is one positive affine regraduation. The controlled law changes which lottery a design induces. It does not change the theorem that ranks lotteries.

3. **STANDARD.** Debreu, "Topological methods in cardinal utility theory," doi 10.1017/ccol052123736x.010. Crossref returns the title and the author and an empty year field, as the representation note recorded; re-checked 22 November 2026. On at least three essential intervals with closed contour sets, the cost is a sum of continuous functions of the factors, unique up to one common \(a>0\) and constants. The same limit on two intervals stands: R1′ is not claimed when fewer than three interval coordinates are essential. \(K\) is not a factor in this step. \(z_u\) is a factor only when \(b\neq 0\).

4. **STANDARD.** Lemmas C and P of `theory/REPRESENTATION.md`: a continuous or monotone solution of the concatenation equation is linear, of either sign. Applied to each concatenating interval coordinate, including \(z_u\) when \(b\neq 0\). Lemma C\(_\mathbb{Z}\) gives \(hK\). Lemma M, which uses A8, signs the prices. None of these lemmas is re-proved here.

5. **STANDARD.** A6, in the scope the representation note states. Finite-law Shannon mutual information is covered. A differential mutual information of a Gaussian plant is the extension that note already names. It is not a new theorem. A6 still does not choose among stock, predictive information, and directed information. This note keeps the coordinate \(I_{\mathrm{mem}}\) the master equation writes. It does not derive that choice.

6. **PROVED HERE.** The currency scale and Debreu's scale are the same \(a\), for the same reason as step 6 of Theorem R1: the cost is already the von Neumann–Morgenstern index. At \(b=0\), step 1 removes \(z_u\) and freezes the law, so the sum is Theorem R1's sum. A8 signs \(\kappa,h,w\) and the acquisition and link prices. The extra separability assumption puts \(hK\) in the sum. The display is the five-term equation. No derivative and no minimization is used. ∎

Storing, predicting, acting, and staying solvent still do not force the sum. That negative statement is Theorem R2, **STANDARD**, and A7′ does not withdraw it.

## 3. Measurement and feedback heat

The five-term equation is an accounting cost. The heats below are floors, and in class LG-b they are also the realized bath heats. They do not replace \(\kappa I_{\mathrm{mem}}\), \(hK\), \(A\), or \(L\). Sagawa and Ueda (2009), doi 10.1103/PhysRevLett.102.250602, equation (4), bound the sum of measurement work and erasure work by \(kT\) times one mutual information. The erratum is doi 10.1103/PhysRevLett.106.189901. Crossref titles: "Minimal Energy Cost for Thermodynamic Information Processing: Measurement and Information Erasure" and the erratum of that paper. Stacking \(\kappa I_{\mathrm{mem}}\) and a second \(kT\dot I\) on the same nats counts that sum twice. This note does not do that.

Sagawa and Ueda (2010), doi 10.1103/PhysRevLett.104.090602, title "Generalized Jarzynski Equality under Nonequilibrium Feedback Control." Their equation (4) is \(\langle e^{-\beta(W-\Delta F)-I}\rangle=1\). The concavity consequence, their (3), is \(\langle W\rangle\ge\Delta F-kT\langle I\rangle\). This is a one-shot protocol with one measurement. It is not a steady rate, and it is not the heat of a spring. It is the statement that feedback can lower the work done on the controlled system by the mutual information the controller obtained. Their efficacy parameter \(\gamma\) in (6) is a different object from a feedback gain.

Horowitz and Esposito (2014), doi 10.1103/PhysRevX.4.031015, equation (11), for a bipartite jump process, with \(k_B=1\):

\[
\dot\Sigma_X=d_t S_X+\dot S^X_r-\dot I_X\ge 0,
\qquad
\dot\Sigma_M=d_t S_M+\dot S^M_r-\dot I_M\ge 0.
\]

For one thermal reservoir they set \(\dot S_r=-\dot Q/T\), with \(\dot Q\) the heat flow into the subsystem. They define the information flows in their (10). They do not prove the diffusion case. The last section says that the continuous limit of their master equation would be a bipartite Fokker–Planck equation, and they do not carry out that limit.

**Class LG-b.** Mobility 1. The diffusion coefficient of a bath equals \(kT\) of that bath. Both noises are additive and independent.

\[
\begin{aligned}
dX&=(-aX-bKM)\,dt+\sqrt{2D}\,dW_X,\\
dM&=(-\gamma M+\gamma c X)\,dt+\sqrt{2D_M}\,dW_M,
\end{aligned}
\]

with \(a,\gamma,c,D,D_M>0\) and \(b,K\) real. The drift is linear, so the second moments close. Global Lipschitz drift gives a unique strong solution; that existence fact is **STANDARD** and is used only to meet A7′'s "one law" inside this class.

**Lemma D (PROVED HERE).** For a bipartite diffusion with additive independent noise, smooth drift, and currents that vanish at infinity, write \(J_X=F_X p-D\,\partial_X p\) and likewise for \(M\). Define

\[
\dot I_X=\int J_X\,\partial_X\ln p(M\mid X),\qquad
\dot I_M=\int J_M\,\partial_M\ln p(X\mid M).
\]

Then \(d_t I=\dot I_X+\dot I_M\). In steady state \(d_t S_X=0\) and

\[
\Sigma_X:=\int\frac{J_X^2}{D\,p}=\mathrm{Sr}_X-\dot I_X\ge 0,
\]

where the bath entropy-production rate is the expectation

\[
\mathrm{Sr}_X=\mathbb{E}[F_X^2+D\,\partial_X F_X]/D,
\]

and likewise for \(M\). The energy flow into bath \(X\) is \(D\,\mathrm{Sr}_X\). The same construction is the diffusion form of Horowitz and Esposito's (11). The citation does not contain this calculation.

*Proof.* \(d_t I=\int(\partial_t p)\ln(p/(p_X p_M))\), because the marginal terms \(\int p\,(\partial_t p_X)/p_X\) integrate to zero. Substitute \(\partial_t p=-\partial_X J_X-\partial_M J_M\) and integrate by parts. \(\partial_X\ln(p/(p_X p_M))=\partial_X\ln p(M\mid X)\). That is the formula for \(\dot I_X\). Next, \(J_X/p=F_X-D\partial_X\ln p\), so

\[
\int\frac{J_X^2}{D\,p}=\frac1D\mathbb{E}\bigl[(J_X/p)F_X\bigr]-\int J_X\,\partial_X\ln p.
\]

The second integral splits into \(\dot I_X\) plus \(\int j_X\partial_X\ln p_X=-d_t S_X\). In steady state the marginal term vanishes. Integration by parts gives \(\mathbb{E}[F_X\partial_X\ln p]=-\mathbb{E}[\partial_X F_X]\), hence \(\mathbb{E}[(J_X/p)F_X]=\mathbb{E}[F_X^2+D\partial_X F_X]\). Nonnegativity of \(\Sigma_X\) is the integrand. ∎

**Lemma LG (PROVED HERE).** In steady state the covariance solves the Lyapunov equation \(A\Sigma+\Sigma A^\top+2\mathrm{diag}(D,D_M)=0\). The bath rates and the memory's information flow are

\[
\begin{aligned}
\mathrm{Sr}_X&=\frac{bK(Dc\gamma+D_M bK)}{D(a+\gamma)},\\
\mathrm{Sr}_M&=\frac{c\gamma(Dc\gamma+D_M bK)}{D_M(a+\gamma)},\\
\dot I_M&=\frac{(Dc\gamma+D_M bK)(Dc\gamma^2-D_M K a b)}{(Dc\gamma+D_M bK)^2+DD_M(a+\gamma)^2},
\end{aligned}
\]

and \(\dot I_X=-\dot I_M\). The algebra is the Gaussian evaluation of Lemma D. The check script compares these expressions with a direct solve of the Lyapunov system and with the expectation in Lemma D.

**Corollary LG-0 (PROVED HERE).** Set \(b=0\). Then \(\mathbb{E}[X^2]=D/a\), \(\mathrm{Sr}_X=0\), and

\[
\dot I_M=\frac{Dc^2\gamma^3}{Dc^2\gamma^2+D_M(a+\gamma)^2},
\]

which is the Gaussian learning rate of the exogenous equilibrium Ornstein–Uhlenbeck signal of variance \(D/a\). The world's bath receives no net heat. The memory's entropy-production rate satisfies \(\mathrm{Sr}_M\ge\dot I_M\), so the energy flow into that bath is at least \(D_M\dot I_M\). The five-term cost is untouched: this corollary does not set \(\kappa\), \(h\), \(A\), or \(L\) to zero.

**Corollary LG-K (PROVED HERE).** For \(b>0\) and \(K\ge 0\),

\[
\mathrm{Sr}_X+\mathrm{Sr}_M=\frac{(Dc\gamma+D_M bK)^2}{DD_M(a+\gamma)}
\]

is strictly increasing in \(K\). The state variance \(v(K)\) has exactly one critical point on \([0,\infty)\), and it is a minimum at a point \(K_E>0\), because \(v'(0)<0\), \(v(K)\to\infty\) as \(K\to\infty\), and the numerator of \(v'\) is a quadratic in \(K\) with negative constant term and positive leading coefficient. Let the loss be \(\varphi(v)\) with \(\varphi\) strictly increasing and \(C^1\). Let \(J_E=\varphi(v)\) and \(J_H=\varphi(v)+D\,\mathrm{Sr}_X+D_M\,\mathrm{Sr}_M\), one currency, the energy flows of the two baths. Then \(J_E'(K_E)=0\) and \(J_H'(K_E)>0\). For every \(K>K_E\), \(v'(K)>0\), so \(J_H'(K)>0\). Every minimizer of \(J_H\) on \([0,\infty)\) is strictly less than \(K_E\).

The exogenous learning rate of Corollary LG-0 does not depend on \(K\). Using it as the heat at \(b\neq 0\) deletes \(\mathrm{Sr}_X\) and the \(K\)-dependence of \(\mathrm{Sr}_M\) and of \(\dot I_M\). There are parameters in LG-b with \(\dot I_M<0\) while the \(b=0\) learning rate is positive: the memory's jumps can destroy correlation once the feedback is strong. The uncontrolled spring formula does not have that sign.

A centered Gaussian has \(\mathbb{E}[X^4]=3v^2\), which is strictly increasing in \(v\). Corollary LG-K therefore covers a quartic loss inside LG-b. It does not cover a drift that is not linear.

## 4. What is not proved

- Numerical prices. R1′ gives the additive shape and one scale. It does not set \(\kappa\) equal to a heat.
- Multiplicative noise, underdamped coordinates, and jump processes. Horowitz and Esposito cover the jump split. Lemma D does not.
- That \(z_u\) is preferentially independent of the loss. That is A3, and it can fail.
- The ordering in Corollary LG-K for a plant whose drift is not linear. Section 5 tests one such plant. The test is a conjecture.
- Adopting any of this into THEORY. The proposal diff is `theory/THEORY_ACTING_PROPOSAL_2026-11-22.diff`. It is not applied.

## 5. The preregistered comparison

The protocol, the tolerance, and the miss rule are `theory/acting_derivation_checks/PREREG.md`. They are not restated as a result here until that file has been hashed and the run has been done. The prediction is an ordering of two grid gains on a cubic drift. Lemma LG does not determine that ordering. The linear plant appears only as a gate on the path estimator.

## References

Crossref, 22 November 2026. The year field for Debreu came back empty.

- Debreu, G. Topological methods in cardinal utility theory. doi 10.1017/ccol052123736x.010.
- Horowitz, J. M. and Esposito, M. 2014. Thermodynamics with Continuous Information Flow. *Phys. Rev. X* 4:031015. doi 10.1103/PhysRevX.4.031015.
- Sagawa, T. and Ueda, M. 2009. Minimal Energy Cost for Thermodynamic Information Processing: Measurement and Information Erasure. *Phys. Rev. Lett.* 102:250602. doi 10.1103/PhysRevLett.102.250602. Erratum, 2011, doi 10.1103/PhysRevLett.106.189901.
- Sagawa, T. and Ueda, M. 2010. Generalized Jarzynski Equality under Nonequilibrium Feedback Control. *Phys. Rev. Lett.* 104:090602. doi 10.1103/PhysRevLett.104.090602.
- von Neumann, J. and Morgenstern, O. Theory of Games and Economic Behavior, 60th Anniversary Commemorative Edition. doi 10.1515/9781400829460.
