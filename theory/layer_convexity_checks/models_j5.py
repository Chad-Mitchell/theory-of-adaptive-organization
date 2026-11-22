#!/usr/bin/env python3
"""Fresh Model S worlds with J = 5 modes (not S5 seeds): convexity and the halving
ratio eps_{K+1}/eps_K, with the S5 solver (merged #116 mse_given_b, reviewer
multi-start incl. a short differential evolution). Also the band-model curve
(tools/layer_convexity_checks.py) on the same worlds for a shape comparison.
NUMERICAL evidence only; it is not part of the proof.

Run: nice -n 19 python3 theory/layer_convexity_checks/models_j5.py
"""
import importlib.util, json, sys, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; REPO = HERE.parents[1]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
s5 = load("s5_lc", REPO / "core" / "keystone_checks" / "s5_rerun.py")
lc = load("lc_checks", REPO / "tools" / "layer_convexity_checks.py")

def world(seed):
    rng = np.random.default_rng(5_000_000 + seed)     # disjoint from S5 (1000+seed)
    J = 5
    sep = 10 ** rng.uniform(0.5, 2.0, J - 1)
    taus = np.cumprod(np.r_[10 ** rng.uniform(0, 1), sep])
    v = 10 ** rng.uniform(-1.5, 1.5, J); N = 10 ** rng.uniform(-2, 1)
    return 1 / taus, v, float(N)

def one(seed):
    a, v, N = world(seed); t0 = time.time()
    Ei = s5.stores.E_inf(a, v, N)
    E = [float(np.sum(v))]
    for K in range(1, 6):
        E.append(s5.optimize_K(a, v, N, K, seed=seed, n_rand=8, use_de=True, de_maxiter=15)["E"])
    eps = [e / Ei - 1 for e in E]
    w, mu, W, Eb_inf = lc.spectrum_grid(lc.ou_S(a, v), lambda w: N + 0 * w, a.min() * 1e-3, a.max() * 1e3 + 100, 320)
    epsB = (lc.band_curve(mu, W, 5) / Eb_inf).tolist()
    return dict(seed=seed, a=a.tolist(), v=v.tolist(), N=N, Einf=Ei, eps=eps, epsB=epsB,
                convex_0J=lc.is_convex(eps, 1e-4), convex_1J=lc.is_convex(eps[1:], 1e-4),
                halving=all(eps[K + 1] <= eps[K] / 2 + 1e-6 for K in range(5) if eps[K] > 1e-4),
                elapsed=time.time() - t0)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    with ProcessPoolExecutor(6) as ex:
        out = list(ex.map(one, range(n)))
    ratios = [o["eps"][K + 1] / o["eps"][K] for o in out for K in range(1, 4) if o["eps"][K] > 1e-4]
    summ = dict(worlds=n, convex_0J=sum(o["convex_0J"] for o in out), convex_1J=sum(o["convex_1J"] for o in out),
                halving=sum(o["halving"] for o in out), max_ratio_K1to3=max(ratios) if ratios else None,
                below_causal=sum(any(e < -1e-6 for e in o["eps"]) for o in out))
    print(json.dumps(summ, indent=1))
    json.dump(dict(summary=summ, worlds=out), open(HERE / "models_j5.json", "w"), indent=1)
