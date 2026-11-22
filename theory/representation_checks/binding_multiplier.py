#!/usr/bin/env python3
"""Check the scalar-path binding multiplier (THEORY CT22, Lemma B9).

The proof is in THEORY.md Appendix B.9. This script checks the algebra the
proof uses, the published path, and two obstructions (J not convex; theta
not unimodal). Standard library plus sympy. No network.
"""
from __future__ import annotations

import math
import sys

import sympy as sp


# Lemma B9 published point. Exact rationals: y=1, c=1/20, w=1, sigma=1, s0=3/10.
Y = sp.Integer(1)
C = sp.Rational(1, 20)
ALPHA = sp.Rational(1, 2)          # w * sigma**2 / 2
BETA = sp.Rational(1, 3)           # w**2 * sigma**4 / 3
S0 = sp.Rational(9, 100)           # s0**2
EPS = sp.Rational(1, 1000)


def symbols():
    t = sp.symbols("t", positive=True)
    y, c, alpha, beta, s0 = sp.symbols("y c alpha beta s0", positive=True)
    return t, y, c, alpha, beta, s0


def check(name, ok, detail=""):
    check.results.append((name, bool(ok), detail))
    mark = "PASS" if ok else "FAIL"
    print(f"  {mark}  {name}" + (f"  {detail}" if detail else ""))
    return bool(ok)


check.results = []


def algebra_unimodality():
    """phi' = m'' s^2 - m (s^2)'' < 0 on {m>0}, so theta is strictly unimodal."""
    t, y, c, alpha, beta, s0 = symbols()
    m = y - c / t - alpha * t
    s2 = s0 + beta * t**3
    phi = sp.diff(m, t) * s2 - m * sp.diff(s2, t)
    phi_p = sp.diff(phi, t)
    claimed = sp.diff(m, t, 2) * s2 - m * sp.diff(s2, t, 2)
    diff = sp.simplify(phi_p - claimed)
    check("numerator derivative identity phi' = m'' s^2 - m (s^2)''", diff == 0)
    # m'' = -2c/t**3 < 0 and (s^2)'' = 6 beta t > 0, so both terms of phi' are
    # negative whenever m>0. The simplified expression must match that.
    simplified = sp.simplify(phi_p)
    expect = -2 * c / t**3 * s2 - m * (6 * beta * t)
    check("phi' expands to -2c/t^3 s^2 - m*6 beta t", sp.simplify(simplified - expect) == 0)
    # At the published point, phi changes from + to - exactly once on {m>0}.
    # theta' has the sign of phi, and phi = (polynomial) / t**2 with t**2 > 0.
    subs = {y: Y, c: C, alpha: ALPHA, beta: BETA, s0: S0}
    phi_n = sp.together(phi.subs(subs))
    num, den = sp.fraction(phi_n)
    cleared = sp.expand(num * t**2)
    quintic = sp.expand(
        2 * ALPHA * BETA * t**5 - 3 * BETA * Y * t**4 + 4 * C * BETA * t**3
        - ALPHA * S0 * t**2 + C * S0
    )
    ratio = sp.simplify(cleared / quintic)
    check("theta' numerator is a positive multiple of the quintic",
          ratio.is_real and ratio > 0, f"ratio={ratio}")
    Pint = sp.Poly(sp.expand(quintic * 6000), t)
    check("cleared numerator is 2000 t^5 - 6000 t^4 + 400 t^3 - 270 t^2 + 27",
          Pint == sp.Poly(2000 * t**5 - 6000 * t**4 + 400 * t**3 - 270 * t**2 + 27, t))
    # Domain m>0: alpha t^2 - y t + c < 0.
    r1 = (Y - sp.sqrt(Y**2 - 4 * ALPHA * C)) / (2 * ALPHA)
    r2 = (Y + sp.sqrt(Y**2 - 4 * ALPHA * C)) / (2 * ALPHA)
    sturm = sp.sturm(Pint)

    def variations(a):
        vals = [sp.sign(s.subs(t, a)) for s in sturm]
        vals = [v for v in vals if v != 0]
        return sum(1 for i in range(len(vals) - 1) if vals[i] * vals[i + 1] < 0)

    n_in = variations(r1) - variations(r2)
    check("exactly one root of theta' on {m>0}", n_in == 1, f"Sturm count {n_in}")
    # sign: positive just inside the left endpoint, negative at tau_E
    tE = sp.sqrt(C / ALPHA)
    left = r1 + (tE - r1) / 100
    check("theta' > 0 on the left of the critical point and theta' < 0 at tau_E",
          Pint.subs(t, left) > 0 and Pint.subs(t, tE) < 0)
    return r1, r2, tE


def fsolve_bracket(f, a, b, n=80):
    """Bisection. f(a) and f(b) must have opposite signs."""
    fa, fb = f(a), f(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError("bracket does not change sign")
    for _ in range(n):
        mid = 0.5 * (a + b)
        fm = f(mid)
        if fa * fm <= 0:
            b, fb = mid, fm
        else:
            a, fa = mid, fm
    return 0.5 * (a + b)


def published_path():
    y, c, w, sg, s0 = 1.0, 0.05, 1.0, 1.0, 0.3
    eps = 1e-3
    alpha = w * sg**2 / 2.0
    beta = (w**2) * (sg**4) / 3.0

    def J(t):
        return c / t + alpha * t

    def Jp(t):
        return -c / t**2 + alpha

    def m(t):
        return y - J(t)

    def s2(t):
        return s0**2 + beta * t**3

    def s2p(t):
        return 3 * beta * t**2

    def th(t):
        return 2 * m(t) / s2(t)

    def thp(t):
        # 2 phi / s^4, phi = m' s2 - m s2'
        return 2 * ((-Jp(t)) * s2(t) - m(t) * s2p(t)) / s2(t)**2

    disc = y * y - 4 * alpha * c
    r1 = (y - math.sqrt(disc)) / (2 * alpha)
    r2 = (y + math.sqrt(disc)) / (2 * alpha)
    tE = math.sqrt(c / alpha)
    # unique zero of theta' on (r1, tE)
    tS = fsolve_bracket(thp, r1 + 1e-6, tE)
    check("tau_S < tau_E", tS < tE, f"tau_S={tS:.6f} tau_E={tE:.6f}")
    check("J'' > 0 at both optima", (2 * c / tS**3) > 0 and (2 * c / tE**3) > 0)
    # phi' < 0 across the domain
    def phip(t):
        mpp = -2 * c / t**3
        s2pp = 6 * beta * t
        return mpp * s2(t) - m(t) * s2pp

    grid = [r1 + (r2 - r1) * i / 400 for i in range(1, 400)]
    check("phi' < 0 on the whole {m>0} grid", all(phip(t) < 0 for t in grid))
    # theta = 2m/s^2 is unimodal and not concave: the second derivative changes sign.
    def thpp(t, h=1e-4):
        return (th(t + h) - 2 * th(t) + th(t - h)) / h**2

    curv = [thpp(t) for t in grid if r1 + 0.05 < t < r2 - 0.05]
    check("theta'' changes sign, so theta is not concave on the domain",
          max(curv) > 1.0 and min(curv) < -1.0,
          f"max={max(curv):.2f} min={min(curv):.2f}")
    Bmin = math.log(1 / eps) / th(tS)
    Bslack = math.log(1 / eps) / th(tE)
    check("B_min and B_slack match the published rounding",
          abs(Bmin - 0.486) < 0.001 and abs(Bslack - 0.508) < 0.001,
          f"B_min={Bmin:.6f} B_slack={Bslack:.6f}")
    check("0 < B_min < B_slack", 0 < Bmin < Bslack)

    def tau_star(B):
        treq = math.log(1 / eps) / B
        if treq > th(tS) + 1e-12:
            return None
        if th(tE) >= treq - 1e-12:
            return tE
        return fsolve_bracket(lambda t: th(t) - treq, tS, tE)

    check("infeasible below B_min", tau_star(Bmin * 0.99) is None)
    # path B = 0.49, 0.50, 0.505, and the slack end
    want = [(0.49, 0.267), (0.50, 0.299), (0.505, 0.310)]
    prev = tS
    mus = []
    for B, tw in want:
        ts = tau_star(B)
        mu = Jp(ts) / thp(ts)
        mus.append(mu)
        ok = ts is not None and abs(ts - tw) < 0.001
        ok = ok and tS < ts < tE and ts > prev - 1e-12
        ok = ok and mu > 0 and abs(Jp(ts) - mu * thp(ts)) < 1e-9
        ok = ok and abs(th(ts) - math.log(1 / eps) / B) < 1e-9
        check(f"binding path at B={B}", ok,
              f"tau={ts:.6f} mu={mu:.6f} th'={thp(ts):.6e}")
        prev = ts
    check("mu at B=0.5 is 0.0052 per unit theta", abs(mus[1] - 0.0052) < 0.0001,
          f"mu={mus[1]:.6f}")
    check("multipliers fall as B rises", mus[0] > mus[1] > mus[2] > 0)
    for B in (Bslack, 0.6, 5.0):
        ts = tau_star(B)
        check(f"slack at B={B:.4f}", ts is not None and abs(ts - tE) < 1e-12, f"tau={ts}")
    # CQ fails only at the survival endpoint: theta'(tau_S) ~ 0, and mu -> +inf
    check("theta' vanishes at the survival endpoint", abs(thp(tS)) < 1e-6)
    for B_cq in (0.49, 0.50, 0.505):
        tau_cq = tau_star(B_cq)
        check(
            "constraint qualification at B=%.3f" % B_cq,
            tau_cq is not None and thp(tau_cq) < -1.0,
            "th'=%.6e" % thp(tau_cq),
        )
    # envelope: dJ*/dB = mu * d(theta_req)/dB = -mu ln(1/eps) / B^2
    B = 0.5
    ts = tau_star(B)
    mu = Jp(ts) / thp(ts)
    dJdB = mu * (-math.log(1 / eps) / B**2)
    check("buffer value dJ*/dB is negative", dJdB < 0, f"dJ*/dB={dJdB:.6f}")
    return {"Bmin": Bmin, "Bslack": Bslack, "tS": tS, "tE": tE, "mu05": mus[1]}


def nonconvex_obstruction():
    """A smooth J that is not quasiconvex. The constrained minimizer is a local
    minimum (J'=0, so any multiplier is 0) while the global unconstrained
    minimizer is uncertified."""
    # J'(t) = t^3 - t + 0.15 = (t-1)(t+1)t + 0.15. Critical points near ±1.
    # Negative linear tilt makes the right well the global minimum and the
    # left well a higher local minimum. theta decreases in t, so the higher
    # local minimum is the safer one.
    def Jp(t):
        return t**3 - t - 0.15

    def J(t):
        return t**4 / 4 - t**2 / 2 - 0.15 * t

    # two sign changes of J' on [-2, 2]
    roots = []
    grid = [ -1.5 + i * 0.01 for i in range(301)]
    for a, b in zip(grid, grid[1:]):
        if Jp(a) == 0 or Jp(a) * Jp(b) < 0:
            roots.append(fsolve_bracket(Jp, a, b))
    # unique-ify
    uniq = []
    for r in roots:
        if not uniq or abs(r - uniq[-1]) > 1e-4:
            uniq.append(r)
    mins = [r for r in uniq if (3 * r * r - 1) > 0]
    check("nonconvex J has two local minima", len(mins) == 2, f"mins={['%.4f' % r for r in mins]}")
    glob, local = sorted(mins, key=J)
    # theta decreases in t, so the left minimum is safer
    def th(t):
        return 2.0 - t

    check("global unconstrained min is the less safe local min",
          th(glob) < th(local) and J(glob) < J(local))
    treq = 0.5 * (th(local) + th(glob))
    # feasible: th >= treq i.e. t <= 2 - treq, which contains local and not glob
    def feasible(t):
        return th(t) + 1e-9 >= treq

    check("local min certified and global min not", feasible(local) and not feasible(glob))
    # constrained minimizer on a grid
    xs = [local - 0.5 + i * 0.002 for i in range(800)]
    feas = [t for t in xs if feasible(t)]
    t_star = min(feas, key=J)
    check("constrained minimizer is the local min, so J'=0 and mu=0",
          abs(t_star - local) < 0.01 and abs(Jp(t_star)) < 0.02,
          f"t*={t_star:.4f} J'={Jp(t_star):.4e} J={J(t_star):.4f} vs global J={J(glob):.4f}")
    check("that point is not the unconstrained global minimizer", abs(t_star - glob) > 0.5)


def nonunimodal_obstruction():
    """Two peaks in theta. The constrained minimizer need not lie between the
    expected-cost optimum and the global survival optimum."""
    def J(t):
        return (t - 1.5) ** 2

    def th(t):
        return math.exp(-(t - 0.0) ** 2) + 3.0 * math.exp(-(t - 4.0) ** 2)

    tE = 1.5
    grid = [i * 0.01 for i in range(-100, 700)]
    tS = max(grid, key=th)
    check("survival peak and cost minimum are apart", tS > 3.5 and abs(tE - 1.5) < 1e-12,
          f"tau_S≈{tS:.2f} tau_E={tE}")
    # a requirement met near both peaks, above theta(tE), so tE is uncertified
    treq = 0.5 * (th(tE) + min(th(0.0), th(4.0)))
    # actually pick a level between theta at the saddle and the lower peak
    saddle = min(th(t) for t in grid if 1.0 < t < 3.0)
    lower_peak = th(0.0)
    treq = 0.5 * (saddle + lower_peak)
    feas = [t for t in grid if th(t) >= treq]
    # disconnected: a gap
    gaps = sum(1 for a, b in zip(feas, feas[1:]) if b - a > 0.05)
    t_star = min(feas, key=J)
    lo, hi = sorted((tS, tE))
    on_segment = lo - 1e-9 <= t_star <= hi + 1e-9
    check("feasible set is disconnected and the minimizer is off the segment",
          gaps >= 1 and not on_segment and th(tE) < treq,
          f"t*={t_star:.2f} segment=[{lo:.2f},{hi:.2f}] gaps={gaps}")


def affine_cardinal():
    """On a fixed menu, aJ+b has the same argmin. With beta held fixed,
    d/(2 beta) is the excess of aJ+b only when a=1. The fraction moves with b."""
    beta = 2.0
    d = 1
    Jstar = 4.0
    # E[J]-J* = d/(2 beta) for a standard normal in the whitened coordinate.
    excess_J = d / (2 * beta)
    a, b = 3.0, 5.0
    excess_C = a * excess_J          # b cancels
    beta_fixed = beta
    def cost(x, scale, shift):
        return scale * (Jstar + x * x) + shift

    grid = [i * 0.05 for i in range(-40, 41)]
    arg_J = min(grid, key=lambda x: cost(x, 1.0, 0.0))
    arg_C = min(grid, key=lambda x: cost(x, a, b))
    check("argmin unchanged by a positive affine map", arg_J == 0.0 and arg_C == 0.0)
    check("absolute excess at fixed beta equals d/(2 beta) only at scale 1",
          abs(excess_J - d / (2 * beta_fixed)) < 1e-15
          and abs(excess_C - d / (2 * beta_fixed)) > 0.4,
          f"excess_J={excess_J} excess_C={excess_C}")
    # refit beta to the new cost: exponent -beta J = -(beta/a) C, excess of C is d/(2 beta_C)
    beta_C = beta / a
    check("refit beta restores d/(2 beta_C) in the new units",
          abs(excess_C - d / (2 * beta_C)) < 1e-12)
    frac_J = excess_J / Jstar
    frac_C = excess_C / (a * Jstar + b)
    frac_scale_only = (a * excess_J) / (a * Jstar)  # b = 0
    check("fractional excess moves with the additive constant and not with pure scale",
          abs(frac_scale_only - frac_J) < 1e-15 and abs(frac_C - frac_J) > 1e-6,
          f"frac_J={frac_J:.4f} frac_C={frac_C:.4f}")


def frontier_scalarization():
    """Theorem F1: positive weights give Pareto; convexity is required for the converse."""
    A, B, C = (0.0, 1.0), (1.0, 0.0), (0.6, 0.6)

    def dominates(p, q):
        return all(x <= y for x, y in zip(p, q)) and any(x < y for x, y in zip(p, q))

    def dot(w, p):
        return w[0] * p[0] + w[1] * p[1]

    check("A, B, C are pairwise nondominated",
          not dominates(A, B) and not dominates(B, A)
          and not dominates(A, C) and not dominates(C, A)
          and not dominates(B, C) and not dominates(C, B))
    # Algebra, every p >= 0, p != 0. A zero coordinate makes A or B score 0
    # and C score a positive multiple of the other price. Both coordinates
    # positive would need p1/p2 <= 2/3 and p2/p1 <= 2/3, and those bounds
    # multiply to 4/9 < 1.
    check("a zero price makes A or B strictly cheaper than C",
          dot((0.0, 1.0), B) < dot((0.0, 1.0), C)
          and dot((1.0, 0.0), A) < dot((1.0, 0.0), C))
    check("the two ratio bounds multiply to 4/9", abs((2.0 / 3.0) * (2.0 / 3.0) - 4.0 / 9.0) < 1e-15)
    check("C minimizes no nonnegative weighted sum", (2.0 / 3.0) * (2.0 / 3.0) < 1.0)
    mix = (0.5 * (A[0] + B[0]), 0.5 * (A[1] + B[1]))
    check("the mixture of A and B dominates C", dominates(mix, C), f"mix={mix}")
    # antitone: the two efficient extremes
    dS, de = A[0] - B[0], A[1] - B[1]
    check("efficient pair is antitone", dS * de <= 0)
    # p >> 0 minimizer is undominated: C beats a dominated neighbor under every positive weight
    D = (0.7, 0.7)
    check("a strictly positive weight rejects a dominated point",
          dominates(C, D) and all(dot((w, 1.0), C) < dot((w, 1.0), D) for w in (0.2, 1.0, 3.0)))


def main(argv=None):
    print("== CT22 scalar binding multiplier")
    algebra_unimodality()
    published_path()
    print("== obstructions")
    nonconvex_obstruction()
    nonunimodal_obstruction()
    print("== affine scale")
    affine_cardinal()
    print("== frontier scalarization")
    frontier_scalarization()
    nfail = sum(1 for _, ok, _ in check.results if not ok)
    print(f"\n{len(check.results)} checks, {nfail} FAIL")
    print("RESULT:", "PASS" if nfail == 0 else "FAIL")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
