"""i4: non-stationary / unstable worlds (data-rate route).
(a) KNOWN (Nair-Evans 2004 type): x'=a x+w (var q). To hold one-step error variance P, any tracker needs
    R >= log2|a| + 1/2 log2(1+q/(a^2 P)) bits/step  (Gaussian-tight, EPI lower bound otherwise).  Check with an
    R-bit adaptive uniform quantizer (MC): error >= bound; noise-free divergence iff R < log2|a|.
(b) multi-mode random-walk world q_i = i^-beta, cost per step  w*sum P_i + kappa*sum rate_i(P_i):
    asymptotic total rate ∝ (w/kappa)^(1/beta)  (the stationary exponent survives a=1), with a sqrt-law pre-asymptote.
(c) unstable modes add a stakes-independent floor sum log2 a_i -> minimum viable throughput; share curve."""
import numpy as np
rng=np.random.default_rng(5); allok=True; LN2=np.log(2)
print("(a) quantized tracking of x'=a x + w")
def track(a,q,R,T=60000):
    # error coordinates: e = x - a*xhat_prev ; designed R-bit uniform quantizer on +-4 sigma_pred
    err=0.0; P=q; L=2**R; errs=[]
    for t in range(T):
        e=a*err+np.sqrt(q)*rng.standard_normal()
        sp=np.sqrt(a*a*P+q); s=4*sp
        c=np.clip(np.floor((e+s)/(2*s)*L),0,L-1); eh=-s+(c+0.5)*2*s/L
        err=e-eh; errs.append(err*err)
        P=16*sp*sp/(3*L*L)
        if abs(e)>s: P=max(P,err*err)*4
        if not np.isfinite(err) or abs(err)>1e60: return np.inf
    return np.mean(errs[T//2:])
for a,q,R in [(1.0,1.0,1),(1.0,1.0,2),(1.0,1.0,3),(1.5,1.0,1),(1.5,1.0,2),(1.5,1.0,3),(3.0,1.0,2),(3.0,1.0,3)]:
    Pb=q/(2**(2*R)-a*a) if 2**(2*R)>a*a else np.inf
    P=track(a,q,R,T=60000)
    ok=P>=Pb*(1-0.02); allok&=ok   # bound must hold; practical quantizer may be far above or unstable
    print(f"  a={a} R={R}b: MC error var={P:9.4f}  lower bound q/(4^R-a^2)={Pb:9.4f}  {'OK' if ok else 'FAIL'}")
# noise-free: divergence iff R<log2 a ; use a=3 (log2=1.585): R=1 diverges in ratio, R=2 converges
for a,R in [(3.0,1),(3.0,2),(1.5,1)]:
    err=rng.uniform(-1,1); s=1.0*a; L=2**R; hist=[abs(err)]
    for t in range(120):
        e=a*err
        c=np.clip(np.floor((e+s)/(2*s)*L),0,L-1); eh=-s+(c+0.5)*2*s/L; err=e-eh
        s=1.05*a*s/L; hist.append(abs(err))   # 5% safety margin on the zoom
    conv = hist[-1]<1e-6
    ok = conv==(R>np.log2(a)); allok&=ok
    print(f"  noise-free a={a}, R={R}: absolute error after 120 steps {hist[-1]:.2e}; data-rate theorem says {'stable' if R>np.log2(a) else 'unstable'} {'OK' if ok else 'FAIL'}")
print("(b) random-walk modes q_i=i^-beta: optimal P_i solves P^2+qP-q*theta=0, theta=kappa/(2 ln2 w)")
def total_rate(theta,q,a=1.0):
    P=(-q+np.sqrt(q*q+4*q*theta))/2 if a==1.0 else None
    return (0.5*np.log2(1+q/P)).sum()
N=2*10**6; i=np.arange(1,N+1)
for beta in [0.8,1.0,1.5,2.5,3.0]:
    q=i**(-beta)
    qN=q[-1]; th=np.logspace(-1,np.log10(30*qN),9) if beta<2 else np.logspace(-3,-9,9)
    R=np.array([total_rate(t,q) for t in th])
    sl=np.polyfit(np.log(1/th[-4:]),np.log(R[-4:]),1)[0]; sl0=np.polyfit(np.log(1/th[:3]),np.log(R[:3]),1)[0]
    th_exp=1/beta if beta>2 else 0.5
    ok=abs(sl-th_exp)<0.07; allok&=ok
    print(f"  beta={beta}: local exponent dlogR/dlog(w/kappa): early {sl0:.3f}, late {sl:.3f}; theory min(1/2,1/beta)={th_exp:.3f} (beta<=2: tail-dominated, needs cutoff N) {'OK' if ok else 'FAIL'}")
print("  beta<=2: sum_i sqrt(q_i) diverges -> with unbounded per-mode loss an infinite random-walk world is NOT viable; exponent 1/2 = EOQ/sqrt law")
print("(c) unstable floor + share curve: share(Q) = kappa*(F + c*(Q/kappa)^(1/beta))/Q, F = sum log2 a_i")
F=5.0; kappa=1.0; c=0.7
for beta in [0.7,1.0,1.5]:
    Q=np.logspace(0,8,400); share=kappa*(F+c*(Q/kappa)**(1/beta))/Q
    k=np.argmin(share)
    interior = 0<k<len(Q)-1
    Qstar=kappa*(F*beta/(c*(1-beta)))**beta if beta<1 else np.inf
    ok = interior==(beta<1) and (beta>=1 or abs(np.log(Q[k]/Qstar))<0.1); allok&=ok
    print(f"  beta={beta}: share minimum interior={interior} at Q={Q[k]:.3g} (theory Q*={Qstar:.3g}) {'OK' if ok else 'FAIL'}")
print("  viability with margin mu per unit Q: Q_min = kappa*F/mu (stakes-independent survival tax, Nair-Evans floor)")
print("ALL","OK" if allok else "FAIL")
