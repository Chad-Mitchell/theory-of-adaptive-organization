# Monte Carlo check of D1 heat formula Qdot = a*g*s*kT/(a+g)... via Sekimoto heat on the memory bath.
import numpy as np
rng = np.random.default_rng(7)
a,v,kT = 1.0,1.0,1.0
mu,kap,lam = 2.0,2.5,2.5*0.8        # g = mu*kap = 5, r = 0.8
g = mu*kap
dt, T, M = 2e-4, 400.0, 64          # M independent chains
n = int(T/dt)
x = rng.normal(0,np.sqrt(v),M); m = np.zeros(M)
heat = np.zeros(M); burn = int(20/dt); e2=[]; cov=np.zeros(3); cnt=0
for i in range(n):
    F = -kap*m + lam*x
    dW1 = rng.normal(0,np.sqrt(dt),M); dW2 = rng.normal(0,np.sqrt(dt),M)
    xn = x - a*x*dt + np.sqrt(2*a*v)*dW1
    mn = m + mu*F*dt + np.sqrt(2*mu*kT)*dW2
    if i>burn:
        Fmid = -kap*(m+mn)/2 + lam*(x+xn)/2     # Stratonovich midpoint
        heat += Fmid*(mn-m)                      # heat delivered to memory bath = F o dm
        cov += np.array([np.mean(x*x),np.mean(x*m),np.mean(m*m)]); cnt+=1
    x,m = xn,mn
Tm = (n-burn-1)*dt
Qsim = heat.mean()/Tm; se = heat.std()/Tm/np.sqrt(M)
s = kap*(lam/kap)**2*v/kT
Qth = a*g*s*kT/(a+g)
cov/=cnt; epssim = cov[0]-cov[1]**2/cov[2]
epsth = v*(a**2+2*a*g+a*g*s+g**2)/((a+g)*(a+g+g*s))
print(f"Qdot sim {Qsim:.4f} +- {se:.4f}  theory {Qth:.4f}")
print(f"eps  sim {epssim:.4f}  theory {epsth:.4f}")
n_ = 1+g/a; print("theory via R(u):", kT*a*n_*(v-epsth)/(n_*epsth-v))
