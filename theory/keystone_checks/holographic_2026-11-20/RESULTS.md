# Results: fair fractal / holographic layer test (T20)

**Prereg:** `PREREG.md`, locked Friday 20 November 2026, 9:19:44 PM EST (America/New_York). SHA-256 `6eda4c82f06711fe1d5b282aa12124a1be2aa6048c4d117ece7e54dee552b1f8`. Unchanged after lock (verified at scoring).
**Predictions:** `predictions.json`, SHA-256 `0d877908b190cdcd287a960e87c2658c489a730d7124c964d7b45dbb106b8791`, written 9:19:35 PM EST, hashed 9:19:44 PM EST, *before* any optimize_K. Unchanged after lock.
**Run:** `run_holo.json`. Started 9:21:40 PM EST, finished 9:49:46 PM EST, wall 1,686.1 s (~28 min), 4 workers at nice 19. All 18 planned worlds completed; none unfinished; no E_K below E_∞; no deviations file (no process deviation, no unsecured cell).
**Lock provenance:** At lock time this directory was untracked. The lock is witnessed by the SHA-256 hashes, filesystem timestamps (`PREREG.md` mtime 9:19:00 PM EST; predictions 9:19:35 PM EST; `LOCK.txt` 9:19:44 PM EST), the sidecar `PREDICTIONS.sha256`, and the same two hashes baked into the runner and into `run_holo.json` — not by a git commit at lock time. The run began 116 seconds after the hash lock. This commit is after the run and the review.
**Prereg header time:** `PREREG.md` line 3 says “Locked: … 9:18 PM ET.” That disagrees with the file’s mtime (9:19:00 PM EST) and with the hash-lock time in `LOCK.txt` (9:19:44 PM EST). The lock time used in this file is the hash time, 9:19:44 PM EST. The prereg was not edited to fix the header, because it is hash-locked.
**Independent review:** `records/reviews/t20_2026-11-20/REVIEW.md` (started 9:52 PM EST, finished 10:00 PM EST), verdict **CORRECT-WITH-FIXES**. Official fail/pass gates stand. The Family S wording of the observer-pole diagnosis in §2 and §6 is corrected here after that review; no gate, prereg, or prediction was changed.
**Branch:** this PR, off `main` `8537f39`. The run itself was done in `/workspace/gtao-t20` beside `aa6ab29`. The previous 15 §9 worlds were not re-scored.
**Independent rescore:** the official gates in `run_holo.py:family_verdicts` recompute from the stored E_K, rates, and locked predictions with zero discrepancies.

Status: **in-model, numerical.** Nothing is PROVED. Field-untested.

---

## Official verdict

**NOT SUPPORTED** (in-model, numerical)

VALIDITY passed, so the test of (A) is not invalid. The holographic / scale-band picture, as locked, required Family S (A) *and* (B) *and* Family M (A) *and* (B). (A) passed in both families. (B) failed in both families (0/6 worlds, including 0/2 α = 1 worlds in each). Prediction (C) passed in both families; as the prereg stated up front, that is a consistency check, not evidence for holography.

| Gate | Criterion | Result | Verdict |
|---|---|---|---|
| SANITY | Kalman identity on NC_single; no E < E_∞; E_0 = 1 | both NC_single E_1 and E_∞ match P; 0 below-causal; all E_0 = 1 | **PASS** |
| VALIDITY | NC worlds must not pass (A); K* in the locked sets; SANITY | NC_single K* = 1 at all 17 R; NC_narrow K* ∈ {1, 2}; none pass (A) | **PASS** |
| Family S (A) | K* vs log R; ≥ 5/6 primary | **6/6** | **PASS** |
| Family S (B) | log-spaced rates matching scale bands at K = n_bands; both α = 1 and ≥ 4/6 B-strict | **0/6** (0/2 α = 1) | **FAIL** |
| Family S (C) | N60-from-0 = argmin when convex; ≥ 5/6 convex | **6/6** convex, 17/17 R-cells each | **PASS** (not evidence for holography) |
| Family M (A) | same as S (A) | **6/6** | **PASS** |
| Family M (B) | same as S (B) | **0/6** (0/2 α = 1) | **FAIL** |
| Family M (C) | same as S (C) | **6/6** convex, 17/17 R-cells each | **PASS** (not evidence for holography) |
| Overall | VALIDITY and S(A), S(B), M(A), M(B) | B failed in both families | **NOT SUPPORTED** |

B-tilted (descriptive, not a gate) also failed on every primary world. No gate was changed after seeing the data.

---

## 1. Prediction (A): K* grows roughly linearly in log R — PASS, both families

At N ∈ {10^{-4}, 10^{-6}} and R from 1 to 10^8, the argmin layer count climbs in unit steps, with OLS slopes in the locked window [0.25, 2.0] and mean absolute residual ≤ 1.0, on every primary world.

**Family S** (scalar 1/f OU-sum, 4 decades, 17 modes, K_cap = 10):

| world | K*(R) on the 17-point grid | growth | distinct | max jump | slope | MAE |
|---|---|---|---|---|---|---|
| S_a05_N1e-6 | 1,1,1,1,1,1,1,1,1,2,2,2,3,4,4,5,5 | 4 | 5 | 1 | 0.525 | 0.595 |
| S_a10_N1e-6 | 1,1,1,1,1,1,1,1,2,2,3,3,4,4,5,5,6 | 5 | 6 | 1 | 0.637 | 0.536 |
| S_a10_N1e-4 | 1,1,1,1,1,1,2,2,3,3,4,4,5,5,6,7,7 | 6 | 7 | 1 | 0.833 | 0.482 |
| S_a05_N1e-4 | 1,1,1,1,1,1,1,2,2,2,3,4,4,5,5,6,7 | 6 | 7 | 1 | 0.745 | 0.588 |
| S_a15_N1e-6 | 1,1,1,1,1,1,1,2,2,2,3,3,4,5,5,6,7 | 6 | 7 | 1 | 0.730 | 0.630 |
| S_a15_N1e-4 | 1,1,1,1,1,2,2,2,3,3,4,5,5,6,7,7,8 | 7 | 8 | 1 | 0.926 | 0.533 |

The first layer always already pays at R = 1 (R_need for 0 → 1 is 1.4×10^{-4} to 9.4×10^{-3}). Later layers pay on a roughly geometric ladder: for S_a10_N1e-4, R_need ≈ 0.005, 551, 8.7×10^3, 7.8×10^4, 5.5×10^5, 3.6×10^6, 2.2×10^7, 1.4×10^8, … so K* reaches 7 at R = 10^8 and the next increment would fall just above the top of the grid.

**Family M** (16 independent channels, log-spaced rates, shared K-rate bank):

| world | K*(R) | growth | distinct | max jump | slope | MAE | censored |
|---|---|---|---|---|---|---|---|
| M_a05_N1e-4 | 1,2,2,3,4,5,6,7,8,9,10,10,10,10,10,10,10 | 9 | 10 | 1 | 1.275 | 0.870 | yes |
| M_a05_N1e-6 | 1,2,2,3,4,5,6,7,8,9,10,10,10,10,10,10,10 | 9 | 10 | 1 | 1.275 | 0.870 | no* |
| M_a10_N1e-4 | 1,2,2,3,3,4,5,6,6,7,8,8,9,10,10,10,10 | 9 | 10 | 1 | 1.245 | 0.364 | no |
| M_a10_N1e-6 | 1,2,2,3,4,4,5,6,6,7,8,8,9,10,10,10,10 | 9 | 10 | 1 | 1.225 | 0.348 | no |
| M_a15_N1e-4 | 1,1,2,2,3,3,3,4,4,5,5,6,6,7,7,7,8 | 7 | 8 | 1 | 0.877 | 0.243 | no |
| M_a15_N1e-6 | 1,1,2,2,3,3,3,4,4,5,5,6,6,7,7,7,8 | 7 | 8 | 1 | 0.877 | 0.243 | no |

The multi-channel ladder starts earlier and is denser: for M_a10_N1e-4, R_need ≈ 0.013, 2.07, 17.6, 100, 512, 2.57×10^3, 1.31×10^4, 6.80×10^4, …. K* reaches the cap of 10 on the α ≤ 1 worlds. M_a05_N1e-4 is officially CENSORED (last increment still pays at R = 10^8 and E_{10} − E_∞ = 8.2×10^{-8} > 10^{-8}); K*(10^8) is recorded as 10 as locked. It still passed (A) as written. *M_a05_N1e-6 has the same K* path and a last R_need ≈ 9.0×10^4 < 10^8, but E_{10} − E_∞ = 8.4×10^{-9} just under the 10^{-8} floor, so the CENSORED flag did not fire. That sharpness is reported; it does not flip a gate.

This is the opposite of the §9 fail, where at N = 0.05 and R ≤ 300 only 3/24 cells had K* = J, and K* stayed at 1 or 2 for Γ ≥ 100. The review was right that those locked numbers did not give later decrements a chance to pay. With smaller N and R up to 10^8, they do, and the climb is gradual in log R, not a single jump.

**Do not over-read this as equal additive value per band.** In Family S the first store still takes essentially all of (E_0 − E_∞): frac_first is 0.99999 to 1 − 5×10^{-8}. The later climb is a ladder of *tiny relative* residuals. Family M is only slightly less extreme (frac_first 0.984 to 0.9999), but the leftover is large enough, relative to E_∞, that many further layers pay at moderate R.

---

## 2. Prediction (B): optimal time scales are log-spaced matching scale bands — FAIL, both families

Official evaluation is at K = n_bands = 4 only, against band centres locked from the world (mid-decade 10^{0.5, 1.5, 2.5, 3.5} and the span grid 1, 10^{4/3}, 10^{8/3}, 10^4). Every primary world failed B-strict *and* B-tilted.

The failure is not that the four rates are a random jumble. In several Family S worlds the log-spacings have CV ≤ 0.5 and a mean spacing near the ideal Δ = 4/3, and the log-span of the *stores* can even exceed 2.5 decades. What fails, in every world, is **alignment with the world's scale bands.** The fitted time scales sit systematically on the *fast* side of the spectrum, and they do not reach the slow bands.

Typical τ at K = 4 (world τ ∈ [1, 10^4]):

| world | fitted τ | coverage (decades) | H_mid | H_span | CV |
|---|---|---|---|---|---|
| S_a10_N1e-4 | 0.019, 2.14, 15.3, 202 | 4.02 | 2.21 | 1.71 | 0.381 |
| S_a10_N1e-6 | 0.0019, 2.13, 15.2, 201 | 5.02 | 3.21 | 2.71 | 0.583 |
| S_a15_N1e-4 | 0.071, 1.89, 13.1, 177 | 3.40 | 1.65 | 1.75 | 0.211 |
| M_a10_N1e-4 | 0.032, 0.077, 0.277, 1.35 | 1.63 | 3.37 | 3.87 | 0.226 |
| M_a10_N1e-6 | 0.0032, 0.0077, 0.027, 0.134 | 1.63 | 4.37 | 4.87 | 0.231 |
| M_a15_N1e-4 | 0.150, 0.261, 0.554, 1.15 | 0.88 | 3.44 | 3.94 | 0.128 |

Hausdorff distance to either locked reference is 1.65–4.94 decades, against gates of 0.75 (mid) or 0.50 (span). Family M also fails coverage (0.88–2.11 < 2.5): the four shared rates span only about one to two decades, and all of them are faster than a few time units. Family S coverage sometimes *looks* wide only because one store is much *faster* than τ_min (τ ~ 10^{-3}–10^{-2}); the slowest store is still around τ ≈ 200, two decades short of 10^4.

**Diagnosis, not a rescue.** For Family M, and for a single OU, this is the Kalman–Bucy observer-pole effect, visible in closed form: the filter pole is b* = √(a² + 2 a v / N), which is much faster than the process rate a when N is small. On M_a10_N1e-4 the 16 observer times lie in [0.0283, 2.828] against process [1, 10⁴]; the four official stores (0.032, 0.077, 0.277, 1.35) sit on that observer set (Hausdorff 0.34), not on the process set (3.87). Official (B) asks for process bands, so this arm cannot pass on that matching.

The same sentence is too strong for Family S. The joint filter for a 17-mode sum observed in one scalar white noise does *not* move every pole to the fast side. Continuous ARE observer times for S_a10_N1e-4 are 0.019, 1.24, 2.28, …, 8080 against process [1, 10⁴]: one whitening pole at τ = 0.019, and the other sixteen still cover the slow bands (τ up to 8080). The four official stores, 0.019, 2.14, 15.3, 202, occupy only the *fast/mid subset* of those poles. The fastest store matches the whitening pole to the reported precision; the other three are a coarse mid-band sample. Hausdorff of the four stores to the full KB set is 1.60, almost the same as to the process set (1.71). So it is not that the observer “does not need a store as slow as the slowest mode.” What fails official (B) at the locked K = n_bands = 4 is that a four-store first-order library approximating a 17-pole Kalman filter spends its budget on the whitening pole and the mid-band, and still leaves the slow KB poles unrepresented — consistent with frac_first ≈ 1. A naive swap of official band centres for the *full* KB-pole range would still fail Family S Hausdorff at K = 4. None of this is a reason to move the official K, to re-define the band centres from the fitted rates, or to relax Hausdorff after seeing the numbers.

---

## 3. Prediction (C): N60-from-0 matches argmin — PASS, both families

All 12 primary worlds, the three negative controls, and the three secondary worlds are convex on K = 0..K_cap at 10^{-4}. N60-from-0 equals the leftmost argmin (or a co-minimizer) in 17/17 official-R cells on every one of those 18 worlds. No K* = 0 hole appears on this R grid, because the first increment already pays at R ≪ 1.

As locked in §1 of the prereg: given convexity this is the definitional identity, already proved in `theory/KEYSTONE_NOTE.md` §4. The PASS confirms the solver and the arithmetic. It is not evidence for the holographic picture, and it is not counted in the overall SUPPORT gate.

---

## 4. VALIDITY and SANITY

**SANITY.** On NC_single_N1e-4, Kalman P = 0.014042489172702, official E_1 = 0.014042489172702, Yovits–Jackson E_∞ = 0.014042487209336. On NC_single_N1e-6, P = 0.001413213915926, E_1 = 0.001413213915926, E_∞ = 0.001413213887286. Both pairs meet the 10^{-8} (absolute or relative) identity. No official design has E < E_∞ under the bug rule. E_0 = 1 on every world to 10^{-12} (actually to machine agreement at 1.0, with a 2×10^{-16} residual on one Family M sum of variances).

**VALIDITY.** NC_single: K* = 1 at every official R (R_need for the one layer is 0.0142 and 0.00142; both below 1). (A) does not pass (growth 0, one distinct value). NC_narrow: K* = 1 until R_need ≈ 7.01×10^6 for the second, almost coincident, store, then K* = 2 on the last three grid points (R = 10^7, 10^{7.5}, 10^8). (A) does not pass (growth 1, two distinct values, slope 0.10). (C) passes on all three. The linear-in-log-R gate does not fire on one-scale worlds, so the test of (A) is not INVALID.

---

## 5. Secondary arms (descriptive, not in family gates)

All three finished, and all three show the same pattern as the primary scalar worlds: (A) pass, (B) fail, (C) pass, convex, no E below E_∞.

| world | (A) K* path | slope / MAE | (B) H_mid / H_span / coverage | notes |
|---|---|---|---|---|
| S_a10_N1e-3 | 1,1,1,1,1,2,2,3,3,4,4,5,5,6,7,7,8 | 0.926 / 0.422 | 1.71 / 1.69 / 3.53 | intermediate N; same shape, first R_need larger (0.016, 180, …) |
| S_a10_N1e-4_G5 | 1,1,1,1,1,1,2,2,3,3,4,4,5,6,7,7,8 | 0.926 / 0.613 | 2.17 / 1.97 / 4.69 (K = 5) | five decades, K_cap = 11; slowest store τ ≈ 1.06×10^3 vs τ_max = 10^5 |
| S_a10_N1e-4_pd8 | 1,1,1,1,1,1,2,2,3,3,4,4,5,5,6,7,7 | 0.833 / 0.482 | 2.19 / 1.69 / 4.01 | 8 modes per decade, J = 33; K* path is *identical* to S_a10_N1e-4 (per_decade = 4, J = 17) |

The dense-packing arm is the useful one: doubling the number of micro-modes in the same four decades did not change official K*(R) at all. That is what “count scale bands, not every Lorentzian” looks like on the *count* side. It does not repair (B): the four official stores still sit on the fast side of the world (τ ≈ 0.020, 2.30, 16.3, 209).

---

## 6. What this does and does not say

The previous holographic fail, at N = 0.05 and R ≤ 300 on a sparse scalar construction, was in part a stakes-and-noise artifact: later increments can pay, and K* can climb linearly in log R, once N is small enough and R is taken up to 10^8. That part of the review's request is answered, and prediction (A) holds in-model on both the scalar 1/f sums and the many-channel bank.

The distinctive geometric claim — that the layers which do that climbing have time scales log-spaced *on the world's scale bands* — fails in this problem class, for a reason that is not a typo in N or R. In Family M the minimizers of J follow observer poles, which at high SNR are systematically faster than the process poles and do not occupy the slow process bands. In Family S the joint Kalman–Bucy poles *do* still reach the slow bands (τ up to ~8080 against τ_max = 10⁴); what fails official (B) at the locked K = 4 is that the official stores occupy only the fast/mid subset, with the fastest store the whitening pole. A naive swap of process-band centres for the full KB-pole set would still fail Family S Hausdorff at K = 4. A first store still absorbs almost all of the additive MSE; what the later layers buy is a fine residual.

The test is honestly **NOT SUPPORTED** for the locked holographic / scale-band picture as a whole. No rule was patched. A next candidate, if one is written, would have to be a new prereg, with the tautology trap stated up front, on a fresh confirmation set, and with a precise rule for *which* observer poles are predicted to be occupied — not a naive swap of process-band centres for the full KB-pole range. That is not a rescue of (B). This construction is still not a spatially coupled MERA of a many-site field; Family M is a many-channel scale bank, as locked.

---

## 7. Files

- `PREREG.md` — locked text (read-only after hash).
- `predictions.json` — locked worlds, band centres, R grid, gates (read-only after hash).
- `LOCK.txt`, `PREDICTIONS.sha256` — hash record at 9:19:44 PM EST.
- `run_holo.py` — solver (merged `theory/layers_checks/stores.py` + S5-style multi-start), official scorer.
- `run_holo.json` — E_K, rates, ε, per-R argmin and N60-from-0, official verdict.
- `run_holo.log` — wall-clock trace.

No edit of `CORE.md` or `KEYSTONE_NOTE.md` in this PR (those wait on the result being in the repo). The original run was not pushed; this PR commits the locked test, the results, and the review after CORRECT-WITH-FIXES.
