# Round 14-M, H1/H2: condition (diamond) on max(I,I) and max(D,D) by full float vertex enumeration (pycddlib), each
# reported vertex re-checked exactly in Q(sqrt5) (sympy): feasible, and its tight product-facet set has rank 15.
# Usage: python3 r14_h1h2_enum.py IxI | DxD.  Prints only.
import sys, time, numpy as np, sympy as sp
from m_round12_parts import max_vertices, PARTS
na,nb=sys.argv[1].split('x'); t=time.time()
X=max_vertices(na,nb)
a=X[:,1:,0]; b=X[:,0,1:]; C=X[:,1:,1:]
A2=(a**2).sum(1); B2=(b**2).sum(1); C2=(C**2).sum((1,2))
phi=9*(C2-1)-3*(1-A2)-3*(1-B2)
prod=(abs(A2-1)<1e-9)&(abs(B2-1)<1e-9)&(np.abs(C-np.einsum('ni,nj->nij',a,b)).max((1,2))<1e-9)
ent=~prod; i=int(np.argmax(np.where(ent,phi,-1e9)))
print(f"max({na},{nb}): {len(X)} extreme pts ({prod.sum()} product) [{time.time()-t:.0f}s]")
print(f"  max Phi over non-product = {phi[i]:+.6f} at |a|^2={A2[i]:.6f}, |b|^2={B2[i]:.6f}, ||C||^2={C2[i]:.6f}; #Phi>1e-9: {(phi[ent]>1e-9).sum()}")
# exact re-check of the maximiser (and of the 20 largest-Phi non-product vertices)
s5=sp.sqrt(5); phi_g=(1+s5)/2
def exact_parts(name):
    import itertools
    base={'I':[(0,1,phi_g)],'D':[(1,1,1),(0,1/phi_g,phi_g)]}[name]
    S=set()
    for bb in base:
        for c in (bb,(bb[1],bb[2],bb[0]),(bb[2],bb[0],bb[1])):
            for sg in itertools.product((1,-1),repeat=3): S.add(tuple(sp.nsimplify(sg[k]*c[k]) for k in range(3)))
    V=[sp.Matrix(v) for v in S]; R=sp.sqrt(sp.simplify(V[0].dot(V[0]))); V=[v/R for v in V]
    # facets from the float list, matched exactly: n with max_v n.v = 1, n = sum of the float normal's tight vertices
    E=[]
    for e in PARTS[name]():
        n=e[1:]; tight=[v for v in V if abs(float(-n@np.array([float(x) for x in v]))-1)<1e-7]
        M=sp.Matrix.hstack(*tight[:3]).T; nn=-(M.solve(sp.ones(3,1)))  # n.v = -1 on the facet (effect 1 + n.r >= 0)
        E.append(sp.Matrix([1]+[sp.nsimplify(sp.simplify(x)) for x in nn]))
    return E
EA,EB=exact_parts(na),exact_parts(nb)
FE=[sp.Matrix(sp.kronecker_product(e,f)) for e in EA for f in EB]
order=np.argsort(-np.where(ent,phi,-1e9))[:20]; worst=None; okall=True
for k in order:
    x=X[k].flatten(); vals=[float(np.kron(np.array([float(z) for z in e]),np.array([float(z) for z in f]))@x) for e in EA for f in EB]
    tight=[j for j,v in enumerate(vals) if abs(v)<1e-7]
    A=sp.Matrix.vstack(*[FE[j].T for j in tight]+[sp.Matrix([[1]+[0]*15])])
    rhs=sp.Matrix([0]*len(tight)+[1])
    sol=(A.T*A).LUsolve(A.T*rhs); sol=sp.Matrix([sp.nsimplify(sp.simplify(z)) for z in sol])
    rank=A.rank(simplify=True)
    feas=all(sp.simplify((FE[j].T*sol)[0])>=0 for j in range(len(FE)))
    Xe=sol.reshape(4,4); ph=sp.simplify(9*(sum(Xe[p,q]**2 for p in range(1,4) for q in range(1,4))-1)-3*(1-sum(Xe[p,0]**2 for p in range(1,4)))-3*(1-sum(Xe[0,q]**2 for q in range(1,4))))
    okall&= (rank==16 and feas)
    if worst is None: worst=(ph,float(ph),rank,feas)
print(f"  exact Q(sqrt5) re-check of the 20 largest-Phi non-product vertices: all exact vertices (rank 16 incl. normalisation, feasible): {okall}")
print(f"  exact Phi at the maximiser = {worst[0]} = {worst[1]:+.9f} (rank {worst[2]}, feasible {worst[3]})")
print(f"  -> diamond {'HOLDS on all enumerated vertices' if (phi[ent]<=1e-9).all() else 'FAILS'} [{time.time()-t:.0f}s]")
