"""Apply preregistered sample rules and outcome coding -> data/analysis_dataset.csv"""
import pandas as pd, numpy as np, datetime as dt
D='<local>/gtao/tests/F1/data/'
import sys
o=pd.read_csv(D+'outcomes_raw.csv')
WIN={'C1':('2015-01-01','2019-12-31','2019-07-01'),'C2':('2020-01-01','2024-12-31','2024-07-01')}
LASTF={'C1':'2014-07-01','C2':'2019-07-01'}
log=[]; parts=[]
for COH in ['C1','C2']:
  m=pd.read_csv(D+f'measures_{COH}.csv'); log.append(f'--- cohort {COH}')
  def step(df,msg): log.append(f'{msg}: {len(df)}'); return df
  f=step(m,'companyfacts entities with >=12 revenue quarters')
  f=step(f[f.lastfiled>=LASTF[COH]],'R1 filed XBRL 10-Q/10-K facts in the half-year before cutoff')
  f=step(f[f.tau.notna()],'R2 tau estimable (>=16 consecutive-quarter pairs, 2009Q1..cutoff-year Q3)')
  f=step(f[f.sigma.notna()&(f.sigma>0)],'R3 sigma (>=10 four-quarter changes in the last 12 quarters, >0)')
  f=step(f[(f.B>0)&(f.assets>0)],'R4 B>0 and assets>0 at latest balance date <= cutoff-year Sep 30')
  f=step(f[f.rev_q_mean>=2.5e6],'R5 mean quarterly revenue over last 4 quarters >= $2.5M')
  f=f.merge(o,on='cik',how='left')
  f=step(f[f.found==1],'R6 found in submissions')
  sic=pd.to_numeric(f.sic,errors='coerce')
  f=step(f[sic.notna()&~sic.between(6000,6799)&~sic.between(4900,4999)],'R7 SIC known, not financial 6000-6799, not utility 4900-4999')
  f=step(f[f[f'pre_bk_{COH}']==0],'R8 no 8-K Item 1.03 filed in the 2 years before risk start')
  w0=pd.Timestamp(WIN[COH][0]); w1=pd.Timestamp(WIN[COH][1]); early=pd.Timestamp(WIN[COH][2])
  def code(row,col):
      if isinstance(row[col],str): return 1,(pd.Timestamp(row[col])-w0).days
      last=pd.Timestamp(row[f'last_filing_{COH}']) if isinstance(row[f'last_filing_{COH}'],str) else w0
      cen=last if last<early else w1   # stopped filing early -> censor at last filing
      return 0,max((min(cen,w1)-w0).days,1)
  f[['D','T']]=f.apply(lambda r: pd.Series(code(r,f'bk_date_{COH}')),axis=1)
  f[['D2','T2']]=f.apply(lambda r: pd.Series(code(r,f'dist_date_{COH}')),axis=1)
  f['T']=f['T'].clip(lower=1); f['T2']=f['T2'].clip(lower=1)
  parts.append(f)
f=pd.concat(parts,ignore_index=True)
f.to_csv(D+'analysis_dataset.csv',index=False)
open(D+'sample_flow.txt','w').write('\n'.join(log)+f'\nevents D={int(f.D.sum())} D2={int(f.D2.sum())}\n')
print('\n'.join(log)); print('events',f.D.sum(),f.D2.sum())
