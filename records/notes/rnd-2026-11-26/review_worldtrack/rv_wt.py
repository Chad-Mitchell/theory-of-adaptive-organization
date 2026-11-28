# Independent reviewer re-implementation of Step 1 (WORLD-TRACK), primary arm (a=0, c_K=2). Own code.
import numpy as np, json, sys
from scipy.special import ndtr, erfcx
from scipy.ndimage import minimum_filter
SQ2=np.sqrt(2.0)
def Gneg(y):
    # G(-y) = phi(y) - y*Phibar(y), stable for y>=0 via Mills ratio; for y<0 use G(-y)=G(y)... handled by identity
    y=np.asarray(y,float); out=np.empty_like(y)
    pos=y>=0
    yp=y[pos]; ph=np.exp(-yp*yp/2)/np.sqrt(2*np.pi)
    out[pos]=ph*(1-yp*erfcx(yp/SQ2)*np.sqrt(np.pi/2))
    yn=-y[~pos]  # G(-y) with y<0 means G(|y|) = |y| + G(-|y|)
    ph=np.exp(-yn*yn/2)/np.sqrt(2*np.pi)
    out[~pos]=yn+ph*(1-yn*erfcx(yn/SQ2)*np.sqrt(np.pi/2))
    return out
def cellprobs(rho):
    # unwrapped: offset u~U(-1/2,1/2) (cell units), drift z~N(0,rho^2); P(round(u+z)=j), j>=1
    J=int(np.ceil(12*rho))+4; j=np.arange(1,J+1).astype(float)
    # P_j=(1/1)int_{-1/2}^{1/2}[Phibar((j-1/2-u)/rho)-Phibar((j+1/2-u)/rho)]du
    # int Phibar((c-u)/rho)du over u in[-1/2,1/2] = rho*[G(-(c-1/2)/rho)-G(-(c+1/2)/rho)]
    I=lambda c: rho*(Gneg((c-0.5)/rho)-Gneg((c+0.5)/rho))
    p=I(j-0.5)-I(j+0.5); p=np.clip(p,0,None)
    return p
def H_exact(n,tau):
    if n==1 or tau<=0: return 0.0
    D=2*np.pi/n; rho=tau/D
    p=cellprobs(rho); p0=1-2*p.sum()
    J=len(p)
    if J>=n//2:
        q=np.zeros(n); q[0]=p0; j=np.arange(1,J+1); np.add.at(q,j%n,p); np.add.at(q,(-j)%n,p)
    else: q=np.r_[p0,p,p]
    q=q[q>1e-300]; return float(-(q*np.log(q)).sum())
def hwrap(tau):
    # differential entropy of wrapped normal, direct numerical integration (own)
    if tau<0.3: return 0.5*np.log(2*np.pi*np.e*tau*tau)
    th=np.linspace(-np.pi,np.pi,20000,endpoint=False); f=np.zeros_like(th)
    for k in range(-20,21): f+=np.exp(-(th+2*np.pi*k)**2/(2*tau*tau))
    f/=f.sum()*(th[1]-th[0]); return float(-(f*np.log(np.maximum(f,1e-300))).sum()*(th[1]-th[0]))
def H_any(n,tau):
    D=2*np.pi/n; rho=tau/D
    if n>1 and rho>40: return min(hwrap(tau)-np.log(D)+np.log1p(1/(12*rho*rho))/2, np.log(n))
    return H_exact(n,tau)
TW=np.geomspace(0.3,60,800); HW=np.array([hwrap(t) for t in TW])
# table of h0(rho) for unwrapped large-n use
RG=np.exp(np.linspace(np.log(1e-8),np.log(40),3000)); H0=np.array([H_exact(10**9,r*2*np.pi/1e9) for r in RG])
def H_fast(n,tau):
    n=np.asarray(n,float); tau=np.asarray(tau,float); D=2*np.pi/n; rho=tau/D
    out=np.interp(np.log(np.clip(rho,1e-8,40)),np.log(RG),H0)
    big=rho>40; small_rho=rho<1e-8
    out=np.where(small_rho,0.0,out)
    if big.any():
        tb=np.broadcast_to(tau,out.shape)[big]; nb=np.broadcast_to(n,out.shape)[big]
        hv=np.where(tb<0.3,0.5*np.log(2*np.pi*np.e*np.maximum(tb,1e-300)**2),np.interp(np.log(np.clip(tb,0.3,60)),np.log(TW),HW))
        out[big]=np.minimum(hv+np.log(nb/(2*np.pi))+np.log1p(1/(12*(np.broadcast_to(rho,out.shape)[big])**2))/2,np.log(nb))
    # wrap regime for small n with tau large: use exact
    return np.where(n==1,0.0,np.minimum(out,np.log(np.maximum(n,1))))
def L(n,s,sig):
    n=np.asarray(n,float); s=np.asarray(s,float); q=np.exp(-sig*sig/2)
    sinc=np.where(n==1,0.0,np.sinc(1/np.maximum(n,1)))
    A=(1-q**s)/(s*(1-q))
    return 1-sinc*A
def J(n,s,sig,x,G,cK=2.0,H=None):
    if H is None: H=H_fast(n,sig*np.sqrt(s))
    return cK*G*np.log(n)+H/s+x*L(n,s,sig)
NG=np.unique(np.r_[np.arange(1,400),np.round(np.geomspace(400,1e7,900))])
SG=np.unique(np.r_[np.arange(1,400),np.round(np.geomspace(400,1e9,1100))])
def solve(sig,x,G):
    Hm=H_fast(NG[:,None],sig*np.sqrt(SG[None,:]))
    # exact H for small n (wrapping) where tau big
    Jm=J(NG[:,None],SG[None,:],sig,x,G,H=Hm)
    i,k=np.unravel_index(np.argmin(Jm),Jm.shape)
    lm=(Jm==minimum_filter(Jm,size=3,mode='nearest'))
    ii,kk=np.nonzero(lm&(Jm<=Jm[i,k]*(1+1e-3)))
    far=sum(1 for p,q in zip(ii,kk) if max(NG[p]/NG[i],NG[i]/NG[p])>1.2 or max(SG[q]/SG[k],SG[k]/SG[q])>1.2)
    # refine with exact H on integer neighbourhood
    n0,s0=NG[i],SG[k]
    nr=np.unique(np.round(np.r_[np.arange(max(1,n0-6),n0+7),n0*np.exp(np.linspace(-.06,.06,61))])).astype(int)
    sr=np.unique(np.round(np.r_[np.arange(max(1,s0-6),s0+7),s0*np.exp(np.linspace(-.06,.06,61))])).astype(int)
    nr=nr[nr>=1]; sr=sr[sr>=1]
    best=(np.inf,None,None)
    for n in nr:
        for s in sr:
            h=H_any(int(n),sig*np.sqrt(s)); v=float(J(n,s,sig,x,G,H=h))
            if v<best[0]: best=(v,int(n),int(s),h)
    v,n,s,h=best
    return dict(sig=sig,x=x,G=G,n=n,s=s,J=v,H=h,rho=sig*np.sqrt(s)*n/(2*np.pi),keep=2*G*np.log(n),read=h/s,loss=x*float(L(n,s,sig)),far=far,edge=bool(i==len(NG)-1 or k==len(SG)-1),coarse=(int(n0),int(s0)))
if __name__=='__main__':
    sigs=[1e-3,3e-3,1e-2,3e-2,0.1,0.3]; xs=[1,3,10,30,100,300,1e3,3e3,1e4,3e4,1e5,1e6]; Gs=[0,1e-5,1e-4,1e-3,1e-2,1e-1]
    out=open('rv_wt.jsonl','w')
    for sig in sigs:
        for G in Gs:
            for x in xs:
                r=solve(sig,x,G); out.write(json.dumps(r)+"\n"); out.flush()
        print("sig done",sig,flush=True)
