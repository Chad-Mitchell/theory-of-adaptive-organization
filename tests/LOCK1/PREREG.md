# LOCK1: lock to the world, not to each other (in-model preregistration)

*Saturday 21 November 2026, written about 1:35 PM ET (America/New_York), before any LOCK1 run. In-model and numerical only; says nothing about nature. Requested by Chad (t2065, t2066, t2067). Code to be written after this lock: `tests/LOCK1/lock1.py`. Results: `tests/LOCK1/RESULTS.md`.*

## Claim under test (Chad t2067, as framed by the coordinating agent)

Under J, a layer should **lock to the world's real rhythms** (phase-locking to an actual world period is tracking), and layers should **stay unlocked from each other** (inter-layer locking makes one layer's phase a function of another's, so the second layer carries redundant information at full upkeep). Badly approximable ("irrational") spacing should then appear only between layers where the world supplies no rhythm.

## What was already run before this lock (disclosed, not scored)

- `theory/spacing_checks/antilock.py` Part A (linear stores, scale-free world, alpha 0.8/1.2/1.6): the error as a function of a two-store rate ratio shows no feature at simple rationals (second-difference ratio 1.04–1.10 near p/q versus elsewhere). Part B (sine circle map, q <= 12): the widest unlocked gaps at Kc = 0.5/0.8/0.95 were not at the golden mean. These are exploratory and are not LOCK1 results.
- The cymatics frequency-locking check (`core/KEYSTONE_NOTE.md`, RHYTHM prereg §8): PASS on the aggregate statistic, 3 of 7 light worlds individually above 0.05. Case (a) below re-tests that on rational-ratio worlds only; it is a repeat, not new.

## Models

**Linear (cases a and d1).** `core/keystone_checks/resonant_layers.py`, `optimize_design`, sensing noise N = 0.01, exact Lyapunov MSE. Lightly damped rhythms: pole real part alpha = 0.05·omega.

**Phase layers (cases b and d2).** Two self-sustained layer clocks with natural frequency ratio r (a design choice) and unavoidable cross-talk Kc, reduced to the noisy sine circle map theta' = theta + Omega − (Kc/2π) sin 2πtheta + sqrt(2D)·xi, Omega = r mod 1, D = 1e-4, 4,000 iterations after 500 burn-in, fixed seeds. Redundancy Red(r) = max over q = 1..6 of |mean exp(2πi·q·theta_n)| (≈ 1 when locked p:q, ≈ 0 when quasi-periodic). This is an assumed stand-in for the mutual information between the two layers' phases (ASSUMPTION). Cost J(r) = (ln r − ln r0)²/(2·0.1²) + V·Red(r), V = 1, minimized over r on a grid of step 1e-3 within r0·[0.7, 1.4]. The smooth term stands for whatever sets the preferred spacing r0 without locking (for example the Chow two-exponent spacing, about 3–4); r0 is drawn uniformly from [3, 4], 150 draws, seed 20261121.

## Predictions (locked)

| ID | Case | Prediction | Pass rule |
|---|---|---|---|
| A1 | (a) world = two rhythms at ratio rho in {2, 3, 3/2} (omega1 = 1), 2 resonant layers | each layer locks to a world rhythm | every resonant-layer frequency within 5% of its matched world frequency, in all three worlds |
| A2 | (a) | the inter-layer ratio is the world's rational ratio | |omega_2/omega_1 − rho|/rho < 5% in all three worlds |
| B1 | (b) no rhythm, phase layers | inter-layer ratios avoid low-order rationals | mean distance of the optimal r to the nearest p/q (q <= 4) exceeds that of r0, at each Kc in {0.3, 0.6, 0.9} |
| B2 | (b) | optimal ratios are more badly approximable than r0 | mean of min over q <= 20 of q·||q·r|| for optimal r exceeds that for r0 by >= 10%, at each Kc |
| B3 | (b) | golden/noble ratios are selected | share of optimal frac(r) within ±0.02 of 0.382 or 0.618 is at least 3× the uniform share (0.08), at each Kc. **Expected to FAIL** (written before running) |
| B4 | (b), linear class | NO rational avoidance in the linear class (no locking mechanism exists there) | the exploratory Part A statistic re-run with a fresh scan (alpha 1.0, 1.4) lies in [0.8, 1.25] |
| D1 | (c) mixed: one rhythm at omega = 1 (variance 0.5) plus OU background at rates 0.01 and 0.1 (variance 0.25 each); 1 resonant + 1 first-order layer | the resonant layer locks to the world rhythm | resonant-layer frequency within 5% of 1 |
| D2 | (c) | the free layer's relation to the locked layer follows (b) | in the phase model D2 is B1 with layer 1 pinned to the world; scored as B1 at Kc = 0.6 (no separate statistic) |

No rescue: a failed row stays failed. A row that cannot be computed is INVALID, not a pass.
