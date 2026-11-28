"""C2: optimal causal (Wiener) filter for a power-law world S_x ~ q|w|^-alpha observed in white noise N.
(a) MMSE e* = q^(1/alpha) N^(1-1/alpha) / sin(pi/alpha)  [continuous time; cf. Afterman et al. Thm 2.5 eq 2.8]
    checked by discrete-time spectral formula (Kolmogorov-Szego innovations variance) as dt->0 AND by
    direct time-domain Gaussian conditioning on simulated-covariance fBm.
(b) kernel tail: weight on an observation of age tau decays as tau^-(1+alpha/2) for tau >> tau_c=(N/q)^(1/alpha),
    exponential iff alpha/2 is an integer (alpha=2: Kalman EWMA)."""
import numpy as np, json
from math import gamma, sin, pi
M=2**22
th=2*pi*(np.arange(M)+0.5)/M; th=np.where(th>pi,th-2*pi,th)   # half-bin offset avoids theta=0
def S_x(theta,alpha,qd,eps=0.0): return qd*(4*np.sin(theta/2)**2+eps**2)**(-alpha/2)
def innov_and_kernel(alpha,qd,Nd,K=200000):
    Sy=S_x(th,alpha,qd)+Nd
    L=np.log(Sy); c=np.fft.ifft(L).real          # cepstrum c_k (real, symmetric)
    log_s2=c[0]; s2=np.exp(log_s2)                # innovations variance sigma_eps^2
    # log A(z) = sum_{k>=1} c_k z^-k  (A monic, minimum phase);  1/A = exp(-log A)
    cc=np.zeros(M); cc[1:M//2]=c[1:M//2]
    logA=np.fft.fft(cc)                            # evaluated on grid (with conj convention irrelevant for magnitudes)
    g=np.fft.ifft(np.exp(-logA))                   # impulse response of 1/A
    g=g.real[:K]
    h=-(Nd/s2)*g; h[0]+=1.0                        # K = 1 - (Nd/s2)/A
    return s2,h
res={"mmse":{},"kernel":{}}
# (a) MMSE, continuum limit: q=N=1 -> e* = 1/sin(pi/alpha)
for alpha in (1.5,2.0,2.5,3.0):
    row={}
    for dt in (1e-2,1e-3,1e-4):
        qd=dt**(alpha-1); Nd=1/dt
        s2,_=innov_and_kernel(alpha,qd,Nd,K=10)
        e=Nd*(1-Nd/s2)
        row[str(dt)]=round(float(e),5)
    row["predicted"]=round(1/sin(pi/alpha),5); res["mmse"][str(alpha)]=row
# (a') direct time-domain conditioning (fBm, x_0 = 0), discrete samples dt, n points; estimate x_n from y_1..y_n
def td(alpha,dt,n):
    H=(alpha-1)/2
    # continuum: Var x(t) = sig2 t^{2H} with sig2 = q/(Gamma(alpha) sin(pi(alpha-1)/2))
    sig2=1.0/(gamma(alpha)*sin(pi*(alpha-1)/2))
    t=dt*np.arange(1,n+1)
    C=0.5*sig2*(t[:,None]**(2*H)+t[None,:]**(2*H)-np.abs(t[:,None]-t[None,:])**(2*H))
    Cy=C+np.eye(n)/dt
    w=np.linalg.solve(Cy,C[:,-1])
    return float(C[-1,-1]-C[-1]@w), w[::-1]
for alpha in (1.5,2.5):
    e,w=td(alpha,0.01,3000)
    res["mmse"][str(alpha)]["time_domain_dt0.01_n3000"]=round(e,5)
# (b) kernel tail exponents (discrete, q_d = 1, N_d chosen so tau_c ~ 10 samples)
for alpha in (0.4,0.8,1.5,2.0,2.5,3.5):
    tau_c=10.0; Nd=tau_c**alpha   # tau_c=(Nd/qd)^(1/alpha)
    s2,h=innov_and_kernel(alpha,1.0,Nd)
    k=np.arange(len(h))
    sel=(k>=20*tau_c)&(k<=20000)
    ah=np.abs(h[sel]); kk=k[sel]
    slope=np.polyfit(np.log(kk),np.log(ah),1)[0]
    # local slopes in 3 windows
    loc=[]
    for a,b in ((200,800),(2000,8000),(8000,20000)):
        s=(k>=a)&(k<=b); loc.append(round(float(np.polyfit(np.log(k[s]),np.log(np.abs(h[s])+1e-300),1)[0]),3))
    # exponential test: log|h| vs k linear fit quality in window
    s=(k>=20)&(k<=200)
    expo=np.polyfit(k[s],np.log(np.abs(h[s])+1e-300),1)[0]
    res["kernel"][str(alpha)]=dict(predicted_tail_exponent=-(1+alpha/2),fitted_tail_200_20000=round(float(slope),3),
        local_slopes=loc,sign_of_tail=int(np.sign(np.median(h[sel]))),h_at_1000=float(h[1000]),h_at_10000=float(h[10000]),
        exp_rate_20_200=round(float(expo),4))
print(json.dumps(res,indent=1))
