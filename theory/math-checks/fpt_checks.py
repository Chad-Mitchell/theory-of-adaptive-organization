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

print("== 1. Elasticities of hazard (finite differences on h(sigma,B,tau)) ==")
print("model  z     eps_sigma  eps_B    eps_tau   eps_sigma/2-1  h*tau")
zs = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
maxdev = 0
min_es = 9e9
for name, m in [("A", F_A), ("B", F_B), ("C", F_C)]:
    for z in zs:
        es, eb, et = elasticities(m, z)
        maxdev = max(maxdev, abs(et-(es/2-1)), abs(eb+es))
        min_es = min(min_es, es)
        print(f"  {name}  {z:4.2f}  {es:8.3f}  {eb:8.3f}  {et:8.3f}  {es/2-1:8.3f}   {m(z):.4g}")
print(f"max |eps_tau-(eps_sigma/2-1)|, |eps_B+eps_sigma| over grid = {maxdev:.2e}")
print(f"min eps_sigma over grid (claim: >= 2 in all three models) = {min_es:.4f}")

print("\n== 2. Closed forms / asymptotes ==")
for z in [2.0, 3.0, 4.0]:
    print(f"  OU (C) z={z}: exact h*tau={F_C(z):.4e}; Kramers asymptote 2z e^-z^2/sqrt(pi) (two-sided = 2x one-sided z e^-z^2/sqrt(pi)) = {2*z*np.exp(-z*z)/np.sqrt(np.pi):.4e}")
for z in [2.0, 3.0, 4.0]:
    print(f"  reset (B) z={z}: h*tau={F_B(z):.4e}; asymptote 2 e^(-sqrt2 z) = {2*np.exp(-np.sqrt(2)*z):.4e}")
for z in [2.0, 3.0, 4.0]:
    p = 1 - S_two_sided(1.0, z)[0]
    print(f"  delay (A) z={z}: h*tau={F_A(z):.4e}; per-window P={p:.4e}; 4*Phi(-z)(=2*erfc(z/sqrt2))={2*special.erfc(z/np.sqrt(2)):.4e}")
print("  one-sided fixed window (reflection principle): P(max_[0,tau] W >= B) = 2 Phi(-z) = erfc(z/sqrt2)")

print("\n== 3. Monte Carlo validation (Brownian-bridge crossing correction) ==")
def mc_mfpt(mode, z, npaths=4000, nsteps_per_tau=400, tmax_tau=400):
    sigma, tau, B = 1.0, 1.0, z
    dt = tau/nsteps_per_tau
    x = np.zeros(npaths); t = np.zeros(npaths); alive = np.ones(npaths, bool)
    tw = np.zeros(npaths)  # time since last deterministic reset
    T = np.full(npaths, np.nan)
    step = 0
    while alive.any() and step < tmax_tau*nsteps_per_tau:
        step += 1
        idx = np.where(alive)[0]
        x0 = x[idx]
        if mode == "C":
            x1 = x0*np.exp(-dt/tau) + sigma*np.sqrt((tau/2)*(1-np.exp(-2*dt/tau)))*rng.standard_normal(idx.size)
        else:
            x1 = x0 + sigma*np.sqrt(dt)*rng.standard_normal(idx.size)
        # bridge crossing prob (approx for OU too, small dt)
        pu = np.where((x0 < B) & (x1 < B), np.exp(-2*(B-x0)*(B-x1)/(sigma**2*dt)), 1.0)
        pl = np.where((x0 > -B) & (x1 > -B), np.exp(-2*(B+x0)*(B+x1)/(sigma**2*dt)), 1.0)
        hit = (rng.random(idx.size) < pu) | (rng.random(idx.size) < pl)
        t[idx] += dt
        T[idx[hit]] = t[idx[hit]]
        alive[idx[hit]] = False
        x[idx] = x1
        if mode == "A":
            tw[idx] += dt
            rs = idx[tw[idx] >= tau - 1e-12]
            x[rs] = 0.0; tw[rs] = 0.0
        if mode == "B":
            rs = idx[rng.random(idx.size) < dt/tau]
            x[rs] = 0.0
    return np.nanmean(T), np.nanstd(T)/np.sqrt(np.sum(~np.isnan(T))), alive.sum()

for name, m in [("A", F_A), ("B", F_B), ("C", F_C)]:
    for z in [0.5, 1.0, 1.5]:
        mean, se, left = mc_mfpt(name, z)
        print(f"  {name} z={z}: MC MFPT/tau = {mean:.3f} +- {se:.3f} (unabsorbed {left});  theory 1/F = {1/m(z):.3f}")
