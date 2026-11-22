# Independent hostile review: PR #147 (T19 Lean core extension)

**Reviewer:** independent (wrote none of the PR, the `formal/lean/` library, `tools/check_lean.sh`, or the OPEN_WORK T19 edit).
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/147
**Head:** `40e99ea7541dbb4744a55e43012efb18d4f26747` on `lean-core-2026-11-21` (two commits: `03a19bd`, `40e99ea`).
**Base:** `c92886af97425102878241740b093983885a0106` (`main`). Merge-base equals the base. Diff is 9 files, +1178/−7.
**Verdict: READY-WITH-FIXES**

No blocker. The four new headline statements say what the README’s “what is proved” column says, the hypotheses are satisfiable, and none of the vacuity patterns checked below is present. Two section pointers in the same README are wrong against the current `CORE.md`, and one of them now collides with a correct use of “CORE §3”. Fix those before treating the mapping table as the claim. Do not merge on the strength of the proofs alone while that table still points the Gibbs theorem at the layer-lifetime section.

---

## What was checked

- `git diff --stat c92886a..40e99ea` and a line-by-line reading of `GTAO/LayerLifetime.lean`, `GTAO/LocalShared.lean`, `GTAO/Equipartition.lean`, `GTAO/HullWalk.lean`, `scripts/AxiomAudit.lean`, and the README mapping rows those files add.
- Each of those statements against CORE §3 and §4, `theory/LAYER_LIFETIME_2026-11-21.md` §2 and §5, `theory/SELECTION_AXIOMS.md` SA1b / SA2, THEORY §4, and `core/KEYSTONE_NOTE.md` §4.
- `nice -n 19 tools/check_lean.sh` from a tree with no toolchain and no `.lake/` (elan installed in this review, pin `leanprover/lean4:v4.37.0-rc1`).
- An independent dump of every environment constant whose defining module has prefix `GTAO`, compared with the source declarations.
- A whole-token grep of `formal/lean/**/*.lean` outside `.lake/` for `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `implemented_by`.
- `python3 tools/check_fresh.py`, `python3 tools/check_consistency.py`, `python3 tools/check_open_work.py`, and `nice -n 19 python3 -m pytest -q tools`.
- Byte comparison of the Part 2 hypothesis sentence, and `git diff --name-only c92886a..HEAD` against locked paths.

---

## Build, axioms, audit coverage

- `tools/check_lean.sh` exits 0. Cache get, then `lake build`: **5835 jobs, “Build completed successfully”**. Then `AxiomAudit: OK (312 GTAO declarations; only propext, Classical.choice, Quot.sound)`. Final line `check_lean.sh: OK`.
- Toolchain `lean-toolchain` is `leanprover/lean4:v4.37.0-rc1`. `lakefile.toml` requires mathlib `v4.37.0-rc1`. The fetched mathlib commit is `31ce06eaadf4a200c0e1407c5f10953cf606b8f8`.
- The token scan inside `check_lean.sh` is restricted to `GTAO.lean` and `GTAO/*.lean` and it passed, so none of those files contains the forbidden tokens even inside comments.
- Independent grep of every `*.lean` under `formal/lean/` except `.lake/` and `lake-packages/`: **one hit**, `formal/lean/scripts/AxiomAudit.lean:10`, the word `` `sorry` `` inside a comment explaining that a `sorry` would surface as `sorryAx`. That file is not in `check_lean.sh`’s source list. `tools/test_lean.py` strips line and block comments before the same token regex, so the comment is not a hit there either. There is no `sorry` / `admit` / `axiom` / `native_decide` / `unsafe` / `implemented_by` tactic or declaration in the project sources. No `private` declaration keyword in `GTAO.lean` or `GTAO/*.lean`.
- A second Lean program, importing `GTAO` and walking `env.constants` with the same `` (`GTAO).isPrefixOf `` test the audit uses, prints **COUNT 312** and the same module set the audit claims. Modules with constants: `GTAO.CT10` (4), `CT20` (4), `CT22` (17), `CT33` (6), `CT34` (27), `CT4` (15), `Cost` (29), `Equipartition` (56), `Hull` (34), `HullWalk` (78), `LayerLifetime` (22), `LocalShared` (20). `GTAO.lean` is imports only, so the root module contributes no constant; the prefix test would have counted one if it existed. Of the 312, 77 names contain `_private` (generated auxiliaries, including `LocalShared.crossing_root_eq` simp lemmas). They are in the imported environment and in the audit, not skipped.
- `Lean.collectAxioms` (`Lean/Util/CollectAxioms.lean` in the v4.37.0-rc1 toolchain) uses the axiom list computed when the olean is exported. That export walks constant bodies in the private environment, so a `sorryAx` or any other axiom reachable from a public declaration through a private auxiliary is stored on the public declaration. The audit’s `collectAxioms` call is that list. A custom axiom or a `sorry` would have failed it. `native_decide` depends on `Lean.ofReduceBool`, which is not one of the three allowed names.
- Every hand-written declaration name in `GTAO/*.lean` appears in the 312, including `LayerLifetime.layer_lifetime`, `LocalShared.switch_iff`, `Equipartition.gibbs_excess`, `Equipartition.gibbs_excess_quadratic`, and `HullWalk.hull_increment_test_eq_argmin`. The README’s “Last run: 312 declarations, OK” matches this run.

---

## Faithfulness

Labels are the Lean statement against the prose it is mapped to. “Assumed” means a Lean hypothesis or an expression the README says is an input. “Proved” means a conclusion of a theorem that typechecks with only the three standard axioms.

### `LayerLifetime.layer_lifetime` — FAITHFUL

`GTAO/LayerLifetime.lean:103-115`. For `k, w, σ² > 0` (`s` stands for `σ²`):

- `Tstar (1/6) k w s = √(6k/(w s))`
- that value minimizes `cost = k/T + (w s) T / 6` over every `T > 0`
- any other `T > 0` with cost at most that value equals it
- the minimum value is `2 √(k w s / 6)`

That is the unique-minimizer claim in the README row and in OPEN_WORK T19 (a). It is the right domain. On `T < 0`, with `k > 0` and `w σ² / 6 > 0`, the same expression tends to `−∞`, so there is no minimizer on `ℝ \ {0}`. The theorem does not claim one.

CORE §3 (`CORE.md:44-50`) states the expected time between resets of the optimal barrier, `T* = √(6k/(wσ²))`, as KNOWN at zero discount (Chalkley 1997; Dixit 1991). `theory/LAYER_LIFETIME_2026-11-21.md:30` states the same `T*` and the excess rate `2√(kwσ²/6)`. Lean does not derive the mean exit time `b²/σ²` or the time-average square gap `b²/6`. The README row says that derivation is assumed. Given the cost `k/T + wσ² T/6`, the calculus fact is what CORE’s formula is the minimizer of, and the AM–GM identity in `amgm_identity` is the standard one: `k/T + a T − 2√(k a) = (√a T − √k)² / T`.

The fixed-period cousin matches §2 of that note: `T*_fix = √(2k/(wσ²))`, minimum `√(2 k w σ²)`, and `√(6k/(wσ²)) = √3 · √(2k/(wσ²))`. `barrier_band_identities` is SA2’s algebra (`theory/SELECTION_AXIOMS.md:126`): with `b*² = √(6kσ²/w)`, both `w b*²/6` and `k σ²/b*²` equal `√(kwσ²/6)`, and `b*²/σ² = T*`. `lifetime_ratio` is the equal-stake Model LS ratio in CORE §3 and LAYER_LIFETIME §3a. Uniqueness for a general coefficient `c` is `Tstar_unique`; `fixed_period_lifetime` restates existence of the minimizer and the value, which is all its README row claims.

### `LocalShared.switch_iff` — FAITHFUL

`GTAO/LocalShared.lean:140-166`. For `e, N, w > 0`, `k_S, k_L ≥ 0`, `ℓ ≥ 0`, the following are equivalent:

- there is `σ² > 0` with shared cost strictly below local cost, and there is `σ² > 0` with local cost at most shared cost
- `ℓ > 0` and `k_S < N k_L`

The README defines “drift switch” as that pair of existentials (“strictly cheaper at some `σ² > 0`, not cheaper at another”). CORE’s D5 sentence (`CORE.md:11` and, in the same words of substance, `CORE.md:60`) is that the fast-local / slow-shared crossing needs delay on the shared channel only and a shared lump cheaper than `N` local ones. LAYER_LIFETIME §5 (`:84-89`) is the same iff, plus the crossing formula.

The cost definitions match that note at the two coefficients the note uses. Local `N e √(k_L w σ²)` and shared `e √(k_S (N w) σ²) + N w σ² ℓ`. At `e = √2` those are `N √(2 k_L w σ²)` and `√(2 k_S (N w) σ²) + N w σ² ℓ`. The crossing `sigma2Star` at `e = √2` is the displayed

`σ²* = ((√(2 k_L w) − √(2 k_S w / N)) / (w ℓ))²`.

`crossing` (`:118-135`) is `shared < local ↔ σ² < σ²*` for `σ² > 0`, under `ℓ > 0` and `k_S < N k_L`. `no_switch_without_delay` is “at `ℓ = 0`, shared is cheaper at a given `σ² > 0` iff `k_S < N k_L`”, independent of the drift. `shared_never_wins` is the `k_S ≥ N k_L`, `ℓ ≥ 0` direction. `equal_delay_no_switch` adds the same floor `N w σ² ℓ` to the local cost and recovers the `ℓ = 0` comparison, which is §5’s cancellation. `barrier_crossing_eq_fixed_div_three` is `(2/√6)² / (√2)² = 1/3`, the note’s “barrier crossing is the fixed-period crossing divided by 3”.

The hypotheses are satisfiable (`e = N = w = ℓ = k_L = 1`, `k_S = 0` makes the right-hand side true; `k_S = k_L` makes it false). Nothing in the statement forces both sides of the iff to be absurd.

### `Equipartition.gibbs_excess` and `gibbs_excess_quadratic` — FAITHFUL

`E_π` is not a named `Measure`. It is the ratio of Bochner integrals against the reference measure `μ`:

`(∫ J(x) exp(−β J(x)) ∂μ) / (∫ exp(−β J(x)) ∂μ) − J*`.

That is the expectation of `J` under the probability density proportional to `exp(−β J)` with respect to `μ`, once the denominator is positive and finite and `J exp(−β J)` is integrable. Both are theorems here, not extra assumptions.

- `HomogCost` (`:63-68`): `p > 0`, `q` continuous, `q ≥ 0`, `q(x) > 0` for `x ≠ 0`, `q(r • x) = r^p q(x)` for `r > 0`. On a nontrivial finite-dimensional real normed space these are inhabited: `homogCost_quadratic` sends a positive definite matrix to a `HomogCost` of degree 2.
- `integrable_exp` and `integrable_moment` prove integrability from the coercivity lemma `q x ≥ m ‖x‖^p` (`m > 0` from the minimum of `q` on the unit sphere). They are not side conditions that can fail while `HomogCost` holds.
- `integral_exp_pos` (Mathlib) gives `0 < ∫ exp(f) ∂μ` when `exp(f)` is integrable and `μ` is not the zero measure. `gibbs_mean_homog` and `gibbs_excess` apply it, so `Z(β) > 0`. The ratio is not the `0/0 → 0` convention Mathlib uses for a non-integrable integrand. A Dirac mass at the minimizer would give excess 0, and `0 = d/(p β)` is false for `d ≥ 1`, `β > 0`. The identity that is proved is the positive number `finrank / (p β)`.
- `μ` is any `IsAddHaarMeasure`. The ratio does not depend on scaling the Haar measure. `gibbs_excess_quadratic` uses `volume` on `Fin d → ℝ`, which is Lebesgue, and rewrites `finrank = d` by `Module.finrank_fin_fun`. The statement’s bare `∫` is that same `volume`.
- Scaling matches Mathlib `integral_comp_smul_of_nonneg`: `∫ f(R • x) ∂μ = R^{−d} ∫ f ∂μ` for `R ≥ 0`. With `R = β^{1/p}` and `q(R • x) = β q(x)`, that is `Z(β) = β^{−d/p} Z(1)` and `N(β) = β^{−1} β^{−d/p} N(1)`, as `Z_scale` and `Nm_scale` state. `Nm_one` is `N(1) = (d/p) Z(1)`, from `e^{−q} − e^{−2q} = ∫_1^2 q e^{−s q} ds` and the scaling on `[1, 2]`. Hence `N(β)/Z(β) = d/(p β)`.
- `gibbs_excess` shifts by `x*` with Haar translation invariance and cancels the constant factor `exp(−β J*)`. The conclusion is `E[J] − J* = d/(p β)` for `J(x) = J* + q(x − x*)`.
- `gibbs_excess_quadratic` (`:319-326`) specializes to `J(x) = J* + ½ (x − x*)ᵀ H (x − x*)`, `p = 2`, so `d/(2β)`. Mathlib `Matrix.PosDef` (`PosDef.lean:176-177`) is `IsHermitian` and `x ≠ 0 → 0 < xᴴ M x`. The README’s “so symmetric” is `PosDef.isHermitian`. `PosDef.one` says the identity is positive definite, so the hypothesis is inhabited for every `d ≥ 1` (`[NeZero d]`). `d = 0` is excluded; the space would not be nontrivial.

This is SA1b’s Gaussian calculation (`theory/SELECTION_AXIOMS.md:62-75`): covariance `(β H)^{−1}`, excess `½ Tr(H Σ) = d/(2β)`, for a quadratic defined on all of `ℝ^d` with density `∝ e^{−β J}` against Lebesgue. The `d/(p β)` row is the homogeneous extension and is what `gibbs_excess` states. SA1 (Sella–Hirsh), the Moran / Wright–Fisher values of `β`, the fractional form `≈ d/(2 σ N_e)`, and the sentence “treat the measure as supported on the quadratic well” are not hypotheses of these theorems. The README and the not-formalized list say they are inputs. That is the right split: the identity is exact for a quadratic on `ℝ^d`; the approximation that a non-quadratic `J` may be replaced by its quadratic well is not formalized.

### `HullWalk.hull_increment_test_eq_argmin` — FAITHFUL

`GTAO/HullWalk.lean:381-388`, using `phi` from `GTAO/Hull.lean:34-35`: `φ(K) = K + R (1 + ε_K)`, the bracket in KEYSTONE_NOTE §4 (`core/KEYSTONE_NOTE.md:74-80`).

KEYSTONE’s proposition (`:80-88`): walk the lower-hull vertices and jump from `k_i` to `k_{i+1}` iff `R (ε_{k_i} − ε_{k_{i+1}}) > (k_{i+1} − k_i)`; the strict test returns the leftmost minimizer of `φ` on `{0, …, n}`, for an arbitrary real sequence, with no convexity hypothesis.

`HullVertices.Pays` (`:59-60`) is that strict inequality. `hull_walk_leftmost_argmin` (`:147-151`) says the stopping vertex `v i*` satisfies `φ(v i*) ≤ φ(j)` for every `j ≤ n`, and `φ(v i*) < φ(j)` for every `j < v i*`. That is a minimizer, and it is the leftmost one. `hull_increment_test_eq_argmin` packages existence: for every `ε : ℕ → ℝ` and every `R ≥ 0` there is `IsLowerHull` vertex data (the greedy minimum-slope chords, `greedy_isLowerHull`) whose walk stops at that leftmost minimizer. `R ≥ 0` includes the note’s `R > 0`. Edges may skip integers (`StrictMono` vertices, not a requirement that they be adjacent). The K\* = 0 end is included (`v 0 = 0`).

The note’s further sentence, that a hull edge of slope exactly `−1/R` consists entirely of minimizers, is not a separate theorem. The README does not claim it. The strict test’s leftmost claim is what the README claims, and it is what is proved.

---

## Assumed versus proved

| Piece | Assumed (not derived in Lean) | Proved |
|---|---|---|
| Layer lifetime | The zero-discount average cost really is `k/T + c w σ² T` (exit time `b²/σ²`, square gap `b²/6`, Chalkley at zero discount). Smooth adjustment, and the OU regime where `T*` is quantitatively false, are out of scope. | Unique minimizer on `T > 0` of that cost; the `c = 1/6` and `c = 1/2` specializations; `√3` ratio; `√k` scaling; equal-stake lifetime ratio; SA2’s two-term band identities. |
| D5 local vs shared | The local and shared cost expressions, including the delay floor `N w σ² ℓ` on the shared observation only. The OU companion (numerical in the note) is not formalized. | `e √(k_S N w) < N e √(k_L w)` iff `k_S < N k_L`; no switch at `ℓ = 0`; shared never strictly wins if `k_S ≥ N k_L` and `ℓ ≥ 0`; shared strictly cheaper iff `σ² < σ²*` when `ℓ > 0` and `k_S < N k_L`; a switch in the sense above iff those two conditions; equal floors cancel; barrier `σ²*` is the fixed-period `σ²*` divided by 3. |
| Equipartition | SA1’s weight, the numerical value of `β`, and “supported on the quadratic well” for a `J` that is not globally quadratic. Coordinates are already the Lebesgue coordinates (the note’s “whiten first” is an input, not a theorem). | Integrability, `Z(β) = β^{−d/p} Z(1)`, `E[q] = d/(p β)` for a `HomogCost`, and `E[J] − J* = d/(2β)` for a positive definite quadratic on `ℝ^d`, `d ≥ 1`, `β > 0`, under `π ∝ e^{−β J}`. |
| Hull increment | Nothing about the world’s poles, and not convexity of `ε`. `R ≥ 0`. `φ` is the N60 reduced objective, not a derivation of `ε_K`. | For every `ε` on `{0,…,n}`, greedy chords are lower-hull vertex data, and the strict increment walk returns the leftmost argmin of `φ`. Model S convexity of `ε_K` stays unproved, as the README says. |

The pre-existing finite-menu block (CT4, CT10, CT20, CT22, CT33, CT34, the adjacent N60 walk) is unchanged in this diff. This review did not re-open those statements except to confirm they still build and still sit in the axiom count.

Nothing in the PR, the README, or the T19 row says the Part 2 hypothesis is proved. T19 stays **PARTIAL**.

---

## Part 2 sentence and locked files

The Part 2 sentence is byte-identical to `c92886a`, one copy each, bold markers included:

`**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**`

Locations: `THEORY.md` (one), `CORE.md` (one), `README.md` (one), `theory/SELECTION_AXIOMS.md` (one). Those four files are not in the diff.

`git diff --name-only c92886a..HEAD` is only:

`OPEN_WORK.md`, `formal/lean/GTAO.lean`, `formal/lean/GTAO/Equipartition.lean`, `formal/lean/GTAO/HullWalk.lean`, `formal/lean/GTAO/LayerLifetime.lean`, `formal/lean/GTAO/LocalShared.lean`, `formal/lean/README.md`, `formal/lean/scripts/AxiomAudit.lean`, `tools/check_lean.sh`.

No path under `tests/`, `prereg/`, no `PREREG`, `PREDICTIONS`, `LOCK`, or `.sha256` file, and not `CORE.md`, `THEORY.md`, `STATUS.md`, `core/KEYSTONE_NOTE.md`, or `theory/SELECTION_AXIOMS.md`. Locked files are unchanged.

---

## Issues

**Blockers:** none.

**Should-fixes (documentation only; no theorem statement needs to change):**

1. **`formal/lean/GTAO/Equipartition.lean:3` and `formal/lean/README.md:97`.** The quadratic row is sourced to “CORE §3, THEORY §4”. Current CORE §3 (`CORE.md:44-56`) is the layer lifetime `T* = √(6k/(wσ²))`. It does not state `E[J] − J* = d/(2β)`. That identity is Theorem SA1b (`theory/SELECTION_AXIOMS.md:62-75`). CORE §8 (`CORE.md:100`) and THEORY §4 (`THEORY.md:71`) point at the selection note’s excess formula; they are not a second statement of the Gaussian identity, and §3 is the wrong section. The “what is proved” cell is already the right sentence. Fix: cite SA1b, and CORE §8 only as the pointer, and drop “CORE §3” from this row and from the Equipartition header.

2. **`formal/lean/README.md:105` and `OPEN_WORK.md:66`.** Both still say the not-formalized remainder includes “the hypothesis in CORE §3 (a claim about the real world).” That sentence was CORE’s old §3. In the current one-page `CORE.md` the hypothesis is the Part 2 sentence at `CORE.md:9` and the Part 2 paragraph in §1 (`CORE.md:32`). Section 3 is the lifetime formula, which this PR maps, correctly, to `layer_lifetime` (`formal/lean/README.md:86`). As the file stands, “CORE §3” is both a proved minimization and an unformalized hypothesis. Fix: point the not-formalized bullet at the Part 2 hypothesis sentence, not at §3. Leave T19 **PARTIAL**.

**Nits:**

3. **`formal/lean/README.md:90` and `:93`.** `localCost` is tagged “CORE §1/§4”, and `switch_iff` is tagged `CORE §1` plus the quotation “needs delay on the shared channel only, and a shared lump cheaper than `N` local ones”. That quotation is the unnumbered lead, `CORE.md:11`. Section 1 is “The cost” and does not contain it. Section 4 (`CORE.md:60`) has the same claim with “latency” and “lumps”. The D5 citation of LAYER_LIFETIME §5 is the accurate one. Renumber the CORE pointer to the lead and to §4.

4. **`formal/lean/GTAO/HullWalk.lean:28-30`.** The module comment says a vertex list for every finite point set “is standard and is not formalized here.” `greedy_isLowerHull` (`:334`) and `hull_increment_test_eq_argmin` (`:381`) formalize it. The README row is right. Delete or rewrite the sentence so the comment matches the theorem.

---

## Commands and results

| Command | Result |
|---|---|
| `elan-init.sh -y --default-toolchain leanprover/lean4:v4.37.0-rc1`, then `nice -n 19 tools/check_lean.sh` | exit 0. Toolchain installed on first use. `lake build` 5835 jobs, success. `AxiomAudit: OK (312 GTAO declarations; only propext, Classical.choice, Quot.sound)`. `check_lean.sh: OK`. About 69 s. |
| Second Lean dump of `env.constants` with the audit’s module test | `COUNT 312`, 12 modules, every source declaration name present, 77 `_private` auxiliaries included. |
| Token grep of `formal/lean/**/*.lean` excluding `.lake/` | 1 hit: the comment in `scripts/AxiomAudit.lean:10`. No tactic or declaration. |
| `python3 tools/check_fresh.py` | exit 0. `STATUS.md` main is `2eeab30`; window includes `c92886a`. `RESULT: PASS`. |
| `python3 tools/check_consistency.py` | exit 0. 0 wording FAILs, 0 process-rule FAILs, 0 core-rule FAILs. Soft length WARNs only (THEORY main text 10569 words, README 1468), pre-existing. `RESULT: PASS`. |
| `python3 tools/check_open_work.py` | exit 0. 0 missing IDs. `RESULT: PASS`. |
| `nice -n 19 python3 -m pytest -q tools` | **176 passed** in 265 s. This environment did not have pytest, sympy, or pandas; those were installed for the run and not added to the repo. `test_lean.py` re-ran `check_lean.sh` on the warm tree as part of the suite. |
| `git diff --name-only c92886a..HEAD` and the four-file sentence extract | Part 2 sentence byte-identical, one copy each. Locked paths absent from the diff. |

---

## Conclusion

Merge after the two section-pointer fixes. The new Lean is a real extension of the finite-menu fragment: the zero-discount layer-lifetime minimization on `T > 0`, the D5 crossing and the switch iff, the Gibbs excess `d/(p β)` and its quadratic case `d/(2β)` as a normalized integral against Lebesgue, and the hull increment test as leftmost argmin for every `ε`. The build and the axiom audit pass, the audit’s 312 constants are the GTAO constants in the environment, and there is no `sorry` and no custom axiom. The stochastic derivations, SA1, the well-supported approximation, and the Part 2 hypothesis are not claimed as proved. The mapping table should stop calling the Gibbs theorem CORE §3, and it should stop calling the hypothesis CORE §3, because that section is now the lifetime formula.
