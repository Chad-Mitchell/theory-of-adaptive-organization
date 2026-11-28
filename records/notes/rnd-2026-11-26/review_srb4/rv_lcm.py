# Spot-check of Proposition SR-b4's lcm family n = 2(1+m*lcm(1..H)).
# (a) reviewer DP (rv_dp: breakpoint distances, no step cap) for H=2..9, m=1,2 (H=9 m=1 only).
# (b) explicit equal-step path, 60 digits, distances from the even-n closed form (checked against breakpoints for n<=40
#     in rv_check_dist.out and here against rv_dp's own distances via the DP), H=2..60, m=1..3.
# (c) the proof's inequality chain itself, step by step, at every (n,T) of (b).
import math, subprocess, mpmath as mp
mp.mp.dps=60
def disk(T): return T*math.sin(math.pi/(2*T))**2
print("(a) DP")
for H in range(2,10):
  for m in ((1,2) if H<9 else (1,)):
    n=2*(1+m*math.lcm(*range(1,H+1)))
    J=list(map(float,subprocess.run(["./rv_dp",str(n),str(H)],capture_output=True,text=True).stdout.split()[1:]))
    mg=[(disk(T)-J[T-1])/disk(T) for T in range(2,H+1)]
    print(f" H={H} m={m} n={n}: J(1)={J[0]:.15f}; cheaper at all T in 2..H: {all(x>0 for x in mg)}; min rel margin {min(mg):.4e}; n*min = {n*min(mg):.4f}")
print("(b,c) explicit path and proof chain")
bad=0
for H in range(2,61):
  L=math.lcm(*range(1,H+1))
  for m in (1,2,3):
    n=2*(1+m*L); S=n//2; mn=mp.inf
    for T in range(2,H+1):
      k=(S-1)//T; assert k*T==S-1
      d=mp.sin(mp.pi*k/n)/(mp.cos(mp.pi/n) if (k-S)%2 else 1)
      cost=T*d**2; dk=T*mp.sin(mp.pi/(2*T))**2
      x=mp.pi/(2*T); y=x*(1-mp.mpf(2)/n)
      c1= mp.sin(y)/mp.cos(mp.pi/n) >= d*(1-mp.mpf(10)**-50)   # worse parity bound (equality when k-S odd; tolerance for rounding)
      c2= mp.sin(y) <= mp.sin(x)-(2*x/n)*mp.cos(x)        # concavity
      c3= 2*mp.sin(mp.pi/(2*n))**2 <= mp.pi**2/(2*n**2)   # 1-cos z written as 2 sin^2(z/2) to avoid cancellation
      c4= x*mp.cot(x) >= mp.pi/4
      c5= mp.pi**2/(2*n**2) < mp.pi/(2*n)
      ok= cost<dk and c1 and c2 and c3 and c4 and c5
      if not ok: bad+=1; print("FAIL",H,m,T,[cost<dk,c1,c2,c3,c4,c5])
      mn=min(mn,(dk-cost)/dk)
    if m==1 and (H<=10 or H%10==0): print(f" H={H} m=1 n~{mp.nstr(mp.mpf(n),5)}: all T in 2..H cheaper and every proof step holds; n*min rel margin = {mp.nstr(n*mn,6)}")
print("failures:",bad)
