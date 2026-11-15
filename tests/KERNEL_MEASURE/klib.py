"""KERNEL-MEASURE (QUEUE pick 28) library: theory kernel (intrinsic/ordinary kriging = best linear predictor with
unknown level), locked kernel-family estimator with block bootstrap, and simulators. Own code; uses only aqn.py's
fBm generator and the D1 constant (variogram E(x_{t+tau}-x_t)^2 = q*D1(alpha)*tau^(alpha-1))."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../measurement/estimators'))
import aqn

L, H = 504, 21                                   # lag window (business days), VIX horizon (30 calendar days)
S_GRID = np.round(np.arange(0.0, 3.0001, 0.02), 4)
C_GRID = np.array([0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256])
BLOCK = 126

def ok_kernel(alpha, q, s2, Lw=L, h=H):
    """Best linear predictor of mean(x_{t+1..t+h}) from y_{t-i} = x_{t-i} + e, i = 0..Lw-1, x with stationary
    increments and variogram q*D1*tau^(alpha-1), unknown level (weights sum to 1). Returns weights by age i."""
    Dc = q * aqn.D1(alpha)
    K = lambda tau: -0.5 * Dc * np.abs(tau) ** (alpha - 1)      # generalized covariance (order 0)
    i = np.arange(Lw)
    A = K(i[:, None] - i[None, :]) + s2 * np.eye(Lw)
    rhs = np.mean([K(i + k) for k in range(1, h + 1)], axis=0)
    M = np.zeros((Lw + 1, Lw + 1)); M[:Lw, :Lw] = A; M[:Lw, Lw] = 1; M[Lw, :Lw] = 1
    sol = np.linalg.solve(M, np.concatenate([rhs, [1.0]]))
    return sol[:Lw]

def family():
    """Locked family w(tau) = (tau + c)^-(1+s), tau = 0..L-1, normalised to sum 1. Columns ordered (s, c)."""
    tau = np.arange(L)[:, None]
    ss, cc = np.meshgrid(S_GRID, C_GRID, indexing='ij')
    ss, cc = ss.ravel(), cc.ravel()
    W = (tau + cc[None, :]) ** (-(1 + ss[None, :]))
    return W / W.sum(0), ss, cc

W_FAM, SS, CC = family()

def lagmat(y):
    """Rows t = L-1..n-1, columns age 0..L-1."""
    from numpy.lib.stride_tricks import sliding_window_view
    return sliding_window_view(y, L)[:, ::-1]

def fit(z, y, nboot=0, seed=0, W=W_FAM):
    """Locked estimator: z_t = a + b * sum_tau w(tau; s, c) y_{t-tau} + e, grid MLE (max R^2 with b > 0);
    circular-free non-overlapping block bootstrap (BLOCK rows) of the same argmax. z aligned with y (same t)."""
    X = lagmat(y); zz = z[L - 1:]
    ok = np.isfinite(zz)
    X, zz = X[ok], zz[ok]
    P = X @ W                                   # (rows, G)
    nb = len(zz) // BLOCK; m = nb * BLOCK
    P, zz = P[:m], zz[:m]
    def blocksums(a): return a.reshape(nb, BLOCK, *a.shape[1:]).sum(1)
    Sz, Szz = blocksums(zz), blocksums(zz * zz)
    Sx, Sxx, Szx = blocksums(P), blocksums(P * P), blocksums(P * zz[:, None])
    def best(wt):
        n = wt.sum() * BLOCK
        sz, szz = wt @ Sz, wt @ Szz; sx, sxx, szx = wt @ Sx, wt @ Sxx, wt @ Szx
        cov = szx / n - sz * sx / n ** 2; vx = sxx / n - (sx / n) ** 2; vz = szz / n - (sz / n) ** 2
        r = cov / np.sqrt(vx * vz)
        r = np.where(cov > 0, r, -np.inf)
        g = int(np.argmax(r)); return g, r[g]
    g, r = best(np.ones(nb))
    out = {'s': float(SS[g]), 'c': float(CC[g]), 'r2': float(r ** 2), 'rows': int(m), 'blocks': int(nb)}
    if nboot:
        rng = np.random.default_rng(seed)
        bs = []
        for _ in range(nboot):
            wt = np.bincount(rng.integers(0, nb, nb), minlength=nb).astype(float)
            bs.append(SS[best(wt)[0]])
        bs = np.array(bs)
        out.update({'boot_sd': float(bs.std(ddof=1)), 'boot_q025': float(np.quantile(bs, .025)),
                    'boot_q975': float(np.quantile(bs, .975)), 'boot_at_cap': float(np.mean(bs >= S_GRID[-1]))})
    return out

def sim_driver(n, alpha, q, s2, rng):
    x = aqn.powerlaw_signal(n, alpha, q, rng)
    return x, x + rng.normal(0, np.sqrt(s2), n)

def ar1(n, phi, sd, rng):
    e = np.empty(n); e[0] = rng.normal(0, sd)
    inn = rng.normal(0, sd * np.sqrt(1 - phi ** 2), n)
    for t in range(1, n): e[t] = phi * e[t - 1] + inn[t]
    return e

def tracker(y, w, rng, r=0.0, phi=0.95, a=-3.0, b=1.0):
    """z_t = a + b (w * y)_t + AR(1) noise with sd = r * sd(b (w*y)); NaN for t < L-1."""
    f = np.full(len(y), np.nan); f[L - 1:] = lagmat(y) @ w
    sd = r * np.nanstd(b * f)
    return a + b * f + (ar1(len(y), phi, sd, rng) if r > 0 else 0)

# ---- design 2 (after design 1 failed MV10 in simulation): horizon-aligned lag bins, unrestricted OLS
EDGES = [0, 1, 2, 5, 10, 21, 42, 84, 168, 336, 504]      # bin j = ages EDGES[j] .. EDGES[j+1]-1
TAIL_PTS = [21, 42, 84, 168, 336]

def bin_stats(beta):
    """beta = per-bin coefficients on bin sums -> per-lag weight in bin; returns tail share W21 (weight on ages >= 21
    over total) and survival slope over ages 21..336 (log S(tau) on log tau, 5 points; NaN if any S <= 0)."""
    sizes = np.diff(EDGES); mass = beta * sizes; tot = mass.sum()
    j21 = EDGES.index(21)
    W21 = mass[j21:].sum() / tot
    S = np.array([mass[EDGES.index(t):].sum() / tot for t in TAIL_PTS])
    slope = np.polyfit(np.log(TAIL_PTS), np.log(S), 1)[0] if np.all(S > 0) else np.nan
    return W21, -slope

def fit_bins(z, y, nboot=0, seed=0):
    X = lagmat(y); zz = z[L - 1:]
    ok = np.isfinite(zz); X, zz = X[ok], zz[ok]
    B = np.stack([X[:, EDGES[j]:EDGES[j + 1]].sum(1) for j in range(len(EDGES) - 1)], 1)
    B = np.concatenate([np.ones((len(B), 1)), B], 1)
    nb = len(zz) // BLOCK; m = nb * BLOCK; B, zz = B[:m], zz[:m]
    XtX = np.einsum('kti,ktj->kij', B.reshape(nb, BLOCK, -1), B.reshape(nb, BLOCK, -1))
    Xtz = np.einsum('kti,kt->ki', B.reshape(nb, BLOCK, -1), zz.reshape(nb, BLOCK))
    def est(wt):
        b = np.linalg.solve(np.tensordot(wt, XtX, 1), wt @ Xtz)[1:]
        return bin_stats(b)
    W21, st = est(np.ones(nb))
    out = {'W21': float(W21), 's_tail': float(st), 'rows': int(m)}
    if nboot:
        rng = np.random.default_rng(seed)
        bs = np.array([est(np.bincount(rng.integers(0, nb, nb), minlength=nb).astype(float)) for _ in range(nboot)])
        out.update({'W21_sd': float(np.nanstd(bs[:, 0], ddof=1)), 's_tail_sd': float(np.nanstd(bs[:, 1], ddof=1)),
                    's_tail_nan': float(np.mean(np.isnan(bs[:, 1]))),
                    'W21_q': [float(np.quantile(bs[:, 0], .025)), float(np.quantile(bs[:, 0], .975))]})
    return out
