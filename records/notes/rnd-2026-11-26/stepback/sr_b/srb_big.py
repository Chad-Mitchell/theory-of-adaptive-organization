# SR-b: larger polygons (OBSERVED). Same J as srb_J.py; Tmax = sat. Mixture vs disk at q near 1.
import math, json, numpy as np, time
from srb_J import dists
disk=lambda T: T*math.sin(math.pi/(2*T))**2
def Jcurve(n):
    d=dists(n); d2=d**2; targets=np.where(d>1-1e-9)[0]
    best=np.full(n,np.inf); best[0]=0; J=[]
    k=np.arange(n)
    while True:
        # min-plus circulant step: nb[j]=min_i best[i]+d2[(j-i)%n]
        nb=np.full(n,np.inf)
        fin=np.where(np.isfinite(best))[0]
        for i in fin: nb=np.minimum(nb,best[i]+np.roll(d2,i))
        best=np.minimum(best,nb); J.append(best[targets].min())
        if len(J)>3 and J[-1]==J[-2]==J[-3] and len(J)>n//2+2: break
    return np.array(J)
if __name__=="__main__":
  out={}
  for n in [301,401,601,801,1001,300,400,600,800,1000]:
      t=time.time(); J=Jcurve(n); out[n]=J.tolist()
      win=sum(J[T-1]<disk(T)-1e-12 for T in range(1,len(J)+1))
      print(f"n={n}: sat~{len(J)-3} J(inf)={J[-1]:.6f} wins {win} of T=1..{len(J)}  ({time.time()-t:.0f}s)",flush=True)
  json.dump({str(k):v for k,v in out.items()},open("srb_big.json","w"))
