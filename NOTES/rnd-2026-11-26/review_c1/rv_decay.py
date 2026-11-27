# Directional decay of correlations / mutual information at radii beyond the greedy records (OBSERVED)
import sys, math, numpy as np
sys.path.insert(0,'../stepback/c1')
from c1_vacua import Vacuum, S_bits, VACUA
from rv_greedy_mu import VacMu
T=[(0,0),(1,0),(0,1),(1,1)]
def blk(x,y): return [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]
vacs=list(VACUA.items())+[('NN mu=-2',None)]
for name,par in vacs:
    v=VacMu(-2.0) if par is None else Vacuum(*par)
    ST=S_bits(v.P(T)); I=lambda B: ST+S_bits(v.P(B))-S_bits(v.P(T+B))
    rows=[]
    for r in (4,8,16,32):
        # 2x2 block whose centre is at distance ~r from plaquette centre along +x axis and along the diagonal
        ax=blk(2*(r//2),0); dg=blk(int(round(r/math.sqrt(2))),int(round(r/math.sqrt(2))))
        ra=math.hypot(ax[0][0]+.5-.5,0); rd=math.hypot(dg[0][0],dg[0][1])
        Ia,Id=I(ax),I(dg)
        rows.append(f"r~{r}: I_axis={Ia:.2e} (r={ra:.1f}) I_diag={Id:.2e} (r={rd:.1f}) diag/axis={Id/Ia:.2f}")
    print(name,'|','; '.join(rows),flush=True)
