"""Independent helpers for the P15 review (operational distance by LP, no reuse of SR_B scripts)."""
import numpy as np
from scipy.optimize import linprog

def reg_poly(n, rot=0.0):
    a = rot + 2*np.pi*np.arange(n)/n
    return np.stack([np.cos(a), np.sin(a)], 1), a

def op_dist_lp(V, u, w, effects=None):
    """d(u,w) = max e(u)-e(w) over affine e with 0<=e<=1 on conv(V) (all effects),
    or over a given finite effect list plus complements (restricted effects)."""
    if effects is not None:
        best = 0.0
        for (a, b) in effects:
            for (aa, bb) in ((a, b), (1-a, -b)):
                best = max(best, (aa + bb @ u) - (aa + bb @ w))
        return best
    c = -np.array([0.0, *(u - w)])          # variables a,b1,b2 ; maximize b.(u-w)
    A = np.vstack([np.c_[np.ones(len(V)), V], -np.c_[np.ones(len(V)), V]])
    bnd = np.r_[np.ones(len(V)), np.zeros(len(V))]
    r = linprog(c, A_ub=A, b_ub=bnd, bounds=[(None, None)]*3, method="highs")
    assert r.status == 0
    return -r.fun

def disk_dist(phi):
    """pure states of the unit disk at angular separation phi"""
    return abs(np.sin(phi/2))

def poly_dist_matrix(V):
    n = len(V)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            D[i, j] = D[j, i] = op_dist_lp(V, V[i], V[j])
    return D
