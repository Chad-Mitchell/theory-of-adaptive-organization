# PREREG — STAKES-SHIFT-CAISO: does CAISO's day-ahead forecast precision respond to the 2024→2025 stakes fall? (THEORY §1 N6, causal form)

Queue item STAKES-SHIFT-CAISO (pick 15, **unaided slot**; ledger 76–78). Locked by the commit that adds this file, pushed to `origin/q-pick15`
(its git timestamp is the lock), by executor queue-pick15, 15 Nov 2026, **before any outcome data (2019–2023 or 2026 load-forecast files, or any
RTD/2DA file for 2024–2025) were fetched.** One system, one proxy: no field claim can follow from it.

## What was seen before the lock (declared)
- STAKES-EXOGENOUS (N21) results: k_lin on proxy "e = actual − DA" 7.8e-4 [1.8, 12.6] (2025) and 32.1e-4 [13.8, 51.4] (2024) $/(MW²h); quarterly
  k_lin; **within-stratum sd of e = actual − DA: 893 MW (2025), 814 MW (2024)**, i.e. a ~20% rise in that variance 2024→2025 on the N21 proxy
  (this is the lag-0 comparison, which is therefore NOT used for a verdict); spread sd 23 → 8 $/MWh.
- CAISO-PROXY-DEFS check (done first, below): mean of (actual − DA) by hour of day in the committed 2024 and 2025 panels.
- Plumbing: SLD_FCST RTM/2DA heads for 2024-06-01 (STAKES-EXOGENOUS plumbing day, excluded; first 8 CA ISO-TAC RTD/RTPD values of hour 1 printed);
  OASIS price availability probes (one day DA NP15 for 2021-06, 2022-06, 2023-06: no data; 2023-11-01 and 2024-01-01: data); a 2026-11-01..10 RTD
  row count, and a 2026-11-01..03 run of `shift_lib.hourly` (non-missing shares only; November 2026 is outside every window and not used).
- Synthetic validation `validate_synth.out` (below). Nothing else about 2019–2023 or 2026 load forecasts.

## CAISO-PROXY-DEFS, settled cheaply first (descriptive)
Mean (actual − DA) by hour of day is solar-shaped: about 0 to −0.2 GW at hours 19–23, rising to +4.1 GW (2024) and +5.8 GW (2025) at hour 12.
That is the signature of the two series counting behind-the-meter (BTM) solar differently: the OASIS DA (and 2DA, RTPD, RTD) forecasts are net of
estimated BTM solar, while "Total Actual Hourly Integrated Load" is not (a secondary source says so explicitly, faculty.xjtu.edu.cn/chenxin
article 40842, a CAISO DART-monitor write-up; CAISO's own definition page was not found in this pass, so the mechanism is "consistent with", not
quoted from CAISO). Consequences: (i) the 1.76 GW mean gap is a definition gap, not forecast bias; (ii) e = actual − DA contains BTM-estimate
variation that is not forecast error, and it grows with BTM solar; (iii) N21's k_lin may be attenuated by that extra noise, and more so in 2025.
**So this test re-measures the stakes on a like-for-like error (G0) and uses the like-for-like error as its precision measure.**

## Regime, premises, optimum scored (QUEUE rule 2; THEORY v1.4.4 §2.2, §2.5, §1 N6)
- **Optimum scored: the best linear tracker** (named here; also THEORY's default). Linear precision pricing (θ = 1), so precision and effort have the same
  elasticities (CLAIM_MAP A5; EFFORT-UNITS-ERRATUM: at θ = 1 spend/price = precision; any θ > 0 keeps the sign).
- From §2.2 Regime B rows (error under noisy sensing e* = q^{1/α}N^{1−1/α}/sin(π/α); precision 1/N ∝ w^{α/(2α−1)} q^{1/(2α−1)}): the optimal
  tracker's MSE ∝ **q^{1/(2α−1)} · w^{−(α−1)/(2α−1)}**. At α = 2 (Regime A, Kalman): precision elasticity in stakes **2/3**, MSE elasticity in
  stakes **−1/3**, in q **+1/3**. For any 1 < α ≤ 3 the stakes elasticity of MSE is in [−0.4, 0): **direction is regime-robust for α > 1**; size is not.
- **Regime: not established.** α of the daily net-load residual is measured as a report (N18 Whittle, `measurement/estimators/aqn.py`); if
  α̂ + 2 SE < 1.1 (clearly outside the 1 < α range where the direction holds) the verdict is capped at INCONCLUSIVE (G4).
- Inputs (CAUSAL-KILL-INPUTS interim rule): the inputs that may change are stakes w (the natural experiment), drift level q (controlled), sensing noise
  N (here N is the design variable itself: precision = 1/N) and α (assumed fixed across years; reported). No Bayes optimum, so no jump inputs.
- Caveat declared now: the DA forecast is a ~1-day-ahead prediction, so its MSE adds horizon innovation that precision cannot remove; that dilutes the
  response below the filter elasticity. Hence the predicted size is an **upper-end** value and the band starts at 0.

## Design (locked)
- **System state M:** CAISO's DA demand forecast, CA ISO-TAC (`SLD_FCST` DAM). **Reference X (same definition):** hourly mean of the 5-min RTD
  forecast (`SLD_FCST` RTM, execution RTD; ≥ 10 of 12 intervals), minutes ahead, net of BTM like the DA forecast.
- **Precision measure:** within-stratum MSE of e_rt = RTD-hour − DA, stratum = hour × month, demeaned per year (removes the level gap and all
  stratum biases). Window: operating days **1 Jan – 31 Oct** of each year (2026 has data only to mid-Nov; same months both years).
- **q control:** seasonal-naive error e_naive = RTD-hour(D) − RTD-hour(D−7), same hour, same FE MSE. For fBm the h-step naive MSE ∝ q at fixed h.
- **Statistic:** D = Δlog MSE(e_rt) − (1/3)·Δlog MSE(e_naive), 2026 minus 2025. The predicted D = −(1/3)·Δlog w, so the q term is removed
  at the predicted q elasticity.
- **Adjustment lag: 12 months, fixed.** Design in year Y responds to stakes in year Y−1 (annual model/vendor/procedure cycles; a guess, declared). So
  the stakes contrast 2025 vs 2024 predicts the precision contrast 2026 vs 2025. Lag 0 (2025 vs 2024) was already seen on the N21 proxy; not used.
- **G0 stakes on the clean proxy:** k_lin (STAKES-EXOGENOUS estimand; FE hour × month slope of FMM − DA hub spread on e_rt) for full years 2024
  and 2025, prices from the committed STAKES-EXOGENOUS panels, 2024-06-01 excluded, week-block bootstrap B = 2000, seeds 20261131 (2025), 20261132
  (2024). Δlog w = log(k25/k24), 95% CI from the paired bootstrap draws. G0 passes iff both k > 0 and the CI upper bound < 0.
- **Prediction:** D_pred = −(1/3)·Δlog w (clean). Band [0, 0.4 × (−CI lower bound of Δlog w)]. (For reference, N21's numbers give D_pred = +0.47.)
- **Uncertainty:** week-block bootstrap within each year (B = 2000, seed 20261130) gives se_boot; **year-to-year noise** s_yr = sd (ddof 1) of the
  same D for consecutive earlier year pairs 2019→2020 … 2024→2025 (Jan–Oct, each year ≥ 90% coverage; needs ≥ 3 pairs). se_tot = √(se_boot² + s_yr²)
  (conservative: s_yr already contains sampling noise and any earlier design responses).
- **Gates:** G0 above; G1 coverage (rows with finite e_rt and e_naive) ≥ 90% of Jan–Oct hours in 2025 and 2026; G2 |Δlog MSE(e_naive)| ≤ log 2
  (q change small enough to adjust); G4 cap above; ≥ 3 earlier pairs.
- Data: `fetch_shift.py` (public OASIS API, no login; CA ISO-TAC filter; DAM, 2DA, ACTUAL, RTD) for 2019–2026; years that OASIS no longer holds are
  dropped (coverage < 90% excludes them from s_yr).

## Decision rules (locked; `analyze_shift.py`)
- If any of G0, G1, G2 fails, G4 caps, or s_yr is unavailable: **INCONCLUSIVE** (stating which).
- **PASSED on proxy "CAISO DA-vs-RTD forecast MSE (q-adjusted by seasonal naive), stakes = k_lin on the same error"** iff D − 1.96·se_tot > 0
  and D ≤ the band's upper end.
- **FAILED on that proxy** iff D + 1.96·se_tot < 0.05 (the data exclude even a 5% rise in q-adjusted MSE: precision did not move in the predicted
  direction after the lag; N6 causal form, one system).
- Otherwise **INCONCLUSIVE** (including "direction right, size above band").
- Named rivals: (R1) fixed effort / no response (D ≈ 0); (R2) secular forecasting improvement (D < 0; report D − mean earlier pair change);
  (R3) q change from BTM solar, batteries, weather (q control, G2); (R4) method or market change, notably CAISO's EDAM go-live in 2026 (report D
  for Jan–Apr and May–Oct separately); (R5) the forecaster does not face these market stakes (interpretation only).
- Report only, no verdict: D on e_2da (RTD − 2DA), on e_act (N21's error, all hours) and on e_act at night hours (1–5, 20–24; BTM ≈ 0);
  D at α̂'s elasticities if 1 < α̂ < 3; unadjusted Δlog MSE.
- A FAILED counts as "failed on system CAISO" in the causal form; §9's theory-level sink needs two scales. No CLAIM_MAP status change from one system.

## Synthetic validation (before lock; `validate_synth.out`)
R = 100 pairs of synthetic Jan–Oct years (stratum means/sds, AR(1) hourly errors with weekly-correlated day shocks), planted D = 0.25:
mean D̂ 0.247, sd across replications 0.072, mean bootstrap se 0.077, 95% CI coverage 0.98.
