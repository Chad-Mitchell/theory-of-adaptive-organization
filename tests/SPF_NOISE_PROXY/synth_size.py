#!/usr/bin/env python3
"""Pre-lock size/power check of gtest (parametric-bootstrap overidentification test) on synthetic truth.
Worlds UNEMP, TBILL, TBOND (fast, middle, slow; env.json point fits and survey counts). Arms a (size) and b lam=1 (power).
NP panels per world x arm, NSIM null simulations each. Usage: nice -n 19 python3 synth_size.py NP NSIM
"""
import json, os, sys
import numpy as np
import common, gtest

SEED = 20261115 + 41
W = ["UNEMP", "TBILL", "TBOND"]

def run(args):
    v, arm, lam, NP, NSIM, seed = args
    env = json.load(open(os.path.join(common.HERE, "..", "LFK_SPF", "results", "env.json")))
    e = env[v]["fit"]; T = int(env[v]["n_pairs"]); rng = np.random.default_rng(seed); res = []
    for _ in range(NP):
        K = float(np.exp(rng.uniform(np.log(0.01), np.log(1.0))))
        pan, xenv = common.synth_panel(e, K, arm, lam, rng, T=T)
        G, k, aux = gtest.g_stat(pan, xenv)
        null = gtest.null_G(aux["fit"], k["L0"][0], T, aux["nf"], NSIM, rng)
        res.append(dict(var=v, arm=arm, lam=lam, K=K, G=G, p=gtest.pval(G, null)))
    return res

if __name__ == "__main__":
    NP, NSIM = int(sys.argv[1]), int(sys.argv[2])
    from multiprocessing import Pool
    jobs = [(v, a, l, NP, NSIM, SEED + 10 * i + j) for i, v in enumerate(W) for j, (a, l) in enumerate([("a", 0.0), ("b", 1.0)])]
    with Pool(4) as p:
        rows = [r for rr in p.map(run, jobs) for r in rr]
    json.dump(rows, open(os.path.join(common.HERE, "results", "synth_size.json"), "w"))
    lines = []
    for a in ("a", "b"):
        rs = [r for r in rows if r["arm"] == a]
        lines.append(f"arm {a}: n={len(rs)} reject(p<0.05)={np.mean([r['p'] < 0.05 for r in rs]):.3f} "
                     f"reject(p<0.10)={np.mean([r['p'] < 0.10 for r in rs]):.3f} median G={np.median([r['G'] for r in rs]):+.2f}")
        for v in W:
            rv = [r for r in rs if r["var"] == v]
            lines.append(f"   {v:6s} reject(p<0.05)={np.mean([r['p'] < 0.05 for r in rv]):.2f}  p-values {[round(r['p'], 2) for r in rv]}")
    txt = "\n".join(lines); print(txt)
    open(os.path.join(common.HERE, "results", "synth_size.out"), "w").write(txt + "\n")
