"""T67 main run (PREREG_T67.md). Usage: run_t67.py d n  -> raw_d{d}_n{n}.json"""
import sys, os, json, time, numpy as np, scipy.linalg as sl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t67lib import *

LS = {(1, 1024): [8, 16, 32, 64, 128], (1, 2048): [16, 32, 64, 128, 256],
      (2, 48): [2, 3, 4, 6, 8, 12], (2, 64): [3, 4, 6, 8, 12, 16]}
GRID = {1: [round(0.6 + 0.1 * i, 1) for i in range(25)], 2: [round(1.1 + 0.1 * i, 1) for i in range(30)]}

d, n = int(sys.argv[1]), int(sys.argv[2])
N = n ** d
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"raw_d{d}_n{n}.json")
res = {"d": d, "n": n, "Ls": LS[(d, n)], "grid": GRID[d], "rows": [], "gate": {"res_max": 0.0, "eq_idot_max": 0.0}}
t0 = time.time()
for p in GRID[d]:
    K = dense_K(d, n, p); lam = spectrum(d, n, p)
    SEQ = lyap_fourier(d, n, lam, np.ones(N))
    res["gate"]["res_max"] = max(res["gate"]["res_max"], residual(K, SEQ, np.ones(N)))
    cEQ = sl.cho_factor(SEQ, lower=True)
    for L in LS[(d, n)]:
        A = region(d, n, L)
        row = {"p": p, "L": L}
        I, idot, t1, t2 = quantities(K, SEQ, np.ones(N), A, cEQ)
        row["EQ"] = [I, idot, t1, t2]
        res["gate"]["eq_idot_max"] = max(res["gate"]["eq_idot_max"], abs(idot))
        for drive in ["HOT", "COLD"]:
            T = temps(N, A, drive)
            S = lyap_fourier(d, n, lam, T)
            res["gate"]["res_max"] = max(res["gate"]["res_max"], residual(K, S, T))
            row[drive] = list(quantities(K, S, T, A))
        res["rows"].append(row)
    print(f"d={d} n={n} p={p} done {time.time()-t0:.0f}s", flush=True)
    json.dump(res, open(out, "w"))
print("FINISHED", json.dumps(res["gate"]), flush=True)
