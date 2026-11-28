"""Hostile check of Conti & Mora 2022 (PRE 106:054404) claim: Bayes-optimal (Wonham) adaptation time to a
two-state switch scales ~log(tau), while the best linear tracker (EWMA) scales ~sqrt(tau*theta).
World: x in {-1,+1}, switch rate 1/tau; observation dy = x dt + sqrt(theta) dW. Seed fixed. In-model only."""
import numpy as np, json
rng = np.random.default_rng(20261115)
theta, dt = 1.0, 0.01
out = {}
for tau in [10, 30, 100, 300, 1000, 3000]:
    # --- Wonham: time from a switch until posterior mean crosses 0, starting from the pre-switch stationary state
    reps, T = 400, int(60 * theta / dt) + int(20*np.log(tau)/dt)
    # burn-in at x=-1 so m sits at its steady (biased) level
    m = np.full(reps, -0.9)
    for _ in range(int(5 / dt)):
        dy = -1 * dt + np.sqrt(theta * dt) * rng.standard_normal(reps)
        m += -(2 * m / tau) * dt + (1 - m * m) / theta * (dy - m * dt); m = np.clip(m, -1 + 1e-12, 1 - 1e-12)
    cross = np.full(reps, np.nan); t = 0.0
    for k in range(T):
        dy = 1 * dt + np.sqrt(theta * dt) * rng.standard_normal(reps)
        m += -(2 * m / tau) * dt + (1 - m * m) / theta * (dy - m * dt); m = np.clip(m, -1 + 1e-12, 1 - 1e-12)
        t += dt; new = np.isnan(cross) & (m > 0); cross[new] = t
        if not np.isnan(cross).any(): break
    tw = float(np.nanmedian(cross))
    # --- best EWMA time constant by MSE on a simulated path
    n = int(min(400 * tau, 4e6) / dt) if tau < 1000 else int(4e5 / dt)
    sw = rng.random(n) < dt / tau
    x = np.where(np.cumsum(sw) % 2 == 0, 1.0, -1.0)
    y = x + np.sqrt(theta / dt) * rng.standard_normal(n)
    best = None
    for tc in np.geomspace(0.05, 50, 40) * np.sqrt(tau * theta):
        a = dt / tc
        from scipy.signal import lfilter
        e = lfilter([a], [1, -(1 - a)], y)
        mse = float(np.mean((e[n // 10:] - x[n // 10:]) ** 2))
        if best is None or mse < best[1]: best = (float(tc), mse)
    out[tau] = {"wonham_median_cross_time": tw, "ewma_best_tc": best[0]}
    print(tau, out[tau], flush=True)
taus = np.array(list(out)); w = np.array([out[k]["wonham_median_cross_time"] for k in out]); e = np.array([out[k]["ewma_best_tc"] for k in out])
res = {"runs": out,
       "slope_loglog_wonham": float(np.polyfit(np.log(taus), np.log(w), 1)[0]),
       "slope_w_vs_lntau": float(np.polyfit(np.log(taus), w, 1)[0]),
       "slope_loglog_ewma": float(np.polyfit(np.log(taus), np.log(e), 1)[0])}
print(json.dumps(res, indent=1)); json.dump(res, open("telegraph_check.json", "w"), indent=1)
