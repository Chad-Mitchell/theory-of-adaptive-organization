"""Independent re-derivations (reviewer). Not copied from checks/check_all.py."""
import sympy as sp, numpy as np
from scipy.optimize import minimize_scalar, brentq
print("== T1a EOQ-type check interval")
c,w,s,T=sp.symbols('c w sigma T',positive=True)
J=c/T+w*s**2*T/2
Ts=sp.solve(sp.diff(J,T),T); print("T*=",Ts, " J*=",sp.simplify(J.subs(T,Ts[0])))
print("== T1b Kalman local-level steady gain")
K,z=sp.symbols('K z',positive=True)
# P- = K r/(1-K); K P- = q  => K^2 r/(1-K)=q
Ksol=[k for k in sp.solve(sp.Eq(K**2/(1-K),z),K) if k.is_positive!=False][0]
print("K=",sp.simplify(Ksol)," series:",sp.series(Ksol,z,0,2))
print("== T1c robustness")
for m in [2,10]: print(m,(m**.5+m**-.5)/2)
# misjudged EWMA gain: steady MSE of EWMA with gain a on random walk q + noise r
def ewma_mse(a,q,r):  # prediction-error variance of x_t - m_t (filtered)
    # e_t = (1-a)(e_{t-1}+eta) - a*eps ; var = ((1-a)^2 q + a^2 r)/(1-(1-a)^2)
    return ((1-a)**2*q+a**2*r)/(1-(1-a)**2)
q,r=1e-4,1.0
Kopt=float(Ksol.subs(z,q/r)); base=ewma_mse(Kopt,q,r)
# gain misjudged: use drift estimate m*q
for m in [2,10]:
    km=float(Ksol.subs(z,m*q/r)); print("EWMA misjudged drift x",m,": +%.1f%%"%(100*(ewma_mse(km,q,r)/base-1)))
print("== T2a/T2b watcher condition")
cm,cw,e,hw=sp.symbols('c_main c_w epsilon h_w',positive=True)
print("escalation break-even eps:",sp.solve(sp.Eq(cw+e*cm,cm),e))
print("== T3a compression threshold")
N,rho=sp.symbols('N rho',positive=True)
flat=N*sp.sqrt(1+rho); nest=sp.sqrt(N*rho)+N   # both /sqrt(2cwq_u)
Nstar=sp.solve(sp.Eq(flat,nest),N); print("N* =",[sp.simplify(x) for x in Nstar])
f=lambda r:(np.sqrt(1+r)+1)**2/r
print({r:round(f(r),2) for r in [1,.5,.1]})
print("== T3b two-level clock saving")
for R in [1,2,4,10,1e6]: print(R, round(1-(1+R)/np.sqrt(2*(1+R*R)),4))
print("== T5 Cho-Garcia-Molina rise-then-fall")
f_,l=sp.symbols('f lambda',positive=True)
F=(f_/l)*(1-sp.exp(-l/f_))
print("d2F/df2 =",sp.simplify(sp.diff(F,f_,2)), " claimed -l e^{-l/f}/f^3 equal?",sp.simplify(sp.diff(F,f_,2)+l*sp.exp(-l/f_)/f_**3)==0)
print("dF/df at f->0+:",sp.limit(sp.diff(F,f_),f_,0,'+'))
mu,W,cc=1.0,10.0,1.0
def fstar(lam):
    res=minimize_scalar(lambda ff: cc*ff+mu*W*(1-(ff/lam)*(1-np.exp(-lam/ff))) if ff>1e-9 else mu*W,bounds=(1e-9,50),method='bounded')
    v0=mu*W
    return res.x if res.fun<v0-1e-9 else 0.0
print([ (lam,round(fstar(lam),2)) for lam in [0.01,1,3,5,7,9,9.9,10.1,12]])
print("== T6 Still et al: per-step identity on a toy (independent impl)")
# 2-state signal Markov chain, 2-state system with Boltzmann relaxation p(s|x) partial
import itertools
A=np.array([[.9,.1],[.2,.8]])     # x transition
px=np.array([2/3,1/3])            # stationary
beta=1.0; E=lambda s,x: 0.0 if s==x else 1.5
eq=lambda x: np.array([np.exp(-beta*E(s,x)) for s in (0,1)])/sum(np.exp(-beta*E(s,x)) for s in (0,1))
lamr=0.5   # partial relaxation toward equilibrium given current x (detailed balance with bath)
def relax(ps,x): return (1-lamr)*ps+lamr*eq(x)   # mixing with equilibrium kernel preserves detailed balance
H=lambda p: -np.sum(p[p>0]*np.log(p[p>0]))
def MI(pj): return H(pj.sum(1))+H(pj.sum(0))-H(pj.flatten())
# joint p(s,x) at t (after relaxation), start: s in equilibrium with x0
pj=np.array([[eq(x)[s]*px[x] for x in (0,1)] for s in (0,1)])
for t in range(5):
    pj=np.array([[sum(pj[s,x0]*0 for x0 in (0,1)) for x in (0,1)] for s in (0,1)]) if False else pj
    # prediction joint p(s_t, x_{t+1})
    pp=pj@A
    Imem=MI(pj); Ipred=MI(pp)
    # work on x change: W = <E(s,x_{t+1})-E(s,x_t)>; F_neq = <E> - kT H(S|X)
    Wk=sum(pj[s,x]*A[x,x2]*(E(s,x2)-E(s,x)) for s in (0,1) for x in (0,1) for x2 in (0,1))
    HSgX=lambda q: H(q.flatten())-H(q.sum(0))
    Fb=sum(pj[s,x]*E(s,x) for s in (0,1) for x in (0,1))-HSgX(pj)/beta
    Fa=sum(pp[s,x]*E(s,x) for s in (0,1) for x in (0,1))-HSgX(pp)/beta
    print(t,"beta*Wdiss=%.6f  Imem-Ipred=%.6f"%(beta*(Wk-(Fa-Fb)),Imem-Ipred))
    pj=np.array([[0.0,0.0],[0.0,0.0]])+0
    pj=np.array([relax(pp[:,x],x) for x in (0,1)]).T
print("== T7b level penalty, Roundy numbers")
D=sp.symbols('Delta',positive=True); u=sp.symbols('u')
phi=sp.integrate(sp.cosh(u)-1,(u,-D/2,D/2))/D
print("phi=",sp.simplify(phi.rewrite(sp.exp)))
print("mean@ratio2=",float(phi.subs(D,sp.log(2))+1)," edge=",float(sp.cosh(sp.log(2)/2)))
print("1/(sqrt2 ln2)=",1/(np.sqrt(2)*np.log(2))," 3/(2sqrt2)=",3/(2*np.sqrt(2)))
psi=D*phi  # objective weight is width*penalty
print("psi''=",sp.simplify(sp.diff(psi,D,2)), " phi''(0)=",sp.limit(sp.diff(phi,D,2),D,0))
print("== T7b K* scaling: C L^2/(24K^2)+K h")
Cc,L,h,Kk=sp.symbols('C L h K',positive=True)
print(sp.solve(sp.diff(Cc*L**2/(24*Kk**2)+Kk*h,Kk),Kk))
print("== T7c exponent")
n,g,d,Hh=sp.symbols('n gamma delta H',positive=True)
print(sp.simplify(sp.log(sp.sqrt(n**g/(n**d*n**(2*Hh))))/sp.log(n)))
print("== T4 local exponents of K(N) at q/r=1e-3")
Kf=lambda zz:(-zz+np.sqrt(zz*zz+4*zz))/2
Ns=np.array([1,4,16,64,256,1024.]); Kv=Kf(1e-3*Ns)
print(np.round(np.diff(np.log(Kv))/np.diff(np.log(Ns)),3), "K range",Kv[0],Kv[-1])
print("== Adler slip & Kuramoto threshold quick")
dw,KK=1.0,0.6; print("slip rate theory",np.sqrt(dw**2-KK**2))
print("== watcher crossover (E3) log-interp")
x=np.log([.3,1]); y=np.log([.805,1.512]); print("r_w*~",np.exp(np.interp(0,y,x)))
