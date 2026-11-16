"""Q2: exact (grid, deterministic) accuracy-best one-pole linear tracker at A, B, Bnull; its zero-crossing t_A;
curvature of the error rate in ln(pole); flatness band; grid convergence. Own code; nice 19."""
import math, json
import numpy as np
from scipy.optimize import minimize_scalar
from gridengine import analyse, linear_f, bayes_f, kalman_pole
N = 1.0; D = 0.01
pts = {"A": (0.01, 2.0), "B": (0.02, math.sqrt(2.0)), "Bnull": (0.026546, math.sqrt(4 * 0.7534))}
s = math.sqrt(N / D)
def lin(lam, mu, t, hfac=8):
    pole, _ = kalman_pole(lam, mu, N, D); a = 1 - (1 - pole) * t
    sn = s / math.sqrt(1 - a * a); B = mu / (1 - a)
    return analyse(linear_f(a), 1.0, lam, mu, N, D, B + 7 * sn, s / hfac)
out = {}
for k, (lam, mu) in pts.items():
    p = (1 - math.exp(-2 * lam * D)) / 2
    bay = analyse(bayes_f(p), 2 * mu * D / N, lam, mu, N, D, 16.0, 0.02)
    kal = lin(lam, mu, 1.0)
    cache = {}
    def E(u):
        if u not in cache: cache[u] = lin(lam, mu, math.exp(u))
        return cache[u]["err"]
    scan = [(float(math.exp(u)), E(u)) for u in np.linspace(0, math.log(4), 15)]
    i0 = int(np.argmin([e for _, e in scan])); us = np.linspace(0, math.log(4), 15)
    r = minimize_scalar(E, bounds=(us[max(i0-1,0)], us[min(i0+1,14)]), method="bounded", options=dict(xatol=1e-5))
    u0 = r.x; at = lin(lam, mu, math.exp(u0)); at16 = lin(lam, mu, math.exp(u0), 16)
    du = 0.02
    em, e0, ep = E(u0 - du), E(u0), E(u0 + du)
    curv = (ep - 2 * e0 + em) / du**2            # d2 err / d(ln t)^2
    dlt = (math.log(lin(lam, mu, math.exp(u0 + du))["tA"]) - math.log(lin(lam, mu, math.exp(u0 - du))["tA"])) / (2 * du)
    hw1 = math.sqrt(2 * 0.01 * e0 / curv)        # half-width in ln t where err rises by 1% of err_min
    out[k] = dict(lam=lam, mu2=mu * mu, kappa=lam * N / mu**2, bayes=bay, kalman=kal, scan=scan,
                  t_best=math.exp(u0), err_best=at["err"], tA_best=at["tA"], tA_best_h16=at16["tA"], err_best_h16=at16["err"],
                  curv_err_lnt=curv, curv_rel=curv / e0, dlntA_dlnt=dlt, halfwidth_lnt_1pct=hw1,
                  excess_err_vs_bayes=at["err"] / bay["err"] - 1)
    print(k, json.dumps({kk: v for kk, v in out[k].items() if kk not in ("scan",)}, default=float), flush=True)
for b in ("B", "Bnull"):
    out[f"dln_A_{b}"] = dict(lin01=math.log(out[b]["tA_best"] / out["A"]["tA_best"]),
                             lin01_h16=math.log(out[b]["tA_best_h16"] / out["A"]["tA_best_h16"]),
                             bayes=math.log(out[b]["bayes"]["tA"] / out["A"]["bayes"]["tA"]),
                             kalman=math.log(out[b]["kalman"]["tA"] / out["A"]["kalman"]["tA"]))
out["ratio_lin01_over_bayes_AB"] = out["dln_A_B"]["lin01"] / out["dln_A_B"]["bayes"]
print(json.dumps({k: v for k, v in out.items() if k.startswith(("dln", "ratio"))}, indent=1))
json.dump(out, open("q2_lin01.json", "w"), indent=1, default=float)
