# Independent check 1: linear tracker on the grid (reviewer's own code)
import numpy as np, sympy as sp
from scipy.optimize import brentq
def riccati_pole(lam,mu,N,D):
    a=2*lam; phi=np.exp(-a*D); Q=mu**2*(1-phi**2); R=N/D
    M=Q+1.0
    for _ in range(200000):
        P=M*R/(M+R); Mn=phi**2*P+Q
        if abs(Mn-M)<1e-15*M: break
        M=Mn
    K=M/(M+R); return (1-K)*phi
rng=np.random.default_rng(7)
for lam,mu,N,D in [(0.01,1,1,0.5),(0.002,1,9,1),(0.1,2,0.3,0.7),(0.05,1,2,3.0)]:
    z=riccati_pole(lam,mu,N,D); a=2*lam; rho=mu**2*D/N
    beta=np.arccosh(np.cosh(a*D)+rho*np.sinh(a*D))/D
    print("pole iter vs closed:",lam,mu,N,D, -np.log(z)/D, beta)
# symbolic series of beta_c/beta
D,a,b=sp.symbols('D a b',positive=True)
B2=sp.symbols('B2')
# cosh(beta D)=cosh(aD)+rho sinh(aD), rho*a*D = b D^2/2 with b=2 a mu^2/N  => rho = b D/(2a)
rhs=sp.series(sp.cosh(a*D)+b*D/(2*a)*sp.sinh(a*D),D,0,7).removeO()
# solve beta^2 = s0 + s1 D^2 + ...
s0,s1,s2=sp.symbols('s0 s1 s2')
x2=(s0+s1*D**2+s2*D**4)*D**2
lhs=sp.series(sp.cosh(sp.sqrt(x2)),D,0,7).removeO()
sol=sp.solve([sp.expand(lhs-rhs).coeff(D,k) for k in (2,4,6)],[s0,s1,s2],dict=True)[0]
print("beta^2 =",sp.factor(sol[s0]),"+",sp.factor(sol[s1]),"D^2 +...")
bc=sp.sqrt(a**2+b)
ratio=sp.series(bc/sp.sqrt(sol[s0]+sol[s1]*D**2),D,0,3).removeO()
print("beta_c/beta - 1 =",sp.simplify(ratio-1), " ; claim b^2 D^2/(24 bc^2):", sp.simplify((ratio-1)-b**2*D**2/(24*(a**2+b))))
# worst case slow world (a->0): exact ratio vs r = tau_c/D
def ratio_exact(r,a_frac):
    # bc=1 units: D=1/r, a = a_frac*bc
    bc=1.0; a=a_frac; b=bc**2-a**2; Dd=1.0/r
    if a==0: c=1+b*Dd**2/2
    else: c=np.cosh(a*Dd)+b*Dd/(2*a)*np.sinh(a*Dd)
    return bc/(np.arccosh(c)/Dd)
for r in [0.6,0.88,1,1.5,2,2.05,3,10]:
    print("r=%.2f ratio(a=0)=%.5f series=%.5f ratio(a=.5bc)=%.5f"%(r,ratio_exact(r,0),1+1/(24*r*r),ratio_exact(r,0.5)))
for tol in (0.01,0.05,0.10):
    print("slow-world threshold r for",tol, brentq(lambda r: ratio_exact(r,0)-1-tol,0.2,50))
