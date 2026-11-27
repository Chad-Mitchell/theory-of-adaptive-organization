from wt_core import *
import time
# continuity at rho=20
for n in [10,50,405,1000,10**5]:
    tau=20*2*np.pi/n
    print("rho=20 n",n,"exact",H_exact(n,tau),"asym",float(H_asym(n,tau)),"diff",H_exact(n,tau)-float(H_asym(n,tau)))
# table vs exact
for r in [1e-6,1e-3,0.05,0.3,1,5,19.9]:
    print("tab rho",r,float(H_tab(np.array([r]))[0]),H_exact(10**6,r*2*np.pi/1e6))
# small-rho asymptote p ln(1/p): p ~ rho*sqrt(2/pi)
for r in [1e-4,1e-6]: print("rho",r,"H",H_exact(10**6,r*2*np.pi/1e6),"p*sqrt",r*np.sqrt(2/np.pi))
print("Monte Carlo check H for n=7, tau=0.5:")
rng=np.random.default_rng(1); N=4000000; D=2*np.pi/7
t=rng.uniform(-D/2,D/2,N); z=t+0.5*rng.standard_normal(N)
c=np.round(z/D).astype(int)%7; p=np.bincount(c,minlength=7)/N; p=p[p>0]
print(" MC",-(p*np.log(p)).sum()," exact",H_exact(7,0.5))
