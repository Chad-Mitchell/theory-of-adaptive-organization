#!/usr/bin/env python3
"""Checks for theory/DRIFT_HEAT_LIFT_2026-11-23.md.

Closed-form rates for a linear Einstein spring coupled to a linear world,
plus a short exact-Gaussian check that the discrete inflow of the
Kalman-Bucy-matched spring approaches the EQ-heat learning rate.

Run from the repo root:
  nice -n 19 python3 theory/drift_heat_lift_checks/drift_heat_lift_checks.py
"""
from __future__ import annotations

import math
import sys

import numpy as np
from numpy.linalg import inv, slogdet

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
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------------------
# Linear-Gaussian rates
# ---------------------------------------------------------------------------

def rates_from_cov(P, C, R, beta, gamma, Dm, kT=1.0):
    """EQ-heat learning rate and bath heat from a joint covariance.

    World / memory: dX = alpha X dt + sigma dW_X,
    dM = (-beta M + gamma X) dt + sqrt(2 Dm) dW_M.
    P=Var(X), C=Cov(X,M), R=Var(M). kT is Boltzmann's constant times
    the memory bath temperature. Q = kT * Sr_M.
    """
    nu = P - C * C / R
    I_dot = gamma * C / R - Dm * (C * C) / (nu * R * R)
    EF2 = gamma * gamma * P + beta * beta * R - 2.0 * gamma * beta * C
    Sr = (EF2 - Dm * beta) / Dm
    Q = kT * Sr
    return {"nu": nu, "I_dot": I_dot, "Q": Q, "Sr": Sr, "err_raw": R + P - 2.0 * C}


def stationary_ou_cov(a, beta, gamma, Dm, v):
    """Steady second moments of an OU world dX = -a X dt + sqrt(2 a v) dW."""
    C = gamma * v / (a + beta)
    R = Dm / beta + (gamma ** 2) * v / (beta * (a + beta))
    return v, C, R


def rw_centered_asymptotics(sigma, lam, Dm, kT=1.0):
    """Long-run rates for a random walk (alpha=0) and a centered spring
    (beta = gamma = lam). Error stays finite while Var(X) grows."""
    sig2 = sigma * sigma
    err = (sig2 + 2.0 * Dm) / (2.0 * lam)
    I_dot = lam * sig2 / (sig2 + 2.0 * Dm)
    Q = kT * lam * sig2 / (2.0 * Dm)
    floor = sig2 / (2.0 * err)
    P_path, T = path_error_and_rate(0.0, lam, lam, sigma, Dm)
    return {
        "err": err,
        "I_dot": I_dot,
        "Q": Q,
        "floor": floor,
        "Q_over_Idot": Q / I_dot,
        "P_path": P_path,
        "T": T,
        "capacity": I_dot / T,
    }


def path_error_and_rate(alpha, beta, gamma, sigma, Dm):
    """Filtering error and Duncan rate for the path of M, treated as
    an observation dY = gamma X dt + sqrt(2 Dm) dW (the -beta M term
    is known given the path)."""
    Acoeff = (gamma * gamma) / (2.0 * Dm)
    disc = (2.0 * alpha) ** 2 + 4.0 * Acoeff * (sigma * sigma)
    P_path = (2.0 * alpha + math.sqrt(disc)) / (2.0 * Acoeff)
    T = (gamma * gamma) * P_path / (4.0 * Dm)
    return P_path, T


def rw_kb_params(sigma, eps):
    """Kalman-Bucy matched centered spring for a random walk at error eps."""
    K = (sigma * sigma) / eps
    Dm = 0.5 * sigma * sigma
    return K, Dm


def rw_fast_params(sigma, eps, Dm):
    """Centered spring that holds error eps at a chosen memory noise Dm."""
    lam = (sigma * sigma + 2.0 * Dm) / (2.0 * eps)
    return lam, Dm


def short_time_inflow(gamma, nu, Dm):
    """dt -> 0 limit of I(X_t; M_{t+dt} | M_t) / dt for a linear spring."""
    return (gamma * gamma) * nu / (4.0 * Dm)


# ---------------------------------------------------------------------------
# Exact discrete-time mutual information for a short step
# ---------------------------------------------------------------------------

def _expm(M):
    try:
        from scipy.linalg import expm
        return expm(M)
    except Exception:
        X = np.eye(M.shape[0])
        term = np.eye(M.shape[0])
        for k in range(1, 24):
            term = term @ M / k
            X = X + term
        return X


def van_loan_Phi_Q(alpha, beta, gamma, sigma, Dm, dt):
    A = np.array([[alpha, 0.0], [gamma, -beta]], dtype=float)
    GG = np.diag([sigma * sigma, 2.0 * Dm])
    M = np.zeros((4, 4))
    M[:2, :2] = A
    M[:2, 2:] = GG
    M[2:, 2:] = -A.T
    E = _expm(M * dt)
    Phi = E[:2, :2]
    Qd = E[:2, 2:] @ Phi.T
    Qd = 0.5 * (Qd + Qd.T)
    return Phi, Qd


def discrete_state_inflow_rate(P, C, R, alpha, beta, gamma, sigma, Dm, dt):
    """I(X_{t+dt}; M_{t+dt} | M_t) / dt from the exact Gaussian transition."""
    Phi, Qd = van_loan_Phi_Q(alpha, beta, gamma, sigma, Dm, dt)
    S0 = np.array([[P, C], [C, R]], dtype=float)
    S10 = Phi @ S0
    S1 = Phi @ S0 @ Phi.T + Qd
    big = np.zeros((4, 4))
    big[:2, :2] = S0
    big[:2, 2:] = S10.T
    big[2:, :2] = S10
    big[2:, 2:] = S1

    def cond_h(idx, cond):
        ix = list(idx) + list(cond)
        S = big[np.ix_(ix, ix)]
        k = len(idx)
        Saa = S[:k, :k]
        Sab = S[:k, k:]
        Sbb = S[k:, k:]
        Schur = Saa - Sab @ inv(Sbb) @ Sab.T
        _, logdet = slogdet(Schur)
        return 0.5 * (k * math.log(2.0 * math.pi * math.e) + logdet)

    # indices: 0=X_t, 1=M_t, 2=X_{t+dt}, 3=M_{t+dt}
    r = cond_h([2], [1]) - cond_h([2], [3, 1])
    return r / dt


def rw_asymptotic_cov(P, sigma, lam, Dm):
    """Late-time second moments for a centered random-walk spring, at a
    chosen (large) world variance P."""
    sig2 = sigma * sigma
    rho = (2.0 * Dm - 3.0 * sig2) / (2.0 * lam)
    C = P - sig2 / lam
    R = P + rho
    return P, C, R


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def run_checks():
    kT = 1.0

    # 1. Stationary OU identities match the repo's linear_memory formulas.
    a, v, beta, gamma, Dm = 1.0, 1.0, 5.0, 4.0, 0.8
    P, C, R = stationary_ou_cov(a, beta, gamma, Dm, v)
    row = rates_from_cov(P, C, R, beta, gamma, Dm, kT)
    L_repo = a * (v / row["nu"] - 1.0)
    Q_repo = a * v * gamma ** 2 / (Dm * (a + beta))
    check(
        "stationary OU I_dot and Q match the known linear-spring formulas",
        near(row["I_dot"], L_repo, 1e-12) and near(row["Q"], Q_repo, 1e-12),
        "I_dot=%.12f Q=%.12f" % (row["I_dot"], row["Q"]),
    )

    # 2. Random-walk Kalman-Bucy matching: identification and factor 2.
    sigma, eps = 1.0, 0.2
    K, Dm_kb = rw_kb_params(sigma, eps)
    asy = rw_centered_asymptotics(sigma, K, Dm_kb, kT)
    check(
        "KB-matched random-walk spring: I_dot equals PD7 floor sigma^2/(2 eps)",
        near(asy["I_dot"], asy["floor"], 1e-14) and near(asy["I_dot"], 2.5, 1e-14)
        and near(asy["err"], eps, 1e-14),
        "I_dot=%.12f err=%.12f" % (asy["I_dot"], asy["err"]),
    )
    check(
        "KB-matched spring: bath heat is 2 kT I_dot (capacity 1)",
        near(asy["Q_over_Idot"], 2.0, 1e-14)
        and near(asy["P_path"], asy["err"], 1e-14)
        and near(asy["capacity"], 1.0, 1e-14)
        and near(asy["T"], asy["I_dot"], 1e-14),
        "Q=%.12f C=%.12f T=%.12f" % (asy["Q"], asy["capacity"], asy["T"]),
    )
    check(
        "KB-matched closed form: Q/I_dot = 1 + sigma^2/(2 Dm) equals 2",
        near(1.0 + (sigma * sigma) / (2.0 * Dm_kb), 2.0, 1e-15),
        "",
    )

    # 3. Fast family: heat approaches kT I_dot; I_dot stays at the PD7 floor;
    #    capacity falls; the short-time discrete inflow does not equal I_dot.
    prev_ratio = None
    for Dm in (0.5, 2.0, 10.0, 100.0, 1e4, 1e6):
        lam, _ = rw_fast_params(sigma, eps, Dm)
        asy = rw_centered_asymptotics(sigma, lam, Dm, kT)
        ratio = asy["Q_over_Idot"]
        expected_ratio = 1.0 + (sigma * sigma) / (2.0 * Dm)
        st = short_time_inflow(lam, asy["err"], Dm)
        ok = (
            near(asy["I_dot"], 2.5, 1e-12)
            and near(asy["err"], eps, 1e-12)
            and near(ratio, expected_ratio, 1e-12)
            and asy["Q"] + 1e-15 >= kT * asy["I_dot"]
            and asy["capacity"] <= 1.0 + 1e-12
        )
        if prev_ratio is not None:
            ok = ok and ratio < prev_ratio + 1e-15
        # short-time inflow equals I_dot only at the KB noise Dm = sigma^2/2
        if near(Dm, 0.5 * sigma * sigma, 1e-12):
            ok = ok and near(st, asy["I_dot"], 1e-12)
        else:
            ok = ok and st > asy["I_dot"] + 1e-9
        check(
            "fast family at Dm=%g: I_dot pinned, heat ratio %s, short-time inflow identified only at KB"
            % (Dm, "2" if Dm == 0.5 else "falls toward 1"),
            ok,
            "Q/I=%.8f short/I=%.4f C=%.6f" % (ratio, st / asy["I_dot"], asy["capacity"]),
        )
        prev_ratio = ratio
    asy_fast = rw_centered_asymptotics(sigma, *rw_fast_params(sigma, eps, 1e6), kT)
    check(
        "fast-spring heat approaches kT times the PD7 rate (factor 1), not a PD1 lift",
        near(asy_fast["Q"], kT * 2.5, 1e-5) and asy_fast["capacity"] < 0.01,
        "Q=%.8f C=%.6f" % (asy_fast["Q"], asy_fast["capacity"]),
    )

    # 4. Discrete inflow of the KB-matched spring approaches I_dot as dt -> 0.
    P_late = 50.0
    P, C, R = rw_asymptotic_cov(P_late, sigma, K, Dm_kb)
    row = rates_from_cov(P, C, R, K, K, Dm_kb, kT)
    check(
        "late-time KB covariance recovers err=0.2 and I_dot=2.5",
        near(row["nu"], 0.2, 1e-12) and near(row["I_dot"], 2.5, 1e-12)
        and near(row["Q"], 5.0, 1e-12),
        "nu=%.12f I_dot=%.12f Q=%.12f" % (row["nu"], row["I_dot"], row["Q"]),
    )
    rates = []
    for dt, tol in ((1e-2, 3e-2), (1e-3, 4e-3), (1e-4, 4e-4)):
        rate = discrete_state_inflow_rate(P, C, R, 0.0, K, K, sigma, Dm_kb, dt)
        rates.append(rate)
        check(
            "KB discrete inflow I(X_{t+dt}; M_{t+dt} | M_t)/dt at dt=%g approaches I_dot" % dt,
            near(rate, row["I_dot"], tol) and (len(rates) < 2 or abs(rate - row["I_dot"]) <= abs(rates[-2] - row["I_dot"]) + 1e-12),
            "rate=%.8f I_dot=%.8f abs err=%.2e" % (rate, row["I_dot"], abs(rate - row["I_dot"])),
        )

    # 5. EQ-heat inequality: Q >= kT I_dot on the whole centered RW family.
    ok_ineq = True
    for Dm in np.geomspace(0.05, 1e4, 16):
        for lam in np.geomspace(0.5, 1e4, 12):
            asy = rw_centered_asymptotics(sigma, float(lam), float(Dm), kT)
            if asy["I_dot"] <= 0 or asy["err"] <= 0:
                ok_ineq = False
                break
            if asy["Q"] + 1e-12 < kT * asy["I_dot"]:
                ok_ineq = False
                break
        if not ok_ineq:
            break
    check(
        "EQ-heat inequality Q >= kT I_dot on a grid of centered random-walk springs",
        ok_ineq,
        "",
    )

    # 6. Shrunk-spring OU consistency with the already-proved factor-1 infimum.
    a, v, eps = 1.0, 1.0, 0.2
    Rkal = a * (v - eps) / eps

    def shrunk(lam):
        c = (v - eps) / v
        rho = lam / (a + lam)
        sig2 = (v - eps) * (rho * (v + eps) / v - 1.0)
        beta, gamma, Dm = lam, c * lam, lam * sig2
        P, C, R = stationary_ou_cov(a, beta, gamma, Dm, v)
        row = rates_from_cov(P, C, R, beta, gamma, Dm, kT)
        return row, Rkal

    row6, _ = shrunk(1e6)
    check(
        "fast shrunk spring on a stationary OU: heat approaches kT R(eps)=4, not 8",
        near(row6["nu"], 0.2, 1e-8) and near(row6["I_dot"], 4.0, 1e-8)
        and near(row6["Q"], 4.0, 1e-4) and row6["Q"] > 4.0,
        "mmse=%.10f I_dot=%.10f Q=%.10f" % (row6["nu"], row6["I_dot"], row6["Q"]),
    )

    print()
    if FAIL == 0:
        print("ALL DRIFT-HEAT-LIFT CHECKS PASS  (%d passed)" % PASS)
        return 0
    print("DRIFT-HEAT-LIFT CHECKS FAILED  (%d passed, %d failed)" % (PASS, FAIL))
    return 1


if __name__ == "__main__":
    sys.exit(run_checks())
