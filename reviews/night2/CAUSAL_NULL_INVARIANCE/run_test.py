"""LOCKED outcome run (see PREREG.md). Do not edit after the lock commit. nice 19."""
import json, math, sys, numpy as np
sys.path.insert(0, '.'); from learner import learner_mse
R = 24; E_SW = 20; TEST_SW = 200
arms = {"A": (0.01, 2.0, 1000), "B": (0.02, math.sqrt(2.0), 2000)}
res = {k: [learner_mse(lam, mu, E_SW, TEST_SW, s0 + i) for i in range(R)] for k, (lam, mu, s0) in arms.items()}
lt = {k: np.log([r["tA"] for r in v]) for k, v in res.items()}
Dh = float(lt["B"].mean() - lt["A"].mean())
sig = float(math.sqrt(lt["A"].var(ddof=1) / R + lt["B"].var(ddof=1) / R))
z = 1.959964; pred = 0.3504; kap = 0.5
fail = Dh + z * sig < kap * pred; pas = (Dh - z * sig > 0) and not fail
verdict = "FAILED" if fail else ("PASSED" if pas else "INCONCLUSIVE")
out = dict(D=Dh, sigma=sig, pred_bayes=pred, kill_line=kap * pred, verdict=verdict,
           frac_linear={k: float(np.mean([r["lin"] for r in v])) for k, v in res.items()},
           mean_tA={k: float(np.exp(lt[k].mean())) for k in lt}, sd_log={k: float(lt[k].std(ddof=1)) for k in lt}, learners=res)
json.dump(out, open("test_result.json", "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in out.items() if k != "learners"}, indent=1, default=float))
