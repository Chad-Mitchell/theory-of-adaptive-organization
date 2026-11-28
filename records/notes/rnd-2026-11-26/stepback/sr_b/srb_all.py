# SR-b: every n-gon 3..401 (OBSERVED). J(n,T) for T up to saturation; saved to srb_all.json.
import json, numpy as np, time
from srb_big import Jcurve
out={}
t=time.time()
for n in range(3,402):
    out[n]=Jcurve(n).tolist()
    if n%50==0: print(n, f"{time.time()-t:.0f}s", flush=True)
json.dump({str(k):v for k,v in out.items()},open("srb_all.json","w"))
print("done")
