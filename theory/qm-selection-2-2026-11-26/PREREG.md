# Preregistration: second QM-selection search (SU(3), Sp(2), G₂ up to dimension 15; U(2), Sp(1)² in dimensions 9–15)

*Thursday 26 November 2026, written 03:30–04:30 ET (America/New_York). Branch `forge-rnd-record-cost-2` (PR #295). This file, `PREREG.sha256` and `search_rank2.py` go in one commit, which is **pushed before any scored run**. Results go append-only in `RESULTS.md`; changes to this file go in `DEVIATIONS.md` and never edit it. `THEORY.md`, `CORE.md` and locked blobs are not touched. It answers §10 of the hostile review of the fix-36 work (session file `HOSTILE_REVIEW_FIX36.md`, items 1–8).*

Labels: **PROVED (in-model)**, **OBSERVED (numerical)**, **KNOWN**, **HYPOTHESIS**, **OPEN**, **open miss**. Every claim below carries one.

## 0. Blind protocol and prior knowledge (read this first)

1. **No development run on these groups.** Before this lock the script was run only in two modes (output committed as `selftest.out` and `list.out`):
   - `--selftest`: construction checks of every representation (the generators close under the bracket and are antisymmetric; no orbit, capacity or face is computed for SU(3), Sp(2) or G₂), and the five SO(3) controls whose outcomes are already published in `../qm-selection-2026-11-26/RESULTS.md` (B3, Z3, C1, Z2, B3 × B3), plus a bit-face check on B3 and Z2. The selftest found five bugs, all fixed before this lock: a sign-power error in the real spin basis; a relative tolerance that misread the stabilizer rank; orbit samples that stayed near the identity (so Z3 got capacity bound 3 instead of 2); the capacity witness that could not find orthogonal pairs in real QM; and a bit-face routine that used an unchecked normal. After the fixes, all five controls give their published outcomes (`selftest.out`). Separately from the bugs, before this lock the enumeration was widened (Weyl-singular directions, products with Sp(1)ᵏ, Sp(1)³) and the amplitude reduction of §3.2 replaced a sign loop; none of this used any output on the new groups.
   - `--list`: the enumeration (names, groups, dimensions, counts). It computes the zero-weight spaces, which are representation-theory facts stated in §3, and no outcome quantity.
2. **The lock is pushed before any run.** GitHub's push time of the lock commit anchors the order. The scored mode refuses to start unless `PREREG.md` and `search_rank2.py` match `PREREG.sha256`.
3. **A separate reader passes the Gate (§2) before the run** (`process/PREREG_GATE.md` §2). The author does not run `--run`. The gate read is committed in this directory (`GATE_READ.md`) before the run.
4. **Prior knowledge, disclosed.** The author wrote the first search (dims 4–8) and saw its outcome (MISS). For this search it has only expectations (§5), not outputs. It expects about 50% that the SU(3) generic adjoint (flag) orbitope is a TIE (§5).
5. **Seeds and hash.** `SEED = 20261127`; body *i* uses `numpy.random.default_rng(SEED + i)` in the enumeration order printed by `--list`; the result does not depend on the number of worker processes. The script's sha256 is in `PREREG.sha256`.
6. **Run command (locked).** `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 search_rank2.py --run --workers=8 > search_rank2.out 2>&1`, run from this directory on a machine without other heavy load. The output is committed as is, followed by `RESULTS.md`. Under heavy box load the final selftest took 24 min instead of about 1 min, and the 3600 s per-body budget (§4.7) is set for an unloaded machine.

## 1. Premises (frozen, unchanged)

The premise list P1–P8 is the one frozen in `../qm-selection-2026-11-26/PREREG.md` §1, as read with that directory's `DEVIATIONS.md`: P4 (group rule: reversible maps form G₀, the identity component of the affine symmetry group) was new at that lock and chosen after C1 and the O(3) point; P4 + P2 ⇒ P3 (a compact connected group acting transitively on two or more points has positive dimension), so U enters through P4. **P7 (Jordan) is dropped** for this search. The question: **do P1–P6 select complex quantum theory without P7 for these groups and dimensions?** A miss would show at most that P7 is not needed *given P5 (hSFP)*, which was itself introduced after C1.

## 2. Gate (G1–G5); label: TEST

- **G1. Hit rule (applies to every body, Jordan or not, except complex QM itself).**
  - N_LB ≤ N ≤ N_UB are the capacity bounds of §4.3, d the affine dimension.
  - **HIT:** d < N_LB² − 1, P1–P5 hold under P4 (SFP passes, no hSFP failure certificate), and P6's bit-face clause holds (§4.5).
  - **TIE:** N_LB = N_UB = N, d = N² − 1, and the rest as for HIT. A tie counts as a hit: the cost does not separate the body from complex QM.
  - **TARGET:** the body is complex QM itself (§4.6). Not a hit.
  - **MISS:** SFP fails, or an hSFP failure certificate is found, or d > N_UB² − 1, or the bit-face clause fails.
  - **OPEN:** anything else (capacity interval straddles the threshold, bit-face check undecided, no upper bound, or time budget).
  - **Overall:** HIT if any body is HIT or TIE; else INCONCLUSIVE if any body is OPEN; else MISS.
  - **Non-complex Jordan bodies** (real QM, balls B_n, quaternionic QM₃) are scored by the same rule, so a cheaper or equal one would count as a hit for "P1–P6 select complex QM". Expected: they all lose (§5).
  - **Primary score uses all of P6, including the clause "every bit face is the cheapest bit".** A secondary count without that clause (dimension only) is printed beside it. If the primary result is MISS and the secondary has a HIT or TIE, the result says so, and records that the bit-face clause is doing the selection.
  - Honest odds of an overall HIT (counting a TIE): about 0.5, mostly from the SU(3) flag body.
- **G2. Not an identity.** The outcome is a numerical classification over a locked family. It is not fixed by a theorem the author has; the flag-body case in particular is not known to the author. Label: **TEST**.
- **G3. Rival.** "P7 is needed": outside the Jordan class P1–P6 admit a body at least as cheap as complex QM. It predicts a HIT or TIE, most likely the SU(3) flag orbitope (§5).
- **G4. Reach.** Level (a), toy classification, with a route to (b) (a general classification of hSFP orbitopes).
- **G5. Next step.** HIT/TIE: log the body as a counterexample to "P1–P6 select complex QM" (OBSERVED (numerical) until an exact proof of its capacity and hSFP), keep P7 load-bearing, and say so in the PR body. MISS: P7 is not needed given P5 for these groups and dimensions on the locked grid; next, products of two rank-2 groups and dimensions 16–24. INCONCLUSIVE: report the OPEN bodies; no claim either way.

## 3. Candidates and the reduction (locked)

1. **Reduction to zero weights (PROVED (in-model)).** Let G be connected compact, acting linearly, K = conv(G·v), and G₀ ⊇ G the identity component of K's symmetry group. If K has SFP under G₀, a maximal torus T₀ of G₀ fixes a pure state p. A maximal torus T of G lies in some maximal torus of G₀, which is gT₀g⁻¹ for some g ∈ G₀ (maximal tori of a compact connected group are conjugate; Hopf–Samelson 1940, `10.1007/BF01378063`). So T fixes g·p. Since G is transitive on the pure states, g·p = h·v with h ∈ G, and h⁻¹Th fixes v. So **v may be taken in the zero-weight space Z of T**.
2. **Amplitudes do not matter (PROVED (in-model)).** Rescaling one irreducible summand by a non-zero real number is a G-equivariant invertible linear map, hence an affine isomorphism of orbitopes. So the relative amplitudes and signs of distinct summands are irrelevant. A summand repeated m times reduces to min(m, dim Zᵢ) copies. Within this range every irreducible with a zero weight has dim Zᵢ ≤ 2, and every repeated sum with dim Zᵢ = 2 exceeds dimension 15, so each type appears once. The only real parameter is the direction of v inside a summand with dim Zᵢ = 2.
3. **Representations (KNOWN; zero-weight dimensions confirmed by `--list`).** Real irreducibles of dimension ≤ 15, with dim Z:
   - SU(3): adjoint 8 (dim Z = 2); C³ as R⁶ (0); Sym²C³ as R¹² (0). Larger ones exceed 15. Adjoint ⊕ trivial is the same body (a translation).
   - Sp(2) (acting through SO(5) where Z ≠ 0): 5 (1), 10 = Λ²5 (2), 14 = Sym²₀5 (2, contains real QM d = 14); the spin 4 = H² as R⁸ (0). 5 ⊕ 5 reduces to 5 (dim Z = 1).
   - G₂: 7 (1); 14 adjoint (2). 7 ⊕ 7 reduces to 7.
   - SO(3) (image of U(2), and of Sp(1) where Z ≠ 0): spin j, dimension 2j + 1, dim Z = 1. Half-integer spins have no zero weight.
   - SO(3)ᵏ: types (j₁, …, j_k), dimension ∏(2jᵢ + 1), dim Z = 1.
4. **The enumeration (927 bodies; counts and names in `list.out`).** Sums of distinct types, affine dimension d as stated:
   - SU(3): 8, angle grid plus Weyl-singular directions (120 + 6 bodies).
   - Sp(2): 5 (1); 10 (120 + 8); 14 (120 + 6); 5 ⊕ 10 at d = 15 (120 + 8).
   - G₂: 7 (1); 14 (120 + 12).
   - U(2) → SO(3), d = 9–15: spins {4}, {5}, {6}, {7}, {1,3}, {1,4}, {1,5}, {2,3}, {2,4}, {1,2,3} (10 bodies).
   - Sp(1)² → SO(3)², d = 9–15, both factors acting: 34 bodies, including (1,1) at d = 9 and the products B3 × Zj.
   - Sp(1)³ → SO(3)³, d = 9–15, all factors acting: 35 bodies, including B3³ at d = 9.
   - Products G × Sp(1)ᵏ (k = 1, 2, 3; G = SU(3), Sp(2), G₂) as external sums, d ≤ 15, with the rank-2 factor on a coarser 15° grid plus its Weyl-singular directions: 205 bodies. Plus Sp(2) × Sp(1) on the tensor product 5 ⊗ 3 (d = 15, 1 body), the only irreducible tensor type in range.
   - **Not covered (stated, not hidden):** products of two rank-2 groups (for example SO(5) × SO(5) on 5 ⊕ 5); Sp(1)ᵏ with k ≥ 4; dimensions above 15.
5. **Family coverage.** For a summand with dim Z = 2 the direction of v is u(θ) = cos θ·e₁ + sin θ·e₂, θ = 0°, 3°, …, 357° (full circle; the Weyl group and ±1 make the bodies repeat, and repeats are a consistency check). Inside products the step is 15°. **The Weyl-singular directions are added as separate bodies** (directions where the orbit dimension drops, found from the acting algebra alone by a 0.25° scan of the smallest generic singular value of [X·u(θ)] and a bounded refinement; `--list` finds 6 for SU(3), 8 for Sp(2) 10 and for 5 ⊕ 10, 6 for Sp(2) 14 and 12 for G₂ 14, the counts the root systems predict). They contain the CP² orbit (complex QM₃) and real QM₅. **Coverage is the grid plus these directions.** A HIT or TIE confined to a window narrower than the step can be missed; a MISS is a statement about the listed bodies.

## 4. Method (locked; implemented in `search_rank2.py`)

1. **G₀ for every candidate.** In centred coordinates on the affine span, g₀ = the linear vector fields tangent to the orbit at max(60, 4d²) sampled points (null space of the stacked tangency conditions). It contains the acting algebra and can be larger (for example G₂ on 7 gives the ball B7 with G₀ = SO(7)). Its rank and dimension are printed. All later steps use g₀.
2. **SFP.** rank of the stabilizer algebra of v in g₀ equals rank g₀ (the maximal-torus criterion; PROVED (in-model) for compact connected groups by maximal-torus conjugacy).
3. **Capacity bounds.**
   - **Upper bound (PROVED (in-model), the method is exact as a bound).** Let λ = min e(c) over affine effects e ≥ 0 on K with e(x₀) = 1, c the centroid. If x₁…x_N are perfectly distinguishable by e₁…e_N, then moving each eᵢ by a symmetry taking xᵢ to x₀ (c is G₀-invariant) gives eᵢ(c) ≥ λ, and 1 = Σ eᵢ(c) ≥ Nλ. So N ≤ ⌊1/λ⌋. The LP over a finite set of orbit points is a relaxation, so its minimum α ≤ λ and **N_UB = ⌊1/α + 10⁻⁶⌋ is a valid upper bound whatever the grid**. Cutting planes (orbit points where the optimal effect is most negative, by local minimization) only tighten α. With no positive α the body is OPEN.
   - **Lower bound (OBSERVED (numerical)).** The largest N ≤ N_UB with an LP witness on a candidate set: subsets of torus-fixed points, prefixes of greedy sets (repeatedly add the orbit point with least summed inner product), then 100 random grid sets. Positivity is imposed on the grid plus cutting planes. A witness is accepted when every effect's orbit minimum, by local minimization from the 12 lowest grid points, is ≥ −10⁻⁶. A HIT or TIE resting on N_LB stays OBSERVED (numerical) until proved.
4. **hSFP (P5), including non-exposed faces.**
   - A face with a positive-dimensional stabilizer is invariant under a circle, which is conjugate into the maximal torus T. So it is invariant under a subtorus S ⊂ T. Which S matter is decided by which weights vanish on S, so the S are the flats of the weight arrangement. For each flat, a generic H in its annihilator generates S.
   - **Failure certificate (OBSERVED (numerical)):** for 24 random S-invariant functionals ℓ, max of ℓ over the orbit exceeds by more than 10⁻⁶ × radius the max over the S-fixed pure states. Those states are the union of Z(S)-orbits of the torus-fixed points. A gap means the S-invariant face exposed by ℓ has no S-fixed pure state.
   - **Non-exposed faces.** The minimal exposed face containing a face F is invariant under F's stabilizer (it is the intersection of the exposed faces containing F, a set permuted by that stabilizer), so an S-invariant exposed face exists whenever F is S-invariant. Faces of exposure depth 2 are probed with ℓ₁ + εℓ₂, ε = 0.01, ℓ₁, ℓ₂ both S-invariant (lexicographic exposure). **Depth ≥ 3 is not tested; this is a declared limit.**
   - "No failure found" is reported as a pass for scoring; it is OBSERVED (numerical), not a proof.
5. **P6 bit-face clause.** For the first two states p, q of the capacity witness, take the minimal exposed face containing (p + q)/2. Its normal is the mean of max(5, d) normal-cone LP vertices, each made valid on the whole orbit by cutting planes; the face is the whole body if the normal cone is {0}. The face's pure states are local maxima of the normal over the orbit. The clause holds iff they span an affine 3-space and lie on an ellipsoid (rms quadric residual < 10⁻³, positive definite; affine dimension counts singular values above 10⁻² of the largest). Controls: B3 gives a 3-ball; real QM₃ (Z2) gives a 2-dim face, not a ball (`selftest.out`).
6. **Complex QM itself (TARGET).** A body is complex QM₃-type if (d, N_LB = N_UB, dim G₀, dimension of the pure-state manifold) = (N² − 1, N, N² − 1, 2(N − 1)). The pure-state dimension separates CP² (4) from the SU(3) flag manifold (6), which share (8, 3, 8). Real QM, balls and quaternionic QM₃ are tabulated the same way for the printout only; they are scored by G1.
7. **Time budget.** Each body has 3600 s wall clock; a body that runs out is OPEN (time budget). This rule is fixed now so that no run can be stopped and rescored afterwards.
8. **Constants (in the script):** N_GRID = 6000 orbit samples; ANG_STEP_DEG = 3; PROD_ANG_STEP_DEG = 15; N_FUNC = 24; EPS_LIST = (1.0, 0.01); FAIL_TOL = 10⁻⁶; CUT_ROUNDS = 60; NEG_TOL = 10⁻⁶; N_FACTORS = 6 (random group element as a product of six one-parameter steps); BODY_BUDGET_S = 3600.

## 5. Predeclared expectations (HYPOTHESIS)

- **SU(3) generic adjoint (flag) orbitope: likely TIE**, at about 50%. Its affine dimension is 8 = 3² − 1. Its stabilizer is a maximal torus, so SFP holds. Its capacity is plausibly 3 (the three Weyl-related points diag(a, b, c) permuted). Singular functionals expose faces that may be 3-balls, so hSFP and the bit-face clause may hold. If so, the overall result is HIT (by tie), and P7 (or a new premise) is doing work at N = 3. The direction angles that are Weyl-singular give the CP² orbit = complex QM₃, which is scored TARGET.
- **Jordan cases:**
  - real QM₅ (Sp(2) 14 at its singular direction): fails hSFP (disc faces);
  - B5 (Sp(2) 5) and B7 (G₂ 7, G₀ = SO(7)): capacity 2 and d > 3, MISS on cost;
  - quaternionic QM₃ (d = 14, N = 3) is not reached by these groups; it would lose on cost (14 > 8).
- **Products** are expected to be MISS on cost (dimension adds, capacity does not grow comparably), and SO(3)-only bodies in dimensions 9–15 to be MISS (hSFP or cost), as in dimensions 4–8.
- **Tie handling.** A TIE is scored as a hit (G1). The result then names the body, its angle range, and the exact checks still owed (an exact capacity proof and an exact face classification). It does not call the tie settled.

## 6. Deviations rule

- Before the scored run, any change to the script or this file is a new commit with a `DEVIATIONS.md` line, a new `PREREG.sha256`, and a new push. No `--run` output may be viewed before it.
- A crash during `--run` may be fixed only if the fix touches no scoring constant or rule. It is logged in `DEVIATIONS.md`, re-locked and re-pushed before the rerun, and the crashed partial output is committed as is.
- After the run, nothing in §2–§4 changes. Relabels, if any, are reported beside the script labels and never move a miss to a hit (the forward rule recorded in #292's `DEVIATIONS.md`, applied here too).
