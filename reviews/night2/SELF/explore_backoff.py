# POST-LOCK exploratory: dynamic geometric back-off after each change (regime-B design) vs uniform, budget-matched
import numpy as np, json, datetime as dt
src=open('analyze.py').read()
exec(src.split('# ---------- P1 ----------')[0])
SPLIT=T('2026-11-01T00:00:00-04:00')
P=[]
for i,vs in by.items():
    if T(vs[0]['at'])>=SPLIT: continue
    t0,end,ev,term=atom_events(vs)
    if term and term<SPLIT: continue
    last=max([e for e in ev if e<SPLIT]); e2=[days(SPLIT,e) for e in ev if e>=SPLIT]
    P.append(dict(last=days(SPLIT,last),e2=e2,L2=max(days(SPLIT,end),0.5),W=stakes(latest(vs,SPLIT))))
def backoff(tau0s,base=2.0):
    checks=0; num=0; den=0
    for p,tau0 in zip(P,tau0s):
        anchors=[p['last']]+p['e2']; L2=p['L2']
        for k,a in enumerate(anchors):
            nxt=anchors[k+1] if k+1<len(anchors) else None
            stop=nxt if nxt is not None else L2
            t=a+tau0; first_after=None
            while True:
                if t>=0 and t<=L2: checks+=1
                if nxt is not None and t>=nxt and first_after is None: first_after=t; break
                if t>stop: break
                t=a+tau0*(base**(np.log(max((t-a)/tau0,1))/np.log(base)+1))
            if nxt is not None:
                num+=p['W']*(first_after-nxt); den+=p['W']
    return checks,num/den
def uniform(budget_days):
    tot=sum(p['L2'] for p in P)/budget_days; Tn=sum(p['L2'] for p in P)/tot
    num=den=0
    for p in P:
        for e in p['e2']: num+=p['W']*Tn/2; den+=p['W']
    return tot,num/den
res={}
for bd in (3,7,14):
    target,uL=uniform(bd)
    lo,hi=0.01,100
    for _ in range(60):
        mid=np.sqrt(lo*hi); c,_=backoff([mid]*len(P))
        if c>target: lo=mid
        else: hi=mid
    c,bL=backoff([hi]*len(P))
    # stakes-weighted variant tau0 ∝ 1/W
    lo2,hi2=0.01,100
    for _ in range(60):
        mid=np.sqrt(lo2*hi2); c2,_=backoff([mid*3/p['W'] for p in P])
        if c2>target: lo2=mid
        else: hi2=mid
    c2,bsL=backoff([hi2*3/p['W'] for p in P])
    res[bd]=dict(budget_checks=round(target,1),uniform_loss=uL,backoff_checks=c,backoff_tau0_days=hi,backoff_loss=bL,ratio_backoff_over_uniform=bL/uL,backoffW_checks=c2,backoffW_loss=bsL,ratio_backoffW_over_uniform=bsL/uL)
print(json.dumps(res,indent=1)); json.dump(res,open('explore_backoff.json','w'),indent=1)
