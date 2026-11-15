"""Task 1 checks: one objective, thermodynamic tracking floor vs EOQ, rule 5 hops, rule 7 watching."""
import numpy as np, sympy as sp
import importlib.util, sys
spec = importlib.util.spec_from_file_location("fpt", "fpt_checks.py")

# --- 1. Thermodynamic floor of tracking a random walk has the EOQ form with c = kT (per nat)
s, w, kT, D, c, T = sp.symbols('sigma w kT D c T', positive=True)
Jth = kT*s**2/(2*D) + w*D            # min dissipation rate (learning-rate bound) + quadratic loss
Dstar = sp.solve(sp.diff(Jth, D), D)[0]
Jth_star = sp.simplify(Jth.subs(D, Dstar))
Jeoq = c/T + w*s**2*T/2
Tstar = sp.solve(sp.diff(Jeoq, T), T)[0]
Jeoq_star = sp.simplify(Jeoq.subs(T, Tstar))
Davg_eoq = sp.simplify(s**2*Tstar/2)
print("== 1. thermo floor vs EOQ ==")
print("  thermo: D* =", Dstar, "  J* =", Jth_star)
print("  EOQ:    T* =", Tstar, "  J* =", Jeoq_star, "  mean error var =", Davg_eoq)
print("  J* equal under c -> kT:", sp.simplify(Jth_star - Jeoq_star.subs(c, kT)) == 0,
      "; mean error equal:", sp.simplify(Dstar - Davg_eoq.subs(c, kT)) == 0)
# Berger (1970) non-causal rate floor: R(D)=2 sigma^2/(pi^2 D) nats/s -> weaker floor
Jb = kT*2*s**2/(sp.pi**2*D) + w*D
Db = sp.solve(sp.diff(Jb, D), D)[0]
print("  Berger-floor J* =", sp.simplify(Jb.subs(D, Db)), " ratio to learning-rate floor =",
      sp.nsimplify(sp.simplify(Jb.subs(D, Db)/Jth_star)))
# Duncan (1970) consistency: Kalman-Bucy, dy = x dt + sqrt(r) dv, dx = sigma dW: P = sigma sqrt(r),
# I-rate = P/(2r); info lost to drift = sigma^2/(2P)
r = sp.symbols('r', positive=True)
P = s*sp.sqrt(r)
print("  Kalman-Bucy: Duncan I-rate P/(2r) =", sp.simplify(P/(2*r)), "; drift info-loss sigma^2/(2P) =", sp.simplify(s**2/(2*P)))

# --- 2. Rule 5: copy-of-copy error grows linearly in hops (variance) and with drift
rng = np.random.default_rng(3)
def chain_err(nhops, Tcopy=1.0, sigma=1.0, r_copy=0.0, n=200000):
    # stationary: each hop's copy has age ~ U(0,Tcopy) relative to its upstream at read time, independent phases
    ages = rng.uniform(0, Tcopy, size=(n, nhops)).sum(1)
    return np.mean((sigma*np.sqrt(ages)*rng.standard_normal(n))**2) + nhops*r_copy
print("\n== 2. rule 5: E[err^2] of a copy n hops from source (sigma=1, refresh T=1) ==")
for nh in [1, 2, 4, 8]:
    print(f"  hops={nh}: MC {chain_err(nh):.3f}  theory sigma^2*n*T/2 = {nh*0.5:.3f};  sigma=2: {chain_err(nh, sigma=2.0):.3f} (theory {nh*2.0:.3f})")

# --- 3. Rule 7: value of watching (shortening tau) vs shock/buffer
exec(open("fpt_core.py").read())
print("\n== 3. rule 7: marginal value of faster fixing, as shock grows (B, tau fixed) ==")
print("  G(z) = -(dh/dln tau)*tau = F(z)*eps_tau(z)  [expected failures avoided per unit time, x tau]")
print("  V(z) = G/(rho*tau + F)^2 * ... : value of survival with discount rho (here rho*tau = 0.05)")
def eps_tau(m, z, d=1e-4):
    lnF = lambda zz: np.log(m(zz))
    return -1 - 0.5*(lnF(z*np.exp(d)) - lnF(z*np.exp(-d)))/(2*d)
zs = np.exp(np.linspace(np.log(0.15), np.log(5), 40))
for name, m in [("A", F_A), ("B", F_B), ("C", F_C)]:
    G = np.array([m(z)*eps_tau(m, z) for z in zs])
    rho = 0.05
    V = np.array([m(z)*eps_tau(m, z)/(rho + m(z))**2 for z in zs])
    iG, iV = np.argmax(G), np.argmax(V)
    print(f"  {name}: G at z=0.15: {G[0]:.4f}, max G {G[iG]:.4f} at z={zs[iG]:.2f}, G at z=5: {G[-1]:.2e};"
          f"  V max at z={zs[iV]:.2f} (h*tau there={m(zs[iV]):.3f}; interior: {0<iV<len(zs)-1})")
