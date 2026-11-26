"""Round 10b checks.
(1) Baer: every polarity of a finite projective plane PG(2,q), q = 2, 3, 4, has an absolute point
    (p lies on its own polar line), so no finite plane carries an orthocomplementation.
(2) Chevalley-Warning: every diagonal quadratic form in 3 variables over GF(q), q = 3, 5, 7, has a
    non-zero zero (isotropic vector).
(3) Two-qubit stabilizer theory: 'superposition' holds in a bit face but the lattice of stabilizer
    codes breaks the covering law (the code spanned by two stabilizer states can be the whole space).
(4) No-small-subgroups reading: minimum displacement of non-identity elements, finite vs SO(3)."""
import itertools, numpy as np

# ---------- GF(q) arithmetic for q = 2, 3, 4 ----------
def field(q):
    if q in (2, 3):
        add = lambda a, b: (a + b) % q; mul = lambda a, b: (a * b) % q
        autos = [lambda a: a]
    else:  # GF(4) = {0,1,w,w^2} coded 0,1,2,3 ; w^2 = w + 1
        exp = [1, 2, 3]; log = {1: 0, 2: 1, 3: 2}
        add = lambda a, b: a ^ b
        mul = lambda a, b: 0 if a == 0 or b == 0 else exp[(log[a] + log[b]) % 3]
        autos = [lambda a: a, lambda a: mul(a, a)]
    return add, mul, autos

def baer(q):
    add, mul, autos = field(q)
    vecs = [v for v in itertools.product(range(q), repeat=3) if any(v)]
    def norm(v):
        k = next(x for x in v if x)
        inv = next(c for c in range(1, q) if mul(c, k) == 1)
        return tuple(mul(inv, x) for x in v)
    pts = sorted(set(norm(v) for v in vecs))
    dot = lambda a, b: add(add(mul(a[0], b[0]), mul(a[1], b[1])), mul(a[2], b[2]))
    on = {(p, l): dot(p, l) == 0 for p in pts for l in pts}  # lines coded by coordinate vectors
    n_pol = n_pol_no_abs = 0
    for A in itertools.product(range(q), repeat=9):
        M = [A[0:3], A[3:6], A[6:9]]
        for s in autos:
            img = {}
            ok = True
            for p in pts:
                sp = tuple(s(x) for x in p)
                l = tuple(add(add(mul(M[i][0], sp[0]), mul(M[i][1], sp[1])), mul(M[i][2], sp[2])) for i in range(3))
                if not any(l): ok = False; break
                img[p] = norm(l)
            if not ok or len(set(img.values())) != len(pts): continue
            # polarity: p on polar(r) <=> r on polar(p)  (symmetric incidence)
            if all(on[(p, img[r])] == on[(r, img[p])] for p in pts for r in pts):
                n_pol += 1
                if not any(on[(p, img[p])] for p in pts): n_pol_no_abs += 1
    return len(pts), n_pol, n_pol_no_abs

for q in (2, 3, 4):
    npts, npol, nfree = baer(q)
    print(f"PG(2,{q}): {npts} points; polarity matrices found {npol}; without absolute point {nfree}")

for q in (3, 5, 7):
    iso = all(any((a*x*x + b*y*y + c*z*z) % q == 0 for x, y, z in itertools.product(range(q), repeat=3) if (x, y, z) != (0, 0, 0))
              for a, b, c in itertools.product(range(1, q), repeat=3))
    print(f"GF({q}): every non-degenerate diagonal ternary form isotropic: {iso}")

# ---------- stabilizer covering law ----------
I2 = np.eye(2); X = np.array([[0, 1], [1, 0]]); Y = np.array([[0, -1j], [1j, 0]]); Z = np.diag([1, -1])
P1 = [I2, X, Y, Z]
paulis = [np.kron(a, b) for a in P1 for b in P1][1:]
def stab_states():
    s1 = [np.array(v, complex) / np.linalg.norm(v) for v in ([1, 0], [0, 1], [1, 1], [1, -1], [1, 1j], [1, -1j])]
    out = [np.kron(a, b) for a in s1 for b in s1]
    for P in paulis:  # add entangled ones: +1 eigenvectors of commuting Pauli pairs
        for Q in paulis:
            if np.allclose(P @ Q, Q @ P) and not np.allclose(P, Q):
                for sp, sq in itertools.product((1, -1), repeat=2):
                    proj = (np.eye(4) + sp * P) @ (np.eye(4) + sq * Q) / 4
                    if abs(np.trace(proj) - 1) < 1e-9:
                        w, v = np.linalg.eigh(proj); out.append(v[:, -1])
    uniq = []
    for v in out:
        if not any(abs(abs(np.vdot(u, v)) - 1) < 1e-9 for u in uniq): uniq.append(v)
    return uniq
S = stab_states()
print("two-qubit stabilizer states:", len(S))
in_span = [v for v in S if abs(v[1]) < 1e-9 and abs(v[2]) < 1e-9]
print("stabilizer states in the bit face span{|00>,|11>}:", len(in_span), "(a third state exists: superposition)")
bad = 0; tot = 0
for a, b in itertools.combinations(S, 2):
    if abs(np.vdot(a, b)) > 1 - 1e-9: continue
    tot += 1
    fixed = any(all(np.allclose(sg * P @ v, v) for v in (a, b)) for P in paulis for sg in (1, -1))
    if not fixed: bad += 1
print(f"pairs whose 2-dim span is not a stabilizer code (join jumps to the whole space): {bad} of {tot}")

# ---------- no small subgroups / minimum displacement ----------
oct_rot = []
for perm in itertools.permutations(range(3)):
    for signs in itertools.product((1, -1), repeat=3):
        M = np.zeros((3, 3)); [M.__setitem__((i, perm[i]), signs[i]) for i in range(3)]
        if np.isclose(np.linalg.det(M), 1): oct_rot.append(M)
def disp(M):  # worst-case move of a unit vector = operator norm of M - I
    return np.linalg.norm(M - np.eye(3), 2)
print("octahedral group: order", len(oct_rot), "; min over non-identity of ||g - 1||:",
      round(min(disp(M) for M in oct_rot if not np.allclose(M, np.eye(3))), 4))
for th in (1e-1, 1e-3, 1e-6):
    R = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]])
    print(f"SO(3) rotation by {th}: ||g - 1|| = {disp(R):.2e}")
