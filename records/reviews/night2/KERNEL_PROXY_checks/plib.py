"""Own library for KERNEL-MEASURE-REFEREE proxy-validity checks (pick 33). Imports nothing from tests/KERNEL_MEASURE
or measurement/estimators. Conventions: S(w)=q|w|^-alpha with dw/2pi, variogram q*D1*tau^(alpha-1),
D1 = 1/(Gamma(alpha) sin(pi(alpha-1)/2)) (derived: int_0^inf (1-cos u)u^-alpha du = pi/(2 Gamma(alpha) sin(pi(alpha-1)/2)))."""
import numpy as np
from math import gamma, sin, pi
ALPHA, LNQ, LNS2 = 1.2587, -1.8116, -0.9005      # locked inputs of tests/KERNEL_MEASURE PREREG s.2 (numbers only)
EDGES = [0, 1, 2, 5, 10, 21, 42, 84, 168, 336, 504]
LMAX, H = 504, 21

def D1(a): return 1.0 / (gamma(a) * sin(pi * (a - 1) / 2))

def fgn(n, Hh, rng):
    """Davies-Harte fractional Gaussian noise, unit variance."""
    k = np.arange(n + 1)
    r = 0.5 * (np.abs(k + 1) ** (2 * Hh) - 2 * np.abs(k) ** (2 * Hh) + np.abs(k - 1) ** (2 * Hh))
    c = np.concatenate([r, r[-2:0:-1]]); lam = np.fft.fft(c).real
    lam[lam < 0] = 0
    m = len(c); w = rng.standard_normal(m) + 1j * rng.standard_normal(m)
    return np.fft.fft(np.sqrt(lam / m) * w).real[:n]

def driver(n, rng, a=ALPHA, lnq=LNQ, lns2=LNS2):
    x = np.cumsum(np.sqrt(np.exp(lnq) * D1(a)) * fgn(n, (a - 1) / 2, rng))
    return x, x + np.sqrt(np.exp(lns2)) * rng.standard_normal(n)

def blp_weights(Lw=1000, a=ALPHA, lnq=LNQ, lns2=LNS2, h=H):
    """Intrinsic kriging: weights (age 0..Lw-1) of the best linear predictor of mean(x_{t+1..t+h}) from y_{t-age}."""
    D = np.exp(lnq) * D1(a); s2 = np.exp(lns2)
    t = -np.arange(Lw, dtype=float)                      # age i at time -i
    G = lambda d: -0.5 * D * np.abs(d) ** (a - 1)
    C = G(t[:, None] - t[None, :]) + s2 * np.eye(Lw)
    fut = np.arange(1, h + 1, dtype=float)
    c = G(t[:, None] - fut[None, :]).mean(1)
    M = np.zeros((Lw + 1, Lw + 1)); M[:Lw, :Lw] = C; M[:Lw, Lw] = 1; M[Lw, :Lw] = 1
    sol = np.linalg.solve(M, np.concatenate([c, [1.0]]))
    return sol[:Lw]

def binmat(y):
    """rows t = LMAX-1 .. n-1: [1, bin sums of y_{t-age}]"""
    cs = np.concatenate([[0.0], np.cumsum(y)])
    t = np.arange(LMAX - 1, len(y))
    cols = [np.ones(len(t))]
    for j in range(len(EDGES) - 1):
        lo, hi = EDGES[j], EDGES[j + 1]           # ages lo..hi-1 -> indices t-hi+1 .. t-lo
        cols.append(cs[t - lo + 1] - cs[t - hi + 1])
    return np.stack(cols, 1), t

def W21(beta):
    mass = beta[1:] * np.diff(EDGES); return mass[EDGES.index(21):].sum() / mass.sum()

def fut_mean(v, h=H):
    cs = np.concatenate([[0.0], np.cumsum(v)]); n = len(v)
    out = np.full(n, np.nan); t = np.arange(n - h)
    out[t] = (cs[t + h + 1] - cs[t + 1]) / h
    return out

def ols(X, z):
    ok = np.isfinite(z); return np.linalg.lstsq(X[ok], z[ok], rcond=None)[0]

def ar1(n, phi, sd, rng):
    e = rng.standard_normal(n) * sd * np.sqrt(1 - phi ** 2); u = np.zeros(n); u[0] = rng.standard_normal() * sd
    for i in range(1, n): u[i] = phi * u[i - 1] + e[i]
    return u
