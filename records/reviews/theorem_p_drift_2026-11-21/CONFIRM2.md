# Blind confirm: PR #149 after the CE7 repair and the merge of main (CONFIRM2)

**Confirmer:** independent. Wrote none of the note, the checker, the tests, `REVIEW.md`, or `CONFIRM.md`.
**Date:** Sunday 22 November 2026 (UTC).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/149
**Head confirmed:** `f9f7482939ec6e11349c8e1b74c894a512b806ed` on `theorem-p-drift-2026-11-21`. Parents: `18614327abd22c832ead2a540f53d762f3bb16e0` (the fix) and `8e829e561aff27bcc3db0f69efd62620111f787d` (`origin/main`, merge of PR #145). Prior confirm `CONFIRM.md` is of `9489486`, verdict NOT READY. Draft. Not merged.

**Verdict: READY**

No blocker and no correction. `CONFIRM.md` had one blocker (the stock `I(M_T; X_T) = 10.63` was not the mutual information of the construction, and the checker and the test locked it) and one should-fix (two summaries still said the stock form fails). Commit `1861432` repairs both. The merge `f9f7482` renumbers the note to v2.74, leaves section S (v2.72) and N64 (v2.73) byte-identical to `8e829e5`, and sets the live tally at 344 rows.

## Items

None. No correction.

## CE7, rederived

World: `Z ~ N(0,1)`, `G_t` i.i.d. `N(0,1)`, independent, `X_t = t Z + G_t`. Looks `Y_t = X_t + N_t`, `N_t ~ N(0,1)`, at `t = 2^k` only. The memory that drives the action is the posterior mean `μ_t = E[Z | looks so far]`. The posterior variance is deterministic: prior `v = 1`, and a look at scale `t` has noise variance 2, so `v ← 2v / (t² v + 2)`. With `u = t² v` and `t` doubling, `u ← 8u / (u + 2)` from `u = 1`. The map fixes `u = 6` and increases toward it, so the pre-look mean squared error `u + 1` stays below 7. Fresh `G_{t+1}` is independent of `(Z, X^t)`, so the one-step innovation variance is at least 1 and PD-B holds with `N_inn ≥ 1`. Inflow of a look is `I(X_t; Y_t | past) = (1/2) log(t² v + 2)`. Late looks approach `(1/2) log 8 = (3/2) ln 2` nats, the total through `T = 2^K` is `O(log T)`, and the mean inflow tends to 0.

This iteration was done in exact rationals, not by calling `sparse_look_counterexample`. Through `T = 2^16` (17 looks):

| Quantity | Note | This derivation |
|---|---|---|
| max pre-look mean squared error | ≤ 7.00 | `10021590359/1431655767 = 6.999999993` |
| total inflow | 16.8 nats | 16.779373370 nats |
| mean inflow | `2.56×10^{−4}` nat/step | `2.560329189×10^{−4}` |
| blind mean squared error | `4.29×10^9` | `T² + 1 = 4294967297` |
| `E[(X_T − T μ_T)²]` | 1 | 1 exactly |
| `I(μ_T; X_T)` | 11.090 nats | 11.090354889141 nats |
| `I(Y; X_T)`, full look record | 11.157 nats | 11.157120585450 nats |

**Action error.** Conditional on the earlier looks, `Z ~ N(μ_pre, v)`, independent of `G, N ~ N(0,1)`. Gain `K = v T / (T² v + 2)`, `μ = μ_pre + K (Y − T μ_pre)`. Then

`X − T μ = [2T / D] (Z − μ_pre) + [2 / D] G − [T² v / D] N`, `D = T² v + 2`,

and the second moment is `(T² v + 2)² / D² = 1` for every `v`. The same identity is `T² v_post + 1 + 2 T Cov(Z − μ, G)` with `Cov(Z − μ, G) = −T v_post / 2`. At this `T` the rational value is `−65536/5726623063`.

**Posterior-mean stock.** `(X, μ)` is jointly Gaussian and zero-mean, `μ = E[Z | looks]`, and `Var(μ) = 1 − v_post`. The cross term `Cov(G_T, μ) = T v_post / 2` does not vanish, so `T μ` is not `E[X | μ]`. The conditional variance is

`Var(X_T | μ_T) = 1 − (T v_post / 2)² / (1 − v_post)`.

Exactly, `v_post = 2/5726623063` and the subtracted term is `4294967296/32794211694230255843 = 1.30967×10^{−10}`, so `Var(X_T | μ_T) = 0.999999999869`. Therefore

`I(μ_T; X_T) = (1/2) log((T² + 1) / Var(X_T | μ_T)) = 11.090354889141`

which is `(1/2) log(T² + 1) = 11.090354889076` plus `6.55×10^{−11}`. The note's "matching `(1/2) log(T² + 1)` to `10^{−10}`" holds, and 11.090 is the three-decimal value. A Sherman–Morrison evaluation of the 17-look covariance, in exact rationals, returns the same `Var(X_T | μ_T)`. Float64 `numpy.linalg.solve` on `Σ_Y = ttᵀ + 2I` differs from that rational by `1.31×10^{−10}`.

**Full look record.** Given the earlier looks, `Var(X_T | Y) = (T² v_pre + 1) / (T² v_pre + 2)`. Here `u_pre = 8589934592/1431655767 = 5.999999993`, so the conditional variance is `10021590359/11453246126 = 0.874999999891`, against the fixed point `7/8`. Then `I(Y; X_T) = 11.157120585450` nats, which prints as 11.157. The same rational is the Schur complement of the 17 observations. The fixed-point stand-in `(1/2) log((T² + 1) / (7/8)) = 11.157120585388` differs by `6.2×10^{−11}`.

**Monte Carlo.** 20000 independent draws, seed 20261121, the scalar filter at `K = 16`: mean of `(X_T − T μ_T)²` is `1.0027 ± 0.0101`. The sample mutual information of `(μ_T, X_T)` is 11.092. That estimate sits on `1 − ρ² ~ 10^{−10}`, so the closed form is the value; the draw rules out the old denominator 2.5 (mean squared error 2.5, stock 10.63).

**Mean inflow.** The same recursion at `T = 2^K`:

| `K` | mean inflow (nat/step) | max pre-look MSE |
|---|---|---|
| 4 | `2.69×10^{−1}` | 6.885 |
| 8 | `3.31×10^{−2}` | 6.9995 |
| 12 | `3.08×10^{−3}` | 7.0000 from below |
| 16 | `2.56×10^{−4}` | 6.999999993 |
| 20 | `2.00×10^{−5}` | below 7 |

The mean goes to 0. At `r̄ = 0`, PD1(a) asks only `D ≥ N_inn`. This design's error stays below 7. PD1(b) does not apply: the world is not `X ↦ A X + W` with i.i.d. `W`.

The note names the memory. `theory/THEOREM_P_DRIFT.md:114` says the state that drives the policy is the posterior mean `M_T = μ_T = E[Z | looks so far]`, states `E[(X_T − T μ_T)²] = 1` and the conditional-variance formula, and gives `I(μ_T; X_T) = 11.090` nats. The same paragraph gives the full record `I(Y; X_T) = 11.157`. The table at `:137` repeats both, labeled posterior mean and full look record.

## Blocker — resolved

`CONFIRM.md` item 1. The old stock was `(1/2) log(Var(X_T) / (T² v_post + 1))` with denominator 2.5. That denominator is `Var(T(Z − μ) + G)` only if `G_T` is independent of `μ`. It is not. `1861432` replaces it.

`tools/theorem_p_drift_checks.py:74–119` defines memory as `μ_t = E[Z | looks]`, sets `Var(X_T | μ_T) = 1 − (T v_post / 2)² / (1 − v_post)`, and sets the record variance to `(T² v_pre + 1) / (T² v_pre + 2)`. The run at `:315–327` requires `stock_I` within `10^{−9}` of both the 17-look Gaussian mutual information and `(1/2) log(T² + 1)`, and within `10^{−6}` of 11.090354889, and `stock_I_record` within `10^{−9}` of the Schur complement and within `10^{−6}` of 11.157120585. Quick mode prints `I(mu_T;X_T)=11.090 nats (I(Y;X_T)=11.157 nats)`.

`tools/test_theorem_p_drift_checks.py:49–75` locks the same two numbers and rebuilds both conditional variances from `Σ_Y = ttᵀ + 2I` with `Cov(X_T, Y_T) = T² + 1`. `theory/theorem_p_drift_checks/results_full.json` stores `stock_I = 11.090354889141024` and `stock_I_record = 11.157120585450167`, the rationals above.

## PD6 wording

The scoped conclusion is: in a Gaussian world whose variance diverges, the raw stock `I(M_t; X_t)` diverges for every uniformly accurate design and cannot be the viability term; Theorem S1's stationary `I_mem` stays valid on its domain; a renormalized stock is **OPEN**. Those three clauses are in:

- `theory/THEOREM_P_DRIFT.md:24` and `:108` (the master equation unchanged, `κ` already per nat per unit time, the common `(κ/2) log Var`, `−(κ/2) log D` still ranking designs, a rate already booked by `theory/INTERNAL_MODEL.md` §4 and CT7, PD5's `σ√(2wc)` matching CT7 with `c` in place of `kT`, an OU filter keeping `I` finite, CE7 showing the information term is not forced to be a flow);
- `measurement/CLAIM_MAP_v2.md:637` (PD6) and `:639` (PD8 leaves the renormalized stock **OPEN**);
- `measurement/CLAIM_MAP_v2.md:86` (the v2.74 note) and `:511` (CX1);
- `OPEN_WORK.md:58` (T11), including the general floor `D ≥ n N_inn e^{−2r̄/n}` and CX1 staying **OPEN**.

CX1 and the v2.74 note compress the booking sentence to "booking a rate or a renormalized stock stays OPEN in PD8". PD6's own row, the note at `:108`, and T11 keep the rate as the booking INTERNAL_MODEL §4 and CT7 already do, and leave **OPEN** on the renormalized stock. PD8's open list starts with that stock. The three clauses the prior should-fix required are in all four places. CX1 stays **OPEN**.

`CORE.md:85` is the assumption cell, not a fifth copy of that paragraph. It says S1 as proved does not apply, and that the flow form of the floor is in `theory/THEOREM_P_DRIFT.md` (CLAIM_MAP section T; reviewed, fixes pending confirm). The prior nit was the phrase "a self-check, not reviewed". That phrase is gone. The cell does not say the stock form fails and does not say `κ` must price a flow.

A search for `must price a flow`, `price a flow`, and `stock form fails` hits only `reviews/theorem_p_drift_2026-11-21/REVIEW.md:66` and `:89`, and `reviews/theorem_p_drift_2026-11-21/CONFIRM.md` quoting that defect. None of those strings is in a maintained file, the note, CLAIM_MAP, OPEN_WORK, or CORE.

## Merge with `8e829e5`

`f9f7482` merges `1861432` with `8e829e5`. Section S and the v2.72 note are byte-identical to `8e829e5`. The N64 row and the v2.73 note are byte-identical to `8e829e5`. Section N is N1..N64, 64 rows, 0 status mismatches.

The live tally on `8e829e5` is OPEN 87, PROVED (in-model) 97, PRIOR ART 34, total 335. This head adds PD1a and PD2–PD6 (PROVED, +6), PD1b and PD7 (PRIOR ART, +2), and PD8 (OPEN, +1): OPEN 88, PROVED 103, PRIOR ART 36, total 344. The counts table at `measurement/CLAIM_MAP_v2.md:645–662` is that list, and the v2.74 note states `335→344`. `check_consistency.py` reports 344 rows and tally total 344.

Version pointers that the consistency check reads all say CLAIM_MAP v2.74 and THEORY v2.9: `THEORY.md:3`, `README.md:33`, `STATUS.md:3`, `STATUS.md:13`. `theory/README.md:13` points section T at v2.74. `STATUS.md:3` names `main` as `8e829e5`, says v2.72 is section S merged with PR #146, v2.73 is N64 merged with PR #145, and v2.74 is this branch's section T, not yet merged. `check_fresh.py` accepts `8e829e5` inside the `origin/main` window `8e829e5 fda5557 dc7d731 c92886a 2eeab30`.

## Sentence, cost, locks

The Part 2 sentence is one line in each of `THEORY.md:41`, `CORE.md:9`, `README.md:9`, and `theory/SELECTION_AXIOMS.md:13`. The line bytes, including the bold markers, are 107 bytes and equal `8e829e5` and `c92886a`:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

The word is `cost`. `git diff 8e829e5 HEAD` contains no `bill`. `theory/THEOREM_P_DRIFT.md` does not contain `bill`.

`git diff --name-only ab31c17 1861432` does not touch `reviews/`, a preregistration, a `.sha256`, a LOCK file, or `tests/`. `git diff --name-only 8e829e5 HEAD` has no path matching `PREREG`, `LOCK`, `.sha256`, or `predictions.json`. The only `reviews/` paths in that diff are this PR's `REVIEW.md` and `CONFIRM.md`. This confirm adds `CONFIRM2.md` and does not edit those two.

## Commands

All from the repo root, with `nice -n 19`, on `f9f7482`, after `git fetch origin main` (`origin/main` is `8e829e5`). NumPy, SciPy, SymPy, and pytest were installed in the environment so the suite could import. That install moved NumPy from 1.26.4 to 2.5.5. SciPy 1.18.1, SymPy 1.14.0, pytest 9.2.0. No project file was changed for that. The drift checker was quick mode, not `--full`.

| Command | Result |
|---|---|
| `python3 tools/check_fresh.py` | PASS. STATUS main is `8e829e5`, inside the origin/main window `8e829e5 fda5557 dc7d731 c92886a 2eeab30`. |
| `python3 tools/check_consistency.py` | PASS. THEORY v2.9; CLAIM_MAP latest note v2.74; version pins OK; wording FAILs 0 on 29 maintained docs; section N 64 rows (N1..N64), 0 mismatches; tally 344 = 344; core index 74 = 74; process-rule FAILs 0; core-rule FAILs 0. Length warnings are the pre-existing advisory ones (THEORY main text 10569 words, README 1468). |
| `python3 tools/check_open_work.py` | PASS. items.json not-DONE 62; QUEUE.md not-DONE 90; missing from OPEN_WORK.md: 0. |
| `python3 tools/theorem_p_drift_checks.py` | PASS. `ALL PD CHECKS PASS`. The CE7 line prints `I(mu_T;X_T)=11.090` nats and `I(Y;X_T)=11.157` nats. Kalman relative gap `2.23×10^{−15}`. Quick-mode quantizer ratios 1.63, 2.00, 2.54 and 1.69, 2.01, 2.41. |
| `python3 -m pytest -q tools` | `191 passed, 1 skipped` in 275.40 s. The skip is `tools/test_lean.py:101`, Lean 4 / lake is not installed. |

## Conclusion

READY. The stock is the posterior-mean mutual information, 11.090354889 nats, the full look record is 11.157120585 nats, the action error is 1, the mean squared error stays below 7, and the mean inflow tends to 0. PD6's scoped reading is the one in the note, PD6, CX1, and T11. The merge leaves S and N64 intact and the tally at 344. The hypothesis sentence matches `8e829e5`. This confirm does not merge.
