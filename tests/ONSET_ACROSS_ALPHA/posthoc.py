"""POST HOC (after lock and verdict; never decides a verdict): (1) level gap ln N*(2.5) - ln N*(1.5) per rho vs theory
(the constants are predicted to depend on alpha even though the exponent does not); (2) drop-one-rho exponents."""
import json, numpy as np
from analyze import load, crossing
from theory import nstar
cells = load('results.jsonl'); R = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
pt = {(a, r): crossing(cells[(a, r)][0][0], np.mean([x[1] for x in cells[(a, r)]], 0)) for a in (1.5, 2.5) for r in R}
gap = [pt[(2.5, r)] - pt[(1.5, r)] for r in R]; gpred = [np.log(nstar(2.5, r) / nstar(1.5, r)) for r in R]
ratio = {a: [float(np.exp(pt[(a, r)]) / nstar(a, r)) for r in R] for a in (1.5, 2.5)}
drop = {}
for k in range(len(R)):
    rr = [r for j, r in enumerate(R) if j != k]
    e = {a: np.polyfit(np.log(rr), [pt[(a, r)] for r in rr], 1)[0] for a in (1.5, 2.5)}
    drop[R[k]] = dict(e15=round(e[1.5], 3), e25=round(e[2.5], 3), delta=round(e[2.5] - e[1.5], 3))
print(json.dumps(dict(gap_meas=[round(g, 3) for g in gap], gap_pred=[round(g, 3) for g in gpred],
                      mean_gap_meas=round(float(np.mean(gap)), 3), mean_gap_pred=round(float(np.mean(gpred)), 3),
                      Nstar_over_theory={str(a): [round(x, 3) for x in v] for a, v in ratio.items()}, drop_one=drop), indent=1))
