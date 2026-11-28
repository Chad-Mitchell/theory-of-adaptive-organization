#!/usr/bin/env python3
"""T27 helpers: Model S reduced cost J, weak-mutation Moran, Boltzmann, scoring.

Import of the merged #116 solver follows core/keystone_checks/s5_rerun.py:
theory/layers_checks/stores.py is loaded under a unique name so the pre-#116
copy in core/keystone_checks/ cannot win.
"""
from __future__ import annotations

import importlib.util
import math
from itertools import combinations
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
MERGED_STORES = REPO / "theory" / "layers_checks" / "stores.py"

spec = importlib.util.spec_from_file_location("stores_merged_t27", MERGED_STORES)
stores = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stores)

# ---- seeds already used by Model S generators in this repository ----
# s5 / convexity_targeted: np.random.default_rng(1000 + seed) for seed in 0..119
S5_RNG_SEEDS = set(range(1000, 1120))
# convexity_search.py: default_rng(seed) for seed in 0..119, plus rng(7) for a helper
CONV_SEARCH_SEEDS = set(range(0, 120)) | {7}
# convexity_wide.py: default_rng(5000 + seed)
WIDE_RNG_SEEDS = set(range(5000, 5120))  # generous upper bound
# holographic T20 BASE_SEED and rhythm BASE_SEED
NAMED_SEEDS = {20261120, 2026112020, 1, 11, 3}


def s5_world_from_rng_seed(rng_seed: int):
    """Same distribution as s5_rerun.world / convexity_targeted.world, but
    the RNG seed is passed in directly (s5 uses 1000+seed)."""
    rng = np.random.default_rng(rng_seed)
    J = int(rng.integers(3, 5))
    sep = 10 ** rng.uniform(0.5, 2.0, J - 1)
    taus = np.cumprod(np.r_[10 ** rng.uniform(0, 1), sep])
    v = 10 ** rng.uniform(-1.5, 1.5, J)
    N = 10 ** rng.uniform(-2, 1)
    return np.asarray(1 / taus, float), np.asarray(v, float), float(N)


def seed_collides(rng_seed: int) -> bool:
    if rng_seed in S5_RNG_SEEDS or rng_seed in CONV_SEARCH_SEEDS:
        return True
    if rng_seed in WIDE_RNG_SEEDS or rng_seed in NAMED_SEEDS:
        return True
    return False


def reduced_J(K: int, E: float, E_inf: float, R: float) -> float:
    """Dimensionless J used in N60 / T20: J = K + R (E / E_inf). K=0 allowed."""
    if not np.isfinite(E) or not np.isfinite(E_inf) or E_inf <= 0:
        return math.inf
    return float(K + R * (E / E_inf))


def mse_at_rates(a, v, N, b) -> float:
    if b is None or len(b) == 0:
        return float(np.sum(v))
    e, _ = stores.mse_given_b(a, v, np.asarray(b, float), N)
    return float(e)


def log_grid(a, n_grid: int, lo_pad: float, hi_pad: float) -> np.ndarray:
    a = np.asarray(a, float)
    lo = math.log(float(a.min())) - lo_pad
    hi = math.log(float(a.max())) + hi_pad
    return np.linspace(lo, hi, n_grid)


def enumerate_designs(log_b_grid: np.ndarray, K_max: int):
    """Designs: K=0, and strictly increasing index tuples for K=1..K_max.

    A design is a tuple (K, idx) with idx a tuple of increasing grid indices.
    """
    n = len(log_b_grid)
    designs = [(0, ())]
    for K in range(1, K_max + 1):
        for idx in combinations(range(n), K):
            designs.append((K, tuple(idx)))
    return designs


def rates_of(design, log_b_grid):
    K, idx = design
    if K == 0:
        return np.array([])
    return np.exp(log_b_grid[list(idx)])


def compute_J_table(a, v, N, R, designs, log_b_grid):
    E_inf = float(stores.E_inf(a, v, N))
    E0 = float(np.sum(v))
    Js = np.empty(len(designs), dtype=float)
    Es = np.empty(len(designs), dtype=float)
    for i, des in enumerate(designs):
        E = mse_at_rates(a, v, N, rates_of(des, log_b_grid))
        Es[i] = E
        Js[i] = reduced_J(des[0], E, E_inf, R)
    return dict(J=Js, E=Es, E_inf=E_inf, E0=E0)


def neighbor_edges(designs):
    """Undirected edges: move one index by ±1 (staying strictly increasing),
    or add/drop a single index (K changes by 1). Symmetric by construction.
    """
    index = {des: i for i, des in enumerate(designs)}
    edges = []
    seen = set()
    for i, (K, idx) in enumerate(designs):
        idx = list(idx)
        # nudge
        for p in range(K):
            for d in (-1, 1):
                new = idx.copy()
                new[p] += d
                if new[p] < 0:
                    continue
                if K > 0 and p > 0 and new[p] <= new[p - 1]:
                    continue
                if p < K - 1 and new[p] >= new[p + 1]:
                    continue
                # also need new[p] < n_grid: combinations only used existing
                cand = (K, tuple(new))
                j = index.get(cand)
                if j is None or j == i:
                    continue
                a, b = (i, j) if i < j else (j, i)
                if (a, b) not in seen:
                    seen.add((a, b))
                    edges.append((a, b))
        # drop one store (the inverse "add" edge is the same undirected edge,
        # so it is recorded when the higher-K design is visited, or here).
        # For locality, a K+1 design is a neighbor of a K design only when the
        # added index sits next to the occupied set (or any index, when K=0).
        if K >= 1:
            for p in range(K):
                new = tuple(idx[q] for q in range(K) if q != p)
                # locality: the dropped index must have been adjacent to what remains,
                # except K=1 -> K=0, which is always allowed.
                if K > 1:
                    dropped = idx[p]
                    remaining = set(new)
                    if not any(abs(dropped - u) == 1 for u in remaining):
                        continue
                cand = (K - 1, new)
                j = index.get(cand)
                if j is None:
                    continue
                a, b = (i, j) if i < j else (j, i)
                if (a, b) not in seen:
                    seen.add((a, b))
                    edges.append((a, b))
    return edges


def adjacency_from_edges(n, edges):
    adj = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)
    return adj


def moran_fixation(r_mut: float, r_wt: float, N_pop: int) -> float:
    """Haploid Moran fixation probability of a single mutant with birth rate
    r_mut in a wild-type background of birth rate r_wt, population N_pop.

    Numerically stable for large N: uses logs so gamma**N never overflows.
    The identity (1-γ)/(1-γ^N) is unchanged.
    """
    if r_mut <= 0 or r_wt <= 0 or not np.isfinite(r_mut) or not np.isfinite(r_wt):
        return 0.0
    if abs(r_mut - r_wt) < 1e-15 * max(r_mut, r_wt):
        return 1.0 / N_pop
    log_gamma = math.log(r_wt) - math.log(r_mut)
    nlog = N_pop * log_gamma
    if abs(nlog) < 1e-12:
        return 1.0 / N_pop
    if log_gamma > 0:
        # deleterious: (γ-1)/(γ^N-1) = (γ-1) exp(-N log γ) / (1 - exp(-N log γ))
        if nlog > 700.0:
            return 0.0
        e = math.exp(-nlog)
        return float((math.exp(log_gamma) - 1.0) * e / (1.0 - e))
    # advantageous: (1-γ)/(1-γ^N)
    if nlog < -700.0:
        return float(1.0 - math.exp(log_gamma))
    g = math.exp(log_gamma)
    gN = math.exp(nlog)
    return float((1.0 - g) / (1.0 - gN))


def birth_rates_from_J(J, alpha: float):
    """Wrightian fitness r = exp(m) with Malthusian m = -alpha J."""
    J = np.asarray(J, float)
    # subtract min for numerical stability; relative rates unchanged
    m = -alpha * (J - np.nanmin(J[np.isfinite(J)]))
    r = np.exp(m)
    r[~np.isfinite(J)] = 0.0
    return r


def beta_from_alpha(alpha: float, N_pop: int) -> float:
    return float(alpha * (N_pop - 1))


def alpha_from_beta(beta: float, N_pop: int) -> float:
    return float(beta / (N_pop - 1))


def exact_boltzmann(J, beta: float):
    J = np.asarray(J, float)
    finite = np.isfinite(J)
    w = np.zeros_like(J, dtype=float)
    if not finite.any():
        return w
    M = J[finite].min()
    w[finite] = np.exp(-beta * (J[finite] - M))
    s = w.sum()
    if s <= 0:
        return w
    w /= s
    return w


def boltzmann_stats(J, pi, d_star, star_index):
    J = np.asarray(J, float)
    Jstar = float(J[star_index])
    excess = float(np.dot(pi, J) - Jstar)
    return dict(
        Jstar=Jstar,
        mean_J=float(np.dot(pi, J)),
        excess=excess,
        beta_excess=None,  # filled by caller
        mass_at_star=float(pi[star_index]),
        mode=int(np.argmax(pi)),
    )


def hessian_K2(a, v, N, R, E_inf, log_b_star, h=1e-3):
    """Central-difference Hessian of reduced J in the two log-rates, at an
    interior K=2 point. Returns (H, eigenvalues, ok).
    """
    x0 = np.asarray(log_b_star, float).copy()

    def f(x):
        b = np.exp(np.sort(x))
        E = mse_at_rates(a, v, N, b)
        return reduced_J(2, E, E_inf, R)

    H = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            if i <= j:
                def shift(di, dj):
                    x = x0.copy()
                    x[i] += di * h
                    x[j] += dj * h
                    return f(x)
                if i == j:
                    H[i, i] = (shift(1, 0) - 2 * f(x0) + shift(-1, 0)) / (h * h)
                else:
                    val = (shift(1, 1) - shift(1, -1) - shift(-1, 1) + shift(-1, -1)) / (4 * h * h)
                    H[i, j] = H[j, i] = val
    ev = np.linalg.eigvalsh(H)
    ok = bool(np.all(np.isfinite(H)) and ev[0] > 0)
    return H, ev, ok


def run_moran_chain(J, edges, beta, N_pop, n_steps, burn, rng, start):
    """Weak-mutation Moran on the undirected design graph with symmetric
    mutation rates (each edge proposed equally often). Stationary distribution
    is exactly Boltzmann: pi_i ∝ exp(-beta J_i), with beta = alpha*(N_pop-1).

    Each step: pick a uniform random edge incident to the current state if any,
    but to keep mu_ij = mu_ji we pick a uniform random edge of the whole graph
    and ignore it if it does not touch the current state (or, equivalently,
    each edge rings as a Poisson clock). Here we use discrete time: propose a
    uniform random edge of the graph; if it is incident to the current state,
    attempt fixation of the other end.
    """
    alpha = alpha_from_beta(beta, N_pop)
    r = birth_rates_from_J(J, alpha)
    n = len(J)
    adj = adjacency_from_edges(n, edges)
    # Precompute incident edges as (neighbor, ...)
    state = int(start)
    visits = np.zeros(n, dtype=np.int64)
    # After burn-in, count occupation of the current state once per accepted
    # or rejected proposal that is incident (a standard embedded jump of the
    # holding chain). To estimate the continuous-time occupation with equal
    # edge rates, the holding time at i is Exponential(deg_i * mu), so the
    # jump-chain occupation is *not* Boltzmann — it is Boltzmann * degree
    # if we sample the jump chain, unless we weight by 1/deg or use the
    # 'pick a global edge, ignore if not incident' scheme, whose accepted
    # holding (including ignored proposals) is uniform in time.
    #
    # Official scheme: each step pick a uniform random edge among all edges.
    # If the edge is incident, attempt Moran fixation; always count the
    # current state after the step. This realizes equal edge clocks and
    # yields Boltzmann occupation (no degree bias).
    n_edges = len(edges)
    if n_edges == 0:
        visits[state] = max(n_steps - burn, 0)
        return visits, state
    edge_arr = np.asarray(edges, dtype=int)
    # Start burn
    for t in range(n_steps):
        e = int(rng.integers(0, n_edges))
        i, j = int(edge_arr[e, 0]), int(edge_arr[e, 1])
        if state == i:
            mut, wt = j, i
        elif state == j:
            mut, wt = i, j
        else:
            mut = None
        if mut is not None:
            p = moran_fixation(r[mut], r[wt], N_pop)
            if rng.random() < p:
                state = mut
        if t >= burn:
            visits[state] += 1
    return visits, state


def tv_distance(p, q):
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    if p.sum() <= 0 or q.sum() <= 0:
        return 1.0
    p = p / p.sum()
    q = q / q.sum()
    return 0.5 * float(np.abs(p - q).sum())


def argmin_unique(J, tol=1e-14):
    J = np.asarray(J, float)
    m = np.nanmin(J)
    idxs = np.flatnonzero(np.isfinite(J) & (np.abs(J - m) <= tol))
    return int(idxs[0]), idxs


def interior_K2(design, n_grid):
    K, idx = design
    if K != 2:
        return False
    return idx[0] > 0 and idx[1] < n_grid - 1


def qualification_consistency(sigma, N_e, d, Jstar):
    """Compare FRAMEWORK §9 / THEORY §3 band ε=10/(σ N_e) (fractional in J)
    to the equipartition fractional excess d / (2 σ N_e), under the map
    σ = |d log r / d log J| = α J* for r = exp(-α J).
    """
    band = 10.0 / (sigma * N_e)
    typ_frac = d / (2.0 * sigma * N_e)
    return dict(
        band_frac=band,
        typical_frac=typ_frac,
        typical_over_band=typ_frac / band if band else math.inf,
        # typical / band = d/20
        formula_typical_over_band=d / 20.0,
    )


def polish_K2(a, v, N, R, E_inf, log_b0, sep=1.02):
    """Local continuous minimization of reduced J over two log-rates."""
    from scipy.optimize import minimize

    x0 = np.sort(np.asarray(log_b0, float))

    def obj(x):
        xs = np.sort(x)
        if xs[1] < xs[0] + np.log(sep):
            xs[1] = xs[0] + np.log(sep)
        E = mse_at_rates(a, v, N, np.exp(xs))
        return reduced_J(2, E, E_inf, R)

    res = minimize(obj, x0, method="L-BFGS-B", bounds=((x0[0] - 3, x0[1] + 3),) * 2)
    x = np.sort(res.x)
    if x[1] < x[0] + np.log(sep):
        x[1] = x[0] + np.log(sep)
    return x, float(obj(x)), bool(res.success)


def whitened_lattice(H, theta_star, half, n_axis):
    """Product grid in y where J ≈ J* + (1/2)|y|^2, y = L^T (θ - θ*), H = L L^T."""
    L = np.linalg.cholesky(H)
    ys = np.linspace(-half, half, n_axis)
    Y = np.array([(y1, y2) for y1 in ys for y2 in ys], dtype=float)
    # θ = θ* + L^{-T} y
    delta = np.linalg.solve(L.T, Y.T).T
    Theta = theta_star + delta
    return Y, Theta, L, ys


def J_on_thetas(a, v, N, R, E_inf, Theta, K=2):
    Js = np.empty(len(Theta), dtype=float)
    for i, th in enumerate(Theta):
        E = mse_at_rates(a, v, N, np.exp(th))
        Js[i] = reduced_J(K, E, E_inf, R)
    return Js


def lattice_4_edges(n_axis):
    """4-neighbor undirected edges on an n_axis × n_axis row-major grid."""
    edges = []
    def vid(i, j):
        return i * n_axis + j
    for i in range(n_axis):
        for j in range(n_axis):
            u = vid(i, j)
            if j + 1 < n_axis:
                edges.append((u, vid(i, j + 1)))
            if i + 1 < n_axis:
                edges.append((u, vid(i + 1, j)))
    return edges


def run_moran_ct(J, edges, beta, N_pop, n_jumps, burn_jumps, rng, start):
    """Continuous-time weak-mutation Moran: each undirected edge rings at the
    same mutation clock, then fixation occurs with the haploid Moran
    probability. Occupation is integrated in continuous time. Stationary
    distribution is exactly Boltzmann, π ∝ exp(-β J), with β = α(N_pop-1).
    """
    alpha = alpha_from_beta(beta, N_pop)
    r = birth_rates_from_J(J, alpha)
    n = len(J)
    adj = adjacency_from_edges(n, edges)
    state = int(start)
    occ = np.zeros(n, dtype=float)
    # Precompute fixation probabilities on existing edges
    # For speed, compute on the fly (N is small).
    n_done = 0
    # If a state has no neighbors, stay forever
    if not adj[state] and n_jumps == 0:
        return occ, state
    while n_done < n_jumps:
        nbrs = adj[state]
        if not nbrs:
            break
        # Equal edge clocks: attempt rate = degree, then accept with φ.
        deg = len(nbrs)
        dt = rng.exponential(1.0 / deg)
        if n_done >= burn_jumps:
            occ[state] += dt
        k = nbrs[int(rng.integers(0, deg))]
        p = moran_fixation(r[k], r[state], N_pop)
        if rng.random() < p:
            state = k
        n_done += 1
    return occ, state


def connected_from(start, edges, n):
    from collections import deque
    adj = adjacency_from_edges(n, edges)
    seen = {int(start)}
    q = deque([int(start)])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                q.append(w)
    return seen


def coarse_mass_on_K(J, designs, beta, K):
    pi = exact_boltzmann(J, beta)
    return float(sum(pi[i] for i, d in enumerate(designs) if d[0] == K))
