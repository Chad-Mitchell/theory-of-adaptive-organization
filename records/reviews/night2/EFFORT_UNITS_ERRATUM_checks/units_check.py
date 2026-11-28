"""EFFORT-UNITS-ERRATUM (pick 25): own first-principles check of N12 referee C3.
Imports nothing from the repo. Technology A_theta (formal Lemma 1(iii)): Kalman-Bucy steady error P = sqrt(q r)
(r = observation-noise intensity, precision = 1/r), cost J(r) = W sqrt(q r) + c r^(-theta), spend = c r^(-theta) = c*prec^theta.
Claims checked:
 (1) spend share of phi is constant, so spend/price = c r^-theta / c = prec^theta has elasticities (a, b) = (2t/(1+2t), t/(1+2t));
 (2) precision elasticities are (a/theta, b/theta) = (2/(1+2t), 1/(1+2t)); equal (a, b) iff theta = 1;
 (3) small-share onset vigilance (level effort / flat member effort at onset N*, h = 0, equal prices):
     slope in rho = -theta in spend/price units and -1 in precision units, for every theta (first-principles onset, numeric);
 (4) sign of each elasticity and the event V > 1 are the same in both units (V_prec = V_spend^(1/theta)).
"""
import numpy as np, sympy as sp
from scipy.optimize import minimize_scalar, brentq
W, q, c, r, t = sp.symbols('W q c r theta', positive=True)
J = W*sp.sqrt(q*r) + c*r**(-t)
rs = sp.solve(sp.diff(J, r), r)[0]
phi = sp.simplify(J.subs(r, rs)); spend = sp.simplify((c*r**(-t)).subs(r, rs)); prec = sp.simplify(1/rs)
el = lambda f, x: sp.simplify(sp.diff(sp.log(f), x)*x)
print("r* =", rs)
print("spend share =", sp.simplify(spend/phi))
print("phi elasticities (W, q):", el(phi, W), el(phi, q))
print("spend/price elasticities:", el(spend/c, W), el(spend/c, q))
print("precision elasticities:", el(prec, W), el(prec, q))
a, b = 2*t/(1+2*t), t/(1+2*t)
print("precision el == (a/theta, b/theta):", sp.simplify(el(prec, W)-a/t) == 0, sp.simplify(el(prec, q)-b/t) == 0)
print("small-share V exponent (b-a)/(1-a) spend units:", sp.simplify((b-a)/(1-a)), "; precision units:", sp.simplify((b-a)/(1-a)/t))

rng = np.random.default_rng(20261126)
def opt(Wv, qv, cv, th):
    f = lambda lr: Wv*np.sqrt(qv*np.exp(lr)) + cv*np.exp(-th*lr)
    res = minimize_scalar(f, bounds=(-60, 60), method='bounded', options={'xatol': 1e-12})
    rr = np.exp(res.x); return res.fun, cv*rr**(-th), 1/rr
print("\nNumeric elasticities (finite differences on scalar optimum), 6 random points:")
for _ in range(6):
    th = rng.uniform(0.3, 3); Wv, qv, cv = np.exp(rng.uniform(-2, 2, 3)); h = 1e-4
    _, s0, p0 = opt(Wv, qv, cv, th); _, s1, p1 = opt(Wv*np.exp(h), qv, cv, th); _, s2, p2 = opt(Wv, qv*np.exp(h), cv, th)
    print(f" theta={th:.3f}  spend el=({np.log(s1/s0)/h:.4f},{np.log(s2/s0)/h:.4f}) vs (a,b)=({2*th/(1+2*th):.4f},{th/(1+2*th):.4f})"
          f"  prec el=({np.log(p1/p0)/h:.4f},{np.log(p2/p0)/h:.4f}) vs (a/t,b/t)=({2/(1+2*th):.4f},{1/(1+2*th):.4f})")

print("\nOnset vigilance from first principles (architecture: N members, drift = shared rho*q + private q;"
      " flat member tracks total drift (1+rho)q with stakes W; level tracks rho*q with pooled stakes N*W; members then track q;"
      " h = 0, equal prices, onset N*: N phi(W,(1+rho)q) = phi(NW, rho q) + N phi(W, q)):")
def onset_V(rho, th, Wv=1.0, qv=1.0, cv=1.0):
    g = lambda lN: np.exp(lN)*opt(Wv, (1+rho)*qv, cv, th)[0] - opt(np.exp(lN)*Wv, rho*qv, cv, th)[0] - np.exp(lN)*opt(Wv, qv, cv, th)[0]
    lN = brentq(g, np.log(1e-3), np.log(1e40), xtol=1e-12)
    N = np.exp(lN)
    _, sL, pL = opt(N*Wv, rho*qv, cv, th); _, sm, pm = opt(Wv, (1+rho)*qv, cv, th)
    return N, sL/sm, pL/pm
out = {}
for th in (0.5, 1.0, 2.0):
    rhos = np.array([1e-4, 1e-3]) if th < 2 else np.array([1e-3, 1e-2]); Vs = np.array([onset_V(x, th)[1] for x in rhos]); Vp = np.array([onset_V(x, th)[2] for x in rhos])
    ss = np.diff(np.log(Vs))[0]/np.diff(np.log(rhos))[0]; sp_ = np.diff(np.log(Vp))[0]/np.diff(np.log(rhos))[0]
    ok = np.allclose(Vp, Vs**(1/th), rtol=1e-6)
    print(f" theta={th}: slope dlnV/dln rho over two small rho a decade apart: spend units {ss:.4f} (pred {-th}), precision units {sp_:.4f} (pred -1);"
          f" V_prec == V_spend^(1/theta): {ok}; V_spend={Vs[1]:.4g}, V_prec={Vp[1]:.4g} at rho={rhos[1]}")
    out[th] = (ss, sp_)
print("\nSign / threshold invariance: V_prec > 1 iff V_spend > 1 because V_prec = V_spend^(1/theta), theta > 0; elasticity signs equal since a/theta and a share a sign.")
