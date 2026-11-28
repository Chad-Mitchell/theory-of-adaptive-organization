# Blind confirm: PR #149 (Theorem P for drifting worlds)

**Confirmer:** independent. Wrote none of the note, the checker, the tests, or `REVIEW.md`.
**Date:** Saturday 21 November 2026 (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/149
**Head confirmed:** `9489486d9dd17894556ee1f9fccbd87aea799b6d` on `theorem-p-drift-2026-11-21`. Review commit `286f2c2` (of `12cf955`); fix commit `9489486`. Branch base `c92886a`. Current `origin/main` is `dc7d731`. Draft. Not merged.

**Verdict: NOT READY**

One blocker. The review's PD3 scope repair is in the text, CE7's mean-squared-error bound and mean inflow recompute, CX1 stays **OPEN**, and the scoped reading of κ is in the note, CLAIM_MAP PD6, and OPEN_WORK. The printed stock `I(M_T; X_T) = 10.63` nats is not the mutual information of the construction. The checker and the test lock that same wrong value in, so a passing run does not witness the identity.

## CE7, recomputed

World: `Z ~ N(0,1)`, `G_t` i.i.d. `N(0,1)`, `X_t = t Z + G_t`. Looks `Y_t = X_t + N(0,1)` at `t = 2^k` only. Between looks, `A_s = s E[Z | looks so far]`. Fresh `G_s` is independent of that posterior, so the mean squared error on an interval is `s² v + 1`, largest at the right endpoint. Prior variance of `Z` starts at 1. A look at scale `t` has observation noise variance 2 (`G` and `N`), so the posterior variance updates by `v ← 2v / (t² v + 2)`, and the inflow of that look is `I(X_t; Y_t | past) = (1/2) log(t² v + 2)`. With `u = t² v` and `t` doubling, `u ← 8u / (u + 2)` from `u_0 = 1`, and `u` rises to 6 from below, so the pre-update mean squared error rises to 7 from below.

Through `T = 2^16` (17 looks), from an independent iteration, not from `sparse_look_counterexample`:

| Quantity | Note | Recomputation |
|---|---|---|
| max mean squared error | ≤ 7.00 | 6.999999993 |
| total inflow | 16.8 nats | 16.77937337 nats |
| mean inflow | `2.56×10^{−4}` nat/step | `2.56032919×10^{−4}` |
| blind mean squared error | `4.29×10^9` | `T² + 1 = 4294967297` |
| `I(M_T; X_T)` | 10.63 nats | 11.090354889 nats if `M` is the posterior mean of `Z`; 11.157120585 nats if `M` is the look record |

The innovation variance is at least 1 because `G_t` is independent of `(Z, X^{t−1})`, so PD-B holds with `N_inn ≥ 1`. Along `T = 2^K` each late look contributes `(1/2) log 8 = (3/2) ln 2` nats, the total inflow is `O(log T)`, and the mean inflow tends to 0, so `r̄ = 0` for the infinite policy. PD1(a) at `r̄ = 0` asks only `D ≥ N_inn`, and this design's error stays below 7. PD1(b) does not apply: the world is not `X ↦ A X + W` with i.i.d. `W`.

## Blocker

1. **`theory/THEOREM_P_DRIFT.md:114` and `:137`; `tools/theorem_p_drift_checks.py:79–101` and `:292`; `tools/test_theorem_p_drift_checks.py:58`.** `I(M_T; X_T) = 10.63` is the number produced by `(1/2) log(Var(X_T) / (T² v_post + 1))` with `T² v_post + 1 = 2.5`. That denominator is `Var(T(Z − μ) + G)` only if `G_T` is independent of the posterior. It is not. The last look is `Y_T = X_T + N_T`, and that `Y_T` is inside `μ`.

   Conditional on the earlier looks, `Z ~ N(μ_pre, v)` independent of `G, N ~ N(0,1)`, `X = T Z + G`, `Y = X + N`, gain `K = v T / (T² v + 2)`, `μ = μ_pre + K (Y − T μ_pre)`. Expanding `X − T μ` gives variance 1 for every `v`. The cross term is `Cov(Z − μ, G) = −T v / 2`, and `T² v + 1 + 2 T Cov(Z − μ, G) = 1`. At this `T`, `T² v_post + 1 = 2.5`, so the code's denominator is 2.5 times the error variance of `A_T = T μ`.

   `(X, μ)` is jointly Gaussian and `E[(X − T μ)²] = 1 = Var(X | μ)`, so `T μ` is the conditional expectation and

   `I(μ; X_T) = (1/2) log(T² + 1) = 11.090354889` nats

   (16 bits, plus `(1/2) ln(1 + T^{−2})`). A Monte Carlo of 8000 draws at `K = 16` gave post-update mean squared error `0.982 ± 0.015`, against the code's `2.500`.

   If `M_T` keeps every look, the Schur complement on the 17 observations gives `Var(X_T | Y) = 0.875` (the fixed point `(6 + 1) / (6 + 2)`) and `I(Y; X_T) = 11.157120585` nats.

   The code comment at `tools/theorem_p_drift_checks.py:79–80` states the false identity, and `:101` implements it. The test requires `abs(stock_I − 10.63) < 0.005`. `theorem_p_drift_checks.py` therefore prints `I(M_T;X_T)=10.63` and passes. The stock does diverge (it grows as `(1/2) log(T² + 1)`), and the rate and error claims of CE7 stand. The equality does not.

## Review items

`REVIEW.md` reviewed `12cf955`, verdict READY-WITH-FIXES. This confirm is of `9489486`.

1. **PD3 scope. Fixed in the prose.** `theory/THEOREM_P_DRIFT.md:90` keeps the blind-loss sentence (`Var(uᵀ X_t) → ∞` makes a blind design's loss unbounded; random walks and fBm are named only there). The rate sentence is restricted to PD-C: bounded mean squared error forces `r̄ > log|det A|` by PD1(b), and for a random walk that threshold is 0. CE7 is the next counterexample, after CE2. CLAIM_MAP PD3 (`measurement/CLAIM_MAP_v2.md:618`) still confines the rate claim to the linear tier. The plain-words rate sentence at `theory/THEOREM_P_DRIFT.md:7–12` sits inside the linear display `X_{t+1} = A X_t + W_t`.

2. **κ reading. Applied in the three named places.** The phrase `must price a flow` is gone from the note, from CLAIM_MAP PD6, and from OPEN_WORK. What those three now say matches the scoped reading:
   - `theory/THEOREM_P_DRIFT.md:24` and `:108`. The master equation is unchanged. `κ` is a price per nat per unit time. Theorem S1's `I_mem = I(M_t; X^t)` stays on the stationary domain (an OU filter keeps `I` finite). In a Gaussian world with diverging variance the raw stock cannot be the viability term; `(κ/2) log Var` is common and `−(κ/2) log D` still ranks designs at a fixed time. Booking a rate is what `theory/INTERNAL_MODEL.md` §4 (the per-step `κ · ½ log₂(1 + q_i/P_i)` at line 176) and CT7 already do, and PD5's `σ√(2wc)` matches CT7 with `c` in place of `kT`. A renormalized stock is **OPEN**. CE7 is cited for why the information term is not forced to be a flow.
   - `measurement/CLAIM_MAP_v2.md:621` (PD6) carries the same clauses, and PD8 (`:623`) leaves the renormalized stock **OPEN**.
   - `OPEN_WORK.md:58` (T11) carries the same clauses, states the general floor as `D ≥ n N_inn e^{−2r̄/n}`, and says CX1 stays **OPEN**.

   A repo-wide search for `must price a flow`, `price a flow`, and `κ must` hits only `reviews/theorem_p_drift_2026-11-21/REVIEW.md:66` and `:89`, the review's own statement of the defect.

3. **Nits. Fixed.**
   - Nit 1: `theory/THEOREM_P_DRIFT.md:7–12`, as above.
   - Nit 2: `:100–106` says the per-step objective is `w D + c r` with `r = ρ dt`, so the cost per unit time is `w D + c ρ`, and names `price_optimum_rw(σ² dt, w, c/dt)`. The call is `tools/theorem_p_drift_checks.py:221`.
   - Nit 3: `:108` says the divergent piece is common and `−(κ/2) log D` still ranks designs. What fails is comparing the unregularized cost with a finite income.
   - Nit 4: `OPEN_WORK.md:58` uses `D ≥ n N_inn e^{−2r̄/n}`.

4. **CX1. Still OPEN.** Status cell `measurement/CLAIM_MAP_v2.md:506` is **OPEN**. No existing row changes status. PD1a and PD2–PD6 are **PROVED (in-model)**, PD1b and PD7 **PRIOR ART**, PD8 **OPEN**. Tally 339, matching `check_consistency.py`.

## Should-fixes

1. **`measurement/CLAIM_MAP_v2.md:86` and `:506`.** Two summaries still say the stock form fails. The v2.73 note says the stationary stock `I(M; X)` diverges for every competent design and that "the stock form fails." The CX1 Why cell says "the stationary stock form fails (PD6)." PD6's own row has the scoped reading: the master equation is unchanged, the stationary `I_mem` stays valid on its domain, the raw stock cannot be the viability term when variance diverges, a rate is what INTERNAL_MODEL §4 and CT7 already book, and a renormalized stock is **OPEN**. These two sentences drop that scope. The same v2.73 sentence still says a status change is left to the independent review; the review of `12cf955` already left CX1 **OPEN**, and the fix says so in T11 and in the note.

## Nits

1. **`CORE.md:85`.** The new pointer still says the drift note is "a self-check, not reviewed." The independent review of `12cf955` is `REVIEW.md`, and this file is the confirm of the repair.

## Merge, sentence, locks

`git merge-tree --write-tree origin/main HEAD` exits 0 and writes tree `8001e74b5f541a4c99eea5d759a5dbf940f43fc5`. No conflict markers. The only path edited on both sides since `c92886a` is `OPEN_WORK.md` (T11 on this branch, T19 on `dc7d731` from PR #147). Git auto-merged it; the merged T11 cell still has the scoped reading. The worktree was not merged.

The Part 2 sentence is one line in each of `THEORY.md:41`, `CORE.md:9`, `README.md:9`, and `theory/SELECTION_AXIOMS.md:13`, and the line bytes, including the bold markers, equal `origin/main` (`dc7d731`) and `c92886a`:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

In the new note, "law" occurs as "shock law" (`theory/THEOREM_P_DRIFT.md:7`) and "stationary law" (`:92`). `check_consistency.py` reported 0 wording FAILs on 29 maintained docs.

`git diff --name-only c92886a HEAD` is 14 paths: `CORE.md`, `OPEN_WORK.md`, `README.md`, `STATUS.md`, `THEORY.md`, `measurement/CLAIM_MAP_v2.md`, `reviews/theorem_p_drift_2026-11-21/REVIEW.md`, `theory/README.md`, `theory/SELECTION_AXIOMS.md`, `theory/THEOREM_P_DRIFT.md`, `theory/theorem_p_drift_checks/results_full.json`, `tools/test_brief.py`, `tools/test_theorem_p_drift_checks.py`, `tools/theorem_p_drift_checks.py`. None is a preregistration, a `.sha256`, a LOCK file, or a path under `tests/`. The same filter against `origin/main` on this branch's side is empty.

## Commands

All from the repo root, with `nice -n 19`, on `9489486`. `numpy`, `scipy`, `sympy`, and `pytest` were installed in the environment so the suite could import. No project file was changed for that.

| Command | Result |
|---|---|
| `python3 tools/check_fresh.py` | PASS. STATUS main is `2eeab30`, inside the origin/main window `dc7d731 c92886a 2eeab30 c04cedd d34df95`. |
| `python3 tools/check_open_work.py` | PASS. items.json not-DONE 62; QUEUE.md not-DONE 90; missing from OPEN_WORK.md: 0. |
| `python3 tools/check_consistency.py` | PASS. THEORY v2.9; CLAIM_MAP latest note v2.73; wording FAILs 0; section N 63 rows, 0 mismatches; tally 339 = 339; core index 74 = 74; process-rule FAILs 0; core-rule FAILs 0. Length warnings are the pre-existing advisory ones (THEORY main text 10569 words, README 1468). |
| `python3 tools/theorem_p_drift_checks.py` | PASS. `ALL PD CHECKS PASS`. The CE7 line prints `I(M_T;X_T)=10.63`, which is the blocker's formula. Kalman relative gap `2.23×10^{−15}`. Quick-mode quantizer ratios 1.63, 2.00, 2.54 and 1.69, 2.01, 2.41. |
| `python3 -m pytest -q tools` | `180 passed, 1 skipped` in 257.77 s. The extra pass against the review's 179 is `test_ce7_sparse_look_counterexample`, which asserts the wrong stock. |
