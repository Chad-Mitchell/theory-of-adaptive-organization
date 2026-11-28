"""AQN-ESTIMATORS library (QUEUE AQN-ESTIMATORS, pick 11). Estimators for the inputs of THEORY v1.4.3 §2.1/§2.2:
alpha (drift-spectrum slope over a stated band), q (drift level, S(w) = q|w|^-alpha, two-sided, continuous time),
N (white sensing-noise density; sampled at step dt with per-sample variance s2, N = s2*dt), plus, for switching
worlds, jump rate lam and jump size mu (two-state, levels m +/- mu, rate lam each way; q = 4 lam mu^2), and event-world
versions (binned counts; Poisson floor). Stakes: error-cost-curve regression (separate module section).

Conventions. Continuous signal s(t) with two-sided spectral density S(w) = q|w|^-alpha, 1 < alpha < 3 (fBm with
H = (alpha-1)/2); variogram D(tau) = int S(w)(2-2cos w tau) dw/2pi = q tau^(alpha-1) / (Gamma(alpha) sin(pi(alpha-1)/2)).
Observed y_t = s(t) + e_t, t = 1..n (dt = 1), e_t iid N(0, s2). Increments d_t = y_t - y_{t-1} have spectral density
(var = int_{-pi}^{pi} f) f(w) = (4 sin^2(w/2)/2pi) [ q sum_k |w + 2 pi k|^-alpha + s2 ].
"""
import numpy as np
from math import gamma as G, sin, pi, log
from scipy.optimize import minimize
from scipy.special import gammaln
import numba

EULER = 0.5772156649015329

# ---------------------------------------------------------------- generators
def fgn(n, H, rng):
    """Exact fGn (unit variance) by Davies-Harte circulant embedding."""
    k = np.arange(n + 1)
    r = 0.5 * (np.abs(k + 1) ** (2 * H) - 2 * np.abs(k) ** (2 * H) + np.abs(k - 1) ** (2 * H))
    c = np.concatenate([r, r[-2:0:-1]])
    lam = np.fft.fft(c).real
    if lam.min() < -1e-8:
        raise ValueError("embedding not PSD")
    lam = np.clip(lam, 0, None)
    m = len(c)
    z = rng.standard_normal(m) + 1j * rng.standard_normal(m)
    w = np.fft.fft(np.sqrt(lam / m) * z)
    return w.real[:n]

def D1(alpha):
    return 1.0 / (G(alpha) * sin(pi * (alpha - 1) / 2))

def powerlaw_signal(n, alpha, q, rng):
    """Sampled s(t) with S = q|w|^-alpha (fBm, H=(alpha-1)/2), s(0)=0."""
    H = (alpha - 1) / 2
    return np.cumsum(np.sqrt(q * D1(alpha)) * fgn(n, H, rng))

def ou_mixture(n, corners, weights, rng, burn=None):
    """Sum of exactly discretised OU processes: corner w0 (rad/step), stationary variance weight."""
    out = np.zeros(n)
    for w0, v in zip(corners, weights):
        phi = np.exp(-w0)
        innov = np.sqrt(v * (1 - phi ** 2))
        e = rng.standard_normal(n) * innov
        x = np.empty(n); x0 = rng.standard_normal() * np.sqrt(v)
        out += _ar1(phi, e, x0)
    return out

@numba.njit(cache=True)
def _ar1(phi, e, x0):
    x = np.empty(e.size); prev = x0
    for t in range(e.size):
        prev = phi * prev + e[t]; x[t] = prev
    return x

def ou_mixture_spec(w, corners, weights):
    """Exact spectral density (var = int_{-pi}^{pi}) of the sum of discretised OU (AR(1)) processes."""
    f = np.zeros_like(w)
    for w0, v in zip(corners, weights):
        phi = np.exp(-w0)
        f += v * (1 - phi ** 2) / (2 * pi * (1 - 2 * phi * np.cos(w) + phi ** 2))
    return f

def telegraph(n, lam, mu, rng, m=0.0):
    p = (1 - np.exp(-2 * lam)) / 2
    flips = rng.random(n) < p
    s0 = 1 if rng.random() < 0.5 else -1
    sgn = s0 * np.where(np.cumsum(flips) % 2 == 0, 1, -1)
    return m + mu * sgn

# ---------------------------------------------------------------- spectral model
KTRUNC = 6
def alias_sum(w, alpha):
    """sum_k |w + 2 pi k|^-alpha for w in (0, pi], with Euler-Maclaurin midpoint tails."""
    s = w ** -alpha
    for k in range(1, KTRUNC + 1):
        s = s + (w + 2 * pi * k) ** -alpha + (2 * pi * k - w) ** -alpha
    a1 = alpha - 1
    s = s + ((w + 2 * pi * (KTRUNC + 0.5)) ** -a1 + (2 * pi * (KTRUNC + 0.5) - w) ** -a1) / (2 * pi * a1)
    return s

def periodogram(d):
    n = d.size
    F = np.fft.rfft(d - d.mean())
    I = (np.abs(F) ** 2) / (2 * pi * n)
    w = 2 * pi * np.arange(F.size) / n
    keep = (w > 0) & (w < pi)  # drop 0 and Nyquist
    return w[keep], I[keep]

def f_incr(w, logq, alpha, logs2):
    return (4 * np.sin(w / 2) ** 2 / (2 * pi)) * (np.exp(logq) * alias_sum(w, alpha) + np.exp(logs2))

def _grad_logf(w, th, h=1e-5):
    g = []
    for i in range(len(th)):
        tp = np.array(th, float); tm = tp.copy(); tp[i] += h; tm[i] -= h
        g.append((np.log(f_incr(w, *tp)) - np.log(f_incr(w, *tm))) / (2 * h))
    return np.array(g)

def whittle_fit(y, band=None, fix_logs2=None, alpha_bounds=(1.02, 2.98), starts=None):
    """Whittle MLE of (log q, alpha, log s2) on the increments of y over frequency band (lo, hi) in rad/step.
    Returns dict with estimates, Wald SEs from the expected Whittle information sum_j grad log f grad log f^T,
    and flags. fix_logs2: hold the noise floor fixed (event worlds under the Poisson premise)."""
    d = np.diff(y)
    w, I = periodogram(d)
    if band is not None:
        sel = (w >= band[0]) & (w <= band[1]); w, I = w[sel], I[sel]
    def nll(p):
        if fix_logs2 is None:
            lq, a, ls = p
        else:
            lq, a = p; ls = fix_logs2
        f = f_incr(w, lq, a, ls)
        return np.sum(np.log(f) + I / f)
    v0 = np.var(d)
    best = None
    for a0 in (starts or (1.3, 2.0, 2.6)):
        for nf in (0.1, 0.5, 0.9):
            lq0 = log(max(v0 * (1 - nf), 1e-12) / D1(a0)); ls0 = log(max(v0 * nf / 2, 1e-12))
            x0 = [lq0, a0, ls0] if fix_logs2 is None else [lq0, a0]
            bnds = [(lq0 - 25, lq0 + 25), alpha_bounds] + ([(ls0 - 30, ls0 + 15)] if fix_logs2 is None else [])
            r = minimize(nll, x0, method="L-BFGS-B", bounds=bnds)
            if best is None or r.fun < best.fun:
                best = r
    p = best.x
    th = list(p) if fix_logs2 is None else [p[0], p[1], fix_logs2]
    gr = _grad_logf(w, th)
    if fix_logs2 is not None:
        gr = gr[:2]
    info = gr @ gr.T
    try:
        cov = np.linalg.inv(info)
    except np.linalg.LinAlgError:
        cov = np.full(info.shape, np.nan)
    se = np.sqrt(np.clip(np.diag(cov), 0, None))
    out = {"logq": th[0], "alpha": th[1], "logs2": th[2], "se_logq": se[0], "se_alpha": se[1],
           "se_logs2": (se[2] if fix_logs2 is None else 0.0), "nll": best.fun, "nfreq": w.size,
           "at_bound": bool(abs(th[1] - alpha_bounds[0]) < 1e-3 or abs(th[1] - alpha_bounds[1]) < 1e-3),
           "cov": cov.tolist()}
    # crossover frequency where signal = noise (identifiability diagnostic)
    out["w_cross"] = float(np.exp((th[0] - th[2]) / th[1])) if th[1] > 0 else np.nan
    return out

def whittle_corner_fit(y, band=None):
    """Alternative with a low-frequency corner: S = q (w^2 + w0^2)^(-alpha/2) (alias sum, same noise model).
    Used for the regime check (pure power law over the band vs a corner inside it)."""
    d = np.diff(y)
    w, I = periodogram(d)
    if band is not None:
        sel = (w >= band[0]) & (w <= band[1]); w, I = w[sel], I[sel]
    def fc(lq, a, ls, lw0):
        w0 = np.exp(lw0)
        s = (w ** 2 + w0 ** 2) ** (-a / 2)
        for k in range(1, KTRUNC + 1):
            s = s + ((w + 2 * pi * k) ** 2 + w0 ** 2) ** (-a / 2) + ((2 * pi * k - w) ** 2 + w0 ** 2) ** (-a / 2)
        return (4 * np.sin(w / 2) ** 2 / (2 * pi)) * (np.exp(lq) * s + np.exp(ls))
    def nll(p):
        f = fc(*p); return np.sum(np.log(f) + I / f)
    base = whittle_fit(y, band)
    best = None
    for lw0 in np.log(np.geomspace(max(w[0], 1e-4), w[-1] / 3, 6)):
        r = minimize(nll, [base["logq"], max(base["alpha"], 1.5), base["logs2"], lw0], method="L-BFGS-B",
                     bounds=[(base["logq"] - 25, base["logq"] + 25), (0.2, 6.0), (base["logs2"] - 30, base["logs2"] + 15),
                             (np.log(w[0]) - 3, np.log(w[-1]))])
        if best is None or r.fun < best.fun:
            best = r
    return {"nll": best.fun, "logq": best.x[0], "alpha": best.x[1], "logs2": best.x[2], "w0": float(np.exp(best.x[3])),
            "LR": float(2 * (base["nll"] - best.fun)), "base": base}

def pseudo_true(fspec_incr, n, band=None):
    """Whittle pseudo-true (log q, alpha, log s2): minimiser of sum_j log f_th + f_true/f_th over the n-point grid."""
    w = 2 * pi * np.arange(1, n // 2) / n
    if band is not None:
        w = w[(w >= band[0]) & (w <= band[1])]
    ft = fspec_incr(w)
    def kl(p):
        f = f_incr(w, *p); return np.sum(np.log(f) + ft / f)
    best = None
    for a0 in (1.2, 1.6, 2.0, 2.5):
        r = minimize(kl, [0.0, a0, -2.0], method="L-BFGS-B", bounds=[(-30, 30), (1.02, 2.98), (-40, 15)])
        if best is None or r.fun < best.fun:
            best = r
    return best.x

# ---------------------------------------------------------------- comparators
def dfa_alpha(y, scales=None):
    """DFA-1 on the increment series (profile = y - mean-adjusted cumsum of d); alpha = 2*h_DFA + 1."""
    d = np.diff(y); prof = np.cumsum(d - d.mean()); n = prof.size
    if scales is None:
        scales = np.unique(np.geomspace(8, n // 8, 14).astype(int))
    F = []
    for s in scales:
        m = n // s; seg = prof[: m * s].reshape(m, s); t = np.arange(s)
        A = np.vstack([t, np.ones(s)]).T
        coef, *_ = np.linalg.lstsq(A, seg.T, rcond=None)
        res = seg.T - A @ coef
        F.append(np.sqrt(np.mean(res ** 2)))
    h = np.polyfit(np.log(scales), np.log(F), 1)[0]
    return 2 * h + 1

def variogram_nugget(y, taus=None):
    """Fit D(tau) = 2 s2 + c tau^(alpha-1) by least squares on log D; returns (alpha, q, s2)."""
    n = y.size
    if taus is None:
        taus = np.unique(np.geomspace(1, n // 20, 20).astype(int))
    Dh = np.array([np.mean((y[t:] - y[:-t]) ** 2) for t in taus])
    def loss(p):
        a, lc, ls = p
        m = 2 * np.exp(ls) + np.exp(lc) * taus ** (a - 1)
        return np.sum((np.log(m) - np.log(Dh)) ** 2)
    best = None
    for a0 in (1.3, 2.0, 2.6):
        r = minimize(loss, [a0, np.log(Dh[-1] / taus[-1] ** (a0 - 1)), np.log(Dh[0] / 4)], method="L-BFGS-B",
                     bounds=[(1.02, 2.98), (-40, 40), (-40, 40)])
        if best is None or r.fun < best.fun:
            best = r
    a, lc, ls = best.x
    return a, np.exp(lc) / D1(a), np.exp(ls)

# ---------------------------------------------------------------- switching world: HMM vs Gaussian (OU) null
@numba.njit(cache=True)
def hmm_nll(y, m, mu, p, s2):
    """Two-state Gaussian HMM, levels m-mu, m+mu, symmetric switch prob p per step; scaled forward algorithm."""
    a0 = 0.5; a1 = 0.5; ll = 0.0; c = 1.0 / np.sqrt(2 * np.pi * s2)
    for t in range(y.size):
        if t > 0:
            b0 = a0 * (1 - p) + a1 * p; b1 = a1 * (1 - p) + a0 * p; a0 = b0; a1 = b1
        e0 = c * np.exp(-0.5 * (y[t] - (m - mu)) ** 2 / s2); e1 = c * np.exp(-0.5 * (y[t] - (m + mu)) ** 2 / s2)
        a0 *= e0; a1 *= e1; z = a0 + a1
        if z <= 0:
            return 1e300
        ll += np.log(z); a0 /= z; a1 /= z
    return -ll

@numba.njit(cache=True)
def ou_nll(y, m, phi, v, s2):
    """Exact Gaussian likelihood of AR(1) (stationary var v, coefficient phi) + white noise s2, Kalman filter."""
    x = m; P = v; ll = 0.0; Q = v * (1 - phi * phi)
    for t in range(y.size):
        if t > 0:
            x = m + phi * (x - m); P = phi * phi * P + Q
        S = P + s2; r = y[t] - x
        ll += -0.5 * (np.log(2 * np.pi * S) + r * r / S)
        K = P / S; x = x + K * r; P = (1 - K) * P
    return -ll

def _sig(x):
    return 1 / (1 + np.exp(-x))

def _hess(f, x, h=1e-4):
    k = len(x); H = np.zeros((k, k)); x = np.asarray(x, float)
    for i in range(k):
        for j in range(i, k):
            ei = np.zeros(k); ej = np.zeros(k); ei[i] = h; ej[j] = h
            H[i, j] = H[j, i] = (f(x + ei + ej) - f(x + ei - ej) - f(x - ei + ej) + f(x - ei - ej)) / (4 * h * h)
    return H

def hmm_fit(y):
    """MLE of (m, mu, lam, s2) for a sampled symmetric telegraph + white noise. lam per step from p = (1-e^{-2 lam})/2.
    Returns estimates, Wald SEs on (m, log mu, log lam, log s2), and the implied q = 4 lam mu^2, N = s2 (dt=1),
    kappa = lam N / mu^2 and the Bayes adaptation time t_A = (N/2mu^2)[ln(2mu^2/(lam N)) - gamma - 1] with delta-method SE."""
    y = np.asarray(y, float)
    def nll(th):
        m, lmu, llam, ls2 = th
        lam = np.exp(llam); p = (1 - np.exp(-2 * lam)) / 2
        return hmm_nll(y, m, np.exp(lmu), p, np.exp(ls2))
    v = np.var(y); med = np.median(y); best = None
    for fmu in (0.4, 0.7, 0.95):
        for lam0 in (0.002, 0.02, 0.1):
            mu0 = np.sqrt(v) * fmu; s20 = max(v - mu0 ** 2, v * 0.02)
            r = minimize(nll, [med, np.log(mu0), np.log(lam0), np.log(s20)], method="Nelder-Mead",
                         options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 4000})
            if best is None or r.fun < best.fun:
                best = r
    th = best.x
    H = _hess(nll, th)
    try:
        cov = np.linalg.inv(H)
    except np.linalg.LinAlgError:
        cov = np.full((4, 4), np.nan)
    m, lmu, llam, ls2 = th
    mu, lam, s2 = np.exp(lmu), np.exp(llam), np.exp(ls2)
    kap = lam * s2 / mu ** 2
    L = np.log(2 * mu ** 2 / (lam * s2))
    tA = (s2 / (2 * mu ** 2)) * (L - EULER - 1)
    # gradient of log tA wrt (lmu, llam, ls2)
    g = np.zeros(4)
    dL = np.array([0, 2.0, -1.0, -1.0])
    dpre = np.array([0, -2.0, 0.0, 1.0])
    g = dpre + dL / (L - EULER - 1)
    se_logtA = float(np.sqrt(max(g @ cov @ g, 0))) if np.all(np.isfinite(cov)) else np.nan
    se = np.sqrt(np.clip(np.diag(cov), 0, None))
    gq = np.array([0, 2.0, 1.0, 0.0])
    se_logq = float(np.sqrt(max(gq @ cov @ gq, 0))) if np.all(np.isfinite(cov)) else np.nan
    return {"m": m, "mu": mu, "lam": lam, "s2": s2, "se_m": se[0], "se_logmu": se[1], "se_loglam": se[2], "se_logs2": se[3],
            "q": 4 * lam * mu ** 2, "se_logq": se_logq, "kappa": kap, "tA": tA, "se_logtA": se_logtA, "nll": best.fun}

def ou_fit(y):
    y = np.asarray(y, float)
    def nll(th):
        m, lphi, lv, ls2 = th
        return ou_nll(y, m, _sig(lphi), np.exp(lv), np.exp(ls2))
    v = np.var(y); best = None
    for phi0 in (0.9, 0.99, 0.999):
        for fs in (0.1, 0.5):
            r = minimize(nll, [np.mean(y), np.log(phi0 / (1 - phi0)), np.log(v * (1 - fs)), np.log(v * fs)],
                         method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 4000})
            if best is None or r.fun < best.fun:
                best = r
    m, lphi, lv, ls2 = best.x
    phi = _sig(lphi); lam_eq = -np.log(phi) / 2  # telegraph with the same autocovariance has e^{-2 lam}
    return {"m": m, "phi": phi, "v": np.exp(lv), "s2": np.exp(ls2), "q": 2 * np.exp(lv) * (-np.log(phi)),
            "lam_eq": lam_eq, "nll": best.fun}

def premise_lr(y):
    """LR = 2 (nll_OU - nll_HMM): two-state switching vs Gaussian Markov with the same kind of spectrum."""
    h = hmm_fit(y); o = ou_fit(y)
    return 2 * (o["nll"] - h["nll"]), h, o

def premise_test(y, B, rng):
    """Parametric bootstrap p-value of premise_lr under the fitted Gaussian (OU + noise) null."""
    lr, h, o = premise_lr(y)
    n = y.size; cnt = 0
    for b in range(B):
        e = rng.standard_normal(n) * np.sqrt(o["v"] * (1 - o["phi"] ** 2))
        s = o["m"] + _ar1(o["phi"], e, rng.standard_normal() * np.sqrt(o["v"]))
        yb = s + rng.standard_normal(n) * np.sqrt(o["s2"])
        lrb, _, _ = premise_lr(yb)
        cnt += lrb >= lr
    return lr, (1 + cnt) / (1 + B), h, o

# ---------------------------------------------------------------- event worlds
@numba.njit(cache=True)
def mmpp_nll(c, r0, r1, p):
    """Two-state Markov-modulated Poisson counts per bin (rates r0 < r1 per bin, switch prob p per bin)."""
    a0 = 0.5; a1 = 0.5; ll = 0.0
    for t in range(c.size):
        if t > 0:
            b0 = a0 * (1 - p) + a1 * p; b1 = a1 * (1 - p) + a0 * p; a0 = b0; a1 = b1
        k = c[t]
        lg = 0.0
        for i in range(2, k + 1):
            lg += np.log(i)
        e0 = np.exp(k * np.log(r0) - r0 - lg); e1 = np.exp(k * np.log(r1) - r1 - lg)
        a0 *= e0; a1 *= e1; z = a0 + a1
        if z <= 0:
            return 1e300
        ll += np.log(z); a0 /= z; a1 /= z
    return -ll

def mmpp_fit(c):
    c = np.asarray(c, np.int64)
    def nll(th):
        lr0, ld, llam = th
        r0 = np.exp(lr0); r1 = r0 + np.exp(ld); lam = np.exp(llam); p = (1 - np.exp(-2 * lam)) / 2
        return mmpp_nll(c, r0, r1, p)
    mbar = c.mean(); best = None
    for f in (0.3, 0.7):
        for lam0 in (0.005, 0.05):
            r = minimize(nll, [np.log(mbar * f + 1e-3), np.log(mbar * (2 - 2 * f) + 1e-3), np.log(lam0)], method="Nelder-Mead",
                         options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 4000})
            if best is None or r.fun < best.fun:
                best = r
    th = best.x; H = _hess(nll, th)
    try:
        cov = np.linalg.inv(H)
    except np.linalg.LinAlgError:
        cov = np.full((3, 3), np.nan)
    se = np.sqrt(np.clip(np.diag(cov), 0, None))
    r0 = np.exp(th[0]); r1 = r0 + np.exp(th[1]); lam = np.exp(th[2])
    return {"r0": r0, "r1": r1, "lam": lam, "mu": (r1 - r0) / 2, "se_loglam": se[2], "nll": best.fun}

def gap_order_stat(times, rng, nshuf=200):
    """Consecutive log-gap Spearman correlation and its shuffle-null z (renewal check; cf. records/tests/D3_OOS)."""
    from scipy.stats import spearmanr
    g = np.log(np.diff(np.sort(times)) + 1e-9)
    r = spearmanr(g[:-1], g[1:]).correlation
    null = []
    for _ in range(nshuf):
        h = rng.permutation(g); null.append(spearmanr(h[:-1], h[1:]).correlation)
    return r, (r - np.mean(null)) / (np.std(null) + 1e-12)


def whittle_counts(c, band=None, fix_s2=None, alpha_bounds=(0.05, 2.95)):
    """Event worlds: Whittle fit of binned counts c_t (undifferenced; stationary rate) with
    f(w) = (1/2pi)[q w^-alpha + s2] on the sampled grid (no aliasing term; the target is the Whittle pseudo-true value
    over the band). Under Poisson sensing of a Cox rate the floor s2 equals the mean count per bin (N = mean rate);
    fix_s2 imposes that premise, free s2 tests it (s2/mean != 1 flags renewal, self-excitation or overdispersion)."""
    w, I = periodogram(np.asarray(c, float))
    if band is not None:
        sel = (w >= band[0]) & (w <= band[1]); w, I = w[sel], I[sel]
    def fm(lq, a, ls):
        return (np.exp(lq) * w ** -a + np.exp(ls)) / (2 * pi)
    def nll(p):
        if fix_s2 is None:
            f = fm(*p)
        else:
            f = fm(p[0], p[1], np.log(fix_s2))
        return np.sum(np.log(f) + I / f)
    v = np.var(c); best = None
    for a0 in (0.5, 1.2, 2.0):
        for nf in (0.3, 0.8):
            ls0 = np.log(v * nf); lq0 = np.log(2 * pi * np.median(I[:10]) + 1e-12) + a0 * np.log(w[min(5, w.size - 1)])
            x0 = [lq0, a0, ls0] if fix_s2 is None else [lq0, a0]
            b = [(lq0 - 30, lq0 + 30), alpha_bounds] + ([(ls0 - 30, ls0 + 10)] if fix_s2 is None else [])
            r = minimize(nll, x0, method="L-BFGS-B", bounds=b)
            if best is None or r.fun < best.fun:
                best = r
    p = best.x
    th = list(p) if fix_s2 is None else [p[0], p[1], np.log(fix_s2)]
    h = 1e-5; g = []
    for i in range(len(p)):
        tp = np.array(th); tm = tp.copy(); tp[i] += h; tm[i] -= h
        g.append((np.log(fm(*tp)) - np.log(fm(*tm))) / (2 * h))
    g = np.array(g); cov = np.linalg.inv(g @ g.T); se = np.sqrt(np.clip(np.diag(cov), 0, None))
    return {"logq": th[0], "alpha": th[1], "logs2": th[2], "se_alpha": se[1], "se_logq": se[0],
            "se_logs2": (se[2] if fix_s2 is None else 0.0), "nll": best.fun,
            "at_bound": bool(min(abs(th[1] - alpha_bounds[0]), abs(th[1] - alpha_bounds[1])) < 1e-3)}

def pseudo_true_counts(ftrue, n, band=None):
    w = 2 * pi * np.arange(1, n // 2) / n
    if band is not None:
        w = w[(w >= band[0]) & (w <= band[1])]
    ft = ftrue(w)
    def kl(p):
        f = (np.exp(p[0]) * w ** -p[1] + np.exp(p[2])) / (2 * pi); return np.sum(np.log(f) + ft / f)
    best = None
    for a0 in (0.5, 1.2, 2.0):
        r = minimize(kl, [0.0, a0, 0.0], method="L-BFGS-B", bounds=[(-40, 40), (0.05, 2.95), (-40, 15)])
        if best is None or r.fun < best.fun:
            best = r
    return best.x

def lomax_renewal_times(T, rate, shape, rng):
    """Renewal process on [0, T] with Lomax(shape) gaps of mean 1/rate (needs shape > 1)."""
    scale = (shape - 1) / rate
    out = []; t = 0.0
    while t < T:
        g = scale * (rng.random(4096) ** (-1 / shape) - 1)
        ts = t + np.cumsum(g); out.append(ts[ts < T]); t = ts[-1]
    return np.concatenate(out)

def cox_times(rate_per_bin, rng):
    """Event times from piecewise-constant rate per unit bin."""
    c = rng.poisson(np.clip(rate_per_bin, 0, None))
    idx = np.repeat(np.arange(c.size), c)
    return idx + rng.random(idx.size), c

# ---------------------------------------------------------------- stakes
def stakes_fit(err, cost, err_rep=None, B=400, rng=None):
    """Stakes w from an error-cost curve, quadratic loss (THEORY §2.1): cost = a + w e^2 + noise.
    OLS slope of cost on err^2 (attenuated if err is measured with noise), and, if a second independent measurement
    err_rep of the same error is available, the IV slope Cov(cost, err_rep^2)/Cov(err^2, err_rep^2), which is
    consistent for w when the two measurement errors are independent, mean zero and independent of e and of the
    cost noise. Pairs-bootstrap 95% percentile CIs. Valid only when the variation in e is exogenous to w
    (designed or natural-experiment variation); see validate_stakes for the failure under self-selected error."""
    rng = rng or np.random.default_rng(0)
    n = err.size
    def est(ix):
        x = err[ix] ** 2; c = cost[ix]
        ols = np.cov(c, x)[0, 1] / np.var(x, ddof=1)
        if err_rep is None:
            return ols, np.nan
        z = err_rep[ix] ** 2
        iv = np.cov(c, z)[0, 1] / np.cov(x, z)[0, 1]
        return ols, iv
    pt = est(np.arange(n))
    bs = np.array([est(rng.integers(0, n, n)) for _ in range(B)])
    out = {"w_ols": pt[0], "ols_lo": np.percentile(bs[:, 0], 2.5), "ols_hi": np.percentile(bs[:, 0], 97.5)}
    if err_rep is not None:
        out.update({"w_iv": pt[1], "iv_lo": np.nanpercentile(bs[:, 1], 2.5), "iv_hi": np.nanpercentile(bs[:, 1], 97.5)})
    return out
