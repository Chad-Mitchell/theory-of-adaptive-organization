# Blind confirm review: PR #125 at merged main 75b58fe (CONFIRM2)

**Reviewer:** independent confirm. This confirm wrote none of the T28 package, prereg, predictions, runner, library, official run, RESULTS numbers, first review (`REVIEW.md`), S1–S4 fix commit, or the first confirm (`CONFIRM.md`). It is a fresh-clone re-read after merge, not a same-session confirm of the fixes.
**Date:** Saturday 21 November 2026, started 1:30 AM ET, finished 1:42 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/125 (merged)
**Clone:** fresh `/tmp/gtao-confirm2/repo` at `origin/main` `75b58fec282c102efa31b57477301636c6f551fb` (merge commit of PR #125). Original lock head `41d79060299d3a1c6d5d1315db0c8ecf16046149` was fetched by full SHA (it is not an ancestor after the rebase onto `#123`/`#124`). Working tree was clean at confirm start. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Other live work branches were not checked out or edited. Compute at nice 19.

**Verdict: CONFIRMED**

S1–S4 are fixed correctly in unlocked files only. Locked files and official numbers are byte-identical to original head `41d7906` and match `LOCK.txt`. The official in-model result remains PASS (P1–P4 3/3). `CORE.md`, including the CORE §3 law sentence, is unchanged. There is no novelty claim for the qualitative “simulate when stakes are high and the model is cheap” idea, and no claim that the law is proved or that T28 is evidence in the world. P1–P3 are implementation-and-box checks of theorems; P4 is the only numerical test. Residuals below do not reopen the review and do not block this confirm.

The first confirm (`CONFIRM.md`, READY, at `57e45b6`) is weaker than the usual standard: it was written by the same session that applied the S1–S4 fixes. That is disclosed in that file. This second confirm is the independent re-read that standard asks for.

---

## What was checked

- Fresh clone at `75b58fe`. `41d7906` fetched by SHA and compared with `git rev-parse` / SHA-256. `/workspace/looper` not opened.
- SHA-256 of `PREREG.md`, `predictions.json`, `run_sim1.py`, and `sim1_lib.py` against `LOCK.txt`, the four sidecar files, `run_sim1.json`, `RESULTS.md`, and original `41d7906`. `LOCK.txt`, official `run_sim1.json`, and `run_sim1.log` are byte-identical to `41d7906`.
- `git hash-object` of `CORE.md` equals `41d7906:CORE.md` and equals `fba2827:CORE.md` (`37b9bf4635f5a21760de9a853053b8317852d39c`). File SHA-256 `aee235cb2a9b7d46a0e82c97825984eb3f5dcb160bdd283c90df552616284a7a`. The hypothesis sentence is unchanged: “**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**”
- Diff of unlocked post-review files versus `41d7906`: `MODEL.md` (S1), `PILOT.md` (appended erratum only), new `DEVIATIONS_2026-11-21.md` (S2), `RESULTS.md` (one added S4 sentence on the OVERALL line). Locked files are not in that diff.
- S1–S4 wording re-read against the first review’s asks. `CHAIN_SEED_BASE = 20261122400` and `P4_BETA = 40` were re-read from the locked `predictions.json` and the locked runner formula `CHAIN_SEED_BASE + 1000·world_index + 10·β + c`; official world-0 chain seeds are `20261122800–807`. Official JSON records exactly those eight chain seeds for world 0.
- Official RESULTS figures and overall PASS agree with `run_sim1.json`. Official seeds 20261122000–02; none rejected. Official candidate seeds do not collide with the pilots; only the world-0 *chain* block does.
- Crossref, this confirm (21 November 2026): Daw, Niv & Dayan 2005, doi `10.1038/nn1560`, *Nature Neuroscience* 8, 1704–1711, issued 6 November 2005; Keramati, Dezfouli & Piray 2011, doi `10.1371/journal.pcbi.1002055`, *PLoS Computational Biology* 7, e1002055, issued 26 May 2011.
- `python3 tools/check_open_work.py` and `python3 tools/check_consistency.py` on this clone at `75b58fe`, both PASS (consistency: 0 FAILs; the usual soft length warnings on THEORY.md and README.md). The official Moran chains were not re-run here: the runner, library, official JSON, and official log are byte-identical to `41d7906`, and the first review already re-ran the committed runner.

---

## S1 — fixed; prior art credited, CT10 named, no novelty claim

`MODEL.md` (unlocked) has a “Prior art (not a novelty claim)” section that credits Daw, Niv & Dayan 2005 and Keramati, Dezfouli & Piray 2011 with the DOIs and Crossref issue dates above, and that states the qualitative arbitration is not original to this package. The “Already in the repository” list names CT10 as the in-repo ancestor of official P1 and P3, and CT33 (with CT20) as the ancestor of the spend-and-error diagnostic, along with CT12 / CT20(ii). The “what is new” sentence is limited to a minimal rehearsal booking and a preregistered in-model test of its comparative statics. The locked prereg was not edited. The two Crossref records match the citations.

---

## S2 — fixed; collision recorded honestly, not silently edited away

`DEVIATIONS_2026-11-21.md` records, as a post-result hygiene note and not a rescoring, that official world-0 chain seeds `20261122800–20261122807` are the first eight pilot world seeds. The formula, the locked `CHAIN_SEED_BASE`, and the “different RNGs / not a scoring miss” account were checked against the locked runner, `predictions.json`, and the official JSON chain-seed lists, and are correct. `PILOT.md`’s pre-lock sentence claiming that pilot seeds do not collide with this test’s reserved official/chain blocks is still present, and is labelled false by an appended erratum; the pre-lock body is otherwise unchanged versus `41d7906`. Official candidate seeds `20261122000–015` are correctly distinguished from the chain-seed overlap. `seed_collides` still checks only prior-set lists, not intra-test disjointness; that is disclosed, and the locked runner was not patched. Locked files and official numbers are untouched.

---

## S3 — fixed at the time of the #125 merge

On the merged tree, W13 is **DONE** and no longer says “needs reviewer (confirm of the fixes)” or “Branch `thermo-bridge-2026-11-21`, off `4398bbd`.” T1 records the #124 literature check (NOT ESTABLISHED, no re-score). T19 records PR #123 merged as `fba2827`. Those were the S3 asks. A new, ordinary header lag now exists *after* the merge itself and is listed under residuals: T28 / SIM-1 still say “needs reviewer (confirm of the fixes),” and the as-of line still says the T28 branch is “not yet merged” with `main` as `fba2827`. That lag is not a failure of the S3 repair, and it does not touch a gate or a locked file.

---

## S4 — fixed; 3/3 is not offered as stochastic evidence

`RESULTS.md` keeps the official PASS and the official numbers, and now says, on the OVERALL line, that official P1–P3 PASS 3/3 are implementation-and-box checks of theorems on this model, not stochastic evidence (P1 and P3 could not have failed under the stated model; P2 was pre-verified on all 16 locked-box corners and the 20 published pilots), that P4 is the only numerical test, and that everything here is in-model only. The T28 OPEN_WORK row carries the same distinction. That is the wording the first review asked for, not a re-score.

---

## Integrity, CORE, and official numbers

All four locked hashes match `LOCK.txt`, the sidecars, `run_sim1.json`, `RESULTS.md`, and original `41d7906`. Bytes are unchanged: PREREG 11540, predictions 3876, runner 11715, library 15962. `LOCK.txt` / official JSON / official log are byte-identical to `41d7906`. `CORE.md` is byte-identical across `41d7906`, `fba2827`, and `75b58fe`. The law sentence is unchanged. Official seeds, lock hashes, overall PASS, and P1–P4 3/3 in `run_sim1.json` agree with `RESULTS.md`. Everything claimed is in-model only.

---

## Checkers (this clone, at `75b58fe`, before any tidy edit)

- `python3 tools/check_open_work.py`: PASS (union missing from OPEN_WORK.md: 0).
- `python3 tools/check_consistency.py`: RESULT: PASS (0 FAILs; the usual soft length warnings on THEORY.md and README.md).

---

## Residuals (do not block this confirm)

These are present on merged `main` `75b58fe`. None flips a T28 gate, touches a locked file, or reopens S1–S4.

1. **T28 / SIM-1 OPEN_WORK lag after merge.** Both rows still say “needs reviewer (confirm of the fixes),” and the as-of line still says the T28 run is “not yet merged” with `main` as `fba2827` and “128 tests on `main`; 129 tests on this branch.” Ordinary header lag, the same class #125 just cleaned up for W13 / T1 / T19.
2. **`tools/test_lean.py` uses `os.path.access`**, which is not an attribute of `posixpath`. The fallback to `~/.elan/bin/lake` therefore raises if `shutil.which("lake")` fails. With `~/.elan/bin` on `PATH`, the test passes. Pre-existing on `main`; not introduced by #125.
3. **No litmap entry** yet for Daw, Niv & Dayan 2005 or Keramati, Dezfouli & Piray 2011. The required S1 repair was the MODEL.md paragraph, and that is in place.
4. **`reviews/README.md` already lists** the wf, thermo, lean, ecoli_qual, and sim1 review folders, but several rows name only `REVIEW.md` and do not point at the confirm files that are already in those folders.
5. **E. coli qualification note still says** the selection-temperature extension is “being developed on branch `thermo-bridge-2026-11-21`.” That work is on `main` via PR #122 (T27, official in-model FAILED). The note correctly keeps the extension out of every qualification verdict; only the “in development” status is stale. A second mention in §7 still points at that branch name.
6. **Test-count consistency** is the same as item 1: after the #125 merge, the 128/129 split in the as-of line is stale.

---

## Conclusion

CONFIRMED. The official in-model PASS stands, the lock is intact versus original head `41d7906`, CORE and the law sentence are untouched, and the four review items are fixed in the unlocked files only. P1–P3 remain theorems checked by implementation and by the locked box, not a stochastic result; P4 remains the only numerical test. The first confirm’s same-session weakness is repaired by this re-read. The residuals above are process nits, not reopeners.
