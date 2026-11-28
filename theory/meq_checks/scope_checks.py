"""Scope checks for THEORY v2.4 (answers to the independent review of v2.3): nice -n 19 python3 scope_checks.py ; ends RESULT: PASS.
 1  CT33  judgment SPEND rises with stakes even when the layer count can fall (reads substitute for layers)   [review B1]
 2  CT34  when a team's optimized cost enters the parent's problem exactly (as upkeep), and the error bound when it does not   [review B4]
 3  CT24  shares = elasticities fails when a ruin constraint binds, holds when it is slack or price-free   [review B3]
 4  CT21  a rhythm (complex pole) needs two layers by degree; real first-order stores need unbounded counts   [review B2]
 5  S1    the alpha-1 look-to-wrong ratio holds for exact reads of a power-law world, not with noisy reads   [review S1]
 6  S5    CT25 is a per-window statement; over a fixed horizon the survivable-shock elasticity is not exactly -1/2   [review S5]
 7  S6    CT29 adaptation threshold 2/N holds for N EQUAL parties (reads clipped at 0); not derived for unequal stakes   [review S6]
 8  S11   L2 interlacing a_1 < b_1 < a_2 < ... : every layer is faster than its mode (proved by sign changes, checked on random worlds)
 9  CT32  (iii) 'time-scale separation' changes which stationary point gradient play reaches, but that point is not a Nash equilibrium when the slow cost is concave; with convex own costs the speed ratio never changes stability   [review 24 B2]
 1b CT33  with the master equation's own RUIN constraint binding, spend CAN fall and error rise as stakes rise (the feasible set depends on the stake)   [review 24 B1]"""
import os, sys, json
import numpy as np
from scipy.optimize import minimize_scalar, minimize, brentq
from scipy.stats import norm
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
bad = []
def chk(name, cond):
    if not cond: bad.append(name); print('  FAIL', name)
rng = np.random.default_rng(24)

print("== 1. CT33: with read rates chosen, layers can FALL as stakes rise, but total judgment spend S* = h*K* + (read price)*(reads) cannot")
c, h = 1.0, 0.05
E1 = lambda f: 1 / f
E2 = lambda f: np.minimum(1 / f, 0.5 + 0.01 / f)         # the reviewer's nested classes: E2 <= E1; a trend store helps only while reads are rare
def best(E, w):
    r = minimize_scalar(lambda lf: c * np.exp(lf) + w * E(np.exp(lf)), bounds=(-15, 15), method='bounded', options={'xatol': 1e-12})
    return r.fun, c * np.exp(r.x), E(np.exp(r.x))
print("  w/h     K*   S*=hK+c*f   E*      J*")
rows = []
for r_ in (1, 2, 5, 10, 20, 50, 100, 200, 400, 1000, 4000, 20000):
    w = r_ * h; G1, f1, e1 = best(E1, w); G2, f2, e2 = best(E2, w)
    J1, J2 = h + G1, 2 * h + G2
    K = 1 if J1 <= J2 else 2; S = h * K + c * (f1 if K == 1 else f2); E = e1 if K == 1 else e2; J = min(J1, J2)
    rows.append((r_, K, S, E, J)); print(f"  {r_:6d}  {K}    {S:9.4f}  {E:.5f}  {J:.4f}")
Ks = [r[1] for r in rows]; Ss = np.array([r[2] for r in rows]); Es = np.array([r[3] for r in rows])
chk('counterexample: K falls', any(Ks[i + 1] < Ks[i] for i in range(len(Ks) - 1)))
chk('counterexample: S nondecreasing', np.all(np.diff(Ss) >= -1e-9)); chk('counterexample: E nonincreasing', np.all(np.diff(Es) <= 1e-9))
dstar = brentq(lambda r: (h + best(E1, r * h)[0]) - (2 * h + best(E2, r * h)[0]), 250, 300)
print(f"  the one-layer and two-layer designs cost the same at w/h = {dstar:.1f}: K* = 2 up to about 250, K* = 1 from about 260")
chk('crossing near 255', 250 < dstar < 260)
print("  layers fall (K: " + "".join(map(str, Ks)) + ") while spend rises and error falls: reads substitute for the second layer")
# general statement: any finite design menu d with spend S(d) and error E(d); J = S + w E
ok = True
for t in range(300):
    n = rng.integers(2, 40); S = rng.uniform(0, 10, n); E = rng.uniform(0, 5, n); ws = np.sort(rng.uniform(0, 20, 60))
    J = S[None, :] + ws[:, None] * E[None, :]; i = J.argmin(1)           # argmin picks the first minimizer; ties are measure zero here
    Js, Ssel, Esel = J.min(1), S[i], E[i]
    ok &= bool(np.all(np.diff(Ssel) >= -1e-12) and np.all(np.diff(Esel) <= 1e-12))
    # envelope: J*(w) concave, slope E*
    ok &= bool(np.all(np.diff(Js) / np.diff(ws) <= np.r_[Esel[:-1]] + 1e-9)) and bool(np.all(np.diff(Js) / np.diff(ws) >= Esel[1:] - 1e-9))
chk('random menus: S nondecr, E nonincr, J* between slopes', ok); print(f"  300 random design menus (any size, any E, S): spend nondecreasing, error nonincreasing, J* slopes bracket E*: {ok}")
# the proof is two inequalities: w1 < w2, optima d1, d2:  S1 + w1 E1 <= S2 + w1 E2  and  S2 + w2 E2 <= S1 + w2 E1  ==>  (w2-w1)(E2-E1) <= 0  and  S2 - S1 >= w1 (E1 - E2) >= 0.
# not true when the upkeep h falls at a fixed stake w (cheaper layers): hK* can fall; in units of h, with price ratios fixed, it is the same problem as raising w/h.
Es_ = lambda K: 1.0 / K
Sf = []
for hh in (1.0, 0.25, 0.0625):
    Ks_ = np.arange(1, 400); J = hh * Ks_ + 100.0 * Es_(Ks_); k = Ks_[J.argmin()]; Sf.append(hh * k)
print(f"  upkeep falling at fixed stake (E_K = 1/K, w = 100): spend h*K* = {np.round(Sf, 3)} falls, so the statement is about stakes at fixed prices (or w/h in units of h), not about h alone")
chk('spend can fall when h falls at fixed w', Sf[0] > Sf[-1])
# (1b) the master equation also carries the ruin constraint theta(D)*B >= ln(1/eps) with the reserve paying J; the feasible set then depends on w.
#      the reviewer's case: diffusion reserve, income y = 20, theta = 2(y - J)/sigma^2 >= 1;  D1: S=1, E=1, sigma^2 = 0.01 w^2;  D2: S=3, E=0.5, sigma^2 = 0.2 w^2
def ruin_opt(w):
    best_ = None
    for nm, S_, E_, v in (('D1', 1.0, 1.0, 0.01), ('D2', 3.0, 0.5, 0.2)):
        J_ = S_ + w * E_
        if 2 * (20.0 - J_) / (v * w ** 2) >= 1.0 and (best_ is None or J_ < best_[0]): best_ = (J_, nm, S_, E_)
    return best_
print("  (1b) with a BINDING ruin constraint (y=20, theta>=1), judgment spend can fall and error rise as stakes rise:")
seq = []
for w in (2, 4, 6, 8, 10, 11, 14, 16):
    o = ruin_opt(w); seq.append(o); print(f"       w={w:3d}: best feasible {o[1]}  S*={o[2]}  E*={o[3]}  J*={o[0]:.2f}")
chk('ruin-binding counterexample: S falls and E rises', seq[-1][2] < max(o[2] for o in seq) and seq[-1][3] > min(o[3] for o in seq))
print("       so CT33 and Master Theorem (ii) are statements for the ruin constraint slack at the stakes compared (B >= B_slack) or absent.")
# (1c) the face map (records/figures/face_map.py): along rising stakes the chosen design's upkeep never falls and its error never rises
sys.path.insert(0, os.path.join(ROOT, 'figures')); import face_map as fm
okS = True; rng_ = np.random.default_rng(33)
for _ in range(300):
    GL_, GS_ = rng_.uniform(0.05, 1, 2); GB_ = rng_.uniform(max(GL_, GS_), GL_ + GS_); n_, hc_ = int(10 ** rng_.uniform(0, 3)), 10 ** rng_.uniform(-1, 2.5)
    up_ = [0, n_, hc_, n_ + hc_]; er_ = [1, 1 - GL_, 1 - GS_, 1 - GB_]; last_ = None
    for wu_ in np.logspace(-2, 5, 200):
        d_ = int(fm.decide(wu_ * GL_, n_ * wu_ * GS_ / hc_, n_ / hc_, (GB_ - GS_) / GL_, (GB_ - GL_) / GS_))
        if last_ is not None: okS &= up_[d_] >= up_[last_] - 1e-12 and er_[d_] <= er_[last_] + 1e-12
        last_ = d_
print(f"  face map (300 random worlds, ruin slack): upkeep of the chosen design never falls and its error never rises as stakes rise: {okS}")
chk('face map: CT33 along stakes', okS)

print("\n== 2. CT34: a team's optimized cost enters the parent's problem exactly as upkeep if (generically only if) the parent sees the team only through quantities fixed before the team optimizes")
# (a) partial minimisation identity  min_{x,y} F(x)+G(y; theta(x)) = min_x [ F(x) + J*_T(theta(x)) ], exact; J*_T acts as a constant iff theta does not depend on x
c0, q, al = 0.7, 1.3, 2.0
def JT(W):                                       # team = one tracker, exact reads (CT12), pooled stake W; J*_T(W) = min_T c/T + W q T^(al-1)/al
    r = minimize_scalar(lambda lt: c0 * np.exp(-lt) + W * q * np.exp((al - 1) * lt) / al, bounds=(-20, 20), method='bounded', options={'xatol': 1e-13}); return r.fun
W0, v0 = 50.0, 0.8
Fp = lambda x: (1 - x) * W0 * v0 + 40.0 * x ** 2           # parent keeps (1-x) of the stake and pays 40 x^2 to manage the team's share x
xs = np.linspace(0.0, 1.0, 2001)
Jred = np.array([Fp(x) + JT(max(x * W0, 1e-12)) for x in xs]); ired = Jred.argmin()
Ts = np.exp(np.linspace(-8, 4, 1201)); best_joint = np.inf
for x in xs[::20]:
    W = max(x * W0, 1e-12); J_T = c0 / Ts + W * q * Ts ** (al - 1) / al; best_joint = min(best_joint, (Fp(x) + J_T).min())
print(f"  parent+team joint min (grid over x, T) = {best_joint:.5f};  reduced problem F(x)+J*_T(theta(x)) at its argmin x={xs[ired]:.3f}: {Jred[ired]:.5f}")
chk('reduced = joint (grid)', abs(best_joint - Jred.min()) < 5e-3 and 0.0 < xs[ired] < 1.0)
Tst = (c0 / (25.0 * q * (al - 1) / al)) ** (1 / al); dJ = (JT(25.0 + 1e-4) - JT(25.0 - 1e-4)) / 2e-4
print(f"  envelope: dJ*_T/dW = {dJ:.6f} = q*T*^(alpha-1)/alpha = {q * Tst ** (al - 1) / al:.6f} (the team's own error per unit stake)")
chk('envelope', abs(dJ - q * Tst ** (al - 1) / al) < 1e-6)
# when theta is fixed (stake passed down does not depend on x) the parent's argmin ignores the team entirely: J*_T is an additive constant = upkeep
Jc = np.array([Fp(x) for x in xs]); Jc_ = Jc + JT(W0); chk('constant theta: argmin unchanged', Jc.argmin() == Jc_.argmin())
print("  (b) stake-passing exogenous: parent's argmin x* is the same with or without the team's problem; J*_T is the upkeep h (exact).")
print("      stake-passing endogenous: J*_T(theta(x)) is a value function of the parent's choice (still exact, no longer a constant).")
# (c) approximation: J(x,y) = F(x) + G(y) + eps*Phi(x,y), G mu-strongly convex, Phi L-Lipschitz in y.   Freeze the team at y0 = argmin G.
print("  (c) error bound when the team is frozen at its stand-alone optimum and the coupling eps*Phi is switched on:  0 <= m0(x) - m(x) <= (eps L)^2/(2 mu),  parent regret <= (eps L)^2/(2 mu)")
mu = 2.0
G = lambda y: 0.5 * mu * (y - 0.3) ** 2; Fx = lambda x: (x - 1.0) ** 2 + 0.2 * x
Phi = lambda x, y: np.sin(2 * y + x) + 0.5 * x * y; Lip = 2.0 + 0.5 * 1.0   # |dPhi/dy| <= 2 + 0.5|x|, x in [0,1]
xg = np.linspace(0, 1, 201); yg = np.linspace(-3, 3, 2401); y0 = 0.3; rows = []
for eps in (0.4, 0.2, 0.1, 0.05, 0.025):
    m = np.array([(Fx(x) + G(yg) + eps * Phi(x, yg)).min() for x in xg]); m0 = np.array([Fx(x) + G(y0) + eps * Phi(x, y0) for x in xg])
    bound = (eps * Lip) ** 2 / (2 * mu); gap = (m0 - m).max(); x0 = xg[m0.argmin()]; regret = (Fx(x0) + G(yg) + eps * Phi(x0, yg)).min() - m.min()
    rows.append((eps, gap, regret, bound)); chk(f'bound holds eps={eps}', gap <= bound + 1e-9 and regret <= bound + 1e-9 and gap >= -1e-12)
    print(f"      eps={eps:5.3f}: worst gap {gap:.2e}  regret {regret:.2e}  bound {bound:.2e}")
sl = np.polyfit(np.log([r[0] for r in rows]), np.log([r[1] for r in rows]), 1)[0]
print(f"      the worst gap scales as eps^{sl:.2f}: second order in the coupling (the bound is eps^2 by construction)")
chk('gap second order', 1.8 < sl < 2.4)
# (d) a real shared driver is NOT small coupling: N units with common-driver share rho; treating each as an independent upkeep misses the pooling gain
def steady_mse(F, Q, H, R, iters=20000):
    P = np.eye(len(F)) * 10.0
    for _ in range(iters):                                    # predict, update, until the posterior covariance stops moving
        Pm = F @ P @ F.T + Q; K = Pm @ H.T @ np.linalg.inv(H @ Pm @ H.T + R); Pn = Pm - K @ H @ Pm
        if np.max(np.abs(Pn - P)) < 1e-15: P = Pn; break
        P = Pn
    return P
qtot, r_, N = 0.02, 0.5, 4
print("  (d) N=4 units, drift variance 0.02 per step split into shared share rho and own share (1-rho); per-unit steady error, local filters vs one pooled filter")
gains = []
for rho in (0.0, 0.1, 0.3, 0.6, 1.0):
    # state: [g, u_1..u_N]; unit i sees y_i = sqrt(rho)*g + sqrt(1-rho)*u_i + noise, signal s_i = same combination without noise
    n = N + 1; F = np.eye(n); Q = np.diag([qtot * rho] + [qtot * (1 - rho)] * N)
    # model the signals as random walks with those drifts (g, u_i) and measure each y_i = g + u_i (g, u_i carry their own scales)
    H = np.hstack([np.ones((N, 1)), np.eye(N)]); Pp = steady_mse(F, Q, H, r_ * np.eye(N))
    a = np.r_[1.0, np.zeros(N)]; vloc = []
    s_err = np.mean([ (np.r_[1.0, np.eye(N)[i]]) @ Pp @ (np.r_[1.0, np.eye(N)[i]]) for i in range(N)])
    # local filter: scalar random walk with total drift qtot and noise r_
    Pl = steady_mse(np.eye(1), np.array([[qtot]]), np.eye(1), np.array([[r_]]))[0, 0]; Vl = Pl
    gains.append((rho, Vl, s_err, Vl - s_err))
    print(f"      rho={rho:3.1f}: local {Vl:.5f}  pooled {s_err:.5f}  pooling gain {Vl - s_err:.5f}")
chk('pooling gain zero at rho=0, positive at rho>0', abs(gains[0][3]) < 1e-9 and gains[2][3] > 1e-4)

print("\n== 3. CT24: share = elasticity needs a price-free constraint set; with a BINDING ruin constraint it fails (Lemma B9 setting)")
y, s0, sg, eps_r = 1.0, 0.3, 1.0, 1e-3
def solve(cc, ww, Bf):
    m = lambda t: y - cc / t - ww * sg ** 2 * t / 2; s2 = lambda t: s0 ** 2 + ww ** 2 * sg ** 4 * t ** 3 / 3; th = lambda t: 2 * m(t) / s2(t)
    tE = np.sqrt(2 * cc / (ww * sg ** 2)); need = np.log(1 / eps_r) / Bf
    if th(tE) >= need: t = tE
    else:
        tS = minimize_scalar(lambda t: -th(t), bounds=(1e-3, 3), method='bounded', options={'xatol': 1e-13}).x
        t = brentq(lambda t: th(t) - need, tS, tE, xtol=1e-14)
    return cc / t + ww * sg ** 2 * t / 2, cc / t, ww * sg ** 2 * t / 2
for Bf, name in ((0.5, 'binding'), (5.0, 'slack')):
    c_, w_ = 0.05, 1.0; J_, a_, b_ = solve(c_, w_, Bf); hh = 1e-5
    ec = (np.log(solve(c_ * (1 + hh), w_, Bf)[0]) - np.log(solve(c_ * (1 - hh), w_, Bf)[0])) / (2 * hh)
    ew = (np.log(solve(c_, w_ * (1 + hh), Bf)[0]) - np.log(solve(c_, w_ * (1 - hh), Bf)[0])) / (2 * hh)
    print(f"  B={Bf} ({name}): shares read {a_/J_:.4f} error {b_/J_:.4f}; elasticities c {ec:.4f} w {ew:.4f}; sum of elasticities {ec+ew:.4f}")
    if name == 'binding': chk('binding ruin: elasticities exceed shares, sum != 1', abs(ec + ew - 1) > 0.1 and abs(ec - a_ / J_) > 0.03)
    else: chk('slack ruin: shares = elasticities', abs(ec - a_ / J_) < 1e-4 and abs(ec + ew - 1) < 1e-4)
print("  so the ruin constraint's feasible set depends on the prices (the reserve pays J) and on income y and buffer B: Euler runs over (c, w, y, B) jointly when it binds.")

print("\n== 4. CT21 (iii): a rhythm (lightly damped oscillator, complex poles) seen through noise")
w0_, z_, vv, Nn = 1.0, 0.05, 0.1, 1.0
b0 = np.sqrt(w0_ ** 4 + vv / Nn); b1 = np.sqrt((4 * z_ ** 2 - 2) * w0_ ** 2 + 2 * b0)
om = np.concatenate([-np.logspace(-4, 4, 3001)[::-1], np.logspace(-4, 4, 3001)]); S = vv / ((w0_ ** 2 - om ** 2) ** 2 + 4 * z_ ** 2 * w0_ ** 2 * om ** 2)
def E_of(Hf): return np.trapezoid((np.abs(1 - Hf) ** 2 * S + np.abs(Hf) ** 2 * Nn), om) / (2 * np.pi)
s = 1j * om; p = s ** 2 + 2 * z_ * w0_ * s + w0_ ** 2; pt = s ** 2 + b1 * s + b0
Einf = E_of((pt - p) / pt)
print(f"  Wiener filter denominator s^2 + {b1:.4f} s + {b0:.4f}: discriminant {b1**2-4*b0:.3f} < 0, so complex poles, McMillan degree 2; E_inf = {Einf:.5f}")
chk('complex filter poles', b1 ** 2 - 4 * b0 < 0)
def best_real(K, starts=12):
    rr = np.random.default_rng(K); bst = np.inf
    def f(x):
        b = np.exp(x[:K]); g = x[K:]; Hf = sum(g[k] * b[k] / (b[k] + s) for k in range(K)); return E_of(Hf)
    for st in range(starts):
        x0 = np.concatenate([rr.uniform(-3, 2, K), rr.normal(0, 0.5, K)])
        r0 = minimize(f, x0, method='Nelder-Mead', options={'maxiter': 3000, 'xatol': 1e-9, 'fatol': 1e-11}); r0 = minimize(f, r0.x, method='Nelder-Mead', options={'maxiter': 3000, 'xatol': 1e-10, 'fatol': 1e-13})
        bst = min(bst, r0.fun)
    return bst
exc = [best_real(K) / Einf - 1 for K in (1, 2, 3)]
print("  real first-order stores K=1,2,3: excess over the degree-2 optimum", [f"{e:.1%}" for e in exc], "(never zero: counted by degree a rhythm is 2 layers; counted as real stores it needs ever more)")
chk('real stores never exact', all(e > 0.05 for e in exc) and exc[0] > exc[1] > exc[2])

print("\n== 5. S1: look : wrong = alpha - 1 for exact reads of a power-law world; not with noisy reads")
for a_ in (1.3, 2.0, 2.7):
    cc, ww, qq = 2.0, 0.3, 1.1; f = lambda lt: cc * np.exp(-lt) + ww * qq * np.exp((a_ - 1) * lt) / a_
    T = np.exp(minimize_scalar(f, bounds=(-30, 30), method='bounded', options={'xatol': 1e-13}).x)
    ratio = (cc / T) / (ww * qq * T ** (a_ - 1) / a_); chk(f'exact reads alpha={a_}', abs(ratio - (a_ - 1)) < 1e-6)
    print(f"  alpha={a_}: look/wrong = {ratio:.6f} (alpha-1 = {a_-1:.1f})")
def kal(T, r, s2=1.0): return brentq(lambda P: P - (P + s2 * T) * r / (P + s2 * T + r), 0, 1e9)
vals = []
for r_ in (0.1, 1.0, 10.0):
    J = lambda lt: 1.0 * np.exp(-lt) + 100.0 * (kal(np.exp(lt), r_) + np.exp(lt) / 2)
    o = minimize_scalar(J, bounds=(-12, 12), method='bounded', options={'xatol': 1e-11}); T = np.exp(o.x); vals.append((1.0 / T) / (o.fun - 1.0 / T))
print("  random walk read through noise (Kalman), c=1, w=100: look/wrong =", np.round(vals, 3), "(exact-read value 1)")
chk('noisy reads break the ratio', vals[0] < 0.9 and vals[-1] < 0.6)

print("\n== 6. S5: CT25 is per fixing window; over a horizon T_h the window count grows as tau falls")
Th, eps = 100.0, 1e-3; taus = np.array([1.0, 0.01]); zs = norm.isf((1 - (1 - eps) ** (taus / Th)) / 2); smax = 1 / (zs * np.sqrt(taus))
el = np.log(smax[0] / smax[1]) / np.log(taus[0] / taus[1]); print(f"  survivable-shock elasticity in tau over [0.01, 1] at horizon 100: {el:.3f} (per-window: -0.5)")
chk('horizon elasticity not -0.5', abs(el + 0.5) > 0.02 and el > -0.5)

print("\n== 7. S6: CT29 best-response adaptation f <- f + lam (BR - f), reads clipped at 0")
def adapt(w, lam, f0, steps=4000):
    f = f0.copy(); Fh = np.sqrt(w)
    for t in range(steps):
        br = np.maximum(0, Fh - (f.sum() - f)); f = np.maximum(0, f + lam * (br - f))
    return f
for Nn_ in (3, 5):
    for frac in (0.95, 1.05):
        res = [adapt(np.ones(Nn_), frac * 2 / Nn_, rng.uniform(0, 3, Nn_)).sum() for _ in range(30)]
        conv = np.mean(np.abs(np.array(res) - 1) < 1e-7); print(f"  N={Nn_} equal stakes, lam = {frac}*2/N: converged {conv:.0%} of 30 random starts")
        chk(f'equal stakes 2/N N={Nn_} {frac}', (conv == 1.0) if frac < 1 else (conv == 0.0))
w3 = np.array([1.0, 2.0, 4.0]); out = []
for lam in (0.6, 0.9, 1.5, 1.9):
    out.append((lam, adapt(w3, lam, np.array([0.2, 0.2, 0.2]))))
print("  unequal stakes (1,2,4), clipped: " + "; ".join(f"lam={l}: total {f.sum():.3f}" for l, f in out) + f"  (Nash total {np.sqrt(4):.3f}); threshold not derived")

print("\n== 8. S11: interlacing of the filter roots with the mode rates (proof: N + sum_j c_j/(x + a_j^2) changes sign between consecutive poles)")
ok = True
for t in range(200):
    J = rng.integers(2, 8); a = np.sort(np.exp(rng.uniform(-3, 3, J))); v = rng.uniform(0.1, 2, J); Nn = np.exp(rng.uniform(-3, 1))
    # numerator of N + sum 2 a_j v_j/(a_j^2 + w^2) in x = w^2: roots are -b_j^2
    num = np.poly1d([0.0]); den = np.poly1d([1.0])
    for aa in a: den = den * np.poly1d([1.0, aa ** 2])
    num = den * float(Nn)
    for j, aa in enumerate(a):
        o = np.poly1d([1.0])
        for k, ab in enumerate(a):
            if k != j: o = o * np.poly1d([1.0, ab ** 2])
        num = num + o * float(2 * aa * v[j])
    roots = np.sort(np.sqrt(-np.real(num.r)))
    good = all(a[j] < roots[j] < a[j + 1] for j in range(J - 1)) and roots[-1] > a[-1] and np.allclose(num.r.imag, 0, atol=1e-7)
    ok &= bool(good)
chk('interlacing a_j < b_j < a_{j+1}, b_J > a_J', ok); print(f"  200 random worlds (J = 2..7 modes): roots b_j satisfy a_j < b_j < a_(j+1) and b_J > a_J: {ok}")

print("\n== 9. B2 (review 24): CT32 (iii): J1 = x1 x2 - (m/2) x1^2 is CONCAVE in the slow party's own action, so the rest point (0,0) is not a Nash equilibrium")
m_ = 1.0; J1 = lambda x1, x2: x1 * x2 - m_ / 2 * x1 ** 2
gain = J1(0.0, 0.0) - J1(1.0, 0.0); print(f"  party 1 deviating from 0 to x1 = 1 (party 2 at 0): J1 changes by {-gain:+.3f} (negative = it gains): the rest point is not a best response")
chk('concave own cost: rest point not Nash', J1(1.0, 0.0) < J1(0.0, 0.0))
nst = 0; nr = 20000
for t in range(nr):
    a_, b_ = rng.uniform(0.05, 5, 2); c1, c2 = rng.uniform(-5, 5, 2); stab_by_eps = []
    for e_ in (0.01, 0.3, 1.0, 20.0):
        Jm = np.array([[-e_ * a_, -e_ * c1], [-c2, -b_]]); stab_by_eps.append(bool(np.all(np.linalg.eigvals(Jm).real < 0)))
    nst += len(set(stab_by_eps)) > 1 or (stab_by_eps[0] != (a_ * b_ > c1 * c2))
print(f"  {nr} random two-party games with CONVEX own costs (a, b > 0): stability depended on the speed ratio in {nst} of them; it holds iff a*b > c1*c2 (trace -eps*a - b < 0 always)")
chk('convex own costs: speed ratio never changes stability', nst == 0)

print("\nRESULT:", "PASS" if not bad else "FAIL " + str(bad))
sys.exit(0 if not bad else 1)
