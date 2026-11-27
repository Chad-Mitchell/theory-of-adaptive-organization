# T0(n) = last T with J(n,T') < disk(T') for all 2<=T'<=T. Even n (claim: T0/sqrt(n) in 1.995..2.161 for n>=1000) and,
# new here, odd n (relevant to the mixed target rule: odd targets are the same under both rules).
import math, subprocess
def disk(T): return T*math.sin(math.pi/(2*T))**2
for n in (1000,1002,2000,2002,4000,4002,10000,10002, 101,201,401,801,1601,3201,6401):
  Tm=int(3*math.sqrt(n))+5
  J=list(map(float,subprocess.run(["./rv_dp",str(n),str(Tm)],capture_output=True,text=True).stdout.split()[1:]))
  T0=1
  for T in range(2,Tm+1):
    if J[T-1]<disk(T)*(1-1e-13): T0=T
    else: break
  print(f"n={n:6d} ({'even' if n%2==0 else 'odd '}) T0={T0:4d} T0/sqrt(n)={T0/math.sqrt(n):.3f}  (Tmax {Tm})")
