"""C3: how many exponential memory stores (layers) does a cost-optimal tracker use, given the world's spectrum?
World: S_x = q (4 sin^2(th/2) + wmin^2)^(-alpha/2) (power law over span tau_c..tau_max=1/wmin), white obs noise Nd.
Agent: xhat = w0*y + sum_j w_j EWMA_j(y), K stores with free rates (init geometric). Excess MSE over the Wiener optimum.
Cost: psi*excess/e_opt + K  (psi = stakes*e_opt/upkeep per store). Prediction: alpha=2 -> K*=1 at every span and psi
(rational spectrum, McMillan degree 1); alpha!=2 -> K* grows with log-span and log psi (approximation theory + price)."""
import numpy as np, json
from scipy.optimize import minimize
G=3000
th=np.logspace(-9,np.log10(np.pi),G); wq=np.zeros(G); _d=np.diff(th); wq[:-1]+=_d/2; wq[1:]+=_d/2   # trapezoid on (0,pi]
TAU_C=4.0; NFIR=4   # free short-lag FIR taps (lags 0..3) absorb sub-tau_c structure; layers = EWMA stores
def setup(alpha,L,q=1.0,Nd=None):
    Nd=TAU_C**alpha if Nd is None else Nd
    wmin=10.0**(-L)/TAU_C; Sx=q*(4*np.sin(th/2)**2+wmin**2)**(-alpha/2)
    Sy=Sx+Nd; s2=np.exp(np.sum(np.log(Sy)*wq)/np.pi); eopt=Nd*(1-Nd/s2)
    return Sx,Nd,eopt
def mse_for_rates(lams,Sx,Nd):
    z=np.exp(-1j*th)
    cols=[z**k for k in range(NFIR)]+[(1-np.exp(-l))/(1-np.exp(-l)*z) for l in lams]
    A=np.array(cols)                      # (K+1) x G transfer functions of each component
    # MSE(w) = (1/pi) int |1 - w.A|^2 Sx + |w.A|^2 Nd ; quadratic in real w
    Sy=Sx+Nd
    Q=np.real((A[:,None,:]*np.conj(A[None,:,:]))*Sy*wq).sum(-1)/np.pi
    b=np.real(A*Sx*wq).sum(-1)/np.pi
    c=np.sum(Sx*wq)/np.pi
    w=np.linalg.lstsq(Q,b,rcond=1e-13)[0]
    return float(c-2*w@b+w@Q@w)
def best_K(alpha,L,K):
    Sx,Nd,eopt=setup(alpha,L)
    best=(np.inf,None)
    for l1 in np.logspace(-1.5,-0.3,5):          # fastest store rate
        for r in np.logspace(0.2,1.6,8):     # rate ratio between stores
            lams=l1/r**np.arange(K)
            if lams[-1]<10.0**(-L-1)/TAU_C: continue
            m=mse_for_rates(lams,Sx,Nd)
            if m<best[0]: best=(m,lams)
    if K>=2:   # free-rate polish
        f=lambda x: mse_for_rates(np.exp(x),Sx,Nd)
        o=minimize(f,np.log(best[1]),method="Nelder-Mead",options=dict(maxiter=150*K,xatol=1e-3,fatol=1e-12))
        if o.fun<best[0]: best=(o.fun,np.exp(o.x))
    return (best[0]-eopt)/eopt, best[1]
out={}
import sys
for alpha in [float(sys.argv[1])]:
    for L in (1,2,3,4):
        ex=[];rates=[]
        for K in range(1,7):
            e,l=best_K(alpha,L,K); ex.append(max(e,0.0)); rates.append(l)
        row={"rel_excess":[float(f"{x:.3g}") for x in ex]}
        for psi in (1e2,1e3,1e4,1e5):
            J=[psi*x+K for K,x in zip(range(1,7),ex)]; Ks=int(np.argmin(J))+1
            lam=np.sort(rates[Ks-1])[::-1]; ratio=float(np.exp(np.mean(np.diff(-np.log(lam))))) if Ks>1 else None
            row[f"Kstar_psi{psi:.0e}"]=Ks; row[f"mean_rate_ratio_psi{psi:.0e}"]=None if ratio is None else round(ratio,2)
        out[f"alpha{alpha}_L{L}"]=row; print(f"alpha{alpha}_L{L}",json.dumps(row),flush=True)
json.dump(out,open(f"c3_layers_{sys.argv[1]}.json","w"),indent=1)
