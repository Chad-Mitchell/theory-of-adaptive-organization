# PREREG — STAKES-EXOGENOUS: stakes w from exogenous error variation on one real system (CAISO day-ahead load forecast)

Queue item STAKES-EXOGENOUS (pick 12, uniform slot; ledger 62–64). Locked by the commit that adds this file (its git timestamp, pushed to
`origin/q-pick12`, is the lock), by executor queue-pick12, 15 Nov 2026, **before any 2025 data or any 2024 data other than the plumbing day was fetched**.
Gate for SAME-SYSTEM-AQN (CLAIM_MAP N13 needs stakes measured on the same system as α, q, N and a design quantity).

## What was seen before the lock (declared)
- CAISO OASIS plumbing: one operating day, **2024-06-01**, of the four queries below (schema and parsing test; first rows of each file printed, 24 merged
  hours built by `analyze.panel` with the exclusion disabled; spread and error were not summarised). That day is **excluded** from all analysis.
  Also 2019-01-01 load files (prices not retained by OASIS for 2019); 2019 is not used.
- AQN-ESTIMATORS §1.S (`measurement/estimators/RESULTS.md`): w is identified only from error variation exogenous to w; cross-sections of self-optimizing
  units give ~3× low; IV fixes measurement noise only.
- `validate_synth.py` / `validate_synth.out` (synthetic only; results below).

## Regime and premises (QUEUE rule 2; THEORY §2.1, §2.5)
This item measures an input (stakes), not a §2.2 optimum, so no spectral regime is needed for its verdict; α, q, N of the load-error series are for
SAME-SYSTEM-AQN (regime **not established** here). Premise used: **quadratic loss**, E[cost | e] = w e² (THEORY §2.1 "w · E[error loss]", quadratic
in §2.2; AQN `stakes_fit`). The premise is checked by S2 (the linear price response and the quadratic cost slope must agree). Optimum compared: none (no
design quantity in this item), so the linear-vs-Bayes premise (THEORY v1.4.3 §2.2) does not arise.

## System and proxy (declared; results are labelled "on proxy" with this name)
**Proxy "CAISO DA load-forecast error; cost = error × (FMM − DA hub price)".**
- World X: CA ISO-TAC hourly integrated actual load (OASIS `SLD_FCST`, `ACTUAL`).
- System state M: CAISO's day-ahead demand forecast for that hour (`SLD_FCST`, `DAM`, `SYS_FCST_DA_MW`). Tracking error e = actual − DA forecast (MW).
- Cost of the error: load bought at its DA forecast settles the difference in real time, C = e · (P_RT − P_DA) ($/h), with P = mean of the
  TH_NP15_GEN-APND and TH_SP15_GEN-APND LMPs; P_DA from `PRC_LMP` DAM; P_RT = hourly mean of the 15-minute FMM LMP (`PRC_RTPD_LMP`, RTPD).
  Hours kept only with both DA hub prices and ≥ 6 of the 8 FMM node-intervals.
- **Why the variation in e is exogenous to w (natural-experiment argument):** e is the realized surprise relative to information at DA issue time.
  The forecaster can set its average precision per hour-of-day and month, so stakes-driven precision choice (the AQN self-selection failure) acts
  across strata; all estimates use **within-stratum (hour × month fixed effects)** variation, i.e. day-to-day surprises within a stratum. Checked by S3.
- Known limits (declared now): (i) CAISO's DA market clears on bid-in demand, not on this forecast, so e is a proxy for the RT imbalance; (ii) weather
  that surprises load may also move renewables and imports, so w is the **reduced-form** cost of a load surprise, not a pure causal supply-curve slope;
  (iii) the estimand under heterogeneous w across strata is the e²-weighted mean of stratum w (synthetic arm B); (iv) one ISO, two years.
- Units: w in $/(MW²·h); also reported per GW² (×10⁶).

## Data and fetch (fixed)
`fetch_caiso.py` (public OASIS API, no login or key; half-month chunks; 6 s between requests). **Primary year 2025** (operating days 2025-01-01 to
2025-12-31); **replication year 2024** (2024-06-01 excluded). No other years, nodes or TACs will be used for a verdict.

## Statistics (`stakes_lib.py`, `analyze.py`)
- **ŵ = k_lin (primary):** FE (hour × month) slope of (P_RT − P_DA) on e, = Σ ẽ·s̃ / Σ ẽ² with ẽ, s̃ demeaned within stratum: the stratum-demeaned
  cost per unit squared error, i.e. the e²-weighted mean of stratum stakes. Under quadratic loss with price noise independent of e, E[C | e] = k e².
- **w_quad (report only):** FE slope of C on e² (the N18 `stakes_fit` form with stratum intercepts). It weights strata by var(e²), so it differs from
  k_lin when stakes vary across strata (synthetic arm B: 0.79 of the e²-weighted mean, coverage 0). *Design change before the lock:* the first draft
  made w_quad primary and S2 a k_lin-vs-w_quad overlap; validation arm B (v0 run, `validate_synth_v0.out`) showed that compares two estimands, so
  k_lin became primary and S2 a shape test.
- **Quadratic-loss shape:** k_small and k_large = k_lin on hours with within-stratum standardized |z| ≤ 0.6745 and > 0.6745; quadratic loss ⇒ equal;
  a convex (super-quadratic) price response ⇒ k_large > k_small (synthetic arm D).
- CIs: 95% percentile, **calendar-week block bootstrap**, B = 2000, seeds 20261115 + 12 (2025) and + 13 (2024).
- **Exogeneity diagnostic:** incremental R² (beyond stratum FE) of e on the D−2 same-hour error and D−2 daily mean error (information known when the DA
  forecast is issued).
- Report only: winsorized spread (0.5/99.5%); ŵ by load tercile and by quarter (B = 500); exploratory Spearman across strata of error variance vs
  stratum k (THEORY predicts precision effort rises with stakes, but q also varies by stratum: **no verdict from it**).

## Decision rules (primary year 2025; replication 2024)
- **S1 (identified):** ŵ > 0, CI lower bound > 0, and CI half-width ≤ 0.5 ŵ.
- **S2 (quadratic-loss shape):** the 95% CI of log(k_large / k_small) contains 0.
- **S3 (exogeneity):** incremental R² ≤ 0.10.
- **S4 (replication):** 2024 ŵ > 0 with CI lower bound > 0.
- **PASS ("stakes identified on proxy … with CI")** iff S1–S4. **PARTIAL** iff S1, S3, S4 but not S2 (identified; quadratic premise doubtful).
  **FAIL ("stakes not identified on proxy")** if ŵ ≤ 0, or its CI contains 0, or incremental R² > 0.25. Otherwise **INCONCLUSIVE**.
- A PASS is a **measurement** result (gate for SAME-SYSTEM-AQN on this system), not a test of N13. No CLAIM_MAP status changes from this item alone;
  the result is recorded as a new N-row (method/measurement) or a note on N18.

## Synthetic validation (before lock; `validate_synth.out`)
R = 200 synthetic years per arm, B = 200, week blocks (52), stratum FE, AR(1) within-day errors, Student-t(3) price noise with weekly-correlated shocks:


| Arm | k_lin (primary): mean ŵ/w, coverage, median half-width/w | w_quad (report): same | S2 passes (CI of log ratio ∋ 0) |
|---|---|---|---|
| A quadratic, homogeneous | 1.002, 0.94, 0.036 | 1.001, 0.91, 0.057 | 0.99 |
| B stakes vary across strata, error sd ∝ k_s^−½ (self-selection) | 1.004, 0.98, 0.049 (truth = e²-weighted mean) | 0.79, 0.00 | 0.99 |
| C 1% price spikes ×20 | 0.999, 0.95, 0.061 | 0.998, 0.93, 0.080 | 0.99 |
| D convex response (super-quadratic loss) | 2.60 (w undefined as one number) | 3.40 | 0.00 |

So: k_lin is unbiased with near-nominal coverage (0.94–0.98) in A–C, robust to cross-stratum self-selection (B) and spikes (C); S2 has size ≈ 0.01
and power 1.0 against arm D's convexity. w_quad is biased under B, hence report-only. A first run (`validate_synth_v0.out`, arms A–C, before the
design change) is kept. One code guard added after the runs started (zero-sd bootstrap strata: z = 0 instead of NaN; those rows have ẽ = 0 and
contribute nothing either way); the table is from the rerun with the guard.
