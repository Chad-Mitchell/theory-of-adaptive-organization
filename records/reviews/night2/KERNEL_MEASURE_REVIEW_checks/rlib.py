"""Independent reviewer library for KERNEL-MEASURE (PR #58 review). Written from scratch; imports nothing from
tests/KERNEL_MEASURE or measurement/estimators. Conventions re-derived: S(w) = q|w|^-alpha with var = int S dw/(2pi);
variogram of x at integer lag tau: q*tau^(alpha-1) / (Gamma(alpha) sin(pi(alpha-1)/2))."""
import csv, math, os, numpy as np
from scipy.optimize import minimize
from scipy.special import gamma as G

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '../../../tests/KERNEL_MEASURE/data')
EDGES = [0, 1, 2, 5, 10, 21, 42, 84, 168, 336, 504]
LW = 504

def load():
    rows = [r for r in csv.DictReader(open(os.path.join(DATA, 'GSPC_ohlc.csv'))) if r['date'] <= '2026-10-30']
    hi = np.array([float(r['high']) for r in rows]); lo = np.array([float(r['low']) for r in rows])
    pv = np.log(hi / lo) ** 2 / (4 * math.log(2))
    assert np.all(pv > 0)
    vix = {}
    for r in csv.DictReader(open(os.path.join(DATA, 'VIXCLS.csv'))):
        try: vix[r['observation_date']] = float(r['VIXCLS'])
        except ValueError: pass
    z = np.array([2 * math.log(vix[r['date']]) if r['date'] in vix else np.nan for r in rows])
    return np.log(pv), z, [r['date'] for r in rows]

def vgc(alpha):                     # variogram constant per unit q
    return 1.0 / (G(alpha) * math.sin(math.pi * (alpha - 1) / 2))

# ---------- Whittle on first differences
def aliased(w, alpha, K=200):
    k = np.arange(-K, K + 1)[:, None]
    s = np.sum(np.abs(w[None, :] + 2 * np.pi * k) ** (-alpha), 0)
    # tail correction for |k| > K (integral approximation, both sides)
    tail = 2 * (2 * np.pi) ** (-alpha) * (K + 0.5) ** (1 - alpha) / (alpha - 1)
    return s + tail

def pgram_diff(y):
    d = np.diff(y); d = d - d.mean(); m = len(d)
    F = np.fft.fft(d); j = np.arange(1, (m - 1) // 2 + 1)
    return 2 * np.pi * j / m, np.abs(F[j]) ** 2 / (2 * np.pi * m)

def f_model(w, alpha, logq, logs2):
    return 4 * np.sin(w / 2) ** 2 / (2 * np.pi) * (math.exp(logq) * aliased(w, alpha) + math.exp(logs2))

def whittle(y, wmax=np.pi, wmin=0.0, fix_logs2=None):
    w, I = pgram_diff(y); k = (w > wmin) & (w <= wmax); w, I = w[k], I[k]
    def unpack(p): return (p[0], p[1], fix_logs2) if fix_logs2 is not None else tuple(p)
    def nll(p):
        a, lq, ls = unpack(p)
        if not 1.01 < a < 2.99: return 1e12
        f = f_model(w, a, lq, ls); return float(np.sum(np.log(f) + I / f))
    best = None
    for a0 in (1.1, 1.3, 1.6, 2.0):
        for ls0 in (-3.0, -1.0, 0.0):
            p0 = [a0, -2.0] + ([] if fix_logs2 is not None else [ls0])
            r = minimize(nll, p0, method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 1e-9, 'maxiter': 20000})
            if best is None or r.fun < best.fun: best = r
    p = best.x
    # Fisher information for Whittle: sum grad log f grad log f^T
    h = 1e-5; g = []
    for i in range(len(p)):
        e = np.zeros(len(p)); e[i] = h
        g.append((np.log(f_model(w, *unpack(p + e))) - np.log(f_model(w, *unpack(p - e)))) / (2 * h))
    g = np.array(g); Fi = g @ g.T
    try: se = np.sqrt(np.diag(np.linalg.inv(Fi)))
    except np.linalg.LinAlgError: se = np.full(len(p), np.nan)
    out = {'alpha': p[0], 'se_alpha': se[0], 'logq': p[1], 'se_logq': se[1], 'nfreq': int(len(w)), 'nll': best.fun}
    if fix_logs2 is None: out.update({'logs2': p[2], 'se_logs2': se[2]})
    else: out['logs2_fixed'] = fix_logs2
    return out

# ---------- theory kernel: best linear predictor of mean(x_{t+1..t+h}) from y_{t-i}, i<Lw, unknown level
def kernel(alpha, q, s2, Lw=LW, h=21):
    c = q * vgc(alpha)
    gam = lambda tau: 0.5 * c * np.abs(tau) ** (alpha - 1)          # semivariogram of x
    i = np.arange(Lw, dtype=float)
    # Kriging in variogram form: sum_j w_j gamma_y(i-j) + mu = gamma_xy(i, target), sum w = 1.
    # gamma_y(i-j) = gam(i-j) + s2*(i!=j); target cross-semivariogram = mean_k gam(i+k) + s2/2? -> derive via null-space
    # Use null-space elimination: w = e0 + N v, with columns of N summing to zero (e_k - e_0).
    Gy = gam(i[:, None] - i[None, :]) + s2 * (1 - np.eye(Lw))
    g0 = np.mean([gam(i + k) for k in range(1, h + 1)], axis=0)        # gamma(y_{t-i}, xbar_target), noise uncorrelated
    # minimise MSE(w) = -w'Gy w + 2 w'g0 + const  (valid for sum w = 1); stationarity => solve over null space
    N = np.zeros((Lw, Lw - 1)); N[0, :] = -1; N[np.arange(1, Lw), np.arange(Lw - 1)] = 1
    e0 = np.zeros(Lw); e0[0] = 1
    A = -(N.T @ Gy @ N); b = N.T @ (Gy @ e0 - g0)
    v = np.linalg.solve(A, b)
    return e0 + N @ v

def survival(w, tau=21): return w[tau:].sum() / w.sum()

# ---------- fGn / fBm by circulant embedding (Davies-Harte)
def fgn(n, H, rng):
    k = np.arange(n + 1, dtype=float)
    r = 0.5 * ((k + 1) ** (2 * H) - 2 * k ** (2 * H) + np.abs(k - 1) ** (2 * H))
    c = np.concatenate([r, r[-2:0:-1]]); lam = np.fft.fft(c).real
    if lam.min() < -1e-8: raise ValueError('embedding not PSD')
    lam = np.clip(lam, 0, None); m = len(c)
    W = rng.standard_normal(m) + 1j * rng.standard_normal(m)
    return np.fft.fft(np.sqrt(lam / m) * W).real[:n]

def sim_y(n, alpha, q, s2, rng):
    x = np.cumsum(math.sqrt(q * vgc(alpha)) * fgn(n, (alpha - 1) / 2, rng))
    return x + (rng.normal(0, math.sqrt(s2), n) if s2 > 0 else 0)

def apply_kernel(y, w):
    """f_t = sum_i w_i y_{t-i}; NaN where history short."""
    L = len(w); f = np.full(len(y), np.nan)
    conv = np.convolve(y, w, mode='valid'); f[L - 1:] = conv
    return f

# ---------- binned projection estimator (own implementation)
def bins(y):
    cs = np.concatenate([[0.0], np.cumsum(y)]); n = len(y); t = np.arange(LW - 1, n)
    cols = [cs[t - a + 1] - cs[t - b + 1] for a, b in zip(EDGES[:-1], EDGES[1:])]   # sum y_{t-a}..y_{t-b+1}
    return t, np.stack(cols, 1)

def w21_from_beta(beta):
    mass = beta * np.diff(EDGES); return mass[EDGES.index(21):].sum() / mass.sum()

def fit_w21(z, y, block=126, nboot=0, seed=1):
    t, B = bins(y); zz = z[t]; ok = np.isfinite(zz); B, zz = B[ok], zz[ok]
    nb = len(zz) // block; m = nb * block; B, zz = B[:m], zz[:m]
    X = np.column_stack([np.ones(m), B])
    beta = np.linalg.lstsq(X, zz, rcond=None)[0]
    out = {'W21': w21_from_beta(beta[1:]), 'rows': m, 'blocks': nb, 'beta': beta[1:]}
    if nboot:
        rng = np.random.default_rng(seed); Xb = X.reshape(nb, block, -1); zb = zz.reshape(nb, block)
        XtX = np.einsum('kti,ktj->kij', Xb, Xb); Xtz = np.einsum('kti,kt->ki', Xb, zb)
        bs = []
        for _ in range(nboot):
            c = np.bincount(rng.integers(0, nb, nb), minlength=nb).astype(float)
            bs.append(w21_from_beta(np.linalg.solve(np.tensordot(c, XtX, 1), c @ Xtz)[1:]))
        bs = np.array(bs); out.update({'sd': bs.std(ddof=1), 'q': np.quantile(bs, [.025, .975]).tolist()})
    return out
