import json, numpy as np, sys
sys.argv=['x']
exec(open('ib_run.py').read().split("Pg=np.exp")[0])  # load parts, Kavg, constants
R=[json.loads(l) for l in open('ib_run.jsonl')]
q=[r['J']/r['core'] for r in R if r['G']==0 and r['c']==0 and r['arm']=='write']
print("(1) J*/CORE frontier at Gamma=0,c=0 all smin: min %.6f max %.4f"%(min(q),max(q)))
low=[(r['sig'],r['x'],r['smin'],r['J'],r['core']) for r in R if r['G']==0 and r['c']==0 and r['arm']=='write' and r['J']<r['core']*(1-1e-9)]
print("    cells below CORE frontier:",len(low),low[:3])
# S-eq
W=[json.loads(l) for l in open('wt_run.jsonl')]
S1=[r for r in W if r['arm']=='primary' and r['G']==0 and r['s']>=3]
from scipy.optimize import minimize
Pg=np.exp(np.linspace(np.log(1e-14),np.log(v),500))
def sstar(sig,x,c,smin=1.0):
    sg=np.exp(np.linspace(np.log(smin),np.log(1e8),500))
    lo,av,a=parts(Pg[:,None],sg[None,:],sig); J=lo+c/sg[None,:]+0.5*x*av
    i,k=np.unravel_index(np.argmin(J),J.shape)
    f=lambda z: 1e300 if (np.exp(z[0])>v or np.exp(z[1])<smin) else float(sum(t for t in [parts(np.exp(z[0]),np.exp(z[1]),sig)[0]+c/np.exp(z[1])+0.5*x*parts(np.exp(z[0]),np.exp(z[1]),sig)[1]]))
    res=minimize(f,[np.log(Pg[i]),np.log(sg[k])],method='Nelder-Mead',options=dict(xatol=1e-7,fatol=1e-14))
    P,s=np.exp(res.x); return max(s,smin), P
cgrid=np.exp(np.linspace(np.log(0.01),np.log(1000),61))
best=None
for c in cgrid:
    rat=np.array([np.log(sstar(r['sig'],r['x'],c)[0]/r['s']) for r in S1])
    m=np.median(np.abs(rat))
    if best is None or m<best[1]: best=(c,m,rat)
c,m,rat=best
print(f"(2) S-eq: {len(S1)} Step-1 cells; best c_eff={c:.3f} kT/look; median |ln ratio| {m:.3f}; within 25%: {(np.abs(rat)<=np.log(1.25)).mean():.3f} -> {'PASS' if (np.abs(rat)<=np.log(1.25)).mean()>=0.75 else 'FAIL'}")
print("    ratio quantiles s_gauss/s_reg:",np.round(np.exp(np.percentile(rat,[0,25,50,75,100])),3))
# stored info offset vs register at matched c_eff
off=[]
for r in S1:
    s,P=sstar(r['sig'],r['x'],c); off.append(np.log(r['n'])-0.5*np.log(v/P))
print(f"(3) ln n*(register) - I*(Gaussian, c_eff): median {np.median(off):.3f} range [{min(off):.3f},{max(off):.3f}] (GP space-filling gap 0.5ln(pi e/6)={0.5*np.log(np.pi*np.e/6):.3f})")
# (4) Gaussian c=0,smin=1 nats/look vs smin*sig*sqrt x
G0=[r for r in R if r['G']==0 and r['c']==0 and r['smin']==1.0 and r['arm']=='write']
u=np.array([r['sig']*np.sqrt(r['x']) for r in G0]); nn=np.array([r['nats'] for r in G0])
print("(4) c=0, smin=1, Gamma=0: nats/look vs u=sig*sqrt(x): corr of ln:",np.corrcoef(np.log(u),np.log(nn))[0,1].round(4))
for a,b in [(1e-3,1e-2),(1e-2,1e-1),(0.1,1),(1,10),(10,1e3)]:
    m_=(u>=a)&(u<b); 
    if m_.any(): print(f"    u in [{a},{b}): nats/look {nn[m_].min():.4f}-{nn[m_].max():.4f}")
# (5) where B3 fails in primary: slopes restricted to u*smin<=0.1
D={(r['sig'],r['x'],r['G']):r for r in R if r['smin']==1.0 and r['c']==0 and r['arm']=='write'}
def reg(r): return 'K' if r['keep']>=2*r['look'] else ('R' if r['look']>=2*r['keep'] else 'M')
sigs=[1e-3,3e-3,1e-2,3e-2,0.1,0.3]; xs=[1,3,10,30,100,300,1e3,3e3,1e4,3e4,1e5,1e6]; Gs=[0,1e-5,1e-4,1e-3,1e-2,1e-1]
rx=[(D[(s,b,G)]['I']-D[(s,a,G)]['I'])/np.log(b/a) for s in sigs for G in Gs for a,b in zip(xs[:-1],xs[1:]) if reg(D[(s,a,G)])=='R' and reg(D[(s,b,G)])=='R' and s*np.sqrt(b)<=0.1]
rs=[(D[(b,x,G)]['I']-D[(a,x,G)]['I'])/np.log(b/a) for x in xs for G in Gs for a,b in zip(sigs[:-1],sigs[1:]) if reg(D[(a,x,G)])=='R' and reg(D[(b,x,G)])=='R' and b*np.sqrt(x)<=0.1]
print(f"(5) post hoc, primary restricted to smin*sig*sqrt(x)<=0.1: R dI/dlnx n={len(rx)} med {np.median(rx):.3f}; R dI/dlnsig n={len(rs)} med {np.median(rs):.3f}")
