"""Apply PREREG sec 6 decision rule to grid_results.json. Writes decisions.out."""
import json, numpy as np, collections, sys
rows = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'grid_results.json'))
LAMS = [0, 1e-4, 1e-3, 1e-2, 1e-1]

def Kmap(pricing, N, kused):
    if pricing == 'FC1':  return dict(a=N, b=N*N, c1=2*N-1, o=2*N-1)
    if pricing == 'FC2':  return dict(a=N, b=kused, c1=2*N-1, o=2*N-1)
    if pricing == 'FC1n': return dict(a=N-1, b=N*N-1, c1=2*N-2, o=2*N-2)
    if pricing == 'FC2n': return dict(a=N-1, b=kused-1, c1=2*N-2, o=2*N-2)

def lnK(k):
    return 0.0 if k <= 1 else np.log(k)

def cmp(Jb, Jx):
    if Jb is None and Jx is None: return None
    if Jb is None: return 'LOSE'
    if Jx is None: return 'WIN'
    tol = 0.01*max(Jb, Jx) + 1e-12
    dJ = Jx - Jb
    return 'WIN' if dJ > tol else ('LOSE' if dJ < -tol else 'TIE')

def cell(row, lam, pricing, readdef, variant):
    N = row['N']; kused = row['b'].get('K_used', 2*N-1)
    K = Kmap(pricing, N, kused)
    J = lambda tr, kk: (lam*lnK(kk) + row[tr]['stake']) if row[tr]['feas'] else None
    Jb = J('b', K['b']); Jc1 = J('b', K['c1']); Jo = J('b', K['o'])
    a_list = ['a1'] if variant == 'strict' else (['a1', 'a3', 'a2'] if variant == 'ticks' else ['a1', 'a3'])
    aJ = [J(a, K['a']) for a in a_list]; aJ = [x for x in aJ if x is not None]
    Ja = min(aJ) if aJ else None
    comps = {'a': Ja}
    if readdef == 'R-Hol': comps['c1'] = Jc1
    res = {k: cmp(Jb, v) for k, v in comps.items()}
    if all(v is None for v in res.values()) and Jb is None: return None, res, cmp(Jb, Jo)
    vals = [v for v in res.values() if v is not None]
    if 'LOSE' in vals: out = 'LOSE'
    elif vals and all(v == 'WIN' for v in vals): out = 'WIN'
    else: out = 'TIE'
    return out, res, cmp(Jb, Jo)

def aggregate(cells):
    n = len(cells); c = collections.Counter(cells)
    if n == 0: return 'EMPTY', c
    if c['WIN']/n >= 0.9 and c['LOSE'] == 0: lab = 'WIN'
    elif c['LOSE']/n >= 0.5: lab = 'LOSE'
    elif c['TIE']/n >= 0.9: lab = 'TIE'
    else: lab = 'MIXED'
    return lab, c

out = []
summary = {}
for reg in ['D', 'S1', 'S2']:
    for readdef in ['R-Hol', 'R-Hardy']:
        for pricing in ['FC1', 'FC2', 'FC1n', 'FC2n']:
            for variant in (['main', 'strict', 'ticks'] if reg != 'S2' else ['main', 'ticks']):
                cells = []; cells0 = []; pervs = collections.Counter(); orb = collections.Counter()
                byT = collections.defaultdict(collections.Counter)
                for row in rows:
                    if row['reg'] != reg: continue
                    for lam in LAMS:
                        o, res, oc = cell(row, lam, pricing, readdef, variant)
                        if o is None: continue
                        (cells if lam > 0 else cells0).append(o)
                        if lam > 0:
                            for k, v in res.items(): pervs[(k, v)] += 1
                            orb[oc] += 1; byT[row['T']][o] += 1
                lab, c = aggregate(cells); lab0, c0 = aggregate(cells0)
                summary[(reg, readdef, pricing, variant)] = lab
                out.append(f"{reg:3s} {readdef:8s} {pricing:5s} {variant:7s} | lambda>0: {lab:6s} {dict(c)} | lambda=0: {lab0:6s} {dict(c0)} | per-competitor {dict(pervs)} | b vs orbitope {dict(orb)}")
                out.append("      by T/tau: " + "; ".join(f"{T}: {dict(v)}" for T, v in sorted(byT.items())))
print("\n".join(out))
print("\nSTEP (ii) CRITERION (PREREG sec 6): quantum WIN in D under R-Hol with FC1 or FC2 (main variant)?")
for p in ['FC1', 'FC2']:
    print(f"  D R-Hol {p} main: {summary[('D','R-Hol',p,'main')]}")
print("  D R-Hardy FC1 main:", summary[('D','R-Hardy','FC1','main')], "| FC2 main:", summary[('D','R-Hardy','FC2','main')])
