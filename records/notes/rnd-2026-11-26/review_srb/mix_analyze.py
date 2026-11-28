# Review: best even polygon vs disk under geometric and uniform horizon mixtures, n up to ~1e5 (dpmix.c output). OBSERVED.
import numpy as np, math
QS=[0.99,0.993,0.995,0.996,0.997,0.998,0.999,0.9995]; HS=[200,500,1000,2000]
R=np.loadtxt("mix_raw.txt"); R=R[np.argsort(R[:,0])]; ns=R[:,0].astype(int)
T=np.arange(1,80_000_001,dtype=float); dk=T*np.sin(np.pi/(2*T))**2
print(f"n computed: {len(ns)} even values, {ns.min()}..{ns.max()} (n=2 mod 4 at ~0.5-1% spacing; n=0 mod 4 at 2%; all n=2 mod 4 in 402..2002)")
for i,q in enumerate(QS):
    ed=float(np.sum((1-q)*q**(T-1)*dk)); col=R[:,1+i]; j=int(np.argmin(col)); nb=ns[j]
    M=1/(1-q)
    print(f"geometric q={q} (mean {M:.0f}): disk={ed:.10f} best n={nb} (mod4={nb%4}) cost={col[j]:.10f} -> {'POLYGON' if col[j]<ed else 'disk'} cheaper, rel margin {(ed-col[j])/ed:+.3e}; interior={0<j<len(ns)-1}; n*/M^2={nb/M**2:.3f}; rel margin/(1-q)^2={(ed-col[j])/ed/(1-q)**2:.1f}")
for h,H in enumerate(HS):
    ed=np.mean([t*math.sin(math.pi/(2*t))**2 for t in range(1,H+1)]); col=R[:,1+len(QS)+h]; j=int(np.argmin(col)); nb=ns[j]
    print(f"uniform 1..{H}: disk={ed:.10f} best n={nb} cost={col[j]:.10f} -> {'POLYGON' if col[j]<ed else 'disk'} cheaper, rel margin {(ed-col[j])/ed:+.3e}; interior={0<j<len(ns)-1}")
i1002=list(ns).index(1002); print("check n=1002 q=0.99:",R[i1002,1],"(mix_review.py gave 0.09615495)")
