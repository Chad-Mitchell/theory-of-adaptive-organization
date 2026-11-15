"""F1 preregistered analysis. Input: data/analysis_dataset.csv with predictor columns and outcome
columns D (bankruptcy 8-K Item 1.03 in risk window), T (days from 2020-01-01 to event/censor),
D2 (secondary distress). Usage: python analyze.py [dataset.csv] [out.json]"""
import sys, json, numpy as np, pandas as pd, warnings
import statsmodels.formula.api as smf
from lifelines import CoxPHFitter
from lifelines.statistics import proportional_hazard_test
from scipy import stats
warnings.filterwarnings('ignore')
SEED=20261114; NBOOT=int(__import__("os").environ.get("NBOOT","1000"))
path=sys.argv[1] if len(sys.argv)>1 else '/workspace/gtao/tests/F1/data/analysis_dataset.csv'
outp=sys.argv[2] if len(sys.argv)>2 else '/workspace/gtao/tests/F1/results.json'
df=pd.read_csv(path)
df['ls']=np.log(df.sigma); df['lb']=np.log(df.B); df['ltau']=np.log(df.tau); df['la']=np.log(df.assets)
df['lsb']=df.ls-df.lb
R={'n':int(len(df)),'events':int(df.D.sum()),'event_rate':float(df.D.mean())}

POOLED=df.cohort.nunique()>1
def cox(d,cols,dur='T',ev='D',robust=True):
    # pooled cohorts: stratified baseline by cohort, firm-clustered robust SEs (lifelines: Efron ties)
    c=CoxPHFitter()
    if POOLED and 'cohort' in d:
        dd=d[cols+[dur,ev,'cohort','cik']].copy()
        if robust: c.fit(dd,dur,ev,strata=['cohort'],cluster_col='cik')
        else: c.fit(dd.drop(columns='cik'),dur,ev,strata=['cohort'])
    else: c.fit(d[cols+[dur,ev]],dur,ev)
    return c

# ---- Primary 1: index restriction
P1=['ls','lb','ltau','la']
c=cox(df,P1)
c_nr=cox(df,P1,robust=False)
b=c.params_; ci=c.confidence_intervals_
R['P1']={k:{'beta':float(b[k]),'lo':float(ci.loc[k].iloc[0]),'hi':float(ci.loc[k].iloc[1]),'p':float(c.summary.loc[k,'p'])} for k in P1}
rB=b['lb']/b['ls']; rT=b['ltau']/b['ls']
df['idx']=df.ls-df.lb+0.5*df.ltau
cr=cox(df,['idx','la'],robust=False)
LR=2*(c_nr.log_likelihood_-cr.log_likelihood_); pLR=float(stats.chi2.sf(LR,2))
R['P1'].update(rB=float(rB),rT=float(rT),LR=float(LR),pLR=pLR,idx_beta=float(cr.params_['idx']))
rng=np.random.default_rng(SEED); bs=[]
ciks=df.cik.unique(); grp={k:v for k,v in df.groupby('cik').indices.items()}
for i in range(NBOOT):   # firm-cluster bootstrap
    pick=rng.choice(ciks,len(ciks)); idx=np.concatenate([grp[k] for k in pick])
    s=df.iloc[idx].copy(); s['cik']=np.repeat(np.arange(len(pick)),[len(grp[k]) for k in pick])
    try:
        cb=cox(s,P1,robust=False).params_; bs.append((cb['lb']/cb['ls'],cb['ltau']/cb['ls'],cb['ltau']))
    except Exception: pass
bs=np.array(bs)
R['P1']['rB_ci']=[float(np.percentile(bs[:,0],2.5)),float(np.percentile(bs[:,0],97.5))]
R['P1']['rT_ci']=[float(np.percentile(bs[:,1],2.5)),float(np.percentile(bs[:,1],97.5))]
R['P1']['nboot_ok']=int(len(bs))
try: R['P1']['schoenfeld_min_p']=float(proportional_hazard_test(c_nr,df[P1+['T','D','cohort']] if POOLED else df[P1+['T','D']],time_transform='rank').p_value.min())
except Exception as e: R['P1']['schoenfeld_min_p']=None

# ---- Primary 2: absolute-scale interaction (LPM, HC1)
d=df.copy()
for v in ['ltau','lsb','la']: d['c_'+v]=d[v]-d[v].mean()
FE=' + C(cohort)' if POOLED else ''
P2F=' + I(c_lsb**2) + I(c_la**2) + I(c_ltau**2) + c_la:c_lsb + c_ltau:c_la'   # flexible controls: base spec had 10% false-positive rate in null simulation (power/p2_typeI.py)
m=smf.ols('D ~ c_ltau*c_lsb + c_la'+P2F+FE,d).fit(cov_type='cluster',cov_kwds={'groups':d.cik})
k='c_ltau:c_lsb'
R['P2']={'inter':float(m.params[k]),'lo':float(m.conf_int().loc[k,0]),'hi':float(m.conf_int().loc[k,1]),'p':float(m.pvalues[k]),
         'ltau':float(m.params['c_ltau']),'lt_lo':float(m.conf_int().loc['c_ltau',0]),'lt_hi':float(m.conf_int().loc['c_ltau',1])}
# descriptive terciles
d['terc']=pd.qcut(d.lsb,3,labels=False); med=d.ltau.median(); tr=[]
for t in range(3):
    s=d[d.terc==t]; hi=s[s.ltau>med].D; lo=s[s.ltau<=med].D
    rd=hi.mean()-lo.mean(); se=np.sqrt(hi.var(ddof=1)/len(hi)+lo.var(ddof=1)/len(lo))
    tr.append({'tercile':t,'n':int(len(s)),'rate':float(s.D.mean()),'rd':float(rd),'lo':float(rd-1.96*se),'hi':float(rd+1.96*se),'flag_gt50':bool(s.D.mean()>0.5)})
R['P2']['terciles']=tr
# P2 base spec (reported, non-decisive)
mb=smf.ols('D ~ c_ltau*c_lsb + c_la'+FE,d).fit(cov_type='cluster',cov_kwds={'groups':d.cik})
R['P2']['base_spec']=[float(mb.params[k]),float(mb.conf_int().loc[k,0]),float(mb.conf_int().loc[k,1])]
# shape check (labelled, not support)
d['cx']=d.c_ltau*d.c_lsb; ci3=cox(d,['c_ltau','c_lsb','cx','c_la'])
R['shape_cox_inter']={'beta':float(ci3.params_['cx']),'lo':float(ci3.confidence_intervals_.loc['cx'].iloc[0]),'hi':float(ci3.confidence_intervals_.loc['cx'].iloc[1])}

# ---- Verdict
P=R['P1']; bs_=P
K1=(P['ltau']['beta']<=0) or (P['rT_ci'][1]<0.25 or P['rT_ci'][0]>1.0) or \
   (P['ls']['lo']>0 and P['ltau']['hi']<0.5*P['ls']['beta'])
K2=(P['rB_ci'][1]<-2 or P['rB_ci'][0]>-0.5) or (P['pLR']<0.01 and not(-2<=P['rB']<=-0.5 and 0.25<=P['rT']<=1.0))
K3=R['P2']['hi']<=0
hit=(not(K1 or K2 or K3)) and P['ls']['lo']>0 and P['lb']['hi']<0 and P['ltau']['lo']>0 and -2<=P['rB']<=-0.5 \
    and 0.25<=P['rT']<=1.0 and P['pLR']>=0.01 and R['P2']['lo']>0
R['verdict']={'K1':bool(K1),'K2':bool(K2),'K3':bool(K3),'label':'MISS' if (K1 or K2 or K3) else ('HIT' if hit else 'INCONCLUSIVE')}

# ---- Sensitivities (non-decisive)
S={}
def tau_row(c,name):
    return {'beta':float(c.params_['ltau']),'lo':float(c.confidence_intervals_.loc['ltau'].iloc[0]),'hi':float(c.confidence_intervals_.loc['ltau'].iloc[1]),'n':int(c._n_examples),'events':int(c.event_observed.sum())}
# S1 known distress controls
d['lev']=(d.liab/d.assets).clip(0,5); d['roa']=(d.oi4/d.assets).clip(-2,2)
s1=d.dropna(subset=['lev','roa'])
c1=cox(s1,P1+['lev','roa']); S['S1_controls']=tau_row(c1,'S1'); S['S1_controls']['all']={k:float(v) for k,v in c1.params_.items()}
# S2 tau_drop instead of tau
s2=d.dropna(subset=['tau_drop']).copy(); s2['ltau']=np.log(s2.tau_drop); S['S2_tau_drop']=tau_row(cox(s2,P1),'S2')
# S3 cash-only buffer
s3=d[(d.cash>0)].copy(); s3['lb']=np.log(s3.cash); S['S3_cash_only']=tau_row(cox(s3,P1),'S3'); S['S3_cash_only']['lb']=float(cox(s3,P1).params_['lb'])
# S4 drop tau at caps
s4=d[(d.tau>1.0)&(d.tau<20)]; S['S4_drop_capped']=tau_row(cox(s4,P1),'S4')
# S5 logit on D
m5=smf.logit('D ~ ls + lb + ltau + la'+FE,d).fit(disp=0,cov_type='cluster',cov_kwds={'groups':d.cik}); S['S5_logit']={k:[float(m5.params[k]),float(m5.conf_int().loc[k,0]),float(m5.conf_int().loc[k,1])] for k in ['ls','lb','ltau','la']}
# S6 secondary outcome D2
if 'D2' in d and 'T2' in d:
    c6=cox(d,P1,'T2','D2'); S['S6_distress']={k:[float(c6.params_[k]),float(c6.confidence_intervals_.loc[k].iloc[0]),float(c6.confidence_intervals_.loc[k].iloc[1])] for k in P1}; S['S6_distress']['events']=int(d.D2.sum())
    m6=smf.ols('D2 ~ c_ltau*c_lsb + c_la'+P2F+FE,d).fit(cov_type='cluster',cov_kwds={'groups':d.cik}); S['S6_distress']['P2_inter']=[float(m6.params[k]),float(m6.conf_int().loc[k,0]),float(m6.conf_int().loc[k,1])]
# S7 tau alone (known-prior-art replication)
c7=cox(d,['ltau']); S['S7_tau_alone']=tau_row(c7,'S7')
# S8 per-cohort primary model (no pooling)
for coh in sorted(df.cohort.unique()):
    sub=df[df.cohort==coh]; cc=CoxPHFitter().fit(sub[P1+['T','D']],'T','D')
    S[f'S8_{coh}']={k:[float(cc.params_[k]),float(cc.confidence_intervals_.loc[k].iloc[0]),float(cc.confidence_intervals_.loc[k].iloc[1])] for k in P1}; S[f'S8_{coh}']['n']=int(len(sub)); S[f'S8_{coh}']['events']=int(sub.D.sum())
R['S']=S
json.dump(R,open(outp,'w'),indent=1)
print(json.dumps({'n':R['n'],'events':R['events'],'P1':{k:R['P1'][k] for k in ['ls','lb','ltau','rB','rT','pLR','rB_ci','rT_ci']},'P2':{k:R['P2'][k] for k in ['inter','lo','hi','ltau']},'verdict':R['verdict']},indent=1))
