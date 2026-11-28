# NON-SCORED: power / planted-effect table from toy runs.
import math, collections, numpy as np
from c4r_decide import parse, decide, R, RAYS
P=parse(open('toy/planted_N1e6.txt')); C=parse(open('toy/control_N1e6.txt')); L=parse(open('toy/lattice_T4000.txt'))
C.sort(key=lambda r:int(r['seed']))
def truth(cp,s): return math.sqrt(1-(s/cp)**2)/math.sqrt(1-s*s)
print("toy size N0=1e6 per diamond at s=0; 10 batches of 16 seeds vs 10 disjoint control batches of 16")
print("control alone: mean R(s) over 160 seeds:",{s:round(float(np.mean([R(r,s) for r in C])),4) for s in RAYS}, " per-seed sd:",{s:round(float(np.std([R(r,s) for r in C],ddof=1)),4) for s in RAYS})
for cp in sorted({r['cp'] for r in P}):
    rs=sorted([r for r in P if r['cp']==cp],key=lambda r:int(r['seed']))
    cnt=collections.Counter(); dR9=[];z9=[]
    for k in range(10):
        dec,res=decide(rs[16*k:16*k+16],C[16*k:16*k+16]); cnt[dec]+=1; dR9.append(res[0.9]['dR']); z9.append(res[0.9]['z'])
    print(f"cp={cp:.2f} planted R-1 at s=.5/.75/.9 = {truth(cp,.5)-1:.3f}/{truth(cp,.75)-1:.3f}/{truth(cp,.9)-1:.3f} | measured dR(.9) mean {np.mean(dR9):.3f} (z median {np.median(z9):.0f}) | decisions {dict(cnt)}")
# lattice toy vs control toy, one batch
dec,res=decide(L,C[:16]); print("toy lattice T=4000 (seeds 1-16) vs control batch 1:",dec,{s:(round(v['Rt'],3),round(v['dR'],3),round(v['z'])) for s,v in res.items()})
# old exponent observable: blind to the plant (fit of log L vs log tau over sizes) - see toy_exponent.py
