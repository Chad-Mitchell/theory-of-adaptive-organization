# Round 13-M, H3: direct automorphism search on max(I,D) through its facets (no vertex enumeration needed).
# Facets of max(A,B) = extreme rays of min(A*,B*) = products e_i (x) f_j of facet effects (KNOWN). A linear automorphism of
# max permutes these 240 facets and preserves K_ij = f_i^T (sum f f^T)^-1 f_j (Bremner et al. 2014, dual form).
# If "same A-factor" and "same B-factor" are unions of K-value classes (and colour refinement keeps them), every
# automorphism is sigma x tau on the facet grid, hence T = T_A (x) T_B (uniform weights: sum_j f_j = 12 u_B), local:
# no entangling automorphism. Float with an explicit gap check.
import numpy as np, itertools
from m_round12_parts import PARTS
EA=np.array(PARTS['I']()); EB=np.array(PARTS['D']())
print("facet effects: I", len(EA), " D", len(EB), "; sum of D facet effects =", np.round(EB.sum(0),12), "; sum of I facet effects =", np.round(EA.sum(0),12))
Fs=np.array([np.kron(e,f) for e in EA for f in EB]); n=len(Fs)
K=Fs@np.linalg.inv(Fs.T@Fs)@Fs.T
vals=np.sort(np.unique(np.round(K,9)))
gaps=np.diff(np.sort(K.flatten())); 
cls=np.round(K,9)
print(f"{n} facets; distinct K values (rounded 1e-9): {len(vals)}; smallest nonzero gap between raw K values: {gaps[gaps>1e-12].min():.3e}; max deviation within a rounded class: {np.abs(K-cls).max():.1e}")
row=np.array([[i//len(EB)==j//len(EB) for j in range(n)] for i in range(n)])
col=np.array([[i%len(EB)==j%len(EB) for j in range(n)] for i in range(n)])
def union_of_classes(rel):
    inside=set(cls[rel].tolist()); outside=set(cls[~rel].tolist())
    return inside.isdisjoint(outside), sorted(inside)
okA,vA=union_of_classes(row & ~np.eye(n,dtype=bool)); okB,vB=union_of_classes(col & ~np.eye(n,dtype=bool))
print("same-A-factor pairs use K values disjoint from all other pairs:", okA, " values:", vA[:6])
print("same-B-factor pairs use K values disjoint from all other pairs:", okB, " values:", vB[:6])
if okA and okB:
    print("=> every linear automorphism of max(I,D) acts on facets as sigma x tau, so T = T_A (x) T_B: no entangling automorphism (H3 HIT)")
else:
    print("=> K values alone do not force the grid structure; refinement / search needed")

# ---- refinement search: can an automorphism fixing facet 0 send a same-row (same-column) partner of 0 to a facet that is
# not a same-row (same-column) partner? Facets 0..239 form one orbit under the local group (transitive on both factors),
# so fixing facet 0 loses no generality. Individualisation-refinement + backtracking (copy of m_round11_lib.find_iso, with
# several initial pairs).
from collections import Counter
ids={v:k for k,v in enumerate(sorted(set(cls.flatten().tolist())))}
Kl=[[ids[cls[i,j]] for j in range(n)] for i in range(n)]
def find_iso_pairs(K, init_pairs, max_nodes=20000):
    n=len(K); nodes=[0]
    def joint_refine(pairs):
        N=2*n
        init=[]
        for i in range(N):
            mk=0
            for t,(x,y) in enumerate(pairs):
                if i==x or i==n+y: mk=t+1
            init.append((K[i%n][i%n],mk))
        m={}; col=[m.setdefault(x,len(m)) for x in init]
        while True:
            sig=[(col[i], tuple(sorted((K[i%n][j%n],col[j]) for j in range(N) if j!=i and (j<n)==(i<n)))) for i in range(N)]
            mm={}; new=[mm.setdefault(s,len(mm)) for s in sig]
            if len(set(new))==len(set(col)): return new
            col=new
    def rec(pairs):
        nodes[0]+=1
        if nodes[0]>max_nodes: return 'LIMIT'
        col=joint_refine(pairs); L=col[:n]; R=col[n:]
        if Counter(L)!=Counter(R): return None
        cells={}; rcells={}
        for i in range(n): cells.setdefault(L[i],[]).append(i); rcells.setdefault(R[i],[]).append(i)
        big=[c for c in cells if len(cells[c])>1]
        if not big:
            perm=[None]*n
            for c in cells: perm[cells[c][0]]=rcells[c][0]
            return perm if all(K[perm[i]][perm[j]]==K[i][j] for i in range(n) for j in range(n)) else None
        c=min(big,key=lambda c:len(cells[c])); x=cells[c][0]
        for y in rcells[c]:
            r=rec(pairs+[(x,y)])
            if r=='LIMIT': return 'LIMIT'
            if r is not None: return r
        return None
    return rec(list(init_pairs))
import time
for name,rel in (("same-A-factor (row)",row),("same-B-factor (column)",col)):
    t=time.time()
    partners=[j for j in range(1,n) if rel[0,j]]; others=[l for l in range(1,n) if not rel[0,l]]
    # candidates: only pairs with equal K to facet 0 can be swapped
    bad=[]; undecided=0; tried=0
    for j in partners:   # every partner (not one per K value: equal K does not mean same stabiliser orbit)
        kv=Kl[0][j]
        for l in others:
            if Kl[0][l]!=kv: continue
            tried+=1
            r=find_iso_pairs(Kl,[(0,0),(j,l)])
            if r=='LIMIT': undecided+=1
            elif r is not None: bad.append((j,l)); break
        if bad: break
    print(f"{name}: tried {tried} (partner-class rep -> non-partner) pairs fixing facet 0: automorphisms found {len(bad)}, undecided {undecided} [{time.time()-t:.0f}s]", flush=True)
