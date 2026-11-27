# Lean status for the record-cost R&D layer, as of 26 November 2026 (Forge)

*Written Thursday 26 November 2026, about 19:40 ET, at branch tip `94771ae` of `mitchell-moving:forge-rnd-record-cost-2` (PR #295). Generated from `formal/lean/scripts/RndAxioms.lean` and `git blame` on the declaring line; the axiom sets are from a rerun of `RndAxioms.lean` tonight on a built tree at `94771ae` (exit 0). Every theorem here is **proved-in-model**: Lean checks the statement as typed, and what the statement means for the theory is set by the README rows (`formal/lean/README.md`, the RND-RECORD-COST section, lines 226–510), which carry the scope notes. Status source for claims: `measurement/CLAIM_MAP_v2.md` only.*

## 1. Summary (observed)

| item | value |
|---|---|
| Names listed in `scripts/RndAxioms.lean` | **253** (248 after dropping the five padding names of README:477–480) |
| Axioms used | 242 names use `propext, Classical.choice, Quot.sound`; 2 use `propext, Quot.sound`; 3 use `propext` only; 6 use none. **No `sorryAx`.** No custom axiom |
| `sorry` / `admit` in `GTAO/Rnd` | none (the only hits are the word "admits" in docstrings) |
| `tools/check_lean.sh` AxiomAudit | 2285 GTAO declarations recorded in `formal/lean/AUDIT.json` (commit `94771ae`, "Record audit 2285 for bee8c5c") |
| Names added on 26 November | 168 (85 → 253) |
| Depth caveat | raw counts are not depth: besides the five padding names, about twelve more are one-line instances, restatements or Mathlib wrappers (README:504–510) |

## 2. Rounds and review status

| round | commits (names added) | running total | review | outcome | fixes |
|---|---|---|---|---|---|
| R1–2 (25 Nov, 21:46–23:09) | `202f6cf` (62), `aac249c` (19), `a2a3f52` (4) | 85 | `rnd-2026-11-26/overnight/HOSTILE_REVIEW_FOUNDATIONS.md` (Lean layer section) | scope notes needed on several names (README:465–482) | scope notes appended (README:465–482; errata `5f36cf5`, `3e4c99e`); no theorem renamed |
| Lean round 3 (26 Nov, 01:14–03:57) | `b40e87a` (6), `80cf785` (31), `d7add19` (32), `e4acb0f` (1), `d699a1f` (2) | 157 | `rnd-2026-11-26/review_lean3/HOSTILE_REVIEW_LEAN3.md` at `4c693b6` | no high; M1 M11′ not assembled, M2 PR text behind, M3 purification clause overclaimed | `0cf559f` (scope notes README:484–503; purification clause withdrawn) |
| Lean round 4 (05:07–06:12) | `c43acfe` (10), `85da274` (10), `aae3eb5` (4), `33657cf` (4), `6138b88` (2), `9b7353d` (5) | 192 | `review_lean4/HOSTILE_REVIEW_LEAN4.md` at `eb8f20b` | no high; two medium wording findings (`nona_beats_disk`, local-symmetry premise) | `7728d59` |
| Lean round 5 (07:08–09:09) | `dd812e3` (22), `7728d59` (3), `7ace8c0` (10) | 227 | `review_lean5/HOSTILE_REVIEW_LEAN5.md` at `96d7fa7` | PASS-WITH-FIXES; four medium (a "Faithful" row sentence not proved; OnsetO ledger and source; two PR-draft items); Theorem O spec items (iii b–d) only in part | `c7ed55d` |
| Lean round 6 (09:56–11:56) | `be06522` (5), `937097f` (6), `ea2b1fe` (7), `c7ed55d` (3), `bee8c5c` (5) | 253 | `review_lean6/HOSTILE_REVIEW_LEAN6.md` at `7d4adb9` | PASS-WITH-FIXES; three medium (credit, non-vacuity), eight low | `bee8c5c`, except L8 (cosmetic linter warnings at `M11BlocksChecks.lean:38`, open) |

Not independently reviewed: the five names added by `bee8c5c` itself (`LemmaRNonVac.lean` and `lemmaR_perm`) came after the round 6 review; they are the reviewer's own requested non-vacuity instances and the build and axiom rerun at `94771ae` pass, but no fresh reviewer has read them.

Note on the "commit" column below: it is the `git blame` commit of the declaring line, so a name whose line was later touched shows the later commit.

## 3. What is open in Lean (not formalized; labels from the README and CLAIM_MAP_v2)

- **Load-bearing steps not in Lean** (README:480–482): NA1 (the SO(3) classification), the general maximal-torus criterion, the Jordan-class classification, Piron, Solèr, Baer, the tensor-product block of the Schur step for parts other than products of cross-polytopes, the Löwner step of M11, M12, purification, and the cost-selection step.
- **Lemma R:** the corollary for a local T is not in Lean; S2 (`Indep3`) is in Lean for the square only (`LemmaRNonVac.lean`), not for regular polygons in general.
- **RC15 combination** (FOR-27 spec item 5): not assembled.
- **Theorem O:** finite version in Lean (`OnsetO.lean`); spec items (iii b–d) only in part (review_lean5 L1).
- **M11′:** chained only for hypercube and cross-polytope parts (`M11Cube.lean`) and products of cross-polytopes (`M11Blocks.lean`); `final_assembly` is an elementary set lemma with the steps not chained (README:500–504).
- **Cost dial:** `Jdial_*_global` only at the tuned weight and 0 < β ≤ π/2; the minimizer for β > π/2 is open.
- **Hanner and non-polyhedral S**, and exact optima for the heptagon and nonagon paths (`hept_beats_disk` is T = 3 for one fixed path, cost bounded not computed).
- **Candidates from today's paper results** (proved-in-model on paper, independently checked, not in Lean): the P15 restriction lemma (REQUIREMENTS_FIRST §9; REVIEW_P15), the SR-b4 proposition and its odd analogue (SR_B4; review_srb4, review_srb4_odd), SR-b3, Lemma D1, SH1 (SELF_HORIZON).

## 4. Per-file table (all 253 listed names)

Counts: 253 listed names; padding flagged: 5; by round: L3 72, L4 35, L5 35, L6 26, R1–2 85; by axiom set: [propext, Classical.choice, Quot.sound] 242; [none] 6; [propext] 3; [propext, Quot.sound] 2

### `formal/lean/GTAO/Rnd/Composition.lean` (4)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.Composition.P1` | 36 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.Composition.log_additive_iff` | 101 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.Composition.P2_entries` | 115 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 | padding (README:477) |
| `GTAORnd.Composition.gbit_no_local_write` | 130 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/Controls.lean` (1)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.unitModel_clones` | 45 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/LemmaB1.lean` (3)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.CopyModel.lemmaB1_k` | 114 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.CopyModel.clone2_to_k` | 174 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.CopyModel.lemmaB1` | 196 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/PolygonDrift.lean` (10)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.discrete_oneParam_trivial` | 50 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.dihedral_oneParam_trivial` | 62 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.simplexPerm_oneParam_trivial` | 69 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.disk_oneParam` | 77 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.ring_closed_form` | 136 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.ring_bound` | 150 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.factor_ge_two` | 160 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.ring_ratio_indep` | 168 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.ring_cost_lower_bound` | 186 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.disk_strictly_cheaper` | 195 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRef/Ball.lean` (2)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.normal_fixer_bot` | 44 | theorem | propext, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.normal_nontrivial_fixes_nothing` | 56 | theorem | propext, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRef/Broadcast.lean` (4)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.amplify` | 125 | theorem | propext, Classical.choice, Quot.sound | `b40e87a` | L3 |  |
| `GTAORnd.SelfRef.LR3.L5_asymptotic` | 174 | theorem | propext, Classical.choice, Quot.sound | `b40e87a` | L3 |  |
| `GTAORnd.SelfRef.LR3.L5_perfect` | 196 | theorem | propext, Classical.choice, Quot.sound | `b40e87a` | L3 |  |
| `GTAORnd.SelfRef.LR3.L5_pairwise` | 224 | theorem | propext, Classical.choice, Quot.sound | `b40e87a` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/BroadcastControl.lean` (2)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.bit_achSet` | 85 | theorem | propext, Classical.choice, Quot.sound | `b40e87a` | L3 |  |
| `GTAORnd.SelfRef.LR3.L5_control` | 112 | theorem | propext, Classical.choice, Quot.sound | `b40e87a` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/CircleOrbit.lean` (4)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.top_coeff_zero` | 137 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.circle_top_zero` | 168 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.circle_all_zero` | 186 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.no_linear_clone_circle` | 209 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRef/Composite.lean` (8)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.cube_corr_bound` | 34 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.square_corr_bound` | 52 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.cube_corr_tight` | 60 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.pure_marginal_product` | 73 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.pure_marginal_factorizes` | 101 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.square_C_bound` | 114 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.square_pure_marginal` | 135 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.pure_marginal_finite` | 153 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/ContinuousTime.lean` (4)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.R10.continuous_line_discrete_const` | 27 | theorem | propext, Classical.choice, Quot.sound | `a2a3f52` | R1–2 |  |
| `GTAORnd.SelfRef.R10.finite_group_no_continuous_motion` | 33 | theorem | propext, Classical.choice, Quot.sound | `a2a3f52` | R1–2 |  |
| `GTAORnd.SelfRef.R10.continuous_change_infinite_group` | 40 | theorem | propext, Classical.choice, Quot.sound | `a2a3f52` | R1–2 |  |
| `GTAORnd.SelfRef.R10.never_returns_infinite_order` | 47 | theorem | propext, Classical.choice, Quot.sound | `a2a3f52` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRef/CostDial.lean` (6)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.Jdial_hasDerivAt` | 40 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.Jdial_stationary_iff` | 55 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.Jdial_midpoint` | 68 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.Jdial_midpoint_60` | 88 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.inv_sqrt3_bracket` | 94 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.Jdial_rho_zero` | 103 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRef/CostDialBeyond.lean` (2)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.Jdial_midpoint_not_global` | 32 | theorem | propext, Classical.choice, Quot.sound | `6138b88` | L4 |  |
| `GTAORnd.SelfRef.LR3.Jdial_tie_at_right_angle` | 53 | theorem | propext, Classical.choice, Quot.sound | `6138b88` | L4 |  |

### `formal/lean/GTAO/Rnd/SelfRef/CostDialGlobal.lean` (4)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.Jdial_midpoint_global` | 50 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.Jdial_midpoint_unique` | 71 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.Jdial_60_global` | 106 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.rho_60` | 119 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/DimBound.lean` (3)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.distinguishable_affineIndependent` | 42 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.dim_bound` | 66 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.dim_bound_one_bit` | 179 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRef/Entangle.lean` (12)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.Entangle.pure_marginal_extreme` | 27 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Entangle.reversible_preserves_pure` | 103 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Entangle.local_map_tmul` | 110 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 | padding (README:477) |
| `GTAORnd.SelfRef.LR3.Entangle.swap_tmul` | 115 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 | padding (README:477) |
| `GTAORnd.SelfRef.LR3.Entangle.local_perm_tprod` | 121 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Entangle.simplex_extreme_iff` | 132 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Entangle.classical_pure_product` | 209 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Entangle.le4_bound` | 218 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Entangle.le4_attained` | 223 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 | padding (README:477) |
| `GTAORnd.SelfRef.LR3.Entangle.classical_no_purification` | 229 | theorem | propext, Classical.choice, Quot.sound | `e4acb0f` | L3 |  |
| `GTAORnd.SelfRef.LR3.Entangle.extreme_trivial_decomp` | 245 | theorem | propext, Classical.choice, Quot.sound | `d699a1f` | L3 |  |
| `GTAORnd.SelfRef.LR3.Entangle.cnot_mixed_correlated` | 285 | theorem | propext, Classical.choice, Quot.sound | `d699a1f` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/FiniteGeometry.lean` (4)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.finite_divring_comm` | 42 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.chevalley_nonzero_zero` | 49 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.diag_form_isotropic` | 69 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.norm_form_isotropic` | 88 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/LemmaR.lean` (20)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.LemmaR.dual_step` | 54 | lemma | propext, Classical.choice, Quot.sound | `be06522` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.exists_dual` | 68 | lemma | propext, Classical.choice, Quot.sound | `be06522` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.indep_of_rows` | 103 | lemma | propext, Classical.choice, Quot.sound | `be06522` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.indep_of_cols` | 136 | lemma | propext, Classical.choice, Quot.sound | `be06522` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.lemmaD` | 163 | theorem | propext, Classical.choice, Quot.sound | `be06522` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.line_of_triangle` | 229 | lemma | none | `937097f` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.row_line` | 248 | lemma | none | `937097f` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.row_col` | 264 | lemma | none | `937097f` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.same_type` | 281 | lemma | none | `937097f` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.assemble` | 300 | lemma | none | `937097f` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.rook_aut` | 325 | theorem | propext, Classical.choice, Quot.sound | `937097f` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.indep_small` | 368 | lemma | propext, Classical.choice, Quot.sound | `ea2b1fe` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.kr_injective` | 375 | lemma | propext, Classical.choice, Quot.sound | `ea2b1fe` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.not_indep_row` | 382 | lemma | propext, Classical.choice, Quot.sound | `ea2b1fe` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.not_indep_col` | 408 | lemma | propext, Classical.choice, Quot.sound | `ea2b1fe` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.exists_line4` | 434 | lemma | propext, Classical.choice, Quot.sound | `ea2b1fe` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.adj_of_map` | 473 | lemma | propext, Classical.choice, Quot.sound | `ea2b1fe` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.lemmaR` | 511 | theorem | propext, Classical.choice, Quot.sound | `ea2b1fe` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.factors_bijective` | 549 | lemma | propext | `bee8c5c` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.lemmaR_perm` | 568 | theorem | propext, Classical.choice, Quot.sound | `bee8c5c` | L6 |  |

### `formal/lean/GTAO/Rnd/SelfRef/LemmaRNonVac.lean` (3)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.LemmaR.sqV_indep3` | 31 | theorem | propext, Classical.choice, Quot.sound | `bee8c5c` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.square_lemmaR` | 47 | theorem | propext, Classical.choice, Quot.sound | `bee8c5c` | L6 |  |
| `GTAORnd.SelfRef.LR3.LemmaR.square_transpose_preserves` | 57 | theorem | propext, Classical.choice, Quot.sound | `bee8c5c` | L6 |  |

### `formal/lean/GTAO/Rnd/SelfRef/Liar.lean` (4)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.liar_half` | 30 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.sharp_flip_no_fixed` | 38 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.exists_fixedPointFree` | 47 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.sharpCopy_facts` | 60 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRef/M11Blocks.lean` (25)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.M11Blocks.diag_of_separating` | 31 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.flips_separate` | 44 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.pure_mem_maxSetB` | 154 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.maxSetB_bounds` | 179 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.maxSetB_blockA` | 197 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.maxSetB_blockB` | 204 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.sum_sgn_sq2` | 217 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.maxSetB_blockC` | 232 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.maxSetB_unit` | 251 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.pure_of_eqB` | 312 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.quad_blockw` | 441 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.m11_blocks` | 523 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.pureSetB_span` | 673 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.m11_blocks_polytope` | 706 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.m11_blocks_polytope_flips` | 736 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.maxSetCX_eq_blocks` | 819 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.pureSetCX_eq_blocks` | 833 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.maxSetX_eq_blocks` | 844 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.pureSetX_eq_blocks` | 853 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.maxSet_eq_blocks` | 866 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.pureSet_eq_blocks` | 883 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.m11_cube_cross_polytope` | 897 | theorem | propext, Classical.choice, Quot.sound | `dd812e3` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.maxSetB_convex` | 919 | theorem | propext, Classical.choice, Quot.sound | `7728d59` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.pureSetB_finite` | 945 | theorem | propext, Classical.choice, Quot.sound | `7728d59` | L5 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.blocks_hyps_consistent` | 968 | theorem | propext, Classical.choice, Quot.sound | `7728d59` | L5 |  |

### `formal/lean/GTAO/Rnd/SelfRef/M11BlocksChecks.lean` (3)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.M11Blocks.sep_necessary` | 31 | theorem | propext, Classical.choice, Quot.sound | `c7ed55d` | L6 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.flipA_pureSetB` | 49 | theorem | propext, Classical.choice, Quot.sound | `c7ed55d` | L6 |  |
| `GTAORnd.SelfRef.LR3.M11Blocks.flipA_hull_pureSetB` | 76 | theorem | propext, Classical.choice, Quot.sound | `c7ed55d` | L6 |  |

### `formal/lean/GTAO/Rnd/SelfRef/M11Cube.lean` (25)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.M11Cube.flip_invariant_diag` | 65 | theorem | propext, Classical.choice, Quot.sound | `c43acfe` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.swap_invariant_blocks` | 100 | theorem | propext, Classical.choice, Quot.sound | `c43acfe` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.pureProd_mem_maxSet` | 158 | theorem | propext, Classical.choice, Quot.sound | `c43acfe` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.maxSet_sq_le` | 169 | theorem | propext, Classical.choice, Quot.sound | `c43acfe` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.pure_of_sq_one` | 200 | theorem | propext, Classical.choice, Quot.sound | `c43acfe` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.avgGram_invariant` | 230 | theorem | propext, Classical.choice, Quot.sound | `c43acfe` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.avgGram_diag_ge_one` | 237 | theorem | propext, Classical.choice, Quot.sound | `c43acfe` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.diag_form_max` | 256 | theorem | propext, Classical.choice, Quot.sound | `c43acfe` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.m11_cube_into` | 279 | theorem | propext, Classical.choice, Quot.sound | `c43acfe` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.m11_cube` | 317 | theorem | propext, Classical.choice, Quot.sound | `c43acfe` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.pureProdX_mem_maxSetX` | 372 | theorem | propext, Classical.choice, Quot.sound | `85da274` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.maxSetX_bounds` | 399 | theorem | propext, Classical.choice, Quot.sound | `85da274` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.sum_sgn_sq` | 440 | theorem | propext, Classical.choice, Quot.sound | `85da274` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.maxSetX_frob` | 458 | theorem | propext, Classical.choice, Quot.sound | `85da274` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.sq_le_of_l1` | 496 | theorem | propext, Classical.choice, Quot.sound | `85da274` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.maxSetX_unit` | 527 | theorem | propext, Classical.choice, Quot.sound | `85da274` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.pure_of_eqX` | 571 | theorem | propext, Classical.choice, Quot.sound | `85da274` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.quad_blocks` | 624 | theorem | propext, Classical.choice, Quot.sound | `85da274` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.m11_cross_into` | 655 | theorem | propext, Classical.choice, Quot.sound | `85da274` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.m11_cross` | 709 | theorem | propext, Classical.choice, Quot.sound | `85da274` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.autSet_finite` | 799 | theorem | propext, Classical.choice, Quot.sound | `9b7353d` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.pureSet_span` | 882 | theorem | propext, Classical.choice, Quot.sound | `9b7353d` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.pureSetX_span` | 920 | theorem | propext, Classical.choice, Quot.sound | `9b7353d` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.m11_cube_polytope` | 989 | theorem | propext, Classical.choice, Quot.sound | `9b7353d` | L4 |  |
| `GTAORnd.SelfRef.LR3.M11Cube.m11_cross_polytope` | 1009 | theorem | propext, Classical.choice, Quot.sound | `9b7353d` | L4 |  |

### `formal/lean/GTAO/Rnd/SelfRef/M11Prime.lean` (10)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.M11Prime.moment_quad` | 30 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.M11Prime.moment_trace` | 58 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.M11Prime.star_equiv` | 72 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.M11Prime.max_pos_corr` | 119 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.M11Prime.lemma1_general` | 133 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.M11Prime.hull_strict` | 184 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.M11Prime.average_invariant` | 206 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.M11Prime.final_assembly` | 238 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.M11Prime.invariant_form_scalar` | 259 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.M11Prime.cross_term_zero` | 273 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/Modular.lean` (9)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.Modular.r_covBy` | 55 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Modular.r_step_le` | 94 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Modular.modular_of_semimodular` | 123 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Modular.lower_of_upper_ortho` | 240 | theorem | propext | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Modular.modular_of_upper_ortho` | 251 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Modular.orthomodular_of_upper_ortho` | 257 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Modular.finite_of_atomistic` | 268 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Modular.upper_of_atomistic_covering` | 291 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.Modular.orthomodular_of_atomistic` | 317 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/OControl.lean` (4)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.ball_O_not_SFP` | 32 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.qubit_O3_not_SFP` | 47 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.SO1_trivial` | 52 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |
| `GTAORnd.SelfRef.LR3.sphere_one_two_points` | 63 | theorem | propext, Classical.choice, Quot.sound | `d7add19` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/OnsetO.lean` (10)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.OnsetO.isMin_iff_local` | 67 | theorem | propext, Classical.choice, Quot.sound | `7ace8c0` | L5 |  |
| `GTAORnd.SelfRef.LR3.OnsetO.Setting.projection` | 151 | theorem | propext, Classical.choice, Quot.sound | `7ace8c0` | L5 |  |
| `GTAORnd.SelfRef.LR3.OnsetO.Setting.onset_union` | 173 | theorem | propext, Classical.choice, Quot.sound | `7ace8c0` | L5 |  |
| `GTAORnd.SelfRef.LR3.OnsetO.Setting.supporting_iff` | 209 | theorem | propext, Classical.choice, Quot.sound | `7ace8c0` | L5 |  |
| `GTAORnd.SelfRef.LR3.OnsetO.Setting.tie_at_wstar` | 230 | theorem | propext, Classical.choice, Quot.sound | `7ace8c0` | L5 |  |
| `GTAORnd.SelfRef.LR3.OnsetO.Setting.kkt` | 242 | theorem | propext, Classical.choice, Quot.sound | `7ace8c0` | L5 |  |
| `GTAORnd.SelfRef.LR3.OnsetO.Setting.wstar_anti` | 276 | theorem | propext, Classical.choice, Quot.sound | `7ace8c0` | L5 |  |
| `GTAORnd.SelfRef.LR3.OnsetO.Setting.wstar_one` | 291 | theorem | propext, Classical.choice, Quot.sound | `7ace8c0` | L5 |  |
| `GTAORnd.SelfRef.LR3.OnsetO.Setting.zero_stake` | 295 | theorem | propext, Classical.choice, Quot.sound | `7ace8c0` | L5 |  |
| `GTAORnd.SelfRef.LR3.OnsetO.example_values` | 325 | theorem | propext, Classical.choice, Quot.sound | `7ace8c0` | L5 |  |

### `formal/lean/GTAO/Rnd/SelfRef/OrbitClone.lean` (4)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.no_linear_clone_orbit` | 57 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.no_linear_clone_moved` | 97 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.measure_prepare_clones` | 109 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.measure_prepare_covariant` | 120 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRef/Precision.lean` (7)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.R78.ball_record_bound` | 36 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.chord` | 72 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.disk_record_error` | 86 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.disk_error_linear` | 93 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.disk_exceeds_ball` | 119 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.mixture_copy_core` | 133 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.no_copy_mixture` | 145 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRef/QubitWitness.lean` (2)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.qubit_attains_bound` | 75 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.qubit_bound_tight` | 97 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/R34.lean` (4)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.fourier_core` | 42 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.no_linear_clone_gpt` | 66 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.F1_cycle_count` | 82 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.SelfRef.R3_full` | 116 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRef/SFP.lean` (12)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.R78.jordan_derangement` | 41 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.finite_transitive_not_SFP` | 79 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.simplex_not_SFP` | 88 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.square_rotation_moves_all` | 93 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.square_not_SFP` | 101 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.SO_odd_fixes_unit` | 110 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.SO_odd_fixes_poles` | 144 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.SO3_fixes_poles` | 153 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.odd_ball_SFP` | 172 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.SO2_nonid_no_fixed` | 178 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.disk_not_SFP` | 211 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |
| `GTAORnd.SelfRef.R78.even_ball_not_SFP` | 225 | theorem | propext, Classical.choice, Quot.sound | `aac249c` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRef/SFPCriterion.lean` (5)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.ball_SFP_iff_odd` | 38 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.complex_fixes_ray` | 52 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.unitary_fixes_ray` | 64 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.real_odd_fixes_ray` | 70 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.real_even_not_SFP` | 109 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/Transport.lean` (8)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.Transport.hept_step_le` | 147 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.Transport.hept_partner` | 191 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.Transport.hept_path_cost` | 223 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.Transport.disk_dist` | 328 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.Transport.disk_cost_ge` | 361 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.Transport.disk_cost_attained` | 376 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.Transport.disk_partner` | 385 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |
| `GTAORnd.SelfRef.LR3.Transport.hept_beats_disk` | 397 | theorem | propext, Classical.choice, Quot.sound | `80cf785` | L3 |  |

### `formal/lean/GTAO/Rnd/SelfRef/TransportHorizons.lean` (8)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.SelfRef.LR3.TransportHorizons.disk_cost_T2` | 30 | theorem | propext, Classical.choice, Quot.sound | `aae3eb5` | L4 |  |
| `GTAORnd.SelfRef.LR3.TransportHorizons.cos_sum4_le` | 37 | lemma | propext, Classical.choice, Quot.sound | `aae3eb5` | L4 |  |
| `GTAORnd.SelfRef.LR3.TransportHorizons.disk_cost_T4_ge` | 64 | theorem | propext, Classical.choice, Quot.sound | `aae3eb5` | L4 |  |
| `GTAORnd.SelfRef.LR3.TransportHorizons.disk_cost_T4_attained` | 75 | theorem | propext, Classical.choice, Quot.sound | `aae3eb5` | L4 |  |
| `GTAORnd.SelfRef.LR3.TransportHorizons.nona_step_le` | 141 | theorem | propext, Classical.choice, Quot.sound | `33657cf` | L4 |  |
| `GTAORnd.SelfRef.LR3.TransportHorizons.nona_partner` | 187 | theorem | propext, Classical.choice, Quot.sound | `33657cf` | L4 |  |
| `GTAORnd.SelfRef.LR3.TransportHorizons.nona_path_cost` | 219 | theorem | propext, Classical.choice, Quot.sound | `33657cf` | L4 |  |
| `GTAORnd.SelfRef.LR3.TransportHorizons.nona_beats_disk` | 232 | theorem | propext, Classical.choice, Quot.sound | `33657cf` | L4 |  |

### `formal/lean/GTAO/Rnd/SelfRefRun/Basic.lean` (7)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `SelfRefRun.liar_half` | 32 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 | padding (README:477) |
| `SelfRefRun.exists_derangement` | 39 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `SelfRefRun.four_point` | 53 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `SelfRefRun.no_copier_four_point` | 67 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `SelfRefRun.perm_periodic` | 79 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `SelfRefRun.path_sq_one_const` | 85 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `SelfRefRun.midpoint_rho` | 105 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SelfRefRun/Round2.lean` (2)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `SelfRefRun.no_zero_drift_while_recording` | 28 | theorem | none | `202f6cf` | R1–2 |  |
| `SelfRefRun.normal_fixer_trivial` | 34 | theorem | propext | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/Spekkens.lean` (5)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.Spekkens.forced` | 40 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.Spekkens.no_injective_clone` | 57 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.Spekkens.no_perm_clone` | 65 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.Spekkens.disjoint_pair_clonable` | 83 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.Spekkens.singletons_clonable` | 96 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |

### `formal/lean/GTAO/Rnd/SquareBit.lean` (3)

| name | line | kind | axioms | commit | round | note |
|---|---|---|---|---|---|---|
| `GTAORnd.square_capacity_le_two` | 112 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.square_B1_hypotheses` | 189 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
| `GTAORnd.square_no_clone` | 218 | theorem | propext, Classical.choice, Quot.sound | `202f6cf` | R1–2 |  |
