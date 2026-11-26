# Hostile review: LEMMA_R.md, STEPBACK.md §14, lemma_r/ scripts

*R&D note, 26 Nov 2026, 07:25 ET. Independent reviewer. I did not write the target. Local notes only: no repo file changed, no commit, no push. THEORY.md, CORE.md and locked files were not touched.*

Targets: `rnd/stepback/LEMMA_R.md` (07:08 ET), `rnd/stepback/STEPBACK.md` §14, `rnd/stepback/lemma_r/lemma_r_check.py` and `.out`.

My files (all in this folder):
- `exact_check.py` → `exact_check.out`: independent code with exact arithmetic in Q(√5), using pairs of Fractions.
- `rerun_float.out`: a rerun of the author's script.
- `crossref_review.txt`: my Crossref lookups.
- `rsa2017.pdf/.txt`: Richens–Selby–Al-Safi, from arXiv:1705.08028.

Labels: PROVED (in-model) · OBS (numerical) · KNOWN (prior art) · HYP.

## Overall: **PASS-WITH-FIXES**

- **Lemma R** (Lemma D plus R.1–R.5) holds up step by step. I found no gap in the logic.
- **The dichotomy (R1, with E1–E3)** holds under its stated premise: all effects on each part.
- **The RC15 combination (R2, R3)** is inherited honestly. It brings in no extra premise beyond RC15's own hypotheses, which LEMMA_R's §4 spells out. But the one-paragraph status in §0 drops two of them.
- **Fixes needed:**
  - the ε = 0.01 caveat, which understates the problem (med);
  - the status scope (med);
  - the prior-art framing, which omits Open Quantum Problem #42 and the rook's-graph fact (med);
  - the §14 tally (med).
- **High findings:** none.

## A. Step-by-step check of Lemma D and Lemma R

| step | result | note |
|---|---|---|
| S2 | holds | No three vertices of a convex polygon are collinear. This is true for the vertices of **any** polytope, in any dimension. |
| S3 | holds | Normalisation (u = 1) removes any scalar freedom in a ⊗ b. |
| D.1, p = 1 | holds | |
| D.1, 2 ≤ p ≤ 3 | holds | m_i ≤ m − (p − 1) ≤ 3. Three or fewer distinct b's are independent by S2, so β_i ≠ 0. |
| D.1, p = 4 | holds | See finding L1: it does **not** need K = 3. |
| D.2 | holds | The support Z has at most 4 elements. Inside one line, three or fewer elements are independent, so Z = Y, which contradicts "mixed". |
| R.1 | holds | See below. |
| R.2 | holds | It uses T⁻¹(P) = P, which follows from bijectivity, and \|L\| ≥ 2. |
| R.3 | holds | This is exactly the automorphism argument for the rook's graph K_{n_A} □ K_{n_B} (finding P2). Case 2 forces n_A = n_B, both by cardinality and by injectivity. |
| R.4 | holds | See the scalar and effect check below. |
| R.5 | holds | Checked: (h ⊗ k)(SW(a_i ⊗ b_j)) = h(b_j) ⊗ k(a_i) = a_{α(j)} ⊗ b_{β(i)}. The domains and codomains are consistent. |

**The 4-point question (does a set that is not a line also span 3 dimensions?).**
- Every subset of P lies in one row, lies in one column, or is mixed.
- Lemma D says every mixed 4-set has linear rank 4. So any mixed set with at least 4 points spans at least 4 dimensions, and no 4-point set outside a line can span only 3.
- Exact check: 0 dependent mixed 4-sets out of 1812 for square², 12600 for pentagon², 4820 for square × pentagon and 200 for bit × pentagon.
- R.1 also pads the mixed set Y₀ (2 to 4 points) up to 4 points inside X. That works because \|X\| ≥ 4, and padding cannot unmix a set.

**Scalars, signs and reflections (R.4).**
- Because T(P) = P maps normalised vectors to normalised vectors, there is no scalar freedom. g_A is fixed by T(v ⊗ b_1) = g_A(v) ⊗ b_{β(1)}, and it sends vertices exactly to vertices.
- The ambiguity g_A ⊗ g_B = (c·g_A) ⊗ (c⁻¹·g_B) is removed by unit preservation.
- Reflections are already inside D_n, so no separate sign case arises.

**g_X ∈ Aut(Ω_X), including effects.**
- g_X permutes the vertices, so it is a linear bijection with g_X(Ω_X) = Ω_X and u ∘ g_X = u.
- Under all effects, the effect set is the dual of the state cone, so it is preserved automatically.
- Lemma R itself defines Aut through the state space only. For parts with restricted effects, "g_X preserves the effect set" is not shown. That case is outside R1 anyway (low, L3).

## B. R1, the dichotomy

- **E1 (pure products are extreme in max): holds.**
  - First use of all effects: the exposing functional e_a is an effect.
  - Second use: "nonnegative on all A-effects ⇒ in the closed state cone". With restricted effects the dual cone is larger and this step fails. LEMMA_R §8 flags both uses correctly.
  - φ_f + φ_{u−f} = φ_u = s_A = a, and a spans an extreme ray, so φ_f = s_B(f)·a. Product functionals span the dual space, so s = a ⊗ s_B.
- **E2 (an extreme point of S inside min is a pure product): holds.** It is a convex combination of points of P ⊆ S, so it equals one of them.
- **E3: holds.** An affine bijection of S preserves extreme points.

## C. R2 and R3 with RC15: inherited or smuggled?

- I checked RC15's hypotheses at the source (CLAIM_MAP_v2 row RC15; ROUND10 §16, Theorem M12 and Corollary M12-P at repo 04c8309):
  - all reads;
  - a transitive, absolutely irreducible finite group on each part;
  - a composite between min and max that is invariant under both groups;
  - finite orbits;
  - condition ♦, which the disk lemma gives for every pair of regular polygons.
- R2 states all of these.
- D_n acts absolutely irreducibly on the 2-dimensional r-space for n ≥ 3, so this premise holds.
- **No premise is smuggled into R2 or R3**, beyond the following model scope, which should be said out loud (M2):
  - (a) two parts only;
  - (b) "reversible step" means an element of Aut(S) acting on the pair alone: no ancilla, no third part, no measurement or conditioning, no mixture of reversible maps (shared randomness would give separable correlated states);
  - (c) RC15's own status: a parallel worker's self-check, not independent, not formalized.
- Mixed product starts are covered correctly: once T = g_A ⊗ g_B (possibly with swap), linearity keeps any ω_A ⊗ ω_B a product.

## D. Numerics, rerun

- **Author's float script:** rerun on the box gives output byte-identical to `lemma_r_check.out` (`rerun_float.out`, 7 s).
- **Independent exact check** (`exact_check.py`):
  - Pentagon in affine Q(√5) coordinates: x = cos 72k°, y = sin 72k° / sin 72°.
  - The K-matrix is used only as a necessary filter, followed by full backtracking over all points.
  - Each surviving permutation is then confirmed linear by an exact rank test.
  - Lines → lines is counted combinatorially.

| parts | mixed 4-sets (dependent) | K-preserving permutations | exactly linear | lines → lines | author |
|---|---|---|---|---|---|
| square² | 1812 (0) | 128 | 128 | 128 | 128/128 ✓ |
| pentagon² | 12600 (0) | 200 | 200 | 200 | 200/200 ✓ |
| square × pentagon | 4820 (0) | 80 | 80 | 80 | 80/80 ✓ |
| bit × pentagon | 200 (0) | 200 | 200 | **20** | 200/20 ✓ |
| cube² (Lemma D only) | 634256 (**0**) | — | — | — | not run by author |
| square pyramid × square (Lemma D only) | 4820 (**0**) | — | — | — | not run by author |

- Every K-preserving permutation found was exactly linear. The 128 and 200 counts are therefore exact (OBS, exact arithmetic).
- The bit-part sharpness (200 vs 20) is confirmed exactly. The trit count of 6000 = 10³·3! matches (D5)³ ⋊ S3 (direct-sum structure; float only).

## E. Findings

### Medium

**M1. The ε = 0.01 caveat is false as worded, not merely unproved (LEMMA_R R3).**
- PREREG_P defines Θ(h, ε) with "a read r_A whose outcome has entropy ≥ 1 bit" and puts no bound on the number of outcomes.
- With all effects, take the state-independent read {0.99·u, 0.01·u/(N−1), …}. For N − 1 ≥ 2^91.92 its entropy is h(0.99) + 0.01·log₂(N − 1) ≥ 1 bit. B's trivial guess "outcome 0" then succeeds with probability 0.99.
- So with unbounded reads, Θ(1, 0.01) is **trivially feasible in every theory, from every state, with no correlation at all.** The note's arithmetic (2⁹² outcomes) is right, but the reading is wrong: for unbounded reads the claim is false, not "not proved".
- **Fix:** state rigidity at ε = 0.01 only for reads with fewer than about 2^91.9 outcomes, which includes every binary read.
- Also record that the ε = 0.01 arm of the locked PREREG_P is degenerate without a cap on the read class. NOTE_P's run used reads where "H(A) ≥ 1 bit forces an exactly uniform A", i.e. binary reads. Record this as a note or deviation entry, never as an edit to the locked file.
- C3v2's classifier needs the same read cap stated before lock.

**M2. The status paragraph drops premises (LEMMA_R §0 bullet 3; §7 line 144).**
- §0 says "every locally symmetric composite of two regular polygons with n ≥ 4 has Aut(S) = local ⋊ swap". It omits two premises:
  - **finite orbits** (an RC15 premise);
  - **all effects** (an R1 premise).
- §7 says these worlds "cannot track at all". That overreaches the model. It is shown only for two parts, one or more steps of Aut(S) on the pair alone, and ε = 0 (or capped reads). Three parts are listed as still open in §7 itself, and so is the repeated task with fresh source bits (Θ_T).
- **Fix:** carry the full hypothesis list into §0 and soften §7 to "cannot correlate the two parts by any reversible map of the pair".

**M3. The prior-art framing is incomplete (LEMMA_R §6).**
- (a) **Open Quantum Problem #42, "Reversible dynamics on composite systems"** (Dakić and Müller, 2017; restated in google-deepmind/formal-conjectures issue #3459, read this session).
  - It asks whether any locally tomographic composite with transitive local groups and a non-product reversible map must embed in quantum theory.
  - R2 would be a partial case of it: polygon parts, invariant composites with finite orbits, all maps trivial.
  - The note should state this relation. It sets the stakes and the priors: a polygon-wide intermediate-composite result is exactly the case Al-Safi–Richens' Discussion names as the obstacle. The extra scrutiny then falls on **RC15**, which carries all of the entangling half.
- (b) **R.3 is the classical automorphism group of the rook's graph** K_m □ K_n: S_m × S_n, or (S_n × S_n) ⋊ Z₂ when m = n.
  - This is standard graph theory. Wikipedia attributes it to Harary 1958, Pacific J. Math. 8:743–755, DOI 10.2140/pjm.1958.8.743, which I verified on Crossref but did not read.
  - The Hamming-distance argument of Gross et al. 2010 and Al-Safi–Richens Lemma 2 is the same idea, applied to effects.
- (c) "Lemma D plays the role of their Lemma 1, which is Al-Safi–Richens' Lemma 4" is loose.
  - ASR Lemma 4 (Marcus–Moyls Lemma 1) is a span statement: Σ x_i ⊗ y_i = Σ w_j ⊗ z_j with the x_i independent ⇒ y_i ∈ span{z_j}.
  - Lemma D is a finite independence statement. Its proof uses the same dual-functional move. Say "same technique", not "plays the role".
- **Assessment:** Lemma R is a short combination of three standard pieces:
  - the dual-functional (Marcus–Moyls) step;
  - "lines go to lines";
  - Aut of the rook's graph, followed by linear extension.
- I did not find the exact statement in print. That covers Crossref plus the searches named in §6 and in my brief. **Folklore-level, not claimed new** is the right label. The author's own "novelty is not claimed" stands.

**M4. The §14 tally of 5/7 is not supported by §14's own text.**
- The seven misses listed are: gravity, U(2), H2, A2 §2, (i) RECORD-COST-U §14, (ii) PREREG_P, (iii) LEMMA_R.
- FH is shown to cover four of them: (i), (ii), (iii) and U(2). It fails on gravity and H2, and A2 §2 is left unclassified. H3 is an eighth item that is not in F2's list. So the count is **4/7 (or 4/8)**, not 5/7.
- Counting (iii) as a miss that "F2 fails on" is also doubtful:
  - LEMMA_R is a proved result, not a test miss.
  - Its content ("rules forced once the parts are fixed") arguably fits F2, because the parts were fixed by hand.
  - (ii) is similar: the theories and N = 2 were fixed in advance.
- With flexible class boundaries, either candidate can be made to fit more misses after the fact. SR-a is correctly labelled "not a test". The numbers 4/7 and 5/7 should be dropped, or reported as one reader's classification with each item's assignment shown.

### Low

**L1. "K = 3 is used only in case p = 4 of D.1" (§2 note, §8) misplaces the dependence.**
- In case p = 4:
  - if the four a's are independent (possible when K_A ≥ 4), then β_i = c_k·b_{j_k} = 0 at once, which is a contradiction;
  - if they are dependent, the written argument goes through, using only S2 for three of them.
- So **Lemma D holds for any two polytopes, in any dimension.** The exact check confirms this for cube² (0 of 634256) and square pyramid × square (0 of 4820).
- K = 3 is actually used in **R.1**: a line spans K = 3 dimensions, which is less than 4, the rank of a mixed 4-set.
- For K ≥ 4, a K-dimensional extension (HYP R′) needs "no mixed set of at least \|L\| points spans only K dimensions". That is a different lemma.
- It already fails for mixed 5-sets in octahedron²: 4 coplanar equator vertices in one column plus any fifth point. Yet lines → lines still holds there numerically. So R′ needs a new argument, not a repaired D.
- §7 item 3's explanation for the square pyramid ("a dependent 4-set, so the analogue of S2 fails") is true of S2 but does not touch Lemma D. The square pyramid's conditional maps come from reducibility (Al-Safi–Richens Theorem 2).

**L2. "15/15 finite horizons chose a polygon" (§14, SR-b prior).**
- ROUND10 §14 records strict polygon wins at T = 2–12, 16 and 20 (13 horizons) and a tie at T = 1. That is 13 wins and 1 tie out of 14, not 15 of 15.
- This does not move the 0.3 prior much, but it should be corrected.

**L3. Restricted-effect parts.** Lemma R's Aut(Ω_X) is state-only. That is fine for R1 and R2, which assume all effects. A future stabilizer-like extension must also check effect preservation.

**L4. Bremner et al. DOI.** LEMMA_R §5 and the crossref file record a 404 for 10.1007/s10208-013-9170-8, so no DOI was cited. The correct DOI, **10.1112/S1461157014000400** (LMS J. Comput. Math. 17:565–581, 2014), resolves on Crossref and is already used in ROUND10 §15.

**L5. Composite-level Aut vs effects.** R2's "Aut(S) = D × D (⋊ swap)" is the state-space group. If composite effects were restricted below the dual of S, the physical group could only be smaller. The conclusion "⊆ local ⋊ swap" still holds, so this is harmless. One sentence would suffice.

**L6. Score scale (§14).** 0.3·4 + 0.7·2 = 2.6, and 2.6 / 3 h ≈ 0.87 per hour. The arithmetic is correct and matches the §13 (C13-6) per-hour scale.
- There is no EIV table in CORE.md. "Same CORE-method table" should read "the same §13 table and scale".
- V_hit = 4 is a judgment value. With the §14 tally corrected (M4) and the rationale that FH explains most misses weakened, a prior below 0.3 is defensible. At 0.2, SR-b would score 0.73 per hour. Either way it is not promoted, so the ranking conclusion stands.

## F. Labels I recommend

- **Lemma D:** PROVED (in-model) for any two polytopes (not only polygons). Hostile-reviewed once (this note). Not formalized.
- **Lemma R** (polygons with ≥ 4 vertices each, any linear bijection with T(P) = P): **PROVED (in-model), hostile-reviewed once (this note, PASS), not formalized; elementary; folklore-level (Marcus–Moyls dual-functional step + rook's-graph automorphisms), novelty not claimed.** It is a good Lean candidate: finite, with no analysis needed.
- **R1:** PROVED (in-model) under all effects, hostile-reviewed once.
- **R2 and R3:** PROVED (in-model) **conditional on RC15** (a self-check, not independent).
  - Scope: two regular polygon parts with n ≥ 4, all effects, a composite invariant under the local groups with finite orbits, two parts acting alone, and ε = 0 (or capped reads at ε = 0.01, M1).
  - Relation to Open Quantum Problem #42 to be stated (M3).
- **C3v2 Arm 2:** "theorem-fixed conditional on RC15" is fair. The suggested exact RC15 instance check on max(P5, P7) is the right independent check, because the whole remaining risk sits in RC15.
- **§14 SR-a:** a classification, not a test. Drop the 4/7 and 5/7 counts, or show each assignment (M4).
