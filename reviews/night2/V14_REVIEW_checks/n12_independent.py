"""V14 review: independent check of THEORY v1.4 N12 (not the author's script).
Uses the formal layer's own definitions (reviews/night1/formal/THEOREMS.md T1, T5):
  h=0 onset: G(N) = N[(1+rho)^b - 1] - N^a rho^b = 0  (root by bisection, no closed form used)
  vigilance: V(N) = (p/p_g)^a N^a (rho/(1+rho))^b, equal prices
Technologies: reset reads a=b=1/alpha; precision priced ~ P^theta: a=alpha*theta/D, b=theta/D, D=alpha(theta+1)-1."""
import numpy as np
from scipy.optimize import brentq
def Nstar(a,b,rho):
    G=lambda lN: np.exp(lN)*((1+rho)**b-1)-np.exp(lN)**a*rho**b
    return np.exp(brentq(G,np.log(1+1e-9)+1e-6 if False else 1e-9,200))
def slope(f,x1,x2): return (np.log(f(x2))-np.log(f(x1)))/(np.log(x2)-np.log(x1))
techs=[]
for al in (1.5,2.0,2.5):
    techs.append((f"reset alpha={al}",1/al,1/al))
    for th in (0.5,1.0,2.0):
        D=al*(th+1)-1; techs.append((f"precision alpha={al} theta={th}",al*th/D,th/D))
print("tech | a | b | onset exponent d ln N*/d ln rho (rho 1e-6..1e-5) | small-share V(N*) exponent in rho | beyond-onset V growth exponent in N")
for name,a,b in techs:
    e=slope(lambda r: Nstar(a,b,r),1e-6,1e-5)
    eV=slope(lambda r: Nstar(a,b,r)**a*(r/(1+r))**b,1e-6,1e-5)
    gV=slope(lambda n: n**a*(1e-3/(1+1e-3))**b,1e3,1e4)
    print(f"{name:32s} a={a:.4f} b={b:.4f} onset={e:+.4f} V*(rho)={eV:+.4f} V~N^{gV:.4f}")

# Mixed technologies (formal T1 item 8): e_u -> +(1-b_m)/(1-a_L). Level = precision (theta), members = reset reads.
print("\nmixed: level precision theta=1, members reset reads: e_g=-(1-b_L)/(1-a_L), e_u=+(1-b_m)/(1-a_L)")
for al in (1.5,2.0,2.5):
    th=1.0; D=al*(th+1)-1; aL,bL=al*th/D,th/D; bm=1/al
    print(f" alpha={al}: e_g={-(1-bL)/(1-aL):+.4f}  e_u={(1-bm)/(1-aL):+.4f}  (alpha-dependent; =theta+1-1/alpha)")
print("Pi* = b^(-1/(1-a)) for reset reads:", {al: round((1/al)**(-1/(1-1/al)),4) for al in (1.5,2.0,2.5)})
