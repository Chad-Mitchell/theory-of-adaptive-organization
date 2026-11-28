# DECISIVE / glucose — preregistration (D2, organism scale)

Written Sat 2026-11-14, ~23:00 ET, by a Grok Bot executor for Chad (via Ace). Committed and sha256-hashed before any outcome (second-block episode count) is computed. Theory: `attack/math/MATH_ATTACK.md` §2.1 corollary (c), §2.6, §5 D2.

## What was seen before this commit (disclosure)
- File structures (column names, 2 rows of two Shanghai files, 2 rows of REPLACE-BG CGM), cohort sizes and recording lengths.
- First-block predictor statistics (`data/predictors.csv`) and the power simulation (`power_output.txt`).
- The second block was split off and saved (`data/outcome_block.parquet`) by `features.py` but **no episode counts, rates, or summaries of it** were computed or looked at.

## Data and licences
- **ShanghaiT1DM/T2DM** (Zhao et al. 2023, Sci. Data 10:35), CC BY 4.0. Figshare blocked this box (HTTP 403 WAF); obtained the authors' `diabetes datasets.zip` from the CC-BY-4.0 Zenodo archive record 18604027 (re-archive of figshare 20444397). Libre, 15-min. 16 T1DM + 109 T2DM recordings (recordings from the same patient are treated as separate units; limitation).
- **REPLACE-BG** (Aleppo et al. 2017, Diabetes Care), Jaeb Center public dataset (public-use release with acknowledgement); same Zenodo record. Dexcom G4, 5-min, 226 adults with T1D, ~26 weeks. **Added beyond the brief** because Shanghai alone is underpowered (below). Labelled clearly as an added cohort, not a substitution.
- **Colas et al. 2019** (PLOS ONE S1 data, CC BY), 5-min, ~2 days, 208 mostly non-diabetic adults at risk; used only in the cross-cohort collapse (P4).
- OhioT1DM not used (requires a data-use agreement; not openly downloadable).

## Split and measures
- Per subject/recording: split at the time midpoint; drop 6 h around the split (cuts autocorrelation leakage, ~2.5 τ); each block needs ≥12 h valid data. Readings outside the sensor range [39, 401] mg/dL dropped.
- **First block (predictors):** mean m, SD s, **τ = 1/e crossing time of the sample ACF** (interpolated, lags ≤ 12 h; primary — glucose ACF is not exponential, lag-1 AR(1) τ is a sensitivity), σ = s√(2/τ), B_hypo = m − 70 mg/dL, B_hyper = 250 − m, z = B/(s√2), LBGI and HBGI (Kovatchev 1998).
- **Second block (outcome):** hypoglycaemia episodes = ≥15 min below 70 mg/dL (≥3 consecutive 5-min or ≥2 consecutive 15-min readings), re-armed after the same duration above; episodes counted within contiguous valid runs. Rate per valid day. Hyper (>250 mg/dL) is secondary.

## Theory-implied values (fixed before outcomes)
- Continuous-time theory at fixed spread s and buffer B: ε_τ = −1 exactly (§2.1c). Any static index (LBGI, SD, CV) predicts 0.
- **Sampling/duration correction:** the ≥15-min rule and sampling interval add a second time scale. Simulating a smooth single-time-scale Gaussian process with each subject's (τ, z, block length) gives a theory-implied fixed-spread slope **β\* = −0.82 (REPLACE-BG)** and **β\* = −0.65 (Shanghai)** (`power.py`). These are the primary targets; the literal −1 is also reported.

## Models (negative binomial, offset ln days, ML dispersion)
- **P1 (primary):** hypo count ~ ln τ + natural spline(z_hypo, 3 df) [+ cohort FE when pooled]. Coefficient on ln τ = fixed-spread slope.
- **P2:** count ~ ln τ + ln σ + ln B. Predictions: β_B = −β_σ; continuous identity β_τ = β_σ/2 − 1 (incident version β_σ/2 also reported). Wald tests.
- **P3:** ln τ × standardized z interaction, predicted **positive**.
- **P4 collapse:** ln(rate·τ) vs z across REPLACE-BG, SH-T1DM, SH-T2DM, Colas: cohort offsets after a common spline; collapse holds if all |offset| < 0.3.
- **P5 baseline:** LBGI (+ LBGI²) vs LBGI + ln τ: LR, ΔAIC; prediction β_τ < 0 given LBGI.
- Cold regime (z ≥ 1.5): P2 β_τ|σ,B reported only if n ≥ 30.

## Hit / kill (evaluated separately for REPLACE-BG [powered, decisive] and Shanghai [named in brief, replication])
- **HIT:** P1 95% CI entirely < 0 and contains β\*.
- **SIGN-RIGHT, SIZE-OFF:** CI < 0 but excludes β\*.
- **KILL (organism scale):** P1 point estimate closer to 0 than to β\* AND CI excludes β\*. (MATH_ATTACK's "closer to 0 than to −1" is also reported.)
- Cold-regime kill (β_τ|σ,B ≤ 0 with upper CI < 0.2) evaluated only if n_cold ≥ 30.
- Otherwise INCONCLUSIVE.

## Power (`power_output.txt`; predictor-only; Gaussian process + lognormal heterogeneity SD 0.5)
- REPLACE-BG: n = 224, ~106 expected episodes/subject, SE(slope) ≈ 0.15, P(CI excludes 0 | theory) ≈ 1.0, P(false kill) ≈ 0.03.
- Shanghai: n = 125, ~4 episodes/recording, SE ≈ 0.19, power ≈ 0.93, **P(false kill) ≈ 0.25** → Shanghai cannot decide alone.
- Caveat: real glucose is skewed and meal/insulin-driven; real SD of ln τ in REPLACE-BG is only 0.225, so this test has a narrow lever arm.

## Circularity guards (τ and outcome both come from the glucose trace)
1. Disjoint blocks with a 6-h gap: τ never sees the outcome period.
2. **G1:** τ recomputed from first-block dynamics with the lower half censored at the median (upper-half dynamics only, no information from the hypo tail). Predicted same sign.
3. **G2:** the circular in-block estimate (τ and episodes from the same block) reported for contrast.
4. **G3:** slope conditional on the first-block episode rate (robustness only; partly over-controls, not a kill).
5. Honest limit stated now: at fixed spread, rate ∝ 1/τ follows from dimensional analysis for *any* stationary single-time-scale process. This test can kill the τ term and beats static indices, but a hit would not by itself show anything specific to adaptive organization.

## Files
`code/load.py`, `code/features.py`, `code/simproc.py`, `code/power.py`, `code/analyze.py` (outcome analysis, written before outcomes).
