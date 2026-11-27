# C12c-G′: is a required accuracy a stake in disguise on our own world menu? (first work unit)

*26 Nov 2026, about 10:45–11:10 EST. Local note only (not committed or pushed). Self-checked only; it needs a hostile review before it counts. Repo read only at `ac92ee2`. Scripts and outputs are in `c12cg/`. Labels: **PIM**, **KNOWN**, **ELEMENTARY**, **HYP**, **OBSERVED**, **CHOSEN**, open miss.*

## 0. Pick: C12c-G′ over the C3v2 P5² cut, and why
Both were listed at ≈ 0.78/h.
- **C3v2 P5² cut: the outcome is already known.** PREREG_DRAFT_C3v2's own corrections (after LEMMA_R and its review) say Arm 2 is theorem-fixed, conditional on RC15: every completed P5² and P5×P7 orbit-union composite is rigid. They also say "do not lock this draft". A run would be an instance check with V ≈ 2 and p ≈ 0.95 of the predicted outcome.
- **C12c-G′: open as far as the notes show.** Prior 0.5 (C12C_ONSET §11.5 point 7). The gap had never been computed. C12C_ONSET §11.5 point 5 warns that if each world is one committed point, the result is pre-computable and is bookkeeping, not a test.
- So the first job is to answer that question before drafting any prereg. Either way the unit produces information, which the C3v2 cut cannot. That gives the higher information value per hour.

## 1. Is the outcome already known? Yes: pre-computable, so this is not a scored test
- **Source of the menu** (`theory/record-cost-2026-11-25/scripts/composition/round2/r2_record_pricing.py:44–52`): nine single-system worlds, each with one (spend S, error E) point at locked settings and zero drift.
  - Spends come from `P_rec_polygons` (per-record reading) or log₂N (total reading).
  - Errors come from the sibling table (`nocloning/polygons.py`), typed in rounded to 3–4 decimals.
- There is no spend–error frontier per world; every input is a committed number. §11.5 point 2 applies: the gap is computable from committed numbers.
- So **no prereg is drafted.** The computation below is done openly as bookkeeping, as §11.5 point 2 asks, and is not scored as a test.
- §11.5 point 3 (≥ 3 worlds) holds: nine worlds. The two-world pairs menu is dropped.

## 2. Precise statement
- **Worlds and costs (CHOSEN, from the chain):** for each world W, a point (S_W, E_W). The stake rule picks argmin_W S_W + q·E_W, with q ≥ 0. The cap rule picks argmin_W {S_W : E_W ≤ D}.
- **Mixing (§11.5 point 4):** none, at either level. No time-sharing within a world (each world is one point, so there is nothing to share) and no mixing across worlds.
- **Gap (V6 definition, §11.5 point 6):** a world that is Pareto-minimal, and hence cap-selected on some D-window, but never a stake minimiser for any q ≥ 0.
- **Reading and drift (§11.5 point 1):** both readings are reported, at zero drift.

**Lemma G (ELEMENTARY; KNOWN in substance).** On a finite menu with no mixing:
- cap-selected worlds = Pareto-minimal points (up to ties);
- stake-selected worlds = points on the lower-left convex hull, i.e. "supported" non-dominated points;
- the gap is exactly the set of *unsupported* Pareto points.

*Proof:*
- (⇐ cap) A Pareto point P is the cap minimiser for D ∈ [E_P, min{E_Q : S_Q < S_P}).
- (⇒ cap) A cap minimiser that is dominated is not a minimiser.
- (stake) S + qE is a linear functional with a non-negative direction (1, q). Its minimisers over a finite set are the points of the lower convex hull exposed by such directions. ∎

This is the supported/unsupported distinction of multi-objective optimisation and the integer-programming duality gap (prior art §5). Its use here is only bookkeeping.

## 3. Numbers (OBSERVED; `c12cg/gap.py` → `gap.out`, `gap.json`; `c12cg/exact_err.py` → `exact_err.out`)
**Errors recomputed precisely.** The committed values are alternating-optimisation upper bounds on a 720-point grid. The nearest-vertex encoder with the optimal decoder, integrated exactly over θ-arcs and on a 2×10⁵-point φ grid, gives:

| world | committed | nearest-vertex | alt-opt rerun at M = 720 / 1440 / 2880 |
|---|---|---|---|
| square | 0.125 | 0.125000 | 0.124996 / 0.124999 / 0.125000 |
| pentagon | **0.176** | **0.176393** | 0.176362 / 0.176381 / 0.176392 |
| hexagon | 0.167 | 0.166667 | 0.166661 / 0.166665 / 0.166666 |
| octagon | 0.172 | 0.172335 | 0.172329 / 0.172334 / 0.172335 |
| disk/ball | 0.1817 | 1/2 − 1/π = 0.181690 | analytic |

The alternating optimiser converges to the nearest-vertex value as the grid refines. Global optimality over all encoders is not proved, so these stay OBSERVED.

**Per-record reading** (spends: ball/disk 1.0, pentagon 1.070431, octagon 1.127571, hexagon 1.188722, square/N=4 2.0, N=3 1.585, N=2 1.0):

| inputs | Pareto set | stake winners (q-interval) | **gap** | margin above hull |
|---|---|---|---|---|
| committed (rounded) E | ball≡disk, pentagon, octagon, hexagon, square≡N4 | ball/disk 0–12.36; pentagon 12.36–13.14; hexagon 13.14–19.32; square/N4 > 19.32 | **octagon** | 0.00035 |
| precise E | same | ball/disk 0–12.56; hexagon 12.56–19.47; square/N4 > 19.47 | **pentagon, octagon** | 0.00031, 0.00080 |

- Cap windows (precise E):
  - **pentagon** wins for D ∈ [0.176393, 0.181690);
  - **octagon** wins for D ∈ [0.172335, 0.176393).
- In both, the world is the cheapest feasible one under the cap, and no stake ever selects it.

**Total reading (the locked definition, RECORD_COST_CHAIN:64):** every N = 2 world has S = 1, so the square (1, 0.125) dominates them all. The Pareto set is {square}, and the gap is **empty, trivially**, as §11.5 point 1 warned. One winner at every q > 0 and every D ≥ 0.125.

**Sensitivity.** The per-record spends are lower bounds: binary reads only, k ≤ 3 bits, and k = 2 only for the pentagon and octagon. Raising the hexagon's spend, with the others fixed:
- +0.01 keeps the gap {pentagon, octagon};
- +0.02 empties it;
- +0.05 makes the hexagon itself the unsupported point.

Raising the pentagon's or octagon's own spend only pushes them further off the hull. So **the gap is conditional on the hexagon's P_rec being tight to within ≈ 0.01–0.02 bits.**

**Side observation for the chain's text (not a repo edit):**
- With the committed rounded errors, the first single-system rival to beat the ball under the per-record reading is the pentagon, at q ≈ 12.36. That matches the chain's "q ≈ 12.4" (RECORD_COST_CHAIN §4 table).
- With precise errors the pentagon never wins, and the first rival is the hexagon, at q ≈ 12.56.
- The upper end, 17.6, is the pairwise square-vs-ball crossover (1/(0.1817 − 0.125) = 17.64; unchanged with precise errors).
- The chain's statement "rivals win again above 12.4–17.6" survives in substance, but **which** rival and the lower end move with the fourth decimal of the pentagon's error. Flagged for Ace's cleanup; nothing in THEORY/CORE is touched.

## 4. Result and labels
- **Lemma G:** ELEMENTARY (KNOWN in substance).
- **Per-record reading:** "every cap-selected world is also stake-selected" **fails on the committed menu.** It is an **open miss** for the sentence "a required accuracy is a stake in disguise" on this menu, with named windows: octagon for D ∈ [0.1723, 0.1764), and pentagon for D ∈ [0.1764, 0.1817) with precise errors. **OBSERVED.**
  - The sentence needs "on the convex hull" (C12C_ONSET §7's miss branch).
  - It is **conditional** on the binary-read spends being tight (sensitivity above). Margins are 3–8×10⁻⁴ in error units.
  - It is fragile, and it is a property of the toy cost, not of physics.
- **Total (locked) reading:** no gap, trivially (one dominant world). OBSERVED; ELEMENTARY given the menu.
- **Not a test:** everything is computable from committed numbers (§1). No prereg, no score as a test.
- **What the miss names:** where accuracy ≠ stake in our own rounds. It happens only under the per-record reading, among the near-tied polygons, and only because of the polygons' non-convex (S, E) arrangement (octagon above the pentagon–hexagon chord). That is an input from the polygon geometry, not from the cost.

## 5. Prior art (DOIs checked on Crossref this session; `c12cg/crossref_c12cg.txt`)
- Everett 1963, "Generalized Lagrange Multiplier Method for Solving Problems of Optimum Allocation of Resources", Oper. Res. 11:399–417, 10.1287/opre.11.3.399: multipliers reach only hull points (already credited in C12C_ONSET as Lemma A(a)).
- Geoffrion 1968, "Proper efficiency and the theory of vector maximization", J. Math. Anal. Appl. 22:618–630, 10.1016/0022-247X(68)90201-1: weighted-sum scalarisation recovers properly efficient points under convexity, and not in general.
- Geoffrion 1974, "Lagrangean relaxation for integer programming", Math. Prog. Studies 2:82–114, 10.1007/BFb0120690: the duality gap on discrete problems.
- Ehrgott 2005, *Multicriteria Optimization* (2nd ed., Springer), 10.1007/3-540-27659-9: supported vs unsupported non-dominated points. Crossref lists the title and year and no author field; the author is from the book itself.

Novelty: none in the method. The finding is a bookkeeping fact about the chain's menu.

## 6. What is open
1. **Exact per-record spends** for the hexagon, pentagon and octagon, with multi-outcome reads and k ≥ 3. This decides whether the gap survives (the hexagon needs to be tight within ≈ 0.01–0.02). This is the next unit, C12c-G″.
2. Global optimality of the nearest-vertex encoder for the later-question error (OBSERVED only).
3. Whether the per-record reading is admissible at all. The chain's locked definition is the total reading, under which there is no gap. The per-record column is "outside A6" (RECORD_COST_CHAIN:64).
4. A drift > 0 menu (the q-flip in the total reading exists only with drift). Not computed.
5. Hostile review of this note.

## 7. Rescore (§13 scale)
- **C12c-G′ as a test:** gone. The outcome is pre-computable and now computed; bookkeeping, unscored.
- **C12c-G″ (exact spends decide the gap):** p(gap survives) 0.6, V 3 (a robust, named place in our own rounds where accuracy ≠ stake); p(gap closes) 0.4, V 2 (the per-record menu is then hull-exact, and the earlier observation was an artefact of lower-bound spends). EIV 2.6 over ≈ 2.5 h (LP/SDP-style search over multi-outcome reads in polygons) → **≈ 1.0 per hour**.
  - Caveat: it lives under a reading that the chain's locked definition does not use, so its V is for the C12c sentence only.
- **Rank (Lean aside):** C12c-G″ ≈ 1.0 · C3v2 P5² cut ≈ 0.78 (outcome known; recommend an RC15 instance check on max(P5, P7) instead) · C1′ ≈ 0.75 (waits for the C1 review) · SR-b2 ≈ 0.67 · C12b-A ≈ 0.67 · PB ≤ 0.52 · C4R ≈ 0.2 (shelved).
- **With Lean ×3:** C12c-L ≈ 2.35 · C9 ≈ 1.2 · C12b-Lean ≈ 1.0 · SR-b-Lean ≈ 1.0.

---

## 8. C12c-G″ specification (written 26 Nov 2026 about 10:45 EST, before any C12c-G″ computation; exploratory, not hash-locked)

**8.1 Exact quantity.**
- For a state space S (here a regular n-gon, as a 3-dimensional cone with unit u = (0, 0, 1)):
  - P_rec(S) = sup_k P_rec(S, k);
  - P_rec(S, k) = max over encodings enc : {0,1}^k → S of Σ_{j=1..k} I_acc(X_j), with X_1..X_k independent uniform bits;
  - I_acc(X_j) = sup over all finite-outcome measurements {e_y} (effects with e_y(ω) ∈ [0, 1] on S, Σ_y e_y = u) of the Shannon mutual information I(X_j ; Y), in bits.
- Each bit is read with its own best measurement, which is r2_record_pricing's definition with the binary-read restriction removed.

**8.2 Read class and the two reductions used (to be proved in §9 before use; PIM if they hold).**
- (R1) **Vertex encodings suffice.** For fixed measurements, I(X_j;Y) is convex in the encoded states. A supremum and a sum of convex functions are convex, so the maximum over the product of polygons is attained at vertices.
- (R2) **Exact accessible information by a finite LP.** I(X;Y) = Σ_y φ(e_y), where φ(e) = Σ_x ½·e(ω_x)·log₂[e(ω_x)/e(ω̄)] is convex and positively homogeneous of degree 1 (a perspective). Splitting any effect into extreme rays of the effect cone does not lower the sum. So I_acc = max{Σ_i λ_i φ(r_i) : λ ≥ 0, Σ_i λ_i r_i = u} over the cone's extreme rays r_i: a linear program. Its optimum sits at a vertex with ≤ 3 non-zero λ, so 3-outcome reads suffice in polygons.
- The read class searched is therefore **all finite-outcome measurements**, solved exactly by (R2) for each encoding.

**8.3 Search and convergence criteria.**
- k = 1, 2, 3: exhaustive over vertex encodings modulo the dihedral symmetry. k = 4: local search (single-string reassignments) from ≥ 2000 random starts plus structured starts.
- **Heuristic validation:** at k = 3 the local search must find the exhaustive optimum.
- **Convergence in k:** report P_rec(S, k) for k = 1–4. Call the k-supremum *converged* if P_rec(S, 4) − P_rec(S, 3) ≤ 10⁻⁴. Otherwise report a lower bound and mark it not converged.
- **Numerical tolerance:** 10⁻⁹ in the LP. Spends are reported to 10⁻⁶.
- **Cross-checks with known answers:**
  - (a) The triangle is the classical 3-simplex. Every measurement is a post-processing of the fine-grained read, so the optimiser must equal the direct value Σ_j I(X_j ; vertex index), brute-forced over all encodings.
  - (b) The square (gbit) must give 2 bits at k = 2 (two bits each read perfectly; KNOWN as the gbit random-access property).
  - (c) Values must be ≥ the committed binary-read values (pentagon 1.070431, hexagon 1.188722, octagon 1.127571, square 2.0), with equality whenever binary reads are optimal.
- **Worlds recomputed:** square, pentagon, hexagon, octagon, plus the triangle as a check.
  - Disk and ball stay at 1 bit: QM and real QM obey information causality (KNOWN, Pawłowski et al. 2009, already the committed basis), and 1 bit is attained.
  - Classical N stays at log₂N, the committed value. Its hull role is only the N = 4 tie with the square.

**8.4 Gap rule (fixed now).** Use the precise errors of §3 (OBSERVED), the recomputed spends, and the §2/Lemma G definitions with tie tolerance 10⁻⁶.
- **The gap survives** if at least one Pareto-minimal world lies above the lower convex hull by more than 10⁻⁵ in error units, with converged spends.
- **The gap closes** if every Pareto world is a hull vertex or lies within 10⁻⁵ of the hull.
- If any spend that decides the outcome is not converged, the result is **OPEN**, and the direction of the remaining uncertainty is stated.

**8.5 Admissibility of the per-record reading (open item 3), argued before the numbers.**
- The locked memory coordinate (RECORD_COST_CHAIN:64; locked in `theory/record-cost-2026-11-25/PREREG.md`) is the **total reading**: I_mem(W;S) = sup_M I(W;M), with W the joint variable of every record held. The reason given is that A6 is the mutual information of one joint distribution.
- The per-record sum Σ_j sup_{M_j} I(X_j;M_j) adds informations from readouts that need not share a joint distribution. The chain itself calls it "outside A6".
- PREREG_ADDENDUM_1 shows it is not even an extension of A6 on classical memories: a memory holding X₀⊕X₁ has A6 information 1 bit and a per-record sum of 0.
- It is **information causality used as a price** (RECORD_COST_CHAIN §6).
- **Conclusion (HYP-level reading of definitions, not a theorem):** the per-record reading is **not admissible as the memory coordinate** under the lock. It is admissible only as the chain's declared alternative column: "if that reason is judged insufficient, the coordinate on GPT memories is open, and both columns carry equal weight".
- Therefore a per-record gap would be an open miss for Ace's sentence **only in the alternative column**. Under the locked reading, the menu has one dominant world and the sentence holds trivially (§3).

## 9. C12c-G″ results (computed after §8; `c12cg/prec.py` → `prec_n{4,5,6,8}.json/.log`; `c12cg/crosscheck.py` → `crosscheck.out`; `c12cg/gap2.py` → `gap2.out`, `gap2.json`)

**9.1 The two reductions (PROVED (in-model), paper; self-checked).**
- **(R1) Vertex encodings suffice.** Fix the measurements. The channel x ↦ p(y | X_j = x) is the average of e_y(ω_s) over the strings s with bit j = x, so it is linear in the encoded states. Mutual information is convex in the channel at a fixed input law, hence convex in the states. A supremum over measurements and a sum over j preserve convexity. A convex function on a product of polygons attains its maximum at a product of vertices. ∎
- **(R2) Accessible information is an LP over effect-cone rays.**
  - I(X;Y) = Σ_y φ(e_y), with φ(e) = Σ_x ½·a_x·log₂(a_x/ā), where a_x = e(ω_x) and ā = (a_0 + a_1)/2.
  - φ is a relative-entropy form in (a, ā), which are linear in e. So φ is convex and positively homogeneous, hence subadditive.
  - The effect cone C* = {e : e(v_i) ≥ 0 ∀i} is a pointed polyhedral cone generated by its n extreme rays r_i (the facet normals of the polygon cone).
  - Writing every e_y = Σ_i μ_{y,i} r_i and splitting outcomes by ray can only raise Σ_y φ(e_y) (subadditivity). Outcomes on the same ray merge without loss (homogeneity).
  - Each split piece is a valid effect, because u − λ_i r_i is a sum of the other pieces and lies in C*.
  - So I_acc = max{Σ_i λ_i φ(r_i) : λ ≥ 0, Σ_i λ_i r_i = u}, a bounded LP whose optimum sits at a basic solution with ≤ 3 non-zero λ_i. **In a polygon, 3-outcome reads suffice for one bit.** ∎

**9.2 Cross-checks with known answers (OBSERVED, all pass).**
- (a) **Triangle = classical 3-simplex.** The effect cone has one basic solution, the fine-grained read, as it must. Over **every** encoding at k = 1, 2, 3, the LP optimiser equals the direct Σ_j I(X_j ; vertex) to within 8.9×10⁻¹⁶.
  - Side fact: the best classical N = 3 per-record value is 1.5 at k = 2 and 3, below the committed log₂3 = 1.585. The committed value is an upper bound. It does not matter here, because N = 3 is dominated either way.
- (b) **Square:** k = 2 gives exactly 2.000000 bits (the gbit random-access property).
- (c) **Never below the committed binary-read values:** square 2.0 = 2.0, hexagon 1.188722 = 1.188722, octagon 1.127571 = 1.127571, and pentagon **1.118489 > 1.070431**. The pentagon is the one world where a 3-outcome read beats every binary read.
- The local search found the exhaustive k = 3 optimum for every polygon.

**9.3 Exact per-record spends (OBSERVED for the k-supremum; exact LP value per k).**

| world | k = 1 | k = 2 (exhaustive) | k = 3 (exhaustive) | k = 4 (local, ≥ 2000 starts + lifts) | k-converged (§8.3) | committed |
|---|---|---|---|---|---|---|
| square | 1 | 2.000000 | 2.000000 | 2.000000 | yes (Δ = 0) | 2.0 |
| pentagon | 1 | 1.118489 | 1.118489 | 1.118489 | yes | 1.070431 |
| hexagon | 1 | 1.188722 | 1.188722 | 1.188722 | yes | 1.188722 |
| octagon | 1 | 1.127571 | 1.127571 | 1.127571 | yes | 1.127571 |

The optimal encodings are the same pattern at every k: two vertices per bit pair (e.g. pentagon 00→0, 01→1, 10→3, 11→2), with extra bits duplicated, which adds nothing. k ≥ 5 is not checked, so sup_k is OBSERVED stable for k ≤ 4, not proved.

**9.4 Gap decision (rule §8.4): the gap SURVIVES.**
- Pareto set: ball ≡ disk, pentagon, octagon, hexagon, square ≡ N4.
- Stake winners: ball/disk for q < 12.56, hexagon for 12.56 < q < 19.47, square/N4 for q > 19.47.
- **Unsupported Pareto worlds:** pentagon (0.0041 above the hull) and octagon (0.0008 above). Both exceed 10⁻⁵, and every deciding spend is converged.
- Cap windows: octagon for D ∈ [0.172335, 0.176393), pentagon for D ∈ [0.176393, 0.181690).
- The exact spends **widen** the pentagon's margin, because its spend rose. The hexagon's spend is exactly the committed value, so the §3 sensitivity worry ("conditional on the hexagon's P_rec being tight") is **discharged**.
- Counterfactual only: the octagon would rejoin the hull if the hexagon cost ≥ 0.02 more. The pentagon stays unsupported even at +0.03.
- **Remaining condition:** the errors. Both margins are in error units, and the errors are OBSERVED (nearest-vertex encoder; global optimality over encoders not proved). The octagon would join the hull if its true error were ≥ 0.0008 below 0.172335; the pentagon would need ≥ 0.0041 below 0.176393. The alternating optimiser converges to the nearest-vertex values from random starts (§3), which is evidence, not proof.

**9.5 Which way this points for Ace's wording ("a required accuracy is a stake in disguise").**
- **Per-record reading (the chain's alternative column; not admissible as the locked memory coordinate, §8.5):** it points **against** the unqualified wording.
  - Two worlds, the pentagon and the octagon, are the cheapest choice under an accuracy cap on named D-windows, and no stake q ≥ 0 ever selects them.
  - This is an **open miss** for the unqualified sentence. OBSERVED, conditional only on the OBSERVED errors; the spend side is now exact for k ≤ 4.
  - The sentence that survives is the hull-qualified one: *a required accuracy acts as a stake on the convex hull of the menu*, or wherever mixing (time-sharing across worlds) is allowed (Lemma A(b′)). That version is ELEMENTARY (Lemma G, §2).
- **Total reading (the locked definition):** the wording holds, but **only trivially**. One world, the square, dominates the whole menu, so cap and stake pick the same world at every D ≥ 0.125 and every q > 0.
  - That is consistent with the wording but gives it **no support**: there is nothing for the two rules to disagree about.
- **Net:** on our own menu, the evidence that bears on the sentence (from the one reading where the rules can disagree) says it needs "on the convex hull". The locked reading cannot test it.

**9.6 Labels.**
- **PROVED (in-model):** R1, R2 (3-outcome reads suffice for one bit in a polygon); Lemma G (ELEMENTARY).
- **OBSERVED:**
  - the exact LP spends per k;
  - k-convergence for k ≤ 4;
  - the cross-checks;
  - the precise errors (nearest-vertex);
  - the per-record gap {pentagon, octagon} with margins 0.0041 and 0.0008;
  - the total-reading no-gap.
- **HYP:**
  - sup_k = k ≤ 4 value;
  - global optimality of the nearest-vertex encoder for the errors;
  - the §8.5 admissibility reading (a reading of definitions, not a theorem).
- **Open miss:** the unqualified "accuracy = stake" sentence, under the per-record reading only.

**9.7 What is still open.**
1. A proof (or LP certificate) that the nearest-vertex encoder is optimal for the later-question error in the pentagon and octagon. This would make the gap PROVED (in-model) apart from sup_k.
2. sup_k for k ≥ 5, or an upper bound on P_rec(n-gon).
3. A menu with drift > 0, where the total reading has a q-flip (§6 item 4).
4. Hostile review of §§8–9.

**9.8 Rescore (§13 scale).**
- C12c-G″ is done; its remaining value is in item 1.
- **C12c-G‴ (encoder-optimality certificate):** p(certificate) 0.7 with V 2 (it upgrades an OBSERVED gap to PIM in a toy menu); p(a better encoder closes the octagon window) 0.1 with V 2. EIV 1.6 over ≈ 2 h → **≈ 0.8 per hour**. Low absolute value.
- **Rank (Lean aside):** C12c-G‴ ≈ 0.8 · C3v2 P5² cut ≈ 0.78 (outcome known; prefer an RC15 instance check on max(P5, P7)) · C1′ ≈ 0.75 (waits for the C1 review) · SR-b2 ≈ 0.67 · C12b-A ≈ 0.67 · PB ≤ 0.52 · C4R ≈ 0.2 (shelved).
- **With Lean ×3:** C12c-L ≈ 2.35 · C9 ≈ 1.2 · C12b-Lean ≈ 1.0 · SR-b-Lean ≈ 1.0.

---

## 10. C12c-G‴: is the nearest-vertex encoder optimal for the later-question error in the pentagon and octagon? (specification written about 11:05 EST, before any C12c-G‴ computation; exploratory, not hash-locked)

**10.1 Quantity.**
- e*(n) = inf over measurable encoders ω : [0, 2π) → P_n and decoders φ ↦ effect e(φ) of P(answer ≠ sign cos(θ − φ)), with θ and φ independent and uniform. The answer is "+" with probability e(φ)(ω(θ)).
- Vertex encoders suffice (linear in ω at a fixed decoder), and extreme effects suffice (linear in e at a fixed encoder).
- Nearest-vertex value (§3): e_nv(5) = 0.176393, e_nv(8) = 0.172335.

**10.2 What would count.**
- **PROVED (in-model):** a written argument (for example a rearrangement step showing optimal encoders are cyclically monotone, followed by an exact optimisation over arc lengths), or an exact dual certificate matching e_nv.
- **Better encoder found:** any encoder whose exactly evaluated error (arcs integrated exactly in θ; optimal decoder on a φ grid of ≥ 2×10⁵ points, with a second grid to confirm) is below e_nv by more than 10⁻⁶.
  - If the improvement is ≥ 0.0008 (octagon) or ≥ 0.0041 (pentagon), that world's gap window from §9.4 closes. Smaller improvements shrink the window without closing it.
- **OBSERVED only (no proof):** none of the searches below beats e_nv by more than 10⁻⁶.
  - In that case, also report any rigorous **lower** bound on e*(n) that the time allows. A lower bound above e_nv − 0.0008 (octagon) or e_nv − 0.0041 (pentagon) would make the gap PROVED (in-model) without proving nearest-vertex optimality.

**10.3 Searches (fixed now).**
- **(S1) Cyclic and free-arc encoders:** sequences of L ≤ 2n arcs with free boundaries and any vertex labels (vertices may repeat or be skipped). Optimise boundaries by Nelder–Mead from ≥ 200 random starts per n, with exact arc integration.
- **(S2) Alternating optimisation at M = 360** (committed method) from ≥ 2000 random starts, plus 500 perturbations of the nearest-vertex solution (10–30% of bins randomly relabelled). Re-evaluate the best result exactly.
- **(S3) Lower bound:** a first-level relaxation of the discretised bilinear problem, giving an LP upper bound on P(correct) (joint (vertex, effect) distributions per (θ, φ) cell with shared marginals). Report it if it is tight enough to matter; label any discretisation step.

---

## 11. Review fixes (governs §§0–9) — after `rnd/review_c12cg/HOSTILE_REVIEW_C12CG.md` (PASS-WITH-FIXES)

*Appended 26 Nov 2026 about 11:20 EST. Numbering: this was requested as §10, but §10 was already taken by the C12c-G‴ specification, which was appended before the review landed. The file is append-only, so the fixes are §11 and the C12c-G‴ results are §12. §§0–10 are left as written. Where they conflict with this section, this section governs.*

**(a) H1: wording.**
- §4's "needs 'on the convex hull'" and §9.5's surviving sentence ("a required accuracy acts as a stake on the convex hull of the menu") are **withdrawn**. C12C_ONSET §11 had already withdrawn that wording.
- Replacement, the review's H1(c) text (a suggestion for Ace's Friday wording, not an edit): *"A required accuracy acts as a stake when the menu is convex (mixtures allowed) or there is no duality gap. On a finite menu without mixing it acts as one only for supported Pareto points. In our own single-system menu, under the per-record column only, the pentagon and octagon are cap-only picks (margins 0.004 and 0.0008 in error units; errors OBSERVED, not proved optimal)."*
- This menu is **one instance** of the KNOWN convexity / duality-gap fact (Everett 1963; integer-programming duality gap; supported vs unsupported points; V6). It sits in the per-record column, which the lock does not use. **It is not evidence for the general fact**, which stands without it.
- The open miss is restated as follows: the unqualified sentence fails on this menu and task, in the alternative column only.

**(b) M1: timing of §8.** §8's heading says it was written "about 10:45, before any C12c-G″ computation". That **cannot be verified**, and it conflicts with the file times: the C12c-G″ outputs (`prec_n*.log/.json`) are stamped 10:43:19–10:43:32, before §8's stated time.
- So "spec before compute" is **not claimed** for §8.
- Mitigation: §8 was exploratory, and its rule (margin > 10⁻⁵) is far from the realised margins (4×10⁻³, 8×10⁻⁴), so the decision does not depend on when the rule was written.
- **Same check for §10:** its heading says "about 11:05". The file write that added §10 is stamped 10:58:01, and `enc_search.py` 10:58:22, so §10 did come before its computation. The time in its heading is wrong (≈ 10:58, not 11:05).

**(c) M2: prior art.**
- **Massar & Patra 2014**, "Information and communication in polygon theories", Phys. Rev. A 89:052124, 10.1103/PhysRevA.89.052124 (Crossref OK per the review). Their Protocol 3 **attains the hexagon value 1.188722**, so that spend is KNOWN as attained; C12CG adds only its OBSERVED optimality for k ≤ 5. Their conjectured monotone fall for even n (square 2 > hexagon 1.1887 > octagon 1.1276) fits.
- **Haimes, Lasdon & Wismer 1971**, the ε-constraint method, IEEE Trans. SMC SMC-1:296–297, 10.1109/TSMC.1971.4308298 (Crossref OK, no author field; authors from the paper). This is the cap half of Lemma G: a cap recovers every Pareto point, including unsupported ones.
- Janotta et al. 2011 (10.1088/1367-2630/13/6/063024) is the polygon-model source.

**(d) M3, side note for the chain: open miss.**
- Under the total reading, a pentagon state carries **≈ 1.0204 bits** (review's `rv_capacity.out`, a lower bound on the sup; Massar–Patra Theorem 2: odd n > 1 bit).
- So the log₂N identification in PREREG_ADDENDUM_1 §C **fails for odd N**, and the chain's total column "pentagon 1.70" should be ≈ 1.72.
- Logged as an **open miss for the chain** (flag for Ace; no committed file edited).
- C12CG's total-reading result is unchanged: the square still dominates.

**(e) M4: evidence for encoder reach.**
- §3's and §9.4's "converges to the nearest-vertex value… from random starts" is not supported by the committed reruns, whose start 0 *is* the nearest-vertex encoder.
- The evidence is the review's check 4:
  - **200/200 random starts** (M = 1440, no NV start) land within 10⁻⁴ of NV;
  - **1,450+ structured and free-boundary encoders** (every vertex subset and order, free arcs, random label sequences) never beat NV.
- Global optimality stays **OBSERVED / HYP**.

**(f) Lows, in brief.**
- L1: the classical N = 3 per-record value is **1.5** at k = 2…5, not log₂3; flag for the chain docstring and Addendum B.
- L2: R2 uses the **no-restriction hypothesis** (every dual-cone element below u is an effect).
- L3: §9 governs §§3–7 where they conflict (margins, the "hexagon tight" condition, §7's ranking).
- L4: the header time should be ≈ 10:45–10:46, not "11:10".
- L5: 17.6 is the **two-world** (square vs ball) crossover. On the full menu the square takes over at **19.47**.
- L6: results hold on this nine-world menu and this later-question task, with per-world spends.
- L7: the disk/ball error 1/2 − 1/π is not proved optimal. A lower true disk error only **raises** the margins, so that direction is safe.
- L8: k-convergence holds for k ≤ 5 (review's local search).
- L9: Geoffrion 1974 is "Math. Prog. Studies 2" from the volume; Crossref has no volume field.
- The review's closed forms: pentagon e = (4 − √5)/10 and octagon e = (7 − 3√2)/16 (OBSERVED to ≥ 10 digits).

## 12. C12c-G‴ results (spec §10; focus moved to a proof attempt, per the parent, with the review's check 4 as the search evidence)

**12.1 Searches (OBSERVED; `c12cg/enc_search.py` → `enc_search_n{5,8}.log/.json`).**
- **S1** (200 Nelder–Mead starts, free arcs, L ≤ 2n, any labels): the best is the cyclic NV pattern. Exact error 0.1763932145 (pentagon) and 0.1723349812 (octagon), i.e. NV + 1.2×10⁻⁸ and NV + 2.4×10⁻⁸ (boundary tolerance). **No better encoder.**
- **S2**: the M = 360 grid minima lie just below NV (0.17632, 0.17231). These are discretisation artefacts, as the review's 4D shows. My exact re-evaluation of S2's grid encoder has a bin-to-arc conversion bug (it returned 0.209 and 0.180, impossible for an encoder whose grid error is ≈ NV), so **S2 is inconclusive and not used**.
- With the review's 1,450 + 200 attempts, nothing beats NV.

**12.2 Proof attempt.**
- **Reduction (PROVED (in-model), paper, self-checked).** Write ẽ = 2e − u, so P(correct) = ½ + ½·V with V = E_φ sup_{ẽ} E_θ[s(θ − φ)·ẽ(ω(θ))], where s = sign cos.
  - The constant part of ẽ drops out, since E_θ s = 0.
  - The admissible linear parts are exactly D° = the polar of D := (P − P)/2. The condition |ẽ(v)| ≤ 1 on all vertices is width_P(w) ≤ 2, i.e. h_D(w) ≤ 1.
  - Hence **V = sup over vertex-valued r(·) of E_φ ‖g(φ)‖_D**, with g(φ) = E_θ[s(θ − φ) r(θ)] and ‖·‖_D the gauge of D.
  - Even n: D = P. Odd n: D is a regular 2n-gon (the pentagon gives a decagon).
  - In Fourier form, V = Re Σ_{m odd} ŝ_m r̂_m conj(f̂_m), with |ŝ_m| = 2/(π|m|).
  - NV values: V = (1 + √5)/5 = 0.64721 (pentagon) and (1 + 3√2)/8 = 0.65533 (octagon), from the review's closed forms.
- **Bound tried (PROVED (in-model) as an inequality; `fourier_bound.py`, `fourier_bound2.out`).**
  - Constraints: Σ|r̂_m|² ≤ 1; |r̂_{±1}| ≤ σ_n (mean support of P = n sin(π/n)/π); |r̂_1| + |r̂_{−1}| ≤ κ_P; the matching constraints for f in D°; then Cauchy–Schwarz on the harmonics |m| ≥ 3.
  - Result: e ≥ 0.1558 (pentagon) and e ≥ 0.1555 (octagon).
  - What the gap needs (e ≥ e_NV − margin): **0.17226** (pentagon) and **0.17153** (octagon). **Not enough, by 0.016–0.017.**
  - Even granting a HYP stability lemma (residual harmonics only at the aliasing orders |m| ≥ 7 or 9), the bound does not reach: 0.1567 and 0.1555.
- **Why this route fails (named obstruction).** Magnitude bounds on harmonics discard the phase alignment between encoder and decoder. The slack sits in splitting energy between the m = +1 and m = −1 harmonics, and Cauchy–Schwarz on that split loses ≈ 0.03 in V. NV is within 0.0016 of what the gap needs, so a certificate must be pointwise, not spectral.
- **The step that would finish it (HYP, not done): a cyclic-monotonicity (rearrangement or exchange) lemma.** Some optimal vertex-valued encoder visits the vertices in cyclic order, one arc each.
  - Given that lemma, the problem is a smooth n-parameter optimisation over arc lengths. The review's search (A) already finds NV to 2×10⁻⁹ there, and by dihedral symmetry plus a second-order check that could be made exact.
  - The lemma is plausible: in the D-gauge form, an out-of-order pair of arcs should be improvable by swapping them, since ‖g‖_D is convex in r and g is a convolution with a monotone-on-half-circle kernel. But no swap inequality is proved.

**12.3 Result and labels.**
- **NV optimality: still HYP** (OBSERVED: S1 here, plus the review's 1,450 + 200 attempts).
- **No better encoder** (OBSERVED).
- **Proved:** the D-gauge reduction, and a lower bound e ≥ 0.155–0.156 that is **too weak to certify either window**.
- **The per-record gap stays OBSERVED, conditional only on NV optimality.** It is unchanged in content, and still an instance in the alternative column, not evidence for the general fact (§11(a)).

**12.4 Open.**
1. The cyclic-monotonicity lemma (the crux).
2. An exact arc-length optimisation with a second-order certificate, once (1) holds.
3. Alternatively, a rigorous discretised dual (LP) bound fine enough for a 0.0008 margin. That needs M ≳ 10³ in each angle; the size is impractical with the first-level relaxation.
4. The S2 conversion bug (low; S2 is not used).

**12.5 Rescore.**
- **C12c-G⁗ (prove the monotonicity lemma):** p(proof) 0.35, V 2 (it upgrades an instance that the review has already ruled is not evidence for the general sentence); p(counterexample) 0.05, V 2; EIV 0.8 over ≈ 3 h → **≈ 0.27 per hour**. Below the bar, so **parked**.
- The C12c line is done for now. Its useful outputs are §11(a)'s wording and the chain flags (§11(d), (f) L1, L5).

*§12.2 precision note (appended):* in V units, the gap needs V ≤ 0.65548 (pentagon) and V ≤ 0.65694 (octagon), against NV values of 0.64721 and 0.65533. So the slack is 0.0083 (pentagon) and 0.0016 (octagon). The proved bound gives V ≤ 0.6883 and 0.6891, which overshoots by ≈ 0.033.
