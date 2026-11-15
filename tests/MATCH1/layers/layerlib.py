import numpy as np
from scipy.optimize import nnls
def logbin_counts(lag,num,den,per_decade=10):
    lag=np.asarray(lag,float); e=np.logspace(np.log10(lag.min()),np.log10(lag.max()+1),int(np.ceil(per_decade*np.log10((lag.max()+1)/lag.min())))+1)
    t=[];f=[]
    for a,b in zip(e[:-1],e[1:]):
        m=(lag>=a)&(lag<b)
        if m.sum()==0: continue
        N=num[m].sum(); D=den[m].sum()
        if N<=0 or D<=N: continue
        p=N/D; t.append(np.average(lag[m],weights=den[m])); f.append(p/(1-p))
    return np.array(t),np.array(f)
def fitK(t,f,K):
    best=(np.inf,None)
    tmin=t.min(); 
    for r in np.geomspace(2,30,15):
        for tau1 in np.geomspace(tmin/3,tmin*10,12):
            taus=tau1*r**np.arange(K)
            A=np.exp(-t[:,None]/taus[None,:])/f[:,None]
            a,_=nnls(A,np.ones_like(f))
            fm=np.exp(-t[:,None]/taus[None,:])@a
            if np.any(fm<=0): continue
            rms=np.sqrt(np.mean((np.log10(fm)-np.log10(f))**2))
            if rms<best[0]: best=(rms,dict(r=float(r),tau1=float(tau1),amps=a.tolist()))
    return best
def Kstar(t,f,tol=0.02,Kmax=10):
    for K in range(1,Kmax+1):
        rms,p=fitK(t,f,K)
        if rms<=tol: return K,rms
    return Kmax+1,rms
def span_series(t,f,spans=(1,1.5,2,2.5,3)):
    out=[]
    t0=t.min()
    for s in spans:
        m=t<=t0*10**s
        if t[m].max()<t0*10**(s-0.1): break   # curve doesn't reach this span
        K,rms=Kstar(t[m],f[m]); out.append(dict(span=s,K=K,rms=float(rms),nbins=int(m.sum())))
    return out
