# C12c-G'' gap decision (C12CG §8.4) with exact per-record spends (prec_n*.json) and precise errors.
import json, numpy as np
import gap as G   # reuses analyse(); importing re-runs gap.py's committed tables (printed), harmless
sp={n:json.load(open(f"prec_n{n}.json")) for n in (4,5,6,8)}
best=lambda n:max(sp[n]["k2_exhaustive"][0],sp[n]["k3_exhaustive"][0],sp[n]["k4_local"][0])
S=dict(G.S_rec); S["square (gbit)"]=best(4); S["pentagon"]=best(5); S["hexagon"]=best(6); S["octagon"]=best(8)
print("\n=== C12c-G'' exact spends (all finite-outcome reads, k<=4):",{k:round(S[k],6) for k in ("square (gbit)","pentagon","hexagon","octagon")})
print("k-convergence (k4-k3):",{n:round(sp[n]['k4_local'][0]-sp[n]['k3_exhaustive'][0],9) for n in sp})
r=G.analyse(S,G.E_pre,tol=1e-6); [print("  ",k,":",v) for k,v in r.items()]
surv=[k for k,m in r["margin_above_hull"].items() if m>1e-5]
print("DECISION (§8.4):","gap SURVIVES" if surv else "gap CLOSES", surv)
# robustness: how much would the hexagon's (exact) spend need to move, or the octagon's error fall, to close it
for dS in (0.01,0.02,0.03): 
    S2=dict(S); S2["hexagon"]+=dS; print(f"  (counterfactual) hexagon spend +{dS}: gap = {G.analyse(S2,G.E_pre,tol=1e-6)['gap']}")
json.dump(dict(spends=S,result=r,decision=surv),open("gap2.json","w"),indent=1,default=str)
