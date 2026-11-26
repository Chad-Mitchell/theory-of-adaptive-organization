# POST-RUN DIAGNOSTIC (not part of the Round 14 lock; written and run at about 05:02 EST after H3 finished). Lines 2-27 are copied from lines 1-26 of r14_h3_exact.py; it checks whether the exact K classes were canonical.
# Round 14-M, H3 replication: the facet-grid automorphism search on max(I,D) of m_round13_h3.py, with the K-value
# classes computed EXACTLY in Q(sqrt5) (sympy) instead of float rounding. Prints only.
import sys, numpy as np, sympy as sp, itertools, time
from collections import Counter
from m_round12_parts import PARTS
s5=sp.sqrt(5); g=(1+s5)/2
def verts(name):
    base={'I':[(0,1,g)],'D':[(1,1,1),(0,1/g,g)]}[name]; S=set()
    for bb in base:
        for c in (bb,(bb[1],bb[2],bb[0]),(bb[2],bb[0],bb[1])):
            for sg in itertools.product((1,-1),repeat=3): S.add(tuple(sp.nsimplify(sg[k]*c[k]) for k in range(3)))
    V=[sp.Matrix(v) for v in S]; R=sp.sqrt(sp.simplify(V[0].dot(V[0]))); return [v/R for v in V]
def facets(name):
    V=verts(name); out=[]
    for e in PARTS[name]():
        n=e[1:]; tight=[v for v in V if abs(float(-(n@np.array([float(x) for x in v])))-1)<1e-7]
        M=sp.Matrix.hstack(*tight[:3]).T; nn=-(M.solve(sp.ones(3,1)))
        out.append([sp.Integer(1)]+[sp.radsimp(x) for x in nn])
    return out
t=time.time()
EA,EB=facets('I'),facets('D')
print("exact facets:", len(EA), len(EB), "; sums:", [sp.simplify(sum(e[k] for e in EA)) for k in range(4)], [sp.simplify(sum(f[k] for f in EB)) for k in range(4)])
# Gram of facets per factor (exact), then K for products = K_A (x) K_B with K_X = E (E^T E)^-1 E^T per factor
def Kfac(E):
    M=sp.Matrix(E); G=(M.T*M).applyfunc(sp.radsimp); return (M*G.inv()*M.T).applyfunc(sp.radsimp)
KA,KB=Kfac(EA),Kfac(EB)
# --- diagnostic appended after the H3 run (not part of the lock): are the exact classes canonical?
nA,nB=len(EA),len(EB)
for nm,K in (("K_I",KA),("K_D",KB)):
    sym=set(K); num=set(round(float(x),9) for x in K)
    canon=set(sp.nsimplify(sp.expand(x),[s5]) for x in K)
    print(nm, "distinct symbolic:", len(sym), "distinct numeric (1e-9):", len(num), "distinct after expand+nsimplify:", len(canon))
prodnum=set(round(float(a)*float(b),9) for a in set(KA) for b in set(KB))
print("product values, numeric distinct (1e-9) over symbolic entry pairs:", len(prodnum))
print(f"[{time.time()-t:.0f}s]")
