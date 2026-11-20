"""V1b: the map theorem with READING PRICED (the reviewer's C0): every design also chooses how precisely its units read.
   nice -n 19 python3 figures/face_collapse_v1b.py [M]       writes face_collapse_v1b.json
Each unit reading at noise density N costs c/N per unit time (precision priced linearly, the face model's C0/N).  Each design picks its
own N (bounded scalar search over log N); errors are computed numerically (face_hybrid.best_fast).  The coordinates become NET worths.
'agree' checks that the exact decision rule (face_map.decide, with kappa_L, kappa_S on net worths) reproduces brute force: an identity check.
It does NOT show that the quadrant edges decide: priced reading is paid once by 'both', so value can be superadditive (kappa > 1) and BOTH
can win below the edges (review 26, counterexample A; tools/test_face_map.py).  face_subadd.py counts kappa > 1 in these worlds."""
import os, sys, json, time
import numpy as np
from multiprocessing import Pool
from scipy.optimize import minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import face_map as fm
from face_hybrid import best_fast

def world(seed):
    r = np.random.default_rng(50_000 + seed)
    return dict(seed=seed, n=int(round(10 ** r.uniform(0, 3))), rho=r.uniform(0, 1) if r.uniform() < 0.7 else 1.0, lead=10 ** r.uniform(-3, 1),
                wu=10 ** r.uniform(-1, 4.5), hl=1.0, hc=10 ** r.uniform(-1, 2.5), c=10 ** r.uniform(-4, 1))

def job(seed):
    p = world(seed); n, rho, l, wu, c = p['n'], p['rho'], p['lead'], p['wu'], p['c']; a, v = 1.0, 1.0
    def err(kind, lnN):
        N = np.exp(lnN)
        if kind == 'L': return v - fm.gains_ou(v, a, N, n, rho, l)[0]
        if kind == 'S': return v - fm.gains_ou(v, a, N, n, rho, l)[1]
        return min(best_fast([a], [v], N, n, rho, l, 1, 1, starts=1, seed=seed)[0], v - max(fm.gains_ou(v, a, N, n, rho, l)[:2]))
    out = {}
    for kind in ('L', 'S', 'B'):
        f = lambda x: n * c / np.exp(x) + n * wu * err(kind, x)
        r = minimize_scalar(f, bounds=(-12, 12), method='bounded', options=dict(xatol=1e-4))
        out[kind] = (r.fun, float(np.exp(r.x)), err(kind, r.x))
    cost = [n * wu * v, n * p['hl'] + out['L'][0], p['hc'] + out['S'][0], n * p['hl'] + p['hc'] + out['B'][0]]
    brute = int(np.argmin(cost))
    XL = (n * wu * v - out['L'][0]) / (n * p['hl']); XS = (n * wu * v - out['S'][0]) / p['hc']; nu = n * p['hl'] / p['hc']
    # both's extra over local, as a share of the shared layer's net worth: kS = (value_B - value_L)/value_S (net of reading)
    netS = n * wu * v - out['S'][0]; kS = ((out['L'][0] - out['B'][0]) / netS) if netS > 0 else 0.0
    kL = ((out['S'][0] - out['B'][0]) / (n * wu * v - out['L'][0])) if XL > 0 else 0.0
    mp = int(fm.decide(XL, XS, nu, kL, kS))
    return dict(p, XL=float(XL), XS=float(XS), nu=nu, kL=float(kL), kS=float(kS), brute=brute, map=mp, NL=out['L'][1], NS=out['S'][1])

if __name__ == '__main__':
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    t0 = time.time()
    with Pool(5) as pool: res = sorted(pool.map(job, range(M)), key=lambda r: r['seed'])
    summ = dict(M=M, agree=float(np.mean([r['brute'] == r['map'] for r in res])), frac=[float(np.mean([r['brute'] == k for r in res])) for k in range(4)], secs=time.time() - t0)
    print(summ); json.dump(dict(summary=summ, worlds=res), open(os.path.join(HERE, 'face_collapse_v1b.json'), 'w'))
