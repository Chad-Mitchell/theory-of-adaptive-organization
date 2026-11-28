"""Numerical checks of the theory kernel (no VIX data). (1) tail slope of ok_kernel vs -(1+alpha/2);
(2) ok_kernel vs an empirical regression of the future h-mean of x on lagged y in a long simulation (short window)."""
import json, numpy as np, klib
out = {}
for a in (1.2, 1.26, 1.5, 1.8):
    w = klib.ok_kernel(a, np.exp(-1.81), np.exp(-0.90), Lw=2000)
    t = np.arange(2000)
    sel = (t >= 200) & (t <= 1000)
    sl = np.polyfit(np.log(t[sel]), np.log(np.abs(w[sel])), 1)[0]
    surv = np.array([w[k:].sum() for k in (100, 400)])
    out[str(a)] = {'tail_slope_200_1000': float(sl), 'pred': -(1 + a / 2), 'min_w': float(w.min()),
                   'surv_slope_100_400': float(np.log(surv[1] / surv[0]) / np.log(4)), 'pred_surv': -a / 2}
    print(a, out[str(a)])
# (2) empirical check, window Lw = 40, alpha 1.26
rng = np.random.default_rng(28)
a, q, s2, Lw, h = 1.26, np.exp(-1.81), np.exp(-0.90), 40, 21
wt = klib.ok_kernel(a, q, s2, Lw=Lw, h=h)
Xs, Ys = [], []
for rep in range(40):
    x, y = klib.sim_driver(60000, a, q, s2, rng)
    from numpy.lib.stride_tricks import sliding_window_view
    X = sliding_window_view(y, Lw)[:, ::-1][: -h]
    fut = sliding_window_view(x, h).mean(1)[Lw:]
    m = min(len(X), len(fut)); X, fut = X[:m], fut[:m]
    # weights sum to 1 constraint: regress (fut - y_t) on (y_{t-i} - y_t), i >= 1
    Xs.append(X[:, 1:] - X[:, :1]); Ys.append(fut - X[:, 0])
Xa, Ya = np.vstack(Xs), np.concatenate(Ys)
b = np.linalg.lstsq(Xa, Ya, rcond=None)[0]
we = np.concatenate([[1 - b.sum()], b])
out['empirical_Lw40'] = {'max_abs_diff': float(np.max(np.abs(we - wt))), 'w0_theory': float(wt[0]), 'w0_emp': float(we[0]),
                         'sum_w_beyond_10_theory': float(wt[10:].sum()), 'emp': float(we[10:].sum())}
print(out['empirical_Lw40'])
json.dump(out, open('check_kernel.json', 'w'), indent=1)
