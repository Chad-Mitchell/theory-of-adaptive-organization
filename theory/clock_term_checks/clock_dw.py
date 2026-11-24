"""Scope check for C1: with world phase diffusion Dw > 0 the clock onset is no longer stake-free.
Onset condition from the closed form: the interior clock fraction w'/om = 1 - 3 f^{3/2} sqrt(kap kT / w)/om must be >= 0 at the optimal f.
We find the onset ratio c*/(kap kT) numerically for several stakes."""
import numpy as np
from scipy.optimize import minimize_scalar, brentq
kT = kap = 1.0; om = 1.0
def Jf(f, c, w, Dw, clock):
    if clock:
        s = np.sqrt(kap*kT*w/f); wp = om - 3*f**2*s/w
        if wp <= 0: return np.inf
        return 2*om*s - 3*f*kap*kT + c*f + w*Dw/f
    return c*f + w*(om**2/(3*f**2) + Dw/f)
def Jstar(c, w, Dw, clock):
    r = minimize_scalar(lambda lf: Jf(np.exp(lf), c, w, Dw, clock), bounds=(-12, 12), method='bounded', options=dict(xatol=1e-12))
    return r.fun
for Dw in (0.0, 0.01, 0.1, 1.0):
    out = []
    for w in (0.1, 1, 10, 100):
        g = lambda c: Jstar(c, w, Dw, True) - Jstar(c, w, Dw, False) if np.isfinite(Jstar(c, w, Dw, True)) else 1.0
        cs = np.exp(np.linspace(np.log(3.2), np.log(1e4), 400)); vals = [g(c) for c in cs]
        k = next((i for i, v in enumerate(vals) if v < -1e-12), None)
        out.append(f"w={w}: c*/kT~{cs[k]:.3g}" if k is not None else f"w={w}: none<1e4")
    print(f"Dw={Dw}: " + "   ".join(out))
