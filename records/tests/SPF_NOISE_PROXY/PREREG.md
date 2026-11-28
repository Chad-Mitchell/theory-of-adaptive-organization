# PREREG — SPF-NOISE-PROXY: an independent sensing-noise (N) proxy for SPF forecasters, and a premise check of the old one

Locked by executor `queue-pick4` (for Ace; Chad t1914), Sunday 15 Nov 2026, America/New_York, on branch `spf-noise-proxy`.
The lock is the git commit that adds this file. Queue: post-protocol pick 4, uniform slot (ledger 26 unaided order, 27 rule_rank,
28 pick). No real SPF dispersion at any horizon other than LFK-ALPHA-SPF's h = 3 (already published in `tests/LFK_SPF/`)
had been computed when this file was committed; `build_micro.py` was code-tested only on CPROF (not one of the 7 variables)
and `analysis.py` only on synthetic fake files. **Seen before lock** (all from LFK-ALPHA-SPF): the h = 3 dispersion-based
K̂ values, every consensus CG coefficient β̂, the environment fits, the survey counts. So S4 below is POST HOC by construction.

## 0. Source in THEORY.md v1.4.1, regime, and what is (not) being tested
- **Section:** §2.2 Regime B table, row "Memory time (filter bandwidth)": "τ ∝ (N/q)^{1/α} | white observation noise; α > 1 |
  KNOWN (Wiener/Kalman bandwidth; Afterman et al. 2022; Kleptsyna et al. 2020)", and row "Error under noisy continuous sensing"
  (premise "white observation noise of density N"). §2.1: "Three quantities set the tracking optimum in time: the slope α, the
  high-frequency drift level q …, and the sensing noise N". §2.5 binding rule: premises (here: white observation noise) are
  checked before a result is applied. §1 N6 / CLAIM_MAP N13 (the open bet) needs N measured on the same system.
- **Regime per variable** (from LFK-ALPHA-SPF's environment stage, Whittle Matérn+white fit on 1960Q1–2019Q4, label A if the 95%
  parametric-bootstrap interval of α contains 2): UNEMP B (α̂ 3.85 [2.81, 5.03]), HOUSING B (3.14 [2.25, 4.69]), TBILL B (2.36
  [2.05, 3.23]), BOND B (2.36 [2.08, 3.11]), TBOND B (2.27 [2.04, 2.99]), RSLGOV A by the rule (2.21 [1.09, 6.0]; α effectively
  unidentified), INDPROD A by the rule (3.28 [1.69, 6.0]; unidentified). The K-inversion uses each variable's own fitted spectrum,
  so no common regime is assumed. UNEMP and HOUSING have α̂ > 3, outside the fBm range of some §2.2 rows; the memory-time row
  needs only α > 1.
- **This is a measurement-validity item (FRAMEWORK MV2, MV7, MV8), not a test of a GTAO prediction.** Nothing here can change
  N13's status. What it can do: (i) supply an N proxy validated on synthetic truth; (ii) test, on real data, the white-noise premise
  that LFK-ALPHA-SPF assumed when it read h = 3 dispersion as N. A failure of (ii) is "the premise failed on proxy …", not a
  failure of the theory.
- **Adjustment lag:** not applicable (no intervention or change in inputs is studied).
- **Prior art.** The horizon logic of T1 is **Patton & Timmermann 2010** (J. Monetary Econ. 57(7):803–820, "Why do forecasters
  disagree? Lessons from the term structure of cross-sectional dispersion"; abstract read this session, doi
  10.1016/j.jmoneco.2010.07.001): signal-noise heterogeneity matters most at short horizons, prior/model heterogeneity at long ones;
  they find for GDP growth and inflation that heterogeneity in priors or models, not information, dominates dispersion, and that
  individual differences persist. So T1 and the fixed-effect removal in L0w are applications of known ideas. Dispersion as
  noisy-information noise: Coibion & Gorodnichenko 2012 (JPE) and 2015 (AER), as recalled, not re-opened. Given Patton &
  Timmermann, rejections in T1 may be broad, not only in the priced group. Increment here: the finite-sample variance bias of the
  D/vf proxy for slow series (§1.1), the level-normalised within-forecaster nowcast proxy validated on synthetic truth, and its use
  for the N of THEORY §2.2.

## 1. Pre-lock findings from the synthetic dry run (`synth_dryrun.py`, `results/synth_dryrun.out`; 20 panels × 7 worlds × 6 arms)
Worlds = the 7 LFK environments (E1–E3 passers) with their survey counts; environment re-fitted by Whittle inside every panel.
1. **The LFK proxy is biased upward even when its premise holds.** P0 (h = 3 dispersion over the *sample* variance of the consensus,
   inverted with the *population* variance of the model) has median ln(K̂/K) = +0.88 (BOND) and +1.65 (TBOND) under pure noise,
   because 108–136 quarters of a slow series (corner 40–46 quarters) under-state its variance (`common.moments_T` gives the exact
   expected sample variance; checked against simulation). Under any contamination arm P0 is +1.2 to +2.3 in log. This bias is in
   the same direction as LFK's S-b anomaly (yields' predicted β ≈ 2.8 vs β̂ ≈ 0); how much of S-b it explains is S4.
2. **Selection rule (locked in `synth_dryrun.summarize`, applied before any real data):** a candidate is admissible if, under pure
   noise, its median |ln K̂/K| ≤ 0.35 and |median signed| ≤ 0.25; choose the admissible candidate with the smallest worst-arm
   median |ln K̂/K| over the contamination arms (fixed individual bias λ = 1, 3; AR(1) individual bias λ = 1, 3; heterogeneous
   dynamics). Result: **L0w** — the *within-forecaster* (forecaster fixed effects removed) robust dispersion of **current-quarter
   (h = 0) nowcasts**, normalised by the environment-implied population variance of x and inverted on the lower branch of
   K(1−1/n)·mean|H₀|². Arm a: 0.33 (signed −0.17); worst contaminated arm 0.35. L0 (raw nowcast dispersion) was also admissible
   (0.31; worst 0.49). Not admissible: P0T (finite-sample-corrected h = 3; worst 1.86), P1T (corrected h = 0, D/vf; arm a 0.39),
   L3 (level-normalised h = 3; arm a 0.62, worst 2.22).
3. **Overidentification statistic.** G = ln K̂_L3 − ln K̂_L0 (same environment fit; pure noise: G ≈ 0, contamination growing with
   horizon: G > 0). A naive survey block-bootstrap CI over-rejects badly under pure noise (CI > 0 in 56% of arm-a panels), so the
   locked test uses a **parametric bootstrap under H0** (`gtest.py`): simulate pure-noise panels from the fitted environment with
   K = K̂_L0, the observed T and panel size, re-fit the environment each time; one-sided p = (1 + #{G_sim ≥ G_obs})/(1 + NSIM).
   Size and power on synthetic truth (`synth_size.py`, worlds UNEMP/TBILL/TBOND, 10 panels × 60 null sims each):
   **size 0/30 rejections at p < 0.05 and at p < 0.10** under pure noise (conservative); **power 16/30 (53%) at p < 0.05**
   (70% at p < 0.10) under fixed individual bias λ = 1 (UNEMP 70%, TBILL 60%, TBOND 30%; the slow, short TBOND panel is weakest).
   With 60 null sims the smallest attainable p was 0.016; the real run uses 200. Holm over 7 lowers per-variable power further,
   so a T1 "not rejected" is weak evidence for the premise, especially for TBOND and BOND.

## 2. Data
SPF microdata (`SPFmicrodata.xlsx`, Philadelphia Fed; box copy `<local>/lfk_spf/`, sha256 in `tests/LFK_SPF/data/RAW_SHA256.txt`),
columns VAR2–VAR6 = quarters t … t+4; growth variables (RSLGOV, INDPROD) as annualised q/q growth of the same forecaster's levels;
surveys with t+3 ≤ 2019Q4 (LFK sample); per-survey statistics only for surveys with ≥ 10 forecasters at that horizon; within-
forecaster dispersion uses forecasters with ≥ 8 surveys at that horizon. Environment: LFK `target_<VAR>.csv` 1960Q1–2019Q4 and
`env.json` fits and 100 parametric draws. Variables: the 7 LFK E1–E3 passers (UNEMP, HOUSING, TBILL, BOND, TBOND, RSLGOV,
INDPROD). Groups fixed now: **priced** = TBILL, BOND, TBOND (market rates observed daily); **non-priced** = UNEMP, HOUSING,
RSLGOV, INDPROD (statistical releases with lags).

## 3. Locked analysis (`analysis.py`; seeds 20261115+42+i for variable i in the order above; NSIM 200; B 500; block 8)
Per variable: K̂ for every candidate; **K̂_L0w** with a 95% CI (circular block bootstrap over surveys × the 100 parametric
environment draws, cycled); N̂ = K̂·var_x in data units; memory scale (K̂/q̂)^{1/α̂} (§2.2 memory-time row, in quarters, same
convention as LFK); G and its parametric p; Holm adjustment over the 7.

**Hypotheses and decision rules (proxy "SPF individual-forecast dispersion by horizon, latest-vintage environment"):**
- **T1 (premise check of LFK's N):** per variable, if Holm p(G) < 0.05: "white-noise premise of h = 3 dispersion as N **failed
  on proxy 'horizon overidentification'** for V"; if raw p ≥ 0.10: "not rejected" (with the dry-run power stated); else
  inconclusive. Prediction (from LFK S-b, not from THEORY): rejections, if any, concentrate in the priced group.
- **T2 (known groups for contamination):** d = mean over priced of (G − G_null mean) minus mean over non-priced; one-sided z with the
  null SDs, and the exact permutation p over all 35 three-vs-four splits (minimum attainable 1/35 ≈ 0.029). Predicted d > 0.
  "Supported" iff z-p < 0.05 **and** permutation p ≤ 0.06; "contradicted" iff d < 0 with permutation p ≥ 0.94; else inconclusive.
- **T3 (known groups for the new proxy, MV7 on real data):** mean ln K̂_L0w of non-priced minus priced > 0 (priced variables'
  current quarter is largely observed by the survey deadline). Permutation p over 35 splits; "passed known-groups" iff p ≤ 0.06,
  "failed known-groups" iff the difference is ≤ 0, else inconclusive.
- **S4 (POST HOC, β̂ seen; no verdict, cannot count as evidence):** the LFK six (E4 passers): β^G recomputed with K̂_L0w (and
  L0, P0) in place of LFK's K̂; mean |ln β̂ − ln β^G| vs LFK's 2.14, static 1.89, null 1.36. **Locked numeric expectation
  (about unseen h = 0 dispersion data):** β^G(K̂_L0w) < 0.5 for BOND and for TBOND (vs LFK's 2.82, 2.83).
- **Robustness (no verdict):** SD instead of IQR within dispersion; L0 instead of L0w.

## 4. Validity (FRAMEWORK §2.2), stated before outcomes
MV1 named (§2). MV2: improved over LFK (fixed effects removed; current-quarter target) but not complete: time-varying model
heterogeneity that is not persistent within forecaster still enters; partial in-quarter observation of the target is not
modelled (the model gives every horizon the same white K). MV3 yes (N from dispersion and the environment only; no β̂ used).
MV5 no (one method). MV6 partial (contamination arms). MV7 in-model yes (§1.2); on real data T3. MV8: synthetic recovery
within ~0.35 in log; T1/T2 power as §1.3; T2/T3 have only 7 variables (minimum permutation p 0.029). MV9: git lock, code,
seeds, raw sha256; not externally timestamped (waived). **No CLAIM_MAP status may change from this item.**

## 5. Files
`common.py`, `synth_dryrun.py`, `gtest.py`, `synth_size.py`, `build_micro.py`, `analysis.py`; results in `results/`.
Run order after lock: `python3 build_micro.py && nice -n 19 python3 analysis.py`.
