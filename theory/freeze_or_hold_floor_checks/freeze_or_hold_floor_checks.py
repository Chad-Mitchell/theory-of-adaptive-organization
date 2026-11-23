#!/usr/bin/env python3
"""Checks for theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md (T59).

Run from the repo root:
  nice -n 19 python3 theory/freeze_or_hold_floor_checks/freeze_or_hold_floor_checks.py

These checks are code identities and worked evaluations in the two-state
class of that note. They are not evidence about a real system. They test
the displayed algebra, including the JP-heat identification
I_alt = r L(eps), not a gross restoration rate (r+Gamma) L(eps). A
machinery failure sets a nonzero exit code.
"""
from __future__ import annotations

import math
import sys

checks_failed = []


def check(name, ok, detail):
    print("CHECK %s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        checks_failed.append(name)


def L(eps):
    return (1.0 - 2.0 * eps) * math.log((1.0 - eps) / eps)


def h_nats(eps):
    if eps <= 0.0 or eps >= 1.0:
        raise ValueError("entropy at the boundary")
    return -eps * math.log(eps) - (1.0 - eps) * math.log(1.0 - eps)


def escape(dE, kT, nu):
    return nu * math.exp(-dE / kT)


def steady_error(r, gamma, mu):
    return (r + gamma) / (2.0 * (r + gamma) + mu)


def mu_from_error(r, gamma, eps):
    return (r + gamma) * (1.0 - 2.0 * eps) / eps


def I_nats(eps):
    return math.log(2.0) - h_nats(eps)


def I_alt(r, gamma, eps):
    """Net information flow of memory jumps at the steady error."""
    mu = mu_from_error(r, gamma, eps)
    return (eps * (gamma + mu) - (1.0 - eps) * gamma) * math.log((1.0 - eps) / eps)


def I_alt_from_sum(r, gamma, eps):
    """Same net flow, expanded as the two opposing memory jumps."""
    mu = mu_from_error(r, gamma, eps)
    # Fair telegraph: each x has mass 1/2. Conditional laws: P(correct|x)=1-eps.
    copy_term = eps * (gamma + mu) * math.log((1.0 - eps) / eps)
    leak_term = (1.0 - eps) * gamma * math.log(eps / (1.0 - eps))
    return copy_term + leak_term


def J_rate(eps, dE, r, w, kT=1.0, nu=1.0, chi=1.0):
    """Corrected bound: JP-heat kT r L(eps) plus optional irreversible work."""
    gamma = escape(dE, kT, nu)
    return kT * r * L(eps) + chi * dE * (r + gamma) * (1.0 - 2.0 * eps) + w * eps


def J_heat_stake(eps, r, w, kT=1.0):
    return kT * r * L(eps) + w * eps


def main():
    kT = 1.0
    nu = 1.0

    # 1. Telegraph L at the repo's worked point.
    L_pt = L(0.2)
    I_dot = 1.0 * L_pt
    check(
        "telegraph_L_at_eps_0p2",
        abs(I_dot - 0.6 * math.log(4.0)) < 1e-15
        and abs(I_dot - 0.831776616672) < 5e-13,
        "code sanity; I_dot=%.12f against 0.6 ln 4" % I_dot,
    )

    # 2. Master-equation inversion.
    r, gamma, eps = 0.7, 0.3, 0.2
    mu = mu_from_error(r, gamma, eps)
    eps_back = steady_error(r, gamma, mu)
    check(
        "mu_error_inverse",
        abs(eps_back - eps) < 1e-15 and abs(mu - (r + gamma) * (1.0 - 2.0 * eps) / eps) < 1e-15,
        "code sanity; mu=%.12f, eps_back=%.12f" % (mu, eps_back),
    )

    # 3–4. Transient destruction equals (r+Gamma) L, and matches dI/dt.
    # This is the mu=0 derivative, not the JP-heat flow.
    r, gamma, eps = 0.4, 0.25, 0.15
    destroy = (r + gamma) * L(eps)
    dI_deps = -math.log((1.0 - eps) / eps)
    deps_dt = (r + gamma) * (1.0 - 2.0 * eps)
    check(
        "destruction_rate_matches_L_transient",
        abs(destroy - (r + gamma) * (1.0 - 2.0 * eps) * math.log((1.0 - eps) / eps)) < 1e-15,
        "code sanity; transient destroy=(r+Gamma)L=%.12f, not the heat flow" % destroy,
    )
    delta = 1e-8
    dI_num = (I_nats(eps + delta) - I_nats(eps - delta)) / (2.0 * delta)
    check(
        "I_derivative_finite_difference",
        abs(dI_num - dI_deps) < 1e-8
        and abs(-dI_num * deps_dt - destroy) < 1e-7,
        "code sanity; dI/deps num=%.12f anal=%.12f" % (dI_num, dI_deps),
    )

    # 5. JP-heat net flow is r L(eps), not (r+Gamma) L(eps).
    r, gamma, eps = 0.4, 0.25, 0.15
    alt = I_alt(r, gamma, eps)
    alt_sum = I_alt_from_sum(r, gamma, eps)
    check(
        "jp_heat_I_alt_equals_r_L",
        abs(alt - r * L(eps)) < 1e-15
        and abs(alt_sum - alt) < 1e-15
        and abs(alt - (r + gamma) * L(eps)) > 0.2,
        "code sanity; I_alt=%.12f, r L=%.12f, gross (r+Gamma)L=%.12f"
        % (alt, r * L(eps), (r + gamma) * L(eps)),
    )

    # 6. At r=0 the copy-plus-leak pair is at detailed balance and I_alt=0.
    gamma, eps = 0.25, 0.15
    mu0 = mu_from_error(0.0, gamma, eps)
    bracket0 = eps * (gamma + mu0) - (1.0 - eps) * gamma
    alt0 = I_alt(0.0, gamma, eps)
    check(
        "jp_heat_I_alt_vanishes_at_r_zero",
        abs(bracket0) < 1e-15 and abs(alt0) < 1e-15 and abs(I_alt(0.0, 1.7, 0.05)) < 1e-15,
        "code sanity; r=0 detailed-balance residual=%.3e, I_alt=%.3e" % (bracket0, alt0),
    )

    # 7. Gamma=0 reduction is the telegraph floor.
    check(
        "reduction_telegraph_Gamma_zero",
        abs(kT * 1.0 * L(0.2) - 0.831776616672) < 5e-13,
        "re-test; kT r L(0.2) at r=1 matches IP3 worked value",
    )

    # 8. One-time write: full bit and partial information.
    write_bit = kT * math.log(2.0)
    write_eps = kT * I_nats(0.2)
    check(
        "one_time_write_landauer",
        abs(write_bit - math.log(2.0)) < 1e-15
        and write_eps > 0.0
        and write_eps < write_bit
        and abs(write_eps - (math.log(2.0) - h_nats(0.2))) < 1e-15,
        "code sanity; full bit=%.12f nats, I(0.2)=%.12f nats" % (write_bit, write_eps),
    )

    # 9. Irreversible-lowering work is zero at dE=0 and positive for dE>0.
    r, eps, w = 0.1, 0.2, 2.0
    works = [J_rate(eps, dE, r, w, kT, nu, chi=1.0) - J_heat_stake(eps, r, w, kT) for dE in (0.0, 1.0, 2.0, 5.0, 10.0)]
    check(
        "irreversible_work_min_at_zero_barrier",
        abs(works[0]) < 1e-15 and all(work > 0.0 for work in works[1:]),
        "code sanity; work at dE=0 is 0; at 1,2,5,10: %s" % (", ".join("%.6f" % x for x in works[1:]),),
    )

    # 10. The chi=0 rate bound is independent of the barrier.
    r, eps, w = 0.3, 0.2, 2.0
    j0 = J_rate(eps, 0.0, r, w, kT, nu, chi=0.0)
    j8 = J_rate(eps, 8.0, r, w, kT, nu, chi=0.0)
    check(
        "heat_bound_independent_of_barrier",
        abs(j0 - j8) < 1e-15 and abs(j0 - J_heat_stake(eps, r, w, kT)) < 1e-15,
        "code sanity; chi=0 J at dE=0 and dE=8 both %.12f" % j0,
    )

    # 11. OU Kalman-rate identity (already-proved floor, checked as arithmetic).
    a, v, eps = 1.0, 1.0, 0.25
    R = a * (v - eps) / eps
    check(
        "ou_kalman_rate_identity",
        abs(R - 3.0) < 1e-15 and abs(a * (v / eps - 1.0) - R) < 1e-15,
        "code sanity; a(v-eps)/eps=%.12f at a=v=1, eps=1/4" % R,
    )

    # 12. JP-heat floor vanishes at r=0 even when Gamma>0, and is positive at r>0.
    eps = 0.2
    phi_frozen_leaky = 0.0 * L(eps)
    phi_world = 0.4 * L(eps)
    phi_leak_only = 0.0 * L(eps)  # Gamma does not enter Phi
    check(
        "jp_heat_floor_vanishes_at_r_zero",
        abs(phi_frozen_leaky) < 1e-15
        and abs(phi_leak_only) < 1e-15
        and phi_world > 0.0
        and L(eps) > 0.0
        and abs(I_alt(0.0, 0.15, eps)) < 1e-15
        and abs(I_alt(0.4, 0.0, eps) - phi_world) < 1e-15,
        "code sanity; Phi(0.2)=r L is 0 at r=0 with Gamma=0.15; at r=0.4 it is %.6f" % phi_world,
    )

    # 13. Joint numerical minimum of the corrected bound: barrier 0 at every r;
    # error small at small r and near 1/2 at large r.
    w = 2.0
    eps_grid = (0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5)
    dE_grid = (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 16.0, 20.0)
    r_grid = (0.001, 0.01, 0.1, 1.0, 10.0)
    best = []
    for r in r_grid:
        # Tie-break: smaller barrier, then larger error (the drop corner).
        j_min = None
        arg = None
        for eps in eps_grid:
            for dE in dE_grid:
                j = J_rate(eps, dE, r, w, kT, nu, chi=1.0)
                cand = (j, dE, -eps)
                if j_min is None or cand < j_min:
                    j_min = cand
                    arg = (eps, dE, j)
        best.append((r, arg[0], arg[1], arg[2]))
        print("  joint min at r=%g: eps=%.3f, dE=%.1f, J=%.8f" % (r, arg[0], arg[1], arg[2]))
    dE_vals = [row[2] for row in best]
    eps_vals = [row[1] for row in best]
    j_vals = [row[3] for row in best]
    heat_only = [min((J_heat_stake(eps, r, w, kT), eps) for eps in eps_grid) for r in r_grid]
    heat_eps = [pair[1] for pair in heat_only]
    check(
        "numeric_minimum_zero_barrier",
        all(abs(dE) < 1e-12 for dE in dE_vals)
        and eps_vals[0] <= 0.05
        and eps_vals[-1] >= 0.45
        and all(abs(e1 - e2) < 1e-12 for e1, e2 in zip(eps_vals, heat_eps))
        and all(abs(j_vals[i] - heat_only[i][0]) < 1e-12 for i in range(len(r_grid))),
        "worked example; optimal (eps, dE) by r: %s" % (
            ", ".join("(%.3f, %.1f)" % (e, d) for e, d in zip(eps_vals, dE_vals)),
        ),
    )

    if checks_failed:
        print("FAILS %d: %s" % (len(checks_failed), ", ".join(checks_failed)))
        sys.exit(1)
    print("FAILS 0")
    print("ALL FREEZE-OR-HOLD-FLOOR CHECKS PASS")


if __name__ == "__main__":
    main()
