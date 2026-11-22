#!/usr/bin/env python3
"""Recompute the digits cited by theory/TEST_SEARCH_2026-11-22.md.

Stdlib only. No network. No outcome series.
"""
import math


def lam(f):
    return 0.6 * math.log(1.0 + f) + 0.4 * math.log(1.0 - f)


def dlam(f):
    return 0.6 / (1.0 + f) - 0.4 / (1.0 - f)


def main():
    assert abs(dlam(0.2)) < 1e-15
    assert abs(lam(0.2) - 0.020135513551) < 5e-13
    assert lam(0.99) < lam(0.2)
    assert abs((0.99 - 0.2) - 0.79) < 1e-15
    # E[W] - 1 = (2p - 1) f = 0.2 f, so the mean maximizer is the right endpoint.
    assert abs((0.6 - 0.4) - 0.2) < 1e-15
    # GB1's following paragraph: on the unit box, eps < 0.2 puts both argmaxes at 1.
    for eps in (0.05, 0.19):
        assert min(1.0, 0.2 / eps) == 1.0
    assert abs(min(1.0, 0.2 / 1.0) - 0.2) < 1e-15

    beta, a1, b1, b0 = 0.05, 1.30, 1.05, 0.90
    q = beta * a1 / (a1 - b1)
    mean_lean = (1.0 - beta) * a1
    mean_robust = (1.0 - beta) * b1 + beta * b0
    assert abs(q - 0.26) < 1e-15
    assert abs(mean_lean - 1.235) < 1e-15
    assert abs(mean_robust - 1.0425) < 1e-15

    c, alpha, s0, beta_v, y = 0.05, 0.5, 0.3, 1.0 / 3.0, 1.0

    def J(t):
        return c / t + alpha * t

    def s2(t):
        return s0 ** 2 + beta_v * t ** 3

    def jp(t):
        return -c / t ** 2 + alpha

    def th_num(t):
        return -(jp(t) * s2(t) + (y - J(t)) * (3.0 * beta_v * t ** 2))

    t_e = math.sqrt(c / alpha)
    lo, hi = 0.05, t_e
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if th_num(mid) > 0.0:
            lo = mid
        else:
            hi = mid
    t_s = 0.5 * (lo + hi)
    assert abs(t_e - 0.316227766017) < 5e-13
    assert abs(t_s - 0.236207526722) < 5e-13

    # Deterministic cost: any strictly decreasing map shares the argmin.
    h, w, Es = 1.0, 2.0, (1.0, 0.4, 0.1)
    js = [h * K + w * Es[K] for K in range(3)]
    k_j = min(range(3), key=lambda K: js[K])
    k_log = max(range(3), key=lambda K: math.log(10.0 - js[K]))
    k_exp = max(range(3), key=lambda K: math.exp(-js[K]))
    assert k_j == k_log == k_exp == 1

    # Linear penalty on a realized error: E[log W] can rank the higher J first.
    # A: ell in {0, 3}, E[ell]=1.5, J=1.5, W=6-ell.
    # B: hK=0.4, ell=1.2, J=1.6, W=4.4.
    elog_a = 0.5 * (math.log(6.0) + math.log(3.0))
    elog_b = math.log(4.4)
    assert 1.5 < 1.6
    assert 4.5 > 4.4
    assert elog_b > elog_a

    print("lam(0.2)=%.15f" % lam(0.2))
    print("lam(0.99)=%.15f" % lam(0.99))
    print("tau_E=%.15f" % t_e)
    print("tau_S=%.15f" % t_s)
    print("q=%.6f lean=%.6f robust=%.6f" % (q, mean_lean, mean_robust))
    print("elog_a=%.15f elog_b=%.15f" % (elog_a, elog_b))
    print("OK")


if __name__ == "__main__":
    main()
