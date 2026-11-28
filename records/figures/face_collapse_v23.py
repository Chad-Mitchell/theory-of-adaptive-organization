"""V2 and V3: what changes when a world's components reach the system through ONE read stream (THEORY L2's class), not separate channels.
   nice -n 19 python3 figures/face_collapse_v23.py [M2] [M3]          writes face_collapse_v23.json
V2 (layer count, one unit, lead 0): for random real-pole worlds (2-5 components, random spacing and variances, random noise), compute
   E_K for K = 0..J (first-order stores, rates optimized; E_J exact) and test whether the marginal gains E_{k-1} - E_k fall with k
   (diminishing returns).  Where they do, the best layer count is exactly #{k : w (E_{k-1} - E_k) > h} for every w/h: each added layer
   is one point on the map's x axis (X = its marginal stakes over its upkeep), and the k -> k+1 boundary is X = 1 in every world.
V3 (local vs shared, n units, delay): two-component worlds (fast and slow; v2.5.1: the shared fraction rho is drawn PER COMPONENT in half
   the worlds, rho = 1 in the other half, so common and idiosyncratic parts can sit at different rates -- review 26's case), the exact cheapest design over
   (local stores, shared stores) in {0,1,2}^2 (face_hybrid.py) against two readings of the map: (a) per component, each treated as if read
   on its own channel (fast: noise N; slow: noise N + 2 v_fast/a_fast, the fast component's low-frequency power); (b) layer by layer, each
   candidate layer (local or shared) placed by its MARGINAL stakes over upkeep given the layers already built (greedy); (c) greedy with a
   pairwise look-ahead: when no single addition pays, add the best PAIR if it pays.  Greedy is exact when marginal values are submodular;
   joint-only value (a shared store paying only as a common-mode reference for local ones) breaks it.
V2 rejects numerically broken optimizer results (negative or non-finite E) and reports them as failures (v2.5.1; seed 139 was one)."""
import os, sys, json, time
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'theory', 'layers_checks'))
import face_map as fm
from face_hybrid import best_fast as best
from stores import E_K as storeE
from lead import E_opt

def v2_job(seed):
    r = np.random.default_rng(10_000 + seed)
    J = int(r.integers(2, 6)); gaps = r.uniform(0.3, 3.0, J - 1)
    tau = 10 ** np.concatenate([[0.0], np.cumsum(gaps)]); a = 1 / tau
    v = r.dirichlet(np.ones(J)); N = 10 ** r.uniform(-4, 0.5)
    E = [1.0]; failed = False
    for K in range(1, J):
        e = storeE(a, v, N, K, starts=10, rng=np.random.default_rng(seed))[0]
        if not (np.isfinite(e) and e >= 0): e = storeE(a, v, N, K, starts=30, rng=np.random.default_rng(seed + 1))[0]
        if not (np.isfinite(e) and e >= 0): failed = True; e = E[-1]
        E.append(min(e, E[-1]))
    eo = E_opt(a, v, N, 0.0)
    if not (np.isfinite(eo) and eo >= 0): failed = True; eo = E[-1]
    E.append(min(eo, E[-1]))
    d = -np.diff(E)
    convex = bool(np.all(d[1:] <= d[:-1] * (1 + 1e-6) + 1e-12))
    convex_tol = bool(np.all(np.isfinite(d)) and np.all(d[1:] <= d[:-1] + 1e-5))     # within the optimizer's tolerance (1e-5 of Var)
    return dict(seed=seed, J=J, failed=failed, convex_tol=convex_tol, tau=tau.tolist(), v=v.tolist(), N=N, E=E, dE=d.tolist(), convex=convex, min_gap=float(gaps.min()))

def v3_world(seed):
    r = np.random.default_rng(20_000 + seed)
    sep = 10 ** r.uniform(1, 4); a = np.array([1.0, 1 / sep]); v = r.dirichlet(np.ones(2))
    N = 10 ** r.uniform(-3, 1); n = int(round(10 ** r.uniform(0.5, 2.5))); lead = 10 ** r.uniform(-1, 1) * np.sqrt(sep)
    wu = 10 ** r.uniform(0, 4); hc = 10 ** r.uniform(-0.5, 2)
    rho = r.uniform(0, 1, 2) if seed % 2 else np.ones(2)
    return a, v, N, n, lead, wu, 1.0, hc, sep, rho

def v3_job(seed):
    a, v, N, n, lead, wu, hl, hc, sep, rho = v3_world(seed)
    E = {}
    for kl in range(3):
        for kc in range(3):
            E[(kl, kc)] = v.sum() if kl + kc == 0 else best(a, v, N, n, rho, lead, kl, kc, starts=4, seed=seed)[0]
    for kl in range(3):                           # adding a store can be given zero weight: enforce monotone E (removes optimizer misses)
        for kc in range(3):
            for m in ((kl - 1, kc), (kl, kc - 1)):
                if min(m) >= 0: E[(kl, kc)] = min(E[(kl, kc)], E[m])
    costs = {k: n * hl * k[0] + hc * k[1] + n * wu * e for k, e in E.items()}
    ex = min(costs, key=costs.get)
    # per-component reading (each component as if on its own channel)
    pred = [0, 0]; comp = []
    Neff = [N, N + 2 * v[0] / a[0]]
    for j in range(2):
        GL, GS, pi = fm.gains_ou(v[j], a[j], Neff[j], n, rho[j], lead)
        eB = best([a[j]], [v[j]], Neff[j], n, rho[j], lead, 1, 1, starts=2, seed=seed)[0]
        GB = max(v[j] - eB, GL, GS); kS = (GB - GL) / GS if GS > 0 else 0.0; kL = (GB - GS) / GL
        XL = wu * GL / hl; XS = n * wu * GS / hc; nu = n * hl / hc
        d = int(fm.decide(XL, XS, nu, kL, kS)); comp.append(dict(XL=float(XL), XS=float(XS), nu=nu, d=d))
        if d in (1, 3): pred[0] += 1
        if d in (2, 3): pred[1] += 1
    pc = costs[tuple(pred)]
    g = (0, 0)                                    # layer by layer: add the local or shared store with the largest marginal value while it pays
    while True:
        nxt = [m for m in ((g[0] + 1, g[1]), (g[0], g[1] + 1)) if m in costs and costs[m] < costs[g]]
        if not nxt: break
        g = min(nxt, key=costs.get)
    p = (0, 0)                                    # greedy with a pairwise look-ahead
    while True:
        nxt = [m for m in ((p[0] + 1, p[1]), (p[0], p[1] + 1)) if m in costs and costs[m] < costs[p]]
        if not nxt: nxt = [m for m in ((p[0] + 2, p[1]), (p[0] + 1, p[1] + 1), (p[0], p[1] + 2)) if m in costs and costs[m] < costs[p]]
        if not nxt: break
        p = min(nxt, key=costs.get)
    return dict(seed=seed, rho=rho.tolist(), pair=list(p), same_pair=list(ex) == list(p), regret_pair=float(costs[p] / costs[ex] - 1), greedy=list(g), same_greedy=list(ex) == list(g), regret_greedy=float(costs[g] / costs[ex] - 1), sep=float(sep), n=n, lead=float(lead), N=float(N), v=v.tolist(), exact=list(ex), pred=pred, comp=comp,
                regret=float(pc / costs[ex] - 1), same=list(ex) == pred, same_total=sum(ex) == sum(pred))

if __name__ == '__main__':
    M2 = int(sys.argv[1]) if len(sys.argv) > 1 else 200; M3 = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    t0 = time.time(); res = {}
    with Pool(5) as pool:
        res['v2'] = sorted(pool.map(v2_job, range(M2)), key=lambda x: x['seed']); print('v2 done', time.time() - t0, flush=True)
        res['v3'] = sorted(pool.map(v3_job, range(M3)), key=lambda x: x['seed']); print('v3 done', time.time() - t0, flush=True)
    ok2 = [x for x in res['v2'] if not x['failed']]
    v2c = np.mean([x['convex'] for x in ok2]); v2t = np.mean([x['convex_tol'] for x in ok2])
    V3 = res['v3']; sub = lambda f: [x for x in V3 if f(x)]
    def stats(rs):
        reg = np.array([x['regret'] for x in rs]); rg = np.array([x['regret_greedy'] for x in rs]); rp = np.array([x['regret_pair'] for x in rs])
        return dict(worlds=len(rs), percomp_same=float(np.mean([x['same'] for x in rs])), percomp_regret_p90=float(np.quantile(reg, 0.9)), percomp_regret_max=float(reg.max()),
                    greedy_same=float(np.mean([x['same_greedy'] for x in rs])), greedy_regret_p90=float(np.quantile(rg, 0.9)), greedy_regret_max=float(rg.max()),
                    greedy_misses=int(sum(not x['same_greedy'] for x in rs)),
                    pair_same=float(np.mean([x['same_pair'] for x in rs])), pair_regret_max=float(rp.max()), pair_misses=int(sum(not x['same_pair'] for x in rs)))
    res['summary'] = dict(M2=M2, v2_failed=int(sum(x['failed'] for x in res['v2'])), v2_convex=float(v2c), v2_convex_within_tol=float(v2t), M3=M3,
                          v3_all=stats(V3), v3_rho1=stats(sub(lambda x: min(x['rho']) == 1.0)), v3_rho_per_component=stats(sub(lambda x: min(x['rho']) < 1.0)),
                          secs=time.time() - t0)
    print(res['summary'])
    json.dump(res, open(os.path.join(HERE, 'face_collapse_v23.json'), 'w'))
