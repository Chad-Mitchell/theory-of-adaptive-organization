#!/usr/bin/env python3
"""Checks for theory/SWARM_RULE_2026-11-23.md (join, stay, leave).

Run from the repo root:
  nice -n 19 python3 theory/swarm_checks/swarm_checks.py

These are code checks of identities and of CT9 / Lemma B1 / CT29 inside the
two-state telegraph class. They re-test proved results; they are not evidence
about cells, agents or people. Machinery failures set a nonzero exit code.
"""
from __future__ import annotations

import math
import random
import sys

from scipy.optimize import minimize_scalar

checks_failed = []


def check(name, ok, detail):
    print("CHECK %s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        checks_failed.append(name)


# Telegraph signal, symmetric switching rate lam. In drift units u = lam*t the
# chance a reading of age u is wrong is r(u) = (1 - e^{-2u})/2, r_inf = 1/2.
R_INF = 0.5
PHI = 0.25  # integral of (r_inf - r(u)) du = 1/4


def A(s):
    """Average error risk over a read interval of s drift units (CT9's A)."""
    return 0.5 - (1.0 - math.exp(-2.0 * s)) / (4.0 * s)


def part_cost(log_s, lam, share, c, w):
    """Part's cost per unit time: lam*share*c/s + w*A(s) (CT9 with a share)."""
    s = math.exp(log_s)
    return lam * share * c / s + w * A(s)


def best(lam, share, c, w):
    """Best periodic schedule, or stopping (s = inf) if that is cheaper."""
    res = minimize_scalar(part_cost, bounds=(-14, 14), method="bounded",
                          args=(lam, share, c, w))
    s, j = math.exp(res.x), res.fun
    if j < w * R_INF:
        return s, j
    return math.inf, w * R_INF


def main():
    # 1. Identity: J_i = w*[lam*c'/s + A(s)] with c' = share*c/w.
    rng = random.Random(20261123)
    worst = 0.0
    for _ in range(2000):
        lam, sh, c, w, s = (rng.uniform(0.01, 3), rng.uniform(0.05, 1),
                            rng.uniform(0.01, 3), rng.uniform(0.1, 5),
                            rng.uniform(0.01, 10))
        lhs = part_cost(math.log(s), lam, sh, c, w)
        rhs = w * (lam * (sh * c / w) / s + A(s))
        worst = max(worst, abs(lhs - rhs) / max(1.0, abs(lhs)))
    check("identity_net_share", worst < 1e-12, "max rel diff %.2e" % worst)

    # 2. Stay iff pi = lam*s*c/(w*Phi) < 1 (CT9 re-tested; code sanity only).
    mism = 0
    tested = 0
    for _ in range(2000):
        lam, sh, c, w = (10 ** rng.uniform(-2, 0.5), rng.uniform(0.05, 1),
                         10 ** rng.uniform(-2, 0.5), 10 ** rng.uniform(-1, 0.7))
        pi = lam * sh * c / (w * PHI)
        if abs(pi - 1) < 0.02:
            continue  # optimizer tolerance near the boundary
        tested += 1
        stays = math.isfinite(best(lam, sh, c, w)[0])
        mism += stays != (pi < 1)
    check("stay_iff_pi_below_1", mism == 0,
          "%d mismatches in %d draws away from pi=1" % (mism, tested))

    # 3. One index: the schedule depends on (share, c, w) only via share*c/w.
    trip = [(1, 1, 1), (0.5, 2, 1), (2, 1, 2)]
    ss = [best(0.1, a, b, d)[0] for a, b, d in trip]
    check("one_index", max(ss) - min(ss) < 1e-5,
          "s* = %s" % ", ".join("%.6f" % x for x in ss))

    # 4. Alignment: the part's schedule equals the whole's (full c, stake W)
    #    iff share = w/W; equal shares fail (CT29 alignment clause, one party).
    lam, c, W = 0.1, 1.0, 1.0
    s_whole = best(lam, 1.0, c, W)[0]
    ok = True
    rows = []
    for w in (0.2, 0.5, 0.8):
        s_al = best(lam, w / W, c, w)[0]
        s_eq = best(lam, 0.5, c, w)[0]
        rows.append("w=%.1f aligned %.6f equal-share %.6f" % (w, s_al, s_eq))
        ok &= abs(s_al - s_whole) < 1e-5
        if abs(w - 0.5) > 1e-9:
            ok &= abs(s_eq - s_whole) > 1e-3
    check("alignment_share_equals_stake_share", ok,
          "whole s* %.6f; %s" % (s_whole, "; ".join(rows)))

    # 5. Levers multiply: pi0 = 2.04; two 30% cuts and one 51% cut reach pi=1.
    pi0 = 2.04
    two30, one51, two20 = pi0 * 0.7 * 0.7, pi0 * 0.49, pi0 * 0.8 * 0.8
    check("levers_multiply", abs(two30 - 1.0) < 1e-3 and abs(one51 - 1.0) < 1e-3
          and two20 > 1.0,
          "two 30%%: %.4f, one 51%%: %.4f, two 20%%: %.4f" % (two30, one51, two20))

    # 6. Churn cliff (Lemma B1): reads per unit time f* = lam/s* rise with lam,
    #    peak, then fall steeply to 0 at lam_c = Phi/(share*c/w) = 0.25 here.
    lams = [0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.22, 0.24, 0.249, 0.251, 0.3]
    fs = []
    for lam in lams:
        s, _ = best(lam, 1.0, 1.0, 1.0)
        fs.append(0.0 if math.isinf(s) else lam / s)
    for lam, f in zip(lams, fs):
        print("  lam=%-6g reads per unit time f*=%.4f" % (lam, f))
    k = fs.index(max(fs))
    rises = all(fs[i] < fs[i + 1] for i in range(k))
    falls = all(fs[i] >= fs[i + 1] for i in range(k, len(fs) - 1))
    check("churn_cliff", rises and falls and 0 < k < len(fs) - 3
          and fs[-2] == 0.0 and fs[-1] == 0.0 and fs[-3] > 0.0,
          "peak f*=%.4f at lam=%g; f*=0 for lam>=0.251" % (fs[k], lams[k]))

    # 7. Re-form band (CL19 via FLUID_LAYERS): b*^2/sigma^2 = sqrt(6k/(w sigma^2)).
    worst = 0.0
    for _ in range(200):
        kk, ww, sg2 = rng.uniform(0.01, 10), rng.uniform(0.01, 10), rng.uniform(0.01, 10)
        b = (6 * kk * sg2 / ww) ** 0.25
        worst = max(worst, abs(b * b / sg2 - math.sqrt(6 * kk / (ww * sg2))))
    check("reform_band_lifetime", worst < 1e-12, "max abs diff %.2e" % worst)


    # 8. Tampering, derived inside the rule. The whole enforces its own optimal
    #    schedule T_W (full price c, stake W). The part may comply (cost
    #    J_i(T_W)), deviate openly (penalty e), or tamper at cost t + q*P:
    #    - enforcement tamper (signal intact): then its own best, w*g(c'), with
    #      g(c') = min(min_T lam*c'/T + A(T), r_inf);
    #    - channel tamper (signal moved, so worthless to the part): w*r_inf.
    #    Tamper gain D = J_i(T_W) - post-tamper cost. Tamper iff D > t+qP < e.
    def sched_cost(T, lam, share, c, w):
        return lam * share * c / T + w * A(T)

    lam, c, W = 0.1, 1.0, 1.0
    T_W = best(lam, 1.0, c, W)[0]
    rows = []
    ok_aligned = True
    ok_order = True
    ok_pos = True
    for w in (0.2, 0.5, 0.8):
        for share in (w / W, 0.5 * w / W, 1.5 * w / W, 2.0 * w / W, 3.0 * w / W):
            comply = sched_cost(T_W, lam, share, c, w)
            s_own, j_own = best(lam, share, c, w)
            d_enf = comply - j_own
            d_ch = comply - w * R_INF
            sig_val = w * R_INF - j_own  # what the signal is worth to the part
            ok_order &= abs((d_enf - d_ch) - sig_val) < 1e-12 and d_ch <= d_enf + 1e-15
            if abs(share - w / W) < 1e-12:
                ok_aligned &= abs(d_enf) < 1e-9
            else:
                ok_pos &= d_enf > 1e-6
            pi_i = lam * share * c / (w * PHI)
            rows.append("w=%.1f s/(w/W)=%.1f pi_i=%.2f D_enf=%.5f D_ch=%.5f" % (
                w, share * W / w, pi_i, d_enf, d_ch))
    for r in rows:
        print("  " + r)
    check("tamper_gain_zero_iff_aligned", ok_aligned and ok_pos,
          "D_enf = 0 at s = w/W and > 0 at 0.5x, 1.5x, 2x, 3x")
    check("channel_tamper_costs_signal_value", ok_order,
          "D_enf - D_ch = w*(r_inf - g) = the signal's worth to the part")

    # 9. Redundancy: N independent checks must all be moved; each costs t and
    #    each detects with chance q. Deterred iff D < N*t + (1-(1-q)^N)*P.
    w, share = 0.5, 3.0 * 0.5 / W
    D = sched_cost(T_W, lam, share, c, w) - best(lam, share, c, w)[1]
    t, q, P = 0.005, 0.1, 0.2
    deter = [N * t + (1 - (1 - q) ** N) * P for N in range(1, 11)]
    n_star = next((N for N, x in enumerate(deter, 1) if x > D), None)
    mono = all(deter[i] < deter[i + 1] for i in range(len(deter) - 1))
    check("redundancy_deterrence", mono and n_star is not None and deter[0] < D,
          "D=%.5f; deterrence N=1..10: %s; first N that deters: %s" % (
              D, ", ".join("%.4f" % x for x in deter), n_star))

    if checks_failed:
        print("FAILS %d: %s" % (len(checks_failed), ", ".join(checks_failed)))
        sys.exit(1)
    print("FAILS 0")
    print("ALL SWARM CHECKS PASS")


if __name__ == "__main__":
    main()
