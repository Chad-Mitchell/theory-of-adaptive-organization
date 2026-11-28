#!/usr/bin/env python3
"""SPF-NOISE-PROXY shared code: horizon-h noisy-information moments, fast K inversion, synthetic panels.

Model (THEORY v1.4.1 §2.2, memory-time row premise "white observation noise"; implemented in ../LFK_SPF/model.py):
unit-variance world with spectrum S; forecaster i sees y_i = x + v_i, v_i white, var K (units of var x), and reports the
causal Wiener forecast of x_{t+h}. Cross-forecaster dispersion D(h) = K(1-1/n) mean|H_h|^2; consensus time variance
vf(h) = mean((S+K/n)|H_h|^2). Ratio r(h; K) = D/vf is inverted for K at each horizon (K-hat(h)).
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "LFK_SPF"))
import model  # noqa: E402

KGRID = np.exp(np.linspace(np.log(1e-4), np.log(1e3), 57))
HORIZONS = (0, 1, 2, 3, 4)

def fejer(T):
    """sin^2(T w/2) / (T^2 sin^2(w/2)) on the model grid (= Var(sample mean) weight); 1 at w = 0."""
    w = model._W
    with np.errstate(invalid="ignore", divide="ignore"):
        f = np.sin(T * w / 2) ** 2 / (T ** 2 * np.sin(w / 2) ** 2)
    f[0] = 1.0
    return f

def moments_T(S, K, h, nf, T=None):
    """(D, vf) with vf the EXPECTED sample variance (divisor T) of the consensus over T consecutive surveys
    (T=None: population variance, as in ../LFK_SPF/model.moments)."""
    Hh = model.filters(S, K, h)[0]
    kn = 0.0 if not np.isfinite(nf) else K / nf
    D = K * (1 - (0.0 if not np.isfinite(nf) else 1 / nf)) * np.mean(np.abs(Hh) ** 2)
    SF = (S + kn) * np.abs(Hh) ** 2
    vf = np.mean(SF) if T is None else np.mean(SF * (1 - fejer(T)))
    return float(D), float(vf)

def ratio_curve(S, h, nf, T=None):
    out = []
    for K in KGRID:
        D, vf = moments_T(S, K, h, nf, T)
        out.append(D / vf)
    return np.array(out)

def invert(curve, ratio):
    """log-linear interpolation of K on a monotone ratio curve; returns (K, flag)."""
    lc = np.log(np.maximum(curve, 1e-300))
    if not np.all(np.diff(lc) > 0):
        raise ValueError("ratio curve not monotone")
    lr = np.log(max(ratio, 1e-300))
    if lr <= lc[0]: return float(KGRID[0]), "low_bound"
    if lr >= lc[-1]: return float(KGRID[-1]), "high_bound"
    return float(np.exp(np.interp(lr, lc, np.log(KGRID)))), "ok"

def level_curve(S, h, nf):
    """D(K)/var_x on KGRID (unit-variance world): K (1-1/n) mean|H_h|^2. Not monotone: rises to a peak, then falls
    (very noisy forecasters ignore their signal). Inverted on the LOWER branch only."""
    return np.array([moments_T(S, K, h, nf)[0] for K in KGRID])

def invert_lower(curve, val):
    i = int(np.argmax(curve)); c = curve[:i + 1]; g = KGRID[:i + 1]
    if val >= c[-1]: return float(g[-1]), "above_noise_max"
    if val <= c[0]: return float(g[0]), "low_bound"
    return float(np.exp(np.interp(np.log(val), np.log(c), np.log(g)))), "ok"

def env_scale(x, fit):
    """Population variance of x implied by the Whittle fit: profiled s^2 times the grid mean of the unnormalised spectrum."""
    w, I = model.periodogram(x)
    Sw = model.spectrum(w, fit["tauE"], fit["alpha"], fit["phi"])
    s2 = np.mean(I / Sw)
    return float(s2 * np.mean(model.spectrum(np.abs(model._Wsym), fit["tauE"], fit["alpha"], fit["phi"])))

def beta_at(S, K, nf, h=3):
    return model.moments(S, K, h=h, nf=nf)[0]

def rvar(a):
    a = np.asarray(a, float)
    q75, q25 = np.percentile(a, [75, 25])
    return ((q75 - q25) / 1.349) ** 2

# ---------------- dispersion statistics from a panel ----------------
def panel_stats(F, act, h, min_n=10, min_spell=8):
    """F: array (T, P) of forecasts at horizon h (NaN when inactive); act: bool (T, P).
    Returns dict with D_raw (mean over surveys of robust variance), D_within (same after removing each forecaster's
    own mean deviation from consensus, forecasters with >= min_spell surveys), vf (time variance of consensus)."""
    T, P = F.shape
    cons = np.nanmean(np.where(act, F, np.nan), axis=1)
    dev = F - cons[:, None]
    nobs = act.sum(0)
    fe = np.array([np.nanmean(dev[act[:, i], i]) if nobs[i] > 0 else np.nan for i in range(P)])
    Draw, Dw, keep = [], [], []
    for t in range(T):
        a = act[t]
        if a.sum() < min_n: continue
        keep.append(t)
        Draw.append(rvar(F[t, a]))
        b = a & (nobs >= min_spell)
        if b.sum() >= min_n:
            Dw.append(rvar(dev[t, b] - fe[b]))
    keep = np.array(keep)
    return dict(D_raw=float(np.mean(Draw)), D_within=float(np.mean(Dw)) if Dw else np.nan,
                vf=float(np.var(cons[keep])), nf=float(np.median(act[keep].sum(1))), n=len(keep))

# ---------------- synthetic panels ----------------
def impulse(Hh, L=600):
    g = np.fft.ifft(Hh).real[:L]
    return g

def causal_filter(g, y):
    n = len(y)
    m = 1 << int(np.ceil(np.log2(n + len(g))))
    return np.fft.irfft(np.fft.rfft(y, m) * np.fft.rfft(g, m), m)[:n]

def synth_panel(env, K, arm, lam, rng, T=200, active=35, spell=20, burn=800, n_env=240):
    """Simulate one SPF-like panel. arm: 'a' pure noise; 'b' fixed individual long-run-mean bias; 'c' heterogeneous
    dynamics (each forecaster designs its Wiener filter for tauE*exp(0.5 z)); 'd' AR(1) individual bias (rho 0.8).
    lam: heterogeneity variance in units of the pure-noise h=3 dispersion K*mean|H_3|^2 (arms b, d).
    Horizon loading of biases: (0.3 + 0.7*h/4) (non-zero at h=0, so no proxy is uncontaminated by construction).
    Returns {h: (F (T,P), act (T,P))}."""
    tau, al, ph = env["tauE"], env["alpha"], env["phi"]
    S = model.env_grid(tau, al, ph)
    n = T + burn + 8
    x = model.simulate(n, tau, al, ph, rng)
    x = x / np.sqrt(np.mean(S))  # env_grid normalises S to unit variance; simulate is unit-variance up to grid
    P = int(active * T / spell) + active
    starts = rng.integers(-spell, T, P); lens = rng.geometric(1 / spell, P)
    act = np.zeros((T, P), bool)
    for i in range(P):
        a, b = max(starts[i], 0), min(starts[i] + lens[i], T)
        if b > a: act[a:b, i] = True
    filt = {h: impulse(model.filters(S, K, h)[0]) for h in HORIZONS}
    D3 = K * np.mean(np.abs(model.filters(S, K, 3)[0]) ** 2)
    sb = np.sqrt(lam * D3)
    out = {h: np.full((T, P), np.nan) for h in HORIZONS}
    bias_fixed = rng.standard_normal(P) * sb
    for i in range(P):
        if not act[:, i].any(): continue
        y = x + rng.standard_normal(n) * np.sqrt(K)
        if arm == "c":
            Si = model.env_grid(tau * np.exp(0.5 * rng.standard_normal()), al, ph)
            fi = {h: impulse(model.filters(Si, K, h)[0]) for h in HORIZONS}
        else:
            fi = filt
        if arm == "d":
            e = rng.standard_normal(n) * sb * np.sqrt(1 - 0.8 ** 2); bi = np.zeros(n)
            bi[0] = rng.standard_normal() * sb
            for t in range(1, n): bi[t] = 0.8 * bi[t - 1] + e[t]
            bi = bi[burn:burn + T]
        elif arm == "b":
            bi = np.full(T, bias_fixed[i])
        else:
            bi = np.zeros(T)
        for h in HORIZONS:
            f = causal_filter(fi[h], y)[burn:burn + T]
            out[h][:, i] = np.where(act[:, i], f + bi * (0.3 + 0.7 * h / 4), np.nan)
    xenv = x[burn + T - n_env: burn + T]
    return {h: (out[h], act) for h in HORIZONS}, xenv
