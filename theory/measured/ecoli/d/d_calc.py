#!/usr/bin/env python3
"""ECOLI-MEM follow-up D (rules locked in ../PREREG_D.md at fc83d62). D1 Celani-Vergassola maximin memory; D2 gain-bounded
drift optimum with Model S+ noise; E2 speed price from measured dissipation; H implied slow habitat mode (diagnostic)."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
lam, av, G, t1, t2, sn = 0.862, 157.1, 1.73, 0.22, 9.9, 0.092
K0 = G * t2 * t2 / (t1 + t2); V0 = sn ** 2 / K0 ** 2
M = (9.3, 10.5)
f2 = json.load(open(os.path.join(HERE, "..", "f2", "f2_results.json")))["park2010"]
S = (f2["s_rma_boot95"][0], f2["s_rma"], f2["s_rma_boot95"][1]); GS = (0.1, 0.2, 0.3, 0.4)
taus = np.logspace(-2, 4, 120001)
def verdict(L, U):
    if L / 2 <= M[0] and M[1] <= 2 * U: return "EXPLAINS"
    if M[0] > 3 * U or M[1] < L / 3: return "DOES NOT EXPLAIN"
    return "NEITHER"
out = {}
# D1
d1 = [1 / (2 * l) for l in (lam - 0.005, lam + 0.005)] + [1 / (8 / 3 / 1.0)]
out["D1_celani_vergassola"] = dict(memory_s=d1, L=min(d1), U=max(d1), verdict=verdict(min(d1), max(d1)))
# D2: corr(a,u)^2 = EV/sigma^2 with a = gain*(store); maximize EV, identical to tracking optimum.
def corr2(tau, s, g):
    s2 = (g * 1e-3) ** 2 * av; A = 1 / (1 + lam * tau)
    return (s2 * A) ** 2 / (s2 * A + V0 * (t2 / tau) ** (2 - 2 * s)) / s2
d2 = [taus[np.argmax(corr2(taus, s, g))] for s in S for g in GS]
out["D2_gain_bounded_drift"] = dict(memory_s=d2, L=min(d2), U=max(d2), verdict=verdict(min(d2), max(d2)))
# E2
j = np.argmin(abs(taus - t2)); lt = np.log(taus)
req = {}
for k in (1, 2):
    vals = []
    for s in S:
        for g in GS:
            lc = 0.5 * np.log(corr2(taus, s, g)); d = np.gradient(lc, lt)[j]; vals.append(-k * d)
    req[k] = (min(vals), max(vals))
P = (1e3 / 3, 1e3 * 3); budget = (7e5, 6.4e6); B = (0.02, 1.0)
rho = (P[0] / budget[1] / B[1], P[1] / budget[0] / B[0])
def e2v(r):
    if r[1] >= rho[0] and r[0] <= rho[1]: return "CONSISTENT"
    if r[0] > 3 * rho[1] or r[1] < rho[0] / 3: return "EXCLUDED"
    return "MARGINAL"
out["E2_speed_price"] = dict(rho_measured=rho, rho_required_k1=req[1], rho_required_k2=req[2],
                             verdict_k1=e2v(req[1]), verdict_k2=e2v(req[2]),
                             rho_central=1e3 / 2e6 / 0.1)
# H: OU world u = fast (lam) + slow (mu) modes, shares (1-phi, phi); store noise s = 0.31; find (mu, phi) giving 9.9 s.
def ev_two(tau, mu, phi, s, g):
    s2 = (g * 1e-3) ** 2 * av; Af = 1 / (1 + lam * tau); As = 1 / (1 + mu * tau)
    cov_zu = s2 * ((1 - phi) * Af + phi * As)   # Cov(LP u, u)
    # Var(LP u) for OU mode rate r: s2_r/(1+r tau)
    var_z = s2 * ((1 - phi) * Af + phi * As) + V0 * (t2 / tau) ** (2 - 2 * s)
    return cov_zu ** 2 / var_z
grid = []
for mu in (1 / 30, 1 / 60, 1 / 120, 1 / 300):
    for phi in (0.01, 0.03, 0.1, 0.3):
        t = [taus[np.argmax(ev_two(taus, mu, phi, S[1], g))] for g in GS]
        grid.append(dict(mu_inv_s=1 / mu, phi=phi, tau_star=[round(x, 2) for x in t]))
out["H_slow_mode_grid_s031"] = grid
json.dump(out, open(os.path.join(HERE, "d_results.json"), "w"), indent=1, default=float)
for k, v in out.items():
    if k.startswith("H"):
        for r in v: print(r)
    else: print(k, v)
