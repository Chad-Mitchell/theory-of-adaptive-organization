# Preregistration: third QM-selection search (SU(3), Sp(2), G₂ up to dimension 15; U(2), Sp(1)², Sp(1)³ and G × Sp(1)ᵏ in dimensions 9–15), amended after a failed gate read

*Thursday 26 November 2026, written 05:56–06:15 ET, §0.10 and §8 added 06:47–07:00 ET (America/New_York). Branch `forge-rnd-record-cost-2` (PR #295). This file, `search_qmsel3.py`, `list.out` and `toy_tests.py` are hashed in `PREREG.sha256` in one lock commit (the renewed lock, §0.10), which is **pushed before any scored run**. Results go append-only in `RESULTS.md`; changes to this file go in `DEVIATIONS.md` and never edit it. `THEORY.md`, `CORE.md` and locked blobs are not touched. It implements amendments A1–A10 of the gate read of the previous lock (session file `GATE_READ_qmsel2.md`, 05:45–05:55 ET).*

Labels: **PROVED (in-model)**, **OBSERVED (numerical)**, **KNOWN**, **HYPOTHESIS**, **OPEN**, **open miss**. Every claim below carries one.

## 0. History, blind protocol and prior knowledge (read this first)

1. **The previous lock failed its gate.** `theory/qm-selection-2-2026-11-26/` (lock commit `641c695`, on GitHub at 05:44:41 ET) was gate-read by a separate reader at 05:45–05:55 ET. Decision: **FAIL on method, not on integrity**: hashes matched, the lock was pushed before any run, and no run exists. The hit path was under-tested in the false-HIT direction (non-exposed faces, bit faces, capacity witness), one scope list was incomplete, and one pre-lock change was not disclosed. That directory stays exactly as committed and is **never run**; this directory supersedes it. Amendments A1–A10 are mapped to sections in §7.
2. **No development run on the new groups, before either lock.** The only pre-lock runs of this script are:
   - `--selftest`: construction checks of every representation (bracket closure and antisymmetry only), and the five SO(3) controls whose outcomes are published in `../qm-selection-2026-11-26/RESULTS.md` (B3, Z3, C1, Z2, B3 × B3), plus a bit-face check on B3 and Z2. Output: `selftest.out`. No orbit, capacity or face of an SU(3), Sp(2) or G₂ body was computed.
   - `--list`: the enumeration only (index, name, group, dimension). Output: `list.out`, committed and checked at run time (§4.9).
3. **Changes made before the previous lock, after seeing control output (all disclosed; none used new-group output).** Five bugs found by the selftest: a sign-power error in the real spin basis; a relative tolerance that misread the stabilizer rank; orbit samples that stayed near the identity (so Z3 got capacity bound 3 instead of 2); a capacity witness that could not find orthogonal pairs in real QM; and a bit-face routine that used an unchecked normal. **A sixth change (A9):** an earlier selftest output (03:24:54 ET, before the 03:57 version of the script) scored the B3 control as `"jordan_type": "ball B3 (spin factor)"`, `"outcome": "TIE (P6 bit-face clause holds)"`. Between 03:24 and 03:57 ET complex QM₂ was added to the Jordan table (correct: the Bloch ball is complex QM₂), and B3 became `complex QM` / `TARGET`. That change altered a control's scored label after the author saw it. In this lock the TARGET label is in addition limited to named CP^{N−1} orbits (§4.6).
4. **Changes made for this lock** (from the gate read only, before any run): A1–A7 in the script and A8–A10 in this file (§7). The selftest was re-run on the five SO(3) controls after these changes (`selftest.out`). **One further change after seeing that selftest output (disclosed):** the first v3 selftest (started 05:59 ET) scored the Z2 bit face `undecided` instead of `not ball` (output kept as `selftest_run1.out`; all five control outcomes there match the re-run), because the relative-interior LP was posed as an exact equality in the ambient space while the numerically found face points lie ~10⁻⁴ off their affine hull, which made the LP infeasible. The LP is now posed in the face's affine-hull coordinates (§4.5). The error went in the cautious direction (undecided scores OPEN, not HIT). The selftest was then re-run; `selftest.out` is that re-run.
5. **The lock is pushed before any run.** GitHub's push time of this lock commit anchors the order. `--run` refuses to start unless `PREREG.md` and `search_qmsel3.py` match `PREREG.sha256`, the numpy/scipy/python versions are the pinned ones, and the regenerated enumeration matches `list.out` line for line.
6. **A fresh separate reader passes the Gate (§2) before the run.** The author does not run `--run`. The gate read is committed in this directory (`GATE_READ.md`) before the run.
7. **Prior knowledge.** The author wrote the first search (dimensions 4–8; outcome MISS, a CONSISTENCY_CHECK) and the failed second prereg. For the new groups it has expectations only (§5). It puts about 50% on the SU(3) generic adjoint (flag) orbitope being a TIE.
8. **Seeds and hash.** `SEED = 20261127`. Body *i* uses `numpy.random.default_rng(SEED + i)` in `list.out` order. The capacity-witness recheck uses `SEED + 10⁶ + i`; the selftest controls use `SEED + 1000 + i` and `SEED + 2000 + i`. The result does not depend on the number of worker processes. The script's sha256 is in `PREREG.sha256`.
9. **Run command (locked).** `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 search_qmsel3.py --run --workers=8 > search_qmsel3.out 2>&1`, run from this directory on a machine without other heavy load. Pinned versions: numpy 2.5.5, scipy 1.18.1, python 3.13.5. The output is committed as is, followed by `RESULTS.md`. Wall time per body is printed.
10. **An earlier local lock commit of this directory was never pushed.** Commit `30f345e` (06:08 ET) locked this directory without the toy-input helper tests now required by the process rule in `theory/RECORD_COST_ERRATA_R1316_2026-11-26.md` (appended to the branch at 4741761 while that commit waited for its checks). It was never on GitHub and no `--run` was made from it. This file adds §8 (helper tests on toy inputs and validity checks), `toy_tests.py` and `toy_tests.out`, and the lock is renewed in a later commit (`PREREG.sha256` rewritten in that commit); both commits are in the branch history. `search_qmsel3.py` and `list.out` are unchanged from `30f345e` (same hashes).

## 1. Premises (frozen, unchanged)

The premise list P1–P8 is the one frozen in `../qm-selection-2026-11-26/PREREG.md` §1, as read with that directory's `DEVIATIONS.md`: P4 (group rule: reversible maps form G₀, the identity component of the affine symmetry group) was new at that lock and chosen after C1 and the O(3) point; P4 + P2 ⇒ P3 (a compact connected group acting transitively on two or more points has positive dimension), so U enters through P4. **P7 (Jordan) is dropped** for this search. The question: **do P1–P6 select complex quantum theory without P7 for these groups and dimensions?** A miss would show at most that P7 is not needed *given P5 (hSFP)*, which was itself introduced after C1.

## 2. Gate (G1–G5); label: TEST

- **G1. Hit rule (applies to every body, Jordan or not, except complex QM itself).**
  - N_LB ≤ N ≤ N_UB are the capacity bounds of §4.3, d the affine dimension.
  - **HIT:** d < N_LB² − 1; the g₀ closure check passes (§4.1); P1–P5 hold under P4 (SFP passes; the torus-fixed points match the Weyl orbit; no re-confirmed hSFP failure certificate at depth 1); the capacity witness passes the fresh-sample recheck (§4.3); and P6's bit-face clause holds for every tested pair (§4.5). A HIT is reported as **conditional on faces of exposure depth ≥ 2, which are untested** (A1, §4.4).
  - **TIE:** N_LB = N_UB = N, d = N² − 1, and the rest as for HIT. A tie counts as a hit: the cost does not separate the body from complex QM.
  - **TARGET:** the body is one of the named CP^{N−1} orbits (§4.6) and passes the recheck. Not a hit. A body with complex QM's signature that is not a named CP^{N−1} orbit is **OPEN (TARGET-signature, check by hand)** (A5).
  - **MISS:** SFP fails, or a re-confirmed hSFP failure certificate is found, or d > N_UB² − 1, or some tested bit face is decided not to be a 3-ball (A2).
  - **OPEN:** anything else: g₀ closure fails (A6); torus-fixed points do not match the Weyl orbit (A4); capacity interval straddles the threshold; the witness fails the recheck (A3); some bit face undecided (A2); TARGET-signature (A5); no upper bound; or time budget.
  - **OPEN bodies settled later (A10).** Any OPEN body that is settled after this run (by hand, by a rerun, or by another script) is a **new, unregistered result**. It is not a hit or a miss of this prereg and does not change this prereg's overall result.
  - **Overall:** HIT if any body is HIT or TIE; else INCONCLUSIVE if any body is OPEN; else MISS.
  - **Non-complex Jordan bodies** (real QM, balls B_n, quaternionic QM₃) are scored by the same rule, so a cheaper or equal one would count as a hit for "P1–P6 select complex QM". Expected: they all lose (§5).
  - **Primary score uses all of P6, including the clause "every bit face is the cheapest bit".** A secondary count without that clause (dimension only) is printed beside it. If the primary result is MISS and the secondary has a HIT or TIE, the result says so, and records that the bit-face clause is doing the selection.
  - Honest odds of an overall HIT (counting a TIE): about 0.5, mostly from the SU(3) flag body.
- **G2. Not an identity.** The outcome is a numerical classification over a locked family. It is not fixed by a theorem the author has; the flag-body case in particular is not known to the author. Label: **TEST**.
- **G3. Rival.** "P7 is needed": outside the Jordan class P1–P6 admit a body at least as cheap as complex QM. It predicts a HIT or TIE, most likely the SU(3) flag orbitope (§5).
- **G4. Reach.** Level (a), toy classification, with a route to (b) (a general classification of hSFP orbitopes).
- **G5. Next step.** HIT/TIE: log the body as a counterexample to "P1–P6 select complex QM" (OBSERVED (numerical), conditional on depth-≥2 faces, until an exact proof of its capacity, hSFP and faces), keep P7 load-bearing, and say so in the PR body. MISS: P7 is not needed given P5, at depth 1, for these groups and dimensions on the locked grid. Next: the rank-3 groups in range, which this search does not cover (§3.4: SU(4) adjoint, Sp(3) on 14, Spin(7) on 8), the balls B9–B15 outside the listed products, products of two rank-2 groups, and dimensions 16–24. INCONCLUSIVE: report the OPEN bodies; no claim either way (A10).

## 3. Candidates and the reduction (locked)

1. **Reduction to zero weights (PROVED (in-model)).** Let G be connected compact, acting linearly, K = conv(G·v), and G₀ ⊇ G the identity component of K's symmetry group. If K has SFP under G₀, a maximal torus T₀ of G₀ fixes a pure state p. A maximal torus T of G lies in some maximal torus of G₀, which is gT₀g⁻¹ for some g ∈ G₀ (maximal tori of a compact connected group are conjugate; Hopf–Samelson 1940, `10.1007/BF01378063`). So T fixes g·p. Since G is transitive on the pure states, g·p = h·v with h ∈ G, and h⁻¹Th fixes v. So **v may be taken in the zero-weight space Z of T**.
2. **Amplitudes do not matter (PROVED (in-model)).** Rescaling one irreducible summand by a non-zero real number is a G-equivariant invertible linear map, hence an affine isomorphism of orbitopes. So the relative amplitudes and signs of distinct summands are irrelevant. A summand repeated m times reduces to min(m, dim Zᵢ) copies. Within this range every irreducible with a zero weight has dim Zᵢ ≤ 2, and every repeated sum with dim Zᵢ = 2 exceeds dimension 15, so each type appears once. The only real parameter is the direction of v inside a summand with dim Zᵢ = 2.
3. **Representations (KNOWN; zero-weight dimensions confirmed by `--list`).** Real irreducibles of dimension ≤ 15, with dim Z:
   - SU(3): adjoint 8 (dim Z = 2); C³ as R⁶ (0); Sym²C³ as R¹² (0). Larger ones exceed 15. Adjoint ⊕ trivial is the same body (a translation).
   - Sp(2) (acting through SO(5) where Z ≠ 0): 5 (1), 10 = Λ²5 (2), 14 = Sym²₀5 (2, contains real QM d = 14); the spin 4 = H² as R⁸ (0). 5 ⊕ 5 reduces to 5 (dim Z = 1).
   - G₂: 7 (1); 14 adjoint (2). 7 ⊕ 7 reduces to 7.
   - SO(3) (image of U(2), and of Sp(1) where Z ≠ 0): spin j, dimension 2j + 1, dim Z = 1. Half-integer spins have no zero weight.
   - SO(3)ᵏ: types (j₁, …, j_k), dimension ∏(2jᵢ + 1), dim Z = 1.
4. **The enumeration (927 bodies; every index and name in `list.out`).** Sums of distinct types, affine dimension d as stated:
   - SU(3): 8, angle grid plus Weyl-singular directions (120 + 6 bodies).
   - Sp(2): 5 (1); 10 (120 + 8); 14 (120 + 6); 5 ⊕ 10 at d = 15 (120 + 8).
   - G₂: 7 (1); 14 (120 + 12).
   - U(2) → SO(3), d = 9–15: spins {4}, {5}, {6}, {7}, {1,3}, {1,4}, {1,5}, {2,3}, {2,4}, {1,2,3} (10 bodies).
   - Sp(1)² → SO(3)², d = 9–15, both factors acting: 34 bodies, including (1,1) at d = 9 and the products B3 × Zj.
   - Sp(1)³ → SO(3)³, d = 9–15, all factors acting: 35 bodies, including B3³ at d = 9.
   - Products G × Sp(1)ᵏ (k = 1, 2, 3; G = SU(3), Sp(2), G₂) as external sums, d ≤ 15, with the rank-2 factor on a coarser 15° grid plus its Weyl-singular directions: 205 bodies. Plus Sp(2) × Sp(1) on the tensor product 5 ⊗ 3 (d = 15, 1 body), the only irreducible tensor type in range.
   - **Not covered (stated, not hidden; A8).** Each can contain a HIT or TIE that this search cannot see:
     - **rank-3 groups in range:** SU(4) ≅ Spin(6) adjoint (d = 15, dim Z = 3; contains complex QM₄ and the N = 4 analogue of the predicted flag tie); Sp(3) on the 14 (traceless quaternionic Hermitian 3 × 3 matrices; d = 14, dim Z = 2; contains quaternionic QM₃, and a generic direction with capacity 4 would be a strict hit, 14 < 15); Spin(7) on 8 (a ball, B8);
     - **the balls B9–B15** (SO(n) on Rⁿ) outside the products listed;
     - products of two rank-2 groups (for example SO(5) × SO(5) on 5 ⊕ 5); Sp(1)ᵏ with k ≥ 4 (11 bodies in dimensions 9–15); dimensions above 15.
     The rank-3 content above is HYPOTHESIS until a later prereg checks it.
5. **Family coverage.** For a summand with dim Z = 2 the direction of v is u(θ) = cos θ·e₁ + sin θ·e₂, θ = 0°, 3°, …, 357° (full circle; the Weyl group and ±1 make the bodies repeat, and repeats are a consistency check). Inside products the step is 15°. **The Weyl-singular directions are added as separate bodies** (directions where the orbit dimension drops, found from the acting algebra alone by a 0.25° scan of the smallest generic singular value of [X·u(θ)] and a bounded refinement; `--list` finds 6 for SU(3), 8 for Sp(2) 10 and for 5 ⊕ 10, 6 for Sp(2) 14 and 12 for G₂ 14, the counts the root systems predict). They contain the CP² orbit (complex QM₃) and real QM₅. **Coverage is the grid plus these directions.** A HIT or TIE confined to a window narrower than the step can be missed; a MISS is a statement about the listed bodies.

## 4. Method (locked; implemented in `search_qmsel3.py`)

1. **G₀ for every candidate, with a closure check (A6).** In centred coordinates on the affine span, g₀ = the linear vector fields tangent to the orbit at max(60, 4d²) sampled points (null space of the stacked tangency conditions). It contains the acting algebra and can be larger (for example G₂ on 7 gives the ball B7 with G₀ = SO(7)). **Per body**, the basis must close under the bracket (least-squares residual of every [Xᵢ, Xⱼ] outside span g₀) and be antisymmetric, both residuals < 10⁻⁸; otherwise the body is OPEN. dim G₀, rank G₀ and both residuals are printed. All later steps use g₀.
2. **SFP.** rank of the stabilizer algebra of v in g₀ equals rank g₀ (the maximal-torus criterion; PROVED (in-model) for compact connected groups by maximal-torus conjugacy).
3. **Capacity bounds.**
   - **Upper bound (PROVED (in-model), the method is exact as a bound).** Let λ = min e(c) over affine effects e ≥ 0 on K with e(x₀) = 1, c the centroid. If x₁…x_N are perfectly distinguishable by e₁…e_N, then moving each eᵢ by a symmetry taking xᵢ to x₀ (c is G₀-invariant) gives eᵢ(c) ≥ λ, and 1 = Σ eᵢ(c) ≥ Nλ. So N ≤ ⌊1/λ⌋. The LP over a finite set of orbit points is a relaxation, so its minimum α ≤ λ and **N_UB = ⌊1/α + 10⁻⁴⌋ is a valid upper bound whatever the grid** (slack raised from 10⁻⁶, gate note N5). Cutting planes (orbit points where the optimal effect is most negative, by local minimization) only tighten α. With no positive α the body is OPEN.
   - **Lower bound (OBSERVED (numerical)).** The largest N ≤ N_UB with an LP witness on a candidate set: subsets of torus-fixed points, prefixes of greedy sets (repeatedly add the orbit point with least summed inner product), then 100 random grid sets. Positivity is imposed on the grid plus cutting planes. A witness is accepted when every effect's orbit minimum, by local minimization from the 12 lowest grid points, is ≥ −10⁻⁶.
   - **Recheck before any HIT, TIE or TARGET (A3).** The accepted witness effects themselves (not recomputed) are evaluated on 10⁵ fresh orbit points (seed SEED + 10⁶ + i), and each effect is locally minimized over the orbit from its 100 lowest fresh points. The minimum found is printed; if it is below −10⁻⁶ the body is OPEN. A HIT or TIE resting on N_LB stays OBSERVED (numerical) until proved.
4. **hSFP (P5) at exposure depth 1; depth ≥ 2 untested (A1).**
   - A face with a positive-dimensional stabilizer is invariant under a circle, which is conjugate into the maximal torus T. So it is invariant under a subtorus S ⊂ T. Which S matter is decided by which weights vanish on S, so the S are the flats of the weight arrangement. For each flat, a generic H in its annihilator generates S.
   - **Torus-fixed points (A4).** The T-fixed pure states are exactly W·v (PROVED (in-model): if T fixes g·v, then g⁻¹Tg is a maximal torus of the identity component of the stabilizer of v, conjugate there to T, so g ∈ N(T)·Stab(v)). The script builds W·v from root reflections w_α = exp(πK_α) in G₀ (K_α in the real root space, normalised so that ad K_α has eigenvalues 0, ±i on its su(2)). It compares this set with the points found by local optimization from 300 random starts. If they differ, the body is OPEN. The Weyl set is used for the hSFP test.
   - **Failure certificate (OBSERVED (numerical)).** For 24 random S-invariant functionals ℓ, the max of ℓ over the orbit exceeds the max over the S-fixed pure states by more than 10⁻⁶ × radius. The S-fixed pure states are the union of the Z(S)-orbits of the T-fixed points. A gap means the S-invariant face exposed by ℓ has no S-fixed pure state. **Re-confirmation (A4):** a gap is accepted only if it persists when both maxima are recomputed with 5× more starts (30 grid starts for the orbit maximum, 5 starts per Z(S)-orbit for the fixed-point maximum). The threshold is 10⁻⁶ × radius throughout.
   - **Non-exposed faces are not tested (A1).** The minimal exposed face containing an S-invariant face is S-invariant, so every S-invariant exposed face is reached. A face of exposure depth ≥ 2, however, is the maximizer of ℓ₂ over the face exposed by ℓ₁, and in general is not exposed by any single functional. The ℓ₁ + εℓ₂ probe of the previous lock does not reach such faces, and it is dropped. **A pass therefore reads "pass at depth 1", and every HIT or TIE is reported as conditional on faces of exposure depth ≥ 2.** This is a false-HIT direction, stated in G1.
   - "No failure found" is OBSERVED (numerical), not a proof.
5. **P6 bit-face clause on every tested pair (A2).**
   - **Pairs:** every pair of the accepted capacity witness, and every pair of T-fixed points (W·v) that is perfectly distinguishable (a two-outcome witness verified like the capacity witness). This includes one representative of every Weyl-inequivalent distinguishable pair of T-fixed pure states, and repeats are harmless.
   - **The bit face** of a pair p, q is the minimal face of m = (p+q)/2. The script finds the minimal exposed face E of m: its normal is the mean of max(5, d) normal-cone LP vertices, each made valid on the whole orbit by cutting planes; E is the whole body if the normal cone is {0}. E's pure states are local maxima of the normal over the orbit. Then:
     - E is a 3-ball (its pure states span an affine 3-space and lie on an ellipsoid: rms quadric residual < 10⁻³, positive definite; affine dimension counts singular values above 10⁻² of the largest) ⇒ the bit face is E, a 3-ball (every chord midpoint of a ball is interior, so the minimal face of m is all of E);
     - E is not a 3-ball and m is in the relative interior of conv(E's pure states) (LP margin > 10⁻⁶, posed in coordinates of the affine hull of the face points, i.e. the directions with singular value above 10⁻² of the largest; m farther than 10⁻³ × face radius from that hull ⇒ not in the relative interior) ⇒ the bit face is E, **not a ball**;
     - otherwise ⇒ **undecided**.
   - **Scoring:** HIT/TIE only if every tested pair gives a 3-ball. Any non-ball ⇒ MISS. Any undecided, or no pair tested ⇒ OPEN.
   - Controls: B3 gives a 3-ball; real QM₃ (Z2) gives a 2-dim face, not a ball (`selftest.out`).
6. **TARGET only for named CP^{N−1} orbits (A5).** A body has complex QM's signature if (d, N_LB = N_UB, dim G₀, dimension of the pure-state manifold) = (N² − 1, N, N² − 1, 2(N − 1)); the pure-state dimension separates CP² (4) from the SU(3) flag manifold (6), which share (8, 3, 8). It is scored **TARGET only if it is a named CP^{N−1} orbit**: the SU(3) 8 bodies at the six Weyl-singular directions (CP² and its affine image under −1), and the B3 control (CP¹). Any other body with the signature is **OPEN (TARGET-signature, check by hand)**. Real QM, balls and quaternionic QM₃ are tabulated for the printout only; they are scored by G1.
7. **Time budget.** Each body has 3600 s wall clock; a body that runs out is OPEN (time budget). The wall time of every body is printed.
8. **Constants (in the script):**
   - grids and families: N_GRID = 6000 orbit samples; ANG_STEP_DEG = 3; PROD_ANG_STEP_DEG = 15; N_FACTORS = 6 (a random group element is a product of six one-parameter steps);
   - hSFP: N_FUNC = 24; EPS_LIST = (1.0,) (depth 1); FAIL_TOL = 10⁻⁶; CONFIRM_FACTOR = 5;
   - capacity: CUT_ROUNDS = 60; NEG_TOL = 10⁻⁶; UB_SLACK = 10⁻⁴; RECHECK_N = 10⁵; RECHECK_STARTS = 100;
   - other: G0_CLOSURE_TOL = 10⁻⁸; BODY_BUDGET_S = 3600.
9. **Reproducibility (A7).** `--run` aborts unless the numpy, scipy and python versions are 2.5.5, 1.18.1 and 3.13.5. It regenerates the enumeration with a fresh `default_rng(SEED)`, as `--list` does, and aborts unless every line (index, name, group, dimension) equals the committed `list.out`, in order. So neither a different library nor a different enumeration order can be scored. The Weyl-singular angles in the names depend on the generator stream and on the library's linear algebra; that is why they are pinned this way.

## 5. Predeclared expectations (HYPOTHESIS)

- **SU(3) generic adjoint (flag) orbitope: likely TIE**, at about 50%. Its affine dimension is 8 = 3² − 1. Its stabilizer is a maximal torus, so SFP holds. Its capacity is plausibly 3 (the three Weyl-related points diag(a, b, c) permuted). Singular functionals expose faces that may be 3-balls, so hSFP and the bit-face clause may hold. If so, the overall result is HIT (by tie), and P7 (or a new premise) is doing work at N = 3. The direction angles that are Weyl-singular give the CP² orbit = complex QM₃, which is scored TARGET.
- **Jordan cases:**
  - real QM₅ (Sp(2) 14 at its singular direction): fails hSFP (disc faces);
  - B5 (Sp(2) 5) and B7 (G₂ 7, G₀ = SO(7)): capacity 2 and d > 3, MISS on cost;
  - quaternionic QM₃ (d = 14, N = 3) is not reached by these groups; it would lose on cost (14 > 8).
- **Products** are expected to be MISS on cost (dimension adds, capacity does not grow comparably), and SO(3)-only bodies in dimensions 9–15 to be MISS (hSFP or cost), as in dimensions 4–8.
- **Tie handling.** A TIE is scored as a hit (G1). The result then names the body, its angle range, and the exact checks still owed: an exact capacity proof, an exact face classification, and the depth-≥2 faces. It does not call the tie settled.
- **New checks:**
  - the Weyl-orbit count is expected to equal |W(G₀)|/|W(Stab)|: 6 for the SU(3) flag body, 3 for CP²;
  - g₀ closure is expected to pass for every body;
  - the recheck is expected to agree with the grid witness.
  An OPEN from any of these is reported, not explained away (A10).

## 6. Deviations rule

- Before the scored run, any change to the script or this file is a new commit with a `DEVIATIONS.md` line, a new `PREREG.sha256`, and a new push. No `--run` output may be viewed before it.
- A crash during `--run` may be fixed only if the fix touches no scoring constant or rule. It is logged in `DEVIATIONS.md`, re-locked and re-pushed before the rerun, and the crashed partial output is committed as is.
- After the run, nothing in §2–§4 changes. Relabels, if any, are reported beside the script labels and never move a miss to a hit (the forward rule recorded in #292's `DEVIATIONS.md`, applied here too). An OPEN body settled later is a new, unregistered result (A10).

## 7. Amendments A1–A10 of the gate read, and where they are implemented

| # | amendment | here |
|---|---|---|
| A1 | true depth-2 exposure, or declare depth 2 untested | declared untested; ε-probe dropped; pass = "pass at depth 1"; HIT/TIE conditional (§2 G1, §4.4) |
| A2 | bit faces on all witness pairs and Weyl-inequivalent T-fixed pairs; non-ball MISS, undecided OPEN | §4.5, `analyse`, `bit_face_status`, `distinguishable_pair` |
| A3 | witness recheck on ≥ 10⁵ fresh points, ≥ 100 starts, before HIT/TIE | §4.3, `recheck_witness` (also before TARGET) |
| A4 | T-fixed count against Weyl; failures re-confirmed with 5× starts; threshold ≥ 10⁻⁶·rad | §4.4, `root_reflections`, `weyl_orbit`, `hsfp_test` |
| A5 | TARGET only for known CP^{N−1} orbits | §4.6, `Body.known_cp` |
| A6 | per-body g₀ closure check, failure OPEN | §4.1, `g0_closure` |
| A7 | names and order checked against `list.out`; versions pinned | §0.9, §4.9, `check_list`, `check_versions` |
| A8 | scope disclosure: SU(4) adjoint, Sp(3) on 14, Spin(7), B9–B15 | §3.4, §2 G5 |
| A9 | disclose the B3 relabel (03:24 TIE → TARGET) | §0.3 |
| A10 | an OPEN body settled later is a new, unregistered result | §2 G1, §6 |

Gate notes N1–N6: N1 kept (grid windows declared); N2 the singular angles are in `list.out` and their counts match the root systems (6, 8, 6, 8, 12); N3, N4 subsumed by A2, A4; N5 done (slack 10⁻⁴); N6 wall time per body printed.

## 8. Helper tests on toy inputs and validity checks (process rule of 2026-11-26)

`toy_tests.py` tests every helper whose failure could print a scored outcome, on inputs with known answers (toy point sets, SO(2) on the plane, the published SO(3) controls; no SU(3), Sp(2) or G₂ orbit). Output: `toy_tests.out`, **38/38 passed** (OBSERVED (numerical)). A first run (`toy_tests_run1.out`, 36/37) had one failing test, and the fault was in the test: it used an LP witness from 2000 grid points without cutting planes as the "valid" witness, and `recheck_witness` correctly found −1.5 × 10⁻⁴ on fresh points. The test now uses the exact B3 witness and adds the grid-only witness as a case that must be caught. No helper was changed.

| Step | Wrong output it could print | Toy test (expected) | Validity check in the scored run |
|---|---|---|---|
| capacity UB LP | MISS (cost) if too low; lets a HIT through if too high | SO(2) disc α = 1/2; square 1/2; triangle 1/3 | Y ⊂ orbit makes the bound valid whatever the grid (§4.3); controls Z3, B3 × B3 MISS cost |
| capacity witness `effects_lp` | false HIT/TIE | triangle 3 distinguishable; disc: antipodal yes, 90° no, 3 points no | A3 recheck on 10⁵ fresh points; OPEN if < −10⁻⁶ |
| `recheck_witness` | lets a false witness through | exact B3 witness ≈ 0; witness shifted by −0.1 gives −0.100; grid-only LP witness caught (−4 × 10⁻²) | printed minimum per body |
| `g0_closure` | wrong G₀ ⇒ wrong signature | so(4) closes (10⁻¹⁶); 2 of 3 so(3) generators give 0.71 | OPEN if residual > 10⁻⁸ |
| `root_reflections`, `weyl_orbit`, `tfixed_points` | wrong T-fixed set ⇒ false hSFP pass or fail | B3 2, Z2 1, Z3 2, B3 × B3 4; search equals Weyl | OPEN on mismatch (§4.4) |
| `hsfp_test` | false failure ⇒ MISS; missed failure ⇒ false HIT | B3 pass; Z2 fail (gap 1.5) | re-confirmation with 5× starts; controls C1, Z2 |
| `distinguishable_pair` | wrong pair set for bit faces | SO(2): antipodal yes, 90° no | same cutting-plane check as the witness |
| `in_relint` | false "not ball" ⇒ MISS | triangle centroid 1/3; vertex 0; outside, off-hull refused; 10⁻⁵ noise tolerated | undecided ⇒ OPEN, never HIT |
| `face_is_ball` | false "ball" ⇒ HIT | sphere, ellipsoid in R⁶ yes; cube surface, circle, S³ no | all bit faces of a body must pass; controls B3 ball, Z2 not ball |
| `bit_face_status` | as above | SO(2) disc: not ball, dim 2 | as above |
| `jordan_type` | wrong TARGET | complex QM₂, CP² vs flag, real QM₃ | TARGET only for named CP^{N−1} orbits (A5) |
| `check_lock`, `check_list`, `check_versions` | run on changed files or a different enumeration | accept matching; refuse edited PREREG, swapped list order, wrong version | abort before any body |

Launch (process rule, steps 1–6): the run is launched from a fresh clone from GitHub at a commit confirmed by `git ls-remote` to be the branch tip or a descendant of the lock commit; the hashes are verified there; the ls-remote line and the clone path go at the top of the run log.
