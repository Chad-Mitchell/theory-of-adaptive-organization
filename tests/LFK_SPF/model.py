#!/usr/bin/env python3
"""LFK-ALPHA-SPF in-model instrument: environment spectrum, Whittle fit, optimal (Wiener) forecaster, CG coefficient.

World (quarterly, unit variance): S(w) = (1-phi)*S_mat(w; tauE, alpha) + phi, w in [-pi, pi], where S_mat is the
aliased sample of the continuous unit-variance spectrum c_a*tauE*(1+(nu*tauE)^2)^(-alpha/2), c_a = 2*pi/B(1/2,(alpha-1)/2)
(THEORY §2.5 / SPECTRUM_MAP Prop. 5 environment; phi = white share, a transitory component).
Forecasters: each sees y_i = x + v_i, v_i white with variance K (in units of var x: assumption A1); each forms the
causal MMSE (Wiener) forecast; the consensus averages out v_i, so the consensus forecast is the individual filter
applied to x. CG coefficient: beta = Cov(x_{t+3}-F_t x_{t+3}, F_t x_{t+3}-F_{t-1} x_{t+3}) / Var(revision).
"""
import numpy as np
from scipy.special import beta as Bfun
from scipy.optimize import minimize

M = 2 ** 13                       # frequency grid for filters
KALIAS = 30                       # aliasing terms each side (+ integral tail)

def s_mat_cont(nu, tauE, alpha):
    ca = 2 * np.pi / Bfun(0.5, (alpha - 1) / 2)
    return ca * tauE * (1 + (nu * tauE) ** 2) ** (-alpha / 2)

def s_mat_disc(w, tauE, alpha):
    k = np.arange(-KALIAS, KALIAS + 1)
    tot = s_mat_cont(w[:, None] + 2 * np.pi * k[None, :], tauE, alpha).sum(1)
    # tail beyond KALIAS by integral approximation (both sides)
    ca = 2 * np.pi / Bfun(0.5, (alpha - 1) / 2)
    L = 2 * np.pi * (KALIAS + 0.5)
    tail = 2 * ca * tauE ** (1 - alpha) * L ** (1 - alpha) / ((alpha - 1) * 2 * np.pi)
    return tot + tail

def spectrum(w, tauE, alpha, phi):
    return (1 - phi) * s_mat_disc(w, tauE, alpha) + phi

# ---------------- Whittle fit ----------------
def periodogram(x):
    x = np.asarray(x, float); x = x - x.mean(); n = len(x)
    I = np.abs(np.fft.fft(x)) ** 2 / n
    j = np.arange(1, (n - 1) // 2 + 1)
    return 2 * np.pi * j / n, I[j]

BOUNDS = dict(logtau=(np.log(0.05), np.log(5000.0)), alpha=(1.02, 6.0), phi=(0.0, 0.98))

def _unpack(p):
    lt = np.clip(p[0], *BOUNDS["logtau"]); a = np.clip(p[1], *BOUNDS["alpha"]); ph = np.clip(p[2], *BOUNDS["phi"])
    pen = 1e3 * ((p[0] - lt) ** 2 + (p[1] - a) ** 2 + (p[2] - ph) ** 2)
    return np.exp(lt), a, ph, pen

def whittle_fit(x, starts=None):
    w, I = periodogram(x)
    def nll(p):
        tau, a, ph, pen = _unpack(p)
        S = spectrum(w, tau, a, ph)
        s2 = np.mean(I / S)                       # profiled variance
        return np.sum(np.log(s2 * S)) + len(w) + pen
    if starts is None:
        starts = [(lt, a, ph) for lt in np.log([0.7, 4, 25, 150]) for a in (1.6, 2.6) for ph in (0.1, 0.5)]
    best = None
    for s in starts:
        r = minimize(nll, np.array(s, float), method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-6, maxiter=4000))
        if best is None or r.fun < best.fun: best = r
    tau, a, ph, _ = _unpack(best.x)
    return dict(tauE=float(tau), alpha=float(a), phi=float(ph), nll=float(best.fun))

def simulate(n, tauE, alpha, phi, rng, burn=4):
    """Gaussian series with the model spectrum (unit variance) by circulant embedding on a long grid."""
    L = 2 ** int(np.ceil(np.log2(n * burn)))
    w = 2 * np.pi * np.fft.fftfreq(L)
    S = spectrum(np.abs(w), tauE, alpha, phi)
    z = (rng.standard_normal(L) + 1j * rng.standard_normal(L))
    x = np.fft.fft(z * np.sqrt(S / L)).real
    return x[:n]

# ---------------- optimal forecaster and CG coefficient ----------------
_W = 2 * np.pi * np.arange(M) / M
_Wsym = np.where(_W > np.pi, _W - 2 * np.pi, _W)

def env_grid(tauE, alpha, phi):
    S = spectrum(np.abs(_Wsym), tauE, alpha, phi)
    return S / np.mean(S)                         # unit variance on the grid

def cg_beta(S, K, h=3):
    """S: unit-variance spectrum on the grid; K: noise variance. Returns (beta, gain_like) for target t+h."""
    Sy = S + K
    c = np.fft.ifft(np.log(Sy)).real              # cepstrum
    cp = np.zeros(M); cp[0] = c[0] / 2; cp[1:M // 2] = c[1:M // 2]
    Phi = np.exp(np.fft.fft(cp))                  # minimum-phase factor, Sy = |Phi|^2
    def H(m):
        G = S * np.exp(1j * _W * m) / np.conj(Phi)
        g = np.fft.ifft(G); g[M // 2:] = 0        # causal part (lags >= 0)
        return np.fft.fft(g) / Phi
    Hh, Hh1 = H(h), H(h + 1)
    E = np.exp(1j * _W * h) - Hh
    R = Hh - np.exp(-1j * _W) * Hh1
    cov = np.mean(S * (E * np.conj(R)).real)
    var = np.mean(S * np.abs(R) ** 2)
    return cov / var

def innovation_var(S):
    return float(np.exp(np.mean(np.log(S))))

def beta_model(tauE, alpha, phi, K, noise="var"):
    S = env_grid(tauE, alpha, phi)
    Kn = K if noise == "var" else K * innovation_var(S)
    return cg_beta(S, Kn)

# ---------------- forecaster moments used for identification ----------------
def _factor(S, K):
    c = np.fft.ifft(np.log(S + K)).real
    cp = np.zeros(M); cp[0] = c[0] / 2; cp[1:M // 2] = c[1:M // 2]
    return np.exp(np.fft.fft(cp))

def filters(S, K, h=3):
    Phi = _factor(S, K)
    def H(m):
        G = S * np.exp(1j * _W * m) / np.conj(Phi)
        g = np.fft.ifft(G); g[M // 2:] = 0
        return np.fft.fft(g) / Phi
    return H(h), H(h + 1)

def moments(S, K, h=3, nf=np.inf):
    """In-model (beta, D/vf) for a consensus of nf forecasters, each seeing y_i = x + v_i (var v = K) and using the
    Wiener filter. Consensus = H*(x + vbar), var vbar = K/nf (finite-panel noise is kept: it biases beta down).
    D = cross-forecaster variance of F_i(t+h) = K*(1-1/nf)*mean|H_h|^2; vf = time variance of the consensus forecast."""
    Hh, Hh1 = filters(S, K, h)
    E = np.exp(1j * _W * h) - Hh; R = Hh - np.exp(-1j * _W) * Hh1
    kn = 0.0 if not np.isfinite(nf) else K / nf
    cov = np.mean(S * (E * np.conj(R)).real) + kn * np.mean((-Hh * np.conj(R)).real)
    var = np.mean((S + kn) * np.abs(R) ** 2)
    D = K * (1 - (0.0 if not np.isfinite(nf) else 1 / nf)) * np.mean(np.abs(Hh) ** 2)
    vf = np.mean((S + kn) * np.abs(Hh) ** 2)
    return float(cov / var), float(D / vf)

def invert_ratio(S, ratio, lo=1e-4, hi=1e4, it=40, nf=np.inf):
    """Solve D/vf(K) = ratio for K by bisection on log K (D/vf is increasing in K; checked in checks_model)."""
    a, b = np.log(lo), np.log(hi)
    ra, rb = moments(S, lo, nf=nf)[1], moments(S, hi, nf=nf)[1]
    if ratio <= ra: return lo, "low_bound"
    if ratio >= rb: return hi, "high_bound"
    for _ in range(it):
        m = 0.5 * (a + b)
        if moments(S, np.exp(m), nf=nf)[1] < ratio: a = m
        else: b = m
    return float(np.exp(0.5 * (a + b))), "ok"
