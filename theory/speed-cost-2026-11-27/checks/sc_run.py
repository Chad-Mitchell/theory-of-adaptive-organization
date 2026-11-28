"""Scored run (locked). Usage: python3 sc_run.py --arm A|B [--toy] [--procs K]
Writes sc_<arm>.json next to this file (toy: toy_run_<arm>.json). Never reads a scored output to decide anything.
Search space and counts are fixed below; no adaptive stopping."""
import argparse, json, os, sys, time
import numpy as np
from multiprocessing import Pool
from sc_lib import *
from paper_two_state import grid

MASTER_SEED = 20261127
TAU = 2e-4
COUNTS = {2: 20, 3: 150, 4: 100}      # random starts per (n, decoder class); plus one embedded two-state start each
ARM_B_POINTS = [(5, 0.3), (20, 0.1), (100, 0.1)]
TOY_B_POINTS = [(7, 0.35), (50, 0.15), (12, 0.25)]       # off the scored grid
NS = (2, 3, 4)

def tasks(arm, toy):
    pts = grid(toy) if arm == 'A' else (TOY_B_POINTS if toy else ARM_B_POINTS)
    out = []
    for pi, (G, e) in enumerate(pts):
        for n in NS:
            labs = labelings(n)
            for li, lam in enumerate(labs):
                cnt = COUNTS[n]
                for s in range(-1, cnt):      # s = -1 is the embedded start
                    out.append((arm, pi, G, e, n, li, lam, s))
    if toy:
        out = [t for t in out if t[7] < 1 and t[4] <= 3]   # toy: embedded start only, n<=3
    return out

def work(t):
    arm, pi, G, e, n, li, lam, s = t
    cap = 'exit' if arm == 'A' else 'edge'
    if s < 0:
        z0 = embedded_two_state_start(n, G, e, lam)
    else:
        rng = np.random.default_rng([MASTER_SEED, 0 if arm == 'A' else 1, pi, n, li, s])
        z0 = random_start(n, G, rng, cap)
    if z0 is None:
        return None
    r = solve_point(n, G, e, lam, cap, z0)
    if r is None:
        return None
    # one polish pass from the end point
    r2 = solve_point(n, G, e, lam, cap, r['z'])
    if r2 is not None and r2['ok'] and (not r['ok'] or r2['heat'] < r['heat']):
        r = r2
    fl = floor_heat(r['eps'])
    return {'arm': arm, 'pi': pi, 'G': G, 'eps0': e, 'n': n, 'lab': list(lam), 's': s, 'heat': r['heat'], 'eps': r['eps'],
            'ok': bool(r['ok']), 'capviol': r['capviol'], 'E': r['heat'] / fl - 1, 'z': [float(v) for v in r['z']]}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--arm', required=True, choices=['A', 'B'])
    ap.add_argument('--toy', action='store_true')
    ap.add_argument('--procs', type=int, default=6)
    a = ap.parse_args()
    T = tasks(a.arm, a.toy)
    print(f'arm {a.arm}: {len(T)} tasks, {a.procs} procs', flush=True)
    t0 = time.time(); res = []
    with Pool(a.procs) as pool:
        for k, r in enumerate(pool.imap_unordered(work, T, chunksize=4)):
            if r is not None:
                res.append(r)
            if (k + 1) % 500 == 0:
                print(f'  {k+1}/{len(T)} done, {time.time()-t0:.0f}s', flush=True)
    here = os.path.dirname(os.path.abspath(__file__))
    name = ('toy_run_' if a.toy else 'sc_') + a.arm + '.json'
    with open(os.path.join(here, name), 'w') as f:
        json.dump(res, f)
    print(f'wrote {name}: {len(res)} results, {time.time()-t0:.0f}s')
