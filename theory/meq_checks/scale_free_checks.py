"""Checks for THEORY v2.2 CT24 (cost shares = price elasticities; looking : being wrong = alpha-1; shadow-price reading;
kT floor with an inefficiency multiplier) and CT25 (the ruin constraint is the temperature z = B/(sigma sqrt(tau)) >= z_eps).
Origin: records/reviews/audit_2026-11-19/AUDIT.md sections 2 and 5. Run: nice -n 19 python3 scale_free_checks.py
(prints the numbers, then asserts; ends with RESULT: PASS)
All checks use the repo's CT12 single-tracker form J(T)=c/T + w*q*T^(alpha-1)/alpha unless stated."""
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.stats import norm
rng = np.random.default_rng(7)

def Jopt(c, w, q, al):
    f = lambda lt: c/np.exp(lt) + w*q*np.exp(lt)**(al-1)/al
    r = minimize_scalar(f, bounds=(-30, 30), method='bounded', options={'xatol': 1e-12})
    return np.exp(r.x), r.fun

print("== 1. Covariance: only dimensionless ratios matter (Buckingham pi / homogeneity, S1-S2)")
worst = 0
for al in (1.3, 1.6, 2.0, 2.5, 2.9):
    ref = None
    for _ in range(6):
        # random currency scale lam, units of x (A), units of time (s) -> c,w,q rescale
        lam, A, s = 10**rng.uniform(-6, 12), 10**rng.uniform(-3, 3), 10**rng.uniform(-3, 3)
        c, w, q = 3.0*lam, 0.7*lam/(A**2)*s*(1.0), 1.1*A**2/s**(al-1)   # q T^(al-1) must be x^2 ; w*x^2/time = cost/time
        T, J = Jopt(c, w, q, al)
        T0 = (c/(w*q))**(1/al); J1 = c**((al-1)/al)*(w*q)**(1/al)
        u, j = T/T0, J/J1
        if ref is None: ref = (u, j)
        worst = max(worst, abs(u/ref[0]-1), abs(j/ref[1]-1))
    ustar = (al/(al-1))**(1/al); jstar = (al/(al-1))**(1-1/al)
    worst = max(worst, abs(ref[0]/ustar-1), abs(ref[1]/jstar-1))
    print(f"alpha={al}: T*/T0={ref[0]:.6f} (closed form {ustar:.6f}), J*/J1={ref[1]:.6f} (closed form {jstar:.6f})")
print(f"max relative deviation over random currency/unit rescalings: {worst:.2e}  (spans 18 decades of currency)")

print("\n== 2. Cost shares = elasticities (envelope theorem) and sum to 1 (Euler, J homogeneous degree 1 in prices)")
for al in (1.5, 2.0, 2.5):
    c, w, q = 5.0, 0.3, 2.0
    T, J = Jopt(c, w, q, al)
    sc, sw = (c/T)/J, (w*q*T**(al-1)/al)/J
    h = 1e-5
    ec = (np.log(Jopt(c*(1+h), w, q, al)[1]) - np.log(Jopt(c*(1-h), w, q, al)[1]))/(np.log(1+h)-np.log(1-h))
    ew = (np.log(Jopt(c, w*(1+h), q, al)[1]) - np.log(Jopt(c, w*(1-h), q, al)[1]))/(np.log(1+h)-np.log(1-h))
    print(f"alpha={al}: sensing share={sc:.6f} elasticity d lnJ*/d ln c={ec:.6f} closed form (a-1)/a={(al-1)/al:.6f}; "
          f"error share={sw:.6f} elasticity={ew:.6f} 1/a={1/al:.6f}; sum={sc+sw:.6f}")
print("=> at the optimum, spend on looking : cost of being wrong = alpha-1, whatever the currency, units or scale (EOQ 'equal costs' at alpha=2).")

print("\n== 3. Shadow-price reading: w is the multiplier of the system's own read budget")
for al in (1.5, 2.0, 2.5):
    c, q, B = 5.0, 2.0, 0.8       # read-cost-rate budget B: c/T <= B  -> T = c/B
    e = lambda B_: q*(c/B_)**(al-1)/al            # min mean error under budget B
    lam = -(e(B*(1+1e-6)) - e(B*(1-1e-6)))/(2e-6*B)  # shadow price: error saved per unit budget
    w_closed = al*B**al/((al-1)*q*c**(al-1))         # w that makes T*=c/B optimal in J
    T, _ = Jopt(c, w_closed, q, al)
    print(f"alpha={al}: budget T={c/B:.6f}, J-optimal T at w=1/lambda: {Jopt(c,1/lam,q,al)[0]:.6f}; lambda*w={lam*w_closed:.6f} (should be 1)")
# two trackers, one budget: marginal error saved per unit currency equalizes = one shadow price per system
al = 2.0; cs = np.array([2.0, 7.0]); qs = np.array([1.0, 4.0]); B = 3.0
from scipy.optimize import minimize
f = lambda x: sum(qs[i]*(cs[i]/x[i])**(al-1)/al for i in range(2))
cons = {'type': 'eq', 'fun': lambda x: x.sum()-B}
r = minimize(f, [1.0, 2.0], bounds=[(1e-3, B)]*2, constraints=cons, method='SLSQP', options={'ftol': 1e-14})
x = r.x
marg = [qs[i]*(al-1)/al*(al-1)*cs[i]**(al-1)*x[i]**(-al) for i in range(2)]   # |d e_i/d x_i|
print(f"two trackers, one budget: allocations {x.round(5)}; marginal value per currency unit {np.round(marg,6)} (equal => one shadow price)")

print("\n== 4. Landauer floor as a lower bound with an inefficiency multiplier beta = c/(kT per nat)")
import sympy as sp
D, s_, kT, w_, beta = sp.symbols('D sigma kT w beta', positive=True)
Jd = beta*kT*s_**2/(2*D) + w_*D
Dst = sp.solve(sp.diff(Jd, D), D)[0]
Jst = sp.simplify(Jd.subs(D, Dst))
print("CT7 with price beta*kT per nat: D* =", sp.simplify(Dst), "; J* =", Jst, "; ratio to floor =", sp.simplify(Jst/Jst.subs(beta, 1)))
for al in (1.5, 2.0, 2.5):
    base = Jopt(1.0, 0.3, 2.0, al)[1]
    out = []
    for b in (1.0, 10.0, 1e6):
        T, J = Jopt(b, 0.3, 2.0, al)
        out.append((b, J/base, b**((al-1)/al), (b/T)/J))
    print(f"alpha={al}: J*(beta)/J*(1) vs beta^((a-1)/a), sensing share:", [(b, round(r, 4), round(p, 4), round(sh, 4)) for b, r, p, sh in out])
print("=> J* is nondecreasing in the price per nat (envelope: dJ*/dc = reads/time > 0), so ANY actual price >= kT gives J* >= floor.")
print("   The optimum's cost SHARES do not depend on beta; only the scales T0, J1 move (by beta^(1/a), beta^((a-1)/a)).")
print("   beta itself is a measured, per-scale number (FRAMEWORK 3.11 beta_phys); the theory does not predict it.")

print("\n== 5. Kelly: the one currency-free exchange rate (horse race, proportional betting, fair odds): gain = I(X;Y) nats")
def kelly_gain(P):  # P[x,y]
    px = P.sum(1); py = P.sum(0); odds = 1/px
    g = 0
    for y in range(P.shape[1]):
        b = P[:, y]/py[y]                      # bet proportional to posterior
        g += sum(P[x, y]*np.log(b[x]*odds[x]) for x in range(P.shape[0]) if P[x, y] > 0)
    I = sum(P[x, y]*np.log(P[x, y]/(px[x]*py[y])) for x in range(P.shape[0]) for y in range(P.shape[1]) if P[x, y] > 0)
    return g, I
for _ in range(3):
    P = rng.random((4, 3)); P /= P.sum()
    g, I = kelly_gain(P); print(f"growth gain {g:.8f} nats vs mutual information {I:.8f} nats")

print("\n== 6. Temperature <-> survival constraint: P(ruin per window)=erfc(z/sqrt2)<=eps  <=>  B >= z_eps * sigma*sqrt(tau)")
for eps in (1e-2, 1e-3, 1e-6):
    z_eps = brentq(lambda z: 2*norm.sf(z)-eps, 0.1, 12)
    print(f"eps={eps:g}: z_eps={z_eps:.4f}")
# Monte-Carlo check of 2*Phi_bar(z) with Broadie-Glasserman-Kou continuity correction (barrier shift 0.5826*sigma*sqrt(dt))
N, M, z = 1000, 40000, 1.6
dt = 1.0/N
W = np.cumsum(rng.normal(0, np.sqrt(dt), (M, N)), axis=1)
hit = (W.max(1) >= z - 0.5826*np.sqrt(dt)).mean()
print(f"MC per-window ruin at z={z}: {hit:.4f} vs 2*Phi_bar(z)={2*norm.sf(z):.4f}")
z_eps = brentq(lambda z: 2*norm.sf(z)-1e-3, 0.1, 12)
for tau in (1, 4, 16, 64):
    print(f"tau={tau}: stress ceiling sigma_max = B/(z_eps sqrt(tau)) with B=1: {1/(z_eps*np.sqrt(tau)):.4f}  (ceiling x sqrt(tau) = {1/z_eps:.4f}, constant)")
print("=> the firm/volatility prediction 'risk ~ shock*sqrt(time to fix)/buffer' is the ruin constraint of the master equation in the diffusive-reset class;")
print("   'faster correction raises the stress ceiling' follows as sigma_max ~ tau^(-1/2). 'Stress strengthens' (adaptation) is NOT implied.")


# ------------------------------------------------------------------ assertions (used by tools/test_scale_free_checks.py)
import sys
bad = []
def chk(name, cond):
    if not cond: bad.append(name)
for al in (1.2, 1.5, 2.0, 2.5, 2.9):
    c, w, q = 5.0, 0.3, 2.0
    T, J = Jopt(c, w, q, al)
    chk(f"sensing share a={al}", abs((c/T)/J - (al-1)/al) < 1e-7)
    chk(f"error share a={al}", abs((w*q*T**(al-1)/al)/J - 1/al) < 1e-7)
    chk(f"looking:wrong = a-1, a={al}", abs((c/T)/(w*q*T**(al-1)/al) - (al-1)) < 1e-6)
    for b in (1.0, 1e3, 1e9):                       # floor multiplier and beta-independent shares
        Tb, Jb = Jopt(b*c, w, q, al)
        chk(f"floor multiplier a={al} beta={b}", abs(Jb/J - b**((al-1)/al)) < 1e-6*b**((al-1)/al))
        chk(f"share independent of beta a={al}", abs((b*c/Tb)/Jb - (al-1)/al) < 1e-7)
    lam_ = 10**rng.uniform(-6, 12)                  # currency invariance of the optimum
    T2, J2 = Jopt(c*lam_, w*lam_, q, al)
    chk(f"currency invariance a={al}", abs(T2/T - 1) < 1e-6 and abs(J2/(J*lam_) - 1) < 1e-6)
chk("two-tracker margins equal", abs(marg[0]-marg[1]) < 1e-5)
chk("z_eps 1e-3", abs(brentq(lambda z: 2*norm.sf(z)-1e-3, 0.1, 12) - 3.2905) < 1e-3)
chk("MC ruin within 8% of 2*Phibar(z)", abs(hit/(2*norm.sf(1.6)) - 1) < 0.08)
if bad:
    print("FAIL", bad); sys.exit(1)
print("\nRESULT: PASS")
