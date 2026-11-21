# Selection axioms: closeness to the cost minimum as a derived result

*Saturday 21 November 2026, evening, America/New_York. Branch `selection-axioms-2026-11-21`. This note builds on the existing bridge (`core/bridge_2026-11-21/SELECTION.md`) and on the redesign lag already recorded as CL19 (`theory/DYNAMICS.md`). It does not change the Part 2 hypothesis sentence, the locked qualification band of THEORY §3 / FRAMEWORK §9, or any locked preregistration or hash file. T27's P3 remains a failed official test and is not rescued.*

## 0. Bottom line

**In plain words.** If staying in existence is costly, if what is copied or retained is whatever persists at lower cost, and if that favoritism is linear in the cost, then in a static world a typical lineage does not sit exactly at the cheapest design: it sits a distance \(d/(2\beta)\) above the minimum, where \(\beta\) grows with selection strength (population size times the cost-to-fitness slope). "Strongly selected" means that remainder is small. If the world also drifts and changing design is lumpy, an additional lag from delayed redesign adds to that remainder.

**What is known, and what is new.** The static-world distribution and the \(d/(2\beta)\) scatter are standard population genetics applied to \(J\): Sella and Hirsh (2005) plus elementary equipartition. That application is already in the 21 November 2026 bridge, including the fractional form \(\approx d/(2\sigma N_e)\). The lumpy-redesign lag \(2\sqrt{kw\sigma^2/6}\) (as a long-run cost rate that includes the lumps) is Dixit's (1991) approximation, exact at zero discounting (Chalkley 1997), and is already CL19. Adding the two terms, when the costs themselves add and the scatter mixes inside a redesign cycle, is a one-line use of linearity of expectation, not a new mechanism. **The packaging is what is new:** closeness to the minimum is a derived remainder, from explicit axioms, rather than a primitive. The open bet then moves to whether real systems satisfy the axioms and the parameters. If a reviewer reads only the formulas, they will correctly say this note restates known results; that is intended, and is said here first.

**The hypothesis sentence is unchanged.** It is, byte for byte,

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

## 1. Status words

**PROVED** means proved inside the stated model, which says nothing by itself about nature; **NUMERICAL** means computed, not proved; **HYPOTHESIS** means a claim about the world; **TESTED** is reported with its result; **KNOWN** means published and credited; **OPEN** means untested or not derived, not refuted; **ANALOGY** means a likeness, not a proof and not a field result.

## 2. The axioms

The three axioms are statements about a class of systems, not about the universe. They are the premises from which closeness is derived. They are not themselves derived here.

**A1 (persistence has a cost).** Over any interval of persistence, a design \(\mathcal{D}\) accrues a cost rate \(J(\mathcal{D})\ge 0\), measured in energy, resources, or another booked scarce quantity in the units of the master equation of THEORY §2. A design that cannot cover \(J\) shrinks or is eliminated (ruin). This note uses \(J\) as already defined; it does not reopen the term list.

**A2 (copying or retention favors lower cost).** Among available designs, those with lower \(J\) are copied or retained at a higher rate. Three formalizations, of decreasing strength:

- **(A2-L) Linear Malthusian map.** \(m(\mathcal{D})=m_0-\alpha J(\mathcal{D})\) with \(\alpha>0\), and Wrightian birth rates \(r=\exp(m)\). This is the assumption of the existing bridge, not a theorem. Under this map, the THEORY §3 cost-to-fitness elasticity is \(\sigma=\lvert\mathrm{d}\log r/\mathrm{d}\log J\rvert=\alpha J\) at an operating point \(J\), so \(\alpha=\sigma/J^\star\) at the minimum.
- **(A2-M) Monotone map.** \(m\) is strictly decreasing in \(J\). Qualitatively, cheaper designs are favored. This does **not** give a Boltzmann law or the constant \(d/(2\beta)\).
- **(A2-P) Persistence only.** There is no copying: a held structure is retained while it covers its cost and is dropped when it does not. The Moran / Wright–Fisher theorems below do **not** apply. A persistence-only version is already listed as missing in `theory/SCALE_ENDS.md` §6b, and remains **OPEN**.

**A3 (the world drifts).** The location of \(\arg\min J\), or the world's statistics that enter \(J\), change with a positive variance rate \(\sigma^2>0\) (Brownian drift of the optimum, unless another process is named). The static world is the special case \(\sigma^2=0\), already treated by the bridge.

**What is not assumed.** Formal Axiom 7 of `reviews/night1/formal/AXIOMS.md` says the realized architecture satisfies \(J(A)\le\min J+\varepsilon\). That axiom *assumes* near-minimization. It is not a premise of this note; the point is to derive a scale for \(\varepsilon\). Frequency dependence, strong mutation, and a binding ruin constraint inside the stationary law are not assumed, and the theorems do not cover them.

## 3. Static world: the existing bridge, stated as a theorem

The results in this section are **KNOWN**. They are restated so the note is self-contained, with short proofs. They are not a new mathematical theorem. The application to the reduced cost \(J\), and the consistency note with the qualification band, are already in `core/bridge_2026-11-21/SELECTION.md`.

**Theorem SA1 (KNOWN: Sella and Hirsh 2005, applied to \(J\)).** Assume A1, A2-L, and a static world (\(\sigma^2=0\), or a frozen snapshot of A3). Consider a haploid Moran process of size \(N\) on a finite connected undirected design graph, in the weak-mutation regime (the population is typically monomorphic; substitutions are an origination–fixation chain), with equal mutation clocks on each undirected edge, and with no frequency dependence. Let \(r_i=\exp(-\alpha J(\mathcal{D}_i))\). Then the unique stationary distribution of the monomorphic chain satisfies

\[
\frac{\pi_i}{\pi_j}=\Bigl(\frac{r_i}{r_j}\Bigr)^{N-1},
\]

and therefore

\[
\pi(\mathcal{D})\;\propto\;\exp\bigl(-\beta J(\mathcal{D})\bigr),\qquad \beta=\alpha(N-1).
\]

For a diploid Wright–Fisher process the same argument gives \(\beta=\alpha(2N-1)\) in Sella and Hirsh's leading-order form (their stationary weight \(f^{2N-1}\), large \(N\)). In all these cases \(\beta\) is set by selection strength: population size times the fitness scale \(\alpha\).

*Proof.* In the weak-mutation limit the state is the currently fixed design. A mutant \(j\) arising in a monomorphic \(i\) population fixes with the standard haploid-Moran probability \(\varphi_{i\to j}=(1-\rho)/(1-\rho^N)\) for \(\rho=r_i/r_j\neq 1\), and \(1/N\) if \(r_i=r_j\). Detailed balance on an undirected edge with equal mutation clocks is \(\pi_i\,\varphi_{i\to j}=\pi_j\,\varphi_{j\to i}\). Substituting the fixation probabilities yields \(\varphi_{j\to i}/\varphi_{i\to j}=(r_i/r_j)^{N-1}\), hence \(\pi_i/\pi_j=(r_i/r_j)^{N-1}\). The algebra: with \(\rho=r_i/r_j\),

\[
\varphi_{i\to j}=\frac{1-\rho}{1-\rho^N}=\frac{\rho-1}{\rho^N-1},\qquad
\varphi_{j\to i}=\frac{1-\rho^{-1}}{1-\rho^{-N}}=\rho^{N-1}\frac{\rho-1}{\rho^N-1},
\]

so the ratio is \(\rho^{N-1}\). Then \(r=\exp(-\alpha J)\) gives \(\pi\propto\exp(-\alpha(N-1)J)\). Uniqueness follows from connectedness of the graph (one communicating class). This is the argument of Sella and Hirsh (2005, doi 10.1073/pnas.0501865102), following the free-fitness Lyapunov function of Iwasa (1988, doi 10.1016/s0022-5193(88)80243-1). □

**Theorem SA1b (KNOWN: equipartition).** Assume the conclusion of SA1, and assume that near the unique minimum, \(J(\theta)=J^\star+\tfrac12(\theta-\theta^\star)^\top H(\theta-\theta^\star)\) in \(d\) continuous design coordinates, with \(H\) symmetric positive definite, and that the Boltzmann measure can be treated as supported on this quadratic well (the tails in other basins are negligible at the \(\beta\) of interest). Then

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

**Corollary SA1c (KNOWN, already in the bridge).** Under the linear map of A2-L, \(\beta=\alpha(N_e-1)\approx\sigma N_e/J^\star\), so the typical *fractional* excess is

\[
\frac{\mathbb{E}[J]-J^\star}{J^\star}\;\approx\;\frac{d}{2\sigma N_e}.
\]

The approximation \(\beta\approx\sigma N_e/J^\star\) replaces \(\alpha(N_e-1)\) by \(\alpha N_e\) and evaluates \(\sigma=\alpha J\) at \(J^\star\). Both are leading-order.

**Closeness is now derived.** "Strongly selected" means \(\sigma N_e\gg d\): the typical fractional excess is then \(\ll 1\). Formal Axiom 7's tolerance \(\varepsilon\) has a scale. The existing qualification band \(\varepsilon=10/(\sigma N_e)\) of THEORY §3 / FRAMEWORK §9 is a *fractional* difference used to exclude a named rival (a one-dimensional comparison). The ratio of typical excess to that band is \(d/20\). For a few soft coordinates the expected scatter sits well inside the conservative band; for large \(d\) it need not. These uses are different. **This note does not change the locked factor of 10.** The factor of 10 is a conservative choice made in the repository, not a constant of Lynch, Ackerman, Gout, Long, Sung, Thomas and Foster (2016, doi 10.1038/nrg.2016.104), who are cited for the drift-barrier scale \(s N_e\approx 1\).

**Infinite-population limit (KNOWN geometry).** Fisher's fundamental theorem and the Shahshahani metric (Shahshahani 1979, doi 10.1090/memo/0211) say that, at infinite \(N\), selection is gradient ascent of mean fitness — equivalently gradient descent of mean \(J\) — in that metric. That is the \(\beta\to\infty\) limit of the same picture. Finite \(N\) replaces the point mass at the minimum by the Boltzmann spread. The geometry is credited; it is not used as a derivation of \(\pi\).

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

minimal at \(b^\star\) with value \(2\sqrt{kw\sigma^2/6}\). This is **KNOWN** (Dixit 1991, *Review of Economic Studies* 58:141, doi 10.2307/2298051, title "Analytical Approximations in Models of Hysteresis"; simplified treatment in *JEDC* 15:657, doi 10.1016/0165-1889(91)90037-2; exact at zero discounting, Chalkley 1997, *Economics Letters* 57:189, doi 10.1016/s0165-1765(97)00222-x; re-derived and checked as CL19).

**Theorem SA2 (PROVED in-model, under SA2-A–C).** Assume A1, A2-L, A3, the conclusion of SA1b for the \(y\)-coordinates, and Assumptions SA2-A–C. Then the long-run operational excess and the long-run total excess rate (including lumps) are, respectively,

\begin{align*}
\mathbb{E}[J(\mathcal{D}_t)-J_t^\star]
&\;=\; \frac{w b^{\star 2}}{6}+\frac{d}{2\beta}
\;=\; \sqrt{\frac{kw\sigma^2}{6}}+\frac{d}{2\beta},\\[4pt]
\mathbb{E}[J_R]-J^\star_{\mathrm{drift}}
&\;=\; 2\sqrt{\frac{kw\sigma^2}{6}}+\frac{d}{2\beta}.
\end{align*}

The two Dixit values differ by the amortized redesign cost, which equals the operational gap cost at the optimal band. A statement about "how close the held design sits to \(J^\star\)" must use the first display; a statement about "how much extra cost rate a lineage pays in a drifting world" must use the second. Conflating them is a mistake.

*Proof.* Linearity of expectation applied to SA2-A gives \(\mathbb{E}[J-J_t^\star]=\mathbb{E}[w x^2]+\mathbb{E}[\tfrac12 y^\top H y]\), with no independence required for the sum of means. Under SA2-B the second term is \(d/(2\beta)\) by SA1b. Under SA2-C the first term is \(w b^{\star 2}/6\). Substituting \(b^{\star 4}=6k\sigma^2/w\) yields \(w b^{\star 2}/6=\sqrt{kw\sigma^2/6}\). Adding the amortized lumps \(k\sigma^2/b^{\star 2}\), which equals the same value at \(b^\star\), gives the \(J_R\) display. □

Independence of \(x\) and \(y\) is not required for these means, but it is required if one wants the joint law to be the product of the Dixit occupation and the Boltzmann measure (for example to compute quantiles, or \(\mathrm{Var}(J)\)). The Dixit occupation density on a cycle is derived in the checks file: \(\rho(x)=(b-|x|)/b^2\) on \([-b,b]\) (a triangular density). The addition of means is also checked there (**NUMERICAL** as a check).

**When SA2 is not claimed.** If adjustment is smooth (\(k=0\), \(\kappa>0\)), there is no inaction band (CL19(c)), and §5 applies instead. If the \(y\)-chain does not mix inside a cycle, or the Hessian depends on \(x\), the sum is **OPEN**. If the world is a step of size \(\Delta\) lasting a regime \(T\), the CL19(b) threshold \(\Delta_k=\sqrt{k/(wT)}\) replaces the fourth-root band; the present note does not add a scatter theorem for that case beyond SA1 inside a regime.

## 5. Smooth tracking of a moving optimum

Lumpy redesign is not the only response to A3. If the design can move continuously, the lag is a tracking lag, not an inaction band.

**Proposition SA3 (PROVED in-model, infinite-population gradient dynamics).** Assume A2-L and \(J=J^\star+w(\theta-\theta^\star)^2\) in one trait (so the Hessian is \(H=2w\)). Let the mean phenotype \(\mu\) follow Lande's selection-gradient dynamics \(\mathrm{d}\mu/\mathrm{d}t=V_G\,\partial m/\partial\theta\), with additive genetic variance \(V_G>0\) treated as given. Then \(\mathrm{d}\mu/\mathrm{d}t=\lambda(\theta^\star-\mu)\) with \(\lambda=2\alpha w V_G\).

- If \(\theta^\star\) moves at constant speed \(v\), the lag is \(L=\mu-\theta^\star\to -v/\lambda\), and the operational excess is \(w(v/\lambda)^2=v^2/(4\alpha^2 w V_G^2)\).
- If \(\mathrm{d}\theta^\star=\sigma_\theta\,\mathrm{d}W\) (Brownian optimum), the lag is an Ornstein–Uhlenbeck process, \(\mathrm{Var}(L)=\sigma_\theta^2/(2\lambda)\), and \(\mathbb{E}[w L^2]=\sigma_\theta^2/(4\alpha V_G)\). The curvature \(w\) cancels: a steeper well costs more per unit lag but is tracked faster.

*Proof.* Under A2-L, \(\partial m/\partial\theta=-2\alpha w(\mu-\theta^\star)\) at the mean, hence \(\lambda=2\alpha w V_G\). Constant speed: in the moving frame, \(\dot L=-\lambda L-v\), with unique rest point \(L=-v/\lambda\). Brownian optimum: \(L=\mu-\theta^\star\) satisfies \(\mathrm{d}L=-\lambda L\,\mathrm{d}t-\sigma_\theta\,\mathrm{d}W\), whose stationary variance is \(\sigma_\theta^2/(2\lambda)\). Then \(\mathbb{E}[w L^2]=w\sigma_\theta^2/(4\alpha w V_G)\). □

**Credit, and a limit on the credit.** The gradient dynamics of the mean are Lande's (1976, *Evolution* 30:314–334, doi 10.1111/j.1558-5646.1976.tb00911.x; JSTOR 10.2307/2407703). The program of adaptation and extinction under a changing environment is that of Bürger and Lynch (1995, *Evolution* 49:151–163, doi 10.1111/j.1558-5646.1995.tb05967.x; JSTOR 10.2307/2410301). Mustonen and Lässig (2010, *PNAS* 107:4248–4253, doi 10.1073/pnas.0907953107), already in `litmap/LITMAP.md`, treat adaptation that lags a moving optimum ("fitness seascapes") and introduce fitness flux. **This note does not borrow a numerical constant or an extinction threshold from Bürger and Lynch or from Mustonen and Lässig:** the papers were identified and their DOIs verified, but their internal formulas were not re-derived from the texts. The constants in SA3 are the ones just proved, in this notation, under the stated dynamics. \(V_G\) is an input, not derived from the weak-mutation chain of SA1; SA3 and SA1 are different regimes (polymorphic quantitative variance versus a typically monomorphic origination–fixation chain).

## 6. Time, mutation, and reachability

**Proposition SA4 (qualitative; no new constant).** The stationary statements SA1–SA2 assume that the origination–fixation chain has mixed, and, for field application, that at least the ten redesign times already required by THEORY §3 have been spent in one world. They do not give a closeness guarantee at finite time, or on a mutation graph that cannot reach the minimum.

- **Waiting time.** In the weak-mutation regime the mixing time is set by waiting for mutations and by fixation times. A very small mutation rate slows approach; it does not change the *stationary* scatter \(d/(2\beta)\). A very large mutation rate leaves the typically-monomorphic assumption, and SA1 is not claimed (strong mutation is outside the theorem).
- **Metastability.** At large \(\beta\), valleys block the chain on relevant timescales. EVO1 worlds W4 and W4b are the in-model examples already on record (CLAIM_MAP Q5–Q6, SIM-FAIL on the proxy): the Boltzmann law assumes the graph can traverse the space. A disconnected or valley-blocked graph is a different process. This is compatible with SA1, not a rescue of those FAILs and not a failure of SA1.
- **The Price identity (KNOWN).** Price (1970, *Nature* 227:520–521, doi 10.1038/227520a0) accounts for the change in a mean. Under A2-L in a static world, \(\mathrm{d}\mathbb{E}[J]/\mathrm{d}t=\mathrm{Cov}(m,J)=-\alpha\,\mathrm{Var}(J)\le 0\): the mean cost declines at a rate set by the variance of cost in the population. When A3 moves \(J^\star\), a tracking term appears. The identity does not, by itself, give the distance to the minimum. A quantitative decay rate would need a bound of \(\mathrm{Var}(J)\) in terms of the excess (a Poincaré or log-Sobolev step), which is not claimed here.

**Dimensionality and Fisher's geometric model.** Orr (1998, *Evolution* 52:935–949, doi 10.1111/j.1558-5646.1998.tb01823.x; JSTOR 10.2307/2411226) analyzes Fisher's geometric model of adaptation: the chance that a random mutation is beneficial falls as the phenotypic dimension rises. That is a statement about the *arrival* of improving steps, not about the stationary scatter \(d/(2\beta)\). It is relevant to SA4 (approach can be slow in high dimension) and to the reading of \(d\) in SA1b (more soft coordinates mean more residual excess at fixed \(\beta\)). Fisher's 1930 book is cited as the source of the geometric picture; it has no Crossref DOI.

## 7. Prior art, checked and limited to what is used

Every DOI below was verified on Crossref on 21 November 2026. No citation is invented. Books are marked as books.

- **Sella and Hirsh (2005)** and **Iwasa (1988)** are the source of the free-fitness / Boltzmann stationary law (SA1). Sella and Hirsh already note that the load in finite populations follows from the same argument. The present \(d/(2\beta)\) is that load, in cost units, for a quadratic well.
- **Ohta (1973, *Nature* 246:96–98, doi 10.1038/246096a0)**, "Slightly Deleterious Mutant Substitutions in Evolution," is the nearly-neutral statement that finite \(N\) lets slightly costlier types fix. That is the same intuition as a positive scatter at finite \(\beta\). This note does not attribute the constant \(d/(2\beta)\) to Ohta.
- **Kimura (1968, *Nature* 217:624–626, doi 10.1038/217624a0)**, "Evolutionary Rate at the Molecular Level," is the neutral substitution-rate argument. It is not a drift-load formula and is not used as one. It is listed because it is the usual companion paper, and to say plainly that it is a different result.
- **Classical mutation-selection balance** (standing polymorphism; the load of order the deleterious mutation rate under strong selection against rare alleles) lives in a different regime from the typically monomorphic chain of SA1. As \(\beta\to\infty\) the monomorphic-chain scatter \(d/(2\beta)\) vanishes; a polymorphism load need not. SA1 does not include that load, and does not refute it.
- **Lande (1976), Bürger and Lynch (1995), Mustonen and Lässig (2010):** see §5. Credit for the moving-optimum program; no borrowed constants.
- **Price (1970):** see §6. An accounting identity, not a distance theorem.
- **Orr (1998) / Fisher's geometric model:** see §6.
- **Shahshahani (1979):** geometry of the infinite-population replicator, already in the bridge.
- **Potential games.** Monderer and Shapley (1996, *Games and Economic Behavior* 14:124–143, doi 10.1006/game.1996.0044), already used in CLAIM_MAP CT31, give Nash = \(\arg\min\) of an exact potential. That is **ANALOGY** to "selection favors lower \(J\)" when \(J\) *is* the potential (as in the aggregative class of CT31). It is not a derivation of the Boltzmann \(\pi\) of SA1.
- **Stochastic replicator dynamics** (Langevin or other finite-\(N\) perturbations of the replicator) also produce fluctuations that shrink with \(N\). This note does not identify those fluctuations with \(\pi\propto e^{-\beta J}\) and does not claim a specific formula from that literature.
- **Dixit (1991) and Chalkley (1997):** the lumpy-redesign lag, already CL19.
- **Lynch et al. (2016):** the drift-barrier scale behind the existing qualification band; the factor of 10 remains the repository's conservative choice.

## 8. What this does not show

- It does not make the hypothesis a physical law, and it is not a theory of everything.
- It does not identify \(\beta\), or the ruin-constraint scale \(z=B/(\sigma\tau^H)\) of CT18, with temperature in kelvin. Those are two different quantities (see the bridge's `BRIDGE.md`). The symbol \(\sigma\) in \(z\) is the CT18 shock scale, not the cost-to-fitness map \(\sigma\) of THEORY §3, and not the world-drift rate \(\sigma^2\) of A3.
- It does not put the ruin cap \(P(\mathrm{ruin})\le\varepsilon_r\) into \(\pi\). Feasibility remains a constraint on the design set.
- It does not cover strong mutation, standing polymorphism, frequency dependence, a nonlinear map \(m(J)\), or the persistence-only process A2-P.
- It does not give closeness at finite time, or on a valley-blocked graph (SA4; EVO1 W4/W4b).
- It does not rescue T27's P3, which failed in-model and is not rescued.
- It does not, by itself, change the Part 2 hypothesis sentence, the locked factor of 10, or THEORY.md's main text. THEORY §4 still records near-minimization as an assumption, because this note is not yet folded into the canonical statement. The derivation proposed here is the candidate for that later fold, not the fold itself.
- It does not show that any real class satisfies A1–A3 with parameters that make the remainder small. That is the remaining empirical bet.

## 9. A falsifiable quantitative consequence (OPEN, not locked)

**SA-P1 (OPEN, not locked, not a test until preregistered).** In a class that qualifies under THEORY §3, with \((\sigma, N_e, d)\) measured independently of the design under test, and, if adjustment is lumpy, with \((k, w, \sigma^2)\) likewise measured and preregistered as already required for the CL19 band (CT41): after at least ten redesign times in one world, the lag-corrected fractional excess

\[
\frac{\overline{J}-J^\star_{\mathrm{proxy}}-\Delta_{\mathrm{lag}}}{J^\star_{\mathrm{proxy}}}
\]

sits within a factor of three of \(d/(2\sigma N_e)\). Here \(\Delta_{\mathrm{lag}}=2\sqrt{kw\sigma^2/6}\) if the comparison is a long-run *total* cost rate including lumps, or \(\sqrt{kw\sigma^2/6}\) if it is the operational excess of the held design; the preregistration must choose one and stick to it. If adjustment is smooth or the class preregisters \(k=0\), \(\Delta_{\mathrm{lag}}\) is omitted and SA3 is not substituted unless its inputs, including \(V_G\), are themselves preregistered.

**Kill conditions.**

1. *Scale.* If, in a qualifying class with the inputs measured as above, the lag-corrected fractional excess is systematically larger than \(3\times d/(2\sigma N_e)\), the quantitative remainder, as applied to that class, fails. (This can mean A2-L fails, timescales are not separated, the graph did not mix, or the axioms do not hold for the class. It kills the quantitative application, not the qualitative claim that lower \(J\) is favored.)
2. *Slope.* If, across at least two qualifying classes, or across a preregistered grid of \(\sigma N_e\) in one class, the log–log slope of the lag-corrected fractional excess on \(\sigma N_e\) lies outside \([-1.5,-0.5]\), the \(1/(\sigma N_e)\) scaling is rejected.
3. *Too close.* An excess much smaller than predicted is a warning (overestimated \(d\), or less residual variation than modeled). This note does not lock a one-sided "too close" kill; one can be added when a class is preregistered.
4. *Not a test.* If the class does not qualify, if the inputs are not independent of the design, if the lag term is used without preregistered \((k,w,\sigma^2)\), or if fewer than ten redesign times have been spent, the status is NOT A TEST, not a pass and not a fail.

SA-P1 is a dated sketch, in the same sense as the layer-lifetime predictions: **OPEN**, not locked, and not a test until a class, the inputs, and the factor are preregistered. It does not change any locked file.

## 10. The Part 2 hypothesis sentence

The sentence stays byte-identical, including the word "law" in a sentence that labels itself a hypothesis. What changes is the *logical status* of "strongly selected \(\Rightarrow\) close": under A1, A2-L, and the regularity of SA1–SA2, that implication is a theorem, with an explicit remainder. The remaining empirical claim is that real systems in a qualifying class satisfy the axioms with parameters that make the remainder small, and that \(J\) as written is the cost that A2 acts on. That is a smaller, sharper bet. It is not yet a field result.

## 11. Relation to the existing bridge and to T27

This note **builds on** `core/bridge_2026-11-21/`, rather than replacing it. Theorem SA1 and Corollary SA1c are the bridge's theorem and consistency note, restated. The official T27 test of that package (locked `PREREG.md`, hashes unchanged) remains: P1 passed (3/3), P2 passed (3/3), P3 failed (0/3) and is not rescued. P3's operationalization (a two-\(K\) mass floor at low \(\beta\)) was already missed by the exact Boltzmann measure on the pilot; the failure is about that operationalization, not a refutation of SA1. Nothing in SA2 repairs P3.

## 12. Numerical checks

The algebraic identities of SA1b, the Dixit occupation and the two CL19 values, and the addition of means in SA2, are checked by `tools/selection_axioms_checks.py`, run by `tools/test_selection_axioms_checks.py`. Those checks are **NUMERICAL**. They are not a substitute for the proofs above. They do not re-run T27 and do not touch locked hashes.

## References

Verified on Crossref, 21 November 2026, America/New_York, unless marked as a book.

- Bürger, R. & Lynch, M. 1995, *Evolution* 49:151–163, doi 10.1111/j.1558-5646.1995.tb05967.x (JSTOR 10.2307/2410301), "Evolution and Extinction in a Changing Environment: A Quantitative-Genetic Analysis."
- Chalkley, J. 1997, *Economics Letters* 57:189, doi 10.1016/s0165-1765(97)00222-x.
- Dixit, A. 1991, *Review of Economic Studies* 58:141, doi 10.2307/2298051, "Analytical Approximations in Models of Hysteresis"; *Journal of Economic Dynamics and Control* 15:657, doi 10.1016/0165-1889(91)90037-2.
- Fisher, R. A. 1930, *The Genetical Theory of Natural Selection* (book; no Crossref DOI).
- Iwasa, Y. 1988, *Journal of Theoretical Biology* 135:265–281, doi 10.1016/s0022-5193(88)80243-1, "Free fitness that always increases in evolution."
- Kimura, M. 1968, *Nature* 217:624–626, doi 10.1038/217624a0, "Evolutionary Rate at the Molecular Level."
- Lande, R. 1976, *Evolution* 30:314–334, doi 10.1111/j.1558-5646.1976.tb00911.x (JSTOR 10.2307/2407703), "Natural Selection and Random Genetic Drift in Phenotypic Evolution."
- Lynch, M., Ackerman, M. S., Gout, J.-F., Long, H., Sung, W., Thomas, W. K. & Foster, P. L. 2016, *Nature Reviews Genetics* 17:704–714, doi 10.1038/nrg.2016.104, "Genetic drift, selection and the evolution of the mutation rate."
- Monderer, D. & Shapley, L. S. 1996, *Games and Economic Behavior* 14:124–143, doi 10.1006/game.1996.0044, "Potential Games."
- Mustonen, V. & Lässig, M. 2010, *Proceedings of the National Academy of Sciences* 107:4248–4253, doi 10.1073/pnas.0907953107, "Fitness flux and ubiquity of adaptive evolution."
- Ohta, T. 1973, *Nature* 246:96–98, doi 10.1038/246096a0, "Slightly Deleterious Mutant Substitutions in Evolution."
- Orr, H. A. 1998, *Evolution* 52:935–949, doi 10.1111/j.1558-5646.1998.tb01823.x (JSTOR 10.2307/2411226), "The Population Genetics of Adaptation: The Distribution of Factors Fixed during Adaptive Evolution."
- Price, G. R. 1970, *Nature* 227:520–521, doi 10.1038/227520a0, "Selection and Covariance."
- Sella, G. & Hirsh, A. E. 2005, *Proceedings of the National Academy of Sciences* 102:9541–9546, doi 10.1073/pnas.0501865102, "The application of statistical physics to evolutionary biology."
- Shahshahani, S. 1979, *Memoirs of the American Mathematical Society* 17, no. 211, doi 10.1090/memo/0211, "A new mathematical framework for the study of linkage and selection."
