# Check the reviewer's breakpoint distance against an LP, and the claimed closed form for even n (SR_B §8.6), and DP variants vs brute force.
import itertools, math, numpy as np
from rv_core import *
mx=0;mx2=0
for n in range(3,41):
    a=dist_row(n); b=dist_lp(n); mx=max(mx,np.abs(a-b).max())
    if n%2==0:
        S=n//2; cf=np.array([math.sin(math.pi*k/n)/(math.cos(math.pi/n) if (k-S)%2 else 1) for k in range(n)])
        cf=np.minimum(cf,cf[::-1].copy()) if False else np.array([cf[k] if k<=S else cf[n-k] for k in range(n)])
        mx2=max(mx2,np.abs(a-cf).max())
print(f"n=3..40: max |breakpoint - LP| = {mx:.2e}; even n: max |breakpoint - closed form| = {mx2:.2e}")
print("targets (d=1) n=6..12:",{n:targets(dist_row(n)) for n in range(5,13)})
mx=0
for n in range(3,61):
    T=min(n,30); a=J_circ(n,T); b=J_fwd(n,T); mx=max(mx,np.abs(a-b).max())
print(f"n=3..60, T<=30: max |circular DP - forward DP| = {mx:.2e}")
for n,T in ((6,3),(7,3),(8,3),(10,3),(14,3),(13,3),(26,3)):
    d=dist_row(n); tg=targets(d)
    bf=[min(sum(d[(b-a)%n]**2 for a,b in zip((0,)+s[:-1],s)) for s in itertools.product(range(n),repeat=t) if s[-1] in tg) for t in range(1,T+1)]
    print(f"n={n:2d} brute force J(1..{T})={np.round(bf,12).tolist()}  DP={np.round(J_circ(n,T),12).tolist()}")
