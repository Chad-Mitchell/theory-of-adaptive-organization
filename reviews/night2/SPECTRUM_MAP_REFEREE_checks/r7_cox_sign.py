"""Referee check R7: does a pure Cox (rate-modulated, no renewal structure) world ALSO give a positive
Spearman(beta, a_need) with MATCH1's estimators? If yes, the positive D3 sign does not discriminate renewal from Cox.
24 random synthetic repos: 60 files x 5000 days; log-rate Gaussian 1/f^gamma, gamma~U(0.4,1.2), s~U(0.5,1.8), r~logU(0.01,0.05)."""
import sys, json, numpy as np
from scipy.stats import spearmanr
sys.path.insert(0,"<local>/smr-wt/tests/MATCH1"); from aslib import spectral_beta, need_counts, fit
rng=np.random.default_rng(11); n=5000; F=60
def gp(gamma):
    f=np.fft.rfftfreq(2*n); A=np.zeros_like(f); A[1:]=f[1:]**(-gamma/2)
    x=np.fft.irfft((rng.normal(size=f.size)+1j*rng.normal(size=f.size))*A)[:n]; return (x-x.mean())/x.std()
rows=[]
for i in range(24):
    gamma=rng.uniform(0.4,1.2); s=rng.uniform(0.5,1.8); r=np.exp(rng.uniform(np.log(0.01),np.log(0.05)))
    lists=[]
    for k in range(F):
        p=np.minimum(1,r*np.exp(s*gp(gamma)-s*s/2)); lists.append(np.nonzero(rng.random(n)<p)[0])
    num,den=need_counts(lists,365,end=n-1); lag=np.arange(366); a=fit(lag[1:],num[1:],den[1:])["exponent"]
    big=[d for d in lists if len(d)>=50]
    ser=[]
    for d in big:
        z=np.zeros(n); z[d]=1; ser.append(z)
    b=spectral_beta(ser,1/730,0.5) if len(ser)>=5 else None
    if b is not None: rows.append(dict(gamma=round(gamma,3),s=round(s,3),r=round(r,4),a_need=round(a,3),beta=round(b,3),n_files=len(big)))
    print(rows[-1] if rows else None,flush=True)
rho,p=spearmanr([x["beta"] for x in rows],[x["a_need"] for x in rows])
summ=dict(n=len(rows),spearman_beta_a=round(float(rho),3),p=float(p)); print(summ)
json.dump(dict(rows=rows,summary=summ),open("r7_cox_sign.json","w"),indent=1)
