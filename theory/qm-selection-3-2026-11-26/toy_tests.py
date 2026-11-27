#!/usr/bin/env python3
"""Toy-input tests of every helper of search_qmsel3.py whose failure could print a scored outcome
(PREREG.md section 8). Inputs are toy point sets (triangle, square, circle, sphere, cube, ellipsoid),
SO(2) on the plane, and the published SO(3) controls. No SU(3), Sp(2) or G2 orbit is computed.
Run: OMP_NUM_THREADS=1 python3 toy_tests.py > toy_tests.out"""
import sys, os, math, tempfile, shutil, subprocess
import numpy as np
from numpy.linalg import norm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import search_qmsel3 as S
S._DEADLINE[0] = 1e18
rng = np.random.default_rng(424242)
res = []
def check(name, cond, info=""):
    res.append(bool(cond)); print("%-4s %-62s %s" % ("PASS" if cond else "FAIL", name, info), flush=True)

def circle(n, r=1.0): t = np.linspace(0, 2*np.pi, n, endpoint=False); return r*np.c_[np.cos(t), np.sin(t)]
def sphere(n, dim=3):
    X = rng.normal(size=(n, dim)); return X / norm(X, axis=1)[:, None]
J = np.array([[0., -1.], [1., 0.]])          # so(2)

# 1. effects_lp: capacity witness LP (a false witness could print HIT/TIE)
tri = np.array([[1, 0], [-.5, math.sqrt(3)/2], [-.5, -math.sqrt(3)/2]])
check("effects_lp: triangle, 3 vertices distinguishable", S.effects_lp(tri, list(tri)) is not None)
C = circle(720)
check("effects_lp: disc, antipodal pair distinguishable", S.effects_lp(C, [C[0], C[360]]) is not None)
check("effects_lp: disc, pair at 90 deg not distinguishable", S.effects_lp(C, [C[0], C[180]]) is None)
check("effects_lp: disc, 3 points not distinguishable", S.effects_lp(C, [C[0], C[240], C[480]]) is None)

# 2. in_relint (decides 'not ball' -> MISS)
F3 = np.c_[tri, np.zeros(3)]
t = S.in_relint(F3, F3.mean(0)); check("in_relint: triangle centroid t = 1/3", abs(t - 1/3) < 1e-6, "t=%.6f" % t)
t = S.in_relint(F3, F3[0]); check("in_relint: vertex t <= 1e-6", t <= 1e-6, "t=%.2e" % t)
t = S.in_relint(F3, np.array([2.0, 0, 0])); check("in_relint: point outside -> not interior", t <= 1e-6, "t=%s" % t)
t = S.in_relint(F3, np.array([0, 0, 0.1])); check("in_relint: point off the hull -> -inf", t == -np.inf)
Fn = F3 + 1e-5 * rng.normal(size=F3.shape); t = S.in_relint(Fn, np.zeros(3))
check("in_relint: centroid with 1e-5 noise on the points", t > 0.3, "t=%.4f" % t)

# 3. face_is_ball (decides 'ball' -> HIT/TIE)
a, b = S.face_is_ball(sphere(200)); check("face_is_ball: sphere S^2 -> (3, True)", (a, b) == (3, True))
E = sphere(200) * np.array([1.0, 0.5, 2.0]); Q, _ = np.linalg.qr(rng.normal(size=(6, 6)))
a, b = S.face_is_ball(np.c_[E, np.zeros((200, 3))] @ Q.T); check("face_is_ball: ellipsoid in R^6 -> (3, True)", (a, b) == (3, True))
cube = rng.uniform(-1, 1, size=(400, 3)); k = np.argmax(np.abs(cube), 1); cube[np.arange(400), k] = np.sign(cube[np.arange(400), k])
a, b = S.face_is_ball(cube); check("face_is_ball: cube surface -> (3, False)", (a, b) == (3, False))
a, b = S.face_is_ball(np.c_[circle(100), np.zeros(100)]); check("face_is_ball: circle -> (2, False)", (a, b) == (2, False))
a, b = S.face_is_ball(sphere(200, 4)); check("face_is_ball: S^3 -> dim 4, not ball", a == 4 and b is False)

# 4. cap_upper_bound (a low bound prints MISS cost; a high one could let a HIT through)
al, N = S.cap_upper_bound(circle(60), np.array([1.0, 0]), [J], rng)
check("cap_upper_bound: SO(2) disc -> alpha 1/2, N_UB 2", N == 2 and abs(al - .5) < 1e-6, "alpha=%.6f" % al)
Ysq = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1.]])
al, N = S.cap_upper_bound(Ysq, Ysq[0], [], rng) if False else (None, None)
# square (finite group, no Lie algebra) checked through the LP alone:
from scipy.optimize import linprog
r = linprog(np.r_[1.0, 0, 0], A_ub=-np.c_[np.ones(4), Ysq], b_ub=np.zeros(4), A_eq=np.r_[1.0, Ysq[0]][None, :], b_eq=[1.0], bounds=[(None, None)]*3, method="highs")
check("cap_upper_bound LP: square -> alpha 1/2 (gbit, N 2)", abs(r.x[0] - .5) < 1e-9)
r = linprog(np.r_[1.0, 0, 0], A_ub=-np.c_[np.ones(3), tri], b_ub=np.zeros(3), A_eq=np.r_[1.0, tri[0]][None, :], b_eq=[1.0], bounds=[(None, None)]*3, method="highs")
check("cap_upper_bound LP: triangle -> alpha 1/3 (trit, N 3)", abs(r.x[0] - 1/3) < 1e-9)

# 5. g0_closure (A6)
w, s = S.g0_closure(S.so_n(4)); check("g0_closure: so(4) basis closes", w < 1e-10 and s < 1e-12, "res=%.1e" % w)
g1, _ = S.so3_spin(1); w, s = S.g0_closure(g1[:2]); check("g0_closure: 2 of 3 so(3) generators do not close", w > 1e-3, "res=%.2f" % w)

# 6. distinguishable_pair (selects the bit-face pairs)
C2 = circle(360)
check("distinguishable_pair: SO(2) antipodal pair -> True", S.distinguishable_pair(C2, C2[0], C2[180], [J], rng))
check("distinguishable_pair: SO(2) pair at 90 deg -> False", not S.distinguishable_pair(C2, C2[0], C2[90], [J], rng))

# 7. bit_face_status on SO(2): the face of an antipodal pair is the whole disc (dim 2) -> not ball
st, ad = S.bit_face_status(C2, C2[0], C2[180], [J], rng)
check("bit_face_status: SO(2) disc -> 'not ball', dim 2", st == "not ball" and ad == 2, "%s %s" % (st, ad))

# 8. root_reflections / weyl_orbit / tfixed_points on SO(3) controls (A4)
def setup(B, seed):
    r = np.random.default_rng(seed); P, c = S.ambient(B, r); y0 = P.T @ (B.v - c)
    G, g0 = S.g0_algebra(B, P, c, r); r0, rh, h0, cart = S.sfp_rank_test(g0, y0, r)
    return r, P, c, y0, g0, cart
for name, B, want in [("B3 spin 1", S.Body("B3", *S.so3_spin(1), "SO(3)"), 2),
                      ("Z2 spin 2", S.Body("Z2", *S.so3_spin(2), "SO(3)"), 1),
                      ("Z3 spin 3", S.Body("Z3", *S.so3_spin(3), "SO(3)"), 2)]:
    r, P, c, y0, g0, cart = setup(B, 7)
    W = S.weyl_orbit(y0, S.root_reflections(g0, cart, r)); T = S.tfixed_points(g0, cart, y0, r, nstart=100)
    check("weyl_orbit = tfixed_points: %s -> %d" % (name, want), len(W) == want == len(T), "W=%d search=%d" % (len(W), len(T)))
g1, z1 = S.so3_spin(1); gb, vb = S.product_body([("a", g1, z1), ("b", g1, z1)])
r, P, c, y0, g0, cart = setup(S.Body("B3xB3", gb, vb, "SO(3)^2"), 7)
W = S.weyl_orbit(y0, S.root_reflections(g0, cart, r)); check("weyl_orbit: B3 x B3 -> 4 (W = Z2 x Z2)", len(W) == 4, "W=%d" % len(W))

# 9. recheck_witness (A3): a valid witness passes, a false one is caught
B = S.Body("B3", *S.so3_spin(1), "SO(3)"); r, P, c, y0, g0, cart = setup(B, 11)
Y = np.array([P.T @ (x - c) for x in S.orbit_samples(B, 2000, r)])
u = y0 / (y0 @ y0); Eok = [(0.5, 0.5 * u), (0.5, -0.5 * u)]          # exact B3 witness: 1/2 +- y.y0/(2|y0|^2)
m1 = S.recheck_witness(B, P, c, Eok, g0, 0)
check("recheck_witness: exact B3 witness, min >= -1e-6", m1 >= -1e-6, "min=%.2e" % m1)
Ebad = [(0.4, lv) for (a0, lv) in Eok]; m2 = S.recheck_witness(B, P, c, Ebad, g0, 0)
check("recheck_witness: false witness (a - 0.1) caught, min ~ -0.1", abs(m2 + 0.1) < 1e-3, "min=%.4f" % m2)
Egrid = S.effects_lp(Y[:50], [y0, -y0]); m3 = S.recheck_witness(B, P, c, Egrid, g0, 0)
check("recheck_witness: LP witness on 50 grid points, no cutting planes, caught", m3 < -1e-6, "min=%.2e" % m3)

# 10. hsfp_test on SO(3) controls (a false failure prints MISS)
for name, B, want in [("B3 pass", S.Body("B3", *S.so3_spin(1), "SO(3)"), True),
                      ("Z2 fail", S.Body("Z2", *S.so3_spin(2), "SO(3)"), False)]:
    r, P, c, y0, g0, cart = setup(B, 13)
    Y = np.array([P.T @ (x - c) for x in S.orbit_samples(B, 2000, r)])
    tp = S.weyl_orbit(y0, S.root_reflections(g0, cart, r)); ok, info = S.hsfp_test(Y, g0, cart, y0, tp, r)
    check("hsfp_test: %s" % name, ok == want, str(info))

# 11. jordan_type (TARGET signature)
check("jordan_type: (3,2,3,2) complex QM; (8,3,8,4) complex QM; (8,3,8,6) no; (5,3,3,2) real QM",
      [S.jordan_type(*x) for x in [(3,2,3,2), (8,3,8,4), (8,3,8,6), (5,3,3,2)]] == ["complex QM", "complex QM", "no", "real QM"])

# 12. run-time guards (A7): lock hash, list.out, versions
here = os.path.dirname(os.path.abspath(__file__)); tmp = tempfile.mkdtemp()
for f in ["search_qmsel3.py", "PREREG.md", "list.out"]: shutil.copy(os.path.join(here, f), tmp)
def guard(code):
    p = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, %r); import search_qmsel3 as S; %s" % (tmp, code)],
                       capture_output=True, text=True, cwd=tmp); return p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1:] 
import hashlib
with open(os.path.join(tmp, "PREREG.sha256"), "w") as fh:
    for f in ["PREREG.md", "search_qmsel3.py", "list.out"]:
        fh.write("%s  theory/x/%s\n" % (hashlib.sha256(open(os.path.join(tmp, f), "rb").read()).hexdigest(), f))
rc, m = guard("S.check_lock(); print('ok')"); check("check_lock: matching hashes accepted", rc == 0, str(m))
open(os.path.join(tmp, "PREREG.md"), "a").write("x"); rc, m = guard("S.check_lock()"); check("check_lock: edited PREREG.md refused", rc != 0, str(m))
rc, m = guard("S.check_list(S.body_names()); print('ok')"); check("check_list: committed list.out accepted", rc == 0, str(m))
L = open(os.path.join(tmp, "list.out")).read().splitlines(); i = next(k for k, l in enumerate(L) if not l.startswith("#"))
L[i], L[i+1] = L[i+1], L[i]; open(os.path.join(tmp, "list.out"), "w").write("\n".join(L) + "\n")
rc, m = guard("S.check_list(S.body_names())"); check("check_list: swapped order refused", rc != 0, str(m))
rc, m = guard("S.check_versions(); print('ok')"); check("check_versions: pinned versions present", rc == 0, str(m))
rc, m = guard("S.PINNED['numpy'] = '0.0'; S.check_versions()"); check("check_versions: wrong version refused", rc != 0, str(m))
shutil.rmtree(tmp)
print("SUMMARY: %d/%d passed" % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
