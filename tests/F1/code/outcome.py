"""Outcomes + SIC from SEC submissions.zip (pulled only AFTER prereg commit).
For each CIK in the pre-outcome candidate list: sic, all filings (form, date, items)."""
import zipfile, json, sys, pandas as pd
from multiprocessing import Pool
Z='<local>/gtao/tests/F1/raw/submissions.zip'
WIN={'C1':('2015-01-01','2019-12-31'),'C2':('2020-01-01','2024-12-31')}
_Z=None
def _init():
    global _Z; _Z=zipfile.ZipFile(Z)
def load(cik):
    z=_Z; name=f'CIK{int(cik):010d}.json'
    try: j=json.loads(z.read(name))
    except KeyError: return {'cik':cik,'found':0}
    f=[j['filings']['recent']]
    for extra in j['filings'].get('files',[]):
        try: f.append(json.loads(z.read(extra['name'])))
        except KeyError: pass
    rows=[]
    for blk in f:
        for form,date,items in zip(blk['form'],blk['filingDate'],blk.get('items',['']*len(blk['form']))):
            rows.append((form,date,items or ''))
    def is8k(r): return r[0] in ('8-K','8-K/A')
    def has(r,it): return it in [x.strip() for x in r[2].split(',')]
    bk=[r[1] for r in rows if is8k(r) and has(r,'1.03')]
    out={'cik':cik,'found':1,'sic':j.get('sic',''),'sicDescription':j.get('sicDescription',''),'n_filings':len(rows)}
    for coh,(W0,W1) in WIN.items():
        pre0=f'{int(W0[:4])-2}'+W0[4:]
        pre_bk=[d for d in bk if pre0<=d<W0]
        win_bk=sorted(d for d in bk if W0<=d<=W1)
        dist=sorted(r[1] for r in rows if is8k(r) and W0<=r[1]<=W1 and (has(r,'1.03') or (has(r,'3.01') and not has(r,'2.01') and not has(r,'5.01'))))
        alld=sorted(r[1] for r in rows if r[1]<=W1)
        out.update({f'pre_bk_{coh}':int(bool(pre_bk)),f'bk_date_{coh}':win_bk[0] if win_bk else None,
                    f'dist_date_{coh}':dist[0] if dist else None,f'last_filing_{coh}':alld[-1] if alld else None})
    return out
if __name__=='__main__':
    ciks=[int(x) for x in open(sys.argv[1]).read().split()]
    with Pool(6,initializer=_init) as p: out=p.map(load,ciks,chunksize=20)
    pd.DataFrame(out).to_csv('<local>/gtao/tests/F1/data/outcomes_raw.csv',index=False)
    print(len(out))
