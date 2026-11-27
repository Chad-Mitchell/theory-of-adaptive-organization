# SR-b analysis (OBSERVED) on srb_all.json (n=3..401) and srb_big.json (n=300..1001 selected).
import json, math, numpy as np
A={int(k):np.array(v) for k,v in json.load(open("srb_all.json")).items()}
A.update({int(k):np.array(v) for k,v in json.load(open("srb_big.json")).items()})
disk=lambda T: T*math.sin(math.pi/(2*T))**2
def J(n,T): c=A[n]; return c[min(T,len(c))-1]
print("(C) best polygon at each horizon, J*(T)=min_n J(n,T) over n=3..401 (+ big n); ratio to disk and to the 1/T floor")
for T in [1,2,3,4,5,8,10,15,20,30,50,75,100,150,200]:
    nb=min(A,key=lambda n:J(n,T)); js=J(nb,T)
    print(f"   T={T:3d}: n*={nb:4d} J*={js:.6f} disk={disk(T):.6f} J*/disk={js/disk(T):.4f} T*J*={T*js:.4f} (floor 1; disk -> pi^2/4={math.pi**2/4:.4f})")
def EJ(n,q):
    c=A[n]; w=1-q; L=len(c); Ts=np.arange(1,L+1)
    return float(np.sum(w*q**(Ts-1)*c)+q**L*c[-1])
def Edisk(q):
    T=np.arange(1,4_000_001); p=(1-q)*q**(T-1.0); return float(np.sum(p*T*np.sin(np.pi/(2*T))**2))
print("(D) geometric horizon mixture p(T)=(1-q)q^(T-1), T>=1; price-free (equal kappa per affine dimension); best polygon over all computed n vs disk")
for q in [0.5,0.8,0.9,0.95,0.96,0.97,0.975,0.98,0.985,0.99,0.995]:
    ed=Edisk(q); vals={n:EJ(n,q) for n in A}; nb=min(vals,key=vals.get)
    print(f"   q={q:5.3f} (mean T {1/(1-q):6.1f}): disk={ed:.6f} best n={nb:4d} ({vals[nb]:.6f}) -> {'polygon' if vals[nb]<ed-1e-12 else 'disk'} cheaper, margin {(ed-vals[nb])/ed:+.4f}")
print("(E) the same with a design price fixed in advance: lambda*log2|G|, |G|=2n (dihedral), disk |G|=inf (price inf) -> disk never chosen; and lambda=0 is (D)")
print("(F) uniform horizon on 1..H (another proper mixture), price-free")
for H in [5,10,20,50,100,200]:
    ed=np.mean([disk(T) for T in range(1,H+1)]); vals={n:np.mean([J(n,T) for T in range(1,H+1)]) for n in A}; nb=min(vals,key=vals.get)
    print(f"   H={H:3d}: disk={ed:.6f} best n={nb:4d} ({vals[nb]:.6f}) -> {'polygon' if vals[nb]<ed-1e-12 else 'disk'} cheaper, margin {(ed-vals[nb])/ed:+.4f}")
print("(G) PIM checks: J(n,T) >= max(1/T, dmin(n)) for all computed n,T")
from srb_J import dists
bad=0
for n in list(range(3,402,7)):
    dm=dists(n)[1]; c=A[n]
    for T in range(1,len(c)+1):
        if c[T-1] < max(1/T, dm)-1e-9: bad+=1
print(f"   violations: {bad}")
