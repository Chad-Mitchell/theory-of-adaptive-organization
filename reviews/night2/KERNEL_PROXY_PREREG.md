# PREREG — KERNEL-MEASURE-REFEREE, proxy-validity part (QUEUE pick 33, rule slot; ledger 153–155)

Executor `queue-pick33` (for Ace; Chad t1914/t1916), Sunday 15 Nov 2026, America/New_York. Separate referee: authored none of pick 28, `tests/KERNEL_MEASURE/`, PR #58 or the ledger-139 review. Own code in `KERNEL_PROXY_checks/` (`plib.py`); imports nothing from `tests/KERNEL_MEASURE` or `measurement/estimators`; reads only the data files in `tests/KERNEL_MEASURE/data/` (span 1990-01-02 … 2026-10-30, as locked there). Locked by the git commit that adds this file, pushed to `origin/q-pick33` **before** `c1_data.py` is run on real data (Tier 2: git-only, no external timestamp). Only the simulated dry run (`DRY=1`) has been run.

## Scope
The item's remaining scope (ledger 139): is "2 ln VIX as tracker, log Parkinson range variance as driver" a valid proxy for the W21 statistic of the pick-28 test? Named distortions: (a) variance risk premium (VRP), (b) log of a (risk-neutral) expectation of the level vs expectation of the log, (c) overnight variance missing from the driver and target, (d) jumps / Gaussian-driver premise. No locked constant of `tests/KERNEL_MEASURE` is re-scored; the pick-28 verdict is not re-decided here.

## First-principles frame
If the tracker were z_t = E^P[T_t | F_t] + independent noise, with T_t = mean log variance over the next 21 business days and past driver readings in F_t, then by iterated projections the regression of z on past readings has the same population kernel as the regression of the **realized** future target on the same readings. Every proxy distortion (a)–(c) is an F-measurable term added to z (VRP_t; Jensen term; overnight/close-to-close and horizon mismatch), so kernel(z) − kernel(realized target) is exactly the kernel of the distortions (OLS is linear in the response; same rows and regressors). (d) does not enter the population projection at all (it depends only on second moments); it can enter only through estimation and the VIX-is-a-conditional-mean premise.

## Pre-outcome simulation (`c0_power.py` → `c0_power.json`, 400 reps, planned n, locked α̂ 1.2587, ln q̂ −1.8116, ln ŝ2 −0.9005, best linear tracker on a 2000-day window, no data read)
| statistic (same 10-bin estimator) | mean | sd |
|---|---|---|
| W_m: tracker = best linear forecast, no noise (reproduces pick 28's 0.277) | 0.2775 | 0.006 |
| W_bar: response = realized mean log reading over t+1..t+21 | **0.2579** | 0.0439 |
| W_L: response = ln of realized mean level reading over t+1..t+21 | 0.2575 | 0.045 |
| Δ_zL = W(z) − W_L, tracker noise r = 0.45 (AR(1) φ 0.95) | **0.0218** | 0.0642 |
The realized-response kernels carry a finite-sample bias of about −0.02 (long-memory OLS); the like-with-like references are the simulated means.

`c2_jensen.py` (in-model, Gaussian, no data): a tracker reporting ln E[mean level] instead of E[mean log] shifts W21 by **+0.0028 ± 0.0004** (Σβ 0.975). Distortion (b) is negligible in the Gaussian model; any larger data effect must come from non-Gaussian structure, VRP or overnight.

## P1 — VIX-free realized-target kernel (model adequacy of the spectrum → kernel map on this driver)
Response ȳ_fut(t) = mean of y over t+1..t+21 (rows t ≤ n−22, no data after 2026-10-30); same bins, block bootstrap (126-row blocks, 999 reps, seed 20261133). D = Ŵ − 0.2579; σ_D = √(boot sd² + 0.0264²) (σ_pred as locked in pick 28; conservative: Ŵ and α̂ come from the same series and co-move). **PASS** iff |D| + 1.96σ_D ≤ 0.13 and the 95% CI of Ŵ excludes the rivals 0.000, 0.012, 0.725; **FAIL** iff |D| − 1.96σ_D > 0.13; else INCONCLUSIVE. Label: "passed/failed on proxy 'log Parkinson range variance, realized 21-business-day mean log as response, survival at 21 days of the 504-day binned projection kernel'". Not an independent theory test: α̂, q̂, ŝ2 are fitted on the same series; it checks that the fitted spectrum carries over to the kernel the data imply.

## P2 — proxy gap (the referee question)
On common rows (VIX present, t ≤ n−22), paired block bootstrap: Δ_zL = Ŵ(z) − Ŵ(L), L = ln of the realized mean Parkinson level over t+1..t+21. e = Δ_zL − 0.0218. **SMALL** (proxy distortions do not move W21 by more than half the locked band) iff |e| + 1.96 sd ≤ 0.065; **DISTORTS** iff |e| − 1.96 sd > 0.065; else UNRESOLVED. Also reported: Ŵ(ȳ) on the same rows, Δ_Lȳ (aggregation/Jensen in data), Σβ for each response, bin shares.

## MV10 gate (`tools/power_gate.py`, `c0_gate.out`) — run before outcomes
- P1 rival discrimination (optimality form, gap 0.246 to R2, σ 0.0512): **met** (P 0.998 both ways).
- P1 band rule (±0.13, σ 0.0512): **not met** (P(PASS | true) 0.72 < 0.8; needs σ ≤ 0.046).
- P2 (margin 0.065, σ 0.0642): **not met** (P 0.17; needs σ ≤ 0.023 — daily data cannot buy it: the realized response's forecast error dominates).
**Consequence, declared now:** P1's band verdict and P2 are **exploratory**; neither can be decisive. A FAIL/DISTORTS whose CI clears its margin is still reported as such.

## Descriptive, not decisive
- C4 overnight (2008-01-02 on; Yahoo `^GSPC` opens equal the prior close on most days before 2008): W21 of z on intraday vs close-to-close drivers (ln(Parkinson + overnight return²)); realized-response W21 with and without overnight variance; mean overnight share.
- C5 Gaussian premise: kurtosis of daily and 21-day changes of y; W(z) with y winsorized at 0.5/99.5 % and with 2008-09…2009-06 and 2020-02-15…2020-06 rows dropped.
- (a) VRP has no separate data in the repo (no option-implied vs realized decomposition beyond P2); it is not identified apart from (c) and VIX noise here.
