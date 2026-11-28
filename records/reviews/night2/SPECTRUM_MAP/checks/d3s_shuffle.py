"""PREREG D3S (locked at commit 6636f02): gap-shuffle test of the renewal explanation of MATCH1 D3.
Pipeline copied from tests/MATCH1/code/run.py (filtered: no merges, commits touching <=100 files)."""
import sys,subprocess,collections,json,numpy as np
from scipy.stats import spearmanr
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../../../tests/MATCH1")); from aslib import need_counts, fit, spectral_beta
REPOS=sys.argv[1:]; rng=np.random.default_rng(20261115); out=[]
for repo in REPOS:
    txt=subprocess.run(["git","-C",repo,"log","--no-merges","--format=@%ct","--name-status","--no-renames","HEAD"],capture_output=True,text=True).stdout
    commits=[];cur=None
    for line in txt.splitlines():
        if line.startswith("@"): cur=[int(line[1:])//86400,[]]; commits.append(cur)
        elif line.strip() and cur is not None:
            st,_,f=line.partition("\t"); cur[1].append((st,f))
    ed=collections.defaultdict(set); dele={}
    for day,fs in commits:
        if len(fs)>100: continue
        for st,f in fs:
            ed[f].add(day)
            if st.startswith("D"): dele[f]=max(dele.get(f,0),day)
    end=max(max(s) for s in ed.values()); start=min(min(s) for s in ed.values()); n=end-start+1
    alive=[sorted(s) for f,s in ed.items() if not (f in dele and dele[f]>=max(s))]
    dead=[sorted(s) for f,s in ed.items() if (f in dele and dele[f]>=max(s))]
    n1,d1=need_counts(alive,365,end=end); n2,d2=need_counts(dead,365,end=None); lag=np.arange(366)
    a=fit(lag[1:],(n1+n2)[1:],(d1+d2)[1:])["exponent"]
    big=[np.array(sorted(s))-start for s in ed.values() if len(s)>=50]
    def ser(lists):
        S=[]
        for d in lists:
            s=np.zeros(n); s[d]=1; S.append(s)
        return S
    b0=spectral_beta(ser(big),1/730,0.5) if len(big)>=5 else None
    bs=[]
    for k in range(5):
        sh=[]
        for d in big:
            g=np.diff(d); rng.shuffle(g); sh.append(np.concatenate([[d[0]],d[0]+np.cumsum(g)]))
        bs.append(spectral_beta(ser(sh),1/730,0.5))
    # Goh-Barabasi memory M: corr of consecutive gaps, pooled over big files
    x=[];y=[]
    for d in big:
        g=np.diff(d).astype(float)
        if len(g)>2: x+=list(g[:-1]); y+=list(g[1:])
    M=float(np.corrcoef(x,y)[0,1]); Ml=float(np.corrcoef(np.log(x),np.log(y))[0,1])
    row=dict(repo=repo,a_need=round(a,3),beta_orig=None if b0 is None else round(b0,3),beta_shuf=round(float(np.mean(bs)),3),
             beta_shuf_sd=round(float(np.std(bs)),3),n_files=len(big),M_gb=round(M,3),M_loggaps=round(Ml,3))
    row["delta"]=None if b0 is None else round(b0-row["beta_shuf"],3)
    out.append(row); print(json.dumps(row),flush=True)
D=[r for r in out if r["delta"] is not None]; dl=np.array([r["delta"] for r in D])
md=float(np.median(dl))
verdict="PASS (S1)" if -0.03<=md<=0.05 else ("KILL R as main explanation" if md>0.08 else "PARTIAL")
summ=dict(n=len(D),median_delta=round(md,3),S1=verdict,
          S2_spearman_beta_shuf_vs_a=round(float(spearmanr([r["beta_shuf"] for r in D],[r["a_need"] for r in D])[0]),3),
          spearman_beta_orig_vs_a=round(float(spearmanr([r["beta_orig"] for r in D],[r["a_need"] for r in D])[0]),3),
          spearman_orig_vs_shuf=round(float(spearmanr([r["beta_orig"] for r in D],[r["beta_shuf"] for r in D])[0]),3),
          median_M_gb=round(float(np.median([r["M_gb"] for r in D])),3))
json.dump(dict(repos=out,summary=summ),open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"d3s_shuffle.json"),"w"),indent=1)
print(json.dumps(summ,indent=1))
