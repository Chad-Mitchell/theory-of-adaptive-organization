# Probe: do larger polygons push alpha* toward 1 (menu-cap dependence)? Exact disk optimizer.
from rv_tl2 import disk_exact, PH
from rv_tl import d0_row, poly_move, disk_move
import numpy as np
for T,lam in [(8,1000),(8,30),(20,30)]:
    DM=disk_move(PH,T); Lp=(1+np.cos(PH))/2; Lr=1-np.sin(PH/2)
    for K in [180,360,720,1440]:
        best={}
        for n in range(K-8,K+1):
            d=d0_row(n); m=poly_move(n,T,d); lp=(1+np.cos(2*np.pi*np.arange(n)/n))/2; lr=1-d
            for a in [0.1,0.3,0.5,0.7,0.9,0.97,0.99]:
                v=(m+lam*(a*lp+(1-a)*lr)).min()
                if v<best.get(a,(np.inf,))[0]: best[a]=(v,n)
        print(T,lam,"K",K,{a:(f"{disk_exact(a,lam,T,DM,Lp,Lr)-best[a][0]:+.2e}",best[a][1]) for a in sorted(best)},flush=True)
