"""K: round 8.
K1 quantifier order: a pure state fixed by ALL laws in a neighbourhood (finite-precision knowledge) vs one per law.
K2 bounded vs growing error under an imprecisely known law: ball (record near the true axis) vs disk.
K3 Jordan-class table: plain SFP, record-SFP (fixed perfectly distinguishable pair, mixed allowed), hereditary (2-level faces).
K4 counterexample: tetrahedron with transitive Klein group V4 (record-SFP with mixed records passes; pure SFP fails).
"""
import numpy as np, itertools
from scipy.stats import special_ortho_group, ortho_group
from scipy.spatial.transform import Rotation as Rot
rng=np.random.default_rng(8)
print("K1 common fixed pure states of two nearby laws g, g' (SO(3), distance ~1e-3)")
cnt=0
for _ in range(1000):
    g=Rot.random(random_state=rng); dg=Rot.from_rotvec(rng.normal(size=3)*1e-3); g2=dg*g
    a1=g.as_rotvec(); a2=g2.as_rotvec(); a1/=np.linalg.norm(a1); a2/=np.linalg.norm(a2)
    cnt+= abs(abs(a1@a2)-1)<1e-12
print(f"  pairs sharing a fixed pure state: {cnt}/1000  -> 'one pattern fixed by every law consistent with finite records' leaves only the centre")
print("\nK2 law = rotation by theta about an axis, known to precision delta; record placed using the estimate; error after t ticks")
theta=0.3; delta=1e-3
for t in (10,100,1000,10000):
    # disk: record at angle 0, compensate with estimated theta_hat=theta+delta
    disk=abs(2*np.sin(t*delta/2))
    # ball: record at estimated axis, which is off the true axis by delta; it circles the true axis
    true=Rot.from_rotvec(np.array([0,0,1.])*theta); rec=np.array([np.sin(delta),0,np.cos(delta)])
    traj=[(true**k).apply(rec) for k in range(0,t+1,max(1,t//200))]
    ball=max(np.linalg.norm(p-rec) for p in traj)
    print(f"  t={t:6d}: disk error {disk:.4f} (grows ~ t*delta) | ball error <= {ball:.4f} (bounded by 2*sin(delta)={2*np.sin(delta):.4f})")
print("\nK3 Jordan-class / ball table (sampled group elements; 'pair' = fixed perfectly distinguishable pair, mixed allowed)")
def fixed_pair_realQM(O):
    # rho fixed by O.O^T: commutant; distinguishable pair exists iff O has >= 2 invariant real subspaces (isotypic split); here: eigen-structure
    w=np.linalg.eigvals(O); 
    # number of real invariant blocks = (#real eigenvalues) + (#complex pairs)
    nreal=sum(abs(x.imag)<1e-9 for x in w); ncpx=(len(w)-nreal)//2
    return nreal+ncpx>=2
def has_real_ev(O): return any(abs(x.imag)<1e-9 for x in np.linalg.eigvals(O))
rows=[]
for d in (2,3,4):
    s=[ortho_group.rvs(d,random_state=rng) for _ in range(2000)]
    rows.append((f"real QM d={d} (dim {d*(d+1)//2-1})", np.mean([has_real_ev(O) for O in s]), np.mean([fixed_pair_realQM(O) for O in s]), "rebit faces fail" if d>=2 else ""))
for n in (3,4,5,6,7,8):
    s=[special_ortho_group.rvs(n,random_state=rng) for _ in range(2000)]
    f=np.mean([np.min(abs(np.linalg.eigvals(R)-1))<1e-8 for R in s])
    rows.append((f"ball B^{n} with SO({n})", f, f, "no proper faces"))
rows.append(("complex QM d=2,3 (dims 3,8)",1.0,1.0,"faces complex: pass"))
rows.append(("quaternionic QM d=2 (=B^5), d=3 (dim 14)",1.0,1.0,"faces B^5: pass"))
rows.append(("octonionic d=3 (dim 26)",1.0,1.0,"faces B^9: pass (F4/Spin(9) equal rank)"))
for k in (2,3,4):
    perms=list(itertools.permutations(range(k)))
    pure=np.mean([any(p[i]==i for i in range(k)) for p in perms])
    def cycles(p):
        seen=set(); c=0
        for i in range(k):
            if i not in seen:
                c+=1; j=i
                while j not in seen: seen.add(j); j=p[j]
        return c
    pair=np.mean([cycles(p)>=2 for p in perms])
    rows.append((f"simplex, {k} outcomes, full S_{k}",pure,pair,"n-cycle fixes only the centre"))
print(f"  {'state space':44s} pure-SFP  record-SFP  heredity")
for r in rows: print(f"  {r[0]:44s} {r[1]:7.3f}   {r[2]:7.3f}    {r[3]}")
print("\nK4 tetrahedron with the transitive Klein group V4 = {e,(01)(23),(02)(13),(03)(12)}")
V4=[(0,1,2,3),(1,0,3,2),(2,3,0,1),(3,2,1,0)]
for p in V4[1:]:
    fixv=[i for i in range(4) if p[i]==i]; pairs=[(i,p[i]) for i in range(4) if i<p[i]]
    print(f"  {p}: fixed vertices {fixv}; fixed distinguishable mixed pair {pairs[0]}-average vs {pairs[1]}-average")
print("  -> transitive, every law fixes a distinguishable (mixed) pair, no law except e fixes a pure state.")
