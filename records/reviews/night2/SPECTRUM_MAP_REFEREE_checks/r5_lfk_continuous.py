"""Referee check R5: independent continuous-time re-derivation of the LFK-alpha exponent.
World S(w) = A * tau_E * (1+(w tau_E)^2)^(-alpha/2), normalized to unit variance (A by quadrature) OR to fixed
high-frequency level q (A*tau_E^(1-alpha) = 1). White noise N=1. Tracker: EWMA with time constant tau (continuous),
error(tau) = int_0^inf [ (w tau)^2/(1+(w tau)^2) S + N/(1+(w tau)^2) ] dw/pi.  Optimal causal filter MSE by
Yovits-Jackson e = (N/pi) int_0^inf ln(1+S/N) dw; its timescale proxy = e/N (Kalman: e/N = tau_m for OU)."""
import numpy as np, json
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
def make_S(alpha,tE,norm):
    f=lambda w: tE*(1+(w*tE)**2)**(-alpha/2)
    if norm=="var":
        v=quad(lambda u: f(np.exp(u))*np.exp(u),-60,60,limit=400)[0]/np.pi; A=1/v
    else: A=tE**(alpha-1)  # so that S ~ w^-alpha with unit coefficient at high w
    return lambda w: A*f(w)
def I(g): return quad(lambda u: g(np.exp(u))*np.exp(u),-60,60,limit=800,epsabs=0,epsrel=1e-10)[0]/np.pi
def ewma_err(tau,S,N=1.0): return I(lambda w: (w*tau)**2/(1+(w*tau)**2)*S(w)+N/(1+(w*tau)**2))
def tau_ewma(S):
    o=minimize_scalar(lambda x: ewma_err(np.exp(x),S),bounds=(-20,40),method="bounded",options=dict(xatol=1e-7)); return np.exp(o.x)
def yj(S,N=1.0): return N*I(lambda w: np.log1p(S(w)/N))
out={}
tEs=np.logspace(4,10,4)
for norm in ("var","q"):
    for alpha in (1.5,2.0,2.5,3.5):
        te=[tau_ewma(make_S(alpha,t,norm)) for t in tEs]; eo=[yj(make_S(alpha,t,norm)) for t in tEs]
        sl=lambda y: [round(float(x),3) for x in np.diff(np.log(y))/np.diff(np.log(tEs))]
        out[f"{norm}_{alpha}"]=dict(ewma_tau_slopes=sl(te),optimal_mse_over_N_slopes=sl(eo),
            pred_var_norm=round(min(1-1/alpha,2/3),3) if norm=="var" else 0.0, pred_mse=(round((1-alpha)/alpha,3) if norm=="var" else 0.0))
        print(norm,alpha,out[f"{norm}_{alpha}"],flush=True)
json.dump(out,open("r5_lfk_continuous.json","w"),indent=1)
