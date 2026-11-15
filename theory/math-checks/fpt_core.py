"""Task 2 checks: first-passage 'temperature' z = B/(sigma*sqrt(tau)).
Three fix mechanisms, two-sided barrier |X|>=B, X starts at 0 (set point), D = sigma^2/2.
 A: fixed delay  -- X fully reset to 0 every tau (deterministic)
 B: fix as rate  -- X reset to 0 at Poisson rate 1/tau (Evans & Majumdar 2011 type)
 C: proportional -- OU restoring force, dX = -X/tau dt + sigma dW
Each: hazard h = 1/MFPT. Dimensional analysis => h*tau = F(z). Check identity eps_tau = eps_sigma/2 - 1.
"""
import numpy as np
from scipy import integrate, special
rng = np.random.default_rng(20261114)

def S_two_sided(t, B=1.0, sigma=1.0, nmax=400):
    # survival of BM (var sigma^2 t) started at 0 in (-B,B)
    n = np.arange(nmax)[:, None]
    lam = (2*n+1)**2*np.pi**2*sigma**2/(8*B**2)
    return np.sum(4/np.pi*(-1)**n/(2*n+1)*np.exp(-lam*np.atleast_1d(t)[None, :]), axis=0)

def F_A(z):
    # tau=1, sigma=1, B=z.  MFPT = E[min(T,tau)] / P(T<tau)  (renewal over windows)
    B = z
    p = 1 - S_two_sided(1.0, B)[0]
    # E[min(T,1)] = int_0^1 S dt
    I = integrate.quad(lambda t: S_two_sided(t, B)[0] if t > 1e-9 else 1.0, 0, 1, limit=200)[0]
    return 1.0/(I/p)

def F_B(z):
    return 1.0/(np.cosh(np.sqrt(2)*z)-1.0)

def F_C(z):
    # MFPT = 2 tau int_0^z e^{v^2} int_0^v e^{-u^2} du dv
    g = lambda v: np.exp(v*v)*np.sqrt(np.pi)/2*special.erf(v)
    I = integrate.quad(g, 0, z, limit=200)[0]
    return 1.0/(2*I)

def h(model, sigma, B, tau):
    z = B/(sigma*np.sqrt(tau))
    return model(z)/tau

def elasticities(model, z, d=1e-4):
    sigma, B, tau = 1.0, z, 1.0
    es = (np.log(h(model, sigma*np.exp(d), B, tau)) - np.log(h(model, sigma*np.exp(-d), B, tau)))/(2*d)
    eb = (np.log(h(model, sigma, B*np.exp(d), tau)) - np.log(h(model, sigma, B*np.exp(-d), tau)))/(2*d)
    et = (np.log(h(model, sigma, B, tau*np.exp(d))) - np.log(h(model, sigma, B, tau*np.exp(-d))))/(2*d)
    return es, eb, et

