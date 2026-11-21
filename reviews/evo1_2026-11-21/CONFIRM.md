# Confirm review of EVO1 (draft PR #114, head ed6bf7c)

*21 Nov 2026 (ET). Independent hostile confirm of head `ed6bf7c8646466e918ec64665a22f29bafc42893`. The first review (`REVIEW.md`, head `6f95897`, READY-WITH-FIXES) was not treated as authority. Verdicts below were re-derived from `tests/EVO1/runs/*.json`, the locked `analyze_evo.py`, and PREREG §5–§7, and only then compared with `RESULTS_EVO.md`, `ANALYSIS_EVO.json`, and the fix commit. Nothing here was committed, pushed, or merged. No locked prereg file and no verdict was edited.*

**Verdict: READY-WITH-FIXES. No blockers.** All eight world verdicts and all secondaries reproduce. No verdict moves. Six of the seven claimed write-up fixes are applied and match the locked numbers. One is only partial.

## Blockers

None.

## Should-fix

1. **W4b's valley is still stated as shown in two places the fix commit touched or was told to fix.** D1b's pre-set bar was ≥ 3/4. The runs are 2/4 (seeds 0 and 1 reached 1L1S inside the band; seeds 2 and 3 stayed 1L0S). CORE.md, the OPEN_WORK W2 cell, RESULTS, and CLAIM_MAP row Q6 already say the bar was missed. These two do not:
   - `OPEN_WORK.md` W10: "W4/W4b FAILED by fitness valleys (diagnosis D1–D2): selection found argmin J only where small steps reach it." The corrected W2 cell points at W10, so the pointer restores the overclaim. W10 was not in the `6f95897..ed6bf7c` diff.
   - `measurement/CLAIM_MAP_v2.md` v2.69 note (a paragraph this commit did edit): "The two FAILs are diagnosed (D1/D2, declared before running) as fitness valleys." Q5 and Q6, immediately below, are the accurate sentences. The same note still says "D1–D4" and does not mention D5.

   Suggested alignment, not a new claim: W4's creation valley met the D2b bar (4/4). W4b's D1b bar was not met (2/4); D1a shows the minimum is selection-stable once reached (4/4).

## Checkout and the fix commit

- HEAD is `ed6bf7c8646466e918ec64665a22f29bafc42893`. Its only parent is `6f95897260f299e65d22fda2a951b4bc6a7a6544`.
- `git diff --name-status 6f95897..ed6bf7c` is seven files, all write-up or review record: `CORE.md`, `OPEN_WORK.md`, `measurement/CLAIM_MAP_v2.md`, `reference/CHANGELOG.md`, `reviews/evo1_2026-11-21/REVIEW.md` (added), `tests/EVO1/DEVIATIONS_EVO.md`, `tests/EVO1/RESULTS_EVO.md`.
- No locked scorer, prediction, simulator, world file, run file, or log is in that diff. The hypothesis sentence is unchanged in `THEORY.md` and in `PREREG_EVO.md` §1: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."

## Re-derived verdicts

Rules used, from the locked scorer and PREREG §6–§7, not from the write-up. EPS_BAND = 10/(βP) with β = 30 and P = 300, so 1/900 = 0.001111…. A seed misses if J/J* − 1 > EPS_BAND (A) or the scored structure differs from the prediction (B; genome structure for W4b). A seed still improving at the end is unscored: mean of `med_cost` in generations 480–539 exceeds the mean in 540–599 by more than max(3 SE, EPS_BAND·J*). World: PASSED if scored misses ≤ 1, INCONCLUSIVE if 2, FAILED if ≥ 3. INVALID if fewer than 6 converged seeds, if ≥ 2/4 null seeds meet both criteria, if the nearest named rival has βP·gap < 10, if the mean final-window death fraction exceeds 10%, or if PC is not PASSED. Death fractions and the improving flag were recomputed from the raw logs and match `ANALYSIS_EVO.json` on every seed. A window-median version of the improving rule flips no seed.

| World | Re-derived | Misses | What the runs show | Agrees with RESULTS and ANALYSIS |
|---|---|---|---|---|
| PC | **PASSED** | 0/8 | b 0.03939–0.04047; max J gap 4.99e-5; null 0/4; nearest sNe 3000 | yes |
| W1 | **PASSED** | 0/8 | b 0.03274–0.03429 vs predicted 0.03356; null 0/4; sNe 2448 | yes |
| W2 | **PASSED** | 1/7 scored | seed 4 is the scored miss (1L0S, gap 3.44%); seed 2 still improving, unscored, gap 1.549e-3, slow-pole Δ ln b = 0.305 > band 0.225; null 0/4 | yes |
| W3 | **INVALID** (ruin); raw **PASSED** | 0/8 | final-window deaths 10.62–15.24%, mean 13.03% > 10%; null 0/4; sNe 3686 | yes |
| W4 | **FAILED** | 3/8 | seeds 0, 4, 6 (low starts) stayed 1L0S, gaps 8.122–8.127%; seeds 1, 2, 3, 5, 7 reached 1L1S; null 0/4; sNe 612 | yes |
| W4b | **FAILED** | 8/8 | all seeds 1L0S, gaps 1.042–1.056% (the no-sharing rival is 1.044%, sNe 93.8); null 0/4 | yes |
| S031 | **INCONCLUSIVE** | 2/8, A only | seeds 1 and 2, gaps 1.235e-3 and 1.289e-3; structure 8/8; not improving; deaths 0; null 0/4; sNe 40.4 | yes |
| S07 | **INCONCLUSIVE** | 2/8, A only | seeds 1 and 2, gaps 1.128e-3 and 1.211e-3; structure 8/8; null 0/4; sNe 175.1 | yes |

PC is PASSED and not invalid, so no other world is INVALID on the positive-control ground. Every nearest-rival gate is ≥ 10. W3's only invalid reason is the ruin gate.

**Secondaries** (same numbers in the rerun, in `ANALYSIS_EVO.json`, and in RESULTS):

| Test | Re-derived | Verdict |
|---|---|---|
| PC→W1 | Δ ln b observed −0.17720 vs predicted −0.17552, tolerance 0.1003, n = 8 and 8 | **PASSED** |
| S031→S07 | observed +1.47024 vs predicted +1.37593, tolerance 0.3110, n = 8 and 8 | **PASSED** |
| Store-noise threshold | S031 slower than its mode in 8/8 (λ/b from 1.50 to 1.77); S07 faster in 8/8 (λ/b from 0.357 to 0.419) | **PASSED** |
| W2 interlacing | seeds 0, 1, 2, 3, 5, 6, 7 interlace, including still-improving seed 2; seed 4 has one rate and does not | **PASSED** under §6 (≥ 7 of 8) |
| Rate band | every converged seed with the predicted structure is inside it; the only seed outside is W2 seed 2 | as RESULTS states |

The locked scorer's stored `W2_interlacing` field is agree 7, n 7, PASSED. It omits miss-B seeds, and seed 4 is miss B, so the field never scores seed 4. §6's denominator is 8. Counting seed 4 as not interlacing is 7 of 8, which also PASSES (one failure is allowed). The prose now follows §6. The JSON field was not rewritten, correctly. On this data the two denominators cannot disagree about the verdict. They could on another outcome, because three structure misses would be FAILED under §6 (≥ 3 do not interlace) and might still be PASSED by the code if the remaining seeds interlace. That is a locked-code mismatch to leave for a successor prereg, not an edit here.

**S-arm margins**, (gap/EPS_BAND − 1): S07 seed 1 is 1.52% over, S07 seed 2 is 8.97% over, S031 seed 1 is 11.18% over, S031 seed 2 is 16.02% over. The table of gap/band in RESULTS rounds correctly (S031 0.66, 1.11, 1.16, 0.66, 0.85, 0.75, 0.74, 0.64; S07 0.92, 1.02, 1.09, 0.96, 0.87, 0.83, 0.77, 0.90). Medians of gap/band are 0.746 and 0.909, which is the stated 0.75–0.91. Correlation of gap with (Δ ln b)² is 0.787 (S031) and 0.058 (S07). Median rate offset is −10.8% (S031) and −1.4% (S07). Null gaps are 30.4–122.2% on PC and 1.36–9.31% on the S arms.

**Diagnostics.** D1's bars are in `cf77048` (20 Nov 2026, 13:51:47 ET) and D2's bar is in `610e87a` (14:18:46 ET). Diagnostic outputs and `DIAG_SCORES.json` first appear in `b5d1805` (15:44:09 ET). `diag_evo.py` was not changed after `610e87a`. The four copied `diag/*/evo.py` files hash-match the locked `evo.py`. D1c's worlds file has the W3 buffer ×10 (1500 → 15000). The ≥ 3/4 sentences are unchanged from the declaration commits. Rescoring the diagnostic runs with `score_seed`:

| ID | Re-derived | Bar |
|---|---|---|
| D1a | 4/4 stayed 1L1S, max gap 9.77e-5 | met (stable) |
| D1b | seeds 0 and 1 in band; seeds 2 and 3 stayed 1L0S | 2/4, not met |
| D1c | 8/8 in band; deaths 5.62–8.24% | beside the INVALID, under 10% |
| D1c-ruin | consensus death 0 on all 8 seeds; weight-sum error ≥ 0.02 dies 20.74–36.27% | matches 20.7–36.3% |
| D2b | 4/4 reached 1L1S, max gap 4.59e-5 | met |

W4 calibration: the paired realized gap of alt_1L0S against the predicted 1L1S design is 0.0817, which is the stated 8.2%. The final logged median costs are 1.666–1.713 on the 1L1S seeds and 1.772–1.816 on the 1L0S seeds.

## Hash and stores.py

`sha256sum -c tests/EVO1/PREREG_EVO.sha256` at this head: every listed file matches except `theory/layers_checks/stores.py`. Current hash `30d2a4716730e7912e41ab787f7c561571d169e94db25b67f412f4f20401f513`. The locked bytes at `70fcbad` hash to `df6b70393ead3332f5b9cd13b756603ecbcef237162e369a80359ea3f7b84a30`, the value in the lock file. `git diff 70fcbad HEAD` is empty for `analyze_evo.py`, `evo.py`, `predict_evo.py`, `worlds.json`, `PREDICTIONS_EVO.json`, `count_rule.py`, `PREREG_EVO.md`, `calibrate_evo.py`, `CALIBRATION_EVO.json`, `runall.sh`, and `figures/face_hybrid.py`. The stores.py diff is the v2.67 guarded pseudo-inverse (PR #116): `mse_given_b` no longer calls `np.linalg.solve` on the raw matrix.

`analyze_evo.py` was rerun unchanged on the committed `runs/` in two throwaway trees (NumPy 1.26.4, SciPy 1.11.4), one with the `70fcbad` stores.py and one with the current file.

- The two outputs are identical on every field. This stack does **not** reproduce D4's "two null-seed J gaps move by about 7e-11". The guard is not a no-op in general: a synthetic near-duplicate pair, rates 0.02 and 0.0200001 on a near-random-walk OU, moves MSE from 0.031668 (locked solve) to 0.034856 (guarded inverse). None of the 96 run designs produces a J-gap difference between the two files.
- Either rerun against the committed `ANALYSIS_EVO.json`: every boolean, string, verdict, miss count, move, threshold, and interlacing field matches. Numeric drift is elsewhere. The largest is 1.73e-5 on one counted shared pole of W4 null seed 1 (`count_rule.py` / Nelder-Mead, which does not call stores.py). One W3 null J gap, seed 101 (two stores), differs by 4.97e-11; seed 103 (four stores) matches exactly; seeds 100 and 102 are inf either way. No miss flag and no verdict moves. The 4.97e-11 is present for both stores versions, so it is cross-machine solver noise, not the PR #116 diff.
- D4's conclusion holds: swapping stores.py does not move a verdict, and the committed analysis is the decision record. D4's specific 7e-11 figure is a record of another machine. It is not what this rerun measures.

D5 checks out against the locked files. PREREG §5, W3 row "none", says the gap is 0 and "identical to the prediction in this world". `PREDICTIONS_EVO.json` has that rival as `Infinity`. `predict_evo.py` sets `none=float('inf')` and says a random walk with no store has unbounded error. The scorer keeps a rival only when J is finite and above J*, so the cell is skipped. The prereg hash still matches. The file was not edited.

## The seven claimed fixes

| # | Claim | Applied | Evidence |
|---|---|---|---|
| 1 | Band label is 10/(βP) = 1/900, not 1/(βP) | **Yes** | RESULTS lines 12 and 152. Locked code `EPS_BAND = 10/(βP)`. No remaining `1/(βP)` in the results write-up. The number used before the fix was already 0.00111. |
| 2 | Miss margins are 1.5–16% over the band, in RESULTS, the v2.69 note, and the OPEN_WORK EVO1 cell | **Yes** | All three say 1.5–16%. Endpoints match: S07 seed 1 is 1.52% over, S031 seed 2 is 16.02% over. The middle misses (8.97% and 11.18%) sit inside the range. "4–16%" survives only as a quotation in `REVIEW.md`. |
| 3 | D4's S031 seed-2 log account | **Yes** | `evo.py` prints when `g % 50 == 0 or g == G − 1`, so a finished log contains g599. `logs/S031_2.log` and `logs_recovered/S031_2.log` end at g550. `runs/S031_s2.json` has G = 600, 600 rows, last g = 599, a consensus block, and `secs` = 8492.2. The scorer reads the run file. The other recovered logs that end at g550 are exactly the list in D4 (S031_4, S031_5, S031_6, S031_101–103, S07_2 through S07_6, S07_100–103). Every other file in `logs/` reaches g599. |
| 4 | D1c-ruin mutant deaths are 20.7–36.3% | **Yes** | `diag/D1c_ruin.json`, field `death_rate_weight_sum_error_ge_0p02`: minimum 0.20736 (seed 5), maximum 0.36274 (seed 2). Consensus death rate is 0 on all 8 seeds. |
| 5 | W2 interlacing is 7 of 8, seed 2 unscored and outside the band, seed 4 does not interlace | **Yes** | RESULTS, D4, and CLAIM_MAP Q3 and Q9. Seed 2: improving, gap 1.549e-3, slow pole 0.305 > 0.225, and it does interlace (0.0005 < 0.00558 < 0.02 < 0.0420). Seed 4: one store. See the denominator note above. |
| 6 | CORE and OPEN_WORK no longer state W4b's valley as shown; CORE header is v2.69 | **No** (partial) | CORE header says CLAIM_MAP v2.69, tally 327. CORE's EVO1 bullet says D2b met its bar (4/4) and D1b missed (2/4), and it says "on the proxy". OPEN_WORK's W2 cell says the same and uses 1.5–16%. W10 still states the valley as the finding for both worlds. See the should-fix. |
| 7 | D5 records the PREREG §5 W3 "none" cell (gap 0) against the locked prediction (inf), without editing the prereg | **Yes** | D5 in `DEVIATIONS_EVO.md`. PREREG hash matches. Scoring uses the JSON and skips the non-finite rival. The W3 verdict does not depend on it. |

## Checks

- `python3 tools/check_consistency.py`: PASS. CLAIM_MAP rows counted 327, tally total 327. Wording FAILs 0. `STATUS.md` and `THEORY.md` point at CLAIM_MAP v2.69.
- `python3 tools/check_open_work.py`: PASS. Union of not-DONE ids missing from OPEN_WORK: 0.
- `python3 -m pytest tools -q` on this machine (NumPy 1.26.4, SciPy 1.11.4, sympy 1.14 installed for the run): **6 failed, 140 passed, 1 skipped** (Lean not installed). Five failures are `np.trapezoid`, which NumPy 1.26 does not have and NumPy 2 does (`test_core_checks`, `test_dynamics_checks::test_d5_bode_discrete`, `test_ht_index::test_store_optimizer_never_below_causal_minimum`, `test_meq_derive`, `test_scope_checks`). The sixth is `test_cross_field_map`: `chow_map.py` asserts a mid-level relative error under 1e-3 and gets 2.86e-3. None of these files is in `6f95897..ed6bf7c`. The pytest run rewrote generated result JSON under `theory/dynamics_checks/`, `theory/measured/ecoli/`, and `theory/store_noise/`; those files were restored with `git checkout` and are not part of this review. The first review's "146 passed, 1 skipped" is what this count becomes if those six environment failures pass. This confirm does not treat them as EVO1 failures.

## New errors and nits

No new numerical error in the fix. The band formula, the miss range, the log account, the ruin range, the interlacing count, and D5 match the runs. The nature caveat is still there: RESULTS says an in-silico pass does not show that nature obeys the hypothesis; CORE and OPEN_WORK say "on the proxy"; the v2.69 note says the rows are in-model and show nothing about nature. Qualifiers were added on the EVO1 lines, not dropped.

Nits, not should-fixes:

- D5's clock says "about 11:00 AM ET". The commit that adds it, `ed6bf7c`, is 10:36:24 ET on 21 Nov 2026. The commit is the record the deviations file itself names; the typed clock is about 24 minutes later. D4's "about 10:10 AM" sits next to `6f95897` at 10:12:24 ET, which is fine.
- RESULTS' opening list of record entries still stops at D4 and does not name D5. The v2.69 note does the same.
- `ANALYSIS_EVO.json` stores W2 interlacing as 7/7. The prose correctly says 7 of 8. Both verdicts are PASSED. Do not rewrite the analysis file to force the prose denominator into the locked output.
- The improving rule in the locked scorer compares means of the per-generation median costs. §7 says "median cost". Recomputing the drop with the median of each window flips no seed. Leave the locked code alone.
- `core/KEYSTONE_NOTE.md` and `core/bridge_2026-11-21/SELECTION.md` still name a fitness valley for W4 and W4b without D1b's missed bar. Neither file is in the fix commit. The first review treated them as a reading of this experiment. Same wording class as W10, outside the files that should-fix named.
- RESULTS' "more layers" paragraph says four-store starts collapsed to the predicted count. High starts did reach the prediction in PC, W1, W2, W3, W4, S031, and S07. In W4b the high starts collapsed to 1L0S, not to the predicted 1L1S. The cap rival is still excluded there. Pre-existing, not in the fix diff.
- A fresh `analyze_evo.py` on this SciPy does not bit-match counted poles in the committed analysis (max 1.73e-5, one null seed). Decision fields match. Not a reason to regenerate `ANALYSIS_EVO.json`.

## What was not done

No file in the remote repo was edited. No commit, push, merge, or PR was made. Locked prereg files were only hashed and read. `CONFIRM.md` is local and uncommitted.

The should-fix and nits were applied in the follow-up commit.
