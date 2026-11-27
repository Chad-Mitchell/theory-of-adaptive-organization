# SH-heat analysis per SELF_HORIZON §8.3-§8.7 (pre-statement hash in WORKLOG 14:25 ET).
import json, math, sys
import sh_heat_core as C
A=json.load(open("argmin_sets.json")); M=json.load(open("sh_heat_modes.json"))
CFG=['E-M3h','O','F-M3h','F-mixed','E-mixed']; NMAX=1201
def dmin(n):
    if n%2: return math.sin(math.pi/n)/math.cos(math.pi/(2*n))
    S=n//2; return math.sin(math.pi/n)/(math.cos(math.pi/n) if (1-S)%2 else 1.0)
def menu(cfg):
    if cfg.startswith('E'): return [n for n in range(4,NMAX+1,2)]
    if cfg=='O': return [n for n in range(3,NMAX+1,2)]
    return list(range(3,NMAX+1))
def mode_of(m):
    ch=m['check'] if m['logcheck'] is None else 0.0
    c={'keep':m['keep'],'check':ch,'fade':m['fade']}
    best=min(c.values()); tied=[k for k,v in c.items() if abs(v-best)<=1e-12*max(abs(best),1e-300)]
    return tied
def tau_of(n,s,x,ck):
    o=M['%d|%g'%(n,s)]; m=o['%g|%g'%(x,ck)]; tied=mode_of(m)
    taus={'keep':float('inf'),'check':float(m['s_star']),'fade':o['tau_fade']}
    md=min(tied,key=lambda k:taus[k])
    return md, taus[md], (md=='check' and m['s_star']>=C.SMAX), len(tied)>1
def cell(cfg,s,x,ck,rnd):
    As={int(k):v for k,v in A[cfg]['A'].items()}
    ns=menu(cfg); T={}; info={}; opens=[]; modes={'keep':0,'check':0,'fade':0}; ties=0
    for n in ns:
        md,tau,edge,tie=tau_of(n,s,x,ck); modes[md]+=1; ties+=tie
        if edge: opens.append(n); T[n]=None; continue
        if tau==float('inf'): T[n]=None; info[n]='kept'; continue
        t=rnd(tau)
        if t>400:
            if t>math.pi**2/(4*dmin(n)): T[n]=None; info[n]='excl'
            else: T[n]=None; opens.append(n)
        else: T[n]=int(t)
    def Phi(n):
        t=T.get(n)
        if t is None: return None
        pol=[a for a in As[t] if a>0]
        return min(pol) if pol else None
    sc=[n for n in ns if T[n] is not None and T[n]>=2 and n in As[T[n]]]
    vac=sum(1 for n in ns if T[n]==1)
    cyc=set()
    for a in ns:
        if T[a] is None or T[a]<2 or a in sc: continue
        for b in As[T[a]]:
            if b>0 and b!=a and b in T and T[b] is not None and T[b]>=2 and b not in sc and a in As[T[b]]: cyc.add(tuple(sorted((a,b))))
    # crossings
    fin=[n for n in ns if Phi(n) is not None]
    cross=[]
    for u,v in zip(ns,ns[1:]):
        pu,pv=Phi(u),Phi(v)
        if pu is None or pv is None: continue
        if (pu-u)*(pv-v)<0: cross.append((u,v,(pv-pu)/(v-u)))
    att=None; slope=None
    if len(sc)==1:
        ns_=ns; i=ns_.index(sc[0])
        if 0<i<len(ns_)-1:
            a,b=ns_[i-1],ns_[i+1]; pa,pb=Phi(a),Phi(b)
            if pa is not None and pb is not None: slope=(pb-pa)/(b-a)
        # iteration
        ends={}
        for n in ns:
            cur=n; ok=True
            for _ in range(60):
                p=Phi(cur)
                if p is None or p not in T: ok=False; break
                cur=p
            ends[cur if ok else 'left']=ends.get(cur if ok else 'left',0)+1
        conv=all(k==sc[0] or k=='left' for k in ends)
        att=(slope is not None and abs(slope)<1 and conv)
        rep=(slope is not None and abs(slope)>1)
    else: ends=None; rep=False
    # triviality: T constant on n*+-2
    triv=None
    if len(sc)==1:
        nb=[m for m in ns if abs(m-sc[0])<=2]
        triv=len(set(T[m] for m in nb))==1
    if opens and not sc: status='OPEN'
    elif len(sc)==1 and not cyc and att: status='HIT'
    elif cyc or len(sc)!=1 or rep: status='MISS'
    else: status='OPEN' if opens else 'UNCLASSIFIED'
    return dict(status=status,sc=sc,cyc=sorted(cyc)[:6],ncyc=len(cyc),slope=slope,att=att,ends=ends,triv=triv,modes=modes,ties=ties,
                open=len(opens),vac=vac,Tstar=(T[sc[0]] if len(sc)==1 else None),cross=cross[:6],ncross=len(cross),
                Tsmall={n:T[n] for n in ns[:6]})
if __name__=="__main__":
    out={}
    for ck in C.CK:
        for rn,rnd in [('floor',math.floor),('ceil',math.ceil)]:
            for cfg in CFG:
                for x in C.XS:
                    for s in C.SIG:
                        out['%s|%g|%s|%g|%g'%(rn,ck,cfg,x,s)]=cell(cfg,s,x,ck,rnd)
    json.dump(out,open('sh_heat_cells.json','w'),default=str)
    # summaries
    for ck in C.CK:
      for rn in ['floor','ceil']:
        print('=== c_K=%g rounding=%s'%(ck,rn))
        for cfg in CFG:
            print(' --',cfg)
            for x in C.XS:
                row=[out['%s|%g|%s|%g|%g'%(rn,ck,cfg,x,s)] for s in C.SIG]
                st=''.join({'HIT':'H','MISS':'M','OPEN':'O','UNCLASSIFIED':'U'}[r['status']] for r in row)
                nst=[(r['sc'][0] if len(r['sc'])==1 else len(r['sc'])) for r in row]
                print('   x=%-6g %s  n*/#sc=%s'%(x,st,nst))
