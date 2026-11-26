#!/usr/bin/env python3
"""Third QM-selection counterexample search (prereg: PREREG.md in this directory). It supersedes
../qm-selection-2-2026-11-26 (lock 641c695, gate read FAILED on method; never run) and implements the
gate read's amendments A1-A10.

Groups: SU(3), Sp(2) (acting through SO(5)) and G2, affine dimension 4-15; U(2) (through SO(3)),
Sp(1)^2, Sp(1)^3 (through SO(3)^k) and G x Sp(1)^k, affine dimension 9-15. Premises P1-P6 frozen in
../qm-selection-2026-11-26/PREREG.md; P7 (Jordan) dropped.

Modes:
  python3 search_qmsel3.py --selftest   construction checks of every representation (closure and
                                        antisymmetry only) and the SO(3) controls whose outcomes are
                                        already published (B3, Z3, C1, Z2, B3 x B3). Allowed before the gate.
  python3 search_qmsel3.py --list       the enumeration (index, name, group, dimension); no outcome.
  python3 search_qmsel3.py --run [--workers=N]
                                        the scored search. NOT to be run before a separate reader passes
                                        the Gate of PREREG.md. Refuses to start unless the files match
                                        PREREG.sha256, the versions are the pinned ones (PINNED) and the
                                        regenerated enumeration equals list.out.
Seeds: default_rng(SEED + body_index) per body, SEED = 20261127; recheck SEED + 10^6 + index.
"""
import sys, itertools, json, math
import numpy as np
from numpy.linalg import svd, norm, eig
from scipy.linalg import expm, null_space
from scipy.optimize import linprog, minimize

SEED = 20261127
TOL_RANK = 1e-7
N_GRID = 6000          # orbit samples for the capacity upper-bound LP and face maxima
ANG_STEP_DEG = 3       # angle grid for multiplicity-2 summands (full circle)
N_FUNC = 24            # invariant functionals per flat in the hSFP test
EPS_LIST = (1.0,)     # depth 1 only: faces of exposure depth >= 2 are declared untested (A1)
FAIL_TOL = 1e-6        # hSFP failure certificate threshold (relative to orbit radius), every eps (A4)
CONFIRM_FACTOR = 5     # a failure certificate is re-confirmed with 5x more starts (A4)
G0_CLOSURE_TOL = 1e-8  # per-body closure/antisymmetry residual of the g0 basis (A6)
RECHECK_N = 100000     # fresh orbit points for the capacity-witness recheck (A3)
RECHECK_STARTS = 100   # local-minimisation starts in the recheck (A3)
RECHECK_SEED_OFFSET = 10**6
UB_SLACK = 1e-4        # N_UB = floor(1/alpha + UB_SLACK)
PINNED = {"numpy": "2.5.5", "scipy": "1.18.1", "python": "3.13.5"}   # A7
BODY_BUDGET_S = 3600   # wall-clock budget per body; a body that runs out is scored OPEN (time budget)

import time
class OutOfBudget(Exception): pass
_DEADLINE = [float("inf")]
def tick():
    if time.time() > _DEADLINE[0]: raise OutOfBudget()

# ---------------------------------------------------------------- Lie algebra helpers
def orth_basis(mats, tol=TOL_RANK):
    if not mats: return []
    d = mats[0].shape[0]
    M = np.array([m.ravel() for m in mats])
    u, s, vt = svd(M, full_matrices=False)
    k = int((s > tol * max(s[0], 1e-300)).sum())
    return [vt[i].reshape(d, d) for i in range(k)]

def comm(a, b): return a @ b - b @ a

def null_abs(M, tol):
    """null space with an ABSOLUTE singular-value tolerance (scipy's rcond is relative to the largest
    singular value, which misclassifies an all-round-off matrix as full rank)."""
    u, s, vt = svd(M, full_matrices=True)
    k = int((s > tol).sum())
    return vt[k:].T

def centralizer(Y, basis):
    if not basis: return []
    C = np.array([comm(Y, B).ravel() for B in basis]).T
    ns = null_abs(C, 1e-8 * max(norm(Y), 1e-300) * max(norm(B) for B in basis))
    return orth_basis([sum(c * B for c, B in zip(col, basis)) for col in ns.T])

def rank_of(basis, rng):
    if not basis: return 0, []
    Y = sum(rng.normal() * B for B in basis)
    cart = centralizer(Y, basis)
    return len(cart), cart

def common_kernel(mats, d):
    if not mats: return np.eye(d)
    return null_space(np.vstack(mats), rcond=1e-9)

# ---------------------------------------------------------------- representations
def so3_spin(j):
    """real antisymmetric generators (Lx, Ly, Lz) of SO(3) spin j in the real-harmonic basis."""
    m = np.arange(-j, j + 1)
    Jz = np.diag(m).astype(complex)
    Jp = np.zeros((2*j+1, 2*j+1), complex)
    for k in range(2*j):
        mm = m[k]; Jp[k+1, k] = math.sqrt(j*(j+1) - mm*(mm+1))
    Jx = (Jp + Jp.conj().T) / 2; Jy = (Jp - Jp.conj().T) / (2j)
    # complex -> real harmonics
    C = np.zeros((2*j+1, 2*j+1), complex)
    for k, mm in enumerate(m):
        if mm == 0: C[k, k] = 1
        elif mm > 0:
            C[k, j+mm] = (-1)**int(mm) / math.sqrt(2); C[k, j-mm] = 1 / math.sqrt(2)
        else:
            a = int(-mm)
            C[k, j-a] = 1j / math.sqrt(2); C[k, j+a] = -1j * (-1)**a / math.sqrt(2)
    gens = []
    for J in (Jx, Jy, Jz):
        L = C @ (-1j * J) @ C.conj().T
        assert norm(L.imag) < 1e-9, "real form failed"
        gens.append(L.real)
    zonal = np.zeros(2*j+1); zonal[j] = 1.0   # m = 0 component
    return gens, zonal

def gellmann():
    l = np.zeros((8, 3, 3), complex)
    l[0][0,1]=l[0][1,0]=1; l[1][0,1]=-1j; l[1][1,0]=1j; l[2][0,0]=1; l[2][1,1]=-1
    l[3][0,2]=l[3][2,0]=1; l[4][0,2]=-1j; l[4][2,0]=1j; l[5][1,2]=l[5][2,1]=1
    l[6][1,2]=-1j; l[6][2,1]=1j; l[7]=np.diag([1,1,-2])/math.sqrt(3)
    return l

def su3_adjoint():
    l = gellmann(); X = [1j * a for a in l]
    gens = []
    for x in X:
        M = np.zeros((8, 8))
        for c in range(8):
            br = x @ l[c] - l[c] @ x
            for b in range(8): M[b, c] = np.real(np.trace(l[b] @ br)) / 2
        gens.append(M)
    cart_vectors = [np.eye(8)[2], np.eye(8)[7]]   # lambda3, lambda8 directions (zero weight space)
    return gens, cart_vectors

def so_n(n):
    g = []
    for i in range(n):
        for k in range(i+1, n):
            E = np.zeros((n, n)); E[i, k] = 1; E[k, i] = -1; g.append(E)
    return g

def rep_on_basis(gens, basis, action):
    """matrix of X acting on span(basis) (orthonormal list of arrays) via action(X, B)."""
    out = []
    for X in gens:
        M = np.array([[np.sum(Bb * action(X, Bc)) for Bc in basis] for Bb in basis]); out.append(M)
    return out

def so5_reps():
    g5 = so_n(5)
    # 10 = adjoint (antisymmetric matrices), orthonormal Frobenius basis
    b10 = [E / math.sqrt(2) for E in g5]
    g10 = rep_on_basis(g5, b10, lambda X, B: comm(X, B))
    # 14 = traceless symmetric
    b14 = []
    for i in range(5):
        for k in range(i+1, 5):
            S = np.zeros((5, 5)); S[i, k] = S[k, i] = 1 / math.sqrt(2); b14.append(S)
    D = [np.diag(r) for r in null_space(np.ones((1, 5))).T]
    b14 += orth_basis(D)
    b14 = orth_basis(b14)
    g14 = rep_on_basis(g5, b14, lambda X, B: comm(X, B))
    return {"5": g5, "10": g10, "14": g14}

def g2_reps():
    trip = [(1,2,3,1),(1,4,5,1),(1,6,7,1),(2,4,6,1),(2,5,7,-1),(3,4,7,-1),(3,5,6,-1)]
    phi = np.zeros((7, 7, 7))
    for a, b, c, s in trip:
        a, b, c = a-1, b-1, c-1
        for p in itertools.permutations([0, 1, 2]):
            idx = [(a, b, c)[q] for q in p]
            sign = np.linalg.det(np.eye(3)[list(p)])
            phi[tuple(idx)] = s * sign
    so7 = so_n(7)
    def act(X):  # X . phi
        return (np.einsum('ia,ajk->ijk', X, phi) + np.einsum('ja,iak->ijk', X, phi) + np.einsum('ka,ija->ijk', X, phi))
    A = np.array([act(X).ravel() for X in so7]).T
    ns = null_space(A, rcond=1e-9)
    g7 = orth_basis([sum(c * X for c, X in zip(col, so7)) for col in ns.T])
    assert len(g7) == 14, len(g7)
    b14 = [B / norm(B) for B in g7]; b14 = orth_basis(b14)
    g14 = rep_on_basis(g7, b14, lambda X, B: comm(X, B))
    return {"7": g7, "14": g14}

def block(mats_list):
    d = sum(m.shape[0] for m in mats_list); M = np.zeros((d, d)); o = 0
    for m in mats_list:
        k = m.shape[0]; M[o:o+k, o:o+k] = m; o += k
    return M

# ---------------------------------------------------------------- bodies
class Body:
    def __init__(self, name, gens, v, group, family="", known_cp=False):
        self.name, self.group, self.family, self.known_cp = name, group, family, known_cp
        self.gens = orth_basis(gens); self.v = np.asarray(v, float)

def tfixed_space(gens, rng):
    r, cart = rank_of(orth_basis(gens), rng)
    return common_kernel(cart, gens[0].shape[0]), r

def angle_vectors(Vt, step=ANG_STEP_DEG):
    """unit vectors over the full circle in a 2-dim zero-weight space."""
    assert Vt.shape[1] == 2
    return [math.cos(math.radians(a)) * Vt[:, 0] + math.sin(math.radians(a)) * Vt[:, 1]
            for a in range(0, 360, step)]

def singular_angles(gens, Vt, offset=None):
    """Directions u(theta) in a 2-dim zero-weight space where the orbit dimension drops (Weyl-singular
    directions: larger stabilizer in the acting algebra). M(theta) = [X u(theta)] is linear in u; scan
    sigma_r (r = generic rank) at 0.25 deg, refine each local minimum, keep it if sigma_r < 1e-6 x the median of the scan.
    Construction data only (acting group, no orbit sampling). offset: vector added to every u (the
    fixed 5-part of Sp(2) 5+10)."""
    from scipy.optimize import minimize_scalar
    def M(th):
        u = math.cos(th) * Vt[:, 0] + math.sin(th) * Vt[:, 1]
        if offset is not None: u = np.r_[offset, u]
        return np.array([X @ u for X in gens]).T
    r = np.linalg.matrix_rank(M(0.123456), tol=1e-9)
    f = lambda th: svd(M(th), compute_uv=False)[r - 1]
    ths = np.radians(np.arange(0, 360, 0.25)); vals = [f(t) for t in ths]
    out = []
    for k in range(len(ths)):
        if vals[k] <= vals[k - 1] and vals[k] <= vals[(k + 1) % len(ths)]:
            res = minimize_scalar(f, bounds=(ths[k] - 0.005, ths[k] + 0.005), method="bounded",
                                  options={"xatol": 1e-13})
            if res.fun < 1e-6 * np.median(vals):
                a = math.degrees(res.x) % 360
                if all(min(abs(a - b), 360 - abs(a - b)) > 0.01 for b in out): out.append(a)
    return sorted(out)

def singular_vectors(gens, Vt, offset=None):
    return [(a, math.cos(math.radians(a)) * Vt[:, 0] + math.sin(math.radians(a)) * Vt[:, 1])
            for a in singular_angles(gens, Vt, offset)]

# ---------------------------------------------------------------- orbit tools
N_FACTORS = 6         # random group element = product of N_FACTORS one-parameter steps

def random_group_element(G, rng):
    """product of N_FACTORS elements exp(t X), X a random direction of the Lie algebra normalised to
    spectral radius 1, t uniform in [0, 4 pi): spreads over the whole compact group (a single exp of a
    Gaussian combination of Frobenius-normalised generators stays near the identity for large reps)."""
    g = np.eye(G[0].shape[0])
    for _ in range(N_FACTORS):
        X = sum(rng.normal() * h for h in G)
        X /= max(np.abs(np.linalg.eigvals(X)).max(), 1e-300)
        g = expm(rng.uniform(0, 4 * math.pi) * X) @ g
    return g

def orbit_samples(B, n, rng):
    pts = np.empty((n, len(B.v)))
    for i in range(n):
        pts[i] = random_group_element(B.gens, rng) @ B.v
    return pts

def ambient(B, rng):
    """centred coordinates on the affine span of the orbit: returns (P, c) with x_centered = P.T (x - c)."""
    S = orbit_samples(B, 400, rng)
    c = S.mean(0)
    # exact centroid: projection of v on the G-fixed subspace
    Fix = common_kernel(B.gens, len(B.v)); c = Fix @ (Fix.T @ B.v) if Fix.shape[1] else np.zeros(len(B.v))
    u, s, vt = svd((S - c).T, full_matrices=False)
    k = int((s > 1e-8 * s[0]).sum())
    return u[:, :k], c

def g0_algebra(B, P, c, rng, nsamp=None):
    """Lie algebra of all linear vector fields on the span tangent to the orbit (= Lie algebra of the
    identity component G0 of the linear symmetry group of the orbitope), in centred coordinates."""
    d = P.shape[1]
    G = [P.T @ g @ P for g in B.gens]
    nsamp = nsamp or max(60, 4 * d * d)
    rows = []
    for x in orbit_samples(B, nsamp, rng):
        y = P.T @ (x - c)
        T = np.array([g @ y for g in G]).T
        u, s, vt = svd(T, full_matrices=True)
        k = int((s > 1e-8 * max(s[0], 1e-300)).sum())
        Q = u[:, k:]
        if Q.shape[1] == 0: continue
        rows.append(np.kron(y[None, :], Q.T))   # (Q^T A y) in vec(A) row-major
    A = np.vstack(rows)
    ns = null_space(A, rcond=1e-8)
    g0 = orth_basis([col.reshape(d, d) for col in ns.T])
    return G, g0

def sfp_rank_test(g0, y0, rng):
    r0, _ = rank_of(g0, rng)
    h0 = []
    if g0:
        M = np.array([(A @ y0) for A in g0]).T
        ns = null_space(M, rcond=1e-8)
        h0 = orth_basis([sum(c * A for c, A in zip(col, g0)) for col in ns.T])
    rh, carth = rank_of(h0, rng)
    return r0, rh, h0, carth

CUT_ROUNDS = 60       # cutting-plane rounds (UB LP and LB witness LP)
NEG_TOL = 1e-6        # an effect counts as non-negative on the orbit if its orbit minimum >= -NEG_TOL

def orbit_min(a, lvec, g0, Y, rng, k=6):
    """local minimisation of the affine function a + l.x over the orbit, from the k lowest grid points."""
    vals = a + Y @ lvec
    low = Y[np.argsort(vals)[:k]]
    mx, x = local_max(lambda z: -(a + z @ lvec), g0, low, rng)
    return -mx, x

def orbit_mins(a, lvec, g0, Y, rng, k=12):
    """all local minima of a + l.x over the orbit reached from the k lowest grid points."""
    vals = a + Y @ lvec
    out = []
    for y in Y[np.argsort(vals)[:k]]:
        mx, x = local_max(lambda z: -(a + z @ lvec), g0, [y], rng)
        out.append((-mx, x))
    return out

def cap_upper_bound(Y, y0, g0, rng):
    """min alpha s.t. alpha + l.y >= 0 on the point set Y, alpha + l.y0 = 1  (centroid = 0).
    Y is always a subset of the orbit, so alpha_grid <= lambda and N <= floor(1/alpha_grid) is valid
    whatever the grid; cutting planes (orbit points where the optimal effect is most negative) are added
    only to tighten it, and every added point is an orbit point, so validity is kept."""
    n, d = Y.shape
    alpha = None
    for _ in range(CUT_ROUNDS):
        tick()
        n = len(Y)
        cobj = np.r_[1.0, np.zeros(d)]
        A_ub = -np.c_[np.ones(n), Y]; b_ub = np.zeros(n)
        A_eq = np.r_[1.0, y0][None, :]; b_eq = [1.0]
        r = linprog(cobj, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(None, None)] * (d + 1), method="highs")
        if r.status != 0: return None, None
        alpha, lvec = r.x[0], r.x[1:]
        mins = orbit_mins(alpha, lvec, g0, Y, rng)
        if min(mn for mn, x in mins) >= -1e-9: break
        Y = np.vstack([Y] + [x for mn, x in mins if mn < -1e-9])
    return alpha, int(math.floor(1.0 / alpha + UB_SLACK)) if alpha > 0 else None

def local_max(fun_x, Gc, starts, rng, iters=200):
    """maximize fun_x(expm(X) y) over X in span(Gc), from starting points y in starts."""
    best = -np.inf; bx = None
    for y in starts:
        f = lambda a: -fun_x(expm(sum(ai * g for ai, g in zip(a, Gc))) @ y)
        r = minimize(f, np.zeros(len(Gc)), method="BFGS", options={"maxiter": iters, "gtol": 1e-10})
        if -r.fun > best:
            best = -r.fun; bx = expm(sum(ai * g for ai, g in zip(r.x, Gc))) @ y
    return best, bx

def tfixed_points(g0, cart, y0, rng, nstart=300):
    """orbit points fixed by the maximal torus exp(cart): minimise the off-torus-fixed part."""
    d = len(y0)
    K = common_kernel(cart, d); Pp = np.eye(d) - K @ K.T
    pts = []
    for s in range(nstart):
        ys = random_group_element(g0, rng) @ y0          # random start over the whole orbit
        f = lambda a: float(norm(Pp @ (expm(sum(ai * g for ai, g in zip(a, g0))) @ ys)) ** 2)
        r = minimize(f, np.zeros(len(g0)), method="BFGS", options={"maxiter": 400, "gtol": 1e-14})
        if r.fun < 1e-12:
            x = expm(sum(ai * g for ai, g in zip(r.x, g0))) @ ys; x = K @ (K.T @ x)
            if all(norm(x - p) > 1e-5 for p in pts): pts.append(x)
    return pts

def weights(cart, d):
    """weights of the Cartan basis on R^d: list of real vectors mu (mu_i = eigenvalue of cart_i / i)."""
    H = sum((k + 1.37) * C for k, C in enumerate(cart))
    w, V = eig(H)
    mus = []
    for k in range(d):
        vec = V[:, k]
        mu = np.array([np.real((vec.conj() @ (C @ vec)) / (vec.conj() @ vec) / 1j) for C in cart])
        if norm(mu) > 1e-7: mus.append(mu)
    dirs = []
    for mu in mus:
        u = mu / norm(mu)
        if all(min(norm(u - q), norm(u + q)) > 1e-6 for q in dirs): dirs.append(u)
    return dirs

def flats(dirs, r):
    out = [np.zeros((0, r))]
    for k in range(1, r):
        for sub in itertools.combinations(range(len(dirs)), k):
            W = np.array([dirs[i] for i in sub])
            if np.linalg.matrix_rank(W, tol=1e-6) != k: continue
            # close under span: include all dirs in span
            Wb = orth_basis_vec(W)
            if all(not same_span(Wb, F) for F in out): out.append(Wb)
    return out

def orth_basis_vec(W):
    u, s, vt = svd(W, full_matrices=False); k = int((s > 1e-8).sum()); return vt[:k]

def same_span(A, B):
    if A.shape[0] != B.shape[0]: return False
    if A.shape[0] == 0: return True
    return np.linalg.matrix_rank(np.vstack([A, B]), tol=1e-6) == A.shape[0]

def hsfp_test(Y, g0, cart, y0, tpts, rng):
    """For every flat W of the weight arrangement (W proper), generic H in W^perp generates a subtorus S.
    For S-invariant functionals l (in ker H), compare max over the orbit with max over the S-fixed
    pure states (union of Z(S)-orbits of torus-fixed points). A gap > FAIL_TOL is a failure certificate:
    the (minimal exposed) S-invariant face has no S-fixed pure state."""
    d = len(y0); r = len(cart)
    dirs = weights(cart, d)
    rad = norm(y0)
    for W in flats(dirs, r):
        Np = null_space(W) if W.shape[0] else np.eye(r)
        h = Np @ rng.normal(size=Np.shape[1])
        H = sum(hi * C for hi, C in zip(h, cart))
        VH = null_space(H, rcond=1e-9)
        if VH.shape[1] == 0: continue
        Z = centralizer(H, g0)
        for t in range(N_FUNC):
            tick()
            l1 = VH @ rng.normal(size=VH.shape[1]); l1 /= norm(l1)
            l2 = VH @ rng.normal(size=VH.shape[1]); l2 /= norm(l2)
            for eps in EPS_LIST:
                l = l1 + (eps * l2 if eps < 1.0 else 0.0)
                vals = Y @ l
                top = Y[np.argsort(vals)[-6:]]
                M, _ = local_max(lambda x: x @ l, g0, top, rng)
                mH = -np.inf
                for p in tpts:
                    val, _ = local_max(lambda x: x @ l, Z, [p], rng) if Z else (p @ l, p)
                    mH = max(mH, val)
                if M - mH > FAIL_TOL * rad:
                    # A4: re-confirm with CONFIRM_FACTOR x more starts before accepting the certificate
                    top2 = Y[np.argsort(vals)[-6 * CONFIRM_FACTOR:]]
                    M2, _ = local_max(lambda x: x @ l, g0, top2, rng)
                    mH2 = -np.inf
                    for p in tpts:
                        sts = [p] + [random_group_element(Z, rng) @ p for _ in range(CONFIRM_FACTOR - 1)] if Z else [p]
                        val, _ = local_max(lambda x: x @ l, Z, sts, rng) if Z else (p @ l, p)
                        mH2 = max(mH2, val)
                    if max(M, M2) - max(mH, mH2) > FAIL_TOL * rad:
                        return False, {"flat_dim": int(W.shape[0]), "gap": float(max(M, M2) - max(mH, mH2)),
                                       "gap_first": float(M - mH), "eps": eps}
    return True, {"flats": len(flats(dirs, r))}

def root_reflections(g0, cart, rng):
    """For every root pair +-alpha of g0 with respect to the maximal torus exp(span cart), an element
    w_alpha = exp(pi K) of G0 acting on the orbit space, K in the real root space normalised so that ad K
    has eigenvalues 0, +-i on the su(2) it spans with [K, .]: w_alpha normalises T and acts on t as the
    reflection s_alpha. Construction from g0 only."""
    n = len(g0); M = np.array([b.ravel() for b in g0]).T
    def coords(X):
        c, *_ = np.linalg.lstsq(M, X.ravel(), rcond=None); return c
    H = sum((k + 1.37) * C for k, C in enumerate(cart))
    adH = np.array([coords(comm(H, b)) for b in g0]).T          # n x n, ad_H in g0 coordinates
    w, V = eig(adH)
    out = []; seen = []
    for k in range(n):
        if abs(w[k]) < 1e-7: continue
        if w[k].imag < 0: continue
        X = sum(np.real(V[j, k]) * g0[j] for j in range(n))
        if norm(X) < 1e-9: X = sum(np.imag(V[j, k]) * g0[j] for j in range(n))
        X /= norm(X)
        Z = comm(X, H)
        if norm(Z) < 1e-9: continue
        lam2 = norm(comm(X, comm(X, Z))) / norm(Z)
        K = X / math.sqrt(lam2)
        wa = expm(math.pi * K)
        if all(norm(wa - s0) > 1e-6 for s0 in seen): seen.append(wa); out.append(wa)
    return out

def weyl_orbit(y0, refl, maxpts=2000):
    """W . y0 = the set of T-fixed points of the orbit (PREREG section 4.4): closure of {y0} under the
    root reflections."""
    pts = [y0]; frontier = [y0]
    while frontier and len(pts) < maxpts:
        new = []
        for x in frontier:
            for wa in refl:
                z = wa @ x
                if all(norm(z - p) > 1e-6 * max(norm(y0), 1e-12) for p in pts):
                    pts.append(z); new.append(z)
        frontier = new
    return pts

def g0_closure(g0):
    """A6: residual of [g0, g0] in span g0 and antisymmetry of the basis."""
    if not g0: return 0.0, 0.0
    _, worst, asym = closure_check(g0)
    return worst, asym

def recheck_witness(B, P, c, E, g0, idx):
    """A3: re-validate a capacity witness on RECHECK_N fresh orbit points (seed SEED + 10^6 + idx) with
    RECHECK_STARTS local minimisations per effect, using the witness effects themselves (not recomputed);
    returns the smallest effect value found."""
    rng = np.random.default_rng(SEED + RECHECK_SEED_OFFSET + idx)
    Yf = np.array([P.T @ (x - c) for x in orbit_samples(B, RECHECK_N, rng)])
    worst = np.inf
    for (a, lvec) in E:
        tick()
        vals = a + Yf @ lvec
        worst = min(worst, vals.min())
        for y in Yf[np.argsort(vals)[:RECHECK_STARTS]]:
            mx, x = local_max(lambda z: -(a + z @ lvec), g0, [y], rng)
            worst = min(worst, -mx)
    return float(worst)

def greedy_sets(Y, y0, tpts, g0, Nmax, rng, runs=12):
    """candidate distinguishable sets: start at y0 or a torus-fixed point, then repeatedly add the orbit
    point minimising the summed inner product with the points chosen so far (local minimisation from the
    lowest grid points). In quantum theory this picks orthogonal pure states."""
    out = []
    starts = [y0] + list(tpts)
    for t in range(runs):
        S = [starts[t % len(starts)]]
        for k in range(1, Nmax):
            tick()
            s = np.sum(S, axis=0)
            low = Y[np.argsort(Y @ s)[:4]]
            low = np.vstack([low, Y[rng.choice(len(Y), 2, replace=False)]])
            mx, x = local_max(lambda z: -(z @ s), g0, low, rng)
            S.append(x)
        out.append(S)
    return out

def cap_lower_bound(Y, tpts, g0, Nmax, rng, trials=100, y0=None):
    """largest N <= Nmax with an LP witness (positivity on the grid plus cutting planes, accepted when
    every effect's orbit minimum found by local minimisation is >= -NEG_TOL). Candidates: subsets of
    torus-fixed points, prefixes of greedy sets, then random grid sets."""
    best = 1; wit = None; best_E = None; wit_E = None
    greedy = greedy_sets(Y, Y[0] if y0 is None else y0, tpts, g0, Nmax, rng) if Nmax >= 2 else []
    for N in range(2, Nmax + 1):
        found = False
        cands = list(itertools.combinations(range(len(tpts)), N))[:2000]
        cand_sets = [[tpts[i] for i in c] for c in cands] + [S[:N] for S in greedy]
        for _ in range(trials):
            cand_sets.append([Y[i] for i in rng.choice(len(Y), N, replace=False)])
        for S in cand_sets:
            Yc = Y; ok = False
            for _ in range(CUT_ROUNDS):
                tick()
                E = effects_lp(Yc, S)
                if E is None: break
                worst, add = 0.0, []
                for (a, lvec) in E:
                    for mn, x in orbit_mins(a, lvec, g0, Yc, rng):
                        worst = min(worst, mn)
                        if mn < -1e-9: add.append(x)
                if worst >= -NEG_TOL: ok = True; break
                Yc = np.vstack([Yc] + add)
            if ok: found = True; wit = S; wit_E = E; break
        if found: best = N; best_E = wit_E
        else: break
    return best, wit, best_E

def effects_lp(Y, S):
    N = len(S); n, d = Y.shape; nv = N * (d + 1)
    A_eq, b_eq = [], []
    for i in range(N):
        for j in range(N):
            row = np.zeros(nv); row[i*(d+1)] = 1; row[i*(d+1)+1:(i+1)*(d+1)] = S[j]
            A_eq.append(row); b_eq.append(1.0 if i == j else 0.0)
    row = np.zeros(nv); row[0::d+1] = 1; A_eq.append(row); b_eq.append(1.0)
    for k in range(d):
        row = np.zeros(nv); row[1+k::d+1] = 1; A_eq.append(row); b_eq.append(0.0)
    A_ub = np.zeros((N * n, nv))
    for i in range(N):
        A_ub[i*n:(i+1)*n, i*(d+1)] = -1; A_ub[i*n:(i+1)*n, i*(d+1)+1:(i+1)*(d+1)] = -Y
    r = linprog(np.zeros(nv), A_ub=A_ub, b_ub=np.zeros(N*n), A_eq=np.array(A_eq), b_eq=np.array(b_eq),
                bounds=[(None, None)] * nv, method="highs")
    if r.status != 0: return None
    return [(r.x[i*(d+1)], r.x[i*(d+1)+1:(i+1)*(d+1)]) for i in range(N)]

def bitface_is_ball(Y, p, q, g0, rng, nstart=60):
    """The bit face of the perfectly distinguishable pure states p, q, taken as the minimal exposed face
    containing m = (p+q)/2. Its normal l is the average of max(5, d) elements of the normal cone at m,
    each an LP vertex (random objective, |l|_inf <= 1, l.(y - m) <= 0 on the grid) made valid on the
    whole orbit by cutting planes (orbit points with l.(x - m) > 1e-9 are added until none is found).
    Pure states of the face: local maxima of l over the orbit from the nstart highest grid points,
    kept when within 1e-7 (relative) of l.m. The face is the 3-ball iff they span an affine 3-space and
    lie on an ellipsoid (least-squares quadric fit, rms residual < 1e-3, positive definite); affine dimension counts singular values above 1e-2 of the largest."""
    n, d = Y.shape
    mid = (p + q) / 2
    rad = max(norm(Y, axis=1).max(), 1e-12)
    ls = []; trivial = 0
    for _ in range(max(5, d)):
        cobj = -rng.normal(size=d)
        Yc = Y; lval = None
        for _r in range(CUT_ROUNDS):
            tick()
            r = linprog(cobj, A_ub=Yc - mid, b_ub=np.zeros(len(Yc)), bounds=[(-1, 1)] * d, method="highs")
            if r.status != 0: break
            lv = r.x
            if norm(lv) < 1e-9: trivial += 1; break
            top = Yc[np.argsort(Yc @ lv)[-6:]]
            add = []
            for y in top:
                val, x = local_max(lambda z: z @ lv, g0, [y], rng)
                if val - lv @ mid > 1e-7 * rad * norm(lv): add.append(x)
            if not add: lval = lv; break
            Yc = np.vstack([Yc] + add)
        if lval is not None: ls.append(lval)
    if not ls and trivial:
        F = Y                     # the normal cone at m is {0}: the face is K itself
    elif not ls:
        return None, None, None, mid
    else:
        F = None
    if F is None:
        F = bitface_points(Y, ls, mid, p, q, g0, rng, nstart, rad)
    adim, isball = face_is_ball(F)
    return adim, isball, F, mid

def in_relint(F, m):
    """largest t with m = sum lambda_i F_i, sum lambda_i = 1, lambda_i >= t (LP), posed in coordinates
    of the affine hull of F (the directions with singular value above 1e-2 of the largest, as in
    face_is_ball), because the numerically found face points lie off that hull by ~1e-4 and an exact
    equality LP in the ambient space is then infeasible. Returns -inf if m lies farther than 1e-3 times
    the face radius from that hull. t > 0 means m lies in the relative interior of conv(F)."""
    k = len(F)
    ctr = F.mean(0); Fc = F - ctr
    u, sv, vt = svd(Fc, full_matrices=False)
    adim = int((sv > 1e-2 * sv[0]).sum())
    V = vt[:adim]; rF = max(norm(Fc, axis=1).max(), 1e-12)
    r = m - ctr; mr = V @ r
    if norm(r - V.T @ mr) > 1e-3 * rF: return -np.inf
    X = Fc @ V.T
    cobj = np.r_[np.zeros(k), -1.0]
    A_eq = np.c_[np.vstack([X.T, np.ones((1, k))]), np.zeros(adim + 1)]
    b_eq = np.r_[mr, 1.0]
    A_ub = np.c_[-np.eye(k), np.ones(k)]
    r = linprog(cobj, A_ub=A_ub, b_ub=np.zeros(k), A_eq=A_eq, b_eq=b_eq,
                bounds=[(0, None)] * k + [(None, None)], method="highs")
    return r.x[-1] if r.status == 0 else -np.inf

def bit_face_status(Y, p, q, g0, rng):
    """A2: status of the bit face of (p, q) = the minimal face of m = (p+q)/2.
    'ball' if the minimal exposed face E is a 3-ball (then the minimal face equals E: every chord
    midpoint of a ball is in its interior); 'not ball' if E is not a 3-ball and m is in the relative
    interior of conv(E's pure states) (then the minimal face is E); 'undecided' otherwise."""
    adim, isball, F, mid = bitface_is_ball(Y, p, q, g0, rng)
    if isball is True: return "ball", adim
    if F is None or len(F) < 2: return "undecided", adim
    t = in_relint(F, mid)
    if isball is False and t > 1e-6: return "not ball", adim
    return "undecided", adim

def distinguishable_pair(Y, p, q, g0, rng):
    """the pair {p, q} has a 2-outcome witness verified like the capacity witness."""
    Yc = Y
    for _ in range(CUT_ROUNDS):
        tick()
        E = effects_lp(Yc, [p, q])
        if E is None: return False
        worst, add = 0.0, []
        for (a, lvec) in E:
            for mn, x in orbit_mins(a, lvec, g0, Yc, rng):
                worst = min(worst, mn)
                if mn < -1e-9: add.append(x)
        if worst >= -NEG_TOL: return True
        Yc = np.vstack([Yc] + add)
    return False

def bitface_points(Y, ls, mid, p, q, g0, rng, nstart, rad):
    l = np.mean(ls, axis=0)
    starts = Y[np.argsort(Y @ l)[-nstart:]]
    pts = [p, q]; top = l @ mid
    for y in starts:
        tick()
        val, x = local_max(lambda z: z @ l, g0, [y], rng)
        pts.append(x)
    return np.array([x for x in pts if x @ l > top - 1e-6 * rad * norm(l)])

def face_is_ball(F):
    Fc = F - F.mean(0)
    u, sv, vt = svd(Fc, full_matrices=False)
    adim = int((sv > 1e-2 * sv[0]).sum()) if len(F) > 1 else 0
    if adim != 3 or len(F) < 12: return adim, False if adim != 3 else None
    X = Fc @ vt[:3].T
    M = np.c_[X[:, 0]**2, X[:, 1]**2, X[:, 2]**2, 2*X[:, 0]*X[:, 1], 2*X[:, 0]*X[:, 2], 2*X[:, 1]*X[:, 2], X]
    coef, *_ = np.linalg.lstsq(M, np.ones(len(X)), rcond=None)
    resid = norm(M @ coef - 1) / math.sqrt(len(X))
    A = np.array([[coef[0], coef[3], coef[4]], [coef[3], coef[1], coef[5]], [coef[4], coef[5], coef[2]]])
    return adim, bool(resid < 1e-3 and np.linalg.eigvalsh(A).min() > 0)

def analyse(B, idx, do_full=True, recheck=True):
    rng = np.random.default_rng(SEED + idx)
    P, c = ambient(B, rng); d = P.shape[1]
    y0 = P.T @ (B.v - c)
    G, g0 = g0_algebra(B, P, c, rng)
    res = {"body": B.name, "group": B.group, "family": B.family, "affine_dim": d,
           "dim_G": len(G), "dim_G0": len(g0)}
    # A6: per-body closure of the computed g0
    clo, asym = g0_closure(g0)
    res.update(g0_closure_residual=clo, g0_antisymmetry_residual=asym)
    if clo > G0_CLOSURE_TOL or asym > G0_CLOSURE_TOL:
        res["outcome"] = "OPEN (g0 closure check fails)"; return res
    r0, rh, h0, carth = sfp_rank_test(g0, y0, rng)
    res.update(rank_G0=r0, rank_stab=rh)
    if r0 != rh:
        res.update(SFP="fail", outcome="MISS (SFP fails under G0)"); return res
    res["SFP"] = "pass"
    Y = np.array([P.T @ (x - c) for x in orbit_samples(B, N_GRID, rng)])
    alpha, NUB = cap_upper_bound(Y, y0, g0, rng)
    res.update(cap_UB=NUB, alpha=alpha)
    if NUB is None:
        res["outcome"] = "OPEN (no capacity upper bound)"; return res
    if d > NUB * NUB - 1:
        res["outcome"] = "MISS (cost: d > N_UB^2 - 1)"; return res
    if not do_full:
        res["outcome"] = "needs full test"; return res
    # A4: T-fixed points = W . y0 (root reflections in G0); cross-check with the optimisation search
    refl = root_reflections(g0, carth, rng)
    tW = weyl_orbit(y0, refl)
    tO = tfixed_points(g0, carth, y0, rng)
    match = (len(tO) == len(tW)) and all(min(norm(x - z) for z in tW) < 1e-5 * max(norm(y0), 1e-12) for x in tO)
    res.update(n_torus_fixed_weyl=len(tW), n_torus_fixed_search=len(tO), torus_fixed_match=bool(match))
    if not match:
        res["outcome"] = "OPEN (torus-fixed points: search does not match the Weyl orbit)"; return res
    tpts = tW
    ok, info = hsfp_test(Y, g0, carth, y0, tpts, rng)
    res["hSFP"] = "pass at depth 1 (no failure found)" if ok else "fail (re-confirmed)"; res["hSFP_info"] = info
    if not ok:
        res["outcome"] = "MISS (hSFP fails)"; return res
    NLB, wit, wit_E = cap_lower_bound(Y, tpts, g0, NUB, rng, y0=y0)
    res["cap_LB"] = NLB
    orbdim = len(g0) - len(h0)
    jordan = jordan_type(d, NUB, len(g0), orbdim)
    res["jordan_type"] = jordan
    strict = d < NLB * NLB - 1
    tie = (NLB == NUB) and d == NLB * NLB - 1
    dim_only = "HIT" if strict else ("TIE" if tie else ("OPEN" if d <= NUB * NUB - 1 else "MISS"))
    res["outcome_dimension_only"] = dim_only
    target_sig = (jordan == "complex QM" and NLB == NUB)
    if dim_only not in ("HIT", "TIE") and not target_sig:
        res["outcome"] = dim_only; return res
    # A3: witness recheck on fresh orbit points before any HIT, TIE or TARGET
    if recheck and wit_E is not None:
        mn = recheck_witness(B, P, c, wit_E, g0, idx)
        res["witness_recheck_min"] = mn
        if mn is None or mn < -NEG_TOL:
            res["outcome"] = "OPEN (capacity witness fails the fresh-sample recheck)"; return res
    # A5: TARGET only for the known CP^(N-1) orbits
    if target_sig:
        if B.known_cp:
            res["outcome"] = "TARGET (complex QM itself)"; return res
        res["outcome"] = "OPEN (TARGET-signature, check by hand)"; return res
    # A2: bit faces of every witness pair and every distinguishable pair of T-fixed points
    pairs = list(itertools.combinations(range(len(wit)), 2))
    statuses = []
    for i, j in pairs:
        st, adim = bit_face_status(Y, wit[i], wit[j], g0, rng); statuses.append(("witness", i, j, st, adim))
    for i, j in itertools.combinations(range(len(tpts)), 2):
        if distinguishable_pair(Y, tpts[i], tpts[j], g0, rng):
            st, adim = bit_face_status(Y, tpts[i], tpts[j], g0, rng); statuses.append(("T-fixed", i, j, st, adim))
    res["bit_faces"] = [list(t) for t in statuses]
    if any(t[3] == "not ball" for t in statuses):
        res["outcome"] = "MISS (P6 bit-face clause fails; dimension-only %s)" % dim_only
    elif any(t[3] == "undecided" for t in statuses) or not statuses:
        res["outcome"] = "OPEN (P6 bit-face clause undecided; dimension-only %s)" % dim_only
    else:
        res["outcome"] = dim_only + " (all bit faces are 3-balls; conditional on faces of exposure depth >= 2, untested)"
    return res

def jordan_type(d, N, dimG0, orbdim):
    """Jordan state spaces in range, keyed by (affine dim, capacity, dim G0, dim of the pure-state
    manifold). The pure-state dimension separates complex QM_3 (CP^2, dim 4) from the SU(3) flag
    orbitope (dim 6), which share (8, 3, 8)."""
    table = {}
    for n in range(2, 6):
        table[(n*n - 1, n, n*n - 1, 2*(n - 1))] = "complex QM"
        table[(n*(n+1)//2 - 1, n, n*(n-1)//2, n - 1)] = "real QM"
    for n in range(3, 16): table.setdefault((n, 2, n*(n-1)//2, n - 1), "ball B%d (spin factor)" % n)
    table[(14, 3, 21, 8)] = "quaternionic QM d=3"
    return table.get((d, N, dimG0, orbdim), "no")

# ---------------------------------------------------------------- enumeration
# Reduction used (PREREG.md section 3): an SFP body has v fixed by a maximal torus of the acting group,
# so v lies in the zero-weight space Z of V. Rescaling one irreducible summand (by any non-zero real,
# sign included) is a G-equivariant invertible linear map, so it is an affine equivalence of orbitopes:
# amplitudes and signs between distinct summands do not matter, and a summand repeated m times can be
# reduced to min(m, dim Z_i) copies. Only the direction of v inside a summand with dim Z_i >= 2 is a
# real parameter; it is covered by a full-circle grid of step ANG_STEP_DEG.

def so3k_rep(js):
    """SO(3)^k acting on spin j1 (x) ... (x) spin jk (spin 0 = trivial 1-dim); 3k generators."""
    reps = [(so3_spin(j) if j > 0 else ([np.zeros((1, 1))] * 3, np.ones(1))) for j in js]
    dims = [len(z) for g, z in reps]
    gens = []
    for t, (g, z) in enumerate(reps):
        for a in g:
            M = np.ones((1, 1))
            for u in range(len(reps)):
                M = np.kron(M, a if u == t else np.eye(dims[u]))
            gens.append(M)
    v = np.ones(1)
    for g, z in reps: v = np.kron(v, z)
    return gens, v

def so3k_bodies(k, dmin, dmax, label):
    """SO(3)^k: sums of distinct irreducible types (j1..jk) (each with a 1-dim zero-weight space, so a
    repeated type reduces to one copy), every factor acting non-trivially, affine dimension dmin..dmax."""
    types = [js for js in itertools.product(range(0, 8), repeat=k)
             if any(js) and int(np.prod([2*j + 1 for j in js])) <= dmax]
    out = []
    for m in range(1, 5):
        for S in itertools.combinations(types, m):
            dim = sum(int(np.prod([2*j + 1 for j in js])) for js in S)
            if not (dmin <= dim <= dmax): continue
            if not all(any(js[t] > 0 for js in S) for t in range(k)): continue
            reps = [so3k_rep(js) for js in S]
            gens = [block([r[0][t] for r in reps]) for t in range(3 * k)]
            out.append(("%s types %s" % (label, S), gens, np.concatenate([r[1] for r in reps]), dim,
                        label))
    return out

def u2_bodies():
    """U(2) acts with a zero weight only through SO(3) (PREREG of 2026-11-26, section 3)."""
    return so3k_bodies(1, 9, 15, "U(2)->SO(3)")

def sp1sq_bodies():
    """Sp(1)^2 acts with a zero weight only through SO(3)^2; Sp(1)^3 through SO(3)^3."""
    return so3k_bodies(2, 9, 15, "Sp(1)^2->SO(3)^2") + so3k_bodies(3, 9, 15, "Sp(1)^3->SO(3)^3")

def rank2_bodies(rng):
    """SU(3): 8. Sp(2) via SO(5): 5, 10, 14, 5+10. G2: 7, 14. (Complete list of sums of real
    irreducibles with a zero weight and total dimension <= 15: PREREG.md section 3.)"""
    out = []
    g8, cv = su3_adjoint()
    for i, v in enumerate(angle_vectors(np.array(cv).T)):
        out.append(("SU(3) 8 angle %d deg" % (i * ANG_STEP_DEG), g8, v, 8, "SU(3)"))
    for a, v in singular_vectors(g8, np.array(cv).T):
        out.append(("SU(3) 8 singular %.4f deg" % a, g8, v, 8, "SU(3)"))
    R = so5_reps()
    V5, _ = tfixed_space(R["5"], rng)
    assert V5.shape[1] == 1
    out.append(("Sp(2) 5", R["5"], V5[:, 0], 5, "Sp(2)"))
    for key in ("10", "14"):
        Vk, _ = tfixed_space(R[key], rng); assert Vk.shape[1] == 2
        for i, v in enumerate(angle_vectors(Vk)):
            out.append(("Sp(2) %s angle %d deg" % (key, i * ANG_STEP_DEG), R[key], v, int(key), "Sp(2)"))
        for a, v in singular_vectors(R[key], Vk):
            out.append(("Sp(2) %s singular %.4f deg" % (key, a), R[key], v, int(key), "Sp(2)"))
    g510 = [block([a, b]) for a, b in zip(R["5"], R["10"])]
    V10, _ = tfixed_space(R["10"], rng)
    for i, w in enumerate(angle_vectors(V10)):
        out.append(("Sp(2) 5+10 angle %d deg" % (i * ANG_STEP_DEG), g510, np.r_[V5[:, 0], w], 15, "Sp(2)"))
    for a, w in singular_vectors(g510, V10, offset=V5[:, 0]):
        out.append(("Sp(2) 5+10 singular %.4f deg" % a, g510, np.r_[V5[:, 0], w], 15, "Sp(2)"))
    Gr = g2_reps()
    V7, _ = tfixed_space(Gr["7"], rng); assert V7.shape[1] == 1
    out.append(("G2 7", Gr["7"], V7[:, 0], 7, "G2"))
    V14, _ = tfixed_space(Gr["14"], rng); assert V14.shape[1] == 2
    for i, v in enumerate(angle_vectors(V14)):
        out.append(("G2 14 angle %d deg" % (i * ANG_STEP_DEG), Gr["14"], v, 14, "G2"))
    for a, v in singular_vectors(Gr["14"], V14):
        out.append(("G2 14 singular %.4f deg" % a, Gr["14"], v, 14, "G2"))
    return out

def product_body(parts):
    gens = []; vs = []; dims = [len(p[2]) for p in parts]; off = 0; D = sum(dims)
    for (name, g, v, *_r) in parts:
        k = len(v)
        for X in g:
            M = np.zeros((D, D)); M[off:off+k, off:off+k] = X; gens.append(M)
        vs.append(v); off += k
    return gens, np.concatenate(vs)

PROD_ANG_STEP_DEG = 15   # angle grid of a rank-2 family factor inside a product with SO(3)^k bodies

def product_bodies(rng):
    """G x SO(3)^k (G = SU(3), Sp(2), G2; k = 1, 2, 3; the images of G x Sp(1)^k): external sums
    (orbitope = product of bodies), affine dimension <= 15, plus the one irreducible tensor type in
    range, Sp(2) x SO(3) on 5 (x) 3 (dimension 15)."""
    out = []
    singles = [r for r in rank2_bodies(rng)
               if ("angle" not in r[0]) or (int(r[0].split("angle ")[1].split()[0]) % PROD_ANG_STEP_DEG == 0)]
    # (Weyl-singular members are kept in products too)
    for (n1, g1, v1, d1, grp1) in singles:
        for k in (1, 2, 3):
            if d1 + 3 * k > 15: continue
            for (n2, g2, v2, d2, grp2) in so3k_bodies(k, 3 * k, 15 - d1, "SO(3)^%d" % k):
                gens, v = product_body([(n1, g1, v1), (n2, g2, v2)])
                out.append(("%s x %s" % (n1, n2), gens, v, d1 + d2, "%s x Sp(1)^%d" % (grp1, k)))
    R = so5_reps(); g3, z3 = so3_spin(1)
    V5, _ = tfixed_space(R["5"], rng)
    gens = [np.kron(a, np.eye(3)) for a in R["5"]] + [np.kron(np.eye(5), b) for b in g3]
    out.append(("Sp(2) x Sp(1) on 5 (x) 3", gens, np.kron(V5[:, 0], z3), 15, "Sp(2) x Sp(1)"))
    return out

def enumerate_bodies(rng):
    rows = rank2_bodies(rng) + u2_bodies() + sp1sq_bodies() + product_bodies(rng)
    return [Body(n, g, v, grp, "d=%d" % d, known_cp=n.startswith("SU(3) 8 singular"))
            for (n, g, v, d, grp) in rows]

def zero_weight_table(rng):
    rows = []
    for j in range(1, 8):
        g, _ = so3_spin(j); V, r = tfixed_space(g, rng); rows.append(("SO(3) spin %d" % j, 2*j+1, V.shape[1]))
    g8, _ = su3_adjoint(); V, r = tfixed_space(g8, rng); rows.append(("SU(3) adjoint 8", 8, V.shape[1]))
    l = gellmann(); g3 = [1j * a for a in l]
    g6 = [np.block([[x.real, -x.imag], [x.imag, x.real]]) for x in g3]
    V, r = tfixed_space(g6, rng); rows.append(("SU(3) on C^3 (real 6)", 6, V.shape[1]))
    for k, g in so5_reps().items():
        V, r = tfixed_space(g, rng); rows.append(("SO(5) %s" % k, int(k), V.shape[1]))
    for k, g in g2_reps().items():
        V, r = tfixed_space(g, rng); rows.append(("G2 %s" % k, int(k), V.shape[1]))
    return rows

def closure_check(gens):
    """the span of the generators is closed under commutators and they are antisymmetric (no orbit,
    no zero weights, no capacity: construction check only)."""
    B = orth_basis(gens); M = np.array([b.ravel() for b in B]).T
    worst = 0.0
    for a in B:
        for b in B:
            cvec = comm(a, b).ravel(); coef, *_ = np.linalg.lstsq(M, cvec, rcond=None)
            worst = max(worst, norm(M @ coef - cvec))
    asym = max(norm(g + g.T) for g in gens)
    return len(B), worst, asym

def selftest():
    import scipy
    print("# numpy %s scipy %s python %s" % (np.__version__, scipy.__version__, sys.version.split()[0]))
    print("# construction checks (no orbit, no outcome quantity is computed)")
    g8, _ = su3_adjoint(); R = so5_reps(); Gr = g2_reps()
    for name, g in [("su(3) adjoint", g8), ("so(5) 5", R["5"]), ("so(5) 10", R["10"]), ("so(5) 14", R["14"]),
                    ("g2 7", Gr["7"]), ("g2 14", Gr["14"])] + [("so(3) spin %d" % j, so3_spin(j)[0]) for j in range(1, 8)]:
        dimg, worst, asym = closure_check(g)
        print("  %-14s algebra dim %2d  closure residual %.1e  antisymmetry residual %.1e" % (name, dimg, worst, asym))
    print("# selftest: SO(3) controls with published outcomes")
    rng = np.random.default_rng(SEED)
    g1, z1 = so3_spin(1); g2, z2 = so3_spin(2); g3, z3 = so3_spin(3)
    controls = [Body("B3 (spin 1)", g1, z1, "SO(3)", known_cp=True), Body("Z3 (spin 3)", g3, z3, "SO(3)"),
                Body("C1 (spin 1+2)", [block([a, b]) for a, b in zip(g1, g2)], np.r_[z1, z2], "SO(3)"),
                Body("Z2 (real QM d=3)", g2, z2, "SO(3)")]
    gb, vb = product_body([("a", g1, z1), ("b", g1, z1)])
    controls.append(Body("B3 x B3", gb, vb, "SO(3)^2"))
    for i, B in enumerate(controls):
        r = analyse(B, 1000 + i, do_full=True)
        print(json.dumps(r, default=float))
    print("# bit-face check on published cases: B3 (bit face = the whole 3-ball), Z2 = real QM d=3 (bit faces are discs)")
    for i, B in enumerate(controls[:1] + controls[3:4]):
        rng = np.random.default_rng(SEED + 2000 + i)
        P, c = ambient(B, rng); y0 = P.T @ (B.v - c)
        G, g0 = g0_algebra(B, P, c, rng)
        r0, rh, h0, carth = sfp_rank_test(g0, y0, rng)
        Y = np.array([P.T @ (x - c) for x in orbit_samples(B, N_GRID, rng)])
        tpts = tfixed_points(g0, carth, y0, rng)
        NLB, wit, wit_E = cap_lower_bound(Y, tpts, g0, 3, rng, y0=y0)
        st, adim = bit_face_status(Y, wit[0], wit[1], g0, rng)
        print("  %-18s cap_LB %d  bit-face affine dim %s  status %s" % (B.name, NLB, adim, st))
    print("expected (published): B3 = complex QM N=2 (TARGET); Z3 MISS cost (N_UB=2); C1 hSFP fail or cost; Z2 hSFP fail; B3xB3 MISS cost")

def _analyse_job(args):
    i, B = args
    _DEADLINE[0] = time.time() + BODY_BUDGET_S
    t0 = time.time()
    try:
        r = analyse(B, i)
    except OutOfBudget:
        r = {"body": B.name, "group": B.group, "family": B.family, "outcome": "OPEN (time budget)"}
    r["index"] = i; r["seconds"] = round(time.time() - t0, 1)
    return r

def check_lock():
    """the scored run refuses to start unless PREREG.md and this script match PREREG.sha256."""
    import hashlib, os
    here = os.path.dirname(os.path.abspath(__file__))
    lock = os.path.join(here, "PREREG.sha256")
    if not os.path.exists(lock): sys.exit("PREREG.sha256 missing: the lock must be committed and pushed first")
    for line in open(lock):
        if not line.strip(): continue
        h, path = line.split(None, 1); path = path.strip()
        fp = os.path.join(here, os.path.basename(path))
        if hashlib.sha256(open(fp, "rb").read()).hexdigest() != h:
            sys.exit("hash mismatch for %s: the locked files were changed" % path)

def body_names():
    rng = np.random.default_rng(SEED)
    return enumerate_bodies(rng)

def list_bodies():
    """enumeration only (index, name, group, dimension); computes no orbit and no outcome quantity.
    The output is committed as list.out; --run regenerates it and aborts on any difference (A7)."""
    bodies = body_names()
    from collections import Counter
    cnt = Counter((B.group, B.family) for B in bodies)
    for k in sorted(cnt): print("# %-18s %-6s %4d" % (k[0], k[1], cnt[k]))
    print("# total %d" % len(bodies))
    for i, B in enumerate(bodies):
        print("%d\t%s\t%s\t%s" % (i, B.name, B.group, B.family))

def check_versions():
    import scipy
    have = {"numpy": np.__version__, "scipy": scipy.__version__, "python": sys.version.split()[0]}
    if have != PINNED: sys.exit("version mismatch: have %s, pinned %s" % (have, PINNED))

def check_list(bodies):
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    want = [l.rstrip("\n") for l in open(os.path.join(here, "list.out")) if not l.startswith("#")]
    have = ["%d\t%s\t%s\t%s" % (i, B.name, B.group, B.family) for i, B in enumerate(bodies)]
    if want != have: sys.exit("enumeration differs from the committed list.out (names or order)")

def run(workers):
    check_lock(); check_versions()
    print("# search_qmsel3.py --run  (prereg PREREG.md)")
    bodies = body_names()               # same fresh generator as --list
    check_list(bodies)
    print("## zero-weight multiplicities")
    for row in zero_weight_table(np.random.default_rng(SEED + 7)): print("  %-24s dim %2d  zero-weight dim %d" % row)
    print("## %d bodies enumerated, names and order match list.out" % len(bodies), flush=True)
    from multiprocessing import Pool
    with Pool(workers) as pool:
        out = pool.map(_analyse_job, list(enumerate(bodies)), chunksize=1)
    for r in out: print(json.dumps(r, default=float))
    hits = [r for r in out if r["outcome"].startswith(("HIT", "TIE"))]
    opens = [r for r in out if "OPEN" in r["outcome"]]
    print("## summary: %d bodies, %d HIT/TIE, %d OPEN, %d TARGET" % (len(out), len(hits), len(opens),
          sum(r["outcome"].startswith("TARGET") for r in out)))
    dim_hits = [r for r in out if r.get("outcome_dimension_only") in ("HIT", "TIE")]
    print("## secondary (dimension only, P6 bit-face clause not applied): %d HIT/TIE" % len(dim_hits))
    print("RESULT:", "HIT" if hits else ("INCONCLUSIVE" if opens else "MISS"))

if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif "--list" in sys.argv: list_bodies()
    elif "--run" in sys.argv:
        w = [int(x.split("=")[1]) for x in sys.argv if x.startswith("--workers=")]
        run(w[0] if w else 4)
    else: print(__doc__)
