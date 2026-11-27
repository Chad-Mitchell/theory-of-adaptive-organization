import json, sys, time, math, os
from multiprocessing import Pool
import sh_heat_core as C
NMAX=1201
def job(args):
    n,s=args; R=C.Rec(n,s); out={'p':R.p,'pmp':float(R.pmp),'tau_fade':float(1/R.pmp) if R.pmp>0 else 1e300}
    for x in C.XS:
        for ck in C.CK:
            out['%g|%g'%(x,ck)]=C.modes(R,x,ck)
    return (n,s,out)
if __name__=="__main__":
    jobs=[(n,s) for s in C.SIG for n in range(3,NMAX+1)]
    t0=time.time(); res={}
    with Pool(8) as P:
        for i,(n,s,o) in enumerate(P.imap_unordered(job,jobs,chunksize=16)):
            res['%d|%g'%(n,s)]=o
            if i%1000==0: print('progress',i,len(jobs),'%.0fs'%(time.time()-t0),flush=True)
    json.dump(res,open('sh_heat_modes.json','w'))
    print('done',len(res),'%.0fs'%(time.time()-t0),flush=True)
