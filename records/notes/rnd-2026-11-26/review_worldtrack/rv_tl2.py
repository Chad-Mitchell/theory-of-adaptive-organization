# Step 0 rerun v2: exact disk optimizer (grid + bounded refinement), vectorized polygons, menu 1x and 3x.
from rv_tl import d0_row, poly_move, disk_move
import numpy as np, json, sys
from scipy.optimize import minimize_scalar
PH=np.linspace(0,np.pi,20001)
def disk_exact(a,lam,T,DM,Lp,Lr):
    v=DM+lam*(a*Lp+(1-a)*Lr); i=int(v.argmin()); best=v[i]
    f=lambda p: float(disk_move(np.array([p]),T)[0]+lam*(a*(1+np.cos(p))/2+(1-a)*(1-np.sin(p/2))))
    r=minimize_scalar(f,bounds=(PH[max(i-1,0)],PH[min(i+1,len(PH)-1)]),method='bounded',options={'xatol':1e-14})
    return min(best,r.fun)
if __name__=="__main__":
    Ts=[2,3,4,5,6,8,10,12,16,20]; lams=[2,5,10,30,100,1000]; al=np.linspace(0,1,2001)
    mult=int(sys.argv[1]); res=[]
    for T in Ts:
        N=mult*max(60,6*T+10); polys=[]
        for n in range(3,N+1):
            d=d0_row(n); polys.append((n,poly_move(n,T,d),(1+np.cos(2*np.pi*np.arange(n)/n))/2,1-d))
        DM=disk_move(PH,T); Lp=(1+np.cos(PH))/2; Lr=1-np.sin(PH/2)
        for lam in lams:
            cd=np.array([disk_exact(a,lam,T,DM,Lp,Lr) for a in al])
            cp=np.full(len(al),np.inf); bn=np.zeros(len(al),int)
            for n,m,lp,lr in polys:
                v=(m[None,:]+lam*(al[:,None]*lp[None,:]+(1-al[:,None])*lr[None,:])).min(1)
                b=v<cp; cp[b]=v[b]; bn[b]=n
            D=cd-cp; W=D>1e-12; ch=np.flatnonzero(W[1:]!=W[:-1])
            r=dict(T=T,lam=lam,N=N,W0=bool(W[0]),crossings=len(ch),cross_at=[float(al[c]) for c in ch],astar=float(al[ch[0]]) if len(ch) else None,
                   n_at_astar=int(bn[ch[0]]) if len(ch) else None,D1=float(D[-1]),tie=float((np.abs(D)<1e-9).mean()),
                   D_after=[float(D[c+1]) for c in ch], Dmax_disk_side=float(D[ch[0]+1:].max()) if len(ch) else None)
            res.append(r); print(r,flush=True)
    json.dump(res,open(f'rv_tl2_{mult}.json','w'))
    print("SINGLE",sum(r['W0'] and r['crossings']==1 for r in res),"of",len(res))
