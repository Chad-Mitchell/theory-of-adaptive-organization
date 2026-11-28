# Independent exact re-check of LEMMA_R.md numerics (hostile review). Exact arithmetic in Q(sqrt5) (pairs of Fractions).
# Pentagon: affine image of the regular pentagon, x_k = cos(72k deg), y_k = sin(72k)/sin(72) -- all in Q(sqrt5).
from fractions import Fraction as F
import itertools, sys
class Q5:
    __slots__=('a','b')
    def __init__(s,a,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o): o=o if isinstance(o,Q5) else Q5(o); return Q5(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __neg__(s): return Q5(-s.a,-s.b)
    def __sub__(s,o): return s+(-(o if isinstance(o,Q5) else Q5(o)))
    def __mul__(s,o): o=o if isinstance(o,Q5) else Q5(o); return Q5(s.a*o.a+5*s.b*o.b,s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def inv(s): n=s.a*s.a-5*s.b*s.b; return Q5(s.a/n,-s.b/n)
    def __truediv__(s,o): o=o if isinstance(o,Q5) else Q5(o); return s*o.inv()
    def iszero(s): return s.a==0 and s.b==0
    def __eq__(s,o): o=o if isinstance(o,Q5) else Q5(o); return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
Z=Q5(0); O=Q5(1)
c1=Q5(F(-1,4),F(1,4))   # cos72
c2=Q5(F(-1,4),F(-1,4))  # cos144
def pent(): xs=[O,c1,c2,c2,c1]; ys=[Z,O,2*c1,-2*c1,-O]; return [[O,xs[k],ys[k]] for k in range(5)]
def square(): return [[O,Q5(1),Q5(1)],[O,Q5(-1),Q5(1)],[O,Q5(-1),Q5(-1)],[O,Q5(1),Q5(-1)]]
def bit(): return [[O,Q5(1)],[O,Q5(-1)]]
def cube(): return [[O]+[Q5(s) for s in v] for v in itertools.product((1,-1),repeat=3)]
def sqpyr(): return [[O,Q5(1),Q5(1),Z],[O,Q5(-1),Q5(1),Z],[O,Q5(-1),Q5(-1),Z],[O,Q5(1),Q5(-1),Z],[O,Z,Z,Q5(1)]]
def kron(a,b): return [x*y for x in a for y in b]
def rank(M):
    M=[r[:] for r in M]; r=0; n=len(M[0])
    for c in range(n):
        p=next((i for i in range(r,len(M)) if not M[i][c].iszero()),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; iv=M[r][c].inv()
        for i in range(len(M)):
            if i!=r and not M[i][c].iszero():
                f=M[i][c]*iv; M[i]=[M[i][k]-f*M[r][k] for k in range(n)]
        r+=1
    return r
def solve_inv(G):
    n=len(G); A=[G[i][:]+[O if i==j else Z for j in range(n)] for i in range(n)]
    for c in range(n):
        p=next(i for i in range(c,n) if not A[i][c].iszero()); A[c],A[p]=A[p],A[c]; iv=A[c][c].inv()
        A[c]=[x*iv for x in A[c]]
        for i in range(n):
            if i!=c and not A[i][c].iszero():
                f=A[i][c]; A[i]=[A[i][k]-f*A[c][k] for k in range(2*n)]
    return [r[n:] for r in A]
def prodset(A,B): return [((i,j),kron(a,b)) for i,a in enumerate(A) for j,b in enumerate(B)]
def d4(A,B):
    P=prodset(A,B); tot=bad=0
    for Y in itertools.combinations(P,4):
        if len({y[0][0] for y in Y})>1 and len({y[0][1] for y in Y})>1:
            tot+=1; bad+= rank([y[1] for y in Y])<4
    return tot,bad
def autos(X):
    N=len(X); d=len(X[0])
    G=[[sum((x[i]*x[j] for x in X),Z) for j in range(d)] for i in range(d)]; Gi=solve_inv(G)
    GX=[[sum((Gi[i][k]*x[k] for k in range(d)),Z) for i in range(d)] for x in X]
    K=[[sum((X[i][k]*GX[j][k] for k in range(d)),Z) for j in range(N)] for i in range(N)]
    res=[]
    def rec(img):
        k=len(img)
        if k==N: res.append(img[:]); return
        for c in range(N):
            if c in img or K[c][c]!=K[k][k]: continue
            if all(K[c][img[t]]==K[k][t] for t in range(k)):
                img.append(c); rec(img); img.pop()
    rec([]); return res,K
def lines_ok(perm,idx,nA,nB):
    img=[idx[p] for p in perm]; pos={idx[k]:k for k in range(len(idx))}
    for L in [[(i,j) for j in range(nB)] for i in range(nA)]+[[(i,j) for i in range(nA)] for j in range(nB)]:
        S=[img[pos[x]] for x in L]
        if not(len({s[0] for s in S})==1 or len({s[1] for s in S})==1): return False
    return True
def linear_check(X,perm):
    # exact: the map X_k -> X_perm(k) is linear iff rank[X | X_perm] == rank X  (rows = points)
    return rank([X[k]+X[perm[k]] for k in range(len(X))])==rank(X)
for name,A,B in [("square^2",square(),square()),("pentagon^2 (affine, Q(sqrt5))",pent(),pent()),
                 ("square x pentagon",square(),pent()),("bit x pentagon",bit(),pent()),
                 ("cube^2 (Lemma D only)",cube(),cube()),("square-pyramid x square (Lemma D only)",sqpyr(),square())]:
    tot,bad=d4(A,B)
    line=f"{name:40s} mixed4={tot:6d} dependent={bad}"
    if "only" not in name:
        P=prodset(A,B); X=[p[1] for p in P]; idx=[p[0] for p in P]
        perms,K=autos(X)
        lin=sum(linear_check(X,p) for p in perms)
        loc=sum(lines_ok(p,idx,len(A),len(B)) for p in perms)
        line+=f" | K-preserving perms={len(perms)} exactly-linear={lin} lines->lines={loc}"
    print(line); sys.stdout.flush()
