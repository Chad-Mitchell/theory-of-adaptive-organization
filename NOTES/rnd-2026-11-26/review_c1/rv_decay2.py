# Wedge-averaged single-site mutual information I(T:site) along axes vs diagonals (OBSERVED); smooths sublattice oscillations
import sys, math, numpy as np
sys.path.insert(0,'../stepback/c1')
from c1_vacua import Vacuum, S_bits, VACUA
from rv_greedy_mu import VacMu
T=[(0,0),(1,0),(0,1),(1,1)]; c=(0.5,0.5)
for name,par in list(VACUA.items())+[('NN mu=-2',None)]:
    v=VacMu(-2.0) if par is None else Vacuum(*par); ST=S_bits(v.P(T)); I=lambda B: ST+S_bits(v.P(B))-S_bits(v.P(T+B))
    out=[]; prev=None
    for r in (6,8,12,16,24):
        acc={0:[],1:[]}
        for x in range(-r-2,r+3):
            for y in range(-r-2,r+3):
                d=math.hypot(x-c[0],y-c[1])
                if abs(d-r)>1.0: continue
                a=math.degrees(math.atan2(y-c[1],x-c[0]))%90
                if a<=12 or a>=78: acc[0].append(I([(x,y)]))
                elif 33<=a<=57: acc[1].append(I([(x,y)]))
        ma,md=np.mean(acc[0]),np.mean(acc[1]); out.append(f"r={r}: axis {ma:.2e} diag {md:.2e} diag/axis {md/ma:.2f}")
    print(name,'|','; '.join(out),flush=True)
