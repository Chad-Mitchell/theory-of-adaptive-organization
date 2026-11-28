# DECISIVE / populations — preregistration (D3, population scale)

Written Sat 2026-11-14, ~23:05 ET, by a Grok Bot executor for Chad (via Ace). Committed and sha256-hashed before second-block crossings are counted. Theory: `attack/math/MATH_ATTACK.md` §2.1(c), §2.2 class C (OU/Kramers), §2.6, §5 D3.

## What was seen before this commit (disclosure)
- GPDD metadata tables and first-block predictor statistics; power simulation.
- **One aggregate leak, recorded:** while counting eligible series I printed the number of long annual series with no zero counts over the *whole* series (336 of 421). This touches second-block information in aggregate (zeros are below threshold). It was not used for any choice below except that the rule "no zeros in the first block" was already in the code; no per-series outcome was inspected.
- The second block was saved to `data/outcome_block.csv` but no crossings were counted.

## Data
- **Global Population Dynamics Database** (NERC Centre for Population Biology, 2010), official CSVs from KNB doi:10.5063/F1BZ63Z8 (`data/knb/`). KNB public; GPDD terms ask for citation. (Living Planet Index not used.)
- Selection: annual sampling (SamplingFrequency = 1), DatasetLength ≥ 40, ≥ 40 observed points with ≥ 90% of years present, units not harvest/kill/catch/pelt/biomass/infection-based, all Reliability levels (≥ 2 is sensitivity S2; most long series are Reliability 1), first block strictly positive and non-constant, ≥ 19 first-block points, ≥ 15 second-block points. n = 274 series, 31 data sources (205 Mammalia, 34 Aves, 24 Osteichthyes, 10 Insecta).

## Split and measures
- Split at the midpoint year; 1-year gap.
- **First block:** x = ln N; s = SD(x); φ = Kendall-corrected AR(1) on consecutive-year pairs about the block mean, clipped [0.05, 0.95]; **τ = −1/ln φ years (primary)**; τ_ss from a state-space Gompertz (AR(1) + observation noise, Kalman MLE) is sensitivity S1.
  - **Deviation from MATH_ATTACK (declared now):** MATH_ATTACK made the state-space fit primary. With ~20–30 first-block points the observation-error variance is weakly identified; OLS-BC is primary, state-space must agree in sign.
- Quasi-extinction line = first-block geometric mean ÷ 5, so **B = ln 5 for every series**; z = B/(s√2); σ = s√(2/τ).
- Density-independent drift μ, σ² from first-block log increments (Dennis et al. 1991).
- **Second block (outcome):** number of downcrossings of the line (zeros count as below), exposure = adjacent observed year pairs; also "any crossing" for the Dennis comparison.

## Theory-implied values (fixed before outcomes)
- Continuous-time literal: fixed-spread slope −1; at fixed σ, β_τ = β_σ/2 − 1.
- **Annual sampling correction:** median τ ≈ 3 years and 16% of series have τ < 1 year, so the continuous law does not apply directly. Simulating each series as a sampled OU (its own φ, s, second-block length) gives **β\*_M1 = −0.34** (fixed spread) and, at fixed σ, **β_τ = +0.70, β_σ = +1.97** (`power.py`). These are the primary targets; the literal −1 is also reported.

## Models (Poisson, offset ln exposure, SEs clustered by data source)
- **P1 (primary):** y ~ ln τ + spline(z, 3 df). Prediction slope = β\* = −0.34.
- **P2:** y ~ ln τ + ln σ. Prediction β_τ > 0 (implied +0.70).
- **P3:** ln τ × standardized z, predicted positive.
- **P4 collapse:** ln(rate·τ) vs z, class offsets (Aves, Osteichthyes, Insecta vs Mammalia); collapse holds if all |offset| < 0.3.
- **P5 baselines:** static spread only (spline z) vs + ln τ (ΔAIC); Dennis density-independent probability of reaching the line in T2 (logit) vs + ln τ + ln s (LR, ΔAIC). Both baselines predict no τ effect.
- Cold regime z ≥ 1.5 (n = 140): P1 and P2 refit.
- Sensitivities: S1 state-space τ; S2 Reliability ≥ 2; S3 negative binomial; S4 + first-block trend; S5 drop clipped φ. Permutation null: τ shuffled within z-quintiles (2,000×), one-sided p.

## Hit / kill
- **HIT:** P1 95% CI < 0 and contains β\*.
- **SIGN-RIGHT, SIZE-OFF:** CI < 0, excludes β\*.
- **KILL (population scale):** P1 point estimate closer to 0 than to β\* AND CI excludes β\*; or (MATH_ATTACK joint rule) in z ≥ 1.5, P2 β_τ ≤ 0 with upper CI < 0.2.
- Otherwise INCONCLUSIVE.

## Power (`power_output.txt`)
- Under the sampled-OU theory: ~0.7 downcrossings per series; β\* = −0.34 (SD across simulations 0.05), P(CI excludes 0) ≈ 1.0, P(false kill) ≈ 0. Optimistic: no extra heterogeneity, catastrophes or trends. Cold-subset SE ≈ 0.13.

## Circularity guards
1. τ and s from the first block; outcome from the second, after a 1-year gap; the line is fixed from first-block data.
2. Permutation null within z-quintiles.
3. Trend control (S4): declining populations cross more irrespective of τ.
4. Honest limit: as with glucose, "fewer crossings per unit time for slower return at fixed spread" is a generic property of single-time-scale stationary processes, so a hit is necessary, not sufficient, evidence for the theory; the population test is distinctive mainly via the Dennis comparison and the collapse.

## Files
`code/features.py`, `code/power.py`, `code/analyze.py` (outcome analysis, written before outcomes).
