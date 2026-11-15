import numpy as np, pandas as pd, statsmodels.api as sm, json, warnings
warnings.filterwarnings('ignore')
from ona_ref import nodes, edges, dyads, fit_h2, jack_h2, h1, meta
D=nodes(); R={}
l=D['lazega']
print('Lazega yrs by status: partners',l[l.lvl==1].ten.describe()[['min','25%','50%','max']].tolist(),'assoc',l[l.lvl==0].ten.describe()[['min','25%','50%','max']].tolist())
print('corr(status, yrs)=',np.corrcoef(l.lvl,l.ten)[0,1], ' corr(status, age)=',np.corrcoef(l.lvl,l.age)[0,1])
print('Lazega units x status:\n',pd.crosstab(l.unit,l.lvl))
def fitx(df,extra,base=('rx','out','ahi','aeq')):
    d=df.copy(); d['rx']=d.r*d.out
    for k,f in extra.items(): d[k]=f(d)
    cols=list(base)+list(extra)
    g=d.groupby('i').y.agg(['sum','count']); d=d[d.i.isin(g[(g['sum']>0)&(g['sum']<g['count'])].index)]
    ga=d.groupby('j').y.sum(); d=d[d.j.isin(ga[ga>0].index)].reset_index(drop=True)
    X=pd.concat([d[cols],pd.get_dummies(d.i,prefix='e',dtype=float),pd.get_dummies(d.j,prefix='a',dtype=float).iloc[:,1:]],axis=1)
    m=sm.GLM(d.y,X,family=sm.families.Binomial()).fit(method='newton',maxiter=100,disp=0,cov_type='cluster',cov_kwds={'groups':d.i.values})
    return {k:[round(float(m.params[k]),3),round(float(m.bse[k]),3)] for k in cols if k in m.params}
lz_adv=edges('lazega','advice')
# unit definitions
for uc in ['unit','office','practice']:
    nd=l.copy()
    if uc=='practice': nd['practice']=nd.unit%10
    df=dyads(nd,lz_adv,unitcol=uc); R[f'lazega_unit={uc}']=fit_h2(df); print('lazega unit',uc,R[f'lazega_unit={uc}'])
df=dyads(l,lz_adv)
lv=l.lvl.values; yrs=l.ten.values.astype(float); age=l.age.values.astype(float); prac=(l.unit%10).values; off=l.office.values
z=lambda v:(v-v.mean())/v.std()
R['lazega_status_x_boundary']=fitx(df,base=('rx','out','ahi'),extra={'ahi_out':lambda d:d.ahi*d.out,'aeq_out':lambda d:d.aeq*d.out}); print('status x boundary',R['lazega_status_x_boundary'])
R['lazega_seniority']=fitx(df,base=('rx','out','ahi'),extra={'yrs_out':lambda d:z(yrs)[d.i]*d.out,'age_out':lambda d:z(age)[d.i]*d.out,'amore_sen':lambda d:(yrs[d.j]>yrs[d.i]).astype(float)}); print('seniority',R['lazega_seniority'])
R['lazega_all']=fitx(df,base=('rx','out','ahi'),extra={'ahi_out':lambda d:d.ahi*d.out,'aeq_out':lambda d:d.aeq*d.out,'yrs_out':lambda d:z(yrs)[d.i]*d.out,'amore_sen':lambda d:(yrs[d.j]>yrs[d.i]).astype(float)}); print('all',R['lazega_all'])
# within-status seniority gradient (GTAO: no level difference inside a status -> no gradient; seniority rival: gradient)
for s,name in [(1,'partners'),(0,'associates')]:
    dd=df[(lv[df.i]==s)].copy()
    R[f'lazega_within_{name}']=fitx(dd,base=('out',),extra={'yrs_out':lambda d:z(yrs)[d.i]*d.out,'amore_sen':lambda d:(yrs[d.j]>yrs[d.i]).astype(float)})
    print('within',name,R[f'lazega_within_{name}'])
# placebo
for n,lay in [('lazega','friendship'),('krack','friendship'),('lazega','cowork')]:
    R[f'{n}_{lay}']=fit_h2(dyads(D[n],edges(n,lay))); print(n,lay,R[f'{n}_{lay}'])
# thresholds CP
for n,th in [('consulting',[2,3,4]),('manufacturing',[2,3,4,5])]:
    for t in th:
        dd=dyads(D[n],edges(n,'advice',t)); R[f'{n}_thr{t}']={'H2':fit_h2(dd),'H1':h1(dd)[0]}; print(n,t,R[f'{n}_thr{t}'])
# Krackhardt: VPs' outside ties & tenure
k=D['krack']; dk=dyads(k,edges('krack','advice'))
a,t=h1(dk); t['lvl']=k.set_index('id').loc[t.index,'lvl'].values; t['ten']=k.set_index('id').loc[t.index,'ten'].values
t['rate_out']=t.yo/t.no; t['rate_in']=t.yi/t.ni.replace(0,np.nan)
print(t.groupby('lvl')[['rate_out','rate_in']].mean())
# H3: elasticity with Krackhardt real subtree size; CP pyramid proxy is a deterministic function of level
rep=edges('krack','reports')
kids={};[kids.setdefault(j,[]).append(i) for i,j in zip(rep.i,rep.j)]
def sub(x):
    s=set();f=[x]
    while f:
        y=f.pop()
        for c in kids.get(y,[]):
            if c not in s: s.add(c); f.append(c)
    return len(s)
k['N']=[sub(x) for x in k.id]; print('Krack subtree N:',k[k.lvl>0][['id','lvl','N']].values.tolist())
rows=[]
for n in ['krack','consulting','manufacturing']:
    nd=D[n].copy()
    if n=='krack': nd['N']=k['N']
    else:
        s=nd.lvl; nd['N']=s.map({L:((s<L).sum()/(s==L).sum()) for L in s.unique()})
    dd=dyads(nd,edges(n,'advice',{'consulting':3,'manufacturing':4}.get(n)))
    _,tt=h1(dd); tt['N']=nd.set_index('id').loc[tt.index,'N'].values; tt['lvl']=nd.set_index('id').loc[tt.index,'lvl'].values; tt['d']=n; rows.append(tt)
    if n!='krack': print(n,'level->N map',nd.groupby('lvl').N.first().round(2).to_dict())
T=pd.concat(rows); T['lnN']=np.log1p(T.N)
X=pd.concat([T[['lnN']],pd.get_dummies(T.d,dtype=float)],axis=1)
m=sm.GLM(T.yo,X,family=sm.families.Poisson(),offset=np.log(T.no)).fit(cov_type='HC1'); print('H3 elasticity',m.params['lnN'],m.bse['lnN'])
m2=sm.GLM(T.yo,X,family=sm.families.Poisson(),offset=np.log(T.no)).fit(cov_type='cluster',cov_kwds={'groups':(T.d+T.lvl.astype(str)).values}); print('H3 clustered by dataset-level cells',m2.bse['lnN'], 'n cells',(T.d+T.lvl.astype(str)).nunique())
R['H3']={'el':float(m.params['lnN']),'se_hc1':float(m.bse['lnN']),'se_cell_cluster':float(m2.bse['lnN'])}
for n in ['krack','consulting','manufacturing']:
    TT=T[T.d==n]
    if TT.N.nunique()>1:
        mm=sm.GLM(TT.yo,sm.add_constant(TT[['lnN']]),family=sm.families.Poisson(),offset=np.log(TT.no)).fit(cov_type='HC1'); print(' H3',n,mm.params['lnN'],mm.bse['lnN']); R[f'H3_{n}']=[float(mm.params['lnN']),float(mm.bse['lnN'])]
# leave-one-out of Krack: without VPs? H3 without manufacturing top 4
TT=T[~((T.d=='manufacturing')&(T.lvl>=2))]; X=pd.concat([TT[['lnN']],pd.get_dummies(TT.d,dtype=float)],axis=1)
mm=sm.GLM(TT.yo,X,family=sm.families.Poisson(),offset=np.log(TT.no)).fit(cov_type='HC1'); print('H3 w/o manufacturing top-2 levels (4 people)',mm.params['lnN'],mm.bse['lnN']); R['H3_drop_mfg_top4']=[float(mm.params['lnN']),float(mm.bse['lnN'])]
json.dump(R,open('ona_robust.json','w'),indent=1,default=float)
