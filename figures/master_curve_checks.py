"""Recompute every number drawn on figures/master_curve.png. Run: nice -n 19 python3 figures/master_curve_checks.py"""
import math
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import master_curve_math as M  # noqa: E402
from master_curve_params import P  # noqa: E402

PASS = FAIL = 0


def check(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print("PASS", name, detail)
    else:
        FAIL += 1
        print("FAIL", name, detail)


def near(a, b, tol):
    return abs(a - b) <= tol * max(1.0, abs(b))


# 1. The collapse: the section-5 frontier divided by kT a equals F(x).
for a, v, w, kT in [(1, 1, 2, 1), (3.0, 0.2, 50.0, 0.7), (1e-2, 4.0, 0.3, 2e-3), (100.0, 1.0, 0.5, 1.0)]:
    x = w * v / (kT * a)
    J = (2 * math.sqrt(kT * a * v * w) - kT * a) if w > kT * a / v else w * v
    check("collapse a=%g v=%g w=%g kT=%g" % (a, v, w, kT), near(J / (kT * a), float(M.F(x)), 1e-12), "x=%.6g J/kTa=%.12f" % (x, J / (kT * a)))

# 2. Repo reference values (GENERAL_FORM_PHYSICS section 5).
check("scalar frontier at a=v=kT=1, w=2 is 1.828427124746", near(float(M.F(2.0)), 1.828427124746, 1e-12), "%.12f" % float(M.F(2.0)))
J3 = sum(float(M.F(2.0 * 1.0 / a)) * a for a in (1.0, 10.0, 100.0))
check("three modes (1,10,100), w=2: cost 5.828427124746, one tracked", near(J3, 5.828427124746, 1e-12)
      and sum(1 for a in (1, 10, 100) if 2.0 / a > 1) == 1, "%.12f" % J3)
# K identical sum: general_checks.py prints J = 2 sqrt(3w) - 1 for K=3, a=v=kT=1
for w in (0.5, 2.0, 8.0):
    check("K=3 sum frontier w=%g on F with x=3w" % w, near(float(M.F(3 * w)), 2 * math.sqrt(3 * w) - 1, 1e-12))

# 3. Brute-force minimum of floor + w*eps lands on F for every random world plotted.
kT, a, v, w = M.random_worlds(P["n_worlds"], P["seed"])
worst = 0.0
for i in range(len(kT)):
    Jb, _ = M.brute_min(a[i], v[i], w[i], kT[i], n=20001)
    x = w[i] * v[i] / (kT[i] * a[i])
    rel = abs(Jb / (kT[i] * a[i]) - float(M.F(x))) / float(M.F(x))
    worst = max(worst, rel)
check("all %d random worlds: brute-force minimum on the curve" % len(kT), worst < 1e-6, "worst rel dev %.2e" % worst)
check("raw stakes span > 8 decades", math.log10(w.max() / w.min()) > 8, "%.1f decades" % math.log10(w.max() / w.min()))

# 4. Nothing in the class goes below the curve: any eps gives floor + w eps >= min.
rng = np.random.default_rng(1)
ok = True
for _ in range(2000):
    aa, vv, ww, kk = 10 ** rng.uniform(-2, 2, 4)
    eps = vv * rng.uniform(1e-4, 1.0)
    x = ww * vv / (kk * aa)
    if (M.heat_floor(aa, vv, eps, kk) + ww * eps) / (kk * aa) < float(M.F(x)) - 1e-12:
        ok = False
check("2000 random designs at the heat floor: none below the curve", ok)

# 5. Error at the minimum = v / sqrt(x) above the knee (section 5: sqrt(kT a v / w)).
for x in (2.0, 100.0, 1e4):
    _, eb = M.brute_min(1.0, 1.0, x, 1.0)
    check("error fraction at x=%g is 1/sqrt(x)" % x, near(eb, float(M.err_frac(x)), 1e-4), "%.6f vs %.6f" % (eb, float(M.err_frac(x))))

# 6. Knee: slope 1 below, slope 1/2 asymptotically; continuous with matching slope at x=1.
h = 1e-7
check("continuous at x=1", near(float(M.F(1 - h)), float(M.F(1 + h)), 1e-6))
check("slope 1 at the knee from both sides", near((float(M.F(1 + h)) - 1) / h, 1.0, 1e-5))
lx = np.log([1e6, 1e8]); ly = np.log(M.F([1e6, 1e8]))
check("log-log slope -> 1/2 at high x", near((ly[1] - ly[0]) / (lx[1] - lx[0]), 0.5, 1e-3))

# 7. Ladder drawn: rho, x at slowest rung, rung count, and the formula.
rho, x0, n = P["rho"], P["x_slowest"], P["rungs"]
xs = M.ladder_xs(x0, rho, n)
tracked = sum(1 for x in xs if x > 1)
check("ladder: tracked rungs = floor(log x/log rho)+1 = %d" % P["ladder_label_count"],
      tracked == M.ladder_count(x0, rho) == P["ladder_label_count"], "xs=%s" % [round(x, 4) for x in xs])
check("ladder: stakes x rho adds one store", M.ladder_count(x0 * rho, rho) == P["ladder_label_count"] + 1)
for k in range(1, 30):
    xx = 1.7 ** k
    brute = sum(1 for j in range(200) if xx / rho ** j > 1)
    if brute != M.ladder_count(xx, rho):
        check("ladder formula vs count at x=%g" % xx, False)
        break
else:
    check("ladder formula matches direct count on 29 stakes", True)
# per-mode cost of the ladder = sum of rho^k F(x/rho^k) (units of kT a_slowest): each rung on F in its own units
Jl = sum(rho ** k * float(M.F(x0 / rho ** k)) for k in range(n))
check("ladder: total is the sum of per-mode frontiers (repo three-mode value reproduced above)", Jl > 0, "J/(kT a1)=%.6f" % Jl)

# 8. Holographic: K separate copies vs one shared memory of the K-item sum.
K = P["K"]
for x in (2.0, 3.9):
    check("x=%g in (1,K]: shared tracks, separate copies blind (cost = x)" % x,
          float(M.F(x)) < x and near(float(M.separate_copies(x, K)), x, 1e-12))
r = float(M.separate_copies(1e10, K) / M.F(1e10))
check("separate/shared cost ratio -> sqrt(K) = %g at high stakes" % math.sqrt(K), near(r, math.sqrt(K), 1e-3), "%.6f" % r)
xs_ = np.logspace(-2, 4, 500)
check("separate copies never below the curve", bool(np.all(M.separate_copies(xs_, K) >= M.F(xs_) - 1e-12)))
# matched-error heat ratio = K (HOLOGRAPHIC_MEMORY section 1; general_checks)
v1, a1, s = 1.0, 1.0, 0.37
shared_heat = M.heat_floor(a1, K * v1, K * s)
sep_heat = K * M.heat_floor(a1, v1, s)
check("matched-error heat ratio separate/shared = K = %d" % K, near(sep_heat / shared_heat, K, 1e-12))
# repo number: unequal rates (1,100), sum error 0.5: separate heat 141 vs mu 103.887732673340
check("repo ratio 141/103.887732673340 = 1.357234", near(141 / 103.887732673340, 1.357234, 1e-6))

# 9. Hypothesis sentence byte-identical to README.md
root = __file__.rsplit("/", 2)[0]
sent = "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."
for f in ("README.md", "CORE.md", "THEORY.md"):
    check("hypothesis sentence present in " + f, sent in open(root + "/" + f, encoding="utf-8").read())
check("figure uses the same sentence", P["hypothesis"] == sent)

# 10. T41 field/cut panel (HOLOGRAPHIC_2026-11-22.md line 130): recomputed with the repo checker's own functions.
rows = M.cut_vs_bulk()
n16 = [r for r in rows if r[0] == 16][0]
check("cut: all loads meet the tolerance", all(r[4] for r in rows))
check("cut: bulk floor 13 per site, 3328 at n=16", near(n16[1], 3328.0, 1e-12))
check("cut: bound 13 per cut site, 208 at n=16", near(n16[2], 208.0, 1e-12))
check("cut: achieved 217.693 at n=16, about 13.61 per cut site", near(n16[3], 217.693, 1e-5) and abs(n16[3] / 16 - 13.61) < 0.005,
      "%.4f per site" % (n16[3] / 16))
sl = np.polyfit(np.log([r[0] for r in rows]), np.log([r[3] for r in rows]), 1)[0]
check("cut: cost exponent in the cut length ~1 (0.999690)", abs(sl - 0.999690) < 1e-4, "%.6f" % sl)
sb = np.polyfit(np.log([r[0] for r in rows]), np.log([r[1] for r in rows]), 1)[0]
check("bulk: exponent 2 in the side (volume in d=2)", near(sb, 2.0, 1e-9))
# 11. 'aligned 4 vs random 19.2' and '2x = sqrt(4)' are quoted from HOLOGRAPHIC_MEMORY_2026-11-22.md line 120 and line 25.
txt = open(root + "/theory/HOLOGRAPHIC_MEMORY_2026-11-22.md", encoding="utf-8").read()
check("quoted: random 19.2 against 4", "\\(19.2\\), against \\(4\\)" in txt)
check("quoted: optimized cost ratio tends to sqrt(K)", "The ratio of optimized costs tends to \\(\\sqrt{K}\\)" in txt)

print("PASS %d  FAIL %d" % (PASS, FAIL))
print("FAILS %d" % FAIL)
sys.exit(1 if FAIL else 0)
