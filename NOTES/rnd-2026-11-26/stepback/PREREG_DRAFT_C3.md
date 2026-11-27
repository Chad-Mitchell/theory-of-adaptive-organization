# DRAFT prereg C3: from a pure (or product) start, which worlds can write an informative event log, and at what start-entropy price?

*DRAFT ONLY. Not locked, not pushed, not run. Written 26 Nov 2026 after GATE_READ_STEPBACK.md, following its lessons (validity gates for any step whose failure prints the prediction; world/target not fixed to decide the outcome; fair comparator; numeric predictions; §0 disclosure). Needs a fresh gate read before any lock.*
Labels: PIM · OBS · HYP · KNOWN · CHOSEN · open miss.

## §0 Disclosure: what is already known or seen (read before judging the predictions)
1. **Most of this is fixed by proved results.** Ent-E1 (R&D notes, hostile-reviewed, not in CLAIM_MAP_v2): under LT, NR, RV, valid product effects, a pure product start and tracking, the history is a reversible entangling map. E-L0 (R&D notes): if every reversible map has the form (⊗g_i)∘P_σ, products stay products. M11′/M12/M12ₙ/RC18 (CLAIM_MAP RC13, RC15, RC17, RC18): in those polytope classes no reversible map entangles. PREREG_P (lock a4e02d65…; outputs/p1.txt): classical bits need exactly 1.000000000000 bit of start entropy for Θ(1,0); QM and stabilizer need 0; boxworld max(□,□) is infeasible from any product start. So Arms 1 and 3 below are **consistency checks** (V ≤ 2), declared as such.
2. **Seen data that bears on Arm 2:** Round 13 H4 (60 random non-symmetric hexagon² composites: no entangling automorphism, colour-refinement certificates); the entangle group-order table (Aut = local ⋊ swap in square², square×octahedron, octahedron², square×hexagon, hexagon² min/max and 13/13 locally symmetric intermediates); R16 / the R13–16 review (Aut(max(I,D)) = 120², all local). These make "rigid" the expected outcome for random intermediates. **No automorphism group of any Arm 2 composite (pentagon × heptagon, cube × octahedron, non-symmetric) has been computed by me or, as far as the notes show, by anyone in this project.**
3. The gate read of the step-back (GATE_READ_STEPBACK.md) was read before writing this; it ranked C3 "a cheap consistency check under P, value capped".
4. Author's own assessment before any run: Arms 1 and 3 restate Ent-E1, E-L0, M11′ and PREREG_P. Only Arm 2 is informative, and it is adjacent to Conjecture C (route C7).

## §1 Question and claim being tested
"Time as a sequence of informative records" is operationalised as: **a closed world can write an informative event log iff, after a reversible history from a product start, some read on part A has a uniform outcome (≥ 1 bit) and a read on part B predicts it perfectly (PREREG_P's task Θ(1, 0)).** The start-entropy price S_min is the minimum, over feasible product starts, of the Shannon entropy of the start written as a mixture of pure product states (defined in §3).
HYP under test (C3): worlds fall into exactly three classes: **fuel-needing** (S_min = 1 bit; classical-like correlating maps exist, none entangling), **rigid** (infeasible from every product start; no informative log at any price), **free** (S_min = 0; an entangling map exists). The pure start P gives an informative log iff the world is "free".

## §2 Worlds (fixed in advance; the target is not chosen to decide the outcome)
Parts have all effects (no-restriction) unless stated; composites are in the locally tomographic slice between min and max.
- **Arm 1 (consistency, theorem-fixed):** classical bit²; QM 2-qubit (CNOT and 10⁴ Haar unitaries, seed 20261126); stabilizer 2-qubit (restricted reads, Clifford group); square² min and max; hexagon² max; octahedron² max; cuboctahedron² max.
- **Arm 2 (open):** 40 new non-locally-symmetric intermediate composites: S = conv(min ∪ R), R a random k-subset of the non-product extreme points of max, k ∈ {1, 2, 3, 5}, 5 seeds each (seeds 101–105), for **pentagon × heptagon** (20 composites, regular polygons, exact coordinates in Q(cos 2π/5, cos 2π/7) handled by the canonical-form gate) and **cube × octahedron** (20 composites, rational coordinates). Neither family appears in any earlier round.
- **Arm 3 (sequence length, theorem-fixed):** for each "free" world in Arm 1, iterate one fixed reversible map g from the Θ-feasible start and record the period of the marginal sequence (stabilizer: exact; QM: g = exp(−iθH) with θ = 1 rad and a fixed generic two-qubit H, 10⁶ steps).

## §3 Method
1. Compute Aut(S) (linear automorphisms) exactly: facets/vertices by exact vertex enumeration (pycddlib exact mode; Q-extension coordinates via canonical exact forms), automorphisms by colour refinement + backtracking, cross-checked by nauty/BLISS on the vertex–facet incidence graph. Reversible maps = Aut(S) (rule RV, composite-relative).
2. Classify each g ∈ Aut(S) (or each coset of the local subgroup): **product-preserving** (maps every product state to a product state), **correlating, non-entangling** (maps some product mixed state to a correlated state but every pure product to a pure product), **entangling** (maps some pure product to a non-product extreme point).
3. Θ(1, 0) feasibility: for each correlating or entangling g, search starts that are products of (a) pure states (S = 0) or (b) a uniform mixture of two pure states on one part and pure elsewhere (S = 1 bit), exhaustively over vertex pairs; test the existence of a read on A with uniform outcome and a read on B predicting it with success 1 (LP over effects, exact re-verification).
4. S_min = 0 if (a) succeeds for some g; 1 bit if only (b) succeeds; "infeasible" if neither succeeds for any g. (Starts with S strictly between 0 and 1 cannot give H(A) ≥ 1 under product-preserving-on-pure maps; this is the PREREG_P argument and is part of §4's gate G6.)

## §4 Validity gates (each one guards a step whose failure could print the predicted outcome)
- **G1 group reach:** Aut orders must reproduce the known table before Arm 2 runs: square² min/max 128, octahedron² min/max 4608, hexagon² min/max 288, square×hexagon 96, classical triangle² 362880, pyramid×square 1024, max(I,D) 14400. Any mismatch stops the run (counts as not tested). *Guards: a search that cannot reach non-local automorphisms would print "rigid".*
- **G2 canonical forms (R14 H3 lesson):** for every composite, the number of distinct exact canonical coordinate/inner-product values must equal the number of distinct float values at separation 1e−9; else stop. *Guards: too-fine classes hide automorphisms and print "rigid".*
- **G3 positive control for "fuel-needing":** square-pyramid × square (min and max) must come out S_min = 1 bit (E-L0: correlating, non-entangling controlled maps exist). If it prints "rigid", the classifier is broken; stop.
- **G4 positive control for "free":** stabilizer 2-qubit must give S_min = 0 with an entangling Clifford (E-err1: 11520 under RV, local 1152); QM CNOT|+0⟩ must give success 1.000000000 ± 1e−9.
- **G5 negative control:** square² max must give "rigid" (Aut = local ⋊ swap).
- **G6 estimator:** the classical bit² must give S_min = 1.000000000000 bit exactly (PREREG_P value), and an LP over effects must recover Helstrom success for a stated qubit pair (|0⟩ vs |+⟩: (1 + 1/√2)/2) to 1e−9.
- **G7 hypotheses:** for every Arm 1–2 composite, check LT (affine dimension of the composite = product of part dimensions + …, per the slice definition) and NR on parts; a composite failing them is reported separately, not scored.
- **G8 finite precision:** every feasibility decision is re-verified in exact arithmetic; any float-only decision counts as not tested.

## §5 Predictions (numeric; written before any run)
| arm | world | predicted class | number |
|---|---|---|---|
| 1 | classical bit² | fuel-needing | S_min = 1.000000000 ± 1e−9 bit |
| 1 | QM 2-qubit, stabilizer 2-qubit | free | S_min = 0 ± 1e−9 |
| 1 | square² min/max, hexagon² max, octahedron² max, cuboctahedron² max | rigid | infeasible at every start |
| 2 | 40 new composites | rigid in **≥ 36 of 40** (prior 0.6); fuel-needing in the rest (prior for ≥ 1 fuel-needing: 0.35); free in **0 of 40** (prior 0.97) | counts as stated |
| 3 | stabilizer | periodic, period divides the order of g in the Clifford group (≤ the maximal element order, computed exactly) | exact |
| 3 | QM, θ = 1 rad | no exact recurrence of the marginal sequence in 10⁶ steps (min trace distance to the start marginal > 1e−12) | exact to 1e−12 |

**Falsifiers:** Arm 1 any mismatch (would contradict a proved result: stop and recheck the instrument first); Arm 2 any "free" composite (a reversible entangling map in a non-locally-symmetric composite of non-classical polytope parts: a counterexample to Conjecture C outside local symmetry, rebuilt as an exact map and reported); Arm 2 more than 4 "fuel-needing" composites (the rigid-majority prediction misses); Arm 3 any mismatch.

## §6 What each outcome would and would not mean
- **As predicted:** under these definitions, an informative event log from a product start comes in three kinds: fuel-needing (classical: novelty must be stored in the start), rigid (polytope classes: no record can ever form), free (entangling worlds: novelty from a pure start). The pure start P buys a free log only in entangling worlds. This is a re-reading of Ent-E1, E-L0 and M11′ plus one new count (Arm 2). It **does not** derive P, the arrow, time, or entanglement; P stays an interpretive premise, and Conjecture C stays open outside the tested families.
- **Arm 2 "free" in any composite:** the most informative outcome (a Conjecture C counterexample), to be rebuilt exactly and hostile-reviewed before any claim.
- **Arm 2 many "fuel-needing":** random intermediates admit classical-like correlating maps; the rigid/free dichotomy for polytope worlds is wrong in general.

## §7 Score on the corrected scale
Arms 1 and 3: V_hit 2 (theorem-fixed). Arm 2: p(as predicted) 0.6, V 2; p(free) 0.03, V 9; p(many fuel-needing) 0.35, V 3 → EIV ≈ 0.6·2 + 0.03·9 + 0.35·3 = 2.52 for about 3 h including the Q-extension canonical-form work → ≈ 0.84 per hour, lower than the 1.38 used in the §9 ranking (which assumed 1.5 h and no open arm). **Assessment: C3 as a whole mostly restates Ent-E1, E-L0, M11′ and PREREG_P; its only informative part (Arm 2) is a rigidity count adjacent to Conjecture C (route C7).**
