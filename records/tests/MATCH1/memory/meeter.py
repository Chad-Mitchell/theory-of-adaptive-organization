import zipfile,io,json,numpy as np,pandas as pd
z=zipfile.ZipFile("sources/meeter2005_data.zip"); P="DNMT-forget txtdata-oct04/"
def rd(n): return pd.read_csv(io.BytesIO(z.read(P+n)),sep="\t",encoding="latin1",low_memory=False)
E={i:rd(f"DNMT-expt{i}.txt") for i in (1,2,3)}
S=rd("DNMT-sessionsdata.txt")[["SESS_ID","S_TEST"]].drop_duplicates("SESS_ID")
for i in E:
    E[i].columns=[c.strip() for c in E[i].columns]
    if "S_ID" in E[i]: E[i]=E[i].rename(columns={"S_ID":"SESS_ID"})
    E[i]=E[i][pd.to_numeric(E[i].SCORE,errors="coerce").notna()&pd.to_numeric(E[i].Q_AGE,errors="coerce").notna()]
    E[i]["SCORE"]=E[i].SCORE.astype(float); E[i]["Q_AGE"]=E[i].Q_AGE.astype(float); E[i]["expt"]=i
def curve(d,label):
    d=d[(d.Q_AGE>=1)&(d.Q_AGE<=730)]
    edges=np.unique(np.round(np.logspace(0,np.log10(731),25)))
    rows=[]; cur=[]
    d=d.sort_values("Q_AGE"); ages=d.Q_AGE.values; sc=d.SCORE.values
    b=np.digitize(ages,edges)
    for k in np.unique(b):
        m=b==k
        rows.append((ages[m].mean(),sc[m].sum(),m.sum()))
    # merge bins with <200
    out=[];acc=[0,0,0]
    for a,s,n in rows:
        acc=[acc[0]+a*n,acc[1]+s,acc[2]+n]
        if acc[2]>=200: out.append((acc[0]/acc[2],acc[1],acc[2])); acc=[0,0,0]
    out=np.array(out); t=out[:,0]; p=out[:,1]/out[:,2]; y=np.log(p/(1-p)); w=out[:,2]
    res={"label":label,"n":int(w.sum()),"bins":len(t)}
    for name,x in (("power",np.log(t)),("exp",t)):
        A=np.vstack([x,np.ones_like(x)]).T; W=np.sqrt(w)
        c,*_=np.linalg.lstsq(A*W[:,None],y*W,rcond=None); r=y-A@c
        res[name]=dict(slope=float(c[0]),sse=float(np.sum(w*r**2)),r2=float(1-np.sum(w*r**2)/np.sum(w*(y-np.average(y,weights=w))**2)))
    res["exponent"]=-res["power"]["slope"]; res["power_wins"]=res["power"]["sse"]<res["exp"]["sse"]
    pd.DataFrame(dict(age=t,correct=out[:,1],n=w,p=p)).to_csv(f"memory/curve_{label}.csv",index=False)
    return res
R=[]
A12=pd.concat([E[1],E[2]]).merge(S,on="SESS_ID",how="left")
for qt,name in ((1,"open"),(0,"mc4afc")):
    R.append(curve(A12[A12.Q_TYPE==qt],f"e12_{name}_all"))
    R.append(curve(A12[(A12.Q_TYPE==qt)&(A12.S_TEST==2)],f"e12_{name}_english"))
    R.append(curve(A12[(A12.Q_TYPE==qt)&(A12.S_TEST==1)],f"e12_{name}_dutch"))
    for i in (1,2,3):
        d=E[i][E[i].Q_TYPE==qt]
        if len(d)>1000: R.append(curve(d,f"e{i}_{name}"))
for r in R: print(r["label"],r["n"],r["bins"],"exp=%.3f"%r["exponent"],"R2pow=%.3f R2exp=%.3f"%(r["power"]["r2"],r["exp"]["r2"]),"power_wins",r["power_wins"])
json.dump(R,open("memory/meeter_results.json","w"),indent=1)
