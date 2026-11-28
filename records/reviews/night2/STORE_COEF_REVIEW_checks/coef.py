#!/usr/bin/env python3
"""STORE-COEF-REVIEW (pick 27): reviewer's own re-derivation of the one-store excess constant c in
excess_1 ~ c (alpha-2)^2. Imports nothing from the repo. Independent of c3_layers.py and SPECTRUM_MAP_FIXES_checks:
own quadrature (composite Gauss-Legendre, linear panel near 0 + log panels), weights by a stable real least-squares
(QR on the residual integrand, no c - w.b cancellation), rates by dense grid + bounded Brent (K=1) / grid + Nelder-Mead
multistart (K=2), Wiener floor by Kolmogorov-Szego, cross-checked against an exact Kalman Riccati at alpha=2.

World (same model class as SPECTRUM_MAP Prop. 4, re-implemented): S_x(th) = q (4 sin^2(th/2) + wmin^2)^(-alpha/2),
wmin = 10^-L / tau_c, white noise Nd = tau_c^alpha (crossover near 1/tau_c), q = 1. Estimator: NT free FIR taps
(lags 0..NT-1) + K free-weight EWMA stores 1/(1 - p z^-1). eps_K = (MSE_K - e_opt)/e_opt."""
import numpy as np, json, sys
from scipy.optimize import minimize_scalar, minimize
from numpy.polynomial.legendre import leggauss

def nodes(wmin, npan=60, ng=24):
    x, w = leggauss(ng)
    lo = wmin*1e-2
    T = [(lo/2)*(x+1)]; Wt = [(lo/2)*w]                       # linear panel [0, lo]
    edges = np.linspace(np.log(lo), np.log(np.pi), npan+1)
    for a, b in zip(edges[:-1], edges[1:]):
        u = (b-a)/2*(x+1)+a; T.append(np.exp(u)); Wt.append((b-a)/2*w*np.exp(u))
    return np.concatenate(T), np.concatenate(Wt)

class World:
    def __init__(s, alpha, L, tau_c=4.0, q=1.0, npan=60):
        s.wmin = 10.0**(-L)/tau_c; s.N = tau_c**alpha
        s.th, s.wq = nodes(s.wmin, npan)
        s.S = q*(4*np.sin(s.th/2)**2 + s.wmin**2)**(-alpha/2)
        lns2 = np.sum(np.log(s.S+s.N)*s.wq)/np.pi
        s.eopt = s.N*(1 - s.N/np.exp(lns2))
    def mse(s, lams, NT):
        z = np.exp(-1j*s.th)
        cols = [z**k for k in range(NT)] + [1/(1-np.exp(-l)*z) for l in lams]
        A = np.array(cols).T                                   # G x m
        sS = np.sqrt(s.wq*s.S/np.pi)[:, None]; sN = np.sqrt(s.wq*s.N/np.pi)[:, None]
        # residual r = [sS(1 - A w); sN A w], real & imag stacked; minimize |r|^2 over real w
        M = np.vstack([-(sS*A).real, -(sS*A).imag, (sN*A).real, (sN*A).imag])
        y = np.concatenate([-sS[:, 0], np.zeros(len(s.th)), np.zeros(len(s.th)), np.zeros(len(s.th))])
        scale = np.linalg.norm(M, axis=0); scale[scale == 0] = 1
        w = np.linalg.lstsq(M/scale, -y, rcond=None)[0]/scale
        r = M@w + y
        return float(r@r)

def best1(W, NT):
    f = lambda u: W.mse([np.exp(u)], NT)
    us = np.linspace(np.log(W.wmin/10), np.log(3.0), 161)
    v = [f(u) for u in us]; i = int(np.argmin(v)); i = min(max(i, 1), len(us)-2)
    o = minimize_scalar(f, bounds=(us[i-1], us[i+1]), method="bounded", options=dict(xatol=1e-7))
    return (o.fun-W.eopt)/W.eopt, float(np.exp(o.x))

def best2(W, NT):
    f = lambda u: W.mse(np.exp(u), NT)
    us = np.linspace(np.log(W.wmin/10), np.log(3.0), 28)
    cand = sorted((f([a, b]), a, b) for i, a in enumerate(us) for b in us[i+1:])[:4]
    best = min(minimize(f, [a, b], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-14, maxiter=2000)).fun for _, a, b in cand)
    return (best-W.eopt)/W.eopt

def kalman_check():
    # alpha=2: S = q/(2-2cos th + w^2) is AR(1) with phi solving (1-phi)^2/phi = w^2, innovation var q*phi
    out = []
    for L in (1, 2, 4):
        W = World(2.0, L); w2 = W.wmin**2
        phi = ((2+w2) - np.sqrt((2+w2)**2-4))/2; Qv = phi*1.0; R = W.N
        P = 1.0
        for _ in range(200000):
            Pp = phi*phi*P + Qv; Pn = Pp*R/(Pp+R)
            if abs(Pn-P) < 1e-15*P: break
            P = Pn
        out.append(dict(L=L, kalman=P, kolmogorov=W.eopt, rel=(W.eopt-P)/P, eps1_alpha2=best1(W, 4)[0]))
    return out

if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = {}
    if part in ("all", "kalman"):
        res["kalman"] = kalman_check(); print("kalman", res["kalman"], flush=True)
    if part in ("all", "conv"):
        c = []
        for npan in (30, 60, 120):
            W = World(1.95, 4, npan=npan); e, l = best1(W, 4); c.append(dict(npan=npan, eps1=e, lam=l, eopt=W.eopt))
        res["conv"] = c; print("conv", c, flush=True)
    if part in ("all", "main"):
        rows = []
        for L in (1, 2, 3, 4, 5):
            for a in (1.8, 1.9, 1.95, 1.98, 2.02, 2.05, 2.1, 2.2):
                W = World(a, L); e1, lam = best1(W, 4)
                e2 = best2(W, 4) if abs(a-2) in (0.05,) or a in (1.95, 2.05) else None
                row = dict(L=L, alpha=a, eps1=e1, lam=lam, c=e1/(a-2)**2, eps2=e2,
                           psi_two=(1/(e1-e2) if e2 is not None else None))
                rows.append(row); print(json.dumps(row), flush=True)
        res["main"] = rows
    if part in ("all", "model"):
        rows = []
        for NT in (0, 1, 2, 4, 8):
            for tc in (2.0, 4.0, 16.0):
                for a in (1.9, 2.1):
                    W = World(a, 3, tau_c=tc); e1, lam = best1(W, NT)
                    rows.append(dict(NT=NT, tau_c=tc, L=3, alpha=a, eps1=e1, c=e1/(a-2)**2)); print(json.dumps(rows[-1]), flush=True)
        res["model"] = rows
    if part in ("all", "cont"):
        from math import cos, sin, pi
        rows = []
        for a in (1.8, 1.9, 1.95, 1.99, 1.999, 2.001, 2.01, 2.05, 2.1, 2.2):
            A = 1/(-2*cos(pi*a/2)); N = 1.0
            lam = (2*(a-1)*A/N)**(1/a); E = lam*N*a/(2*(a-1)); es = 1/sin(pi/a)
            rows.append(dict(alpha=a, eps1=E/es-1, c=(E/es-1)/(a-2)**2))
        res["cont"] = rows; print("cont", rows, flush=True)
    json.dump(res, open(f"coef_{part}.json", "w"), indent=1)
