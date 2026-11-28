"""ONSET-NOISY-READS check 2 (own code). Pooling onset with noisy periodic reads, member units q_u = w = c = 1.
Flat member tracks q = 1+rho; pooled: member tracks q = 1, level tracks shared drift rho at weight N.
Onset: N [phi(1,1+rho) - phi(1,1)] = phi(N, rho), phi(w,q) = min_T 1/T + w q T^(a-1) f(s2/(q T^(a-1))).
f from fz.py (conditioning, M=2000) on a log grid, joined to the closed asymptote g z^b beyond z_hi.
Derived (report section 2): N* rho = X(s2/rho) to O(rho); X(0) = a^(a/(a-1)); X(s) ~ C_inf s, C_inf closed form."""
import numpy as np, math, json, sys
from scipy import optimize, interpolate
from fz import f, g

ZHI = {1.5: 1e3, 2.0: 1e4, 2.5: 1e4}
class F:
    def __init__(s, a):
        s.a = a; s.H = (a-1)/2; s.b = 1-1/a; s.g = g(a); s.f0 = f(s.H, 0.0, 2000); s.zhi = ZHI[a]
        zz = np.logspace(-6, math.log10(s.zhi), 241)
        r = [f(s.H, z, 2000)/(s.f0 + s.g*z**s.b) for z in zz]
        s.sp = interpolate.CubicSpline(np.log(zz), r)
        s.rhi = r[-1]
    def __call__(s, z):
        if z <= 1e-6: return s.f0 + s.g*z**s.b
        if z >= s.zhi:  # asymptote g z^b, joined continuously (relative mismatch at join stated in output)
            return s.g*z**s.b*(1 + (s.f(s.zhi)/(s.g*s.zhi**s.b) - 1)*(s.zhi/z)**s.b)
        return (s.f0 + s.g*z**s.b)*float(s.sp(math.log(z)))
    def f(s, z): return (s.f0 + s.g*z**s.b)*float(s.sp(math.log(z)))

def phi(Fa, w, q, s2):
    a = Fa.a
    obj = lambda lT: math.exp(-lT) + w*q*math.exp((a-1)*lT)*Fa(s2/(q*math.exp((a-1)*lT)))
    return optimize.minimize_scalar(obj, bounds=(-60, 60), method='bounded', options={'xatol': 1e-10}).fun

def onset(Fa, rho, s2):
    flat = phi(Fa, 1.0, 1.0+rho, s2) - phi(Fa, 1.0, 1.0, s2)
    G = lambda lN: math.exp(lN)*flat - phi(Fa, math.exp(lN), rho, s2)
    return math.exp(optimize.brentq(G, math.log(1e-3), math.log(1e14), xtol=1e-12))

def closed(a, f0, gg):
    D0 = (a-1)**(1/a-1)*f0**(1/a)
    X0 = a**(a/(a-1))
    Cinf = ((2*a-1)/((a-1)*D0))**((2*a-1)/(a-1))*(gg*(a-1)/a)**(a/(a-1))
    return X0, Cinf, D0

if __name__ == "__main__":
    res = {}
    for a in (1.5, 2.0, 2.5):
        Fa = F(a); X0, Ci, D0 = closed(a, Fa.f0, Fa.g)
        print(f"\n== alpha={a}: f0={Fa.f0:.6f} g={Fa.g:.6f} D0={D0:.6f} X0={X0:.6f} C_inf={Ci:.4f} "
              f"rho_c/s2 = C_inf/X0 = {Ci/X0:.4f}  (join mismatch at z_hi {Fa.rhi:.5f})", flush=True)
        # (A) exact reads: N* rho -> X0
        Ne = [onset(Fa, r, 0.0)*r for r in (1e-2, 1e-3, 1e-4)]
        print("  exact reads N*rho at rho=1e-2,1e-3,1e-4:", [round(v, 5) for v in Ne], flush=True)
        # (B) collapse: N* rho vs s = s2/rho for three noise levels
        rows = []
        for s2 in (1e-4, 1e-3, 1e-2):
            for k in range(4, 21):
                rho = 10**(-k/4)
                if rho > 0.1 or s2/rho > 1e4: continue
                N = onset(Fa, rho, s2); rows.append((s2, rho, s2/rho, N, N*rho))
        res[str(a)] = {"f0": Fa.f0, "g": Fa.g, "D0": D0, "X0": X0, "Cinf": Ci, "rhoc_over_s2": Ci/X0,
                       "exactNrho": Ne, "rows": rows}
        print("   s2       rho        s=s2/rho   N*rho     X0+Cinf*s   ratio  N*rho/(Cinf s)")
        for s2, rho, s, N, x in rows:
            print(f"  {s2:<8g} {rho:<10.4g} {s:<10.4g} {x:<9.4f} {X0+Ci*s:<11.4f} {x/(X0+Ci*s):.4f} {x/(Ci*s):.4f}", flush=True)
    json.dump(res, open("onset.json", "w"), indent=1)
