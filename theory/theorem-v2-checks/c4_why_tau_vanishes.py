"""C4. Why a real time-to-fix effect can vanish in cross-sectional survival data (C3-like design).
Simulate N projects with known causal hazard; fit the C3-style logit of event on ln tau and ln(sigma/B)."""
import numpy as np
from scipy import special
rng = np.random.default_rng(4)
def S2(z, K=40):
    """two-sided survival of sigma W in (-B,B) to tau, z=sigma sqrt(tau)/B. Image series (fast for small z)."""
    z = np.atleast_1d(z).astype(float); k = np.arange(-K, K+1)[:, None]
    Phi = lambda x: 0.5*special.erfc(-x/np.sqrt(2))
    S = np.sum((-1.0)**k*(Phi((2*k+1)/z[None, :]) - Phi((2*k-1)/z[None, :])), 0)
    return np.clip(S, 1e-300, 1)
# cross-check against Fourier series used in c2
_zz = np.array([0.3, 0.6, 1.0, 2.0]); _k = np.arange(200)[:, None]
_F = (4/np.pi)*np.sum((-1)**_k/(2*_k+1)*np.exp(-(2*_k+1)**2*np.pi**2*_zz[None, :]**2/8), 0)
print("image vs Fourier survival at z=0.3,0.6,1,2:", np.round(S2(_zz), 6), np.round(_F, 6))
def logit_fit(X, yv, it=50):
    X = np.column_stack([np.ones(len(yv)), X]); b = np.zeros(X.shape[1])
    for _ in range(it):
        p = special.expit(X @ b); Wt = p*(1-p)+1e-12; H = X.T @ (X*Wt[:, None]); b += np.linalg.solve(H, X.T @ (yv-p))
    se = np.sqrt(np.diag(np.linalg.inv(H))); return b[1:], se[1:]
N, Hz = 20_000, 2.33
lsb = rng.normal(np.log(0.75), 0.35, N)           # ln(sigma/B) per sqrt(yr); calibrated so pure-diffusive event rate ~ C3's
ltau = rng.normal(np.log(44/365.25), 1.0, N) + 0.3*(lsb-lsb.mean())   # slow fixers somewhat thinner-buffered (C3 corr ~0.26)
def run(label, lam_jump=0.0, tau_noise=0.0, frailty=0.0, select=False):
    z = np.exp(lsb + frailty*rng.standard_normal(N))*np.sqrt(np.exp(ltau))   # true z (frailty = unmeasured shock)
    h_diff = -np.log(S2(z))/np.exp(ltau)                                         # calendar hazard, resets every tau
    h = h_diff + lam_jump
    if select:   # must survive a 2-yr pre-period to enter the sample (C3: alive mid-2023)
        keep = rng.random(N) < np.exp(-h*2.0)
    else: keep = np.ones(N, bool)
    ev = (rng.random(N) < 1-np.exp(-h*Hz)) & keep
    obs_ltau = ltau + tau_noise*rng.standard_normal(N)
    b, se = logit_fit(np.column_stack([obs_ltau[keep], lsb[keep]]), ev[keep].astype(float))
    share = np.mean(h_diff[keep])/np.mean(h[keep])
    print(f"  {label:58s} n={keep.sum():5d} events={ev.sum()/keep.sum():.3f} diffusive share={share:.2f}  beta_lntau={b[0]:+.3f}±{1.96*se[0]:.3f}  beta_ln(s/B)={b[1]:+.3f}")
print("logit(event) ~ ln tau + ln(sigma/B); true model: two-sided diffusive ruin reset every tau, plus optional tau-independent jump hazard")
run("A. pure diffusive mechanism")
run("B. + jump hazard 0.06/yr (maintainer exits etc.)", lam_jump=0.06)
run("C. B + tau measured with noise (sd 1.0 in ln tau)", lam_jump=0.06, tau_noise=1.0)
run("D. C + unmeasured shock frailty (sd 0.4) + survivor selection", lam_jump=0.06, tau_noise=1.0, frailty=0.4, select=True)
lsb -= 0.3
run("E. sigma/B lower by e^-0.3 and jump hazard 0.07/yr dominates", lam_jump=0.07)
print("Reading: beta_lntau is large when failure is diffusive first passage (A). It shrinks toward 0 as tau-independent")
print("failure modes take over (B,E) and as tau is mismeasured (C). Selection on prior survival with unmeasured shocks attenuates further (D).")
