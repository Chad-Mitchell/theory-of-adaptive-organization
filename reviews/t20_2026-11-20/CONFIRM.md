# Confirm review: PR #120 at cf1254c

**Reviewer:** independent (wrote the first T20 review; wrote none of the fix commit).
**Date:** Friday 20 November 2026, started 10:11 PM ET, finished 10:20 PM ET (America/New_York).
**Clone:** `/tmp/t20-confirm/pr120`, fetched `pull/120/head`, checked out `cf1254cbc5fa2ab50d2d7f10db1e56264a9cf2d5` (parent `8537f39b59922ed5dd7d1ba283ebeefc99f43c47`; base of the PR). Clean detached HEAD. Nothing pushed or merged. `/workspace/looper` was not touched. Compute at nice 19.

**Verdict: CONFIRMED**

Issues 1–3 are handled correctly. The prereg and predictions hashes are unchanged. The first review is committed byte-identical. OPEN_WORK T20 / T24 are accurate. Checkers and `pytest tools/` pass. No new problem that would reopen the scoring. One residual private path in newly written RESULTS prose does not flip a gate and does not block (see below).

The fix commit is `cf1254c` (“T20 holographic / fractal test: prereg, results, and review”), authored 10:11 PM EST. It adds the locked test tree, the corrected RESULTS, and the review, and it updates OPEN_WORK.md and `reviews/README.md`. `CORE.md` and `core/KEYSTONE_NOTE.md` are not edited. No prereg, predictions file, run JSON, inclusion rule, or gate table was changed after the data.

---

## Issue 1 — fixed

`RESULTS.md` §2 and §6 now draw the Family M / Family S distinction the first review required.

- Family M, and a single OU, keep the closed-form Kalman–Bucy shift `b* = √(a² + 2av/N)`. The official numbers are the ones independently computed in the first review: on `M_a10_N1e-4`, observer times in `[0.0283, 2.828]` against process `[1, 10⁴]`; the four official stores sit on the observer set (Hausdorff 0.34), not the process set (3.87). Official (B) asks for process bands, so this arm cannot pass on that matching.
- Family S no longer says the observer “does not need a store as slow as the slowest mode,” and no longer claims “the same shift” for the many-mode fits. The joint ARE poles for `S_a10_N1e-4` are given as `0.019, 1.24, 2.28, …, 8080`; the four official stores `0.019, 2.14, 15.3, 202` occupy only the fast/mid subset; the fastest store is the whitening pole; Hausdorff to the full KB set is 1.60, almost the same as to the process set (1.71). A naive swap of official band centres for the full KB-pole range would still fail Family S Hausdorff at `K = 4`.
- A next candidate is stated as a new prereg, with a tautology trap, a fresh confirmation set, and a precise rule for *which* observer poles are predicted — not a rescue of (B).

No official gate, prereg criterion, or prediction was moved. Overall remains **NOT SUPPORTED** (in-model, numerical). That is the right treatment.

## Issue 2 — fixed

The holographic directory is now committed, so a clone can witness the files. `RESULTS.md` states, accurately, that at lock time the directory was untracked, that the lock is witnessed by the SHA-256 hashes, filesystem timestamps, the sidecar, and the hashes baked into the runner and `run_holo.json` — not by a git commit at lock time — and that this commit is after the run and the review. That is what Issue 2 asked for.

## Issue 3 — fixed without touching the lock

`PREREG.md` was not edited (it is hash-locked). `RESULTS.md` records that line 3 says “Locked: … 9:18 PM ET,” that this disagrees with the file’s mtime (9:19:00 PM EST) and with `LOCK.txt` (9:19:44 PM EST), and that the lock time used in RESULTS is the hash time. Correct.

---

## Hashes, review identity, checkers, tests

- `PREREG.md` SHA-256 `6eda4c82f06711fe1d5b282aa12124a1be2aa6048c4d117ece7e54dee552b1f8` — unchanged vs the first review, `LOCK.txt`, `PREDICTIONS.sha256`, and `run_holo.json`.
- `predictions.json` SHA-256 `0d877908b190cdcd287a960e87c2658c489a730d7124c964d7b45dbb106b8791` — unchanged on the same witnesses.
- `run_holo.py`, `run_holo.json`, `run_holo.log`, `build_predictions.py`, `LOCK.txt`, and `PREDICTIONS.sha256` are byte-identical to the tree that was scored.
- `reviews/t20_2026-11-20/REVIEW.md` is byte-identical to `/workspace/review-archive/t20_REVIEW.md` (SHA-256 `6afa750ad0b3c8ff735bf1f96740e94db77b4ba5d6953458e009105df4af00a8`, 128 lines).
- `python3 tools/check_consistency.py`: RESULT: PASS (0 FAILs). Soft length warnings only (THEORY.md 10471; README.md 1468; advisory). Frozen-record INFO hits 23; wording FAILs 0.
- `python3 tools/check_open_work.py`: RESULT: PASS (union missing = 0).
- `python3 -m pytest tools/ -q`: **125 passed** in 375 s.

---

## OPEN_WORK T20 / T24

Accurate.

- T20 is **DONE**, with the official in-model result (A pass 6/6 in both families, B fail 0/6 in both including 0/2 α = 1, C pass as the definitional identity, VALIDITY and SANITY passed, overall NOT SUPPORTED), the review verdict, the “not a re-score of the §9 worlds” scope, and “follow-up is T24, not a rescue of (B).”
- T24 is a new, in-progress-able item for an observer-band placement rule: it records the Family M / Family S distinction, the tautology guard, the need for a precise “which observer poles” criterion and a fresh confirmation set, that it is not a rescue of T20 (B), and that it is distinct from T21 (observer *kind*).
- W9, W11, and §5 are updated to match (T20 DONE; follow-ups T21–T24). `reviews/README.md` has a `t20_2026-11-20/REVIEW.md` row that states the verdict and that the Family S wording is corrected in this PR with no gate change.

No “law” beyond the standing hypothesis sentence (untouched C3). No “theory of everything.” Nothing in these files is called PROVED.

---

## Residuals (do not block)

- Newly written RESULTS prose still names `/workspace/gtao-t20` in the Branch line (“The run itself was done in `/workspace/gtao-t20` beside `aa6ab29`”). The same path necessarily remains in the hash-locked `PREREG.md`, the contemporaneous `LOCK.txt` and `run_holo.log`, and the unedited review. Those historical records should stay as they are. The Branch line could have described the run tree without a box path, as #119 did for newly authored provenance. Strip that one path if the public tree is to be kept clean; it is not a scoring issue and is not a reason to reopen Issues 1–3.
- OPEN_WORK W11 and §5 still say “writeup corrections applied in this PR” / “scored in this PR” in sentences that originally referred to the IMP-N60 / #119 work. The T20 status appended next to them is accurate; the leftover “this PR” is mildly stale and pre-existing, not a T20/T24 error.
- The committed first review names `/workspace/gtao-t20`, `/tmp/t20-review`, and `/workspace/looper`, because that is the review text. It must stay unedited to remain byte-identical.

No push or merge was made. This report: `/workspace/review-archive/t20_CONFIRM.md`.
