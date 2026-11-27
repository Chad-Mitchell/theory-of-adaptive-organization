# Independent re-implementation of the C1 §1 criteria + review diagnostics (OBSERVED)
import sys, json, math, numpy as np
sys.path.insert(0,'../stepback/c1')
from c1_vacua import Vacuum, S_bits, VACUA
from rv_greedy_mu import vac_for
T=[(0,0),(1,0),(0,1),(1,1)]; c0=np.array([0.5,0.5])
def hull_fill(full):
    pts=np.array(sorted(full),float)
    from scipy.spatial import ConvexHull
    h=ConvexHull(pts); A=h.equations  # a x + b y + c <= 0 inside
    xs=np.arange(pts[:,0].min(),pts[:,0].max()+1); ys=np.arange(pts[:,1].min(),pts[:,1].max()+1)
    G=np.array([(x,y) for x in xs for y in ys]); inside=(G@A[:,:2].T+A[:,2]<=1e-9).all(1).sum(); return len(full)/inside
def rq(r,w,q):
    o=np.argsort(r,kind='stable'); cw=np.cumsum(w[o])/w.sum(); return r[o][min(np.searchsorted(cw,q-1e-12),len(r)-1)]
def iso_of(full,S):
    nb=lambda p:[(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)]
    Lin=[p for p in S if any(q not in full for q in nb(p))]
    sec=[[] for _ in range(8)]
    for p in Lin:
        a=math.atan2(p[1]-c0[1],p[0]-c0[0]); sec[int(((a+math.pi/8)%(2*math.pi))//(math.pi/4))].append(math.hypot(p[0]-c0[0],p[1]-c0[1]))
    rs=[np.mean(s) if s else 0.0 for s in sec]; return (max(rs)-min(rs))/np.mean(rs), rs, Lin
def crit(sel,g,v,tgt=120):
    kap=float(min(g[:tgt])); n=0
    while n<len(g) and g[n]>=kap: n+=1
    S=sel[:n]; full=set(T)|set(S); fill=hull_fill(full)
    rS=np.linalg.norm(np.array(S,float)-c0,axis=1); rU=np.linalg.norm(np.array(sorted(full),float)-c0,axis=1)
    d_gain=rq(rS,np.array(g[:n]),.99)-rq(rS,np.array(g[:n]),.90); d_ind=rq(rU,np.ones(len(rU)),.99)-rq(rU,np.ones(len(rU)),.90)
    iso,rs,Lin=iso_of(full,S)
    ST=S_bits(v.P(T)); I=lambda X: ST+S_bits(v.P(list(X)))-S_bits(v.P(T+list(X)))
    nb=lambda p:[(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)]
    Lout=sorted({q for p in full for q in nb(p) if q not in full}); I0=I(S)
    rin=(I0-I([p for p in S if p not in set(Lin)]))/(kap*len(Lin)); rout=(I(S+Lout)-I0)/(kap*len(Lout))
    par=sum((p[0]+p[1])%2 for p in S)/len(S)
    axes=np.mean([rs[0],rs[2],rs[4],rs[6]]); diag=np.mean([rs[1],rs[3],rs[5],rs[7]])
    return dict(kappa=kap,n=n,fill=round(fill,3),r99_r90_gain=round(float(d_gain),2),r99_r90_indicator=round(float(d_ind),2),iso=round(iso,3),diag_over_axes=round(diag/axes,3),
                rho_in=round(rin,3),rho_out=round(rout,3),odd_parity_frac=round(par,3))
if __name__=="__main__":
    runs=[('orig V1 (tie lo, cheb3)','../stepback/c1/c1_greedy_v0_c3_n200.json',0),('V1 tie hi','rv_v0_hi.json',0),('V1 cheb6','rv_v0_c6.json',0),
          ('orig V2','../stepback/c1/c1_greedy_v1_c3_n200.json',1),('V2 tie hi','rv_v1_hi.json',1),
          ('orig V3','../stepback/c1/c1_greedy_v2_c3_n200.json',2),('V3 tie hi','rv_v2_hi.json',2),('V3 cheb6','rv_v2_c6.json',2),
          ('orig V4','../stepback/c1/c1_greedy_v3_c3_n200.json',3),('NN mu=-2 (round-ish Fermi surface)','rv_mu2.json','mu')]
    base={}
    for lab,fn,vi in runs:
        d=json.load(open(fn)); sel=[tuple(p) for p in d['sel']]; g=d['gains']
        v=vac_for(vi)
        key=vi
        r=crit(sel,g,v); print(lab,r,flush=True)
        if 'orig' in lab: base[vi]=(set(sel[:120]),g[:120])
        elif vi in base:
            s0,g0=base[vi]; print('   vs orig: same set of first 120:',set(sel[:120])==s0,'; max|gain diff| first 120:',float(np.max(np.abs(np.array(g[:120])-np.array(g0)))),
                  '; steps with >1 candidate within 1e-10 of max:',sum(1 for t in d.get('nties',[])[:120] if t>1))
    # digital baselines for the ISO metric
    print('--- ISO/fill baselines for ideal shapes around the plaquette centre ---')
    allp=[(x,y) for x in range(-20,21) for y in range(-20,21) if (x,y) not in T]
    for shape,key in [('disc',lambda p: math.hypot(p[0]-.5,p[1]-.5)),('square (axis-aligned)',lambda p:max(abs(p[0]-.5),abs(p[1]-.5))),('diamond',lambda p:abs(p[0]-.5)+abs(p[1]-.5)),
                      ('ellipse 2:1 along x',lambda p: math.hypot((p[0]-.5)/2,p[1]-.5)),('ellipse 1.25:1 along x',lambda p: math.hypot((p[0]-.5)/1.25,p[1]-.5))]:
        o=sorted(allp,key=key)
        res=[]
        for n in (40,80,120,160):
            S=o[:n]; full=set(T)|set(S); iso,rs,_=iso_of(full,S); res.append(f"n={n}: iso {iso:.3f}, fill {hull_fill(full):.2f}, diag/axes {np.mean(rs[1::2])/np.mean(rs[0::2]):.2f}, x/y {rs[0]/rs[2]:.2f}")
        print(shape,'|','; '.join(res))
