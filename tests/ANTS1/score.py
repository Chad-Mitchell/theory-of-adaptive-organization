"""ANTS1 scorer. Written BEFORE any ant code (rule d).

Inputs: true positions x[t] and a readout r[t] (the colony's or an ant's estimate of the food position,
taken BEFORE that step's deposits, i.e. what an ant leaving the nest would use). NaN readouts (empty trail)
are scored as a uniformly random guess (expected squared circular error M^2/12, capture prob 2R+1 over M).

Metrics over steps t >= BURN (on the step subset where the readout exists):
  MSE      : mean squared circular distance (primary; T4 assumes quadratic loss)
  CAPTURE  : fraction of steps with circular distance <= R_CAPTURE (secondary, descriptive)
"""
import numpy as np
from world import M, BURN

R_CAPTURE = 8.0


def circ_dist(a, b):
    d = np.abs(a - b) % M
    return np.minimum(d, M - d)


def score(x, r, steps=None):
    """x: full truth array; r: readout array aligned with `steps` (default every step)."""
    if steps is None:
        steps = np.arange(len(x))
    keep = steps >= BURN
    xs, rs = x[steps[keep]], r[keep]
    nan = np.isnan(rs)
    d = circ_dist(xs, np.where(nan, 0.0, rs))
    se = np.where(nan, M * M / 12.0, d * d)
    cap = np.where(nan, (2 * R_CAPTURE + 1) / M, (d <= R_CAPTURE).astype(float))
    return float(se.mean()), float(cap.mean())
