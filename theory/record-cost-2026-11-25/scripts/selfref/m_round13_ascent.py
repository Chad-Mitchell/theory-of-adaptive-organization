# Round 13-M, H1/H2 search: convex-maximisation ascent for Phi on max(A,B) (3D parts). From a random start, repeatedly
# solve max grad Phi(x_k) . x over max (an LP; optimum at a vertex) until the vertex repeats. Phi is convex, so each step
# does not decrease Phi; the end points are vertices that are local maxima of Phi along LP steps. A search, not a proof.
import sys, numpy as np
from scipy.optimize import linprog
from m_round12_parts import PARTS
rng=np.random.default_rng(int(__import__("os").environ.get("SEED","13")))
def run(na,nb,starts=1500):
    EA,EB=np.array(PARTS[na]()),np.array(PARTS[nb]())
    A_ub=-np.array([np.kron(e,f) for e in EA for f in EB])[:,1:]; b_ub=np.ones(len(A_ub))
    W=np.zeros((4,4)); W[1:,0]=3; W[0,1:]=3; W[1:,1:]=9   # Phi = sum W*X^2 - 15
    best=-1e9; bestX=None; ends=set()
    for s in range(starts):
        g=rng.normal(size=15); prev=None
        for it in range(50):
            r=linprog(-g,A_ub=A_ub,b_ub=b_ub,bounds=[(None,None)]*15,method='highs')
            x=np.round(r.x,9); key=tuple(x)
            if key==prev: break
            prev=key; X=np.concatenate([[1],r.x]).reshape(4,4); g=(2*W*X).flatten()[1:]
        X=np.concatenate([[1],r.x]).reshape(4,4); ph=(W*X**2).sum()-15
        prod=abs((X[1:,0]**2).sum()-1)<1e-7 and abs((X[0,1:]**2).sum()-1)<1e-7
        if not prod:
            ends.add(round(ph,6))
            if ph>best: best,bestX=ph,X
    print(f"max({na},{nb}): {starts} ascents; non-product end points: {len(ends)} distinct Phi values; best Phi = {best:+.6f} "
          f"(|a|^2={bestX[1:,0]@bestX[1:,0]:.4f}, |b|^2={bestX[0,1:]@bestX[0,1:]:.4f}, ||C||^2={(bestX[1:,1:]**2).sum():.6f}); "
          f"top values {sorted(ends)[-4:]}", flush=True)
for s in (sys.argv[1:] or ['IxI','DxD','COxCO','IxD']): run(*s.split('x'))
