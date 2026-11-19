#!/usr/bin/env python3
"""Independent review checks for PR #91 (REACH notes). Written by the independent reviewer, not the author.
Run: nice -n 19 python3 independent_review_checks.py > independent_review_checks.out
(A) Pooling algebra re-derived symbolically, and generalised to partial sharing with T3a's own rho = q_g/q_u:
    flat:   N*sqrt(2 c w (q_g+q_u));   hybrid: sqrt(2 (c+N d) N w q_g) + N*sqrt(2 c w q_u)   (+ N w q_g l for staleness l)
    claim:  hybrid beats flat at l = 0 iff d/c < 1/N*(rho) - 1/N, N*(rho) = (sqrt(1+rho)+1)^2/rho  (T3a recovered at d = 0;
            WORMHOLES' rule d/c < 1 - 1/N recovered as rho -> infinity, i.e. q_u = 0).
(B) Multi-hop ('tube map') shortcut networks: finite throats of reach Lam, hop latency tau, light-speed transfers.
    claim:  latency grows linearly with distance at slope >= tau/Lam, so LAT-1 survives with c replaced by v_eff <= Lam/tau;
            unlimited-reach throats (or tau = 0 on a percolating throat graph) remove the distance limit.
(C) Circle map: the p/q tongue width scales like K^q at small K, so 'width proportional to K' holds only for q = 1.
(D) Coutinho-style nearest-neighbour (M3) in-degree for Poisson vs clustered points at matched mean degree.
"""
import numpy as np, sympy as sp, networkx as nx
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra, csgraph_from_dense
from scipy.optimize import minimize_scalar
rng = np.random.default_rng(42)

print("(A) pooling algebra")
c, d, w, qg, qu, N, l = sp.symbols('c d w q_g q_u N l', positive=True)
flat = N*sp.sqrt(2*c*w*(qg+qu)); hyb = sp.sqrt(2*(c+N*d)*N*w*qg) + N*sp.sqrt(2*c*w*qu)
# rho -> infinity (q_u = 0) and d general: central wins iff N^2 c > N (c + N d)  <=> d/c < 1 - 1/N
print("  q_u=0, l=0: flat^2 - central^2 =", sp.factor(sp.expand(flat.subs(qu, 0)**2 - hyb.subs(qu, 0)**2)))
# latency threshold at q_u = 0
lc = sp.simplify((flat.subs(qu, 0) - hyb.subs(qu, 0)) / (N*w*qg)); Tstar = sp.sqrt(2*c/(w*qg))
print("  q_u=0: l_crit / T*_local =", sp.simplify(lc/Tstar), " (expect 1 - sqrt((1+N d/c)/N))")
def check_general(Nv, rho, dc):
    cv, wv, quv = 1.0, 1.0, 1.0; qgv = rho*quv
    f = Nv*np.sqrt(2*cv*wv*(qgv+quv))
    g = lambda T: (cv+Nv*dc*cv)/T + Nv*wv*qgv*T/2           # shared component, brute force over T
    h = lambda T: cv/T + wv*quv*T/2                        # each residual, brute force
    Tg = minimize_scalar(g, bounds=(1e-6, 1e4), method='bounded').x
    Th = minimize_scalar(h, bounds=(1e-6, 1e4), method='bounded').x
    hy = g(Tg) + Nv*h(Th)
    Nstar = (np.sqrt(1+rho)+1)**2/rho
    return hy < f, dc < 1/Nstar - 1/Nv, Nstar
agree = tot = 0
for Nv in (2, 4, 8, 16, 50, 200):
    for rho in (0.1, 0.5, 1, 4, 100):
        for dc in (0, 0.001, 0.01, 0.05, 0.2, 0.5):
            a, b, _ = check_general(Nv, rho, dc); tot += 1; agree += (a == b)
print("  partial sharing: brute force vs 'd/c < 1/N*(rho) - 1/N' agree in %d/%d cases" % (agree, tot))
print("  at d=0 this is N > N*(rho) = (sqrt(1+rho)+1)^2/rho, i.e. T3a; e.g. N*(1) = %.3f, N*(0.1) = %.1f" % ((np.sqrt(2)+1)**2, (np.sqrt(1.1)+1)**2/0.1))
print("  NOTE: WORMHOLES' 'fully shared drift (rho = 1)' is T3a's rho -> infinity (q_u = 0), not T3a's rho = 1.")

print("\n(B) multi-hop shortcut networks (c = 1); centre at the origin corner of a box of side 10; mouths Poisson, density 2")
def tube(Lam, tau, box=10.0, nu=2.0, Rt=1.5, ntarg=3000):
    n = rng.poisson(nu*box**3); M = rng.random((n, 3))*box
    P = np.vstack([np.zeros((1, 3)), M]); t = cKDTree(P)
    W = np.full((n+1, n+1), np.inf)                       # dense weights; duplicate edges keep the MINIMUM
    for i, j in t.query_pairs(Rt):                         # light-speed transfers between nearby points
        dd = np.linalg.norm(P[i]-P[j]); W[i, j] = W[j, i] = min(W[i, j], dd)
    if np.isfinite(Lam):
        for i, j in t.query_pairs(Lam):                    # throats: any two mouths within Lam, latency tau
            if i == 0 or j == 0: continue
            W[i, j] = W[j, i] = min(W[i, j], tau + 1e-12)
        lat = dijkstra(csgraph_from_dense(W, null_value=np.inf), directed=True, indices=0)
    else:                                                  # open: every mouth linked to every other by one throat
        walk = dijkstra(csgraph_from_dense(W, null_value=np.inf), directed=True, indices=0)
        lat = np.minimum(walk, walk[1:].min() + tau); lat[0] = 0.0
    T = rng.random((ntarg, 3))*box; dist = np.linalg.norm(T, axis=1)
    dm, im = t.query(T, k=16); L = np.min(lat[im] + dm, axis=1); L = np.minimum(L, dist)
    sel = (dist > 3) & (dist < 9.5)
    slope = np.polyfit(dist[sel], L[sel], 1)[0]
    return slope, np.median(L[sel])
print("  %-28s %10s %14s %12s" % ("case", "slope", "pred tau/Lam", "median lat"))
for name, Lam, tau in [("no throats (light only)", 0.0, 0.0), ("finite Lam=1, tau=0.1", 1.0, 0.1), ("finite Lam=1, tau=0.3", 1.0, 0.3),
                       ("finite Lam=2, tau=0.1", 2.0, 0.1), ("finite Lam=1, tau=0 (percolating)", 1.0, 0.0), ("open (any-to-any), tau=0.1", np.inf, 0.1)]:
    if Lam == 0.0:
        s, m = tube(1e-9, 0.0)
    else:
        s, m = tube(Lam, tau)
    pred = "light: 1" if Lam == 0.0 else ("0" if (not np.isfinite(Lam) or tau == 0) else "%.3f" % (tau/Lam))
    print("  %-28s %10.3f %14s %12.3f" % (name, s, pred, m))
print("  Reading: finite throats with tau > 0 act as a faster medium (slope >= tau/Lam, approached as mouths get dense; v_eff <= Lam/tau);")
print("  LAT-1 then holds with c -> v_eff. Open throats, or tau = 0 on a percolating throat graph, give slope ~ 0: no distance limit.")

print("\n(C) circle-map tongue widths at small K (width of the plateau at rotation number p/q)")
def rot(Om, K, ntr=3000, n=6000):
    th = np.zeros_like(Om)
    for _ in range(ntr): th = th + Om - K/(2*np.pi)*np.sin(2*np.pi*th)
    s = np.zeros_like(Om); x = th.copy()
    for _ in range(n):
        st = Om - K/(2*np.pi)*np.sin(2*np.pi*x); x = x + st; s += st
    return s/n
for p, q in ((1, 2), (1, 3)):
    ws = []
    for K in (0.2, 0.4, 0.8):
        Om = np.linspace(p/q - 0.03, p/q + 0.03, 6001)
        r = rot(Om, K); wdt = (np.abs(r - p/q) < 1e-5).sum()*(Om[1]-Om[0]); ws.append(wdt)
    e1 = np.log(ws[1]/ws[0])/np.log(2); e2 = np.log(ws[2]/ws[1])/np.log(2)
    print("  %d:%d tongue width at K = 0.2, 0.4, 0.8: %.2e %.2e %.2e; local exponent %.2f, %.2f (expect -> %d at small K)" % (p, q, *ws, e1, e2, q))

print("\n(D) nearest-neighbour (M3-style) in-degree, Poisson vs clustered points, periodic cube, N = 6000")
def nscott(n, npar, s):
    par = rng.random((npar, 3)); idx = rng.integers(0, npar, n); return (par[idx] + rng.normal(0, s, (n, 3))) % 1.0
for name, P in [("Poisson", rng.random((6000, 3))), ("Neyman-Scott 300 parents s=0.03", nscott(6000, 300, 0.03)), ("Neyman-Scott 60 parents s=0.02", nscott(6000, 60, 0.02))]:
    t = cKDTree(P, boxsize=1.0); out = []
    for k in (1, 4, 20):
        _, nb = t.query(P, k+1); ind = np.bincount(nb[:, 1:].ravel(), minlength=len(P)); out.append("k=%d var/mean %.2f max %d" % (k, ind.var()/ind.mean(), ind.max()))
    print("  %-32s %s" % (name, " | ".join(out)))
print("  Reading: random points give in-degree narrower than Poisson (Coutinho's analytic 0.709 at <k> = 1 is for RANDOM points);")
print("  clustering of the point set broadens it, as Coutinho Fig. 4(a) shows for the real web at <k> = 20. Broader than Poisson is not a hub tail.")
