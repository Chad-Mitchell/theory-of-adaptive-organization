"""Check C1 (class CK): internal clock vs paid reads, with the TUR as the clock's heat floor.
J(f, w', D) = kap*kT*w'^2/D + c*f + w*[ (om-w')^2/(3 f^2) + (D + Dw)/f ]
Claims checked (Dw = 0):
  (a) clock appears iff c > 6*kap*kT, for every stake w and frequency om;
  (b) above: J* = 3((c-3 kap kT) kap kT om^2 w)^(1/3), w'/om = 1 - 3 kap kT/(c - 3 kap kT);
      below: J* = (9/4 c^2 w om^2)^(1/3) (no clock);
  (c) shares of clock heat / read spend / loss -> 1/3 each as c/(kap kT) -> inf;
  (d) Monte Carlo of a ring clock (Markov jump, N states) between perfect reads reproduces the error formula,
      and the ring's TUR factor kap = (k+ + k-) ln(k+/k-) / (2 (k+ - k-)) >= 1, -> 1 near equilibrium.
"""
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(20261123)
kT = 1.0

def J(p, c, w, om, kap, Dw=0.0):
    lf, lD, u = p
    f, D = np.exp(lf), np.exp(lD)
    wp = om / (1 + np.exp(-u))          # w' in (0, om)
    return kap*kT*wp**2/D + c*f + w*((om-wp)**2/(3*f**2) + (D+Dw)/f)

def J_noclock(c, w, om, Dw=0.0):
    # w'=0 (no clock, D irrelevant -> 0): J = c f + w(om^2/(3 f^2) + Dw/f)
    best = np.inf
    for lf0 in np.linspace(-8, 8, 33):
        r = minimize(lambda q: c*np.exp(q[0]) + w*(om**2/(3*np.exp(2*q[0])) + Dw/np.exp(q[0])), [lf0], method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-14, maxiter=4000))
        best = min(best, r.fun)
    return best

def numopt(c, w, om, kap, Dw=0.0):
    best = (np.inf, None)
    for lf0 in (-3, 0, 3):
        for lD0 in (-4, 0, 4):
            for u0 in (-4, 0, 4):
                r = minimize(J, [lf0, lD0, u0], args=(c, w, om, kap, Dw), method='Nelder-Mead',
                             options=dict(xatol=1e-12, fatol=1e-14, maxiter=20000, maxfev=40000))
                if r.fun < best[0]: best = (r.fun, r.x)
    jn = J_noclock(c, w, om, Dw)
    return min(best[0], jn), best, jn

def closed(c, w, om, kap):
    if c <= 6*kap*kT:
        return (9/4*c**2*w*om**2)**(1/3), 0.0
    return 3*((c-3*kap*kT)*kap*kT*om**2*w)**(1/3), 1 - 3*kap*kT/(c-3*kap*kT)

print("(a,b) closed form vs numerical minimum, random (c/kap kT, w, om, kap)")
maxrel = 0; n = 0
for _ in range(60):
    kap = rng.uniform(1, 3); c = kap*kT*np.exp(rng.uniform(np.log(1), np.log(200)))
    w = np.exp(rng.uniform(-3, 5)); om = np.exp(rng.uniform(-2, 3))
    jnum, best, jn = numopt(c, w, om, kap)
    jc, frac = closed(c, w, om, kap)
    rel = abs(jnum-jc)/jc; maxrel = max(maxrel, rel); n += 1
    if rel > 1e-5: print("  MISMATCH", c/kap, w, om, jnum, jc)
print(f"  {n} cases, max relative gap {maxrel:.2e}")

print("(a) threshold scan: clock fraction w'/om at the numerical optimum vs c/(kap kT); several (w, om)")
for (w, om) in [(0.1, 0.5), (10, 3), (1000, 0.2)]:
    row = []
    for ratio in (4, 5.5, 5.9, 6.1, 6.5, 8, 20, 100):
        jnum, best, jn = numopt(ratio*kT, w, om, 1.0)
        if best[0] <= jn*(1+1e-9):
            wp = 1/(1+np.exp(-best[1][2])); row.append(f"{ratio}:{wp:.3f}")
        else:
            row.append(f"{ratio}:0(noclock)")
    print(f"  w={w}, om={om}: " + "  ".join(row))
    print("     closed-form w'/om: " + "  ".join(f"{r}:{max(0,1-3/(r-3)) if r>6 else 0:.3f}" for r in (4,5.5,5.9,6.1,6.5,8,20,100)))

print("(c) shares at the optimum (kap=1, w=om=1)")
for ratio in (7, 20, 100, 1e4):
    c = ratio*kT; jnum, best, jn = numopt(c, 1.0, 1.0, 1.0)
    lf, lD, u = best[1]; f, D = np.exp(lf), np.exp(lD); wp = 1/(1+np.exp(-u))
    clock = kT*wp**2/D; read = c*f; loss = (1-wp)**2/(3*f**2) + D/f
    print(f"  c/kT={ratio:>7}: clock {clock/jnum:.4f}  reads {read/jnum:.4f}  loss {loss/jnum:.4f}  (J*={jnum:.5g})")

print("(d) ring clock Monte Carlo (Markov jump, N states per cycle)")
def ring_kappa(kp, km): return (kp+km)*np.log(kp/km)/(2*(kp-km))
for (kp, km) in [(2.0, 1.0), (1.1, 1.0), (1.01, 1.0), (10.0, 0.1)]:
    print(f"  k+/k- = {kp/km:7.3f}: kappa = {ring_kappa(kp, km):.5f}")
# simulate phase error between reads; clock rates chosen to give mean frequency om' and diffusion D
N = 50; dphi = 2*np.pi/N; om = 1.0; T = 2.0
kp, km = 30.0, 25.0
omp = (kp-km)*dphi; D = (kp+km)*dphi**2/2
nrun = 4000; ts = np.linspace(0, T, 201)
err2 = np.zeros_like(ts)
for r in range(nrun):
    # Gillespie up to T, record clock advance at grid times
    t = 0.0; x = 0; k = 0; tot = kp+km
    while k < len(ts):
        dt = rng.exponential(1/tot)
        while k < len(ts) and ts[k] < t+dt:
            # estimate: theta_read + clock advance; world advanced om*ts[k]
            err2[k] += (x*dphi - om*ts[k])**2; k += 1
        t += dt; x += 1 if rng.random() < kp/tot else -1
err2 /= nrun
mc = np.trapezoid(err2, ts)/T
formula = (om-omp)**2*T**2/3 + D*T
print(f"  ring N={N}, k+={kp}, k-={km}: om'={omp:.4f}, D={D:.5f}; time-avg sq error MC {mc:.5f} vs formula {formula:.5f} (rel {abs(mc-formula)/formula:.3%})")
print(f"  ring heat rate (kT units) = (k+-k-) ln(k+/k-) = {(kp-km)*np.log(kp/km):.5f} >= TUR floor om'^2/D = {omp**2/D:.5f}")
