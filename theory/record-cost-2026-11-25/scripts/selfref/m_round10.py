"""Round 10 checks: composition with finite reversible groups (stabilizer qubits),
octahedron capacity, and the counting step behind 'purification => not a polytope'."""
import itertools, numpy as np
from scipy.optimize import linprog
np.set_printoptions(precision=4, suppress=True)

def canon(U):
    f = U.flatten(); k = np.argmax(np.abs(f) > 1e-9)
    V = U * (abs(f[k]) / f[k])
    return tuple(np.round(V.flatten(), 6).view(float).round(6))

def closure(gens):
    d = gens[0].shape[0]; I = np.eye(d, dtype=complex)
    seen = {canon(I): I}; frontier = [I]
    while frontier:
        new = []
        for U in frontier:
            for g in gens:
                W = g @ U; c = canon(W)
                if c not in seen: seen[c] = W; new.append(W)
        frontier = new
    return list(seen.values())

H = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2); S = np.diag([1, 1j]); I2 = np.eye(2)
C1 = closure([H, S])
print("1-qubit Clifford group mod phase: order", len(C1))
def kets_orbit(group, psi):
    out = {}
    for U in group:
        v = U @ psi; k = np.argmax(np.abs(v) > 1e-9); v = v * abs(v[k]) / v[k]
        out[tuple(np.round(v, 6))] = v
    return list(out.values())
stab1 = kets_orbit(C1, np.array([1, 0], complex))
print("1-qubit stabilizer pure states:", len(stab1), "(transitive orbit of |0>)")
def fixes(U, v): return abs(abs(np.vdot(v, U @ v)) - 1) < 1e-9
der = [U for U in C1 if not any(fixes(U, v) for v in stab1)]
print("Clifford elements fixing no stabilizer state (derangements, Jordan):", len(der), "of", len(C1))

CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], complex)
C2 = closure([np.kron(H, I2), np.kron(I2, H), np.kron(S, I2), np.kron(I2, S), CNOT])
print("2-qubit Clifford group mod phase: order", len(C2), "(known 11520)")
stab2 = kets_orbit(C2, np.array([1, 0, 0, 0], complex))
print("2-qubit stabilizer pure states:", len(stab2), "(known 60; single orbit => transitive)")
def marg_purity(v):
    M = v.reshape(2, 2); r = M @ M.conj().T; return np.real(np.trace(r @ r))
ent = sum(1 for v in stab2 if marg_purity(v) < 0.99)
print("entangled stabilizer pure states:", ent)
plus0 = np.kron(np.array([1, 1]) / np.sqrt(2), np.array([1, 0])).astype(complex)
print("CNOT|+0> marginal purity:", round(marg_purity(CNOT @ plus0), 6), "(0.5 = maximally entangled)")
P = [I2, np.array([[0,1],[1,0]]), np.array([[0,-1j],[1j,0]]), np.diag([1,-1])]
rank_local = np.linalg.matrix_rank(np.array([np.kron(a, b).flatten() for a in P for b in P]))
print("local tomography: rank of local Pauli products =", rank_local, "of 16")
der2 = sum(1 for U in C2 if not any(fixes(U, v) for v in stab2))
print("2-qubit Clifford elements fixing no stabilizer state:", der2)

# Octahedron with all non-negative affine effects: capacity (max perfectly distinguishable vertices)
V = [np.array(s) * e for e in np.eye(3) for s in (1, -1)]
def distinguishable(vs):
    n = len(vs); nv = 4 * n  # effect i = (a_i, b_i); constraints e_i(v)>=0 all 6 vertices, e_i(vs_j)=delta, sum=unit
    A_ub, b_ub, A_eq, b_eq = [], [], [], []
    for i in range(n):
        for v in V:
            row = np.zeros(nv); row[4*i] = -1; row[4*i+1:4*i+4] = -v; A_ub.append(row); b_ub.append(0)
        for j, w in enumerate(vs):
            row = np.zeros(nv); row[4*i] = 1; row[4*i+1:4*i+4] = w; A_eq.append(row); b_eq.append(1.0 if i == j else 0.0)
    for k in range(4):
        row = np.zeros(nv); row[k::4] = 1; A_eq.append(row); b_eq.append(1.0 if k == 0 else 0.0)
    r = linprog(np.zeros(nv), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(None, None)] * nv)
    return r.status == 0
cap = max(n for n in range(1, 7) if any(distinguishable(list(c)) for c in itertools.combinations(V, n)))
print("octahedron (all effects) capacity:", cap, "at affine dimension 3 (same as the qubit ball)")

# Counting step: a polytope composite has finitely many pure states, each purifies one marginal;
# the marginals form a convex set with a segment, so uncountably many states need purifying.
print("counting: a segment of A-states has continuum many points; a polytope AB has", len(stab2),
      "-like finite vertex sets => at most finitely many A-states purified")
