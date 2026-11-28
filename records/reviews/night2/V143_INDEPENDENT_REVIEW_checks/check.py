# Independent checks for THEORY v1.4.3 (v143 independent reviewer; own code, not the referee's or TLP_EDITS_REVIEW's).
# Units mu=1, N=1 unless stated; kappa = lam*N/mu^2.
import numpy as np, mpmath as mp
from scipy import integrate
g=float(mp.euler); out={}
# 1. MSE via the stationary density of x = E[y|F]/mu, derived here from the Wonham SDE in x:
#    dx = -2 lam x dt + (1-x^2)(mu/N) dnu  =>  rho(x) ∝ (1-x^2)^-2 exp(-2 kappa/(1-x^2)); MSE/mu^2 = E[1-x^2].
#    Substitute u = 1/(1-x^2) is avoided; integrate in x with mpmath (1-D only).
mp.mp.dps=25
def mse_x(k):
    f=lambda x: mp.exp(-2*k/(1-x**2))/(1-x**2)**2
    pts=[-1,-1+1e-3,-0.5,0,0.5,1-1e-3,1]
    return mp.quad(lambda x: f(x)*(1-x**2),pts)/mp.quad(f,pts)
def mse_bessel(k): return 2*mp.besselk(0,k)/(mp.besselk(0,k)+mp.besselk(1,k))
for k in [1e-1,1e-2,1e-3,1e-4]:
    a=mse_x(k); b=mse_bessel(k); asym=2*k*(mp.log(2/k)-g)
    out[f"MSE k={k}: density-quad, Bessel, Bessel/2k[ln(2/k)-g]"]=(float(a),float(b),float(b/asym))
for k in [1e-3,2.5e-4,1e-4]:
    out[f"MSE elasticity in kappa (=lam,=N) k={k}"]=float(mp.diff(lambda lk: mp.log(mse_bessel(mp.e**lk)), mp.log(k)))
# 2. t_A: mean first passage of the log-odds L to 0 after a +mu -> -mu switch.
#    dL = (2mu/N) ds - 2 lam sinh L dt (derived: L = log ratio of unnormalised Zakai densities)
#    under y=-1: drift -2 - 2k sinh L, sigma^2 = 4; scale density exp(y + k cosh y);
#    T'(y) = 1/2 ∫_y^inf exp[phi(z)-phi(y)] dz, phi(z) = -z - k cosh z.
#    Start law EXACT (no large-L approx): stationary L-density cosh^2(L/2) e^{-k cosh L} times P(y=+|L) = 1/(1+e^-L);
#    L0 < 0 contributes T = 0 (estimate already on the new side).
def tA(k,n=400001):
    Lmax=np.arccosh(80/k); y=np.linspace(0,Lmax,n)
    phi=-y-k*np.cosh(y)
    ez=np.exp(phi)
    tail=np.concatenate([integrate.cumulative_trapezoid(ez[::-1],-y[::-1],initial=0)[::-1]])  # ∫_y^Lmax e^phi
    Tp=0.5*tail*np.exp(-phi)
    Lf=np.linspace(-Lmax,Lmax,2*n-1)
    w=np.cosh(Lf/2)**2*np.exp(-k*np.cosh(Lf))/(1+np.exp(-Lf))
    Z=integrate.trapezoid(w,Lf)
    wp=w[n-1:]  # L>=0
    surv=integrate.cumulative_trapezoid(wp[::-1],-y[::-1],initial=0)[::-1]/Z  # P(L0>y)
    return integrate.trapezoid(Tp*surv,y)
for k in [5e-2,1e-2,1e-3,1e-4,1e-5,1e-6]:
    t=tA(k); c=float(np.log(2/k))-2*t
    out[f"t_A k={k}: quad, leading (1/2)[ln(2/k)-g-1], implied const (g+1={g+1:.4f})"]=(t,0.5*(np.log(2/k)-g-1),c)
# 3. elasticities of leading t_A = (N/2mu^2) l, l = ln(2mu^2/(lam N)) - g - 1 (finite differences)
def tlead(lam,N,mu): return N/(2*mu**2)*(np.log(2*mu**2/(lam*N))-g-1)
lam,N,mu,h=1e-3,1.0,1.0,1e-6; f0=np.log(tlead(lam,N,mu))
out["t_A elasticities numeric (switching time 1/lam, N, mu) at k=1e-3"]=(
 -(np.log(tlead(lam*(1+h),N,mu))-f0)/np.log(1+h),(np.log(tlead(lam,N*(1+h),mu))-f0)/np.log(1+h),(np.log(tlead(lam,N,mu*(1+h)))-f0)/np.log(1+h))
l=np.log(2/1e-3)-g-1
out["formula 1/l, 1-1/l, -2+2/l"]=(1/l,1-1/l,-2+2/l); out["l at k=1e-3"]=l
# also the elasticity of the exact (quadrature) t_A in kappa at 1e-3 (switching-time elasticity = d ln t/d ln(1/lam))
out["exact-quad switching-time elasticity at k=1e-3"]=-(np.log(tA(1e-3*1.01))-np.log(tA(1e-3)))/np.log(1.01)
# 4. homogeneity: MSE(lam,N,mu) = mu^2 f(lam N/mu^2)
def MSE(lam,N,mu): return mu**2*float(mse_bessel(lam*N/mu**2))
b=MSE(1e-3,1,1)
out["Bayes: scale N and mu^2 by 3 -> MSE ratio"]=MSE(1e-3,3,np.sqrt(3))/b
out["Bayes: scale N and lam by 3 -> MSE ratio"]=MSE(3e-3,3,1)/b
ML=lambda lam,N,mu: 2*mu*np.sqrt(lam*N)
out["linear 2mu sqrt(lam N): (N,mu^2)x3, (N,lam)x3"]=(ML(1e-3,3,np.sqrt(3))/ML(1e-3,1,1),ML(3e-3,3,1)/ML(1e-3,1,1))
for kk,v in out.items(): print(kk,"=>",v)
