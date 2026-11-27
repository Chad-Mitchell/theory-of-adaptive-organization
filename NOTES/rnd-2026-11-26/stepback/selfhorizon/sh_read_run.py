# SH-read (SELF_HORIZON §10; pre-statement hash logged in WORKLOG 14:40 ET before this file was written).
import json, math, time, numpy as np
from multiprocessing import Pool
import sh_heat_core as C
SMAX=20000; YS=[0.1,1.0,10.0]; XS=C.XS; NMAX=1201
def best_check(R,x,y,smax=SMAX):
    grid=sorted(set(int(round(v)) for v in np.geomspace(1,smax,110))|set(range(1,11))|{max(1,math.floor(2/x)),math.ceil(2/x)})
    if R.p>0:
        g=math.sqrt(2*y/(x*R.p)) if (R.p>0 and y>0) else 1.0
        g=min(g,4*smax)
        for f in (0.5,1,2):
            v=int(round(g*f))
            if 1<=v<=smax: grid.append(v)
    grid=sorted(set(t for t in grid if 1<=t<=smax))
    J=lambda t:(y/R.p+R.HE(t)[0]+x*R.HE(t)[1])/t if R.p>0 else None
    if R.p==0:   # first-order regime with p underflow: J/p dominated by y/(p s) -> s*=smax (decreasing)
        return smax, None, True
    b=min(grid,key=J); w=3+int(0.05*b)
    for t in range(max(1,b-w),min(smax,b+w)+1): R.HE(t)
    b=min(R.cache,key=J)
    dec = (b==smax and J(smax)<J(smax-1))
    return b, R.p*J(b), dec
def job(args):
    n,s=args; R=C.Rec(n,s); out={'p':R.p,'tau_fade':float(1/R.pmp) if R.pmp>0 else 1e300}
    for x in XS:
        for y in YS:
            sb,jc,dec=best_check(R,x,y)
            keep=2.0*(s*s/2)*math.log(n); fade=x*(1-1/n)
            out['%g|%g'%(x,y)]={'keep':keep,'check':(jc if jc is not None else float('inf')) ,'fade':fade,'s_star':sb,'dec_at_edge':bool(dec),'p0':bool(R.p==0),'s_star':int(sb)}
    return n,s,out
if __name__=="__main__":
    jobs=[(n,s) for s in C.SIG for n in range(3,NMAX+1)]
    t0=time.time(); res={}
    with Pool(8) as P:
        for i,(n,s,o) in enumerate(P.imap_unordered(job,jobs,chunksize=16)):
            res['%d|%g'%(n,s)]=o
            if i%1000==0: print('progress',i,len(jobs),'%.0fs'%(time.time()-t0),flush=True)
    import pickle; pickle.dump(res,open('sh_read_modes.pkl','wb'))
    json.dump(res,open('sh_read_modes.json','w'),default=lambda o: o.item() if hasattr(o,'item') else str(o)); print('done',len(res),'%.0fs'%(time.time()-t0),flush=True)
