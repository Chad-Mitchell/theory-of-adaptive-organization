"""P-info pricing (secondary): lambda per nat of record-world information, regime D (stationary trackers).
b priced by Holevo chi; c1 by I of its canonical density; c-RD = noiseless point read through the best covariant channel
with I <= ln N (Gibbs family p ~ exp(beta cos - nu 1_tail)). Decision rule as PREREG sec 6 (b vs c-RD)."""
import numpy as np, duel_core as d, collections
NS = [2,3,4,5,6,8,12,16,24,32,48,64]; LAMS = [0, 1e-4, 1e-3, 1e-2, 1e-1]; EPSS = [0.05, 1e-2, 1e-3]
cosg = np.cos(d.CENT)
def b_path(N, eps):
    """designs on the Lagrange path mu in [mu_eps, inf) plus mu-scan; returns list of (stake, chi, Ican, tail)."""
    A = d.stake_matrix(N); B = d.tail_matrix(N)
    out = []
    for mu in np.concatenate([[0], np.geomspace(1e-3, 1e4, 120)]):
        w, V = np.linalg.eigh(A - mu*B); c = V[:, -1]
        tl = c@B@c
        if tl > eps: continue
        p2 = c**2; chi = -np.sum(p2*np.log(p2+1e-300))
        z = np.exp(1j*np.outer(d.CENT, np.arange(N)))@c; m = np.abs(z)**2; m /= m.sum()
        out.append((1-c@A@c, chi, d.info_of_density(m), tl))
    return out
def crd_designs():
    out = []
    for beta in np.concatenate([[0], np.geomspace(0.05, 20000, 160)]):
        for nu in [0, 0.5, 1, 2, 4, 8, 16, 40]:
            m = d.gibbs_density(beta, nu)
            out.append((1-np.sum(m*cosg), d.info_of_density(m), m[d.TAILMASK].sum()))
    return np.array(out)
CRD = crd_designs()
cells = []; lines = []
for N in NS:
    for eps in EPSS:
        bp = b_path(N, eps)
        ok = CRD[(CRD[:, 2] <= eps) & (CRD[:, 1] <= np.log(N) + 1e-9)]
        for lam in LAMS:
            Jb = min((s + lam*chi) for s, chi, I, tl in bp) if bp else None
            Jc1 = min((s + lam*I) for s, chi, I, tl in bp) if bp else None
            Jr = (ok[:, 0] + lam*ok[:, 1]).min() if len(ok) else None
            if Jb is None and Jr is None: continue
            if Jb is None: o = 'LOSE'
            elif Jr is None: o = 'WIN'
            else:
                tol = 0.01*max(Jb, Jr) + 1e-12; o = 'WIN' if Jr - Jb > tol else ('LOSE' if Jb - Jr > tol else 'TIE')
            if lam > 0: cells.append(o)
            if lam in (0, 1e-2): lines.append(f"N={N:3d} eps={eps:g} lam={lam:g}: J_b={Jb if Jb is None else round(Jb,5)} J_c1={Jc1 if Jc1 is None else round(Jc1,5)} J_cRD={Jr if Jr is None else round(Jr,5)} -> {o}")
c = collections.Counter(cells); n = len(cells)
lab = 'WIN' if c['WIN']/n >= .9 and c['LOSE'] == 0 else ('LOSE' if c['LOSE']/n >= .5 else ('TIE' if c['TIE']/n >= .9 else 'MIXED'))
print("\n".join(lines)); print(f"\nP-info aggregate (lambda>0), b vs c-RD: {lab} {dict(c)}")
