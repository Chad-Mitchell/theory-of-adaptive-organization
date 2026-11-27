import numpy as np
from scipy.special import roots_laguerre, gammaln, xlogy
from scipy.integrate import quad, solve_ivp
NMAX=40
XL,WL=roots_laguerre(200)
def binom_pmf(n,p):
    k=np.arange(n+1)
    lc=gammaln(n+1)-gammaln(k+1)-gammaln(n-k+1)
    p=np.clip(p,1e-300,1-1e-16)
    return np.exp(lc+xlogy(k,p)+xlogy(n-k,1-p))
def pk_given_x1(n,r,f,G,u):
    flip=(1-np.exp(-2*r*u))/2; keep=(1+np.exp(-G*u))/2
    # X=1: W=1 w.p. 1-flip -> cell=1 w.p. keep ; W=0 w.p. flip -> cell=1 w.p. 1-keep
    return (1-flip)*binom_pmf(n,keep)+flip*binom_pmf(n,1-keep)
def Itab(r,f,G,nmax=NMAX,adaptive=False):
    out=np.zeros(nmax+1)
    for n in range(1,nmax+1):
        if adaptive:
            P1=np.array([quad(lambda u: f*np.exp(-f*u)*pk_given_x1(n,r,f,G,u)[k],0,np.inf,epsabs=1e-13,epsrel=1e-12,limit=400)[0] for k in range(n+1)])
        else:
            u=XL/f
            P1=sum(WL[i]*pk_given_x1(n,r,f,G,u[i]) for i in range(len(XL)))
        P0=P1[::-1]  # symmetry: X=0 mirrors counts
        Pk=0.5*(P1+P0)
        I=0.5*np.sum(xlogy(P1,P1)-xlogy(P1,Pk))+0.5*np.sum(xlogy(P0,P0)-xlogy(P0,Pk))
        out[n]=I
    return out
def ess(I_list,c,G,R,s,nu=1.0,m=0.02):
    K=len(I_list); ns=np.arange(NMAX+1)
    def best(B):
        res=[]
        for k in range(K):
            v=nu*I_list[k]-c[k]*G*ns/B
            n=int(np.argmax(v)); res.append((n,v[n]-m))
        return res
    def resid(B):
        tot=G*B
        for (n,gv) in best(B):
            if gv>0 and n>0: tot+=G*n*gv/s
        return tot-R
    lo,hi=1e-12,R/G
    for _ in range(200):
        mid=np.sqrt(lo*hi)
        if resid(mid)>0: hi=mid
        else: lo=mid
    B=np.sqrt(lo*hi); br=best(B)
    N=[(gv/s if (gv>0 and n>0) else 0.0) for (n,gv) in br]
    return B,[n for n,_ in br],N
def Bstar_single(I,c,G,nu=1.0,m=0.02):
    ns=np.arange(NMAX+1)
    lo,hi=1e-12,1e6
    def ok(B): return np.max(nu*I-c*G*ns/B)-m>=0
    if not ok(hi): return np.inf
    for _ in range(200):
        mid=np.sqrt(lo*hi)
        if ok(mid): hi=mid
        else: lo=mid
    return hi
def run_dyn(I_list,c,G,R,s,T=2e4,mu=1e-4,nu=1.0,m=0.02,pools=None,D=0.0):
    """pools: list assigning lineage->pool index; R list per pool"""
    K=len(I_list); L=NMAX+1; ns=np.arange(L)
    if pools is None: pools=[0]*K; Rs=[R]
    else: Rs=R
    P=max(pools)+1
    Iarr=np.array(I_list)
    def rhs(t,y):
        N=np.maximum(y[:K*L].reshape(K,L),0); B=np.maximum(y[K*L:],1e-300)
        dN=np.empty_like(N); dB=np.array([Rs[p]-G*B[p] for p in range(P)],float)
        for k in range(K):
            p=pools[k]; Nk=N[k].sum()
            g=nu*Iarr[k]-m-c[k]*G*ns/B[p]-s*Nk
            lap=np.zeros(L); lap[1:]+=N[k,:-1]; lap[:-1]+=N[k,1:]; lap-=2*N[k]
            lap[0]+=N[k,0]; lap[-1]+=N[k,-1]   # reflecting ends
            dN[k]=N[k]*g+mu*lap
            dB[p]-=G*np.dot(ns,N[k])
        if P==2 and D>0:
            dB[0]+=D*(B[1]-B[0]); dB[1]+=D*(B[0]-B[1])
        return np.concatenate([dN.ravel(),dB])
    y0=np.concatenate([np.tile(np.r_[np.full(11,0.1/11),np.zeros(L-11)],K),[Rs[p]/G for p in range(P)]])
    sol=solve_ivp(rhs,(0,T),y0,method='LSODA',rtol=1e-8,atol=1e-14)
    y=sol.y[:,-1]; N=np.maximum(y[:K*L].reshape(K,L),0); B=y[K*L:]
    d=rhs(T,y); dN=d[:K*L].reshape(K,L)
    mask=N>1e-6
    stat=float(np.max(np.abs(dN[mask]/N[mask]))) if mask.any() else 0.0
    return N,B,stat,sol.success
def modes(Nk):
    tot=Nk.sum(); 
    if tot<=1e-6: return []
    pk=[]
    for n in range(len(Nk)):
        l=Nk[n-1] if n>0 else -1; r=Nk[n+1] if n<len(Nk)-1 else -1
        if Nk[n]>l and Nk[n]>=r and Nk[n]>0.1*tot: pk.append(n)
    return pk
