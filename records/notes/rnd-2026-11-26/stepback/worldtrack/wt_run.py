import json, time, sys
from wt_core import *
from scipy.ndimage import minimum_filter
sigs=[1e-3,3e-3,1e-2,3e-2,0.1,0.3]
xs=[1,3,10,30,100,300,1e3,3e3,1e4,3e4,1e5,1e6]
Gs=[0,1e-5,1e-4,1e-3,1e-2,1e-1]
arms=[('primary',0,2.0),('a1',1,2.0),('cK4',0,4.0)]
def geo(lo,hi,r): 
    k=int(np.ceil(np.log(hi/lo)/np.log(r))); return lo*r**np.arange(1,k+1)
ng=np.r_[np.arange(1,3001),np.round(geo(3000,3e6,1.02))].astype(float); ng=np.unique(ng)
sg=np.r_[np.arange(1,3001),np.round(geo(3000,1e8,1.02))].astype(float); sg=np.unique(sg)
out=open('wt_run.jsonl','a')
t0=time.time()
for sig in sigs:
    H=H_point(ng[:,None],sg[None,:],sig)
    print(f"sigma {sig}: H matrix done {time.time()-t0:.0f}s",flush=True)
    lnn=np.log(ng)[:,None]
    for arm,a,cK in arms:
        Lm=Lfun(ng[:,None],sg[None,:],sig,a)
        R=H/sg[None,:]
        for G in Gs:
            K=cK*G*lnn
            for x in xs:
                J=K+R+x*Lm
                i,k=np.unravel_index(np.argmin(J),J.shape); Jmin=J[i,k]
                lm=(J==minimum_filter(J,size=3,mode='nearest'))&(J<=Jmin*(1+1e-3))
                ii,kk=np.nonzero(lm)
                far=[(int(ng[p]),int(sg[q]),float(J[p,q])) for p,q in zip(ii,kk) if (max(ng[p]/ng[i],ng[i]/ng[p])>1.2 or max(sg[q]/sg[k],sg[k]/sg[q])>1.2)]
                n0,s0=ng[i],sg[k]
                # refine beyond integer region
                if n0>1 and (n0>3000 or s0>3000):
                    nf=np.unique(np.round(n0*np.exp(np.linspace(-0.05,0.05,201)))) if n0>3000 else np.arange(max(1,n0-3),n0+4)
                    sf=np.unique(np.round(s0*np.exp(np.linspace(-0.05,0.05,201)))) if s0>3000 else np.arange(max(1,s0-3),s0+4)
                    Hf=H_point(nf[:,None],sf[None,:],sig)
                    Jf=cK*G*np.log(nf)[:,None]+Hf/sf[None,:]+x*Lfun(nf[:,None],sf[None,:],sig,a)
                    p,q=np.unravel_index(np.argmin(Jf),Jf.shape)
                    if Jf[p,q]<Jmin: n0,s0,Jmin=nf[p],sf[q],Jf[p,q]
                Hs=float(H_point(np.array([n0]),np.array([s0]),sig)[0])
                keep=cK*G*np.log(n0); read=Hs/s0; loss=x*float(Lfun(np.array([n0]),np.array([s0]),sig,a)[0])
                rec=dict(arm=arm,sig=sig,x=x,G=G,n=int(n0),s=int(s0),J=float(Jmin),keep=float(keep),read=float(read),loss=float(loss),
                    H=Hs,rho=float(sig*np.sqrt(s0)*n0/(2*np.pi)),blind=bool(n0==1),
                    edge_n=bool(i==len(ng)-1),edge_s=bool(k==len(sg)-1 and n0>1),nfar=len(far),far=far[:5],
                    nGPK=(float(np.pi*np.sqrt(x/(3*cK*G))) if G>0 else None),Jblind=float(x))
                out.write(json.dumps(rec)+"\n"); out.flush()
        print(f"sigma {sig} arm {arm} done {time.time()-t0:.0f}s",flush=True)
print("ALL DONE",flush=True)
