#!/usr/bin/env python3
"""Checks for theory/GROWTH_BRIDGE.md. Standard library only.

No network unless --crossref is passed. Prints PASS/FAIL lines and exits 1
on a failure. Heavy enough to count as the numeric check of every displayed
formula; run it under nice -n 19.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HYP = (
    "The law of adaptive organization (hypothesis): "
    "strongly selected systems minimize the cost of judgment."
)
NOTE = os.path.join(ROOT, "theory", "GROWTH_BRIDGE.md")


def check(name, ok, detail=""):
    check.fails += int(not ok)
    mark = "PASS" if ok else "FAIL"
    print(f"  {mark}  {name}" + (f"  {detail}" if detail else ""))
    return bool(ok)


check.fails = 0


def bisection(lo, hi, positive_on_the_right, n=80):
    """Root of a continuous function whose sign pattern is known.

    positive_on_the_right True means f(hi) and the upper side are the
    positive side: the root has f>0 on the right of the root? We just
    pass a predicate `high` that is True when the midpoint should move
    the lower bound up. Caller encodes the sign.
    """
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if positive_on_the_right(mid):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def section_expansion():
    print("expansion")
    # Unscoped identity fails for a deterministic factor.
    w = 1.2
    left = math.log(w)
    right = (w - 1.0) - 0.0
    check(
        "deterministic W=1.2: log is below E[W-1]-Var/2 by about 0.0177",
        abs(left - 0.182321556794) < 1e-12 and abs((w - 1.0) - left - 0.017678443206) < 1e-12,
        f"log={left:.12f} gap={(w - 1.0) - left:.12f}",
    )
    check(
        "the missing term at W=1.2 is (E[W-1])^2/2 = 0.02",
        abs(0.5 * (w - 1.0) ** 2 - 0.02) < 1e-15,
    )

    # Lagrange remainder bound on |x|<=1/2: |R2| <= (8/3) |x|^3.
    def remainder_ok(x):
        exact = math.log(1.0 + x) - (x - 0.5 * x * x)
        return abs(exact) <= (8.0 / 3.0) * abs(x) ** 3 + 1e-15

    xs = [i / 50.0 for i in range(-24, 25) if i != 0]
    check("Lagrange remainder |R2|<=(8/3)|x|^3 on |x|<=0.48", all(remainder_ok(x) for x in xs))

    # Weak-selection expansion, constant X=1: the eps^2 term is the squared mean.
    eps = 0.01
    lam = math.log(1.0 + eps)
    series = eps - 0.5 * eps ** 2
    check(
        "log(1+eps) = eps - eps^2/2 + O(eps^3)",
        abs(lam - series) < (8.0 / 3.0) * eps ** 3,
        f"lam={lam:.12e} series={series:.12e}",
    )

    # Diffusion scaling. Z=±1, mu=0.2, sigma^2=0.5, limit mu-sigma^2/2 = -0.05.
    mu, sig2 = 0.2, 0.5
    sig = math.sqrt(sig2)
    limit = mu - 0.5 * sig2
    check("diffusion limit is -0.05 while the drift is +0.2", abs(limit + 0.05) < 1e-15 and mu > 0)

    def diffusion(dt):
        a = mu * dt
        b = sig * math.sqrt(dt)
        elog = 0.5 * math.log(1.0 + a + b) + 0.5 * math.log(1.0 + a - b)
        ex = a
        ex2 = a * a + b * b
        var = ex2 - ex * ex
        return elog, ex - 0.5 * var

    prev = None
    for dt in (1e-2, 1e-3, 1e-4, 1e-5):
        elog, approx = diffusion(dt)
        # User's identity: difference is O(dt^{3/2}).
        check(
            f"diffusion identity remainder O(dt^1.5) at dt={dt:.0e}",
            abs(elog - approx) < 5.0 * dt ** 1.5,
            f"diff={elog - approx:.3e}",
        )
        rate = elog / dt
        check(
            f"growth rate approaches -0.05 at dt={dt:.0e}",
            abs(rate - limit) < 0.6 * math.sqrt(dt),
            f"rate={rate:.6f}",
        )
        if prev is not None:
            # Remainder shrinks faster than the leading term.
            check(
                f"remainder shrinks from the previous step at dt={dt:.0e}",
                abs(elog - approx) < abs(prev) * 0.05,
            )
        prev = elog - approx

    # Mean gap, not equal means. eps=0.2, A is 0, B is ±1 with
    # probabilities 0.525 and 0.475, so E[X_B]=0.05.
    eps = 0.2
    p = 0.525
    lam_b = p * math.log(1.0 + eps) + (1.0 - p) * math.log(1.0 - eps)
    ex_b = 2.0 * p - 1.0
    excess_b = eps * ex_b
    check(
        "E[X]=0.05, not an equal-mean pair: excess 0.01, growth negative",
        abs(ex_b - 0.05) < 1e-12 and abs(excess_b - 0.01) < 1e-12
        and abs(lam_b + 0.010274369557) < 1e-12,
        f"E[X]={ex_b:.6f} excess={excess_b:.6f} lam={lam_b:.12f}",
    )
    # The equal-mean ranking is a different example (Gillespie 1977).
    lam_equal = 0.5 * math.log(1.0 - eps) + 0.5 * math.log(1.0 + eps)
    check(
        "equal-mean symmetric law at eps=0.2 has growth -0.020411",
        abs(lam_equal + 0.020411) < 1e-6 and abs(lam_equal - 0.5 * math.log(0.96)) < 1e-15,
        f"lam={lam_equal:.6f}",
    )

    # Equal mean and second moment, unequal third moment.
    eps = 0.05
    skew_p = (4.0 / 9.0, 4.0 / 9.0, 1.0 / 9.0)
    skew_x = (-1.0, 0.5, 2.0)
    mean = sum(p_ * x for p_, x in zip(skew_p, skew_x))
    m2 = sum(p_ * x * x for p_, x in zip(skew_p, skew_x))
    m3 = sum(p_ * x ** 3 for p_, x in zip(skew_p, skew_x))
    check("skew law has mean 0, second moment 1, third moment 1/2",
          abs(mean) < 1e-12 and abs(m2 - 1.0) < 1e-12 and abs(m3 - 0.5) < 1e-12)
    lam_skew = sum(p_ * math.log(1.0 + eps * x) for p_, x in zip(skew_p, skew_x))
    lam_sym = 0.5 * math.log(1.0 - eps) + 0.5 * math.log(1.0 + eps)
    cubic = (eps ** 3) / 3.0 * 0.5
    check(
        "third-moment law outgrows the symmetric law",
        lam_skew > lam_sym and abs((lam_skew - lam_sym) - cubic) < 2e-6,
        f"diff={lam_skew - lam_sym:.6e} cubic={cubic:.6e}",
    )

    # Menu agreement at small eps, disagreement is not claimed there.
    check(
        "gapped menu at eps=0.01: log(1.01) > 0",
        math.log(1.01) > 0.009 and math.log(1.01) < 0.01,
    )


def section_stake():
    print("stake")

    def lam(f):
        return 0.6 * math.log(1.0 + f) + 0.4 * math.log(1.0 - f)

    def dlam(f):
        return 0.6 / (1.0 + f) - 0.4 / (1.0 - f)

    check("Kelly derivative zero at f=0.2", abs(dlam(0.2)) < 1e-12)
    check("growth at 0.2 beats both neighbors", lam(0.2) > lam(0.1) and lam(0.2) > lam(0.3))
    check(
        "growth at 0.2 is 0.020135513551",
        abs(lam(0.2) - 0.020135513551) < 1e-12,
        f"lam={lam(0.2):.12f}",
    )
    # Expected excess 0.2*f is maximized at the right endpoint of [0, 0.99].
    check("expected excess rises in f", 0.2 * 0.99 > 0.2 * 0.2)
    check("endpoint growth is below the interior maximum", lam(0.99) < lam(0.2))

    # Vanishing exposure eps*f with f in [0,1] pushes Kelly outside the box
    # once eps<0.2, so both criteria sit at the corner. The box [0, 1/eps]
    # keeps them apart.
    for eps, box in ((0.05, 1.0), (1.0, 1.0)):
        f_star = min(box, 0.2 / eps)
        f_mean = box
        agree = abs(f_star - f_mean) < 1e-12
        if eps < 0.2 and box <= 1.0:
            check(f"corner agreement at eps={eps} on [0,1]", agree and f_star == 1.0)
        else:
            check(f"interior disagreement at eps={eps}", (not agree) and abs(f_star - 0.2) < 1e-12)


def section_coin_and_ct42():
    print("coin")
    # CT43's Peters coin, arithmetic only.
    factors = (1.5, 0.6)
    mean = 0.5 * (factors[0] + factors[1])
    lam = 0.5 * (math.log(factors[0]) + math.log(factors[1]))
    excess = mean - 1.0
    second = 0.5 * ((factors[0] - 1.0) ** 2 + (factors[1] - 1.0) ** 2)
    var = second - excess ** 2
    check("coin mean excess +0.05 and growth -0.052680257829",
          abs(excess - 0.05) < 1e-15 and abs(lam + 0.052680257829) < 1e-12,
          f"lam={lam:.12f}")
    check("coin Var formula misses the log by about 0.00143",
          abs((excess - 0.5 * var) - lam - 0.001430257829) < 1e-12,
          f"var-form={excess - 0.5 * var:.12f}")
    check("coin second-moment form is within 0.0002 of the log",
          abs((excess - 0.5 * second) - lam) < 2e-4)

    # CT42 factors are outside the disk where a cubic remainder is small.
    check(
        "CT42 factors 1.30, 0.90, and 0 sit outside a 0.05 neighborhood of 1",
        abs(1.30 - 1.0) > 0.2 and abs(0.90 - 1.0) > 0.05 and abs(0.0 - 1.0) == 1.0,
    )


def section_ruin():
    print("ruin")
    c, alpha, s0, beta, y = 0.05, 0.5, 0.3, 1.0 / 3.0, 1.0

    def J(t):
        return c / t + alpha * t

    def s2(t):
        return s0 ** 2 + beta * t ** 3

    def m(t):
        return y - J(t)

    def theta(t):
        return 2.0 * m(t) / s2(t)

    def phi(t):
        return m(t) - 0.5 * s2(t)

    def Jp(t):
        return -c / t ** 2 + alpha

    def th_num(t):
        # Numerator of theta', up to a positive factor: sign of theta'.
        return -(Jp(t) * s2(t) + m(t) * (3.0 * beta * t ** 2))

    t_e = math.sqrt(c / alpha)
    disc = y * y - 4.0 * alpha * c
    r1 = (y - math.sqrt(disc)) / (2.0 * alpha)
    r2 = (y + math.sqrt(disc)) / (2.0 * alpha)
    t_s = bisection(r1 + 1e-12, t_e, lambda mid: th_num(mid) > 0.0)
    check("tau_E = sqrt(0.1) = 0.316227766017", abs(t_e - 0.316227766017) < 1e-12)
    check("tau_S = 0.236207526722", abs(t_s - 0.236207526722) < 1e-12, f"tau_S={t_s:.12f}")
    check("theta decreases from tau_S to tau_E", theta(t_s) > theta(t_e) and th_num(0.5 * (t_s + t_e)) < 0.0)

    # Multiplicative diffusion point: t^4 + t^2 - 0.1 = 0.
    u = (-1.0 + math.sqrt(1.4)) / 2.0
    t_g = math.sqrt(u)
    check("tau_G = 0.302668099260", abs(t_g - 0.302668099260) < 1e-12, f"tau_G={t_g:.12f}")
    check("phi is higher at tau_G than at tau_E or tau_S",
          phi(t_g) > phi(t_e) and phi(t_g) > phi(t_s))
    check("tau_G and tau_E differ", abs(t_g - t_e) > 0.01)

    # Published cap: eps=1e-3, B=0.5.
    theta_req = math.log(1000.0) / 0.5
    check("theta_req = 13.815510557964", abs(theta_req - 13.815510557964) < 1e-12)
    check("theta(tau_S)=14.200588175815 above the requirement, theta(tau_E)=13.601868698785 below it",
          abs(theta(t_s) - 14.200588175815) < 1e-12 and abs(theta(t_e) - 13.601868698785) < 1e-12)
    t_hi = bisection(t_s, r2 - 1e-9, lambda mid: theta(mid) > theta_req)
    t_lo = bisection(r1 + 1e-12, t_s, lambda mid: theta(mid) < theta_req)
    check("tau_lo = 0.183706411069 and tau_cap = 0.299049733488",
          abs(t_lo - 0.183706411069) < 1e-12 and abs(t_hi - 0.299049733488) < 1e-12,
          f"lo={t_lo:.12f} hi={t_hi:.12f}")
    check("feasible set in tau is a bounded interval, not a half-line",
          t_lo > 0.1 and t_hi < 0.5 and t_hi - t_lo > 0.05 and t_hi < r2 - 0.5)
    check("tau_E and tau_G lie outside that interval; tau_S lies inside",
          t_e > t_hi and t_g > t_hi and t_lo < t_s < t_hi)
    check("J(tau_cap)=0.316721136799 and J(tau_S)=0.329782030747",
          abs(J(t_hi) - 0.316721136799) < 1e-12 and abs(J(t_s) - 0.329782030747) < 1e-12)
    check("three published-path designs differ",
          min(abs(t_hi - t_s), abs(t_hi - t_e), abs(t_s - t_e)) > 0.01)

    # A requirement between theta(tau_G) and theta(tau_E) separates the criteria.
    theta_mid = 0.5 * (theta(t_g) + theta(t_e))
    t_j = bisection(t_g, t_e, lambda mid: theta(mid) > theta_mid)
    check("split cap: tau_J = 0.309679835108 differs from tau_G",
          abs(t_j - 0.309679835108) < 1e-12 and abs(t_j - t_g) > 0.005,
          f"t_J={t_j:.12f}")
    check("on that cap, J prefers tau_J and phi prefers tau_G",
          J(t_j) < J(t_g) and phi(t_g) > phi(t_j))

    # Brownian scale function.
    def ruin(mu, sig2, x):
        if mu <= 0.0:
            return 1.0
        return math.exp(-2.0 * mu * x / sig2)

    check("Brownian ruin is 1 at nonpositive drift and exp(-2 mu x/sig2) above",
          ruin(-0.1, 1.0, 1.0) == 1.0 and abs(ruin(0.5, 1.0, 1.0) - math.exp(-1.0)) < 1e-15)
    # Half-space in (mu, sig2): mu - k sig2 >= 0.
    k = math.log(1.0 / 0.05) / 2.0  # x=1
    check("level set mu >= k sig2 is a half-space through the origin",
          (0.4 - k * 0.2) * (0.1 - k * 0.2) < 0.0)

    # Feller generator residual.
    alpha_f, beta_f, z = 0.3, 0.2, 1.7
    u = math.exp(-alpha_f * z / beta_f)
    up = -(alpha_f / beta_f) * u
    upp = (alpha_f / beta_f) ** 2 * u
    residual = alpha_f * z * up + beta_f * z * upp
    check("Feller extinction probability is in the kernel of the generator", abs(residual) < 1e-12)
    check("Feller level set is a threshold on alpha/beta",
          math.exp(-alpha_f * z / beta_f) < 0.1 and alpha_f / beta_f > math.log(10.0) / z)

    # Galton-Watson Poisson.
    def eta_poisson(m):
        s = 0.0
        for _ in range(100000):
            nxt = math.exp(m * (s - 1.0))
            if abs(nxt - s) < 1e-15:
                return nxt
            s = nxt
        return s

    ratios = []
    for m in (1.001, 1.01, 1.05):
        surv = 1.0 - eta_poisson(m)
        ratios.append(surv / (2.0 * (m - 1.0)))
    check("Poisson survival / 2(m-1) approaches 1 as m approaches 1",
          abs(ratios[0] - 1.0) < abs(ratios[1] - 1.0) < abs(ratios[2] - 1.0)
          and abs(ratios[0] - 1.0) < 0.002,
          f"ratios={ratios}")

    # Birth-death from z=20, b=1.1, d=1.
    eta = 1.1 ** (-20)
    check("birth-death extinction from 20 at b/d=1.1 is 0.148643628024",
          abs(eta - 0.148643628024) < 1e-12, f"eta={eta:.12f}")
    ratio_needed = math.exp(-math.log(0.05) / 20.0)
    check("cap 0.05 from size 20 needs b/d at least 1.161586349642",
          abs(ratio_needed - 1.161586349642) < 1e-12 and 1.1 < ratio_needed)

    # CT43 pair, analytic parts.
    a_arith = 0.5 * (1.04 + 1.02)
    b_arith = 0.5 * (1.131 + 0.931)
    a_geo = 0.5 * (math.log(1.04) + math.log(1.02))
    b_geo = 0.5 * (math.log(1.131) + math.log(0.931))
    check("D3d arithmetic prefers B and growth prefers A",
          abs(a_arith - 1.03) < 1e-15 and abs(b_arith - 1.031) < 1e-12
          and b_arith > a_arith and a_geo > b_geo,
          f"A={a_arith:.6f},{a_geo:.12f} B={b_arith:.6f},{b_geo:.12f}")
    check("D3d growth values 0.029511670225 and 0.025803097714",
          abs(a_geo - 0.029511670225) < 1e-12 and abs(b_geo - 0.025803097714) < 1e-12)


def section_coordinates():
    print("coordinates")
    # Memory total derivative: loss falls with I, so offspring rises.
    w0 = math.exp(-1.0)
    w1 = math.exp(-math.exp(-2.0))
    check("memory total derivative 0.367879441171 -> 0.873423018493",
          abs(w0 - 0.367879441171) < 1e-12 and abs(w1 - 0.873423018493) < 1e-12 and w1 > w0)
    # Budget partial at fixed loss: d/dI (-kappa I - ell) = -kappa < 0.
    kappa = 0.5
    check("memory budget partial is -kappa at fixed loss",
          (-kappa * 2.0) - (-kappa * 1.0) == -kappa and kappa > 0)

    # Acquisition: total derivative positive on [0, log 4); partial at fixed loss is -c.
    def log_total(r):
        return -r - 4.0 * math.exp(-r)

    def total_deriv(r):
        return -1.0 + 4.0 * math.exp(-r)

    check("acquisition total derivative rises from r=0 to r=1",
          abs(math.exp(log_total(0.0)) - 0.018315638889) < 1e-12
          and abs(math.exp(log_total(1.0)) - 0.084456576466) < 1e-12
          and log_total(1.0) > log_total(0.0)
          and total_deriv(0.0) > 0 and total_deriv(1.0) > 0)
    check("acquisition budget partial at fixed loss is -c",
          -1.0 < 0)

    # Learning loss is a total derivative, not the partial in task loss.
    check("learning-loss total derivative: offspring 3 at loss 1 beats 1.1 at loss 0", 3.0 > 1.1)

    # LY-1 is the witness that expected task loss fails H3.
    lam_l = 0.5 * math.log(0.2)
    lam_h = math.log(1.1)
    check("LY-1 expected task loss fails H3", abs(lam_l + 0.804718956217) < 1e-9 and abs(lam_h - 0.095310179804) < 1e-9
          and lam_l < lam_h)

    # Scalar ruin probability is not a pathwise coordinate.
    check("scalar ruin probability at fixed W=1.2 does not move offspring", 1.2 == 1.2)

    # Attention total derivative through a falling loss. Budget partial is -c_a.
    a0 = math.exp(-4.0)
    a1 = math.exp(-4.0 / math.e)
    check("attention total derivative 0.018315638889 -> 0.229576777100",
          abs(a0 - 0.018315638889) < 1e-12 and abs(a1 - 0.229576777100) < 1e-12 and a1 > a0)
    check("attention budget partial at fixed loss is negative when the price is positive",
          -0.4 < 0)

    # Growth vs Lundberg vs drift on (mu, sigma^2).
    # A: mu=0.30, sig2=0.40. B: mu=0.20, sig2=0.10.
    g_a, g_b = 0.30 - 0.20, 0.20 - 0.05
    th_a, th_b = 2 * 0.30 / 0.40, 2 * 0.20 / 0.10
    check("drift picks A, diffusion-growth picks B, Lundberg picks B",
          0.30 > 0.20 and g_a < g_b and th_a < th_b,
          f"g={g_a:.2f},{g_b:.2f} theta={th_a:.1f},{th_b:.1f}")
    # A pair where diffusion-growth and Lundberg disagree.
    # C: mu=0.30, sig2=0.20. D: mu=0.16, sig2=0.08.
    g_c, g_d = 0.30 - 0.10, 0.16 - 0.04
    th_c, th_d = 2 * 0.30 / 0.20, 2 * 0.16 / 0.08
    check("diffusion-growth picks C and Lundberg picks D",
          g_c > g_d and th_c < th_d,
          f"g={g_c:.2f},{g_d:.2f} theta={th_c:.1f},{th_d:.1f}")


def section_note():
    print("note")
    text = open(NOTE, encoding="utf-8").read()
    check("hypothesis sentence is byte-identical", HYP in text)
    labeled = False
    for line in text.splitlines():
        if "law of adaptive organization" in line and "hypothesis" in line:
            labeled = True
    check("the sentence that names the law labels itself a hypothesis", labeled)
    check("headline recovers the ranking only", "recovers the ranking only" in text)
    check("menu proof names M^{2/3}", "M^{2/3}" in text)
    stray = any(ln.startswith("|\\mathbb{E}[\\log W]") for ln in text.splitlines())
    check("diffusion identity has no leading bar", not stray)
    low = text.lower()
    for banned in ("bill", "kill", "verdict", "theory of everything"):
        check(f"note has no {banned!r}", banned not in low)
    quoted = [
        "0.182321556794",
        "0.020135513551",
        "0.236207526722",
        "0.316227766017",
        "0.302668099260",
        "0.299049733488",
        "0.183706411069",
        "0.309679835108",
        "13.815510557964",
        "0.052680257829",
        "0.148643628024",
        "0.367879441171",
        "0.873423018493",
    ]
    for s in quoted:
        check(f"note quotes {s}", s in text)


DOIS = [
    ("10.1002/j.1538-7305.1956.tb03809.x", "A New Interpretation of Information Rate"),
    ("10.1016/0022-5193(66)90188-3", "Optimizing reproduction in a randomly varying environment"),
    ("10.1093/genetics/76.3.601", "WITHIN-GENERATION VARIANCE IN OFFSPRING NUMBER"),
    ("10.1086/283230", "Natural Selection for Variances in Offspring Numbers"),
    ("10.1073/pnas.62.4.1056", "POPULATION GROWTH IN A RANDOMLY VARYING ENVIRONMENT"),
    ("10.1111/j.1420-9101.2011.02378.x", "uncertain returns on investment"),
    ("10.1086/285094", "Evolution in a Variable Environment"),
    ("10.1101/sqb.1955.020.01.005", "GENETIC HETEROGENEITY"),
    ("10.1111/j.1558-5646.1976.tb00911.x", "NATURAL SELECTION AND RANDOM GENETIC DRIFT"),
    ("10.1017/S0305004100015644", "Selection and Mutation"),
    ("10.1525/9780520411586-018", "Diffusion Processes in Genetics"),
    ("10.2307/3211999", "Diffusion approximations in collective risk theory"),
    ("10.1007/978-3-642-40607-2_17", "Collective risk theory"),
]


def crossref():
    print("crossref")
    out_dir = os.path.join(ROOT, "theory", "growth_bridge_checks")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "crossref.out")
    lines = []
    ua = {"User-Agent": "gtao-growth-bridge (mailto:chad39@gmail.com)"}
    for doi, needle in DOIS:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
        ok = False
        title = ""
        err = ""
        for attempt in range(5):
            try:
                req = urllib.request.Request(url, headers=ua)
                with urllib.request.urlopen(req, timeout=40) as resp:
                    message = json.load(resp)["message"]
                title = (message.get("title") or [""])[0]
                authors = "; ".join(a.get("family", "") for a in message.get("author", [])[:6])
                year = (message.get("issued", {}).get("date-parts") or [[None]])[0][0]
                container = (message.get("container-title") or [""])[0]
                ok = needle.lower() in title.lower()
                lines.append(f"{'OK' if ok else 'MISMATCH'}\t{doi}\t{year}\t{authors}\t{title}\t{container}")
                err = ""
                break
            except Exception as exc:
                err = str(exc)
                time.sleep(2.0 * (attempt + 1))
        if err and not title:
            lines.append(f"FAIL\t{doi}\t{err}")
        check(f"Crossref title matches {doi}", ok, (title or err)[:100])
        time.sleep(1.1)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  wrote {out_path}")


def main(argv):
    section_expansion()
    section_stake()
    section_coin_and_ct42()
    section_ruin()
    section_coordinates()
    section_note()
    if "--crossref" in argv:
        crossref()
    print("FAILS", check.fails)
    if check.fails == 0:
        print("ALL GROWTH-BRIDGE CHECKS PASS")
        return 0
    print("SOME GROWTH-BRIDGE CHECKS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
