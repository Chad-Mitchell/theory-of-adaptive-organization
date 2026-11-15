"""Stage A: lone trackers learn (ES, realized payoffs only) on a stakes x drift grid; their realized
minimum cost is measured on fresh long paths; (a, b) = OLS elasticities of realized cost.
Usage: python run_lone.py OUT.json"""
import sys, json, os, numpy as np
from multiprocessing import Pool
import world as w

GRID = {'R': ([0.25, 1, 4, 16], [0.03, 0.1, 0.3, 1.0]),
        'A': ([1, 4, 16, 64, 256], [0.03, 0.1, 0.3, 1.0])}
SEEDS = 8

def realized(tech, eff, Wt, q, rng):
    if tech == 'R':
        L = 400000; T = int(eff)
        x = w.bm(rng, L + T, q)
        e, nr = w.r_errors(x, T, int(rng.integers(T)))
        return (w.C_R * nr + Wt * np.dot(e, e)) / e.shape[0]
    L = 200000
    x = w.bm(rng, L, q)
    e, al = w.a_errors(x, eff, rng, L // 4)
    return w.C_A * eff + Wt * np.dot(e, e) / e.shape[0]

def job(args):
    tech, Wt, q, seed = args
    rng = np.random.default_rng([7, seed, int(Wt * 100), int(q * 1000), tech == 'A'])
    eff = w.es_learn(tech, Wt, q, rng)
    return dict(tech=tech, W=Wt, q=q, seed=seed, effort=float(eff), cost=float(realized(tech, eff, Wt, q, rng)))

if __name__ == '__main__':
    os.nice(19)
    jobs = [(t, Wt, q, s) for t, (Ws, qs) in GRID.items() for Wt in Ws for q in qs for s in range(SEEDS)]
    with Pool(int(os.environ.get('NPROC', '3'))) as p:
        res = p.map(job, jobs, chunksize=4)
    out = {'rows': res}
    for tech in GRID:
        r = [x for x in res if x['tech'] == tech]
        X = np.column_stack([np.ones(len(r)), np.log([x['W'] for x in r]), np.log([x['q'] for x in r])])
        y = np.log([x['cost'] for x in r])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        # seed-cluster bootstrap
        bs = []; rng = np.random.default_rng(99)
        seeds = np.array([x['seed'] for x in r])
        for _ in range(2000):
            pick = rng.integers(SEEDS, size=SEEDS)
            idx = np.concatenate([np.where(seeds == s)[0] for s in pick])
            b, *_ = np.linalg.lstsq(X[idx], y[idx], rcond=None); bs.append(b)
        bs = np.array(bs)
        a, b = beta[1], beta[2]
        out[tech] = dict(a=float(a), b=float(b), a_ci=np.percentile(bs[:, 1], [2.5, 97.5]).tolist(),
                         b_ci=np.percentile(bs[:, 2], [2.5, 97.5]).tolist(), e_g_measured=float(-(1 - b) / (1 - a)))
    out['mixed'] = {'AR_e_g': -(1 - out['A']['b']) / (1 - out['A']['a']), 'RA_e_g': -(1 - out['R']['b']) / (1 - out['R']['a'])}
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'rows'}, indent=1))
