"""Check 1 (the only geometric step of P15): d_poly(u,w) >= sin(phi/2) = d_disk for
vertices of regular n-gons (circumradius 1, all effects), plus irregular inscribed
polygons; count exact ties; and show the step fails with restricted effects."""
import numpy as np
from p15_core import *
rng = np.random.default_rng(15)
worst = (9, None); ties = {}; strict_odd_ok = True
for n in range(3, 81):
    V, a = reg_poly(n)
    D = poly_dist_matrix(V)
    t = 0; tot = 0
    for j in range(1, n):
        phi = a[j] - a[0]
        r = D[0, j] - disk_dist(phi)
        worst = min(worst, (r, (n, j)), key=lambda x: x[0])
        tot += 1
        if abs(r) < 1e-10:
            t += 1
            if n % 2: strict_odd_ok = False
    ties[n] = (t, tot)
print("regular n=3..80, all vertex pairs: min (d_poly - d_disk) =", worst)
print("odd n: no exact tie on any nonzero step:", strict_odd_ok)
print("even n tie counts (ties/nonzero steps from v0):",
      {n: ties[n] for n in range(4, 81, 2) if n <= 24})
# closed-form cross-check vs SR_B 8.6 for even n
bad = 0
for n in range(4, 81, 2):
    V, a = reg_poly(n); D = poly_dist_matrix(V)
    for k in range(1, n):
        cf = np.sin(np.pi*k/n) / (np.cos(np.pi/n) if (k - n//2) % 2 else 1)
        bad += abs(cf - D[0, k]) > 1e-9
print("even-n closed form (SR_B 8.6) mismatches:", bad)
# irregular inscribed polygons (random vertex angles on the unit circle, incl. non-centred hulls)
mn = 9
for trial in range(400):
    m = rng.integers(3, 12)
    ang = np.sort(rng.uniform(0, 2*np.pi, m)); V = np.stack([np.cos(ang), np.sin(ang)], 1)
    for i in range(m):
        for j in range(i+1, m):
            mn = min(mn, op_dist_lp(V, V[i], V[j]) - disk_dist(ang[j]-ang[i]))
print("400 random inscribed polygons, all pairs: min (d_K - d_disk) =", mn)
# scope probe: restricted effects (NOT P15's class) -> step can fail
V, a = reg_poly(6)
eff = [(0.5, np.array([0.5, 0.0]))]          # one disk effect only (x-direction) + complement
d_r = op_dist_lp(V, V[0], V[1], effects=eff)
print("hexagon v0->v1 with one effect pair: d=%.4f vs disk sin(pi/6)=%.4f (restricted effects can undercut)" % (d_r, disk_dist(a[1])))
