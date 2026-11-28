# Confirm review of PR #140 (live git brief)

**Reviewer:** blind confirm. This pass wrote none of the brief, the freshness check, or `reviews/brief_2026-11-21/REVIEW.md`. Nothing here was committed, pushed, or merged.
**Date:** Saturday 21 November 2026, about 2:26 PM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/140
**Head:** `ea871a7a47b44b95c0b23cc786c1bad5946be9b8` on `live-brief-2026-11-21`.
**Base:** `main` `2c32ade7bb48917a8fb5996ac7a840e94f349b70` (`origin/main`).
**First review:** `reviews/brief_2026-11-21/REVIEW.md`, READY-WITH-FIXES, written against `6f824e47728010aa2fb33f478dfc842f62ee49ab`. The only commit since that review is `ea871a7`.

**Verdict: READY.**

The four should-fixes landed and were re-checked, including on a throwaway repository. Unquoted `main is feedback` produces no SHA. Unbackticked `current to main <sha>` is a pointer. The `CORE.md` hypothesis sentence is unchanged. Residuals below can ship.

## Should-fixes

1. **Freshness window.** `tools/check_fresh.py` `history_tip` uses `refs/remotes/origin/main`, then `refs/heads/main`, then `HEAD`, and judges the last 5 first-parent commits of that tip. `STATUS.md:17` names main (`origin/main` if that ref exists, otherwise local `main`). On a throwaway repo, a branch 6 commits ahead of main, with `origin/main` at that main and `STATUS` naming it, passed. A window taken from `HEAD` did not contain that main SHA. Pointing `STATUS` at a local `main` that had been moved to the branch tip failed, and `resolve_main` still returned `refs/remotes/origin/main`. With the origin ref deleted, local `main` was used and the branch-point pointer passed. With neither ref, the fallback is `HEAD`: naming `HEAD` passed, and naming the commit 6 behind `HEAD` failed. On this repo the window is `2c32ade 6222c38 5f252e6 cd84095 32b46bd`. `a65b64e` is `#132`, two merges past that window, so the width of 5 still excludes it.

2. **`tools/brief.py` `resolve_main`.** The lookup order at line 49 is `refs/remotes/origin/main`, `refs/heads/main`, `HEAD`. The throwaway case with local `main` ahead of origin returned the origin SHA. This checkout resolves `refs/remotes/origin/main` `2c32ade7bb48917a8fb5996ac7a840e94f349b70`.

3. **Nested copy.** `is_git_repo` returns false when `os.path.join(root, ".git")` is absent, before git is called. A nested copy whose `STATUS` said `deadbee` was skipped. `git rev-parse --is-inside-work-tree` from that copy was true, because git walks up to the parent. The parent still failed on `deadbee`.

4. **`OPEN_WORK.md:3` and `:91`.** Line 3 says W15’s confirm is READY (`reviews/revealed_prices_2026-11-21/CONFIRM.md`; that verdict is READY) and that C7 still needs Chad. `cda9c41` is the `#133` merge and is an ancestor of `origin/main`. Line 91 says EVO1 (W2) merged as `2c32ade` and is not the live test. W2 is DONE at that merge.

## Regex and hypothesis

`main is feedback`, `main is feedback.`, `main is Feedback`, `` `main` is `feedback` ``, `main is `feedback``, and `current to main feedback` produce no pointer in `tools/brief.py` and no SHA in `tools/check_fresh.py`. `current to main deadbeef` is one pointer, with or without a trailing period or comma, and with backticks on `main`, on the SHA, or on both. The live hits in `STATUS.md`, `OPEN_WORK.md`, and `CORE.md` are only `2c32ade`.

`CORE.md:24` matches `2c32ade` byte for byte: “The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.”

`domain is deadbeef` and `remain is deadbeef` still match, because the unquoted `main is` pattern has no leading word boundary. Those phrases are absent from the three pointer files. A leading `\b` is the fix (`tools/brief.py:267`, `tools/check_fresh.py:26`).

## Residuals

- `OPEN_WORK.md:27`: W15’s state still says “needs confirm review” and the gate is `needs reviewer`. Set the state to `**DONE.** Merged as `cda9c41`; confirm READY (`reviews/revealed_prices_2026-11-21/CONFIRM.md`)` and the gate to `DONE`.
- `OPEN_WORK.md:92`: replace “needs confirm + Chad's call” with “confirm READY (`reviews/revealed_prices_2026-11-21/CONFIRM.md`); needs Chad's call”.
- `OPEN_WORK.md:20`: mark `#118` (`ff14a87`) and `#119` (`d907f6b`) done in the W8 arrow. Both are on main. The gate can say reorganization is still open and the sequence through `#119` is on main.
- `CORE.md:3`: say that `#114` (`ed6bf7c`) rewrote the §6 evolution bullet (`CORE.md:60`). PRs `#120`–`#132` left the body unchanged. The hypothesis sentence was not part of that edit.
- `STATUS.md:17`: add “otherwise HEAD” after “otherwise local `main`”.
- `tools/brief.py:126`: drop the unused `seen`. `tools/brief.py:210`: delete the unreachable `Status now (all sections)` branch. `tools/brief.py:218`: use `r"^DONE(?!-)(\b|$)"` so `DONE-ish` stays open.

## Checks

- `python3 tools/check_consistency.py`: RESULT PASS (0 FAIL, 23 INFO). Advisory length warnings: THEORY.md 10471 words, README.md 1468.
- `python3 tools/check_open_work.py`: RESULT PASS (0 missing).
- `python3 -m pytest -q tools`: 165 passed, 1 skipped (`tools/test_lean.py:101`, Lean 4 / lake is not installed). Five of those passes are the new window, nested-copy, and regex tests.
- `python3 tools/brief.py`: exit 0. main `2c32ade`, Sat 21 Nov 2026, 11:01 AM ET, resolved from `refs/remotes/origin/main`, THEORY v2.9, CLAIM_MAP v2.69, tally 327, 52 open-work rows, Pointers OK.

The residuals listed above were applied after this branch was rebased onto `main` `a97887e` (PRs #138, #139 and #141). The pointer lines in `STATUS.md`, `OPEN_WORK.md` and `CORE.md` were updated to that main, W15 and W16 were marked DONE, and the regex / brief.py residuals were applied, in the next commit.
