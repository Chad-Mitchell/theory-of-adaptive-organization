import json, numpy as np
R=[json.loads(l) for l in open('wt_run.jsonl')]
sigs=[1e-3,3e-3,1e-2,3e-2,0.1,0.3]; xs=[1,3,10,30,100,300,1e3,3e3,1e4,3e4,1e5,1e6]; Gs=[0,1e-5,1e-4,1e-3,1e-2,1e-1]
D={(r['sig'],r['x'],r['G']):r for r in R if r['arm']=='primary'}
def reg(r):
    return 'K' if r['keep']>=2*r['read'] else ('R' if r['read']>=2*r['keep'] else 'M')
print("(1) s*=1 cells by sigma*sqrt(x): ")
for s in sigs:
    print(" sigma",s,"x with s*=1 (Gamma=0):",[x for x in xs if D[(s,x,0)]['s']==1])
print("(2) H-b restricted to pairs with s*>=3 in both (post hoc robustness):")
ex=[np.log(D[(s,b,G)]['n']/D[(s,a,G)]['n'])/np.log(b/a) for s in sigs for G in Gs for a,b in zip(xs[:-1],xs[1:]) if reg(D[(s,a,G)])=='K' and reg(D[(s,b,G)])=='K' and D[(s,a,G)]['s']>=3 and D[(s,b,G)]['s']>=3]
ex=np.array(ex); print("  pairs",len(ex),"median",np.median(ex).round(3),"frac in window",((ex>=.35)&(ex<=.65)).mean().round(3))
print("(3) S3 rows (sigma,Gamma): local e_x(n*) along x, regimes")
for s in sigs:
    for G in Gs[1:]:
        regs=[reg(D[(s,x,G)]) for x in xs]
        if 'K' in regs and 'R' in regs:
            sl=[np.log(D[(s,b,G)]['n']/D[(s,a,G)]['n'])/np.log(b/a) for a,b in zip(xs[:-1],xs[1:])]
            print(f"  {s},{G}: "+" ".join(f"{t}" for t in regs)); print("      slopes "+" ".join(f"{v:.2f}" for v in sl)); print("      s*   "+" ".join(str(D[(s,x,G)]['s']) for x in xs))
print("(4) crossover location: data x_cross (keep=read, log-interp) vs composition estimate (keep floor on the Gamma=0 design = its read cost)")
rows=[]
for s in sigs:
    for G in Gs[1:]:
        kr=np.array([D[(s,x,G)]['keep']/D[(s,x,G)]['read'] for x in xs])
        k0=np.array([2*G*np.log(D[(s,x,0)]['n'])/D[(s,x,0)]['read'] for x in xs])
        def cross(v):
            lx=np.log(xs); lv=np.log(v)
            for i in range(len(xs)-1):
                if (lv[i]-0)*(lv[i+1]-0)<=0 and lv[i]!=lv[i+1]:
                    return float(np.exp(lx[i]+(0-lv[i])*(lx[i+1]-lx[i])/(lv[i+1]-lv[i])))
            return None
        xd,xc=cross(kr),cross(k0)
        if xd and xc: rows.append((s,G,xd,xc,xd/xc))
for r in rows: print(f"  sigma {r[0]} Gamma {r[1]}: x_data {r[2]:.3g}  x_comp {r[3]:.3g}  ratio {r[4]:.2f}")
if rows:
    rat=np.array([r[4] for r in rows]); print("  ratio range",rat.min().round(2),rat.max().round(2),"all within factor 3:",bool(((rat<=3)&(rat>=1/3)).all()))
print("(5) composition predictor n_comp = (n_K^-p + n_R^-p)^(-1/p) best p, error:")
best=None
for p in [1,2,3,4,6,8]:
    err=[]
    for k,r in D.items():
        s,x,G=k
        if G==0: continue
        nK=r['nGPK']; nR=D[(s,x,0)]['n']
        nc=(nK**-p+nR**-p)**(-1/p); err.append(abs(np.log(r['n']/nc)))
    err=np.array(err); print(f"  p={p}: median |ln err| {np.median(err):.3f}, 95% {np.percentile(err,95):.3f}, max {err.max():.3f}")
print("(6) cost split at optimum, Gamma=0, s*>=3: read/loss ratio")
q=[D[k]['read']/D[k]['loss'] for k in D if k[2]==0 and D[k]['s']>=3]; print("  median",np.median(q).round(3),"range",np.round(min(q),3),np.round(max(q),3))
print("(7) n* ~ C x^0.25 sigma^-0.5 at Gamma=0, s*>=3: C values")
C=[D[k]['n']/(k[1]**0.25*k[0]**-0.5) for k in D if k[2]==0 and D[k]['s']>=3]; print("  median",np.median(C).round(3),"range",np.round(min(C),3),np.round(max(C),3))
Cs=[D[k]['s']*k[0]*k[1]**0.5 for k in D if k[2]==0 and D[k]['s']>=3]; print("  s* sigma sqrt(x): median",np.median(Cs).round(3),"range",np.round(min(Cs),3),np.round(max(Cs),3))
