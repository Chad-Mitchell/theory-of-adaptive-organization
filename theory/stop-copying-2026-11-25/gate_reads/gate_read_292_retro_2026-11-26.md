# Retrospective independent gate read of #292 `PREREG_5.md`

*Copied from §8 of the hostile review of the FOR-36 fix commits (session file `HOSTILE_REVIEW_FIX36.md`, Thursday 26 November 2026, 03:01 ET, fresh-context reviewer). Unchanged except for this header. Retrospective: the runs were on 25 November at 22:11–22:41 ET.*

## 8. Independent gate read: #292 `PREREG_5.md`

This read is retrospective. The runs already happened (22:11–22:41 ET, 25 Nov), but I did not open RESULTS, `run_t*_v2.out` scores or `aggregate.out` before writing it. I only counted lines: each `.out` has 5 SETTING_JSON lines and 1 TOTAL_JSON.

- **Scope.** PREREG_5 adds no new Gate table. G1–G5 come from PREREG_2 as amended by PREREG_3 and PREREG_4, which I read. Hit: A > 0.12 at all 5 settings, honest hit odds 0.12. T2 is the same with A_(5). G2: global minimization with no closed form. G3, G4 and G5 are as in PREREG_2.
- **Well-posed:** yes.
  - The completeness rule (§1) is defined.
  - The 4 paths have locked one-line commands. The functions and signatures exist in `checks/aggregate.py`, and `checks/test_prereg5_paths.py` gives 5 passed.
  - One loophole: "complete" means **at least** five SETTING_JSON lines. That should be exactly the five locked settings, distinct, plus TOTAL_JSON. Not material here.
- **Hit rule fairness:** fair to strict. All-five plus resolution, and every degenerate label (not settled, budget, guard, measurement/code, incomplete) scores as a miss, so the hypothesis cannot win on a technicality.
- **One issue: §2 relabels.** §2 replaces an unreachable clause (correctly argued so) with "any post-hoc relabel … recorded in `checks/RELABELS.md`", with no stated grounds and no rule that scoring uses the unrelabelled labels. That opens an unlocked degree of freedom after the run. Add: scoring uses the script labels; relabels are reported beside them and cannot move a miss to a hit.
- **Gate status:** pass as a TEST, with the §2 relabel caveat. The process breach stands as logged: v5 passed by the author agent, not by a fresh reader. This read can be recorded as the owed independent read, but only as retrospective.

