import json, numpy as np
R=[json.loads(l) for l in open('ib_run.jsonl')]
sigs=[1e-3,3e-3,1e-2,3e-2,0.1,0.3]; xs=[1,3,10,30,100,300,1e3,3e3,1e4,3e4,1e5,1e6]; Gs=[0,1e-5,1e-4,1e-3,1e-2,1e-1]
def sel(smin,c,arm='write'): return {(r['sig'],r['x'],r['G']):r for r in R if r['smin']==smin and r['c']==c and r['arm']==arm}
def reg(r):
    if r['blind']: return 'B'
    return 'K' if r['keep']>=2*r['look'] else ('R' if r['look']>=2*r['keep'] else 'M')
print("cells",len(R),"edge cells",sum(r['edge'] for r in R),"blind",sum(r['blind'] for r in R))
# C0
D=sel(0.01,0.0); err=[]
for (s,x,G),r in D.items():
    if G==0 and 0.01*s*np.sqrt(x)<=1e-3: err.append(r['J']/r['core']-1)
err=np.array(err); print(f"C0: {len(err)} cells, J*/CORE-1: max |.| {np.abs(err).max():.2e} -> {'PASS' if len(err) and np.abs(err).max()<0.01 else 'FAIL'}")
def score(smin,c,arm='write',verbose=True):
    D=sel(smin,c,arm); nb=[r for r in D.values() if not r['blind']]
    pinned=[r for r in nb if r['s']<=1.02*smin]
    Rc=[r for k,r in D.items() if reg(r)=='R']
    nats=np.array([r['nats'] for r in Rc])
    B1=len(nats)>0 and abs(np.median(nats)-1.10)<=0.30
    es=[];ex=[]
    for x in xs:
        for G in Gs:
            for a,b in zip(sigs[:-1],sigs[1:]):
                A,Bq=D[(a,x,G)],D[(b,x,G)]
                if not A['blind'] and not Bq['blind'] and A['s']>1.02*smin and Bq['s']>1.02*smin: es.append(np.log(Bq['s']/A['s'])/np.log(b/a))
    for s in sigs:
        for G in Gs:
            for a,b in zip(xs[:-1],xs[1:]):
                A,Bq=D[(s,a,G)],D[(s,b,G)]
                if not A['blind'] and not Bq['blind'] and A['s']>1.02*smin and Bq['s']>1.02*smin: ex.append(np.log(Bq['s']/A['s'])/np.log(b/a))
    fp=len(pinned)/max(1,len(nb))
    B2=fp<0.25 and len(es)>0 and 0.8<=np.median(np.abs(es))<=1.2 and len(ex)>0 and -0.65<=np.median(ex)<=-0.35
    def slopes(regt,var):
        out=[]
        if var=='x':
            for s in sigs:
                for G in Gs:
                    for a,b in zip(xs[:-1],xs[1:]):
                        A,Bq=D[(s,a,G)],D[(s,b,G)]
                        if reg(A)==regt and reg(Bq)==regt: out.append((Bq['I']-A['I'])/np.log(b/a))
        else:
            for x in xs:
                for G in Gs:
                    for a,b in zip(sigs[:-1],sigs[1:]):
                        A,Bq=D[(a,x,G)],D[(b,x,G)]
                        if reg(A)==regt and reg(Bq)==regt: out.append((Bq['I']-A['I'])/np.log(b/a))
        return np.array(out)
    rx,rs,kx=slopes('R','x'),slopes('R','s'),slopes('K','x')
    B3=(len(rx) and 0.2<=np.median(rx)<=0.3) and (len(rs) and -0.6<=np.median(rs)<=-0.4) and (len(kx) and 0.4<=np.median(kx)<=0.6)
    if verbose:
        print(f"\n== smin {smin} c {c} keep-arm {arm}: nonblind {len(nb)}, pinned {len(pinned)} ({fp:.1%}); regimes",{t:[reg(r) for r in D.values()].count(t) for t in 'KRMB'})
        if len(nats): print(f"  B1 nats/look R cells {len(nats)}: median {np.median(nats):.4f} q10 {np.percentile(nats,10):.4f} q90 {np.percentile(nats,90):.4f} -> {'PASS' if B1 else 'FAIL'}")
        print(f"  B2 non-pinned sigma pairs {len(es)} median|e_sig(s*)| {np.median(np.abs(es)) if es else float('nan'):.3f}; x pairs {len(ex)} median e_x(s*) {np.median(ex) if ex else float('nan'):.3f} -> {'PASS' if B2 else 'FAIL'}")
        print(f"  B3 R dI/dlnx n={len(rx)} med {np.median(rx) if len(rx) else np.nan:.3f}; R dI/dlnsig n={len(rs)} med {np.median(rs) if len(rs) else np.nan:.3f}; K dI/dlnx n={len(kx)} med {np.median(kx) if len(kx) else np.nan:.3f} -> {'PASS' if B3 else 'FAIL'}")
    return B1,B2,B3
res={}
for smin in [1.0,0.1,0.01]:
    for c in [0.0,0.1,1.0,10.0]:
        res[(smin,c)]=score(smin,c)
score(1.0,0.0,'avgkeep')
# B4
D=sel(0.01,0.0); q=np.array([r['J']/(r['sig']*np.sqrt(r['x'])) for (s,x,G),r in D.items() if G==0 and 0.01*s*np.sqrt(x)<=0.1])
cst=np.median(q); B4=bool((np.abs(q/cst-1)<=0.10).all() and cst<=1.244)
print(f"\nB4: {len(q)} cells, J*/(sig sqrt x) median {cst:.4f} range [{q.min():.4f},{q.max():.4f}] -> {'PASS' if B4 else 'FAIL'}")
# collapse: J/(sig sqrt x) vs smin*sig*sqrt x at Gamma=0,c=0 across smin
print("collapse check Gamma=0 c=0: J/(sig sqrt x) binned by u=smin*sig*sqrt(x):")
pts=[(r['smin']*r['sig']*np.sqrt(r['x']),r['J']/(r['sig']*np.sqrt(r['x']))) for r in R if r['G']==0 and r['c']==0 and r['arm']=='write']
pts=np.array(pts); 
for lo,hi in [(1e-5,1e-3),(1e-3,1e-2),(1e-2,1e-1),(0.1,1),(1,10),(10,100),(100,1e3)]:
    m=(pts[:,0]>=lo)&(pts[:,0]<hi)
    if m.any(): print(f"  u in [{lo:g},{hi:g}): n={m.sum()} J/(s sqrt x) {pts[m,1].min():.4f}-{pts[m,1].max():.4f}")
B1,B2,B3=res[(1.0,0.0)]
overall='HIT' if (B1 and B2 and B3 and B4) else ('PARTIAL' if (B3 and B4) else 'MISS')
print(f"\nPRIMARY (smin=1,c=0): B1 {B1} B2 {B2} B3 {B3} B4 {B4} -> {overall}")
# per-look price theory check: nats/look vs 0.5 ln(1+2 sqrt c), R cells, smin=0.01
for c in [0.1,1.0,10.0]:
    D=sel(0.01,c); n=[r['nats'] for r in D.values() if reg(r)=='R' and r['s']>1.02*0.01]
    print(f"c={c}: nats/look R non-pinned n={len(n)} median {np.median(n) if n else np.nan:.4f} (paper 0.5ln(1+2sqrt c)={0.5*np.log(1+2*np.sqrt(c)):.4f})")
