#!/usr/bin/env python3
"""POST HOC exploration (not a test; written after ECOLI-MEM results were known).
World as read by the cell = integrated-OU signal x (u = dx/dt, rate lam) + a slow OU nuisance n
(receptor-array fluctuations; correlation time tau_c = 34 s in cheR cheB deletion cells, Colin et al. 2017)
+ a white read floor r. Target: current u. Report the optimal (Kalman) filter's slowest decay time
as the nuisance variance is scanned. Question asked: does the optimum's slow memory sit between tau_v and tau_c?"""
import json, numpy as np
from scipy.linalg import solve_continuous_are
lam = 0.862; av = 157.1; tau_c = 34.0; gam = 1 / tau_c
out = []
for g_mm in [0.1, 0.4]:
    su2 = (g_mm * 1e-3) ** 2 * av
    for r in [1e-8, 1e-6, 1e-4]:
        for vn in np.logspace(-6, 0, 13):  # nuisance variance in (ln c)^2
            A = np.array([[0, 1, 0], [0, -lam, 0], [0, 0, -gam]])
            C = np.array([[1.0, 0, 1.0]])
            Q = np.diag([0, 2 * lam * su2, 2 * gam * vn])
            P = solve_continuous_are(A.T, C.T, Q, np.array([[r]]))
            L = P @ C.T / r
            ev = np.linalg.eigvals(A - L @ C)
            rates = sorted(-ev.real)
            out.append(dict(g=g_mm, r=r, vn=float(vn), slow_tau=1 / rates[0], all_tau=[1 / x for x in rates]))
json.dump(out, open('nuisance_mode.json', 'w'), indent=1)
for o in out:
    print(o['g'], o['r'], '%.1e' % o['vn'], 'slow %.2f s' % o['slow_tau'], ['%.3g' % t for t in o['all_tau']])
