# Confirm review: PR #128 at 1ebfe5b (S1–S7 fix, rebased on ac079ea)

**Reviewer:** confirm pass on a fresh clone. This confirm wrote none of the prereg, LOCK.txt, runner, library, reachability log, RESULTS, DEVIATIONS, robustness helper, OPEN_WORK edits, `tools/test_grid_cross.py`, or the first independent review. Same bot family, not a blind second executor; the verdict is from this fresh re-read and re-computation, not from memory of the edits.
**Date:** Saturday 21 November 2026, started about 2:27 AM ET, finished about 2:35 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/128
**Clone:** fresh `/tmp/rev128-confirm/repo` (not the first-review clone and not the author workdir), branch `grid-cross-2026-11-21` at head `1ebfe5bc2e384e1dc177d1b5e0a6837a86d3719d`. Parents: lock replay `b42b8a8153f16917c6292742c0801299c7993d95` (original lock `ca2fdf51523ceeffba5349522f169ce9b35bcecd`), then the S1–S7 fix. Merge-base equals current `origin/main` `ac079ea0b2724cec34f30d83e3b3c551c6877c07`. Clean tree at confirm start. Nothing merged at the start of this confirm. `/workspace/looper` and `/workspace/gtao-evo` were not touched. The parallel branch name `discrim-2026-11-21` was not checked out or otherwise touched. Compute at nice 19. Existing elan toolchain was reused; Mathlib cache was fetched into this clone’s own `formal/lean/.lake/`.

**Verdict: READY**

The lock is intact. `PREREG.md`, `run_grid_cross.py`, and `grid_cross_lib.py` are byte-identical to the original lock commit `ca2fdf5` and to the hashes in `LOCK.txt`. The official comparison remains not run: there is still no official Pass 1 selection-pressure score and no non-GB distance. P25 and GRID-DX are not re-scored. `CORE.md`, including the CORE §3 law sentence, is byte-identical to `origin/main`. The S1 typo is recorded as a dated informational-table correction; official permutation p is unchanged. The S2 resolution is a legitimate pre-data correction, not goal-post moving: the locked prereg’s {0, max} fill governs, the locked library is not edited, and the governing fill lives in a new separately hashed file whose SHA-256 matches `DEVIATIONS_2026-11-21.md`. The S3 resolution is coherent. Unlocked RESULTS discloses the small-n power of the locked gates and does not relax them. The S6 reachability addendum is accurate on a spot-check. The strengthened tests actually enumerate the no-tie table and assert a robustness flip. Checkers PASS. `tools/check_lean.sh` exits 0 and prints `check_lean.sh: OK`. `pytest tools/` is **146 passed**. No new problem that would reopen the review. Residuals below do not block.

At confirm start the PR was open, mergeable, rebaseable, and CLEAN, head `1ebfe5b`, base `ac079ea`, two commits, twelve files, +1527 / −2.

---

## What was checked

- Fresh clone at the stated head; `git diff --stat origin/main...HEAD` (two commits, twelve files). Working tree clean. `/workspace/looper` and `/workspace/gtao-evo` not opened. Other branches not checked out.
- SHA-256 and `cmp` of `PREREG.md`, `run_grid_cross.py`, `grid_cross_lib.py`, and `LOCK.txt` against original lock `ca2fdf5` (fetched by SHA) and against `LOCK.txt` / `run_grid_cross.py lock-check`. Git blobs agree across `ca2fdf5`, the rebase replay `b42b8a8`, and `1ebfe5b`. The fix commit does not touch those four files.
- Author and committer timestamps, and which commit introduced the lock, RESULTS, DEVIATIONS, the robustness helper, and the review copy.
- `DEVIATIONS_2026-11-21.md` (D1–D3), unlocked RESULTS power and leave-one-out disclosures, the reachability addendum, and `grid_cross_robustness_dev_20261121.py` against the hash recorded in DEVIATIONS.
- Independent exact enumeration of mid-rank Spearman on distinct ranks 1…n for n = 5–9 (one-sided p = (# permutations with ρ ≤ ρ_obs) / n!).
- Skeptical reading of whether D2 (prereg {0, max} over locked code {min, max}) is a pre-data correction or a moved goal-post.
- `git hash-object` / SHA-256 of `CORE.md` equals `origin/main:CORE.md`. The hypothesis sentence is unchanged: “**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**” `THEORY.md`, `STATUS.md`, `measurement/CLAIM_MAP_v2.md`, and `theory/measured/grid/` have no diff versus `main`. P25 remains OPEN, rank test UNTESTED, in the untouched CLAIM_MAP row.
- SHA-256 of `reviews/grid_cross_2026-11-21/REVIEW.md` against `/workspace/review-archive/rev128_REVIEW.md`.
- Spot-check of the S6 addendum: HTTP HEAD/GET of Fingrid dataset 397 and of `https://data.fingrid.fi/files/397/`, plus a confirming HEAD of NEMWEB `Reports/Current/`. No accounts, forms, or API keys. No zip or archive body was downloaded.
- `python3 tools/check_open_work.py`; `python3 tools/check_consistency.py`; `tools/check_lean.sh`; `python3 -m pytest tools/ -q` with `~/.elan/bin` on `PATH`, all at nice 19.

---

## Lock integrity and commit order

`theory/measured/grid_cross_2026-11-21/PREREG.md`, `run_grid_cross.py`, and `grid_cross_lib.py` are byte-identical to original lock commit `ca2fdf5`. SHA-256 and sizes match `LOCK.txt` and the runner’s `lock-check PASS`:

| File | SHA-256 | Bytes |
|---|---|---|
| `PREREG.md` | `1cd856331b968e369b9b97f8ac675186140b040ae2c14e1792147489a3d4d763` | 28105 |
| `run_grid_cross.py` | `eb4bf7d42e71db961fc73d778547bcd9dde548be6babdf939917c35825d8bd89` | 4795 |
| `grid_cross_lib.py` | `d9086f8a09a91e8bb7133bdd012c3adcc94f7726800f04409439a119279dc9b4` | 12732 |

The same git blobs are at `ca2fdf5`, `b42b8a8`, and `1ebfe5b`. `LOCK.txt` itself is also byte-identical to `ca2fdf5` (SHA-256 `5834e7ad9fbd286ab58efe0eb3b9ae88c2723ce57d68400a0dba6aba562a07b2`). The S1–S7 fix commit does not touch the locked files.

Author dates remain in lock-then-fix order: original lock `ca2fdf5` Saturday 21 November 2026, 01:58:48 −0500 (lock record itself is 01:55:05 EST, before that commit). After the rebase onto `ac079ea`, the lock replay `b42b8a8` keeps that author date and has committer date 02:23:16 −0500; the fix `1ebfe5b` is author 02:23:15 −0500, committer 02:23:38 −0500. `DEVIATIONS_2026-11-21.md` is dated 2:18 AM EST and appears only in the later fix commit. RESULTS existed in the lock commit (official comparison not run) and was extended in the fix commit with S4–S5 disclosures only.

There is no `SELECTION_SCORES.md`, no `selection_scores.json`, no distance JSON, and no official Pass 1 or Pass 2 output in the package. The only d1 number in RESULTS is the already-recorded GB value (d1 = 3 under B1, tagged BINDING-RUIN), explicitly “not recomputed.” Synthetic scores appear only in tests. No new official S score and no non-GB distance are present.

---

## S1 — typo recorded; independent n = 9 enumeration agrees

This confirm re-enumerated all n! mid-rank Spearman assignments of distinct ranks 1…n, n = 5–9. Official one-sided p is the share of permutations with ρ ≤ ρ_obs. n = 5–8 match the locked table. At n = 9 (9! = 362880):

| ρ (no ties) | exact one-sided p | Role |
|---|---|---|
| **−0.483333** | 0.096900 (35163/362880) | Maximum attainable ρ with p ≤ 0.10 |
| −0.466667 | 0.106261 (38560/362880) | Next attainable value; p is *above* α = 0.10 |

The locked PREREG §8 table and `NO_TIE_CRIT_RHO[9]` list −0.466667 with p = 0.096900 (35163/362880). That hit count and p-value belong to −0.483333. D1 records this as the typo-that-does-not-change-a-criterion the prereg already contemplates: the table is informational, official p is still `permutation_p` on observed values, and the locked sentence that for n ≥ 9 the effect-size floor ρ ≤ −0.5 is the stricter of the two remains true, because −0.483333 is still weaker than −0.5. The locked constant and PREREG table are not silently rewritten. That is the right repair.

---

## S2 — legitimate pre-data correction, not goal-post moving

The first review found a real discrepancy: PREREG §8 fills UNTESTED grids from {0, max observed complete d}; locked `robustness_tables` fills from {min, max}. Official verdicts had not been computed. The written fix asked for a dated deviation before Pass 2, with PREREG text treated as governing until then, “either conform[ing] the code to the prereg or amend[ing] the clause.”

D2 takes the first of those options. It states that the locked prereg clause governs, treats locked {min, max} as an implementation slip, and does not edit the locked library. The governing fill is implemented in a new file, `grid_cross_robustness_dev_20261121.py`, written with the deviations note and before any official score. SHA-256 on this clone is `f189de0e6d53deb42ab9c850c7e9a37e1f25e136bbb455d7981349e4c3f01a57` (2898 bytes), which matches the hash and size in DEVIATIONS exactly. Official Pass 2 UNTESTED-fill robustness is declared to use `robustness_tables_prereg`; leave-one-out, the lower-bound 0/8 sweep, and the BINDING-RUIN sensitivity remain those of the locked library.

This confirm also read the helper: it really fills with `(0, max(complete_d))`, not `(min, max)`. The worked example in D2 and in `test_robustness_fill_zero_vs_min_can_disagree` is the right kind of check: five anti-aligned complete pairs with d ∈ {2, 3, 4, 5, 6} plus an UNTESTED grid at S = 2 is PASS and robust under locked {min, max}, and INCONCLUSIVE under {0, max}, because fill d = 0 yields NEITHER. So the governing rule is *stricter* than the locked code, not a relaxation that would make a later PASS easier to keep.

Skeptical reading: this is not a post-result amendment. There is no official ρ, no official robustness table, and no scored headline being rescued or sharpened. The choice follows the locked prose rather than the locked implementation, is dated, is separately hashed, and was made before any Pass 1 or Pass 2. That is a pre-data correction of an implementation slip, not goal-post moving.

---

## S3 — coherent

The tension is real: §6 and the §8 robustness bullet say that if the BINDING-RUIN sensitivity leaves n < 5, that sensitivity is UNTESTED and the official headline follows the main §8 rule (the locked code does this). A later “Not applicable, as a gradient diagnostic” sentence lists “every complete d1 is BINDING-RUIN and dropping them leaves n < 5” as if the *headline* were NOT APPLICABLE.

D3 lets the more specific §6 / §8 sensitivity rule govern, as already implemented in the locked library, and reads the later list as a narrative summary of when the diagnostic cannot be used as a scored gradient, not as a headline override. That is consistent with the same list also naming “n < 5”, which the official diagnostic already labels UNTESTED, not NOT APPLICABLE. No locked file is edited; no new helper is required. Today’s official result (n = 1, UNTESTED) is unaffected either reading. The resolution is coherent and is also pre-data.

---

## S4–S5 — disclosed; bars not relaxed

Unlocked RESULTS now states, before any official ρ, that leave-one-out cannot bite at n = n_min = 5 (dropping one complete grid leaves n = 4, UNTESTED, which is excluded from the scored-label flip set), and that the locked test is underpowered for its own effect-size bar at small n. The disclosed figures match this confirm’s enumeration and the first review’s simulation: minimum detectable no-tie ρ −0.80 / −0.66 / −0.52 at n = 5, 6, 8; P(PASS | true ρ = −0.5) about 0.23, 0.34, and 0.47. The locked bars (ρ ≤ −0.5, α = 0.10, n_min = 5) are explicitly not relaxed. That is the disclosure the first review asked for, not a silent change of gates.

---

## S6 — reachability addendum accurate on a spot-check

The addendum, dated 2:18 AM EST, adds NEMWEB, Fingrid dataset 397, and the public ERCOT EMIL catalog, and does not treat them as a d1 rescue. This confirm spot-checked Fingrid 397 (21 November 2026, about 2:29 AM ET, no account):

- `https://data.fingrid.fi/en/datasets/397` returns HTTP 200. The page title is “Calculated imbalance.” The description is “the momentary calculated net imbalance (ACE open loop) without activated reserves in Finland.” Dataset ID 397; data period “1 min”; “Valid from 25.6.2025.” The license link is `https://creativecommons.org/licenses/by/4.0/` (CC BY 4.0), matching the addendum’s “CC BY 4.0” even though the visible label is “Creative Commons Attribution.”
- `https://data.fingrid.fi/files/397/` returns HTTP 404, as claimed. There is still no keyless static archive.
- A confirming request to `https://www.nemweb.com.au/Reports/Current/` returns HTTP 200, as claimed.

Content-Length on the dataset page was 54,377 bytes in this confirm, two bytes above the 54,375 recorded in the addendum. That is a dynamic-HTML drift, not a classification error. The addendum’s conclusions stand: these sources do not create n ≥ 5 complete (S, d1) pairs, and closed-loop frequency, a form-gated download, and an API-key route are not treated as a rescue.

---

## S7 — new tests are meaningful

`test_no_tie_critical_values_match_locked_table` now enumerates n = 5–9 rather than looking up the locked constant; it would have failed on the n = 9 typo, and it records that the locked `NO_TIE_CRIT_RHO[9]` is the non-critical −0.466667. `test_robustness_inconclusive_when_leave_one_out_flips` now asserts a scored-label flip at n = 6 (official NEITHER, drop the concordant sixth point, PASS, headline INCONCLUSIVE). New tests assert the S2 {0, max} vs {min, max} disagreement and that the robustness-helper hash is the one written in DEVIATIONS, while locked-file hashes still match `LOCK.txt`. Locked files are not edited to make the tests pass. That is what S7 asked for.

---

## No re-score, CORE, law sentence

`git diff origin/main...HEAD` does not touch `CORE.md`, `THEORY.md`, `STATUS.md`, `measurement/CLAIM_MAP_v2.md`, or `theory/measured/grid/`. `CORE.md` is byte-identical to `origin/main` (SHA-256 `aee235cb2a9b7d46a0e82c97825984eb3f5dcb160bdd283c90df552616284a7a`; git blob `37b9bf4635f5a21760de9a853053b8317852d39c`). The law sentence is unchanged. The word “law” is not used as a status label in the new files. P25 remains **OPEN**, rank test UNTESTED as locked; this PR adds no CLAIM_MAP row.

The copied first review at `reviews/grid_cross_2026-11-21/REVIEW.md` is byte-identical to `/workspace/review-archive/rev128_REVIEW.md` (SHA-256 `8ec81492c6671b44805f8d77daecbff9d12d5f32097e52d2951f91174cc6f76a`, 23059 bytes).

---

## Checkers and tests (this clone)

- `python3 tools/check_open_work.py`: PASS (union missing from OPEN_WORK.md: 0).
- `python3 tools/check_consistency.py`: RESULT: PASS (0 FAILs; the usual soft length warnings on THEORY.md and README.md).
- `tools/check_lean.sh`: OK (Mathlib cache hit after fetch into this clone; `lake build` completed, 4047 jobs).
- `python3 -m pytest tools/ -q`: **146 passed** in 122 s, with `~/.elan/bin` on `PATH`. That matches the fix commit’s claimed count (144 at lock plus the two new tests).

---

## Residuals (do not block)

1. **Fingrid 397 Content-Length is 54,377 bytes here, 54,375 in the addendum.** Classification, HTTP status, and the 404 on `/files/397/` agree. Not a reachability or d1 issue.
2. **OPEN_WORK as-of line still reads “about 2:13 AM ET” and, like T3 / W14 / `reviews/README`, still says the confirm review is not yet filed.** Ordinary header lag of the same class earlier PRs have cleaned up later. Not a conflict and not a gate change. After merge those lines will be briefly stale in the same way.

---

## Conclusion

Merge is appropriate. The lock is intact and precedes any official Pass 1 or Pass 2, CORE and the law sentence are untouched, P25 is not re-scored, and the official comparison remains not run (diagnostic UNTESTED, n = 1). S1 is an honest typo note, independently re-enumerated here. S2 is a pre-data conformance of the robustness fill to the locked prereg, separately hashed, and stricter than the locked code, not a moved goal-post. S3 is a coherent reading of the more specific sensitivity rule. Power is disclosed; bars are not relaxed. The residuals above are process nits, not reopeners.
