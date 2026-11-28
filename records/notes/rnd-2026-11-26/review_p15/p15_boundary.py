"""Check 3: the class boundary. SR-b3/SR-b4 score an OPERATIONAL target (any vertex at
d = 1 in that design), which is a design-dependent function of angle, so P15 does not
apply. Reproduce the polygon wins and show where the d=1 targets sit in angle."""
import numpy as np
from p15_core import reg_poly, op_dist_lp
def row(n):
    V, a = reg_poly(n); return np.array([0.0]+[op_dist_lp(V, V[0], V[k]) for k in range(1, n)]), a
def reach_cost(n, T, targets):
    d, a = row(n); D = d[(np.arange(n)[None, :]-np.arange(n)[:, None]) % n]
    V = np.where(np.isin(np.arange(n), targets), 0.0, np.inf)
    for t in range(T): V = np.min(D**2 + V[None, :], axis=1)
    return V[0]
print("design | angles (deg) of d=1 vertices from v0 | reach cost T=2,3,4 (M3h) | disk T*sin^2(pi/2T)")
for n in [3, 4, 5, 6, 7, 8, 9, 10, 12]:
    d, a = row(n); tg = [k for k in range(n) if abs(d[k]-1) < 1e-9]
    print(n, [round(np.degrees(a[k]), 2) for k in tg], [round(reach_cost(n, T, tg), 4) for T in (2, 3, 4)],
          [round(T*np.sin(np.pi/(2*T))**2, 4) for T in (2, 3, 4)])
print("disk: only d=1 state is the antipode (180 deg)")
print()
print("Same polygons under the ANGLE-ONLY target 'be at 180 deg' (P15's class): cost (inf = unreachable)")
for n in [3, 4, 5, 6, 8, 10, 12]:
    tg = [n//2] if n % 2 == 0 else []
    print(n, [reach_cost(n, T, tg) if tg else np.inf for T in (2, 3, 4)])
