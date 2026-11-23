#!/usr/bin/env python3
"""Continuous stationary costs for the cubic plant in the acting-derivation preregistration.

Does not read or edit PREREG.md. Euler–Maruyama is not used. The stationary
Fokker–Planck equation is solved by a Scharfetter–Gummel finite-volume scheme
on a square with no-flux faces. The costs are the preregistration's:

    J_E = E[X^2],  J_H = E[X^2] + Sr_X + Sr_M,

with D = D_M = 1, so the entropy rates are the bath energy flows.
"""
from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.optimize import minimize_scalar
from scipy.sparse.linalg import spsolve


def bernoulli(z: np.ndarray) -> np.ndarray:
    out = np.empty_like(z, dtype=float)
    small = np.abs(z) < 1e-5
    zs = z[small]
    out[small] = 1.0 - zs / 2.0 + zs**2 / 12.0 - zs**4 / 720.0
    zb = z[~small]
    out[~small] = zb / np.expm1(zb)
    return out


def moments(K: float, N: int = 200, L: float = 4.0) -> tuple[float, float, float]:
    dx = 2.0 * L / N
    xc = -L + (np.arange(N) + 0.5) * dx
    xf = -L + np.arange(1, N) * dx
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []

    def add(r: int, c: int, v: float) -> None:
        rows.append(r)
        cols.append(c)
        data.append(v)

    def idx(i: int, j: int) -> int:
        return j * N + i

    for j in range(N):
        Fx = -(xf + xf**3 + K * xc[j])
        Bm = bernoulli(-Fx * dx)
        Bp = bernoulli(Fx * dx)
        for i in range(N - 1):
            ci = Bm[i] / (dx * dx)
            cip = -Bp[i] / (dx * dx)
            ri, rip = idx(i, j), idx(i + 1, j)
            add(ri, idx(i, j), ci)
            add(ri, idx(i + 1, j), cip)
            add(rip, idx(i, j), -ci)
            add(rip, idx(i + 1, j), -cip)
    for i in range(N):
        Fm = -xf + xc[i]
        Bm = bernoulli(-Fm * dx)
        Bp = bernoulli(Fm * dx)
        for j in range(N - 1):
            cj = Bm[j] / (dx * dx)
            cjp = -Bp[j] / (dx * dx)
            rj, rjp = idx(i, j), idx(i, j + 1)
            add(rj, idx(i, j), cj)
            add(rj, idx(i, j + 1), cjp)
            add(rjp, idx(i, j), -cj)
            add(rjp, idx(i, j + 1), -cjp)
    matrix = sparse.coo_matrix((data, (rows, cols)), shape=(N * N, N * N)).tolil()
    matrix[-1, :] = dx * dx
    rhs = np.zeros(N * N)
    rhs[-1] = 1.0
    prob = spsolve(matrix.tocsr(), rhs).reshape(N, N)
    xx = xc[None, :]
    mm = xc[:, None]
    weight = dx * dx
    ex2 = float((prob * (xx * xx)).sum() * weight)
    fx = -(xx + xx**3 + K * mm)
    srx = float((prob * (fx * fx - (1.0 + 3.0 * xx * xx))).sum() * weight)
    fm = -mm + xx
    srm = float((prob * (fm * fm - 1.0)).sum() * weight)
    return ex2, srx, srm


def main() -> None:
    specs = ((200, 4.0), (160, 4.0), (160, 4.5), (180, 4.5))
    for N, L in specs:
        fit = minimize_scalar(
            lambda K: moments(K, N, L)[0],
            bracket=(0.12, 0.24, 0.40),
            tol=1e-4,
        )
        e0, sx0, sm0 = moments(0.0, N, L)
        e1, sx1, sm1 = moments(0.01, N, L)
        jh0 = e0 + sx0 + sm0
        jh1 = e1 + sx1 + sm1
        print(
            f"N {N} L {L:.1f} K_E {fit.x:.6f} J_E {fit.fun:.8f} "
            f"J_E0 {e0:.8f} Sr_X0 {sx0:.6f} J_H0 {jh0:.8f} "
            f"slope_H {(jh1 - jh0) / 0.01:.4f}"
        )
        if not fit.success:
            raise SystemExit(f"minimizer failed at N={N} L={L}")


if __name__ == "__main__":
    main()
