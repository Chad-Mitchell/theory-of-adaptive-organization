"""S4. Theorem 6 (complementarity, inclusion, lattice, accretion) for GENERAL concave member costs, plus
counterexamples showing each hypothesis is needed, and a check of ARCH_EQUATION's claim about bundled reads."""
import numpy as np, itertools
rng=np.random.default_rng(4)
def subsets(M):
    for k in range(M+1):
        for S in itertools.combinations(range(M),k): yield frozenset(S)
def make_psi(kind,w,b,cap,c=1.0,Tmin=None):
    if kind=='power':   # k (w)^a R^b with optional lookup cap
        return lambda R: min((w**0.5)*(R**b) if R>0 else 0.0, cap)
def J_of(S,B,q,qu,psis,levcost,hfun):
    R=qu+(B**2)@q-sum((B[:,m]**2)*q[m] for m in S) if S else qu+(B**2)@q
    return levcost(S)+hfun(S)+sum(psis[i](max(R[i],0.0)) for i in range(len(psis)))
def check_model(B,q,qu,psis,levcost,hfun):
    M=B.shape[1]; vals={S:J_of(S,B,q,qu,psis,levcost,hfun) for S in subsets(M)}
    viol=0; tot=0
    for S in vals:
        for T_ in vals:
            if S<=T_:
                for m in range(M):
                    if m in T_: continue
                    tot+=1
                    if (vals[T_|{m}]-vals[T_])>(vals[S|{m}]-vals[S])+1e-9*(1+abs(vals[S])): viol+=1
    jmin=min(vals.values()); opts=[S for S,v in vals.items() if v<=jmin+1e-9*(1+abs(jmin))]
    U=frozenset().union(*opts); I=frozenset.intersection(*opts)
    lat_ok=(vals[U]<=jmin+1e-9*(1+abs(jmin))) and (vals[I]<=jmin+1e-9*(1+abs(jmin)))
    return viol,tot,lat_ok,opts,vals
print("=== (1) random models: heterogeneous concave member costs psi_i(R)=min(sqrt(w_i) R^b_i, cap_i), b_i in (0.1,0.95) ===")
V=T=L=0; incl_fail=0; trials=0
for t in range(300):
    N=int(rng.integers(5,40)); M=int(rng.integers(2,7))
    B=(rng.random((N,M))<rng.uniform(0.2,0.9))*rng.lognormal(0,0.5,(N,M)); q=10**rng.uniform(-3,0,M); qu=rng.lognormal(0,0.3,N)
    w=rng.lognormal(0,0.5,N); bs=rng.uniform(0.1,0.95,N); caps=np.where(rng.random(N)<0.5,np.inf,rng.uniform(0.5,3,N))
    psis=[make_psi('power',w[i],bs[i],caps[i]) for i in range(N)]
    a_lev=rng.uniform(0.2,0.9); bl=rng.uniform(0.1,0.95); h=10**rng.uniform(-2,0.5)
    Wm=(w[:,None]*B**2).sum(0)
    levcost=lambda S: sum(Wm[m]**a_lev*q[m]**bl for m in S); hfun=lambda S: h*len(S)
    v,tt,lat,opts,vals=check_model(B,q,qu,psis,levcost,hfun); V+=v; T+=tt; L+=(not lat); trials+=1
    # first-order rule with left derivatives at R(empty)
    R0=qu+(B**2)@q; keep=set()
    for m in range(M):
        dpsi=np.array([(psis[i](R0[i])-psis[i](R0[i]-1e-7*R0[i]))/(1e-7*R0[i]) for i in range(N)])
        if (dpsi*(B[:,m]**2)).sum()*q[m]-Wm[m]**a_lev*q[m]**bl>h: keep.add(m)
    if not all(keep<=set(o) for o in opts): incl_fail+=1
print(f"  submodularity violations: {V}/{T};  lattice failures: {L}/{trials};  first-order set outside an optimum: {incl_fail}/{trials}")

print("\n=== (2) accretion in upkeep h (Topkis), same model family ===")
nonmono=0; steps=0
for t in range(80):
    N=int(rng.integers(5,30)); M=int(rng.integers(2,6))
    B=(rng.random((N,M))<rng.uniform(0.2,0.9))*rng.lognormal(0,0.5,(N,M)); q=10**rng.uniform(-3,0,M); qu=rng.lognormal(0,0.3,N)
    w=rng.lognormal(0,0.5,N); bs=rng.uniform(0.1,0.95,N); caps=np.where(rng.random(N)<0.5,np.inf,rng.uniform(0.5,3,N))
    psis=[make_psi('power',w[i],bs[i],caps[i]) for i in range(N)]; Wm=(w[:,None]*B**2).sum(0)
    levcost=lambda S: sum(np.sqrt(Wm[m]*q[m]) for m in S); prev=None
    for h in np.logspace(1,-3,30):
        _,_,_,opts,_=check_model(B,q,qu,psis,levcost,lambda S: h*len(S)); mx=frozenset().union(*opts)
        if prev is not None:
            steps+=1; nonmono+=(not prev<=mx)
        prev=mx
print(f"  largest optimal set lost a level as h fell: {nonmono}/{steps} steps")

print("\n=== (3) accretion in STAKES without fallback (power class, all costs scale s^a): check ===")
nonmono=0; steps=0
for t in range(60):
    N=int(rng.integers(5,30)); M=int(rng.integers(2,6)); a=0.5
    B=(rng.random((N,M))<0.6)*rng.lognormal(0,0.5,(N,M)); q=10**rng.uniform(-3,0,M); qu=rng.lognormal(0,0.3,N); w=rng.lognormal(0,0.5,N)
    Wm=(w[:,None]*B**2).sum(0); h=0.3; prev=None
    for s in np.logspace(-1,3,25):
        psis=[(lambda R,i=i,s=s: np.sqrt(2*s*w[i]*R)) for i in range(N)]
        levcost=lambda S,s=s: sum(np.sqrt(2*s*Wm[m]*q[m]) for m in S)
        _,_,_,opts,_=check_model(B,q,qu,psis,levcost,lambda S: h*len(S)); mx=frozenset().union(*opts)
        if prev is not None:
            steps+=1; nonmono+=(not prev<=mx)
        prev=mx
print(f"  level lost as stakes rose (no fallback): {nonmono}/{steps}")

print("\n=== (4) COUNTEREXAMPLE: bounded lookup fallback breaks stakes-accretion and lookup-cost monotonicity ===")
N=100; qg=0.1; qu1=1.0; h=0.5
def onelevel(s,mu_u):
    flat=N*min(np.sqrt(2*s*(qg+qu1)),mu_u); nest=N*min(np.sqrt(2*s*qu1),mu_u)+np.sqrt(2*s*N*qg)+h
    return flat,nest
for s,muu in [(1,2.0),(4,2.0),(1,1.4),(1,9e9),(4,9e9)]:
    f,n_=onelevel(s,muu); print(f"  stakes s={s}, lookup cost mu*u={muu:g}: flat={f:.2f} level={n_:.2f} -> {'LEVEL' if n_<f else 'no level'}")
print("  => with a fallback, raising stakes (1->4) or cheapening lookup (2->1.4) DISSOLVES the level; without one it stays.")

print("\n=== (5) COUNTEREXAMPLE: convex member cost (read-rate cap + quartic loss) -> levels are substitutes ===")
def psi_capped_quartic(R,c=1.0,w=1.0,Tmin=1.0):
    # |e|^4 loss, Brownian: E e^4 = 3 (R t)^2 ; avg over [0,T] = R^2 T^2 ; cost c/T + w R^2 T^2, T>=Tmin
    Tst=(c/(2*w*R**2))**(1/3) if R>0 else np.inf
    T_=max(Tst,Tmin); return c/T_+w*R**2*T_**2
B=np.ones((20,2)); q=np.array([2.0,2.0]); qu=np.full(20,1.0)
psis=[psi_capped_quartic]*20; levcost=lambda S: sum(psi_capped_quartic(q[m],w=20.0) for m in S)
v,tt,lat,opts,vals=check_model(B,q,qu,psis,levcost,lambda S: 151.0*len(S))
print("  J:",{tuple(sorted(S)):round(x,2) for S,x in vals.items()}); print(f"  submodularity violations {v}/{tt}; lattice holds: {lat}; optima {[tuple(sorted(o)) for o in opts]}")
print("  marginal member saving of level 2: alone =",round(vals[frozenset()]-vals[frozenset({1})]+levcost({1})+151,3)," given level 1 =",round(vals[frozenset({0})]-vals[frozenset({0,1})]+levcost({1})+151,3))
print("  each level pays alone (first-order/standalone rule keeps both), but the optima are {0} or {1}: union not optimal, inclusion fails.")

print("\n=== (6) COUNTEREXAMPLE: supermodular level costs (convex span-of-control cost h|S|^2) ===")
NN=400; B=np.ones((NN,2)); q=np.array([0.05,0.05]); qu=np.full(NN,1.0)
psis=[lambda R: np.sqrt(2*R)]*NN; Wm=np.full(2,float(NN)); levcost=lambda S: sum(np.sqrt(2*Wm[m]*q[m]) for m in S)
_,_,_,_,v0=check_model(B,q,qu,psis,levcost,lambda S: 0.0)
s1=v0[frozenset()]-v0[frozenset({0})]; s12=v0[frozenset({0})]-v0[frozenset({0,1})]
kap=(s1+s12/3)/2 if s12<3*s1 else None
kap=0.5*(s12/3+s1)   # cost k|S|^2: alone pays iff s1>k ; second pays iff s12>3k  -> choose s12/3<k<s1
print(f"  net savings without span cost: first level {s1:.3f}, second given first {s12:.3f}; choose k={kap:.3f} in (s12/3, s1)")
v,tt,lat,opts,vals=check_model(B,q,qu,psis,levcost,lambda S: kap*len(S)**2)
print("  J:",{tuple(sorted(S)):round(x,4) for S,x in vals.items()}); print(f"  submodularity violations {v}/{tt}; lattice holds: {lat}; optima {[tuple(sorted(o)) for o in opts]}")

print("\n=== (7) ARCH_EQUATION claim check: an indivisible bundled level (one read returns all sources in S) ===")
V=T=L=0; incl=0; trials=0
for t in range(200):
    N=int(rng.integers(5,40)); M=int(rng.integers(2,7))
    B=(rng.random((N,M))<rng.uniform(0.2,0.9))*rng.lognormal(0,0.5,(N,M)); q=10**rng.uniform(-3,0,M); qu=rng.lognormal(0,0.3,N); w=rng.lognormal(0,0.5,N)
    Wm=(w[:,None]*B**2).sum(0); h=10**rng.uniform(-2,0.5)
    psis=[(lambda R,i=i: np.sqrt(2*w[i]*R)) for i in range(N)]
    levcost=lambda S: np.sqrt(2*sum(Wm[m]*q[m] for m in S)) if S else 0.0   # one read, one interval for all of S
    v,tt,lat,opts,vals=check_model(B,q,qu,psis,levcost,lambda S: h*(len(S)>0)); V+=v; T+=tt; L+=(not lat); trials+=1
print(f"  submodularity violations: {V}/{T}; lattice failures: {L}/{trials}  (ARCH said J 'is then no longer submodular')")
