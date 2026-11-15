"""Monte Carlo spread of the locked P1 decision statistic |D| + 1.96 sqrt(bootsd^2 + 0.0264^2) over bootstrap seeds
(block 126, 999 reps, the locked design); the point estimate is seed-free. Own code."""
import numpy as np, json, math
from rlib import *
g = load(); y = g['y'].values; X, t = design(y); yb = future_mean(y)[t]; ok = np.isfinite(yb)
sds = []
for s in range(100, 160):
    f, Wd, _, _ = block_boot(X[ok], {'ybar': yb[ok]}, seed=s); sds.append(Wd['ybar'].std(ddof=1))
Wb = f['ybar'][0]; sds = np.array(sds); stat = abs(Wb - 0.2579) + 1.96 * np.sqrt(sds ** 2 + 0.0264 ** 2)
out = {'W': Wb, 'boot_sd_mean': sds.mean(), 'boot_sd_sd': sds.std(ddof=1), 'boot_sd_range': [sds.min(), sds.max()],
       'stat_mean': stat.mean(), 'frac_PASS': float((stat <= 0.13).mean()), 'seeds': 60,
       'bootsd_at_boundary': math.sqrt(((0.13 - abs(Wb - 0.2579)) / 1.96) ** 2 - 0.0264 ** 2)}
json.dump(out, open('r3_seeds.json', 'w'), indent=1, default=float); print(out)
