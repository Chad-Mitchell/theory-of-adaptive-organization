# Independent review: DECISIVE (banks, glucose, populations) and F1 (US public firms)

Reviewer: Grok Bot executor (independent subagent). I did not build either test. Written Sat 2026-11-14, ~23:30 ET.
Scope: provenance of the preregs, a rerun of every main analysis, my own extra checks, a ruling on each deviation, whether the kill rules fired, and a referee verdict.
No test folder was edited. Reruns ran on copies in /tmp, which have since been deleted. My scripts are in `reviews/DECISIVE_F1_review_checks/`; they are exploratory, not preregistered.

**Bottom line**
- The arithmetic is sound and reproduces exactly.
- The preregs are real but self-attested.
- Every test gets the *signs* right.
- None hits the theory's *quantitative* predictions: the −1 slope, the √τ weight, the identities, or the collapse.
- Nothing tested so far separates GTAO from a generic "mean-reverting process with a barrier" model. That model is textbook (Siegert 1951; Black–Cox 1976; Lande & Orzack 1988).
- Under MATH_ATTACK's literal joint-kill rule, the τ/"dynamical temperature" term is **killed on the most natural reading**. It survives only through the sampling-corrected targets, and those were added after MATH_ATTACK wrote the rule.

---

## 1. Provenance: were the preregs committed before the outcomes?

| Test | Prereg commit | Outcome first on disk | Hash check now | Note |
|---|---|---|---|---|
| F1 | d656d6a, 2026-11-14 22:36:14 ET | `raw/submissions.zip` mtime 22:36:35 ET (21 s later) | PREREG.md + 8/9 code files OK; `outcome.py` FAILS (expected, see below). RESULTS.sha256 all OK. submissions.zip sha256 509f4566… matches `raw/submissions.sha256` | Outcome file absent at commit, as far as file times can show |
| DECISIVE/banks | 2b12786, 22:53:42 ET | `banks/data/failures.csv` mtime 22:53:51 ET (9 s later) | all 6 OK | Outcome absent at commit |
| DECISIVE/glucose | 2b12786 | `data/outcome_block.parquet` written 22:51:22 ET, **before** the commit, and committed with it | PREREG OK; `code/analyze.py` FAILS (post-outcome D1 fix, disclosed) | Outcome data were on disk; blinding is self-attested |
| DECISIVE/populations | 2b12786 | `data/outcome_block.csv` written 22:47:12 ET, before the commit | all 4 OK | Same. Plus one disclosed aggregate leak: "336 of 421 series have no zeros over the whole series" |

**Caveats a hostile referee will raise**

1. **Nothing anchors the commits externally.** Both repos are local, unpushed and author-dated (author date = committer date, and the reflogs show only these commits). The hashes appear nowhere outside the test folders. File mtimes agree with the story, but the same agent controls all of them. The ordering is credible, not provable. For the next test, push the prereg hash somewhere third-party-timestamped (a public gist, OSF, or a Zenodo draft) before pulling outcomes.
2. **For glucose and populations, the outcome block sat on disk next to the prereg author.** "No counts were computed" is an unverifiable claim. Banks and F1 are cleaner because the outcome file did not yet exist.
3. **Clerical: the written times disagree with the file times.**
   - glucose/PREREG.md says "~23:00 ET", but the file was last modified at 22:53:41 and committed at 22:53:42.
   - banks says "~22:55", but the file mtime is 22:52:51.
   - These look like estimates, not tampering, but fix them.
4. **Pace.** DECISIVE ran from data download to all three results in about 23 minutes (22:38 to 23:01 ET), with three preregs written in roughly 15 minutes. Speed alone is not misconduct. Still, the "locked design" was written fast by the same agent that had the data.
5. **Post-commit code changes**
   - F1 `outcome.py`: I read the diff. The zip is now opened once per worker, with no logic change. Confirmed. I also recoded the outcome independently (§2).
   - glucose `analyze.py`: (a) a BFGS → GLM-NB/HC0 fallback for NaN SEs; (b) the collapse model now uses the same fit function. Both were made after outcomes. The authors say the primary P1 estimate is unchanged. I could not verify that without the pre-fix output (none was saved). Since the fallback only fires when SEs are NaN, the claim is plausible. Treat the glucose P4 collapse numbers as post-hoc-coded.

## 2. Reruns

- **Method.** Every `analyze.py` and `exploratory.py` ran on a copy, with the repo's own venv for DECISIVE and system python3 + lifelines for F1.
- **Result.** All outputs are **identical** to the committed `results.json` / `exploratory.json`, for all four tests and every key. That covers F1's 1,000-resample bootstrap at seed 20261114.
- **Independent data checks**
  - **Banks:** I refetched the live FDIC failures API. It lists 4,117 records and 507 failures in 2008–2014, the same CERT set as the cached file. 421 of the 7,857 predictor rows match a failure; the code keeps 419 after the B>0, σ>0 filters. ✓
  - **F1:** my own recode of 8-K Item 1.03 inside each cohort window, read straight from submissions.zip, gives **183 events, 0 disagreements**. Spot-checked events are real Chapter 11s, e.g. Cenveo 2018, Gordmans 2017, Standard Register 2015, Ebix 2023, Enviva 2024. ✓
  - **Populations:** I independently recomputed the sampling-corrected target. I used the exact per-year downcrossing probability of a stationary, annually sampled Gaussian AR(1), with each series' own φ and z, on the real design. That gives **−0.339**, matching the prereg's β\* = −0.34. ✓ The cold subset (z ≥ 1.5) gives **−0.287**.
  - **Not re-derived:** glucose's β\* = −0.82/−0.65. Raw GPDD/CGM files were not re-downloaded; I used the stored copies.

Key numbers confirmed:

| Test | Primary number |
|---|---|
| Banks | β_lnτ\|σ,B = +0.202 [0.111, 0.293]; P3 +0.049 [−0.028, 0.127]; own-mean τ +0.06 [−0.03, 0.15]; ΔAIC vs Z-score 15.4; P4 ΔAIC 7.1; incident identity p = 0.041; continuous p ≈ 1e-64 |
| Glucose (REPLACE-BG) | fixed-spread slope −0.46 [−0.70, −0.23]; lag-1 τ −0.09 [−0.19, 0.01]; G3 −0.14 [−0.55, 0.27]; collapse fails |
| Populations | −0.211 [−0.37, −0.05]; cold +0.10 [−0.29, 0.49]; S5 −0.09 [−0.36, 0.17]; Dennis LR p = 0.50; collapse fails |
| F1 | β_τ 0.354 [0.21, 0.50], β_σ 0.22, β_B −0.31; r_τ 1.61 (boot 0.73–4.66); P2 +0.0067 [−0.0001, 0.0135]; LR p 0.024; τ + margin 0.15 [−0.04, 0.34] |

## 3. Deviations and post-hoc choices, judged

### Banks: detrended τ instead of MATH_ATTACK's own-mean τ — *legitimate in procedure, damaging in substance*
- **Procedure.** The switch was declared in the prereg, made before the failures file existed, and had a stated predictor-only reason: 36.7% of own-mean fits hit the φ = 0.95 clip. That is a reasonable fix for trend-contaminated AR(1) fits.
- **Substance.**
  - The version MATH_ATTACK actually specified is **null**: +0.06 [−0.03, 0.15].
  - With both measures in one model, they go opposite ways (+0.33 / −0.17).
  - This is one fork in a garden of forking paths. The analyst saw predictor diagnostics, not outcomes, and chose the definition with more variance. That choice was not outcome-tuned, but a referee will discount it.
- **Confound I tested.** "Detrended persistence" might just flag banks whose capital ratio rose and then fell (late-2000s growth into commercial real estate). I added quadratic curvature, linear slope, the 8-quarter change in the capital ratio, and 8-quarter asset growth. β_τ stays at **+0.215 [0.122, 0.309]**, so curvature does not explain it. With the same controls, own-mean τ is +0.09 [−0.004, 0.183].
- **Ruling.** The bank τ signal is real in this data and holds up to my checks. It is specific to the detrended definition.

### Banks: is "HIT" the right label? — *overstated*
- The hit rule needs only β_τ > 0 and a positive P3 *point* estimate. P3 is the one prediction that separates GTAO from "slow banks die when weak", and its CI includes 0.
- Median z ≈ 29, and the jump-share check says failures were 21σ shocks. The prereg itself says the theory then predicts ε_τ → 0. A clearly positive β_τ is therefore **not** what the diffusive mechanism predicts here. It is what a generic "persistently weak capital management" story predicts.
- The quantitative structure all failed:
  - ε_B = −ε_σ is rejected (p = 1e-5);
  - the continuous identity is rejected (p ≈ 1e-64);
  - P4 failed (ΔAIC 7.1, below 10);
  - the incident identity is rejected at α = 0.05 (p = 0.041), yet RESULTS calls it "roughly".
- **Ruling.** Accurate wording is "the sign of the τ term replicates; nothing specific to the theory does."

### Glucose and populations: lowering the −1 target to sampling-corrected β\* — *mathematically right, procedurally a goalpost move*
- **The math is right.** I reproduced −0.34 exactly for populations. With annual sampling against a median τ of about 3 years, a literal OU process would not show −1. MATH_ATTACK itself flagged sampling bias as a risk.
- **The procedure is the problem.** MATH_ATTACK wrote the kill rule as "closer to 0 than to −1", and each test then rewrote its own kill rule against a model-derived target before outcomes. In plain terms, the theory's own rule was mis-specified for the data it was pointed at. Once the target is "whatever a stationary AR(1) would give on this design", the test checks the AR(1)/OU model, not GTAO (see §5).
- **Ruling.** Report the corrected verdicts, but lead with the literal verdicts. The summary table already does this.

### Glucose: adding REPLACE-BG (and making it the decisive cohort) — *legitimate*
- It was declared before outcomes, with a sound power reason: Shanghai's P(false kill) was 0.25. It is labelled as added beyond the brief, and Shanghai is still reported.
- **Weaknesses**
  - REPLACE-BG's SD of ln τ is only 0.225, a narrow lever arm.
  - The result depends on the τ definition: lag-1 AR(1) τ gives −0.09, null.
  - Conditioning on the first-block episode rate erases it (G3 −0.14, CI spans 0). Whatever τ carries largely duplicates past hypo frequency.
  - P2 is a reparametrization of P1 (σ ≡ s√(2/τ)), so it adds no independent evidence. RESULTS says so.

### Populations: fur-harvest compilation — *a pre-registered filter failure that undermines the dataset*
- Source 12 (Novak et al. 1987, *Furbearer harvests in North America*) is **138 of 274 series**, recorded as "All Individuals". These are harvest counts, driven by trapping effort and pelt prices, which the prereg meant to exclude. The filter failed silently because of a units label.
- The authors' exploratory splits look reassuring: −0.26 without source 12, −0.20 within it. But "within source 12" used unclustered SEs on 138 series that share the same years and fur markets.
- My own checks:

| Specification | Slope [95% CI] |
|---|---|
| Source 12 only, clustered by taxon (12 taxa) | −0.20 [−0.55, 0.16] |
| Full sample, clustered by taxon instead of source | −0.21 [−0.42, 0.002] |
| Full sample + source fixed effects | −0.14 [−0.31, 0.03] |
| Non-clipped φ and no source 12 | −0.11 [−0.62, 0.40] |
| Drop the fastest τ quintile | −0.04 [−0.33, 0.25] |

- **Shape check.** Crossing rate by τ quintile, fast to slow, is 0.051, 0.028, 0.022, 0.020, 0.029. The sampled-OU theory predicts 0.046, 0.023, 0.019, 0.016, 0.016.
  - Quintiles 1–4 fit the theory; I had expected the fast end to break it, and it doesn't.
  - The slowest quintile crosses at almost twice the predicted rate, which points to non-stationarity or trends.
  - The fast quintile, which carries the effect, is 38% series clipped at φ = 0.05. Observation error predicts the same pattern: noisy counts give a low φ and spurious crossings. The test cannot tell those apart.
- **Other failures.** In the cold regime, the part the theory says matters most, the slope is +0.10, the wrong sign. The Dennis baseline is not beaten (p = 0.50). The collapse fails (Osteichthyes −1.70).
- **Ruling.** The population "HIT" is fragile: one structural choice (source FE or taxon clustering) or one quintile flips it to non-significant. It should not be cited as support.

### F1 deviations — *minor and clean*
- These were all made before outcomes: the τ redefinition ("1 +"), the added C1 cohort, and the flexible P2 spec chosen by a predictor-only null simulation.
- The verdict honestly says the τ main effect replicates published cost-stickiness → distress work.
- The post-hoc margin and loss controls, and the γ/λ decomposition, are labelled exploratory. They are the most informative thing in F1: the signal is fixed-cost share (1−γ, operating leverage), not correction speed λ (0.12 [−0.05, 0.29]). So F1 does not measure "time to fix" at all. Its construct validity fails.
- The "τ weight ≈ 1, not ½" claim rests on 3 grid points with a log-likelihood gap of 2.9. That is suggestive, not a finding.

## 4. Did the literal kill rules fire?

| Rule | Banks | Glucose (REPLACE-BG) | Populations | F1 |
|---|---|---|---|---|
| The test's own prereg KILL | no (z ≥ 1.5: +0.22 [0.13, 0.31]) | no (−0.46 is closer to β\* −0.82 than to 0) | no (CI contains β\*) | no (K1, K1c, K2, K3 all false; verified) |
| MATH_ATTACK joint kill, cold regime (z ≥ 1.5): β_τ\|σ,B ≤ 0 with CI excluding +0.2, **or** fixed-spread slope closer to 0 than to −1 | does not fire | **not evaluable as written** (n = 2 cold subjects); on the full sample the slope is closer to 0 → fires | **fires** (cold fixed-spread slope +0.10, wrong sign; even the full sample's −0.21 is closer to 0) | not computed in F1's design |
| MATH_ATTACK D2 band [−1.4, −0.6] | — | **fails** (−0.46) | — | — |

The joint rule needs two or more scales.
- Populations fires unambiguously.
- Glucose fires on the full sample but cannot be evaluated in its cold regime.
- So the literal joint kill **fires on the natural reading** and is formally indeterminate only through glucose's empty cold cell.
- An honest write-up should say "the literal kill rule fired; with sampling-corrected targets introduced afterwards, it does not." It should not say "kill not triggered."

The SUMMARY.md table already says "fires" for glucose and populations. Keep that and lead with it.

## 5. Is "fewer crossings at fixed spread with slower correction" just dimensional analysis?

**Yes, essentially.**
- Take any stationary process with one timescale τ, a stationary spread s and a barrier B. A crossing rate has units of 1/time, and τ is the only timescale, so rate = τ⁻¹·f(B/s) (Buckingham π). That gives slope −1 at fixed spread.
- This needs no adaptation, organization, model, cost currency or thermodynamics. A thermostat, a viscous pendulum or an AR(1) of rainfall predicts the same.
- The fixed-σ version (β_τ > 0, risk ∝ σ√τ/B) is the same fact read the other way: stationary variance is σ²τ. That is Merton/Black–Cox with horizon τ. The theory's own math notes say it reduces to the Black–Cox first-passage form.

**Where the content would be, and how it fared**
- (a) **The shape f and a cross-system collapse.** This failed in both glucose (offsets −1.2 to −1.4) and populations (Osteichthyes −1.7).
- (b) **The exact exponent.** −1 fails everywhere. Where the shortfall isn't a sampling artifact, it means these systems are multi-timescale. That fits the litmap's own "layered memory / power-law forgetting" point and contradicts the single-τ temperature.
- (c) **The interaction with z.** Not significant at any scale (banks +0.05, populations +0.20, glucose −0.16, F1 P2 p = 0.055).

**Competitors.** The preregistered competitors were the Z-score, LBGI/CV and Dennis. Each lacks mean reversion by construction, so beating them on τ shows only that mean reversion exists. The competitor that matters, a generic OU-with-barrier model, predicts the same signs as GTAO in all four tests and was never posed as an alternative.

## 6. Referee paragraph (as a hostile referee would write it)

> The authors preregistered four real-data tests of the claim that slower error-correction raises failure risk at fixed shock and buffer. The computations reproduce exactly and the outcome coding checks out, but what is confirmed is modest and not theory-specific. Every directional result follows from treating each system as a stationary mean-reverting process with an absorbing or reflecting barrier: at fixed stationary spread, crossing rates scale as 1/τ by dimensional analysis, and at fixed innovation they rise with τ because variance accumulates as σ²τ. That is the Black–Cox/Siegert first-passage result, not a new law of adaptive organization. The distinctive predictions failed:
> - the −1 fixed-spread exponent (−0.46 in glucose, −0.21 in populations; the literal kill rule fires at the population scale and, on the full sample, at the organism scale);
> - the √τ weighting (F1's data prefer a weight near 1, and its "τ" measures operating leverage rather than correction speed);
> - the ε_B = −ε_σ and continuous identities (rejected in banks);
> - the z-interaction (null everywhere);
> - the cross-system collapse (fails by 1–1.7 log units).
>
> The surviving positive results lean on analyst choices:
> - a detrended τ in banks, where the specified own-mean τ is null;
> - an ACF-1/e τ in glucose, where lag-1 τ is null and past episode rate absorbs the effect;
> - a population sample half made of fur-harvest records, whose effect loses significance under source fixed effects, taxon clustering, or removal of clipped/fastest series.
>
> The "sampling-corrected" targets are correctly derived, but they were introduced after the theory's own kill rule was written, and they turn the test into a test of an AR(1) model. Preregistration was genuine in intent but rests on unpushed local git timestamps, with outcome data already on disk for two of the three DECISIVE arms. I would summarize the evidence as: mean reversion matters for failure (known), the specific GTAO structure is unsupported, and by its own literal rule the dynamical-temperature term is falsified at two scales. Reject as evidence for the theory; acceptable as an honest negative/replication report.

## 7. Recommended wording changes (for Ace/Chad; none made)
- **SUMMARY.md, banks:** "HIT (sign)" → "τ sign replicates (detrended τ only; specified own-mean τ null); all quantitative/theory-specific checks fail".
- **Populations:** add the fur-harvest share, the source-FE/taxon-cluster results, and the wrong-sign cold slope beside "HIT".
- **Overall:** "MATH_ATTACK joint kill: fires on natural reading (populations cold; glucose full-sample); avoided only via post-rule sampling corrections."
- **Public post:** the live qualifier about slow fixers needs softening, as the parent already suspected. No public claim should say these tests support the τ term specifically.
- **Next test:** anchor the prereg hash externally before any outcome pull, keep outcome blocks off the box until then, and preregister a generic OU-barrier competitor that GTAO must beat. It must beat it on the exponent, the collapse or the interaction, not on sign.
