"""Round 4 numerics (no physics).
G1 stationary finite-state worlds: novelty rate H(X1|X0) equals destruction rate H(X0|X1) (exact identity; checked).
G2 how much a tracker can ever learn from a trajectory:
   - reversible finite world (permutation): distinct length-L observation windows stop growing (bounded total information);
   - irrational rotation observed through one sharp effect (sign): distinct windows grow like L+1 (Sturmian), so total
     information is unbounded but the RATE -> 0;
   - positive-rate novelty needs a stochastic map, which destroys information at the same rate (G1).
G3 selection needs irreversibility: long-run share of a feature under (a) a permutation, (b) an irrational rotation,
   (c) a contracting (many-to-one) map.
"""
import numpy as np
rng=np.random.default_rng(11)
def H(p): p=np.asarray(p,float).ravel(); p=p[p>1e-15]; return float(-(p*np.log2(p)).sum())
print("G1 stationary Markov chains (random, n states): novelty H(X1|X0) vs destruction H(X0|X1)")
worst=0
for n in [2,3,5,8]:
    for _ in range(500):
        P=rng.random((n,n))**3; P/=P.sum(1,keepdims=True)
        w,v=np.linalg.eig(P.T); pi=np.real(v[:,np.argmin(abs(w-1))]); pi/=pi.sum()
        J=pi[:,None]*P; nov=H(J)-H(pi); des=H(J)-H(J.sum(0))
        worst=max(worst,abs(nov-des))
print(f"   max |novelty - destruction| over 2000 chains: {worst:.2e}  (identity: H(X0,X1)-H(X0) = H(X0,X1)-H(X1) when marginals are equal)")
print("   a permutation chain: novelty 0, destruction 0; any positive novelty rate is paid by an equal destruction rate.")

print("\nG2 distinct observation windows of length L (log2 = information a tracker can ever extract from that window)")
M=64; perm=rng.permutation(M); x=0; seq=[]
for t in range(20000): seq.append(x%2); x=perm[x]
alpha=(np.sqrt(5)-1)/2; th=0.123; rot=[int(((th+alpha*t)%1)<0.5) for t in range(20000)]
for L in [4,8,16,32,64,128]:
    wp=len({tuple(seq[i:i+L]) for i in range(len(seq)-L)}); wr=len({tuple(rot[i:i+L]) for i in range(len(rot)-L)})
    print(f"   L={L:4d}  permutation world (64 states): {wp:5d} windows   irrational rotation: {wr:5d} windows")
print("   permutation: windows saturate at <= period (bounded learning). rotation (sign readout): about 2L windows, so")
print("   total information ~ log L, unbounded, rate -> 0. (For a single half-circle readout the count is 2L; Sturmian n+1 is the")
print("   two-letter coding by an interval of length alpha; both are linear in L.)")

print("\nG3 long-run share of a feature (the 'variant' set) along one trajectory")
def share(step,x0,feat,T=200000):
    x=x0; c=0
    for t in range(T):
        c+=feat(x); x=step(x)
    return c/T
feat_set=set(rng.choice(M,16,replace=False))
for T in [1000,10000,100000]:
    a=share(lambda z: perm[z],0,lambda z: z in feat_set,T)
    b=share(lambda z: (z+alpha)%1,0.3,lambda z: z<0.25,T)
    c=share(lambda z: z/2 if z<0.5 else z,0.9,lambda z: z<0.25,T)   # placeholder replaced below
    print(f"   T={T:6d}: permutation share={a:.4f}  rotation share={b:.4f}")
def contract(z):  # many-to-one: everything flows into [0,0.25) and stays
    return z*0.5 if z>=0.25 else z
print(f"   contracting map: share of [0,0.25) after T steps from z0=0.9: {share(contract,0.9,lambda z:z<0.25,10000):.4f} (-> 1: the feature grows)")
print("   permutation and rotation: shares converge to fixed values (orbit measure); no feature grows. Growth (selection) needs a many-to-one map.")
