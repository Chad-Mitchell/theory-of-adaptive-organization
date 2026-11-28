"""BA-T1 (scored): is W2 with both bath heats a weighted potential game? (PREREG.md section 2.)
Run only from a fresh clone at the pushed lock commit, after the gate read (PREREG.md section 5)."""
import time
import numpy as np
import sympy as sp
import ba_t1_sym as T
import ba_lib as L

t0 = time.time()
Jm, Jw, QM, QX = T.w2_costs()
one = sp.Integer(1)
base = {T.a: one, T.D: one, T.DM: one, T.w: 10 * one, T.ww: 10 * one}
print("BA-T1 scored settings: a = D = D_M = 1, w = w_w = 10")
scored = {}
for wxv in (sp.Rational(1, 2), one, 2 * one):
    fixed = dict(base); fixed[T.wx] = wxv
    r = T.potential_test(Jm.subs(fixed), Jw.subs(fixed), fixed=fixed)
    scored[str(wxv)] = r["outcome_code"]
    print("  w_x = %s: %s; witness %s" % (wxv, r["outcome_code"], r.get("witness", r.get("ratio"))))
print("Reported, not scored:")
for label, fx in [("w_x = 0 (no shared excursion term)", dict(base, **{T.wx: 0 * one})),
                  ("heat only (w = w_w = w_x = 0)", {T.a: one, T.D: one, T.DM: one, T.w: 0 * one, T.ww: 0 * one, T.wx: 0 * one}),
                  ("all parameters free", {})]:
    r = T.potential_test(Jm.subs(fx), Jw.subs(fx), fixed=fx)
    print("  %s: %s; witness %s" % (label, r["outcome_code"], r.get("witness", r.get("ratio"))))

# Delta at the logged A-T1''' designs (theory/two-route-2026-11-25/RESULTS.md:38 and PREREG_4.md section 1.2), numeric
Pm = [sp.diff(Jm, T.gam, T.g), sp.diff(Jm, T.c, T.g)]
Pw = [sp.diff(Jw, T.gam, T.g), sp.diff(Jw, T.c, T.g)]
f = sp.lambdify((T.a, T.D, T.DM, T.w, T.ww, T.wx, T.gam, T.c, T.g), Pm + Pw, "mpmath")
for label, (wxv, gv, cv, ggv) in [("A-T1''' Nash, w_x = 2", (2.0, 6.500, 0.5448, 0.7682)),
                                  ("PAPER joint minimum, w_x = 1", (1.0, 5.779, 0.8030, 0.6118))]:
    pm0, pm1, pw0, pw1 = [float(x) for x in f(1, 1, 1, 10, 10, wxv, gv, cv, ggv)]
    print("  %s: P_m = (%.6g, %.6g), P_w = (%.6g, %.6g), Delta = %.6g, ratios P_w/P_m = (%.6g, %.6g)"
          % (label, pm0, pm1, pw0, pw1, pm0 * pw1 - pm1 * pw0, pw0 / pm0, pw1 / pm1))
ok = all(v == "no-weighted-potential" for v in scored.values())
print("BA-T1 outcome:", "HIT (no weighted potential at all three w_x)" if ok else "MISS: " + str(scored))
print("elapsed %.1f s" % (time.time() - t0))
