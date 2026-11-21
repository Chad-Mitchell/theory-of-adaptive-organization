#!/usr/bin/env python3
"""Checks for theory/FREEZE_PROCESS_2026-11-21.md.

Is freezing a continuous limit of holding under the cost equation?
Sections (numbers match the note):
  S1  static freeze edge (Theorem 8 / CT11): continuity, C1 kink, second-derivative jump
  S2  fixed machinery cost h_m: first-order switch, jump size sqrt(h_m/(cH))
  S3  ruin cap: frozen design infeasible above q_r = Q_eps/H; forced, discontinuous melt
  S4  G2/G3 small-drift limit (OU, quadratic loss): effort -> 0 as sqrt(lambda)
  S5  cooling world q(t)=q0 exp(-t/tau_c): exact optimal read schedule (DP), freeze-out
  S6  design freeze-out (lagged adaptation): finite relic iff integral dt/tau_a < inf;
      relic scaling; rate-dependent hysteresis loop
  S7  switching-cost hysteresis (Dixit-type band)
  S8  Arrhenius store decay: freezing temperature, price enters only in a log
Run: nice -n 19 python3 freeze_process.py > freeze_process.out
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import solve_ivp, quad

np.set_printoptions(precision=6, suppress=False)
ok_all = True
def check(name, cond):
    global ok_all
    ok_all &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

# ---------------------------------------------------------------- S1
print("S1  static freeze edge, Theorem 8 setting (quadratic loss, alpha=2)")
c, W, H = 1.0, 2.0, 10.0
qf = 2*c/(W*H**2)
def Topt(q): return np.minimum(np.sqrt(2*c/(W*q)), H)
def Jhold(q): T = Topt(q); return c/T + W*q*T/2
qs = np.geomspace(qf/50, qf*50, 200001)
J = Jhold(qs); f = 1/Topt(qs)
i = np.searchsorted(qs, qf)
print(f"  q_f = {qf:.6g}")
jumpJ = abs(J[i]-J[i-1]); jumpf = abs(f[i]-f[i-1])
check(f"J continuous at q_f (adjacent-grid jump {jumpJ:.2e})", jumpJ < 1e-4)
check(f"effort continuous at q_f (adjacent-grid jump {jumpf:.2e})", jumpf < 1e-4)
dJ = np.gradient(J, qs)
left, right = dJ[i-50], dJ[i+50]
print(f"  dJ/dq just below / above q_f: {left:.6f} / {right:.6f}  (both -> W H/2 = {W*H/2})")
check("J is C1 at q_f (slopes agree to 1e-3)", abs(left-right)/(W*H/2) < 1e-3)
d2_above = -np.sqrt(2*c*W)/4*qf**-1.5
print(f"  d2J/dq2: 0 below, {d2_above:.4g} above  -> second-derivative jump (Ehrenfest 'second order')")
# order parameter: excess refresh rate above the imprint 1/H
qq = qf*(1+np.array([1e-3, 1e-2, 1e-1]))
exc = 1/Topt(qq) - 1/H
pred = (1/H)*(qq-qf)/(2*qf)
print(f"  excess effort f-1/H at q=q_f(1+d): {exc}  linear pred {pred}")
check("excess effort vanishes linearly in (q-q_f)", np.allclose(exc[:2], pred[:2], rtol=1e-2))
# contrast: lookup edge is a cliff (Theorem 8 item 5), reproduce quickly
mu, u, h = 3.0, 1.0, 0.5
qc = (mu*u-h)**2/(2*c*W)
eff_below = 1/np.sqrt(2*c/(W*qc*(1-1e-9)))
print(f"  contrast, lookup edge q_c={qc:.4g}: effort {eff_below:.4f} just below -> 0 above (cliff; pred (mu u-h)/2c={(mu*u-h)/(2*c):.4f})")
check("lookup-edge cliff reproduced", abs(eff_below-(mu*u-h)/(2*c)) < 1e-6)

# ---------------------------------------------------------------- S2
print("\nS2  fixed machinery cost h_m (paid only while able to refresh)")
for hm in [0.0, 1e-4, 1e-3, 1e-2, 1e-1]:
    JF = lambda q: c/H + W*q*H/2
    JH = lambda q: np.sqrt(2*c*W*q) + hm          # interior hold (T<H)
    qstar_pred = 2*(np.sqrt(c/H)+np.sqrt(hm))**2/(W*H)
    if hm == 0:
        qstar = qf
    else:
        qstar = brentq(lambda q: JH(q)-JF(q), qf*(1+1e-12), 1e3*qf)
    T_at = np.sqrt(2*c/(W*qstar))
    jump = 1/T_at - 1/H
    jump_pred = np.sqrt(hm/(c*H))
    slopeH, slopeF = W*T_at/2, W*H/2
    print(f"  h_m={hm:<7g} q*={qstar:.6g} (pred {qstar_pred:.6g})  effort jump {jump:.5f} (pred sqrt(h_m/cH)={jump_pred:.5f})  upkeep jump {hm}  dJ/dq {slopeH:.3f}|{slopeF:.3f}")
    check(f"h_m={hm}: switch point and jump match closed form", abs(qstar-qstar_pred)/qstar_pred < 1e-8 and abs(jump-jump_pred) < 1e-8)

# ---------------------------------------------------------------- S3
print("\nS3  ruin cap per window: q*T <= Q_eps (Brownian error, z fixed)")
Qeps = 0.5*qf*H   # chosen so q_r = Q/H = qf/2 < q*: cap binds first
qr = Qeps/H
hm = 1e-2
qstar = 2*(np.sqrt(c/H)+np.sqrt(hm))**2/(W*H)
def best(q):
    # frozen: one window of length H, feasible iff q*H <= Q
    JF = c/H + W*q*H/2 if q*H <= Qeps else np.inf
    T = min(np.sqrt(2*c/(W*q)), Qeps/q, H)
    JH = c/T + W*q*T/2 + hm
    return (JF, JH)
print(f"  q_r = Q/H = {qr:.4g}, q* (no cap) = {qstar:.4g}")
for q in [qr*0.999, qr*1.001]:
    JF, JH = best(q)
    print(f"  q={q:.6g}: J_frozen={JF:.6f} J_hold={JH:.6f} -> {'frozen' if JF<JH else 'hold'}")
a, b = best(qr*0.999999), best(qr*1.000001)
jumpJ = min(b) - min(a)
check(f"with the cap binding, melting is forced at q_r and J* jumps by {jumpJ:.4f} (>0)", jumpJ > 1e-3)
# without machinery cost the cap keeps T* continuous
Tc = lambda q: min(np.sqrt(2*c/(W*q)), Qeps/q, H)
gaps = max(abs(1/Tc(q*(1+1e-7))-1/Tc(q)) for q in np.geomspace(qf/100, qf*100, 2000))
check(f"with h_m=0 the capped effort stays continuous (max local gap {gaps:.2e})", gaps < 1e-5)

# ---------------------------------------------------------------- S4
print("\nS4  G2/G3 small-drift limit: OU world, quadratic loss, r(u)=1-exp(-2u), r'(0)=2")
cc = 1.0
A = lambda s: 1 - (1-np.exp(-2*s))/(2*s)
rows = []
for lam in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
    res = minimize_scalar(lambda ls: lam*cc/np.exp(ls) + A(np.exp(ls)), bounds=(-12, 8), method='bounded', options={'xatol':1e-12})
    s = np.exp(res.x); fstar = lam/s
    rows.append((lam, fstar, fstar/np.sqrt(lam)))
    print(f"  lambda={lam:.0e}  f*={fstar:.6g}  f*/sqrt(lambda)={fstar/np.sqrt(lam):.5f} (limit sqrt(r'(0)/2c)={np.sqrt(2/(2*cc)):.5f})")
check("effort -> 0 continuously as sqrt(lambda)", abs(rows[-1][2]-1.0) < 2e-3)
print(f"  (G2's threshold lambda_c = Phi/c = {0.25/cc*2:.3g}... is the HIGH-drift fade edge; nothing jumps as lambda -> 0)")

# ---------------------------------------------------------------- S5
print("\nS5  cooling world q(t)=q0 exp(-t/tau_c): exact optimal read times by DP (horizon Hor)")
def dp_schedule(tau, cr, Hor, Wt=1.0, q0=1.0, k=25):
    # nonuniform grid: ~k points per local optimal interval or per tau/k
    tt = [0.0]
    while tt[-1] < Hor:
        q = q0*np.exp(-tt[-1]/tau)
        dt = min(np.sqrt(2*cr/(Wt*q)), tau)/k
        tt.append(tt[-1]+dt)
    t = np.array(tt); t[-1] = Hor
    uu = q0*tau*(1-np.exp(-t/tau))
    UU = q0*tau*(t - tau*(1-np.exp(-t/tau)))
    n = len(t); bestc = np.full(n, np.inf); prev = np.full(n, -1)
    bestc[0] = cr
    for j in range(1, n):
        seg = Wt*((UU[j]-UU[:j]) - uu[:j]*(t[j]-t[:j]))
        tot = bestc[:j] + seg + cr
        m = np.argmin(tot); bestc[j] = tot[m]; prev[j] = m
    seg_end = Wt*((UU[-1]-UU) - uu*(Hor-t))
    tot = bestc + seg_end
    last = int(np.argmin(tot))
    reads = []; j = last
    while j >= 0:
        reads.append(t[j]); j = prev[j]
    return np.array(reads[::-1]), n
summary = []
el_errs = []
for tau, cr, Hor in [(10, 5e-3, 300), (20, 5e-3, 600), (40, 5e-3, 1200), (20, 2e-2, 600), (20, 5e-3, 1500), (20, 5e-3, 5000)]:
    r, n = dp_schedule(tau, cr, Hor)
    gaps = np.diff(r)
    mid = r[:-1] + gaps/2
    q_mid = np.exp(-mid/tau)
    adia = np.sqrt(2*cr/q_mid)
    early = mid < 0.3*tau*np.log(tau**2/(2*cr))
    rel = np.median(np.abs(gaps[early]/adia[early]-1)) if early.any() else np.nan
    q_fo = 2*cr/tau**2
    k_fo = np.argmax(gaps > tau) if (gaps > tau).any() else None
    q_at = np.exp(-r[k_fo]/tau) if k_fo is not None else np.nan
    after = len(r) - 1 - k_fo if k_fo is not None else 0
    q_last = np.exp(-r[-1]/tau)
    q_prev = np.exp(-r[-2]/tau)
    u_r = tau*(1 - np.exp(-r/tau))
    el_lhs = u_r[-1] - u_r[-2]
    el_rhs = q_last*(Hor - r[-1])
    el_errs.append(abs(el_lhs/el_rhs - 1))
    q_tail_pred = tau*q_prev/(Hor - r[-1])
    summary.append((tau, cr, Hor, q_at/q_fo, q_last, r[-1], after, len(r)))
    print(f"  tau_c={tau:<3} c={cr:<6g} Hor={Hor:<5}: grid {n}, reads {len(r)}; early gaps vs sqrt(2c/Wq(t)): median rel dev {rel:.3f}")
    print(f"     first gap > tau_c starts at q={q_at:.3g}; q_fo=2c/(W tau_c^2)={q_fo:.3g}; ratio {q_at/q_fo:.2f}; reads after that: {after}; last read at t={r[-1]:.1f}, q={q_last:.3g} (EL tail pred {q_tail_pred:.3g}, EL ratio {el_lhs/el_rhs:.4f})")
ratios = [s[3] for s in summary]
check(f"freeze-out onset tracks q_fo=2c/(W tau_c^2) within a factor 3 across runs (ratios {np.round(ratios,2)})", all(1/3 < x < 3 for x in ratios))
check("reads stop well before the horizon (frozen afterwards) in every run", all(s_[5] < 0.8*s_[2] for s_ in summary))
check("after the first gap > tau_c the schedule makes only O(1) further reads (<=3)", all(s_[6] <= 3 for s_ in summary))
check(f"Euler-Lagrange last-read condition u_N-u_{{N-1}}=q_N(Hor-t_N) holds (max rel err {max(el_errs):.3f})", max(el_errs) < 0.05)
check("read count saturates between Hor=1500 and Hor=5000 (both N=403)", summary[-2][7] == summary[-1][7])

# ---------------------------------------------------------------- S6
print("\nS6  design freeze-out: d x/dt = -(x - x*(t))/tau_a(q), x = ln f, x* = (1/alpha) ln q (alpha=2)")
alpha = 2.0
def relic_exp(tau_c, zeta, tau1=1.0, Tend_mult=80):
    rhs = lambda t, x: [-(x[0] - np.log(np.exp(-t/tau_c))/alpha)/(tau1*np.exp(zeta*t/tau_c))]
    Tend = Tend_mult*tau_c/zeta
    sol = solve_ivp(rhs, [0, Tend], [0.0], t_eval=[Tend/2, Tend], rtol=1e-10, atol=1e-12, method='LSODA')
    return sol.y[0, -1], sol.y[0, 0]
for zeta in [0.5, 1.0, 2.0]:
    taus = np.array([10., 30., 100., 300., 1000.])
    xr = np.array([relic_exp(tc, zeta)[0] for tc in taus])
    slope = np.polyfit(np.log(taus), xr, 1)[0]
    print(f"  zeta={zeta}: relic ln f_inf at tau_c={taus.astype(int)}: {np.round(xr,4)}; slope d ln f_inf / d ln tau_c = {slope:.4f} (pred -1/(alpha zeta) = {-1/(alpha*zeta):.4f})")
    check(f"zeta={zeta}: relic exponent matches -1/(alpha zeta) within 0.02", abs(slope + 1/(alpha*zeta)) < 0.02)
x1, xm = relic_exp(100., 1.0)
check(f"exponential cooling: x converges (finite relic; |x(80 tau_c)-x(40 tau_c)|={abs(x1-xm):.2e})", abs(x1-xm) < 1e-6)
gamma_E = 0.5772156649015329
for zeta in [0.5, 1.0, 2.0]:
    x_num, _ = relic_exp(1000., zeta)
    x_asymp = -(np.log(1000./zeta) + gamma_E)/(alpha*zeta)
    check(f"zeta={zeta}: exact Euler-Mascheroni relic formula matches tau_c=1000 ({x_num:.6f} vs {x_asymp:.6f})", abs(x_num - x_asymp) < 1e-8)
print("  power-law cooling q=(1+t)^-p, tau_a = q^-zeta: lag y = x - x* at late times")
for p, zeta in [(1.0, 0.5), (1.0, 1.0), (1.0, 2.0)]:
    rhs = lambda t, x: [-(x[0] + p*np.log1p(t)/alpha)/((1+t)**(p*zeta))]
    ts = [1e2, 1e3, 1e4, 1e5]
    sol = solve_ivp(rhs, [0, ts[-1]], [0.0], t_eval=ts, rtol=1e-10, atol=1e-12, method='LSODA')
    lag = sol.y[0] + p*np.log1p(np.array(ts))/alpha
    print(f"    p*zeta={p*zeta}: lag at t={ts}: {np.round(lag,4)}   x(t)={np.round(sol.y[0],4)}")
    if p*zeta < 1:
        check("p*zeta<1: lag stays bounded and shrinks (keeps tracking, no freeze)", lag[-1] < lag[0] and lag[-1] < 0.1)
    elif p*zeta == 1:
        check("p*zeta=1: critical boundary converges to constant nonzero lag p/alpha", abs(lag[-1] - p/alpha) < 1e-4)
    else:
        check("p*zeta>1: x converges while x* -> -inf (frozen relic)", abs(sol.y[0][-1]-sol.y[0][-2]) < 1e-3 and lag[-1] > lag[0])
print("  cooling-then-reheating loop: q from 1 down to 1e-3 and back, at rate 1/tau_c, zeta=1")
areas = []
for tc in [0.3, 3., 10., 30., 100., 300., 1e3, 1e4]:
    Tdown = tc*np.log(1e3)
    lnq = lambda t: -t/tc if t < Tdown else -Tdown/tc + (t-Tdown)/tc
    rhs = lambda t, x: [-(x[0] - lnq(t)/alpha)/(np.exp(-lnq(t)))]
    te = np.linspace(0, 2*Tdown, 4001)
    sol = solve_ivp(rhs, [0, 2*Tdown], [0.0], t_eval=te, rtol=1e-9, atol=1e-12, method='LSODA', max_step=Tdown/400)
    L = np.array([lnq(t) for t in te]); X = sol.y[0]
    area = abs(np.trapezoid(X, L))
    areas.append(area)
    print(f"    tau_c={tc:<5}: loop area in (ln q, ln f) = {area:.4f}")
# First-run prediction 'area shrinks monotonically as cooling slows' FAILED (recorded in the note, sec. 6.4):
# the area is non-monotone: tiny when cooling is far faster than adaptation (design never moves),
# largest at intermediate rates, and -> 0 only in the quasi-static limit.
print(f"    monotone shrink over all rates: {'yes' if all(np.diff(areas) < 0) else 'NO (first-run prediction failed; recorded)'}")
check("loop area peaks at an intermediate rate (non-monotone)", np.argmax(areas) not in (0, len(areas)-1))
check("loop area -> small in the quasi-static limit (tau_c=1e4 area < 10% of peak)", areas[-1] < 0.1*max(areas))

# ---------------------------------------------------------------- S7
print("\nS7  switching costs: build C_b, dismantle C_d, discount rho (static q after the shift)")
hm, rho = 1e-2, 0.05
JF = lambda q: c/H + W*q*H/2
JH = lambda q: np.sqrt(2*c*W*q) + hm if q > qf else c/H + W*q*H/2 + hm
qstar = 2*(np.sqrt(c/H)+np.sqrt(hm))**2/(W*H)
for Cb, Cd in [(0, 0), (0.1, 0.0), (0.1, 0.1), (0.5, 0.1)]:
    q_down = brentq(lambda q: (JH(q)-JF(q)) - rho*Cd, qf*1e-3, qstar) if Cd > 0 else qstar
    q_up = brentq(lambda q: (JF(q)-JH(q)) - rho*Cb, qstar, qstar*1e4) if Cb > 0 else qstar
    print(f"  C_b={Cb}, C_d={Cd}: freeze below q={q_down:.5g}, re-melt above q={q_up:.5g}, q*={qstar:.5g}, band ratio {q_up/q_down:.3f}")
    if Cb == 0 and Cd == 0: band0 = q_up/q_down
check("zero switching cost: no hysteresis (re-melts at the same q*)", abs(band0-1) < 1e-12)

# ---------------------------------------------------------------- S8
print("\nS8  Arrhenius store decay q_s = nu0 exp(-Ea/kT): freeze iff q_s <= q_f = 2c/(W H^2)")
nu0, Ea = 1e13, 1.0     # 1/s, eV
kB = 8.617333e-5
for (cW, Hs) in [(1.0, 3.15e7), (1e-3, 3.15e7), (1.0, 3.15e16)]:
    Tf = Ea/(kB*np.log(nu0*Hs**2/(2*cW)))
    Tf_num = brentq(lambda T: nu0*np.exp(-Ea/(kB*T)) - 2*cW/Hs**2, 1, 5000)
    el = 1/np.log(nu0*Hs**2/(2*cW))
    print(f"  c/W={cW:g}, H={Hs:.3g} s: T_f={Tf:.3f} K (root {Tf_num:.3f} K); elasticity of T_f in c/W = {el:.4f}")
    check("closed form matches root", abs(Tf-Tf_num) < 1e-6*Tf)
print("  1000x change in the price ratio c/W moves T_f by about", f"{(Ea/(kB*np.log(nu0*3.15e7**2/2e-3)))/(Ea/(kB*np.log(nu0*3.15e7**2/2)))-1:+.3%}")

print("\nALL CHECKS PASS" if ok_all else "\nSOME CHECKS FAILED")
