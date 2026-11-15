import sys,subprocess,collections,json,numpy as np
sys.path.insert(0,'.'); from aslib import *
repo=sys.argv[1]; name=repo.rstrip('/').split('/')[-1]
out=subprocess.run(["git","-C",repo,"log","--no-merges","--format=@%ct","--name-status","--no-renames","HEAD"],capture_output=True,text=True).stdout
commits=[];cur=None
for line in out.splitlines():
    if line.startswith("@"): cur=[int(line[1:])//86400,[]]; commits.append(cur)
    elif line.strip() and cur is not None:
        st,_,f=line.partition("\t"); cur[1].append((st,f))
res={"repo":name,"commits":len(commits)}
for label,maxf in (("filtered",100),("unfiltered",10**9)):
    ed=collections.defaultdict(set); dele={}
    for day,fs in commits:
        if len(fs)>maxf: continue
        for st,f in fs:
            ed[f].add(day)
            if st.startswith("D"): dele[f]=max(dele.get(f,0),day)
    end=max(max(s) for s in ed.values()); start=min(min(s) for s in ed.values())
    lists=[]; 
    for f,s in ed.items():
        d=sorted(s); lists.append(d)
    # censoring: files deleted at their last event get no tail; handle by two passes
    alive=[sorted(s) for f,s in ed.items() if not (f in dele and dele[f]>=max(s))]
    dead=[sorted(s) for f,s in ed.items() if (f in dele and dele[f]>=max(s))]
    for Lmax,tag in ((365,""),(3650,"_L3650")):
        n1,d1=need_counts(alive,Lmax,end=end); n2,d2=need_counts(dead,Lmax,end=None)
        num=n1+n2; den=d1+d2; lag=np.arange(Lmax+1)
        np.savetxt(f"code/{name}_{label}{tag}.csv",np.c_[lag[1:],num[1:],den[1:]],delimiter=",",fmt="%d",header="lag,needed,at_risk")
        if tag=="": 
            r=fit(lag[1:],num[1:],den[1:]); res[label]=dict(exponent=r["exponent"],power_wins=r["power_wins"],r2_power=r["power"]["r2"],r2_exp=r["exp"]["r2"],files=len(ed))
    if label=="filtered":
        n=end-start+1; big=[d for d in lists if len(d)>=50]
        ser=[]
        for d in big:
            s=np.zeros(n); s[np.array(d)-start]=1; ser.append(s)
        res["beta"]=spectral_beta(ser,1/730,0.5) if len(ser)>=5 else None; res["n_beta_files"]=len(ser)
print(json.dumps(res))
