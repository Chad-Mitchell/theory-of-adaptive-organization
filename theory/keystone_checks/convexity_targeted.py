"""Targeted search for non-convex eps_K in Model S (sum of J OU modes + white read noise, K first-order stores).
For OU sums the causal Wiener filter has J real poles, so E_J = E_inf exactly; we use E_inf := min(E_J, YJ integral)
to remove quadrature error. A violation must exceed TOL in absolute eps.  Run: nice -n 19 python3 convexity_targeted.py N"""
import numpy as np, json, sys
from multiprocessing import Pool
from stores import E_K, E_inf
TOL = 1e-4

def world(seed):
    rng = np.random.default_rng(1000 + seed)
    J = int(rng.integers(3, 5))
    sep = 10**rng.uniform(0.5, 2.0, J-1)              # factor 3 to 100 between scales
    taus = np.cumprod(np.r_[10**rng.uniform(0, 1), sep])
    v = 10**rng.uniform(-1.5, 1.5, J)
    N = 10**rng.uniform(-2, 1)
    return 1/taus, v, N

def eps_of(a, v, N, starts=16):
    J = len(a); rng = np.random.default_rng(3)
    E = [E_K(a, v, N, K, starts=starts, rng=rng)[0] for K in range(1, J+1)]
    E = list(np.minimum.accumulate(E))
    Einf = min(E[-1], E_inf(a, v, N))
    return [e/Einf - 1 for e in E]

def run(seed):
    a, v, N = world(seed)
    eps = eps_of(a, v, N)
    dec = [eps[k]-eps[k+1] for k in range(len(eps)-1)]
    viol = [k for k in range(len(dec)-1) if dec[k+1] - dec[k] > TOL]
    return dict(seed=seed, taus=list(1/a), v=list(v), N=N, eps=eps, dec=dec, viol=viol)

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    with Pool(6) as p:
        out = p.map(run, range(n))
    viol = [o for o in out if o['viol']]
    r = [o['eps'][1]/o['eps'][0] for o in out if o['eps'][0] > 1e-3 and len(o['eps']) == 3]
    print(f"worlds {n}; non-convex beyond TOL: {len(viol)}; J=3 eps2/eps1 range {min(r):.3f}..{max(r):.3f} (convex iff <= 0.5)")
    print("eps_1 quantiles", np.round(np.quantile([o['eps'][0] for o in out],[.1,.5,.9]),4))
    for o in viol[:12]:
        print(o['seed'], 'taus', np.round(o['taus'],1), 'v', np.round(o['v'],3), 'N', round(o['N'],4), 'eps', np.round(o['eps'],4), 'dec', np.round(o['dec'],4))
    json.dump(out, open('convexity_targeted.json', 'w'), indent=1)
