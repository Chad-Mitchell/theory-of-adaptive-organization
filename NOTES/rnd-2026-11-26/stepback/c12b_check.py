# Sanity checks for C12B_ORDER.md (OBSERVED numerical; not proofs). Units kT = 1.
import numpy as np
from scipy.optimize import minimize_scalar
L=lambda e:(1-2*e)*np.log((1-e)/e)                 # telegraph / one-carrier factor (CORE:74; T63 one carrier)
h=lambda e:-(e*np.log(e)+(1-e)*np.log(1-e))         # binary entropy, nats
g4=lambda e:4*(np.log(2)-h(e))                       # T63 lower bound 4(ln2-h)
print("(a) quadratic onset near blind: L(1/2-d)/d^2 and g4(1/2-d)/d^2 -> 8")
for d in [1e-1,1e-2,1e-3]:
    print(f"   d={d:g}: {L(0.5-d)/d**2:.6f} {g4(0.5-d)/d**2:.6f}")
def eps_star(rate,w):
    r=minimize_scalar(lambda e: rate*L(e)+w*e,bounds=(1e-12,0.5),method='bounded',options={'xatol':1e-13})
    return r.x, r.fun
print("(b) binary: best error < 1/2 at every w>0 (w1=w2=0); scaling eps_keep(w;G)=eps_track(w*r/G;r)")
r,G=0.3,1.7
for w in [1e-3,1e-2,0.1,1,10]:
    et,_=eps_star(r,w); ek,_=eps_star(G,w); et2,_=eps_star(r,w*r/G)
    print(f"   w={w:g}: eps_track={et:.6f} eps_keep={ek:.6f} eps_track(w r/G)={et2:.6f}")
print("(c) Gaussian OU tracking (CORE:91-92): J(eps)=kT a (v-eps)/eps + w eps on (0,v]; onset at w1 = kT a/v")
a,v=0.4,2.0
for w in [0.9*a/v,0.99*a/v,1.01*a/v,1.1*a/v]:
    res=minimize_scalar(lambda e:a*(v-e)/e+w*e,bounds=(1e-9,v),method='bounded',options={'xatol':1e-12})
    print(f"   w/w1={w/(a/v):.2f}: eps*={res.x:.6f} (blind = {v})")
print("(d) OU carrier leak: d/dt I at small I is -2*Gamma*I under both storage conventions")
for I in [1e-1,1e-2,1e-3]:
    S=np.exp(2*I)-1
    c1=G*S/(1+S); c2=G*S       # N = s^2 convention ; total variance = s^2 convention
    print(f"   I={I:g}: loss/(2*Gamma*I) = {c1/(2*G*I):.6f} , {c2/(2*G*I):.6f}")
print("(e) Gaussian keep cost f(I)=kT G (1-e^{-2I}) + w Var e^{-2I}: holds iff w > w2 = kT G/Var")
Var=2.0
for w in [0.9*G/Var,1.1*G/Var]:
    I=np.linspace(0,5,5001); f=G*(1-np.exp(-2*I))+w*Var*np.exp(-2*I)
    print(f"   w/w2={w/(G/Var):.2f}: argmin I = {I[np.argmin(f)]:.3f}")
print(f"(f) ratio w2/w1 = (G/Var)/(a/Var) = G/a; here G/a = {G/a:.4f}")
print("(g) HYP Gaussian keep floor F(I)=2 kT G I + w Var e^{-2I}: convex; minimizer I*=max(0, 0.5 ln(w Var/(kT G)))")
for w in [0.5*G/Var,0.99*G/Var,1.01*G/Var,3*G/Var]:
    res=minimize_scalar(lambda I:2*G*I+w*Var*np.exp(-2*I),bounds=(0,20),method='bounded',options={'xatol':1e-12})
    print(f"   w/w2={w/(G/Var):.2f}: I*={res.x:.6f} closed={max(0,0.5*np.log(w*Var/G)):.6f}")
print("(h) OU relative-entropy decay rate for Gaussian p=N(m,s2) vs pi=N(0,1), relaxation G: -dD/dt / D at small offset")
for m0 in [0.1,0.01]:
    D=lambda t:0.5*(m0*np.exp(-G*t))**2   # mean offset only, variance at equilibrium
    dt=1e-6; print(f"   m0={m0}: rate/G = {-(D(dt)-D(0))/dt/D(0)/G:.6f}")
