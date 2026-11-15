import sys,json,numpy as np,pandas as pd
sys.path.insert(0,'.'); from aslib import *
pages=[json.loads(l) for l in open("wiki/revisions.jsonl")][:400]
ref=pd.Timestamp("2001-01-01",tz="UTC"); end=None
res={}
allmax=0
for label,botfilter in (("nobots",True),("all",False)):
    lists=[]
    for p in pages:
        days=sorted(set(int((pd.Timestamp(ts)-ref).days) for ts,u in p["revs"] if not (botfilter and u.lower().endswith("bot"))))
        if days: lists.append(days); allmax=max(allmax,days[-1])
    end=int((pd.Timestamp("2026-11-14",tz="UTC")-ref).days)
    for Lmax,tag in ((365,""),(3650,"_L3650")):
        num,den=need_counts(lists,Lmax,end=end); lag=np.arange(Lmax+1)
        np.savetxt(f"wiki/needodds_{label}{tag}.csv",np.c_[lag[1:],num[1:],den[1:]],delimiter=",",fmt="%d",header="lag,needed,at_risk")
        if tag=="":
            r=fit(lag[1:],num[1:],den[1:]); res[label]=dict(exponent=r["exponent"],power_wins=r["power_wins"],r2_power=r["power"]["r2"],r2_exp=r["exp"]["r2"],pages=len(lists),edits=int(sum(len(x) for x in lists)))
print(json.dumps(res,indent=1)); json.dump(res,open("wiki/results.json","w"),indent=1)
