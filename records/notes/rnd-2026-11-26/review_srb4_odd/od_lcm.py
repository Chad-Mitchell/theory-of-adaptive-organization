# lcm family n = 1 + 2 m lcm(1..H), H = 2..8, m = 1,2,3: 60-digit explicit equal-step path with directly computed distances,
# and float64 DP (no cap, both target rules) for n <= 3400.
import math, sys, mpmath as mp, numpy as np
from od_core import dp_np
mp.mp.dps = 60
P = lambda *a: (print(*a), sys.stdout.flush())
def dist_fast(n, ks):
    """d(v0,vk) at 60 digits. Width computed directly (max-min over all n vertices) for ONE edge normal; by rotation symmetry
    of the regular n-gon and w(nu)=w(-nu), every +-edge normal has that width. Then max over all 2n +-edge normals."""
    V = [(mp.cos(2*mp.pi*k/n), mp.sin(2*mp.pi*k/n)) for k in range(n)]
    nu0 = (mp.cos(mp.pi/n), mp.sin(mp.pi/n))
    p = [nu0[0]*v[0]+nu0[1]*v[1] for v in V]; w = max(p)-min(p)
    nus = [(mp.cos(2*mp.pi*(i+mp.mpf(1)/2)/n), mp.sin(2*mp.pi*(i+mp.mpf(1)/2)/n)) for i in range(n)]
    res = {}
    for k in ks:
        dx, dy = V[0][0]-V[k][0], V[0][1]-V[k][1]
        res[k] = max(abs(c*dx+s*dy) for (c, s) in nus)/w
    return res, w
def disk(T): return T*mp.sin(mp.pi/(2*T))**2
fails = 0
for H in range(2, 9):
    L = math.lcm(*range(1, H+1))
    for m in (1, 2, 3):
        n = 1+2*m*L; Sp = (n-1)//2
        ks = sorted({Sp//T for T in range(1, H+1)})
        d, w = dist_fast(n, ks)
        assert abs(d[Sp]-1) < mp.mpf(10)**-50
        assert abs(w-(1+mp.cos(mp.pi/n))) < mp.mpf(10)**-50
        margins = []
        for T in range(2, H+1):
            path = T*d[Sp//T]**2; D = disk(T)
            if not path < D: fails += 1
            margins.append((D-path)/D)
        line = f"H={H} m={m} n={n}: 60-digit equal-step path < disk at every T in 2..H: {all(x>0 for x in margins)}; min rel margin {mp.nstr(min(margins),8)}; n*min margin {mp.nstr(n*min(margins),6)}"
        if n <= 3400:
            ang = 2*np.pi*np.arange(n)/n; V = np.stack([np.cos(ang), np.sin(ang)], 1)
            a2 = 2*np.pi*(np.arange(n)+.5)/n; N = np.stack([np.cos(a2), np.sin(a2)], 1)
            row = np.abs((V[0]-V) @ N.T).max(1)/float(w)
            tg = [k for k in range(n) if row[k] > 1-1e-12]
            assert tg == [Sp, Sp+1], tg
            dpm = []
            for T in range(1, H+1):
                J = dp_np(list(row), T, tg); J2 = dp_np(list(row), T, [Sp])
                assert abs(J-J2) < 1e-14
                if T == 1: assert abs(J-1) < 1e-12
                else:
                    dpm.append((float(disk(T))-J)/float(disk(T)))
                    assert abs(J-float(T*d[Sp//T]**2)) < 1e-12, (n, T, J)
            line += f" | float DP (both rules, no cap): win at all T: {all(x>0 for x in dpm)}; DP optimum = equal-step path"
        P(line)
P("failures:", fails)
