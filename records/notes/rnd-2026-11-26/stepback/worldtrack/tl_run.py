from tl_core import *
Ts=[2,3,4,5,6,8,10,12,16,20]; lams=[2,5,10,30,100,1000]
alphas=np.round(np.arange(201)*0.005,3)
out={'cells':[],'diskcheck':{}}
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
for T in Ts:
    ang,m=disk_grid_dp(T,M=3600); sel=ang<=np.pi+1e-12
    out['diskcheck'][T]=float((m[sel]-disk_D(ang[sel],T)).min())
    polys={}
    for n in range(3,max(60,6*T+10)+1):
        mv,d0=poly_move(n,T); phi=2*np.pi*np.arange(n)/n
        polys[n]=(mv,(1+np.cos(phi))/2,1-d0,phi)
    # P15 strong check: at alpha=1 each polygon endpoint vs disk endpoint at same angle
    viol=0
    for n,(mv,lp,lr,phi) in polys.items():
        pa=np.minimum(phi,2*np.pi-phi)
        viol+=int(np.sum(mv+1e-12<disk_D(pa,T)))
    for lam in lams:
        rec=[]
        for a in alphas:
            cd,pd=disk_C(a,lam,T)
            best=np.inf;bn=None;bk=None
            for n,(mv,lp,lr,phi) in polys.items():
                v=mv+lam*(a*lp+(1-a)*lr); k=int(v.argmin())
                if v[k]<best-1e-15: best,bn,bk=v[k],n,k
            rec.append((float(a),float(cd),float(best),bn,bk,float(pd)))
        out['cells'].append({'T':T,'lam':lam,'rec':rec,'p15_endpoint_viol':viol})
        print(T,lam,'done',flush=True)
json.dump(out,open('tl_run.json','w'))
