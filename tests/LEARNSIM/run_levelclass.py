"""PREREG_2 inputs (no onset outcome used):
 (1) LEVEL class measured on the level alone: a tracker of the shared driver learns (ES, realized payoffs only)
     at level-like stakes W (= N) and drift q (= q_g); class = elasticities of LEARNED EFFORT on W and q
     (primary, framework 3.4) and of realized cost (convergent, MV5).
 (2) MEMBER class: effort elasticities of the Stage A lone members (MEASURED_AB.json rows), plus their cost elasticities.
 (3) Selection resolution eps_hat (framework 3.10) from dispersion of learned member efforts in Stage A.
Usage: python run_levelclass.py LEVEL_CLASS.json"""
import sys, json, os, numpy as np
from multiprocessing import Pool
import world as w
from run_lone import realized

GRID = {'R': ([16, 64, 256, 1024], [0.01, 0.04, 0.16]), 'A': ([300, 3000, 30000, 300000], [0.01, 0.04, 0.16])}
SEEDS = 8

def eff_of(tech, e): return 1.0 / e if tech == 'R' else e

def job(a):
    tech, Wt, q, s = a
    rng = np.random.default_rng([21, s, int(Wt), int(q * 1000), tech == 'A'])
    e = w.es_learn(tech, Wt, q, rng)
    return dict(tech=tech, W=Wt, q=q, seed=s, effort=float(e), cost=float(realized(tech, e, Wt, q, rng)))

def fit(rows, ykey, tech):
    X = np.column_stack([np.ones(len(rows)), np.log([r['W'] for r in rows]), np.log([r['q'] for r in rows])])
    y = np.log([eff_of(tech, r['effort']) if ykey == 'effort' else r['cost'] for r in rows])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    seeds = np.array([r['seed'] for r in rows]); S = sorted(set(seeds)); rng = np.random.default_rng(5); bs = []
    for _ in range(2000):
        pick = rng.choice(S, size=len(S)); idx = np.concatenate([np.where(seeds == s)[0] for s in pick])
        b, *_ = np.linalg.lstsq(X[idx], y[idx], rcond=None); bs.append(b)
    bs = np.array(bs); resid = y - X @ beta
    return dict(a=float(beta[1]), b=float(beta[2]), a_se=float(bs[:, 1].std()), b_se=float(bs[:, 2].std()),
                a_ci=np.percentile(bs[:, 1], [2.5, 97.5]).tolist(), b_ci=np.percentile(bs[:, 2], [2.5, 97.5]).tolist(),
                resid_sd=float(resid.std()))

if __name__ == '__main__':
    os.nice(19)
    jobs = [(t, Wt, q, s) for t, (Ws, qs) in GRID.items() for Wt in Ws for q in qs for s in range(SEEDS)]
    with Pool(3) as p: rows = p.map(job, jobs, chunksize=4)
    out = {'level_rows': rows, 'level': {}, 'member': {}}
    for t in GRID:
        rr = [r for r in rows if r['tech'] == t]
        out['level'][t] = {'effort_elasticities': fit(rr, 'effort', t), 'cost_elasticities': fit(rr, 'cost', t)}
    MAB = json.load(open('MEASURED_AB.json'))
    for t in ['R', 'A']:
        rr = [r for r in MAB['rows'] if r['tech'] == t]
        fe = fit(rr, 'effort', t)
        # eps_hat: median |ln effort residual| -> cost loss of a mis-set effort, (k + 1/k)/2 - 1 with k = exp(|dev|)
        X = np.column_stack([np.ones(len(rr)), np.log([r['W'] for r in rr]), np.log([r['q'] for r in rr])])
        y = np.log([eff_of(t, r['effort']) for r in rr]); beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        md = float(np.median(np.abs(y - X @ beta)))
        out['member'][t] = {'effort_elasticities': fe, 'cost_elasticities': {'a': MAB[t]['a'], 'b': MAB[t]['b']},
                            'median_abs_dev_ln_effort': md, 'eps_hat': float(np.cosh(md) - 1)}
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'level_rows'}, indent=1))
