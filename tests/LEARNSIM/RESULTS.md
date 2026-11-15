# LEARNSIM results: a learning-agent onset test of GTAO's surviving in-model results (no cost function given)

Private. America/New_York times. Nothing posted or sent. Repo `Chad-Mitchell/theory-of-adaptive-organization` is still PRIVATE; locks are on branch `learnsim-prereg` (no PR opened).

## Locks (all made before any onset output existed)
| Lock | Commit (ET) | What |
|---|---|---|
| PREREG.md + code + estimators + theory predictions | 820b224 08:16:31; 41f297c 08:16:37 (in-body time corrected to match the commit, text only) | `PREREG.sha256` |
| Stage A lone-member class | c95f3c6 08:20:58 | `MEASURED_AB.sha256` |
| PREREG_2 (mixed-arm level-class test, framework gates) | c86f8e5 08:27:34 | `PREREG_2.sha256` |
Onset runs started 08:28 and finished ~09:00; all hashes re-verified OK afterwards. Analysis code, bootstrap method and RNG seeds (analyze.py: 2026; analyze2.py: 2027) were inside the locks, which complies with the referee's 08:32 lock rule. Locks are self-attested (private commits, no third-party timestamp; that needs Chad's go).

## What this test is and isn't
- **Not circular in the night-1 sense.** The simulator contains no expected-cost formula. Trackers learn their policy by a noisy (1+1)-ES from realized payoffs, starting from a random policy. Averaging trackers tune their gain from their own observations only. Predictions come from a separate file (`theory.py`) or from **measured** cost laws (PREREG_2).
- **Still a model world.** A learner that minimises realized cost moves toward the world's optimum, so a pass means only this: GTAO's continuous-time algebra predicts what learning finds in a discrete, noisy, learned world. It is **not evidence about nature**.
- **Regime:** Brownian drift only, i.e. THEORY.md §2.2 Regime A, one source, quadratic bundled loss. It does **not** test the drift-spectrum hypothesis (N6).

## Headline (locked verdicts)
| Claim | Locked result |
|---|---|
| Onset exponent, ES learners, PREREG rule (≥ 4 valid ρ spanning ≥ 1 decade) | **INCONCLUSIVE in all 5 arms.** Only ρ ≥ 0.04 gave a findable onset (0.9 decade). Point estimates: RR −0.76 [−1.18, −0.40]; RRh −1.15 [−1.86, −0.76]; AA −2.17 [−2.96, −1.48]; AR −2.00 [−2.80, −1.39]; RA −0.89 [−1.37, −0.50] (valid 0.08–0.32). Theory windows: −0.96, −0.97, −1.93, −1.94, −0.95 |
| C1: rival "the exponent does not depend on sensing technology" | **Rival KILLED** (pre-specified rule): ê_AA − ê_RR = −1.41, CI [−2.25, −0.60], upper bound < −0.4. Theory predicted −0.94 over the same ρ (post-lock computation; the locked code returned NaN because the arms' e_pred was not computed when inconclusive), and that value is inside the CI |
| **PREREG_2 (framework gates, measured level class): T1.8 "the level's class sets e_g"** | **NOT PASSED.** RA **PASS** (−0.736 [−1.03, −0.52] vs measured-input prediction −0.759; members'-class rival −1.650 **killed**). AR point estimate −2.00 vs prediction −1.91, rival −0.93 excluded by the CI, but the bootstrap SE 0.371 exceeds the MV8 power gate 0.35, so the locked verdict is **INCONCLUSIVE (MV8 failed)**. Known-groups (MV7): AA **PASS** (−1.538 [−1.77, −1.33] vs −1.650); RR **INCONCLUSIVE** (−0.76 [−1.20, −0.39] vs −0.933) |
| V at onset (level effort ÷ flat member's), THEORY.md §6 exact formula | RR **PASS**: geometric-mean V̂/V_pred = 1.01 [0.85, 1.20]; per-ρ V̂ 1.42, 2.73, 2.02, 1.86 vs 1.98, 1.96, 1.93, 1.87. RRh (h′ = 1) **PASS**: 1.06 [0.89, 1.26]; V̂ 3.20, 3.12, 2.44, 2.43 vs 2.70, 2.67, 2.61, 2.52. AA **INCONCLUSIVE**: 1.22 [0.87, 1.70]. Every RRh per-ρ V̂ sits above the floor 1 + (1+ρ)^−½. Per-ρ CIs are wide |
| T3 signs (factorial at ρ = 0.04, ×2 factors) | Shared×2 lowers N* with a CI excluding 0 in **RRh (PASS)** and **RA (PASS)**. Every other cell is **INCONCLUSIVE**, including all private×2 cells, so the contingency-rival kill did not fire anywhere. **Locked-code bug:** the code labelled 4 cells MISS whose CIs actually include 0. The PREREG text rule makes them INCONCLUSIVE (`postlock_fixes.py`, disclosed). No cell has a CI wholly on the wrong side |
| Measured-(a, b) prediction (Stage A) | **INCONCLUSIVE** under the text rule (span < 1 decade). The locked code returned "PASS" for AA, AR and RA because it skipped the span check; that is a code bug and the text governs. Points agree: AA −2.17 vs −2.00; AR −2.00 vs −2.00; RA −0.89 vs −1.00 |

## Findability (the dominant fact)
- Per-seed noise in the realized per-member saving is 1.4–3.9% of cost (SD across seeds at the grid centre). It comes mainly from 16 ES-learning members per arm each mis-tuning by ~20–30% in ln effort. The prize bρ is 0.3–2% at ρ ≤ 0.04, so the small-ρ onset is buried. This replicates the POOLSIM / P10 / THEORY.md N2 warning ("invisible under ≥ 1% decision noise") with learners that were never given the cost function.
- The **PREREG_2 selection gate, computed before outcomes** (ε̂ = 1.47% for R members and 3.77% for A members, from Stage A dispersion), predicted where onsets would be findable: ρ > 0.030 (R members) and ρ > 0.12 (A members). The valid sets that came out (ρ ≥ 0.04 R-member arms; RA valid only from 0.08) matched that.
- F1 (POOLSIM: perception noise steepens the slope): **mixed.** AA steepened (−1.49 → −1.98 at ε = 1%). RR went shallower (−1.59 → −1.45). Not supported as a general rule.
- F2 (P10 tolerance threshold): **not borne out as a behaviour.** At ε = 1% under "adopt iff realized saving > ε", 38–44% of RR seeds still "adopted" at ρ = 0.01–0.02, below the predicted threshold 0.020. Those adoptions are noise, not real savings: with learning noise above the prize, a tolerance rule does not stop false adoptions. (I flagged F2 as weak in the prereg.)
- No common random numbers (independent worlds): RR −0.76 [−1.16, −0.40], AA −2.20 [−2.99, −1.52]. Essentially unchanged.

## Robustness learner (never decides a verdict)
Population-selection learners (every policy lives through one long common path, cheapest realized survives; R-level arms, 8 seeds) cut the learning noise. The onset then becomes findable over the full 1.5 decades:
- **RR −0.910 [−0.965, −0.851]** vs theory −0.963. N̂* = 335, 185, 99, 52, 27, 14.5 vs theory 402, 202, 102, 52, 27, 14.4.
- **RRh −0.982 [−1.043, −0.938]** vs −0.970.

Both are within the 15% tolerance. This is the cleanest evidence here that the ES INCONCLUSIVEs are learning noise, not a failure of the algebra. The caveat: this learner is close to an exhaustive realized-cost optimiser, so it is closer to the circular end. (The first launch of this run died silently under host memory pressure; it was resumed and one partial line deduplicated.)

## Honest reading
1. When learning noise is small, emergent onset in a no-formula world follows GTAO's T1 closed form in exponent and level (pop learner). This is robustness, not a locked pass.
2. With realistic noisy learners, the locked tests are mostly INCONCLUSIVE. The reason is findability, which the pre-outcome selection gate predicted.
3. Inside the gate, the first clean mixed-technology result came out: in RA, the **level's** measured class predicted the exponent and the members'-class rival was killed. The mirror arm AR pointed the same way but missed the power gate by a hair (SE 0.371 vs 0.35). So T1.8 is **not passed**.
4. The technology-independent rival is killed (C1).
5. Vigilance at onset matches the THEORY.md §6 exact formula in the two R arms (point-level; wide per-ρ CIs).
6. The T3 opposite-sign factorial was underpowered at its locked base ρ = 0.04, which sits at or below the selection gate. Only the shared-side sign was confirmed (2 arms), and nothing contradicted the sign.
7. None of this is evidence about real organisations.

## Theory provenance (current THEORY.md v1.1, origin/main ac7f33a)
| Prediction tested | Current THEORY.md source | Regime / assumptions | Older-file dependence |
|---|---|---|---|
| Onset N*(ρ), exponent −(1−b)/(1−a) set by the **level's** class | §1 N2 row, L53 ("generalized to N\* = [ρ^b/((1+ρ)^b−1)]^{1/(1−a)}, with exponent −(1−b)/(1−a) set by the level's sensing class"); §8b item 1, L261; §9 sink condition, L287 ("onset relation in agents not given the cost function…"); §11 test 3, L419 | Regime A (§2.2 L78–79, random walk with white increments); one source; h = 0, plus h′ = 1 in RRh; quadratic loss; component readability | Exact formulas and the upkeep root were taken from night-1 `FORMAL/THEOREMS.md` T1 (the same content THEORY.md cites). The **numerical class of averaging sensing (A_θ, a = ⅔, b = ⅓, e = −2) is NOT in THEORY.md**; it comes from FORMAL Lemma 1. **Flag: possibly outdated / not current-theory text.** PREREG_2 avoids it by measuring the class |
| Technology, not loss, sets the exponent (C1) | §8b items 1–2, L261–262 | Regime A | As above (A_θ class from FORMAL Lemma 1, flagged) |
| Measure the level's class, then predict (PREREG_2) | §8b item 6, L266; §11 L419 ("mixed-technology arm") | Regime A | None; inputs measured |
| V at onset, exact formula with upkeep, floor 1+(1+ρ)^−½ | §6 "Fractal vigilance", L192–194; §9 L286 | Reset-type (class R), Regime A, flat comparator | AA's V values come from FORMAL T5.3 (general class), **not in THEORY.md text. Flag** |
| T3 opposite signs of shared and private drift | Only a one-line mention: L17 ("opposite effects of shared and private drift") | Common technology at any ρ; THEORY.md §8b L249 notes the mixed-technology sign holds only at small ρ or with a common technology | Magnitudes and the mixed-arm sign predictions come from FORMAL T3 / T1.8. **Flag: mixed-arm (AR, RA) T3 at ρ = 0.04 is outside the scope THEORY.md now states** |
| T1.7 "both ×2" (total volatility promotes levels when h > 0) | **Not in THEORY.md.** L275 instead says "'Volatility promotes levels' assumes zero processing delay… point the other way" | — | From FORMAL T1.7 (night 1). **Flag: possibly outdated** (cells were INCONCLUSIVE anyway) |
| P10 tolerance threshold (F2) | **Not in THEORY.md** as a formula; only the N2-row remark on decision noise (L53) | — | From FORMAL P10. **Flag** |
| POOLSIM F1 (noise steepens slope) | Not in THEORY.md | — | From night-1 POOLSIM. **Flag** |
No prediction used `theorems/`, v2–v5, theory-v3, CLAIMS.md or the repo's `theory/THEOREMS.md`.

## Deviations and errors (all disclosed)
- **analyze.py bugs found post-lock**, where the code disagreed with the locked text (the text governs): (1) the factorial MISS sign rule; (2) the measured-(a, b) verdict ignored the span rule; (3) C1's predicted difference was NaN when the arms were inconclusive. Corrections are in `postlock_fixes.py` → `POSTLOCK_FIXES.json`, written after seeing outcomes. Every correction moves a verdict **toward INCONCLUSIVE** or adds a number; none creates a PASS.
- The first onset launch (08:21) died before writing any result (empty file). It was relaunched after the PREREG_2 lock.
- Smoke tests looked only at timing and structure, on out-of-design ρ = 0.5.
- The ES learner's integer-boundary pathology was fixed before the lock (PREREG §2).
- N grids were centred on the theory N* (declared); every valid onset fell inside its grid.
- The level learns from its own attributable cost share; the cross term enters evaluation only (declared).

## Files
`PREREG.md`, `PREREG_2.md` (+ .sha256), `world.py`, `run_lone.py`, `run_levelclass.py`, `run_onset.py`, `run_onset2.py`, `run_pop_r.py`, `theory.py`, `prereg2_predict.py`, `analyze.py`, `analyze2.py`, `postlock_fixes.py`; data `results_es.jsonl`, `results_ext.jsonl`, `results_pop.jsonl` (+ dedup); outputs `ANALYSIS_1.json`, `ANALYSIS_2.json`, `ANALYSIS_POP.json`, `POSTLOCK_FIXES.json`, `MEASURED_AB.json`, `LEVEL_CLASS.json`, `THEORY_PREDICTIONS.json`, `PREDICTIONS_2.json`.

## Next steps that would settle it
Use more learning members, or longer ES budgets, so the per-seed noise drops below bρ. Re-run the T3 factorial at a gated base (ρ ≈ 0.16). Re-run AR with 32 seeds to clear MV8. Each needs a fresh lock.
