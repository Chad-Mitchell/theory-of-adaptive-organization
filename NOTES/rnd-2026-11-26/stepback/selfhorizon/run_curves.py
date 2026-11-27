import subprocess, numpy as np
from concurrent.futures import ThreadPoolExecutor
TM=400
og=sorted(set(int(round(x/2))*2+1 for x in np.geomspace(4003,16001,70)))
ns=list(range(3,4002))+[n for n in og if n>4001]
def run(n): return subprocess.run(["./shdp",str(n),str(TM)],capture_output=True,text=True).stdout
with ThreadPoolExecutor(8) as ex: out=list(ex.map(run,ns[::-1]))
rows={}
for o in out:
  for l in o.strip().split("\n"):
    p=l.split(); rows[(int(p[0]),p[1])]=list(map(float,p[2:]))
N=sorted(set(k[0] for k in rows))
np.savez("curves_sh.npz",n=np.array(N),m3h=np.array([rows[(n,'M3h')] for n in N]),mix=np.array([rows[(n,'MIX')] for n in N]))
print(len(N),N[-1])
