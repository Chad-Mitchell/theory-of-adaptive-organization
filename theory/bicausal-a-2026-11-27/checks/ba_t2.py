"""BA-T2 (scored): the pooling threshold when a link is paid as heat (PREREG.md section 3).
Run only from a fresh clone at the pushed lock commit, after the gate read. Usage: python3 ba_t2.py [--half]
--half is the resolution rerun: every tolerance halved and twice the number of polished starts."""
import sys, time, itertools
import numpy as np
import sympy as sp
from multiprocessing import Pool
from scipy.optimize import minimize
import ba_lib as L

HALF = "--half" in sys.argv
A = V = 1.0
WS = (3.0, 10.0, 100.0)
KS = (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128)
LO = np.array([-4.0, -16.0, -4.0, -16.0]); HI = np.array([12.0, 12.0, 12.0, 12.0])   # ln b0, ln D0, ln b1, ln D1
XATOL, FATOL = (1e-9, 1e-11) if HALF else (2e-9, 2e-11)
NPOLISH = 40 if HALF else 20
MARGIN = 1e-3


def cost(x, K, w):
    x = np.clip(x, LO, HI)
    b0, D0, b1, D1 = np.exp(x)
    try:
        c, _ = L.pooled_cost(K, w, A, V, b0, D0, b1, D1)
    except Exception:
        return np.inf
    return c if np.isfinite(c) else np.inf


GRID = [np.array(p) for p in itertools.product((-2, 0, 2, 4, 6, 8), (-12, -9, -6, -3, 0, 3), (0, 3, 6, 9), (-8, -5, -2, 1, 4))]


def paper_seeds(w):
    """Seeds from the PAPER-approx optimum (paper_approx.out): b0 = b, D0 = u b0^2, fast member b1 = 1e3 b0, D1 = delta b1."""
    out = []
    for b, u, d in [(2.25, 0.089, 0.078), (3.08, 0.036, 0.030), (5.0, 0.0077, 0.007), (6.2, 0.0037, 0.0037),
                    (7.6, 0.0018, 0.002), (2.3, 0.027, 0.065), (19.5, 0.0006, 0.0001)]:
        b1 = 1e3 * b
        out.append(np.log([b, u * b * b, b1, d * b1]))
    return out


def solve(args):
    K, w, warm = args
    starts = GRID + paper_seeds(w) + list(warm)
    vals = np.array([cost(s, K, w) for s in starts])
    order = np.argsort(vals)[:NPOLISH]
    best = None
    for i in order:
        r = minimize(cost, starts[i], args=(K, w), method="Nelder-Mead",
                     options=dict(xatol=XATOL, fatol=FATOL, maxiter=40000, maxfev=80000, adaptive=True))
        x = np.clip(r.x, LO, HI)
        f = cost(x, K, w)
        if best is None or f < best[0]:
            best = (f, x)
    return K, w, best


def exact_cost(K, w, x):
    """Exact rational re-evaluation of a design (rounded to 12 significant digits, then exact): Lyapunov by sympy."""
    b0, D0, b1, D1 = [sp.nsimplify(float("%.12g" % v), rational=True) for v in np.exp(x)]
    a = v = sp.Integer(1)
    F = sp.Matrix([[-a, 0, 0], [b0, -b0, 0], [0, b1, -b1]])
    s = sp.symbols("s0:6")
    S = sp.Matrix([[s[0], s[1], s[2]], [s[1], s[3], s[4]], [s[2], s[4], s[5]]])
    M = F * S + S * F.T + 2 * sp.diag(a * v, D0, D1)
    sol = sp.solve([M[i, j] for i in range(3) for j in range(i, 3)], s, dict=True)[0]
    S = S.subs(sol)
    e0 = S[1, 1] - 2 * S[0, 1] + S[0, 0]
    e1 = S[2, 2] - 2 * S[1, 2] + S[1, 1]
    Q0 = b0 ** 2 * e0 / D0 - b0
    Q1 = b1 ** 2 * e1 / D1 - b1
    eps1 = v - S[0, 2] ** 2 / S[2, 2]
    P = sp.nsimplify(Q0 / K + Q1 + sp.Rational(int(w)) * eps1)
    Jd = 2 * sp.sqrt(sp.Rational(int(w))) - 1
    return P, Jd, (b0, D0, b1, D1), sp.N(eps1, 30), sp.N(Q0, 30), sp.N(Q1, 30)


if __name__ == "__main__":
    t0 = time.time()
    print("BA-T2 %s run: a = v = kT = 1; K grid %s; stakes %s; box ln b in [-4,12], ln D in [-16,12]; xatol %g fatol %g; polished starts %d"
          % ("half-tolerance" if HALF else "primary", KS, WS, XATOL, FATOL, NPOLISH))
    results = {}
    with Pool(8) as pool:
        warm = {w: [] for w in WS}
        # one pass over K in order, warm-starting each stake from the previous K's optimum
        for K in KS:
            outs = pool.map(solve, [(K, w, warm[w]) for w in WS])
            for K_, w, best in outs:
                results[(K_, w)] = best
                warm[w] = [best[1]]
    for w in WS:
        Jd = L.direct_infimum(w)
        print("\nstake w = %g: direct infimum 2 sqrt(w) - 1 = %.9f" % (w, Jd))
        print("  K   per-member pooled   ratio      ln b0    ln D0    ln b1    ln D1   eps1      eps0      Q0/K      Q1      box-edge")
        for K in KS:
            f, x = results[(K, w)]
            r = L.link_member(A, V, *np.exp(x))
            edge = [n for n, xi, lo, hi in zip(("lnb0", "lnD0", "lnb1", "lnD1"), x, LO, HI) if abs(xi - lo) < 1e-6 or abs(xi - hi) < 1e-6]
            print("  %-3d %.9f   %.6f   %7.3f  %7.3f  %7.3f  %7.3f  %.6f  %.6f  %.6f  %.6f  %s"
                  % (K, f, f / Jd, *x, r["eps1"], r["eps0"], r["Q0"] / K, r["Q1"], ",".join(edge) or "-"))
    # code gate (BA-C2): at K = 1 nothing may beat the direct infimum
    gate = all(results[(1, w)][0] >= L.direct_infimum(w) - 1e-9 for w in WS)
    print("\nCode gate BA-C2 (K = 1 never below the direct infimum):", "passed" if gate else "FIRED (measurement/code)")
    kstar = {}
    for w in WS:
        Jd = L.direct_infimum(w)
        kstar[w] = None
        for K in KS[1:]:
            f, x = results[(K, w)]
            if f < Jd * (1 - MARGIN):
                P, Jd_exact, des, eps1, Q0, Q1 = exact_cost(K, w, x)
                diff = sp.N(P - Jd_exact * (1 - sp.Rational(1, 1000)), 40)
                print("  w = %g, K = %d: exact rational re-evaluation, per-member %s, direct %s, margin-adjusted difference %s"
                      % (w, K, sp.N(P, 20), sp.N(Jd_exact, 20), diff))
                if diff < 0:
                    kstar[w] = K
                    break
    print("\nK-hat* by stake:", {w: kstar[w] for w in WS})
    cls = {w: ("none" if k is None else "low" if k < 12 else "high" if k > 48 else "band") for w, k in kstar.items()}
    vals = set(cls.values())
    if vals == {"band"} and gate:
        outcome = "HIT"
    elif not gate:
        outcome = "not scored (code gate fired)"
    elif len(vals) > 1:
        outcome = "MISS, mixed (sensitivity-dependent open miss): %s" % cls
    else:
        outcome = "MISS, %s: %s" % (vals.pop(), cls)
    print("BA-T2 outcome (%s run):" % ("half-tolerance" if HALF else "primary"), outcome)
    print("elapsed %.1f s" % (time.time() - t0))
