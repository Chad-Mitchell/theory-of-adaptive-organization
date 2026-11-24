# Reviewer check for PR #248 (section 9), written independently of info_reads.py: own asymmetric-Laplace-plus-Gaussian density (erfcx-stabilized), own entropy quadrature, own multistart.
# Usage: python3 review_pr248_indep.py KAPPA LAMBDA MULT  (MULT x 4 kappa/lambda nats). Slow (minutes per case). Outputs stored in review_pr248_indep.out.
# Independent reviewer check of CLOCK_TERM section 9 (own code, not info_reads.py)
import numpy as np, warnings
from scipy.special import log_ndtr
from scipy.optimize import brentq, minimize
from scipy.integrate import quad
warnings.filterwarnings("ignore")
LN=np.log(2*np.pi*np.e)
from scipy.special import erfcx
def _lt(x,sc,v):
    # log[ exp(v/(2 sc^2) - x/sc) * Phi(x/s - s/sc) ], stable
    s=np.sqrt(v); z=s/sc - x/s
    out=np.empty_like(x)
    pos=z>0
    out[pos]=-x[pos]**2/(2*v)+np.log(erfcx(z[pos]/np.sqrt(2))/2)
    out[~pos]=v/(2*sc*sc)-x[~pos]/sc+log_ndtr(-z[~pos])
    return out
def logp(x,sp,sm,v):
    L=-np.log(sp+sm); t1=L+_lt(x,sp,v)
    if sm<=0: return t1
    return np.logaddexp(t1,L+_lt(-x,sm,v))
def h(mu,sig2,v,n=40001):
    R=np.sqrt(mu*mu+2*sig2); sp=(R+mu)/2; sm=sig2/(2*sp)
    s=np.sqrt(v); lo=-(40*sm+12*s); hi=40*sp+12*s
    x=np.linspace(lo,hi,n); lp=logp(x,sp,sm,v); p=np.exp(lp)
    return -np.trapezoid(np.where(p>0,p*lp,0.0),x)
def I(mu,sig2,r):
    v=h(mu,sig2,2*r)-0.5*np.log(2*np.pi*np.e*r)
    return v if np.isfinite(v) and v>=0 else 1e6
# (A) closed-form h(AL) sanity via MC
rng=np.random.default_rng(1); mu,s2=0.7,0.1
sp=(np.sqrt(mu*mu+2*s2)+mu)/2; sm=s2/(2*sp)
print("h_AL closed",1+0.5*np.log(mu*mu+2*s2),"quad tiny-noise",h(mu,s2,1e-7)-0.0)
r=1e-4
for mu in [0.02,0.05,0.2]:
    e=1e-6*mu*mu
    a=mu*(I(mu*(1+1e-4),0,r)-I(mu*(1-1e-4),0,r))/(2e-4*mu)
    b=mu*mu*(I(mu,e,r)-I(mu,0,r))/e
    print(f"mu/sqrt(2r)={mu/np.sqrt(2*r):.2f} I0={I(mu,0,r):.4f} a={a:.5f} b={b:.5f} b/a={b/a:.5f}")
# (B) global onset: pick f0 with I0 = target, set w by stationarity, then optimize full J
def run(kap,lam,mult,r=1e-4):
    tgt=mult*4*kap/lam
    f0=brentq(lambda f:I(1/f,0,r)-tgt,1e-3,1/np.sqrt(r)*0.9)
    mu0=1/f0; d=1e-4*mu0
    a=mu0*(I(mu0+d,0,r)-I(mu0-d,0,r))/(2*d)
    w=lam*(tgt-a)*f0**3/2
    J0=lambda f: lam*f*I(1/f,0,r)+w*(r+1/f**2)
    def J(p):
        f=np.exp(p[0]); wp=1/(1+np.exp(-p[1])); D=np.exp(p[2])
        mu=(1-wp)/f; s2=2*D/f
        return kap*wp*wp/D+lam*f*I(mu,s2,r)+w*(r+mu*mu+s2)
    best=(J0(f0),0.0)
    for wp0 in [0.02,0.05,0.1,0.2,0.4]:
        for Dl in [-14,-11,-8,-5]:
            res=minimize(J,[np.log(f0),np.log(wp0/(1-wp0)),Dl],method="Nelder-Mead",options=dict(xatol=1e-9,fatol=1e-12,maxiter=4000))
            if res.fun<best[0]: best=(res.fun,1/(1+np.exp(-res.x[1])))
    return tgt,J0(f0),best
import sys
if len(sys.argv)>1:
  kap,lam,m=map(float,sys.argv[1:4])
  if True:
    if True:
        tgt,j0,b=run(kap,lam,m)
        print(f"kap={kap} lam={lam} I0={tgt:.3f} ({m}x) J0={j0:.6f} Jbest={b[0]:.6f} clockfrac={b[1]:.4f} gain={(j0-b[0])/j0:.2e}")
