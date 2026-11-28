"""BA-T1 deviation run (DEVIATIONS.md, 2026-11-27): the locked ba_t1.py passed Delta through sympy.nsimplify, which
printed a non-rational guess for the w_x = 1/2 witness, and its unscored section stopped on a dict-keyword bug.
This script uses the same model and the same witness points, evaluates Delta with exact rational arithmetic only
(subs, then cancel; no nsimplify, no floats), checks the result is a sympy Rational, and runs the unscored settings."""
import random
import sympy as sp
import ba_t1_sym as T

Jm, Jw, QM, QX = T.w2_costs()
Pm = [sp.diff(Jm, T.gam, T.g), sp.diff(Jm, T.c, T.g)]
Pw = [sp.diff(Jw, T.gam, T.g), sp.diff(Jw, T.c, T.g)]
Delta = Pm[0] * Pw[1] - Pm[1] * Pw[0]
one = sp.Integer(1)


def exact_at(p):
    vals = [sp.cancel(e.subs(p)) for e in Pm + Pw]
    d = sp.cancel(Delta.subs(p))
    assert all(isinstance(x, sp.Rational) for x in vals + [d]), "not rational"
    return vals, d


pt = {T.a: one, T.D: one, T.DM: one, T.gam: sp.Rational(19, 7), T.c: sp.Rational(-1, 2), T.g: 3 * one,
      T.w: 10 * one, T.ww: 10 * one}
print("Scored witnesses, exact (gamma = 19/7, c = -1/2, g = 3, a = D = D_M = 1, w = w_w = 10; g c = -3/2 < 1):")
for wxv in (sp.Rational(1, 2), one, 2 * one):
    p = dict(pt); p[T.wx] = wxv
    (pm0, pm1, pw0, pw1), d = exact_at(p)
    print("  w_x = %s: P_m = (%s, %s), P_w = (%s, %s), Delta = %s = %.10g" % (wxv, pm0, pm1, pw0, pw1, d, float(d)))

# A second exact witness inside the region the A-T1''' runs visited (gamma > 0, 0 < c < 1, 0 < g < 1.5)
print("Second witness in the visited region (gamma = 13/2, c = 1/2, g = 3/4):")
for wxv in (sp.Rational(1, 2), one, 2 * one):
    p = dict(pt); p.update({T.gam: sp.Rational(13, 2), T.c: sp.Rational(1, 2), T.g: sp.Rational(3, 4), T.wx: wxv})
    (pm0, pm1, pw0, pw1), d = exact_at(p)
    print("  w_x = %s: Delta = %s = %.10g; ratios P_w/P_m = (%.6g, %.6g)" % (wxv, d, float(d), float(pw0 / pm0), float(pw1 / pm1)))

print("Reported, not scored (same witness test, exact):")
settings = [("w_x = 0, w = w_w = 10", {T.a: one, T.D: one, T.DM: one, T.w: 10 * one, T.ww: 10 * one, T.wx: 0 * one}),
            ("heats only, w = w_w = w_x = 0", {T.a: one, T.D: one, T.DM: one, T.w: 0 * one, T.ww: 0 * one, T.wx: 0 * one})]
rng = random.Random(20261127)
for label, fx in settings:
    found = None
    for _ in range(40):
        p = T._rand_point(rng, fx)
        _, d = exact_at(p)
        if d != 0:
            found = (p, d)
            break
    if found:
        p, d = found
        print("  %s: no-weighted-potential; gamma = %s, c = %s, g = %s, Delta = %s = %.6g" % (label, p[T.gam], p[T.c], p[T.g], d, float(d)))
    else:
        print("  %s: Delta = 0 at 40 exact points" % label)
# all parameters free: Delta is not identically zero as a function (a nonzero value at one exact point shows it)
p = T._rand_point(rng, {})
_, d = exact_at(p)
print("  all parameters free: Delta at %s = %.6g" % ({str(k): str(v) for k, v in p.items()}, float(d)))
