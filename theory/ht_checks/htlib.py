"""Shared functions for theory/HT_INDEX.md (head/tail breaks, ht-index, world generators, pole counters).
numpy/scipy only. Run everything at nice 19."""
import numpy as np

THR = 0.40  # Jiang, Liu & Jia 2013 / Jiang & Yin 2014 head-fraction threshold


def ht_index(x, thr=THR):
    """Jiang & Yin (2014) ht-index: 1 + number of head/tail splits whose head (values > mean) is a minority (<= thr).
    Reproduces Jiang & Ma's worked example: Zipf 1, 1/2, ..., 1/10 -> 3."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    h = 1
    while x.size > 1:
        m = x.mean()
        head = x[x > m]
        if head.size == 0 or head.size / x.size > thr:
            break
        h += 1
        x = head
    return h


def head_fractions(x, thr=THR):
    x = np.asarray(x, float); out = []
    while x.size > 1:
        head = x[x > x.mean()]
        if head.size == 0:
            break
        out.append(head.size / x.size)
        if out[-1] > thr:
            break
        x = head
    return out


def p_pareto(alpha):
    """Asymptotic head fraction per split for a Pareto tail of index alpha > 1: ((alpha-1)/alpha)^alpha.
    alpha -> inf gives e^-1 (exponential / Gumbel domain)."""
    return ((alpha - 1) / alpha) ** alpha


def ht_pred(n, p):
    """Leading-order prediction: ht ~ 1 + ln(n)/ln(1/p) (each split keeps a fraction p; stops near one value)."""
    return 1 + np.log(n) / np.log(1 / p)


# ---------------------------------------------------------------- worlds
def ou_sum(taus, var, n, dt, rng, noise_sd=0.0):
    """Sum of independent OU modes (exact discretisation) plus white read noise. Returns y (n,) and the modes (J, n)."""
    taus = np.asarray(taus, float); var = np.asarray(var, float)
    phi = np.exp(-dt / taus); sd = np.sqrt(var * (1 - phi ** 2))
    J = len(taus); s = np.zeros((J, n))
    s[:, 0] = rng.standard_normal(J) * np.sqrt(var)
    e = rng.standard_normal((J, n)) * sd[:, None]
    for t in range(1, n):
        s[:, t] = phi * s[:, t - 1] + e[:, t]
    y = s.sum(0) + noise_sd * rng.standard_normal(n)
    return y, s


def ou_modes_fast(taus, var, n, dt, rng):
    """Same as ou_sum's modes but via scipy.signal.lfilter (fast)."""
    from scipy.signal import lfilter
    taus = np.asarray(taus, float); var = np.asarray(var, float)
    phi = np.exp(-dt / taus); sd = np.sqrt(var * (1 - phi ** 2))
    s = np.empty((len(taus), n))
    for j in range(len(taus)):
        e = rng.standard_normal(n) * sd[j]
        e[0] = rng.standard_normal() * np.sqrt(var[j])
        s[j] = lfilter([1.0], [1.0, -phi[j]], e)
    return s


def fgn(H, n, rng):
    """Fractional Gaussian noise by Davies-Harte circulant embedding (exact)."""
    k = np.arange(n + 1)
    g = 0.5 * ((k + 1.0) ** (2 * H) - 2 * k ** (2.0 * H) + np.abs(k - 1.0) ** (2 * H))
    c = np.concatenate([g, g[-2:0:-1]])
    lam = np.fft.fft(c).real
    lam[lam < 0] = 0
    m = len(c)
    w = rng.standard_normal(m) + 1j * rng.standard_normal(m)
    z = np.fft.fft(np.sqrt(lam / (2 * m)) * w)
    return z.real[:n]


def periodogram(y):
    Y = np.fft.rfft(y - y.mean())
    return (np.abs(Y[1:]) ** 2) / len(y)


def crossing_durations(y):
    """Durations between successive crossings of the record's mean (excursion lengths, in samples)."""
    s = np.sign(y - y.mean()); idx = np.flatnonzero(np.diff(s) != 0)
    return np.diff(idx).astype(float)


# ---------------------------------------------------------------- pole counting (Hankel DMD; a proxy for the counting rule)
def gavish_donoho_rank(sv, shape):
    """Optimal hard threshold for unknown noise (Gavish & Donoho 2014): tau = omega(beta) * median(sv)."""
    m, n = sorted(shape); beta = m / n
    omega = 0.56 * beta ** 3 - 0.95 * beta ** 2 + 1.82 * beta + 1.43
    return int(np.sum(sv > omega * np.median(sv)))


def hankel_dmd_rates(Y, dt, lags=40, stride=1, rank=None, max_rank=12):
    """Y: (M, n) records. Delay-embed each with `lags` lags at `stride`, SVD, truncate (Gavish-Donoho, capped),
    exact DMD; return continuous-time rates (1/time) of real, decaying eigenvalues, and the rank used."""
    Y = np.atleast_2d(Y); M, n = Y.shape
    Y = (Y - Y.mean(1, keepdims=True))
    Y = Y[:, ::stride]; n = Y.shape[1]; h = dt * stride
    cols = n - lags
    Hk = np.vstack([Y[:, i:i + cols] for i in range(lags)])
    X, X2 = Hk[:, :-1], Hk[:, 1:]
    U, sv, Vt = np.linalg.svd(X, full_matrices=False)
    r = rank if rank is not None else min(max_rank, max(1, gavish_donoho_rank(sv, X.shape)))
    Ur, Sr, Vr = U[:, :r], sv[:r], Vt[:r].T
    A = Ur.T @ X2 @ Vr / Sr
    lam = np.linalg.eigvals(A)
    rates = []
    for l in lam:
        if abs(l.imag) < 1e-3 * max(abs(l), 1e-12) and 0 < l.real < 1:
            rates.append(-np.log(l.real) / h)
    return np.sort(np.array(rates)), r, sv


def merge_count(rates, band, factor=3.0):
    """Counting-rule merge (face_placements.md §4 step 3): keep rates whose time constants lie in the band,
    then merge time constants within a factor `factor` of each other. Returns the number of distinct scales."""
    taus = np.sort(1 / np.asarray(rates)) if len(rates) else np.array([])
    taus = taus[(taus >= band[0]) & (taus <= band[1])]
    if taus.size == 0:
        return 0, taus
    groups = [[taus[0]]]
    for t in taus[1:]:
        if t / groups[-1][0] < factor:
            groups[-1].append(t)
        else:
            groups.append([t])
    return len(groups), np.array([np.exp(np.mean(np.log(g))) for g in groups])


# ---------------------------------------------------------------- rival estimators
def mfdfa(y, qs=(-3, -1, 1, 2, 3, 5), scales=None, order=1):
    """MF-DFA (Kantelhardt et al. 2002); q = 2 is DFA (Peng et al. 1994). Returns scales, F_q(s) (len(qs), len(scales)), h(q)
    from a log-log fit over all scales. For stationary fGn-like input, h(2) estimates the Hurst exponent."""
    y = np.asarray(y, float); n = len(y)
    prof = np.cumsum(y - y.mean())
    if scales is None:
        scales = np.unique(np.logspace(np.log10(10), np.log10(n // 8), 18).astype(int))
    F = np.zeros((len(qs), len(scales)))
    for k, s in enumerate(scales):
        m = n // s
        seg = prof[:m * s].reshape(m, s)
        x = np.arange(s)
        V = np.vander(x, order + 1)
        coef, *_ = np.linalg.lstsq(V, seg.T, rcond=None)
        res = seg.T - V @ coef
        f2 = (res ** 2).mean(0)
        f2 = f2[f2 > 0]
        for i, q in enumerate(qs):
            F[i, k] = np.exp(0.5 * np.mean(np.log(f2))) if q == 0 else np.mean(f2 ** (q / 2)) ** (1 / q)
    ls = np.log(scales)
    h = np.array([np.polyfit(ls, np.log(F[i]), 1)[0] for i in range(len(qs))])
    return scales, F, h


def dfa_local_slopes(y, scales=None):
    """Local DFA slopes d log F2 / d log s; crossovers (changes in slope) mark scale corners."""
    sc, F, h = mfdfa(y, qs=(2,), scales=scales)
    ls, lf = np.log(sc), np.log(F[0])
    return sc, np.gradient(lf, ls), h[0]


def mf_width(y, qs=(-3, -1, 1, 2, 3, 5)):
    """Multifractal width proxy Δh = h(q_min) - h(q_max) from MF-DFA."""
    _, _, h = mfdfa(y, qs=qs)
    return float(h[0] - h[-1])


def spectral_peak_count(y, dt, per_decade=6, prom=0.15, band=None):
    """Count peaks of the variance-per-log-frequency curve f*S(f) (log-binned periodogram, smoothed in log f).
    Each separated OU (Lorentzian) mode is one hump of f*S(f) at f = 1/(2*pi*tau). prom = minimum relative prominence (dex)."""
    from scipy.signal import find_peaks
    P = periodogram(y); f = np.arange(1, len(P) + 1) / (len(y) * dt)
    lf = np.log10(f); edges = np.arange(lf.min(), lf.max() + 1e-9, 1 / per_decade)
    idx = np.digitize(lf, edges)
    fc, v = [], []
    for b in np.unique(idx):
        sel = idx == b
        if sel.sum() >= 3:
            fc.append(np.mean(lf[sel])); v.append(np.log10(np.mean(f[sel] * P[sel])))
    fc, v = np.array(fc), np.array(v)
    if band is not None:
        keep = (fc >= np.log10(band[0])) & (fc <= np.log10(band[1])); fc, v = fc[keep], v[keep]
    vs = np.convolve(np.pad(v, 1, mode='edge'), np.ones(3) / 3, mode='valid')
    pk, _ = find_peaks(np.pad(vs, 1, constant_values=-np.inf), prominence=prom)
    return len(pk), 10 ** fc[pk - 1] if len(pk) else np.array([])


# ---------------------------------------------------------------- Whittle pole count (the counting rule's ΔBIC step, on spectra)
def binned_periodogram(y, dt, per_decade=24):
    """Log-binned periodogram: bin centres f (1/time), mean ordinate Pbar, count m. Ordinates are ~ S(f)*Exp(1)
    asymptotically, so a bin's Whittle term is m*(log S + Pbar/S)."""
    y = np.asarray(y, float); n = len(y)
    Y = np.fft.rfft(y - y.mean())
    P = (np.abs(Y[1:]) ** 2) * dt / n          # two-sided density convention S(f) with var = int S df over (-1/2dt, 1/2dt)
    f = np.arange(1, len(P) + 1) / (n * dt)
    lf = np.log10(f); edges = np.arange(lf.min(), lf.max() + 1 / per_decade, 1 / per_decade)
    idx = np.digitize(lf, edges)
    F, Pb, M = [], [], []
    for b in np.unique(idx):
        sel = idx == b
        F.append(np.exp(np.mean(np.log(f[sel])))); Pb.append(P[sel].mean()); M.append(sel.sum())
    return np.array(F), np.array(Pb), np.array(M)


def lorentz_sum(f, taus, vs, N, dt):
    """Discrete-time spectrum of a sum of AR(1)=sampled-OU modes plus white noise (density N*dt), two-sided."""
    w = 2 * np.pi * f * dt
    S = np.full_like(f, N * dt)
    for t, v in zip(taus, vs):
        phi = np.exp(-dt / t)
        S = S + v * (1 - phi ** 2) * dt / (1 - 2 * phi * np.cos(w) + phi ** 2)
    return S


def whittle_fit(F, Pb, M, dt, K, rng, starts=8, tau_band=None):
    from scipy.optimize import minimize
    tmin, tmax = tau_band if tau_band else (dt, 1 / F.min())
    var0 = np.sum(Pb * M) / np.sum(M) / dt  # rough scale
    def unpack(x):
        taus = np.exp(x[:K]); vs = np.exp(x[K:2 * K]); N = np.exp(x[-1]); return taus, vs, N
    def nll(x):
        taus, vs, N = unpack(x)
        if np.any(taus < tmin / 3) or np.any(taus > tmax * 3):
            return 1e30
        S = lorentz_sum(F, taus, vs, N, dt)
        return float(np.sum(M * (np.log(S) + Pb / S)))
    best = (np.inf, None)
    for s in range(starts):
        lt = np.sort(rng.uniform(np.log(tmin), np.log(tmax), K)) if s else np.linspace(np.log(tmin), np.log(tmax), K + 2)[1:-1]
        x0 = np.concatenate([lt, np.log(np.full(K, var0 * dt / K + 1e-12) / dt), [np.log(Pb[-3:].mean() / dt + 1e-12)]])
        r = minimize(nll, x0, method='Nelder-Mead', options=dict(maxiter=3000 * (2 * K + 1), xatol=1e-6, fatol=1e-6))
        r = minimize(nll, r.x, method='Nelder-Mead', options=dict(maxiter=3000 * (2 * K + 1), xatol=1e-7, fatol=1e-8))
        if r.fun < best[0]:
            best = (r.fun, r.x)
    taus, vs, N = unpack(best[1])
    o = np.argsort(taus)
    return best[0], taus[o], vs[o], N


def whittle_pole_count(y, dt, Kmax=5, dbic=10.0, factor=3.0, band=None, rng=None, per_decade=24):
    """Counting-rule proxy on one record: Whittle fits of order K = 0..Kmax (white floor always present);
    accept K+1 over K only if ΔBIC >= dbic (face_placements.md §4 step 3); then drop time constants outside the band
    and merge within `factor`. Returns (count, merged taus, accepted K, fitted taus)."""
    rng = rng or np.random.default_rng(0)
    F, Pb, M = binned_periodogram(y, dt, per_decade)
    n_eff = np.sum(M)
    # K = 0: white only
    N0 = np.sum(M * Pb) / np.sum(M) / dt
    nll0 = float(np.sum(M * (np.log(N0 * dt) + Pb / (N0 * dt))))
    bic = [2 * nll0 + 1 * np.log(n_eff)]; fits = [(np.array([]), np.array([]), N0)]
    K = 0
    for k in range(1, Kmax + 1):
        nll, taus, vs, N = whittle_fit(F, Pb, M, dt, k, rng, tau_band=band)
        b = 2 * nll + (2 * k + 1) * np.log(n_eff)
        bic.append(b); fits.append((taus, vs, N))
        if bic[K] - b >= dbic:
            K = k
        else:
            break
    taus = fits[K][0]
    if band is not None:
        taus = taus[(taus >= band[0]) & (taus <= band[1])]
    c, merged = merge_count(1 / taus if len(taus) else [], (0, np.inf), factor)
    return c, merged, K, fits[K]
