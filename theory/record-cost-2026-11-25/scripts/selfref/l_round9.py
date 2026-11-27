"""L: round 9. (Repo copy: candidate diagonal sets are all combinations of distinct permutations; the session copy
repeated entries and under-reported the CP^2 capacity as 2.)
L2 price the law-memory a tracker needs to keep a 1-bit record readable at error <= eps under an unknown, nontrivial,
   RELATIVE reversible law: disk (re-learning), ball (axis memory, no re-learning), classical bit / square / simplex
   (finite period memory, exact).
L3 capacity of non-Jordan transitive orbitopes in dims 4-8 (LP with sampled positivity), plus sanity checks (B^3, CP^2).
"""
import numpy as np, itertools
from scipy.optimize import linprog
from scipy.special import sph_harm_y
from scipy.stats import unitary_group
rng=np.random.default_rng(9)
print("L2 standing law-memory (bits) + re-learning rate (bits/tick) to hold a 1-bit record at read error <= eps")
def disk_cost(eps,kappa=1.0):
    best=None
    for b in range(1,60):
        delta=2*np.pi*2.0**-b
        D=2*np.arcsin(np.sqrt(eps))
        if delta/2>=D: continue
        T=(D-delta/2)/(delta/2)
        rate=kappa*2*b/max(T,1e-12)
        tot=b+rate
        if best is None or tot<best[0]: best=(tot,b,rate)
    return best
def ball_cost(eps):
    D=2*np.arcsin(np.sqrt(eps)); cap=(1-np.cos(D))/2
    return np.log2(1/cap)
def simplex_expected(n):
    perms=list(itertools.permutations(range(n))); tot=0
    for p in perms:
        for v in range(n):
            L=1; j=p[v]
            while j!=v: j=p[j]; L+=1
            tot+=np.log2(L)/n
    return tot/len(perms)
sq_laws={'id':0,'r90':2,'r180':1,'r270':2,'diag1':0,'diag2':0,'edge1':1,'edge2':1}
print(f"  {'eps':>7s} | disk (standing+relearn) | ball (axis memory) | classical bit E[.] | square E[.] | simplex n=3 E[.]")
for eps in (1e-1,1e-2,1e-3,1e-4):
    d=disk_cost(eps); bl=ball_cost(eps)
    print(f"  {eps:7.0e} | {d[0]:6.2f} (b={d[1]}, rate {d[2]:.3f}) | {bl:6.2f}            | {0.5:5.2f}              | {np.mean(list(sq_laws.values())):5.3f}       | {simplex_expected(3):.3f}")
print("  (finite-group memories are exact and eps-independent; continuous ones grow ~log2(1/eps); disk-ball gap = re-learning + O(1))")
print("\nL3 capacity by LP: N points, effects = affine functionals >= 0 on the sampled orbit, summing to the unit")
def fib(M):
    i=np.arange(M)+0.5; ph=np.arccos(1-2*i/M); th=np.pi*(1+5**0.5)*i
    return np.stack([np.cos(th)*np.sin(ph),np.sin(th)*np.sin(ph),np.cos(ph)],1)
def feat_ball(n): return n
def feat_12(n):
    x,y,z=n.T; return np.stack([x,y,z,x*x-y*y,3*z*z-1,x*y,x*z,y*z],1)
def feat_3(n):
    x,y,z=n.T; th=np.arccos(np.clip(z,-1,1)); ph=np.arctan2(y,x); cols=[]
    for m in range(0,4):
        Y=sph_harm_y(3,m,th,ph); cols.append(Y.real)
        if m>0: cols.append(Y.imag)
    return np.stack(cols,1)
GM=[np.array(a,complex) for a in [[[0,1,0],[1,0,0],[0,0,0]],[[0,-1j,0],[1j,0,0],[0,0,0]],[[1,0,0],[0,-1,0],[0,0,0]],
    [[0,0,1],[0,0,0],[1,0,0]],[[0,0,-1j],[0,0,0],[1j,0,0]],[[0,0,0],[0,0,1],[0,1,0]],[[0,0,0],[0,0,-1j],[0,1j,0]],
    [[1,0,0],[0,1,0],[0,0,-2]]]]
def herm_feat(X): return np.array([np.real(np.trace(g@X)) for g in GM])
def adj_orbit(lam,M):
    out=[]
    for _ in range(M):
        U=unitary_group.rvs(3,random_state=rng); out.append(herm_feat(U@np.diag(lam)@U.conj().T))
    return np.array(out)
def distinguishable(P,S):
    N,D=P.shape; nv=N*(1+D)
    A_ub=[]
    for i in range(N):
        blk=np.zeros((S.shape[0],nv)); blk[:,i*(1+D)]=-1; blk[:,i*(1+D)+1:(i+1)*(1+D)]=-S; A_ub.append(blk)
    A_ub=np.vstack(A_ub); b_ub=np.full(A_ub.shape[0],1e-9)
    A_eq=[];b_eq=[]
    for i in range(N):
        for j in range(N):
            r=np.zeros(nv); r[i*(1+D)]=1; r[i*(1+D)+1:(i+1)*(1+D)]=P[j]; A_eq.append(r); b_eq.append(1.0 if i==j else 0.0)
    r=np.zeros(nv); r[[i*(1+D) for i in range(N)]]=1; A_eq.append(r); b_eq.append(1.0)
    for k in range(D):
        r=np.zeros(nv); r[[i*(1+D)+1+k for i in range(N)]]=1; A_eq.append(r); b_eq.append(0.0)
    res=linprog(np.zeros(nv),A_ub=A_ub,b_ub=b_ub,A_eq=np.array(A_eq),b_eq=np.array(b_eq),bounds=[(None,None)]*nv,method='highs')
    return res.status==0
def sphere_capacity(feat,name,dim):
    S=feat(fib(4000)); cap=1
    tests={2:[np.array([[0,0,1],[0,0,-1.]])],
           3:[np.eye(3),np.array([[1,0,0],[-.5,np.sqrt(3)/2,0],[-.5,-np.sqrt(3)/2,0]])],
           4:[np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1.]])/np.sqrt(3),np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0.]])]}
    for N in (2,3,4):
        cands=tests[N]+[(lambda v: v/np.linalg.norm(v,axis=1,keepdims=True))(rng.normal(size=(N,3))) for _ in range(40)]
        if any(distinguishable(feat(c),S) for c in cands): cap=N
        else: break
    print(f"  {name:48s} dim {dim}: capacity found {cap}",flush=True)
sphere_capacity(feat_ball,"B^3 (sanity)",3)
sphere_capacity(feat_12,"S^2 orbitope, spin 1+2 (qutrit coherent states)",8)
sphere_capacity(feat_3,"S^2 orbitope, spin 3 (odd zonal)",7)
for lam,name in [((2/3,-1/3,-1/3),"CP^2 = complex QM d=3 (sanity)"),((1,0,-1),"flag orbitope SU(3)/T (regular adjoint orbit)")]:
    S=adj_orbit(np.array(lam),5000); cap=1
    perms=sorted(set(itertools.permutations(lam)))
    for N in (2,3,4,6):
        cands=[np.array([herm_feat(np.diag(p)) for p in comb]) for comb in itertools.combinations(perms,N)]
        for _ in range(30):
            cands.append(np.array([herm_feat((lambda U: U@np.diag(lam)@U.conj().T)(unitary_group.rvs(3,random_state=rng))) for _ in range(N)]))
        if any(distinguishable(c,S) for c in cands): cap=N
        else: break
    print(f"  {name:48s} dim 8: capacity found {cap}",flush=True)
print("\nL3b SFP for these orbitopes: pure states G/H; pass iff H contains a maximal torus of G")
print("  spin 1+2 and spin 3 orbits of a zonal vector: H=SO(2) (max torus of SO(3)) -> pass; Caratheodory SO(2)-orbitope in R^4: H trivial -> fail;")
print("  flag orbitope SU(3)/T: H=T -> pass; generic SO(3) orbit in spin 2 (distinct eigenvalues): H finite -> fail; torus orbitopes: fail")
