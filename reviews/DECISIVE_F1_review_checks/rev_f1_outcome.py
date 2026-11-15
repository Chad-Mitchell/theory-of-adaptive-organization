import zipfile, json, pandas as pd, numpy as np
Z=zipfile.ZipFile('/workspace/gtao/tests/F1/raw/submissions.zip')
d=pd.read_csv('/workspace/gtao/tests/F1/data/analysis_dataset.csv')
W={'C1':('2015-01-01','2019-12-31'),'C2':('2020-01-01','2024-12-31')}
cache={}
def filings(cik):
    if cik in cache: return cache[cik]
    j=json.loads(Z.read(f'CIK{int(cik):010d}.json')); blks=[j['filings']['recent']]
    for e in j['filings'].get('files',[]):
        try: blks.append(json.loads(Z.read(e['name'])))
        except KeyError: pass
    rows=[(f,dt,it or '') for b in blks for f,dt,it in zip(b['form'],b['filingDate'],b.get('items',['']*len(b['form'])))]
    cache[cik]=rows; return rows
mine=[]
for r in d.itertuples():
    w0,w1=W[r.cohort]
    ev=any(f in('8-K','8-K/A') and '1.03' in [x.strip() for x in it.split(',')] and w0<=dt<=w1 for f,dt,it in filings(r.cik))
    mine.append(int(ev))
d['D_rev']=mine
print('events mine',sum(mine),'theirs',int(d.D.sum()),'disagree',int((d.D_rev!=d.D).sum()))
print(d[d.D_rev!=d.D][['cik','name','cohort','D','D_rev']].head(20).to_string())
print(d[d.D==1].sample(12,random_state=0)[['name','cohort','bk_date_C1','bk_date_C2']].to_string())
# share of events with T at window start (left issues)
print('min T event',d.loc[d.D==1,'T'].min(), 'median T',d.loc[d.D==1,'T'].median())
print('firms in both cohorts',d.cik.duplicated(keep=False).sum())
