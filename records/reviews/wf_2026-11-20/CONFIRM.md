# Confirm review: PR #121 at 4253fce (S1–S3 fix commit)

**Reviewer:** independent (wrote the first review of `4b3df21`; wrote none of the fix commit, the WF-HSV package, OPEN_WORK T26, or any other file in this PR).
**Date:** Saturday 21 November 2026, started Friday 20 November 11:58 PM ET, finished Saturday 21 November about 12:03 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/121
**Clone:** fresh `/workspace/gtao-confirm121/repo` (not the first-review clone), fetched `pull/121/head`, checked out `4253fce70044a59788494df7a50bb9ff499fa0eb` (parent `4b3df21155719287ee08c25e093d4e2ba6556b0f`; base still `7275c4b`). Clean detached HEAD. Nothing pushed or merged at the start of this confirm. `/workspace/looper` was not touched. The branch `thermo-bridge-2026-11-21` was not touched. Compute at nice 19.

**Verdict: READY**

S1–S3 are fixed correctly. D2 is honest post-result housekeeping. The locked files are byte-identical to `4b3df21` and their SHA-256 values still match the recorded locks. Official gates are unchanged. T26 is labelled a hypothesis. `CORE.md` and the law sentence are unchanged. Checkers and `pytest tools/` pass. No new problem that would reopen the review. Residuals below do not block.

The fix commit is `4253fce` (“Apply PR #121 review fixes (S1–S3) and add T26”), authored 11:57:59 PM EST on 20 November 2026. It touches only `OPEN_WORK.md`, `DEVIATIONS_2026-11-20.md`, `RESULTS.md`, `build_predictions.py`, `run_wf.log`, `run_wf.py`, `worlds.py`, `reviews/README.md`, and a byte-identical copy of the first review at `reviews/wf_2026-11-20/REVIEW.md`. `PREREG.md`, `MATH.md`, `wf_rule.py`, `wf_predictions.json`, `LOCK.txt`, `START.txt`, `PREDICTIONS.sha256`, `wf_run.json`, `wf_score.json`, and `CORE.md` are not edited.

---

## S1 — fixed

Newly authored, non-locked *code and run artifacts* no longer hardcode box paths.

- `worlds.py` now sets `REPO = Path(__file__).resolve().parents[3]` and loads exclusion inputs from the public clone (`rhythm_rule.json`, `s5_rerun.json`, T20 `predictions.json`, `imp_n60_predictions.json`).
- `run_wf.py` uses the same repo-relative root, writes RESULTS under `core/keystone_checks/waterfill_2026-11-20/`, and the RESULTS template names that package path instead of `/workspace/gtao-wf`.
- `build_predictions.py` looks for `PREREG.md` / `MATH.md` beside itself (`ROOT = HERE`).
- `run_wf.log` path prefixes were redacted to repo-relative / package-relative forms (`core/keystone_checks/waterfill_2026-11-20/run_wf.py:…`, `scipy/_lib/_util.py:…`, `wrote RESULTS.md`). The three Lyapunov warning texts and the run lines are otherwise unchanged.

Hash-locked files still mention `/workspace/gtao-wf` (and, in MATH.md / PREREG.md, `/workspace/gtao-t20`). That is what the first review allowed. The committed first review also names its working clones; it was left unedited and is byte-identical to the archive (see residuals).

## S2 — fixed without rescoring

The exclusion loader now implements the prereg §4 set: rhythm-test worlds from `rhythm_rule.json`, S5 seeds 0..119, the T20 18, and the 15 rhythm-prereg fractal worlds (reconstructed from the locked `scalefree_world` formula and metadata in `imp_n60_predictions.json`). Model S now calls `_too_close` and records a bump on redraw, for later use only.

This confirm regenerated all 64 official worlds from the new generators: ids match, `(a,v,N)` are bit-identical to the locked predictions, and every world has `bumps=0`. The official set is not regenerated or rescored. The loader returns 174 excluded rows (21 rhythm-test + 120 S5 + 18 T20 + 15 fractal), which is the full prereg set. D2 correctly calls the original gap a procedure miss, not a contaminated set.

## S3 — fixed

RESULTS.md “Suspicious points” now names three SciPy Lyapunov `RuntimeWarning`s: two early in the rhythm phase, and a third later in the mixed phase, just before `mx_0006` completed. The official log (after prefix redaction) has exactly those three, at the stated places (the first two immediately before `done rh_0003`; the third immediately before `done mx_0006`). No world is flagged; no \(E\) is below the floor; not a gate change.

---

## D2 is honest post-result housekeeping

D2 is dated after official scoring (11:17 PM ET) and after the first review (READY-WITH-FIXES), at about 11:55 PM ET. It states that it is housekeeping, not a rule change and not a rescoring; that no official count or gate is changed; and that the locked files are not edited. It records S1–S3 as applied, notes that the as-run `worlds.py` hash remains the prediction-time value `f56ceaa3…` (the file on this commit differs because of S1 and S2 only), and documents S4 only, leaving the locked `wf_rule.py` fallback untouched. RESULTS.md’s integrity line and a short D2 paragraph match that account. Nothing in D2 treats a fix as a new result or moves a gate.

---

## Locked files and official gates

Byte-identical to `4b3df21`, and SHA-256 still matches the recorded locks:

| File | SHA-256 | Witnesses |
|---|---|---|
| `PREREG.md` | `9592042bc2932acec025315c5f34d401ad896a76f16940ee12c43d4be5a7bb05` | LOCK.txt, START.txt, predictions file, RESULTS.md, re-hash of the file on disk |
| `MATH.md` | `e8ea856a6d888671d2004ba82f80186f01073910bfc3f1978849c295c029e148` | LOCK.txt, predictions file, re-hash |
| `wf_rule.py` | `f9960cd49b9d01c427a6289fd91253fff70137d7352ee5b5afaed9161dbbe7d2` | LOCK.txt, predictions file, re-hash |
| `wf_predictions.json` | `ba66cef743bec29d0c2292f9b4d25c0596726623d52a05b8d881d3420fe612d1` | PREDICTIONS.sha256, START.txt, `wf_run.json`, RESULTS.md, re-hash |

`LOCK.txt`, `START.txt`, `PREDICTIONS.sha256`, `wf_run.json`, and `wf_score.json` are also byte-identical to `4b3df21`. Official gates in RESULTS.md are unchanged versus `4b3df21`, and they match the stored `wf_score.json`:

- TAUTOLOGY: PASS (`taut_ok=True`, 0 mismatches; identity diagnostic not triggered)
- SANITY: PASS (9/9)
- PRIMARY Model S: **1882/6440 = 29.22%** (0 INDETERMINATE) — FAIL
- PRIMARY rhythmic+mixed: **87/264 = 32.95%** (rhythm 47/132, mixed 40/132) — FAIL
- HOLE: **70/70** — PASS

---

## T26, CORE.md, law sentence

OPEN_WORK T26 is labelled **“Hypothesis, not a result.”** It does not add a term to \(J\), does not change CORE.md or the law sentence, and points the in-progress derivation/simulation at branch `thermo-bridge-2026-11-21` (tracked as T27). This confirm did not check out or otherwise touch that branch.

`CORE.md` is byte-identical to `4b3df21` and to `origin/main`. The law sentence is unchanged:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

---

## Checkers and tests (nice 19, this clone, at `4253fce`)

- `python3 tools/check_open_work.py`: RESULT: PASS (union missing = 0).
- `python3 tools/check_consistency.py`: RESULT: PASS (0 FAILs). Soft length warnings only (THEORY.md 10471; README.md 1468; advisory). Frozen-record INFO hits 24; wording FAILs 0.
- `python3 -m pytest tools/ -q`: **125 passed** in 102 s.

The first review committed at `reviews/wf_2026-11-20/REVIEW.md` is byte-identical to `/workspace/review-archive/rev121_REVIEW.md` (SHA-256 `f41756a1737497b79a550dbb50133bd6821f111a24f48cbd3c450e9fdddbe631`, 117 lines).

No GitHub Actions check runs were reported on `4253fce`. The pull request was `mergeable_state: clean` at the start of this confirm.

---

## Residuals (do not block)

- **S4** remains documented only, as the first review allowed. The looser consistency fallback in locked `wf_rule.py` is unchanged. It was not used on any of the 64+3 official worlds.
- `reviews/wf_2026-11-20/REVIEW.md` names `/workspace/gtao-rev121`, `/workspace/gtao-wf`, `/workspace/review-archive`, and `/workspace/looper` (as “not touched”), because that is the review text. It must stay unedited to remain byte-identical.
- D2’s S1 paragraph mentions `/workspace/gtao-wf/…` and `/home/box/…` only as a description of the paths that were removed. That is documentation of the fix, not a live hardcoded path.
- Mentions inside hash-locked `PREREG.md`, `MATH.md`, and `wf_rule.py` remain, as historical locked text.
- T26’s “tracked as T27” pointer has no separate T27 row on this page. The work is described in the T26 row itself; `check_open_work.py` still passes. Not a gate issue.

No new “law” beyond the standing hypothesis sentence. No “theory of everything.” Nothing in these files is called PROVED. No Looper content.

This report: `/workspace/review-archive/rev121_CONFIRM.md`.
