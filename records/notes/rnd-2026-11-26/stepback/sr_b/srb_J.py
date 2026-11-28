# SR-b: J(n,T) beyond the design horizon, and horizon mixtures. OBSERVED numerics. Same cost as ROUND10 §14 (M3h):
# min over T-tick vertex paths (staying put allowed) from vertex 0 to a perfectly distinguishable vertex of sum d^2,
# d = operational (all-effects) distance in the regular n-gon. Disk: T sin^2(pi/2T) (ROUND10 §14).
import math, sys, json, numpy as np
from scipy.optimize import linprog
def dists(n):
    V=np.array([[1,math.cos(2*math.pi*k/n),math.sin(2*math.pi*k/n)] for k in range(n)])
    out=[0.0]
    for j in range(1,n):
        r=linprog(-(V[0]-V[j]),A_ub=np.vstack([V,-V]),b_ub=np.concatenate([np.ones(n),np.zeros(n)]),bounds=[(None,None)]*3,method="highs")
        out.append(-r.fun)
    return np.array(out)
def Jcurve(n,Tmax):
    d=dists(n); d2=d**2; targets=np.where(d>1-1e-9)[0]
    best=np.full(n,np.inf); best[0]=0; J=[]
    idx=(np.arange(n)[None,:]-np.arange(n)[:,None])%n   # idx[i,j]=(j-i)%n
    C=d2[idx]
    for t in range(1,Tmax+1):
        best=np.minimum(best,(best[:,None]+C).min(0)); J.append(best[targets].min())
    return np.array(J), d
if __name__=="__main__":
    Tmax=int(sys.argv[1]) if len(sys.argv)>1 else 120
    ns=list(range(3,62))+[81,101,121,161,201]
    res={}
    for n in ns:
        J,d=Jcurve(n,Tmax); res[n]=J.tolist()
        dmin=d[1]
        print(f"n={n:3d} dmin={dmin:.4f} J(1..5)={np.round(J[:5],4).tolist()} J(T={Tmax})={J[-1]:.5f} sat_T={int(np.argmax(J<=J[-1]+1e-12))+1}")
    json.dump({"Tmax":Tmax,"J":{str(k):v for k,v in res.items()}},open("srb_J.json","w"))
