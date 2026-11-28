"""V1: the map theorem on randomly drawn one-component worlds, by brute force.   nice -n 19 python3 figures/face_collapse_v1.py
For each world: draw raw parameters (noise, units, shared fraction, delay, stakes, two upkeeps), compute the error of each design NUMERICALLY
(first-order stores, rates optimized, covariances from a Lyapunov equation: face_hybrid.py; no closed form used), take the cheapest design,
and compare with the map's reading from the CLOSED-FORM X_L, X_S (face_map.py) and the numerical overlap k.  Writes face_collapse_v1.json."""
import os, sys, json, time
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import face_map as fm
from face_hybrid import best_fast as best

def world(seed):
    r = np.random.default_rng(seed)
    a, v = 1.0, 1.0                                   # time unit = the component's time scale, signal unit = its sd
    N = 10 ** r.uniform(-3, 2); n = int(round(10 ** r.uniform(0, 3))); rho = r.uniform(0, 1) if r.uniform() < 0.7 else 1.0
    lead = 10 ** r.uniform(-3, 1); wu = 10 ** r.uniform(-1, 4.5); hl = 1.0; hc = 10 ** r.uniform(-1, 2.5)
    return dict(seed=seed, a=a, v=v, N=N, n=n, rho=rho, lead=lead, wu=wu, hl=hl, hc=hc)

def job(seed):
    p = world(seed); a, v, N, n, rho, l = p['a'], p['v'], p['N'], p['n'], p['rho'], p['lead']
    eL = best([a], [v], N, n, rho, l, 1, 0, starts=2, seed=seed)[0]
    eS = best([a], [v], N, n, rho, l, 0, 1, starts=2, seed=seed)[0]
    eB = best([a], [v], N, n, rho, l, 1, 1, starts=4, seed=seed)[0]
    eB = min(eB, eL, eS)
    cost = [n * p['wu'] * v, n * p['hl'] + n * p['wu'] * eL, p['hc'] + n * p['wu'] * eS, n * p['hl'] + p['hc'] + n * p['wu'] * eB]
    brute = int(np.argmin(cost))
    GL, GS, pi = fm.gains_ou(v, a, N, n, rho, l)
    XL = p['wu'] * GL / p['hl']; XS = n * p['wu'] * GS / p['hc']; nu = n * p['hl'] / p['hc']
    GB = v - eB; kS = (GB - GL) / GS if GS > 0 else 0.0; kL = (GB - GS) / GL
    mp = int(fm.decide(XL, XS, nu, kL, kS))
    return dict(p, eL=eL, eS=eS, eB=eB, GL_num=v - eL, GS_num=v - eS, GL=float(GL), GS=float(GS), pi=float(pi), XL=float(XL), XS=float(XS), nu=nu,
                kL=float(kL), kS=float(kS), brute=brute, map=mp, R=p['wu'] * v / p['hl'], lat=l * a,
                gap=float(sorted(cost)[1] / sorted(cost)[0] - 1))

if __name__ == '__main__':
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    t0 = time.time(); out = []
    with Pool(6) as pool:
        for i, r in enumerate(pool.imap_unordered(job, range(M))):
            out.append(r)
            if i % 50 == 0: print(i, f'{time.time() - t0:.0f}s', flush=True)
    out.sort(key=lambda r: r['seed'])
    agree = np.mean([r['brute'] == r['map'] for r in out])
    relL = max(abs(r['GL_num'] / r['GL'] - 1) for r in out); relS = max(abs(r['GS_num'] / r['GS'] - 1) for r in out if r['GS'] > 1e-6)
    summ = dict(M=M, agree=float(agree), max_rel_err_GL=relL, max_rel_err_GS=relS, max_kS=max(r['kS'] for r in out), max_kL=max(r['kL'] for r in out),
                frac_both=float(np.mean([r['brute'] == 3 for r in out])), secs=time.time() - t0)
    print(summ)
    json.dump(dict(summary=summ, worlds=out), open(os.path.join(HERE, 'face_collapse_v1.json'), 'w'))
