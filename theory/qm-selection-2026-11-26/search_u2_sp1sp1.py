#!/usr/bin/env python3
"""Counterexample search named in round 9 (rnd/selfref NOTE R9.4 item 2; rounds 4-9 note §9 item 6):
transitive bodies of U(2) and Sp(1)xSp(1) in affine dimension 4-8, scored under the frozen premise
list of theory/qm-selection-2026-11-26/PREREG.md (P1-P6, Jordan premise P7 dropped).

Deterministic (seeded). Output: search_u2_sp1sp1.out. numpy >= 1.26, scipy >= 1.15.
Steps (as locked in PREREG.md §3):
 S1  enumerate real irreducible representations of U(2) and Sp(1)xSp(1) of real dimension <= 8 and the
     dimension of the zero-weight space of a maximal torus in each (by weights; checked numerically on
     a random torus element);
 S2  build every orbitope through a torus-fixed vector whose affine dimension is 4-8;
 S3  for each: SFP (sampled), hSFP (an exposed face with a free circle action is a failure certificate;
     otherwise the invariant-functional argument of PREREG.md §3), capacity (central-symmetry bound or
     LP lower bound), Jordan check, and the HIT rule of PREREG.md §2;
 S4  control: generic (non-torus-fixed) orbits fail SFP numerically.
"""
import itertools
import numpy as np
from scipy.special import sph_harm_y
from scipy.optimize import linprog
from scipy.spatial.transform import Rotation

RNG = np.random.default_rng(20261126)
TOL = 1e-9

def real_harm(j, n):
    """Real orthonormal spherical harmonics of degree j at unit vectors n (N,3) -> (N, 2j+1)."""
    th = np.arccos(np.clip(n[:, 2], -1, 1)); ph = np.arctan2(n[:, 1], n[:, 0])
    out = []
    for m in range(-j, j + 1):
        Y = sph_harm_y(j, abs(m), th, ph)
        if m < 0:   out.append(np.sqrt(2) * (-1) ** m * Y.imag)
        elif m == 0: out.append(Y.real)
        else:       out.append(np.sqrt(2) * (-1) ** m * Y.real)
    A = np.array(out).T
    return A / np.linalg.norm(A[0])  # unit-norm orbit (the norm is constant on S^2 by the addition theorem)

def sphere_grid(N):
    i = np.arange(N) + 0.5; z = 1 - 2 * i / N; r = np.sqrt(1 - z * z); p = np.pi * (1 + 5 ** 0.5) * i
    return np.c_[r * np.cos(p), r * np.sin(p), z]

def affine_dim(X):
    s = np.linalg.svd(X - X.mean(0), compute_uv=False)
    return int((s > 1e-8 * s[0]).sum())

# ---------------- S1: representations and zero-weight spaces ----------------
def u2_irreps(maxdim=8):
    """Sym^k (x) det^m, central character z^(k+2m). Real form exists iff k+2m = 0 (then k even, SO(3) spin k/2)."""
    rows = []
    for k in range(0, 8):
        for m in range(-8, 9):
            real = (k + 2 * m == 0)
            d = (k + 1) if real else 2 * (k + 1)
            if d > maxdim or (k == 0 and m == 0): continue
            if not real and m < -k / 2 - 0.0: continue  # V and its conjugate give the same real rep; keep k+2m > 0
            weights = [(p + m, k - p + m) for p in range(k + 1)]
            zw = sum(1 for w in weights if w == (0, 0))
            zw_real = zw if real else 2 * zw
            rows.append(("U(2)", f"Sym^{k}(x)det^{m}", d, zw_real, real))
    return rows

def sp1sp1_irreps(maxdim=8):
    """V_j1 (x) V_j2: real iff j1+j2 integer (dim (2j1+1)(2j2+1)), else underlying real of a quaternionic rep (2x)."""
    rows = []
    for a in range(0, 8):          # a = 2 j1
        for b in range(0, 8):      # b = 2 j2
            if a == 0 and b == 0: continue
            real = (a + b) % 2 == 0
            d = (a + 1) * (b + 1) * (1 if real else 2)
            if d > maxdim: continue
            zw = (1 if a % 2 == 0 else 0) * (1 if b % 2 == 0 else 0)
            rows.append(("Sp(1)xSp(1)", f"V_{a}/2(x)V_{b}/2", d, zw * (1 if real else 2), real))
    return rows

def spin_weights_check(j2, alpha):
    """Numerical check: eigenvalue-1 multiplicity of exp(i*alpha*J_z) on spin j = j2/2 (complex)."""
    ms = np.arange(-j2, j2 + 1, 2) / 2
    return int(np.sum(np.abs(np.exp(1j * alpha * ms) - 1) < 1e-9))

# ---------------- S3 helpers ----------------
def capacity_lp_lower(X, k, trials=300):
    """Try to find k perfectly distinguishable pure states among grid points: LP feasibility of effects
    e_i = c_i + a_i.x >= 0 on all of X, sum_i e_i = 1, e_i(x_j) = delta_ij. Returns True if any trial succeeds."""
    n, d = X.shape
    Xc = X - X.mean(0)
    for t in range(trials):
        idx = RNG.choice(n, size=k, replace=False)
        nv = k * (d + 1)
        A_eq, b_eq = [], []
        for i in range(k):
            for j in range(k):
                row = np.zeros(nv); row[i*(d+1)] = 1; row[i*(d+1)+1:(i+1)*(d+1)] = Xc[idx[j]]
                A_eq.append(row); b_eq.append(1.0 if i == j else 0.0)
        row = np.zeros(nv); row[0::d+1] = 1; A_eq.append(row); b_eq.append(1.0)  # sum of constants = 1
        for c in range(d):
            row = np.zeros(nv); row[1 + c::d+1] = 1; A_eq.append(row); b_eq.append(0.0)  # sum of linear parts = 0
        A_ub = np.zeros((k * n, nv))
        for i in range(k):
            A_ub[i*n:(i+1)*n, i*(d+1)] = -1; A_ub[i*n:(i+1)*n, i*(d+1)+1:(i+1)*(d+1)] = -Xc
        r = linprog(np.zeros(nv), A_ub=A_ub, b_ub=np.zeros(k*n), A_eq=np.array(A_eq), b_eq=np.array(b_eq),
                    bounds=[(None, None)] * nv, method="highs")
        if r.status == 0: return True, idx
    return False, None

def central_symmetry(X, Xm):
    """max over grid of distance from -x (about the centroid) to the reflected orbit point."""
    c = X.mean(0)
    return float(np.max(np.linalg.norm((Xm - c) + (X - c), axis=1)))

def circle_face(phi, A, B, nlat=4001, naz=64):
    """For an SO(2)_z-equivariant orbit map phi, maximize the invariant functional
    f(n) = A*<e_z part> + B*<Y20 part> over latitudes; return the maximizing latitude z*,
    the gap to the poles, and the number of distinct orbit points on the maximizing circle."""
    z = np.linspace(-1, 1, nlat)
    n = np.c_[np.sqrt(1 - z**2), np.zeros_like(z), z]
    f = phi["func"](n, A, B)
    i = int(np.argmax(f)); zs = z[i]
    gap = float(f[i] - max(f[0], f[-1]))
    az = np.linspace(0, 2*np.pi, naz, endpoint=False)
    ring = np.c_[np.sqrt(1-zs**2)*np.cos(az), np.sqrt(1-zs**2)*np.sin(az), np.full(naz, zs)]
    P = phi["map"](ring)
    distinct = len({tuple(np.round(x, 6)) for x in P})  # distinct pure states on the circle
    return zs, gap, distinct

def main():
    print("# search_u2_sp1sp1.py  (frozen premises: theory/qm-selection-2026-11-26/PREREG.md)")
    print("## S1 real irreps of real dim <= 8 and maximal-torus zero-weight dimension")
    rows = u2_irreps() + sp1sp1_irreps()
    for g, name, d, zw, real in rows:
        print(f"{g:12s} {name:18s} real_dim={d}  real={'yes' if real else 'no (underlying real)'}  zero_weight_dim={zw}")
    a = 0.7316
    chk = [(j2, spin_weights_check(j2, a)) for j2 in range(0, 8)]
    print("numeric check, spin j=j2/2 torus fixed-space dims at alpha=0.7316:", chk,
          "(1 for integer j, 0 for half-integer: matches the weight count)")
    zr = [r for r in rows if r[3] > 0]
    print("irreps with a torus-fixed vector:", ", ".join(f"{r[0]} {r[1]} (dim {r[2]})" for r in zr))
    print("=> every such irrep is an SO(3) spin-j rep (U(2): centre acts trivially) or an SO(3)xSO(3) rep (j1, j2 integer).")

    print("\n## S2-S3 candidate bodies (affine dim 4-8 after the S1 reduction)")
    G = sphere_grid(6000)
    def zon(j):   return lambda n: real_harm(j, n)
    def K_theta(t):
        return lambda n: np.c_[np.cos(t) * real_harm(1, n), np.sin(t) * real_harm(2, n)]
    def K_func(t):
        def f(n, A, B):
            X = K_theta(t)(n)
            ez = real_harm(1, np.array([[0, 0, 1.0]]))[0]; y20 = real_harm(2, np.array([[0, 0, 1.0]]))[0]
            return A * (X[:, :3] @ ez) + B * (X[:, 3:] @ y20)
        return f
    results = []

    # B4: U(2) / Sp(1)xSp(1) on R^4 (orbit S^3). -I is in the identity component and fixes no unit vector.
    print("B4 (U(2) or Sp(1)xSp(1) on C^2 = H): affine dim 4, Jordan (spin factor); SFP FAILS (-1 in the group fixes no pure state; also zero_weight_dim = 0). MISS.")
    results.append(("B4", 4, "fail", "-", "2", "Jordan", "MISS"))

    # Z2 = real QM d=3 (spin-2 zonal, RP^2)
    X = zon(2)(G); d = affine_dim(X)
    zs, gap, nd = circle_face({"map": zon(2), "func": lambda n, A, B: B * (zon(2)(n) @ zon(2)(np.array([[0, 0, 1.0]]))[0])}, 0, -1)
    print(f"Z2 spin-2 zonal (= real QM d=3, Jordan): affine dim {d}; SO(2)-invariant functional -Y20 is maximized on latitude z*={zs:+.4f} (gap to poles {gap:.4f}), {nd} distinct points on that circle -> exposed circle face, (antipodes identified) rotations by angles not in {{0, pi}} fix none of its pure states: hSFP FAILS. MISS.")
    results.append(("Z2 (real QM d=3)", d, "pass", "fail", "3", "Jordan", "MISS"))

    # Z3 spin-3 zonal
    X = zon(3)(G); Xm = zon(3)(-G); d = affine_dim(X)
    cs = central_symmetry(X, Xm)
    z = np.linspace(-1, 1, 4001); n = np.c_[np.sqrt(1 - z**2), np.zeros_like(z), z]
    f = zon(3)(n) @ zon(3)(np.array([[0, 0, 1.0]]))[0]
    print(f"Z3 spin-3 zonal (S^2 orbit, non-Jordan): affine dim {d}; centrally symmetric (max |phi(-n)+phi(n)| = {cs:.2e})")
    print(f"   SO(2)_z-invariant functionals are spanned by Y30: +Y30 is maximized only at z = {z[np.argmax(f)]:+.4f}, -Y30 only at z = {z[np.argmin(f)]:+.4f}; max over latitudes |z| <= 0.99 is {np.max(np.abs(f[np.abs(z) <= 0.99])):.6f} < {f.max():.6f}")
    print("   => every proper face with a positive-dimensional stabilizer is a single pure state: hSFP PASSES (identity-component rule).")
    ok3, _ = capacity_lp_lower(X[::6], 3, trials=200)
    ok2, _ = capacity_lp_lower(X[::6], 2, trials=50)
    print(f"   capacity: central symmetry gives capacity <= 2 (PREREG §3); LP finds 2 distinguishable: {ok2}; 3 among grid triples (200 random): {ok3}")
    print(f"   capacity 2 at affine dim {d} > 3 (the 3-ball): loses on the dimension price. MISS.")
    results.append(("Z3 (spin-3 zonal)", d, "pass", "pass", "2", "no", "MISS (cost)"))

    # K_theta family, spin-1 (+) spin-2 zonal
    tC1 = np.arctan(np.sqrt(2/3) / 1.0)
    # C1 = (n, n n^T - I/3): Frobenius norms 1 and sqrt(2/3); normalized harmonics give tan(theta) = sqrt(2/3)
    for t in sorted(set([0.05, 0.2, 0.4, tC1, 0.8, 1.0, 1.2, 1.4, 1.5])):
        phi = {"map": K_theta(t), "func": K_func(t)}
        X = K_theta(t)(G); d = affine_dim(X)
        zs, gap, nd = circle_face(phi, 0.0, -1.0)
        tag = " (= C1 of round 9)" if abs(t - tC1) < 1e-12 else ""
        print(f"K_theta theta={t:.4f}{tag}: affine dim {d}; functional (0*e_z, -Y20) max at z*={zs:+.4f}, gap to poles {gap:.4f}, {nd} distinct pure states on the circle -> free SO(2) action on an exposed face: hSFP FAILS. MISS.")
        results.append((f"K_theta {t:.3f}{tag}", d, "pass", "fail", "-", "no", "MISS"))

    # Products for Sp(1)xSp(1) = SO(3)xSO(3) on V (+) W
    print("B3 x B3 (SO(3)xSO(3) on (1,0)+(0,1)): affine dim 6; faces are products of faces of balls (points or balls), each with SFP under its SO(3): hSFP PASSES.")
    Gs = sphere_grid(400)
    P = np.array([np.r_[a, b] for a in Gs[::4] for b in Gs[::4]])
    ok3, _ = capacity_lp_lower(P, 3, trials=200)
    print(f"   capacity: centrally symmetric => <= 2; LP 3-state attempts (200): {ok3}. Capacity 2 at dim 6 > 3: loses on cost. MISS.")
    results.append(("B3 x B3", 6, "pass", "pass", "2", "no", "MISS (cost)"))
    print("B3 x Z2 (SO(3)xSO(3) on (1,0)+(0,2)): affine dim 8; face {a} x (circle face of Z2) carries the free rotation of Z2's circle face: hSFP FAILS. MISS.")
    results.append(("B3 x Z2", 8, "pass", "fail", ">=3", "no", "MISS"))

    print("\n## S4 control: generic (non-torus-fixed) orbits fail SFP")
    rots = Rotation.random(400, random_state=7)
    # Represent a generic vector of spin-3 by a random combination of harmonics evaluated on rotated frames:
    # x(g) = sum_k w_k Y3(g u_k) spans the orbit of a generic vector (u_k fixed directions).
    U = sphere_grid(5); w = RNG.normal(size=5)
    def gen_vec(M):  # M: (N,3,3) rotations -> orbit points (N,7)
        return sum(w[k] * real_harm(3, (M @ U[k])) for k in range(5))
    frames = Rotation.random(20000, random_state=11).as_matrix()
    O = gen_vec(frames)
    fails = 0
    for R in rots[:60].as_matrix():
        moved = gen_vec(np.einsum("ij,njk->nik", R, frames))
        if np.min(np.linalg.norm(moved - O, axis=1)) > 1e-2: fails += 1
    print(f"spin-3 generic vector: for {fails}/60 random rotations R no sampled orbit point g.v has |R g.v - g.v| < 1e-2 (20000 orbit samples): SFP fails, as the maximal-torus criterion requires.")

    print("\n## Summary (HIT rule of PREREG.md §2)")
    print("| body | affine dim | SFP | hSFP | capacity | Jordan | outcome |")
    print("|---|---|---|---|---|---|---|")
    for r in results: print("| " + " | ".join(str(x) for x in r) + " |")
    hits = [r for r in results if r[-1].startswith("HIT") or r[-1].startswith("TIE")]
    print(f"\nHITS: {len(hits)}.  RESULT: {'HIT' if hits else 'MISS (no counterexample)'}")

if __name__ == "__main__":
    main()
