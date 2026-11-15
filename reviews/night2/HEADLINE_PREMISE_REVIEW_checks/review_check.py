"""HEADLINE-PREMISE-REVIEW: reviewer's own checks (pick-14 executor; independent of SCOPE/APPLY code).
Routes differ from both earlier check.py files: scipy (not mpmath), CARE solver for the linear filter, Monte Carlo of the
Wonham filter in log-odds form (not the stationary-density quadrature), and a direct numerical precision optimisation.
World: x in {+mu,-mu}, switching rate lam each way; dy = x dt + sqrt(N) dW.  q = 4 lam mu^2, kappa = lam N / mu^2.
Log-odds L = ln P(+)/P(-):  dL = (2 mu/N) dy + lam (e^-L - e^L) dt   (exact; from the Zakai equations)."""
import numpy as np, sys
from scipy.special import k0, k1
from scipy.linalg import solve_continuous_are
from scipy.optimize import minimize_scalar
G = np.euler_gamma
def bayes_mse(lam, mu2, N):
    k = lam*N/mu2; return mu2*2*k0(k)/(k0(k)+k1(k))
def lin_mse(lam, mu2, N):   # OU with rate 2 lam, variance mu2: dx = -a x dt + sqrt(2 a mu2) dB
    a = 2*lam
    P = solve_continuous_are(np.array([[-a]]), np.array([[1.0]]), np.array([[2*a*mu2]]), np.array([[N]]))
    return P[0, 0]
out = []
pr = lambda s: (print(s), out.append(s))
# (1) fixed q = N = 1, split q between lam and mu
pr("(1) fixed q=N=1: lam, linear MSE (CARE), Bayes MSE (Bessel, scipy)")
L, B = [], []
for lam in 10.0**np.arange(-5, -1.99, 0.5):
    mu2 = 1/(4*lam); l = lin_mse(lam, mu2, 1.0); b = bayes_mse(lam, mu2, 1.0); L.append(l); B.append(b)
    pr(f"  lam={lam:.1e} linear={l:.6f} bayes={b:.4e}")
pr(f"  spread linear {max(L)/min(L):.4f}x  Bayes {max(B)/min(B):.1f}x")
# (2) precision elasticities: minimise w*MSE(N=1/p) + c p^theta numerically; compare with 1/(theta+eta) etc.
pr("(2) precision optimum, Bayes jump world, mu=1, lam=1e-3, theta=1, c=1")
def pstar(w, lam=1e-3, mu2=1.0, theta=1.0):
    r = minimize_scalar(lambda lp: w*bayes_mse(lam, mu2, np.exp(-lp)) + np.exp(theta*lp), bounds=(-10, 30), method="bounded",
                        options={"xatol": 1e-11})
    return np.exp(r.x)
def el(f, x, h=1e-3): return (np.log(f(x*np.exp(h))) - np.log(f(x*np.exp(-h))))/(2*h)
w0 = 50.0; p0 = pstar(w0); N0 = 1/p0
eta = el(lambda N: bayes_mse(1e-3, 1.0, N), N0)
pr(f"  p*={p0:.4f}; local eta (MSE elasticity in N) = {eta:.4f}")
pr(f"  d ln p*/d ln w = {el(pstar, w0):.4f}  vs 1/(theta+eta) = {1/(1+eta):.4f}  (linear world: 2/3)")
pr(f"  d ln p*/d ln lam = {el(lambda lam: pstar(w0, lam=lam), 1e-3):.4f} vs eta/(theta+eta) = {eta/(1+eta):.4f}")
# (3) Monte Carlo Wonham filter: MSE and mean adaptation time (first zero-crossing of the estimate after a switch)
def mc(kappa, paths=3000, dt=0.01, T=None, seed=20261115):
    rng = np.random.default_rng(seed); lam = kappa; mu = 1.0; N = 1.0
    T = T or 20/lam; n = int(T/dt); burn = int(3/lam/dt)
    x = np.where(rng.random(paths) < .5, mu, -mu); Lo = 2*np.arctanh(x/mu*0.999)
    se, cnt = 0.0, 0; since = np.full(paths, np.nan); crossings = []
    for i in range(n):
        sw = rng.random(paths) < lam*dt
        x = np.where(sw, -x, x)
        if i > burn:
            since = np.where(sw, 0.0, since)
        dy = x*dt + np.sqrt(N*dt)*rng.standard_normal(paths)
        Lc = np.clip(Lo, -50, 50)
        Lo = Lo + (2*mu/N)*dy + lam*(np.exp(-Lc) - np.exp(Lc))*dt
        m = mu*np.tanh(Lo/2)
        if i > burn:
            se += np.sum((x - m)**2); cnt += paths
            act = ~np.isnan(since)
            since[act] += dt
            done = act & (np.sign(m) == np.sign(x))
            crossings.extend(since[done].tolist()); since[done] = np.nan
    c = np.array(crossings)
    return se/cnt, c.mean(), c.std()/np.sqrt(len(c)), len(c)
if "--mc" in sys.argv:
    out.clear()
    pr("(3) Monte Carlo (Euler; dt 0.01 at kappa 1e-2, 0.02 at 1e-3; T=20/lam after 3/lam burn-in) vs closed forms; mu=N=1")
    for kappa, dt, P in ((1e-2, 0.01, 2000), (1e-3, 0.02, 1000)):
        mse, tA, se_t, nsw = mc(kappa, paths=P, dt=dt)
        th = 0.5*(np.log(2/kappa) - G - 1)
        pr(f"  kappa={kappa:g}: MSE MC={mse:.4e} closed={bayes_mse(kappa,1,1):.4e} linear={lin_mse(kappa,1,1):.4e}; "
           f"t_A MC={tA:.3f}+-{se_t:.3f} (n={nsw}) vs (N/2mu^2)[ln(2mu^2/lamN)-g-1]={th:.3f}")
open(__file__.replace(".py", ".out"), "a").write("\n".join(out) + "\n")
