"""i1: stochastic internal-model theorem, exact checks.
I1 excess log loss over L-block = I(S;X_{1:L}|M)  (M a function of the past)
I3 P(g(M)!=S) <= sqrt(2*delta_nats)/gamma   (gamma = min TV between causal-state L-block laws)
   homomorphism violation <= 2*sqrt(2 delta)/gamma
I4 Fano: I(M;S) >= H(S) - h(Pe) - Pe log(|S|-1)
I2 delta=0 => exact homomorphism (golden mean, k=1)
Counterexamples: Hamming loss on Even process (no model needed); SNS (nonunifilar, never exact).
"""
import itertools, numpy as np
rng=np.random.default_rng(7)
LN2=np.log(2)
def H(p):
    p=np.asarray(p,float).ravel(); p=p[p>1e-300]; return -(p*np.log(p)).sum()
def stationary(T):
    M=sum(T.values()); w,v=np.linalg.eig(M.T); i=np.argmin(abs(w-1)); pi=np.real(v[:,i]); return pi/pi.sum()
def block_probs(T,start,L):
    """dict word -> vector over states: start @ T^{x1}...T^{xL}"""
    out={():start}
    for _ in range(L):
        new={}
        for w,v in out.items():
            for x,Tx in T.items(): new[w+(x,)]=v@Tx
        out=new
    return out
def future_given_state(T,ns,L):
    words=list(itertools.product(sorted(T),repeat=L))
    F=np.zeros((ns,len(words)))
    for s in range(ns):
        e=np.zeros(ns); e[s]=1
        bp=block_probs(T,e,L)
        for j,w in enumerate(words): F[s,j]=bp[w].sum()
    return F,words
def analyse(name,T,ns,k,L,next_state=None):
    pi=stationary(T)
    J=block_probs(T,pi,k)               # P(window w, S_t=s)
    wins=[w for w in J if J[w].sum()>1e-15]
    P=np.array([J[w] for w in wins])    # rows windows, cols states
    F,_=future_given_state(T,ns,L)
    PS=P.sum(0); Pm=P.sum(1)
    # delta = I(S;Fut|M) = H(Fut|M)-H(Fut|S)  (S screens past, M fn of past)
    HfutS=sum(PS[s]*H(F[s]) for s in range(ns))
    HfutM=sum(Pm[i]*H((P[i]/Pm[i])@F) for i in range(len(wins)))
    delta=HfutM-HfutS
    # direct excess log loss with optimal q(.|m)
    ex=0
    for i in range(len(wins)):
        q=(P[i]/Pm[i])@F
        for s in range(ns):
            if P[i,s]>0:
                f=F[s]; m=f>0; ex+=P[i,s]*(f[m]*np.log(f[m]/q[m])).sum()
    TV=[0.5*abs(F[a]-F[b]).sum() for a in range(ns) for b in range(ns) if a<b]
    gamma=min(TV)
    g=P.argmax(1); Pe=1-sum(P[i,g[i]] for i in range(len(wins)))
    IMS=H(PS)+H(Pm)-H(P)
    fano=H(PS)-H([Pe,1-Pe])-(Pe*np.log(ns-1) if ns>2 else 0)
    bnd=np.sqrt(2*max(delta,0))/gamma if gamma>0 else np.inf
    hv=None
    if next_state is not None:
        idx={w:i for i,w in enumerate(wins)}; hv=0
        for i,w in enumerate(wins):
            for s in range(ns):
                if P[i,s]==0: continue
                for x,Tx in T.items():
                    px=Tx[s].sum()
                    if px==0: continue
                    w2=(w+(x,))[1:] if k>0 else ()
                    if w2 not in idx: continue
                    if g[idx[w2]]!=next_state(g[i],x): hv+=P[i,s]*px
    ok=abs(ex-delta)<1e-9 and Pe<=bnd+1e-12 and IMS>=fano-1e-12 and (hv is None or hv<=2*bnd+1e-12)
    print(f"{name:10s} k={k:2d} L={L} delta={delta/LN2:9.6f}b ex={ex/LN2:9.6f}b Pe={Pe:7.4f} bound={min(bnd,9):7.4f} "
          f"I(M;S)={IMS/LN2:6.4f}b H(S)={H(PS)/LN2:6.4f}b Fano>={fano/LN2:7.4f} hom_viol={hv if hv is None else round(hv,4)} gamma={gamma:.3f} {'OK' if ok else 'FAIL'}")
    return ok,delta,Pe
allok=True
# Even process: A --0(1/2)--> A, A --1(1/2)--> B, B --1--> A
TE={0:np.array([[.5,0],[0,0]]),1:np.array([[0,.5],[1,0]])}
nsE=lambda s,x: 0 if s==1 else (0 if x==0 else 1)
print("== Even process (causal states A,B; C_mu = H(2/3,1/3)) ==")
for k in [0,1,2,3,4,6,8,10]:
    ok,_,_=analyse("Even",TE,2,k,4,nsE); allok&=ok
# Golden mean: A --0(1/2)-->B, A --1(1/2)-->A, B --1-->A (no 00). Markov order 1.
TG={0:np.array([[0,.5],[0,0]]),1:np.array([[.5,0],[1,0]])}
nsG=lambda s,x: 1 if x==0 else 0
print("== Golden mean (order-1 Markov) : I2 exact homomorphism at k>=1 ==")
for k in [0,1,2]:
    ok,d,Pe=analyse("Golden",TG,2,k,4,nsG); allok&=ok
    if k>=1: allok&= (abs(d)<1e-12 and Pe<1e-12)
# random 4-state unifilar HMM over binary alphabet
print("== random 4-state unifilar machine ==")
ns=4
for trial in range(12):
    T={0:np.zeros((ns,ns)),1:np.zeros((ns,ns))}; dest={}
    for s in range(ns):
        p=rng.uniform(.15,.85)
        for x,px in [(0,p),(1,1-p)]:
            d=rng.integers(ns); T[x][s,d]=px; dest[(s,x)]=d
    M=sum(T.values())
    if np.linalg.matrix_rank(np.eye(ns)-M)!=ns-1 or stationary(T).min()<0.05: continue
    for k in [0,2,4,6,8]:
        ok,_,_=analyse(f"rand{trial}",T,ns,k,3,lambda s,x,dest=dest: dest[(s,x)]); allok&=ok
# Counterexample 1: Hamming loss next symbol, Even process. Bayes act = 1 in both states.
pi=stationary(TE); p1=[TE[1][s].sum() for s in range(2)]
print("== FAILS-direction counterexample: Hamming loss on Even process ==")
print(f"P(next=1|A)={p1[0]:.2f}, P(next=1|B)={p1[1]:.2f}: 'always predict 1' is Bayes-optimal in every causal state;"
      f" memoryless agent has zero excess Hamming risk and I(M;S)=0.  -> model of S NOT forced by this loss")
# Counterexample 2: Simple Nonunifilar Source (infinitely many causal states)
# HMM states A,B: A -1(1/2)->A, A -1(1/2)->B, B -1(1/2)->B, B -0(1/2)->A
TS={1:np.array([[.5,.5],[0,.5]]),0:np.array([[0,0],[.5,0]])}
pi=stationary(TS)
print("== Simple nonunifilar source: delta_k = I(past;future_L | last k) estimated with past=K=16 ==")
def Hblock_cond(T,pi,k,L):
    # H(X_{1:L} | last k symbols)
    J=block_probs(T,pi,k+L); Hj=H([v.sum() for v in J.values()])
    Jk=block_probs(T,pi,k); Hk=H([v.sum() for v in Jk.values()]); return Hj-Hk
L=3; HK=Hblock_cond(TS,pi,16,L); prev=None; mono=True
for k in [0,1,2,4,6,8,10,12]:
    d=(Hblock_cond(TS,pi,k,L)-HK)/LN2
    print(f"  k={k:2d} delta_k ~ {d:.6f} bits"); mono&= (prev is None or d<=prev+1e-12) and d>0 if k<16 else True; prev=d
allok&=mono
print("finite-k agents never exact (delta_k>0, decreasing) -> exact homomorphism impossible for finite memory; I3 holds only with approximate states")
print("ALL", "OK" if allok else "FAIL")
