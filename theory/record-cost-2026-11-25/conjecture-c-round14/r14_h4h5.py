# Round 14-M, H4 (new non-symmetric family: square x hexagon) and H5 (new three-part composites without full symmetry).
# Exact lrs/redund + rational Gram invariant + colour refinement + exhaustive pairwise search (m_round11_lib).
import sys, random, time
from fractions import Fraction as F
import m_round11_lib as L
from m_round11_lib import kron, gram_M, stable_colors, find_iso, extreme_subset, max_tensor_vertices
S=L.systems()
S['hexagon']=dict(V=[[1,1,0],[1,0,1],[1,-1,1],[1,-1,0],[1,0,-1],[1,1,-1]],
                  E=[[1,-1,0],[1,1,0],[1,0,-1],[1,0,1],[1,-1,-1],[1,1,1]], u=[1,0,0])
def P(*a): print(*a, flush=True)
def test(name, pts, prodset):
    V=extreme_subset(pts); n=len(V)
    prod=[i for i,v in enumerate(V) if tuple(v) in prodset]; ps=set(prod); ent=[i for i in range(n) if i not in ps]
    assert len(prod)==len(prodset), "product not extreme"
    if not ent: P(f"{name}: {n} extreme pts, no non-product extreme points"); return 'vacuous'
    K=gram_M(V); Kl=[[int(K[i,j]) for j in range(n)] for i in range(n)]
    col=stable_colors(Kl); pc=set(col[i] for i in prod); shared=[j for j in ent if col[j] in pc]
    if not shared:
        P(f"{name}: {n} extreme pts ({len(prod)} product, {len(ent)} other), classes {len(set(col))}: CERTIFIED (refinement separates)"); return 'cert'
    res=[]
    for j in shared:
        for p in [i for i in prod if col[i]==col[j]]:
            r=find_iso(Kl,p,j); res.append(r)
            if r not in (None,'LIMIT'):
                P(f"{name}: ENTANGLING AUTOMORPHISM FOUND {[str(x) for x in V[p]]} -> {[str(x) for x in V[j]]}"); return 'FOUND'
    st='UNDECIDED' if 'LIMIT' in res else 'CERTIFIED (exhaustive pairwise search)'
    P(f"{name}: {n} extreme pts ({len(prod)} product, {len(ent)} other), classes {len(set(col))}, shared {len(shared)}: {st}"); return st
def h4():
    A,B=S['square'],S['hexagon']
    MV=max_tensor_vertices(A,B); prodset=set(tuple(F(x) for x in kron(a,b)) for a in A['V'] for b in B['V'])
    entV=[v for v in MV if tuple(v) not in prodset]
    P(f"H4: max(square,hexagon) {len(MV)} vertices, {len(entV)} non-product")
    tally={}
    for k in (2,4,6,10):
        for seed in range(5):
            R=random.Random(14000+100*k+seed).sample(entV,k)
            r=test(f"H4 sq×hex min+{k} seed {seed}", [list(p) for p in prodset]+R, prodset); tally[r]=tally.get(r,0)+1
    # near-symmetric stress: all non-product max vertices except one (refinement has little to work with)
    for seed in range(3):
        drop=random.Random(14900+seed).randrange(len(entV)); R=[v for i,v in enumerate(entV) if i!=drop]
        r=test(f"H4 sq×hex max minus one non-product vertex (seed {seed})", [list(p) for p in prodset]+R, prodset); tally[r]=tally.get(r,0)+1
    P("H4 tally:", tally)
def h5():
    A=S['square']; MV=max_tensor_vertices(A,A); p2=set(tuple(F(x) for x in kron(a,b)) for a in A['V'] for b in A['V'])
    PR=[v for v in MV if tuple(v) not in p2]; Vs=[[F(x) for x in v] for v in A['V']]
    prod3=set(tuple(kron(kron(a,b),c)) for a in Vs for b in Vs for c in Vs)
    def place(pr,v,which):
        M=[[pr[3*i+j] for j in range(3)] for i in range(3)]
        if which=='AB': return kron(pr,v)
        if which=='BC': return kron(v,pr)
        return [M[i][k]*v[j] for i in range(3) for j in range(3) for k in range(3)]
    for pairs in (('AB',),('AB','BC')):
        pts=[list(p) for p in prod3]+[place(pr,v,w) for pr in PR for v in Vs for w in pairs]
        test(f"H5 three squares, PR on {'+'.join(pairs)} only", pts, prod3)
    # one PR box only, on AB, with every pure C
    pts=[list(p) for p in prod3]+[place(PR[0],v,'AB') for v in Vs]
    test("H5 three squares, one PR box on AB", pts, prod3)
if __name__=="__main__":
    w=sys.argv[1:] or ['h5','h4']
    if 'h5' in w: h5()
    if 'h4' in w: h4()
