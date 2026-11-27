# SR-b: n = 1400..2400 selected (OBSERVED), saved to srb_huge.json
import json, time
from srb_big import Jcurve
out={}
for n in [1400,1600,1800,2000,2001,2400]:
    t=time.time(); out[n]=Jcurve(n).tolist(); print(n, f"{time.time()-t:.0f}s", flush=True)
    json.dump({str(k):v for k,v in out.items()},open("srb_huge.json","w"))
print("done")
