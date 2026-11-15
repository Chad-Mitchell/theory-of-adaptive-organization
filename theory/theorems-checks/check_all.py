"""Algebra and numeric checks for THEOREMS.md. Run: python check_all.py > check_all.out"""
import numpy as np, sympy as sp
from scipy.linalg import solve_discrete_are
from scipy.optimize import minimize_scalar, brentq
from scipy.signal import lfilter
rng = np.random.default_rng(0)
def H(s): print('\n== ' + s + ' ==')

# ---------------- T1 ----------------
H('T1a EOQ check interval: cost rate c/T + w*sig^2*T/2')
c, w, s, T, h = sp.symbols('c w sigma T h', positive=True)
J = c / T + w * s**2 * T / 2
Ts = sp.solve(sp.diff(J, T), T)[0]; print('T* =', sp.simplify(Ts), '| J* =', sp.simplify(J.subs(T, Ts)))
x = sp.symbols('x', positive=True)
pen = sp.simplify(J.subs(T, x * Ts) / J.subs(T, Ts)); print('J(x T*)/J* =', pen, '  (= cosh(ln x))')
print('penalty at x=2:', float(pen.subs(x, 2)), ' x=sqrt2:', float(pen.subs(x, sp.sqrt(2))), ' x=10:', float(pen.subs(x, 10)))
H('T1b Monte Carlo: random walk, perfect periodic checks')
for sig in [0.5, 1, 2]:
    cc, ww, dt = 1.0, 1.0, 0.01; Tst = np.sqrt(2 * cc / (ww * sig**2)); n = int(Tst / dt)
    paths = np.cumsum(rng.normal(0, sig * np.sqrt(dt), (4000, n)), 1)
    loss = ww * (paths**2).mean(0).sum() * dt
    print(f'sigma={sig}: MC cost {(cc + loss) / (n*dt):.3f} vs sigma*sqrt(2cw) {sig*np.sqrt(2):.3f}')
H('T1c Kalman steady-state gain for random walk + noise: K^2/(1-K) = q/r')
K, z = sp.symbols('K z', positive=True)   # z = q/r
Ksol = [k for k in sp.solve(sp.Eq(K**2, z * (1 - K)), K) if k.subs(z, 1) > 0][0]
print('K(z) =', sp.simplify(Ksol), '| series:', sp.series(Ksol, z, 0, 2).removeO())
H('T1d misspecified gain penalty, EWMA MSE(a) = [(1-a)^2 q + a^2 r]/[a(2-a)]')
def mse(a, q, r): return ((1 - a)**2 * q + a**2 * r) / (a * (2 - a))
q, r = 1e-4, 1.0
ast = minimize_scalar(lambda a: mse(a, q, r), bounds=(1e-6, .999), method='bounded').x
for m in [2, 10, 0.1]:
    a = ast * np.sqrt(m)
    print(f'rate misjudged x{m}: exact MSE ratio {mse(a, q, r) / mse(ast, q, r):.4f}; small-gain formula (m^-1/2+m^1/2)/2 = {(m**-.5 + m**.5) / 2:.4f}')

# ---------------- T2 ----------------
H('T2 watcher condition (EOQ algebra) and the escalation refinement')
cm, cw, hw, eps = sp.symbols('c_main c_w h_w epsilon', positive=True)
Jm = s * sp.sqrt(2 * w * cm); Jw = s * sp.sqrt(2 * w * (cw)) + hw
print('main-only cost:', Jm, '| watcher cost:', Jw)
print('watcher pays iff  ', sp.simplify(Jm - Jw), '> 0  i.e. sqrt(2w)*sigma*(sqrt(c_main)-sqrt(c_w)) > h_w  [verified symbolic]')
Jwe = s * sp.sqrt(2 * w * (cw + eps * cm)) + hw
print('with escalation fraction eps (each escalated check also wakes main):  pays iff', sp.simplify(Jm - Jwe), '> 0')
print('  necessary: eps < 1 - c_w/c_main')
# MC: periodic checks with random escalations, expected cost per unit time
for e in [0.0, 0.2, 0.5]:
    cmn, cwt, ww, sg = 1.0, 0.1, 1.0, 1.0; ce = cwt + e * cmn
    Tst = np.sqrt(2 * ce / (ww * sg**2)); costs = []
    nchk = 200000; esc = rng.random(nchk) < e
    cost = (nchk * cwt + esc.sum() * cmn) / (nchk * Tst) + ww * sg**2 * Tst / 2
    print(f'eps={e}: simulated cost {cost:.4f} vs formula sigma*sqrt(2w(c_w+eps c_main)) {sg*np.sqrt(2*ww*ce):.4f}; main-only {sg*np.sqrt(2*ww*cmn):.4f}')

# ---------------- T3 ----------------
H('T3a compression threshold: N facts share a driver (rate q_g) plus own residual (q_u)')
N, qg, qu, cg, rho = sp.symbols('N q_g q_u c_g rho', positive=True)
flat = N * sp.sqrt(2 * c * w * (qg + qu))
nested = sp.sqrt(2 * cg * w * N * qg) + N * sp.sqrt(2 * c * w * qu) + h
print('flat cost:', flat); print('nested cost (upper bound):', nested)
gain = sp.simplify((flat - nested).subs({cg: c, h: 0}).subs(qg, rho * qu))
Nst = sp.solve(sp.Eq(gain, 0), N); print('N* (c_g=c, h=0):', [sp.simplify(n_) for n_ in Nst])
alt = (sp.sqrt(1 + rho) + 1)**2 / rho
print('equals (sqrt(1+rho)+1)^2/rho ?', [sp.simplify(n_ - alt) == 0 for n_ in Nst])
for rv in [0.1, 0.5, 1, 4, 10]: print(f'  rho={rv}: N* = {float(alt.subs(rho, rv)):.2f}   (small-rho approx 4/rho = {4/rv:.1f})')
H('T3b flat single clock vs per-level clocks (Cauchy-Schwarz identity); two levels with separation ratio R = sqrt(q_fast/q_slow)')
Rr = sp.symbols('R', positive=True)
sav = 1 - (1 + 1 / Rr) / sp.sqrt(2 * (1 + 1 / Rr**2))
for Rv in [1, 2, 4, 10, 100]: print(f'  R={Rv}: fraction saved by per-level clocks = {float(sav.subs(Rr, Rv)):.4f}')
print('  limit R->oo:', sp.limit(sav, Rr, sp.oo), '=', float(sp.limit(sav, Rr, sp.oo)))
H('T3c timescale separation: x = s + f, s random walk (q_s), f AR(1) (time constant tau, variance v), obs noise r')
def steady_kf_mse(A, Q, Hm, R):
    P = solve_discrete_are(A.T, Hm.T, Q, R)   # prior covariance
    S = Hm @ P @ Hm.T + R; Kk = P @ Hm.T @ np.linalg.inv(S); Pp = P - Kk @ Hm @ P
    return float((Hm @ Pp @ Hm.T)[0, 0])
def sim_filters(tau, q_s=1e-4, v=0.04, r=0.04, n=200000):
    ph = np.exp(-1 / tau); qf = v * (1 - ph**2)
    s_ = np.cumsum(rng.normal(0, np.sqrt(q_s), n)); f_ = np.zeros(n); e = rng.normal(0, np.sqrt(qf), n)
    f_ = lfilter([1.0], [1.0, -ph], e)
    x_ = s_ + f_; y = x_ + rng.normal(0, np.sqrt(r), n)
    A = np.array([[1, 0], [0, ph]]); Q = np.diag([q_s, qf]); Hm = np.array([[1., 1.]])
    opt = steady_kf_mse(A, Q, Hm, np.array([[r]]))
    def ewma(a):
        return lfilter([a], [1.0, -(1 - a)], y)
    # flat: best single EWMA (grid search on gain)
    best = min(((np.mean((ewma(a)[1000:] - x_[1000:])**2), a) for a in np.geomspace(1e-3, 1, 25)))
    # nested-decoupled: slow level treats f + noise as white (var v + r); fast level is the AR(1) Kalman on the residual
    a_s = float(np.real(sp.N([k for k in sp.solve(sp.Eq(K**2, (q_s / (v + r)) * (1 - K)), K) if k > 0][0])))
    sh = ewma(a_s); res = y - sh
    Pf = solve_discrete_are(np.array([[ph]]), np.array([[1.]]), np.array([[qf]]), np.array([[r]]))[0, 0]
    kf = Pf / (Pf + r); fh = np.zeros(n)
    fh = lfilter([kf], [1.0, -ph * (1 - kf)], res)
    nest = np.mean((sh[1000:] + fh[1000:] - x_[1000:])**2)
    return opt, best[0], nest
for tau in [2, 10, 50, 250, 1000]:
    o, fl, ne = sim_filters(tau)
    print(f'  tau={tau:5}: optimal joint KF {o:.5f} | best single-timescale EWMA {fl:.5f} ({fl/o:.2f}x) | nested decoupled {ne:.5f} ({ne/o:.2f}x)')

# ---------------- T4 ----------------
H('T4 shared trace with N independent depositors: K^2/(1-K) = N q / r')
for qr in [1e-3]:
    for Nn in [1, 4, 16, 64, 256, 1024]:
        zz = Nn * qr; Kv = (-zz + np.sqrt(zz**2 + 4 * zz)) / 2
        print(f'  N={Nn:5}: gain {Kv:.4f}  sqrt(Nq/r)={np.sqrt(zz):.4f}')
Ns = np.array([1, 4, 16, 64, 256, 1024]); zz = Ns * 1e-3; Kv = (-zz + np.sqrt(zz**2 + 4 * zz)) / 2
print('  local exponents dlnK/dlnN:', np.round(np.diff(np.log(Kv)) / np.diff(np.log(Ns)), 3))
# Monte Carlo: best EWMA gain for shared trace from simulation
def best_gain_sim(Nn, q=1e-3, r=1.0, n=60000):
    xx = np.cumsum(rng.normal(0, np.sqrt(q), n)); y = xx + rng.normal(0, np.sqrt(r / Nn), n)
    def m_(a):
        out = lfilter([a], [1.0, -(1 - a)], y)
        return np.mean((out[2000:] - xx[2000:])**2)
    gs = np.geomspace(0.005, 0.8, 30); vals = [m_(a) for a in gs]; return gs[int(np.argmin(vals))]
print('  MC best gain N=1,4,16:', [round(best_gain_sim(Nn), 4) for Nn in [1, 4, 16]], ' theory', [round(float(np.sqrt(Nn * 1e-3)), 4) for Nn in [1, 4, 16]])

# ---------------- T5 ----------------
H('T5 rise-then-fall: bounded staleness loss (Cho & Garcia-Molina form)')
f, lam, mu, W = sp.symbols('f lambda mu W', positive=True)
F = (f / lam) * (1 - sp.exp(-lam / f))
print('marginal freshness at f->0+:', sp.limit(sp.diff(F, f), f, 0, '+'), ' => refreshing pays iff mu*W/lambda > c, i.e. lambda < mu W / c')
d2 = sp.diff(F, f, 2); print('F concave in f? d2F/df2 =', sp.simplify(d2))
grid_ok = all(float(d2.subs({f: fv, lam: 1})) < 0 for fv in np.geomspace(1e-2, 1e2, 200)); print('  d2F/df2 < 0 on grid f in [0.01,100] (lambda=1):', grid_ok, ' (F depends on f/lambda only, so this covers all lambda)')
def fstar(l, muv=1, Wv=10, cv=1):
    if l <= 0: return 0.0
    g = lambda fv: cv * fv + muv * Wv * (1 - (fv / l) * (1 - np.exp(-l / fv)))
    res = minimize_scalar(g, bounds=(1e-9, 100), method='bounded'); return res.x if g(res.x) < g(1e-9) else 0.0
ls = [0.001, 0.1, 1, 3, 5, 7, 9, 9.9, 10.1, 20]
print('  f*(lambda), mu=1 W=10 c=1:', [(l, round(fstar(l), 3)) for l in ls])
H('T5b quadratic loss with a bounded read-at-use fallback (cost u per use, use rate mu): cliff')
for sg in [0.5, 1, 1.4, 1.42, 2, 4]:
    hold = sg * np.sqrt(2 * 1 * 1); live = 2.0 * 1
    print(f'  sigma={sg}: hold {hold:.3f} vs fallback {live:.3f} ->', 'hold, f*=%.3f' % (sg * np.sqrt(1 / 2)) if hold < live else 'fallback, f*=0')

# ---------------- T6 ----------------
H('T6 Still et al. 2012: per-step beta<W_diss> = I_mem - I_pred, exact enumeration on a 2-state toy')
def H_(p): p = np.asarray(p, float); p = p[p > 0]; return -np.sum(p * np.log(p))
def MI(J): return H_(J.sum(1)) + H_(J.sum(0)) - H_(J.ravel())
beta = 1.0; eps_ = 1.5; pflip = 0.1; kappa = 0.4
E = lambda s_, x_: -eps_ * (s_ == x_)
Px = np.array([[1 - pflip, pflip], [pflip, 1 - pflip]])           # protocol Markov chain
peq = lambda x_: np.array([np.exp(-beta * E(s_, x_)) for s_ in (0, 1)]) / sum(np.exp(-beta * E(s_, x_)) for s_ in (0, 1))
# relaxation kernel at fixed x: s' ~ (1-kappa) delta_s + kappa peq(.|x)  (satisfies detailed balance w.r.t. peq)
def relax(ps_x, x_): return (1 - kappa) * ps_x + kappa * peq(x_)
# joint p(s_t, x_t) at stationarity by iteration; start equilibrium
px = np.array([.5, .5]); joint = np.array([peq(x_) * px[x_] for x_ in (0, 1)]).T  # joint[s,x]
tot_diss = 0; tot_nost = 0; relax_term = 0
def Fneq_avg(J):  # beta <F_neq[p(s|x)]>_x = beta<E> - H(S|X)
    return beta * sum(J[s_, x_] * E(s_, x_) for s_ in (0, 1) for x_ in (0, 1)) - (H_(J.ravel()) - H_(J.sum(0)))
for t in range(40):
    # three-way joint p(s_t, x_t, x_{t+1})
    J3 = np.einsum('sx,xy->sxy', joint, Px)
    Imem = MI(J3.sum(2)); Ipred = MI(J3.sum(1))
    Wavg = beta * sum(J3[s_, x_, y_] * (E(s_, y_) - E(s_, x_)) for s_ in (0, 1) for x_ in (0, 1) for y_ in (0, 1))
    dF = Fneq_avg(J3.sum(1)) - Fneq_avg(J3.sum(2))
    diss = Wavg - dF
    if t in (0, 1, 5, 39): print(f'  step {t}: beta<W_diss> = {diss:.6f}   I_mem - I_pred = {Imem - Ipred:.6f}')
    after_work = J3.sum(1)  # p(s_t, x_{t+1})
    new = np.zeros((2, 2))
    for y_ in (0, 1):
        col = after_work[:, y_]; py = col.sum(); new[:, y_] = relax(col / py, y_) * py
    relax_term += Fneq_avg(new) - Fneq_avg(after_work)
    tot_diss += diss; tot_nost += Imem - Ipred; joint = new
print(f'  summed: nostalgia {tot_nost:.5f}; relaxation free-energy change {relax_term:.5f} (<= 0): total beta<W_diss> = nostalgia - relax = {tot_nost - relax_term:.5f} >= nostalgia')

# ---------------- T7 ----------------
H('T7a scale-free banding: mean penalty for log-uniform items in a band of log-width D (geometric band, centered)')
D, u = sp.symbols('D u', positive=True)
avgpen = sp.simplify(sp.integrate(sp.cosh(u) - 1, (u, -D / 2, D / 2)) / D)
print('mean penalty =', avgpen)
val = sp.simplify(avgpen.subs(D, sp.log(2)) + 1); print('at D=ln2: 1 + penalty =', val, '=', float(val), ' (Roundy 1985 power-of-two bound 1/(sqrt2 ln2) = %.4f)' % (1 / (np.sqrt(2) * np.log(2))))
print('worst-case at band edge D=ln2:', float(sp.cosh(sp.log(2) / 2) - 1), ' (Roundy fixed-base bound ~6%)')
H('T7b optimal number of levels K for a log-span L of natural intervals, base cost C, per-level upkeep h')
Kk, L, C = sp.symbols('K L C', positive=True)
tot = C * (L / Kk)**2 / 24 + Kk * h
Kst = sp.solve(sp.diff(tot, Kk), Kk)[0]; print('small-band approx: K* =', sp.simplify(Kst))
for Lv, Cv, hv in [(np.log(1000), 100, 0.5), (np.log(1e5), 100, 0.5)]:
    exact = min(range(1, 60), key=lambda k: Cv * (2 * k / Lv * np.sinh(Lv / (2 * k)) - 1) + k * hv)
    print(f'  L=ln({np.exp(Lv):.0f}) C={Cv} h={hv}: K* exact {exact}, approx {float(Kst.subs({L: Lv, C: Cv, h: hv})):.2f}; level ratio e^(L/K*) = {np.exp(Lv/exact):.2f}')
H('T7c coarse-graining: unit of size n, check cost ~ n^gamma, stakes ~ n^delta, aggregate drift variance ~ n^(2H)')
n_, g_, d_, H_s, c0, w0, s0 = sp.symbols('n gamma delta H c0 w0 s0', positive=True)
Tn = sp.sqrt(2 * c0 * n_**g_ / (w0 * n_**d_ * s0**2 * n_**(2 * H_s)))
print('T*(n) =', sp.simplify(Tn), ' => log-log slope', sp.simplify(sp.diff(sp.log(Tn), n_) * n_))
# closure: sum of n independent random walks is a random walk with n times the variance rate (numeric)
paths = rng.normal(0, 1, (20000, 8, 50)).cumsum(2).sum(1); print('  var of sum of 8 RWs at t=50 / (8*50):', round(paths[:, -1].var() / 400, 3))

# ---------------- T8 ----------------
H('T8a Adler/Kuramoto two oscillators: dphi/dt = dw - K sin(phi); locked iff |dw| <= K')
for dw, Kc in [(0.5, 1.0), (0.99, 1.0), (1.01, 1.0), (1.5, 1.0)]:
    ph = 0.0; dt = 0.01
    for i in range(200000): ph += dt * (dw - Kc * np.sin(ph))
    drift = ph / (200000 * dt); th = np.sqrt(max(dw**2 - Kc**2, 0))
    print(f'  dw={dw} K={Kc}: mean slip rate {drift:.4f} (theory sqrt(dw^2-K^2) = {th:.4f}) -> {"locked" if th == 0 else "drifting (quasi-periodic on T^2)"}')
H('T8b Kuramoto N=2000, Lorentzian width g=0.5 -> K_c = 2g = 1; r_inf = sqrt(1 - K_c/K)')
Nn = 2000; gam = 0.5
om = gam * np.tan(np.pi * (np.arange(Nn) + 0.5) / Nn - np.pi / 2)  # deterministic Lorentzian quantiles
for Kc in [0.5, 0.9, 1.2, 1.6, 2.5]:
    th = rng.uniform(0, 2 * np.pi, Nn); dt = 0.02
    rs = []
    for i in range(6000):
        Z = np.exp(1j * th).mean(); th += dt * (om + Kc * np.abs(Z) * np.sin(np.angle(Z) - th))
        if i > 4000: rs.append(abs(Z))
    print(f'  K={Kc}: r = {np.mean(rs):.3f}  theory {np.sqrt(max(0, 1 - 1 / Kc)):.3f}')
H('T8c identical frequencies: Kuramoto is gradient descent of V = -(K/2N) sum cos(th_i - th_j) on the torus T^N')
th = rng.uniform(0, 2 * np.pi, 50); Kc = 1.0; dt = 0.01
V = lambda t_: -(Kc / (2 * 50)) * np.sum(np.cos(t_[:, None] - t_[None, :]))
vals = []
for i in range(3000):
    Z = np.exp(1j * th).mean(); th = th + dt * (Kc * np.abs(Z) * np.sin(np.angle(Z) - th)); vals.append(V(th))
print('  V monotone non-increasing:', bool(np.all(np.diff(vals) <= 1e-12)), '| V start', round(vals[0], 3), '-> end', round(vals[-1], 3), '(min = -K N/2 =', -Kc * 50 / 2, ': full sync, the torus flow collapses to a point/cycle)')

H('T7a-extra convexity of the band penalty phi(D) = (2/D) sinh(D/2) - 1 (needed for the Jensen step)')
Dv = sp.symbols('D', positive=True); phi = 2 / Dv * sp.sinh(Dv / 2) - 1
d2p = sp.diff(phi, Dv, 2); print('series of phi:', sp.series(phi, Dv, 0, 6))
print('phi\'\'(D) > 0 on grid D in [0.01, 30]:', all(float(d2p.subs(Dv, v)) > 0 for v in np.geomspace(0.01, 30, 300)))
print('(all Taylor coefficients of phi are positive: phi = sum_k D^{2k}/(4^k (2k+1)!), so phi is convex on D > 0)')
