# Confirm review: PR #123 at 05cdcf4 (S1–S4 fix commit)

**Reviewer:** independent (wrote none of the PR, the `formal/lean/` library, the S1–S4 / N1–N3 fix commit, `tools/check_lean.sh`, `tools/test_lean.py`, the OPEN_WORK T19 edit, or the first review).
**Date:** Saturday 21 November 2026, started about 12:52 AM ET, finished about 1:03 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/123
**Clone:** fresh `/workspace/gtao-confirm123/repo` (not a previous review clone), branch `lean-core-2026-11-21` at head `05cdcf4a66667fa282751c9a6dc9d812cddfeb87` (parent `87ec00635077c5ec31b63a84baf54b9a8190fc89`; original merge-base equals the PR's recorded base `17277348dd0f3492489400fca3c76c8e9bd46e43`). Clean tree at confirm start. Nothing pushed or merged at the start of this confirm. `/workspace/looper` was not touched. Other live branches were not checked out or otherwise touched. Compute at nice 19. Existing elan toolchain `leanprover/lean4:v4.37.0-rc1` was reused; Mathlib was fetched into this clone’s own `formal/lean/.lake/`.

During the confirm, PR #124 merged and `origin/main` moved from `1727734` to `d63ac233b3e7fb3622732303dae2adb2200615ed`. The two PRs touch no common files. A local test-merge of `origin/main` into this head was clean (no conflicts). Checkers, `tools/check_lean.sh`, and `pytest tools/` were re-run on that merged tree and passed (see below). The test-merge was then aborted; this confirm is of head `05cdcf4`.

**Verdict: READY**

S1–S4 and N1–N3 are fixed correctly. The two theorems that the first review labelled VACUOUS are no longer vacuous and are no longer advertised as if they were the THEORY claims they failed to reach. `first_bit_sign` and `expected_cost_opt_at_or_above_Bslack` are faithful to the THEORY CT4 / CT22 wording as stated, in the slope-form and slack-case senses the README records. No remaining VACUOUS theorem is mapped as a headline. The not-formalized list is complete for the items S4 named. T19 is **PARTIAL**. There is no claim that the law is proved. `CORE.md`, the CORE §3 hypothesis sentence, `THEORY.md`, `core/KEYSTONE_NOTE.md`, and `STATUS.md` are byte-identical to base `1727734`. A clean and a warm `tools/check_lean.sh` both exit 0 and print `check_lean.sh: OK`. There is no `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, or `implemented_by` in the project sources. `#print axioms` on every README headline theorem, and on every other theorem or lemma in the project sources, returns only `propext`, `Classical.choice`, and `Quot.sound`. Checkers PASS. `pytest tools/` is 128 passed, on this head and on the local merge with post-#124 `main`. No new problem that would reopen the review. Residuals below do not block.

The fix commit is `05cdcf4` (“T19: apply review S1–S4 for PR #123 (rebase onto #122)”), authored 12:51:45 AM EST on 21 November 2026, on top of the formalization commit `87ec006` and the #122 merge `1727734`. It also copies the first review to `reviews/lean_2026-11-21/REVIEW.md` (SHA-256 matches `/workspace/review-archive/rev123_REVIEW.md`).

---

## What was checked

- Fresh clone at the stated head; `git diff --stat 1727734..05cdcf4` (two commits, 20 files, +1824/−2). Working tree clean at start and after aborting the test-merge. `/workspace/looper` not opened.
- Independent source grep of the 9 project files `formal/lean/GTAO.lean` and `formal/lean/GTAO/*.lean` (not `.lake/` or `lake-packages/`) for `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `implemented_by`, with both `rg` and `grep`. A broader unanchored scan of those same files also returned no hits. A naive `grep -R` of all of `formal/lean/` including `.lake/` still reports 1480 hits, so the exclusion is load-bearing.
- Clean build: `nice -n 19 tools/check_lean.sh` from a tree with no `.lake/` (elan already installed). Cache get + `lake build`, 4047 jobs, exit 0, `check_lean.sh: OK`. Re-run on the warm tree: exit 0, `check_lean.sh: OK`.
- `#print axioms` via `nice -n 19 lake env lean` on a `/tmp` file importing `GTAO`, covering every Lean name in the README mapping table and every other theorem or lemma in the project sources (67 declarations). Every list is exactly `[propext, Classical.choice, Quot.sound]`.
- Line-by-line comparison of `first_bit_sign`, `first_bit_positive_minimizer`, `L_right_slope`, and `expected_cost_opt_at_or_above_Bslack` against THEORY.md Appendix B (CT4 at line 278, CT22 at line 439), and a check that the previously vacuous names `first_bit_pays_iff` and `expected_cost_opt_is_constrained_opt` are gone from the library and the README (they remain only as quotations in the first review).
- README mapping table: helpers are labelled helpers, not CT4 first-bit; no headline is mapped to a vacuous statement. README and OPEN_WORK T19 not-formalized lists against the S4 checklist. T19 status **PARTIAL**. No “law proved” claim in the PR body, README, T19 row, or Lean sources. Formalization is stated not to establish the CORE §3 hypothesis.
- `git hash-object` of `CORE.md`, `THEORY.md`, `core/KEYSTONE_NOTE.md`, and `STATUS.md` equals `1727734:<path>`. The hypothesis sentence is unchanged: “**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**”
- `python3 tools/check_open_work.py`; `python3 tools/check_consistency.py`; `nice -n 19 python3 -m pytest tools/ -q` on head `05cdcf4` (**128 passed**, 216.3 s).
- Concurrent #124: `git fetch origin main`; `comm` of files changed since `1727734` on each side is empty; `git merge --no-commit --no-ff origin/main` succeeded with no conflicts (CLAIM_MAP notes and the E. coli qualification files only). Checkers, `check_lean.sh`, and `pytest tools/` re-run on that merged tree: PASS, `check_lean.sh: OK`, **128 passed** (113.4 s). Merge then aborted.

---

## S1 — fixed

`tools/check_lean.sh` now builds an explicit source list, `$LEAN_DIR/GTAO.lean` and `$LEAN_DIR/GTAO/*.lean`, and scans only those files. Both the `rg` and `grep` branches also exclude `.lake/` and `lake-packages/`. The token list is `sorry|admit|axiom|native_decide|unsafe|implemented_by`. On this warm tree the script still exits 0. `tools/test_lean.py` skips those cache directories, strips both `--` line comments and nested `/- ... -/` block comments (including `/--` and `/-!` doc comments), and uses the same token list. The sorry-scan still does not require Lean.

This was a checker bug, and it is fixed. The proofs were already clean.

---

## S2 — fixed; `first_bit_sign` is faithful, not vacuous

THEORY CT4 (Appendix B.1): “L(I) = D(IB(I)) + κI is a convex lower bound on cost at memory size I, and its minimizer is positive iff κ < −(D∘IB)′(0⁺).” The written proof is that L is convex and a convex function’s minimizer is positive iff its right derivative at 0 is negative.

What Lean now proves:

- `L_right_slope`: every right slope of `L(I)=D(IB(I))+κI` from 0 equals the corresponding right slope of `D∘IB` plus `κ`.
- `first_bit_sign`: `0` fails to minimize `L` on `[0, ∞)` iff `∃ x > 0, (D(IB x) − D(IB 0))/x + κ < 0`.
- `first_bit_positive_minimizer`: if a minimizer exists and that sign condition holds, the minimizer is strictly positive.

That is exactly the repair S2 asked for. For convex `D∘IB`, the right derivative at 0 exists in the extended reals and equals the infimum of those slopes, so the slope condition is equivalent to `κ < −(D∘IB)′(0⁺)`. The README and the theorem comment are honest that this is right-slope form, that the right derivative need not exist as a real, that convexity is not required for the equivalence, and that existence of a minimizer on `[0, ∞)` is not proved. The generic slope facts (`zero_isMinOn_iff` and companions) are still in the library and are mapped in the README as helpers, explicitly “not the CT4 first-bit criterion.” Unused `ConvexOn` hypotheses on those helpers are gone.

This is **FAITHFUL** to the CT4 sign condition as stated, in the slope form the file records. It is not a tautology about an arbitrary `L`.

---

## S3 — fixed; `expected_cost_opt_at_or_above_Bslack` is faithful, not vacuous

THEORY CT22: “For B ≥ B_slack the constraint is slack and 𝒟_E is optimal (multiplier μ_s = 0).” v2.4 already clarifies that “no design is feasible below B_min” means no design is Lundberg-certified.

The old standalone restriction lemma `expected_cost_opt_is_constrained_opt` is gone. The new theorem `expected_cost_opt_at_or_above_Bslack` takes `dE` an unconstrained minimizer of `J`, `θ(dE) > 0`, and `B ≥ B_slack`, and concludes that `dE` is Lundberg-certified **and** is therefore optimal among certified designs. The first conjunct is `certified_at_Bslack`; the second is the restriction of the unconstrained minimum to the certified set. `B`, `θ`, `ε`, and `Bslack` are used. No KKT is used; the binding region and `μ_s = 0` are not formalized, and the README and the theorem comment say so.

This is **FAITHFUL** to the slack-case claim as stated (certification of 𝒟_E at or above B_slack, hence a constrained optimum). It is not vacuous. The second conjunct is still a restriction argument, which is the right content once certification is proved; it is no longer listed as a standalone formalized piece of CT22.

`not_certified_below_Bmin`, `certified_at_Bslack`, and `Bmin_le_Bslack` remain as in the first review’s FAITHFUL reading.

---

## S4 — fixed

`formal/lean/README.md` “What is not formalized” and the OPEN_WORK T19 row now include, explicitly:

- CT20 (ii)’s second clause: `f*` nondecreasing in `w/c`.
- CT4 as a lower bound on cost (only convexity of `L` is proved) and the Gaussian closed form; the right derivative as a real, with the sign condition proved in right-slope form.
- CT34 (ii)’s “generically only if” converse, and CT34 (iv).
- CT6, CT7, and CT24 (the list now has CT1–CT3, CT5, CT6, CT7, CT8, CT9, then CT11–CT19, CT23, CT24, CT25, CT26–CT32, CT35–CT43, and the Master Theorem).
- The N60-as-written cardinality, with the zero-hole ingredients (no later step pays; leftmost minimizer is 0) still proved and not over-claimed as that cardinality.

Also already present, and still present: Model S convexity, the non-adjacent hull-vertex walk, CT20 on a continuous parameter set, CT21, CT22’s KKT / binding region, and the CORE §3 hypothesis. T19 is marked **PARTIAL**, gate still “in progress,” and says formalization cannot establish that hypothesis.

---

## Nits N1–N3 — fixed

- **N1.** The OPEN_WORK header is dated Saturday 21 November 2026, about 12:45 AM ET, records `main` as `1727734` (the #122 merge, which was `main` when this fix landed), and tallies 128 tests. `pytest tools/` on this head is 128 passed, including the two tests in `tools/test_lean.py`.
- **N2.** `formal/lean/README.md` documents the `v4.37.0-rc1` pin: Lean 4.37’s module system is not in stable `v4.36.0`, Mathlib’s then-current `lean-toolchain` and olean cache resolved to this RC, and a later bump to the next stable tag is open work. The pin is consistent across `lean-toolchain`, `lakefile.toml` (`rev = "v4.37.0-rc1"`), and `lake-manifest.json` (mathlib `31ce06eaadf4a200c0e1407c5f10953cf606b8f8`, `inputRev v4.37.0-rc1`).
- **N3.** The unused hypotheses named in the first review (`_hL`, `_hxStar`, `_hε0` / `_hε1` in `not_certified_below_Bmin`, `_hθ` in `Bmin_le_Bslack`) are gone from the sources. `lakefile.toml` leaves unused-variable and unused-section-var linters on (style linters stay off). The build completed with those linters enabled.

---

## Build, axioms, CORE, and checkers

- Toolchain and Mathlib pins unchanged and internally consistent, as above.
- Project sources: 9 `.lean` files, no forbidden tokens.
- Every printed axiom list is exactly `[propext, Classical.choice, Quot.sound]`. `Classical.choice` is expected (`Classical.choose` for `Jstar` / `JstarT`, and Mathlib). No extra axioms, and no `sorry` / `admit` / project-level `axiom`.
- CORE.md including the §3 hypothesis sentence is byte-identical to base. THEORY.md, KEYSTONE_NOTE, and STATUS.md are unchanged.
- `check_open_work.py`: PASS (0 IDs missing). `check_consistency.py`: PASS, 0 FAILs (soft length WARNs only, pre-existing). Same on the local merge with post-#124 `main` (frozen-record INFO count rises from 285 to 288, as expected from the new E. coli files; still 0 FAILs).
- `pytest tools/`: **128 passed** on `05cdcf4` and on the merged tree.
- No claim that the law, or the CORE §3 hypothesis, is proved. The PR title, README, and T19 row all say partial / finite-menu / cannot establish the hypothesis.

---

## Residuals (do not block)

1. **The GitHub PR body’s “Not formalized” paragraph is still the pre-S4 list.** It omits CT6, CT7, CT24, CT20 (ii) `f*`, CT4 as a cost bound, CT34 (ii) converse and (iv), and the N60-as-written cardinality, which README and OPEN_WORK T19 now list. This is a description on GitHub, not a file in the repo, and it does not claim those items were proved. Not a reason to hold the merge.
2. **`origin/main` moved during this confirm** (`d63ac23`, PR #124). No overlapping files; the local test-merge was clean; checkers, the Lean build, and 128 tests passed on the merged result. The OPEN_WORK header still cites `main` as `1727734`, which was correct at `05cdcf4`. It will be stale once this PR merges; that is ordinary header lag, not a conflict.
3. **`first_bit_sign` is the slope-form equivalent of “0 fails to minimize,”** not a proof that a positive minimizer exists, and not a construction of `(D∘IB)′(0⁺)` as a real. That is honestly labelled and was the agreed repair.
4. **The second conjunct of `expected_cost_opt_at_or_above_Bslack` is still a restriction argument.** The first conjunct is the content. The composition is what S3 asked for.

---

## Conclusion

Merge is appropriate. The formalization does what it says: a finite-menu, no-`sorry` Lean 4 + Mathlib fragment of J, CT33, the finite / sensing-fixed parts of CT20, discrete CT10, CT34 (i)–(iii), CT4’s convexity and first-bit sign in right-slope form, CT22’s certified comparisons and the slack-case theorem, and the convex-case / hull-membership facts of KEYSTONE_NOTE §4. It does not formalize Model S convexity, the general hull walk, CT21, CT22’s binding region, or the CORE §3 hypothesis, and it does not claim to. The two vacuous mappings and the warm-cache sorry-grep that blocked a clean merge at the first review are fixed.
