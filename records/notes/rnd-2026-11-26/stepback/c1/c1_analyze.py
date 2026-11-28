# Evaluate C1 §1 criteria (H1-2D, ISO, SP) on greedy outputs. OBSERVED numerics.
import sys, json, math, numpy as np
from scipy.spatial import Delaunay
from c1_vacua import Vacuum, S_bits, VACUA
T=[(0,0),(1,0),(0,1),(1,1)]; c0=np.array([0.5,0.5])
def record(gains,kappa):
    n=0
    while n<len(gains) and gains[n]>=kappa: n+=1
    return n
def analyze(fn, targets=(40,80,120,160), K=256):
    d=json.load(open(fn)); sel=[tuple(p) for p in d["sel"]]; g=np.array(d["gains"])
    name=d["vacuum"]; flux,m=VACUA[name]; v=Vacuum(flux,m,K=K); S_T=S_bits(v.P(T))
    I=lambda S: S_T+S_bits(v.P(list(S)))-S_bits(v.P(T+list(S))) if S else 0.0
    rows=[]
    for tgt in targets:
        if tgt>len(g): continue
        kap=float(g[:tgt].min()); n=record(g,kap); S=sel[:n]; full=set(T)|set(S)
        pts=np.array(sorted(full),float)
        tri=Delaunay(pts); xs=np.arange(pts[:,0].min(),pts[:,0].max()+1); ys=np.arange(pts[:,1].min(),pts[:,1].max()+1)
        grid=np.array([(x,y) for x in xs for y in ys]); inside=(tri.find_simplex(grid,tol=1e-9)>=0).sum(); fill=len(full)/inside
        # radial weight: weight of site = its greedy gain (as G4-1 radial-weight proxy)
        r=np.linalg.norm(np.array(S,float)-c0,axis=1); w=g[:n]; o=np.argsort(r); cw=np.cumsum(w[o])/w.sum()
        r90=r[o][np.searchsorted(cw,0.90)]; r99=r[o][min(np.searchsorted(cw,0.99),n-1)]
        nb=lambda p:[(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)]
        Lin=[p for p in S if any(q not in full for q in nb(p))]
        Lout=sorted({q for p in full for q in nb(p) if q not in full})
        ang=[math.atan2(p[1]-c0[1],p[0]-c0[0]) for p in Lin]; rad=[math.hypot(p[0]-c0[0],p[1]-c0[1]) for p in Lin]
        sec=[[] for _ in range(8)]
        for a,rr in zip(ang,rad): sec[int(((a+math.pi/8)%(2*math.pi))//(math.pi/4))].append(rr)
        rs=[np.mean(s) if s else 0.0 for s in sec]; iso=(max(rs)-min(rs))/np.mean(rs)
        I0=I(S); Iin=I([p for p in S if p not in set(Lin)]); Iout=I(S+Lout)
        rin=(I0-Iin)/(kap*len(Lin)); rout=(Iout-I0)/(kap*len(Lout))
        # out-of-window check of greedy frontier: best single gain among Lout vs kappa
        bestout=max(I(S+[q])-I0 for q in Lout)
        rows.append(dict(target=tgt,kappa=kap,n=n,fill=fill,r90=float(r90),r99=float(r99),H1=bool(fill>=0.8 and r99-r90<=3),
            iso=float(iso),sector_r=[round(x,2) for x in rs],ISO=bool(iso<=0.2),rho_in=rin,rho_out=rout,SP=bool(0.8<=rin<=1.2 and 0.8<=rout<=1.2),
            nLin=len(Lin),nLout=len(Lout),best_next_over_kappa=bestout/kap))
    return name,rows
if __name__=="__main__":
    out={}
    for fn in sys.argv[1:]:
        name,rows=analyze(fn); out[name]=rows; print("==",name,fn)
        for r in rows: print({k:(round(x,4) if isinstance(x,float) else x) for k,x in r.items()})
    json.dump(out,open("c1_analysis.json","w"),indent=1)
