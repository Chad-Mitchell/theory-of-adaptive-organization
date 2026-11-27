# Level arm L of §6.2: tau_delta = mean exit time of the snapped record from {d(v0,.) < delta}; n <= 1201 exact.
import json, math, numpy as np, mpmath as mp
from multiprocessing import Pool
from scipy.stats import norm
SIG=[0.4,0.3,0.2,0.15,0.1,0.07,0.05,0.035,0.025,0.018,0.012,0.008,0.005,0.0035]
DEL=[0.1,0.2,0.3,0.5]; NMAX=1201
def dk(n,k):
    k=abs(k)
    if n%2: return math.sin(math.pi*k/n)/math.cos(math.pi/(2*n))
    S=n//2; return math.sin(math.pi*k/n)/(math.cos(math.pi/n) if (k-S)%2 else 1.0)
def dmin(n): return dk(n,1)
def pconf(n,s):
    a=mp.pi/n; s=mp.mpf(s); return float(1-sum(mp.ncdf((a+2*mp.pi*k)/s)-mp.ncdf((-a+2*mp.pi*k)/s) for k in range(-3,4)))
def qker(n,s,W):
    j=np.arange(-W,W+1); out=np.zeros(len(j))
    for w in range(-3,4):
        hi=(2*np.pi*j/n+np.pi/n+2*np.pi*w)/s; lo=(2*np.pi*j/n-np.pi/n+2*np.pi*w)/s
        out+=norm.cdf(hi)-norm.cdf(lo)
    return j,out
def tau_poly(args):
    n,s=args; res={}
    p=pconf(n,s)
    for dl in DEL:
        if p<1e-7: res[dl]=('big',1/p if p>0 else float('inf')); continue
        Aidx=[k for k in range(-(n//2)+1,n//2+1) if dk(n,k)<dl]
        if len(Aidx)==1: res[dl]=('exact',1/p); continue
        W=min(n//2,int(12*s*n/(2*math.pi))+3); j,q=qker(n,s,W); qd=dict(zip(j.tolist(),q.tolist()))
        pos={k:i for i,k in enumerate(Aidx)}; m=len(Aidx); Ai=np.array(Aidx)
        half=(n//2) if n%2==0 else (n-1)//2
        D=((Ai[None,:]-Ai[:,None])+half)%n-half
        qa=np.zeros(2*W+1); qa[:]=q
        Q=np.where(np.abs(D)<=W, qa[np.clip(D+W,0,2*W)], 0.0)
        mvec=np.linalg.solve(np.eye(m)-Q,np.ones(m)); res[dl]=('solve',float(mvec[pos[0]]))
    return (n,s,res)
def tau_disk(s,dl):
    a=2*math.asin(dl)
    if a/s>40: rho=0.5826; return ((a+rho*s)**2)/s**2, 'siegmund'
    M=int(60*a/s)+400; x=np.linspace(-a,a,M); h=x[1]-x[0]; w=np.full(M,h); w[0]=w[-1]=h/2
    K=norm.pdf((x[None,:]-x[:,None])/s)/s*w[None,:]
    mv=np.linalg.solve(np.eye(M)-K,np.ones(M)); return float(np.interp(0,x,mv)),'nystrom M=%d'%M
if __name__=="__main__":
    jobs=[(n,s) for n in range(3,NMAX+1) for s in SIG]
    import sys, time
    out=[]; t0=time.time()
    with Pool(8) as P:
        for i,r in enumerate(P.imap_unordered(tau_poly,jobs,chunksize=20)):
            out.append(r)
            if i%2000==0: print('progress',i,len(jobs),'%.0fs'%(time.time()-t0),flush=True)
    TAU={}
    for n,s,res in out: TAU["%d|%g"%(n,s)]={str(k):v for k,v in res.items()}
    D={}
    for s in SIG:
        for dl in DEL: D["%g|%g"%(s,dl)]=tau_disk(s,dl)
    # check Nystrom vs Siegmund at a/s ~ 20..40
    chk=[]
    for s,dl in [(0.05,0.5),(0.035,0.3),(0.025,0.2)]:
        a=2*math.asin(dl); M=int(60*a/s)+400; x=np.linspace(-a,a,M); h=x[1]-x[0]; w=np.full(M,h); w[0]=w[-1]=h/2
        K=norm.pdf((x[None,:]-x[:,None])/s)/s*w[None,:]; mv=np.linalg.solve(np.eye(M)-K,np.ones(M))
        chk.append((s,dl,float(np.interp(0,x,mv)),((a+0.5826*s)/s)**2))
    json.dump({'poly':TAU,'disk':D,'disk_check':chk},open("level_tau.json","w"))
    print("disk check (nystrom, siegmund):",chk)
