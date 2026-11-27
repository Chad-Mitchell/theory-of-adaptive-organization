# SR-b4 (A): the lcm construction. n = 2(1 + m*lcm(1..H)). Claim (Prop. SR-b4, §9): J(n,T) < disk(T) for every 2<=T<=H.
# (A1) exact DP (dp4) for H=2..12, m=1,2; (A2) the explicit equal-step path cost in 50-digit arithmetic for H up to 80.
import math, subprocess, mpmath as mp
mp.mp.dps=50
def disk(T): return T*math.sin(math.pi/(2*T))**2
print("(A1) exact DP")
for H in range(2,13):
  for m in (1,2):
    L=math.lcm(*range(1,H+1)); n=2*(1+m*L)
    J=list(map(float,subprocess.run(["./dp4",str(n),str(H)],capture_output=True,text=True).stdout.split()[1:]))
    marg=[(disk(T)-J[T-1])/disk(T) for T in range(2,H+1)]
    print(f"H={H:2d} m={m} n={n:6d}: J(T=1)={J[0]:.15f}; all T in 2..H cheaper than disk: {all(x>0 for x in marg)}; min rel margin {min(marg):.3e} (2/n={2/n:.3e})")
print("(A2) explicit path, 50 digits: cost_T = T*sin^2(pi k/n)/cos^2(pi/n)^[k-S odd], k=(S-1)/T")
worst=None
for H in list(range(2,41))+[50,60,70,80]:
  L=math.lcm(*range(1,H+1)); n=2*(1+L); S=n//2; ok=True; mn=mp.inf
  for T in range(2,H+1):
    k=(S-1)//T; assert k*T==S-1
    d=mp.sin(mp.pi*k/n)
    if (k-S)%2: d/=mp.cos(mp.pi/n)
    c=T*d**2; dk=T*mp.sin(mp.pi/(2*T))**2
    r=(dk-c)/dk; mn=min(mn,r); ok&= (c<dk)
  if H<=12 or H%10==0: print(f"H={H} n=2(1+lcm)~{mp.nstr(mp.mpf(n),6)}: path cheaper at all T in 2..H: {ok}; min rel margin {mp.nstr(mn,5)}; n*margin={mp.nstr(mn*n,5)}")
  assert ok
print("all asserts passed")
