#!/usr/bin/env python3
"""Independent spot check for the generality audit.

Does not import theory/generality_checks. The quartic law is the equilibrium
of the cubic drift. The channel is Laplace, not the audit's Gaussian kernels.
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import quad
from scipy.special import gamma


def main() -> None:
    v_exact = 2 * gamma(0.75) / gamma(0.25)
    i_exact = 3 * v_exact
    print(f"exact v={v_exact:.10f}  I=3v={i_exact:.10f}  1/v={1/v_exact:.10f}")

    z, _ = quad(lambda x: np.exp(-(x**4) / 4), -np.inf, np.inf, epsabs=1e-12)
    v_q, _ = quad(lambda x: (x**2) * np.exp(-(x**4) / 4), -np.inf, np.inf, epsabs=1e-12)
    i_q, _ = quad(lambda x: (x**6) * np.exp(-(x**4) / 4), -np.inf, np.inf, epsabs=1e-12)
    print(f"quad v={v_q/z:.10f}  I={i_q/z:.10f}  I-3v={(i_q - 3*v_q)/z:.2e}")

    x = np.linspace(-4.0, 4.0, 8001)
    logp = -(x**4) / 4.0
    logp -= logp.max()
    p = np.exp(logp)
    p /= np.trapezoid(p, x)
    s = -(x**3)
    i_prior = float(np.trapezoid((s**2) * p, x))
    centers = np.array([-1.2, 0.0, 1.2])
    loglik = -np.abs(x[:, None] - centers[None, :]) / 0.9
    loglik -= loglik.max(axis=1, keepdims=True)
    pm_x = np.exp(loglik)
    pm_x /= pm_x.sum(axis=1, keepdims=True)
    joint = p[:, None] * pm_x
    mass = np.array([np.trapezoid(joint[:, m], x) for m in range(3)])
    mass /= mass.sum()
    ef = eps = l_cur = 0.0
    for m in range(3):
        px = joint[:, m] / np.trapezoid(joint[:, m], x)
        u = np.gradient(np.log(np.maximum(px, 1e-300)), x)
        u = np.where(px > 1e-10, u, 0.0)
        mean = float(np.trapezoid(x * px, x))
        var = float(np.trapezoid((x - mean) ** 2 * px, x))
        fm = float(np.trapezoid((u**2) * px, x))
        moment = float(np.trapezoid(u * (x - mean) * px, x))
        ef += mass[m] * fm
        eps += mass[m] * var
        l_cur += mass[m] * float(np.trapezoid((-(s - u) * u) * px, x))
        print(f"m={m} F={fm:.6f} 1/var={1/var:.6f} score_moment={moment:.6f}")
    v = float(np.trapezoid((x**2) * p, x))
    l_formula = ef - i_prior
    bound = 1.0 / eps - i_prior
    fake = 1.0 / eps - 1.0 / v
    print(
        f"Laplace L={l_formula:.6f} current={l_cur:.6f} "
        f"bound={bound:.6f} OU-style={fake:.6f}"
    )
    if abs(l_formula - l_cur) > 5e-3 or l_formula + 1e-6 < bound or abs(fake - bound) < 0.05:
        raise SystemExit("laplace check did not hold")

    xs = np.array([0.0, 1.0, 8.0])
    ws = np.array([0.7, 0.2, 0.1])
    ephi = float(ws @ np.exp(xs / 4.0))
    at = float(np.exp((ws @ xs) / 4.0))
    print(f"Jensen E phi={ephi:.6f} phi(E)={at:.6f}")
    if ephi <= at:
        raise SystemExit("jensen check did not hold")

    grid = np.linspace(-2.8, 2.8, 81)

    def gibbs(b, u):
        pot = grid**4 / 4.0 - b * u * grid
        w = np.exp(-pot - (-pot).max())
        return w / w.sum()

    g0, g5, g1 = gibbs(0.0, 0.0), gibbs(0.0, 5.0), gibbs(1.0, 1.0)
    print(
        f"Gibbs b=0 gap={np.max(np.abs(g0-g5)):.3e} "
        f"mean0={g0 @ grid:.6f} mean1={g1 @ grid:.6f}"
    )
    if not np.allclose(g0, g5) or abs((g1 @ grid) - (g0 @ grid)) <= 0.2:
        raise SystemExit("gibbs check did not hold")
    print("SPOTCHECK HOLDS")


if __name__ == "__main__":
    main()
