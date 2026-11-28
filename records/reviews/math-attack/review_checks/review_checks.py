"""Independent reviewer checks (REVIEW.md). Notation: zM = B/(sigma sqrt tau) (MATH_ATTACK), zG = 1/zM (GENERAL_THEOREM)."""
import numpy as np
from scipy import special, integrate, optimize, stats
def S2(zG, K=400):  # two-sided survival of sigma W in (-B,B) over tau, zG = sigma sqrt(tau)/B
    zG = np.atleast_1d(zG).astype(float); k = np.arange(K)[:, None]
    return np.clip((4/np.pi)*np.sum((-1)**k/(2*k+1)*np.exp(-(2*k+1)**2*np.pi**2*zG[None, :]**2/8), 0), 1e-300, 1)
print("== R1. Toy reversal: crossing sigma/B of dh (tau 4->16), one-sided, under three hazard definitions ==")
p_win = lambda z: 2*stats.norm.sf(z)
def Emin(B, s, tau):
    return integrate.quad(lambda t: 1-2*stats.norm.sf(B/(s*np.sqrt(t))) if t > 0 else 1.0, 0, tau, limit=200)[0]
defs = {
 "naive P/tau": lambda s, tau: p_win(1/(s*np.sqrt(tau)))/tau,
 "renewal P/E[min(T,tau)] (=1/MFPT)": lambda s, tau: p_win(1/(s*np.sqrt(tau)))/Emin(1.0, s, tau),
 "survival -ln(1-P)/tau": lambda s, tau: -np.log1p(-p_win(1/(s*np.sqrt(tau))))/tau,
}
for nm, h in defs.items():
    f = lambda s: h(s, 16) - h(s, 4)
    xs = np.linspace(0.12, 3, 600); v = np.array([f(x) for x in xs]); i = np.where(np.diff(np.sign(v)) != 0)[0]
    roots = [optimize.brentq(f, xs[j], xs[j+1]) for j in i]
    print(f"  {nm:38s}: sign changes at sigma/B = {np.round(roots, 3)}")
print("\n== R2. C3 regime pinning (h=0.0712/yr) under different fix mechanisms; HR per doubling of tau at fixed sigma,B ==")
h_obs = 0.0712
def hazard_A(zG, tau):  # deterministic reset every tau, survival-decay definition
    return -np.log(S2(zG)[0])/tau
def hazard_B(zG, tau):  # Poisson resets at rate 1/tau, two-sided, 1/MFPT: h tau = 1/(cosh(sqrt2 zM)-1)
    zM = 1/zG; return 1/(np.cosh(np.sqrt(2)*zM)-1)/tau
def hazard_C(zG, tau):  # OU, two-sided, 1/MFPT
    zM = 1/zG; I = integrate.quad(lambda v: np.exp(v*v)*np.sqrt(np.pi)/2*special.erf(v), 0, zM, limit=200)[0]
    return 1/(2*I)/tau
def hazard_LN(zG, tau, s=2.0, n=4000):  # deterministic reset at random i.i.d. lognormal intervals L = tau*U, median(U)=1, sd(lnU)=s
    u = np.exp(s*np.sqrt(2)*special.erfinv(2*(np.arange(n)+0.5)/n-1))  # quantile grid
    L = tau*u; P = 1-S2(zG*np.sqrt(u))
    # renewal: h = E[P]/E[min(T,L)] ; E[min(T,L)] ~ E[L] in the cold limit; use int_0^L S dt approx by L*(1-P/2) (crude, bounded)
    return np.mean(P)/np.mean(L*(1-P/2))
def hazard_PAR(zG, tau, kappa=1.2, n=6000):  # Pareto intervals with tail index kappa, median tau
    q = (np.arange(n)+0.5)/n; xm = tau/2**(1/kappa); L = xm*(1-q)**(-1/kappa); u = L/tau
    P = 1-S2(zG*np.sqrt(u)); return np.mean(P)/np.mean(L*(1-P/2))
tau = 44/365.25
for nm, hf in [("A deterministic reset", hazard_A), ("B Poisson-rate reset", hazard_B), ("C OU restoring", hazard_C),
               ("lognormal intervals sd(ln)=2", hazard_LN), ("Pareto intervals kappa=1.2", hazard_PAR), ("Pareto intervals kappa=1.05", lambda z, t: hazard_PAR(z, t, 1.05))]:
    try:
        zG = optimize.brentq(lambda q: np.log(hf(q, tau))-np.log(h_obs), 0.02, 3.0)
    except ValueError as e:
        print(f"  {nm}: no root ({e})"); continue
    d = 0.05
    # elasticity wrt tau at fixed sigma,B: zG scales as sqrt(tau)
    el = (np.log(hf(zG*np.exp(d/2), tau*np.exp(d))) - np.log(hf(zG*np.exp(-d/2), tau*np.exp(-d))))/(2*d)
    print(f"  {nm:30s}: pinned zG={zG:.3f} (zM={1/zG:.2f}); eps_tau={el:.2f}; HR/doubling={2**el:.2f}; max diffusive share at HR<=1.087: {100*min(1,0.087/max(2**el-1,1e-9)):.1f}%")
print("\n== R3. MATH_ATTACK equal-attenuation prediction for beta_tau, using sigma vs B as the anchor ==")
for lab, anchor in [("beta_sigma (L) 0.28", 0.28), ("beta_sigma upper CI 0.66", 0.66), ("|beta_B| (L) 0.47", 0.47), ("|beta_B| (A) 0.57", 0.57)]:
    out = []
    for eps in [2, 4.4, 9.9, 16.8]:
        out.append(f"eps_s={eps}: {anchor/2 - anchor/eps:.3f}")
    print(f"  anchor {lab:26s} -> predicted beta_tau: " + "; ".join(out))
print("  (C3 literal CI for beta_tau: [-0.09, 0.10]; coding A: [-0.05, 0.12]; eps_s = 4.4/9.9/16.8 are models B/A/C at the pinned cold regime zM~3)")
print("\n== R4. Weakest-link rule depends on tail class ==")
FA = lambda zM: 2*special.erfc(zM/np.sqrt(2))  # model A per-window large-z
for z in [3.0, 4.0]:
    for N in [4, 16]:
        zp = optimize.brentq(lambda q: FA(q) - N*FA(z), 0.1, z)
        print(f"  model A (fixed delay) z={z} N={N}: exact z'={zp:.3f}; sqrt(z^2-lnN)={np.sqrt(z*z-np.log(N)):.3f}; sqrt(z^2-2lnN)={np.sqrt(z*z-2*np.log(N)):.3f}")
print("\n== R5. O1: EOQ check rate equals 'nats per unit time' only formally ==")
print("  EOQ: checks/time = 1/T*, mean error D_avg = sigma^2 T/2  =>  1/T = sigma^2/(2 D_avg). Thermo floor: nats/time = sigma^2/(2 D).")
print("  So c/T == c * sigma^2/(2 D_avg): identifying one check with one nat makes the forms identical by construction.")
print("  A perfect check acquires unbounded information (error -> 0), and info lost over a sawtooth cycle int_0^T dt/(2t) diverges:")
for eps in [1e-2, 1e-4, 1e-6]:
    print(f"    nats lost per cycle from error var eps*sigma^2*T to sigma^2*T: {0.5*np.log(1/eps):.2f}")

print("\n== R2b. Random fix intervals, exact renewal: h = E[P(L)] / E[int_0^L S dt] (two-sided BM, reset to 0 at the end of each interval) ==")
def ES_int(L, sigma_over_B, K=300):
    # int_0^L S(t) dt for two-sided BM from centre in (-B,B), B=1: sum 4/pi (-1)^k/(2k+1) (1-exp(-lam_k L))/lam_k
    k = np.arange(K)[:, None]; lam = (2*k+1)**2*np.pi**2*sigma_over_B**2/8
    return np.sum(4/np.pi*(-1)**k/(2*k+1)*(1-np.exp(-lam*L[None, :]))/lam, 0)
def h_random(sB, tau, sampler):
    L = tau*sampler; P = 1-S2(sB*np.sqrt(L)); return np.mean(P)/np.mean(ES_int(L, sB))
n = 20000; q = (np.arange(n)+0.5)/n
samplers = {"deterministic (check)": np.ones(n),
            "exponential (Poisson-like)": -np.log(1-q)/np.log(2),
            "lognormal sd(ln)=1": np.exp(1*np.sqrt(2)*special.erfinv(2*q-1)),
            "lognormal sd(ln)=2": np.exp(2*np.sqrt(2)*special.erfinv(2*q-1)),
            "Pareto kappa=1.5": (1-q)**(-1/1.5)/2**(1/1.5),
            "Pareto kappa=1.2": (1-q)**(-1/1.2)/2**(1/1.2)}
for nm, u in samplers.items():
    f = lambda lsB: np.log(h_random(np.exp(lsB), tau, u)) - np.log(h_obs)
    lsB = optimize.brentq(f, np.log(0.05), np.log(20)); sB = np.exp(lsB)
    d = 0.05; el = (np.log(h_random(sB, tau*np.exp(d), u)) - np.log(h_random(sB, tau*np.exp(-d), u)))/(2*d)
    print(f"  {nm:28s}: pinned sigma*sqrt(median tau)/B={sB*np.sqrt(tau):.3f}; eps_tau={el:.2f}; HR/doubling={2**el:.2f}; max diffusive share (HR<=1.087): {100*min(1,0.087/max(2**el-1,1e-9)):.0f}%")
