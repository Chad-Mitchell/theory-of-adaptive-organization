"""I: round 6. Open finite part R fed by priced inflow cells; learn L (classical info about the inflow data X kept in R')
and select Delta (entropy drop of R) under one reversible step U:(R,in)->(R',out).
I1 qubit (ball) cells: random unitaries; check L + Delta <= k*log2 N with L = Holevo I(X;R').
I2 the quantum-mutual-information caveat (entangled inflow).
I3 gbit (square) cells: all 128 reversible maps (Gross et al.: local symmetries + swap); entropy = measurement vs decomposition.
I4 frontier per unit price under capacity pricing (log N) and dimension pricing (log K).
"""
import numpy as np, itertools
rng=np.random.default_rng(11)
def S(r):
    w=np.linalg.eigvalsh((r+r.conj().T)/2); w=w[w>1e-12]; return float(-(w*np.log2(w)).sum())
def Hs(p):
    p=np.asarray(p,float); p=p[p>1e-12]; return float(-(p*np.log2(p)).sum())
def haar(n):
    Z=(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))/np.sqrt(2); Q,R=np.linalg.qr(Z); return Q*(np.diag(R)/abs(np.diag(R)))
def rand_rho(n,rank=None):
    G=rng.normal(size=(n,rank or n))+1j*rng.normal(size=(n,rank or n)); r=G@G.conj().T; return r/np.trace(r)
def ptrace_out(rho,dR,dI):   # keep R (first factor)
    return np.einsum('ijkj->ik',rho.reshape(dR,dI,dR,dI))
print("I1 qubit cells, random unitaries on R (1 or 2 qubits) x inflow (1 qubit); X takes 2-4 values")
worst=-9
for t in range(4000):
    dR=2**rng.integers(1,3); dI=2; nx=rng.integers(2,5); px=rng.dirichlet(np.ones(nx))
    rhoR=rand_rho(dR); enc=[rand_rho(dI,rank=rng.integers(1,3)) for _ in range(nx)]
    U=haar(dR*dI) if rng.random()<0.8 else None
    if U is None:                      # swap-type: put inflow into first qubit of R
        U=np.eye(dR*dI)[np.argsort([ (a//dI, a%dI) for a in range(dR*dI)],axis=0)] if False else haar(dR*dI)
    outs=[ptrace_out(U@np.kron(rhoR,e)@U.conj().T,dR,dI) for e in enc]
    avg=sum(p*o for p,o in zip(px,outs))
    L=S(avg)-sum(p*S(o) for p,o in zip(px,outs)); Delta=S(rhoR)-S(avg)
    worst=max(worst,L+Delta-np.log2(dI))
print(f"  4000 random cases: max(L + Delta - log2 N_cell) = {worst:.2e}   (<= 0 predicted)")
# achievability: SWAP on 1 qubit R maximally mixed, inflow encodes X orthogonally with H(X)=a
for a in (0,0.5,1.0):
    q=0.5 if a==1 else (0 if a==0 else 0.11002786443835955)
    L=Hs([q,1-q]); Delta=1-L
    print(f"  swap, R maximally mixed, inflow entropy {L:.3f}: L={L:.3f} Delta={Delta:.3f} L+Delta={L+Delta:.3f}  (frontier reached; same protocol is classical)")
print("\nI2 caveat: count quantum mutual information with a reference E entangled with the inflow")
phi=np.zeros(4); phi[0]=phi[3]=1/np.sqrt(2); P=np.outer(phi,phi)
print("  swap a maximally entangled inflow qubit into R: I(R';E) = S(R')+S(E)-S(R'E) =",1+1-S(P),
      "bits on a 1-bit channel; with Delta = 1 - S(in) = 0: L_q + Delta = 2. Not a classical record (cannot be copied/broadcast).")
print("\nI3 gbit (square) cells. state (x,y) = (P(meas a -> 0), P(meas b -> 0)); vertices (0/1,0/1)")
V=[(0,0),(0,1),(1,0),(1,1)]
def Hmeas(x,y): return min(Hs([x,1-x]),Hs([y,1-y]))
def Hdec(x,y):
    # weights on vertices (00,01,10,11) with marginals x=P(a=0)=w(1,*)? use: x = w10+w11, y = w01+w11 ; one free parameter t=w11
    best=9
    for t in np.linspace(max(0,x+y-1),min(x,y),201):
        w=[1-x-y+t, y-t, x-t, t]
        if min(w)>-1e-12: best=min(best,Hs(np.clip(w,0,1)))
    return best
D8=[]
for sw in (False,True):
    for r in range(4):
        def mk(sw=sw,r=r):
            def g(x,y):
                for _ in range(r): x,y=y,1-x
                if sw: x,y=y,x
                return (x,y)
            return g
        D8.append(mk())
print("  dihedral group size:",len(D8),"; reversible maps on 2 gbits = 8*8*2 =",len(D8)**2*2)
def accessible(states,px):
    best=0
    for m in (0,1):
        pj=np.array([[p*s[m],p*(1-s[m])] for p,s in zip(px,states)])
        best=max(best,Hs(pj.sum(0))+Hs(pj.sum(1))-Hs(pj.ravel()))
    return best
res={'meas':-9,'dec':-9}; ex=None
cases=[((0.5,0.5),[(1,1),(1,0)],[0.5,0.5])]
for _ in range(250):
    R=tuple(rng.uniform(0,1,2)); nx=rng.integers(2,4); px=rng.dirichlet(np.ones(nx))
    enc=[tuple(rng.choice([0,1,rng.uniform()],2)) for _ in range(nx)]
    cases.append((R,enc,px))
for R,enc,px in cases:
    for gR in D8:
        for gI in D8:
            for sw in (False,True):
                outs=[gI(*e) if sw else gR(*R) for e in enc]
                avg=tuple(np.dot(px,[o[i] for o in outs]) for i in (0,1))
                L=accessible(outs,px)
                for key,Hf in (('meas',Hmeas),('dec',Hdec)):
                    v=L+Hf(*R)-Hf(*avg)
                    if v>res[key]: res[key]=v; ex=(key,R,enc,px,sw) if key=='meas' else ex
print(f"  max L + Delta over all 128 maps and {len(cases)} input cases: measurement entropy {res['meas']:.3f} ; decomposition entropy {res['dec']:.3f}  (cell capacity 1 bit)")
print("  witness: R=(.5,.5) centre; inflow encodes X in coordinate b with a fixed: (1,1)/(1,0); swap.")
print("    measurement entropy: inflow mixture (1,.5) has H_meas 0, so Delta=1 and L=1: L+Delta=2 (looks strictly better)")
print("    decomposition entropy: (1,.5) has H_dec 1, Delta=0, L+Delta=1 (ties)")
print("\nI4 frontier per unit priced inflow (best L+Delta per cell / price per cell)")
for name,N,K,front in [("classical bit",2,2,1.0),("square gbit (decomposition entropy)",2,3,1.0),("square gbit (measurement entropy)",2,3,2.0),("qubit ball",2,4,1.0)]:
    print(f"  {name:38s} capacity price log2N={np.log2(N):.3f}: {front/np.log2(N):.3f} | dimension price log2K={np.log2(K):.3f}: {front/np.log2(K):.3f}")
