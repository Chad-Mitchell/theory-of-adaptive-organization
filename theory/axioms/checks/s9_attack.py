"""S9. Checks prompted by the adversarial pass (FIXES.md):
(1) mixed technologies: level in P(aL,bL), members in P(am,bm). Claim: e_g -> -(1-bL)/(1-aL) (LEVEL's class), e_u -> (1-bm)/(1-aL).
(2) complementarity needs members to track their residual as ONE bundle: with separately read components (member clocks)
    savings are modular, J is modular, levels are independent (no complementarity, no avalanche).
(3) T7 ordering with heterogeneous concave member costs (same residual, different psi_i)."""
import numpy as np, itertools
from scipy.optimize import brentq
def Nstar(qg,qu,aL,bL,am,bm,h=0.0,w=1.0):
    G=lambda n: n*w**am*((qg+qu)**bm-qu**bm)-((n*w)**aL*qg**bL+h)
    lo,hi=1.0,2.0
    while G(hi)<=0: lo=hi; hi*=2
    return brentq(G,lo,hi,xtol=1e-12*hi)
print("=== (1) mixed technologies, h=0, qu=1, slopes at rho 1e-6 -> 2e-6 and qu slope ===")
for (aL,bL,am,bm) in [(0.5,0.5,2/3,1/3),(2/3,1/3,0.5,0.5),(0.5,0.25,0.5,0.5),(0.5,0.5,0.4,0.2)]:
    eg=np.log(Nstar(2e-6,1,aL,bL,am,bm)/Nstar(1e-6,1,aL,bL,am,bm))/np.log(2)
    eu=np.log(Nstar(1e-6,2,aL,bL,am,bm)/Nstar(1e-6,1,aL,bL,am,bm))/np.log(2)
    print(f"  level ({aL:.3f},{bL:.3f}) members ({am:.3f},{bm:.3f}): e_g={eg:+.4f} (pred {-(1-bL)/(1-aL):+.4f});  e_u={eu:+.4f} (pred {(1-bm)/(1-aL):+.4f})")
print("\n=== (2) separately-read components: member cost sum_m sqrt(2 w B^2 q_m) + sqrt(2 w qu) -> modular ===")
rng=np.random.default_rng(9); maxdev=0
for _ in range(200):
    N=int(rng.integers(5,30)); M=int(rng.integers(2,6)); B=(rng.random((N,M))<0.6)*rng.lognormal(0,0.5,(N,M)); q=10**rng.uniform(-3,0,M); qu=rng.lognormal(0,0.3,N)
    def J(S): return sum(np.sqrt(2*(B[:,m]**2).sum()*q[m])+0.1 for m in S)+sum(np.sqrt(2*B[i,m]**2*q[m]) for i in range(N) for m in range(M) if m not in S)+np.sum(np.sqrt(2*qu))
    for S in [frozenset(np.flatnonzero(rng.random(M)<0.5))]:
        for m in range(M):
            if m in S: continue
            d1=J(S|{m})-J(S); d0=J(frozenset({m}))-J(frozenset())
            maxdev=max(maxdev,abs(d1-d0))
print(f"  max |marginal at S - marginal at empty| = {maxdev:.2e}  (0 => modular: levels independent)")
print("\n=== (3) T7 ordering with heterogeneous concave members psi_i(R)=k_i R^{b_i} (same R), kappa<kappa* ===")
def solve(S,beta,q0,kap,qu,a,b,h,ks,bs):
    Ntot=beta**S; best=None
    for k in range(S+1):
        for L in itertools.combinations(range(1,S+1),k):
            L=set(L); cost=0.0; R=qu
            for s in range(1,S+1):
                n=beta**s; qs=q0*n**(-kap)
                if s in L: cost+=(Ntot/n)*(n**a*qs**b+h)
                else: R+=qs
            cost+=Ntot*np.mean(ks*R**bs)
            if best is None or cost<best[0]-1e-12*abs(cost): best=(cost,L)
    return best[1]
bad=0; tot=0
for _ in range(120):
    b=rng.uniform(0.2,0.8); a=rng.uniform(0.1,0.85); ks_=(1-a)/(1-b); kap=rng.uniform(0,min(ks_,1)*0.98); q0=10**rng.uniform(-1,4)
    kk=rng.lognormal(0,0.5,8); bb=rng.uniform(0.2,0.9,8); h=0 if rng.random()<0.5 else 10**rng.uniform(-2,1)
    L=solve(9,2,q0,kap,1.0,a,b,h,kk,bb); tot+=1
    if L and L!=set(range(min(L),10)): bad+=1
print(f"  non-upper optimal sets: {bad}/{tot}")
