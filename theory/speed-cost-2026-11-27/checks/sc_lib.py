"""sc_lib.py: capped-rate memory tracking a symmetric telegraph. Helpers for theory/speed-cost-2026-11-27.

World: x in {0,1}, flips at rate r in each direction (r = 1 sets the time unit).  Memory: n states.
Memory jumps i->j at rate W[x,i,j] (may depend on x; the world never jumps with the memory: bipartite).
Local detailed balance: the heat the memory's bath receives, in units of kT, per unit time, is
    Q = sum_{x,i != j} p[x,i] W[x,i,j] ln( W[x,i,j] / W[x,j,i] ).
Decision error: Hamming error of a decoder lam in {0,1}^n (guess for x given the memory state), eps = P(lam[m] != x).
Caps (rate unit: r = 1, so G = g/r):
    'exit': sum_j W[x,i,j] <= G for every (x,i)        (bounded escape rate of every memory state; primary arm)
    'edge': W[x,i,j] <= G for every edge                (bounded rate of every single transition; secondary arm)
Floor (CORE.md:74): Q >= r L(eps), L(eps) = (1-2 eps) ln((1-eps)/eps).
"""
import itertools
import numpy as np
from scipy.optimize import minimize

LOWER = 1e-9   # lowest allowed rate, as a fraction of G (every transition is reversible, so heat is finite)

def floor_heat(eps, r=1.0):
    return r * (1 - 2 * eps) * np.log((1 - eps) / eps)

def two_state_closed(G, eps, r=1.0):
    """Symmetric two-state copy with the toward-rate at the cap: returns (heat/kT, a_minus, a_plus). Feasible iff eps > r/(G+2r) (a_minus > 0)."""
    a_plus = G
    a_minus = (eps * a_plus - r * (1 - 2 * eps)) / (1 - eps)
    if a_minus <= 0:
        return np.inf, a_minus, a_plus
    return r * (1 - 2 * eps) * np.log(a_plus / a_minus), a_minus, a_plus

def eps_min_two_state(G, r=1.0):
    return r / (G + 2 * r)


def build_generator(W, r=1.0):
    n = W.shape[1]
    N = 2 * n
    A = np.zeros((N, N))
    for x in (0, 1):
        A[x*n:(x+1)*n, x*n:(x+1)*n] = W[x]
    I = np.eye(n)
    A[0:n, n:2*n] += r * I
    A[n:2*n, 0:n] += r * I
    A -= np.diag(A.sum(axis=1))
    return A

def stationary(W, r=1.0):
    A = build_generator(W, r)
    N = A.shape[0]
    M = A.T.copy()
    M[-1, :] = 1.0
    b = np.zeros(N); b[-1] = 1.0
    p = np.linalg.solve(M, b)
    return p.reshape(2, -1)           # p[x, i]

def heat(W, p):
    n = W.shape[1]
    off = ~np.eye(n, dtype=bool)
    q = 0.0
    for x in (0, 1):
        Wx = W[x]
        with np.errstate(divide='ignore', invalid='ignore'):
            L = np.where(off, np.log(Wx / Wx.T), 0.0)
        q += float((p[x][:, None] * Wx * L)[off].sum())
    return q

def error(p, lam):
    n = p.shape[1]
    return float(sum(p[1 - lam[i], i] for i in range(n)))   # guess lam[i] wrong when x = 1 - lam[i]

def best_decoder_error(p):
    return float(np.sum(np.minimum(p[0], p[1])))

def n_edges(n):
    return [(i, j) for i in range(n) for j in range(n) if i != j]

_IDX = {}
def _idx(n):
    if n not in _IDX:
        E = n_edges(n)
        _IDX[n] = (np.array([i for i, j in E]), np.array([j for i, j in E]))
    return _IDX[n]

def unpack(z, n, G):
    I, J = _idx(n)
    m = len(I)
    W = np.zeros((2, n, n))
    for x in (0, 1):
        W[x, I, J] = G * np.exp(z[x * m:(x + 1) * m])
    return W

def exit_sums(W):
    return W.sum(axis=2)   # [x, i]

def evaluate(z, n, G, lam, r=1.0):
    W = unpack(z, n, G)
    p = stationary(W, r)
    return heat(W, p), error(p, lam), W, p

def solve_point(n, G, eps0, lam, cap, z0, r=1.0, maxiter=400):
    """Minimize heat subject to error(lam) <= eps0 and the cap, from start z0 (log of W/G). Returns dict or None."""
    nv = 2 * n * (n - 1)
    lo = np.log(LOWER)
    cache = {}
    def ev(z):
        key = z.tobytes()
        if key not in cache:
            if len(cache) > 4000:
                cache.clear()
            W = unpack(z, n, G); p = stationary(W, r)
            cache[key] = (heat(W, p), error(p, lam))
        return cache[key]
    def f(z):
        return ev(z)[0]
    def c_eps(z):
        return eps0 - ev(z)[1]
    cons = [{'type': 'ineq', 'fun': c_eps}]
    if cap == 'exit':
        def c_exit(z):
            W = unpack(z, n, G); return (G - exit_sums(W)).ravel() / G
        cons.append({'type': 'ineq', 'fun': c_exit})
    bounds = [(lo, 0.0)] * nv
    try:
        res = minimize(f, z0, method='SLSQP', bounds=bounds, constraints=cons,
                       options={'maxiter': maxiter, 'ftol': 1e-14})
    except Exception:
        return None
    z = np.clip(res.x, lo, 0.0)
    W = unpack(z, n, G); p = stationary(W, r)
    e = error(p, lam); q = heat(W, p)
    capviol = 0.0
    if cap == 'exit':
        capviol = float(max(0.0, (exit_sums(W) - G).max() / G))
    return {'heat': float(q), 'eps': e, 'z': z, 'capviol': capviol, 'ok': (e <= eps0 + 1e-7) and capviol <= 1e-7}

def labelings(n):
    """Decoder classes up to memory permutation and the x-swap: k memory states decode to 0, n-k to 1, k = 1..floor(n/2)."""
    return [tuple([0] * k + [1] * (n - k)) for k in range(1, n // 2 + 1)]

def random_start(n, G, rng, cap):
    nv = 2 * n * (n - 1)
    lo = np.log(LOWER)
    z = rng.uniform(lo, 0.0, size=nv) * rng.choice([0.15, 0.4, 1.0])
    if cap == 'exit':
        W = unpack(z, n, G)
        scale = max(1.0, (exit_sums(W) / G).max())   # shrink uniformly so every exit sum <= G
        z = z - np.log(scale) - 1e-3
    return z

def embedded_two_state_start(n, G, eps0, lam, r=1.0):
    """Start from the closed-form two-state copy: states 0..k-1 (label 0) and the rest (label 1) are clones; clones reach each other only at LOWER."""
    heat2, am, ap = two_state_closed(G, eps0, r)
    if not np.isfinite(heat2):
        return None
    k = sum(1 for v in lam if v == 0)
    rep = [0, k]                      # representative states of label 0 and label 1
    W = np.full((2, n, n), G * LOWER)
    for x in (0, 1):
        for i in range(n):
            li = lam[i]
            ri = rep[li]
            other = rep[1 - li]
            aligned = (li == x)
            # state i has the same outgoing rates as the two-state copy: to the other label's representative
            rate = am if aligned else ap
            W[x, i, other] = rate
    z = np.log(np.clip(W / G, LOWER, 1.0))
    out = []
    for x in (0, 1):
        for (i, j) in n_edges(n):
            out.append(z[x, i, j])
    return np.array(out)
