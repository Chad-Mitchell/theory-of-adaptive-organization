"""TELEGRAPH-LINEAR-PREMISE P5 (amendment 1): projection kernel of the Bayes tracker = Kalman kernel (law of iterated projections).
Seed 20261118. In-model only."""
import numpy as np, json
from scipy.special import expit
theta, tau, dt, R = 1.0, 100.0, 0.01, 64
T = 400 * tau; n = int(T / dt); burn = int(5 * tau / dt)
bw, NB = 0.5, 80; spb = int(bw / dt)
rng = np.random.default_rng(20261118)
k = dt / (2 * tau); c = 1 - 2 * k
y = np.where(rng.random(R) < 0.5, 1.0, -1.0); Lam = np.zeros(R)
nb = n // spb
dsb = np.zeros((R, nb)); xh = np.zeros((R, nb)); yy = np.zeros((R, nb))
acc = np.zeros(R)
for i in range(n):
    y = np.where(rng.random(R) < k, -y, y)
    ds = y * dt + np.sqrt(theta * dt) * rng.standard_normal(R)
    a = np.abs(Lam); u = 2 * expit(-2 * a)
    Lam = np.sign(Lam) * 0.5 * (np.log(1 + c - c * u) - np.log(2 * k + c * u)) + ds / theta
    acc += ds
    if (i + 1) % spb == 0:
        j = (i + 1) // spb - 1
        dsb[:, j] = acc; acc[:] = 0; xh[:, j] = np.tanh(Lam); yy[:, j] = y
# design: for bin j, regressors = increments in bins j, j-1, ..., j-NB+1 (bin j ends at the sample time)
b0 = burn // spb + NB
X = np.concatenate([np.stack([dsb[r, j - np.arange(NB)] for j in range(b0, nb)]) for r in range(R)])
Yx = np.concatenate([xh[r, b0:nb] for r in range(R)]); Yy = np.concatenate([yy[r, b0:nb] for r in range(R)])
cx = np.linalg.lstsq(X, Yx, rcond=None)[0]; cy = np.linalg.lstsq(X, Yy, rcond=None)[0]
beta = np.sqrt(1 / tau ** 2 + 2 / (tau * theta)); P = theta * (-1 / tau + beta); g = P / theta
lags = np.arange(NB) * bw
# analytic coefficient for a bin of increments covering ages [l, l+bw): integral of g e^{-beta u} over the bin / bw * bw -> per unit ds
kal = g * (np.exp(-beta * lags) - np.exp(-beta * (lags + bw))) / (beta * bw)
rel = lambda a, b: float(np.linalg.norm(a - b) / np.linalg.norm(b))
out = {"rel_L2_bayes_vs_y": rel(cx, cy), "rel_L2_bayes_vs_kalman": rel(cx, kal), "rel_L2_y_vs_kalman": rel(cy, kal),
       "coef_bayes_first5": cx[:5].tolist(), "coef_y_first5": cy[:5].tolist(), "kalman_first5": kal[:5].tolist(),
       "n_rows": int(X.shape[0])}
print(json.dumps(out, indent=1)); json.dump(out, open("../out_linproj.json", "w"), indent=1)
