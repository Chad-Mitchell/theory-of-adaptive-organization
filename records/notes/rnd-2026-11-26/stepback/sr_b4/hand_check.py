# SR-b4 (B): independent small-case checks. LP-based operational distances (sr_b/srb_J.dists, no closed form) and
# brute-force enumeration of every T-step vertex sequence (no DP, no step cap). Also R_H by hand at H=2,3.
import sys, math, itertools, numpy as np
sys.path.insert(0,"../sr_b"); from srb_J import dists
def disk(T): return T*math.sin(math.pi/(2*T))**2
for n,H in ((6,2),(14,3),(26,4)):
  d=dists(n); targ=[j for j in range(n) if d[j]>1-1e-9]
  print(f"n={n}: LP distances d(v0,vk) k=1..n/2 = {np.round(d[1:n//2+1],6).tolist()}; targets {targ}")
  for T in range(1,H+1):
    best=min(sum(d[(b-a)%n]**2 for a,b in zip((0,)+seq[:-1],seq)) for seq in itertools.product(range(n),repeat=T) if seq[-1] in targ)
    print(f"   T={T}: brute-force J={best:.12f}  disk={disk(T):.12f}  polygon cheaper: {best<disk(T)-1e-12}")
# R_H by hand, H=2: J*(1)=1, J*(2)=1/2 (SR-b1(a) + hexagon). disk: rho=(1,2) -> R_2=(1+2/2)/(1+1/2)=4/3. hexagon: rho=(1,1) -> R_2=1.
print("H=2 by hand: R_2(disk) = (1 + 2/2)/(3/2) =", (1+2/2)/1.5, "; R_2(hexagon) = 1 (it attains J* at T=1,2)")
