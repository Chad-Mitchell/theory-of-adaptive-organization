# Blind confirm: PR #152 at 678c6d8

**Confirmer:** independent. Wrote none of the PR, the `formal/lean/` library, the OPEN_WORK T19 edit, the fix commit, or `REVIEW.md`.
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/152
**Head confirmed:** `678c6d8713d2fb393286f760a401aa6c59872035` on `lean-layer-drift-2026-11-21`. Parent `025cdf3` is `REVIEW.md`. Base `d1a6de448bbaca2e2e0f18d4dc2ce9c3972308a5` (`main`). The fix commit edits `N60Exact.lean`, `BandMonge.lean`, `Coadaptation.lean`, `formal/lean/README.md`, and `OPEN_WORK.md`. This confirm does not merge.

**Verdict: CONFIRMED**

`REVIEW.md` (head `025cdf3`, verdict READY-WITH-FIXES) listed five should-fixes. `678c6d8` resolves each one, three by a stronger statement and two by the mapping table and the not-formalized list. The three Lean files are unchanged on the descendant `d549e60`, and that tree builds.

---

## What was checked

- `git show 678c6d8` and the five sites named in `REVIEW.md`, read at this head: `GTAO/N60Exact.lean` (the interval theorem and the `d = (−2, −1)` uniqueness conjunct), `GTAO/BandMonge.lean` (`bandE` through `bandE_second_difference`), `GTAO/Coadaptation.lean` (`gibbs_form` and the CA1 comment), and `formal/lean/README.md:105-106`, `:110`, `:113`, `:115`, `:142-143`.
- `git diff 678c6d8 d549e60 -- formal/lean/GTAO/N60Exact.lean formal/lean/GTAO/BandMonge.lean formal/lean/GTAO/Coadaptation.lean` is empty, so the build below typechecks these proofs.
- elan installed with toolchain `leanprover/lean4:v4.37.0-rc1`. `nice -n 19 tools/check_lean.sh` on `d549e60` (the script also runs `lake` at `nice -n 19`): Mathlib `31ce06eaadf4a200c0e1407c5f10953cf606b8f8`, `lake build` 5857 jobs, “Build completed successfully”, `AxiomAudit: OK (712 GTAO declarations; only propext, Classical.choice, Quot.sound)`, `check_lean.sh: OK`. The isolated count 635 in `formal/lean/README.md:38` was not regenerated at `678c6d8` by itself.
- Whole-token scan of `formal/lean/GTAO.lean` and `formal/lean/GTAO/*.lean` for `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `implemented_by`, same boundary regex as `tools/check_lean.sh`. The scan is clean on this head’s sources (the build’s scan on the descendant, which adds four modules, is also clean).

The Part 2 hypothesis sentence is present once, byte-identical, in `CORE.md`, `THEORY.md`, `README.md`, and `theory/SELECTION_AXIOMS.md` at `d1a6de4` and at `678c6d8`. The fix commit does not touch those files.

---

## Should-fix 1 — CONFIRMED

`REVIEW.md` asked for `φ(0) < φ(j)` on `0 < j ≤ 2` inside `exists_nonconvex_count_exact`, or else for the README to say “leftmost” instead of “unique.”

`epsCE_zero_min` (`formal/lean/GTAO/N60Exact.lean:411-427`) proves both `IsLeftmostArgmin` at `0` and `φ(0) < φ(j)` for `j = 1, 2`. `exists_nonconvex_count_exact` (`:432-441`) puts that conjunct on the count, after `epsCE_count_zero` rewrites the count to `0`. The values are `φ = (−2R, 1, 2+R)` with `ε = (−3, −1, 0)`, and the proof is `linarith` under `0 ≤ R`. On `{0, 1, 2}` the strict inequality is uniqueness. `formal/lean/README.md:106` says “the unique minimizer” and cites `φ(0) < φ(j)` for `j = 1, 2`. The module comment (`N60Exact.lean:37-39`) says the same.

## Should-fix 2 — CONFIRMED

`REVIEW.md` asked for an open interval of `R > 0` on which `count = j+1` and the count is not a minimizer, or else for the README to call the converse a single `R` and to drop `K*_0(R) = m`.

`exists_R_interval_count_not_argmin` (`N60Exact.lean:160-165`) concludes

```lean
∃ R₀ > 0, ∃ δ > 0, ∀ R, |R - R₀| < δ →
  0 < R ∧ count R ε n = j + 1 ∧ ∃ k ≤ n, phi R ε k < phi R ε (count R ε n)
```

under pairwise distinct decrements, a rise at `j`, and at least `j+1` positive decrements. The witness is a neighborhood of the midpoint between the consecutive order statistics `g_{(j+2)}` and `g_{(j+1)}` (or above `0` when the lower one is nonpositive), which is the interval the note’s proof already used (`theory/LAYER_CONVEXITY.md:38`). `not_min_of_rise` supplies the failure to minimize, and the count equality is `j+1`, which is `m` one past the rise. `exists_R_count_not_argmin` (`:337-346`) is the single-`R` projection of that theorem. `formal/lean/README.md:105` describes the interval and calls the single-`R` form a projection.

## Should-fix 3 — CONFIRMED

`REVIEW.md` asked to define `E_k` as the minimum `k`-link path cost and prove `2 E_{k+1} ≤ E_k + E_{k+2}` for `k ≥ 1`, and to list the staircase identification and the `K*_0` corollary as not formalized.

`bandE` (`BandMonge.lean:455-460`) is that minimum for `k ≥ 1`, via `exists_path` (`:427`) and `exists_optimal`. `bandE_is_min` (`:463`) and `bandE_eq` (`:476`) are the minimality lemmas. `bandE_second_difference` (`:486-499`) takes optimal paths for `k`, `k+1`, and `k+2` links and applies `band_convex`. A `k`-link path is `k−1` free bands plus the terminal band, so `bandE (k+1)` is the note’s `E_k` and the inequality is Lemma X’s `2 E_K ≤ E_{K−1} + E_{K+1}` for `K ≥ 1` (`theory/LAYER_CONVEXITY.md:66`). `formal/lean/README.md:110` states that second difference for the minimum path cost. `formal/lean/README.md:142` names the two halves that remain open: identifying `bandE` with `BandCounterexample.cost`, and the corollary that `K*_0` equals the leftmost argmin in 𝓑.

## Should-fix 4 — CONFIRMED

`REVIEW.md` asked to add DS1(b) for a general mutation matrix `M` and DS1(c) as the single summed excess to the not-formalized list, and to keep `velocity_mean_excess` described as the mean-lag term.

`formal/lean/README.md:143` lists both: `d/(2β) + Tr(M^{-1} Q)/(2β)`, and `d/(2β) + vᵀ H^{-1} v / (2 β² D_m²)`, with the clause that only the mean-lag term is formalized and that `Equipartition` does not supply the fluctuation here. `formal/lean/README.md:113` still calls `velocity_mean_excess` the mean-lag term and says the fluctuation `d/(2β)` is added outside the identity. No declaration states the general-`M` formula or the summed DS1(c) formula.

## Should-fix 5 — CONFIRMED

`REVIEW.md` asked to drop `gibbs_form` from the CA1 row. The correspondence is `detailedBalance_of_potential` and `potential_of_detailedBalance`.

`formal/lean/README.md:115` lists `LogLinearChain`, `detailedBalance_of_potential`, `potential_of_detailedBalance`, `ca1_iff`, and `stationary_of_detailedBalance`. `gibbs_form` is not among them. The proved cell says `π x = exp(-Ψ x)` for the first theorem and `Ψ = -log π` for the second, which is the constant `c = 1` the review allowed. The lemma remains at `Coadaptation.lean:154-156` and is still `π = exp(log π)`. Its comment (`:151-153`) says it is not the CA1 Gibbs correspondence and names the two theorems that are. The row no longer calls it the Gibbs form.

---

## Conclusion

CONFIRMED. The `d = (−2, −1)` theorem now carries the strict inequality that makes the minimizer unique. L1’s converse exports an open interval on which the count equals `j+1` and misses. `bandE` is the minimum path cost and satisfies the second difference the review asked for, with the staircase reading and the `K*_0` corollary left in the not-formalized list. General `M` and the summed DS1(c) formula are in that list, and the mean-lag row still describes only the mean-lag term. `gibbs_form` is off the CA1 row. The descendant build that contains these proofs exits 0. This confirm does not merge the draft.
