"""Independent check of the pre-lock 0-1 finding: finer pole grid, new seeds, more samples; also the Bnull point.
Reports t_A of the accuracy-best linear tracker and the Bayes error, and the flatness of accuracy in the pole. nice 19."""
import json, math, sys, numpy as np
sys.path.insert(0, '.'); from core import *
N = 1.0; D = 0.01
pts = {"A": (0.01, 2.0), "B": (0.02, math.sqrt(2.0)), "Bnull": (0.026546, math.sqrt(4 * 0.7534))}
out = {}
for k, (lam, mu) in pts.items():
    pole, _ = kalman_pole(lam, mu, N, D); rows = []
    for t in np.exp(np.linspace(math.log(1.0), math.log(4.0), 15)):
        s = stats(lam, mu, N, D, (1 - pole) * t / 2, 1.0, 2_000_000, range(101, 141), lin=True)
        rows.append((float(t), s["err"], s["tA"], s["se"]))
    e = np.array([r[1] for r in rows]); tx = np.log([r[0] for r in rows])
    c = np.polyfit(tx, e, 2); tbest = math.exp(-c[1] / (2 * c[0]))
    sb = stats(lam, mu, N, D, (1 - pole) * tbest / 2, 1.0, 4_000_000, range(201, 241), lin=True)
    out[k] = dict(rows=rows, pole_tx_best_quadfit=tbest, at_best=sb)
    print(k, round(tbest, 3), {kk: sb[kk] for kk in ("tA", "se", "err")}, flush=True)
out["dln_A_B"] = math.log(out["B"]["at_best"]["tA"] / out["A"]["at_best"]["tA"])
out["dln_A_Bnull"] = math.log(out["Bnull"]["at_best"]["tA"] / out["A"]["at_best"]["tA"])
print("dln A->B", out["dln_A_B"], "A->Bnull", out["dln_A_Bnull"])
json.dump(out, open("check_lin01.json", "w"), indent=1, default=float)
