"""POST HOC (NOT preregistered): the preregistered estimator applied to the corner-free strip runs (posthoc_strip.py)."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from t67lib import approach_exponent, p_crossing
print("POST HOC strip diagnosis (not preregistered; cannot change the preregistered outcome)")
for n in [256, 512, 1024]:
    f = os.path.join(HERE, f"strip_n{n}.json")
    if not os.path.exists(f): continue
    r = json.load(open(f)); grid = [x["p"] for x in r["rows"]]
    print(f"\n-- strip n={n}, ladder L={r['Ls']}, boundary 2n --")
    res = {}
    for q, (dr, k) in {"I_EQ": ("EQ", 0), "I_HOT": ("HOT", 0), "Idot_HOT": ("HOT", 1), "I_COLD": ("COLD", 0), "Idot_COLD": ("COLD", 1)}.items():
        ss = [approach_exponent([abs(v[k]) / (2 * n) for v in row[dr]]) for row in r["rows"]]
        res[q] = ss
        pc = p_crossing(grid, ss)
        print(f"{q:10s} p_c={pc['p_c']:.3f} [{pc['status']}]  crossings={['%.3f'%c for c in pc['all']]}")
    print("p     " + " ".join(f"{q:>10s}" for q in res))
    for i, p in enumerate(grid):
        if p <= 2.2:
            print(f"{p:<5} " + " ".join(f"{res[q][i]:>10.4f}" if res[q][i] is not None else f"{'undef':>10s}" for q in res))
