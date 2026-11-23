#!/usr/bin/env python3
"""Checks for theory/NON_GAUSSIAN_FLOOR_2026-11-23.md (T49).

Run from the repo root:
  nice -n 19 python3 theory/non_gaussian_floor_checks/non_gaussian_floor_checks.py

Three classes beyond the Gaussian/OU and telegraph classes:
  A. diffusive worlds with any smooth stationary law (heavy tails included),
  B. regime-switching (volatility-switching) diffusive worlds,
  C. rare-shock (jump / reset) worlds.
Every check is a quadrature, a code identity, or an exact steady state of a
finite bipartite Markov chain. None is a measurement of a real system.
A failure sets a nonzero exit code.
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy import integrate, special

checks_failed = []
EULER = 0.5772156649015329
KAPPA_GAUSS_OFFSET = -EULER - math.log(2.0)  # E ln Z^2, Z standard normal


def check(name, ok, detail):
    print("CHECK %s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        checks_failed.append(name)


def fmt(x):
    return "%.6g" % x


# ---------------------------------------------------------------- helpers

def student_logpdf(x, nu, s=1.0):
    return (special.gammaln((nu + 1) / 2) - special.gammaln(nu / 2)
            - 0.5 * math.log(nu * math.pi * s * s)
            - (nu + 1) / 2 * np.log1p((x / s) ** 2 / nu))


def student_score(x, nu, s=1.0):
    return -(nu + 1) * x / (nu * s * s + x * x)


def student_fisher(nu, s=1.0):
    return (nu + 1) / ((nu + 3) * s * s)


def grid_channel_mse(px, x, P):
    """Bayes MSE of X from M for prior weights px on x and channel P[m, x]."""
    joint = P * px[None, :]
    pm = joint.sum(axis=1)
    keep = pm > 0
    mean = (joint[keep] @ x) / pm[keep]
    second = (joint[keep] @ (x * x)) / pm[keep]
    return float(np.sum(pm[keep] * (second - mean * mean)))


def gauss_channel(x, m, g, sig):
    """Column-normalized discretized Gaussian channel N(g(x), sig^2) on grid m."""
    dm = m[1] - m[0]
    G = np.exp(-0.5 * ((m[:, None] - g[None, :]) / sig) ** 2) / (sig * math.sqrt(2 * math.pi)) * dm
    return G / G.sum(axis=0, keepdims=True)


def info_I_L(px, P):
    """Mutual information I and lautum information L (nats) of a discrete channel."""
    pm = P @ px
    with np.errstate(divide="ignore", invalid="ignore"):
        lp = np.log(np.where(P > 0, P, 1e-300))
        lpm = np.log(np.where(pm > 0, pm, 1e-300))
    I = float(np.sum(px[None, :] * P * (lp - lpm[:, None])))
    L = float(np.sum(px[None, :] * pm[:, None] * (lpm[:, None] - lp)))
    return I, L


def stationary(Q):
    """Stationary law of a CTMC with sparse generator Q (rows sum to zero)."""
    n = Q.shape[0]
    A = Q.T.tocsr().tolil()
    A[0, :] = np.ones(n)
    b = np.zeros(n)
    b[0] = 1.0
    p = spla.spsolve(A.tocsc(), b)
    return np.maximum(p, 0.0) / np.maximum(p, 0.0).sum()


# ======================================================== 0. sentence lock

def check_sentence():
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sentence = ("The law of adaptive organization (hypothesis): strongly selected systems "
                "minimize the cost of judgment.")
    with open(os.path.join(root, "THEORY.md"), encoding="utf-8") as f:
        th = f.read()
    with open(os.path.join(root, "theory", "NON_GAUSSIAN_FLOOR_2026-11-23.md"), encoding="utf-8") as f:
        note = f.read()
    check("hypothesis_sentence_byte_identical", sentence in th and sentence in note,
          "present in THEORY.md and in the note")


# ======================================================== A. diffusive class

def section_A():
    print("== A. diffusive worlds, any smooth stationary distribution ==")
    # A1. Fisher information of Student-t laws (heavy tails) by quadrature.
    worst = 0.0
    for nu in (1.0, 2.0, 3.0, 5.0, 30.0):
        f = lambda t: (student_score(t, nu) ** 2) * math.exp(student_logpdf(t, nu))
        val = integrate.quad(f, -np.inf, np.inf, limit=400)[0]
        worst = max(worst, abs(val - student_fisher(nu)) / student_fisher(nu))
    check("A1_student_t_fisher_closed_form", worst < 1e-8,
          "J=(nu+1)/((nu+3)s^2) for nu in 1,2,3,5,30; max rel err %s; Cauchy J=1/2" % fmt(worst))
    # Gaussian minimizes J at fixed variance (Stam / Cramer-Rao): J*Var >= 1.
    jv = [student_fisher(nu) * nu / (nu - 2) for nu in (3.0, 5.0, 30.0)]
    check("A1b_fisher_times_variance_ge_one", all(v > 1.0 for v in jv),
          "Student-t J*Var = %s (Gaussian = 1)" % ", ".join(fmt(v) for v in jv))

    # A2. Van Trees floor E[F] >= 1/eps - J on worlds x channels, and the
    #     fast-Gaussian-copy gap 0 <= D/s^2 - D(1/eps - J) <= D J.
    x = np.linspace(-40.0, 40.0, 4001)
    dx = x[1] - x[0]
    worlds = {}
    lg = -0.5 * x * x
    worlds["gauss_v1"] = (np.exp(lg), 1.0)
    for nu in (2.0, 3.0):
        worlds["student_nu%g" % nu] = (np.exp(student_logpdf(x, nu)), student_fisher(nu))
    dw = np.exp(-x ** 4 / 4 + x ** 2)
    worlds["double_well"] = (dw, None)
    chans = {
        "linear": (lambda t: t, lambda t: np.ones_like(t)),
        "wiggle": (lambda t: t + 0.4 * np.sin(2 * t), lambda t: 1 + 0.8 * np.cos(2 * t)),
        "saturating": (lambda t: 2 * np.tanh(t) + 0.2 * t, lambda t: 2 / np.cosh(t) ** 2 + 0.2),
    }
    n_ok = n_tot = 0
    gap_ok = True
    worst_margin = math.inf
    for wname, (dens, J) in worlds.items():
        px = dens / dens.sum()
        if J is None:
            sc = np.gradient(np.log(np.maximum(dens, 1e-300)), dx)
            J = float(np.sum(px * sc * sc))
        for cname, (g, gp) in chans.items():
            for sig in (0.15, 0.4, 1.0):
                gx = g(x)
                m = np.arange(gx.min() - 8 * sig, gx.max() + 8 * sig, min(0.02, sig / 10))
                if wname == "double_well" or wname == "gauss_v1":
                    sel = px > 1e-14
                else:
                    sel = np.ones_like(px, dtype=bool)
                xs, pxs = x[sel], px[sel] / px[sel].sum()
                gxs = g(xs)
                m = np.arange(gxs.min() - 8 * sig, gxs.max() + 8 * sig, min(0.02, sig / 10))
                P = gauss_channel(xs, m, gxs, sig)
                eps = grid_channel_mse(pxs, xs, P)
                EF = float(np.sum(pxs * gp(xs) ** 2)) / sig ** 2
                lhs, rhs = EF, 1.0 / eps - J
                n_tot += 1
                margin = (lhs - rhs) / lhs
                worst_margin = min(worst_margin, margin)
                if lhs >= rhs * (1 - 1e-3):
                    n_ok += 1
                if cname == "linear":
                    gap = 1.0 / sig ** 2 - (1.0 / eps - J)
                    if not (-1e-3 * J <= gap <= J * (1 + 1e-3)):
                        gap_ok = False
    check("A2_van_trees_floor_on_worlds_and_channels", n_ok == n_tot,
          "%d/%d (world, channel, sigma) cases satisfy D*E[F] >= D(1/eps - J); min relative margin %s"
          % (n_ok, n_tot, fmt(worst_margin)))
    check("A2b_fast_copy_gap_between_0_and_DJ", gap_ok,
          "for the Gaussian copy, 0 <= D/sigma^2 - D(1/eps-J) <= D*J on every world and sigma")

    # A3. The identity l_X = -D E[(d_x ln p(m|x))^2] for an exogenous world with
    #     ANY drift f and ANY (non-stationary) marginal: the drift term integrates to 0.
    rng = np.random.default_rng(20261123)
    xg = np.linspace(-6, 6, 1201)
    mg = np.linspace(-9, 9, 1801)
    hx = xg[1] - xg[0]
    worst = 0.0
    for trial in range(4):
        c = rng.normal(0, 1.2, 3)
        wts = rng.dirichlet(np.ones(3))
        pxv = sum(w * np.exp(-0.5 * ((xg - ci) / 0.8) ** 2) for w, ci in zip(wts, c))
        pxv /= pxv.sum() * hx
        a1, a2 = rng.normal(0, 1, 2)
        f = a1 * np.sin(xg) - 0.5 * xg ** 3 / 9 + a2  # arbitrary drift, no detailed balance
        D = 0.7
        sig = 0.5 + 0.3 * np.tanh(xg)  # x-dependent channel width
        gx = xg + 0.3 * np.sin(1.5 * xg)
        logp = -0.5 * ((mg[:, None] - gx[None, :]) / sig[None, :]) ** 2 - np.log(sig[None, :] * math.sqrt(2 * math.pi))
        pmx = np.exp(logp)
        joint = pmx * pxv[None, :]
        dj = np.gradient(joint, hx, axis=1)
        Jx = f[None, :] * joint - D * dj
        score = np.gradient(logp, hx, axis=1)
        dm = mg[1] - mg[0]
        lX = float(np.sum(Jx * score) * hx * dm)
        rhs = -D * float(np.sum(joint * score * score) * hx * dm)
        err = abs(lX - rhs) / abs(rhs)
        worst = err if not math.isfinite(err) else max(worst, err)
    check("A3_destruction_identity_any_drift", math.isfinite(worst) and worst < 2e-3,
          "world-side flow = -D E[channel Fisher] for 4 random non-equilibrium drifts and marginals; max rel err %s" % fmt(worst))

    # A4. Exact steady state of a bipartite lattice chain: Student-t (nu=3) world,
    #     fast spring memory. JP-heat Q >= I_alt; I_alt above the floor; Q -> D/sigma^2.
    nu, D, sig = 3.0, 1.0, 0.5
    hX, hM = 0.25, 0.1
    xs = np.arange(-10, 10 + 1e-9, hX)
    ms = np.arange(-11, 11 + 1e-9, hM)
    nx, nm = len(xs), len(ms)
    lpi = student_logpdf(xs, nu)
    res = {}
    for gam in (5.0, 50.0, 500.0):
        rows, cols, vals = [], [], []
        idx = lambda i, j: i * nm + j
        E = (ms[None, :] - xs[:, None]) ** 2 / (2 * sig * sig)
        for i in range(nx):
            for di in (-1, 1):
                k = i + di
                if 0 <= k < nx:
                    r = D / hX ** 2 * math.exp(0.5 * (lpi[k] - lpi[i]))
                    for j in range(nm):
                        rows.append(idx(i, j)); cols.append(idx(k, j)); vals.append(r)
        base = gam * sig * sig / hM ** 2
        mem_edges = []
        for i in range(nx):
            for j in range(nm):
                for dj_ in (-1, 1):
                    k = j + dj_
                    if 0 <= k < nm:
                        r = base * math.exp(-0.5 * (E[i, k] - E[i, j]))
                        rows.append(idx(i, j)); cols.append(idx(i, k)); vals.append(r)
                        mem_edges.append((i, j, k, r))
        n = nx * nm
        Q = sp.csr_matrix((vals, (rows, cols)), shape=(n, n))
        Q = Q - sp.diags(np.asarray(Q.sum(axis=1)).ravel())
        p = stationary(Q).reshape(nx, nm)
        pxm = p.sum(axis=1)
        cond = p / pxm[:, None]
        heat = 0.0
        ialt = 0.0
        for (i, j, k, r) in mem_edges:
            fl = p[i, j] * r
            heat += fl * (E[i, j] - E[i, k])
            if cond[i, j] > 0 and cond[i, k] > 0:
                ialt += fl * math.log(cond[i, k] / cond[i, j])
        pm = p.sum(axis=0)
        mean = (p.T @ xs) / pm
        eps = float(np.sum(pm * ((p.T @ xs ** 2) / pm - mean ** 2)))
        res[gam] = (heat, ialt, eps)
    J = student_fisher(nu)
    ok_jp = all(h >= ia - 1e-9 for (h, ia, _) in res.values())
    ok_floor = all(ia >= D * (1 / e - J) * 0.97 for (_, ia, e) in res.values())
    ratios = [res[g][0] / (D / sig ** 2) for g in (5.0, 50.0, 500.0)]
    conv = abs(ratios[2] - 1) < 0.05 and abs(ratios[2] - 1) < abs(ratios[0] - 1) + 1e-12
    check("A4_lattice_JP_heat_and_floor", ok_jp and ok_floor,
          "Student-t nu=3 lattice world, spring memory: Q>=I_alt and I_alt >= 0.97*D(1/eps-J) at gamma=5,50,500")
    check("A4b_fast_spring_heat_to_D_over_sigma2", conv,
          "Q/(D/sigma^2) = %s at gamma = 5, 50, 500" % ", ".join(fmt(r) for r in ratios))

    # A5. Cost sandwich. OU: lower bound = known minimum 2 sqrt(kT a v w) - kT a.
    kT, a, v, w = 1.0, 1.0, 1.0, 9.0
    Dou = a * v
    lower = 2 * math.sqrt(kT * Dou * w) - kT * Dou * (1 / v)
    check("A5_ou_lower_bound_is_known_minimum", abs(lower - (2 * math.sqrt(kT * a * v * w) - kT * a)) < 1e-12,
          "2 sqrt(kT D w) - kT D J = %s at a=v=1, w=9" % fmt(lower))
    rows = []
    for nu in (1.0, 2.0, 3.0):
        Jn = student_fisher(nu)
        for wv in (1.0, 10.0, 100.0):
            lo = 2 * math.sqrt(wv) - Jn if wv >= Jn ** 2 else wv / Jn
            up = 2 * math.sqrt(wv)
            rows.append((nu, wv, lo, up))
    ok = all(lo <= up for (_, _, lo, up) in rows)
    check("A5b_sandwich_student_t", ok,
          "kT=D=1: J* in [2sqrt(w)-J, 2sqrt(w)]; e.g. Cauchy w=10: [%s, %s] (blind cost infinite)"
          % (fmt(rows[1][2]), fmt(rows[1][3])))
    return res


# ======================================================== B. switching class

def section_B():
    print("== B. regime-switching (volatility) worlds ==")
    a = 1.0
    Ds = np.array([0.25, 4.0])
    r12, r21 = 0.3, 0.6
    hX = 0.1
    xs = np.arange(-12, 12 + 1e-9, hX)
    nx = len(xs)
    # world lattice chain on (s, x): detailed balance to N(0, D_s/a) in each regime
    rows, cols, vals = [], [], []
    idx = lambda s, i: s * nx + i
    for s in range(2):
        for i in range(nx):
            for di in (-1, 1):
                k = i + di
                if 0 <= k < nx:
                    r = Ds[s] / hX ** 2 * math.exp(-0.5 * a * (xs[k] ** 2 - xs[i] ** 2) / (2 * Ds[s]))
                    rows.append(idx(s, i)); cols.append(idx(s, k)); vals.append(r)
            rows.append(idx(s, i)); cols.append(idx(1 - s, i)); vals.append(r12 if s == 0 else r21)
    n = 2 * nx
    Q = sp.csr_matrix((vals, (rows, cols)), shape=(n, n))
    Q = Q - sp.diags(np.asarray(Q.sum(axis=1)).ravel())
    p = stationary(Q).reshape(2, nx)
    ps = p.sum(axis=1)
    pxs = p / ps[:, None]
    Js = []
    for s in range(2):
        sc = np.gradient(np.log(np.maximum(pxs[s], 1e-300)), hX)
        Js.append(float(np.sum(pxs[s] * sc * sc)))
    Js = np.array(Js)
    check("B1_regime_conditional_distributions", abs(ps[0] - r21 / (r12 + r21)) < 1e-9 and np.all(Js > 0),
          "p(s)=%s; within-regime Fisher J_s=%s (non-Gaussian mixtures of OU distributions)"
          % (", ".join(fmt(t) for t in ps), ", ".join(fmt(t) for t in Js)))

    # B2. Per-regime Van Trees floor for regime-tuned AND regime-blind Gaussian copies.
    ok = True
    worst = math.inf
    for sig_pair in ((0.2, 0.2), (0.2, 0.6), (0.5, 0.5), (0.1, 0.4)):
        m = np.arange(-14, 14, 0.02)
        eps_s, EF_s = [], []
        # joint over (s, x, m) with channel N(x, sigma_s^2); Bayes estimator from m only
        Ps = [gauss_channel(xs, m, xs, sig_pair[s]) for s in range(2)]
        joint = [Ps[s] * (ps[s] * pxs[s])[None, :] for s in range(2)]
        pm = joint[0].sum(axis=1) + joint[1].sum(axis=1)
        mean = (joint[0] @ xs + joint[1] @ xs) / pm
        for s in range(2):
            err = ((xs[None, :] - mean[:, None]) ** 2 * joint[s]).sum() / ps[s]
            eps_s.append(float(err))
            EF_s.append(1.0 / sig_pair[s] ** 2)
        lhs = sum(ps[s] * Ds[s] * EF_s[s] for s in range(2))
        rhs = sum(ps[s] * Ds[s] * (1 / eps_s[s] - Js[s]) for s in range(2))
        worst = min(worst, (lhs - rhs) / lhs)
        ok = ok and lhs >= rhs
    check("B2_per_regime_van_trees_floor", ok,
          "sum_s p_s D_s E[F_s] >= sum_s p_s D_s (1/eps_s - J_s) for 4 copies (tuned and blind); min rel margin %s" % fmt(worst))

    # B3. Hybrid destruction identity and heat on an exact bipartite chain:
    #     world (s, x) lattice, memory spring with regime-tuned stiffness.
    hXc, hM = 0.25, 0.1
    xc = np.arange(-8, 8 + 1e-9, hXc)
    mc = np.arange(-9, 9 + 1e-9, hM)
    nxc, nmc = len(xc), len(mc)
    sig_s = np.array([0.35, 0.7])
    out = {}
    for gam in (20.0, 400.0):
        rows, cols, vals = [], [], []
        idx3 = lambda s, i, j: (s * nxc + i) * nmc + j
        E = np.stack([(mc[None, :] - xc[:, None]) ** 2 / (2 * sig_s[s] ** 2) for s in range(2)])
        wx_edges, ws_edges, mem_edges = [], [], []
        for s in range(2):
            for i in range(nxc):
                for di in (-1, 1):
                    k = i + di
                    if 0 <= k < nxc:
                        r = Ds[s] / hXc ** 2 * math.exp(-0.5 * a * (xc[k] ** 2 - xc[i] ** 2) / (2 * Ds[s]))
                        wx_edges.append((s, i, k, r))
                rs = r12 if s == 0 else r21
                ws_edges.append((s, i, rs))
                for j in range(nmc):
                    for dj_ in (-1, 1):
                        k = j + dj_
                        if 0 <= k < nmc:
                            r = gam * sig_s[s] ** 2 / hM ** 2 * math.exp(-0.5 * (E[s, i, k] - E[s, i, j]))
                            mem_edges.append((s, i, j, k, r))
        for (s, i, k, r) in wx_edges:
            for j in range(nmc):
                rows.append(idx3(s, i, j)); cols.append(idx3(s, k, j)); vals.append(r)
        for (s, i, rs) in ws_edges:
            for j in range(nmc):
                rows.append(idx3(s, i, j)); cols.append(idx3(1 - s, i, j)); vals.append(rs)
        for (s, i, j, k, r) in mem_edges:
            rows.append(idx3(s, i, j)); cols.append(idx3(s, i, k)); vals.append(r)
        nn = 2 * nxc * nmc
        Q = sp.csr_matrix((vals, (rows, cols)), shape=(nn, nn))
        Q = Q - sp.diags(np.asarray(Q.sum(axis=1)).ravel())
        pj = stationary(Q).reshape(2, nxc, nmc)
        pw = pj.sum(axis=2)
        cond = pj / np.maximum(pw[:, :, None], 1e-300)
        lc = np.log(np.maximum(cond, 1e-300))
        heat = ialt = 0.0
        for (s, i, j, k, r) in mem_edges:
            fl = pj[s, i, j] * r
            heat += fl * (E[s, i, j] - E[s, i, k])
            ialt += fl * (lc[s, i, k] - lc[s, i, j])
        dX = sum(pw[s, i] * r * float(np.sum(cond[s, i] * (lc[s, i] - lc[s, k]))) for (s, i, k, r) in wx_edges)
        dS = sum(pw[s, i] * rs * float(np.sum(cond[s, i] * (lc[s, i] - lc[1 - s, i]))) for (s, i, rs) in ws_edges)
        ps_c = pw.sum(axis=1)
        tuned = sum(ps_c[s] * Ds[s] / sig_s[s] ** 2 for s in range(2))
        kl12 = 0.5 * (sig_s[0] ** 2 / sig_s[1] ** 2 - 1 - math.log(sig_s[0] ** 2 / sig_s[1] ** 2))
        kl21 = 0.5 * (sig_s[1] ** 2 / sig_s[0] ** 2 - 1 - math.log(sig_s[1] ** 2 / sig_s[0] ** 2))
        switch = ps_c[0] * r12 * kl12 + ps_c[1] * r21 * kl21
        out[gam] = (heat, ialt, dX, dS, tuned, switch)
    h, ia, dX, dS, tuned, switch = out[400.0]
    ok_id = all(abs(v[1] - (v[2] + v[3])) < 1e-8 * max(1.0, abs(v[1])) for v in out.values())
    check("B3_hybrid_destruction_identity_exact", ok_id,
          "memory learning rate = diffusive part + switching KL part (exact steady state), gamma=20,400")
    check("B3b_switching_part_matches_KL_surcharge", abs(dS - switch) / switch < 0.05,
          "switching part %s vs fast-limit sum p_s r KL(sigma_s||sigma_s') = %s" % (fmt(dS), fmt(switch)))
    check("B3c_fast_tuned_heat_to_identity", h >= ia - 1e-9 and abs(h / (tuned + switch) - 1) < 0.06,
          "Q=%s, I_alt=%s, fast-limit value sum p_s D_s/sigma_s^2 + surcharge = %s (gamma=400)"
          % (fmt(h), fmt(ia), fmt(tuned + switch)))

    # B4. Regime awareness: leading-order saving 2 sqrt(kT w)(sqrt(Dbar) - E sqrt(D_S)),
    #     against a stake-independent surcharge; explicit threshold stake.
    kT = 1.0
    Dbar = float(np.sum(ps * Ds))
    EsqrtD = float(np.sum(ps * np.sqrt(Ds)))
    ratio = math.sqrt(Ds[0] / Ds[1])
    kl_a = 0.5 * (ratio - 1 - math.log(ratio))
    kl_b = 0.5 * (1 / ratio - 1 - math.log(1 / ratio))
    sur = ps[0] * r12 * kl_a + ps[1] * r21 * kl_b
    # constant-volatility world at Dbar: floor 2 sqrt(kT Dbar w) - kT Dbar J_c, J_c = a/Dbar (OU)
    Jc = a / Dbar
    w_thr = ((kT * (sur + Dbar * Jc)) / (2 * math.sqrt(kT) * (math.sqrt(Dbar) - EsqrtD))) ** 2
    w = 4 * w_thr
    design = 2 * math.sqrt(kT * w) * EsqrtD + kT * sur
    const_floor = 2 * math.sqrt(kT * Dbar * w) - kT * Dbar * Jc
    check("B4_regime_aware_beats_constant_world_floor_above_threshold", design < const_floor and w_thr > 0,
          "Dbar=%s, E sqrt(D)=%s, surcharge=%s nats/time, threshold stake %s; at 4x: design %s < constant-world floor %s"
          % (fmt(Dbar), fmt(EsqrtD), fmt(sur), fmt(w_thr), fmt(design), fmt(const_floor)))


# ======================================================== C. shock class

def section_C():
    print("== C. rare-shock (jump / reset) worlds ==")
    v = 1.0
    x = np.linspace(-8, 8, 801)
    px = np.exp(-0.5 * x * x / v)
    px /= px.sum()
    m = np.linspace(-14, 14, 1401)
    dm = m[1] - m[0]

    # C1. Gaussian copy: E_{x,x'} KL = I + L = v/sigma^2 (exact closed form).
    worst = 0.0
    for sig in (0.2, 0.5, 1.0):
        P = gauss_channel(x, m, x, sig)
        I, L = info_I_L(px, P)
        worst = max(worst, abs((I + L) - v / sig ** 2) / (v / sig ** 2))
        # direct double sum check of E KL = I + L
    sig = 0.5
    P = gauss_channel(x[::8], m, x[::8], sig)
    pxc = px[::8] / px[::8].sum()
    lP = np.log(np.maximum(P, 1e-300))
    EKL = float(sum(pxc[i] * pxc[k] * np.sum(P[:, i] * (lP[:, i] - lP[:, k]))
                    for i in range(len(pxc)) for k in range(len(pxc))))
    I, L = info_I_L(pxc, P)
    check("C1_reset_identity_I_plus_L", worst < 5e-3 and abs(EKL - (I + L)) < 1e-9,
          "E KL = I + L exactly (%s vs %s); Gaussian copy I+L = v/sigma^2 (max rel err %s)"
          % (fmt(EKL), fmt(I + L), fmt(worst)))

    # C2. kappa = inf_c E ln (X-c)^2: Gaussian at c=0 equals ln v - gamma - ln 2;
    #     Cauchy E ln X^2 = 2 ln s.
    def elog(c, logpdf):
        f = lambda t: math.log((t - c) ** 2) * math.exp(logpdf(t))
        pts = [c]
        return integrate.quad(f, -np.inf, c, limit=400)[0] + integrate.quad(f, c, np.inf, limit=400)[0]
    gl = lambda t: -0.5 * t * t - 0.5 * math.log(2 * math.pi)
    vals = [elog(c, gl) for c in (0.0, 0.3, 1.0, 2.0)]
    cl = lambda t: -math.log(math.pi * (1 + t * t))
    kc = elog(0.0, cl)
    check("C2_log_moment_kappa", abs(vals[0] - KAPPA_GAUSS_OFFSET) < 1e-7 and vals == sorted(vals) and abs(kc) < 1e-7,
          "Gaussian E ln(X-c)^2 at c=0,0.3,1,2: %s (min at 0 = -gamma-ln2 = %s); Cauchy(s=1) E ln X^2 = %s"
          % (", ".join(fmt(t) for t in vals), fmt(KAPPA_GAUSS_OFFSET), fmt(kc)))

    # C3. The floor I+L >= (3/2) ln(v/eps) - gamma - ln 2 on many channel families.
    fams = []
    for sig in (0.05, 0.1, 0.3, 0.7):
        fams.append(("gauss s=%g" % sig, gauss_channel(x, m, x, sig)))
    for nu_c in (1.0, 2.0, 4.0):
        for sc in (0.05, 0.2):
            G = np.exp(student_logpdf((m[:, None] - x[None, :]), nu_c, sc))
            fams.append(("t%g s=%g" % (nu_c, sc), G / G.sum(axis=0, keepdims=True)))
    prior_m = np.exp(-0.5 * m * m / v)
    prior_m /= prior_m.sum()
    for sig in (0.05, 0.2):
        for delta in (1e-3, 1e-2, 0.1):
            core = gauss_channel(x, m, x, sig)
            fams.append(("core+floor s=%g d=%g" % (sig, delta), (1 - delta) * core + delta * prior_m[:, None]))
    lap = np.exp(-np.abs(m[:, None] - x[None, :]) / 0.1)
    fams.append(("laplace b=0.1", lap / lap.sum(axis=0, keepdims=True)))
    ok_all = True
    worst = math.inf
    lines = []
    for name, P in fams:
        I, L = info_I_L(px, P)
        eps = grid_channel_mse(px, x, P)
        fl = 1.5 * math.log(v / eps) + KAPPA_GAUSS_OFFSET
        okI = I >= 0.5 * math.log(v / eps) - 2e-3
        okL = L >= math.log(v / eps) + KAPPA_GAUSS_OFFSET - 2e-3
        ok_all = ok_all and okI and okL and (I + L >= fl - 3e-3)
        worst = min(worst, (I + L) - fl)
        lines.append((name, eps, I + L, fl))
    check("C3_reset_floor_on_channel_families", ok_all,
          "%d channels (Gaussian, Student-t, Laplace, core+floor): I >= R(eps), L >= ln(v/eps)-gamma-ln2, I+L >= floor; min excess %s nats"
          % (len(fams), fmt(worst)))
    g = [t for t in lines if t[0] == "gauss s=0.05"][0]
    cf = [t for t in lines if t[0] == "core+floor s=0.05 d=0.001"][0]
    check("C3b_light_tailed_copy_far_above_floor", g[2] > 10 * g[3] and cf[2] < 2 * cf[3] + 4,
          "Gaussian copy s=0.05: eps=%s, I+L=%s vs floor %s; core+floor s=0.05 d=1e-3: eps=%s, I+L=%s vs floor %s"
          % (fmt(g[1]), fmt(g[2]), fmt(g[3]), fmt(cf[1]), fmt(cf[2]), fmt(cf[3])))

    # C4. Near-attaining design: core+floor with sigma^2 = eps/2, delta = eps/(4v).
    #     Proved: I+L <= (3/2) ln(v/eps) + (5/2) ln 2 + eps/(4v); MSE(m) <= eps.
    ok = True
    gaps = []
    xs2 = np.linspace(-9, 9, 1801)
    px2 = np.exp(-0.5 * xs2 ** 2 / v)
    px2 /= px2.sum()
    m2 = np.linspace(-12, 12, 6001)
    pm2 = np.exp(-0.5 * m2 ** 2 / v)
    pm2 /= pm2.sum()
    for target in (0.3, 0.1, 0.03, 0.01, 0.003):
        sig = math.sqrt(target / 2)
        delta = target / (4 * v)
        P = (1 - delta) * gauss_channel(xs2, m2, xs2, sig) + delta * pm2[:, None]
        I, L = info_I_L(px2, P)
        joint = P * px2[None, :]
        mse_m = float(np.sum(joint * (m2[:, None] - xs2[None, :]) ** 2))
        upper = 1.5 * math.log(v / target) + 2.5 * math.log(2) + target / (4 * v)
        floor = 1.5 * math.log(v / target) + KAPPA_GAUSS_OFFSET
        ok = ok and (I + L <= upper + 2e-3) and (mse_m <= target * (1 + 1e-3)) and (I + L >= floor - 2e-3)
        gaps.append((I + L) - floor)
    check("C4_core_plus_floor_within_constant_of_floor", ok and all(gp <= 2.5 * math.log(2) - KAPPA_GAUSS_OFFSET + t / 4 for gp, t in zip(gaps, (0.3, 0.1, 0.03, 0.01, 0.003))),
          "targets eps=0.3..0.003: MSE<=eps, I+L <= (3/2)ln(v/eps)+(5/2)ln2+eps/4v; gap to floor %s nats (proved <= 3.003+eps/4v)"
          % ", ".join(fmt(t) for t in gaps))

    # C5. Exact bipartite chain: reset world (rate lam, landing law pi), memory relaxing at
    #     rate gamma in the landscape E = -ln p_x(m). Q >= I_alt = world-side destruction,
    #     and Q -> lam * E KL as gamma/lam grows.
    lam = 1.0
    xr = np.linspace(-3.5, 3.5, 29)
    pir = np.exp(-0.5 * xr ** 2)
    pir /= pir.sum()
    mr = np.linspace(-5, 5, 61)
    sigr, delr = 0.35, 0.05
    core = np.exp(-0.5 * ((mr[:, None] - xr[None, :]) / sigr) ** 2)
    core /= core.sum(axis=0, keepdims=True)
    pmr = np.exp(-0.5 * mr ** 2)
    pmr /= pmr.sum()
    Pch = (1 - delr) * core + delr * pmr[:, None]
    Een = -np.log(Pch)  # E[m, x]
    lP = np.log(Pch)
    EKL_target = float(sum(pir[i] * pir[k] * np.sum(Pch[:, i] * (lP[:, i] - lP[:, k]))
                           for i in range(len(xr)) for k in range(len(xr))))
    nxr, nmr = len(xr), len(mr)
    res = {}
    for gam in (3.0, 30.0, 300.0):
        n = nxr * nmr
        Qd = np.zeros((n, n))
        for i in range(nxr):
            for k in range(nxr):
                if k != i:
                    for j in range(nmr):
                        Qd[i * nmr + j, k * nmr + j] += lam * pir[k]
            # memory: all-to-all LDB rates gamma/nm * sqrt(p(m')/p(m))
            R = gam / nmr * np.sqrt(Pch[:, i][None, :] / Pch[:, i][:, None])
            np.fill_diagonal(R, 0.0)
            Qd[i * nmr:(i + 1) * nmr, i * nmr:(i + 1) * nmr] += R
        np.fill_diagonal(Qd, -Qd.sum(axis=1))
        A = Qd.T.copy()
        A[0, :] = 1.0
        b = np.zeros(n)
        b[0] = 1.0
        pst = np.linalg.solve(A, b).reshape(nxr, nmr)
        pxx = pst.sum(axis=1)
        cond = pst / pxx[:, None]
        lc = np.log(cond)
        heat = ialt = 0.0
        for i in range(nxr):
            R = gam / nmr * np.sqrt(Pch[:, i][None, :] / Pch[:, i][:, None])
            np.fill_diagonal(R, 0.0)
            fl = pst[i][:, None] * R
            heat += float(np.sum(fl * (Een[:, i][:, None] - Een[:, i][None, :])))
            ialt += float(np.sum(fl * (lc[i][None, :] - lc[i][:, None])))
        destr = float(sum(pxx[i] * lam * pir[k] * np.sum(cond[i] * (lc[i] - lc[k]))
                          for i in range(nxr) for k in range(nxr) if k != i))
        res[gam] = (heat, ialt, destr)
    ok_id = all(abs(r[1] - r[2]) < 1e-9 * max(1, abs(r[1])) and r[0] >= r[1] - 1e-12 for r in res.values())
    ratios = [res[g][0] / (lam * EKL_target) for g in (3.0, 30.0, 300.0)]
    check("C5_reset_chain_identity_and_JP_heat", ok_id,
          "exact steady state: I_alt = lam * sum pi pi' KL (world-side), Q >= I_alt, gamma=3,30,300")
    check("C5b_fast_relaxation_heat_to_lam_EKL", abs(ratios[2] - 1) < 0.02 and abs(ratios[2] - 1) < abs(ratios[0] - 1),
          "Q/(lam E KL) = %s at gamma/lam = 3, 30, 300" % ", ".join(fmt(t) for t in ratios))

    # C6. Ruin floor: L >= kl(1 - beta_b || eta) for the event |X - xhat(M)| > b.
    def kl_bin(p, q):
        return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))
    ok = True
    cnt = 0
    for name, P in fams:
        joint = P * px[None, :]
        pmm = joint.sum(axis=1)
        keep = pmm > 0
        xhat = np.zeros(len(m))
        xhat[keep] = (joint[keep] @ x) / pmm[keep]
        _, L = info_I_L(px, P)
        for b in (0.1, 0.3, 1.0):
            beta = math.erf(b / math.sqrt(2 * v))
            eta = float(np.sum(joint * (np.abs(x[None, :] - xhat[:, None]) > b)))
            if 0 < eta < 1 - beta:
                cnt += 1
                ok = ok and L >= kl_bin(1 - beta, eta) - 2e-3
    check("C6_ruin_cap_floor", ok and cnt > 10,
          "%d (channel, margin) cases: lautum L >= kl(1-beta_b || P(ruin))" % cnt)

    # C7. Heavy-tailed shocks: Cauchy-location KL closed form ln(1+z^2/(4 s^2)) and a finite
    #     learning rate under an alpha-stable jump measure, where a Gaussian copy diverges.
    worst = 0.0
    for z in (0.1, 1.0, 5.0, 40.0):
        s = 0.3
        f = lambda t: (1 / (math.pi * s * (1 + (t / s) ** 2))) * (math.log1p(((t - z) / s) ** 2) - math.log1p((t / s) ** 2))
        val = integrate.quad(f, -np.inf, np.inf, points=None, limit=500)[0]
        worst = max(worst, abs(val - math.log1p(z * z / (4 * s * s))))
    alpha, s = 1.5, 0.3
    fin = 2 * integrate.quad(lambda z: math.log1p(z * z / (4 * s * s)) * z ** (-1 - alpha), 0, np.inf, limit=500)[0]
    gauss_part = 2 * integrate.quad(lambda z: z * z / (2 * s * s) * z ** (-1 - alpha), 0, 1e6, limit=500)[0]
    check("C7_heavy_tailed_shocks_need_heavy_tailed_memory", worst < 1e-7 and math.isfinite(fin) and gauss_part > 1e3 * fin,
          "Cauchy KL closed form (max err %s); alpha=1.5: Cauchy-copy rate %s vs Gaussian-copy rate >%s (diverges with cutoff)"
          % (fmt(worst), fmt(fin), fmt(gauss_part)))

    # C8. Local shocks: Bretagnolle-Huber per-pair floor KL(p_x||p_x+z) >= ln(z^2/(4(e_x+e_x+z))).
    ok = True
    cnt = 0
    for name, P in fams:
        joint = P * px[None, :]
        pmm = joint.sum(axis=1)
        keep = pmm > 0
        xhat = np.zeros(len(m))
        xhat[keep] = (joint[keep] @ x) / pmm[keep]
        e = np.array([np.sum(P[:, i] * (xhat - x[i]) ** 2) for i in range(0, len(x), 40)])
        ii = list(range(0, len(x), 40))
        lP = np.log(np.maximum(P, 1e-300))
        for a_ in range(len(ii)):
            for b_ in range(len(ii)):
                if a_ != b_:
                    i, k = ii[a_], ii[b_]
                    z = x[k] - x[i]
                    kl = float(np.sum(P[:, i] * (lP[:, i] - lP[:, k])))
                    bound = math.log(z * z / (4 * (e[a_] + e[b_])))
                    cnt += 1
                    ok = ok and kl >= bound - 1e-6
    check("C8_bretagnolle_huber_per_shock_floor", ok,
          "%d (channel, pair) cases: KL(p_x||p_x+z) >= ln(z^2/(4(e(x)+e(x+z))))" % cnt)

    # C9. Cost minimum in a Gaussian reset world (kT=1): floor and design bracket,
    #     J* = (3/2) lam ln(v w/lam) + O(lam); eps* = (3/2) kT lam / w.
    lam, v = 1.0, 1.0
    rows = []
    for w in (10.0, 100.0, 1000.0, 1e4):
        e_lo = 1.5 * lam / w
        lo = lam * (1.5 * math.log(v / e_lo) + KAPPA_GAUSS_OFFSET) + w * e_lo
        e_up = 1.5 * lam / (w + lam / (4 * v))
        up = lam * (1.5 * math.log(v / e_up) + 2.5 * math.log(2) + e_up / (4 * v)) + w * e_up
        lead = 1.5 * lam * math.log(v * w / lam)
        rows.append((w, lo - lead, up - lead))
    c_lo = 1.5 - 1.5 * math.log(1.5) + KAPPA_GAUSS_OFFSET
    ok = all(abs(r[1] - c_lo) < 1e-12 and r[2] <= 2.7 for r in rows)
    check("C9_reset_cost_minimum_bracket", ok,
          "J* - (3/2)lam ln(vw/lam) in [%s, %s] at w=10..1e4 (log growth in the stake; OU grows as sqrt(w))"
          % (fmt(min(r[1] for r in rows)), fmt(max(r[2] for r in rows))))


def main():
    np.set_printoptions(precision=6)
    check_sentence()
    section_A()
    section_B()
    section_C()
    if checks_failed:
        print("FAILS %d: %s" % (len(checks_failed), ", ".join(checks_failed)))
        sys.exit(1)
    print("FAILS 0")
    print("ALL NON-GAUSSIAN-FLOOR CHECKS PASS")


if __name__ == "__main__":
    main()
