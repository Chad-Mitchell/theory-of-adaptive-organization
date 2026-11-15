"""Task 3 checks: does coarse-graining preserve the problem?"""
import numpy as np
from scipy import signal, special
exec(open("fpt_core.py").read())
rng = np.random.default_rng(11)

print("== 1. Representative-agent (Gorman-type) closure of the tracking cost ==")
# parts i: cost c_i/T_i + w_i s_i^2 T_i/2. Decentralized optimum: sum sqrt(2 c_i w_i s_i^2).
# A single aggregate agent with one clock: sqrt(2 * sum c_i * sum w_i s_i^2). Ratio >= 1 (Cauchy-Schwarz),
# = 1 iff c_i/(w_i s_i^2) equal for all i. With a COMMON check cost c_i=c it is <= sqrt(K) (T3b);
# with heterogeneous c_i it is UNBOUNDED (cost in one part, drift in another).
worst = 0; worst_common = 0
for trial in range(20000):
    K = rng.integers(2, 20)
    cc = np.exp(rng.normal(0, 2, K)); q = np.exp(rng.normal(0, 2, K))  # q = w s^2
    ratio = np.sqrt(cc.sum()*q.sum())/np.sum(np.sqrt(cc*q))
    assert ratio >= 1-1e-12
    worst = max(worst, ratio)
    rc = np.sqrt(K*q.sum())/np.sum(np.sqrt(q)); assert rc <= np.sqrt(K)+1e-9
    worst_common = max(worst_common, rc/np.sqrt(K))
cc = np.array([1., 2., 5.]); q = 3*cc
print("  20000 random draws: ratio >= 1 always; max ratio seen (heterogeneous c) =", round(worst, 2),
      "; common-c case: ratio <= sqrt(K) held, max ratio/sqrt(K) =", round(worst_common, 3))
cc2 = np.array([1.0, 1e-6]); q2 = np.array([1e-6, 1.0])
print("  adversarial 2 parts (cost in one, drift in other): ratio =", round(np.sqrt(cc2.sum()*q2.sum())/np.sum(np.sqrt(cc2*q2)), 1))
print("  equal c_i/q_i example ratio =", np.sqrt(cc.sum()*q.sum())/np.sum(np.sqrt(cc*q)))

print("\n== 2. Temperature flow under pooling (fungible buffers, equal parts, pairwise shock corr rho) ==")
# z_N = N B / (sigma sqrt(N(1+(N-1)rho)) sqrt(tau)) = z sqrt(N/(1+(N-1)rho))
for rho in [0.0, 0.1, 0.5, 1.0]:
    zN = [np.sqrt(N/(1+(N-1)*rho)) for N in [1, 4, 16, 64, 1024]]
    print(f"  rho={rho}: z_N/z for N=1,4,16,64,1024:", np.round(zN, 2), " limit 1/sqrt(rho) =", (np.inf if rho == 0 else round(1/np.sqrt(rho), 2)))
# MC check of aggregate sigma for N=16, rho=0.3
N, rh, n = 16, 0.3, 200000
common = rng.standard_normal(n); idio = rng.standard_normal((n, N))
X = np.sqrt(rh)*common[:, None] + np.sqrt(1-rh)*idio
print("  MC: SD of sum, N=16 rho=0.3:", X.sum(1).std().round(3), " theory sqrt(N(1+(N-1)rho)) =", np.sqrt(N*(1+(N-1)*rh)).round(3))

print("\n== 3. Weakest link (non-fungible buffers): aggregate hazard N*h(z). Same tail form, opposite flow ==")
for name, m, zeff in [("B (exp tail)", F_B, lambda z, N: z - np.log(N)/np.sqrt(2)),
                      ("C (Gauss tail)", F_C, None)]:
    for z in [3.0, 4.0]:
        for N in [4, 16]:
            target = N*m(z)
            # solve m(z') = N m(z) for z'
            lo, hi = 0.05, z
            for _ in range(200):
                mid = 0.5*(lo+hi)
                (lo, hi) = (mid, hi) if m(mid) > target else (lo, mid)
            zp = 0.5*(lo+hi)
            approx = (z - np.log(N)/np.sqrt(2)) if name.startswith("B") else np.sqrt(z*z - np.log(N))
            print(f"  {name} z={z} N={N}: exact z' = {zp:.3f}; asymptotic rule z'={'z-lnN/sqrt2' if name.startswith('B') else 'sqrt(z^2-lnN)'} = {approx:.3f}")
print("  Pooling instead: z' = sqrt(N) z (cooling).  Max size before weakest-link heats a unit to z'~1 (Gauss tail): N_max ~ e^(z^2-1)")

print("\n== 4. Heterogeneous fix speeds: aggregation of OU/AR(1) parts gives long memory (Granger 1980) ==")
def gph_d(x, frac=0.5):
    n = len(x); f, P = signal.periodogram(x - x.mean())
    m = int(n**frac); f, P = f[1:m+1], P[1:m+1]
    Xr = -np.log(4*np.sin(np.pi*f)**2)
    return np.polyfit(Xr, np.log(P), 1)[0]
Tn, Np = 2**15, 3000
def aggregate(phis):
    # Granger's setting: unit INNOVATION variance per part, stationary start
    tot = np.zeros(Tn)
    for ph in phis:
        e = rng.standard_normal(Tn)
        x0 = rng.standard_normal()/np.sqrt(1-ph**2)
        tot += signal.lfilter([1.0], [1.0, -ph], e, zi=[ph*x0])[0]
    return tot
same = aggregate(np.full(Np, 0.9))
q = 1.2  # phi^2 ~ Beta(p=1, q): Granger (1980) gives d = 1 - q/2 = 0.4
phis = np.sqrt(rng.beta(1.0, q, Np))
het = aggregate(phis)
print(f"  identical phi=0.9 parts: GPH d = {gph_d(same):.3f} (short memory, expect ~0: aggregate is AR(1) again)")
print(f"  phi^2 ~ Beta(1,{q}) parts: GPH d = {gph_d(het):.3f} (long memory if clearly > 0)")

print("\n== 5. Does a single fitted (sigma, tau) predict the aggregate's failure rate? ==")
# aggregate = fast OU (tau1) + slow OU (tau2), equal stationary variance; fit OU by lag-1 autocorr at dt;
# compare MC two-sided crossing MFPT with OU prediction tau_fit/F_C(z_fit)
def mc_mfpt_sum(tau1, tau2, s1, s2, B, dt, npaths=3000, tmax=2e5):
    # start at 0 (set point); Brownian-bridge crossing correction with the instantaneous diffusion coeff.
    a1, a2 = np.exp(-dt/tau1), np.exp(-dt/tau2)
    sig2 = 2*s1**2/tau1 + 2*s2**2/tau2
    x1 = np.zeros(npaths); x2 = np.zeros(npaths)
    t = 0.0; T = np.full(npaths, np.nan); alive = np.ones(npaths, bool)
    while alive.any() and t < tmax:
        y0 = x1 + x2
        x1 = a1*x1 + s1*np.sqrt(1-a1*a1)*rng.standard_normal(npaths)
        x2 = a2*x2 + s2*np.sqrt(1-a2*a2)*rng.standard_normal(npaths)
        y1 = x1 + x2
        pu = np.where((y0 < B) & (y1 < B), np.exp(-2*(B-y0)*(B-y1)/(sig2*dt)), 1.0)
        pl = np.where((y0 > -B) & (y1 > -B), np.exp(-2*(B+y0)*(B+y1)/(sig2*dt)), 1.0)
        hit = alive & ((rng.random(npaths) < pu) | (rng.random(npaths) < pl))
        t += dt
        T[hit] = t; alive &= ~hit
    return np.nanmean(T), alive.sum()
def fit_ou(tau1, tau2, s1, s2, dt):
    var = s1**2 + s2**2
    rho1 = (s1**2*np.exp(-dt/tau1) + s2**2*np.exp(-dt/tau2))/var
    tau_fit = -dt/np.log(rho1)
    sigma_fit = np.sqrt(2*var/tau_fit)   # OU: stationary var = sigma^2 tau/2
    return tau_fit, sigma_fit
dt = 0.01
for (tau1, tau2) in [(1.0, 1.0), (1.0, 10.0), (1.0, 100.0)]:
    s1 = s2 = np.sqrt(0.5)
    B = 2.2
    tf, sf = fit_ou(tau1, tau2, s1, s2, dt)
    zf = B/(sf*np.sqrt(tf))
    pred = tf/F_C(zf)
    mc, left = mc_mfpt_sum(tau1, tau2, s1, s2, B, dt)
    print(f"  tau1={tau1}, tau2={tau2}: fitted tau={tf:.2f}, z_fit={zf:.2f}; OU-predicted MFPT={pred:.1f}; MC MFPT={mc:.1f} (ratio MC/pred={mc/pred:.2f}; unabsorbed {left})")
    for dts in [0.05, 1.0, 10.0]:
        print(f"      fitted tau if sampled every {dts}: {fit_ou(tau1, tau2, s1, s2, dts)[0]:.2f}")
print("  (identical-tau row is the calibration; a fitted OU's tau depends on the sampling interval when taus differ)")
