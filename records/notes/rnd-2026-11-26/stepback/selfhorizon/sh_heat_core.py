# SH-heat core (SELF_HORIZON §8; pre-statement hash logged in WORKLOG 14:25 ET before this file was written).
import math, numpy as np, mpmath as mp
from scipy.stats import norm
SIG=[0.4,0.3,0.2,0.15,0.1,0.07,0.05,0.035,0.025,0.018,0.012,0.008,0.005,0.0035]
XS=[0.005,0.01,0.02,0.05,0.1,0.2,0.5,1.0]
CK=[2.0,4.0]; SMAX=4000
def pconf_mp(n,s):
    a=mp.pi/n; s=mp.mpf(s); mp.mp.dps=50
    return 1-sum(mp.ncdf((a+2*mp.pi*k)/s)-mp.ncdf((-a+2*mp.pi*k)/s) for k in range(-4,5))
def arcmass(lo,hi):
    # P(lo<Z<hi), Z std normal, accurate in tails
    lo=np.asarray(lo); hi=np.asarray(hi)
    out=np.where(lo>0, norm.sf(lo)-norm.sf(hi), np.where(hi<0, norm.cdf(hi)-norm.cdf(lo), norm.cdf(hi)-norm.cdf(lo)))
    return out
def kernel(n,s):
    """q_j for j=0..n-1 (index mod n), wrapped normal snapped to nearest vertex; plus log-mass of the nearest arcs."""
    W=min(n//2, int(14*s*n/(2*math.pi))+3)
    j=np.arange(-W,W+1); q=np.zeros(len(j))
    for w in range(-4,5):
        hi=(2*np.pi*j/n+np.pi/n+2*np.pi*w)/s; lo=(2*np.pi*j/n-np.pi/n+2*np.pi*w)/s
        q+=arcmass(lo,hi)
    full=np.zeros(n)
    for jj,qq in zip(j,q): full[jj%n]+=qq if not (n%2==0 and jj==-(n//2) and W==n//2) else 0.0
    return full
def tail_logs(n,s):
    """log q_j for j=+-1 (first neighbours) for the first-order regime when p underflows."""
    lo=(np.pi/n)/s; hi=(3*np.pi/n)/s
    l=norm.logsf(lo)+np.log1p(-np.exp(norm.logsf(hi)-norm.logsf(lo)))
    return l  # q_1 = q_{-1} = exp(l) (next arcs negligible relative, ratio exp(-(hi^2-lo^2)/2))
def lampow(a,t):
    # (1-a)^t, accurate for a near 0 and valid for lambda=1-a <= 0 (a >= 1)
    lam=1-a; out=np.empty_like(a)
    near=a<0.5
    out[near]=np.exp(t*np.log1p(-a[near]))
    out[~near]=np.power(lam[~near],t)
    return out
class Rec:
    def __init__(self,n,s):
        self.n=n; self.s=s
        self.q=kernel(n,s); self.q[0]=0.0
        self.p=float(self.q.sum())
        self.pmp=pconf_mp(n,s)
        k=np.arange(n); jj=np.arange(n)
        nz=np.nonzero(self.q)[0]
        if len(nz):
            self.a=(2*np.sin(np.pi*np.outer(k,nz)/n)**2)@self.q[nz]   # 1-lambda_k
        else: self.a=np.zeros(n)
        self.cache={}
        # first-order constants
        if self.p>0:
            qt=self.q[nz]/self.p; self.hq=float(-(qt*np.log(qt)).sum()); self.logp=math.log(self.p)
        else:
            self.hq=math.log(2.0); self.logp=float(tail_logs(n,s))+math.log(2.0)
    def HE(self,t):
        """returns (H(K_t)/p, E(t)/p) with E(t)=sum_{u=0}^{t-1} eps(u); both divided by p for range."""
        if t in self.cache: return self.cache[t]
        if self.p==0 or t*self.p<1e-6:
            H=t*(1-math.log(t)-self.logp+self.hq); E=t*(t-1)/2.0
            r=(H,E,'fo')
        else:
            a=self.a[1:]; m=t-1
            sm=m*a<1e-4
            f=np.empty_like(a)
            f[sm]=a[sm]*m*(m+1)/2-a[sm]**2*(m+1)*m*(m-1)/6
            aa=a[~sm]; f[~sm]=m-(1-aa)*(1-lampow(aa,m))/aa
            E=f.sum()/self.n
            lam_t=lampow(self.a,t)
            row=np.fft.fft(lam_t).real/self.n
            row=np.clip(row,0,None); row/=row.sum()
            nzr=row[row>0]; H=float(-(nzr*np.log(nzr)).sum())
            r=(H/self.p,E/self.p,'ex')
        self.cache[t]=r; return r
    def best_check(self,x):
        grid=sorted(set([int(round(v)) for v in np.geomspace(1,SMAX,80)])|set(range(1,11))|{max(1,math.floor(2/x)),math.ceil(2/x)})
        grid=[g for g in grid if 1<=g<=SMAX]
        J=lambda t:(self.HE(t)[0]+x*self.HE(t)[1])/t
        b=min(grid,key=J)
        w=3+int(0.05*b)
        for t in range(max(1,b-w),min(SMAX,b+w)+1): self.HE(t)
        cand=[t for t in self.cache]
        b=min(cand,key=J)
        return b, J(b)   # J in units of p (per tick, kT units / p)
def modes(R,x,ck):
    """cost per tick in kT units: keep, check, fade; returns dict"""
    n=R.n; s=R.s
    keep=ck*(s*s/2)*math.log(n)
    sb,jb=R.best_check(x)
    # check cost = p * jb ; if p underflows use log
    if R.p>0: chk=R.p*jb; logchk=None
    else: chk=0.0; logchk=R.logp+math.log(max(jb,1e-300))
    fade=x*(1-1/n)
    return {'keep':keep,'check':chk,'logcheck':logchk,'s_star':sb,'fade':fade}
