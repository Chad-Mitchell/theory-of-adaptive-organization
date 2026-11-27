import numpy as np, json, itertools
from t1_core import *
# quadrature check
for (r,f,G) in [(0.05,1,0.05),(0.8,4,0.2)]:
    a=Itab(r,f,G,nmax=40); 
    for n in (1,7,40):
        b=Itab(r,f,G,nmax=n,adaptive=True)[n] if n<=7 else None
        if b is not None: print(f"quad check r={r} f={f} G={G} n={n}: GL={a[n]:.12f} adaptive={b:.12f} diff={abs(a[n]-b):.2e}")
    print(f"  r={r} f={f} G={G}: I_1..5 =",np.round(a[1:6],5)," I_40=",round(a[40],5), " concave(ΔI nonincreasing) violations:",int(np.sum(np.diff(np.diff(a))>1e-12)))
# n=40 adaptive check (one case, slower)
b=Itab(0.2,1,0.05,nmax=40,adaptive=True); a=Itab(0.2,1,0.05)
print("n=40 adaptive check r=0.2 f=1 G=0.05: diff max over n =",float(np.max(np.abs(a-b))))
# Gate P
r=(0.05,0.2,0.8); 
for (f,G) in [(1,0.05),(4,0.2)]:
    It=[Itab(rk,f,G) for rk in r]
    fails=0; tested=0
    for M in range(1,61):
        best=(-1,None)
        for n1 in range(0,min(M,40)+1):
            for n2 in range(0,min(M-n1,40)+1):
                n3=min(M-n1-n2,40)
                v=It[0][n1]+It[1][n2]+It[2][n3]
                if v>best[0]+1e-15: best=(v,(n1,n2,n3))
        ns=best[1]
        if min(ns)>=1 and max(ns)<40:
            conc=all(It[k][ns[k]+1]-It[k][ns[k]]<=It[k][ns[k]]-It[k][ns[k]-1]+1e-12 for k in range(3))
            lo=max(It[k][ns[k]+1]-It[k][ns[k]] for k in range(3)); hi=min(It[k][ns[k]]-It[k][ns[k]-1] for k in range(3))
            if conc:
                tested+=1
                if lo>hi+1e-12: fails+=1
    print(f"Gate P f={f} G={G}: tested M={tested}, bracket failures={fails}")
