# Drift selection: closeness to a moving cost minimum

*Saturday 21 November 2026, evening, America/New_York. Branch `drift-selection-2026-11-21`, draft PR. Written by one executor for Chad Mitchell; a self-check, not independently reviewed. Builds on `theory/SELECTION_AXIOMS.md` (A1, A2-L, SA1–SA4) and `theory/DYNAMICS.md` (CL19). It does not change the Part 2 hypothesis sentence, THEORY §4, CORE (beyond a one-line pointer), the locked factor of 10, or any locked preregistration or hash file.*

## 0. Bottom line

**In plain words.** In a static world, the weak-mutation substitution chain of SA1 leaves a lineage, on average, \(d/(2\beta)\) above the cost minimum. If the minimum itself wanders, the lineage also lags behind it. In the diffusion limit of the chain (lattice steps small compared with the scatter), with a quadratic cost and an optimum that wanders as a Brownian or Ornstein–Uhlenbeck process, the time-averaged excess is the static scatter plus a tracking term:

\[
\overline{J-J^\star}\;=\;\frac{d}{2\beta}\;+\;\frac12\,\mathrm{Tr}\!\bigl[H\,(D_m\beta H+\gamma I)^{-1}Q\bigr].
\]

For an optimum that wanders as Brownian motion with the same diffusion coefficient \(D\) in every whitened coordinate, this is

\[
\overline{J-J^\star}\;=\;\frac{d}{2\beta}\Bigl(1+\frac{D}{D_m}\Bigr),
\]

where \(D_m=\mu\delta^2/(2d)\) is how fast neutral substitutions wander. A wandering world acts like a higher temperature: it multiplies the static scatter by \(1+D/D_m\). The curvature of the cost well cancels. Closeness therefore needs \(\sigma N_e\gg d\,(1+D/D_m)\), not just \(\sigma N_e\gg d\).

**Where it stops holding.** (i) If the world fluctuates faster than the chain relaxes (\(\gamma\gg D_m\beta\lambda\)), the chain cannot follow. It settles near the time-averaged optimum, and its excess over the *instantaneous* minimum tends to the cost of not tracking at all, \(\tfrac12\mathrm{Tr}(HQ/\gamma)\). Selection on the slow chain cannot remove that cost. Only within-lifetime judgment (sensing and memory, the terms of \(J\)) can. (ii) The chain has a hard speed limit. Each coordinate moves on average slower than \(v_{\max}=N\mu\delta/(2d)\), the rate at which mutants pointing that way arise. An optimum moving steadily faster than that outruns the chain: the lag grows without bound and the time-averaged excess diverges (DS2, proved for the exact chain). (iii) Between the linear regime and the speed limit the formula is not claimed. The simulations show it stays within a few percent somewhat beyond its stated conditions, and drifts upward as steps stop being small (DS3, open).

**Status, honestly.** The tracking formula is **PRIOR ART in substance**: Held, Nourmohammad and Lässig (2014) derive an equilibrium load plus an adaptive load that is linear in the driving rate when the peak moves slowly and saturates at the peak's variance when it moves fast, for a one-dimensional quantitative trait. Their fast-driving limit matches ours exactly; for the slow-driving coefficient our mapping of their notation leaves an unresolved factor of 2 (§5), so the coefficient used here is our own, checked by simulation. The static equipartition \(d/2\) in scaled units is older still (they cite Hartl and Taubes 1998, Poon and Otto 2000, Tenaillon et al. 2007). What is done here: the \(d\)-dimensional trace form with a general Hessian and a general mutation matrix (an elementary Lyapunov step), its statement in the repository's \(\beta\) and \(J\) notation, the speed-limit bound for the exact chain, the drift-adjusted closeness condition, and a simulation of the exact lattice Moran chain against the formula. None of it is new mathematics in a strong sense. **The packaging is what is new:** the drifting-world version of "selection puts a lineage near the minimum" is now a derived remainder with explicit conditions and an explicit failure regime, not a primitive.

**What this does not close.** CLAIM_MAP CX1 is recorded as *Theorem P* (the information floor CT1–CT4) for worlds with stationary increments. That is a different claim: a floor that every design pays, not how close selection brings a lineage to the minimum. CX1 stays **OPEN**. This note closes the selection-side gap that `SELECTION_AXIOMS.md` §4 left open (the optimum moving in the soft coordinates) in the diffusion limit. It does not prove anything about Theorem P.

## 1. Status words

As in `theory/SELECTION_AXIOMS.md` §1. **PROVED (in-model)** means proved inside the stated model, which says nothing by itself about nature. **SKETCH** means an argument with a stated gap. **NUMERICAL** means computed, not proved. **PRIOR ART** / **KNOWN** means published and credited. **OPEN** means not derived or not tested, not refuted.

## 2. Model

Everything in SA1 is kept: A1 (persistence has a cost), A2-L (Wrightian birth rate \(r=\exp(m_0-\alpha J)\), \(\alpha\) constant), a haploid Moran population of size \(N\), weak mutation \(N\mu\ll 1\) per generation so the population is typically monomorphic, no frequency dependence. \(\beta=\alpha(N-1)\). The design space is a uniform lattice \(\delta\mathbb{Z}^d\) in coordinates \(\theta\) where mutation clocks are equal (SA1b's whitened coordinates): a mutant steps \(\pm\delta\) along one of the \(2d\) axes, each with probability \(1/(2d)\).

**DS-A (quadratic cost with a moving centre).** \(J(\theta,t)=J^\star+\tfrac12(\theta-\theta^\star_t)^\top H(\theta-\theta^\star_t)\), with \(H\) constant and symmetric positive definite and \(J^\star\) constant. Only the centre moves. (A moving \(J^\star\) adds nothing to the excess; a moving \(H\) is not covered.)

**DS-B (the world).** The centre follows one of:
- Ornstein–Uhlenbeck: \(\mathrm{d}\theta^\star=-\gamma\theta^\star\,\mathrm{d}t+\sqrt{2Q}\,\mathrm{d}B\), \(\gamma>0\), \(Q\) symmetric positive semidefinite (stationary covariance \(Q/\gamma\));
- Brownian: the same with \(\gamma=0\) (A3 of `SELECTION_AXIOMS.md`, with variance rate \(2Q\); in one coordinate A3's \(\sigma^2\) is \(2D\));
- constant velocity: \(\theta^\star_t=\theta^\star_0+vt\).

The world is exogenous: the lineage does not move \(\theta^\star\) (CX2 excluded).

**The chain.** A mutant arising in direction \(e\) from the fixed design \(\theta\) fixes with the exact Moran probability \(\varphi(x)=(1-e^{x})/(1-e^{Nx})\), \(x=\alpha\,[J(\theta+\delta e)-J(\theta)]\). Origination in each direction is at rate \(N\mu/(2d)\). The jump rate in direction \(e\) is therefore \(\tfrac{N\mu}{2d}\varphi(x_e)\); the neutral substitution rate is \(\mu\).

**Symbols.** \(D_m=\mu\delta^2/(2d)\) is the per-coordinate diffusion coefficient of the neutral substitution walk. \(\lambda\) is an eigenvalue of \(H\). The chain's relaxation rates are \(a=D_m\beta\lambda\). \(\varepsilon_{\mathrm{lat}}=\delta^2\beta\lambda_{\max}(1+\mathrm{tr}\,Q/(d D_m))\) measures lattice coarseness against the drift-inflated scatter. \(\sigma\), \(N_e\) are THEORY §3's elasticity and effective size, as in SA1c; they are not A3's drift rate.

## 3. The diffusion limit of the chain (KNOWN technique)

For a smooth test function \(f\), the chain's generator is \(\mathcal{L}f(\theta)=\sum_{e}\tfrac{N\mu}{2d}\varphi(x_e)\,[f(\theta+\delta e)-f(\theta)]\). With \(x_e=\alpha\delta\,e\cdot\nabla J+O(\alpha\delta^2)\) and \(\varphi(x)=\tfrac1N\bigl(1-\tfrac{N-1}{2}x+O(N^2x^2)\bigr)\), pairing \(+e\) with \(-e\) gives

\[
\mathcal{L}f=D_m\,\Delta f-D_m\beta\,\nabla J\cdot\nabla f\;+\;O(\varepsilon)\,,
\]

the generator of the Langevin equation

\[
\mathrm{d}\theta=-D_m\beta\,\nabla_\theta J\,\mathrm{d}t+\sqrt{2D_m}\,\mathrm{d}W. \tag{L}
\]

The error is small when steps are small compared with the scatter (\(\varepsilon_{\mathrm{lat}}\ll 1\), which also makes \(N|x_e|\ll1\) at typical lags) and when the world moves little per substitution (\(\gamma\ll\mu\), and \(\mathrm{tr}\,Q/\mu\) small against the scatter, included in \(\varepsilon_{\mathrm{lat}}\)). In a static world (L) has stationary density \(\propto e^{-\beta J}\), which is SA1's weight: the limit is consistent with the exact detailed balance. Passing from a Markov chain to its diffusion limit by generator convergence is standard (Ethier and Kurtz 1986). **What is not proved here:** convergence of the chain's *time-averaged excess* to that of (L) as \(\varepsilon_{\mathrm{lat}}\to0\) (it needs uniform integrability of the stationary laws). It is checked numerically in §7. Origination–fixation chains as models are reviewed by McCandlish and Stoltzfus (2014).

The weak-mutation requirement and the diffusion limit do not conflict. \(N\mu\ll1\) is about generations (fixation is fast compared with origination). The diffusion limit is about lattice steps compared with the scatter, in time measured in substitutions.

## 4. Theorem DS1 (tracking excess in the diffusion limit)

**Theorem DS1 (PROVED (in-model) for (L); PRIOR ART in substance; see §5).** Assume DS-A, DS-B and dynamics (L) for the design, with the world independent of the mutational noise. Let \(L_t=\theta_t-\theta^\star_t\) be the lag.

(a) *OU or Brownian world.* The pair \((L,\theta^\star)\) (Brownian: \(L\) alone) has a unique stationary distribution, and the long-run time average of \(J-J^\star\) equals its stationary mean, almost surely:

\[
\overline{J-J^\star}=\frac{d}{2\beta}+\frac12\mathrm{Tr}\bigl[H(D_m\beta H+\gamma I)^{-1}Q\bigr].
\]

(b) *Brownian world* (\(\gamma=0\)): \(\overline{J-J^\star}=\dfrac{d}{2\beta}+\dfrac{\mathrm{Tr}\,Q}{2\beta D_m}\). It does not depend on \(H\). With \(Q=DI\): \(\dfrac{d}{2\beta}(1+D/D_m)\). With a general constant mutation matrix \(M\) in place of \(D_mI\) (anisotropic clocks or steps): \(\dfrac{d}{2\beta}+\dfrac{\mathrm{Tr}(M^{-1}Q)}{2\beta}\).

(c) *Constant velocity:* \(\overline{J-J^\star}=\dfrac{d}{2\beta}+\dfrac{v^\top H^{-1}v}{2\beta^2D_m^2}\).

(d) *Limits.* \(Q=0\) gives SA1b. As \(\gamma\to\infty\) at fixed \(Q/\gamma\), the tracking term tends to \(\tfrac12\mathrm{Tr}(HQ/\gamma)\), the excess of a design that never moves from the mean optimum.

*Proof.* Write \(A=D_m\beta H\). By (L), \(\mathrm{d}L=-AL\,\mathrm{d}t+\gamma\theta^\star\mathrm{d}t+\sqrt{2D_m}\,\mathrm{d}W-\sqrt{2Q}\,\mathrm{d}B\). All eigenvalues of \(A\) are positive, so the linear system is stable and has a unique Gaussian stationary distribution, and time averages of quadratic functions converge to their stationary means (ergodic theorem for stable linear SDEs). Let \(P=\mathbb{E}[LL^\top]\), \(C=\mathbb{E}[L\theta^{\star\top}]\), \(S=\mathbb{E}[\theta^\star\theta^{\star\top}]=Q/\gamma\). Itô's rule at stationarity gives
\(0=-(A+\gamma I)C+\gamma S-2Q\), so \(C=-(A+\gamma I)^{-1}Q\); and
\(0=-AP-PA+\gamma(C+C^\top)+2D_mI+2Q\).
Take the trace of the second identity. Because \(A=D_m\beta H\), \(\mathrm{Tr}(AP+PA)=2D_m\beta\,\mathrm{Tr}(HP)\). So
\(D_m\beta\,\mathrm{Tr}(HP)=dD_m+\mathrm{Tr}\,Q-\gamma\,\mathrm{Tr}[(A+\gamma I)^{-1}Q]=dD_m+\mathrm{Tr}[(A+\gamma I)^{-1}AQ]\).
Divide by \(2D_m\beta\) and use \(A=D_m\beta H\): \(\tfrac12\mathrm{Tr}(HP)=\tfrac{d}{2\beta}+\tfrac12\mathrm{Tr}[H(A+\gamma I)^{-1}Q]\). Since \(J-J^\star=\tfrac12L^\top HL\), this is (a). For \(\gamma=0\) the \(C\) terms vanish and the trace gives (b). For general \(M\), the drift is \(-\beta MH L\) and the noise covariance \(2M+2Q\); in coordinates \(\tilde L=M^{-1/2}L\) the mutation matrix is \(I\), the Hessian \(M^{1/2}HM^{1/2}\) and the world covariance \(M^{-1/2}QM^{-1/2}\); the trace of the Brownian case is then \(d/(2\beta)+\mathrm{Tr}(M^{-1}Q)/(2\beta)\). (c): in the moving frame \(\mathrm{d}L=-AL\,\mathrm{d}t-v\,\mathrm{d}t+\sqrt{2D_m}\mathrm{d}W\); the mean lag is \(-A^{-1}v\), the fluctuation is SA1b's, and \(\tfrac12(A^{-1}v)^\top H(A^{-1}v)=v^\top H^{-1}v/(2\beta^2D_m^2)\). (d) is the limit of the formula. □

The closed form is checked against a direct Lyapunov solve for random \(H\), \(Q\), \(M\), \(\gamma\) in `tools/drift_selection_checks.py` (**NUMERICAL** check, agreement to \(10^{-9}\)).

**Conditions on (c).** The drift approximation needs a small fitness step at the mean lag, \(N\alpha\delta\lvert H\bar L\rvert\ll1\), i.e. \(\lvert v\rvert\ll D_m/\delta=\mu\delta/(2d)\): the optimum must move slower than the *neutral* substitution speed scale. Beyond that, see DS3.

**Corollary DS1c (fractional form, same caveats as SA1c).** With \(\beta=\sigma N_e/J^\star\) at leading order and an isotropic Brownian world,
\[
\frac{\overline{J}-J^\star}{J^\star}\approx\frac{d\,(1+D/D_m)}{2\sigma N_e}.
\]
So the drifting-world version of "strongly selected implies close" needs \(\sigma N_e\gg d\,(1+D/D_m)\). This is a statement in the model. It does not change THEORY §3's qualification band or its locked factor of 10.

**Consistency with SA3.** SA3 (Lande gradient dynamics, polymorphic, \(V_G\) given) gives \(\mathbb{E}[wL^2]=\sigma_\theta^2/(4\alpha V_G)=D/(2\alpha V_G)\) for a Brownian optimum with \(\sigma_\theta^2=2D\). DS1(b) in one coordinate is \(D/(2\alpha(N-1)D_m)\). The two coincide if \(V_G\) is replaced by \((N-1)D_m\). This is a consistency observation between two different regimes, not a derivation of \(V_G\).

## 5. Prior art, and what is packaging

Every DOI below was checked on Crossref on 21 November 2026 (America/New_York). No citation is invented. Constants from these papers are not borrowed unless stated.

- **Held, Nourmohammad and Lässig (2014)**, "Adaptive evolution of molecular phenotypes", *J. Stat. Mech.* P09029, doi 10.1088/1742-5468/2014/09/P09029. A quantitative trait under mutation, drift and a single-peak *fitness seascape* whose peak performs an OU walk. In scaled units they write the mean load as an equilibrium part (\(2NL_{\rm eq}\simeq 1/2\), and \(d/2\) for a \(d\)-component trait, which they call the evolutionary equipartition theorem) plus an adaptive part that is \(\upsilon\tilde\tau(c)\) for slow driving and saturates at \(c\,r^2\), the cost of the peak's variance, for fast driving (their eqs. 53–54 in the arXiv version, 1403.1803). Their fast-driving saturation is exactly our DS1(d) (in fitness units, \(c_0\) times the peak's variance). For the slow-driving coefficient, our own mapping of their notation (their trait-mean diffusion coefficient \(\langle\Delta\rangle/2N\) written as our \(D_m\), their \(\upsilon_0\) as our \(D\)) gives \(2NL_{\rm ad}\simeq D/D_m\) from their eq. 54, while DS1(b) in the same units gives \(D/(2D_m)\). We could not resolve this factor of 2 from their text; it may be a diffusion-coefficient convention or our misreading. The coefficient stated here is the one derived in §4 and checked against the exact lattice chain in §7, not one borrowed from them. **DS1 is therefore prior art in substance.** This mapping was done from their text, not by re-deriving their eqs. 33–34.
- **Nourmohammad, Schiffels and Lässig (2013)**, *J. Stat. Mech.* P01012, doi 10.1088/1742-5468/2013/01/P01012, "Evolution of molecular phenotypes under stabilizing selection" (the static companion: diffusion equations for trait mean and diversity, low-mutation Boltzmann limit), and **Nourmohammad, Held and Lässig (2013)**, *Curr. Opin. Genet. Dev.* 23:684–693, doi 10.1016/j.gde.2013.11.001, "Universality and predictability in molecular quantitative genetics."
- **Mustonen and Lässig (2009)**, *Trends Genet.* 25:111–119, doi 10.1016/j.tig.2009.01.002, "From fitness landscapes to seascapes: non-equilibrium dynamics of selection and adaptation"; **(2008)**, *Phys. Rev. Lett.* 100:108101, doi 10.1103/PhysRevLett.100.108101, "Molecular Evolution under Fitness Fluctuations"; **(2010)**, *PNAS* 107:4248–4253, doi 10.1073/pnas.0907953107, "Fitness flux and ubiquity of adaptive evolution." The seascape framing and fitness flux. Not used for constants.
- **Static equipartition.** Held et al. credit the \(d/2\) equilibrium load to Hartl and Taubes (1998), *Genetica* 102–103:525–533, doi 10.1023/a:1017071901530, "Towards a theory of evolutionary adaptation"; Poon and Otto (2000), *Evolution* 54:1467–1479, doi 10.1111/j.0014-3820.2000.tb00693.x, "Compensating for our load of mutations: freezing the meltdown of small populations"; and Tenaillon, Silander, Uzan and Chao (2007), *PLoS ONE* 2:e217, doi 10.1371/journal.pone.0000217, "Quantifying Organismal Complexity using a Population Genetic Approach." **Flag for `SELECTION_AXIOMS.md`:** that note credits Sella and Hirsh (2005) for the weight and calls \(d/(2\beta)\) equipartition "under that weight". Row R1 is already PRIOR ART, so no status changes, but R1's credit should add these three papers in a later pass. This note does not edit R1.
- **de Vladar and Barton (2011)**, *J. R. Soc. Interface* 8:720–739, doi 10.1098/rsif.2010.0438, "The statistical mechanics of a polygenic character under stabilizing selection, mutation and drift." Static statistical mechanics of a polygenic trait; context.
- **Lande and Shannon (1996)**, *Evolution* 50:434–437, doi 10.1111/j.1558-5646.1996.tb04504.x, "The role of genetic variation in adaptation and population persistence in a changing environment." The polymorphic (\(V_G\)) moving-optimum lag and load for directional, random-walk and autocorrelated optima. Same OU-tracking structure as SA3; constants not borrowed.
- **Bürger and Lynch (1995)**, *Evolution* 49:151–163, doi 10.1111/j.1558-5646.1995.tb05967.x. Adaptation and extinction under a steadily moving optimum (critical rate). DS2 is the weak-mutation chain's own, cruder speed limit; Bürger and Lynch's critical rate is a different (polymorphic, demographic) threshold and is not used.
- **Kopp and Hermisson (2007)**, *Genetics* 176:715–719, doi 10.1534/genetics.106.067215, "Adaptation of a Quantitative Trait to a Moving Optimum"; **(2009)**, *Genetics* 182:233–249, doi 10.1534/genetics.108.099820, "The Genetic Basis of Phenotypic Adaptation I: Fixation of Beneficial Mutations in the Moving Optimum Model." They separate environmental, mutation and fixation time scales into regimes of the substitution pattern under a moving optimum. DS1(d) and DS2 are statements of the same regime logic for the cost excess; no constant is taken from them.
- **Collins, de Meaux and Acquisti (2007)**, *Genetics* 176:1089–1099, doi 10.1534/genetics.107.072926, "Adaptive Walks Toward a Moving Optimum" (monomorphic sequential-fixation walks, simulated). Context.
- **McCandlish and Stoltzfus (2014)**, *Q. Rev. Biol.* 89:225–252, doi 10.1086/677571 (origination–fixation models); **Sella and Hirsh (2005)**, doi 10.1073/pnas.0501865102 (the static weight); **Uhlenbeck and Ornstein (1930)**, *Phys. Rev.* 36:823–841, doi 10.1103/PhysRev.36.823 (the OU process); **Ethier and Kurtz (1986)**, *Markov Processes: Characterization and Convergence*, Wiley, doi 10.1002/9780470316658 (diffusion approximation).

**Split.** *Prior art:* the static \(d/2\) equipartition; the equilibrium-plus-adaptive decomposition; linear-in-drive adaptive load for slow driving and saturation for fast driving (one dimension); the regime logic of time scales. *Done here (packaging and elementary extensions):* the \(d\)-dimensional trace formula with general \(H\), \(Q\), \(\gamma\) and mutation matrix \(M\); the "drift multiplies the temperature by \(1+D/D_m\)" reading and the drift-adjusted closeness condition DS1c in the repository's \(\beta\), \(J\), \(\sigma N_e\) notation; the exact-chain speed limit DS2 (elementary; likely known in substance as mutation-limited adaptation, novelty not claimed); the simulation of the exact lattice Moran chain against the formula.

## 6. DS2 (speed limit) and DS3 (the regime between)

**Theorem DS2 (PROVED (in-model), exact chain, no diffusion limit).** In the chain of §2 (any \(J\), any world), each coordinate's expected displacement over time \(t\) satisfies \(\lvert\mathbb{E}[\theta_k(t)-\theta_k(0)]\rvert<v_{\max}t\) with \(v_{\max}=N\mu\delta/(2d)\). If the optimum moves at constant velocity with \(\lvert v_k\rvert\ge v_{\max}\) in some coordinate and \(H\) is positive definite, then \(\mathbb{E}[\lvert L_k(t)\rvert]\ge(\lvert v_k\rvert-v_{\max})t-\lvert L_k(0)\rvert\), so \(\mathbb{E}[J-J^\star]\ge\tfrac12\lambda_{\min}\bigl((\lvert v_k\rvert-v_{\max})t-\lvert L_k(0)\rvert\bigr)^2\) and the time-averaged excess grows without bound.

*Proof.* Steps toward \(+e_k\) occur at rate \(\tfrac{N\mu}{2d}\varphi<\tfrac{N\mu}{2d}\) (Moran \(\varphi<1\)), each of size \(\delta\); steps toward \(-e_k\) have nonnegative rate. So the drift of \(\theta_k\) is below \(v_{\max}\) at all times, and \(\mathbb{E}[\theta_k(t)]-\theta_k(0)<v_{\max}t\). The lag bound follows from \(L_k=\theta_k-\theta^\star_k\) and Jensen; the cost bound from \(\tfrac12 L^\top HL\ge\tfrac12\lambda_{\min}L_k^2\) and Jensen again. □

In words: a lineage that improves only by substitutions cannot follow an optimum that moves faster than mutants pointing the right way arise. This is the mismatch the theory describes between how fast a world drifts and how fast a store can be refreshed: here the "store" is the lineage's design and its refresh rate is the substitution rate.

**DS3 (OPEN; SKETCH where stated).** Between the linear regime of DS1 and the hard limit of DS2:
- *Velocity.* For \(\mu\delta/(2d)\lesssim v<v_{\max}\), a stationary lag exists in the simulation (DS2's \(v=5<v_{\max}=10\) case), but its size is not derived. SKETCH: the forward–backward rate difference \(\tfrac{N\mu}{2d}[\varphi(-x)-\varphi(x)]\) stays close to linear in \(x\) up to \(x\sim1\) while the sum of rates grows, so the restoring drift is nearly the DS1 one but the noise is larger, and the excess should exceed DS1(c). The simulation agrees in sign (+4.1% at \(N x=0.2\), +5.8% at \(N x=0.4\), of which about 2.5 points is time-step bias; §7).
- *Brownian world, coarse steps.* No hard threshold exists for a Brownian optimum (a bounded restoring speed still gives a stationary lag). SKETCH lower bound in one coordinate: with restoring speed at most \(v_{\max}\), the lag cannot be tighter than the Laplace distribution of a diffusion with drift \(-v_{\max}\,\mathrm{sign}(L)\), giving excess at least of order \(h D^2/v_{\max}^2\). The comparison argument is not written out. In the simulation DS1(b) stays within 0.2–3% up to \(\varepsilon_{\mathrm{lat}}\approx1\), so the stated condition \(\varepsilon_{\mathrm{lat}}\ll1\) is conservative.
- *Not covered at all:* non-quadratic \(J\) with several basins under drift (metastability, SA4), a moving Hessian, frequency dependence, strong mutation and clonal interference, the persistence-only case A2-P, a world the lineage shapes (CX2), and Theorem P for drifting worlds (CX1).

## 7. Simulation check (NUMERICAL)

`tools/drift_selection_checks.py --full`, run at nice 19, results in `theory/drift_selection_checks/results_full.json`; quick mode is run by `tools/test_drift_selection_checks.py`. The exact weak-mutation chain on \(\mathbb{Z}^d\) (\(\delta=1\), \(\mu=1\), so \(D_m=1/(2d)\)) with exact Moran fixation probabilities, time step \(\Delta t\) for the moving optimum, 1,500 replicates, time-averaged after burn-in. \(N=100\), \(\beta h=0.02\), so \(d/(2\beta)=25\) per coordinate and the chain relaxes in about 100 time units. Tolerance for a check inside DS1's conditions: 8%.

| Case | Simulated excess (± SE) | DS1 formula | Relative error | Inside DS1 conditions? |
|---|---|---|---|---|
| BM d=1 D/D_m=0.0 (eps_lat=0.02) | 25.13 ± 0.16 | 25.00 | +0.5% | yes (tolerance 8%) |
| BM d=1 D/D_m=0.5 (eps_lat=0.03) | 37.96 ± 0.25 | 37.50 | +1.2% | yes (tolerance 8%) |
| BM d=1 D/D_m=1.0 (eps_lat=0.04) | 51.14 ± 0.33 | 50.00 | +2.3% | yes (tolerance 8%) |
| BM d=1 D/D_m=2.0 (eps_lat=0.06) | 76.30 ± 0.47 | 75.00 | +1.7% | yes (tolerance 8%) |
| BM d=1 D/D_m=5.0 (eps_lat=0.12) | 153.77 ± 0.96 | 150.00 | +2.5% | yes (tolerance 8%) |
| BM d=1 D/D_m=5.0 dt=0.01 (time-step check) | 150.67 ± 0.94 | 150.00 | +0.4% | yes (tolerance 3%) |
| BM d=2 H=diag(1,3) D/D_m=0.0 | 49.95 ± 0.21 | 50.00 | -0.1% | yes (tolerance 8%) |
| BM d=2 H=diag(1,3) D/D_m=2.0 | 153.29 ± 0.65 | 150.00 | +2.2% | yes (tolerance 8%) |
| OU d=1 D=D_m gamma=0.001 (chain rate a=0.010) | 48.45 ± 0.29 | 47.73 | +1.5% | yes (tolerance 8%) |
| OU d=1 D=D_m gamma=0.010 (chain rate a=0.010) | 37.47 ± 0.20 | 37.50 | -0.1% | yes (tolerance 8%) |
| OU d=1 D=D_m gamma=0.100 (chain rate a=0.010) | 27.15 ± 0.15 | 27.27 | -0.5% | yes (tolerance 8%) |
| velocity d=1 v=0.05 (N x=0.10) | 38.46 ± 0.27 | 37.50 | +2.6% | yes (tolerance 8%) |
| velocity d=1 v=0.10 (N x=0.20) | 78.04 ± 0.49 | 75.00 | +4.1% | no; reported only |
| velocity d=1 v=0.20 (N x=0.40) | 238.02 ± 0.95 | 225.00 | +5.8% | no; reported only |
| BM d=1 D/D_m=20 (eps_lat=0.42) | 526.17 ± 4.63 | 525.00 | +0.2% | no; reported only |
| BM d=1 D/D_m=50 (eps_lat=1.02) | 1313.66 ± 11.16 | 1275.00 | +3.0% | no; reported only |

DS2 runs (\(N=20\), \(\alpha h=0.05\), \(v_{\max}=10\), 400 replicates, \(T=300\), \(\Delta t=0.004\)): at \(v=5\) the mean lag is stationary at 14.7 (slope over the second half -2.2e-07); at \(v=12\) the mean lag grows at slope 2.22 (bound \(v-v_{\max}=2\)) and reaches 698 at \(T\).

**Reading.** Inside DS1's conditions every case matches the formula within 2.6% at \(\Delta t=0.05\). Those errors are small but positive and a few standard errors wide; the time-step check at \(\Delta t=0.01\) removes most of the bias (\(+0.4\%\), within one standard error), so it is mostly a time-discretization artifact of the simulator, not of the formula. The two-dimensional case with \(H=\mathrm{diag}(1,3)\) gives the same excess as the isotropic formula, as DS1(b) says (curvature cancels). The OU cases follow the interpolation from Brownian-like (\(\gamma\ll a\)) toward the static-scatter-plus-variance limit (\(\gamma\gg a\)). The velocity cases outside the stated condition sit +4.1% and +5.8% above the formula. Part of that is the same time-step bias (about +2.5% at \(\Delta t=0.05\)), so the remainder (roughly +1.5% and +3%) is in the direction DS3 sketches but is not separated cleanly from the simulator's bias. The Brownian cases at \(D/D_m=20\) and 50 (\(\varepsilon_{\mathrm{lat}}\approx0.4\) and 1.0, \(\Delta t=0.02\)) stay within +0.2% and +3%. DS2: at \(N=20\), \(\alpha h=0.05\), \(v_{\max}=10\), the lag is stationary at \(v=5\) and grows at slope \(\approx2.2\ge v-v_{\max}=2\) at \(v=12\).

## 8. How this ties to the theory's layers

The chain's relaxation rate \(a=D_m\beta\lambda\) is the lineage's refresh rate for its slow design. World variation slower than \(a\) is tracked by selection, at a cost of order \(D/(2\beta D_m)\) per DS1(b). World variation faster than \(a\) is averaged out by the chain, and its cost, \(\tfrac12\mathrm{Tr}(HQ/\gamma)\) in DS1(d), is not something the substitution chain can reduce. That is the place where within-lifetime judgment (sensing, memory, reads: the terms of \(J\)) earns its cost. This is the THEORY §2 picture of layers matched to the time scales of the world, read for selection itself: selection tunes the slow layer, and fast drift has to be met by a held model. Read this way, "near the minimum" in a drifting world means near the minimum of the cost averaged over the variation the chain cannot follow, not near each instantaneous minimum. This reading is an interpretation of DS1(d) and DS2, not a further theorem.

## 9. A dated prediction (OPEN, not locked)

**DS-P1 (OPEN, not locked, not a test until preregistered).** Extends SA-P1. For a class where the optimum's diffusion \(D\) in whitened soft coordinates and the neutral substitution diffusion \(D_m\) can be measured independently of the design (for example, a laboratory evolution experiment with a programmed drifting optimum), the fractional excess should scale as \(d(1+D/D_m)/(2\sigma N_e)\), and in particular should rise linearly in \(D\) at fixed \(\sigma N_e\) with intercept \(d/(2\sigma N_e)\) and slope \(d/(2\sigma N_e D_m)\). A steady drift faster than \(v_{\max}\) should give a lag that grows in time. Factors, sample sizes and decision rules are to be fixed in a preregistration. A miss would be a result to diagnose (measurement of \(D_m\), hidden coordinates, a non-quadratic chart, or the claim), and the class would be followed up, not discarded.

## 10. Numerical checks and files

- `theory/DRIFT_SELECTION.md` (this note).
- `tools/drift_selection_checks.py` (quick and `--full`), `tools/test_drift_selection_checks.py`.
- `theory/drift_selection_checks/results_full.json` (the documented run).

The Part 2 hypothesis sentence is unchanged and is not restated here.
