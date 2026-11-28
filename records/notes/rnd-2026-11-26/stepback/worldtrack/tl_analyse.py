from tl_core import *
import json
from tl_run_funcs import disk_C, build
R=json.load(open('tl_run.json'))
print("disk DP-vs-formula min diff per T (must be >= -1e-9):",{k:round(v,12) for k,v in R['diskcheck'].items()})
cls={'proper_single':0,'proper_multi':0,'never_poly':0,'always_poly':0,'ambig':0}
rows=[];affine=0;ncross=0
for c in R['cells']:
    T,lam=c['T'],c['lam']; rec=c['rec']
    a=np.array([r[0] for r in rec]); D=np.array([r[1]-r[2] for r in rec])
    W=D>1e-12; tie=np.abs(D)<1e-9
    if tie.mean()>0.10: cls['ambig']+=1; tag='ambig'
    elif not W.any(): cls['never_poly']+=1; tag='never_poly'
    elif W.all(): cls['always_poly']+=1; tag='always_poly'
    else:
        ch=np.flatnonzero(W[1:]!=W[:-1])
        if W[0] and len(ch)==1: cls['proper_single']+=1; tag='single'
        else: cls['proper_multi']+=1; tag='multi'
    polys=build(T)
    def delta(al):
        cd,_=disk_C(al,lam,T)
        return cd-min((mv+lam*(al*lp+(1-al)*lr)).min() for mv,lp,lr,phi in polys.values())
    astar=None
    if tag in('single','multi'):
        i=np.flatnonzero(W[1:]!=W[:-1])[0]; lo,hi=a[i],a[i+1]
        for _ in range(40):
            m=(lo+hi)/2
            if delta(m)>1e-12: lo=m
            else: hi=m
        astar=(lo+hi)/2
        # affine test: argmins unchanged across alpha?
        bn=set((r[3],r[4]) for r in rec); pdk=set(round(r[5],6) for r in rec)
        ncross+=1
        if len(bn)==1 and len(pdk)==1: affine+=1
    bnset=sorted(set(r[3] for r in rec))
    rows.append((T,lam,tag,astar,(astar*lam if astar else None),D[0],D[-1],c['p15_endpoint_viol'],bnset[:6],len(set((r[3],r[4]) for r in rec)),len(set(round(r[5],6) for r in rec))))
print("P15 endpoint violations total:",sum(r[7] for r in rows[::6]))
print("max Delta at alpha=1 over cells:",max(r[6] for r in rows))
print("classes:",cls)
print("crossing cells:",ncross,"affine (argmins fixed):",affine)
print("T lam class alpha* alpha*lam Delta(0) Delta(1) best-n-set #poly-argmins #disk-endpoints")
for r in rows: print(r[0],r[1],r[2],None if r[3] is None else round(r[3],6),None if r[4] is None else round(r[4],4),f"{r[5]:.5f}",f"{r[6]:.2e}",r[8],r[9],r[10])
json.dump(rows,open('tl_analyse.json','w'),default=str)
