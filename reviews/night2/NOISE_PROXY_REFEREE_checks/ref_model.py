#!/usr/bin/env python3
"""NOISE-PROXY-REFEREE: independent re-implementation (time domain) of the noisy-information forecaster used by
tests/SPF_NOISE_PROXY and tests/LFK_SPF. Imports NOTHING from those folders.

World: sampled Matern + white share; autocovariance gamma(k) = (1-phi) rho(k) + phi delta_k with
rho(t) = 2^(1-nu)/Gamma(nu) (|t|/tau)^nu K_nu(|t|/tau), nu = (alpha-1)/2 (the covariance whose spectral density is
proportional to (1+(nu' tau)^2)^(-alpha/2); sampling at integers = aliasing). Unit variance.
Forecaster i: private y_i = x + v_i (white, var K); optional common public z = x + u (white, var Kc), seen by all.
Forecasts are finite-memory (L lags) MMSE projections solved from the Toeplitz normal equations.
"""
import numpy as np
from scipy.special import kv, gamma as G
from scipy.linalg import solve_toeplitz, toeplitz

L = 600

def acov(tau, alpha, phi, n):
    nu = (alpha - 1) / 2
    t = np.arange(n) / tau
    r = np.ones(n)
    t1 = t[1:]
    r[1:] = 2 ** (1 - nu) / G(nu) * t1 ** nu * kv(nu, t1)
    g = (1 - phi) * r
    g[0] += phi
    return g

class World:
    def __init__(self, tau, alpha, phi, Lm=L):
        self.L = Lm
        self.g = acov(tau, alpha, phi, 2 * Lm + 20)
    def gam(self, d):
        return self.g[np.abs(d)]

def weights_single(W, K, h):
    """weights a_k on y_{t-k}, k=0..L-1, for the MMSE forecast of x_{t+h}."""
    c = W.g[:W.L].copy(); c[0] += K
    r = W.g[h:h + W.L]
    return solve_toeplitz(c, r)

def weights_two(W, K, Kc, h):
    """weights (a on private y, b on public z), both lags 0..L-1."""
    Gm = toeplitz(W.g[:W.L])
    I = np.eye(W.L)
    A = np.block([[Gm + K * I, Gm], [Gm, Gm + Kc * I]])
    r = W.g[h:h + W.L]
    s = np.linalg.solve(A, np.concatenate([r, r]))
    return s[:W.L], s[W.L:]

def disp(K, a, nf):
    return K * (1 - 1 / nf) * float(a @ a)

def cg_beta(W, K, nf, h=3, Kc=None):
    """Consensus CG coefficient Cov(x_{t+h}-F_t, F_t-F_{t-1}) / Var(F_t-F_{t-1}) for target x_{t+h}.
    Consensus = average over nf forecasters; private noise average vbar has var K/nf; public noise u common."""
    if Kc is None:
        a3 = weights_single(W, K, h); a4 = weights_single(W, K, h + 1); b3 = b4 = None
    else:
        a3, b3 = weights_two(W, K, Kc, h); a4, b4 = weights_two(W, K, Kc, h + 1)
    Lm = W.L
    # represent each form as coefficients on x_{t+h-j} for j = 0..Lm+h+1 (j index from the target time)
    n = Lm + h + 2
    def place(w, shift):   # w on lags k of time (t - shift): x_{t-shift-k} -> j = h + shift + k
        out = np.zeros(n); out[h + shift: h + shift + Lm] = w; return out
    # revision R = F_t(x_{t+h}) - F_{t-1}(x_{t+h}); F_{t-1}(x_{t+h}) uses (h+1)-step weights at time t-1
    ax = place(a3, 0) - place(a4, 1)                     # private-signal weights (act on x and on vbar)
    bx = np.zeros(n) if b3 is None else place(b3, 0) - place(b4, 1)
    rx = ax + bx                                          # loading of R on x
    ex = -(place(a3, 0) + (0 if b3 is None else place(b3, 0))); ex[0] += 1.0   # error loading on x
    ev = -place(a3, 0); eu = np.zeros(n) if b3 is None else -place(b3, 0)
    Gm = toeplitz(W.g[:n])
    kn = K / nf
    cov = ex @ Gm @ rx + kn * (ev @ ax) + (0 if Kc is None else Kc * (eu @ bx))
    var = rx @ Gm @ rx + kn * (ax @ ax) + (0 if Kc is None else Kc * (bx @ bx))
    return float(cov / var)

def nowcast_cons_var(W, K, nf, Kc=None, T=None):
    """(population or expected sample (divisor T) variance of the consensus h=0 forecast)."""
    if Kc is None:
        a = weights_single(W, K, 0); b = None
    else:
        a, b = weights_two(W, K, Kc, 0)
    fx = a + (0 if b is None else b)
    n = W.L + (T or 0)
    if T is None:
        Gm = toeplitz(W.g[:W.L])
        return float(fx @ Gm @ fx + K / nf * a @ a + (0 if b is None else Kc * b @ b))
    # expected sample variance over T consecutive t: average consensus = sum over t; use autocov of consensus
    gc = cons_acov(W, a, b, K, nf, Kc, T)
    k = np.arange(1, T)
    return float(gc[0] - (gc[0] + 2 * np.sum((1 - k / T) * gc[1:T])) / T)

def cons_acov(W, a, b, K, nf, Kc, m):
    fx = a + (0 if b is None else b)
    Lm = len(a)
    out = np.zeros(m)
    for d in range(m):
        # cov(f_t, f_{t-d}) = sum_jk fx_j fx_k g(d + k - j) + white parts
        idx = d + np.arange(Lm)[None, :] - np.arange(Lm)[:, None]
        out[d] = fx @ W.gam(idx) @ fx
        if d < Lm:
            out[d] += K / nf * float(a[d:] @ a[:Lm - d]) + (0 if b is None else Kc * float(b[d:] @ b[:Lm - d]))
    return out
