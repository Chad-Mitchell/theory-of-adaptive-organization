"""Author's check of the two holes R2 names, using THEORY §2.2 / CLAIM_MAP N16's Bayes adaptation time for the
two-state switching world, t_A = (N/2mu^2)[ln(2mu^2/(lam N)) - gamma - 1], and the drift level q = lam*mu^2
(telegraph variance rate, up to a constant factor that does not affect the argument)."""
import math
from scipy.optimize import brentq
G = 0.5772156649015329
tA = lambda lam, mu, N: (N/(2*mu**2))*(math.log(2*mu**2/(lam*N)) - G - 1)
N = 1.0; lam0, mu0 = 0.01, 2.0; q0 = lam0*mu0**2; t0 = tA(lam0, mu0, N)
print(f"base: lam={lam0} mu={mu0} q={q0} t_A={t0:.4f}")
# (a) q fixed, lam and mu traded: Bayes optimum moves (a linear-locked trigger list would not fire)
for f in (0.5, 2.0):
    lam, mu = lam0*f, mu0/math.sqrt(f)
    print(f"(a) q fixed={lam*mu**2:.4f}, lam x{f}: t_A={tA(lam,mu,N):.4f} ({tA(lam,mu,N)/t0-1:+.1%})")
# (b) q doubles, split between lam and mu so that t_A is unchanged: Bayes optimum stays put
def g(s):  # lam x 2^s, mu^2 x 2^(1-s): q doubles for every s
    return tA(lam0*2**s, mu0*math.sqrt(2**(1-s)), N) - t0
s = brentq(g, 0.0, 3.0)  # scanned: g<0 at s=0 (all of the q rise in mu), g>0 at s=3
lam, mu = lam0*2**s, mu0*math.sqrt(2**(1-s))
print(f"(b) q x{lam*mu**2/q0:.3f}, lam x{2**s:.4f}, mu^2 x{2**(1-s):.4f}: t_A={tA(lam,mu,N):.4f} ({tA(lam,mu,N)/t0-1:+.2e})")
# validity of the asymptotic formula (needs 2mu^2/(lam N) >> 1) at the points used
print(f"validity: 2mu^2/(lam N) = {2*mu0**2/(lam0*N):.0f} (base), {2*mu**2/(lam*N):.0f} (b)")
