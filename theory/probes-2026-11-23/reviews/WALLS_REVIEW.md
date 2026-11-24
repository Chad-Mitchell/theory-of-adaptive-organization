# Independent hostile review: `walls-2026-11-23/WALLS_MEMO.md` and `checks/`

*Reviewer: independent; I did not write the memo. Monday 23 November 2026, about 8:30–9:30 PM EST. Checked against GTAO `main` `d592662` (fresh clone in `/workspace/revwalls`, TMPDIR there, nice 19, deleted after). THEORY.md untouched, no PR, nothing posted, no real-world data. Labels: PROVED (in-model) / KNOWN / CONJECTURE / SPECULATION. Memo line numbers refer to the memo **after** reviewer edits; there are 19 `[REVIEWER EDIT 2026-11-23]` marks, plus three wording swaps of "solves/solving" to "obeys/obeying" at memo lines 84, 85 and 90. Reviewer checks are in `walls_review_checks/` (hashes in `walls_review_checks/SHA256SUMS`).*

## 0. Summary

| Claim | Result | New or known |
|---|---|---|
| W1 sign: bridge vs real time differ only in the sign of (U+Q); same continuity equation | **PASS.** Re-derived independently with ψ=√ρ e^{iS/λ} and φ,φ̂=√ρ e^{±S/λ} (R1a). | KNOWN (Zambrini 1986; Guerra–Morato 1983; von Renesse 2012). The GTAO wording is new to the repo. |
| W1 "exactly one negative price ⇒ A8 fails" (memo:22–25, `CORE.md:52`) | **PASS with correction.** The flip is a *relative* sign. It can be booked on transport (one price) or on stake + information (two prices). A8 fails somewhere, but the place is not unique (R1c). | KNOWN in substance |
| Two-judge split (memo:17–21, §3.2) | **PASS for the math, FAIL for the interpretation.** See §2. It is a block-wise (partial) optimum of one biconvex function, "pricer optimum = Bohm potential" holds by construction, and the fringes are imported through V = U+Q[ρ_QM]. | KNOWN in substance: a Fenchel-dual rewrite of Pavon 1995. The min–min wording was not found in print but is one line from Pavon. |
| Wallstrom objection stands | **PASS.** | KNOWN |
| Caticha ED closest; GTAO adds nothing (memo §3.3) | **PASS.** | KNOWN |
| λ = iħ reproduces propagator; fails as a cost (Cameron 1960) (memo §3.4) | **PASS.** C3 reruns identically (errors ~1e−12; conjugate-time sign change between T=3.14 and 3.15). | KNOWN (Mehler; Cameron 1960; Jacobi) |
| W2: one universal price from composite-body consistency (C5b) | **PASS (elementary), with caveats.** It needs independent constituent noise, and going from "m·D(m) constant on rationals" to the reals needs a regularity assumption. It is the standard Nelson-type consistency argument and should be credited as such. | KNOWN in substance |
| W2: value of ħ is a units question (SI 2019); α untouched | **PASS** | KNOWN |
| W2: Adler trace dynamics as "set by the layer below" | **PASS as stated** (the memo says the book was not read; I did not read it either) | KNOWN |
| W3: clock–system **mutual** information = S(time-averaged state) (memo:27, §5) | **FAIL (factor 2), fixed.** Boette et al. 2016 eq. 16 gives *entanglement entropy* E(S,T)=S(ρ_S), with ρ_S = (1/N)Σ_t |ψ_t⟩⟨ψ_t|. Mutual information is 2S(ρ̄) (R2a: 2.1555 = 2×1.0778). C4b computed entanglement entropy. | KNOWN |
| C4c: closed classical ring changes only by permutations | **PASS with correction.** Periodic (block-cyclic) non-permutation chains also change, but only through class weights, i.e. as permutations after coarse-graining (R2b). | KNOWN (this is Hardy's own motivation) |
| W1 = W3 "same wall" | **PASS as a framing.** It is the probabilities-vs-amplitudes question, which is Hardy's continuity point. | KNOWN |
| Record counts N_R = K(K+1)/2, N_C = K², N_H = K(2K−1); only ℂ multiplicative | **PASS.** Explicit basis counting agrees (R2c); 2×2: 10 vs 9, 16 vs 16, 28 vs 36. | KNOWN (Hardy–Wootters 2012; Barnum–Wilce 2014) |
| Hardy 2001 quotes verbatim | **PASS.** Axiom 2: "where, for each given N, K takes the minimum value consistent with the axioms"; Axiom 5: "There exists a continuous reversible transformation on a system between any two pure states of that system"; abstract: "If Axiom 5 (or even just the word 'continuous' from Axiom 5) is dropped then we obtain classical probability theory instead" (`walls_review_checks/hardy_quotes.txt`, from arXiv quant-ph/0101012v4). **Missing from memo:** Axiom 4 is "N = N_A N_B and K = K_A K_B", so local tomography is an *axiom* in Hardy. | KNOWN |
| Removing "continuous" gives classical | **PASS** (Hardy's claim, given Axiom 2). One caveat in the philosophy literature (EJPS 2024, doi 10.1007/s13194-024-00581-w): it depends on the simplicity axiom. | KNOWN |
| Page–Wootters / Boette | **PASS** after the factor-2 fix | KNOWN |
| DOIs | **PASS.** All 41 memo DOIs resolve on Crossref with matching author, year and venue (`crossref_memo_rerun.out`). The 6 reviewer-added DOIs also resolve (`crossref_review.out`); the Zenodo DOI resolves on DataCite. | — |
| C1–C5 reproducibility | **PASS.** Fresh copy, nice 19. All five `.out` files are byte-identical and all 14 hashes match (`rerun_c1_c5.txt`). | — |
| Door (Hardy + GTAO forcing Axiom 5 and local tomography) | **CONJECTURE. Plausible as a question, mostly not new, likely to stop at step (ii).** See §4. | Mostly KNOWN; narrow GTAO piece not found in print |

## 1. W1 sign (independent re-derivation)

`walls_review_checks/r1_sign_and_tautology.py` (sympy). Real-time: substituting ψ=√ρ e^{iS/λ} and splitting real and imaginary parts with real symbols gives continuity ∂ρ/∂t + ∂x(ρS_x/m) = 0 and S_t + S_x²/2m **+** (U+Q_λ) = 0, with residual 0. Bridge: φ=√ρ e^{S/λ} backward and φ̂=√ρ e^{−S/λ} forward give the same continuity equation and S_t + S_x²/2m **−** (U+Q_λ) = 0, with residual 0. This matches C2 (memo:22–25, §3.1).

Correction (R1c): stationary points of ∫(K − J) and ∫(J − K) coincide. What flips is the *relative* sign between transport K and J = stake + information. In GTAO's priced sum (`CORE.md:52`) J contains two priced terms, so "exactly one price is negative" is true only if the negative is put on transport. Memo edited at line 25.

## 2. Two-judge claim: what it is

Let \(G(\rho,j,\phi)=\iint\big[j^2/2\rho-(U+\phi)\rho\big]+\int\Lambda(\phi)\,dt\), with Λ(φ) the top eigenvalue of (λ²/2m)Δ + φ.
- **Mover:** min over (ρ,j) of G at fixed φ. This is the memo's M plus a constant. It is convex (a perspective function plus a linear term).
- **Pricer:** min over φ of G at fixed ρ. This is Λ(φ) − ⟨φ,ρ⟩, convex in φ because Λ is convex.
- By Donsker–Varadhan, min_φ G = A_R(ρ,j) = ∫∫ K − F − Uρ, the real-time action.

Findings:
1. **"Pricer optimum = Bohm potential" holds by construction.** The argmax in a Legendre transform is the gradient of the transformed function, and δF/δρ = Q_λ exactly (R1b: residual 0). The only non-trivial input is that the Fisher term is convex, so F = F**. KNOWN (Donsker–Varadhan 1975; Reginatto 1998).
2. **"Mover's global min" is a best response.** It is the global minimum of a convex subproblem with φ held at Q[ρ_QM], and its stationarity condition is the quantum Euler equation. This holds for *any* smooth classical fluid in a fixed potential (Benamou–Brenier convexity). The identity M′ − M = quad + ∫A·(Euler) is correct, and C1(b) confirms it numerically.
3. **Both judges minimize the same G.** Real time is a *partial optimum* of a biconvex function (terminology: Gorski–Pfeuffer–Klamroth 2007), not a joint minimum. Because G(ρ,j,Q[ρ]) = A_R(ρ,j), the 280/400 descent directions in C1(c) are descent directions of G, and G is unbounded below. "Person-by-person optimal, not team-optimal" (memo §3.2) is accurate.
4. **Fringes are imported.** The mover's minimizer has fringes only because V = U + Q[ρ_QM] already encodes them. That is a fixed-point property, not interference produced by minimization. INVERT_REVIEW §2 ("positive reweightings cannot interfere") therefore stands for any single cost. Memo bottom line 2 retitled.
5. **Prior art.** Pavon 1995 (abstract and §4 checked): Nelson's process is the saddle-point equilibrium of a zero-sum game. "The first player chooses the control v so as to minimize the action… The second player chooses the control u so as to minimize minus the action." Fenchel-dualizing Pavon's concave osmotic part turns his min–max into the memo's min–min. Status: **KNOWN in substance**. The min–min/biconvex presentation was not found in print, but I would not claim it as new.
6. **Numerics.** C1(a)'s pointwise residual (max 0.80) is a stencil artifact *everywhere*, not only at the window edge. A closed-form ∂x(w²/2+U+Q) built from spectral derivatives of ψ gives a max of 2.7e−8 in the window (R3a). Fringe support is thin: of the times touched by the perturbations, 49% have ≥2 interior maxima and 6% have ≥3 (R3b). This does not affect the analytic identity.

Label: the elementary facts are **PROVED (in-model, ρ>0)**. The physics reading is **KNOWN**. "Minima can interfere" is withdrawn.

## 3. W2, W3 details

- **C5b.** The argument shows D(Nm)·Nm = D(m)·m for integer N. This gives m·D(m) constant on positive rationals. Extending it to the reals needs a regularity assumption such as continuity or monotonicity. It also assumes independent constituent noises; correlated noise breaks it. The C5b Monte Carlo only checks D_com = D/N, which is a textbook fact. Status: elementary and KNOWN in substance (Nelson-type composite consistency). It is fine to keep, credited.
- **W3.** Factor 2 fixed (memo:27, §5). Gambini–Porto–Pullin and the speed-limit links are fine.

## 4. The door: honest assessment

**What is verified.** Hardy's axioms are quoted correctly, and the "drop *continuous* ⇒ classical" claim is Hardy's own.

**What the memo missed.**
1. **Step (iii) re-derives an axiom Hardy already assumes.** Local tomography (K = K_A K_B) is Hardy's Axiom 4. Complex numbers then follow from K = N^r with the smallest r (Axiom 2) and Axiom 5. Also, T44 (`theory/BOUNDARY_SUFFICIENCY_2026-11-22.md:39,45`) is a conditional-independence (screening) result for a Markov field, not a count of state parameters. It does not imply K_AB = K_A K_B, and tracking wholes through parts might as easily argue against holistic parameters as for any particular count.
2. **Step (i) holds only for the whole universe.** A closed universe has no outside bath, but any subsystem can dump heat into the rest. Hardy's Axiom 5 is needed for every system, so (i) does not deliver it.
3. **Step (ii) must exclude classical mechanics.** A continuous phase space with Liouville flow is a continuous reversible tracker. Hardy's continuity separates classical from quantum only at **finite N**, so (ii) needs a finite-capacity premise. GTAO might supply one, since a price per nat makes unbounded records cost unboundedly much (compare the record caps in `theory/BARRIER_MASS_FIELD_THEORY_2026-11-23.md:18`).
4. **Cost headwind.** At equal readable information (ln N; Holevo cap) a quantum record has K = N² parameters against N classically (R2d). A cost per nat of record dimension, which is the memo's own pricing (memo §6), therefore *favors classical* unless the tracking-lag/ruin term pays for at least ln N extra nats.
5. **Prior art on the motivation.** Continuity motivated by continuous time and tracking already appears in Höhn 2017 (Quantum 1:38, Rule 4: the catalogue of knowledge "evolves continuously in time in-between interrogations"; he notes the classical bit fails it), in Masanes–Müller–Augusiak–Pérez-García 2013 (PNAS 110:16373, Postulate 1), and in Dakić–Brukner 2011 (Axiom 3′). The phrase itself: Brooke 2026 (Zenodo 10.5281/zenodo.19908706, not refereed), "Quantum Structure as Least-Cost Admissible Bookkeeping". Chiribella–D'Ariano–Perinotti 2011 and Masanes–Müller 2011 are already credited. A quick search found nothing that derives continuity *from ruin-free tracking cost*.

**Assessment.** Plausible as a research question. Novelty is limited to one narrow step: deriving finite capacity plus continuity from GTAO's cost and ruin cap. Most likely to stop at **step (ii)**, either because a discrete or classical-continuous tracker matches the cost, or because the K = N² headwind cannot be paid. If it does stop there, the result is still a clean map entry rather than a loss.

## 5. The one next derivation I would run

**A finite-capacity tracking duel, with a preregistered criterion.** A world drifts continuously on a circle (a rotor phase, constant or diffusive rate). Compare three trackers at equal readable information ln N under the GTAO cost (price λ per nat of record dimension, stake on phase error, ruin cap on error excursions):
- (a) an N-state reversible permutation tracker;
- (b) an N-level quantum tracker with continuous unitaries and optimal covariant measurement;
- (c) a classical continuous-phase tracker whose resolution is priced the same way.

Step (ii) survives only if (b) beats both (a) and (c) after paying K = N² against N. Write down in advance what counts as a tie. This tests the door's weakest step directly, and it can be done in closed form or in a small numerical model.

## 6. Revised plain-words paragraph for Chad (audio)

You were right that "walls" was the wrong picture. The three turned out to be one question: are nature's deepest records plain odds, or arrows that can point different ways and cancel? Plain odds give the imaginary-time version, where cheapest-path reasoning works. Arrows give real time and interference. Real time does come out as a standoff between two judges, one moving things and one pricing where things are. That part checks out, but it's a 1995 result in new clothes, and the interference only shows up because each judge is reacting to the other. No single cost produces it. Your "time comes from the layer below" idea is real physics from 1983: time is read off an internal clock, and with no outside world, the information term we thought was missing comes back as the link between the clock and everything else. For Planck's constant, its number is now a units choice. "One price for everything" does follow from asking that bigger things obey the same rule as smaller ones. The best remaining door is a 2001 result by Lucien Hardy: quantum theory uses the fewest numbers that still let things change smoothly. Others have built on that idea, so the door isn't new. The one piece that might be ours is showing that smooth change is forced by tracking a changing world without going broke. My honest odds are low. The likely sticking point is that ordinary smooth physics also changes smoothly, and quantum records carry more numbers for the same readable information. Still, that's the one derivation worth running next.

## 7. Files

- `walls_review_checks/r1_sign_and_tautology.py/.out`: W1 sign re-derivation, δF/δρ = Q, relative-sign note.
- `walls_review_checks/r2_clock_records.py/.out`: I(C:S) = 2S(ρ̄); block-cyclic closure; record counts; Holevo vs K.
- `walls_review_checks/r3_c1_numerics.py/.out`: C1 Euler residual without a stencil; fringe support.
- `walls_review_checks/rerun_c1_c5.txt`, `crossref_memo_rerun.out`, `crossref_review.out`, `dois_review.txt`, `crossref_review.py`, `hardy_quant-ph_0101012v4.txt`, `hardy_quotes.txt`.
