# Reviewer curves: J(n,T), T<=400, every n in 3..1000 (both parities) plus spot n near the claimed H=200,300,400 winners.
import subprocess, numpy as np
from concurrent.futures import ThreadPoolExecutor
ns=list(range(3,1001))+list(range(1100,1141,2))+list(range(2290,2321,2))+list(range(3820,3861,2))+[1121,2305,3841]
def run(n): return subprocess.run(["./rv_dp",str(n),"400"],capture_output=True,text=True).stdout
with ThreadPoolExecutor(8) as ex: out=list(ex.map(run,ns[::-1]))
A=np.array([list(map(float,l.split())) for l in out]); A=A[np.argsort(A[:,0])]
np.save("rv_curves.npy",A); print(A.shape)
