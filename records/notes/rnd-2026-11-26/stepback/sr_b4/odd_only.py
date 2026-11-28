# SR-b4 (E): odd polygons only (their target is the same under M3c's and M3h's rules). n = 3..401 (sr_b/srb_all.json, LP-based).
import json, math, numpy as np
TM=400; odd=json.load(open("../sr_b/srb_all.json")); on=[];Jo=[]
for k,v in odd.items():
  if int(k)%2: v=list(v)+[v[-1]]*(TM-len(v)); on.append(int(k)); Jo.append(v[:TM])
on=np.array(on); Jo=np.array(Jo); A=np.load("curves_even.npy"); Je=A[:,1:]
T=np.arange(1,TM+1); disk=T*np.sin(np.pi/(2*T))**2
Jstar=np.minimum(np.minimum(Je.min(0),Jo.min(0)),disk)
for H in (2,3,5,10,20,50,100,150,200):
  w=1/(T[:H]*Jstar[:H]); L=(1/T[:H]).sum(); p=(Jo[:,:H]*w).sum(1)/L; dk=(disk[:H]*w).sum()/L; j=int(np.argmin(p))
  dom=[int(n) for n,J in zip(on,Jo) if np.all(J[1:H]<disk[1:H])]
  print(f"H={H:3d} disk {dk:.8f} best odd n={on[j]} {p[j]:.8f} margin {dk-p[j]:+.3e} interior={on[j]<401} | odd n<=401 dominating disk on 2..H: {dom[:3]}{'...' if len(dom)>3 else ''} ({len(dom)})")
