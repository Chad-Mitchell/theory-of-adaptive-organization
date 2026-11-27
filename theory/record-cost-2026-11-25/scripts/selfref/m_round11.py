# Round 11-M main: Conjecture C tests. Repository copy: output in m_round11.stdout.
import sys, os, random, itertools, time
sys.path.insert(0, os.path.dirname(__file__))
from m_round11_lib import *
out=[]
def P(*a):
    s=" ".join(str(x) for x in a); print(s, flush=True); out.append(s)
S=systems()

def analyse(name, A, B, V, check_linear=True):
    P_=[tuple(F(t) for t in kron(x,y)) for x in A['V'] for y in B['V']]
    Ps=set(P_)
    prod=[i for i,v in enumerate(V) if tuple(v) in Ps]
    ent=[i for i,v in enumerate(V) if tuple(v) not in Ps]
    assert len(prod)==len(P_), "a product pure state is not extreme?!"
    K=gram_M(V); n=len(V); Kl=[[int(K[i,j]) for j in range(n)] for i in range(n)]
    col=stable_colors(Kl)
    pc=set(col[i] for i in prod); shared=[j for j in ent if col[j] in pc]
    status=""
    found=None
    if not ent: status="no entangled extreme points (C vacuous)"
    elif not shared: status="CERTIFIED: colour refinement separates product from entangled vertices -> no entangling automorphism"
    else:
        # one representative per colour class among shared
        reps={}
        for j in shared: reps.setdefault(col[j], j)
        res=[]
        for c,j in reps.items():
            r=find_iso(Kl, prod[0], j)
            res.append(r)
            if r not in (None,'LIMIT'): found=(prod[0],j,r); break
        if found: status="ENTANGLING AUTOMORPHISM FOUND"
        elif 'LIMIT' in res: status="UNDECIDED (search limit)"
        else: status="CERTIFIED by exhaustive individualisation search (classes shared but no automorphism)"
        # caveat: find_iso maps prod[0]; products form one orbit under local symmetries when parts are transitive
    P(f"{name}: extreme pts {n} (product {len(prod)}, entangled {len(ent)}), stable classes {len(set(col))}, entangled sharing a product class {len(shared)} -> {status}")
    if found:
        T,ok=linear_map_from_perm(V,found[2])
        P("   exact linear map reproduces the permutation on all extreme points:", ok, "; maps", [str(x) for x in V[found[0]]], "->", [str(x) for x in V[found[1]]])
    return status, found, V, prod, ent, Kl

P("=== Round 11-M (2026-11-26) ===")
t0=time.time()
P("-- C1 maximal tensor products (exact lrs) and minimal tensor products")
maxV={}
for a,b in [('triangle','triangle'),('triangle','square'),('triangle','octahedron'),('square','square'),('square','octahedron'),('octahedron','octahedron')]:
    V=max_tensor_vertices(S[a],S[b]); maxV[(a,b)]=V
    analyse(f"max {a}x{b}", S[a],S[b],V)
    Vmin=[[F(t) for t in kron(x,y)] for x in S[a]['V'] for y in S[b]['V']]
    analyse(f"min {a}x{b}", S[a],S[b],Vmin)
P("elapsed", round(time.time()-t0,1),"s")

# sanity: classical parts admit non-trivial (non-local) reversible maps: CNOT-like permutation of triangle x triangle vertices
A=S['triangle']; V=[[F(t) for t in kron(x,y)] for x in A['V'] for y in A['V']]
perm=[ (3*i + ((j+i)%3)) for i in range(3) for j in range(3)]   # controlled shift: (i,j)->(i,j+i)
T,ok=linear_map_from_perm(V,perm)
P("C1 sanity triangle x triangle: controlled shift (i,j)->(i,j+i) is an exact linear automorphism:", ok, "(non-local, correlating, not entangling: no entangled states exist)")

def gen_intermediate(a,b, X):
    A,B=S[a],S[b]
    pts=[[F(t) for t in kron(x,y)] for x in A['V'] for y in B['V']]+X
    return extreme_subset(pts)

def center(a,b):
    A,B=S[a],S[b]
    ca=[sum(F(v[k]) for v in A['V'])/len(A['V']) for k in range(len(A['u']))]
    cb=[sum(F(v[k]) for v in B['V'])/len(B['V']) for k in range(len(B['u']))]
    return kron(ca,cb)

summary={}
def run_family(label,a,b,X):
    V=gen_intermediate(a,b,X)
    st,found,_,_,_,_=analyse(label,S[a],S[b],V)
    summary.setdefault(st[:12],0); summary[st[:12]]+=1
    return st

P("-- C2 square x square intermediate composites")
V=maxV[('square','square')]
Ps=set(tuple(F(t) for t in kron(x,y)) for x in S['square']['V'] for y in S['square']['V'])
PR=[v for v in V if tuple(v) not in Ps]
c=center('square','square')
# (a) min + every subset of the 8 PR boxes (255 non-empty subsets)
cnt=0
for r in range(1,9):
    for sub in itertools.combinations(range(8),r):
        run_family(f"sq min+PR{list(sub)}", 'square','square',[PR[k] for k in sub]); cnt+=1
# (b) noisy PR boxes (isotropic) at lambda, all 8 and single
for lam in [F(3,5),F(2,3),F(3,4),F(9,10)]:
    X=[[lam*x+(1-lam)*y for x,y in zip(v,c)] for v in PR]
    run_family(f"sq min+all PR at lambda={lam}", 'square','square',X)
    run_family(f"sq min+PR0 at lambda={lam}", 'square','square',X[:1])
    run_family(f"sq min+PR0,PR1 at lambda={lam},1", 'square','square',[X[0],PR[1]])

P("-- C3 octahedron x octahedron and square x octahedron intermediate composites (orbit-structured + random)")
for (a,b) in [('square','octahedron'),('octahedron','octahedron')]:
    V=maxV[(a,b)]
    Ps=set(tuple(F(t) for t in kron(x,y)) for x in S[a]['V'] for y in S[b]['V'])
    E=[v for v in V if tuple(v) not in Ps]
    c=center(a,b)
    # group entangled max-vertices by stable colour class in the max composite
    K=gram_M(V); n=len(V); Kl=[[int(K[i,j]) for j in range(n)] for i in range(n)]
    col=stable_colors(Kl)
    classes={}
    for i,v in enumerate(V):
        if tuple(v) not in Ps: classes.setdefault(col[i],[]).append(v)
    P(f"{a}x{b}: entangled max vertices fall in {len(classes)} refinement classes of sizes {sorted(len(x) for x in classes.values())}")
    for ci,(cc,Xs) in enumerate(sorted(classes.items(), key=lambda t:len(t[1]))):
        run_family(f"{a}x{b} min+class{ci}(size {len(Xs)})",a,b,Xs)
        for lam in [F(1,2),F(3,4)]:
            Xn=[[lam*x+(1-lam)*y for x,y in zip(v,c)] for v in Xs]
            run_family(f"{a}x{b} min+class{ci} at lambda={lam}",a,b,Xn)
    random.seed(11)
    ntrial = 40 if a=='square' else 25
    for t in range(ntrial):
        k=random.randint(1,6)
        Xs=random.sample(E,k)
        # random mixtures of entangled vertices with weights, plus noise
        X=[]
        for v in Xs:
            w=random.sample(E,2); lam=F(random.randint(5,10),10); mu=F(random.randint(0,4),10)
            p=[lam*x+(1-lam)*((1-mu)*y+mu*z) for x,y,z in zip(v,w[0],w[1])]
            X.append(p)
        run_family(f"{a}x{b} random#{t} k={k}",a,b,X)
P("summary of intermediate-composite outcomes:", summary)
P("elapsed", round(time.time()-t0,1),"s")
# (repository copy: prints only; the session copy also appended this output to outputs_m.txt)
