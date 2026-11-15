# DECISIVE / populations — results (population scale)

Prereg: `PREREG.md` (sha256 e6dd7aa6…, git commit 2b12786, 2026-11-14 22:53 ET, before crossings were counted). Raw: `results.json`, `exploratory.json`. **Not independently reviewed.**

## Data
- GPDD (KNB official CSVs): 274 annual series ≥ 40 years long, from 31 data sources.
- 238 quasi-extinction downcrossings in the second blocks; 107 series had at least one.

## Preregistered results (Poisson, SEs clustered by source; 95% CI)

| Prediction | Result | Met? |
|---|---|---|
| **P1 fixed-spread slope on ln τ** (literal theory −1; annual-sampling-corrected β\* = −0.34; static CV and Dennis predict 0) | **−0.21 [−0.37, −0.05]**; permutation p (τ shuffled within z-quintiles) = 0.006 | yes vs β\*; no vs −1 |
| P2 at fixed σ: β_τ > 0 (implied +0.70), β_σ (implied +1.97) | +0.20 [−0.04, 0.44]; +0.80 [0.49, 1.11] | sign right, smaller, not significant |
| P3 ln τ × z > 0 | +0.20 [−0.05, 0.46] | point right, not significant |
| Cold regime (z ≥ 1.5, n = 140, 82 events): fixed-spread slope | +0.10 [−0.29, 0.49] | **not seen in the cold regime** |
| Cold regime β_τ\|σ (kill rule) | +0.67 [0.12, 1.23] | kill does not fire |
| P4 collapse across classes (offsets vs Mammalia; threshold \|offset\| < 0.3) | Aves +0.24; Insecta +0.58; Osteichthyes −1.70 | **fails** |
| P5a: τ adds to static spread | ΔAIC = 15 | yes |
| P5b: τ adds to the Dennis density-independent model (any crossing) | β_τ = +0.08 [−0.14, 0.30], LR p = 0.50 | **no** |

**Verdicts:**
- Prereg primary (sampling-corrected): **HIT** (CI < 0 and contains β\*).
- **Literal −1 rule: KILL** (the estimate is closer to 0 than to −1, and the CI excludes −1).

## Sensitivities

| Sensitivity | Slope [95% CI] |
|---|---|
| S1 state-space τ | −0.31 [−0.52, −0.10] |
| S3 negative binomial | −0.16 [−0.30, −0.01] |
| S4 + trend | −0.26 [−0.39, −0.13] |
| **S5 drop clipped φ** | **−0.09 [−0.36, 0.17], not significant** |
| S2 Reliability ≥ 2 | n < 40, not run |

The effect leans on series whose φ hit the clip: the fastest-returning quintile has the highest crossing rate.

## Post-hoc problem found
- Data source 12 (Novak et al. 1987, "Furbearer harvests in North America") supplies **138 of the 274 series**. Its units say "All Individuals", so the preregistered unit filter missed that these are harvest records.
- Exploratory checks:
  - without source 12: −0.26 [−0.52, −0.01];
  - source 12 alone: −0.20 [−0.34, −0.05];
  - one series per taxon (n = 77): −0.29 [−0.63, 0.05].

## Caveats
- Annual sampling against a median τ of about 3 years compresses the 1/τ law. The −0.34 target is a model-derived correction set before outcomes, and a sceptic may call it softening.
- The cold-regime fixed-spread slope is null.
- τ does not beat the classical density-independent model on "any crossing".
- The collapse fails.
- Clustering is heavy: half the series come from one harvest source.
