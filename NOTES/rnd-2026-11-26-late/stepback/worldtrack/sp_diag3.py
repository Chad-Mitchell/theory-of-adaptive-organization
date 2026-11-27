import json,numpy as np
from wt_core import *
from sp_common import n_profile_minima
def geo(lo,hi,r):
    k=int(np.ceil(np.log(hi/lo)/np.log(r))); return lo*r**np.arange(1,k+1)
ng=np.unique(np.r_[np.arange(1,3001),np.round(geo(3000,3e6,1.02))]).astype(float)
sg=np.unique(np.r_[np.arange(1,3001),np.round(geo(3000,1e8,1.02))]).astype(float)
R=[json.loads(l) for l in open('sp_reg.jsonl')]
bad=[r for r in R if r['nprof']!=1]
m=ng>=405; nn=ng[m]
for r in bad[:6]:
    sp=r['sig']*np.sqrt(r['smin']); 
    H=H_point(nn[:,None],sg[None,:],sp)
    J=2*r['G']*r['smin']*np.log(nn)[:,None]+H/sg[None,:]+r['c']/sg[None,:]+r['x']*r['smin']*Lfun(nn[:,None],sg[None,:],sp,0)
    prof=J.min(1); d=np.diff(prof); tol=1e-9*prof.min()
    idx=[i+1 for i in range(len(d)-1) if d[i]<-tol and d[i+1]>tol]
    print(r['sig'],r['smin'],r['c'],r['G'],r['x'],"n*",r['n'],"profile minima at n=",[int(nn[i]) for i in idx],"J=",[float('%.10g'%prof[i]) for i in idx], "rel gap %.2e"%((max(prof[i] for i in idx)-min(prof[i] for i in idx))/prof.min() if len(idx)>1 else 0))
    # same with s on fine geometric grid (ratio 1.001) to test grid artifact
    sf=np.unique(np.round(np.exp(np.linspace(0,np.log(1e5),12000))))
    H2=H_point(nn[:,None],sf[None,:],sp)
    J2=2*r['G']*r['smin']*np.log(nn)[:,None]+H2/sf[None,:]+r['c']/sf[None,:]+r['x']*r['smin']*Lfun(nn[:,None],sf[None,:],sp,0)
    print("    with all-integer s grid to 1e5: profile minima count",n_profile_minima(J2.min(1),1e-9*J2.min()))
