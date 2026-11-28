import numpy as np, sys
sys.path.insert(0,"../../review_srb4"); import rv_core as rc
d=np.load("curves_sh.npz"); N=list(d['n']); M=d['m3h']; X=d['mix']
E=np.load("../sr_b4/curves_even.npy"); En=E[:,0].astype(int)
mx=0
for i,n in enumerate(En):
  if n in N and n<=4000: mx=max(mx,np.max(np.abs(E[i,1:]-M[N.index(n)])))
print("max |diff| vs sr_b4 curves_even (M3h, even n<=4000):",mx)
mx2=0
for n in [5,6,7,8,9,10,11,12,13,14,15,17,21,22,25,30,31]:
  jc=rc.J_circ(n,12); mx2=max(mx2,np.max(np.abs(jc-M[N.index(n)][:12])))
print("max |diff| vs rv_core.J_circ (no cap, circular), n<=31, T<=12:",mx2)
# antipode-rule (mixed) even: check J>=disk (PIM bound) numerically
T=np.arange(1,401); disk=T*np.sin(np.pi/(2*T))**2
viol=min(np.min(X[i]-disk) for i,n in enumerate(N) if n%2==0)
print("min over even n of J_mix - disk:",viol)
