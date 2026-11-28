import math, sys, random, mpmath as mp
from od_core import *
mp.mp.dps = 50
TOL = mp.mpf(10)**-40
out = []
P = lambda *a: (print(*a), sys.stdout.flush())

P("== (1) distances: gauge (50 digits) vs float LP, and the d=1 target set for each n ==")
maxerr = 0; tsets = {}
for n in range(3, 62):
    row = dist_row_gauge(n)
    for k in range(n):
        maxerr = max(maxerr, abs(float(row[k]) - dist_lp(n, k)))
    tsets[n] = [k for k in range(n) if abs(row[k]-1) < TOL]
P("max |gauge - LP| over n=3..61, all k:", f"{maxerr:.2e}")
odd_ok = all(tsets[n] == [(n-1)//2, (n+1)//2] for n in range(3, 62, 2))
P("odd n=3..61: d=1 targets are exactly {(n-1)/2,(n+1)/2}:", odd_ok)
P("even n: antipode n/2 has d=1:", all(n//2 in tsets[n] for n in range(4, 62, 2)),
  "| even n with extra d=1 vertices (any-vertex rule differs from antipode):", [n for n in range(4, 62, 2) if tsets[n] != [n//2]][:8], "...")
P("example target sets: 6:", tsets[6], " 8:", tsets[8], " 7:", tsets[7])

P("\n== (2) disk optimum T*sin^2(pi/2T): numeric lower-bound check over the KKT family and random splits (50 digits) ==")
worst = mp.inf
random.seed(1)
for T in range(2, 61):
    D = disk(T)
    # KKT family for a convex-then-concave f: (T-1) equal steps a and one step pi-(T-1)a
    for s in range(0, 2001):
        a = mp.pi/(T-1)*s/2000
        b = mp.pi-(T-1)*a
        val = (T-1)*mp.sin(a/2)**2 + mp.sin(b/2)**2
        worst = min(worst, val - D)
    for _ in range(200):
        w = [mp.mpf(random.random()) for _ in range(T)]; S = sum(w)
        val = sum(mp.sin(mp.pi*x/S/2)**2 for x in w)
        worst = min(worst, val - D)
P("min over tested splits of (cost - T sin^2(pi/2T)), T=2..60:", mp.nstr(worst, 5), "(>= 0 up to rounding; =0 at equal steps)")

P("\n== (3) odd n = 5..61, every T>=2 dividing (n-1)/2: exact DP (50 digits) under both rules, vs disk ==")
fails = []; rows_cache = {}
nchk = 0; minrel = mp.inf
for n in range(5, 62, 2):
    row = dist_row_gauge(n); rows_cache[n] = row
    Sp = (n-1)//2
    anyv = [k for k in range(n) if abs(row[k]-1) < TOL]
    antip = [n//2]                      # ROUND10 M3c code's target index best[n//2]; for odd n this is (n-1)/2
    for T in range(2, Sp+1):
        if Sp % T: continue
        Ja = dp_exact(row, T, anyv, mp.mpf(0)); Jb = dp_exact(row, T, antip, mp.mpf(0))
        j = Sp//T
        path = T*row[j]**2
        D = disk(T)
        nchk += 1
        rel = (D-Ja)/D; minrel = min(minrel, n*rel)
        if not (Ja < D and Jb < D and abs(Ja-Jb) < TOL and Ja <= path + TOL): fails.append((n, T, Ja, Jb, D))
        if n <= 15 or n in (31, 61):
            P(f"n={n:2d} T={T:2d}: J_any={mp.nstr(Ja,12)} J_antipode={mp.nstr(Jb,12)} equal-step path={mp.nstr(path,12)} disk={mp.nstr(D,12)} rel margin={mp.nstr(rel,6)}")
P(f"(n,T) pairs checked: {nchk}; failures: {len(fails)}; min n*rel margin: {mp.nstr(minrel,6)}")

P("\n== (4) brute force (all vertex sequences) vs DP, small n ==")
bad = 0; cnt = 0
for n in (5, 7, 9, 11, 13):
    row = [float(x) for x in rows_cache[n]]
    tg = [(n-1)//2, (n+1)//2]
    for T in range(1, 6 if n <= 9 else 5):
        b = brute(row, T, tg); d = dp_np(row, T, tg); cnt += 1
        if abs(b-d) > 1e-12: bad += 1; P("mismatch", n, T, b, d)
P(f"brute vs DP: {cnt} cases, mismatches {bad}")

P("\n== (5) beyond the claim (OBSERVED): odd n=5..61, ALL T in 2..30 (not only divisors): where J(n,T) < disk ==")
for n in (9, 15, 21, 31, 45, 61):
    row = rows_cache[n]; tg = [(n-1)//2, (n+1)//2]
    wins = [T for T in range(2, 31) if dp_np(row, T, tg) < float(disk(T)) - 1e-12]
    P(f"n={n}: T with a strict win: {wins}")
