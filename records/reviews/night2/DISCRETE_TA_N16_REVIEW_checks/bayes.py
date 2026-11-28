# Independent check 2-4: Bayes (Wonham) t_A on a grid, reviewer's own Nystrom solver (theta=1 units, mu=1, N=1, lambda=kappa, Delta=rho)
import numpy as np, sys, json
from scipy.integrate import quad
from scipy.special import k0,k1,zeta
from numpy.polynomial.legendre import leggauss
EG=np.euler_gamma
C1=-zeta(0.5)/np.sqrt(2*np.pi)
def plugin(k): return 0.5*(np.log(2/k)-EG-1)
# ---- continuous: T(y)=int_0^y g, g(y)=1/2 int_y^inf exp(Phi(y)-Phi(z))dz ; t_A = int_0^inf g(y) P(L0>y) dy
def cont_ta(k,law):
    Phi=lambda L: L+k*np.cosh(L)
    def g(y): return 0.5*quad(lambda z: np.exp(Phi(y)-Phi(z)),y,np.inf,limit=200,epsabs=1e-13,epsrel=1e-12)[0]
    if law=='quiet': dens=lambda L: np.exp(L-k*np.cosh(L))/(2*k1(k))
    else: dens=lambda L: (1+np.exp(L))*np.exp(-k*np.cosh(L))/(2*(k0(k)+k1(k)))
    Lhi=np.log(2/k)+8
    tail=lambda y: quad(dens,y,Lhi+20,limit=200,epsabs=1e-14)[0]
    return quad(lambda y: g(y)*tail(y),0,Lhi+10,limit=400,epsabs=1e-12,epsrel=1e-11)[0]
# ---- discrete
def nodes(a,b,pw,m):
    x,w=leggauss(m); n=int(np.ceil((b-a)/pw)); e=np.linspace(a,b,n+1)
    X=((e[:-1,None]+e[1:,None])/2+(e[1:,None]-e[:-1,None])/2*x).ravel()
    W=((e[1:,None]-e[:-1,None])/2*w).ravel(); return X,W
def grid_ta(k,rho,law,pw_fac=0.4,m=10,pad=9.0):
    lam,D=k,rho; p=(1-np.exp(-2*lam*D))/2
    f=lambda L: np.logaddexp(np.log1p(-p)+L,np.log(p))-np.logaddexp(np.log(p)+L,np.log1p(-p))
    sd=2*np.sqrt(rho); pw=pw_fac*sd
    Lmax=np.log(2/k)+pad
    gk=lambda v,mean: np.exp(-0.5*((v-mean)/sd)**2)/(sd*np.sqrt(2*np.pi))
    # start law
    if law=='quiet':
        a0=-12.0
        n1=int(np.ceil((0-a0)/pw)); n2=int(np.ceil(Lmax/pw))
        X1,W1=nodes(a0,0,(0-a0)/n1,m); X2,W2=nodes(0,Lmax,Lmax/n2,m)
        X=np.r_[X1,X2]; W=np.r_[W1,W2]
        K=gk(X[:,None],f(X)[None,:]+2*rho)*W[None,:]
    else:
        n2=int(np.ceil(Lmax/pw)); X2,W2=nodes(0,Lmax,Lmax/n2,m)
        X=np.r_[-X2[::-1],X2]; W=np.r_[W2[::-1],W2]
        # p+(v)=int[(1-p)p+(u)+p p+(-u)] k+(v|f(u))du ; p+(-u) at node j is p+ at mirrored node
        Kb=gk(X[:,None],f(X)[None,:]+2*rho)*W[None,:]
        n=len(X); J=np.arange(n)[::-1]
        K=(1-p)*Kb+p*Kb[:,J]  # since W symmetric, mirrored weight equal
    A=np.eye(len(X))-K; A[-1,:]=W; bvec=np.zeros(len(X)); bvec[-1]=1
    P=np.linalg.solve(A,bvec)
    # hitting: h(u)=1+int_0^inf h(v)k-(v|f(u))dv on positive nodes
    pos=X>0; Xp=X[pos]; Wp=W[pos]
    Kh=gk(Xp[None,:],f(Xp)[:,None]-2*rho)*Wp[None,:]
    h=np.linalg.solve(np.eye(len(Xp))-Kh,np.ones(len(Xp)))
    En=np.sum(P[pos]*W[pos]*h)
    return D*En, np.sum(P*W*(X<=0))
if __name__=="__main__":
    out={}
    task=sys.argv[1]
    if task=="cont":
        for k in [0.1,0.03,0.01,1e-3,1e-4,1e-6]:
            q=cont_ta(k,'quiet'); s=cont_ta(k,'switch'); P=plugin(k)
            out[str(k)]=dict(quiet=q,switch=s,plugin=P)
            print(k,"plugin %.4f quiet/pl %.5f switch/pl %.5f  (q-s)/pl %.5f  k ln(1/k) %.5f"%(P,q/P,s/P,(q-s)/P,k*np.log(1/k)),flush=True)
    elif task=="mccells":
        # report MC/lattice cells in report units: mu=1,Delta=1,N=sigma^2 -> theta=N, rho=1/N, kappa=lam*N ; time in theta units *N
        for law,lam,N,ref in [('quiet',0.002,9,16.315),('quiet',0.0005,36,61.101),('switch',0.002,9,15.569),('switch',0.01,2.25,4.2458)]:
            t,_=grid_ta(lam*N,1/N,law); print(law,lam,N,"mine %.4f report-lattice %.4f"%(t*N,ref),flush=True)
    elif task=="conv":
        k=float(sys.argv[2]); rho=float(sys.argv[3])
        for pf,m,pad in [(0.4,10,9),(0.25,12,12),(0.15,14,14)]:
            t,_=grid_ta(k,rho,'quiet',pf,m,pad); print(k,rho,pf,m,pad,"%.9f"%t,flush=True)
