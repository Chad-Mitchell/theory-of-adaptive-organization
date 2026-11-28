# Independent R_H (log-uniform average of rho=J/J*) for H=2..8 and the per-H selection (P); J* = min over n=3..600 and the disk.
import math, numpy as np
from rv_core import *
TM=8; NS=range(3,601)
J={n:J_fwd(n,TM) for n in NS}
T=np.arange(1,TM+1); dk=np.array([disk(t) for t in T])
Js=np.minimum(np.min(np.array(list(J.values())),0),dk)
print("J*(T), T=1..8:",np.round(Js,6).tolist()); print("argmin n:",[min(NS,key=lambda n:J[n][t]) for t in range(TM)])
print("T*J*:",np.round(T*Js,4).tolist(), " disk:",np.round(dk,6).tolist())
for H in range(2,TM+1):
    L=(1/T[:H]).sum(); w=1/(T[:H]*Js[:H])
    R={n:(J[n][:H]*w).sum()/L for n in NS}; Rd=(dk[:H]*w).sum()/L
    nb=min(R,key=R.get)
    dom=[n for n in NS if np.all(J[n][1:H]<dk[1:H])]
    print(f"H={H}: R_H(disk)={Rd:.10f} best n={nb} R_H={R[nb]:.10f} margin={Rd-R[nb]:+.4e}  #n<=600 dominating disk on 2..H: {len(dom)} (smallest {dom[:4]})")
# by hand H=2: J*(1)=1 (any design must make a d=1 jump), J*(2)=1/2 (SR-b1(a) floor, hexagon v0->v1->v2 = 1/4+1/4)
print("by hand H=2: R_2(disk) = (1/1*1/1 + (1/2)*(1/(1/2)))/(3/2) = 4/3 =",4/3)
