import subprocess,sys,collections,json,numpy as np
repo=sys.argv[1]
out=subprocess.run(["git","-C",repo,"log","--no-merges","--format=@%ct","--name-status","--no-renames","HEAD"],capture_output=True,text=True).stdout
edits=collections.defaultdict(set); dele={}
day=None
MAXF=int(sys.argv[2]) if len(sys.argv)>2 else 10**9
blocks=out.split("\n@")
out2=[]
for b in blocks:
    ls=[l for l in b.splitlines() if l.strip()]
    if len(ls)-1<=MAXF: out2.extend(["@"+ls[0].lstrip("@")]+ls[1:])
out="\n".join(out2)
for line in out.splitlines():
    if line.startswith("@"): day=int(line[1:])//86400; continue
    if not line.strip(): continue
    st,_,f=line.partition("\t")
    edits[f].add(day)
    if st.startswith("D"): dele[f]=max(dele.get(f,0),day)
end=max(max(s) for s in edits.values())
L=365; num=np.zeros(L+1); den=np.zeros(L+1)
for f,s in edits.items():
    d=sorted(s)
    for a,b in zip(d,d[1:]):
        if f in dele and a>=dele[f] : pass
        g=b-a; m=min(g,L); den[1:m+1]+=1
        if g<=L: num[g]+=1
    last=d[-1]
    if f in dele and dele[f]>=last: continue  # file deleted at last event: no censored tail
    m=min(end-last,L); den[1:m+1]+=1
lag=np.arange(1,L+1); p=num[1:]/den[1:]
ok=(num[1:]>0)
odds=p/(1-p)
x=np.log(lag[ok]); y=np.log(odds[ok]); w=num[1:][ok]  # binomial weight ~ count
def wls(X,y,w):
    A=np.vstack([X,np.ones_like(X)]).T; W=np.sqrt(w)
    c,*_=np.linalg.lstsq(A*W[:,None],y*W,rcond=None); r=y-A@c
    sse=np.sum(w*r**2); r2=1-sse/np.sum(w*(y-np.average(y,weights=w))**2); return c,sse,r2
cp,ssep,r2p=wls(x,y,w); ce,ssee,r2e=wls(lag[ok].astype(float),y,w)
res=dict(repo=repo,files=len(edits),days=int(end-min(min(s) for s in edits.values())),power_exponent=-cp[0],power_sse=ssep,power_r2=r2p,exp_rate_per_day=-ce[0],exp_sse=ssee,exp_r2=r2e,n_lags=int(ok.sum()))
print(json.dumps(res))
np.savetxt(repo.rstrip('/').split('/')[-1]+"_needodds_maxf.csv",np.c_[lag,num[1:],den[1:]],delimiter=",",header="lag_days,needed,at_risk",fmt="%d")
