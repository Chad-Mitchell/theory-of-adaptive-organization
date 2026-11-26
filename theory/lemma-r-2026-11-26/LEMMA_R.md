<!-- Repository copy, added 26 Nov 2026. The note below is reproduced as written, with its appended review corrections (§9). Paths in it refer to the R&D working folders: `lemma_r/…` and `rnd/review_lemma_r/…` correspond to the files in this directory. PREREG_P, NOTE_P, STEPBACK and PREREG_DRAFT_C3v2 are R&D session notes that are not in this repository. Status source: ledger row RC20 in `measurement/CLAIM_MAP_v2.md`. -->

# Lemma R: maps that keep pure products pure in polygon composites are local ⋊ swap

*R&D note, 26 Nov 2026. Not a repo file and not a CLAIM_MAP row. Written for a fresh reviewer: every step is numbered so it can be checked on its own.*
Labels: PROVED (in-model) = every step written here, self-checked, not independently reviewed, not formalized · OBS = numerical · KNOWN = prior art · HYP.
Scripts: `lemma_r/lemma_r_check.py` → `lemma_r/lemma_r_check.out`; `lemma_r/crossref_lemma_r.py` → `.txt`.

## 0. Status in one paragraph
**Lemma R is PROVED (in-model) for any two polygons with ≥ 4 vertices each, in every composite between min and max.**
- **Scope:** no regularity is needed. Neither the composite nor local symmetry is used.
- **Sharpness:** the hypothesis "≥ 4 vertices" cannot be dropped. With a bit (2 vertices) or a trit (3 vertices) as one part, correlating controlled maps exist (OBS: 200 vs 20 maps for bit × pentagon; 6000 vs 60 for trit × pentagon).
- **Combined with RC15:** every locally symmetric composite of two regular polygons with n ≥ 4 has Aut(S) = local ⋊ swap. So every product start is rigid: no Θ(1, 0) at any start entropy. This inherits RC15's status (PROVED (in-model), a parallel worker's self-check, not independent, not formalized).
- **Prior art:** the second half of the proof is the same structure as Al-Safi–Richens 2015 Lemma 2 (KNOWN). The first half, a dimension lemma, is an elementary finite-set analogue of the Marcus–Moyls rank-one argument. I did not find this exact statement in print; **novelty is not claimed.**

## 1. Setting and definitions
- **S1 (parts).** For X ∈ {A, B}, Ω_X is a polygon (a compact convex 2-dimensional polytope) with vertex set {x_1, …, x_{n_X}}, n_X ≥ 4. Each vertex is written in homogeneous coordinates: x = (1, p) ∈ V_X = ℝ³, with p ∈ ℝ² the vertex position. So K_X = dim V_X = 3, and unit effect u_X = first coordinate.
- **S2 (fact about vertices).** Any 3 distinct vertices of a polygon are linearly independent in V_X.
  - *Proof:* (1, p), (1, q), (1, r) are dependent iff p, q, r are collinear.
  - Distinct vertices of a convex polygon are extreme points; if three were collinear, the middle one would be a convex combination of the other two. ∎
  - Consequences: any two distinct vertices are non-parallel, and the vertices span V_X.
- **S3 (product vectors).** P = {a_i ⊗ b_j} ⊂ V_A ⊗ V_B (the pure product states). The map (i, j) ↦ a_i ⊗ b_j is injective: a ⊗ b = a′ ⊗ b′ with all first coordinates equal to 1 forces a = a′ and b = b′.
- **Lines.** Row R_i = {a_i ⊗ b_j : j}, with |R_i| = n_B and span R_i = a_i ⊗ V_B (dim 3). Column C_j = {a_i ⊗ b_j : i}, with |C_j| = n_A and span C_j = V_A ⊗ b_j (dim 3).
- **Mixed set.** A set Y ⊆ P is *mixed* if it lies in no single row and no single column. Equivalently, Y contains two elements with different A-index and two elements (possibly the same ones) with different B-index.
- **"≥ 3 dims" made precise.** "A mixed set spans ≥ 3 affine dimensions" means: every mixed Y ⊆ P with |Y| = 4 is linearly independent (linear rank 4, affine dimension 3). That is Lemma D below.
- **"Preserves products".** A linear bijection T: V_A ⊗ V_B → V_A ⊗ V_B with T(P) = P, i.e. T maps pure product states onto pure product states. Because P is finite and T is injective, T(P) ⊆ P already implies T(P) = P.
- **"Local ⋊ swap".** Either
  - (i) T = g_A ⊗ g_B with g_X ∈ Aut(Ω_X), a linear bijection of V_X mapping Ω_X onto Ω_X; or
  - (ii) Ω_A and Ω_B are affinely isomorphic and T = (h ⊗ k) ∘ SW, where SW(x ⊗ y) = y ⊗ x, and h: V_B → V_A and k: V_A → V_B are linear bijections with h(Ω_B) = Ω_A and k(Ω_A) = Ω_B.
  - After identifying B with A, case (ii) is "local ∘ swap".
- **Composites (used only in §4).** min = conv(P); max = {s : s(e ⊗ f) ≥ 0 for all effects e of A and f of B, and s(u ⊗ u) = 1}; S closed convex with min ⊆ S ⊆ max. "Entangled" means not in min. Aut(S) = linear bijections of V_A ⊗ V_B mapping S onto S.

## 2. Lemma D (dimension). Under S1–S3, every mixed 4-set Y ⊆ P is linearly independent.
**D.1 (claim).** Let Z = {a_{i_k} ⊗ b_{j_k}}, k = 1…m, be m ≤ 4 distinct elements of P with Σ c_k a_{i_k} ⊗ b_{j_k} = 0 and every c_k ≠ 0. Then Z lies in one row or one column.

*Proof.* Let I′ be the set of distinct A-indices in Z, and p = |I′|. Group terms by A-index: Σ_{i ∈ I′} a_i ⊗ β_i = 0, where β_i = Σ_{k : i_k = i} c_k b_{j_k}. Within one group the j_k are distinct, by S3.
- **p = 1:** Z lies in a row. Done.
- **2 ≤ p ≤ 3:** the a_i, i ∈ I′, are independent by S2. Extend them to a basis of V_A and apply (dual functional) ⊗ id to get β_i = 0 for every i.
  - Group i has m_i ≤ m − (p − 1) ≤ 3 terms, all with nonzero coefficients on distinct b's.
  - By S2, ≤ 3 distinct b's are independent, so β_i ≠ 0. Contradiction: this case cannot occur.
- **p = 4** (so m = 4, all A-indices distinct): four vectors in ℝ³, any three of them independent (S2). Write a_{i_4} = Σ_{k ≤ 3} λ_k a_{i_k}.
  - Every λ_k ≠ 0; otherwise a_{i_4} and two of the others would be dependent.
  - Substituting gives Σ_{k ≤ 3} a_{i_k} ⊗ (c_k b_{j_k} + c_4 λ_k b_{j_4}) = 0. Independence of a_{i_1}, a_{i_2}, a_{i_3} gives c_k b_{j_k} = −c_4 λ_k b_{j_4} for k = 1, 2, 3.
  - The right side is nonzero, so b_{j_k} ∥ b_{j_4}. By S2, j_k = j_4. So Z lies in column C_{j_4}. ∎

**D.2 (the lemma).** Suppose a mixed Y with |Y| = 4 were dependent.
- Take a nontrivial relation and let Z ⊆ Y be its support (all coefficients nonzero).
- By D.1, Z lies in a row or a column. Inside one row or column, ≤ 3 distinct elements are independent (S2, transported by a ⊗ · or · ⊗ b), so |Z| = 4 and Z = Y.
- Then Y lies in a row or column, contradicting "mixed". ∎

Note: K = 3 is used only in case p = 4 of D.1.

## 3. Lemma R. Under S1–S3, every linear bijection T with T(P) = P is local ⋊ swap.
- **R.1 (lines go into lines).** Let L be any line (a row or a column). X := T(L) has |X| = |L| ≥ 4, and dim span X = dim span L = 3, since T is injective.
  - Suppose X were mixed. Pick x, y ∈ X with different A-index and x′, y′ ∈ X with different B-index. Y₀ = {x, y, x′, y′} is mixed with |Y₀| ≤ 4.
  - Pad Y₀ with elements of X up to 4 elements (possible since |X| ≥ 4). Padding keeps it mixed, so by Lemma D it is independent, giving dim span X ≥ 4. Contradiction.
  - So X lies in a single line L′.
- **R.2 (lines go onto lines; τ is a bijection).** T⁻¹ is also a linear bijection with T⁻¹(P) = P, so R.1 applies to it: T⁻¹(L′) ⊆ L″ for some line L″.
  - Then L = T⁻¹(X) ⊆ T⁻¹(L′) ⊆ L″. A line containing another line of ≥ 2 elements equals it: two distinct rows (or two distinct columns) are disjoint, and a row and a column share one point. So L″ = L.
  - Hence T⁻¹(L′) ⊆ L, so L′ ⊆ T(L) = X ⊆ L′, and T(L) = L′.
  - So T induces a map τ on lines with T(L) = τ(L). τ is injective because T is, and bijective because T⁻¹ induces its inverse.
- **R.3 (incidence).** Distinct rows are disjoint, distinct columns are disjoint, and a row meets a column in exactly one point. τ preserves "disjoint" and "meets", because T is a bijection of P.
  - **Case 1: τ(R_1) is a row.**
    - For i ≠ 1, τ(R_i) is disjoint from the row τ(R_1). Every column meets every row, so τ(R_i) is a row.
    - τ restricted to rows is injective into a set of n_A rows, so it is onto the rows.
    - A column C meets every row, so τ(C) meets every row. If τ(C) were a row it would be disjoint from the other n_A − 1 ≥ 1 rows. So τ(C) is a column.
  - **Case 2: τ(R_1) is a column.** By the same argument, rows go to columns and columns go to rows. Injectivity both ways gives n_A = n_B.
- **R.4 (Case 1 ⇒ (i)).** Write τ(R_i) = R_{α(i)} and τ(C_j) = C_{β(j)}. Then T(a_i ⊗ b_j) ∈ R_{α(i)} ∩ C_{β(j)} = {a_{α(i)} ⊗ b_{β(j)}}.
  - Since T(V_A ⊗ b_1) = span T(C_1) = V_A ⊗ b_{β(1)}, and v ↦ v ⊗ b_{β(1)} is a linear injection onto V_A ⊗ b_{β(1)}, there is a unique linear g_A with T(v ⊗ b_1) = g_A(v) ⊗ b_{β(1)}. It satisfies g_A(a_i) = a_{α(i)}. Likewise there is g_B with g_B(b_j) = b_{β(j)}.
  - T and g_A ⊗ g_B agree on {a_i ⊗ b_j}, which spans V_A ⊗ V_B (S2), so T = g_A ⊗ g_B.
  - g_A maps the vertex set onto itself, so it is onto V_A (a bijection) and maps Ω_A = conv(vertices) onto Ω_A. Same for g_B. ∎(i)
- **R.5 (Case 2 ⇒ (ii)).** Write τ(R_i) = C_{β(i)} and τ(C_j) = R_{α(j)}, so T(a_i ⊗ b_j) = a_{α(j)} ⊗ b_{β(i)}.
  - As in R.4, T(a_1 ⊗ w) = h(w) ⊗ b_{β(1)} defines a linear h: V_B → V_A with h(b_j) = a_{α(j)}.
  - T(v ⊗ b_1) = a_{α(1)} ⊗ k(v) defines a linear k: V_A → V_B with k(a_i) = b_{β(i)}.
  - T and (h ⊗ k) ∘ SW agree on a spanning set, so they are equal. h maps the vertices of Ω_B onto those of Ω_A, so Ω_B ≅ Ω_A. ∎(ii)

**Converse (trivial).** Every local ⋊ swap map sends P onto P.

## 4. From Lemma R to "rigid"
- **Corollary R1 (dichotomy).** Assume S1 and that each part has all effects (no-restriction: the effect cone is the dual of the state cone). Let min ⊆ S ⊆ max. Then every T ∈ Aut(S) either sends some pure product to an entangled state, or satisfies T(P) = P.
  - **E1 (pure products are extreme in max).** Each vertex a is exposed: there is an effect e_a with e_a(a) = 1 and e_a < 1 elsewhere on Ω_A (a polygon vertex has a supporting line meeting Ω_A only at a; no-restriction makes e_a an effect).
    - Let s ∈ max and f an effect of B. The functional φ_f(e) := s(e ⊗ f) is nonnegative on all A-effects, so φ_f lies in the bidual, which is the closed state cone of A.
    - Its normalisation is the marginal s_A := φ_u, so s_A ∈ Ω_A.
    - If a ⊗ b = λs + (1 − λ)t with s, t ∈ max and 0 < λ < 1, apply e_a ⊗ u: e_a(s_A) = e_a(t_A) = 1, so s_A = a.
    - Then φ_f + φ_{u−f} = a, which spans an extreme ray, so φ_f = s_B(f)·a for every f. Product functionals span (V_A ⊗ V_B)*, so s = a ⊗ s_B.
    - Repeating with e_b gives s_B = b, so s = a ⊗ b, and likewise t. Hence a ⊗ b is extreme in max, and so in S ⊆ max.
  - **E2 (separable extreme points are pure products).** If x is extreme in S and x ∈ min = conv(P), then x is a convex combination of points of P ⊆ S, so x ∈ P.
  - **E3.** T ∈ Aut(S) maps extreme points to extreme points. If T(P) ⊆ min, then by E2 T(P) ⊆ P, and so T(P) = P. Otherwise some T(a ⊗ b) is entangled. ∎
- **Corollary R2 (with RC15).** Let both parts be regular polygons with n_A, n_B ≥ 4 and all effects, and let S be a closed convex composite between min and max that is invariant under D_{n_A} × D_{n_B} (local maps stay reversible) and has finite orbits.
  - RC15 (Theorem M12 + disk lemma; CLAIM_MAP RC15) gives: no T ∈ Aut(S) sends a pure product to an entangled state.
  - By R1, T(P) = P. By Lemma R, T is local ⋊ swap. So **Aut(S) = D_{n_A} × D_{n_B}, ⋊ swap when n_A = n_B and S is swap-invariant.**
  - Status: PROVED (in-model) *conditional on RC15*. RC15 is itself PROVED (in-model) but is a parallel worker's self-check, not independent, not formalized.
- **Corollary R3 (rigid).** In such an S, from any product start ω_A ⊗ ω_B (pure or mixed), every reversible step keeps the state a product (R2, E-L0).
  - For any read on A and any read on B, p(x, y) = p_A(x)·p_B(y). The best guess of x from y succeeds with probability max_x p_A(x).
  - If A's outcome has entropy ≥ 1 bit, max_x p_A(x) < 1, so Θ(1, 0) (PREREG_P, ε = 0) is infeasible at every start entropy: **rigid**.
  - Caveat for ε = 0.01: max p_A ≥ 0.99 together with H ≥ 1 bit needs about 2⁹² or more outcomes. So "rigid" holds at ε = 0.01 for reads with fewer outcomes; I did not prove it for unbounded reads.

## 5. Sanity checks (not tests)
OBS numerical, float tolerance 1e-9. These numbers come from `lemma_r_check.out`.
- **"Linear maps with T(P) = P"** is the number of permutations of P that extend to a linear map. They are found by a K-matrix backtracking search (the repository's method: K_ij = x_iᵀ(Σ x x ᵀ)⁻¹ x_j, Bremner et al. 2014 as cited in ROUND10 §15), and each one is rebuilt and checked as a linear map.
- **"Lines → lines"** counts the maps that send every row and column to a row or column, i.e. the local ⋊ swap shape.

| parts | dependent mixed 4-sets | #T with T(P) = P | lines → lines | expected local ⋊ swap | covered by Lemma R? |
|---|---|---|---|---|---|
| square² | 0 / 1812 | 128 | 128 | 8·8·2 = 128 | yes |
| pentagon² | 0 / 12600 | 200 | 200 | 200 | yes (C3v2) |
| hexagon² | 0 / 58725 | 288 | 288 | 288 | yes |
| heptagon² | 0 / 211386 | 392 | 392 | 392 | yes |
| square × pentagon | 0 / 4820 | 80 | 80 | 80 | yes |
| pentagon × heptagon | 0 / 52150 | 140 | 140 | 140 | yes (C3v2) |
| bit × pentagon | 0 / 200 | **200** | 20 | 20 | **no** (n_A = 2) |
| trit × pentagon | 0 / 1350 | **6000** | 60 | 60 | **no** (n_A = 3) |
| bit² | 0 / 1 | **24** | 8 | 8 | no |
| octahedron² (K = 4) | 0 / 58725 | 4608 | 4608 | 48·48·2 | no (not a polygon) |

Readings:
- **square², hexagon².** Lemma R agrees, and so does the repository's group-order table (Aut = local ⋊ swap for min and max). Al-Safi–Richens Theorem 1 already gives "all reversible maps trivial" for max of even (dichotomic) polygons (KNOWN). Lemma R adds every intermediate composite, but only for maps that preserve products.
- **RC15.** It covers entangling maps; Lemma R covers the complement. Together they give R2. There is no tension: RC15's statement does not mention correlating maps, and those are exactly what Lemma R rules out.
- **Where the hypothesis bites.** In the excluded rows (bit or trit as a part), the extra maps are the classical controlled maps (Al-Safi–Richens' "conditional transformations"; the PREREG_P classical case; C3v2's G3a control).
  - Proof step that fails: R.1 needs |L| ≥ 4. A column of bit × pentagon has 2 elements, and a mixed 2-set spans 2 = K_A dimensions. A column of trit × pentagon has 3 elements, and a mixed (diagonal) 3-set spans 3 = K_A.
  - **This boundary is sharp for polygons:** a polygon with fewer than 4 vertices is a segment or a triangle, i.e. a classical bit or trit.
- **Stabilizer: correctly not covered.** Its parts are octahedra (K = 4, not polygons) with restricted effects, so S1 and R1's no-restriction both fail.
  - Its "free" outcome comes from an entangling map: CNOT sends |+⟩|0⟩ to a Bell state. That is a non-product-preserving map, outside Lemma R in any case.
  - The linear product preservers of octahedron² are 4608 = local ⋊ swap (OBS). So a Lemma-R-type statement plausibly holds for octahedra too (HYP), but it does not touch the stabilizer's free outcome.
- **QM: not covered** (Bloch balls, infinitely many pure states). The QM analogue is KNOWN: Friedland–Li–Poon–Sze 2011, Theorem 3. A linear map with Ψ(P_m ⊗ P_n) = P_m ⊗ P_n is a product of unitary conjugations, optionally transposed, or that composed with swap when m = n.
  - QM is "free" because it has entangling maps (the RC15 step fails), not because of anything in Lemma R.

## 6. Prior art (DOIs verified on Crossref, `lemma_r/crossref_lemma_r.txt`)
- **Al-Safi, Richens 2015, NJP 17:123001 (10.1088/1367-2630/17/12/123001)**, read from arXiv:1508.03491:
  - Lemma 2: adjacency-preserving reversible maps of a max tensor product are trivial. This is the same structure as my R.2–R.5, stated for effects in max composites.
  - Theorem 1: max composites of non-classical dichotomic parts are trivial; this includes even polygons.
  - Theorem 3: max composites of identical odd polygons are trivial.
  - Theorem 2 + Conjecture 1: reducible parts allow conditional maps.
  - Their Discussion (arXiv text lines 556–564) says that extending to non-max composites is the main obstacle.
  - **So KNOWN:** rigidity of max(P5, P5) and of max of even polygons. **Not covered there:** intermediate composites, and non-identical odd pairs such as max(P5, P7) (odd polygons are not dichotomic, and Theorem 3 needs identical parts).
- **Gross, Müller, Colbeck, Dahlsten 2010, PRL 104:080402 (10.1103/PhysRevLett.104.080402)** and **Al-Safi, Short 2014, J. Phys. A 47:325303 (10.1088/1751-8113/47/32/325303):** boxworld reversible maps are trivial (Hamming/adjacency argument).
- **Marcus, Moyls 1959, Pacific J. Math. 9:1215 (10.2140/pjm.1959.9.1215)** and **Westwick 1967, Pacific J. Math. 23:613 (10.2140/pjm.1967.23.613):** linear maps preserving all rank-one tensors are A ⊗ B or composed with swap. Lemma R is a finite-configuration analogue: it preserves a finite spanning set of rank-one tensors, not all of them. Lemma D plays the role of their Lemma 1, which is Al-Safi–Richens' Lemma 4.
- **Friedland, Li, Poon, Sze 2011, JMP 52:042203 (10.1063/1.3578015); Alfsen, Shultz 2010, JMP 51:052201 (10.1063/1.3399808); Johnston 2011, Lin. Multilin. Alg. (10.1080/03081087.2011.596540):** QM preservers of product pure states and of separable states.
- Not found: a statement of Lemma R for finite polytope parts in arbitrary composites. A reviewer should search "linear preservers of finite sets of decomposable tensors" and "automorphisms of Segre products of point configurations". It may well be folklore.

## 7. What it settles and what stays open
- **C3v2 family** (P5², P5 × P7 orbit unions, all locally symmetric with finite orbits): by R2 + R3, **every member is rigid**, Aut(S) = local group (⋊ swap for P5²), free = 0 and fuel-needing = 0.
  - C3v2's Arm 2 is therefore theorem-fixed, conditional on RC15. A run would be an instance check of RC15 + Lemma R: V = 2, with p(miss) ≈ p(RC15 or R wrong) ≈ 0.05.
  - New EIV ≈ 0.95·2 + 0.05·9 ≈ 2.35 over 5 h ≈ **0.47 per hour** (P5² cut: 2.35/3 ≈ 0.78 per hour). **Do not run C3v2 Arm 2 as a prereg.** If an independent check is wanted, an exact RC15 + R instance check on max(P5, P7) alone is the useful one, because that case is not covered by Al-Safi–Richens.
- **Conjecture C:** **Lemma R settles none of it.** C is about entangling maps, and Lemma R is about the other class. What it does is upgrade every polygon case where C is proved (RC15) from "no entangling map" to "all reversible maps trivial".
  - So for polygon parts with n ≥ 4, in locally symmetric composites, even classical-like correlation cannot be generated. Premise I of E-L0 fails there outright, so these worlds cannot track at all.
  - This does not derive QM, the arrow, time, or "tracking never finishes" (RECORD-COST-U stays an open miss).
- **Still open:**
  1. Composites that are not locally symmetric. Lemma R and R1 still apply there; only the RC15 step is missing.
  2. Three or more parts (HYP: an n-part Lemma R via the same incidence argument; not written).
  3. Parts of dimension ≥ 3 (HYP R′). Octahedron² agrees numerically. The square pyramid × square is a known boundary (Al-Safi–Richens Theorem 2 and the repository table): 4 coplanar base vertices make a dependent 4-set, so the analogue of S2 fails.
  4. Restricted-effect parts (R1 fails).
  5. The entangling-map premise of C.

## 8. For the reviewer: where to push
- **D.1 case p = 4:** this uses K_A = 3, so it is where a higher-dimensional extension would break.
- **R.2:** "a line containing a line equals it" uses |L| ≥ 2.
- **R1/E1:** this uses no-restriction twice: for the exposing effect, and for "φ_f is in the state cone".
- **R3:** the ε = 0.01 caveat.
- **The numerics** use floats with tolerance 1e-9, not exact arithmetic. They are OBS only, and the proof does not depend on them.

---

## 9. Corrections after the hostile review (appended; §§0–8 above are left as written)
Source: `rnd/review_lemma_r/HOSTILE_REVIEW_LEMMA_R.md` (outcome PASS-WITH-FIXES, no high findings), with `exact_check.py` → `exact_check.out`, an independent exact check in Q(√5). Where this section disagrees with §§0–8, this section holds.

**C9-1 (M1): the ε = 0.01 caveat in R3 and §8 is false, not merely unproved.**
- PREREG_P's Θ(h, ε) puts no cap on the number of outcomes of the read r_A.
- Counterexample: with all effects, take the state-ignoring read {0.99·u, 0.01·u/(N − 1), …, 0.01·u/(N − 1)}. Its outcome entropy is h(0.99) + 0.01·log₂(N − 1), which is ≥ 1 bit once N − 1 ≥ 2^91.92. B's constant guess "outcome 0" succeeds with probability 0.99.
- So with unbounded reads, Θ(1, 0.01) is feasible in every theory, from every state, with no correlation at all.
- **Corrected R3:**
  - At ε = 0, rigid with no cap.
  - At ε = 0.01, rigid only for reads with M outcomes where M − 1 < 2^91.92. Proof: success ≥ 0.99 under a product state forces max p_A ≥ 0.99, so H ≤ h(0.99) + 0.01·log₂(M − 1) < 1. This includes every binary read.
- Consequences recorded elsewhere:
  - `rnd/entangle/NOTE_PREREG_P_EPS.md` (separate note; the locked PREREG_P.md is not edited), with a pointer in NOTE_P.md's DEVIATIONS;
  - the read cap in `PREREG_DRAFT_C3v2.md`, appended before any lock.

**C9-2 (M2): full premise list for R2 and R3. It replaces the short form in §0 bullet 3 and in §7.**
R2 and R3 hold only under all of the following:
1. two parts only;
2. each part a regular polygon with n ≥ 4 vertices;
3. **all effects** on each part (needed for R1);
4. a closed convex composite S with min ⊆ S ⊆ max, **invariant under D_{n_A} × D_{n_B}**, with **finite orbits** (needed for RC15);
5. "reversible step" means an element of Aut(S) acting on the pair alone: no ancilla, no third part, no measurement or conditioning, and no mixture of reversible maps (shared randomness would give separable correlated states);
6. ε = 0, or reads capped as in C9-1;
7. RC15's own status: a parallel worker's self-check, not independent, not formalized.

§7's phrase "these worlds cannot track at all" is withdrawn. It reads instead: **"no reversible map of the pair alone can correlate the two parts"**, under premises 1–7. Three or more parts, ancillas, and the repeated task Θ_T stay open.

**C9-3 (M3): prior art.**
- (a) **Open Quantum Problem #42, "Reversible dynamics on composite systems"** (B. Dakić and M. Müller, added 2017-05-20; IQOQI Vienna list, https://oqp.iqoqi.oeaw.ac.at/reversible-dynamics-on-composite-systems, read this session).
  - It asks: if Ω_A and Ω_B have pure-state-transitive reversible groups, and a locally tomographic composite has a reversible map not of the form T_A ⊗ T_B (one that creates correlations), must the theory embed in complex quantum theory?
  - **R2 is a partial case:** for regular polygons with n ≥ 4 (D_n is transitive on vertices), in invariant composites with finite orbits and all effects, Aut(S) contains no correlating map. So the hypothesis of #42 is never met, and the conjecture holds there vacuously. The one non-local map that remains is swap, which creates no correlation.
  - The whole entangling half of R2 rests on RC15, so RC15 is where scrutiny should go.
  - The OQP page lists composites strictly between min and max as open in general. This is a partial case only, and novelty is not claimed.
- (b) **R.3 is the automorphism group of the rook's graph** K_{n_A} □ K_{n_B}: S_{n_A} × S_{n_B}, or (S_n × S_n) ⋊ Z₂ when n_A = n_B. It is standard graph theory and is attributed to Harary 1958, Pacific J. Math. 8:743–755, DOI 10.2140/pjm.1958.8.743. I verified the DOI on Crossref (`lemma_r/crossref_lemma_r_fix.txt`) but **did not read the paper**. The Hamming and adjacency argument of Gross et al. 2010 and Al-Safi–Richens Lemma 2 is the same idea, applied to effects.
- (c) §6's sentence "Lemma D plays the role of their Lemma 1, which is Al-Safi–Richens' Lemma 4" is replaced by: **Lemma D uses the same technique (the dual-functional step) as Marcus–Moyls Lemma 1 = Al-Safi–Richens Lemma 4.** That lemma is a span statement; Lemma D is a finite independence statement.
- (d) **Bremner et al. 2014**, "Computing symmetry groups of polyhedra", LMS J. Comput. Math. 17:565–581, **DOI 10.1112/S1461157014000400**, verified on Crossref. It replaces the §5 remark "cited without DOI".
- **Assessment (adopted from the review):** Lemma R combines three standard pieces:
  1. the Marcus–Moyls dual-functional step;
  2. "lines go to lines";
  3. the rook's-graph automorphisms, followed by linear extension.

  It is **folklore-level, and novelty is not claimed.**

**C9-4 (L1): where K = 3 is used.**
- §2's note and §8's first bullet are wrong. In D.1 case p = 4, if the four a's are independent (possible when K_A ≥ 4), every β_i = 0 at once, which is a contradiction. Otherwise the written argument applies.
- So **Lemma D holds for any two polytopes, in any dimension.** The review's exact check agrees: 0 dependent mixed 4-sets out of 634256 for cube², and 0 out of 4820 for square pyramid × square.
- **K = 3 is used in R.1:** a line spans K = 3 dimensions, which is less than 4, the rank of a mixed 4-set.
- A K ≥ 4 extension (HYP R′) needs a different lemma: "no mixed set of at least |L| points spans only K dimensions". That already fails for mixed 5-sets in octahedron² (4 coplanar equator vertices in one column plus any fifth point), even though lines → lines holds there numerically.
- §7 item 3's explanation for the square pyramid is corrected: its conditional maps come from **reducibility** (Al-Safi–Richens Theorem 2), not from a failure of Lemma D.

**C9-5 (L3, L5): effects.**
- Aut(Ω_X) in Lemma R is state-only. That is enough under all effects, where the effect set is the dual cone and is preserved automatically.
- A restricted-effect extension must also check that effects are preserved.
- If composite effects were restricted below the dual of S, the physical group could only be smaller. So "⊆ local ⋊ swap" still holds.

**C9-6 (L4 and numerics).**
- The float script reruns byte-identically (`review_lemma_r/rerun_float.out`).
- The exact Q(√5) check confirms 128 / 200 / 80 / 200-vs-20 exactly. Every permutation that preserves K was exactly linear.
- The trit count 6000 = 10³·3! (that is, (D5)³ ⋊ S3) is float only.

**C9-7: labels (exactly as the review recommends).**
- **Lemma D:** PROVED (in-model) for any two polytopes (not only polygons). Hostile-reviewed once. Not formalized.
- **Lemma R** (polygons with ≥ 4 vertices each, any linear bijection with T(P) = P): **PROVED (in-model), hostile-reviewed once (PASS), not formalized; elementary; folklore-level (Marcus–Moyls dual-functional step + rook's-graph automorphisms), novelty not claimed.** It is a Lean candidate (spec: `LEMMA_R_LEAN_SPEC.md`).
- **R1:** PROVED (in-model) under all effects. Hostile-reviewed once.
- **R2 and R3:** PROVED (in-model) **conditional on RC15** (a self-check, not independent).
  - Scope: two regular polygon parts with n ≥ 4, all effects, a composite invariant under the local groups with finite orbits, two parts acting alone, and ε = 0 (or capped reads at ε = 0.01).
  - Relation to Open Quantum Problem #42 as stated in C9-3(a).
- **C3v2 Arm 2:** "theorem-fixed conditional on RC15". The useful independent check is an exact RC15 instance check on max(P5, P7).
