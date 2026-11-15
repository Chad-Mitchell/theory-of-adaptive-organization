"""Secondary arm E (COVID shock). Industry shock = leave-one-out median over firms in the same 3-digit SIC
(>=5 others; else 2-digit, >=5 others) of ln(R_2020Q2 / R_2019Q2), from companyfacts (any filing date).
Own-firm 2020 data never used for the firm's own shock."""
import zipfile, json, numpy as np, pandas as pd, sys
sys.path.insert(0,'/workspace/gtao/tests/F1/code')
from multiprocessing import Pool
ZIP='/workspace/gtao/tests/F1/raw/companyfacts.zip'
REV=['Revenues','RevenueFromContractWithCustomerExcludingAssessedTax','RevenueFromContractWithCustomerIncludingAssessedTax','SalesRevenueNet','SalesRevenueGoodsNet','SalesRevenueServicesNet']
import datetime as dt
def qidx(e):
    e=dt.date.fromisoformat(e)-dt.timedelta(days=15); return e.year*4+(e.month-1)//3
def rq(cik):
    z=zipfile.ZipFile(ZIP)
    try: j=json.loads(z.read(f'CIK{int(cik):010d}.json'))
    except KeyError: return (cik,None,None)
    usg=j['facts'].get('us-gaap',{}); vals={}
    for t in REV:
        for r in usg.get(t,{}).get('units',{}).get('USD',[]):
            if 'start' in r and 80<=(dt.date.fromisoformat(r['end'])-dt.date.fromisoformat(r['start'])).days<=100:
                vals.setdefault(qidx(r['end']),{}).setdefault(t,r['val'])
    def g(q):
        v=vals.get(q,{}); 
        for t in REV:
            if t in v: return v[t]
    return (cik,g(2019*4+1),g(2020*4+1))
if __name__=='__main__':
    D='/workspace/gtao/tests/F1/data/'
    a=pd.read_csv(D+'analysis_dataset.csv'); a=a[a.cohort=='C2'].copy()
    o=pd.read_csv(D+'outcomes_raw.csv')   # all candidate firms with SIC (industry peers)
    o=o[o.found==1].copy(); o['sicn']=pd.to_numeric(o.sic,errors='coerce'); o=o[o.sicn.notna()]
    with Pool(6) as p: r=p.map(rq,o.cik.tolist(),chunksize=20)
    r=pd.DataFrame(r,columns=['cik','r19','r20']); o=o.merge(r,on='cik')
    o['g']=np.where((o.r19>0)&(o.r20>0),np.log(o.r20/o.r19),np.nan)
    o['s3']=(o.sicn//10).astype(int); o['s2']=(o.sicn//100).astype(int)
    sh=[]
    for _,x in a.iterrows():
        sicn=int(float(x.sic)); peers=o[(o.cik!=x.cik)&o.g.notna()]
        p3=peers[peers.s3==sicn//10].g; p2=peers[peers.s2==sicn//100].g
        med=p3.median() if len(p3)>=5 else (p2.median() if len(p2)>=5 else np.nan)
        sh.append(med)
    a['ind_g']=sh; a['shockE']=np.maximum(0,-a.ind_g)
    a.to_csv(D+'analysis_dataset_E.csv',index=False); print(a.shockE.describe())
