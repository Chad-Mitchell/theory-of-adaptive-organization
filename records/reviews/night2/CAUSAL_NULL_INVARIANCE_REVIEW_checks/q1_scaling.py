"""Q1: fixed-kappa time rescaling on the grid (lam x2, mu^2 x2 at N fixed: kappa fixed, lam*D doubles) for Bayes, Kalman and
the exact accuracy-best one-pole tracker; continuous-time elasticities. Own code."""
import math, json
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import k0, k1
from gridengine import analyse, linear_f, bayes_f, kalman_pole
N = 1.0; s = 10.0
def allq(lam, mu, D):
    s = math.sqrt(N / D); p = (1 - math.exp(-2 * lam * D)) / 2
    bay = analyse(bayes_f(p), 2 * mu * D / N, lam, mu, N, D, 16.0, 0.02)
    pole, _ = kalman_pole(lam, mu, N, D)
    def lin(t):
        a = 1 - (1 - pole) * t; sn = s / math.sqrt(1 - a * a)
        return analyse(linear_f(a), 1.0, lam, mu, N, D, mu / (1 - a) + 7 * sn, s / 8)
    kal = lin(1.0)
    r = minimize_scalar(lambda u: lin(math.exp(u))["err"], bounds=(0.0, 1.2), method="bounded", options=dict(xatol=1e-5))
    l01 = lin(math.exp(r.x))
    return dict(bayes=bay["tA"], kalman=kal["tA"], lin01=l01["tA"], t01=math.exp(r.x))
out = {}
out["A"] = allq(0.01, 2.0, 0.01)
out["C_kfixed_x2"] = allq(0.02, math.sqrt(8.0), 0.01)
out["C_kfixed_x2_D/2"] = allq(0.02, math.sqrt(8.0), 0.005)   # same lam*D as A: exact time rescaling expected (ratio 0.5)
for c in ("C_kfixed_x2", "C_kfixed_x2_D/2"):
    out["ratio_" + c] = {q: out[c][q] / out["A"][q] for q in ("bayes", "kalman", "lin01")}
# continuous-time: separation per dln kappa, Bayes t_A vs Kalman memory time
def ell(k): return math.log(2 / k) - np.euler_gamma - 1
out["half_minus_inv_ell"] = {k: 0.5 - 1 / ell(k) for k in (0.0025, 0.005, 0.01)}
fB = lambda k: (k / 2) * ell(k); fL = lambda k: 1 / (2 * math.sqrt(1 + 1 / k))
out["cont_sep_per_dlnk_A_to_B"] = (math.log(fB(0.01) / fB(0.0025)) - math.log(fL(0.01) / fL(0.0025))) / math.log(4)
print(json.dumps(out, indent=1, default=float))
json.dump(out, open("q1_scaling.json", "w"), indent=1, default=float)
