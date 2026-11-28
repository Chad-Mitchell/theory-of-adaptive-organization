"""Scored run with the n=4 random-start count reduced from 100 to 25 per decoder class (DEVIATIONS.md, entry of 28 Nov 2026 12:20 AM ET).
It does not edit the locked sc_run.py: it imports it, patches COUNTS[4], and runs the same tasks. The start indices 0..24 and the
per-start seeds are the first 25 of the locked sequence, and the embedded start is kept. Usage: python3 sc_run_reduced.py --arm A|B [--procs K]"""
import argparse, json, os, time
from multiprocessing import Pool
import sc_run

sc_run.COUNTS[4] = 25

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--arm', required=True, choices=['A', 'B'])
    ap.add_argument('--procs', type=int, default=6)
    a = ap.parse_args()
    T = sc_run.tasks(a.arm, False)
    print(f'arm {a.arm} (n=4 random starts 25 per class): {len(T)} tasks, {a.procs} procs', flush=True)
    t0 = time.time(); res = []
    with Pool(a.procs) as pool:
        for k, r in enumerate(pool.imap_unordered(sc_run.work, T, chunksize=2)):
            if r is not None:
                res.append(r)
            if (k + 1) % 100 == 0:
                print(f'  {k+1}/{len(T)} done, {time.time()-t0:.0f}s', flush=True)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, f'sc_{a.arm}.json'), 'w') as f:
        json.dump(res, f)
    print(f'wrote sc_{a.arm}.json: {len(res)} results, {time.time()-t0:.0f}s')
