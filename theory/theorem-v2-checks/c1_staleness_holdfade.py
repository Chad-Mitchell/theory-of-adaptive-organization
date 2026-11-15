"""C1. General staleness monotonicity, hold-or-fade threshold, rise-then-fall, stakes monotonicity.
Theorem G1/G2 in GENERAL_THEOREM.md.  Exact formulas + numerical optimization + Monte Carlo."""
import numpy as np
from scipy import integrate, optimize
rng = np.random.default_rng(1)
print("== C1a: staleness risk r(u) for Markov envs is nondecreasing; MA(2) counterexample ==")
# two-state CTMC, flip rate lam each way, 0-1 loss: r(u) = (1-exp(-2 lam u))/2
u = np.linspace(0, 5, 501)
r2 = 0.5*(1-np.exp(-2*u))
print("two-state chain: r nondecreasing:", bool(np.all(np.diff(r2) >= -1e-15)))
# OU (theta=1, stationary var 1), quadratic loss: r(u)=1-exp(-2u)
rou = 1-np.exp(-2*u); print("OU quadratic: r nondecreasing:", bool(np.all(np.diff(rou) >= -1e-15)))
# random 5-state reversible-or-not Markov chains, random losses: r(u)=E_x min_a sum_y P^u(x,y) l(a,y)
from scipy.linalg import expm
bad = 0
for trial in range(300):
    n = 5; Q = rng.random((n, n)); np.fill_diagonal(Q, 0); Q -= np.diag(Q.sum(1))
    w, v = np.linalg.eig(Q.T); pi = np.real(v[:, np.argmin(np.abs(w))]); pi /= pi.sum()
    L = rng.random((4, n))  # 4 actions, arbitrary loss
    rs = []
    for t in np.linspace(0, 3, 61):
        P = expm(Q*t); rs.append(sum(pi[x]*np.min(L @ P[x]) for x in range(n)))
    bad += np.any(np.diff(rs) < -1e-10)
print("random 5-state CTMCs x random losses: violations of monotonicity:", bad, "/ 300")
# MA(2): X_t = e_t + e_{t-2}. Predict X_{t+k} from X_t (linear, Gaussian => optimal). r(k)=Var(X)-Cov^2/Var
covs = {0: 2.0, 1: 0.0, 2: 1.0, 3: 0.0}
print("MA(2) prediction MSE by lag k=1,2,3:", [2.0-covs[k]**2/2.0 for k in (1, 2, 3)], "-> lag-2 reading beats lag-1: NOT monotone (non-Markov in observed coordinate)")
# MC confirm MA(2)
e = rng.standard_normal(2_000_003); X = e[2:] + e[:-2]
for k in (1, 2):
    a = np.cov(X[:-k], X[k:])[0, 1]/np.var(X); print(f"  MC lag {k}: MSE={np.mean((X[k:]-a*X[:-k])**2):.4f}")
# hops: copy chain with Gaussian noise each hop (garbling) -> MSE monotone in hops
s2, n2 = 1.0, 0.3
print("copy-chain MSE by hops 0..4:", [round(s2*(h*n2)/(s2+h*n2), 4) for h in range(5)])

print("\n== C1b: hold-or-fade threshold lam_c = Phi/c, Phi = int_0^inf (r_inf - r(u)) du ==")
def best(lam, rfun, rinf, c, F=None):
    """periodic checks every T: J = c/T + (1/T) int_0^T r(lam t) dt.  Return (f*, J*) vs fallback F (default r_inf)."""
    F = rinf if F is None else F
    def J(logT):
        T = np.exp(logT); val, _ = integrate.quad(lambda t: rfun(lam*t), 0, T, limit=200)
        return c/T + val/T
    res = optimize.minimize_scalar(J, bounds=(-12, 12), method='bounded', options={'xatol': 1e-9})
    # guard: scan grid too (non-convex cases)
    grid = np.linspace(-12, 12, 481); vals = [J(g) for g in grid]; g0 = grid[int(np.argmin(vals))]
    res2 = optimize.minimize_scalar(J, bounds=(g0-0.1, g0+0.1), method='bounded')
    r_ = res if res.fun < res2.fun else res2
    if r_.fun < F: return 1/np.exp(r_.x), r_.fun
    return 0.0, F
mu, W, c = 1.0, 1.0, 0.05
r = lambda s: mu*W*0.5*(1-np.exp(-2*s))      # two-state chain, 0-1 loss per use, use rate mu
Phi = mu*W/4; lamc = Phi/c
print(f"two-state chain: Phi={Phi}, predicted lam_c={lamc}")
for lam in [0.01, 0.1, 0.5, 1, 2, 3, 4, 4.5, 4.9, 5.1, 6, 10]:
    f, Jv = best(lam, r, mu*W*0.5, c); print(f"  lam={lam:5}: f*={f:.4f}  hold={'yes' if f>0 else 'no'}")
# small-lam asymptote f* ~ sqrt(lam r'(0)/(2c)), r'(0)=mu W
for lam in [1e-4, 1e-3]:
    f, _ = best(lam, r, 0.5, c); print(f"  small lam={lam}: f*={f:.5f} vs sqrt(lam*r'(0)/2c)={np.sqrt(lam*mu*W/(2*c)):.5f}")
print("OU quadratic loss, fixed stationary var s2=1, mean-reversion speed theta = drift speed:")
r = lambda s: 1.0*(1-np.exp(-2*s)); Phi = 0.5; print(f"  predicted theta_c = Phi/c = {Phi/c}")
for th in [0.5, 5, 9.5, 10.5]:
    f, _ = best(th, r, 1.0, c); print(f"  theta={th}: f*={f:.4f}")
print("bounded fallback F < r_inf (read the source at use) gives a CLIFF (f* jumps to 0 from >0):")
r = lambda s: mu*W*0.5*(1-np.exp(-2*s)); F = 0.3
fs = [(lam, best(lam, r, 0.5, c, F=F)[0]) for lam in np.linspace(0.2, 3.0, 29)]
last_pos = max(l for l, f in fs if f > 0); print("  last lam with hold:", round(last_pos, 3), " f* there:", round(dict(fs)[last_pos], 4),
      " next:", [round(f, 4) for l, f in fs if l > last_pos][:2])
print("\n== C1c: effort rises with stakes w (Topkis) ==")
for lam in [0.5, 2.0]:
    fsw = [best(lam, lambda s, w=w: w*0.5*(1-np.exp(-2*s)), w*0.5, c)[0] for w in [0.5, 1, 2, 4, 8]]
    print(f"  lam={lam}: f*(w=0.5..8) = {[round(x, 3) for x in fsw]}  monotone:", bool(np.all(np.diff(fsw) >= -1e-6)))
print("\n== C1d: Monte Carlo of periodic checking on two-state chain (lam=1, T=0.3) ==")
lam, T, dt = 1.0, 0.3, 1e-3; nsteps = 2_000_000
flips = rng.random(nsteps) < lam*dt; x = np.cumsum(flips) % 2
k = int(T/dt); held = x[(np.arange(nsteps)//k)*k]; mc = np.mean(held != x)*mu*W + c/T
an = c/T + integrate.quad(lambda t: 0.5*(1-np.exp(-2*lam*t)), 0, T)[0]/T
print(f"  MC J={mc:.4f}  analytic J={an:.4f}")
print("\n== C1e: approach to lam_c (blind fallback): f* -> 0 only logarithmically (near-cliff when r_inf is approached exponentially) ==")
r = lambda s: 0.5*(1-np.exp(-2*s))
for lam in [4.9, 4.99, 4.999, 4.9999]:
    print(f"  lam={lam}: f*={best(lam, r, 0.5, c)[0]:.4f}")
print("fallback F=0.3: predicted lam_c = Phi_F/c with Phi_F = int_0^{s_F}(F-r):")
sF = -0.5*np.log(1-2*0.3); PhiF = 0.3*sF - integrate.quad(r, 0, sF)[0]; print(f"  s_F={sF:.4f} Phi_F={PhiF:.5f} lam_c={PhiF/c:.4f}")
for lam in [PhiF/c*0.99, PhiF/c*1.01]:
    print(f"  lam={lam:.4f}: f*={best(lam, r, 0.5, c, F=0.3)[0]:.4f}  (predicted jump value lam_c/s_F={PhiF/c/sF:.4f})")
