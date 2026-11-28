"""Referee Monte Carlo cross-check of the quadrature adaptation time (independent code).
Exact discrete-time two-state HMM forward filter on observation increments ds ~ N(y dt, theta dt), switching prob
k = (1 - e^{-2 lam dt})/2 per step, lam = 1/(2 tau); log-odds update L <- ln[((1-k)e^L + k)/(k e^L + 1 - k)] + 2 ds/theta.
Burn-in: L0 drawn by running 60 theta at y=+1 from L=0; then y=-1 (no further switch); first step with L<0.
Seeds 7100+i. theta = 1."""
import numpy as np, json, sys
def run(tau, dt, reps, seed, th=1.0, burn=60.0, tmax=80.0):
    rng = np.random.default_rng(seed)
    lam = 1/(2*tau); k = 0.5*(1-np.exp(-2*lam*dt))
    L = np.zeros(reps)
    def prior(L):  # log-odds after one Markov step, stable
        a = np.logaddexp(np.log1p(-k) + L, np.log(k)); b = np.logaddexp(np.log(k) + L, np.log1p(-k)); return a - b
    for _ in range(int(burn/dt)):
        ds = dt + np.sqrt(th*dt)*rng.standard_normal(reps)
        L = prior(L) + 2*ds/th
    L0 = L.copy()
    t = np.full(reps, np.nan); alive = np.ones(reps, bool)
    n = 0
    while alive.any() and n*dt < tmax:
        n += 1
        ds = -dt + np.sqrt(th*dt)*rng.standard_normal(alive.sum())
        L[alive] = prior(L[alive]) + 2*ds/th
        hit = alive.copy(); hit[alive] = L[alive] < 0
        t[hit] = n*dt; alive &= ~hit
    t0 = (L0 < 0)  # already below at switch: count passage at 0
    t[t0] = 0.0
    return float(np.nanmean(t)), float(np.nanstd(t)/np.sqrt(reps)), float(np.mean(L0)), float(np.isnan(t).mean())
out = {}
for tau in [100, 10000]:
    for dt in [0.004, 0.001]:
        m, se, l0, cens = run(tau, dt, 4000, 7100 + int(np.log10(tau))*10 + int(dt*1e3))
        out[f"tau={tau},dt={dt}"] = {"mean_tA": m, "se": se, "mean_L0": l0, "censored": cens,
            "Siegmund_discrete_monitoring_bias≈0.5826*sigma*sqrt(dt)/|drift|": 0.5826*2*np.sqrt(dt)/2}
        print(tau, dt, out[f"tau={tau},dt={dt}"], flush=True)
json.dump(out, open("out_mc_ref.json", "w"), indent=1)
