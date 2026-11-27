# DEVIATIONS from PREREG.md

*Friday 27 November 2026 (America/New_York). Appended in order; entries are not edited after the fact.*

## D1. The toy run of the first lock stopped in a helper (machinery, not mathematics)

- **Lock.** `checks/SHA256SUMS`, commit `289b639e5bb5e13b7b05bb576c731e1299516342`, pushed and seen with `git ls-remote` before the run.
- **What happened.** Step 2 (toy run) from a fresh clone at that commit printed the helper outputs up to `tp_value`, then stopped in `tp_equilibrium` → `tp_next` → `brentq` with "f(a) and f(b) must have different signs" (`checks/toy_smoke_run1.out`, box paths replaced by `<clone>` and `<site-packages>`). No check line had run; the full run (step 3) was not started.
- **Cause.** `tp_next` bracketed the next boundary at \(q_k(1+10^{-15})\). For a target just above \(q_k\) that bracket can round so that the bracketing function is not negative there.
- **Fix.** `checks/swarm27_fix1.py` imports the locked script and replaces `tp_next` with one that brackets at \(q_k\) itself, where the function equals \(q_k-\text{target}<0\) whenever the target exceeds \(q_k\) (checked just above). Nothing else changes. The locked files keep their bytes, so `checks/SHA256SUMS` still verifies. `checks/test_swarm27_checks.py` (locked, runs the unpatched script) is kept and not collected (`checks/conftest.py`); `checks/test_swarm27_run.py` runs the patched script. `checks/toy_smoke_2.py` repeats the toy run with the patch.
- **New lock.** `checks/SHA256SUMS_2` covers this file, the fix, the second toy script, the new test, the conftest and the first toy output. Steps 2–4 of `PREREG.md` are repeated under it.
- **Effect on results.** None on the notes' proofs. The numbers in the notes come from the run under the second lock.
