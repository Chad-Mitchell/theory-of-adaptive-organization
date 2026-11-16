"""Pre-lock noise pilot for the MSE-payoff learner at pilot point P (kappa=0.005, q fixed; not an outcome arm);
plus large-sample MSE of Bayes vs Kalman at arms A, B (predictions). nice 19."""
import json, math, sys, numpy as np
sys.path.insert(0, '.'); from core import *; from learner import *
out = {}
arms = {"A": (0.01, 2.0), "B": (0.02, math.sqrt(2.0)), "P": (0.01 * math.sqrt(2), math.sqrt(4 / math.sqrt(2)))}
for k in ("A", "B"):
    lam, mu = arms[k]; pB, gB = bayes_params(lam, mu, N, D); pole, _ = kalman_pole(lam, mu, N, D)
    rb = run2(lam, mu, N, D, pB, gB, 20_000_000, 3, False); rl = run2(lam, mu, N, D, (1 - pole) / 2, 1.0, 20_000_000, 3, True)
    out[f"mse_{k}"] = dict(bayes=mse_of(rb, mu), kalman=mse_of(rl, mu))
    print(k, out[f"mse_{k}"], flush=True)
lam, mu = arms["P"]
R = [learner_mse(lam, mu, 20, 200, 700 + i) for i in range(8)]
lt = np.log([r["tA"] for r in R])
out["pilot_P_mse"] = dict(R=R, sd_log_tA=float(lt.std(ddof=1)), mean_log_tA=float(lt.mean()))
print("pilot sd_log", out["pilot_P_mse"]["sd_log_tA"], [(r['lin'], round(r['pp_over_p'], 2), round(r['g_over_gB'], 2), round(r['tA'], 3)) for r in R])
json.dump(out, open('pilot2.json', 'w'), indent=1, default=float)
