# The mirror probe: what forces the backward factor to be the complex conjugate?

*Monday 23 November 2026, about 9:10–10:15 PM EST (America/New_York). Written against GTAO `main` `d592662` (fresh clone in `/workspace/mirror`, TMPDIR there, nice 19, deleted after). This is a scratch memo, not a PR. It is a self-check only; an independent review is still to come. [REVIEWER EDIT 2026-11-23: independent hostile review done, `reviews-indep-2026-11-23/MIRROR_REVIEW.md`; edits are marked inline.] `THEORY.md` is untouched, nothing was posted, and no real-world data was used. Inputs: `walls-2026-11-23/WALLS_MEMO.md` (reviewer-edited), `reviews-indep-2026-11-23/WALLS_REVIEW.md` and `INVERT_REVIEW.md`. Labels: **PROVED (in-model)**, **KNOWN** (published, credited), **CONJECTURE**, **SPECULATION**, **FAILED-AT-STEP**. Checks M1–M4 are in `checks/`, with hashes in `checks/SHA256SUMS`. All 26 DOIs below resolve on api.crossref.org (`checks/crossref.out`).*

> "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." (`CORE.md:7`)

**Question (Chad, t2365u: "the two times? They are the same thing. Mirror. One.").** The Schrödinger bridge, our two-look judgment, gives ρ = φ·φ̂: a backward heat solution times a forward heat solution, two independent real functions. Quantum mechanics gives ρ = ψ·ψ̄: one forward wave times its own complex conjugate. What forces the backward factor to be the conjugate mirror of the forward one?

**Repo grep before calling anything new.** The repo has no hits for Aharonov, two-state vector, Wharton, transactional, Zambrini, Bernstein, Osterwalder, reflection positivity, Eddington or 1/137. "Mirror" appears only in unrelated senses (`OPEN_WORK.md:122`; `theory/SCALE_ENDS.md:319` cites Hayden–Preskill "Black holes as mirrors"). "Complex conjugate" appears only for world rhythms (`core/KEYSTONE_NOTE.md:37`). "Fine-structure" appears only as a Lieb–Yau parameter (`theory/TRANSPORT_BARRIER_2026-11-23.md:105`). Everything below is therefore new *to the repo*. Where it is known in print, it is credited as such.

## 0. Bottom line

1. **Chad is right that the two times are one mirror, and the mirror is a known, central object.** If the judgment is invariant under swapping its two looks (past ↔ future), the cheapest two-look judgment is a **mirror pair**, φ(τ) = φ̂(−τ). Continue that pair from imaginary time τ to real time t (τ = it), and the **Schwarz reflection principle** turns the time mirror into complex conjugation: φ(it) = conj φ̂(it). The product is then exactly the Born density |e^{−itH}h|² (M1a–b, agreement to about 1e−15). **PROVED (in-model)** on a lattice with a real Hamiltonian. **KNOWN in substance:** this is Osterwalder–Schrader reflection positivity (1973), the standard bridge from imaginary-time to real-time quantum theory, and close to the gluing in Hartle–Hawking (1983); Schwinger's closed time path (1961) is an analogous forward–backward fold in real time [REVIEWER EDIT 2026-11-23: was "the same gluing"]. Short version: **complex conjugation is what a time mirror looks like after the Wick turn.** [REVIEWER EDIT 2026-11-23: circular in a precise sense: the real, time-symmetric H already carries the conjugation symmetry, and the Born equality holds for any real record with no minimization (R1a). The cost supplies only the mirror pair.]
2. **Independent factors are the two-state vector; the mirror is "no outside post-selector."** With *different* first and second looks, the same continuation gives a complex, sometimes negative "weak" density whose total is still conserved (M1c). That is the Aharonov–Bergmann–Lebowitz / two-state-vector picture (1964, 1990), with χ ≠ ψ. The Born rule is the special case where the second look carries no independent information: it is the system's own record, χ = ψ. **KNOWN** physics; the GTAO reading, "no outside world ⇔ backward state = forward state ⇔ Born", is new to the repo (CONJECTURE as an interpretation). [REVIEWER EDIT 2026-11-23: χ = ψ is a final condition that carries no independent information (a trivial post-selection); that ABL reduces to Born without post-selection is itself KNOWN (ABL 1964). Only the "no outside world" reading is the conjecture.]
3. **[REVIEWER EDIT 2026-11-23: relabeled KNOWN; see §4 notes] GTAO restatement of a known link: the mirror of a stationary Markov law exists exactly where net heat is zero.** For a stationary Markov judge, the time mirror is a positive inner product (reflection positivity, with complex functionals) **if and only if** the process obeys detailed balance, which holds if and only if entropy production is zero (M2; any drive > 0 breaks it). Through the heat floor (`CORE.md:70`, Q̇_M ≥ kT·İ_M), a tracker with a positive net learning rate produces entropy and so **cannot** carry the mirror on its own path measure. **KNOWN** [REVIEWER EDIT 2026-11-23: was "PROVED (in-model)"; this is the reversibility criterion (Kolmogorov 1936; Kelly 1979; Klein–Landau 1981), and İ_M > 0 ⇒ nonzero currents ⇒ no detailed balance follows without the heat floor (Horowitz–Esposito 2014). Only the GTAO wording is new to the repo.] Model implication, stated plainly: *information about an outside world costs the mirror* [REVIEWER EDIT 2026-11-23: "exactly" removed; one-way only, since the mirror is also lost with zero learning (R3 case C); and this concerns the tracker's real-time Markov law, not a quantum Euclidean measure (R4b)]. An open, tracking judge lives on the one-way heat side, and the mirror (with it a Hilbert space and a real-time unitary group via OS) is available only for the closed, zero-net-flow part.
4. **Second, independent route: the record's norm.** A record that changes continuously, two-way (reversibly) and with mixing, while keeping a norm, must use the 2-norm (M3: isometry Lie algebra has dimension n(n−1)/2 over ℝ and n² over ℂ at p = 2, and only trivial or phase-only for p ≠ 2; Lamperti 1958). The 2-norm weight of a complex entry is z·z̄, so summing over an unobserved future leaves conj(forward) as the backward factor. Probabilities (1-norm) leave the factor 1 instead. **KNOWN.**
5. **What this does not do.** The factor *i* still enters by analytic continuation. The mirror explains the *conjugate*, not the *i*. With a real Hamiltonian, a real-linear mirror reaches only time-reversal-invariant data (real h). For complex data, or a Hamiltonian that is not time-reversal invariant (magnetic flux), the mirror has to be the **antilinear** Θ = (time reflection) ∘ (conjugation), i.e. Wigner's time reversal (M1d–e). So in general, part of the conjugation is put in through Θ, not derived. Nothing here derives quantum mechanics. [REVIEWER EDIT 2026-11-23: for a Hamiltonian that is not time-reversal invariant, e^{−sH} is not a positive kernel, so the GTAO path-KL cost is not even defined there (Feynman–Kac–Itô weights are complex).]
6. **Item (4), the bounded side branch: no route to a physical dimensionless constant was found.** GTAO's pure numbers are exponent and geometry factors, not couplings. The look-elsewhere test (M4) shows that a menu of 1.8×10⁸ simple formulas hits α⁻¹ to 10⁻⁶ fifteen times by chance. Details in §6.

## 1. The GTAO method, explicitly

- **Cost (named terms).** J[P] = λ·KL(P ‖ R) + E_P ∫ U(X_τ) dτ, with:
  - λ = price per nat of steering the path law P away from the reference R (the judgment price);
  - U = the stake;
  - two looks as constraints: ρ_{−T} = ρ_a and ρ_{+T} = ρ_b;
  - ruin cap absent or slack.
  This is the priced-information form of `CORE.md:52` (A1–A8 priced sum, nonnegative prices) with the memory term read as path KL, as in INVERT/WALLS.
- **Minimum.** The Schrödinger system. Write K_s = e^{−sH}, H = −½Δ + U (λ = 1 units). Then φ̂_τ = K_{τ+T} φ̂_{−T} and φ_τ = K_{T−τ} φ_T, with ρ_τ = φ̂_τ φ_τ. The pair is unique up to the gauge φ̂ → φ̂/c, φ → cφ (KNOWN: Schrödinger 1931; Föllmer; Léonard 2014; Chen–Georgiou–Pavon 2016, 2021).
- **Design.** The pair (φ̂, φ): the forward and backward "messages" of the two-filter smoother.
- **Scope.** Finite lattice (n = 40), real symmetric H (a time-reversal-invariant reference), Feynman–Kac reference, looks at ±T. M1e adds a complex-Hermitian ring with flux. M2 uses finite continuous-time Markov chains. No claim is made outside these classes.

## 2. Item (1): the time mirror and the conjugate

**Proposition M (mirror pair). PROVED (in-model).** Assume the reference is invariant under τ ↦ −τ (true for the Feynman–Kac reference of a real symmetric H, i.e. a reversible reference), and the looks are symmetric (ρ_a = ρ_b = r). Then, after gauge fixing, φ_T = φ̂_{−T} =: g and φ(τ) = φ̂(−τ) for all τ ∈ [−T, T].

*Proof.* Time reflection maps the problem to itself, so it maps the unique minimizer to itself. Under reflection the forward and backward factors swap. Fixing the gauge gives equality. M1a: gauge-fixed |φ̂_{−T} − φ_T|/max = 1.3e−14, and max_τ |φ(τ) − φ̂(−τ)| = 8.5e−15.

**Proposition S (Schwarz reflection ⇒ conjugate pair). PROVED (in-model).** Under Proposition M, z ↦ φ̂(z) = K_{T+z} g is holomorphic for Re z > −T, and z ↦ φ(z) = K_{T−z} g is holomorphic for Re z < T. Both domains contain the imaginary axis. Since H and g are real, φ̂ is real on the real axis, so φ̂(z̄) = conj φ̂(z). Then φ(it) = φ̂(−it) = conj φ̂(it), and

  ρ(it) = φ̂(it)·φ(it) = |e^{−itH} h|², where h = e^{−TH} g,

which is the Born density of h evolved in real time. M1b over t ∈ [0, 6]: |φ(it) − conj φ̂(it)| ≤ 2.8e−15, |ρ − |ψ_t|²| ≤ 9.5e−16, and the norm is conserved to 2.4e−15.

**What forces the conjugate, stated exactly.** Three things: (a) a reversible (reflection-invariant) reference, (b) a judgment invariant under swapping its looks, and (c) real Euclidean records (probabilities). Then the conjugate is the image of the time mirror under continuation, not an extra assumption. **KNOWN in substance:** in Osterwalder–Schrader, the Hilbert-space inner product is defined as ⟨F, G⟩ = E[conj(ΘF)·G] with Θ the time reflection, and real time is reached by exactly this continuation (OS 1973, 1975; Nelson 1973 for Markov fields). Zambrini's Euclidean quantum mechanics (1986) and Nagasawa (1989) use the same (φ̂, φ) pairing.

**[REVIEWER EDIT 2026-11-23]** **Circularity check (R1).** The conjugate is not derived from the cost; it is relocated into premises (a) and (c) plus a fourth, (d) the choice τ = it. A real H means H commutes with complex conjugation in the position basis, i.e. the antilinear time reversal is a symmetry of the reference by assumption. Given (a), (c), (d), the identity conj K(z) = K(z̄) holds exactly (R1b: 0.0), and the product equals the Born density for **any** real g, with no minimization at all (R1a: 6e−16 over five random real g). The minimization contributes only Proposition M (the mirror pair), which itself is the one-line symmetry-plus-uniqueness argument. Rotating by any angle other than π/2 gives a product that is not a modulus squared (R1c), and a real but non-reversible reference breaks the mirror pair (R1d: 1.05). So "PROVED (in-model)" stands for the statement, but the 1e−15 agreements confirm the code, not physics, and the claim is KNOWN in substance (OS; Zambrini).

**Limits (honest scope).**
- **Real data only, unless the mirror is antilinear.** With a complex record g, the real-linear mirror fails. The antilinear mirror φ_T = conj g gives Born for any ψ₀ = e^{−TH}g, a dense set of states (M1d: 1.0e−15).
- **Hamiltonians that are not time-reversal invariant.** With magnetic flux on a ring, the real-linear mirror gives |φ(it) − conj φ̂(it)| = 2.0 and a complex Euclidean density (max |Im| = 3.6). The antilinear mirror with the transposed backward kernel gives 0 and a positive Euclidean density (M1e). So the general mirror is Wigner's antilinear time reversal, and the conjugation is partly put in through Θ.
- **[REVIEWER EDIT 2026-11-23]** M1d and M1e are algebraic identities, not tests: with real H, K(T−it)·conj g = conj(K(T+it)g) exactly, and with complex H, conj(e^{−zH}) = e^{−z̄ H^T}, so the "0.0" in M1e is the definition of the transposed kernel. Also, for a Hamiltonian that is not time-reversal invariant, e^{−sH} is not a positive (Feynman–Kac) kernel, so the GTAO path-KL cost and the Schrödinger bridge are not defined there; the antilinear mirror lies outside the cost's domain.
- **The *i*.** It still enters through τ = it. The mirror accounts for "times its conjugate"; it does not account for "why rotate time."

**Chad's specific candidates.**
- *One judge serving both directions.* That is Proposition M: one reflection-invariant problem, one minimizer, which is its own mirror. **PROVED (in-model).**
- *A single record read forward and backward.* In real time, propagating the final self-record back gives the forward state exactly, because U⁻¹ = U† (M3: 1.8e−16). In imaginary time it does not: K^T K f ≠ f, with relative residual 0.50 (M3). Instead, the self-record makes the Euclidean problem a bridge reflected about the look time, which is again Proposition M on a doubled interval. **PROVED (in-model).**
- *No outside world, so the second look is the system's own record.* This is item 2 of §0 and §3. It selects χ = ψ, the Born case. **KNOWN** physics, GTAO reading new to the repo.

## 3. Independent factors = the two-state vector

M1c uses asymmetric looks (ρ_b ≠ ρ_a) with the same continuation. ρ(it) = ⟨χ_t|x⟩⟨x|ψ_t⟩ has max relative |Im| = 0.96 and min relative Re = −0.67, while Σρ is conserved to 3e−15. This is the ABL two-state vector's "weak" distribution: complex and sometimes negative, but normalized by a bilinear pairing. **KNOWN** (Aharonov–Bergmann–Lebowitz 1964; Aharonov–Albert–Vaidman 1988; Aharonov–Vaidman 1990).

So the bridge's two independent factors are not a defect. They are the general two-state object, and the Born rule is the diagonal case. In GTAO words: an **outside** post-selector supplies an independent second look (χ ≠ ψ, weak values). With **no outside world**, the second look is the system's own record (χ = ψ, Born). **CONJECTURE** as an interpretation; the math is KNOWN.

## 4. When does the mirror exist? Reflection positivity ⇔ zero net heat

**Proposition H. KNOWN** [REVIEWER EDIT 2026-11-23: relabeled from PROVED (in-model). This is the textbook reversibility criterion: for a stationary Markov law, reflection invariance ⇔ D_μL symmetric ⇔ Kolmogorov cycle criterion ⇔ detailed balance (Kolmogorov 1936; Kelly 1979), and given invariance, positivity follows from the Markov property (Klein–Landau 1981; Neeb–Ólafsson 2018). R2 shows the three textbook diagnostics vanish exactly where M2's Gram test passes. The finite-chain proof below is correct; nothing in it is new.] for finite stationary continuous-time Markov chains with generator L and stationary law μ.
- (⇐) If L obeys detailed balance, the reversed process has the same law, and the past and future of X₀ are conditionally independent given X₀. So E[conj(ΘF)·F] = Σ_x μ(x)|E[F | X₀ = x]|² ≥ 0 for every complex functional F of the positive-time path. This direction is standard (KNOWN).
- (⇒) For single-time functionals F = f(X_s), E[conj(ΘF)F] = ⟨f, e^{2sL} f⟩_μ. If this is real for every complex f and every s > 0, then D_μ e^{2sL} is Hermitian for all s. Differentiating at s = 0 shows D_μ L is symmetric, which is detailed balance, which in turn is zero entropy production (Schnakenberg 1976).

**M2** biases one cycle of a 5-state chain with drive d. At d = 0, entropy production is 0 and the Gram matrix is symmetric with min eigenvalue −6e−18 (numerical zero). For d = 0.1 to 4, entropy production runs 0.005 to 15.1 (k_B per unit time). ‖G − Gᵀ‖/‖G‖ runs 0.026 to 0.43, and the symmetric part has a negative eigenvalue (down to −1.0e−3), so even the real-functional mirror fails. An explicit witness gives E[conj(ΘF)F] = −0.00079 + 0.00149i: not a positive inner product.

**Link to the GTAO floor.** `CORE.md:70`: Q̇_M ≥ kT·İ_M. A memory with a positive net learning rate pays positive heat, so the joint memory–world chain produces entropy. By Proposition H, its path measure has no reflection-positive mirror. Each step is PROVED (in-model); the composition is new to the repo.

**[REVIEWER EDIT 2026-11-23]** The composition is valid but the heat floor is not needed and the step is KNOWN. Information flow İ_M is a sum of edge currents times log-ratios, so detailed balance (all currents zero) gives İ_M = 0 directly (Horowitz–Esposito 2014). Contrapositive: İ_M ≠ 0 ⇒ some current ≠ 0 ⇒ not detailed balance ⇒ no mirror (R3: case A İ_M = 1.8e−15; case B İ_M = 1.10, Q_M = 1.35 ≥ İ_M). Scope: `CORE.md:70` is a steady-state / long-run statement, and Proposition H is stationary; a transient learner started out of equilibrium is outside both (R2 scope line). Also, the statement is about the *joint* memory–world chain; the memory's own marginal path law is not Markov and is not covered.

**Model implication, stated plainly (SPECULATION beyond the model).** The mirror pairing, and with it the OS route to a Hilbert space and unitary real time, is available only for the zero-net-flow, closed part of a system. Tracking an outside world puts a judge on the one-way side, where its cost is a plain cheapest path with no conjugate. This fits the earlier W3 result: with no outside world, the information term returns as clock–system correlation (`WALLS_MEMO.md` §0 item 5).

**[REVIEWER EDIT 2026-11-23]** Two cautions. (1) **Levels.** Proposition H is about the physical, real-time Markov law of a tracker. The OS mirror that yields Hilbert space and unitary time is a property of a *Euclidean* (imaginary-time) measure. Any quantum whole with a Hamiltonian bounded below has a reflection-positive Euclidean structure (antilinear Θ if needed), whatever its parts do in real time; e.g. the flux ring carries a persistent current and is OS-positive (R4b). So "the mirror is available only for the zero-net-flow part" is not shown and mixes the two levels. (2) **One-way.** Learning ⇒ no mirror; the converse fails: a driven world with a decoupled memory has entropy production 2.08 and learning rate 0, and loses the mirror anyway (R3 case C). "Costs exactly the mirror" is therefore too strong; "cannot keep the mirror" is the supported wording. Label: SPECULATION.

## 5. Item (3): a GTAO cost whose minimizer pair is a conjugate pair?

- **Imaginary-time cost, symmetric looks → mirror pair → conjugate pair on continuation.** Yes: Propositions M and S. **PROVED (in-model)**; KNOWN in substance (OS, Zambrini).
- **A real cost minimized directly in real time with a conjugate-pair minimizer.** **FAILED-AT-STEP** "minimum": a real convex cost has a real minimizer, and real-time Schrödinger dynamics is a stationary point, not a minimum (Pavon 1995, whose abstract calls it a "saddle-point action principle"; earlier Yasue 1981 and Guerra–Morato 1983 [REVIEWER EDIT 2026-11-23: credit added]; WALLS C1c, a block-wise optimum of a biconvex function). Wallstrom 1994 still applies to any purely hydrodynamic (ρ, S) version.
- **Fisher-information price.** The pricer's best response is Bohm's Q (WALLS §0 item 2, reviewer R1b: true by construction). It contributes no conjugation. **FAILED-AT-STEP** "conjugate pair."
- **Ruin cap.** The ruin-cap optimum is a Doob h-transform (INVERT Prop R): a one-sided bridge whose backward factor is the survival function h, not a mirror of the forward factor. **FAILED-AT-STEP** "mirror." A symmetric two-sided ruin cap would reduce to Proposition M.
- **Single shared record, norm route.** Two-way, continuous, mixing change that keeps the record's norm forces the 2-norm (M3; Lamperti 1958; Aaronson 2004, arXiv quant-ph/0401062, not read this pass, cited for the statement only). Then the backward factor is conj(forward) over ℂ and the identity over ℝ. **KNOWN.** The choice of ℂ over ℝ is the Hardy / local-tomography route from WALLS §0 item 6. Real quantum theory is excluded experimentally (Renou et al. 2021).

## 6. Item (4), bounded side branch: can a GTAO cost fix a dimensionless constant?

**What counts as a genuine derivation, as opposed to a fit:**
- (a) the formula is fixed and hash-locked before comparison;
- (b) it has zero adjustable parameters and no choice from a menu;
- (c) it matches to better than the look-elsewhere rate of its menu, and for α that means near CODATA's 1.6e−10 (α⁻¹ = 137.035999177(21), CODATA 2022, NIST page fetched tonight);
- (d) it says *which* α. α runs, ≈ 1/137.036 at q → 0 and ≈ 1/128 at the Z mass, so a derivation has to pick a scale and predict the running;
- (e) it predicts a second constant it was not tuned on.

**Known failure mode (KNOWN).**
- Eddington 1929 argued 136, then 137 (Proc. R. Soc. A 122:358).
- Wyler 1969 gives 137.03608, now 6.1e−7 off, which is thousands of standard uncertainties.
- M4 looks across 2^a 3^b 5^c π^d e^f with simple rational exponents: 1.85×10⁸ formulas give 15 hits within 1e−6 and 1 within 1e−8. Wyler-level agreement is what chance delivers from such a menu.
  - **[REVIEWER EDIT 2026-11-23]** Reviewer recomputed the chance expectation from the density of the menu's log-values at ln 137.036: 14.65 expected hits within 1e−6 (observed 15) and 0.15 within 1e−8 (observed 1). Wyler's formula, α⁻¹ = 2^(19/4)·3^(−7/4)·5^(1/4)·π^(11/4), uses an exponent outside this menu; its error is ≈ 3,970 CODATA standard uncertainties. CODATA 2022 value 137.035999177(21), relative 1.6e−10, confirmed on physics.nist.gov (`mirror_review_checks/codata_nist.txt`).

**GTAO's own pure numbers.**
- CT24 shares (α−1)/α (`THEORY.md:101`, `THEORY.md:169`; GTAO's α there is an error-cost exponent, not the fine-structure constant).
- The virial shares k/(k+2).
- The Kalman factor 2 (`CORE.md:76`).
- √6 in T* (`CORE.md:100`).
- The pooling exponent n^{1/a} (CT28, `THEORY.md:125`).

All of these are fixed by model exponents and geometry, like the ½ in the virial theorem. None is a ratio of two couplings, which is what α is (e²/4πε₀ħc). **CHECKED by inspection** [REVIEWER EDIT 2026-11-23: was "PROVED (in-model)"; an inspection of a list is not a theorem] of their derivations: each is a rational or algebraic function of the model's integer exponents.

**The only legitimate pattern found: a fixed point of a nested-layer map.** Feigenbaum's δ ≈ 4.669 (1978) is a genuine dimensionless constant produced by self-consistency between nested levels (renormalization). If CT34's exact nesting (a team's minimized cost folds into its parent's problem) defined a nonlinear map on cost shapes with a nontrivial fixed point, its scaling ratio would be a universal GTAO number. That is **CONJECTURE**, and it is untested. Connecting such a number to α would also require α to be a fixed-point ratio. QED's α is not at a fixed point (it runs, with a Landau pole), so **no route to α was found. Be blunt: none.** Calling any GTAO number "α" without (a)–(e) would be numerology.

## 7. Literature for item (2): what is known

| Work | What it says that bears on the mirror | Label |
|---|---|---|
| Osterwalder & Schrader 1973, 1975 | Reflection positivity: the time mirror Θ defines the inner product; real-time QM is reconstructed uniquely by continuation. **Closest prior art.** | KNOWN |
| Nelson 1973 (Markov fields) | Markov property + reflection gives the OS structure for Euclidean fields | KNOWN |
| Schwinger 1961 (closed time path) | Expectations as forward branch glued to backward branch: the "fold" | KNOWN |
| Hartle & Hawking 1983 | Wave function as half a Euclidean path integral; gluing two mirror halves gives \|Ψ\|² | KNOWN |
| Aharonov, Bergmann & Lebowitz 1964; Aharonov, Albert & Vaidman 1988; Aharonov & Vaidman 1990 | Two-state vector: independent forward and backward states; weak values; Born rule when the post-selection is trivial | KNOWN |
| Zambrini 1986; Nagasawa 1989 | Bernstein / Schrödinger processes: ρ = φ̂φ as Euclidean QM; continuation to real time | KNOWN |
| Pavon 1995 | Real-time Nelson process as a saddle, not a minimum | KNOWN |
| Chen, Georgiou & Pavon 2016, 2021 | Bridges as stochastic control; symmetric forward/backward (Fortet–Sinkhorn) structure | KNOWN |
| Cramer 1986 (transactional) | Offer wave ψ times confirmation wave ψ* = Born; ψ* is posited as the advanced wave | KNOWN; the conjugate is assumed |
| Wharton 2007; Price 2012; Leifer & Pusey 2017; Wharton & Argaman 2020 | Time-symmetric and retrocausal readings; time symmetry plus certain assumptions imply retrocausality | KNOWN; interpretive |
| Lamperti 1958; Aaronson 2004 (arXiv) | Only the 1- and 2-norms allow nontrivial norm-preserving linear dynamics; only p = 2 is two-way | KNOWN |
| Schnakenberg 1976 | Detailed balance ⇔ zero entropy production | KNOWN |
| Wigner 1932 (Göttinger Nachrichten, no DOI) | Time reversal in QM is antilinear (complex conjugation) | KNOWN |

## 8. Claim map

| Claim | Label | Check |
|---|---|---|
| Symmetric looks + reversible reference ⇒ mirror pair | PROVED (in-model); KNOWN in substance | M1a |
| Mirror + real records + continuation ⇒ conjugate pair, Born density | PROVED (in-model); KNOWN (OS) | M1b |
| Asymmetric looks ⇒ two-state weak density | PROVED (in-model); KNOWN (ABL) | M1c |
| General data / flux needs the antilinear mirror | PROVED (in-model); KNOWN (Wigner) | M1d–e |
| Reflection positivity ⇔ detailed balance ⇔ zero entropy production | **KNOWN** [REVIEWER EDIT 2026-11-23: relabeled; Kolmogorov 1936, Kelly 1979, Klein–Landau 1981, Schnakenberg 1976] | M2 |
| Positive net learning rate ⇒ no mirror on the joint path measure | KNOWN (Horowitz–Esposito 2014: information flow vanishes when all currents do) + Prop H; heat floor not needed; only the GTAO wording is new to the repo [REVIEWER EDIT 2026-11-23] | M2 + `CORE.md:70` |
| "Information about an outside world costs exactly the mirror" | SPECULATION; one-way only (learning ⇒ no mirror; the converse fails, R3 case C); refers to the tracker's physical Markov law, not to a quantum Euclidean measure [REVIEWER EDIT 2026-11-23] | n/a |
| Two-way continuous mixing ⇒ 2-norm ⇒ conj backward factor over ℂ | KNOWN | M3 |
| A real cost's minimum in real time is a conjugate pair | FAILED-AT-STEP "minimum" | WALLS C1 |
| GTAO fixes α or another physical dimensionless constant | No route found | M4, §6 |
| Nested-layer fixed point gives a universal GTAO number | CONJECTURE, untested | n/a |

## 9. Most promising next step

**Currents inside a mirror-symmetric whole (CONJECTURE, testable on small lattices).** A classical reversible (detailed-balance) universe has zero net current everywhere (KNOWN), so it can contain no tracker with a positive net learning rate (§4). Quantum systems can carry persistent currents and still have an antilinear-reflection-positive Euclidean structure (M1e).

Conjecture: a closed whole that keeps the mirror globally (zero net heat) while some parts carry net flow (trackers that pay heat locally) cannot be a positive reversible Markov path measure. The smallest extension that keeps the mirror is the antilinear one, which supplies the complex conjugate.

If that holds, "trackers inside a closed whole" would force the antilinear mirror in the same way that "two-way continuous change" forces the 2-norm. That would be the piece GTAO adds. Plan:
1. A Page–Wootters-style clock + tracker + world on a lattice.
2. Check whether any positive, reflection-positive path measure reproduces the tracker's local net flow.
3. Check whether the antilinear one does.

Preregister before running. Odds are moderate-to-low: it may reduce to the known fact that time-reversal-odd observables need a complex structure.

**[REVIEWER EDIT 2026-11-23]** **Assessment of this next step (see `MIRROR_REVIEW.md` §4; checks R4a–c).** (i) "A classical reversible whole cannot host a stationary net-flow tracker" is immediate from Proposition H plus the fact that information flow is a current-weighted sum (KNOWN; Horowitz–Esposito 2014). (ii) "The smallest extension that keeps the mirror is the antilinear one" does **not** hold at the level of one closed whole: the flux ring (persistent current, positive antilinear OS form) is reproduced exactly by the real symmetric H_R = [[Re H, −Im H], [Im H, Re H]] on a doubled real space with a **real-linear** mirror (R4c: same current −0.1706, OS form min eig 0.0168 > 0). Complex time reversal becomes a linear flip of one extra real switch (Stueckelberg 1960; McKague–Mosca–Gisin 2009). (iii) A classical velocity-flip mirror (generalized detailed balance, Graham–Haken 1971) carries phase-space currents but is not positive (R4a: odd witness −0.449). So what a positive mirror with currents forces is leaving positive Markov kernels, i.e. the OS Hilbert structure (KNOWN), not ℂ over ℝ. Real versus complex needs a composition / local-tomography input (Hardy 2001 axiom 4; Renou et al. 2021), which is the WALLS tracker-contest door. **Recommendation:** do not run this as a separate simulation. Fold the one open part (does ruin-free tracking cost force local tomography of composites?) into the multi-direction tracker contest, with R4a and R4c as preregistered controls. Label for the conjecture as written: CONJECTURE, expected to reduce to KNOWN.

## 10. For Chad (plain words, audio)

**[REVIEWER EDIT 2026-11-23]** The original paragraph overstated two things (the conjugate is built in by the real, time-symmetric setup; the heat link is one-way and known). Revised:

You were right that the two times are one mirror. If the cheapest two-look judgment has to stay the same when you swap the past look and the future look, the backward half comes out as the mirror image of the forward half. Turn imaginary time into real time, and that mirror becomes the complex conjugate. So a wave times its conjugate is what a time mirror looks like after the turn. But to be straight with you, that step works because we started from a real, time-symmetric setup, so the conjugate was already built in. It's the known 1973 bridge between the two kinds of time. That's solid ground, but not a new door. The heat link is known math too: anything that learns about an outside world makes heat and can't keep the mirror. It only runs one way, though, because plenty of things lose the mirror without learning anything. I also checked the proposed next step, trackers inside a mirror-symmetric whole, and it doesn't force complex numbers. A real-number version with one extra hidden switch does the same job, which has been known since 1960. What separates real from complex is how parts combine, and that's the tracker contest we're already running, so the push goes there. On the 1/137 idea, there's still nothing. Simple formulas hit it by luck about as often as chance predicts.

*Original paragraph, kept for the record:* You were right: the two times really are one mirror. If you ask the cheapest two-look judgment to stay the same when you swap the past look and the future look, the backward half comes out as the exact mirror image of the forward half. When you turn imaginary time into real time, that mirror becomes the complex conjugate. So "wave times its conjugate" is just what a time mirror looks like after the turn. That's a known result from 1973, called reflection positivity, and it's the standard bridge between the two kinds of time. So it's solid ground, not a new door. When the two looks are different, you get Aharonov's two-state picture, with strange complex in-between values. The ordinary quantum rule is the case where the second look is the system's own record, with no outside world. The new piece for us is this: the mirror exists exactly when a system makes zero net heat. Anything that tracks an outside world makes heat, so it loses the mirror. In our terms, knowing an outside world costs you the mirror. What's still not explained is why time gets turned at all, the "i." On your ratio idea, I found nothing. Our pure numbers are shape factors, not couplings like the 1/137 constant, and a quick test shows that simple formulas hit 137.036 by luck many times over. The best next step is to test whether trackers living inside a mirror-symmetric whole force the complex conjugate. If they do, that part would be ours.

## 11. Checks and references

- `checks/m1_mirror_bridge.py/.out`: mirror pair, Schwarz reflection, Born density, two-state density, antilinear mirror, flux ring.
- `checks/m2_rp_vs_heat.py/.out`: reflection positivity vs entropy production; complex witness.
- `checks/m3_lp_isometries.py/.out`: isometry Lie-algebra dimensions for ℓ^p; backward factor after summing out the future.
- `checks/m4_numerology.py/.out`: Wyler and Eddington errors; look-elsewhere count.
- `checks/crossref.py`, `dois.txt`, `crossref.out`: 26 OK.

DOIs (all verified on Crossref):
- Osterwalder & Schrader 1973 CMP 31:83, 10.1007/BF01645738; and 1975 CMP 42:281, 10.1007/BF01608978
- Nelson 1973 JFA 12:97, 10.1016/0022-1236(73)90091-8
- Schwinger 1961 JMP 2:407, 10.1063/1.1703727
- Hartle & Hawking 1983 PRD 28:2960, 10.1103/PhysRevD.28.2960
- Aharonov, Bergmann & Lebowitz 1964 Phys. Rev. 134:B1410, 10.1103/PhysRev.134.B1410
- Aharonov, Albert & Vaidman 1988 PRL 60:1351, 10.1103/PhysRevLett.60.1351
- Aharonov & Vaidman 1990 PRA 41:11, 10.1103/PhysRevA.41.11
- Zambrini 1986 JMP 27:2307, 10.1063/1.527002
- Nagasawa 1989 PTRF 82:109, 10.1007/bf00340014
- Pavon 1995 JMP 36:6774, 10.1063/1.531187
- Chen, Georgiou & Pavon 2016 JOTA 169:671, 10.1007/s10957-015-0803-z; and 2021 SIAM Rev. 63:249, 10.1137/20m1339982
- Cramer 1986 RMP 58:647, 10.1103/RevModPhys.58.647
- Wharton 2007 Found. Phys. 37:159, 10.1007/s10701-006-9089-1
- Price 2012 SHPMP 43:75, 10.1016/j.shpsb.2011.12.003
- Leifer & Pusey 2017 Proc. R. Soc. A 473:20160607, 10.1098/rspa.2016.0607
- Wharton & Argaman 2020 RMP 92:021002, 10.1103/RevModPhys.92.021002
- Lamperti 1958 Pacific J. Math. 8:459, 10.2140/pjm.1958.8.459
- Schnakenberg 1976 RMP 48:571, 10.1103/RevModPhys.48.571
- Wallstrom 1994 PRA 49:1613, 10.1103/PhysRevA.49.1613
- Page & Wootters 1983 PRD 27:2885, 10.1103/PhysRevD.27.2885
- Renou et al. 2021 Nature 600:625, 10.1038/s41586-021-04160-4
- Feigenbaum 1978 J. Stat. Phys. 19:25, 10.1007/BF01020332
- Eddington 1929 Proc. R. Soc. A 122:358, 10.1098/rspa.1929.0025
- Smolin 1992 CQG 9:173, 10.1088/0264-9381/9/1/016 (cosmological selection of constants; cited as the known "selection fixes constants" route, not used)

No DOI: Aaronson 2004, arXiv quant-ph/0401062 (not read this pass) · Wigner 1932, Göttinger Nachrichten (not read; standard statement) · Wyler 1969, C. R. Acad. Sci. Paris (formula only) · CODATA 2022 α⁻¹ from physics.nist.gov (fetched).

**[REVIEWER EDIT 2026-11-23]** Reviewer-added references, all checked on Crossref (`reviews-indep-2026-11-23/mirror_review_checks/crossref_review.out`): Horowitz & Esposito 2014 PRX 4:031015, 10.1103/PhysRevX.4.031015 · Kolmogorov 1936 Math. Ann. 112:155, 10.1007/BF01565412 · Klein & Landau 1981 JFA 42:368, 10.1016/0022-1236(81)90096-3 · Neeb & Ólafsson 2018 *Reflection Positivity* (SpringerBriefs), 10.1007/978-3-319-94755-6 · Guerra & Morato 1983 PRD 27:1774, 10.1103/PhysRevD.27.1774 · Yasue 1981 JFA 41:327, 10.1016/0022-1236(81)90079-3 · Graham & Haken 1971 Z. Phys. 243:289, 10.1007/BF01394858 · McKague, Mosca & Gisin 2009 PRL 102:020505, 10.1103/PhysRevLett.102.020505 · Esposito, Lindenberg & Van den Broeck 2010 NJP 12:013013, 10.1088/1367-2630/12/1/013013. No DOI: Kelly 1979, *Reversibility and Stochastic Networks* (Wiley) · Stueckelberg 1960, Helv. Phys. Acta 33:727 (not read; standard statement). Note: Chen–Georgiou–Pavon JOTA 169 is issued online 2015 on Crossref, print 2016.
