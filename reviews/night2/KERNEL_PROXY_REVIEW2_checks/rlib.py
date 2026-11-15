"""Reviewer-2 library (PR #66 independent review). Written from the prereg text only; imports nothing from
tests/KERNEL_MEASURE, measurement/ or reviews/night2/KERNEL_PROXY_checks."""
import numpy as np, pandas as pd, math
DATA = '../../../tests/KERNEL_MEASURE/data/'
AGES = [(0, 0), (1, 1), (2, 4), (5, 9), (10, 20), (21, 41), (42, 83), (84, 167), (168, 335), (336, 503)]
WID = np.array([b - a + 1 for a, b in AGES], float)
TAIL = np.array([a >= 21 for a, b in AGES])
H = 21; MAXAGE = 503

def load(end='2026-10-30'):
    g = pd.read_csv(DATA + 'GSPC_ohlc.csv'); g = g[g['date'] <= end].reset_index(drop=True)
    v = pd.read_csv(DATA + 'VIXCLS.csv', na_values=['.', ''])
    v = v.rename(columns={'observation_date': 'date'})
    g = g.merge(v, on='date', how='left')
    g['park'] = np.log(g['high'] / g['low']) ** 2 / (4 * np.log(2))
    g['y'] = np.log(g['park']); g['z'] = 2 * np.log(g['VIXCLS'])
    g['on2'] = np.r_[0.0, np.log(g['open'].values[1:] / g['close'].values[:-1]) ** 2]
    return g

def design(y):
    """row for each t>=MAXAGE: [1, sum_{age in bin} y_{t-age}] built with pandas rolling sums (shifted)."""
    s = pd.Series(y)
    cols = [np.ones(len(y))]
    for a, b in AGES:
        cols.append(s.shift(a).rolling(b - a + 1).sum().values)
    X = np.column_stack(cols)
    idx = np.arange(MAXAGE, len(y))
    return X[idx], idx

def future_mean(v, h=H):
    s = pd.Series(v)
    return s.rolling(h).mean().shift(-h).values      # mean of v[t+1..t+h]

def kernel_stats(beta):
    w = beta[1:] * WID            # mass per bin
    return w[TAIL].sum() / w.sum(), w.sum(), w / w.sum()

def W(beta): return kernel_stats(beta)[0]

def ols(X, z):
    return np.linalg.lstsq(X, z, rcond=None)[0]

def block_boot(X, Ys, block=126, nb=999, seed=7, trunc=True, stat=None):
    """Non-overlapping blocks of `block` consecutive rows, resampled with replacement. Ys: dict of responses
    (same rows). Returns full-sample stats and bootstrap draws of (W, sum)."""
    m = (len(X) // block) * block if trunc else len(X)
    X = X[:m]; Ys = {k: v[:m] for k, v in Ys.items()}
    nbk = m // block
    XX = np.stack([X[i*block:(i+1)*block].T @ X[i*block:(i+1)*block] for i in range(nbk)])
    XY = {k: np.stack([X[i*block:(i+1)*block].T @ v[i*block:(i+1)*block] for i in range(nbk)]) for k, v in Ys.items()}
    def fit(ix):
        A = XX[ix].sum(0)
        return {k: kernel_stats(np.linalg.solve(A, XY[k][ix].sum(0))) for k in Ys}
    full = fit(np.arange(nbk)); rng = np.random.default_rng(seed)
    draws = [fit(rng.integers(0, nbk, nbk)) for _ in range(nb)]
    Wd = {k: np.array([d[k][0] for d in draws]) for k in Ys}
    Sd = {k: np.array([d[k][1] for d in draws]) for k in Ys}
    return full, Wd, Sd, m

# ---------- model side (own fGn, own intrinsic kriging) ----------
def fgn_circulant(n, hurst, rng):
    """exact fGn by circulant embedding (Wood-Chan); unit variance."""
    k = np.arange(0, n)
    g = 0.5 * ((k + 1.0) ** (2 * hurst) - 2 * k.astype(float) ** (2 * hurst) + np.abs(k - 1.0) ** (2 * hurst))
    row = np.r_[g, g[-2:0:-1]]
    ev = np.fft.rfft(row).real if False else np.fft.fft(row).real
    if ev.min() < -1e-8: raise ValueError('embedding not psd')
    ev = np.clip(ev, 0, None); M = len(row)
    Z = rng.standard_normal(M) + 1j * rng.standard_normal(M)
    return np.fft.fft(np.sqrt(ev / M) * Z).real[:n]

def vario_coef(alpha, lnq):
    # S(w)=q|w|^-alpha (dw/2pi)  =>  Var(x_t-x_0) = q t^(alpha-1) / (Gamma(alpha) sin(pi(alpha-1)/2))
    return math.exp(lnq) / (math.gamma(alpha) * math.sin(math.pi * (alpha - 1) / 2))

def sim_driver(n, rng, alpha, lnq, lns2):
    c = vario_coef(alpha, lnq)
    x = np.cumsum(math.sqrt(c) * fgn_circulant(n, (alpha - 1) / 2, rng))
    return x, x + math.exp(lns2 / 2) * rng.standard_normal(n)

def blp(L, alpha, lnq, lns2, h=H):
    """weights on y_{t-0..t-L+1} for E[mean x_{t+1..t+h}]: universal kriging with unknown constant mean,
    generalized covariance K(d) = -c|d|^(alpha-1)/2, nugget s2."""
    c = vario_coef(alpha, lnq); s2 = math.exp(lns2)
    pos = -np.arange(L, dtype=float)
    K = lambda d: -0.5 * c * np.abs(d) ** (alpha - 1)
    A = np.empty((L + 1, L + 1)); A[:L, :L] = K(pos[:, None] - pos[None, :]); A[np.diag_indices(L)] += s2
    A[L, :L] = A[:L, L] = 1.0; A[L, L] = 0.0
    fut = np.arange(1, h + 1, dtype=float)
    rhs = np.r_[K(pos[:, None] - fut[None, :]).mean(1), 1.0]
    return np.linalg.solve(A, rhs)[:L]
