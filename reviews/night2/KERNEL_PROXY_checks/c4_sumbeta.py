"""POST HOC (descriptive): block-bootstrap sd of the total kernel loading (sum of per-age weights) for z, ybar, L and
of the paired difference z - ybar, common rows, same blocks/seed as c1."""
import numpy as np, json, runpy
g = runpy.run_path('c1_data.py', run_name='lib')
X, rows, tgt, BLOCK = g['X'], g['rows'], g['tgt'], g['BLOCK']
from plib import EDGES
ok = rows & np.isfinite(tgt['z']) & np.isfinite(tgt['ybar']) & np.isfinite(tgt['L'])
Xo = X[ok]; T = {k: v[ok] for k, v in tgt.items()}; m = len(Xo) // BLOCK * BLOCK; nb = m // BLOCK
Xb = Xo[:m].reshape(nb, BLOCK, -1); XtX = np.einsum('bti,btj->bij', Xb, Xb)
Xty = {k: np.einsum('bti,bt->bi', Xb, v[:m].reshape(nb, BLOCK)) for k, v in T.items()}
sz = np.diff(EDGES)
def s(idx): A = XtX[idx].sum(0); return {k: np.linalg.solve(A, Xty[k][idx].sum(0))[1:] @ sz for k in T}
full = s(np.arange(nb)); rng = np.random.default_rng(20261133); bs = [s(rng.integers(0, nb, nb)) for _ in range(999)]
out = {k: [float(full[k]), float(np.std([b[k] for b in bs], ddof=1))] for k in T}
out['z_minus_ybar'] = [float(full['z'] - full['ybar']), float(np.std([b['z'] - b['ybar'] for b in bs], ddof=1))]
json.dump(out, open('c4_sumbeta.json', 'w'), indent=1); print(out)
