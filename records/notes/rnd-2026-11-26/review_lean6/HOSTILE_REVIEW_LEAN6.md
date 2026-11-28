# Hostile review: Lean round 6 at 7d4adb9

Reviewer: independent executor, fresh context. 26 Nov 2026, 11:27–11:52 ET.
Object: `mitchell-moving:forge-rnd-record-cost-2`. `git ls-remote` tip = `7d4adb92b9f7202cafdce3fb21e6e592859e6437`.
Fresh clones: `clone/` (build, audits, repo checks) and `clone-pytest/` (full pytest), both at 7d4adb9.
Range reviewed: be06522 (stage 1, Lemma D), c7ed55d (round 5 fixes), 937097f (stage 2, rook), ea2b1fe (stage 3,
`lemmaR`), 7d4adb9 (AUDIT.json only). The PR draft reviewed is `/workspace/gtao-notes/rnd/PR295_BODY_EDITS_r6_DRAFT.md`.
No commit, no push, no email. The only local changes are the clones' `origin` URLs, which point at upstream so the
checks compare with upstream `main`. Logs: `check_lean.log`, `rndaxioms.out`, `rc_*.log`, `pytest.log`,
`pytest_rerun2.log`, `crossref.txt`, `harary1958.txt`, `scratch/NonVacR.lean` and `.out`.

## Overall: PASS-WITH-FIXES

There are no high findings. The Lean statements say what the README rows say. No hypothesis is vacuous: the
reviewer's scratch proves S2 (`Indep3`) for the square in Lean and instantiates `lemmaR` with it. The bound
"dimensions ≤ 3" is not hidden: it is disclosed in the README, and together with S2 it means exactly 3, i.e.
polygons. No text claims that T itself is g_A ⊗ g_B, that S2 for polygons is in Lean, or that C3v2 is settled.
The axioms are clean and every figure reproduces. There are three medium findings, all about credit or
non-vacuity, and eight low ones.

## 1. Build, axioms, figures (observed at 7d4adb9)

| Check | Result |
|---|---|
| `tools/check_lean.sh`, detached, logged | **OK**: 18433 jobs. `LemmaR` and `M11BlocksChecks` were built from source in this clone (7.6 s, 2.4 s). AxiomAudit: **2276** GTAO declarations, only propext, Classical.choice, Quot.sound. Token scan: no sorry/admit/axiom/native_decide/unsafe/implemented_by. |
| AUDIT.json | `audit_count` 2276 at `ea2b1fe`. 7d4adb9 touches only AUDIT.json, so the Lean sources at 7d4adb9 equal those at ea2b1fe. **Matches.** |
| `scripts/RndAxioms.lean` | 248 `#print axioms` lines with no duplicates; 248 outputs. 238 use the standard three and 4 use a subset (propext with or without Quot.sound). 6 depend on no axioms: `line_of_triangle`, `row_line`, `row_col`, `same_type`, `assemble`, and the old `no_zero_drift_while_recording`. `lemmaD`, `rook_aut`, `adj_of_map`, `lemmaR`, `sep_necessary`, `flipA_*`: standard three or a subset. **248 confirmed**; 243 after the five declared paddings (README l. 475–477). |
| pytest (full, fresh clone) | 470 passed and 2 failed (`test_banned_words::test_standalone_entry_point`, `test_check_claims::test_clean_tree_passes`). Both compare against `origin/main`, and the clone's origin was the fork, whose `main` is stale (THEORY.md:179 / CX2). With origin pointed at upstream, both pass (`pytest_rerun2.log`). **472 is confirmed under the upstream-origin setup** that the PR draft describes. |
| repo checks vs upstream main | check_consistency, verify_locks, banned_words, check_claims **PASS**. check_fresh and check_pending were not rerun (they need the token; the author's run is logged). |
| append-only | Claim map: RC13 and RC20 Lean cells changed only by appended text after the original token; RC21 is a new row. Errata: §12–§13 are pure additions. README/INVENTORY: the counters 232→248, 227→243 and 36→37 files are status counters, rewritten in place as in earlier rounds. The committed C12C spec equals the side-session file byte for byte below its dated note. |
| wording | No banned word in the round-6 additions or the PR draft. "Fixes from the hostile review" is not followed by `#N`, so it is not a closing keyword. |

## 2. Do the statements say what the prose claims?

- **`lemmaD`** (any `dA, dB`, S2 on both sides, `|Y| = 4`, Y in no single row and no single column ⇒ independent).
  This matches note Lemma D and the README row "any dimensions". The proof is real: the rows and columns cases
  come from the dual-functional step, and the all-distinct case from a dual vector plus pairwise independence.
- **`rook_aut`**. If f: Fin m × Fin n → Fin p × Fin q is injective and preserves adjacency both ways, then f is
  a product map or a swapped product map, for m ≥ 1 and n ≥ 2. "Slightly more general" is accurate: there is no
  surjectivity and the target grid is arbitrary.
- **`lemmaR`**. Hypotheses: `Indep3 a`, `Indep3 b`, `dA ≤ 3`, `dB ≤ 3`, `m, n ≥ 4`, T a K-linear equivalence of
  `Matrix (Fin dA) (Fin dB) K` with `T '' range (kr a b) = range (kr a b)`. Conclusion: there is a bijective f with
  T(a_x ⊗ b_x) = kr(f x), and f is a product map or a swapped product map. This is spec item 4 in substance.
  - **S2 can be met by a polygon.** S2 holds for the vertices (1, p) of any convex polygon (LEMMA_R §1 S2), and
    with m ≥ 3 it forces dA ≥ 3. So with `dA ≤ 3` the dimension is exactly 3, as the README discloses.
  - **Checked in Lean (scratch, axioms standard three):** `sqV_indep3 : Indep3 sqV` for the square
    (1,±1,0), (1,0,±1) over ℚ. Then `lemmaR sqV_indep3 sqV_indep3 le_rfl le_rfl le_rfl le_rfl T hP` typechecks
    for every T. The transpose (the swap) is a non-identity T with T''P = P. So the hypotheses are jointly
    satisfiable, non-trivially.
  - **"Dimensions ≤ 3" is a real scope restriction, not a hidden one.** It confines the theorem to polygon
    parts. The line step needs four points of a row to be dependent. Polytopes of dimension ≥ 3 stay HYP R′.
    This is disclosed in the README; see L2 for the ledger and PR wording.
- **`adj_of_map`, `not_indep_row/col`, `exists_line4`, `kr_injective`, `indep_small`.** These say what their rows
  say. `adj_of_map` uses `T` linear, injectivity, Lemma D on the images and the dependence of the four
  preimages; the argument is sound.
- **`sep_necessary`** proves (diag d)ᵀ(E_uv+E_vu)diag d = E_uv+E_vu when d_u·d_v = 1. This is the same
  congruence as in `diag_of_separating`, so it shows necessity for the Schur step, as labelled.
- **`flipA_pureSetB` / `flipA_hull_pureSetB`.** These are exactly the `hfA i` hypothesis of
  `m11_blocks_polytope_flips` with V = pureSetB. "Partial" is correct: hfB, the permutations and hT are not stated.
- **Not covered, and disclosed everywhere:** spec item 5 (T = g_A ⊗ g_B or with swap); S2 for the polygon
  instance; the RC15 combination.

## 3. Overclaims

None at the high level:
- The ledger (RC20 Lean cell), errata §13, the README rows and the PR draft each say "abstract form" and list
  item 5, S2 and the RC15 combination as not formalized.
- RC20's status column is unchanged.
- No new text mentions C3v2.
- RC13 says "superseded for polytope S" only for the finiteness clause and keeps the Löwner step open.

Wording issues are in L2, L3, L5 and L6.

## 4. Prior art (Crossref: `crossref.txt`)

- Al-Safi & Richens 2015, *Reversibility and the structure of the local state space*, NJP 17:123001,
  10.1088/1367-2630/17/12/123001. **Crossref OK.** I checked the arXiv text (`stepback-refs/asr.txt`): Lemma 4 is
  the span statement "∑xᵢ⊗yᵢ = ∑wⱼ⊗zⱼ, {xᵢ} independent ⇒ yᵢ ∈ span{zⱼ}", proved by citing Marcus–Moyls Lemma 1.
  `dual_step` is its special case with all zⱼ = 0. **The credit is correct.**
- Marcus & Moyls 1959, *Transformations on tensor product spaces*, PJM 9:1215–1221, 10.2140/pjm.1959.9.1215.
  **Crossref OK.**
- Harary 1958, *On the number of bi-colored graphs*, PJM 8:743–755, 10.2140/pjm.1958.8.743. **Crossref OK.**
  I read it (msp.org PDF, `harary1958.txt`); see M1.
- Whitney 1932, *Congruent graphs and the connectivity of graphs*, Amer. J. Math. 54:150,
  10.2307/2371086. **Crossref OK.** I suggest adding it; see M1.

## 5. Findings

**High.** None.

**Medium.**
- **M1 (Harary credit is imprecise; "cited, not read" is now stale).** Harary 1958 §2–3 (pp. 745–746) gives the
  *line group* of K_{m,n}: S_m × S_n for m ≠ n, plus the colour interchange for m = n. That is the group the
  automorphisms of K_{m,n} induce on its edges, and the edges are the cells of the grid. That this is the *whole*
  automorphism group of the rook's graph L(K_{m,n}) needs Whitney's line-graph theorem (Whitney 1932; DOI verified, paper not read by this reviewer, so cite it as "cited, not read"). The fix:
  - In README, errata §13 and the PR draft, write "Harary 1958 (line group of K_{m,n}); full automorphism group
    via Whitney 1932, 10.2307/2371086".
  - Drop "cited, not read".
  - `rook_aut` is proved directly in Lean, so no result depends on either paper.
- **M2 (Al-Safi–Richens Lemma 2 not credited at the Lean layer).** LEMMA_R §0 and §6 say the second half of the
  proof "is the same structure as Al-Safi–Richens 2015 Lemma 2" (adjacency-preserving reversible maps of the
  composite are trivial). The README credit line, errata §13 and the PR draft credit only Lemma 4 and Harary. The
  LemmaR.lean header says "the same adjacency idea" without the lemma number. Add "and Lemma 2 for the adjacency
  argument (stated for effects in max composites)".
- **M3 (no non-vacuity witness in the repo for `lemmaR`).** The same pattern applied at round 5 (the M2 of that
  review). `scratch/NonVacR.lean` gives `sqV_indep3`, the square instance of `lemmaR` and the transpose example.
  It has no sorry and uses the standard three axioms. Moving it in, as was done with the round 5 scratch, would
  close the first half of "S2 for polygon vertices" for one polygon over ℚ. Regular n-gons with n ≠ 4 need ℝ
  (cos 2π/n), and the general convex-polygon S2 (no three collinear vertices) stays on paper.

**Low.**
- **L1.** `lemmaR` returns functions α, β, not `Equiv.Perm`, and does not state m = n in the swap case. Spec item
  4 asks for σ, τ permutations and m = n. Both follow from `Function.Bijective f` in a few lines, but they are not
  stated. Either add a corollary or append "(α, β bijective and m = n follow from f bijective; not stated)" to the
  README row.
- **L2.** "Dimensions at most 3" in RC20's Lean cell, errata §13 and the PR draft. Under S2 with m, n ≥ 4 this
  means exactly 3 (polygons only). A reader could take "at most 3" to include bit or trit parts, which are exactly
  where Lemma R fails (LEMMA_R §0, sharpness). Say "dimension 3 (polygon parts)", as the README already does.
- **L3.** RC13 correction "superseded for polytope S": `autSet_finite` also needs `span (conv V) = ⊤`. Say
  "spanning polytope S".
- **L4.** The ledger and the PR draft say "S2 for *regular* polygon vertices". S2 needs no regularity
  (LEMMA_R §1 S2, any convex polygon). The narrower wording is harmless but understates what is on paper.
- **L5.** Four exported theorems are not in RndAxioms or in a README row: `image_convexHull_of_image_eq`,
  `vecMulVec_sum_left`, `vecMulVec_sum_right` and `vecMul_vecMulVec`. AxiomAudit covers them. "248 exported
  theorems" is really "248 listed". Either list them or say "248 listed".
- **L6.** PR draft wording:
  - "Checks at 7d4adb9 on a fresh upstream clone" should read "a fresh clone of the fork branch with `origin` set
    to upstream". The upstream origin is what makes the two pytest cases pass (§1).
  - "RC20 stays as it was" should read "RC20's status is unchanged; its Lean cell gains an appended note".
- **L7.** RC20's Lean cell still opens with "not-formalized; Lean round 6 (appended): … proves …". This is forced
  by append-only, but the leading token is now partly superseded. One errata sentence saying so would help a
  reader who only scans the first token. The same applies to the repo copy of LEMMA_R.md §9 C9-7 ("not
  formalized").
- **L8.** Linter warnings at M11BlocksChecks.lean:38 (`<;>`). These are cosmetic.

## 6. Bottom line

The round 6 Lean is sound and says what its labels say. Lemma R is proved in Lean in abstract form for
dimension-3 families with S2; the scratch instance shows the polygon case can meet its hypotheses. The map
corollary (T local or local with swap) and the RC15 combination remain on paper. Before Friday's merge, fix the
credit lines (M1, M2) and preferably add the non-vacuity file (M3).
