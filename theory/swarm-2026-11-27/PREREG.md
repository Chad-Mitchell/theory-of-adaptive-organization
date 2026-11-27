# PREREG (CONSISTENCY_CHECK): numeric checks for the swarm rule completion

*Friday 27 November 2026 (America/New_York). Written and hash-locked before any run of `checks/swarm27_checks.py`, `checks/toy_smoke.py` or `checks/crossref_check.py` in this branch (lock: `checks/SHA256SUMS`). Branched from `863a8a8bb3e0bb46c00a9236a9b4d5192c4b9d8d`. Process: `process/PREREG_GATE.md`.*

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

## Gate

| Field | Answer |
|---|---|
| **G1. Miss** | A `CHECK FAIL` line, or a nonzero exit, in `checks/swarm27_checks.py`. Honest odds of a miss on the mathematics: about 0, because each line re-computes a statement proved on paper in this folder or evaluates a stated formula or counterexample. Odds of a machinery miss (a bug in the rebuilt sections A and B, written after a box restart erased the first version): not small. |
| **G2. Not an identity** | Fails G2. Every scored value follows from the proofs in this folder, from `THEORY.md` Appendix B, or from known theorems (credited in the notes). |
| **G3. Named rival** | None needed for a CONSISTENCY_CHECK. |
| **G4. Reach** | Level (a), toy classes we built. No route to (b) or (c) is claimed from these numbers. |
| **G5. Next step** | All pass: the outputs are committed and the notes cite them by check name. A `FAIL`: the line is reported in `DEVIATIONS.md` in this folder with its cause; a code fix goes in a new commit with a new lock (`checks/SHA256SUMS_2`), and the original lock and output are kept. |

**Label.** Every check is `CONSISTENCY_CHECK` (`process/PREREG_GATE.md` §3): information about 0, never a support headline, one ledger line each in the sense of the gate (here the rows SWARM-* in `measurement/CLAIM_MAP_v2.md`, whose status comes from the proofs, not from these runs).

## What is run, in order

1. **Lock.** `checks/SHA256SUMS` holds the sha256 of this file, `checks/swarm27_checks.py`, `checks/toy_smoke.py`, `checks/crossref_check.py` and `checks/test_swarm27_checks.py`. The lock commit is pushed and seen with `git ls-remote` before step 2.
2. **Toy run (launch rule).** From a fresh GitHub clone at the lock commit: `nice -n 19 python3 theory/swarm-2026-11-27/checks/toy_smoke.py > toy_smoke.out`. Its sha256 is written to `checks/SHA256SUMS_toy`, committed and pushed before step 3.
3. **Full run.** From a fresh GitHub clone at the commit of step 2: `nice -n 19 python3 -u theory/swarm-2026-11-27/checks/swarm27_checks.py > swarm27_checks.out`, budget 15 minutes wall time (the predecessor of this script, before the box restart, ran in about 4 s; the toy run's section A time is recorded in step 2). The output is committed as `checks/swarm27_checks.out`.
4. **DOIs.** From the same clone: `nice -n 19 python3 theory/swarm-2026-11-27/checks/crossref_check.py > crossref.out`, committed as `checks/crossref.out`.

## Known history (disclosed)

A predecessor of `swarm27_checks.py` (sections A–H, all passing) and of `crossref_check.py` (31 of 31 DOIs) was run on the box on 27 November 2026 before any lock, in a clone under `/tmp` that a box restart erased before anything was pushed (`process/FAILURES.md`, row `SWARM-ABORT-1`). Sections B–H of the present script are that predecessor's text, recovered from the session record; section A and the telling-price helpers were rewritten. Two checks were added after that run (`proportional_shares_reward_underreporting`, `pair_floor_under_tamper`; the second was run once, unlocked, before the restart). Numbers quoted in the notes come from the locked run of step 3 or are computed by hand from stated formulas.
