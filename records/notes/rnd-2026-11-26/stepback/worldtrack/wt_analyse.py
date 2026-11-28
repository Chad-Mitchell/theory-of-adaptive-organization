import json, numpy as np, sys
recs=[json.loads(l) for l in open('wt_run.jsonl')]
sigs=[1e-3,3e-3,1e-2,3e-2,0.1,0.3]; xs=[1,3,10,30,100,300,1e3,3e3,1e4,3e4,1e5,1e6]; Gs=[0,1e-5,1e-4,1e-3,1e-2,1e-1]
def regime(r):
    if r['blind']: return 'blind'
    if r['keep']>=2*r['read']: return 'K'
    if r['read']>=2*r['keep']: return 'R'
    return 'M'
for arm in ['primary','a1','cK4']:
    D={(r['sig'],r['x'],r['G']):r for r in recs if r['arm']==arm}
    if len(D)<432: print(arm,"incomplete",len(D)); continue
    print(f"\n===== ARM {arm} =====")
    nb=[r for r in D.values() if not r['blind']]
    reg={k:regime(r) for k,r in D.items()}
    print("cells",len(D),"blind",sum(r['blind'] for r in D.values()),"regimes",{t:list(reg.values()).count(t) for t in 'KRM'})
    nonuniq=[(k,r['far'][:2]) for k,r in D.items() if not r['blind'] and r['nfar']>0]
    print("H-a non-unique non-blind cells:",len(nonuniq),"of",len(nb),nonuniq[:6])
    edges=[k for k,r in D.items() if r['edge_n'] or r['edge_s']]
    print("H-d edge cells:",len(edges),edges[:6])
    s1=sum(r['s']==1 for r in nb); print("s*=1 cells (stated regime):",s1)
    # H-b
    ex=[]
    for s in sigs:
        for G in Gs:
            for a,b in zip(xs[:-1],xs[1:]):
                A,B=D[(s,a,G)],D[(s,b,G)]
                if reg[(s,a,G)]=='K' and reg[(s,b,G)]=='K':
                    ex.append(np.log(B['n']/A['n'])/np.log(b/a))
    ex=np.array(ex); inw=((ex>=0.35)&(ex<=0.65)).mean() if len(ex) else np.nan
    print(f"H-b keep pairs {len(ex)} median e_x(n*) {np.median(ex) if len(ex) else np.nan:.3f} frac in [0.35,0.65] {inw:.3f}  -> {'PASS' if len(ex)>=10 and 0.35<=np.median(ex)<=0.65 and inw>=0.75 else ('OPEN' if len(ex)<10 else 'FAIL')}")
    # H-c
    es=[]
    for x in xs:
        for G in Gs:
            for a,b in zip(sigs[:-1],sigs[1:]):
                A,B=D[(a,x,G)],D[(b,x,G)]
                if not A['blind'] and not B['blind'] and A['s']>=3 and B['s']>=3:
                    es.append(np.log(B['s']/A['s'])/np.log(b/a))
    es=np.abs(np.array(es)); inw2=((es>=0.8)&(es<=1.2)).mean()
    print(f"H-c sigma pairs {len(es)} median |e_sig(s*)| {np.median(es):.3f} frac in [0.8,1.2] {inw2:.3f} -> {'PASS' if len(es)>=10 and 0.8<=np.median(es)<=1.2 and inw2>=0.75 else ('OPEN' if len(es)<10 else 'FAIL')}")
    print("   |e_sig(s*)| quantiles 10/25/50/75/90:",np.round(np.percentile(es,[10,25,50,75,90]),3))
    # S1
    Rc=[r for k,r in D.items() if reg[k]=='R' and r['s']>=3]
    rh=np.array([r['rho'] for r in Rc]); 
    print(f"S1 R cells s*>=3: {len(Rc)} rho* median {np.median(rh):.3f} range [{rh.min():.3f},{rh.max():.3f}] frac in [0.05,0.8] {((rh>=0.05)&(rh<=0.8)).mean():.3f}")
    Hs=np.array([r['H'] for r in Rc]); print(f"   H* nats median {np.median(Hs):.3f} range [{Hs.min():.3f},{Hs.max():.3f}]")
    # S2
    exR=[];esR=[]
    for s in sigs:
        for G in Gs:
            for a,b in zip(xs[:-1],xs[1:]):
                if reg[(s,a,G)]=='R' and reg[(s,b,G)]=='R' and D[(s,a,G)]['s']>=3 and D[(s,b,G)]['s']>=3:
                    exR.append(np.log(D[(s,b,G)]['n']/D[(s,a,G)]['n'])/np.log(b/a))
    for x in xs:
        for G in Gs:
            for a,b in zip(sigs[:-1],sigs[1:]):
                if reg[(a,x,G)]=='R' and reg[(b,x,G)]=='R' and D[(a,x,G)]['s']>=3 and D[(b,x,G)]['s']>=3:
                    esR.append(np.log(D[(b,x,G)]['n']/D[(a,x,G)]['n'])/np.log(b/a))
    print(f"S2 R pairs: e_x(n*) n={len(exR)} median {np.median(exR):.3f}; e_sig(n*) n={len(esR)} median {np.median(esR):.3f}")
    # S3 crossover
    rows=0;ok=0
    for s in sigs:
        for G in Gs[1:]:
            regs=[reg[(s,x,G)] for x in xs]; nonb=[x for x in xs if not D[(s,x,G)]['blind']]
            if 'K' in regs and 'R' in regs and len(nonb)>=3:
                rows+=1
                sl=[np.log(D[(s,b,G)]['n']/D[(s,a,G)]['n'])/np.log(b/a) for a,b in zip(nonb[:-1],nonb[1:])]
                ok+= sl[-1]<sl[0]
    print(f"S3 rows spanning K and R: {rows}, slope lower at largest x: {ok}")
    # Bar A
    print(f"Bar A1: median |e_sig(n*)| over R pairs = {np.median(np.abs(esR)):.3f}")
    rat=[np.log(r['n']/r['nGPK']) for k,r in D.items() if reg[k]=='K' and r['nGPK']]
    print(f"Bar A2: K cells {len(rat)} median |ln(n*/n_GPK)| = {np.median(np.abs(rat)):.4f}  (threshold ln1.25={np.log(1.25):.3f}); max {np.max(np.abs(rat)):.3f}")
    # blind thresholds
    th={}
    for s in sigs:
        for G in Gs:
            nbx=[x for x in xs if not D[(s,x,G)]['blind']]
            th[(s,G)]=min(nbx) if nbx else None
    print("smallest non-blind x per (sigma,Gamma):",{f"{k[0]},{k[1]}":v for k,v in th.items() if v!=1})
    # non-monotone n*(x)
    nm=[(s,G) for s in sigs for G in Gs if any(D[(s,b,G)]['n']<D[(s,a,G)]['n'] for a,b in zip(xs[:-1],xs[1:]) if not D[(s,a,G)]['blind'])]
    print("rows with non-monotone n*(x):",nm)
    nms=[(x,G) for x in xs for G in Gs if any(D[(b,x,G)]['s']>D[(a,x,G)]['s'] for a,b in zip(sigs[:-1],sigs[1:]) if not D[(a,x,G)]['blind'] and not D[(b,x,G)]['blind'])]
    print("rows with s* increasing in sigma:",nms)
