"""Extract pre-2020 quarterly series from SEC companyfacts.zip.
Only facts with filed <= CUTOFF_FILED are used. Writes data/panel.parquet-ish CSVs.
"""
import zipfile, json, sys, datetime as dt, csv
from multiprocessing import Pool
ZIP='<local>/gtao/tests/F1/raw/companyfacts.zip'
COH=sys.argv[1] if len(sys.argv)>1 else 'C2'
CUTOFF_FILED={'C1':'2014-12-31','C2':'2019-12-31'}[COH]
REV=['Revenues','RevenueFromContractWithCustomerExcludingAssessedTax','RevenueFromContractWithCustomerIncludingAssessedTax','SalesRevenueNet','SalesRevenueGoodsNet','SalesRevenueServicesNet','RevenuesNetOfInterestExpense']
OI=['OperatingIncomeLoss']
CE=['CostsAndExpenses']
CASH=['CashAndCashEquivalentsAtCarryingValue','CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents','Cash']
STI=['ShortTermInvestments','MarketableSecuritiesCurrent','AvailableForSaleSecuritiesCurrent','AvailableForSaleSecuritiesDebtSecuritiesCurrent']
LOC=['LineOfCreditFacilityRemainingBorrowingCapacity']
ASSETS=['Assets']; LIAB=['Liabilities']
FORMS=('10-Q','10-K','10-Q/A','10-K/A','10-KT','10-QT')

def d(s): return dt.date.fromisoformat(s)
def qidx(end):
    e=d(end)-dt.timedelta(days=15); return e.year*4+(e.month-1)//3

def facts_for(usg, tags):
    out={}
    for t in tags:
        u=usg.get(t,{}).get('units',{}).get('USD',[])
        rows=[r for r in u if r.get('form') in FORMS and r['filed']<=CUTOFF_FILED]
        out[t]=rows
    return out

def quarterly(rows):
    """rows: duration facts for one tag. return {qidx: val}"""
    best={}
    for r in rows:
        if 'start' not in r: continue
        k=(r['start'],r['end'])
        if k not in best or r['filed']>best[k]['filed']: best[k]=r
    q={}; byS={}
    for (s,e),r in best.items():
        n=(d(e)-d(s)).days
        byS.setdefault(s,[]).append((e,n,r['val']))
        if 80<=n<=100: q[qidx(e)]=r['val']
    # derive missing quarters from YTD differences with same start
    for s,lst in byS.items():
        lst.sort()
        for i in range(len(lst)):
            e2,n2,v2=lst[i]
            if n2<170: continue
            for j in range(i):
                e1,n1,v1=lst[j]
                gap=n2-n1
                if 80<=gap<=100 and qidx(e2) not in q:
                    q[qidx(e2)]=v2-v1
    # annual minus three quarters
    for (s,e),r in best.items():
        n=(d(e)-d(s)).days
        if 350<=n<=380:
            qe=qidx(e)
            prev=[qe-1,qe-2,qe-3]
            if qe not in q and all(p in q for p in prev):
                q[qe]=r['val']-sum(q[p] for p in prev)
    return q

def merged_q(fs, tags):
    out={}
    for t in tags:
        for k,v in quarterly(fs[t]).items():
            out.setdefault(k,v)
    return out

def instants(fs,tags):
    out={}
    for t in tags:
        best={}
        for r in fs[t]:
            if 'start' in r: continue
            if r['end'] not in best or r['filed']>best[r['end']]['filed']: best[r['end']]=r
        for e,r in best.items(): out.setdefault(e,{})[t]=r['val']
    return out

def proc(name):
    try:
        z=zipfile.ZipFile(ZIP); j=json.loads(z.read(name))
    except Exception as ex:
        return None
    usg=j.get('facts',{}).get('us-gaap')
    if not usg: return None
    alltags=REV+OI+CE+CASH+STI+LOC+ASSETS+LIAB
    fs=facts_for(usg,alltags)
    R=merged_q(fs,REV); O=merged_q(fs,OI); C=merged_q(fs,CE)
    if len(R)<12: return None
    # last filing date (any form) <= cutoff, among these tags
    lastfiled=max([r['filed'] for t in alltags for r in fs[t]] or ['0'])
    inst={}
    for grp,tags in (('cash',CASH),('sti',STI),('loc',LOC),('assets',ASSETS),('liab',LIAB)):
        inst[grp]=instants(fs,tags)
    return dict(cik=j['cik'],name=j.get('entityName',''),R=R,O=O,C=C,inst=inst,lastfiled=lastfiled)

if __name__=='__main__':
    z=zipfile.ZipFile(ZIP); names=z.namelist()
    out=open(f'<local>/gtao/tests/F1/data/extract_{COH}.jsonl','w')
    with Pool(5) as p:
        for i,res in enumerate(p.imap_unordered(proc,names,chunksize=20)):
            if res:
                res['R']={str(k):v for k,v in res['R'].items()}
                res['O']={str(k):v for k,v in res['O'].items()}
                res['C']={str(k):v for k,v in res['C'].items()}
                out.write(json.dumps(res)+'\n')
            if i%2000==0: print(i,flush=True)
