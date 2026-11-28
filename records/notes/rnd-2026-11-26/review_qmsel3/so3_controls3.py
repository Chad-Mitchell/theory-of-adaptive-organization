"""Gate-read harness for qm-selection-3: SO(3) published controls only. Never calls --run."""
import sys, json, time, numpy as np
from numpy.linalg import norm
sys.path.insert(0, "/workspace/gate-qmsel3/theory/qm-selection-3-2026-11-26")
import search_qmsel3 as S
S._DEADLINE[0] = 1e18
cap = {}
orig = S.recheck_witness
def wrap(B, P, c, E, g0, idx):
    mn = orig(B, P, c, E, g0, idx); cap[B.name] = (E, P, c, mn); return mn
S.recheck_witness = wrap
g1, z1 = S.so3_spin(1); g2, z2 = S.so3_spin(2); g3, z3 = S.so3_spin(3)
Body = S.Body
controls = [Body("B3 (spin 1)", g1, z1, "SO(3)", known_cp=True), Body("Z3 (spin 3)", g3, z3, "SO(3)"),
            Body("C1 (spin 1+2)", [S.block([a, b]) for a, b in zip(g1, g2)], np.r_[z1, z2], "SO(3)"),
            Body("Z2 (real QM d=3)", g2, z2, "SO(3)")]
gb, vb = S.product_body([("a", g1, z1), ("b", g1, z1)])
controls.append(Body("B3 x B3", gb, vb, "SO(3)^2"))
mode = sys.argv[1]
if mode == "controls":
    for i, B in enumerate(controls):
        t = time.time(); r = S.analyse(B, 1000 + i, do_full=True)
        print(json.dumps({k: r.get(k) for k in ("body", "outcome", "cap_UB", "cap_LB", "witness_recheck_min", "hSFP", "n_torus_fixed_weyl", "bit_faces")}, default=float), "%.0fs" % (time.time()-t), flush=True)
    E, P, c, mn = cap["B3 (spin 1)"]
    # exact min of each affine effect a + l.y over the B3 orbit (a sphere of radius r in centred coords)
    B = controls[0]; r = norm(P.T @ (B.v - c))
    ex = [a - norm(l) * r for a, l in E]
    print("B3 witness: recheck min %.3e ; exact sphere minima %s ; radius %.6f" % (mn, ["%.3e" % x for x in ex], r))
elif mode == "b3seeds":
    B = controls[0]
    for s in range(8):
        rng = np.random.default_rng(777 + s)
        P, c = S.ambient(B, rng); y0 = P.T @ (B.v - c); G, g0 = S.g0_algebra(B, P, c, rng)
        Y = np.array([P.T @ (x - c) for x in S.orbit_samples(B, S.N_GRID, rng)])
        r = norm(y0); tp = S.weyl_orbit(y0, S.root_reflections(g0, S.sfp_rank_test(g0, y0, rng)[3], rng))
        NLB, wit, E = S.cap_lower_bound(Y, tp, g0, 2, rng, y0=y0)
        ex = min(a - norm(l) * r for a, l in E)
        print("seed %d NLB %d exact witness min %.3e" % (s, NLB, ex), flush=True)
elif mode == "bitfaces":
    # B3 x B3 = B3 x B3 product of balls: proper 3-ball faces {n} x B3 and B3 x {a}; whole body through the centre
    B = controls[4]
    for s in range(6):
        rng = np.random.default_rng(555 + s)
        P, c = S.ambient(B, rng); G, g0 = S.g0_algebra(B, P, c, rng)
        Y = np.array([P.T @ (x - c) for x in S.orbit_samples(B, S.N_GRID, rng)])
        n = rng.normal(size=3); n /= norm(n); a = rng.normal(size=3); a /= norm(a)
        pt = lambda u, w: P.T @ (np.r_[u, w] - c)
        cases = [("{n} x ball (expect ball 3)", pt(n, a), pt(n, -a)), ("ball x {a} (expect ball 3)", pt(n, a), pt(-n, a)),
                 ("through centre (expect not ball 6)", pt(n, a), pt(-n, -a))]
        for name, p, q in cases:
            st, adim = S.bit_face_status(Y, p, q, g0, rng)
            print("seed %d %-36s status %-10s adim %s" % (s, name, st, adim), flush=True)
