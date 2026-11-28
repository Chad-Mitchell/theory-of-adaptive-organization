#!/usr/bin/env python3
"""Bounded search for a counting rule on rhythms (M_LG, first-order real stores).

N60's increment formula is false here (worked example: two oscillators, R=3,
formula 2 vs argmin 3). A 'paid for as a pair' rule predicts even K* and also
fails on that example. This sweep asks what, if anything, fits.

Optimizer: the independent reviewer's multi-start (informed grids around
oscillator moduli; Nelder-Mead, L-BFGS-B, differential evolution), with the
PR #116 guarded inversion, 2% rate separation, MSE re-evaluated at the
returned rates. No minimum.accumulate on E_K. Lyapunov MSE is a check on the
worked example and on any suspicious E sequence, not a term in the objective.

Run: nice -n 19 python3 rhythm_rule.py
Budget: about 40 minutes, 6 workers. Findings are a candidate, not a law.
"""
from __future__ import annotations
import json, time, sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, differential_evolution
from scipy.integrate import quad
from concurrent.futures import ProcessPoolExecutor, as_completed

DIR = Path(__file__).resolve().parent
DEADLINE_S = 40 * 60
N_WORKERS = 7
R_GRID = [0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0]


# ---- MSE: complex-pole mats + #116 guarded inversion ----
def mats(a, v, b, N):
    a = np.asarray(a); v = np.asarray(v); b = np.asarray(b, float)
    a3 = a[:, None, None]; v3 = v[:, None, None]
    bk = b[None, :, None]; bl = b[None, None, :]
    Ms = np.real((v3 * bk * bl / (bk + bl) * (1/(a3 + bk) + 1/(a3 + bl))).sum(0))
    Mn = N * b[:, None] * b[None, :] / (b[:, None] + b[None, :])
    r  = np.real((v[:, None] * b[None, :] / (a[:, None] + b[None, :])).sum(0))
    return Ms + Mn, r

def mse_guarded(a, v, b, N, rcond=1e-11):
    with np.errstate(all='ignore'):
        M, r = mats(a, v, b, N)
    if not (np.all(np.isfinite(M)) and np.all(np.isfinite(r))):
        return np.inf
    d = np.sqrt(np.clip(np.diag(M), 1e-300, None))
    Ms = M / np.outer(d, d); rs = r / d
    try:
        lam, U = np.linalg.eigh(Ms)
    except np.linalg.LinAlgError:
        return np.inf
    keep = lam > rcond * lam.max()
    if not np.any(keep):
        return np.inf
    c = U[:, keep].T @ rs
    return float(np.real(np.sum(v)) - np.sum(c * c / lam[keep]))

def safe_log_rates(x, sep=1.02):
    x = np.sort(np.clip(np.asarray(x, float), -40, 40))
    for i in range(1, len(x)):
        x[i] = max(x[i], x[i-1] + np.log(sep))
    return x

def E_inf_YJ(a, v, N):
    def S(w):
        return float(np.real(np.sum(v * 2 * a / (a**2 + w**2))))
    def f(x):
        return np.log1p(max(S(np.exp(x)), 0) / N) * np.exp(x)
    lo = np.log(np.abs(a).min()) - 14
    hi = np.log(max(np.abs(a).max(), np.real(np.sum(v)) * 2 * np.abs(a).max() / N)) + 16
    edges = np.linspace(lo, hi, 80)
    tot = 0.0
    for x0, x1 in zip(edges[:-1], edges[1:]):
        tot += quad(f, x0, x1, epsrel=1e-11, epsabs=0, limit=200)[0]
    return N / np.pi * tot

def var0(v):
    return float(np.real(np.sum(v)))


# ---- Lyapunov check (reviewer's realization; real v on conjugate pairs) ----
def world_realization(a, v):
    a = np.asarray(a); v = np.asarray(v)
    used = np.zeros(len(a), dtype=bool)
    blocks_A, blocks_Q, blocks_C = [], [], []
    for i, (ai, vi) in enumerate(zip(a, v)):
        if used[i]:
            continue
        if np.abs(np.imag(ai)) < 1e-14:
            ai_r, vi_r = float(np.real(ai)), float(np.real(vi))
            blocks_A.append(np.array([[-ai_r]]))
            blocks_Q.append(np.array([[2 * ai_r * vi_r]]))
            blocks_C.append(np.array([1.0]))
            used[i] = True
        else:
            js = [j for j in range(len(a)) if (not used[j]) and np.abs(a[j] - np.conj(ai)) < 1e-12]
            if not js:
                raise RuntimeError(f'unmatched complex pole {ai}')
            j = js[0]
            used[i] = used[j] = True
            alpha, omega = float(np.real(ai)), float(np.imag(ai))
            vi_mean = 0.5 * (vi + np.conj(v[j]))
            vr, vimag = float(np.real(vi_mean)), float(np.imag(vi_mean))
            if abs(vimag) > 1e-14:
                raise RuntimeError('complex v not implemented')
            Px = 2 * vr
            Ablk = np.array([[-alpha, -omega], [omega, -alpha]])
            P = np.array([[Px, 0.0], [0.0, Px]])
            Qblk = -(Ablk @ P + P @ Ablk.T)
            blocks_A.append(Ablk)
            blocks_Q.append(Qblk)
            blocks_C.append(np.array([1.0, 0.0]))
    n = sum(b.shape[0] for b in blocks_A)
    A = np.zeros((n, n)); Q = np.zeros((n, n)); C = np.zeros(n)
    i = 0
    for Ab, Qb, Cb in zip(blocks_A, blocks_Q, blocks_C):
        m = Ab.shape[0]
        A[i:i+m, i:i+m] = Ab
        Q[i:i+m, i:i+m] = Qb
        C[i:i+m] = Cb
        i += m
    return A, C, Q

def lyapunov_mse(a, v, b, N):
    from scipy.linalg import solve_continuous_lyapunov
    Aw, Cw, Qw = world_realization(a, v)
    nw = Aw.shape[0]
    b = np.asarray(b, float)
    K = len(b)
    n = nw + K
    A = np.zeros((n, n)); Q = np.zeros((n, n))
    A[:nw, :nw] = Aw
    Q[:nw, :nw] = Qw
    for k, bk in enumerate(b):
        A[nw + k, :nw] = bk * Cw
        A[nw + k, nw + k] = -bk
        for l, bl in enumerate(b):
            Q[nw + k, nw + l] = N * bk * bl
    try:
        P = solve_continuous_lyapunov(A, -Q)
    except Exception as e:
        return dict(error=str(e), mse=np.inf)
    Pxz = P[:nw, nw:]; Pzz = P[nw:, nw:]
    r = Pxz.T @ Cw
    var_s_chk = float(Cw @ P[:nw, :nw] @ Cw)
    try:
        g = np.linalg.solve(Pzz, r)
    except np.linalg.LinAlgError:
        g = np.linalg.lstsq(Pzz, r, rcond=None)[0]
    mse = var_s_chk - 2 * g @ r + g @ Pzz @ g
    return dict(mse=float(mse), Pzz_cond=float(np.linalg.cond(Pzz)))


# ---- reviewer-validated multi-start (slightly trimmed random starts / DE iters) ----
def informed_inits(K, a, lo, hi, rng, n_rand=24):
    freqs = np.sort(np.unique(np.abs(a)))
    inits = [np.linspace(lo + 1, hi - 1, K), np.linspace(lo, hi, K)]
    if K <= 2 * len(freqs) + 2:
        for scale in (0.3, 0.7, 1.0, 1.5, 3.0, 8.0):
            pts = []
            for f in freqs:
                pts.append(np.log(f * scale))
                pts.append(np.log(f * scale) + 0.15)
            x = np.sort(pts)[:K] if len(pts) >= K else np.linspace(lo, hi, K)
            if len(x) < K:
                x = np.r_[x, rng.uniform(lo, hi, K - len(x))]
            inits.append(np.sort(x[:K]))
        if len(freqs) >= 1:
            f_list = list(freqs)
            f1, f2 = f_list[0], f_list[-1]
            if K == 1:
                for f in freqs:
                    for r in (0.3, 1, 3, 10):
                        inits.append(np.array([np.log(f * r)]))
            if K == 2 and len(freqs) == 1:
                f = freqs[0]
                for r1 in (0.5, 1, 4):
                    for d in (0.15, 0.5):
                        inits.append(np.sort([np.log(f * r1) - d, np.log(f * r1) + d]))
            if K == 2 and len(freqs) >= 2:
                for r1 in (0.5, 1, 3, 10):
                    for r2 in (0.5, 1, 3, 10):
                        inits.append(np.sort([np.log(f1 * r1), np.log(f2 * r2)]))
            if K == 3 and len(freqs) >= 2:
                for r1 in (0.5, 1, 4):
                    for r2 in (0.5, 1, 4):
                        inits.append(np.sort([np.log(f1 * r1), np.log(f1 * r1) + 0.2, np.log(f2 * r2)]))
                        inits.append(np.sort([np.log(f1 * r1), np.log(f2 * r2), np.log(f2 * r2) + 0.2]))
            if K == 4 and len(freqs) >= 2:
                for r1 in (0.5, 1, 4):
                    for r2 in (0.5, 1, 4):
                        inits.append(np.sort([np.log(f1 * r1) - 0.15, np.log(f1 * r1) + 0.15,
                                              np.log(f2 * r2) - 0.15, np.log(f2 * r2) + 0.15]))
            # 3-oscillator allocations
            if len(freqs) >= 3 and K in (3, 5, 6):
                for scale in (0.5, 1, 2, 5):
                    logs = [np.log(f * scale) for f in freqs]
                    if K > len(logs):
                        extra = [logs[i % len(logs)] + 0.2 * ((i // len(logs))) for i in range(K - len(logs))]
                        logs = logs + extra
                    inits.append(np.sort(np.array(logs[:K])))
    for _ in range(n_rand):
        inits.append(np.sort(rng.uniform(lo, hi, K)))
    out, seen = [], set()
    for x in inits:
        key = tuple(np.round(x, 5))
        if key not in seen:
            seen.add(key)
            out.append(np.asarray(x, float))
    return out

def optimize_K(a, v, N, K, seed=0, n_rand=16, use_de=True):
    """Reviewer methods (informed starts, NM, L-BFGS-B, DE), budgeted:
    NM on all starts, L-BFGS-B polish on the top few, one DE pass."""
    rng = np.random.default_rng(seed)
    la = np.log(np.abs(a))
    lo, hi = float(la.min() - 5), float(la.max() + 8)

    def obj(x):
        return mse_guarded(a, v, np.exp(safe_log_rates(x)), N)

    inits = informed_inits(K, a, lo, hi, rng, n_rand=n_rand)
    t0 = time.time()
    ranked = []  # (fun, x, method)
    for x0 in inits:
        try:
            r = minimize(obj, x0, method='Nelder-Mead',
                         options=dict(xatol=1e-8, fatol=1e-14, maxiter=2500 * K))
            fun = obj(r.x)
            ranked.append((fun, safe_log_rates(r.x), 'Nelder-Mead'))
        except Exception:
            pass
    ranked.sort(key=lambda t: t[0])
    # L-BFGS-B polish of the best NM starts (and a couple of raw informed starts)
    polish = [t[1] for t in ranked[:5]] + list(inits[:3])
    for x0 in polish:
        try:
            r = minimize(obj, x0, method='L-BFGS-B',
                         bounds=[(lo - 2, hi + 2)] * K,
                         options=dict(ftol=1e-14, maxiter=2000 * K))
            fun = obj(r.x)
            ranked.append((fun, safe_log_rates(r.x), 'L-BFGS-B'))
        except Exception:
            pass
    if use_de:
        try:
            maxiter = 25 if K >= 6 else (40 if K >= 4 else 60)
            popsize = 8 if K >= 5 else 10
            r = differential_evolution(obj, bounds=[(lo - 2, hi + 2)] * K,
                                       popsize=popsize, mutation=0.5, recombination=0.7,
                                       seed=int(seed) % (2**31 - 1), polish=True,
                                       workers=1, atol=1e-12, maxiter=maxiter)
            fun = obj(r.x)
            ranked.append((fun, safe_log_rates(r.x), 'DE'))
        except Exception:
            pass
    if not ranked:
        return dict(E=float('inf'), stores=None, method='none', n_inits=len(inits),
                    elapsed=time.time() - t0)
    ranked.sort(key=lambda t: t[0])
    best = ranked[0]
    b = np.exp(best[1])
    return dict(E=float(best[0]), stores=b.tolist(),
                method=best[2], n_inits=len(inits), elapsed=time.time() - t0)


# ---- rules ----
def eps_from_E(E, Einf):
    # E[0] is K=0 (blind), then K=1..Kmax
    return [float(e / Einf - 1.0) for e in E]

def J_of(eps, R, k0=0):
    # J_K = K + R(1+eps_K); index 0 is K=k0
    return [k0 + k + R * (1.0 + e) for k, e in enumerate(eps)]

def argmin_J(eps, R, k0=0):
    J = J_of(eps, R, k0)
    return int(np.argmin(J) + k0), J

def n60_raw(eps_from1, R):
    """N60 as written: starts at K=1, counts adjacent decrements > 1/R."""
    return 1 + sum(1 for k in range(1, len(eps_from1)) if R * (eps_from1[k - 1] - eps_from1[k]) > 1)

def lower_convex_hull(xs, ys):
    """Indices of the lower convex hull of (xs, ys), left to right. Andrew's monotone chain."""
    pts = list(zip(xs, ys, range(len(xs))))
    if len(pts) <= 2:
        return list(range(len(xs)))
    hull = []
    for p in pts:
        while len(hull) >= 2:
            x0, y0, _ = hull[-2]
            x1, y1, _ = hull[-1]
            # cross <= 0 means not a strict lower-left turn (drop middle)
            if (x1 - x0) * (p[1] - y0) - (y1 - y0) * (p[0] - x0) <= 1e-15:
                hull.pop()
            else:
                break
        hull.append(p)
    return [i for _, _, i in hull]

def hull_increment(eps, R, k0=0):
    """N60 increment rule on the lower convex envelope of ε_K (includes K=k0).

    Walk hull edges from the left. Take a hull jump from Ka to Kb iff
    R(ε_Ka - ε_Kb) > (Kb - Ka), i.e. the average marginal error reduction
    pays for the extra stores. Stop at the last taken vertex. This equals
    argmin_K [K + R(1+ε_K)] except for exact ties (we take the leftmost min
    of J, and the supporting-line walk may land on either end of a flat).
    """
    Ks = [k0 + i for i in range(len(eps))]
    hull = lower_convex_hull(Ks, eps)
    k_star = Ks[hull[0]]
    for a, b in zip(hull, hull[1:]):
        Ka, Kb = Ks[a], Ks[b]
        if R * (eps[a] - eps[b]) > (Kb - Ka) + 1e-15:
            k_star = Kb
        else:
            break
    return int(k_star), [Ks[i] for i in hull]

def even_argmin(eps, R, k0=0):
    """Pair-rule: argmin of J restricted to even K."""
    J = J_of(eps, R, k0)
    even = [(k0 + i, J[i]) for i in range(len(J)) if (k0 + i) % 2 == 0]
    if not even:
        return None
    return min(even, key=lambda t: (t[1], t[0]))[0]

def degree_cap_argmin(eps, R, n_osc, k0=0):
    """Argmin of J restricted to K in {0, 2, 4, ..., 2 n_osc} (pay whole pairs only)."""
    J = J_of(eps, R, k0)
    allowed = set(range(0, 2 * n_osc + 1, 2))
    cands = [(k0 + i, J[i]) for i in range(len(J)) if (k0 + i) in allowed]
    if not cands:
        return None
    return min(cands, key=lambda t: (t[1], t[0]))[0]


# ---- worlds ----
# seed-2 of convexity_wide.py (the worked counterexample)
SEED2_A = np.array([0.015043913155370778+0.8245963835269933j,
                    0.015043913155370778-0.8245963835269933j,
                    0.005596688432223706+0.05512283118769611j,
                    0.005596688432223706-0.05512283118769611j])
SEED2_V = np.array([0.16591255090832438, 0.16591255090832438,
                    0.1809360888442601,  0.1809360888442601], dtype=complex)
SEED2_N = 0.04014640614993535

def osc_world(omegas, zetas, variances, N):
    """n oscillators: poles α±iω with α=ζω, variance split equally, real v."""
    a, v = [], []
    for w, z, vr in zip(omegas, zetas, variances):
        w = float(w); z = float(z); vr = float(vr)
        alpha = z * w
        a += [alpha + 1j * w, alpha - 1j * w]
        v += [vr / 2, vr / 2]
    return np.array(a, dtype=complex), np.array(v, dtype=complex), float(N)

def world_list():
    worlds = []
    # 0. the independently confirmed counterexample
    worlds.append(dict(id='seed2_two_light', n=2, kind='worked example (wide-search seed 2)',
                       zeta='light/light', a=SEED2_A, v=SEED2_V, N=SEED2_N,
                       meta=dict(omegas=[0.05512283118769611, 0.8245963835269933],
                                 zetas=[0.10153, 0.01824], variances=[0.361872, 0.331825])))
    # 1 oscillator: zeta sweep x two noise levels
    for z in (0.02, 0.08, 0.25, 1.0):
        for N in (0.04, 0.2):
            a, v, N_ = osc_world([1.0], [z], [1.0], N)
            worlds.append(dict(id=f'1osc_z{z}_N{N}', n=1, kind='1 oscillator',
                               zeta=str(z), a=a, v=v, N=N_,
                               meta=dict(omegas=[1.0], zetas=[z], variances=[1.0])))
    # 2 oscillators: two frequency separations x four damping patterns, N=0.04
    zeta_pairs = [('light/light', (0.02, 0.02)),
                  ('light/medium', (0.02, 0.25)),
                  ('medium/medium', (0.25, 0.25)),
                  ('heavy/heavy', (1.0, 1.0))]
    for tag, omegas in (('sep15', (0.05, 0.8)), ('close2', (0.5, 1.0))):
        for zname, zs in zeta_pairs:
            a, v, N_ = osc_world(omegas, zs, [0.5, 0.5], 0.04)
            worlds.append(dict(id=f'2osc_{tag}_{zname.replace("/","_")}', n=2, kind='2 oscillators',
                               zeta=zname, a=a, v=v, N=N_,
                               meta=dict(omegas=list(omegas), zetas=list(zs), variances=[0.5, 0.5])))
    # 3 oscillators
    omega3 = (0.05, 0.3, 1.5)
    for zname, zs in (('light/light/light', (0.02, 0.02, 0.02)),
                      ('mixed', (0.02, 0.25, 1.0)),
                      ('medium/medium/medium', (0.25, 0.25, 0.25)),
                      ('heavy/heavy/heavy', (1.0, 1.0, 1.0))):
        a, v, N_ = osc_world(omega3, zs, [1/3, 1/3, 1/3], 0.04)
        worlds.append(dict(id=f'3osc_{zname.replace("/","_")}', n=3, kind='3 oscillators',
                           zeta=zname, a=a, v=v, N=N_,
                           meta=dict(omegas=list(omega3), zetas=list(zs), variances=[1/3, 1/3, 1/3])))
    return worlds


def run_world(spec, seed_base=20261120):
    a, v, N = spec['a'], spec['v'], spec['N']
    n = spec['n']
    Kmax = 2 * n + 2
    t0 = time.time()
    Einf = E_inf_YJ(a, v, N)
    E0 = var0(v)
    rows = []
    E = [E0]
    stores = [[]]
    methods = ['closed']
    for K in range(1, Kmax + 1):
        r = optimize_K(a, v, N, K, seed=seed_base + 17 * K + n, n_rand=16, use_de=(K <= 4))
        E.append(r['E'])
        stores.append(r['stores'])
        methods.append(r['method'])
        rows.append(r)
        print(f"    {spec['id']} K={K} E={r['E']:.8g} meth={r['method']} t={r['elapsed']:.1f}s", flush=True)
    # flags
    incr = [k for k in range(1, len(E)) if E[k] > E[k - 1] + 1e-10]  # K at which E rose
    below = [k for k, e in enumerate(E) if k > 0 and e < Einf - 1e-9]
    # Lyapunov on worked example and on suspicious sequences
    lyap = []
    need_lyap = (spec['id'] == 'seed2_two_light') or bool(incr) or bool(below)
    if need_lyap:
        for K in range(1, len(E)):
            b = stores[K]
            if b is None:
                lyap.append(dict(K=K, mse=None, err='no stores'))
                continue
            try:
                L = lyapunov_mse(a, v, b, N)
                lyap.append(dict(K=K, mse=L.get('mse'), cond=L.get('Pzz_cond'),
                                 err=L.get('error'), gap=None if L.get('mse') is None
                                 else float(L['mse'] - E[K])))
            except Exception as ex:
                lyap.append(dict(K=K, mse=None, err=str(ex)))
    eps = eps_from_E(E, Einf)          # includes K=0
    eps1 = eps[1:]                     # K=1..
    dec = [eps[k] - eps[k + 1] for k in range(len(eps) - 1)]
    convex = all(dec[i] >= dec[i + 1] - 1e-4 for i in range(len(dec) - 1))
    # per-R comparison
    per_R = []
    for R in R_GRID:
        k_arg, J = argmin_J(eps, R, k0=0)
        k_n60 = n60_raw(eps1, R)
        k_hull, hull_K = hull_increment(eps, R, k0=0)
        k_even = even_argmin(eps, R, k0=0)
        k_deg = degree_cap_argmin(eps, R, n, k0=0)
        # also N60-from-0: 0 + count of k>=1 with R(eps_{k-1}-eps_k)>1  (still raw adjacent)
        k_n60_from0 = sum(1 for k in range(1, len(eps)) if R * (eps[k - 1] - eps[k]) > 1)
        per_R.append(dict(
            R=R, J=J, argmin=k_arg,
            n60_raw=k_n60, n60_from0=k_n60_from0,
            hull=k_hull, hull_vertices=hull_K,
            even=k_even, degree_pairs=k_deg,
            n60_match=k_n60 == k_arg,
            n60_from0_match=k_n60_from0 == k_arg,
            hull_match=k_hull == k_arg,
            even_match=k_even == k_arg,
            degree_match=k_deg == k_arg,
            argmin_odd=(k_arg % 2 == 1),
        ))
    out = dict(
        id=spec['id'], n=n, kind=spec['kind'], zeta=spec['zeta'],
        N=N, meta=spec['meta'],
        E=E, E_inf=Einf, eps=eps, decrements=dec, convex=convex,
        stores=stores, methods=methods, incr=incr, below_Einf=below,
        lyap=lyap, per_R=per_R, Kmax=Kmax, elapsed=time.time() - t0,
        # serialize poles as re/im
        a=[[float(z.real), float(z.imag)] for z in a],
        v=[float(np.real(x)) for x in v],
    )
    return out


def summarize(results):
    n_worlds = len(results)
    n_R = n_worlds * len(R_GRID)
    def count(pred):
        return sum(1 for r in results for p in r['per_R'] if pred(p, r))
    odd = count(lambda p, r: p['argmin_odd'])
    n60_miss = count(lambda p, r: not p['n60_match'])
    n60_0_miss = count(lambda p, r: not p['n60_from0_match'])
    hull_miss = count(lambda p, r: not p['hull_match'])
    even_miss = count(lambda p, r: not p['even_match'])
    deg_miss = count(lambda p, r: not p['degree_match'])
    odd_when_light = count(lambda p, r: p['argmin_odd'] and 'light' in r['zeta'])
    # mismatches of N60 where argmin is the interesting case (not just the K=0 hole)
    n60_miss_pos = count(lambda p, r: (not p['n60_match']) and p['argmin'] >= 1)
    # cases like the worked example: n60 != argmin and argmin odd
    n60_miss_odd = count(lambda p, r: (not p['n60_match']) and p['argmin_odd'])
    even_miss_odd = count(lambda p, r: (not p['even_match']) and p['argmin_odd'])
    nonconvex = [r['id'] for r in results if not r['convex']]
    incr = [r['id'] for r in results if r['incr']]
    below = [r['id'] for r in results if r['below_Einf']]
    # show a few representative mismatches
    examples = []
    for r in results:
        for p in r['per_R']:
            if (not p['n60_match']) or (not p['even_match']):
                examples.append(dict(id=r['id'], n=r['n'], zeta=r['zeta'], R=p['R'],
                                     argmin=p['argmin'], n60=p['n60_raw'],
                                     hull=p['hull'], even=p['even'], degree=p['degree_pairs'],
                                     hull_vertices=p['hull_vertices'],
                                     eps=[round(x, 5) for x in r['eps']],
                                     dec=[round(x, 5) for x in r['decrements']]))
                break  # one R per world in the short list; full data is in json
    return dict(
        n_worlds=n_worlds, n_comparisons=n_R, R_grid=R_GRID,
        nonconvex_worlds=nonconvex, n_nonconvex=len(nonconvex),
        incr_E_worlds=incr, below_Einf_worlds=below,
        odd_argmin=odd, odd_when_light_in_zeta_label=odd_when_light,
        mismatches=dict(n60_raw=n60_miss, n60_raw_argmin_ge1=n60_miss_pos,
                        n60_from0=n60_0_miss, n60_raw_and_odd_argmin=n60_miss_odd,
                        hull=hull_miss, even_pair=even_miss,
                        even_and_odd_argmin=even_miss_odd, degree_pairs=deg_miss),
        examples=examples,
    )


def main():
    t0 = time.time()
    worlds = world_list()
    print(f'{len(worlds)} worlds, Kmax=2n+2, R grid {R_GRID}, workers={N_WORKERS}', flush=True)
    results = []
    # run seed2 first in this process as a sanity check, then the rest in the pool
    # seed2 first in the submit order so a worker picks it up immediately
    ordered = [w for w in worlds if w['id'] == 'seed2_two_light'] + [w for w in worlds if w['id'] != 'seed2_two_light']
    with ProcessPoolExecutor(max_workers=N_WORKERS) as ex:
        futs = {ex.submit(run_world, w): w['id'] for w in ordered}
        for fut in as_completed(futs):
            wid = futs[fut]
            if time.time() - t0 > DEADLINE_S + 120:
                print(f'past deadline; skipping remaining after {wid}', flush=True)
            try:
                r = fut.result()
            except Exception as e:
                print(f'FAILED {wid}: {e}', flush=True)
                continue
            results.append(r)
            # print a compact line
            odd_Rs = [p['R'] for p in r['per_R'] if p['argmin_odd']]
            n60_bad = [p['R'] for p in r['per_R'] if not p['n60_match']]
            print(f"  {r['id']}: convex={r['convex']} incr={r['incr']} "
                  f"oddR={odd_Rs} n60_missR={n60_bad} t={r['elapsed']:.1f}s", flush=True)
            # checkpoint
            summary = summarize(results)
            payload = dict(summary=summary, results=results,
                           elapsed=time.time() - t0, n_done=len(results))
            (DIR / 'rhythm_rule.json').write_text(json.dumps(payload, indent=1))
            if time.time() - t0 > DEADLINE_S:
                print('deadline reached; stopping after this completed batch', flush=True)
                # cannot cancel easily; just stop scheduling (already all submitted)
                # we still wait for in-flight jobs (as_completed)
                # but if we're past deadline we continue to collect already running ones
                # and do not start new — already all submitted at once. OK.

    results.sort(key=lambda r: (r['n'], r['id']))
    summary = summarize(results)
    payload = dict(
        note=('Candidate only, not a law. Sweep of 1-3 oscillators x damping x R, '
              'first-order real stores, reviewer multi-start + #116 guarded inversion.'),
        summary=summary, results=results,
        elapsed=time.time() - t0, n_done=len(results), n_planned=len(worlds),
        deadline_s=DEADLINE_S,
    )
    (DIR / 'rhythm_rule.json').write_text(json.dumps(payload, indent=1))
    # human-readable
    lines = []
    s = summary
    lines.append(f"rhythm rule sweep: {s['n_worlds']} worlds, {s['n_comparisons']} (world, R) comparisons, "
                 f"{time.time()-t0:.0f}s")
    lines.append(f"non-convex ε_K worlds: {s['n_nonconvex']} {s['nonconvex_worlds']}")
    lines.append(f"optimizer flags: incr E {s['incr_E_worlds'] or 'none'}; "
                 f"E < E_inf {s['below_Einf_worlds'] or 'none'}")
    lines.append(f"odd argmin: {s['odd_argmin']} / {s['n_comparisons']}")
    m = s['mismatches']
    lines.append(f"mismatches vs argmin J (incl K=0):")
    lines.append(f"  N60 raw (starts at 1): {m['n60_raw']}  (among argmin>=1: {m['n60_raw_argmin_ge1']}; "
                 f"and odd argmin: {m['n60_raw_and_odd_argmin']})")
    lines.append(f"  N60 adjacent from K=0: {m['n60_from0']}")
    lines.append(f"  hull increment (convex envelope of ε_K): {m['hull']}")
    lines.append(f"  even/pair argmin: {m['even_pair']}  (odd-argmin cases: {m['even_and_odd_argmin']})")
    lines.append(f"  degree-pairs (K in 0,2,...,2n): {m['degree_pairs']}")
    lines.append('examples (first mismatching R per world):')
    for e in s['examples']:
        lines.append(f"  {e['id']} R={e['R']}: argmin={e['argmin']} n60={e['n60']} "
                     f"hull={e['hull']} even={e['even']} deg={e['degree']} "
                     f"hullK={e['hull_vertices']} dec={e['dec']}")
    text = '\n'.join(lines) + '\n'
    (DIR / 'rhythm_rule.out').write_text(text)
    print(text, flush=True)
    print('wrote', DIR / 'rhythm_rule.json', 'and', DIR / 'rhythm_rule.out', flush=True)

if __name__ == '__main__':
    main()
