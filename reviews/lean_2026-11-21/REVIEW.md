# Independent hostile review: PR #123 (T19 Lean 4 formalization, partial)

**Reviewer:** independent (wrote none of the PR, the `formal/lean/` library, `tools/check_lean.sh`, `tools/test_lean.py`, or the OPEN_WORK T19 edit).
**Date:** Saturday 21 November 2026, started 12:32 AM ET, finished 12:40 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/123
**Clone:** fresh `/workspace/gtao-rev123/repo` at head `8fe3e8058a67793e45e18075d240129b439705d3` (branch `lean-core-2026-11-21`), base `4398bbdc434b766d4b761aa86d8b8836b0ef8c4c` (merge-base equals base). Clean detached HEAD at review start and at finish. One commit, 18 files, +1493/−1. Nothing pushed or merged. `/workspace/looper` was not touched. Compute at nice 19. Existing elan toolchain `leanprover/lean4:v4.37.0-rc1` was reused; Mathlib was fetched into this clone’s own `formal/lean/.lake/`.

**Verdict: READY-WITH-FIXES**

This is a genuine, machine-checked partial formalization of a finite-menu fragment, honestly labelled **PARTIAL**. From a clean tree, `tools/check_lean.sh` exits 0 and prints `check_lean.sh: OK`. There is no `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, or `@[implemented_by]` in the project sources. `#print axioms` on every headline theorem named in `formal/lean/README.md` returns only `propext`, `Classical.choice`, and `Quot.sound`. CORE.md, the CORE §3 hypothesis sentence, THEORY.md, KEYSTONE_NOTE, and STATUS.md are unchanged. The PR, the README, and the T19 row do not claim that the law is proved. `tools/check_open_work.py` and `tools/check_consistency.py` PASS. `pytest tools/` is 127 passed. `test_lean.py` skips cleanly when lake is absent, and the sorry-scan does not require Lean.

None of the issues below is a reason to reject the formalization or to widen any claim. They should be fixed before merge: one is a real landmine in the checker after a warm cache, and two of the mapped “headline” theorems are tautologies dressed as CT4 / CT22 content.

---

## What was checked

- Fresh clone at the stated head/base; `git diff --stat 4398bbd..8fe3e80` (one commit, 18 files). Working tree clean. `/workspace/looper` not opened.
- Independent source grep of `formal/lean/**/*.lean` excluding `.lake/` and `lake-packages/` for `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `@[implemented_by]`.
- Clean build: `nice -n 19 tools/check_lean.sh` from a tree with no `.lake/` (elan already installed). Cache get + `lake build`, 4047 jobs, exit 0 in 48.3 s, `check_lean.sh: OK`.
- `#print axioms` via `nice -n 19 lake env lean` on a `/tmp` file importing `GTAO`, covering every Lean name in the README mapping table (33 theorems / lemmas; definitions `J` and `Jstar` are not theorems).
- Line-by-line comparison of each mapped theorem against THEORY.md Appendix B (CT4, CT10, CT20, CT22, CT33, CT34) and `core/KEYSTONE_NOTE.md` §4, including hypotheses that would make a claim weaker, vacuous, or overstated.
- README, PR body, and OPEN_WORK T19 wording: PARTIAL, not-formalized lists, no “law proved” claim, CORE §3 called out as unformalizable.
- `python3 tools/check_open_work.py`; `python3 tools/check_consistency.py`; `nice -n 19 python3 -m pytest tools/ -q` (127 passed, 108.4 s).
- Skip path: `test_lean_sources_have_no_sorry` passes without Lean; `test_lean_build_if_available` raises `Skipped: Lean 4 / lake is not installed` when `_lake_on_path` returns `None`.
- Replication of `check_lean.sh`’s `grep -R` fallback on the warm tree (after `.lake/` exists).

---

## Build, axioms, and checkers

- Toolchain pin `leanprover/lean4:v4.37.0-rc1` matches `lakefile.toml` (`rev = "v4.37.0-rc1"`) and `lake-manifest.json` (mathlib `31ce06eaadf4a200c0e1407c5f10953cf606b8f8`, `inputRev v4.37.0-rc1`).
- Project sources (11 `.lean` files under `formal/lean/`, not `.lake`): no `sorry` / `admit` / `axiom` / `native_decide` / `unsafe` / `implemented_by`. The only `rg` hit on a broad token list was the word “partial” in a CT34 doc comment.
- Every printed axiom list is exactly `[propext, Classical.choice, Quot.sound]`. Classical.choice is expected (`Classical.choose` for `Jstar` / `JstarT`, and Mathlib). No extra axioms.
- CORE.md including “**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**” is byte-identical to base. THEORY.md and KEYSTONE_NOTE are unchanged.
- `check_open_work.py`: PASS (0 IDs missing). `check_consistency.py`: PASS, 0 FAILs (soft length WARNs only, pre-existing).
- `pytest tools/`: **127 passed**. Base `4398bbd` advertised 125 tests; this PR adds `tools/test_lean.py` (2 tests).
- Skip without Lean: clean.

### S1. `check_lean.sh` will fail on a warm tree if `rg` is missing

The script greps `$LEAN_DIR` (`formal/lean`) for `sorry` *before* building, but it does not exclude `.lake/` or `lake-packages/`. On a clean clone this is harmless, because the grep runs before `lake exe cache get`. After the first cache get, this clone has 10,080 `.lean` files under `formal/lean/.lake/packages/`, and `grep -R -n --include='*.lean' -E '(^|[^A-Za-z_])sorry([^A-Za-z_]|$)` reports **437 hits** (Mathlib tests, Aesop tests, comments). On this box `rg` is installed and respects `.gitignore`, so the `rg` branch reports nothing and `pytest tools/` (which re-runs the script on the already-built tree) passed. The `grep` fallback, which the script itself uses when `rg` is absent, would exit 1 on any second run.

Fix: search only project sources (`GTAO.lean`, `GTAO/*.lean`), or explicitly exclude `.lake` and `lake-packages` in both branches. While there, scan the same sources for `admit`, `axiom`, `native_decide`, `unsafe`, and `@[implemented_by]`, which the current checker does not. `test_lean.py`’s sorry scan already skips those directories, but it only strips `--` comments, not block comments.

This is a checker bug, not a hole in the proofs.

---

## Faithfulness (the main question)

Standing context, stated honestly in the README: almost every comparative-static theorem is proved on a nonempty finite menu whose spend and error do not depend on the stake (ruin slack or absent). That is a real restriction, and it is not hidden. Labels below are for the Lean statement against the THEORY / KEYSTONE wording, not against a wish list.

| Mapped item | Label | Reason |
|---|---|---|
| CT20 (i) existence (`exists_minimizer`) | **WEAKER-BUT-HONESTLY-STATED** | THEORY uses Weierstrass on a compact rate set plus “only finitely many K can beat a one-layer reference.” Lean proves existence on a nonempty finite type. README and Cost.lean say exactly that. |
| CT20 (i) layer bound (`layer_count_bound`) | **WEAKER-BUT-HONESTLY-STATED** | The inequality `K ≤ J(d₁)/h` is proved, for any competitor that beats or matches `d₁`, once `h > 0`, `h K ≤ S`, and `0 ≤ w E` are assumed. Those nonnegativity facts are hypotheses, not derived from the structured master equation `J = κI + hK + wE + A + L`. The reference need not be one-layer. The intended bound on `K*` follows. |
| CT20 (ii) layer count (`layer_count_nondecreasing`) | **FAITHFUL** | Sensing fixed is formalized as `S = h K` with `h > 0`; then CT33’s spend comparison lifts to `K`. The README and comments correctly record THEORY’s counterexample once reads are also chosen. The second clause of CT20 (ii), `f*` nondecreasing in `w/c`, is not formalized (see S4). |
| CT33 (`error_nonincreasing`, `spend_nondecreasing`, envelope) | **FAITHFUL** | Revealed-preference inequalities, `(w₂−w₁)(E₂−E₁) ≤ 0`, `E*` nonincreasing for `w₁ < w₂`, `S*` nondecreasing for `0 ≤ w₁ < w₂`, `J*` concave with supporting slope `E`, and `S*/h` nondecreasing in `w` at fixed `h > 0`. The stake-independent menu is the standing `FiniteDesignMenu` hypothesis, matching THEORY’s “ruin slack or absent.” Ties are handled by the strict stake comparison, as THEORY allows any selection at a tie. |
| CT10 (`effortJ_decreasing_differences`, `effort_nondecreasing`) | **WEAKER-BUT-HONESTLY-STATED** | Decreasing differences and the discrete Topkis conclusion (the frequency coordinate does not fall) on an arbitrary finite-type menu, taking “error is nonincreasing along the coordinate” and `c > 0` as hypotheses. The specific form `A(λ/f)` and the general-lattice Topkis citation are not formalized. This is the discrete fragment the README claims. |
| CT34 (i) (`jointOptimal_iff`, `exact_nesting_value`) | **FAITHFUL** | `min_{x,y} J = min_x [F(x)+J_T*(θ(x))]` and agreement of minimizers, proved as an iff plus a value identity, with existence granted by finite nonempty parent and team menus. |
| CT34 (ii) (`parentOptimal_of_constant_theta`) | **WEAKER-BUT-HONESTLY-STATED** | The “if `θ` is independent of `x`, then `J_T*` is an upkeep and the parent’s argmin is the argmin of `F`” direction is proved. THEORY’s “generically only if” converse is not. |
| CT34 (iii) (weak-coupling bound) | **WEAKER-BUT-HONESTLY-STATED** | The algebraic bound `0 ≤ m₀(x)−m(x) ≤ (εL)²/(2μ)` and the parent-regret comparison are proved from the strong-convexity and one-sided Lipschitz *inequalities* that THEORY’s proof uses, with `ε ≥ 0` and `μ > 0` stated. `dist : Y → ℝ` is not required to be a metric on a vector space; `y⁰ = argmin G` is implied by the inequality when `μ > 0`. This is the written calculus step, not a formalization of strong convexity as such. `weak_coupling_parent_regret` does not use the hypothesis that `x*` is a true joint minimizer (the inequality holds for any `x*`); the intended claim is still true. CT34 (iv) is not formalized, and is mentioned only in a comment. |
| CT4 convexity (`D_comp_IB_convex`, `L_convex`) | **WEAKER-BUT-HONESTLY-STATED** | `D` convex and nonincreasing on the image of `IB`, `IB` concave, imply `D ∘ IB` convex and `L(I)=D(IB(I))+κ I` convex. This is the first sentence of THEORY’s proof. That `L` is a *lower bound on cost*, and that `IB` is the information-bottleneck curve (including monotonicity of `IB`, which is not needed for this lemma), are not formalized. |
| CT4 first-bit (`zero_isMinOn_iff`, `first_bit_pays_iff`, companions) | **VACUOUS** | See S2. |
| CT22 `not_certified_below_Bmin`, `certified_at_Bslack`, `Bmin_le_Bslack` | **FAITHFUL** | Matches THEORY’s certified-feasibility reading (`B_min = ln(1/ε)/max θ`, `B_slack = ln(1/ε)/θ(D_E)`), including the v2.4 clarification that “no design is feasible” means no design is Lundberg-certified. Hypotheses `0 < ε < 1`, `B ≥ 0`, `max θ > 0`, `θ(d_E) > 0` are the ones the definitions need. |
| CT22 slack-case optimality (`expected_cost_opt_is_constrained_opt`) | **VACUOUS** | See S3. |
| KEYSTONE §4 `minimizer_on_lower_hull` | **FAITHFUL** | Every minimizer of `φ(K)=K+R(1+ε_K)` on `{0,…,n}` lies on the lower convex hull of `{(K,ε_K)}`, for `R ≥ 0`. This is the first sentence of the §4 Proposition (Lean includes the `R = 0` edge). `OnLowerHull` is the right discrete-combination definition (vertices and points on hull edges). |
| KEYSTONE §4 `n60_from_zero_leftmost` | **WEAKER-BUT-HONESTLY-STATED** | The adjacent walk from 0, under discrete convexity of `ε` (nondecreasing first differences), returns a leftmost minimizer. This is the first paragraph of §4 (“the N60 increment rule equals argmin when `ε_K` is convex”), not the Proposition’s general hull-vertex walk that may skip integers. The README lists the non-adjacent walk as not formalized. |
| KEYSTONE §4 `n60_as_written_zero_hole` | **WEAKER-BUT-HONESTLY-STATED** | Under discrete convexity, if the first adjacent step does not pay, no later step pays and `0` is a leftmost minimizer. The comment and README say that N60 as written, `1 + #{k ≥ 2 : step k−1 pays}`, equals `1`. That cardinality is never defined in Lean, and the equality is not a conclusion of the theorem — only the two ingredients are. Immediate, but slightly over-described. |

No mapped theorem is **OVERSTATED** in the strong sense of proving something under hidden hypotheses that assume the conclusion and then advertising the THEORY wording. The two vacuous items are advertised more generously than their Lean statements warrant (S2, S3).

---

## Honesty of PARTIAL / not-formalized / “law proved”

- OPEN_WORK T19 is marked **PARTIAL**, status still “in progress.” The row lists what was formalized and what was not, and says formalization cannot establish the CORE §3 hypothesis. That is the right status for a partial delivery.
- `formal/lean/README.md` and the PR body repeat that formalization cannot establish the hypothesis, that anything not listed as proved is not “proved with a hole,” and that there is no `sorry`. No claim that the law is proved was found in the PR, the README, or the T19 edit.
- The not-formalized list is largely complete for the big items (Model S convexity, non-adjacent hull walk, CT4 Gaussian closed form, CT20 on a continuous parameter set, CT21, CT22 KKT / binding region, CT1–CT3, CT5/CT8/CT9, Master Theorem, CORE §3). It is not complete on a few smaller THEORY clauses. See S4.

### S2. The “CT4 first-bit sign condition” is a tautology

THEORY CT4: the minimizer of `L(I)=D(IB(I))+κ I` is positive iff `κ < −(D∘IB)′(0⁺)`. The written proof is: `L` is convex, and a convex function’s minimizer is positive iff its right derivative at 0 is negative, i.e. `(D∘IB)′(0⁺)+κ < 0`.

What Lean proves, in `first_bit_pays_iff` and companions:

- `0` is a minimizer of an arbitrary `L : ℝ → ℝ` on `[0, ∞)` iff every right difference quotient from 0 is nonnegative.
- Therefore `0` fails to minimize iff some right slope is negative, and any minimizer is then strictly positive.

Convexity is a hypothesis on three of the four lemmas and is unused in every proof (`_hL`). The decomposition of a right slope of `L` into a right slope of `D∘IB` plus `κ` is not proved. The right derivative need not exist, and the README is honest about using slopes rather than a two-sided derivative — but it still calls this “CT4, first-bit sign.” That name belongs to the `κ` vs `(D∘IB)′(0⁺)` criterion.

This is not a hole in a proof; it is a packaging problem. Fix before merge: either prove that every right slope of `L` equals a right slope of `D∘IB` plus `κ` (so the sign condition becomes `∃ x > 0, (D(IB x) − D(IB 0))/x + κ < 0`), or move the current lemmas out of the “CT4 first-bit” slot and list the actual sign condition as not formalized. Drop the unused `ConvexOn` hypotheses, or use them.

### S3. `expected_cost_opt_is_constrained_opt` is a one-line restriction argument

The statement is: if `dE` minimizes `J` over all designs and is certified, then it minimizes `J` among certified designs. The proof is `fun d _ => hE d`. The certification hypothesis is unused (`_hFeas`). This is true for any predicate, not just Lundberg certification, and does not use `B`, `θ`, or `ε`.

THEORY’s slack-case claim is: for `B ≥ B_slack`, the constraint is slack and `D_E` is optimal. The interesting half of that — `certified_at_Bslack` — is faithfully proved. The “therefore it is a constrained optimum” half is this tautology. The PR body runs them together: “`D_E` is certified at or above `B_slack` and is then a constrained optimum.” That composition is never a single theorem, and the second conjunct has no content.

Fix: compose the two into one theorem (`θ(d_E) > 0`, `B ≥ B_slack` ⇒ `d_E` is certified and is a constrained optimum), and do not list the restriction lemma as a standalone formalized piece of CT22. No KKT is involved, and the README is already clear that the binding region is not formalized.

### S4. Not-formalized list, a few missing clauses

Add, in README / OPEN_WORK T19 / the PR body, explicitly:

- CT20 (ii)’s second clause: for one layer whose error grows with the age of its reading, `f*` is nondecreasing in `w/c`.
- CT4: that `L` is a lower bound on cost (only the convexity of `L` is proved); the first-bit criterion `κ < −(D∘IB)′(0⁺)` if S2 is not repaired by a proof.
- CT34 (ii)’s “generically only if” converse, and CT34 (iv) (shared driver is not weak coupling).
- CT6, CT7, and CT24. The present list goes CT1–CT3, CT5/CT8/CT9, then CT11–CT19, CT23, CT25, CT26–CT32, CT35–CT43, and so skips these three (THEORY has CT1 through CT43).
- Optionally, define N60-as-written as a cardinality and prove it equals 1 in `n60_as_written_zero_hole`, or stop saying the theorem proves that equality.

None of these omissions hides a claim that the items were proved.

---

## Issues (numbered)

**Blockers:** none.

**Should-fixes (apply before merge; do not change any theorem’s mathematical content except as noted in S2–S3):**

1. **S1.** Exclude `.lake/` and `lake-packages/` from `tools/check_lean.sh`’s sorry scan in both the `rg` and `grep` branches; prefer a source path list (`GTAO.lean`, `GTAO/*.lean`). After a warm `lake exe cache get`, the `grep` fallback currently reports 437 false hits and would fail the checker. Also reject `admit`, `axiom`, `native_decide`, `unsafe`, and `@[implemented_by]` in project sources. Align `test_lean.py` with block-comment stripping.
2. **S2.** Do not present the unused-convexity slope tautologies as CT4’s first-bit sign condition. Prove the `κ` / `(D∘IB)` slope form, or list that form as not formalized and rename the current lemmas.
3. **S3.** Do not present `expected_cost_opt_is_constrained_opt` as a formalized piece of CT22’s slack case. Compose it with `certified_at_Bslack`, or drop it from the proved list.
4. **S4.** Complete the not-formalized list (CT20 (ii) `f*`, CT4 lower-bound / sign criterion if unproved, CT34 (ii) converse and (iv), CT6, CT7, CT24; optionally the N60-as-written cardinality).

**Nits:**

5. **N1.** OPEN_WORK.md’s header still says “As of Friday 20 November 2026… 125 tests” and an older `main` SHA. This PR edits that file and adds two tests (127 passed). Pre-existing staleness relative to later same-night work, but the header should move if the row does.
6. **N2.** The toolchain is a release candidate (`v4.37.0-rc1`). The pin is internally consistent with Mathlib; worth saying so, not a reason to block.
7. **N3.** Several hypotheses are unused (`_hL` in CT4, `_hxStar` in CT34, `_hε0` / `_hε1` in `not_certified_below_Bmin`, `_hθ` in `Bmin_le_Bslack`) and `linter.unusedSectionVars` is off. Harmless given S2–S3, but it is how a tautology can look like a theorem.

---

## Conclusion

Merge is appropriate after S1–S4. The formalization does what it says: a finite-menu, no-`sorry` Lean 4 + Mathlib fragment of J, CT33, the finite / sensing-fixed parts of CT20, discrete CT10, CT34 (i)–(iii), CT4’s convexity, the certified comparisons in CT22, and the convex-case / hull-membership facts of KEYSTONE_NOTE §4. It does not formalize Model S convexity, the general hull walk, CT21, CT22’s binding region, or the CORE §3 hypothesis, and it does not claim to. The two vacuous mappings (CT4 first-bit, CT22 slack-case optimality) and the warm-cache sorry-grep are the items to clean up so the PARTIAL label stays as precise as the proofs.
