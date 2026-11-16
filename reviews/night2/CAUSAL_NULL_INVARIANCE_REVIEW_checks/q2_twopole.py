"""Q2 scope check: is the one-pole family the accuracy-best LINEAR tracker? Two-pole linear filters z = r1*m1 + w*r2*m2
(m_i <- a_i m_i + y, r_i = 1 - a_i) on common random numbers, vs the one-pole optimum from the same paths. Own code."""
import numpy as np, numba as nb, math, json, itertools
from gridengine import kalman_pole

@nb.njit(parallel=True, cache=True)
def errs(lam, mu, N, D, A1, A2, W, nsamp, seeds):
    C = A1.shape[0]; S = seeds.shape[0]
    out = np.zeros((S, C)); outT = np.zeros((S, C)); outN = np.zeros((S, C))
    for si in nb.prange(S):
        np.random.seed(seeds[si])
        p = (1 - math.exp(-2 * lam * D)) / 2; s = math.sqrt(N / D)
        x = 1.0
        m1 = np.zeros(C); m2 = np.zeros(C)
        waiting = np.zeros(C, dtype=nb.boolean); cnt = np.zeros(C)
        burn = 200000
        for k in range(burn + nsamp):
            sw = False
            if np.random.random() < p:
                x = -x; sw = k >= burn
            y = x * mu + s * np.random.standard_normal()
            for c in range(C):
                m1[c] = A1[c] * m1[c] + y
                m2[c] = A2[c] * m2[c] + y
                z = (1 - A1[c]) * m1[c] + W[c] * (1 - A2[c]) * m2[c]
                if k >= burn:
                    if z * x <= 0: out[si, c] += 1
                    if sw:
                        waiting[c] = True; cnt[c] = 0
                    if waiting[c]:
                        cnt[c] += 1
                        if z * x > 0:
                            outT[si, c] += cnt[c]; outN[si, c] += 1; waiting[c] = False
    return out / nsamp, outT, outN

N = 1.0; D = 0.01
pts = {"A": (0.01, 2.0, 2.265), "B": (0.02, math.sqrt(2.0), 1.548)}
res = {}
for k, (lam, mu, t1best) in pts.items():
    pole, _ = kalman_pole(lam, mu, N, D); r0 = 1 - pole
    cands = [(t1best, t1best, 0.0)]                        # exact one-pole optimum (reference)
    for f in np.exp(np.linspace(-0.3, 0.3, 7)):            # one-pole neighbours
        cands.append((t1best * f, t1best * f, 0.0))
    for ts, tf, w in itertools.product(np.exp(np.linspace(math.log(0.8), math.log(3.2), 9)),
                                       np.exp(np.linspace(math.log(1.5), math.log(10.0), 6)),
                                       [-0.4, -0.2, -0.1, 0.05, 0.1, 0.2, 0.4, 0.8]):
        cands.append((ts, tf * ts, w))
    A1 = np.array([1 - r0 * c[0] for c in cands]); A2 = np.array([1 - r0 * c[1] for c in cands]); W = np.array([c[2] for c in cands])
    e, T, n = errs(lam, mu, N, D, A1, A2, W, 10_000_000, np.arange(31, 47))
    d = e - e[:, [0]]                                      # paired difference vs exact one-pole optimum
    md = d.mean(0); sd = d.std(0, ddof=1) / math.sqrt(e.shape[0])
    j = int(np.argmin(md))
    tA = D * T.sum(0) / n.sum(0)
    res[k] = dict(onepole_err=float(e[:, 0].mean()), best=cands[j], best_diff=float(md[j]), best_diff_se=float(sd[j]),
                  best_rel=float(md[j] / e[:, 0].mean()), tA_onepole=float(tA[0]), tA_best=float(tA[j]),
                  n_better_2se=int(((md + 2 * sd) < 0).sum()), ncand=len(cands))
    order = np.argsort(md)[:8]
    res[k]["top8"] = [(cands[i], float(md[i]), float(sd[i]), float(tA[i])) for i in order]
    print(k, res[k], flush=True)
json.dump(res, open("q2_twopole.json", "w"), indent=1, default=float)
