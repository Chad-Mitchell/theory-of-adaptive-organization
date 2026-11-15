# DECISIVE / banks — preregistration (D1, firm scale)

Written Sat 2026-11-14, ~22:55 ET, by a Grok Bot executor for Chad (via Ace). Committed and sha256-hashed before any outcome (failure) data are joined to predictors. Source theory: `/workspace/gtao/attack/math/MATH_ATTACK.md` §2.1, §2.3, §2.6, §5 D1. Lessons from C3 (`tests/C3/RESULTS.md`): B must be a stock, σ an innovation, τ pre-measured and not chosen in response to the outcome; report the continuous and incident versions of the identity.

## What was seen before this commit (disclosure)
- FDIC BankFind `financials` 2001Q1–2007Q4 for all FDIC-insured institutions (predictor block only), summary stats and power simulation (`power_output.txt`).
- Two rows of the FDIC failures API (a 1934 failure) while checking the endpoint. No 2008–2014 failure record was looked at or joined.
- General background knowledge that roughly 500 US banks failed 2008–2014 (used only to size the power simulation).

## Data
- Predictors: FDIC BankFind Suite API (`api.fdic.gov/banks/financials`), quarterly Call Report aggregates 2001Q1–2007Q4 (`data/financials_2001_2007.csv`). Public US-government data. **Substitution note:** the brief named FFIEC CDR bulk call reports *or* FDIC BankFind; BankFind was used (same Call Report source, API-accessible).
- Outcome: FDIC failed-bank records (`api.fdic.gov/banks/failures`), RESTYPE = FAILURE, FAILDATE 2008-01-01 … 2014-12-31, matched by CERT.
- Sample: institutions filing at 2007Q4 with ≥20 quarterly filings in 2001–2007, assets > 0, B > 0, σ > 0, τ defined. n = 7,837 (predictor-only count).

## Measures (all from 2001Q1–2007Q4)
- **B (stock, % of assets)** = equity/assets at 2007Q4 − 2 (the critically-undercapitalized line).
- **σ (innovation, % of assets per quarter)** = SD of quarterly ROA (quarterly net income from YTD differences ÷ average assets).
- **τ (quarters, primary)** = −1/ln φ, φ = Kendall-bias-corrected AR(1) coefficient of the capital ratio's deviation from its own **linear trend**, clipped to [0.05, 0.95].
  - **Deviation from MATH_ATTACK spec (declared before outcomes):** MATH_ATTACK said "deviation from own mean". Predictor diagnostics showed 36.7% of banks hit the φ = 0.95 clip with own-mean deviations (trend growth masquerading as slow correction). Detrended τ is primary; own-mean τ is sensitivity S2.
- z = B/(σ√τ). Median z is very large (≈29 with own-mean τ), i.e. by historical σ every bank is deep in the "cold" regime. **This means 2008–2014 failures are, by construction, driven by a shock far outside the 2001–2007 σ (a common jump).** The theory itself (§2.3) then predicts a *reduced* τ effect (single-jump limit ε_τ → 0). Stated up front.

## Models (complementary log-log on failure within 2008–2014 ≈ hazard elasticities for rare events)
- **P1 (primary):** fail ~ ln σ + ln B + ln τ. Prediction β_τ > 0 (one-sided α = 0.05; 95% CI reported).
- **Identity checks (Wald):** β_B = −β_σ; continuous identity β_τ = β_σ/2 − 1; incident identity β_τ = β_σ/2. Reported, not decisive.
- **P2:** r_τ = β_τ/β_σ in the top tercile of z, bootstrap 95% CI (1,000). Theory band [0.19, 0.5].
- **P3:** add ln τ × standardized ln z. Prediction **positive** (τ matters more in well-capitalized banks). A "slow banks die when weak" story predicts negative.
- **P4:** ln[B/(σ√τ_i)] vs ln[B/(σ·√4)] (fixed one-year horizon) as single predictor; prediction ΔAIC > 10 favoring τ_i.
- **Baseline (Boyd–Graham Z-score)** Z = (E/A + mean ROA)/σ_ROA: fail ~ ln Z vs ln Z + ln τ; LR test, ΔAIC, AUC. Z-score predicts β_τ|Z = 0.
- **Jump-share check:** among failed banks, share with any single quarter (2008→failure) loss > B (and > B/2), and median max-quarter-loss/σ.
- Sensitivities (non-decisive): S1 + ln assets; S2 own-mean τ; S3 τ from ROA AR(1); S4 logit; S5 σ = capital-ratio AR innovation SD.

## Nulls, hit and kill
- Null: β_τ = 0 given σ and B (static Z-score world).
- **HIT:** P1 95% CI excludes 0 on the positive side AND P3 point estimate > 0.
- **KILL (firm scale, MATH_ATTACK joint-kill rule):** in the z ≥ 1.5 subset, β_τ ≤ 0 AND its 95% upper bound < 0.2.
- **SIGN-WRONG:** P1 CI entirely < 0 (without meeting kill) — reported as a miss.
- Otherwise INCONCLUSIVE.
- Interpretation rule fixed now: if KILL fires AND the jump-share check shows most failures had a single-quarter loss > B/2, report "τ term absent, consistent with the single-jump limit the theory allows" — that is still a miss for the τ term at this scale, not a rescue.

## Power (predictor-only simulation, `code/power.py`, `power_output.txt`)
- With 300–500 failures and the observed SD of ln τ (1.08): power ≈ 0.61–0.76 for β_τ = 0.1, ≈ 0.99–1.00 for β_τ = 0.2 (one-sided 5%). Ignores measurement error in τ (28 quarterly points), which attenuates; true power is lower.

## Circularity / endogeneity guards
- τ and σ come from 2001–2007 capital and income; the outcome is a regulator's failure decision 2008–2014. No shared measurement.
- Endogeneity remains: banks choose capital policy (MATH_ATTACK §2.5 point 5); big-buffer banks may tolerate slow correction (biases β_τ toward 0). Not fixable here; stated.

## Files
`code/pull_predictors.py`, `code/predictors.py`, `code/power.py`, `code/analyze.py` (outcome analysis, written before outcomes), `code/sklearn_free_auc.py`.
