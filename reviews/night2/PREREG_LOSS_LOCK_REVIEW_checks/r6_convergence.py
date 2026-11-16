"""Grid-convergence check of r4: at M = 12 cells per kernel sd (r4 used 6), re-locate each loss's argmin pole in a
+-0.15 ln window around the M = 6 argmin and recompute t_A; also Bayes. Usage: python r6_convergence.py PT"""
import sys, json, numpy as np
sys.argv = [sys.argv[0], '12', sys.argv[1]]
import r4_telegraph_grid as R
from scipy.optimize import minimize_scalar
pt = sys.argv[2]
prev = json.load(open('r4_telegraph_grid_M6.json'))[pt]
rk = prev['kalman_rate']; out = {'M': R.M, 'bayes': R.bayes(pt)}
for loss in ('err', 'mse', 'abs'):
    x0 = prev['best_'+loss]['lnrel']
    fn = lambda xx: R.onepole(pt, np.exp(-rk*np.exp(xx)*R.D))[loss]
    r = minimize_scalar(fn, bounds=(x0-0.15, x0+0.15), method='bounded', options=dict(xatol=2e-3))
    o = R.onepole(pt, np.exp(-rk*np.exp(r.x)*R.D)); out['best_'+loss] = dict(lnrel=r.x, **o)
    print(pt, loss, 'M12 argmin x Kalman %.4f (M6 %.4f)  tA %.4f (M6 %.4f)' % (np.exp(r.x), np.exp(x0), o['tA'], prev['best_'+loss]['tA']), flush=True)
print(pt, 'Bayes M12 tA %.4f (M6 %.4f)' % (out['bayes']['tA'], prev['bayes']['tA']))
json.dump(out, open(f'r6_convergence_{pt}.json', 'w'), indent=1, default=float)
