"""Referee check R6: does the locked D3S gap-shuffle test have power? (positive/negative controls, not in the prereg)
Synthetic 'repos': 40 files, 5000 days, binary daily edit series. Same spectral_beta (MATCH1 aslib) and same shuffle.
 - RENEWAL: i.i.d. gaps, discretized Weibull (shape k<1 -> bursty) -> expect delta ~ 0.
 - COX: daily edit prob p_t = min(1, r*exp(s*g_t)), g_t a unit-variance Gaussian process with 1/f^gamma spectrum
        (shared within a file) -> rate modulation; expect delta > 0 if the test has power.
Reports beta_orig, beta_shuf, delta (median over 6 synthetic repos per setting)."""
import sys, json, numpy as np
sys.path.insert(0,"<local>/smr-wt/tests/MATCH1"); from aslib import spectral_beta
rng=np.random.default_rng(7); n=5000; F=40
def series(d):
    s=np.zeros(n); s[d]=1; return s
def shuf(d):
    g=np.diff(d); rng.shuffle(g); return np.concatenate([[d[0]],d[0]+np.cumsum(g)])
def powerlaw_gp(gamma):
    f=np.fft.rfftfreq(2*n); A=np.zeros_like(f); A[1:]=f[1:]**(-gamma/2)
    z=(rng.normal(size=f.size)+1j*rng.normal(size=f.size))*A; x=np.fft.irfft(z)[:n]; return (x-x.mean())/x.std()
def repo(kind,par):
    files=[]
    while len(files)<F:
        if kind=="renewal":
            k,scale=par; g=np.maximum(1,np.round(scale*rng.weibull(k,size=4000))).astype(int)
            d=np.cumsum(g); d=d[d<n]
        else:
            gamma,s,r=par; p=np.minimum(1,r*np.exp(s*powerlaw_gp(gamma))); d=np.nonzero(rng.random(n)<p)[0]
        if len(d)>=50: files.append(d)
    b0=spectral_beta([series(d) for d in files],1/730,0.5)
    bs=np.mean([spectral_beta([series(shuf(d)) for d in files],1/730,0.5) for _ in range(5)])
    return b0,bs
out={}
settings=[("renewal",(0.5,20)),("renewal",(0.35,10)),("renewal",(0.25,5)),
          ("cox",(1.0,1.0,0.03)),("cox",(1.0,1.5,0.02)),("cox",(0.6,1.5,0.02)),("cox",(0.4,1.0,0.03)),("cox",(1.0,0.6,0.04))]
for kind,par in settings:
    R=[repo(kind,par) for _ in range(6)]
    b0=np.median([r[0] for r in R]); bs=np.median([r[1] for r in R]); dl=np.median([r[0]-r[1] for r in R])
    out[f"{kind}{par}"]=dict(beta_orig=round(float(b0),3),beta_shuf=round(float(bs),3),median_delta=round(float(dl),3))
    print(kind,par,out[f"{kind}{par}"],flush=True)
json.dump(out,open("r6_d3s_power.json","w"),indent=1)
