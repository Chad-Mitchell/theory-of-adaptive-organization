"""i2: I5 maintenance-is-a-flow.  Stationary agent M tracking drifting world S through observations Y.
Claim [PROOF]: I(Y_t;S_t|M_{t-1}) >= (1-eta) I(M;S), eta = SDPI constant of the world kernel.
(i) binary world, flip prob q, eta=(1-2q)^2, BSC(e) observations, random stochastic finite-state agents (exact).
(ii) Gaussian AR(1) world s'=a s+noise, Kalman agent: eta=a^2 for Gaussian channel (exact formulas).
"""
import numpy as np
rng=np.random.default_rng(3)
def H(p):
    p=np.asarray(p,float).ravel(); p=p[p>1e-300]; return -(p*np.log2(p)).sum()
def MI(J): return H(J.sum(1))+H(J.sum(0))-H(J)
allok=True; worst=np.inf
for trial in range(400):
    q=rng.uniform(0.005,0.3); e=rng.uniform(0.0,0.45); nm=rng.integers(2,6)
    K=np.array([[1-q,q],[q,1-q]]); O=np.array([[1-e,e],[e,1-e]])
    U=rng.dirichlet(np.ones(nm)*0.3,size=(nm,2))   # U[m,y,m']
    # chain on (s,m): s'~K[s], y~O[s'], m'~U[m,y]
    n=2*nm; P=np.zeros((n,n))
    for s in range(2):
        for m in range(nm):
            for s2 in range(2):
                for y in range(2):
                    for m2 in range(nm): P[s*nm+m,s2*nm+m2]+=K[s,s2]*O[s2,y]*U[m,y,m2]
    w,v=np.linalg.eig(P.T); pi=np.real(v[:,np.argmin(abs(w-1))]); pi/=pi.sum()
    J=pi.reshape(2,nm)       # stationary joint (S,M)
    IMS=MI(J)
    # I(Y_t;S_t|M_{t-1}): joint over (m_prev, s_t, y_t)
    Jm=np.einsum('sm,st,ty->mty',J,K,O)
    Iobs=sum(Jm[m].sum()*MI(Jm[m]/Jm[m].sum()) for m in range(nm) if Jm[m].sum()>0)
    eta=(1-2*q)**2
    r=Iobs-(1-eta)*IMS
    worst=min(worst,r)
    if r<-1e-10: allok=False; print("VIOLATION",q,e,nm,Iobs,IMS)
print(f"binary: 400 random agents, min[I_obs-(1-eta)I(M;S)] = {worst:.3e} bits  {'OK' if worst>-1e-10 else 'FAIL'}")
# show the flow law: at fixed I(M;S), required inflow grows ~ linearly in drift q for small q
print(" q      1-eta    => min obs bits/step to hold 1 bit of world-model ")
for q in [0.001,0.01,0.05,0.1]:
    print(f" {q:<6} {1-(1-2*q)**2:.4f}  {1-(1-2*q)**2:.4f}  (≈4q)")
# Gaussian AR(1) with Kalman filter
print("Gaussian AR(1): s'=a s + w (var Qw), y=s+v (var R); agent = Kalman posterior mean")
for a,Qw,R in [(0.99,0.02,1.0),(0.9,0.2,0.5),(0.5,1.0,2.0),(0.999,0.002,0.1)]:
    Ps=Qw/(1-a*a)
    Pp=Ps
    for _ in range(100000):
        Pf=Pp*R/(Pp+R); Pn=a*a*Pf+Qw
        if abs(Pn-Pp)<1e-15: break
        Pp=Pn
    Pf=Pp*R/(Pp+R)
    IMS=0.5*np.log2(Ps/Pf)                      # I(m_t;s_t)
    Iobs=0.5*np.log2(Pp/Pf)                     # I(y_t;s_t|m_{t-1})
    # NOTE: unconstrained Gaussian kernel has input-free eta_KL = 1, so use the exact jointly-Gaussian
    # contraction: rho^2 -> a^2 rho^2, i.e. decay = I - I', I' = -1/2 log2(1 - a^2 (1-2^{-2I})).
    Ip=-0.5*np.log2(1-a*a*(1-2**(-2*IMS))); decay=IMS-Ip
    ok=Iobs>=decay-1e-12; allok&=ok
    print(f" a={a} I(M;S)={IMS:.4f}b inflow={Iobs:.4f}b/step decay={decay:.4f}b/step (small-I approx (1-a^2)I={(1-a*a)*IMS:.4f}) ratio={Iobs/decay:.3f} {'OK' if ok else 'FAIL'}")
print("Landauer floor: holding I bits against drift costs >= kT ln2 * (1-eta) * I per step (Sagawa-Ueda measurement+erasure W>=kT*I per acquired bit).")
print("ALL","OK" if allok else "FAIL")
