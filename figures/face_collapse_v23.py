"""V2 and V3: what changes when a world's components reach the system through ONE read stream (THEORY L2's class), not separate channels.
   nice -n 19 python3 figures/face_collapse_v23.py [M2] [M3]          writes face_collapse_v23.json
V2 (layer count, one unit, lead 0): for random real-pole worlds (2-5 components, random spacing and variances, random noise), compute
   E_K for K = 0..J (first-order stores, rates optimized; E_J exact) and test whether the marginal gains E_{k-1} - E_k fall with k
   (diminishing returns).  Where they do, the best layer count is exactly #{k : w (E_{k-1} - E_k) > h} for every w/h: each added layer
   is one point on the map's x axis (X = its marginal stakes over its upkeep), and the k -> k+1 boundary is X = 1 in every world.
V3 (local vs shared, n units, delay): two-component worlds (fast and slow, fully shared driver), the exact cheapest design over
   (local stores, shared stores) in {0,1,2}^2 (face_hybrid.py) against two readings of the map: (a) per component, each treated as if read
   on its own channel (fast: noise N; slow: noise N + 2 v_fast/a_fast, the fast component's low-frequency power); (b) layer by layer, each
   candidate layer (local or shared) placed by its MARGINAL stakes over upkeep given the layers already built (greedy)."""
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
    E = [1.0]
    for K in range(1, J):
        E.append(min(storeE(a, v, N, K, starts=10, rng=np.random.default_rng(seed))[0], E[-1]))
    E.append(min(E_opt(a, v, N, 0.0), E[-1]))
    d = -np.diff(E)
    convex = bool(np.all(d[1:] <= d[:-1] * (1 + 1e-6) + 1e-12))
    convex_tol = bool(np.all(np.isfinite(d)) and np.all(d[1:] <= d[:-1] + 1e-5))     # within the optimizer's tolerance (1e-5 of Var)
    return dict(seed=seed, J=J, convex_tol=convex_tol, tau=tau.tolist(), v=v.tolist(), N=N, E=E, dE=d.tolist(), convex=convex, min_gap=float(gaps.min()))

def v3_world(seed):
    r = np.random.default_rng(20_000 + seed)
    sep = 10 ** r.uniform(1, 4); a = np.array([1.0, 1 / sep]); v = r.dirichlet(np.ones(2))
    N = 10 ** r.uniform(-3, 1); n = int(round(10 ** r.uniform(0.5, 2.5))); lead = 10 ** r.uniform(-1, 1) * np.sqrt(sep)
    wu = 10 ** r.uniform(0, 4); hc = 10 ** r.uniform(-0.5, 2)
    return a, v, N, n, lead, wu, 1.0, hc, sep

def v3_job(seed):
    a, v, N, n, lead, wu, hl, hc, sep = v3_world(seed)
    costs = {}
    for kl in range(3):
        for kc in range(3):
            if kl + kc == 0: e = v.sum()
            else: e = best(a, v, N, n, 1.0, lead, kl, kc, starts=3, seed=seed)[0]
            costs[(kl, kc)] = n * hl * kl + hc * kc + n * wu * e
    ex = min(costs, key=costs.get)
    # per-component reading (each component as if on its own channel)
    pred = [0, 0]; comp = []
    Neff = [N, N + 2 * v[0] / a[0]]
    for j in range(2):
        GL, GS, pi = fm.gains_ou(v[j], a[j], Neff[j], n, 1.0, lead)
        eB = best([a[j]], [v[j]], Neff[j], n, 1.0, lead, 1, 1, starts=2, seed=seed)[0]
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
    return dict(seed=seed, greedy=list(g), same_greedy=list(ex) == list(g), regret_greedy=float(costs[g] / costs[ex] - 1), sep=float(sep), n=n, lead=float(lead), N=float(N), v=v.tolist(), exact=list(ex), pred=pred, comp=comp,
                regret=float(pc / costs[ex] - 1), same=list(ex) == pred, same_total=sum(ex) == sum(pred))

if __name__ == '__main__':
    M2 = int(sys.argv[1]) if len(sys.argv) > 1 else 200; M3 = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    t0 = time.time(); res = {}
    with Pool(5) as pool:
        res['v2'] = sorted(pool.map(v2_job, range(M2)), key=lambda x: x['seed']); print('v2 done', time.time() - t0, flush=True)
        res['v3'] = sorted(pool.map(v3_job, range(M3)), key=lambda x: x['seed']); print('v3 done', time.time() - t0, flush=True)
    v2c = np.mean([x['convex'] for x in res['v2']]); v2t = np.mean([x['convex_tol'] for x in res['v2']]); v3s = np.mean([x['same'] for x in res['v3']]); v3t = np.mean([x['same_total'] for x in res['v3']])
    reg = np.array([x['regret'] for x in res['v3']])
    res['summary'] = dict(M2=M2, v2_convex=float(v2c), v2_convex_within_tol=float(v2t), M3=M3, v3_same=float(v3s), v3_same_total=float(v3t), v3_regret_median=float(np.median(reg)),
                          v3_regret_p90=float(np.quantile(reg, 0.9)), v3_regret_max=float(reg.max()), v3_greedy_same=float(np.mean([x['same_greedy'] for x in res['v3']])),
                          v3_greedy_regret_p90=float(np.quantile([x['regret_greedy'] for x in res['v3']], 0.9)), v3_greedy_regret_max=float(max(x['regret_greedy'] for x in res['v3'])), secs=time.time() - t0)
    print(res['summary'])
    json.dump(res, open(os.path.join(HERE, 'face_collapse_v23.json'), 'w'))
