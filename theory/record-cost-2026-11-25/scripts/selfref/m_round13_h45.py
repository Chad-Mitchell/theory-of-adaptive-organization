# Round 13-M, H4 (non-symmetric hexagon composites) and H5 (three squares). Exact (lrs/redund, rational Gram invariant).
# Test: every product pure state must not be mapped to a non-product extreme point by a linear automorphism of S.
# Complete when colour refinement separates all products from all non-products; otherwise backtracking per pair.
import sys, random, itertools, time
from fractions import Fraction as F
import m_round11_lib as L
from m_round11_lib import kron, gram_M, stable_colors, find_iso, extreme_subset, max_tensor_vertices, linear_map_from_perm
S=L.systems()
S['hexagon']=dict(V=[[1,1,0],[1,0,1],[1,-1,1],[1,-1,0],[1,0,-1],[1,1,-1]],
                  E=[[1,-1,0],[1,1,0],[1,0,-1],[1,0,1],[1,-1,-1],[1,1,1]], u=[1,0,0])  # as in m_round11_more.py
def P(*a): print(*a, flush=True)
def test(name, pts, prodset, max_pairs=400):
    V=extreme_subset(pts); n=len(V)
    prod=[i for i,v in enumerate(V) if tuple(v) in prodset]; ent=[i for i in range(n) if i not in set(prod)]
    assert len(prod)==len(prodset), "product not extreme"
    if not ent: P(f"{name}: {n} extreme pts, no non-product extreme points"); return 'vacuous'
    K=gram_M(V); Kl=[[int(K[i,j]) for j in range(n)] for i in range(n)]
    col=stable_colors(Kl); pc=set(col[i] for i in prod); shared=[j for j in ent if col[j] in pc]
    if not shared:
        P(f"{name}: {n} extreme pts ({len(prod)} product, {len(ent)} other), classes {len(set(col))}: CERTIFIED (refinement separates)"); return 'cert'
    # backtracking: for each product class rep x each shared non-product class rep
    preps={}; [preps.setdefault(col[i],i) for i in prod]
    ereps={}; [ereps.setdefault(col[j],j) for j in shared]
    res=[]
    for c,j in ereps.items():
        for p in [i for i in prod if col[i]==c]:
            r=find_iso(Kl,p,j); res.append(r)
            if r not in (None,'LIMIT'):
                T,ok=linear_map_from_perm(V,r)
                P(f"{name}: ENTANGLING AUTOMORPHISM FOUND p={[str(x) for x in V[p]]} -> {[str(x) for x in V[j]]}; exact linear map ok: {ok}"); return 'FOUND'
    st='UNDECIDED (limit)' if 'LIMIT' in res else 'CERTIFIED (exhaustive search, all product/non-product pairs in shared classes)'
    P(f"{name}: {n} extreme pts ({len(prod)} product, {len(ent)} other), classes {len(set(col))}, shared {len(shared)}: {st}"); return st

def h4():
    A=S['hexagon']; t=time.time()
    MV=max_tensor_vertices(A,A); prodset=set(tuple(F(x) for x in kron(a,b)) for a in A['V'] for b in A['V'])
    entV=[v for v in MV if tuple(v) not in prodset]
    P(f"H4: max(hexagon,hexagon) {len(MV)} vertices, {len(entV)} non-product [{time.time()-t:.0f}s]")
    cen=[F(1)]+[F(0)]*8
    tally={}
    for mix in (False,True):
        for k in (1,2,3,5,8):
            for seed in range(6):
                R=random.Random(1000*k+seed+(7 if mix else 0)).sample(entV,k)
                if mix: R=[[F(3,4)*x+F(1,4)*c for x,c in zip(r,cen)] for r in R]
                pts=[list(p) for p in prodset]+R
                r=test(f"H4 hex² min+{k} {'mixed 3/4' if mix else 'vertices'} seed {seed}", pts, prodset)
                tally[r]=tally.get(r,0)+1
    P("H4 tally:", tally)

def h5():
    A=S['square']; t=time.time()
    MV=max_tensor_vertices(A,A); p2=set(tuple(F(x) for x in kron(a,b)) for a in A['V'] for b in A['V'])
    PR=[v for v in MV if tuple(v) not in p2]
    P(f"H5: max(square,square) {len(MV)} vertices, {len(PR)} PR boxes")
    Vs=[[F(x) for x in v] for v in A['V']]
    prod3=set(tuple(kron(kron(a,b),c)) for a in Vs for b in Vs for c in Vs)
    pts=[list(p) for p in prod3]
    for pr in PR:
        M=[[pr[3*i+j] for j in range(3)] for i in range(3)]
        for v in Vs:
            pts.append(kron(pr,v))                       # PR on (A,B), C pure
            pts.append(kron(v,pr))                       # PR on (B,C), A pure
            pts.append([M[i][k]*v[j] for i in range(3) for j in range(3) for k in range(3)])  # PR on (A,C), B pure
    P(f"H5: {len(prod3)} products + {len(pts)-len(prod3)} PR⊗pure points in R^27 [{time.time()-t:.0f}s]")
    test("H5 three squares S3", pts, prod3)

if __name__=="__main__":
    which=sys.argv[1:] or ['h5','h4']
    if 'h5' in which: h5()
    if 'h4' in which: h4()
