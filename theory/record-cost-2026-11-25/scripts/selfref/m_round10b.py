# Round 10b-M (routes to U: inflow, composition, cost). Repository copy: output in m_round10b.stdout.
# Pure numerics/toys. No physics constants. Labels in NOTE.md.
import numpy as np, itertools, math
from scipy.optimize import linprog, minimize
np.set_printoptions(precision=6, suppress=True)
out=[]
def P(*a):
    s=" ".join(str(x) for x in a); print(s); out.append(s)

P("=== Round 10b-M (2026-11-25, written 23:50 EST) ===")
# ---------------- Route 1: inflow + finite capacity ----------------
P("-- M1 inflow + finite capacity")
# M1a closed finite-dim world: element of infinite order => closure of <g> is an infinite compact abelian Lie group => contains a circle.
# illustrate: rotation by irrational angle a; orbit of a point gets eps-dense on the circle (no return).
a=2*math.pi*(math.sqrt(2)-1); pts=np.mod(np.arange(1,20001)*a,2*math.pi)
gap=np.max(np.diff(np.sort(np.concatenate([[0],pts,[2*math.pi]]))))
P("M1a irrational rotation, 20000 steps: min return distance", round(float(np.min(np.abs(np.angle(np.exp(1j*pts))))),8), "max gap on circle", round(float(gap),6))
# finite group: every orbit periodic with period dividing |G| (octahedral rotation group, order 24)
def rotgroup_oct():
    G=[]
    for perm in itertools.permutations(range(3)):
        for s in itertools.product([1,-1],repeat=3):
            M=np.zeros((3,3))
            for i,j in enumerate(perm): M[i,j]=s[i]
            if np.linalg.det(M)>0: G.append(M)
    return G
G=rotgroup_oct(); ords=[]
for g in G:
    k=1; M=g.copy()
    while not np.allclose(M,np.eye(3)): M=M@g; k+=1
    ords.append(k)
P("M1a octahedral rotation group: order", len(G), "element orders", sorted(set(ords)), "-> every orbit returns within 4 steps")
# M1b infinite world of finite cells: shift on Thue-Morse configuration; cell 0 sees an aperiodic stream forever; local group S2.
tm=[bin(i).count("1")%2 for i in range(4096)]
def has_period(seq,p): return all(seq[i]==seq[i+p] for i in range(len(seq)-p))
per=[p for p in range(1,1025) if has_period(tm[:4096],p)]
P("M1b Thue-Morse stream seen by cell 0 under the shift: periods <=1024 found:", per, "(none => aperiodic inflow); cell group S2 (order 2)")
# M1c inflow price: absorb a fresh bit per tick into a capacity-1 cell. Option A swap-out (reversible, zero erasure) exists in both
# worlds (SWAP is a permutation / a Clifford). Option B overwrite: Landauer cost = H(stored bit) bits per tick, same number for
# a classical bit and a qubit holding the same classical record.
for p in [0.5,0.1]:
    H=-(p*math.log2(p)+(1-p)*math.log2(1-p))
    rho=np.diag([1-p,p]); S=-sum(l*math.log2(l) for l in np.linalg.eigvalsh(rho) if l>1e-15)
    P(f"M1c overwrite cost per tick, record bias p={p}: classical H={H:.6f} bits, qubit S={S:.6f} bits; swap-out cost 0 in both")
# law-memory (round 9): finite group needs log2|G| bits; continuous group at precision eps needs ~dim*log2(1/eps)
for eps in [1e-2,1e-4]:
    P(f"M1c law memory eps={eps}: octahedral log2(24)={math.log2(24):.3f} bits; SO(3) ~3*log2(1/eps)={3*math.log2(1/eps):.2f} bits")

# ---------------- Route 2: composition ----------------
P("-- M2 composition")
I=np.eye(2); X=np.array([[0,1],[1,0]]); Y=np.array([[0,-1j],[1j,0]]); Z=np.diag([1,-1])
paulis=[I,X,Y,Z]
def kron(*ms):
    r=np.array([[1]])
    for m in ms: r=np.kron(r,m)
    return r
# stabilizer states for n=1,2,3 via orbit of |0..0> under Clifford generators (H,S,CNOT); collect projectors
Hd=np.array([[1,1],[1,-1]])/math.sqrt(2); Sg=np.diag([1,1j])
def gens(n):
    g=[]
    for q in range(n):
        for u in [Hd,Sg]:
            g.append(kron(*[u if k==q else I for k in range(n)]))
    for c in range(n):
        for t in range(n):
            if c!=t:
                d=2**n; M=np.zeros((d,d))
                for b in range(d):
                    bits=[(b>>(n-1-k))&1 for k in range(n)]
                    if bits[c]: bits[t]^=1
                    M[sum(bt<<(n-1-k) for k,bt in enumerate(bits)),b]=1
                g.append(M)
    return g
def stab_states(n):
    d=2**n; v=np.zeros(d,complex); v[0]=1
    seen={}; frontier=[v]
    def key(v):
        i=np.argmax(np.abs(v)>1e-9); w=v*np.conj(v[i])/abs(v[i]); return tuple(np.round(w,6))
    seen[key(v)]=v
    gs=gens(n)
    while frontier:
        nf=[]
        for s in frontier:
            for g in gs:
                w=g@s; k=key(w)
                if k not in seen: seen[k]=w; nf.append(w)
        frontier=nf
    return list(seen.values())
for n in [1,2,3]:
    St=stab_states(n); d=2**n
    vecs=[np.real(np.concatenate([[1],[np.trace(kron(*pp)@np.outer(s,s.conj())) for pp in itertools.product(paulis,repeat=n)][1:]])) for s in St]
    affdim=np.linalg.matrix_rank(np.array(vecs)[:,1:]-np.array(vecs)[0,1:],tol=1e-8)
    P(f"M2a stabilizer n={n}: pure states {len(St)}, affine dim {affdim} (= 4^n-1 = {4**n-1}), capacity >= {d} (computational basis), <= {d} (subset of QM)")
# M2b: no-restriction octahedron (effects = full dual: e(r)=1/2+b.r/2, b in {-1,1}^3, plus 0,1) cannot host the Bell stabilizer state.
bell=np.array([1,0,0,1])/math.sqrt(2); rho=np.outer(bell,bell)
T=np.array([[np.real(np.trace(kron(paulis[i],paulis[j])@rho)) for j in range(1,4)] for i in range(1,4)])
mn=min(0.25+0.25*np.array(b)@T@np.array(c) for b in itertools.product([1,-1],repeat=3) for c in itertools.product([1,-1],repeat=3))
P("M2b Bell correlation matrix diag", np.diag(T), "; min over product effects of full-dual octahedra:", mn, "(<0 => not a valid state; stabilizer entanglement needs restricted effects)")
# M2c: Hardy-type cost: K = N^r; cheapest r consistent with composites (K_AB=K_A K_B, N_AB=N_A N_B) is r=1 (classical).
for N in [2,3,4]:
    P(f"M2c N={N}: dimension K classical r=1: {N}, r=2 (QM or stabilizer): {N**2}")

# ---------------- Route 3: the cost J ----------------
P("-- M3 cost J: gentle transport of one record to its distinguishable partner in T ticks (closed world)")
def poly_dist(n,a,b):
    V=np.array([[1,math.cos(2*math.pi*k/n),math.sin(2*math.pi*k/n)] for k in range(n)])
    c=-(np.array(a)-np.array(b))
    A=np.vstack([V,-V]); ub=np.concatenate([np.ones(n),np.zeros(n)])
    r=linprog(c,A_ub=A,b_ub=ub,bounds=[(None,None)]*3,method="highs"); return -r.fun
def vert(n,k): return [1,math.cos(2*math.pi*k/n),math.sin(2*math.pi*k/n)]
# disk: operational distance between pure states at angle phi = sin(phi/2)
P("M3a check disk op distance via LP on 2000-gon approx, phi=pi/3:", round(poly_dist(2000,vert(2000,0),vert(2000,1000//3*1)) ,6), "vs sin(pi/6)=0.5 (approx 333/2000 turn)")
def disk_opt(T):
    # min sum sin^2(phi_t/2), sum phi_t = pi, phi_t in [0,pi]
    best=1e9
    for trial in range(30):
        x0=np.random.dirichlet(np.ones(T))*math.pi
        cons=({'type':'eq','fun':lambda x: np.sum(x)-math.pi},)
        r=minimize(lambda x: np.sum(np.sin(x/2)**2), x0, bounds=[(0,math.pi)]*T, constraints=cons, method="SLSQP")
        best=min(best,r.fun)
    return best
np.random.seed(0)
for T in [1,2,3,4,6,10]:
    P(f"M3b disk T={T}: optimum {disk_opt(T):.6f}, equal steps T*sin^2(pi/2T)={T*math.sin(math.pi/(2*T))**2:.6f}")
def poly_opt(n,T):
    # shortest path from vertex 0 to vertex n/2 with exactly <=T steps; step k->j allowed (group transitive & dihedral: any vertex reachable in one step); cost d^2
    D=[[poly_dist(n,vert(n,0),vert(n,j))**2 for j in range(n)]]
    dj=D[0]; INF=1e9; best=[INF]*n; best[0]=0
    for t in range(T):
        nb=best[:]
        for i in range(n):
            if best[i]<INF:
                for j in range(n):
                    nb[j]=min(nb[j],best[i]+dj[(j-i)%n])
        best=nb
    return best[n//2], dj
for T in [2,3,4,5]:
    disk=T*math.sin(math.pi/(2*T))**2
    rows=[]
    for n in [4,6,8,12,16,20,24]:
        c,_=poly_opt(n,T); rows.append(f"{n}:{c:.6f}")
    P(f"M3c T={T} disk={disk:.6f} | n-gon optimum (all effects): "+" ".join(rows))
# linear pricing: cost sum d_t
P("M3d linear pricing (sum d_t): classical bit jump = 1; disk equal steps T*sin(pi/2T):", [round(T*math.sin(math.pi/(2*T)),4) for T in [1,2,4,10,100]], "-> classical bit wins under linear pricing")
# M3e decision window with dimension price kappa (per affine dim) and disturbance price c=1
for T in [5,10,100]:
    disk=T*math.sin(math.pi/(2*T))**2
    lo=disk/1.0; hi=1-disk
    P(f"M3e T={T}: disk J=2k+{disk:.4f}; classical bit J=k+1; any D>=3 world J>=3k. disk beats bit iff k<{hi:.4f}; beats every D>=3 world iff k>{disk:.4f}; 4T-gon ties disk (see M3c)")
# M3f finite single-shot tasks: 2->1 random access code
P("M3f 2->1 RAC success: square (gbit, dim 2) 1.0; disk/ball 0.853553 (=(1+1/sqrt2)/2); classical bit 0.75 (KNOWN values)")
# (repository copy: prints only; the session copy also appended this output to outputs_m.txt)
