# Independent reviewer code for the odd analogue (M2 of HOSTILE_REVIEW_SRB4.md). Imports nothing from sr_b/, sr_b4/ or review_srb4/.
# Model: regular n-gon (circumradius 1) with ALL effects; operational distance d(a,b) = max_e [e(a)-e(b)].
# For a convex body K, max over affine effects 0<=e<=1 of e(a)-e(b) equals the gauge of a-b in the difference body K-K.
# Facet normals of K-K are the union of facet normals of K and -K, so d(a,b) = max over nu in {+-edge normals of K} of <nu,a-b>/w_K(nu),
# where the width w_K(nu) is computed here DIRECTLY as max-min of <nu,v> over vertices (no closed form).
import math, itertools, mpmath as mp
import numpy as np
from scipy.optimize import linprog

def verts(n):
    return [(mp.cos(2*mp.pi*k/n), mp.sin(2*mp.pi*k/n)) for k in range(n)]

def dist_row_gauge(n):
    """d(v0, vk) for k=0..n-1, mp precision, via difference-body facet normals with directly computed widths."""
    V = verts(n)
    normals = []
    for i in range(n):
        a, b = V[i], V[(i+1) % n]
        ex, ey = b[0]-a[0], b[1]-a[1]
        L = mp.sqrt(ex*ex+ey*ey)
        nx, ny = ey/L, -ex/L          # one unit normal of edge i
        normals += [(nx, ny), (-nx, -ny)]
    data = []
    for (nx, ny) in normals:
        p = [nx*v[0]+ny*v[1] for v in V]
        data.append((p, max(p)-min(p)))
    row = []
    for k in range(n):
        row.append(max((p[0]-p[k])/w for (p, w) in data))
    return row

def dist_lp(n, k):
    """float LP over affine effects e(x)=c+t.x with 0<=e(v)<=1 on all vertices; maximise e(v0)-e(vk)."""
    V = np.array([[1, math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)] for i in range(n)])
    g = V[0]-V[k]
    r = linprog(-g, A_ub=np.vstack([V, -V]), b_ub=np.concatenate([np.ones(n), np.zeros(n)]),
                bounds=[(None, None)]*3, method="highs")
    return -r.fun

def dp_exact(row, T, targets, zero):
    """min over paths of EXACTLY T ticks (each tick: jump to any vertex, staying put = jump of d=0), from v0 to any target.
    No step cap, no direction restriction. Uses dihedral transitivity: d(vi,vj) = row[(j-i)%n]. Returns value."""
    n = len(row)
    sq = [r*r for r in row]
    inf = None
    best = [zero if i == 0 else inf for i in range(n)]
    for _ in range(T):
        nb = [inf]*n
        for i in range(n):
            if best[i] is None: continue
            bi = best[i]
            for j in range(n):
                c = bi + sq[(j-i) % n]
                if nb[j] is None or c < nb[j]: nb[j] = c
        best = nb
    return min(best[t] for t in targets)

def dp_np(row, T, targets):
    """float64 vectorised version of dp_exact for large n."""
    n = len(row); sq = np.array([float(r)**2 for r in row])
    idx = (np.arange(n)[None, :]-np.arange(n)[:, None]) % n
    C = sq[idx]
    best = np.full(n, np.inf); best[0] = 0.0
    for _ in range(T):
        best = np.min(best[:, None]+C, axis=0)
    return min(best[t] for t in targets)

def brute(row, T, targets):
    n = len(row); sq = [r*r for r in row]; b = None
    for seq in itertools.product(range(n), repeat=T):
        if seq[-1] not in targets: continue
        prev = 0; c = 0
        for s in seq:
            c += sq[(s-prev) % n]; prev = s
        if b is None or c < b: b = c
    return b

def disk(T):
    return T*mp.sin(mp.pi/(2*T))**2
