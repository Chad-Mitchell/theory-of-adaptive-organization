#!/usr/bin/env python3
"""Independent referee re-implementation of MEASURE-SELF from PREREG text (not from analyze.py)."""
import json, re, collections, datetime as dt, numpy as np, statsmodels.api as sm
from zoneinfo import ZoneInfo
from scipy.stats import spearmanr
NY=ZoneInfo('America/New_York'); rng=np.random.default_rng(77)
rows=[json.loads(l) for l in open('/workspace/looper/store/journal.jsonl')]
def ts(s):
    d=dt.datetime.fromisoformat(s); return d if d.tzinfo else d.replace(tzinfo=NY)
CUT=ts('2026-11-15T08:00:00-05:00'); ACE=('review','routine','eval','research'); TERM={'done','cancelled'}
atoms=collections.OrderedDict()
for r in sorted(rows,key=lambda r:r['seq']):
    if r['id']!='morning-returns': atoms.setdefault(r['id'],[]).append(r)
D=lambda a,b:(b-a).total_seconds()/86400
def life(vs,upto):
    t0=ts(vs[0]['at']); term=next((ts(v['at']) for v in vs if v['status'] in TERM and ts(v['at'])<=upto),None)
    end=min(upto,term) if term else upto
    ev=[t0]
    for v in vs[1:]:
        if v['from'].startswith(ACE): continue
        t=ts(v['at'])
        if t<=t0 or t>end: continue
        if (t-ev[-1]).total_seconds()<3600: continue
        ev.append(t)
    return t0,end,ev,term
def W(v):
    s=(v['id']+' '+' '.join(v.get('cues') or [])+' '+(v.get('why') or '')).lower()
    if re.search('bill|pay|nelnet|loan|tax|insur|bank|card|hours|invoice|medical|doctor|dentist|appointment|health|vitamin|school|pickup|dogwood|half-day|deadline|renew|registration|refund',s): return 3
    if re.search('idea|hypothes|research|theory|readme|looper|gtao|adaptive|bet|explore|someday|docuseries|brainstorm|model',s): return 1
    return 2
OUT={}
Q=[];allev=[]
for i,vs in atoms.items():
    t0,end,ev,_=life(vs,CUT); allev+= [e.timestamp() for e in ev[1:]]
    if len(ev)>=3: Q.append(np.array([e.timestamp() for e in ev]))
cv=lambda x:(np.diff(x).std()/np.diff(x).mean())
S=np.median([cv(x) for x in Q])
def null(kind,K=4000):
    out=[]; allE=np.array(sorted(allev))
    for _ in range(K):
        c=[]
        for x in Q:
            a,b,n=x[0],x[-1],len(x)
            if kind=='uniform': mid=rng.uniform(a,b,n-2)
            elif kind=='uniform_mingap':
                for _t in range(200):
                    mid=rng.uniform(a,b,n-2); y=np.sort(np.r_[a,b,mid])
                    if np.diff(y).min()>=3600: break
            elif kind=='session':
                pool=np.unique(allE[(allE>a)&(allE<b)])
                mid=rng.uniform(a,b,n-2) if len(pool)<n-2 else rng.choice(pool,n-2,replace=False)
            c.append(cv(np.sort(np.r_[a,b,mid])))
        out.append(np.median(c))
    return np.percentile(out,[2.5,50,97.5]).tolist()
OUT['P1']={'n':len(Q),'S':float(S),'null_uniform':null('uniform'),'null_uniform_mingap60':null('uniform_mingap',1500),'null_session_schedule':null('session',1500)}
print('P1',OUT['P1'],flush=True)
P=[]
for i,vs in atoms.items():
    t0,end,ev,_=life(vs,CUT); d0=t0.astimezone(NY).date(); dE=end.astimezone(NY).date()
    evd={e.astimezone(NY).date() for e in ev[1:]}; last=d0; d=d0+dt.timedelta(1)
    while d<=dE:
        P.append((i,(d-last).days,int(d in evd),d))
        if d in evd: last=d
        d+=dt.timedelta(1)
x=np.log([p[1] for p in P]); y=np.array([p[2] for p in P])
m=sm.Logit(y,sm.add_constant(x)).fit(disp=0)
days=sorted({p[3] for p in P}); okd=sorted(d for d in days if sum(p[2] for p in P if p[3]==d)>0)
sel=np.array([p[3] in set(okd) for p in P])
Dm2=np.array([[p[3]==d for d in okd[1:]] for p in P],float)[sel]
m2=sm.Logit(y[sel],np.column_stack([np.ones(sel.sum()),x[sel],Dm2])).fit(disp=0,method='newton',maxiter=200)
OUT['P1b']={'n':len(P),'events':int(y.sum()),'slope':float(m.params[1]),'se':float(m.bse[1]),'slope_dayFE':float(m2.params[1]),'se_dayFE':float(m2.bse[1]),'event_days':len(okd),'calendar_days':len(days)}
print('P1b',OUT['P1b'],flush=True)
mr=[r for r in rows if r['id']=='morning-returns'][-1]['text']
chunks=re.split(r'(?=2026-11-1[1-5] \()',mr); att=collections.Counter(); nr=0
for c in chunks:
    if not re.match(r'2026-11-1[1-5]',c): continue
    nr+=1; s=set()
    for br in re.findall(r'\[([^\]]+)\]',c):
        for t in re.split(r'[,+;]',br):
            if t.strip() in atoms: s.add(t.strip())
    att.update(s)
C2=ts('2026-11-10T23:59:00-05:00')
def dl(v,lo=dt.date(2026,11,11),hi=dt.date(2026,11,17)):
    w=v.get('window')
    if not w: return 0
    d=dt.date.fromisoformat(w[:10]); rep=v.get('repeat'); c=[d]
    if rep=='weekly': c+=[d+dt.timedelta(7*k) for k in range(1,60)]
    if rep=='monthly': c+=[dt.date(y_,m_,d.day) for y_ in (2026,2027) for m_ in range(1,13) if d.day<=28]
    if rep=='yearly': c+=[d.replace(year=2026),d.replace(year=2027)]
    return int(any(lo<=z<=hi for z in c))
R2=[]
for i,vs in atoms.items():
    if ts(vs[0]['at'])>C2: continue
    t0,end,ev,term=life(vs,C2)
    if term: continue
    lv=[v for v in vs if ts(v['at'])<=C2][-1]
    R2.append((att[i],np.log((len(ev)-1+.5)/max(D(t0,end),.5)),np.log(W(lv)),dl(lv),np.log(max(D(ts(lv['at']),C2),.1)),i))
A=np.array([r[0] for r in R2],float); LL=np.array([r[1] for r in R2]); LW=np.array([r[2] for r in R2]); DD=np.array([r[3] for r in R2]); LR=np.array([r[4] for r in R2])
def g(*c): return sm.GLM(A,sm.add_constant(np.column_stack(c)) if c else np.ones((len(A),1)),family=sm.families.Poisson()).fit()
mG=g(LL,LW); bs=[]
for _ in range(2000):
    k=rng.integers(0,len(A),len(A))
    try: bs.append(sm.GLM(A[k],sm.add_constant(np.column_stack([LL[k],LW[k]])),family=sm.families.Poisson()).fit().params[1])
    except Exception: pass
mGD=g(LL,LW,DD); mGDR=g(LL,LW,DD,LR)
OUT['P2']={'runs':nr,'n':len(A),'surfaced':int((A>0).sum()),'tot':int(A.sum()),'drift_el':float(mG.params[1]),'ci':np.nanpercentile(bs,[2.5,97.5]).tolist(),
 'stakes_el':float(mG.params[2]),'aic':{'U':g().aic,'D':g(DD).aic,'R':g(LR).aic,'G':mG.aic,'G+D':mGD.aic,'G+D+R':mGDR.aic},
 'GD_drift':[float(mGD.params[1]),float(mGD.bse[1])],'GD_D':[float(mGD.params[3]),float(mGD.bse[3])],'GDR_drift':[float(mGDR.params[1]),float(mGDR.bse[1])],'n_D1':int(DD.sum()),
 'corr_logdrift_D':float(np.corrcoef(LL,DD)[0,1]),'corr_logdrift_logrecency':float(np.corrcoef(LL,LR)[0,1]),
 'pearson_dispersion':float(((A-mG.mu)**2/mG.mu).sum()/(len(A)-3))}
print('P2',OUT['P2'],flush=True)
SPL=ts('2026-11-01T00:00:00-04:00'); P3=[]
for i,vs in atoms.items():
    if ts(vs[0]['at'])>=SPL: continue
    t0,end,ev,term=life(vs,CUT)
    if term and term<SPL: continue
    e1=[e for e in ev[1:] if e<SPL]; e2=[D(SPL,e) for e in ev[1:] if e>=SPL]
    L1=max(D(t0,SPL),.5); L2=max(D(SPL,end),.5); lv=[v for v in vs if ts(v['at'])<SPL][-1]
    P3.append(dict(l1=(len(e1)+.5)/L1,r1=len(e1)/L1,r2=len(e2)/L2,e2=np.array(e2),L2=L2,W=W(lv),rec=max(D(max(ts(v['at']) for v in vs if ts(v['at'])<SPL),SPL),.1),n1=len(e1)))
r1=np.array([p['r1'] for p in P3]); r2=np.array([p['r2'] for p in P3])
rho=spearmanr(r1,r2).correlation; bb=[spearmanr(r1[k],r2[k]).correlation for k in (rng.integers(0,len(P3),len(P3)) for _ in range(2000))]
OUT['P3a']={'n':len(P3),'rho':float(rho),'ci':np.nanpercentile(bb,[2.5,97.5]).tolist(),'atoms_p1_events':int((r1>0).sum()),'atoms_p2_events':int((r2>0).sum()),'p2_events':int(sum(len(p['e2']) for p in P3))}
print('P3a',OUT['P3a'],flush=True)
def P3b(bud):
    lam=np.array([p['l1'] for p in P3]); Wt=np.array([p['W'] for p in P3]); rec=np.array([p['rec'] for p in P3]); L2=np.array([p['L2'] for p in P3])
    ne=np.array([len(p['e2']) for p in P3])
    pol={'U':np.ones(len(P3)),'G':np.sqrt(lam*Wt),'L':lam*Wt,'S':Wt*1.,'R':1/rec}; res={}
    for k,w in pol.items():
        f=w/(w*L2).sum()*(L2/bud).sum(); lag=0.5/f
        res[k]=(Wt*ne*lag, Wt*ne)
    pt={k:float(v[0].sum()/v[1].sum()) for k,v in res.items()}; rat={}
    for k in 'ULSR':
        b=[]
        for _ in range(2000):
            s=rng.integers(0,len(P3),len(P3)); den=res['G'][1][s].sum()
            if den==0: continue
            b.append((res['G'][0][s].sum()/den)/(res[k][0][s].sum()/res[k][1][s].sum()))
        rat['G/'+k]=[pt['G']/pt[k]]+np.percentile(b,[2.5,97.5]).tolist()
    return {'loss':pt,'ratios':rat}
OUT['P3b']={str(b):P3b(b) for b in (7,3,14)}
print('P3b',json.dumps(OUT['P3b']['7']),flush=True)
nt=ch=0
for i,vs in atoms.items():
    k=next((n for n,v in enumerate(vs) if v['status'] in TERM),None)
    if k is None: continue
    nt+=1; tk=ts(vs[k]['at'])
    if any((not v['from'].startswith(ACE)) and (ts(v['at'])-tk).total_seconds()>=3600 for v in vs[k+1:]): ch+=1
OUT['P4a']={'terminal':nt,'changed_after':ch}
print('P4a',OUT['P4a'])
json.dump(OUT,open('self_ref.json','w'),indent=1,default=float)
