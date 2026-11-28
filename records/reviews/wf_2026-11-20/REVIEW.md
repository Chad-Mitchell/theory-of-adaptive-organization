# Independent hostile review: PR #121 (WF-HSV water-filling count test, T25)

**Reviewer:** independent (wrote none of the PR, MATH.md, PREREG.md, predictions, run, RESULTS, deviations, OPEN_WORK edits, or the WF-HSV code).
**Date:** Friday 20 November 2026, started 11:34 PM ET, finished 11:45 PM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/121
**Clone:** fresh `/workspace/gtao-rev121/repo` at head `4b3df21155719287ee08c25e093d4e2ba6556b0f`, base `7275c4bc8461e62a38e95e4e4b47b770e6a636fc` (merge-base equals base). Detached HEAD, clean tree. Nothing pushed or merged. `/workspace/looper` was not touched. Compute at nice 19.

**Verdict: READY-WITH-FIXES**

The official gates recompute exactly from the locked predictions and stored designs. The prereg was locked at 9:54:48 PM ET, before official start 9:57:06 PM ET; predictions were written at 9:55:25 PM ET, before any reduced-order \(E_K\). D1 is a genuine pre-start parser fix, not a rule change. Both PRIMARY gates fail as written (Model S 1882/6440 = 29.22%, rhythmic+mixed 87/264 = 32.95%). TAUTOLOGY, SANITY, and HOLE pass. MATH.md’s mapping claims are sound, and the prior-art DOIs check out on Crossref. The confirmation set does not collide with the excluded worlds. T18 is deprioritized, not closed; SIM-1 is labelled a hypothesis. Checkers and `pytest tools/` pass. CORE.md is unchanged. None of the issues below flip a gate or the FAILED verdict. They should be fixed before merge, without touching the locked prereg, MATH, `wf_rule.py`, or the predictions file.

---

## What was checked

- Fresh clone at the stated head/base; diff `7275c4b..4b3df21` (one commit, 16 files). Package `core/keystone_checks/waterfill_2026-11-20/` and the OPEN_WORK.md diff.
- SHA-256 of PREREG.md, MATH.md, `wf_rule.py`, `worlds.py`, and `wf_predictions.json` against LOCK.txt, START.txt, PREDICTIONS.sha256, and hashes embedded in the predictions file. Workdir mtimes at `/workspace/gtao-wf` were used only as corroboration of the lock/start sequence; the workdir files byte-match the committed package.
- Independent regeneration of all 64 worlds from the locked generators; full re-application of `wf_rule.predict` to the stored poles, variances, \(N\), and \(R\); independent SANITY against the closed-form L1 identity; independent rescore of argmin, N60-from-0 / hull identity, convexity, HOLE, and the identity diagnostic from stored \(E_K\) / \(E_C\) (no optimizer rerun).
- Collision check of the 64 confirmation worlds against the 21 rhythm-test worlds, S5 seeds 0..119 (120 worlds), and the 18 T20 holographic worlds, at the prereg tolerance \(10^{-10}\).
- MATH.md §§2–7 and the §6 Crossref table: formulas, the \(\kappa I_{\mathrm{mem}}\) vs \(hK\) distinction, the innovations-form \(H_2\)/Hankel construction, and DOIs re-queried on the Crossref API this review.
- OPEN_WORK IDs vs base `7275c4b`; `python3 tools/check_open_work.py`; `python3 tools/check_consistency.py`; `python3 -m pytest tools/ -q`.
- Wording: “PROVED,” rescue, CORE claims, private / Looper paths.

---

## Integrity

- PREREG.md SHA-256 `9592042bc2932acec025315c5f34d401ad896a76f16940ee12c43d4be5a7bb05`. Matches LOCK.txt, START.txt, the predictions file, RESULTS.md, and a re-hash of the file on disk. LOCK.txt time is 2026-11-20 21:54:48 EST. The prereg header rounds this to “9:55 PM ET.” MATH.md and `wf_rule.py` hashes also match the lock (`e8ea856a…`, `f9960cd4…`).
- Predictions SHA-256 `ba66cef743bec29d0c2292f9b4d25c0596726623d52a05b8d881d3420fe612d1`. Matches PREDICTIONS.sha256, START.txt, `wf_run.json`, RESULTS.md, and a re-hash of the file on disk. Workdir mtime of `wf_predictions.json` is 9:55:25 PM ET. Official start (START.txt and `wf_run.json`) is 9:57:06 PM ET. The run finished 11:17:54 PM ET, 64/64 worlds, `scored: true`.
- The predictions file was written with *post-D1* `worlds.py` (embedded `worlds_sha256 = f56ceaa32f3d2b761796817cf88ac2e83ab4490ec1157bbd95f997ae178aa206`, which is the file on HEAD). LOCK.txt still records the pre-D1 hash `c1e13a3a…`. That is the expected signature of a parser fix between lock and the prediction write, and it is documented as D1.
- D1: `worlds.py` birth 9:51:22 PM ET, lock 9:54:48, modify 9:55:23, predictions 9:55:25, start 9:57:06. The deviations file says “9:56 PM ET,” which is a one-minute rounding of 9:55:23. The change is the exclusion parser’s handling of `[re, im]` pole pairs in `rhythm_rule.json`. Generators, seeds, grids, inclusion thresholds, and PREREG.md are unchanged. All 64 worlds have `bumps=0` and regenerate identically from the locked formulas, so the parser fix did not redraw any world. This is a genuine pre-start, pre-\(E_K\) deviation, not a rule change. The pre-D1 `worlds.py` bytes are not in the repo (only the lock hash); that is acceptable given the above.
- `wf_rule.py` does not import or call a reduced-order \(E_K\) routine. A static read and a full re-application agree with the predictions file on every cell (0 mismatches), including INDETERMINATE. No world is INDETERMINATE. The H2-consistency fallback in `predict` (looser than MATH.md §7 item 5) was not exercised; every world meets the locked tolerance against \(\mathrm{Var}(s)-E_\infty^{\mathrm{ARE}}\).

---

## Official gates (recomputed from stored data)

| Gate | Criterion | Independent result | Verdict |
|---|---|---|---|
| TAUTOLOGY | §3 items 1–4; item 5 not triggered | Predictions written before start; 0/64 re-apply mismatches; `wf_rule.py` has no reduced-order \(E_K\); \(\sum\gamma_i\) meets the locked tolerance on all determinate cells. Identity diagnostic not triggered: 0/40 Model S worlds have \(K^*_{\mathrm{WF}}=\) N60-from-0 at every \(R\); 0/40 have \(\delta_i\) equal to the joint decrements to \(10^{-8}\). Max relative discrepancy \(2.0659\times 10^{7}\), median \(1.4035\times 10^{4}\), min \(19.854\) | **PASS** |
| SANITY | 9 one-OU cells match L1; both \(K^*=0\) and \(1\) occur | 9/9 (recomputed against \(P=N(\sqrt{a^2+2av/N}-a)\)). Both values occur (`sane_B` is the hole) | **PASS** |
| PRIMARY Model S | \(\ge 95\%\) of determinate cells | **1882/6440 = 29.22%** (0 INDETERMINATE of 6440) | **FAIL** |
| PRIMARY rhythmic+mixed | \(\ge 90\%\) of determinate cells | **87/264 = 32.95%** (rhythm 47/132, mixed 40/132; 0 INDETERMINATE of 264) | **FAIL** |
| HOLE | \(\ge 95\%\) of Model S cells with true argmin \(0\) predicted \(0\) | **70/70 = 100%** | **PASS** |

N60-from-0 / lower-hull increment agrees with argmin in **6440/6440** Model S cells. All 40 Model S worlds are convex on \(K=0..J\) at \(10^{-4}\). No ties, no \(E_\infty\) floor flags, no non-empty `flags`.

Failure-mode counts in RESULTS.md recompute exactly: Model S 4527 over, 31 under (all predicted \(0\) against argmin \(1\)); pair counts (4,3) 965, (2,1) 925, (3,1) 837, (3,2) 749, (4,2) 643, (4,1) 408; per-world best 66.46%, median 27.02%, worst 0%, no perfect world. The `ms_0000` \(\delta\) / joint-decrement example matches. Rhythmic+mixed: 117 over, 60 under; 1/11 on four rhythm worlds and 9/11 on two one-oscillator worlds (`rh_0000`, `rh_0003`); `mx_0006`, `mx_0007`, `mx_0011` are 0/11, all by over-inclusion.

No gate was changed after seeing the data. The FAILED verdict stands. No rescue is registered, and none should be.

---

## MATH.md mapping and prior art

- **\(\kappa I_{\mathrm{mem}}+w D\).** Reverse water-filling is the right allocation for a linear price on nats. The Kolmogorov–Berger parametric formulae in §2 are the standard two-sided MSE formulae. The Lagrangian match to \(\kappa I_{\mathrm{mem}}\) is already in the theory (P3; INTERNAL_MODEL water level \(\theta=\kappa/(2\ln 2\cdot w)\)). The causal caveat in §3.3 is correctly drawn (Yovits–Jackson / Kalman–Bucy is not \(\min(\theta,S)\); sequential RD is a different object). This claim is mathematically sound and is not overstated as new.
- **Frequency-axis peaks of \(S(\omega)\).** A sum of Lorentzians all peaked at \(\omega=0\) has \(\{S>\theta\}\) a single interval. That is a real break with “count the bumps,” already in Model S. Correct, and not the rule under test.
- **WF-HSV as an \(H_2\)/Hankel split of the unique Kalman–Bucy estimate.** The innovations realisation \(d\hat x=A\hat x\,dt+K_g\,d\nu\), Gramians on \(A\) (not \(A_f\)), square-root balancing, and per-state energies \(\gamma_i=C_{\mathrm{bal},i}^2\sigma_i\) with \(\sum\gamma_i=\mathrm{Var}(s)-E_\infty\) are a well-defined construction, implemented as written. Using \(A_f\) would break the one-OU identity, as the note says. The one-OU reduction recovers N60-from-0 / L1 exactly (SANITY). The step from those \(\gamma_i\) to a *predictive* count \(K^*_{\mathrm{WF}}=\#\{i:R\delta_i>1\}\) is a hypothesis, not a theorem; §4.4’s phrase “the derived rule” is a bit strong, but the same section and the short answer already say it is not an identity for \(J>1\) and not a theorem. The confirmation correctly kills it.
- **Prior art, Crossref (this review, 20 Nov 2026).** Every DOI in MATH.md §6 resolved and matches the stated work: Kolmogorov 1956 `10.1109/TIT.1956.1056823`; Sims 2003 `10.1016/S0304-3932(03)00029-1`; Maćkowiak & Wiederholt 2009 `10.1257/aer.99.3.769`; Tatikonda & Mitter 2004 `10.1109/TAC.2004.831187`; Tanaka, Kim, Parrilo & Mitter 2017 `10.1109/TAC.2016.2601148`; Kalman & Bucy 1961 `10.1115/1.3658902`; Moore 1981 `10.1109/TAC.1981.1102568`; Glover 1984 `10.1080/00207178408933239`; Desai & Pal 1984 `10.1109/TAC.1984.1103438`; Francis & Wonham 1976 `10.1016/0005-1098(76)90006-6`. Roles are apt (Francis & Wonham is correctly marked as not a counting rule). Berger 1971, Shannon 1959, and Yovits & Jackson 1955 are honestly listed as having no Crossref DOI; Berger is confirmed as the 1971 Prentice-Hall book via contemporary reviews on Crossref. The novelty paragraph is appropriately modest.

MATH.md §8 still says WF-HSV is “Open.” That is correct: the file is hash-locked and must not be edited after the run. The fail lives in RESULTS.md and OPEN_WORK.

---

## Excluded worlds

The 64 confirmation ids are only `ms_0000`–`ms_0039`, `rh_0000`–`rh_0011`, `mx_0000`–`mx_0011`. No id overlap with the 21 rhythm-test worlds, `seed2_two_light`, or the 18 T20 ids listed in the prereg. Independent parameter collision checks at relative \(10^{-10}\) against those 21 worlds, the 120 S5 worlds (seeds 0..119), and the 18 T20 worlds: **zero collisions**. The confirmation set is clean. The *machinery* that was supposed to enforce this is incomplete; see S2.

---

## OPEN_WORK

No table IDs present on base `7275c4b` are missing on this head (57 → 60). Added: W12, T25, SIM-1. `process/queue/items.json` and `process/QUEUE.md` are not in the diff. Open-work checker PASS: union of not-DONE items.json / QUEUE.md missing from OPEN_WORK.md = 0.

- **T18** remains **OPEN**, marked **deprioritized**, and the gate is now `parked` (restarts only if a genuinely new predictive candidate is written). It is not closed or DROPPED. Accurate.
- **T25** is **DONE. FAILED** (in-model, numerical), with the official counts, “no rescue,” and review owed as W12. Accurate.
- **SIM-1** is labelled **“Hypothesis, not a result,”** explicitly not a new term in \(J\) and not a change to CORE.md. Accurate.
- W9 and T19 are updated to match (T19 unparked because it no longer waits on a closed-form rhythm count). The header’s `main` SHA `7275c4b` and the “125 tests” tally are correct. CLAIM_MAP is untouched (still 318 rows).

---

## Issues

**S1. Newly authored, non-locked files still contain box-private paths.** `worlds.py` hardcodes `REPO = Path("/workspace/gtao-wf/repo")`, so a public clone will not load `rhythm_rule.json` for the exclusion check. `run_wf.py` writes `/workspace/gtao-wf` into its RESULTS template. `run_wf.log` contains `/workspace/gtao-wf/` and `/home/box/.local/...`. No `/workspace/looper`, and no personal information. Hash-locked files (PREREG.md, MATH.md, `wf_rule.py`, and the predictions-hashed `worlds.py` source as run) may keep the paths they already have; do not rewrite them. For `worlds.py`, switch the repo root to a path relative to the file (or to the clone root), and record a short post-results hygiene deviation. Do not rewrite `wf_predictions.json`, PREREG.md, MATH.md, or `wf_rule.py`. Redact or rewrite the log / RESULTS template similarly.

**S2. The locked exclusion check was not implemented as the prereg wrote it.** `PREREG.md` §4 says a draw within relative \(10^{-10}\) of any excluded world’s \((a,v,N)\) is discarded and redrawn. `_load_excluded` only reads `rhythm_rule.json`. Model S worlds never call `_too_close`. S5 seeds 0..119 and the T20 18 are not loaded. This is a procedure miss, not a contaminated set: this review found zero collisions, and all worlds have `bumps=0`. Disclose the gap in the deviations file, and fix the loader for any later use. Do not rescore and do not treat the fix as a new result.

**S3. RESULTS.md under-reports the Lyapunov `RuntimeWarning`s.** The writeup says two warnings appeared early in the rhythm phase. The committed log has those two and a third, later, in the mixed phase (just before `mx_0006` completed). No world is flagged, no \(E\) is below the floor, and this is not a gate change. Add the third warning to “Suspicious points.”

**S4. `wf_rule.predict` has a consistency fallback that is looser than the locked MATH.md §7 item 5** (alternative target \(C W_c C^\top\), and a \(10\times\) tolerance). It was not used on any of the 64+3 worlds, so no status would change. Tighten the code to the locked test, or document the fallback as a deviation, without rescoring.

---

## What does not block

- PREREG “9:55 PM ET” vs lock 9:54:48, and D1 “9:56 PM ET” vs mtime 9:55:23, are rounding, not a sequence problem.
- `run_wf.py` `SyntaxWarning`s on invalid escape sequences in the RESULTS writer. Cosmetic; the official RESULTS.md was edited after the auto-draft (23:29 vs 23:17 ET) and the numbers match the rescore.
- MATH.md §4.4 calling WF-HSV “the derived rule.” Qualified in the same note as a hypothesis / not an identity for \(J>1\).
- Deprioritizing T18 and unparking T19 is a judgment about what the law needs, not a claimed theorem. It is labelled as such.
- Convexity in Model S remains numerical, as elsewhere. On this fresh set it holds at \(10^{-4}\) in 40/40, and N60-from-0 is an identity with argmin here; that confirms the solver, not WF-HSV.

---

## Private / Looper / wording

- No “theory of everything.” Nothing marked PROVED. The fail is labelled in-model, numerical. No rescue.
- “Law” appears only as the existing hypothesis / “the law and the equation do not need a closed-form count,” not as a new proved claim.
- No Looper data, no `/workspace/looper` tree access, no personal information. Path mentions in non-locked files: S1. Mentions inside hash-locked PREREG.md / MATH.md / `wf_rule.py` stay, as historical locked text.
- CORE.md, CLAIM_MAP, STATUS.md, and README.md are not in the diff.

---

## Required before merge

Apply S1–S3 in the same pass (hygiene deviation for the `worlds.py` path and the exclusion-loader gap; name the third Lyapunov warning). Do not touch PREREG.md, MATH.md, `wf_rule.py`, `wf_predictions.json`, or any official count. S4 can be residual if time is tight; it does not affect stored statuses.

No push or merge was made from this review. Working clone: `/workspace/gtao-rev121/repo`. This report: `/workspace/review-archive/rev121_REVIEW.md`.
