# SR-b4 (D) data: exact J(n,T), T=1..400, for every even n in 4..4000 and a ~2% grid of even n in 4002..64000 (both residues mod 4).
import subprocess, numpy as np
from concurrent.futures import ThreadPoolExecutor
TM=400
g=set()
for x in np.geomspace(4002,64000,140):
  m=int(round(x/4))*4; g.add(m); g.add(m+2)
ns=list(range(4,4001,2))+sorted(g)
def run(n): return subprocess.run(["./dp4",str(n),str(TM)],capture_output=True,text=True).stdout
with ThreadPoolExecutor(8) as ex: out=list(ex.map(run,ns[::-1]))
A=np.array([list(map(float,l.split())) for l in out]); A=A[np.argsort(A[:,0])]
np.save("curves_even.npy",A); print(A.shape)
