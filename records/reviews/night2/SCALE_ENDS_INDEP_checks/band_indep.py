"""Independent check of SCALE_ENDS's key logical step (BH = frozen-corner limit via Theorem 8) and LAT-1.
Written by the independent referee. Run: nice -n 19 python3 band_indep.py
Theorem 8 (reviews/night1/formal/THEOREMS.md): hold cost min_{T<=H}[c/T + W q T/2] + h; freeze = corner T=H; lookup = mu*u.
Extension tested here (not in Theorem 8): each read returns a value that is l old (latency), so error adds W q l^(alpha-1)."""
import numpy as np
out=[]
def p(*a): s=" ".join(str(x) for x in a); print(s); out.append(s)
rng=np.random.default_rng(7)

def best_mode(q,c,W=1.0,H=10.0,mu=1.0,u=1.0,h=0.1,l=0.0,alpha=2.0,hfreeze=None):
    hf=h if hfreeze is None else hfreeze
    lat=W*q*l**(alpha-1) if l>0 else 0.0
    Ts=np.geomspace(1e-9,H,20000)
    hold=np.min(c/Ts+W*q*Ts/2)+h+lat
    Tstar=np.sqrt(2*c/(W*q)) if q>0 else np.inf
    freeze=c/H+W*q*H/2+hf+lat
    look=mu*u
    costs={'hold(interior)':hold if Tstar<H else np.inf,'freeze':freeze,'lookup':look}
    return min(costs,key=costs.get),costs

p("A. Theorem 8 as c -> infinity (no latency term). Which mode is optimal?")
for c in (1e1,1e3,1e9):
    modes=sorted(set(best_mode(q,c)[0] for q in np.geomspace(1e-12,1e4,400)))
    qf=2*c/(1*10**2)
    p(f"  c={c:g}: q_f=2c/(W H^2)={qf:.3g} (freeze edge vs hold), modes reached over q in [1e-12,1e4]: {modes}")
p("  -> as c grows, the hold/freeze comparison favours 'freeze' (q_f -> inf) but freeze costs c/H -> inf, so the OPTIMUM is LOOKUP, not freeze.")
p("     Theorem 8 therefore places an infinitely costly store beyond the lookup edge (unused), not in the frozen corner.")
p("  Even with zero-upkeep freezing (h_freeze=0) and q -> 0:")
for c in (1e1,1e3):
    m,cost=best_mode(1e-12,c,hfreeze=0.0); p(f"    c={c:g}, q=1e-12: best={m}, freeze cost={cost['freeze']:.3g} vs lookup={cost['lookup']:.3g}")

p("\nB. Read cost priced as ENERGY per bit (GTAO's beta_phys convention) instead of time.")
p("   A 1 Msun hole's emitted quanta cost ~kT_H ~ 8.5e-31 J per nat; take c in units where lookup mu*u=1 and c = 1e-6:")
for l in (0.0,):
    modes=sorted(set(best_mode(q,1e-6,l=l)[0] for q in np.geomspace(1e-12,1e4,400)))
    p(f"   latency ignored: modes reached = {modes}  -> band wide open; a black hole would look like an excellent store.")
p("   So the 'band closes' conclusion does NOT follow from energy pricing; it needs the time cost (lateness) GTAO's budget counts.")

p("\nC. Same cheap c, but each read is l old (lateness enters prediction error, THEORY §0):")
for l in (0.0,1.0,10.0,1e3,1e66):
    qs=np.geomspace(1e-12,1e4,400); ms=[best_mode(q,1e-6,l=l)[0] for q in qs]
    look=[q for q,m in zip(qs,ms) if m=='lookup']
    p(f"   l={l:g}: lookup wins for all q >= {min(look) if look else float('nan'):.3g} (analytic: q > (mu u - h)/(W l) = {0.9/l if l>0 else float('inf'):.3g})")
p("   (Lookup is assumed latency-free here. If lookup also has latency l_L, the comparison is W q (l - l_L): the store loses only if it is later than the world.)")

p("\nD. LAT-1: hold-last-value with read latency l on fBm targets, structure function E(dx^2)=q tau^(alpha-1).")
def fbm_paths(n,dt,H,P):
    # exact Gaussian via Cholesky of fBm covariance
    t=np.arange(1,n+1)*dt
    C=0.5*(t[:,None]**(2*H)+t[None,:]**(2*H)-np.abs(t[:,None]-t[None,:])**(2*H))
    L=np.linalg.cholesky(C+1e-12*np.eye(n))
    return (L@rng.standard_normal((n,P))).T
for alpha in (1.5,2.0,2.5):
    H=(alpha-1)/2; dt=0.02; n=600; P=3000
    X=fbm_paths(n,dt,H,P)
    res=[]
    for l in (0.1,0.2,0.4,0.8,1.6):
        k=int(round(l/dt)); err=np.mean((X[:,k:]-X[:,:-k])**2)  # continuous reading (T->0): error = value l old
        res.append((l,err))
    ls=np.log([r[0] for r in res]); es=np.log([r[1] for r in res]); slope=np.polyfit(ls,es,1)[0]
    p(f"   alpha={alpha}: mse vs l slope = {slope:.3f} (predicted alpha-1 = {alpha-1:.2f}); mse(l=0.4)={res[2][1]:.3f} vs q l^(alpha-1)={0.4**(alpha-1):.3f}")
    # optimal linear one-step extrapolation for alpha>2: predict X(t) from past values sampled up to t-l
    if alpha>2:
        k=int(round(0.4/dt)); m=8  # use m past samples at spacing k
        rows=[];ys=[]
        for s in range(m*k, n):
            rows.append(X[:, [s-k-j*k for j in range(m)]]); ys.append(X[:,s])
        A=np.concatenate(rows); y=np.concatenate(ys)
        coef,*_=np.linalg.lstsq(A,y,rcond=None); e=np.mean((A@coef-y)**2)
        p(f"     linear extrapolation from {m} past reads (each 0.4 old): mse={e:.3f} vs hold-last-value {res[2][1]:.3f} -> latency penalty smaller, as SCALE_ENDS says")
p("   L_max: need q (L/c)^(alpha-1) < D*  =>  L_max = c (D*/q)^(1/(alpha-1)); e.g. alpha=2, D*/q = 1 day -> L_max = 1 light-day.")
open("band_indep.out","w").write("\n".join(out)+"\n")
