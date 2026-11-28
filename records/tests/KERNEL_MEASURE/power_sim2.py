"""DESIGN 2 (binned OLS; W21 tail share, s_tail). MV10 power gate + estimator dry run on synthetic truth for KERNEL-MEASURE (no VIX data used).
World: driver = fBm(alpha, q) + white noise s2, inputs as measured on the driver (driver_band.json, locked primary);
n = 9276 business days. Trackers: H0 = theory's best linear predictor (2000-day window) of the 21-day-ahead mean
+ AR(1) tracker noise; rivals R1 (alpha = 2 Kalman/EWMA kernel), R2 (flat 1/5/22-day averages), R3 (power-law
kernel with survival exponent alpha - 1, c = 21)."""
import sys, json, time, numpy as np, klib
cond = sys.argv[1]; reps = int(sys.argv[2]); seed = int(sys.argv[3])
A, Q, S2, N = 1.2587, np.exp(-1.8116), np.exp(-0.9005), 9276
def kern(name, a=A):
    if name == 'H0':
        return klib.ok_kernel(a, Q, S2, Lw=2000)
    if name == 'R1':
        q2 = Q * klib.aqn.D1(A) * 21 ** (A - 1) / (klib.aqn.D1(2.0) * 21)
        return klib.ok_kernel(2.0, q2, S2, Lw=2000)
    if name == 'R2':
        w = np.zeros(2000); w[0] += 1 / 3; w[:5] += 1 / 15; w[:22] += 1 / 66; return w
    if name == 'R3':
        t = np.arange(2000); w = (t + 21.0) ** (-(1 + (A - 1))); return w / w.sum()
from numpy.lib.stride_tricks import sliding_window_view
def tracker_long(y, w, rng, r, phi=0.95):
    f = np.full(len(y), np.nan); f[1999:] = sliding_window_view(y, 2000)[:, ::-1] @ w
    sd = r * np.nanstd(f)
    return -3.0 + f + (klib.ar1(len(y), phi, sd, rng) if r > 0 else 0)
name, r, a_world = cond.split('_')[0], float(cond.split('_')[1]), float(cond.split('_')[2]) if cond.count('_') > 1 else A
rng = np.random.default_rng(seed)
w = kern(name, a_world)
res = []
t0 = time.time()
for k in range(reps):
    x, y = klib.sim_driver(N + 1999 - 503, a_world, Q, S2, rng)   # 1999-503 extra presample so the fit sees n = N
    z = tracker_long(y, w, rng, r)
    o = klib.fit_bins(z[1999 - 503:], y[1999 - 503:], nboot=199, seed=seed + k)
    res.append(o)
    print(k, o, round(time.time() - t0, 1), flush=True)
json.dump({'cond': cond, 'seed': seed, 'res': res}, open(f'power2/{cond}.json', 'w'), indent=1)
