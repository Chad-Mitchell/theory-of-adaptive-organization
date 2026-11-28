# C1 greedy per-site-priced record around a 2x2 plaquette (OBSERVED numerics). Usage: python3 c1_greedy.py <vacuum index 0-3> [cheb=3] [nmax=200] [K=256]
import sys, json, math, time, numpy as np
from c1_vacua import Vacuum, S_bits, VACUA
idx=int(sys.argv[1]); cheb=int(sys.argv[2]) if len(sys.argv)>2 else 3; nmax=int(sys.argv[3]) if len(sys.argv)>3 else 200
K=int(sys.argv[4]) if len(sys.argv)>4 else 256
name,(flux,m)=list(VACUA.items())[idx]; v=Vacuum(flux,m,K=K)
T=[(0,0),(1,0),(0,1),(1,1)]; c0=(0.5,0.5); RMAX=30
def I_of(S):
    return S_T + S_bits(v.P(S)) - S_bits(v.P(T+S))
S_T=S_bits(v.P(T))
sel=[]; gains=[]; Icur=0.0; t0=time.time()
occupied=set(T)
def cands():
    out=set()
    for (x,y) in list(occupied):
        for dx in range(-cheb,cheb+1):
            for dy in range(-cheb,cheb+1):
                p=(x+dx,y+dy)
                if p not in occupied and (p[0]-c0[0])**2+(p[1]-c0[1])**2<=RMAX**2: out.add(p)
    return sorted(out)
while len(sel)<nmax:
    best=None
    for p in cands():
        g=I_of(sel+[p])-Icur
        if best is None or g>best[0]+1e-13: best=(g,p)
    g,p=best; sel.append(p); occupied.add(p); gains.append(g); Icur+=g
    if len(sel)%20==0: print(len(sel),round(g,5),round(time.time()-t0),flush=True)
json.dump({"vacuum":name,"cheb":cheb,"K":K,"S_T":S_T,"sel":sel,"gains":gains},open(f"c1_greedy_v{idx}_c{cheb}_n{nmax}.json","w"))
print(f"{name}: S(T)={S_T:.4f} bits; {len(sel)} sites in {time.time()-t0:.0f}s; final I(T:S)={Icur:.4f}; gains first 10={np.round(gains[:10],4).tolist()} last 5={np.round(gains[-5:],5).tolist()}")
