# Independent review of PR #140 (live git brief)

**Reviewer:** independent read-only pass. Nothing here was committed, pushed, or merged.
**Date:** Saturday 21 November 2026 (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/140
**Head:** `6f824e47728010aa2fb33f478dfc842f62ee49ab` on `live-brief-2026-11-21`.
**Base:** `main` `2c32ade7bb48917a8fb5996ac7a840e94f349b70`.

**Verdict: READY-WITH-FIXES. No blockers.**

Reversible tooling plus pointer hygiene. The CORE diff is the header line. The hypothesis sentence is unchanged. `brief.py` parses this repo's merge commits, renders America/New_York (EST in November, EDT in July), skips open PRs when `gh` is missing, and warns only on current pointers. Historical `on main at SHA` and table-row `beside main SHA` do not warn. `check_fresh.py` uses the last 5 first-parent commits including HEAD, expands `2c32ade` to the full hash, and skips a directory that is not inside any repo. W2 and W10 DONE at `2c32ade` with CLAIM_MAP v2.69 (tally 318 to 327) match the `#114` merge and `reviews/evo1_2026-11-21/` (both rounds READY-WITH-FIXES). S9a–S9e listed as open work is the gate rule: their state is `applied`, and S5 in the same table is `**DONE.**` and is omitted.

## Should-fixes (on this branch before merge)

1. **`tools/check_fresh.py:90` counts the window from HEAD.** A feature branch fails a correct `main is <branch-point>` pointer at 5 commits ahead (passes at 4). `#114` was 10 first-parent commits; `#133`–`#137` were 7 or 8. Judge `origin/main`, else local `main`, else HEAD. Keep the width at 5: one merge commit on main leaves the previous SHA inside the window, and `a65b64e` is six merges behind `2c32ade`, which is the miss this check is for. Update `STATUS.md:17` to say main, not HEAD. Add a test with six commits on a side branch.
2. **`tools/brief.py:42` prefers local `main` over `origin/main`.** A local main left behind after fetch is then treated as an allowed pointer. Look up `refs/remotes/origin/main` first.
3. **`tools/check_fresh.py:68` does not require a `.git` in the directory it was given.** A nested copy with no `.git` is graded against the parent repo and fails. Return false when `os.path.join(root, ".git")` is absent. Outside-repo copies already skip, which is why `test_check_consistency.py` passes.
4. **`OPEN_WORK.md:3` says W15 still needs confirm review.** `reviews/revealed_prices_2026-11-21/CONFIRM.md` is READY (`353aa5f`); `#133` merged as `cda9c41`. Say that, and that C7 still needs Chad. **`OPEN_WORK.md:91`** still says EVO1 is the live in-silico test. Say it merged as `2c32ade`.

## Nits

- Unquoted `main is feedback` parses as SHA `feedbac` (`tools/brief.py:260`, `tools/check_fresh.py:25`). `current to main <sha>` without backticks is missed. Live files use backticks.
- `OPEN_WORK.md:27` W15 gate is still `needs reviewer`. Same READY confirm as should-fix 4. The row predates this diff.
- `OPEN_WORK.md:20`: `#114 (done, 2c32ade)` is right. The arrow still lists `#118` and the CORE PR after it. Both are on main (`ff14a87`, `#119` `d907f6b`).
- `CORE.md:3`: `#114` rewrote the §6 evolution bullet, so the body is not only the text written beside `ff14a87`.
- `tools/brief.py:121` unused `seen`. `tools/brief.py:204-206` unreachable tally branch. `DONE-ish` matches `is_done_gate` (`tools/brief.py:213`).

## Merge order

`#138` (`dir1-directional`, `0aad420`, draft) and `#139` (`shannon-core-2026-11-21`, `7d8690c`) merge cleanly with each other. `#140` conflicts with `#138` in `STATUS.md` and `OPEN_WORK.md`, and with `#139` in `CORE.md`. Merge `#139` and `#138` in either order, then rebase `#140` last. Keep `#139`'s CORE. Keep `#140`'s pointer lines and W8. Keep `#138`'s DIR1 paragraph and W16. Do not take `#138`'s W2 row whole: it has six cells on a five-column table.

## Checks (this pass)

- `python3 tools/check_consistency.py`: RESULT PASS (0 FAIL, 23 INFO).
- `python3 tools/check_open_work.py`: RESULT PASS (0 missing).
- `python3 -m pytest -q tools`: 160 passed, 1 skipped (`tools/test_lean.py:101`, Lean not installed).
- `python3 tools/brief.py`: exit 0. main `2c32ade`, Sat 21 Nov 2026, 11:01 AM ET, THEORY v2.9, CLAIM_MAP v2.69, tally 327, 52 open-work rows, Pointers OK.
