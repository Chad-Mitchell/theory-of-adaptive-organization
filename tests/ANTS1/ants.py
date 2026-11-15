"""ANTS1 ant implementation (written after PREREG commit d38ff12). Numba; lazy-inflation evaporation."""
import numpy as np
from numba import njit
from world import M

MODE_EVERY = 10
HALF_W = 8          # MODE window = 17 sites
F_FOLLOW = 0.75
K_LOCK = 100.0
ARM_CODE = {"IND": 0, "FOL": 1, "LOCK": 2}

TH = 2 * np.pi * np.arange(M) / M
COS, SIN = np.cos(TH), np.sin(TH)


@njit(cache=True)
def _fw_add(tree, i, v):
    i += 1
    n = tree.shape[0] - 1
    while i <= n:
        tree[i] += v
        i += i & (-i)


@njit(cache=True)
def _fw_build(tree, field):
    n = field.shape[0]
    for i in range(n + 1):
        tree[i] = 0.0
    for i in range(n):
        _fw_add(tree, i, field[i])


@njit(cache=True)
def _fw_find(tree, u):
    # smallest index with prefix sum > u
    n = tree.shape[0] - 1
    pos = 0
    step = 1
    while step * 2 <= n:
        step *= 2
    while step > 0:
        if pos + step <= n and tree[pos + step] <= u:
            pos += step
            u -= tree[pos]
        step //= 2
    if pos >= n:
        pos = n - 1
    return pos


@njit(cache=True)
def _mode(field, half):
    m = field.shape[0]
    w = 0.0
    for j in range(-half, half + 1):
        w += field[j % m]
    best = w
    bi = 0
    for i in range(1, m):
        w += field[(i + half) % m] - field[(i - half - 1) % m]
        if w > best:
            best = w
            bi = i
    return bi


@njit(cache=True)
def run_shared(arm, x, N, e, s_obs, seed, cosv, sinv):
    np.random.seed(seed)
    T = x.shape[0]
    m = cosv.shape[0]
    d = 1.0 - e
    field = np.zeros(m)
    tree = np.zeros(m + 1)
    C = 0.0; S = 0.0; tot = 0.0; G = 1.0
    out_mean = np.empty(T)
    out_mode = np.empty(T // 10)
    use_tree = arm != 0
    sites = np.empty(N, dtype=np.int64)
    for t in range(T):
        # 1) readouts of the trail as left by the previous step (F_{t-1})
        if tot > 0.0:
            ang = np.arctan2(S, C)
            if ang < 0:
                ang += 2 * np.pi
            out_mean[t] = ang / (2 * np.pi) * m
        else:
            out_mean[t] = np.nan
        if t % 10 == 0:
            out_mode[t // 10] = _mode(field, 8) if tot > 0.0 else np.nan
        # 2) each ant decides (followers sample the trail they see, F_{t-1})
        Sabs = tot / G
        if arm == 1:
            p = 0.75
        elif arm == 2:
            p = Sabs * Sabs / (Sabs * Sabs + 100.0 * 100.0)
        else:
            p = 0.0
        tot_now = tot
        for a in range(N):
            if p > 0.0 and tot_now > 0.0 and np.random.random() < p:
                sites[a] = _fw_find(tree, np.random.random() * tot_now)
            else:
                sites[a] = int(np.floor(x[t] + s_obs * np.random.standard_normal() + 0.5)) % m
        # 3) evaporation: F <- (1-e) F
        if d <= 0.0:
            for i in range(m):
                field[i] = 0.0
            if use_tree:
                for i in range(m + 1):
                    tree[i] = 0.0
            C = 0.0; S = 0.0; tot = 0.0; G = 1.0
        else:
            G /= d
            if G > 1e100:
                for i in range(m):
                    field[i] /= G
                C /= G; S /= G; tot /= G
                if use_tree:
                    _fw_build(tree, field)
                G = 1.0
        # 4) deposits
        for a in range(N):
            site = sites[a]
            field[site] += G
            if use_tree:
                _fw_add(tree, site, G)
            C += G * cosv[site]; S += G * sinv[site]; tot += G
    return out_mean, out_mode


@njit(cache=True)
def run_private(x, n_ants, e, s_obs, seed, cosv, sinv):
    np.random.seed(seed)
    T = x.shape[0]
    m = cosv.shape[0]
    d = 1.0 - e
    field = np.zeros((n_ants, m))
    C = np.zeros(n_ants); S = np.zeros(n_ants); tot = np.zeros(n_ants)
    G = 1.0
    out_mean = np.empty((n_ants, T))
    out_mode = np.empty((n_ants, T // 10))
    for t in range(T):
        for a in range(n_ants):
            if tot[a] > 0.0:
                ang = np.arctan2(S[a], C[a])
                if ang < 0:
                    ang += 2 * np.pi
                out_mean[a, t] = ang / (2 * np.pi) * m
            else:
                out_mean[a, t] = np.nan
            if t % 10 == 0:
                out_mode[a, t // 10] = _mode(field[a], 8) if tot[a] > 0.0 else np.nan
        if d <= 0.0:
            field[:, :] = 0.0
            C[:] = 0.0; S[:] = 0.0; tot[:] = 0.0; G = 1.0
        else:
            G /= d
            if G > 1e100:
                field /= G; C /= G; S /= G; tot /= G
                G = 1.0
        for a in range(n_ants):
            site = int(np.floor(x[t] + s_obs * np.random.standard_normal() + 0.5)) % m
            field[a, site] += G
            C[a] += G * cosv[site]; S[a] += G * sinv[site]; tot[a] += G
    return out_mean, out_mode
