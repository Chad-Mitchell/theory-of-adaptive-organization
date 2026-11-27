# Hostile review: Lean round 3 on `forge-rnd-record-cost-2` at 4c693b6 (statement fidelity)

*Thursday 26 November 2026, 05:05 ET. Fresh-context executor for Forge. Fresh clone in the persistent folder `/workspace/review-lean3/repo` (HEAD 4c693b6). No commit, no push. `THEORY.md`, `CORE.md` and locked blobs untouched. In-model only. Logs are copied beside this file: `build.log`, `check_lean.log`, `rndaxioms.out`, `pr295_body.md` (PR body as of 2026-11-26 04:54:27 ET).*

Commits in scope:
- b40e87a: L5 (`Broadcast.lean`, `BroadcastControl.lean`)
- 80cf785: batch 2 (`SFPCriterion`, `Transport`, `CostDialGlobal`, `QubitWitness`, `FiniteGeometry`, `Composite`)
- d7add19: batch 3 (`OControl`, `Modular`, `Entangle`, `M11Prime`)
- e4acb0f: batch 4 (`classical_no_purification`)
- d699a1f: batch 5 (`extreme_trivial_decomp`, `cnot_mixed_correlated`)
- merges 3388a21, 1c59736, 4c693b6

## 0. Mechanical checks: all confirmed

- **`lake build`** (after `lake exe cache get`): "Build completed successfully (18419 jobs)", 0 warnings and 0 errors.
- **`tools/check_lean.sh`:** OK. It reports "AxiomAudit: OK (1923 GTAO declarations; only propext, Classical.choice, Quot.sound)".
  - That equals `formal/lean/AUDIT.json` (`audit_count` 1923, audited at d699a1f).
  - `sources_sha256` 16657776… recomputes identically with `tools/check_pending.lean_sources_sha256`.
  - The script's header says to run it only in `/tmp/gtao-lean`. I ran it in the persistent clone as instructed; it passed.
- **`#print axioms` (`scripts/RndAxioms.lean`):** 157 `#print axioms` lines and 157 outputs.
  - Every output is within {propext, Classical.choice, Quot.sound}. `SelfRefRun.no_zero_drift_while_recording` uses none.
  - The output is byte-identical to the committed `theory/record-cost-2026-11-25/rnd_axioms_lr3e.out` (name lines).
- **Count 157 / 152:** confirmed.
  - The only duplicated short name is `liar_half` (two namespaces).
  - 157 − {`SelfRefRun.liar_half`, `P2_entries`, `local_map_tmul`, `swap_tmul`, `le4_attained`} = 152.
  - The 48 helper lemmas in the round 3 files are not in RndAxioms, which is fine; AxiomAudit covers them.
- **No `sorry`, `admit`, `native_decide`, `axiom`, `unsafe` or `implemented_by`** in `GTAO/**` or `scripts/`. The only match is the comment in `AxiomAudit.lean:10`.
- **No committed theorem renamed or edited:**
  - Against upstream `main` (8b553c6), every `.lean` under `GTAO/` has 0 deleted lines.
  - Within the branch, the only commit that touched a `.lean` file again is `Entangle.lean` (d7add19 → e4acb0f → d699a1f), and the later two hunks append at end of file.
  - `RndAxioms.lean` deletions are only its header count lines (62→81→85→91→122→154→155→157).

## 1. Findings by severity

**High:** none. Every statement I read is true as typed (Lean checks that). None carries a hypothesis that is its own conclusion. None is vacuous: controls exist (`L5_control`, `qubit_attains_bound`, `cube_corr_tight`, `odd_ball_SFP` non-empty).

**Medium**

- **M1. M11′ is not assembled in Lean.**
  - **What `final_assembly` is.** A 12-line set lemma: if T maps E onto E, q∘T = q, and q is strictly larger on P than on E∖P, then T maps P onto P.
  - **Where the content sits.** Both the invariance of q under every reversible map of the composite (`hq`) and the strict separation (`hstrict`) are hypotheses. `hstrict` is the mathematical core of M11′: product pure states are the unique maximizers of the invariant quadratic.
  - **What deriving `hstrict` needs:**
    - the Schur step, including the tensor-product block, which is NOT formalized, to fix the form of q on the C block;
    - then `lemma1_general`, `hull_strict` and the Lemma 2 forms, chained.
  - **What exists today.** No Lean theorem states M11′, and the steps are not chained. Each step is proved under its own hypotheses (`star_equiv`, `max_pos_corr`, `lemma1_general`, `hull_strict`, `average_invariant`, `invariant_form_scalar`, `cross_term_zero`). `final_assembly` is the trivial last implication.
  - **Wording.** README :340 ("Faithful, elementary … Schur block … not formalized") is accurate. RC13 ("proves the Lean-able steps of M11′ (… the final step …)") and round 10 :215 are accurate in letter, but they read as "M11′ mostly in Lean". Fix with the text in §3.
- **M2. The PR #295 body's Lean section is stale and incomplete.**
  - The title still says "(85 theorems)".
  - The section stops at 80cf785: "AUDIT 1808 at 539ffa5; RndAxioms lists 122".
  - It does not mention batches 3–5 (35 theorems: OControl, Modular, Entangle, M11Prime, purification and round C controls), the current counts (157 names / 152 without padding; AUDIT 1923 at d699a1f), or the M11′ gap in M1.
  - It overclaims nothing, but as the public description it is out of date.
- **M3. `classical_no_purification`: README :334 says "Purification … is not implied by the other premises".**
  - Lean shows only that classical theory (simplex on Fin m × Fin n) lacks purification.
  - An independence claim would need a model that satisfies the other premises (named) and fails purification. Classical theory fails U/P3, so it is not that model.
  - Drop the clause or name the premises and the model.

**Low**

- **L1. `orthomodular_of_atomistic` needs finitely many atoms, not just finite height.**
  - The hypothesis `hfin` makes the lattice finite. The orthocomplement is an abstract `Ortho` (antitone involution with complements). Its identification with "perfectly distinguishable from" on a GPT face lattice is a premise; round 10 :97 says so, correctly.
  - The errata line "finite height plus atomistic plus covering plus orthocomplement gives modular" (PR body line 91) is stronger than Lean. It is enough for the round 10 use, which is a proof by contradiction that assumes finitely many atoms. Say "finitely many atoms" when citing.
  - The theorem is genuine (Jordan–Dedekind → Dilworth–Birkhoff → orthomodular), not trivial.
- **L2. `SFPCriterion.lean` docstring says "What is proved are the cases the survivor table uses".**
  - The pass/fail list at rounds 4–9 :42 also has quaternionic QM (all d), octonionic d = 3, "even balls (any transitive group)", G₂ on B⁷, and the C1 orbitope. None is in Lean.
  - The README, RC5 and errata §9 say "concrete cases", which is correct.
  - `complex_fixes_ray` is the fundamental theorem of algebra (an eigenvector exists). `unitary_fixes_ray` is a restatement of it.
  - `real_even_not_SFP` exhibits one matrix with no eigenvector (det = 1, so it also lies in SO(2m)) rather than stating `¬ SFP`. The content is the same.
  - `ball_SFP_iff_odd` is correct, including n = 0 (empty sphere, Odd 0 false).
- **L3. `L5_perfect` closedness.**
  - `IsClosed (achSet G x y)` carries the limit step from `L5_asymptotic` to perfect. It is a fair hypothesis, not the conclusion.
  - The docstring says it is "true when the effect set is compact, e.g. any finite-dimensional GPT with a closed effect cone". That is not provable in `CopyModel`, which has no topology. It is a true remark about finite-dimensional GPTs, but outside Lean.
  - The control is only the classical bit, where the conclusion is immediate. The result covers cloning, not broadcasting of mixed states, and is pairwise, not joint. README :295 says all this. Safe to cite with the three hypotheses.
- **L4. `Jdial_midpoint_global` / `_unique` / `_60_global` hold only at the tuned weight `wRD = qκ/(4cos(β/2))`** (ρ = 1/(2cos(β/2))), where the midpoint is stationary by construction. The README states this. Commit 80cf785's title, "cost-dial global minimum for beta <= pi/2", omits the tuned ρ. Cite as "at ρ = 1/(2cos(β/2)), 0 < β ≤ π/2".
- **L5. `hept_beats_disk` is T = 3 only** and makes these choices:
  - one fixed 7-gon vertex path (cost bounded above by 3λ² < 0.67, not computed);
  - disk paths through pure states only;
  - the disk partner fixed to p π (its uniqueness is not formalized);
  - unit price per squared operational distance (the κ term cancels at equal dimension 2).
  - The README, RC10 and round 10 :165 are accurate.
  - RC10's "(at every finite horizon it is a hypothesis)" is ambiguous. Prefer "at untested horizons it is a hypothesis".
- **L6. LE1 `pure_marginal_extreme`.**
  - The added normalization hypothesis (`uA·w = 1` on Ω) is standard, not conclusion-carrying, and is needed: the worker's counterexample (triangle (1,0), (2,±1), x = (1,0)) is right.
  - The load-bearing modelling input is `hcone` (each conditional X f_q is in the cone over Ω). That is the max-composite property with no-restriction on A, and it is assumed (entanglement note §5; review E1 row 2a).
  - Safe to cite with `hcone`, `hspan` and the unit combination stated.
- **L7. `reversible_preserves_pure` is one line** (`image_extremePoints` from Mathlib). It is true and elementary; count it as a restatement.
- **L8. `cnot_mixed_correlated`.**
  - `cnotState` is defined directly as ½δ₀₀ + ½δ₁₁. The CNOT map is not formalized.
  - "Not a product" is shown by one entry (½ ≠ ¼).
  - The docstring's "so a mixed whole can carry a perfect record" and NOTE_C's "I(A:B) = 1 bit" are not in Lean.
- **L9. `le4_attained` is `1/2 + (1/3)(3/2) = 1`.** That point, β = (½, ½, ½), violates `le4_bound`'s own hypothesis (Σ|β| = 3/2 > 1/2). It is the all-reads value, not attainment of the 2/3 bound, so the name misleads. It is already excluded as padding.
- **L10. Padding beyond the declared 5.** At least these are one-line wrappers, instances or restatements:
  - `unitary_fixes_ray`, `qubit_O3_not_SFP`, `reversible_preserves_pure`, `final_assembly`
  - `finite_divring_comm` (`littleWedderburn`), `chevalley_nonzero_zero` (Mathlib Chevalley–Warning)
  - `rho_60`, `Jdial_60_global`, `SO1_trivial`, `sphere_one_two_points`, `moment_trace`
  - the second conjunct of `qubit_bound_tight` (finrank ℝ³ = 3)

  "152 without padding" therefore still overstates depth. Suggest "152 names, of which about 12 more are one-line instances or Mathlib wrappers".
- **L11. Stale or inconsistent note text after in-place status edits.**
  - b40e87a, 80cf785 and d7add19 edit committed lines in place: rounds 4–9 :83 and :85, round 10 :97, :165 and :215, and CLAIM_MAP RC1, RC5, RC8 and RC13. These are status cells, not theorems or prereg/log lines, but the edits are not append-only.
  - Rounds 4–9 :46 still says L5 is "partial in Lean", contradicting the edited :83.
  - Rounds 4–9 :42 cites "Hopf and Samelson 1941". Crossref dates 10.1007/BF01378063 to 1940 (Comment. Math. Helv. 13:240–251).
- **L12. Docstring nits.**
  - `final_assembly` says "T is a bijection", but only `T '' E = E` is assumed. The theorem is stronger than the docstring; harmless.
  - `M11Prime.lean`'s header says "a repository note for it is pending". Round 10 §17 now exists.

## 2. Per-theorem fidelity table (priority targets)

| Theorem | Trivial / vacuous / circular? | Name or docstring overclaim? | Ledger and PR text |
|---|---|---|---|
| `star_equiv` | Genuine, short (averaging identity) | No | RC13 accurate |
| `max_pos_corr` | Elementary (4 linear inequalities) | No | accurate |
| `lemma1_general` | Genuine; the moment constant is forced by trace | No | accurate |
| `hull_strict` | Standard strict convexity of the Euclidean ball | No | accurate |
| `average_invariant` | Standard averaging, finite group | No | accurate |
| `final_assembly` | **Trivial set lemma; the core inequality is a hypothesis** | **Name suggests M11′ is assembled** | RC13 / round 10 :215 need the M1 clarification |
| `invariant_form_scalar`, `cross_term_zero` | Schur, scalar part only; absolute irreducibility is a hypothesis | No | accurate ("tensor block not formalized") |
| `orthomodular_of_atomistic` | Genuine | Needs "finitely many atoms"; Ortho abstract | RC8 accurate; errata "finite height" is stronger than Lean (L1) |
| `L5_perfect` | Closedness is a fair hypothesis | Docstring remark not provable in-model (L3) | RC5 and rounds 4–9 :83 accurate; :46 stale |
| `ball_SFP_iff_odd` + concrete cases | Correct; complex case elementary | "cases the survivor table uses" overclaims (L2) | RC5, errata §9 accurate |
| `hept_beats_disk` | Genuine at T = 3 | No | RC10 accurate (wording nit) |
| `Jdial_*_global` | Genuine at tuned ρ | Commit title omits ρ | README accurate |
| `pure_marginal_extreme` (LE1) | Genuine; normalization needed | No | README accurate |
| `reversible_preserves_pure` | One-line Mathlib | No | count as restatement |
| `classical_no_purification` | Elementary control | README's independence clause unsupported (M3) | not in PR body |
| `cnot_mixed_correlated` | Elementary; CNOT not modelled | "perfect record" not in Lean | not in PR body |

## 3. Erratum and ledger text to route (append-only)

1. **RC13, append to the Lean column:** "No Lean theorem states M11′ and the Lean steps are not chained. `final_assembly` takes as hypotheses the invariance of q under every reversible map and the strict separation of product pure states (the core of M11′); deriving that separation needs the tensor-product Schur block, which is not formalized."
2. **Round 10 note, after :215 (append):** the same sentence, plus "`final_assembly` is an elementary set lemma."
3. **`formal/lean/README.md` :334, append a scope note:** "`classical_no_purification` shows only that classical theory lacks purification; it does not show purification is independent of the other premises (classical theory fails U)."
4. **Errata §10 (append):**
   - `orthomodular_of_atomistic` assumes finitely many atoms (a finite lattice), not only finite height.
   - The `SFPCriterion.lean` docstring's "cases the survivor table uses" covers balls with SO(n), complex QM and real QM only; quaternionic, octonionic, G₂ and the C1 orbitope are not in Lean.
   - The Jdial global results hold at ρ = 1/(2cos(β/2)).
   - `le4_attained` is the all-reads value at a point outside `le4_bound`'s hypothesis.
   - Rounds 4–9 :46 ("partial in Lean") is superseded by :83 (L5 in Lean round 3).
   - Hopf–Samelson is 1940 (Crossref 10.1007/BF01378063).
5. **PR #295 body, Lean section and title** (needs your approval to edit):
   - Title: "with Lean (157 theorems; 152 without padding)".
   - Add: "Lean round 3 batches 3–5 (d7add19, e4acb0f, d699a1f): `OControl`, `Modular`, `Entangle`, `M11Prime`; AUDIT 1923 at d699a1f; RndAxioms 157 names, 152 without the five declared paddings, about 12 more one-line instances. M11′: steps only; no Lean statement of M11′; the tensor Schur block is not formalized."
6. **RC10 wording:** "at every finite horizon it is a hypothesis" becomes "at untested horizons it is a hypothesis". Append a correction line; don't edit the row in place, if the ledger is append-only.

## 4. Safe to cite in the index (with the stated hypotheses)

| Topic | Theorems |
|---|---|
| M11′ steps | `star_equiv`, `max_pos_corr`, `lemma1_general`, `hull_strict`, `average_invariant`, `invariant_form_scalar`, `cross_term_zero` (as separate steps of M11′, not M11′ itself) |
| Composite | `cube_corr_bound`, `square_corr_bound`, `square_C_bound`, `cube_corr_tight`, `square_pure_marginal`, `pure_marginal_finite`, `pure_marginal_product`, `pure_marginal_factorizes` |
| Lattice | `r_covBy`, `modular_of_semimodular`, `orthomodular_of_upper_ortho`, `upper_of_atomistic_covering`, `orthomodular_of_atomistic` (finitely many atoms; Ortho as premise) |
| L5 | `L5_asymptotic`, `L5_perfect` (closed achievable set), `L5_pairwise`, `L5_control` |
| SFP | `ball_SFP_iff_odd`, `complex_fixes_ray`, `real_odd_fixes_ray`, `real_even_not_SFP`, `ball_O_not_SFP` |
| Transport, T = 3 only | `disk_dist`, `disk_cost_ge`, `hept_path_cost`, `hept_beats_disk` |
| Cost dial | `Jdial_midpoint_global` and `Jdial_midpoint_unique` (tuned ρ, β ≤ π/2 and < π/2) |
| Qubit witness | `qubit_bound_tight` (witness for `dim_bound`) |
| Finite geometry | `finite_divring_comm`, `diag_form_isotropic`, `norm_form_isotropic` (algebra after Piron only) |
| Entanglement | `pure_marginal_extreme` (LE1), `extreme_trivial_decomp`, `simplex_extreme_iff`, `classical_pure_product` |

**Cite only with their caveats:**
- `classical_no_purification` and `cnot_mixed_correlated` as classical controls only;
- `final_assembly` as an elementary lemma, never as "M11′ in Lean".

**Do not cite as results:** `le4_attained`, `local_map_tmul`, `swap_tmul`, `unitary_fixes_ray` (duplicate), `reversible_preserves_pure` (one-line), `qubit_O3_not_SFP` (an instance), `rho_60`.
