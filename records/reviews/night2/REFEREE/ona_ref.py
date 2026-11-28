#!/usr/bin/env python3
"""Independent referee re-analysis of VIGIL_ONA (written without reading the authors' RESULTS.md).
Own loaders, own estimators (statsmodels GLM), jackknife + two-way cluster SEs, seniority controls,
ego-rank permutation test, robustness to unit/threshold choices."""
import numpy as np, pandas as pd, statsmodels.api as sm, json, sys, warnings
warnings.filterwarnings('ignore')
RAW='<local>/gtao/night2/VIGIL_ONA/data/raw'
rng=np.random.default_rng(2026)

def nodes():
    D={}
    k=pd.read_csv(f'{RAW}/krack_nodes.txt',sep=' ')
    D['krack']=pd.DataFrame({'id':k.nodeID-1,'lvl':3-k.nodeLevel,'unit':k.nodeDepartment,'ten':k.nodeTenure,
                             'ego':k.nodeLevel!=1})
    l=pd.read_csv(f'{RAW}/lz/ELattr.dat',sep=r'\s+',header=None,
                  names=['sen','status','gender','office','yrs','age','practice','school'])
    D['lazega']=pd.DataFrame({'id':np.arange(len(l)),'lvl':2-l.status,'unit':l.office*10+l.practice,'ten':l.yrs,
                              'office':l.office,'age':l.age,'ego':True})
    for n in ['consulting','manufacturing']:
        d=pd.read_csv(f'{RAW}/cp/{n}/nodes.csv'); d.columns=[c.strip('# ') for c in d.columns]
        lvl=d.orglevel-1 if n=='consulting' else 4-d.orglevel
        D[n]=pd.DataFrame({'id':d['index'],'lvl':lvl,'unit':d.location,
                           'ten':d['tenure'] if 'tenure' in d else np.nan,'ego':True})
    return D

def edges(name,layer='advice',thr=None):
    if name=='krack':
        e=pd.read_csv(f'{RAW}/krack_multiplex.edges',sep=' ',header=None,names=['L','i','j','w'])
        L={'advice':1,'friendship':2,'reports':3}[layer]; e=e[e.L==L]
        return pd.DataFrame({'i':e.i-1,'j':e.j-1})
    if name=='lazega':
        f={'advice':'ELadv.dat','cowork':'ELwork.dat','friendship':'ELfriend.dat'}[layer]
        m=np.loadtxt(f'{RAW}/lz/{f}'); i,j=np.nonzero(m); return pd.DataFrame({'i':i,'j':j})
    e=pd.read_csv(f'{RAW}/cp/{name}/edges.csv'); e.columns=['i','j','layer','w']
    e['layer']=e.layer.str.strip(); e=e[(e.layer==layer)&(e.w>=thr)]
    return e[['i','j']]

def dyads(nd,ed,unitcol='unit'):
    n=len(nd); A=np.zeros((n,n)); ed=ed[ed.i!=ed.j]; A[ed.i.values,ed.j.values]=1
    I,J=np.where(~np.eye(n,dtype=bool))
    lv=nd.lvl.values; u=nd[unitcol].values; eg=nd.ego.values
    lo,hi=lv[eg].min(),lv[eg].max(); rs=(lv-lo)/(hi-lo)
    t=nd.ten.values.astype(float); tz=(t-np.nanmean(t[eg]))/np.nanstd(t[eg]) if np.isfinite(t).any() else np.zeros(n)
    df=pd.DataFrame({'i':I,'j':J,'y':A[I,J],'out':(u[I]!=u[J]).astype(float),'r':rs[I],
                     'ahi':(lv[J]>lv[I]).astype(float),'aeq':(lv[J]==lv[I]).astype(float),
                     'tz':tz[I],'tmore':(t[J]>t[I]).astype(float)})
    return df[eg[I]].reset_index(drop=True)

def fit_h2(df,senior=False,perm_r=None):
    d=df.copy()
    if perm_r is not None: d['r']=d.i.map(perm_r)
    d['rx']=d.r*d.out
    cols=['rx','out','ahi','aeq']
    if senior: d['tx']=d.tz*d.out; cols+=['tx','tmore']
    g=d.groupby('i').y.agg(['sum','count']); d=d[d.i.isin(g[(g['sum']>0)&(g['sum']<g['count'])].index)]
    ga=d.groupby('j').y.sum(); d=d[d.j.isin(ga[ga>0].index)].reset_index(drop=True)
    X=pd.concat([d[cols],pd.get_dummies(d.i,prefix='e',dtype=float),pd.get_dummies(d.j,prefix='a',dtype=float).iloc[:,1:]],axis=1)
    X=X.loc[:,X.std()>0] if 'const' not in X else X
    try:
        m=sm.GLM(d.y,X,family=sm.families.Binomial()).fit(method='newton',maxiter=100,disp=0)
    except Exception as ex:
        m=sm.GLM(d.y,X,family=sm.families.Binomial()).fit_regularized(alpha=1e-6,L1_wt=0)
    b=m.params['rx']
    if perm_r is not None: return b
    # two-way cluster
    p=m.predict(X); S=X.values*(d.y-p).values[:,None]; W=p*(1-p)
    Hinv=np.linalg.pinv(X.values.T@(X.values*W.values[:,None]))
    def meat(gr):
        M=np.zeros((X.shape[1],)*2)
        for _,ix in pd.Series(np.arange(len(d))).groupby(gr.values): s=S[ix.values].sum(0); M+=np.outer(s,s)
        return M
    V=Hinv@(meat(d.i)+meat(d.j)-S.T@S)@Hinv; k=list(X.columns).index('rx')
    se2=np.sqrt(V[k,k]) if V[k,k]>0 else np.nan
    out={'beta':float(b),'se_model':float(m.bse['rx']),'se_2way':float(se2),'n_dyads':len(d),'n_egos':int(d.i.nunique())}
    if senior: out['beta_tenure_x_out']=float(m.params.get('tx',np.nan))
    return out

def jack_h2(df,senior=False):
    egos=df.i.unique(); bs=[]
    for e in egos:
        try: bs.append(fit_h2(df[(df.i!=e)&(df.j!=e)],senior,perm_r=None)['beta'])
        except Exception: pass
    bs=np.array(bs); n=len(bs); return float(np.sqrt((n-1)/n*((bs-bs.mean())**2).sum()))

def perm_h2(df,K=200,senior=False):
    """permute ego rank among egos for the interaction term only (a_hi/a_eq kept at true ranks)"""
    b0=fit_h2(df,senior)['beta']; rmap=df.groupby('i').r.first()
    bs=[]
    for _ in range(K):
        pr=pd.Series(rng.permutation(rmap.values),index=rmap.index)
        try: bs.append(fit_h2(df,senior,perm_r=pr))
        except Exception: pass
    bs=np.array(bs); return float(np.mean(bs>=b0)), float(np.mean(bs)), float(np.std(bs))

def h1(df):
    t=df.groupby('i').apply(lambda x: pd.Series({'yo':x.y[x.out==1].sum(),'no':(x.out==1).sum(),
        'yi':x.y[x.out==0].sum(),'ni':(x.out==0).sum(),'r':x.r.iloc[0],'tz':x.tz.iloc[0]}),include_groups=False)
    t=t[t.no>0]
    m=sm.GLM(t.yo,sm.add_constant(t[['r']]),family=sm.families.Poisson(),offset=np.log(t.no)).fit(cov_type='HC1')
    return {'logRR':float(m.params['r']),'se':float(m.bse['r']),'n':len(t)}, t

def meta(L,key='beta',sek='se_2way'):
    L=[x for x in L if x and np.isfinite(x[sek]) and x[sek]<=3 and abs(x[key])<=5]
    w=np.array([1/x[sek]**2 for x in L]); b=np.array([x[key] for x in L]); m=(w*b).sum()/w.sum(); s=1/np.sqrt(w.sum())
    return {'est':float(m),'se':float(s),'lo':float(m-1.96*s),'hi':float(m+1.96*s),'w_share':[float(x) for x in w/w.sum()],'Q':float((w*(b-m)**2).sum())}

if __name__=='__main__':
    D=nodes(); THR={'consulting':3,'manufacturing':4}; R={}
    H2=[];H2s=[];H1=[]
    for n in ['krack','lazega','consulting','manufacturing']:
        df=dyads(D[n],edges(n,'advice',THR.get(n)))
        a,t=h1(df); b=fit_h2(df); 
        b['se_jack']=jack_h2(df)
        bs=fit_h2(df,senior=True) if n!='consulting' else None
        if bs: bs['se_jack']=jack_h2(df,True)
        pv=perm_h2(df,K=200)
        R[n]={'H1':a,'H2':b,'H2_senior':bs,'H2_perm_p_one_sided':pv[0],'perm_null_mean_sd':pv[1:],
              'n_nodes':len(D[n]),'n_ties':int(df.y.sum()),'levels':D[n][D[n].ego].lvl.value_counts().sort_index().to_dict()}
        H1.append(a); H2.append(b); H2s.append(bs if bs else b)
        print(n,json.dumps(R[n],default=float),flush=True)
    R['pooled']={'H1':meta(H1,'logRR','se'),'H2_2way':meta(H2),'H2_jack':meta(H2,'beta','se_jack'),
                 'H2_senior_jack(consulting unadjusted)':meta(H2s,'beta','se_jack'),
                 'H2_noLazega_jack':meta([x for k,x in zip(R,H2) if k!='lazega'],'beta','se_jack')}
    print(json.dumps(R['pooled'],indent=1))
    json.dump(R,open('<local>/gtao/night2/REVIEW/ona_ref_main.json','w'),indent=1,default=float)
