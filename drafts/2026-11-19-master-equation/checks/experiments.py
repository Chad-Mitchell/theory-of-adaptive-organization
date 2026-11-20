"""Experiments for VERDICT (A) and (B). Run: nice -n 19 python3 experiments.py > experiments.out"""
import numpy as np, json
from stores import E_K, E_inf, scalefree_world

def noise_at_fast_edge(a, v, frac=1.0):
    a = np.asarray(a); v = np.asarray(v); w = a.max()
    return frac * float(np.sum(v * 2 * a / (a**2 + w**2)))

def profile(a, v, N, Kmax):
    ei = E_inf(a, v, N); rows = []
    for K in range(1, Kmax + 1):
        e, lb = E_K(a, v, N, K)
        rows.append(dict(K=K, eps=(e - ei) / ei, taus=sorted((1/np.exp(lb)).tolist())))
    return ei, rows

def kstar(rows, R):
    costs = [r['K'] + R * (1 + r['eps']) for r in rows]
    return rows[int(np.argmin(costs))]['K']

out = {}
print("== Exp0: single-pole worlds (OU at several rates): eps_2 should be ~0 ==")
for a in [1.0, 0.01]:
    ei, rows = profile([a], [1.0], 0.05, 2)
    print(f" a={a}: eps1={rows[0]['eps']:.2e} eps2={rows[1]['eps']:.2e}")

print("\n== Exp1: cadence world, 3 OU modes at tau=1, 30, 1000 (equal variance) ==")
a = 1/np.array([1., 30., 1000.]); v = np.ones(3)/3; N = noise_at_fast_edge(a, v, 0.1)
ei, rows = profile(a, v, N, 4)
for r in rows: print(f" K={r['K']}: excess={r['eps']*100:8.3f}%  store taus={np.round(r['taus'],2)}")
print("  K* by R=w*Einf/h:", {R: kstar(rows, R) for R in [1, 10, 100, 1e3, 1e4, 1e6]})
out['cadence'] = rows

print("\n== Exp1b: two modes, separation ratio r (tau=1 and r), equal variance ==")
for rr in [1.5, 3, 10, 100, 1e4]:
    a = 1/np.array([1., rr]); v = np.array([.5, .5]); N = noise_at_fast_edge(a, v, 0.1)
    ei, rows = profile(a, v, N, 2)
    print(f" r={rr:>7}: flat excess eps1={rows[0]['eps']*100:7.3f}%   (K=2 exact: eps2={rows[1]['eps']:.1e})  layers pay iff R > {1/rows[0]['eps']:.3g}")

print("\n== Exp2: scale-free band (Lorentzian mixture, S~f^-alpha inside span), noise crossing at the fast edge ==")
tab = []
for alpha in [0.5, 1.0, 1.5, 1.9]:
    for span in [10, 100, 1e3, 1e4, 1e5]:
        a, v = scalefree_world(alpha, span)
        N = noise_at_fast_edge(a, v, 1.0)
        ei, rows = profile(a, v, N, 4)
        eps = [r['eps'] for r in rows]
        ks = {R: kstar(rows, R) for R in [10, 100, 1e3, 1e4]}
        print(f" alpha={alpha} span={span:>8.0e}: excess% K1..4 = {np.round(np.array(eps)*100,3)}  K*(R=10,1e2,1e3,1e4)={list(ks.values())}")
        tab.append(dict(alpha=alpha, span=span, eps=eps, kstar=ks, taus4=rows[3]['taus']))
out['scalefree'] = tab

print("\n== Exp3 (B): spacing of optimal stores, scale-free band; log10 ratios of consecutive store taus ==")
for t in tab:
    if t['span'] >= 1e3:
        lr = np.diff(np.log10(t['taus4']))
        print(f" alpha={t['alpha']} span={t['span']:.0e}: taus={np.round(t['taus4'],2)} log10 ratios={np.round(lr,2)}")

print("\n== Exp4: noise moves the effective span: alpha=1, span 1e4, noise crossover at tau_c ==")
a, v = scalefree_world(1.0, 1e4)
for frac in [1.0, 1e-2*0+30, 1e3]:
    N = noise_at_fast_edge(a, v, frac)
    ei, rows = profile(a, v, N, 3)
    print(f" noise x{frac:g} of fast-edge S: excess% K1..3 = {np.round([r['eps']*100 for r in rows],3)}  taus(K=3)={np.round(rows[2]['taus'],1)}")
json.dump(out, open('experiments.json', 'w'), indent=1, default=float)
