"""Symbolic W2 moments and the weighted-potential test (Monderer and Shapley 1996) for two-party smooth games.

A two-party game with costs J_m(theta_m, g), J_w(theta_m, g), theta_m = (gamma, c), is a weighted potential game with
positive weights (l_m, l_w) iff there is Psi with dJ_m/dtheta_m = l_m dPsi/dtheta_m and dJ_w/dg = l_w dPsi/dg. On a
simply connected open domain with C^2 costs this holds iff d2J_m/(dtheta_k dg) / l_m = d2J_w/(dtheta_k dg) / l_w for
k = gamma, c at every point. So with P_m = (d2J_m/dgamma dg, d2J_m/dc dg) and P_w likewise, a weighted potential needs
Delta = P_m[0] P_w[1] - P_m[1] P_w[0] = 0 everywhere, and a constant positive ratio P_w / P_m.
"""
import random
import sympy as sp

a, D, DM, g, gam, c = sp.symbols("a D D_M g gamma c", real=True)
w, ww, wx = sp.symbols("w w_w w_x", real=True)
sxx, sxm, smm = sp.symbols("s_xx s_xm s_mm", real=True)

_eqs = [sp.Eq(2 * (-a * sxx + a * g * sxm) + 2 * D, 0),
        sp.Eq(-a * sxm + a * g * smm + gam * c * sxx - gam * sxm, 0),
        sp.Eq(2 * (gam * c * sxm - gam * smm) + 2 * DM, 0)]
_sol = sp.solve(_eqs, [sxx, sxm, smm], dict=True)[0]
SXX, SXM, SMM = [sp.simplify(_sol[s]) for s in (sxx, sxm, smm)]


def sigma_numeric(av, gv, gamv, cv, Dv, DMv):
    sub = {a: av, g: gv, gam: gamv, c: cv, D: Dv, DM: DMv}
    return [float(e.subs(sub)) for e in (SXX, SXM, SMM)]


def w2_costs():
    """J_m, J_w of theory/two-route-2026-11-25/PREREG_4.md section 1.1 (shared excursion term w_x E[x^2])."""
    e_x = SXX - 2 * g * SXM + g ** 2 * SMM
    e_m = SMM - 2 * c * SXM + c ** 2 * SXX
    QX = a ** 2 * e_x - D * a
    QM = gam ** 2 * e_m - DM * gam
    track = SXX - 2 * SXM + SMM
    Jm = QM + w * track + wx * SXX
    Jw = QX + ww * e_x + wx * SXX
    return Jm, Jw, QM, QX


def _rand_point(rng, fixed):
    """An exact rational point inside the W2 domain (gamma > 0, g c < 1, a, D, D_M > 0), honoring fixed values."""
    while True:
        p = {a: sp.Rational(rng.randint(1, 9), rng.randint(1, 9)), D: sp.Rational(rng.randint(1, 9), rng.randint(1, 9)),
             DM: sp.Rational(rng.randint(1, 9), rng.randint(1, 9)), gam: sp.Rational(rng.randint(1, 40), rng.randint(1, 9)),
             c: sp.Rational(rng.randint(-20, 30), 10), g: sp.Rational(rng.randint(0, 30), 10),
             w: sp.Rational(rng.randint(0, 20), 1), ww: sp.Rational(rng.randint(0, 20), 1), wx: sp.Rational(rng.randint(0, 4), 2)}
        p.update(fixed)
        if p[g] * p[c] < 1:
            return p


def potential_test(Jm, Jw, fixed=None, npts=12, seed=20261127):
    """Return a dict: outcome_code in {'potential', 'no-weighted-potential'} with the exact witness."""
    fixed = fixed or {}
    Pm = [sp.diff(Jm, gam, g), sp.diff(Jm, c, g)]
    Pw = [sp.diff(Jw, gam, g), sp.diff(Jw, c, g)]
    Delta = Pm[0] * Pw[1] - Pm[1] * Pw[0]
    rng = random.Random(seed)
    witness = None
    ratios = []
    for _ in range(npts):
        p = _rand_point(rng, fixed)
        dv = sp.nsimplify(Delta.subs(p))
        dv = sp.simplify(dv)
        if dv != 0:
            witness = (p, dv)
            break
        pm = [sp.simplify(x.subs(p)) for x in Pm]
        pw = [sp.simplify(x.subs(p)) for x in Pw]
        for x, y in zip(pm, pw):
            if x != 0:
                ratios.append(sp.simplify(y / x))
            elif y != 0:
                witness = (p, "P_m component 0, P_w component %s" % y)
                break
        if witness:
            break
    if witness is not None:
        return dict(outcome_code="no-weighted-potential", witness=witness)
    if len(set(ratios)) > 1:
        return dict(outcome_code="no-weighted-potential", witness=("ratio varies", sorted(set(ratios), key=str)[:3]))
    if ratios and ratios[0] <= 0:
        return dict(outcome_code="no-weighted-potential", witness=("ratio not positive", ratios[0]))
    return dict(outcome_code="potential", ratio=ratios[0] if ratios else None)
