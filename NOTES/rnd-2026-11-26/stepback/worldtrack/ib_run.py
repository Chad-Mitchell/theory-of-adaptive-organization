import json, time, numpy as np
from scipy.optimize import minimize
sigs=[1e-3,3e-3,1e-2,3e-2,0.1,0.3]; xs=[1,3,10,30,100,300,1e3,3e3,1e4,3e4,1e5,1e6]; Gs=[0,1e-5,1e-4,1e-3,1e-2,1e-1]
smins=[1.0,0.1,0.01]; cs=[0.0,0.1,1.0,10.0]; cK=2.0
v=np.pi**2/3
def parts(P,s,sig):
    a=3*sig**2/(2*np.pi**2); y=2*a*s
    E=-np.expm1(-y); r=np.where(y<1e-8,1-y/2,E/np.where(y==0,1,y))
    Pm=P+(v-P)*E
    look=0.5*np.log(Pm/P)/s
    avg=v+(P-v)*r
    return look,avg,a
def Kavg(P,s,sig):  # cycle-averaged stored info 0.5 ln(v/P(u))
    a=3*sig**2/(2*np.pi**2)
    g,w=np.polynomial.legendre.leggauss(16); u=(g+1)/2
    acc=0
    for ui,wi in zip(u,w):
        Pu=P+(v-P)*(-np.expm1(-2*a*s*ui)); acc=acc+wi/2*0.5*np.log(v/Pu)
    return acc
Pg=np.exp(np.linspace(np.log(1e-14),np.log(v),600)); 
out=open('ib_run.jsonl','w'); t0=time.time()
for sig in sigs:
    for smin in smins:
        sg=np.exp(np.linspace(np.log(smin),np.log(1e8),600))
        look,avg,a=parts(Pg[:,None],sg[None,:],sig)
        Kw=0.5*np.log(v/Pg)[:,None]
        Ka=None
        for c in cs:
            for G in Gs:
                arms=[('write',Kw)]
                if smin==1.0 and c==0.0:
                    if Ka is None: Ka=Kavg(Pg[:,None],sg[None,:],sig)
                    arms.append(('avgkeep',Ka))
                for arm,Kmat in arms:
                    for x in xs:
                        J=look+cK*G*Kmat+c/sg[None,:]+0.5*x*avg
                        i,k=np.unravel_index(np.argmin(J),J.shape)
                        def f(z):
                            P=np.exp(z[0]); s=np.exp(z[1])
                            if P>v or s<smin or P<1e-16 or s>1e9: return 1e300
                            lo,av,_=parts(P,s,sig)
                            Kk=0.5*np.log(v/P) if arm=='write' else Kavg(P,s,sig)
                            return float(lo+cK*G*Kk+c/s+0.5*x*av)
                        z0=np.array([np.log(Pg[i]),np.log(sg[k])])
                        res=minimize(f,z0,method='Nelder-Mead',options=dict(xatol=1e-7,fatol=1e-14,maxiter=4000))
                        z=res.x if res.fun<=J[i,k] else z0
                        P,s=np.exp(z); s=max(s,smin); P=min(P,v)
                        lo,av,_=parts(P,s,sig)
                        Kk=float(0.5*np.log(v/P) if arm=='write' else Kavg(P,s,sig))
                        rec=dict(sig=sig,smin=smin,c=c,G=G,x=x,arm=arm,P=float(P),s=float(s),J=float(lo+cK*G*Kk+c/s+0.5*x*av),
                                 look=float(lo),keep=float(cK*G*Kk),price=float(c/s),loss=float(0.5*x*av),
                                 nats=float(lo*s),I=float(0.5*np.log(v/P)),blind=bool(P>0.999*v),
                                 edge=bool(k==len(sg)-1 or i==0),core=float(2*np.sqrt(a*v*x/2)-a) if x/2>=a/v else float(x/2*v))
                        out.write(json.dumps(rec)+"\n")
            out.flush()
        print(f"sig {sig} smin {smin} done {time.time()-t0:.0f}s",flush=True)
print("ALL DONE",flush=True)
