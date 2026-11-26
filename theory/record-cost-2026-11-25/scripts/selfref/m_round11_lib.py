# Round 11-M library: exact polytope composites of GPT parts (lrs/redund, rational arithmetic), Gram-matrix
# linear-automorphism test (Bremner-Dutour Sikiric-Schurmann criterion), entangling-map search.
import subprocess, tempfile, itertools, os
from fractions import Fraction as F
import numpy as np, networkx as nx
from networkx.algorithms import isomorphism as iso
import sympy as sp

def systems():
    S={}
    S['triangle']=dict(V=[[1,0,0],[0,1,0],[0,0,1]], E=[[1,0,0],[0,1,0],[0,0,1]], u=[1,1,1])
    S['square']=dict(V=[[1,a,b] for a in (1,-1) for b in (1,-1)], E=[[1,-1,0],[1,1,0],[1,0,-1],[1,0,1]], u=[1,0,0])
    S['octahedron']=dict(V=[[1]+[s if k==i else 0 for k in range(3)] for i in range(3) for s in (1,-1)],
                         E=[[1]+list(b) for b in itertools.product((1,-1),repeat=3)], u=[1,0,0,0])
    return S

def kron(a,b): return [x*y for x in a for y in b]

def fmt(x): return str(F(x))
def lrs_run(text, prog='lrs'):
    with tempfile.NamedTemporaryFile('w',suffix='.ine',delete=False) as f: f.write(text); fn=f.name
    out=subprocess.run([prog,fn],capture_output=True,text=True,timeout=3000).stdout
    os.unlink(fn); return out

def max_tensor_vertices(A,B):
    D=len(A['u'])*len(B['u']); rows=[]
    rows.append(['-1']+[fmt(x) for x in kron(A['u'],B['u'])])
    for e in A['E']:
        for f in B['E']: rows.append(['0']+[fmt(x) for x in kron(e,f)])
    txt="H-representation\nlinearity 1 1\nbegin\n%d %d rational\n"%(len(rows),D+1)+"\n".join(" ".join(r) for r in rows)+"\nend\n"
    out=lrs_run(txt); V=[]
    inb=False
    for line in out.splitlines():
        t=line.split()
        if line.strip()=='begin': inb=True; continue
        if line.strip()=='end': inb=False; continue
        if inb and t and t[0]=='1': V.append([F(x) for x in t[1:]])
    return V

def extreme_subset(points):
    # exact: redund on V-representation
    D=len(points[0])
    txt="V-representation\nbegin\n%d %d rational\n"%(len(points),D+1)+"\n".join("1 "+" ".join(fmt(x) for x in p) for p in points)+"\nend\n"
    out=lrs_run(txt,'redund'); V=[]; inb=False
    for line in out.splitlines():
        t=line.split()
        if line.strip()=='begin': inb=True; continue
        if line.strip()=='end': inb=False; continue
        if inb and t and t[0]=='1': V.append([F(x) for x in t[1:]])
    return V

def gram_M(V):
    # exact integer Gram invariant: K_ij = vint_i^T adj(G) vint_j, proportional (common positive factor) to v_i^T (sum v v^T)^-1 v_j
    from math import lcm
    L=1
    for v in V:
        for x in v: L=lcm(L,x.denominator)
    Vi=[[int(x*L) for x in v] for v in V]
    G=sp.Matrix(Vi).T*sp.Matrix(Vi)
    A=G.adjugate(); d=G.det()
    assert d!=0
    if d<0: A=-A
    Vo=np.array(Vi,dtype=object); Ao=np.array(A.tolist(),dtype=object)
    K=Vo.dot(Ao).dot(Vo.T)
    return K

def automorphism_test(V, prod_idx, ent_idx, timeout_pairs=None):
    """Return dict: row-invariant classes, and for each entangled orbit candidate whether an automorphism maps prod->ent."""
    M=gram_M(V); n=len(V)
    keys=[[int(M[i,j]) for j in range(n)] for i in range(n)]
    rowinv=[(keys[i][i], tuple(sorted(keys[i]))) for i in range(n)]
    pinv=set(rowinv[i] for i in prod_idx)
    cand=[j for j in ent_idx if rowinv[j] in pinv]
    res={'n':n,'n_prod':len(prod_idx),'n_ent':len(ent_idx),'ent_sharing_prod_rowinv':len(cand),'entangling_found':[]}
    if cand:
        G=nx.Graph()
        for i in range(n): G.add_node(i,c=rowinv[i])
        for i in range(n):
            for j in range(i+1,n): G.add_edge(i,j,w=keys[i][j])
        p0=prod_idx[0]
        for j in cand:
            G1=G.copy(); G2=G.copy()
            G1.nodes[p0]['c']=('MARK',); G2.nodes[j]['c']=('MARK',)
            GM=iso.GraphMatcher(G1,G2,node_match=lambda a,b:a['c']==b['c'],edge_match=lambda a,b:a['w']==b['w'])
            if GM.is_isomorphic(): res['entangling_found'].append((p0,j,dict(GM.mapping)))
    return res, M, rowinv

def automorphism_group_order(V, rowinv, M, limit=200000):
    n=len(V); keys=[[int(M[i,j]) for j in range(n)] for i in range(n)]
    G=nx.Graph()
    for i in range(n): G.add_node(i,c=rowinv[i])
    for i in range(n):
        for j in range(i+1,n): G.add_edge(i,j,w=keys[i][j])
    GM=iso.GraphMatcher(G,G,node_match=lambda a,b:a['c']==b['c'],edge_match=lambda a,b:a['w']==b['w'])
    c=0
    for _ in GM.isomorphisms_iter():
        c+=1
        if c>=limit: break
    return c

def linear_map_from_perm(V, perm):
    # exact T with T v_i = v_perm(i); verify on all vertices
    Vm=sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in v] for v in V]).T
    Wm=sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in V[perm[i]]] for i in range(len(V))]).T
    T=Wm*Vm.pinv()
    ok = (T*Vm - Wm).is_zero_matrix
    return T, ok

# ---- colour refinement (1-WL) on the edge-coloured complete graph K; exact certificate of non-equivalence ----
def refine(K, init):
    n=len(init); col=list(init)
    while True:
        sig=[(col[i], tuple(sorted((K[i][j], col[j]) for j in range(n) if j!=i))) for i in range(n)]
        m={}; new=[m.setdefault(s,len(m)) for s in sig]
        # canonical relabel keeps classes comparable only within one run; count classes
        if len(set(new))==len(set(col)): return new
        col=new

def stable_colors(K):
    n=len(K); m={}
    init=[m.setdefault(K[i][i],len(m)) for i in range(n)]
    return refine(K, init)

def find_iso(K, a, b, max_nodes=200000):
    """Search an automorphism sigma (K[s(i)][s(j)]==K[i][j]) with sigma(a)=b. Individualisation-refinement + backtracking.
    Returns perm list or None (exhaustive if returns None without hitting max_nodes; flag in second value)."""
    n=len(K); nodes=[0]
    def joint_refine(pairs):
        # refine the disjoint union so colours are comparable between the two copies
        N=2*n
        def KK(i,j):
            if (i<n)!=(j<n): return ('X',)
            return K[i%n][j%n]
        init=[]
        for i in range(N):
            mk=0
            for t,(x,y) in enumerate(pairs):
                if i==x or i==n+y: mk=t+1
            init.append((K[i%n][i%n],mk))
        m={}; col=[m.setdefault(x,len(m)) for x in init]
        while True:
            sig=[(col[i], tuple(sorted((KK(i,j),col[j]) for j in range(N) if j!=i and (j<n)==(i<n)))) for i in range(N)]
            mm={}; new=[mm.setdefault(s,len(mm)) for s in sig]
            if len(set(new))==len(set(col)): return new
            col=new
    def rec(pairs):
        nodes[0]+=1
        if nodes[0]>max_nodes: return 'LIMIT'
        col=joint_refine(pairs)
        L=col[:n]; R=col[n:]
        from collections import Counter
        if Counter(L)!=Counter(R): return None
        cells={}
        for i in range(n): cells.setdefault(L[i],[]).append(i)
        rcells={}
        for i in range(n): rcells.setdefault(R[i],[]).append(i)
        big=[c for c in cells if len(cells[c])>1]
        if not big:
            perm=[None]*n
            for c in cells: perm[cells[c][0]]=rcells[c][0]
            ok=all(K[perm[i]][perm[j]]==K[i][j] for i in range(n) for j in range(n))
            return perm if ok else None
        c=min(big,key=lambda c:len(cells[c])); x=cells[c][0]
        for y in rcells[c]:
            r=rec(pairs+[(x,y)])
            if r=='LIMIT': return 'LIMIT'
            if r is not None: return r
        return None
    r=rec([(a,b)])
    return r


# ---- shared analysis (same code as m_round11.py analyse) ----
_out=[]
def P(*a):
    s=" ".join(str(x) for x in a); print(s, flush=True); _out.append(s)
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


def center(a,b):
    A,B=S[a],S[b]
    ca=[sum(F(v[k]) for v in A['V'])/len(A['V']) for k in range(len(A['u']))]
    cb=[sum(F(v[k]) for v in B['V'])/len(B['V']) for k in range(len(B['u']))]
    return kron(ca,cb)
