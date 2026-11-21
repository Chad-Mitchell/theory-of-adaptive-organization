# Confirm review: PR #125 at bb98725 (S1–S4 fix commit)

**Reviewer:** confirm pass on a fresh clone, after the S1–S4 housekeeping. This confirm wrote none of the original T28 package, prereg, predictions, runner, library, official run, first review, or RESULTS numbers. The same session applied the S1–S4 fix commit `bb98725` (author workdir `/tmp/gtao-pr125-fix`, not this clone) and then re-read the pushed head here. Same bot family, not a blind second executor. The verdict is from this fresh re-read, not from memory of the edits.
**Date:** Saturday 21 November 2026, started about 1:16 AM ET, finished about 1:27 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/125
**Clone:** fresh `/tmp/gtao-pr125-confirm` (not the author-fix workdir and not the first-review clone), branch `sim1-2026-11-21` at head `bb987254271f857735b353ae56f05a4cabcc317e` (parent `db0b4d931d47f3161a903d04609334e4f49af7c2`, the rebase of original `41d79060299d3a1c6d5d1315db0c8ecf16046149` onto `origin/main` `fba28278a1cbd82431451f3417e6279a0516530b`). Merge-base equals current `origin/main`. Clean tree at confirm start. Nothing merged at the start of this confirm. `/workspace/looper` was not touched. Other live branches were not checked out or otherwise touched. Compute at nice 19. Existing elan toolchain was reused; Mathlib was fetched into this clone’s own `formal/lean/.lake/`.

**Verdict: READY**

S1–S4 are fixed correctly, without touching locked files or official numbers. The official in-model result remains PASS (P1–P4 3/3). `CORE.md`, including the CORE §3 law sentence, is byte-identical to `origin/main`. `THEORY.md` and `STATUS.md` are also unchanged versus `main`. There is no novelty claim for the qualitative “simulate when stakes are high and the model is cheap” idea, and no claim that the law is proved or that T28 is evidence in the world. Checkers PASS. `tools/check_lean.sh` exits 0 and prints `check_lean.sh: OK`. `pytest tools/` is **129 passed** (128 on `main` `fba2827`, plus `tools/test_sim1_checks.py`). No new problem that would reopen the review. Residuals below do not block.

The rebase replay is `db0b4d9` (“T28 SIM-1 rehearsal test: PASSED (P1–P4 3/3)”). The fix commit is `bb98725` (“T28: apply review S1–S4 for PR #125 (rebase onto #123/#124)”), authored 1:17 AM EST on 21 November 2026. It also copies the first review to `reviews/sim1_2026-11-21/REVIEW.md` (SHA-256 `6f88396b07a45ae9cb38e7ce378aab7fea136e0263ba3aabcb4155774b097e1f`, 25675 bytes, byte-identical to `/workspace/review-archive/rev125_REVIEW.md`).

At confirm start the PR was open, mergeable, CLEAN, head `bb98725`, base `fba2827`.

---

## What was checked

- Fresh clone at the stated head; `git diff --stat origin/main...HEAD` (two commits, 23 files). Working tree clean. `/workspace/looper` not opened.
- SHA-256 of `PREREG.md`, `predictions.json`, `run_sim1.py`, and `sim1_lib.py` against `LOCK.txt`, the four sidecar files, `run_sim1.json`, `RESULTS.md`, the pre-fix replay `db0b4d9`, and the original head `41d7906` (fetched by SHA). `LOCK.txt`, `run_sim1.json`, and `run_sim1.log` are byte-identical to `41d7906`.
- `git hash-object` of `CORE.md` equals `origin/main:CORE.md`. The hypothesis sentence is unchanged: “**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**”
- S1–S4 wording in `MODEL.md`, `PILOT.md` (pre-lock body vs appended erratum), `DEVIATIONS_2026-11-21.md`, `RESULTS.md`, and `OPEN_WORK.md`. `CHAIN_SEED_BASE = 20261122400` and `P4_BETA = 40` were re-read from the locked `predictions.json`; official world-0 chain seeds are `20261122400 + 10·40 + 0..7 = 20261122800–807`.
- Official RESULTS figures cited in the first review (P4 TV, empirical means, joint argmin) are still present; the only RESULTS diff versus `41d7906` is the added S4 sentence on the OVERALL line. The only PILOT.md diff versus `41d7906` is the appended erratum; the false pre-lock collision sentence is still on the page.
- Crossref, this confirm (21 November 2026): Daw, Niv & Dayan 2005, doi `10.1038/nn1560`, *Nature Neuroscience*, issued 6 November 2005; Keramati, Dezfouli & Piray 2011, doi `10.1371/journal.pcbi.1002055`, *PLoS Computational Biology*, issued 26 May 2011.
- `python3 tools/check_open_work.py`; `python3 tools/check_consistency.py`; `tools/check_lean.sh`; `python3 -m pytest tools/ -q` with `~/.elan/bin` on `PATH`.
- Cheap residuals named in the fix commit: `reviews/README.md` rows; E. coli QUALIFICATION landing note.

---

## S1 — fixed; prior art credited, CT10 and CT33 named, no novelty claim

`MODEL.md` (unlocked) now has a “Prior art (not a novelty claim)” section that credits Daw, Niv & Dayan 2005 and Keramati, Dezfouli & Piray 2011 with the DOIs and Crossref issue dates above, and that states the qualitative arbitration is not original to this package. The “Already in the repository” list now names CT10 as the in-repo ancestor of official P1 and P3, and CT33 (with CT20) as the ancestor of the spend-and-error diagnostic, along with CT12 / CT20(ii). The “what is new” sentence is limited to a parametric rehearsal booking and a preregistered in-model test of its comparative statics. The locked prereg was not edited.

---

## S2 — fixed; collision recorded honestly, not silently edited away

`DEVIATIONS_2026-11-21.md` records, as a post-result hygiene note and not a rescoring, that official world-0 chain seeds `20261122800–20261122807` are the first eight pilot world seeds. The formula, the locked `CHAIN_SEED_BASE`, and the “different RNGs / not a scoring miss” account were checked against the locked runner and `predictions.json` and are correct. `PILOT.md`’s pre-lock sentence claiming that pilot seeds do not collide with this test’s reserved official/chain blocks is still present, and is labelled false by an appended erratum. Official candidate seeds `20261122000–015` are correctly distinguished from the chain-seed overlap. Locked files and official numbers are untouched.

---

## S3 — fixed; OPEN_WORK matches current `main`

- W13 is **DONE** and no longer says “needs reviewer (confirm of the fixes)” or “Branch `thermo-bridge-2026-11-21`, off `4398bbd`.” T26’s gate is DONE; T27 was already DONE on the original branch and remains so, citing the #122 merge `1727734`.
- The as-of line cites `main` as `fba2827`, with 128 tests on that commit and 129 on this branch. That matches this confirm’s `pytest tools/` count.
- T1 no longer says “Not started.” It records the #124 literature check, verdict NOT ESTABLISHED, no re-score of P1, P3, P4 or P13, and the path-to-establish pointer.
- T19 no longer says it was merely rebased onto `main` `1727734`. It records PR #123 merged as `fba2827`, confirm READY. A search for a stale “`main` is `1727734`” or “Rebased onto `main` `1727734`” line is empty.

---

## S4 — fixed; 3/3 is not offered as stochastic evidence

`RESULTS.md` keeps the official PASS and the official numbers, and now says, on the OVERALL line, that official P1–P3 PASS 3/3 are implementation-and-box checks of theorems, not stochastic evidence (P1 and P3 could not have failed under the stated model; P2 was pre-verified on all 16 locked-box corners and the 20 published pilots), that P4 is the only numerical test, and that everything here is in-model only. The T28 OPEN_WORK row carries the same distinction. That is the wording the first review asked for, not a re-score.

---

## Integrity, CORE, and official numbers

All four locked hashes match `LOCK.txt`, the sidecars, `run_sim1.json`, `RESULTS.md`, `db0b4d9`, and original `41d7906`. Bytes are unchanged: PREREG 11540, predictions 3876, runner 11715, library 15962. `LOCK.txt` / official JSON / official log are byte-identical to `41d7906`. `CORE.md` is byte-identical to `origin/main` (SHA-256 `aee235cb2a9b7d46a0e82c97825984eb3f5dcb160bdd283c90df552616284a7a`). The law sentence is unchanged. Official seeds, P4 table figures, and the overall PASS in `run_sim1.json` agree with `RESULTS.md`.

---

## Checkers and tests (this clone)

- `python3 tools/check_open_work.py`: PASS (union missing from OPEN_WORK.md: 0).
- `python3 tools/check_consistency.py`: RESULT: PASS (0 FAILs; the usual soft length warnings on THEORY.md and README.md).
- `tools/check_lean.sh`: OK (Mathlib cache hit; `lake build` completed, 4047 jobs).
- `python3 -m pytest tools/ -q`: **129 passed** in 114 s, with `~/.elan/bin` on `PATH`.

---

## Residuals (do not block)

1. **Same-session confirm.** The executor that applied `bb98725` also wrote this confirm, after a fresh-clone re-read. That is weaker than a blind second executor. It is disclosed so it is not mistaken for one. The first review itself was independent of the T28 package.
2. **After merge, T28 / SIM-1 will still say “needs reviewer (confirm of the fixes).”** Ordinary header lag, the same class this PR just cleaned up for W13 / T1 / T19. Not a conflict and not a gate change.
3. **`tools/test_lean.py` uses `os.path.access`,** which is not an attribute of `posixpath`. The fallback to `~/.elan/bin/lake` therefore raises if `shutil.which("lake")` fails. With `~/.elan/bin` on `PATH`, the test passes. This is pre-existing on `main` and is not introduced by this PR.
4. **No new litmap entry** for the two RL papers. The first review mentioned that as a should-fix; the required S1 repair was the MODEL.md paragraph, and that is in place.

The E. coli QUALIFICATION landing note leaves the historical “written off `4398bbd`” header in place and records the later rebase and the #124 merge. `reviews/README.md` now lists the wf, thermo, lean, ecoli_qual, and sim1 reviews.

---

## Conclusion

Merge is appropriate. The official in-model PASS stands, the lock is intact, CORE and the law sentence are untouched, and the four review items are fixed in the unlocked files only. P1–P3 remain theorems checked by implementation and by the locked box, not a stochastic result; P4 remains the only numerical test. The residuals above are process nits, not reopeners.
