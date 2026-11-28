# Curves under the mixed (M3c) rule: even n with antipode target only, n=4..1000; odd n are unchanged (rv_curves.npy).
import subprocess, numpy as np
from concurrent.futures import ThreadPoolExecutor
ns=list(range(4,1001,2))
def run(n): return subprocess.run(["./rv_dp",str(n),"400","a"],capture_output=True,text=True).stdout
with ThreadPoolExecutor(8) as ex: out=list(ex.map(run,ns[::-1]))
A=np.array([list(map(float,l.split())) for l in out]); A=A[np.argsort(A[:,0])]
np.save("rv_curves_antipode.npy",A); print(A.shape)
