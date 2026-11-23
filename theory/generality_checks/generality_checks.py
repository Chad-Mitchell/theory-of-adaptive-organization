#!/usr/bin/env python3
"""Numerical checks for the (B) propositions in theory/GENERALITY_2026-11-22.md.

The examples are outside the linear-Gaussian class: a quartic equilibrium
(cubic drift), a three-state jump chain, and a heavy-tailed discrete law.
No stochastic draw. SymPy carries the capped-payoff counterexample exactly.
"""
from __future__ import annotations

import sys

import numpy as np
import sympy as sp
from scipy.integrate import simpson


FAILS = 0


def check(name, cond, detail):
    global FAILS
    if cond:
        print(f"PASS  {name}: {detail}")
    else:
        FAILS += 1
        print(f"FAIL  {name}: {detail}")


def trap(y, x):
    return float(simpson(y, x=x))


def stationary(Q):
    """Left null vector of a rate matrix, rows sum to 0, positive mass."""
    w, v = np.linalg.eig(Q.T)
    k = int(np.argmin(np.abs(w.real)))
    pi = np.real(v[:, k])
    pi = np.abs(pi)
    pi /= pi.sum()
    if pi.min() <= 0:
        # fall back: solve the augmented system
        n = Q.shape[0]
        A = np.vstack([Q.T, np.ones(n)])
        b = np.zeros(n + 1)
        b[-1] = 1.0
        pi, *_ = np.linalg.lstsq(A, b, rcond=None)
        pi = np.clip(pi, 0, None)
        pi /= pi.sum()
    return pi


def main():
    global FAILS
    np.set_printoptions(precision=12, suppress=False)

    # ------------------------------------------------------------------
    # BL-screen: a factorized joint on {0,1,2}^3, not a Gaussian law.
    # ------------------------------------------------------------------
    states = (0, 1, 2)

    def f(r, b):
        return 1.0 + 30.0 * (r == b)

    def g(e, b):
        return 1.0 + 30.0 * (e == b)

    weights = {}
    for r in states:
        for b in states:
            for e in states:
                weights[(r, b, e)] = f(r, b) * g(e, b)
    Z = sum(weights.values())
    # P(e | r, b) versus P(e | b)
    gap = 0.0
    for r in states:
        for b in states:
            den_rb = sum(weights[(r, b, e)] for e in states)
            den_b = sum(weights[(rr, b, e)] for rr in states for e in states)
            for e in states:
                prb = weights[(r, b, e)] / den_rb
                pb = sum(weights[(rr, b, e)] for rr in states) / den_b
                gap = max(gap, abs(prb - pb))
    check("BL-screen factorized", gap == 0.0, f"max |P(e|r,b)-P(e|b)| = {gap}")

    # The region alone does not screen: P(e|r) differs from P(e|r,b) somewhere.
    bare = 0.0
    for r in states:
        den_r = sum(weights[(r, b, e)] for b in states for e in states)
        for b in states:
            den_rb = sum(weights[(r, b, ee)] for ee in states)
            for e in states:
                pr = sum(weights[(r, bb, e)] for bb in states) / den_r
                prb = weights[(r, b, e)] / den_rb
                bare = max(bare, abs(pr - prb))
    check("BL-screen region is not enough", bare > 0.05, f"max gap {bare:.6f}")

    # A joint that does not factor: screening fails.
    bad = {}
    for r in states:
        for b in states:
            for e in states:
                bad[(r, b, e)] = 1 + r * e + b
    bad_gap = 0.0
    for r in states:
        for b in states:
            den_rb = sum(bad[(r, b, e)] for e in states)
            den_b = sum(bad[(rr, b, e)] for rr in states for e in states)
            for e in states:
                prb = bad[(r, b, e)] / den_rb
                pb = sum(bad[(rr, b, e)] for rr in states) / den_b
                bad_gap = max(bad_gap, abs(prb - pb))
    check("BL-screen needs the factorization", bad_gap > 1e-6, f"max gap {bad_gap:.6f}")

    # ------------------------------------------------------------------
    # EQ-learn: cubic drift, quartic equilibrium, three-state channel.
    # dX = -X^3 dt + sqrt(2D) dW, D = 1. Prior is not Gaussian.
    # ------------------------------------------------------------------
    D = 1.0
    x = np.linspace(-3.4, 3.4, 4001)
    logp = -(x ** 4) / (4.0 * D)
    logp -= logp.max()
    p = np.exp(logp)
    p /= trap(p, x)
    s_prior = -(x ** 3) / D  # exact equilibrium score
    I_prior = trap((s_prior ** 2) * p, x)
    I_parts = trap((3.0 * x ** 2) * p, x)  # -E[s']
    v = trap((x ** 2) * p, x)
    check(
        "EQ-learn prior Fisher identity",
        abs(I_prior - I_parts) < 1e-8,
        f"I={I_prior:.8f}  -E[s']={I_parts:.8f}",
    )
    check(
        "EQ-learn prior is not Gaussian",
        abs(I_prior - 1.0 / v) > 0.2,
        f"I={I_prior:.6f}  1/v={1.0 / v:.6f}  v={v:.6f}",
    )

    centers = np.array([-1.3, 0.0, 1.3])
    sigma = 0.75
    loglik = -0.5 * ((x[:, None] - centers[None, :]) / sigma) ** 2
    loglik -= loglik.max(axis=1, keepdims=True)
    pm_x = np.exp(loglik)
    pm_x /= pm_x.sum(axis=1, keepdims=True)
    joint = p[:, None] * pm_x
    mass = np.array([trap(joint[:, m], x) for m in range(3)])
    mass /= mass.sum()

    EF = 0.0
    eps = 0.0
    L_current = 0.0
    for m in range(3):
        px = joint[:, m] / trap(joint[:, m], x)
        # score of the conditional, masked where the mass is negligible
        u = np.gradient(np.log(np.maximum(px, 1e-300)), x)
        u = np.where(px > 1e-12, u, 0.0)
        Fm = trap((u ** 2) * px, x)
        mean = trap(x * px, x)
        var = trap(((x - mean) ** 2) * px, x)
        EF += mass[m] * Fm
        eps += mass[m] * var
        # J/p = D (s_prior - u); L = -E[(J/p) u]
        L_current += mass[m] * trap((-(D * (s_prior - u)) * u) * px, x)
        check(
            f"EQ-learn Fisher at m={m}",
            Fm + 1e-8 >= 1.0 / var,
            f"F={Fm:.6f}  1/var={1.0 / var:.6f}",
        )
    L_formula = D * (EF - I_prior)
    bound = D * (1.0 / eps - I_prior)
    fake = D * (1.0 / eps - 1.0 / v)
    check(
        "EQ-learn two expressions",
        abs(L_formula - L_current) < 2e-3,
        f"formula={L_formula:.6f}  current={L_current:.6f}",
    )
    check(
        "EQ-learn Fisher-Jensen bound",
        L_formula + 1e-6 >= bound and bound > 0,
        f"L={L_formula:.6f}  bound={bound:.6f}  eps={eps:.6f}",
    )
    check(
        "EQ-learn is not the OU formula",
        abs(fake - bound) > 0.2,
        f"OU-style D(1/eps-1/v)={fake:.6f}  true bound={bound:.6f}",
    )

    # ------------------------------------------------------------------
    # Three-state chain. Local detailed balance, not a telegraph.
    # Qdot = sigma + I_alt, so the bath term is at least I_alt.
    # ------------------------------------------------------------------
    def energy(x, m):
        return float((m - x) ** 2)

    def w_m(x, m, mp):
        # Symmetric prefactor, bias toward the signal label. Not a two-state telegraph.
        return np.exp(0.5 * (energy(x, m) - energy(x, mp)))

    W_X = np.array(
        [
            [0.0, 1.1, 0.35],
            [0.25, 0.0, 0.9],
            [0.55, 0.4, 0.0],
        ]
    )
    # joint states (x, m), index 3*x+m
    Q = np.zeros((9, 9))
    for x in range(3):
        for m in range(3):
            i = 3 * x + m
            for xp in range(3):
                if xp == x:
                    continue
                j = 3 * xp + m
                Q[i, j] += W_X[x, xp]
            for mp in range(3):
                if mp == m:
                    continue
                j = 3 * x + mp
                Q[i, j] += w_m(x, m, mp)
    np.fill_diagonal(Q, 0.0)
    row = Q.sum(axis=1)
    np.fill_diagonal(Q, -row)
    check("chain rows sum to 0", np.allclose(Q.sum(axis=1), 0.0), f"max {np.max(np.abs(Q.sum(axis=1))):.2e}")
    pi = stationary(Q).reshape(3, 3)  # pi[x, m]
    check("chain stationary", np.allclose(pi.ravel() @ Q, 0.0, atol=1e-8), f"residual {np.max(np.abs(pi.ravel() @ Q)):.2e}")
    px = pi.sum(axis=1)
    pm = pi.sum(axis=0)
    p_m_given_x = pi / px[:, None]
    p_x_given_m = pi / pm[None, :]

    sigma = 0.0
    I_alt = 0.0
    Qdot = 0.0
    for x in range(3):
        for m in range(3):
            for mp in range(3):
                if mp == m:
                    continue
                rate = w_m(x, m, mp)
                back = w_m(x, mp, m)
                a = pi[x, m] * rate
                sigma += a * np.log((pi[x, m] * rate) / (pi[x, mp] * back))
                I_alt += a * np.log(p_m_given_x[x, mp] / p_m_given_x[x, m])
                Qdot += a * (energy(x, m) - energy(x, mp))
    check("chain sigma nonnegative", sigma > 1e-6, f"sigma={sigma:.8f}")
    check(
        "chain heat identity",
        abs(Qdot - (sigma + I_alt)) < 1e-8,
        f"Qdot={Qdot:.8f}  sigma+I_alt={sigma + I_alt:.8f}  I_alt={I_alt:.8f}",
    )
    check("chain heat at least I_alt", Qdot + 1e-10 >= I_alt and I_alt > 0.0, f"Qdot={Qdot:.6f}  I_alt={I_alt:.6f}")
    # A variance formula in the style of the scalar OU rate, using the
    # stationary second moment of the labels {0,1,2}. It is a different number.
    labels = np.array([0.0, 1.0, 2.0])
    mean_x = float(px @ labels)
    var_x = float(px @ (labels - mean_x) ** 2)
    # conditional variance of X given M
    eps_chain = 0.0
    for m in range(3):
        mean_m = float(p_x_given_m[:, m] @ labels)
        var_m = float(p_x_given_m[:, m] @ (labels - mean_m) ** 2)
        eps_chain += pm[m] * var_m
    # fake rate: D_fake * (1/eps - 1/var) with D_fake = 1
    fake_chain = 1.0 / eps_chain - 1.0 / var_x
    check(
        "chain flow is not a variance formula",
        abs(fake_chain - I_alt) > 0.05,
        f"I_alt={I_alt:.6f}  1/eps-1/v={fake_chain:.6f}  eps={eps_chain:.6f}",
    )

    # ------------------------------------------------------------------
    # JN-pay and JN-cap. Heavy tail, and an exact cap counterexample.
    # ------------------------------------------------------------------
    ks = np.arange(0, 500)
    tail = (1.0 + ks) ** (-2.5)
    tail /= tail.sum()
    # phi(t)=(1+t)^{3/2} is strictly convex on [0, infinity). The tail is heavier
    # than a Gaussian of the same mean: the second moment sits far above the mean square.
    phi = (1.0 + ks) ** 1.5
    mean = float(tail @ ks)
    ephi = float(tail @ phi)
    second = float(tail @ (ks ** 2))
    check(
        "JN-pay heavy tail",
        ephi > (1.0 + mean) ** 1.5 * (1.0 + 1e-9) and second > 20.0 * mean ** 2,
        f"E phi={ephi:.6f}  phi(E)={(1.0 + mean) ** 1.5:.6f}  mean={mean:.4f}  E k^2={second:.4f}",
    )
    # Exact cap. phi(x)=x^2, cap 1, P(X=0)=P(X=4)=1/2.
    half = sp.Rational(1, 2)
    e_cap = half * sp.Min(0, 1) + half * sp.Min(16, 1)
    at_mean = sp.Min(4, 1)
    e_uncap = half * 0 + half * 16
    check(
        "JN-cap reverses Jensen",
        sp.simplify(e_cap) == half and at_mean == 1 and e_uncap == 8 and e_cap < at_mean,
        f"E[min(X^2,1)]={e_cap}  min((EX)^2,1)={at_mean}  E[X^2]={e_uncap}",
    )

    # ------------------------------------------------------------------
    # GN-zero. Birth-death with potential x^4/4 - b*u*x, and a controlled chain.
    # ------------------------------------------------------------------
    grid = np.linspace(-2.8, 2.8, 81)

    def birth_death(b, u, Dcoef=1.0):
        n = len(grid)
        V = grid ** 4 / 4.0 - b * u * grid
        Qb = np.zeros((n, n))
        for i in range(n - 1):
            dV = V[i + 1] - V[i]
            Qb[i, i + 1] = np.exp(-dV / (2.0 * Dcoef))
            Qb[i + 1, i] = np.exp(+dV / (2.0 * Dcoef))
        np.fill_diagonal(Qb, 0.0)
        np.fill_diagonal(Qb, -Qb.sum(axis=1))
        return Qb

    pi_u0 = stationary(birth_death(0.0, 0.0))
    pi_u5 = stationary(birth_death(0.0, 5.0))
    pi_b1 = stationary(birth_death(1.0, 1.0))
    check(
        "GN-zero cubic at b=0",
        np.allclose(pi_u0, pi_u5, atol=1e-12),
        f"max |pi(u=0)-pi(u=5)|={np.max(np.abs(pi_u0 - pi_u5)):.2e}",
    )
    mean0 = float(pi_u0 @ grid)
    mean1 = float(pi_b1 @ grid)
    check(
        "GN-zero cubic moves when b is not 0",
        abs(mean1 - mean0) > 0.2,
        f"mean b=0 {mean0:.6f}  mean b=1,u=1 {mean1:.6f}",
    )

    def controlled_chain(b, lam):
        """World rates Q0(x) + b*u(m)*A. Memory rates scale with lam."""
        u = np.array([0.0, 1.0, 2.0])
        A = np.array(
            [
                [0.0, 0.8, 0.0],
                [0.0, 0.0, 0.8],
                [0.8, 0.0, 0.0],
            ]
        )
        A = A.copy()
        np.fill_diagonal(A, 0.0)
        np.fill_diagonal(A, -A.sum(axis=1))
        Qc = np.zeros((9, 9))
        for x in range(3):
            for m in range(3):
                i = 3 * x + m
                for xp in range(3):
                    if xp == x:
                        continue
                    rate = W_X[x, xp] + b * u[m] * A[x, xp]
                    if rate < -1e-12:
                        raise RuntimeError("negative rate")
                    Qc[i, 3 * xp + m] += rate
                for mp in range(3):
                    if mp == m:
                        continue
                    Qc[i, 3 * x + mp] += lam * w_m(x, m, mp)
        np.fill_diagonal(Qc, 0.0)
        np.fill_diagonal(Qc, -Qc.sum(axis=1))
        return Qc

    def x_marginal(b, lam):
        pic = stationary(controlled_chain(b, lam)).reshape(3, 3)
        return pic.sum(axis=1)

    m_slow = x_marginal(0.0, 0.4)
    m_fast = x_marginal(0.0, 3.0)
    m_b_slow = x_marginal(1.0, 0.4)
    m_b_fast = x_marginal(1.0, 3.0)
    check(
        "GN-zero chain at b=0",
        np.allclose(m_slow, m_fast, atol=1e-10),
        f"max gap {np.max(np.abs(m_slow - m_fast)):.2e}  marginal {m_slow}",
    )
    check(
        "GN-zero chain moves when b is not 0",
        np.max(np.abs(m_b_slow - m_b_fast)) > 1e-3,
        f"max gap {np.max(np.abs(m_b_slow - m_b_fast)):.6f}",
    )

    print(f"FAILS {FAILS}")
    if FAILS == 0:
        print("ALL GENERALITY CHECKS PASS")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
