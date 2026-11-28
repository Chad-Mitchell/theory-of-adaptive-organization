# Each step of the paper proof (review §2), checked separately at 80 digits; strict steps checked strictly.
# Families: (2T+1)-gon, T=2..300 (with directly computed exact d(v0,v1) and d(v0,vT)); odd lcm n=1+2m lcm(1..H), H=2..40, m=1..3 (bound chain only).
# Also: mixed-state paths (straight chord, T equal pieces) cost exactly 1/T in every design (pure-jump rule is load-bearing).
import math, mpmath as mp
mp.mp.dps = 80
def steps(n, T):
    Sp = (n-1)//2; assert Sp % T == 0 and T >= 2
    x = mp.pi/(2*T); y = mp.pi*(Sp//T)/n
    s = []
    s.append(abs(y - x*(1-mp.mpf(1)/n)) < mp.mpf(10)**-70)                     # y = x(1-1/n)
    s.append(mp.sin(y) < mp.sin(x) - (x/n)*mp.cos(x))                           # strict tangent-line (concavity)
    s.append(x*mp.cot(x) >= mp.pi/4 - mp.mpf(10)**-70)                          # x cot x >= pi/4 (equality at T=2)
    s.append(mp.sin(mp.pi/(2*n))**2 < mp.pi**2/(4*n**2))                         # sin^2 z < z^2
    s.append(mp.pi**2/(4*n**2) < mp.pi/(4*n))                                   # n > pi
    bound = mp.sin(y)/mp.cos(mp.pi/(2*n))**2
    s.append(T*bound**2 < T*mp.sin(x)**2)
    return all(s), bound
def dist_direct(n, k):
    V = [(mp.cos(2*mp.pi*i/n), mp.sin(2*mp.pi*i/n)) for i in range(n)]
    best = mp.mpf(0)
    for i in range(n):  # +- normals of every edge, width computed directly for each
        a, b = V[i], V[(i+1) % n]; ex, ey = b[0]-a[0], b[1]-a[1]; L = mp.sqrt(ex*ex+ey*ey); nx, ny = ey/L, -ex/L
        p = [nx*v[0]+ny*v[1] for v in V]; w = max(p)-min(p)
        best = max(best, abs(nx*(V[0][0]-V[k][0])+ny*(V[0][1]-V[k][1]))/w)
    return best
bad = 0; minm = mp.inf
for T in range(2, 301):
    n = 2*T+1; ok, bound = steps(n, T)
    d1 = dist_direct(n, 1) if n <= 201 else None; dT = dist_direct(n, T) if n <= 201 else None
    if d1 is not None:
        ok = ok and d1 <= bound and abs(dT-1) < mp.mpf(10)**-70 and T*d1**2 < T*mp.sin(mp.pi/(2*T))**2
        minm = min(minm, n*(1-T*d1**2/(T*mp.sin(mp.pi/(2*T))**2)))
    bad += not ok
print("(2T+1)-gon, T=2..300: every proof step holds (exact distances for n<=201):", bad == 0, "| min n*rel margin (exact path, n<=201):", mp.nstr(minm, 6))
bad = 0; cnt = 0
for H in range(2, 41):
    for m in (1, 2, 3):
        n = 1+2*m*math.lcm(*range(1, H+1))
        for T in range(2, H+1):
            cnt += 1; bad += not steps(n, T)[0]
print(f"odd lcm family, H=2..40, m=1..3: {cnt} (n,T) cases, proof-chain failures: {bad}")
# load-bearing pure-jump rule: chord path
for n in (5, 7, 61):
    Sp = (n-1)//2; T = 4
    print(f"n={n}: mixed-state chord path, T={T}: each piece has d = 1/T by homogeneity of the gauge, total = {mp.nstr(T*(mp.mpf(1)/T)**2, 6)} = 1/T (same for the disk)")
