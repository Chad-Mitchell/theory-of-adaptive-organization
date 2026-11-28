# DECISIVE / banks — results (firm scale)

Prereg: `PREREG.md` (sha256 b7ea310e…, git commit 2b12786, 2026-11-14 22:53 ET, before any 2008–2014 failure record was joined). Raw: `results.json`, `exploratory.json`. **Not independently reviewed.**

## Data
- 7,837 FDIC-insured institutions (2001Q1–2007Q4 Call Report aggregates via the FDIC BankFind API).
- 419 failures in 2008–2014 matched. The FDIC list has 507 failures in that window; the other 88 are banks outside the sample (mostly too young for 20 quarters, or not filing at 2007Q4). Young de novo banks, which failed often, are therefore excluded.

## Preregistered results (cloglog; coefficient = elasticity of failure hazard; 95% CI)

| Prediction | Result | Met? |
|---|---|---|
| P1: β_lnτ > 0 given σ, B | **+0.20 [0.11, 0.29]**, one-sided p = 7e-6. Doubling τ → about 15% higher failure hazard | **yes** |
| β_σ / β_B | +0.62 [0.52, 0.72] / −1.18 [−1.41, −0.94] | signs right |
| ε_B = −ε_σ | rejected (p = 1e-5); the buffer matters about 2× more than σ | no |
| Continuous identity β_τ = β_σ/2 − 1 (= −0.69) | rejected (p ≈ 1e-64) | no |
| Incident identity β_τ = β_σ/2 (= 0.31) | 0.20 vs 0.31, p = 0.04 | roughly |
| P2: r_τ in [0.19, 0.5] (top z tercile) | 0.55, bootstrap CI [−1.6, 4.2] (only 41 failures) | uninformative; full-sample r_τ = 0.33 |
| P3: ln τ × ln z > 0 | +0.05 [−0.03, 0.13] | point right, not significant |
| P4: bank-specific √τ horizon beats a fixed 1-yr horizon by ΔAIC > 10 | ΔAIC = 7.1 | no |
| Baseline: τ adds to the Boyd–Graham Z-score | β_τ\|Z = +0.19 [0.10, 0.28], LR p = 3e-5, ΔAIC = 15. AUC 0.709 → 0.718 (theory model 0.732) | **yes** |
| Kill rule (z ≥ 1.5: β_τ ≤ 0 and upper CI < 0.2) | +0.22 [0.13, 0.31] | does not fire |

**Verdict under the prereg: HIT** (P1 met, P3 point estimate > 0).

## Sensitivities (preregistered)

| Sensitivity | β_τ [95% CI] |
|---|---|
| S1 + size | +0.17 [0.08, 0.26] |
| **S2 τ from own-mean deviations** | **+0.06 [−0.03, 0.15], not significant** |
| S3 τ from ROA AR(1) | +0.29 [0.22, 0.36] |
| S4 logit | +0.22 [0.12, 0.31] |
| S5 σ = capital-ratio innovation | +0.23 [0.14, 0.32] |

## Jump-share check
- 9.8% of failed banks had a single quarter with a loss greater than B; 47% had one greater than B/2.
- The median worst quarterly loss was about 21× the bank's 2001–2007 σ.
- So 2008–2014 failures came from a shock far outside the historical σ. That fits the incident-regime identity holding roughly and the continuous one failing.

## Exploratory (not preregistered)
- Adding asset growth, size and mean ROA: β_τ = +0.19 [0.10, 0.28].
- Dropping banks whose φ hit the clip: +0.23 [0.11, 0.35].
- Failure rate by τ quintile, fastest to slowest: 3.3%, 5.4%, 5.7%, 6.3%, 6.1%.
- With both τ definitions in one model: detrended τ +0.33, own-mean τ −0.17. The "τ" that predicts failure is persistence of deviations from a bank's own capital trend, not from its mean.

## Caveats
- The result depends on how τ is defined. The detrended definition was chosen before outcomes, for a stated reason (37% of own-mean fits hit the clip), but the own-mean version that MATH_ATTACK specified is null.
- τ is not exogenous: banks choose capital policy. Persistence of capital deviations could proxy for business model or management.
- The quantitative structure the theory predicts did not hold:
  - ε_B ≠ −ε_σ;
  - the continuous identity is rejected;
  - P4 is not met.

  What holds is the sign and the incident-regime ratio.
- One crisis, one country, one period. There is survivorship from excluding young banks.
