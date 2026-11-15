"""Referee check of P5's scope. Iterated projections make the regression kernel of a Bayes tracker on its own
observations s equal the Wiener/Kalman kernel. Does that also hold when the experimenter regresses the tracker's output
on the TRUE driver y (sensing noise internal/unseen)? Kalman: projection of K*s on span(y) = K*y exactly (noise ⟂ y).
Bayes: no such identity. Telegraph, tau = 30, theta = 1 (kappa = 1/60), dt = 0.01, 32 paths x 300 tau, seed 7300.
Regress x_hat (Bayes, exact discrete HMM filter) and x_K (Kalman) on 60 lagged bins (width 0.5) of y; compare kernels."""
import numpy as np, json
rng = np.random.default_rng(7300)
tau, th, dt = 30.0, 1.0, 0.01
lam = 1/(2*tau); k = 0.5*(1-np.exp(-2*lam*dt))
beta = np.sqrt(1/tau**2 + 2/(tau*th)); P = th*(-1/tau + np.sqrt(1/tau**2 + 2/(tau*th))); g = P/th
nb, w = 60, 50   # bins of 50 steps = 0.5
X_rows, yb_rows, xb_rows, xk_rows = [], [], [], []
for path in range(32):
    n = int(300*tau/dt)
    sw = rng.random(n) < k
    y = np.where(np.cumsum(sw) % 2 == 0, 1.0, -1.0)
    ds = y*dt + np.sqrt(th*dt)*rng.standard_normal(n)
    L = 0.0; xk = 0.0
    xb = np.empty(n); xK = np.empty(n)
    lk, l1k = np.log(k), np.log1p(-k)
    for i in range(n):
        a = np.logaddexp(l1k + L, lk); b = np.logaddexp(lk + L, l1k); L = a - b + 2*ds[i]/th
        xb[i] = np.tanh(L/2)
        xk += -xk*dt/tau + g*(ds[i] - xk*dt)
        xK[i] = xk
    ybin = y[:n//w*w].reshape(-1, w).mean(1)
    xbe = xb[w-1::w][:len(ybin)]; xke = xK[w-1::w][:len(ybin)]
    for t in range(nb, len(ybin)):
        X_rows.append(ybin[t-nb+1:t+1][::-1]); xb_rows.append(xbe[t]); xk_rows.append(xke[t])
X = np.array(X_rows); XB = np.array(xb_rows); XK = np.array(xk_rows)
cb = np.linalg.lstsq(X, XB, rcond=None)[0]; ck = np.linalg.lstsq(X, XK, rcond=None)[0]
u = (np.arange(nb) + 0.5)*0.5
analytic = g*np.exp(-beta*u)*0.5*(1 - 0)  # Kalman impulse response to y (s = y + noise, noise drops out), per bin width
rel = lambda a, b: float(np.linalg.norm(a - b)/np.linalg.norm(b))
out = {"tau": tau, "theta": th, "kappa": th/(2*tau),
       "relL2_kalman_reg_vs_analytic": rel(ck, analytic),
       "relL2_bayes_reg_vs_kalman_reg": rel(cb, ck),
       "sum_bayes_kernel": float(cb.sum()), "sum_kalman_kernel": float(ck.sum()),
       "bayes_kernel_first10": cb[:10].tolist(), "kalman_kernel_first10": ck[:10].tolist(),
       "R2_bayes_on_y": float(1 - np.var(XB - X@cb)/np.var(XB)), "R2_kalman_on_y": float(1 - np.var(XK - X@ck)/np.var(XK))}
print(json.dumps(out, indent=1)); json.dump(out, open("out_kernel_input_ref.json", "w"), indent=1)
