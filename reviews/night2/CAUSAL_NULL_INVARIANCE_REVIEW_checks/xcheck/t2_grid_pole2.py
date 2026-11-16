import math
import sys; sys.path.insert(0, "..")
from gridengine import analyse, linear_f, kalman_pole
N=1.0; D=0.01; s=10.0
for name,(lam,mu) in {"A":(0.01,2.0),"B":(0.02,math.sqrt(2))}.items():
    pole,K=kalman_pole(lam,mu,N,D); a=1-(1-pole)*2.0
    sn=s/math.sqrt(1-a*a); B=mu/(1-a)
    print(name, analyse(linear_f(a),1.0,lam,mu,N,D,B+7*sn,s/8))
