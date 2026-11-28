# C12c-G' bookkeeping (NOT a test: every input is a committed number or a recomputation of one).
# Worlds = the 9-world single-system menu of r2_record_pricing.py (both readings).
# cap-selected (no mixing) = Pareto-minimal points of (S, E); stake-selected (q >= 0) = minimisers of S + qE
# = vertices of the lower-left convex hull. Gap = Pareto points never a stake minimiser.
import numpy as np, json
S_rec={"classical N=2":1.0,"classical N=3":np.log2(3),"classical N=4":2.0,"square (gbit)":2.0,"pentagon":1.070431,
       "hexagon":1.188722,"octagon":1.127571,"disk (rebit)":1.0,"ball (qubit)":1.0}
S_tot={k:(np.log2(3) if k=="classical N=3" else 2.0 if k=="classical N=4" else 1.0) for k in S_rec}
E_com={"classical N=2":.25,"classical N=3":.167,"classical N=4":.125,"square (gbit)":.125,"pentagon":.176,"hexagon":.167,
       "octagon":.172,"disk (rebit)":.1817,"ball (qubit)":.1817}
E_pre={"classical N=2":.25,"classical N=3":1/6,"classical N=4":.125,"square (gbit)":.125,"pentagon":0.176393,"hexagon":1/6,
       "octagon":0.172335,"disk (rebit)":0.5-1/np.pi,"ball (qubit)":0.5-1/np.pi}
def analyse(S,E,tol=1e-9):
    pts={k:(S[k],E[k]) for k in S}
    pareto=[k for k in pts if not any((pts[j][0]<=pts[k][0]+tol and pts[j][1]<=pts[k][1]+tol) and (pts[j][0]<pts[k][0]-tol or pts[j][1]<pts[k][1]-tol) for j in pts)]
    # stake minimisers over a fine q grid plus exact breakpoints
    qs=set(np.linspace(0,200,200001))
    ks=list(pts)
    for a in ks:
        for b in ks:
            if pts[a][1]!=pts[b][1]:
                q=(pts[b][0]-pts[a][0])/(pts[a][1]-pts[b][1])
                if q>0: qs|={q,q*(1+1e-9),q*(1-1e-9)}
    winners=set(); wq={}
    for q in sorted(qs):
        J={k:pts[k][0]+q*pts[k][1] for k in ks}; m=min(J.values())
        for k in ks:
            if J[k]<=m+tol: winners.add(k); wq.setdefault(k,[q,q]); wq[k][1]=q; wq[k][0]=min(wq[k][0],q)
    gap=[k for k in pareto if k not in winners]
    # vertical margin of each gap point above the hull (hull = lower envelope over stake winners)
    W=sorted({pts[k] for k in winners})
    def hullE(s):
        best=np.inf
        for i in range(len(W)):
            for j in range(i+1,len(W)):
                (s1,e1),(s2,e2)=W[i],W[j]
                if s1<=s<=s2 and s2>s1: best=min(best,e1+(e2-e1)*(s-s1)/(s2-s1))
        return best
    marg={k:pts[k][1]-hullE(pts[k][0]) for k in gap}
    # cap windows: D range where k is the (unique-spend) cap minimiser
    win={}
    for k in pareto:
        cheaper=[pts[j][1] for j in pts if pts[j][0]<pts[k][0]-tol]
        win[k]=(pts[k][1], min(cheaper) if cheaper else np.inf)
    return dict(pareto=sorted(pareto),stake_winners={k:(round(v[0],3),round(v[1],3)) for k,v in sorted(wq.items())},gap=gap,
                margin_above_hull={k:round(v,6) for k,v in marg.items()},cap_windows={k:(round(a,6),round(b,6)) for k,(a,b) in win.items()})
res={}
for name,S,E in [("per-record, committed E (3-4 d.p.)",S_rec,E_com),("per-record, precise E",S_rec,E_pre),
                 ("total, committed E",S_tot,E_com),("total, precise E",S_tot,E_pre)]:
    r=analyse(S,E); res[name]=r; print("==",name); [print("  ",k,":",v) for k,v in r.items()]
# sensitivity: how much would hexagon's spend have to rise (P_rec is a binary-read lower bound) for pentagon/octagon to join the hull?
for dS in (0.0,0.005,0.01,0.02,0.05):
    S2=dict(S_rec); S2["hexagon"]+=dS; r=analyse(S2,E_pre); print(f"hexagon spend +{dS}: gap = {r['gap']}")
json.dump(res,open("gap.json","w"),indent=1,default=str)
