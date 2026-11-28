# RESULTS — STAKES-EXOGENOUS (pick 12, uniform slot; ledger 62–64, outcome 70, renumbered from 66 at the q-pick13 merge)

Lock: `27bbe72` (PREREG.md, code, seeds, decision rules, synthetic validation), pushed to `origin/q-pick12` at 2:07 PM ET on 15 Nov 2026,
before any 2025 data or any 2024 data beyond the declared plumbing day was fetched. Data: CAISO OASIS public API, fetched about 2:07–2:49 PM ET
(192 files, no errors); raw files not committed (323 MB, re-fetchable with `fetch_caiso.py`); the merged hourly panels are in
`data/panel_2025.csv.gz` and `data/panel_2024.csv.gz`. Full output: `results.json`.

## Amendments after the lock (declared; neither touches a decision statistic)
- **A1 (fetch only):** `urllib` hung on one chunked response, so `fetch_caiso.get` uses `curl -m 180`. Same URLs and files.
- **A2 (report-only rows):** the locked `analyze.py` computed the by-tercile and by-quarter rows with w_quad, while PREREG says ŵ (= k_lin).
  Fixed and rerun with the same seeds; the primary, replication, S1–S4 and verdict are byte-identical (`results_lockedcode.json` and
  `analyze_lockedcode.out` keep the locked-code output).

## Results on proxy "CAISO DA load-forecast error; cost = error × (FMM − DA hub price)"
Units: ŵ in $/(MW²·h) (= $ per hour per MW² of squared error); ×10⁶ gives $/(GW²·h).

| | 2025 (primary) | 2024 (replication) |
|---|---|---|
| hours / weeks | 8,761 / 53 | 8,760 / 53 (2024-06-01 excluded) |
| within-stratum sd of e | 893 MW | 814 MW |
| **ŵ = k_lin** [95% week-block CI] | **7.8 × 10⁻⁴ [1.8, 12.6] × 10⁻⁴** | **32.1 × 10⁻⁴ [13.8, 51.4] × 10⁻⁴** |
| CI half-width / ŵ | 0.70 | 0.59 |
| w_quad (report only) | 1.3 × 10⁻⁴ [−2.3, 4.1] × 10⁻⁴ | 3.4 × 10⁻⁴ [−1.5, 8.3] × 10⁻⁴ |
| log(k_large / k_small) | −0.29 [−1.66, 1.50] | −0.25 [−1.40, 1.17] |
| exogeneity: incremental R² on D−2 errors | 0.029 | 0.057 |
| ŵ, winsorized spread (0.5/99.5%) | 7.3 × 10⁻⁴ [1.4, 12.4] × 10⁻⁴ | 21.4 × 10⁻⁴ [13.7, 29.4] × 10⁻⁴ |

Decision rules: **S1 failed** (ŵ > 0 and CI excludes 0, but half-width 0.70 ŵ > 0.5); **S2 passed** (shape consistent with quadratic loss, but
the test is weak here: the CI spans a factor of ~20); **S3 passed** (0.029 ≤ 0.10); **S4 passed** (2024 ŵ > 0, CI excludes 0).
**Verdict (locked rules): INCONCLUSIVE.** Stakes are positive and identified in sign on this proxy in both years, but not measured to the locked
precision (±50%) in the primary year.

Report-only rows (k_lin, ×10⁻³, B = 500): 2025 load terciles low/mid/high 1.15 [0.43, 2.37], 0.84 [−0.07, 1.48], 0.59 [−0.04, 0.98]; quarters
1.37, 0.50, 0.65, 0.75 (only Q3's CI excludes 0). 2024 terciles 1.40 [−0.38, 2.87], 1.03 [0.35, 1.93], 5.04 [1.67, 8.45]; quarters 1.65, 2.20, 5.10,
1.04. Exploratory (no verdict, q is a confounder): Spearman across the 288 strata of error variance vs stratum k = −0.43 (2025), −0.11 (2024).

## Interpretation (separate from the locked results; not tested)
1. **What was measured.** On this proxy, a 1 GW day-ahead load surprise costs load that bought at the forecast about $780/h in 2025 and $3,200/h in
   2024 (ŵ × 10⁶ MW²); over a year of within-stratum error that is roughly $5M (2025) and $19M (2024). This is the reduced-form cost of a load
   surprise (weather that surprises load may move renewables and imports too; limit (ii) in PREREG), not a supply-curve slope.
2. **Stakes moved about 4× between years** (2024 vs 2025 CIs do not overlap: [13.8, 51.4] vs [1.8, 12.6] × 10⁻⁴), with a falling RT−DA spread
   variance (sd 23 → 8 $/MWh). Unlocked observation, but it is the kind of change THEORY §1 N6's causal form needs ("when measured stakes change,
   the design quantity moves in the predicted direction after its adjustment lag"). The within-year pattern by load level is not stable (falls
   with load in 2025, rises in 2024), so a single w per year is a summary, not a constant.
3. **Gate for SAME-SYSTEM-AQN: not met at the locked precision.** Plausible routes, each needing its own lock: pool years with a year effect and
   longer records (precision ∝ √weeks: ±50% in 2025 needs ≈ 2× the weeks); net-load error (load − wind − solar), which is closer to the RT
   imbalance; 5-minute RTM prices; a second ISO.
4. **Proxy check owed.** The DA forecast sits 1.76 GW (7%) below "Total Actual Hourly Integrated Load" on average in 2025 (1.20 GW in 2024), which
   is far above a forecast bias. Stratum fixed effects absorb the mean, so ŵ is unaffected to first order, but the two series may not share a
   definition (for example, what each counts behind the meter or across the EIM). Not checked; no claim made.
5. **w_quad vs k_lin.** w_quad's CIs include 0 in both years. Synthetic validation showed w_quad weights strata by var(e²) and is noisier; with
   real price spikes it is uninformative. k_lin is the estimand fixed before the data.
6. No CLAIM_MAP status changes. This is a measurement of an input, not a test of N13. New row N21. Not refereed.
