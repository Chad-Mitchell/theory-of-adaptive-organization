"""TELEGRAPH-LINEAR-PREMISE P4: exact periodic reads every T; between reads predict with (a) hold-last-value, (b) the
conditional mean y_read * exp(-s/tau). Time-averaged MSE for a telegraph world vs an OU world with the same covariance
e^{-|t|/tau}, var 1. Theory (S5): hold MSE = mean over s in [0,T) of 2(1 - e^{-s/tau}); conditional-mean MSE = mean of 1 - e^{-2s/tau}, for BOTH worlds.
Seed 20261117. tau = 1, T/tau in {0.01, 0.1, 1}."""
import numpy as np, json
tau, dt, R = 1.0, 0.001, 4000
out = {}
for j, T in enumerate([0.01, 0.1, 1.0]):
    rng = np.random.default_rng(20261117 + j)
    n = int(round(T / dt)); s = np.arange(n) * dt
    # telegraph: y(0) = +-1 at stationarity, simulate path on [0,T)
    y0 = np.where(rng.random(R) < 0.5, 1.0, -1.0)
    flips = rng.random((R, n)) < dt / (2 * tau); flips[:, 0] = False
    ytel = y0[:, None] * np.where(np.cumsum(flips, axis=1) % 2 == 0, 1.0, -1.0)
    # OU exact discretisation, var 1, corr e^{-t/tau}
    z0 = rng.standard_normal(R); a = np.exp(-dt / tau); zou = np.empty((R, n)); zou[:, 0] = z0
    for k in range(1, n):
        zou[:, k] = a * zou[:, k - 1] + np.sqrt(1 - a * a) * rng.standard_normal(R)
    cm = np.exp(-s / tau)
    r = {}
    for name, path, x0 in (("telegraph", ytel, y0), ("ou", zou, z0)):
        hold = ((path - x0[:, None]) ** 2).mean(axis=1); cond = ((path - x0[:, None] * cm) ** 2).mean(axis=1)
        r[name] = {"hold_mse": float(hold.mean()), "hold_se": float(hold.std() / np.sqrt(R)),
                   "cond_mse": float(cond.mean()), "cond_se": float(cond.std() / np.sqrt(R))}
    r["theory_hold"] = float(np.mean(2 * (1 - cm))); r["theory_cond"] = float(np.mean(1 - cm ** 2))
    out[str(T)] = r; print(T, r, flush=True)
json.dump(out, open("../out_reset.json", "w"), indent=1)
