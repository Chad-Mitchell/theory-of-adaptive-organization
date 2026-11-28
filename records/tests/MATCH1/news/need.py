import sys,re,json,collections,numpy as np,pandas as pd
sys.path.insert(0,'.'); from aslib import *
STOP=set("the and for with from that this are was were has have had not but its his her their they them you your our who what when where why how all any can will would could should into over after before about against between under than then there here also more most some such only own same very just new says say said off out set sets get gets back down amid".split())
df=pd.read_csv("news/abcnews-date-text.csv",dtype={"publish_date":str})
df["day"]=(pd.to_datetime(df.publish_date,format="%Y%m%d")-pd.Timestamp("2003-01-01")).dt.days
def run(sub,label,Lmax=730,beta=True):
    occ=collections.defaultdict(set)
    for d,h in zip(sub.day,sub.headline_text.astype(str)):
        for w in set(re.findall(r"[a-z]+",h.lower())):
            if len(w)>=3 and w not in STOP: occ[w].add(d)
    tot=collections.Counter()
    for d,h in zip(sub.day,sub.headline_text.astype(str)):
        for w in re.findall(r"[a-z]+",h.lower()):
            if len(w)>=3 and w not in STOP: tot[w]+=1
    words=[w for w in occ if tot[w]>=20]
    end=int(sub.day.max())
    num,den=need_counts((sorted(occ[w]) for w in words),Lmax,end=end)
    lag=np.arange(Lmax+1)
    r=fit(lag[1:],num[1:],den[1:]); r.update(label=label,n_words=len(words),start=int(sub.day.min()),end=end)
    if beta:
        start=int(sub.day.min()); n=end-start+1
        big=[w for w in words if tot[w]>=200]
        cnt=collections.defaultdict(lambda: np.zeros(n))
        for d,h in zip(sub.day,sub.headline_text.astype(str)):
            for w in re.findall(r"[a-z]+",h.lower()):
                if w in cnt or w in set(big): cnt[w][d-start]+=1
        r["beta"]=spectral_beta([cnt[w] for w in big],1/730,0.5); r["n_beta_words"]=len(big)
    np.savetxt(f"news/needodds_{label}.csv",np.c_[lag[1:],num[1:],den[1:]],delimiter=",",header="lag,needed,at_risk",fmt="%d")
    return r
res=[run(df[(df.day>=0)&(df.day<=pd.Timestamp('2006-12-31').dayofyear+365*3)],"2003_2006"), run(df,"full",beta=False)]
for r in res: print(json.dumps(r))
json.dump(res,open("news/need_results.json","w"),indent=1)
