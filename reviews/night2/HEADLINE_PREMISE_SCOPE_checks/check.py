"""HEADLINE-PREMISE-SCOPE check (pick 10). Two-state switching world, levels +-mu, switching rate lam each way,
white observation noise density N. Drift level q = 4 lam mu^2 (high-frequency level of S = q/omega^2).
Compares, at FIXED q and N, the best linear tracker's steady MSE (Kalman for the OU with the same covariance)
and the Bayes (Wonham) MSE mu^2 * 2K0(k)/(K0(k)+K1(k)), k = lam N / mu^2 (THEORY v1.4.3 sec 2.2, CLAIM_MAP N16).
Claim checked: with q and N fixed, the linear MSE is (to leading order in k) fixed, while the Bayes MSE moves with
how q is split between jump rate and amplitude. So 'alpha, q, N, stakes' is a complete input list only for the
linear tracker (or a Gaussian world)."""
import numpy as np
from scipy.special import k0, k1
from scipy.integrate import quad

def lin_mse(lam, mu, N):
    # OU dx = -2 lam x dt + sqrt(4 lam mu^2) dW ; Riccati 0 = -4 lam P + 4 lam mu^2 - P^2/N
    return 2*N*(np.sqrt(lam**2 + lam*mu**2/N) - lam)

def bayes_mse(lam, mu, N):
    k = lam*N/mu**2
    return mu**2 * 2*k0(k)/(k0(k)+k1(k))

def bayes_mse_quad(lam, mu, N):
    # independent check: stationary density of the Wonham filter m in (-1,1) (units mu=1 after scaling):
    # dm = -2 lam m dt + (mu^2/N)^(1/2)... use known form p(m) ∝ (1-m^2)^-2 exp(-2k/(1-m^2)); MSE = mu^2 E[1-m^2]
    k = lam*N/mu**2
    # substitute m = tanh(y): p dm ∝ cosh^2(y) exp(-2k cosh^2 y) dy, and 1-m^2 = sech^2 y; symmetric in y
    ymax = np.arccosh(np.sqrt(60/k))
    g = lambda y: np.cosh(y)**2*np.exp(-2*k*np.cosh(y)**2)
    Z = quad(g, 0, ymax, limit=1000)[0]
    E = quad(lambda y: np.exp(-2*k*np.cosh(y)**2), 0, ymax, limit=1000)[0]/Z
    return mu**2*E

N, q = 1.0, 1.0
print("fixed q=%.3g, N=%.3g; sqrt(qN)=%.4f (alpha=2 linear asymptote e* = q^1/2 N^1/2)" % (q, N, np.sqrt(q*N)))
print("%10s %10s %10s %12s %12s %12s" % ("lam", "mu", "kappa", "lin_MSE", "bayes_MSE", "bayes_quad"))
rows = []
for lam in [1e-5, 1e-4, 1e-3, 1e-2]:
    mu = np.sqrt(q/(4*lam))
    r = (lam, mu, lam*N/mu**2, lin_mse(lam, mu, N), bayes_mse(lam, mu, N), bayes_mse_quad(lam, mu, N))
    rows.append(r); print("%10.1e %10.3f %10.2e %12.5f %12.5f %12.5f" % r)
lin = [r[3] for r in rows]; bay = [r[4] for r in rows]
print("linear MSE range / mean: %.3f ; Bayes MSE max/min: %.2f" % ((max(lin)-min(lin))/np.mean(lin), max(bay)/min(bay)))
assert all(abs(r[4]-r[5])/r[5] < 1e-3 for r in rows), "closed form vs quadrature mismatch"
assert (max(lin)-min(lin))/np.mean(lin) < 0.1 and max(bay)/min(bay) > 3
print("PASS: at fixed (q, N) the linear optimum barely moves (leading order sqrt(qN)); the Bayes optimum moves by >3x")
