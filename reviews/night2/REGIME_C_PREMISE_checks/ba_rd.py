#!/usr/bin/env python3
"""REGIME-C-GAUSSIAN-PREMISE check 1 (pick 18). Blahut-Arimoto (cold start per slope) for the MSE
rate-distortion function of unit-variance, zero-mean scalar sources on a grid. For each slope u (nats per unit
distortion, the multiplier in exp(-u (x-y)^2)) it records D, an achievable rate R_up = I(p, W) and a weak-duality
lower bound R_lo = -u D - sum p ln Z - ln max_y c(y) (valid for any q), plus the exact zero-rate test:
the point output at the mean is optimal at slope u iff max_y exp(-u y^2) E exp(2 u y X) <= 1.
Sources: gauss, uniform, laplace (truncated at |x| <= 20), bern02 (two-point, P = 0.2).
Run: nice -n 19 python3 ba_rd.py SOURCE   -> rd_SOURCE.json"""
import json, sys, numpy as np
def source(name):
    if name == "gauss":   x = np.arange(-7, 7.0001, 0.04); p = np.exp(-x**2/2); y = np.arange(-8, 8.0001, 0.04)
    if name == "uniform": a = 3**0.5; x = np.linspace(-a, a, 301); p = np.ones_like(x); y = np.arange(-3, 3.0001, 0.02)
    if name == "laplace": x = np.arange(-20, 20.0001, 0.1); p = np.exp(-abs(x)*2**0.5); y = np.arange(-25, 25.0001, 0.1)
    if name == "bern02":  x = np.array([0.0, 1.0]); p = np.array([0.8, 0.2]); y = np.arange(-15, 15.0001, 0.01)
    p = p/p.sum(); m = p @ x; x = (x-m)/np.sqrt(p @ (x-m)**2)
    return x, p, y
def zero_rate_test(x, p, u, yy=np.linspace(-60, 60, 24001)):
    from scipy.special import logsumexp
    return float(np.exp(np.max(-u*yy**2 + logsumexp(np.log(p)[None, :] + 2*u*np.outer(yy, x), axis=1))))
def run(x, p, y, u, iters=30000, gap_tol=1e-5):
    A = np.exp(-u*(x[:, None]-y[None, :])**2); q = np.full(len(y), 1/len(y))
    for k in range(iters):
        Z = A @ q; c = (p/Z) @ A
        if k % 200 == 0:
            W = A*q[None, :]/Z[:, None]; D = float((p[:, None]*W*(x[:, None]-y[None, :])**2).sum())
            qo = p @ W; m = W > 1e-300; Rup = float((p[:, None]*W)[m] @ np.log((W/np.maximum(qo, 1e-300)[None, :])[m]))
            Rlo = -u*D - float(p @ np.log(Z)) - float(np.log(c.max()))
            if Rup - Rlo < gap_tol: break
        q = q*c; q /= q.sum()
    return D, Rup, Rlo, k
if __name__ == "__main__":
    name = sys.argv[1]; x, p, y = source(name); out = []
    for u in (np.geomspace(8, 0.05, 30) if name == "laplace" else np.geomspace(30, 0.05, 40)):
        D, Rup, Rlo, k = run(x, p, y, u); z = zero_rate_test(x, p, u)
        out.append({"u": float(u), "d": D, "R_up": max(Rup, 0), "R_lo": Rlo, "iters": k, "zero_rate_cmax": z})
        print(name, f"u={u:.4g} d={D:.5f} Rup={Rup:.4g} Rlo={Rlo:.4g} it={k} cmax0={z:.4g}", flush=True)
    json.dump({"source": name, "rows": out}, open(f"rd_{name}.json", "w"), indent=0)
