import json,numpy as np
from sp_common import *
exec(open('ib_run.py').read().split("Pg=np.exp")[0])
Pg=np.exp(np.linspace(np.log(1e-14),np.log(v),600))
R=[json.loads(l) for l in open('sp_gauss.jsonl')]
for r in [r for r in R if r['nprof']!=1][:30]:
    sg=np.exp(np.linspace(np.log(r['smin']),np.log(1e8),600))
    look,avg,a=parts(Pg[:,None],sg[None,:],r['sig'])
    J=look+2*r['G']*0.5*np.log(v/Pg)[:,None]+r['c']/sg[None,:]+0.5*r['x']*avg
    prof=J.min(1)[::-1]; I=0.5*np.log(v/Pg[::-1])
    d=np.diff(prof); idx=[0] if d[0]>0 else []
    idx+=[i+1 for i in range(len(d)-1) if d[i]<0 and d[i+1]>0]
    print(r['sig'],r['smin'],r['c'],r['G'],r['x'],"local minima at I=",[round(float(I[i]),3) for i in idx],"J=",[round(float(prof[i]),5) for i in idx],"global I*",round(r['I'],3))
