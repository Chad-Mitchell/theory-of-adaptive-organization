"""C4b (POST HOC): for each MATCH1 repo, simulate a pure renewal process with the repo's own pooled empirical
hazard (from <repo>_filtered_L3650.csv), keep simulated files with >= 50 events (as MATCH1 did) until 30 such files
(or 40000 files tried), and compute the renewal-implied beta with MATCH1's spectral_beta. Compare with measured beta.
Caveat: the pooled hazard mixes heterogeneous files; the >=50-event files are an active subset; repo lifetime set to 3650 d."""
import numpy as np, json, sys
from scipy.stats import spearmanr
sys.path.insert(0,"../../../../tests/MATCH1"); from aslib import spectral_beta
rng=np.random.default_rng(7)
rows=[json.loads(l) for l in open("../../../../tests/MATCH1/code/results.jsonl")]
C=[]; n=3650
for r in rows:
    if r.get("beta") is None: continue
    tab=np.loadtxt(f"../../../../tests/MATCH1/code/{r['repo']}_filtered_L3650.csv",delimiter=",",skiprows=1)
    need,risk=tab[:,1],tab[:,2]
    h=np.clip(np.where(risk>=20,need/np.maximum(risk,1),np.nan),0,0.999)
    # fill sparse tail with last reliable hazard
    last=np.nanmax(np.where(~np.isnan(h))[0]); h[last+1:]=h[last]; h=np.nan_to_num(h)
    surv=np.concatenate([[1.0],np.cumprod(1-h)[:-1]]); cdf=np.cumsum(h*surv)
    ser=[]; tried=0
    while len(ser)<30 and tried<40000:
        tried+=1; t=int(rng.integers(0,n//2)); d=[t]
        u=rng.random(400)
        for uu in u:
            if uu>=cdf[-1]: break
            t+=int(np.searchsorted(cdf,uu))+1
            if t>=n: break
            d.append(t)
        if len(d)>=50:
            s=np.zeros(n); s[d]=1; ser.append(s)
    b=spectral_beta(ser,1/730,0.5) if len(ser)>=5 else None
    C.append(dict(repo=r["repo"],a_need=round(r["filtered"]["exponent"],3),beta_measured=round(r["beta"],3),
                  beta_renewal=None if b is None else round(b,3),n_sim_files=len(ser),tried=tried))
    print(C[-1],flush=True)
D=[c for c in C if c["beta_renewal"] is not None]
bm=[c["beta_measured"] for c in D]; br=[c["beta_renewal"] for c in D]; an=[c["a_need"] for c in D]
summ=dict(n=len(D),spearman_measured_vs_renewal=float(spearmanr(bm,br)[0]),p_measured_vs_renewal=float(spearmanr(bm,br)[1]),
          spearman_renewal_beta_vs_a=float(spearmanr(br,an)[0]),spearman_measured_beta_vs_a=float(spearmanr(bm,an)[0]),
          median_measured_minus_renewal=float(np.median(np.array(bm)-np.array(br))))
json.dump(dict(repos=C,summary=summ),open("c4b_match1_renewal.json","w"),indent=1)
print(json.dumps(summ,indent=1))
