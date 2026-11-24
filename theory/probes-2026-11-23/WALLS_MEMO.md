# Attacking the three walls (phase 2 of the inverted-physics probe)

*Monday 23 November 2026, America/New_York. Written against `main` `d592662` (fresh clone in `/workspace/walls`, TMPDIR there, nice 19, deleted after). This is a scratch memo, not a PR, and a self-check rather than an independent review. `THEORY.md` is untouched and nothing was posted. No real-world data was used. Inputs: `/workspace/gtao/invert-2026-11-23/INVERT_MEMO.md` (reviewer-edited) and `/workspace/gtao/reviews-indep-2026-11-23/INVERT_REVIEW.md`. Labels: **PROVED (in-model)**, **KNOWN** (published, credited), **CONJECTURE**, **SPECULATION**, **FAILED-AT-STEP**. Checks C1–C5 are in `checks/` (hashes in `checks/SHA256SUMS`). Every DOI below resolves on api.crossref.org (`checks/crossref.out`, 41 records).*

> **[REVIEWER EDIT 2026-11-23]** An independent hostile review is in `/workspace/gtao/reviews-indep-2026-11-23/WALLS_REVIEW.md` (checks in `walls_review_checks/`). C1–C5 rerun byte-identical from a fresh copy and all hashes match. The W1 sign result holds. Corrections are marked inline. The main ones: (1) the two-judge result is a block-wise (partial) optimum of one biconvex function, obtained by Legendre-dualizing the known indefinite action. It is KNOWN in substance (Pavon 1995), and the fringes reach the mover through the pricer's potential rather than arising at a minimum of any single cost. (2) Clock–system *mutual* information is **twice** the entropy of the time-averaged state. (3) Hardy's Axiom 4 *is* local tomography, so door step (iii) re-derives an axiom Hardy already assumes. (4) Door step (ii) must also exclude classical continuous phase space, and at equal readable information it faces a record-count headwind.

> "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." (`CORE.md:7`)

Target: Level 4 in `theory/PHYSICS_CHAIN_2026-11-23.md:86-87`, "physics as the minimum-cost way for a universe to keep track of itself" (SPECULATION). The walls come from `INVERT_REVIEW.md` §9:
- **W1:** the cost reading works only in imaginary time.
- **W2:** nothing selects ħ.
- **W3:** nothing corresponds to GTAO's information about an outside world.

## 0. Bottom line

1. **The three walls are one wall.** In every route checked, real time, the factor *i*, and the "no outside world" question reduce to a single question: are the deepest records **probabilities** (real, nonnegative weights) or **amplitudes**? With probabilities you get imaginary-time physics: bridges, ground states, Markov clocks. With amplitudes you get real time. ħ appears only as the unit that converts one into the other. (C2, C3, C4.)
2. **"Minima can't interfere" is too strong as stated.** **[REVIEWER EDIT 2026-11-23]** Retitle: *a single cost's minimum still can't interfere; real time is an equilibrium of two coupled minimizers.* Split real-time quantum motion between two judges:
   - a **mover**, who pays the transport cost of shifting probability;
   - a **pricer**, who prices position information. The pricer's best price is the Fisher-information term at price ħ, i.e. Bohm's quantum potential.
   Wherever the density is nonzero, each judge's own problem is convex, and the quantum solution is each one's genuine global minimum. Interference fringes appear in the mover's minimizer (C1). The joint problem has no minimum; real time is the equilibrium point of the two (C1c). **PROVED (in-model)** where ρ>0.
   **[REVIEWER EDIT 2026-11-23]** What is proved: two elementary convexity facts, Benamou–Brenier convexity with a fixed potential and Donsker–Varadhan duality of the Fisher term. Each judge's minimum is a *best response with the other held fixed*. Both judges minimize the **same** function \(G(\rho,j,\phi)=\iint j^2/2\rho-(U+\phi)\rho+\int\Lambda(\phi)\), which is biconvex (convex in each block, not jointly). Real time is a partial optimum of G, and G decreases along joint directions (C1c, since \(G(\rho,j,Q[\rho])=A_R\)). "Pricer optimum = Bohm potential" holds by construction: the Legendre argmax is the gradient \(\delta F/\delta\rho=Q\) of the Fisher term the pricer was built from (reviewer R1b). The fringes in the mover's minimizer are imported through \(V=U+Q[\rho_{\rm QM}]\). So this does **not** show interference at a minimum of any single cost. It is a Fenchel-dual rewrite of Pavon's 1995 saddle, in which v minimizes and u "minimize[s] minus the action". KNOWN in substance; the min–min presentation was not found in print. The structure is close to known work: Pavon 1995 (Nelson's process as the saddle of a zero-sum game), von Renesse 2012, and Hall–Reginatto 2002. The two-convex-judges split is not claimed as new without a further search.
3. **Exactly where the *i* enters (W1), stated term by term.** The two-look judgment problem (the Schrödinger bridge) and real-time quantum mechanics have the **same continuity equation**. Their Hamilton–Jacobi equations differ in one sign only: the sign of (stake + quantum potential) (C2, symbolic). In GTAO terms:
   - imaginary time is "transport **plus** cost of judgment", minimized;
   - real time is "transport **minus** cost of judgment", held at an equilibrium point, with the total conserved.
   Real time is what the cost reading gives if exactly one price is negative. That violates the repo's nonnegative-price assumption A8 (`CORE.md:52`). **[REVIEWER EDIT 2026-11-23]** The flipped sign is a *relative* sign between transport and (stake + information). Stationary points do not see the overall sign, so the negative can be booked on the transport price alone (one price) or on both the stake and the information prices (two GTAO prices). A8 must fail somewhere, but the place is not unique (reviewer R1c). KNOWN in substance (Zambrini 1986; von Renesse 2012). The GTAO wording and the A8 location are new to the repo.
4. **W2 (ħ).** Requiring that a composite body obey the same noise law as an elementary body of equal mass (layer self-similarity) forces **one universal price for every mass** and the 1/m in Nelson's diffusion constant (C5b, elementary). It does not give a number. No number is possible: since the 2019 SI redefinition, the numerical value of h is fixed by definition. The physical questions are why there is one universal price (answered by the layer argument, as Adler 2004 answers it by equipartition) and dimensionless constants such as α ≈ 1/137, which nothing here touches. Chad's "set by the layer below" is literally Adler's trace dynamics: ħ, and even the *i*, appear as the equilibrium average of a conserved charge of a deeper classical matrix layer. KNOWN. Its value is assumed there too.
5. **W3 (no outside world).** For a closed universe with an internal clock (Page–Wootters), GTAO's "information about the world" term becomes the **clock–system mutual information**. That equals the entropy of the time-averaged system state (C4b, KNOWN: Boette et al. 2016). **[REVIEWER EDIT 2026-11-23]** Correction: for a pure global state, the *entanglement entropy* equals \(S(\bar\rho)\) (Boette et al. eq. 16, with \(\rho_S=\tfrac1N\sum_t|\psi_t\rangle\langle\psi_t|\)), and the *mutual information* is \(I(C{:}S)=2S(\bar\rho)\) (reviewer R2a: 2.1555 = 2 × 1.0778). C4b computed the entanglement entropy. So the term does have a counterpart, and W3 is not a wall. The real-time *i* in Page–Wootters comes from the clock's own unitary structure: the construction moves the *i* into the clock rather than producing it. With classical records, a closed ring-clock universe either freezes (any mixing dynamics) or can change only by discrete reversible jumps (C4c). **[REVIEWER EDIT 2026-11-23]** Precisely: change requires a periodic chain. Non-permutation block-cyclic stochastic maps also close the ring with change, but the change lives only in the weights of the cyclic classes, i.e. it is a permutation after coarse-graining (reviewer R2b).
6. **The one door with real (small) odds** is the reconstruction route:
   - Hardy 2001 derives quantum theory from five axioms. Axiom 2 ("Simplicity") says the number of parameters K takes **the minimum value consistent with the axioms**. That is a minimum-bookkeeping axiom, and the closest prior art to `PHYSICS_CHAIN:86` found so far. Hardy's paper is arXiv-only (`quant-ph/0101012`, read this pass), so it has no DOI in `crossref.out`.
   - Drop the single word "continuous" from his Axiom 5 and you get classical probability. Keep it and you get quantum theory with complex numbers.
   - Among real, complex and quaternionic quantum theory, only the complex one keeps the record count of a whole equal to the product of its parts' counts (local tomography; C5a; Hardy–Wootters 2012; Barnum–Wilce 2014). **[REVIEWER EDIT 2026-11-23]** In Hardy 2001 this product rule *is* Axiom 4 ("K = K_A K_B", verified verbatim). Complex numbers are then selected by Axiom 2 (smallest r in K = N^r) together with Axiom 5. Local tomography is an input there, not an output. Real quantum theory is ruled out experimentally (Renou et al. 2021).
   - **Most promising next derivation (CONJECTURE).** Show that GTAO's own cost does the work of three of Hardy's axioms:
     - (i) GTAO's heat floor needs a bath (`CORE.md:70`), so with no outside world only reversible record updates are allowed;
     - (ii) tracking a continuously drifting world without ruin then needs *continuous* reversible updates (Axiom 5);
     - (iii) layered tracking, where wholes are tracked through their parts (T44, `theory/BOUNDARY_SUFFICIENCY_2026-11-22.md:39,45`), means log-record cost adds over parts (local tomography).
     Together with Hardy, (i)–(iii) would select complex quantum theory as the cheapest self-tracking bookkeeping. Pieces (ii) and (iii) are where GTAO would add something. Nothing here is proved yet.
     **[REVIEWER EDIT 2026-11-23]** Weak points found in review: (i) holds only for the whole universe, because a subsystem can use the rest of a closed universe as its bath. (ii) Classical mechanics on a continuous phase space already has continuous reversible maps (Liouville flow). Hardy's continuity bites only with **finite** N, so (ii) needs a finite-capacity premise, which GTAO's price per nat might supply. At equal readable information (ln N, the Holevo cap), quantum records carry K = N² parameters against N classical ones (reviewer R2d), which pushes a record-count cost *toward* classical. (iii) T44 (`BOUNDARY_SUFFICIENCY:39,45`) is a conditional-independence (screening) statement, not a parameter count, so it does not imply K_AB = K_A K_B. Prior art on motivating continuity from continuous time: Höhn 2017 Rule 4, Masanes et al. 2013 Postulate 1, Dakić–Brukner 2011 Axiom 3′. Same phrase, not refereed: Brooke 2026, Zenodo, "Quantum Structure as Least-Cost Admissible Bookkeeping". No prior art was found for deriving continuity from *ruin-free tracking*. That narrow piece is the only candidate for something new.

**What opens a genuine new door?** Of the attack lines, only the reconstruction route above (line W3/W1-R) has a precise, falsifiable next step that GTAO's own machinery could supply. Every other line ends in KNOWN physics, rewritten in GTAO vocabulary. That rewriting is useful as a map, but it is not new.

## 1. Repo check before calling anything new

Grep on `d592662` for the following terms gave **no hits**: Caticha, Page–Wootters, Rovelli, QBism, Barbour, Nottale, stochastic electrodynamics / zero-point, Wallstrom, Madelung, Schrödinger bridge, imaginary time, Müller 2020, Lieb–Robinson.

Hits that do exist:
- **Zurek:** only Kibble–Zurek (`theory/FREEZE_PROCESS_2026-11-21.md:40`).
- **'t Hooft:** only holography (`theory/AREA_LAW_PROBE_2026-11-23.md:45`).
- **Adler:** only Adler 1946 locking (`litmap/PRIOR_ART.md:30`).
- **Smolin:** only cosmological natural selection (`reference/THEORY_v1.4.29.md:500`).
- **Risk-sensitive control:** Jacobson 1973 already credited (`THEORY.md:464`; `theory/GENERAL_THEOREM.md:292`, with Whittle 1990).
- **Friston:** the 2010 FEP and Markov blankets (`theory/NOVELTY_NOTE_2026-11-21.md:21`; T44 `theory/BOUNDARY_SUFFICIENCY_2026-11-22.md:39,45`).
- **Thermodynamic uncertainty relation:** Barato–Seifert (`litmap/LITMAP.md:21`).
- **Fisher information:** present, but not in the Madelung use.

Everything credited below is therefore new to the repo, and almost none of it is new to the literature.

## 2. The method, run on the walls

**Cost with named terms.** These are the INV-E pieces (`INVERT_MEMO.md` §2). In one dimension (with the gradient read as a vector in d dimensions), with \(\hbar=\lambda\) the price per nat:
- density \(\rho_t\);
- current \(j=\rho w\);
- transport (mover) cost \(K=\int |j|^2/(2m\rho)\);
- information (pricer) term \(F(\rho)=\tfrac{\lambda^2}{8m}\int|\nabla\rho|^2/\rho=\lambda\times\) (Donsker–Varadhan rate of ρ);
- stake \(\int U\rho\).

INV-E's stationary cost of judgment is \(j(\rho)=F(\rho)+\int U\rho\) (`INVERT_REVIEW.md` §1).

**Minimum / stationary point.** There are three readings:
- **Imaginary time (two-look bridge):** minimize \(\int (K + j)\,dt\) between two observed laws. This is the Schrödinger bridge, a convex problem with a unique minimum (KNOWN: Chen–Georgiou–Pavon 2016; Léonard 2014).
- **Real time:** the stationary point of \(\int(K - j)\,dt\). This is Madelung / von Renesse 2012: Newton's law on Wasserstein space with potential \(U+F\).
- **Two-judge split:** §3.2.

**Design read-off.** In imaginary time, prediction and retrodiction multiply into the density (a two-filter smoother). In real time they combine as a phase.

**Scope.** Spinless, nonrelativistic, finite-Fisher densities. All statements about the region where ρ>0 exclude nodes (Wallstrom). In d≥2 the current is assumed irrotational away from vortex lines.

## 3. W1 — real time

### 3.1 Two-look judgment (Schrödinger 1931 bridge). KNOWN; the term-by-term location of the *i* is PROVED (symbolic, C2)

**Cost.** The cost is \(\lambda\,\mathrm{KL}(Q\|P)\) over path laws Q with \(Q_0=\mu_0\) (prior look) and \(Q_T=\mu_T\) (later look), where P is free diffusion \(\sigma^2=\lambda/m\) killed at rate \(U/\lambda\) (Feynman–Kac).

**Minimum.** \(Q^*=f(X_0)g(X_T)P\), with \(\rho_t=\varphi_t\hat\varphi_t\):
- \(\hat\varphi\) (the prediction from the prior look) obeys the forward heat equation with \(-U/\lambda\);
- \(\varphi\) (the retrodiction from the later look) obeys the backward one.
This is the two-filter smoother of the Feynman–Kac model (Fraser & Potter 1969; Todorov 2008; Mitter & Newton 2003), and it is Zambrini's 1986 Euclidean quantum mechanics.

**Where the *i* enters, exactly.** Write \(\varphi=e^{(R+S)/\lambda}\), \(\hat\varphi=e^{(R-S)/\lambda}\), so \(\rho=e^{2R/\lambda}\). C2 derives symbolically:
- the bridge obeys \(\partial_t\rho+\partial_x(\rho\,\partial_xS/m)=0\) and \(\partial_tS+(\partial_xS)^2/2m-(U+Q_\lambda)=0\);
- \(\psi=e^{(R+iS)/\lambda}\) obeying \(i\lambda\partial_t\psi=-\tfrac{\lambda^2}{2m}\partial_x^2\psi+U\psi\) obeys the **same** continuity equation and \(\partial_tS+(\partial_xS)^2/2m+(U+Q_\lambda)=0\).

Here \(Q_\lambda=-\tfrac{\lambda^2}{2m}\partial_x^2\sqrt\rho/\sqrt\rho\). The only difference is the sign of \(U+Q_\lambda\), which is \(\delta j/\delta\rho\), the variation of INV-E's cost of judgment.

Equivalently:
- \(S/\lambda=\tfrac12\ln(\varphi/\hat\varphi)\) is half the log-ratio of retrodiction to prediction;
- real time turns that log-ratio into a phase (\(\varphi\to\psi\), \(\hat\varphi\to\psi^*\)).

The Guerra–Morato kinetic term is the **product** of forward and backward drifts, \(\tfrac m2 b\cdot b_*=\tfrac m2(v^2-u^2)\). The bridge charges their **average square**, \(\tfrac m2(v^2+u^2)\) (C2). So the *i* is a Lorentzian signature between transport (v) and information (u = osmotic velocity, whose cost is the Fisher term).

**GTAO reading.** Real time corresponds to the information term entering with a negative price. `CORE.md:52` makes nonnegative prices a separate assumption (A8), and `THEORY.md:474` (CT24) needs \(\varphi_i\ge0\). W1 is therefore exactly the place where A8 would have to fail for one term.

**Real-time two-look analogue.** Aharonov–Bergmann–Lebowitz 1964 (pre- and post-selection), KNOWN. It uses amplitudes, not a cost.

### 3.2 Two judges, each at a genuine minimum. PROVED (in-model) where ρ>0; numerically checked (C1); novelty unverified

**[REVIEWER EDIT 2026-11-23]** Relabel: *two judges, each at its best response; a partial optimum of one biconvex function.* The elementary facts are PROVED (in-model); the structure is KNOWN in substance (Pavon 1995; Donsker–Varadhan 1975; partial optima of biconvex functions, Gorski–Pfeuffer–Klamroth 2007, doi 10.1007/s00186-007-0161-1). C1(a)'s large pointwise residual is a stencil artifact everywhere, not just near the window edge: a closed-form derivative built from spectral derivatives of ψ gives a max residual of 2.7e−8 (reviewer R3a). In C1, ≥2 interior density maxima are present at 49% of the perturbation-support times, and ≥3 at 6% (R3b).

**Pricer.** By convex duality, \(F(\rho)=\sup_\phi[\langle\phi,\rho\rangle-\Lambda(\phi)]\), where \(\Lambda(\phi)\) is the top eigenvalue of \(\tfrac{\lambda^2}{2m}\Delta+\phi\) (Donsker–Varadhan). Hence \(-F(\rho)=\min_\phi[\Lambda(\phi)-\langle\phi,\rho\rangle]\), attained at \(\phi=Q_\lambda\) (+const), Bohm's potential. Under that potential, √ρ is the positive zero-mode.
- **C1d:** at a fringed density, \(\Lambda(Q)-\langle Q,\rho\rangle=-F=-0.47574518\), with \(\Lambda(Q)=5\times10^{-14}\). 300 random φ perturbations never go lower (min excess \(+5.9\times10^{-6}\)).

**Mover.** With \(V=U+\phi\) held fixed, the mover minimizes \(M[\rho,j]=\iint j^2/(2m\rho)-V\rho\) over \((\rho,j)\) obeying continuity, with fixed ends. M is jointly convex in \((\rho,j)\) (a perspective function plus a linear term). For any admissible perturbation supported where ρ>0, write \(\delta\rho=\partial_xA\), \(\delta j=-\partial_tA\), with A vanishing on the boundary. Then

(units m = 1 as in C1; general m by rescaling)

\[ M'-M=\iint\frac{(j'-\rho' w)^2}{2\rho'}\;+\;\iint A\,\big[\partial_tw+\partial_x(\tfrac12w^2+V)\big], \]

and the bracket vanishes by the quantum Euler equation. This needs no single-valued phase, only \(w=\mathrm{Im}(\psi^*\partial_x\psi)/\rho\). So the quantum path is the mover's global minimum among all such perturbations.
- **C1b:** harmonic stake, 400 random perturbations, a window where ρ ≥ 2% of its maximum, 3 interference maxima at early times. Results: first-order term ≤ \(1.4\times10^{-4}\) of its own scale; \(M'-M\ge0\) in every case; \(M'-M\) matches the quadratic term to a median \(2\times10^{-4}\).

**The joint problem is not a minimum.** The real-time action \(\iint K-F-U\rho\) **decreased** for 280 of the same 400 perturbations, mostly at high wavenumber (C1c). It is unbounded below, because a rough ρ makes F large. Real time is therefore an equilibrium point of two convex problems coupled through ρ and φ, not a joint optimum. In team-theory language (Radner 1962; not opened this pass), it is person-by-person optimal, not team-optimal.

**What this changes.** `INVERT_REVIEW.md` §2 says positive reweightings cannot interfere. That is right for one KL-control judge. With two coupled judges, each at a true convex minimum, the mover's minimizer carries interference fringes, because the price it faces (φ = Q) encodes them. The fringes come from the coupling, not from either minimization alone. **[REVIEWER EDIT 2026-11-23]** So INVERT_REVIEW §2 stands as stated for any single cost. The coupled pair does not minimize G jointly (G(ρ,j,Q[ρ]) = A_R is unbounded below). The fringes are a fixed-point property, and the mover sees them only because they are already written into its price.

**Scope.** No nodes in the support of the perturbation. At nodes, w and Q are singular. In d≥2 the Euler step also needs irrotational w, which fails on vortex lines. That is exactly Wallstrom's 1994 objection: Madelung plus single-valued S misses quantum states, and multivalued S needs an added quantization condition. Nothing here repairs it.

**Closest prior art:**
- Pavon 1995 (J. Math. Phys. 36:6774): Nelson's process is the saddle of a **zero-sum stochastic differential game**. The current velocity minimizes and the osmotic velocity maximizes the Guerra–Morato action. Chad's "system vs world" game is that result.
- von Renesse 2012: Schrödinger as a Hamiltonian flow on Wasserstein space with potential U + Fisher.
- Hall–Reginatto 2002: the Fisher term from an exact uncertainty principle.
- Benamou–Brenier duality: the certificate above is its standard form with a potential.

The split "two convex minimizers whose coupling gives real time" was not found in the search this pass. That is not a novelty claim. A dedicated search is needed before any claim.

### 3.3 Signed costs, entropic dynamics, Nelson

**Caticha's entropic dynamics** is the closest prior art for "quantum mechanics from inference". Read this pass: arXiv 1908.04693 = Entropy 21:943 (2019); Carrara–Caticha 2017 (arXiv 1708.08977); Bartolomeo–Caticha 2016 (arXiv 1603.08469).
- ED treats (ρ, Φ) as a phase space with a natural symplectic form. It adds an information-geometric metric, which yields Fubini–Study, and selects the flow that preserves both (a "Hamilton–Killing flow"). That flow is the linear Schrödinger equation.
- In ED, complex numbers come from the joint symplectic and metric structure.
- ħ is introduced as "an overall constant that fixes the units of the \(m_n\)s relative to the units of time" (1908.04693, eq. 16) and is identified with Planck's constant by matching (eq. 143–144).
- Single-valuedness and Wallstrom are handled through gauge symmetry and charge quantization (1908.04693 §10; Carrara–Caticha 2017).

**What GTAO adds to ED:** nothing to the derivation. GTAO's contributions would be:
- a cost reading of ED's conserved energy as transport + cost of judgment;
- the price bookkeeping (A8, CT24);
- the ruin cap, which ED does not have.
That is a relabel (KNOWN).

**Nelson / Guerra–Morato / Yasue / Madelung / Fisher (Reginatto 1998; Frieden 1989).** KNOWN. They are all the same Lorentzian split as §3.1. Wallstrom 1994 applies to all of them.

### 3.4 Saddle vs minimum; risk-sensitive control. KNOWN; C3 checks the formal price continuation

- **Risk-sensitive control** (Jacobson 1973; Whittle 1981; Fleming–Souganidis 1989; Dupuis–James–Petersen 2000) is equivalent to a zero-sum game against an adversary penalized by relative entropy. With a real risk parameter it stays on the imaginary-time side.
- **Price continuation.** Kappen's finite-horizon kernel with price λ and stake −U becomes the real-time (Mehler) propagator at **λ = iħ**. That is, the Feynman weight is the KL-control weight with an imaginary price per nat and a sign-flipped stake. C3(ii) matches exact evolution to about \(10^{-12}\) before and after the conjugate time, with the Maslov phase.
- **Real-price wall.** With a real price, the same stake −U makes the cost's second variation lose positivity exactly at the conjugate time \(T=\pi/\omega\) (C3(i): min eigenvalue +0.0005 at 3.14, −0.0027 at 3.15). With stake +U it never does.
- **Measure.** The continuation is formal. There is no countably additive "Wiener measure with imaginary variance" (Cameron 1960). So an imaginary price is not a cost in any measure-theoretic sense. **FAILED-AT-STEP:** "a GTAO cost with an imaginary price" fails at the step where a cost must be a real expectation.

## 4. W2 — why ħ

| Route | Gives a number? | Status |
|---|---|---|
| Layer self-similarity of the noise law: a composite of mass Nm obeys the elementary law at mass Nm | Forces D = λ/2m with **one** λ for all masses; no value | PROVED (elementary), C5b. With \(D\propto m^{-1/2}\), the implied price at masses 1, 8, 64 is 1, 2.83, 8 |
| Nelson 1966: D = ħ/2m | Postulated | KNOWN, relabel |
| Stochastic electrodynamics (Boyer 1975) | ħ is the amplitude of the zero-point spectrum (input) | KNOWN, relabel |
| Adler 2004 trace dynamics | ħ (and \(i_{\rm eff}\)) is the equipartition value of the conserved Adler–Millard charge of a deeper matrix layer. Universality comes from equilibrium; the value is a Lagrange multiplier, assumed. Verified via the book's description and a published review (arXiv quant-ph/0602078); the book itself was not read | KNOWN; closest match to "set by the layer below" |
| Caticha ED | Unit-fixing constant, matched | KNOWN, relabel |
| Nottale; 't Hooft 2016 (CA); Smolin | Not read this pass; no claim | — |
| Quantum speed limits (Mandelstam–Tamm; Margolus–Levitin 1998) | ħ is the slope: at most \(2E/(\pi\hbar)\) orthogonal ticks per unit time. In GTAO currency, ħ is the action price of one distinguishable tick. Thermal analogue: the TUR, already in the repo (`litmap/LITMAP.md:21`) | KNOWN, relabel |
| Real-time phase period | The same λ that prices the Fisher term sets the action period 2πλ for a single-valued ψ | KNOWN (Madelung, Wallstrom, Caticha §10) |

**Plain point for the record.** Since the 2019 SI redefinition, h = 6.62607015×10⁻³⁴ J s exactly, by definition (BIPM SI Brochure, 9th ed.; no DOI used). "Deriving the value of ħ" is a units question. The physical content is (a) universality, one price for everything, which layer consistency or equilibrium does supply, and (b) dimensionless constants (α), which nothing here reaches. W2 is therefore not a wall to the extent that ħ's value is a units choice. As a question about α it is wide open and untouched.

## 5. W3 — no outside world

**Closed self-tracking (Page–Wootters 1983).** A stationary universe state under "advance clock + advance system" (C4a: closure residual 3e−15). The conditional system states then evolve unitarily, so the Schrödinger equation is relative to the clock subsystem. This is Chad's "time relative to the next layer down", and it is KNOWN (Page–Wootters 1983; Giovannetti–Lloyd–Maccone 2015; Höhn–Smith–Lock 2021; experiment: Moreva et al. 2014).

**The GTAO term exists here.** GTAO's information-about-the-world term becomes \(I(C{:}S)\), the clock–system information. **[REVIEWER EDIT 2026-11-23]** For a pure history state, \(I(C{:}S)=2S(\bar\rho)\); the *entanglement entropy* equals the entropy of the time-averaged system state (C4b: 1.0777729111 = 1.0777729111; KNOWN, Boette–Rossignoli–Gigena–Cerezo 2016). A natural self-tracking cost is \(J=\lambda I(C{:}S)+w\,\mathbb E[\text{time-reading error}]\), a rate–distortion problem for a clock. Its minimum has not been computed here (CONJECTURE that it gives more than the speed limits; Gambini–Porto–Pullin 2004 is the known "realistic clock" decoherence line).

**W1 = W3.** In Page–Wootters, the *i* comes from the clock's unitary translation, the canonical structure of the clock. With classical (probability) records:
- a closed ring clock with any mixing Markov dynamics admits only the stationary law, so nothing ever changes (C4c: one unit-modulus eigenvalue; change across ticks 2e−16);
- only permutations, which are reversible and discrete, give change; **[REVIEWER EDIT 2026-11-23]** (or periodic chains, which are permutations of cyclic classes; R2b)
- the quantum case offers a continuous one-parameter family of reversible maps.

So "no outside world" plus "continuous change" pushes from probabilities to amplitudes. That is Hardy's Axiom 5 (verified text: "There exists a continuous reversible transformation on a system between any two pure states"). C4d shows the consequence: a two-path interference term of 0.5 (quantum) vs 0 (classical).

**Other frames, mapped (all KNOWN; GTAO adds no theorem):**
- **Relational QM (Rovelli 1996):** states are relative to systems, which is the PW stance.
- **QBism (Fuchs–Schack 2013):** the agent's coherence norms. It has no cost.
- **Quantum Darwinism (Zurek 2009):** redundant records make objectivity. That is a record-count economy, and a natural place for a GTAO price.
- **Müller 2020, "Law without law":** observer-state first, algorithmic.
- **Friston 2019** (arXiv 1906.10184, no DOI, not read this pass): Markov-blanket "particular physics". The repo already credits the FEP as anticipating the ambition (`theory/NOVELTY_NOTE_2026-11-21.md:21`).
- **Chiribella–D'Ariano–Perinotti 2011, purification:** every mixed state is part of a pure state of a larger system. This is the cleanest formal version of "there is no outside world: ignorance is always correlation with the rest of the same closed system". With their other axioms, it yields quantum theory.

## 6. The door: minimum bookkeeping for a closed, continuously self-tracking universe

**Known pieces:**
- Hardy 2001, Axiom 2 ("Simplicity"; verified): for each N, K takes the minimum value consistent with the axioms. Together with Axioms 1, 3 and 4, it gives K = N (classical). Adding continuity (Axiom 5) gives K = N² (complex quantum theory).
- Masanes–Müller 2011 and Chiribella–D'Ariano–Perinotti 2011 give related derivations.
- Local tomography (\(K_{AB}=K_AK_B\)) holds for complex quantum theory only. Real quantum theory needs extra "holistic" parameters (2×2: 10 vs 9; 4×4: 136 vs 100). Naive quaternionic counting falls short (28 vs 36), and quaternionic composites have no standard tensor product (C5a; Hardy–Wootters 2012; Barnum–Wilce 2014). Real quantum theory is experimentally falsified (Renou et al. 2021).

**GTAO-native conjecture (CONJECTURE).** Price records at λ per nat of record dimension (ln K per system). Impose three conditions:
- **(i) No bath.** No outside world, so no heat sink. GTAO's heat floor \(\dot Q_M\ge kT\,\dot I_M\) (`CORE.md:70`) then leaves only reversible record updates (C4c is the classical case).
- **(ii) A continuously drifting world tracked without ruin.** The conjecture is that reversible but discrete (permutation) updates have a lag/ruin cost floor that continuous reversible updates avoid. That would make Axiom 5 a cost minimum, not an axiom.
- **(iii) Layered tracking.** Wholes are tracked through parts (T44, `theory/BOUNDARY_SUFFICIENCY_2026-11-22.md:39,45`), so log record cost is additive over parts. That is local tomography, which selects ℂ.

Claim to try: under (i)–(iii), the minimum-cost record theory is complex quantum theory, with ħ entering only as the unit of the generator of the continuous reversible family.

**How it could fail:**
- **[REVIEWER EDIT 2026-11-23]** Classical continuous phase space already supplies continuous reversible tracking. Without a finite-capacity premise, step (ii) selects nothing.
- **[REVIEWER EDIT 2026-11-23]** At equal readable information (Holevo, ln N), the quantum record dimension is N² against N classically, so a cost per nat of record dimension favors classical unless the tracking-lag term pays for the difference.
- **[REVIEWER EDIT 2026-11-23]** Hardy's Axiom 4 already *is* local tomography, so (iii) must derive K_AB = K_A K_B itself. T44's screening statement does not give a parameter count.
- **[REVIEWER EDIT 2026-11-23]** A closed universe's subsystems can use the rest of the universe as a bath, so (i) constrains only the global dynamics, while Hardy's Axiom 5 is needed for every system.
- a discrete reversible tracker matches the continuous one's cost at equal K;
- a real-amplitude theory wins once its holistic parameters are priced at λ ln(K_AB/(K_AK_B)) (it loses by C5a's count, but the tracking-lag term could offset this);
- step (ii) cannot be made precise without assuming the Holevo-type readout limits that it is supposed to derive.

**Why this is the most promising line.** It is the only line where GTAO's own terms (the heat floor needing a bath, layered and boundary tracking, the ruin cap) would do work that the reconstruction literature currently does by axiom. It also reads Chad's three hunches as one claim:
- the next layer down sets time (Page–Wootters);
- no outside world (purification / closure);
- the minimum-cost way to keep track (Hardy's simplicity).

## 7. Per-line status

| Line | Status | Closest prior art |
|---|---|---|
| W1a two-look bridge = Euclidean QM; *i* = sign of (U+Q) / log-ratio → phase | KNOWN; term-level location PROVED (symbolic, C2) | Schrödinger 1931; Zambrini 1986; Nagasawa 1989; Léonard 2014; Chen–Georgiou–Pavon 2016, 2021; Fraser–Potter 1969 |
| W1 real time = transport − cost of judgment; needs one negative price (A8 fails) **[REVIEWER EDIT 2026-11-23]** relative sign; can be booked on transport | KNOWN in substance; GTAO wording new to repo | von Renesse 2012; Reginatto 1998; Hall–Reginatto 2002 |
| W1b two convex judges (mover + Fisher pricer), fringes at a genuine minimum | PROVED (in-model, ρ>0); C1. **[REVIEWER EDIT 2026-11-23]** Partial optimum of one biconvex G; fringes imported via φ=Q; KNOWN in substance (Fenchel-dual of Pavon 1995) | Pavon 1995 (zero-sum saddle); Benamou–Brenier duality; Donsker–Varadhan |
| W1b entropic dynamics | KNOWN; GTAO adds nothing to the derivation | Caticha 2011, 2019; Carrara–Caticha 2017; Bartolomeo–Caticha 2016 |
| W1b nodes / quantization | Puzzle stays open | Wallstrom 1994 |
| W1c imaginary price λ = iħ | Formal identity checked (C3); FAILED-AT-STEP as a cost (no measure) | Cameron 1960; Jacobson 1973; Whittle 1981; Dupuis–James–Petersen 2000; Kappen 2005 |
| W2 one universal price from layer self-similarity | PROVED (elementary), C5b; no value | Nelson 1966; Adler 2004 |
| W2 value of ħ | Not a physics question in SI 2019 units; α untouched | — |
| W2 ħ as slope of a trade-off | KNOWN, relabel | Mandelstam–Tamm; Margolus–Levitin 1998 |
| W3 closed system, clock–system information = GTAO world term | KNOWN identity (C4b; **[REVIEWER EDIT 2026-11-23]** entanglement entropy = S(ρ̄); mutual information = 2S(ρ̄)); cost minimum is a CONJECTURE | Page–Wootters 1983; Boette et al. 2016; Giovannetti–Lloyd–Maccone 2015; Höhn–Smith–Lock 2021 |
| W3 = W1 (the *i* lives in the clock / in amplitudes) | PROVED in the finite model (C4a, c, d); KNOWN in substance | Page–Wootters 1983; Hardy 2001 |
| Door: minimum record cost + closure + continuity + layering → complex QM | CONJECTURE (GTAO part); reconstruction parts KNOWN | Hardy 2001; Masanes–Müller 2011; Chiribella–D'Ariano–Perinotti 2011; Hardy–Wootters 2012; Barnum–Wilce 2014; Renou et al. 2021 |
| Level 4 sentence (`PHYSICS_CHAIN:86`) | Still SPECULATION. Its nearest formal realization is Hardy's simplicity axiom | Wheeler 1992 (already cited); Hardy 2001 |

**Model implications, stated plainly:**
- If physics is read as a minimum-cost bookkeeping, imaginary-time physics is a minimum.
- Real-time physics is an equilibrium point between a transport judge and an information judge, which requires one negative price or amplitude-valued records.
- This is not a derivation of quantum mechanics. GR and holography are not touched.

## 8. Checks (`checks/`, nice 19, seeds fixed)

- **C1 `c1_two_judge_certificate.py`.** The mover's minimum with fringes (b), the joint action not a minimum (c), and the pricer's minimum at Bohm's Q (d). In (a), the pointwise Euler residual's maximum is a finite-difference artifact near the window edge: the median relative residual is 4e−4, and the integrated first-order term is ≤1.4e−4.
- **C2 `c2_bridge_vs_realtime.py`.** Symbolic. Same continuity; the HJ sign of (U+Q) flips; b·b* = v²−u² vs (|b|²+|b*|²)/2 = v²+u².
- **C3 `c3_price_continuation.py`.** Conjugate-time positivity loss with a real price; λ = iħ reproduces exact evolution to ~1e−12 across t = π.
- **C4 `c4_closed_clock.py`.** Page–Wootters closure; I(C:S) = S(ρ̄); a closed classical ring clock freezes under mixing dynamics; interference 0.5 vs 0.
- **C5 `c5_records_and_price.py`.** Record counts for real, complex and quaternionic theories; layer self-similarity forces one price.
- **`crossref.py` → `crossref.out`.** 41 DOIs, all OK. The Fleming–Souganidis 1989 record has an empty title field on Crossref; venue, volume and page match.

## 9. Sources (Crossref-verified 23 Nov 2026 unless marked)

Caticha 2011 J. Phys. A 44:225303, 10.1088/1751-8113/44/22/225303 · Caticha 2019 Entropy 21:943, 10.3390/e21100943 · Wallstrom 1994 PRA 49:1613, 10.1103/PhysRevA.49.1613 · Page & Wootters 1983 PRD 27:2885, 10.1103/PhysRevD.27.2885 · Giovannetti, Lloyd & Maccone 2015 PRD 92:045033, 10.1103/PhysRevD.92.045033 · Höhn, Smith & Lock 2021 PRD 104:066001, 10.1103/PhysRevD.104.066001 · Masanes & Müller 2011 NJP 13:063001, 10.1088/1367-2630/13/6/063001 · Chiribella, D'Ariano & Perinotti 2011 PRA 84:012311, 10.1103/PhysRevA.84.012311 · Hardy & Wootters 2012 Found. Phys. 42:454 (Crossref issued 2011), 10.1007/s10701-011-9616-6 · Barnum & Wilce 2014 Found. Phys. 44:192, 10.1007/s10701-014-9777-1 · Renou et al. 2021 Nature 600:625, 10.1038/s41586-021-04160-4 · Wootters 1981 PRD 23:357, 10.1103/PhysRevD.23.357 · Adler 2004 CUP, 10.1017/CBO9780511535277 · 't Hooft 2016 Springer, 10.1007/978-3-319-41285-6 (not read) · Boyer 1975 PRD 11:790, 10.1103/PhysRevD.11.790 · Cameron 1960 J. Math. Phys. (MIT) 39:126, 10.1002/sapm1960391126 · Jacobson 1973 IEEE TAC 18:124, 10.1109/TAC.1973.1100265 · Whittle 1981 Adv. Appl. Probab. 13:764, 10.2307/1426972 · Dupuis, James & Petersen 2000 MCSS 13:318, 10.1007/pl00009872 · Fleming & Souganidis 1989 Indiana Univ. Math. J. 38:293, 10.1512/iumj.1989.38.38015 · Swiecicki, Gobron & Ullmo 2016 PRL 116:128701, 10.1103/PhysRevLett.116.128701 and Ullmo, Swiecicki & Gobron 2019 Phys. Rep. 799:1, 10.1016/j.physrep.2019.01.001 (mean-field games ↔ imaginary-time NLS: multi-agent judges stay on the Euclidean side) · Chen, Georgiou & Pavon 2016 JOTA 169:671 (Crossref issued 2015), 10.1007/s10957-015-0803-z · Hall & Reginatto 2002 J. Phys. A 35:3289, 10.1088/0305-4470/35/14/310 · Aharonov, Bergmann & Lebowitz 1964 Phys. Rev. 134:B1410, 10.1103/PhysRev.134.B1410 · Margolus & Levitin 1998 Physica D 120:188, 10.1016/S0167-2789(98)00054-2 · Rovelli 1996 IJTP 35:1637, 10.1007/BF02302261 · Zurek 2009 Nat. Phys. 5:181, 10.1038/nphys1202 · Fuchs & Schack 2013 RMP 85:1693, 10.1103/RevModPhys.85.1693 · Müller 2020 Quantum 4:301, 10.22331/q-2020-07-20-301 · Nagasawa 1989 PTRF 82:109, 10.1007/bf00340014 · Todorov 2008 CDC 4286, 10.1109/CDC.2008.4739438 · Fraser & Potter 1969 IEEE TAC 14:387, 10.1109/TAC.1969.1099196 · Moreva et al. 2014 PRA 89:052122, 10.1103/PhysRevA.89.052122 · Boette, Rossignoli, Gigena & Cerezo 2016 PRA 93:062127, 10.1103/PhysRevA.93.062127 · Gambini, Porto & Pullin 2004 PRL 93:240401, 10.1103/PhysRevLett.93.240401 · von Renesse 2012 Can. Math. Bull. 55:858, 10.4153/CMB-2011-121-9 · Pavon 1995 J. Math. Phys. 36:6774, 10.1063/1.531187 · Guerra & Morato 1983 PRD 27:1774, 10.1103/PhysRevD.27.1774 · Zambrini 1986 J. Math. Phys. 27:2307, 10.1063/1.527002 · Köppe, Grecksch & Paul 2017 Ann. Phys. 529:1600251 (Crossref issued 2016), 10.1002/andp.201600251.

No DOI (arXiv or book, read where marked): Hardy 2001, arXiv quant-ph/0101012 (axioms read verbatim) · Caticha arXiv 1908.04693, Carrara & Caticha arXiv 1708.08977, Bartolomeo & Caticha arXiv 1603.08469 (read) · Friston 2019, arXiv 1906.10184 (not read) · Radner 1962 team theory (not opened; cited only for terminology) · BIPM SI Brochure 9th ed. 2019. Already in the INVERT memo: Nelson 1966, Léonard 2014, Chen–Georgiou–Pavon 2021, Kappen 2005, Reginatto 1998, Frieden 1989, Yasue 1981, Mitter–Newton 2003, Donsker–Varadhan 1975.

## 10. For Chad (plain words, audio)

**[REVIEWER EDIT 2026-11-23]** Revised paragraph (the original over-sold the two-judge result and Hardy's paper):

You were right that "walls" was the wrong picture. The three turned out to be one question: are nature's deepest records plain odds, or arrows that can point different ways and cancel? Plain odds give the imaginary-time version, where cheapest-path reasoning works. Arrows give real time and interference. Real time does come out as a standoff between two judges, one moving things and one pricing where things are. That part checks out, but it's a 1995 result in new clothes, and the interference only shows up because each judge is reacting to the other. No single cost produces it. Your "time comes from the layer below" idea is real physics from 1983: time is read off an internal clock, and with no outside world, the information term we thought was missing comes back as the link between the clock and everything else. For Planck's constant, its number is now a units choice. "One price for everything" does follow from asking that bigger things obey the same rule as smaller ones. The best remaining door is a 2001 result by Lucien Hardy: quantum theory uses the fewest numbers that still let things change smoothly. Others have built on that idea, so the door isn't new. The one piece that might be ours is showing that smooth change is forced by tracking a changing world without going broke. My honest odds are low. The likely sticking point is that ordinary smooth physics also changes smoothly, and quantum records carry more numbers for the same readable information. Still, that's the one derivation worth running next.
