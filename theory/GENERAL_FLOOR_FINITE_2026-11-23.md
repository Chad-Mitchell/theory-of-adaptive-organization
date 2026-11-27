# A finite-state lower bound on the learning-rate floor

*Monday 23 November 2026 (America/New_York). A follow-up to the general heat-floor attempt and the two-state freeze-or-hold note, not a change to `THEORY.md` or the hypothesis sentence. Written against `main` `20eb6d8` (after PR #232; drafted against `615cdb9`). DOIs below were resolved on the Crossref API the same day (`theory/general_floor_finite_checks/crossref.out`). A check script on small finite-state worlds and memories, not a new simulation of a real system. Open-work row T60. T57–T59 are on `main` as of pull requests #229–#231 and are not rewritten here except for a pointer from T57. A self-check, not an independent review.*

Labels follow the repo: **PROVED (in-model)** is a result inside a named class. **KNOWN** is published and credited, only for what that source states. **ELEMENTARY** is a direct consequence of a proved or known inequality, not a new named theorem. **CONJECTURE** is a named bet, not a result. **OPEN** is not derived. A lower bound is not a derivation of the cost.

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

## 0. Bottom line

The two-state freeze-or-hold note (T59) proved that, under Proposition JP-heat, a telegraph world of flip rate \(r\) and a two-state memory have net learning rate \(I_{\mathrm{alt}}=r\,L(\varepsilon)\), with \(L(\varepsilon)=(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\). The leak cancels. A frozen world still has vanishing ongoing heat at a finite Boltzmann error.

This note asks for the same kind of design-independent lower bound when the world \(X\) and the memory \(M\) are arbitrary finite-state jump processes, with bipartite dynamics and local detailed balance on the memory. The thermodynamic step is unchanged: \(\dot Q_M\ge kT\,I_{\mathrm{alt}}\) is **KNOWN** (Horowitz and Esposito 2014; Proposition JP-heat). The informational step is the one that has to be extended.

The exact destruction identity, for an exogenous world in a steady state, is **ELEMENTARY**, and is the stationary Horowitz–Esposito / Barato–Hartich–Seifert learning rate (\(l_y=h_x\)) written as a flux-weighted sum of KL divergences of the memory's conditionals (the stationary flux term drops). It is not claimed as a new identity:

\[
I_{\mathrm{alt}}=\sum_{x\neq x'}\pi(x)\,W_X(x\to x')\,D_{\mathrm{KL}}\bigl(p(M\mid x)\,\|\,p(M\mid x')\bigr).
\]

The unconditional target — that \(I_{\mathrm{alt}}\ge\Phi_X(\varepsilon)>0\) whenever the world is not frozen and the Bayes error \(\varepsilon\) is below its no-memory value \(\varepsilon_0=1-\max_x\pi(x)\) — is false. A world with two recurrent classes, one of them mixing and one frozen, can have \(I_{\mathrm{alt}}=0\) at an error strictly below \(\varepsilon_0\), by holding only the class label. That is the precise condition: what matters is the *occupied flux graph*, the directed graph of pairs with \(\pi(x)W_X(x\to x')>0\). If that graph is disconnected, a static record of the class is free. If it is strongly connected — in particular, if \(X\) is irreducible — then \(I_{\mathrm{alt}}=0\) implies \(\varepsilon=\varepsilon_0\), so \(\varepsilon<\varepsilon_0\) implies \(I_{\mathrm{alt}}>0\). The converse is false once the world has three or more states: a memory can sit at chance Bayes error while still distinguishing non-mode states, with a strictly positive net learning rate. On the telegraph the two coincide, and the biconditional holds.

When the occupied flux graph is strongly connected, two design-independent lower bounds are **PROVED (in-model)**.

1. *Telegraph reduction, any finite memory.* For a fair two-state world of flip rate \(r\), \(I_{\mathrm{alt}}\ge r\,L(\varepsilon)\), with equality at the symmetric two-state copy. The T59 floor is not special to a two-state record.
2. *Path-Pinsker bound, any finite irreducible world.* \(I_{\mathrm{alt}}\ge(\varepsilon_0-\varepsilon)^2/K_X\), where the constant \(K_X\) is computed from the world's rates and \(\pi\) alone (a shortest-path Cauchy–Schwarz form, displayed in §4). On the telegraph, \(K_X=1/(4r)\), so the bound is \(4r(\tfrac12-\varepsilon)^2\). That is half the leading quadratic of \(r\,L(\varepsilon)\) as \(\varepsilon\to\tfrac12\), and it does not diverge as \(\varepsilon\to 0\).
3. *Pairwise \(L\) bound.* For any pair of states whose flux is positive, if \(\varepsilon<\min(\pi(i),\pi(j))\), then \(I_{\mathrm{alt}}\ge \min\bigl(\pi(i)W(i\to j),\pi(j)W(j\to i)\bigr)\,2L\bigl(\varepsilon/(2\min(\pi(i),\pi(j)))\bigr)\). On the telegraph this is again \(r\,L(\varepsilon)\). It captures the logarithmic divergence as \(\varepsilon\to 0\) whenever a well-occupied pair shares a flux.

The causal learning-rate–distortion function \(\Phi_X(\varepsilon)\) of T57 is still the infimum of \(I_{\mathrm{alt}}\) at fixed error. The three displays are lower bounds on \(\Phi_X\). The telegraph bound is tight. A closed form of \(\Phi_X\) for a general irreducible kernel is **OPEN**, and is not conjectured here as a formula. T57's frozen-world loophole stays open whenever the occupied flux is zero.

## 1. The cost, with named terms

The method is the same as everywhere in the theory: write the cost, find its minimum, and read off the design. Whether a real system sits near that minimum is Part 2, and is not decided here.

**World.** A finite-state continuous-time Markov chain \(X\) on a set of size \(n\ge 2\), with generator \(W_X\) (off-diagonal rates, bounded, not identically zero unless the frozen case is being named). The world is exogenous: the design does not move \(X\) (T57's (S5); a world the memory moves is CX2, **OPEN**). When \(X\) is irreducible it has a unique stationary distribution \(\pi\). When it is reducible, a stationary distribution may be a mixture over recurrent classes, and that mixture is part of the world's occupancy, not of the memory design.

**Memory.** A finite-state process \(M\), of any size, with bipartite dynamics: \(X\) and \(M\) do not jump together. Memory rates \(w(m\to m'\mid x)\) obey local detailed balance at a single bath temperature \(T\), as in Proposition JP-heat. The pair is in a steady state, or is averaged in the long run so that the Shannon entropy of \(M\) stays bounded (T57's (S4)).

**Error.** The Bayes 0-1 error

\[
\varepsilon=1-\sum_m\max_x\pi(x,m)=\min_f\mathbb{P}(f(M)\neq X).
\]

The no-memory value is \(\varepsilon_0=1-\max_x\pi(x)\). For a fair telegraph and a well-labelled two-state memory, this is the Hamming error of T59 and of IP3. A mismatched labelling can make a Hamming score worse than the Bayes error; the bounds below use the Bayes error.

**Named terms of the cost.** As in T57 and T59, the cost of judgment as a long-run rate, subject to the ruin cap, is

\[
J=\dot Q_M+w\varepsilon.
\]

- \(\dot Q_M\) is the energy flow into the bath that implements the memory's transitions. Under local detailed balance, Proposition JP-heat gives \(\dot Q_M\ge kT\,I_{\mathrm{alt}}\), **KNOWN**.
- \(I_{\mathrm{alt}}=\sum\pi\,w\,\ln\bigl(\pi(m'\mid x)/\pi(m\mid x)\bigr)\) is the net information flow of memory jumps (the Horowitz–Esposito flow; T57's \(\dot I_M\)).
- \(w\varepsilon\) is stake times Bayes error. Temperature does not set the stake.
- The ruin cap stands outside the sum. A one-time write is a finite cost, not a rate, as in T59.
- A lower bound \(\varphi(\varepsilon)\) on \(I_{\mathrm{alt}}\) at fixed \(\varepsilon\) is a lower bound \(kT\,\varphi(\varepsilon)+w\varepsilon\) on \(J\) at that \(\varepsilon\). The minimum over designs is at least the minimum of that bound over attainable \(\varepsilon\in(0,\varepsilon_0]\).

## 2. Prior art: what each source establishes, and what is new

Every DOI in this section was resolved on `api.crossref.org` on 23 November 2026. A repository search was done first. Nothing below is claimed as new except the in-model composition in §3–§5, and that composition is labeled. The gap each source leaves is stated for that source, not as a criticism of the paper.

**Horowitz and Esposito (2014),** *Phys. Rev. X* 4:031015, doi 10.1103/PhysRevX.4.031015. The bipartite information-flow heat inequality used as JP-heat. It bounds \(\dot Q_M\) by the net flow \(I_{\mathrm{alt}}\). It has no tracking-error variable, and it does not evaluate \(I_{\mathrm{alt}}\) as a function of \(\varepsilon\). **Horowitz (2015),** *J. Stat. Mech.* 2015:P03006, doi 10.1088/1742-5468/2015/03/p03006, extends the split to many subsystems. Still no tracking error.

**Barato, Hartich, and Seifert (2014),** *New J. Phys.* 16:103024, doi 10.1088/1367-2630/16/10/103024. A learning rate is at most the entropy production of the learning subsystem. The same thermodynamic step, written as an efficiency. Their receptor example also shows that another bath can pay. **Hartich, Barato, and Seifert (2016),** *Phys. Rev. E* 93:022116, doi 10.1103/PhysRevE.93.022116, define a sensory capacity. Neither paper is a design-independent floor on the learning rate in terms of a Bayes error of a finite-state world.

**Still, Sivak, Bell, and Crooks (2012),** *Phys. Rev. Lett.* 109:120604, doi 10.1103/PhysRevLett.109.120604, and **Still (2020),** *Phys. Rev. Lett.* 124:050601, doi 10.1103/PhysRevLett.124.050601. Dissipation is bounded by the part of the memory that does not predict. As T57 already says, those inequalities charge useless memory. They do not force the heat to rise as the tracking error falls, and they do not close a frozen or disconnected-class loophole.

**Bo, Del Giudice, and Celani (2015),** *J. Stat. Mech.* 2015:P01014, doi 10.1088/1742-5468/2015/01/P01014. Crossref lists the families as Bo, Giudice, and Celani. Extra memory about the sensory past, beyond the present reading, is bounded by extra entropy production. In steady state they recover a learning-rate bound of the Horowitz–Esposito type. They do not give a design-independent \(\Phi_X(\varepsilon)\) for a finite-state jump world. Already booked that way in `theory/INFO_PHYSICS.md` and `theory/GENERAL_FORM_PHYSICS_2026-11-22.md`.

**Sartori, Granger, Lee, and Horowitz (2014),** *PLoS Comput. Biol.* 10:e1003974, doi 10.1371/journal.pcbi.1003974. Adaptation costs tracked by the information the sensor holds about its environment. Already in the repo. It is the same family as Still and as Horowitz–Esposito: heat versus information, not heat versus a Bayes error of a general finite-state world.

**Mehta and Schwab (2012),** *PNAS* 109:17978, doi 10.1073/pnas.1207814109. For a two-component Berg–Purcell network, learning a concentration requires breaking detailed balance, and more learning costs more energy. Already in the repo. **Lang, Fisher, Mora, and Mehta (2014),** *Phys. Rev. Lett.* 113:148103, doi 10.1103/PhysRevLett.113.148103. Thermodynamic constraints on a cell's statistical estimate of a concentration. **Mehta, Lang, and Schwab (2016),** *J. Stat. Phys.* 162:1153, doi 10.1007/s10955-015-1431-6. A review of energy use in biochemical information processing (specificity, dynamics, variability, amplification, erasure). These are the Lang–Mehta line on the energetics of sensing. They do not supply the destruction identity or a design-independent \(\Phi_X(\varepsilon)\) for a finite-state Markov-jump world.

**Lan, Sartori, Neumann, Sourjik, and Tu (2012),** *Nat. Phys.* 8:422, doi 10.1038/nphys2276. A logarithmic accuracy cost at fixed adaptation speed in a coarse-grained chemotaxis model. Already distinguished from the telegraph floor in `theory/INFO_PHYSICS.md`.

**Tjalma and ten Wolde (2024),** *Phys. Rev. Research* 6:033049, doi 10.1103/PhysRevResearch.6.033049. A prediction-error trade-off for discrete receptor sampling, already discussed in `theory/STORE_NOISE.md`. It is an optimal-timing calculation for one sensory task, not a finite-state learning-rate–distortion floor.

**Wonham (1964),** *SIAM J. Control* 2:347, doi 10.1137/0302028. The optimal filter for a finite-state Markov chain observed in continuous noise: a posterior ODE, not a finite-state jump memory, and not a heat bound. **Duncan (1970),** *SIAM J. Appl. Math.* 19:215, doi 10.1137/0119020, already used in the repo for the continuous-time Kalman–Bucy rate. Neither paper is a lower bound on \(I_{\mathrm{alt}}\) at fixed Bayes error for a jump memory.

A search of the repo and of the filtering / information-thermodynamic literature named above did not find a design-independent lower bound of the form \(I_{\mathrm{alt}}\ge\varphi_X(\varepsilon)\) for a general finite-state jump world and a finite-state jump memory, with a reduction to \(r\,L(\varepsilon)\) on the telegraph. That search can miss a paper. This note does not claim that no such bound exists in print; it claims only that the composition below is not taken from the sources just listed, and is labeled as an in-model result of this note.

**What is new here, if anything.** The thermodynamic step is JP-heat, already in the repo. The destruction identity is a rewriting, in steady state, of the Horowitz–Esposito information flow of the world's jumps, for an exogenous stationary chain. The addition is the design-independent use of that identity: the exact condition for positivity, the two-class counterexample to the unconditional target, the telegraph bound for an arbitrary finite memory, the pairwise \(L\) bound, and the path-Pinsker bound with an explicit world-only constant \(K_X\). T57's loophole is not closed.

## 3. The destruction identity, and the exact condition

**Assumptions for this section:** (S1) bipartite jumps; (S4) a steady state; (S5) an exogenous world, so \(W_X\) does not depend on \(M\), and the marginal \(\pi\) of \(X\) is the world's own stationary distribution. Local detailed balance is not required for the identity; it is required only to pass from \(I_{\mathrm{alt}}\) to heat.

**Identity.** In a steady state the mutual information \(I(X;M)\) is constant, so the Horowitz–Esposito flows of the two sides sum to zero: \(I_{\mathrm{alt}}=-I^X\). Expanding \(I^X\) in the conditionals \(p(M\mid x)\) produces a term \(\sum\pi(x)W_X(x\to x')\ln(\pi(x')/\pi(x))\) and a term \(-\sum\pi(x)W_X(x\to x')\,D_{\mathrm{KL}}(p(M\mid x)\,\|\,p(M\mid x'))\). For a stationary exogenous world the first term vanishes (the incoming and outgoing fluxes at each \(x\) match). What remains is

\[
I_{\mathrm{alt}}=\sum_{x\neq x'}\pi(x)\,W_X(x\to x')\,D_{\mathrm{KL}}\bigl(p(M\mid x)\,\|\,p(M\mid x')\bigr).
\]

This is **ELEMENTARY**, and is the same stationary learning-rate identity already in Horowitz–Esposito and in Barato, Hartich, and Seifert (their \(h_x=l_y\)), after the term \(\sum\pi W\ln(\pi(x)/\pi(x'))\) vanishes by flux balance. It is not claimed as new. The check script compares the two sides on the telegraph, on an irreversible three-cycle, and on random three-to-five-state worlds, including shuffled and coarse memories.

**Positivity.** The right-hand side vanishes if and only if \(p(M\mid x)=p(M\mid x')\) on every directed edge with positive flux \(\pi(x)W_X(x\to x')\). So \(I_{\mathrm{alt}}=0\) if and only if the conditionals are constant on each weakly connected component of the occupied flux graph (more sharply: constant along every directed path of positive flux). If that graph is strongly connected on the support of \(\pi\), the conditionals are the same at every occupied state, \(M\perp X\), and the Bayes error equals \(\varepsilon_0\). This is **PROVED (in-model)** in the present class. A finite irreducible chain that is not frozen has a unique, strictly positive \(\pi\) and a strongly connected flux graph, so \(I_{\mathrm{alt}}>0\) whenever \(\varepsilon<\varepsilon_0\). The converse, that \(\varepsilon=\varepsilon_0\) forces \(I_{\mathrm{alt}}=0\), is false for a world with three or more states: Bayes 0-1 error only sees the mode, so a memory that distinguishes non-mode states can sit at \(\varepsilon=\varepsilon_0\) with a strictly positive net learning rate. On the telegraph, total variation fixes the Bayes error, and the biconditional holds.

**Counterexample to the unconditional target.** Let \(X\) have states \(\{0,1,2\}\), with \(0\) and \(1\) flipping at rate \(r_A=1\) and with \(2\) isolated and frozen. The occupied flux graph has two components. A two-state memory that tracks only the class, \(\{0,1\}\) versus \(\{2\}\), and a mixture occupancy \(\pi=(0.3,0.3,0.4)\), give \(I_{\mathrm{alt}}=0\) at Bayes error \(\varepsilon=0.312590<\varepsilon_0=0.600000\), as checked by the script. The world is not frozen: the class \(\{0,1\}\) mixes. The error is below chance for the mixture. The flow is nevertheless zero, because the memory does not distinguish the states that jump. That is the precise condition the unconditional statement missed: positivity requires a connected occupied flux graph, not merely a generator that is not the zero matrix.

A tiny leak between the classes, of rate \(10^{-4}\), makes the chain irreducible. The same class-tracking memory then has a strictly positive flow \(I_{\mathrm{alt}}=0.00025706\), at \(\varepsilon=0.345315<\varepsilon_0=0.666644\). The flow can be arbitrarily small if the leak is. Any quantitative bound has to see that conductance.

**Frozen support.** If every occupied flux vanishes, the identity gives \(I_{\mathrm{alt}}=0\) at every finite error a static bias can hold. The check records a two-state frozen world with a static copy of energy \(1\), Boltzmann error \(1/(1+e)=0.268941<\varepsilon_0=\tfrac12\), and \(I_{\mathrm{alt}}=0\). This is T57's loophole, still open, in the same terms as T59.

## 4. Design-independent lower bounds

**Telegraph, any finite memory.** Let \(X\) be the fair telegraph of rate \(r>0\). Then \(\pi=(1/2,1/2)\) and

\[
I_{\mathrm{alt}}=\frac r2\Bigl(D_{\mathrm{KL}}(p_0\|p_1)+D_{\mathrm{KL}}(p_1\|p_0)\Bigr),
\]

the Jeffreys divergence of the two conditionals, times \(r/2\). The Bayes error of a fair bit is \(\varepsilon=\tfrac12\sum_m\min(p_0(m),p_1(m))\), or \(\varepsilon=(1-\mathrm{TV}(p_0,p_1))/2\). Lumping each conditional onto the Bayes partition \(\{p_0\ge p_1\}\) and its complement does not raise the Jeffreys divergence (the data-processing inequality) and preserves total variation, so the minimum at fixed \(\varepsilon\) is attained at a binary pair. On that pair, with masses \(a+b=2\varepsilon\), the Jeffreys divergence equals \((1-2\varepsilon)\ln\bigl[(1-a)(1-b)/(ab)\bigr]\), which is minimized at \(a=b=\varepsilon\) and equals \(2L(\varepsilon)\). Therefore \(I_{\mathrm{alt}}\ge r\,L(\varepsilon)\). (Credit added 27 November 2026: the minimum of the Jeffreys divergence at fixed total variation, attained at the symmetric binary pair, is KNOWN: Gilardoni 2006, *C. R. Math.* 343:763–766, doi 10.1016/j.crma.2006.10.027 (corrigendum *C. R. Math.* 348, 2010, doi 10.1016/j.crma.2010.02.006); Sason 2015, IEEE Information Theory Workshop, doi 10.1109/ITW.2015.7133079, Prop. 4. The step this note adds is joining it to the learning-rate identity.) Equality holds at the symmetric two-state copy of T59 and IP3. This is **PROVED (in-model)** for any finite memory, and is checked on thirty random local-detailed-balance memories with two to six states.

**Pairwise \(L\).** For any pair \(\{i,j\}\) and any memory, \(\sum_m\min(\pi(i,m),\pi(j,m))\le\varepsilon\), because the mass of every non-top state is part of the Bayes error. Hence \(\sum_m\min(p_i,p_j)\le\varepsilon/\min(\pi(i),\pi(j))\) when that minimum is positive, and the balanced pairwise error is at most \(\varepsilon/(2\min(\pi(i),\pi(j)))\). If this quantity is strictly less than \(\tfrac12\), that is if \(\varepsilon<\min(\pi(i),\pi(j))\), the telegraph argument gives a Jeffreys lower bound \(2L\bigl(\varepsilon/(2\min(\pi(i),\pi(j)))\bigr)\). Multiplying by the smaller of the two directed fluxes yields the pairwise bound stated in §0. It is **PROVED (in-model)**. It is tight on the telegraph. It is silent on a pair when \(\varepsilon\) is larger than that pair's occupancy, which is why a path bound is still needed at moderate error.

**Path-Pinsker.** Let the occupied flux graph be strongly connected, and let \(x^*\) be a mode of \(\pi\). For each occupied \(x\neq x^*\), pick a shortest directed path \(P_x\) of positive-rate edges from \(x\) to \(x^*\). Pinsker's inequality in nats, \(D_{\mathrm{KL}}(p\|q)\ge 2\,\mathrm{TV}(p,q)^2\), and the triangle inequality, give \(\mathrm{TV}(p_x,p_{x^*})\le\sum_{e\in P_x}\sqrt{D_{\mathrm{KL},e}/2}\). From §3's comparison of Bayes error with total variation,

\[
\varepsilon_0-\varepsilon\le\sum_{x\neq x^*}\pi(x)\,\mathrm{TV}(p_x,p_{x^*}).
\]

Collecting coefficients \(c_e=\sqrt{1/2}\sum_{x:\,e\in P_x}\pi(x)\) and applying Cauchy–Schwarz against the fluxes \(j_e=\pi(u)W_X(u\to v)\) produces

\[
I_{\mathrm{alt}}\ge\frac{(\varepsilon_0-\varepsilon)^2}{K_X},\qquad K_X=\sum_e\frac{c_e^2}{j_e}.
\]

The constant \(K_X\) depends on the world and on the choice of paths, not on the memory. Shortest paths are a definite choice; any other system of directed paths would give another valid, world-only constant. On the fair telegraph, \(K_X=1/(4r)\), so the bound is \(4r(\tfrac12-\varepsilon)^2\). As \(\varepsilon\to\tfrac12\), \(r\,L(\varepsilon)\sim 8r(\tfrac12-\varepsilon)^2\), twice this Pinsker form. At \(\varepsilon=0.2\), \(r=1\), the Pinsker number is \(0.36\) and \(r\,L(\varepsilon)=0.831776616672\). The path bound is **PROVED (in-model)** for any finite world whose occupied flux graph is strongly connected. It does not diverge as \(\varepsilon\to 0\); the pairwise \(L\) bound is the one that does, when it is active. A single closed form that is tight for every irreducible kernel is **OPEN**.

## 5. The minimum, and what is read off

Composing with JP-heat, in the bipartite local-detailed-balance class,

\[
J\ge kT\,\varphi_X(\varepsilon)+w\varepsilon,
\]

where \(\varphi_X\) may be taken as the pointwise maximum of the path-Pinsker bound, of any active pairwise \(L\) bound, and, when the world is a telegraph, of \(r\,L(\varepsilon)\). The ruin cap stands outside. The stake and the cap are not derived.

On the telegraph, \(\varphi=r\,L(\varepsilon)\) is tight, and the minimum over \(\varepsilon\in(0,1/2]\) is the usual telegraph tradeoff already in `theory/GENERAL_FORM_PHYSICS_2026-11-22.md`. The design that approaches it is a fast copy at the minimal affinity, as in IP3. A leak does not change the floor.

On a general irreducible world, the path-Pinsker piece is quadratic in the error deficit. If the cap is slack and one uses only that piece, with \(kT=1\), the unconstrained minimum of \((\varepsilon_0-\varepsilon)^2/K_X+w\varepsilon\) sits at \(\varepsilon=\varepsilon_0-w K_X/2\) when this lies in \((0,\varepsilon_0)\), and at a corner otherwise. That location is a consequence of the Pinsker relaxation, not of the tight \(\Phi_X\). A memory that approaches \(\Phi_X\) itself is **OPEN** outside the telegraph: the script finds local-detailed-balance copies, including shuffled and coarse embeddings, that stay above the proved bounds, but it does not identify an attaining family for a general kernel.

A one-time write remains a finite cost, amortized to zero as a rate on a long horizon, and is not a substitute for the ongoing floor when the occupied flux is positive.

## 6. What this does and does not close

- **T57.** The thermodynamic step is unchanged. The useful bound on \(\Phi\) is no longer a complete break in the finite-state jump class: when the occupied flux graph is strongly connected, \(\Phi_X(\varepsilon)\ge(\varepsilon_0-\varepsilon)^2/K_X>0\) for \(\varepsilon<\varepsilon_0\), and on the telegraph \(\Phi_X(\varepsilon)=r\,L(\varepsilon)\). The frozen-world loophole, and the disconnected-class loophole, stay open. A general strong-data-processing bound for an arbitrary kernel, including diffusions, is still a larger job.
- **T58, T59.** Not edited. The T59 identification \(I_{\mathrm{alt}}=r\,L(\varepsilon)\) is the telegraph special case of the identity and of the telegraph bound, and is here shown to hold for any finite memory, not only a two-state record. The claimed critical barrier of the withdrawn T59 draft remains retracted.
- **T48, T49, T40.** Not applied. `THEORY.md` is not edited. Non-Gaussian or non-jump closed forms stay class by class.
- **CX2.** A memory that moves the world can change \(\pi\) and \(W_X\). The identity of §3 is then not the one proved, and a design that freezes its world is a different problem. A follow-up is `theory/FEEDBACK_FLOOR_2026-11-23.md` (OPEN_WORK T61; a self-check, not an independent review).

## 7. Numerical checks

The script `theory/general_floor_finite_checks/general_floor_finite_checks.py` records the algebra and the in-model evaluations used above: the telegraph identities, including cancellation of a leak; a frozen static copy; the path-Pinsker constant on the telegraph; thirty richer memories on the telegraph; the two-class counterexample and the tiny-leak companion; an irreversible three-cycle; twenty-four random irreducible three-to-five-state worlds with shuffled, random-energy, and coarse memories; sixteen strong reversible three-state memories against the pairwise \(L\) bound; and the calculus check that the Jeffreys minimum at fixed total variation is the binary symmetric pair. The run used for this note reports `FAILS 0`. These are not measurements of a real system.

## 8. References

DOIs resolved on Crossref, 23 November 2026, America/New_York. The log is `theory/general_floor_finite_checks/crossref.out`.

- Wonham, W. M. 1964. Some Applications of Stochastic Differential Equations to Optimal Nonlinear Filtering. *SIAM J. Control* 2:347. doi 10.1137/0302028.
- Duncan, T. E. 1970. On the Calculation of Mutual Information. *SIAM J. Appl. Math.* 19:215. doi 10.1137/0119020.
- Mehta, P. and Schwab, D. J. 2012. Energetic costs of cellular computation. *Proc. Natl. Acad. Sci. U.S.A.* 109:17978. doi 10.1073/pnas.1207814109.
- Lan, G., Sartori, P., Neumann, S., Sourjik, V. and Tu, Y. 2012. The energy–speed–accuracy trade-off in sensory adaptation. *Nat. Phys.* 8:422. doi 10.1038/nphys2276.
- Still, S., Sivak, D. A., Bell, A. J. and Crooks, G. E. 2012. Thermodynamics of Prediction. *Phys. Rev. Lett.* 109:120604. doi 10.1103/PhysRevLett.109.120604.
- Horowitz, J. M. and Esposito, M. 2014. Thermodynamics with Continuous Information Flow. *Phys. Rev. X* 4:031015. doi 10.1103/PhysRevX.4.031015.
- Barato, A. C., Hartich, D. and Seifert, U. 2014. Efficiency of cellular information processing. *New J. Phys.* 16:103024. doi 10.1088/1367-2630/16/10/103024.
- Sartori, P., Granger, L., Lee, C. F. and Horowitz, J. M. 2014. Thermodynamic Costs of Information Processing in Sensory Adaptation. *PLoS Comput. Biol.* 10:e1003974. doi 10.1371/journal.pcbi.1003974.
- Lang, A. H., Fisher, C. K., Mora, T. and Mehta, P. 2014. Thermodynamics of Statistical Inference by Cells. *Phys. Rev. Lett.* 113:148103. doi 10.1103/PhysRevLett.113.148103.
- Horowitz, J. M. 2015. Multipartite information flow for multiple Maxwell demons. *J. Stat. Mech.* 2015:P03006. doi 10.1088/1742-5468/2015/03/p03006.
- Bo, S., Del Giudice, M. and Celani, A. 2015. Thermodynamic limits to information harvesting by sensory systems. *J. Stat. Mech.* 2015:P01014. doi 10.1088/1742-5468/2015/01/P01014.
- Hartich, D., Barato, A. C. and Seifert, U. 2016. Sensory capacity: An information theoretical measure of the performance of a sensor. *Phys. Rev. E* 93:022116. doi 10.1103/PhysRevE.93.022116.
- Mehta, P., Lang, A. H. and Schwab, D. J. 2016. Landauer in the Age of Synthetic Biology: Energy Consumption and Information Processing in Biochemical Networks. *J. Stat. Phys.* 162:1153. doi 10.1007/s10955-015-1431-6.
- Still, S. 2020. Thermodynamic Cost and Benefit of Memory. *Phys. Rev. Lett.* 124:050601. doi 10.1103/PhysRevLett.124.050601.
- Tjalma, A. J. and ten Wolde, P. R. 2024. Predicting concentration changes via discrete receptor sampling. *Phys. Rev. Research* 6:033049. doi 10.1103/PhysRevResearch.6.033049.

Already in the repository, and used rather than re-derived: Propositions JP-heat and EQ-heat in `theory/GENERALITY_2026-11-22.md`; the telegraph and Ornstein–Uhlenbeck heat infima in `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` and `theory/INFO_PHYSICS_ATTAINABILITY.md`; the general-floor attempt and its loophole in `theory/GENERAL_FLOOR_ATTEMPT_2026-11-23.md`; the two-state JP-heat identification and the still-open frozen loophole in `theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md`. The thermodynamic lift of the drifting information floor (T58) is `theory/DRIFT_HEAT_LIFT_2026-11-23.md` and is not edited here.

## 9. What this note does not do

It does not edit `THEORY.md`, `CORE.md`, or the hypothesis sentence. It does not add a CLAIM_MAP row, and it does not change the status of IP3, IP11, T40, T48, T49, T57, T58, or T59 except to point at this follow-up from T57 and from the open-work rows. It does not edit the T58 or T59 files. It does not prove a closed-form \(\Phi_X\) for every finite irreducible kernel, and it does not treat an in-model statement as a fact about a real system. It does not claim to close T57's loophole. A world the memory moves is T61, not this note. No system has been shown to qualify under THEORY §3.

## Credits (appended 27 November 2026)

The telegraph bound of §4 uses the fixed-total-variation minimum of the Jeffreys divergence, which is KNOWN: Gilardoni 2006, *C. R. Math.* 343:763–766, doi 10.1016/j.crma.2006.10.027 (corrigendum *C. R. Math.* 348, 2010, doi 10.1016/j.crma.2010.02.006); Sason 2015, IEEE Information Theory Workshop, doi 10.1109/ITW.2015.7133079, Prop. 4. Both DOIs were checked on Crossref on 27 November 2026. The credit was missing until the hostile review of PR #295 found it. Only the step from that minimum to the learning-rate floor, through the identity of §3, is this note's.
