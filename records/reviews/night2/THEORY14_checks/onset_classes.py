"""THEORY v1.4 §2.5 check (self-check, not refereed): pooling-onset exponent -(1-b)/(1-a) for the two
sensing technologies of the tracking layer.
 reset reads (THEORY §2.2, SPECTRUM_MAP Thm 1): a = b = 1/alpha
 precision-priced continuous sensing, linear price (Cor 2'): a = alpha/(2 alpha - 1), b = 1/(2 alpha - 1)
Also: formal Lemma 1(iii) A_theta (Brownian) at theta = 1 equals Cor 2' at alpha = 2; and numeric confirmation
that minimized cost c'P + W q^(1/alpha) P^-(1-1/alpha) has elasticities (a, b) in (W, q)."""
import sympy as sp, numpy as np
from scipy.optimize import minimize_scalar
al, th = sp.symbols('alpha theta', positive=True)
a_r = b_r = 1/al
print("reset reads onset exponent:", sp.simplify(-(1-b_r)/(1-a_r)))
a_p, b_p = al/(2*al-1), 1/(2*al-1)
print("precision-priced onset exponent:", sp.simplify(-(1-b_p)/(1-a_p)))
print("V>1-for-all criterion a>=b (precision):", sp.simplify(a_p-b_p), "(>0 for alpha>1)")
a_t, b_t = 2*th/(1+2*th), th/(1+2*th)
print("A_theta at theta=1:", a_t.subs(th,1), b_t.subs(th,1), "| Cor2' at alpha=2:", a_p.subs(al,2), b_p.subs(al,2))
print("A_theta onset exponent:", sp.simplify(-(1-b_t)/(1-a_t)))
def phi(W,q,alpha,c=1.0):
    f=lambda lp: c*np.exp(lp)+W*q**(1/alpha)*np.exp(lp)**(-(1-1/alpha))
    r=minimize_scalar(f,bounds=(-60,60),method='bounded',options={'xatol':1e-12}); return r.fun
for alpha in (1.25,1.5,2.0,2.5,2.9):
    d=1e-3
    eW=(np.log(phi(np.exp(d),1,alpha))-np.log(phi(np.exp(-d),1,alpha)))/(2*d)
    eq=(np.log(phi(1,np.exp(d),alpha))-np.log(phi(1,np.exp(-d),alpha)))/(2*d)
    print(f"alpha={alpha}: numeric a={eW:.4f} (theory {alpha/(2*alpha-1):.4f}), b={eq:.4f} (theory {1/(2*alpha-1):.4f}), onset={-(1-eq)/(1-eW):.4f}")

# General precision-price exponent theta: cost c' P^theta + W q^(1/alpha) P^-(1-1/alpha)
print("\nGeneral theta (symbolic):")
m = 1 - 1/al
a_g = th/(th+m); b_g = (th/al)/(th+m)
print(" a =", sp.simplify(a_g), " b =", sp.simplify(b_g))
print(" onset exponent -(1-b)/(1-a) =", sp.simplify(-(1-b_g)/(1-a_g)))
print(" small-share vigilance exponent (b-a)/(1-a) =", sp.simplify((b_g-a_g)/(1-a_g)))
def phi2(W,q,alpha,theta,c=1.0):
    f=lambda lp: c*np.exp(theta*lp)+W*q**(1/alpha)*np.exp(lp)**(-(1-1/alpha))
    return minimize_scalar(f,bounds=(-60,60),method='bounded',options={'xatol':1e-12}).fun
for alpha in (1.5,2.5):
    for theta in (0.5,2.0):
        d=1e-3
        eW=(np.log(phi2(np.exp(d),1,alpha,theta))-np.log(phi2(np.exp(-d),1,alpha,theta)))/(2*d)
        eq=(np.log(phi2(1,np.exp(d),alpha,theta))-np.log(phi2(1,np.exp(-d),alpha,theta)))/(2*d)
        print(f" alpha={alpha} theta={theta}: a={eW:.4f} b={eq:.4f} onset={-(1-eq)/(1-eW):.4f} (theory {-(1+theta):.4f})")
