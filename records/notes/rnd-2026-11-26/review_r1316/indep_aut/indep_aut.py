# Independent check (reviewer's own code, no repo code, no sympy): exact Q(sqrt5) arithmetic with Fractions,
# facets by brute force, K = E (E^T E)^-1 E^T per factor, K_AB = K_A (x) K_B, then |Aut| of the edge-coloured
# complete graph on facets via nauty (dreadnaut). All automorphisms local  <=>  |Aut(K_AB)| == |Aut(K_A)|*|Aut(K_B)|
# (local maps act faithfully on facets). Positive control: triangle x triangle (classical), where non-local maps exist.
import itertools, subprocess, sys, time
from fractions import Fraction as F
class Q5:
    __slots__=("p","q")
    def __init__(s,p=0,q=0): s.p=F(p); s.q=F(q)
    def __add__(s,o): o=c(o); return Q5(s.p+o.p,s.q+o.q)
    __radd__=__add__
    def __neg__(s): return Q5(-s.p,-s.q)
    def __sub__(s,o): return s+(-c(o))
    def __rsub__(s,o): return c(o)-s
    def __mul__(s,o): o=c(o); return Q5(s.p*o.p+5*s.q*o.q, s.p*o.q+s.q*o.p)
    __rmul__=__mul__
    def inv(s): d=s.p*s.p-5*s.q*s.q; assert d!=0; return Q5(s.p/d,-s.q/d)
    def __truediv__(s,o): return s*c(o).inv()
    def __eq__(s,o): o=c(o); return s.p==o.p and s.q==o.q
    def __hash__(s): return hash((s.p,s.q))
    def f(s): return float(s.p)+float(s.q)*5**0.5
    def iszero(s): return s.p==0 and s.q==0
def c(x): return x if isinstance(x,Q5) else Q5(x)
phi=Q5(F(1,2),F(1,2)); iphi=phi-1
def cyc(t): return [t,(t[1],t[2],t[0]),(t[2],t[0],t[1])]
def signs(t):
    out=set()
    for s in itertools.product((1,-1),repeat=3): out.add(tuple(c(s[k])*c(t[k]) for k in range(3)))
    return out
def ico(): S=set(); [S.update(signs(t)) for t in cyc((Q5(0),Q5(1),phi))]; return list(S)
def dod():
    S=set(signs((Q5(1),Q5(1),Q5(1)))); [S.update(signs(t)) for t in cyc((Q5(0),iphi,phi))]; return list(S)
def tri():  # triangle in the plane (classical trit), exact rationals; centroid at 0
    return [(Q5(1),Q5(0),Q5(0)),(Q5(-1),Q5(1),Q5(0)),(Q5(0),Q5(-1),Q5(0))]
def sq(): return [(Q5(a),Q5(b),Q5(0)) for a,b in ((1,0),(0,1),(-1,0),(0,-1))]
def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q5(0))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def sgn(x): v=x.f(); return 0 if x.iszero() else (1 if v>0 else -1)
def facets3(V):
    """effects e=(1,-n/h): e(1,x)=1-n.x/h >= 0 on V, zero on a facet (3D polytope, centroid 0)."""
    out=set()
    for a,b,cc in itertools.combinations(V,3):
        n=cross(sub(b,a),sub(cc,a))
        if all(x.iszero() for x in n): continue
        h=dot(n,a)
        if h.iszero(): continue
        if sgn(h)<0: n=tuple(-x for x in n); h=-h
        if all(sgn(dot(n,v)-h)<=0 for v in V): out.add((Q5(1),)+tuple(-x/h for x in n))
    return sorted(out,key=lambda e:tuple(x.f() for x in e))
def facets2(V):
    out=set()
    for a,b in itertools.combinations(V,2):
        d=sub(b,a); n=(d[1],-d[0]); h=n[0]*a[0]+n[1]*a[1]
        if h.iszero(): continue
        if sgn(h)<0: n=(-n[0],-n[1]); h=-h
        if all(sgn(n[0]*v[0]+n[1]*v[1]-h)<=0 for v in V): out.add((Q5(1),-n[0]/h,-n[1]/h))
    return sorted(out,key=lambda e:tuple(x.f() for x in e))
def matinv(M):
    n=len(M); A=[list(r)+[Q5(1) if i==j else Q5(0) for j in range(n)] for i,r in enumerate(M)]
    for col in range(n):
        piv=next(r for r in range(col,n) if not A[r][col].iszero()); A[col],A[piv]=A[piv],A[col]
        iv=A[col][col].inv(); A[col]=[x*iv for x in A[col]]
        for r in range(n):
            if r!=col and not A[r][col].iszero():
                fct=A[r][col]; A[r]=[x-fct*y for x,y in zip(A[r],A[col])]
    return [r[n:] for r in A]
def Kmat(E):
    k=len(E[0]); G=[[sum((E[r][i]*E[r][j] for r in range(len(E))),Q5(0)) for j in range(k)] for i in range(k)]
    Gi=matinv(G)
    return [[sum((E[a][i]*Gi[i][j]*E[b][j] for i in range(k) for j in range(k)),Q5(0)) for b in range(len(E))] for a in range(len(E))]
def aut_order(K, tag):
    n=len(K); vals={}
    col=[[None]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i!=j: col[i][j]=vals.setdefault(K[i][j],len(vals))+1
    dvals={}; dcol=[dvals.setdefault(K[i][i],len(dvals)) for i in range(n)]
    L=max(1,(len(vals)).bit_length())
    N=n*L; adj=[set() for _ in range(N)]
    for l in range(L):
        for i in range(n):
            if l+1<L: adj[i+l*n].add(i+(l+1)*n)
            for j in range(i+1,n):
                if (col[i][j]>>l)&1: adj[i+l*n].add(j+l*n)
    cells=[]
    for l in range(L):
        for d in range(len(dvals)): cells.append([i+l*n for i in range(n) if dcol[i]==d])
    lines=[f"n={N} g"]
    for v in range(N): lines.append(f"{v}: "+" ".join(str(w) for w in sorted(adj[v]))+";")
    lines[-1]=lines[-1][:-1]+"."
    lines.append("f=["+" | ".join(",".join(map(str,cl)) for cl in cells)+"]")
    lines.append("x"); lines.append("q")
    out=subprocess.run(["dreadnaut"],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout
    g=[ln for ln in out.split("\n") if "grpsize" in ln]
    return len(vals), len(dvals), (g[0].strip() if g else out[-400:])
t0=time.time()
EI=facets3(ico()); ED=facets3(dod()); ET=facets2(tri()); ES=facets2(sq())
print("facets: ico", len(EI), "dod", len(ED), "tri", len(ET), "sq", len(ES))
print("facet sums (should be (n,0,0,0)):", [ (sum((e[k] for e in EI),Q5(0)).f()) for k in range(4)], [ (sum((e[k] for e in ED),Q5(0)).f()) for k in range(4)])
KI=Kmat(EI); KD=Kmat(ED); KT=Kmat(ET); KS=Kmat(ES)
def kron(A,B): return [[A[i//len(B)][j//len(B)]*B[i%len(B)][j%len(B)] for j in range(len(A)*len(B))] for i in range(len(A)*len(B))]
print("per-factor distinct K values: ico", len({x for r in KI for x in r}), "dod", len({x for r in KD for x in r}))
for tag,K in (("ico",KI),("dod",KD),("tri",KT),("sq",KS),("tri x tri (control: classical, expect 9! = 362880)",kron(KT,KT)),
              ("sq x sq (boxworld, Gross et al.: expect local only, 8*8*2 = 128 incl. swap)",kron(KS,KS)),
              ("ico x dod (expect 120*120 = 14400 if all automorphisms are local)",kron(KI,KD))):
    nv,nd,g=aut_order(K,tag); print(f"{tag}: facets {len(K)}, distinct off-diagonal K values {nv}, diagonal classes {nd}: {g}  [{time.time()-t0:.0f}s]", flush=True)
