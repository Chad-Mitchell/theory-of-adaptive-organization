"""C8. (a) Merton / Black-Cox correspondence. (b) In calendar time the tau/sigma exponent ratio is not 1/2."""
import numpy as np
from scipy import special, stats
rng = np.random.default_rng(8)
Phi = stats.norm.cdf
print("== C8a: Merton PD = Phi(-DD), DD = [ln(V/D) + (mu - s^2/2)T]/(s sqrt T). Black-Cox first passage, zero log-drift = 2 Phi(-DD) = erfc(DD/sqrt2) ==")
V, D, s, T = 1.0, 0.7, 0.3, 1.0
for mu in [s**2/2, 0.10]:
    DD = (np.log(V/D)+(mu-s**2/2)*T)/(s*np.sqrt(T)); nu = mu-s**2/2; b = np.log(V/D)
    bc = Phi((-b-nu*T)/(s*np.sqrt(T))) + np.exp(-2*nu*b/s**2)*Phi((-b+nu*T)/(s*np.sqrt(T)))
    n, steps = 100_000, 500; dt = T/steps; x = np.zeros(n); hit = np.zeros(n, bool)
    for _ in range(steps):
        xn = x+nu*dt+s*np.sqrt(dt)*rng.standard_normal(n); pc = np.exp(-2*np.clip(x+b, 0, None)*np.clip(xn+b, 0, None)/(s**2*dt))
        hit |= (xn <= -b) | (rng.random(n) < pc); x = xn
    print(f"  mu={mu:.3f}: DD={DD:.3f}  Merton PD={Phi(-DD):.4f}  Black-Cox={bc:.4f}  MC first passage={hit.mean():.4f}  2Phi(-DD)={2*Phi(-DD):.4f}")
print("  => with zero log-drift, our one-sided 'temperature' ruin erfc(1/(z sqrt2)) IS Black-Cox with buffer ln(V/D) and z = 1/DD, horizon = fix interval.")
print("== C8b: calendar hazard h = (s^2/B^2) G(z). Exponent ratio r_tau = (dlnh/dln tau)/(dlnh/dln(s/B)) = g/(2(2+g)), g = dlnG/dlnz ==")
def mlogS2(z, K=200):
    k = np.arange(K); S = (4/np.pi)*np.sum((-1)**k/(2*k+1)*np.exp(-(2*k+1)**2*np.pi**2*z**2/8)); return -np.log(S)
for z in [0.3, 0.35, 0.5, 1.0, 2.0]:
    e = 1e-5; G = lambda q: mlogS2(q)/q**2; g = (np.log(G(z*(1+e)))-np.log(G(z)))/np.log(1+e)
    print(f"  z={z}: g={g:.3f}  r_tau={g/(2*(2+g)):.3f}   (per-window risk, not calendar hazard, gives exactly 1/2)")
