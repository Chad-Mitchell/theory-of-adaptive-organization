"""Independent MC of the Whittle claims (own simulator + own estimator). Conditions mirror block A cells."""
import numpy as np, sys, json
from multiprocessing import Pool
sys.path.insert(0, '.')
from ownlib import fgn_dh, whittle
from scipy.special import gamma
CONDS = [(2.0, 0.5, 8192), (1.4, 0.5, 8192), (2.6, 0.05, 8192), (2.0, 0.05, 8192), (2.0, 0.05, 32768), (1.4, 0.05, 32768)]
REPS = 150
def one(args):
    a, wc, n, rep = args
    rng = np.random.default_rng(777000 + int(a*100)*1000 + int(wc*1000)*7 + n + rep*13)
    q = 1.0; s2 = q*wc**(-a)  # crossover wc = (q/s2)^(1/a)
    D1 = 1/(gamma(a)*np.sin(np.pi*(a-1)/2))
    x = np.cumsum(np.sqrt(q*D1)*fgn_dh(n, (a-1)/2, rng))
    y = x + rng.standard_normal(n)*np.sqrt(s2)
    r = whittle(y)
    return [a, wc, n, r['a'], r['se'][1], r['lq'], r['se'][0], r['ls'], r['se'][2], np.log(s2)]
if __name__ == '__main__':
    jobs = [(a, wc, n, k) for (a, wc, n) in CONDS for k in range(REPS)]
    with Pool(4) as p:
        out = p.map(one, jobs, chunksize=5)
    json.dump(out, open('mc_whittle.json', 'w'))
    out = np.array(out)
    print("alpha wc n | M | med bias a | RMSE | cover95 a | mean SE | 1/sqrt(M) | cover logq | cover logs2 | at-bound")
    for (a, wc, n) in CONDS:
        s = out[(out[:,0]==a)&(out[:,1]==wc)&(out[:,2]==n)]
        M = n*min(wc, np.pi)/(2*np.pi)
        ea = s[:,3]-a; cov = np.mean(np.abs(ea) <= 1.96*s[:,4])
        cq = np.mean(np.abs(s[:,5]-0) <= 1.96*s[:,6]); cs = np.mean(np.abs(s[:,7]-s[:,9]) <= 1.96*s[:,8])
        bnd = np.mean((s[:,3] < 1.02) | (s[:,3] > 2.98))
        print(f"{a} {wc} {n} | {M:.0f} | {np.median(ea):+.3f} | {np.sqrt(np.mean(ea**2)):.3f} | {cov:.2f} | {np.median(s[:,4]):.3f} | {1/np.sqrt(M):.3f} | {cq:.2f} | {cs:.2f} | {bnd:.2f}")
