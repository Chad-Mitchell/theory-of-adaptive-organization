# Independent hostile review: PR #128 (GRID-CROSS preregistration)

**Reviewer:** independent (wrote none of the PR, PREREG.md, LOCK.txt, runner, library, reachability log, RESULTS, OPEN_WORK edits, or `tools/test_grid_cross.py`).
**Date:** Saturday 21 November 2026, started 1:59 AM ET, finished 2:12 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/128
**Clone:** fresh `/tmp/rev128/repo` at head `ca2fdf51523ceeffba5349522f169ce9b35bcecd`, base `54a45629280edc9dfe0275d04eaf19626aa4523d` (merge-base equals `origin/main`). Clean tree at review start. Nothing pushed or merged. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19. Author workdir `/workspace/gtao-grid-cross/theory/measured/grid_cross_2026-11-21/` was read only as corroboration of timestamps and hashes; every packaged file compared there is byte-identical to this head (the only extra is a pre-lock `__pycache__`).

**Verdict: READY-WITH-FIXES**

The lock is intact and is before any official selection-pressure score or non-GB distance. Official comparison was correctly not run: this review also did not find no-account public pre-control imbalance or DV-GB1.2-style reconstruction data sufficient for n ≥ 5 complete (S, d1) pairs. P25 is not re-scored. CORE.md and the law-of-adaptive-organization sentence are unchanged. The d1 rule is consistent with the existing GB analysis (GRID-DX B1 / C.4, DV-GB1.2). Qualification vs "not an applicable test" vs gradient-diagnostic split is coherent with FRAMEWORK §9, with two internal tensions that do not affect today's UNTESTED result (S2, S3). Checkers pass. `pytest tools/` is 142 passed with the two Lean tests excluded here to avoid filling the disk; `test_lean_sources_have_no_sorry` passed; the author's pre-lock run recorded no failures and claimed 144, which matches 142 + 2 Lean tests. The branch is a clean fast-forward onto main `54a4562`.

The issues below do not unlock the prereg, do not invent an official score, and do not justify running the comparison from closed-loop frequency. Locked files should not be silently rewritten. S1 is a typo in an informational table (a dated typo-correction / deviation as the prereg already allows). S2–S3 should be resolved in a dated DEVIATIONS note before any Pass 2 scoring, with PREREG text treated as governing until then. S5–S6 belong in the unlocked RESULTS / reachability log.

---

## What was checked

- Fresh clone at the stated head/base; diff `54a4562..ca2fdf5` (one commit, 8 files, +1082 / −1). Package `theory/measured/grid_cross_2026-11-21/` plus `OPEN_WORK.md` and `tools/test_grid_cross.py`.
- Mergeability against `origin/main` `54a4562`: merge-base equals main; `git merge-tree` reported no conflicts; `git merge --no-commit` of main into the head was already up to date (fast-forward). The merge was aborted; nothing was committed or pushed.
- SHA-256 and byte counts of `PREREG.md`, `run_grid_cross.py`, and `grid_cross_lib.py` against `LOCK.txt`, a re-hash on disk, and `run_grid_cross.py lock-check`. Author-workdir birth/mtimes used only as corroboration of lock order.
- Independent exact enumeration of the no-tie Spearman reference table and of the minimum detectable ρ at n = 5, 6, 8 (and n = 9, to check the table). Monte Carlo power under a Gaussian latent-rank model (5,000 draws) for the locked gates (ρ ≤ −0.5 and exact one-sided p ≤ 0.10).
- GRID-DX `PREREG_GRIDDX.md` / `RESULTS_GRIDDX.md` / `SELECTION_SCORES.md` / `DATA_SOURCES.md` compared to the locked d1 / K_obs / BINDING-RUIN rule. FRAMEWORK §9 and the "NOT A TEST" convention in `measurement/FRAMEWORK.md`.
- Reachability: independent HEAD/GET (no accounts, no forms, no API keys; large files not downloaded) of the claimed URLs, plus a search for missed no-account pre-control imbalance or reconstruction sources (NEMWEB, Fingrid dataset 397, ERCOT EMIL / GetReports, guessed AEMO annual frequency paths). Author probe artifacts in `/tmp/grid-cross-survey/` (written 1:46–1:47 AM EST, before lock) were read only.
- Wording: CORE.md, the hypothesis sentence, P25 / GRID-DX numbers, "law" in status labels, overclaim.
- `python3 tools/check_open_work.py`; `python3 tools/check_consistency.py`; `python3 -m pytest tools/ -q --ignore=tools/test_lean.py`; `test_lean_sources_have_no_sorry`.

---

## 1. Lock integrity

`LOCK.txt` timestamp is Saturday 21 November 2026, 01:55:05 AM EST (America/New_York), beside main `54a4562`. It records that no new official S score and no non-GB distance, layer count, or spectrum has been computed. That matches the tree: there is no `SELECTION_SCORES.md`, no `selection_scores.json`, no distance JSON, and no official verdict output in the package. `RESULTS.md` (unlocked) is dated after the lock and says the official comparison was not run.

Hashes and sizes, recomputed on this clone, match `LOCK.txt` and the runner's `lock-check PASS`:

| File | SHA-256 | Bytes |
|---|---|---|
| `PREREG.md` | `1cd856331b968e369b9b97f8ac675186140b040ae2c14e1792147489a3d4d763` | 28105 |
| `run_grid_cross.py` | `eb4bf7d42e71db961fc73d778547bcd9dde548be6babdf939917c35825d8bd89` | 4795 |
| `grid_cross_lib.py` | `d9086f8a09a91e8bb7133bdd012c3adcc94f7726800f04409439a119279dc9b4` | 12732 |

Author-workdir file order, byte-identical to this head (America/New_York):

- `PREREG.md` birth/mtime 1:52:45 AM EST
- `DATA_SOURCES_REACHABILITY.md` birth/mtime 1:53:17 AM EST (not hash-locked; before lock)
- `grid_cross_lib.py` birth 1:53:54 AM EST, mtime 4 ms later
- `run_grid_cross.py` birth/mtime 1:54:37 AM EST
- `__pycache__` / `.pytest_cache` 1:54:40–1:54:54 AM EST (tests before lock; `lastfailed` is empty)
- `LOCK.txt` birth/mtime 1:55:05 AM EST (matches the recorded stamp)
- `RESULTS.md` birth/mtime 1:55:33 AM EST (after lock, not locked)
- Commit `ca2fdf5` at 1:58:48 AM EST

Locked files were not edited after the lock record. The T27 standing rule is stated in the lock and in the prereg. Reachability checks (HTTP status, type, size) are disclosed as pre-lock and are not official S or d scores. The first saved probe (`/tmp/grid-cross-survey/`, 1:46:16–1:46:51 AM EST) used capped GETs (64 KiB). It pulled 64 KiB of the newly reachable AEMC reliability-settings PDF into a temp file that was deleted; ESORI / FRCR / other large PDFs were not downloaded (bytes = 0 under `--max-filesize`). There is no residual PDF body, no extracted numbers, and no official score file. That is consistent with "not opened for numbers," with the nit that a prefix of the AEMC PDF did transit the machine (see Nits).

A later, unlogged HEAD pass supplied the exact Content-Length values in the reachability log (those sizes match this review's independent HEADs). The second pass is not itself a protocol lapse; it is a thinner audit trail than the first probe's TSV.

---

## 2. Design

### Selection-pressure proxies

The four components (S_mkt, S_pen, S_rel, S_own), the 1 January 2011–21 November 2026 window, the {0,1,2} scoring, the MISSING / lower-bound rule, and the ban on scoring from how close products already look to an optimum are written in the locked prereg before any new official S is recorded. They are not a copy of the GRID-DX S_σ / S_N / S_red / S_ruin rubric, and old Pass 1 numbers are not carried forward. S_mkt is written so that the GRID-DX S_N ambiguity (score 0 vs legally required competitive procurement) cannot recur. Double-counting a single incentive scheme in both S_pen and S_own is forbidden. Sources are restricted to official URLs fetched without an account.

These are defensible *operational* proxies of institutional pressure on a grid operator. They are not FRAMEWORK §9 qualification: the prereg says so, and it forbids inferring σ from S. Two design limits, not defects of a priori locking: almost no listed system will reach S_mkt = 2 (N_e ≥ 10 competing design-setting authorities), so variation may be thin; equal 0–2 weights are a convention, not a measured elasticity.

### d1 consistency with GB / GRID-DX / DV-GB1.2

The counting rule for K_obs (group by official full-delivery time; DC and DM as one layer; mandatory droop treated consistently with GRID-2) is the GRID-2 rule. For a pre-control spectrum that is a power law with γ ∈ [1.7, 2.3] or a single first-order mode, K* = 1 under the ruin-slack premise and d1 = max(0, K_obs − 1). GB is taken from the already-recorded fits: K* = 1, K_obs = 4, d1 = 3, under B1, tagged BINDING-RUIN because FRCR DC is sized for an 1,800 MW largest loss. That is exactly RESULTS_GRIDDX B1 / the Part B caveat.

Closed-loop frequency, even at 0.1 s or 1 s, is correctly refused as a d1 input. That is the consistent reading of DV-GB1.2, which reconstructs D(t) from frequency, inertia, delivered response, and balancing-mechanism dispatch. A 15-minute imbalance series is correctly refused when the locked band must include 1 min. An official prose "random walk" claim is correctly not enough.

The only addition to GRID-DX C.4 is the branch for a measured pre-control spectrum that is *not* of that form: K* is then the GRID-2 separated-mode count, and d1 = max(0, K_obs − K*). GRID-DX was silent on that case. It does not change the GB number and is a compatible extension, not a re-score.

### Minimum detectable ρ, and power at small n

Independent exact enumeration of mid-rank Spearman on distinct ranks 1…n, one-sided p = (# permutations with ρ ≤ ρ_obs) / n!, confirms the locked no-tie table for n = 5–8 and finds an error at n = 9 (S1):

| n | Max ρ with exact one-sided p ≤ 0.10 (no ties) | exact p | Next attainable ρ (p > 0.10) |
|---|---|---|---|
| 5 | −0.800000 | 0.066667 (8/120) | −0.700000 (14/120 = 0.116667) |
| 6 | −0.657143 | 0.087500 (63/720) | −0.600000 (87/720 = 0.120833) |
| 7 | −0.571429 | 0.100000 (504/5040) | −0.535714 (594/5040 = 0.117857) |
| 8 | −0.523810 | 0.098313 (3964/40320) | −0.500000 (4358/40320 = 0.108085) |
| 9 | **−0.483333** (not the locked −0.466667) | 0.096900 (35163/362880) | −0.466667 (38560/362880 = 0.106261) |

Those n = 5, 6, 8 values *are* the minimum detectable no-tie ρ at α = 0.10. At n = 5 the p-bar is already far stricter than ρ ≤ −0.5; at n = 8 it is just stricter than −0.5 (a no-tie ρ of exactly −0.5 has p = 0.108 > 0.10). The official gate remains the permutation test on the observed, possibly tied, values; the table is informational, as the prereg says.

Power of the *official* gates (ρ ≤ −0.5 and p ≤ 0.10), 5,000 Gaussian latent-rank draws, distinct ranks:

| n | true ρ = −0.5, P(PASS) | true ρ = −0.8, P(PASS) | true ρ = 0, P(PASS) |
|---|---|---|---|
| 5 | 0.231 | 0.507 | 0.064 |
| 6 | 0.337 | 0.697 | 0.086 |
| 8 | 0.466 | 0.864 | 0.089 |

A perfect monotone relationship is always detected (P(PASS) = 1 at true ρ = −1). A true effect equal to the named bar is not: at the locked n_min = 5, a true ρ = −0.5 is more often NEITHER (~76%) than PASS (~23%). That is underpowered, not adequately powered. It is not "hopeless" for a near-perfect rank alignment, and the Type I rate is slightly conservative because of the effect-size floor. Integer S ∈ {0,…,8} and integer d1 with ties would typically reduce power further. The bars should not be relaxed after lock; the power should be stated in RESULTS so a later NEITHER is not misread (S5).

Leave-one-out robustness is vacuous at n = 5: dropping any complete grid leaves n = 4, verdict UNTESTED, and UNTESTED is not treated as a scored-label change, so a 5-point PASS is never flipped to INCONCLUSIVE by LOO (S4).

### Kill criteria and not-applicable split

The split is the right one, and it matches FRAMEWORK §9 and the GRID-DX "NOT A TEST" convention:

- Qualification (all five §2 items, class-specific N_e proxy preregistered, recorded before distances are used in a hypothesis verdict). Fail or not-established ⇒ **NOT A TEST**, not evidence either way. S is not qualification.
- Gradient diagnostic is a separate headline (PASS / FAIL / NEITHER / UNTESTED / NOT APPLICABLE / INCONCLUSIVE), and is not a test of the hypothesis unless the class qualified.
- A robust FAIL on diagnostic kills the *gradient prediction as operationalised here*; it refutes the hypothesis only if the class had already qualified. A robust PASS supports the hypothesis only with qualification plus beating a named rival (FRAMEWORK §9 items 5–6). That is the right reading of item 5. This Spearman test is not the binomial miss-count in FRAMEWORK §9 item 7; the prereg fixes n_min = 5 and α = 0.10 for *this* comparison and does not pretend otherwise.
- Predictions will not be patched; deviations go in a dated file before further official scoring.

Two coherence problems remain, both about robustness wording versus code, and both irrelevant to today's UNTESTED (n = 1) result: the UNTESTED-fill set {0, max} vs min/max (S2), and all-BINDING-RUIN (S3).

---

## 3. Reachability and missed sources

Independent checks (21 November 2026, 2:05–2:08 AM EST, no accounts) confirm the claimed sizes and the main blockers.

Confirmed 200, sizes match the log: AEMC reliability-settings PDF 235,556 bytes; AEMO Q1/Q2/Q3 2026 frequency-monitoring PDFs 3,004,168 / 2,711,586 / 2,666,439; EirGrid DS3 Protocol v4.1 1,042,484 and volume-requirements 487,820; Fingrid `data.fingrid.fi/files/339/2026/2026-09.7z` 65,757,645, no API key; Netztransparenz 2022 1-s frequency zip 48,053,151.

Confirmed blockers:

- **ERCOT Public API / Data Access Portal:** the portal page states that users must accept terms and "register to use the API Explorer by providing their name and email address." Registration-required API use is correctly excluded. The public EMIL catalog at `https://www.ercot.com/mp/data-products` returns 200 without an account; public frequency products found there are weekly/monthly event or performance zips and a real-time dashboard, not a sub-minute pre-control imbalance series. The author's earlier probe of `GetReports.do?reportTypeId=13103` (200) is Hourly Resource Outage Capacity, not a d1 input, and was omitted from the log (nit).
- **AEMO 4-s annual frequency files:** the HTML landing page returns 403 to curl, as claimed. Guessed `/-/media/files/...` CSV/XLSX paths also returned 403 here (the author reported 302 → 404/403). Quarterly monitoring PDFs on the same media path return 200 and are reports, not a verified 4-s series. Even if the annual frequency files were fetched, they would be closed-loop frequency and, under the locked rule, not enough for d1.
- **Fingrid REST API:** the instructions page states that API access "requires registration and the use of an API key," and that the key must be sent as a request header. Correctly excluded. Static 7z frequency archives remain eligible.
- **Elia and TenneT** HTML paths: 403, as claimed. **ENTSO-E Transparency** root is a JS shell (200, small HTML), consistent with the log.

Missed no-account sources that should have been in the log, and what they actually yield (S6):

- **NEMWEB** (`https://www.nemweb.com.au/Reports/Current/`, HTTP 200, no account). `FPPDAILY` and `ARCHIVE/FPPDAILY` list public daily zips (unit-level 4-s FPP / MW files, not a system pre-control imbalance). `Causer_Pays` and `Causer_Pays_Scada` current directories are empty; `ARCHIVE/Causer_Pays` is 404; `ARCHIVE/Causer_Pays_Scada` has no file listing in this pass. The historical Causer Pays 4-s feed (which official AEMO documentation describes as including Area Control Error) is not currently posted as a fetchable archive at these paths. This is a missed *portal*, not a missed ready d1 series.
- **Fingrid dataset 397**, "Calculated imbalance": "the momentary calculated net imbalance (ACE open loop) without activated reserves in Finland," 1-minute, CC BY 4.0, valid from 25 June 2025, page `https://data.fingrid.fi/en/datasets/397` (HTTP 200). This is the closest official open-loop imbalance series found in this review, and it sits on the same portal the author already used for dataset 339. There are no static `/files/397/` archives (404). The REST API requires a key. The `/en/data?datasets=397` route is a JavaScript "Download datasets" UI, which the prereg would treat as form-gated unless a keyless static file is shown. It is also Finland-only, not a Nordic-area series, and a 1-min sampling interval is a tight fit to a band that must include 1 min. It does not, by itself, create n ≥ 5 complete pairs, but it should have been classified in the log.

This review did not find a no-account official open-loop / pre-control imbalance series, or a complete DV-GB1.2-style reconstruction kit, for five of the listed grids. The official "comparison not run / diagnostic UNTESTED" conclusion stands.

EUR-Lex SOGL text returned HTTP 200 from this environment; the author recorded a WAF / 403. That is environment-dependent and is not a d1 source.

---

## 4. No re-score, CORE, overclaim

`git diff main...HEAD` does not touch `CORE.md`, `THEORY.md`, `measurement/CLAIM_MAP_v2.md`, or `theory/measured/grid/`. CORE.md is byte-identical to main (`sha256 aee235cb2a9b7d46a0e82c97825984eb3f5dcb160bdd283c90df552616284a7a`). The hypothesis sentence is unchanged: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." The word "law" is not used as a status label in the new files.

P25 remains UNTESTED as locked. No GRID-DX number is recomputed. RESULTS.md and OPEN_WORK T3/W14 state that plainly. There is no official ρ, no patched correlation, and no claim that the class now qualifies. The headline "UNTESTED" / "NOT A TEST until the §2 record is written" is not an overclaim. T27 is cited as a prior in-model FAIL and is not treated as confirmation.

---

## 5. Checkers, tests, mergeability

- `python3 tools/check_open_work.py`: PASS.
- `python3 tools/check_consistency.py`: PASS (0 FAILs; existing soft length WARNs on THEORY.md / README.md only).
- `pytest tools/ --ignore=tools/test_lean.py`: **142 passed** in 124 s. `tools/test_lean.py::test_lean_sources_have_no_sorry`: passed. `test_lean_build_if_available` was not re-run in this clone: an earlier unfiltered `pytest tools/` started `check_lean.sh` and filled the disk unpacking Mathlib into `/tmp/rev128/repo/formal/lean/.lake` (that cache was then deleted). The author's pre-lock pytest cache has empty `lastfailed`, and the commit message's 144 passed equals 142 + 2 Lean tests. This is an environment limit of the review clone, not a demonstrated test failure.
- Fast-forward mergeable onto main `54a4562`.

The new tests cover lock hashes, the d1 rule, lower-bound completeness, PASS/FAIL/NEITHER smoke cases, and n < 5. They do not actually verify the no-tie table (S1 would have been caught) and the robustness test does not assert a label flip (S7).

---

## Numbered issues

**S1. Locked no-tie table is wrong at n = 9.** PREREG §8 and `NO_TIE_CRIT_RHO[9]` list −0.466667 with p = 0.096900 (35163/362880). That hit count and p-value belong to ρ = −0.483333. The attainable value −0.466667 has p = 0.106261 (38560/362880), which is *above* α = 0.10. n = 5–8 are correct. The table is informational; official p is the permutation test on observed values; the sentence that for n ≥ 9 the effect-size floor ρ ≤ −0.5 is the stricter of the two remains true, because −0.483333 is still weaker than −0.5. Treat this as the typo-that-does-not-change-a-criterion the prereg already contemplates: a dated deviation, not a silent relock.

**S2. PREREG vs library on the UNTESTED-fill robustness sweep.** §8 says "assigning every UNTESTED grid the most extreme d in {0, max observed complete d} in either direction." `robustness_tables` fills with `min(complete_d)` and `max(complete_d)`, and only with a single common fill for all untested grids. If every complete d1 is ≥ 1, the two procedures differ. Official verdicts are not computed in this commit. Do not silently edit the locked library. Record the discrepancy and, before Pass 2, a dated deviation that either conforms the code to the prereg or amends the clause.

**S3. Internal tension on all-BINDING-RUIN.** One paragraph says that if the BINDING-RUIN sensitivity leaves n < 5, that sensitivity is UNTESTED and the official headline follows the main §8 rule (code does this, and does not flip a scored headline when the sensitivity drops below n_min). A later "not applicable, as a gradient diagnostic" sentence says the diagnostic is not applicable if every complete d1 is BINDING-RUIN and dropping them leaves n < 5. Those cannot both be executed as written. Resolve in the same pre-Pass-2 deviation. Today's n = 1 UNTESTED is unaffected.

**S4. Leave-one-out robustness cannot bite at n = n_min = 5.** Dropping one complete grid yields UNTESTED, which is excluded from the scored-label flip set, so a 5-point PASS/FAIL is never INCONCLUSIVE by LOO. Disclose this in unlocked RESULTS. Do not change the locked clause after seeing official ρ.

**S5. The locked test is underpowered for its own effect-size bar at small n.** Minimum detectable no-tie ρ is −0.80 / −0.66 / −0.52 at n = 5, 6, 8. Simulated P(PASS | true ρ = −0.5) is about 0.23, 0.34, and 0.47. State that in RESULTS. Do not relax ρ ≤ −0.5, α, or n_min after lock.

**S6. Reachability log is incomplete, but the "insufficient for n ≥ 5 d1" conclusion is not overturned.** Add NEMWEB, Fingrid dataset 397, and the public ERCOT EMIL catalog to the unlocked reachability file, with the classifications above (no static ACE archive currently posted; 397 has no keyless static file and is Finland-only starting 25 June 2025; EMIL public frequency products are not a sub-minute pre-control series). Do not treat closed-loop frequency or a form-gated / API-key route as a rescue.

**S7. Tests are thinner than the locked gates.** `test_no_tie_critical_values_match_locked_table` does not enumerate the table (it would have failed on S1). `test_robustness_inconclusive_when_leave_one_out_flips` does not assert a flip. Strengthen tests in this PR without touching locked files.

---

## Nits (not blocking)

- The first reachability probe downloaded and discarded a 64 KiB prefix of the AEMC PDF. No evidence it was parsed for numbers.
- Exact Content-Lengths in the log come from an unlogged second HEAD pass. Harmless, thinner trail.
- EUR-Lex SOGL returned 200 here and 403 in the author's environment.
- `is_complete_pair` is unused; `diagnostic_verdict` duplicates the rule.
- OPEN_WORK W14 / T3 updates are accurate and do not stale other rows in a way that failed `check_open_work`.

---

## What would not be a fix

- Editing `PREREG.md`, `run_grid_cross.py`, or `grid_cross_lib.py` after lock without a dated typo/deviation record.
- Treating Fingrid 10 Hz, NESO 1-s, or Netztransparenz 1-s frequency as d1.
- Copying GRID-DX S numbers into this rubric, or patching P25.
- Relaxing ρ ≤ −0.5, α = 0.10, or n_min = 5 because of S5.
- Running official Pass 2, or adding a CLAIM_MAP row, in this merge.

