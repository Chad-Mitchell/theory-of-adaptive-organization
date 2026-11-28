# RESULTS — LFK-ALPHA-SPF (SPF forecasters vs the optimal noisy filter of each variable's measured spectrum)

Executor `lfk-spf` (for Ace; Chad t1914), Sunday 15 Nov 2026, ~09:28–10:20 AM ET. Locked prereg: `PREREG.md`, commit `b2a17f7`
(09:51 ET), before any outcome. Environment stage committed separately (`0cd59e5`) before the outcome stage. One post-lock code fix
(`8f11d67`): a NameError in the secondary S1/S2 block (a pre-lock comment had swallowed `lt = …`); no logic changed.
Labels per THEORY v1.4: this is a first, underpowered probe of **N13** (measured-input optimality) using the **KNOWN** bandwidth
relation τ ∝ (N/q)^{1/α} (**N11**, PRIOR ART: Afterman et al. 2022; Kleptsyna et al. 2020; α = 2: Mora & Nemenman 2019).
Its τ_E form (P-LFKα) is reported only as secondary S1, a test of the fixed-variance assumption.

## Verdict
**Primary: INCONCLUSIVE (fewer than 8 variables passed the gates; n = 6).** This was the expected outcome. The pre-lock dry run on
synthetic truth had already shown that the design fails MV8 (power) at SPF sample sizes (PREREG §7). Tier 3. **No CLAIM_MAP status
changes.** α-specific sub-verdict: inconclusive (CI of MAE_G − MAE_M = [−1.40, +0.29]). Nothing is claimed as passed or failed.

## What happened, in order
1. **Gates (environment only, before outcomes):** 7 of 21 candidates passed E1–E3. Excluded: EMP, BAABOND, CORECPI, PCE and COREPCE
   (fewer than 80 surveys before 2020); NGDP, PGDP, CPI, CORECPI, PCE and COREPCE (corner time at the 5,000-quarter bound: no corner
   inside 1960–2019, slopes α̂ 1.1–1.8); CPROF, RGDP, RCONSUM, RNRESIN, RRESINV and RFEDGOV (α̂ at the bound 6: quarterly growth rates
   are mostly white noise plus a corner of about one quarter, so the slope above the crossover cannot be seen at quarterly resolution).
   E4 (β̂ SE ≤ 0.5) then removed INDPROD (0.51).
2. **Regime (THEORY §2.5 rule):** every included variable has a measured corner τ̂_E of 5–46 quarters and α̂ of 2.2–3.9 (regime: smooth
   above the corner, α > 2, for the three level series UNEMP, HOUSING and TBILL; α ≈ 2.3 for the yields). The excluded inflation and
   nominal-GDP series look scale-free over the whole sample (no corner; α̂ 1.1–1.7). That is an environment fact, not a test.
3. **Per variable** (consensus CG β̂ with NW SE; predictions; `results/outcome.json`):

| Var | β̂ (SE) | GTAO / optimal filter β^G | static R-S | α = 2 R-M | K̂ | τ̂_E, α̂, φ̂ |
|---|---|---|---|---|---|---|
| UNEMP | 0.82 (0.23) | 0.67 | 0.045 | 8.1 | 0.027 | 5.3, 3.85, 0.00 |
| HOUSING | 1.47 (0.29) | 1.22 | 0.12 | 2.7 | 0.21 | 6.1, 3.14, 0.01 |
| TBILL | 0.62 (0.18) | 0.62 | 0.031 | 2.9 | 0.045 | 17.1, 2.36, 0.00 |
| BOND (Aaa) | −0.02 (0.23) | 2.82 | 0.046 | 6.6 | 0.27 | 46.2, 2.36, 0.00 |
| TBOND (10y) | −0.07 (0.15) | 2.83 | 0.059 | 8.3 | 0.35 | 40.6, 2.27, 0.00 |
| RSLGOV | 0.60 (0.47) | 7.6 | 1.6 | 8.1 | 11.3 | 15.4, 2.21, 0.59 |

   Mean |ln error|: GTAO 2.14, static 1.89, α = 2 3.15, leave-one-out null 1.36. Calibration slope −0.81 (CI −2.19 to 0.96). Every
   bootstrap CI of a difference includes 0.
4. **Secondary S1 (τ_E-only slope, a test of the fixed-variance assumption):** slope of ln β̂ on ln τ̂_E = −1.93 (CI −3.57 to −0.38).
   That is below every candidate: 1−1/ᾱ = 0.61, LFK ½, §2.2's old 1, fixed-q 0. It is driven by the two long yields, and it is not
   robust: the full sample through 2026 gives +0.26 (CI −2.06 to 1.49), and pre-1990 environment fits give −0.08. No verdict (locked as
   secondary). Plain reading: on this panel the forecasters' memory does not scale with τ_E at fixed variance. That is what the
   referee's re-scoping expects, but n = 6 cannot establish it.
5. **Secondary S2 (how noise scales):** slope of ln K̂ on ln q̂ = −0.62 (CI −4.0 to 2.9). It cannot tell "noise ∝ variance" (0) from
   "noise ∝ short-timescale volatility" (1).
6. **Robustness (point values; all INCONCLUSIVE, n = 6):** R1, full sample through 2026: UNEMP's β̂ flips to −0.09 (COVID quarters);
   MAE_G 2.72. R2, SD instead of IQR dispersion: MAE_G 2.30, and the UNEMP, HOUSING and TBILL predictions move to 0.84, 1.67 and 0.71.
   R3, pre-1990 environment: MAE_G 2.48. In every variant the α = 2 rival has the largest error (3.15–3.73).

## Surprises (read per QUEUE rule 4; all POST HOC, none is evidence)
- **S-a (largest).** For the three non-financial level series with precise β̂ (UNEMP, HOUSING, TBILL), the optimal-filter prediction lands
  within 0–25% of the observed consensus CG coefficient (0.67 vs 0.82, 1.22 vs 1.47, 0.62 vs 0.62). The α = 2 (Markov) version of the
  same model is 2–10× too high, and static noisy information is 10–20× too low. This was not predicted for these three, and n = 3, so it
  counts for nothing yet. It is the reason to build a powered version (new item SPF-AQN-POWERED).
- **S-b.** For the long yields (Aaa, 10-year), β̂ ≈ 0 while the filter, fed the forecasters' dispersion as noise, predicts about 2.8. A
  likely reading: forecasters observe market yields almost exactly, so their dispersion is model heterogeneity, not signal noise (MV2
  for priced variables). That is a measurement-validity issue with the noise proxy, not a fact about tracking. New item SPF-NOISE-PROXY.
- **S-c.** Real-activity growth rates at quarterly resolution are α-unidentifiable (α̂ at the bound in 6 of 6). Any test of α near a
  forecaster's crossover needs monthly or higher-frequency series (or a controlled lab DGP).
- **S-d.** UNEMP's β̂ is fragile to 2020–21 (0.82 → −0.09). Pre-COVID sampling was locked, so the primary is unaffected.

## Validity (FRAMEWORK §2.2), as run
MV1 yes. MV2 partial, and worse than assumed for priced variables (S-b). MV3 yes. MV4 yes. MV5 no. MV6 partial. MV7 in-model yes (AR(1)
exact; instrument slope → 1−1/α at fixed variance; ≈ 0 at fixed q). MV8 **fails** (pre-lock dry run; realized n = 6). MV9: git lock, code,
raw sha256, synthetic dry run; one post-lock mechanical fix, disclosed. Tier 3.

## What this changes
Nothing in CLAIM_MAP. N13 stays OPEN, N11 stays PRIOR ART. The queue gains SPF-AQN-POWERED, SPF-NOISE-PROXY and LAB-AKLMT-TAU (lab
forecasts of AR(1) series with set persistence; Afrouzi et al. 2023 replication data, doi 10.7910/dvn/3q6bhc), which can test the
fixed-variance τ_E slope on a known DGP. VIX-KERNEL (optional in the brief) was not run.
