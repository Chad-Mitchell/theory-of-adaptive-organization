"""C5: generalizing Lee-Flack-Krakauer (2024) tau_m ~ tau_E^(1/2).
World: stationary, unit variance, spectrum cornered at 1/tau_E with high-frequency slope alpha:
  S_x(w) = C (1+(w tau_E)^2)^(-alpha/2); white observation noise N per sample (discrete time, w in (0,pi]).
Prediction: optimal memory timescale tau_m ~ tau_E^(1-1/alpha) = tau_E^(2H/(1+2H)) (alpha=1+2H); for an EWMA-restricted agent the
exponent is min(1-1/alpha, 2/3). alpha=2 (telegraph/OU, LFK's case) gives 1/2."""
import numpy as np, json
from scipy.optimize import minimize_scalar
G=20000; th=np.logspace(-12,np.log10(np.pi),G); wq=np.gradient(th)
def Sx(alpha,tE):
    s=(1+(th*tE)**2)**(-alpha/2); return s/(np.sum(s*wq)/np.pi)
def ewma_mse(lam,S,N):
    r=np.exp(-lam); z=np.exp(-1j*th); Kf=(1-r)/(1-r*z)
    return np.sum((np.abs(1-Kf)**2*S+np.abs(Kf)**2*N)*wq)/np.pi
def opt_tau_ewma(alpha,tE,N=1.0):
    S=Sx(alpha,tE); f=lambda x: ewma_mse(np.exp(x),S,N)
    o=minimize_scalar(f,bounds=(np.log(1e-9),np.log(3)),method="bounded",options=dict(xatol=1e-6)); return float(np.exp(-o.x))
M=2**22; thg=2*np.pi*(np.arange(M)+0.5)/M; thg=np.where(thg>np.pi,thg-2*np.pi,thg)
def opt_filter_halfage(alpha,tE,N=1.0):
    s=(1+(np.abs(thg)*tE)**2)**(-alpha/2); s=s/np.mean(s)
    Sy=s+N; c=np.fft.ifft(np.log(Sy)).real; s2=np.exp(c[0])
    cc=np.zeros(M); cc[1:M//2]=c[1:M//2]; g=np.fft.ifft(np.exp(-np.fft.fft(cc))).real
    h=-(N/s2)*g; h[0]+=1.0; h=h[:M//2]
    cw=np.cumsum(np.abs(h)); return float(np.searchsorted(cw,0.5*cw[-1])), float(N*(1-N/s2))
out={}
tEs=np.logspace(2,8,13)
for alpha in (1.5,2.0,2.5,3.5,4.0):
    te=[opt_tau_ewma(alpha,t) for t in tEs]
    sl=np.diff(np.log(te))/np.diff(np.log(tEs))
    row=dict(pred_opt=round(1-1/alpha,3),pred_ewma=round(min(1-1/alpha,2/3),3),
             ewma_local_slopes=[round(float(x),3) for x in sl],ewma_tau=[round(x,1) for x in te])
    tE2=np.logspace(2,5,7); ha=[];er=[]
    for t in tE2:
        a,e=opt_filter_halfage(alpha,t); ha.append(a); er.append(e)
    row["opt_halfage_local_slopes"]=[round(float(x),3) for x in np.diff(np.log(ha))/np.diff(np.log(tE2))]
    row["opt_mse_local_slopes"]=[round(float(x),3) for x in np.diff(np.log(er))/np.diff(np.log(tE2))]
    row["pred_mse_slope"]=round((1-alpha)/alpha,3)
    out[str(alpha)]=row; print(alpha,json.dumps(row),flush=True)
json.dump(out,open("c5_lfk.json","w"),indent=1)
