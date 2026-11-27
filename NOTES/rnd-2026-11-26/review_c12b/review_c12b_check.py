# Independent checks for HOSTILE_REVIEW_C12B.md. OBSERVED numerics, not proofs. kT = 1.
# Written by the reviewer; does not import or reuse c12b/c12bg code.
import numpy as np
rng = np.random.default_rng(2026)

# ---- (R1) OU generator normalization + LSI constant via direct Fokker-Planck evolution ----
# Leak channel: dm = -(D/s2) m dt + sqrt(2D) dW  ->  Gamma = D/s2, pi = N(0,s2).
# FP: dp/dt = d/dm [ D (dp/dm + p m/s2) ].  Check: -dD(p||pi)/dt = D * Fisher(p||pi) and >= 2 Gamma D(p||pi).
print("(R1) FP evolution under the leak alone, non-Gaussian starts (Laplace, uniform-ish, bimodal, skewed)")
x = np.linspace(-30, 30, 6001); dx = x[1]-x[0]
def Dkl(p, s2):
    lp = -x**2/(2*s2) - 0.5*np.log(2*np.pi*s2); m = p > 1e-300
    return np.sum(p[m]*(np.log(p[m]) - lp[m]))*dx
def fisher(p, s2):
    m = p > 1e-200; g = np.gradient(p, dx)/np.maximum(p, 1e-300) + x/s2
    return np.sum((p*g*g)[m])*dx
def fp_step(p, Dc, s2, dt):
    # conservative finite-volume step of dp/dt = d/dx[ D (dp/dx + p x/s2) ]
    xm = 0.5*(x[1:]+x[:-1]); pm = 0.5*(p[1:]+p[:-1])
    J = -Dc*((p[1:]-p[:-1])/dx + pm*xm/s2)          # flux at interfaces
    dp = np.zeros_like(p); dp[:-1] -= J/dx; dp[1:] += J/dx
    return p + dt*dp   # dp holds dp/dt
starts = {
 "laplace(1.5,0.7)": np.exp(-np.abs(x-1.5)/0.7),
 "box[0.5,3]":       0.5*(np.tanh((x-0.5)/0.05)-np.tanh((x-3)/0.05)),
 "bimodal":          np.exp(-(x+2)**2/0.3)+0.4*np.exp(-(x-3)**2/1.2),
 "skew":             np.where(x>0, x**2*np.exp(-x/0.6), 0.0),
}
for s2, Dc in [(1.0, 1.0), (2.5, 0.8)]:
    G = Dc/s2
    for name, p0 in starts.items():
        p = p0/np.sum(p0*dx); dt = 0.2*dx*dx/Dc
        for _ in range(int(0.3/dt)): p = fp_step(p, Dc, s2, dt)   # smooth briefly
        D0 = Dkl(p, s2); F0 = fisher(p, s2)
        n = 200; q = p.copy()
        for _ in range(n): q = fp_step(q, Dc, s2, dt)
        rate = -(Dkl(q, s2) - D0)/(n*dt)
        print(f"   s2={s2} Gamma={G:.3f} {name:17s}: -dD/dt={rate:.5f}  D*Fisher={Dc*F0:.5f}  ratio(-dD/dt)/(2*Gamma*D)={rate/(2*G*D0):.4f}")

# ---- (R2) LSI ratio over a non-mixture family: q ∝ pi * exp(poly) ----
print("(R2) LSI: (s2/2)*Fisher/D over q ∝ pi*exp(random cubic/quartic tilt), 400 draws")
worst = np.inf
for _ in range(400):
    s2 = rng.uniform(0.3, 3)
    c = rng.normal(0, 1, 4) * np.array([1.0, 0.5, 0.15, 0.03])
    lq = -x**2/(2*s2) + c[0]*x + c[1]*x**2/s2*0.3 + c[2]*x**3/s2**1.5 - abs(c[3])*x**4/s2**2
    lq -= lq.max(); q = np.exp(lq); q /= q.sum()*dx
    d = Dkl(q, s2)
    if d < 1e-6: continue
    worst = min(worst, (s2/2)*fisher(q, s2)/d)
print(f"   min ratio = {worst:.6f} (>=1 expected)")

# ---- (R3) two-channel OU heat, independent route: Gauss-Hermite quadrature of per-channel EP + Ito-heat Euler sim ----
print("(R3) two-channel OU with a corrector that knows x: per-channel EP by quadrature, and an Ito-form heat simulation")
def analytic(G, kap, s2, V):
    a = kap/(G+kap)
    return G*a*a*V/s2 + kap*(1-a)**2*V/s2
def quad(G, kap, s2, V):
    # p_{M|x} = N(a x, s2) stationary (s_C = s). EP_k = E[(drift_k - D_k d ln p)^2 / D_k]
    a = kap/(G+kap); DL, DC = G*s2, kap*s2
    gx, gw = np.polynomial.hermite_e.hermegauss(60); gw = gw/gw.sum()
    tot = 0.0
    for xx, wx in zip(np.sqrt(V)*gx, gw):
        for zz, wz in zip(np.sqrt(s2)*gx, gw):
            m = a*xx + zz; dlp = -(m - a*xx)/s2
            jL = -G*m - DL*dlp; jC = -kap*(m-xx) - DC*dlp
            tot += wx*wz*(jL**2/DL + jC**2/DC)
    return tot
print(f"   G=1,kap=3,s2=1,V=2: analytic={analytic(1,3,1,2):.6f} quadrature={quad(1,3,1,2):.6f}")
for (G,kap,s2,V) in [(0.5,2.0,1.5,3.0),(2.0,0.7,0.8,1.0)]:
    print(f"   G={G},kap={kap},s2={s2},V={V}: analytic={analytic(G,kap,s2,V):.6f} quadrature={quad(G,kap,s2,V):.6f}")
G,kap,s2,V = 1.0,3.0,1.0,2.0
N, dt, T, burn = 20000, 1e-3, 25.0, 5.0
X = rng.normal(0, np.sqrt(V), N); a = kap/(G+kap); m = a*X + rng.normal(0, np.sqrt(s2), N)
Q = np.zeros(N); steps = int(T/dt); nb = int(burn/dt)
for k in range(steps):
    FL = -m/s2; FC = -(m-X)/s2                     # forces in kT units
    dWL = rng.normal(size=N)*np.sqrt(dt); dWC = rng.normal(size=N)*np.sqrt(dt)
    dmL = G*s2*FL*dt + np.sqrt(2*G*s2)*dWL; dmC = kap*s2*FC*dt + np.sqrt(2*kap*s2)*dWC
    if k >= nb:   # Ito -> Stratonovich: F∘dm = F dm + 0.5 F' (dm)^2, F' = -1/s2 per channel
        Q += FL*dmL - 0.5/s2*(2*G*s2*dt) + FC*dmC - 0.5/s2*(2*kap*s2*dt)
    m = m + dmL + dmC
tt = (steps-nb)*dt
print(f"   Ito-corrected Euler (dt={dt}): heat rate = {Q.mean()/tt:.4f} +- {Q.std()/tt/np.sqrt(N):.4f}  (analytic 1.5)")

# ---- (R4) live source, separate-leak carrier: leak EP grows with Gamma at fixed information ----
print("(R4) LIVE OU source (rate r, var v), tracker with a SEPARATE leak channel (P1-type), conditional var s2")
r, v, s2 = 0.4, 2.0, 1.0
def live(G, kap):
    lam = G + kap
    varmu = kap**2*v/(lam*(lam+r)); cov = kap*v/(lam+r)
    I = -0.5*np.log(1 - cov**2/(v*(varmu+s2)))
    sigL = G*varmu/s2           # leak-channel EP, conditioned on the source path: p(m|path)=N(mu,s2)
    return I, sigL
for Itarget in [0.05, 0.3]:
    for G in [0.0, 0.2, 1.0, 5.0]:
        lo, hi = 1e-6, 1e4
        for _ in range(200):
            k = np.sqrt(lo*hi)
            if live(G, k)[0] < Itarget: lo = k
            else: hi = k
        I, sL = live(G, k)
        print(f"   I(X_t;M_t)={I:.3f} Gamma={G:4.1f}: kappa={k:9.4f} leak EP={sL:.4f}  2*Gamma*I={2*G*I:.4f}")
