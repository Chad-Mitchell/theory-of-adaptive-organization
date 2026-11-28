"""Checks for theory/osc-structure-2026-11-28 (PREREG.md locked at edddf23).
Run: OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 nice -n 19 python3 checks/osc_checks.py
Small compute only: closed forms first, then grids and one short delay-equation integration."""
import numpy as np, sympy as sp
from scipy.linalg import solve_continuous_are as care
from scipy.optimize import minimize_scalar, brentq

OK = []
def check(name, cond, msg=""):
    OK.append(bool(cond)); print(f"[{'PASS' if cond else 'MISS'}] {name} {msg}")

print("== OS-A1 rotating world: Kalman-Bucy memory frequency")
a, w0, s, so, P = sp.symbols('a omega0 sigma sigma_o P', positive=True)
Psol = [r for r in sp.solve(sp.Eq(-2*a*P + s**2 - P**2/so**2, 0), P) if r.is_positive is not False]
Psol = sp.simplify(Psol[0]); K = Psol/so**2
F = -a + sp.I*w0 - K
print("  P =", Psol, "; Im F =", sp.simplify(sp.im(F)))
check("A1a Im F = omega0 symbolically", sp.simplify(sp.im(F) - w0) == 0)
rng = np.random.default_rng(1)
maxdev = 0.0
for _ in range(200):
    av, wv, sv, sov = rng.uniform(0.05, 3, 4)
    A = np.array([[-av, -wv], [wv, -av]]); Cm = np.eye(2)
    Pm = care(A.T, Cm.T, sv**2*np.eye(2), sov**2*np.eye(2))
    Km = Pm @ Cm.T / sov**2
    ev = np.linalg.eigvals(A - Km @ Cm)
    maxdev = max(maxdev, abs(np.max(np.abs(ev.imag)) - wv))
check("A1b numeric 2D filter: |Im eig| = omega0 (200 draws)", maxdev < 1e-9, f"max dev {maxdev:.2e}")
A = np.array([[-1.0, 0], [0, -1.0]]); Pm = care(A.T, np.eye(2), np.eye(2), np.eye(2))
check("A1c omega0=0: filter real", np.max(np.abs(np.linalg.eigvals(A - Pm).imag)) < 1e-12)

print("== OS-A2 lagged integrating world, optimal predictor design")
nu, k, tau, sig = sp.symbols('nu k tau sigma', positive=True)
X, Xh, U, Xi = sp.symbols('X Xh U Xi')
E = sp.exp(-sp.I*nu*tau)
sol = sp.solve([sp.Eq(X, U/(sp.I*nu) + sig*Xi/(sp.I*nu)), sp.Eq(Xh, E*X + U*(1-E)/(sp.I*nu)), sp.Eq(U, -k*Xh)], [X, Xh, U], dict=True)[0]
H = sp.simplify(sol[X]/Xi)
Hclaim = sig*(k + sp.I*nu - k*E)/(sp.I*nu*(k + sp.I*nu))
check("A2a transfer H = sigma(k+i nu-k e^{-i nu tau})/(i nu (k+i nu))", sp.simplify(H - Hclaim) == 0)
# variance and optimal gain
kk, ww, rr = sp.symbols('kk w r', positive=True)
Jk = rr*kk*sig**2/2 + ww*(sig**2/(2*kk) + sig**2*tau)
kst = sp.solve(sp.diff(Jk, kk), kk)
check("A2b CE gain k* = sqrt(w/r) minimizes J over the predictor family", sp.simplify(kst[0] - sp.sqrt(ww/rr)) == 0, f"k* = {kst}")
Sfun = sp.lambdify((nu, k, tau), sp.simplify(sp.Abs(Hclaim/sig)**2), 'numpy')
def S_A2(nuv, kv, tv=1.0):
    e = np.exp(-1j*nuv*tv); return np.abs(kv + 1j*nuv - kv*e)**2/(nuv**2*(kv**2 + nuv**2))
nug = np.linspace(1e-4, 60, 600001)
# numeric variance check against sigma^2/(2k)+sigma^2 tau at k=1,tau=1
var_num = np.trapezoid(S_A2(np.linspace(1e-6, 4000, 4000001), 1.0), np.linspace(1e-6, 4000, 4000001))/np.pi
check("A2c Var x = sigma^2/(2k)+sigma^2 tau (k=tau=1, spectral integral)", abs(var_num - 1.5) < 2e-3, f"{var_num:.5f} vs 1.5")
A2_ok = True
for kt in [0.1, 0.5, 1, 2, 5, 10]:
    Sv = S_A2(nug, kt); S0 = (1 + kt)**2/kt**2
    i = np.argmax(Sv); interior = Sv[i] > S0*(1 + 1e-9) and nug[i] > 1e-3
    # local maxima list
    loc = np.where((Sv[1:-1] > Sv[:-2]) & (Sv[1:-1] > Sv[2:]))[0] + 1
    print(f"  k tau={kt:5}: S(0+)={S0:.6g}, global max at nu={nug[i]:.4g} (S={Sv[i]:.6g}); interior local maxima: {len(loc)}"
          + (f", first at nu*tau={nug[loc[0]]:.4f} S/S0={Sv[loc[0]]/S0:.4g}" if len(loc) else ""))
    A2_ok &= not interior
check("A2d OS-A2: global max of S_x at nu=0 for every listed k tau", A2_ok)

print("== OS-B1 reduced cost of coupled stores (Schur complement)")
g1, g2, w1, w2, c, om = sp.symbols('gamma1 gamma2 w1 w2 c omega', positive=True)
Hs = sp.Matrix([[g1*nu**2 + w1 + c, -c], [-c, g2*nu**2 + w2 + c]])
red = sp.simplify(Hs[0, 0] - Hs[0, 1]**2/Hs[1, 1])
Weff = sp.simplify(red - g1*nu**2)
check("B1a W_eff = w1 + c(g2 nu^2+w2)/(g2 nu^2+w2+c)", sp.simplify(Weff - (w1 + c*(g2*nu**2 + w2)/(g2*nu**2 + w2 + c))) == 0)
Wim = sp.simplify(Weff.subs(nu, sp.I*om))
print("  W_eff(i omega) =", Wim)
f = sp.lambdify((om,), Wim.subs({g1: 1, g2: 1, w1: 0.1, w2: 1, c: 2}))
omg = np.linspace(0, 3, 30001); vals = f(omg)
neg = omg[vals < 0]
print(f"  example g1=g2=1,w1=0.1,w2=1,c=2: W_eff(i omega)<0 for omega in [{neg.min():.4f},{neg.max():.4f}] (sqrt(w2/g2)=1, sqrt((w2+c)/g2)={np.sqrt(3):.4f})")
check("B1b negative only at imaginary frequency, inside (sqrt(w2/g2), sqrt((w2+c)/g2))", neg.size > 0 and neg.min() > 1 and neg.max() < np.sqrt(3))
# random PSD symbols incl. gyroscopic coupling: reduced >= 0 on a real nu grid
worst = np.inf
for _ in range(2000):
    G1, G2, K1, K2, Cc = rng.uniform(0.01, 3, 5)
    gmax = 2*np.sqrt(min(G1*K2, G2*K1)) if True else 0
    gg = rng.uniform(-1, 1)*gmax*0.999
    nv = np.linspace(-20, 20, 2001)
    h11 = G1*nv**2 + K1 + Cc; h22 = G2*nv**2 + K2 + Cc; h12 = -Cc + 1j*gg*nv
    det = h11*h22 - np.abs(h12)**2
    if np.min(det) < 0: continue
    worst = min(worst, np.min(h11 - np.abs(h12)**2/h22))
check("B1c reduced symbol >= 0 at every real nu for PSD symbols incl. gyroscopic (2000 draws)", worst >= -1e-12, f"min {worst:.3e}")

print("== OS-B2 two stores in series: J-optimal closed loop")
def lqr(A, B, Q, R):
    Pm = care(A, B, Q, R); return np.linalg.solve(R, B.T @ Pm)
dev = 0; zmin = np.inf; c0min = np.inf; peak_any = False
for _ in range(500):
    wv, pv, rv = rng.uniform(0.01, 10, 3); pv = pv*rng.integers(0, 2)
    Kg = lqr(np.array([[0, 1.], [0, 0]]), np.array([[0], [1.]]), np.diag([wv, pv]), np.array([[rv]]))
    c0, c1 = Kg[0, 0], Kg[0, 1]
    zeta = c1/(2*np.sqrt(c0)); zc = np.sqrt(0.5 + pv/(4*np.sqrt(wv*rv)))
    dev = max(dev, abs(c0 - np.sqrt(wv/rv)), abs(zeta - zc)); zmin = min(zmin, zeta); c0min = min(c0min, c0)
    nv = np.linspace(0, 20*np.sqrt(c0), 20001); Sx = 1/((c0 - nv**2)**2 + (c1*nv)**2)
    peak_any |= (np.argmax(Sx) > 0 and Sx.max() > Sx[0]*(1 + 1e-9))
check("B2a c0 = sqrt(w/r), zeta = sqrt(1/2 + p/(4 sqrt(w r))) (500 draws)", dev < 1e-8, f"max dev {dev:.2e}")
check("B2b c0 > 0 (W_dyn < 0) and zeta >= 1/sqrt2, no spectral peak", c0min > 0 and zmin >= 1/np.sqrt(2) - 1e-9 and not peak_any, f"min zeta {zmin:.6f}")
# one store: dx = u dt + noise, cost r u^2 + w x^2 -> dx = -sqrt(w/r) x: first order, no restoring second-order term
check("B2c one store: closed loop first order (xddot = +k^2 x along decay: Euclidean sign)", True, "(by inspection: x' = -k x gives x'' = k^2 x)")

print("== OS-B3 n stores in series: Butterworth")
B3_zr = True; B3_pk = True; B3_flat = 0.0
for n in range(1, 9):
    A = np.diag(np.ones(n - 1), 1); B = np.zeros((n, 1)); B[-1, 0] = 1
    Q = np.zeros((n, n)); Q[0, 0] = 1.0
    for wr in [1.0, 7.0]:
        Kg = lqr(A, B, wr*Q, np.array([[1.0]]))
        ev = np.linalg.eigvals(A - B @ Kg)
        zeta = np.min(-ev.real/np.abs(ev)); pred = np.sin(np.pi/(2*n))
        rad = np.abs(ev); radp = wr**(1/(2*n))
        nv = np.linspace(0, 6*radp, 60001)
        poly = np.poly(ev).real; Sx = 1/np.abs(np.polyval(poly, 1j*nv))**2
        pk = np.argmax(Sx) > 0 and Sx.max() > Sx[0]*(1 + 1e-9)
        B3_zr &= abs(zeta - pred) < 1e-6 and np.max(np.abs(rad - radp)) < 1e-6
        B3_pk &= (pk == (n >= 3))
        # diagnostic (added after the first run, DEVIATIONS.md): |p(i nu)|^2 = nu^(2n) + w/r, so S_x1 is monotone
        flat = np.max(np.abs(np.abs(np.polyval(poly, 1j*nv))**2 - (nv**(2*n) + wr))/(nv**(2*n) + wr))
        B3_flat = max(B3_flat, flat)
        if wr == 1.0:
            print(f"  n={n}: zeta_min={zeta:.7f} (sin(pi/2n)={pred:.7f}), |pole|={rad.max():.6f}, peak at nu>0: {pk}, slowest-mode angle from decay axis = {np.degrees(np.arccos(zeta)):.2f} deg")
check("B3-i Butterworth zeta_n = sin(pi/2n), |pole| = (w/r)^(1/2n) (n=1..8, two stake ratios)", B3_zr)
check("B3-ii locked peak rule: S_x1 has a peak at nu>0 iff n>=3", B3_pk)
print(f"  diagnostic: max rel. dev of |p(i nu)|^2 from nu^(2n)+w/r = {B3_flat:.2e} (S_x1 = sigma^2/(nu^(2n)+w/r), maximally flat, never peaked)")

print("== OS-C1 lagged reading, memoryless gain")
def var_km(z):  # Var * k / sigma^2 ... return Var/(sigma^2 tau) as function of z = k tau
    return (1 + np.sin(z))/(2*z*np.cos(z))
# spectral check of the Kuchler-Mensch variance at z = 0.3, 0.74, 1.2 (tau=1, sigma=1)
for z in [0.3, 0.74, 1.2]:
    nv = np.linspace(-3000, 3000, 6000001); Sx = 1/np.abs(1j*nv + z*np.exp(-1j*nv))**2
    vn = np.trapezoid(Sx, nv)/(2*np.pi)
    check(f"C1a Kuchler-Mensch variance at z={z}", abs(vn - var_km(z)) < 2e-3*var_km(z), f"{vn:.5f} vs {var_km(z):.5f}")
def zstar(rho):
    g = lambda z: (z**2 + rho)*(1 + np.sin(z))/(z*np.cos(z))
    return minimize_scalar(g, bounds=(1e-6, np.pi/2 - 1e-9), method='bounded', options={'xatol': 1e-12}).x
zinf = minimize_scalar(lambda z: (1 + np.sin(z))/(z*np.cos(z)), bounds=(1e-6, np.pi/2 - 1e-9), method='bounded', options={'xatol': 1e-12}).x
rhos = [0.01, 0.1, 1, 3, 10, 30, 100, 1e3, 1e4, 1e6]
zs = [zstar(r) for r in rhos]
for r, z in zip(rhos, zs): print(f"  rho={r:g}: z*={z:.6f}")
print(f"  z_inf = argmin (1+sin z)/(z cos z) = {zinf:.6f}")
check("C1(i) z* < pi/2 at every rho on the grid", max(zs) < np.pi/2 - 1e-3)
check("C1(ii) z_inf in [0.70, 0.78]", 0.70 <= zinf <= 0.78, f"{zinf:.6f}")
# peak rule: S_x(nu) = 1/(nu^2 - 2 k nu sin(nu tau) + k^2): peak at nu>0 iff z>1/2
rule_ok = True
for z in [0.3, 0.45, 0.49, 0.51, 0.55, 0.74, 1.0, 1.4]:
    nv = np.linspace(0, 6, 600001); Sx = 1/(nv**2 - 2*z*nv*np.sin(nv) + z**2)
    pk = np.argmax(Sx) > 0 and Sx.max() > Sx[0]*(1 + 1e-12)
    rule_ok &= (pk == (z > 0.5))
check("C1(iii-a) peak at nu>0 iff z > 1/2 (8 values)", rule_ok)
rho_c = brentq(lambda r: zstar(r) - 0.5, 1e-3, 1e4, xtol=1e-10)
check("C1(iii-b) rho_c in [1, 30]", 1 <= rho_c <= 30, f"rho_c = {rho_c:.6f}")
nv = np.linspace(1e-4, 6, 600001); Sx = 1/(nv**2 - 2*zinf*nv*np.sin(nv) + zinf**2)
nupk = nv[np.argmax(Sx)]; Tpk = 2*np.pi/nupk
print(f"  at z_inf: peak nu*tau = {nupk:.5f}, period = {Tpk:.4f} tau, peak/zero ratio = {Sx.max()/Sx[0]:.4f}")
check("C1(iv) peak period in [5 tau, 9 tau]", 5 <= Tpk <= 9, f"{Tpk:.4f}")
# dominant root of lambda = -z e^{-lambda} at z_inf (period of the free ringing)
from scipy.special import lambertw
lam = lambertw(-zinf, 0)  # lambda e^{lambda} = -z  -> lambda = W(-z)
print(f"  dominant root lambda tau = {complex(lam):.5f}; ringing period 2pi/Im = {2*np.pi/abs(lam.imag):.4f} tau; zeta = {-lam.real/abs(lam):.4f}")

print("== OS-C2 fixed price per action, steady drain")
U, L, d, ka, wv2 = sp.symbols('U L d k_a w', real=True)
rate = ka*d/(U - L) + wv2*(U**2 + U*L + L**2)/3
Asym = sp.symbols('A', positive=True)
symrate = sp.simplify(rate.subs({U: Asym, L: -Asym}))
Ast = sp.solve(sp.diff(symrate, Asym), Asym)
Tst = sp.simplify(2*Ast[0]/d)
Tclaim = lambda dv, kv, wv: 2*(3*kv/(4*wv*dv**2))**(1/3)
devT = max(abs(float(Tst.subs({d: dv, ka: kv, wv2: wv})) - Tclaim(dv, kv, wv)) for dv, kv, wv in [(1.3, 0.7, 2.1), (0.2, 5.0, 0.3), (4.0, 0.01, 9.0)])
check("C2a symmetric optimum: T* = 2 (3 k_a/(4 w d^2))^(1/3) (= (6 k_a/(w d^2))^(1/3))", devT < 1e-12, f"T* = {Tst}; max dev {devT:.1e}")
# full numeric over (U, L): optimum symmetric
from scipy.optimize import minimize
fr = lambda v: 0.7*1.3/(v[0] - v[1]) + 2.1*(v[0]**2 + v[0]*v[1] + v[1]**2)/3 if v[0] > v[1] else 1e9
res = minimize(fr, [1.0, -0.2], method='Nelder-Mead', options={'xatol': 1e-12, 'fatol': 1e-14, 'maxiter': 20000})
Tnum = (res.x[0] - res.x[1])/1.3
check("C2b unrestricted (U,L) optimum is symmetric and matches T*", abs(res.x[0] + res.x[1]) < 1e-6 and abs(Tnum - 2*(3*0.7/(4*2.1*1.69))**(1/3)) < 1e-6, f"U={res.x[0]:.6f} L={res.x[1]:.6f} T={Tnum:.6f}")
dd = sp.symbols('dd', positive=True)
check("C2c T* -> infinity as d -> 0 (T* ~ d^(-2/3))", sp.limit(Tst.subs(d, dd).subs({ka: 1, wv2: 1}), dd, 0, '+') == sp.oo)

print("== OS-C3 delayed adaptation with a saturating step")
def dde(mu, T=400.0, dt=1e-3, x0=0.1):
    nd = int(round(1/dt)); N = int(T/dt); x = np.empty(N + nd); x[:nd + 1] = x0
    for i in range(nd, N + nd - 1):
        x[i + 1] = x[i] - dt*mu*np.tanh(x[i - nd])
    return x[nd:], dt
for mu, lab in [(0.9*np.pi/2, "0.9x"), (1.1*np.pi/2, "1.1x")]:
    x, dt = dde(mu); tail = x[int(0.75*len(x)):]
    amp = np.max(np.abs(tail))
    zc = np.where((tail[:-1] < 0) & (tail[1:] >= 0))[0]
    per = np.mean(np.diff(zc))*dt if len(zc) > 2 else float('nan')
    print(f"  mu={lab} onset: late amplitude {amp:.5f}, period {per:.4f} tau, mean J excess (x^2/2) {np.mean(tail**2)/2:.5f}")
    if lab == "1.1x":
        x2, _ = dde(mu, x0=2.0); amp2 = np.max(np.abs(x2[int(0.75*len(x2)):]))
        check("C3 stable cycle at 1.1x onset: period in [4.0,4.6] tau, amplitude < 1.5, same cycle from x0=0.1 and 2.0, excess > 0",
              4.0 <= per <= 4.6 and amp < 1.5 and abs(amp - amp2) < 1e-3 and np.mean(tail**2) > 0, f"amp {amp:.5f} vs {amp2:.5f}")
    else:
        check("C3 decays below onset (0.9x)", amp < 1e-3)

print("== OS-D no imaginary-axis eigenvalue at strictly positive prices (B2, B3)")
mre = np.inf
for _ in range(300):
    n = rng.integers(1, 9); A = np.diag(np.ones(n - 1), 1); B = np.zeros((n, 1)); B[-1, 0] = 1
    Q = np.diag(rng.uniform(0.01, 5, n)); Kg = lqr(A, B, Q, np.array([[rng.uniform(0.01, 5)]]))
    mre = min(mre, np.min(-np.linalg.eigvals(A - B @ Kg).real))
check("D closed-loop eigenvalues strictly in the left half plane (300 draws, n<=8)", mre > 0, f"min -Re = {mre:.4e}")

print("RESULT", "PASS" if all(OK) else f"{OK.count(False)} locked checks MISS; see RESULTS.md")
