"""Secondary (PREREG sec 5): free size in regime D. Each tracker picks its own N to minimize J; then b vs competitors."""
import json, numpy as np, collections
import duel_core as d
from duel_grid import a_eval, b_eval, TS, EPSS
LAMS = [1e-4, 1e-3, 1e-2, 1e-1]
NSF = list(range(2, 65)) + [80, 96, 128, 160, 192, 256]
RF = [0.5, 0.85, 1.0, 1.15, 2.0]
def run_T(T):
    cfg = dict(reg='D', T=T, s=0.0, kobs=None); res = {}
    for N in NSF:
        rstar = 2*np.pi/np.sin(2*np.pi/N) if N >= 3 else 2*np.pi*N
        a1 = a_eval(N, cfg, None, r=0.0); a3 = [a_eval(N, cfg, None, r=f*rstar) for f in RF]
        for eps in EPSS:
            sb, tb, c = b_eval(N, cfg, eps)
            res[(N, eps)] = dict(b=(sb if (sb is not None and tb <= eps*(1+1e-6)) else None),
                                  a=min([x[0] for x in [a1]+a3 if x[1] <= eps], default=None))
    return T, res
if __name__ == '__main__':
    from multiprocessing import Pool
    with Pool(5) as p: out = dict(p.map(run_T, TS))
    lines = []; agg = collections.defaultdict(collections.Counter)
    for T in TS:
        for eps in EPSS:
            for lam in LAMS:
                best = {}
                for pricing in ['FC1', 'FC2']:
                    def Jmin(kind, Kf):
                        vals = [(lam*np.log(Kf(N)) + out[T][(N, eps)][kind], N) for N in NSF if out[T][(N, eps)][kind] is not None]
                        return min(vals) if vals else (None, None)
                    Jb, Nb = Jmin('b', (lambda N: N*N) if pricing == 'FC1' else (lambda N: 2*N-1))
                    Jc, Nc = Jmin('b', lambda N: 2*N-1)
                    Ja, Na = Jmin('a', lambda N: N)
                    def cmp(x):
                        if Jb is None and x is None: return None
                        if Jb is None: return 'LOSE'
                        if x is None: return 'WIN'
                        tol = 0.01*max(Jb, x) + 1e-12
                        return 'WIN' if x - Jb > tol else ('LOSE' if Jb - x > tol else 'TIE')
                    for readdef, comps in [('R-Hol', [Ja, Jc]), ('R-Hardy', [Ja])]:
                        r = [cmp(x) for x in comps]; r = [x for x in r if x is not None]
                        o = None if not r else ('LOSE' if 'LOSE' in r else ('WIN' if all(x == 'WIN' for x in r) else 'TIE'))
                        if o: agg[(pricing, readdef)][o] += 1
                        if lam == 1e-2 and eps == 1e-2:
                            lines.append(f"T={T} eps={eps} lam={lam} {pricing} {readdef}: b J={Jb and round(Jb,5)} (N={Nb}), a J={Ja and round(Ja,5)} (N={Na}), c1 J={Jc and round(Jc,5)} (N={Nc}) -> {o}")
    print("\n".join(lines))
    for k, v in agg.items():
        n = sum(v.values()); lab = 'WIN' if v['WIN']/n >= .9 and v['LOSE'] == 0 else ('LOSE' if v['LOSE']/n >= .5 else ('TIE' if v['TIE']/n >= .9 else 'MIXED'))
        print("free-size", k, lab, dict(v))
