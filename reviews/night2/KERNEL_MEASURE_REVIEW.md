# KERNEL-MEASURE independent review (PR #58: THEORY v1.4.10 + CLAIM_MAP v2.28)

Independent reviewer executor (for Ace; Chad t1914/t1916), Sunday 15 Nov 2026, about 6:15–6:45 PM ET (America/New_York). I authored none of pick 28, `tests/KERNEL_MEASURE/`, PR #58 or PR #59. Out-of-cycle, unscored (independent review of the pick 28 author PR per t1916); ledger 138. Own code in `KERNEL_MEASURE_REVIEW_checks/` (`rlib.py`, `c1`–`c4`), run at nice 19. It imports nothing from `tests/KERNEL_MEASURE/` or `measurement/estimators/`. I read the author's code to get the definitions, then rewrote everything: my own Whittle with aliasing on first differences, my own null-space kriging (the author used a bordered system), my own Davies–Harte fGn, and my own binned OLS and block bootstrap.

## Verdict: PASS-WITH-FIXES
The evidence edit claims no more than "passed on proxy (VIX vs range variance), exploratory" once the fixes below are in. Every key number reproduces. One author sensitivity claim is wrong: free-noise α̂ does **not** make the verdict inconclusive once the refit is done consistently. Fixing it does not upgrade the result. The bootstrap SE of the measured share alone is 0.041, above the locked 0.040, so the test stays exploratory whatever the prediction side does.

## Re-derived numbers (`c1.json`, `c2.json`, `c3.json`, `c4.json`)
| quantity | author | reviewer |
|---|---|---|
| data SHA-256 (GSPC, VIXCLS) | SHA256SUMS | match |
| n, VIX missing, regression rows | 9276, 3, 8694 | 9276, 3, 8694 |
| full-band α̂, ln ŝ2 | 1.303 ± 0.048, −0.900 ± 0.118 | 1.303 ± 0.048, −0.900 ± 0.119 |
| R1 split: high (≤ 20 d) / low α̂ | 2.83 ± 0.51 / 1.18 | 2.83 ± 0.51 / 1.18 (noise → 0, boundary) |
| in-band fixed-noise α̂, ln q̂ | 1.2587 ± 0.0429, −1.8116 ± 0.1009 | 1.2587 ± 0.0429, −1.8116 ± 0.1009 |
| in-band free-noise α̂ | 1.190 ± 0.098 | 1.190; ln ŝ2 → −30 (boundary), so the SE is undefined |
| Ŵ21 (blocks 126 / 252 / 63) | 0.2596 ± 0.0414 / 0.2625 ± 0.0382 / — | 0.2596 ± 0.0408 / 0.2625 ± 0.0374 / 0.2614 ± 0.0390 |
| direct S(21), 504-day window | 0.301 | 0.3007 (2000-day: 0.3045) |
| planned-n like-with-like W21 | 0.2770 | 0.2773 ± 0.0006 (100 reps) |
| long-run W21 (200 000 days) | 0.288 | 0.290 |
| dW21/dα | −0.601 | −0.597 |
| rivals R1/R2/R3 | 0.000/0.012/0.725 (binned) | 0.0008/0.015/0.706 (direct kernels); all far outside CI 0.18–0.34 |
| summed slope | 0.75 | 0.754 |
| tracker noise r = 0.45 (AR(1) 0.95): mean, sd of Ŵ21 | bias ≤ 0.007 | 0.280, 0.053 (60 reps): no material bias |

## The four questions
1. **Simulated 0.277 vs direct 0.301.** The simulated value is the right comparison. The estimator projects VIX onto 10 bin sums of noisy readings over 504 days. That differs from the kernel's own binned mass for two reasons: equal weights are forced within each bin, and weight from beyond 504 days loads onto correlated bins. The estimator also has a planned-n bias (0.277 at n = 9276 vs 0.290 long-run). Comparing the data to the estimator's expectation under the theory, at the planned n, is like with like. This choice matters: using 0.301 would move D to −0.041, and |D| + 1.96σ_D = 0.137 > 0.13 would give INCONCLUSIVE. But it was locked, with its reason, in `6d235ed` before the outcome, and it is the correct comparison.
2. **Fixed-noise vs free-noise α̂.** The fixed-noise fit is defensible: the in-band free fit drives the noise to zero, which the author's own Brownian range-floor simulation rules out (Parkinson log-variance noise 0.34–0.39 even for an ideal Brownian day). More importantly, **the question does not decide the verdict.** Along the in-band noise profile (ln ŝ2 fixed at −30, −3, −1.5, −1.2, −1.08, −0.94, −0.90, −0.7, −0.5), the refit (α̂, ln q̂) runs from (1.190, −1.53) to (1.299, −1.98), and the planned-n W21 prediction stays at 0.2764–0.2781 (`c3.json`). α and q trade off to fit the same in-band spectrum, and the kernel depends on that spectrum. The author's sensitivity (0.318, INCONCLUSIVE) substituted α̂ = 1.19 while keeping ln q̂ and ln ŝ2 at the fixed-noise values. That parameter set is not a fit to anything; my planned-n value for it is 0.320. **The sentence "with the free-noise α̂ the verdict is inconclusive" is replaced** in THEORY and CLAIM_MAP.
3. **Choosing the band after R1 said "not established".** Acceptable as declared. R1 failed because its fixed 20-day split puts a noise-dominated high band (α̂ 2.83) against the signal band. The choice used the driver only, and git orders it before the VIX regression: lock 6d235ed at 6:05:07 PM ET, results 4cb83b1 at 6:06:21 PM ET. That is Tier 2 only, with no external timestamp, so it cannot be independently verified that no VIX regression ran first. Using the full-band inputs instead (α̂ 1.303) predicts 0.256, also PASS. The band choice is a researcher degree of freedom that the result does not depend on. AQN-R1-NOISE-BAND should fix R1 before the next test.
4. **Should the evidence row wait for KERNEL-MEASURE-REFEREE?** No. The row is labelled exploratory and on proxy, moves no CLAIM_MAP status, and now says the lock is git-only, the key numbers were re-derived independently, and proxy validity was not refereed. KERNEL-MEASURE-REFEREE stays open, narrowed to proxy validity: variance risk premium, log of an expectation vs expectation of a log, overnight variance omitted, jumps / the Gaussian premise for the driver. This review covered its numerical scope (kernel derivation, like-with-like, noise treatment, band, bootstrap).

## Further finding: σ_pred
The locked σ_pred (0.0264) adds the α, ln q and ln ŝ2 SEs in quadrature. With the joint Whittle covariance (α–ln q correlation −0.83), and the noise effect taken as the total derivative along the profile (0.0012 per unit ln ŝ2, not the partial 0.039), σ_pred is **0.023**. σ_D is then 0.047, still above 0.040. Not re-scored: the locked constants stand, and the verdict (PASS, exploratory) is unchanged under every variant in `c4.json`. KERNEL-DECISIVE-RV's note is updated to match: a decisive design needs a smaller bootstrap SE of Ŵ21 (lower tracker or driver noise, intraday realized variance, or a second system), not a tighter α.

## Wording and goalposts
- THEORY §2.2, the §2.4 row and the Net sentence now each say on proxy and exploratory. No headline, premise, kill or math change. K13 stays MATH-CORRECTED, N13 OPEN, vigilance (H8) OPEN.
- `git diff 6d235ed origin/main -- tests/KERNEL_MEASURE/` adds only RESULTS.md, results.*, posthoc_bins.*. PREREG, decide.py, klib.py, gate, power and data are unchanged, and decide.py's constants match the PREREG. No other locked prereg is touched.
- Fixes applied: (F1) free-noise clause replaced, in THEORY and CLAIM_MAP; (F2) row status now reads "locked (git commit only, no external timestamp); key numbers re-derived by an independent reviewer, proxy validity not refereed"; (F3) "on proxy" added in §2.2 and the Net sentence; (F4) the long-lag bin "falls to about zero (last bin slightly negative)"; (F5) changelog review paragraph; CLAIM_MAP v2.28 header says merged after review. Versions: v1.4.10 and v2.28 were still free on main (open PR #60 uses v1.4.11).
- `tests/KERNEL_MEASURE/RESULTS.md` is not edited (author's post-lock record); this review corrects its §0 free-noise bullet.

## Prior art
None read; none credited.
