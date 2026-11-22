# Selection axioms: closeness to the cost minimum as a derived result

*Saturday 21 November 2026, evening, America/New_York. Holdability cuts and the THEORY §4 fold merged with PR #144, after the independent review of PR #143 (`reviews/selection_axioms_2026-11-21/REVIEW.md`, verdict NOT READY) and the confirm (`CONFIRM.md`). This note builds on the existing bridge (`core/bridge_2026-11-21/SELECTION.md`) and on the redesign lag already recorded as CL19 (`theory/DYNAMICS.md`). It does not change the Part 2 hypothesis sentence, the locked qualification band of THEORY §3 / FRAMEWORK §9, or any locked preregistration or hash file. T27's P3 remains a failed official test and is not rescued.*

## 0. Bottom line

**In plain words.** If persistence is costly (A1) and copying or retention favors lower cost under the log-linear map A2-L (Wrightian \(r=\exp(m_0-\alpha J)\), with \(\alpha\) constant on the graph), then in a static world, under \(N\mu\ll 1\) and the regularity of SA1–SA1b, a typical lineage sits a distance \(d/(2\beta)\) above the minimum, where \(\beta=\alpha\nu\) and \(\nu\) is the Sella–Hirsh exponent of the named process. A selection strength \(\sigma N_e\gg d\), under A2-L and SA1b, makes the fractional remainder small. THEORY §3's operational meaning of strongly selected is unchanged. Copying that merely favors lower cost (A2-M) is not enough for \(d/(2\beta)\). If the world also drifts and redesign is lumpy, an additional lag from delayed redesign adds to that remainder only under the extra assumptions of SA2.

**What is known, and what is new.** The static-world stationary weight of the fixed type is Sella and Hirsh (2005), already applied to \(J\) in the 21 November 2026 bridge. The scatter \(d/(2\beta)\) is equipartition on a quadratic cost well under that weight, not their fixed-drift load (their eqs. 11–13; see §7). **Credit (added 21 November 2026, evening ET):** the static equipartition load is older than this note first said. Tenaillon, Silander, Uzan and Chao (2007) derive the drift load of Fisher's geometric model from the Sella–Hirsh weight. For log-fitness proportional to \(-\lVert x\rVert^Q\) in \(n_e\) dimensions, they get mean fitness \((1-\nu^{-1})^{n_e/Q}\), so a mean log-fitness deficit of about \(n_e/(2\nu)\) at \(Q=2\). That is \(d/(2\beta)\) in fitness units. They credit the link between drift load and phenotypic dimension to Hartl and Taubes (1998), refined by Poon and Otto (2000). Held, Nourmohammad and Lässig (2014) cite the same three papers for \(2NL_{\rm eq}\simeq d/2\). The constant \(d/(2\beta)\) is therefore prior art, not ours. The fractional form \((\mathbb{E}[J]-J^\star)/J^\star\approx d/(2\sigma N_e)\) is the bridge's formula, with \(N_e\) equal to Sella and Hirsh's \(\nu\) (haploid Moran \(\beta=\alpha(N-1)\); diploid Wright–Fisher \(\beta=\alpha(2N-1)\), an approximation). The lumpy-redesign lag \(2\sqrt{kw\sigma^2/6}\) (as a long-run cost rate that includes the lumps) is Dixit's (1991) approximation, exact at zero discounting (Chalkley 1997), and is already CL19. Adding the two terms, when the costs themselves add and the scatter mixes inside a redesign cycle, is a one-line use of linearity of expectation, not a new mechanism. **The packaging is what is new:** closeness to the minimum is a derived remainder, from explicit axioms, rather than a primitive. The open bet then moves to whether real systems satisfy the axioms and the parameters.

**The hypothesis sentence is unchanged.** It is, byte for byte,

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

## 1. Status words

**PROVED** means proved inside the stated model, which says nothing by itself about nature; **NUMERICAL** means computed, not proved; **HYPOTHESIS** means a claim about the world; **TESTED** is reported with its result; **KNOWN** means published and credited; **OPEN** means untested or not derived, not refuted; **ANALOGY** means a likeness, not a proof and not a field result.

## 2. The axioms

The three axioms are statements about a class of systems, not about the universe. They are the premises from which closeness is derived. They are not themselves derived here.

**A1 (persistence has a cost).** Over any interval of persistence, a design \(\mathcal{D}\) accrues a cost rate \(J(\mathcal{D})\ge 0\), measured in energy, resources, or another booked scarce quantity in the units of the master equation of THEORY §2. A design that cannot cover \(J\) shrinks or is eliminated (ruin). This note uses \(J\) as already defined; it does not reopen the term list.

**A2 (copying or retention favors lower cost).** Among available designs, those with lower \(J\) are copied or retained at a higher rate. Three formalizations, of decreasing strength:

- **(A2-L) Linear Malthusian map.** \(m(\mathcal{D})=m_0-\alpha J(\mathcal{D})\) with \(\alpha>0\), and Wrightian birth rates \(r=\exp(m)\). This is the assumption of the existing bridge, not a theorem. Under this map, the THEORY §3 cost-to-fitness elasticity is \(\sigma=\lvert\mathrm{d}\log r/\mathrm{d}\log J\rvert=\alpha J\) at an operating point \(J\), so \(\alpha=\sigma/J^\star\) at the minimum. A birth rate linear in cost, \(r=m_0-\alpha J\), does not give \(\pi\propto\exp(-\beta J)\). The exponential map is load-bearing, and \(\alpha\) is constant on the whole graph. Local linearity at \(J^\star\) is enough for a local Gaussian and for SA1b, and it is not enough for the global weight in SA1. \(\sigma=\alpha J\) identifies THEORY §3's elasticity with this Wrightian log-fitness. A profit margin or a survival probability is that \(r\) only when the preregistration says so. The fractional form also needs \(J^\star>0\).
- **(A2-M) Monotone map.** \(m\) is strictly decreasing in \(J\). Qualitatively, cheaper designs are favored. This does **not** give a Boltzmann law or the constant \(d/(2\beta)\).
- **(A2-P) Persistence only.** There is no copying: a held structure is retained while it covers its cost and is dropped when it does not. The Moran / Wright–Fisher theorems below do **not** apply. A persistence-only version is already listed as missing in `theory/SCALE_ENDS.md` §6b, and remains **OPEN**.

**A3 (the world drifts).** The location of \(\arg\min J\), or the world's statistics that enter \(J\), change with a positive variance rate \(\sigma^2>0\) (Brownian drift of the optimum, unless another process is named). The static world is the special case \(\sigma^2=0\), already treated by the bridge.

**What is not assumed.** Formal Axiom 7 of `reviews/night1/formal/AXIOMS.md` says the realized architecture satisfies \(J(A)\le\min J+\varepsilon\). That axiom *assumes* near-minimization. It is not a premise of this note; the point is to derive a scale for \(\varepsilon\). Frequency dependence, strong mutation, and a binding ruin constraint inside the stationary law are not assumed, and the theorems do not cover them.

## 3. Static world: the existing bridge, stated as a theorem

The results in this section are **KNOWN**. They are restated so the note is self-contained, with short proofs. They are not a new mathematical theorem. The application to the reduced cost \(J\), and the fractional consistency note with the qualification band, are already in `core/bridge_2026-11-21/SELECTION.md`, now with the same per-model exponents as Corollary SA1c.

**Theorem SA1 (KNOWN: Sella and Hirsh 2005, applied to \(J\)).** Assume A1, A2-L, and a static world (\(\sigma^2=0\), or a frozen snapshot of A3). Consider a haploid Moran process of size \(N\) on a finite connected undirected design graph, in the weak-mutation regime \(N\mu\ll 1\) (the population is typically monomorphic; substitutions are an origination–fixation chain), with equal mutation clocks on each undirected edge, and with no frequency dependence. Let \(r_i=\exp(-\alpha J(\mathcal{D}_i))\). Then the unique stationary distribution of the monomorphic chain satisfies

\[
\frac{\pi_i}{\pi_j}=\Bigl(\frac{r_i}{r_j}\Bigr)^{N-1},
\]

and therefore

\[
\pi(\mathcal{D})\;\propto\;\exp\bigl(-\beta J(\mathcal{D})\bigr),\qquad \beta=\alpha(N-1).
\]

For diploid Wright–Fisher with multiplicative fitness within a locus, Sella and Hirsh's approximation gives \(\beta=\alpha(2N-1)\) (their weight \(f^{2N-1}\)). Haploid Wright–Fisher in the same table is \(2(N-1)\), which this note does not use. The weak-mutation condition in their introduction is \(N\mu\ll 1\).

*Proof.* In the weak-mutation limit the state is the currently fixed design. A mutant \(j\) arising in a monomorphic \(i\) population fixes with the standard haploid-Moran probability \(\varphi_{i\to j}=(1-\rho)/(1-\rho^N)\) for \(\rho=r_i/r_j\neq 1\), and \(1/N\) if \(r_i=r_j\). Detailed balance on an undirected edge with equal mutation clocks is \(\pi_i\,\varphi_{i\to j}=\pi_j\,\varphi_{j\to i}\). Substituting the fixation probabilities yields \(\varphi_{j\to i}/\varphi_{i\to j}=(r_i/r_j)^{N-1}\), hence \(\pi_i/\pi_j=(r_i/r_j)^{N-1}\). The algebra: with \(\rho=r_i/r_j\),

\[
\varphi_{i\to j}=\frac{1-\rho}{1-\rho^N}=\frac{\rho-1}{\rho^N-1},\qquad
\varphi_{j\to i}=\frac{1-\rho^{-1}}{1-\rho^{-N}}=\rho^{N-1}\frac{\rho-1}{\rho^N-1},
\]

so the ratio is \(\rho^{N-1}\). Then \(r=\exp(-\alpha J)\) gives \(\pi\propto\exp(-\alpha(N-1)J)\). Uniqueness follows from connectedness of the graph (one communicating class). This is the argument of Sella and Hirsh (2005, doi 10.1073/pnas.0501865102). The weight is Sella and Hirsh's detailed balance. Iwasa 1988 is the free-fitness Lyapunov function. This proof does not use it. □

**Theorem SA1b (KNOWN: equipartition).** Assume the conclusion of SA1, and assume that near the unique minimum, \(J(\theta)=J^\star+\tfrac12(\theta-\theta^\star)^\top H(\theta-\theta^\star)\) in \(d\) continuous design coordinates, with \(H\) symmetric positive definite, and that the Boltzmann measure can be treated as supported on this quadratic well (the tails in other basins are negligible at the \(\beta\) of interest). The coordinates \(\theta\) are coordinates in which the design graph is a uniform lattice (equal clocks, equal spacing), so the stationary weight converges to the Lebesgue density \(\propto e^{-\beta J}\). If the natural coordinates are not those, whiten before quoting \(d/(2\beta)\). T27's pilot recorded that a raw log-rate grid did not give this excess. Then

\[
\mathbb{E}[J]-J^\star \;=\; \frac{d}{2\beta}.
\]

*Proof.* The density is \(\pi(\theta)\propto\exp\bigl(-\tfrac{\beta}{2}(\theta-\theta^\star)^\top H(\theta-\theta^\star)\bigr)\), a Gaussian with covariance \(\Sigma=(\beta H)^{-1}\). Then

\[
\mathbb{E}\bigl[\tfrac12(\theta-\theta^\star)^\top H(\theta-\theta^\star)\bigr]
=\tfrac12\mathrm{Tr}(H\Sigma)
=\tfrac12\mathrm{Tr}(I_d)
=\frac{d}{2\beta}.
\]

□

The identity is also checked numerically in `tools/selection_axioms_checks.py` (labeled **NUMERICAL** as a check, not as the proof).

**Corollary SA1c.** The absolute excess is the SA1b quantity \(\mathbb{E}[J]-J^\star=d/(2\beta)\). The fractional excess is a separate statement. Under A2-L, \(\beta=\alpha\nu\) with \(\nu\) the Sella–Hirsh exponent of the process just named. The \(N_e\) in THEORY §3's drift barrier is this \(\nu\) (\(s N_e\approx 1\) matches their scale \(\nu s\approx 1\)), so \(\beta=\alpha N_e=\sigma N_e/J^\star\) at leading order when \(J^\star>0\) and \(\sigma\) is evaluated at \(J^\star\). Then \((\mathbb{E}[J]-J^\star)/J^\star\approx d/(2\sigma N_e)\). The form \(\alpha(N_e-1)\) is the haploid Moran exponent when \(N_e\) is census size. It is not the diploid exponent.

**Closeness under the formula.** The existing qualification band \(\varepsilon=10/(\sigma N_e)\) of THEORY §3 / FRAMEWORK §9 is a *fractional* difference used to exclude a named rival (a one-dimensional comparison). The ratio of the typical fractional excess to that band is \(d/20\). For a few soft coordinates that fractional excess sits well inside the conservative band; for large \(d\) it need not. These uses are different. **This note does not change the locked factor of 10.** The factor of 10 is a conservative choice made in the repository, not a constant of Lynch, Ackerman, Gout, Long, Sung, Thomas and Foster (2016, doi 10.1038/nrg.2016.104), who are cited for the drift-barrier scale \(s N_e\approx 1\).

**Infinite-population limit (KNOWN geometry).** The Shahshahani metric (Shahshahani 1979, doi 10.1090/memo/0211) is the geometry in which, at infinite \(N\), selection is gradient ascent of mean fitness, and so gradient descent of mean \(J\). Fisher's fundamental theorem is the variance statement for that infinite-population increase. That geometry is the \(\beta\to\infty\) limit of the same picture. Finite \(N\) replaces the point mass at the minimum by the Boltzmann spread. The geometry is credited; it is not used as a derivation of \(\pi\).

## 4. Drifting world: selection scatter plus redesign lag

This section is the one place the note goes beyond a restatement of the bridge. The two *terms* are still **KNOWN**. What is **PROVED (in-model)** is their sum under the assumptions below. The sum is bookkeeping, not a new mechanism; a hostile reading that calls SA2 thin is fair.

Write \(\mathcal{D}_t\) for the design in force and \(\mathcal{D}_t^\star\) for \(\arg\min J\) at the inputs in force. Split the design coordinates as \((x,y)\), where \(x=\mathcal{D}-\mathcal{D}^\star\) is the gap along a lumpy redesign direction and \(y\in\mathbb{R}^d\) are fine coordinates that can be substituted without paying the lump \(k\).

**Assumption SA2-A (additive costs).** In a frame attached to the moving minimum,

\[
J(\mathcal{D}_t)-J_t^\star \;=\; w\,x_t^2 \;+\; \tfrac12 y_t^\top H y_t,
\]

with \(w>0\) and \(H\) symmetric positive definite, independent of \(x\). (If the Hessian in \(y\) depends on the gap \(x\), the expectations need not add in closed form, and SA2 is not claimed.)

**Assumption SA2-B (timescale separation).** The origination–fixation chain in \(y\), at the current \(x\), mixes on a timescale much shorter than the mean redesign cycle. The \(y\)-marginal may then be treated as the stationary Boltzmann measure of SA1 at the current basin.

**Assumption SA2-C (lumpy redesign, CL19).** The gap \(x\) is managed by the optimal lumpy policy of CL19(a): \(x\) is a Brownian motion with variance rate \(\sigma^2\), left alone until \(|x|\) reaches \(b^\star=(6k\sigma^2/w)^{1/4}\), then reset to zero. The long-run *operational* excess from the gap is \(\mathbb{E}[w x^2]=wb^{\star 2}/6\). The long-run *total* excess rate, including amortized lumps, is the CL19 quantity

\[
J_R-J^\star_{\mathrm{drift}} \;=\; \frac{k\sigma^2}{b^2}+\frac{wb^2}{6},
\]

minimal at \(b^\star\) with value \(2\sqrt{kw\sigma^2/6}\). This is **KNOWN** (Dixit 1991, *Review of Economic Studies* 58:141, doi 10.2307/2298051, title "Analytical Approximations in Models of Hysteresis"; simplified treatment in *Journal of Economic Dynamics and Control* 15:657–673, doi 10.1016/0165-1889(91)90037-2, title "A simplified treatment of the theory of optimal regulation of Brownian motion"; exact at zero discounting, Chalkley 1997, *Economics Letters* 57:189–195, doi 10.1016/s0165-1765(97)00222-x; re-derived and checked as CL19). The coefficient 6 was re-derived in this repository and was not checked against the equations printed in those papers. Discount rate zero. Between redesigns the lumpy coordinate is not a site of the origination–fixation chain. The optimum moves only in that coordinate. A reset changes that coordinate only. The pair \(N\mu\ll 1\) and \(t_{\mathrm{mix}}(y)\ll b^{\star 2}/\sigma^2\) is part of the hypothesis; if no mutation rate satisfies both, SA2 is not claimed. Here \(d=\dim y\).

**Theorem SA2 (PROVED in-model, under SA2-A–C).** Assume A1, A2-L, A3, the conclusion of SA1b for the \(y\)-coordinates, and Assumptions SA2-A–C in full, including: discount rate zero; between redesigns the lumpy coordinate is not a site of the origination–fixation chain; the optimum moves only in that coordinate; a reset changes that coordinate only; the pair \(N\mu\ll 1\) and \(t_{\mathrm{mix}}(y)\ll b^{\star 2}/\sigma^2\) holds (if no mutation rate satisfies both, SA2 is not claimed); and \(d=\dim y\). Then the long-run operational excess and the long-run total excess rate (including lumps) are, respectively,

\[
\mathbb{E}[J(\mathcal{D}_t)-J_t^\star]
\;=\; \frac{w b^{\star 2}}{6}+\frac{d}{2\beta}
\;=\; \sqrt{\frac{kw\sigma^2}{6}}+\frac{d}{2\beta},
\]

\[
\mathbb{E}[J_R]-J^\star_{\mathrm{drift}}
\;=\; 2\sqrt{\frac{kw\sigma^2}{6}}+\frac{d}{2\beta}.
\]

The two Dixit values differ by the amortized redesign cost, which equals the operational gap cost at the optimal band. A statement about "how close the held design sits to \(J^\star\)" must use the first display; a statement about "how much extra cost rate a lineage pays in a drifting world" must use the second. Conflating them is a mistake.

*Proof.* Linearity of expectation applied to SA2-A gives \(\mathbb{E}[J-J_t^\star]=\mathbb{E}[w x^2]+\mathbb{E}[\tfrac12 y^\top H y]\), with no independence required for the sum of means. Under SA2-B the second term is \(d/(2\beta)\) by SA1b. Under SA2-C the first term is \(w b^{\star 2}/6\). Substituting \(b^{\star 4}=6k\sigma^2/w\) yields \(w b^{\star 2}/6=\sqrt{kw\sigma^2/6}\). Adding the amortized lumps \(k\sigma^2/b^{\star 2}\), which equals the same value at \(b^\star\), gives the \(J_R\) display. □

Independence of \(x\) and \(y\) is not required for these means, but it is required if one wants the joint law to be the product of the Dixit occupation and the Boltzmann measure (for example to compute quantiles, or \(\mathrm{Var}(J)\)). The occupation \(\rho(x)=(b-|x|)/b^2\) is the normalized Green function of driftless Brownian motion killed at \(\pm b\). CL19 re-derives the coefficient 6 by a renewal argument and says the coefficient was not checked against Dixit's or Chalkley's displayed equations. `tools/selection_axioms_checks.py` records those Green-function identities from the closed form. A path simulation of the reset process checks the moments \(\mathbb{E}[x^2]=b^2/6\) and \(\mathbb{E}[|x|]=b/3\). It does not histogram the density, and it is not a derivation of \(\rho\). An inverse-CDF draw from the assumed density, where used, is labeled as such and is not a derivation. The addition of means is also checked there (**NUMERICAL** as a check).

**When SA2 is not claimed.** If adjustment is smooth (\(k=0\), \(\kappa>0\)), there is no inaction band (CL19(c)), and §5 applies instead. If the discount rate is positive, if the lumpy coordinate is a site of the substitution chain, if the optimum moves in \(y\), if a reset moves \(y\), if no mutation rate satisfies both \(N\mu\ll 1\) and \(t_{\mathrm{mix}}(y)\ll b^{\star 2}/\sigma^2\), or if the Hessian in \(y\) depends on \(x\), the sum is **OPEN**. If the world is a step of size \(\Delta\) lasting a regime \(T\), the CL19(b) threshold \(\Delta_k=\sqrt{k/(wT)}\) replaces the fourth-root band; the present note does not add a scatter theorem for that case beyond SA1 inside a regime.

## 5. Smooth tracking of a moving optimum

Lumpy redesign is not the only response to A3. If the design can move continuously, the lag is a tracking lag, not an inaction band.

**Proposition SA3 (PROVED in-model, infinite-population gradient dynamics).** Assume A2-L and \(J=J^\star+w(\theta-\theta^\star)^2\) in one trait (so the Hessian is \(H=2w\)). Let the mean phenotype \(\mu\) follow Lande's selection-gradient dynamics \(\mathrm{d}\mu/\mathrm{d}t=V_G\,\partial m/\partial\theta\), with additive genetic variance \(V_G>0\) treated as given. Then \(\mathrm{d}\mu/\mathrm{d}t=\lambda(\theta^\star-\mu)\) with \(\lambda=2\alpha w V_G\).

- If \(\theta^\star\) moves at constant speed \(v\), the lag is \(L=\mu-\theta^\star\to -v/\lambda\), and the operational excess is \(w(v/\lambda)^2=v^2/(4\alpha^2 w V_G^2)\).
- If \(\mathrm{d}\theta^\star=\sigma_\theta\,\mathrm{d}W\) (Brownian optimum), the lag is an Ornstein–Uhlenbeck process, \(\mathrm{Var}(L)=\sigma_\theta^2/(2\lambda)\), and \(\mathbb{E}[w L^2]=\sigma_\theta^2/(4\alpha V_G)\). The curvature \(w\) cancels: a steeper well costs more per unit lag but is tracked faster.

*Proof.* Under A2-L, \(\partial m/\partial\theta=-2\alpha w(\mu-\theta^\star)\) at the mean, hence \(\lambda=2\alpha w V_G\). For quadratic \(J\), the mean of the Malthusian gradient equals the gradient at the mean. Lande 1976 writes the gradient of log mean Wrightian fitness. That gradient equals \(-2\alpha w(\mu-\theta^\star)\) only in the weak-selection limit \(2\alpha w V_P\ll 1\); the exact Gaussian integral carries the factor \(1/(1+2\alpha w V_P)\). \(V_G\) is an input and is not phenotypic variance. The constants in the two displays are the ones proved from the ODE written here. Constant speed: in the moving frame, \(\dot L=-\lambda L-v\), with unique rest point \(L=-v/\lambda\). Brownian optimum: \(L=\mu-\theta^\star\) satisfies \(\mathrm{d}L=-\lambda L\,\mathrm{d}t-\sigma_\theta\,\mathrm{d}W\), whose stationary variance is \(\sigma_\theta^2/(2\lambda)\). Then \(\mathbb{E}[w L^2]=w\sigma_\theta^2/(4\alpha w V_G)\). Here \(\sigma_\theta\) is a diffusion coefficient; A3's \(\sigma^2\) is a variance rate. □

**Credit, and a limit on the credit.** The gradient dynamics of the mean are Lande's (1976). The program of adaptation and extinction under a changing environment is that of Bürger and Lynch (1995). Mustonen and Lässig 2010 prove a fitness-flux theorem for mutation, drift, and time-dependent selection. This note uses none of their constants. **This note does not borrow a numerical constant or an extinction threshold from Bürger and Lynch:** the papers were identified and their DOIs verified, but their internal formulas were not re-derived from the texts. The constants in SA3 are the ones just proved, in this notation, under the stated dynamics. \(V_G\) is an input, not derived from the weak-mutation chain of SA1; SA3 and SA1 are different regimes (polymorphic quantitative variance versus a typically monomorphic origination–fixation chain).

## 6. Time, mutation, and reachability

**Proposition SA4 (qualitative; no new constant).** The stationary statements SA1–SA2 assume that the origination–fixation chain has mixed, and, for field application, that at least the ten redesign times already required by THEORY §3 have been spent in one world. They do not give a closeness guarantee at finite time, or on a mutation graph that cannot reach the minimum.

- **Waiting time.** In the weak-mutation regime the mixing time is set by waiting for mutations and by fixation times. A very small mutation rate slows approach; it does not change the *stationary* scatter \(d/(2\beta)\). A very large mutation rate leaves the typically-monomorphic assumption, and SA1 is not claimed (strong mutation is outside the theorem).
- **Metastability.** At large \(\beta\), valleys block the chain on relevant timescales. EVO1 worlds W4 and W4b are the in-model examples already on record (CLAIM_MAP Q5–Q6, SIM-FAIL on the proxy): the Boltzmann law assumes the graph can traverse the space. A disconnected or valley-blocked graph is a different process. This is compatible with SA1, not a rescue of those FAILs and not a failure of SA1.
- **The Price identity (KNOWN).** Price 1970, Nature 227:520–521, is the discrete identity \(\Delta\bar z=\mathrm{Cov}(w,z)/\bar w\) plus a transmission term. Under A2-L, faithful transmission, and continuous time, the Malthusian limit is \(\mathrm{d}\mathbb{E}[J]/\mathrm{d}t=\mathrm{Cov}(m,J)=-\alpha\,\mathrm{Var}(J)\le 0\). That limit is what is used here. It does not give the distance to the minimum. A quantitative decay rate would need a bound of \(\mathrm{Var}(J)\) in terms of the excess (a Poincaré or log-Sobolev step), which is not claimed here.

**Dimensionality and Fisher's geometric model.** Orr 1998 derives the distribution of factors fixed in Fisher's geometric model. The fall, with dimension, in the chance a random mutation is beneficial is Fisher 1930, and Orr uses that model. Neither result is the stationary excess \(d/(2\beta)\). Fisher's 1930 book has no Crossref DOI. The fall with dimension is relevant to SA4 (approach can be slow in high dimension) and to the reading of \(d\) in SA1b (more soft coordinates mean more residual excess at fixed \(\beta\)).

## 7. Prior art, checked and limited to what is used

Every DOI below was verified on Crossref on 21 November 2026. No citation is invented. Books are marked as books.

- **Sella and Hirsh (2005)** and **Iwasa (1988).** Sella and Hirsh derive the stationary weight of fixed genotypes. In their equations 11–13 the fixed-drift load is for fitness uniform on (0,1): mean fitness \((\nu+1)/(\nu+2)\), load about \(1/\nu\). They defer Fisher's geometric model in more than one dimension. SA1b's excess \(d/(2\beta)\) is equipartition on a quadratic cost well under their stationary weight. Iwasa 1988 is the free-fitness Lyapunov function; the SA1 proof does not use it.
- **Hartl and Taubes (1998), Poon and Otto (2000), Tenaillon et al. (2007)** (credit added 21 November 2026). The drift load of Fisher's geometric model as a function of phenotypic dimension. Tenaillon et al. derive it from the Sella–Hirsh weight; at quadratic log-fitness their result is a mean log-fitness deficit of about \(n_e/(2\nu)\), which is SA1b's \(d/(2\beta)\) in fitness units. SA1b is a restatement of this prior result in the repository's \(J\) and \(\beta\) notation.
- **Ohta (1973, *Nature* 246:96–98, doi 10.1038/246096a0)**, "Slightly Deleterious Mutant Substitutions in Evolution," is the nearly-neutral statement that finite \(N\) lets slightly costlier types fix. That is the same intuition as a positive scatter at finite \(\beta\). This note does not attribute the constant \(d/(2\beta)\) to Ohta.
- **Kimura (1968, *Nature* 217:624–626, doi 10.1038/217624a0)**, "Evolutionary Rate at the Molecular Level," is the neutral substitution-rate argument. It is not a drift-load formula and is not used as one. It is listed because it is the usual companion paper, and to say plainly that it is a different result.
- **Classical mutation-selection balance** (standing polymorphism; the load of order the deleterious mutation rate under strong selection against rare alleles) lives in a different regime from the typically monomorphic chain of SA1. As \(\beta\to\infty\) the monomorphic-chain scatter \(d/(2\beta)\) vanishes; a polymorphism load need not. SA1 does not include that load, and does not refute it.
- **Shahshahani (1979):** geometry of the infinite-population replicator, already in the bridge.
- **Potential games.** Monderer and Shapley (1996, *Games and Economic Behavior* 14:124–143, doi 10.1006/game.1996.0044), already used in CLAIM_MAP CT31, give Nash = \(\arg\min\) of an exact potential. That is **ANALOGY** to "selection favors lower \(J\)" when \(J\) *is* the potential (as in the aggregative class of CT31). It is not a derivation of the Boltzmann \(\pi\) of SA1.
- **Stochastic replicator dynamics** (Langevin or other finite-\(N\) perturbations of the replicator) also produce fluctuations that shrink with \(N\). This note does not identify those fluctuations with \(\pi\propto e^{-\beta J}\) and does not claim a specific formula from that literature.
- **Dixit (1991) and Chalkley (1997):** the lumpy-redesign lag, already CL19.
- **Lynch et al. (2016):** the drift-barrier scale behind the existing qualification band; the factor of 10 remains the repository's conservative choice.

## 8. What this does not show

- It does not make the hypothesis a physical law, and it is not a theory of everything.
- It does not identify \(\beta\), or the ruin-constraint scale \(z=B/(\sigma\tau^H)\) of CT18, with temperature in kelvin. Those are two different quantities (see the bridge's `BRIDGE.md`). The symbol \(\sigma\) in \(z\) is the CT18 shock scale, not the cost-to-fitness map \(\sigma\) of THEORY §3, and not the world-drift rate \(\sigma^2\) of A3.
- It does not put the ruin cap \(P(\mathrm{ruin})\le\varepsilon_r\) into \(\pi\). Feasibility remains a constraint on the design set.
- It does not change the Part 2 hypothesis sentence or the locked factor of 10. The in-model derivation is now also stated in THEORY §4.

## 9. A falsifiable quantitative consequence (OPEN, not locked)

**SA-P1 (OPEN, not locked, not a test until preregistered).** The preregistration fixes, before any outcome is computed: the process whose \(\nu\) is \(N_e\) (Corollary SA1c); \(d=\dim y\) by a counting rule that excludes the lumpy gap; whether \(\overline J\) includes amortized lumps, and therefore whether \(\Delta_{\mathrm{lag}}\) is \(\sqrt{kw\sigma^2/6}\) or twice that; and \(J^\star_{\mathrm{proxy}}>0\) as the perfect-tracking cost rate in the same units. The lag-corrected fractional excess is then compared with \(d/(2\sigma N_e)\). Kill, for a preregistered set of at least \(n_{\min}\) qualifying systems: the excess exceeds \(3\times d/(2\sigma N_e)\) in more than the preregistered count, or it is below \((1/3)\times d/(2\sigma N_e)\), or it is not positive. The factor of three is a placeholder, not a derived constant, and it is not THEORY §3's factor of 10. A log–log slope of that excess on \(\sigma N_e\), with a preregistered confidence interval, kills the \(1/(\sigma N_e)\) scaling when the interval misses \([-1.5,-0.5]\). Two points and the word "systematically" are not a kill. If there is no quadratic chart, the status is NOT A TEST. If adjustment is smooth or the class preregisters \(k=0\), \(\Delta_{\mathrm{lag}}\) is omitted and SA3 is not substituted unless its inputs, including \(V_G\), are themselves preregistered. A class that does not qualify, inputs not independent of the design, a lag term used without preregistered \((k,w,\sigma^2)\), or fewer than ten redesign times, is also NOT A TEST, not a pass and not a fail.

SA-P1 is a dated sketch, in the same sense as the layer-lifetime predictions: **OPEN**, not locked, and not a test until a class, the inputs, and the factor are preregistered. It does not change any locked file.

## 10. The Part 2 hypothesis sentence

The sentence stays byte-identical, including the word "law" in a sentence that labels itself a hypothesis. The theorem is the formula for the excess under A1, A2-L, \(N\mu\ll 1\), and the regularity in SA1–SA2. THEORY §3 still defines strongly selected by the five qualification items. The formula plus \(\sigma N_e\gg d\) is what puts a qualifying class near the minimum. The remaining empirical claim is that real systems in a qualifying class satisfy those assumptions with parameters that make the remainder small, and that \(J\) as written is the cost that A2 acts on. That is a smaller, sharper bet. It is not yet a field result.

## 11. Relation to the existing bridge and to T27

This note **builds on** `core/bridge_2026-11-21/`, rather than replacing it. Theorem SA1 is the bridge's Moran theorem, restated. Corollary SA1c keeps the bridge's fractional form, with \(\beta=\alpha\nu\). The bridge file now states the same per-model exponents (haploid Moran \(\beta=\alpha(N-1)\); diploid Wright–Fisher \(\beta=\alpha(2N-1)\), an approximation). The official T27 test of that package (locked `PREREG.md`, hashes unchanged) remains: P1 passed (3/3), P2 passed (3/3), P3 failed (0/3) and is not rescued. P3's operationalization (a two-\(K\) mass floor at low \(\beta\)) was already missed by the exact Boltzmann measure on the pilot; the failure is about that operationalization, not a refutation of SA1. Nothing in SA2 repairs P3.

## 12. Numerical checks

`tools/selection_axioms_checks.py`, run by `tools/test_selection_axioms_checks.py`. **NUMERICAL**.

## References

Verified on Crossref, 21 November 2026, America/New_York, unless marked as a book.

- Bürger, R. & Lynch, M. 1995, *Evolution* 49:151–163, doi 10.1111/j.1558-5646.1995.tb05967.x (JSTOR 10.2307/2410301), "Evolution and Extinction in a Changing Environment: A Quantitative-Genetic Analysis."
- Chalkley, M. 1997, *Economics Letters* 57:189–195, doi 10.1016/s0165-1765(97)00222-x, "An explicit solution for dynamic menu costs with zero discounting."
- Dixit, A. 1991, *Review of Economic Studies* 58:141, doi 10.2307/2298051, "Analytical Approximations in Models of Hysteresis"; *Journal of Economic Dynamics and Control* 15:657–673, doi 10.1016/0165-1889(91)90037-2, "A simplified treatment of the theory of optimal regulation of Brownian motion."
- Fisher, R. A. 1930, *The Genetical Theory of Natural Selection* (book; no Crossref DOI).
- Hartl, D. L. & Taubes, C. H. 1998, *Genetica* 102–103:525–533, doi 10.1023/a:1017071901530, "Towards a theory of evolutionary adaptation."
- Held, T., Nourmohammad, A. & Lässig, M. 2014, *Journal of Statistical Mechanics* P09029, doi 10.1088/1742-5468/2014/09/P09029, "Adaptive evolution of molecular phenotypes."
- Iwasa, Y. 1988, *Journal of Theoretical Biology* 135:265–281, doi 10.1016/s0022-5193(88)80243-1, "Free fitness that always increases in evolution."
- Kimura, M. 1968, *Nature* 217:624–626, doi 10.1038/217624a0, "Evolutionary Rate at the Molecular Level."
- Lande, R. 1976, *Evolution* 30:314–334, doi 10.1111/j.1558-5646.1976.tb00911.x (JSTOR 10.2307/2407703), "Natural Selection and Random Genetic Drift in Phenotypic Evolution."
- Lynch, M., Ackerman, M. S., Gout, J.-F., Long, H., Sung, W., Thomas, W. K. & Foster, P. L. 2016, *Nature Reviews Genetics* 17:704–714, doi 10.1038/nrg.2016.104, "Genetic drift, selection and the evolution of the mutation rate."
- Monderer, D. & Shapley, L. S. 1996, *Games and Economic Behavior* 14:124–143, doi 10.1006/game.1996.0044, "Potential Games."
- Mustonen, V. & Lässig, M. 2010, *Proceedings of the National Academy of Sciences* 107:4248–4253, doi 10.1073/pnas.0907953107, "Fitness flux and ubiquity of adaptive evolution."
- Ohta, T. 1973, *Nature* 246:96–98, doi 10.1038/246096a0, "Slightly Deleterious Mutant Substitutions in Evolution."
- Orr, H. A. 1998, *Evolution* 52:935–949, doi 10.1111/j.1558-5646.1998.tb01823.x (JSTOR 10.2307/2411226), "The Population Genetics of Adaptation: The Distribution of Factors Fixed during Adaptive Evolution."
- Poon, A. & Otto, S. P. 2000, *Evolution* 54:1467–1479, doi 10.1111/j.0014-3820.2000.tb00693.x, "Compensating for our load of mutations: freezing the meltdown of small populations."
- Price, G. R. 1970, *Nature* 227:520–521, doi 10.1038/227520a0, "Selection and Covariance."
- Sella, G. & Hirsh, A. E. 2005, *Proceedings of the National Academy of Sciences* 102:9541–9546, doi 10.1073/pnas.0501865102, "The application of statistical physics to evolutionary biology."
- Shahshahani, S. 1979, *Memoirs of the American Mathematical Society* 17, no. 211, doi 10.1090/memo/0211, "A new mathematical framework for the study of linkage and selection."
- Tenaillon, O., Silander, O. K., Uzan, J.-P. & Chao, L. 2007, *PLoS ONE* 2:e217, doi 10.1371/journal.pone.0000217, "Quantifying Organismal Complexity using a Population Genetic Approach."
