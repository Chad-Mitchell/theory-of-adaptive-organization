"""C3 (own code, pick 37; independent of pick 35's code): in the two-state (telegraph) world, the best EWMA (linear,
one-pole) tracker depends on the loss, so its adaptation-time response to a q-fixed kappa x4 change depends on the loss.
Discrete grid Delta = 0.01, N = 1 (per-sample noise variance N/Delta), points A (lam .01, mu^2 4) and B (lam .02, mu^2 2).
EWMA xh_k = xh_{k-1} + g (y_k - xh_{k-1}); estimate s*xh (s optimal per loss); losses: squared error (p=2), absolute
error (p=1), sign error (0-1 on sign(xh) != x). t_A = mean number of samples * Delta from a switch to the first sample at
which sign(xh) equals the new state (zero-crossing), over all switches with >= 1 sample of history.
Common random numbers across gains; optimum by quadratic fit of loss vs ln g near the grid minimum."""
import numpy as np, json, math, sys
from numba import njit

@njit(cache=True)
def run(gains, lam, mu, N, Delta, nsteps, seed, svals):
    np.random.seed(seed)
    G = gains.shape[0]; S = svals.shape[0]
    xh = np.zeros(G)
    se = np.zeros(G); ae = np.zeros((G, S)); sg = np.zeros(G)
    p = (1 - math.exp(-2 * lam * Delta)) / 2
    sd = math.sqrt(N / Delta)
    x = mu
    tA_sum = np.zeros(G); tA_n = np.zeros(G); since = -1; crossed = np.ones(G, dtype=np.bool_)
    cnt = 0
    for k in range(nsteps):
        if np.random.random() < p:
            x = -x
            for i in range(G):
                if not crossed[i]:
                    tA_n[i] -= 0  # censored crossing (another switch first): dropped
                crossed[i] = False
            since = 0
        y = x + sd * np.random.normal()
        if since >= 0:
            since += 1
        for i in range(G):
            xh[i] += gains[i] * (y - xh[i])
            if k > 100000:
                d = xh[i] - x
                se[i] += d * d
                for j in range(S):
                    ae[i, j] += abs(svals[j] * xh[i] - x)
                if (xh[i] > 0) != (x > 0):
                    sg[i] += 1
            if (not crossed[i]) and since > 0 and ((xh[i] > 0) == (x > 0)):
                crossed[i] = True
                if k > 100000:
                    tA_sum[i] += since * Delta; tA_n[i] += 1
        if k > 100000:
            cnt += 1
    return se / cnt, ae / cnt, sg / cnt, tA_sum / np.maximum(tA_n, 1), tA_n

def qmin(lg, L):
    i = int(np.argmin(L)); i = min(max(i, 2), len(L) - 3)
    c = np.polyfit(lg[i - 2:i + 3], L[i - 2:i + 3], 2)
    return -c[1] / (2 * c[0]) if c[0] > 0 else lg[i]

def interp_ta(lg, ta, x):
    return float(np.exp(np.interp(x, lg, np.log(ta))))

N, Delta = 1.0, 0.01
pts = {"A": (0.01, 2.0), "B": (0.02, math.sqrt(2.0))}
nsteps = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000_000
seeds = [37101, 37102, 37103, 37104]
out = {"nsteps_per_seed": nsteps, "seeds": seeds}
for name, (lam, mu) in pts.items():
    # Kalman (MSE-best linear, continuous) gain per sample: K ~ Delta*sqrt(q/N)-ish; scan widely around it
    q = 4 * lam * mu * mu; a = 2 * lam
    beta = math.sqrt(a * a + q / N)
    g0 = beta * Delta
    gains = g0 * np.exp(np.linspace(-1.6, 1.6, 33))
    svals = np.linspace(0.6, 1.4, 9)
    acc = None
    for sd_ in seeds:
        r = run(gains, lam, mu, N, Delta, nsteps, sd_, svals)
        acc = [np.array(v) for v in r] if acc is None else [acc[j] + (r[j] * (r[4] if j == 3 else 1) if False else r[j]) for j in range(5)]
    se, ae, sg, ta, tn = [v / len(seeds) if j < 4 else v for j, v in enumerate(acc)]
    lg = np.log(gains)
    # MSE with optimal scale s: E(s xh - x)^2 minimized -> use se at s=1 and also scaled MSE not stored; report s=1 MSE
    best = {"MSE(s=1)": qmin(lg, se), "abs(best s)": qmin(lg, ae.min(axis=1)), "sign01": qmin(lg, sg)}
    out[name] = {"lam": lam, "mu2": mu * mu, "kappa": lam * N / mu / mu, "kalman_cont_gain": g0,
                 "best_lng_minus_lnKalman": {k: round(v - math.log(g0), 4) for k, v in best.items()},
                 "tA_at_best": {k: round(interp_ta(lg, ta, v), 4) for k, v in best.items()},
                 "tA_at_kalman": round(interp_ta(lg, ta, math.log(g0)), 4),
                 "sign_err_min": round(float(sg.min()), 6), "sign_err_at_kalman": round(float(np.interp(math.log(g0), lg, sg)), 6),
                 "switches_counted": int(tn[16]),
                 "curve": {"lng": lg.round(4).tolist(), "mse": se.round(6).tolist(), "abs": ae.min(axis=1).round(6).tolist(),
                           "sign": sg.round(7).tolist(), "tA": ta.round(4).tolist()}}
    print(name, {k: v for k, v in out[name].items() if k != "curve"}, flush=True)
out["dln_tA_A_to_B"] = {k: round(math.log(out["B"]["tA_at_best"][k] / out["A"]["tA_at_best"][k]), 4) for k in out["A"]["tA_at_best"]}
print(out["dln_tA_A_to_B"])
json.dump(out, open("c3_telegraph_ewma_loss.json", "w"), indent=1)
