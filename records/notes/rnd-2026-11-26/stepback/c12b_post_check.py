# Checks for C12B_ORDER.md §9 (OBSERVED; not proofs). kT = 1.
# (1) consistent-world track onset: f(eps)=max(G ln(v/eps), r(v-eps)/eps) + w eps on (0,v]; blind iff w <= max(r,G)/v
import numpy as np
from scipy.optimize import minimize_scalar
print("(1) onset of f(eps) = max(G ln(v/eps), r(v-eps)/eps) + w*eps")
for r,G,v in [(0.4,1.0,2.0),(1.0,0.3,2.0),(0.5,0.5,1.0)]:
    wstar=max(r,G)/v
    for fac in [0.98,1.02]:
        w=fac*wstar
        f=lambda e: max(G*np.log(v/e), r*(v-e)/e)+w*e
        res=minimize_scalar(f,bounds=(1e-6,v),method='bounded',options={'xatol':1e-12})
        print(f"   r={r} G={G} v={v} w/w*={fac}: argmin eps={res.x:.6f} (blind={v}); f(min)-w*v={res.fun-w*v:.2e}")
