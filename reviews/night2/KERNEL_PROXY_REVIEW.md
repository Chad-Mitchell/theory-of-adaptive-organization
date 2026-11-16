# KERNEL-MEASURE-REFEREE — proxy validity (QUEUE pick 33, rule slot; ledger 153–155 + outcome)

Executor `queue-pick33` (for Ace; Chad t1914/t1916), Sunday 15 Nov 2026, America/New_York. Separate referee of pick 28 (`tests/KERNEL_MEASURE/`), completing the scope left open by the ledger-139 review: **proxy validity**. Own code `KERNEL_PROXY_checks/` (imports nothing from `tests/KERNEL_MEASURE` or `measurement/estimators`; reads only its data files; nice 19). Prereg `KERNEL_PROXY_PREREG.md`, locked at `c1e13b2` (pushed about 6:38 PM ET) before the real-data run (about 6:39 PM ET). Tier 2 (git only). Prior art: none read; none credited.

## 0. Bottom line
- **Shape: the VIX kernel's survival matches the VIX-free one.** Regressing the *realized* mean log Parkinson variance over the next 21 business days on the same past readings, with the same bins, gives Ŵ21 = **0.259 ± 0.058**; VIX's is 0.2596 (reproduced to 7 digits by own code: 0.259595). Paired difference **0.0005 ± 0.055** (post hoc; block bootstrap). Under the first-principles frame (iterated projections), every proxy distortion — variance risk premium, log of an expectation, overnight and horizon mismatch — is an F-measurable term whose kernel is exactly kernel(VIX) − kernel(realized target). That difference is centred on zero.
- **But the resolution cannot certify the distortions small.** Locked P2 (VIX vs the realized log *level* response, margin ±0.065): Δ = 0.037 vs reference 0.022, sd 0.064 → **UNRESOLVED**. MV10 was not met before outcomes (needs sd ≤ 0.023; daily data cannot buy it — the realized response's forecast error dominates), as declared.
- **P1, VIX-free kernel vs the spectrum's prediction: PASSED on proxy "log Parkinson range variance, realized 21-business-day mean log as response, survival at 21 days of the 504-day binned projection kernel", exploratory.** D = +0.001 (Ŵ 0.259 vs like-with-like 0.258), σ_D 0.064, |D| + 1.96σ_D = 0.126 ≤ 0.13; rivals (0.000, 0.012, 0.725) excluded. Low resolution (σ_D > 0.040; MV10 band rule not met: P(PASS | true) 0.72). Not an independent theory test: α̂, q̂, ŝ2 come from the same series.
- **Scale, not shape, is distorted (post hoc).** Total kernel loading Σβ: VIX **0.754 ± 0.028**, realized mean log 0.878 ± 0.042, realized log level 0.808 ± 0.047; paired VIX − realized mean log **−0.124 ± 0.050**. Simulated best linear tracker 0.976 ± 0.012, simulated realized response 0.931 ± 0.039. VIX moves about 0.75 log units per log unit of forecastable variance: consistent with a premium that shrinks in relative terms as variance rises (not tested here). W21 is a ratio, so the pick-28 statistic is immune to this; any test that uses VIX's *gain* is not.
- **Log of expectation (in-model):** a tracker reporting ln E[mean level] instead of E[mean log] moves W21 by **+0.0028 ± 0.0004** in the Gaussian model (`c2_jensen.json`). Negligible.
- **Overnight (2008-01-02 … 2026-10-30, descriptive):** overnight variance is 14.6% of close-to-close on average. VIX's W21 on the intraday driver 0.268 ± 0.067; on a close-to-close driver ln(Parkinson + overnight return²) **0.358 ± 0.056**. Not interpretable without a refit: the close-to-close driver is noisier, and a larger nugget predicts more weight on old readings. New item KERNEL-OVERNIGHT-REFIT.
- **Gaussian premise / jumps (descriptive):** kurtosis of daily changes of log Parkinson variance 2.83, of 21-day changes 3.18 (near Gaussian at the log-variance scale; this says nothing about return jumps). W(VIX) with y winsorized at 0.5/99.5%: 0.252 ± 0.045; with 2008-09…2009-06 and 2020-02-15…2020-06 dropped: 0.306 ± 0.031. Both inside the locked ±0.13 band around 0.277. The linear projection depends only on second moments, so non-Gaussianity enters only through estimation and the "VIX is a conditional mean" premise.
- **Net:** the pick-28 row stays **passed on proxy, exploratory**. Proxy validity for the *shape* statistic is supported in direction (VIX ≈ realized-target kernel) but not certified (UNRESOLVED at ±0.065). VRP is not identified separately from overnight and VIX noise here. No CLAIM_MAP status changes; K13 MATH-CORRECTED, N13 OPEN; vigilance (H8) OPEN.

## 1. Numbers (`c1_data.json`, locked run; common rows 8 694, 69 blocks)
| response | Ŵ21 | boot sd | Σβ | bin shares (ages 0, 1, 2–4, 5–9, 10–20, 21–41, 42–83, 84–167, 168–335, 336–503) |
|---|---|---|---|---|
| 2 ln VIX | 0.2596 | 0.042 | 0.754 | .164 .117 .184 .134 .143 .102 .070 .081 .034 −.027 |
| realized mean log (ȳ) | 0.2591 | 0.056 | 0.878 | .166 .123 .193 .142 .118 .114 .002 .142 .008 −.007 |
| realized ln mean level (L) | 0.2229 | 0.069 | 0.808 | .183 .134 .210 .144 .107 .142 −.044 .158 .002 −.036 |
Δ_Lȳ = −0.036 ± 0.017: aggregating in levels shortens the realized kernel slightly (big days dominate a level mean); VIX, a level forecast, nonetheless sits on ȳ, not L.

## 2. Pre-outcome simulation and gate (`c0_power.json`, `c0_gate.out`)
Locked inputs, 400 planned data sets: noiseless best linear tracker 0.2775 (reproduces pick 28's 0.277), realized mean-log response 0.2579 ± 0.0439 (finite-sample bias −0.02), realized-level 0.2575 ± 0.045, Δ_zL at tracker noise r = 0.45: 0.022 ± 0.064. Gate: P1 rival discrimination met; P1 band and P2 not met → exploratory, declared before the run. The realized data were noisier than the model (boot sd 0.058 vs simulated 0.044).

## 3. Answers to the open proxy questions (ledger 139)
| question | finding | status |
|---|---|---|
| (a) variance risk premium | not separable from (c) and VIX noise with these data; jointly with them its kernel survival effect is 0.0005 ± 0.055; it shows up as a scale effect (Σβ 0.75 vs 0.88) | shape: not detected, not certified; scale: distorted (post hoc) |
| (b) log of expectation | +0.003 in the Gaussian model; data Δ_Lȳ −0.036 ± 0.017 is aggregation of the *realized* response, and VIX does not follow it | negligible for W21 |
| (c) overnight omitted | close-to-close driver raises VIX's W21 by about 0.09 (2008–2026) | open: needs refit (KERNEL-OVERNIGHT-REFIT) |
| (d) jumps / Gaussian driver | log-variance changes near Gaussian; winsorizing and dropping crises keep W21 within 0.252–0.306 | no effect on the verdict detected |

## 4. Questions for Ace / a later reviewer
1. Should the THEORY row say "proxy validity refereed: shape supported, not certified" (PR for v1.4.13) or keep "not refereed" until KERNEL-OVERNIGHT-REFIT?
2. P1 passed by 0.004 of slack (0.126 vs 0.13) with σ_D computed conservatively (independent quadrature although Ŵ and α̂ co-move); a joint-refit σ (simulate, refit α̂ each rep) would tighten it. Worth doing only if P1 is cited anywhere.
3. The scale finding (Σβ −0.12 ± 0.05) is post hoc; it bears on any future test that reads a tracker's gain from VIX (e.g. stakes or vigilance-gain tests using VIX as tracker).

## 5. Files
`KERNEL_PROXY_checks/`: `plib.py` (own fBm, kriging, bins), `c0_power.py/.json/.out`, `c0_gate.out`, `c1_data.py/.json/.out` (locked run; `c1_data_dry.json` = simulated dry run), `c2_jensen.py/.json/.out`, `c3_posthoc.py/.json`, `c4_sumbeta.py/.json`, `SHA256SUMS` (lock).
