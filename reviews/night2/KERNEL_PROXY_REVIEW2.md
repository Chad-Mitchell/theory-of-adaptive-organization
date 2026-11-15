# Independent review of PR #66 (THEORY v1.4.13 / CLAIM_MAP v2.31, KERNEL-MEASURE-REFEREE proxy part, pick 33)

Reviewer: independent executor for Ace (Chad t1914/t1916), Sunday 15 Nov 2026, about 6:44–6:57 PM ET (America/New_York). Authored none of pick 28, pick 33, `tests/KERNEL_MEASURE/`, `KERNEL_PROXY_*` or PR #66. Ledger 158 (out-of-cycle, unscored). Own code: `KERNEL_PROXY_REVIEW2_checks/` (`rlib.py` written from the prereg text; imports nothing from `tests/KERNEL_MEASURE`, `measurement/` or `KERNEL_PROXY_checks/`; reads only `tests/KERNEL_MEASURE/data/`; nice 19).

## Verdict: **PASS-WITH-FIXES** (applied and merged)
Evidence-only edit; no headline, kill condition, locked prediction, result or CLAIM_MAP status changes. K13 MATH-CORRECTED, N13 OPEN, H8 vigilance OPEN. Wording stays at "passed on proxy, exploratory".

## 1. Re-derivation (own code)
`r1_data.py` → `r1_data.json` (data), `r2_sim.py` → `r2_sim.json` (400 in-model reps), `r3_seeds.py` → `r3_seeds.json` (bootstrap-seed spread).

| quantity | author | reviewer |
|---|---|---|
| W21, 2 ln VIX (common rows 8 694) | 0.2596 ± 0.042 | 0.259595 ± 0.043 |
| W21, realized mean log ȳ (common / P1 rows) | 0.2591 ± 0.056 / 0.058 | 0.259059 ± 0.058 / 0.259055 ± 0.058 |
| W21, realized ln mean level L | 0.2229 ± 0.069 | 0.222935 ± 0.071 |
| VIX − ȳ (paired) | 0.0005 ± 0.055 | 0.0005 ± 0.055 |
| VIX − L (P2), e = Δ − 0.0218 | 0.037 ± 0.064, UNRESOLVED | 0.037 ± 0.065, e 0.015, UNRESOLVED |
| Σβ: VIX / ȳ / L | 0.754 / 0.878 / 0.808 | same (sd 0.029 / 0.041 / 0.046) |
| Σβ VIX − ȳ; VIX − L | −0.124 ± 0.050; not reported | −0.124 ± 0.051; **−0.054 ± 0.053** |
| 2008–2026: VIX on intraday / close-to-close driver | 0.268 ± 0.067 / 0.358 ± 0.056 | 0.268 ± 0.070 / 0.358 ± 0.058 |
| overnight share | 0.1455 | 0.1455 |
| in-model: noiseless tracker W21 | 0.2775 | 0.2773 ± 0.0003 |
| in-model: realized mean-log response | 0.2579 ± 0.0022 | **0.2585 ± 0.0025** (8 694-row truncation 0.2583) |
| in-model: Jensen shift (ln E level − mean log) | +0.0028 | +0.0028 |
| in-model: W(z) − W(ȳ), tracker = conditional mean (+ AR(1) noise r 0.25 / 0.45) | not computed | **+0.019 / +0.019 / +0.021** |
| in-model: Σβ realized ȳ / tracker | 0.931 / 0.976 | 0.927 / 0.974 |
| dW(ȳ)/dα | not computed | −0.54 ± 0.006 (σ_pred from α alone 0.023 < locked 0.0264) |

Point estimates on data match to 9+ digits (same rows, same estimator); bootstrap sds agree within seed noise.

## 2. Answers to the four questions
**Q1. Kernel-difference identity.** Valid. In sample, OLS is linear in the response, so β̂(z) − β̂(ȳ) = β̂(z − ȳ) exactly on common rows (checked: 1.8×10⁻¹⁵). In population, β(ȳ) = β(E[ȳ | F]) whenever every regressor (ages 0–503 of the Parkinson reading, plus the intercept) is F-measurable; hence kernel(VIX) − kernel(realized target) = projection kernel of VIX − E[ȳ | F], which contains every distortion (risk premium P vs Q, log of a level expectation, overnight/close-to-close and 30-calendar vs 21-business-day horizon, VIX noise correlated with past readings). Assumptions: (i) past readings in the information set at VIX's close (true: 4:15 PM VIX close vs the day's high/low); (ii) identical rows, regressors and intercept; (iii) finite second moments (the driver is fBm with H ≈ 0.13, so "population" means the projection given the design). **Not needed:** orthogonality of future Parkinson noise — ȳ − E[ȳ | F] is orthogonal to F by definition. That premise is needed only to read the realized kernel as the latent target's kernel (P1's link to the spectrum prediction). **Caveats the PR text omitted:** (a) in finite samples the forecast error is orthogonal to past but not to future regressors (not strictly exogenous), which produces the realized response's −0.02 bias; the in-model expectation of W(VIX) − W(ȳ) under "VIX = conditional mean" is therefore about **+0.02, not 0**, so the post hoc 0.0005 ± 0.055 sits at −0.02 ± 0.055 from its reference — still nothing detected. (b) W21 is a ratio: equal shares do not mean a zero distortion kernel, only that the distortion kernel's own survival matches the target's (measured: distortion mass −0.126, its survival 0.23 vs ȳ's 0.26 — a roughly proportional, gain-like distortion).

**Q2. 0.2579 after finite-sample bias; 0.004 slack.** 0.2579 is the right like-with-like reference: own simulation 0.2585 ± 0.0025 at planned rows (the locked run's 58-row truncation to 69 × 126 moves it 0.0002). Using 0.2585 changes D by 0.0006, less than the slack. The slack is governed by the bootstrap sd: across 60 other seeds the sd ranges 0.057–0.062 (mean 0.0588) and the boundary is 0.0602; PASS at 56 of 60, INCONCLUSIVE at 4 (e.g. seed 12 in `r1_data.json`: 0.1315). Blocks 63 and 252 give PASS at the seeds tried. The locked seed's PASS stands as locked; it is a near-boundary, exploratory PASS. A tighter σ_pred (0.023 from α alone here; 0.023 joint per ledger 139) would add about 0.003 of slack but was not locked, so it is not used.

**Q3. "Supported, not certified".** "Supported" overstates: the paired CI (±0.11) spans most of the locked ±0.13 band and P2 is UNRESOLVED. Changed to **"consistent, not certified"**, with the +0.02 in-model reference stated and "no distortion of the share detected" in place of "do not move the share detectably" (same meaning, reference made explicit).

**Q4. Post hoc gain finding in the row.** The author's "the proxy distorts gain, not shape" is target-dependent: the deficit is −0.12 ± 0.05 against the realized mean log but −0.05 ± 0.05 against the realized log level (closer to what VIX prices), and on 2008–2026 the realized close-to-close log level has *lower* gain (0.59 ± 0.12) than VIX (0.75 ± 0.05). Ruling: keep one post hoc, target-dependent caution in the row (it matters for any test that reads gain from VIX) and drop the interpretive clause. VIX-GAIN-SCALE note updated.

## 3. Goalposts and wording
- `KERNEL_PROXY_PREREG.md`, `c0_power.py`, `c1_data.py`, `plib.py` unchanged since lock `c1e13b2` (18:38:37 ET); later commits only add outputs (`c1_data.json/.out`) and post hoc scripts (`c3_posthoc`, `c4_sumbeta`), labelled post hoc. `tests/KERNEL_MEASURE/` at `6d235ed` unchanged on main (only result files added). Data hashes match pick 28's SHA256SUMS.
- MV10 handled as declared: P1 band rule and P2 not met → exploratory; nothing is called decisive.
- Labels: "passed on proxy" uses the full locked label now (the PR shortened it). "Theory", not "law"; no field kill; vigilance OPEN.

## 4. Fixes applied (THEORY v1.4.13 row, changelog record; CLAIM_MAP v2.31 note; THEORY CLAIM_MAP pointer v2.29 → v2.31)
F1 header clause "supported" → "consistent". F2 identity stated "in population", OLS-identity and ratio caveat added. F3 P1 full proxy label; slack and seed robustness stated. F4 in-model +0.02 reference for VIX − realized. F5 gain sentence narrowed to post hoc, target-dependent, VIX-GAIN-SCALE pointer.

## 5. Not done
No joint-refit σ_D (refit α̂ per simulated rep); not needed for the verdict (it would only widen the slack). VRP is still not identified separately from overnight and VIX noise. KERNEL-OVERNIGHT-REFIT stays open.
