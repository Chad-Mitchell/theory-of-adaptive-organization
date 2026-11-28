"""Search for violations of the N60(ii) premise (eps_K convex and decreasing in K) in Model S.
World: sum of J OU modes (rates a_j, variances v_j), white read noise N; K first-order stores (stores.py).
eps_K = E_K/E_inf - 1.  Then compare K* = argmin_{K>=1} [K + R(1+eps_K)] with 1 + #{k>=2: R(eps_{k-1}-eps_k) > 1}.
Run: nice -n 19 python3 convexity_search.py  (seeds fixed)."""
import numpy as np, json, sys
from multiprocessing import Pool
from stores import E_K, E_inf

KMAX = 5
def eps_seq(a, v, N, starts=10):
    ei = E_inf(a, v, N)
    rng = np.random.default_rng(7)
    E = [E_K(a, v, N, K, starts=starts, rng=rng)[0] for K in range(1, KMAX+1)]
    # enforce monotone by optimizer (K+1 stores can mimic K): take running min
    E = list(np.minimum.accumulate(E))
    return ei, [e/ei - 1 for e in E]

def world(seed):
    rng = np.random.default_rng(seed)
    J = int(rng.integers(2, 5))
    taus = np.sort(10**rng.uniform(0, 4, J))
    v = 10**rng.uniform(-2, 1, J)
    N = 10**rng.uniform(-3, 0)
    return 1/taus, v, N

def run(seed):
    a, v, N = world(seed)
    ei, eps = eps_seq(a, v, N)
    d = np.diff(eps)            # eps_{k+1}-eps_k (<=0)
    dec = -d                    # decrements
    nonconvex = [k+1 for k in range(len(dec)-1) if dec[k+1] > dec[k]*(1+1e-3) + 1e-6]
    return dict(seed=seed, taus=list(1/a), v=list(v), N=N, eps=eps, dec=list(dec), nonconvex_at=nonconvex)

def formula_vs_argmin(eps, R):
    Ks = np.arange(1, len(eps)+1)
    J = Ks + R*(1+np.array(eps))
    kstar = int(Ks[np.argmin(J)])
    cnt = 1 + sum(1 for k in range(2, len(eps)+1) if R*(eps[k-2]-eps[k-1]) > 1)
    return kstar, cnt

if __name__ == '__main__':
    seeds = list(range(int(sys.argv[1]) if len(sys.argv) > 1 else 120))
    with Pool(6) as p:
        out = p.map(run, seeds)
    Rs = np.logspace(0, 7, 141)
    for o in out:
        mism = []
        for R in Rs:
            ks, c = formula_vs_argmin(o['eps'], R)
            if ks != c: mism.append((float(R), ks, c))
        o['mismatch'] = mism
    nc = [o for o in out if o['nonconvex_at']]
    mm = [o for o in out if o['mismatch']]
    print(f"worlds {len(out)}; nonconvex eps: {len(nc)}; formula != argmin at some R: {len(mm)}")
    for o in mm[:10]:
        print(o['seed'], 'taus', np.round(o['taus'],2), 'v', np.round(o['v'],3), 'N', round(o['N'],4))
        print('   eps', np.round(o['eps'],4), 'dec', np.round(o['dec'],4), 'mismatch R range', o['mismatch'][0][0], o['mismatch'][-1][0], o['mismatch'][0][1:])
    json.dump(out, open('convexity_search.json', 'w'), indent=1)
