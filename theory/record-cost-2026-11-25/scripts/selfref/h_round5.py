"""H: round 5. Price the destruction that selection needs.
H1 single-feature selection: min destruction to move a feature's share from its base rate p0 (in the invariant state)
   to s. Claim: = binary relative entropy D(s||p0), in every world tested (Shannon/von Neumann; GPTs via measurement entropy).
H2 multi-feature selection at fixed destruction: square, disk/ball, classical.
H3 maintenance against unknown noise at matched contraction of the feature bias.
H4 infinite reversible CA boundary budget: learned + selected <= inflow capacity (random bijections).
H5 zero-drift comparison at matched destruction budget.
"""
import numpy as np, itertools
rng=np.random.default_rng(5)
def h(p):
    p=np.clip(p,1e-15,1-1e-15); return -(p*np.log2(p)+(1-p)*np.log2(1-p))
def H(v):
    v=np.asarray(v,float); v=v[v>1e-15]; return -(v*np.log2(v)).sum()
def Dbin(s,p): return s*np.log2(s/p)+(1-s)*np.log2((1-s)/(1-p))
print("H1 min destruction to raise a feature's share from base rate p0 to s (bits)")
print(" world                     p0      s=0.6    s=0.8    s=0.95   D(s||p0) at s=0.8")
# classical n states, feature = k states: maximise Shannon entropy with mass s on k states
for n,k in [(2,1),(4,1),(4,2),(8,1)]:
    row=[np.log2(n)-(h(s)+s*np.log2(k)+(1-s)*np.log2(n-k)) for s in (0.6,0.8,0.95)]
    print(f" classical n={n} k={k}        {k/n:5.3f}  "+"  ".join(f"{x:7.4f}" for x in row),f"  {Dbin(0.8,k/n):.4f}")
# quantum d-level, rank-1 projector feature; numeric: random states with <P>=s, max von Neumann entropy (search)
for d in (2,3):
    best={}
    for s in (0.6,0.8,0.95):
        bestS=-1
        for _ in range(4000):
            # random state, then mix to hit <P>=s exactly: rho = s|0><0| + (1-s) sigma on complement, plus random coherences test
            G=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); r=G@G.conj().T; r/=np.trace(r)
            p=np.real(r[0,0])
            if p<=1e-6 or p>=1-1e-6: continue
            # rescale block weights to make <P>=s while keeping positivity: congruence by diag(sqrt(s/p), sqrt((1-s)/(1-p))...)
            D_=np.diag([np.sqrt(s/p)]+[np.sqrt((1-s)/(1-p))]*(d-1)); r2=D_@r@D_
            w=np.linalg.eigvalsh(r2); S=H(np.clip(w,0,1)); bestS=max(bestS,S)
        best[s]=np.log2(d)-bestS
    print(f" quantum d={d} (numeric)    {1/d:5.3f}  "+"  ".join(f"{best[s]:7.4f}" for s in (0.6,0.8,0.95)),f"  {Dbin(0.8,1/d):.4f}")
# square (gbit) states (x,y) in [0,1]^2 ; measurement entropy = min over fine-grained measurements = min(h(x),h(y)); mu=(.5,.5)
# disk: Bloch vector r in unit disk, feature along e1, fine-grained measurements = antipodal pairs; H_meas = h((1+|r|)/2)
for name,Hm in [("square (meas. entropy)",lambda x,y: min(h(x),h(y))),("disk/ball (meas. entropy)",lambda x,y: h((1+np.hypot(2*x-1,2*y-1))/2) if np.hypot(2*x-1,2*y-1)<=1 else -9)]:
    g=np.linspace(0.0005,0.9995,2000); row=[]
    for s in (0.6,0.8,0.95): row.append(1-max(Hm(s,y) for y in g))
    print(f" {name:26s}0.500  "+"  ".join(f"{x:7.4f}" for x in row),f"  {Dbin(0.8,0.5):.4f}")
print("\nH2 select m features at once to share s each; destruction (bits), measurement entropy where GPT")
for s in (0.55,0.6,0.7):
    sq=1-h(s)                                   # state (s,s): both square features at s, H_meas=min(h(s),h(s))
    b=2*s-1; disk2=1-h((1+np.sqrt(2)*b)/2) if np.sqrt(2)*b<=1 else np.nan   # Bloch (b,b) in disk
    ball3=1-h((1+np.sqrt(3)*b)/2) if np.sqrt(3)*b<=1 else np.nan
    cl2=2*(1-h(s)); cl3=3*(1-h(s))
    print(f" s={s}: single feature {1-h(s):.4f} | m=2: square {sq:.4f}, disk/ball {disk2:.4f}, classical 2 bits {cl2:.4f}"
          f" | m=3: ball {ball3:.4f}, classical 3 bits {cl3:.4f}")
print(" small-bias ratios (s=0.5+eps, eps=1e-3): ball m=2 / single =",round((1-h(0.5+np.sqrt(2)*1e-3))/(1-h(0.5+1e-3)),4),
      "; classical m=2 / single = 2 ; square m=2 / single = 1")
print("\nH3 hold share s against unknown noise; matched contraction c of the bias per tick; destruction per tick to restore")
for s in (0.6,0.8):
    for c in (0.9,0.5):
        b=2*s-1; bc=c*b
        bitflip=h((1+bc)/2)-h(s)                  # classical bit, symmetric flip contracting bias by c
        depol=h((1+bc)/2)-h(s)                    # qubit depolarising, Bloch length b -> c b
        # qubit: unknown rotation about an axis orthogonal to the feature, angle ~ N(0,sig^2) with E cos = c: Bloch -> (b*c along feature, 0)
        rot=h((1+bc)/2)-h(s)                      # averaged state has Bloch length c*b (sin terms average to 0)
        # square: noise flipping x with prob (1-c)/2, y untouched
        sqn=min(h((1+bc)/2),1)-min(h(s),1)
        print(f" s={s} c={c}: classical {bitflip:.4f} | qubit depolarising {depol:.4f} | qubit random rotation {rot:.4f} | square {sqn:.4f}")
print("\nH4 infinite reversible CA: region R (r bits) + inflow (k bits) -> bijection -> R' + outflow (k bits)")
def ent_joint(P): return H(P.ravel())
worst=-9; cnt=0
for trial in range(3000):
    r=rng.integers(1,3); k=rng.integers(1,3); nR=2**r; nI=2**k
    pR=rng.dirichlet(np.ones(nR)*rng.uniform(.2,3)); pI=rng.dirichlet(np.ones(nI)*rng.uniform(.2,3))
    perm=rng.permutation(nR*nI)                       # bijection on (R,in) -> (R',out)
    J=np.zeros((nR,nI,nR,nI))                         # joint over (R', in) for learning, keep in-index
    for a in range(nR):
        for i in range(nI):
            y=perm[a*nI+i]; J[y//nI, i, a, i]+=0  # placeholder
    PRpI=np.zeros((nR,nI))                            # P(R', in)
    for a in range(nR):
        for i in range(nI):
            y=perm[a*nI+i]; PRpI[y//nI,i]+=pR[a]*pI[i]
    HRp=H(PRpI.sum(1)); L=HRp+H(pI)-ent_joint(PRpI)   # learned = I(R';in)
    Delta=H(pR)-HRp                                   # local destruction = selection budget
    worst=max(worst,L+Delta-k); cnt+=1
    assert Delta<=k-H(pI)+1e-9
print(f" {cnt} random bijections: max (learned + local entropy drop - k*log2 a) = {worst:.2e}  (<= 0 predicted); Delta <= k - H(in) held in all")
# example: 1-bit inflow, swap tracker learns 1 bit; then demand selection Delta
for Delta in (0,0.25,0.5):
    print(f"  1-bit channel, selection Delta={Delta}: learning rate <= {1-Delta}")
print("\nH5 zero external drift, matched destruction budget (q=4 questions/tick, kappa=1, answers overwritten: c=4 bits common)")
rows=[("classical 1 bit",0.25,0.0),("square (long run)",0.25,1.0),("ball eta=1 (long run)",0.29,0.0)]
for name,e,once in rows: print(f" {name:22s} error {e:.2f}  J = 1 + 4*{e:.2f} = {1+4*e:.2f}  + common answer erasure 4  + one-off destruction {once}")
print(" selection term (H1) is the same D(s||1/2) for all three at a base-rate-1/2 feature: adds equally, ordering unchanged")
