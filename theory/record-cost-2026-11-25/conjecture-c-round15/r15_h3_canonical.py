# Round 15-M, H3 with canonical exact classes: the facet-grid automorphism search on max(I,D) of r14_h3_exact.py, but every
# K value is mapped into the number field Q(sqrt5) (sympy QQ.algebraic_field), whose elements p + q*sqrt5 have a unique
# coefficient form, before values are compared. Round 14's radsimp forms were not canonical (413 classes). Prints only.
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
FQ=sp.QQ.algebraic_field(s5)
def canon(x):
    a=FQ.from_sympy(sp.expand(x)); return tuple(a.to_list())
CA=[[canon(KA[i,j]) for j in range(KA.shape[1])] for i in range(KA.shape[0])]
CB=[[canon(KB[i,j]) for j in range(KB.shape[1])] for i in range(KB.shape[0])]
print("per-factor canonical classes:", len({x for r in CA for x in r}), len({x for r in CB for x in r}), f"[{time.time()-t:.0f}s]", flush=True)
def fmul(x,y):
    return tuple((FQ.from_list(list(x))*FQ.from_list(list(y))).to_list())
nA,nB=len(EA),len(EB); n=nA*nB
vals={}
Kl=[[None]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        Kl[i][j]=vals.setdefault(fmul(CA[i//nB][j//nB],CB[i%nB][j%nB]),len(vals))
num=sorted(float(FQ.to_sympy(FQ.from_list(list(v)))) for v in vals)
print(f"{n} facets; canonical exact distinct K values: {len(vals)}; smallest gap between them in floats: {min(b-a for a,b in zip(num,num[1:])):.3e} [{time.time()-t:.0f}s]", flush=True)
row=[[i//nB==j//nB for j in range(n)] for i in range(n)]; col=[[i%nB==j%nB for j in range(n)] for i in range(n)]
def find_iso_pairs(K, init_pairs, max_nodes=20000):
    nodes=[0]
    def joint_refine(pairs):
        N=2*n; init=[]
        for i in range(N):
            mk=0
            for tt,(x,y) in enumerate(pairs):
                if i==x or i==n+y: mk=tt+1
            init.append((K[i%n][i%n],mk))
        m={}; c=[m.setdefault(x,len(m)) for x in init]
        while True:
            sig=[(c[i], tuple(sorted((K[i%n][j%n],c[j]) for j in range(N) if j!=i and (j<n)==(i<n)))) for i in range(N)]
            mm={}; new=[mm.setdefault(s,len(mm)) for s in sig]
            if len(set(new))==len(set(c)): return new
            c=new
    def rec(pairs):
        nodes[0]+=1
        if nodes[0]>max_nodes: return 'LIMIT'
        c=joint_refine(pairs); L=c[:n]; R=c[n:]
        if Counter(L)!=Counter(R): return None
        cells={}; rc={}
        for i in range(n): cells.setdefault(L[i],[]).append(i); rc.setdefault(R[i],[]).append(i)
        big=[k for k in cells if len(cells[k])>1]
        if not big:
            perm=[None]*n
            for k in cells: perm[cells[k][0]]=rc[k][0]
            return perm if all(K[perm[i]][perm[j]]==K[i][j] for i in range(n) for j in range(n)) else None
        k=min(big,key=lambda k:len(cells[k])); x=cells[k][0]
        for y in rc[k]:
            r=rec(pairs+[(x,y)])
            if r=='LIMIT': return 'LIMIT'
            if r is not None: return r
        return None
    return rec(list(init_pairs))
for name,rel in (("same-A-factor (row)",row),("same-B-factor (column)",col)):
    t=time.time(); partners=[j for j in range(1,n) if rel[0][j]]; others=[l for l in range(1,n) if not rel[0][l]]
    found=0; und=0; tried=0
    for j in partners:
        for l in others:
            if Kl[0][l]!=Kl[0][j]: continue
            tried+=1; r=find_iso_pairs(Kl,[(0,0),(j,l)])
            if r=='LIMIT': und+=1
            elif r is not None: found+=1
    print(f"{name}: tried {tried} pairs fixing facet 0: automorphisms found {found}, undecided {und} [{time.time()-t:.0f}s]", flush=True)
