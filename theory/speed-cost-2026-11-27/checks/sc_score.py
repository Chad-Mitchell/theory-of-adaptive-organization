"""Scoring (locked). Reads sc_A.json and sc_B.json, applies the bars of PREREG.md section 3, prints the outcome per bar.
Usage: python3 sc_score.py [--toy]"""
import json, os, sys
import numpy as np
from sc_lib import *
from paper_two_state import grid, two_state_closed
from sc_run import ARM_B_POINTS, TOY_B_POINTS

TAU = 2e-4          # B1: floor reached if E <= TAU
QFRAC = 0.10        # B2: miss if a 3- or 4-state design removes more than this share of the two-state excess
B3_BAND = (8.0, 12.5)
B4_SHARE = 0.20
here = os.path.dirname(os.path.abspath(__file__))

def load(arm, toy):
    with open(os.path.join(here, ('toy_run_' if toy else 'sc_') + arm + '.json')) as f:
        return json.load(f)

def best_by(res, key):
    out = {}
    for r in res:
        if not r['ok']:
            continue
        k = key(r)
        if k not in out or r['E'] < out[k]['E']:
            out[k] = r
    return out

def repro(res, key, best, tol=1e-6):
    cnt = {}
    for r in res:
        if r['ok']:
            k = key(r)
            if abs(r['heat'] - best[k]['heat']) <= tol * abs(best[k]['heat']):
                cnt[k] = cnt.get(k, 0) + 1
    return cnt

def main(toy):
    A = load('A', toy)
    key = lambda r: (r['pi'], r['n'])
    best = best_by(A, key)
    rep = repro(A, key, best)
    pts = grid(toy)
    ptsB = TOY_B_POINTS if toy else ARM_B_POINTS
    print('== code gates ==')
    gate_ok = True
    for pi, (G, e) in enumerate(pts):
        if (pi, 2) in best:
            h2 = two_state_closed(G, e)[0]
            rel = abs(best[(pi, 2)]['heat'] - h2) / h2
            if rel > 1e-6:
                gate_ok = False; print(f'  GATE FAIL n=2 vs closed form at G={G} eps={e}: rel {rel:.2e}')
    for r in A:
        if r['ok'] and (r['capviol'] > 1e-7 or r['eps'] > r['eps0'] + 1e-7):
            gate_ok = False; print('  GATE FAIL cap or error violated', r['pi'], r['n']); break
    for r in A:
        if r['ok'] and r['E'] < -1e-6:
            gate_ok = False; print('  GATE FAIL design below the proved floor (T60 section 4): code error', r['pi'], r['n'], r['E']); break
    for pi in range(len(pts)):
        for n in (3, 4):
            if (pi, n) in best and (pi, 2) in best and best[(pi, n)]['heat'] > best[(pi, 2)]['heat'] * (1 + 1e-5):
                gate_ok = False; print(f'  GATE FAIL n={n} worse than n=2 at point {pi} (embedded start broken; tolerance 1e-5 relative, the numerical floor of the 1e-9 rate lower bound)')
    print('  code gates:', 'PASS' if gate_ok else 'FAIL (bars below are not scored)')
    print('\n== arm A table: best-found excess E = heat / (r L(eps)) - 1 ==')
    print(f'{"G":>6} {"eps":>5} {"E2":>11} {"E3":>11} {"E4":>11} {"Qfrac":>8} {"best":>11} {"reach":>6} {"repro(n=2,3,4)":>16}')
    qmax = (0, None); reached = []; Ebest = {}
    for pi, (G, e) in enumerate(pts):
        Es = {n: best[(pi, n)]['E'] if (pi, n) in best else float('nan') for n in (2, 3, 4)}
        Eb = np.nanmin(list(Es.values()))
        Ebest[(G, e)] = Eb
        qf = max(0.0, 1 - np.nanmin([Es[3], Es[4]]) / Es[2]) if Es[2] == Es[2] else float('nan')
        if qf > qmax[0]:
            qmax = (qf, (G, e))
        reach = Eb <= TAU
        if reach:
            reached.append((G, e, Eb))
        rp = tuple(rep.get((pi, n), 0) for n in (2, 3, 4))
        print(f'{G:>6} {e:>5} {Es[2]:>11.6f} {Es[3]:>11.6f} {Es[4]:>11.6f} {qf:>8.4f} {Eb:>11.6f} {str(reach):>6} {str(rp):>16}')
    print('\n== bars ==')
    print(f'B1 (floor reached within {TAU} at any point?): ', 'MISS ' + str(reached) if reached else 'HIT (no point reaches the floor; min over points of best E = %.6f)' % min(Ebest.values()))
    print(f'B2 (max share of two-state excess removed by n=3,4 <= {QFRAC}?): max Qfrac = {qmax[0]:.4f} at {qmax[1]}:', 'HIT' if qmax[0] <= QFRAC else 'MISS')
    ok3 = True; s3 = []
    for e in (0.05, 0.1, 0.2, 0.3):
        if (100, e) in Ebest and (1000, e) in Ebest:
            q = Ebest[(100, e)] / Ebest[(1000, e)]; s3.append((e, round(q, 4)))
            ok3 &= B3_BAND[0] <= q <= B3_BAND[1]
    print(f'B3 (E(100)/E(1000) in {B3_BAND} at every eps?): {s3}:', 'HIT' if ok3 else 'MISS')
    try:
        B = load('B', toy)
        bestB = best_by(B, key)
        print('\n== arm B (per-edge cap), best-found E ==')
        out = {}
        for pi, (G, e) in enumerate(ptsB):
            Es = {n: bestB[(pi, n)]['E'] if (pi, n) in bestB else float('nan') for n in (2, 3, 4)}
            qf = max(0.0, 1 - np.nanmin([Es[3], Es[4]]) / Es[2])
            out[(G, e)] = qf
            print(f'  G={G} eps={e}: E2={Es[2]:.6f} E3={Es[3]:.6f} E4={Es[4]:.6f} share removed={qf:.4f}')
        q = out[ptsB[1]]
        print(f'B4 (per-edge cap: n<=4 removes >= {B4_SHARE} of the two-state excess at G=20, eps=0.1?): share {q:.4f}:', 'HIT' if q >= B4_SHARE else 'MISS')
    except FileNotFoundError:
        print('arm B file not found')

if __name__ == '__main__':
    main('--toy' in sys.argv)
