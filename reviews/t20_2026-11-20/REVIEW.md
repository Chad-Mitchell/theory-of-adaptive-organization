# Independent hostile review: GTAO T20 fair holographic / fractal test

**Reviewer:** independent (wrote none of the prereg, predictions, runner, or results).
**Date:** 2026-11-20, started 9:52 PM EST, finished 10:00 PM EST (America/New_York).
**Targets:** `/workspace/gtao-t20/core/keystone_checks/holographic_2026-11-20/` — `PREREG.md`, `predictions.json`, `LOCK.txt`, `PREDICTIONS.sha256`, `build_predictions.py`, `run_holo.py`, `run_holo.json` / `.log`, `RESULTS.md`. Branch `t20-holographic-2026-11-20` beside `aa6ab29`.
**Constraints honored:** work at nice 19 in a copy under `/tmp/t20-review/`; originals not modified; no push; `/workspace/looper` not touched. Scoring was reimplemented from the locked prereg text (not by importing `run_holo.py` gate functions). All stored `E_K` were re-evaluated at the stored rates. `E_∞` was recomputed (Family M closed form; Family S Yovits–Jackson and, separately, the ARE `1^T P 1`). Process-band designs were scored for MSE against the fitted designs. Joint Kalman–Bucy poles were computed from the continuous ARE. The 28-minute optimizer was not rerun in full.

**Verdict: CORRECT-WITH-FIXES**

Every official gate recomputes from the stored `E_K`, rates, and locked predictions: Family S (A) 6/6 and Family M (A) 6/6 (12/12 primary), Family S (B) 0/6 and Family M (B) 0/6 (0/12 primary, 0/2 α = 1 in each, B-tilted also 0/12), (C) is the convexity identity (18/18 worlds convex, 17/17 official-R cells each), VALIDITY passes, SANITY passes, overall **NOT SUPPORTED**. Censoring follows the locked rule. Headline numbers in `RESULTS.md` match. The B failure is real, not an optimizer miss and not a typo in N or R.

The official diagnosis of that failure is mathematically right for Family M and for the single-OU formula it quotes, and is overstated for Family S (Issue 1). That does not flip a gate. Issue 2 is a process limitation on the lock (files are untracked). Issue 3 is a timestamp nit.

---

## Integrity

Hashes match the lock record and the run file:

| file | sha256 | mtime (EST) |
|---|---|---|
| `PREREG.md` (mode 444) | `6eda4c82f06711fe1d5b282aa12124a1be2aa6048c4d117ece7e54dee552b1f8` | 9:19:00 PM |
| `predictions.json` (mode 444) | `0d877908b190cdcd287a960e87c2658c489a730d7124c964d7b45dbb106b8791` | 9:19:35 PM |
| `LOCK.txt` / `PREDICTIONS.sha256` | both hashes recorded | 9:19:44 PM |
| `run_holo.py` | `ae50e353…` (not part of the hash lock) | 9:21:32 PM |
| `run_holo.pid` | pid 1349767 | 9:21:39 PM |
| `run_holo.json` `started_s` | — | **9:21:40.419 PM** |
| `run_holo.json` / `.log` finished | wall 1,686.069 s | **9:49:46.488 PM** |
| `RESULTS.md` | — | 9:51:45 PM |

Lock precedes the run by 116 seconds. `PREREG.md` and `predictions.json` are read-only; their ctimes (9:20:11 PM, chmod) are still before the run; mtimes were not updated after the hash lock. `run_holo.json` records the same two hashes. A rebuild of every world's `a`, `v`, `τ`, `J`, `K_cap`, and both locked band lists from the prereg formulae and merged `stores.scalefree_world` matches `predictions.json` exactly. The merged solver `theory/layers_checks/stores.py` is unchanged from `aa6ab29`.

The holographic directory is **untracked** on `t20-holographic-2026-11-20` (Issue 2). Git cannot independently witness the lock. Filesystem timestamps, the sidecar, the baked-in runner hashes, and the run file are consistent with lock-before-run, and there is no sign of a post-data edit to the prereg or predictions. `run_holo.py` was written (or last touched) after the hash lock and 8 seconds before start; that is the expected place to embed the hashes. An independent reimplementation of §§5.1–5.6 agrees with the official scorer on every world and every family gate.

The previous 15 §9 worlds were not reused. No `DEVIATIONS_*.md` exists; none is required. No official `E < E_∞` under the bug rule. Compute order in the log is NC, Family S primary, Family M primary, then secondary, as locked.

---

## Official gates (independent rescore)

Scoring used the prereg rules literally: leftmost argmin of `J(K) = K + R(1+ε_K)` with co-minima at `10^{-9} max(1,|J|)`; N60-from-0 strict; convexity at `TOL = 10^{-4}` on `K = 0..K_cap`; OLS of `k_i` on `log10 R_i`; Hausdorff in `log10 τ`; CV with `ddof = 0`; (B) only at `K = n_bands`; family thresholds 5/6 for (A), both α = 1 and ≥ 4/6 B-strict for (B), every convex primary and ≥ 5/6 convex for (C).

| Gate | Official | Independent | Match |
|---|---|---|---|
| SANITY | PASS | PASS (Kalman identity, no E below causal, all `E_0 = 1` to `2.2×10^{-16}`) | yes |
| VALIDITY | PASS | PASS | yes |
| Family S (A) | 6/6 PASS | 6/6 PASS | yes |
| Family S (B) | 0/6 FAIL (0/2 α = 1) | 0/6 FAIL, B-tilted 0/6 | yes |
| Family S (C) | 6/6 convex, 17/17 | 6/6, 17/17 | yes |
| Family M (A) | 6/6 PASS | 6/6 PASS | yes |
| Family M (B) | 0/6 FAIL (0/2 α = 1) | 0/6 FAIL, B-tilted 0/6 | yes |
| Family M (C) | 6/6 convex, 17/17 | 6/6, 17/17 | yes |
| Overall | NOT SUPPORTED | NOT SUPPORTED | yes |
| Secondaries | (A) pass, (B) fail, (C) pass | same, all three | yes |
| NC (A) | must not pass | none pass | yes |

NC_single: `K* = 1` at all 17 R, growth 0, one distinct value. NC_narrow: `K* = 1` then `2` on the last three grid points (`R = 10^7, 10^{7.5}, 10^8`), growth 1, two distinct values, slope 0.1029 (quoted 0.10). Kalman identity: `P = E_1` to `~10^{-16}`; `E_∞` differs from `P` by `1.96×10^{-9}` and `2.86×10^{-11}`, inside the locked looser of absolute / relative `10^{-8}`. Quoted P, E_1, and E_∞ agree to the last reported digit.

Stored `E_K` re-evaluate at the stored rates with no discrepancies. All primary and secondary `E` sequences are monotone except `M_a15_N1e-6` at `K = 10`, where `E` rises by `6.1×10^{-15}` (`Δε ≈ -1.3×10^{-11}`), far inside `TOL`. Official convexity is still true as locked. Every official-R N60-from-0 cell matches the leftmost argmin or a co-minimizer. That is the identity the prereg already flagged as not evidence for holography.

Quoted (A) paths, growth, distinct counts, max jump (all 1), slopes, and MAE agree after ordinary 3-decimal rounding (e.g. S_a10_N1e-4 slope `0.833333` / MAE `0.482122`; M_a05 MAE `0.869666` quoted 0.870). Quoted (B) `τ`, coverage, `H_mid`, `H_span`, and CV agree (Hausdorff range 1.6505–4.9416, quoted 1.65–4.94; Family M coverage 0.8847–2.1060, quoted 0.88–2.11). Quoted `R_need` ladders and `frac_first` ranges agree (`1.412×10^{-4}`–`9.358×10^{-3}` quoted `1.4×10^{-4}` to `9.4×10^{-3}`; Family S `frac_first` `0.99999` to `1-4.5×10^{-8}`, quoted to `1-5×10^{-8}`; Family M `0.98381`–`0.99990`, quoted 0.984 to 0.9999). Secondary `S_a10_N1e-3` first `R_need` is `0.01618`, `179.94` (quoted 0.016, 180). The pd8 `K*` path is identical to `S_a10_N1e-4`, as claimed.

Censoring: `M_a05_N1e-4` is the only flagged world. Last increment still pays (`R_need ≈ 9.058×10^4`) and `E_{10}-E_∞ = 8.238×10^{-8}` (quoted `8.2×10^{-8}`), both limbs of §2. `K*(10^8)` is recorded as `K_cap = 10` as locked; (A) still passes as written (growth 9, slope 1.2745, MAE 0.8697). `M_a05_N1e-6` has the same `K*` path and `R_need ≈ 8.989×10^4` (quoted `9.0×10^4`) but residual `8.377×10^{-9}` (quoted `8.4×10^{-9}`), just under the `10^{-8}` floor, so the flag does not fire. That sharpness is reported and does not flip a gate. Two further worlds (`M_a10_N1e-4`, `M_a10_N1e-6`) also have a last increment that pays and a residual under the floor (`1.28×10^{-9}`, `1.31×10^{-10}`); those are in the JSON and are not called out in the writeup (see notes). Remaining residual at `R = 10^8` is small; raising `K_cap` would not have failed (A).

---

## World construction

Family S is the merged `scalefree_world`: `τ` log-spaced in `[1, 10^4]`, `v ∝ τ^{α-1}`, `J = 17` at `per_decade = 4` (21 at five decades, 33 at `per_decade = 8`). That is exactly four decades, denser than the failed §9 construction (`per_decade = 1`). The composite Lorentzian spectrum in the interior band has mid-band log-log slope `-1.0000` at `α = 1` (MAE in `log10 S` of 0.025, max ripple 0.082). At `α = 0.5` and `1.5` the mid-band slopes are `-0.57` and `-1.43` against `-0.50` and `-1.50` (MAE 0.037). That is a fair 1/f-like sum, exact at the flat-per-decade case, with the usual discrete-mixture ripple; it is not a reason to reject the construction.

Family M is 16 independent log-spaced channels, `τ_m = 10^{4(m-1)/15}`, same variance rule, as locked. It is a many-channel scale bank, not a spatially coupled MERA, and is labelled as such.

Negative controls are the locked one-OU and two nearly coincident OU worlds. Band centres are the locked mid-decade list `10^{0.5,1.5,2.5,3.5}` and span grid `1, 10^{4/3}, 10^{8/3}, 10^4`, computed from the world only.

---

## Why (B) fails — and where the official diagnosis needs a fix

B is not an optimizer artefact. The S5-style search box includes rates slower than `τ = 10^4` and faster than `τ_min`; inits include a log-spaced grid on the process rates. Every official method tag is Nelder–Mead (DE and L-BFGS-B were run for `K ≤ 6` and lost). Placing the four stores on either locked process-band list is much worse than the fitted design on every primary and secondary world (e.g. `S_a10_N1e-4`: `E_fit = 0.005136` against `E_mid = 0.164` and `E_span = 0.085`, with `E_∞ = 0.005136`; Family M gaps are the same order). The official rates really do minimise `J` on this library, and they really do not sit on the world's scale bands.

**Family M (and the single-OU formula): the explanation is right.** For an isolated OU the stationary Kalman–Bucy pole is `b* = √(a² + 2av/N)`, so `τ_obs ≈ √(N τ / (2v))` at high SNR, much faster than the process time `τ`. On `M_a10_N1e-4` the 16 observer times lie in `[0.0283, 2.828]` against process `[1, 10^4]`; the four fitted stores are `0.032, 0.077, 0.277, 1.35` (Hausdorff 0.34 to the observer set, 3.87 to the process set). At `K = 10` the fitted bank is `[0.028, …, 2.759]`, essentially the full observer range. `N = 10^{-6}` scales the same picture down by 10. That is the closed-form shift, and it is why (B) cannot pass on this arm: official (B) asks for process bands.

**Family S: the same sentence is too strong (Issue 1).** The joint filter for a 17-mode sum observed in one scalar white noise does *not* move every pole to the fast side. Continuous ARE observer times for `S_a10_N1e-4` are

`0.019, 1.24, 2.28, …, 8080`

against process `[1, 10^4]`. There is one whitening pole at `τ = 0.019`, and the other sixteen poles still cover the slow bands (`τ` up to 8080). The four official stores, `0.019, 2.14, 15.3, 202`, sit on the *fast/mid subset* of those poles: the fastest store matches the whitening pole to the reported precision, and the other three are a coarse mid-band sample. Hausdorff of the four stores to the full KB set is 1.60, almost the same as to the process set (1.71). At `K = 10` the library does reach slower scales (`τ_slowest ≈ 2×10^3`–`5×10^3`). `1^T P 1` agrees with stored `E_∞` to relative `~5×10^{-9}`, so this is the same filter the solver is approximating.

So “layers follow observer poles, not process poles” is exact for Family M. For Family S, what fails official (B) at the locked `K = n_bands = 4` is that a four-store first-order library approximating a 17-pole Kalman filter spends its budget on the whitening pole and the mid-band, and still leaves the slow KB poles unrepresented — consistent with `frac_first ≈ 1`. It is not that the observer “does not need a store as slow as the slowest mode.” A next prereg that simply replaces process-band centres by the *full* KB-pole range would still fail Family S Hausdorff at `K = 4`. Any observer-band successor still needs a fresh prereg, a tautology guard, and a precise rule for *which* observer poles are predicted, as the results already say in general terms.

None of this is a rescue of (B). The locked geometric claim is false in this problem class, for a structural reason, and is correctly scored FAIL / NOT SUPPORTED.

---

## Overstatement check

The writeup does not over-claim the overall result. Status is in-model, numerical, not proved, field-untested. (C) is not counted as holographic evidence. (A) is not read as equal additive value per band; `frac_first` is reported. Family M is not called a MERA. The previous §9 fail is described as “in part” a stakes-and-noise artefact, which is fair: (A) now passes and (B) still fails. No gate was moved after the data. The suggested observer-band successor is explicitly not a rescue of (B). The one overstatement is the Family S wording of the observer-pole mechanism (Issue 1).

---

## Numbered issues

**1. (Fix in `RESULTS.md` §2 / §6; does not flip a gate.) Family S observer-pole diagnosis is overstated.**

The closed-form `b* = √(a² + 2av/N)` and the claim that official rates sit on observer scales, not process scales, are right for Family M and for a single OU. They are not right as stated for the scalar many-mode arm. Joint Kalman–Bucy poles of the Family S worlds still occupy the slow bands (`τ` up to ~8080 against `τ_max = 10^4`). The four official stores occupy only the fast/mid subset; the fastest store is the whitening pole. Replace the Family S sentence “it does not need a store as slow as the slowest mode / the same shift appears in the many-mode fits” with that distinction. Note also that a naive swap of official band centres for the full KB-pole set would not automatically pass (B) on Family S at `K = n_bands`.

**2. (Process; does not flip a gate.) The locked files are not in git.**

Branch `t20-holographic-2026-11-20` points at `aa6ab29` with `core/keystone_checks/holographic_2026-11-20/` untracked. The lock cannot be verified from a clone, only from this working tree’s timestamps and `LOCK.txt`. Those checks pass (lock 9:19:44 PM EST, run 9:21:40 PM EST, hashes stable). Commit the prereg, predictions, and lock record if this test is kept.

**3. (Nit.) Prereg header time disagrees with the hash lock.**

`PREREG.md` line 3 says “Locked: … 9:18 PM ET.” The file’s mtime is 9:19:00 PM EST; `LOCK.txt` and `RESULTS.md` use 9:19:44 PM EST. Harmless, but the lock time should be the hash time.

---

## Notes (not issues)

- Mid-band spectral slope at `α ≠ 1` is off by about 0.07 with four Lorentzians per decade. `α = 1` is exact. Fair construction, not a validity problem.
- `M_a10_N1e-4` and `M_a10_N1e-6` also finish with a paying last increment and a residual under the `10^{-8}` floor, so they are not flagged CENSORED. The residuals are in `run_holo.json`. This does not change (A) or the overall verdict.
- `M_a15_N1e-6` has a `6×10^{-15}` uptick in `E` at `K = 10`, inside locked convexity tolerance.
- All 155 official optimizations are tagged Nelder–Mead. That is a best-of-inits label, not evidence that DE / L-BFGS-B were skipped for `K ≤ 6`.

---

## Bottom line

The test was locked before it was run, the hashes match, the scoring matches the locked rules exactly, the 1/f construction is a fair four-decade sum, and censoring is applied as written. Official result **NOT SUPPORTED** stands. Fix the Family S wording of the observer-pole explanation before treating that diagnosis as settled; do not patch (B).
