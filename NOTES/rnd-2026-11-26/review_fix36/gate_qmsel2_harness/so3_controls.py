# Gate-reader harness: runs ONLY the SO(3) control block of search_rank2.selftest() (lines 752-773 of the
# locked script, copied verbatim in logic); no SU(3)/Sp(2)/G2 construction or analysis.
import sys, json, numpy as np, scipy
import search_rank2 as s
print("# numpy %s scipy %s python %s" % (np.__version__, scipy.__version__, sys.version.split()[0]))
g1, z1 = s.so3_spin(1); g2, z2 = s.so3_spin(2); g3, z3 = s.so3_spin(3)
controls = [s.Body("B3 (spin 1)", g1, z1, "SO(3)"), s.Body("Z3 (spin 3)", g3, z3, "SO(3)"),
            s.Body("C1 (spin 1+2)", [s.block([a, b]) for a, b in zip(g1, g2)], np.r_[z1, z2], "SO(3)"),
            s.Body("Z2 (real QM d=3)", g2, z2, "SO(3)")]
gb, vb = s.product_body([("a", g1, z1), ("b", g1, z1)])
controls.append(s.Body("B3 x B3", gb, vb, "SO(3)^2"))
for i, B in enumerate(controls):
    r = s.analyse(B, 1000 + i, do_full=True); print(json.dumps(r, default=float), flush=True)
for i, B in enumerate(controls[:1] + controls[3:4]):
    rng = np.random.default_rng(s.SEED + 2000 + i)
    P, c = s.ambient(B, rng); y0 = P.T @ (B.v - c)
    G, g0 = s.g0_algebra(B, P, c, rng)
    r0, rh, h0, carth = s.sfp_rank_test(g0, y0, rng)
    Y = np.array([P.T @ (x - c) for x in s.orbit_samples(B, s.N_GRID, rng)])
    tpts = s.tfixed_points(g0, carth, y0, rng)
    NLB, wit = s.cap_lower_bound(Y, tpts, g0, 3, rng, y0=y0)
    adim, isball = s.bitface_is_ball(Y, wit[0], wit[1], g0, rng)
    print("  %-18s cap_LB %d  bit-face affine dim %s  is 3-ball %s" % (B.name, NLB, adim, isball), flush=True)
