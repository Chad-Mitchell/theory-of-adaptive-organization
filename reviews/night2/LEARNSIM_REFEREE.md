# Hostile independent referee report: LEARNSIM (night 2)

Referee: an independent referee subagent, claimed 15 November 2026, writing finished 09:16 AM ET (America/New_York). Private working file; nothing posted or sent. The repository `Chad-Mitchell/theory-of-adaptive-organization` remains private.

Procedure: I did not trust `RESULTS.md`. I checked lock integrity from git commit times against filesystem birth/mtimes and sha256 blobs; grepped the simulator for theory imports; reran the locked analysis scripts (`analyze.py`, `analyze2.py`, `postlock_fixes.py`) from the raw jsonl; reran four onset jobs with `nice -n 19` against the locked RNG; and ran my own forking-path checks (`reviews/night2/LEARNSIM_REFEREE_checks/`). Wording follows THEORY.md: this is a theory, never a law; all labels below are in-model (SIM-PASS / SIM-FAIL / INCONCLUSIVE), regime A only.

## 0. Bottom line

| Claim | Authors' headline | Referee verdict |
|---|---|---|
| Locks precede onset outputs | All three locks before any onset output | **CONFIRMED**, with one residual, unprovable gap: `results_es.jsonl` was *created* at 08:21:02 ET, six minutes before the PREREG_2 lock (08:27:34). The successful run's log says `jobs to run 736` (a complete fresh set). I cannot independently prove the file was empty rather than truncated at relaunch. See §1. |
| Simulator never imports theory predictions | Non-circular in the night-1 sense | **CONFIRMED.** `world.py` and `run_*.py` do not import `theory.py`. Costs are realized money + realized squared error. Trackers learn from episode payoffs. Averaging gains are tuned on the tracker's own innovations. The remaining, disclosed, circularity is the usual one: a good cost-minimiser approaches the world's true optimum. Grid centres are theory N\* (declared; used only to place a ×/÷16 window). |
| ES onset exponents, PREREG rule (≥ 4 valid ρ, ≥ 1 decade) | INCONCLUSIVE in all 5 arms | **CONFIRMED.** Reproduced exactly. Valid set is ρ ∈ {0.04, 0.08, 0.16, 0.32} (0.9 decade) except RA primary, which is only {0.08, 0.16, 0.32}. Point estimates match the write-up. |
| C1: "the exponent does not depend on sensing technology" | Rival KILLED (CI upper bound −0.60 < −0.4) | **CONFIRMED as a locked-rule application; DOWNGRADED as a substantive kill.** The pre-specified contrast fires on the valid set {0.04…0.32}. It does **not** fire if ρ = 0.04 is dropped (CI upper bound +0.76), nor on {0.16, 0.32}. RR's fitted N\* is not monotone in ρ (55, 107, 29, 15). The headline "rival killed" should not be repeated without that caveat. In-model, regime A only. |
| PREREG_2 T1.8 ("the level's class sets e_g") | NOT PASSED (RA PASS + rival killed; AR INCONCLUSIVE on MV8) | **CONFIRMED.** Official `ANALYSIS_2.json` reproduces byte-for-byte. T1.8 requires both mixed arms to PASS and the members'-class rival to be killed in both. AR's bootstrap SE 0.371 exceeds the locked MV8 gate 0.35, so the arm is INCONCLUSIVE under the text that was locked. Without that gate AR would have been a PASS; the gate was pre-specified and must stand. |
| PREREG_2 RA mixed-arm: measured level class predicts ê; members'-class rival killed | PASS (−0.736 [−1.03, −0.52] vs −0.759; rival −1.650 killed) | **CONFIRMED.** Not a forking-paths artifact under the checks I ran (leave-one-ρ-out, even/odd and first-8 seeds, no PAVA, no common random numbers, logistic N50). Known-groups (MV7) did **not** succeed on RR (INCONCLUSIVE, with the non-monotone N\*), so the instrument is only half-validated; the locked rule flags only a known-groups *MISS*, so no flag was required. **Wording: in-model, regime A, RA arm only. This is not a T1.8 pass.** |
| V at onset (class R, exact formula) | RR PASS (geo-mean ratio 1.01); RRh PASS (1.06); AA INCONCLUSIVE | **CONFIRMED as a locked-rule application.** The geometric-mean ratio stays inside ×/÷1.15 even after dropping the two noisiest ρ. Per-ρ values at ρ = 0.04 and 0.08 for RR are poor (1.42 and 2.73 vs 1.98 and 1.96) and almost swap the two onsets; the mean is helped by cancellation. Per-ρ CIs are wide, as the authors said. In-model, regime A, reset-type sensing only. |
| T3 / T1.7 factorial signs | Two shared×2 PASSes (RRh, RA); everything else INCONCLUSIVE after a disclosed post-lock text-governs fix | **CONFIRMED.** The four locked-code "MISS" labels were bugs (CI included 0; predicted sign negative). The text rule makes them INCONCLUSIVE. No cell has a CI wholly on the wrong side. The mixed-arm (AR, RA) T3 magnitudes are outside the scope THEORY.md now states. |
| Stage-A measured-(a, b) prediction | INCONCLUSIVE under the text rule (span < 1 decade); locked code wrongly said PASS for AA, AR, RA | **CONFIRMED.** The post-lock correction moves those three verdicts toward INCONCLUSIVE; none becomes a new PASS. |
| Pop-learner RR / RRh slopes (secondary; never a verdict) | RR −0.910 [−0.965, −0.851] vs −0.963; RRh −0.982 [−1.043, −0.939] vs −0.970 | **CONFIRMED as numbers; UPHELD as robustness only.** Analysis of the deduplicated file reproduces exactly. The raw file has a torn mid-write (line 97, a fragment of RRh ρ = 0.32 seed 1) and six identical duplicate lines; dedup is honest. This learner is close to an exhaustive realized-cost optimiser, as the authors said. It does not decide a locked verdict and must not be advertised as a non-circular pass. |
| "Killed the members'-technology-sets-exponent rival" | Stated for RA, with T1.8 NOT PASSED as the headline | **CONFIRMED, if and only if qualified as in-model, regime A, RA arm only.** It is incorrect as a general, two-arm, or field claim. See §6. |

No locked number I recomputed was wrong. No proof or pre-lock prediction was silently altered. I do not change any existing `measurement/CLAIM_MAP_v2.md` row status (see §8).

## 1. Lock integrity

### Commits (AuthorDate = CommitDate, America/New_York)

| Commit | Time (ET) | What |
|---|---|---|
| `820b224` | 08:16:31 | PREREG.md, code, estimators, `THEORY_PREDICTIONS.json`, `GRID_CENTERS.json` |
| `41f297c` | 08:16:37 | In-body time "08:17" → "08:16" (text only; sha256 of PREREG.md updated). The diff is one word. |
| `c95f3c6` | 08:20:58 | Stage A `MEASURED_AB.json` + sha256 |
| `c86f8e5` | 08:27:34 | PREREG_2.md, level-class inputs, measured-input predictions, `analyze2.py`, extension runner |
| `2843f5b` | 09:08:56 | Results, post-lock fixes (labelled), raw data |

Every file listed in `PREREG.sha256` (after the time-fix commit) and in `PREREG_2.sha256` hashes to the blob in that lock commit, and those blobs are byte-identical to the working tree and to `<local>/gtao/night2/LEARNSIM/`. `MEASURED_AB.sha256` matches. Analysis code, bootstrap seeds (2026 / 2027) and the PAVA estimator were inside the locks.

### Order versus filesystem times

- Theory predictions and the first N-grid are from 07:56 / 08:12, before the PREREG lock. Good.
- Stage A output mtime 08:16:51, sha256/commit 08:20:58, before any onset *result*. Good.
- `LEVEL_CLASS.json` (08:26:10), `PREDICTIONS_2.json` (08:26:47) and `GRID_CENTERS_2.json` (08:27:03) are inputs to PREREG_2, hashed into the 08:27:34 lock. Their numbers appear in the prereg text, as they should: measure, then lock the prediction, then run onset.
- Onset outputs: `results_es.jsonl` mtime 08:52:53, `results_ext.jsonl` birth 08:52:54 / mtime 08:56:56, analyses 09:00, post-lock script 09:01, pop run 09:00–09:07, `RESULTS.md` 09:08:56 with the results commit. Good.

### The 08:21 launch (the one gap)

`results_es.jsonl` and `logs/onset_es.log` have **birth time 08:21:02 ET**, after the Stage A lock and **before** PREREG_2. The authors disclose a first launch that "died before writing any result (empty file)" and a relaunch after the PREREG_2 lock (`runall.sh` itself was born only at 08:27:39). The successful log starts `jobs to run 736` and the committed file has exactly 736 unique, well-formed jobs and no duplicates. That is what you would see if the file was empty at relaunch (the runner skips already-written jobs).

I cannot prove it was empty rather than truncated. A six-minute 3-worker run at the later speed would have been enough to finish on the order of 100 jobs. The first jobs in the sort are AA, then AR, then RA, so a hidden peek would have been of small-ρ AA, not of the RA mixed-arm result. `analyze.pyc` was compiled at 08:27:08, 26 seconds before the PREREG_2 commit; that is consistent with importing `analyze` from the declared `analyze2.py` smoke-run on synthetic data, and is not evidence of peeking at onset outcomes. **Residual risk: low for the RA result; not zero for PREREG_2's existence as a truly pre-outcome addendum.** Locks are self-attested private commits, as the authors said.

Smoke tests were on out-of-design ρ = 0.5, as declared. `run_onset.pyc` and the numba caches date to 08:13, before the first lock, which matches the declared smoke.

## 2. Non-circularity

- Import graph: `world.py` imports only `numpy` and `numba`. `run_lone.py`, `run_onset.py`, `run_levelclass.py` import `world` (and `run_lone.realized` for level-class costs). `run_onset2.py` and `run_pop_r.py` import `run_onset`. None of them import `theory`, `THEORY_PREDICTIONS.json`, or any earlier simulator (POOLSIM, SENSING, SENSING2).
- There is no expected-cost closed form in the simulator. `episode_cost` is spend plus realized mean squared error on a fresh path. Tech-A `tune_alpha` minimises innovation SSE on observations only.
- `theory.py` duplicates world constants by hand and is used by the analysis and by `postlock_fixes.py`, not by the world.
- **Declared, and I agree it matters:** N-grid centres are exactly theory N\* (I recomputed; max relative difference 0). An onset outside the ×/÷16 window would have been reported invalid, not forced. Every valid ES onset fell inside its grid. This can hide a miss that lands off-grid, and is conservative for PASSes only if the window is wide enough; here it is wide, and the RA onsets sit close to the measured-input prediction, not pinned to the grid centre.
- A learner that reliably minimises realized cost approaches the world's optimum. A PASS is evidence that GTAO's continuous-time algebra predicts what selection on realized payoffs finds in this discrete, noisy, learned world. It is **not evidence about nature.** The pop learner is closer to exhaustive search and is correctly labelled robustness, not a locked pass.

`run_lone.py` does compute `e_g_measured = −(1−b)/(1−a)` after Stage A; that is an output of the measurement step, not a quantity the trackers are given.

## 3. Reproduction

All official analysis reruns (`python3 analyze2.py`, `analyze.py`, `postlock_fixes.py`, and `analyze.py` on `results_pop_dedup.jsonl`) are **byte-identical** to the committed `ANALYSIS_*.json` and `POSTLOCK_FIXES.json`.

Locked PREREG_2 RA result, reproduced: ê = −0.735554, CI [−1.031066, −0.519917], valid ρ = {0.16, 0.32, 0.64, 1.28}, measured-input window prediction −0.758544, members'-class rival −1.649689, bootstrap SE 0.136, MV8 gate 0.318, rival killed, verdict PASS. Π ratios vs the measured-input N\* are 1.059, 1.032, 1.163, 1.074. N̂\* = 66.1, 35.4, 23.4, 13.9 against predicted 62.4, 34.3, 20.1, 12.9.

Primary (PREREG) onset estimates, reproduced:

| Arm | ê | 95% CI | Valid ρ | N̂\* on the valid set |
|---|---|---|---|---|
| RR | −0.7614 | [−1.177, −0.402] | 0.04–0.32 | 55.3, **107.5**, 29.0, 14.7 |
| RRh | −1.1539 | [−1.861, −0.763] | 0.04–0.32 | 266, 124, 46.7, 25.6 |
| AA | −2.1708 | [−2.963, −1.476] | 0.04–0.32 | 31411, 6023, 1010, 378 |
| AR | −1.9976 | [−2.802, −1.389] | 0.04–0.32 | 5712, 936, 285, 84.0 |
| RA (primary, 3 ρ) | −0.8915 | [−1.368, −0.499] | 0.08–0.32 | 122, 66.1, 35.4 |

RR's N̂\* rises from ρ = 0.04 to 0.08. That is the opposite of the predicted direction and is the main reason the RR known-groups test is only INCONCLUSIVE (ê = −0.76 vs measured-class window −0.933, CI includes the prediction). AA's PREREG_2 gated window (0.16–1.28) is a PASS (−1.538 vs −1.650).

Simulator subset, `nice -n 19`, locked seeds, compared to the saved jsonl: RR / RA / AA at ρ = 0.16 seed 0, and RA at ρ = 0.64 seed 0. In all four jobs the learned policies match exactly, `flat_pm` matches exactly, and max |Δ D_rel| is < 10^{−15}. The onset data are deterministic and the committed lines are the output of the committed code.

Pop-learner N̂\* (secondary): RR 335, 185, 99, 52, 27.3, 14.5 vs theory 402, 202, 102, 52, 27.0, 14.4; RRh 779, 389, 188, 96, 49.5, 26.2 vs 749, 376, 190, 96, 49.5, 26.1. ê within the 15% band, as written.

## 4. Is the RA pass a forking-paths artifact?

**No, not under the locked rule and the checks below.** The gated ρ set {0.16, 0.32, 0.64, 1.28}, the window (not asymptotic) prediction, the 0.6-decade / ≥ 3 ρ rule, the 15% tolerance, PAVA, MV8's 2.8, and the rival-kill thresholds were locked in PREREG_2 before onset output (subject to the 08:21 caveat in §1). The extra ρ = 0.64, 1.28 were justified by a selection gate computed from Stage A dispersion (ε̂ = 3.77% for A members ⇒ ρ > 0.12), also locked before onset.

| Check | ê | Verdict vs locked window pred | Members'-class rival |
|---|---|---|---|
| Official (16 seeds, PAVA) | −0.736 [−1.03, −0.52] | PASS (error 0.023 vs tol 0.114) | killed |
| Drop ρ = 0.16 | −0.675 | PASS | killed |
| Drop ρ = 0.32 | −0.751 | PASS | killed |
| Drop ρ = 0.64 | −0.740 | PASS | killed |
| Drop ρ = 1.28 | −0.750 | PASS | killed |
| Also include 0.08 (below the locked gate) | −0.777 | PASS | killed |
| No PAVA (raw-mean crossing) | −0.736 (identical; the isotonic fit did not bind) | PASS | killed |
| No common random numbers | −0.744 [−1.05, −0.52] | PASS | killed |
| Logistic N50 slope | −0.785 | — (close to −0.759) | — |
| First 8 seeds | −0.808 [−1.44, −0.52] | PASS | killed |
| Even seeds | −0.656 [−1.27, −0.36] | PASS (error 0.103, just inside 0.114) | killed |
| Odd seeds | −0.792 [−1.06, −0.55] | PASS | killed |

If the prediction is replaced by something that was **not** the locked target, the pass goes away, which is what you want if the lock is doing its job: the effort-elasticity asymptote −0.985, the theory window −0.950, the theory asymptote −1, and Stage-A cost-elasticity −1.003 are all INCONCLUSIVE against this ê. The members'-class asymptote −1.969 is a MISS (rival killed). The authors correctly judged on the measured-input *window* slope, and said so in advance because the gated window is not asymptotic.

Caveats that do **not** overturn the locked PASS but must travel with it:

1. **Known-groups (MV7) is only half-green.** AA PASSed; RR is INCONCLUSIVE, and RR's N̂\* is non-monotone. The locked text flags AR/RA only if a known-groups arm *MISSes*. I would still not call the instrument fully calibrated.
2. **T1.8 is not passed.** AR points the same way (−1.998 vs −1.912; rival −0.933 excluded) but fails MV8 by 0.02 on the SE. That is close, not a reason to waive a locked gate.
3. Even-seed ê is close to the 15% line. The official 16-seed result is not.
4. This is regime A (Brownian, one source, quadratic bundled loss), in a model world, on the RA arm only.

C1 is the contrast that *does* look like a forking-paths / fragile-end artifact: the locked valid set includes the noisiest ρ, RR's N̂\* is not monotone, and dropping ρ = 0.04 (or restricting to 0.16–0.32) stops the "rival killed" rule from firing. I do not overturn the locked-rule application; I downgrade the substantive claim.

## 5. Post-lock fixes: were they honest?

Yes. `postlock_fixes.py` is labelled post-lock in its docstring, in `RESULTS.md`, and in the results commit message. I reran it; `POSTLOCK_FIXES.json` is byte-identical.

The three code/text disagreements and the two additions:

1. **Factorial MISS sign.** Locked `analyze.py` used `s * hi < 0` as the MISS test. When the predicted sign is negative, that fires whenever the upper CI is positive, including when the CI contains 0. The PREREG text says MISS only if the CI is wholly on the wrong side. Four cells move from MISS → INCONCLUSIVE (RR shared×2, RRh both×2, AR shared×2, AR both×2). The two shared×2 PASSes (RRh, RA) are unchanged. No new PASS.
2. **Measured-(a, b) span rule.** The locked code returned PASS for AA, AR, RA without requiring ≥ 4 valid ρ spanning a decade. The text requires it. All four arms become (or stay) INCONCLUSIVE. No new PASS.
3. **C1 predicted difference** was NaN in the locked code when the arms were inconclusive. The post-lock number (−0.942 over the common valid ρ) is a disclosed addition; it is inside the CI and is not used to create a kill or a pass (the kill uses only the pre-specified upper-bound < −0.4).
4. **Noise-vs-prize diagnostics** are labelled secondary.

Every correction moves a verdict toward INCONCLUSIVE or adds a number. That is honest. The text was correctly treated as governing.

## 6. Wording of "killed the members'-technology-sets-exponent rival"

The correct, complete sentence is:

> In this designed simulation, in THEORY.md §2.2 **Regime A** (Brownian increments, one shared source, quadratic bundled loss), on the **RA arm only** (reset-type level, averaging members), the members'-class rival for the onset exponent was killed under the PREREG_2 rule. This is **in-model only**. It is **not** a pass of T1.8, which required the same result on AR as well and was **NOT PASSED**. It is not a field result and is not a law.

`RESULTS.md` already says most of this: the T1.8 headline is NOT PASSED; the rival kill is stated in the RA cell; the "What this test is and isn't" section states "not evidence about nature" and "Regime: Brownian drift only, i.e. THEORY.md §2.2 Regime A"; point 7 repeats that it is not about real organisations. I **confirm** that wording as adequate in the results file.

What would be incorrect, and should not appear in a chat summary or a claim-map short title without the qualifiers: "LEARNSIM killed the members-set-the-exponent rival" or "T1.8 passed on RA." C1 is a different rival (technology-independent exponent) and, as §4 says, I downgrade that kill.

## 7. Provenance against current THEORY.md (v1.2.1, origin/main as of 09:14 ET)

`RESULTS.md` cites "THEORY.md v1.1, origin/main ac7f33a". That pointer is stale. v1.2 (PR #4) added the canonical-file rule, §2.5 (regime first; formal constants are functions of H; Proposition SG), and §8c. v1.2.1 (PR #7, 09:14 ET) applied the audit-referee wording fixes. I checked the substance against **v1.2.1**. None of the LEARNSIM locks or numbers depend on the stale pointer. Line numbers in the authors' table have shifted; the claims they pointed to are still in the current file.

| Prediction | Still in v1.2.1? | Referee note |
|---|---|---|
| Onset N\*(ρ), exponent −(1−b)/(1−a) set by the **level's** class | Yes: §1 N2, §8b candidate 1, §9, §11 history item 3 | Correctly labelled Regime A. §2.5 now says the class-R constants (a = b = ½, vigilance floor 1+(1+ρ)^{−1/2}) are the H = ½ instance of a = b = 1/(1+2H). This test is that instance (Brownian). It does not test the spectrum hypothesis (N6), as the authors said. |
| Numerical averaging class (a = ⅔, b = ⅓, e = −2) | **Still not in THEORY.md.** From formal Lemma 1 | The authors' flag stands. PREREG_2 avoids relying on it by measuring the class. |
| Technology, not loss, sets the exponent (C1) | Yes, §8b candidate 2 | In-model, regime A. I downgrade the sim kill (§4). |
| Measure the level's class, then predict (PREREG_2) | Yes, §8b candidate 6 | This is the programme I16 / FRAMEWORK §6.1. The RA arm is a first in-model run of it. T1.8 as a whole is not passed. |
| V at onset, exact formula, floor 1+(1+ρ)^{−1/2} | Yes, §6 L199–200, §9 | Numbers in `theory.py` match the formal / math-review formula, denominator **ρ**. Current THEORY.md typesets the upkeep term as `/(rρ)`. That looks like a typo (an extra r); I did not treat it as a change of target. AA's V still comes from formal T5.3, not from THEORY.md text; the authors' flag stands. |
| T3 opposite signs | One-line mention; §8b / FORMAL row: mixed-technology sign only at small ρ or with a common technology | The authors' flag stands: mixed-arm T3 at ρ = 0.04 is outside the scope the current text states. Cells were INCONCLUSIVE anyway (except two shared-side PASSes). |
| T1.7 "both ×2" / "volatility promotes levels" | **Still not in THEORY.md** as a theorem. L282 points the other way once delay is allowed | Flag stands. Cells INCONCLUSIVE. |
| P10 and POOLSIM F1 | Not in THEORY.md as formulas; N2 remarks on decision noise | Flags stand. Secondary; F2 was pre-labelled weak. |
| §9 sink: onset exponent excludes the level-class value, over ≥ 1.5 decades, prize > noise, class measured separately | Still there (L301) | This test does **not** fire a sink. ES learners did not get 1.5 findable decades. The pop learner did, but is not a locked verdict and is closer to circular. |

THEORY.md's status block still says "Simulations: passes so far are circular; four locked in-model predictions failed." After this test that sentence is incomplete: there is now a non-circular in-model RA mixed-arm PASS (and locked-rule V and C1 results, the latter downgraded here). I recommend a one-line update in a later THEORY.md revision; I am not editing THEORY.md in this PR.

## 8. Claim-map changes

**No existing `measurement/CLAIM_MAP_v2.md` row changes status.**

- B9 (T1.8, level's class sets e_g) stays **PROVED (in-model)** from the formal layer. This simulation did not pass the locked two-arm test, so it cannot upgrade or threaten B9.
- I16 (measure the level's class, predict the group) stays **OPEN**. It is a field programme. RA is one in-model data point, not a field instrument.
- G7 / G12 (SENSING rivals) stay **OPEN**; they are about those earlier tests.
- G8 stays **MATH-CORRECTED**.

Recommended *new* G-section rows (not applied in this PR; for the maintainer):

| # | Claim | v2 status | Why |
|---|---|---|---|
| G23 | LEARNSIM ES onset exponents under the PREREG decade rule | **SIM-INCONCLUSIVE** | Locked; only 0.9 findable decade |
| G24 | LEARNSIM C1, technology-independent exponent | **SIM-PASS (downgraded)** | Locked rule fires; not robust to dropping ρ = 0.04; RR N\* non-monotone. In-model, regime A |
| G25 | LEARNSIM PREREG_2 T1.8 overall | **NOT PASSED (in-model)** | RA PASS, AR INCONCLUSIVE (MV8); RR known-groups INCONCLUSIVE |
| G26 | LEARNSIM PREREG_2 RA: level class predicts ê; members'-class rival killed | **SIM-PASS (in-model, regime A, RA only)** | Reproduced; robust under §4. Not a T1.8 pass and not a field result |
| G27 | LEARNSIM V at onset, class R | **SIM-PASS (locked rule)** | RR and RRh geo-mean within ×/÷1.15; wide per-ρ CIs; in-model, regime A |
| G28 | LEARNSIM T3 factorial signs | **SIM-INCONCLUSIVE** | Two shared-side PASSes after an honest post-lock fix; no private-side confirmation |
| G29 | LEARNSIM pop-learner RR/RRh (secondary) | **NOT EVIDENCE (robustness only)** | Recovers T1 when learning noise is small; closer to an exhaustive optimiser |

Queue ledger outcome for LEARNSIM (protocol v2): `status_changed` = false, `rows` = [].

## 9. What would settle it

The authors' next-step list is right and should be freshly locked: more (or better) learners so per-seed noise falls below bρ; T3 factorial at a gated base (ρ ≈ 0.16); AR with 32 seeds to clear MV8. I would add: a pre-specified monotone-N\* (or drop-nonmonotone-ρ) rule, so a C1-style contrast cannot lean on a non-monotone RR onset; and a known-groups *pass* requirement, not only a MISS flag, before a mixed-arm PASS is allowed to move a claim-map row. None of that is to be done by re-analysing this file.

---

Checks live in `reviews/night2/LEARNSIM_REFEREE_checks/` (`rerun_official.sh`, `robust_ra.py`, `rerun_jobs.py`, rerun JSON, `robust.json`, `sim_rerun.json`). Working data: `<local>/gtao/night2/LEARNSIM/` and branch `learnsim-prereg` (commits `820b224..2843f5b`).
