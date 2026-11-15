import pandas as pd,numpy as np,json,matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig,ax=plt.subplots(2,2,figsize=(14,11))
# (a) timescale pairs, each system normalised to its own first point? No: raw, log-log, with guides
d=pd.read_csv("collapse_data.csv")
a=ax[0,0]; mk={'S':'o','D':'s'}
for s,g in d.groupby("system",sort=False):
    b=np.polyfit(np.log(g.world_timescale),np.log(g.memory_timescale),1)[0]
    a.plot(g.world_timescale/g.world_timescale.iloc[0],g.memory_timescale/g.memory_timescale.iloc[0],marker=mk[g['class'].iloc[0]],label=f"{s} ({g['class'].iloc[0]}) slope {b:.2f}")
xx=np.array([1,10]); a.plot(xx,xx,'k--',lw=2,label="slope 1 (N1 / class S,D)"); a.plot(xx,xx**0.5,'k:',lw=2,label="slope 1/2 (class C)")
a.set_xscale('log');a.set_yscale('log');a.set_xlabel("world timescale / first point");a.set_ylabel("memory timescale / first point")
a.set_title("(a) Within-system scaling (each series normalised to its first point)");a.legend(fontsize=7)
# (b) exponent space
b=ax[0,1]
need=[("news headlines (A&S 1991)",0.73),("child-directed speech (A&S)",0.77),("email (A&S)",0.83)]
cs=json.load(open("code_need/results.json"))
for r in cs: need.append((f"code {r['repo']} (this test{', bulk commits excl.' if r['sens'] else ''})",r['exp']))
mem=[("antibody tetanus (Saha 2025)",0.43),("antibody diphtheria",0.36),("antibody VZV",0.42),("Benna-Fusi chain model (theory)",0.5),("Ebbinghaus savings (A&S; % savings scale)",0.126)]
y=0
for n,v in need: b.barh(y,v,color="tab:blue"); b.text(v+0.01,y,n,va='center',fontsize=8); y+=1
for n,v in mem: b.barh(y,v,color="tab:red" if 'theory' not in n else 'grey'); b.text(v+0.01,y,n,va='center',fontsize=8); y+=1
b.set_yticks([]);b.set_xlim(0,1.6);b.set_xlabel("power-law exponent m (decay ~ t^-m)")
b.set_title("(b) Exponents: blue = need decay, red = memory decay")
# (c) firm inventory slopes
c=ax[1,0]; R=pd.read_csv("firm/industry_slopes.csv").sort_values("slope").reset_index(drop=True)
c.errorbar(R.slope,range(len(R)),xerr=[R.slope-R.ci_lo,R.ci_hi-R.slope],fmt='o')
c.set_yticks(range(len(R)));c.set_yticklabels([f"SIC {s} (n={n})" for s,n in zip(R.sic2,R.n)],fontsize=7)
c.axvline(0.5,ls=':',c='k',label='EOQ square-root law (0.5)');c.axvline(1,ls='--',c='k',label='proportional (1)')
c.set_xlabel("slope of log inventory on log cost of goods, within industry (US filers, FY2023)");c.legend(fontsize=8)
c.set_title("(c) Firm scale: inventory vs throughput")
# (d) measurement-age artifact
e=ax[1,1]; t=np.logspace(0,2,50)
for m in (0.36,0.43): e.plot(t,t*np.log(2)/m,'k-' if m==0.43 else 'k--',label=f"apparent half-life under power law, m={m}")
pts=[("tetanus",8,11),("diphtheria",8,19),("VZV",45,50),("vaccinia",45,92),("rubella",45,114),("mumps",45,542),("measles",45,3014),("EBV",45,11552)]
for n,tt,h in pts: e.scatter(tt,h,c='tab:red'); e.annotate(n,(tt,h),fontsize=8,xytext=(4,2),textcoords='offset points')
e.axhline(50,c='grey',lw=0.8); e.text(1.1,55,"50 y 'horizon'",fontsize=8)
e.set_xscale('log');e.set_yscale('log');e.set_xlabel("years after exposure when the half-life was measured (approx., per Saha et al.)");e.set_ylabel("reported half-life (y), Amanna 2007")
e.set_title("(d) Why BIO1's immune 'failure' was partly an artifact");e.legend(fontsize=8)
plt.suptitle("COLLAPSE1: memory timescales vs world timescales across substrates (sources in sources/, data in CSVs)",fontsize=12)
plt.tight_layout(); plt.savefig("collapse.png",dpi=130)
