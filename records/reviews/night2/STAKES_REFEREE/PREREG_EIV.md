# PREREG — STAKES-REFEREE locked check R-EIV: is pick 15's "errors-in-variables from BTM solar" the reason N21's k_lin is small?

Queue item STAKES-REFEREE (pick 34, rule slot; ledger 159 unaided order, 160 rule_rank, 161 claim). Referee executor queue-pick34, who authored
none of STAKES-EXOGENOUS, STAKES-SHIFT-CAISO or their amendments. Locked by the commit that adds this file (pushed to `origin/q-pick34`),
**before any RTD load-forecast file was fetched by this referee** (no raw RTD data exist on the box; pick 15's raw files were not committed).

## Seen before the lock (declared)
- `tests/STAKES_EXOGENOUS/data/panel_{2024,2025}.csv.gz` (DA forecast, ACTUAL, hub DA price, FMM price), and the published numbers in
  STAKES_EXOGENOUS/RESULTS.md and STAKES_SHIFT_CAISO/RESULTS.md: k_lin on e_act (N21) 3.21e-3 (2024), 0.78e-3 (2025); k_lin on e_rt 5.37e-3 (2024),
  3.54e-3 (2025). So the all-hours ratio is known in rough terms (ln 0.60 ≈ −0.51, ln 0.22 ≈ −1.51). **No night-hour k on e_rt or e_act has been
  computed by anyone** (pick 15 reported D on e_act at night, a precision statistic, not k).

## Question and hypotheses
Pick 15 (Interpretation 1) says N21's error e_act = ACTUAL − DA is gross of behind-the-meter (BTM) solar while DA is net of it, and that BTM-estimate
variation in e_act attenuates k_lin (errors-in-variables, EIV). Reference error e_rt = hourly mean RTD − DA (same definition as DA).
- **H_EIV (pick 15's mechanism):** the wedge u = e_act − e_rt is BTM-driven, so it vanishes at night, and at night k(e_act) ≈ k(e_rt).
- **Rival H_W (wedge not BTM-specific):** the gap persists at night about as large as over all hours (e.g. the two series also differ by EIM/area
  accounting, metering timing, or operator adjustments in RTD).

## Statistic (own code `eiv.py`; numpy/pandas)
Pool 2024 and 2025 (STAKES-EXOGENOUS hourly panels joined to the hourly mean of 5-min RTD, ≥ 10 of 12 intervals; 2024-06-01 excluded), stratum
g = year × hour × month, spread = FMM − DA hub price as in N21. k(x) = FE slope of spread on x. **Night** = OPR_HR ∈ {1..5, 21..24} (hour-ending local,
BTM solar ≈ 0 all year in California). r_night = ln k_night(e_act) − ln k_night(e_rt); r_all = same over all hours. σ_n = sd of r_night over
B = 2000 paired calendar-week block bootstrap draws (seed 20261115 + 34); σ_n and r_all are computed and printed **before** r_night is printed
(blind gate).
- **Midpoint** m = r_all / 2 (κ = ½ of the all-hours gap; FRAMEWORK MV10 / THEORY §1 N6 κ range).
- **PASS (H_EIV supported on proxy "CAISO night-hour k_lin, ACTUAL vs RTD reference error"):** r_night − 1.96 σ_n > m.
- **FAIL (H_EIV rejected on that proxy):** r_night + 1.96 σ_n < m.
- Else INCONCLUSIVE. If r_all ≥ −0.2 (no gap to explain), the check is void.
- **MV10 gate (optimality form, effect = |r_all| between H_EIV's 0 and H_W's r_all; κ inside the rules is ½, so the gate is run as
  `power_gate.py contrast --form optimality --effect |m| --sigma σ_n`):** both rules reachable with probability ≥ 0.8 iff |m| ≥ 2.80 σ_n. If not met,
  any verdict is labelled exploratory.

Report only (no verdict): the reliability identity k(e_act)/k(e_rt) vs λ = Cov(e_act, e_rt)/Var(e_act) by hour band (exact if the part of e_act not
explained by e_rt is uncorrelated with spread); day band (OPR_HR 10–16) r_day; per-year r_night; sd of u by hour.
This is a check on a mechanism claim in an interpretation paragraph; it moves no locked verdict (N21 INCONCLUSIVE, N22 INCONCLUSIVE stay).
