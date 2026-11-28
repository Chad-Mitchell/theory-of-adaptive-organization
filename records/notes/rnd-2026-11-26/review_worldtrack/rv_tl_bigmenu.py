from rv_tl2 import disk_exact, PH
from rv_tl import d0_row, poly_move, disk_move
import numpy as np, json, sys
al=np.linspace(0,1,401); out=[]
for T in [8,20]:
  for N in [720,1440]:
    DM=disk_move(PH,T); Lp=(1+np.cos(PH))/2; Lr=1-np.sin(PH/2)
    polys=[]
    for n in range(3,N+1):
        d=d0_row(n); polys.append((n,poly_move(n,T,d),(1+np.cos(2*np.pi*np.arange(n)/n))/2,1-d))
    for lam in [30,1000]:
        cd=np.array([disk_exact(a,lam,T,DM,Lp,Lr) for a in al]); cp=np.full(len(al),np.inf); bn=np.zeros(len(al),int)
        for n,m,lp,lr in polys:
            v=(m[None,:]+lam*(al[:,None]*lp[None,:]+(1-al[:,None])*lr[None,:])).min(1); b=v<cp; cp[b]=v[b]; bn[b]=n
        D=cd-cp; W=D>1e-12; ch=np.flatnonzero(W[1:]!=W[:-1])
        r=dict(T=T,N=N,lam=lam,W0=bool(W[0]),crossings=len(ch),cross_at=[float(al[c]) for c in ch],n_at=[int(bn[c]) for c in ch],D1=float(D[-1]))
        out.append(r); print(r,flush=True)
json.dump(out,open('rv_tl_bigmenu.json','w'))
