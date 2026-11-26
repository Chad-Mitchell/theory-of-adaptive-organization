# Round 11-M: symmetric (repository copy runs one octahedron x octahedron sample, as the session run did before it was stopped by hand)
# Round 11-M: symmetric (local-group-invariant) intermediate composites, plus simple-invariant diagnostics
# (leverage K_ii). Repository copy: prints only (output in the .stdout file beside it).
import sys, os, random, itertools, time
sys.path.insert(0, os.path.dirname(__file__))
from m_round11_lib import *
from m_round11_lib import _out as out0
maxV={k:max_tensor_vertices(S[k[0]],S[k[1]]) for k in [('square','square'),('square','octahedron'),('octahedron','octahedron')]}
def P2(*a):
    s=" ".join(str(x) for x in a); print(s, flush=True); out0.append(s)

def sym_group(name):
    V=S[name]['V']; d=len(V[0]); G=[]
    # linear symmetries = vertex permutations preserving Gram invariant; brute force for small parts
    import sympy as sp
    Vm=sp.Matrix(V).T
    for perm in itertools.permutations(range(len(V))):
        W=sp.Matrix([V[p] for p in perm]).T
        T=W*Vm.pinv()
        if (T*Vm-W).is_zero_matrix: G.append([[F(int(x.p),int(x.q)) for x in row] for row in T.tolist()])
    return G
def apply(T,v): return [sum(T[i][k]*v[k] for k in range(len(v))) for i in range(len(T))]
def kronM(A,B):
    return [[A[i][j]*B[k][l] for j in range(len(A)) for l in range(len(B))] for i in range(len(A)) for k in range(len(B))]

GS={n:sym_group(n) for n in ['square','octahedron']}
P("=== Round 11-M continued: symmetric composites (m_round11_sym.py) ===")
P2("-- C4 local symmetry groups: square", len(GS['square']), "octahedron", len(GS['octahedron']))

def swapP(dA,dB):
    M=[[F(0)]*(dA*dB) for _ in range(dA*dB)]
    for i in range(dA):
        for j in range(dB): M[j*dA+i][i*dB+j]=F(1)
    return M

def orbit(a,b,p,sub=None):
    GA,GB=GS[a],GS[b]
    if sub: GA=GA[:sub]; GB=GB[:sub]
    pts=set()
    for ga in GA:
        for gb in GB:
            pts.add(tuple(apply(kronM(ga,gb),p)))
    if a==b:
        Sw=swapP(len(S[a]['u']),len(S[b]['u']))
        pts|=set(tuple(apply(Sw,list(q))) for q in list(pts))
    return [list(q) for q in pts]

random.seed(1111)
for (a,b,ntr) in [('square','square',12),('square','octahedron',10),('octahedron','octahedron',1)]:
    V=maxV[(a,b)]
    Ps=set(tuple(F(t) for t in kron(x,y)) for x in S[a]['V'] for y in S[b]['V'])
    E=[v for v in V if tuple(v) not in Ps]; c=center(a,b)
    for t in range(ntr):
        k=random.randint(1,3); ws=[F(random.randint(1,9)) for _ in range(k)]; tot=sum(ws)
        vs=random.sample(E,k); lam=F(random.randint(6,10),10)
        p=[lam*sum(w*v[i] for w,v in zip(ws,vs))/tot+(1-lam)*c[i] for i in range(len(c))]
        X=orbit(a,b,p)
        t0=time.time()
        Vc=extreme_subset([[F(x) for x in kron(u,w)] for u in S[a]['V'] for w in S[b]['V']]+X)
        st,found,VV,prod,ent,Kl=analyse(f"SYM {a}x{b} #{t} (seed mix of {k} max-vertices, lambda={lam}, orbit {len(X)})",S[a],S[b],Vc)
        if ent:
            lp=set(Kl[i][i] for i in prod); le=set(Kl[i][i] for i in ent)
            P2(f"   leverage separates: {lp.isdisjoint(le)}; product leverage > every entangled leverage: {min(lp)>max(le)} ; {round(time.time()-t0,1)}s")
# (repository copy: prints only; the session copy also appended this output to outputs_m.txt)
