import json,time,numpy as np
from sp_common import *
exec(open('ib_run.py').read().split("Pg=np.exp")[0])
sigs=[1e-3,3e-3,1e-2,3e-2,0.1,0.3]; xs=[1,3,10,30,100,300,1e3,3e3,1e4,3e4,1e5,1e6]; Gs=[0,1e-5,1e-4,1e-3,1e-2,1e-1]
Pg=np.exp(np.linspace(np.log(1e-14),np.log(v),600)); out=open('sp_gauss.jsonl','w')
for sig in sigs:
    for smin in [1.0,0.1,0.01]:
        sg=np.exp(np.linspace(np.log(smin),np.log(1e8),600))
        look,avg,a=parts(Pg[:,None],sg[None,:],sig); Kw=0.5*np.log(v/Pg)[:,None]; Ka=None
        for c in [0.0,0.1,1.0,10.0]:
            arms=[('write',Kw)]
            if smin==1.0 and c==0.0: Ka=Kavg(Pg[:,None],sg[None,:],sig); arms.append(('avgkeep',Ka))
            for arm,Km in arms:
                for G in Gs:
                    for x in xs:
                        J=look+2*G*Km+c/sg[None,:]+0.5*x*avg
                        i,k,Jmin,far=u1(J,Pg,sg)
                        prof=J.min(1)[::-1]  # order by increasing I (decreasing P)
                        m=n_profile_minima(prof,1e-9*Jmin)
                        out.write(json.dumps(dict(cls='G',sig=sig,smin=smin,c=c,arm=arm,G=G,x=x,nfar=len(far),far=far[:3],nprof=m,
                            I=float(0.5*np.log(v/Pg[i])),s=float(sg[k]),edge=bool(k==len(sg)-1 or i==0),blind=bool(i==len(Pg)-1)))+"\n")
        print(sig,smin,"done",flush=True)
print("ALL DONE",flush=True)
