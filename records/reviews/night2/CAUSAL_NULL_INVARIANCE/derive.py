"""Pre-lock derivations and predictions (no learner outcomes). nice 19."""
import json, math, sys, numpy as np
sys.path.insert(0, '.'); from core import *
N = 1.0; D = 0.01
pts = {"A_base": (0.01, 2.0), "B_qfixed_kx4": (0.02, math.sqrt(2.0)), "Bnull_split": (0.01 * 2.6546, 2.0 * math.sqrt(0.7534 * 2) / math.sqrt(2) ),
       "C_timescale_kfixed": (0.02, math.sqrt(8.0))}
# fix Bnull: mu^2 = 4*0.7534
pts["Bnull_split"] = (0.01 * 2.6546, math.sqrt(4 * 0.7534))
out = {}
seeds = range(1, 41); ns = 2_000_000
for k, (lam, mu) in pts.items():
    pB, gB = bayes_params(lam, mu, N, D)
    pole, K = kalman_pole(lam, mu, N, D)
    b = stats(lam, mu, N, D, pB, gB, ns, seeds)
    l = stats(lam, mu, N, D, (1 - pole) / 2, 1.0, ns, seeds, lin=True)
    out[k] = dict(lam=lam, mu2=mu**2, kappa=lam * N / mu**2, q=4 * lam * mu**2, tB_cont=tB_cont(lam, mu, N), tL_mem=tL_mem(lam, mu, N),
                  bayes=b, kalman=l, kalman_pole=pole)
    print(k, json.dumps(out[k], default=float), flush=True)
json.dump(out, open('derive.json', 'w'), indent=1, default=float)
