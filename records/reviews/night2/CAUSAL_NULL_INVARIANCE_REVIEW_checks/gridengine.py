"""Independent reviewer code (PR #70 review). Imports nothing from the author's CAUSAL_NULL_INVARIANCE/.
Exact (deterministic) discrete-time computation on a state grid for a 1-D filter z driven by a sampled telegraph world:
  each sample k: the state x in {+1,-1} flips with prob p = (1 - exp(-2 lam D))/2, then y = x*mu + sqrt(N/D)*eps,
  then z <- f(z) + g*y.  Decision sign(z).
Outputs: stationary joint law of (z, x); error rate P(z*x <= 0); 'switch-law' adaptation time = D * E[n], n = first sample
(n >= 1, counting the first post-switch sample as 1) with z*x_new > 0, starting from the stationary law of z given the
pre-switch state, with passages overtaken by a later switch dropped (weight (1-p)^(n-1)), i.e. the estimator of a
stationary record. Grid: cell-integrated Gaussian transition (CDF differences), 0 is a cell edge."""
import numpy as np, math
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.special import ndtr

def make_grid(zmax, h):
    n = int(math.ceil(zmax / h))
    edges = np.arange(-n, n + 1) * h
    return edges, 0.5 * (edges[1:] + edges[:-1])

def kernel(fz, shift, sd, edges, cut=9.0):
    """Sparse matrix K[i, j] = P(z' in cell j | z = centre i) for z' ~ N(fz[i] + shift, sd^2); tails folded into end cells."""
    n = len(fz); h = edges[1] - edges[0]; lo = edges[0]
    rows, cols, vals = [], [], []
    w = int(math.ceil(cut * sd / h)) + 2
    for i in range(n):
        m = fz[i] + shift
        jc = int((m - lo) // h)
        j0 = max(jc - w, 0); j1 = min(jc + w, n - 1)
        if j0 > j1:
            j0 = j1 = (0 if jc < 0 else n - 1)
        e = edges[j0:j1 + 2]
        c = ndtr((e - m) / sd)
        v = np.diff(c)
        v[0] += c[0]; v[-1] += 1 - c[-1]
        rows.append(np.full(len(v), i)); cols.append(np.arange(j0, j1 + 1)); vals.append(v)
    return sparse.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))

def analyse(f, g, lam, mu, N, D, zmax, h, nmax=200000, tol=1e-13):
    edges, zc = make_grid(zmax, h)
    n = len(zc)
    p = (1 - math.exp(-2 * lam * D)) / 2
    sd = abs(g) * math.sqrt(N / D)
    fz = f(zc)
    Kp = kernel(fz, g * mu, sd, edges)    # next state x' = +1
    Km = kernel(fz, -g * mu, sd, edges)   # x' = -1
    # joint chain on (z, x): order [x=+1 block, x=-1 block]; P((z,x)->(z',x')) = T(x,x') K_{x'}(z,z')
    P = sparse.bmat([[(1 - p) * Kp, p * Km], [p * Kp, (1 - p) * Km]], format='csr')
    A = (P.T - sparse.identity(2 * n, format='csr')).tolil()
    A[0, :] = np.ones(2 * n)
    b = np.zeros(2 * n); b[0] = 1.0
    pi = spsolve(A.tocsc(), b)
    pi = np.maximum(pi, 0); pi /= pi.sum()
    pip, pim = pi[:n], pi[n:]
    pos = zc > 0
    err = pip[~pos].sum() + pim[pos].sum()
    # adaptation: start = law of z given x = -1 (pre-switch), then x = +1 for all later samples
    v = pim / pim.sum()
    KpT = Kp.T.tocsr()
    neg = ~pos
    num = 0.0; den = 0.0; surv = 1.0; k = 0; num2 = 0.0
    while True:
        k += 1
        v = KpT @ v
        hit = v[pos].sum()
        wgt = (1 - p) ** (k - 1)
        num += k * hit * wgt; num2 += k * k * hit * wgt; den += hit * wgt
        v[pos] = 0.0
        if v.sum() < tol or k >= nmax:
            break
    tA = D * num / den
    sdT = D * math.sqrt(num2 / den - (num / den) ** 2)
    return dict(err=float(err), tA=float(tA), cvT=sdT / tA, left=float(v.sum()), steps=k, n=n,
                edge_mass=float(pi[[0, n - 1, n, 2 * n - 1]].sum()))

def linear_f(a):
    return lambda z: a * z

def bayes_f(p):
    def f(L):
        Lc = np.clip(L, -50, 50); e = np.exp(Lc)
        return np.log(((1 - p) * e + p) / (p * e + 1 - p))
    return f

def kalman_pole(lam, mu, N, D):
    """Own steady-state Riccati for the OU world with the same covariance: x_k = phi x_{k-1} + w, Var w = mu^2 (1-phi^2)."""
    phi = math.exp(-2 * lam * D); Q = mu * mu * (1 - phi * phi); R = N / D
    # steady prior variance Pm solves Pm = phi^2 Pm R/(Pm+R) + Q  -> quadratic
    # Pm^2 + Pm (R - phi^2 R - Q) - Q R = 0
    bq = R * (1 - phi * phi) - Q
    Pm = (-bq + math.sqrt(bq * bq + 4 * Q * R)) / 2
    K = Pm / (Pm + R)
    return (1 - K) * phi, K
