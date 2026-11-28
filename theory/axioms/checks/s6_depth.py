"""S6. Theorem 8 (which scales of a nested hierarchy get a level). Groups nested with branching beta; scale s has
groups of size n_s=beta^s, shared driver rate q_s = q0 n_s^(-kappa). Power class (a,b). Exact brute force over all
subsets of scales vs the first-order rule  n_s^((1-a)-kappa(1-b)) > const, i.e. critical kappa* = (1-a)/(1-b) = 1/|e_g|."""
import numpy as np, itertools
def total(L,S,beta,q0,kap,qu,a,b,h,w=1.0):
    Ntot=beta**S; cost=0.0; R=qu
    for s in range(1,S+1):
        n=beta**s; qs=q0*n**(-kap)
        if s in L: cost+=(Ntot/n)*((n*w)**a*qs**b+h)
        else: R+=qs
    return cost+Ntot*w**a*R**b
def solve(S,beta,q0,kap,qu,a,b,h):
    best=None
    for k in range(S+1):
        for L in itertools.combinations(range(1,S+1),k):
            v=total(set(L),S,beta,q0,kap,qu,a,b,h)
            if best is None or v<best[0]-1e-12*abs(v): best=(v,set(L))
    return best[1]
def first_order(S,beta,q0,kap,qu,a,b,h,w=1.0):
    R=qu+sum(q0*(beta**s)**(-kap) for s in range(1,S+1)); keep=set()
    for s in range(1,S+1):
        n=beta**s; qs=q0*n**(-kap)
        if n*b*w**a*R**(b-1)*qs-((n*w)**a*qs**b+h)>0: keep.add(s)
    return keep
def shape(L,S):
    if not L: return 'none'
    if L==set(range(min(L),S+1)): return 'upper (broad scales: top-down)'
    if L==set(range(1,max(L)+1)): return 'lower (narrow scales: bottom-up)'
    return 'interval' if L==set(range(min(L),max(L)+1)) else 'other'
S=14; beta=2; qu=1.0
import collections
for (a,b,name) in [(0.5,0.5,'R (|e_g|=1, kappa*=1)'),(2/3,1/3,'A_1 (|e_g|=2, kappa*=0.5)')]:
    ks=(1-a)/(1-b); print(f"=== class {name}: kappa* = (1-a)/(1-b) = {ks:.3f} ===")
    for kap in ([0.3,0.6,0.9,1.1,1.4,2.0] if a==0.5 else [0.1,0.25,0.4,0.6,0.8,1.2]):
        shapes=collections.Counter(); incl=0; tot=0; ex=[]
        for q0 in np.logspace(-2,4,13):
            L=solve(S,beta,q0,kap,qu,a,b,0.0); fo=first_order(S,beta,q0,kap,qu,a,b,0.0)
            sh=shape(L,S); shapes[sh]+=1; tot+=1; incl+=(fo<=L)
            if sh not in ('none',) and len(ex)<2: ex.append((round(q0,3),sorted(L),sorted(fo)))
        print(f"  kappa={kap:.2f} ({'<' if kap<ks else '>'} kappa*): shapes over 13 q0 values: {dict(shapes)}; first-order subset of exact {incl}/{tot}; e.g. {ex}")
print("\n=== upkeep h=2 (a=b: e_g=-1 for all h, so kappa*=1 unchanged; class A at small rho keeps kappa*=0.5) ===")
for (a,b) in [(0.5,0.5),(2/3,1/3)]:
    for kap in [0.3,0.45,0.55,0.9,1.1,1.5]:
        shapes=collections.Counter()
        for q0 in np.logspace(-1,4,11):
            shapes[shape(solve(S,beta,q0,kap,qu,a,b,2.0),S)]+=1
        print(f"  a={a:.2f} b={b:.2f} kappa={kap}: {dict(shapes)}")
print("\n=== depth vs q0 (fine scan), class R, h=0: gradual growth for kappa<kappa*, avalanche for kappa>kappa* ===")
for kap in [0.3,0.6,1.4,2.0]:
    row=[]
    for q0 in np.logspace(-2,4.5,27):
        L=solve(S,beta,q0,kap,qu,0.5,0.5,0.0); row.append(len(L))
    print(f"  kappa={kap}: depth over q0=1e-2..10^4.5 (27 log steps): {row}")
print("\n=== exact upper-set property for kappa<kappa*: random (a,b), concave member cost, h>=0 ===")
rng=np.random.default_rng(66); bad=0; tot=0
for _ in range(150):
    b=rng.uniform(0.2,0.8); a=rng.uniform(0.1,0.85); ks=(1-a)/(1-b); kap=rng.uniform(0,ks*0.98); q0=10**rng.uniform(-2,4); h=0 if rng.random()<0.5 else 10**rng.uniform(-2,1)
    L=solve(10,2,q0,kap,qu,a,b,h); tot+=1
    if L and L!=set(range(min(L),11)): bad+=1
print(f"  optimal set not an upper set: {bad}/{tot}")
