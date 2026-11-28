"""PREREG_2 extension: extra gated rho (0.64, 1.28) for the A-member arms (AA, RA). Reuses the locked
run_onset.job unchanged.  Usage: python run_onset2.py OUT.jsonl"""
import sys, os, json
from multiprocessing import Pool
import run_onset as ro
if __name__ == '__main__':
    os.nice(19)
    C = json.load(open('GRID_CENTERS_2.json'))['ext']; out = sys.argv[1]
    done = set()
    if os.path.exists(out):
        for l in open(out): d = json.loads(l); done.add((d['arm'], d['cell'], d['seed']))
    J = [(arm, 'rho=%g' % float(r), float(r), 1.0, c, s, 'es') for arm, d in C.items() for r, c in d.items() for s in range(16)]
    J = [a for a in J if (a[0], a[1], a[5]) not in done]
    print('jobs', len(J), flush=True)
    with Pool(3) as p, open(out, 'a') as f:
        for i, line in enumerate(p.imap_unordered(ro.work, J)):
            f.write(line + '\n'); f.flush()
