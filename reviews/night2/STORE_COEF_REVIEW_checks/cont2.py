#!/usr/bin/env python3
"""STORE-COEF-REVIEW: scale-free continuous world S = |w|^-alpha, N = 1. One unit-gain EWMA (closed form, as in coef.py)
vs two EWMAs with free split g, 1-g (unit total gain, needed for finite error at alpha >= 1). Own code; numeric quadrature
in log-frequency. Gives the two-store threshold psi_two = 1/(eps1 - eps2) at |alpha - 2| = 0.05."""
import numpy as np, json
from math import cos, sin, pi
from scipy.optimize import minimize
from numpy.polynomial.legendre import leggauss
x, w = leggauss(40); ed = np.linspace(np.log(1e-12), np.log(1e12), 241)
U = np.concatenate([(b-a)/2*(x+1)+a for a, b in zip(ed[:-1], ed[1:])]); WU = np.concatenate([(b-a)/2*w for a, b in zip(ed[:-1], ed[1:])])
om = np.exp(U); dw = WU*om
def err(lams, gs, a):
    H = sum(g*l/(l+1j*om) for g, l in zip(gs, lams))
    return float(np.sum((np.abs(1-H)**2*om**(-a) + np.abs(H)**2)*dw)/pi)
rows = []
for a in (1.95, 2.05, 1.9, 2.1):
    es = 1/sin(pi/a); A = 1/(-2*cos(pi*a/2)); l1 = (2*(a-1)*A)**(1/a); E1 = l1*a/(2*(a-1))
    E1q = err([l1], [1.0], a)
    f = lambda p: err([np.exp(p[0]), np.exp(p[1])], [p[2], 1-p[2]], a)
    best = min((minimize(f, [np.log(l1)+d1, np.log(l1)+d2, g], method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-15, maxiter=4000))
                for d1 in (-1, 0.5) for d2 in (1, 2.5) for g in (0.3, 0.8, 1.2)), key=lambda o: o.fun)
    e1, e2 = E1/es-1, best.fun/es-1
    rows.append(dict(alpha=a, eps1=e1, eps1_quad=E1q/es-1, eps2=e2, psi_two=1/(e1-e2), params=list(map(float, best.x))))
    print(json.dumps(rows[-1]), flush=True)
json.dump(rows, open("cont2.json", "w"), indent=1)
