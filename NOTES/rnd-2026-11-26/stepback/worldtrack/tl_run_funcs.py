from tl_core import *
phig=np.linspace(0,np.pi,20001)
def disk_C(a,lam,T):
    f=lambda p: disk_D(np.atleast_1d(p),T)+lam*(a*(1+np.cos(p))/2+(1-a)*(1-np.sin(np.atleast_1d(p)/2)))
    v=f(phig); i=int(v.argmin()); lo,hi=phig[max(i-1,0)],phig[min(i+1,len(phig)-1)]
    g=(5**.5-1)/2
    for _ in range(80):
        c=hi-g*(hi-lo); d=lo+g*(hi-lo)
        if f(c)[0]<f(d)[0]: hi=d
        else: lo=c
    p=(lo+hi)/2; return min(f(p)[0],v[i]), p
_cache={}
def build(T):
    if T in _cache: return _cache[T]
    polys={}
    for n in range(3,max(60,6*T+10)+1):
        mv,d0=poly_move(n,T); phi=2*np.pi*np.arange(n)/n
        polys[n]=(mv,(1+np.cos(phi))/2,1-d0,phi)
    _cache[T]=polys; return polys
