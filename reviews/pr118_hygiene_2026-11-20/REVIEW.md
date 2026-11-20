# Independent review: PR #118 (hygiene)

Reviewer: separate executor; I wrote none of the PR. 20 November 2026, about 6:13 PM ET (America/New_York).
Fresh clone `/workspace/rev118` at head `2be7f18`, base `main` `a1a98aa`. Compute at nice 19.
Nothing pushed, commented, or merged.

## Verdict: READY-WITH-FIXES

Three required fixes (B1–B3), then a short confirm is enough; no new analysis is needed. The counts, the scorer fix, the prereg lock, the checker, and pytest all hold.

Reproduced: `python3 tools/check_consistency.py` RESULT: PASS (FAIL 0; advisory length warnings only: THEORY 10458 words, README 1399). `python3 -m pytest -q tools/`: 121 passed in 4:32. `git diff --exit-code a1a98aa..2be7f18 -- prereg/` and the same for `prereg/**`, `**/PREREG.md`, and `**/DEVIATIONS.md`: no locked prereg file or hash is touched. Working tree clean after pytest; the live ledger was not written.

## Required fixes

**B1. A committed review names `/workspace/looper`.** `reviews/pr111_map_2026-11-20/REVIEW28.md:3`.

The sentence is otherwise just the reviewer's setup ("fresh clone … nothing pushed … compute at nice 19"), but it includes "`/workspace/looper` untouched". That is Looper content in a public repository. The PR body already flags the mention and says nothing was stripped. The checklist for this review is that committed reviews contain no private/Looper/personal content. I found no other Looper, Nelnet, personal, or credential material in the added review files (the Crossref scripts use the placeholder `mailto:none@example.com`, which is fine).

Fix: delete the Looper path phrase from that one sentence. Do not add a substitute that still names the project.

**B2. Several not-DONE items in `process/QUEUE.md` are neither on `OPEN_WORK.md` nor covered by the stated remainder.**

H6 (`OPEN_WORK.md:32`) and the S8 remainder (`OPEN_WORK.md:85`) say the 62 not-DONE items "have not been folded into this page line by line" and remain in the frozen queue. That count is correct for `process/queue/items.json` (117 items, 55 with `status: "DONE"`, 62 with no status). For those 62, an explicit remainder is enough, and the old STATUS "Next" items that were already in the queue or later work are represented:

- SAME-SYSTEM-AQN / N13 and STAKES-PRECISION, and the killing tests N56 and N57: T6 (`OPEN_WORK.md:46`)
- Theorem P / CX1: T11 (`OPEN_WORK.md:51`)
- SENSE-CELL-MATCHED and C3b: T10 and T9 (`OPEN_WORK.md:50`, `:49`)
- SG-SCORE / Q0: H7 (`OPEN_WORK.md:33`)
- WHOLE-THEORY-REVIEW: T16 in substance (`OPEN_WORK.md:56`)

The remainder does not cover not-DONE bullets that were never ledgered into `items.json`, including the 18 Nov lock-pass set (`process/QUEUE.md:454-462`) and two later open items. These IDs appear in `QUEUE.md` and do not appear in `OPEN_WORK.md` (including under another name):

- **N52-N53-SWEEP** (`QUEUE.md:458`) — literature sweep owed before any N52/N53 prereg
- **MV9-DECISION** (`QUEUE.md:459`) — blocked on Chad; without an OSF/Zenodo timestamp no test reaches Tier 1
- **N51-LAB-PREREG** (`QUEUE.md:460`) — attention-exponent lab prereg; this is not T7 (T7 is the tracking / chemotaxis lab)
- **LOCK-V1.5** (`QUEUE.md:462`) — Chad's call, after WHOLE-THEORY-REVIEW
- **SENSE-CELL-EFFORT** (`QUEUE.md:452`) — blocked on a dataset; contacting authors needs Chad
- **CAUSAL-OVER-RESPONSE** (`QUEUE.md:438`) — open kill-rule question, not in `items.json`

Fix: add these six as rows (N51, MV9, and LOCK-V1.5 belong in §4 if they still wait on Chad), or widen H6/S8 so the remainder is "every not-DONE item in `process/QUEUE.md`", and name this unledgered set explicitly. Leaving them only in a frozen file that `STATUS.md` now calls historical is a drop.

**B3. `theory/STORE_NOISE.md` still contradicts its own (correct) s = 1/2 statement, and THEORY §6 (iii) still has the wording this PR meant to fix.**

The correct statement is `theory/STORE_NOISE.md:33` (E1-a): the store "is slower than its mode iff s < 1/2, matches it at s = 1/2, and is faster iff s > 1/2." Higher SNR then shortens the memory, so at *positive* SNR a store with s = 1/2 is faster; equality holds at the low-SNR limit. README (`README.md:16`) and the matching THEORY §1 sentence (`THEORY.md:19`) now say this, and CLAIM_MAP CT21 (`THEORY.md:532`) already has "faster iff s > 1/2".

The interlacing bullet does not. `theory/STORE_NOISE.md:63-64`:

> In Model S+ it holds for a one-store layer iff s ≥ 1/2 at h1 = 0 (E1-a); with s < 1/2 or h1 > 0 the optimal store is **slower** than its mode.

That "iff s ≥ 1/2" is false at the low-SNR case E1-a is about: at s = 1/2, λτ\* = 1, equal, not faster. The second clause is also too strong: any h1 > 0 lengthens memory relative to E1-a (`STORE_NOISE.md:53-54`), but a store that starts faster than its mode (s > 1/2) need not become slower.

This PR's H8 (`OPEN_WORK.md:34`) fixed "the matching THEORY sentence" but left the same claim in THEORY §6 (iii) (`THEORY.md:81`): "faster than the mode whenever s ≥ 1/2". That sentence is the live special-case of CT21, not a frozen changelog note.

Fix, in both places, to match E1-a and the already-corrected §1/README wording. Suggested STORE_NOISE bullet:

> In Model S+ it holds for a one-store layer iff s > 1/2 at h1 = 0 (E1-a); at s = 1/2 and low SNR, λτ\* = 1 (equal, not faster); with s < 1/2 the optimal store is slower than its mode at low SNR. Any h1 > 0 lengthens memory relative to E1-a.

And in THEORY §6 (iii): "faster than the mode when s > 1/2 (at s = 1/2, λτ\* = 1 at low signal-to-noise, equal, not faster)". Historical v2.5.4 / v2.64 notes in CHANGELOG and CLAIM_MAP can stay as written; they are dated records. `theory/measured/SYNTHESIS.md:76` still has "iff s ≥ ½ at h1 = 0" and should be fixed in the same pass if that page is treated as live.

## Checks that pass

**THEORY §8 counts.** `THEORY.md:189` now says "30 field rows are NOT A TEST (10 passed on proxy and 20 failed on proxy)". I counted the compound status cells in `measurement/CLAIM_MAP_v2.md` (not the tally table): 30 rows.

Passed on proxy (10): H3, H9, N1, N2, N10, N20, N23, P4, P18, P20.

Failed on proxy (20): H1, H2, H7, H11, H12, H13, H14, H15, H17, H18, K4, K10, N5, N14, N17, P1, P3, P13, and P19, P21 (`NOT A TEST (not qualified; proxy: failed)`). The official tally table (`CLAIM_MAP_v2.md:584-586`) splits these as 10 + 18 + 2, which is the same 30. Line 599 states the 10/20 split explicitly. Each of the 30 rows has a "Qualification prospect" note (30 such lines; `grep -c prospect` is 32 because two other uses of the word appear).

**SG-SCORE fix and dry run.** The crash is real: ledger entry 156 (`ONSET-ACROSS-ALPHA-SIM`) has `claim_map_status_changed: false` and no `status_changed`. `process/queue/sg_rank.py` now accepts either name (`outcome_status_changed`), prefers `status_changed` when both exist (entry 162), and skips an outcome missing both, with a warning. The pass/kill rule, first-seen predictor, and 15-outcome floor are unchanged. `tools/test_sg_rank.py` is meaningful: one test aliases the field and checks there is no verdict below 15 outcomes; one tests the skip path; one runs the real ledger read-only and checks that entry 156 is accepted and the scorer no longer crashes. The third test will print AUC text into captured stdout; it does not write the ledger, does not snapshot an AUC, and does not add a `rule_change` entry.

The PR body's mechanical dry run (rule AUC 0.719, CI 0.417–0.969; re-read 0.557, CI 0.266–0.836; both would be INCONCLUSIVE; clock n = 2) is labeled as a dry run, and H7 / the CHANGELOG hygiene entry say the official score is still owed and that no ledger entry was written. That is not an unpreregistered official score. I did not treat those numbers as a verdict.

**Preregs.** No file under `prereg/` (or any `PREREG.md` / `DEVIATIONS.md`) is in the diff.

**CHANGELOG #113.** The missing v2.65 / PR #113 entry is now in `reference/CHANGELOG.md` (new paragraph after the robustness-fixes entry). It correctly records the qualification-gate wording, the 30-row retype, P19/P21, and the prospect notes. One nit is below.

## Should-fixes

**S1.** The new #113 CHANGELOG paragraph says the confirm round was "READY-WITH-FIXES, conditional on Chad's go". The committed review's confirm section is READY-WITH-FIXES (`reviews/pr113_griddx_2026-11-20/REVIEW.md:183`), but its final verdict is **READY**, conditional on Chad's go (`:217`). `reviews/README.md:23` already follows the final line. Use that.

**S2.** The old STATUS "Next" item "Independent review of the v2.4 delta" (scope: the v2.3 blockers as restated, CT30–CT34, the face figure, operational "strongly selected", then CT20–CT25 and the rest, `reviews/audit_2026-11-19/AUDIT.md` §3) is not named on `OPEN_WORK.md`. T16 is the broader whole-theory review. Either point that old item at T16, or record that it is still open as a narrower owed review.

**S3.** Two of the 62 `items.json` "not-DONE" IDs are already marked DONE in `QUEUE.md` itself: SENSE-CELL (`QUEUE.md:83`; the T10 hit is a substring of SENSE-CELL-MATCHED, not this item) and CAUSAL-KAPPA-LENIENCY-REVIEW (`QUEUE.md:437`). The remainder is therefore slightly stale relative to the markdown. Not a drop; worth a one-line note, or drop those two from the "62" if the page is edited anyway.

**S4.** `test_real_ledger_no_longer_crashes_on_entry_156` runs the live scorer on the real ledger. That is a fair smoke test of the crash, but keep it from being mistaken for the official Q0 score: it already avoids asserting an AUC; a one-line comment that this is not the official score would make that obvious in the test file.

## What I am not blocking on

The 62-item remainder, as a remainder, is an allowed way to avoid folding every frozen-queue ID into `OPEN_WORK.md`. STATUS's "Next" list is no longer a second live list; that part of the hygiene job is done. Reviews 26, 27, 29 and the #115 re-review are honestly reported as not found (W6). Stale branches are listed and not deleted. CLAIM_MAP stays at v2.68, as stated. I did not re-review the scientific content of the committed reports, only the hygiene checklist above.
