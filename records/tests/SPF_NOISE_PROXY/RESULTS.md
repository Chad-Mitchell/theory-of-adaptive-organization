# RESULTS — SPF-NOISE-PROXY (queue pick 4, uniform slot; ledger 26–28, outcome 31)

Executor `queue-pick4` (for Ace; Chad t1914), Sunday 15 Nov 2026, America/New_York. Prereg `PREREG.md` locked at commit
`2f96b41` (10:48 AM ET) before any real dispersion other than LFK's h = 3 was computed. Real data extracted and analysed after
the lock with the locked code unchanged (`git diff 2f96b41 -- tests/SPF_NOISE_PROXY` empty for code; outputs only). The run
finished before an executor interruption at ~11:00 AM ET; nothing was re-run. Source section: THEORY v1.4.1 §2.2 Regime B
memory-time row (premise "white observation noise"), unchanged in v1.4.2. Measurement-validity item: **no CLAIM_MAP status
changes; N13 stays OPEN; vigilance stays OPEN.**

## Verdicts
| Test | Result | Label |
|---|---|---|
| Instrument selection (synthetic truth, pre-lock) | L0w (within-forecaster, level-normalised nowcast dispersion) recovers K within median 0.33 in log under pure noise and ≤ 0.35 under every contamination arm; LFK's proxy P0 is biased +0.9 to +1.7 (slow series) even when its premise holds and +1.2 to +2.3 under contamination | **passed on synthetic truth (MV7 in-model)** |
| T1 white-noise premise of h = 3 dispersion as N | G = ln K̂(h=3) − ln K̂(h=0) = +1.26 (UNEMP), +2.11 (HOUSING), +2.50 (TBILL), +2.04 (BOND), +2.30 (TBOND), +2.97 (RSLGOV): Holm p = 0.035 each (the floor with 200 null sims); INDPROD +1.08, p = 0.139 | **failed on proxy "horizon overidentification of SPF dispersion" for 6 of 7 variables**; INDPROD not rejected (low power) |
| T2 contamination concentrated in priced variables (LFK S-b reading) | d = +0.46 (z-p 0.106; permutation p 0.23) | **inconclusive**: contamination is broad, not specific to market-priced variables |
| T3 known groups for L0w: nowcast noise lower for priced variables | mean ln K̂_L0w non-priced − priced = +2.66 (≈ 14×), permutation p = 0.057 (≤ 0.06; minimum attainable 0.029) | **passed known-groups on real data (marginal, n = 7)** |
| S4 (POST HOC, β̂ seen; no verdict) | see below | not evidence |

## Per variable (`results/analysis.out`, `results/analysis.json`)
| Var (regime) | K̂ LFK proxy P0 (reproduced; LFK reported) | P0T (finite-sample corrected) | **K̂_L0w** [95% CI] | memory scale (K̂/q̂)^{1/α̂}, quarters: L0w vs LFK |
|---|---|---|---|---|
| UNEMP (B) | 0.0266 (0.027) | 0.0222 | **0.0077** [0.0041, 0.028] | 0.68 vs 0.94 |
| HOUSING (B) | 0.224 (0.21) | 0.189 | **0.030** [0.015, 0.067] | 0.78 vs 1.43 |
| TBILL (B) | 0.046 (0.045) | 0.029 | **0.0040** [0.0010, 0.015] | 0.33 vs 0.94 |
| BOND (B) | 0.232 (0.27) | 0.061 | **0.011** [≤0.0001, 0.087] | 0.91 vs 3.58 |
| TBOND (B) | 0.332 (0.35) | 0.074 | **0.0016** [≤0.0001, 0.0089] | 0.32 vs 3.42 |
| RSLGOV (A by rule; α unidentified) | 11.8 (11.3) | 7.8 | **0.17** [0.012, 0.28] | 2.07 vs 13.7 |
| INDPROD (A by rule; α unidentified) | 1.70 | 1.66 | **0.29** [0.16, 0.55] | 0.52 vs n/a |
K in units of the variable's population variance. The reproduction of LFK's K̂ (first column) from the microdata pipeline
checks the code. The P0/P0T gap is the finite-sample variance bias (3.8× for BOND, 4.5× for TBOND). Robustness (SD instead of
IQR): K̂_L0w moves within its CI except RSLGOV (1.0, at its lower-branch peak) and INDPROD (0.64).

## S4 — POST HOC (β̂ were published by LFK-ALPHA-SPF before this item; cannot count)
Optimal-filter CG coefficient β^G recomputed with K̂_L0w, LFK six:
UNEMP β̂ 0.82 vs β^G 0.32 [0.21, 0.43] (LFK 0.67); HOUSING 1.47 vs 0.35 [0.25, 0.47] (1.22); TBILL 0.62 vs 0.10 [0.03, 0.21]
(0.62); BOND −0.02 vs 0.56 [−0.95, 0.87] (2.82); TBOND −0.07 vs 0.09 [−0.72, 0.10] (2.83); RSLGOV 0.60 vs 0.15 [0.08, 0.25] (7.62).
Mean |ln β̂ − ln β^G|: L0w 1.73, L0 1.70, LFK 2.14, static rival 1.89, leave-one-out null 1.36.
Locked expectation "β^G < 0.5 for BOND and for TBOND": **TBOND met (0.09), BOND not met (0.56)**.

Plain reading (post hoc): (i) LFK's yield anomaly S-b came mostly from an invalid noise proxy (finite-sample bias plus
long-horizon heterogeneity); with the validated proxy the predicted yields' β is near β̂ ≈ 0 for TBOND and uncertain for BOND.
(ii) **LFK's S-a ("UNEMP, HOUSING, TBILL within 0–25% of the optimal filter") was also an artifact of the same inflated N.** With
measured nowcast noise, consensus CG coefficients for the non-financial series and the T-bill are 2.5–6× larger than the
optimal noisy filter implies: forecasters under-react more than their measured sensing noise justifies. That is the familiar
"information rigidity beyond noise" pattern (Coibion & Gorodnichenko, as recalled) and is POST HOC here.

## Validity as run (FRAMEWORK §2.2)
MV1 yes. MV2 improved (h = 0, fixed effects removed) but time-varying heterogeneity and partial in-quarter observation are not
modelled. MV3 yes (no β̂ used for N). MV5 no. MV6 partial. MV7 in-model yes; real-data known-groups T3 passed, marginally.
MV8: T1 size 0/30 and power 53% (λ = 1) in the dry run; observed G far beyond the null (≥ 3 null SDs in 6 of 7); T2/T3 n = 7.
The Holm floor 0.035 is a resolution limit of NSIM = 200 (declared, not changed). MV9: git lock, code, seeds, raw sha256.

## Surprises (QUEUE rule 4)
- **S-1 (largest):** LFK's S-a closeness disappears with a valid N; the remaining pattern is excess under-reaction relative to
  the measured-noise optimal filter (post hoc) → new item SPF-RIGIDITY-OOS; SPF-AQN-POWERED's rationale (S-a) is withdrawn.
- **S-2:** the D/vf dispersion proxy carries a large finite-sample bias for slow series even under its own premise; every
  dispersion-based N in the repo is suspect → NOISE-PROXY-REFEREE.
- **S-3:** contamination is broad (T2 inconclusive, T1 rejects for statistical-release series too), as Patton & Timmermann 2010
  found for GDP and inflation.

## Proposed theory/measurement edits (not applied; for independent review)
1. THEORY §2.4 / §8c (LFK-ALPHA-SPF line): add "post hoc S-a closeness was an artifact of an invalid noise proxy (SPF-NOISE-PROXY
   T1, S4); with measured nowcast noise the optimal filter under-predicts consensus CG coefficients 2.5–6× (post hoc)".
2. FRAMEWORK §3 (measuring N): "forecaster dispersion counts as N only after a horizon-overidentification check; default proxy:
   within-forecaster nowcast dispersion over the environment-implied variance; never divide by the sample variance of a slow
   consensus series without the finite-sample correction."
No change to §0 or the core is implied.

## Referee addendum (NOISE-PROXY-REFEREE, pick 22, 15 Nov ~5:20 PM ET; `reviews/night2/NOISE_PROXY_REFEREE.md`)
PASS-WITH-FIXES; the text above is left as run. Fixes: (F1) RSLGOV's K̂_L0w is not identified (consensus nowcast variance favours
neither branch, leans upper, where β^G ≈ 7), so S-1 reads "2.5–6× on UNEMP, HOUSING, TBILL; RSLGOV branch-ambiguous" (post hoc).
(F2) L0w was validated on K ∈ [0.01, 1]; UNEMP, TBILL, TBOND are below it (estimator re-checked to K = 0.001 by the referee, bias
≈ −0.07 in log; environment refit not re-checked). (F3) Erratum: G is ≥ 3 null SDs in **5** of 7 (UNEMP 2.4), not 6; T1 verdicts
unchanged. A common public signal does not reproduce G > 0 or β̂ > β^G (it pushes both the other way).
