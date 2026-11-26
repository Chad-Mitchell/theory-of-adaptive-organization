# Round 13-M: exact rational re-check of the cert3 certificate for cuboctahedron^2 (and P4/P6 sanity, cube, octahedron).
# Unnormalised rational coordinates: CO vertices = permutations of (+-1,+-1,0), radius^2 = 2; invariant metric scaled
# so that the condition reads Phi = 9(||C||^2/R^4 - 1) - 3(1 - |a|^2/R^2) - 3(1 - |b|^2/R^2) <= 0; Lorentz form J = diag(R^2,-1,-1,-1).
# Exact: build the LP data in Fractions, solve in floats, then re-solve the active system exactly and verify all signs.
import itertools, sys, numpy as np, sympy as sp
from fractions import Fraction as F
from scipy.optimize import linprog
def co():
    V=set()
    for p in itertools.permutations((1,1,0)):
        for s in itertools.product((1,-1),repeat=3): V.add(tuple(a*b for a,b in zip(p,s)))
    V=sorted(V)
    E=[(1,)+tuple(-x for x in n) for n in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]  # squares: x_i <= 1
    E+=[(1,)+tuple(-F(s,2) for s in sg) for sg in itertools.product((1,-1),repeat=3)]           # triangles: (s.x) <= 2
    return [list(map(F,v)) for v in V],[list(map(F,e)) for e in E],F(2)
def check_part(V,E):
    for v in V:
        vals=[e[0]+sum(a*b for a,b in zip(e[1:],v)) for e in E]
        assert min(vals)>=0
def run(name,part):
    V,E,R2=part; check_part(V,E); m=len(V[0]); d=m+1
    J=[[R2 if (i==j==0) else (-1 if i==j else 0) for j in range(d)] for i in range(d)]
    def outer(a,b): return [[x*y for y in b] for x in a]
    def add(A,B): return [[x+y for x,y in zip(r,s)] for r,s in zip(A,B)]
    def kron(A,B): return [[A[i][j]*B[k][l] for j in range(d) for l in range(d)] for i in range(d) for k in range(d)]
    def ip(x,y): return sum(a*b for a,b in zip(x[1:],y[1:]))
    W=[(0,e) for e in E]+[(1,[R2]+list(v)) for v in V]       # (R^2, v) is in K* since R^2 + v.r >= R^2 - |v||r| >= 0
    def classes(L,key):
        d_={}; out={}
        for i,(ti,wi) in enumerate(L):
            for j,(tj,wj) in enumerate(L):
                k=key(ti,wi,tj,wj); out.setdefault(d_.setdefault(k,len(d_)),[]).append((i,j))
        return out
    cE=classes([(0,e) for e in E],lambda ti,wi,tj,wj:ip(wi,wj)); cW=classes(W,lambda ti,wi,tj,wj:(min(ti,tj),max(ti,tj),ip(wi,wj)))
    def grp(L,pairs):
        M=[[F(0)]*d for _ in range(d)]
        for i,j in pairs: M=add(M,outer(L[i][1],L[j][1]))
        return [[(M[i][j]+M[j][i])/2 for j in range(d)] for i in range(d)]
    ME=[grp([(0,e) for e in E],p) for p in cE.values()]; MW=[grp(W,p) for p in cW.values()]
    mats=[kron(A,B) for A in ME for B in ME]+[kron(N,J) for N in MW]+[kron(J,N) for N in MW]
    def blocks(M):
        g=lambda i,k,j,l: M[i*d+k][j*d+l]
        return [g(0,0,0,0), sum(g(i,0,i,0) for i in range(1,d))/m, sum(g(0,k,0,k) for k in range(1,d))/m,
                sum(g(i,k,i,k) for i in range(1,d) for k in range(1,d))/(m*m)]
    Mb=[blocks(M) for M in mats]
    # -Q blocks in these coordinates: x^T(-Q)x = (mA+mB+mAmB) x0^2 - (mA/R2)|a|^2 - (mB/R2)|b|^2 - (mAmB/R2^2)||C||^2
    nQ=[F(m+m+m*m), F(-m)/R2, F(-m)/R2, F(-m*m)/(R2*R2)]
    A=np.array([[float(x) for x in col] for col in Mb]).T; b=np.array([float(x) for x in nQ])
    r=linprog(np.zeros(A.shape[1]),A_ub=A,b_ub=b,bounds=[(0,None)]*A.shape[1],method='highs')
    if r.status!=0: print(f"{name}: float LP infeasible"); return
    supp=[k for k,x in enumerate(r.x) if x>1e-12]
    # exact: least-norm exact solution of the active rows on the support, then verify
    act=[i for i in range(4) if abs(b[i]-A[i]@r.x)<1e-9]
    Ms=sp.Matrix([[sp.Rational(Mb[k][i].numerator,Mb[k][i].denominator) for k in supp] for i in act])
    rhs=sp.Matrix([sp.Rational(nQ[i].numerator,nQ[i].denominator) for i in act])
    sol=None
    try:
        sol=Ms.pinv()*rhs
    except Exception as ex: print("pinv failed",ex)
    lam={k:sol[t] for t,k in enumerate(supp)} if sol is not None else {}
    ok_sign=all(v>=0 for v in lam.values())
    resid=[sp.Rational(nQ[i].numerator,nQ[i].denominator)-sum(sp.Rational(Mb[k][i].numerator,Mb[k][i].denominator)*lam[k] for k in supp) for i in range(4)]
    ok=ok_sign and all(x>=0 for x in resid)
    print(f"{name}: {len(Mb)} multipliers, support {len(supp)}; exact multipliers >= 0: {ok_sign}; exact S blocks = {[str(x) for x in resid]} -> {'EXACT CERTIFICATE: diamond holds on all of max' if ok else 'exact re-check failed'}", flush=True)
run("max(CO,CO)", co())
