import numpy as np
from scipy.special import erfcx, ndtr
SQ2PIE=np.sqrt(2*np.pi*np.e)
def Kfun(y,tau):
    z=np.asarray(y)/tau
    phi=np.exp(-z*z/2)/np.sqrt(2*np.pi)
    mills=erfcx(z/np.sqrt(2))*np.sqrt(np.pi/2)   # Phibar/phi, z>=0
    return tau*phi*(1-z*mills)
def H_exact(n,tau,Jcap=None):
    """H(R'|R) nats, cell width 2pi/n, Gaussian drift sd tau, uniform in cell; exact up to tail z>10."""
    n=int(n); D=2*np.pi/n; rho=tau/D
    if tau<=0 or n==1: return 0.0
    J=int(np.ceil(10*rho))+3
    j=np.arange(1,J+1); a=(j-0.5)*D; b=(j+0.5)*D
    p=(Kfun(a-D/2,tau)-Kfun(a+D/2,tau)-Kfun(b-D/2,tau)+Kfun(b+D/2,tau))/D
    p=np.clip(p,0,None)
    p0=1-2*p.sum()
    if J>=n//2:  # fold
        full=np.zeros(n); full[0]+=p0
        np.add.at(full,j%n,p); np.add.at(full,(-j)%n,p)
        q=full
    else:
        q=np.r_[p0,p,p]
    q=q[q>0]; return float(-(q*np.log(q)).sum())
# wrapped-normal differential entropy table
_tg=np.exp(np.linspace(np.log(0.2),np.log(30),1500)); _hw=[]
th=np.linspace(-np.pi,np.pi,8192,endpoint=False); dth=th[1]-th[0]
for t in _tg:
    k=np.arange(-12,13)[:,None]
    f=(np.exp(-(th[None,:]+2*np.pi*k)**2/(2*t*t))/np.sqrt(2*np.pi*t*t)).sum(0)
    f=f/(f.sum()*dth)
    _hw.append(float(-(f*np.log(np.maximum(f,1e-300))).sum()*dth))
_hw=np.array(_hw)
def h_wN(tau):
    tau=np.asarray(tau,float)
    out=np.where(tau<0.2,np.log(SQ2PIE*np.maximum(tau,1e-300)),0.0)
    mid=(tau>=0.2)&(tau<=30)
    out=np.where(mid,np.interp(np.log(np.clip(tau,0.2,30)),np.log(_tg),_hw),out)
    out=np.where(tau>30,np.log(2*np.pi),out)
    return out
def H_asym(n,tau):
    n=np.asarray(n,float); D=2*np.pi/n; rho=tau/D
    return np.minimum(h_wN(tau)-np.log(D)+0.5*np.log1p(1/(12*rho*rho)), np.log(n))
# table for unwrapped exact h0(rho), used when n>404 and rho<=20
_rg=np.exp(np.linspace(np.log(1e-9),np.log(20),6000))
_h0=np.array([H_exact(10**7,r*2*np.pi/10**7) for r in _rg])
def H_tab(rho):
    return np.exp(np.interp(np.log(rho),np.log(_rg),np.log(np.maximum(_h0,1e-300))))
def H_point(n,s,sig):
    n=np.asarray(n,float); s=np.asarray(s,float)
    tau=sig*np.sqrt(s); rho=tau*n/(2*np.pi)
    out=np.zeros(np.broadcast(n,s).shape)
    nb=np.broadcast_to(n,out.shape); tb=np.broadcast_to(tau,out.shape); rb=np.broadcast_to(rho,out.shape)
    big=rb>20
    out[big]=H_asym(nb[big],tb[big])
    small=(~big)&(nb>404)
    out[small]=H_tab(rb[small])
    ex=(~big)&(nb<=404)&(nb>1)
    idx=np.argwhere(ex)
    for ii in idx:
        t=tuple(ii); out[t]=H_exact(int(nb[t]),float(tb[t]))
    out[nb==1]=0.0
    return out
def Lfun(n,s,sig,a=0):
    n=np.asarray(n,float); s=np.asarray(s,float)
    sinc=np.where(n==1,0.0,np.sin(np.pi/n)/(np.pi/n))
    q=np.exp(-sig*sig/2)
    # (1/s) sum_{u=a}^{s-1+a} q^u
    A=np.where(np.abs(1-q)<1e-15,1.0,q**a*(1-q**s)/(s*(1-q)))
    return 1-sinc*A
