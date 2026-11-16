"""Pre-lock: (1) best-linear (0-1 payoff) optimum's t_A at arms A and B, large sample (prediction of the rival);
(2) noise pilot of the learner at pilot point P (kappa = 0.005, q fixed; NOT an outcome arm). nice 19."""
import json, math, sys, numpy as np
sys.path.insert(0, '.'); from core import *; from learner import *
out = {}
arms = {"A": (0.01, 2.0), "B": (0.02, math.sqrt(2.0)), "P": (0.01 * math.sqrt(2), math.sqrt(4 / math.sqrt(2)))}
for k in ("A", "B"):
    lam, mu = arms[k]; pole, _ = kalman_pole(lam, mu, N, D)
    best = None
    for t in np.exp(np.linspace(math.log(1/4), math.log(4), 17)):
        pp = (1 - pole) * t / 2
        s = stats(lam, mu, N, D, pp, 1.0, 1_000_000, range(1, 21), lin=True)
        if best is None or s["err"] < best[1]["err"]: best = (t, s)
    out[f"bestlin01_{k}"] = dict(pole_tx=best[0], **best[1])
    print(k, out[f"bestlin01_{k}"], flush=True)
lam, mu = arms["P"]
R = [learner(lam, mu, 20, 200, 500 + i) for i in range(10)]
lt = np.log([r["tA"] for r in R])
out["pilot_P"] = dict(R=R, sd_log_tA=float(lt.std(ddof=1)), mean_log_tA=float(lt.mean()))
print("pilot sd_log", out["pilot_P"]["sd_log_tA"], [ (r['lin'], round(r['pp_over_p'],2), round(r['g_over_gB'],2), round(r['tA'],3)) for r in R])
json.dump(out, open('pilot.json', 'w'), indent=1, default=float)
