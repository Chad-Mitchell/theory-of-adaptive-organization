"""C4 (POST HOC): does a pure renewal (no spectral 'world' at all) reproduce MATCH1 D3's POSITIVE Spearman(beta, a_need)?
Uses MATCH1's exact estimators (aslib.need_counts, fit with Lmax=365, spectral_beta band 1/730..0.5 c/d, files >= 50 edit days)."""
import numpy as np, json, sys
from scipy.stats import spearmanr
sys.path.insert(0,"../../../../tests/MATCH1"); from aslib import need_counts, fit, spectral_beta
LMAXG=3650
def pmf_from_odds(a,o1):
    L=np.arange(1,LMAXG+1); o=o1*L**(-a); p=o/(1+o); p=np.minimum(p,0.999)
    surv=np.concatenate([[1.0],np.cumprod(1-p)[:-1]]); return p*surv     # sums to <1: remainder = 'no more events'
def pmf_from_hazard(p):
    surv=np.concatenate([[1.0],np.cumprod(1-p)[:-1]]); return p*surv
def sim_repo(pmf,rng,nfiles=300,n=3650,o1_sd=0.0):
    lists=[]
    cdf=np.cumsum(pmf)
    for i in range(nfiles):
        t=int(rng.integers(0,n//2)); d=[t]
        while True:
            u=rng.random()
            if u>=cdf[-1]: break
            g=int(np.searchsorted(cdf,u))+1; t+=g
            if t>=n: break
            d.append(t)
        lists.append(d)
    return lists,n
def measure(lists,n):
    num,den=need_counts(lists,365,end=n-1); lag=np.arange(366)
    a=fit(lag[1:],num[1:],den[1:])["exponent"]
    big=[d for d in lists if len(d)>=50]; ser=[]
    for d in big:
        s=np.zeros(n); s[np.array(d)]=1; ser.append(s)
    b=spectral_beta(ser,1/730,0.5) if len(ser)>=5 else None
    return a,b,len(ser)
rng=np.random.default_rng(20261115); out={"A_grid":[], "B_random_repos":None, "C_matched_to_MATCH1":None}
# A: controlled sweep of the hazard exponent a (o1 fixed)
for a in (0.2,0.35,0.5,0.65,0.8,0.95):
    for o1 in (0.3,):
        ah,b,nb=measure(*sim_repo(pmf_from_odds(a,o1),rng))
        out["A_grid"].append(dict(a_true=a,o1=o1,a_hat=round(ah,3),beta=None if b is None else round(b,3),n_beta_files=nb))
        print(out["A_grid"][-1],flush=True)
# B: 26 random 'repos' with a and o1 drawn independently -> Spearman(beta, a_hat)
A=[];B=[]
for r in range(26):
    a=rng.uniform(0.3,0.9); o1=np.exp(rng.uniform(np.log(0.1),np.log(1.0)))
    ah,b,nb=measure(*sim_repo(pmf_from_odds(a,o1),rng))
    if b is not None: A.append(ah); B.append(b)
rho,p=spearmanr(B,A); out["B_random_repos"]=dict(n=len(A),spearman_beta_a=round(float(rho),3),p=float(p))
print(out["B_random_repos"],flush=True)
# C: MATCH1 repos. Build each repo's empirical hazard from its L3650 need/at-risk table, simulate a pure renewal
#    with that hazard, compute the renewal-implied beta, compare with the measured beta.
rows=[json.loads(l) for l in open("../../../../tests/MATCH1/code/results.jsonl")]
C=[]
for r in rows:
    if r.get("beta") is None: continue
    try: tab=np.loadtxt(f"../../../../tests/MATCH1/code/{r['repo']}_filtered_L3650.csv",delimiter=",",skiprows=1)
    except OSError: continue
    lag,need,risk=tab[:,0],tab[:,1],tab[:,2]
    h=np.where(risk>0,need/np.maximum(risk,1),0.0); h=np.clip(h,0,0.999)
    hz=np.zeros(LMAXG); hz[:len(h)]=h[:LMAXG]
    bs=[]
    for k in range(3):
        lists,n=sim_repo(pmf_from_hazard(hz),rng,nfiles=300)
        _,b,_=measure(lists,n)
        if b is not None: bs.append(b)
    if bs: C.append(dict(repo=r["repo"],a_need=round(r["filtered"]["exponent"],3),beta_measured=round(r["beta"],3),beta_renewal=round(float(np.mean(bs)),3)))
    print(C[-1] if C else None,flush=True)
bm=[c["beta_measured"] for c in C]; br=[c["beta_renewal"] for c in C]; an=[c["a_need"] for c in C]
out["C_matched_to_MATCH1"]=dict(repos=C,n=len(C),spearman_measured_vs_renewal=spearmanr(bm,br)[0],
    spearman_renewal_beta_vs_a=spearmanr(br,an)[0],spearman_measured_beta_vs_a=spearmanr(bm,an)[0],
    mean_abs_diff=float(np.mean(np.abs(np.array(bm)-np.array(br)))))
json.dump(out,open("c4_d3_renewal.json","w"),indent=1,default=float)
print(json.dumps({k:v for k,v in out["C_matched_to_MATCH1"].items() if k!="repos"},indent=1))
