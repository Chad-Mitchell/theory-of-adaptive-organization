"""C6. Theorem P (persistence requires predictive information): for any agent, long-run mean loss >= D(I_pred),
so persistence (non-negative reserve drift) requires I_pred >= R(y - c). Checked on binary and Gaussian worlds."""
import numpy as np
from scipy import optimize, integrate, special
rng = np.random.default_rng(6)
h2 = lambda e: 0.0 if e in (0, 1) else -(e*np.log2(e)+(1-e)*np.log2(1-e))
hinv = lambda v: optimize.brentq(lambda e: h2(e)-v, 1e-15, 0.5, xtol=1e-15, rtol=1e-14) if v < 1 else 0.5
D_bern = lambda R: hinv(max(0.0, 1-R))     # Bernoulli(1/2), Hamming: D(R) = h^{-1}(1-R)
print("== C6a: binary symmetric Markov world (flip prob q), agent acts on X_{t+1} using a reading delayed by d steps ==")
q = 0.05
for d in [0, 2, 5, 10, 20]:
    e = (1-(1-2*q)**(d+1))/2; Ip = 1-h2(e)
    print(f"  delay d={d:2d}: error={e:.4f}  I_pred={Ip:.4f} bits  D(I_pred)={D_bern(Ip):.4f}  (bound tight: agent sits on D(R))")
print("  noisy 1-bit memory (stored bit flips w.p. eps each step it is held), d=3:")
for eps in [0.0, 0.02, 0.1]:
    e_mem = (1-(1-2*eps)**3)/2; e_world = (1-(1-2*q)**4)/2; e = e_mem*(1-e_world)+e_world*(1-e_mem)
    Ip = 1-h2(e); print(f"   eps={eps}: error={e:.6f}  >= D(I_pred)={D_bern(Ip):.6f}")
print("  ruin: reserve += y - 1[wrong] each step, start B=20, 20k steps, 4k agents")
def ruin(y, e, B=20, steps=20_000, n=4000):
    R = np.full(n, float(B)); alive = np.ones(n, bool)
    for _ in range(steps):
        R += y - (rng.random(n) < e); alive &= R > 0
    return 1-alive.mean()
for d in [2, 10]:
    e = (1-(1-2*q)**(d+1))/2
    for y in [e-0.02, e+0.02]:
        print(f"   d={d} (error {e:.3f}), income y={y:.3f}: ruin fraction={ruin(y, e):.3f}  (theorem: certain iff y < D(I_pred)={e:.3f})")
y = 0.30; dmax = max(d for d in range(200) if (1-(1-2*q)**(d+1))/2 < y)
print(f"  maximum viable lead time at income y={y}: d_max={dmax} steps (I(X_t;X_(t+d+1)) must exceed R(y)={1-h2(y):.4f} bits)")
print("== C6b: Gaussian AR(1) world, quadratic loss. D(R) = Var * 2^(-2R); linear-Gaussian agents achieve it exactly ==")
a, sv = 0.95, 1.0; VarX = sv**2/(1-a**2)
for d, nm in [(0, 0.0), (0, 1.0), (3, 0.5)]:
    # memory M = X_{t-d} + noise(nm); target X_{t+1}
    rho2 = (a**(d+1))**2*VarX/(VarX+nm**2) ; mse = VarX*(1-rho2); I = -0.5*np.log2(1-rho2)
    print(f"  d={d} noise={nm}: MSE={mse:.4f}  D(I_pred)=Var*2^(-2I)={VarX*2**(-2*I):.4f}")
# 1-bit quantizer M = sign(X_t): MSE = Var(1 - a^2 2/pi); I(sign X_t; X_{t+1}) numeric
cond_sd = sv; mu1 = a*np.sqrt(VarX)*np.sqrt(2/np.pi)
def I_sign():
    sx = np.sqrt(VarX); f = lambda x: 0.5*(special.erfc(-a*0/1))  # placeholder
    # p(x_{t+1}|s=+) = 2 * int_0^inf N(x_t;0,VarX) N(x_{t+1}; a x_t, sv^2) dx_t ; mixture density closed form via Owen-type erf
    marg = lambda y: np.exp(-y**2/(2*VarX))/np.sqrt(2*np.pi*VarX)
    # Y=aX+e with X|X>0: density = 2*marg(y)*Phi(a*sx*y/(sv*sqrt(VarX)) ... use joint Gaussian: corr r = a*sqrt(VarX)/sqrt(VarX)=a
    r = a; cplus = lambda y: 2*marg(y)*0.5*special.erfc(-(r*y/np.sqrt(VarX))/np.sqrt(1-r**2)/np.sqrt(2))
    integrand = lambda y: cplus(y)*np.log2(cplus(y)/marg(y)) if cplus(y) > 0 else 0.0
    return integrate.quad(integrand, -40, 40, limit=400)[0]   # I = E_s KL(p(y|s)||p(y)), symmetric in s
I1 = I_sign(); mse1 = VarX*(1-a**2*2/np.pi)
print(f"  1-bit sign memory: I_pred={I1:.4f} bits, MSE={mse1:.4f} > D(I_pred)={VarX*2**(-2*I1):.4f}  (bound holds, strictly: not on the frontier)")
print("== C6c: the thermodynamic layer (Still et al. 2012), for the binary world with perfect memory of X_t ==")
Imem, Ipred = 1.0, 1-h2(q)
print(f"  I_mem={Imem} bit, I_pred={Ipred:.4f} bit -> nonpredictive memory {Imem-Ipred:.4f} bit/step -> floor kT ln2 * {Imem-Ipred:.4f} per step (if Still's conditions hold)")
print("  Persistence fixes a floor on I_pred (C6a); dissipation penalizes I_mem - I_pred; together: min I_mem s.t. I_pred >= R(y-c) = an information-bottleneck point.")
print("== C6d: when does carrying a model pay? Gaussian AR(1): loss(I) = D(F(I)) = Var[(1-a^2) + a^2 2^(-2I)], cost kappa per bit ==")
import sympy as sp
I_, k_, V_, a_ = sp.symbols('I kappa V a', positive=True)
Lo = V_*((1-a_**2) + a_**2*2**(-2*I_)) + k_*I_
Istar = sp.solve(sp.diff(Lo, I_), I_)[0]
print("  I* =", sp.simplify(Istar), " ; carry a model (I*>0) iff kappa <", sp.simplify(-sp.diff(Lo - k_*I_, I_).subs(I_, 0)))
# numeric brute-force check: memory = X_t + Gaussian noise, scan noise
aa, VV, kk = 0.95, VarX, 0.8
best = min(((VarX*(1-(aa**2)*VarX/(VarX+n2)) + kk*0.5*np.log2(1+VarX/n2)), n2) for n2 in np.logspace(-4, 4, 4001))
Ist = float(Istar.subs({k_: kk, V_: VV, a_: aa}))
print(f"  brute force over memory noise: min cost={best[0]:.5f} at I_mem={0.5*np.log2(1+VarX/best[1]):.4f} bits; formula I*={Ist:.4f}")
print("  => optimal model size grows only logarithmically in (stakes x predictable variance / cost per bit); zero below the threshold.")
