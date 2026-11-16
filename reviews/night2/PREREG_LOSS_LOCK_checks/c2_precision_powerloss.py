"""C2 (own code, pick 37): precision effort under power loss, alpha = 2 (random walk, per-step drift variance q),
observations with noise variance N = 1/r per step, price pi per unit precision r (linear pricing, theta = 1).
Exact discrete steady-state Kalman (prediction) error variance V(q, N); Gaussian errors => E|e|^p = c_p V^{p/2};
Monte Carlo confirms the moment at one point. Claim: effort r* has elasticities a = 2alpha/(2alpha + p(alpha-1)) in w,
b = p/(2alpha + p(alpha-1)) in q (alpha = 2: 4/(4+p), p/(4+p); p = 2 gives 2/3, 1/3, THEORY 2.2)."""
import numpy as np, json
from math import gamma, sqrt, pi
from scipy.optimize import minimize_scalar

def V(q, N):  # filtered (posterior) steady-state variance for x_k = x_{k-1}+w, y = x + e
    P = q / 2 + np.sqrt(q * q / 4 + q * N)  # prior variance solves P = P N/(P+N) + q... use iteration for safety
    for _ in range(200):
        Pp = P * N / (P + N) + q
        P = Pp
    return P * N / (P + N)

def cp(p):  # E|Z|^p, Z ~ N(0,1)
    return 2 ** (p / 2) * gamma((p + 1) / 2) / sqrt(pi)

def rstar(w, q, p):
    f = lambda lr: np.exp(lr) + w * cp(p) * V(q, 1 / np.exp(lr)) ** (p / 2)
    return np.exp(minimize_scalar(f, bounds=(-30, 30), method="bounded", options={"xatol": 1e-9}).x)

out = {}
rng = np.random.default_rng(37002)
for p in (0.5, 1.0, 2.0, 4.0):
    q0 = 1e-6
    # choose w so that r* gives N ~ 1e2 q0^{-?}: memory >> 1 step (continuous limit): N*/q0 large
    w0 = {0.5: 1e2, 1.0: 1e3, 2.0: 1e5, 4.0: 1e9}[p]
    r0 = rstar(w0, q0, p)
    mem = np.sqrt((1 / r0) / q0)  # memory time in steps ~ sqrt(N/q)
    fac = np.exp(np.linspace(-1, 1, 9))
    a = np.polyfit(np.log(fac), np.log([rstar(w0 * f, q0, p) for f in fac]), 1)[0]
    b = np.polyfit(np.log(fac), np.log([rstar(w0, q0 * f, p) for f in fac]), 1)[0]
    out[f"p={p}"] = {"memory_steps": round(float(mem), 1), "a_hat": round(a, 4), "a_theory": round(4 / (4 + p), 4),
                     "b_hat": round(b, 4), "b_theory": round(p / (4 + p), 4)}
    print(p, out[f"p={p}"], flush=True)
# Monte Carlo moment check at one point (q=1e-4, N=1): steady Kalman, E|e|^p vs c_p V^{p/2}
q, N = 1e-4, 1.0
Vs = V(q, N); P = Vs + q; K = P / (P + N)
n = 2_000_000
x = np.cumsum(rng.normal(0, sqrt(q), n)); y = x + rng.normal(0, 1, n)
from scipy.signal import lfilter
xh = lfilter([K], [1, -(1 - K)], y)
e = (xh - x)[20000:]
out["mc_check"] = {f"p={p}": [round(float(np.mean(np.abs(e) ** p)), 6), round(cp(p) * Vs ** (p / 2), 6)] for p in (0.5, 1, 2, 4)}
print(out["mc_check"])
json.dump(out, open("c2_precision_powerloss.json", "w"), indent=1)
