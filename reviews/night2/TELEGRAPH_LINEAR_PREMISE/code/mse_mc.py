"""TELEGRAPH-LINEAR-PREMISE: Monte Carlo stationary MSE of the exact discrete Bayes filter (F1 of adapt_mc.py) on a switching
world, cross-check of fp_mse.py at tau in {100, 300, 1000}. dt 0.01, 64 paths, length 60 tau after 5 tau burn-in. Seed 20261116."""
import numpy as np, json
from scipy.special import expit
theta, dt, R = 1.0, 0.01, 64
out = {}
for i, tau in enumerate([100, 300, 1000]):
    rng = np.random.default_rng(20261116 + i)
    y = np.where(rng.random(R) < 0.5, 1.0, -1.0); Lam = np.zeros(R)
    k = dt / (2 * tau); c = 1 - 2 * k
    nb, nt = int(5 * tau / dt), int(60 * tau / dt)
    acc = np.zeros(R); cnt = 0
    for n in range(nb + nt):
        y = np.where(rng.random(R) < k, -y, y)   # switch prob per step = rate*dt = dt/(2tau)
        ds = y * dt + np.sqrt(theta * dt) * rng.standard_normal(R)
        a = np.abs(Lam); u = 2 * expit(-2 * a)
        Lam = np.sign(Lam) * 0.5 * (np.log(1 + c - c * u) - np.log(2 * k + c * u)) + ds / theta
        if n >= nb:
            acc += (y - np.tanh(Lam)) ** 2; cnt += 1
    per = acc / cnt
    out[str(tau)] = {"mse": float(per.mean()), "se": float(per.std() / np.sqrt(R))}
    print(tau, out[str(tau)], flush=True)
json.dump(out, open("../out_mse_mc.json", "w"), indent=1)
