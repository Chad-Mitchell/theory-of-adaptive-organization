#!/usr/bin/env python3
"""Checks for theory/ACTING_DERIVATION_2026-11-22.md.

Algebra and the five-term reduction only. The cubic comparison is
theory/acting_derivation_checks/run_locked.py, and this file does not call it.
"""
from __future__ import annotations

import sys

import numpy as np

TERMS = ("kappa_Imem", "hK", "wE", "A", "L")


def cost_keys(b: float) -> tuple[str, ...]:
    if b == 0:
        return TERMS
    return TERMS + ("rho_zu",)


def cost(b: float, coords: dict[str, float]) -> float:
    keys = cost_keys(b)
    missing = [k for k in keys if k not in coords]
    if missing:
        raise KeyError(missing)
    extra = [k for k in coords if k not in keys]
    if extra:
        raise KeyError(extra)
    return float(sum(coords[k] for k in keys))


def closed_moments(a, b, K, g, c, D, Dm):
    den = g * (a + g) * (K * b * c + a)
    v = (D * K * b * c * g + D * a * g + D * g * g + Dm * K * K * b * b) / den
    s = (D * c * g * g - Dm * K * a * b) / den
    m = (D * c * c * g * g + Dm * K * b * c * g + Dm * a * a + Dm * a * g) / den
    return v, s, m


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


def flows_from_definition(a, b, K, g, c, D, Dm):
    v, s, m = lyapunov_moments(a, b, K, g, c, D, Dm)
    sigma = np.array([[v, s], [s, m]], dtype=float)
    prec = np.linalg.inv(sigma)
    drift = np.array([[-a, -b * K], [g * c, -g]], dtype=float)
    link = drift + np.diag([D, Dm]) @ prec
    var_m_given_x = m - s * s / v
    gain = s / v
    alpha = np.array([-(gain ** 2) / var_m_given_x, gain / var_m_given_x])
    flow_x = float(link[0] @ sigma @ alpha)
    var_x_given_m = v - s * s / m
    gain_x = s / m
    beta = np.array([gain_x / var_x_given_m, -(gain_x ** 2) / var_x_given_m])
    flow_m = float(link[1] @ sigma @ beta)
    return flow_x, flow_m, v, s, m


def closed_rates(a, b, K, g, c, D, Dm):
    comb = D * c * g + Dm * K * b
    sr_x = b * K * comb / (D * (a + g))
    sr_m = c * g * comb / (Dm * (a + g))
    i_m = comb * (D * c * g * g - Dm * K * a * b) / (comb ** 2 + D * Dm * (a + g) ** 2)
    return sr_x, sr_m, i_m


def learning_rate_b0(a, g, c, D, Dm):
    return (D * c ** 2 * g ** 3) / (D * c ** 2 * g ** 2 + Dm * (a + g) ** 2)


def variance_minimizer(a, b, g, c, D, Dm):
    # Numerator of v' is proportional to A K^2 + B K + C with C < 0 < A.
    aa = Dm * b * b * c
    bb = 2.0 * Dm * a * b
    cc = -D * c * g * g
    disc = bb * bb - 4.0 * aa * cc
    return (-bb + np.sqrt(disc)) / (2.0 * aa)


def main() -> int:
    fails = 0

    def check(name, ok, detail=""):
        nonlocal fails
        if not ok:
            fails += 1
            print(f"FAIL {name} {detail}")
        else:
            print(f"ok   {name}")

    # Five-term reduction: every term is kept, and the effort coordinate is absent at b=0.
    exog = {
        "kappa_Imem": 1.0,
        "hK": 2.0,
        "wE": 3.0,
        "A": 4.0,
        "L": 5.0,
    }
    check("b=0 keys are the five terms", cost_keys(0.0) == TERMS)
    check("b=0 cost keeps each term", cost(0.0, exog) == 15.0)
    acted = dict(exog)
    acted["rho_zu"] = 7.0
    check("b!=0 adds the effort coordinate", cost_keys(1.0)[-1] == "rho_zu")
    check("effort is not minimized away at b!=0", cost(1.0, acted) == 22.0)
    try:
        cost(0.0, acted)
        check("b=0 rejects an effort coordinate", False)
    except KeyError:
        check("b=0 rejects an effort coordinate", True)

    points = [
        (1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0),
        (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
        (0.7, 0.4, 1.3, 1.1, 0.8, 0.5, 0.9),
        (1.2, 1.0, 2.0, 0.6, 1.4, 0.3, 1.5),
        (2.0, -0.5, 0.8, 1.5, 0.4, 1.1, 0.2),
    ]
    worst = 0.0
    for p in points:
        a, b, K, g, c, D, Dm = p
        closed = np.array(closed_moments(*p))
        solved = np.array(lyapunov_moments(*p))
        rel = np.max(np.abs(closed - solved) / np.maximum(1.0, np.abs(solved)))
        worst = max(worst, rel)
        fx, fm, *_ = flows_from_definition(*p)
        sr_x, sr_m, i_m = closed_rates(*p)
        # Rebuild Sr from the definition E[F^2 + D dF]/D using the solved moments.
        v, s, m = solved
        fxx = a * a * v + 2 * a * b * K * s + (b * K) ** 2 * m
        dfx = -a
        sr_x_def = (fxx + D * dfx) / D
        fmm = (g * g) * m + (g * c) ** 2 * v - 2 * g * g * c * s
        dfm = -g
        sr_m_def = (fmm + Dm * dfm) / Dm
        worst = max(worst, abs(fx + fm))
        worst = max(worst, abs(fm - i_m))
        worst = max(worst, abs(sr_x_def - sr_x), abs(sr_m_def - sr_m))
    check("Lyapunov, flow, and bath rates agree", worst < 1e-8, f"worst {worst}")

    a = g = c = D = Dm = 1.0
    v0, _, _ = closed_moments(a, 0.0, 3.0, g, c, D, Dm)
    sr0, _, i0 = closed_rates(a, 0.0, 3.0, g, c, D, Dm)
    check("b=0 variance is D/a", abs(v0 - D / a) < 1e-12)
    check("b=0 world bath rate is 0", abs(sr0) < 1e-12)
    check(
        "b=0 memory flow is the exogenous learning rate",
        abs(i0 - learning_rate_b0(a, g, c, D, Dm)) < 1e-12,
    )

    # Strong feedback: memory flow can be negative while the exogenous rate stays positive.
    _, _, i_neg = closed_rates(1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0)
    check("exogenous learning rate stays positive", learning_rate_b0(1, 1, 1, 1, 1) > 0)
    check("feedback can make the memory flow negative", i_neg < 0)

    b = 0.8
    Ke = variance_minimizer(a, b, g, c, D, Dm)

    def variance(K):
        return closed_moments(a, b, K, g, c, D, Dm)[0]

    def heat_energy(K):
        sx, sm, _ = closed_rates(a, b, K, g, c, D, Dm)
        return D * sx + Dm * sm

    check("K_E is positive", Ke > 0)
    check("variance falls through 0 and rises after K_E", variance(0.0) > variance(Ke) < variance(Ke + 0.5))
    dheat = (heat_energy(Ke + 1e-4) - heat_energy(Ke - 1e-4)) / 2e-4
    check("bath energy increases at K_E", dheat > 0)
    # Quartic loss 3 v^2. Its K-derivative vanishes at K_E; the heat derivative does not.
    def quartic(K):
        return 3.0 * variance(K) ** 2

    dq = (quartic(Ke + 1e-4) - quartic(Ke - 1e-4)) / 2e-4
    check("quartic loss is stationary at the variance minimizer", abs(dq) < 1e-4)
    check(
        "heat-aware slope at K_E is the heat slope",
        abs((quartic(Ke + 1e-4) + heat_energy(Ke + 1e-4) - quartic(Ke - 1e-4) - heat_energy(Ke - 1e-4)) / 2e-4 - dheat)
        < 1e-4,
    )

    print(f"FAILS {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
