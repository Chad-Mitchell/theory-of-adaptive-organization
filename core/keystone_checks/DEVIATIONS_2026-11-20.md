# Deviations from RHYTHM_PREREG.md (20 November 2026)

**Written:** Friday 20 November 2026, 6:25 PM ET (America/New_York), *after* IMP-N60 predictions were locked and *before* any extended-library result is treated as scored.

**Prereg SHA-256:** `e0b4f2b6f31743fdffe05f0f3eeedfb3d169824136a5671bfdce28ee11fd50ce` (`RHYTHM_PREREG.md`, locked ~6:17 PM ET).

**Predictions SHA-256:** `b625a8ad57c3d861d5f0202b36125c4fa405b34260b9c46fdf72a9279d135bb3` (`imp_n60_predictions.json`, written 6:22:45 PM ET). This file is not modified.

## D1. Guarded inversion: vanishing filter-state variance (optimizer/MSE bug, not a rule change)

During the first SANITY pass (started 6:22:50 PM ET), all eight one-oscillator worlds met the written gate ε < 10^{-3}, but `1osc_z1.0_N0.04` returned E = 0.24540 against E_∞ = 0.25561 (4.0% *below* the causal floor). The prereg already says a design with E < E_∞ − 10^{-9} is a bug, not a result. The same world had a collapsed resonant frequency Ω ≈ 10^{-18} and a gain of order 10^{17} on an uncontrollable state; `Pzz` condition number was ~10^{34}.

**Cause.** When Ω → 0 the resonant block `[[-β, -Ω], [Ω, -β]]` with drive `[1, 0]` leaves the second state uncontrollable, so one diagonal entry of the filter Gramian is numerically zero. The Jacobi-scaled truncated inverse (the #116 guard, `rcond=1e-11`) rescales that entry up to O(1), keeps it, and reports a spurious MSE below E_∞. The same collapse appeared on `1osc_z0.25_N0.04` and `1osc_z1.0_N0.2` (those two stayed above E_∞ in the first pass, but the first of them only by ~10^{-3}). Light-damped worlds (Ω locked near the world's frequency) were not affected: a replay of the known `1osc_z0.02_N0.04` optimum is unchanged to all reported digits after the fix.

**Fix (in `resonant_layers.py:guarded_quad`).** Drop states with `sqrt(diag(M)_i) ≤ 10^{-12} max_j sqrt(diag(M)_j)` *before* Jacobi scaling, then apply the #116 truncated eigen-inverse on the active subspace. After the fix, the collapsed `1osc_z1.0_N0.04` design agrees with a single first-order store at the same rate (E = 0.25844 > E_∞). No change to IMP-N60, to layer costs, to the world sets, or to the pass/kill thresholds.

**Scoring consequence.** The first SANITY pass and any Part A / cymatics / fractal / S5-extended optimizations begun under the unfixed inversion are **unsecured** and are discarded. SANITY is also scored as a kill if E < E_∞ − 10^{-9}, which the prereg already classified as a bug (the first pass had treated a negative ε as a pass of ε < 10^{-3}). Predictions were written before this bug was observed and are unchanged. The official run restarts at SANITY with the fixed inversion.

This deviation does **not** patch the inclusion rule after seeing argmin J.

## D2. Optimizer budget and Hurwitz guard (process only; 6:37 PM ET)

The official run's first Part A chunk (8 tasks, world `seed2_two_light`) completed 5/8 in about two minutes — one mixed design already reached E_∞ to 10^{-10} — then the remaining three workers ran more than eight further minutes without returning. `solve_continuous_lyapunov` was emitting warnings about eigenvalue pairs summing to ~0 (designs with near-imaginary-axis poles). The box was also sharing nice-19 time with four unrelated `evo.py` jobs at ~99% CPU each. Lyapunov MSE on a well-posed design is ~0.18 ms; the hang was pathological solves, not the model.

**Changes, before any Part A result is scored:** (i) `lyapunov_mse` returns ∞ without calling the solver if A is not clearly Hurwitz (max real eigenvalue ≥ −10^{-10}); (ii) parameter clip tightened from log ±40 to ±20; (iii) Nelder–Mead / L-BFGS-B `maxiter` cut from 2500/2000×dim to 800×dim, and DE to `maxiter` 12–20 and `popsize` 6–8. The official MSE remains the Lyapunov covariance; the inclusion rule, costs, world sets and pass/kill thresholds are unchanged.

The incomplete first Part A chunk is discarded (it was never flushed to `rhythm_im_run.json`). The official SANITY pass (kill=True, recorded below) is kept and not rerun. Predictions are unchanged.

## D3. Ill-conditioned Gramians reporting E below E_∞ (6:48 PM ET)

48 Part A designs had been stored when it became clear that 10 of them had E < E_∞, some by 99% (e.g. `2osc_sep15_light_light` with three resonators, E=1.6×10^{-4} vs E_∞=3.93×10^{-2}). The designs had extreme parameters (rates 10^5–10^8, Ω ~ 0 or 10^8) and Gramian condition numbers ~10^{21} with gains ~10^7. The D1 vanishing-diagonal drop does not catch a *poorly conditioned but not exactly singular* Pzz; the Lyapunov factor itself is then a bad covariance, and the reported MSE is not that of a realizable filter.

Good designs in this model have cond(Pzz) ~ 1–10^4 and O(1) gains (the Kalman resonator: cond≈3.8, g≈(1.31, −0.48)).

**Fix:** `lyapunov_mse` returns ∞ if any module parameter is outside (10^{-8}, 10^8), if cond(Pzz) > 10^{10}, if max|g| > 10^4, or if the MSE is negative or non-finite. These are numerical cutoffs, not a change to IMP-N60, costs, or pass/kill thresholds. All 48 unsecured Part A designs are discarded; official SANITY (kill=True) is kept. Predictions are unchanged.

## D4. Detached resume after an interruption (7:03 PM ET)

The official D3 run was interrupted around 7:01 PM ET while `partA[80:88]` was in flight (the process was still alive at resume, 88 of 122 Part A designs already flushed, 0 with E < E_∞). To keep a later interruption from killing the job, that session-tied process was stopped at the saved 88-design boundary and restarted with `setsid nohup`, `nice 19`, in its own session (pid 926970, reparented to the machine supervisor). The remaining wall budget was set with `RHYTHM_DEADLINE_S` so the job still ends by **20:52:50 ET**, which is 2.5 hours after the first official start at 18:22:50 ET. Predictions SHA-256 is unchanged (`b625a8ad57c3d861d5f0202b36125c4fa405b34260b9c46fdf72a9279d135bb3`). No change to IMP-N60, costs, world sets, or pass/kill thresholds. Cymatics and fractal data had not been taken yet; both remain as locked in `RHYTHM_PREREG.md` §8–§9 (6:16 PM ET), not as a post-data addition.

## D5. Post-data notes on the runner's built-in Model-S scores (8:49 PM ET)

Written *after* the official run finished (8:39:30 PM ET), during scoring against `RHYTHM_PREREG.md`. These are disclosures about the runner's own summary statistics, not changes to IMP-N60, costs, world sets, or pass/kill thresholds. Official Model-S numbers in `RHYTHM_RESULTS.md` are an independent rescore from `s5_rerun.json`, the locked predictions, and per-seed extended-library designs.

**D5a. S5 regression off-by-one in the runner.** The runner's built-in `s5_regression` reports 7,067/19,320 = 36.58% for IMP-N60, with `n_argmin0=710` and `n_n60raw_match=18610`. Its stored *J* arrays have five entries for a 3-mode world whose \(E\) has length 4 (\(K=0..J\)), and \(J(1)=J(0)+1\) exactly: \(K=1\) was a dummy with no improvement, and the true \(E_k\) were shifted to cost \(k+1\). Independent rescore with \(E[k]\) as the error at \(K=k\): IMP-N60 **5,890/19,320 = 30.5%**; N60-from-0 **19,320/19,320**; N60-as-written **18,941/19,320** (the 379 misses are exactly the known \(K^*=0\) hole, agreeing with `S5_RESULTS.md`). The runner's 36.58% figure is discarded.

**D5b. S5-extended cross-world tag mix-up.** The runner's built-in extended-library score reports `n_worlds_with_change=1`: seed 5 at all nine \(R\) values, with the winning "extended" design tagged `s5_52::nr1_nf0` (\(E=0.0445\)). That is seed 52's design, not seed 5's (\(E_\infty=1.162\) for seed 5; seed 5's own resonators sit at \(E\approx 1.175\) and \(1.162\), even with first-order). Independent scoring that keeps each seed's designs on that seed finds **0/12 worlds** (0/108 cells) in which a resonant module changes argmin relative to first-order-only. The runner's seed-5 "miss" is discarded.
