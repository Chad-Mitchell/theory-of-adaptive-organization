# RESULTS — STAKES-SHIFT-CAISO (pick 15, unaided slot; ledger 76–78, outcome 91)

**Lock:** `874576f` (PREREG.md, `fetch_shift.py`, `shift_lib.py`, `analyze_shift.py`, seeds, decision rules, synthetic validation), pushed to
`origin/q-pick15` at 3:14 PM ET on 15 Nov 2026, before any outcome data were fetched. After a rebase onto main for the merge the same tree is
commit `7784320` (rebased copy on branch `q-pick15-merge`; the original `874576f` stays on `origin/q-pick15`, which was not force-pushed).
**Data:** CAISO OASIS public API, CA ISO-TAC, fetched 3:15–4:29 PM ET (512 files, 0 failed, 0 empty; 129 MB raw, not committed, re-fetchable with
`fetch_shift.py`). Locked code ran once, unchanged: `analyze.out`, `results.json`.

## Amendment after the lock (declared; fetch only)
- **A1:** `FETCH_KEYS` env var added to `fetch_shift.py` so that 2019–2023 fetched only DAM and RTD (the 4-query fetch ran at ~12 s per file).
  For those years only e_rt and e_naive enter any statistic (s_yr), so no statistic changed. Commit `cf7d372`.

## Results (locked rules) on proxy "CAISO DA-vs-RTD forecast MSE (q-adjusted by seasonal naive), stakes = k_lin on the same error"
| Quantity | Value |
|---|---|
| Coverage, Jan–Oct, 2019–2026 | 0.955–0.971 every year (G1 **pass**) |
| Stakes k_lin on e_rt (clean, like-for-like error), 2024 | 5.37 × 10⁻³ [3.34, 7.32] $/(MW²h) |
| Stakes k_lin on e_rt, 2025 | 3.54 × 10⁻³ [2.60, 4.46] |
| Δlog w, 2025 vs 2024 | **−0.41 [−0.88, +0.07]** (a ~34% fall; CI includes 0) → **G0 fail** |
| Prediction D_pred = −(1/3)Δlog w | +0.14, band [0, 0.35] (N21's numbers would have given +0.47) |
| D (2026 vs 2025) = Δlog MSE(e_rt) − (1/3)Δlog MSE(naive) | **−0.088**, bootstrap [−0.34, +0.17], se_boot 0.134 |
| Δlog MSE(e_rt), unadjusted | +0.17 (FE rms 590 → 642 MW) |
| Δlog MSE(seasonal naive) | **+0.77** (×2.17) → **G2 fail** (locked ≤ log 2 = 0.69) |
| Earlier year pairs (D, 2019→20 … 2024→25) | +0.32, −0.53, −0.02, +0.30, −0.04, −0.15; s_yr 0.32, mean −0.02 |
| se_tot = √(se_boot² + s_yr²) | 0.34; D ± 1.96 se_tot = [−0.76, +0.58] |
| α̂ (N18 Whittle, daily net-load residual 2024–25) | 2.10 ± 0.09 (G4 no cap; regime consistent with A, α ≈ 2) |

**Verdict (locked): INCONCLUSIVE on proxy "CAISO DA-vs-RTD forecast MSE (q-adjusted by seasonal naive), stakes = k_lin on the same error"**,
by gates: G0 failed (on the like-for-like error the 2024→2025 stakes fall is not established), G2 failed (seasonal-naive MSE rose 2.17×, beyond the
locked 2× adjustment limit). Neither the PASS nor the FAIL rule was reached either way (D's total interval [−0.76, +0.58] contains both 0 and 0.05).
No CLAIM_MAP status change; one system, one proxy, no field claim.

Report only: D on e_2da +0.02; on e_act (N21's error) +0.11, night hours +0.11; detrended −0.07; Jan–Apr −0.33, May–Oct +0.02; at α̂'s
elasticities D −0.07 vs predicted +0.14.

Post-verdict diagnostic (not locked; `diag_naive.out`): the naive-MSE rise is concentrated in Sep–Oct 2026 (FE rms 6.5 and 6.0 GW vs 3.2 and 1.8 GW
in 2025; Sep 2024 was 6.1 GW too), i.e. a weather-year difference (heat events) rather than a series break; e_rt rms rose less (0.81, 0.69 GW vs
0.59, 0.48 GW).

## Interpretation (separate from the locked results; not tested)
1. **CAISO-PROXY-DEFS is settled, and it matters.** "Actual" load includes BTM solar while the DA/RTD forecasts are net of it (solar-shaped mean gap,
   ~0 at night, +4–6 GW at noon). On the like-for-like error the stakes are ~1.7× (2024) and ~4.5× (2025) larger than N21's values and fell only
   ~34%, not ~4×. The likely mechanism is errors-in-variables: BTM-estimate variation in N21's error attenuates k_lin, more so as BTM solar grew.
   So **N21's "4× fall" is mostly a proxy artifact**, and the natural experiment this item was built on is weak on the clean proxy. That is a
   finding for STAKES-REFEREE and STAKES-PRECISION.
2. **The test had little power even if the gates had passed.** Year-to-year noise in the q-adjusted MSE is s_yr ≈ 0.32 log units, while a ~34%
   stakes fall predicts D ≈ 0.14 at α = 2 (upper end; the horizon term dilutes it). A one-year contrast needs a stakes change of roughly
   e^{3·1.96·0.34} ≈ 7× or more, or many years of stakes, to pass or fail. The prereg should have checked attainability before the lock (the
   KG-FEASIBILITY-GATE lesson, now for causal tests).
3. Unadjusted, DA forecast MSE did rise 2025→2026 (+17%) in the predicted direction, but the world was harder too (naive ×2.17), and after the
   locked q adjustment D is slightly negative. Neither reading is evidence for or against N6 here.
4. α̂ ≈ 2.1 on the daily net-load residual puts this system near Regime A, where the linear-tracker elasticities used are the Kalman ones.
5. Rival R5 stays open: the ISO's forecasting effort may not be priced by the market cost of DA surprises at all.
