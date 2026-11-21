# S5 results: 120-world Model S convexity rerun with the merged solver

*Friday 20 November 2026, about 5:31 PM ET (America/New_York). Beside `main` at `a1a98aa`. Script: `core/keystone_checks/s5_rerun.py`. Data: `s5_rerun.json`. Short log: `s5_rerun.out`. Analytic probe (not the headline search): `s5_analytic_probe.py`.*

This is the owed rerun of the 120-world search behind N60's convexity premise (OPEN_WORK S5; review should-fix S5). It does **not** prove convexity.

## Protocol

- **Worlds.** Bit-identical to `convexity_targeted.py`: seeds 0..119, `rng = default_rng(1000+seed)`, J ∈ {3, 4} (50 three-mode, 70 four-mode), scale separations ×3 to ×100, log-uniform variances and read noise. Parameters of every world match the earlier JSON, including seed 24.
- **Solver.** The merged #116 code in `theory/layers_checks/stores.py` (Jacobi-scaled pseudo-inverse; MSE re-evaluated at the returned rates), imported under a unique name so the pre-#116 copy of `stores.py` in this folder cannot win. Multi-start adapted from the reviewer routine in `rhythm_rule.py`: informed grids at the mode rates, 2% store-rate separation, Nelder–Mead, L-BFGS-B polish, and differential evolution. No `minimum.accumulate`. E_0 = Σ v_j (act blind). ε_K = E_K / E_∞ − 1 with E_∞ the Yovits–Jackson integral from the merged solver, not `min(E_J, YJ)`.
- **Tests.** Convexity of ε_K on K = 1..J (the N60 premise) and on K = 0..J, at the original absolute decrement tolerance 10⁻⁴, and also at 10⁻⁶. N60 increment K* = 1 + #{k ≥ 2: R(ε_{k−1} − ε_k) > 1} against leftmost argmin_K [K + R(1+ε_K)] on K = 0..J, over R ∈ logspace(−1, 7, 161). The K* = 0 hole (the formula starts at 1) is counted separately.
- **Compute.** `nice -n 19`, 6 workers, 126.7 s wall, 753 s of worker time (well under the ~60-minute cap). All 430 K-fits were won by Nelder–Mead; L-BFGS-B and DE did not improve the value.

## Results

| Check | Result |
|---|---|
| Worlds completed | 120 / 120, all finite |
| Convex ε_K on K = 1..J, tolerance 10⁻⁴ | **120 / 120** |
| Same, tolerance 10⁻⁶ | **120 / 120** |
| Convex ε_K on K = 0..J, tolerance 10⁻⁴ | **120 / 120** |
| E_K below the causal floor | **0** |
| Increasing E_K (optimizer flag) | **0** |
| N60 = argmin J, excluding the K* = 0 hole | **18,941 / 18,941** |
| K* = 0 hole (argmin is 0; N60 returns ≥ 1) | **379 / 19,320** comparisons, in 39 of 120 worlds, all at R ∈ [0.10, 1.41] |
| Genuine formula mismatches (argmin ≥ 1, not a knife-edge tie) | **0** |
| Counterexample | **None found** |

For every 3-mode world with ε_1 > 10⁻³ (41 such worlds), ε_2/ε_1 ranged from 6.6×10⁻⁶ to **0.3147** (convexity needs ≤ 0.5). The closest was seed 100 (τ ≈ 1.01, 6.92, 271; v ≈ 0.136, 1.44, 0.242; N ≈ 0.0626). That is the same closest random world as in the earlier search, to the reported digits. The closest *numerical* approach to a decrement increase on K = 1..J was −9.8×10⁻⁸ on the already-flat tail of seed 62, not a near-violation in the interesting part of the curve.

E_J − E_∞ was positive in every world (never below the causal floor): median 8.5×10⁻⁸, maximum 2.4×10⁻⁶. So ε_J is a residual of at most 8.9×10⁻⁷, not a forced zero.

The K* = 0 hole is exactly the known index gap: the formula as written starts at K = 1 and cannot return the blind act that CT21 allows when R is small. The largest threshold 1/(ε_0 − ε_1) on this draw was about 1.55 (seed 0). On every comparison with argmin ≥ 1, N60 matched. That is what the count formula is proved to do once convexity is granted; it is a consistency check, not further evidence for convexity.

## What the earlier 120-world search had hidden

The pre-#116 `stores.py` (raw `solve`/`lstsq`) overflowed on **seed 24** and recorded ε = [−1, NaN, NaN, NaN]. That world was counted as “no violation” only because a NaN fails the test `dec[k+1] − dec[k] > 10⁻⁴`. The earlier “0 non-convex beyond 10⁻⁴” figure therefore included one broken world. Under the merged solver the same parameters are clean and convex:

- τ ≈ 4.205, 32.45, 368.7, 24791; v ≈ 0.0423, 14.43, 8.651, 3.503; N ≈ 0.04941
- (E_0, …, E_4) ≈ (26.625, 0.216119, 0.216002, 0.215994, 0.215994); E_∞ ≈ 0.21599387
- ε_{1..4} ≈ (5.81×10⁻⁴, 3.76×10⁻⁵, 1.23×10⁻⁶, 6.08×10⁻⁸)

Of the other 119 worlds, 116 agree with the old ε sequence to 10⁻⁸ absolute / 10⁻⁶ relative, and three differ only at 10⁻⁷ to 10⁻⁸ on an already-flat tail. The headline 0.315 ratio is unchanged.

The 24 real-pole worlds in `convexity_wide.py` were **not** part of this owed rerun and still rest on the older solver.

## Analytic attempt (time-boxed): no proof; where it fails

N60's count formula is elementary once ε_K is convex and decreasing. The open claim is that this premise holds in Model S (sums of OU modes, first-order real stores). In Model S, E_J = E_∞ exactly (the causal Wiener filter has J real poles and is realizable by J first-order real stores). Decreasing is likewise exact in the design class (K+1 stores can mimic K by setting a gain to zero). Convexity is not.

A proof would have to show that the MSE of the best degree-K real-rational causal filter is a convex sequence in K on a positive combination of Lorentzians. Standard tools do not close:

1. **Residual induction fails.** After a first-order store is placed, the residual process is not a sum of OU modes, so the problem class is not preserved and one cannot induct on J.
2. **Subset / eigenvalue diminishing returns do not apply.** If the stores were a best K-subset of a *fixed* dictionary, the residual of an orthogonal (or Ky-Fan) expansion would be a tail of eigenvalues and hence convex in K. Store rates are free parameters; ℋ_K is a nonlinear manifold, not a Grassmannian of a fixed feature map. Das & Kempe (STOC 2008; doi 10.1145/1374376.1374384), already noted in the keystone note, is subset selection in linear regression — a different problem.
3. **Hankel / balanced-truncation tails are the wrong object.** Discarded Hankel singular values give a convex *bound* on a *specific* model-reduction error, in a different norm, and the reduced poles need not be real. A convex upper bound does not imply convexity of the true Wiener-MSE error, and our design class is restricted to real poles.
4. **J = 1 is vacuous, and J = 2 is vacuous on K = 1, 2.** The first nontrivial N60-premise case is J = 3: with ε_3 = 0, convexity is ε_2 / ε_1 ≤ 1/2. Including K = 0, the first nontrivial inequality is already at J = 2: 2 E_1 ≤ Var + E_∞, i.e. one store captures at least half the reducible error. A 1-D search on 500 random two-mode worlds (`s5_analytic_probe.py`) found 0 violations (minimum (E_0−E_1)/(E_1−E_∞) = 1.49). That is further numerical support, not a proof; a closed comparison-filter argument was not obtained.

In the well-separated, equal-variance limit the claim is plausible: the Kalman filter approximately decouples, stores are assigned to modes in order of value, and increments are then nonincreasing. That is a special case, and it is not the tight case. The tightest random and adversarial approaches to the bound (ε_2/ε_1 ≈ 0.315 here; 0.4625 / 0.461 in the earlier climb, still below 0.5) are close or extreme-scale worlds, not well-separated equal-variance ones.

The same geometry explains why a proof that worked for Model S would not be expected to cover rhythms: a lightly damped oscillation is not well approximated by one real pole, so a later real store can buy more than an earlier one. That is already a theorem in the wrong direction in 𝓜_LG (worked example: decrements 0.179, **0.578**, 0.226).

## Status

Convexity of ε_K in Model S remains **numerical only, unproved**. After the merged-solver rerun: 120 / 120 random worlds in this draw are convex at 10⁻⁴ and at 10⁻⁶, on both K = 1..J and K = 0..J; N60 matches argmin J in every comparison with argmin ≥ 1; the only disagreements are the known K* = 0 hole; no E_K fell below E_∞; the one world the old solver had broken is now clean and convex. No counterexample was found. That is stronger numerical support than the earlier search, which used the pre-#116 solver and had hidden a NaN world inside “0 violations.” It is not a proof.
