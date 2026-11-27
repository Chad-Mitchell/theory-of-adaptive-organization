# Round 10b-M, M3g/M3h: odd polygons and the gauge check (same code as run 2026-11-25 ~23:55 EST; output in m_round10b_poly.stdout)
import math, numpy as np
from scipy.optimize import linprog
def poly_dist(n,a,b):
    V=np.array([[1,math.cos(2*math.pi*k/n),math.sin(2*math.pi*k/n)] for k in range(n)])
    r=linprog(-(np.array(a)-np.array(b)),A_ub=np.vstack([V,-V]),b_ub=np.concatenate([np.ones(n),np.zeros(n)]),bounds=[(None,None)]*3,method="highs"); return -r.fun
v=lambda n,k:[1,math.cos(2*math.pi*k/n),math.sin(2*math.pi*k/n)]
if __name__=="__main__":
    for n in [3,5,7,9]:
        print(f"M3g odd {n}-gon (all effects): max op distance between two vertices = {max(poly_dist(n,v(n,0),v(n,j)) for j in range(1,n)):.6f}")
    for n in [6,8,10]:
        print(f"M3g {n}-gon: d(v0,vj)/sin(pi j/n) for j=1..n/2:", [round(poly_dist(n,v(n,0),v(n,j))/math.sin(math.pi*j/n),4) for j in range(1,n//2+1)])
    for T in [3,4,5,8]:
        disk=T*math.sin(math.pi/(2*T))**2; row=[]
        for n in [3,5,7,9,11,15,21,31]:
            d=[poly_dist(n,v(n,0),v(n,j)) for j in range(n)]
            targets=[j for j in range(n) if d[j]>1-1e-9]
            INF=1e9; best=[INF]*n; best[0]=0
            for t in range(T):
                nb=best[:]
                for i in range(n):
                    if best[i]<INF:
                        for j in range(n): nb[j]=min(nb[j],best[i]+d[(j-i)%n]**2)
                best=nb
            row.append(f"{n}:{min(best[j] for j in targets):.4f}")
        print(f"M3h T={T} disk={disk:.4f} | odd n-gon optimum to a perfectly distinguishable vertex: "+" ".join(row))
