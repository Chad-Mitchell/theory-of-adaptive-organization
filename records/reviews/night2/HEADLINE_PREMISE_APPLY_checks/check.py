"""HEADLINE-PREMISE-APPLY independent check (applier's own code; not the pick-10 check.py).
Two-state world +-mu, switching rate lam each way, white noise density N; q = 4 lam mu^2 (high-frequency level of
S = 2 mu^2 (4 lam) / (w^2 + (2lam)^2) ~ q / w^2). Holds q = N = 1 fixed and splits q into (lam, mu).
(a) best linear tracker: steady-state Kalman error for an OU with the same covariance (rate a = 2 lam, var mu^2).
(b) Bayes tracker: Wonham stationary density p(u) ~ (1-u^2)^-2 exp(-2k/(1-u^2)), k = lam N/mu^2, MSE = mu^2 E[1-u^2],
    by quadrature in s = 1/(1-u^2) (own derivation), vs the closed form mu^2 2K0(k)/(K0(k)+K1(k)) (THEORY 2.2).
(c) reset reads: E[x(t+s)|x(t)] = x(t) e^{-2 lam s}, linear in the last exact read (Markov two-state), so the
    hold/predict error depends on second moments only: check by exact two-state transition probabilities."""
import numpy as np
from mpmath import mp, quad, exp, besselk, sqrt, inf, mpf
mp.dps = 30
q = N = mpf(1)
print(" lam      mu^2       kappa      linear_MSE   Bayes_quad    Bayes_closed   rel_diff")
lin, bay = [], []
for lam in [mpf(10)**e for e in (-5, -4.5, -4, -3.5, -3, -2.5, -2)]:
    mu2 = q/(4*lam); k = lam*N/mu2; a = 2*lam
    P = N*(-a + sqrt(a*a + 2*a*mu2/N))  # Riccati 0 = -2aP + 2a mu2 - P^2/N (OU, rate a, variance mu2)
    # s = 1/(1-u^2) = 1 + t^2; density in t (u > 0 half; symmetric): exp(-2k(1+t^2)) sqrt(1+t^2); 1-u^2 = 1/(1+t^2)
    f = lambda t: exp(-2*k*(1+t*t))*sqrt(1+t*t)
    pts = [0, 1, 10, 1/sqrt(k), 10/sqrt(k), inf]
    Z = quad(f, pts); E = quad(lambda t: f(t)/(1+t*t), pts)
    bq = mu2*E/Z; bc = mu2*2*besselk(0, k)/(besselk(0, k)+besselk(1, k))
    lin.append(float(P)); bay.append(float(bq))
    print(f"{float(lam):.1e} {float(mu2):10.1f} {float(k):10.2e} {float(P):12.6f} {float(bq):13.6e} {float(bc):13.6e} {float(abs(bq/bc-1)):.1e}")
print(f"linear spread max/min = {max(lin)/min(lin):.4f}; Bayes spread max/min = {max(bay)/min(bay):.1f}")
# (c)
lam, mu, s = 0.3, 1.7, 0.8
p_stay = 0.5*(1+np.exp(-2*lam*s))
print("(c) E[x(t+s)|x(t)=mu]/mu =", (p_stay*mu - (1-p_stay)*mu)/mu, " e^{-2 lam s} =", np.exp(-2*lam*s))
