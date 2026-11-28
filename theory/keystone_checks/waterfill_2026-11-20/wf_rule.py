#!/usr/bin/env python3
"""WF-HSV: discrete water-filling on Kalman-Bucy observer H2 state energies.

Predicts K* from poles, variances, N, R only, plus the unique full-order
Kalman-Bucy ARE and the innovations-to-estimate Gramians.  Does not compute
any reduced-order E_K, does not import stores.E_K or optimize_design, and
does not read s5_rerun.json or rhythm_rule.json.

See /workspace/gtao-wf/MATH.md §7 and PREREG.md §2.
"""
from __future__ import annotations

import numpy as np
from numpy.linalg import eigvalsh, norm
from scipy.linalg import cholesky, solve_continuous_are, solve_continuous_lyapunov, svd


def world_realization(a, v):
    """Block-diagonal realization; same convention as resonant_layers.py."""
    a = np.asarray(a)
    v = np.asarray(v)
    used = np.zeros(len(a), dtype=bool)
    blocks_A, blocks_Q, blocks_C = [], [], []
    for i, (ai, vi) in enumerate(zip(a, v)):
        if used[i]:
            continue
        if abs(np.imag(ai)) < 1e-14:
            ai_r, vi_r = float(np.real(ai)), float(np.real(vi))
            blocks_A.append(np.array([[-ai_r]], float))
            blocks_Q.append(np.array([[2 * ai_r * vi_r]], float))
            blocks_C.append(np.array([1.0], float))
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
            Ablk = np.array([[-alpha, -omega], [omega, -alpha]], float)
            Pblk = np.array([[Px, 0.0], [0.0, Px]], float)
            Qblk = -(Ablk @ Pblk + Pblk @ Ablk.T)
            blocks_A.append(Ablk)
            blocks_Q.append(Qblk)
            blocks_C.append(np.array([1.0, 0.0], float))
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
    var_s = float(np.real(np.sum(v)))
    return A, C, Q, var_s


def _spd_factor(W, ev_floor_rel=1e-14):
    """Return L with L @ L.T ~ W, allowing a positive-semidefinite Gramian."""
    W = 0.5 * (np.asarray(W, float) + np.asarray(W, float).T)
    if not np.all(np.isfinite(W)):
        raise RuntimeError("non-finite Gramian")
    # Try Cholesky on a slightly jittered matrix first.
    jitter = 1e-14 * max(float(np.trace(W)), 1.0)
    try:
        return cholesky(W + jitter * np.eye(W.shape[0]), lower=True)
    except np.linalg.LinAlgError:
        pass
    ev, U = np.linalg.eigh(W)
    floor = ev_floor_rel * max(float(np.max(np.abs(ev))), 1e-300)
    ev = np.clip(ev, 0.0, None)
    keep = ev > floor
    if not np.any(keep):
        raise RuntimeError("Gramian has no positive eigenvalues")
    L = U[:, keep] * np.sqrt(ev[keep])
    return L


def predict(a, v, N, R, rcond=1e-12):
    """Return a dict with K_star or status INDETERMINATE.

    Inputs: poles a, variances v, noise density N, stakes R.
    """
    out = dict(status="OK", K_star=None, reason=None, E_inf_ARE=None,
               var_s=None, delta=[], gamma=[], sigma=[], n=None, R=float(R), N=float(N))
    try:
        A, C, Q, var_s = world_realization(a, v)
    except Exception as e:
        out.update(status="INDETERMINATE", reason=f"realization: {e}")
        return out
    out["n"] = int(A.shape[0])
    out["var_s"] = float(var_s)
    if A.shape[0] == 0:
        out["K_star"] = 0
        return out
    N = float(N)
    if not (np.isfinite(N) and N > 0):
        out.update(status="INDETERMINATE", reason="bad N")
        return out
    C = np.asarray(C, float).reshape(1, -1)
    try:
        # Filter ARE: A P + P A.T - P C.T N^{-1} C P + Q = 0
        # scipy solve_continuous_are(A, B, Q, R) solves
        #   A.T X + X A - X B R^{-1} B.T X + Q = 0
        # so pass A.T and C.T.
        P = solve_continuous_are(A.T, C.T, Q, np.array([[N]], float))
        P = 0.5 * (P + P.T)
    except Exception as e:
        out.update(status="INDETERMINATE", reason=f"ARE: {e}")
        return out
    if not np.all(np.isfinite(P)):
        out.update(status="INDETERMINATE", reason="non-finite P")
        return out
    evP = eigvalsh(P)
    if np.min(evP) < -1e-8 * max(np.max(np.abs(evP)), 1.0):
        out.update(status="INDETERMINATE", reason="P not PSD")
        return out
    E = float(np.asarray(C @ P @ C.T).reshape(-1)[0])
    out["E_inf_ARE"] = E
    if not (np.isfinite(E) and E > 0):
        out.update(status="INDETERMINATE", reason="non-positive E_inf_ARE")
        return out
    Kg = (P @ C.T) / N          # shape (n, 1)
    Af = A - Kg @ C
    # Observer pole (recorded, not used as a placement prediction).
    evF = np.linalg.eigvals(Af)
    out["observer_poles"] = [[float(complex(z).real), float(complex(z).imag)] for z in evF]
    evA = np.linalg.eigvals(A)
    if (not np.all(np.isfinite(evA))) or float(np.max(np.real(evA))) >= -1e-10:
        out.update(status="INDETERMINATE", reason="process A not Hurwitz (Lyapunov)")
        return out
    # Innovations form of the estimate: d xhat = A xhat dt + K d nu,
    # with nu white of intensity N.  This is the map whose H2 is Var(shat)
    # = Var(s)-E.  (The y-to-shat realisation uses A_f, and its white-input
    # H2 is NOT Var(shat); that was the SANITY mismatch.)
    BnBn = N * (Kg @ Kg.T)
    CtC = C.T @ C
    try:
        Pi = solve_continuous_lyapunov(A, -Q)
        Wc = solve_continuous_lyapunov(A, -BnBn)
        Wo = solve_continuous_lyapunov(A.T, -CtC)
    except Exception as e:
        out.update(status="INDETERMINATE", reason=f"Gramian: {e}")
        return out
    Pi = 0.5 * (Pi + Pi.T)
    # Cov(xhat) = Pi - P; its output variance is Var(shat) = Var(s) - E.
    resid_cov = float(np.max(np.abs((Pi - P) - 0.5*(Wc+Wc.T))))
    out["Pi_minus_P_residual"] = resid_cov
    Wc = 0.5 * (Wc + Wc.T)
    Wo = 0.5 * (Wo + Wo.T)
    try:
        Lc = _spd_factor(Wc)
        Lo = _spd_factor(Wo)
        # Lo is n x r or n x n; Lc similar.  SVD of Lo.T @ Lc.
        U, S, Vh = svd(Lo.T @ Lc, full_matrices=False)
    except Exception as e:
        out.update(status="INDETERMINATE", reason=f"balance: {e}")
        return out
    pos = S > rcond * max(float(S[0]) if S.size else 0.0, 1e-300)
    if not np.any(pos):
        out.update(status="INDETERMINATE", reason="no positive HSV")
        return out
    S = S[pos]
    Vh = Vh[pos]
    # T = Lc @ V @ Sigma^{-1/2}
    T = Lc @ Vh.T * (1.0 / np.sqrt(S))
    Cbal = (C @ T).ravel()
    gamma = np.real(Cbal * Cbal * S)
    gamma = np.clip(gamma, 0.0, None)
    sum_g = float(np.sum(gamma))
    target = float(var_s - E)
    # residual of the estimate: Var(s) - E = C Wc C.T, theoretically
    h2_wc = float(np.asarray(C @ Wc @ C.T).reshape(-1)[0])
    tol_abs = 1e-6 * max(abs(var_s), 1.0)
    tol_relE = 1e-4 * E
    if max(abs(sum_g - target), abs(h2_wc - target)) > max(tol_abs, tol_relE):
        # Try reallocating using C Wc C as the target, if it's the H2 identity
        # that holds more tightly than var_s - E (numerical ARE error).
        if abs(sum_g - h2_wc) <= max(tol_abs, tol_relE) and abs(h2_wc - target) <= 10 * max(tol_abs, tol_relE):
            target = h2_wc
            out["consistency_note"] = "used C Wc C.T as H2 target (ARE/YJ gap)"
        else:
            out.update(status="INDETERMINATE",
                       reason=(f"H2 split mismatch: sum_gamma={sum_g}, "
                               f"var-E={target}, CWcC={h2_wc}"))
            out["gamma"] = gamma.tolist()
            out["sigma"] = S.tolist()
            return out
    delta = gamma / E
    out["gamma"] = [float(x) for x in gamma]
    out["sigma"] = [float(x) for x in S]
    out["delta"] = [float(x) for x in delta]
    out["sum_gamma"] = sum_g
    out["target_h2"] = target
    R = float(R)
    if not np.isfinite(R):
        out.update(status="INDETERMINATE", reason="bad R")
        return out
    out["K_star"] = int(np.sum(R * delta > 1.0))
    return out


def n60_from0_one_ou(a, v, N, R):
    """Closed-form N60-from-0 / L1 for a single OU mode."""
    a, v, N, R = map(float, (a, v, N, R))
    P = N * (np.sqrt(a * a + 2 * a * v / N) - a)
    return (1 if R * (v - P) / P > 1.0 else 0), P
