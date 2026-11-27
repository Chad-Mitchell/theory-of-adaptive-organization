from rv_tl import *
from scipy.optimize import minimize_scalar
import sys
def disk_exact(a,lam,T):
    f=lambda p: float(disk_move(np.array([p]),T)[0]+lam*(a*(1+np.cos(p))/2+(1-a)*(1-np.sin(p/2))))
    v=disk_move(PH,T)+lam*(a*(1+np.cos(PH))/2+(1-a)*(1-np.sin(PH/2)))
    best=v.min()
    for i in np.argsort(v)[:5]:
        lo=PH[max(i-1,0)];hi=PH[min(i+1,len(PH)-1)]
        r=minimize_scalar(f,bounds=(lo,hi),method='bounded',options={'xatol':1e-13})
        best=min(best,r.fun)
    return best
for T,lam in [(4,2),(5,2),(6,2)]:
    N=60; polys=[]
    for n in range(3,N+1):
        d=d0_row(n); m=poly_move(n,T,d); phi=2*np.pi*np.arange(n)/n; polys.append((n,m,(1+np.cos(phi))/2,1-d))
    al=np.linspace(0,1,2001); D=[];BN=[]
    for a in al:
        cd=disk_exact(a,lam,T); vs=[(m+lam*(a*lp+(1-a)*lr)).min() for n,m,lp,lr in polys]; j=int(np.argmin(vs))
        D.append(cd-vs[j]); BN.append(polys[j][0])
    D=np.array(D); W=D>1e-12; ch=np.flatnonzero(W[1:]!=W[:-1])
    print(T,lam,"crossings",len(ch),[(round(al[c],4),D[c-1:c+3].tolist(),BN[c]) for c in ch])
