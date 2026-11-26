"""Round 12-M: zero-marginal slice of max(A,B) for 3D parts: maximise tr(O^T C) subject to 1 + n^T C m >= 0 (a = b = 0)
for O = +-identity and 4000 random orthogonal O (seed 7); report the largest Phi = 9(||C||^2 - 1) - 6 found.
A search, not a proof: Phi > 0 refutes (diamond) on max (Phi is convex), Phi <= 0 does not prove it. Prints only."""
import sys
import numpy as np
from scipy.optimize import linprog
from scipy.stats import special_ortho_group
from m_round12_parts import PARTS
rng = np.random.default_rng(7)
def run(na, nb, K=4000):
    NA = [e[1:] for e in PARTS[na]()]; NB = [f[1:] for f in PARTS[nb]()]
    A_ub = -np.array([np.outer(n, m).flatten() for n in NA for m in NB]); b_ub = np.ones(len(A_ub))
    best = -1e9
    Os = [np.eye(3), -np.eye(3)]+[special_ortho_group.rvs(3, random_state=rng)*s for _ in range(K//2) for s in (1, -1)]
    for O in Os:
        r = linprog(-O.flatten(), A_ub=A_ub, b_ub=b_ub, bounds=[(None, None)]*9, method='highs')
        if r.status != 0:
            continue
        ph = 9*((r.x**2).sum()-1)-6
        if ph > best:
            best, bc = ph, (r.x**2).sum()
    print(f"max({na},{nb}) zero-marginal slice: best Phi = {best:+.6f} (||C||^2 = {bc:.6f}) over {len(Os)} objectives -> diamond {'FAILS on max' if best > 1e-9 else 'not refuted'}")
if __name__ == "__main__":
    for s in (sys.argv[1:] or ['cube3xcube3', 'oct3xoct3', 'IxI', 'DxD', 'COxCO', 'IxD']):
        run(*s.split('x'))
