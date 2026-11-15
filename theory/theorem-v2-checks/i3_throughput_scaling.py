"""i3: (A) optimal model size vs stakes for a power-law world (reverse water-filling) -> bits ∝ (w/kappa)^(1/beta)
(B) spectral bridge: a 1/f^alpha world in d dims has rank spectrum lambda_i ∝ i^(-alpha/d)  => beta = alpha/d
(C) cross-scale chain predictions vs fetched data
(D) Kelly with overround v: growth = D(p||r~) - ln(1+v) + I(X;Y); MC check; blind viable iff D>ln(1+v)"""
import numpy as np
rng=np.random.default_rng(11); allok=True
LN2=np.log(2)
def model(w,kappa,lam):
    th=kappa/(2*LN2*w)                       # water level
    on=lam>th
    bits=0.5*np.log2(lam[on]/th).sum()
    loss=w*np.minimum(lam,th).sum()
    return on.sum(),bits,loss,kappa*bits
print("(A) reverse water-filling, lambda_i=i^-beta, N=10^6 components")
N=10**6; i=np.arange(1,N+1)
for beta in [0.5,0.9,1.0,1.5,2.0]:
    lam=i**(-beta); wmax=(N/5)**beta/(2*LN2); W=np.logspace(np.log10(wmax)-3*min(1,beta),np.log10(wmax),7); B=[]; 
    for w in W: n,b,l,c=model(w,1.0,lam); B.append(b)
    slope=np.polyfit(np.log(W),np.log(B),1)[0]
    n,b,_,_=model(W[-2],1.0,lam); ratio=b/n
    ok=abs(slope-1/beta)<0.03 and abs(ratio-beta/(2*LN2))<0.05*beta/(2*LN2)+0.02; allok&=ok
    print(f"  beta={beta}: d log bits/d log w = {slope:.4f} (theory 1/beta={1/beta:.4f}); bits/n* = {ratio:.4f} (theory beta/(2ln2)={beta/(2*LN2):.4f}) {'OK' if ok else 'FAIL'}")
print("  finite-dimensional world (n modes, flat): bits = (n/2)log2(w/w0) -> LOG growth, no power law")
lam=np.ones(20); W=np.logspace(2,5,7); B=[model(w,1.0,lam)[1] for w in W]
print("   bits per decade of w:",np.round(np.diff(B),3))
print("(B) spectral bridge: simulate 2-D field with power spectrum k^-alpha, rank-order Fourier mode variances")
for alpha,d in [(1.81,2),(2.0,2),(1.0,1),(2.0,1)]:
    n=256 if d==2 else 2**16
    ks=np.fft.fftfreq(n)*n
    if d==2: K=np.sqrt(ks[:,None]**2+ks[None,:]**2).ravel()
    else: K=abs(ks)
    K=K[K>0]; var=np.sort(K**(-alpha))[::-1]; r=np.arange(1,len(var)+1)
    sel=(r>10)&(r<len(var)/10)
    sl=-np.polyfit(np.log(r[sel]),np.log(var[sel]),1)[0]
    ok=abs(sl-alpha/d)<0.03; allok&=ok
    print(f"  alpha={alpha}, d={d}: fitted beta={sl:.3f}, theory alpha/d={alpha/d:.3f} {'OK' if ok else 'FAIL'}")
print("(C) chain: model bits ∝ (stakes)^(1/beta); stakes ∝ throughput Q (ASSUMPTION A-w)")
rows=[("vision, Ruderman-Bialek 1994 alpha=1.81 (2-D)",1.81/2),("1/f temporal noise (1-D)",1.0),("1/f^2 (Brownian) 1-D",2.0)]
for nm,b in rows: print(f"  {nm}: beta={b:.3f} -> model exponent vs Q = {1/b:.3f}; with WBE Q∝M^0.75 -> model ∝ M^{0.75/b:.3f}")
print("  DATA (fetched): brain mass ∝ M^0.75 (Martin 1981); brain energy ∝ Vbrain^0.86 (Karbowski 2007) -> brain energy ∝ M^0.645;")
print("    neurons ∝ brain energy (Herculano-Houzel 2011, ~constant per-neuron glucose) -> model size ∝ Q^0.86 (if Q∝M^0.75)")
print("    implied beta (brain-energy reading) = 1/0.86 = %.2f ; (brain-mass reading) beta = 1.00"%(1/0.86))
print("  Cities: GDP ∝ N^1.13-1.26 (Bettencourt 2007 Tbl1); admin staff ∝ N^~1.2 (Hutcheson & Prather 1979, abstract-level)")
for g in [1.13,1.26]: print(f"    beta=1 predicts admin ∝ N^{g:.2f}; implied beta from 1.2: {g/1.2:.3f}")
print("  Firms: Blau 1970 administrative ratio FALLS with size; Zhang-Kempes-Hamilton-Tao-West: sales ∝ assets^0.90, employees ∝ assets^0.74 (US)")
print("    -> admin ∝ sales^(<1) unless measured differently: tension with beta<=1 (needs beta>1, or w not ∝ sales)")
print("(D) Kelly with overround")
for t in range(5):
    m=rng.integers(2,6); p=rng.dirichlet(np.ones(m)); v=rng.uniform(0,0.2)
    rt=rng.dirichlet(np.ones(m)) if t<3 else 0.9*p+0.1*rng.dirichlet(np.ones(m)); r=rt*(1+v); o=1/r  # t>=3: near-efficient market
    th=(p*np.log(p/rt)).sum()-np.log(1+v)
    # numeric optimum over portfolios b (bet all wealth): maximize sum p log(b o)
    best=-np.inf
    for _ in range(20000):
        b=rng.dirichlet(np.ones(m)); best=max(best,(p*np.log(b*o)).sum())
    # side info Y: noisy copy
    eps=rng.uniform(0,0.5); C=(1-eps)*np.eye(m)+eps/m
    Jxy=p[:,None]*C; py=Jxy.sum(0); I=(Jxy*np.log(Jxy/(p[:,None]*py[None,:]))).sum()
    Gside=sum(py[y]*((Jxy[:,y]/py[y])*np.log((Jxy[:,y]/py[y])*o)).sum() for y in range(m))
    # MC wealth with proportional betting given y
    T=200000; x=rng.choice(m,size=T,p=p); 
    yy=np.array([rng.choice(m,p=C[xi]) for xi in x[:20000]]); 
    post=Jxy/py[None,:]
    mc=np.mean(np.log(post[x[:20000],yy]*o[x[:20000]]))
    ok=best<=th+1e-9 and th-best<0.02 and abs(Gside-(th+I))<1e-9 and abs(mc-(th+I))<0.05; allok&=ok
    print(f"  m={m} v={v:.3f} D-ln(1+v)={th:+.4f} (num max {best:+.4f}) I={I:.4f} G_side={Gside:+.4f}=D-ln(1+v)+I  MC={mc:+.4f} blind viable={th>0} {'OK' if ok else 'FAIL'}")
print("  information value is LINEAR (slope 1 nat/nat) in Kelly: with linear cost kappa*I the choice is bang-bang at kappa=1")
print("ALL","OK" if allok else "FAIL")
