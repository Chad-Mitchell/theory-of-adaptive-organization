"""Own check of the Parkinson log-variance noise floor: Var(log((ln H/L)^2/(4 ln 2))) for a Brownian day sampled at
m intraday steps (m = 390 one-minute steps; and m = 78, 5-minute). Compare with the full-band Whittle s2 = exp(-0.90)."""
import numpy as np, json
rng = np.random.default_rng(2028)
out = {}
for m in (78, 390, 4000):
    b = np.cumsum(rng.standard_normal((20000, m)), axis=1) / np.sqrt(m)
    b = np.concatenate([np.zeros((20000, 1)), b], axis=1)
    rg = b.max(1) - b.min(1)
    v = np.log(rg ** 2 / (4 * np.log(2)))
    out[m] = {'var_log': float(v.var()), 'mean_log': float(v.mean())}
out['whittle_full_s2'] = float(np.exp(-0.9005))
print(out); json.dump(out, open('range_floor.json', 'w'), indent=1)
