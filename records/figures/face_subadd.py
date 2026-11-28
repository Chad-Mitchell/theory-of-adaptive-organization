"""Which model classes satisfy SUBADDITIVITY (G_B <= G_L + G_S, i.e. kappa <= 1), the named condition of the map theorem (THEORY B.11)?
   nice -n 19 python3 figures/face_subadd.py [M]        writes figures/face_subadd.json  (about 5-10 minutes)
Gains are optimized robustly: a log-grid over store rates, then Nelder-Mead polish (G_L, G_S: 1 rate; G_B: 2 rates).  Families:
  base    one OU component, own read channel, independent unit noise, reading unpriced (the theory's separate-channel class)
  base*   the same, ADVERSARIAL: Nelder-Mead maximizes the excess G_B - G_L - G_S over (N, rho, n, delay) from many starts
  cnoise  base + read noise common to all units (density Nc)
  scales  two components on ONE read stream: a common part and an idiosyncratic part at different rates (rho = 1 and 0)
  priced  reading priced (face_collapse_v1b.json, net worths): counted from that file
An excess counts only if > 1e-5 of the variance (optimizer noise is about 1e-7 here)."""
import os, sys, json, time
import numpy as np
from multiprocessing import Pool
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from face_hybrid import mse_fast
TOL = 1e-5

def gains(a, v, N, n, rho, lead, Nc=0.0):
    a = np.asarray(a, float); v = np.asarray(v, float); rho = np.asarray(rho, float); V = v.sum()
    f = lambda bl, bc: mse_fast(a, v, N, n, rho, lead, bl, bc, Nc)
    lo, hi = np.log(a.min()) - 4, np.log(a.max()) + 8
    g1 = np.linspace(lo, hi, 241)
    def one(kind):
        h = (lambda x: f([np.exp(x)], [])) if kind == 'L' else (lambda x: f([], [np.exp(x)]))
        i = int(np.argmin([h(x) for x in g1]))
        r = minimize(lambda z: h(z[0]), [g1[i]], method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-15))
        return min(r.fun, h(g1[i]))
    eL, eS = one('L'), one('S')
    g2 = np.linspace(lo, hi, 61)
    E = np.array([[f([np.exp(x)], [np.exp(y)]) for y in g2] for x in g2]); i, j = np.unravel_index(E.argmin(), E.shape)
    r = minimize(lambda z: f([np.exp(z[0])], [np.exp(z[1])]), [g2[i], g2[j]], method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-15))
    eB = min(r.fun, E[i, j], eL, eS)
    return V - eL, V - eS, V - eB, V

def world(seed):
    r = np.random.default_rng(70_000 + seed); fam = ['base', 'cnoise', 'scales'][seed % 3]
    N = 10 ** r.uniform(-3, 2); n = int(round(10 ** r.uniform(0.3, 3.5))); lead = 10 ** r.uniform(-3, 1.3)
    if fam == 'base': return fam, dict(a=[1.0], v=[1.0], N=N, n=n, rho=[r.uniform()], lead=lead, Nc=0.0)
    if fam == 'cnoise': return fam, dict(a=[1.0], v=[1.0], N=N, n=n, rho=[r.uniform()], lead=lead, Nc=10 ** r.uniform(-3, 1) * N)
    vc = r.uniform(0.05, 0.95)
    return fam, dict(a=[1.0, 10 ** r.uniform(-4, 4)], v=[vc, 1 - vc], N=N, n=n, rho=[1.0, 0.0], lead=lead, Nc=0.0)

def job(seed):
    fam, p = world(seed)
    GL, GS, GB, V = gains(**p)
    return dict(seed=seed, fam=fam, **{k: (list(map(float, x)) if isinstance(x, list) else float(x)) for k, x in p.items()},
                GL=float(GL), GS=float(GS), GB=float(GB), excess=float((GB - GL - GS) / V))

def adversary(seed):
    """Maximize the excess in the base class from a random start (parameters: log N, logit rho, log n, log delay)."""
    r = np.random.default_rng(80_000 + seed)
    def neg(z):
        N, rho, n, lead = np.exp(z[0]), 1 / (1 + np.exp(-z[1])), 1 + np.exp(z[2]), np.exp(z[3])
        GL, GS, GB, V = gains([1.0], [1.0], N, n, [rho], lead)
        return -(GB - GL - GS)
    z0 = np.array([r.uniform(-7, 4), r.uniform(-4, 4), r.uniform(0, 8), r.uniform(-7, 3)])
    res = minimize(neg, z0, method='Nelder-Mead', options=dict(maxiter=120, xatol=1e-3, fatol=1e-10))
    return dict(seed=seed, z=res.x.tolist(), excess=float(-res.fun))

if __name__ == '__main__':
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 600; t0 = time.time()
    with Pool(5) as pool:
        res = pool.map(job, range(M)); adv = pool.map(adversary, range(20))
    v1b = json.load(open(os.path.join(HERE, 'face_collapse_v1b.json')))['worlds']
    sup = [w for w in v1b if w['kS'] > 1 + 1e-6 or w['kL'] > 1 + 1e-6]
    import face_map as fm
    off = [w for w in v1b if fm.quadrant(w['XL'], w['XS']) < 3 and int(fm.quadrant(w['XL'], w['XS'])) != w['brute']]
    S = {}
    for fam in ('base', 'cnoise', 'scales'):
        rs = [x for x in res if x['fam'] == fam]
        S[fam] = dict(worlds=len(rs), superadditive=int(sum(x['excess'] > TOL for x in rs)), max_excess=float(max(x['excess'] for x in rs)))
    S['base_adversarial'] = dict(starts=len(adv), max_excess=float(max(x['excess'] for x in adv)))
    S['priced_v1b'] = dict(worlds=len(v1b), superadditive=len(sup), max_kL=float(max(w['kL'] for w in v1b)), max_kS=float(max(w['kS'] for w in v1b)),
                           quadrant_wrong=len(off))
    S['secs'] = time.time() - t0
    print(json.dumps(S, indent=1)); json.dump(dict(summary=S, worlds=res, adversary=adv), open(os.path.join(HERE, 'face_subadd.json'), 'w'))
