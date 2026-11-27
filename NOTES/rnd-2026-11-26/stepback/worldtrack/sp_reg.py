import json,time,numpy as np
from sp_common import *
from wt_core import *
sigs=[1e-3,3e-3,1e-2,3e-2,0.1,0.3]; xs=[1,3,10,30,100,300,1e3,3e3,1e4,3e4,1e5,1e6]; Gs=[0,1e-5,1e-4,1e-3,1e-2,1e-1]
def geo(lo,hi,r):
    k=int(np.ceil(np.log(hi/lo)/np.log(r))); return lo*r**np.arange(1,k+1)
ng=np.unique(np.r_[np.arange(1,3001),np.round(geo(3000,3e6,1.02))]).astype(float)
sg=np.unique(np.r_[np.arange(1,3001),np.round(geo(3000,1e8,1.02))]).astype(float)
out=open('sp_reg.jsonl','w'); t0=time.time(); lnn=np.log(ng)[:,None]
for sig in sigs:
    for smin in [1.0,0.1,0.01]:
        sp=sig*np.sqrt(smin)
        H=H_point(ng[:,None],sg[None,:],sp); Rm=H/sg[None,:]; Lm=Lfun(ng[:,None],sg[None,:],sp,0)
        for c in [0.0,0.1,1.0,10.0]:
            for G in Gs:
                for x in xs:
                    J=2*G*smin*lnn+Rm+c/sg[None,:]+x*smin*Lm
                    i,k,Jmin,far=u1(J,ng,sg)
                    m=n_profile_minima(J.min(1),1e-9*Jmin)
                    out.write(json.dumps(dict(cls='Reg',sig=sig,smin=smin,c=c,arm='write',G=G,x=x,nfar=len(far),far=far[:3],nprof=m,
                        I=float(np.log(ng[i])),n=int(ng[i]),s=float(sg[k]),edge=bool(k==len(sg)-1 and ng[i]>1) or bool(i==len(ng)-1),blind=bool(ng[i]==1)))+"\n")
            out.flush()
        print(sig,smin,f"done {time.time()-t0:.0f}s",flush=True)
print("ALL DONE",flush=True)
