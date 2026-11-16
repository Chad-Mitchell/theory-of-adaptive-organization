import math, time, sys
import sys; sys.path.insert(0, "..")
from gridengine import *
N=1.0; D=0.01
for name,(lam,mu) in {"A":(0.01,2.0),"B":(0.02,math.sqrt(2))}.items():
    p=(1-math.exp(-2*lam*D))/2; g=2*mu*D/N
    for h in (0.04,0.02):
        t=time.time(); r=analyse(bayes_f(p), g, lam, mu, N, D, 16.0, h); print(name,"bayes h",h,r, round(time.time()-t,1), flush=True)
    pole,K=kalman_pole(lam,mu,N,D); a=pole
    s=math.sqrt(N/D); sn=s/math.sqrt(1-a*a); B=mu/(1-a)
    for h in (s/8, s/16):
        t=time.time(); r=analyse(linear_f(a),1.0,lam,mu,N,D,B+7*sn,h); print(name,"kalman h",round(h,3),r, round(time.time()-t,1), flush=True)
