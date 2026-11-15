# Independent spot checks for TLP-EDITS-REVIEW (pick 9). nice 19.
import numpy as np
from scipy.special import k0e, k1e, exp1
from scipy import integrate
g=np.euler_gamma
def mse(k): return 2*k0e(k)/(k0e(k)+k1e(k))   # MSE/mu^2
out={}
for k in [1e-3,2.5e-4,1e-4,1/60]:
    h=1e-4; eta=(np.log(mse(k*np.exp(h)))-np.log(mse(k*np.exp(-h))))/(2*h)
    out[k]=dict(mse=mse(k), asym=2*k*(np.log(2/k)-g), eta=eta)
print("MSE closed form vs 2k[ln(2/k)-g], elasticity in kappa (=in lambda and in N):")
for k,v in out.items(): print(f"  k={k:.3g} mse={v['mse']:.6g} asym={v['asym']:.6g} ratio={v['mse']/v['asym']:.4f} eta={v['eta']:.4f} ; 2k ln(2/k) ratio={v['mse']/(2*k*np.log(2/k)):.3f}")
# homogeneity: MSE(mu,lam,N)=mu^2 f(lam N/mu^2)
mu,lam,N=1.0,1e-3,1.0; c=3.0
f=lambda mu,lam,N: mu**2*mse(lam*N/mu**2)
print("scale N and mu^2 by c:", f(mu*np.sqrt(c),lam,N*c)/f(mu,lam,N), "(c=3 => degree-1 homogeneous)")
print("scale N and lambda by c:", f(mu,lam*c,N*c)/f(mu,lam,N), "(not 3)")
# elasticities of t_A
k=1e-3; l=np.log(2/k)-g-1
print("ell",l,"1/ell",1/l,"1-1/ell",1-1/l,"-2+2/ell",-2+2/l)
# gamma+1 constant: E T = 1/2 E_{L0}[ int_0^{L0} dy e^{b}E2(b)/... ] ; do direct numeric of referee's formula independently
# T(L0) = 1/2 int_0^{L0} dy int_y^inf exp[(y-z) - k(cosh z - cosh y)] dz ; L0 ~ density ∝ exp(L - k cosh L) on L>0 (quasi-stationary)
def ET(k):
    Lmax=np.arccosh(60/k)+1
    ys=np.linspace(0,Lmax,4001)
    inner=np.array([integrate.quad(lambda z: np.exp((y-z)-k*(np.cosh(z)-np.cosh(y))),y,y+60,limit=200)[0] for y in ys])
    T=np.concatenate([[0],np.cumsum(0.5*(inner[1:]+inner[:-1])*np.diff(ys))])*0.5
    w=np.exp(ys-k*np.cosh(ys)-(ys-k*np.cosh(ys)).max())
    return np.trapezoid(T*w,ys)/np.trapezoid(w,ys)
for k in [1e-3,1e-5]:
    e=ET(k); print(f"k={k}: E T={e:.4f}; 0.5[ln(2/k)-g-1]={0.5*(np.log(2/k)-g-1):.4f}; implied const={np.log(2/k)-2*e:.4f} (g+1={g+1:.4f})")
