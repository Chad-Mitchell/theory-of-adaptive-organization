# Rescore Step 1 from the reviewer's own run (rv_wt.jsonl) using the hashed §1.5 criteria literally; robustness cuts.
import json, numpy as np
from rv_wt import RG, H0
D={(r['sig'],r['x'],r['G']):r for r in map(json.loads,open('rv_wt.jsonl'))}
sigs=[1e-3,3e-3,1e-2,3e-2,0.1,0.3]; xs=[1,3,10,30,100,300,1e3,3e3,1e4,3e4,1e5,1e6]; Gs=[0,1e-5,1e-4,1e-3,1e-2,1e-1]
def reg(r):
    if r['n']==1: return 'blind'
    return 'K' if r['keep']>=2*r['read'] else ('R' if r['read']>=2*r['keep'] else 'M')
R={k:reg(r) for k,r in D.items()}
print("regimes",{t:list(R.values()).count(t) for t in ['K','R','M','blind']},"s*=1:",sum(r['s']==1 for r in D.values()),"far:",sum(r['far']>0 for r in D.values()),"edge:",sum(r['edge'] for r in D.values()))
def Hb(smin=1):
    e=[np.log(D[(s,b,G)]['n']/D[(s,a,G)]['n'])/np.log(b/a) for s in sigs for G in Gs for a,b in zip(xs[:-1],xs[1:])
       if R[(s,a,G)]=='K' and R[(s,b,G)]=='K' and min(D[(s,a,G)]['s'],D[(s,b,G)]['s'])>=smin]
    e=np.array(e); return len(e),np.median(e),((e>=.35)&(e<=.65)).mean()
def Hc(smin=3):
    e=[abs(np.log(D[(b,x,G)]['s']/D[(a,x,G)]['s'])/np.log(b/a)) for x in xs for G in Gs for a,b in zip(sigs[:-1],sigs[1:])
       if D[(a,x,G)]['n']>1 and D[(b,x,G)]['n']>1 and min(D[(a,x,G)]['s'],D[(b,x,G)]['s'])>=smin]
    e=np.array(e); return len(e),np.median(e),((e>=.8)&(e<=1.2)).mean()
print("H-b (all K pairs):",Hb(1)," s*>=3:",Hb(3)," s*>=10:",Hb(10))
print("H-c (pre-stated s*>=3):",Hc(3)," s*>=10:",Hc(10)," s*>=30:",Hc(30))
# Hc by sigma pair
for a,b in zip(sigs[:-1],sigs[1:]):
    e=[abs(np.log(D[(b,x,G)]['s']/D[(a,x,G)]['s'])/np.log(b/a)) for x in xs for G in Gs if D[(a,x,G)]['n']>1 and min(D[(a,x,G)]['s'],D[(b,x,G)]['s'])>=3]
    print("  H-c pair",a,b,len(e),np.round(np.median(e),3) if e else None)
# scaling identity: small-sigma, s>>1, Gamma=0: J = H(rho)/s + x sigma^2 s g(rho), g = 1/(24 rho^2)+1/4
rho=np.exp(np.linspace(np.log(0.05),np.log(10),20000)); H=np.interp(np.log(rho),np.log(RG),H0); g=1/(24*rho**2)+0.25
f=np.sqrt(H*g); i=f.argmin()
print(f"scaling identity: rho*={rho[i]:.3f}, H*={H[i]:.3f} nats, J*/(sigma sqrt x)={2*f[i]:.4f}, s* sigma sqrt x={np.sqrt(H[i]/g[i]):.3f}, n* x^-1/4 sigma^1/2={2*np.pi*rho[i]*(H[i]/g[i])**-0.25:.3f}")
G0=[r for k,r in D.items() if k[2]==0 and r['s']>=3]
c=[r['n']*r['x']**-0.25*r['sig']**0.5 for r in G0]; cs=[r['s']*r['sig']*r['x']**0.5 for r in G0]; cj=[r['J']/(r['sig']*r['x']**0.5) for r in G0]
print("observed (mine) Gamma=0 s*>=3:",len(G0),"C_n median",np.median(c),"C_s median",np.median(cs),"J/(sig sqrt x) median",np.median(cj), "rho median",np.median([r['rho'] for r in G0]),"H median",np.median([r['H'] for r in G0]))
small=[r for r in G0 if r['sig']<=0.01 and r['s']>=30]
print(" restricted sigma<=0.01, s*>=30:",len(small),"J/(sig sqrt x)",np.round([r['J']/(r['sig']*r['x']**0.5) for r in small],4))
