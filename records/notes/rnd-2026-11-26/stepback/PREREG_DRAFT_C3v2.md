# DRAFT prereg C3v2: rigid, fuel-needing or free? Locally symmetric odd-polygon composites from a product start

*DRAFT ONLY. Not locked, not pushed, not run. 26 Nov 2026, after GATE_READ_STEPBACK2.md (amendments 3a–3j). Supersedes PREREG_DRAFT_C3.md (kept as written). Needs a gate read before any lock; §8 argues a paper lemma should come first.*
Labels: PIM · OBS · HYP · KNOWN · CHOSEN · open miss.

## §0 Disclosure: what is already known, seen or argued
1. **Proved results that fix parts of the outcome.**
   - Ent-E1 (R&D notes, hostile-reviewed, not in CLAIM_MAP_v2) and E-L0.
   - M11′ (RC13); M12 plus the disk lemma (**RC15: ♦ holds for every pair of regular polygons, odd or even, so locally symmetric polygon composites with finite orbits have no reversible entangling map**; PROVED (in-model), a parallel worker's self-check, not independent, not formalized).
   - M12ₙ (RC17); RC18 (cuboctahedron² ♦, not preregistered).
   - PREREG_P (lock a4e02d65…).
   - **Consequence, stated before the run: the "free" outcome in Arm 2 is excluded by RC15.** Arm 2 is therefore (i) an independent instance check of RC15 and (ii) a test of the question RC15 does not cover: whether correlating, non-entangling automorphisms ("fuel-needing") exist.
2. **Correction to gate read 2 §3.1, with proof.** In a regular n-gon with all effects, vertices i and j are perfectly distinguishable iff their normal cones N_i and −N_j overlap. Each N_i spans 2π/n about the vertex direction. For the pentagon, N_0 = [54°, 126°] and −N_2 = [18°, 90°] overlap, so every non-adjacent pair is perfectly distinguishable: 5 pairs in the pentagon, 7 in the heptagon (`STEPBACK` §13 C13-4; float check over 2·10⁵ directions agrees). Vertex starts can therefore reach Θ(1,0) in odd polygons; the start search is widened anyway (§3.3).
3. **Author's paper argument (HYP, not proved; called "Lemma R"):**
   - Setup: let S lie between min and max, with LT and valid product effects, and both parts polygons with n ≥ 4.
   - Rows and columns are faces of S. Each row F_i = v_i ⊗ P_B is exposed by e_i ⊗ u (pure marginal ⇒ product); each column is exposed likewise.
   - An automorphism that maps pure products to pure products sends a row to a 2-dimensional face whose extreme points are n_B product vertices. If every "mixed" set of ≥ 4 product vertices (not all in one row or one column) is affinely ≥ 3-dimensional, that face must be a row or a column. Column images then force the map to be local ⋊ swap.
   - If Lemma R holds, "fuel-needing" is impossible here, and **the whole predicted outcome follows from RC15 + Lemma R**. The affine-dimension condition is the unproved step.
   - **I have not tried it on any Arm 2 composite.**
4. **Seen data:** the entangle group-order table (Aut = local ⋊ swap in square², square × octahedron, octahedron², square × hexagon and hexagon² min/max, and in 13/13 locally symmetric intermediates); R13 H4 (non-symmetric hexagon² composites); R16 (Aut(max(I, D)) = 120²). **No automorphism group, vertex set or orbit decomposition of any pentagon², pentagon × heptagon or pentagon × bit composite has been computed in this project, as far as the notes show.** The cuboctahedron² max Aut order is not recorded anywhere.
5. Gate reads 1 and 2 were read before writing this. No exploratory run was made.

## §1 Question
From a product start, under reversible maps RV = **Aut(S)** (one rule for every arm; the CP-restricted group is reported beside it but not used), each world is classified by whether a closed history can complete PREREG_P's task Θ(1, 0): a read on A with a uniform outcome (≥ 1 bit) and a read on B that predicts it with success 1. The classes are:
- **free:** S_min = 0 (an entangling automorphism exists);
- **fuel-needing:** S_min > 0 is finite (a correlating, non-entangling automorphism exists);
- **rigid:** infeasible from every product start (Aut(S) ⊆ local ⋊ swap, so products stay products by E-L0).

## §2 Worlds
- **Arm 1, theorem-fixed (consistency):**
  - classical bit²: fuel-needing, S_min = 1;
  - QM 2-qubit: free;
  - stabilizer 2-qubit (restricted reads; Aut(S) expected 23040, CP-restricted 11520): free;
  - square² max: rigid;
  - hexagon² max: rigid.
  - Cuboctahedron² max appears here **only if** its Aut order, computed pre-run in G1, equals 48·48·2 = 4608. Otherwise it moves to Arm 2.
- **Arm 2, open, locally symmetric odd-polygon intermediates (3c):** for P5² (field Q(√5)) and P5 × P7 (field Q(√5, cos 2π/7), degree 6):
  - Compute max's non-product extreme points and their orbits under the local group: D5 × D5 ⋊ swap (order 200) for P5², and D5 × D7 (order 140, no swap) for P5 × P7.
  - Let m be the number of orbits. If 2^m − 1 ≤ 63, take every union R of orbits; otherwise take all unions of at most 2 orbits plus max itself. S = conv(min ∪ R).
  - Every such S is invariant under the local group, so local reversible maps stay reversible (the M12/RC13–19 premise holds by construction, 3a).
- **Arm 3 (sequence, theorem-fixed):** stabilizer: the period of the marginal sequence under one fixed entangling Clifford. QM: U = exp(−iθH) with θ = 1 rad and a fixed generic H (seed 20261126). U^n is computed by eigendecomposition, U^n = V·diag(e^{−inθE})·V†, for n ≤ 10⁶ (3j).

## §3 Method
1. **Exact geometry.**
   - Vertices: regular polygon vertices in exact coordinates. P5 uses cos 72° = (√5 − 1)/4 and sin-free affine coordinates (an affine image with coordinates in Q(√5)). P7 uses c = 2cos(2π/7), with c³ + c² − 2c − 1 = 0.
   - Every number is reduced to its rational coordinates in the fixed Q-basis {1, √5} ⊗ {1, c, c²}.
   - max = all states positive on product effects, by exact vertex enumeration of the dual cone.
2. **Aut(S):** colour refinement plus backtracking on the vertex–facet incidence with exact inner-product classes, cross-checked by nauty/BLISS. Each element is classified as product-preserving, correlating non-entangling, or entangling (as in C3 §3.2), in exact arithmetic.
3. **Θ(1, 0) and S_min.**
   - Starts: products of states of the form uniform mixtures of up to 4 points, each point drawn from the part's vertices, its edge midpoints, and a 20-point rational grid on every edge (3d).
   - **S_min** is the minimum over feasible starts of the decomposition entropy: the minimum, over decompositions of the start into pure product states, of the Shannon entropy of the weights.
   - Decomposition entropy and measurement entropy differ in general GPTs; the measurement entropy of A's novelty read is reported beside S_min.
   - Feasibility is decided by an LP over effects, re-verified in exact arithmetic.

## §4 Validity gates
- **G1 group reach**, all before Arm 2 runs:
  - known orders: square² min/max 128; octahedron² min/max 4608; hexagon² min/max 288; triangle² 362880; pyramid × square 1024; max(I, D) 14400;
  - **same-field controls:** P5 × P7 min = 140 and P5² min = 200;
  - the cuboctahedron² max order is computed and recorded here.
  - Any mismatch stops the run (not tested).
- **G2 exact basis reduction:**
  - every value used in colour refinement is reduced to the 6 rational coordinates in the fixed basis;
  - the exact class count must equal the float class count on the same quantities at separation 1e−9;
  - (√5 − 1)/4 and 2·((1 + √5)/4)² − 1 (two exact forms of cos 72°, equal by hand) must land in one class.
- **G3a odd-polygon fuel control, vertex start:** P5 × bit (classical segment), with the controlled reflection whose axis passes through v_{i+1}. It must give fuel-needing, S_min = 1 bit, success 1 (v_i and v_{i+2} are perfectly distinguishable, §0.2).
- **G3b odd-polygon reach control, non-vertex start:** P5 × bit restricted to controlled 72° rotations. The classifier's answer (feasible or not; if feasible, which edge-grid start) must equal a hand calculation appended before lock. If the hand calculation is not done, G3b is marked missing and Arm 2 is not scored.
- **G4 free control:** stabilizer 2-qubit with RV = Aut(S); |Aut(S)| must equal 23040 (the CP-restricted 11520 is reported). It must give free. The QM CNOT|+0⟩ success must be 1 ± 1e−9.
- **G5 rigid control:** square² max must give rigid.
- **G6 estimator:** the classical bit² must give S_min = 1.000000000000 bit; Helstrom success for |0⟩ vs |+⟩ must equal (1 + 1/√2)/2 to 1e−9.
- **G7 hypotheses:** for every S, the exact rank of its vertex set must be K_S = K_A·K_B (9 for every polygon pair, 4 for bit², 16 for qubit²); LT then holds. Invariance of S under the local group is checked exactly.
- **G8:** every classification and feasibility decision is re-verified in exact arithmetic; float-only decisions count as not tested.
- **G9 time and completion:**
  - limit 2 h for max(P5 × P7) vertex enumeration and 20 min per Arm 2 composite;
  - a timeout counts as not tested, never as rigid;
  - Arm 2 is scored only if ≥ 80% of its declared composites complete;
  - predictions are stated as fractions of completed composites.

## §5 Priors, derived (not picked)
- **p(any Arm 2 composite free) ≈ 0.04.** This equals p(RC15 fails in this class). Of about six hostile-reviewed theorem claims in this thread (E-L0, Ent-E1, M11, M12, M12ₙ, the RC18 certificate), one (M11) needed a scope correction: 1/6. Such an error must land on polygon pairs, which is one of about four scope components (parts, composite class, orbits, ♦): 1/6 × 1/4 ≈ 0.04.
- **p(every Arm 2 composite rigid) ≈ 0.75.** Families of non-classical parts with absolutely irreducible groups seen so far: 5 of 5 rigid. By the rule of succession, a new family is rigid with probability 6/7, and two new families with (6/7)(7/8) = 0.75. Lemma R would raise this; it is unproved, so it is not used.
- **p(≥ 1 fuel-needing composite)** ≈ 1 − 0.75 − 0.04 ≈ 0.21.

## §6 Predictions (numeric)
| arm | world | prediction |
|---|---|---|
| 1 | classical bit² | fuel-needing, S_min = 1.000000000 ± 1e−9 bit |
| 1 | QM, stabilizer | free, S_min = 0 ± 1e−9 |
| 1 | square² max, hexagon² max | rigid |
| 2 | every completed P5² and P5 × P7 orbit-union composite | **rigid: 100% of completed composites**, Aut(S) = local group (⋊ swap for P5²); **free: 0%** |
| 3 | stabilizer | period divides the order of the chosen Clifford (exact) |
| 3 | QM | min over 1 ≤ n ≤ 10⁶ of the trace distance from the start marginal > 1e−12. This is a numeric threshold: quasi-periodic orbits come arbitrarily close in principle |

**Falsifiers:**
- Arm 2: any completed composite that is not rigid. A fuel-needing composite refutes Lemma R's conclusion for these parts; a free composite contradicts RC15 and is rebuilt as an exact map.
- Arm 1 or 3: any mismatch (stop; check the instrument first).

## §7 What outcomes would and would not mean
- **As predicted:** an independent instance check of RC15 in odd-polygon intermediates, plus evidence that no classical-like controlled maps exist there. Under P, these worlds can write no informative event log at any start price (rigid). It does **not** derive P, the arrow, time or entanglement, and it does not touch Conjecture C beyond polygons.
- **Fuel-needing found:** locally symmetric, irreducible non-classical parts can carry classical-like correlating maps, so the "rigid" pattern in the group-order table is not general. That is new and worth a hostile review.
- **Free found:** RC15 fails; stop and recheck RC15 first.

## §8 Score (corrected scale) and recommendation
- **Full draft (P5² and P5 × P7):** EIV = 0.75·2 + 0.21·4 + 0.04·9 = 2.70. Cost ≈ 5 h (degree-6 exact field, max enumeration, G3b hand calculation, G9 limits). Score **≈ 0.54 per hour.**
- **P5²-only cut (Q(√5) only; one family):** p(rigid) 6/7 ≈ 0.86, p(free) 0.03, p(fuel) 0.11. EIV = 1.71 + 0.44 + 0.27 = 2.42 over ≈ 3 h. Score **≈ 0.81 per hour.**
- **Paper alternative (Lemma R):** prove or refute the affine-dimension step for polygon pairs (n ≥ 4). p(proof) 0.6 with V 3; refutation (a mixed coplanar product set) V 2 at 0.4. EIV 2.6 over ≈ 1.5 h ≈ **1.7 per hour**, the best item in this file.
- **Recommendation:** do Lemma R on paper first. If it holds, Arm 2's main question is answered without a run, and C3v2 reduces to an instance check of RC15 (V ≈ 2).

---

## Corrections after LEMMA_R.md and its hostile review (appended before any lock; the text above is left as written)
- **Read cap (M1 of `rnd/review_lemma_r/HOSTILE_REVIEW_LEMMA_R.md`).**
  - Θ(1, ε) is evaluated only over reads on A with **M ≤ 2 outcomes** (binary reads, as in PREREG_P's actual run), and over reads on B with any finite number of outcomes.
  - Reason: with unbounded M, a state-ignoring read with M − 1 ≥ 2^91.92 outcomes meets Θ(1, 0.01) with no correlation. At ε = 0, the cap does not change any outcome.
  - Any lock must state this cap in §1 and in §3.3.
- **Arm 2 is now theorem-fixed, conditional on RC15** (LEMMA_R R2 and R3, under the premise list in LEMMA_R C9-2): every completed P5² and P5 × P7 orbit-union composite is rigid.
  - Rescore: EIV ≈ 0.95·2 + 0.05·9 ≈ 2.35, which is ≈ 0.47 per hour for the full run and ≈ 0.78 per hour for the P5² cut.
  - **Recommendation: do not lock this draft.** The useful independent item is an exact RC15 instance check on max(P5, P7) alone, which Al-Safi–Richens do not cover.
- **Prior art for §0.3:** "Lemma R" is now written and reviewed (LEMMA_R.md §9). It is a partial case of Open Quantum Problem #42 (Dakić–Müller).
