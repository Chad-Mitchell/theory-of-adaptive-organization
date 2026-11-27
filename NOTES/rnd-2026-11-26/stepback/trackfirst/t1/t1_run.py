import numpy as np, json, sys, time
from t1_core import *
r=(0.05,0.2,0.8); out=open('t1_run.jsonl','a'); cache={}
def It(rk,f,G):
    key=(rk,f,G)
    if key not in cache: cache[key]=Itab(rk,f,G)
    return cache[key]
def rec(d): out.write(json.dumps(d)+'\n'); out.flush()
t0=time.time()
for f in (1,4):
  for G in (0.05,0.2):
    I=[It(rk,f,G) for rk in r]
    for R in (0.5,1,2,5):
      # S1
      c=[1,1,1]; Bs=[Bstar_single(I[k],c[k],G) for k in range(3)]
      N,B,stat,ok=run_dyn(I,c,G,R,0.0)
      rec(dict(arm='S1',f=f,G=G,R=R,Bstar=Bs,B=B.tolist(),Ntot=N.sum(1).tolist(),modes=[modes(N[k]) for k in range(3)],stat=stat,ok=ok))
      for s in (0.01,0.1):
        for arm,c in (('S2',[1,1,1]),('S3',[0.5,1,2])):
          for scale in (1,2):
            Rr,ss=R*scale,s/scale
            N,B,stat,ok=run_dyn(I,c,G,Rr,ss)
            Be,ne,Ne=ess(I,c,G,Rr,ss)
            rec(dict(arm=arm,scale=scale,f=f,G=G,R=Rr,s=ss,c=c,B=float(B[0]),Ntot=N.sum(1).tolist(),modes=[modes(N[k]) for k in range(3)],
                     dist=[N[k].tolist() for k in range(3)],stat=stat,ok=ok,ess_B=Be,ess_n=ne,ess_N=Ne))
      print(f"done f={f} G={G} R={R} t={time.time()-t0:.0f}s",flush=True)
# Arm L
I2=Itab(0.2,1,0.05); 
for G in (0.05,0.2):
  I2=Itab(0.2,1,G)
  for D in (0,0.01,0.1,1,10):
    N,B,stat,ok=run_dyn([I2,I2],[1,1],G,[2,0.5],0.1,pools=[0,1],D=D)
    rec(dict(arm='L',G=G,D=D,B=B.tolist(),Ntot=N.sum(1).tolist(),modes=[modes(N[k]) for k in range(2)],stat=stat,ok=ok))
print('ALL DONE',time.time()-t0,flush=True)
