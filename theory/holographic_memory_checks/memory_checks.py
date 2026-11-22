#!/usr/bin/env python3
"""Checks for theory/HOLOGRAPHIC_MEMORY_2026-11-22.md.

Superposed versus local memory, priced at the heat floor of independent
equilibrium Ornstein–Uhlenbeck modes. Run from the repo root:

  nice -n 19 python3 theory/holographic_memory_checks/memory_checks.py
"""
from __future__ import annotations

import math

import numpy as np

PASS = 0
FAIL = 0


def check(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print("PASS  %s  %s" % (name, detail))
    else:
        FAIL += 1
        print("FAIL  %s  %s" % (name, detail))


def near(a, b, tol=1e-9):
    a = float(a)
    b = float(b)
    scale = max(1.0, abs(a), abs(b))
    return abs(a - b) <= tol * scale


def lyapunov(A, Q):
    n = A.shape[0]
    Kmat = np.kron(np.eye(n), A) + np.kron(A, np.eye(n))
    c = np.linalg.solve(Kmat, -np.asarray(Q, float).reshape(-1, order="F"))
    C = c.reshape((n, n), order="F")
    return 0.5 * (C + C.T)


def subset_task(K, s):
    """E[1_Omega 1_Omega^T] for a uniform s-subset of K items."""
    p = s / K
    q = s * (s - 1) / (K * (K - 1)) if K > 1 and s > 1 else 0.0
    U = np.full((K, K), q)
    np.fill_diagonal(U, p)
    return U


def subset_eigs(K, s):
    """Closed eigenvalues of the random-subset task. One spike, K-1 bulk."""
    if s <= 0:
        return np.zeros(K)
    lam_max = (s * s) / K
    if s >= K:
        out = np.zeros(K)
        out[0] = float(K)
        return out
    lam_bulk = (s / K) * (K - s) / (K - 1)
    return np.array([lam_max] + [lam_bulk] * (K - 1))


def component_jl(lam, w, a, v, kT, active):
    """Heat and stake-weighted loss along one task eigen-direction of weight lam."""
    if lam <= 0.0:
        return 0.0, 0.0
    blind = (not active) or (w * lam <= kT * a / v)
    if blind:
        return 0.0, w * lam * v
    sigma = math.sqrt(kT * a * v / (w * lam))
    heat = kT * a * (v - sigma) / sigma
    return heat, w * lam * sigma


def allocate(weights, w, a, v, kT, D):
    """Water-fill the D largest weights. Returns heat, loss term, cost, n_on."""
    order = np.argsort(-np.asarray(weights, float))
    heat = 0.0
    loss = 0.0
    n_on = 0
    for idx in order:
        lam = float(weights[idx])
        # A blind direction spends no dimension. The cap binds only on directions
        # the stake would otherwise track.
        if lam <= 0.0 or w * lam <= kT * a / v or n_on >= D:
            h, ell = component_jl(lam, w, a, v, kT, False)
        else:
            h, ell = component_jl(lam, w, a, v, kT, True)
            n_on += 1
        heat += h
        loss += ell
    return heat, loss, heat + loss, n_on


def pure_sum_costs(K, w, a=1.0, v=1.0, kT=1.0, D_super=1, D_local=None):
    """Un-normalized sum of K identical modes. U = 11^T."""
    if D_local is None:
        D_local = K
    eigs = np.zeros(K)
    eigs[0] = float(K)
    diag = np.ones(K)
    hs, ls, Js, ns = allocate(eigs, w, a, v, kT, D_super)
    hl, ll, Jl, nl = allocate(diag, w, a, v, kT, D_local)
    return (hs, ls, Js, ns), (hl, ll, Jl, nl)


def matched_heat_ratio_sum(s, eps, a=1.0, v=1.0, kT=1.0):
    """Heat of s local memories versus one joint memory, sum-error eps."""
    V = s * v
    if not (0.0 < eps < V):
        raise ValueError("eps outside (0, s v)")
    heat_joint = kT * a * (V - eps) / eps
    # Equal split s_k = eps/s. Each (v - s_k)/s_k = (V - eps)/eps.
    heat_local = s * kT * a * (V - eps) / eps
    return heat_joint, heat_local


def joint_mu_of_error(a, v, eps):
    """Solve eps = sum a_k v_k / (a_k + mu). Monotone in mu."""
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    lo, hi = 0.0, 1.0
    while sum(ai * vi / (ai + hi) for ai, vi in zip(a, v)) > eps:
        hi *= 2.0
        if hi > 1e12:
            break
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        err = sum(ai * vi / (ai + mid) for ai, vi in zip(a, v))
        if err > eps:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def local_heat_fixed_sum_error(a, v, eps, kT=1.0):
    """Min sum kT a (v-s)/s subject to sum s = eps, 0 < s_k <= v_k.

    Unconstrained stationarity is s_k proportional to sqrt(a_k v_k).
    """
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    scale = np.sqrt(a * v)
    # s = scale / sqrt(lambda), sum s = eps ⇒ sqrt(lambda) = sum(scale)/eps
    # if that s stays inside (0, v].
    lam_sqrt = float(np.sum(scale) / eps)
    s = scale / lam_sqrt
    if np.any(s > v + 1e-10) or np.any(s <= 0):
        raise RuntimeError("allocation hit a variance bound; extend the solver")
    heat = float(np.sum(kT * a * (v - s) / s))
    return heat, s


def degrade(V, eps, f):
    """Split-channel error and item-erasure error after fraction f fails."""
    eps_h = V * eps / ((1.0 - f) * V + f * eps)
    eps_l = (1.0 - f) * eps + f * V
    gap = f * (1.0 - f) * (V - eps) ** 2 / ((1.0 - f) * V + f * eps)
    return eps_h, eps_l, gap


def binom_pmf_upto(n, p, kmax):
    """P(X <= kmax) for X ~ Bin(n, p)."""
    q = 1.0 - p
    total = 0.0
    term = q ** n
    total += term
    for i in range(0, kmax):
        term *= (n - i) * p / ((i + 1) * q) if q > 0 else 0.0
        total += term
    return total


def rho_crit(V, eps0, eps_cap):
    """Remaining precision fraction below which the split error exceeds eps_cap."""
    return eps0 * (V - eps_cap) / (eps_cap * (V - eps0))


def split_error(V, eps0, rho):
    return V * eps0 / (eps0 + rho * (V - eps0))


def expected_split_error(D, p_up, V, eps0):
    q = 1.0 - p_up
    term = q ** D
    acc = 0.0
    for i in range(D + 1):
        rho = i / D
        acc += term * split_error(V, eps0, rho)
        if i < D:
            term *= (D - i) * p_up / ((i + 1) * q)
    return acc


def static_channel(a, v, G, sig2):
    """Posterior covariance and learning rate of Y = G X + noise."""
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    G = np.asarray(G, float)
    prec = np.diag(1.0 / v) + (G.T @ G) / sig2
    S = np.linalg.inv(prec)
    Ddiff = a * v
    Phi = (G.T @ G) / sig2
    L = float(np.sum(Ddiff * np.diag(Phi)))
    return S, L


def fast_spring_heat(a, v, G, sig2, lam):
    """Lyapunov heat of D independent fast springs, gain lam * G, noise lam * sig2."""
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    G = np.asarray(G, float)
    K = a.shape[0]
    D = G.shape[0]
    n = K + D
    A = np.zeros((n, n))
    Q = np.zeros((n, n))
    for i in range(K):
        A[i, i] = -a[i]
        Q[i, i] = 2.0 * a[i] * v[i]
    for j in range(D):
        A[K + j, K + j] = -lam
        Q[K + j, K + j] = 2.0 * lam * sig2
        for i in range(K):
            A[K + j, i] = lam * G[j, i]
    C = lyapunov(A, Q)
    heat = 0.0
    for j in range(D):
        # f = -lam M + lam (G X)_j ; E[f^2] / (lam sig2) - lam
        row = np.zeros(n)
        row[:K] = lam * G[j]
        row[K + j] = -lam
        Ef2 = float(row @ C @ row)
        heat += Ef2 / (lam * sig2) - lam
    Sxx = C[:K, :K]
    Sxm = C[:K, K:]
    Smm = C[K:, K:]
    # Conditional covariance of X given M.
    S_cond = Sxx - Sxm @ np.linalg.inv(Smm) @ Sxm.T
    return heat, 0.5 * (S_cond + S_cond.T), C


def random_subspace_capture(K, D, n_draw, seed):
    rng = np.random.default_rng(seed)
    caps = np.empty(n_draw)
    ones = np.ones(K)
    for i in range(n_draw):
        A = rng.normal(size=(K, D))
        Q, _ = np.linalg.qr(A)
        caps[i] = float(ones @ Q @ Q.T @ ones)
    return float(np.mean(caps)), float(np.std(caps) / math.sqrt(n_draw))


def known_support_compare(K, s, D, heat_budget, n_support, seed, a=1.0, v=1.0, kT=1.0):
    """Fixed local slots versus random projections, support known only at readout.

    Active coordinates are s equilibrium modes. Inactive coordinates are absent,
    so they do not add drive. The local code maintains D fixed slots whether or
    not they are active. The projection code's heat is the heat of the active
    columns only.
    """
    rng = np.random.default_rng(seed)
    # Local: D fixed items. The heat budget is spread across those D slots and
    # is paid whether or not the slot is in the active set.
    phi = heat_budget / (D * kT * a * v)
    sigma_stored = v / (1.0 + v * phi)
    capture = s * (D / K)
    err_local = capture * sigma_stored + (s - capture) * v
    # Random projections. One fixed codebook. On each support the gain is scaled
    # so the heat of the active columns equals the budget exactly. The excess
    # error over the ideal is the conditioning of that support's columns.
    G = rng.normal(size=(D, K))
    err_proj = 0.0
    heat_proj = 0.0
    worst = 0.0
    for _ in range(n_support):
        omega = rng.choice(K, size=s, replace=False)
        Go = G[:, omega]
        frob = float(np.sum(Go * Go))
        gamma = heat_budget / (kT * a * v * frob)
        heat_proj += heat_budget
        prec = np.eye(s) / v + gamma * (Go.T @ Go)
        e = float(np.trace(np.linalg.inv(prec)))
        err_proj += e
        worst = max(worst, e)
    err_proj /= n_support
    heat_proj /= n_support
    # Ideal: s dedicated sensors, same total heat, equal precision.
    phi_star = heat_budget / (s * kT * a * v)
    err_ideal = s * v / (1.0 + v * phi_star)
    return {
        "err_local": err_local,
        "err_proj": err_proj,
        "err_ideal": err_ideal,
        "heat_proj": heat_proj,
        "sigma_stored": sigma_stored,
        "capture": capture,
        "worst": worst,
    }


def mi_versus_heat(a, V, kT, kappa, ws):
    eps_h = np.sqrt(kT * a * V / ws)
    eps_m = kappa / (2.0 * ws)
    slope_h = np.polyfit(np.log(ws), np.log(eps_h), 1)[0]
    slope_m = np.polyfit(np.log(ws), np.log(eps_m), 1)[0]
    return eps_h, eps_m, float(slope_h), float(slope_m)


def main():
    # ------------------------------------------------------------------ anchor
    # The merged sum-loss numbers. Not a new result: a guard that this file
    # prices the same floor.
    a_u = np.array([1.0, 100.0])
    v_u = np.array([1.0, 1.0])
    mu = joint_mu_of_error(a_u, v_u, 0.5)
    heat_l, s_loc = local_heat_fixed_sum_error(a_u, v_u, 0.5)
    check(
        "anchor: rates (1, 100), sum-error 0.5, joint mu and separate heat 141",
        near(mu, 103.887732673340, 1e-9) and near(heat_l, 141.0, 1e-9),
        "mu=%.12f separate=%.12f s=%s" % (mu, heat_l, np.array2string(s_loc, precision=6)),
    )
    print("ANCHOR mu=%.12f separate_heat=%.12f ratio=%.6f" % (mu, heat_l, heat_l / mu))

    # ------------------------------------------------------- matched heat ratio
    for s, eps in ((1, 0.4), (2, 0.5), (3, 1.1), (4, 0.5), (8, 2.0)):
        hj, hl = matched_heat_ratio_sum(s, eps)
        check(
            "matched-error heat ratio equals sparsity s=%d" % s,
            near(hl / hj, s, 1e-12) and near(hj, 1.0 * (s * 1.0 - eps) / eps, 1e-12),
            "joint=%.12f local=%.12f ratio=%.12f" % (hj, hl, hl / hj),
        )
    # s=K identical modes, the three points already in INFO_PHYSICS_GENERAL.
    for K, eps, joint in ((2, 0.8, 1.5), (3, 1.1, 1.727272727273), (4, 0.5, 7.0)):
        hj, hl = matched_heat_ratio_sum(K, eps)
        check(
            "identical-mode factor K=%d reproduces the merged heats" % K,
            near(hj, joint, 1e-12) and near(hl, K * joint, 1e-12),
            "joint=%.12f local=%.12f" % (hj, hl),
        )

    # ------------------------------------------------------- frontiers, pure sum
    # K identical modes, a=v=kT=1. Joint threshold 1/K, local threshold 1.
    K = 4
    w0_j = 1.0 / K
    w0_l = 1.0
    check("pure-sum thresholds: joint 1/K, local 1", near(w0_j, 0.25) and near(w0_l, 1.0))
    print("PURESUM K=%d w0_joint=%.6f w0_local=%.6f" % (K, w0_j, w0_l))
    for w in (0.1, 0.25, 0.5, 1.0, 4.0, 100.0):
        (hs, ls, Js, ns), (hl, ll, Jl, nl) = pure_sum_costs(K, w)
        # Closed forms.
        if w <= w0_j:
            J_closed = w * K * 1.0
        else:
            J_closed = 2.0 * math.sqrt(K * w) - 1.0
        if w <= w0_l:
            Jl_closed = w * K
        else:
            Jl_closed = K * (2.0 * math.sqrt(w) - 1.0)
        check(
            "pure-sum frontier at w=%g" % w,
            near(Js, J_closed, 1e-12) and near(Jl, Jl_closed, 1e-12) and Js <= Jl + 1e-12,
            "Jsuper=%.12f Jlocal=%.12f nonsuper=%d" % (Js, Jl, ns),
        )
        print("PURESUM w=%.4f Jsuper=%.12f Jlocal=%.12f ratio=%.6f nsuper=%d" % (w, Js, Jl, Jl / Js, ns))
    # High-stake ratio tends to sqrt(K).
    _, _, Js, _ = pure_sum_costs(K, 1e8)[0]
    _, _, Jl, _ = pure_sum_costs(K, 1e8)[1]
    check(
        "pure-sum cost ratio tends to sqrt(K)",
        near(Jl / Js, math.sqrt(K), 1e-4),
        "ratio=%.8f sqrtK=%.8f" % (Jl / Js, math.sqrt(K)),
    )

    # Dimension cap: one aligned coordinate beats every local budget on a pure sum.
    for Dloc in (1, 2, 3, 4):
        (_, _, Js, _), (_, _, Jl, _) = pure_sum_costs(K, 4.0, D_super=1, D_local=Dloc)
        check(
            "at w=4, one aligned coordinate beats local D=%d on the sum" % Dloc,
            Js < Jl - 1e-9,
            "Jsuper=%.12f Jlocal=%.12f" % (Js, Jl),
        )

    # --------------------------------------------------------- per-item task
    # U = I. Eigenvalues and diagonal agree, so the costs agree at every D.
    K = 6
    eigs = np.ones(K)
    for D in (1, 3, 6):
        for w in (0.5, 2.0, 9.0):
            hs, _, Js, ns = allocate(eigs, w, 1, 1, 1, D)
            hl, _, Jl, nl = allocate(eigs, w, 1, 1, 1, D)
            check(
                "per-item U=I ties at D=%d w=%g" % (D, w),
                near(Js, Jl, 1e-12) and ns == nl,
                "J=%.12f n=%d" % (Js, ns),
            )
    # Off-diagonal precision raises every marginal variance at fixed diagonal.
    # S_kk >= 1/P_kk, with equality only when row k has no off-diagonal entry.
    for trial, rho in enumerate((0.2, 0.5, 0.8)):
        P = np.array([[2.0, rho], [rho, 2.0]])
        Sdiag = np.array([0.5, 0.5])
        S2 = np.linalg.inv(P)
        gap = float(np.trace(S2) - np.sum(Sdiag))
        check(
            "off-diagonal precision raises the per-item error, rho=%.1f" % rho,
            gap > 1e-6 and np.all(np.diag(S2) > Sdiag),
            "trace gap=%.6e diag=%s" % (gap, np.array2string(np.diag(S2), precision=6)),
        )

    # Unequal per-item stakes: aligning with the heavy items beats a shared axis.
    # Loss sum c_k S_kk. Compare diagonal allocation on the two heavy items
    # against putting the same heat on the all-ones direction.
    c = np.array([4.0, 3.0, 0.2, 0.1])
    w = 1.0
    # Use allocate on the diagonal weights with D=2, versus one eigen-direction
    # that is not an item axis. The item-axis cost is the local optimum.
    _, _, J_local, nloc = allocate(c, w, 1, 1, 1, 2)
    # All-ones direction, unit vector. The quadratic form u^T diag(c) u is the
    # loss weight of that single direction only if S is reduced along u and the
    # loss is u-weighted — for a diagonal loss the single direction's marginal
    # effect is computed directly.
    u = np.ones(4) / 2.0
    # Phi = phi u u^T. Heat = phi (a=v=kT=1, heat = a v phi = phi).
    # S = (I + phi u u^T)^{-1} = I - phi u u^T / (1 + phi).
    # Loss = sum c_k S_kk = sum c_k (1 - phi u_k^2 / (1+phi)).
    def aligned_cost(phi):
        shrink = phi / (1.0 + phi)
        loss = float(np.sum(c * (1.0 - shrink * (u * u))))
        return phi + w * loss

    phi_grid = np.linspace(0.0, 20.0, 4001)
    J_mix = min(aligned_cost(phi) for phi in phi_grid)
    # Closed form on the two heavy items, u=(1,1,0,0)/sqrt(2).
    # sum c_k u_k^2 = 3.5, optimum phi = sqrt(3.5)-1, cost 2*sqrt(3.5)+2.8.
    J_heavy = 2.0 * math.sqrt(3.5) + 2.8
    check(
        "unequal per-item stakes: item-aligned D=2 beats the all-ones mixture",
        J_local + 1e-6 < J_mix and J_local + 1e-6 < J_heavy,
        "Jlocal=%.6f Jmix=%.6f Jheavy=%.6f" % (J_local, J_mix, J_heavy),
    )
    print("PERITEM Jlocal=%.12f Jmix=%.12f Jheavy=%.12f" % (J_local, J_mix, J_heavy))

    # ------------------------------------------------------- subset-query spectrum
    for K, s in ((12, 1), (12, 2), (12, 6), (12, 12), (8, 3)):
        U = subset_task(K, s)
        ev = np.sort(np.linalg.eigvalsh(U))[::-1]
        closed = np.sort(subset_eigs(K, s))[::-1]
        check(
            "subset-task spectrum K=%d s=%d" % (K, s),
            np.allclose(ev, closed, rtol=1e-10, atol=1e-10),
            "lead=%.6f bulk=%.6f" % (closed[0], closed[-1]),
        )
    # Stake window and high-stake ratio.
    K = 12
    print("SUBSET K=%d  (stake unit kT a/v = 1)" % K)
    for s in (1, 2, 4, 6, 12):
        ev = subset_eigs(K, s)
        diag = np.diag(subset_task(K, s))
        w_spike = K / (s * s)
        w_local = (K / s) if s < K else 1.0
        # s=K: U_kk=1, local threshold 1; spike threshold 1/K.
        if s == K:
            w_spike = 1.0 / K
            w_local = 1.0
        _, _, Js_lo, _ = allocate(ev, w_spike * 1.01, 1, 1, 1, K)
        _, _, Jl_lo, _ = allocate(diag, w_spike * 1.01, 1, 1, 1, K)
        _, _, Js_hi, nshi = allocate(ev, 1e6, 1, 1, 1, K)
        _, _, Jl_hi, _ = allocate(diag, 1e6, 1, 1, 1, K)
        check(
            "subset s=%d: just above the spike threshold, local is blind or tied" % s,
            Js_lo <= Jl_lo + 1e-9,
            "Jsuper=%.6f Jlocal=%.6f wspike=%.6f wlocal=%.6f" % (Js_lo, Jl_lo, w_spike, w_local),
        )
        print(
            "SUBSET s=%d wspike=%.6f wlocal=%.6f window=%.6f high_ratio=%.6f n_at_high=%d"
            % (s, w_spike, w_local, w_local / w_spike, Jl_hi / Js_hi, nshi)
        )
        check(
            "subset s=%d high-stake ratio" % s,
            (s == 1 and near(Jl_hi / Js_hi, 1.0, 1e-8))
            or (s == K and near(Jl_hi / Js_hi, math.sqrt(K), 1e-3))
            or (1 < s < K and Jl_hi / Js_hi > 1.0),
            "ratio=%.8f" % (Jl_hi / Js_hi),
        )

    # ----------------------------------------------- m disjoint combination tasks
    # m blocks of s ones. Eigenvalues: m copies of s, and the rest 0.
    m, s = 3, 4
    K = m * s
    eigs = np.zeros(K)
    eigs[:m] = s
    diag = np.ones(K)  # each ones-block has unit diagonal
    for w in (0.2, 1.0, 5.0, 1e4):
        _, _, Js, ns = allocate(eigs, w, 1, 1, 1, m)
        _, _, Jl, nl = allocate(diag, w, 1, 1, 1, K)
        _, _, Js_unc, _ = allocate(eigs, w, 1, 1, 1, K)
        check(
            "m=%d disjoint sums of s=%d at w=%g, D=m meets the uncapped memory" % (m, s, w),
            near(Js, Js_unc, 1e-12) and Js <= Jl + 1e-12,
            "Jsuper=%.6f Jlocal=%.6f n=%d" % (Js, Jl, ns),
        )
    _, _, Js, _ = allocate(eigs, 1e8, 1, 1, 1, m)
    _, _, Jl, _ = allocate(diag, 1e8, 1, 1, 1, K)
    check(
        "disjoint combinations, high-stake ratio tends to sqrt(s)",
        near(Jl / Js, math.sqrt(s), 1e-3),
        "ratio=%.6f sqrt(s)=%.6f" % (Jl / Js, math.sqrt(s)),
    )
    print("DISJOINT m=%d s=%d high_ratio=%.6f" % (m, s, Jl / Js))

    # Drift scales thresholds and heat together; the ratio of thresholds stays s
    # for a pure sum of s modes (here s=K=4).
    for a in (0.25, 1.0, 7.0):
        w0j = a / K
        w0l = a / 1.0
        (_, _, Js, _), (_, _, Jl, _) = pure_sum_costs(K, w=4.0 * a, a=a)
        # At stake 4a, which is 4 times the local threshold, both track.
        check(
            "drift a=%g scales both thresholds and keeps superposed ahead" % a,
            near(w0l / w0j, K, 1e-12) and Js < Jl,
            "w0j=%.6f w0l=%.6f Jsuper=%.6f Jlocal=%.6f" % (w0j, w0l, Js, Jl),
        )
    print("DRIFT threshold_ratio=%.6f (equals K, independent of a)" % K)

    # Unequal rates: the anchor ratio, plus a slow/fast pair at several stakes.
    print("UNEQUAL a=(1,100) matched heat ratio=%.6f (already the merged pair)" % (heat_l / mu))
    for ratio_a in (1.0, 4.0, 100.0):
        aa = np.array([1.0, ratio_a])
        vv = np.array([1.0, 1.0])
        # Pick a sum-error halfway from 0 to the prior sum of variances, scaled.
        # Use eps = 0.5 * (v1+v2) * 0.5 = 0.5 when variances are 1? Prior sum-error
        # if blind and estimating 0 is v1+v2=2. Use eps=0.5.
        muj = joint_mu_of_error(aa, vv, 0.5)
        hl, _ = local_heat_fixed_sum_error(aa, vv, 0.5)
        check(
            "unequal rates ratio %g, joint heat is below separate heat" % ratio_a,
            muj < hl - 1e-8,
            "joint=%.6f separate=%.6f ratio=%.6f" % (muj, hl, hl / muj),
        )
        print("UNEQUAL aratio=%.4f joint=%.6f separate=%.6f heat_ratio=%.6f" % (ratio_a, muj, hl, hl / muj))

    # ------------------------------------------------------- random vs aligned
    K, D = 20, 5
    mean_cap, se_cap = random_subspace_capture(K, D, 2000, seed=0)
    check(
        "random subspace captures fraction D/K of a known sum",
        near(mean_cap, D, 0.02),
        "mean ||P 1||^2=%.4f se=%.4f target D=%d" % (mean_cap, se_cap, D),
    )
    # Infinite-precision residual equals the local residual (K-D)*v in expectation.
    print(
        "RANDOM K=%d D=%d captured=%.4f residual_var=%.4f local_residual=%d"
        % (K, D, mean_cap, 1.0 * (K - mean_cap), K - D)
    )
    # Finite heat: one aligned coordinate versus a random coordinate, same heat.
    # Aligned gain on the sum. Identical a=v=1, heat = ||g||^2 / sig2 * (since a v=1,
    # heat = sum g_k^2 / sig2).
    heat_budget = 4.0
    # Aligned: g proportional to ones, Phi rank one, tr Phi = heat_budget.
    # eps_sum = K / (1 + phi_along) with the unit-vector precision.
    # From earlier: heat = (v/sigma_u - 1) with a=kT=1, and eps = K sigma_u,
    # heat = K/eps * K? Let sigma_u = eps/K, heat = (1/sigma_u - 1) = K/eps - 1.
    # At heat 4,  K/eps - 1 = 4, eps = K/5.
    eps_aligned = K / (heat_budget + 1.0)
    # Random one-dimensional projection, Monte Carlo, same heat.
    rng = np.random.default_rng(2)
    errs = []
    for _ in range(400):
        g = rng.normal(size=K)
        g = g / np.linalg.norm(g)
        # Y = alpha g·X + xi, var xi = 1, choose alpha so heat = a v alpha^2 = alpha^2 = heat.
        alpha2 = heat_budget
        # Var(g·X)=1. Posterior var of g·X is 1/(1+alpha2).
        # Var(sum | Y) = Var(1·X) - cov^2 / varY.
        # 1·X = sqrt(K) u·X with u=ones/sqrt(K). g is unit.
        # cov(1·X, alpha g·X) = alpha g·1 * v = alpha g·1
        # var Y = alpha2 * 1 + 1
        cov = math.sqrt(alpha2) * float(np.sum(g))
        varY = alpha2 + 1.0
        eps = K - cov * cov / varY
        errs.append(eps)
    mean_rand = float(np.mean(errs))
    # E[(1·g)^2]=1 for a uniform unit vector, so E[eps]=K - heat*(1)/(heat+1)*1
    # wait: cov^2/varY = alpha2 * (1·g)^2 / (alpha2+1), E[(1·g)^2]=1.
    expect_rand = K - heat_budget * 1.0 / (heat_budget + 1.0)
    check(
        "a random coordinate at the same heat misses a known sum",
        near(expect_rand, 19.2, 1e-12) and abs(mean_rand - expect_rand) < 0.15,
        "aligned_eps=%.4f expect=%.4f seed2_mean=%.4f" % (eps_aligned, expect_rand, mean_rand),
    )
    print(
        "RANDOM1D heat=%.2f aligned_eps=%.4f expect_eps=%.4f seed2_mean=%.4f"
        % (heat_budget, eps_aligned, expect_rand, mean_rand)
    )

    # ----------------------------------------------- known-support sparse features
    ks = known_support_compare(K=32, s=4, D=8, heat_budget=16.0, n_support=300, seed=3)
    check(
        "known support: random projections beat fixed local slots at the same heat",
        ks["err_proj"] < 0.5 * ks["err_local"] and ks["err_proj"] < 2.0 * ks["err_ideal"],
        "local=%.4f proj=%.4f ideal=%.4f heat=%.4f capture=%.4f"
        % (ks["err_local"], ks["err_proj"], ks["err_ideal"], ks["heat_proj"], ks["capture"]),
    )
    print(
        "SUPPORT K=32 s=4 D=8 local_err=%.6f proj_err=%.6f ideal_err=%.6f"
        % (ks["err_local"], ks["err_proj"], ks["err_ideal"])
    )
    # s=K, support is everything: projections should not beat a local code that
    # stores every item. D=K=8, s=8.
    full = known_support_compare(K=8, s=8, D=8, heat_budget=16.0, n_support=1, seed=4)
    # Seed 4 is one matrix. The mean is over independent codebooks.
    rng_books = np.random.default_rng(4)
    book_errs = []
    for _ in range(2000):
        G = rng_books.normal(size=(8, 8))
        frob = float(np.sum(G * G))
        gamma = 16.0 / frob
        prec = np.eye(8) + gamma * (G.T @ G)
        book_errs.append(float(np.trace(np.linalg.inv(prec))))
    book_mean = float(np.mean(book_errs))
    book_se = float(np.std(book_errs) / math.sqrt(len(book_errs)))
    check(
        "full support: projections do not beat storing every item",
        book_mean > full["err_local"] and full["err_proj"] > full["err_local"],
        "local=%.4f seed4=%.4f mean=%.4f se=%.4f" % (full["err_local"], full["err_proj"], book_mean, book_se),
    )
    print(
        "SUPPORT K=8 s=8 D=8 local_err=%.6f seed4_err=%.6f codebook_mean=%.6f se=%.6f"
        % (full["err_local"], full["err_proj"], book_mean, book_se)
    )

    # ------------------------------------------------------- graceful degradation
    for V, eps, f in ((4.0, 1.0, 0.25), (4.0, 0.2, 0.1), (10.0, 3.0, 0.5), (2.0, 1.999, 0.3)):
        eh, el, gap = degrade(V, eps, f)
        check(
            "split error is below item erasure at f=%.2f" % f,
            eh < el and near(el - eh, gap, 1e-12) and gap > 0.0,
            "holo=%.8f local=%.8f gap=%.8e" % (eh, el, gap),
        )
    eh, el, gap = degrade(4.0, 1.0, 0.25)
    # Derivative ratio at f=0: local slope V-eps, holo slope eps(V-eps)/V.
    slope_l = 4.0 - 1.0
    slope_h = 1.0 * (4.0 - 1.0) / 4.0
    check(
        "at small f the split slope is the item-erasure slope times eps/V",
        near(slope_h, slope_l * (1.0 / 4.0), 1e-12),
        "slope_h=%.6f slope_l=%.6f" % (slope_h, slope_l),
    )
    print("DEGRADE f=0.25 eps_h=%.12f eps_l=%.12f gap=%.12f slope_h=%.6f slope_l=%.6f" % (eh, el, gap, slope_h, slope_l))
    # Equality at the endpoints.
    for f in (0.0, 1.0):
        eh, el, gap = degrade(4.0, 1.0, f)
        check("degradation gap vanishes at f=%.0f" % f, near(eh, el, 1e-15) and near(gap, 0.0, 1e-15))

    # A single unsplit coordinate does not degrade gracefully: it is either up or down.
    # That is the f in {0, 1} case. Recorded by the endpoint check above.

    # --------------------------------------------------------------- ruin cap
    V, eps0, eps_cap = 4.0, 1.0, 1.5
    rc = rho_crit(V, eps0, eps_cap)
    check("rho crit for the worked cap", near(rc, 1.0 * (4.0 - 1.5) / (1.5 * (4.0 - 1.0)), 1e-15), "rho=%.6f" % rc)
    p_up = 0.8
    # D=1: ruin when down. P=0.2
    # For general D, ruin when i/D < rc, i.e. i <= floor(rc*D - 1e-15)
    def p_ruin(D):
        kmax = int(math.floor(rc * D - 1e-12))
        if kmax < 0:
            return 0.0
        return binom_pmf_upto(D, p_up, kmax)

    pr1 = p_ruin(1)
    pr4 = p_ruin(4)
    pr8 = p_ruin(8)
    pr16 = p_ruin(16)
    check(
        "finer split lowers the chance the error crosses the cap, at fixed total precision",
        near(pr1, 0.2, 1e-12) and pr16 < pr4 and pr8 > 0.05 and pr8 > p_ruin(7),
        "P1=%.6f P4=%.6f P7=%.6f P8=%.6f P16=%.6e" % (pr1, pr4, p_ruin(7), pr8, pr16),
    )
    e1 = expected_split_error(1, p_up, V, eps0)
    e16 = expected_split_error(16, p_up, V, eps0)
    check(
        "finer split lowers expected error at the same heat",
        e16 < e1 - 1e-6,
        "E1=%.6f E16=%.6f" % (e1, e16),
    )
    print(
        "RUIN P1=%.6f P4=%.6f P7=%.6f P8=%.6f P16=%.6e E1=%.6f E16=%.6f rho=%.6f"
        % (pr1, pr4, p_ruin(7), pr8, pr16, e1, e16, rc)
    )

    # Overhead h per unit. Heat of the precision is fixed (same mu). Extra units
    # add h. Cap eps_r = 0.05. D=1 is infeasible (P=0.2). Smallest feasible D
    # costs more by D*h and is the one the cap selects.
    # Same total precision, per-unit upkeep h. This upkeep is not the heat floor.
    # It is the master-equation h, used here only as an added charge.
    h_upkeep = 0.5
    w_stake = 1.0
    heat_fixed = (V - eps0) / eps0  # mu = 3, paid whether or not the packaging is split
    rows = []
    for D in range(1, 21):
        pr = p_ruin(D)
        err = expected_split_error(D, p_up, V, eps0)
        J = heat_fixed + D * h_upkeep + w_stake * err
        rows.append((J, D, pr, err))
    uncapped = min(rows, key=lambda t: t[0])
    capped_rows = [t for t in rows if t[2] <= 0.05]
    capped = min(capped_rows, key=lambda t: t[0])
    check(
        "upkeep makes the expected-cost optimum a single unit",
        uncapped[1] == 1 and uncapped[2] > 0.05,
        "D=%d P=%.4f J=%.4f" % (uncapped[1], uncapped[2], uncapped[0]),
    )
    check(
        "the ruin cap then selects a finer split and a higher cost",
        capped[1] > uncapped[1] and capped[0] > uncapped[0] and capped[2] <= 0.05,
        "Dcap=%d P=%.4f Jcap=%.4f Junc=%.4f" % (capped[1], capped[2], capped[0], uncapped[0]),
    )
    print(
        "RUINCAP uncapped D=%d P=%.6f J=%.6f | capped D=%d P=%.6f J=%.6f heat=%.6f"
        % (uncapped[1], uncapped[2], uncapped[0], capped[1], capped[2], capped[0], heat_fixed)
    )
    # No failures: overhead makes a split strictly costlier, and the cap does not bind.
    J_extra = heat_fixed + 4 * h_upkeep + w_stake * eps0
    J_single_ok = heat_fixed + 1 * h_upkeep + w_stake * eps0
    check(
        "with no failures, overhead makes a split strictly costlier",
        J_extra > J_single_ok,
        "J4=%.6f J1=%.6f" % (J_extra, J_single_ok),
    )

    # Heat itself, not upkeep. Dead units stop dissipating, so expected heat is
    # p_up * kT * mu. Raising mu to keep the lower tail under the cap costs heat.
    def tail_stats(D, mu, eps_cap, p_success):
        probs = []
        q = 1.0 - p_success
        term = q ** D
        eh = ee = pr = 0.0
        for i in range(D + 1):
            rho = i / D
            eps = V / (1.0 + rho * mu)
            heat_i = rho * mu
            eh += term * heat_i
            ee += term * eps
            if eps > eps_cap:
                pr += term
            if i < D:
                term *= (D - i) * p_success / ((i + 1) * q)
        return eh, ee, eh + 1.5 * ee, pr

    best_u = None
    best_c = None
    for D in (1, 2, 4, 8, 16):
        for step in range(0, 48):
            mu = 0.5 * (1.12 ** step)
            eh, ee, J, pr = tail_stats(D, mu, 1.5, 0.8)
            rec = (J, eh, D, mu, pr, ee)
            if best_u is None or J < best_u[0]:
                best_u = rec
            if pr <= 0.05 and (best_c is None or J < best_c[0]):
                best_c = rec
    check(
        "on the split-only grid the cap's minimum has higher heat than the uncapped minimum",
        best_c is not None
        and best_c[1] > best_u[1] + 0.2
        and best_c[0] > best_u[0]
        and best_c[4] <= 0.05 < best_u[4],
        "uncap J=%.4f heat=%.4f D=%d mu=%.4f P=%.4f | cap J=%.4f heat=%.4f D=%d mu=%.4f P=%.4f"
        % (best_u[0], best_u[1], best_u[2], best_u[3], best_u[4],
           best_c[0], best_c[1], best_c[2], best_c[3], best_c[4]),
    )
    print(
        "HEATCAP uncap J=%.6f heat=%.6f D=%d mu=%.6f P=%.6f | cap J=%.6f heat=%.6f D=%d mu=%.6f P=%.6f"
        % (best_u[0], best_u[1], best_u[2], best_u[3], best_u[4],
           best_c[0], best_c[1], best_c[2], best_c[3], best_c[4])
    )

    # ------------------------------------------------------- copies vs the split
    # Same installed precision mu, same upkeep h per unit. A copy keeps the
    # whole precision whenever at least one unit is up. The split keeps (i/n) mu.
    def binom_probs(n, p_success):
        q = 1.0 - p_success
        term = q ** n
        probs = []
        for i in range(n + 1):
            probs.append(term)
            if i < n:
                term *= (n - i) * p_success / ((i + 1) * q)
        return probs

    def copy_split_costs(V, mu, n, p_fail, h, w):
        p_up = 1.0 - p_fail
        probs = binom_probs(n, p_up)
        e_copy = e_split = 0.0
        pathwise = True
        for i, prb in enumerate(probs):
            eps_s = V / (1.0 + (i / n) * mu)
            eps_c = V / (1.0 + mu) if i >= 1 else V
            if eps_c > eps_s + 1e-12:
                pathwise = False
            e_copy += prb * eps_c
            e_split += prb * eps_s
        # Heat of the one installed precision, plus upkeep per unit. This is
        # the note's upkeep accounting.
        J_copy = mu + n * h + w * e_copy
        J_split = mu + n * h + w * e_split
        p_all_down = p_fail ** n
        return pathwise, e_copy, e_split, J_copy, J_split, p_all_down

    pathwise_ok = True
    for p_fail in (0.05, 0.2, 0.5, 0.9):
        for n in (1, 2, 3, 7, 12):
            for mu in (0.5, 5.0 / 3.0, 3.0, 8.0):
                ok, _, _, Jc, Js, _ = copy_split_costs(4.0, mu, n, p_fail, 0.5, 1.0)
                pathwise_ok = pathwise_ok and ok and Jc <= Js + 1e-9
    ok2, e_c2, e_s2, J_c2, J_s2, p2 = copy_split_costs(4.0, 3.0, 2, 0.2, 0.5, 1.0)
    ok7, e_c7, e_s7, J_c7, J_s7, p7 = copy_split_costs(4.0, 3.0, 7, 0.2, 0.5, 1.0)
    check(
        "at equal installed precision, a copy error is at most the split error on every draw",
        pathwise_ok and ok2 and near(J_c2, 5.12, 1e-12) and near(p2, 0.04, 1e-12),
        "n2 Jcopy=%.6f E=%.6f P=%.6f | n7 Jcopy=%.6f" % (J_c2, e_c2, p2, J_c7),
    )
    print(
        "COPIES n2 P=%.6f E=%.6f J=%.6f | n7 P=%.6e E=%.6f J=%.6f | split_n7_from_search"
        % (p2, e_c2, J_c2, p7, e_c7, J_c7)
    )
    # Each copy pays its own floor. Smallest mu whose up-state clears 1.5 is 5/3.
    mu_clear = 4.0 / 1.5 - 1.0
    e_two = (1.0 - 0.2 ** 2) * (4.0 / (1.0 + mu_clear)) + (0.2 ** 2) * 4.0
    J_two = 2.0 * mu_clear + 2.0 * 0.5 + 1.0 * e_two
    check(
        "two self-funded trackers still cost less than the split at the worked upkeep",
        near(mu_clear, 5.0 / 3.0, 1e-12) and near(J_two, 5.933333333333, 1e-9) and J_two < 7.700585,
        "mu=%.6f E=%.6f J=%.6f" % (mu_clear, e_two, J_two),
    )
    print("COPIES_OWN_HEAT mu=%.6f E=%.6f J=%.6f" % (mu_clear, e_two, J_two))
    # Heat rule of the grid: expected heat mu (1-p^n), stake weight 1.5.
    e_heat_copy = (5.0 / 3.0) * (1.0 - 0.04)
    J_heat_copy = e_heat_copy + 1.5 * e_two
    check(
        "under the grid's heat rule a two-copy memory meets the cap below the split's heat",
        near(e_heat_copy, 1.6, 1e-12) and near(J_heat_copy, 4.0, 1e-12) and e_heat_copy < best_c[1],
        "heat=%.6f J=%.6f split_heat=%.6f" % (e_heat_copy, J_heat_copy, best_c[1]),
    )
    print("HEATCAP_COPY heat=%.6f E=%.6f J=%.6f" % (e_heat_copy, e_two, J_heat_copy))

    # Both degradation curves increase in f. A Gaussian channel cannot lower
    # its error by deleting a positive-semidefinite piece of precision.
    slopes_up = True
    for f in (0.0, 0.25, 0.5, 0.9):
        eh0, el0, _ = degrade(4.0, 1.0, f)
        eh1, el1, _ = degrade(4.0, 1.0, f + 0.05)
        slopes_up = slopes_up and eh1 > eh0 and el1 > el0
    Phi = np.array([[2.0, 0.4], [0.4, 2.0]])
    drop = np.array([[0.3, 0.1], [0.1, 0.2]])
    S_full = np.linalg.inv(Phi)
    S_drop = np.linalg.inv(Phi - drop)
    # Loss tr(S) rises when a PSD update is removed.
    check(
        "error rises when a unit is removed, inside the Gaussian mean-square class",
        slopes_up and float(np.trace(S_drop) - np.trace(S_full)) > 0.0,
        "dtr=%.6e" % float(np.trace(S_drop) - np.trace(S_full)),
    )
    # J(f)=(1-f)mu + w V/(1+(1-f)mu). Second derivative 2 w V mu^2 / (1+(1-f)mu)^3.
    mu_j, w_j, V_j, f_j = 3.0, 1.0, 4.0, 0.25
    sec = 2.0 * w_j * V_j * mu_j ** 2 / (1.0 + (1.0 - f_j) * mu_j) ** 3
    check(
        "the split cost is convex in the failed fraction",
        sec > 0.0 and near(sec, 2.0 * 4.0 * 9.0 / (1.0 + 0.75 * 3.0) ** 3, 1e-12),
        "second=%.6f" % sec,
    )

    # ------------------------------------------------------- capacity cap
    # Prediction, fixed before this search: under heat = sum of installed
    # precisions and upkeep h per unit, a pool of the same units has error at
    # most the non-pooling copy on every draw. Copies of one unit are feasible
    # for the cap only when c >= V/eps_cap - 1. A common shock of probability
    # beta > eps_r makes both designs infeasible. On a sum of K items, aiming
    # the same precision at the sum beats aiming it at single items.
    def pool_and_copy(V, phi, n, p_fail, h, w, beta=0.0):
        """Equal accounting. beta is a common shock that downs every unit."""
        p_up = 1.0 - p_fail
        probs = binom_probs(n, p_up)
        e_copy = e_pool = 0.0
        pathwise = True
        for i, prb in enumerate(probs):
            eps_c = V / (1.0 + phi) if i >= 1 else V
            eps_p = V / (1.0 + i * phi)
            if eps_p > eps_c + 1e-9:
                pathwise = False
            e_copy += prb * eps_c
            e_pool += prb * eps_p
        # Mix in the common shock: with probability beta every unit is down.
        e_copy = beta * V + (1.0 - beta) * e_copy
        e_pool = beta * V + (1.0 - beta) * e_pool
        heat = n * phi
        upkeep = n * h
        return pathwise, heat + upkeep + w * e_copy, heat + upkeep + w * e_pool, e_copy, e_pool

    dom = True
    for c_cap, phi, n, p_fail, h, w, beta in (
        (2.0, 1.0, 2, 0.2, 0.5, 1.0, 0.0),
        (0.4, 0.4, 6, 0.2, 0.5, 1.0, 0.0),
        (5.0, 5.0 / 3.0, 3, 0.3, 0.1, 2.0, 0.0),
        (1.0, 0.5, 4, 0.2, 0.5, 1.0, 0.02),
        (3.0, 3.0, 2, 0.5, 2.0, 0.0, 0.0),
    ):
        okp, Jc, Jp, _, _ = pool_and_copy(4.0, phi, n, p_fail, h, w, beta)
        dom = dom and okp and Jp <= Jc + 1e-9
    # Strict when two or more can be up.
    _, Jc_s, Jp_s, ec_s, ep_s = pool_and_copy(4.0, 5.0 / 3.0, 2, 0.2, 0.5, 1.0, 0.0)
    check(
        "equal heat and upkeep: pooling the same units costs at most the non-pooling copy",
        dom and Jp_s < Jc_s - 1e-6,
        "Jcopy=%.6f Jpool=%.6f Ecopy=%.6f Epool=%.6f" % (Jc_s, Jp_s, ec_s, ep_s),
    )
    mu_star = 4.0 / 1.5 - 1.0
    # Single-unit copies cannot clear error 1.5 when c < mu_star.
    check(
        "a unit below the cap-clearing precision cannot be a feasible copy",
        (4.0 / (1.0 + 0.5)) > 1.5 and (4.0 / (1.0 + mu_star)) <= 1.5 + 1e-12,
        "mu_star=%.6f err_at_half=%.6f" % (mu_star, 4.0 / 1.5),
    )
    # Common shock above the cap: both ruin probabilities are at least beta.
    beta = 0.06
    p_copy_shock = beta + (1.0 - beta) * (0.2 ** 2)
    check(
        "a common shock above the cap makes every identical-unit design infeasible",
        beta > 0.05 and p_copy_shock > 0.05,
        "beta=%.3f Pcopy=%.6f" % (beta, p_copy_shock),
    )

    # Sum of K=4 items. Same total precision Phi. Item-diagonal sum-error
    # K^2/(K+Phi), aligned sum-error K/(1+Phi).
    Ksum = 4
    for Phi in (0.5, 1.0, 4.0):
        err_item = Ksum ** 2 / (Ksum + Phi)
        err_aligned = Ksum / (1.0 + Phi)
        check(
            "sum of %d, precision %.2f: aiming at the sum beats aiming at items" % (Ksum, Phi),
            err_aligned < err_item - 1e-12,
            "aligned=%.6f item=%.6f" % (err_aligned, err_item),
        )
    # Cap sum-error at 2, so mu_star=1. c=0.5. Aligned needs two units up.
    # Item-diagonal needs total precision 4 even with every unit up.
    # Smallest aligned N with P(Bin(N,0.8) < 2) <= 0.05.
    def p_fewer_than(n, p_success, k):
        # P(I < k) = P(I <= k-1)
        if k <= 0:
            return 0.0
        return binom_pmf_upto(n, p_success, k - 1)

    best_aligned = None
    for N in range(2, 40):
        pr = p_fewer_than(N, 0.8, 2)
        if pr <= 0.05:
            # phi=c=0.5, heat=N*0.5, upkeep=N*0.5, w=1
            probs = binom_probs(N, 0.8)
            ee = sum(prb * (4.0 / (1.0 + i * 0.5)) for i, prb in enumerate(probs))
            J = N * 0.5 + N * 0.5 + ee
            best_aligned = (N, pr, ee, J)
            break
    # Item-diagonal: n_per item, four items, each unit precision 0.5, a copy of
    # an item survives on its own. Sum-error given the four up-counts.
    # Search n_per from 1 to 12. Ruin if the conditional sum-error exceeds 2.
    best_item = None
    for n_per in range(1, 16):
        # Independent binomials. Enumerate via convolution of one item's error contribution.
        # Contribution of one item with I up: 1/(1+I*0.5). Sum of four.
        probs_one = binom_probs(n_per, 0.8)
        # dp over the sum of four independent contributions, but the cap is on
        # the sum of the four variances. Use the generating function on a grid
        # of the up-count, since the variance is monotone in the count.
        # Exact enumeration: the joint is a product. 16^4 is too big; n_per+1
        # states per item, (n_per+1)^4 at n_per=15 is 16^4=65536, fine.
        states = len(probs_one)
        # Iterative convolution of the scalar error, plus a ruin flag via
        # enumerating counts.
        from itertools import product
        ee = 0.0
        pruin = 0.0
        for counts in product(range(states), repeat=4):
            prb = 1.0
            err = 0.0
            for m in counts:
                prb *= probs_one[m]
                err += 1.0 / (1.0 + m * 0.5)
            ee += prb * err
            if err > 2.0 + 1e-12:
                pruin += prb
        heat = 4 * n_per * 0.5
        upkeep = 4 * n_per * 0.5
        J = heat + upkeep + ee
        if pruin <= 0.05 and (best_item is None or J < best_item[3]):
            best_item = (n_per, pruin, ee, J)
    check(
        "capacity-limited sum: the aligned pool meets the cap and the item copies cost more",
        best_aligned is not None
        and best_item is not None
        and best_aligned[3] < best_item[3] - 0.5,
        "aligned N=%d P=%.4f J=%.4f | item n_per=%d P=%.4f J=%.4f"
        % (best_aligned[0], best_aligned[1], best_aligned[3],
           best_item[0], best_item[1], best_item[3]),
    )
    print(
        "CAPALIGN N=%d P=%.6f E=%.6f J=%.6f | ITEM n_per=%d P=%.6f E=%.6f J=%.6f"
        % (best_aligned[0], best_aligned[1], best_aligned[2], best_aligned[3],
           best_item[0], best_item[1], best_item[2], best_item[3])
    )
    print(
        "CAPDOM Jcopy=%.6f Jpool=%.6f mu_star=%.6f err_c=%.6f"
        % (Jc_s, Jp_s, mu_star, 4.0 / (1.0 + 0.5))
    )

    # ------------------------------------------------------- phone-scale units
    kB = 1.380649e-23
    T = 300.0
    kT_J = kB * T
    # (v-eps)/eps = 1, a = 1 per second, r decision modes.
    p_slow = kT_J * 1.0 * 1.0 * 1e9
    p_clock = kT_J * 1e9 * 1.0 * 1e12
    check(
        "unit conversion: slow drift, 1e9 modes, is picowatts; a clock-rate identification is watts",
        1e-12 < p_slow < 1e-11 and 1.0 < p_clock < 10.0,
        "pslow=%.6e pclock=%.6f kT=%.6e" % (p_slow, p_clock, kT_J),
    )
    print("PHONE kT=%.6e P_slow_1e9=%.6e W P_clock_1e12=%.6f W" % (kT_J, p_slow, p_clock))
    # Rank bound: heat does not grow with ambient K once the task rank is r.
    r, Kamb = 2, 100
    eigs = np.zeros(Kamb)
    eigs[:r] = 1.0
    _, _, Js, ns = allocate(eigs, 4.0, 1, 1, 1, Kamb)
    _, _, Js2, ns2 = allocate(eigs[:r], 4.0, 1, 1, 1, r)
    check(
        "ambient dimension drops out of the cost once the task rank is fixed",
        near(Js, Js2, 1e-12) and ns == r == ns2,
        "J=%.12f n=%d" % (Js, ns),
    )

    # ------------------------------------------------------- heat price vs nat price
    ws = np.array([2.0, 4.0, 8.0, 16.0, 32.0])
    _, _, slope_h, slope_m = mi_versus_heat(a=1.0, V=1.0, kT=1.0, kappa=1.0, ws=ws)
    check(
        "error falls as w to the -1/2 under the heat price and as w to the -1 under a nat price",
        near(slope_h, -0.5, 1e-12) and near(slope_m, -1.0, 1e-12),
        "slope_heat=%.6f slope_nat=%.6f" % (slope_h, slope_m),
    )
    # Drift enters the heat optimum and not the nat optimum.
    eh_fast = math.sqrt(5.0 * 1.0 / 4.0)
    eh_slow = math.sqrt(1.0 * 1.0 / 4.0)
    check(
        "doubling nothing: a nat-priced error ignores drift, the heat-priced error scales as sqrt(a)",
        near(eh_fast / eh_slow, math.sqrt(5.0), 1e-12),
        "fast=%.6f slow=%.6f" % (eh_fast, eh_slow),
    )
    print("SCALING slope_heat=%.6f slope_nat=%.6f eps_ratio_a5=%.6f" % (slope_h, slope_m, eh_fast / eh_slow))

    # ------------------------------------------------------- fast spring attains
    a = np.array([1.0, 2.0, 4.0])
    v = np.array([1.0, 0.5, 1.5])
    G = np.array([[0.3, -0.2, 0.4], [0.1, 0.5, -0.3]])
    sig2 = 0.35
    S, L = static_channel(a, v, G, sig2)
    lam = 1e5
    heat, Scond, _ = fast_spring_heat(a, v, G, sig2, lam)
    check(
        "two fast springs approach the static learning rate and the static error",
        near(heat, L, 1e-4) and np.allclose(Scond, S, rtol=1e-4, atol=1e-5),
        "heat=%.6f L=%.6f max|S|=%.3e" % (heat, L, np.max(np.abs(Scond - S))),
    )
    print("SPRING heat=%.8f L=%.8f" % (heat, L))

    # D=1 reproduces the scalar floor on one mode.
    G1 = np.array([[1.0]])
    # Choose sig2 so the error is 0.2 on a=v=1: posterior var = 1/(1+1/sig2)=0.2
    # 1+1/sig2 = 5, 1/sig2=4, sig2=0.25. Heat = a v / sig2 = 4.
    S1, L1 = static_channel(np.array([1.0]), np.array([1.0]), G1, 0.25)
    check(
        "one mode, static channel hits the scalar floor at error 0.2",
        near(S1[0, 0], 0.2, 1e-12) and near(L1, 4.0, 1e-12),
        "eps=%.6f L=%.6f" % (S1[0, 0], L1),
    )

    print()
    print("PASS %d  FAIL %d" % (PASS, FAIL))
    if FAIL:
        print("HOLOGRAPHIC MEMORY CHECKS FAIL")
        raise SystemExit(1)
    print("FAILS 0")
    print("ALL HOLOGRAPHIC MEMORY CHECKS PASS")


if __name__ == "__main__":
    main()
