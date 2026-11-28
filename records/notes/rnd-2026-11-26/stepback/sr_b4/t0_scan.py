# SR-b4 (C): for generic even n, T0(n) = last T such that J(n,T') < disk(T') for every 2<=T'<=T (exact DP, dp4). OBSERVED.
import math, subprocess, numpy as np
from concurrent.futures import ThreadPoolExecutor
def disk(T): return T*math.sin(math.pi/(2*T))**2
ns=sorted(set(list(range(6,402,2))+[int(round(x/2))*2 for x in np.geomspace(402,40000,120)]))
def run(n):
  Tm=min(n//2+2,600)
  J=list(map(float,subprocess.run(["./dp4",str(n),str(Tm)],capture_output=True,text=True).stdout.split()[1:]))
  T0=1
  for T in range(2,Tm+1):
    if J[T-1]<disk(T)*(1-1e-13): T0=T
    else: break
  nwin=sum(J[T-1]<disk(T)*(1-1e-13) for T in range(2,Tm+1))
  return n,T0,nwin,Tm
with ThreadPoolExecutor(8) as ex: res=list(ex.map(run,ns))
print("n  T0(n)  T0/sqrt(n)  wins_in_2..Tm  Tm")
for n,T0,nw,Tm in res:
  if n<=60 or n%4==2 and (n<=402 and n%40==2) or n>402: print(n,T0,f"{T0/math.sqrt(n):.3f}",nw,Tm)
a=np.array([(n,T0) for n,T0,_,_ in res if n>=1000])
print("n>=1000: T0/sqrt(n) min %.3f median %.3f max %.3f"%(np.min(a[:,1]/np.sqrt(a[:,0])),np.median(a[:,1]/np.sqrt(a[:,0])),np.max(a[:,1]/np.sqrt(a[:,0]))))
for r in (0,2):
  b=np.array([(n,T0) for n,T0,_,_ in res if n>=1000 and n%4==r])
  print(f"n=={r} mod 4, n>=1000: T0/sqrt(n) min {np.min(b[:,1]/np.sqrt(b[:,0])):.3f} max {np.max(b[:,1]/np.sqrt(b[:,0])):.3f}; count {len(b)}")
