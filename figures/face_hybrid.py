"""Exact MSE of a nested design (local stores on own reads at lead 0 + shared stores on pooled reads, used `lead` late)
for a world of OU modes shared across n units with shared fraction rho.  Store class of THEORY (first-order stores)."""
import numpy as np
from scipy.linalg import solve_continuous_lyapunov, expm
from scipy.optimize import minimize

def mse(a, v, N, n, rho, lead, bl, bc):
    a = np.asarray(a, float); v = np.asarray(v, float); J = len(a)
    vm = v * (rho + (1 - rho) / n); vd = v - vm
    bl = np.asarray(bl, float); bc = np.asarray(bc, float); kl, kc = len(bl), len(bc)
    d = 2 * J + kl + kc
    A = np.zeros((d, d)); A[:J, :J] = -np.diag(a); A[J:2*J, J:2*J] = -np.diag(a)
    for i, b in enumerate(bl):
        r = 2 * J + i; A[r, :2*J] = b; A[r, r] = -b
    for i, b in enumerate(bc):
        r = 2 * J + kl + i; A[r, :J] = b; A[r, r] = -b
    Q = np.zeros((d, d)); Q[:J, :J] = np.diag(2 * a * vm); Q[J:2*J, J:2*J] = np.diag(2 * a * vd)
    b = np.concatenate([bl, bc]); dens = np.full((kl + kc, kl + kc), N / n); dens[:kl, :kl] = N
    Q[2*J:, 2*J:] = dens * np.outer(b, b)
    P = solve_continuous_lyapunov(A, -Q); P = (P + P.T) / 2
    if kl + kc == 0: return float(v.sum())
    L = expm(A * lead) @ P if (kc and lead > 0) else P          # L[i,j] = Cov(X_i(t), X_j(t-lead))
    li = np.arange(2*J, 2*J + kl); ci = np.arange(2*J + kl, d); s = np.arange(2*J)
    M = np.zeros((kl + kc, kl + kc))
    M[:kl, :kl] = P[np.ix_(li, li)]; M[kl:, kl:] = P[np.ix_(ci, ci)]
    M[:kl, kl:] = L[np.ix_(li, ci)]; M[kl:, :kl] = M[:kl, kl:].T
    r = np.concatenate([P[np.ix_(s, li)].sum(0), L[np.ix_(s, ci)].sum(0)])
    try: g = np.linalg.solve(M, r)
    except np.linalg.LinAlgError: g = np.linalg.lstsq(M, r, rcond=None)[0]
    e = float(v.sum() - r @ g)
    return e if np.isfinite(e) else 1e9

def best(a, v, N, n, rho, lead, kl, kc, starts=6, seed=0):
    if kl + kc == 0: return float(np.sum(v)), None
    a = np.asarray(a, float); rng = np.random.default_rng(seed)
    la = np.log(a); lo, hi = la.min() - 3, la.max() + 7
    def f(x):
        xl = np.sort(x[:kl]); xc = np.sort(x[kl:])
        bl = np.exp(np.clip(xl, -40, 25)) * (1 + 1e-6 * np.arange(kl)); bc = np.exp(np.clip(xc, -40, 25)) * (1 + 1e-6 * np.arange(kc))
        try: return mse(a, v, N, n, rho, lead, bl, bc)
        except Exception: return 1e9
    inits = [np.concatenate([np.linspace(lo + 2, hi - 2, kl), np.linspace(lo + 1, hi - 3, kc)])]
    inits += [rng.uniform(lo, hi, kl + kc) for _ in range(starts)]
    bestv = (np.inf, None)
    for x0 in inits:
        res = minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-12, maxiter=3000 * (kl + kc)))
        if res.fun < bestv[0]: bestv = (res.fun, res.x)
    return bestv

# ---- closed-form covariances (same model, about 50x faster; checked against mse() in tools/test_face_map.py) ----
def _F0(a, bk, bl):
    """Cov of two first-order stores (rates bk, bl) driven by one unit-variance OU component of rate a, same time."""
    return bk * bl / (bk + bl) * (1 / (a + bk) + 1 / (a + bl))

def _Flag(a, b1, b2, lag):
    """Cov(x1(t), x2(t - lag)) for stores b1, b2 driven by one unit-variance OU component of rate a, lag >= 0."""
    b1 = np.where(np.abs(a - b1) < 1e-9 * (a + b1), b1 * (1 + 1e-7), b1)
    return b1 * b2 * (2 * a * np.exp(-b1 * lag) / ((a * a - b1 * b1) * (b1 + b2)) - np.exp(-a * lag) / ((a - b1) * (a + b2)))

def mse_fast(a, v, N, n, rho, lead, bl, bc):
    a = np.asarray(a, float)[:, None, None]; v = np.asarray(v, float)
    vm = v * (rho + (1 - rho) / n); vv = v[:, None, None]; vmm = vm[:, None, None]
    bl = np.asarray(bl, float); bc = np.asarray(bc, float); kl, kc = len(bl), len(bc)
    if kl + kc == 0: return float(v.sum())
    M = np.zeros((kl + kc, kl + kc)); r = np.zeros(kl + kc)
    if kl:
        BK, BL = bl[None, :, None], bl[None, None, :]
        M[:kl, :kl] = (vv * _F0(a, BK, BL)).sum(0) + N * np.outer(bl, bl) / (bl[:, None] + bl[None, :])
        r[:kl] = (vv[:, :, 0] * bl[None, :] / (a[:, :, 0] + bl[None, :])).sum(0)
    if kc:
        BK, BL = bc[None, :, None], bc[None, None, :]
        M[kl:, kl:] = (vmm * _F0(a, BK, BL)).sum(0) + (N / n) * np.outer(bc, bc) / (bc[:, None] + bc[None, :])
        r[kl:] = (vmm[:, :, 0] * bc[None, :] * np.exp(-a[:, :, 0] * lead) / (a[:, :, 0] + bc[None, :])).sum(0)
    if kl and kc:
        B1, B2 = bl[None, :, None], bc[None, None, :]
        X = (vmm * _Flag(a, B1, B2, lead)).sum(0) + (N / n) * np.outer(bl, bc) * np.exp(-bl[:, None] * lead) / (bl[:, None] + bc[None, :])
        M[:kl, kl:] = X; M[kl:, :kl] = X.T
    try: g = np.linalg.solve(M, r)
    except np.linalg.LinAlgError: g = np.linalg.lstsq(M, r, rcond=None)[0]
    e = float(v.sum() - r @ g)
    return e if np.isfinite(e) else 1e9

def best_fast(a, v, N, n, rho, lead, kl, kc, starts=6, seed=0):
    if kl + kc == 0: return float(np.sum(v)), None
    a = np.asarray(a, float); rng = np.random.default_rng(seed)
    la = np.log(a); lo, hi = la.min() - 3, la.max() + 7
    def f(x):
        bl = np.exp(np.clip(np.sort(x[:kl]), -40, 25)) * (1 + 1e-6 * np.arange(kl)); bc = np.exp(np.clip(np.sort(x[kl:]), -40, 25)) * (1 + 1e-6 * np.arange(kc))
        with np.errstate(all='ignore'):
            return mse_fast(a, v, N, n, rho, lead, bl, bc)
    inits = [np.concatenate([np.linspace(lo + 2, hi - 2, kl), np.linspace(lo + 1, hi - 3, kc)])]
    inits += [rng.uniform(lo, hi, kl + kc) for _ in range(starts)]
    bestv = (np.inf, None)
    for x0 in inits:
        res = minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-12, maxiter=2000 * (kl + kc)))
        if res.fun < bestv[0]: bestv = (res.fun, res.x)
    return bestv
