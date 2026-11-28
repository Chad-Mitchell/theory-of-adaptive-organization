import json,numpy as np,pandas as pd,matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig,ax=plt.subplots(2,2,figsize=(14,11))
# (a) exponents need vs memory
a=ax[0,0]
news=json.load(open("news/need_results.json")); mem={r["label"]:r for r in json.load(open("memory/meeter_results.json"))}
code=[json.loads(l) for l in open("code/results.jsonl")]; wiki=json.load(open("wiki/results.json")); mz=json.load(open("measles/results.json"))
rows=[("NEWS need: headlines 2003-06",news[0]["exponent"],"b"),("NEWS need: headlines 2003-21",news[1]["exponent"],"b"),
("NEWS memory: open recall (all)",mem["e12_open_all"]["exponent"],"r"),("NEWS memory: open recall (English)",mem["e12_open_english"]["exponent"],"r"),("NEWS memory: 4-choice (all)",mem["e12_mc4afc_all"]["exponent"],"r"),
("CODE need: median of 26 repos",np.median([c["filtered"]["exponent"] for c in code]),"b"),("WIKIPEDIA need: 400 random pages",wiki["nobots"]["exponent"],"b"),
("MEASLES need: town re-exposure",mz["need_exponent"],"b"),("MEASLES memory: antibody",mz["mem_exponent"],"r")]
for i,(n,v,c) in enumerate(rows): a.barh(i,v,color=c); a.text(v+0.02,i,f"{n}  {v:.2f}",va="center",fontsize=8)
a.axvspan(0.5,0.85,color="grey",alpha=0.15); a.set_yticks([]); a.set_xlim(0,2.6); a.set_xlabel("power-law exponent (log odds vs log lag)")
a.set_title("(a) Need (blue) vs memory (red) exponents; grey = preregistered need band")
# (b) news need vs memory curves
b=ax[0,1]
n=np.loadtxt("news/needodds_2003_2006.csv",delimiter=",",skiprows=1); ok=n[:,1]>0; p=n[ok,1]/n[ok,2]
b.loglog(n[ok,0],p/(1-p)/(p[0]/(1-p[0])),'.',ms=2,label="need odds (headlines), normalised")
c=pd.read_csv("memory/curve_e12_open_all.csv"); o=c.p/(1-c.p); b.loglog(c.age,o/o.iloc[0],'o-',c="r",label="recall odds (open), normalised")
b.set_xlabel("days since last occurrence / since event"); b.set_ylabel("odds relative to first point"); b.legend(); b.set_title("(b) News: need falls ~3x faster (in log-log slope) than memory")
# (c) code exponents vs beta
cc=ax[1,0]; x=[c_["beta"] for c_ in code]; y=[c_["filtered"]["exponent"] for c_ in code]
cc.scatter(x,y); [cc.annotate(c_["repo"].split("_")[-1],(c_["beta"],c_["filtered"]["exponent"]),fontsize=6) for c_ in code]
cc.axhspan(0.5,0.85,color="grey",alpha=0.15); cc.set_xlabel("spectral redness beta of per-file edit series"); cc.set_ylabel("need exponent"); cc.set_title("(c) 26 repos: 24 in band; redder -> STEEPER need decay (rho=+0.57)")
# (d) layers
d=ax[1,1]; L=json.load(open("layers/results.json"))
diag=open("layers/diag_tolerances.txt").read().splitlines()
for j,line in enumerate(diag):
    name,rest=line.split(" ",1); vals=eval(rest.replace("np.float64",""))
    if not vals: continue
    d.plot([v[0]+0.03*j for v in vals],[v[2]+0.08*j for v in vals],'o-',label=f"{name} (tol 0.03, post hoc; offset for visibility)")
d.set_xlabel("span fitted (decades)"); d.set_ylabel("layers needed K*"); d.set_ylim(0,10); d.legend(fontsize=7)
d.set_title("(d) Layers vs span: at preregistered tol 0.02 only Wikipedia resolves (2,3,4,5,5)")
plt.suptitle("MATCH1: does memory's decay exponent match need's? (sources/ and per-test folders)"); plt.tight_layout(); plt.savefig("match.png",dpi=130)
