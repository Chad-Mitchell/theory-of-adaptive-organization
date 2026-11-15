# ANTS1 preregistration: code ants, the sqrt(N) trail fade (T4) and drift-matched evaporation (H77)

Written Sat 2026-11-14 ~10:45 PM ET, after `world.py` and `score.py` (commit 912c6d3) and `meanfield.py`
(predictions in `meanfield_pred.json`), and BEFORE any ant code exists. Hashed (sha256 in PREREG.sha256) and
git-committed before any run. Any change after this commit is logged in DEVIATIONS.md.

## Model
- Ring of M=1024 sites, one food source; worlds in `world.py`: RW (Gaussian random walk, step sd 0.03/0.2/1.0),
  POIS (uniform relocation at rate 2e-4/1e-3/5e-3 per step), HEAVY (same, Pareto(1.5) holding times, same mean).
- Ant observation each step: x + N(0, s^2), s in {4, 16}; deposit 1 unit at round(obs) mod M.
- Trail: field F over sites, F <- (1-e) F + deposits each step. Evaporation grid: 19 values log-spaced 3e-4..1.0.
- Readouts, taken before each step's deposits: MEAN = circular trail-weighted mean (every step);
  MODE = centre of the heaviest 17-site window (every 10th step). Scored by `score.py`: MSE (primary), capture
  within 8 sites (secondary, descriptive only).
- Arms (N in {1,2,4,...,256}):
  - IND  independent depositors: every ant observes and deposits its own observation.
  - FOL  trail-followers: each ant each step, with prob f=0.75, deposits at a site sampled from the trail (prob proportional
         to F) instead of observing; otherwise deposits its own observation.
  - LOCK positive-feedback lock-in (Deneubourg-type nonlinear choice): follow prob p = S^2/(S^2+k^2), S = total
         trail mass in absolute deposit units, k=100. Followers as in FOL; non-followers observe.
  - PRIV private memory only: each ant keeps its own trail field from its own observations (same e, same readouts);
         scored per ant and averaged. Its expected score does not depend on N (ants are exchangeable and
         independent), so it is simulated with min(N,8) ants. This is by construction.
- 24 seeds per cell; the same world trajectory and RNG seed across evaporation values and arms (paired).
- Total: 4 arms x 3 worlds x 3 drift x 2 noise x 9 N x 19 e x 24 seeds.

## Estimators (fixed now)
- e* for a (cell, arm, readout, N): mean MSE over seeds at each grid e; take the grid argmin; refine with a parabola in
  ln e through it and its two neighbours (if the argmin is at a grid edge, e* = that edge value and it is flagged).
- Exponent: OLS slope of ln e* on ln N over the stated N set. 95% CI: 1000 bootstrap resamples of seeds.
- "Small-gain N set" for a RW cell: N with T4-predicted K*(N) <= 0.3, where K^2/(1-K) = N q/r, q = sd_drift^2,
  r = s^2 + 1/12. "Large-gain set": K*(N) >= 0.5.

## Calibration (NOT evidence; true by construction if the code is right)
- C0. IND, RW, MEAN readout: e* within a factor 1.3 of K*(N) in every (cell, N) with K*(N) in [1e-3, 0.9].
  The trail mean is algebraically an EWMA with gain e, so this checks the code, not T4.
- C1. PRIV e* exponent in [-0.1, 0.1] (by construction).

## Predictions
P1 (T4 exponent, small gain). For IND in each RW cell with >= 3 small-gain N values, the e* exponent over the
   small-gain set lies in [0.3, 0.7], for MEAN and for MODE readout (12 tests: 6 cells x 2 readouts). Supported if
   >= 10/12 point estimates are in the band. The MODE readout is the non-trivial part (nonlinear, ant-like).
P2 (T4 failure at large gain). In the RW cell with >= 2 large-gain N (drift 1.0, obs 4), the IND exponent over the large-gain set
   is < 0.3 for both readouts; and pooled over IND RW cells, the local slope between consecutive N decreases as
   K*(N) increases (Spearman rho < 0 between local slope and K* at the pair midpoint).
P3 (IND error pools). In the small-gain set, IND's best MSE falls with N with slope in [-0.6, -0.4] (MEAN and MODE).
P4 (trail-followers: predicted failure of the raw-N reading). Mean-field (meanfield.py) predicts that FOL keeps
   roughly the SAME e* as IND (ratio within 0.8-1.4, exponent in band) but its best MSE is ~1/(1-f) = 4x IND's at the same N
   (i.e. effective N = (1-f)^2 N = N/16). Predicted: (a) FOL e* / IND e* in [0.7, 1.5] in >= 80% of small-gain
   (cell, N) for MEAN; (b) FOL best MSE >= 2x IND best MSE at the same N in >= 90% of RW (cell, N), MEAN readout.
   Consequence if (a) and (b) hold: the sqrt(N) scaling of e* is NOT diagnostic of independent pooling; only the
   error scaling is.
P5 (lock-in mimic). Mean-field predicts LOCK's e* rises with N with exponent 0.6-0.9 (above or at the top of the band) and its
   best MSE stops improving and then rises with N. Predicted: (a) LOCK e* exponent over the IND small-gain set > 0.55 in >= 4 of 6
   RW cells (MEAN); (b) LOCK best MSE at N=256 > LOCK best MSE at its best N, and > 2x IND's at N=256, in >= 5/6 RW cells
   (MEAN); (c) in POIS/HEAVY at N >= 32, LOCK best MSE > 2x IND best MSE (both readouts) in >= 80% of cells.
P6 (H77 inverted U). For IND, every world, both readouts, N <= 16: MSE vs e has an interior minimum (not at a grid edge)
   in >= 90% of curves.
P7 (H77 peak tracks drift). For IND, every world, both readouts, every N and noise: e* strictly increases from slow to mid
   to fast drift in >= 90% of the series where none of the three e* is at a grid edge.
P8 (jump worlds). For IND in POIS and HEAVY, e* is non-decreasing in N (allowing one step down within the bootstrap 95%
   CI) in >= 80% of (world, drift, noise, readout) series. No exponent band is claimed: T4 is derived for random-walk
   drift only. The e* exponent and the elasticity d ln e* / d ln(lambda) are reported as exploratory.
Exploratory, no prediction: HEAVY vs POIS at matched mean rate; capture metric; FOL/LOCK in MODE readout.

## Kill / scope statements
- If P1 fails for MODE readout but passes for MEAN, T4 holds only for linear (averaging) readouts; report it so.
- If P4(a) holds, the public line "only an arm with independent depositors tests pooling" must be sharpened to
  "only the ERROR scaling tests pooling; e* scaling does not".
- Everything here is a model; results say whether the math holds in a stochastic ant implementation, not whether real
  ants do it. The real-ant check is the literature section of RESULTS.md.
