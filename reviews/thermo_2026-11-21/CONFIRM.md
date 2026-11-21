# Confirm review: PR #122 at 2a63897 (S1–S5 fix commit)

**Reviewer:** independent (wrote the first review of `3517e46`; wrote none of the fix commit, the T27 package, PREREG, predictions, runner, library, official run, RESULTS, DEVIATIONS, BRIDGE / FLOOR / SELECTION, OPEN_WORK / STATUS edits, or math_checks).
**Date:** Saturday 21 November 2026, started about 12:33 AM ET, finished about 12:38 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/122
**Clone:** fresh `/workspace/gtao-confirm122/repo` (not the first-review clone), branch `thermo-bridge-2026-11-21` at head `2a638978f5983416289b5ae10e33fdab59434d56` (parent `3517e465e94e2b791f965f12b36910bfcd724d89`; merge-base equals base `4398bbdc434b766d4b761aa86d8b8836b0ef8c4c`). Clean tree at confirm start. Nothing pushed or merged at the start of this confirm. `/workspace/looper` was not touched. Branches `lean-core-2026-11-21` and `ecoli-qual-2026-11-21` were not checked out or otherwise touched. Compute at nice 19.

**Verdict: READY**

S1–S5 are fixed correctly. The P3 lesson is framed as not-a-rescue. DEVIATIONS states the mid-run protocol lapse plainly. The locked prereg, predictions, lock record, and official run artifacts are byte-identical to `3517e46`, and their SHA-256 values still match the recorded locks. The official verdict is unchanged: **FAIL** (P1 PASS 3/3, P2 PASS 3/3, P3 FAIL 0/3). No overclaim. `CORE.md` and the hypothesis sentence are unchanged. Checkers and `pytest tools/` pass. No new problem that would reopen the review. Residuals below do not block.

The fix commit is `2a63897` (“Apply review S1–S5 for PR #122 (post-result housekeeping)”), authored 12:33:21 AM EST on 21 November 2026. It touches only `OPEN_WORK.md`, `core/bridge_2026-11-21/BRIDGE.md`, `core/bridge_2026-11-21/DEVIATIONS_2026-11-21.md` (added), `core/bridge_2026-11-21/RESULTS.md`, `core/bridge_2026-11-21/SELECTION.md`, `reviews/README.md`, and a byte-identical copy of the first review at `reviews/thermo_2026-11-21/REVIEW.md`. Locked `PREREG.md`, `predictions.json`, `LOCK.txt`, `PREREG.sha256`, `PREDICTIONS.sha256`, `run_t27.json`, `run_t27.log`, and the committed `run_t27.py` / `bridge_lib.py` are not edited.

---

## S1 — fixed

The OPEN_WORK header tally is now “126 tests,” matching `pytest tools/` on this head (126 passed, including `tools/test_bridge_checks.py`). The as-of line is updated to about 12:35 AM ET and records the READY-WITH-FIXES review and that no official number changed. W13 and T27 still report official FAIL, P1/P2 3/3 and P3 0/3, and “no rescue,” and now point at the deviations file and the committed first review. Their gate is “needs reviewer (confirm of the fixes),” which is the right residual state at this head.

## S2 — fixed; protocol lapse stated plainly

A dated file, `core/bridge_2026-11-21/DEVIATIONS_2026-11-21.md`, records the mid-run `moran_fixation` rewrite as **D1, a protocol lapse**. It is not a rule change and it is not a rescoring.

The times match the first review: lock 12:05:31 AM EST; official start 12:05:33 AM EST; `bridge_lib.py` rewrite mtime 12:06:26 AM EST; official finish 12:07:41 AM EST (127.2 s). The official log still shows the overflow at the pre-rewrite line 180 (`gN = gamma ** N_pop`) on the first official world, and this confirm re-read that warning in the locked `run_t27.log`. The note states that the official process had already imported the pre-rewrite function, so all three official worlds were scored with the overflowing formula; that the committed rewrite is a log-stable form of the same identity; that the two formulas agree to machine precision on a wide γ grid, including the overflow regime; and that a later re-run of the committed runner reproduced official `run_t27.json` exactly except wall-clock `seconds`. The official JSON SHA-256 `daf2ac2d446a457a74e14c555db3fe689561c54c7871d4086b6f0e3c5919927a` is recorded, and those bytes are still the committed file. RESULTS.md no longer says “No DEVIATIONS file was required”; it points at this note. No gate is reopened.

## S3 — fixed

The same deviations file records the committed hashes, which this confirm re-hashed on disk and found unchanged from `3517e46` and from the hashes the first review asked to record:

| File | SHA-256 |
|---|---|
| `run_t27.py` | `26039b3c81862f36e01ac516d17aa91ab6fd50e4b36cebfd0aafeaa0ccbdb19a` |
| `bridge_lib.py` | `4e779b3dd4754dfa29a4ef74836a8986837f31a92c55601ae32579911e4b8fd2` |

A standing rule is stated: future tests must hash-lock the runner and the library at lock time, the same way the prereg and the predictions are locked, and a mid-run rewrite, even a numerically equivalent one, is a protocol lapse. `LOCK.txt` itself is correctly left unedited.

## S4 — fixed without touching the lock

D2 in the deviations file, and a matching sentence in RESULTS.md, record that the locked `PREREG.md` header says “Friday 20 November 2026, late evening ET” while `LOCK.txt` is Saturday 21 November 2026, 12:05:31 AM EST. `PREREG.md` is not edited. The lock hashes still match.

## S5 — fixed

`BRIDGE.md` now flags, in the “already in the repository” list, in the \(z\) paragraph, and in the one-picture paragraph, that \(\sigma\) in \(z=B/(\sigma\tau^H)\) is the CT18 shock scale, while \(\sigma\) in \(\varepsilon=10/(\sigma N_e)\) is the cost-to-fitness map of THEORY §3 / FRAMEWORK §9. The two share a letter and are not identified. `SELECTION.md` adds the same flag in the two-temperature section. No other claim in those paragraphs was changed.

---

## P3 lesson is not a rescue

RESULTS.md adds a section titled “Lesson (not a rescue).” It states that the two-\(K\) floor was ill-posed at lock time: exact Boltzmann weights on the only pre-lock published pilot (S5 rng seed 1000) already miss the 0.10 floor at the locked \(\beta=0.5\) (\(K=3\) mass 0.908, \(K=2\) mass 0.090), that \(\beta=1.5\) is not the locked value, and that the official 0/3 is the same pattern, not a surprise about the sampler. It says, twice, that the paragraph does not change the official FAIL and is not a rescue of P3, and that a different spread statistic would be a new prereg. The procedural lesson (compute exact-Boltzmann gate values on published pilots before locking) is a future-prereg rule, not a rescoring. Official table numbers in RESULTS.md are unchanged versus `3517e46`.

---

## Locked files and official gates

Byte-identical to `3517e46`, and SHA-256 still matches the recorded locks:

| File | SHA-256 | Witnesses |
|---|---|---|
| `PREREG.md` | `25955df4ffb825254100568c9b9d1e751b9d5e0e533146a5d438414c8d5ba994` | LOCK.txt, PREREG.sha256, `run_t27.json`, RESULTS.md, DEVIATIONS, re-hash of the file on disk (10047 bytes) |
| `predictions.json` | `6715777ca45d02ad443a3e5003f19849331a9e60dba900aa6f6c68c93e7adfe3` | LOCK.txt, PREDICTIONS.sha256, `run_t27.json`, RESULTS.md, DEVIATIONS, re-hash of the file on disk (2246 bytes) |

Also byte-identical to `3517e46`: `LOCK.txt`, `PREREG.sha256`, `PREDICTIONS.sha256`, `run_t27.json` (SHA-256 `daf2ac2d446a457a74e14c555db3fe689561c54c7871d4086b6f0e3c5919927a`), and `run_t27.log` (SHA-256 `9ad73799e2c052713dadf73e31eb2cf7cc0cc29826dbe1177c43d6c40629cf9c`). This confirm rescored P1, P2, and P3 from the stored occupation summaries in `run_t27.json`. Official gates are unchanged versus `3517e46` and versus the first review:

- P1: **PASS**, 3/3 worlds, 9/9 cells. Modes 157, 146, 180 equal the coarse argmin. TVs 0.0089, 0.0014, 0.0389; 0.0160, 0.0195, 0.0029; 0.0422, 0.0110, 0.0195.
- P2: **PASS**, 3/3 worlds, 9/9 cells. Empirical \(\beta\)-excess 0.922–1.065 (max relative error 7.8%) against \(d/2=1\) and a 20% bar. Exact Boltzmann diagnostic 1.004–1.011.
- P3: **FAIL**, 0/3. Clauses 1 and 3 hold (means 104.905, 104.879, 104.827 against \(J^\star\) 102.080, 102.296, 102.445; excess ratios 168.50, 104.88, 59.38). Clause 2 fails on every world: masses on \(K=0,1,2,3\) are 0.000, 0.001, 0.085, 0.913; 0.000, 0.001, 0.066, 0.933; 0.000, 0.000, 0.066, 0.934. One \(K\ge 0.10\) in each case.
- Overall: **FAIL**. Three official-valid worlds (seeds 2026112100–02; none rejected). A fail on any locked gate is a fail of the prereg. No rescue is registered.

`run_t27.json` summary is `P1=True`, `P2=True`, `P3=False`, `OVERALL=False`. The official log begins `LOCK ok` and ends with the same summary and a 127.2 s write.

---

## No overclaim; CORE.md and the hypothesis sentence

No “all physics” claim; BRIDGE.md still denies it in so many words. Nothing is “proved about nature.” Official labels remain in-model, numerical, FAIL. The hypothesis remains a hypothesis. T26 is still labelled “Hypothesis, not a result,” not a new term in \(J\), and not a change to CORE.md.

`CORE.md` is byte-identical to `3517e46` and to `origin/main` (`4398bbd`). `THEORY.md` is unchanged versus `origin/main`. The hypothesis sentence is unchanged in both files:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

---

## Checkers and tests (nice 19, this clone, at `2a63897`)

- `python3 tools/check_open_work.py`: RESULT: PASS (union of not-DONE items.json / QUEUE.md missing from OPEN_WORK.md = 0).
- `python3 tools/check_consistency.py`: RESULT: PASS (0 FAILs). Soft length warnings only (THEORY.md 10471; README.md 1468; advisory, pre-existing). Frozen-record INFO hits 23; wording FAILs 0.
- `python3 -m pytest tools/ -q`: **126 passed** in 111.45 s.

The first review committed at `reviews/thermo_2026-11-21/REVIEW.md` is byte-identical to `/workspace/review-archive/rev122_REVIEW.md` (SHA-256 `fa7331f3a1be198483595496489ab4c360f5d674b397da4b05e43de47135f5c6`, 142 lines).

The pull request was OPEN and MERGEABLE at the start of this confirm, head `2a63897`.

---

## Residuals (do not block)

- RESULTS.md’s lead sentence still says “P3 failed 3/3” (failed on all three worlds) while the section header says “P3 — FAIL, 0/3 worlds.” That wording was already in `3517e46` and was not introduced by the fix. The split is unambiguous in context.
- The locked official log still names `/workspace/gtao-thermo/…`. That is historical run text and was correctly left unedited.
- Mentions of “125 tests” remain in earlier review files (`reviews/core_2026-11-20/rev119_REVIEW.md`, `reviews/wf_2026-11-20/REVIEW.md`, and the first review of this PR). Those are dated records. The live OPEN_WORK header is 126.
- W13 and T27 remain “needs reviewer (confirm of the fixes)” at this head, which is correct until this confirm is committed.
- D1’s committed-code re-run (12:27:51 AM EST, 123.841 s) is a later author re-run, distinct from the first review’s independent re-run (124.6 s). Both are described as matching official `run_t27.json` except `seconds`. This confirm did not perform a third full re-run; the official artifacts are byte-identical to `3517e46`, and the gates recompute from those stored outputs.

No new “law” beyond the standing hypothesis sentence. No “theory of everything.” Nothing in these files is called PROVED about nature.

This report: `/workspace/review-archive/rev122_CONFIRM.md`.
