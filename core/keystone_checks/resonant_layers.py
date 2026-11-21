#!/usr/bin/env python3
"""Extended layer library: first-order stores plus resonant (second-order) layers.

Does not modify theory/layers_checks/stores.py. MSE is the exact linear-Gaussian
Lyapunov covariance of world + filter; gains use the PR #116 guarded inversion.
IMP-N60 predictions use only closed-form / Yovits-Jackson quantities (no
library optimizer).

See RHYTHM_PREREG.md (locked 20 Nov 2026, 6:16 PM ET).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Iterable

import numpy as np
from scipy.integrate import quad
from scipy.linalg import solve_continuous_lyapunov
from scipy.optimize import differential_evolution, minimize

# ---------------------------------------------------------------------------
# Modes, spectra, causal floors
# ---------------------------------------------------------------------------

def parse_modes(a, v):
    """Split poles into OU modes (real) and rhythms (conjugate pairs)."""
    a = np.asarray(a)
    v = np.asarray(v)
    used = np.zeros(len(a), dtype=bool)
    modes = []
    for i, (ai, vi) in enumerate(zip(a, v)):
        if used[i]:
            continue
        if abs(np.imag(ai)) < 1e-14:
            used[i] = True
            ar, vr = float(np.real(ai)), float(np.real(vi))
            modes.append(dict(
                kind="ou", c=1, alpha=ar, omega=0.0,
                sigma2=vr,
                poles=np.array([ar], dtype=complex),
                v=np.array([vr], dtype=complex),
            ))
        else:
            js = [j for j in range(len(a))
                  if (not used[j]) and abs(a[j] - np.conj(ai)) < 1e-12]
            if not js:
                raise RuntimeError(f"unmatched complex pole {ai}")
            j = js[0]
            used[i] = used[j] = True
            alpha, omega = float(np.real(ai)), float(np.imag(ai))
            # Keep omega > 0 by convention.
            if omega < 0:
                alpha, omega = float(np.real(a[j])), float(np.imag(a[j]))
            vr = float(np.real(0.5 * (vi + np.conj(v[j]))))
            # Each pole carries vr; the mode variance is 2*vr under the
            # realization used in rhythm_rule.py (Px = 2*vr, C = [1,0]).
            # osc_world stores v_pole = variance/2, so 2*vr = mode variance.
            sigma2 = 2.0 * vr
            modes.append(dict(
                kind="rhythm", c=2, alpha=alpha, omega=omega,
                sigma2=sigma2,
                poles=np.array([alpha + 1j * omega, alpha - 1j * omega], dtype=complex),
                v=np.array([vr, vr], dtype=complex),
            ))
    return modes


def var0(v):
    return float(np.real(np.sum(v)))


def E_inf_YJ(a, v, N, n_edges=80):
    """Yovits-Jackson causal MMSE, same construction as rhythm_rule.py."""
    a = np.asarray(a)
    v = np.asarray(v)

    def S(w):
        return float(np.real(np.sum(v * 2 * a / (a**2 + w**2))))

    def f(x):
        return np.log1p(max(S(np.exp(x)), 0.0) / N) * np.exp(x)

    lo = np.log(max(np.abs(a).min(), 1e-18)) - 14
    hi = np.log(max(np.abs(a).max(),
                    max(np.real(np.sum(v)), 1e-18) * 2 * np.abs(a).max() / max(N, 1e-18))) + 16
    edges = np.linspace(lo, hi, n_edges)
    tot = 0.0
    for x0, x1 in zip(edges[:-1], edges[1:]):
        tot += quad(f, x0, x1, epsrel=1e-11, epsabs=0, limit=200)[0]
    return N / np.pi * tot


def E_inf_OU(a, sigma2, N):
    """Kalman MSE for a single OU mode in white noise density N."""
    a = float(a)
    return float(N * (np.sqrt(a * a + 2 * a * sigma2 / N) - a))


def isolated_Einf(mode, N):
    if mode["kind"] == "ou":
        return E_inf_OU(mode["alpha"], mode["sigma2"], N)
    return E_inf_YJ(mode["poles"], mode["v"], N)


def imp_n60(a, v, N, R, E_inf=None):
    """Predict included modes and C* from poles, variances, N, R only."""
    modes = parse_modes(a, v)
    if E_inf is None:
        E_inf = E_inf_YJ(a, v, N)
    if E_inf <= 0:
        raise RuntimeError("non-positive E_inf")
    rows = []
    included = []
    for i, m in enumerate(modes):
        e_m = isolated_Einf(m, N)
        V = (m["sigma2"] - e_m) / E_inf
        take = (R * V) > m["c"]
        rec = dict(
            i=i, kind=m["kind"], c=m["c"], sigma2=m["sigma2"],
            E_inf_m=float(e_m), V=float(V), RV=float(R * V),
            include=bool(take),
            alpha=m["alpha"], omega=m["omega"],
        )
        rows.append(rec)
        if take:
            included.append(i)
    C = int(sum(modes[i]["c"] for i in included))
    n_res = int(sum(1 for i in included if modes[i]["kind"] == "rhythm"))
    n_first = int(sum(1 for i in included if modes[i]["kind"] == "ou"))
    return dict(
        E_inf=float(E_inf),
        C_star=C,
        n_res=n_res,
        n_first=n_first,
        included=included,
        modes=rows,
        var0=var0(v),
    )


# ---------------------------------------------------------------------------
# State-space realizations and Lyapunov MSE
# ---------------------------------------------------------------------------

def world_realization(a, v):
    """Block-diagonal realization; same convention as rhythm_rule.py."""
    a = np.asarray(a)
    v = np.asarray(v)
    used = np.zeros(len(a), dtype=bool)
    blocks_A, blocks_Q, blocks_C = [], [], []
    for i, (ai, vi) in enumerate(zip(a, v)):
        if used[i]:
            continue
        if abs(np.imag(ai)) < 1e-14:
            ai_r, vi_r = float(np.real(ai)), float(np.real(vi))
            blocks_A.append(np.array([[-ai_r]]))
            blocks_Q.append(np.array([[2 * ai_r * vi_r]]))
            blocks_C.append(np.array([1.0]))
            used[i] = True
        else:
            js = [j for j in range(len(a))
                  if (not used[j]) and abs(a[j] - np.conj(ai)) < 1e-12]
            if not js:
                raise RuntimeError(f"unmatched complex pole {ai}")
            j = js[0]
            used[i] = used[j] = True
            alpha, omega = float(np.real(ai)), float(np.imag(ai))
            vi_mean = 0.5 * (vi + np.conj(v[j]))
            vr, vimag = float(np.real(vi_mean)), float(np.imag(vi_mean))
            if abs(vimag) > 1e-14:
                raise RuntimeError("complex v not implemented")
            Px = 2 * vr
            Ablk = np.array([[-alpha, -omega], [omega, -alpha]])
            P = np.array([[Px, 0.0], [0.0, Px]])
            Qblk = -(Ablk @ P + P @ Ablk.T)
            blocks_A.append(Ablk)
            blocks_Q.append(Qblk)
            blocks_C.append(np.array([1.0, 0.0]))
    n = sum(b.shape[0] for b in blocks_A)
    A = np.zeros((n, n))
    Q = np.zeros((n, n))
    C = np.zeros(n)
    i = 0
    for Ab, Qb, Cb in zip(blocks_A, blocks_Q, blocks_C):
        m = Ab.shape[0]
        A[i:i + m, i:i + m] = Ab
        Q[i:i + m, i:i + m] = Qb
        C[i:i + m] = Cb
        i += m
    return A, C, Q


def filter_realization(first_rates, resonants):
    """zdot = Af z + Bf y. first_rates: b>0; resonants: (beta>0, Omega≠0)."""
    first_rates = [float(b) for b in first_rates]
    resonants = [(float(be), float(om)) for be, om in resonants]
    n = len(first_rates) + 2 * len(resonants)
    Af = np.zeros((n, n))
    Bf = np.zeros(n)
    i = 0
    for b in first_rates:
        Af[i, i] = -b
        Bf[i] = b
        i += 1
    for beta, omega in resonants:
        Af[i:i + 2, i:i + 2] = np.array([[-beta, -omega], [omega, -beta]])
        Bf[i] = 1.0
        Bf[i + 1] = 0.0
        i += 2
    return Af, Bf


def guarded_quad(M, r, var_s, rcond=1e-11, dmin_rel=1e-12):
    """var_s - r' M^{+} r with Jacobi scaling and truncated eigen-inverse.

    States with vanishing variance (diag(M) <= dmin_rel * max diag) are dropped
    *before* scaling.  Without that drop, a numerically zero diagonal entry is
    scaled up to O(1), the truncated eigen-inverse keeps it, and the MSE can
    fall below the causal floor (seen when a resonant layer's Ω → 0, leaving an
    uncontrollable state).  See DEVIATIONS_2026-11-20.md.
    """
    M = np.asarray(M, float)
    r = np.asarray(r, float)
    if M.size == 0:
        return float(var_s), np.zeros(0)
    if not (np.all(np.isfinite(M)) and np.all(np.isfinite(r))):
        return np.inf, np.zeros(len(r))
    d_raw = np.sqrt(np.clip(np.diag(M), 0.0, None))
    dmax = float(np.max(d_raw)) if d_raw.size else 0.0
    active = d_raw > dmin_rel * max(dmax, 1e-300)
    if not np.any(active):
        return float(var_s), np.zeros(len(r))
    idx = np.where(active)[0]
    M2 = M[np.ix_(idx, idx)]
    r2 = r[idx]
    d = np.sqrt(np.clip(np.diag(M2), 1e-300, None))
    Ms = M2 / np.outer(d, d)
    rs = r2 / d
    try:
        lam, U = np.linalg.eigh(Ms)
    except np.linalg.LinAlgError:
        return np.inf, np.zeros(len(r))
    keep = lam > rcond * max(lam.max(), 1e-300)
    if not np.any(keep):
        return float(var_s), np.zeros(len(r))
    c = U[:, keep].T @ rs
    gs = U[:, keep] @ (c / lam[keep])
    mse = float(var_s - np.sum(c * c / lam[keep]))
    if not np.isfinite(mse):
        return np.inf, np.zeros(len(r))
    g = np.zeros(len(r))
    g[idx] = gs / d
    return mse, g


def lyapunov_mse(a, v, N, first_rates=(), resonants=()):
    """MSE of the best linear readout of the given filter modules."""
    first_rates = list(first_rates)
    resonants = list(resonants)
    if len(first_rates) + len(resonants) == 0:
        return dict(mse=var0(v), g=[], Pzz_cond=None, var_s=var0(v))
    for b in first_rates:
        if not np.isfinite(b) or b <= 1e-8 or b >= 1e8:
            return dict(mse=np.inf, error="extreme first-order rate", g=None, Pzz_cond=None)
    for beta, om in resonants:
        if (not np.isfinite(beta)) or (not np.isfinite(om)) or beta <= 1e-8 or beta >= 1e8            or abs(om) <= 1e-8 or abs(om) >= 1e8:
            return dict(mse=np.inf, error="extreme resonant params", g=None, Pzz_cond=None)
    Aw, Cw, Qw = world_realization(a, v)
    Af, Bf = filter_realization(first_rates, resonants)
    nw = Aw.shape[0]
    nf = Af.shape[0]
    n = nw + nf
    A = np.zeros((n, n))
    Q = np.zeros((n, n))
    A[:nw, :nw] = Aw
    Q[:nw, :nw] = Qw
    A[nw:, :nw] = np.outer(Bf, Cw)
    A[nw:, nw:] = Af
    Q[nw:, nw:] = N * np.outer(Bf, Bf)
    # Reject non-Hurwitz or extreme designs before the Lyapunov solve
    # (those cases can make the solver extremely slow and were hanging Part A).
    ev = np.linalg.eigvals(A)
    if (not np.all(np.isfinite(ev))) or float(np.max(np.real(ev))) >= -1e-10:
        return dict(mse=np.inf, error="not Hurwitz", g=None, Pzz_cond=None)
    try:
        P = solve_continuous_lyapunov(A, -Q)
    except Exception as e:
        return dict(mse=np.inf, error=str(e), g=None, Pzz_cond=None)
    if not np.all(np.isfinite(P)):
        return dict(mse=np.inf, error="non-finite P", g=None, Pzz_cond=None)
    Pzz = 0.5 * (P[nw:, nw:] + P[nw:, nw:].T)
    r = P[nw:, :nw] @ Cw
    var_s = float(Cw @ P[:nw, :nw] @ Cw)
    mse, g = guarded_quad(Pzz, r, var_s)
    cond = None
    try:
        cond = float(np.linalg.cond(Pzz))
    except Exception:
        pass
    # Ill-conditioned or extreme-gain designs can report a spurious MSE below
    # the causal floor (D3). Good designs in this model have cond ~ 1e0–1e4
    # and O(1) gains; 1e10 / 1e4 are loose numerical cutoffs, not theory.
    if (cond is not None and (not np.isfinite(cond) or cond > 1e10)) or        (g is not None and np.max(np.abs(g)) > 1e4) or        (not np.isfinite(mse)) or mse < 0:
        return dict(mse=np.inf, error="ill-conditioned filter Gramian",
                    g=None, Pzz_cond=cond, var_s=var_s)
    return dict(mse=float(mse), g=g.tolist(), Pzz_cond=cond, var_s=var_s)


def degree_cost(n_first, n_res):
    return int(n_first) + 2 * int(n_res)


def J_of_E(C, E, E_inf, R):
    return C + R * (E / E_inf)


# ---------------------------------------------------------------------------
# Parameter packing, informed starts, optimizer
# ---------------------------------------------------------------------------

def pack_params(first_rates, resonants):
    x = [np.log(max(float(b), 1e-18)) for b in first_rates]
    for beta, omega in resonants:
        x.append(np.log(max(float(beta), 1e-18)))
        x.append(np.log(max(abs(float(omega)), 1e-18)))
    return np.asarray(x, float)


def unpack_params(x, n_first, n_res):
    x = np.asarray(x, float)
    x = np.clip(x, -20, 20)
    first = list(np.exp(x[:n_first]))
    # 2% separation of real rates
    if n_first >= 2:
        logs = np.sort(x[:n_first])
        for i in range(1, n_first):
            logs[i] = max(logs[i], logs[i - 1] + np.log(1.02))
        first = list(np.exp(logs))
    res = []
    y = x[n_first:]
    omegas = []
    betas = []
    for k in range(n_res):
        betas.append(float(np.exp(y[2 * k])))
        omegas.append(float(np.exp(y[2 * k + 1])))
    # 2% floor on distinct |Omega| when n_res >= 2
    if n_res >= 2:
        order = np.argsort(omegas)
        om = np.array(omegas, float)
        logs = np.log(np.clip(om, 1e-18, None))
        # enforce in sorted-omega order
        slog = logs[order].copy()
        for i in range(1, n_res):
            slog[i] = max(slog[i], slog[i - 1] + np.log(1.02))
        om[order] = np.exp(slog)
        omegas = list(om)
    for b, o in zip(betas, omegas):
        res.append((b, o))
    return first, res


def informed_inits(n_first, n_res, modes, rng, n_rand=16):
    """Informed (β, Ω, b) starts from the world's modes, plus random."""
    ou = [m for m in modes if m["kind"] == "ou"]
    rh = [m for m in modes if m["kind"] == "rhythm"]
    ou_rates = [max(m["alpha"], 1e-12) for m in ou]
    rh_beta = [max(m["alpha"], 1e-12) for m in rh]
    rh_om = [max(abs(m["omega"]), 1e-12) for m in rh]
    all_rates = ou_rates + rh_beta + rh_om
    if not all_rates:
        all_rates = [1.0]
    lo = np.log(min(all_rates)) - 5
    hi = np.log(max(all_rates)) + 8
    inits = []

    def add(first, resonants):
        inits.append(pack_params(first, resonants))

    # matched: assign layers to modes of the same kind, cycle if needed
    if n_res:
        for scale_b in (0.5, 1.0, 2.0, 4.0):
            for scale_o in (0.7, 1.0, 1.5):
                res = []
                for k in range(n_res):
                    if rh:
                        m = rh[k % len(rh)]
                        res.append((m["alpha"] * scale_b, abs(m["omega"]) * scale_o))
                    elif ou:
                        m = ou[k % len(ou)]
                        # a wrongly typed resonant on an OU world: heavy damp, rate as freq
                        res.append((m["alpha"] * scale_b, m["alpha"] * scale_o))
                    else:
                        res.append((np.exp(rng.uniform(lo, hi)), np.exp(rng.uniform(lo, hi))))
                first = []
                for k in range(n_first):
                    pool = ou_rates or rh_om or [1.0]
                    first.append(pool[k % len(pool)] * (0.5 + 0.5 * scale_b))
                add(first or ([1.0] if n_first else []), res if n_res else [])
                if n_first == 0 and not first:
                    add([], res)
    else:
        # first-order only: grids around mode moduli
        freqs = np.array(sorted(set(ou_rates + rh_om + rh_beta)))
        for scale in (0.3, 0.7, 1.0, 1.5, 3.0, 8.0):
            pts = [f * scale for f in freqs]
            if n_first > len(pts):
                pts = pts + [pts[i % len(pts)] * (1.2 + 0.1 * (i // max(len(pts), 1)))
                             for i in range(n_first - len(pts))]
            add(pts[:n_first], [])
        if n_first >= 1:
            add(list(np.geomspace(np.exp(lo + 1), np.exp(hi - 1), n_first)), [])

    # a few matched-at-exact-poles starts (the internal-model start)
    if n_res and rh:
        res = []
        for k in range(n_res):
            m = rh[k % len(rh)]
            res.append((m["alpha"], abs(m["omega"])))
        first = [ou_rates[k % len(ou_rates)] for k in range(n_first)] if ou_rates else (
            [rh_om[k % len(rh_om)] for k in range(n_first)] if n_first else [])
        add(first, res)

    for _ in range(n_rand):
        first = list(np.exp(rng.uniform(lo, hi, n_first))) if n_first else []
        res = [(np.exp(rng.uniform(lo, hi)), np.exp(rng.uniform(lo, hi)))
               for _ in range(n_res)]
        add(first, res)

    out, seen = [], set()
    for x in inits:
        if x.size != n_first + 2 * n_res:
            continue
        key = tuple(np.round(x, 5))
        if key not in seen:
            seen.add(key)
            out.append(x)
    return out, lo, hi


def optimize_design(a, v, N, n_first, n_res, seed=0, n_rand=16, use_de=True,
                    de_maxiter=None, extra_inits=None):
    """Reviewer multi-start over (b, β, Ω). Returns best E and parameters."""
    if n_first == 0 and n_res == 0:
        return dict(E=var0(v), first=[], resonants=[], method="closed",
                    n_inits=0, elapsed=0.0, C=0)
    import time
    t0 = time.time()
    rng = np.random.default_rng(seed)
    modes = parse_modes(a, v)
    inits, lo, hi = informed_inits(n_first, n_res, modes, rng, n_rand=n_rand)
    if extra_inits:
        inits = list(inits) + [np.asarray(x, float) for x in extra_inits]
    dim = n_first + 2 * n_res
    bounds = [(lo - 2, hi + 2)] * dim

    def obj(x):
        first, res = unpack_params(x, n_first, n_res)
        out = lyapunov_mse(a, v, N, first, res)
        e = out["mse"]
        return e if np.isfinite(e) and e > 0 else 1e12

    ranked = []
    for x0 in inits:
        try:
            r = minimize(obj, x0, method="Nelder-Mead",
                         options=dict(xatol=1e-8, fatol=1e-14, maxiter=800 * max(dim, 1)))
            fun = obj(r.x)
            ranked.append((fun, r.x, "Nelder-Mead"))
        except Exception:
            pass
    ranked.sort(key=lambda t: t[0])
    polish = [t[1] for t in ranked[:5]] + list(inits[:3])
    for x0 in polish:
        try:
            r = minimize(obj, x0, method="L-BFGS-B", bounds=bounds,
                         options=dict(ftol=1e-14, maxiter=800 * max(dim, 1)))
            fun = obj(r.x)
            ranked.append((fun, r.x, "L-BFGS-B"))
        except Exception:
            pass
    if use_de and dim <= 6:
        try:
            maxiter = de_maxiter if de_maxiter is not None else (12 if dim >= 4 else 20)
            popsize = 6 if dim >= 5 else 8
            r = differential_evolution(
                obj, bounds=bounds, popsize=popsize, mutation=0.5,
                recombination=0.7, seed=int(seed) % (2**31 - 1),
                polish=True, workers=1, atol=1e-12, maxiter=maxiter,
            )
            fun = obj(r.x)
            ranked.append((fun, r.x, "DE"))
        except Exception:
            pass
    if not ranked:
        return dict(E=float("inf"), first=None, resonants=None, method="none",
                    n_inits=len(inits), elapsed=time.time() - t0,
                    C=degree_cost(n_first, n_res))
    ranked.sort(key=lambda t: t[0])
    best = ranked[0]
    first, res = unpack_params(best[1], n_first, n_res)
    # re-evaluate
    e = lyapunov_mse(a, v, N, first, res)["mse"]
    return dict(
        E=float(e),
        first=[float(b) for b in first],
        resonants=[[float(b), float(o)] for b, o in res],
        method=best[2],
        n_inits=len(inits),
        elapsed=time.time() - t0,
        C=degree_cost(n_first, n_res),
        n_first=int(n_first),
        n_res=int(n_res),
    )


def locking_errors(resonants, world_omegas):
    """Min-sum relative |Ω - ω| assignment; returns per-layer errors and median."""
    om_l = np.array([abs(r[1]) for r in resonants], float)
    om_w = np.array([abs(w) for w in world_omegas], float)
    if om_l.size == 0 or om_w.size == 0:
        return dict(median=None, errors=[], assignment=[], unmatched_world=[], unmatched_layer=[])
    n_l, n_w = len(om_l), len(om_w)
    # assignment of min(n_l, n_w) pairs; exhaustive if small
    import itertools
    if n_l <= n_w:
        best = None
        for perm in itertools.permutations(range(n_w), n_l):
            rel = [abs(om_l[i] - om_w[perm[i]]) / max(om_w[perm[i]], 1e-18) for i in range(n_l)]
            s = float(np.sum(rel))
            if best is None or s < best[0]:
                best = (s, list(perm), rel)
        assign = [(i, best[1][i]) for i in range(n_l)]
        errors = best[2]
        unmatched_w = [j for j in range(n_w) if j not in best[1]]
        unmatched_l = []
    else:
        best = None
        for perm in itertools.permutations(range(n_l), n_w):
            rel = [abs(om_l[perm[j]] - om_w[j]) / max(om_w[j], 1e-18) for j in range(n_w)]
            s = float(np.sum(rel))
            if best is None or s < best[0]:
                best = (s, list(perm), rel)
        assign = [(best[1][j], j) for j in range(n_w)]
        errors = best[2]
        unmatched_l = [i for i in range(n_l) if i not in best[1]]
        unmatched_w = []
    return dict(
        median=float(np.median(errors)) if errors else None,
        mean=float(np.mean(errors)) if errors else None,
        errors=[float(e) for e in errors],
        assignment=[(int(i), int(j)) for i, j in assign],
        unmatched_world=[int(j) for j in unmatched_w],
        unmatched_layer=[int(i) for i in unmatched_l],
        layer_omegas=[float(x) for x in om_l],
        world_omegas=[float(x) for x in om_w],
    )


# Compositions scored for a rhythm-only world with n oscillators (prereg §6)
def part_a_compositions(n):
    comps = [(0, 0)]  # (n_res, n_first); C=0 handled separately
    # resonant only
    for nr in range(1, n + 2):  # 1..n+1
        comps.append((nr, 0))
    # mixed
    comps.extend([(1, 1), (1, 2)])
    if n >= 2:
        comps.append((2, 1))
    if n == 3:
        comps.extend([(2, 2), (3, 1)])
    # unique, skip (0,0) duplicate
    out, seen = [], set()
    for c in comps:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


BASE_SEED = 20261120
R_GRID = [0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0]


def composition_key(n_res, n_first):
    return int(n_res) * 100 + int(n_first)


def opt_seed(world_index, n_res, n_first, base=BASE_SEED):
    return int(base + 1000 * world_index + 17 * composition_key(n_res, n_first))
