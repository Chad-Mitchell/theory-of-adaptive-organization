#!/usr/bin/env python3
"""Independent arithmetic for the PR 161 review. Standard library only."""
from __future__ import annotations

import math
from decimal import Decimal, getcontext

getcontext().prec = 50


def main() -> None:
    a = Decimal("0.9")
    Q = Decimal(1)
    P = Decimal("0.5")
    k = 2
    V = Q / (1 - a * a)
    a2k = a ** (2 * k)
    I = Decimal("0.5") * (V / P).ln()
    r = Decimal("0.5") * (a * a + Q / P).ln()
    D = a2k * P + V * (1 - a2k)
    print(f"V={V}")
    print(f"I={I}")
    print(f"r={r}")
    print(f"D={D}")

    q = Decimal("0.05") * Decimal("1.30") / (Decimal("1.30") - Decimal("1.05"))
    lean = Decimal("0.95") * Decimal("1.30")
    robust = Decimal("0.95") * Decimal("1.05") + Decimal("0.05") * Decimal("0.90")
    print(f"q={q} lean={lean} robust={robust}")

    c, w, sg, s0, y = 0.05, 1.0, 1.0, 0.3, 1.0
    alpha = w * sg ** 2 / 2.0
    beta = (w ** 2) * (sg ** 4) / 3.0
    tE = math.sqrt(c / alpha)
    disc = y * y - 4 * alpha * c
    r1 = (y - math.sqrt(disc)) / (2 * alpha)
    r2 = (y + math.sqrt(disc)) / (2 * alpha)

    def phi(t: float) -> float:
        mp = c / t ** 2 - alpha
        m = y - (c / t + alpha * t)
        s2 = s0 ** 2 + beta * t ** 3
        return mp * s2 - m * (3 * beta * t ** 2)

    lo, hi = r1 + 1e-15, tE
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if phi(mid) > 0:
            lo = mid
        else:
            hi = mid
    tS = 0.5 * (lo + hi)
    print(f"tau_E={tE:.12f} tau_S={tS:.12f} phi(tau_S)={phi(tS):.3e}")
    changes = 0
    prev = None
    for i in range(1, 20001):
        t = r1 + (r2 - r1) * i / 20000
        s = 1 if phi(t) > 0 else -1
        if prev is not None and s != prev:
            changes += 1
        prev = s
    print(f"phi sign changes on (r1,r2): {changes}")

    ratio = math.gamma(5 / 4) / math.gamma(1 / 4)
    print(f"Gamma(5/4)/Gamma(1/4)={ratio:.16f}")

    lam_L = 0.5 * (math.log(4.0) + math.log(0.05))
    lam_H = math.log(1.1)
    print(f"lambda_L={lam_L:.12f} lambda_H={lam_H:.12f}")

    # f_B - f_A = 2 - 1.5 x on the frequency of the dominated type
    for x in (0.0, 0.5, 1.0):
        gap = 2.0 - 1.5 * x
        print(f"invasion gap at x={x:.1f}: {gap:.3f}")


if __name__ == "__main__":
    main()
