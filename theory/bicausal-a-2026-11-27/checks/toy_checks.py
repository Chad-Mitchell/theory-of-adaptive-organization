"""Toy-input runs of every helper the scored path calls (process/PREREG_GATE.md launch rule). No scored input is used:
the inputs below are published repo numbers or arbitrary points, never the scored grids."""
import numpy as np
import sympy as sp
import ba_lib as L
import ba_t1_sym as T1

fails = 0
def chk(name, got, want, tol):
    global fails
    ok = abs(got - want) <= tol
    fails += (not ok)
    print("%-62s got %.9g want %.9g %s" % (name, got, want, "ok" if ok else "FAIL"))

# 1. W2 against the logged RI numbers (theory/two-route-2026-11-25/DEVIATIONS.md, 2026-11-25 09:29 ET)
r = L.w2_heats(1.0, 0.0, 6.884105, 0.592273)
chk("W2 RI design, g=0: QM", r["QM"], 2.108563, 2e-6)
chk("W2 RI design, g=0: Sigma_xm", r["sxm"], 0.517151, 2e-6)
r = L.w2_heats(1.0, 0.5, 6.884105, 0.592273)
chk("W2 RI design, g=0.5: QM", r["QM"], 1.849987, 2e-6)
chk("W2 RI design, g=0.5: Sigma_xx", r["sxx"], 1.373910, 2e-6)
chk("W2 g=0: QX = 0 (A-C1)", r["QX"] * 0 + L.w2_heats(1.0, 0.0, 3.0, 0.7)["QX"], 0.0, 1e-12)

# 2. LINK direct member against AT-attain (theory/INFO_PHYSICS_ATTAINABILITY.md section 4):
#    a=v=1, eps=0.2, lambda=1e6: heat 4.000020 (exact 200000/199999 * 4)
a = v = 1.0; eps = 0.2; lam = 1e6
cc = (v - eps) / v; rho = lam / (a + lam); sig2 = (v - eps) * (rho * (v + eps) / v - 1)
# AT-attain uses f = -lam M + c lam X with noise lam sig2; the LINK helper has gain 1, so rescale M by 1/c:
# noise lam sig2 / c^2, same heat and same decision error.
d = L.link_member(a, v, None, None, lam, lam * sig2 / cc ** 2, linked=False)
chk("direct spring heat vs AT-attain 4*200000/199999", d["Q1"], 4 * 200000 / 199999, 1e-6)
chk("direct spring decision error vs 0.2 (limit)", d["eps1"], 0.2, 1e-6)
chk("direct: world heat 0", d["QX"], 0.0, 1e-9)
chk("direct infimum at w=10: 2 sqrt(10) - 1", L.direct_infimum(10.0), 2 * np.sqrt(10) - 1, 1e-12)

# 3. LINK level heat: Lyapunov against the paper closed form, arbitrary points
for (b0, D0, b1, D1) in [(2.0, 0.3, 5.0, 0.7), (0.4, 2.0, 1.3, 0.01), (30.0, 0.05, 300.0, 3.0)]:
    rr = L.link_member(1.0, 1.0, b0, D0, b1, D1)
    chk("level heat Lyapunov vs closed form (%g,%g)" % (b0, D0), rr["Q0"], L.level_heat_closed_form(1, 1, b0, D0), 1e-8 * max(1, rr["Q0"]))
    chk("linked: world heat 0", rr["QX"], 0.0, 1e-9)

# 4. Chain at K=1 never below the direct infimum (BA-C2 identity), arbitrary toy designs at toy stake w=2.5
rng = np.random.default_rng(7)
worst = np.inf
for _ in range(2000):
    b0, D0, b1, D1 = np.exp(rng.uniform(-4, 6, 4))
    c, _r = L.pooled_cost(1, 2.5, 1.0, 1.0, b0, D0, b1, D1)
    worst = min(worst, c - L.direct_infimum(2.5))
print("K=1 chain minus direct infimum, min over 2000 toy designs at w=2.5: %.6g" % worst)
fails += worst < -1e-9

# 5. Symbolic W2 moments against the numeric Lyapunov at an arbitrary point
num = L.w2_cov(1.3, 0.4, 2.2, 0.6, 0.9, 1.1)
sym = T1.sigma_numeric(1.3, 0.4, 2.2, 0.6, 0.9, 1.1)
for k, (i, j) in enumerate([(0, 0), (0, 1), (1, 1)]):
    chk("symbolic Sigma[%d,%d] vs Lyapunov" % (i, j), sym[k], num[i, j], 1e-12)

# 6. Potential detector on games whose answer is known
#    (a) team game: both parties pay J_tot -> weighted potential with ratio 1
#    (b) J_w = 3 J_m + h(g) + k(gamma, c) -> weighted potential with ratio 3 (k drops out of the world's choice)
#    (c) J_m = gamma g^2 + c, J_w = g c^2: not potential (cross partials (2g, 0) and (0, 2c))
g, gam, c = T1.g, T1.gam, T1.c
Jtot = gam ** 2 * g + sp.sin(c * g) + c ** 2
print("team game:", T1.potential_test(Jtot, Jtot))
print("scaled game:", T1.potential_test(Jtot, 3 * Jtot + g ** 3 + sp.exp(gam) * c))
print("non-potential toy:", T1.potential_test(gam * g ** 2 + c, g * c ** 2))
fails += T1.potential_test(Jtot, Jtot)["outcome_code"] != "potential"
fails += T1.potential_test(Jtot, 3 * Jtot + g ** 3 + sp.exp(gam) * c)["outcome_code"] != "potential"
fails += T1.potential_test(gam * g ** 2 + c, g * c ** 2)["outcome_code"] != "no-weighted-potential"
# 7. W2 cost expressions against a logged number: J_m = 10.5035 on the ln gamma = 5 edge at w_x = 0.5
#    (theory/two-route-2026-11-25/RESULTS.md:38: gamma = 148.41, c = 0.0205, g = 1.4497)
Jm, Jw, QM, QX = T1.w2_costs()
val = float(Jm.subs({T1.a: 1, T1.D: 1, T1.DM: 1, T1.w: 10, T1.ww: 10, T1.wx: sp.Rational(1, 2),
                     T1.gam: sp.exp(5), T1.c: sp.Rational(205, 10000), T1.g: sp.Rational(14497, 10000)}))
chk("W2 J_m on the A-T1 v4 box edge (logged 10.5035)", val, 10.5035, 6e-4)

# 8. BA-T2 helpers on toy inputs only: exact rational re-evaluation vs float at a toy design (K = 4, w = 2), and the
#    optimizer at K = 1 (the BA-C2 identity, whose answer is known), toy stake w = 2.5
import ba_t2 as T2
x = np.log([1.7, 0.21, 40.0, 3.3])
P, Jd, des, e1, q0, q1 = T2.exact_cost(4, 2.0, x)
fl, _ = L.pooled_cost(4, 2.0, 1.0, 1.0, *[float(d) for d in des])
chk("exact rational per-member cost vs float, toy design", float(P), fl, 1e-9)
K_, w_, best = T2.solve((1, 2.5, []))
print("optimizer at K = 1, toy w = 2.5: best per-member %.6f, direct infimum %.6f" % (best[0], L.direct_infimum(2.5)))
fails += best[0] < L.direct_infimum(2.5) - 1e-9
print("FAILS", fails)
