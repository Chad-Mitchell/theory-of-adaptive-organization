"""SPECTRUM-MAP-FIXES own checks (pick 26). Own code; imports nothing from the repo. Seed 20261127.
A  item 4: survival exponent of ARFIMA(0,d,0) AR(inf) weights (tail k^-(1+d), d = alpha/2) is -d = -alpha/2.
B  item 5: one-store knife-edge near alpha = 2. B1 scale-free continuous-time world S=|w|^-alpha, N=1, one unit-gain EWMA
   (closed form + quadrature) vs optimal causal MMSE 1/sin(pi/alpha). B2 own discrete-time model (free taps + 1 weighted EWMA,
   finite span) on a different grid. Fit excess ~ c (alpha-2)^2.
B3 item 5: log-decrements of committed c3_layers_1.5 rel_excess at L = 4 (read-only) vs 2 pi^2/ln(8R).
C  item 6: EWMA optimal memory time vs tau_E at fixed variance (slope 1-1/alpha) and at fixed high-frequency level q (slope 0;
   alpha=3.5: -1/6).
D  item 7: pure Cox (rate-modulated) binary daily series: Spearman(beta, a_need) sign, and gap-shuffle delta beta at beta~0.2.
"""
import numpy as np, json, math, sys
from scipy import integrate, optimize, special
from scipy.stats import spearmanr
R={}
# ---------- A
A={}
for alpha in (1.5,2.5,3.0,3.5):
    d=alpha/2; K=np.arange(1,2_000_001,dtype=float)
    lw=special.gammaln(K-d)-special.gammaln(K+1)   # |pi_k| up to the constant 1/|Gamma(-d)|
    w=np.exp(lw); tail=np.cumsum(w[::-1])[::-1]   # sum_{j>=k}^{2e6}
    tail=tail+ (K[-1]**(-d))/d                     # remainder ~ int_{Kmax} x^{-1-d}
    k1,k2=1000,100000
    A[str(alpha)]=dict(survival_slope=round(float(np.log(tail[k2-1]/tail[k1-1])/np.log(k2/k1)),4),theory=-d,
                       density_slope=round(float((lw[k2-1]-lw[k1-1])/np.log(k2/k1)),4),theory_density=-(1+d))
R["A_survival"]=A
# ---------- B1
def ewma_mse_closed(tau,a): return tau**(a-1)/(-2*np.cos(np.pi*a/2))+1/(2*tau)
def ewma_mse_quad(tau,a):
    f=lambda w:(w*w*tau*tau/(1+w*w*tau*tau))*w**(-a)+1/(1+w*w*tau*tau)
    v=integrate.quad(f,0,1,limit=200)[0]+integrate.quad(f,1,np.inf,limit=200)[0]
    return v/np.pi
B1={}
for a in (1.8,1.9,1.95,1.99,2.0,2.01,2.05,2.1,2.2):
    o=optimize.minimize_scalar(lambda lt:ewma_mse_closed(np.exp(lt),a),bounds=(-5,5),method="bounded")
    m=o.fun; mq=ewma_mse_quad(np.exp(o.x),a); e=1/np.sin(np.pi/a)
    B1[str(a)]=dict(excess=float(f"{m/e-1:.4g}"),quad_check=float(f"{mq/e-1:.4g}"),c=None if a==2 else round((m/e-1)/(a-2)**2,4))
R["B1_scalefree_single_ewma"]=B1
# ---------- B2 own discrete model: x has S(th)=(4sin^2(th/2)+wmin^2)^(-a/2); y=x+white(Nd); estimator = 4 FIR taps + 1 weighted EWMA
th=np.concatenate([np.logspace(-10,-2,4000,endpoint=False),np.linspace(1e-2,np.pi,6000)])
wt=np.gradient(th)
def B2(a,L,taus=4.0):
    wmin=10.0**(-L)/taus; Sx=(4*np.sin(th/2)**2+wmin**2)**(-a/2); Nd=taus**a; Sy=Sx+Nd
    eopt=Nd*(1-Nd/np.exp(np.sum(np.log(Sy)*wt)/np.pi))
    z=np.exp(-1j*th)
    def mse(lam):
        cols=[z**k for k in range(4)]+[(1-np.exp(-lam))/(1-np.exp(-lam)*z)]
        Am=np.array(cols); Q=np.real(Am[:,None]*np.conj(Am[None])*Sy*wt).sum(-1)/np.pi
        b=np.real(Am*Sx*wt).sum(-1)/np.pi; c=np.sum(Sx*wt)/np.pi
        w=np.linalg.solve(Q,b); return c-w@b
    o=optimize.minimize_scalar(lambda ll:mse(np.exp(ll)),bounds=(np.log(10.0**(-L-1)/taus),0),method="bounded")
    return (o.fun-eopt)/eopt
B2r={}
for L in (2,4):
    for a in (1.8,1.9,1.95,2.0,2.05,2.1,2.2):
        ex=B2(a,L); B2r[f"L{L}_a{a}"]=dict(excess=float(f"{ex:.3g}"),c=None if a==2 else round(ex/(a-2)**2,4))
R["B2_discrete_taps_plus_one_ewma"]=B2r
# ---------- B3
ex=[0.0103,0.00116,0.000178,3.11e-05,5.97e-06,1.42e-06]   # committed c3_layers_1.5.out, alpha1.5_L4 rel_excess K=1..6
Rspan=10**4; R["B3_rate"]=dict(log_decrements=[round(math.log(ex[i]/ex[i+1]),3) for i in range(5)],predicted=round(2*math.pi**2/math.log(8*Rspan),3))
# ---------- C
def ewma_tau(a,tauE,mode):
    if mode=="var":  S=lambda w: tauE*(1+(w*tauE)**2)**(-a/2)
    else:            S=lambda w: tauE**a*(1+(w*tauE)**2)**(-a/2)   # high-frequency level q = 1 fixed
    def mse(lt):
        t=np.exp(lt); f=lambda u:((u*u/(1+u*u))*S(u/t)+1/(1+u*u))/t   # w = u/t
        br=[0,1e-3,1,1e3,np.inf]; return sum(integrate.quad(f,br[i],br[i+1],limit=400)[0] for i in range(4))/np.pi
    o=optimize.minimize_scalar(mse,bounds=(-20,40),method="bounded",options=dict(xatol=1e-7)); return o.x
C={}
for mode in ("var","q"):
    for a in (1.5,2.0,2.5,3.5):
        t1,t2=ewma_tau(a,1e7,mode),ewma_tau(a,1e8,mode)
        th_=(min(1-1/a,2/3) if mode=="var" else (0.0 if a<3 else (3-a)/3))
        C[f"{mode}_a{a}"]=dict(slope=round((t2-t1)/math.log(10),3),theory=round(th_,3))
R["C_memory_time_slope"]=C
# ---------- D
rng=np.random.default_rng(20261127)
def pinkgauss(n,g):
    f=np.fft.rfftfreq(n); amp=np.zeros_like(f); amp[1:]=f[1:]**(-g/2)
    x=np.fft.irfft(amp*(rng.normal(size=f.size)+1j*rng.normal(size=f.size)),n); return (x-x.mean())/x.std()
def beta_band(s):
    n=len(s); P=np.abs(np.fft.rfft(s-s.mean()))**2; f=np.fft.rfftfreq(n)
    m=(f>=1/730)&(f<=0.5); lf=np.log(f[m]); lp=np.log(P[m])
    edges=np.linspace(lf.min(),lf.max(),21); idx=np.digitize(lf,edges)
    X=[lf[idx==i].mean() for i in range(1,21) if np.any(idx==i)]; Y=[lp[idx==i].mean() for i in range(1,21) if np.any(idx==i)]
    return -np.polyfit(X,Y,1)[0]
def a_need(s,Lmax=365):
    ev=np.flatnonzero(s); g=np.diff(ev)
    L=np.arange(1,Lmax+1); ge=np.array([(g>=l).sum() for l in L]); eq=np.bincount(g,minlength=Lmax+2)[1:Lmax+1]
    ok=(ge>=20)&(eq>0); return -np.polyfit(np.log(L[ok]),np.log(eq[ok]/ge[ok]),1)[0]
def shuffled(s):
    ev=np.flatnonzero(s); g=np.diff(ev); rng.shuffle(g); t=np.concatenate([[ev[0]],ev[0]+np.cumsum(g)]); o=np.zeros_like(s); o[t]=1; return o
rows=[]
for i in range(24):
    n=4096; g=rng.uniform(0.8,1.8); sd=rng.uniform(0.5,2.0); p0=rng.uniform(0.02,0.15)
    pb=[];sb=[];ab=[]
    for f in range(8):    # 8 "files" per repo share nothing; average estimates
        lam=np.clip(p0*np.exp(sd*pinkgauss(n,g)-sd*sd/2),0,1); s=(rng.random(n)<lam).astype(float)
        if s.sum()<60: continue
        pb.append(beta_band(s)); sb.append(beta_band(shuffled(s))); ab.append(a_need(s))
    if len(pb)>=4: rows.append(dict(gamma=round(g,3),sd=round(sd,3),p0=round(p0,3),beta=float(np.mean(pb)),beta_shuf=float(np.mean(sb)),a=float(np.mean(ab))))
b=np.array([r["beta"] for r in rows]); a=np.array([r["a"] for r in rows]); dl=b-np.array([r["beta_shuf"] for r in rows])
rho,p=spearmanr(b,a); near=(b>0.12)&(b<0.32)
R["D_cox"]=dict(n=len(rows),spearman_beta_a=round(float(rho),3),p=float(f"{p:.2g}"),
   delta_beta_near_beta_0p2=[round(float(x),3) for x in dl[near]],beta_near=[round(float(x),3) for x in b[near]],
   delta_over_beta_median_all=round(float(np.median(dl/b)),3),rows=rows)
json.dump(R,open("fixes_check.json","w"),indent=1)
for k,v in R.items():
    if k=="D_cox": print(k,json.dumps({x:y for x,y in v.items() if x!="rows"}))
    else: print(k,json.dumps(v))
