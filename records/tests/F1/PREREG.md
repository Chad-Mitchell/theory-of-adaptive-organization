# F1 preregistration: shock × √(time to fix) ÷ buffer, second scale (US public firms)

Written 2026-11-14 (ET), BEFORE any outcome data was pulled. Author: Grok Bot (executor for Ace/Chad).
Data touched before writing: SEC `companyfacts.zip` (XBRL facts; sha256 in raw/companyfacts.sha256), used
ONLY through facts with `filed` ≤ the cohort cutoff (2014-12-31 or 2019-12-31). Predictor distributions and
their reliability were inspected (allowed: no outcome information). Not yet touched: SEC `submissions.zip`
(filing histories, SIC codes, 8-K items), EDGAR full-text search, any post-cutoff fact of a sample firm.
SEC access identity: User-Agent "Looper research research@example.invalid" (accepted by SEC, HTTP 200).

## 0. Claim under test (X_TEXT v9, verbatim)
"Where shocks are large relative to buffers, slow error-fixers fall apart faster than fast ones, with risk
tracking shock size × √(time to fix) ÷ buffer, the form of Merton's distance to default with time to fix as
the horizon." Volatility and thin buffers killing firms is known; the bet is the τ (time-to-fix) term and its
interaction with shock/buffer.

### Prior art (WebSearch, 2026-11-14), so "what's new" is stated honestly
- Cost stickiness / asymmetric cost behaviour (Anderson, Banker & Janakiraman 2003) is ALREADY reported to
  predict bankruptcy and distress: Ntounis & Vlismas, Eur. J. Finance 31(5), 2024 (US firms 1990–2020,
  "incrementally useful for bankruptcy prediction"); "Asymmetric cost behavior and financial distress",
  Economics Letters 2024 (107k firm-years); Homburg, Hoppe, Nasev, Reimer & Uhrig-Homburg 2016 SSRN
  "Cost stickiness and credit risk"; a Polish study (2025) finds the opposite sign. So a positive τ main
  effect alone is NOT new and would only replicate known work.
- Not found in that search (absence of evidence, not proof of novelty): (a) a speed-of-adjustment τ in
  quarters (mean adjustment lag), rather than an asymmetry coefficient; (b) the specific index restriction
  β_B = −β_σ, β_τ = ½β_σ; (c) the τ × (σ/B) interaction on the absolute scale. These are the novel parts.

## 1. Design
Two cohorts, same rules, measurement strictly before the risk window, pooled:
| Cohort | Facts used (filed ≤) | τ window | σ window (4-qtr $ changes) | Buffer date ≤ | Risk window |
|---|---|---|---|---|---|
| C1 | 2014-12-31 | 2009Q1–2014Q3 | 2011Q4–2014Q3 | 2014-09-30 | 2015-01-01 – 2019-12-31 |
| C2 | 2019-12-31 | 2009Q1–2019Q3 | 2016Q4–2019Q3 | 2019-09-30 | 2020-01-01 – 2024-12-31 |
A firm may appear in both cohorts (≈ half do); pooled models are stratified by cohort with firm-clustered
inference. Second cohort was added after a power check on C2 alone (power ≈ 0.26–0.48), before any outcome.

## 2. Measures (code: code/extract.py, code/measures.py; quarterly series built from 3-month facts, YTD
differences and annual-minus-three-quarters; quarter = calendar quarter of (period end − 15 days); for each
(start,end) the latest-filed value ≤ cutoff)
- Revenue R: first available of Revenues, RevenueFromContractWithCustomer{Excluding,Including}AssessedTax,
  SalesRevenueNet, SalesRevenueGoodsNet, SalesRevenueServicesNet, RevenuesNetOfInterestExpense.
- Cost C = R − OperatingIncomeLoss; fallback CostsAndExpenses.
- τ (time to fix): Huber-robust error-correction regression on quarterly logs,
  Δln C_t = a_q + γ Δln R_t + θ (ln C_{t−1} − ln R_{t−1}) + e (quarter dummies), using all consecutive
  quarter pairs in the τ window (≥16 required). λ = −θ. τ = 1 + max(0, 1−γ)/λ quarters (1 = costs fully
  adjust in the shock quarter; the second term is the mean lag of the remaining adjustment). λ ≤ 0 → τ = 20;
  τ clipped to [1, 20].
  Pre-outcome facts about τ (recorded so nobody thinks they were tuned on outcomes): 26–28% of firms sit at
  τ = 1, ~5% at the 20 cap, median ≈ 1.25–1.3. Split-half reliability (log τ, first vs second half of the
  window) r = 0.35 (C2) and 0.14 (C1): τ is noisy, which biases its coefficient toward 0. An earlier
  definition without the "1 +" (floor 0.25) put 48% at the floor; changed before outcomes for that reason.
- τ_drop (sensitivity S2): same model with an extra slope on revenue-decrease quarters; impact on drops =
  γ + γ_d; needs ≥6 drop quarters. Correlation with τ: r = 0.88 (log).
- σ (shock size, $/√quarter): SD (ddof=1) of R_t − R_{t−4} over the σ window, ÷ 2 (≥10 changes required).
- B (buffer, $): cash & equivalents (CashAndCashEquivalentsAtCarryingValue, fallbacks
  CashCashEquivalentsRestrictedCash…, Cash) + short-term investments/marketable securities (if reported at
  the same date, else 0) + undrawn credit (LineOfCreditFacilityRemainingBorrowingCapacity dated ≤365 days
  before the cash date, else 0; reported for only ~10%) at the latest balance date ≤ buffer date.
  Note: "relative to fixed costs" cancels in σ/B when both are in the same units; fixed costs are not used.
- A = total assets at the buffer date (size control; σ and B both scale with size, corr(ln σ, ln A) ≈ 0.83).
- Controls (S1 only): leverage = Liabilities/Assets (clip 0–5); ROA = trailing-4-quarter operating income /
  Assets (clip ±2).

## 3. Sample rules (code/build_dataset.py, applied per cohort, in this order)
R1 XBRL 10-Q/10-K facts filed in the half-year before the cutoff (alive and filing);
R2 τ estimable; R3 σ estimable and > 0; R4 B > 0 and A > 0; R5 mean quarterly revenue over the last 4
quarters ≥ $2.5M; R6 CIK found in submissions.zip; R7 SIC known, not 6000–6799 (finance, REITs, shells), not
4900–4999 (utilities); R8 no 8-K Item 1.03 in the 2 years before the risk window.
Expected n before R6–R8: C1 2,381, C2 2,420 (≈3,800–4,000 firm-cohorts after R7).

## 4. Outcomes (code/outcome.py; submissions.zip pulled only after this file is committed)
- Primary D: first 8-K or 8-K/A whose items include 1.03 (Bankruptcy or Receivership), filed in the
  cohort's risk window. Time T = days from window start. Non-events censored at window end, or at the
  last filing date if the firm stopped filing more than 6 months before window end (exit by merger etc.).
- Secondary D2 (S6, non-decisive): first of Item 1.03 or an 8-K Item 3.01 (delisting notice / listing-rule
  failure) not in the same filing as Item 2.01 or 5.01 (i.e., not merger-driven).
- Known gaps: bankruptcies without an 8-K 1.03, distress resolved out of court, going-dark (Form 15) without
  bankruptcy are not counted as events; delisting-for-cause is only approximated by D2.

## 5. Predictions and models (code/analyze.py; verdict computed by code)
Primary 1 (index restriction): Cox PH, Efron ties, stratified by cohort, firm-clustered robust SEs,
covariates ln σ, ln B, ln τ, ln A.
- β_σ > 0, β_B < 0, β_τ > 0; r_B = β_B/β_σ in [−2, −0.5]; r_τ = β_τ/β_σ in [0.25, 1] (theory −1, ½).
- LR test of the restricted model (ln σ − ln B + ½ ln τ as one covariate, plus ln A) vs free (2 df) does not
  reject at p < 0.01 (non-robust likelihoods).
- Ratio CIs: firm-cluster bootstrap, 1,000 resamples, seed 20261114, percentile 95%.
Primary 2 (absolute scale): linear probability model of D with cohort fixed effects, firm-clustered SEs:
D ~ c(ln τ)·c(ln σ/B) + c(ln A) + c(ln σ/B)² + c(ln A)² + c(ln τ)² + c(ln A)·c(ln σ/B) + c(ln τ)·c(ln A)
(c = centred). Prediction: c(ln τ)·c(ln σ/B) > 0. The flexible terms were added because in a null simulation
on the real predictors (τ with no effect, multiplicative hazard), the plain spec falsely rejected 10% of the
time vs 2% for the flexible one (power/p2_typeI.py). Plain spec reported as non-decisive.
Descriptive: τ-above-vs-below-median risk differences within σ/B terciles (predict rising).
Shape check (not support): Cox interaction c(ln τ)·c(ln σ/B).

## 6. Verdict rules (unchanged from C3 except K1c, added from the C3 lesson)
- MISS if any: K1 β_τ ≤ 0, or the bootstrap CI of r_τ entirely outside [0.25, 1], or (K1c) β_σ's CI > 0 and
  β_τ's upper 95% limit < ½·β̂_σ (data exclude the τ effect size the index form implies);
  K2 the bootstrap CI of r_B entirely outside [−2, −0.5], or LR rejects at p < 0.01 with a ratio point
  estimate outside its band; K3 the Primary 2 interaction CI entirely ≤ 0.
- HIT if no K fires AND β_σ > 0, β_B < 0, β_τ > 0 each with CI excluding 0, both ratio point estimates in
  band, LR p ≥ 0.01, AND the Primary 2 interaction CI excludes 0 on the positive side.
- INCONCLUSIVE otherwise.
- Interpretation rule fixed now: a HIT with a positive τ main effect replicates known stickiness→bankruptcy
  work; the new evidence is the ratio bands + interaction. A MISS on τ, given the known prior art, would also
  mean our τ measure fails where asymmetry measures succeed; that is reported as a measurement caveat, not
  explained away.

## 7. Power (code/power.py, power/power.json; simulated outcomes on the real predictor matrix, β_σ = 0.5,
β_B = −0.5, β_A = −0.2, 150 sims each, ~3,840 firm-cohorts, cohorts not stratified, overlap ignored)
| 5-yr event rate | β_τ | power β_τ > 0 (p<.05) | power P2 plain spec |
|---|---|---|---|
| 2.5% (~96 events) | 0 | 0.05 | 0.12 (false-positive) |
| 2.5% | 0.25 (= theory ½β_σ) | 0.63 | 0.62 |
| 2.5% | 0.5 | 1.00 | 0.97 |
| 4% (~154) | 0.25 | 0.76 | 0.75 |
P2 flexible spec at 3%: false-positive 0.02, power 0.51 at β_τ = 0.25. These assume measured τ IS the causal
τ; with reliability 0.14–0.35 the real power is lower. So: a null on β_τ alone is weak evidence; K1c is the
informative kill (it fires only if the CI excludes the theory-implied size).

## 8. Sensitivities (non-decisive)
S1 + leverage, ROA (known distress predictors) — the "is τ incremental to known predictors" check;
S2 τ_drop; S3 cash-only buffer; S4 drop τ at 1 or 20; S5 logit on D; S6 D2 outcome (Cox and P2);
S7 τ alone (replication of the known univariate stickiness→bankruptcy link); S8 each cohort separately.
Secondary arm E (code/covid.py, code/analyze_E.py; C2 only, risk window from 2020-04-01): exogenous
shock = leave-one-out median of ln(R_2020Q2/R_2019Q2) across same-3-digit-SIC firms (≥5 peers; else 2-digit),
shockE = max(0, −median); z = ln(1 + shockE × quarterly revenue / B). LPM D ~ c(ln τ)·c(z) + c(ln A),
predict interaction > 0. Uses peers' 2020 revenue (post-cutoff, but never the firm's own). Non-decisive.

## 9. Confounds named now
Size (σ, B ∝ size; A controlled); τ correlates with small size (r ≈ −0.25 with ln A) and thin margins;
τ reliability is low (attenuation); impairments and restructuring charges spike C (Huber regression
mitigates); tag switching (ASC 606 in 2018) can create revenue level shifts; cohort C2's risk window is
dominated by COVID and the 2022–23 rate shock; survivorship (firms must have filed XBRL for ≥4 years);
bankruptcies without 8-K 1.03 are missed (non-differential in τ is a hypothesis); one country, public firms.
This is one more scale; a hit is evidence the math generalizes, not that thermodynamics is doing the work.
