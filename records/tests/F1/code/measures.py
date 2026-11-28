"""Build firm-level predictors (all from facts filed <= 2019-12-31). No outcome data used."""
import json, numpy as np, pandas as pd, datetime as dt, warnings
import statsmodels.api as sm
warnings.filterwarnings('ignore')
Q=lambda y,q: y*4+(q-1)
import sys
COH=sys.argv[1] if len(sys.argv)>1 else 'C2'
Y={'C1':2014,'C2':2019}[COH]
Q_START=Q(2009,1); Q_END=Q(Y,3)        # tau window: all quarters 2009Q1..cutoff-year Q3
S_START=Q(Y-3,4)                        # sigma: 4-quarter $ changes over the last 12 quarters (Y-3 Q4 .. Y Q3)
B_DATE_MAX=f'{Y}-09-30'
TAU_MIN,TAU_MAX=1.0,20.0   # tau = 1 + mean adjustment lag (quarters); 1 = full adjustment within the shock quarter

def ecm_tau(lnR,lnC,qs,drop=False):
    """Huber-robust ECM: dlnC_t = a_q + g dlnR_t [+ gd*D_t*dlnR_t] + th*(lnC_{t-1}-lnR_{t-1}).
    lam=-th; tau = (1-impact)/lam quarters (mean adjustment lag), clipped to [TAU_MIN,TAU_MAX]."""
    rows=[]
    for i in range(1,len(qs)):
        if qs[i]-qs[i-1]!=1: continue
        dR=lnR[i]-lnR[i-1]; dC=lnC[i]-lnC[i-1]; gap=lnC[i-1]-lnR[i-1]
        rows.append((qs[i]%4,dC,dR,gap))
    if len(rows)<16: return None
    a=np.array(rows)
    X=np.column_stack([np.ones(len(a)),(a[:,0]==1),(a[:,0]==2),(a[:,0]==3),a[:,2]]+([np.minimum(a[:,2],0)] if drop else [])+[a[:,3]]).astype(float)
    y=a[:,1]
    try:
        f=sm.RLM(y,X,M=sm.robust.norms.HuberT()).fit()
    except Exception: return None
    b=f.params
    g=b[4]; gd=b[5] if drop else 0.0; th=b[-1]
    if drop and (np.sum(a[:,2]<0)<6): return None
    impact=g+gd if drop else g
    lam=-th
    if lam<=0: tau=TAU_MAX
    else: tau=1+max(0.0,1-impact)/lam
    return float(np.clip(tau,TAU_MIN,TAU_MAX)), float(impact), float(lam), len(a)

def latest_instant(dct, maxdate=B_DATE_MAX):
    ks=[k for k in dct if k<=maxdate]
    if not ks: return None,None
    k=max(ks); return k,dct[k]

def build(rec):
    R={int(k):v for k,v in rec['R'].items()}; O={int(k):v for k,v in rec['O'].items()}; C={int(k):v for k,v in rec['C'].items()}
    qs=[q for q in sorted(R) if Q_START<=q<=Q_END]
    cost={}
    for q in qs:
        if q in O: cost[q]=R[q]-O[q]
        elif q in C: cost[q]=C[q]
    qq=[q for q in qs if q in cost and R[q]>0 and cost[q]>0]
    out=dict(cik=rec['cik'],name=rec['name'],lastfiled=rec['lastfiled'],n_q=len(qq))
    if len(qq)<17: return out
    lnR=np.log([R[q] for q in qq]); lnC=np.log([cost[q] for q in qq])
    t=ecm_tau(lnR,lnC,qq)
    if t: out.update(tau=t[0],impact=t[1],lam=t[2],n_ecm=t[3])
    td=ecm_tau(lnR,lnC,qq,drop=True)
    if td: out.update(tau_drop=td[0])
    # split-half reliability pieces (pre-outcome only)
    mid=qq[len(qq)//2]; h1=[i for i,q in enumerate(qq) if q<mid]; h2=[i for i,q in enumerate(qq) if q>=mid]
    for nm,idx in (('tau_h1',h1),('tau_h2',h2)):
        if len(idx)>=9:
            r=ecm_tau_small(lnR[idx],lnC[idx],[qq[i] for i in idx])
            if r: out[nm]=r
    # sigma: SD of 4-quarter revenue changes in $ / 2, quarters 2015Q1..2019Q3
    d4=[R[q]-R[q-4] for q in sorted(R) if S_START<=q<=Q_END and (q-4) in R]
    out['n_sig']=len(d4)
    if len(d4)>=10: out['sigma']=float(np.std(d4,ddof=1)/2)
    rec4=[R[q] for q in range(Q(Y-1,4),Q(Y,3)+1) if q in R]
    out['rev_q_mean']=float(np.mean(rec4)) if len(rec4)==4 else np.nan
    out['last_rev_q']=max(R) if R else None
    # buffer
    inst=rec['inst']
    cd,cash=latest_instant({k:list(v.values())[0] for k,v in inst['cash'].items()})
    out['cash_date']=cd; out['cash']=cash
    if cd:
        sti=inst['sti'].get(cd,{}); out['sti']=float(sum(sti.values())) if sti else 0.0
        # undrawn credit: latest value dated within 365 days before cash date
        lk=[k for k in inst['loc'] if k<=cd and (dt.date.fromisoformat(cd)-dt.date.fromisoformat(k)).days<=365]
        out['loc']=float(list(inst['loc'][max(lk)].values())[0]) if lk else 0.0
        out['loc_reported']=int(bool(lk))
        a=inst['assets'].get(cd); out['assets']=float(list(a.values())[0]) if a else np.nan
        l=inst['liab'].get(cd); out['liab']=float(list(l.values())[0]) if l else np.nan
    # trailing 4Q operating income
    oi4=[R[q]-cost[q] for q in range(Q(Y-1,4),Q(Y,3)+1) if q in cost]
    out['oi4']=float(sum(oi4)) if len(oi4)==4 else np.nan
    return out

def ecm_tau_small(lnR,lnC,qs):
    rows=[]
    for i in range(1,len(qs)):
        if qs[i]-qs[i-1]!=1: continue
        rows.append((qs[i]%4,lnC[i]-lnC[i-1],lnR[i]-lnR[i-1],lnC[i-1]-lnR[i-1]))
    if len(rows)<8: return None
    a=np.array(rows)
    X=np.column_stack([np.ones(len(a)),(a[:,0]==1),(a[:,0]==2),(a[:,0]==3),a[:,2],a[:,3]]).astype(float)
    try: b=sm.RLM(a[:,1],X,M=sm.robust.norms.HuberT()).fit().params
    except Exception: return None
    lam=-b[-1]; tau=TAU_MAX if lam<=0 else 1+max(0.0,1-b[4])/lam
    return float(np.clip(tau,TAU_MIN,TAU_MAX))

if __name__=='__main__':
    from multiprocessing import Pool
    recs=(json.loads(l) for l in open(f'<local>/gtao/tests/F1/data/extract_{COH}.jsonl'))
    with Pool(6) as p: rows=p.map(build,list(recs),chunksize=50)
    df=pd.DataFrame(rows)
    df['B']=df['cash'].fillna(0)+df['sti'].fillna(0)+df['loc'].fillna(0)
    df['cohort']=COH
    df.to_csv(f'<local>/gtao/tests/F1/data/measures_{COH}.csv',index=False)
    print(len(df), df[['tau','tau_drop','sigma','B','assets']].notna().sum().to_dict())
