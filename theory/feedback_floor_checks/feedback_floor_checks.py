#!/usr/bin/env python3
"""Checks for theory/FEEDBACK_FLOOR_2026-11-23.md (T61).

Run from the repo root:
  nice -n 19 python3 theory/feedback_floor_checks/feedback_floor_checks.py

These checks are code identities and in-model evaluations on linear
Langevin loops and finite-state bipartite chains. They are not evidence
about a real system. A machinery failure sets a nonzero exit code.
"""
from __future__ import annotations

import math
import sys

import numpy as np

checks_failed = []


def check(name, ok, detail):
    print("CHECK %s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        checks_failed.append(name)


def close(a, b, tol=1e-12):
    return abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b)))


def L(eps):
    if eps <= 0.0 or eps >= 0.5:
        return math.inf if eps <= 0.0 else 0.0
    return (1.0 - 2.0 * eps) * math.log((1.0 - eps) / eps)


# ---- LG-b formulas, same conventions as T47 ----

def closed_moments(a, b, K, g, c, D, Dm):
    den = g * (a + g) * (K * b * c + a)
    v = (D * K * b * c * g + D * a * g + D * g * g + Dm * K * K * b * b) / den
    s = (D * c * g * g - Dm * K * a * b) / den
    m = (D * c * c * g * g + Dm * K * b * c * g + Dm * a * a + Dm * a * g) / den
    return v, s, m


def closed_rates(a, b, K, g, c, D, Dm):
    comb = D * c * g + Dm * K * b
    sr_x = b * K * comb / (D * (a + g))
    sr_m = c * g * comb / (Dm * (a + g))
    i_m = comb * (D * c * g * g - Dm * K * a * b) / (comb ** 2 + D * Dm * (a + g) ** 2)
    return sr_x, sr_m, i_m


def lyapunov_moments(a, b, K, g, c, D, Dm):
    mat = np.array(
        [
            [a, b * K, 0.0],
            [g * c, -(a + g), -b * K],
            [0.0, g * c, -g],
        ],
        dtype=float,
    )
    rhs = np.array([D, 0.0, -Dm], dtype=float)
    v, s, m = np.linalg.solve(mat, rhs)
    return float(v), float(s), float(m)


def kalman_params(a, D, r, gain):
    """Compensated Kalman-Bucy filter of the LG-b plant, gain g on M.

    Plant: dX = -a X dt - gain M dt + sqrt(2D) dW_X.
    Observation: dY = X dt + sqrt(r) dV.
    Filter uses the known control. Memory Einstein temperature is D_M.
    """
    disc = (a * r) ** 2 + 2.0 * D * r
    p = -a * r + math.sqrt(disc)
    kf = p / r
    theta = D / a
    v = p + a * (theta - p) / (a + gain)
    dm = D - a * p
    gamma = a + gain + kf
    c = kf / gamma
    sr_x, sr_m, i_m = closed_rates(a, 1.0, gain, gamma, c, D, dm)
    q_x = D * sr_x
    q_m = dm * sr_m
    L_exog = a * (theta / p - 1.0)
    q_x_display = gain * (D * kf + dm * gain) / (2.0 * a + gain + kf)
    q_m_display = 2.0 * dm * L_exog
    return dict(
        p=p, kf=kf, theta=theta, v=v, dm=dm, gamma=gamma, c=c,
        sr_x=sr_x, sr_m=sr_m, i_m=i_m, q_x=q_x, q_m=q_m,
        q_tot=q_x + q_m, L=L_exog, q_x_display=q_x_display,
        q_m_display=q_m_display,
    )


# ---- finite-state bipartite chains ----

def stationary_from_Q(Q):
    n = Q.shape[0]
    A = Q.T.copy()
    A[-1, :] = 1.0
    b = np.zeros(n)
    b[-1] = 1.0
    pi = np.linalg.solve(A, b)
    pi = np.clip(np.real(pi), 0.0, None)
    return pi / pi.sum()


def joint_Q(Wx, wm, nX=2, nM=2):
    """Wx[m, x, xp] world rates; wm[x, m, mp] memory rates."""
    N = nX * nM
    Q = np.zeros((N, N))
    for x in range(nX):
        for m in range(nM):
            i = x * nM + m
            for xp in range(nX):
                if xp == x:
                    continue
                Q[i, xp * nM + m] += Wx[m, x, xp]
            for mp in range(nM):
                if mp == m:
                    continue
                Q[i, x * nM + mp] += wm[x, m, mp]
    np.fill_diagonal(Q, 0.0)
    np.fill_diagonal(Q, -Q.sum(axis=1))
    return Q


def analyze_jump(Wx, wm, E_mem, V_world, nX=2, nM=2):
    Q = joint_Q(Wx, wm, nX, nM)
    pi = stationary_from_Q(Q)
    p = pi.reshape(nX, nM)
    pX = p.sum(axis=1)
    pM = p.sum(axis=0)
    I_M = 0.0
    Q_M = 0.0
    W_ctrl = 0.0
    for x in range(nX):
        for m in range(nM):
            for mp in range(nM):
                if mp == m:
                    continue
                flux = p[x, m] * wm[x, m, mp]
                if pX[x] <= 0.0:
                    continue
                pm_x = p[x, m] / pX[x]
                pmp_x = p[x, mp] / pX[x]
                if flux > 0.0 and pm_x > 0.0 and pmp_x > 0.0:
                    I_M += flux * math.log(pmp_x / pm_x)
                Q_M += flux * (E_mem[x, m] - E_mem[x, mp])
                W_ctrl += flux * (V_world[x, mp] - V_world[x, m])
    I_X = 0.0
    Q_X = 0.0
    for m in range(nM):
        for x in range(nX):
            for xp in range(nX):
                if xp == x:
                    continue
                flux = p[x, m] * Wx[m, x, xp]
                if pM[m] <= 0.0:
                    continue
                px_m = p[x, m] / pM[m]
                pxp_m = p[xp, m] / pM[m]
                if flux > 0.0 and px_m > 0.0 and pxp_m > 0.0:
                    I_X += flux * math.log(pxp_m / px_m)
                Q_X += flux * (V_world[x, m] - V_world[xp, m])
    eps_track = 0.0
    for m in range(nM):
        if pM[m] <= 0.0:
            continue
        eps_track += pM[m] - p[:, m].max()
    eps_task = float(pX[1]) if nX == 2 else float(1.0 - pX.max())
    Wbar = np.zeros((nX, nX))
    for x in range(nX):
        if pX[x] <= 0.0:
            continue
        for xp in range(nX):
            if xp == x:
                continue
            Wbar[x, xp] = sum(p[x, m] * Wx[m, x, xp] for m in range(nM)) / pX[x]
    I_t60 = 0.0
    for x in range(nX):
        for xp in range(nX):
            if xp == x or Wbar[x, xp] <= 0.0 or pX[x] <= 0.0 or pX[xp] <= 0.0:
                continue
            pMx = p[x, :] / pX[x]
            pMxp = p[xp, :] / pX[xp]
            kl = 0.0
            for m in range(nM):
                if pMx[m] > 1e-15:
                    kl += pMx[m] * math.log(pMx[m] / max(pMxp[m], 1e-15))
            I_t60 += pX[x] * Wbar[x, xp] * kl
    return dict(
        I_M=I_M, I_X=I_X, sumI=I_M + I_X, Q_M=Q_M, Q_X=Q_X,
        W_ctrl=W_ctrl, eps_track=eps_track, eps_task=eps_task,
        I_t60=I_t60, pX=pX, p=p,
    )


def make_memory_ldb(h, nu, nX=2, nM=2):
    E = np.zeros((nX, nM))
    for x in range(nX):
        for m in range(nM):
            E[x, m] = -h if x == m else 0.0
    wm = np.zeros((nX, nM, nM))
    for x in range(nX):
        for m in range(nM):
            for mp in range(nM):
                if mp == m:
                    continue
                wm[x, m, mp] = nu * math.exp(-0.5 * (E[x, mp] - E[x, m]))
    return wm, E


def make_world_conservative(delta, r, mode="enslave"):
    nX = nM = 2
    V = np.zeros((nX, nM))
    for x in range(nX):
        for m in range(nM):
            if mode == "enslave":
                V[x, m] = -delta if x == m else 0.0
            elif mode == "openloop":
                V[x, m] = delta * x
            elif mode == "regulate":
                V[x, m] = delta * x * m
            else:
                raise ValueError(mode)
    Wx = np.zeros((nM, nX, nX))
    for m in range(nM):
        for x in range(nX):
            for xp in range(nX):
                if xp == x:
                    continue
                Wx[m, x, xp] = r * math.exp(-0.5 * (V[xp, m] - V[x, m]))
    return Wx, V


def make_joint_eq(Etot, nu, r):
    nX = nM = 2
    wm = np.zeros((nX, nM, nM))
    Wx = np.zeros((nM, nX, nX))
    for x in range(nX):
        for m in range(nM):
            for mp in range(nM):
                if mp == m:
                    continue
                wm[x, m, mp] = nu * math.exp(-0.5 * (Etot[x, mp] - Etot[x, m]))
            for xp in range(nX):
                if xp == x:
                    continue
                Wx[m, x, xp] = r * math.exp(-0.5 * (Etot[xp, m] - Etot[x, m]))
    return Wx, wm


def main():
    # 1. LG-b Lyapunov matches the closed moments; T47 rates match the
    # energy-flow definition at five points, including a sign change of I_M.
    points = [
        (1.0, 1.0, 0.0, 2.0, 1.0, 1.0, 1.0),
        (1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0),
        (1.0, 1.0, 4.0, 2.0, 1.0, 1.0, 1.0),
        (1.0, 1.0, 8.0, 2.0, 1.0, 1.0, 1.0),
        (0.7, 1.3, 2.5, 1.1, 0.8, 1.2, 0.6),
    ]
    lyap_ok = True
    sign_ok = True
    worst_lyap = 0.0
    i_vals = []
    for a, b, K, g, c, D, Dm in points:
        v, s, m = closed_moments(a, b, K, g, c, D, Dm)
        v2, s2, m2 = lyapunov_moments(a, b, K, g, c, D, Dm)
        worst_lyap = max(worst_lyap, abs(v - v2), abs(s - s2), abs(m - m2))
        sr_x, sr_m, i_m = closed_rates(a, b, K, g, c, D, Dm)
        i_vals.append(i_m)
        # Threshold from the numerator of I_M.
        thresh = D * c * g * g / (Dm * a * b) if (Dm * a * b) > 0 else math.inf
        if K > thresh + 1e-12 and i_m >= -1e-15:
            sign_ok = False
        if K < thresh - 1e-12 and i_m <= 1e-15 and K > 0:
            # at K=0, I_M should be positive for a tracker
            if K != 0.0:
                sign_ok = False
        # Sr_M - I_M >= 0 (EQ-heat / Lemma D)
        if sr_m - i_m < -1e-12:
            sign_ok = False
    check(
        "lgb_lyapunov_matches_closed_moments",
        worst_lyap < 1e-12,
        "worst abs moment residual=%.3e" % worst_lyap,
    )
    # Explicit sign change at a=b=D=c=Dm=1, gamma=2: threshold K=4.
    _sx, _sm, i_at_4 = closed_rates(1, 1, 4, 2, 1, 1, 1)
    _sx, _sm, i_at_8 = closed_rates(1, 1, 8, 2, 1, 1, 1)
    _sx, _sm, i_at_0 = closed_rates(1, 1, 0, 2, 1, 1, 1)
    check(
        "lgb_learning_rate_changes_sign",
        sign_ok and close(i_at_4, 0.0) and i_at_8 < 0.0 and i_at_0 > 0.0,
        "I_M(K=0)=%.12f; I_M(K=4)=%.12f; I_M(K=8)=%.12f" % (i_at_0, i_at_4, i_at_8),
    )
    # Frozen decimals used in the note, a=b=D=c=Dm=1, gamma=2, K=0 and K=8.
    v0, s0, m0 = closed_moments(1, 1, 0, 2, 1, 1, 1)
    v8, s8, m8 = closed_moments(1, 1, 8, 2, 1, 1, 1)
    sx0, sm0, _ = closed_rates(1, 1, 0, 2, 1, 1, 1)
    sx8, sm8, _ = closed_rates(1, 1, 8, 2, 1, 1, 1)
    check(
        "lgb_frozen_heats_and_variance",
        close(v0, 1.0) and close(1.0 * sm0, 4.0 / 3.0) and close(1.0 * sx0, 0.0)
        and close(v8, 43.0 / 27.0) and sm8 > 0.0 and sx8 > 0.0 and i_at_8 < 0.0,
        "v(0)=%.12f Q_M(0)=%.12f Q_X(0)=%.12f; v(8)=%.12f Q_M(8)=%.12f Q_X(8)=%.12f I_M(8)=%.12f"
        % (v0, sm0, sx0, v8, sm8, 1.0 * sx8, i_at_8),
    )

    # 2. Kalman-Bucy identification: I_M and Q_M independent of gain;
    # I_M equals the exogenous formula; Q_M = 2 D_M I_M; Q_X matches the display;
    # moments match LG-b Lyapunov; v decreases toward p and cannot go below p.
    a = D = 1.0
    r = 0.5
    h0 = kalman_params(a, D, r, 0.0)
    p_exact = (math.sqrt(5.0) - 1.0) / 2.0
    check(
        "kalman_error_at_r_half_is_golden_conjugate",
        close(h0["p"], p_exact),
        "p=%.12f; (sqrt(5)-1)/2=%.12f" % (h0["p"], p_exact),
    )
    gain_ok = True
    details = []
    for gain in [0.0, 0.414213562373, 1.0, 4.0, 16.0, 64.0]:
        h = kalman_params(a, D, r, gain)
        v2, s2, m2 = lyapunov_moments(a, 1.0, gain, h["gamma"], h["c"], D, h["dm"])
        if not close(h["i_m"], h0["L"]):
            gain_ok = False
        if not close(h["q_m"], h0["q_m"]):
            gain_ok = False
        if not close(h["q_m"], h["q_m_display"]):
            gain_ok = False
        if not close(h["q_x"], h["q_x_display"]):
            gain_ok = False
        if not close(h["v"], v2) or not close(h["v"] - h["p"], m2, tol=1e-11):
            gain_ok = False
        if h["v"] + 1e-12 < h["p"]:
            gain_ok = False
        if gain > 0.0 and h["v"] >= h0["v"] - 1e-15:
            gain_ok = False
        details.append((gain, h["v"], h["i_m"], h["q_m"], h["q_x"]))
    # Independence also at a second observation noise, and off the unit point.
    for a2, D2, r2 in [(1.0, 1.0, 2.0), (0.5, 1.5, 0.8), (2.0, 1.0, 1.0)]:
        base = kalman_params(a2, D2, r2, 0.0)
        for gain in [0.0, 1.0, 5.0]:
            h = kalman_params(a2, D2, r2, gain)
            if not close(h["i_m"], base["L"]) or not close(h["q_m"], base["q_m_display"]):
                gain_ok = False
            if not close(h["q_x"], h["q_x_display"]):
                gain_ok = False
    check(
        "kalman_heat_and_learning_rate_independent_of_gain",
        gain_ok and close(h0["q_m"], 2.0 * h0["dm"] * h0["L"]),
        "r=1/2: p=%.12f I_M=%.12f Q_M=%.12f D_M=%.12f; Q_X(g=1)=%.12f Q_X(g=4)=%.12f"
        % (h0["p"], h0["i_m"], h0["q_m"], h0["dm"],
           kalman_params(1, 1, 0.5, 1)["q_x"],
           kalman_params(1, 1, 0.5, 4)["q_x"]),
    )
    # As g -> infinity, v -> p and Q_X diverges, Q_M stays put.
    h64 = kalman_params(1, 1, 0.5, 64.0)
    h256 = kalman_params(1, 1, 0.5, 256.0)
    check(
        "kalman_world_heat_diverges_as_variance_approaches_p",
        h256["v"] - h256["p"] < h64["v"] - h64["p"]
        and h256["q_x"] > h64["q_x"] > 20.0
        and close(h256["q_m"], h0["q_m"]),
        "g=64: v-p=%.12f Q_X=%.12f; g=256: v-p=%.12f Q_X=%.12f"
        % (h64["v"] - h64["p"], h64["q_x"], h256["v"] - h256["p"], h256["q_x"]),
    )

    # 3. Necessary sensing bound: to hold v <= v* one needs p <= v*, hence
    # I_M >= a(theta/v* - 1). Equality is not attainable at finite gain.
    nec_ok = True
    for vstar in [0.9, 0.7, 0.5]:
        # Any Kalman design with v <= v* must have p <= v, so I_M >= a(1/vstar-1) at a=D=1.
        floor = 1.0 * (1.0 / vstar - 1.0)
        for r in [0.05, 0.2, 0.5, 1.0, 2.0]:
            p = kalman_params(1, 1, r, 0.0)["p"]
            if p > vstar:
                continue
            g_need = (1.0 - p) / (vstar - p) - 1.0
            h = kalman_params(1, 1, r, max(g_need, 0.0))
            if h["v"] > vstar + 1e-10:
                nec_ok = False
            if h["i_m"] + 1e-12 < floor:
                nec_ok = False
            if h["p"] > vstar + 1e-12:
                nec_ok = False
    check(
        "kalman_task_variance_needs_estimation_error_below_it",
        nec_ok,
        "I_M >= a(theta/v*-1) whenever v<=v* in this family; v cannot undercut p",
    )

    # 4. Cost J = Q_M + Q_X + w v on the Kalman family, a=D=1.
    # Blind design (no sensor, no gain) has J = w. A cheap observation at g=0
    # cannot beat the blind line, because v stays at theta and Q_M > 0.
    # At w=8 a closed loop at a named point is cheaper than the blind line.
    # At w=1 every named loop in this grid is dearer.
    def J_of(w, r, gain):
        if gain == 0.0 and math.isinf(r):
            return w * 1.0, dict(q_m=0.0, q_x=0.0, v=1.0, i_m=0.0, p=1.0)
        h = kalman_params(1.0, 1.0, r, gain)
        return h["q_m"] + h["q_x"] + w * h["v"], h

    # Named point used in the note: r=1/2, g=1, w=8 and w=1.
    J8, h8p = J_of(8.0, 0.5, 1.0)
    J1, h1p = J_of(1.0, 0.5, 1.0)
    check(
        "kalman_cost_beats_blind_at_stake_eight_not_one",
        J8 < 8.0 and J1 > 1.0,
        "r=1/2 g=1: J(w=8)=%.12f < 8; J(w=1)=%.12f > 1; v=%.12f Q_M=%.12f Q_X=%.12f"
        % (J8, J1, h8p["v"], h8p["q_m"], h8p["q_x"]),
    )

    # 5. Jump processes: steady-state flows sum to zero; JP-heat Q_M >= I_M
    # under LDB on the memory energy; T60 identity holds when W is exogenous
    # and fails when it depends on M; joint equilibrium has vanishing heats.
    def cases_ok():
        return True

    # 5a. Exogenous telegraph, memory LDB: T59 / T60 identity and JP-heat.
    t59_ok = True
    worst_jp = 0.0
    for h, nu in [(0.5, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 2.0)]:
        wm, E = make_memory_ldb(h, nu)
        Wx, V = make_world_conservative(0.0, 1.0, "openloop")
        out = analyze_jump(Wx, wm, E, V)
        floor = L(out["eps_track"])
        if not close(out["I_M"], floor, tol=1e-10):
            t59_ok = False
        if not close(out["I_M"], out["I_t60"], tol=1e-10):
            t59_ok = False
        if not close(out["sumI"], 0.0, tol=1e-12):
            t59_ok = False
        if out["Q_M"] + 1e-12 < out["I_M"]:
            t59_ok = False
        worst_jp = max(worst_jp, out["Q_M"] - out["I_M"])
    check(
        "exogenous_telegraph_recovers_t59_and_t60",
        t59_ok,
        "I_M = r L(eps) = I_t60; Q_M - I_M >= 0 (smallest slack on this grid is recorded by JP-heat checks below)",
    )

    # 5b. Joint equilibrium, one energy: all flows and heats vanish.
    eq_ok = True
    eq_details = []
    for desc, Etot, task_expected in [
        ("tilt d=2", np.array([[0.0, 0.0], [2.0, 2.0]]), 1.0 / (1.0 + math.exp(2.0))),
        ("copy h=2", np.array([[-2.0, 0.0], [0.0, -2.0]]), 0.5),
        ("enslave d=2", np.array([[-2.0, 0.0], [0.0, -2.0]]), 0.5),
    ]:
        Wx, wm = make_joint_eq(Etot, 1.0, 1.0)
        out = analyze_jump(Wx, wm, Etot, Etot)
        if max(abs(out["I_M"]), abs(out["I_X"]), abs(out["Q_M"]), abs(out["Q_X"]), abs(out["W_ctrl"])) > 1e-10:
            eq_ok = False
        if not close(out["eps_task"], task_expected, tol=1e-12):
            eq_ok = False
        eq_details.append((desc, out["eps_task"], out["I_M"], out["Q_M"]))
    # Open-loop tilt of the world alone, unused memory, same Boltzmann task error.
    wm0, E0 = make_memory_ldb(0.0, 1.0)
    Wx0, V0 = make_world_conservative(2.0, 1.0, "openloop")
    out0 = analyze_jump(Wx0, wm0, E0, V0)
    boltz = 1.0 / (1.0 + math.exp(2.0))
    check(
        "joint_equilibrium_and_openloop_tilt_have_zero_ongoing_heat",
        eq_ok and close(out0["Q_M"], 0.0) and close(out0["Q_X"], 0.0)
        and close(out0["I_M"], 0.0) and close(out0["eps_task"], boltz),
        "open-loop tilt d=2: task=%.12f = 1/(1+e^2); I_M=Q_M=Q_X=0; joint equilibria also vanish"
        % out0["eps_task"],
    )

    # 5c. Feedback breaks the T60 identity; I_M can fall below r L(eps) and change sign.
    # Enslavement with different potentials (memory copy energy vs world coupling).
    wm, E = make_memory_ldb(1.0, 1.0)
    Wx, V = make_world_conservative(3.0, 1.0, "enslave")
    out_en = analyze_jump(Wx, wm, E, V)
    floor_en = L(out_en["eps_track"])
    # A sluggish memory with strong enslavement: I_M < 0, JP-heat still holds.
    wm_s, E_s = make_memory_ldb(0.2, 0.2)
    Wx_s, V_s = make_world_conservative(4.0, 2.0, "enslave")
    out_s = analyze_jump(Wx_s, wm_s, E_s, V_s)
    # Regulation (asymmetric coupling) with a mismatch of potentials.
    wm_r, E_r = make_memory_ldb(1.0, 1.0)
    Wx_r, V_r = make_world_conservative(2.0, 1.0, "regulate")
    out_r = analyze_jump(Wx_r, wm_r, E_r, V_r)
    check(
        "feedback_breaks_t60_identity",
        abs(out_en["I_M"] - out_en["I_t60"]) > 0.5
        and abs(out_s["I_M"] - out_s["I_t60"]) > 0.1,
        "enslave h=1 d=3: I_M=%.12f I_t60=%.12f; sluggish: I_M=%.12f I_t60=%.12f"
        % (out_en["I_M"], out_en["I_t60"], out_s["I_M"], out_s["I_t60"]),
    )
    check(
        "acting_can_reduce_or_reverse_the_learning_rate",
        out_en["I_M"] < floor_en - 0.5 and out_s["I_M"] < 0.0 and out_r["I_M"] < 0.0,
        "enslave h=1 d=3: I_M=%.12f < r L(eps)=%.12f at eps=%.12f; sluggish I_M=%.12f; regulate I_M=%.12f"
        % (out_en["I_M"], floor_en, out_en["eps_track"], out_s["I_M"], out_r["I_M"]),
    )
    jp_ok = (
        out_en["Q_M"] + 1e-12 >= out_en["I_M"]
        and out_s["Q_M"] + 1e-12 >= out_s["I_M"]
        and out_r["Q_M"] + 1e-12 >= out_r["I_M"]
        and close(out_en["sumI"], 0.0, tol=1e-12)
        and close(out_s["sumI"], 0.0, tol=1e-12)
        and close(out_r["sumI"], 0.0, tol=1e-12)
    )
    check(
        "jp_heat_holds_and_flows_sum_to_zero_under_feedback",
        jp_ok,
        "enslave: Q_M=%.12f I_M=%.12f; sluggish: Q_M=%.12f I_M=%.12f; regulate: Q_M=%.12f I_M=%.12f"
        % (out_en["Q_M"], out_en["I_M"], out_s["Q_M"], out_s["I_M"], out_r["Q_M"], out_r["I_M"]),
    )

    # 5d. Adversarial relabelling: a memory with the opposite copy energy on an
    # exogenous telegraph is the T59 copy under a flipped label. The Bayes error
    # and the net learning rate equal those of the matching copy. Hamming error
    # would look worse; the bounds use the Bayes error, as in T60.
    wm_anti, E_anti = make_memory_ldb(-2.0, 1.0)
    wm_copy, E_copy = make_memory_ldb(2.0, 1.0)
    Wx_t, V_t = make_world_conservative(0.0, 1.0, "openloop")
    out_anti = analyze_jump(Wx_t, wm_anti, E_anti, V_t)
    out_copy = analyze_jump(Wx_t, wm_copy, E_copy, V_t)
    check(
        "adversarial_anticopy_is_a_relabelled_t59_copy",
        close(out_anti["eps_track"], out_copy["eps_track"], tol=1e-12)
        and close(out_anti["I_M"], out_copy["I_M"], tol=1e-12)
        and close(out_anti["I_M"], out_anti["I_t60"], tol=1e-10)
        and close(out_anti["I_M"], L(out_anti["eps_track"]), tol=1e-10)
        and out_anti["Q_M"] + 1e-12 >= out_anti["I_M"]
        and out_anti["eps_track"] < 0.5,
        "anti-copy h=-2: track=%.12f I_M=%.12f; copy h=2: track=%.12f I_M=%.12f"
        % (out_anti["eps_track"], out_anti["I_M"], out_copy["eps_track"], out_copy["I_M"]),
    )

    # 6. Exogenous reference plus a slaved plant: the T59 floor on the reference
    # is independent of how hard the plant is slaved.
    def analyze_tripartite(h, nu, r_R, delta, r_X):
        # State index: R*4 + X*2 + M.
        n = 8
        Q = np.zeros((n, n))
        E = np.zeros((2, 2))
        V = np.zeros((2, 2))
        for rr in range(2):
            for mm in range(2):
                E[rr, mm] = -h if rr == mm else 0.0
            for xx in range(2):
                V[xx, rr] = 0.0  # unused; V is on (X,M)
        for xx in range(2):
            for mm in range(2):
                V[xx, mm] = -delta if xx == mm else 0.0
        def idx(rr, xx, mm):
            return rr * 4 + xx * 2 + mm
        for rr in range(2):
            for xx in range(2):
                for mm in range(2):
                    i = idx(rr, xx, mm)
                    # R flips, exogenous
                    Q[i, idx(1 - rr, xx, mm)] += r_R
                    # M copies R, LDB in E(R,M)
                    mp = 1 - mm
                    Q[i, idx(rr, xx, mp)] += nu * math.exp(-0.5 * (E[rr, mp] - E[rr, mm]))
                    # X enslaved to M, LDB in V(X,M)
                    xp = 1 - xx
                    Q[i, idx(rr, xp, mm)] += r_X * math.exp(-0.5 * (V[xp, mm] - V[xx, mm]))
        np.fill_diagonal(Q, 0.0)
        np.fill_diagonal(Q, -Q.sum(axis=1))
        pi = stationary_from_Q(Q)
        p = np.zeros((2, 2, 2))
        for rr in range(2):
            for xx in range(2):
                for mm in range(2):
                    p[rr, xx, mm] = pi[idx(rr, xx, mm)]
        pR = p.sum(axis=(1, 2))
        I_M = 0.0
        Q_M = 0.0
        for rr in range(2):
            for xx in range(2):
                for mm in range(2):
                    mp = 1 - mm
                    flux = p[rr, xx, mm] * nu * math.exp(-0.5 * (E[rr, mp] - E[rr, mm]))
                    p_m = p[rr, :, mm].sum() / pR[rr]
                    p_mp = p[rr, :, mp].sum() / pR[rr]
                    if flux > 0.0 and p_m > 0.0 and p_mp > 0.0:
                        I_M += flux * math.log(p_mp / p_m)
                    Q_M += flux * (E[rr, mm] - E[rr, mp])
        # Bayes error for R given M (and X, or M alone)
        pRM = p.sum(axis=1)
        pM = pRM.sum(axis=0)
        eps_M = 0.0
        for mm in range(2):
            if pM[mm] <= 0.0:
                continue
            eps_M += pM[mm] - pRM[:, mm].max()
        # Task: plant disagrees with the reference
        eps_task = float(p[0, 1, :].sum() + p[1, 0, :].sum())
        return I_M, Q_M, eps_M, eps_task

    I_ref, Q_ref, eps_ref, _ = analyze_tripartite(2.0, 1.0, 1.0, 0.0, 1.0)
    floor_ref = 1.0 * L(eps_ref)
    trip_ok = close(I_ref, floor_ref, tol=1e-9)
    I_vals = [I_ref]
    for delta, r_X in [(0.0, 1.0), (1.0, 1.0), (3.0, 1.0), (3.0, 4.0), (6.0, 0.5)]:
        I_M, Q_M, eps_M, eps_task = analyze_tripartite(2.0, 1.0, 1.0, delta, r_X)
        I_vals.append(I_M)
        if not close(I_M, I_ref, tol=1e-9):
            trip_ok = False
        if not close(eps_M, eps_ref, tol=1e-9):
            trip_ok = False
        if Q_M + 1e-12 < I_M:
            trip_ok = False
    check(
        "exogenous_reference_floor_independent_of_slave_gain",
        trip_ok and close(I_ref, floor_ref, tol=1e-9),
        "I_M=%.12f = r L(eps)=%.12f at eps=%.12f, unchanged across five slave settings; Q_M>=I_M"
        % (I_ref, floor_ref, eps_ref),
    )

    # 7. Record the frozen decimals the note quotes.
    h_g1 = kalman_params(1, 1, 0.5, 1.0)
    h_g4 = kalman_params(1, 1, 0.5, 4.0)
    check(
        "recorded_decimals_match_the_note",
        close(out_en["I_M"], -0.675396079423, tol=1e-9)
        and close(out_en["eps_track"], 0.119202922022, tol=1e-9)
        and close(out_s["I_M"], -0.592743580181, tol=1e-9)
        and close(h_g1["v"], 0.809016994375, tol=1e-9)
        and close(h_g1["q_x"], 0.381966011250, tol=1e-9)
        and close(h_g1["q_m"], 0.472135955000, tol=1e-9)
        and close(h_g4["q_x"], 1.527864045000, tol=1e-9)
        and close(J8, 7.326237921249, tol=1e-9)
        and close(out0["eps_task"], 0.119202922022, tol=1e-9),
        "enslave I_M=%.12f eps=%.12f; sluggish I_M=%.12f; Kalman r=1/2 g=1: v=%.12f Q_M=%.12f Q_X=%.12f J(w=8)=%.12f"
        % (out_en["I_M"], out_en["eps_track"], out_s["I_M"], h_g1["v"], h_g1["q_m"], h_g1["q_x"], J8),
    )

    if checks_failed:
        print("FAILS %d: %s" % (len(checks_failed), ", ".join(checks_failed)))
        sys.exit(1)
    print("FAILS 0")
    print("ALL FEEDBACK-FLOOR CHECKS PASS")


if __name__ == "__main__":
    main()
