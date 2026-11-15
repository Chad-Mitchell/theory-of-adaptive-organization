"""Object under test: the locked premise test (measurement/estimators/aqn.py premise_test, B = 39) and the
FRAMEWORK §3.1 step-4 kurtosis screen, on worlds the locked validation did not include.
Worlds simulated with this file's own code: W Gaussian random walk; G Gaussian random walk with GARCH(1,1)
volatility (no jumps); J jump-diffusion random walk (Brownian + compound Poisson, jumps carry half the variance).
Small white sensing noise (5% of increment variance) in all. Kurtosis screen threshold = 95th percentile of
excess kurtosis under W (simulated here)."""
import numpy as np, sys, json
from multiprocessing import Pool
sys.path.insert(0, '../../../measurement/estimators')
import aqn
def world(kind, n, rng):
    if kind == 'W':
        d = rng.standard_normal(n)
    elif kind == 'G':
        om, al, be = 0.02, 0.08, 0.90; h = om/(1-al-be); d = np.empty(n); e = rng.standard_normal(n)
        for t in range(n):
            d[t] = np.sqrt(h)*e[t]; h = om + al*d[t]**2 + be*h
    else:  # J: lam 0.01/step, jump var 0.5/0.01 = 50 -> jumps carry half the per-step variance 1
        d = np.sqrt(0.5)*rng.standard_normal(n) + (rng.random(n) < 0.01)*rng.standard_normal(n)*np.sqrt(50.0)
    return np.cumsum(d) + rng.standard_normal(n)*np.sqrt(0.05)
def kurt(y):
    d = np.diff(y); d = d - d.mean(); return (d**4).mean()/(d**2).mean()**2 - 3
def one(a):
    kind, n, rep = a
    rng = np.random.default_rng(424242 + rep*101 + n + ord(kind))
    y = world(kind, n, rng)
    lr, p, h, o = aqn.premise_test(y, 39, np.random.default_rng(99 + rep))
    return [kind, n, rep, float(lr), float(p), float(kurt(y))]
if __name__ == '__main__':
    rng = np.random.default_rng(5); kw = np.array([kurt(world('W', 2048, rng)) for _ in range(2000)])
    thr = float(np.quantile(kw, 0.95))
    jobs = [(k, 2048, r) for k in 'WGJ' for r in range(24)]
    with Pool(3) as pl:
        out = pl.map(one, jobs, chunksize=2)
    json.dump({'thr': thr, 'out': out}, open('premise_scope.json', 'w'))
    print(f"kurtosis screen threshold (95% under W, n=2048): {thr:.3f}")
    for k in 'WGJ':
        s = [o for o in out if o[0] == k]
        print(f"world {k}: premise test reject (p<=0.05) {np.mean([o[4] <= 0.05 for o in s]):.2f}; median LR {np.median([o[3] for o in s]):.0f}; kurtosis flag {np.mean([o[5] > thr for o in s]):.2f}; median excess kurtosis {np.median([o[5] for o in s]):.2f}  (n=2048, {len(s)} series)")
