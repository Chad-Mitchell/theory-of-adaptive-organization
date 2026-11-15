import json, re, math, random, collections, datetime as dt
import numpy as np
from zoneinfo import ZoneInfo
import statsmodels.api as sm
NY=ZoneInfo('America/New_York')
J=[json.loads(l) for l in open('/workspace/looper/store/journal.jsonl')]
def T(s):
    d=dt.datetime.fromisoformat(s)
    if d.tzinfo is None: d=d.replace(tzinfo=NY)
    return d
CUT=T('2026-11-15T08:00:00-05:00')
ACE=('review','routine','eval','research')
by=collections.defaultdict(list)
for j in J:
    if j['id']=='morning-returns': continue
    by[j['id']].append(j)
TERM={'done','cancelled'}
def days(a,b): return (b-a).total_seconds()/86400
def atom_events(vs, upto=CUT):
    v1=vs[0]; t0=T(v1['at'])
    end=upto; term=None
    for v in vs:
        if v['status'] in TERM and T(v['at'])<=upto: term=T(v['at']); break
    if term: end=min(end,term)
    ev=[t0]
    for v in vs[1:]:
        if v['from'].startswith(ACE): continue
        t=T(v['at'])
        if t>end or t>upto: continue
        if days(ev[-1],t)*24*60<60: continue
        ev.append(t)
    return t0,end,ev,term
def stakes(v):
    s=(v['id']+' '+' '.join(v.get('cues') or [])+' '+(v.get('why') or '')).lower()
    hi='bill pay nelnet loan tax insur bank card hours invoice medical doctor dentist appointment health vitamin school pickup dogwood half-day deadline renew registration refund'.split()
    lo='idea hypothes research theory readme looper gtao adaptive bet explore someday docuseries brainstorm model'.split()
    if any(k in s for k in hi): return 3
    if any(k in s for k in lo): return 1
    return 2
def latest(vs, upto):
    c=[v for v in vs if T(v['at'])<=upto]; return c[-1] if c else None
out={}
rng=np.random.default_rng(20261115)
# ---------- P1 ----------
cvs=[];ats=[]
for i,vs in by.items():
    t0,end,ev,term=atom_events(vs)
    if len(ev)>=3:
        iv=np.diff([e.timestamp() for e in ev]); cvs.append(iv.std()/iv.mean()); ats.append((ev[0].timestamp(),ev[-1].timestamp(),len(ev)))
S=float(np.median(cvs)); null=[]
for _ in range(10000):
    c=[]
    for a,b,n in ats:
        x=np.sort(np.concatenate([[a,b],rng.uniform(a,b,n-2)])); iv=np.diff(x); c.append(iv.std()/iv.mean())
    null.append(np.median(c))
null=np.array(null)
out['P1']=dict(n_atoms=len(cvs),S_obs=S,null_p2_5=float(np.percentile(null,2.5)),null_p50=float(np.median(null)),null_p97_5=float(np.percentile(null,97.5)),p_upper=float((null>=S).mean()))
# P1b daily panel
rows=[]
for i,vs in by.items():
    t0,end,ev,term=atom_events(vs)
    d0=t0.astimezone(NY).date(); dE=end.astimezone(NY).date()
    evd=sorted(set(e.astimezone(NY).date() for e in ev))
    last=d0; d=d0+dt.timedelta(1)
    while d<=dE:
        hit=d in evd
        rows.append((i,(d-last).days,int(hit)))
        if hit: last=d
        d+=dt.timedelta(1)
X=np.log([r[1] for r in rows]); y=np.array([r[2] for r in rows])
m=sm.Logit(y,sm.add_constant(X)).fit(disp=0)
ids=sorted(set(r[0] for r in rows)); idx=collections.defaultdict(list)
for k,r in enumerate(rows): idx[r[0]].append(k)
bs=[]
for _ in range(1000):
    pick=rng.choice(len(ids),len(ids)); ks=np.concatenate([idx[ids[p]] for p in pick])
    try: bs.append(sm.Logit(y[ks],sm.add_constant(X[ks])).fit(disp=0).params[1])
    except Exception: pass
out['P1b']=dict(n_atom_days=len(rows),events=int(y.sum()),slope=float(m.params[1]),ci=[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))])
# ---------- P2 ----------
mr=[j for j in J if j['id']=='morning-returns'][-1]['text']
ent=re.split(r'(?=20\d\d-11-1[1-5] \()',mr)
surf=collections.Counter(); runs=0
for e in ent:
    m_=re.match(r'(20\d\d-11-1[1-5])',e)
    if not m_: continue
    runs+=1; got=set()
    for br in re.findall(r'\[([^\]]+)\]',e):
        for tok in re.split(r'[,+;]',br):
            tok=tok.strip()
            if tok in by: got.add(tok)
    for g in got: surf[g]+=1
P2cut=T('2026-11-10T23:59:00-05:00')
def window_in(v,lo,hi):
    w=v.get('window')
    if not w: return 0
    d=dt.date.fromisoformat(w[:10]); rep=v.get('repeat')
    cands=[d]
    if rep=='weekly':
        k=d
        while k<hi: k+=dt.timedelta(7); cands.append(k)
    if rep=='monthly' or rep=='yearly':
        for y_ in (2026,2027):
            for mo in range(1,13):
                try: cands.append(d.replace(year=y_,month=mo) if rep=='monthly' else d.replace(year=y_))
                except ValueError: pass
    return int(any(lo<=c<=hi for c in cands))
P2rows=[]
for i,vs in by.items():
    if T(vs[0]['at'])>P2cut: continue
    t0,end,ev,term=atom_events(vs,P2cut)
    if term: continue
    lv=latest(vs,P2cut)
    lam=(len(ev)-1+0.5)/max(days(t0,end),0.5)
    rec=max(days(T(lv['at']),P2cut),0.1)
    P2rows.append(dict(id=i,att=surf.get(i,0),lam=lam,W=stakes(lv),D=window_in(lv,dt.date(2026,11,11),dt.date(2026,11,17)),rec=rec))
A=np.array([r['att'] for r in P2rows]); LL=np.log([r['lam'] for r in P2rows]); LW=np.log([r['W'] for r in P2rows]); D=np.array([r['D'] for r in P2rows]); LR=np.log([r['rec'] for r in P2rows])
def pois(Xs):
    Xm=sm.add_constant(np.column_stack(Xs)) if Xs else np.ones((len(A),1))
    return sm.GLM(A,Xm,family=sm.families.Poisson()).fit()
mods={'U':[], 'D':[D], 'R':[LR], 'G':[LL,LW], 'G+D':[LL,LW,D]}
aic={k:float(pois(v).aic) for k,v in mods.items()}
g=pois([LL,LW]); bs=[]
for _ in range(2000):
    k=rng.choice(len(A),len(A))
    try:
        r=sm.GLM(A[k],sm.add_constant(np.column_stack([LL[k],LW[k]])),family=sm.families.Poisson()).fit(); bs.append(r.params[1:3])
    except Exception: pass
bs=np.array(bs)
gd=pois([LL,LW,D])
out['P2']=dict(n_atoms=len(A),runs=runs,atoms_surfaced=int((A>0).sum()),total_surfacings=int(A.sum()),drift_elast=float(g.params[1]),drift_ci=[float(np.nanpercentile(bs[:,0],2.5)),float(np.nanpercentile(bs[:,0],97.5))],stakes_elast=float(g.params[2]),stakes_ci=[float(np.nanpercentile(bs[:,1],2.5)),float(np.nanpercentile(bs[:,1],97.5))],aic=aic,GD_params=[float(x) for x in gd.params],GD_p=[float(x) for x in gd.pvalues],
  surf_rate_by_D={int(k):float(A[D==k].mean()) for k in (0,1)}, n_D1=int(D.sum()))
# ---------- P3 ----------
SPLIT=T('2026-11-01T00:00:00-04:00')
P3=[]
for i,vs in by.items():
    if T(vs[0]['at'])>=SPLIT: continue
    t0,end,ev,term=atom_events(vs)
    if term and term<SPLIT: continue
    e1=[e for e in ev[1:] if e<SPLIT]; e2=[e for e in ev[1:] if e>=SPLIT]
    L1=max(days(t0,SPLIT),0.5); L2=max(days(SPLIT,end),0.5)
    lv=latest(vs,SPLIT); last=max([T(v['at']) for v in vs if T(v['at'])<SPLIT])
    P3.append(dict(id=i,lam1=(len(e1)+0.5)/L1,r1=len(e1)/L1,r2=len(e2)/L2,e2=[days(SPLIT,e) for e in e2],L2=L2,W=stakes(lv),rec=max(days(last,SPLIT),0.1)))
from scipy.stats import spearmanr
r1=np.array([p['r1'] for p in P3]); r2=np.array([p['r2'] for p in P3])
rho=spearmanr(r1,r2).correlation; bsr=[]
for _ in range(2000):
    k=rng.choice(len(P3),len(P3)); bsr.append(spearmanr(r1[k],r2[k]).correlation)
P3a=dict(n_atoms=len(P3),rho=float(rho),ci=[float(np.nanpercentile(bsr,2.5)),float(np.nanpercentile(bsr,97.5))],atoms_with_p2_events=int(sum(1 for p in P3 if p['e2'])),p2_events=int(sum(len(p['e2']) for p in P3)))
def weights(pol,P):
    lam=np.array([p['lam1'] for p in P]); W=np.array([p['W'] for p in P]); rec=np.array([p['rec'] for p in P])
    return {'U':np.ones(len(P)),'G':np.sqrt(lam*W),'L':lam*W,'S':W.astype(float),'R':1/rec}[pol]
def loss(pol,P,budget_days,phases):
    w=weights(pol,P); L2=np.array([p['L2'] for p in P])
    total_checks=(L2/budget_days).sum()
    f=w/ (w*L2).sum()*total_checks  # checks per day per atom
    T_=1/f; num=0; den=0
    per=np.zeros(len(P)); perw=np.zeros(len(P))
    for a,p in enumerate(P):
        for e in p['e2']:
            ph=phases[a]*T_[a]
            # next check time >= e : checks at ph + k*T
            k=np.ceil((e-ph)/T_[a]); nxt=ph+np.maximum(k,0)*T_[a]
            lag=np.mean(nxt-e); per[a]+=p['W']*lag; perw[a]+=p['W']
    return per,perw
def P3b(budget,ndraw=200):
    ph=rng.uniform(0,1,(ndraw,len(P3)))
    res={}
    for pol in 'UGLSR':
        per=np.zeros(len(P3)); perw=None
        for d in range(ndraw):
            a,b=loss(pol,P3,budget,ph[d]); per+=a/ndraw; perw=b
        res[pol]=(per,perw)
    pts={k:float(v[0].sum()/v[1].sum()) for k,v in res.items()}
    ratios={}
    for k in 'ULSR':
        bsr=[]
        for _ in range(2000):
            s=rng.choice(len(P3),len(P3))
            gG=res['G'][0][s].sum()/res['G'][1][s].sum(); gK=res[k][0][s].sum()/res[k][1][s].sum()
            bsr.append(gG/gK)
        ratios['G/'+k]=[float(pts['G']/pts[k]),float(np.percentile(bsr,2.5)),float(np.percentile(bsr,97.5))]
    return dict(loss_days=pts,ratios=ratios)
out['P3a']=P3a
out['P3b']={str(b):P3b(b) for b in (7,3,14)}
# ---------- P4a ----------
term_atoms=0; reopened=0
for i,vs in by.items():
    k=next((n for n,v in enumerate(vs) if v['status'] in TERM),None)
    if k is None: continue
    term_atoms+=1
    later=[v for v in vs[k+1:] if not v['from'].startswith(ACE) and days(T(vs[k]['at']),T(v['at']))*1440>=60]
    if later: reopened+=1
out['P4a']=dict(terminal_atoms=term_atoms,changed_after_terminal=reopened,frac=reopened/term_atoms if term_atoms else None)
# descriptive
allK=[];allL=[]
for i,vs in by.items():
    t0,end,ev,term=atom_events(vs); allK.append(len(ev)-1); allL.append(days(t0,end))
out['desc']=dict(atoms=len(by),versions=sum(len(v) for v in by.values()),ace_initiated_versions=sum(1 for v in sum(by.values(),[]) if v['from'].startswith(ACE)),change_events=int(sum(allK)),atom_days=float(sum(allL)),median_lambda=float(np.median([(k+0.5)/max(l,0.5) for k,l in zip(allK,allL)])),stakes_hist=dict(collections.Counter(stakes(v[-1]) for v in by.values())))
json.dump(out,open('/workspace/gtao/night2/SELF/results.json','w'),indent=1,default=str)
print(json.dumps(out,indent=1,default=str))
