# SH-read analysis per SELF_HORIZON §10 (hash logged 14:40 ET).
import json, math, sys
import numpy as np
import sh_heat_core as C
A=json.load(open("argmin_sets.json")); M=json.load(open("sh_read_modes.json"))
CFG=['E-M3h','O','F-M3h','F-mixed','E-mixed']; SCORED=CFG[:4]; NMAX=1201
XS=C.XS; YS=[0.1,1.0,10.0]
def dmin(n):
    if n%2: return math.sin(math.pi/n)/math.cos(math.pi/(2*n))
    S=n//2; return math.sin(math.pi/n)/(math.cos(math.pi/n) if (1-S)%2 else 1.0)
def menu(cfg):
    if cfg.startswith('E'): return list(range(4,NMAX+1,2))
    if cfg=='O': return list(range(3,NMAX+1,2))
    return list(range(3,NMAX+1))
def tau(n,s,x,y,reading):
    o=M['%d|%g'%(n,s)]; m=o['%g|%g'%(x,y)]
    c={'keep':m['keep'],'check':m['check'],'fade':m['fade']}
    best=min(c.values()); tied=[k for k,v in c.items() if abs(v-best)<=1e-12*max(abs(best),1e-300)]
    taus={'keep':math.inf,'check':(float(m['s_star']) if reading=='W' else math.inf),'fade':o['tau_fade']}
    md=min(tied,key=lambda k:taus[k]); edge_open = (md=='check' and reading=='W' and m['s_star']>=20000 and not m['dec_at_edge'] and not m['p0'])
    return md,taus[md],edge_open
def cell(cfg,s,x,y,reading,rnd):
    As={int(k):v for k,v in A[cfg]['A'].items()}; ns=menu(cfg); T={}; opens=0; modes={'keep':0,'check':0,'fade':0}
    for n in ns:
        md,t,eo=tau(n,s,x,y,reading); modes[md]+=1
        if eo: T[n]=None; opens+=1; continue
        if t==math.inf: T[n]=None; continue
        tt=rnd(t)
        if tt>400:
            T[n]=None
            if not tt>math.pi**2/(4*dmin(n)): opens+=1
        else: T[n]=int(tt)
    def Phi(n):
        t=T.get(n)
        if t is None: return None
        pol=[a for a in As[t] if a>0]; return min(pol) if pol else None
    sc=[n for n in ns if T[n] is not None and T[n]>=2 and n in As[T[n]]]
    cyc=0
    for a in ns:
        if T[a] is None or T[a]<2 or a in sc: continue
        for b in As[T[a]]:
            if b>0 and b!=a and T.get(b) is not None and T[b]>=2 and b not in sc and a in As[T[b]]: cyc+=1
    nc=None; sc_slope=None
    for u,v in zip(ns,ns[1:]):
        pu,pv=Phi(u),Phi(v)
        if pu is None or pv is None: continue
        if (pu-u)==0 or (pu-u)*(pv-v)<0:
            nc=(u+v)/2 if (pu-u)!=0 else u; 
            # slope across the crossing, using neighbours of u and v
            i=ns.index(u); a=ns[i-1] if i>0 else u; b=ns[i+2] if i+2<len(ns) else v
            pa,pb=Phi(a),Phi(b)
            sc_slope=((pb-pa)/(b-a)) if (pa is not None and pb is not None) else (pv-pu)/(v-u)
            break
    status='MISS'; slope=None
    if len(sc)==1 and cyc==0:
        n0=sc[0]; i=ns.index(n0); nb=[m for m in (ns[i-1] if i>0 else None, ns[i+1] if i+1<len(ns) else None) if m is not None and Phi(m) is not None]
        if len(nb)==2: slope=(Phi(nb[1])-Phi(nb[0]))/(nb[1]-nb[0])
        elif len(nb)==1: slope=(Phi(nb[0])-Phi(n0))/(nb[0]-n0)
        if slope is None: status='EDGE'
        else:
            conv=True
            for n in ns:
                cur=n
                for _ in range(60):
                    p=Phi(cur)
                    if p is None or p not in T: cur=None; break
                    cur=p
                if cur is not None and cur!=n0: conv=False; break
            status='HIT' if (abs(slope)<1 and conv) else ('MISS' if abs(slope)>1 else 'EDGE')
    if status=='MISS' and len(sc)==0 and opens>0: status='OPEN'
    return dict(status=status,sc=sc[:5],nsc=len(sc),cyc=cyc,slope=slope,nc=nc,s_c=sc_slope,modes=modes,open=opens,Tstar=(T[sc[0]] if len(sc)==1 else None))
if __name__=="__main__":
    out={}
    for reading in ['W','I']:
        for rn,rnd in [('floor',math.floor),('ceil',math.ceil)]:
            for cfg in CFG:
                for x in XS:
                    for y in YS:
                        for s in C.SIG:
                            out['%s|%s|%s|%g|%g|%g'%(reading,rn,cfg,x,y,s)]=cell(cfg,s,x,y,reading,rnd)
        print('reading',reading,'done',flush=True)
    json.dump(out,open('sh_read_cells.json','w'),default=str)
    for reading in ['W','I']:
      for rn in ['floor','ceil']:
        tot={}
        for k,v in out.items():
            r,rr,cfg=k.split('|')[:3]
            if r==reading and rr==rn and cfg in SCORED: tot[v['status']]=tot.get(v['status'],0)+1
        perxy=[]
        for x in XS:
            for y in YS:
                st=[out['%s|%s|%s|%g|%g|%g'%(reading,rn,c,x,y,s)]['status'] for c in SCORED for s in C.SIG]
                perxy.append('MISS' if 'MISS' in st else ('HIT' if all(z=='HIT' for z in st) else 'OPEN'))
        print('=== reading %s rounding %s: cells'%(reading,rn),tot,' per-(x,y):',{k:perxy.count(k) for k in set(perxy)})
        if rn=='floor':
            for cfg in ['F-M3h','O']:
                for y in YS:
                    for x in XS:
                        row=[out['%s|%s|%s|%g|%g|%g'%(reading,rn,cfg,x,y,s)] for s in C.SIG]
                        print('  %s y=%g x=%-6g %s n*=%s nc=%s'%(cfg,y,x,''.join(r['status'][0] for r in row),[r['sc'][0] if r['nsc']==1 else r['nsc'] for r in row],[r['nc'] for r in row]))
