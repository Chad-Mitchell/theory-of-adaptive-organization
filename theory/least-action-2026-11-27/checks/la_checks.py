"""Checks for DERIVATION.md (least action against the cost of judgment, class PATH).

Exact sympy identities plus small finite-dimensional numerical cross-checks. Run at nice 19:
  nice -n 19 python3 checks/la_checks.py > checks/la_checks.out
"""
import numpy as np
import sympy as sp

ok = True
def report(name, cond):
    global ok
    ok &= bool(cond)
    print(f"{'PASS' if cond else 'FAIL'}  {name}")

t, tau, g, w, wT, x0, x1, D, kT, M, om = sp.symbols('t tau gamma w w_tau x0 x1 D kT M omega', positive=True)
v = sp.symbols('v', real=True)

# --- 1. Free particle, open loop -------------------------------------------------------------
# Heat of an open-loop drift u(t): gamma*E[u^2] + kT*E[d_x u] = gamma*u^2 (d_x u = 0).
# Mean path xbar' = u; Var(X_t) = 2 D t, independent of u. Euler-Lagrange of gamma*xbar'^2: xbar'' = 0 (affine).
# Terminal transversality: 2 gamma xbar'(tau) + 2 wT (xbar(tau) - x1) = 0.
J_v = g*v**2*tau + wT*((x0 + v*tau - x1)**2 + 2*D*tau)
vstar = sp.solve(sp.diff(J_v, v), v)[0]
report("1a open-loop optimal constant velocity v* = wT(x1-x0)/(gamma+wT tau)",
       sp.simplify(vstar - wT*(x1 - x0)/(g + wT*tau)) == 0)
report("1b J(v)-J(v*) = (gamma tau + wT tau^2)(v-v*)^2 (strict minimum, any D)",
       sp.simplify(sp.expand(J_v - J_v.subs(v, vstar) - (g*tau + wT*tau**2)*(v - vstar)**2)) == 0)
report("1c wT -> oo: v* -> (x1-x0)/tau (classical free path)",
       sp.simplify(sp.limit(vstar, wT, sp.oo) - (x1 - x0)/tau) == 0)
report("1d wT = 0: v* = 0 whatever the endpoints (degenerate limit selects no path)", vstar.subs(wT, 0) == 0)
# heat on the mean path versus the free action S = int 1/2 M v^2 dt
Q_tot = g*vstar**2*tau
S_free = sp.Rational(1, 2)*M*vstar**2*tau
report("1e minimized heat = (2 gamma / M) * free action on the same path", sp.simplify(Q_tot - 2*g/M*S_free) == 0)
# units: gamma [J s m^-2] * v^2 [m^2 s^-2] * tau [s] = J ; S = kg m^2 s^-1 = J s ; ratio 2 gamma/M has s^-1
J_, s_, m_, kg = sp.symbols('J s m kg', positive=True)
units = {g: J_*s_/m_**2, v: m_/s_, tau: s_, M: kg}
heat_units = sp.simplify((g*v**2*tau).subs(units))
action_units = sp.simplify((M*v**2*tau).subs(units).subs(kg, J_*s_**2/m_**2))
report("1f units: heat on window is J, action is J s, ratio is 1/s",
       heat_units == J_ and sp.simplify(action_units - J_*s_) == 0)

# Numerical cross-check without Euler-Lagrange: N-step open-loop protocol, exact quadratic minimum.
N, gam, Tw, WT, a, b = 50, 1.3, 2.0, 7.0, 0.4, 1.9
dt = Tw/N
# J(u) = gam*sum(u^2)dt + WT*(a + sum(u)dt - b)^2 ; gradient = 0 -> (2 gam dt I + 2 WT dt^2 11^T) u = 2 WT dt (b-a) 1
A = 2*gam*dt*np.eye(N) + 2*WT*dt**2*np.ones((N, N))
u = np.linalg.solve(A, 2*WT*dt*(b - a)*np.ones(N))
report("1g discrete N=50 optimum has equal steps (affine path) to 1e-12", np.ptp(u) < 1e-12)
report("1h discrete optimum velocity equals v*", abs(u[0] - WT*(b - a)/(gam + WT*Tw)) < 1e-12)

# --- 2. Harmonic oscillator ---------------------------------------------------------------------
# Running stake w on (X - 0)^2: Euler-Lagrange gamma xbar'' = w xbar  (open loop; Var term is design-independent).
W = sp.symbols('W', real=True)   # signed stake, to show where the real-time oscillator sits
Om = sp.sqrt(w/g)
x_e = (x0*sp.sinh(Om*(tau - t)) + x1*sp.sinh(Om*t))/sp.sinh(Om*tau)
report("2a positive stake: sinh path solves gamma x'' = w x with ends x0, x1",
       sp.simplify(g*sp.diff(x_e, t, 2) - w*x_e) == 0 and sp.simplify(x_e.subs(t, 0) - x0) == 0
       and sp.simplify(x_e.subs(t, tau) - x1) == 0)
x_r = (x0*sp.sin(om*(tau - t)) + x1*sp.sin(om*t))/sp.sin(om*tau)
report("2b real-time path solves x'' = -omega^2 x", sp.simplify(sp.diff(x_r, t, 2) + om**2*x_r) == 0)
# Euler-Lagrange of gamma x'^2 + W x^2 is gamma x'' = W x; matching x'' = -omega^2 x needs W = -gamma omega^2 < 0.
Wsol = sp.solve(sp.Eq(W/g, -om**2), W)
report("2c match needs W = -gamma*omega^2 (negative stake, excluded by A8)", Wsol == [-g*om**2])
# Midpoint comparison, x0 = 0, x1 = 1, w = gamma omega^2 (same magnitude): sinh path vs sin path differ.
mid_e = float((sp.sinh(Om*tau/2)/sp.sinh(Om*tau)).subs({w: 1, g: 1, tau: 1}))
mid_r = float((sp.sin(om*tau/2)/sp.sin(om*tau)).subs({om: 1, tau: 1}))
print(f"      midpoint, x0=0, x1=1, |w|/gamma = omega^2 = 1, tau = 1: Euclidean {mid_e:.6f}, real-time {mid_r:.6f}")
report("2d with w>0 the selected path is not the real-time path (midpoints differ)", abs(mid_e - mid_r) > 1e-3)
# Second variation of int (gamma eta'^2 + W eta^2) with eta(0)=eta(tau)=0: eigenvalues gamma (n pi/tau)^2 + W.
print("      second variation, W = -gamma omega^2, gamma = omega = 1: lowest Dirichlet eigenvalue (n=1)")
signs = []
for r in [0.5, 0.9, 1.1, 2.0]:
    T_ = r*np.pi
    lam1 = (np.pi/T_)**2 - 1.0
    # numerical: discretized Hessian of sum gamma (dx)^2/dt - omega^2 x^2 dt, interior points
    n = 400; h = T_/n
    H = (2/h)*np.eye(n - 1) - (1/h)*(np.eye(n - 1, k=1) + np.eye(n - 1, k=-1)) - h*np.eye(n - 1)
    lmin = np.linalg.eigvalsh(H).min()/h   # scale to the continuum operator
    signs.append(np.sign(lam1))
    print(f"      tau*omega/pi = {r}: lambda_1 = {lam1:+.6f} (continuum), {lmin:+.6f} (n=400 grid); "
          f"{'minimum' if lam1 > 0 else 'saddle: J unbounded below along sin(pi t/tau)'}")
report("2e real-time oscillator: minimum for tau<pi/omega, saddle (no J minimum) for tau>pi/omega",
       signs == [1, 1, -1, -1])
report("2f any W >= 0: second variation positive for every tau (Euclidean, always a minimum)",
       all((np.pi/(r*np.pi))**2 + Wv >= 0 for r in [0.5, 0.9, 1.1, 2.0, 10.0] for Wv in [0.0, 1.0, 100.0]))

# --- 3. Linear feedback: where the information heat sits -----------------------------------------
# u = a(t) - k(t) X; X Gaussian with mean mu, variance V. mu' = a - k mu, V' = 2D - 2kV.
# Heat (Sekimoto, repo convention): Qdot = gamma E[u^2] + kT E[d_x u], with kT = gamma D.
mu, V, a_, k_ = sp.symbols('mu V a k', real=True)
V = sp.symbols('V', positive=True)
mudot = a_ - k_*mu
Vdot = 2*D - 2*k_*V
Qdot = g*((a_ - k_*mu)**2 + k_**2*V) + (g*D)*(-k_)
target = g*mudot**2 + g*Vdot**2/(4*V) - (g*D/2)*Vdot/V
report("3a Qdot = gamma mu'^2 + gamma V'^2/(4V) - (kT/2) d ln V/dt (mean and width decouple)",
       sp.simplify(sp.expand(Qdot - target)) == 0)
print("      the mean-path part gamma*mu'^2 is the open-loop free-particle cost; the information")
print("      (entropy) term -(kT/2) d ln V/dt acts only on the width V, so the selected mean path")
print("      is affine with or without feedback (certainty equivalence).")
print("RESULT:", "PASS" if ok else "FAIL")
