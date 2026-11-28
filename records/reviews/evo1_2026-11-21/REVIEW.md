# Independent hostile review of EVO1 final results (draft PR #114, head 6f95897)

*21 Nov 2026 (ET). A separate cloud agent with no stake, told to break the verdicts. It did not commit, push or open a PR; this file is the lead executor's record of its report.*

**Verdict: READY-WITH-FIXES. No blockers.** The eight world verdicts and the secondaries reproduce from the locked runs. Nothing flips a verdict.

## Verified clean
- Lock: `sha256sum -c PREREG_EVO.sha256` OK for every file except `theory/layers_checks/stores.py` (changed on main by PR #116 after scoring; locked bytes at `70fcbad`). `git diff 70fcbad HEAD` is empty for `analyze_evo.py`, `evo.py`, `predict_evo.py`, `worlds.json`, `PREDICTIONS_EVO.json`, `count_rule.py`, `PREREG_EVO.md`, `figures/face_hybrid.py`.
- Rerun of `analyze_evo.py` on the committed runs with the locked and with the current `stores.py`: the locked one matches the committed analysis on every field; the current one moves only two W3 null J gaps (7.45e-11, 4.97e-11). D4's size claim holds.
- Verdicts re-derived from `runs/*.json`: PC PASSED 0/8; W1 PASSED 0/8; W2 PASSED 1/7; W3 INVALID (raw PASSED; deaths 10.62–15.24%); W4 FAILED 3/8; W4b FAILED 8/8; S031 and S07 INCONCLUSIVE 2/8 (criterion A only). Null controls 0/4 in all worlds. Rival gates all ≥ 10 (S031 40.4, S07 175.1, W4b 93.8). Secondaries PC→W1, S031→S07, threshold 8/8 and 8/8.
- All 96 run files present, each G = 600 with 600 log rows. The improving rule flips no seed under a window-median rule.
- S-arm correlations (0.787, 0.058), medians and per-seed gaps recomputed correctly.
- D1/D2 were declared before the runs they govern (`cf77048` 13:51:47, `610e87a` 14:18:46; outputs first in `b5d1805` 15:44:09); the ≥ 3/4 bars never changed.
- `tools/check_consistency.py` PASS (tally 327); `pytest tools -q`: 146 passed, 1 skipped (Lean not installed).
- The reachability reading is not in THEORY.md; it is already in `core/KEYSTONE_NOTE.md` and `core/bridge_2026-11-21/SELECTION.md`. It is a reading of this experiment, not new theory.

## Should-fixes (all applied; see commit after 6f95897)
1. The band formula was written 1/(βP); the locked band is 10/(βP) = 1/900 = 0.001111… (the number used was right).
2. "4–16% over the band" was wrong: the misses are 1.5% (S07 s1), 9.0% (S07 s2), 11.2% (S031 s1), 16.0% (S031 s2) over.
3. D4's account of the S031 seed-2 log was wrong: the locked printer also writes at g = G−1, so a finished log would contain g599; the log was cut off (as were other recovered logs); the run file is complete and is what the scorer reads.
4. D1c-ruin mutant death range is 20.7–36.3%, not 22–36%.
5. W2 seed 2 is unscored and outside the band; interlacing is 7 of 8 seeds, not 7/7 scored.
6. CORE.md and OPEN_WORK.md stated W4b's valley as shown where D1b's bar failed (2/4), used bare PASSED/FAILED, and CORE.md line 3 still said CLAIM_MAP v2.68.
7. PREREG §5's W3 "none" cell (gap 0) disagrees with the locked prediction file (inf); recorded as D5, prereg not edited.
