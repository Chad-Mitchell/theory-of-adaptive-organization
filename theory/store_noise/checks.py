#!/usr/bin/env python3
"""Checks for theory/STORE_NOISE.md (extension E1 store noise, E2 speed-priced upkeep). Run: python3 checks.py
Every assertion here is in-model (one OU mode, first-order stores, static linear read-out of the stores)."""
import json, os
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize, brentq
HERE = os.path.dirname(os.path.abspath(__file__))
out = {}

def ev_single(tau, lam, s2, V0, t0, s):
    A = 1 / (1 + lam * tau)
    return (s2 * A) ** 2 / (s2 * A + V0 * (t0 / tau) ** (2 - 2 * s))

# 1. Closed form at low SNR: lam*tau* = (1-s)/s, checked against the full optimum at SNR -> 0.
lam = 1.0; taus = np.logspace(-3, 4, 200001); rows = []
for s in (0.1, 0.2, 0.31, 0.4, 0.5, 0.6, 0.8):
    t = taus[np.argmax(ev_single(taus, lam, 1e-6, 1.0, 1.0, s))]
    rows.append((s, lam * t, (1 - s) / s)); assert abs(np.log(lam * t / ((1 - s) / s))) < 0.01, (s, t)
out["E1_closed_form_low_snr"] = rows
# 1b. SNR shortens the memory (higher SNR -> faster store) for s = 0.31.
prev = np.inf; rr = []
for s2 in (1e-6, 1e-2, 1e-1, 1, 10):
    t = taus[np.argmax(ev_single(taus, lam, s2, 1.0, 1.0, 0.31))]; rr.append((s2, t)); assert t <= prev * 1.0001; prev = t
out["E1_snr_shortens_memory_s031"] = rr

# 2. Equivalence (s = 1/2, one store): store noise of density N on the store's state, referred to the store input, has
#    the same spectrum as sensing noise of density N on the input: N tau^2/(1+w^2 tau^2) / tau^2 = N/(1+w^2 tau^2).
for tau in (0.3, 1.0, 7.0):
    w = np.logspace(-3, 3, 50); store = (1.0 * tau ** 2 / (1 + (w * tau) ** 2)) / tau ** 2; sense = 1.0 / (1 + (w * tau) ** 2)
    assert np.allclose(store, sense)
out["E1_equivalence_s_half_single_store"] = "spectra identical at 3 tau x 50 frequencies"

# 3. Copies: with independent store noise, the best two stores for one OU mode are two copies at one time constant (no
#    second distinct time constant), and they nearly double the explained variance at low SNR. E. coli-scale numbers.
lamE = 0.862; s2E = (0.2e-3) ** 2 * 157.1; t2 = 9.9; K0 = 1.73 * t2 * t2 / (0.22 + t2); V0E = 0.092 ** 2 / K0 ** 2
def cov(ta, tb):
    f = lambda w: (2 * s2E * lamE / (w * w + lamE * lamE)) * np.real(1 / ((1 + 1j * w * ta) * (1 - 1j * w * tb))) / (2 * np.pi)
    return 2 * quad(f, 0, np.inf, limit=400)[0]
def ev_multi(ts, s):
    C = np.array([[cov(a, b) for b in ts] for a in ts]) + np.diag([V0E * (t2 / a) ** (2 - 2 * s) for a in ts])
    c = np.array([s2E / (1 + lamE * a) for a in ts]); return c @ np.linalg.solve(C, c)
cp = []
for s in (0.1, 0.31, 0.5):
    one = -minimize(lambda p: -ev_multi([np.exp(p[0])], s), [0.0], method="Nelder-Mead").fun
    best = max((minimize(lambda p: -ev_multi(list(np.exp(p)), s), x0, method="Nelder-Mead") for x0 in ([-1, 1], [0, 2], [-2, 0.5])), key=lambda r: -r.fun)
    t = np.exp(best.x); cp.append(dict(s=s, two_store_taus=list(t), gain_over_one=-best.fun / one))
    assert abs(np.log(t[0] / t[1])) < 0.05 and 1.9 < -best.fun / one < 2.0
out["E1_copies_not_new_time_constants"] = cp

# 4. E2 speed-priced upkeep h(tau) = h0 + h1/tau. Low SNR: J(x) = -W x^a/(1+x)^2 + H/x, a = 2-2s, x = lam*tau.
#    Interior optimum solves H/W = x^(a+1) [2x - a(1+x)] / (1+x)^3 > 0, so x* > (1-s)/s whenever h1 > 0. The right side
#    grows without bound for s < 1/2 (any price gives a finite memory) and tends to 1 for s = 1/2 (H/W >= 1: never track).
def hw(x, s):
    a = 2 - 2 * s; return x ** (a + 1) * (2 * x - a * (1 + x)) / (1 + x) ** 3
for s in (0.31, 0.5):
    for HW in ((0.01, 0.1, 1.0) if s < 0.5 else (0.01, 0.1, 0.9)):
        x = brentq(lambda x: hw(x, s) - HW, (1 - s) / s * 1.000001, 1e6)
        xs = np.logspace(-2, 6, 400001); J = -xs ** (2 - 2 * s) / (1 + xs) ** 2 + HW / xs
        assert abs(np.log(xs[np.argmin(J)] / x)) < 0.01 and x > (1 - s) / s
for s in (0.1, 0.244, 0.31, 0.372, 0.49):
    xs = np.logspace(np.log10((1 - s) / s), 5, 20001)[1:]; assert np.all(np.diff(hw(xs, s)) > 0)  # monotone: w up -> memory down
out["E2_monotone_rhs_checked"] = True
out["E2_implied_H_over_W_ecoli_x8p53"] = {f"s={s}": hw(8.53, s) for s in (0.244, 0.31, 0.372, 0.5)}
json.dump(out, open(os.path.join(HERE, "checks.json"), "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=float)); print("ALL STORE_NOISE CHECKS PASS")
