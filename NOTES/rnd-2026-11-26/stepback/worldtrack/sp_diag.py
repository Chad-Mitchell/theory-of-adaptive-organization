import json,numpy as np
from sp_common import *
exec(open('ib_run.py').read().split("Pg=np.exp")[0])
Pg=np.exp(np.linspace(np.log(1e-14),np.log(v),600))
R=[json.loads(l) for l in open('sp_gauss.jsonl')]
fails=[r for r in R if r['nfar']>0]
# P-ratio of far points vs argmin; s-ratio; true J gap
pr=[];gaps=[]
for r in fails:
    P0=v*np.exp(-2*r['I'])
    for (Pf,sf) in r['far']:
        pr.append(max(Pf/P0,P0/Pf))
print("U1 failures:",len(fails),"; far points differing in P by >1.2:",sum(p>1.2 for p in pr),"of",len(pr),"; max P ratio %.3f"%max(pr))
# examine J along s at fixed optimal P for one failing cell, fine
r=fails[4]; sig,smin,x,G=r['sig'],r['smin'],r['x'],r['G']
sg=np.exp(np.linspace(np.log(smin),np.log(1e3),4000))
best=[]
for s in sg:
    lo,av,a=parts(Pg,s,sig); J=lo+2*G*0.5*np.log(v/Pg)+0.5*x*av; best.append(J.min())
best=np.array(best); d=np.diff(best)
print("cell",sig,smin,x,G,": profile over s (min over P): J range rel %.2e; # local minima"%((best.max()-best.min())/best.min()), n_profile_minima(best,1e-12*best.min()), "; increasing from s_min:",bool((d>=-1e-15*best.min()).all()))
print("   J(s_min)=%.10g  J(10)=%.10g  J(72)=%.10g"%(best[0],best[np.searchsorted(sg,10)],best[np.searchsorted(sg,72)]))
u2f=[r for r in R if r['nprof']!=1]
print("U2 failures:",len(u2f),[(r['sig'],r['smin'],r['c'],r['G'],r['x'],r['nprof']) for r in u2f][:12])
