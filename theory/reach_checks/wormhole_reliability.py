#!/usr/bin/env python3
"""REACH check 6: throat reliability (Pi6) and endogenous drift (Pi7) in the pooling model of WORMHOLES.md section 2.
Run: nice -n 19 python3 wormhole_reliability.py > wormhole_reliability.out      (numpy, scipy)
Model (alpha = 2, diffusive drift, error variance of a target = w*s2 * AGE of its last delivered reading; c = read price,
d = price of one telling attempt, N targets, update interval T; cost rate of the central design =
(c + N d)/T + N w s2 * E[age]; all-local = N sqrt(2 c w s2)).
(A) independent delivery failure, s = (1-p)^h = success probability per target per cycle, no retry within the cycle:
      E[age] = T (2-s)/(2 s);  central wins at zero extra latency iff d/c < 1/g - 1/N, g = (2-s)/s.
(A') retry until acknowledged (attempts per target 1/s, same age as no failure): central wins iff d/c < s (1 - 1/N).
(B) throat outages (alternating up/down renewal process, up-fraction A, down time X with mean theta, CV^2), FIFO delivery:
      E[age] = T/2 + (1-A) E[X^2]/(2 E[X]) = T/2 + (1-A) theta (1+CV^2)/2  -> the section-2 latency rule with l = that extra term.
(C) station coverage with independent throat failure p: nu -> (1-p) nu (thinning of a Poisson process).
    Tube map with throats failing independently (quenched) with probability p: slope of latency against distance (simulation).
(D) endogenous drift q = q0 m^beta when shortcuts speed signals up by a factor m:
      zero-latency rule d/c < 1 - 1/N is invariant (both designs scale as sqrt(q)); latency threshold l_crit ~ q^(-1/2);
      LAT-1 reach L = m c (D*/q)^(1/(alpha-1)) ~ m^(1 - beta/(alpha-1)); partial sharing: 1/N*(rho) = (sqrt(1+rho)-1)/(sqrt(1+rho)+1).
"""
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
rng = np.random.default_rng(1119)

print("(A) independent delivery failure: Monte Carlo of the age process vs T(2-s)/(2s)   [T = 1]")
print("%6s %10s %10s" % ("s", "MC age", "formula"))
for s in (1.0, 0.9, 0.7, 0.5, 0.25):
    ncyc = 400000
    ok = rng.random(ncyc) < s
    # age at a uniformly random time inside cycle j = U + T * (number of cycles since the last delivered cycle, counting the current)
    last = np.maximum.accumulate(np.where(ok, np.arange(ncyc), -1)); k = np.arange(ncyc) - last
    valid = last >= 0
    age = rng.random(ncyc) + k            # time since the measurement of the last delivered update, T = 1
    print("%6.2f %10.4f %10.4f" % (s, age[valid].mean(), (2 - s) / (2 * s)))

print("\n(A) thresholds, brute force over T (c = 1, w s2 = 1) vs closed form; central wins iff cost_central < N sqrt(2)")
def central_cost(N, dc, s, retry):
    if retry: a, g = dc / s, 1.0
    else: a, g = dc, (2 - s) / s
    f = lambda T: (1 + N * a) / T + N * T * g / 2
    T = minimize_scalar(f, bounds=(1e-6, 1e4), method="bounded").x
    return f(T)
bad = tot = 0
for N in (4, 16, 100):
    for s in (1.0, 0.95, 0.8, 0.5):
        g = (2 - s) / s
        for dc in np.linspace(0, 1.0, 41):
            for retry in (False, True):
                win = central_cost(N, dc, s, retry) < N * np.sqrt(2)
                thr = s * (1 - 1.0 / N) if retry else 1.0 / g - 1.0 / N
                if abs(dc - thr) < 1e-3: continue
                tot += 1; bad += (win != (dc < thr))
print("  brute force vs closed form: disagree in %d of %d cases (cases within 1e-3 of a boundary skipped)" % (bad, tot))
print("  examples (N = 16): s = 1: d/c < %.4f;  s = 0.9 no retry: d/c < %.4f, retry: d/c < %.4f;  s = 0.5 no retry: d/c < %.4f, retry: d/c < %.4f" %
      (1 - 1 / 16, 0.9 / 1.1 - 1 / 16, 0.9 * (1 - 1 / 16), 0.5 / 1.5 - 1 / 16, 0.5 * (1 - 1 / 16)))
print("  per-hop failure p over h hops: s = (1-p)^h, g = 2 (1-p)^-h - 1  (about 1 + 2 h p for small p); e.g. p = 0.1: h = 1 g = %.3f, h = 3 g = %.3f" % (2 / 0.9 - 1, 2 / 0.9 ** 3 - 1))

print("\n(B) throat outages: Monte Carlo of the mean age with FIFO delivery vs T/2 + (1-A) theta (1+CV^2)/2   [T = 1, up mean 10]")
def saw_int(x0, x1, T):
    k0, k1 = np.floor(x0 / T), np.floor(x1 / T)
    if k0 == k1: return ((x0 - k0 * T) + (x1 - k1 * T)) / 2 * (x1 - x0)
    first = ((x0 - k0 * T) + T) / 2 * ((k0 + 1) * T - x0); last = (x1 - k1 * T) / 2 * (x1 - k1 * T)
    return first + last + (k1 - k0 - 1) * T * T / 2
def sim_outage(sampler_down, up_mean, T=1.0, horizon=4e6):
    # alternating renewal: up ~ Exp(up_mean), down ~ sampler_down(); updates measured at kT, delivered at max(kT, reopen).
    # In an up period [a, b] the age is the sawtooth t - floor(t/T) T. During a down period [b, e] it grows from its value at b.
    t = 0.0; tot = 0.0; down = 0.0
    while t < horizon:
        u = rng.exponential(up_mean); x = sampler_down(); a, b, e = t, t + u, t + u + x
        tot += saw_int(a, b, T)
        tot += (b - np.floor(b / T) * T) * x + x * x / 2
        down += x; t = e
    return tot / t, 1 - down / t
print("%-28s %8s %8s %10s %10s" % ("down-time law (mean theta = 2)", "A", "CV^2", "MC age", "formula"))
laws = [("exponential", lambda: rng.exponential(2.0), 1.0),
        ("gamma k=4 (CV^2 = 0.25)", lambda: rng.gamma(4.0, 0.5), 0.25),
        ("lognormal sigma=1.2 (CV^2>1)", lambda: rng.lognormal(np.log(2.0) - 0.72, 1.2), np.exp(1.44) - 1),
        ("constant", lambda: 2.0, 0.0)]
for name, smp, cv2 in laws:
    mc, A = sim_outage(smp, 10.0)
    print("%-28s %8.4f %8.2f %10.4f %10.4f" % (name, A, cv2, mc, 0.5 + (1 - A) * 2.0 * (1 + cv2) / 2))

print("\n(C) station coverage with independent throat failure p: sim vs 1 - exp(-(4pi/3)(1-p) nu r^3)   [periodic unit cube]")
targets = rng.random((3000, 3)); print("%6s %7s %6s %9s %9s" % ("p", "nu", "r", "sim", "formula"))
for p in (0.0, 0.3, 0.6):
    for nu, r in ((100, 0.1), (1000, 0.05)):
        cov = []
        for _ in range(60):
            n = max(rng.poisson(nu), 1); st = rng.random((n, 3)); st = st[rng.random(n) >= p]
            if len(st) == 0: cov.append(np.zeros(len(targets), bool)); continue
            cov.append(cKDTree(st, boxsize=1.0).query(targets)[0] <= r)
        print("%6.1f %7d %6.2f %9.3f %9.3f" % (p, nu, r, np.mean(cov), 1 - np.exp(-4 * np.pi / 3 * (1 - p) * nu * r ** 3)))

print("\n(C) tube map with throats failing independently (quenched): latency slope vs distance (box 10, mouths density 2, Lam = 1, tau = 0.1, light transfers within 1.5, c = 1)")
def tube_fail(p, Lam=1.0, tau=0.1, box=10.0, nu=2.0, Rt=1.5, ntarg=3000):
    n = rng.poisson(nu * box ** 3); M = rng.random((n, 3)) * box; P = np.vstack([np.zeros((1, 3)), M]); t = cKDTree(P)
    W = {}                                   # keep the minimum weight on duplicate edges (a throat and a light transfer between the same pair)
    for i, j in t.query_pairs(Rt):
        dd = np.linalg.norm(P[i] - P[j]); W[(i, j)] = W[(j, i)] = dd
    for i, j in t.query_pairs(Lam):
        if i == 0 or j == 0: continue
        if rng.random() >= p:                # a working throat
            W[(i, j)] = min(W.get((i, j), np.inf), tau); W[(j, i)] = W[(i, j)]
    G = coo_matrix(([v for v in W.values()], ([k[0] for k in W], [k[1] for k in W])), shape=(n + 1, n + 1)).tocsr()
    lat = dijkstra(G, directed=True, indices=0)
    T = rng.random((ntarg, 3)) * box; dist = np.linalg.norm(T, axis=1)
    dm, im = t.query(T, k=16); L = np.minimum(np.min(lat[im] + dm, axis=1), dist)
    sel = (dist > 3) & (dist < 9.5); return np.polyfit(dist[sel], L[sel], 1)[0]
print("%6s %10s   (light only = 1.000; bound tau/Lam = 0.100)" % ("p", "slope"))
for p in (0.0, 0.3, 0.6, 0.8, 0.9, 0.95, 1.0):
    print("%6.2f %10.3f" % (p, np.mean([tube_fail(p) for _ in range(3)])))

print("\n(D) endogenous drift q = q0 m^beta")
print("(D1) zero-latency rule is invariant to a common scaling of q; latency threshold scales as q^(-1/2) (brute force):")
def thresholds(N, dc, q):
    loc = N * np.sqrt(2 * 1.0 * q)
    f = lambda T: (1 + N * dc) / T + N * q * T / 2
    Tt = minimize_scalar(f, bounds=(1e-7, 1e5), method="bounded").x; cen = f(Tt)
    return cen < loc, (loc - cen) / (N * q)          # (wins at zero latency, critical latency)
for N, dc in ((16, 0.0), (16, 0.5), (100, 0.05)):
    row = []
    for q in (0.25, 1.0, 4.0, 16.0):
        win, lcrit = thresholds(N, dc, q); row.append("q=%g: wins=%s l_crit=%.4f (l_crit sqrt(q)=%.4f)" % (q, win, lcrit, lcrit * np.sqrt(q)))
    print("  N=%d d/c=%.2f  " % (N, dc) + " | ".join(row))
print("(D2) reach L = m c (D*/q0 m^beta)^(1/(alpha-1)) relative to m = 1 (c = 1, D* = q0 = 1); exponent 1 - beta/(alpha-1)")
print("%7s %7s %6s %10s %10s" % ("alpha", "beta", "m", "L(m)/L(1)", "m^(1-b/(a-1))"))
for a_ in (2.0, 3.0):
    for b_ in (0.0, 0.5, 1.0, 1.5, 2.0):
        for m in (2.0, 10.0):
            L = m * (1.0 / m ** b_) ** (1 / (a_ - 1)); print("%7.1f %7.1f %6.0f %10.4f %10.4f" % (a_, b_, m, L, m ** (1 - b_ / (a_ - 1))))
print("(D3) partial sharing: 1/N*(rho) = (sqrt(1+rho)-1)/(sqrt(1+rho)+1)  (identity check) and its direction under acceleration of the shared or private part")
for rho in (0.1, 0.5, 1.0, 4.0, 100.0):
    Ns = (np.sqrt(1 + rho) + 1) ** 2 / rho; sr = np.sqrt(1 + rho)
    print("  rho = %6.1f  1/N* = %.5f  (s-1)/(s+1) = %.5f" % (rho, 1 / Ns, (sr - 1) / (sr + 1)))
print("  1/N*(rho) increases with rho, so acceleration of the SHARED drift (rho up) widens the range of d/c where pooling wins, and of the PRIVATE drift narrows it.")
