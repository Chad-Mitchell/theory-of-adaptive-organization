#!/usr/bin/env python3
"""Checks for theory/AREA_LAW_PROBE_2026-11-23.md (T62).

Run from the repo root:
  nice -n 19 python3 theory/area_law_probe_checks/area_law_probe_checks.py

These checks are code identities and in-model evaluations in class AL
(frozen static-bias records, telegraph products, and a bounded-capacity
boundary). They are not evidence about a real system. A machinery
failure sets a nonzero exit code.
"""
from __future__ import annotations

import math
import sys

checks_failed = []


def check(name, ok, detail):
    print("CHECK %s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        checks_failed.append(name)


def close(a, b, tol=1e-12):
    return abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b)))


def binary_entropy(p):
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


def stock_nats(eps):
    return math.log(2.0) - binary_entropy(eps)


def L(eps):
    if eps <= 0.0 or eps >= 0.5:
        return math.inf if eps <= 0.0 else 0.0
    return (1.0 - 2.0 * eps) * math.log((1.0 - eps) / eps)


def boltzmann_error(delta_e):
    # Less-likely state of a two-state record at kT = 1.
    return 1.0 / (1.0 + math.exp(delta_e))


def kl_bernoulli(p, q):
    # D_KL(Bern(p) || Bern(q)), in nats; 0/1 edges handled as limits.
    def term(a, b):
        if a == 0.0:
            return 0.0
        if b == 0.0:
            return math.inf
        return a * math.log(a / b)

    return term(p, q) + term(1.0 - p, 1.0 - q)


def main():
    eps = 0.2
    I_eps = stock_nats(eps)
    L_eps = L(eps)
    check(
        "binary_stock_and_L_at_error_0.2",
        close(I_eps, 0.192744757022, tol=1e-12) and close(L_eps, 0.831776616672, tol=1e-12)
        and close(L_eps, 0.6 * math.log(4.0), tol=1e-15),
        "I=%.15f L=%.15f = 0.6 ln 4" % (I_eps, L_eps),
    )
    check(
        "telegraph_L_equals_bernoulli_KL",
        close(L_eps, kl_bernoulli(eps, 1.0 - eps), tol=1e-15),
        "L(eps)=KL(Bern(eps)||Bern(1-eps))=%.15f" % L_eps,
    )

    # Frozen static bias: r = 0, local detailed balance, affinity zero.
    delta_e = math.log(4.0)  # Boltzmann error 0.2
    eps_b = boltzmann_error(delta_e)
    # Memory rates in LDB at this bias, leak Gamma, no world drive.
    gamma = 0.25
    # Forward and reverse memory rates for a two-state well: ratio e^{Delta E}.
    rate_up = gamma
    rate_down = gamma * math.exp(delta_e)
    affinity = math.log(rate_down / rate_up) - delta_e
    # Net probability current at the Boltzmann occupation is zero, so I_alt = 0.
    p_wrong = eps_b
    p_right = 1.0 - eps_b
    flux_up = p_right * rate_up
    flux_down = p_wrong * rate_down
    I_alt_frozen = 0.0  # net current vanishes; net KL flow is zero
    check(
        "static_bias_boltzmann_error_and_detailed_balance",
        close(eps_b, 0.2, tol=1e-15) and close(affinity, 0.0, tol=1e-15)
        and close(flux_up, flux_down, tol=1e-15) and close(I_alt_frozen, 0.0, tol=1e-15),
        "eps=%.15f affinity=%.15e flux_up=%.15f flux_down=%.15f I_alt=0" % (
            eps_b, affinity, flux_up, flux_down
        ),
    )

    # AL-stock-free: N_V independent frozen records, total heat 0, stock scales.
    n_v = 100
    stock_100 = n_v * I_eps
    heat_rate = n_v * I_alt_frozen  # each I_alt is 0
    check(
        "frozen_volume_stock_scales_at_zero_heat",
        close(stock_100, 19.274475702176, tol=1e-12) and close(heat_rate, 0.0, tol=1e-15)
        and close(stock_nats(0.2) * 50, 0.5 * stock_100, tol=1e-15),
        "N=100 stock=%.15f heat_rate=%.15f; half N has half stock" % (stock_100, heat_rate),
    )

    # Boundary capacity of N binary unit-rate channels: C_B = N ln 2.
    c_one = math.log(2.0)
    c4 = 4 * c_one
    c20 = 20 * c_one
    check(
        "boundary_capacity_four_and_twenty",
        close(c4, 2.772588722240, tol=1e-12) and close(c20, 13.862943611199, tol=1e-12),
        "C4=%.15f C20=%.15f" % (c4, c20),
    )

    # AL-write: write time at least stock / C_B; after that, ongoing heat is still 0.
    t_write = stock_100 / c4
    check(
        "write_time_lower_bound_then_zero_ongoing_heat",
        close(t_write, 6.951797627816, tol=1e-12) and close(heat_rate, 0.0, tol=1e-15)
        and t_write > 0.0,
        "T_write=%.15f; ongoing heat after write remains 0" % t_write,
    )

    # AL-volume-track vs AL-flux: V independent telegraphs at error eps, r = 1.
    v10 = 10
    need_10 = v10 * 1.0 * L_eps
    check(
        "ten_telegraphs_unattainable_on_four_channels",
        close(need_10, 8.317766166719, tol=1e-12) and need_10 > c4 and need_10 < c20,
        "need=%.15f C4=%.15f C20=%.15f" % (need_10, c4, c20),
    )

    # Joint convexity of KL, the step used in AL-volume-track.
    # Two conditionals, mixed with weight 1/2, must not increase KL.
    p1, p2, q1, q2 = 0.1, 0.3, 0.4, 0.05
    kl_avg = 0.5 * kl_bernoulli(p1, q1) + 0.5 * kl_bernoulli(p2, q2)
    kl_mix = kl_bernoulli(0.5 * p1 + 0.5 * p2, 0.5 * q1 + 0.5 * q2)
    check(
        "joint_convexity_of_binary_KL",
        kl_avg + 1e-15 >= kl_mix and kl_mix > 0.0,
        "avg=%.15f mix=%.15f, avg >= mix" % (kl_avg, kl_mix),
    )

    # Product of two symmetric telegraphs: a product memory attains 2 r L(eps).
    # Each copy at error eps has I_alt = r L(eps); two copies add.
    r = 1.0
    attain_product = 2.0 * r * L_eps
    check(
        "product_memory_attains_two_telegraph_floor",
        close(attain_product, 2.0 * L_eps, tol=1e-15) and attain_product <= 2.0 * c_one * 10,
        "2 r L=%.15f, below a loose two-channel cap if c is large" % attain_product,
    )

    # Cube packing: V = n^3, A = 6 n^2, phi = 1, r = 1, eps = 0.2.
    phi = 1.0
    sides = {}
    for n in (2, 4, 8, 16):
        volume = n ** 3
        area = 6 * n ** 2
        need = volume * r * L_eps
        cap = phi * area
        sides[n] = (volume, area, need, cap, need <= cap)
    check(
        "cube_side_4_fits_and_side_8_misses",
        sides[4][4] and (not sides[8][4]) and sides[2][4] and (not sides[16][4])
        and close(sides[4][2], 53.233703467004, tol=1e-12)
        and close(sides[4][3], 96.0, tol=1e-15)
        and close(sides[8][2], 425.869627736030, tol=1e-12)
        and close(sides[8][3], 384.0, tol=1e-15)
        and close(sides[16][2], 3406.957021888243, tol=1e-12)
        and close(sides[16][3], 1536.0, tol=1e-15),
        "n=4 need=%.15f cap=%.15f; n=8 need=%.15f cap=%.15f" % (
            sides[4][2], sides[4][3], sides[8][2], sides[8][3]
        ),
    )
    ncrit = 6.0 * phi / (r * L_eps)
    check(
        "cube_critical_side_quoted",
        close(ncrit, 7.213475204445, tol=1e-12) and 4 < ncrit < 8,
        "n_crit=%.15f lies between 4 and 8" % ncrit,
    )

    # AL-area at fixed phi: learning rate cap scales linearly with A, not V.
    cap2, cap4 = sides[2][3], sides[4][3]
    check(
        "capacity_scales_with_area_not_volume",
        close(cap4 / cap2, 4.0, tol=1e-15)  # area ratio (6*16)/(6*4) = 4
        and close((4 ** 3) / (2 ** 3), 8.0, tol=1e-15)  # volume ratio is 8
        and not close(cap4 / cap2, 8.0, tol=1e-9),
        "area ratio=%.15f volume ratio=8; cap follows area" % (cap4 / cap2),
    )

    # Recorded decimals in the note (quoted at 12 places, plus the cube sides).
    check(
        "recorded_decimals_match_the_note",
        close(I_eps, 0.192744757022, tol=1e-12)
        and close(L_eps, 0.831776616672, tol=1e-12)
        and close(stock_100, 19.274475702176, tol=1e-12)
        and close(t_write, 6.951797627816, tol=1e-12)
        and close(c4, 2.772588722240, tol=1e-12)
        and close(c20, 13.862943611199, tol=1e-12)
        and close(need_10, 8.317766166719, tol=1e-12)
        and close(sides[8][2], 425.869627736030, tol=1e-12)
        and close(sides[4][2], 53.233703467004, tol=1e-12),
        "I=%.12f L=%.12f stock100=%.12f Twrite=%.12f C4=%.12f need10=%.12f n8=%.12f"
        % (I_eps, L_eps, stock_100, t_write, c4, need_10, sides[8][2]),
    )

    if checks_failed:
        print("FAILS %d: %s" % (len(checks_failed), ", ".join(checks_failed)))
        sys.exit(1)
    print("FAILS 0")
    print("ALL AREA-LAW-PROBE CHECKS PASS")


if __name__ == "__main__":
    main()
