"""C2. Temperature as a first-passage result. Exact formulas vs Monte Carlo; regimes where the index fails."""
import numpy as np, sympy as sp
from scipy import special, integrate, optimize
rng = np.random.default_rng(2)
def mc_bm(sig, tau, B, mu=0.0, n=200_000, steps=400, two_sided=False):
    """Brownian error from 0 over one fix window [0,tau]; Brownian-bridge crossing correction between grid points."""
    dt = tau/steps; x = np.zeros(n); hit = np.zeros(n, bool)
    for _ in range(steps):
        xn = x + mu*dt + sig*np.sqrt(dt)*rng.standard_normal(n)
        pc = np.exp(-2*np.clip(B-x, 0, None)*np.clip(B-xn, 0, None)/(sig**2*dt))
        if two_sided: pc = pc + np.exp(-2*np.clip(B+x, 0, None)*np.clip(B+xn, 0, None)/(sig**2*dt))
        hit |= (xn >= B) | (rng.random(n) < pc) | ((xn <= -B) if two_sided else False)
        x = xn
    return hit.mean()
P1 = lambda z: special.erfc(1/(z*np.sqrt(2)))                     # one-sided, reflection principle
def S2(z, K=200):                                                   # two-sided survival in (-B,B) to tau
    k = np.arange(K); return (4/np.pi)*np.sum((-1)**k/(2*k+1)*np.exp(-(2*k+1)**2*np.pi**2*z**2/8))
P2 = lambda z: 1-S2(z)
def mlogS2(z):                                                      # -ln survival, stable for large z
    return np.pi**2*z**2/8 - np.log(4/np.pi) if z > 3 else -np.log(S2(z))
print("== C2a: one-sided P(max_{t<=tau} sigma W_t >= B) = erfc(B/(sigma sqrt(2 tau))) = 2 Phibar(1/z), z = sigma sqrt(tau)/B ==")
for (s, t, B) in [(1, 1, 1), (2, 0.25, 1), (0.5, 4, 1), (1, 1, 2), (3, 1, 2)]:
    z = s*np.sqrt(t)/B; print(f"  sigma={s} tau={t} B={B}  z={z:.3f}  exact={P1(z):.4f}  MC={mc_bm(s, t, B):.4f}")
print("  collapse: same z=0.5 from different (sigma,tau,B):", [round(mc_bm(s, t, B), 4) for s, t, B in [(1, 1, 2), (0.5, 4, 2), (2, 0.0625, 1)]], "exact", round(P1(0.5), 4))
print("== C2b: two-sided exit series (Feller) vs MC ==")
for z in [0.3, 0.6, 1.0, 2.0]:
    print(f"  z={z}: series={P2(z):.4f}  MC={mc_bm(z, 1, 1, two_sided=True):.4f}")
print("== C2c: drift mu in the error (systematic bias): Bachelier-Levy  P = Phibar((B-mu t)/(s sqrt t)) + e^{2 mu B/s^2} Phibar((B+mu t)/(s sqrt t)) ==")
Phib = lambda x: 0.5*special.erfc(x/np.sqrt(2))
for mu in [-1.0, 0.5, 1.0]:
    s, t, B = 1, 1, 1.5; ex = Phib((B-mu*t)/(s*np.sqrt(t))) + np.exp(2*mu*B/s**2)*Phib((B+mu*t)/(s*np.sqrt(t)))
    print(f"  mu={mu}: exact={ex:.4f} MC={mc_bm(s, t, B, mu=mu):.4f}   (second group Pe = mu B/s^2 = {mu*B/s**2})")
print("  same z, different Pe => different ruin:", round(Phib((1.5-0)/1)+Phib(1.5), 4), "vs", round(Phib((1.5-1)/1)+np.exp(3)*Phib(2.5), 4), " -> z alone is NOT sufficient once errors are biased")
print("== C2d: hazard per unit time with resets every tau, in diffusion units B^2/sigma^2:  h B^2/sigma^2 = G(z) = -ln(1-P(z))/z^2 ==")
zs = np.array([0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 5, 10, 30])
print("  z      :", zs)
print("  G2(z)  :", np.round([mlogS2(z)/z**2 for z in zs], 4), " (two-sided; limit pi^2/8 =", round(np.pi**2/8, 4), ")")
print("  G1(z)  :", np.round([-np.log(1-P1(z))/z**2 for z in zs], 4), " (one-sided; ->0 as z->inf, non-monotone)")
print("  => two-sided: for z >~ 1.5 hazard is within ~10% of pi^2 sigma^2/(8B^2): the fix interval stops mattering in the hot regime.")
print("== C2e: where does slow fixing hurt most? (one fix window) ==")
z = sp.symbols('z', positive=True); P = sp.erfc(1/(z*sp.sqrt(2)))
dPz = sp.diff(P, z); el = sp.simplify(z/2*dPz)   # dP/dln tau = (z/2) dP/dz
print("  argmax_z dP/dz        :", sp.nsolve(sp.diff(dPz, z), z, 0.7), " (exact 1/sqrt2 =", round(1/np.sqrt(2), 6), ")")
print("  argmax_z dP/dln(tau)  :", sp.nsolve(sp.diff(el, z), z, 1.0), " (exact 1)")
print("  dP/dln(tau) at z=0.25,0.5,1,2,4,8:", [round(float(el.subs(z, v)), 4) for v in [0.25, 0.5, 1, 2, 4, 8]])
dl = [(-np.log(1-P2(v*1.0001))/(v*1.0001)**2*0 ) for v in [1]]
# calendar hazard elasticity wrt tau (two-sided), at fixed sigma,B: h = (s^2/B^2) G(z), z ~ sqrt(tau): d ln h / d ln tau = (1/2) dlnG/dlnz
for v in [0.2, 0.3, 0.5, 1, 2, 4]:
    e = 1e-4; G = lambda q: mlogS2(q)/q**2
    print(f"  two-sided calendar-hazard elasticity d ln h/d ln tau at z={v}: {0.5*(np.log(G(v*(1+e)))-np.log(G(v)))/np.log(1+e):.3f}")
print("== C2f: continuous correction (OU, rate 1/tau) instead of resets. Large-barrier MFPT T ~ tau sqrt(pi) z e^{1/z^2} ==")
def mfpt_ou(sig, tau, a):
    th = 1/tau; V = lambda y: th*y**2/sig**2
    inner = lambda y: integrate.quad(lambda q: np.exp(-V(q)+V(y)), -np.inf, y)[0]  # e^{V(y)} int e^{-V}
    return 2/sig**2*integrate.quad(inner, 0, a, limit=200)[0]
for (s, t, a) in [(1, 1, 2.0), (2, 0.25, 2.0), (1, 1, 3.0), (0.5, 4, 1.5)]:
    zz = s*np.sqrt(t)/a; T = mfpt_ou(s, t, a)
    print(f"  sigma={s} tau={t} B={a} z={zz:.3f}: MFPT/tau={T/t:.3f}  asymptote sqrt(pi) z e^(1/z^2)={np.sqrt(np.pi)*zz*np.exp(1/zz**2):.3f}")
print("  (rows 1,2 share z and give identical MFPT/tau: the group sigma sqrt(tau)/B is forced by dimensional analysis)")
print("== C2g: heavy-tailed jumps (compound Poisson, Pareto alpha=1.5 sizes, rate lam) + small diffusion: tau barely matters ==")
def mc_jump(lam, xm, al, sig, tau, B, n=200_000):
    N = rng.poisson(lam*tau, n); hit = np.zeros(n, bool); x = np.zeros(n)
    # order statistics are irrelevant for one-sided max when jumps are positive? jumps can be +/-; use symmetric signs
    maxN = N.max(); times = np.sort(rng.random((n, maxN))*tau, axis=1)
    sizes = xm*(rng.random((n, maxN))**(-1/al))*np.where(rng.random((n, maxN)) < 0.5, -1, 1)
    sizes[np.arange(maxN)[None, :] >= N[:, None]] = 0
    # diffusion between jumps approximated by evaluating at jump times + endpoint and bridge correction ignored (sig small)
    prev_t = np.zeros(n)
    for j in range(maxN):
        dtj = times[:, j]-prev_t; x = x + sig*np.sqrt(dtj)*rng.standard_normal(n); hit |= np.abs(x) >= B
        x = x + sizes[:, j]; hit |= np.abs(x) >= B; prev_t = times[:, j]
    x = x + sig*np.sqrt(tau-prev_t)*rng.standard_normal(n); hit |= np.abs(x) >= B
    return hit.mean()
lam, xm, al, sig, B = 2.0, 0.05, 1.5, 0.02, 1.0
for tau in [0.25, 0.5, 1, 2, 4]:
    p = mc_jump(lam, xm, al, sig, tau, B); h = -np.log(1-p)/tau
    print(f"  tau={tau}: per-window P={p:.4f}  calendar hazard={h:.4f}   single-big-jump rate lam*P(|J|>B)={lam*(xm/B)**al:.4f}")
print("  => calendar-hazard elasticity wrt tau ~0.14 here (vs 1.5-12 for diffusive errors at z<=0.5): failure is set by the jump tail, not by sqrt(tau).")
print("== C2h: long-memory shocks (fractional BM, H=0.75): the group is sigma tau^H / B, not sigma sqrt(tau)/B ==")
def fbm_max_hit(H, sig, tau, B, n=40_000, steps=256):
    t = np.linspace(tau/steps, tau, steps); TT, SS = np.meshgrid(t, t)
    C = 0.5*(TT**(2*H)+SS**(2*H)-np.abs(TT-SS)**(2*H)); Lc = np.linalg.cholesky(C+1e-12*np.eye(steps))
    X = sig*(rng.standard_normal((n, steps)) @ Lc.T); return np.mean(X.max(1) >= B)
H = 0.75
a = fbm_max_hit(H, 1, 1, 1.5); b = fbm_max_hit(H, 1*(4**-H), 4, 1.5); cc = fbm_max_hit(H, 0.5, 4, 1.5)
print(f"  (sigma,tau)=(1,1): {a:.4f};  (4^-H,4) same sigma tau^H: {b:.4f};  (0.5,4) same sigma sqrt(tau): {cc:.4f}")
print("== C2i: fixes that don't fully reset (error multiplied by (1-k) at each fix): stationary pre-fix variance sigma^2 tau/(k(2-k)) ==")
def mc_partial(sig, tau, B, k, windows=400, n=20_000, steps=40):
    x = np.zeros(n); alive = np.ones(n, bool); dt = tau/steps
    for wdw in range(windows):
        for _ in range(steps):
            x = x + sig*np.sqrt(dt)*rng.standard_normal(n); alive &= np.abs(x) < B
        x = (1-k)*x
    return -np.log(alive.mean())/(windows*tau)
for k in [1.0, 0.5, 0.2]:
    h = mc_partial(0.25, 1, 1, k, windows=100); zeff = 0.25/np.sqrt(k*(2-k)); href = mc_partial(zeff, 1, 1, 1.0, windows=100)
    print(f"  k={k}: calendar hazard={h:.5f}   z_eff={zeff:.3f}; full-reset hazard at sigma=z_eff: {href:.5f}")
print("  => with partial fixes the index needs roughly tau/(k(2-k)) (approximation good to ~2x at k=0.2): measured 'time to close' is not the variable the index needs.")
print("== C2j: units-free consistency test against C3 (896 projects). In the reset model the per-window ruin is h*tau = -ln S(z), so h and tau alone pin z ==")
h = -np.log(1-137/896)/2.33; print(f"  C3 coding A: hazard h = {h:.4f}/yr (137 events / 896, 2.33-yr window; literal coding 105 events gives {-np.log(1-105/896)/2.33:.4f})")
for tau_days in [7, 44, 180, 546]:
    t = tau_days/365.25; target = h*t
    zz = optimize.brentq(lambda q: mlogS2(q)-target, 0.05, 50)
    e = 1e-4; G = lambda q: mlogS2(q)/q**2; el = 0.5*(np.log(G(zz*(1+e)))-np.log(G(zz)))/np.log(1+e)
    phi_max = (np.exp(0.693*0.12)-1)/(2**el-1)
    print(f"  tau={tau_days:4d} d: implied z={zz:.3f}; predicted hazard elasticity d ln h/d ln tau = {el:.2f} -> HR per doubling of tau = {2**el:.2f};"
          f" observed upper CI 1.087 caps the diffusive share of hazard at {100*min(phi_max,1):.1f}%")
print("  => if dormancy were diffusive first passage reset every 'time to close', slow fixers would die several-fold faster. C3 rules that out:")
print("     at most a few percent of dormancy hazard can come from that mechanism (conditional on tau measuring the fix interval).")
